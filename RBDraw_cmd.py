import math
from myLibs import RButil as rbu
import rhinoscriptsyntax as rs
import Rhino.DocObjects as rdo
import Rhino.Geometry as rg
import scriptcontext as sc
import Rhino.FileIO
import Rhino.Display

__commandname__ = "RBDraw"

def WritePdf(name):
    folder = rs.GetDocumentData('DocumentData', 'PlotPath')
    
    filename = folder + '\\' + name + '.pdf'
    
    pdf = Rhino.FileIO.FilePdf.Create()
    
    capture = Rhino.Display.ViewCaptureSettings(sc.doc.Views.Find("A3", False), 300)
    
    pdf.AddPage(capture)
    pdf.Write(filename)

def WriteDwg(name):
    folder = rs.GetDocumentData('DocumentData', 'PlotPath')
    
    filename = folder + '\\' + name + '.dwg'
    
    rObjs = sc.doc.Objects.FindByLayer('Drawings')
    
    rs.SelectObjects(rObjs)
    
    rs.Command('-Export ' + filename + ' ' + '-Enter ')

def SetUpCamera(ocs, bB, i):
    #Selecting a view
    a = rs.ViewNames(True, 0)
    
    #Setting the views
    cTar = bB.Center
    if i<3:
        cLoc = cTar + rbu.rotate(ocs, 1)[i]
    else:
        cLoc = cTar + ocs[0] + ocs[1] + ocs[2]
    
    rs.ViewCameraTarget(a[0], cLoc, cTar)
    rs.ViewDisplayMode(a[0], 'Shaded')
    rs.ViewProjection(a[0], 1)
    
    sc.doc.Views.Redraw()
    
    rs.Command('-SelAll ')
    
    rs.Command('-Make2D Enter ')
    twoD = rs.SelectedObjects(False, False)
    
    #Get the object area
    c = rdo.ObjRef(twoD[0]).Geometry().GetBoundingBox(True).Center
    
    m = 40
    n = 20
    rs.MoveObjects(twoD,[-c.X,-c.Y, -c.Z])
    rs.MoveObject(twoD, [m*math.cos((math.pi/2)*(i+1))+m*math.sin((math.pi/2)*(i+1)),n*math.cos((math.pi/2)*i)+n*math.sin((math.pi/2)*i), 0])
    
    rs.ObjectLayer(twoD, 'Drawings')

def RetrieveOCS(rObj):
    # Retrieve rObj orientation info
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
    # Retrieve info from UserText
    pos = [rg.Point3d(-180,-128.5,0), rg.Point3d(-100,-128.5,0), rg.Point3d(-70,-128.5,0), rg.Point3d(-50,-128.5,0), rg.Point3d(-20,-128.5,0)]
    
    i = 0
    for k in li:
        _ = rs.AddText(str(li[k]), pos[i], 5)
        rs.ObjectLayer(_, 'Drawings')
        i += 1
    
    return 0

def Do():
    rObj = rs.GetObject('Select object to draw')
    ocs = RetrieveOCS(rObj)
    
    if rObj:
        rs.LayerVisible('Drawings', False)
        
        # Get BoundingBox
        bB= rdo.ObjRef(rObj).Brep().GetBoundingBox(True)
        
        # li is the dictionary of the UserText of the rObj
        li = rbu.Fetch(rObj)
        
        # Set Camera Method
        for i in range(4): #range to be controlled
            #range(3) = 3 ortho views
            #range(4) = 4 the 4th should be isometric view
            SetUpCamera(ocs, bB, i)
        
        # Plot the info of the Obj
        PlotInfo(li)
        
        # Delete the layer Make2d
        rs.DeleteLayer('Make2D')
        
        rs.LayerVisible('Drawings', True)
        rs.LayerVisible('Sheet', True)
        
        # Write the pdf file
        # WriteFile(fileName, savings)
        # 1 = .pdf; 2 = .pdf + .dwg
        WritePdf(li['Name'])
        WriteDwg(li['Name'])
        
        rs.LayerVisible('Drawings', False)
        rs.LayerVisible('Sheet', False)

def RunCommand( is_interactive ):
    Do()
    
    return 0