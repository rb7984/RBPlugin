import rhinoscriptsyntax as rs
import Rhino.UI as rui
import Eto.Forms as ef
import Eto.Drawing as ed

__commandname__ = "RBCheckComponents"

def ExtractAssemblages():
    # assemblageInfo = [int, [string]]
    dict = rs.GetDocumentData('Assemblages')
    
    li = []
    for assemblage in dict:
        a = rs.GetDocumentData('Assemblages', assemblage)
        tmp = [assemblage, a]
        li.append(tmp)
    
    return li

def Do():
    dialog = ef.Dialog()
    dialog.Title = "Assemblages"
    dialog.ClientSize = ed.Size(300, 400)
    dialog.Padding = ed.Padding(5)
    dialog.Resizable = True
    
    # assemblageInfo = [int, [string]]
    assemblagesInfo = ExtractAssemblages()
    
    t = ef.GridView()
    t.ShowHeader = True
    t.DataStore = assemblagesInfo
    
    c1 = ef.GridColumn()
    c1.HeaderText = 'Assemblage'
    c1.Editable = False
    c1.DataCell = ef.TextBoxCell(0)
    t.Columns.Add(c1)
    
    c2 = ef.GridColumn()
    c2.HeaderText = 'Pieces'
    c2.Editable = False
    c2.DataCell = ef.TextBoxCell(1)
    t.Columns.Add(c2)
    
    # Maybe add the count coloumn
    
    dialog.Content = t
    
    dialog.ShowModal(rui.RhinoEtoApp.MainWindow)

def RunCommand(is_interactive):
    Do()
    
    return 0