import os
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

__commandname__ = "RBDefineEntity"

dict = {'Acciaio': 7.8*(10**(-6)), 'Alluminio': 2.7*(10**(-6)) }

def AdditionalUT(rObj):
    # y_plot = Name|Volume|Weight
    y_plot = '' + str(rs.GetUserText(rObj, 'Name')) + '|' + str(rs.GetUserText(rObj, 'Volume')) + '|' + str(rs.GetUserText(rObj, 'Weight'))  
    
    vol = rs.SurfaceVolume(rObj)[0]
    weight = vol * float(dict[rs.GetUserText(rObj, 'Material')])
    
    rs.SetUserText(rObj, 'Volume', vol)
    rs.SetUserText(rObj, 'Weight', weight)
    
    rs.SetUserText(rObj, 'y_plot', y_plot)
    
    return 0

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
        plList = '|'.join(str(vi).split(',')) + ';' + '|'.join(str(vj).split(',')) + ';' + '|'.join(str(vk).split(',')) + ';'
        #plList = str(vi) + ';' + str(vj) + ';' + str(vk) + ';'
        
        #Store in User Text        
        rs.SetUserText(rObj, 'z_dim', plList[:len(plList)-1])
        
        result = True
    
    return result

def Do():
    rObj = rs.GetObject('Select Object to define', preselect = True)
    
    if rObj:
        # True = Obj already ha been defined
        if CheckUserString(rObj):
            keys = rs.GetUserText(rObj, None)
            guid = []
            for k in keys:
                _ = str(k) + ': '
                _ += str(rs.GetUserText(rObj, k))
                guid.append(_)
                
            rs.ListBox(guid, 'This object has already some fields')
        
        # False: Define Object for the first time
        else:
            i = 0
            k = 0
            while i == 0:
                if k == 0:                    
                    value = rs.StringBox('Name')
                    rs.SetUserText(rObj, 'Name', value)
                    
                    names = rs.GetDocumentData('Database')
                    
                    if names.count(value) == 0:
                        k += 1
                    else:
                        a = rs.MessageBox('This Entity already exist', 0, 'Alert')
                
                elif k == 1:                    
                    value = rs.ListBox(['Acciaio', 'Alluminio'], 'Choose the material', 'Material')
                    #value = rs.StringBox('Material')
                    
                    rs.SetUserText(rObj, 'Material', value)
                    
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
            
            AdditionalUT(rObj)
            
            TexDot(rObj)
            if not poly(rObj):
                rs.SetUserText(rObj, 'z_dim', '0')
            
            # Commit the object in the Archive folder and database
            name = str(len(rs.GetDocumentData('Database')))
            rs.SetDocumentData('Database', name, str(rs.GetUserText(rObj, 'Name')))
            b = rs.MessageBox('Would you like to Archive the entity?', 4, 'Archive')
            if b == 6:
                CommitToArc(rObj)
            
            # Commit object to the Model Layer
            rs.ObjectLayer(rObj, 'Model')
        
        return rObj

def RunCommand( is_interactive ):
    rObj = Do()
    
    return 0