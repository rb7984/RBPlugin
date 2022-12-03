import os
import clr
clr.AddReference("Eto")
clr.AddReference("Rhino.UI")

from Rhino.UI import *
from Eto.Forms import *
from Eto.Drawing import *

__commandname__ = "RBInfo"

def Do():
    dialog = Dialog()
    dialog.Title = "RBPlugin Info"
    dialog.ClientSize = Size(500, 500)
    dialog.Padding = Padding(5)
    dialog.Resizable = False

    image_view = ImageView()
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, 'img/00.png')
    image_view.Image = Bitmap(path)

    dialog.Content = image_view

    dialog.ShowModal(RhinoEtoApp.MainWindow)

def RunCommand( is_interactive ):
    Do()

    return 0