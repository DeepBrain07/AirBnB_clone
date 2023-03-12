#!/usr/bin/python3
""" Command interprenter """
import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def inst_checker(arg):
    """ checks if an instance exists """
    temp_storage = storage.all()
    for key, value in temp_storage.items():
        obj_name = value.__class__.__name__
        if obj_name == arg:
            return True
    return False


def id_checker(arg):
    """ checks if an id exists """
    temp_storage = storage.all()
    for key, value in temp_storage.items():
        obj_id = value.id
        if obj_id == arg:
            return True
    return False


ob_list = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
ob_dct = {"BaseModel": BaseModel,
          "User": User,
          "State": State,
          "City": City,
          "Amenity": Amenity,
          "Place": Place,
          "Review": Review}
com_list1 = ["all", "count"]
com_list2 = ["create", "show", "destroy"]


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def precmd(self, line):
        """ precmd modification """
        if '.' in line and '(' in line and ')' in line:
            s_arg1 = line.split('(')  # ["cls.mthd", "args)"]
            s_arg2 = s_arg1[1].split(')')  # ["args"]
            s_arg3 = s_arg1[0].split('.')  # ["cls", "mthd"]
            id_arg = s_arg2[0]  # "args"
            if '{' not in id_arg and '}' not in id_arg:
                s_arg4 = id_arg.split(", ")  # ["id", "att_name", "att_value"]
            else:
                s_arg4 = id_arg.split(", ", 1)
            cls_name = s_arg3[0].strip('"')
            mthd = s_arg3[1].strip('"')
            if cls_name in ob_list and mthd in com_list1:
                args = mthd + " " + cls_name
                return args
            elif cls_name in ob_list and mthd in com_list2:
                args = mthd + " " + cls_name + " " + id_arg.strip('"')
                return args
            elif cls_name in ob_list and mthd == 'update':
                id_arg = s_arg4[0].strip('"')
                att_name = s_arg4[1].strip('"')
                att_value = s_arg4[2]
                args = mthd + " " + cls_name + " " + id_arg + " " + \
                    att_name + " " + att_value
                return args
            else:
                return line
        else:
            return line

    def do_EOF(self, line):
        """ quits """
        print('')
        return True

    def do_quit(self, line):
        """ quits """
        return True

    def do_create(self, line):
        """ creates an instance """
        s_line = line.split()
        if len(s_line) == 0:
            print("** class name missing **")
        elif len(s_line) > 0 and s_line[0] not in ob_list:
            print("** class doesn't exist **")
        else:
            temp = s_line[0]
            obj = ob_dct[temp]()
            print(obj.id)
            obj.save()

    def do_count(self, line):
        """ counts the number of instances created """
        s_line = line.split()
        temp_storage = storage.all()
        count = 0
        for key, value in temp_storage.items():
            obj_name = value.__class__.__name__
            if obj_name == s_line[0]:
                count += 1
        print(count)

    def do_show(self, line):
        """shows an instance with the specified id """
        s_line = line.split()
        if len(s_line) == 0:
            print("** class name missing **")
        elif len(s_line) > 0 and inst_checker(s_line[0]) is False:
            print("** class doesn't exist **")
        elif len(s_line) > 0 and len(s_line) < 2:
            print("** instance id missing **")
        else:
            temp_storage = storage.all()
            for key, value in temp_storage.items():
                obj_name = value.__class__.__name__
                obj_id = value.id
                if obj_name == s_line[0] and obj_id == s_line[1].strip('"'):
                    print(value)
                    return
            print("** no instance found **")

    def do_destroy(self, line):
        """ destroys an instance with the specified id """
        s_line = line.split()
        if len(s_line) == 0:
            print("** class name missing **")
        elif len(s_line) > 0 and inst_checker(s_line[0]) is False:
            print("** class doesn't exist **")
        elif len(s_line) > 0 and len(s_line) < 2:
            print("** instance id missing **")
        else:
            temp_storage = storage.all()
            for key, value in temp_storage.items():
                obj_name = value.__class__.__name__
                obj_id = value.id
                if obj_name == s_line[0] and obj_id == s_line[1].strip('"'):
                    del value
                    del storage._FileStorage__objects[key]
                    storage.save()
                    return
            print("** no instance found **")

    def do_all(self, line):
        """ show all instances """
        s_line = line.split()
        if len(s_line) == 0 or s_line[0] == "BaseModel":
            temp_list = []  # Temporary list
            temp_st = storage.all()  # Temporary storage
            for key, value in temp_st.items():
                t_string = value.__str__()  # String representation
                temp_list.append(t_string)
            print(temp_list)
            return
        else:
            temp_list = []
            temp_st = storage.all()
            for key, value in temp_st.items():
                obj_name = value.__class__.__name__
                if obj_name == s_line[0]:
                    t_string = value.__str__()
                    temp_list.append(t_string)
            print(temp_list)
            return
        print("** class doesn't exist **")

    def do_update(self, line):
        """ updates an instance """
        s_line = line.split()
        if len(s_line) == 0:
            print("** class name missing **")
            return
        if inst_checker(s_line[0]) is False:
            print("** class doesn't exist **")
            return
        if len(s_line) < 2:
            print("** instance id missing **")
            return
        if id_checker(s_line[1]) is False:
            print("** no instance found **")
            return
        if len(s_line) < 3:
            print("** attribute name missing **")
            return
        if len(s_line) < 4:
            print("** value missing **")
            return
        attr = s_line[3]
        attr_temp = attr
        attr = attr.strip('"')
        for key, value in storage.all().items():
            id_value = value.id
            if id_value == s_line[1]:
                if attr_temp[0] == '"' or attr_temp[0] == "'":
                    setattr(value, s_line[2], attr)
                else:
                    if "." in attr:
                        try:
                            setattr(value, s_line[2], float(attr))
                        except ValueError:
                            print("ValueError1")
                    else:
                        try:
                            setattr(value, s_line[2], int(attr))
                        except ValueError:
                            print("ValueError2")
                storage.save()
                return

    def help_quit(self):
        print("Quit command to exit the program\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
