from common import *

#Useage:
#        import BreederWindow
#        window = BreederWindow.BreederWindow()
#        window.visible = 1

class BreederWindow(JFrame):
    def __init__(self, title='Breeder'):
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
        self.setBounds(315, 163, 427, 191  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.OnDestroy = FormDestroy
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Menu = BreederMenu
        #  --------------- UNHANDLED ATTRIBUTE: self.AutoScroll = False
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poDefaultPosOnly
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        
        self.plantsDrawGrid = JTable(DefaultTableModel())
        self.plantsDrawGrid.setBounds(2, 48, 345, 141)
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.OnEndDrag = plantsDrawGridEndDrag
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.OnDrawCell = plantsDrawGridDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.OnDragOver = plantsDrawGridDragOver
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.FixedRows = 0
        self.plantsDrawGrid.mousePressed = self.plantsDrawGridMouseDown
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.RowCount = 30
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.DefaultRowHeight = 64
        self.plantsDrawGrid.mouseReleased = self.plantsDrawGridMouseUp
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.OnDblClick = plantsDrawGridDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.Options = [goFixedVertLine, goFixedHorzLine, goRangeSelect]
        self.Label1 = JLabel('The breeder is empty. To make some breeder plants, select a plant (or two plants) in the main window and choose Breed from the Plant menu.', font=buttonFont)
        self.Label1.setBounds(10, 8, 152, 70)
        self.emptyWarningPanel = JPanel(layout=None)
        # -- self.emptyWarningPanel.setLayout(BoxLayout(self.emptyWarningPanel, BoxLayout.Y_AXIS))
        self.emptyWarningPanel.add(self.Label1)
        self.emptyWarningPanel.setBounds(362, 46, 183, 93)
        self.variationLowImage = toolkit.createImage("../resources/BreederForm_variationLow.png")
        self.variationLow = SpeedButton(ImageIcon(self.variationLowImage), 1, actionPerformed=self.variationLowClick, font=buttonFont, margin=buttonMargin)
        self.variationLow.setBounds(74, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.variationLow.GroupIndex = 1
        self.variationMediumImage = toolkit.createImage("../resources/BreederForm_variationMedium.png")
        self.variationMedium = SpeedButton(ImageIcon(self.variationMediumImage), actionPerformed=self.variationMediumClick, font=buttonFont, margin=buttonMargin)
        self.variationMedium.setBounds(102, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.variationMedium.GroupIndex = 1
        self.variationCustomImage = toolkit.createImage("../resources/BreederForm_variationCustom.png")
        self.variationCustom = SpeedButton(ImageIcon(self.variationCustomImage), actionPerformed=self.variationCustomClick, font=buttonFont, margin=buttonMargin)
        self.variationCustom.setBounds(156, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.variationCustom.GroupIndex = 1
        self.varyColorsImage = toolkit.createImage("../resources/BreederForm_varyColors.png")
        self.varyColors = SpeedButton(ImageIcon(self.varyColorsImage), 1, actionPerformed=self.varyColorsClick, font=buttonFont, margin=buttonMargin)
        self.varyColors.setBounds(207, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.varyColors.GroupIndex = 2
        self.vary3DObjectsImage = toolkit.createImage("../resources/BreederForm_vary3DObjects.png")
        self.vary3DObjects = SpeedButton(ImageIcon(self.vary3DObjectsImage), actionPerformed=self.vary3DObjectsClick, font=buttonFont, margin=buttonMargin)
        self.vary3DObjects.setBounds(239, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.vary3DObjects.GroupIndex = 3
        self.helpButtonImage = toolkit.createImage("../resources/BreederForm_helpButton.png")
        self.helpButton = SpeedButton(ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setBounds(310, 4, 25, 25)
        self.variationHighImage = toolkit.createImage("../resources/BreederForm_variationHigh.png")
        self.variationHigh = SpeedButton(ImageIcon(self.variationHighImage), actionPerformed=self.variationHighClick, font=buttonFont, margin=buttonMargin)
        self.variationHigh.setBounds(129, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.variationHigh.GroupIndex = 1
        self.variationNoneNumericImage = toolkit.createImage("../resources/BreederForm_variationNoneNumeric.png")
        self.variationNoneNumeric = SpeedButton(ImageIcon(self.variationNoneNumericImage), actionPerformed=self.variationNoneNumericClick, font=buttonFont, margin=buttonMargin)
        self.variationNoneNumeric.setBounds(47, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.variationNoneNumeric.GroupIndex = 1
        self.breedButtonImage = toolkit.createImage("../resources/BreederForm_breedButton.png")
        self.breedButton = SpeedButton(ImageIcon(self.breedButtonImage), actionPerformed=self.breedButtonClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.breedButton.setBounds(5, 4, 25, 25)
        self.breederToolbarPanel = JPanel(layout=None)
        # -- self.breederToolbarPanel.setLayout(BoxLayout(self.breederToolbarPanel, BoxLayout.Y_AXIS))
        self.breederToolbarPanel.add(self.variationLow)
        self.breederToolbarPanel.add(self.variationMedium)
        self.breederToolbarPanel.add(self.variationCustom)
        self.breederToolbarPanel.add(self.varyColors)
        self.breederToolbarPanel.add(self.vary3DObjects)
        self.breederToolbarPanel.add(self.helpButton)
        self.breederToolbarPanel.add(self.variationHigh)
        self.breederToolbarPanel.add(self.variationNoneNumeric)
        self.breederToolbarPanel.add(self.breedButton)
        self.breederToolbarPanel.setBounds(2, 10, 339, 33)
        
        self.BreederMenu = JMenuBar()
        self.setJMenuBar(self.BreederMenu)

        self.BreederMenuEdit = self.createMenu("Edit", "E", self.BreederMenu)
        self.BreederMenuUndoAction = createAction(self.BreederMenuUndoClick, "Undo", None, self.BreederMenuEdit, KeyEvent.VK_U, None, None, "standard")
        self.BreederMenuRedoAction = createAction(self.BreederMenuRedoClick, "Redo", None, self.BreederMenuEdit, KeyEvent.VK_R, None, None, "standard")
        self.BreederMenuUndoRedoListAction = createAction(self.BreederMenuUndoRedoListClick, "Undo/Redo List...", None, self.BreederMenuEdit, KeyEvent.VK_L, None, None, "standard")
        self.BreederMenuEdit.addSeparator()
        self.BreederMenuCopyAction = createAction(self.BreederMenuCopyClick, "Copy", None, self.BreederMenuEdit, KeyEvent.VK_C, None, None, "standard")
        self.BreederMenuPasteAction = createAction(self.BreederMenuPasteClick, "Paste", None, self.BreederMenuEdit, KeyEvent.VK_P, None, None, "standard")
        self.BreederMenuSendCopyToMainWindowAction = createAction(self.BreederMenuSendCopyToMainWindowClick, "Send Copy to Main Window", None, self.BreederMenuEdit, KeyEvent.VK_S, None, None, "standard")
        
        self.BreederMenuPlant = self.createMenu("Breed", "B", self.BreederMenu)
        self.BreederMenuBreedAction = createAction(self.BreederMenuBreedClick, "Breed", None, self.BreederMenuPlant, KeyEvent.VK_B, None, None, "standard")
        self.BreederMenuMakeTimeSeriesAction = createAction(self.BreederMenuMakeTimeSeriesClick, "Make Time Series", None, self.BreederMenuPlant, KeyEvent.VK_T, None, None, "standard")
        self.BreederMenuPlant.addSeparator()
        self.BreederMenuDeleteRowAction = createAction(self.BreederMenuDeleteRowClick, "Delete Generation", None, self.BreederMenuPlant, KeyEvent.VK_G, None, None, "standard")
        self.BreederMenuDeleteAllAction = createAction(self.BreederMenuDeleteAllClick, "Delete All", None, self.BreederMenuPlant, KeyEvent.VK_A, None, None, "standard")
        self.BreederMenuPlant.addSeparator()
        self.BreederMenuRandomizeAction = createAction(self.BreederMenuRandomizeClick, "Randomize", None, self.BreederMenuPlant, KeyEvent.VK_R, None, None, "standard")
        self.BreederMenuRandomizeAllAction = createAction(self.BreederMenuRandomizeAllClick, "Randomize All", None, self.BreederMenuPlant, KeyEvent.VK_L, None, None, "standard")
        
        self.BreederMenuOptions = self.createMenu("Options", "O", self.BreederMenu)
        self.BreederMenuOptionsDrawAs = JMenu("Draw Using")
        self.BreederMenuOptionsDrawAs.setMnemonic(KeyEvent.VK_D)
        self.BreederMenuOptions.add(self.BreederMenuOptionsDrawAs)
        group = ButtonGroup()
        self.BreederMenuOptionsFastDrawAction = createAction(self.BreederMenuOptionsFastDrawClick, "Bounding Boxes", None, self.BreederMenuOptionsDrawAs, KeyEvent.VK_B, None, None, "radiobutton")
        group.add(self.BreederMenuOptionsFastDrawAction.menuItem)
        self.BreederMenuOptionsFastDrawAction.setChecked(1)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuOptionsFastDraw.GroupIndex = 10
        self.BreederMenuOptionsMediumDrawAction = createAction(self.BreederMenuOptionsMediumDrawClick, "Wire Frames", None, self.BreederMenuOptionsDrawAs, KeyEvent.VK_W, None, None, "radiobutton")
        group.add(self.BreederMenuOptionsMediumDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuOptionsMediumDraw.GroupIndex = 10
        self.BreederMenuOptionsBestDrawAction = createAction(self.BreederMenuOptionsBestDrawClick, "Solids", None, self.BreederMenuOptionsDrawAs, KeyEvent.VK_S, None, None, "radiobutton")
        group.add(self.BreederMenuOptionsBestDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuOptionsBestDraw.GroupIndex = 10
        self.BreederMenuOptionsCustomDrawAction = createAction(self.BreederMenuOptionsCustomDrawClick, "Custom...", None, self.BreederMenuOptionsDrawAs, KeyEvent.VK_C, None, None, "radiobutton")
        group.add(self.BreederMenuOptionsCustomDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuOptionsCustomDraw.GroupIndex = 10
        self.BreederMenuVariation = JMenu("Vary Numbers")
        self.BreederMenuVariation.setMnemonic(KeyEvent.VK_N)
        self.BreederMenuOptions.add(self.BreederMenuVariation)
        group = ButtonGroup()
        self.BreederMenuVariationNoneAction = createAction(self.BreederMenuVariationNoneClick, "None", None, self.BreederMenuVariation, KeyEvent.VK_N, None, None, "radiobutton")
        group.add(self.BreederMenuVariationNoneAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuVariationNone.GroupIndex = 1
        self.BreederMenuVariationLowAction = createAction(self.BreederMenuVariationLowClick, "Low", None, self.BreederMenuVariation, KeyEvent.VK_L, None, None, "radiobutton")
        group.add(self.BreederMenuVariationLowAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuVariationLow.GroupIndex = 1
        self.BreederMenuVariationMediumAction = createAction(self.BreederMenuVariationMediumClick, "Medium", None, self.BreederMenuVariation, KeyEvent.VK_M, None, None, "radiobutton")
        group.add(self.BreederMenuVariationMediumAction.menuItem)
        self.BreederMenuVariationMediumAction.setChecked(1)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuVariationMedium.GroupIndex = 1
        self.BreederMenuVariationHighAction = createAction(self.BreederMenuVariationHighClick, "High", None, self.BreederMenuVariation, KeyEvent.VK_H, None, None, "radiobutton")
        group.add(self.BreederMenuVariationHighAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuVariationHigh.GroupIndex = 1
        self.BreederMenuVariationCustomAction = createAction(self.BreederMenuVariationCustomClick, "Custom...", None, self.BreederMenuVariation, KeyEvent.VK_C, None, None, "radiobutton")
        group.add(self.BreederMenuVariationCustomAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuVariationCustom.GroupIndex = 1
        self.BreederMenuVaryColorsAction = createAction(self.BreederMenuVaryColorsClick, "Vary Colors", None, self.BreederMenuOptions, KeyEvent.VK_C, None, None, "checkbox")
        self.BreederMenuVaryColorsAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuVaryColors.GroupIndex = 1
        self.BreederMenuVary3DObjectsAction = createAction(self.BreederMenuVary3DObjectsClick, "Vary 3D Objects", None, self.BreederMenuOptions, KeyEvent.VK_3, None, None, "checkbox")
        self.BreederMenuVary3DObjectsAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenuVary3DObjects.GroupIndex = 1
        self.BreederMenuOptions.addSeparator()
        self.BreederMenuOtherOptionsAction = createAction(self.BreederMenuOtherOptionsClick, "More Options...", None, self.BreederMenuOptions, KeyEvent.VK_M, None, None, "standard")
        
        self.MenuBreederHelp = self.createMenu("Help", "H", self.BreederMenu)
        self.BreederMenuHelpOnBreedingAction = createAction(self.BreederMenuHelpOnBreedingClick, "Help on Breeding", None, self.MenuBreederHelp, KeyEvent.VK_B, None, None, "standard")
        self.MenuBreederHelp.addSeparator()
        self.BreederMenuHelpTopicsAction = createAction(self.BreederMenuHelpTopicsClick, "Help Topics", None, self.MenuBreederHelp, KeyEvent.VK_H, None, None, "standard")
        
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenu.Top = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederMenu.Left = 360
        
        self.BreederPopupMenu = JPopupMenu()
        self.BreederPopupMenuBreedAction = createAction(self.BreederPopupMenuBreedClick, "Breed", None, self.BreederPopupMenu, KeyEvent.VK_B, None, None, "standard")
        self.BreederPopupMenu.addSeparator()
        self.BreederPopupMenuCopyAction = createAction(self.BreederPopupMenuCopyClick, "Copy", None, self.BreederPopupMenu, KeyEvent.VK_C, None, None, "standard")
        self.BreederPopupMenuPasteAction = createAction(self.BreederPopupMenuPasteClick, "Paste", None, self.BreederPopupMenu, KeyEvent.VK_P, None, None, "standard")
        self.BreederPopupMenuSendCopytoMainWindowAction = createAction(self.BreederPopupMenuSendCopytoMainWindowClick, "Send Copy to Main Window", None, self.BreederPopupMenu, KeyEvent.VK_S, None, None, "standard")
        self.BreederPopupMenu.addSeparator()
        self.BreederPopupMenuRandomizeAction = createAction(self.BreederPopupMenuRandomizeClick, "Randomize", None, self.BreederPopupMenu, KeyEvent.VK_R, None, None, "standard")
        self.BreederPopupMenuMakeTimeSeriesAction = createAction(self.BreederPopupMenuMakeTimeSeriesClick, "Make Time Series", None, self.BreederPopupMenu, KeyEvent.VK_M, None, None, "standard")
        self.BreederPopupMenu.addSeparator()
        self.BreederPopupMenuDeleteRowAction = createAction(self.BreederPopupMenuDeleteRowClick, "Delete generation", None, self.BreederPopupMenu, KeyEvent.VK_G, None, None, "standard")
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederPopupMenu.Top = 12
        #  --------------- UNHANDLED ATTRIBUTE: self.BreederPopupMenu.Left = 396
        self.plantsDrawGrid.addMouseListener(MenuPopupMouseListener(self.BreederPopupMenu))
        contentPane.add(self.plantsDrawGrid)
        contentPane.add(self.emptyWarningPanel)
        contentPane.add(self.breederToolbarPanel)
        
    def None(self, event):
        print "None"
        
    def BreederMenuBreedClick(self, event):
        print "BreederMenuBreedClick"
        
    def BreederMenuCopyClick(self, event):
        print "BreederMenuCopyClick"
        
    def BreederMenuDeleteAllClick(self, event):
        print "BreederMenuDeleteAllClick"
        
    def BreederMenuDeleteRowClick(self, event):
        print "BreederMenuDeleteRowClick"
        
    def BreederMenuHelpOnBreedingClick(self, event):
        print "BreederMenuHelpOnBreedingClick"
        
    def BreederMenuHelpTopicsClick(self, event):
        print "BreederMenuHelpTopicsClick"
        
    def BreederMenuMakeTimeSeriesClick(self, event):
        print "BreederMenuMakeTimeSeriesClick"
        
    def BreederMenuOptionsBestDrawClick(self, event):
        print "BreederMenuOptionsBestDrawClick"
        
    def BreederMenuOptionsCustomDrawClick(self, event):
        print "BreederMenuOptionsCustomDrawClick"
        
    def BreederMenuOptionsFastDrawClick(self, event):
        print "BreederMenuOptionsFastDrawClick"
        
    def BreederMenuOptionsMediumDrawClick(self, event):
        print "BreederMenuOptionsMediumDrawClick"
        
    def BreederMenuOtherOptionsClick(self, event):
        print "BreederMenuOtherOptionsClick"
        
    def BreederMenuPasteClick(self, event):
        print "BreederMenuPasteClick"
        
    def BreederMenuRandomizeAllClick(self, event):
        print "BreederMenuRandomizeAllClick"
        
    def BreederMenuRandomizeClick(self, event):
        print "BreederMenuRandomizeClick"
        
    def BreederMenuRedoClick(self, event):
        print "BreederMenuRedoClick"
        
    def BreederMenuSendCopyToMainWindowClick(self, event):
        print "BreederMenuSendCopyToMainWindowClick"
        
    def BreederMenuUndoClick(self, event):
        print "BreederMenuUndoClick"
        
    def BreederMenuUndoRedoListClick(self, event):
        print "BreederMenuUndoRedoListClick"
        
    def BreederMenuVariationCustomClick(self, event):
        print "BreederMenuVariationCustomClick"
        
    def BreederMenuVariationHighClick(self, event):
        print "BreederMenuVariationHighClick"
        
    def BreederMenuVariationLowClick(self, event):
        print "BreederMenuVariationLowClick"
        
    def BreederMenuVariationMediumClick(self, event):
        print "BreederMenuVariationMediumClick"
        
    def BreederMenuVariationNoneClick(self, event):
        print "BreederMenuVariationNoneClick"
        
    def BreederMenuVary3DObjectsClick(self, event):
        print "BreederMenuVary3DObjectsClick"
        
    def BreederMenuVaryColorsClick(self, event):
        print "BreederMenuVaryColorsClick"
        
    def BreederPopupMenuBreedClick(self, event):
        print "BreederPopupMenuBreedClick"
        
    def BreederPopupMenuCopyClick(self, event):
        print "BreederPopupMenuCopyClick"
        
    def BreederPopupMenuDeleteRowClick(self, event):
        print "BreederPopupMenuDeleteRowClick"
        
    def BreederPopupMenuMakeTimeSeriesClick(self, event):
        print "BreederPopupMenuMakeTimeSeriesClick"
        
    def BreederPopupMenuPasteClick(self, event):
        print "BreederPopupMenuPasteClick"
        
    def BreederPopupMenuRandomizeClick(self, event):
        print "BreederPopupMenuRandomizeClick"
        
    def BreederPopupMenuSendCopytoMainWindowClick(self, event):
        print "BreederPopupMenuSendCopytoMainWindowClick"
        
    def breedButtonClick(self, event):
        print "breedButtonClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def plantsDrawGridMouseDown(self, event):
        print "plantsDrawGridMouseDown"
        
    def plantsDrawGridMouseUp(self, event):
        print "plantsDrawGridMouseUp"
        
    def variationCustomClick(self, event):
        print "variationCustomClick"
        
    def variationHighClick(self, event):
        print "variationHighClick"
        
    def variationLowClick(self, event):
        print "variationLowClick"
        
    def variationMediumClick(self, event):
        print "variationMediumClick"
        
    def variationNoneNumericClick(self, event):
        print "variationNoneNumericClick"
        
    def vary3DObjectsClick(self, event):
        print "vary3DObjectsClick"
        
    def varyColorsClick(self, event):
        print "varyColorsClick"
        
if __name__ == "__main__":
    window = BreederWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
