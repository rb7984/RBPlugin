import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "RBDeleteAssemblage"

def Do():
    rObj = rs.GetObjects('Select Assemblage to delete', group = True, preselect = True)
    
    if rObj:
        name = rs.GetUserText(rObj[0],'Assemblage')
        
        # group
        change = str(rs.GetDocumentData('Assemblages', name)).split('|')
        count = str(int(change[1]) - 1)
        new = change[0] + '|' + count + '|' + change[2]
        rs.SetDocumentData('Assemblages', name, new)
        
        rs.DeleteObjects(rObj)

def RunCommand( is_interactive ):
    Do()
    
    return 0