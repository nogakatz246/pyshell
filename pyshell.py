"""
A linux shell, written in Python2.
"""
import os
import shutil 
import glob


def clean_arguments(arguments):
    """
    Cleans the arguments list - deletes empty arguments ('').
    :param arguments: the list of arguemtns.
    :arguments type: list.
    :returns: None.
    """
    while '' in arguments:
        arguments.remove('')

test
def ls_no_flags(arguments):
    """
    Prints the content of a chosen directory.
    If no directory was specified, displays the current directory.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: None.
    """
    if len(arguments) == 0:
        list_of_files = os.listdir('.')
        print os.getcwd() + ":"
        for file_in_dir in list_of_files:
            print(file_in_dir)
    else:
        for directory in arguments:
            try:
                print directory + ":"
                list_of_files = os.listdir(directory)
                for file_in_dir in list_of_files:
                    print(file_in_dir)
            except OSError:
                print "Directory does not exist!"


def change_dir(arguments):
    """
    Change the current working directory to a selected directory.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: None.
    """
    if len(arguments) != 1:
        print "Error: the cd function should receive 1 argument, received " + str(len(arguments))
    else:
        try:
            os.chdir(arguments[0])
        except OSError:
            print "Directory does not exist!"


def current_dir(arguments):
    """
    Prints the name of the current working directory.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: None.
    """
    print os.getcwd()


def echo(arguments):
    """
    Prints the arguments received from the user.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: None.
    """
    to_echo = ""
    for argument in arguments:
        to_echo += argument + " "
    print to_echo


def python_shell():
    """
    A linux shell implementation in Python2.
    :returns: None.
    """
    # a dictionary to hold all the shell commands and the matching python function.
    command_to_function = {"ls": ls_no_flags, "cd": change_dir, "pwd": current_dir, "echo": echo}

    print "Welcome to the python shell!:)"
    while True:
        command_line = raw_input(os.getcwd() + "  > ")
        splitted_command_line = command_line.split(" ")
        clean_arguments(splitted_command_line)
        command = splitted_command_line[0]
        arguments = splitted_command_line[1:]
        try:
            command_to_function[command](arguments)
        except KeyError:
            print "Pyshell: " + command + " does not exist."


def main():
    python_shell()


if __name__ == "__main__":
    main()
