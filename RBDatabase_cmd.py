import os
import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "RBDatabase"

def WriteFileXlsx(xlsx, k):
    xlsx += k
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
    pathfolderArrive = os.path.join(folderStart, "test")
    
    filePath = os.path.join(pathfolderArrive, 'database' + '.txt')
    filePathXlsx = os.path.join(pathfolderArrive, 'database' + '.xlsx')
    
    #Get Object
    rObjs = rs.GetObjects('Oggetti da estrarre')

    txt += 'Name' + '\n'

    i = 0
    for rObj in rObjs:        
        i += 1

        keys = rs.GetUserText(rObj, None)

        for k in keys:                    
            value = rs.GetUserText(rObj, k)
            
            #txt = WriteFileTxt(txt, str(k), str(value))  
            xlsx = WriteFileXlsx(xlsx, str(value))               
    
    #Write to file
    # file = open(filePath, "w")
    # file.write(txt[:len(txt)-1])
    # file.close()
    #Write to .xlsx
    file1 = open(filePathXlsx, "w")
    file1.write(xlsx)
    file1.close()

def RunCommand( is_interactive ):
    
    Database()
    
    return 0