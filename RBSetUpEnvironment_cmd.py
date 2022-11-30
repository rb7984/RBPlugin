import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg
import os
from myLibs import RButil as rbu

__commandname__ = "RBSetUpEnvironment"


def Save():
    filename = rs.StringBox('Name of this model', 'Model')
    folder = rs.GetDocumentData('DocumentData', 'WorkingDirectoryPath')
    path = os.path.abspath(folder + filename)
    cmd = "_-SaveAs " + chr(34) + path + chr(34)
    rs.Command(cmd, True)

    return 0


def Layout():
    layout = rs.AddLayout('A3', [420, 297])
    detail_id = rs.AddDetail(layout, (0, 0), (420, 297), projection=1)
    zoom_ids = rs.ObjectsByLayer('Sheet')

    #set_detail_top_zoomed(detail_id, zoom_ids)

    # Ensure topview projection through scripted commands
    rs.UnselectAllObjects()
    rs.SelectObject(detail_id)
    rs.Command('-Detail Enable ', echo=False)
    rs.UnselectAllObjects()

    # Get Rhino Object of detail
    detail_obj = rs.coercerhinoobject(detail_id)
    # Get the viewport of the detail
    viewport = detail_obj.Viewport
    
    # Convoluted way to construct Rhino.Geometry Boundingbox from rs.BoundingBox points
    rs_bbox = rs.BoundingBox(zoom_ids[len(zoom_ids)-1])
    bbox = rg.BoundingBox(rs_bbox[0], rs_bbox[6])

    # Zoom the detail in on the boundingbox of the zoom_ids objects
    viewport.ZoomBoundingBox(bbox)
    rs.Redraw()
    rs.Command('-Detail EnablePage ', echo=False)
    rs.UnselectAllObjects()


def DrawSheet():
    # Draw a sheet of paper
    pts = [rg.Point3d(210, 148.5, 0), rg.Point3d(-210, 148.5, 0), rg.Point3d(-210, -148.5, 0), rg.Point3d(210, -148.5, 0), rg.Point3d(210, 148.5, 0)]
    pl = rg.Polyline(pts)
    _ = sc.doc.Objects.AddPolyline(pl)
    rs.ObjectLayer(_, 'Sheet')
    pts = [rg.Point3d(200, 138.5, 0), rg.Point3d(-200, 138.5, 0), rg.Point3d(-200, -138.5, 0), rg.Point3d(200, -138.5, 0), rg.Point3d(200, 138.5, 0)]
    pl = rg.Polyline(pts)
    _ = sc.doc.Objects.AddPolyline(pl)
    rs.ObjectLayer(_, 'Sheet')
    pts = [rg.Point3d(200, -108.5, 0), rg.Point3d(-200, -108.5, 0), rg.Point3d(-200, -138.5, 0), rg.Point3d(200, -138.5, 0), rg.Point3d(200, -108.5, 0)]
    pl = rg.Polyline(pts)
    _ = sc.doc.Objects.AddPolyline(pl)
    rs.ObjectLayer(_, 'Sheet')
    pts = [rg.Point3d(-135, -108.5, 0), rg.Point3d(-135, -138.5, 0)]
    pl = rg.Polyline(pts)
    _ = sc.doc.Objects.AddPolyline(pl)
    rs.ObjectLayer(_, 'Sheet')

    rs.LayerVisible('Sheet', False)


def Do():
    if not rs.LayerId('RBP'):
        # Create my Environment
        tmpFolderStart = rs.StringBox("Directory path, please")

        if tmpFolderStart:
            folderStart = rbu.CheckDr(tmpFolderStart)

            # Create Arrive directory
            #parentDir = os.path.split(folderStart)[0]
            pathfolderArrive = os.path.join(folderStart, "Archive")
            os.mkdir(pathfolderArrive)

            # Set Document Data, Working Directory and Archive Directory
            tmp = folderStart + '/'
            rs.SetDocumentData('DocumentData', 'WorkingDirectoryPath', tmp)
            rs.SetDocumentData('DocumentData', 'ArchivePath', pathfolderArrive)

            # Create Layers
            rbp = rs.AddLayer("RBP")
            tD = rs.AddLayer("TextDots")
            dr = rs.AddLayer("Drawings")
            cartiglio = rs.AddLayer("Sheet")
            trash = rs.AddLayer("Trash")

            # Parent
            rs.ParentLayer(tD, rbp)
            rs.ParentLayer(dr, rbp)
            rs.ParentLayer(cartiglio, dr)
            rs.ParentLayer(trash, rbp)

            # Visibility
            rs.LayerVisible('TextDots', False)

            # Draw Sheet
            DrawSheet()

            # Create Layout
            Layout()

            # Save the file in Working Directory
            Save()

        else:
            rs.MessageBox('Set Up incomplete, please start over')

    else:
        rs.MessageBox('Set up already done')


def RunCommand(is_interactive):
    Do()

    return 0