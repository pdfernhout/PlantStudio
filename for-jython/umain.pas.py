# unit Umain

from conversion_common import *
import ubmpsupport
import uundo
import uamendmt
import uoptions3dexport
import unoted
import ucustdrw
import uregister
import uabout
import uanimate
import unozzle
import uwelcome
import utdomove
import ubmpopt
import udebug
import uwizard
import utimeser
import uturtle
import umover
import uwait
import ubreedr
import upp_hed
import upp_tdo
import upp_scv
import upp_rea
import upp_lis
import upp_int
import upp_col
import upp_boo
import uplantmn
import uparams
import usplash
import umath
import updcom
import uoptions
import ucursor
import ubitmap
import u3dexport
import usupport
import udomain
import uwinsliders
import usection
import ustats
import uppanel
import ucollect
import usliders
import uplant
import ucommand
import updform
import delphi_compatability

# const
kCursorModeSelectDrag = 0
kCursorModeMagnify = 1
kCursorModeScroll = 2
kCursorModeRotate = 3
kCursorModePosingSelect = 4
kMinWidthOnScreen = 100
kMinHeightOnScreen = 100
kDrawNow = true
kDontDrawYet = false
kScaleAndMove = true
kJustMove = false
kAlwaysMove = true
kOnlyMoveIfOffTheScreen = false

# var
plantFileChanged = false

# var
MainForm = TMainForm()

# const
kBetweenGap = 4
kSplitterDragToTopMinPixels = 100
kSplitterDragToBottomMinPixelsInHorizMode = 160
kSplitterDragToBottomMinPixelsInVertMode = 60
kSplitterDragToLeftMinPixels = 100
kSplitterDragToRightMinPixels = 260
kPlantListChanged = true
kPlantListNotChanged = false
kHintRange = 1
kMaxHintRangeForLargeAreas = 50
kTabRotations = 0
kTabParameters = 1
kTabLifeCycle = 2
kTabPosing = 3
kTabStatistics = 4
kTabNote = 5
kTabHighest = 5
kMaxMagnificationToTypeIn = 10000
kEnableAllForms = true
kDisableAllForms = false
kDrawAllPlants = true
kDrawOnlySelectedPlants = false
kExpand = 0
kCollapse = 1
kExpandOrCollapse = 2

# var
pictureFileSaveAttemptsThisSession = 0
nozzleFileSaveAttemptsThisSession = 0
exportTo3DFileSaveAttemptsThisSession = [0] * (range(1, u3dexport.k3DExportTypeLast + 1) + 1)

def setPlantCharacteristicsForAnimationFrame(plant, frame):
    if plant == None:
        return
    if udomain.domain.animationOptions.animateBy == udomain.kAnimateByAge:
        if frame <= 0:
            plant.setAge(1)
        elif frame >= udomain.domain.animationOptions.frameCount - 1:
            plant.setAge(plant.pGeneral.ageAtMaturity)
        else:
            plant.setAge(udomain.domain.animationOptions.ageIncrement * frame)
    elif udomain.domain.animationOptions.animateBy == udomain.kAnimateByXRotation:
        if udomain.domain.animationOptions.frameCount > 1:
            plant.xRotation = udomain.domain.animationOptions.xRotationIncrement * frame

# const
kProgressBarColor = delphi_compatability.clBlue

# const
kScaleToFitMargin = 10
kOffscreenMargin = 20

# const
kSelectNoPosedPartString = "< Select None >"

# const
kNoPartSelected = "Selected part: (none)"

def enableOrDisableSet(aLabel, anEdit, aSpin, anExtraLabel, enable):
    if aLabel != None:
        aLabel.Enabled = enable
    if anEdit != None:
        anEdit.Enabled = enable
    if aSpin != None:
        aSpin.Visible = enable
    if anExtraLabel != None:
        anExtraLabel.Enabled = enable

class TMainForm(PdForm):
    def __init__(self):
        self.MainMenu = TMainMenu()
        self.MenuFile = TMenuItem()
        self.MenuFileNew = TMenuItem()
        self.MenuFileOpen = TMenuItem()
        self.MenuFileClose = TMenuItem()
        self.N1 = TMenuItem()
        self.MenuFileSave = TMenuItem()
        self.MenuFileSaveAs = TMenuItem()
        self.N2 = TMenuItem()
        self.MenuFileExit = TMenuItem()
        self.MenuEdit = TMenuItem()
        self.MenuEditUndo = TMenuItem()
        self.MenuEditRedo = TMenuItem()
        self.N3 = TMenuItem()
        self.MenuEditCut = TMenuItem()
        self.MenuEditCopy = TMenuItem()
        self.MenuEditPaste = TMenuItem()
        self.MenuHelp = TMenuItem()
        self.MenuHelpTopics = TMenuItem()
        self.MenuHelpAbout = TMenuItem()
        self.MenuPlant = TMenuItem()
        self.MenuFilePlantMover = TMenuItem()
        self.MenuPlantRename = TMenuItem()
        self.MenuPlantBreed = TMenuItem()
        self.MenuPlantRandomize = TMenuItem()
        self.MenuPlantNew = TMenuItem()
        self.N7 = TMenuItem()
        self.toolbarPanel = TPanel()
        self.dragCursorMode = TSpeedButton()
        self.magnifyCursorMode = TSpeedButton()
        self.scrollCursorMode = TSpeedButton()
        self.horizontalSplitter = TPanel()
        self.verticalSplitter = TPanel()
        self.paletteImage = TImage()
        self.MenuEditPreferences = TMenuItem()
        self.visibleBitmap = TImage()
        self.PlantPopupMenu = TPopupMenu()
        self.MenuFileSaveDrawingAs = TMenuItem()
        self.MenuFilePrintDrawing = TMenuItem()
        self.MenuEditCopyDrawing = TMenuItem()
        self.PopupMenuCut = TMenuItem()
        self.PopupMenuCopy = TMenuItem()
        self.PopupMenuPaste = TMenuItem()
        self.N6 = TMenuItem()
        self.MenuEditDelete = TMenuItem()
        self.N5 = TMenuItem()
        self.PrintDialog = TPrintDialog()
        self.sectionImagesPanel = TPanel()
        self.Sections_FlowersPrimary = TImage()
        self.Sections_General = TImage()
        self.Sections_InflorPrimary = TImage()
        self.Sections_Meristems = TImage()
        self.Sections_Leaves = TImage()
        self.Sections_RootTop = TImage()
        self.Sections_Fruit = TImage()
        self.Sections_InflorSecondary = TImage()
        self.Sections_Internodes = TImage()
        self.Sections_SeedlingLeaves = TImage()
        self.Sections_FlowersSecondary = TImage()
        self.PopupMenuRename = TMenuItem()
        self.PopupMenuRandomize = TMenuItem()
        self.PopupMenuBreed = TMenuItem()
        self.rotateCursorMode = TSpeedButton()
        self.MenuPlantExportToDXF = TMenuItem()
        self.MenuPlantMakeTimeSeries = TMenuItem()
        self.MenuWindow = TMenuItem()
        self.MenuWindowBreeder = TMenuItem()
        self.MenuWindowTimeSeries = TMenuItem()
        self.N12 = TMenuItem()
        self.MenuWindowNumericalExceptions = TMenuItem()
        self.animateTimer = TTimer()
        self.MenuPlantAnimate = TMenuItem()
        self.centerDrawing = TSpeedButton()
        self.MenuOptions = TMenuItem()
        self.MenuOptionsShowLongButtonHints = TMenuItem()
        self.MenuOptionsShowParameterHints = TMenuItem()
        self.MenuOptionsShowSelectionRectangles = TMenuItem()
        self.paramPanelOpenArrowImage = TImage()
        self.paramPanelClosedArrowImage = TImage()
        self.plantListPanel = TPanel()
        self.progressPaintBox = TPaintBox()
        self.plantFocusPanel = TPanel()
        self.lifeCyclePanel = TPanel()
        self.lifeCycleGraphImage = TImage()
        self.timeLabel = TLabel()
        self.selectedPlantNameLabel = TLabel()
        self.lifeCycleEditPanel = TPanel()
        self.daysAndSizeLabel = TLabel()
        self.ageAndSizeLabel = TLabel()
        self.lifeCycleDaysEdit = TEdit()
        self.lifeCycleDaysSpin = TSpinButton()
        self.lifeCycleDragger = TPanel()
        self.statsScrollBox = TScrollBox()
        self.tabSet = TTabSet()
        self.parametersPanel = TPanel()
        self.parametersScrollBox = TScrollBox()
        self.PopupMenuMakeTimeSeries = TMenuItem()
        self.PopupMenuAnimate = TMenuItem()
        self.MenuLayout = TMenuItem()
        self.MenuLayoutSelectAll = TMenuItem()
        self.MenuLayoutDeselect = TMenuItem()
        self.MenuLayoutHide = TMenuItem()
        self.MenuLayoutHideOthers = TMenuItem()
        self.MenuLayoutShow = TMenuItem()
        self.N18 = TMenuItem()
        self.MenuLayoutBringForward = TMenuItem()
        self.MenuLayoutSendBack = TMenuItem()
        self.N19 = TMenuItem()
        self.MenuLayoutHorizontalOrientation = TMenuItem()
        self.MenuLayoutVerticalOrientation = TMenuItem()
        self.MenuLayoutScaleToFit = TMenuItem()
        self.MenuLayoutViewOnePlantAtATime = TMenuItem()
        self.MenuLayoutMakeBouquet = TMenuItem()
        self.maxSizeAxisLabel = TLabel()
        self.plantFileChangedImage = TImage()
        self.fileChangedImage = TImage()
        self.fileNotChangedImage = TImage()
        self.plantListDrawGrid = TDrawGrid()
        self.MenuEditDuplicate = TMenuItem()
        self.N8 = TMenuItem()
        self.MenuPlantNewUsingLastWizardSettings = TMenuItem()
        self.N4 = TMenuItem()
        self.paramPopupMenu = TPopupMenu()
        self.paramPopupMenuHelp = TMenuItem()
        self.N15 = TMenuItem()
        self.paramPopupMenuExpand = TMenuItem()
        self.paramPopupMenuCollapse = TMenuItem()
        self.AfterRegisterMenuSeparator = TMenuItem()
        self.MenuFileTdoMover = TMenuItem()
        self.animateGrowth = TSpeedButton()
        self.MenuFileMakePainterNozzle = TMenuItem()
        self.unregisteredExportReminder = TImage()
        self.MenuFileMakePainterAnimation = TMenuItem()
        self.N17 = TMenuItem()
        self.N13 = TMenuItem()
        self.MenuHelpRegister = TMenuItem()
        self.MenuHelpSuperSpeedTour = TMenuItem()
        self.MenuHelpTutorial = TMenuItem()
        self.MenuEditCopyAsText = TMenuItem()
        self.plantsAsTextMemo = TMemo()
        self.MenuEditPasteAsText = TMenuItem()
        self.N16 = TMenuItem()
        self.MenuOptionsFastDraw = TMenuItem()
        self.MenuOptionsMediumDraw = TMenuItem()
        self.MenuOptionsBestDraw = TMenuItem()
        self.MenuOptionsCustomDraw = TMenuItem()
        self.MenuOptionsUsePlantBitmaps = TMenuItem()
        self.plantBitmapsIndicatorImage = TImage()
        self.plantBitmapsGreenImage = TImage()
        self.noPlantBitmapsImage = TImage()
        self.plantBitmapsYellowImage = TImage()
        self.plantBitmapsRedImage = TImage()
        self.animatingLabel = TLabel()
        self.N22 = TMenuItem()
        self.MenuPlantZeroRotations = TMenuItem()
        self.PopupMenuZeroRotations = TMenuItem()
        self.rotationsPanel = TPanel()
        self.xRotationLabel = TLabel()
        self.xRotationEdit = TEdit()
        self.xRotationSpin = TSpinButton()
        self.yRotationLabel = TLabel()
        self.yRotationEdit = TEdit()
        self.yRotationSpin = TSpinButton()
        self.zRotationLabel = TLabel()
        self.zRotationEdit = TEdit()
        self.zRotationSpin = TSpinButton()
        self.resetRotations = TSpeedButton()
        self.rotationLabel = TLabel()
        self.magnificationPercent = TComboBox()
        self.N10 = TMenuItem()
        self.Reconcile3DObjects1 = TMenuItem()
        self.notePanel = TPanel()
        self.noteMemo = TMemo()
        self.noteLabel = TLabel()
        self.noteEdit = TSpeedButton()
        self.PopupMenuEditNote = TMenuItem()
        self.MenuPlantEditNote = TMenuItem()
        self.N25 = TMenuItem()
        self.paramPopupMenuCopyName = TMenuItem()
        self.MenuPlantExportToPOV = TMenuItem()
        self.MenuFileExport = TMenuItem()
        self.Recent0 = TMenuItem()
        self.Recent1 = TMenuItem()
        self.Recent2 = TMenuItem()
        self.Recent3 = TMenuItem()
        self.Recent4 = TMenuItem()
        self.MenuFileReopen = TMenuItem()
        self.Recent5 = TMenuItem()
        self.Recent6 = TMenuItem()
        self.Recent7 = TMenuItem()
        self.Recent8 = TMenuItem()
        self.Recent9 = TMenuItem()
        self.viewFreeFloating = TSpeedButton()
        self.viewOneOnly = TSpeedButton()
        self.MenuOptionsDrawAs = TMenuItem()
        self.drawingAreaOnTop = TSpeedButton()
        self.drawingAreaOnSide = TSpeedButton()
        self.MenuLayoutDrawingAreaOn = TMenuItem()
        self.MenuLayoutView = TMenuItem()
        self.MenuLayoutViewFreeFloating = TMenuItem()
        self.Sections_FlowersPrimaryAdvanced = TImage()
        self.sizingLabel = TLabel()
        self.drawingScaleEdit = TEdit()
        self.drawingScaleSpin = TSpinButton()
        self.drawingScalePixelsPerMmLabel = TLabel()
        self.packPlants = TSpeedButton()
        self.locationLabel = TLabel()
        self.xLocationLabel = TLabel()
        self.xLocationEdit = TEdit()
        self.xLocationSpin = TSpinButton()
        self.yLocationLabel = TLabel()
        self.yLocationEdit = TEdit()
        self.yLocationSpin = TSpinButton()
        self.locationPixelsLabel = TLabel()
        self.arrangementPlantName = TLabel()
        self.alignTops = TSpeedButton()
        self.alignBottoms = TSpeedButton()
        self.alignLeft = TSpeedButton()
        self.alignRight = TSpeedButton()
        self.makeEqualWidth = TSpeedButton()
        self.makeEqualHeight = TSpeedButton()
        self.MenuLayoutAlign = TMenuItem()
        self.MenuLayoutAlignTops = TMenuItem()
        self.MenuLayoutAlignBottoms = TMenuItem()
        self.MenuLayoutAlignLeftSides = TMenuItem()
        self.MenuLayoutAlignRightSides = TMenuItem()
        self.MenuLayoutSize = TMenuItem()
        self.MenuLayoutSizeSameHeight = TMenuItem()
        self.MenuLayoutSizeSameWidth = TMenuItem()
        self.MenuLayoutPack = TMenuItem()
        self.parametersPlantName = TLabel()
        self.MenuPlantExportTo3DS = TMenuItem()
        self.N9 = TMenuItem()
        self.posingPanel = TPanel()
        self.posingPlantName = TLabel()
        self.MenuOptionsGhostHiddenParts = TMenuItem()
        self.posingDetailsPanel = TPanel()
        self.posingXRotationLabel = TLabel()
        self.posingYRotationLabel = TLabel()
        self.posingZRotationLabel = TLabel()
        self.posingScaleMultiplierPercent = TLabel()
        self.posingHidePart = TCheckBox()
        self.posingXRotationEdit = TEdit()
        self.posingXRotationSpin = TSpinButton()
        self.posingYRotationEdit = TEdit()
        self.posingYRotationSpin = TSpinButton()
        self.posingZRotationEdit = TEdit()
        self.posingZRotationSpin = TSpinButton()
        self.posingAddExtraRotation = TCheckBox()
        self.posingMultiplyScale = TCheckBox()
        self.MenuOptionsHighlightPosedParts = TMenuItem()
        self.MenuOptionsPosing = TMenuItem()
        self.N20 = TMenuItem()
        self.N21 = TMenuItem()
        self.MenuFileMove = TMenuItem()
        self.posingScaleMultiplierLabel = TLabel()
        self.posingLengthMultiplierPercent = TLabel()
        self.posingLengthMultiplierLabel = TLabel()
        self.posingWidthMultiplierPercent = TLabel()
        self.posingWidthMultiplierLabel = TLabel()
        self.posingMultiplyScaleAllPartsAfter = TCheckBox()
        self.MenuOptionsShowBoundsRectangles = TMenuItem()
        self.MenuOptionsDrawRectangles = TMenuItem()
        self.MenuOptionsHints = TMenuItem()
        self.MenuFileSaveJPEG = TMenuItem()
        self.posingScaleMultiplierEdit = TEdit()
        self.posingScaleMultiplierSpin = TSpinButton()
        self.posingLengthMultiplierEdit = TEdit()
        self.posingLengthMultiplierSpin = TSpinButton()
        self.posingWidthMultiplierEdit = TEdit()
        self.posingWidthMultiplierSpin = TSpinButton()
        self.MenuOptionsHidePosing = TMenuItem()
        self.UndoMenuEditUndoRedoList = TMenuItem()
        self.MenuPlantExportToOBJ = TMenuItem()
        self.MenuPlantExportToVRML = TMenuItem()
        self.MenuPlantExportToLWO = TMenuItem()
        self.sectionsComboBox = TComboBox()
        self.paramPopupMenuExpandAllInSection = TMenuItem()
        self.paramPopupMenuCollapseAllInSection = TMenuItem()
        self.N11 = TMenuItem()
        self.hideExtraLabel = TLabel()
        self.rotationDegreesLabel = TLabel()
        self.posingColorsPanel = TPanel()
        self.posingLineColorLabel = TLabel()
        self.posingFrontfaceColorLabel = TLabel()
        self.posingBackfaceColorLabel = TLabel()
        self.posingChangeColors = TCheckBox()
        self.posingChangeAllColorsAfter = TCheckBox()
        self.posingLineColor = TPanel()
        self.posingFrontfaceColor = TPanel()
        self.posingBackfaceColor = TPanel()
        self.posingSelectionCursorMode = TSpeedButton()
        self.posedPartsLabel = TLabel()
        self.posedPlantParts = TComboBox()
        self.posingHighlight = TSpeedButton()
        self.posingGhost = TSpeedButton()
        self.posingNotShown = TSpeedButton()
        self.selectedPartLabel = TLabel()
        self.posingPosePart = TSpeedButton()
        self.posingUnposePart = TSpeedButton()
        self.posingMultiplyScaleAllPartsAfterLabel = TLabel()
        self.sectionPopupMenuHelp = TMenuItem()
        self.Sections_Orthogonal = TImage()
        self.drawingBitmap = TBitmap()
        self.commandList = PdCommandList()
        self.drawingPaintBox = PdPaintBoxWithPalette()
        self.statsPanel = PdStatsPanel()
        self.invalidDrawingRect = TRect()
        self.internalChange = false
        self.inFormCreation = false
        self.inFileOpen = false
        self.lastSaveProceeded = false
        self.resizingAtStart = false
        self.plants = TListCollection()
        self.selectedPlants = TList()
        self.numPlantsInClipboard = 0
        self.lastSingleClickPlantIndex = 0
        self.justDoubleClickedOnDrawGrid = false
        self.rubberBanding = false
        self.rubberBandNeedToRedraw = false
        self.rubberBandStartDragPoint = TPoint()
        self.rubberBandLastDrawPoint = TPoint()
        self.drawing = false
        self.animateCommand = PdCommand()
        self.drawProgressMax = 0L
        self.cursorModeForDrawing = 0
        self.actionInProgress = false
        self.mouseMoveActionInProgress = false
        self.lifeCycleDragging = false
        self.lifeCycleDraggingNeedToRedraw = false
        self.lifeCycleDraggingStartPos = 0
        self.lifeCycleDraggingLastDrawPos = 0
        self.cursorPosInDrawingPaintBox = TPoint()
        self.horizontalSplitterDragging = false
        self.verticalSplitterDragging = false
        self.horizontalSplitterNeedToRedraw = false
        self.verticalSplitterNeedToRedraw = false
        self.horizontalSplitterStartPos = 0
        self.verticalSplitterStartPos = 0
        self.horizontalSplitterLastDrawPos = 0
        self.verticalSplitterLastDrawPos = 0
        self.lastWidth = 0
        self.lastHeight = 0
        self.hintX = 0
        self.hintY = 0
        self.hintActive = false
        self.lastHintString = ""
        self.backTabbingInParametersPanel = false
        self.selectedParameterPanel = PdParameterPanel()
        self.selectedPlantPartID = 0L
        self.mouseDownSelectedPlantPartID = 0L
        self.selectedPlantPartType = ""
        self.mouseDownSelectedPlantPartType = ""
    
    #$R *.DFM
    #in each direction, so box is 100 x 100
    def FormCreate(self, Sender):
        tempBoundsRect = TRect()
        
        ucursor.cursor_startWait()
        try:
            delphi_compatability.Application.helpFile = ExtractFilePath(delphi_compatability.Application.exeName) + "PlantStudio.hlp"
            delphi_compatability.Application.OnActivate = self.FormActivate
            if udomain.domain == None:
                raise GeneralException.create("Problem: Nil domain in method TMainForm.FormCreate.")
            # domain must exist when this is created; use this pointer to shorten code
            self.plants = udomain.domain.plantManager.plants
            self.updateForRegistrationChange()
            # turn off panel bevels 
            self.plantListPanel.BevelOuter = UNRESOLVED.bvNone
            self.plantFocusPanel.BevelOuter = UNRESOLVED.bvNone
            self.plantListDrawGrid.DragCursor = ucursor.crDragPlant
            # save height and width for resizing use 
            self.lastWidth = self.ClientWidth
            self.lastHeight = self.ClientHeight
            self.inFormCreation = true
            # application options 
            delphi_compatability.Application.OnShowHint = self.DoShowHint
            # cfk played with menu hints - to use menu hints, respond to this and display the hint in a window or status panel
            # Application.OnHint := DoMenuHint;    
            delphi_compatability.Application.ShowHint = true
            # creation of dependent objects and setting them up 
            self.selectedPlants = delphi_compatability.TList().Create()
            self.commandList = ucommand.PdCommandList().create()
            self.commandList.setNewUndoLimit(udomain.domain.options.undoLimit)
            self.commandList.setNewObjectUndoLimit(udomain.domain.options.undoLimitOfPlants)
            self.drawingPaintBox = ubitmap.PdPaintBoxWithPalette().Create(self)
            self.drawingPaintBox.Parent = self
            self.drawingPaintBox.OnPaint = self.drawingPaintBoxPaint
            self.drawingPaintBox.OnMouseDown = self.PaintBoxMouseDown
            self.drawingPaintBox.OnMouseMove = self.PaintBoxMouseMove
            self.drawingPaintBox.OnMouseUp = self.PaintBoxMouseUp
            self.drawingPaintBox.OnEndDrag = self.PaintBoxEndDrag
            self.drawingPaintBox.OnDragOver = self.PaintBoxDragOver
            self.drawingPaintBox.DragCursor = ucursor.crDragPlant
            self.drawingPaintBox.PopupMenu = self.PlantPopupMenu
            self.drawingBitmap = delphi_compatability.TBitmap().Create()
            self.statsPanel = ustats.PdStatsPanel().create(self)
            self.statsPanel.Parent = self.statsScrollBox
            self.statsPanel.ParentFont = false
            # hints 
            self.hintActive = false
            self.lastHintString = ""
            # intial settings of stored info 
            self.tabSet.tabIndex = kTabRotations
            self.dragCursorMode.Down = true
            # loading info 
            self.loadSectionsIntoListBox()
            if udomain.domain.options.drawSpeed == udomain.kDrawFast:
                # updating 
                self.MenuOptionsFastDraw.checked = true
            elif udomain.domain.options.drawSpeed == udomain.kDrawMedium:
                self.MenuOptionsMediumDraw.checked = true
            elif udomain.domain.options.drawSpeed == udomain.kDrawBest:
                self.MenuOptionsBestDraw.checked = true
            elif udomain.domain.options.drawSpeed == udomain.kDrawCustom:
                self.MenuOptionsCustomDraw.checked = true
            self.updateMenusForUndoRedo()
            self.updatePasteMenuForClipboardContents()
            if self.sectionsComboBox.Items.Count > 0:
                self.sectionsComboBox.ItemIndex = 0
                self.updateParameterPanelsForSectionChange()
            #v2.0
            self.rotationsPanel.Visible = true
            ubmpsupport.setPixelFormatBasedOnScreenForBitmap(self.drawingBitmap)
            # set size and splitters as saved in domain 
            # keep window on screen - left corner of title bar 
            tempBoundsRect = udomain.domain.mainWindowRect
            if (tempBoundsRect.Left != 0) or (tempBoundsRect.Right != 0) or (tempBoundsRect.Top != 0) or (tempBoundsRect.Bottom != 0):
                if tempBoundsRect.Left > delphi_compatability.Screen.Width - kMinWidthOnScreen:
                    tempBoundsRect.Left = delphi_compatability.Screen.Width - kMinWidthOnScreen
                if tempBoundsRect.Top > delphi_compatability.Screen.Height - kMinHeightOnScreen:
                    tempBoundsRect.Top = delphi_compatability.Screen.Height - kMinHeightOnScreen
                self.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom)
            if udomain.domain.horizontalSplitterPos > 0:
                self.horizontalSplitter.Top = udomain.domain.horizontalSplitterPos
            else:
                self.horizontalSplitter.Top = self.ClientHeight / 2
            if udomain.domain.verticalSplitterPos > 0:
                self.verticalSplitter.Left = udomain.domain.verticalSplitterPos
            else:
                self.verticalSplitter.Left = self.ClientWidth / 3
        finally:
            ucursor.cursor_stopWait()
    
    def loadPlantFileAtStartup(self):
        ucursor.cursor_startWait()
        try:
            if udomain.domain.plantFileLoaded:
                # if file loaded at startup, update for it, else act as if they picked new 
                uwait.startWaitMessage("Drawing...")
                try:
                    self.updateForPlantFile()
                finally:
                    uwait.stopWaitMessage()
            else:
                self.MenuFileNewClick(self)
            if usplash.splashForm != None:
                usplash.splashForm.Hide()
            self.updateForChangeToDomainOptions()
            self.updateFileMenuForOtherRecentFiles()
            self.selectedPlantPartID = -1
            self.inFormCreation = false
        finally:
            ucursor.cursor_stopWait()
    
    def FormActivate(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        self.MenuEditPasteAsText.enabled = (UNRESOLVED.Clipboard.hasFormat(UNRESOLVED.CF_TEXT)) and (udomain.domain.plantFileLoaded)
    
    def showWelcomeForm(self):
        welcomeForm = TWelcomeForm()
        
        if udomain.domain.options.hideWelcomeForm:
            return
        welcomeForm = uwelcome.TWelcomeForm().create(delphi_compatability.Application)
        try:
            if welcomeForm.ShowModal() != mrCancel:
                if welcomeForm.whatToDo == uwelcome.kReadSuperSpeedTour:
                    delphi_compatability.Application.HelpJump("Super-Speed_Tour")
                elif welcomeForm.whatToDo == uwelcome.kReadTutorial:
                    delphi_compatability.Application.HelpJump("Tutorial")
                elif welcomeForm.whatToDo == uwelcome.kMakeNewPlant:
                    self.MenuPlantNewClick(self)
                elif welcomeForm.whatToDo == uwelcome.kOpenPlantLibrary:
                    if udomain.domain.plantFileName == "":
                        udomain.domain.plantFileName = ExtractFilePath(delphi_compatability.Application.exeName)
                    self.MenuFileOpenClick(self)
                elif welcomeForm.whatToDo == uwelcome.kStartUsingProgram:
                    pass
            udomain.domain.options.hideWelcomeForm = welcomeForm.hideWelcomeForm.Checked
        finally:
            welcomeForm.free
            welcomeForm = None
    
    def FormDestroy(self, Sender):
        self.commandList.free
        self.commandList = None
        self.drawingBitmap.free
        self.drawingBitmap = None
        self.selectedPlants.free
        self.selectedPlants = None
        # don't free statsPanel because we are the owner 
    
    # ------------------------------------------------------------------------- *file menu 
    def MenuFileNewClick(self, Sender):
        if not self.askForSaveAndProceed():
            return
        udomain.domain.resetForNoPlantFile()
        self.updateForNoPlantFile()
        udomain.domain.resetForEmptyPlantFile()
        self.updateForPlantFile()
        # new v1.4 reset to 100% magnification on new file
        self.magnificationPercent.Text = "100%"
        self.changeMagnificationWithoutClick()
    
    def WMDropFiles(self, Msg):
        CFileName = [0] * (range(0, UNRESOLVED.MAX_PATH + 1) + 1)
        
        try:
            if UNRESOLVED.DragQueryFile(Msg.Drop, 0, CFileName, UNRESOLVED.MAX_PATH) > 0:
                if UNRESOLVED.pos(".PLA", uppercase(CFileName)) <= 0:
                    return
                if not self.askForSaveAndProceed():
                    return
                self.openFile(CFileName)
                Msg.Result = 0
        finally:
            UNRESOLVED.DragFinish(Msg.Drop)
    
    def MenuFileOpenClick(self, Sender):
        fileNameWithPath = ""
        
        if not self.askForSaveAndProceed():
            return
        fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypePlant, udomain.domain.plantFileName, "Choose a plant file")
        if fileNameWithPath == "":
            return
        self.openFile(fileNameWithPath)
    
    # dependent objects 
    # general 
    # plant handling 
    # selecting plants with rubber banding 
    # drawing and progress 
    # mouse movement 
    # resizing and splitting 
    # hints 
    # parameters panel 
    # posings panel
    # file menu 
    def openFile(self, fileNameWithPath):
        udomain.domain.resetForNoPlantFile()
        self.updateForNoPlantFile()
        try:
            self.inFileOpen = true
            try:
                uwait.startWaitMessage("Opening " + ExtractFileName(fileNameWithPath))
                udomain.domain.load(fileNameWithPath)
            except Exception, E:
                uwait.stopWaitMessage()
                ShowMessage(E.message)
                ShowMessage("Could not load file " + fileNameWithPath)
                return
            self.updateForPlantFile()
            uwait.stopWaitMessage()
        finally:
            self.inFileOpen = false
    
    def MenuFileCloseClick(self, Sender):
        if not self.askForSaveAndProceed():
            return
        udomain.domain.resetForNoPlantFile()
        self.updateForPlantFile()
    
    # returns false if user canceled leaving
    def askForSaveAndProceed(self):
        result = false
        messageBoxResult = 0
        
        result = true
        if not plantFileChanged:
            return result
        #cfk fix - put help context in - for all messageDlgs 
        messageBoxResult = MessageDialog("Save changes to " + ExtractFileName(udomain.domain.plantFileName) + "?", mtConfirmation, mbYesNoCancel, 0)
        if messageBoxResult == delphi_compatability.IDCANCEL:
            result = false
        elif messageBoxResult == delphi_compatability.IDYES:
            self.MenuFileSaveClick(self)
            result = self.lastSaveProceeded
        elif messageBoxResult == delphi_compatability.IDNO:
            result = true
        else :
            ShowMessage("Error with save request dialog.")
            result = true
        return result
    
    def MenuFileSaveClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        
        if UNRESOLVED.pos(uppercase(udomain.kUnsavedFileName), uppercase(ExtractFileName(udomain.domain.plantFileName))) > 0:
            self.MenuFileSaveAsClick(self)
            return
        self.lastSaveProceeded = usupport.getFileSaveInfo(usupport.kFileTypePlant, usupport.kDontAskForFileName, udomain.domain.plantFileName, fileInfo)
        if not self.lastSaveProceeded:
            return
        try:
            usupport.startFileSave(fileInfo)
            uwait.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...")
            udomain.domain.save(fileInfo.tempFile)
            fileInfo.writingWasSuccessful = true
        finally:
            uwait.stopWaitMessage()
            usupport.cleanUpAfterFileSave(fileInfo)
            self.setPlantFileChanged(false)
            udomain.domain.updateRecentFileNames(fileInfo.newFile)
            self.clearCommandList()
    
    def setPlantFileChanged(self, fileChanged):
        plantFileChanged = fileChanged
        if self.plantFileChangedImage != None:
            if plantFileChanged:
                self.plantFileChangedImage.Picture = self.fileChangedImage.Picture
            else:
                self.plantFileChangedImage.Picture = self.fileNotChangedImage.Picture
            self.plantFileChangedImage.Invalidate()
            self.plantFileChangedImage.Refresh()
    
    def MenuFileSaveAsClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        
        self.lastSaveProceeded = usupport.getFileSaveInfo(usupport.kFileTypePlant, usupport.kAskForFileName, udomain.domain.plantFileName, fileInfo)
        if not self.lastSaveProceeded:
            return
        try:
            usupport.startFileSave(fileInfo)
            uwait.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...")
            udomain.domain.save(fileInfo.tempFile)
            fileInfo.writingWasSuccessful = true
        finally:
            uwait.stopWaitMessage()
            usupport.cleanUpAfterFileSave(fileInfo)
            self.setPlantFileChanged(false)
            self.clearCommandList()
        udomain.domain.plantFileName = fileInfo.newFile
        udomain.domain.lastOpenedPlantFileName = udomain.domain.plantFileName
        udomain.domain.updateRecentFileNames(udomain.domain.lastOpenedPlantFileName)
        self.Caption = self.captionForFile()
    
    def MenuFilePlantMoverClick(self, Sender):
        mover = TMoverForm()
        response = 0
        
        if plantFileChanged:
            response = MessageDialog("Do you want to save your changes to " + ExtractFileName(udomain.domain.plantFileName) + chr(13) + "before you use the plant mover?", mtConfirmation, mbYesNoCancel, 0)
            if response == delphi_compatability.IDCANCEL:
                return
            elif response == delphi_compatability.IDYES:
                self.MenuFileSaveClick(self)
            elif response == delphi_compatability.IDNO:
                pass
        mover = umover.TMoverForm().create(self)
        if mover == None:
            raise GeneralException.create("Problem: Could not create plant mover window.")
        try:
            mover.ShowModal()
            #in case mover copied something
            self.updatePasteMenuForClipboardContents()
            if mover.changedCurrentPlantFile:
                if mover.untitledDomainFileSavedAs != "":
                    udomain.domain.plantFileName = mover.untitledDomainFileSavedAs
                # cfk fix put help context in 
                response = MessageDialog("The current plant file has changed." + chr(13) + "Do you want to reload the changed file?", mtConfirmation, [mbYes, mbNo, ], 0)
                if response == delphi_compatability.IDYES:
                    try:
                        uwait.startWaitMessage("Opening " + ExtractFileName(udomain.domain.plantFileName))
                        self.updateForNoPlantFile()
                        udomain.domain.load(udomain.domain.plantFileName)
                    except Exception, E:
                        uwait.stopWaitMessage()
                        ShowMessage(E.message)
                        ShowMessage("Could not load file " + udomain.domain.plantFileName + ".")
                        return
                    self.updateForPlantFile()
                    uwait.stopWaitMessage()
        finally:
            mover.free
            mover = None
    
    def MenuFileTdoMoverClick(self, Sender):
        mover = TTdoMoverForm()
        
        mover = utdomove.TTdoMoverForm().create(self)
        if mover == None:
            raise GeneralException.create("Problem: Could not create 3D object mover window.")
        try:
            mover.ShowModal()
        finally:
            mover.free
            mover = None
    
    def WMQueryEndSession(self, message):
        PdForm.WMQueryEndSession(self)
        if not self.askForSaveAndProceed():
            # prevents windows from shutting down
            message.result = 0
        elif not self.cleanUpBeforeExit():
            message.result = 0
    
    def MenuFileExitClick(self, Sender):
        if not self.askForSaveAndProceed():
            return
        elif not self.cleanUpBeforeExit():
            return
        delphi_compatability.Application.Terminate()
    
    def FormClose(self, Sender, Action):
        if not self.askForSaveAndProceed():
            # same as exit, but can't call exit because we have to set the action flag 
            Action = delphi_compatability.TCloseAction.caNone
        elif not self.cleanUpBeforeExit():
            Action = delphi_compatability.TCloseAction.caNone
    
    # returns false if user cancels quit
    def cleanUpBeforeExit(self):
        result = false
        response = 0
        okayToQuit = false
        randomNumber = 0.0
        lowerLimit = 0.0
        upperLimit = 0.0
        
        result = true
        udomain.domain.mainWindowRect = Rect(self.Left, self.Top, self.Width, self.Height)
        udomain.domain.horizontalSplitterPos = self.horizontalSplitter.Top
        udomain.domain.verticalSplitterPos = self.verticalSplitter.Left
        udomain.domain.breederWindowRect = Rect(ubreedr.BreederForm.Left, ubreedr.BreederForm.Top, ubreedr.BreederForm.Width, ubreedr.BreederForm.Height)
        udomain.domain.timeSeriesWindowRect = Rect(utimeser.TimeSeriesForm.Left, utimeser.TimeSeriesForm.Top, utimeser.TimeSeriesForm.Width, utimeser.TimeSeriesForm.Height)
        udomain.domain.debugWindowRect = Rect(udebug.DebugForm.Left, udebug.DebugForm.Top, udebug.DebugForm.Width, udebug.DebugForm.Height)
        if udomain.domain.useIniFile:
            okayToQuit = self.storeIniFile()
            if not okayToQuit:
                result = false
                return result
        # start putting up reminder after one hour
        lowerLimit = 1.0 / 24.0
        if (not udomain.domain.registered) and (udomain.domain.accumulatedUnregisteredTime > lowerLimit):
            UNRESOLVED.Randomize
            randomNumber = UNRESOLVED.random
            # v2 changed this - used to get to saturation after 24 hrs, changed to 12 - more reminding
            # almost always after 12 hrs
            upperLimit = umath.min(udomain.domain.accumulatedUnregisteredTime / (12.0 / 24.0), 0.9)
            if (randomNumber < upperLimit):
                uabout.AboutForm.initializeWithWhetherClosingProgram(true)
                response = uabout.AboutForm.ShowModal()
                self.updateForRegistrationChange()
                if response == mrCancel:
                    result = false
                    return result
        # have to clear out parameter panels before leaving, for some reason was making program crash
        #    but only if tdo components existed at the time of leaving the program. this works for now,
        #    but it would be better to understand why it was happening. 
        self.sectionsComboBox.ItemIndex = -1
        self.updateParameterPanelsForSectionChange()
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_QUIT, 0)
        return result
    
    def storeIniFile(self):
        result = false
        fileSavedOK = false
        choseAnotherFileName = false
        buttonPressed = 0
        saveDialog = TSaveDialog()
        
        result = true
        fileSavedOK = false
        choseAnotherFileName = false
        while not fileSavedOK:
            try:
                udomain.domain.storeProfileInformation()
                fileSavedOK = true
            except:
                fileSavedOK = false
            if not fileSavedOK:
                buttonPressed = MessageDialog("Could not save settings to " + chr(13) + chr(13) + "  " + udomain.domain.iniFileName + chr(13) + chr(13) + "Would you like to save them to another file?", delphi_compatability.TMsgDlgType.mtError, mbYesNoCancel, 0)
                if buttonPressed == delphi_compatability.IDYES:
                    saveDialog = delphi_compatability.TSaveDialog().Create(delphi_compatability.Application)
                    try:
                        saveDialog.FileName = udomain.domain.iniFileName
                        saveDialog.Filter = "Ini files (*.ini)|*.ini|All files (*.*)|*.*"
                        saveDialog.DefaultExt = "ini"
                        saveDialog.Options = saveDialog.Options + [delphi_compatability.TOpenOption.ofPathMustExist, delphi_compatability.TOpenOption.ofOverwritePrompt, delphi_compatability.TOpenOption.ofHideReadOnly, delphi_compatability.TOpenOption.ofNoReadOnlyReturn, ]
                        result = saveDialog.Execute()
                        if result:
                            udomain.domain.iniFileName = saveDialog.FileName
                            choseAnotherFileName = true
                    finally:
                        saveDialog.free
                    if not result:
                        return result
                elif buttonPressed == delphi_compatability.IDNO:
                    return result
                elif buttonPressed == delphi_compatability.IDCANCEL:
                    result = false
                    return result
        if fileSavedOK and choseAnotherFileName:
            ShowMessage("Your settings have been saved in " + chr(13) + chr(13) + "  " + udomain.domain.iniFileName + chr(13) + chr(13) + "But PlantStudio will load the original settings file again at startup." + chr(13) + "To use this settings file at startup, search in the help system" + chr(13) + "for \"alternate settings file\".")
        return result
    
    # ---------------------------------------------------------------------------- *edit menu 
    def MenuEditUndoClick(self, Sender):
        self.commandList.undoLast()
        # commands handle updating if it has to do with plant list, so only update drawing part here 
        self.updateForPossibleChangeToDrawing()
    
    def UndoMenuEditUndoRedoListClick(self, Sender):
        undoRedoListForm = TUndoRedoListForm()
        response = 0
        newCommand = PdCommand()
        i = 0
        
        undoRedoListForm = uundo.TUndoRedoListForm().create(self)
        if undoRedoListForm == None:
            raise GeneralException.create("Problem: Could not create undo/redo list window.")
        try:
            undoRedoListForm.initializeWithCommandList(self.commandList)
            response = undoRedoListForm.ShowModal()
            if response == mrOK:
                try:
                    self.enableOrDisableAllForms(kDisableAllForms)
                    uwait.startWaitMessage("Multiple undo/redo in progress; please wait...")
                    if undoRedoListForm.undoToIndex() >= 0:
                        for i in range(0, undoRedoListForm.undoToIndex() + 1):
                            self.commandList.undoLast()
                    elif undoRedoListForm.redoToIndex() >= 0:
                        for i in range(0, undoRedoListForm.redoToIndex() + 1):
                            self.commandList.redoLast()
                finally:
                    self.updateForPossibleChangeToDrawing()
                    uwait.stopWaitMessage()
                    self.enableOrDisableAllForms(kEnableAllForms)
        finally:
            undoRedoListForm.free
    
    def MenuEditRedoClick(self, Sender):
        self.commandList.redoLast()
        self.updateForPossibleChangeToDrawing()
    
    def MenuEditCutClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdRemoveCommand().createWithListOfPlantsAndClipboardFlag(self.selectedPlants, updcom.kCopyToClipboard)
        #command calls copy, which enables paste menu item
        self.doCommand(newCommand)
    
    def MenuEditCopyClick(self, Sender):
        self.copySelectedPlantsToClipboard()
    
    def MenuEditCopyAsTextClick(self, Sender):
        i = 0
        plant = PdPlant()
        
        if self.selectedPlants.Count > 0:
            UNRESOLVED.Clipboard.clear
            self.plantsAsTextMemo.Clear()
            for i in range(0, self.selectedPlants.Count):
                plant = uplant.PdPlant(self.selectedPlants.Items[i])
                if plant == None:
                    continue
                plant.writeToMainFormMemoAsText()
            self.plantsAsTextMemo.SelectAll()
            self.plantsAsTextMemo.CutToClipboard()
    
    def MenuEditPasteAsTextClick(self, Sender):
        fakeTextFile = TextFile()
        plant = PdPlant()
        newPlants = TList()
        newCommand = PdCommand()
        aLine = ""
        secondLine = ""
        plantName = ""
        i = 0
        startLine = 0
        endLine = 0
        
        newPlants = None
        if not UNRESOLVED.Clipboard.hasFormat(UNRESOLVED.CF_TEXT):
            MessageDialog("The clipboard has no text in it.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            return
        self.plantsAsTextMemo.Clear()
        self.plantsAsTextMemo.PasteFromClipboard()
        if self.plantsAsTextMemo.Lines.Count <= 0:
            MessageDialog("The clipboard has no text in it.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            return
        startLine = -1
        endLine = -1
        for i in range(0, self.plantsAsTextMemo.Lines.Count):
            if UNRESOLVED.pos(uplant.kPlantAsTextStartString, self.plantsAsTextMemo.Lines.Strings[i]) > 0:
                startLine = i
                break
        for i in range(self.plantsAsTextMemo.Lines.Count - 1, 0 + 1):
            if UNRESOLVED.pos(uplant.kPlantAsTextEndString, self.plantsAsTextMemo.Lines.Strings[i]) > 0:
                endLine = i
                break
        if startLine < 0:
            self.plantsAsTextMemo.Clear()
            MessageDialog("The clipboard has text in it, but no plants." + chr(13) + chr(13) + "I can't find a starting line for a plant text description." + chr(13) + "It should have \"" + uplant.kPlantAsTextStartString + "\" in it." + chr(13) + chr(13) + "If you copied the text for a plant," + chr(13) + "make sure the first line is selected and copy it again.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            return
        if endLine < 0:
            self.plantsAsTextMemo.Clear()
            MessageDialog("The clipboard has text in it, but no plants." + chr(13) + chr(13) + "I can't find an ending line for a plant text description." + chr(13) + "It should have \"" + uplant.kPlantAsTextEndString + "\" in it." + chr(13) + chr(13) + "If you copied the text for a plant," + chr(13) + "make sure the whole plant is selected and copy it again.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            return
        newPlants = delphi_compatability.TList().Create()
        try:
            # since startLine and endLine are comments, we can read them
            i = startLine
            while i <= endLine:
                aLine = self.plantsAsTextMemo.Lines.Strings[i]
                i += 1
                if trim(aLine) == "":
                    # v1.60final ignore blank lines
                    continue
                if UNRESOLVED.pos(";", aLine) == 1:
                    continue
                if UNRESOLVED.pos("[", aLine) == 1:
                    uplantmn.checkVersionNumberInPlantNameLine(aLine)
                    plant = uplant.PdPlant().create()
                    plantName = usupport.stringBeyond(aLine, "[")
                    plantName = usupport.stringUpTo(plantName, "]")
                    plant.setName(plantName + " from text")
                    udomain.domain.parameterManager.setAllReadFlagsToFalse()
                    plant.readingFromMemo = true
                    try:
                        while (UNRESOLVED.pos(uplant.kPlantAsTextEndString, aLine) <= 0) and (i <= endLine):
                            # v1.60final fixed cutting off plant at blank line (was changed in file read in v1.3)
                            # aLine <> '' do
                            aLine = self.plantsAsTextMemo.Lines.Strings[i]
                            i += 1
                            if UNRESOLVED.pos(";", aLine) == 1:
                                continue
                            if trim(aLine) == "":
                                continue
                            if UNRESOLVED.pos(uppercase(uplant.kStartNoteString), uppercase(aLine)) > 0:
                                # added v1.6b1 to accommodate paste from text with note
                                plant.noteLines.Clear()
                                while i <= self.plantsAsTextMemo.Lines.Count - 1:
                                    aLine = self.plantsAsTextMemo.Lines.Strings[i]
                                    i += 1
                                    if (UNRESOLVED.pos(uppercase(uplant.kEndNoteString), uppercase(aLine)) > 0) and (plant.noteLines.Count < 5000):
                                        break
                                    elif UNRESOLVED.pos(";", aLine) == 1:
                                        continue
                                    else:
                                        plant.noteLines.Add(aLine)
                            # end added v1.6b1
                            plant.readingMemoLine = i
                            plant.readLineAndTdoFromPlantFile(aLine, fakeTextFile)
                            if i != plant.readingMemoLine:
                                i = plant.readingMemoLine
                    finally:
                        plant.readingFromMemo = false
                        plant.readingMemoLine = -1
                    plant.finishLoadingOrDefaulting(uplant.kCheckForUnreadParams)
                    # cfk change v1.3 make plant fit into 100x100 box with paste from text, because
                    # the scale always seems to be way off from what is being used; this way it always
                    # looks okay when it pastes
                    plant.drawPreviewIntoCache(Point(udomain.domain.options.pasteRectSize, udomain.domain.options.pasteRectSize), uplant.kDontConsiderDomainScale, uplant.kDontDrawNow)
                    newPlants.Add(plant)
            newCommand = updcom.PdPasteCommand().createWithListOfPlantsAndOldSelectedList(newPlants, self.selectedPlants)
            self.doCommand(newCommand)
        finally:
            #command has another list, so we need to free this one; command will free plants if paste is undone
            newPlants.free
    
    # export 
    def getBitmapCopySavePrintOptions(self, copySavePrintType):
        result = 0
        bitmapOptionsForm = TBitmapOptionsForm()
        
        result = mrCancel
        bitmapOptionsForm = ubmpopt.TBitmapOptionsForm().create(self)
        if bitmapOptionsForm == None:
            raise GeneralException.create("Problem: Could not create copy/save/print options window.")
        try:
            bitmapOptionsForm.initializeWithTypeAndOptions(copySavePrintType, udomain.domain.bitmapOptions)
            result = bitmapOptionsForm.ShowModal()
            udomain.domain.bitmapOptions = bitmapOptionsForm.options
        finally:
            bitmapOptionsForm.free
        return result
    
    def MenuEditCopyDrawingClick(self, Sender):
        bitmapForExport = TBitmap()
        
        if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort():
            return
        if (udomain.domain == None) or (udomain.domain.plantManager == None) or (self.plants.Count <= 0):
            return
        if self.getBitmapCopySavePrintOptions(ubmpopt.kCopyingDrawing) == mrOK:
            bitmapForExport = delphi_compatability.TBitmap().Create()
            try:
                self.fillBitmapForExport(bitmapForExport, udomain.domain.bitmapOptions)
                ubitmap.CopyBitmapToClipboard(bitmapForExport)
            finally:
                bitmapForExport.free
                if (not udomain.domain.registered):
                    self.incrementUnregisteredExportCount()
    
    def MenuFileSaveDrawingAsClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        bitmapForExport = TBitmap()
        suggestedFileName = ""
        
        if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort():
            return
        if (udomain.domain == None) or (udomain.domain.plantManager == None) or (self.plants.Count <= 0):
            return
        if self.getBitmapCopySavePrintOptions(ubmpopt.kSavingDrawingToBmp) == mrCancel:
            return
        pictureFileSaveAttemptsThisSession += 1
        suggestedFileName = "picture" + IntToStr(pictureFileSaveAttemptsThisSession) + ".bmp"
        if not usupport.getFileSaveInfo(usupport.kFileTypeBitmap, usupport.kAskForFileName, suggestedFileName, fileInfo):
            return
        bitmapForExport = delphi_compatability.TBitmap().Create()
        try:
            usupport.startFileSave(fileInfo)
            uwait.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...")
            self.fillBitmapForExport(bitmapForExport, udomain.domain.bitmapOptions)
            if not ubitmap.RequiresPalette(bitmapForExport):
                bitmapForExport.ReleasePalette()
                bitmapForExport.ignorePalette = true
            bitmapForExport.SaveToFile(fileInfo.tempFile)
            fileInfo.writingWasSuccessful = true
        finally:
            bitmapForExport.free
            uwait.stopWaitMessage()
            usupport.cleanUpAfterFileSave(fileInfo)
    
    def MenuFileSaveJPEGClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        bitmapForExport = TBitmap()
        jpegForExport = TJPEGImage()
        suggestedFileName = ""
        
        if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort():
            return
        if (udomain.domain == None) or (udomain.domain.plantManager == None) or (self.plants.Count <= 0):
            return
        if self.getBitmapCopySavePrintOptions(ubmpopt.kSavingDrawingToJpeg) == mrCancel:
            return
        pictureFileSaveAttemptsThisSession += 1
        suggestedFileName = "picture" + IntToStr(pictureFileSaveAttemptsThisSession) + ".jpg"
        if not usupport.getFileSaveInfo(usupport.kFileTypeJPEG, usupport.kAskForFileName, suggestedFileName, fileInfo):
            return
        bitmapForExport = delphi_compatability.TBitmap().Create()
        jpegForExport = UNRESOLVED.TJPEGImage.create
        try:
            usupport.startFileSave(fileInfo)
            uwait.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...")
            self.fillBitmapForExport(bitmapForExport, udomain.domain.bitmapOptions)
            if not ubitmap.RequiresPalette(bitmapForExport):
                bitmapForExport.ReleasePalette()
                bitmapForExport.ignorePalette = true
            jpegForExport.assign(bitmapForExport)
            # no option here
            jpegForExport.pixelFormat = UNRESOLVED.jf24Bit
            # we ask for compression, they want quality, so we switch here
            jpegForExport.compressionQuality = UNRESOLVED.TJPEGQualityRange(100 - udomain.domain.bitmapOptions.jpegCompressionRatio)
            jpegForExport.saveToFile(fileInfo.tempFile)
            fileInfo.writingWasSuccessful = true
        finally:
            bitmapForExport.free
            jpegForExport.free
            uwait.stopWaitMessage()
            usupport.cleanUpAfterFileSave(fileInfo)
    
    def MenuFilePrintDrawingClick(self, Sender):
        printRect_pixels = TRect()
        bitmapForExport = TBitmap()
        xResolution_pixelsPerInch = 0.0
        yResolution_pixelsPerInch = 0.0
        printOffsetX_px = 0
        printOffsetY_px = 0
        
        if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort():
            return
        if (udomain.domain == None) or (udomain.domain.plantManager == None) or (self.plants.Count <= 0):
            return
        if self.getBitmapCopySavePrintOptions(ubmpopt.kPrintingDrawing) == mrCancel:
            return
        bitmapForExport = delphi_compatability.TBitmap().Create()
        try:
            self.fillBitmapForExport(bitmapForExport, udomain.domain.bitmapOptions)
            UNRESOLVED.Printer.Title = "PlantStudio Picture"
            UNRESOLVED.Printer.beginDoc
            xResolution_pixelsPerInch = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSX)
            yResolution_pixelsPerInch = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSY)
            printOffsetX_px = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PhysicalOffsetX)
            printOffsetY_px = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PhysicalOffsetY)
            printRect_pixels.Left = intround(udomain.domain.bitmapOptions.printLeftMargin_in * xResolution_pixelsPerInch) - printOffsetX_px
            printRect_pixels.Top = intround(udomain.domain.bitmapOptions.printTopMargin_in * yResolution_pixelsPerInch) - printOffsetY_px
            printRect_pixels.Right = printRect_pixels.Left + intround(udomain.domain.bitmapOptions.printWidth_in * xResolution_pixelsPerInch)
            printRect_pixels.Bottom = printRect_pixels.Top + intround(udomain.domain.bitmapOptions.printHeight_in * yResolution_pixelsPerInch)
            UNRESOLVED.inflateRect(printRect_pixels, -udomain.domain.bitmapOptions.borderThickness, -udomain.domain.bitmapOptions.borderThickness)
            ubitmap.PrintBitmap(bitmapForExport, printRect_pixels)
            # FIX unresolved WITH expression: UNRESOLVED.Printer.Canvas
            # border
            self.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
            if udomain.domain.bitmapOptions.printBorderInner:
                UNRESOLVED.pen.color = udomain.domain.bitmapOptions.printBorderColorInner
                UNRESOLVED.pen.width = udomain.domain.bitmapOptions.printBorderWidthInner
                UNRESOLVED.rectangle(printRect_pixels.Left, printRect_pixels.Top, printRect_pixels.Right, printRect_pixels.Bottom)
            if udomain.domain.bitmapOptions.printBorderOuter:
                UNRESOLVED.pen.color = udomain.domain.bitmapOptions.printBorderColorOuter
                UNRESOLVED.pen.width = udomain.domain.bitmapOptions.printBorderWidthOuter
                UNRESOLVED.rectangle(printRect_pixels.Left - udomain.domain.bitmapOptions.borderGap, printRect_pixels.Top - udomain.domain.bitmapOptions.borderGap, printRect_pixels.Right + udomain.domain.bitmapOptions.borderGap, printRect_pixels.Bottom + udomain.domain.bitmapOptions.borderGap)
            UNRESOLVED.Printer.endDoc
        finally:
            bitmapForExport.free
            if (not udomain.domain.registered):
                self.incrementUnregisteredExportCount()
    
    # edit menu 
    def copySelectedPlantsToClipboard(self):
        if self.selectedPlants.Count <= 0:
            return
        udomain.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(self.selectedPlants)
        udomain.domain.plantManager.setCopiedFromMainWindowFlagInClipboardPlants()
        self.updatePasteMenuForClipboardContents()
    
    def fillBitmapForExport(self, bitmapForExport, options):
        combinedBoundsRect = TRect()
        rectToDrawIn = TRect()
        unregRect = TRect()
        xMultiplier = 0.0
        yMultiplier = 0.0
        scaleMultiplier = 0.0
        plantPartsToDraw = 0L
        plantsToDraw = TList()
        excludeInvisiblePlants = false
        excludeNonSelectedPlants = false
        
        if (bitmapForExport == None) or (udomain.domain == None) or (delphi_compatability.Application.terminated):
            return
        plantsToDraw = None
        # set up according to domain options
        bitmapForExport.PixelFormat = options.colorType
        excludeInvisiblePlants = true
        excludeNonSelectedPlants = false
        if options.exportType == udomain.kIncludeSelectedPlants:
            plantsToDraw = self.selectedPlants
            excludeInvisiblePlants = true
            excludeNonSelectedPlants = true
            combinedBoundsRect = udomain.domain.plantManager.combinedPlantBoundsRects(self.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants)
        elif options.exportType == udomain.kIncludeVisiblePlants:
            plantsToDraw = self.plants
            excludeInvisiblePlants = true
            excludeNonSelectedPlants = false
            combinedBoundsRect = udomain.domain.plantManager.combinedPlantBoundsRects(self.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants)
        elif options.exportType == udomain.kIncludeAllPlants:
            plantsToDraw = self.plants
            excludeInvisiblePlants = false
            excludeNonSelectedPlants = false
            combinedBoundsRect = udomain.domain.plantManager.combinedPlantBoundsRects(self.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants)
        elif options.exportType == udomain.kIncludeDrawingAreaContents:
            plantsToDraw = self.plants
            excludeInvisiblePlants = true
            excludeNonSelectedPlants = false
            combinedBoundsRect = Rect(0, 0, self.drawingBitmap.Width, self.drawingBitmap.Height)
        rectToDrawIn = Rect(0, 0, options.width_pixels, options.height_pixels)
        if (plantsToDraw == None) or (plantsToDraw.Count <= 0):
            return
        bitmapForExport.Palette = UNRESOLVED.CopyPalette(self.paletteImage.Picture.Bitmap.Palette)
        xMultiplier = umath.safedivExcept(1.0 * usupport.rWidth(rectToDrawIn), 1.0 * usupport.rWidth(combinedBoundsRect), 1.0)
        yMultiplier = umath.safedivExcept(1.0 * usupport.rHeight(rectToDrawIn), 1.0 * usupport.rHeight(combinedBoundsRect), 1.0)
        scaleMultiplier = umath.min(xMultiplier, yMultiplier)
        try:
            ucursor.cursor_startWait()
            ubmpsupport.resizeBitmap(bitmapForExport, Point(intround(usupport.rWidth(combinedBoundsRect) * scaleMultiplier), intround(usupport.rHeight(combinedBoundsRect) * scaleMultiplier)))
            udomain.domain.drawingToMakeCopyBitmap = true
            udomain.domain.temporarilyHideSelectionRectangles = true
            udomain.domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm() * scaleMultiplier
            udomain.domain.plantDrawOffsetWhenDrawingCopy_mm = udomain.domain.plantDrawOffset_mm()
            if options.exportType != udomain.kIncludeDrawingAreaContents:
                udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.x = udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.x - umath.safedivExcept(1.0 * combinedBoundsRect.Left, udomain.domain.plantDrawScale_PixelsPerMm(), 0)
                udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.y = udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.y - umath.safedivExcept(1.0 * combinedBoundsRect.Top, udomain.domain.plantDrawScale_PixelsPerMm(), 0)
            ubmpsupport.fillBitmap(bitmapForExport, udomain.domain.options.backgroundColor)
            plantPartsToDraw = 0
            if udomain.domain.options.showPlantDrawingProgress:
                plantPartsToDraw = udomain.domain.plantManager.totalPlantPartCountInInvalidRect(plantsToDraw, combinedBoundsRect, excludeInvisiblePlants, excludeNonSelectedPlants)
            try:
                self.drawing = true
                if udomain.domain.options.showPlantDrawingProgress:
                    self.startDrawProgress(plantPartsToDraw)
                # leave out openGL for now, put in later when you get bitmap drawing working
                udomain.domain.plantManager.drawOnInvalidRect(bitmapForExport.Canvas, plantsToDraw, combinedBoundsRect, excludeInvisiblePlants, excludeNonSelectedPlants)
            finally:
                self.drawing = false
                if udomain.domain.options.showPlantDrawingProgress:
                    self.finishDrawProgress()
            if not udomain.domain.registered:
                scaleMultiplier = umath.max(1.0, scaleMultiplier)
                unregRect = Rect(1, 1, intround(self.unregisteredExportReminder.Width * scaleMultiplier) + 1, intround(self.unregisteredExportReminder.Height * scaleMultiplier) + 1)
                bitmapForExport.Canvas.StretchDraw(unregRect, self.unregisteredExportReminder.Picture.Bitmap)
        finally:
            ucursor.cursor_stopWait()
            udomain.domain.temporarilyHideSelectionRectangles = false
            udomain.domain.drawingToMakeCopyBitmap = false
            udomain.domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm = 1.0
            udomain.domain.plantDrawOffsetWhenDrawingCopy_mm = usupport.setSinglePoint(0, 0)
    
    def MenuEditPasteClick(self, Sender):
        self.pastePlantsFromClipboard()
    
    def pastePlantsFromClipboard(self):
        newPlants = TList()
        newCommand = PdCommand()
        
        newPlants = None
        if udomain.domain.plantManager.privatePlantClipboard.Count <= 0:
            return
        newPlants = delphi_compatability.TList().Create()
        try:
            udomain.domain.plantManager.pastePlantsFromPrivatePlantClipboardToList(newPlants)
            newCommand = updcom.PdPasteCommand().createWithListOfPlantsAndOldSelectedList(newPlants, self.selectedPlants)
            self.doCommand(newCommand)
        finally:
            #command has another list, so we need to free this one; command will free plants if paste is undone
            newPlants.free
    
    def standardPastePosition(self):
        result = TPoint()
        result = Point(self.drawingPaintBox.Width / 2, 3 * self.drawingPaintBox.Height / 4)
        return result
    
    def MenuEditDeleteClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdRemoveCommand().createWithListOfPlantsAndClipboardFlag(self.selectedPlants, updcom.kDontCopyToClipboard)
        self.doCommand(newCommand)
    
    def MenuEditDuplicateClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdDuplicateCommand().createWithListOfPlants(self.selectedPlants)
        self.doCommand(newCommand)
    
    def MenuEditPreferencesClick(self, Sender):
        optionsForm = TOptionsForm()
        response = 0
        newCommand = PdCommand()
        
        optionsForm = uoptions.TOptionsForm().create(self)
        if optionsForm == None:
            raise GeneralException.create("Problem: Could not create preferences window.")
        try:
            optionsForm.options = udomain.domain.options
            response = optionsForm.ShowModal()
            if (response == mrOK) and (optionsForm.optionsChanged):
                newCommand = updcom.PdChangeDomainOptionsCommand().createWithOptions(optionsForm.options)
                self.doCommand(newCommand)
        finally:
            optionsForm.free
            optionsForm = None
    
    # ---------------------------------------------------------------------------- *plant menu 
    def MenuPlantNewClick(self, Sender):
        newCommand = PdCommand()
        wizardForm = TWizardForm()
        response = 0
        newPlantFromWizard = PdPlant()
        
        try:
            ucursor.cursor_startWait()
            # on slower computer wizard takes a long time to come up
            uwait.startWaitMessage("Starting the plant wizard...")
            wizardForm = uwizard.TWizardForm().create(self)
        finally:
            uwait.stopWaitMessage()
            ucursor.cursor_stopWait()
        if wizardForm == None:
            raise GeneralException.create("Problem: Could not create wizard window.")
        try:
            response = wizardForm.ShowModal()
            if response == mrOK:
                if wizardForm.plant == None:
                    raise GeneralException.create("Problem: New wizard plant is nil.")
                newPlantFromWizard = uplant.PdPlant().create()
                wizardForm.plant.copyTo(newPlantFromWizard)
                newCommand = updcom.PdNewCommand().createWithWizardPlantAndOldSelectedList(newPlantFromWizard, self.selectedPlants)
                self.doCommand(newCommand)
                # command will free newPlantFromWizard 
        finally:
            wizardForm.free
            wizardForm = None
    
    def MenuPlantNewUsingLastWizardSettingsClick(self, Sender):
        newCommand = PdCommand()
        wizardForm = TWizardForm()
        newPlantFromWizard = PdPlant()
        
        try:
            # use wizard form to make a new plant using the current settings, but don't show the form
            # this is a sloppy way of doing this, but using the settings to set plant params is embedded in the form.
            ucursor.cursor_startWait()
            uwait.startWaitMessage("Making new plant...")
            wizardForm = uwizard.TWizardForm().create(self)
        finally:
            ucursor.cursor_stopWait()
        newPlantFromWizard = uplant.PdPlant().create()
        try:
            if wizardForm == None:
                raise GeneralException.create("Problem: Could not create plant from last wizard settings.")
            if wizardForm.plant == None:
                raise GeneralException.create("Problem: Could not create plant from last wizard settings (nil plant).")
            wizardForm.setPlantVariables()
            wizardForm.plant.copyTo(newPlantFromWizard)
            newPlantFromWizard.setAge(newPlantFromWizard.pGeneral.ageAtMaturity)
            newCommand = updcom.PdNewCommand().createWithWizardPlantAndOldSelectedList(newPlantFromWizard, self.selectedPlants)
            self.doCommand(newCommand)
        finally:
            # command will free newPlantFromWizard 
            wizardForm.free
            wizardForm = None
            uwait.stopWaitMessage()
    
    def MenuPlantRenameClick(self, Sender):
        newName = ansistring()
        response = false
        newCommand = PdCommand()
        plant = PdPlant()
        
        plant = self.focusedPlant()
        if plant == None:
            return
        newName = plant.getName()
        response = InputQuery("Rename plant", "Enter a new name for " + plant.getName(), newName)
        if response:
            newCommand = updcom.PdRenameCommand().createWithPlantAndNewName(plant, newName)
            self.doCommand(newCommand)
    
    def MenuPlantRandomizeClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdRandomizeCommand().createWithListOfPlants(self.selectedPlants)
        self.doCommand(newCommand)
    
    def MenuPlantZeroRotationsClick(self, Sender):
        self.resetRotationsClick(self)
    
    def MenuPlantBreedClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        if ubreedr.BreederForm.selectedRow >= udomain.domain.breedingAndTimeSeriesOptions.maxGenerations - 2:
            # check if there is room in the breeder - this command will make two new generations 
            ubreedr.BreederForm.fullWarning()
        else:
            newCommand = updcom.PdBreedFromParentsCommand().createWithInfo(ubreedr.BreederForm.generations, self.focusedPlant(), self.firstUnfocusedPlant(), -1, udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, updcom.kCreateFirstGeneration)
            self.doCommand(newCommand)
    
    def MenuPlantMakeTimeSeriesClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdMakeTimeSeriesCommand().createWithNewPlant(self.focusedPlant())
        self.doCommand(newCommand)
    
    def checkForUnregisteredExportCountOverMaxReturnTrueIfAbort(self):
        result = false
        result = false
        if (udomain.domain.totalUnregisteredExportsAtThisMoment() >= udomain.kMaxUnregExportsAllowed) and (udomain.domain.unregisteredExportCountThisSession >= udomain.kMaxUnregExportsPerSessionAfterMaxReached):
            MessageDialog("Thank you for evaluating PlantStudio!" + chr(13) + chr(13) + "You have exported PlantStudio output at least " + IntToStr(udomain.kMaxUnregExportsAllowed) + " times" + chr(13) + "since installing it for evaluation," + " and " + IntToStr(udomain.kMaxUnregExportsPerSessionAfterMaxReached) + " times this session." + chr(13) + chr(13) + "To export more output without registering," + chr(13) + "simply close and restart the program." + chr(13) + chr(13) + "To remove this restriction, purchase a registration code," + chr(13) + "then enter it into the Help-Register window" + chr(13) + "to register your copy of PlantStudio.", mtInformation, [mbOK, ], 0)
            result = true
            self.MenuHelpRegisterClick(self)
        return result
    
    def incrementUnregisteredExportCount(self):
        udomain.domain.unregisteredExportCountThisSession += 1
        if udomain.domain.totalUnregisteredExportsAtThisMoment() == udomain.kMaxUnregExportsAllowed:
            udomain.domain.unregisteredExportCountBeforeThisSession = udomain.domain.unregisteredExportCountBeforeThisSession + udomain.domain.unregisteredExportCountThisSession
            udomain.domain.unregisteredExportCountThisSession = 0
        self.updateForChangedExportCount()
    
    #v2.1
    # v2.1 separated this out and added call in animation saving
    # it is the same otherwise except for the padding
    def enoughRoomToSaveFile(self, tempFileName, fileDescriptor, fileSizeNeeded_MB):
        result = false
        driveLetter = ""
        driveNumber = 0
        fileMegaBytesAvailable = 0.0
        
        result = true
        driveLetter = uppercase(UNRESOLVED.copy(UNRESOLVED.ExtractFileDrive(tempFileName), 1, 1))
        driveNumber = ord(driveLetter[1]) - ord("A") + 1
        fileMegaBytesAvailable = 1.0 * UNRESOLVED.diskFree(driveNumber) / (1024 * 1024)
        if fileMegaBytesAvailable >= 0:
            if fileMegaBytesAvailable < fileSizeNeeded_MB * 1.1:
                # if there are too many bytes available, the integer wraps around and goes negative, so ignore this case
                # pad size needed in case estimate is slightly off  // v2.1
                ShowMessage("Not enough space to save " + fileDescriptor + " file(s) (" + usupport.digitValueString(fileSizeNeeded_MB) + " MB needed, " + usupport.digitValueString(fileMegaBytesAvailable) + " MB available)." + chr(13) + "Choose another option or make more space available.")
                result = false
        return result
    
    def ExportToGeneric3DType(self, outputType):
        fileInfo = SaveFileNamesStructure()
        optionsForm = TGeneric3DOptionsForm()
        tempOptions = FileExport3DOptionsStructure()
        response = 0
        fileType = 0
        suggestedFileName = ""
        fileDescriptor = ""
        optionsChanged = false
        excludeInvisiblePlants = false
        excludeNonSelectedPlants = false
        newCommand = PdCommand()
        
        if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort():
            return
        response = mrCancel
        optionsChanged = false
        optionsForm = uoptions3dexport.TGeneric3DOptionsForm().create(self)
        if optionsForm == None:
            raise GeneralException.create("Problem: Could not create 3D export options window.")
        try:
            optionsForm.outputType = outputType
            optionsForm.rearrangeItemsForOutputType()
            optionsForm.options = udomain.domain.exportOptionsFor3D[outputType]
            response = optionsForm.ShowModal()
            tempOptions = optionsForm.options
            optionsChanged = optionsForm.optionsChanged
        finally:
            optionsForm.free
            optionsForm = None
        if response != mrOK:
            return
        fileType = u3dexport.fileTypeFor3DExportType(outputType)
        fileDescriptor = usupport.nameStringForFileType(fileType)
        exportTo3DFileSaveAttemptsThisSession[outputType] += 1
        suggestedFileName = "plants" + IntToStr(exportTo3DFileSaveAttemptsThisSession[outputType]) + "." + usupport.extensionForFileType(fileType)
        if not usupport.getFileSaveInfo(fileType, usupport.kAskForFileName, suggestedFileName, fileInfo):
            if optionsChanged:
                if MessageDialog(fileDescriptor + " export stopped." + chr(13) + chr(13) + "Do you want to save the changes you made" + chr(13) + "to the " + fileDescriptor + " export options?", mtConfirmation, [mbYes, mbNo, ], 0) == delphi_compatability.IDYES:
                    newCommand = updcom.PdChangeDomain3DOptionsCommand().createWithOptionsAndType(tempOptions, outputType)
                    self.doCommand(newCommand)
            return
        if not self.enoughRoomToSaveFile(fileInfo.tempFile, fileDescriptor, tempOptions.fileSize):
            return
        if optionsChanged:
            newCommand = updcom.PdChangeDomain3DOptionsCommand().createWithOptionsAndType(tempOptions, outputType)
            self.doCommand(newCommand)
        try:
            usupport.startFileSave(fileInfo)
            if outputType == u3dexport.kPOV:
                fileInfo.newFile = usupport.replacePunctuationWithUnderscores(usupport.stringUpTo(ExtractFileName(fileInfo.newFile), ".")) + ".inc"
            uwait.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...")
            excludeInvisiblePlants = false
            excludeNonSelectedPlants = false
            if tempOptions.exportType == udomain.kIncludeSelectedPlants:
                excludeInvisiblePlants = true
                excludeNonSelectedPlants = true
            elif tempOptions.exportType == udomain.kIncludeVisiblePlants:
                excludeInvisiblePlants = true
            udomain.domain.plantManager.write3DOutputFileToFileName(self.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants, fileInfo.tempFile, outputType)
            fileInfo.writingWasSuccessful = true
        finally:
            uwait.stopWaitMessage()
            usupport.cleanUpAfterFileSave(fileInfo)
    
    def MenuPlantExportToDXFClick(self, Sender):
        self.ExportToGeneric3DType(u3dexport.kDXF)
    
    def MenuPlantExportTo3DSClick(self, Sender):
        self.ExportToGeneric3DType(u3dexport.k3DS)
    
    def MenuPlantExportToOBJClick(self, Sender):
        self.ExportToGeneric3DType(u3dexport.kOBJ)
    
    def MenuPlantExportToPOVClick(self, Sender):
        self.ExportToGeneric3DType(u3dexport.kPOV)
    
    def MenuPlantExportToVRMLClick(self, Sender):
        self.ExportToGeneric3DType(u3dexport.kVRML)
    
    def MenuPlantExportToLWOClick(self, Sender):
        self.ExportToGeneric3DType(u3dexport.kLWO)
    
    # -------------------------------------------------------------------------- *layout menu 
    def MenuLayoutSelectAllClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = updcom.PdSelectOrDeselectAllCommand().createWithListOfPlants(self.selectedPlants)
        self.doCommand(newCommand)
    
    def MenuLayoutDeselectClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = updcom.PdSelectOrDeselectAllCommand().createWithListOfPlants(self.selectedPlants)
        (newCommand as updcom.PdSelectOrDeselectAllCommand).deselect = true
        self.doCommand(newCommand)
    
    def MenuFileMakePainterNozzleClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        bitmapForExport = TBitmap()
        suggestedFileName = ""
        
        if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort():
            return
        if (udomain.domain == None) or (udomain.domain.plantManager == None) or (self.plants.Count <= 0):
            return
        if self.getNozzleOptions() == mrCancel:
            return
        if udomain.domain.nozzleOptions.cellCount <= 0:
            return
        nozzleFileSaveAttemptsThisSession += 1
        suggestedFileName = "nozzle" + IntToStr(nozzleFileSaveAttemptsThisSession) + " " + IntToStr(udomain.domain.nozzleOptions.cellSize.X) + "x" + IntToStr(udomain.domain.nozzleOptions.cellSize.Y) + "x" + IntToStr(udomain.domain.nozzleOptions.cellCount) + ".bmp"
        if not usupport.getFileSaveInfo(usupport.kFileTypeBitmap, usupport.kAskForFileName, suggestedFileName, fileInfo):
            return
        bitmapForExport = delphi_compatability.TBitmap().Create()
        try:
            usupport.startFileSave(fileInfo)
            uwait.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...")
            self.fillBitmapForPainterNozzle(bitmapForExport)
            bitmapForExport.SaveToFile(fileInfo.tempFile)
            fileInfo.writingWasSuccessful = true
        finally:
            bitmapForExport.free
            uwait.stopWaitMessage()
            usupport.cleanUpAfterFileSave(fileInfo)
    
    def getNozzleOptions(self):
        result = 0
        nozzleOptionsForm = TNozzleOptionsForm()
        
        result = mrCancel
        nozzleOptionsForm = unozzle.TNozzleOptionsForm().create(self)
        if nozzleOptionsForm == None:
            raise GeneralException.create("Problem: Could not create nozzle options window.")
        try:
            nozzleOptionsForm.initializeWithOptions(udomain.domain.nozzleOptions)
            result = nozzleOptionsForm.ShowModal()
            udomain.domain.nozzleOptions = nozzleOptionsForm.options
        finally:
            nozzleOptionsForm.free
        return result
    
    def fillBitmapForPainterNozzle(self, bitmapForExport):
        plantsToDraw = TList()
        oldBackgroundColor = TColorRef()
        i = 0
        plant = PdPlant()
        oldPlantScale = 0.0
        scaleMultiplier = 0.0
        scaledPlantSize = TPoint()
        
        if (bitmapForExport == None) or (udomain.domain == None) or (delphi_compatability.Application.terminated):
            return
        plantsToDraw = None
        oldBackgroundColor = udomain.domain.options.backgroundColor
        bitmapForExport.PixelFormat = udomain.domain.nozzleOptions.colorType
        if udomain.domain.nozzleOptions.exportType == udomain.kIncludeSelectedPlants:
            plantsToDraw = self.selectedPlants
        else:
            plantsToDraw = self.plants
        if (plantsToDraw == None) or (plantsToDraw.Count <= 0):
            return
        try:
            ucursor.cursor_startWait()
            ubmpsupport.resizeBitmap(bitmapForExport, Point(intround(udomain.domain.nozzleOptions.cellSize.X * plantsToDraw.Count), udomain.domain.nozzleOptions.cellSize.Y))
            scaleMultiplier = umath.safedivExcept(1.0 * udomain.domain.nozzleOptions.resolution_pixelsPerInch, 1.0 * delphi_compatability.Screen.PixelsPerInch, 1.0)
            # v1.4 changed 0.8 to 0.9 because fitting algorithm works better now
            # extra margin to make sure plants fit
            scaleMultiplier = scaleMultiplier * 0.9
            udomain.domain.options.backgroundColor = udomain.domain.nozzleOptions.backgroundColor
            ubmpsupport.fillBitmap(bitmapForExport, udomain.domain.nozzleOptions.backgroundColor)
            for i in range(0, plantsToDraw.Count):
                plant = uplant.PdPlant(plantsToDraw.Items[i])
                scaledPlantSize = Point(intround(usupport.rWidth(plant.boundsRect_pixels()) * scaleMultiplier), intround(usupport.rHeight(plant.boundsRect_pixels()) * scaleMultiplier))
                oldPlantScale = plant.drawingScale_PixelsPerMm
                try:
                    # v1.4
                    plant.fixedPreviewScale = false
                    # v1.4
                    plant.fixedDrawPosition = false
                    plant.drawPreviewIntoCache(scaledPlantSize, uplant.kDontConsiderDomainScale, kDrawNow)
                    bitmapForExport.Canvas.Draw(i * udomain.domain.nozzleOptions.cellSize.X, 0, plant.previewCache)
                    plant.shrinkPreviewCache()
                finally:
                    plant.drawingScale_PixelsPerMm = oldPlantScale
                    plant.recalculateBounds(kDrawNow)
        finally:
            ucursor.cursor_stopWait()
            udomain.domain.options.backgroundColor = oldBackgroundColor
    
    def MenuFileMakePainterAnimationClick(self, Sender):
        saveDialog = TSaveDialog()
        sizeNeeded_MB = 0.0
        
        if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort():
            return
        if (udomain.domain == None) or (udomain.domain.plantManager == None) or (self.plants.Count <= 0):
            return
        if self.focusedPlant() == None:
            return
        if self.getAnimationOptions() == mrCancel:
            return
        if udomain.domain.animationOptions.frameCount <= 0:
            return
        saveDialog = delphi_compatability.TSaveDialog().Create(delphi_compatability.Application)
        try:
            saveDialog.Title = "Choose a file name (numbers will be added)"
            saveDialog.FileName = self.focusedPlant().getName() + ".bmp"
            saveDialog.Filter = "Bitmap files (*.bmp)|*.bmp"
            saveDialog.DefaultExt = "bmp"
            saveDialog.Options = saveDialog.Options + [delphi_compatability.TOpenOption.ofPathMustExist, delphi_compatability.TOpenOption.ofOverwritePrompt, delphi_compatability.TOpenOption.ofHideReadOnly, delphi_compatability.TOpenOption.ofNoReadOnlyReturn, ]
            if saveDialog.Execute():
                sizeNeeded_MB = 1.0 * udomain.domain.animationOptions.fileSize / (1024 * 1024)
                if not self.enoughRoomToSaveFile(saveDialog.FileName, "animation", sizeNeeded_MB):
                    return
                ucursor.cursor_startWait()
                uwait.startWaitMessage("Starting...")
                try:
                    self.writeAnimationFilesWithFileSpec(usupport.stringUpTo(saveDialog.FileName, ".") + " ")
                finally:
                    ucursor.cursor_stopWait()
                    uwait.stopWaitMessage()
        finally:
            saveDialog.free
    
    def writeAnimationFilesWithFileSpec(self, startFileName):
        plant = PdPlant()
        oldXRotation = 0.0
        scaleMultiplier = 0.0
        minScale = 0.0
        oldScale = 0.0
        oldAge = 0
        i = 0
        saveFileName = ""
        unregRect = TRect()
        bestPosition = TPoint()
        widestWidth = 0L
        tallestHeight = 0L
        
        if self.focusedPlant() == None:
            return
        plant = self.focusedPlant()
        oldXRotation = plant.xRotation
        oldAge = plant.age
        oldScale = plant.drawingScale_PixelsPerMm
        try:
            plant.previewCache.PixelFormat = udomain.domain.animationOptions.colorType
            # draw plant for all frames, get min drawing scale
            plant.fixedPreviewScale = false
            plant.fixedDrawPosition = false
            minScale = 0
            for i in range(0, udomain.domain.animationOptions.frameCount):
                setPlantCharacteristicsForAnimationFrame(plant, i)
                plant.drawPreviewIntoCache(udomain.domain.animationOptions.scaledSize, uplant.kDontConsiderDomainScale, uplant.kDontDrawNow)
                if (i == 1) or (plant.drawingScale_PixelsPerMm < minScale):
                    minScale = plant.drawingScale_PixelsPerMm
            # draw plant for all frames, get common draw position
            plant.drawingScale_PixelsPerMm = minScale
            plant.fixedPreviewScale = true
            widestWidth = 0
            tallestHeight = 0
            for i in range(0, udomain.domain.animationOptions.frameCount):
                setPlantCharacteristicsForAnimationFrame(plant, i)
                plant.drawPreviewIntoCache(udomain.domain.animationOptions.scaledSize, uplant.kDontConsiderDomainScale, uplant.kDontDrawNow)
                if (i == 0) or (usupport.rWidth(plant.boundsRect_pixels()) > widestWidth):
                    widestWidth = usupport.rWidth(plant.boundsRect_pixels())
                    bestPosition.X = plant.drawPositionIfFixed.X
                if (i == 0) or (usupport.rHeight(plant.boundsRect_pixels()) > tallestHeight):
                    tallestHeight = usupport.rHeight(plant.boundsRect_pixels())
                    bestPosition.Y = plant.drawPositionIfFixed.Y
            # now really draw
            plant.drawPositionIfFixed = bestPosition
            plant.fixedDrawPosition = true
            for i in range(0, udomain.domain.animationOptions.frameCount):
                saveFileName = startFileName
                if i + 1 < 100:
                    saveFileName = saveFileName + "0"
                if i + 1 < 10:
                    saveFileName = saveFileName + "0"
                saveFileName = saveFileName + IntToStr(i + 1) + ".bmp"
                uwait.startWaitMessage("Saving " + ExtractFileName(saveFileName) + "...")
                setPlantCharacteristicsForAnimationFrame(plant, i)
                plant.drawPreviewIntoCache(udomain.domain.animationOptions.scaledSize, uplant.kDontConsiderDomainScale, kDrawNow)
                if not udomain.domain.registered:
                    scaleMultiplier = umath.safedivExcept(1.0 * udomain.domain.animationOptions.resolution_pixelsPerInch, 1.0 * delphi_compatability.Screen.PixelsPerInch, 1.0)
                    scaleMultiplier = umath.max(1.0, scaleMultiplier)
                    unregRect = Rect(1, 1, intround(self.unregisteredExportReminder.Width * scaleMultiplier) + 1, intround(self.unregisteredExportReminder.Height * scaleMultiplier) + 1)
                    plant.previewCache.Canvas.StretchDraw(unregRect, self.unregisteredExportReminder.Picture.Bitmap)
                plant.previewCache.SaveToFile(saveFileName)
            # clean up for next time
            plant.fixedPreviewScale = false
            plant.fixedDrawPosition = false
        finally:
            plant.shrinkPreviewCache()
            plant.fixedPreviewScale = false
            plant.xRotation = oldXRotation
            plant.drawingScale_PixelsPerMm = oldScale
            plant.setAge(oldAge)
            plant.recalculateBounds(kDrawNow)
    
    def getAnimationOptions(self):
        result = 0
        animationOptionsForm = TAnimationFilesOptionsForm()
        
        result = mrCancel
        if self.focusedPlant() == None:
            return result
        animationOptionsForm = uanimate.TAnimationFilesOptionsForm().create(self)
        if animationOptionsForm == None:
            raise GeneralException.create("Problem: Could not create animation options window.")
        try:
            animationOptionsForm.initializeWithOptionsAndPlant(udomain.domain.animationOptions, self.focusedPlant())
            result = animationOptionsForm.ShowModal()
            udomain.domain.animationOptions = animationOptionsForm.options
        finally:
            animationOptionsForm.free
        return result
    
    def MenuLayoutShowClick(self, Sender):
        newCommand = PdCommand()
        atLeastOnePlantIsHidden = false
        i = 0
        
        if self.selectedPlants.Count <= 0:
            return
        # make sure at least one plant is hidden 
        atLeastOnePlantIsHidden = false
        for i in range(0, self.selectedPlants.Count):
            if uplant.PdPlant(self.selectedPlants.Items[i]).hidden:
                atLeastOnePlantIsHidden = true
                break
        if not atLeastOnePlantIsHidden:
            return
        newCommand = updcom.PdHideOrShowCommand().createWithListOfPlantsAndHideOrShow(self.selectedPlants, updcom.kShow)
        self.doCommand(newCommand)
    
    def MenuLayoutHideClick(self, Sender):
        newCommand = PdCommand()
        atLeastOnePlantIsShowing = false
        i = 0
        
        if self.selectedPlants.Count <= 0:
            return
        # make sure at least one plant is showing 
        atLeastOnePlantIsShowing = false
        for i in range(0, self.selectedPlants.Count):
            if not uplant.PdPlant(self.selectedPlants.Items[i]).hidden:
                atLeastOnePlantIsShowing = true
                break
        if not atLeastOnePlantIsShowing:
            return
        newCommand = updcom.PdHideOrShowCommand().createWithListOfPlantsAndHideOrShow(self.selectedPlants, updcom.kHide)
        self.doCommand(newCommand)
    
    def MenuLayoutHideOthersClick(self, Sender):
        booleansList = TListCollection()
        newCommand = PdCommand()
        i = 0
        plant = PdPlant()
        
        if self.selectedPlants.Count <= 0:
            return
        booleansList = ucollect.TListCollection().Create()
        for i in range(0, self.plants.Count):
            plant = uplant.PdPlant(self.plants.Items[i])
            booleansList.Add(updcom.PdBooleanValue().createWithBoolean(not self.isSelected(plant)))
        try:
            newCommand = updcom.PdHideOrShowCommand().createWithListOfPlantsAndListOfHides(self.plants, booleansList)
            self.doCommand(newCommand)
        finally:
            booleansList.free
    
    def MenuLayoutMakeBouquetClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 1:
            return
        newCommand = updcom.PdDragCommand().createWithListOfPlantsAndNewPoint(self.selectedPlants, self.focusedPlant().basePoint_pixels())
        self.doCommand(newCommand)
    
    def MenuLayoutScaleToFitClick(self, Sender):
        self.centerDrawingClick(self)
    
    # drawing 
    def changeViewingOptionTo(self, aNewOption):
        newCommand = PdCommand()
        
        if (aNewOption == udomain.kViewPlantsInMainWindowOneAtATime) and (self.selectedPlants.Count <= 0):
            if self.plants.Count < 0:
                return
            self.selectedPlants.Add(self.plants.Items[0])
            self.updateForChangeToPlantSelections()
        newCommand = updcom.PdChangeMainWindowViewingOptionCommand().createWithListOfPlantsAndSelectedPlantsAndNewOption(self.plants, self.selectedPlants, aNewOption)
        self.doCommand(newCommand)
        self.MenuLayoutMakeBouquet.enabled = (self.selectedPlants.Count > 1) and (not udomain.domain.viewPlantsInMainWindowOnePlantAtATime())
    
    def MenuLayoutViewOnePlantAtATimeClick(self, Sender):
        if udomain.domain.options.mainWindowViewMode != udomain.kViewPlantsInMainWindowOneAtATime:
            self.changeViewingOptionTo(udomain.kViewPlantsInMainWindowOneAtATime)
    
    def viewOneOnlyClick(self, Sender):
        self.MenuLayoutViewOnePlantAtATimeClick(self)
    
    def MenuLayoutViewFreeFloatingClick(self, Sender):
        if udomain.domain.options.mainWindowViewMode != udomain.kViewPlantsInMainWindowFreeFloating:
            self.changeViewingOptionTo(udomain.kViewPlantsInMainWindowFreeFloating)
    
    def viewFreeFloatingClick(self, Sender):
        self.MenuLayoutViewFreeFloatingClick(self)
    
    def MenuLayoutBringForwardClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        if self.plants.IndexOf(self.firstSelectedPlantInList()) <= 0:
            # don't do if you can't go forward any more 
            return
        newCommand = updcom.PdSendBackwardOrForwardCommand().createWithBackwardOrForward(updcom.kBringForward)
        self.doCommand(newCommand)
    
    def MenuLayoutSendBackClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        if self.plants.IndexOf(self.lastSelectedPlantInList()) >= self.plants.Count - 1:
            # don't do if you can't go backward any more 
            return
        newCommand = updcom.PdSendBackwardOrForwardCommand().createWithBackwardOrForward(updcom.kSendBackward)
        self.doCommand(newCommand)
    
    def MenuLayoutHorizontalOrientationClick(self, Sender):
        newCommand = PdCommand()
        
        if udomain.domain.options.mainWindowOrientation != udomain.kMainWindowOrientationHorizontal:
            newCommand = updcom.PdChangeMainWindowOrientationCommand().createWithNewOrientation(udomain.kMainWindowOrientationHorizontal)
            self.doCommand(newCommand)
    
    def MenuLayoutVerticalOrientationClick(self, Sender):
        newCommand = PdCommand()
        
        if udomain.domain.options.mainWindowOrientation != udomain.kMainWindowOrientationVertical:
            newCommand = updcom.PdChangeMainWindowOrientationCommand().createWithNewOrientation(udomain.kMainWindowOrientationVertical)
            self.doCommand(newCommand)
    
    def drawingAreaOnTopClick(self, Sender):
        self.MenuLayoutHorizontalOrientationClick(self)
    
    def drawingAreaOnSideClick(self, Sender):
        self.MenuLayoutVerticalOrientationClick(self)
    
    # --------------------------------------------------------------------------- *options menu 
    def MenuOptionsFastDrawClick(self, Sender):
        oldSpeed = 0
        
        oldSpeed = udomain.domain.options.drawSpeed
        udomain.domain.options.drawSpeed = udomain.kDrawFast
        self.MenuOptionsFastDraw.checked = true
        ubreedr.BreederForm.BreederMenuOptionsFastDraw.checked = true
        utimeser.TimeSeriesForm.TimeSeriesMenuOptionsFastDraw.checked = true
        if oldSpeed != udomain.domain.options.drawSpeed:
            self.updateForChangeToDrawOptions()
    
    def MenuOptionsMediumDrawClick(self, Sender):
        oldSpeed = 0
        
        oldSpeed = udomain.domain.options.drawSpeed
        udomain.domain.options.drawSpeed = udomain.kDrawMedium
        self.MenuOptionsMediumDraw.checked = true
        ubreedr.BreederForm.BreederMenuOptionsMediumDraw.checked = true
        utimeser.TimeSeriesForm.TimeSeriesMenuOptionsMediumDraw.checked = true
        if oldSpeed != udomain.domain.options.drawSpeed:
            self.updateForChangeToDrawOptions()
    
    def MenuOptionsBestDrawClick(self, Sender):
        oldSpeed = 0
        
        oldSpeed = udomain.domain.options.drawSpeed
        udomain.domain.options.drawSpeed = udomain.kDrawBest
        self.MenuOptionsBestDraw.checked = true
        ubreedr.BreederForm.BreederMenuOptionsBestDraw.checked = true
        utimeser.TimeSeriesForm.TimeSeriesMenuOptionsBestDraw.checked = true
        if oldSpeed != udomain.domain.options.drawSpeed:
            self.updateForChangeToDrawOptions()
    
    def MenuOptionsCustomDrawClick(self, Sender):
        customDrawForm = TCustomDrawOptionsForm()
        newCommand = PdCommand()
        response = 0
        lastDrawSpeed = 0
        
        lastDrawSpeed = udomain.domain.options.drawSpeed
        udomain.domain.options.drawSpeed = udomain.kDrawCustom
        self.MenuOptionsCustomDraw.checked = true
        ubreedr.BreederForm.BreederMenuOptionsCustomDraw.checked = true
        utimeser.TimeSeriesForm.TimeSeriesMenuOptionsCustomDraw.checked = true
        customDrawForm = ucustdrw.TCustomDrawOptionsForm().create(self)
        if customDrawForm == None:
            raise GeneralException.create("Problem: Could not create 3D object mover window.")
        try:
            customDrawForm.options = udomain.domain.options
            response = customDrawForm.ShowModal()
            newCommand = None
            if (response == mrOK) and (customDrawForm.optionsChanged):
                newCommand = updcom.PdChangeDomainOptionsCommand().createWithOptions(customDrawForm.options)
                self.doCommand(newCommand)
            else:
                if lastDrawSpeed != udomain.kDrawCustom:
                    # escape just escapes changing options in dialog, not setting to custom, should still redraw
                    # v1.4 change UNLESS it was custom before.
                    self.updateForChangeToDrawOptions()
        finally:
            customDrawForm.free
            customDrawForm = None
    
    def MenuOptionsUsePlantBitmapsClick(self, Sender):
        if udomain.domain.options.cachePlantBitmaps:
            self.stopUsingPlantBitmaps()
        else:
            self.startUsingPlantBitmaps()
        self.updateForChangeToPlantBitmaps()
        self.updateForPossibleChangeToDrawing()
    
    def plantBitmapsIndicatorImageClick(self, Sender):
        if (not udomain.domain.options.cachePlantBitmaps) and (self.MenuOptionsUsePlantBitmaps.enabled):
            self.MenuOptionsUsePlantBitmapsClick(self)
    
    def MenuOptionsShowSelectionRectanglesClick(self, Sender):
        self.MenuOptionsShowSelectionRectangles.checked = not self.MenuOptionsShowSelectionRectangles.checked
        udomain.domain.options.showSelectionRectangle = self.MenuOptionsShowSelectionRectangles.checked
        self.copyDrawingBitmapToPaintBox()
    
    def MenuOptionsShowBoundsRectanglesClick(self, Sender):
        self.MenuOptionsShowBoundsRectangles.checked = not self.MenuOptionsShowBoundsRectangles.checked
        udomain.domain.options.showBoundsRectangle = self.MenuOptionsShowBoundsRectangles.checked
        self.copyDrawingBitmapToPaintBox()
    
    def MenuOptionsGhostHiddenPartsClick(self, Sender):
        self.MenuOptionsGhostHiddenParts.checked = not self.MenuOptionsGhostHiddenParts.checked
        udomain.domain.options.showGhostingForHiddenParts = self.MenuOptionsGhostHiddenParts.checked
        self.internalChange = true
        self.posingGhost.Down = udomain.domain.options.showGhostingForHiddenParts
        self.internalChange = false
        # cannot just redraw plants because bounds rects may have changed
        self.redrawEverything()
    
    def MenuOptionsHighlightPosedPartsClick(self, Sender):
        self.MenuOptionsHighlightPosedParts.checked = not self.MenuOptionsHighlightPosedParts.checked
        udomain.domain.options.showHighlightingForNonHiddenPosedParts = self.MenuOptionsHighlightPosedParts.checked
        self.internalChange = true
        self.posingHighlight.Down = udomain.domain.options.showHighlightingForNonHiddenPosedParts
        self.internalChange = false
        self.redrawAllPlantsInViewWithAmendments()
    
    def MenuOptionsHidePosingClick(self, Sender):
        self.MenuOptionsHidePosing.checked = not self.MenuOptionsHidePosing.checked
        udomain.domain.options.showPosingAtAll = not self.MenuOptionsHidePosing.checked
        self.internalChange = true
        self.posingNotShown.Down = not udomain.domain.options.showPosingAtAll
        self.internalChange = false
        # cannot just redraw plants because bounds rects may have changed
        self.redrawEverything()
    
    def posingHighlightClick(self, Sender):
        if self.internalChange:
            return
        udomain.domain.options.showHighlightingForNonHiddenPosedParts = not udomain.domain.options.showHighlightingForNonHiddenPosedParts
        self.MenuOptionsHighlightPosedParts.checked = udomain.domain.options.showHighlightingForNonHiddenPosedParts
        self.posingHighlight.Down = udomain.domain.options.showHighlightingForNonHiddenPosedParts
        self.redrawAllPlantsInViewWithAmendments()
    
    def posingGhostClick(self, Sender):
        if self.internalChange:
            return
        udomain.domain.options.showGhostingForHiddenParts = not udomain.domain.options.showGhostingForHiddenParts
        self.MenuOptionsGhostHiddenParts.checked = udomain.domain.options.showGhostingForHiddenParts
        self.posingGhost.Down = udomain.domain.options.showGhostingForHiddenParts
        # cannot just redraw plants because bounds rects may have changed
        self.redrawEverything()
    
    def posingNotShownClick(self, Sender):
        if self.internalChange:
            return
        udomain.domain.options.showPosingAtAll = not udomain.domain.options.showPosingAtAll
        self.MenuOptionsHidePosing.checked = not udomain.domain.options.showPosingAtAll
        self.posingNotShown.Down = not udomain.domain.options.showPosingAtAll
        # cannot just redraw plants because bounds rects may have changed
        self.redrawEverything()
    
    def MenuOptionsShowLongButtonHintsClick(self, Sender):
        self.MenuOptionsShowLongButtonHints.checked = not self.MenuOptionsShowLongButtonHints.checked
        udomain.domain.options.showLongHintsForButtons = self.MenuOptionsShowLongButtonHints.checked
        self.updateHintPauseForOptions()
        # shows different hint
        self.updateForChangeToPlantBitmaps()
    
    def MenuOptionsShowParameterHintsClick(self, Sender):
        self.MenuOptionsShowParameterHints.checked = not self.MenuOptionsShowParameterHints.checked
        udomain.domain.options.showHintsForParameters = self.MenuOptionsShowParameterHints.checked
        self.updateHintPauseForOptions()
    
    # --------------------------------------------------------------------------- *window menu 
    def MenuWindowBreederClick(self, Sender):
        ubreedr.BreederForm.Show()
        ubreedr.BreederForm.BringToFront()
        if ubreedr.BreederForm.WindowState == delphi_compatability.TWindowState.wsMinimized:
            ubreedr.BreederForm.WindowState = delphi_compatability.TWindowState.wsNormal
    
    def MenuWindowTimeSeriesClick(self, Sender):
        utimeser.TimeSeriesForm.Show()
        utimeser.TimeSeriesForm.BringToFront()
        if utimeser.TimeSeriesForm.WindowState == delphi_compatability.TWindowState.wsMinimized:
            utimeser.TimeSeriesForm.WindowState = delphi_compatability.TWindowState.wsNormal
    
    def MenuWindowNumericalExceptionsClick(self, Sender):
        udebug.DebugForm.Show()
        udebug.DebugForm.BringToFront()
        if udebug.DebugForm.WindowState == delphi_compatability.TWindowState.wsMinimized:
            udebug.DebugForm.WindowState = delphi_compatability.TWindowState.wsNormal
    
    # ---------------------------------------------------------------------------- *help menu 
    def MenuHelpTopicsClick(self, Sender):
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_FINDER, 0)
    
    def MenuHelpAboutClick(self, Sender):
        if udomain.domain.registered:
            if usplash.splashForm == None:
                return
            #domain.registrationName);
            usplash.splashForm.showLoadingString("Registered to:")
            #domain.registrationCode);
            usplash.splashForm.showCodeString(udomain.domain.registrationName)
            usplash.splashForm.close.Visible = true
            usplash.splashForm.supportButton.Visible = true
            usplash.splashForm.ShowModal()
        else:
            if uabout.AboutForm == None:
                return
            uabout.AboutForm.initializeWithWhetherClosingProgram(false)
            uabout.AboutForm.ShowModal()
            self.updateForRegistrationChange()
    
    def MenuHelpRegisterClick(self, Sender):
        uregister.RegistrationForm.ShowModal()
        self.updateForRegistrationChange()
    
    def updateForRegistrationChange(self):
        self.MenuHelpRegister.visible = not udomain.domain.registered
        self.AfterRegisterMenuSeparator.visible = not udomain.domain.registered
        self.Caption = self.captionForFile()
    
    def MenuHelpSuperSpeedTourClick(self, Sender):
        delphi_compatability.Application.HelpJump("Super-Speed_Tour")
    
    def MenuHelpTutorialClick(self, Sender):
        delphi_compatability.Application.HelpJump("Tutorial")
    
    # ---------------------------------------------------------------------------- *progress showing 
    def progressPaintBoxPaint(self, Sender):
        self.progressPaintBox.Canvas.Brush.Color = UNRESOLVED.clBtnFace
        self.progressPaintBox.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear
        self.progressPaintBox.Canvas.Rectangle(0, 0, self.progressPaintBox.Width, self.progressPaintBox.Height)
    
    def startDrawProgress(self, maximum):
        self.drawProgressMax = maximum
        self.progressPaintBox.Invalidate()
        self.progressPaintBox.Refresh()
    
    def showDrawProgress(self, amount):
        progress = 0L
        
        if not self.drawing:
            return
        if (not self.animateTimer.enabled) and (not udomain.domain.options.showPlantDrawingProgress):
            return
        if self.animateTimer.enabled:
            return
        if self.drawProgressMax != 0:
            progress = intround((1.0 * self.progressPaintBox.Width * amount) / (self.drawProgressMax * 1.0))
        else:
            progress = 0
        if progress > 0:
            self.progressPaintBox.Canvas.Brush.Color = kProgressBarColor
            self.progressPaintBox.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear
            self.progressPaintBox.Canvas.Rectangle(0, 0, progress, self.progressPaintBox.Height)
    
    def finishDrawProgress(self):
        self.progressPaintBox.Invalidate()
        self.progressPaintBox.Refresh()
    
    # plant menu 
    # help menu 
    # updating 
    # ---------------------------------------------------------------------------- *updating 
    def updateForNoPlantFile(self):
        self.selectedPlants.Clear()
        self.plantListDrawGrid.Invalidate()
        self.clearCommandList()
        self.Caption = self.captionForFile()
        self.updateRightSidePanelForFirstSelectedPlant()
        self.redrawEverything()
        self.updateMenusForChangedPlantFile()
    
    def redrawEverything(self):
        self.recalculateAllPlantBoundsRects(kDrawNow)
        self.invalidateEntireDrawing()
        self.updateForPossibleChangeToDrawing()
    
    def captionForFile(self):
        result = ""
        numLeft = 0
        
        if (not udomain.domain.plantFileLoaded) or (udomain.domain.plantFileName == ""):
            result = delphi_compatability.Application.Title + " - no file"
        else:
            result = delphi_compatability.Application.Title + " - " + usupport.stringUpTo(ExtractFileName(udomain.domain.plantFileName), ".")
            if not udomain.domain.registered:
                if udomain.domain.totalUnregisteredExportsAtThisMoment() < udomain.kMaxUnregExportsAllowed:
                    # before pool runs out
                    numLeft = umath.intMax(0, udomain.kMaxUnregExportsAllowed - udomain.domain.totalUnregisteredExportsAtThisMoment())
                    if numLeft == 1:
                        result = result + " [unregistered - " + IntToStr(numLeft) + " export left in evaluation]"
                    else:
                        result = result + " [unregistered - " + IntToStr(numLeft) + " exports left in evaluation]"
                    # after pool runs out, fixed number per session
                else:
                    numLeft = umath.intMax(0, udomain.kMaxUnregExportsPerSessionAfterMaxReached - udomain.domain.unregisteredExportCountThisSession)
                    if numLeft <= 0:
                        result = result + " [unregistered - NO exports left this session]"
                    elif numLeft == 1:
                        result = result + " [unregistered - " + IntToStr(numLeft) + " export left this session]"
                    else:
                        result = result + " [unregistered - " + IntToStr(numLeft) + " exports left this session]"
            elif self.plants.Count <= 0:
                result = result + " (no plants)"
            elif self.plants.Count == 1:
                result = result + " (1 plant)"
            else:
                result = result + " (" + IntToStr(self.plants.Count) + " plants)"
        return result
    
    def updateForPlantFile(self):
        plant = PdPlant()
        i = 0
        
        self.internalChange = true
        if not udomain.domain.plantFileLoaded:
            self.updateForNoPlantFile()
        else:
            self.Caption = self.captionForFile()
            self.updateForChangeToPlantList()
            self.updateMenusForChangedPlantFile()
            self.selectedPlants.Clear()
            self.magnificationPercent.Text = IntToStr(intround(udomain.domain.plantDrawScale_PixelsPerMm() * 100.0)) + "%"
            if udomain.domain.plantManager.mainWindowOrientation != udomain.domain.options.mainWindowOrientation:
                # v2.0 load and save window orientation (top or side)
                udomain.domain.options.mainWindowOrientation = udomain.domain.plantManager.mainWindowOrientation
                self.updateForChangeToOrientation()
            if self.plants.Count > 0:
                for i in range(0, self.plants.Count):
                    # v2.0 load and save plant hidden and selected flags
                    plant = uplant.PdPlant(self.plants.Items[i])
                    if plant.selectedWhenLastSaved:
                        self.selectedPlants.Add(plant)
                if self.selectedPlants.Count <= 0:
                    self.selectedPlants.Add(uplant.PdPlant(self.plants.Items[0]))
                self.updateForChangeToPlantSelections()
            if udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
                # deal with possibly changed viewing mode (one/many)
                self.showOnePlantExclusively(kDontDrawYet)
            self.viewOneOnly.Down = udomain.domain.viewPlantsInMainWindowOnePlantAtATime()
            if udomain.domain.plantManager.fitInVisibleAreaForConcentrationChange:
                self.fitVisiblePlantsInDrawingArea(kDrawNow, kScaleAndMove, kAlwaysMove)
                udomain.domain.plantManager.fitInVisibleAreaForConcentrationChange = false
            else:
                self.fitVisiblePlantsInDrawingArea(kDrawNow, kJustMove, kOnlyMoveIfOffTheScreen)
                self.redrawEverything()
        # v2.0 switch to select/drag mode - sometimes it seems to get broken - this will fix it - not unreasonable to do
        self.cursorModeForDrawing = kCursorModeSelectDrag
        self.dragCursorMode.Down = true
        self.internalChange = false
    
    def updateHintPauseForOptions(self):
        delphi_compatability.Application.HintPause = udomain.domain.options.pauseBeforeHint * 1000
        if udomain.domain.options.showLongHintsForButtons or udomain.domain.options.showHintsForParameters:
            delphi_compatability.Application.HintHidePause = udomain.domain.options.pauseDuringHint * 1000
        else:
            delphi_compatability.Application.HintHidePause = 2500
        self.statsPanel.updateHint()
    
    def updateForChangedExportCount(self):
        self.Caption = self.captionForFile()
    
    def updateForChangeToDomainOptions(self):
        self.internalChange = true
        # fonts
        # v1.6b1 -- fix for large fonts problem
        self.Font.Size = udomain.domain.options.parametersFontSize
        self.parametersScrollBox.Font.Size = udomain.domain.options.parametersFontSize
        self.parametersScrollBox.Invalidate()
        # viewing option
        self.MenuLayoutMakeBouquet.enabled = (self.selectedPlants.Count > 1) and (not udomain.domain.viewPlantsInMainWindowOnePlantAtATime())
        self.updateMenusForChangeToViewingOption()
        # drawing
        self.MenuOptionsUsePlantBitmaps.checked = udomain.domain.options.cachePlantBitmaps
        # showing optional things
        self.MenuOptionsShowSelectionRectangles.checked = udomain.domain.options.showSelectionRectangle
        self.MenuOptionsShowBoundsRectangles.checked = udomain.domain.options.showBoundsRectangle
        self.MenuOptionsShowLongButtonHints.checked = udomain.domain.options.showLongHintsForButtons
        self.MenuOptionsShowParameterHints.checked = udomain.domain.options.showHintsForParameters
        # posing
        self.MenuOptionsGhostHiddenParts.checked = udomain.domain.options.showGhostingForHiddenParts
        self.posingGhost.Down = udomain.domain.options.showGhostingForHiddenParts
        self.MenuOptionsHighlightPosedParts.checked = udomain.domain.options.showHighlightingForNonHiddenPosedParts
        self.posingHighlight.Down = udomain.domain.options.showHighlightingForNonHiddenPosedParts
        self.MenuOptionsHidePosing.checked = not udomain.domain.options.showPosingAtAll
        self.posingNotShown.Down = not udomain.domain.options.showPosingAtAll
        # vertical/horizontal
        self.MenuLayoutHorizontalOrientation.checked = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal
        self.MenuLayoutVerticalOrientation.checked = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical
        self.drawingAreaOnTop.Down = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal
        self.drawingAreaOnSide.Down = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical
        self.internalChange = false
        # hint, undo
        self.updateHintPauseForOptions()
        self.commandList.setNewUndoLimit(udomain.domain.options.undoLimit)
        self.commandList.setNewObjectUndoLimit(udomain.domain.options.undoLimitOfPlants)
        if ubreedr.BreederForm != None:
            ubreedr.BreederForm.updateForChangeToDomainOptions()
        if utimeser.TimeSeriesForm != None:
            utimeser.TimeSeriesForm.updateForChangeToDomainOptions()
        if self.lifeCycleShowing():
            #because max drawing scale might have changed
            self.updateLifeCyclePanelForFirstSelectedPlant()
        if not self.inFormCreation:
            self.redrawEverything()
        # in case max changed
        self.updateForChangeToPlantBitmaps()
    
    def updateForChangeToDrawOptions(self):
        self.redrawEverything()
        if ubreedr.BreederForm != None:
            if (ubreedr.BreederForm.Visible) and (ubreedr.BreederForm.WindowState != delphi_compatability.TWindowState.wsMinimized):
                ubreedr.BreederForm.redrawPlants(ubreedr.kDontConsiderIfPreviewCacheIsUpToDate)
            else:
                ubreedr.BreederForm.needToRedrawFromChangeToDrawOptions = true
        if utimeser.TimeSeriesForm != None:
            if (utimeser.TimeSeriesForm.Visible) and (utimeser.TimeSeriesForm.WindowState != delphi_compatability.TWindowState.wsMinimized):
                utimeser.TimeSeriesForm.redrawPlants()
            else:
                utimeser.TimeSeriesForm.needToRedrawFromChangeToDrawOptions = true
    
    def updateMenusForChangeToViewingOption(self):
        self.MenuLayoutViewOnePlantAtATime.checked = udomain.domain.viewPlantsInMainWindowOnePlantAtATime()
        self.MenuLayoutViewFreeFloating.checked = udomain.domain.viewPlantsInMainWindowFreeFloating()
        self.viewOneOnly.Down = udomain.domain.viewPlantsInMainWindowOnePlantAtATime()
        self.viewFreeFloating.Down = udomain.domain.viewPlantsInMainWindowFreeFloating()
    
    def updateForChangeToOrientation(self):
        self.MenuLayoutHorizontalOrientation.checked = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal
        self.MenuLayoutVerticalOrientation.checked = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical
        self.drawingAreaOnTop.Down = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal
        self.drawingAreaOnSide.Down = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical
        self.Resize()
    
    def moveUpOrDownWithKeyInPlantList(self, indexAfterMove):
        newList = TList()
        newCommand = PdCommand()
        
        if indexAfterMove > self.plants.Count - 1:
            # loop around 
            indexAfterMove = 0
        if indexAfterMove < 0:
            indexAfterMove = self.plants.Count - 1
        if (indexAfterMove >= 0) and (indexAfterMove <= self.plants.Count - 1):
            newList = delphi_compatability.TList().Create()
            try:
                newList.Add(self.plants.Items[indexAfterMove])
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(self.selectedPlants, newList)
                self.doCommand(newCommand)
            finally:
                newList.free
    
    def updateForChangeToPlantSelections(self):
        if udomain.domain.options.showSelectionRectangle:
            self.copyDrawingBitmapToPaintBox()
        self.plantListDrawGrid.Repaint()
        # must be done BEFORE updating so it picks it up
        self.selectedPlantPartID = -1
        self.updateRightSidePanelForFirstSelectedPlant()
        self.updateMenusForChangedSelectedPlants()
        if not self.internalChange:
            # reset for posing because posing works only on focused plant
            # don't do if reading file in
            # if change selected plant, must redraw to remove red color
            self.redrawAllPlantsInViewWithAmendments()
    
    def invalidateSelectedPlantRectangles(self):
        i = 0
        plant = PdPlant()
        
        if self.selectedPlants.Count > 0:
            for i in range(0, self.selectedPlants.Count):
                plant = uplant.PdPlant(self.selectedPlants.Items[i])
                if plant != None:
                    self.invalidateDrawingRect(plant.boundsRect_pixels())
    
    def updateForChangeToPlantList(self):
        plant = PdPlant()
        i = 0
        plantsToRemove = TList()
        
        if delphi_compatability.Application.terminated:
            return
        if (udomain.domain == None) or (udomain.domain.plantManager == None):
            return
        self.Caption = self.captionForFile()
        self.plantListDrawGrid.RowCount = self.plants.Count
        self.plantListDrawGrid.Invalidate()
        # selected plants list - make sure no pointers are invalid 
        plantsToRemove = delphi_compatability.TList().Create()
        try:
            if self.selectedPlants.Count > 0:
                for i in range(0, self.selectedPlants.Count):
                    plant = uplant.PdPlant(self.selectedPlants.Items[i])
                    if self.plants.IndexOf(plant) < 0:
                        plantsToRemove.Add(plant)
            if plantsToRemove.Count > 0:
                for i in range(0, plantsToRemove.Count):
                    plant = uplant.PdPlant(plantsToRemove.Items[i])
                    self.selectedPlants.Remove(plant)
        finally:
            plantsToRemove.free
        if udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
            self.showOnePlantExclusively(kDrawNow)
        self.updateRightSidePanelForFirstSelectedPlant()
        self.updateForPossibleChangeToDrawing()
        self.updateMenusForChangedPlantList()
    
    def updateForPossibleChangeToDrawing(self):
        self.updateMenusForUndoRedo()
        if (self.invalidDrawingRect.Top != 0) or (self.invalidDrawingRect.Left != 0) or (self.invalidDrawingRect.Bottom != 0) or (self.invalidDrawingRect.Right != 0):
            self.paintDrawing(kDrawNow)
    
    def recalculateAllPlantBoundsRects(self, drawNow):
        i = 0
        plant = PdPlant()
        showProgress = false
        plantPartsToDraw = 0L
        partsDrawn = 0L
        
        if self.plants.Count <= 0:
            return
        plantPartsToDraw = 0
        showProgress = drawNow and udomain.domain.options.cachePlantBitmaps and udomain.domain.options.showPlantDrawingProgress
        if showProgress:
            plantPartsToDraw = udomain.domain.plantManager.totalPlantPartCountInInvalidRect(self.plants, Rect(0, 0, self.drawingBitmap.Width, self.drawingBitmap.Height), udomain.kExcludeInvisiblePlants, udomain.kIncludeNonSelectedPlants)
        partsDrawn = 0
        try:
            ucursor.cursor_startWait()
            self.drawing = true
            if showProgress:
                self.startDrawProgress(plantPartsToDraw)
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                plant.plantPartsDrawnAtStart = partsDrawn
                plant.recalculateBounds(drawNow)
                partsDrawn = partsDrawn + plant.totalPlantParts
        finally:
            ucursor.cursor_stopWait()
            self.drawing = false
            if showProgress:
                self.finishDrawProgress()
    
    def recalculateSelectedPlantsBoundsRects(self, drawNow):
        i = 0
        plant = PdPlant()
        showProgress = false
        plantPartsToDraw = 0L
        partsDrawn = 0L
        
        if self.selectedPlants.Count <= 0:
            return
        plantPartsToDraw = 0
        showProgress = drawNow and udomain.domain.options.cachePlantBitmaps and udomain.domain.options.showPlantDrawingProgress
        if showProgress:
            plantPartsToDraw = udomain.domain.plantManager.totalPlantPartCountInInvalidRect(self.selectedPlants, Rect(0, 0, self.drawingBitmap.Width, self.drawingBitmap.Height), udomain.kExcludeInvisiblePlants, udomain.kIncludeNonSelectedPlants)
        partsDrawn = 0
        try:
            ucursor.cursor_startWait()
            self.drawing = true
            if showProgress:
                self.startDrawProgress(plantPartsToDraw)
            for i in range(0, self.selectedPlants.Count):
                plant = uplant.PdPlant(self.selectedPlants.Items[i])
                plant.plantPartsDrawnAtStart = partsDrawn
                plant.recalculateBounds(drawNow)
                partsDrawn = partsDrawn + plant.totalPlantParts
        finally:
            ucursor.cursor_stopWait()
            self.drawing = false
            if showProgress:
                self.finishDrawProgress()
    
    def shrinkAllPlantBitmaps(self):
        i = 0
        
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                uplant.PdPlant(self.plants.Items[i]).shrinkPreviewCache()
        self.updateForChangeToPlantBitmaps()
    
    def recalculateAllPlantBoundsRectsForOffsetChange(self):
        i = 0
        plant = PdPlant()
        
        for i in range(0, self.plants.Count):
            plant = uplant.PdPlant(self.plants.Items[i])
            plant.recalculateBoundsForOffsetChange()
    
    def updateForRenamingPlant(self, aPlant):
        i = 0
        
        self.plantListDrawGrid.Invalidate()
        for i in range(0, kTabHighest + 1):
            self.updatePlantNameLabel(i)
    
    def updateForChangeToPlantNote(self, aPlant):
        start = 0
        
        start = self.noteMemo.SelStart
        self.noteMemo.Clear()
        if aPlant == None:
            return
        self.internalChange = true
        if self.focusedPlant() != None:
            self.noteMemo.Lines.AddStrings(aPlant.noteLines)
        self.noteMemo.SelStart = start
        self.internalChange = false
    
    # menu updating 
    # ---------------------------------------------------------------------------- *menu updating 
    def updateMenusForUndoRedo(self):
        if self.commandList.isUndoEnabled():
            self.MenuEditUndo.enabled = true
            self.MenuEditUndo.caption = "&Undo " + self.commandList.undoDescription()
        else:
            self.MenuEditUndo.enabled = false
            self.MenuEditUndo.caption = "Can't undo"
        if self.commandList.isRedoEnabled():
            self.MenuEditRedo.enabled = true
            self.MenuEditRedo.caption = "&Redo " + self.commandList.redoDescription()
        else:
            self.MenuEditRedo.enabled = false
            self.MenuEditRedo.caption = "Can't redo"
        self.UndoMenuEditUndoRedoList.enabled = (self.commandList.isUndoEnabled()) or (self.commandList.isRedoEnabled())
        if ubreedr.BreederForm != None:
            ubreedr.BreederForm.BreederMenuUndo.enabled = self.MenuEditUndo.enabled
            ubreedr.BreederForm.BreederMenuUndo.caption = self.MenuEditUndo.caption
            ubreedr.BreederForm.BreederMenuRedo.enabled = self.MenuEditRedo.enabled
            ubreedr.BreederForm.BreederMenuRedo.caption = self.MenuEditRedo.caption
            ubreedr.BreederForm.BreederMenuUndoRedoList.enabled = self.UndoMenuEditUndoRedoList.enabled
        if utimeser.TimeSeriesForm != None:
            utimeser.TimeSeriesForm.TimeSeriesMenuUndo.enabled = self.MenuEditUndo.enabled
            utimeser.TimeSeriesForm.TimeSeriesMenuUndo.caption = self.MenuEditUndo.caption
            utimeser.TimeSeriesForm.TimeSeriesMenuRedo.enabled = self.MenuEditRedo.enabled
            utimeser.TimeSeriesForm.TimeSeriesMenuRedo.caption = self.MenuEditRedo.caption
            utimeser.TimeSeriesForm.TimeSeriesMenuUndoRedoList.enabled = self.UndoMenuEditUndoRedoList.enabled
    
    def updateMenusForChangedPlantFile(self):
        self.MenuFileClose.enabled = udomain.domain.plantFileLoaded
        self.MenuPlantNew.enabled = udomain.domain.plantFileLoaded
        self.MenuPlantNewUsingLastWizardSettings.enabled = udomain.domain.plantFileLoaded
        self.MenuLayoutViewFreeFloating.enabled = udomain.domain.plantFileLoaded
        self.viewFreeFloating.Enabled = udomain.domain.plantFileLoaded
        self.MenuLayoutViewOnePlantAtATime.enabled = udomain.domain.plantFileLoaded
        self.viewOneOnly.Enabled = udomain.domain.plantFileLoaded
        self.MenuLayoutHorizontalOrientation.enabled = udomain.domain.plantFileLoaded
        self.drawingAreaOnTop.Enabled = udomain.domain.plantFileLoaded
        self.MenuLayoutVerticalOrientation.enabled = udomain.domain.plantFileLoaded
        self.drawingAreaOnSide.Enabled = udomain.domain.plantFileLoaded
        self.updateMenusForChangedPlantList()
        self.updatePasteMenuForClipboardContents()
    
    def updateMenusForChangedPlantList(self):
        havePlants = false
        
        havePlants = (self.plants.Count > 0)
        self.MenuFileSave.enabled = havePlants
        self.MenuFileSaveAs.enabled = havePlants
        self.MenuFileSaveDrawingAs.enabled = havePlants
        self.MenuFilePrintDrawing.enabled = havePlants
        self.MenuLayoutSelectAll.enabled = havePlants
        self.MenuEditCopyDrawing.enabled = havePlants
        self.MenuLayoutScaleToFit.enabled = havePlants
        self.MenuFileMakePainterNozzle.enabled = havePlants
        self.MenuPlantExportToDXF.enabled = havePlants
        self.MenuPlantExportToPOV.enabled = havePlants
        self.MenuPlantExportTo3DS.enabled = havePlants
        self.MenuFileSaveJPEG.enabled = havePlants
        self.MenuPlantExportToLWO.enabled = havePlants
        self.MenuPlantExportToOBJ.enabled = havePlants
        self.MenuPlantExportToVRML.enabled = havePlants
        if not havePlants:
            self.dragCursorModeClick(self)
        self.toolbarPanel.Enabled = havePlants
        self.dragCursorMode.Enabled = havePlants
        self.magnifyCursorMode.Enabled = havePlants
        self.scrollCursorMode.Enabled = havePlants
        self.rotateCursorMode.Enabled = havePlants
        self.posingSelectionCursorMode.Enabled = havePlants
        self.centerDrawing.Enabled = havePlants
        self.magnificationPercent.Enabled = havePlants
        self.updateMenusForChangedSelectedPlants()
    
    def updateMenusForChangedSelectedPlants(self):
        haveSelectedPlants = false
        haveMoreThanOneSelectedPlant = false
        
        haveSelectedPlants = (self.selectedPlants.Count > 0)
        haveMoreThanOneSelectedPlant = (self.selectedPlants.Count > 1)
        self.MenuEditCut.enabled = haveSelectedPlants
        self.PopupMenuCut.enabled = haveSelectedPlants
        self.MenuEditCopy.enabled = haveSelectedPlants
        self.PopupMenuCopy.enabled = haveSelectedPlants
        self.MenuEditCopyAsText.enabled = haveSelectedPlants
        self.MenuEditPasteAsText.enabled = (UNRESOLVED.Clipboard.hasFormat(UNRESOLVED.CF_TEXT)) and (udomain.domain.plantFileLoaded)
        self.MenuEditDelete.enabled = haveSelectedPlants
        self.MenuEditDuplicate.enabled = haveSelectedPlants
        self.MenuPlantRename.enabled = haveSelectedPlants
        self.PopupMenuRename.enabled = haveSelectedPlants
        self.MenuPlantEditNote.enabled = haveSelectedPlants
        # v1.4
        self.PopupMenuEditNote.enabled = haveSelectedPlants
        # v1.4
        self.noteEdit.Enabled = haveSelectedPlants
        self.MenuPlantRandomize.enabled = haveSelectedPlants
        self.PopupMenuRandomize.enabled = haveSelectedPlants
        self.MenuPlantZeroRotations.enabled = haveSelectedPlants
        self.PopupMenuZeroRotations.enabled = haveSelectedPlants
        self.MenuPlantBreed.enabled = haveSelectedPlants
        self.PopupMenuBreed.enabled = haveSelectedPlants
        self.MenuPlantMakeTimeSeries.enabled = haveSelectedPlants
        self.PopupMenuMakeTimeSeries.enabled = haveSelectedPlants
        self.MenuPlantAnimate.enabled = haveSelectedPlants
        self.PopupMenuAnimate.enabled = haveSelectedPlants
        self.MenuLayoutSelectAll.enabled = (self.plants.Count > 0) and (self.selectedPlants.Count < self.plants.Count)
        self.MenuLayoutDeselect.enabled = haveSelectedPlants
        self.MenuFileMakePainterAnimation.enabled = haveSelectedPlants
        self.MenuLayoutHide.enabled = haveSelectedPlants
        self.MenuLayoutShow.enabled = haveSelectedPlants
        self.MenuLayoutHideOthers.enabled = (haveMoreThanOneSelectedPlant) and (not udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) and (self.selectedPlants.Count < self.plants.Count)
        self.MenuLayoutMakeBouquet.enabled = haveMoreThanOneSelectedPlant and not udomain.domain.viewPlantsInMainWindowOnePlantAtATime()
        self.MenuLayoutBringForward.enabled = haveSelectedPlants and (self.selectedPlants.Count < self.plants.Count)
        self.MenuLayoutSendBack.enabled = haveSelectedPlants and (self.selectedPlants.Count < self.plants.Count)
        # location
        self.xLocationEdit.Enabled = haveSelectedPlants
        self.xLocationSpin.Enabled = haveSelectedPlants
        self.yLocationEdit.Enabled = haveSelectedPlants
        self.yLocationSpin.Enabled = haveSelectedPlants
        # rotation
        self.xRotationEdit.Enabled = haveSelectedPlants
        self.xRotationSpin.Enabled = haveSelectedPlants
        self.yRotationEdit.Enabled = haveSelectedPlants
        self.yRotationSpin.Enabled = haveSelectedPlants
        self.zRotationEdit.Enabled = haveSelectedPlants
        self.zRotationSpin.Enabled = haveSelectedPlants
        self.resetRotations.Enabled = haveSelectedPlants
        # drawing scale
        self.drawingScaleEdit.Enabled = haveSelectedPlants
        self.drawingScaleSpin.Enabled = haveSelectedPlants
        # alignment
        self.alignTops.Enabled = haveMoreThanOneSelectedPlant
        self.alignBottoms.Enabled = haveMoreThanOneSelectedPlant
        self.alignLeft.Enabled = haveMoreThanOneSelectedPlant
        self.alignRight.Enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutAlign.enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutAlignTops.enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutAlignBottoms.enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutAlignLeftSides.enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutAlignRightSides.enabled = haveMoreThanOneSelectedPlant
        # size
        self.makeEqualWidth.Enabled = haveMoreThanOneSelectedPlant
        self.makeEqualHeight.Enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutSize.enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutSizeSameWidth.enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutSizeSameHeight.enabled = haveMoreThanOneSelectedPlant
        # pack
        self.packPlants.Enabled = haveMoreThanOneSelectedPlant
        self.MenuLayoutPack.enabled = haveMoreThanOneSelectedPlant
    
    def updatePasteMenuForClipboardContents(self):
        self.MenuEditPaste.enabled = (udomain.domain.plantManager.privatePlantClipboard.Count > 0)
        self.PopupMenuPaste.enabled = self.MenuEditPaste.enabled
        if ubreedr.BreederForm != None:
            ubreedr.BreederForm.updatePasteMenuForClipboardContents()
        if utimeser.TimeSeriesForm != None:
            utimeser.TimeSeriesForm.updatePasteMenuForClipboardContents()
    
    def updateSectionPopupMenuForSectionChange(self):
        haveSection = false
        
        haveSection = self.currentSection() != None
        self.sectionPopupMenuHelp.enabled = haveSection
    
    def updateParamPopupMenuForParamSelectionChange(self):
        haveSection = false
        haveParam = false
        
        haveSection = self.currentSection() != None
        self.paramPopupMenuExpandAllInSection.enabled = haveSection
        self.paramPopupMenuCollapseAllInSection.enabled = haveSection
        haveParam = self.selectedParameterPanel != None
        self.paramPopupMenuHelp.enabled = haveParam
        self.paramPopupMenuExpand.enabled = haveParam
        self.paramPopupMenuCollapse.enabled = haveParam
    
    # ---------------------------------------------------------------------------- *drawing 
    def invalidateDrawingRect(self, aRect):
        newRect = TRect()
        
        newRect = self.invalidDrawingRect
        delphi_compatability.UnionRect(newRect, newRect, aRect)
        self.invalidDrawingRect = newRect
    
    def invalidateEntireDrawing(self):
        self.invalidDrawingRect = Rect(0, 0, self.drawingBitmap.Width, self.drawingBitmap.Height)
    
    def paintDrawing(self, immediate):
        plantPartsToDraw = 0L
        showProgress = false
        
        if delphi_compatability.Application.terminated:
            return
        plantPartsToDraw = 0
        showProgress = udomain.domain.options.showPlantDrawingProgress and (not udomain.domain.options.cachePlantBitmaps)
        if (self.invalidDrawingRect.Top != 0) or (self.invalidDrawingRect.Left != 0) or (self.invalidDrawingRect.Bottom != 0) or (self.invalidDrawingRect.Right != 0):
            try:
                if not self.mouseMoveActionInProgress:
                    ucursor.cursor_startWait()
                UNRESOLVED.intersectClipRect(self.drawingBitmap.Canvas.Handle, self.invalidDrawingRect.Left, self.invalidDrawingRect.Top, self.invalidDrawingRect.Right, self.invalidDrawingRect.Bottom)
                ubmpsupport.fillBitmap(self.drawingBitmap, udomain.domain.options.backgroundColor)
                if showProgress:
                    plantPartsToDraw = udomain.domain.plantManager.totalPlantPartCountInInvalidRect(self.selectedPlants, self.invalidDrawingRect, udomain.kExcludeInvisiblePlants, udomain.kIncludeNonSelectedPlants)
                try:
                    self.drawing = true
                    if showProgress:
                        self.startDrawProgress(plantPartsToDraw)
                    udomain.domain.plantManager.drawOnInvalidRect(self.drawingBitmap.Canvas, self.selectedPlants, self.invalidDrawingRect, udomain.kExcludeInvisiblePlants, udomain.kIncludeNonSelectedPlants)
                finally:
                    self.drawing = false
                    if showProgress:
                        self.finishDrawProgress()
                if (immediate):
                    self.copyDrawingBitmapToPaintBox()
            finally:
                if not self.mouseMoveActionInProgress:
                    ucursor.cursor_stopWait()
                self.invalidDrawingRect = delphi_compatability.Bounds(0, 0, 0, 0)
    
    def drawingPaintBoxPaint(self, Sender):
        self.copyDrawingBitmapToPaintBox()
    
    def copyDrawingBitmapToPaintBox(self):
        drawSelectionRects = false
        drawBoundingRects = false
        includePlant = false
        i = 0
        plant = PdPlant()
        aRect = TRect()
        insetOneRect = TRect()
        intersection = TRect()
        intersectResult = longbool()
        oldPalette = HPALETTE()
        
        if delphi_compatability.Application.terminated:
            return
        if (udomain.domain == None) or (self.plants == None):
            return
        aRect = Rect(0, 0, self.drawingBitmap.Width, self.drawingBitmap.Height)
        # use an inset rect to avoid flicker in the boundary rectangle
        insetOneRect = Rect(1, 1, self.drawingBitmap.Width - 1, self.drawingBitmap.Height - 1)
        oldPalette = 0
        oldPalette = UNRESOLVED.selectPalette(self.drawingPaintBox.Canvas.Handle, MainForm.paletteImage.Picture.Bitmap.Palette, false)
        UNRESOLVED.realizePalette(self.drawingPaintBox.Canvas.Handle)
        self.drawingPaintBox.Canvas.CopyRect(insetOneRect, self.drawingBitmap.Canvas, insetOneRect)
        self.drawingPaintBox.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.drawingPaintBox.Canvas.Pen.Width = 1
        drawBoundingRects = (udomain.domain.options.showBoundsRectangle) and (not udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) and (not udomain.domain.temporarilyHideSelectionRectangles)
        if (drawBoundingRects) and (self.plants.Count > 0):
            self.drawingPaintBox.Canvas.Pen.Color = delphi_compatability.clSilver
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if not plant.hidden:
                    self.drawingPaintBox.Canvas.Rectangle(plant.boundsRect_pixels().Left, plant.boundsRect_pixels().Top, plant.boundsRect_pixels().Right, plant.boundsRect_pixels().Bottom)
        drawSelectionRects = (udomain.domain.options.showSelectionRectangle) and (not udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) and (not udomain.domain.temporarilyHideSelectionRectangles)
        if (drawSelectionRects) and (self.plants.Count > 0):
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                includePlant = false
                intersectResult = delphi_compatability.IntersectRect(intersection, plant.boundsRect_pixels(), aRect)
                includePlant = includePlant or intersectResult
                includePlant = includePlant and not plant.hidden
                if not includePlant:
                    continue
                if self.isFocused(plant):
                    self.drawingPaintBox.Canvas.Pen.Color = udomain.domain.options.firstSelectionRectangleColor
                    self.drawingPaintBox.Canvas.Rectangle(plant.boundsRect_pixels().Left, plant.boundsRect_pixels().Top, plant.boundsRect_pixels().Right, plant.boundsRect_pixels().Bottom)
                    if self.cursorModeForDrawing == kCursorModeSelectDrag:
                        self.drawingPaintBox.Canvas.Brush.Color = self.drawingPaintBox.Canvas.Pen.Color
                        self.drawingPaintBox.Canvas.Rectangle(plant.resizingRect().Left, plant.resizingRect().Top, plant.resizingRect().Right, plant.resizingRect().Bottom)
                        self.drawingPaintBox.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
                elif self.isSelected(plant):
                    self.drawingPaintBox.Canvas.Pen.Color = udomain.domain.options.multiSelectionRectangleColor
                    self.drawingPaintBox.Canvas.Rectangle(plant.boundsRect_pixels().Left, plant.boundsRect_pixels().Top, plant.boundsRect_pixels().Right, plant.boundsRect_pixels().Bottom)
        self.drawingPaintBox.Canvas.Pen.Color = UNRESOLVED.clBtnText
        self.drawingPaintBox.Canvas.Rectangle(0, 0, self.drawingPaintBox.Width, self.drawingPaintBox.Height)
        UNRESOLVED.selectPalette(self.drawingPaintBox.Canvas.Handle, oldPalette, true)
        UNRESOLVED.realizePalette(self.drawingPaintBox.Canvas.Handle)
    
    # plant bitmaps
    # ---------------------------------------------------------------------------- *bitmaps for plants 
    def screenBytesPerPixel(self):
        result = 0.0
        screenDC = HDC()
        
        screenDC = UNRESOLVED.GetDC(0)
        try:
            result = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES))
            result = result / 8.0
        finally:
            UNRESOLVED.ReleaseDC(0, screenDC)
        return result
    
    def bytesInPlantBitmaps(self, plantToExclude):
        result = 0L
        bytesInBitmap = 0L
        bytesPerPixel = 0.0
        i = 0
        plant = PdPlant()
        
        result = 0
        bytesPerPixel = self.screenBytesPerPixel()
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if plant.hidden:
                    continue
                if plant == plantToExclude:
                    # plant that is asking should not be counted, since it is looking to resize and lose the old size
                    continue
                bytesInBitmap = intround(plant.previewCache.Width * plant.previewCache.Height * bytesPerPixel)
                result = result + bytesInBitmap
        return result
    
    def roomForPlantBitmap(self, plant, bytesForThisPlant):
        result = false
        bytesAlreadyNotIncludingThisPlant = 0L
        bytesLimit = 0L
        megabytesTried = 0.0
        
        bytesAlreadyNotIncludingThisPlant = self.bytesInPlantBitmaps(plant)
        bytesLimit = udomain.domain.options.memoryLimitForPlantBitmaps_MB * 1024 * 1024
        result = bytesAlreadyNotIncludingThisPlant + bytesForThisPlant < bytesLimit
        if not result:
            megabytesTried = (bytesAlreadyNotIncludingThisPlant + bytesForThisPlant) / (1024 * 1024)
            ShowMessage("The total size of plant bitmaps (" + FloatToStrF(megabytesTried, UNRESOLVED.ffFixed, 7, 1) + ") has exceeded " + "the memory limit of " + IntToStr(udomain.domain.options.memoryLimitForPlantBitmaps_MB) + " megabytes." + chr(13) + "All plant bitmaps have been dropped and plants will be drawn directly on the window." + chr(13) + "To use plant bitmaps again, choose Use Plant Bitmaps from the Options menu." + chr(13) + chr(13) + "If you have more free memory, your memory limit is set too low." + chr(13) + "To increase the memory limit, choose Preferences from the Edit menu." + chr(13) + "Click Help in the Preferences window for details.")
            self.stopUsingPlantBitmaps()
        return result
    
    def exceptionResizingPlantBitmap(self):
        ShowMessage("An exception occurred while resizing a plant bitmap. " + chr(13) + "All plant bitmaps have been dropped and plants will be drawn directly on the window." + chr(13) + "To use plant bitmaps again, choose Use Plant Bitmaps from the Options menu." + chr(13) + chr(13) + "This exception means that your memory limit is set too high for the available memory." + chr(13) + "To decrease the memory limit, choose Preferences from the Edit menu." + chr(13) + "Click Help in the Preferences window for details.")
        self.stopUsingPlantBitmaps()
    
    def updateForChangeToPlantBitmaps(self):
        aString = ""
        bytesInUse = 0L
        megabytesInUse = 0.0
        
        if udomain.domain.options.showLongHintsForButtons:
            aString = "Plant bitmaps are used to speed up drawing by caching each plant into a separate " + "bitmap in memory. Plant bitmaps are turned "
        else:
            aString = "Plant bitmaps are turned "
        bytesInUse = 0
        megabytesInUse = 0
        if udomain.domain.options.cachePlantBitmaps:
            bytesInUse = self.bytesInPlantBitmaps(None)
            megabytesInUse = bytesInUse / (1024 * 1024)
            aString = aString + "ON and are using " + FloatToStrF(megabytesInUse, UNRESOLVED.ffFixed, 7, 1) + " out of " + IntToStr(udomain.domain.options.memoryLimitForPlantBitmaps_MB) + " MB of memory."
        else:
            aString = aString + "OFF."
        if udomain.domain.options.showLongHintsForButtons:
            if not udomain.domain.options.cachePlantBitmaps:
                aString = aString + " You can turn plant bitmaps on using the Options menu."
            else:
                aString = aString + " You can change the amount of memory dedicated to plant bitmaps in the Preferences window."
        if self.plantBitmapsIndicatorImage != None:
            if udomain.domain.options.cachePlantBitmaps:
                if megabytesInUse / udomain.domain.options.memoryLimitForPlantBitmaps_MB <= 0.5:
                    self.plantBitmapsIndicatorImage.Picture = self.plantBitmapsGreenImage.Picture
                elif megabytesInUse / udomain.domain.options.memoryLimitForPlantBitmaps_MB <= 0.8:
                    self.plantBitmapsIndicatorImage.Picture = self.plantBitmapsYellowImage.Picture
                else:
                    self.plantBitmapsIndicatorImage.Picture = self.plantBitmapsRedImage.Picture
            else:
                self.plantBitmapsIndicatorImage.Picture = self.noPlantBitmapsImage.Picture
            self.plantBitmapsIndicatorImage.Hint = aString
    
    def stopUsingPlantBitmaps(self):
        udomain.domain.options.cachePlantBitmaps = false
        self.MenuOptionsUsePlantBitmaps.checked = udomain.domain.options.cachePlantBitmaps
        self.shrinkAllPlantBitmaps()
        self.invalidateEntireDrawing()
    
    def startUsingPlantBitmaps(self):
        udomain.domain.options.cachePlantBitmaps = true
        self.MenuOptionsUsePlantBitmaps.checked = udomain.domain.options.cachePlantBitmaps
        self.recalculateAllPlantBoundsRects(kDrawNow)
        self.invalidateEntireDrawing()
    
    # command list management 
    # ---------------------------------------------------------------------------- *command list management 
    def clearCommandList(self):
        self.commandList.free
        self.commandList = None
        self.commandList = ucommand.PdCommandList().create()
        self.updateMenusForUndoRedo()
    
    def doCommand(self, command):
        self.commandList.doCommand(command)
        self.updateForPossibleChangeToDrawing()
    
    # called by commands 
    # ------------------------------------------------------------------------------- *called by commands 
    def hideOrShowSomePlants(self, plantList, hideList, hide, drawNow):
        redrawRect = TRect()
        i = 0
        plant = PdPlant()
        
        if (plantList == None) or (plantList.Count <= 0):
            return
        redrawRect = delphi_compatability.Bounds(0, 0, 0, 0)
        for i in range(0, plantList.Count):
            plant = uplant.PdPlant(plantList.Items[i])
            if (hideList != None) and (hideList.Count > 0):
                plant.hidden = updcom.PdBooleanValue(hideList.Items[i]).saveBoolean
            else:
                plant.hidden = hide
            # magnification might have changed
            plant.recalculateBounds(kDrawNow)
            delphi_compatability.UnionRect(redrawRect, redrawRect, plant.boundsRect_pixels())
        self.invalidateDrawingRect(redrawRect)
        self.plantListDrawGrid.Invalidate()
        if drawNow:
            self.updateForPossibleChangeToDrawing()
    
    def fitVisiblePlantsInDrawingArea(self, drawNow, scaleAsWellAsMove, alwaysMove):
        upperLeft_mm = TPoint()
        lowerRight_mm = TPoint()
        size_mm = TPoint()
        offScreenUpperLeft_mm = TPoint()
        offScreenLowerRight_mm = TPoint()
        xScale_pixelsPerMm = 0.0
        yScale_pixelsPerMm = 0.0
        newScale_pixelsPerMm = 0.0
        marginOffset_mm = 0.0
        i = 0
        plant = PdPlant()
        allPlantsAreOffscreen = false
        
        if self.plants.Count <= 0:
            return
        for i in range(0, self.plants.Count):
            plant = uplant.PdPlant(self.plants.Items[i])
            if not plant.hidden:
                plant.recalculateBounds(kDontDrawYet)
        upperLeft_mm = self.upperLeftMostPlantBoundsRectPoint_mm()
        lowerRight_mm = self.lowerRightMostPlantBoundsRectPoint_mm()
        size_mm = Point(lowerRight_mm.X - upperLeft_mm.X, lowerRight_mm.Y - upperLeft_mm.Y)
        if alwaysMove:
            # move domain offset so all plants begin within drawing area
            allPlantsAreOffscreen = false
        else:
            # determine if all plants are out of the drawing area and so must be moved
            offScreenUpperLeft_mm.X = intround(kOffscreenMargin / udomain.domain.plantManager.plantDrawScale_PixelsPerMm)
            offScreenUpperLeft_mm.Y = intround(kOffscreenMargin / udomain.domain.plantManager.plantDrawScale_PixelsPerMm)
            offScreenLowerRight_mm.X = intround((self.drawingPaintBox.Width - kOffscreenMargin) / udomain.domain.plantManager.plantDrawScale_PixelsPerMm)
            offScreenLowerRight_mm.Y = intround((self.drawingPaintBox.Height - kOffscreenMargin) / udomain.domain.plantManager.plantDrawScale_PixelsPerMm)
            allPlantsAreOffscreen = (lowerRight_mm.X <= offScreenUpperLeft_mm.X) or (lowerRight_mm.Y <= offScreenUpperLeft_mm.Y) or (upperLeft_mm.X >= offScreenLowerRight_mm.X) or (upperLeft_mm.Y >= offScreenLowerRight_mm.Y)
        if scaleAsWellAsMove:
            xScale_pixelsPerMm = umath.safedivExcept(1.0 * self.drawingPaintBox.Width - 1.0 * kScaleToFitMargin * 2, size_mm.X, 0)
            yScale_pixelsPerMm = umath.safedivExcept(1.0 * self.drawingPaintBox.Height - 1.0 * kScaleToFitMargin * 2, size_mm.Y, 0)
            newScale_pixelsPerMm = umath.min(xScale_pixelsPerMm, yScale_pixelsPerMm)
        else:
            newScale_pixelsPerMm = 0
        if alwaysMove or allPlantsAreOffscreen:
            marginOffset_mm = umath.safedivExcept(1.0 * kScaleToFitMargin, newScale_pixelsPerMm, 0)
            udomain.domain.plantManager.plantDrawOffset_mm = usupport.setSinglePoint(-upperLeft_mm.X + marginOffset_mm, -upperLeft_mm.Y + marginOffset_mm)
        if (scaleAsWellAsMove) and (newScale_pixelsPerMm != 0.0):
            # calculate new scale to fit all plants in drawing area and apply
            self.magnifyOrReduce(newScale_pixelsPerMm, Point(0, 0), drawNow)
    
    # ------------------------------------------------------------------------------- *selected plants list 
    def selectPlantAtPoint(self, aPoint, shift):
        newCommand = PdCommand()
        newList = TList()
        plant = PdPlant()
        i = 0
        
        plant = udomain.domain.plantManager.findPlantAtPoint(aPoint)
        newList = delphi_compatability.TList().Create()
        try:
            if (shift) and (self.selectedPlants.Count > 0):
                for i in range(0, self.selectedPlants.Count):
                    newList.Add(self.selectedPlants.Items[i])
            if newList.IndexOf(plant) >= 0:
                newList.Remove(plant)
            elif plant != None:
                newList.Add(plant)
            if not self.twoListsAreIdentical(self.selectedPlants, newList):
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(self.selectedPlants, newList)
                self.doCommand(newCommand)
        finally:
            newList.free
    
    def selectPlantAtIndex(self, Shift, index):
        newCommand = PdCommand()
        newList = TList()
        i = 0
        plant = PdPlant()
        
        if delphi_compatability.Application.terminated:
            return
        if self.plants.Count <= 0:
            return
        if (index < 0):
            if self.selectedPlants.Count <= 0:
                return
            newList = delphi_compatability.TList().Create()
            try:
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(self.selectedPlants, newList)
                self.doCommand(newCommand)
            finally:
                newList.free
            return
        plant = uplant.PdPlant(self.plants.Items[index])
        if plant == None:
            return
        newList = delphi_compatability.TList().Create()
        try:
            if (delphi_compatability.TShiftStateEnum.ssCtrl in Shift):
                if self.selectedPlants.Count > 0:
                    for i in range(0, self.selectedPlants.Count):
                        newList.Add(self.selectedPlants.Items[i])
                if newList.IndexOf(plant) >= 0:
                    newList.Remove(plant)
                else:
                    newList.Add(plant)
            elif (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                if self.selectedPlants.Count > 0:
                    for i in range(0, self.selectedPlants.Count):
                        newList.Add(self.selectedPlants.Items[i])
                if (self.lastSingleClickPlantIndex >= 0) and (self.lastSingleClickPlantIndex <= self.plants.Count - 1) and (self.lastSingleClickPlantIndex != index):
                    if self.lastSingleClickPlantIndex < index:
                        for i in range(self.lastSingleClickPlantIndex, index + 1):
                            if newList.IndexOf(self.plants.Items[i]) < 0:
                                newList.Add(self.plants.Items[i])
                    elif self.lastSingleClickPlantIndex > index:
                        for i in range(self.lastSingleClickPlantIndex, index + 1):
                            if newList.IndexOf(self.plants.Items[i]) < 0:
                                newList.Add(self.plants.Items[i])
            else:
                if self.isSelected(plant):
                    if self.selectedPlants.Count > 0:
                        for i in range(0, self.selectedPlants.Count):
                            newList.Add(self.selectedPlants.Items[i])
                else:
                    newList.Add(plant)
                    self.lastSingleClickPlantIndex = index
            if not self.twoListsAreIdentical(self.selectedPlants, newList):
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(self.selectedPlants, newList)
                self.doCommand(newCommand)
        finally:
            newList.free
    
    def twoListsAreIdentical(self, firstList, secondList):
        result = false
        i = 0L
        
        result = false
        if (firstList == None) or (secondList == None):
            return result
        if firstList.Count != secondList.Count:
            return result
        if firstList.Count <= 0:
            return result
        for i in range(0, firstList.Count):
            if firstList.Items[i] != secondList.Items[i]:
                return result
        result = true
        return result
    
    def deselectAllPlants(self):
        self.selectedPlants.Clear()
        self.updateForChangeToPlantSelections()
    
    def deselectAllPlantsButFirst(self):
        firstPlant = PdPlant()
        
        if self.selectedPlants.Count <= 0:
            return
        firstPlant = self.focusedPlant()
        self.selectedPlants.Clear()
        self.selectedPlants.Add(firstPlant)
        self.updateForChangeToPlantSelections()
    
    def selectFirstPlantInPlantList(self):
        if self.plants.Count <= 0:
            return
        self.selectedPlants.Clear()
        self.selectedPlants.Add(self.plants.Items[0])
        self.updateForChangeToPlantSelections()
    
    def showOnePlantExclusively(self, drawNow):
        booleansList = TListCollection()
        i = 0
        plant = PdPlant()
        firstPlant = PdPlant()
        
        booleansList = None
        firstPlant = self.focusedPlant()
        try:
            ucursor.cursor_startWait()
            booleansList = ucollect.TListCollection().Create()
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if plant != None:
                    booleansList.Add(updcom.PdBooleanValue().createWithBoolean(not (plant == firstPlant)))
            self.hideOrShowSomePlants(self.plants, booleansList, false, kDontDrawYet)
            self.fitVisiblePlantsInDrawingArea(kDontDrawYet, kScaleAndMove, kAlwaysMove)
            if firstPlant != None:
                # must draw now because bitmap could be wrong
                firstPlant.recalculateBounds(kDrawNow)
                self.invalidateDrawingRect(firstPlant.boundsRect_pixels())
            if drawNow:
                self.updateForPossibleChangeToDrawing()
        finally:
            booleansList.free
            ucursor.cursor_stopWait()
    
    def redrawFocusedPlantOnly(self, drawNow):
        firstPlant = PdPlant()
        
        firstPlant = self.focusedPlant()
        if firstPlant != None:
            firstPlant.recalculateBounds(kDrawNow)
            self.invalidateDrawingRect(firstPlant.boundsRect_pixels())
        if drawNow:
            self.updateForPossibleChangeToDrawing()
    
    def addSelectedPlant(self, aPlant, insertIndex):
        if (insertIndex >= 0) and (insertIndex <= self.selectedPlants.Count - 1):
            self.selectedPlants.Insert(insertIndex, aPlant)
        else:
            self.selectedPlants.Add(aPlant)
        self.invalidateDrawingRect(aPlant.boundsRect_pixels())
    
    def removeSelectedPlant(self, aPlant):
        self.invalidateDrawingRect(aPlant.boundsRect_pixels())
        self.selectedPlants.Remove(aPlant)
    
    def isSelected(self, plant):
        result = false
        result = false
        if (self.selectedPlants == None) or (self.selectedPlants.Count <= 0):
            return result
        result = self.selectedPlants.IndexOf(plant) >= 0
        return result
    
    def isFocused(self, plant):
        result = false
        result = false
        if plant == None:
            return result
        if (self.selectedPlants == None) or (self.selectedPlants.Count <= 0):
            return result
        result = self.selectedPlants.IndexOf(plant) == 0
        return result
    
    # selected plants list 
    def focusedPlant(self):
        result = PdPlant()
        result = None
        if self.selectedPlants.Count > 0:
            result = uplant.PdPlant(self.selectedPlants.Items[0])
        return result
    
    def focusedPlantIndex(self):
        result = 0
        result = -1
        if self.selectedPlants.Count > 0:
            result = self.plants.IndexOf(uplant.PdPlant(self.selectedPlants.Items[0]))
        return result
    
    def firstUnfocusedPlant(self):
        result = PdPlant()
        result = None
        if self.selectedPlants.Count > 1:
            result = uplant.PdPlant(self.selectedPlants.Items[1])
        return result
    
    def firstSelectedPlantInList(self):
        result = PdPlant()
        i = 0
        plant = PdPlant()
        
        result = None
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if self.isSelected(plant):
                    result = plant
                    return result
        return result
    
    def lastSelectedPlantInList(self):
        result = PdPlant()
        i = 0
        plant = PdPlant()
        
        result = None
        if self.plants.Count > 0:
            for i in range(self.plants.Count - 1, 0 + 1):
                plant = uplant.PdPlant(self.plants.Items[i])
                if self.isSelected(plant):
                    result = plant
                    return result
        return result
    
    # ------------------------------------------------------------------------------------- *list of plants 
    def plantListDrawGridDrawCell(self, Sender, Col, Row, Rect, State):
        plant = PdPlant()
        selected = false
        visibleRect = TRect()
        remainderRect = TRect()
        cText = [0] * (range(0, 255 + 1) + 1)
        
        if delphi_compatability.Application.terminated:
            return
        self.plantListDrawGrid.Canvas.Brush.Color = self.plantListDrawGrid.Color
        self.plantListDrawGrid.Canvas.FillRect(Rect)
        if (self.plants.Count <= 0) or (Row < 0) or (Row > self.plants.Count - 1):
            return
        # set up plant pointer 
        plant = uplant.PdPlant(self.plants.Items[Row])
        if plant == None:
            return
        selected = self.isSelected(plant)
        # set up rectangles 
        visibleRect = Rect
        visibleRect.Right = visibleRect.Left + self.plantListDrawGrid.DefaultRowHeight
        remainderRect = Rect
        remainderRect.Left = remainderRect.Left + usupport.rWidth(visibleRect)
        # fill first box with white, rest with clHighlight if selected 
        self.plantListDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        self.plantListDrawGrid.Canvas.Brush.Color = self.plantListDrawGrid.Color
        self.plantListDrawGrid.Canvas.FillRect(visibleRect)
        if not plant.hidden:
            self.plantListDrawGrid.Canvas.Draw(visibleRect.Left + (visibleRect.Right - visibleRect.Left) / 2 - self.visibleBitmap.Picture.Bitmap.Width / 2, Rect.top, self.visibleBitmap.Picture.Bitmap)
        self.plantListDrawGrid.Canvas.Font = self.plantListDrawGrid.Font
        if selected:
            self.plantListDrawGrid.Canvas.Brush.Color = UNRESOLVED.clHighlight
            self.plantListDrawGrid.Canvas.Font.Color = UNRESOLVED.clHighlightText
        else:
            self.plantListDrawGrid.Canvas.Brush.Color = self.plantListDrawGrid.Color
            self.plantListDrawGrid.Canvas.Font.Color = UNRESOLVED.clBtnText
        self.plantListDrawGrid.Canvas.FillRect(remainderRect)
        UNRESOLVED.strPCopy(cText, plant.getName())
        # margin for text 
        remainderRect.Left = remainderRect.Left + 5
        UNRESOLVED.winprocs.drawText(self.plantListDrawGrid.Canvas.Handle, cText, len(cText), remainderRect, delphi_compatability.DT_LEFT)
        if plant == self.focusedPlant():
            UNRESOLVED.drawFocusRect(Rect)
    
    def plantListDrawGridMouseDown(self, Sender, Button, Shift, X, Y):
        col = 0
        row = 0
        plant = PdPlant()
        hideList = TList()
        newCommand = PdCommand()
        
        if self.plants.Count <= 0:
            return
        if Button == delphi_compatability.TMouseButton.mbRight:
            return
        if self.justDoubleClickedOnDrawGrid:
            self.justDoubleClickedOnDrawGrid = false
            return
        else:
            self.justDoubleClickedOnDrawGrid = false
        col, row = self.plantListDrawGrid.MouseToCell(X, Y, col, row)
        # does updating in command
        self.selectPlantAtIndex(Shift, row)
        if (X <= 16) and (row >= 0) and (row <= self.plants.Count - 1):
            plant = uplant.PdPlant(self.plants.Items[row])
            if plant == None:
                return
            hideList = delphi_compatability.TList().Create()
            try:
                hideList.Add(plant)
                newCommand = updcom.PdHideOrShowCommand().createWithListOfPlantsAndHideOrShow(hideList, not plant.hidden)
                self.doCommand(newCommand)
            finally:
                hideList.free
        if X > 16:
            self.plantListDrawGrid.BeginDrag(false)
    
    def plantListDrawGridMouseUp(self, Sender, Button, Shift, X, Y):
        popupPositionInScreenCoords = TPoint()
        
        if Button == delphi_compatability.TMouseButton.mbRight:
            popupPositionInScreenCoords = self.plantListDrawGrid.ClientToScreen(Point(X, Y))
            self.PlantPopupMenu.popup(popupPositionInScreenCoords.X, popupPositionInScreenCoords.Y)
    
    def plantListDrawGridDragOver(self, Sender, Source, X, Y, State, Accept):
        Accept = (Source != None) and (Sender != None) and ((ubreedr.BreederForm != None) and (Source == ubreedr.BreederForm.plantsDrawGrid) or (utimeser.TimeSeriesForm != None) and (Source == utimeser.TimeSeriesForm.grid))
        return Accept
    
    def plantListDrawGridEndDrag(self, Sender, Target, X, Y):
        if delphi_compatability.Application.terminated:
            return
        if (Target != None) and (Target.__class__ is delphi_compatability.TDrawGrid):
            if self.focusedPlant() != None:
                if ((Target as delphi_compatability.TDrawGrid).Owner.__class__ is ubreedr.TBreederForm):
                    ubreedr.BreederForm.copyPlantToPoint(self.focusedPlant(), X, Y)
                elif ((Target as delphi_compatability.TDrawGrid).Owner.__class__ is utimeser.TTimeSeriesForm):
                    utimeser.TimeSeriesForm.copyPlantToPoint(self.focusedPlant(), X, Y)
    
    def plantListDrawGridDblClick(self, Sender):
        self.MenuPlantRenameClick(self)
        self.plantListDrawGrid.endDrag(false)
        self.justDoubleClickedOnDrawGrid = true
    
    # list box 
    def moveSelectedPlantsUp(self):
        i = 0
        plant = PdPlant()
        
        if self.plants.Count > 1:
            # start at 1 because you can't move first one up any more 
            i = 1
            while i <= self.plants.Count - 1:
                plant = uplant.PdPlant(self.plants.Items[i])
                if self.isSelected(plant):
                    self.plants.Move(i, i - 1)
                i += 1
        self.invalidateSelectedPlantRectangles()
        self.updateForPossibleChangeToDrawing()
        self.plantListDrawGrid.Invalidate()
    
    def moveSelectedPlantsDown(self):
        i = 0
        plant = PdPlant()
        
        if self.plants.Count > 1:
            # start at next to last one because you can't move last one down any more 
            i = self.plants.Count - 2
            while i >= 0:
                plant = uplant.PdPlant(self.plants.Items[i])
                if self.isSelected(plant):
                    self.plants.Move(i, i + 1)
                i -= 1
        self.invalidateSelectedPlantRectangles()
        self.updateForPossibleChangeToDrawing()
        self.plantListDrawGrid.Invalidate()
    
    def plantListDrawGridKeyDown(self, Sender, Key, Shift):
        if Key == delphi_compatability.VK_DOWN:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.MenuLayoutSendBackClick(self)
            else:
                Key = 0
                self.moveUpOrDownWithKeyInPlantList(self.focusedPlantIndex() + 1)
        elif Key == delphi_compatability.VK_RIGHT:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.MenuLayoutSendBackClick(self)
            else:
                Key = 0
                self.moveUpOrDownWithKeyInPlantList(self.focusedPlantIndex() + 1)
        elif Key == delphi_compatability.VK_UP:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.MenuLayoutBringForwardClick(self)
            else:
                Key = 0
                self.moveUpOrDownWithKeyInPlantList(self.focusedPlantIndex() - 1)
        elif Key == delphi_compatability.VK_LEFT:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.MenuLayoutBringForwardClick(self)
            else:
                Key = 0
                self.moveUpOrDownWithKeyInPlantList(self.focusedPlantIndex() - 1)
        elif Key == delphi_compatability.VK_RETURN:
            Key = 0
            self.MenuPlantRenameClick(self)
        return Key
    
    # mouse handling in drawing 
    # -------------------------------------------------------------------------- *mouse handling in drawing 
    def PaintBoxMouseDown(self, Sender, Button, Shift, X, Y):
        newCommand = PdCommand()
        anchorPoint = TPoint()
        plantClickedOn = PdPlant()
        
        if delphi_compatability.Application.terminated:
            return
        if self.plants.Count <= 0:
            return
        if self.actionInProgress:
            try:
                # error somewhere - user did weird things with mouse buttons - teminate action...
                self.PaintBoxMouseUp(Sender, Button, Shift, X, Y)
            finally:
                self.actionInProgress = false
        if self.cursorModeForDrawing == kCursorModeSelectDrag:
            if Button == delphi_compatability.TMouseButton.mbRight:
                return
            plantClickedOn = None
            plantClickedOn = udomain.domain.plantManager.findPlantAtPoint(Point(X, Y))
            if plantClickedOn == None:
                if udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
                    return
                self.rubberBanding = true
                self.rubberBandStartDragPoint = Point(X, Y)
                self.rubberBandLastDrawPoint = Point(X, Y)
                self.rubberBandNeedToRedraw = true
                # select command made in mouse up
                return
            else:
                self.actionInProgress = true
                if (not plantClickedOn.pointIsInResizingRect(Point(X, Y))) and ((not self.isSelected(plantClickedOn)) or (delphi_compatability.TShiftStateEnum.ssShift in Shift)):
                    self.selectPlantAtPoint(Point(X, Y), (delphi_compatability.TShiftStateEnum.ssShift in Shift) and (not (delphi_compatability.TShiftStateEnum.ssCtrl in Shift)))
                    self.updateForPossibleChangeToDrawing()
        elif self.cursorModeForDrawing == kCursorModeScroll:
            pass
        elif self.cursorModeForDrawing == kCursorModeMagnify:
            self.rubberBanding = true
            self.rubberBandStartDragPoint = Point(X, Y)
            self.rubberBandLastDrawPoint = Point(X, Y)
            self.rubberBandNeedToRedraw = true
        elif self.cursorModeForDrawing == kCursorModeRotate:
            pass
        elif self.cursorModeForDrawing == kCursorModePosingSelect:
            if udomain.domain.options.drawSpeed != udomain.kDrawBest:
                if MessageDialog("To pose a plant, you need the \"Draw Using\" option set to \"Solids.\"" + chr(13) + chr(13) + "Do you want to change it?", mtConfirmation, [mbYes, mbNo, ], 0) == delphi_compatability.IDYES:
                    self.MenuOptionsBestDrawClick(self)
                return
            if self.tabSet.tabIndex != kTabPosing:
                self.tabSet.tabIndex = kTabPosing
            plantClickedOn = None
            plantClickedOn = udomain.domain.plantManager.findPlantAtPoint(Point(X, Y))
            if self.isFocused(plantClickedOn):
                self.mouseDownSelectedPlantPartID, self.mouseDownSelectedPlantPartType = plantClickedOn.getInfoForPlantPartAtPoint(Point(X, Y), self.mouseDownSelectedPlantPartID, self.mouseDownSelectedPlantPartType)
            else:
                self.mouseDownSelectedPlantPartID = -1
            if self.mouseDownSelectedPlantPartID == self.selectedPlantPartID:
                return
        anchorPoint = Point(X, Y)
        # makes shift-click work as right-click
        self.commandList.rightButtonDown = (Button == delphi_compatability.TMouseButton.mbRight) or (delphi_compatability.TShiftStateEnum.ssShift in Shift)
        newCommand = self.makeMouseCommand(anchorPoint, Shift)
        if newCommand != None:
            self.actionInProgress = self.commandList.mouseDown(newCommand, anchorPoint)
        else:
            self.actionInProgress = false
        if self.actionInProgress:
            self.updateForPossibleChangeToDrawing()
    
    def PaintBoxMouseMove(self, Sender, Shift, X, Y):
        shouldCancelHint = false
        plantClickedOn = PdPlant()
        aRect = TRect()
        
        if delphi_compatability.Application.terminated:
            return
        if self.plants.Count <= 0:
            return
        if self.cursorModeForDrawing == kCursorModeSelectDrag:
            # show cursor that tells you you can resize plant when mouse is in resize rect, but only in select mode
            delphi_compatability.Screen.Cursor = delphi_compatability.crDefault
            plantClickedOn = udomain.domain.plantManager.findPlantAtPoint(Point(X, Y))
            if (udomain.domain.options.showSelectionRectangle) and (plantClickedOn != None) and (plantClickedOn == self.focusedPlant()) and (plantClickedOn.pointIsInResizingRect(Point(X, Y))):
                delphi_compatability.Screen.Cursor = delphi_compatability.crSizeNS
        if not self.actionInProgress:
            # show hint for plant mouse is over
            shouldCancelHint = false
            if self.hintActive and ((X < self.hintX - kHintRange) or (X > self.hintX + kHintRange) or (Y < self.hintY - kHintRange) or (Y > self.hintY + kHintRange)):
                if self.hintForPlantAtPoint(Point(X, Y)) != self.lastHintString:
                    shouldCancelHint = true
                if self.actionInProgress:
                    shouldCancelHint = true
                if ((X < self.hintX - kMaxHintRangeForLargeAreas) or (X > self.hintX + kMaxHintRangeForLargeAreas) or (Y < self.hintY - kMaxHintRangeForLargeAreas) or (Y > self.hintY + kMaxHintRangeForLargeAreas)):
                    shouldCancelHint = true
                if shouldCancelHint:
                    delphi_compatability.Application.CancelHint()
                    self.hintActive = false
        if self.rubberBanding:
            # continue rubber banding - could be done in either select or magnify mode
            self.undrawRubberBandBox()
            self.drawRubberBandBox(Point(X, Y))
            return
        if self.actionInProgress:
            # continue action started in mouse down
            self.commandList.mouseMove(Point(X, Y))
            if self.commandList.didMouseMove(Point(X, Y)):
                self.mouseMoveActionInProgress = true
            self.updateForPossibleChangeToDrawing()
    
    def PaintBoxMouseUp(self, Sender, Button, Shift, X, Y):
        popupPositionInScreenCoords = TPoint()
        
        if delphi_compatability.Application.terminated:
            return
        if self.plants.Count <= 0:
            return
        if (Button == delphi_compatability.TMouseButton.mbRight) and (self.cursorModeForDrawing == kCursorModeSelectDrag):
            # show popup menu but only if in select/drag mode
            popupPositionInScreenCoords = self.ClientToScreen(Point(X, Y))
            self.PlantPopupMenu.popup(popupPositionInScreenCoords.X, popupPositionInScreenCoords.Y)
            return
        if self.rubberBanding:
            # finish rubber banding if doing that, could be in select or magnify mode
            self.rubberBanding = false
            self.undrawRubberBandBox()
            if self.cursorModeForDrawing == kCursorModeSelectDrag:
                self.selectPlantsInRubberBandBox()
                return
        try:
            if self.actionInProgress:
                # finish action in progress
                self.commandList.mouseUp(Point(X, Y))
                self.actionInProgress = false
            self.mouseMoveActionInProgress = false
            self.updateForPossibleChangeToDrawing()
        finally:
            # clear out all mouse settings
            delphi_compatability.Screen.Cursor = delphi_compatability.crDefault
            self.mouseMoveActionInProgress = false
            self.commandList.rightButtonDown = false
            self.actionInProgress = false
    
    def PaintBoxDragOver(self, Sender, Source, X, Y, State, Accept):
        Accept = (Source != None) and (Sender != None) and ((ubreedr.BreederForm != None) and (Source == ubreedr.BreederForm.plantsDrawGrid) or (utimeser.TimeSeriesForm != None) and (Source == utimeser.TimeSeriesForm.grid))
        return Accept
    
    def PaintBoxEndDrag(self, Sender, Target, X, Y):
        plantClickedOn = PdPlant()
        
        if delphi_compatability.Application.terminated:
            return
        if (Target != None) and (Target.__class__ is delphi_compatability.TDrawGrid):
            plantClickedOn = None
            plantClickedOn = udomain.domain.plantManager.findPlantAtPoint(self.commandList.anchorPoint)
            if plantClickedOn != None:
                if ((Target as delphi_compatability.TDrawGrid).Owner.__class__ is ubreedr.TBreederForm):
                    ubreedr.BreederForm.copyPlantToPoint(plantClickedOn, X, Y)
                elif ((Target as delphi_compatability.TDrawGrid).Owner.__class__ is utimeser.TTimeSeriesForm):
                    utimeser.TimeSeriesForm.copyPlantToPoint(plantClickedOn, X, Y)
            # command undoes itself when it starts the drag 
    
    def makeMouseCommand(self, point, shift):
        result = PdCommand()
        result = None
        if self.cursorModeForDrawing == kCursorModeSelectDrag:
            if (delphi_compatability.TShiftStateEnum.ssShift in shift) and (delphi_compatability.TShiftStateEnum.ssCtrl in shift):
                result = None
                self.commandList.anchorPoint = Point
                self.drawingPaintBox.BeginDrag(true)
            elif (delphi_compatability.TShiftStateEnum.ssCtrl in shift):
                result = updcom.PdDuplicateCommand().createWithListOfPlants(self.selectedPlants)
            elif (self.focusedPlant() != None) and (self.focusedPlant().pointIsInResizingRect(Point)):
                delphi_compatability.Screen.Cursor = delphi_compatability.crSizeNS
                result = updcom.PdResizePlantsCommand().createWithListOfPlants(self.selectedPlants)
            else:
                result = updcom.PdDragCommand().createWithListOfPlants(self.selectedPlants)
        elif self.cursorModeForDrawing == kCursorModeScroll:
            result = updcom.PdScrollCommand().create()
        elif self.cursorModeForDrawing == kCursorModeMagnify:
            if (self.commandList.rightButtonDown):
                # to zoom out, can do right button or shift
                delphi_compatability.Screen.Cursor = ucursor.crMagMinus
                result = updcom.PdChangeMagnificationCommand().create()
                (result as updcom.PdChangeMagnificationCommand).shift = true
            else:
                result = updcom.PdChangeMagnificationCommand().create()
                (result as updcom.PdChangeMagnificationCommand).shift = (delphi_compatability.TShiftStateEnum.ssShift in shift)
        elif self.cursorModeForDrawing == kCursorModeRotate:
            if self.commandList.rightButtonDown:
                delphi_compatability.Screen.Cursor = delphi_compatability.crSizeWE
            result = updcom.PdRotateCommand().createWithListOfPlants(self.selectedPlants)
        elif self.cursorModeForDrawing == kCursorModePosingSelect:
            result = updcom.PdSelectPosingPartCommand().createWithPlantAndPartIDsAndTypes(self.focusedPlant(), self.mouseDownSelectedPlantPartID, self.selectedPlantPartID, self.mouseDownSelectedPlantPartType, self.selectedPlantPartType)
        return result
    
    # rubber banding 
    # ----------------------------------------------------------------------- *rubber banding 
    def selectPlantsInRubberBandBox(self):
        rubberBandRect = TRect()
        newList = TList()
        newCommand = PdCommand()
        
        newList = delphi_compatability.TList().Create()
        try:
            rubberBandRect = Rect(umath.intMin(self.rubberBandStartDragPoint.X, self.rubberBandLastDrawPoint.X), umath.intMin(self.rubberBandStartDragPoint.Y, self.rubberBandLastDrawPoint.Y), umath.intMax(self.rubberBandStartDragPoint.X, self.rubberBandLastDrawPoint.X), umath.intMax(self.rubberBandStartDragPoint.Y, self.rubberBandLastDrawPoint.Y))
            udomain.domain.plantManager.fillListWithPlantsInRectangle(rubberBandRect, newList)
            if not self.twoListsAreIdentical(self.selectedPlants, newList):
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(self.selectedPlants, newList)
                self.doCommand(newCommand)
        finally:
            newList.free
    
    def drawRubberBandBox(self, newPoint):
        self.rubberBandLastDrawPoint = newPoint
        self.drawOrUndrawRubberBandBox()
        self.rubberBandNeedToRedraw = true
    
    def undrawRubberBandBox(self):
        if not self.rubberBandNeedToRedraw:
            return
        self.drawOrUndrawRubberBandBox()
        self.rubberBandNeedToRedraw = false
    
    def drawOrUndrawRubberBandBox(self):
        theDC = HDC()
        drawRect = TRect()
        
        theDC = UNRESOLVED.getDC(0)
        drawRect = Rect(self.ClientOrigin.X + self.drawingPaintBox.Left + self.rubberBandStartDragPoint.X, self.ClientOrigin.Y + self.drawingPaintBox.Top + self.rubberBandStartDragPoint.Y, self.ClientOrigin.X + self.drawingPaintBox.Left + self.rubberBandLastDrawPoint.X, self.ClientOrigin.Y + self.drawingPaintBox.Top + self.rubberBandLastDrawPoint.Y)
        UNRESOLVED.patBlt(theDC, drawRect.Left, drawRect.Top, drawRect.Right - drawRect.Left, 1, delphi_compatability.DSTINVERT)
        UNRESOLVED.patBlt(theDC, drawRect.Right, drawRect.Top, 1, drawRect.Bottom - drawRect.Top, delphi_compatability.DSTINVERT)
        UNRESOLVED.patBlt(theDC, drawRect.Left, drawRect.Bottom, drawRect.Right - drawRect.Left, 1, delphi_compatability.DSTINVERT)
        UNRESOLVED.patBlt(theDC, drawRect.Left, drawRect.Top, 1, drawRect.Bottom - drawRect.Top, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
    
    # hint handling 
    # ------------------------------------------------------------------------------------ *hint handling 
    def DoShowHint(self, HintStr, CanShow, HintInfo):
        raise "method DoShowHint had assigned to var parameter HintStr not added to return; fixup manually"
        HintInfo.HintPos = HintInfo.HintControl.ClientToScreen(Point(HintInfo.CursorPos.X + 20, HintInfo.CursorPos.Y + 20))
        HintInfo.HintMaxWidth = 200
        if HintInfo.HintControl == self.drawingPaintBox:
            if not self.actionInProgress:
                HintStr = self.hintForPlantAtPoint(HintInfo.CursorPos)
                self.lastHintString = HintStr
                self.hintActive = true
                self.hintX = HintInfo.CursorPos.X
                self.hintY = HintInfo.CursorPos.Y
        else:
            if (udomain.domain != None) and (udomain.domain.hintManager != None):
                HintStr = udomain.domain.hintManager.hintForComponentName(HintInfo, udomain.domain.options.showLongHintsForButtons, udomain.domain.options.showHintsForParameters)
            if (HintStr == "") and (HintInfo.HintControl.ShowHint):
                HintStr = HintInfo.HintControl.Hint
        return CanShow
    
    def hintForPlantAtPoint(self, aPoint):
        result = ""
        plant = PdPlant()
        
        result = ""
        plant = None
        plant = udomain.domain.plantManager.findPlantAtPoint(aPoint)
        if plant != None:
            # v1.60 final
            result = plant.getHint(aPoint)
        if (self.cursorModeForDrawing == kCursorModeSelectDrag) and (udomain.domain.options.showLongHintsForButtons) and (udomain.domain.options.showSelectionRectangle) and (plant != None) and (plant == self.focusedPlant()) and (plant.pointIsInResizingRect(aPoint)):
            # extra hint if over resizing rect on focused plant in select/drag mode
            result = result + ": Click here and drag up or down to resize all selected plants."
        return result
    
    # -------------------------------------------------------------------------------- *popup menu commands 
    def PopupMenuCutClick(self, Sender):
        self.MenuEditCutClick(self)
    
    def PopupMenuCopyClick(self, Sender):
        self.MenuEditCopyClick(self)
    
    def PopupMenuPasteClick(self, Sender):
        self.MenuEditPasteClick(self)
    
    def PopupMenuRenameClick(self, Sender):
        self.MenuPlantRenameClick(self)
    
    def PopupMenuRandomizeClick(self, Sender):
        self.MenuPlantRandomizeClick(self)
    
    def PopupMenuHideAllOthersClick(self, Sender):
        self.MenuLayoutHideOthersClick(self)
    
    def PopupMenuBreedClick(self, Sender):
        self.MenuPlantBreedClick(self)
    
    def PopupMenuHideClick(self, Sender):
        self.MenuLayoutHideClick(self)
    
    def PopupMenuShowClick(self, Sender):
        self.MenuLayoutShowClick(self)
    
    def PopupMenuMakeTimeSeriesClick(self, Sender):
        self.MenuPlantMakeTimeSeriesClick(self)
    
    def PopupMenuZeroRotationsClick(self, Sender):
        self.MenuPlantZeroRotationsClick(self)
    
    def PopupMenuAnimateClick(self, Sender):
        self.MenuPlantAnimateClick(self)
    
    def paramPopupMenuExpandAllInSectionClick(self, Sender):
        if self.currentSection() != None:
            self.collapseOrExpandAllParameterPanelsInCurrentSection(kExpand)
    
    def paramPopupMenuCollapseAllInSectionClick(self, Sender):
        if self.currentSection() != None:
            self.collapseOrExpandAllParameterPanelsInCurrentSection(kCollapse)
    
    def sectionPopupMenuHelpClick(self, Sender):
        section = PdSection()
        helpID = ""
        
        section = self.currentSection()
        if section == None:
            return
        helpID = self.sectionHelpIDForSectionName(section.getName())
        if helpID != "":
            delphi_compatability.Application.HelpJump(helpID)
    
    # new v1.4
    def paramPopupMenuCopyNameClick(self, Sender):
        textToCopy = ""
        newText = ""
        
        if self.selectedParameterPanel == None:
            return
        if self.currentSection() != None:
            textToCopy = self.currentSection().getName() + ": "
        else:
            textToCopy = ""
        textToCopy = textToCopy + self.selectedParameterPanel.Caption
        if usupport.found("[", textToCopy):
            # v2.1 deal with orthogonal sections
            newText = usupport.stringUpTo(usupport.stringBeyond(textToCopy, "["), "]")
            newText = newText + ": " + trim(usupport.stringUpTo(usupport.stringBeyond(textToCopy, ":"), "["))
            textToCopy = newText
        UNRESOLVED.Clipboard.asText = textToCopy
    
    def paramPopupMenuHelpClick(self, Sender):
        helpID = ""
        
        helpID = self.paramHelpIDForParamPanel(self.selectedParameterPanel)
        if helpID != "":
            delphi_compatability.Application.HelpJump(helpID)
    
    def paramPopupMenuExpandClick(self, Sender):
        if self.selectedParameterPanel != None:
            self.selectedParameterPanel.expand()
            self.repositionParameterPanels()
    
    def paramPopupMenuCollapseClick(self, Sender):
        if self.selectedParameterPanel != None:
            self.selectedParameterPanel.collapse()
            self.repositionParameterPanels()
    
    # ------------------------------------------------------------------------------------ *toolbar 
    def dragCursorModeClick(self, Sender):
        self.drawingPaintBox.Cursor = delphi_compatability.crArrow
        self.cursorModeForDrawing = kCursorModeSelectDrag
        if udomain.domain.options.showSelectionRectangle:
            self.copyDrawingBitmapToPaintBox()
    
    def magnifyCursorModeClick(self, Sender):
        self.drawingPaintBox.Cursor = ucursor.crMagPlus
        self.cursorModeForDrawing = kCursorModeMagnify
        if udomain.domain.options.showSelectionRectangle:
            self.copyDrawingBitmapToPaintBox()
    
    def posingSelectionCursorModeClick(self, Sender):
        self.tabSet.tabIndex = kTabPosing
        self.drawingPaintBox.Cursor = ucursor.crPosingSelect
        self.cursorModeForDrawing = kCursorModePosingSelect
        if udomain.domain.options.showSelectionRectangle:
            self.copyDrawingBitmapToPaintBox()
    
    def scrollCursorModeClick(self, Sender):
        self.drawingPaintBox.Cursor = ucursor.crScroll
        self.cursorModeForDrawing = kCursorModeScroll
        if udomain.domain.options.showSelectionRectangle:
            self.copyDrawingBitmapToPaintBox()
    
    def rotateCursorModeClick(self, Sender):
        self.drawingPaintBox.Cursor = ucursor.crRotate
        self.cursorModeForDrawing = kCursorModeRotate
        if udomain.domain.options.showSelectionRectangle:
            self.copyDrawingBitmapToPaintBox()
    
    def centerDrawingClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = updcom.PdCenterDrawingCommand().create()
        self.doCommand(newCommand)
    
    def magnificationPercentClick(self, Sender):
        newScale = 0.0
        
        newScale = self.magnifyScaleForText(self.magnificationPercent.Text)
        if (newScale != udomain.domain.plantDrawScale_PixelsPerMm()):
            self.changeMagnificationWithoutClick()
    
    def magnificationPercentExit(self, Sender):
        newScale = 0.0
        
        newScale = self.magnifyScaleForText(self.magnificationPercent.Text)
        if (newScale != udomain.domain.plantDrawScale_PixelsPerMm()):
            self.changeMagnificationWithoutClick()
    
    def magnifyPlusClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = updcom.PdChangeMagnificationCommand().createWithNewScaleAndPoint(udomain.domain.plantDrawScale_PixelsPerMm() * 1.5, Point(self.drawingPaintBox.Width / 2, self.drawingPaintBox.Height / 2))
        self.doCommand(newCommand)
    
    def magnifyMinusClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = updcom.PdChangeMagnificationCommand().createWithNewScaleAndPoint(udomain.domain.plantDrawScale_PixelsPerMm() * 0.75, Point(self.drawingPaintBox.Width / 2, self.drawingPaintBox.Height / 2))
        self.doCommand(newCommand)
    
    # popup menu commands 
    # toolbar 
    def changeMagnificationWithoutClick(self):
        newCommand = PdCommand()
        
        newCommand = updcom.PdChangeMagnificationCommand().createWithNewScaleAndPoint(self.magnifyScaleForText(self.magnificationPercent.Text), Point(self.drawingPaintBox.Width / 2, self.drawingPaintBox.Height / 2))
        self.doCommand(newCommand)
    
    def magnifyScaleForText(self, aText):
        result = 0.0
        intResult = 0
        oldIntResult = 0
        
        result = 1.0
        try:
            oldIntResult = intround(udomain.domain.plantDrawScale_PixelsPerMm() * 100.0)
            intResult = StrToIntDef(usupport.stringUpTo(aText, "%"), -1)
            if (intResult <= 0):
                intResult = oldIntResult
                self.magnificationPercent.Text = IntToStr(intResult) + "%"
            if intResult > kMaxMagnificationToTypeIn:
                intResult = kMaxMagnificationToTypeIn
                self.magnificationPercent.Text = IntToStr(intResult) + "%"
            result = intResult / 100.0
        except:
            result = 1.0
        return result
    
    def magnifyOrReduce(self, newScale_PixelsPerMm, point_pixels, drawNow):
        result = TPoint()
        oldOffset_mm = SinglePoint()
        pointInOldScale_mm = SinglePoint()
        pointInNewScale_mm = SinglePoint()
        newOffset_mm = SinglePoint()
        oldScale_PixelsPerMm = 0.0
        
        self.recalculateAllPlantBoundsRects(kDontDrawYet)
        oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
        oldOffset_mm = udomain.domain.plantDrawOffset_mm()
        pointInOldScale_mm = usupport.setSinglePoint(intround(point_pixels.X / oldScale_PixelsPerMm), intround(point_pixels.Y / oldScale_PixelsPerMm))
        pointInNewScale_mm = usupport.setSinglePoint(intround(point_pixels.X / newScale_PixelsPerMm), intround(point_pixels.Y / newScale_PixelsPerMm))
        newOffset_mm = usupport.setSinglePoint(oldOffset_mm.x + pointInNewScale_mm.x - pointInOldScale_mm.x, oldOffset_mm.y + pointInNewScale_mm.y - pointInOldScale_mm.y)
        udomain.domain.plantManager.plantDrawScale_PixelsPerMm = intround(newScale_PixelsPerMm * 100.0) / 100.0
        udomain.domain.plantManager.plantDrawOffset_mm = newOffset_mm
        if drawNow:
            self.redrawEverything()
        self.magnificationPercent.Text = IntToStr(intround(udomain.domain.plantDrawScale_PixelsPerMm() * 100.0)) + "%"
        return result
    
    def upperLeftMostPlantBoundsRectPoint_mm(self):
        result = TPoint()
        plant = PdPlant()
        i = 0
        topLeft_mm = TPoint()
        initialized = false
        
        result = Point(0, 0)
        initialized = false
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if plant.hidden:
                    continue
                topLeft_mm.X = intround(plant.boundsRect_pixels().Left / udomain.domain.plantDrawScale_PixelsPerMm() - udomain.domain.plantDrawOffset_mm().x)
                topLeft_mm.Y = intround(plant.boundsRect_pixels().Top / udomain.domain.plantDrawScale_PixelsPerMm() - udomain.domain.plantDrawOffset_mm().y)
                if not initialized:
                    result = topLeft_mm
                    initialized = true
                else:
                    if (topLeft_mm.X < result.X):
                        result.X = topLeft_mm.X
                    if (topLeft_mm.Y < result.Y):
                        result.Y = topLeft_mm.Y
        return result
    
    def lowerRightMostPlantBoundsRectPoint_mm(self):
        result = TPoint()
        plant = PdPlant()
        i = 0
        bottomRight_mm = TPoint()
        initialized = false
        
        result = Point(0, 0)
        initialized = false
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if plant.hidden:
                    continue
                bottomRight_mm.X = intround(plant.boundsRect_pixels().Right / udomain.domain.plantDrawScale_PixelsPerMm() - udomain.domain.plantDrawOffset_mm().x)
                bottomRight_mm.Y = intround(plant.boundsRect_pixels().Bottom / udomain.domain.plantDrawScale_PixelsPerMm() - udomain.domain.plantDrawOffset_mm().y)
                if not initialized:
                    result = bottomRight_mm
                    initialized = true
                else:
                    if (bottomRight_mm.X > result.X):
                        result.X = bottomRight_mm.X
                    if (bottomRight_mm.Y > result.Y):
                        result.Y = bottomRight_mm.Y
        return result
    
    def xLocationEditExit(self, Sender):
        increment = 0
        oldXLocation = 0
        newXLocation = 0
        direction = 0
        
        if self.focusedPlant() == None:
            return
        oldXLocation = self.focusedPlant().basePoint_pixels().X
        newXLocation = StrToIntDef(self.xLocationEdit.Text, oldXLocation)
        if newXLocation != oldXLocation:
            increment = newXLocation - oldXLocation
            if increment > 0:
                direction = utdomove.kRight
            else:
                direction = utdomove.kLeft
            self.nudgeSelectedPlantsByPixelsAndDirection(increment, direction)
    
    def yLocationEditExit(self, Sender):
        increment = 0
        oldYLocation = 0
        newYLocation = 0
        direction = 0
        
        if self.focusedPlant() == None:
            return
        oldYLocation = self.focusedPlant().basePoint_pixels().Y
        newYLocation = StrToIntDef(self.yLocationEdit.Text, oldYLocation)
        if newYLocation != oldYLocation:
            increment = newYLocation - oldYLocation
            if increment > 0:
                direction = updcom.kDown
            else:
                direction = updcom.kUp
            self.nudgeSelectedPlantsByPixelsAndDirection(increment, direction)
    
    def xLocationSpinDownClick(self, Sender):
        self.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, utdomove.kLeft)
    
    def xLocationSpinUpClick(self, Sender):
        self.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, utdomove.kRight)
    
    def yLocationSpinDownClick(self, Sender):
        self.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, updcom.kUp)
    
    def yLocationSpinUpClick(self, Sender):
        self.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, updcom.kDown)
    
    def xRotationEditChange(self, Sender):
        self.checkRotationEditAgainstBounds(self.xRotationEdit)
    
    def yRotationEditChange(self, Sender):
        self.checkRotationEditAgainstBounds(self.yRotationEdit)
    
    def zRotationEditChange(self, Sender):
        self.checkRotationEditAgainstBounds(self.zRotationEdit)
    
    def checkRotationEditAgainstBounds(self, edit):
        newRotation = 0
        oldRotation = 0
        
        if self.internalChange:
            return
        newRotation = StrToIntDef(edit.Text, 0)
        oldRotation = newRotation
        if newRotation < -360:
            newRotation = 360 - (abs(newRotation) - 360)
        if newRotation > 360:
            newRotation = -360 + (newRotation - 360)
        if newRotation != oldRotation:
            self.internalChange = true
            edit.Text = IntToStr(newRotation)
            self.internalChange = false
    
    def xRotationEditExit(self, Sender):
        self.changeSelectedPlantRotations(self.xRotationEdit, updcom.kRotateX, 0)
    
    def xRotationSpinUpClick(self, Sender):
        self.changeSelectedPlantRotations(self.xRotationEdit, updcom.kRotateX, udomain.domain.options.rotationIncrement)
    
    def xRotationSpinDownClick(self, Sender):
        self.changeSelectedPlantRotations(self.xRotationEdit, updcom.kRotateX, -udomain.domain.options.rotationIncrement)
    
    def yRotationEditExit(self, Sender):
        self.changeSelectedPlantRotations(self.yRotationEdit, updcom.kRotateY, 0)
    
    def yRotationSpinUpClick(self, Sender):
        self.changeSelectedPlantRotations(self.yRotationEdit, updcom.kRotateY, udomain.domain.options.rotationIncrement)
    
    def yRotationSpinDownClick(self, Sender):
        self.changeSelectedPlantRotations(self.yRotationEdit, updcom.kRotateY, -udomain.domain.options.rotationIncrement)
    
    def zRotationEditExit(self, Sender):
        self.changeSelectedPlantRotations(self.zRotationEdit, updcom.kRotateZ, 0)
    
    def zRotationSpinUpClick(self, Sender):
        self.changeSelectedPlantRotations(self.zRotationEdit, updcom.kRotateZ, udomain.domain.options.rotationIncrement)
    
    def zRotationSpinDownClick(self, Sender):
        self.changeSelectedPlantRotations(self.zRotationEdit, updcom.kRotateZ, -udomain.domain.options.rotationIncrement)
    
    def changeSelectedPlantRotations(self, edit, rotateDirection, changeInRotation):
        newRotation = 0
        newCommand = PdCommand()
        
        if self.internalChange:
            return
        newRotation = StrToIntDef(edit.Text, 0) + changeInRotation
        edit.Text = IntToStr(newRotation)
        # need this? 
        self.checkRotationEditAgainstBounds(edit)
        # in case changed 
        newRotation = StrToIntDef(edit.Text, 0)
        if self.focusedPlant() == None:
            #should be disabled, but
            return
        newCommand = updcom.PdRotateCommand().createWithListOfPlantsDirectionAndNewRotation(self.selectedPlants, rotateDirection, newRotation)
        self.doCommand(newCommand)
    
    def resetRotationsClick(self, Sender):
        newCommand = PdCommand()
        i = 0
        plant = PdPlant()
        allRotationsAreZero = false
        
        if self.selectedPlants.Count <= 0:
            return
        # don't do if none of the selected plants have rotations other than zero 
        allRotationsAreZero = true
        for i in range(0, self.selectedPlants.Count):
            plant = uplant.PdPlant(self.selectedPlants.Items[i])
            if (plant.xRotation != 0) or (plant.yRotation != 0) or (plant.zRotation != 0):
                allRotationsAreZero = false
                break
        if allRotationsAreZero:
            return
        newCommand = updcom.PdResetRotationsCommand().createWithListOfPlants(self.selectedPlants)
        self.doCommand(newCommand)
    
    def drawingScaleEditExit(self, Sender):
        oldValue = 0.0
        newValue = 0.0
        
        if self.focusedPlant() == None:
            return
        oldValue = self.focusedPlant().drawingScale_PixelsPerMm
        try:
            newValue = StrToFloat(self.drawingScaleEdit.Text)
        except:
            newValue = oldValue
        if newValue != oldValue:
            self.resizeSelectedPlantsWithMultiplierOrNewAmount(0, newValue)
    
    def drawingScaleSpinUpClick(self, Sender):
        resizeMultiplier = 0.0
        
        if self.focusedPlant() == None:
            return
        resizeMultiplier = udomain.domain.options.resizeKeyUpMultiplierPercent / 100.0
        self.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0)
    
    def drawingScaleSpinDownClick(self, Sender):
        resizeMultiplier = 0.0
        
        if self.focusedPlant() == None:
            return
        resizeMultiplier = umath.safedivExcept(1.0, udomain.domain.options.resizeKeyUpMultiplierPercent / 100.0, 0.9)
        self.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0)
    
    def makeEqualWidthClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdResizePlantsToSameWidthOrHeightCommand().createWithListOfPlantsAndNewWidthOrHeight(self.selectedPlants, usupport.rWidth(self.focusedPlant().boundsRect_pixels()), 0, updcom.kChangeWidth)
        self.doCommand(newCommand)
    
    def makeEqualHeightClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdResizePlantsToSameWidthOrHeightCommand().createWithListOfPlantsAndNewWidthOrHeight(self.selectedPlants, 0, usupport.rHeight(self.focusedPlant().boundsRect_pixels()), updcom.kChangeHeight)
        self.doCommand(newCommand)
    
    def MenuLayoutSizeSameWidthClick(self, Sender):
        self.makeEqualWidthClick(self)
    
    def MenuLayoutSizeSameHeightClick(self, Sender):
        self.makeEqualHeightClick(self)
    
    def alignTopsClick(self, Sender):
        self.alignSelectedPlants(updcom.kUp)
    
    def alignBottomsClick(self, Sender):
        self.alignSelectedPlants(updcom.kDown)
    
    def alignLeftClick(self, Sender):
        self.alignSelectedPlants(utdomove.kLeft)
    
    def alignRightClick(self, Sender):
        self.alignSelectedPlants(utdomove.kRight)
    
    def alignSelectedPlants(self, alignDirection):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 1:
            return
        newCommand = updcom.PdAlignPlantsCommand().createWithListOfPlantsRectAndDirection(self.selectedPlants, self.focusedPlant().boundsRect_pixels(), alignDirection)
        self.doCommand(newCommand)
    
    def MenuLayoutAlignTopsClick(self, Sender):
        self.alignTopsClick(self)
    
    def MenuLayoutAlignBottomsClick(self, Sender):
        self.alignBottomsClick(self)
    
    def MenuLayoutAlignLeftSidesClick(self, Sender):
        self.alignLeftClick(self)
    
    def MenuLayoutAlignRightSidesClick(self, Sender):
        self.alignRightClick(self)
    
    def packPlantsClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 1:
            return
        newCommand = updcom.PdPackPlantsCommand().createWithListOfPlantsAndFocusRect(self.selectedPlants, self.focusedPlant().boundsRect_pixels())
        self.doCommand(newCommand)
    
    def MenuLayoutPackClick(self, Sender):
        self.packPlantsClick(self)
    
    def FormKeyDown(self, Sender, Key, Shift):
        if self.animateTimer.enabled:
            # pressing any key will stop animation 
            Key = 0
            self.stopAnimation()
        if (delphi_compatability.TShiftStateEnum.ssCtrl in Shift) and (delphi_compatability.TShiftStateEnum.ssShift in Shift):
            if (Key == delphi_compatability.VK_LEFT) or (Key == delphi_compatability.VK_RIGHT) or (Key == delphi_compatability.VK_UP) or (Key == delphi_compatability.VK_DOWN):
                # hold down control and shift and press arrow keys - resize current plants 
                self.resizeSelectedPlantsByKey(Key)
                Key = 0
            # hold down control and press arrow keys - shift current plants 
        elif (delphi_compatability.TShiftStateEnum.ssCtrl in Shift):
            if (Key == delphi_compatability.VK_LEFT) or (Key == delphi_compatability.VK_RIGHT) or (Key == delphi_compatability.VK_UP) or (Key == delphi_compatability.VK_DOWN):
                self.nudgeSelectedPlantsByKey(Key)
                Key = 0
            # hold down shift - do magnification as minus 
        elif (Key == delphi_compatability.VK_SHIFT):
            if self.cursorModeForDrawing == kCursorModeMagnify:
                self.drawingPaintBox.Cursor = ucursor.crMagMinus
        return Key
    
    def nudgeSelectedPlantsByKey(self, key):
        direction = 0
        
        if self.selectedPlants.Count <= 0:
            return
        if key == delphi_compatability.VK_LEFT:
            direction = utdomove.kLeft
        elif key == delphi_compatability.VK_RIGHT:
            direction = utdomove.kRight
        elif key == delphi_compatability.VK_UP:
            direction = updcom.kUp
        elif key == delphi_compatability.VK_DOWN:
            direction = updcom.kDown
        else :
            return
        self.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, direction)
    
    def nudgeSelectedPlantsByPixelsAndDirection(self, pixels, direction):
        newCommand = PdCommand()
        movePoint = TPoint()
        
        if self.selectedPlants.Count <= 0:
            return
        movePoint = Point(0, 0)
        if direction == updcom.kUp:
            movePoint.Y = -pixels
        elif direction == updcom.kDown:
            movePoint.Y = pixels
        elif direction == utdomove.kLeft:
            movePoint.X = -pixels
        elif direction == utdomove.kRight:
            movePoint.X = pixels
        newCommand = updcom.PdDragCommand().createWithListOfPlantsAndDragOffset(self.selectedPlants, movePoint)
        self.doCommand(newCommand)
    
    def resizeSelectedPlantsByKey(self, key):
        resizeMultiplier = 0.0
        
        if self.selectedPlants.Count <= 0:
            return
        if (key == delphi_compatability.VK_LEFT) or (key == delphi_compatability.VK_UP):
            resizeMultiplier = udomain.domain.options.resizeKeyUpMultiplierPercent / 100.0
        elif (key == delphi_compatability.VK_RIGHT) or (key == delphi_compatability.VK_DOWN):
            resizeMultiplier = umath.safedivExcept(1.0, udomain.domain.options.resizeKeyUpMultiplierPercent / 100.0, 0.9)
        else:
            return
        self.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0)
    
    def resizeSelectedPlantsWithMultiplierOrNewAmount(self, multiplier, newAmount_pixelsPerMm):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        if multiplier != 0:
            newCommand = updcom.PdResizePlantsCommand().createWithListOfPlantsAndMultiplier(self.selectedPlants, multiplier)
        else:
            newCommand = updcom.PdResizePlantsCommand().createWithListOfPlantsAndNewValue(self.selectedPlants, newAmount_pixelsPerMm)
        self.doCommand(newCommand)
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        if self.animateTimer.enabled:
            # pressing any key will stop animation 
            Key = chr(0)
            self.stopAnimation()
        return Key
    
    def FormKeyUp(self, Sender, Key, Shift):
        if self.animateTimer.enabled:
            # pressing any key will stop animation 
            Key = 0
            self.stopAnimation()
        if (Key == delphi_compatability.VK_SHIFT):
            if self.cursorModeForDrawing == kCursorModeMagnify:
                # let up shift or control - go back to plus magnification 
                self.drawingPaintBox.Cursor = ucursor.crMagPlus
        return Key
    
    # tab set 
    # ------------------------------------------------------------------------------------ *tab set 
    def lifeCycleShowing(self):
        result = false
        result = (self.tabSet.tabIndex == kTabLifeCycle)
        return result
    
    def rotationsShowing(self):
        result = false
        result = (self.tabSet.tabIndex == kTabRotations)
        return result
    
    def parametersShowing(self):
        result = false
        result = (self.tabSet.tabIndex == kTabParameters)
        return result
    
    def statsShowing(self):
        result = false
        result = (self.tabSet.tabIndex == kTabStatistics)
        return result
    
    def noteShowing(self):
        result = false
        result = (self.tabSet.tabIndex == kTabNote)
        return result
    
    def posingShowing(self):
        result = false
        result = (self.tabSet.tabIndex == kTabPosing)
        return result
    
    def tabSetChange(self, Sender, NewTab, AllowChange):
        self.lifeCyclePanel.Visible = (NewTab == kTabLifeCycle)
        self.rotationsPanel.Visible = (NewTab == kTabRotations)
        self.parametersPanel.Visible = (NewTab == kTabParameters)
        self.statsScrollBox.Visible = (NewTab == kTabStatistics)
        self.notePanel.Visible = (NewTab == kTabNote)
        self.posingPanel.Visible = (NewTab == kTabPosing)
        self.updateRightSidePanelForFirstSelectedPlantWithTab(NewTab)
        return AllowChange
    
    def updateRightSidePanelForFirstSelectedPlant(self):
        # set tab font colors - pay attention to multiple selections 
        # v2.0 removed this
        #  tabSet.font.color := self.textColorToRepresentPlantSelection(true);
        #  tabSet.invalidate;
        self.updateRightSidePanelForFirstSelectedPlantWithTab(self.tabSet.tabIndex)
    
    def updateRightSidePanelForFirstSelectedPlantWithTab(self, newTab):
        if newTab == kTabLifeCycle:
            self.updateLifeCyclePanelForFirstSelectedPlant()
        elif newTab == kTabRotations:
            self.updateRotationsPanelForFirstSelectedPlant()
        elif newTab == kTabParameters:
            self.updateParametersPanelForFirstSelectedPlant()
        elif newTab == kTabStatistics:
            self.updateStatisticsPanelForFirstSelectedPlant()
        elif newTab == kTabNote:
            self.updateNoteForFirstSelectedPlant()
        elif newTab == kTabPosing:
            self.updatePosingForFirstSelectedPlant()
    
    def textColorToRepresentPlantSelection(self, payAttentionToMultiSelect):
        result = TColorRef()
        if self.focusedPlant() != None:
            if payAttentionToMultiSelect:
                if self.selectedPlants.Count <= 1:
                    result = UNRESOLVED.clBtnText
                else:
                    # v2.0  was clRed
                    result = delphi_compatability.clBlue
            else:
                result = UNRESOLVED.clBtnText
        else:
            result = delphi_compatability.clGray
        return result
    
    def updateForChangeToPlantRotations(self):
        firstPlant = PdPlant()
        
        firstPlant = self.focusedPlant()
        if firstPlant != None:
            self.xRotationEdit.Text = IntToStr(intround(firstPlant.xRotation))
            self.yRotationEdit.Text = IntToStr(intround(firstPlant.yRotation))
            self.zRotationEdit.Text = IntToStr(intround(firstPlant.zRotation))
        else:
            self.xRotationEdit.Text = ""
            self.yRotationEdit.Text = ""
            self.zRotationEdit.Text = ""
        self.xRotationEdit.Refresh()
        self.yRotationEdit.Refresh()
        self.zRotationEdit.Refresh()
    
    def updateForChangeToSelectedPlantsDrawingScale(self):
        firstPlant = PdPlant()
        
        firstPlant = self.focusedPlant()
        if firstPlant != None:
            self.drawingScaleEdit.Text = usupport.digitValueString(firstPlant.drawingScale_PixelsPerMm)
        else:
            self.drawingScaleEdit.Text = ""
        self.drawingScaleEdit.Refresh()
    
    def updateForChangeToSelectedPlantsLocation(self):
        firstPlant = PdPlant()
        
        firstPlant = self.focusedPlant()
        if firstPlant != None:
            self.xLocationEdit.Text = usupport.digitValueString(firstPlant.basePoint_pixels().X)
            self.yLocationEdit.Text = usupport.digitValueString(firstPlant.basePoint_pixels().Y)
        else:
            self.xLocationEdit.Text = ""
            self.yLocationEdit.Text = ""
        self.xLocationEdit.Refresh()
        self.yLocationEdit.Refresh()
    
    # ------------------------------------------------------- *life cycle panel drawing and mouse handling 
    def updateLifeCyclePanelForFirstSelectedPlant(self):
        firstPlant = PdPlant()
        
        self.updatePlantNameLabel(kTabLifeCycle)
        firstPlant = self.focusedPlant()
        self.lifeCycleDaysEdit.Enabled = firstPlant != None
        self.lifeCycleDaysSpin.Enabled = firstPlant != None
        self.lifeCycleDragger.Enabled = firstPlant != None
        self.animateGrowth.Enabled = firstPlant != None
        self.timeLabel.Font.Color = self.textColorToRepresentPlantSelection(false)
        self.maxSizeAxisLabel.Font.Color = self.timeLabel.Font.Color
        self.ageAndSizeLabel.Font.Color = self.timeLabel.Font.Color
        self.daysAndSizeLabel.Font.Color = self.timeLabel.Font.Color
        if firstPlant != None:
            #special case
            self.lifeCycleDragger.Color = delphi_compatability.clRed
        else:
            self.lifeCycleDragger.Color = delphi_compatability.clGray
        # reset red dragger panel 
        self.placeLifeCycleDragger()
        if firstPlant != None:
            # set life cycle days in edit 
            self.lifeCycleDaysEdit.Text = IntToStr(firstPlant.age)
        else:
            self.lifeCycleDaysEdit.Text = "0"
        if firstPlant != None:
            # set % size label
            self.daysAndSizeLabel.Caption = "days, " + IntToStr(intround(firstPlant.totalBiomass_pctMPB)) + "% max size"
        else:
            self.daysAndSizeLabel.Caption = ""
        self.placeLifeCycleDragger()
        self.redrawLifeCycleGraph()
    
    def updatePlantNameLabel(self, tabIndex):
        firstPlant = PdPlant()
        labelToChange = TLabel()
        payAttentionToOtherPlants = false
        prefix = ""
        handlingDifferently = false
        
        firstPlant = self.focusedPlant()
        payAttentionToOtherPlants = true
        handlingDifferently = false
        prefix = ""
        labelToChange = None
        if tabIndex == kTabRotations:
            labelToChange = self.arrangementPlantName
            prefix = "Arrangement for "
        elif tabIndex == kTabParameters:
            labelToChange = self.parametersPlantName
            prefix = "Parameters for "
        elif tabIndex == kTabLifeCycle:
            labelToChange = self.selectedPlantNameLabel
            prefix = "Life cycle for "
        elif tabIndex == kTabPosing:
            labelToChange = self.posingPlantName
            payAttentionToOtherPlants = false
            prefix = "Posing for "
        elif tabIndex == kTabStatistics:
            handlingDifferently = true
            self.statsPanel.updatePlant(firstPlant)
        elif tabIndex == kTabNote:
            labelToChange = self.noteLabel
            payAttentionToOtherPlants = false
            prefix = "Note for "
        if (handlingDifferently) or (labelToChange == None):
            return
        if firstPlant != None:
            labelToChange.Caption = prefix + firstPlant.getName()
            if (payAttentionToOtherPlants) and (self.selectedPlants.Count > 1):
                labelToChange.Caption = labelToChange.Caption + " (and other plants)"
        else:
            labelToChange.Caption = "(no plants selected)"
        labelToChange.Font.Color = self.textColorToRepresentPlantSelection(payAttentionToOtherPlants)
    
    def animateGrowthClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdAnimatePlantCommand().createWithListOfPlants(self.selectedPlants)
        self.doCommand(newCommand)
    
    def MenuPlantAnimateClick(self, Sender):
        self.animateGrowthClick(self)
    
    # animation 
    def startAnimation(self):
        # called by animate command, which also sets up the pointer for the timer to call 
        # disable all non-modal forms 
        # keeps space bar from affecting magnification
        self.ActiveControl = self.plantListDrawGrid
        self.enableOrDisableAllForms(kDisableAllForms)
        # add warning about disabled forms 
        self.animatingLabel.Visible = true
        self.tabSet.visible = false
        # start timer 
        self.animateTimer.enabled = true
    
    def animateTimerTimer(self, Sender):
        if self.animateCommand != None:
            updcom.PdAnimatePlantCommand(self.animateCommand).animateOneDay()
    
    def stopAnimation(self):
        # called by animate command or self (if user clicks in drawing area or presses a key) 
        # stop timer 
        self.animateTimer.enabled = false
        # nil out pointer 
        self.animateCommand = None
        # re-enable everything 
        self.enableOrDisableAllForms(kEnableAllForms)
        # remove warning about disabled forms 
        self.animatingLabel.Visible = false
        self.tabSet.visible = true
        if udomain.domain.options.showSelectionRectangle:
            # if there were selection rectangles before, put them back 
            self.copyDrawingBitmapToPaintBox()
    
    def enableOrDisableAllForms(self, enable):
        # cfk note: put any new NON-MODAL forms here 
        self.Enabled = enable
        ubreedr.BreederForm.Enabled = enable
        utimeser.TimeSeriesForm.Enabled = enable
        udebug.DebugForm.Enabled = enable
    
    def lifeCycleDaysEditExit(self, Sender):
        newAge = 0
        plant = PdPlant()
        
        plant = self.focusedPlant()
        if plant == None:
            return
        newAge = StrToIntDef(self.lifeCycleDaysEdit.Text, 0)
        if newAge == plant.age:
            return
        if newAge > plant.pGeneral.ageAtMaturity:
            newAge = self.focusedPlant().pGeneral.ageAtMaturity
            self.lifeCycleDaysEdit.Text = IntToStr(newAge)
        self.changeSelectedPlantAges(newAge)
    
    def lifeCycleDaysSpinUpClick(self, Sender):
        newAge = 0
        
        if self.focusedPlant() == None:
            return
        newAge = umath.intMin(StrToIntDef(self.lifeCycleDaysEdit.Text, 0) + 1, self.focusedPlant().pGeneral.ageAtMaturity)
        newAge = umath.intMax(0, newAge)
        self.lifeCycleDaysEdit.Text = IntToStr(newAge)
        self.changeSelectedPlantAges(newAge)
    
    def lifeCycleDaysSpinDownClick(self, Sender):
        newAge = 0
        
        if self.focusedPlant() == None:
            return
        newAge = umath.intMin(StrToIntDef(self.lifeCycleDaysEdit.Text, 0) - 1, self.focusedPlant().pGeneral.ageAtMaturity)
        newAge = umath.intMax(0, newAge)
        self.lifeCycleDaysEdit.Text = IntToStr(newAge)
        self.changeSelectedPlantAges(newAge)
    
    def lifeCycleDraggerMouseDown(self, Sender, Button, Shift, X, Y):
        if self.focusedPlant() != None:
            self.lifeCycleDragging = true
            self.lifeCycleDraggingStartPos = X
            self.lifeCycleDraggingLastDrawPos = -1
            self.lifeCycleDraggingNeedToRedraw = true
    
    def lifeCycleDraggerMouseMove(self, Sender, Shift, X, Y):
        if self.lifeCycleDragging and (self.lifeCycleDragger.Left + X >= self.lifeCycleGraphImage.Left) and (self.lifeCycleDragger.Left + X < self.lifeCycleGraphImage.Left + self.lifeCycleGraphImage.Width):
            self.undrawLifeCycleDraggerLine()
            self.lifeCycleDraggingLastDrawPos = self.drawLifeCycleDraggerLine(X)
    
    def lifeCycleDraggerMouseUp(self, Sender, Button, Shift, X, Y):
        firstPlant = PdPlant()
        newAge = 0
        
        if self.lifeCycleDragging:
            self.undrawLifeCycleDraggerLine()
            self.lifeCycleDragger.Left = self.lifeCycleDragger.Left - (self.lifeCycleDraggingStartPos - X)
            if self.lifeCycleDragger.Left < self.lifeCycleGraphImage.Left:
                self.lifeCycleDragger.Left = self.lifeCycleGraphImage.Left
            if self.lifeCycleDragger.Left + self.lifeCycleDragger.Width > self.lifeCycleGraphImage.Left + self.lifeCycleGraphImage.Width:
                self.lifeCycleDragger.Left = self.lifeCycleGraphImage.Left + self.lifeCycleGraphImage.Width - self.lifeCycleDragger.Width
            firstPlant = self.focusedPlant()
            if firstPlant == None:
                raise GeneralException.create("Problem: First plant is nil during drag in method TMainForm.lifeCycleDraggerMouseUp.")
            if (self.lifeCycleGraphImage.Width - self.lifeCycleDragger.Width) != 0:
                newAge = intround(firstPlant.pGeneral.ageAtMaturity * (self.lifeCycleDragger.Left - self.lifeCycleGraphImage.Left) / (self.lifeCycleGraphImage.Width - self.lifeCycleDragger.Width))
            else:
                newAge = 0
            self.changeSelectedPlantAges(newAge)
            self.resizePanelsToVerticalSplitter()
            self.lifeCycleDragging = false
    
    def drawLifeCycleDraggerLine(self, pos):
        result = 0
        theDC = HDC()
        
        theDC = UNRESOLVED.getDC(0)
        result = self.ClientOrigin.X + self.plantFocusPanel.Left + self.lifeCyclePanel.Left + self.lifeCycleDragger.Left + pos + 2
        UNRESOLVED.patBlt(theDC, result, self.ClientOrigin.Y + self.plantFocusPanel.Top + self.lifeCyclePanel.Top + self.lifeCycleDragger.Top, 1, self.lifeCycleDragger.Height, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
        self.lifeCycleDraggingNeedToRedraw = true
        return result
    
    def undrawLifeCycleDraggerLine(self):
        theDC = HDC()
        
        if not self.lifeCycleDraggingNeedToRedraw:
            return
        theDC = UNRESOLVED.getDC(0)
        UNRESOLVED.patBlt(theDC, self.lifeCycleDraggingLastDrawPos, self.ClientOrigin.Y + self.plantFocusPanel.Top + self.lifeCyclePanel.Top + self.lifeCycleDragger.Top, 1, self.lifeCycleDragger.Height, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
        self.lifeCycleDraggingNeedToRedraw = false
    
    def changeSelectedPlantAges(self, newAge):
        newCommand = PdCommand()
        
        if self.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdChangePlantAgeCommand().createWithListOfPlantsAndNewAge(self.selectedPlants, newAge)
        self.doCommand(newCommand)
    
    # life cycle panel drawing and mouse handling 
    def redrawLifeCycleGraph(self):
        sCurveError = false
        
        self.lifeCycleGraphImage.Picture.Bitmap.Canvas.Brush.Color = UNRESOLVED.clBtnFace
        self.lifeCycleGraphImage.Picture.Bitmap.Canvas.Rectangle(0, 0, self.lifeCycleGraphImage.ClientWidth, self.lifeCycleGraphImage.ClientHeight)
        sCurveError = self.drawSCurveOrCheckForError(self.lifeCycleGraphImage.Picture.Bitmap.Canvas, delphi_compatability.Bounds(0, 0, self.lifeCycleGraphImage.ClientWidth, self.lifeCycleGraphImage.ClientHeight), true, sCurveError)
        if sCurveError and (self.focusedPlant() != None):
            # error - do something, should be caught by parameter panel 
            # PDF PORT -- put in NIL
            None
    
    def drawSCurveOrCheckForError(self, aCanvas, aRect, draw, failed):
        firstPlant = PdPlant()
        i = 0
        x = 0.0
        y = 0.0
        thisPoint = TPoint()
        curve = SCurveStructure()
        numPoints = 0
        
        firstPlant = self.focusedPlant()
        if firstPlant == None:
            return failed
        failed = true
        numPoints = 100
        # assumes that zero does NOT fall between x1 and x2, though one of these could be zero 
        curve.x1 = firstPlant.pGeneral.growthSCurve.x1
        curve.y1 = firstPlant.pGeneral.growthSCurve.y1
        curve.x2 = firstPlant.pGeneral.growthSCurve.x2
        curve.y2 = firstPlant.pGeneral.growthSCurve.y2
        try:
            failed = umath.calcSCurveCoeffsWithResult(curve, failed)
            if failed:
                return failed
            for i in range(0, numPoints):
                # delphi 2.0 wants this 
                x = 0.0
                y = 0.0
                try:
                    x = 1.0 * i / numPoints
                except:
                    return failed
                y = umath.scurveWithResult(x, curve.c1, curve.c2, failed)
                if failed:
                    return failed
                if draw:
                    thisPoint.X = aRect.Left + intround(x * (aRect.Right - aRect.Left))
                    thisPoint.Y = aRect.Top + intround((1.0 - y) * (aRect.Bottom - aRect.Top))
                    if i == 0:
                        aCanvas.MoveTo(thisPoint.X, thisPoint.Y)
                    else:
                        aCanvas.LineTo(thisPoint.X, thisPoint.Y)
        except:
            return failed
        failed = false
        return failed
    
    # ----------------------------------------------------------------------------- *parameters panel 
    def sectionsComboBoxDrawItem(self, Control, index, Rect, State):
        section = PdSection()
        sectionPicture = TPicture()
        selected = false
        textDrawRect = TRect()
        cText = [0] * (range(0, 255 + 1) + 1)
        
        if delphi_compatability.Application.terminated:
            return
        if (self.sectionsComboBox.Items.Count <= 0) or (index < 0) or (index > self.sectionsComboBox.Items.Count - 1):
            return
        selected = (delphi_compatability.TOwnerDrawStateType.odSelected in State)
        # set up section pointer 
        section = self.sectionsComboBox.Items.Objects[index] as usection.PdSection
        if section == None:
            return
        self.sectionsComboBox.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        self.sectionsComboBox.Canvas.Font = self.sectionsComboBox.Font
        if selected:
            self.sectionsComboBox.Canvas.Brush.Color = UNRESOLVED.clHighlight
            self.sectionsComboBox.Canvas.Font.Color = UNRESOLVED.clHighlightText
        else:
            self.sectionsComboBox.Canvas.Brush.Color = self.sectionsComboBox.Color
            self.sectionsComboBox.Canvas.Font.Color = UNRESOLVED.clBtnText
        self.sectionsComboBox.Canvas.FillRect(Rect)
        textDrawRect = Rect
        textDrawRect.Left = textDrawRect.Left + 4
        textDrawRect.Top = textDrawRect.Top + (textDrawRect.Bottom - textDrawRect.Top) / 2 - (self.sectionsComboBox.Canvas.TextHeight("W") / 2)
        sectionPicture = self.sectionPictureForSectionName(section.getName())
        if sectionPicture != None:
            self.sectionsComboBox.Canvas.Draw(Rect.left + 4, Rect.top, sectionPicture.Graphic)
        textDrawRect.Left = textDrawRect.Left + 32 + 4
        UNRESOLVED.strPCopy(cText, self.sectionsComboBox.Items[index])
        UNRESOLVED.winprocs.drawText(self.sectionsComboBox.Canvas.Handle, cText, len(cText), textDrawRect, delphi_compatability.DT_LEFT)
    
    def sectionsComboBoxChange(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        self.updateParameterPanelsForSectionChange()
        self.updateSectionPopupMenuForSectionChange()
    
    # parameters panel 
    def loadSectionsIntoListBox(self):
        section = PdSection()
        i = 0
        indexOfPrimaryInflors = 0
        
        if (udomain.domain == None) or (udomain.domain.sectionManager == None):
            return
        self.sectionsComboBox.Clear()
        if udomain.domain.sectionManager.sections.Count > 0:
            for i in range(0, udomain.domain.sectionManager.sections.Count):
                section = usection.PdSection(udomain.domain.sectionManager.sections.Items[i])
                if section.showInParametersWindow:
                    if section.name == "Primary flowers, advanced":
                        # kludge to get around necessary ordering of new advanced floral section
                        # advanced floral params are at end of file, but want to show them
                        # in the list before inflorescences
                        # WATCH OUT: change this code if you change the names of the sections
                        indexOfPrimaryInflors = self.sectionsComboBox.Items.IndexOf("Primary inflorescences")
                        self.sectionsComboBox.Items.InsertObject(indexOfPrimaryInflors, section.name, section)
                    else:
                        self.sectionsComboBox.Items.AddObject(section.name, section)
        if udomain.domain.sectionManager.orthogonalSections.Count > 0:
            for i in range(0, udomain.domain.sectionManager.orthogonalSections.Count):
                # v2.1 add orthogonal sections
                section = usection.PdSection(udomain.domain.sectionManager.orthogonalSections.Items[i])
                if section.showInParametersWindow:
                    self.sectionsComboBox.Items.AddObject(section.name, section)
    
    def currentSection(self):
        result = PdSection()
        result = None
        if (self.sectionsComboBox.Items.Count <= 0) or (self.sectionsComboBox.ItemIndex < 0) or (self.sectionsComboBox.ItemIndex > self.sectionsComboBox.Items.Count - 1):
            return result
        result = usection.PdSection(self.sectionsComboBox.Items.Objects[self.sectionsComboBox.ItemIndex])
        return result
    
    def sectionPictureForSectionName(self, aName):
        result = TPicture()
        image = TImage()
        
        result = None
        if aName == "(no section)":
            return result
        image = None
        aName = lowercase(aName)
        if usupport.found("general", aName):
            image = self.Sections_General
        elif usupport.found("meris", aName):
            image = self.Sections_Meristems
        elif usupport.found("inter", aName):
            image = self.Sections_Internodes
        elif usupport.found("seed", aName):
            image = self.Sections_SeedlingLeaves
        elif usupport.found("lea", aName):
            #must be below seedling leaves
            image = self.Sections_Leaves
        elif usupport.found("flow", aName) and usupport.found("primary", aName) and usupport.found("advanced", aName):
            image = self.Sections_FlowersPrimaryAdvanced
        elif usupport.found("flow", aName) and usupport.found("primary", aName):
            image = self.Sections_FlowersPrimary
        elif usupport.found("inflo", aName) and usupport.found("primary", aName):
            image = self.Sections_InflorPrimary
        elif usupport.found("fruit", aName):
            image = self.Sections_Fruit
        elif usupport.found("flow", aName) and usupport.found("secondary", aName):
            image = self.Sections_FlowersSecondary
        elif usupport.found("inflo", aName) and usupport.found("secondary", aName):
            image = self.Sections_InflorSecondary
        elif usupport.found("root", aName):
            # v2.1 otherwise assume it is an orthogonal section
            image = self.Sections_RootTop
        else:
            image = self.Sections_Orthogonal
        if image != None:
            result = image.Picture
        return result
    
    def sectionHelpIDForSectionName(self, aName):
        result = ""
        result = ""
        if aName == "(no section)":
            return result
        aName = lowercase(aName)
        if usupport.found("general", aName):
            # trying to be flexible about possible name changes here 
            result = "General_parameters"
        elif usupport.found("meris", aName):
            result = "Meristem_parameters"
        elif usupport.found("inter", aName):
            result = "Internode_parameters"
        elif usupport.found("first", aName):
            result = "First_leaf_parameters"
        elif usupport.found("lea", aName):
            #must be below seedling leaves
            result = "Leaf_parameters"
        elif usupport.found("advanced", aName):
            # must be above flower params
            result = "Advanced_flower_parameters"
        elif usupport.found("flow", aName):
            result = "Flower_parameters"
        elif usupport.found("inflo", aName):
            result = "Inflorescence_parameters"
        elif usupport.found("fruit", aName):
            result = "Fruit_parameters"
        elif usupport.found("root", aName):
            # add more sections here if any are added to the params file 
            # v2.1 otherwise assume it is an orthogonal section
            result = "Root_top_parameters"
        else:
            result = "Transverse_parameter_sections"
        return result
    
    def updateParameterPanelsForSectionChange(self):
        paramPanel = PdParameterPanel()
        oldParamPanel = PdParameterPanel()
        section = PdSection()
        parameter = PdParameter()
        i = 0
        
        try:
            ucursor.cursor_startWait()
            # clear out any earlier panels 
            self.selectedParameterPanel = None
            if self.parametersScrollBox.ControlCount > 0:
                while self.parametersScrollBox.ControlCount > 0:
                    # this is the only valid time to free a component owned by something - after it has
                    #        been removed from the component list (owned objects) of the owner 
                    oldParamPanel = uppanel.PdParameterPanel(self.parametersScrollBox.Controls[0])
                    self.RemoveComponent(oldParamPanel)
                    oldParamPanel.Parent = None
                    oldParamPanel.free
            if self.sectionsComboBox.ItemIndex < 0:
                # make new panels for the current section 
                return
            section = self.sectionsComboBox.Items.Objects[self.sectionsComboBox.ItemIndex] as usection.PdSection
            if section.numSectionItems > 0:
                for i in range(0, section.numSectionItems):
                    parameter = udomain.domain.parameterManager.parameterForFieldNumber(section.sectionItems[i])
                    if parameter == None:
                        continue
                    paramPanel = None
                    # note that the longint type is used to store plant positions, but should not be used
                    #          for parameter panels 
                    if parameter.fieldType == uparams.kFieldHeader:
                        paramPanel = upp_hed.PdHeaderParameterPanel().createForParameter(self, parameter)
                    elif parameter.fieldType == uparams.kFieldEnumeratedList:
                        paramPanel = upp_lis.PdListParameterPanel().createForParameter(self, parameter)
                    elif parameter.fieldType == uparams.kFieldThreeDObject:
                        paramPanel = upp_tdo.PdTdoParameterPanel().createForParameter(self, parameter)
                    elif parameter.fieldType == uparams.kFieldColor:
                        paramPanel = upp_col.PdColorParameterPanel().createForParameter(self, parameter)
                    elif parameter.fieldType == uparams.kFieldSmallint:
                        paramPanel = upp_int.PdSmallintParameterPanel().createForParameter(self, parameter)
                    elif parameter.fieldType == uparams.kFieldFloat:
                        if parameter.indexCount() <= 1:
                            paramPanel = upp_rea.PdRealParameterPanel().createForParameter(self, parameter)
                        elif parameter.indexType == uparams.kIndexTypeSCurve:
                            paramPanel = upp_scv.PdSCurveParameterPanel().createForParameter(self, parameter)
                    elif parameter.fieldType == uparams.kFieldBoolean:
                        paramPanel = upp_boo.PdBooleanParameterPanel().createForParameter(self, parameter)
                    else :
                        raise GeneralException.create("Problem: Unsupported parameter type in method TMainForm.updateParameterPanelsForSectionChange.")
                    if paramPanel != None:
                        paramPanel.Parent = self.parametersScrollBox
                        #9 +
                        paramPanel.TabOrder = i
                        paramPanel.calculateTextDimensions()
                        paramPanel.calculateHeight()
                        if (parameter.originalSectionName != section.name) and not (paramPanel.__class__ is upp_hed.PdHeaderParameterPanel):
                            # v2.1 add original section name to params in orthogonal sections
                            paramPanel.Caption = paramPanel.Caption + " [" + parameter.originalSectionName + "]"
            self.updateParametersPanelForFirstSelectedPlant()
            self.repositionParameterPanels()
        finally:
            ucursor.cursor_stopWait()
    
    def paramHelpIDForParamPanel(self, panel):
        result = ""
        result = ""
        if panel == None:
            return result
        if panel.__class__ is upp_hed.PdHeaderParameterPanel:
            result = "Using_header_parameter_panels"
        elif (panel.__class__ is upp_int.PdSmallintParameterPanel) or (panel.__class__ is upp_rea.PdRealParameterPanel):
            result = "Using_number_parameter_panels"
        elif panel.__class__ is upp_scv.PdSCurveParameterPanel:
            result = "Using_S_curve_parameter_panels"
        elif panel.__class__ is upp_boo.PdBooleanParameterPanel:
            result = "Using_yes/no_parameter_panels"
        elif panel.__class__ is upp_lis.PdListParameterPanel:
            result = "Using_list_parameter_panels"
        elif panel.__class__ is upp_col.PdColorParameterPanel:
            result = "Using_color_parameter_panels"
        elif panel.__class__ is upp_tdo.PdTdoParameterPanel:
            result = "Using_3D_object_parameter_panels"
        return result
    
    def updateParametersPanelForFirstSelectedPlant(self):
        i = 0
        paramPanel = PdParameterPanel()
        
        self.updatePlantNameLabel(kTabParameters)
        if self.parametersScrollBox.ControlCount > 0:
            for i in range(0, self.parametersScrollBox.ControlCount):
                if self.parametersScrollBox.Controls[i].__class__ is uppanel.PdParameterPanel:
                    paramPanel = self.parametersScrollBox.Controls[i] as uppanel.PdParameterPanel
                    #panels check if the new plant is different from current one
                    paramPanel.updatePlant(self.focusedPlant())
        self.repositionParameterPanels()
    
    def enteringAParameterPanel(self, aPanel):
        self.selectedParameterPanel = aPanel
        # update menu items and other things 
    
    def leavingAParameterPanel(self, aPanel):
        self.selectedParameterPanel = None
        # update menu items and other things 
    
    def repositionParameterPanels(self):
        i = 0
        lastPos = 0
        totalMaxWidth = 0
        panelMaxWidth = 0
        panelMinWidth = 0
        requestedWidth = 0
        windowLock = false
        paramPanel = PdParameterPanel()
        oldPosition = 0
        
        if delphi_compatability.Application.terminated:
            return
        if self.parametersScrollBox.ControlCount > 0:
            totalMaxWidth = 0
            lastPos = 0
            oldPosition = self.parametersScrollBox.VertScrollBar.Position
            self.parametersScrollBox.VertScrollBar.Position = 0
            windowLock = UNRESOLVED.lockWindowUpdate(self.Handle)
            requestedWidth = self.parametersScrollBox.ClientWidth
            for i in range(0, self.parametersScrollBox.ControlCount):
                paramPanel = uppanel.PdParameterPanel(self.parametersScrollBox.Controls[i])
                paramPanel.Left = 0
                paramPanel.Top = lastPos
                paramPanel.calculateTextDimensions()
                panelMaxWidth = paramPanel.maxWidth()
                panelMinWidth = paramPanel.minWidth(requestedWidth)
                if panelMaxWidth <= requestedWidth:
                    paramPanel.Width = panelMaxWidth
                else:
                    if panelMinWidth == -1:
                        paramPanel.Width = requestedWidth
                    else:
                        paramPanel.Width = panelMinWidth
                paramPanel.calculateHeight()
                lastPos = lastPos + paramPanel.Height
                if paramPanel.Width > totalMaxWidth:
                    totalMaxWidth = paramPanel.Width
            lastPos = 0
            for i in range(0, self.parametersScrollBox.ControlCount):
                paramPanel = uppanel.PdParameterPanel(self.parametersScrollBox.Controls[i])
                paramPanel.Top = lastPos
                # cfk change v2.0 final - can't remember why we had a max width - looks better this way
                # paramPanel.width := totalMaxWidth;   // was this
                # changed to
                paramPanel.Width = self.parametersScrollBox.Width - 20
                paramPanel.calculateHeight()
                paramPanel.resizeElements()
                lastPos = lastPos + paramPanel.Height
            self.parametersScrollBox.VertScrollBar.Position = oldPosition
            if windowLock:
                UNRESOLVED.lockWindowUpdate(0)
    
    def collapseOrExpandParameterPanelsUntilNextHeader(self, headerPanel):
        collapsing = false
        paramPanel = PdParameterPanel()
        i = 0
        
        collapsing = false
        self.internalChange = true
        if self.parametersScrollBox.ControlCount > 0:
            for i in range(0, self.parametersScrollBox.ControlCount):
                paramPanel = uppanel.PdParameterPanel(self.parametersScrollBox.Controls[i])
                if paramPanel == headerPanel:
                    collapsing = true
                elif collapsing and (paramPanel.__class__ is upp_hed.PdHeaderParameterPanel):
                    collapsing = false
                elif collapsing:
                    if headerPanel.param.collapsed:
                        paramPanel.expand()
                    else:
                        paramPanel.collapse()
        self.internalChange = false
        self.repositionParameterPanels()
    
    def collapseOrExpandAllParameterPanelsInCurrentSection(self, doWhat):
        section = PdSection()
        paramPanel = PdParameterPanel()
        i = 0
        
        self.internalChange = true
        if self.sectionsComboBox.ItemIndex < 0:
            return
        section = self.sectionsComboBox.Items.Objects[self.sectionsComboBox.ItemIndex] as usection.PdSection
        if section == None:
            return
        if doWhat == kExpand:
            section.expanded = true
        elif doWhat == kCollapse:
            section.expanded = false
        elif doWhat == kExpandOrCollapse:
            section.expanded = not section.expanded
        if self.parametersScrollBox.ControlCount > 0:
            for i in range(0, self.parametersScrollBox.ControlCount):
                paramPanel = uppanel.PdParameterPanel(self.parametersScrollBox.Controls[i])
                if section.expanded:
                    paramPanel.expand()
                else:
                    paramPanel.collapse()
        self.internalChange = false
        self.repositionParameterPanels()
    
    def updateParameterValuesWithUpdateListForPlant(self, aPlant, updateList):
        i = 0L
        paramPanel = PdParameterPanel()
        updateEvent = PdPlantUpdateEvent()
        needToUpdateWholePlant = false
        
        if aPlant != self.focusedPlant():
            return
        if updateList.Count <= 0:
            return
        # first look to see if the whole plant needs updated - if any do, update it 
        # this is for side effects in GWI - left in just in case we need it later 
        needToUpdateWholePlant = false
        for i in range(0, updateList.Count):
            updateEvent = uplant.PdPlantUpdateEvent(updateList.Items[i])
            if (updateEvent.plant != None) and (updateEvent.plant.wholePlantUpdateNeeded):
                needToUpdateWholePlant = true
                updateEvent.plant.wholePlantUpdateNeeded = false
        if needToUpdateWholePlant:
            self.updateParametersPanelForFirstSelectedPlant()
            return
        if self.parametersScrollBox.ControlCount > 0:
            for i in range(0, self.parametersScrollBox.ControlCount):
                if self.parametersScrollBox.Controls[i].__class__ is uppanel.PdParameterPanel:
                    # if not updating everything, update based on list 
                    # tell all components to look at list to see if they need updating 
                    paramPanel = self.parametersScrollBox.Controls[i] as uppanel.PdParameterPanel
                    # components check if use models and fields in list 
                    paramPanel.updateFromUpdateEventList(updateList)
    
    # stats panel
    def updateStatisticsPanelForFirstSelectedPlant(self):
        if delphi_compatability.Application.terminated:
            return
        if self.statsPanel == None:
            return
        self.statsPanel.updatePlant(self.focusedPlant())
        self.statsPanel.updatePlantValues()
    
    # note panel
    def updateNoteForFirstSelectedPlant(self):
        selStart = 0
        
        if delphi_compatability.Application.terminated:
            return
        if self.notePanel == None:
            return
        if self.noteMemo == None:
            return
        self.updatePlantNameLabel(kTabNote)
        self.updateForChangeToPlantNote(self.focusedPlant())
    
    def noteEditClick(self, Sender):
        newCommand = PdCommand()
        noteForm = TNoteEditForm()
        commandLines = TStringList()
        
        if self.focusedPlant() == None:
            return
        noteForm = unoted.TNoteEditForm().create(self)
        if noteForm == None:
            raise GeneralException.create("Problem: Could not create note edit window.")
        try:
            noteForm.noteEditMemo.Lines.AddStrings(self.focusedPlant().noteLines)
            noteForm.Caption = "Edit note for " + self.focusedPlant().getName()
            if noteForm.ShowModal() != mrCancel:
                # command will take ownership of this and free it if necessary
                commandLines = delphi_compatability.TStringList.create
                commandLines.AddStrings(noteForm.noteEditMemo.Lines)
                newCommand = updcom.PdEditNoteCommand().createWithPlantAndNewTStrings(self.focusedPlant(), commandLines)
                self.doCommand(newCommand)
        finally:
            noteForm.free
            noteForm = None
    
    def NotePopupMenuCopyClick(self, Sender):
        self.noteMemo.CopyToClipboard()
    
    def NotePopupMenuEditClick(self, Sender):
        self.noteEditClick(self)
    
    def NotePopupMenuSelectAllClick(self, Sender):
        self.noteMemo.SelectAll()
    
    def MenuPlantEditNoteClick(self, Sender):
        self.noteEditClick(self)
    
    def PopupMenuEditNoteClick(self, Sender):
        self.noteEditClick(self)
    
    # rotations panel
    def updateRotationsPanelForFirstSelectedPlant(self):
        color = TColorRef()
        
        self.updatePlantNameLabel(kTabRotations)
        color = self.textColorToRepresentPlantSelection(false)
        # location
        self.locationLabel.Font.Color = color
        self.xLocationLabel.Font.Color = color
        self.yLocationLabel.Font.Color = color
        self.locationPixelsLabel.Font.Color = color
        # size
        self.sizingLabel.Font.Color = color
        self.drawingScalePixelsPerMmLabel.Font.Color = color
        # rotation
        self.rotationLabel.Font.Color = color
        self.xRotationLabel.Font.Color = color
        self.yRotationLabel.Font.Color = color
        self.zRotationLabel.Font.Color = color
        # other updates
        self.updateForChangeToPlantRotations()
        self.updateForChangeToSelectedPlantsDrawingScale()
        self.updateForChangeToSelectedPlantsLocation()
    
    # posing panel
    # ------------------------------------------------------------------------------------- *posing - updating 
    def updatePosingForFirstSelectedPlant(self):
        i = 0
        amendment = PdPlantDrawingAmendment()
        partString = ""
        
        self.internalChange = true
        self.posedPartsLabel.Font.Color = self.textColorToRepresentPlantSelection(false)
        self.selectedPartLabel.Font.Color = self.textColorToRepresentPlantSelection(false)
        self.posingPosePart.Enabled = false
        self.posingUnposePart.Enabled = false
        # called when plant changes
        self.posedPlantParts.Clear()
        self.updatePlantNameLabel(kTabPosing)
        if self.focusedPlant() == None:
            self.posedPlantParts.Text = ""
            self.posedPlantParts.Enabled = false
        else:
            self.posedPlantParts.Enabled = true
            if self.focusedPlant().amendments.Count <= 0:
                # load list of parts with amendments
                self.selectedPlantPartID = -1
            else:
                for i in range(0, self.focusedPlant().amendments.Count):
                    amendment = uamendmt.PdPlantDrawingAmendment(self.focusedPlant().amendments.Items[i])
                    partString = self.partDescriptionForIDAndType(amendment.partID, amendment.typeOfPart)
                    if self.posedPlantParts.Items.IndexOf(partString) < 0:
                        self.posedPlantParts.Items.Add(partString)
                self.posedPlantParts.Items.Add(kSelectNoPosedPartString)
        self.internalChange = false
        self.updatePosingForSelectedPlantPart()
    
    def updatePosingForSelectedPlantPart(self):
        partString = ""
        index = 0
        
        # PDF PORT -- removed semicolon from after begin
        self.internalChange = true
        if self.focusedPlant() == None:
            # called when selected part changes
            self.selectedPlantPartID = -1
            self.selectedPlantPartType = ""
            self.selectedPartLabel.Caption = kNoPartSelected
        if self.selectedPlantPartID >= 0:
            partString = self.partDescriptionForIDAndType(self.selectedPlantPartID, self.selectedPlantPartType)
            self.selectedPartLabel.Caption = "Selected part: " + partString
            index = self.posedPlantParts.Items.IndexOf(partString)
            if index >= 0:
                self.posedPlantParts.ItemIndex = index
            else:
                self.posedPlantParts.ItemIndex = -1
        else:
            self.posedPlantParts.ItemIndex = -1
            self.selectedPartLabel.Caption = kNoPartSelected
        self.posingPosePart.Enabled = not (self.selectedPartLabel.Caption == kNoPartSelected)
        self.posingUnposePart.Enabled = false
        self.internalChange = false
        self.updatePoseInfo()
    
    def updatePoseInfo(self):
        amendment = PdPlantDrawingAmendment()
        partID = 0L
        
        self.internalChange = true
        amendment = None
        partID = self.selectedPartIDInAmendedPartsList()
        if partID >= 0:
            amendment = self.focusedPlant().amendmentForPartID(partID)
        self.posingPosePart.Enabled = (not (self.selectedPartLabel.Caption == kNoPartSelected)) and (amendment == None)
        self.posingUnposePart.Enabled = (not (self.selectedPartLabel.Caption == kNoPartSelected)) and (not (amendment == None))
        self.posingDetailsPanel.Visible = amendment != None
        if (amendment != None):
            self.posingHidePart.Checked = amendment.hide
            #
            #    posingChangeColors.checked := changeColors;
            #    posingFrontfaceColor.color := faceColor;
            #    posingBackfaceColor.color := BackfaceColor;
            #    posingLineColor.color := lineColor;
            #    posingChangeAllColorsAfter.checked := propagateColors;
            #    
            self.posingAddExtraRotation.Checked = amendment.addRotations
            self.posingXRotationEdit.Text = IntToStr(intround(amendment.xRotation))
            self.posingYRotationEdit.Text = IntToStr(intround(amendment.yRotation))
            self.posingZRotationEdit.Text = IntToStr(intround(amendment.zRotation))
            self.posingMultiplyScale.Checked = amendment.multiplyScale
            self.posingMultiplyScaleAllPartsAfter.Checked = amendment.propagateScale
            self.posingScaleMultiplierEdit.Text = IntToStr(amendment.scaleMultiplier_pct)
            self.posingLengthMultiplierEdit.Text = IntToStr(amendment.lengthMultiplier_pct)
            self.posingWidthMultiplierEdit.Text = IntToStr(amendment.widthMultiplier_pct)
        self.internalChange = false
        self.updateForDependenciesWithinPoseInfo()
    
    def updateForDependenciesWithinPoseInfo(self):
        self.internalChange = true
        self.posingChangeAllColorsAfter.Enabled = self.posingChangeColors.Checked
        self.posingMultiplyScaleAllPartsAfter.Enabled = self.posingMultiplyScale.Checked
        self.posingMultiplyScaleAllPartsAfterLabel.Enabled = self.posingMultiplyScaleAllPartsAfter.Enabled
        #
        #  posingLineColor.visible := posingChangeColors.checked;
        #  posingLineColorLabel.enabled := posingChangeColors.checked;
        #  posingFrontfaceColor.visible := posingChangeColors.checked;
        #  posingFrontfaceColorLabel.enabled := posingChangeColors.checked;
        #  posingBackfaceColor.visible := posingChangeColors.checked;
        #  posingBackfaceColorLabel.enabled := posingChangeColors.checked;
        #  
        enableOrDisableSet(self.posingXRotationLabel, self.posingXRotationEdit, self.posingXRotationSpin, None, self.posingAddExtraRotation.Checked)
        enableOrDisableSet(self.posingYRotationLabel, self.posingYRotationEdit, self.posingYRotationSpin, None, self.posingAddExtraRotation.Checked)
        enableOrDisableSet(self.posingZRotationLabel, self.posingZRotationEdit, self.posingZRotationSpin, None, self.posingAddExtraRotation.Checked)
        self.rotationDegreesLabel.Enabled = self.posingAddExtraRotation.Checked
        enableOrDisableSet(self.posingScaleMultiplierLabel, self.posingScaleMultiplierEdit, self.posingScaleMultiplierSpin, self.posingScaleMultiplierPercent, self.posingMultiplyScale.Checked)
        enableOrDisableSet(self.posingLengthMultiplierLabel, self.posingLengthMultiplierEdit, self.posingLengthMultiplierSpin, self.posingLengthMultiplierPercent, self.posingMultiplyScale.Checked)
        enableOrDisableSet(self.posingWidthMultiplierLabel, self.posingWidthMultiplierEdit, self.posingWidthMultiplierSpin, self.posingWidthMultiplierPercent, self.posingMultiplyScale.Checked)
        self.internalChange = false
    
    def redrawAllPlantsInViewWithAmendments(self):
        i = 0
        plant = PdPlant()
        
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if (plant != None) and (plant.amendments != None) and (plant.amendments.Count > 0):
                    plant.recalculateBounds(kDrawNow)
                    self.invalidateDrawingRect(plant.boundsRect_pixels())
        self.updateForPossibleChangeToDrawing()
    
    # ------------------------------------------------------------------------------------- *posing - interface 
    def posedPlantPartsChange(self, Sender):
        newCommand = PdCommand()
        
        if self.internalChange:
            return
        if self.posedPlantParts.ItemIndex == self.posedPlantParts.Items.Count - 1:
            newCommand = updcom.PdSelectPosingPartCommand().createWithPlantAndPartIDsAndTypes(self.focusedPlant(), -1, self.selectedPlantPartID, "", self.selectedPlantPartType)
        else:
            newCommand = updcom.PdSelectPosingPartCommand().createWithPlantAndPartIDsAndTypes(self.focusedPlant(), self.selectedPartIDInAmendedPartsList(), self.selectedPlantPartID, self.selectedPartTypeInAmendedPartsList(), self.selectedPlantPartType)
        self.doCommand(newCommand)
    
    def posingFrontfaceColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.posingFrontfaceColor.Color = udomain.domain.getColorUsingCustomColors(self.posingFrontfaceColor.Color)
        self.changeSelectedPose(self.posingFrontfaceColor)
    
    def posingBackfaceColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.posingBackfaceColor.Color = udomain.domain.getColorUsingCustomColors(self.posingBackfaceColor.Color)
        self.changeSelectedPose(self.posingBackfaceColor)
    
    def posingLineColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.posingLineColor.Color = udomain.domain.getColorUsingCustomColors(self.posingLineColor.Color)
        self.changeSelectedPose(self.posingLineColor)
    
    def posingRotationSpinUp(self, Sender):
        if (Sender != None) and (Sender.__class__ is delphi_compatability.TSpinButton):
            self.spinPoseRotationBy((Sender as delphi_compatability.TSpinButton).focusControl, udomain.domain.options.rotationIncrement)
    
    def posingRotationSpinDown(self, Sender):
        if (Sender != None) and (Sender.__class__ is delphi_compatability.TSpinButton):
            self.spinPoseRotationBy((Sender as delphi_compatability.TSpinButton).focusControl, -udomain.domain.options.rotationIncrement)
    
    def spinPoseRotationBy(self, sender, amount):
        newRotation = 0
        oldRotation = 0
        
        if (sender != None) and (sender.__class__ is delphi_compatability.TEdit):
            newRotation = StrToIntDef((sender as delphi_compatability.TEdit).Text, 0)
            oldRotation = newRotation
            newRotation = newRotation + amount
            if newRotation < -360:
                newRotation = 360 - (abs(newRotation) - 360)
            if newRotation > 360:
                newRotation = -360 + (newRotation - 360)
            if newRotation != oldRotation:
                (sender as delphi_compatability.TEdit).Text = IntToStr(newRotation)
    
    def posingScaleMultiplierSpinUpClick(self, Sender):
        if (Sender != None) and (Sender.__class__ is delphi_compatability.TSpinButton):
            self.spinScaleMultiplierBy((Sender as delphi_compatability.TSpinButton).focusControl, udomain.domain.options.resizeKeyUpMultiplierPercent - 100)
    
    def posingScaleMultiplierSpinDownClick(self, Sender):
        if (Sender != None) and (Sender.__class__ is delphi_compatability.TSpinButton):
            self.spinScaleMultiplierBy((Sender as delphi_compatability.TSpinButton).focusControl, -(udomain.domain.options.resizeKeyUpMultiplierPercent - 100))
    
    def spinScaleMultiplierBy(self, sender, amount):
        newValue = 0
        oldValue = 0
        
        if (sender != None) and (sender.__class__ is delphi_compatability.TEdit):
            newValue = StrToIntDef((sender as delphi_compatability.TEdit).Text, 0)
            oldValue = newValue
            newValue = newValue + amount
            if newValue < 0:
                newValue = 0
            if newValue > 1000:
                newValue = 1000
            if newValue != oldValue:
                (sender as delphi_compatability.TEdit).Text = IntToStr(newValue)
    
    # ------------------------------------------------------------------------------------- *posing - commands 
    def changeSelectedPose(self, Sender):
        newCommand = PdCommand()
        newAmendment = PdPlantDrawingAmendment()
        partID = 0L
        currentAmendment = PdPlantDrawingAmendment()
        field = ""
        
        if self.internalChange:
            return
        self.updateForDependenciesWithinPoseInfo()
        if self.focusedPlant() == None:
            return
        # command will take ownership of this and free it if necessary
        newAmendment = uamendmt.PdPlantDrawingAmendment().create()
        partID = self.selectedPartIDInAmendedPartsList()
        currentAmendment = self.focusedPlant().amendmentForPartID(partID)
        if currentAmendment == None:
            return
        if (Sender == self.posingHidePart):
            field = "hide"
        elif (Sender == self.posingAddExtraRotation):
            field = "rotate"
        elif ((Sender == self.posingXRotationEdit) or (Sender == self.posingXRotationSpin)):
            field = "X rotation"
        elif ((Sender == self.posingYRotationEdit) or (Sender == self.posingYRotationSpin)):
            field = "Y rotation"
        elif ((Sender == self.posingZRotationEdit) or (Sender == self.posingZRotationSpin)):
            field = "Z rotation"
        elif (Sender == self.posingMultiplyScale):
            field = "scale"
        elif (Sender == self.posingMultiplyScaleAllPartsAfter):
            field = "scale above"
        elif ((Sender == self.posingScaleMultiplierEdit) or (Sender == self.posingScaleMultiplierSpin)):
            field = "3D object scale"
        elif ((Sender == self.posingLengthMultiplierEdit) or (Sender == self.posingLengthMultiplierSpin)):
            field = "line length"
        elif ((Sender == self.posingWidthMultiplierEdit) or (Sender == self.posingWidthMultiplierSpin)):
            field = "line width"
        else:
            field = ""
        #   cfk if bring back color finish these
        #    posingChangeColors: TCheckBox;
        #    posingChangeAllColorsAfter: TCheckBox;
        #    posingLineColor: TPanel;
        #    posingFrontfaceColor: TPanel;
        #    posingBackfaceColor: TPanel;
        #    posingLineColorLabel: TLabel;
        #    posingFrontfaceColorLabel: TLabel;
        #    posingBackfaceColorLabel: TLabel;
        #    
        newAmendment.partID = self.partIDForFullDescription(self.posedPlantParts.Text)
        newAmendment.typeOfPart = self.partTypeForFullDescription(self.posedPlantParts.Text)
        newAmendment.hide = self.posingHidePart.Checked
        #
        #    changeColors := posingChangeColors.checked;
        #    faceColor := posingFrontfaceColor.color;
        #    backfaceColor := posingBackfaceColor.color;
        #    lineColor := posingLineColor.color;
        #    propagateColors := posingChangeAllColorsAfter.checked;
        #    
        newAmendment.addRotations = self.posingAddExtraRotation.Checked
        newAmendment.xRotation = umath.intMax(-360, umath.intMin(360, StrToIntDef(self.posingXRotationEdit.Text, intround(currentAmendment.xRotation))))
        newAmendment.yRotation = umath.intMax(-360, umath.intMin(360, StrToIntDef(self.posingYRotationEdit.Text, intround(currentAmendment.yRotation))))
        newAmendment.zRotation = umath.intMax(-360, umath.intMin(360, StrToIntDef(self.posingZRotationEdit.Text, intround(currentAmendment.zRotation))))
        newAmendment.multiplyScale = self.posingMultiplyScale.Checked
        newAmendment.propagateScale = self.posingMultiplyScaleAllPartsAfter.Checked
        newAmendment.scaleMultiplier_pct = umath.intMax(0, umath.intMin(1000, StrToIntDef(self.posingScaleMultiplierEdit.Text, currentAmendment.scaleMultiplier_pct)))
        newAmendment.lengthMultiplier_pct = umath.intMax(0, umath.intMin(1000, StrToIntDef(self.posingLengthMultiplierEdit.Text, currentAmendment.lengthMultiplier_pct)))
        newAmendment.widthMultiplier_pct = umath.intMax(0, umath.intMin(1000, StrToIntDef(self.posingWidthMultiplierEdit.Text, currentAmendment.widthMultiplier_pct)))
        newCommand = updcom.PdEditAmendmentCommand().createWithPlantAndAmendmentAndField(self.focusedPlant(), newAmendment, field)
        self.doCommand(newCommand)
    
    def posingPosePartClick(self, Sender):
        newCommand = PdCommand()
        newAmendment = PdPlantDrawingAmendment()
        
        if self.focusedPlant() == None:
            return
        if self.selectedPlantPartID < 0:
            return
        if self.focusedPlant().amendmentForPartID(self.selectedPlantPartID) != None:
            # only one amendment per part id
            return
        # command will take ownership of this and free it if necessary
        newAmendment = uamendmt.PdPlantDrawingAmendment().create()
        newAmendment.partID = self.selectedPlantPartID
        newAmendment.typeOfPart = self.selectedPlantPartType
        newCommand = updcom.PdCreateAmendmentCommand().createWithPlantAndAmendment(self.focusedPlant(), newAmendment)
        self.doCommand(newCommand)
    
    def posingUnposePartClick(self, Sender):
        newCommand = PdCommand()
        amendment = PdPlantDrawingAmendment()
        
        if self.focusedPlant() == None:
            return
        amendment = self.focusedPlant().amendmentForPartID(self.selectedPartIDInAmendedPartsList())
        if amendment == None:
            return
        newCommand = updcom.PdDeleteAmendmentCommand().createWithPlantAndAmendment(self.focusedPlant(), amendment)
        self.doCommand(newCommand)
    
    def addAmendedPartToList(self, partID, partType):
        newString = ""
        selectNoneIndex = 0
        indexToSave = 0
        
        newString = MainForm.partDescriptionForIDAndType(partID, partType)
        self.posedPlantParts.Items.Add(newString)
        indexToSave = self.posedPlantParts.Items.Count - 1
        # add "select none" to end - move down if already there
        selectNoneIndex = self.posedPlantParts.Items.IndexOf(kSelectNoPosedPartString)
        if selectNoneIndex >= 0:
            self.posedPlantParts.Items.Delete(selectNoneIndex)
        self.posedPlantParts.Items.Add(kSelectNoPosedPartString)
        self.posedPlantParts.ItemIndex = indexToSave
        self.updatePosingForSelectedPlantPart()
    
    def removeAmendedPartFromList(self, partID, partType):
        oldString = ""
        index = 0
        oldItemIndex = 0
        
        oldItemIndex = self.posedPlantParts.ItemIndex
        oldString = self.partDescriptionForIDAndType(partID, partType)
        index = self.posedPlantParts.Items.IndexOf(oldString)
        if index >= 0:
            self.posedPlantParts.Items.Delete(index)
        if oldItemIndex <= self.posedPlantParts.Items.Count - 1:
            self.posedPlantParts.ItemIndex = oldItemIndex
        self.updatePosingForSelectedPlantPart()
    
    # ------------------------------------------------------------------------------------- *posing - supporting 
    def partDescriptionForIDAndType(self, id, typeName):
        result = ""
        result = IntToStr(id) + " (" + typeName + ")"
        return result
    
    def partIDForFullDescription(self, aString):
        result = 0L
        result = StrToIntDef(usupport.stringUpTo(aString, " ("), -1)
        return result
    
    def partTypeForFullDescription(self, aString):
        result = ""
        result = ""
        if len(aString) <= 0:
            return result
        result = usupport.stringBeyond(aString, "(")
        result = usupport.stringUpTo(result, ")")
        return result
    
    def selectedPartIDInAmendedPartsList(self):
        result = 0L
        result = -1
        if (self.focusedPlant() == None) or (self.posedPlantParts.Items.Count <= 0) or (self.posedPlantParts.ItemIndex < 0):
            return result
        result = self.partIDForFullDescription(self.posedPlantParts.Items[self.posedPlantParts.ItemIndex])
        return result
    
    def selectedPartTypeInAmendedPartsList(self):
        result = ""
        result = ""
        if (self.focusedPlant() == None) or (self.posedPlantParts.Items.Count <= 0) or (self.posedPlantParts.ItemIndex < 0):
            return result
        result = self.partTypeForFullDescription(self.posedPlantParts.Items[self.posedPlantParts.ItemIndex])
        return result
    
    # ------------------------------------------------------------------------------------- *resizing 
    def FormResize(self, Sender):
        newTop = 0
        newLeft = 0
        newWidth = 0
        newHeight = 0
        splitterWidthOrHeight = 0
        windowLock = false
        
        if delphi_compatability.Application.terminated:
            return
        if self.WindowState == delphi_compatability.TWindowState.wsMinimized:
            return
        if udomain.domain == None:
            return
        if self.drawingBitmap == None:
            return
        if self.selectedPlants == None:
            return
        self.horizontalSplitter.Visible = false
        self.verticalSplitter.Visible = false
        self.plantListPanel.Visible = false
        self.plantFocusPanel.Visible = false
        windowLock = UNRESOLVED.lockWindowUpdate(self.Handle)
        self.toolbarPanel.SetBounds(0, 0, self.ClientWidth, self.toolbarPanel.Height)
        #assumes they are equal, I have at 4 now
        splitterWidthOrHeight = self.verticalSplitter.Width
        if self.lastHeight != 0:
            newTop = intround(1.0 * self.horizontalSplitter.Top * self.ClientHeight / self.lastHeight)
        else:
            newTop = self.ClientHeight / 2
        newTop = umath.intMax(0, umath.intMin(self.ClientHeight - 1, newTop))
        newHeight = umath.intMax(0, self.ClientHeight - newTop - splitterWidthOrHeight)
        if self.lastWidth != 0:
            newLeft = intround(1.0 * self.verticalSplitter.Left * self.ClientWidth / self.lastWidth)
        else:
            newLeft = self.ClientWidth / 2
        newLeft = umath.intMax(0, umath.intMin(self.ClientWidth - 1, newLeft))
        newWidth = umath.intMax(0, self.ClientWidth - newLeft - splitterWidthOrHeight)
        if udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal:
            self.horizontalSplitter.SetBounds(0, newTop, self.ClientWidth, self.horizontalSplitter.Height)
            self.verticalSplitter.SetBounds(newLeft, newTop + self.horizontalSplitter.Height, self.verticalSplitter.Width, newHeight)
        elif udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical:
            self.verticalSplitter.SetBounds(newLeft, self.toolbarPanel.Height, self.verticalSplitter.Width, umath.intMax(0, self.ClientHeight - self.toolbarPanel.Height))
            self.horizontalSplitter.SetBounds(newLeft + self.verticalSplitter.Width, newTop, newWidth, self.horizontalSplitter.Height)
        # resize images and panels 
        self.resizePanelsToHorizontalSplitter()
        self.resizePanelsToVerticalSplitter()
        self.lastHeight = self.ClientHeight
        self.lastWidth = self.ClientWidth
        if windowLock:
            UNRESOLVED.lockWindowUpdate(0)
        self.horizontalSplitter.Visible = true
        self.verticalSplitter.Visible = true
        self.plantListPanel.Visible = true
        self.plantFocusPanel.Visible = true
    
    # resizing 
    def resizePanelsToVerticalSplitter(self):
        newLeft = 0
        newWidth = 0
        newTop = 0
        newHeight = 0
        
        newLeft = self.verticalSplitter.Left + self.verticalSplitter.Width
        newWidth = umath.intMax(0, self.ClientWidth - newLeft)
        newTop = self.horizontalSplitter.Top + self.horizontalSplitter.Height
        newHeight = umath.intMax(0, self.ClientHeight - newTop)
        if udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal:
            self.plantListPanel.SetBounds(0, newTop, self.verticalSplitter.Left, newHeight)
            self.plantFocusPanel.SetBounds(newLeft, newTop, newWidth, newHeight)
        elif udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical:
            self.plantListPanel.SetBounds(newLeft, self.toolbarPanel.Height, newWidth, self.horizontalSplitter.Top - self.toolbarPanel.Height)
            self.plantFocusPanel.SetBounds(newLeft, newTop, newWidth, newHeight)
            #don't change top here
            self.horizontalSplitter.SetBounds(newLeft, self.horizontalSplitter.Top, newWidth, self.horizontalSplitter.Height)
            self.drawingPaintBox.SetBounds(0, self.toolbarPanel.Height, newLeft, umath.intMax(0, self.ClientHeight - self.toolbarPanel.Height))
            self.resizeDrawingBitmapIfNecessary()
        self.resizePlantListPanel()
        self.resizePlantFocusPanel()
    
    def resizePanelsToHorizontalSplitter(self):
        newLeft = 0
        newWidth = 0
        newTop = 0
        newHeight = 0
        
        newLeft = self.verticalSplitter.Left + self.verticalSplitter.Width
        newWidth = umath.intMax(0, self.ClientWidth - newLeft)
        newTop = self.horizontalSplitter.Top + self.horizontalSplitter.Height
        newHeight = umath.intMax(0, self.ClientHeight - newTop)
        if udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal:
            self.plantListPanel.SetBounds(0, newTop, self.verticalSplitter.Left, newHeight)
            #don't change left here
            self.verticalSplitter.SetBounds(self.verticalSplitter.Left, newTop, self.verticalSplitter.Width, newHeight)
            self.plantFocusPanel.SetBounds(newLeft, newTop, newWidth, newHeight)
            self.drawingPaintBox.SetBounds(0, self.toolbarPanel.Height, self.ClientWidth, umath.intMax(0, self.horizontalSplitter.Top - self.toolbarPanel.Height))
            self.resizeDrawingBitmapIfNecessary()
        elif udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical:
            self.plantListPanel.SetBounds(newLeft, self.toolbarPanel.Height, newWidth, self.horizontalSplitter.Top - self.toolbarPanel.Height)
            self.plantFocusPanel.SetBounds(newLeft, newTop, newWidth, newHeight)
        self.resizePlantListPanel()
        self.resizePlantFocusPanel()
    
    def resizeDrawingBitmapIfNecessary(self):
        bitmapWasMadeBigger = false
        
        if (self.drawingBitmap.Width != self.drawingPaintBox.Width) or (self.drawingBitmap.Height != self.drawingPaintBox.Height):
            # if have to make bitmap larger, redraw all plants in case some were not drawing before
            # because they were off the bitmap
            bitmapWasMadeBigger = (self.drawingPaintBox.Width > self.drawingBitmap.Width) or (self.drawingPaintBox.Height > self.drawingBitmap.Height)
            ubmpsupport.resizeBitmap(self.drawingBitmap, Point(self.drawingPaintBox.Width, self.drawingPaintBox.Height))
            if not self.inFormCreation:
                if bitmapWasMadeBigger:
                    self.recalculateAllPlantBoundsRects(kDontDrawYet)
                self.invalidateEntireDrawing()
                self.updateForPossibleChangeToDrawing()
    
    def resizePlantListPanel(self):
        self.plantListDrawGrid.SetBounds(0, 0, self.plantListPanel.Width, self.plantListPanel.Height - self.plantFileChangedImage.Height - kBetweenGap * 2)
        self.plantListDrawGrid.DefaultColWidth = self.plantListDrawGrid.ClientWidth
        self.plantFileChangedImage.SetBounds(kBetweenGap, self.plantListDrawGrid.Top + self.plantListDrawGrid.Height + kBetweenGap, self.plantFileChangedImage.Width, self.plantFileChangedImage.Height)
        self.plantBitmapsIndicatorImage.SetBounds(self.plantFileChangedImage.Left + self.plantFileChangedImage.Width + kBetweenGap, self.plantFileChangedImage.Top, self.plantBitmapsIndicatorImage.Width, self.plantBitmapsIndicatorImage.Height)
        self.progressPaintBox.SetBounds(self.plantBitmapsIndicatorImage.Left + self.plantBitmapsIndicatorImage.Width + kBetweenGap, self.plantBitmapsIndicatorImage.Top + self.plantBitmapsIndicatorImage.Height / 2 - self.progressPaintBox.Height / 2, self.plantListPanel.Width - self.plantFileChangedImage.Width - self.plantBitmapsIndicatorImage.Width - kBetweenGap * 4, self.progressPaintBox.Height)
    
    def resizePlantFocusPanel(self):
        newTop = 0
        
        # FIX unresolved WITH expression: self.tabSet
        # tab set 
        self.SetBounds(0, self.plantFocusPanel.Height - self.Height, self.plantFocusPanel.Width, self.Height)
        # v1.4 change
        self.animatingLabel.SetBounds(umath.intMax(0, self.plantFocusPanel.Width - self.animatingLabel.Width - kBetweenGap), self.plantFocusPanel.Height - self.animatingLabel.Height - kBetweenGap, self.animatingLabel.Width, self.animatingLabel.Height)
        # life cycle panel 
        self.lifeCyclePanel.SetBounds(0, 0, self.plantFocusPanel.Width, umath.intMax(0, self.plantFocusPanel.Height - self.tabSet.height))
        # v1.4 change - 2
        self.lifeCycleEditPanel.Height = self.animateGrowth.Height + kBetweenGap * 2 - 2
        # v1.4 change +1, -1, -2
        self.lifeCycleEditPanel.SetBounds(1, umath.intMax(0, self.lifeCyclePanel.Height - self.lifeCycleEditPanel.Height - 1), self.lifeCyclePanel.Width - 2, self.lifeCycleEditPanel.Height)
        # rotations panel
        self.rotationsPanel.SetBounds(0, 0, self.lifeCyclePanel.Width, self.lifeCyclePanel.Height)
        # posing panel
        self.posingPanel.SetBounds(0, 0, self.lifeCyclePanel.Width, self.lifeCyclePanel.Height)
        newTop = self.posingPlantName.Top + self.posingPlantName.Height + kBetweenGap
        self.posingNotShown.SetBounds(self.posingPanel.Width - self.posingNotShown.Width - kBetweenGap, newTop, self.posingNotShown.Width, self.posingNotShown.Height)
        self.posingGhost.SetBounds(self.posingNotShown.Left - self.posingGhost.Width - kBetweenGap, newTop, self.posingGhost.Width, self.posingGhost.Height)
        self.posingHighlight.SetBounds(self.posingGhost.Left - self.posingHighlight.Width - kBetweenGap, newTop, self.posingHighlight.Width, self.posingHighlight.Height)
        newTop = self.posingNotShown.Top + self.posingNotShown.Height + kBetweenGap
        self.posedPartsLabel.SetBounds(kBetweenGap, newTop + (self.posedPlantParts.Height / 2 - self.posedPartsLabel.Height / 2), self.posedPartsLabel.Width, self.posedPartsLabel.Height)
        self.posedPlantParts.SetBounds(self.posedPartsLabel.Left + self.posedPartsLabel.Width + kBetweenGap, newTop, umath.intMax(10, self.posingPanel.Width - self.posedPartsLabel.Width - kBetweenGap * 3), self.posedPlantParts.Height)
        newTop = self.posedPlantParts.Top + self.posedPlantParts.Height + kBetweenGap
        # fix later
        self.selectedPartLabel.SetBounds(kBetweenGap, newTop + (self.posingUnposePart.Height / 2 - self.selectedPartLabel.Height / 2), self.selectedPartLabel.Width, self.selectedPartLabel.Height)
        newTop = self.selectedPartLabel.Top + self.selectedPartLabel.Height + kBetweenGap
        self.posingPosePart.SetBounds(kBetweenGap, newTop, self.posingPosePart.Width, self.posingPosePart.Height)
        self.posingUnposePart.SetBounds(self.posingPosePart.Left + self.posingPosePart.Width + kBetweenGap, newTop, self.posingUnposePart.Width, self.posingUnposePart.Height)
        newTop = self.posingUnposePart.Top + self.posingUnposePart.Height + kBetweenGap
        self.posingDetailsPanel.SetBounds(0, newTop, self.lifeCyclePanel.Width, umath.intMax(230, self.lifeCyclePanel.Height - newTop))
        # lifeCycleEditPanel 
        self.lifeCycleDaysEdit.SetBounds(self.ageAndSizeLabel.Width + kBetweenGap * 2, kBetweenGap, self.lifeCycleDaysEdit.Width, self.lifeCycleDaysEdit.Height)
        self.lifeCycleDaysSpin.SetBounds(self.lifeCycleDaysEdit.Left + self.lifeCycleDaysEdit.Width, kBetweenGap + self.lifeCycleDaysEdit.Height / 2 - self.lifeCycleDaysSpin.Height / 2, self.lifeCycleDaysSpin.Width, self.lifeCycleDaysSpin.Height)
        self.ageAndSizeLabel.SetBounds(kBetweenGap, umath.intMax(0, self.lifeCycleDaysEdit.Top + self.lifeCycleDaysEdit.Height / 2 - self.ageAndSizeLabel.Height / 2), self.ageAndSizeLabel.Width, self.ageAndSizeLabel.Height)
        self.daysAndSizeLabel.SetBounds(self.lifeCycleDaysSpin.Left + self.lifeCycleDaysSpin.Width + kBetweenGap, umath.intMax(0, self.lifeCycleDaysEdit.Top + self.lifeCycleDaysEdit.Height / 2 - self.daysAndSizeLabel.Height / 2), self.daysAndSizeLabel.Width, self.daysAndSizeLabel.Height)
        self.animateGrowth.SetBounds(self.lifeCycleEditPanel.Width - self.animateGrowth.Width - kBetweenGap, self.lifeCycleDaysEdit.Top, self.animateGrowth.Width, self.animateGrowth.Height)
        # above lifeCycleEditPanel 
        self.timeLabel.SetBounds(umath.intMax(0, self.lifeCyclePanel.Width / 2 - self.timeLabel.Width / 2), umath.intMax(0, self.lifeCycleEditPanel.Top - self.timeLabel.Height - kBetweenGap), self.timeLabel.Width, self.timeLabel.Height)
        self.lifeCycleGraphImage.SetBounds(kBetweenGap + self.maxSizeAxisLabel.Width + kBetweenGap, umath.intMax(1, self.selectedPlantNameLabel.Top + self.selectedPlantNameLabel.Height + kBetweenGap), umath.intMax(1, self.lifeCyclePanel.Width - self.maxSizeAxisLabel.Width - kBetweenGap * 3), umath.intMax(1, self.timeLabel.Top - self.selectedPlantNameLabel.Height - kBetweenGap * 2))
        self.maxSizeAxisLabel.SetBounds(kBetweenGap, umath.intMax(0, self.lifeCycleGraphImage.Top + self.lifeCycleGraphImage.Height / 2 - self.maxSizeAxisLabel.Height / 2), self.maxSizeAxisLabel.Width, self.maxSizeAxisLabel.Height)
        self.selectedPlantNameLabel.SetBounds(kBetweenGap, kBetweenGap, self.selectedPlantNameLabel.Width, self.selectedPlantNameLabel.Height)
        if (self.lifeCycleGraphImage.Picture.Bitmap.Width != self.lifeCycleGraphImage.Width) or (self.lifeCycleGraphImage.Picture.Bitmap.Height != self.lifeCycleGraphImage.Height):
            # with selectedPlantNameLabel do setBounds(lifeCycleGraphImage.left, kBetweenGap, width, height);
            ubmpsupport.resizeBitmap(self.lifeCycleGraphImage.Picture.Bitmap, Point(self.lifeCycleGraphImage.Width, self.lifeCycleGraphImage.Height))
        self.placeLifeCycleDragger()
        self.redrawLifeCycleGraph()
        self.resizeParametersPanel()
        # stats scroll box 
        self.statsScrollBox.SetBounds(0, 0, self.plantFocusPanel.Width, umath.intMax(0, self.plantFocusPanel.Height - self.tabSet.height))
        self.statsPanel.resizeElements()
        self.notePanel.SetBounds(0, 0, self.plantFocusPanel.Width, umath.intMax(0, self.plantFocusPanel.Height - self.tabSet.height))
        self.noteLabel.SetBounds(kBetweenGap, kBetweenGap, self.noteLabel.Width, self.noteLabel.Height)
        #kBetweenGap + noteEdit.height div 2 - height div 2, width, height);
        self.noteEdit.SetBounds(umath.intMax(0, self.notePanel.Width - self.noteEdit.Width - kBetweenGap), kBetweenGap, self.noteEdit.Width, self.noteEdit.Height)
        self.noteMemo.SetBounds(0, self.noteEdit.Height + kBetweenGap * 2, self.notePanel.Width, umath.intMax(0, self.notePanel.Height - self.noteEdit.Height - kBetweenGap * 2))
    
    def resizeParametersPanel(self):
        newTop = 0
        
        self.parametersPanel.SetBounds(0, 0, self.plantFocusPanel.Width, umath.intMax(0, self.plantFocusPanel.Height - self.tabSet.height))
        self.parametersPlantName.SetBounds(kBetweenGap, kBetweenGap, self.parametersPlantName.Width, self.parametersPlantName.Height)
        self.sectionsComboBox.SetBounds(kBetweenGap, self.parametersPlantName.Top + self.parametersPlantName.Height + kBetweenGap, self.parametersPanel.Width - kBetweenGap * 2, self.sectionsComboBox.Height)
        newTop = self.sectionsComboBox.Top + self.sectionsComboBox.Height + kBetweenGap
        self.parametersScrollBox.SetBounds(0, self.sectionsComboBox.Top + self.sectionsComboBox.Height + kBetweenGap, self.parametersPanel.Width, self.parametersPanel.Height - newTop)
        self.repositionParameterPanels()
    
    def placeLifeCycleDragger(self):
        firstPlant = PdPlant()
        fractionOfMaxAge = 0.0
        
        firstPlant = self.focusedPlant()
        fractionOfMaxAge = 0.0
        if firstPlant != None:
            try:
                fractionOfMaxAge = firstPlant.age / firstPlant.pGeneral.ageAtMaturity
            except:
                fractionOfMaxAge = 0.0
        self.lifeCycleDragger.SetBounds(self.lifeCycleGraphImage.Left + intround((self.lifeCycleGraphImage.Width - self.lifeCycleDragger.Width) * fractionOfMaxAge), self.lifeCycleGraphImage.Top + 1, self.lifeCycleDragger.Width, self.lifeCycleGraphImage.Height - 2)
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 300
        UNRESOLVED.ptMinTrackSize.y = 300
    
    # ------------------------------------------------------------------------------------- *splitting 
    def horizontalSplitterMouseDown(self, Sender, Button, Shift, X, Y):
        self.horizontalSplitterDragging = true
        self.horizontalSplitterStartPos = Y
        self.horizontalSplitterLastDrawPos = -1
        self.horizontalSplitterNeedToRedraw = true
    
    def horizontalSplitterMouseMove(self, Sender, Shift, X, Y):
        bottomLimit = 0
        
        if udomain.domain == None:
            return
        if udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal:
            bottomLimit = kSplitterDragToBottomMinPixelsInHorizMode
        elif udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical:
            bottomLimit = kSplitterDragToBottomMinPixelsInVertMode
        else:
            bottomLimit = kSplitterDragToBottomMinPixelsInHorizMode
        if self.horizontalSplitterDragging and (self.horizontalSplitter.Top + Y >= kSplitterDragToTopMinPixels) and (self.horizontalSplitter.Top + Y < self.ClientHeight - bottomLimit):
            self.undrawHorizontalSplitterLine()
            self.horizontalSplitterLastDrawPos = self.drawHorizontalSplitterLine(Y)
    
    def horizontalSplitterMouseUp(self, Sender, Button, Shift, X, Y):
        bottomLimit = 0
        
        if udomain.domain == None:
            return
        if udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal:
            bottomLimit = kSplitterDragToBottomMinPixelsInHorizMode
        elif udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical:
            bottomLimit = kSplitterDragToBottomMinPixelsInVertMode
        else:
            bottomLimit = kSplitterDragToBottomMinPixelsInHorizMode
        if self.horizontalSplitterDragging:
            self.undrawHorizontalSplitterLine()
            self.horizontalSplitter.Top = self.horizontalSplitter.Top - (self.horizontalSplitterStartPos - Y)
            if self.horizontalSplitter.Top < kSplitterDragToTopMinPixels:
                self.horizontalSplitter.Top = kSplitterDragToTopMinPixels
            if self.horizontalSplitter.Top > self.ClientHeight - bottomLimit:
                self.horizontalSplitter.Top = self.ClientHeight - bottomLimit
            self.resizePanelsToHorizontalSplitter()
            self.horizontalSplitterDragging = false
    
    # splitting 
    def drawHorizontalSplitterLine(self, pos):
        result = 0
        theDC = HDC()
        
        theDC = UNRESOLVED.getDC(0)
        result = self.ClientOrigin.Y + self.horizontalSplitter.Top + pos + 2
        UNRESOLVED.patBlt(theDC, self.ClientOrigin.X + self.horizontalSplitter.Left, result, self.horizontalSplitter.Width, 1, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
        self.horizontalSplitterNeedToRedraw = true
        return result
    
    def undrawHorizontalSplitterLine(self):
        theDC = HDC()
        
        if not self.horizontalSplitterNeedToRedraw:
            return
        theDC = UNRESOLVED.getDC(0)
        UNRESOLVED.patBlt(theDC, self.ClientOrigin.X + self.horizontalSplitter.Left, self.horizontalSplitterLastDrawPos, self.horizontalSplitter.Width, 1, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
        self.horizontalSplitterNeedToRedraw = false
    
    def verticalSplitterMouseDown(self, Sender, Button, Shift, X, Y):
        self.verticalSplitterDragging = true
        self.verticalSplitterStartPos = X
        self.verticalSplitterLastDrawPos = -1
        self.verticalSplitterNeedToRedraw = true
    
    def verticalSplitterMouseMove(self, Sender, Shift, X, Y):
        if self.verticalSplitterDragging and (self.verticalSplitter.Left + X >= kSplitterDragToLeftMinPixels) and (self.verticalSplitter.Left + X < self.ClientWidth - kSplitterDragToRightMinPixels):
            self.undrawVerticalSplitterLine()
            self.verticalSplitterLastDrawPos = self.drawVerticalSplitterLine(X)
    
    def verticalSplitterMouseUp(self, Sender, Button, Shift, X, Y):
        if self.verticalSplitterDragging:
            self.undrawVerticalSplitterLine()
            self.verticalSplitter.Left = self.verticalSplitter.Left - (self.verticalSplitterStartPos - X)
            if self.verticalSplitter.Left < kSplitterDragToLeftMinPixels:
                self.verticalSplitter.Left = kSplitterDragToLeftMinPixels
            if self.verticalSplitter.Left > self.ClientWidth - kSplitterDragToRightMinPixels:
                self.verticalSplitter.Left = self.ClientWidth - kSplitterDragToRightMinPixels
            self.resizePanelsToVerticalSplitter()
            self.verticalSplitterDragging = false
    
    def drawVerticalSplitterLine(self, pos):
        result = 0
        theDC = HDC()
        
        theDC = UNRESOLVED.getDC(0)
        result = self.ClientOrigin.X + self.verticalSplitter.Left + pos + 2
        UNRESOLVED.patBlt(theDC, result, self.ClientOrigin.Y + self.verticalSplitter.Top, 1, self.verticalSplitter.Height, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
        self.verticalSplitterNeedToRedraw = true
        return result
    
    def undrawVerticalSplitterLine(self):
        theDC = HDC()
        
        if not self.verticalSplitterNeedToRedraw:
            return
        theDC = UNRESOLVED.getDC(0)
        UNRESOLVED.patBlt(theDC, self.verticalSplitterLastDrawPos, self.ClientOrigin.Y + self.verticalSplitter.Top, 1, self.verticalSplitter.Height, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
        self.verticalSplitterNeedToRedraw = false
    
    # palette stuff 
    # ----------------------------------------------------------------------------- *palette stuff 
    def GetPalette(self):
        result = HPALETTE()
        result = self.paletteImage.Picture.Bitmap.Palette
        return result
    
    #overriden because paint box will not update correctly
    #makes window take first priority for palettes
    def PaletteChanged(self, Foreground):
        result = false
        oldPalette = HPALETTE()
        palette = HPALETTE()
        windowHandle = HWnd()
        DC = HDC()
        
        palette = self.GetPalette()
        if palette != 0:
            DC = self.GetDeviceContext(windowHandle)
            oldPalette = UNRESOLVED.selectPalette(DC, palette, not Foreground)
            if (UNRESOLVED.realizePalette(DC) != 0) and (not delphi_compatability.Application.terminated) and (self.drawingPaintBox != None):
                # if palette changed, repaint drawing 
                ubmpsupport.setPixelFormatBasedOnScreenForBitmap(self.drawingBitmap)
                self.drawingPaintBox.Invalidate()
            if self.statsPanel != None:
                self.statsPanel.Invalidate()
            UNRESOLVED.selectPalette(DC, oldPalette, true)
            UNRESOLVED.realizePalette(DC)
            UNRESOLVED.releaseDC(windowHandle, DC)
        result = PdForm.PaletteChanged(self, Foreground)
        return result
    
    def FormShow(self, Sender):
        UNRESOLVED.DragAcceptFiles(self.Handle, true)
    
    # v1.11
    def Reconcile3DObjects1Click(self, Sender):
        response = 0
        numTdosAdded = 0
        
        numTdosAdded = 0
        if plantFileChanged:
            # ask if want to save file first
            response = MessageDialog("Do you want to save your changes to " + ExtractFileName(udomain.domain.plantFileName) + chr(13) + "before you reconcile its 3D objects" + chr(13) + "with those in the current 3D object file?", mtConfirmation, mbYesNoCancel, 0)
            if response == delphi_compatability.IDCANCEL:
                return
            elif response == delphi_compatability.IDYES:
                self.MenuFileSaveClick(self)
            elif response == delphi_compatability.IDNO:
                pass
        if not udomain.domain.checkForExistingDefaultTdoLibrary():
            return
        if MessageDialog("You are about to add any 3D objects in the current plant file" + chr(13) + chr(13) + "    (" + udomain.domain.plantFileName + ")" + chr(13) + chr(13) + "that are not already in the current 3D object library" + chr(13) + chr(13) + "    (" + udomain.domain.defaultTdoLibraryFileName + ")" + chr(13) + chr(13) + "into that library. Do you want to go ahead?", mtConfirmation, [mbYes, mbNo, ], 0) == delphi_compatability.IDYES:
            numTdosAdded = udomain.domain.plantManager.reconcileFileWithTdoLibrary(udomain.domain.plantFileName, udomain.domain.defaultTdoLibraryFileName)
            if numTdosAdded <= 0:
                MessageDialog("All the 3D objects in the current plant file" + chr(13) + chr(13) + "    (" + udomain.domain.plantFileName + ")" + chr(13) + chr(13) + "were already in the current 3D object library" + chr(13) + chr(13) + "    (" + udomain.domain.defaultTdoLibraryFileName + ").", mtInformation, [mbOK, ], 0)
            else:
                MessageDialog(IntToStr(numTdosAdded) + " 3D objects from the current plant file" + chr(13) + chr(13) + "    (" + udomain.domain.plantFileName + ")" + chr(13) + chr(13) + "were copied to the current 3D object library" + chr(13) + chr(13) + "    (" + udomain.domain.defaultTdoLibraryFileName + ").", mtInformation, [mbOK, ], 0)
    
    # v1.60
    # end v1.11
    # v1.60 recent files menu
    # PDF PORT removed empty parens
    def updateFileMenuForOtherRecentFiles(self):
        i = 0
        numSet = 0
        shortcutString = ""
        atLeastOneFileNameExists = false
        showThis = false
        
        atLeastOneFileNameExists = false
        numSet = 0
        for i in range(0, udomain.kMaxRecentFiles):
            if numSet + 1 == 10:
                shortcutString = "1&0"
            else:
                shortcutString = "&" + IntToStr(numSet + 1)
            self.MenuFileReopen.items[i].caption = shortcutString + " " + udomain.domain.options.recentFiles[udomain.kMaxRecentFiles - 1 - i]
            showThis = (udomain.domain.options.recentFiles[udomain.kMaxRecentFiles - 1 - i] != "") and (FileExists(udomain.domain.options.recentFiles[udomain.kMaxRecentFiles - 1 - i]))
            self.MenuFileReopen.items[i].visible = showThis
            if showThis:
                numSet += 1
            if not atLeastOneFileNameExists:
                atLeastOneFileNameExists = showThis
        self.MenuFileReopen.enabled = atLeastOneFileNameExists
    
    # v1.60 recent files menu
    def Recent0Click(self, Sender):
        index = 0
        
        index = udomain.kMaxRecentFiles - 1 - self.MenuFileReopen.indexOf(Sender as UNRESOLVED.TMenuItem)
        if not FileExists(udomain.domain.options.recentFiles[index]):
            MessageDialog("Cannot find the file" + chr(13) + udomain.domain.options.recentFiles[index] + ".", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            return
        if not self.askForSaveAndProceed():
            return
        self.openFile(udomain.domain.options.recentFiles[index])
    
