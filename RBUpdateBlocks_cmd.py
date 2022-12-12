import rhinoscriptsyntax as rs
import Rhino
import Rhino.DocObjects as rdo

__commandname__ = "RBUpdateBlocks"

def GetDynBlocks():
    dynBlockList = []
    
    for rObj in Rhino.RhinoDoc.ActiveDoc.Objects:
        # create a nested list to pass to the Adjourn() function
        # [[rObj, dynKey, ..., dynKey], ...]
        #    ^      ^             ^
        # RhinoObj  dynamic Keys        
        objAttributes = []
        keys = rs.GetUserText(rObj, None)
        
        for k in keys:
            if str(k)== 'Dyn':
                if rs.GetUserText(rObj, k) == 1:
                    dynBlockList.append(rObj)
            #insert break mechanism
            #otherwise in dynBlockList there will be duplicates
    
    return dynBlockList

def Adjourn():
    #Get all dynamic blocks
    options = GetDynBlocks()
    
    if len(options)>0:
        result = rs.ListBox(options, "Pick an option")
        if result: rs.MessageBox( result + " was selected" )
    
    #Get Object
    i = 0
    for rObj in Rhino.RhinoDoc.ActiveDoc.Objects:        
        a = 0

def AdjournManual():
    #Get Object
    rObj = rs.GetObject("Block to Adjourn")
    objRef = rdo.ObjRef(rObj)
    brep = rdo.ObjRef.Brep(objRef)
    
    #Get Attributes in Aplhabetic order  
    keys = rs.GetUserText(rObj, None)
    keys.sort()
    
    guid = 0
    for k in keys:
        kk = str(k)
        if kk[:2] == 'dP':
            if len(kk) == 3:
                guid = int(rs.GetUserText(rObj, k))
            else:
                crv = brep.Edges[guid]
                length = rs.CurveLength(crv)
                rs.SetUserText(rObj, k, length)

def RunCommand( is_interactive ):
    options= ['Selected', 'All']
    _ = rs.ListBox(options)
    
    if _ == options[0]:
        AdjournManual()
    elif _ == options[1]:
        Adjourn()
    
    return 0