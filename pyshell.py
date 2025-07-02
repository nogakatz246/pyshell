"""
A linux shell, written in Python2.
"""
import os
import shutil 
import glob


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
        "Usage: man [command]",
        "history": "Prints the history of commands.\n" + 
        "Usage: history",
        "cat": "Prints a file or files.\n" + 
        "Usage: cat [file...]"
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


# TODO: finish this function, add changing the timestamp
def touch(command, arguments):
    """
    Changes the timestamp of a file, or creates a new one if it does not exist.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    """
    if len(arguments) == 0:
        print "Error: touch should receive at lease 1 argument."
        return False
    for filename in arguments:
        try:
            os.mknod(filename)
        except OSError:
            fd = os.open(filename, os.O_WRONLY)
            os.write(fd, "")
            os.close(fd)
    return True


def cat(command, arguments):
    """
    Prints the content of a file / files.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    if len(arguments) == 0:
        print "Error: cat should receive at least 1 argument."
        return False
    for filename in arguments:
        try:
            fd = os.open(filename, os.O_RDONLY)
            size_of_file = os.stat(filename).st_size
            file_data = ""
            for chunk in range(size_of_file):
                file_data += os.read(fd, chunk)
            print file_data
            os.close(fd)
        except OSError:
            print "Error: file could not be printed."
            return False
    return True


def cp(command, arguments):
    """
    Copies a file to a different location.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    if len(arguments) != 2:
        print "Error: cp chould receive 2 arguments, received " + str(len(arguments))
        return False
    try:
        shutil.copyfile(arguments[0], arguments[1])
    except shutil.Error:
        print "Error: file was not copied."
        return False
    except IOError:
        print "Error: file was not copied."
        return False
    return True


def mv(command, arguments):
    """
    Moves a file from one location to another.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    if len(arguments) != 2:
        print "Error: mv should receive 2 arguments, received " + len(arguments)
        return False
    try:
        shutil.move(arguments[0], arguments[1])
    except OSError:
        print "Error: file does not exist."
        return False
    return True


def mkdir(command, arguments):
    """
    Creates a new directory with the name received.
    :param command: the command itself.
    :command type: str.
    :param arguments: the list of arguments.
    :arguments type: list.
    :returns: True if nothing went wrong.
    """
    if len(arguments) == 0:
        print "Error: mkdir should receive at least 1 arguments."
        return False
    for dirname in arguments:
        try:
            os.mkdir(dirname)
        except OSError:
            print "Error: file already exists."
            return False
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
    "touch": touch,
    "cat": cat,
    "cp": cp,
    "mv": mv,
    "mkdir": mkdir
    }
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
        try:
            if command.find("!") == 0:
                command = special_command(command, history_list)
                history_list.pop()
                history_list.append(str(index) + ". " + command)
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
