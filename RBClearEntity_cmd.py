import rhinoscriptsyntax as rs
import Rhino.DocObjects as rdo
import scriptcontext as sc

__commandname__ = "RBClearEntity"

def RunCommand( is_interactive ):
    rObj = rs.GetObject('Select the object to clear', preselect = True)
    
    brep = rdo.ObjRef(rObj).Brep()
    
    rs.DeleteObject(rObj)
    
    sc.doc.Objects.AddBrep(brep)
    
    sc.doc.Views.Redraw()
    
    #DELETE ALSO THE TEXTDOT!
    
    return 0