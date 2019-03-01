# turtledemo

Author: Lukas Ahrenberg

Simple turtle-graphics demo written in Python and Qt. Turtle commands are read from file or input interactively. Drawing area always centred at the origin and automatically scaled to show whole scene. Initial drawing area size is 200 by 200 units. Turtles start at origin with pen down, and colour blue.

## Requirements
- Python3 (Tested with Python 3.7.2)
- PyQt5 (Tested with PyQt 5.11.3)

## Running
From the project folder the program is started with:

   `python turtledemo/main.py`

From the GUI it is possible to submit turtle command lines using the input field. Commands are executed on enter and echoed in the text area above. Error messages are shown in red.

Any command line arguments provided to the program is interpreted as names of text files containing turtle commands, which will be executed first.

   `python turtledemo/main.py examples/square.txt`

   `python turtledemo/main.py examples/square.txt examples/triangle.txt`

Note that the effect is a concatenation of the files, and that processing will not stop on errors. E.g. two files with identically named turtles may lead to unexpected results.

## Turtle commands

* turtle name - Create a new turtle identified by the given name
* move name d - Moves the named turtle forward by d units (d must be positive)
* left name a - Rotate the turtle anticlockwise by a degrees
* right name a - Rotate the turtle clockwise by a degrees
* pen name up - Lift the pen from the drawing area, moving turtle will not leave a trail
* pen name down - Put the pen down on drawing area, moving turtle will leave a trail
* colour name c - Set the drawing colour of the turtle trail to c (accepted colours: red, green, blue, black)
* quit - Exit the program (has no effect in a command file)

Commands `left` and `right` accepts negative rotation, so that `left name -a` has the same effect as `right name a`.
