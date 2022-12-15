import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "RBDeleteAssemblage"

def Do():
    # Unblock Model Layer
    rs.LayerLocked('Model', False)
    
    rObj = rs.GetObjects('Select Assemblage to delete', group = True, preselect = True)
    
    if rObj:
        name = rs.GetUserText(rObj[0],'Assemblage')
        
        # group
        change = str(rs.GetDocumentData('Assemblages', name)).split('|')
        count = str(int(change[2]) - 1)
        new = change[0] + '|' + change[1] + '|' + count
        rs.SetDocumentData('Assemblages', name, new)
        
        rs.DeleteObjects(rObj)
        
        # Block Model Layer
        rs.LayerLocked('Model', True) 

def RunCommand( is_interactive ):
    Do()
    
    return 0