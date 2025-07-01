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


def ls_no_flags(command, arguments):
    """
    Prints the content of a chosen directory.
    If no directory was specified, displays the current directory.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    if len(arguments) == 0:
        arguments.append(".")
    for directory in arguments:
        try:
            print directory + ":"
            list_of_files = os.listdir(directory)
            for file_in_dir in list_of_files:
                print(file_in_dir)
        except OSError:
            print "Directory does not exist!"
            return False
        return True


def change_dir(command, arguments):
    """
    Change the current working directory to a selected directory.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    if len(arguments) > 1:
        print "Error: the cd function should receive 1 argument, received " + str(len(arguments))
        return
    if len(arguments) == 0:
        arguments.append(os.getenv('HOME'))
    try:
        os.chdir(arguments[0])
    except OSError:
        print "Directory " + arguments[0] + " does not exist!"
        return False
    return True


def current_dir(command, arguments):
    """
    Prints the name of the current working directory.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True.
    """
    print os.getcwd()
    return True


def echo(command, arguments):
    """
    Prints the arguments received from the user.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: None.
    """
    print ' '.join(arguments)
    return True


def man(command, arguments):
    """
    Prints information about a chosen command.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: None.
    """
    manual = {
        "ls": "Prints the content of a chosen directory.\n" +
        "Usage: ls [directory: default is current directory]",
        "cd": "Changes the current working directory to a chosen directory.\n" +
        "Usage: cd [directory]",
        "pwd": "Prints the name of the current working directory.\n" +
        "Usage: pwd",
        "echo": "Prints the arguments of the command.\n" +
        "Usage: echo [expression...]",
        "man": "Prints information about a chosen command.\n" +
        "Usage: man [command]"
        }
    if len(arguments) == 1:
        try:
            print manual[arguments[0]]
        except KeyError:
            print "Man: " + arguments[0] + " does not exist."
            return False
    else:
        print "Error: man should receive 1 argument, received " + str(len(arguments))
    return True


def history(command, arguments):
    """
    Prints the history of commands.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returne: True.
    """
    if len(arguments) != 1:
        print "Error: history function should not receive any arguments!"
        return False
    history_list = arguments[0]
    for command in history_list:
        print command
    return True


def python_shell():
    """
    A linux shell implementation in Python2.
    :returns: None.
    """
    # a dictionary to hold all the shell commands and the matching python function.
    command_to_function = {
    "ls": ls_no_flags, 
    "cd": change_dir, 
    "pwd": current_dir, 
    "echo": echo,
    "man": man,
    "history": history,
    }
    index = 1

    # a list to hold all the past commands
    history_list = []
    
    print "Welcome to the python shell!:)"
    while True:
        command_line = raw_input(os.getcwd() + "  > ")
        history_list.append(str(index) + ". " + command_line)
        splitted_command_line = command_line.split(" ")
        command = splitted_command_line[0]
        arguments = splitted_command_line[1:]
        try:
            if command == "history":
                arguments.append(history_list)
            result = command_to_function[command](command, arguments)
            if not result:
                print "Error while executing command: " + command
        except KeyError:
            if command not in command_to_function.keys():
                print "Pyshell: " + command + " does not exist."
            else:
                print "Error while executing command: " + command
        index += 1


def main():
    python_shell()


if __name__ == "__main__":
    main()
