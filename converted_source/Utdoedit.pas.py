# unit Utdoedit

from conversion_common import *
import ubmpsupport
import uwait
import usupport
import umath
import ucursor
import updcom
import umain
import udomain
import uturtle
import updform
import uparams
import ucommand
import utdo
import delphi_compatability

# const
kSplitterDragToTopMinPixels = 50
kSplitterDragToBottomMinPixels = 50
kSplitterDragToLeftMinPixels = 100
kSplitterDragToRightMinPixels = 50
kBetweenGap = 4
kDrawAsLeaf = 0
kDrawAsFlower = 1
kDrawAsFruit = 2
kCursorModeScroll = 0
kCursorModeMagnify = 1
kCursorModeRotate = 2
kCursorModeAddTriangles = 3
kCursorModeDeleteTriangles = 4
kCursorModeDragPoints = 5
kCursorModeFlipTriangles = 6
kLineColor = delphi_compatability.clBlack
kLightUpColor = delphi_compatability.clRed
kConnectedPointColor = delphi_compatability.clBlue
kUnconnectedPointColor = delphi_compatability.clGreen
kOriginPointColor = delphi_compatability.clBlack

# var
TdoEditorForm = TTdoEditorForm()

class PdTdoPaintBox(TPaintBox):
    def __init__(self):
        self.bitmap = TBitmap()
        self.canRotate = false
        self.draggingIn = false
        self.scale = 0.0
        self.xRotation = 0.0
        self.yRotation = 0.0
        self.zRotation = 0.0
        self.drawPosition = TPoint()
        self.startDragPosition = TPoint()
        self.tdoBoundsRect = TRect()
    
    #$R *.DFM
    # --------------------------------------------------------------------------------- PdTdoImage 
    def create(self, anOwner):
        TPaintBox.create(self, anOwner)
        self.bitmap = delphi_compatability.TBitmap().Create()
        return self
    
    def destroy(self):
        self.bitmap.free
        self.bitmap = None
        TPaintBox.destroy(self)
    
    def magnifyOrReduce(self, newScale, clickPoint):
        self.drawPosition.X = intround(clickPoint.X + (self.drawPosition.X - clickPoint.X) * newScale / self.scale)
        self.drawPosition.Y = intround(clickPoint.Y + (self.drawPosition.Y - clickPoint.Y) * newScale / self.scale)
        self.scale = newScale
        self.Paint()
    
    def centerTdo(self):
        xScale = 0.0
        yScale = 0.0
        newScale = 0.0
        turtle = KfTurtle()
        
        xScale = umath.safedivExcept(0.75 * self.scale * self.Width, usupport.rWidth(self.tdoBoundsRect), 0.1)
        yScale = umath.safedivExcept(0.75 * self.scale * self.Height, usupport.rHeight(self.tdoBoundsRect), 0.1)
        newScale = umath.min(xScale, yScale)
        if TdoEditorForm.tdo != None:
            turtle = uturtle.KfTurtle.defaultStartUsing()
            try:
                self.drawPosition = TdoEditorForm.tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(self.Width, self.Height), newScale)
            finally:
                uturtle.KfTurtle.defaultStopUsing()
        else:
            self.drawPosition = Point(self.Width / 2, self.Height - 10)
        self.magnifyOrReduce(newScale, self.drawPosition)
    
    def resetRotations(self):
        self.xRotation = 0
        self.yRotation = 0
        self.zRotation = 0
        self.Paint()
    
class TTdoEditorForm(PdForm):
    def __init__(self):
        self.ok = TButton()
        self.cancel = TButton()
        self.undoLast = TButton()
        self.redoLast = TButton()
        self.toolbarPanel = TPanel()
        self.dragCursorMode = TSpeedButton()
        self.magnifyCursorMode = TSpeedButton()
        self.scrollCursorMode = TSpeedButton()
        self.addTrianglePointsCursorMode = TSpeedButton()
        self.removeTriangleCursorMode = TSpeedButton()
        self.flipTriangleCursorMode = TSpeedButton()
        self.rotateCursorMode = TSpeedButton()
        self.optionsPanel = TPanel()
        self.fillTriangles = TCheckBox()
        self.plantParts = TSpinEdit()
        self.drawAsLabel = TLabel()
        self.picturesPanel = TPanel()
        self.verticalSplitter = TPanel()
        self.horizontalSplitter = TPanel()
        self.drawLines = TCheckBox()
        self.writeToDXF = TButton()
        self.renameTdo = TButton()
        self.Label1 = TLabel()
        self.circlePointSize = TSpinEdit()
        self.helpButton = TSpeedButton()
        self.mirrorTdo = TSpeedButton()
        self.reverseZValues = TSpeedButton()
        self.centerDrawing = TSpeedButton()
        self.resetRotations = TSpeedButton()
        self.writeToPOV = TButton()
        self.mirrorHalf = TCheckBox()
        self.ReadFromDXF = TButton()
        self.connectionPointLabel = TLabel()
        self.connectionPoint = TSpinEdit()
        self.clearTdo = TButton()
        self.tdo = KfObject3d()
        self.originalTdo = KfObject3d()
        self.param = PdParameter()
        self.editPaintBox = PdTdoPaintBox()
        self.viewPaintBoxOne = PdTdoPaintBox()
        self.viewPaintBoxTwo = PdTdoPaintBox()
        self.paintBoxClickedIn = PdTdoPaintBox()
        self.commandList = PdCommandList()
        self.internalChange = false
        self.actionInProgress = false
        self.scrolling = false
        self.rotating = false
        self.startDragPoint = TPoint()
        self.scrollStartPosition = TPoint()
        self.draggingPoint = false
        self.pointIndexBeingDragged = 0
        self.cursorMode = 0
        self.rotateDirection = 0
        self.pointRadius = 0
        self.rotateStartAngle = 0.0
        self.lastCommandWasApply = false
        self.lastCommandWasUndoApply = false
        self.editPoints = [0] * (range(0, utdo.kMaximumRecordedPoints + 1) + 1)
        self.numEditPoints = 0
        self.numNewPoints = 0
        self.newPointIndexes = [0] * (range(0, 2 + 1) + 1)
        self.newPoints = [0] * (range(0, 2 + 1) + 1)
        self.horizontalSplitterDragging = false
        self.verticalSplitterDragging = false
        self.horizontalSplitterNeedToRedraw = false
        self.verticalSplitterNeedToRedraw = false
        self.horizontalSplitterStartPos = 0
        self.verticalSplitterStartPos = 0
        self.horizontalSplitterLastDrawPos = 0
        self.verticalSplitterLastDrawPos = 0
        self.lastPicturesPanelWidth = 0
        self.lastPicturesPanelHeight = 0
    
    # resizing and splitting 
    # creation/destruction 
    # -------------------------------------------------------------------------------------------- *creation/destruction 
    def create(self, AOwner):
        PdForm.create(self, AOwner)
        TdoEditorForm = self
        self.tdo = utdo.KfObject3D().create()
        self.commandList = ucommand.PdCommandList().create()
        self.commandList.setNewUndoLimit(udomain.domain.options.undoLimit)
        self.commandList.setNewObjectUndoLimit(udomain.domain.options.undoLimitOfPlants)
        self.editPaintBox = PdTdoPaintBox().create(self)
        self.editPaintBox.Parent = self.picturesPanel
        self.editPaintBox.OnMouseDown = self.editPaintBoxMouseDown
        self.editPaintBox.OnMouseMove = self.imagesMouseMove
        self.editPaintBox.OnMouseUp = self.imagesMouseUp
        self.editPaintBox.OnPaint = self.editPaintBoxPaint
        self.editPaintBox.scale = 1.5
        self.editPaintBox.Cursor = ucursor.crScroll
        self.viewPaintBoxOne = PdTdoPaintBox().create(self)
        self.viewPaintBoxOne.Parent = self.picturesPanel
        self.viewPaintBoxOne.OnMouseDown = self.viewPaintBoxOneMouseDown
        self.viewPaintBoxOne.OnMouseMove = self.imagesMouseMove
        self.viewPaintBoxOne.OnMouseUp = self.imagesMouseUp
        self.viewPaintBoxOne.OnPaint = self.viewPaintBoxOnePaint
        self.viewPaintBoxOne.scale = 0.5
        self.viewPaintBoxOne.Cursor = ucursor.crScroll
        self.viewPaintBoxTwo = PdTdoPaintBox().create(self)
        self.viewPaintBoxTwo.Parent = self.picturesPanel
        self.viewPaintBoxTwo.OnMouseDown = self.viewPaintBoxTwoMouseDown
        self.viewPaintBoxTwo.OnMouseMove = self.imagesMouseMove
        self.viewPaintBoxTwo.OnMouseUp = self.imagesMouseUp
        self.viewPaintBoxTwo.OnPaint = self.viewPaintBoxTwoPaint
        self.viewPaintBoxTwo.scale = 0.5
        self.viewPaintBoxTwo.Cursor = ucursor.crScroll
        self.updateButtonsForUndoRedo()
        return self
    
    def FormCreate(self, Sender):
        tempBoundsRect = TRect()
        
        # keep window on screen - left corner of title bar 
        tempBoundsRect = udomain.domain.tdoEditorWindowRect
        if (tempBoundsRect.Left != 0) or (tempBoundsRect.Right != 0) or (tempBoundsRect.Top != 0) or (tempBoundsRect.Bottom != 0):
            if tempBoundsRect.Left > delphi_compatability.Screen.Width - umain.kMinWidthOnScreen:
                tempBoundsRect.Left = delphi_compatability.Screen.Width - umain.kMinWidthOnScreen
            if tempBoundsRect.Top > delphi_compatability.Screen.Height - umain.kMinHeightOnScreen:
                tempBoundsRect.Top = delphi_compatability.Screen.Height - umain.kMinHeightOnScreen
            self.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom)
        self.scrollCursorMode.Down = true
        self.scrollCursorModeClick(self)
        self.internalChange = true
        self.circlePointSize.Value = udomain.domain.options.circlePointSizeInTdoEditor
        self.plantParts.Value = udomain.domain.options.partsInTdoEditor
        self.fillTriangles.Checked = udomain.domain.options.fillTrianglesInTdoEditor
        self.drawLines.Checked = udomain.domain.options.drawLinesInTdoEditor
        self.internalChange = false
        self.pointRadius = self.circlePointSize.Value / 2
        self.toolbarPanel.BevelOuter = UNRESOLVED.bvNone
        #optionsPanel.bevelOuter := bvNone;
    
    def initializeWithTdoAndParameter(self, aTdo, aParam):
        self.originalTdo = aTdo
        if self.originalTdo == None:
            raise GeneralException.create("Problem: Nil 3D object in method TTdoEditorForm.initializeWithTdoAndParameter.")
        self.param = aParam
        if self.param == None:
            raise GeneralException.create("Problem: Nil parameter in method TTdoEditorForm.initializeWithTdoAndParameter.")
        self.tdo.copyFrom(self.originalTdo)
        self.updateCaptionForNewTdoName()
        self.updateForChangeToNumberOfPoints()
        #v1.6b1
        self.centerDrawingClick(self)
    
    def initializeWithTdo(self, aTdo):
        self.originalTdo = aTdo
        if self.originalTdo == None:
            raise GeneralException.create("Problem: Nil 3D object in method TTdoEditorForm.initializeWithTdo.")
        self.tdo.copyFrom(self.originalTdo)
        self.updateCaptionForNewTdoName()
        self.updateForChangeToNumberOfPoints()
        #v1.6b1
        self.centerDrawingClick(self)
    
    def destroy(self):
        self.tdo.free
        self.tdo = None
        self.commandList.free
        self.commandList = None
        # don't free paint boxes because we are their owner 
        PdForm.destroy(self)
    
    # -------------------------------------------------------------------------------- *command list 
    def undoLastClick(self, Sender):
        if self.lastCommandWasApply:
            umain.MainForm.MenuEditUndoClick(umain.MainForm)
            self.lastCommandWasUndoApply = true
            self.lastCommandWasApply = false
            self.updateButtonsForUndoRedo()
        else:
            self.commandList.undoLast()
            self.updateButtonsForUndoRedo()
            self.updateForChangeToTdo()
    
    def redoLastClick(self, Sender):
        if self.lastCommandWasUndoApply:
            umain.MainForm.MenuEditRedoClick(umain.MainForm)
            self.lastCommandWasUndoApply = false
            self.lastCommandWasApply = true
            self.updateButtonsForUndoRedo()
        else:
            self.commandList.redoLast()
            self.updateButtonsForUndoRedo()
            self.updateForChangeToTdo()
    
    # updating 
    # ------------------------------------------------------------------------------- *updating 
    def updateButtonsForUndoRedo(self):
        if self.lastCommandWasApply:
            self.undoLast.Enabled = true
            self.undoLast.Caption = "&Undo apply"
        elif self.lastCommandWasUndoApply:
            self.redoLast.Enabled = true
            self.redoLast.Caption = "&Redo apply"
        else:
            if self.commandList.isUndoEnabled():
                self.undoLast.Enabled = true
                self.undoLast.Caption = "&Undo " + self.commandList.undoDescription()
            else:
                self.undoLast.Enabled = false
                self.undoLast.Caption = "Can't undo"
            if self.commandList.isRedoEnabled():
                self.redoLast.Enabled = true
                self.redoLast.Caption = "&Redo " + self.commandList.redoDescription()
            else:
                self.redoLast.Enabled = false
                self.redoLast.Caption = "Can't redo"
    
    def updateForChangeToTdo(self):
        self.updateButtonsForUndoRedo()
        self.updateForChangeToNumberOfPoints()
        self.updateForChangeToConnectionPointIndex()
        self.clearTdo.Enabled = (self.tdo != None) and (self.tdo.pointsInUse > 0)
        if (self.editPaintBox != None) and (self.viewPaintBoxOne != None) and (self.viewPaintBoxTwo != None):
            self.editPaintBox.Paint()
            self.viewPaintBoxOne.Paint()
            self.viewPaintBoxTwo.Paint()
    
    def updateForChangeToClickedOnPaintBox(self):
        self.updateButtonsForUndoRedo()
        if self.paintBoxClickedIn != None:
            self.paintBoxClickedIn.Paint()
    
    def updateCaptionForNewTdoName(self):
        self.Caption = "3D object editor - " + self.tdo.getName()
        self.Invalidate()
    
    def updateForChangeToNumberOfPoints(self):
        self.internalChange = true
        self.connectionPoint.Value = self.tdo.originPointIndex + 1
        self.connectionPoint.MaxValue = self.tdo.pointsInUse
        self.connectionPointLabel.Caption = "Connection point (1-" + IntToStr(self.connectionPoint.MaxValue) + ")"
        self.internalChange = false
    
    def updateForChangeToConnectionPointIndex(self):
        oldPoint = TPoint()
        newPoint = TPoint()
        
        self.internalChange = true
        self.connectionPoint.Value = self.tdo.originPointIndex + 1
        self.internalChange = false
        #
        #  // adjust drawing point so 3D object does not move
        #  if connectionPoint.value - 1 <> tdo.originPointIndex then
        #    begin
        #    if (tdo.originPointIndex >= 0) and (tdo.originPointIndex <= numEditPoints - 1) then
        #      oldPoint := editPoints[tdo.originPointIndex]
        #    else
        #      oldPoint := Point(0, 0);
        #    if (connectionPoint.value - 1 >= 0) and (connectionPoint.value - 1 <= numEditPoints - 1) then
        #      newPoint := editPoints[connectionPoint.value - 1]
        #    else
        #      newPoint := Point(0, 0);
        #    editPaintBox.drawPosition.x := editPaintBox.drawPosition.x + (newPoint.x - oldPoint.x);
        #    editPaintBox.drawPosition.y := editPaintBox.drawPosition.y + (newPoint.y - oldPoint.y);
        #    end;
        #  tdo.setOriginPointIndex(connectionPoint.value - 1);
        #  if editPaintBox <> nil then editPaintBox.paint;
        #  
    
    # -------------------------------------------------------------------------------------- *buttons 
    def okClick(self, Sender):
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def FormClose(self, Sender, Action):
        # save settings to domain even if they clicked cancel or clicked the close box
        udomain.domain.tdoEditorWindowRect = Rect(self.Left, self.Top, self.Width, self.Height)
        udomain.domain.options.circlePointSizeInTdoEditor = self.circlePointSize.Value
        udomain.domain.options.partsInTdoEditor = self.plantParts.Value
        udomain.domain.options.fillTrianglesInTdoEditor = self.fillTriangles.Checked
        udomain.domain.options.drawLinesInTdoEditor = self.drawLines.Checked
    
    def applyClick(self, Sender):
        umain.MainForm.doCommand(updcom.PdChangeTdoValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.tdo, self.param.fieldNumber, self.param.regrow))
        self.lastCommandWasApply = true
        self.updateButtonsForUndoRedo()
    
    def renameTdoClick(self, Sender):
        newCommand = PdCommand()
        newName = ansistring()
        
        newName = self.tdo.getName()
        if not InputQuery("Enter new name", "Type a new name for " + newName + ".", newName):
            return
        newCommand = PdRenameTdoCommand().createWithTdoAndNewName(self.tdo, newName)
        self.doCommand(newCommand)
    
    def clearTdoClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = PdClearAllPointsCommand().createWithTdo(self.tdo)
        self.doCommand(newCommand)
    
    def writeToDXFClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        suggestedName = ""
        
        suggestedName = "export.dxf"
        if not usupport.getFileSaveInfo(usupport.kFileTypeDXF, usupport.kAskForFileName, suggestedName, fileInfo):
            return
        try:
            usupport.startFileSave(fileInfo)
            self.tdo.writeToDXFFile(fileInfo.tempFile, utdo.kTdoForeColor, utdo.kTdoBackColor)
            fileInfo.writingWasSuccessful = true
        finally:
            usupport.cleanUpAfterFileSave(fileInfo)
    
    def ReadFromDXFClick(self, Sender):
        fileNameWithPath = ""
        newTdo = KfObject3D()
        inputFile = TextFile()
        newCommand = PdCommand()
        
        newTdo = None
        fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypeDXF, "input.dxf", "Choose a DXF file")
        if fileNameWithPath == "":
            return
        try:
            uwait.startWaitMessage("Reading " + ExtractFileName(fileNameWithPath))
            AssignFile(inputFile, fileNameWithPath)
            try:
                # v1.5
                usupport.setDecimalSeparator()
                Reset(inputFile)
                newTdo = utdo.KfObject3D().create()
                newTdo.readFromDXFFile(inputFile)
                # v1.6b1
                newTdo.setName(usupport.stringUpTo(ExtractFileName(fileNameWithPath), "."))
            finally:
                CloseFile(inputFile)
        except Exception, E:
            uwait.stopWaitMessage()
            ShowMessage(E.message)
            ShowMessage("Could not load file " + fileNameWithPath)
            return
        if newTdo != None:
            newCommand = PdLoadTdoFromDXFCommand().createWithOldAndNewTdo(self.tdo, newTdo)
            self.doCommand(newCommand)
        uwait.stopWaitMessage()
    
    def writeToPOVClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        suggestedName = ""
        
        suggestedName = usupport.replacePunctuationWithUnderscores(self.tdo.getName()) + ".inc"
        if not usupport.getFileSaveInfo(usupport.kFileTypeINC, usupport.kAskForFileName, suggestedName, fileInfo):
            return
        try:
            usupport.startFileSave(fileInfo)
            self.tdo.writeToPOV_INCFile(fileInfo.tempFile, utdo.kTdoForeColor, utdo.kEmbeddedInPlant, self.plantParts.Value)
            fileInfo.writingWasSuccessful = true
        finally:
            usupport.cleanUpAfterFileSave(fileInfo)
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Editing_3D_objects")
    
    # mouse handling 
    # ------------------------------------------------------------------------------------- *mouse handling 
    def imagesMouseDown(self, Sender, Button, Shift, X, Y):
        newCommand = PdCommand()
        anchorPoint = TPoint()
        
        if delphi_compatability.Application.terminated:
            return
        if self.paintBoxClickedIn == None:
            return
        if self.actionInProgress:
            try:
                #error somewhere - user did weird things with mouse buttons - teminate action...
                self.imagesMouseUp(Sender, Button, Shift, X, Y)
            finally:
                self.actionInProgress = false
        # makes shift-click work as right-click
        self.commandList.rightButtonDown = (Button == delphi_compatability.TMouseButton.mbRight) or (delphi_compatability.TShiftStateEnum.ssShift in Shift)
        if self.cursorMode == kCursorModeMagnify:
            if self.commandList.rightButtonDown:
                self.paintBoxClickedIn.Cursor = ucursor.crMagMinus
        elif self.cursorMode == kCursorModeScroll:
            if self.commandList.rightButtonDown:
                return
            self.scrolling = true
            self.startDragPoint = Point(X, Y)
            self.scrollStartPosition = self.paintBoxClickedIn.drawPosition
        elif self.cursorMode == kCursorModeRotate:
            if self.paintBoxClickedIn != self.editPaintBox:
                self.rotating = true
                self.startDragPoint = Point(X, Y)
                self.rotateDirection = updcom.kRotateNotInitialized
                if self.commandList.rightButtonDown:
                    self.paintBoxClickedIn.Cursor = delphi_compatability.crSizeWE
        elif self.cursorMode == kCursorModeAddTriangles:
            if self.numNewPoints >= 3:
                self.numNewPoints = 0
        else :
            if (self.commandList.rightButtonDown) and (self.cursorMode != kCursorModeDragPoints):
                return
            anchorPoint = Point(X, Y)
            self.actionInProgress = true
            newCommand = self.makeMouseCommand(anchorPoint, (delphi_compatability.TShiftStateEnum.ssShift in Shift), (delphi_compatability.TShiftStateEnum.ssCtrl in Shift))
            if newCommand != None:
                self.actionInProgress = self.commandList.mouseDown(newCommand, anchorPoint)
            else:
                self.actionInProgress = false
            if self.actionInProgress:
                self.updateForChangeToTdo()
    
    def imagesMouseMove(self, Sender, Shift, X, Y):
        if delphi_compatability.Application.terminated:
            return
        if (Sender == self.editPaintBox):
            if self.cursorMode == kCursorModeAddTriangles:
                if self.numNewPoints == 0:
                    self.lightUpPointAtMouse(X, Y, umain.kDrawNow)
            elif self.cursorMode == kCursorModeDragPoints:
                if self.numNewPoints == 0:
                    self.lightUpPointAtMouse(X, Y, umain.kDrawNow)
            elif self.cursorMode == kCursorModeDeleteTriangles:
                self.lightUpTriangleAtMouse(X, Y)
            elif self.cursorMode == kCursorModeFlipTriangles:
                self.lightUpTriangleAtMouse(X, Y)
        if self.paintBoxClickedIn == None:
            return
        if Sender != self.paintBoxClickedIn:
            return
        if self.cursorMode == kCursorModeMagnify:
            if self.scrolling:
                self.scrollBy(X, Y)
        elif self.cursorMode == kCursorModeScroll:
            if self.scrolling:
                self.scrollBy(X, Y)
        elif self.cursorMode == kCursorModeRotate:
            if self.rotating:
                self.rotateBy(X, Y)
        elif self.cursorMode == kCursorModeAddTriangles:
            if Sender == self.editPaintBox:
                if (self.numNewPoints == 1) or (self.numNewPoints == 2):
                    self.lightUpAddingLineAtMouse(X, Y)
        else :
            if self.actionInProgress:
                self.commandList.mouseMove(Point(X, Y))
                self.updateForChangeToTdo()
    
    def imagesMouseUp(self, Sender, Button, Shift, X, Y):
        triangle = KfIndexTriangle()
        
        if delphi_compatability.Application.terminated:
            return
        if self.paintBoxClickedIn == None:
            return
        if self.cursorMode != kCursorModeAddTriangles:
            self.numNewPoints = 0
        try:
            if self.cursorMode == kCursorModeMagnify:
                if (self.commandList.rightButtonDown):
                    self.paintBoxClickedIn.magnifyOrReduce(self.paintBoxClickedIn.scale * 0.75, Point(X, Y))
                    if not (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                        self.paintBoxClickedIn.Cursor = ucursor.crMagPlus
                elif (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                    self.paintBoxClickedIn.magnifyOrReduce(self.paintBoxClickedIn.scale * 0.75, Point(X, Y))
                else:
                    self.paintBoxClickedIn.magnifyOrReduce(self.paintBoxClickedIn.scale * 1.5, Point(X, Y))
            elif self.cursorMode == kCursorModeScroll:
                if self.scrolling:
                    self.scrollBy(X, Y)
            elif self.cursorMode == kCursorModeRotate:
                if self.rotating:
                    self.rotateBy(X, Y)
                if self.paintBoxClickedIn != self.editPaintBox:
                    self.paintBoxClickedIn.Cursor = ucursor.crRotate
            elif self.cursorMode == kCursorModeFlipTriangles:
                if self.paintBoxClickedIn == self.editPaintBox:
                    triangle = self.triangleAtMouse(X, Y)
                    if triangle != None:
                        triangle.flip()
                        self.updateForChangeToTdo()
            elif self.cursorMode == kCursorModeAddTriangles:
                if self.paintBoxClickedIn == self.editPaintBox:
                    self.addTrianglePoints(X, Y)
            else :
                if self.actionInProgress:
                    self.commandList.mouseUp(Point(X, Y))
                    self.actionInProgress = false
                    self.updateForChangeToTdo()
        finally:
            self.scrolling = false
            self.rotating = false
            self.commandList.rightButtonDown = false
            self.actionInProgress = false
            self.draggingPoint = false
    
    def editPaintBoxMouseDown(self, Sender, Button, Shift, X, Y):
        self.paintBoxClickedIn = self.editPaintBox
        self.imagesMouseDown(Sender, Button, Shift, X, Y)
    
    def viewPaintBoxOneMouseDown(self, Sender, Button, Shift, X, Y):
        self.paintBoxClickedIn = self.viewPaintBoxOne
        self.imagesMouseDown(Sender, Button, Shift, X, Y)
    
    def viewPaintBoxTwoMouseDown(self, Sender, Button, Shift, X, Y):
        self.paintBoxClickedIn = self.viewPaintBoxTwo
        self.imagesMouseDown(Sender, Button, Shift, X, Y)
    
    # -------------------------------------------------------------------------------- *finding and lighting up 
    def lightUpPointAtMouse(self, x, y, immediate):
        i = 0
        pointFound = 0
        
        pointFound = -1
        if self.draggingPoint:
            if (self.pointIndexBeingDragged >= 0) and (self.pointIndexBeingDragged <= self.numEditPoints - 1):
                pointFound = self.pointIndexBeingDragged
        else:
            pointFound = self.pointIndexAtMouse(x, y)
        if pointFound >= 0:
            self.editPaintBox.bitmap.Canvas.Pen.Color = kLightUpColor
            self.editPaintBox.bitmap.Canvas.Brush.Color = kLightUpColor
            self.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
            self.editPaintBox.bitmap.Canvas.Ellipse(self.editPoints[pointFound].X - self.pointRadius, self.editPoints[pointFound].Y - self.pointRadius, self.editPoints[pointFound].X + self.pointRadius, self.editPoints[pointFound].Y + self.pointRadius)
        else:
            if not self.draggingPoint:
                if self.numEditPoints > 0:
                    for i in range(0, self.numEditPoints):
                        if i == self.tdo.originPointIndex:
                            self.editPaintBox.bitmap.Canvas.Pen.Color = kOriginPointColor
                            self.editPaintBox.bitmap.Canvas.Brush.Color = kOriginPointColor
                        else:
                            self.editPaintBox.bitmap.Canvas.Pen.Color = kConnectedPointColor
                            self.editPaintBox.bitmap.Canvas.Brush.Color = kConnectedPointColor
                        self.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
                        self.editPaintBox.bitmap.Canvas.Ellipse(self.editPoints[i].X - self.pointRadius, self.editPoints[i].Y - self.pointRadius, self.editPoints[i].X + self.pointRadius, self.editPoints[i].Y + self.pointRadius)
        if immediate:
            self.drawPaintBoxBitmapOnCanvas(self.editPaintBox)
    
    def pointIndexAtMouse(self, x, y):
        result = 0
        i = 0
        
        result = -1
        if self.numEditPoints > 0:
            for i in range(0, self.numEditPoints):
                if (abs(x - self.editPoints[i].X) <= self.pointRadius) and (abs(y - self.editPoints[i].Y) <= self.pointRadius):
                    result = i
                    return result
        return result
    
    def lightUpTriangleAtMouse(self, x, y):
        triangle = KfIndexTriangle()
        aPolygon = [0] * (range(0, 2 + 1) + 1)
        
        self.drawTdoOnTdoPaintBox(self.editPaintBox, umain.kDontDrawYet)
        triangle = self.triangleAtMouse(x, y)
        if triangle != None:
            self.editPaintBox.bitmap.Canvas.Pen.Color = kLightUpColor
            self.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
            aPolygon[0] = self.editPoints[triangle.pointIndexes[0] - 1]
            aPolygon[1] = self.editPoints[triangle.pointIndexes[1] - 1]
            aPolygon[2] = self.editPoints[triangle.pointIndexes[2] - 1]
            self.editPaintBox.bitmap.Canvas.Polygon(aPolygon)
        self.drawPaintBoxBitmapOnCanvas(self.editPaintBox)
    
    def triangleAtMouse(self, x, y):
        result = KfIndexTriangle()
        i = 0
        triangle = KfIndexTriangle()
        polygon = [0] * (range(0, 2 + 1) + 1)
        hPolygon = HRgn()
        inTriangle = false
        
        result = None
        if self.tdo.triangles.Count > 0:
            for i in range(0, self.tdo.triangles.Count):
                triangle = utdo.KfIndexTriangle(self.tdo.triangles.Items[i])
                polygon[0] = self.editPoints[triangle.pointIndexes[0] - 1]
                polygon[1] = self.editPoints[triangle.pointIndexes[1] - 1]
                polygon[2] = self.editPoints[triangle.pointIndexes[2] - 1]
                hPolygon = UNRESOLVED.createPolygonRgn(polygon, 3, delphi_compatability.ALTERNATE)
                UNRESOLVED.selectObject(self.Handle, hPolygon)
                try:
                    inTriangle = UNRESOLVED.ptInRegion(hPolygon, x, y)
                finally:
                    UNRESOLVED.deleteObject(hPolygon)
                if inTriangle:
                    result = utdo.KfIndexTriangle(self.tdo.triangles.Items[i])
                    return result
        return result
    
    def scrollBy(self, x, y):
        self.paintBoxClickedIn.drawPosition.X = self.scrollStartPosition.X + x - self.startDragPoint.X
        self.paintBoxClickedIn.drawPosition.Y = self.scrollStartPosition.Y + y - self.startDragPoint.Y
        self.updateForChangeToClickedOnPaintBox()
    
    def rotateBy(self, x, y):
        if (self.rotateDirection == updcom.kRotateNotInitialized) and ((abs(x - self.startDragPoint.X) > 5) or (abs(y - self.startDragPoint.Y) > 5)):
            if self.commandList.rightButtonDown:
                # don't initialize for first few pixels so any wobbling at the start doesn't start you out
                #    in the wrong direction 
                self.rotateDirection = updcom.kRotateZ
            elif abs(x - self.startDragPoint.X) > abs(y - self.startDragPoint.Y):
                self.rotateDirection = updcom.kRotateX
            else:
                self.rotateDirection = updcom.kRotateY
            if self.rotateDirection == updcom.kRotateX:
                self.rotateStartAngle = self.paintBoxClickedIn.xRotation
            elif self.rotateDirection == updcom.kRotateY:
                self.rotateStartAngle = self.paintBoxClickedIn.yRotation
            elif self.rotateDirection == updcom.kRotateZ:
                self.rotateStartAngle = self.paintBoxClickedIn.zRotation
        if self.rotateDirection == updcom.kRotateX:
            self.paintBoxClickedIn.xRotation = umath.min(360, umath.max(-360, self.rotateStartAngle + (x - self.startDragPoint.X) * 0.5))
        elif self.rotateDirection == updcom.kRotateY:
            self.paintBoxClickedIn.yRotation = umath.min(360, umath.max(-360, self.rotateStartAngle + (y - self.startDragPoint.Y) * 0.5))
        elif self.rotateDirection == updcom.kRotateZ:
            self.paintBoxClickedIn.zRotation = umath.min(360, umath.max(-360, self.rotateStartAngle + (self.startDragPoint.X - x) * 0.5))
        self.updateForChangeToClickedOnPaintBox()
    
    def addTrianglePoints(self, x, y):
        pointIndex = 0
        newCommand = PdCommand()
        circleRect = TRect()
        newPoint = TPoint()
        
        self.numNewPoints += 1
        pointIndex = self.pointIndexAtMouse(x, y)
        self.newPointIndexes[self.numNewPoints - 1] = pointIndex
        if pointIndex >= 0:
            self.newPoints[self.numNewPoints - 1] = self.tdo.points[pointIndex]
        else:
            self.newPoints[self.numNewPoints - 1].x = (x - self.editPaintBox.drawPosition.X) / self.editPaintBox.scale
            self.newPoints[self.numNewPoints - 1].y = (y - self.editPaintBox.drawPosition.Y) / self.editPaintBox.scale
            self.newPoints[self.numNewPoints - 1].z = 0
        self.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        self.editPaintBox.bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        self.editPaintBox.bitmap.Canvas.Brush.Color = kUnconnectedPointColor
        self.editPaintBox.bitmap.Canvas.Pen.Color = kUnconnectedPointColor
        newPoint.X = self.editPaintBox.drawPosition.X + intround(self.newPoints[self.numNewPoints - 1].x * self.editPaintBox.scale)
        newPoint.Y = self.editPaintBox.drawPosition.Y + intround(self.newPoints[self.numNewPoints - 1].y * self.editPaintBox.scale)
        circleRect = Rect(newPoint.X - self.pointRadius, newPoint.Y - self.pointRadius, newPoint.X + self.pointRadius, newPoint.Y + self.pointRadius)
        self.editPaintBox.bitmap.Canvas.Ellipse(circleRect.Left, circleRect.Top, circleRect.Right, circleRect.Bottom)
        if self.numNewPoints >= 3:
            newCommand = PdAddTdoTriangleCommand().createWithTdoAndNewPoints(self.tdo, self.newPointIndexes, self.newPoints)
            self.numNewPoints = 0
            self.newPointIndexes[0] = 0
            self.newPointIndexes[1] = 0
            self.newPointIndexes[2] = 0
            self.doCommand(newCommand)
        if self.numNewPoints < 3:
            self.drawPaintBoxBitmapOnCanvas(self.editPaintBox)
    
    def drawPaintBoxBitmapOnCanvas(self, aPaintBox):
        if aPaintBox != None:
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(aPaintBox.bitmap, aPaintBox.Canvas, Rect(0, 0, 0, 0))
    
    def lightUpAddingLineAtMouse(self, x, y):
        firstPoint = TPoint()
        secondPoint = TPoint()
        
        self.editPaintBox.bitmap.Canvas.Brush.Color = delphi_compatability.clWindow
        self.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        self.editPaintBox.bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear
        self.editPaintBox.bitmap.Canvas.FillRect(Rect(0, 0, self.editPaintBox.Width, self.editPaintBox.Height))
        self.drawTdoOnTdoPaintBox(self.editPaintBox, umain.kDontDrawYet)
        self.lightUpPointAtMouse(x, y, umain.kDontDrawYet)
        firstPoint.X = self.editPaintBox.drawPosition.X + intround(self.newPoints[0].x * self.editPaintBox.scale)
        firstPoint.Y = self.editPaintBox.drawPosition.Y + intround(self.newPoints[0].y * self.editPaintBox.scale)
        if self.numNewPoints > 1:
            secondPoint.X = self.editPaintBox.drawPosition.X + intround(self.newPoints[1].x * self.editPaintBox.scale)
            secondPoint.Y = self.editPaintBox.drawPosition.Y + intround(self.newPoints[1].y * self.editPaintBox.scale)
        self.editPaintBox.bitmap.Canvas.Pen.Color = kUnconnectedPointColor
        self.editPaintBox.bitmap.Canvas.MoveTo(firstPoint.X, firstPoint.Y)
        if self.numNewPoints > 1:
            self.editPaintBox.bitmap.Canvas.LineTo(secondPoint.X, secondPoint.Y)
        self.editPaintBox.bitmap.Canvas.LineTo(x, y)
        self.editPaintBox.bitmap.Canvas.Pen.Color = kUnconnectedPointColor
        self.editPaintBox.bitmap.Canvas.Brush.Color = kUnconnectedPointColor
        self.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        self.editPaintBox.bitmap.Canvas.Ellipse(firstPoint.X - self.pointRadius, firstPoint.Y - self.pointRadius, firstPoint.X + self.pointRadius, firstPoint.Y + self.pointRadius)
        if self.numNewPoints > 1:
            self.editPaintBox.bitmap.Canvas.Ellipse(secondPoint.X - self.pointRadius, secondPoint.Y - self.pointRadius, secondPoint.X + self.pointRadius, secondPoint.Y + self.pointRadius)
        self.editPaintBox.bitmap.Canvas.Ellipse(x - self.pointRadius + 1, y - self.pointRadius + 1, x + self.pointRadius - 1, y + self.pointRadius - 1)
        self.drawPaintBoxBitmapOnCanvas(self.editPaintBox)
    
    def makeMouseCommand(self, point, shift, ctrl):
        result = PdCommand()
        result = None
        if self.paintBoxClickedIn != self.editPaintBox:
            return result
        if self.cursorMode == kCursorModeAddTriangles:
            pass
        elif self.cursorMode == kCursorModeDeleteTriangles:
            if self.paintBoxClickedIn == self.editPaintBox:
                #handled in mouse up
                result = PdRemoveTdoTriangleCommand().createWithTdo(self.tdo)
        elif self.cursorMode == kCursorModeDragPoints:
            if self.paintBoxClickedIn == self.editPaintBox:
                result = PdDragTdoPointCommand().createWithTdoAndScale(self.tdo, self.paintBoxClickedIn.scale)
        return result
    
    # drawing 
    # ------------------------------------------------------------------------------------- *drawing 
    def editPaintBoxPaint(self, Sender):
        self.checkImageForBitmapSizeAndFill(self.editPaintBox)
        self.drawTdoOnTdoPaintBox(self.editPaintBox, umain.kDrawNow)
    
    def viewPaintBoxOnePaint(self, Sender):
        self.checkImageForBitmapSizeAndFill(self.viewPaintBoxOne)
        self.drawTdoOnTdoPaintBox(self.viewPaintBoxOne, umain.kDrawNow)
    
    def viewPaintBoxTwoPaint(self, Sender):
        self.checkImageForBitmapSizeAndFill(self.viewPaintBoxTwo)
        self.drawTdoOnTdoPaintBox(self.viewPaintBoxTwo, umain.kDrawNow)
    
    def checkImageForBitmapSizeAndFill(self, aPaintBox):
        if (aPaintBox.bitmap.Width != aPaintBox.Width) or (aPaintBox.bitmap.Height != aPaintBox.Height):
            try:
                aPaintBox.bitmap.Width = aPaintBox.Width
                aPaintBox.bitmap.Height = aPaintBox.Height
            except:
                aPaintBox.bitmap.Width = 1
                aPaintBox.bitmap.Height = 1
        aPaintBox.bitmap.Canvas.Brush.Color = delphi_compatability.clWindow
        aPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        aPaintBox.bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear
        aPaintBox.bitmap.Canvas.FillRect(Rect(0, 0, aPaintBox.Width, aPaintBox.Height))
    
    def drawTdoOnTdoPaintBox(self, aPaintBox, immediate):
        turtle = KfTurtle()
        i = 0
        parts = 0
        wasFillingTriangles = false
        pointOfConnection = TPoint()
        
        if self.tdo == None:
            return
        turtle = uturtle.KfTurtle.defaultStartUsing()
        try:
            # set up turtle
            turtle.drawingSurface.pane = aPaintBox.bitmap.Canvas
            turtle.setDrawOptionsForDrawingTdoOnly()
            turtle.drawOptions.drawLines = self.drawLines.Checked
            turtle.drawOptions.wireFrame = not self.fillTriangles.Checked
            turtle.drawOptions.circlePoints = aPaintBox == self.editPaintBox
            if aPaintBox == self.editPaintBox:
                turtle.drawOptions.circlePointRadius = self.pointRadius
                turtle.drawingSurface.circleColor = kConnectedPointColor
            # must be after pane and draw options set 
            turtle.reset()
            turtle.xyz(aPaintBox.drawPosition.X, aPaintBox.drawPosition.Y, 0)
            turtle.resetBoundsRect(aPaintBox.drawPosition)
            turtle.rotateX(aPaintBox.yRotation * 256 / 360)
            turtle.rotateY(aPaintBox.xRotation * 256 / 360)
            turtle.rotateZ(aPaintBox.zRotation * 256 / 360)
            # draw parts
            parts = self.plantParts.Value
            if aPaintBox == self.editPaintBox:
                parts = 1
            if parts == 0:
                raise GeneralException.create("Zero parts not allowed.")
            turtle.drawingSurface.recordingStart()
            if parts > 1:
                turtle.rotateZ(-64)
            for i in range(0, parts):
                if parts > 1:
                    turtle.rotateX(256 / parts)
                    turtle.push()
                    turtle.rotateY(64)
                    turtle.rotateX(64)
                self.tdo.draw(turtle, aPaintBox.scale, "", "", 0, 0)
                if (self.mirrorHalf.Checked) and (not (aPaintBox == self.editPaintBox)):
                    turtle.push()
                    turtle.rotateY(256 / 2)
                    self.tdo.reverseZValues()
                    turtle.drawingSurface.foreColor = UNRESOLVED.rgb(255, 255, 200)
                    turtle.drawingSurface.backColor = UNRESOLVED.rgb(255, 255, 200)
                    turtle.drawingSurface.lineColor = delphi_compatability.clBlack
                    self.tdo.draw(turtle, aPaintBox.scale, "", "", 0, 0)
                    turtle.drawingSurface.foreColor = utdo.kTdoForeColor
                    turtle.drawingSurface.backColor = utdo.kTdoBackColor
                    self.tdo.reverseZValues()
                    turtle.pop()
                if parts > 1:
                    turtle.pop()
            turtle.drawingSurface.recordingStop()
            turtle.drawingSurface.recordingDraw()
            turtle.drawingSurface.clearTriangles()
            if aPaintBox == self.editPaintBox:
                # if edit panel, get new locations of edit points
                self.numEditPoints = turtle.recordedPointsInUse
                if self.numEditPoints > 0:
                    for i in range(0, self.numEditPoints):
                        self.editPoints[i] = Point(intround(turtle.recordedPoints[i].x), intround(turtle.recordedPoints[i].y))
                if self.numEditPoints > 0:
                    # draw connection point circle in black over rest
                    aPaintBox.bitmap.Canvas.Brush.Color = kOriginPointColor
                    aPaintBox.bitmap.Canvas.Pen.Color = kOriginPointColor
                    pointOfConnection = self.editPoints[self.tdo.originPointIndex]
                    aPaintBox.bitmap.Canvas.Ellipse(pointOfConnection.X - self.pointRadius, pointOfConnection.Y - self.pointRadius, pointOfConnection.X + self.pointRadius, pointOfConnection.Y + self.pointRadius)
                if self.draggingPoint:
                    self.lightUpPointAtMouse(self.commandList.previousPoint.X, self.commandList.previousPoint.Y, umain.kDontDrawYet)
            # get bounds rect from turtle
            aPaintBox.tdoBoundsRect = turtle.boundsRect()
            # draw border
            aPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
            aPaintBox.bitmap.Canvas.Pen.Color = UNRESOLVED.clBtnText
            aPaintBox.bitmap.Canvas.Rectangle(0, 0, aPaintBox.Width, aPaintBox.Height)
            if immediate:
                # draw
                self.drawPaintBoxBitmapOnCanvas(aPaintBox)
        finally:
            uturtle.KfTurtle.defaultStopUsing()
    
    def centerDrawingInPaintBox(self, aPaintBox):
        newScaleX = 0.0
        newScaleY = 0.0
        centerPointOfTdoBoundsRect = TPoint()
        centerOfPaintBox = TPoint()
        offset = TPoint()
        
        if aPaintBox == None:
            return
        # set high so it will never be too small
        aPaintBox.scale = 100.0
        # 1. draw to determine new scale 
        self.drawTdoOnTdoPaintBox(aPaintBox, umain.kDontDrawYet)
        newScaleX = umath.safedivExcept(0.95 * aPaintBox.scale * aPaintBox.Width, usupport.rWidth(aPaintBox.tdoBoundsRect), 0.1)
        newScaleY = umath.safedivExcept(0.95 * aPaintBox.scale * aPaintBox.Height, usupport.rHeight(aPaintBox.tdoBoundsRect), 0.1)
        aPaintBox.scale = umath.min(newScaleX, newScaleY)
        # 2. draw to determine shift of drawPosition if any - fill in case this is last draw 
        aPaintBox.bitmap.Canvas.Brush.Color = delphi_compatability.clWhite
        aPaintBox.bitmap.Canvas.FillRect(Rect(0, 0, aPaintBox.Width, aPaintBox.Height))
        self.drawTdoOnTdoPaintBox(aPaintBox, umain.kDontDrawYet)
        # v2 improved how this is done
        centerPointOfTdoBoundsRect = Point(aPaintBox.tdoBoundsRect.Left + (aPaintBox.tdoBoundsRect.Right - aPaintBox.tdoBoundsRect.Left) / 2, aPaintBox.tdoBoundsRect.Top + (aPaintBox.tdoBoundsRect.Bottom - aPaintBox.tdoBoundsRect.Top) / 2)
        centerOfPaintBox = Point(aPaintBox.Width / 2, aPaintBox.Height / 2)
        offset = Point(centerOfPaintBox.X - centerPointOfTdoBoundsRect.X, centerOfPaintBox.Y - centerPointOfTdoBoundsRect.Y)
        aPaintBox.drawPosition.X = aPaintBox.drawPosition.X + offset.X
        aPaintBox.drawPosition.Y = aPaintBox.drawPosition.Y + offset.Y
        # 3. draw with new scale and position if position changed 
        aPaintBox.bitmap.Canvas.Brush.Color = delphi_compatability.clWhite
        aPaintBox.bitmap.Canvas.FillRect(Rect(0, 0, aPaintBox.Width, aPaintBox.Height))
        self.drawTdoOnTdoPaintBox(aPaintBox, umain.kDontDrawYet)
        self.drawPaintBoxBitmapOnCanvas(aPaintBox)
    
    # ------------------------------------------------------------------------ *toolbar 
    def scrollCursorModeClick(self, Sender):
        self.cursorMode = kCursorModeScroll
        if (self.editPaintBox != None) and (self.viewPaintBoxOne != None) and (self.viewPaintBoxTwo != None):
            self.editPaintBox.Cursor = ucursor.crScroll
            self.viewPaintBoxOne.Cursor = ucursor.crScroll
            self.viewPaintBoxTwo.Cursor = ucursor.crScroll
    
    def magnifyCursorModeClick(self, Sender):
        self.cursorMode = kCursorModeMagnify
        self.editPaintBox.Cursor = ucursor.crMagPlus
        self.viewPaintBoxOne.Cursor = ucursor.crMagPlus
        self.viewPaintBoxTwo.Cursor = ucursor.crMagPlus
    
    def rotateCursorModeClick(self, Sender):
        self.cursorMode = kCursorModeRotate
        #can't rotate edit picture
        self.editPaintBox.Cursor = delphi_compatability.crDefault
        self.viewPaintBoxOne.Cursor = ucursor.crRotate
        self.viewPaintBoxTwo.Cursor = ucursor.crRotate
    
    def addTrianglePointsCursorModeClick(self, Sender):
        self.cursorMode = kCursorModeAddTriangles
        self.editPaintBox.Cursor = ucursor.crAddTriangle
        self.viewPaintBoxOne.Cursor = delphi_compatability.crDefault
        self.viewPaintBoxTwo.Cursor = delphi_compatability.crDefault
    
    def removeTriangleCursorModeClick(self, Sender):
        self.cursorMode = kCursorModeDeleteTriangles
        self.editPaintBox.Cursor = ucursor.crDeleteTriangle
        self.viewPaintBoxOne.Cursor = delphi_compatability.crDefault
        self.viewPaintBoxTwo.Cursor = delphi_compatability.crDefault
    
    def dragCursorModeClick(self, Sender):
        self.cursorMode = kCursorModeDragPoints
        self.editPaintBox.Cursor = ucursor.crDragPoint
        self.viewPaintBoxOne.Cursor = delphi_compatability.crDefault
        self.viewPaintBoxTwo.Cursor = delphi_compatability.crDefault
    
    def flipTriangleCursorModeClick(self, Sender):
        self.cursorMode = kCursorModeFlipTriangles
        self.editPaintBox.Cursor = ucursor.crFlipTriangle
        self.viewPaintBoxOne.Cursor = delphi_compatability.crDefault
        self.viewPaintBoxTwo.Cursor = delphi_compatability.crDefault
    
    def FormKeyDown(self, Sender, Key, Shift):
        if Key == delphi_compatability.VK_SHIFT:
            if self.cursorMode == kCursorModeMagnify:
                self.editPaintBox.Cursor = ucursor.crMagMinus
                self.viewPaintBoxOne.Cursor = ucursor.crMagMinus
                self.viewPaintBoxTwo.Cursor = ucursor.crMagMinus
        return Key
    
    def FormKeyUp(self, Sender, Key, Shift):
        if Key == delphi_compatability.VK_SHIFT:
            if self.cursorMode == kCursorModeMagnify:
                self.editPaintBox.Cursor = ucursor.crMagPlus
                self.viewPaintBoxOne.Cursor = ucursor.crMagPlus
                self.viewPaintBoxTwo.Cursor = ucursor.crMagPlus
        return Key
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
    def magnifyPlusClick(self, Sender):
        if self.editPaintBox != None:
            self.editPaintBox.magnifyOrReduce(self.editPaintBox.scale * 1.5, self.editPaintBox.drawPosition)
        if self.viewPaintBoxOne != None:
            self.viewPaintBoxOne.magnifyOrReduce(self.viewPaintBoxOne.scale * 1.5, self.viewPaintBoxOne.drawPosition)
        if self.viewPaintBoxTwo != None:
            self.viewPaintBoxTwo.magnifyOrReduce(self.viewPaintBoxTwo.scale * 1.5, self.viewPaintBoxTwo.drawPosition)
    
    def magnifyMinusClick(self, Sender):
        if self.editPaintBox != None:
            self.editPaintBox.magnifyOrReduce(self.editPaintBox.scale * 0.75, self.editPaintBox.drawPosition)
        if self.viewPaintBoxOne != None:
            self.viewPaintBoxOne.magnifyOrReduce(self.viewPaintBoxOne.scale * 0.75, self.viewPaintBoxOne.drawPosition)
        if self.viewPaintBoxTwo != None:
            self.viewPaintBoxTwo.magnifyOrReduce(self.viewPaintBoxTwo.scale * 0.75, self.viewPaintBoxTwo.drawPosition)
    
    def centerDrawingClick(self, Sender):
        if self.editPaintBox != None:
            self.centerDrawingInPaintBox(self.editPaintBox)
        if self.viewPaintBoxOne != None:
            self.centerDrawingInPaintBox(self.viewPaintBoxOne)
        if self.viewPaintBoxTwo != None:
            self.centerDrawingInPaintBox(self.viewPaintBoxTwo)
    
    def resetRotationsClick(self, Sender):
        if self.editPaintBox != None:
            self.editPaintBox.resetRotations()
        if self.viewPaintBoxOne != None:
            self.viewPaintBoxOne.resetRotations()
        if self.viewPaintBoxTwo != None:
            self.viewPaintBoxTwo.resetRotations()
    
    def mirrorTdoClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = PdMirrorTdoCommand().createWithTdo(self.tdo)
        self.doCommand(newCommand)
    
    def reverseZValuesClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = PdReverseZValuesTdoCommand().createWithTdo(self.tdo)
        self.doCommand(newCommand)
    
    # --------------------------------------------------------------------------------------- *resizing and splitting 
    def FormResize(self, Sender):
        newTop = 0
        newLeft = 0
        widthBeforeButtons = 0
        
        if delphi_compatability.Application.terminated:
            return
        if self.tdo == None:
            return
        if self.WindowState == delphi_compatability.TWindowState.wsMinimized:
            return
        self.verticalSplitter.Visible = false
        self.horizontalSplitter.Visible = false
        widthBeforeButtons = umath.intMax(0, self.ClientWidth - self.ok.Width - kBetweenGap * 2)
        # pictures panel 
        self.picturesPanel.SetBounds(0, self.toolbarPanel.Height, widthBeforeButtons, umath.intMax(0, self.ClientHeight - self.optionsPanel.Height - self.toolbarPanel.Height - 4))
        if self.lastPicturesPanelWidth != 0:
            # vertical splitter 
            newLeft = intround(1.0 * self.verticalSplitter.Left * self.picturesPanel.Width / self.lastPicturesPanelWidth)
        else:
            newLeft = self.picturesPanel.Width / 2
        if newLeft >= self.picturesPanel.Width:
            newLeft = self.picturesPanel.Width - 1
        if newLeft < 0:
            newLeft = 0
        self.verticalSplitter.SetBounds(newLeft, 0, self.verticalSplitter.Width, self.picturesPanel.Height)
        if self.lastPicturesPanelHeight != 0:
            # horizontal splitter 
            newTop = intround(1.0 * self.horizontalSplitter.Top * self.picturesPanel.Height / self.lastPicturesPanelHeight)
        else:
            newTop = self.picturesPanel.Height / 2
        if newTop >= self.picturesPanel.Height:
            newTop = self.picturesPanel.Height - 1
        if newTop < 0:
            newTop = 0
        self.horizontalSplitter.SetBounds(self.verticalSplitter.Left + self.verticalSplitter.Width, newTop, umath.intMax(0, self.picturesPanel.Width - self.verticalSplitter.Left - self.verticalSplitter.Width), self.horizontalSplitter.Height)
        self.internalChange = true
        self.resizeImagesToVerticalSplitter()
        self.resizeImagesToHorizontalSplitter()
        self.internalChange = false
        self.setInitialDrawPositionsIfNotSet()
        # rest of window 
        self.toolbarPanel.SetBounds(0, 0, self.picturesPanel.Width, self.toolbarPanel.Height)
        self.optionsPanel.SetBounds(0, self.picturesPanel.Top + self.picturesPanel.Height + 4, self.picturesPanel.Width, self.optionsPanel.Height)
        self.ok.Left = self.ClientWidth - self.ok.Width - kBetweenGap
        self.cancel.Left = self.ok.Left
        self.undoLast.Left = self.ok.Left
        self.redoLast.Left = self.ok.Left
        self.renameTdo.Left = self.ok.Left
        self.clearTdo.Left = self.ok.Left
        self.writeToDXF.Left = self.ok.Left
        self.ReadFromDXF.Left = self.ok.Left
        self.writeToPOV.Left = self.ok.Left
        self.helpButton.Left = self.ok.Left
        self.lastPicturesPanelWidth = self.picturesPanel.Width
        self.lastPicturesPanelHeight = self.picturesPanel.Height
        self.verticalSplitter.Visible = true
        self.horizontalSplitter.Visible = true
    
    def resizeImagesToVerticalSplitter(self):
        newLeft = 0
        
        if self.editPaintBox != None:
            self.editPaintBox.SetBounds(0, 0, self.verticalSplitter.Left, self.picturesPanel.Height)
        newLeft = self.verticalSplitter.Left + self.verticalSplitter.Width
        self.horizontalSplitter.SetBounds(newLeft, self.horizontalSplitter.Top, umath.intMax(0, self.picturesPanel.Width - newLeft), self.horizontalSplitter.Height)
        if self.viewPaintBoxOne != None:
            self.viewPaintBoxOne.SetBounds(newLeft, self.viewPaintBoxOne.Top, umath.intMax(0, self.picturesPanel.Width - newLeft), self.viewPaintBoxOne.Height)
        if self.viewPaintBoxTwo != None:
            self.viewPaintBoxTwo.SetBounds(newLeft, self.viewPaintBoxTwo.Top, umath.intMax(0, self.picturesPanel.Width - newLeft), self.viewPaintBoxTwo.Height)
        if not self.internalChange:
            self.updateForChangeToTdo()
    
    def resizeImagesToHorizontalSplitter(self):
        newTop = 0
        
        if self.viewPaintBoxOne != None:
            self.viewPaintBoxOne.SetBounds(self.viewPaintBoxOne.Left, 0, self.viewPaintBoxOne.Width, self.horizontalSplitter.Top)
        newTop = self.horizontalSplitter.Top + self.horizontalSplitter.Height
        if self.viewPaintBoxTwo != None:
            self.viewPaintBoxTwo.SetBounds(self.viewPaintBoxTwo.Left, newTop, self.viewPaintBoxTwo.Width, umath.intMax(0, self.picturesPanel.Height - newTop))
        if not self.internalChange:
            self.updateForChangeToTdo()
    
    def setInitialDrawPositionsIfNotSet(self):
        if self.editPaintBox != None:
            if (self.editPaintBox.drawPosition.X == 0) and (self.editPaintBox.drawPosition.Y == 0):
                self.editPaintBox.drawPosition = Point(self.editPaintBox.Width / 2, self.editPaintBox.Height - 10)
                self.editPaintBox.Paint()
        if self.viewPaintBoxOne != None:
            if (self.viewPaintBoxOne.drawPosition.X == 0) and (self.viewPaintBoxOne.drawPosition.Y == 0):
                self.viewPaintBoxOne.drawPosition = Point(self.viewPaintBoxOne.Width / 2, self.viewPaintBoxOne.Height - 10)
                self.viewPaintBoxOne.Paint()
        if self.viewPaintBoxTwo != None:
            if (self.viewPaintBoxTwo.drawPosition.X == 0) and (self.viewPaintBoxTwo.drawPosition.Y == 0):
                self.viewPaintBoxTwo.drawPosition = Point(self.viewPaintBoxTwo.Width / 2, self.viewPaintBoxTwo.Height - 10)
                self.viewPaintBoxTwo.Paint()
    
    def verticalSplitterMouseDown(self, Sender, Button, Shift, X, Y):
        self.verticalSplitterDragging = true
        self.verticalSplitterStartPos = X
        self.verticalSplitterLastDrawPos = -1
        self.verticalSplitterNeedToRedraw = true
    
    def verticalSplitterMouseMove(self, Sender, Shift, X, Y):
        if self.verticalSplitterDragging and (self.verticalSplitter.Left + X >= kSplitterDragToLeftMinPixels) and (self.verticalSplitter.Left + X < self.picturesPanel.Width - kSplitterDragToRightMinPixels):
            self.undrawVerticalSplitterLine()
            self.verticalSplitterLastDrawPos = self.drawVerticalSplitterLine(X)
    
    def verticalSplitterMouseUp(self, Sender, Button, Shift, X, Y):
        if self.verticalSplitterDragging:
            self.undrawVerticalSplitterLine()
            self.verticalSplitter.Left = self.verticalSplitter.Left - (self.verticalSplitterStartPos - X)
            if self.verticalSplitter.Left < kSplitterDragToLeftMinPixels:
                self.verticalSplitter.Left = kSplitterDragToLeftMinPixels
            if self.verticalSplitter.Left > self.picturesPanel.Width - kSplitterDragToRightMinPixels:
                self.verticalSplitter.Left = self.picturesPanel.Width - kSplitterDragToRightMinPixels
            self.resizeImagesToVerticalSplitter()
            self.verticalSplitterDragging = false
    
    def drawVerticalSplitterLine(self, pos):
        result = 0
        theDC = HDC()
        
        theDC = UNRESOLVED.getDC(0)
        result = self.ClientOrigin.X + self.verticalSplitter.Left + pos + 2
        UNRESOLVED.patBlt(theDC, result, self.ClientOrigin.Y + self.picturesPanel.Top + self.verticalSplitter.Top, 1, self.verticalSplitter.Height, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
        self.verticalSplitterNeedToRedraw = true
        return result
    
    def undrawVerticalSplitterLine(self):
        theDC = HDC()
        
        if not self.verticalSplitterNeedToRedraw:
            return
        theDC = UNRESOLVED.getDC(0)
        UNRESOLVED.patBlt(theDC, self.verticalSplitterLastDrawPos, self.ClientOrigin.Y + self.picturesPanel.Top + self.verticalSplitter.Top, 1, self.verticalSplitter.Height, delphi_compatability.DSTINVERT)
        UNRESOLVED.releaseDC(0, theDC)
        self.verticalSplitterNeedToRedraw = false
    
    def horizontalSplitterMouseDown(self, Sender, Button, Shift, X, Y):
        self.horizontalSplitterDragging = true
        self.horizontalSplitterStartPos = Y
        self.horizontalSplitterLastDrawPos = -1
        self.horizontalSplitterNeedToRedraw = true
    
    def horizontalSplitterMouseMove(self, Sender, Shift, X, Y):
        if self.horizontalSplitterDragging and (self.horizontalSplitter.Top + Y >= kSplitterDragToTopMinPixels) and (self.horizontalSplitter.Top + Y < self.picturesPanel.Height - kSplitterDragToBottomMinPixels):
            self.undrawHorizontalSplitterLine()
            self.horizontalSplitterLastDrawPos = self.drawHorizontalSplitterLine(Y)
    
    def horizontalSplitterMouseUp(self, Sender, Button, Shift, X, Y):
        if self.horizontalSplitterDragging:
            self.undrawHorizontalSplitterLine()
            self.horizontalSplitter.Top = self.horizontalSplitter.Top - (self.horizontalSplitterStartPos - Y)
            if self.horizontalSplitter.Top < kSplitterDragToTopMinPixels:
                self.horizontalSplitter.Top = kSplitterDragToTopMinPixels
            if self.horizontalSplitter.Top > self.picturesPanel.Height - kSplitterDragToBottomMinPixels:
                self.horizontalSplitter.Top = self.picturesPanel.Height - kSplitterDragToBottomMinPixels
            self.resizeImagesToHorizontalSplitter()
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
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 456
        UNRESOLVED.ptMinTrackSize.y = 260
    
    def fillTrianglesClick(self, Sender):
        if not self.fillTriangles.Checked:
            self.drawLines.Checked = true
            self.drawLines.Enabled = false
        else:
            self.drawLines.Enabled = true
        if self.internalChange:
            return
        self.updateForChangeToTdo()
    
    def mirrorHalfClick(self, Sender):
        self.updateForChangeToTdo()
    
    def drawLinesClick(self, Sender):
        if self.internalChange:
            return
        self.updateForChangeToTdo()
    
    def plantPartsChange(self, Sender):
        if self.internalChange:
            return
        self.updateForChangeToTdo()
    
    def circlePointSizeChange(self, Sender):
        if self.internalChange:
            return
        self.pointRadius = self.circlePointSize.Value / 2
        self.updateForChangeToTdo()
    
    def connectionPointChange(self, Sender):
        oldPoint = TPoint()
        newPoint = TPoint()
        
        if self.internalChange:
            return
        if self.connectionPoint.Value - 1 != self.tdo.originPointIndex:
            if (self.tdo.originPointIndex >= 0) and (self.tdo.originPointIndex <= self.numEditPoints - 1):
                # adjust drawing point so 3D object does not move
                oldPoint = self.editPoints[self.tdo.originPointIndex]
            else:
                oldPoint = Point(0, 0)
            if (self.connectionPoint.Value - 1 >= 0) and (self.connectionPoint.Value - 1 <= self.numEditPoints - 1):
                newPoint = self.editPoints[self.connectionPoint.Value - 1]
            else:
                newPoint = Point(0, 0)
            self.editPaintBox.drawPosition.X = self.editPaintBox.drawPosition.X + (newPoint.X - oldPoint.X)
            self.editPaintBox.drawPosition.Y = self.editPaintBox.drawPosition.Y + (newPoint.Y - oldPoint.Y)
        self.tdo.setOriginPointIndex(self.connectionPoint.Value - 1)
        if self.editPaintBox != None:
            self.editPaintBox.Paint()
        self.updateForChangeToConnectionPointIndex()
    
    # commands 
    # ------------------------------------------------------------------------ *commands 
    def doCommand(self, command):
        self.commandList.doCommand(command)
        self.updateButtonsForUndoRedo()
        self.updateForChangeToTdo()
    
class PdTdoCommand(PdCommand):
    def __init__(self):
        self.tdo = KfObject3D()
        self.lastCommandWasApply = false
        self.lastCommandWasUndoApply = false
    
    # ------------------------------------------------------------------------ PdTdoCommand 
    def createWithTdo(self, aTdo):
        PdCommand.create(self)
        self.commandChangesPlantFile = false
        self.tdo = aTdo
        self.lastCommandWasApply = TdoEditorForm.lastCommandWasApply
        self.lastCommandWasUndoApply = TdoEditorForm.lastCommandWasUndoApply
        return self
    
    def doCommand(self):
        PdCommand.doCommand(self)
        TdoEditorForm.lastCommandWasApply = false
        TdoEditorForm.lastCommandWasUndoApply = false
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        TdoEditorForm.lastCommandWasApply = self.lastCommandWasApply
        TdoEditorForm.lastCommandWasUndoApply = self.lastCommandWasUndoApply
    
class PdDragTdoPointCommand(PdTdoCommand):
    def __init__(self):
        self.scale = 0.0
        self.movingPointIndex = 0
        self.dragStartPoint = TPoint()
        self.oldPoint3D = KfPoint3D()
        self.newPoint3D = KfPoint3D()
    
    # -------------------------------------------------------------------- PdDragTdoPointCommand 
    def createWithTdoAndScale(self, aTdo, aScale):
        PdTdoCommand.createWithTdo(self, aTdo)
        self.scale = aScale
        return self
    
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        result = self
        if aTrackPhase == ucommand.TrackPhase.trackPress:
            self.movingPointIndex = TdoEditorForm.pointIndexAtMouse(nextPoint.X, nextPoint.Y)
            TdoEditorForm.draggingPoint = true
            TdoEditorForm.pointIndexBeingDragged = self.movingPointIndex
            if self.movingPointIndex < 0:
                result = None
                self.free
            else:
                self.dragStartPoint = nextPoint
                self.oldPoint3D = self.tdo.points[self.movingPointIndex]
                self.newPoint3D = self.oldPoint3D
        elif aTrackPhase == ucommand.TrackPhase.trackMove:
            if rightButtonDown:
                self.newPoint3D.z = self.oldPoint3D.z - (nextPoint.Y - self.dragStartPoint.Y) / self.scale
            else:
                self.newPoint3D.x = self.oldPoint3D.x + (nextPoint.X - self.dragStartPoint.X) / self.scale
                self.newPoint3D.y = self.oldPoint3D.y + (nextPoint.Y - self.dragStartPoint.Y) / self.scale
            self.tdo.points[self.movingPointIndex] = self.newPoint3D
        elif aTrackPhase == ucommand.TrackPhase.trackRelease:
            if not mouseDidMove:
                result = None
                self.free
        return result
    
    def undoCommand(self):
        PdTdoCommand.undoCommand(self)
        self.tdo.points[self.movingPointIndex] = self.oldPoint3D
    
    def redoCommand(self):
        PdTdoCommand.doCommand(self)
        self.tdo.points[self.movingPointIndex] = self.newPoint3D
    
    def description(self):
        result = ""
        result = "drag"
        return result
    
class PdRenameTdoCommand(PdTdoCommand):
    def __init__(self):
        self.oldName = ""
        self.newName = ""
    
    # --------------------------------------------------------------------------- PdRenameTdoCommand 
    def createWithTdoAndNewName(self, aTdo, aName):
        PdTdoCommand.createWithTdo(self, aTdo)
        self.oldName = self.tdo.getName()
        self.newName = aName
        return self
    
    def doCommand(self):
        self.tdo.setName(self.newName)
        TdoEditorForm.updateCaptionForNewTdoName()
        PdTdoCommand.doCommand(self)
    
    def undoCommand(self):
        self.tdo.setName(self.oldName)
        TdoEditorForm.updateCaptionForNewTdoName()
        PdTdoCommand.undoCommand(self)
    
    def description(self):
        result = ""
        result = "rename"
        return result
    
class PdReplaceTdoCommand(PdTdoCommand):
    def __init__(self):
        self.oldTdo = KfObject3D()
        self.newTdo = KfObject3D()
    
    # ------------------------------------------------------------------------ PdReplaceTdoCommand 
    def createWithTdo(self, aTdo):
        PdTdoCommand.createWithTdo(self, aTdo)
        self.oldTdo = utdo.KfObject3D().create()
        self.newTdo = utdo.KfObject3D().create()
        self.oldTdo.copyFrom(self.tdo)
        self.newTdo.copyFrom(self.tdo)
        return self
    
    def destroy(self):
        self.oldTdo.free
        self.oldTdo = None
        self.newTdo.free
        self.newTdo = None
        PdTdoCommand.destroy(self)
    
    def undoCommand(self):
        PdTdoCommand.undoCommand(self)
        self.tdo.copyFrom(self.oldTdo)
        # v1.6
        TdoEditorForm.updateForChangeToTdo()
    
    def redoCommand(self):
        PdTdoCommand.doCommand(self)
        self.tdo.copyFrom(self.newTdo)
        # v1.6
        TdoEditorForm.updateForChangeToTdo()
    
class PdAddTdoTriangleCommand(PdReplaceTdoCommand):
    def __init__(self):
        self.newPoints = [0] * (range(0, 2 + 1) + 1)
        self.newPointIndexes = [0] * (range(0, 2 + 1) + 1)
        self.newTriangle = KfIndexTriangle()
    
    # -------------------------------------------------------------------- PdAddTdoTriangleCommand 
    def createWithTdoAndNewPoints(self, aTdo, aNewPointIndexes, aNewPoints):
        i = 0
        
        PdReplaceTdoCommand.createWithTdo(self, aTdo)
        for i in range(0, 2 + 1):
            self.newPointIndexes[i] = aNewPointIndexes[i]
            self.newPoints[i] = aNewPoints[i]
        return self
    
    def doCommand(self):
        i = 0
        
        PdReplaceTdoCommand.doCommand(self)
        for i in range(0, 2 + 1):
            if self.newPointIndexes[i] < 0:
                self.newPointIndexes[i] = self.newTdo.addPoint(self.newPoints[i]) - 1
        self.newTriangle = utdo.KfIndexTriangle().createABC(self.newPointIndexes[0] + 1, self.newPointIndexes[1] + 1, self.newPointIndexes[2] + 1)
        #newTdo will free newTriangle
        self.newTdo.triangles.Add(self.newTriangle)
        self.tdo.copyFrom(self.newTdo)
        TdoEditorForm.updateForChangeToNumberOfPoints()
    
    def undoCommand(self):
        PdReplaceTdoCommand.undoCommand(self)
        TdoEditorForm.updateForChangeToNumberOfPoints()
    
    def redoCommand(self):
        PdReplaceTdoCommand.redoCommand(self)
        TdoEditorForm.updateForChangeToNumberOfPoints()
    
    def description(self):
        result = ""
        result = "add"
        return result
    
class PdRemoveTdoTriangleCommand(PdReplaceTdoCommand):
    def __init__(self):
        self.triangle = KfIndexTriangle()
    
    # ----------------------------------------------------------------------- PdRemoveTdoTriangleCommand 
    def doCommand(self):
        PdReplaceTdoCommand.doCommand(self)
        TdoEditorForm.updateForChangeToNumberOfPoints()
    
    def undoCommand(self):
        PdReplaceTdoCommand.undoCommand(self)
        TdoEditorForm.updateForChangeToNumberOfPoints()
    
    def redoCommand(self):
        PdReplaceTdoCommand.redoCommand(self)
        TdoEditorForm.updateForChangeToNumberOfPoints()
    
    def destroy(self):
        if self.done:
            # since triangle was removed from, not added to, newTdo, we must free it ourselves 
            self.triangle.free
        self.triangle = None
        PdReplaceTdoCommand.destroy(self)
    
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        triangleInTdo = KfIndexTriangle()
        index = 0
        
        result = self
        if aTrackPhase == ucommand.TrackPhase.trackPress:
            pass
        elif aTrackPhase == ucommand.TrackPhase.trackMove:
            pass
        elif aTrackPhase == ucommand.TrackPhase.trackRelease:
            triangleInTdo = TdoEditorForm.triangleAtMouse(nextPoint.X, nextPoint.Y)
            index = self.tdo.triangles.IndexOf(triangleInTdo)
            if (index >= 0) and (index <= self.newTdo.triangles.Count - 1):
                self.triangle = utdo.KfIndexTriangle(self.newTdo.triangles.Items[index])
                #we will free triangle
                self.newTdo.removeTriangle(self.triangle)
                self.tdo.copyFrom(self.newTdo)
            else:
                result = None
                self.free
        return result
    
    def description(self):
        result = ""
        result = "delete"
        return result
    
class PdMirrorTdoCommand(PdReplaceTdoCommand):
    def __init__(self):
        pass
    
    # -------------------------------------------------------------------- PdMirrorTdoCommand 
    def doCommand(self):
        self.newTdo.makeMirrorTriangles()
        self.tdo.copyFrom(self.newTdo)
        PdReplaceTdoCommand.doCommand(self)
    
    def description(self):
        result = ""
        result = "mirror"
        return result
    
class PdReverseZValuesTdoCommand(PdReplaceTdoCommand):
    def __init__(self):
        pass
    
    # -------------------------------------------------------------------- PdReverseZValuesTdoCommand 
    def doCommand(self):
        self.newTdo.reverseZValues()
        self.tdo.copyFrom(self.newTdo)
        PdReplaceTdoCommand.doCommand(self)
    
    def description(self):
        result = ""
        result = "reverse"
        return result
    
class PdClearAllPointsCommand(PdReplaceTdoCommand):
    def __init__(self):
        pass
    
    # -------------------------------------------------------------------- PdClearAllPointsCommand 
    def doCommand(self):
        self.newTdo.clearPoints()
        self.tdo.copyFrom(self.newTdo)
        PdReplaceTdoCommand.doCommand(self)
    
    def description(self):
        result = ""
        result = "clear"
        return result
    
class PdLoadTdoFromDXFCommand(PdReplaceTdoCommand):
    def __init__(self):
        pass
    
    # -------------------------------------------------------------------- PdLoadTdoFromDXFCommand 
    def createWithOldAndNewTdo(self, anOldTdo, aNewTdo):
        PdReplaceTdoCommand.createWithTdo(self, anOldTdo)
        self.oldTdo = utdo.KfObject3D().create()
        self.newTdo = utdo.KfObject3D().create()
        self.oldTdo.copyFrom(anOldTdo)
        self.newTdo.copyFrom(aNewTdo)
        return self
    
    def doCommand(self):
        self.tdo.copyFrom(self.newTdo)
        TdoEditorForm.updateCaptionForNewTdoName()
        #v1.6b1
        TdoEditorForm.centerDrawingClick(TdoEditorForm)
        PdReplaceTdoCommand.doCommand(self)
    
    def undoCommand(self):
        PdReplaceTdoCommand.undoCommand(self)
        TdoEditorForm.updateCaptionForNewTdoName()
        #v1.6b1
        TdoEditorForm.centerDrawingClick(TdoEditorForm)
    
    def redoCommand(self):
        PdReplaceTdoCommand.redoCommand(self)
        TdoEditorForm.updateCaptionForNewTdoName()
        #v1.6b1
        TdoEditorForm.centerDrawingClick(TdoEditorForm)
    
    def description(self):
        result = ""
        result = "DXF"
        return result
    
