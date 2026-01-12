"""
A linux shell, written in Python2.
"""
import os
import shutil 
import glob


class Command:
    def __init__(self, func, man):
        self.func = func
        self.man = man

    
def ls(command, arguments):
    """
    Prints the content of a chosen directory.
    If no directory was specified, displays the current directory.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    ret_value = True
    if len(arguments) == 0:
        arguments.append(".")
    for directory in arguments:
        try:
            if len(arguments) > 1:
                print directory + ":"
            list_of_files = os.listdir(directory)
            for file_in_dir in list_of_files:
                print(file_in_dir)
        except OSError:
            print "Directory " + directory + " does not exist!"
            ret_value = False
        return ret_value


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
        return False
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
    if len(arguments) != 2:
        print "Error: man should receive 1 argument, received " + str(len(arguments))
        return False
    command_to_function = arguments[-1] 
    try:
        print command_to_function[arguments[0]].man
    except KeyError:
        print "Man: " + arguments[0] + " does not exist."
        return False
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


def remove_command_index(command_with_index):
    """
    Removes the index from a command in the history list.
    :param command_with_index: the command with the index number.
    :command_with_index type: str.
    :returns: the command without the index.
    """
    return command_with_index[3:]


def special_command(command, history_list):
    """
    Handles the event designators.
    :param command: the command itself.
    :command type: str.
    :param history_list: the history list of the commands.
    :history_list type: list of strings.
    :returns: the correct command according to the history list.
    """
    if command == "!!":
        return remove_command_index(history_list[-2])
    if command.find("!-") == 0:
        num = int(command[2:])
        return remove_command_index(history_list[-1 * num - 1])
    else:
        num = int(command[1:])
        return remove_command_index(history_list[num - 1])


def python_shell():
    """
    A linux shell implementation in Python2.
    :returns: None.
    """
    # a dictionary to hold all the shell commands and the matching python function.
    command_to_function = (
        {
        "ls": Command(ls, ("Prints the content of a chosen directory.\n" +
        "Usage: ls [directory: default is current directory]")),
        "cd": Command(change_dir, ("Changes the current working directory to a chosen directory.\n" +
        "Usage: cd [directory]")),
        "pwd": Command(current_dir, ("Prints the name of the current working directory.\n" +
        "Usage: pwd")),
        "echo": Command(echo, ("Prints the arguments of the command.\n" +
        "Usage: echo [expression...]")),
        "man": Command(man, ("Prints information about a chosen command.\n" +
        "Usage: man [command]")),
        "history": Command(history, ("Prints the history of commands.\n" + 
        "Usage: history"))
        })

    index = 1
    # a list to hold all the past commands
    history_list = []
    
    print "Welcome to the python shell!:)"
    while True:
        command_line = raw_input(os.getcwd() + "  > ")
        history_list.append(str(index) + ". " + command_line)
        splitted_command_line = command_line.split(" ")
        try:
            command = splitted_command_line[0]
            arguments = splitted_command_line[1:]
        except IndexError:
            print "Error: bad command."
            continue
        if command.find("!") == 0:
            command = special_command(command, history_list)
            history_list.pop()
            history_list.append(str(index) + ". " + command)
        if command == "history":
            arguments.append(history_list)
        if command == "man":
            arguments.append(command_to_function)
        if command not in command_to_function.keys():
            print "Pyshell " + command + " does not exist."
        result = command_to_function[command].func(command, arguments)
        if not result:
            print "Error while executing command: " + command
        index += 1


def main():
    python_shell()


if __name__ == "__main__":
    main()
