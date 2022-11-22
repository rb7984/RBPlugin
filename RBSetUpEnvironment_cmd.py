import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg

__commandname__ = "RBSetUpEnvironment"

def Do():
    if not rs.LayerId('RBP'):
        #Create Layers
        rbp =rs.AddLayer("RBP")
        tD=rs.AddLayer("TextDots")
        dr = rs.AddLayer("Drawings")
        cartiglio = rs.AddLayer("Sheet")
        #Parent
        rs.ParentLayer(tD, rbp)
        rs.ParentLayer(dr, rbp)
        rs.ParentLayer(cartiglio, dr)
        #Visibility
        rs.LayerVisible('TextDots', False)

        #Draw a sheet of paper
        pts = [rg.Point3d(210,148.5,0),rg.Point3d(-210,148.5,0),rg.Point3d(-210,-148.5,0),rg.Point3d(210,-148.5,0),rg.Point3d(210,148.5,0)]
        pl = rg.Polyline(pts)
        _ = sc.doc.Objects.AddPolyline(pl)
        rs.ObjectLayer(_, 'Sheet')
        pts = [rg.Point3d(200,138.5,0),rg.Point3d(-200,138.5,0),rg.Point3d(-200,-138.5,0),rg.Point3d(200,-138.5,0), rg.Point3d(200,138.5,0)]
        pl = rg.Polyline(pts)
        _ = sc.doc.Objects.AddPolyline(pl)
        rs.ObjectLayer(_, 'Sheet')
        pts = [rg.Point3d(200, -108.5,0), rg.Point3d(-200,-108.5,0),rg.Point3d(-200,-138.5,0),rg.Point3d(200,-138.5,0),rg.Point3d(200, -108.5,0)]
        pl = rg.Polyline(pts)
        _ = sc.doc.Objects.AddPolyline(pl)
        rs.ObjectLayer(_, 'Sheet')

        rs.LayerVisible('Sheet', False)

    else:
        rs.MessageBox('Set up already done')

def RunCommand( is_interactive ):
    Do()

    return 0
