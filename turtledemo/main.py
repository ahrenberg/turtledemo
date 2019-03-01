# Turtle demo
# Author: Lukas Ahrenberg

import sys
import parser
from errors import *
import drawing
import signal

def command(line, line_num = None):
    """
    Parse and execute command.
    line - Command string.
    line_num - optional line number.
    Writes error message on fail, echoes command on success.
    """
    try:
        # Remove leading and trailing white space & newline
        line = line.strip()
        # Get command and arguments from parser.
        cmd, args = parser.parse(line)
        # Apply command to arguments.
        cmd(*args)
        # Echo command to user.
        drawing.text_out(line)
    except (ParseError,TurtleError) as e:
        # Create error message.
        msg = ""
        if None != line_num:
            msg += f"Line {line_num}"
        else:
            msg += f"'{line}'"
        msg+=f" : {e}"
        drawing.error_out(msg)
    except ValueError:
        # Parsing empty line. Do nothing.
        pass

def read_files(file_names):
    """ Try to open every file in file_names, parse inputs line by line.
    Note: This in effect concatenates the files.
    Echoes file name when opening.
    Writes an error message if the file could not be opened.
    """
    # Go over each file, parse line by line.
    for fn in file_names:
        try:
            with open(fn, 'r') as fd:
                drawing.text_out(f"Reading file: '{fn}'")
                for ln,line in enumerate(fd,start=1):
                    command(line,ln)
        except FileNotFoundError:
            drawing.error_out(f"No such file '{fn}'")


if __name__ == "__main__":
    # Qt takes over when GUI is started; this line makes sure Ctrl-C can be
    # used to interrupt in shells which supports it.
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # Set up GUI
    drawing.init()
    # Assume any parameters are command files.
    read_files(sys.argv[1:])
    # Start GUI main loop
    drawing.start()
