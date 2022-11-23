#import Rhino
import rhinoscriptsyntax as rs

def Fetch(rObj):
    li = {}

    keys = rs.GetUserText(rObj, None)
    for key in keys:
        li[key] = rs.GetUserText(rObj, key)

    return li