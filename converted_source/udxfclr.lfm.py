from common import *

#Useage:
#        import ChooseDXFColorWindow
#        window = ChooseDXFColorWindow.ChooseDXFColorWindow()
#        window.visible = 1

class ChooseDXFColorWindow(JFrame):
    def __init__(self, title='Choose DXF color'):
        JFrame.__init__(self, title, windowClosing=self.OnClose)
        self.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE) # HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        self.BuildWindow()
        
    def OnClose(self, event):
        print "Closed"
        
    # a menu is top item on the menu bar and can be pulled down for a list of menu items
    def createMenu(self, name, mnemonic=None, menuBar = None):
        menu = JMenu(name)
        if mnemonic:
            menu.setMnemonic(mnemonic)
        if menuBar:
            menuBar.add(menu)
        return menu
        
    def BuildWindow(self):
        toolkit = java.awt.Toolkit.getDefaultToolkit()
        contentPane = self.getContentPane()
        contentPane.setLayout(None)
        # -- contentPane.setLayout(BoxLayout(contentPane, BoxLayout.Y_AXIS))
        buttonFont = Font("Arial Narrow", Font.PLAIN, 9)
        buttonMargin = Insets(1, 1, 1, 1)
        self.setBounds(409, 127, 273, 62  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = [biSystemMenu, biMaximize]
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.colorsDrawGrid = JTable(DefaultTableModel())
        self.colorsDrawGrid.setBounds(2, 4, 206, 57)
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.OnDrawCell = colorsDrawGridDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.OnSelectCell = colorsDrawGridSelectCell
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.RowCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.DefaultColWidth = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.ColCount = 12
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.DefaultRowHeight = 54
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.ScrollBars = ssNone
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.OnDblClick = colorsDrawGridDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsDrawGrid.Options = [goFixedVertLine, goFixedHorzLine, goVertLine, goHorzLine]
        self.Close = JButton('OK', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.getRootPane().setDefaultButton(self.Close)
        self.Close.setBounds(212, 4, 60, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setBounds(212, 27, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        contentPane.add(self.colorsDrawGrid)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def cancelClick(self, event):
        print "cancelClick"
        
if __name__ == "__main__":
    window = ChooseDXFColorWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
