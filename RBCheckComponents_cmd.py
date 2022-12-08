import os
import Rhino.UI as rui
import Eto.Forms as ef
import Eto.Drawing as ed

__commandname__ = "RBCheckComponents"

def ExtractAssemblages():
    # assemblageInfo = [int, [string]]
    li = []
    li.append(3)
    
    return li

def Do():
    dialog = ef.Dialog()
    dialog.Title = "Assemblages"
    dialog.ClientSize = ed.Size(600, 800)
    dialog.Padding = ed.Padding(5)
    dialog.Resizable = True
    
    # assemblageInfo = [int, [string]]
    assemblagesInfo = ExtractAssemblages()
    
    t = ef.TableLayout()
    
    table = ef.DynamicTable(3,)
    
    dialog.Content = table
    
    dialog.ShowModal(rui.RhinoEtoApp.MainWindow)

def RunCommand(is_interactive):
    Do()
    
    return 0