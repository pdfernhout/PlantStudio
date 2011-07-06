from common import *

#Useage:
#        import TimeSeriesWindow
#        window = TimeSeriesWindow.TimeSeriesWindow()
#        window.visible = 1

class TimeSeriesWindow(JFrame):
    def __init__(self, title='Time series'):
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
        self.setBounds(366, 184, 520, 119  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.Menu = MainMenu1
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.OnDestroy = FormDestroy
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        
        self.grid = JTable(DefaultTableModel())
        self.grid.setBounds(8, 4, 185, 67)
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.OnEndDrag = gridEndDrag
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.OnDrawCell = gridDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.RowCount = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.OnDragOver = gridDragOver
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.ColCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.DefaultRowHeight = 64
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.FixedCols = 0
        self.grid.mousePressed = self.gridMouseDown
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.Options = [goFixedVertLine, goFixedHorzLine]
        self.Label1 = JLabel('The time series window is empty. To fill it, select a plant in the main window and choose Make Time Series from the Plant menu.', font=buttonFont)
        self.Label1.setBounds(8, 8, 221, 42)
        self.emptyWarningPanel = JPanel(layout=None)
        # -- self.emptyWarningPanel.setLayout(BoxLayout(self.emptyWarningPanel, BoxLayout.Y_AXIS))
        self.emptyWarningPanel.add(self.Label1)
        self.emptyWarningPanel.setBounds(206, 10, 241, 57)
        
        self.MainMenu1 = JMenuBar()
        self.setJMenuBar(self.MainMenu1)

        self.TimeSeriesMenuEdit = self.createMenu("Edit", "E", self.MainMenu1)
        self.TimeSeriesMenuUndoAction = createAction(self.TimeSeriesMenuUndoClick, "Undo", None, self.TimeSeriesMenuEdit, KeyEvent.VK_U, None, None, "standard")
        self.TimeSeriesMenuRedoAction = createAction(self.TimeSeriesMenuRedoClick, "Redo", None, self.TimeSeriesMenuEdit, KeyEvent.VK_R, None, None, "standard")
        self.TimeSeriesMenuUndoRedoListAction = createAction(self.TimeSeriesMenuUndoRedoListClick, "Undo/Redo List...", None, self.TimeSeriesMenuEdit, KeyEvent.VK_L, None, None, "standard")
        self.TimeSeriesMenuEdit.addSeparator()
        self.TimeSeriesMenuCopyAction = createAction(self.TimeSeriesMenuCopyClick, "Copy", None, self.TimeSeriesMenuEdit, KeyEvent.VK_C, None, None, "standard")
        self.TimeSeriesMenuPasteAction = createAction(self.TimeSeriesMenuPasteClick, "Paste", None, self.TimeSeriesMenuEdit, KeyEvent.VK_P, None, None, "standard")
        self.TimeSeriesMenuSendCopyAction = createAction(self.TimeSeriesMenuSendCopyClick, "Send Copy to Main Window", None, self.TimeSeriesMenuEdit, KeyEvent.VK_S, None, None, "standard")
        self.TimeSeriesMenuEdit.addSeparator()
        self.TimeSeriesMenuBreedAction = createAction(self.TimeSeriesMenuBreedClick, "Breed", None, self.TimeSeriesMenuEdit, KeyEvent.VK_B, None, None, "standard")
        self.TimeSeriesMenuEdit.addSeparator()
        self.TimeSeriesMenuDeleteAction = createAction(self.TimeSeriesMenuDeleteClick, "Delete Time Series", None, self.TimeSeriesMenuEdit, KeyEvent.VK_D, None, None, "standard")
        
        self.TimeSeriesMenuOptions = self.createMenu("Options", "O", self.MainMenu1)
        self.TimeSeriesMenuOptionsDrawAs = JMenu("Draw Using")
        self.TimeSeriesMenuOptionsDrawAs.setMnemonic(KeyEvent.VK_D)
        self.TimeSeriesMenuOptions.add(self.TimeSeriesMenuOptionsDrawAs)
        group = ButtonGroup()
        self.TimeSeriesMenuOptionsFastDrawAction = createAction(self.TimeSeriesMenuOptionsFastDrawClick, "Bounding Boxes", None, self.TimeSeriesMenuOptionsDrawAs, KeyEvent.VK_B, None, None, "radiobutton")
        group.add(self.TimeSeriesMenuOptionsFastDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.TimeSeriesMenuOptionsFastDraw.GroupIndex = 10
        self.TimeSeriesMenuOptionsMediumDrawAction = createAction(self.TimeSeriesMenuOptionsMediumDrawClick, "Wire Frames", None, self.TimeSeriesMenuOptionsDrawAs, KeyEvent.VK_W, None, None, "radiobutton")
        group.add(self.TimeSeriesMenuOptionsMediumDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.TimeSeriesMenuOptionsMediumDraw.GroupIndex = 10
        self.TimeSeriesMenuOptionsBestDrawAction = createAction(self.TimeSeriesMenuOptionsBestDrawClick, "Solids", None, self.TimeSeriesMenuOptionsDrawAs, KeyEvent.VK_S, None, None, "radiobutton")
        group.add(self.TimeSeriesMenuOptionsBestDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.TimeSeriesMenuOptionsBestDraw.GroupIndex = 10
        self.TimeSeriesMenuOptionsCustomDrawAction = createAction(self.TimeSeriesMenuOptionsCustomDrawClick, "Custom...", None, self.TimeSeriesMenuOptionsDrawAs, KeyEvent.VK_C, None, None, "radiobutton")
        group.add(self.TimeSeriesMenuOptionsCustomDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.TimeSeriesMenuOptionsCustomDraw.GroupIndex = 10
        self.TimeSeriesMenuOptionsStagesAction = createAction(self.TimeSeriesMenuOptionsStagesClick, "More Options...", None, self.TimeSeriesMenuOptions, KeyEvent.VK_M, None, None, "standard")
        
        self.TimeSeriesMenuHelp = self.createMenu("Help", "H", self.MainMenu1)
        self.TimeSeriesMenuHelpOnTimeSeriesAction = createAction(self.TimeSeriesMenuHelpOnTimeSeriesClick, "Help on Time Series", None, self.TimeSeriesMenuHelp, KeyEvent.VK_T, None, None, "standard")
        self.TimeSeriesMenuHelp.addSeparator()
        self.TimeSeriesMenuHelpTopicsAction = createAction(self.TimeSeriesMenuHelpTopicsClick, "Help Topics", None, self.TimeSeriesMenuHelp, KeyEvent.VK_H, None, None, "standard")
        
        #  --------------- UNHANDLED ATTRIBUTE: self.MainMenu1.Top = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.MainMenu1.Left = 478
        
        self.TimeSeriesPopupMenu = JPopupMenu()
        self.TimeSeriesPopupMenuCopyAction = createAction(self.TimeSeriesPopupMenuCopyClick, "Copy", None, self.TimeSeriesPopupMenu, KeyEvent.VK_C, None, None, "standard")
        self.TimeSeriesPopupMenuPasteAction = createAction(self.TimeSeriesPopupMenuPasteClick, "Paste", None, self.TimeSeriesPopupMenu, KeyEvent.VK_P, None, None, "standard")
        self.TimeSeriesPopupMenuSendCopyAction = createAction(self.TimeSeriesMenuSendCopyClick, "Send Copy to Main Window", None, self.TimeSeriesPopupMenu, KeyEvent.VK_S, None, None, "standard")
        self.TimeSeriesPopupMenu.addSeparator()
        self.TimeSeriesPopupMenuBreedAction = createAction(self.TimeSeriesPopupMenuBreedClick, "Breed", None, self.TimeSeriesPopupMenu, None, None, None, "standard")
        #  --------------- UNHANDLED ATTRIBUTE: self.TimeSeriesPopupMenu.Top = 38
        #  --------------- UNHANDLED ATTRIBUTE: self.TimeSeriesPopupMenu.Left = 468
        self.grid.addMouseListener(MenuPopupMouseListener(self.TimeSeriesPopupMenu))
        contentPane.add(self.grid)
        contentPane.add(self.emptyWarningPanel)
        
    def None(self, event):
        print "None"
        
    def TimeSeriesMenuBreedClick(self, event):
        print "TimeSeriesMenuBreedClick"
        
    def TimeSeriesMenuCopyClick(self, event):
        print "TimeSeriesMenuCopyClick"
        
    def TimeSeriesMenuDeleteClick(self, event):
        print "TimeSeriesMenuDeleteClick"
        
    def TimeSeriesMenuHelpOnTimeSeriesClick(self, event):
        print "TimeSeriesMenuHelpOnTimeSeriesClick"
        
    def TimeSeriesMenuHelpTopicsClick(self, event):
        print "TimeSeriesMenuHelpTopicsClick"
        
    def TimeSeriesMenuOptionsBestDrawClick(self, event):
        print "TimeSeriesMenuOptionsBestDrawClick"
        
    def TimeSeriesMenuOptionsCustomDrawClick(self, event):
        print "TimeSeriesMenuOptionsCustomDrawClick"
        
    def TimeSeriesMenuOptionsFastDrawClick(self, event):
        print "TimeSeriesMenuOptionsFastDrawClick"
        
    def TimeSeriesMenuOptionsMediumDrawClick(self, event):
        print "TimeSeriesMenuOptionsMediumDrawClick"
        
    def TimeSeriesMenuOptionsStagesClick(self, event):
        print "TimeSeriesMenuOptionsStagesClick"
        
    def TimeSeriesMenuPasteClick(self, event):
        print "TimeSeriesMenuPasteClick"
        
    def TimeSeriesMenuRedoClick(self, event):
        print "TimeSeriesMenuRedoClick"
        
    def TimeSeriesMenuSendCopyClick(self, event):
        print "TimeSeriesMenuSendCopyClick"
        
    def TimeSeriesMenuUndoClick(self, event):
        print "TimeSeriesMenuUndoClick"
        
    def TimeSeriesMenuUndoRedoListClick(self, event):
        print "TimeSeriesMenuUndoRedoListClick"
        
    def TimeSeriesPopupMenuBreedClick(self, event):
        print "TimeSeriesPopupMenuBreedClick"
        
    def TimeSeriesPopupMenuCopyClick(self, event):
        print "TimeSeriesPopupMenuCopyClick"
        
    def TimeSeriesPopupMenuPasteClick(self, event):
        print "TimeSeriesPopupMenuPasteClick"
        
    def gridMouseDown(self, event):
        print "gridMouseDown"
        
if __name__ == "__main__":
    window = TimeSeriesWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
