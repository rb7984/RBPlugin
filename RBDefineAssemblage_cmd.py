import rhinoscriptsyntax as rs
import scriptcontext as sc

__commandname__ = "RBDefineAssemblage"

def Do():
    rObj = rs.GetObjects('Select Object to define', preselect = True)
    name = rs.StringBox('What\'s the name of the Assemblage?')
    subNames = ''
    
    if rObj:
        for i in rObj:
            rs.SetUserText(i, 'Assemblage', name)
            subNames += str(rs.GetUserText(i, 'Name')) + ','
        
        sc.doc.Groups.Add(rObj)
        sc.doc.Views.Redraw()
        
        a = subNames[:len(subNames)-1]
        subNames = a + '|1'
        
        rs.SetDocumentData('Assemblages', name, subNames)

def RunCommand( is_interactive ):
    Do()
    
    return 0