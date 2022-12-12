import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "RBDuplicateAssemblage"

def Do():
    rObj = rs.GetObjects('Select Assemblage to duplicate', group = True, preselect = True)
    
    id_c_L = []
    
    if rObj:
        name = rs.GetUserText(rObj[0],'Assemblage')
        
        for i in rObj:
            # copy
            obj_c = rs.coercegeometry(i)
            
            # bake
            id_c = Rhino.RhinoDoc.ActiveDoc.Objects.Add(obj_c)
            rs.SetUserText(id_c, 'Assemblage', name)
            id_c_L.append(id_c)
        
        # group
        
        groupName = str(rs.GroupCount())
        
        # allGroupName_L = rs.GroupNames()
        # if groupName not in allGroupName_L:
        #     rs.AddGroup(groupName)
        
        rs.AddGroup(groupName)
        
        rs.AddObjectsToGroup(id_c_L, groupName)
        
        k = rs.ObjectsByGroup(groupName)
        rs.MoveObjects(k, (25, 25, 0))
        
        change = str(rs.GetDocumentData('Assemblages', name)).split('|')
        count = str(int(change[1]) + 1)
        new = change[0] + '|' + count
        rs.SetDocumentData('Assemblages', name, new)

def RunCommand( is_interactive ):
    rObj = Do()
    
    return 0