#!/usr/bin/python3
""" a program called console.py that
contains the entry point of the command interpreter:
A command interpreter created with cmd uses a loop to
read all lines from its input, parse them, and
then dispatch the command to an appropriate command handler
"""
import cmd
from models import *


class HBNBCommand(cmd.Cmd):
    """defines the HBNBCommand interpreter"""
    prompt = '(hbnb) '

    def do_EOF(self, line):
        """command handler returns a true value,
        the program will exit cleanly
        """
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """ensures an empty line + ENTER doesnt execute anything
        """
        pass

    def do_create(self, line):
        """Command handler creates a new instance of a class,
        saves it to JSON file and prints id"""
        if line == "":
            print("** class name missing **")
        else:
            if line not in storage.classes():
                print("** class doesn't exist **")
            else:
                obj = storage.classes()[line]()
                obj.save()
                print(obj.id)

    def do_show(self, line):
        """Command handler prints the string representation
        of an instance based on the class name and id"""
        arg = line.split()
        if line == "":
            print("** class name missing **")
        elif arg[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        else:
            obj = storage.all()
            key = f"{arg[0]}.{arg[1]}"
            if key not in obj.keys():
                print("** no instance found **")
            else:
                print(obj[key])

    def do_destroy(self, line):
        """Command handler deletes an instance based on the class
        name and id and saves the changes in a JSON file"""
        arg = line.split()
        if line == "":
            print("** class name missing **")
        elif arg[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        else:
            obj = storage.all()
            key = f"{arg[0]}.{arg[1]}"
            if key not in obj.keys():
                print("** no instance found **")
            else:
                del (obj[key])
                storage.save()

    def do_all(self, line):
        """Command handler prints all str representations
        of all instances based or not on the class name"""
        list = []
        arg = line.split()
        objs = storage.all()
        if not arg:
            for key in objs.keys():
                list.append(str(objs[key]))
            print(list)

        elif arg[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            for key in objs.keys():
                kwarg = key.split(".")
                if arg[0] == kwarg[0]:
                    list.append(str(objs[key]))
            print(list)

    def do_update(self, line):
        """Command handler updates an instance based on the class
        name and id by adding or updating an attribute"""
        attr_list = line.split()
        len_attr = len(attr_list)
        # print(self.instance_check(attr_list))
        check, instance_data = self.instance_check(attr_list)
        if check:
            if len_attr < 3:
                return self.print_msg("** attribute name missing **")
            elif len_attr < 4:
                return self.print_msg("** value missing **")
            instance = instance_data[0]
            start = 2
            stop = start + 2
            again = True
            while again:
                attribute_name, attribute_value = attr_list[start:stop]
                if attribute_value[0] == '"' and attr_list[-1] is attribute_value:
                    if attribute_value[-1] == '"':
                        attribute_value = attribute_value[1:-1]
                    else:
                        attribute_value = attribute_value[1:]
                elif attribute_value[0] == '"':
                    start = stop
                    for value in attr_list[start:]:
                        attribute_value = " ".join([attribute_value, value])
                        stop += 1
                        if value[-1] == '"':
                            attribute_value = attribute_value[1:-1]
                            break
                        elif attr_list[-1] is value:
                            attribute_value = "".join([attribute_value, '"'])
                            attribute_value = attribute_value[1:-1]
                setattr(instance, attribute_name, attribute_value)
                if self.update_dict and len(attr_list) > stop:
                    again = True
                    start = stop
                    stop = start + 2
                else:
                    again = False
                    self.update_dict = False
                # obj_dict[key] = instance.to_dict()
            instance.save()

    def instance_check(self, obj):
        """Check and return an instance"""
        i = 0
        len_obj = len(obj)
        class_dict = storage.classes()
        all_objs = storage.all()
        if len_obj == 0:
            self.print_msg("** class name missing **")
            return False, None
        elif obj[i] not in class_dict:
            self.print_msg("** class doesn't exist **")
            return False, None
        elif len_obj == 1:
            self.print_msg("** instance id missing **")
            return False, None
        class_name, obj_id = obj[:2]
        key = ".".join([class_name, obj_id])
        if key not in all_objs:
            self.print_msg("** no instance found **")
            return False, None
        instance = all_objs[key]
        return True, [instance, all_objs, key]

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns. It has been overriden and extended here :)

        """
        cmd_str, full_args = self.parser(line)
        if hasattr(self, cmd_str):
            cmd_fn = getattr(self, cmd_str)
            return cmd_fn(full_args)
        self.stdout.write('*** Unknown syntax: %s\n' % line)

    def parser(self, line):
        obj_type, others = line.split(".")
        cmd_chars = []

        for char in others:
            if char == "(":
                break
            cmd_chars.append(char)
        start = len(cmd_chars)
        args = others[start:]
        args = args[1:-1]
        count = args.count(",")
        if count > 0:
            # print(count)
            args = args.split(",")
            print(args)
            count = args[1].count("{")
            if count > 0:
                obj_id = args[0]
                attr_dict = "".join(args[1:])
                attr_dict = attr_dict.strip()
                attr_dict = attr_dict[1:-1]
                print(attr_dict)
                attr_dict = attr_dict.split(": ")
                attr_dict.insert(0, obj_id)
                args = " ".join(attr_dict)
                self.update_dict = True
                print(attr_dict)
            else:
                args = "".join(args)
            print(args)
            # print(args)
        cmd_str = "".join(cmd_chars)
        cmd_str = "".join(['do_', cmd_str])
        full_args = " ".join([obj_type, args])
        full_args = full_args.strip()
        # self.stdout.write("-%s-\n" % full_args)
        return cmd_str, full_args

    def handle_all(self, args):
        class_dict = storage.classes()
        obj_dict = storage.all()
        all_instances = []
        class_instances = []
        if len(args) == 0:
            for key in obj_dict:
                instance = obj_dict[key]
                all_instances.append(str(instance))
            return all_instances
        else:
            if args not in class_dict:
                return self.print_msg("** class doesn't exist **")
            for key in obj_dict:
                instance_dict = obj_dict[key].to_dict()
                if instance_dict["__class__"] == args:
                    instance = obj_dict[key]
                    class_instances.append(str(instance))
            return class_instances

    def do_count(self, args):
        """Return a count all needed instances"""
        count = len(self.handle_all(args))
        return self.print_msg(count)

    def print_msg(self, msg=None):
        """Called to handle messages"""
        self.stdout.write("{}\n".format(msg))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
