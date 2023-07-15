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
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            objs = storage.all()
            key = "{}.{}".format(args[0], args[1])
            if key not in objs.keys():
                print("** no instance found **")
            else:
                setattr(objs[key], args[2], args[3])
                storage.save()

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

    def do_count(self, args):
        """Return a count all needed instances"""
        count = len(self.handle_all(args))
        return self.print_msg(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
