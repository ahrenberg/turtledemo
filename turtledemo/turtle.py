# Turtle representation and commands
# Author: Lukas Ahrenberg

import math
from functools import wraps
from errors import TurtleError
import drawing

class Turtle:
    """
    Turtle having a position, direction, pen status, and pen colour. 
    """    
    def __init__(self):
        """ Initializes the turtle.
        Initial position : (0,0)
        Initial rotation : -90 degrees - 'North' on screen coordinate system.
        Initial colour : blue
        Initial pen state : Down (True)
        """
        # Angle to x-axis in radians (left hand system); face north.
        self.theta = math.radians(-90.0)
        # Position coordinate (x,y), start at 0,0.
        self.position = (0.0,0.0)
        # Colour as string, use blue as default.
        self.colour = drawing.colours["blue"]
        # Pen state, True - down, False - up.
        self.pen = True


# Dictionary containing all Turtle objects created.
turtles = {}

# Utility wrapper for commands which will need to look up a turtle.
# Handles error if the turtle in question is undefined.
# Applied with decorator below.
def checkturtle(f):
    """ Maps `KeyError` raised by function `f` to a `TurtleError`.
    Used as decorator for functions needing to do `turtles[name]`.
    `KeyError` assumed to be due to non-existing turtle.
    """
    @wraps(f)
    def ct(*args,**kwargs):
        try:
            # Apply function.
            return f(*args, **kwargs)
        except KeyError as k:
            # Generate error.
            # The offending key can be had as the first argument of the exception.
            name = k.args[0]
            raise TurtleError(f"Turtle '{name}' does not exist")
    return ct

# --- Command functions ---
# These functions corresponds to turtle commands.

def turtle(name):
    """ Creates a turtle with name `name`.
    Raises `TurtleError` if name already in use.
    """
    if name in turtles.keys():
        raise TurtleError(f"Turtle '{name}' already exists")
    turtles[name] = Turtle()
   
@checkturtle
def left(name, a):
    """ Turn left by subtracting angle `a`."""
    turtles[name].theta -= math.radians(a)

@checkturtle
def right(name, a):
    """ Turn right by adding angle `a`"""
    turtles[name].theta += math.radians(a)

@checkturtle
def move(name, d):
    """ Moves the turtle distance `d`.
    Causes a line to be drawn if pen is down.
    """
    t = turtles[name]
    (x,y) = t.position
    t.position = (x + d * math.cos(t.theta), y + d * math.sin(t.theta))
    # Should the pen be town, move will generate a line.
    if True == t.pen:
        drawing.line((x,y),t.position, t.colour)
    
@checkturtle
def colour(name, c):
    """ Sets turtle colour to `c`."""
    turtles[name].colour = c

@checkturtle
def pen(name,state):
    """ Sets turtle pen state to `state`
    True - pen down; False - pen up.
    """
    turtles[name].pen = state

def quit():
    """ Quits the application by asking the GUI to shut down."""
    drawing.app.quit()
