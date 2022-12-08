import rhinoscriptsyntax as rs
import Rhino.DocObjects as rdo
import scriptcontext as sc

__commandname__ = "RBCheck"

def RunCommand( is_interactive ):
    rs.Command("SelAll ")
    a = rs.SelectedObjects()
    
    for rObj in a:
        
        return 0
    
    return 0