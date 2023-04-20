import rhinoscriptsyntax as rs
import Rhino.DocObjects as rdo
import scriptcontext
import Rhino

__commandname__ = "RBAxonometric"

def RunCommand( is_interactive ):
    rObj = rs.GetObjects('Select the objects to project', preselect = True)
    origin = (list(rdo.ObjRef(rObj[0]).Brep().GetBoundingBox(True).GetCorners()))[0]
    
    pnt = rs.CreatePoint(origin[0]-2, origin[1], origin[2])
    
    rs.ScaleObjects(rObj,origin,[0.5,1,1],False)
    
    rs.ShearObjects(rObj, origin, pnt, -45)
    
    rs.RotateObjects(rObj, origin, 90, [1,0,0], False )
    rs.ShearObjects(rObj, origin, pnt, 45)
    rs.RotateObjects(rObj, origin, -90, [1,0,0], False )
    rs.RotateObjects(rObj, origin, -90, [0,1,0], False )

    rs.MoveObjects(rObj,[-origin.X,-origin.Y,-origin.Z])
    rs.Command('-Make2D Enter ')

    return 0