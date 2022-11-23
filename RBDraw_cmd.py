#import os
#import Rhino as rc
#import Rhino.Display as rd
from myLibs import RBfetch as RBf
import rhinoscriptsyntax as rs
import Rhino.DocObjects as rdo
import Rhino.Geometry as rg
import scriptcontext as sc
import math
 
__commandname__ = "RBDraw"

def rotate(l, n):
    
    return l[n:] + l[:n]

def SetUpCamera(ocs, bB, i):
    #Selecting a view
    a = rs.ViewNames(True, 0)
    #Setting the views
    cTar = bB.Center
    if i<3:
        cLoc = cTar + rotate(ocs, 1)[i]
    else:
        cLoc = cTar + ocs[0] + ocs[1] + ocs[2]
    
    rs.ViewCameraTarget(a[0], cLoc, cTar)
    rs.ViewDisplayMode(a[0], 'Shaded')
    rs.ViewProjection(a[0], 1)

    sc.doc.Views.Redraw()

    rs.Command('-SelAll ')

    rs.Command('-Make2D Enter ')
    twoD = rs.SelectedObjects(False, False)
    rs.ObjectLayer(twoD, 'Drawings')

    #Get the object area
    c = rdo.ObjRef(twoD[0]).Geometry().GetBoundingBox(True).Center

    m = 40
    n = 20
    rs.MoveObjects(twoD,[-c.X,-c.Y, -c.Z])
    rs.MoveObject(twoD, [m*math.cos((math.pi/2)*(i+1))+m*math.sin((math.pi/2)*(i+1)),n*math.cos((math.pi/2)*i)+n*math.sin((math.pi/2)*i), 0])

    return 0

def RetrieveOCS(rObj):
    #retrieve rObj orientation info
    pl = rs.GetUserText(rObj, 'z_dim')
    _ = str(pl).split(';')

    p, v = [], []
    
    for i in _:
        p.append(i.split(','))

    vi = rg.Vector3d(float(p[0][0]), float(p[0][1]), float(p[0][2]))
    vj = rg.Vector3d(float(p[1][0]), float(p[1][1]), float(p[1][2]))
    vk = rg.Vector3d(float(p[2][0]), float(p[2][1]), float(p[2][2]))

    v.append(vi)
    v.append(vj)
    v.append(vk)

    return v

def PlotInfo(li):

    for k in li:
        _ = rs.AddText(str(li[k]), rg.Point3d(0,0,0), 20)
        rs.ObjectLayer(_, 'Drawings')

    return 0

def Draw():
    #Get the object
    rObj = rs.GetObject('Select object to draw')
    ocs = RetrieveOCS(rObj)

    if rObj:
        #isolate object        
        rs.HideObjects(rs.InvertSelectedObjects((rs.SelectObject(rObj))))
        
        #Get BoundingBox
        bB= rdo.ObjRef(rObj).Brep().GetBoundingBox(True)

        rs.LayerVisible('Drawings', False)

        li = RBf.Fetch(rObj)
        
        #Set Camera Method
        for i in range(4): #range to be controlled
            #range(3) = 3 ortho views
            #range(4) = 4 the 4th should be isometric view
            SetUpCamera(ocs, bB, i)
        
        #Plot the info of the Obj
        PlotInfo(li)

        #Delete the layer Make2d
        rs.DeleteLayer('Make2D')

def RunCommand( is_interactive ):
    Draw()
    
    return 0