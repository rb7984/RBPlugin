import os
import Rhino.UI as rui
import Eto.Forms as ef
import Eto.Drawing as ed

__commandname__ = "RBInfo"

def Do():    
    dialog = ef.Dialog()
    dialog.Title = "RBPlugin Info"
    dialog.ClientSize = ed.Size(600, 600)
    dialog.Padding = ed.Padding(5)
    dialog.Resizable = True
    
    image_view = ef.ImageView()
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, 'img/00.png')
    image_view.Image = ed.Bitmap(path)
    
    dialog.Content = image_view
    
    dialog.ShowModal(rui.RhinoEtoApp.MainWindow)

def RunCommand( is_interactive ):
    Do()
    
    return 0