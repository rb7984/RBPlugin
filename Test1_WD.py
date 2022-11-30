import Rhino
import rhinoscriptsyntax as rs

def set_detail_top_zoomed(detail_id, zoom_ids):
    """
    set the detail to top_view and zoom in on zoom_ids
    """
    
    #ensure topview projection through scripted commands
    rs.UnselectAllObjects()
    rs.SelectObject(detail_id)
    rs.Command('-Detail Enable ', echo=False)
    rs.UnselectAllObjects()
    
    #get Rhino Object of detail
    detail_obj = rs.coercerhinoobject(detail_id)
    #getthe viewport of the detail
    viewport = detail_obj.Viewport
    
    #convoluted way to construct Rhino.Geometry Boundingbox from rs.BoundingBox points
    rs_bbox = rs.BoundingBox(zoom_ids)
    bbox = Rhino.Geometry.BoundingBox(rs_bbox[0], rs_bbox[6])
    
    #zoom the detail in on the boundingbox of the zoom_ids objects
    viewport.ZoomBoundingBox(bbox)
    rs.Redraw()
    rs.Command('-Detail EnablePage ', echo=False)
    rs.UnselectAllObjects()
 
def NewLayout():
    layName = rs.AddLayout("Page1", size=([17,11]))
    rs.CurrentView(layName)
    print(layName)
    detail_id = rs.AddDetail(layName,(0,0),(17,11), projection=1)
    print(detail_id)
    
    #get the objects you want to zoom in on
    zoom_ids = rs.ObjectsByLayer('DOCUMENTATION::REGAL BORDER')
    print(zoom_ids)
    set_detail_top_zoomed(detail_id, zoom_ids)
