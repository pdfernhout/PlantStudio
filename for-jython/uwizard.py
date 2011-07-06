# unit uwizard

from conversion_common import *
import ubmpsupport
import umain
import ucursor
import updcom
import utravers
import usupport
import uturtle
import udomain
import ubitmap
import utdo
import ucollect
import updform
import uplant
import delphi_compatability

# const
kMeristem_AlternateOrOpposite = 1
kMeristem_BranchIndex = 2
kMeristem_SecondaryBranching = 3
kMeristem_BranchAngle = 4
kInternode_Curviness = 5
kInternode_Length = 6
kLeaves_Scale = 7
kLeaves_PetioleLength = 8
kLeaves_Angle = 9
kLeaflets_Number = 10
kLeaflets_Shape = 11
kLeaflets_Spread = 12
kFlowers_NumPetals = 13
kFlowers_Scale = 14
kInflorDraw_NumFlowers = 15
kInflorDraw_Shape = 16
kInflorPlace_NumApical = 17
kInflorPlace_NumAxillary = 18
kInflorPlace_ApicalStalkLength = 19
kInflorPlace_AxillaryStalkLength = 20
kFruit_NumSections = 21
kFruit_Scale = 22
kInternode_Thickness = 23
kInflorDraw_Thickness = 24

# const
kStart = 0
kMeristems = 1
kInternodes = 2
kLeaves = 3
kCompoundLeaves = 4
kInflorescencesPlacement = 5
kInflorescences = 6
kFlowers = 7
kFruit = 8
kFinish = 9
kLastPanel = 9
kReloadVariables = true
kDontReloadVariables = false

# const
kPreviewSize = 110

# group indexes 
class TWizardForm(PdForm):
    def __init__(self):
        self.wizardNotebook = TNotebook()
        self.cancel = TButton()
        self.back = TButton()
        self.next = TButton()
        self.panelMeristemsLabel = TLabel()
        self.panelInternodesLabel = TLabel()
        self.panelLeavesLabel = TLabel()
        self.panelInflorDrawingLabel = TLabel()
        self.branchingLabel = TLabel()
        self.leavesAlternateOppositeLabel = TLabel()
        self.branchAngleLabel = TLabel()
        self.secondaryBranchingLabel = TLabel()
        self.curvinessLabel = TLabel()
        self.internodeLengthLabel = TLabel()
        self.leafTdosLabel = TLabel()
        self.leafScaleLabel = TLabel()
        self.leafAngleLabel = TLabel()
        self.petioleLengthLabel = TLabel()
        self.finishLabelFirst = TLabel()
        self.newPlantName = TEdit()
        self.finishLabelSecond = TLabel()
        self.finishLabelThird = TLabel()
        self.panelFinishLabel = TLabel()
        self.panelStartLabel = TLabel()
        self.introLabelThird = TLabel()
        self.panelFlowersLabel = TLabel()
        self.petalTdosLabel = TLabel()
        self.petalScaleLabel = TLabel()
        self.petalsNumberLabel = TLabel()
        self.fruitTdoLabel = TLabel()
        self.fruitSectionsNumberLabel = TLabel()
        self.fruitScaleLabel = TLabel()
        self.panelFruitsLabel = TLabel()
        self.inflorFlowersLabel = TLabel()
        self.inflorShapeLabel = TLabel()
        self.panelInflorPlacementLabel = TLabel()
        self.apicalInflorsNumberLabel = TLabel()
        self.axillaryInflorsNumberLabel = TLabel()
        self.apicalStalkLabel = TLabel()
        self.axillaryStalkLabel = TLabel()
        self.introLabelFirst = TLabel()
        self.apicalInflorExtraImage = TImage()
        self.axillaryInflorExtraImage = TImage()
        self.previewPanel = TPanel()
        self.internodesVeryShort = TSpeedButton()
        self.internodesShort = TSpeedButton()
        self.internodesMedium = TSpeedButton()
        self.internodesLong = TSpeedButton()
        self.internodesVeryLong = TSpeedButton()
        self.curvinessNone = TSpeedButton()
        self.curvinessLittle = TSpeedButton()
        self.curvinessSome = TSpeedButton()
        self.curvinessVery = TSpeedButton()
        self.leavesAlternate = TSpeedButton()
        self.leavesOpposite = TSpeedButton()
        self.branchNone = TSpeedButton()
        self.branchLittle = TSpeedButton()
        self.branchMedium = TSpeedButton()
        self.branchLot = TSpeedButton()
        self.secondaryBranchingYes = TSpeedButton()
        self.secondaryBranchingNo = TSpeedButton()
        self.branchAngleSmall = TSpeedButton()
        self.branchAngleMedium = TSpeedButton()
        self.branchAngleLarge = TSpeedButton()
        self.arrowLeavesAlternateOpposite = TImage()
        self.arrowBranching = TImage()
        self.arrowSecondaryBranching = TImage()
        self.arrowBranchAngle = TImage()
        self.arrowCurviness = TImage()
        self.arrowInternodeLength = TImage()
        self.arrowLeafScale = TImage()
        self.leafScaleTiny = TSpeedButton()
        self.leafScaleSmall = TSpeedButton()
        self.leafScaleMedium = TSpeedButton()
        self.leafScaleLarge = TSpeedButton()
        self.leafScaleHuge = TSpeedButton()
        self.arrowLeafAngle = TImage()
        self.leafAngleSmall = TSpeedButton()
        self.leafAngleMedium = TSpeedButton()
        self.leafAngleLarge = TSpeedButton()
        self.arrowPetioleLength = TImage()
        self.petioleVeryShort = TSpeedButton()
        self.petioleShort = TSpeedButton()
        self.petioleMedium = TSpeedButton()
        self.petioleLong = TSpeedButton()
        self.petioleVeryLong = TSpeedButton()
        self.arrowLeafTdos = TImage()
        self.petalsOne = TSpeedButton()
        self.petalsThree = TSpeedButton()
        self.petalsFour = TSpeedButton()
        self.petalsFive = TSpeedButton()
        self.petalsTen = TSpeedButton()
        self.petalScaleTiny = TSpeedButton()
        self.petalScaleSmall = TSpeedButton()
        self.petalScaleMedium = TSpeedButton()
        self.petalScaleLarge = TSpeedButton()
        self.petalScaleHuge = TSpeedButton()
        self.arrowPetalTdos = TImage()
        self.arrowPetalsNumber = TImage()
        self.arrowPetalScale = TImage()
        self.arrowInflorFlowers = TImage()
        self.arrowInflorShape = TImage()
        self.inflorFlowersOne = TSpeedButton()
        self.inflorFlowersTwo = TSpeedButton()
        self.inflorFlowersThree = TSpeedButton()
        self.inflorFlowersFive = TSpeedButton()
        self.inflorFlowersTen = TSpeedButton()
        self.inflorFlowersTwenty = TSpeedButton()
        self.inflorShapeSpike = TSpeedButton()
        self.inflorShapeRaceme = TSpeedButton()
        self.inflorShapePanicle = TSpeedButton()
        self.inflorShapeUmbel = TSpeedButton()
        self.inflorShapeHead = TSpeedButton()
        self.apicalInflorsNone = TSpeedButton()
        self.apicalInflorsOne = TSpeedButton()
        self.apicalInflorsTwo = TSpeedButton()
        self.apicalInflorsThree = TSpeedButton()
        self.apicalInflorsFive = TSpeedButton()
        self.arrowApicalInflorsNumber = TImage()
        self.axillaryInflorsNone = TSpeedButton()
        self.axillaryInflorsThree = TSpeedButton()
        self.axillaryInflorsFive = TSpeedButton()
        self.axillaryInflorsTen = TSpeedButton()
        self.axillaryInflorsTwenty = TSpeedButton()
        self.arrowAxillaryInflorsNumber = TImage()
        self.apicalStalkVeryShort = TSpeedButton()
        self.apicalStalkShort = TSpeedButton()
        self.apicalStalkMedium = TSpeedButton()
        self.apicalStalkLong = TSpeedButton()
        self.apicalStalkVeryLong = TSpeedButton()
        self.arrowApicalStalk = TImage()
        self.arrowAxillaryStalk = TImage()
        self.axillaryStalkVeryShort = TSpeedButton()
        self.axillaryStalkShort = TSpeedButton()
        self.axillaryStalkMedium = TSpeedButton()
        self.axillaryStalkLong = TSpeedButton()
        self.axillaryStalkVeryLong = TSpeedButton()
        self.arrowFruitTdo = TImage()
        self.arrowFruitSectionsNumber = TImage()
        self.arrowFruitScale = TImage()
        self.fruitSectionsOne = TSpeedButton()
        self.fruitSectionsThree = TSpeedButton()
        self.fruitSectionsFour = TSpeedButton()
        self.fruitSectionsFive = TSpeedButton()
        self.fruitSectionsTen = TSpeedButton()
        self.fruitScaleTiny = TSpeedButton()
        self.fruitScaleSmall = TSpeedButton()
        self.fruitScaleMedium = TSpeedButton()
        self.fruitScaleLarge = TSpeedButton()
        self.fruitScaleHuge = TSpeedButton()
        self.introLabelSecond = TLabel()
        self.panelCompoundLeavesLabel = TLabel()
        self.arrowLeaflets = TImage()
        self.leafletsLabel = TLabel()
        self.leafletsShapeLabel = TLabel()
        self.arrowLeafletsShape = TImage()
        self.leafletsOne = TSpeedButton()
        self.leafletsThree = TSpeedButton()
        self.leafletsFour = TSpeedButton()
        self.leafletsFive = TSpeedButton()
        self.leafletsSeven = TSpeedButton()
        self.leafletsPinnate = TSpeedButton()
        self.leafletsPalmate = TSpeedButton()
        self.arrowLeafletsSpacing = TImage()
        self.leafletSpacingLabel = TLabel()
        self.leafletSpacingClose = TSpeedButton()
        self.leafletSpacingMedium = TSpeedButton()
        self.leafletSpacingFar = TSpeedButton()
        self.leafTdosDraw = TDrawGrid()
        self.petalTdosDraw = TDrawGrid()
        self.sectionTdosDraw = TDrawGrid()
        self.defaultChoices = TButton()
        self.arrowInternodeWidth = TImage()
        self.internodeWidthLabel = TLabel()
        self.internodeWidthVeryThin = TSpeedButton()
        self.internodeWidthThin = TSpeedButton()
        self.internodeWidthMedium = TSpeedButton()
        self.internodeWidthThick = TSpeedButton()
        self.internodeWidthVeryThick = TSpeedButton()
        self.inflorShapeCluster = TSpeedButton()
        self.arrowInflorThickness = TImage()
        self.inflorThicknessLabel = TLabel()
        self.inflorWidthVeryThin = TSpeedButton()
        self.inflorWidthThin = TSpeedButton()
        self.inflorWidthMedium = TSpeedButton()
        self.inflorWidthThick = TSpeedButton()
        self.inflorWidthVeryThick = TSpeedButton()
        self.arrowPetalColor = TImage()
        self.petalColorLabel = TLabel()
        self.petalColor = TPanel()
        self.fruitColorLabel = TLabel()
        self.fruitColor = TPanel()
        self.arrowFruitColor = TImage()
        self.hiddenPicturesPanel = TPanel()
        self.startPageImage = TImage()
        self.meristemsPageImage = TImage()
        self.internodesPageImage = TImage()
        self.leavesPageImage = TImage()
        self.compoundLeavesPageImage = TImage()
        self.flowersPageImage = TImage()
        self.inflorDrawPageImage = TImage()
        self.inflorPlacePageImage = TImage()
        self.fruitsPageImage = TImage()
        self.finishPageImage = TImage()
        self.fruitColorExplainLabel = TLabel()
        self.flowerColorExplainLabel = TLabel()
        self.arrowShowFruits = TImage()
        self.showFruitsLabel = TLabel()
        self.showFruitsYes = TRadioButton()
        self.showFruitsNo = TRadioButton()
        self.previewLabel = TLabel()
        self.randomizePlant = TButton()
        self.inflorDrawPageImageDisabled = TImage()
        self.flowersPageImageDisabled = TImage()
        self.fruitsPageImageDisabled = TImage()
        self.turnLeft = TSpeedButton()
        self.turnRight = TSpeedButton()
        self.bottomBevel = TBevel()
        self.longHintsSuggestionLabel = TLabel()
        self.Label1 = TLabel()
        self.Label2 = TLabel()
        self.Label3 = TLabel()
        self.Label4 = TLabel()
        self.Label5 = TLabel()
        self.Label6 = TLabel()
        self.Label7 = TLabel()
        self.Label8 = TLabel()
        self.Label9 = TLabel()
        self.Label10 = TLabel()
        self.progressDrawGrid = TDrawGrid()
        self.Label11 = TLabel()
        self.Label12 = TLabel()
        self.helpButton = TSpeedButton()
        self.changeTdoLibrary = TSpeedButton()
        self.sectionTdoSelectedLabel = TLabel()
        self.petalTdoSelectedLabel = TLabel()
        self.leafTdoSelectedLabel = TLabel()
        self.startPicture = TImage()
        self.plant = PdPlant()
        self.tdos = TListCollection()
        self.plantHasInflorescences = false
        self.tdoSelectionChanged = false
        self.askedToSaveOptions = false
        self.previewPaintBox = PdPaintBoxWithPalette()
    
    #$R *.DFM
    # panels 
    # -------------------------------------------------------------------------------------------- creation/destruction 
    def create(self, AOwner):
        i = 0
        
        PdForm.create(self, AOwner)
        self.leafTdoSelectedLabel.Caption = ""
        self.petalTdoSelectedLabel.Caption = ""
        self.sectionTdoSelectedLabel.Caption = ""
        self.previewPaintBox = ubitmap.PdPaintBoxWithPalette().Create(self)
        self.previewPaintBox.Parent = self.previewPanel
        self.previewPaintBox.Align = delphi_compatability.TAlign.alClient
        self.previewPaintBox.OnPaint = self.previewPaintBoxPaint
        # initialize default plant 
        self.plant = uplant.PdPlant().create()
        self.plant.defaultAllParameters()
        self.plant.setName("New plant " + IntToStr(updcom.numPlantsCreatedThisSession + 1))
        updcom.numPlantsCreatedThisSession += 1
        self.newPlantName.Text = self.plant.getName()
        # initialize tdos 
        self.tdos = ucollect.TListCollection().Create()
        self.readTdosFromFile()
        if udomain.domain != None:
            for i in range(1, udomain.kMaxWizardQuestions + 1):
                # load info from domain on choices 
                self.setDownButtonForGroupIndexFromName(i, udomain.domain.options.wizardChoices[i])
        if udomain.domain.options.wizardShowFruit:
            # handle radio button choice separately 
            self.showFruitsYes.Checked = true
        else:
            self.showFruitsNo.Checked = true
        # colors are handled separately 
        self.petalColor.Color = udomain.domain.options.wizardColors[1]
        self.fruitColor.Color = udomain.domain.options.wizardColors[2]
        if not self.selectFirstTdoInDrawGridWithStringInName(self.leafTdosDraw, udomain.domain.options.wizardTdoNames[1]):
            # tdo choices are handled separately - if not found use defaults by type 
            self.selectFirstTdoInDrawGridWithStringInName(self.leafTdosDraw, "leaf")
        if not self.selectFirstTdoInDrawGridWithStringInName(self.petalTdosDraw, udomain.domain.options.wizardTdoNames[2]):
            self.selectFirstTdoInDrawGridWithStringInName(self.petalTdosDraw, "petal")
        if not self.selectFirstTdoInDrawGridWithStringInName(self.sectionTdosDraw, udomain.domain.options.wizardTdoNames[3]):
            self.selectFirstTdoInDrawGridWithStringInName(self.sectionTdosDraw, "section")
        self.updateForButtonInteractions()
        return self
    
    def FormCreate(self, Sender):
        self.startPicture.Picture.Bitmap.Palette = UNRESOLVED.CopyPalette(umain.MainForm.paletteImage.Picture.Bitmap.Palette)
        self.wizardNotebook.Invalidate()
        # assumes there is no border
        self.progressDrawGrid.DefaultColWidth = self.progressDrawGrid.Width / self.progressDrawGrid.ColCount
        self.progressDrawGrid.Width = self.progressDrawGrid.DefaultColWidth * self.progressDrawGrid.ColCount
        self.progressDrawGrid.DefaultRowHeight = self.progressDrawGrid.Height
        self.setPageIndex(0)
        self.updateProgress()
    
    def destroy(self):
        self.plant.free
        self.plant = None
        self.tdos.free
        self.tdos = None
        PdForm.destroy(self)
    
    # -------------------------------------------------------------------------------------------- *tdos 
    def hintForTdosDrawGridAtPoint(self, aComponent, aPoint, cursorRect):
        raise "method hintForTdosDrawGridAtPoint had assigned to var parameter cursorRect not added to return; fixup manually"
        result = ""
        grid = TDrawGrid()
        col = 0
        row = 0
        tdo = KfObject3D()
        
        result = ""
        if (aComponent == None) or (not (aComponent.__class__ is delphi_compatability.TDrawGrid)):
            return result
        grid = aComponent as delphi_compatability.TDrawGrid
        col, row = grid.MouseToCell(aPoint.X, aPoint.Y, col, row)
        if grid == self.progressDrawGrid:
            if col == kStart:
                result = "start"
            elif col == kMeristems:
                result = "meristems"
            elif col == kInternodes:
                result = "internodes"
            elif col == kLeaves:
                result = "leaves"
            elif col == kCompoundLeaves:
                result = "compound leaves"
            elif col == kFlowers:
                result = "flowers"
            elif col == kInflorescences:
                result = "inflorescence drawing"
            elif col == kInflorescencesPlacement:
                result = "inflorescence placement"
            elif col == kFruit:
                result = "fruit"
            elif col == kFinish:
                result = "finish"
        else:
            tdo = self.tdoForIndex(col)
            if tdo == None:
                return result
            result = tdo.getName()
        # change hint if cursor moves out of the current item's rectangle 
        cursorRect = grid.CellRect(col, row)
        return result
    
    def changeTdoLibraryClick(self, Sender):
        self.loadNewTdoLibrary()
        self.leafTdosDraw.Invalidate()
        self.petalTdosDraw.Invalidate()
        self.sectionTdosDraw.Invalidate()
    
    def loadNewTdoLibrary(self):
        fileNameWithPath = ""
        
        fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypeTdo, udomain.domain.defaultTdoLibraryFileName, "Choose a 3D object library (tdo) file")
        if fileNameWithPath == "":
            return
        udomain.domain.defaultTdoLibraryFileName = fileNameWithPath
        self.readTdosFromFile()
    
    def readTdosFromFile(self):
        newTdo = KfObject3D()
        inputFile = TextFile()
        
        self.tdos.clear()
        if udomain.domain == None:
            return
        if not udomain.domain.checkForExistingDefaultTdoLibrary():
            MessageDialog("Because you didn't choose a 3D object library, you will only" + chr(13) + "be able to use a default 3D object on your new plant." + chr(13) + chr(13) + "You can also choose a 3D object library" + chr(13) + "by clicking the 3D Objects button in the wizard.", mtWarning, [mbOK, ], 0)
            return
        AssignFile(inputFile, udomain.domain.defaultTdoLibraryFileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Reset(inputFile)
            while not UNRESOLVED.eof(inputFile):
                newTdo = utdo.KfObject3D().create()
                newTdo.readFromFileStream(inputFile, utdo.kInTdoLibrary)
                self.tdos.Add(newTdo)
        finally:
            CloseFile(inputFile)
            self.leafTdosDraw.ColCount = self.tdos.Count
            self.petalTdosDraw.ColCount = self.tdos.Count
            self.sectionTdosDraw.ColCount = self.tdos.Count
    
    def tdoForIndex(self, index):
        result = KfObject3D()
        result = None
        if (index >= 0) and (index <= self.tdos.Count - 1):
            result = utdo.KfObject3D(self.tdos.Items[index])
        return result
    
    def leafTdosDrawDrawCell(self, Sender, Col, Row, Rect, State):
        self.drawCellInTdoDrawGrid(self.leafTdosDraw, Col, UNRESOLVED.gdSelected in State, Rect)
    
    def petalTdosDrawDrawCell(self, Sender, Col, Row, Rect, State):
        self.drawCellInTdoDrawGrid(self.petalTdosDraw, Col, UNRESOLVED.gdSelected in State, Rect)
    
    def sectionTdosDrawDrawCell(self, Sender, Col, Row, Rect, State):
        self.drawCellInTdoDrawGrid(self.sectionTdosDraw, Col, UNRESOLVED.gdSelected in State, Rect)
    
    def drawCellInTdoDrawGrid(self, grid, column, selected, rect):
        tdo = KfObject3d()
        turtle = KfTurtle()
        bestPoint = TPoint()
        
        if not selected:
            grid.Canvas.Brush.Color = delphi_compatability.clWhite
            grid.Canvas.Font.Color = UNRESOLVED.clBtnText
        else:
            grid.Canvas.Brush.Color = UNRESOLVED.clHighlight
            grid.Canvas.Font.Color = UNRESOLVED.clHighlightText
        grid.Canvas.FillRect(Rect)
        tdo = None
        tdo = self.tdoForIndex(column)
        if tdo == None:
            return
        # draw tdo 
        turtle = uturtle.KfTurtle.defaultStartUsing()
        try:
            turtle.drawingSurface.pane = grid.Canvas
            turtle.setDrawOptionsForDrawingTdoOnly()
            # must be after pane and draw options set 
            turtle.reset()
            bestPoint = tdo.bestPointForDrawingAtScale(turtle, Point(Rect.left, Rect.top), Point(usupport.rWidth(Rect), usupport.rHeight(Rect)), 0.2)
            turtle.xyz(bestPoint.X, bestPoint.Y, 0)
            #turtle.xyz(rect.left + (rect.right - rect.left) div 2, rect.bottom - 5, 0);
            turtle.drawingSurface.recordingStart()
            #15);
            tdo.draw(turtle, 0.2, "", "", 0, 0)
            turtle.drawingSurface.recordingStop()
            turtle.drawingSurface.recordingDraw()
            turtle.drawingSurface.clearTriangles()
        finally:
            uturtle.KfTurtle.defaultStopUsing()
    
    # ---------------------------------------------------------------------------------------- interactions 
    def updateForButtonInteractions(self):
        hadInflors = false
        
        # do all of these at once, because then you can do them after loading options at startup
        #    (it doesn't take very long) 
        # meristems 
        self.arrowSecondaryBranching.Visible = not self.branchNone.Down
        self.secondaryBranchingLabel.Enabled = not self.branchNone.Down
        self.secondaryBranchingYes.Enabled = not self.branchNone.Down
        self.secondaryBranchingNo.Enabled = not self.branchNone.Down
        self.arrowBranchAngle.Visible = not self.branchNone.Down
        self.branchAngleLabel.Enabled = not self.branchNone.Down
        self.branchAngleSmall.Enabled = not self.branchNone.Down
        self.branchAngleMedium.Enabled = not self.branchNone.Down
        self.branchAngleLarge.Enabled = not self.branchNone.Down
        # internodes 
        # leaves 
        # compound leaves 
        self.arrowLeafletsShape.Visible = not self.leafletsOne.Down
        self.leafletsShapeLabel.Enabled = not self.leafletsOne.Down
        self.leafletsPinnate.Enabled = not self.leafletsOne.Down
        self.leafletsPalmate.Enabled = not self.leafletsOne.Down
        self.arrowLeafletsSpacing.Visible = not self.leafletsOne.Down
        self.leafletSpacingLabel.Enabled = not self.leafletsOne.Down
        self.leafletSpacingClose.Enabled = not self.leafletsOne.Down
        self.leafletSpacingMedium.Enabled = not self.leafletsOne.Down
        self.leafletSpacingFar.Enabled = not self.leafletsOne.Down
        # inflor placement 
        hadInflors = self.plantHasInflorescences
        self.plantHasInflorescences = (not self.apicalInflorsNone.Down) or (not self.axillaryInflorsNone.Down)
        if hadInflors != self.plantHasInflorescences:
            self.progressDrawGrid.Invalidate()
        self.arrowApicalStalk.Visible = not self.apicalInflorsNone.Down
        self.apicalStalkLabel.Enabled = not self.apicalInflorsNone.Down
        self.apicalStalkVeryShort.Enabled = not self.apicalInflorsNone.Down
        self.apicalStalkShort.Enabled = not self.apicalInflorsNone.Down
        self.apicalStalkMedium.Enabled = not self.apicalInflorsNone.Down
        self.apicalStalkLong.Enabled = not self.apicalInflorsNone.Down
        self.apicalStalkVeryLong.Enabled = not self.apicalInflorsNone.Down
        self.arrowAxillaryStalk.Visible = not self.axillaryInflorsNone.Down
        self.axillaryStalkLabel.Enabled = not self.axillaryInflorsNone.Down
        self.axillaryStalkVeryShort.Enabled = not self.axillaryInflorsNone.Down
        self.axillaryStalkShort.Enabled = not self.axillaryInflorsNone.Down
        self.axillaryStalkMedium.Enabled = not self.axillaryInflorsNone.Down
        self.axillaryStalkLong.Enabled = not self.axillaryInflorsNone.Down
        self.axillaryStalkVeryLong.Enabled = not self.axillaryInflorsNone.Down
        # inflor drawing 
        self.arrowInflorShape.Visible = not self.inflorFlowersOne.Down
        self.inflorShapeLabel.Enabled = not self.inflorFlowersOne.Down
        self.inflorShapeSpike.Enabled = not self.inflorFlowersOne.Down
        self.inflorShapeRaceme.Enabled = not self.inflorFlowersOne.Down
        self.inflorShapePanicle.Enabled = not self.inflorFlowersOne.Down
        self.inflorShapeUmbel.Enabled = not self.inflorFlowersOne.Down
        self.inflorShapeCluster.Enabled = not self.inflorFlowersOne.Down
        self.inflorShapeHead.Enabled = not self.inflorFlowersOne.Down
        # flowers 
        # fruit 
        self.arrowFruitTdo.Visible = not self.showFruitsNo.Checked
        self.fruitTdoLabel.Enabled = not self.showFruitsNo.Checked
        self.sectionTdosDraw.Visible = not self.showFruitsNo.Checked
        self.sectionTdoSelectedLabel.Visible = not self.showFruitsNo.Checked
        self.arrowFruitSectionsNumber.Visible = not self.showFruitsNo.Checked
        self.fruitSectionsNumberLabel.Enabled = not self.showFruitsNo.Checked
        self.fruitSectionsOne.Enabled = not self.showFruitsNo.Checked
        self.fruitSectionsThree.Enabled = not self.showFruitsNo.Checked
        self.fruitSectionsFour.Enabled = not self.showFruitsNo.Checked
        self.fruitSectionsFive.Enabled = not self.showFruitsNo.Checked
        self.fruitSectionsTen.Enabled = not self.showFruitsNo.Checked
        self.arrowFruitScale.Visible = not self.showFruitsNo.Checked
        self.fruitScaleLabel.Enabled = not self.showFruitsNo.Checked
        self.fruitScaleTiny.Enabled = not self.showFruitsNo.Checked
        self.fruitScaleSmall.Enabled = not self.showFruitsNo.Checked
        self.fruitScaleMedium.Enabled = not self.showFruitsNo.Checked
        self.fruitScaleLarge.Enabled = not self.showFruitsNo.Checked
        self.fruitScaleHuge.Enabled = not self.showFruitsNo.Checked
        self.arrowFruitColor.Visible = not self.showFruitsNo.Checked
        self.fruitColorLabel.Enabled = not self.showFruitsNo.Checked
        self.fruitColor.Visible = not self.showFruitsNo.Checked
        self.fruitColorExplainLabel.Enabled = not self.showFruitsNo.Checked
    
    def branchNoneClick(self, Sender):
        self.updateForButtonInteractions()
    
    def branchLittleClick(self, Sender):
        self.updateForButtonInteractions()
    
    def branchMediumClick(self, Sender):
        self.updateForButtonInteractions()
    
    def branchLotClick(self, Sender):
        self.updateForButtonInteractions()
    
    def leafletsOneClick(self, Sender):
        self.updateForButtonInteractions()
    
    def leafletsThreeClick(self, Sender):
        self.updateForButtonInteractions()
    
    def leafletsFourClick(self, Sender):
        self.updateForButtonInteractions()
    
    def leafletsFiveClick(self, Sender):
        self.updateForButtonInteractions()
    
    def leafletsSevenClick(self, Sender):
        self.updateForButtonInteractions()
    
    def inflorFlowersOneClick(self, Sender):
        self.updateForButtonInteractions()
    
    def inflorFlowersTwoClick(self, Sender):
        self.updateForButtonInteractions()
    
    def inflorFlowersThreeClick(self, Sender):
        self.updateForButtonInteractions()
    
    def inflorFlowersFiveClick(self, Sender):
        self.updateForButtonInteractions()
    
    def inflorFlowersTenClick(self, Sender):
        self.updateForButtonInteractions()
    
    def inflorFlowersTwentyClick(self, Sender):
        self.updateForButtonInteractions()
    
    def apicalInflorsNoneClick(self, Sender):
        self.updateForButtonInteractions()
    
    def apicalInflorsOneClick(self, Sender):
        self.updateForButtonInteractions()
    
    def apicalInflorsTwoClick(self, Sender):
        self.updateForButtonInteractions()
    
    def apicalInflorsThreeClick(self, Sender):
        self.updateForButtonInteractions()
    
    def apicalInflorsFiveClick(self, Sender):
        self.updateForButtonInteractions()
    
    def axillaryInflorsNoneClick(self, Sender):
        self.updateForButtonInteractions()
    
    def axillaryInflorsThreeClick(self, Sender):
        self.updateForButtonInteractions()
    
    def axillaryInflorsFiveClick(self, Sender):
        self.updateForButtonInteractions()
    
    def axillaryInflorsTenClick(self, Sender):
        self.updateForButtonInteractions()
    
    def axillaryInflorsTwentyClick(self, Sender):
        self.updateForButtonInteractions()
    
    def showFruitsYesClick(self, Sender):
        self.updateForButtonInteractions()
    
    def showFruitsNoClick(self, Sender):
        self.updateForButtonInteractions()
    
    # -------------------------------------------------------------------------------------------- transfer 
    def defaultChoicesClick(self, Sender):
        if MessageDialog("Are you sure you want to set all the wizard choices to defaults?" + chr(13) + chr(13) + "This action is not undoable.", mtConfirmation, [mbYes, mbNo, ], 0) == delphi_compatability.IDNO:
            return
        self.setDownButtonForGroupIndexFromName(kMeristem_AlternateOrOpposite, "leavesAlternate")
        self.setDownButtonForGroupIndexFromName(kMeristem_BranchIndex, "branchNone")
        self.setDownButtonForGroupIndexFromName(kInternode_Curviness, "curvinessLittle")
        self.setDownButtonForGroupIndexFromName(kInternode_Length, "internodesMedium")
        self.setDownButtonForGroupIndexFromName(kInternode_Thickness, "internodeWidthThin")
        self.setDownButtonForGroupIndexFromName(kLeaves_Scale, "leafScaleMedium")
        self.setDownButtonForGroupIndexFromName(kLeaves_PetioleLength, "petioleMedium")
        self.setDownButtonForGroupIndexFromName(kLeaves_Angle, "leafAngleMedium")
        self.setDownButtonForGroupIndexFromName(kLeaflets_Number, "leafletsOne")
        self.setDownButtonForGroupIndexFromName(kInflorPlace_NumApical, "apicalInflorsNone")
        self.setDownButtonForGroupIndexFromName(kInflorPlace_NumAxillary, "axillaryInflorsNone")
        self.updateForButtonInteractions()
        if self.wizardNotebook.PageIndex == kLastPanel:
            self.drawPreview(kReloadVariables)
    
    def selectFirstTdoInDrawGridWithStringInName(self, grid, aString):
        result = false
        indexToSelect = 0
        i = 0
        tdo = KfObject3D()
        gridRect = TGridRect()
        
        # returns true if a tdo was selected 
        result = false
        indexToSelect = -1
        if self.tdos.Count > 0:
            for i in range(0, self.tdos.Count):
                tdo = utdo.KfObject3D(self.tdos.Items[i])
                if tdo == None:
                    return result
                if UNRESOLVED.pos(uppercase(aString), uppercase(tdo.getName())) > 0:
                    indexToSelect = i
                    result = true
                    break
        if indexToSelect >= 0:
            gridRect.left = indexToSelect
            gridRect.right = indexToSelect
            gridRect.top = 0
            gridRect.bottom = 0
            grid.Selection = gridRect
            grid.LeftCol = indexToSelect
            if grid == self.leafTdosDraw:
                self.showTdoNameInLabel(indexToSelect, self.leafTdoSelectedLabel)
            elif grid == self.petalTdosDraw:
                self.showTdoNameInLabel(indexToSelect, self.petalTdoSelectedLabel)
            elif grid == self.sectionTdosDraw:
                self.showTdoNameInLabel(indexToSelect, self.sectionTdoSelectedLabel)
        return result
    
    def setPlantVariables(self):
        if self.plant == None:
            return
        self.plant.defaultAllParameters()
        # set variables in plant based on options 
        self.finishForMeristems()
        self.finishForInternodes()
        self.finishForLeaves()
        self.finishForCompoundLeaves()
        self.finishForInflorescencePlacement()
        self.finishForInflorescences()
        self.finishForFlowers()
        self.finishForFruit()
        self.plant.setName(self.newPlantName.Text)
        self.plant.setAge(self.plant.pGeneral.ageAtMaturity)
    
    def saveOptionsToDomain(self):
        i = 0
        
        for i in range(1, udomain.kMaxWizardQuestions + 1):
            udomain.domain.options.wizardChoices[i] = self.downButtonNameForGroupIndex(i)
        # handle radio button choice separately 
        udomain.domain.options.wizardShowFruit = self.showFruitsYes.Checked
        udomain.domain.options.wizardColors[1] = self.petalColor.Color
        udomain.domain.options.wizardColors[2] = self.fruitColor.Color
        if self.plant.pLeaf.leafTdoParams.object3D != None:
            udomain.domain.options.wizardTdoNames[1] = self.plant.pLeaf.leafTdoParams.object3D.getName()
        if self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].object3D != None:
            # cfk do first petal only in wizard, right?
            udomain.domain.options.wizardTdoNames[2] = self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].object3D.getName()
        if self.plant.pFruit.tdoParams.object3D != None:
            udomain.domain.options.wizardTdoNames[3] = self.plant.pFruit.tdoParams.object3D.getName()
    
    def optionsHaveChanged(self):
        result = false
        i = 0
        downButtonName = ""
        
        result = false
        for i in range(1, udomain.kMaxWizardQuestions + 1):
            downButtonName = self.downButtonNameForGroupIndex(i)
            if udomain.domain.options.wizardChoices[i] != "":
                result = result or (udomain.domain.options.wizardChoices[i] != downButtonName)
        result = result or (udomain.domain.options.wizardShowFruit != self.showFruitsYes.Checked)
        result = result or (udomain.domain.options.wizardColors[1] != self.petalColor.Color)
        result = result or (udomain.domain.options.wizardColors[2] != self.fruitColor.Color)
        result = result or self.tdoSelectionChanged
        return result
    
    def setDownButtonForGroupIndexFromName(self, aGroupIndex, aName):
        i = 0
        button = TSpeedButton()
        
        if aName == "":
            return
        if self.ComponentCount > 0:
            for i in range(0, self.ComponentCount):
                if not (self.Components[i].__class__ is delphi_compatability.TSpeedButton):
                    continue
                button = self.Components[i] as delphi_compatability.TSpeedButton
                if button.GroupIndex == aGroupIndex:
                    if button.Name == aName:
                        # only one can be down, so can exit when one is down 
                        button.Down = true
                        return
    
    def downButtonNameForGroupIndex(self, aGroupIndex):
        result = ""
        i = 0
        button = TSpeedButton()
        
        result = ""
        if self.ComponentCount > 0:
            for i in range(0, self.ComponentCount):
                if not (self.Components[i].__class__ is delphi_compatability.TSpeedButton):
                    continue
                button = self.Components[i] as delphi_compatability.TSpeedButton
                if (button.GroupIndex == aGroupIndex) and (button.Enabled):
                    if button.Down:
                        # if not enabled, don't want to match
                        # only one can be down, so can exit when one is down 
                        result = button.Name
                        return result
        return result
    
    def finishForMeristems(self):
        if self.leavesAlternate.Enabled:
            if self.leavesAlternate.Down:
                # alternate/opposite 
                self.plant.pMeristem.branchingAndLeafArrangement = uplant.kArrangementAlternate
            else:
                self.plant.pMeristem.branchingAndLeafArrangement = uplant.kArrangementOpposite
        if self.branchNone.Enabled:
            if self.branchNone.Down:
                # branching index 
                self.plant.pMeristem.branchingIndex = 0
            elif self.branchLittle.Down:
                self.plant.pMeristem.branchingIndex = 10
            elif self.branchMedium.Down:
                self.plant.pMeristem.branchingIndex = 30
            elif self.branchLot.Down:
                self.plant.pMeristem.branchingIndex = 80
        if self.secondaryBranchingYes.Enabled:
            # secondary branching 
            self.plant.pMeristem.secondaryBranchingIsAllowed = self.secondaryBranchingYes.Down
        if self.branchAngleSmall.Enabled:
            if self.branchAngleSmall.Down:
                # branch angle 
                self.plant.pMeristem.branchingAngle = 20
            elif self.branchAngleMedium.Down:
                self.plant.pMeristem.branchingAngle = 40
            elif self.branchAngleLarge.Down:
                self.plant.pMeristem.branchingAngle = 60
    
    def finishForInternodes(self):
        if self.curvinessNone.Enabled:
            if self.curvinessNone.Down:
                # curviness 
                self.plant.pInternode.curvingIndex = 0
                self.plant.pInternode.firstInternodeCurvingIndex = 0
            elif self.curvinessLittle.Down:
                self.plant.pInternode.curvingIndex = 10
                self.plant.pInternode.firstInternodeCurvingIndex = 5
            elif self.curvinessSome.Down:
                self.plant.pInternode.curvingIndex = 30
                self.plant.pInternode.firstInternodeCurvingIndex = 10
            elif self.curvinessVery.Down:
                self.plant.pInternode.curvingIndex = 50
                self.plant.pInternode.firstInternodeCurvingIndex = 20
        if self.internodesVeryShort.Enabled:
            if self.internodesVeryShort.Down:
                # length 
                self.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 1
            elif self.internodesShort.Down:
                self.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 10
            elif self.internodesMedium.Down:
                self.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 15
            elif self.internodesLong.Down:
                self.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 25
            elif self.internodesVeryLong.Down:
                self.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 50
        if self.internodeWidthVeryThin.Enabled:
            if self.internodeWidthVeryThin.Down:
                # width 
                self.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 0.5
            elif self.internodeWidthThin.Down:
                self.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 1
            elif self.internodeWidthMedium.Down:
                self.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 2
            elif self.internodeWidthThick.Down:
                self.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 3
            elif self.internodeWidthVeryThick.Down:
                self.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 10
    
    def finishForLeaves(self):
        tdo = KfObject3D()
        
        if self.leafScaleTiny.Enabled:
            if self.leafScaleTiny.Down:
                # scale 
                self.plant.pLeaf.leafTdoParams.scaleAtFullSize = 5
            elif self.leafScaleSmall.Down:
                self.plant.pLeaf.leafTdoParams.scaleAtFullSize = 20
            elif self.leafScaleMedium.Down:
                self.plant.pLeaf.leafTdoParams.scaleAtFullSize = 40
            elif self.leafScaleLarge.Down:
                self.plant.pLeaf.leafTdoParams.scaleAtFullSize = 60
            elif self.leafScaleHuge.Down:
                self.plant.pLeaf.leafTdoParams.scaleAtFullSize = 100
        if self.petioleVeryShort.Enabled:
            if self.petioleVeryShort.Down:
                # petiole length 
                self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 1
            elif self.petioleShort.Down:
                self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 10
            elif self.petioleMedium.Down:
                self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 20
            elif self.petioleLong.Down:
                self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 30
            elif self.petioleVeryLong.Down:
                self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 60
        if self.leafAngleSmall.Enabled:
            if self.leafAngleSmall.Down:
                # petiole angle 
                self.plant.pLeaf.petioleAngle = 20
            elif self.leafAngleMedium.Down:
                self.plant.pLeaf.petioleAngle = 40
            elif self.leafAngleLarge.Down:
                self.plant.pLeaf.petioleAngle = 60
        if self.leafTdosDraw.Visible:
            # tdo 
            tdo = self.tdoForIndex(self.leafTdosDraw.Selection.left)
            if (tdo != None) and (self.plant.pLeaf.leafTdoParams.object3D != None):
                self.plant.pLeaf.leafTdoParams.object3D.copyFrom(tdo)
    
    def finishForCompoundLeaves(self):
        if self.leafletsOne.Enabled:
            if self.leafletsOne.Down:
                # num leaflets 
                self.plant.pLeaf.compoundNumLeaflets = 1
            elif self.leafletsThree.Down:
                self.plant.pLeaf.compoundNumLeaflets = 3
            elif self.leafletsFour.Down:
                self.plant.pLeaf.compoundNumLeaflets = 4
            elif self.leafletsFive.Down:
                self.plant.pLeaf.compoundNumLeaflets = 5
            elif self.leafletsSeven.Down:
                self.plant.pLeaf.compoundNumLeaflets = 7
        if self.leafletsPinnate.Enabled:
            if self.leafletsPinnate.Down:
                # shape 
                self.plant.pLeaf.compoundPinnateOrPalmate = uplant.kCompoundLeafPinnate
            elif self.leafletsPalmate.Down:
                self.plant.pLeaf.compoundPinnateOrPalmate = uplant.kCompoundLeafPalmate
        if self.leafletSpacingClose.Enabled:
            if self.leafletSpacingClose.Down:
                # spread 
                self.plant.pLeaf.compoundRachisToPetioleRatio = 10.0
            elif self.leafletSpacingMedium.Down:
                self.plant.pLeaf.compoundRachisToPetioleRatio = 30.0
            elif self.leafletSpacingFar.Down:
                self.plant.pLeaf.compoundRachisToPetioleRatio = 50.0
    
    def finishForInflorescencePlacement(self):
        if self.apicalInflorsNone.Enabled:
            if self.apicalInflorsNone.Down:
                # num apical inflors 
                self.plant.pGeneral.numApicalInflors = 0
            elif self.apicalInflorsOne.Down:
                self.plant.pGeneral.numApicalInflors = 1
            elif self.apicalInflorsTwo.Down:
                self.plant.pGeneral.numApicalInflors = 2
            elif self.apicalInflorsThree.Down:
                self.plant.pGeneral.numApicalInflors = 3
            elif self.apicalInflorsFive.Down:
                self.plant.pGeneral.numApicalInflors = 5
        if self.axillaryInflorsNone.Enabled:
            if self.axillaryInflorsNone.Down:
                # num axillary inflors 
                self.plant.pGeneral.numAxillaryInflors = 0
            elif self.axillaryInflorsThree.Down:
                self.plant.pGeneral.numAxillaryInflors = 3
            elif self.axillaryInflorsFive.Down:
                self.plant.pGeneral.numAxillaryInflors = 5
            elif self.axillaryInflorsTen.Down:
                self.plant.pGeneral.numAxillaryInflors = 10
            elif self.axillaryInflorsTwenty.Down:
                self.plant.pGeneral.numAxillaryInflors = 20
        if self.apicalInflorsNone.Enabled and self.apicalInflorsNone.Down and self.axillaryInflorsNone.Enabled and self.axillaryInflorsNone.Down:
            # if no flowers, set age to allocate at max
            self.plant.pGeneral.ageAtWhichFloweringStarts = self.plant.pGeneral.ageAtMaturity + 1
        else:
            self.plant.pGeneral.ageAtWhichFloweringStarts = intround(self.plant.pGeneral.ageAtMaturity * 0.6)
        if self.apicalStalkVeryShort.Enabled:
            if self.apicalStalkVeryShort.Down:
                # apical stalk 
                self.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 1
            elif self.apicalStalkShort.Down:
                self.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 10
            elif self.apicalStalkMedium.Down:
                self.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 30
            elif self.apicalStalkLong.Down:
                self.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 50
            elif self.apicalStalkVeryLong.Down:
                self.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 100
        if self.axillaryStalkVeryShort.Enabled:
            if self.axillaryStalkVeryShort.Down:
                # axillary stalk (peduncle) 
                self.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 1
            elif self.axillaryStalkShort.Down:
                self.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 5
            elif self.axillaryStalkMedium.Down:
                self.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 10
            elif self.axillaryStalkLong.Down:
                self.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 15
            elif self.axillaryStalkVeryLong.Down:
                self.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 40
    
    def finishForInflorescences(self):
        numFlowers = 0
        
        if not self.plantHasInflorescences:
            return
        # num flowers 
        numFlowers = 0
        if self.inflorFlowersOne.Enabled:
            if self.inflorFlowersOne.Down:
                numFlowers = 1
            elif self.inflorFlowersTwo.Down:
                numFlowers = 2
            elif self.inflorFlowersThree.Down:
                numFlowers = 3
            elif self.inflorFlowersFive.Down:
                numFlowers = 5
            elif self.inflorFlowersTen.Down:
                numFlowers = 10
            elif self.inflorFlowersTwenty.Down:
                numFlowers = 20
        self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = numFlowers
        self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0
        self.plant.pInflor[uplant.kGenderFemale].numBranches = 0
        if self.inflorShapeSpike.Enabled:
            if self.inflorShapeSpike.Down:
                # shape 
                self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = numFlowers
                self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0
                self.plant.pInflor[uplant.kGenderFemale].numBranches = 0
                self.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 1
                self.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 30
                self.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 10
                self.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true
            elif self.inflorShapeRaceme.Down:
                self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = numFlowers
                self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0
                self.plant.pInflor[uplant.kGenderFemale].numBranches = 0
                self.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 20
                self.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 45
                self.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 10
                self.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true
            elif self.inflorShapePanicle.Down:
                if numFlowers == 1:
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 1
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0
                    self.plant.pInflor[uplant.kGenderFemale].numBranches = 0
                elif numFlowers == 2:
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 0
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 1
                    self.plant.pInflor[uplant.kGenderFemale].numBranches = 2
                elif numFlowers == 3:
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 1
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 1
                    self.plant.pInflor[uplant.kGenderFemale].numBranches = 2
                elif numFlowers == 5:
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 1
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 2
                    self.plant.pInflor[uplant.kGenderFemale].numBranches = 2
                elif numFlowers == 10:
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 1
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 3
                    self.plant.pInflor[uplant.kGenderFemale].numBranches = 3
                elif numFlowers == 20:
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 4
                    self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 4
                    self.plant.pInflor[uplant.kGenderFemale].numBranches = 4
                self.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 15
                self.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 30
                self.plant.pInflor[uplant.kGenderFemale].branchAngle = 35
                self.plant.pInflor[uplant.kGenderFemale].branchesAreAlternate = true
                self.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 7
                self.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true
            elif self.inflorShapeUmbel.Down:
                self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 0
                self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 1
                self.plant.pInflor[uplant.kGenderFemale].numBranches = numFlowers
                self.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 20
                self.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 20
                self.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 0.0
                self.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true
            elif self.inflorShapeCluster.Down:
                self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 0
                self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 1
                self.plant.pInflor[uplant.kGenderFemale].numBranches = numFlowers
                self.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true
                self.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 3
                self.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 1
                self.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 25
            elif self.inflorShapeHead.Down:
                self.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = numFlowers
                self.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0
                self.plant.pInflor[uplant.kGenderFemale].numBranches = 0
                self.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 10
                self.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 0
                self.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 10
                self.plant.pInflor[uplant.kGenderFemale].isHead = true
                self.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = false
        if self.inflorWidthVeryThin.Enabled:
            if self.inflorWidthVeryThin.Down:
                # width 
                self.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 0.5
            elif self.inflorWidthThin.Down:
                self.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 1
            elif self.inflorWidthMedium.Down:
                self.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 2
            elif self.inflorWidthThick.Down:
                self.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 3
            elif self.inflorWidthVeryThick.Down:
                self.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 10
    
    def finishForFlowers(self):
        tdo = KfObject3D()
        
        if not self.plantHasInflorescences:
            return
        if self.petalsOne.Enabled:
            if self.petalsOne.Down:
                # cfk only first petals for wizard?
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 1
            elif self.petalsThree.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 3
            elif self.petalsFour.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 4
            elif self.petalsFive.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 5
            elif self.petalsTen.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 10
        if self.petalScaleTiny.Enabled:
            if self.petalScaleTiny.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 4
            elif self.petalScaleSmall.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 10
            elif self.petalScaleMedium.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 20
            elif self.petalScaleLarge.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 30
            elif self.petalScaleHuge.Down:
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 60
        if self.petalColor.Visible:
            self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].faceColor = self.petalColor.Color
            self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].backfaceColor = usupport.darkerColor(self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].faceColor)
            self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kBud].faceColor = self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].faceColor
            self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kBud].backfaceColor = self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].backfaceColor
        if self.petalTdosDraw.Visible:
            tdo = self.tdoForIndex(self.petalTdosDraw.Selection.left)
            if (tdo != None) and (self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].object3D != None):
                # cfk first petals again
                self.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].object3D.copyFrom(tdo)
    
    def finishForFruit(self):
        tdo = KfObject3D()
        
        if not self.plantHasInflorescences:
            return
        if self.showFruitsNo.Enabled:
            if self.showFruitsNo.Checked:
                self.plant.pFlower[uplant.kGenderFemale].minDaysBeforeSettingFruit = 200
            else:
                self.plant.pFlower[uplant.kGenderFemale].minDaysBeforeSettingFruit = 3
        if self.fruitSectionsOne.Enabled:
            if self.fruitSectionsOne.Down:
                # num sections 
                self.plant.pFruit.tdoParams.repetitions = 1
            elif self.fruitSectionsThree.Down:
                self.plant.pFruit.tdoParams.repetitions = 3
            elif self.fruitSectionsFour.Down:
                self.plant.pFruit.tdoParams.repetitions = 4
            elif self.fruitSectionsFive.Down:
                self.plant.pFruit.tdoParams.repetitions = 5
            elif self.fruitSectionsTen.Down:
                self.plant.pFruit.tdoParams.repetitions = 10
        if self.fruitScaleTiny.Enabled:
            if self.fruitScaleTiny.Down:
                # scale 
                self.plant.pFruit.tdoParams.scaleAtFullSize = 4
            elif self.fruitScaleSmall.Down:
                self.plant.pFruit.tdoParams.scaleAtFullSize = 10
            elif self.fruitScaleMedium.Down:
                self.plant.pFruit.tdoParams.scaleAtFullSize = 20
            elif self.fruitScaleLarge.Down:
                self.plant.pFruit.tdoParams.scaleAtFullSize = 30
            elif self.fruitScaleHuge.Down:
                self.plant.pFruit.tdoParams.scaleAtFullSize = 60
        if self.fruitColor.Visible:
            self.plant.pFruit.tdoParams.faceColor = self.fruitColor.Color
            self.plant.pFruit.tdoParams.backfaceColor = usupport.darkerColor(self.plant.pFruit.tdoParams.faceColor)
            self.plant.pFruit.tdoParams.alternateFaceColor = self.plant.pFruit.tdoParams.faceColor
            self.plant.pFruit.tdoParams.alternateBackfaceColor = self.plant.pFruit.tdoParams.backfaceColor
        if self.sectionTdosDraw.Visible:
            tdo = self.tdoForIndex(self.sectionTdosDraw.Selection.left)
            if (tdo != None) and (self.plant.pFruit.tdoParams.object3D != None):
                self.plant.pFruit.tdoParams.object3D.copyFrom(tdo)
    
    # ------------------------------------------------------------------------------------------- *preview 
    def drawPreview(self, reloadVariables):
        if self.plant == None:
            return
        if reloadVariables:
            self.setPlantVariables()
        try:
            # always update cache in case any params have changed 
            ucursor.cursor_startWait()
            # want nice drawing here, only case
            self.plant.useBestDrawingForPreview = true
            self.plant.drawPreviewIntoCache(Point(self.previewPaintBox.Width, self.previewPaintBox.Height), uplant.kDontConsiderDomainScale, umain.kDrawNow)
            self.plant.previewCache.Transparent = false
        finally:
            ucursor.cursor_stopWait()
        self.previewPaintBox.Invalidate()
    
    def previewPaintBoxPaint(self, Sender):
        if (self.plant != None) and (self.plant.previewCache != None):
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(self.plant.previewCache, self.previewPaintBox.Canvas, Rect(0, 0, 0, 0))
    
    def randomizePlantClick(self, Sender):
        self.plant.randomize()
        self.drawPreview(kDontReloadVariables)
    
    def turnLeftClick(self, Sender):
        if self.plant == None:
            return
        self.plant.xRotation = self.plant.xRotation - 10
        if self.plant.xRotation < -360:
            self.plant.xRotation = 360
        self.drawPreview(kDontReloadVariables)
    
    def turnRightClick(self, Sender):
        if self.plant == None:
            return
        self.plant.xRotation = self.plant.xRotation + 10
        if self.plant.xRotation > 360:
            self.plant.xRotation = -360
        self.drawPreview(kDontReloadVariables)
    
    # -------------------------------------------------------------------------------------------- buttons/notebook 
    def setPageIndex(self, newIndex):
        self.wizardNotebook.PageIndex = newIndex
    
    def backClick(self, Sender):
        if self.wizardNotebook.PageIndex > 0:
            if self.wizardNotebook.PageIndex == kFinish:
                if self.plantHasInflorescences:
                    self.setPageIndex(kFruit)
                else:
                    self.setPageIndex(kInflorescencesPlacement)
            else:
                self.setPageIndex(self.wizardNotebook.PageIndex - 1)
        self.updateProgress()
    
    def nextClick(self, Sender):
        if self.wizardNotebook.PageIndex < kLastPanel:
            if self.wizardNotebook.PageIndex == kInflorescencesPlacement:
                if self.plantHasInflorescences:
                    self.setPageIndex(kInflorescences)
                else:
                    self.setPageIndex(kFinish)
            else:
                self.setPageIndex(self.wizardNotebook.PageIndex + 1)
            self.updateProgress()
        else:
            self.setPlantVariables()
            self.saveOptionsToDomain()
            self.plant.shrinkPreviewCache()
            self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def FormClose(self, Sender, Action):
        response = 0
        
        if (self.optionsHaveChanged()) and (self.ModalResult == mrCancel):
            # same as cancel, but if they click cancel on dialog, we must change action
            response = MessageDialog("Do you want to save the changes you made" + chr(13) + "to the wizard options?", mtConfirmation, [mbYes, mbNo, mbCancel, ], 0)
            if response == delphi_compatability.IDYES:
                self.saveOptionsToDomain()
                Action = delphi_compatability.TCloseAction.caFree
            elif response == delphi_compatability.IDNO:
                Action = delphi_compatability.TCloseAction.caFree
            elif response == delphi_compatability.IDCANCEL:
                Action = delphi_compatability.TCloseAction.caNone
    
    def updateProgress(self):
        self.progressDrawGrid.Invalidate()
        self.progressDrawGrid.Refresh()
        if self.wizardNotebook.PageIndex == kLastPanel:
            self.previewPaintBox.Visible = false
            delphi_compatability.Application.ProcessMessages()
            self.drawPreview(kReloadVariables)
            self.previewPaintBox.Visible = true
    
    def progressDrawGridDrawCell(self, Sender, Col, Row, Rect, State):
        bitmap = TBitmap()
        bitmapRect = TRect()
        
        # need this to make bitmaps come on as transparent
        self.progressDrawGrid.Canvas.Brush.Color = UNRESOLVED.clBtnFace
        self.progressDrawGrid.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear
        self.progressDrawGrid.Canvas.FillRect(Rect)
        bitmap = self.bitmapForProgressPage(Col)
        bitmapRect.Left = Rect.left + usupport.rWidth(Rect) / 2 - bitmap.Width / 2
        bitmapRect.Right = bitmapRect.Left + bitmap.Width
        bitmapRect.Top = Rect.top + usupport.rHeight(Rect) / 2 - bitmap.Height / 2
        bitmapRect.Bottom = bitmapRect.Top + bitmap.Height
        if bitmap != None:
            self.progressDrawGrid.Canvas.Draw(bitmapRect.Left, bitmapRect.Top, bitmap)
        if Col == self.wizardNotebook.PageIndex:
            self.progressDrawGrid.Canvas.Pen.Color = delphi_compatability.clRed
            self.progressDrawGrid.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
            self.progressDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
            # FIX unresolved WITH expression: Rect
            self.progressDrawGrid.Canvas.Rectangle(self.Left, self.Top, UNRESOLVED.right, UNRESOLVED.bottom)
    
    def bitmapForProgressPage(self, page):
        result = TBitmap()
        result = None
        if page == kStart:
            result = self.startPageImage.Picture.Bitmap
        elif page == kMeristems:
            result = self.meristemsPageImage.Picture.Bitmap
        elif page == kInternodes:
            result = self.internodesPageImage.Picture.Bitmap
        elif page == kLeaves:
            result = self.leavesPageImage.Picture.Bitmap
        elif page == kCompoundLeaves:
            result = self.compoundLeavesPageImage.Picture.Bitmap
        elif page == kInflorescencesPlacement:
            result = self.inflorPlacePageImage.Picture.Bitmap
        elif page == kInflorescences:
            if self.plantHasInflorescences:
                result = self.inflorDrawPageImage.Picture.Bitmap
            else:
                result = self.inflorDrawPageImageDisabled.Picture.Bitmap
        elif page == kFlowers:
            if self.plantHasInflorescences:
                result = self.flowersPageImage.Picture.Bitmap
            else:
                result = self.flowersPageImageDisabled.Picture.Bitmap
        elif page == kFruit:
            if self.plantHasInflorescences:
                result = self.fruitsPageImage.Picture.Bitmap
            else:
                result = self.fruitsPageImageDisabled.Picture.Bitmap
        elif page == kFinish:
            result = self.finishPageImage.Picture.Bitmap
        return result
    
    def progressDrawGridSelectCell(self, Sender, Col, Row, CanSelect):
        if ((Col == kInflorescences) or (Col == kFlowers) or (Col == kFruit)) and (not self.plantHasInflorescences):
            CanSelect = false
        else:
            self.setPageIndex(Col)
            self.updateProgress()
        return CanSelect
    
    def wizardNotebookPageChanged(self, Sender):
        if self.wizardNotebook.PageIndex == 0:
            self.back.Enabled = false
            self.next.Enabled = true
            self.next.Caption = "&Next >"
        elif self.wizardNotebook.PageIndex == kLastPanel:
            self.back.Enabled = true
            self.next.Caption = "&Finish"
        else :
            self.back.Enabled = true
            self.next.Enabled = true
            self.next.Caption = "&Next >"
    
    def petalColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.petalColor.Color = udomain.domain.getColorUsingCustomColors(self.petalColor.Color)
    
    def fruitColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.fruitColor.Color = udomain.domain.getColorUsingCustomColors(self.fruitColor.Color)
    
    def leafTdosDrawSelectCell(self, Sender, Col, Row, CanSelect):
        if (Col != self.leafTdosDraw.Selection.left):
            self.tdoSelectionChanged = true
            self.showTdoNameInLabel(Col, self.leafTdoSelectedLabel)
        return CanSelect
    
    def petalTdosDrawSelectCell(self, Sender, Col, Row, CanSelect):
        if (Col != self.petalTdosDraw.Selection.left):
            self.tdoSelectionChanged = true
            self.showTdoNameInLabel(Col, self.petalTdoSelectedLabel)
        return CanSelect
    
    def sectionTdosDrawSelectCell(self, Sender, Col, Row, CanSelect):
        if (Col != self.sectionTdosDraw.Selection.left):
            self.tdoSelectionChanged = true
            self.showTdoNameInLabel(Col, self.sectionTdoSelectedLabel)
        return CanSelect
    
    def sectionTdosDrawMouseMove(self, Sender, Shift, X, Y):
        pass
        #var col, row: integer;
        #sectionTdosDraw.mouseToCell(x, y, col, row);
        #if (col <> sectionTdosDraw.selection.left) then
        #  self.showTdoNameInLabel(col, sectionTdoSelectedLabel);
    
    def showTdoNameInLabel(self, index, aLabel):
        tdo = KfObject3D()
        
        tdo = None
        if (index >= 0) and (index <= self.tdos.Count - 1):
            tdo = utdo.KfObject3D(self.tdos.Items[index])
        if tdo != None:
            aLabel.Caption = tdo.getName()
        else:
            aLabel.Caption = ""
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Making_a_new_plant_with_the_wizard")
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
