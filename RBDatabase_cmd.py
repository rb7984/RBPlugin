import os
import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "RBDatabase"

def WriteFileXlsx(xlsx, k, v):
    xlsx += k
    xlsx += ','
    xlsx += v
    xlsx += '\n'
    return xlsx

def WriteFileTxt(txt, k, v):
    txt += k
    txt += ': '
    txt += v
    txt += '\n'
    return txt

def Database():
    txt = ""
    xlsx = ""

    tmpFolderStart = rs.StringBox("Directory path, please")
    folderStart = tmpFolderStart.replace("\\","/")

    # Create Arrive directory
    #parentDir = os.path.split(folderStart)[0]
    pathfolderArrive = os.path.join(folderStart, "test")
    #folderArrive = os.mkdir(pathfolderArrive)
    
    filePath = os.path.join(pathfolderArrive, 'database' + '.txt')
    filePathXlsx = os.path.join(pathfolderArrive, 'database' + '.xlsx')
    
    #Get Object
    i = 0
    for rObj in Rhino.RhinoDoc.ActiveDoc.Objects:        
        txt += str(i) + '\n'
        i += 1
        if rObj.IsNormal:
            keys = rs.GetUserText(rObj, None)
            for k in keys:                    
                value = rs.GetUserText(rObj, k)
                
                txt = WriteFileTxt(txt, str(k), str(value))  
                xlsx = WriteFileXlsx(xlsx, str(k), str(value))               
    
    #Write to file
    file = open(filePath, "w")
    file.write(txt[:len(txt)-1])
    file.close()
    #Write to .xlsx
    file1 = open(filePathXlsx, "w")
    file1.write(xlsx)
    file1.close()

def RunCommand( is_interactive ):
    
    Database()
    
    return 0