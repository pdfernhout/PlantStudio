# unit Ubreedr

from swing_helpers import *
import swingdrawingsurface

import math

from conversion_common import *
import delphi_compatability

import ucollect
import ugener
import usupport
import uplant
import ubmpsupport
import udomain
import updcom

"""
import utimeser
import ucommand
import umain
import umath
import ucursor
import ubrdopt
import updform
"""

# var
# PDF PORT COMMENTED OUT FOR NOW
#BreederForm = TBreederForm()

# const
kRedrawPlants = True
kDontRedrawPlants = False
kConsiderIfPreviewCacheIsUpToDate = True
kDontConsiderIfPreviewCacheIsUpToDate = False

# const
kSelectionIsInFirstColumn = True
kSelectionIsNotInFirstColumn = False

kFirstColumnWidth = 20

kBetweenGap = 4

kOptionTabSize = 0
kOptionTabMutation = 1
kOptionTabBlending = 2
kOptionTabNonNumeric = 3
kOptionTabTdos = 4

class PlantDrawingArea(JPanel):
    def __init__(self, mouseDownMethod):
        JPanel.__init__(self)
        self.connect("expose_event", self.expose)
        self.RowCount = 30
        self.ColCount = 10
        self.DefaultRowHeight = 64
        self.DefaultColWidth = 64
        self.OnDrawCell = None
        self.ColWidths = {}
        if mouseDownMethod:
            self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
            self.connect("button_press_event", mouseDownMethod)
        self.set_size_request(11 * 64, 30 * 64) 
        
    #def get_child_requisition(self):
    #    # a little extra big for first column with number
    #    return self.ColCount * self.DefaultRowHeight, self.RowCount * self.DefaultColWidth
            
    def boundsForCell(self, colTarget, rowTarget):
        usedHeight = self.DefaultRowHeight * rowTarget
        usedWidth = 0
        for col in range(colTarget + 1):
            try:
                colWidth = self.ColWidths[col]
            except KeyError:
                colWidth = self.DefaultColWidth
            left = usedWidth
            top = usedHeight
            usedWidth += colWidth
            right = usedWidth
            bottom = usedHeight + self.DefaultRowHeight
        cellBounds = Rect(left, top, right, bottom)
        return cellBounds
        
    def updateForChanges(self):
        cellBounds = self.boundsForCell(self.ColCount - 1, self.RowCount - 1)
        usedWidth = cellBounds.right
        usedHeight = cellBounds.bottom
        self.set_size_request(max(usedWidth, 100), max(usedHeight, 100))
        self.queue_resize()
        
    def expose(self, widget, event):
        gc = widget.window.new_gc()
        context = (widget.window, gc) 
        
        if not self.OnDrawCell:
            return
        
        Cursor_StartWait()
        try:
            usedHeight = 0
            for row in range(self.RowCount):
                usedWidth = 0
                for col in range(self.ColCount):
                    try:
                        colWidth = self.ColWidths[col]
                    except KeyError:
                        colWidth = self.DefaultColWidth
                    left = usedWidth
                    top = usedHeight
                    usedWidth += colWidth
                    right = usedWidth
                    bottom = usedHeight + self.DefaultRowHeight 
                    cellBounds = Rect(left, top, right, bottom)
                    state = None
                    self.OnDrawCell(self, gc, col, row, cellBounds, state)
                usedHeight += self.DefaultRowHeight  
        finally:
            Cursor_StopWait()
            
    def MouseToCell(self, x, y):
        usedHeight = 0
        for row in range(self.RowCount):
            usedWidth = 0
            for col in range(self.ColCount):
                try:
                    colWidth = self.ColWidths[col]
                except KeyError:
                    colWidth = self.DefaultColWidth
                left = usedWidth
                top = usedHeight
                usedWidth += colWidth
                right = usedWidth
                bottom = usedHeight + self.DefaultRowHeight 
                if left <= x and x < right:
                    if top <= y and y < bottom:
                        return col, row
            usedHeight += self.DefaultRowHeight   
        return None , None    
    
    def Invalidate(self):
        InvalidateWidget(self)   
            
class TBreederForm:
    def __init__(self):
        self.generations = ucollect.TListCollection()
        self.lightUpCell = delphi_compatability.TPoint(0, 0)
        self.selectedRow = 0
        self.font = None # gtk.gdk.Font('fixed')
        
        self.BuildWindow()
        self.plantsDrawGrid.ColWidths[0] = kFirstColumnWidth
        
        ShowWindow(self.window)
        
        # PDF PORT FOR TESTING
        import uplant
        self.fileName = "Garden plants.pla"
        plants = uplant.PlantLoader().loadPlantsFromFile(self.fileName, inPlantMover=1, justLoad=1)
        
        lastPlant = None
        for plant in plants:
            newGeneration = ugener.PdGeneration().createWithParents(plant, lastPlant, 0.5)
            self.addGeneration(newGeneration)
            lastPlant = plant
            
        ucursor.windowsToWaitWith.append(self.window.window)
        
        return
    
        self.BreederMenu = TMainMenu()
        self.BreederMenuEdit = TMenuItem()
        self.BreederMenuCopy = TMenuItem()
        self.BreederMenuPaste = TMenuItem()
        self.N2 = TMenuItem()
        self.BreederMenuPlant = TMenuItem()
        self.BreederMenuBreed = TMenuItem()
        self.BreederMenuUndo = TMenuItem()
        self.BreederMenuRedo = TMenuItem()
        self.N1 = TMenuItem()
        self.BreederMenuDeleteRow = TMenuItem()
        self.BreederMenuDeleteAll = TMenuItem()
        self.BreederPopupMenu = TPopupMenu()
        self.BreederPopupMenuBreed = TMenuItem()
        self.BreederPopupMenuCopy = TMenuItem()
        self.BreederPopupMenuPaste = TMenuItem()
        self.BreederPopupMenuDeleteRow = TMenuItem()
        self.N4 = TMenuItem()
        self.BreederMenuRandomize = TMenuItem()
        self.BreederMenuRandomizeAll = TMenuItem()
        self.BreederMenuMakeTimeSeries = TMenuItem()
        self.BreederPopupMenuRandomize = TMenuItem()
        self.N5 = TMenuItem()
        self.emptyWarningPanel = TPanel()
        self.Label1 = TLabel()
        self.BreederPopupMenuMakeTimeSeries = TMenuItem()
        self.BreederMenuVariation = TMenuItem()
        self.BreederMenuVariationLow = TMenuItem()
        self.BreederMenuVariationMedium = TMenuItem()
        self.BreederMenuVariationHigh = TMenuItem()
        self.BreederMenuVariationCustom = TMenuItem()
        self.BreederMenuOptions = TMenuItem()
        self.BreederMenuOtherOptions = TMenuItem()
        self.MenuBreederHelp = TMenuItem()
        self.BreederMenuHelpOnBreeding = TMenuItem()
        self.BreederMenuHelpTopics = TMenuItem()
        self.N3 = TMenuItem()
        self.BreederMenuOptionsDrawAs = TMenuItem()
        self.BreederMenuOptionsFastDraw = TMenuItem()
        self.BreederMenuOptionsMediumDraw = TMenuItem()
        self.BreederMenuOptionsBestDraw = TMenuItem()
        self.BreederMenuOptionsCustomDraw = TMenuItem()
        self.N6 = TMenuItem()
        self.BreederMenuVaryColors = TMenuItem()
        self.BreederMenuVary3DObjects = TMenuItem()
        self.breederToolbarPanel = TPanel()
        self.variationLow = TSpeedButton()
        self.variationMedium = TSpeedButton()
        self.variationCustom = TSpeedButton()
        self.varyColors = TSpeedButton()
        self.vary3DObjects = TSpeedButton()
        self.helpButton = TSpeedButton()
        self.variationHigh = TSpeedButton()
        self.BreederMenuVariationNone = TMenuItem()
        self.variationNoneNumeric = TSpeedButton()
        self.BreederMenuSendCopyToMainWindow = TMenuItem()
        self.N7 = TMenuItem()
        self.BreederPopupMenuSendCopytoMainWindow = TMenuItem()
        self.N8 = TMenuItem()
        self.breedButton = TSpeedButton()
        self.BreederMenuUndoRedoList = TMenuItem()
        self.dragPlantStartPoint = TPoint()
        self.numBreederPlantsCopiedThisSession = 0L
        self.internalChange = False
        self.drawing = False
        self.needToRedrawFromChangeToDrawOptions = False
        
    def FormCreate(self, Sender):
        tempBoundsRect = TRect()
        
        self.plantsDrawGrid.DragCursor = ucursor.crDragPlant
        self.Position = delphi_compatability.TPosition.poDesigned
        # keep window on screen - left corner of title bar 
        tempBoundsRect = udomain.domain.breederWindowRect
        if (tempBoundsRect.Left != 0) or (tempBoundsRect.Right != 0) or (tempBoundsRect.Top != 0) or (tempBoundsRect.Bottom != 0):
            if tempBoundsRect.Left > delphi_compatability.Screen.Width - umain.kMinWidthOnScreen:
                tempBoundsRect.Left = delphi_compatability.Screen.Width - umain.kMinWidthOnScreen
            if tempBoundsRect.Top > delphi_compatability.Screen.Height - umain.kMinHeightOnScreen:
                tempBoundsRect.Top = delphi_compatability.Screen.Height - umain.kMinHeightOnScreen
            self.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom)
        if udomain.domain.options.drawSpeed == udomain.kDrawFast:
            self.BreederMenuOptionsFastDraw.checked = True
        elif udomain.domain.options.drawSpeed == udomain.kDrawMedium:
            self.BreederMenuOptionsMediumDraw.checked = True
        elif udomain.domain.options.drawSpeed == udomain.kDrawBest:
            self.BreederMenuOptionsBestDraw.checked = True
        elif udomain.domain.options.drawSpeed == udomain.kDrawCustom:
            self.BreederMenuOptionsCustomDraw.checked = True
        self.updateForChangeToDomainOptions()
        self.updateMenusForChangeToGenerations()
        #to get redo messages
        umain.MainForm.updateMenusForUndoRedo()
        self.lightUpCell = Point(-1, -1)
        self.emptyWarningPanel.SendToBack()

    def BuildWindow(self):
        self.window = MakeWindow("Breeder", 750, 500)
        
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.window.add(scrolled_window)
        scrolled_window.show()
        self.scrolledWindow = scrolled_window
                
        self.plantsDrawGrid = DrawGrid(self.plantsDrawGridMouseDown)
        self.plantsDrawGrid.RowCount = 30
        self.plantsDrawGrid.DefaultRowHeight = 64
        self.plantsDrawGrid.DefaultColWidth = 64
        self.plantsDrawGrid.OnDrawCell = self.plantsDrawGridDrawCell
        self.plantsDrawGrid.updateForChanges()
        
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.OnEndDrag = self.plantsDrawGridEndDrag
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.OnDragOver = self.plantsDrawGridDragOver
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.OnDblClick = self.plantsDrawGridDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsDrawGrid.Options = [goFixedVertLine, goFixedHorzLine, goRangeSelect]
    
        self.plantsDrawGrid.show()
        scrolled_window.add_with_viewport(self.plantsDrawGrid)
        viewport = scrolled_window.get_child()
        viewport.set_shadow_type(gtk.SHADOW_NONE)
        
        return
                
        ### PORT toolkit = java.awt.Toolkit.getDefaultToolkit()
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.OnDestroy = FormDestroy
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Menu = BreederMenu
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        
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
    
    def FormActivate(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        if len(self.generations) <= 0:
            self.emptyWarningPanel.BringToFront()
        elif self.needToRedrawFromChangeToDrawOptions:
            self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate)
            self.needToRedrawFromChangeToDrawOptions = False

    # a menu is top item on the menu bar and can be pulled down for a list of menu items
    def createMenu(self, name, mnemonic=None, menuBar = None):
        menu = JMenu(name)
        if mnemonic:
            menu.setMnemonic(mnemonic)
        if menuBar:
            menuBar.add(menu)
        return menu
        
    # -------------------------------------------------------------------------------------- grid 
    def updateForChangeToDomainOptions(self):
        if self.plantsDrawGrid.ColCount != udomain.domain.breedingAndTimeSeriesOptions.plantsPerGeneration + 1:
            self.plantsDrawGrid.ColCount = udomain.domain.breedingAndTimeSeriesOptions.plantsPerGeneration + 1
            self.plantsDrawGrid.updateForChanges()
        if ((self.plantsDrawGrid.DefaultColWidth != udomain.domain.breedingAndTimeSeriesOptions.thumbnailWidth) or (self.plantsDrawGrid.DefaultRowHeight != udomain.domain.breedingAndTimeSeriesOptions.thumbnailHeight)):
            self.plantsDrawGrid.DefaultColWidth = udomain.domain.breedingAndTimeSeriesOptions.thumbnailWidth
            self.plantsDrawGrid.ColWidths[0] = kFirstColumnWidth
            self.plantsDrawGrid.DefaultRowHeight = udomain.domain.breedingAndTimeSeriesOptions.thumbnailHeight
            self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate)
        if udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationLow:
            self.BreederMenuVariationLow.checked = True
            self.variationLow.Down = True
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationMedium:
            self.BreederMenuVariationMedium.checked = True
            self.variationMedium.Down = True
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationHigh:
            self.BreederMenuVariationHigh.checked = True
            self.variationHigh.Down = True
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationCustom:
            self.BreederMenuVariationCustom.checked = True
            self.variationCustom.Down = True
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationNoNumeric:
            self.BreederMenuVariationNone.checked = True
            self.variationNoneNumeric.Down = True
        self.BreederMenuVaryColors.checked = udomain.domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues
        self.varyColors.Down = udomain.domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues
        self.BreederMenuVary3DObjects.checked = udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary
        self.vary3DObjects.Down = udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary
        self.redoCaption()
        atLeastOnePlantHasChangedAge = False
        for generation in self.generations:
            for plant in generation.plants:
                newAge = intround(udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0 * plant.pGeneral.ageAtMaturity)
                if plant.age != newAge:
                    plant.setAge(newAge)
                    atLeastOnePlantHasChangedAge = True
        if atLeastOnePlantHasChangedAge:
            self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate)
    
    def redrawPlants(self, considerIfPreviewCacheIsUpToDate):
        if not considerIfPreviewCacheIsUpToDate:
            for generation in self.generations:
                for plant in generation.plants:
                    plant.previewCacheUpToDate = False
        self.plantsDrawGrid.Invalidate()
        self.plantsDrawGrid.Update()
    
    def plantsDrawGridDrawCell(self, widget, gc, Col, Row, cellRect, State):
        width = usupport.rWidth(cellRect)
        height = usupport.rHeight(cellRect)
        # PDF PORT TEMPORARILY COMMENT OUT
        #self.plantsDrawGrid.Canvas.Font = self.plantsDrawGrid.Font
        #self.plantsDrawGrid.Canvas.Font.Color = delphi_compatability.clBlack
        if Col == 0:
            penWidth = 1
            font = self.font
            penColor = delphi_compatability.clWhite
            brushColor = delphi_compatability.clWhite
            DrawRectangle(widget.window, gc, cellRect, penWidth, penColor, brushColor)
            if Row > len(self.generations) - 1:
                return
            text = IntToStr(Row + 1)
            textWidth = MeasureTextWidth(widget, gc, text)
            textHeight = MeasureTextHeight(widget, gc, "0")
            textDrawRect = Rect(0, 0, 0, 0)
            textDrawRect.left = cellRect.left + width / 2 - textWidth / 2
            textDrawRect.top = cellRect.top + height / 2 - textHeight / 2
            brushColor = delphi_compatability.clBlack
            DrawText(widget.window, gc, textDrawRect, text, font, brushColor)
            return
        else:
            penWidth = 1
            penColor = delphi_compatability.clWhite
            brushColor = delphi_compatability.clWhite
            DrawRectangle(widget.window, gc, cellRect, penWidth, penColor, brushColor)
        generation = self.generationForIndex(Row)
        if generation == None:
            return
        plant = generation.plantForIndex(Col - 1)
        if plant == None:
            return
        if not plant.previewCacheUpToDate:
            if not plant.previewCache.Width != width or plant.previewCache.Height != height:
                plant.previewCache.Width = width
                plant.previewCache.Height = height
                plant.previewCache.updateForChanges(widget.window)
                plant.previewCache.pixmap.widget = widget.window
                plant.previewCache.Fill(gc, delphi_compatability.clWhite)
                plant.previewCache.pixmap.widget = None
            # draw plant 
            # draw gray solid box to show delay for drawing plant cache
            penWidth = 1
            penColor = delphi_compatability.clSilver
            brushColor = delphi_compatability.clSilver
            DrawRectangle(widget.window, gc, cellRect, penWidth, penColor, brushColor, filled=1)
            
            # draw plant preview cache
            plant.fixedPreviewScale = False
            plant.fixedDrawPosition = False
            # PDF PORT __ FOR TESTING
            #flag = umain.kDrawNow
            flag = True
            plant.previewCache.pixmap.widget = widget.window
            plant.drawPreviewIntoCache(gc, delphi_compatability.TPoint(self.plantsDrawGrid.DefaultColWidth, self.plantsDrawGrid.DefaultRowHeight), uplant.kDontConsiderDomainScale, flag)
            plant.previewCache.pixmap.widget = None
        plant.previewCache.Transparent = False
        ubmpsupport.copyBitmapToCanvasWithGlobalPalette(gc, plant.previewCache, self.plantsDrawGrid.window, cellRect)

        # draw selection rectangle 
        #self.plantsDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        penWidth = 2
        if (Col == self.lightUpCell.X) and (Row == self.lightUpCell.Y):
            penColor = delphi_compatability.clAqua
        elif Row == self.selectedRow:
            if plant == generation.firstSelectedPlant():
                penColor = udomain.domain.options.firstSelectionRectangleColor
            elif plant == generation.secondSelectedPlant():
                penColor = udomain.domain.options.multiSelectionRectangleColor
            else:
                penColor = delphi_compatability.clSilver
        else:
            penColor = delphi_compatability.clSilver
        # inset rect for drawing issue with pen
        aRect = Rect(cellRect.left, cellRect.top, cellRect.right - penWidth,  cellRect.bottom - penWidth)
        DrawRectangle(widget.window, gc, aRect, penWidth, penColor, penColor, filled=0)
        label = ""
        if plant == generation.firstParent:
            # draw parent indicator 
            label = "p1"
        elif plant == generation.secondParent:
            label = "p2"
        if label:
            textHeight = MeasureTextHeight(widget, gc, "0")
            textDrawRect = Rect(cellRect.left + 4, cellRect.top + 2 + textHeight, 0, 0)
            font = self.font
            brushColor = delphi_compatability.clBlack
            DrawText(widget.window, gc, textDrawRect, label, font, brushColor)

    
    def invalidateGridCell(self, column, row):
        if (column < 0) and (row < 0):
            return
        cellRectOver = self.plantsDrawGrid.CellRect(column, row)
        UNRESOLVED.invalidateRect(self.plantsDrawGrid.Handle, cellRectOver, True)
    
    def invalidateGridRow(self, row):
        if row < 0:
            return
        rowRectOver = self.plantsDrawGrid.CellRect(0, row)
        rowRectOver.Right = self.plantsDrawGrid.Width
        UNRESOLVED.invalidateRect(self.plantsDrawGrid.Handle, rowRectOver, True)
    
    def plantsDrawGridDblClick(self, Sender):
        self.BreederMenuBreedClick(self)
    
    # ------------------------------------------------------------------------ dragging 
    def plantsDrawGridMouseDown(self, widget, event):
        # GTK BUG __ SEEMS TO CALL THREE TIMES IF DOUBLE CLICK 9only last is double click)
        isDoubleClick = event.type == gtk.gdk._2BUTTON_PRESS
        if isDoubleClick:
            self.plantsDrawGridDblClick(event)
            return
        x = event.x
        y = event.y
        col, row = self.plantsDrawGrid.MouseToCell(x, y)
        if (row >= 0) and (row <= len(self.generations) - 1):
            generation = self.generations[row]
            if generation != None:
                self.selectGeneration(generation)
                if (col >= 1) and (col <= len(generation.plants)):
                    plant = generation.plants[col - 1]
                    if plant != None:
                        shiftHeldDown = event.state & gtk.gdk.SHIFT_MASK
                        generation.selectPlant(plant, shiftHeldDown)
                    else:
                        generation.deselectAllPlants()
                    # in first column or past them on right 
                else:
                    generation.deselectAllPlants()
            else:
                self.deselectAllGenerations()
        else:
            self.deselectAllGenerations()
        self.updateForChangeToGenerations()
        # PDF PORT __ DRAGGIGN RELATED FIX LATER
        """
        if (Button == delphi_compatability.TMouseButton.mbRight) or (delphi_compatability.TShiftStateEnum.ssShift in Shift):
            # start drag of plant
            return
        """
        plant = self.plantAtMouse(x, y)
        if plant == None:
            return
        self.dragPlantStartPoint = Point(x, y)
        """ PDF DRAG RELATED FIX
        self.plantsDrawGrid.BeginDrag(False)
        """
    
    def plantsDrawGridDragOver(self, Sender, Source, X, Y, State, Accept):
        Accept = (Source != None) and (Sender != None) and ((Sender == Source) or (Source == umain.MainForm.drawingPaintBox) or (Source == umain.MainForm.plantListDrawGrid) or (Source == utimeser.TimeSeriesForm.grid))
        if (Accept):
            plant = self.plantAtMouse(X, Y)
            if plant == None:
                Accept = False
                return Accept
            col, row = self.plantsDrawGrid.MouseToCell(X, Y, col, row)
            if (col != self.lightUpCell.X) or (row != self.lightUpCell.Y):
                self.invalidateGridCell(self.lightUpCell.X, self.lightUpCell.Y)
                self.lightUpCell = Point(col, row)
                self.invalidateGridCell(col, row)
        return Accept
    
    def plantsDrawGridEndDrag(self, Sender, Target, X, Y):
        if delphi_compatability.Application.terminated:
            return
        # remove lightup on cell before resetting cell
        self.invalidateGridCell(self.lightUpCell.X, self.lightUpCell.Y)
        self.lightUpCell = Point(-1, -1)
        if Target == None:
            return
        # get plant being dragged 
        plant = self.plantAtMouse(self.dragPlantStartPoint.X, self.dragPlantStartPoint.Y)
        if plant == None:
            return
        if (Target == umain.MainForm.drawingPaintBox) or (Target == umain.MainForm.plantListDrawGrid):
            # make paste command - wants list of plants 
            newPlant = plant.makeCopy()
            self.numBreederPlantsCopiedThisSession += 1
            newPlant.setName("Breeder plant " + IntToStr(self.numBreederPlantsCopiedThisSession))
            if (Target == umain.MainForm.drawingPaintBox):
                newPlant.moveTo(Point(X, Y))
            else:
                newPlant.moveTo(umain.MainForm.standardPastePosition())
            if not udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
                # v2.1
                newPlant.calculateDrawingScaleToLookTheSameWithDomainScale()
            #to save memory - don't need it in main window
            newPlant.shrinkPreviewCache()
            newPlants = delphi_compatability.TList()
            newPlants.Add(newPlant)
            newCommand = updcom.PdPasteCommand().createWithListOfPlantsAndOldSelectedList(newPlants, umain.MainForm.selectedPlants)
            newCommand.useSpecialPastePosition = True
            try:
                ucursor.cursor_startWait()
                umain.MainForm.doCommand(newCommand)
            finally:
                ucursor.cursor_stopWait()
            #command will free plant if paste is undone
        elif Target == utimeser.TimeSeriesForm.grid:
            utimeser.TimeSeriesForm.copyPlantToPoint(plant, X, Y)
        elif Target == Sender:
            # get plant being replaced 
            col, row = self.plantsDrawGrid.MouseToCell(X, Y, col, row)
            if not self.inGrid(row, col):
                return
            plantToReplace = self.plantForRowAndColumn(row, col)
            if plantToReplace == None:
                return
            if plantToReplace == plant:
                return
            # make replace command 
            newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(plant, row, col)
            try:
                ucursor.cursor_startWait()
                umain.MainForm.doCommand(newCommand)
            finally:
                ucursor.cursor_stopWait()
    
    def copyPlantToPoint(self, aPlant, x, y):
        col, row = self.plantsDrawGrid.MouseToCell(x, y, col, row)
        plant = self.plantForRowAndColumn(row, col)
        if plant == None:
            return
        newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(aPlant, row, col)
        umain.MainForm.doCommand(newCommand)
    
    # ------------------------------------------------------------- responding to commands 
    def replacePlantInRow(self, oldPlant, newPlant, row):
        generation = self.generationForIndex(row)
        if generation == None:
            raise GeneralException.create("Problem: Invalid row in method TBreederForm.replacePlantInRow.")
        generation.replacePlant(oldPlant, newPlant)
        self.updateForChangeToPlant(newPlant)
    
    def forgetGenerationsListBelowRow(self, aRow):
        while len(self.generations) - 1 > aRow:
            self.forgetLastGeneration()
    
    def addGenerationsFromListBelowRow(self, aRow, aGenerationsList):
        if aRow + 1 <= len(aGenerationsList) - 1:
            for i in range(aRow + 1, len(aGenerationsList)):
                self.addGeneration(aGenerationsList[i])
    
    def addGeneration(self, newGeneration):
        self.generations.Add(newGeneration)
    
    def forgetLastGeneration(self):
        if len(self.generations) <= 0:
            return
        lastGeneration = self.generations[len(self.generations) - 1]
        self.generations.Remove(lastGeneration)
    
    def selectGeneration(self, aGeneration):
        self.selectedRow = self.generations.IndexOf(aGeneration)
        self.ensureRowIsCompletelyVisible(self.selectedRow)
    
    def ensureRowIsCompletelyVisible(self, row):
        if row < 0:
            return
        allocation = self.scrolledWindow.get_allocation()
        adjustment = self.scrolledWindow.get_vadjustment()
        scrollPosition = adjustment.get_value()
        
        rowBounds = self.plantsDrawGrid.boundsForCell(0, row)
           
        # if viewport inside scroll window has a shadow, would neeed a fudge factor
        if rowBounds.top < scrollPosition:
            adjustment.set_value(rowBounds.top)
        elif rowBounds.bottom > allocation.height + scrollPosition:
            newScrollPosition = max(rowBounds.bottom - allocation.height, 0)
            adjustment.set_value(newScrollPosition)

        """
        PDF PORT -- To do with auto scrolling into view?
        lastFullyVisibleRow = self.plantsDrawGrid.TopRow + self.plantsDrawGrid.VisibleRowCount - 1
        if self.selectedRow > lastFullyVisibleRow:
            self.plantsDrawGrid.TopRow = self.plantsDrawGrid.TopRow + (self.selectedRow - lastFullyVisibleRow)
        if self.selectedRow < self.plantsDrawGrid.TopRow:
            self.plantsDrawGrid.TopRow = self.selectedRow
        """
        pass       
        
    def deselectAllGenerations(self):
        self.selectedRow = -1
        for generation in self.generations:
            generation.deselectAllPlants()
    
    def updateForChangeToGenerations(self):
        self.updateMenusForChangeToGenerations()
        self.internalChange = True
        # PDF PORT MAYBE FIX
        """
        if not self.Visible:
            #calls resize
            self.Show()
        self.BringToFront()
        if self.WindowState == delphi_compatability.TWindowState.wsMinimized:
            self.WindowState = delphi_compatability.TWindowState.wsNormal
        self.internalChange = False
        """
        if self.plantsDrawGrid.RowCount < len(self.generations):
            self.plantsDrawGrid.RowCount = len(self.generations)
            self.plantsDrawGrid.updateForChanges()
        self.plantsDrawGrid.Invalidate()
        """
        self.plantsDrawGrid.Update()
        self.redoCaption()
        if len(self.generations) <= 0:
            self.emptyWarningPanel.BringToFront()
        else:
            self.emptyWarningPanel.SendToBack()
        """
    
    def updateForChangeToPlant(self, aPlant):
        genCount = -1
        for generation in self.generations:
            genCount += 1
            plCount = 0
            for plant in generation.plants:
                plCount += 1
                if plant == aPlant:
                    cellRectOver = self.plantsDrawGrid.CellRect(plCount, genCount)
                    self.plantsDrawGridDrawCell(self, plCount, genCount, cellRectOver, [UNRESOLVED.gdFocused, UNRESOLVED.gdSelected, ])
                    return
    
    def updateForChangeToSelections(self, selectionIsInFirstColumn):
        self.updateMenusForChangeToSelection()
        #
        #  if selectedPlants.count > 0 then
        #    for i := 0 to selectedPlants.count - 1 do
        #      begin
        #      plant := PdPlant(selectedPlants.items[i]);
        #      self.updateForChangeToPlant(plant);
        #      end;
        #      
        #if selectionIsInFirstColumn then
        self.plantsDrawGrid.Invalidate()
    
    #
    #procedure TBreederForm.updateForChangeToSelections;
    #  begin
    #  for genCount := 0 to generations.count - 1 do
    #    begin
    #    generation := PdGeneration(generations.items[genCount]);
    #    if generation.plants.count > 0 then for plCount := 0 to generation.plants.count - 1 do
    #      begin
    #      plant := PdPlant(generation.plants.items[plCount]);
    #      if generation.plantWasSelected(plant) then
    #        self.plantsDrawGridDrawCell(self, plCount+1, genCount, plantsDrawGrid.cellRect(plCount+1, genCount), []);
    #      if generation.plantIsSelected(plant) then
    #        self.plantsDrawGridDrawCell(self, plCount+1, genCount, plantsDrawGrid.cellRect(plCount+1, genCount), []);
    #      end;
    #    end;
    #  end;
    #    
    def redoCaption(self):
        if len(self.generations) == 1:
            # new v1.4
            self.Caption = "Breeder (1 generation)"
        else:
            self.Caption = "Breeder (" + IntToStr(len(self.generations)) + " generations)"
        #
        #  self.caption := self.caption + ', numbers ';
        #  case domain.breedingAndTimeSeriesOptions.variationType of
        #    kBreederVariationNoNumeric: self.caption := self.caption + none ;
        #    kBreederVariationLow:     self.caption := self.caption + 'low' ;
        #    kBreederVariationMedium:  self.caption := self.caption + 'medium' ;
        #    kBreederVariationHigh:    self.caption := self.caption + 'high' ;
        #    kBreederVariationCustom:  self.caption := self.caption + 'custom' ;
        #    end;
        #  if domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues then
        #    self.caption := self.caption + ', colors on'
        #  else
        #    self.caption := self.caption + ', colors off'
        #  if domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary then
        #    self.caption := self.caption + ', 3D objects on'
        #  else
        #    self.caption := self.caption + ', 3D objects off'
        #    
    
    def updateMenusForChangeToGenerations(self):
        # PDF PORT FIX LATER!!!
        #print "menu updatign unfinished"
        pass
        """
        havePlants = len(self.generations) > 0
        self.BreederMenuDeleteAll.enabled = havePlants
        self.BreederMenuRandomizeAll.enabled = havePlants
        self.updateMenusForChangeToSelection()
        """
    
    def updateMenusForChangeToSelection(self):
        haveSelection = (self.primarySelectedPlant() != None)
        self.BreederMenuRandomize.enabled = haveSelection
        self.BreederMenuDeleteRow.enabled = haveSelection
        self.BreederPopupMenuDeleteRow.enabled = haveSelection
        self.BreederMenuBreed.enabled = haveSelection
        self.BreederMenuMakeTimeSeries.enabled = haveSelection
        self.BreederMenuCopy.enabled = haveSelection
        self.BreederPopupMenuBreed.enabled = self.BreederMenuBreed.enabled
        self.breedButton.Enabled = self.BreederMenuBreed.enabled
        self.BreederPopupMenuMakeTimeSeries.enabled = self.BreederMenuMakeTimeSeries.enabled
        self.BreederPopupMenuCopy.enabled = self.BreederMenuCopy.enabled
        self.BreederPopupMenuRandomize.enabled = self.BreederMenuRandomize.enabled
        self.updatePasteMenuForClipboardContents()
        # must paste onto a selected plant 
        self.BreederMenuPaste.enabled = self.BreederMenuPaste.enabled and haveSelection
        self.BreederPopupMenuPaste.enabled = self.BreederMenuPaste.enabled
    
    def updatePasteMenuForClipboardContents(self):
        self.BreederMenuPaste.enabled = (self.primarySelectedPlant() != None) and (udomain.domain.plantManager.privatePlantClipboard.Count > 0)
        self.BreederPopupMenuPaste.enabled = self.BreederMenuPaste.enabled
    
    def selectedGeneration(self):
        result = None
        if (self.selectedRow < 0) or (self.selectedRow > len(self.generations) - 1):
            return result
        result = self.generations[self.selectedRow]
        return result
    
    def primarySelectedPlant(self):
        result = None
        generation = self.selectedGeneration()
        if generation == None:
            return result
        result = generation.firstSelectedPlant()
        return result
    
    def plantAtMouse(self, x, y):
        result = None
        col, row = self.plantsDrawGrid.MouseToCell(x, y)
        if not self.inGrid(row, col):
            return result
        result = self.plantForRowAndColumn(row, col)
        return result
    
    # ----------------------------------------------------------------------------- menu 
    def BreederMenuUndoClick(self, Sender):
        umain.MainForm.MenuEditUndoClick(Sender)
    
    def BreederMenuRedoClick(self, Sender):
        umain.MainForm.MenuEditRedoClick(Sender)
    
    def BreederMenuCopyClick(self, Sender):
        plant = self.primarySelectedPlant()
        if plant == None:
            return
        copyList = delphi_compatability.TList()
        copyList.Add(plant)
        # temporarily change plant name to make copy, then put back 
        saveName = plant.getName()
        self.numBreederPlantsCopiedThisSession += 1
        plant.setName("Breeder plant " + IntToStr(self.numBreederPlantsCopiedThisSession))
        udomain.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(copyList)
        plant.setName(saveName)
        #sets our paste menu also
        umain.MainForm.updatePasteMenuForClipboardContents()
    
    def BreederMenuSendCopyToMainWindowClick(self, Sender):
        self.BreederMenuCopyClick(self)
        umain.MainForm.MenuEditPasteClick(umain.MainForm)
    
    def BreederMenuUndoRedoListClick(self, Sender):
        umain.MainForm.UndoMenuEditUndoRedoListClick(umain.MainForm)
    
    def BreederMenuPasteClick(self, Sender):
        if udomain.domain.plantManager.privatePlantClipboard.Count <= 0:
            return
        generation = self.selectedGeneration()
        if generation == None:
            return
        plant = generation.firstSelectedPlant()
        if plant == None:
            return
        column = generation.plants.IndexOf(plant) + 1
        newPlant = uplant.PdPlant().create()
        udomain.domain.plantManager.pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant)
        newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(newPlant, self.selectedRow, column)
        umain.MainForm.doCommand(newCommand)
        #command will free plant if paste is undone
    
    def BreederMenuBreedClick(self, Sender):
        if (self.selectedRow < 0) or (self.selectedRow > len(self.generations) - 1):
            return
        if self.selectedRow >= udomain.domain.breedingAndTimeSeriesOptions.maxGenerations - 1:
            # check if there is room in the breeder - this command will make one new generation 
            self.fullWarning()
            return
        generationToBreed = self.generations[self.selectedRow]
        if len(generationToBreed.selectedPlants) <= 0:
            return
        newCommand = updcom.PdBreedFromParentsCommand().createWithInfo(self.generations, generationToBreed.firstSelectedPlant(), generationToBreed.secondSelectedPlant(), self.selectedRow, udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, updcom.kDontCreateFirstGeneration)
        generationToBreed.firstParent = generationToBreed.firstSelectedPlant()
        generationToBreed.secondParent = generationToBreed.secondSelectedPlant()
        # PDF PORT FIX LATER __ FOR TESTING
        #umain.MainForm.doCommand(newCommand)
        #newCommand.doCommand()
        Cursor_StartWait()
        gobject.idle_add(newCommand.doCommand)
        gobject.idle_add(Cursor_StopWait)
    
    def BreederMenuMakeTimeSeriesClick(self, Sender):
        if self.primarySelectedPlant() == None:
            return
        newCommand = updcom.PdMakeTimeSeriesCommand().createWithNewPlant(self.primarySelectedPlant())
        umain.MainForm.doCommand(newCommand)
    
    def fullWarning(self):
        MessageDialog("The breeder is full. " + chr(13) + chr(13) + "You must delete some rows" + chr(13) + "(or increase the number of rows allowed in the breeder options) " + chr(13) + "before you can breed more plants.", mtWarning, [mbOK, ], 0)
    
    def BreederMenuDeleteRowClick(self, Sender):
        if self.selectedGeneration() == None:
            return
        newCommand = updcom.PdDeleteBreederGenerationCommand().createWithGeneration(self.selectedGeneration())
        umain.MainForm.doCommand(newCommand)
    
    def BreederMenuDeleteAllClick(self, Sender):
        if len(self.generations) <= 0:
            return
        newCommand = updcom.PdDeleteAllBreederGenerationsCommand().create()
        umain.MainForm.doCommand(newCommand)
    
    def BreederMenuRandomizeClick(self, Sender):
        aGeneration = self.selectedGeneration()
        if aGeneration == None:
            return
        if len(aGeneration.selectedPlants) <= 0:
            return
        randomizeList = delphi_compatability.TList()
        try:
            ucursor.cursor_startWait()
            for plant in aGeneration.selectedPlants:
                randomizeList.Add(plant)
            newCommand = updcom.PdRandomizeCommand().createWithListOfPlants(randomizeList)
            newCommand.isInBreeder = True
            umain.MainForm.doCommand(newCommand)
        finally:
            #command has another list, so we must free this one
            ucursor.cursor_stopWait()
    
    def BreederMenuRandomizeAllClick(self, Sender):
        if len(self.generations) <= 0:
            return
        randomizeList = None
        try:
            ucursor.cursor_startWait()
            randomizeList = delphi_compatability.TList()
            for generation in self.generations:
                for plant in generation.plants:
                    randomizeList.Add(plant)
            newCommand = updcom.PdRandomizeCommand().createWithListOfPlants(randomizeList)
            newCommand.isInBreeder = True
            newCommand.isRandomizeAllInBreeder = True
            umain.MainForm.doCommand(newCommand)
        finally:
            randomizeList.free
            ucursor.cursor_stopWait()
    
    def BreederMenuVariationNoneClick(self, Sender):
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationNoNumeric
        self.BreederMenuVariationNone.checked = True
        self.redoCaption()
    
    def BreederMenuVariationLowClick(self, Sender):
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationLow
        self.BreederMenuVariationLow.checked = True
        self.redoCaption()
    
    def BreederMenuVariationMediumClick(self, Sender):
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationMedium
        self.BreederMenuVariationMedium.checked = True
        self.redoCaption()
    
    def BreederMenuVariationHighClick(self, Sender):
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationHigh
        # this is to deal with if it was turned off by not having a library
        # v2.0 removed - this is separate now
        # domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary := True;
        self.BreederMenuVariationHigh.checked = True
        self.redoCaption()
    
    def BreederMenuVariationCustomClick(self, Sender):
        self.changeBreederAndTimeSeriesOptions(kOptionTabMutation)
    
    def BreederMenuOtherOptionsClick(self, Sender):
        self.changeBreederAndTimeSeriesOptions(kOptionTabSize)
    
    def BreederMenuVaryColorsClick(self, Sender):
        self.BreederMenuVaryColors.checked = not self.BreederMenuVaryColors.checked
        options = udomain.domain.breedingAndTimeSeriesOptions
        options.mutateAndBlendColorValues = self.BreederMenuVaryColors.checked
        newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(options, udomain.domain.options)
        umain.MainForm.doCommand(newCommand)
    
    def BreederMenuVary3DObjectsClick(self, Sender):
        self.BreederMenuVary3DObjects.checked = not self.BreederMenuVary3DObjects.checked
        options = udomain.domain.breedingAndTimeSeriesOptions
        options.chooseTdosRandomlyFromCurrentLibrary = self.BreederMenuVary3DObjects.checked
        newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(options, udomain.domain.options)
        umain.MainForm.doCommand(newCommand)
    
    def changeBreederAndTimeSeriesOptions(self, tabIndexToShow):
        if tabIndexToShow == kOptionTabMutation:
            udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationCustom
            self.BreederMenuVariationCustom.checked = True
            self.redoCaption()
        optionsForm = ubrdopt.TBreedingOptionsForm(self)
        if optionsForm == None:
            raise GeneralException.create("Problem: Could not create breeding options window.")
        try:
            optionsForm.breedingOptions.pageIndex = tabIndexToShow
            optionsForm.initializeWithBreedingAndTimeSeriesOptionsAndDomainOptions(udomain.domain.breedingAndTimeSeriesOptions, udomain.domain.options)
            response = optionsForm.ShowModal()
            if response == mrOK:
                newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(optionsForm.options, optionsForm.domainOptions)
                umain.MainForm.doCommand(newCommand)
        finally:
            optionsForm.free
            optionsForm = None
    
    def variationLowClick(self, Sender):
        self.BreederMenuVariationLowClick(self)
    
    def variationNoneNumericClick(self, Sender):
        self.BreederMenuVariationNoneClick(self)
    
    def variationMediumClick(self, Sender):
        self.BreederMenuVariationMediumClick(self)
    
    def variationHighClick(self, Sender):
        self.BreederMenuVariationHighClick(self)
    
    def variationCustomClick(self, Sender):
        self.BreederMenuVariationCustomClick(self)
    
    def varyColorsClick(self, Sender):
        self.BreederMenuVaryColorsClick(self)
    
    def vary3DObjectsClick(self, Sender):
        self.BreederMenuVary3DObjectsClick(self)
    
    def BreederPopupMenuRandomizeClick(self, Sender):
        self.BreederMenuRandomizeClick(self)
    
    def BreederPopupMenuBreedClick(self, Sender):
        self.BreederMenuBreedClick(self)
    
    def breedButtonClick(self, Sender):
        self.BreederMenuBreedClick(self)
    
    def BreederPopupMenuMakeTimeSeriesClick(self, Sender):
        self.BreederMenuMakeTimeSeriesClick(self)
    
    def BreederPopupMenuCopyClick(self, Sender):
        self.BreederMenuCopyClick(self)
    
    def BreederPopupMenuPasteClick(self, Sender):
        self.BreederMenuPasteClick(self)
    
    def BreederPopupMenuSendCopytoMainWindowClick(self, Sender):
        self.BreederMenuSendCopyToMainWindowClick(self)
    
    def BreederPopupMenuDeleteRowClick(self, Sender):
        self.BreederMenuDeleteRowClick(self)
    
    # --------------------------------------------------------------------------- utilities 
    def inGrid(self, row, column):
        result = True
        if (row < 0) or (row > len(self.generations) - 1):
            result = False
        if (column < 1) or (column - 1 > self.plantsDrawGrid.ColCount - 1):
            result = False
        return result
    
    def generationForIndex(self, index):
        result = None
        if index < 0:
            return result
        if index > len(self.generations) - 1:
            return result
        if self.generations[index] == None:
            return result
        result = self.generations[index]
        return result
    
    def plantForRowAndColumn(self, row, column):
        result = None
        generation = self.generationForIndex(row)
        if generation == None:
            return result
        result = generation.plantForIndex(column - 1)
        return result
    
    # ---------------------------------------------------------------------------- resizing 
    def FormResize(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        if self.generations == None:
            return
        self.breederToolbarPanel.SetBounds(0, 0, self.ClientWidth, self.breederToolbarPanel.Height)
        self.helpButton.SetBounds(self.breederToolbarPanel.Width - self.helpButton.Width - 4, self.helpButton.Top, self.helpButton.Width, self.helpButton.Height)
        self.plantsDrawGrid.SetBounds(0, self.breederToolbarPanel.Height, self.ClientWidth, self.ClientHeight - self.breederToolbarPanel.Height)
        self.emptyWarningPanel.SetBounds(self.ClientWidth / 2 - self.emptyWarningPanel.Width / 2, self.ClientHeight / 2 - self.emptyWarningPanel.Height / 2, self.emptyWarningPanel.Width, self.emptyWarningPanel.Height)
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 250
        UNRESOLVED.ptMinTrackSize.y = 150
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Breeding_plants_using_the_breeder")
    
    # ----------------------------------------------------------------------------- *palette stuff 
    def GetPalette(self):
        result = umain.MainForm.paletteImage.Picture.Bitmap.Palette
        return result
    
    def PaletteChanged(self, Foreground):
        palette = self.GetPalette()
        if palette != 0:
            DC = self.GetDeviceContext(windowHandle)
            oldPalette = UNRESOLVED.selectPalette(DC, palette, not Foreground)
            if (UNRESOLVED.realizePalette(DC) != 0) and (not delphi_compatability.Application.terminated) and (self.plantsDrawGrid != None):
                # if palette changed, repaint drawing 
                self.plantsDrawGrid.Invalidate()
            UNRESOLVED.selectPalette(DC, oldPalette, True)
            UNRESOLVED.realizePalette(DC)
            UNRESOLVED.releaseDC(windowHandle, DC)
        result = PdForm.PaletteChanged(self, Foreground)
        return result
    
    def BreederMenuHelpOnBreedingClick(self, Sender):
        delphi_compatability.Application.HelpJump("Breeding_plants_using_the_breeder")
    
    def BreederMenuHelpTopicsClick(self, Sender):
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_FINDER, 0)
    
    def BreederMenuOptionsFastDrawClick(self, Sender):
        umain.MainForm.MenuOptionsFastDrawClick(umain.MainForm)
    
    def BreederMenuOptionsMediumDrawClick(self, Sender):
        umain.MainForm.MenuOptionsMediumDrawClick(umain.MainForm)
    
    def BreederMenuOptionsBestDrawClick(self, Sender):
        umain.MainForm.MenuOptionsBestDrawClick(umain.MainForm)
    
    def BreederMenuOptionsCustomDrawClick(self, Sender):
        umain.MainForm.MenuOptionsCustomDrawClick(umain.MainForm)
  
# refernced by commands
BreederForm = None

def main(): 
    global BreederForm           
    BreederForm = TBreederForm()
    gtk.main()
    
if __name__ == "__main__":
    main()
      
