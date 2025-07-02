"""
A linux shell, written in Python2.
"""
import os
import shutil 
import glob


def ls(arguments):
    """
    Prints the content of a chosen directory.
    If no directory was specified, displays the current directory.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    if len(arguments) == 0:
        arguments.append(".")
    for directory in arguments:
        try:
            if len(arguments) > 1:
                print directory + ":"
            list_of_files = os.listdir(directory)
            for file_in_dir in list_of_files:
                print file_in_dir
        except OSError:
            print "Directory " + directory + " does not exist!"
            return False
    return True


def change_dir(arguments):
    """
    Change the current working directory to a selected directory.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    if len(arguments) > 1:
        print "Error: the cd function should receive 1 argument, received " + str(len(arguments))
        return False 
    if len(arguments) == 0:
        arguments.append(os.getenv('HOME'))
    try:
        os.chdir(arguments[0])
    except OSError:
        print "Directory " + arguments[0] + " does not exist!"
        return False
    return True


def current_dir(arguments):
    """
    Prints the name of the current working directory.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True.
    """
    print os.getcwd()
    return True


def echo(arguments):
    """
    Prints the arguments received from the user.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True.
    """
    print ' '.join(arguments)
    return True


def python_shell():
    """
    A linux shell implementation in Python2.
    :returns: None.
    """
    # a dictionary to hold all the shell commands and the matching python function.
    command_to_function = {
        "ls": ls,
        "cd": change_dir, 
        "pwd": current_dir, 
        "echo": echo
        }

    print "Welcome to the python shell!:)"
    while True:
        command_line = raw_input(os.getcwd() + "  > ")
        splitted_command_line = command_line.split(" ")
        try:
            command = splitted_command_line[0]
            arguments = splitted_command_line[1:]
        except IndexError:
            print "Error: bad command."
            continue
        if command not in command_to_function.keys():
            print "Pyshell: " + command + " does not exist."
        else:
            result = command_to_function[command](arguments)


def main():
    python_shell()


if __name__ == "__main__":
    main()
