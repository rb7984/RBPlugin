import os
import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "RBDatabase"

def WriteFileXlsx(xlsx, k):
    xlsx += k
    xlsx += ','
    return xlsx

def WriteFileTxt(txt, k):
    txt += k
    txt += ','
    return txt

def Database():
    txt = ""
    xlsx = ""

    # Get Pathin the document
    folder = rs.GetDocumentData('DocumentData', 'WorkingDirectoryPath')
    
    filePath = os.path.join(folder, 'database' + '.txt')
    filePathXlsx = os.path.join(folder, 'database' + '.xlsx')
    
    # Get Object
    rObjs = rs.GetObjects('Oggetti da estrarre')

    # Set the extraction Keys
    # AAA Cambiare il criterio di selezione del primo
    for k in rs.GetUserText(rObjs[0], None):
        txt += str(k) + ','
        xlsx += str(k) + ','
    
    txt += '\n'
    xlsx += '\n'

    for rObj in rObjs:        
        keys = rs.GetUserText(rObj, None)

        for k in keys:                    
            value = rs.GetUserText(rObj, k)
            
            txt = WriteFileTxt(txt,  str(value))  
            xlsx = WriteFileXlsx(xlsx, str(value))
        txt += '\n'
        xlsx += '\n'
    
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