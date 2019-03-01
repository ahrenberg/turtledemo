# Parsing related functionalityfor turtle demo.
# Author: Lukas Ahrenberg

import sys
import turtle
import drawing
from errors import ParseError

def distance(s):
    """ Interprets string `s` as floating point distance. 
    Distance must be positive.
    Raises `ParseError` on error.
    """
    try:
        d = float(s)
        if d <= 0:
            raise ParseError("Distance must be positive")
        return d
    except ValueError:
        raise ParseError(f"'{s}' not a distance")

def degrees(s):
    """ Interprets string `s` as floating point angle.
    Raises `ParseError` on error.
    """
    try:
        return float(s)
    except ValueError:
        raise ParseError(f"'{s}' not a valid angle")

def name(s):
    """ Interprets string `s` as name."""
    # Dummy used as id in parsing.
    return s

def pen_state(s):
    """ Maps from string `s` to Boolean pen state.
    'up' : False, 'down' : True
    Raises `ParseError` on error.
    """
    if "up" == s:
        return False
    elif "down" == s:
        return True
    else:
        raise ParseError(f"'{s}' not a valid pen state")

def colour(s):
    """ Maps from string `s` to Boolean pen state.
    Valid colours are keys in dictionary `drawing.colours`.
    Raises `ParseError` on error.
    """
    try:
        return drawing.colours[s]
    except KeyError:
        cs = ", ".join(drawing.colours)
        raise ParseError(f"'{s}' is not a valid colour. [Known colours: {cs}]")

# This dictionary maps from functions representing a particular command to
# a list of functions to convert a list of strings to function arguments.
# For instance turtle.move takes two arguments, a string (turtle name) and a
# float (distance to move). Thus the two functions `name` and `distance` is
# included in its list.
# To add a command, add its implementation to the turtle module, then and
# an entry in the command_parsers dictionary.
command_parsers = {turtle.turtle : [name],
                   turtle.move  : [name, distance],
                   turtle.left : [name, degrees],
                   turtle.right : [name, degrees],
                   turtle.pen : [name, pen_state],
                   turtle.colour : [name, colour],
                   turtle.quit : []}

def parse_arguments(parsers,arg_strings):
    """ Applies argument parsers to strings by pairing them one by one.
    Returns a list of the result.
    parsers - list of functions (e.g. `[name, distance]`) 
    arg_strings - list of strings.
    Raises ParseError if lists of different length.
    """
    if len(arg_strings) < len(parsers):
        raise ParseError("Too few arguments.")
    if len(arg_strings) > len(parsers):
        raise ParseError("Too many arguments.")
    return [p(s) for (p,s) in zip(parsers, arg_strings)]
            
def parse(line):
    """ Parse a command string.
    Returns a pair, where the first component is the command function 
    and the second component the arguments.
    Raises ParseError on error.
    """
    try:
        # Split line at space, first word in c, all others in list cc.
        c, *cc = line.split()
        # The functions are named the same as the commands, so getattr can
        # be used to retrieve the function from the turtle module.
        # This raises AttributeError if not found.
        op = getattr(turtle,c)
        parsers = command_parsers[op]
        cargs = parse_arguments(parsers,cc)
        return (op,cargs)
    except (KeyError, AttributeError):
        raise ParseError(f"Unknown command '{c}'")
    except ParseError as pe:
        raise ParseError(f"{pe}")
        
