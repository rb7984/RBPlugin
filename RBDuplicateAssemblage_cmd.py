import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "RBDuplicateAssemblage"

def Do():
    # Unblock Model Layer
    rs.LayerLocked('Model', False)
    
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
            rs.ObjectLayer(id_c, 'Model')
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
        
        # Document Text
        change = str(rs.GetDocumentData('Assemblages', name)).split('|')
        count = str(int(change[2]) + 1)
        new = change[0] + '|' + change[1] + '|' + count
        rs.SetDocumentData('Assemblages', name, new)
        
        # Block Model Layer
        rs.LayerLocked('Model', True) 

def RunCommand( is_interactive ):
    rObj = Do()
    
    return 0