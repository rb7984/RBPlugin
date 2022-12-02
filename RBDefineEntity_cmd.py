import rhinoscriptsyntax as rs
import os
import Rhino.Geometry as rg

__commandname__ = "RBDefineEntity"


def CommitToArc(rObj):
    pathfolderArrive = rs.GetDocumentData('DocumentData', 'ArchivePath')

    fileName = rs.GetUserText(rObj, 'Name') + '.3dm'

    rs.SelectObject(rObj)
    
    filePath = os.path.join(pathfolderArrive, fileName)

    rs.Command("-Export " + filePath + " " + "Enter ")

    return 0

def CheckUserString(rObj):
    bool = False
    a = rs.GetUserText(rObj, None)

    if len(a) == 0:
        bool = False
    else:
        bool = True
    
    return bool

def TexDot(rObj):
    massprop= rs.SurfaceVolumeCentroid(rObj)

    a = str(rs.GetUserText(rObj, 'Name', None))
    tD = rs.AddTextDot(a, massprop[0])

    rs.ObjectLayer(tD, 'TextDots')
    
    return 0

def poly(rObj):
    #Check
    result = False
    #Get the UCS through a polyline
    txt = 'OCS\'s {} point of for future representation'
    pl = rs.GetPolyline(3, txt.format('first'),txt.format('second'),txt.format('last'),'nil',2, 3)
    
    if pl:        
        vi = rg.Vector3d(pl[0].X-pl[1].X, pl[0].Y-pl[1].Y,pl[0].Z-pl[1].Z)
        vi.Unitize()
        vj = rg.Vector3d(pl[2].X-pl[1].X, pl[2].Y-pl[1].Y,pl[2].Z-pl[1].Z)
        vj.Unitize()
        vk = rs.VectorCrossProduct(vi, vj)
        plList = str(vi) + ';' + str(vj) + ';' + str(vk) + ';'

        #Store in User Text        
        rs.SetUserText(rObj, 'z_dim', plList[:len(plList)-1])
        #Store the polyline
        #_ = sc.doc.Objects.AddPolyline(pl)

        result = True
    
    return result

def Do():
    rObj = rs.GetObject('Select Object to define', preselect = True)

    if rObj:
        #True = Obj already ha been defined
        if CheckUserString(rObj):
            keys = rs.GetUserText(rObj, None)
            guid = []
            for k in keys:
                _ = str(k) + ': '
                _ += str(rs.GetUserText(rObj, k))
                guid.append(_)

            rs.ListBox(guid, 'This object has already some fields')
        #False: Define Object for the first time
        else:
            i = 0
            k = 0
            while i == 0:
                if k == 0:                    
                    value = rs.StringBox('Name')
                    rs.SetUserText(rObj, 'Name', value)
    
                    a = rs.MessageBox('Would you like to add a field?', 4, 'Define Entity')
                    i += a - 6
                    k += 1
                else:
                    # Yes = 6
                    # No = 7            
                    key = rs.StringBox('Key')
                    value =rs.StringBox('Value')
                    rs.SetUserText(rObj, key, value)

                    a = rs.MessageBox('Would you like to add a field?', 4, 'Define Entity')
                    i += a - 6
                    k += 1

            TexDot(rObj)
            if not poly(rObj):
                rs.SetUserText(rObj, 'z_dim', '0')
            
            #Commit the object in the Archive folder
            b = rs.MessageBox('Would you like to Archive the entity?', 4, 'Archive')
            if b == 6:
                CommitToArc(rObj)
        
        return rObj

def RunCommand( is_interactive ):
    rObj = Do()
    
    return 0