# GUI-related functionality for turtle demo.
# Author: Lukas Ahrenberg

from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QWidget, QTextEdit, QBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QRectF 
from PyQt5.QtGui import QPainter, QPen 
from main import command

# Accepted colours
colours = {"red": Qt.red, "green" : Qt.green, "blue" : Qt.blue, "black" : Qt.black}


class GraphicsView(QGraphicsView):
    """ Custom QGraphicsView widget.
    Will always 'grows' a scene around the origin.
    """
    # When the a turtle moves outside the current scene the
    # view needs to 'grow'.
    # This slot will calculate the correct view rectangle
    # from a scene rectangle, r.
    def handle_scene_rect(self,r):
        # Create a mirrored copy of the new screen rectangle.
        s = QRectF(-r.x(), -r.y(), -r.width(), -r.height())
        # The union of the rectangle with its mirrored image is
        # the uniform rectangle around the origin.
        u = s.united(r)
        # Create the union with existing screen rectangle to grow area.
        u = u.united(self.sceneRect())
        # Update view.
        self.fitInView(s.united(u), Qt.KeepAspectRatio)

    # Override resizeEvent so that the view is re-scaled.
    def resizeEvent(self,re):
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(re)
        
# ---- Qt5 Objects ----    
# Application object.
app = QApplication([])
# Main window widget
window = QWidget()
# A scene to hold the graphical components
scene = QGraphicsScene()
# And a view widget to show it
view = GraphicsView(scene)
# A text area for providing use feedback
output = QTextEdit()
# A line input to read commands
cmd_input = QLineEdit()

def init():
    """ Set up GUI and layout. """

    # Feedback area is read only.
    output.setReadOnly(True)

    # Ask view to use antialiasing.
    view.setRenderHints(QPainter.Antialiasing)

    # Create layout.
    # Drawing area top, feedback in middle, and input below.
    layout = QBoxLayout(QBoxLayout.Direction.Down)
    layout.addWidget(view, stretch = 1)
    layout.addWidget(output)
    layout.addWidget(cmd_input)
    window.setLayout(layout)

    # Cause the text of the input text field to be parsed and executed.
    # A custom function is needed to read the text and call the parser.
    def handle_input():
        txt = cmd_input.text()
        command(txt)
        cmd_input.clear()
    # Connect returnPressed signal to this function.
    cmd_input.returnPressed.connect(handle_input)
    
    # Set initial scene rectangle
    # This will limit the minimum size of the view.
    # Adding graphics will cause it to grow.
    view.setSceneRect(-100,-100,200,200)
    # Connect this to scene change signal.
    scene.sceneRectChanged.connect(view.handle_scene_rect)

    # Let the input have focus on startup.
    cmd_input.setFocus()

   
def start():
    """ Displays the main widget and starts the GUI loop."""
    window.show()
    app.exec()
    
def line(point_1,point_2,col):
    """ Draw coloured line between two points.
    point_1, point_2 : 2-tuples; x, y coordinates.
    col : QColor.
    """
    (x1,y1) = point_1
    (x2,y2) = point_2
    p = QPen(col)
    p.setWidth(0)
    scene.addLine(x1,y1,x2,y2,pen=p)

def text_out(txt, colour=Qt.black):
    """Write string to feedback area using given colour."""
    output.setTextColor(colour)
    output.append(txt)

def error_out(txt):
    """Write string to feedback area using red."""
    text_out(txt, colour=Qt.red)

