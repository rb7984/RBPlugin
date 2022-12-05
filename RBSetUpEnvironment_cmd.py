from myLibs import RButil as rbu
import os
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as rg

__commandname__ = "RBSetUpEnvironment"

def Save():
    filename = rs.StringBox('Name of this model', 'Model')
    folder = rs.GetDocumentData('DocumentData', 'WorkingDirectoryPath')
    path = os.path.abspath(folder + filename)
    cmd = "_-SaveAs " + chr(34) + path + chr(34)
    rs.Command(cmd, True)

    return 0

def Layout():
    # Add layout to file
    layout = rs.AddLayout('A3', [420, 297])
    detail_id = rs.AddDetail(layout, (0, 0), (420, 297), projection=1)

    rs.DetailScale(detail_id, 1, 1)
    rs.Redraw()
    rs.Command('-Detail EnablePage ', echo=False)

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

            # Create Archive directory
            pathfolderArchive = os.path.join(folderStart, "Archive")
            os.mkdir(pathfolderArchive)

            # Create a plot directory inside Archive
            pathFolderPlot = os.path.join(pathfolderArchive, 'Plot')
            os.mkdir(pathFolderPlot)

            # Set Document Data, Working-Archive-Plot Directory
            tmp = folderStart + '/'
            rs.SetDocumentData('DocumentData', 'WorkingDirectoryPath', tmp)
            rs.SetDocumentData('DocumentData', 'ArchivePath', pathfolderArchive)
            rs.SetDocumentData('DocumentData', 'PlotPath', pathFolderPlot)
            rs.SetDocumentData('Database', '-1', '000')

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