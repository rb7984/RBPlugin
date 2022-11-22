import os
import rhinoscriptsyntax as rs

__commandname__ = "RBBatchExportStp"

def CheckDr(string):
    a = string.replace("\\","/")
    
    return a

def BatchSaveAs():   
    tmpFolderStart = rs.StringBox("Directory path, please")
    folderStart = CheckDr(tmpFolderStart)
    
    # Create Arrive directory
    parentDir = os.path.split(folderStart)[0]
    pathfolderArrive = os.path.join(parentDir, "stp")
    folderArrive = os.mkdir(pathfolderArrive)
    
    for filename in os.listdir(folderStart):
        
        startingPath = os.path.join(folderStart, filename).lower()
        
        rs.Command("-Import {} _Enter ".format(startingPath))

        rs.Command ("_SelAll ")
        
        newFileName = filename[:len(filename) - 4] + '.stp'        
        filePath = os.path.join(pathfolderArrive, newFileName)
        
        #rs.Command('-Export "{}" Default _Enter'.format(filePath), echo=True)
        rs.Command("-Export " + filePath + " " + "Enter ")
        rs.Command("-SelAll ")
        rs.Command("Delete ")

def RunCommand( is_interactive ):    
    print("Let's export some .stp files"), __commandname__
  
    BatchSaveAs()
  
    return 0