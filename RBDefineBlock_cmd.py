import rhinoscriptsyntax as rs
import Rhino
import Rhino.DocObjects as rdo

__commandname__ = "RBDefineBlock"

def DefineBlock():
    rObj = rs.GetObject('Select the object to be made into a dyn Block', preselect = True)
    
    if rObj:
        brep = rdo.ObjRef.Brep(rdo.ObjRef(rObj))
        
        i = int(rs.RealBox('How many parameters are gonna be dynamic?'))
        #For loop to take the input 
        for x in range(i):
            optionsList = ['Length', 'Radius']
            _ = rs.ListBox(optionsList)
            if _ == optionsList[0]:
                #Get the Line corresponding to the dynamic length
                rs.UnselectAllObjects()
                go = Rhino.Input.Custom.GetObject()
                go.SetCommandPrompt('Select the dyn parameter')
                go.GeometryFilter = Rhino.DocObjects.ObjectType.Curve#EdgeFilter
                go.GeometryAttributeFilter=Rhino.Input.Custom.GeometryAttributeFilter.EdgeCurve
                go.SubObjectSelect = True
                go.AcceptNothing(False)
                
                if go.Get()!=Rhino.Input.GetResult.Object: return
                crvObjRef = go.Object(0)
                
                guid = go.Object(0)
                
                objRef = rdo.ObjRef(guid)
                edge = guid.Edge()
                eI = edge.EdgeIndex
                
                rs.SetUserText(rObj, 'dP{0}'.format(x), str(eI))
                length = rs.CurveLength(guid)            
                rs.SetUserText(rObj, 'dP{0}Length'.format(x), length)
            
            elif _ == optionsList[1]:
                #Get the Circle corresponding to the dynamic radius
                return 0

def RunCommand( is_interactive ):
    DefineBlock()
    
    return 0