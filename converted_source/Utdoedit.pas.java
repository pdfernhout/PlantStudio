// unit Utdoedit

from conversion_common import *;
import ubmpsupport;
import uwait;
import ucursor;
import updform;
import delphi_compatability;

// const
kSplitterDragToTopMinPixels = 50;
kSplitterDragToBottomMinPixels = 50;
kSplitterDragToLeftMinPixels = 100;
kSplitterDragToRightMinPixels = 50;
kBetweenGap = 4;
kDrawAsLeaf = 0;
kDrawAsFlower = 1;
kDrawAsFruit = 2;
kCursorModeScroll = 0;
kCursorModeMagnify = 1;
kCursorModeRotate = 2;
kCursorModeAddTriangles = 3;
kCursorModeDeleteTriangles = 4;
kCursorModeDragPoints = 5;
kCursorModeFlipTriangles = 6;
kLineColor = delphi_compatability.clBlack;
kLightUpColor = delphi_compatability.clRed;
kConnectedPointColor = delphi_compatability.clBlue;
kUnconnectedPointColor = delphi_compatability.clGreen;
kOriginPointColor = delphi_compatability.clBlack;


// var
TTdoEditorForm TdoEditorForm = new TTdoEditorForm();



class PdTdoPaintBox extends TPaintBox {
    public TBitmap bitmap;
    public boolean canRotate;
    public boolean draggingIn;
    public float scale;
    public float xRotation;
    public float yRotation;
    public float zRotation;
    public TPoint drawPosition;
    public TPoint startDragPosition;
    public TRect tdoBoundsRect;
    
    //$R *.DFM
    // --------------------------------------------------------------------------------- PdTdoImage 
    public void create(TComponent anOwner) {
        super.create(anOwner);
        this.bitmap = delphi_compatability.TBitmap().Create();
    }
    
    public void destroy() {
        this.bitmap.free;
        this.bitmap = null;
        super.destroy();
    }
    
    public void magnifyOrReduce(float newScale, TPoint clickPoint) {
        this.drawPosition.X = intround(clickPoint.X + (this.drawPosition.X - clickPoint.X) * newScale / this.scale);
        this.drawPosition.Y = intround(clickPoint.Y + (this.drawPosition.Y - clickPoint.Y) * newScale / this.scale);
        this.scale = newScale;
        this.Paint();
    }
    
    public void centerTdo() {
        float xScale = 0.0;
        float yScale = 0.0;
        float newScale = 0.0;
        KfTurtle turtle = new KfTurtle();
        
        xScale = UNRESOLVED.safedivExcept(0.75 * this.scale * this.Width, UNRESOLVED.rWidth(this.tdoBoundsRect), 0.1);
        yScale = UNRESOLVED.safedivExcept(0.75 * this.scale * this.Height, UNRESOLVED.rHeight(this.tdoBoundsRect), 0.1);
        newScale = UNRESOLVED.min(xScale, yScale);
        if (TdoEditorForm.tdo != null) {
            turtle = UNRESOLVED.KfTurtle.defaultStartUsing;
            try {
                this.drawPosition = TdoEditorForm.tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(this.Width, this.Height), newScale);
            } finally {
                UNRESOLVED.KfTurtle.defaultStopUsing;
            }
        } else {
            this.drawPosition = Point(this.Width / 2, this.Height - 10);
        }
        this.magnifyOrReduce(newScale, this.drawPosition);
    }
    
    public void resetRotations() {
        this.xRotation = 0;
        this.yRotation = 0;
        this.zRotation = 0;
        this.Paint();
    }
    
}
class TTdoEditorForm extends PdForm {
    public TButton ok;
    public TButton cancel;
    public TButton undoLast;
    public TButton redoLast;
    public TPanel toolbarPanel;
    public TSpeedButton dragCursorMode;
    public TSpeedButton magnifyCursorMode;
    public TSpeedButton scrollCursorMode;
    public TSpeedButton addTrianglePointsCursorMode;
    public TSpeedButton removeTriangleCursorMode;
    public TSpeedButton flipTriangleCursorMode;
    public TSpeedButton rotateCursorMode;
    public TPanel optionsPanel;
    public TCheckBox fillTriangles;
    public TSpinEdit plantParts;
    public TLabel drawAsLabel;
    public TPanel picturesPanel;
    public TPanel verticalSplitter;
    public TPanel horizontalSplitter;
    public TCheckBox drawLines;
    public TButton writeToDXF;
    public TButton renameTdo;
    public TLabel Label1;
    public TSpinEdit circlePointSize;
    public TSpeedButton helpButton;
    public TSpeedButton mirrorTdo;
    public TSpeedButton reverseZValues;
    public TSpeedButton centerDrawing;
    public TSpeedButton resetRotations;
    public TButton writeToPOV;
    public TCheckBox mirrorHalf;
    public TButton ReadFromDXF;
    public TLabel connectionPointLabel;
    public TSpinEdit connectionPoint;
    public TButton clearTdo;
    public KfObject3d tdo;
    public KfObject3d originalTdo;
    public PdParameter param;
    public PdTdoPaintBox editPaintBox;
    public PdTdoPaintBox viewPaintBoxOne;
    public PdTdoPaintBox viewPaintBoxTwo;
    public PdTdoPaintBox paintBoxClickedIn;
    public PdCommandList commandList;
    public boolean internalChange;
    public boolean actionInProgress;
    public boolean scrolling;
    public boolean rotating;
    public TPoint startDragPoint;
    public TPoint scrollStartPosition;
    public boolean draggingPoint;
    public short pointIndexBeingDragged;
    public short cursorMode;
    public short rotateDirection;
    public short pointRadius;
    public float rotateStartAngle;
    public boolean lastCommandWasApply;
    public boolean lastCommandWasUndoApply;
    public  editPoints;
    public short numEditPoints;
    public short numNewPoints;
    public  newPointIndexes;
    public  newPoints;
    public boolean horizontalSplitterDragging;
    public boolean verticalSplitterDragging;
    public boolean horizontalSplitterNeedToRedraw;
    public boolean verticalSplitterNeedToRedraw;
    public int horizontalSplitterStartPos;
    public int verticalSplitterStartPos;
    public int horizontalSplitterLastDrawPos;
    public int verticalSplitterLastDrawPos;
    public int lastPicturesPanelWidth;
    public int lastPicturesPanelHeight;
    
    // resizing and splitting 
    // creation/destruction 
    // -------------------------------------------------------------------------------------------- *creation/destruction 
    public void create(TComponent AOwner) {
        super.create(AOwner);
        TdoEditorForm = this;
        this.tdo = UNRESOLVED.KfObject3D.create;
        this.commandList = UNRESOLVED.PdCommandList.create;
        this.commandList.setNewUndoLimit(UNRESOLVED.domain.options.undoLimit);
        this.commandList.setNewObjectUndoLimit(UNRESOLVED.domain.options.undoLimitOfPlants);
        this.editPaintBox = PdTdoPaintBox().create(this);
        this.editPaintBox.Parent = this.picturesPanel;
        this.editPaintBox.OnMouseDown = this.editPaintBoxMouseDown;
        this.editPaintBox.OnMouseMove = this.imagesMouseMove;
        this.editPaintBox.OnMouseUp = this.imagesMouseUp;
        this.editPaintBox.OnPaint = this.editPaintBoxPaint;
        this.editPaintBox.scale = 1.5;
        this.editPaintBox.Cursor = ucursor.crScroll;
        this.viewPaintBoxOne = PdTdoPaintBox().create(this);
        this.viewPaintBoxOne.Parent = this.picturesPanel;
        this.viewPaintBoxOne.OnMouseDown = this.viewPaintBoxOneMouseDown;
        this.viewPaintBoxOne.OnMouseMove = this.imagesMouseMove;
        this.viewPaintBoxOne.OnMouseUp = this.imagesMouseUp;
        this.viewPaintBoxOne.OnPaint = this.viewPaintBoxOnePaint;
        this.viewPaintBoxOne.scale = 0.5;
        this.viewPaintBoxOne.Cursor = ucursor.crScroll;
        this.viewPaintBoxTwo = PdTdoPaintBox().create(this);
        this.viewPaintBoxTwo.Parent = this.picturesPanel;
        this.viewPaintBoxTwo.OnMouseDown = this.viewPaintBoxTwoMouseDown;
        this.viewPaintBoxTwo.OnMouseMove = this.imagesMouseMove;
        this.viewPaintBoxTwo.OnMouseUp = this.imagesMouseUp;
        this.viewPaintBoxTwo.OnPaint = this.viewPaintBoxTwoPaint;
        this.viewPaintBoxTwo.scale = 0.5;
        this.viewPaintBoxTwo.Cursor = ucursor.crScroll;
        this.updateButtonsForUndoRedo();
    }
    
    public void FormCreate(TObject Sender) {
        TRect tempBoundsRect = new TRect();
        
        // keep window on screen - left corner of title bar 
        tempBoundsRect = UNRESOLVED.domain.tdoEditorWindowRect;
        if ((tempBoundsRect.Left != 0) || (tempBoundsRect.Right != 0) || (tempBoundsRect.Top != 0) || (tempBoundsRect.Bottom != 0)) {
            if (tempBoundsRect.Left > delphi_compatability.Screen.Width - UNRESOLVED.kMinWidthOnScreen) {
                tempBoundsRect.Left = delphi_compatability.Screen.Width - UNRESOLVED.kMinWidthOnScreen;
            }
            if (tempBoundsRect.Top > delphi_compatability.Screen.Height - UNRESOLVED.kMinHeightOnScreen) {
                tempBoundsRect.Top = delphi_compatability.Screen.Height - UNRESOLVED.kMinHeightOnScreen;
            }
            this.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom);
        }
        this.scrollCursorMode.Down = true;
        this.scrollCursorModeClick(this);
        this.internalChange = true;
        this.circlePointSize.Value = UNRESOLVED.domain.options.circlePointSizeInTdoEditor;
        this.plantParts.Value = UNRESOLVED.domain.options.partsInTdoEditor;
        this.fillTriangles.Checked = UNRESOLVED.domain.options.fillTrianglesInTdoEditor;
        this.drawLines.Checked = UNRESOLVED.domain.options.drawLinesInTdoEditor;
        this.internalChange = false;
        this.pointRadius = this.circlePointSize.Value / 2;
        this.toolbarPanel.BevelOuter = UNRESOLVED.bvNone;
        //optionsPanel.bevelOuter := bvNone;
    }
    
    public void initializeWithTdoAndParameter(KfObject3D aTdo, PdParameter aParam) {
        this.originalTdo = aTdo;
        if (this.originalTdo == null) {
            throw new GeneralException.create("Problem: Nil 3D object in method TTdoEditorForm.initializeWithTdoAndParameter.");
        }
        this.param = aParam;
        if (this.param == null) {
            throw new GeneralException.create("Problem: Nil parameter in method TTdoEditorForm.initializeWithTdoAndParameter.");
        }
        this.tdo.copyFrom(this.originalTdo);
        this.updateCaptionForNewTdoName();
        this.updateForChangeToNumberOfPoints();
        //v1.6b1
        this.centerDrawingClick(this);
    }
    
    public void initializeWithTdo(KfObject3D aTdo) {
        this.originalTdo = aTdo;
        if (this.originalTdo == null) {
            throw new GeneralException.create("Problem: Nil 3D object in method TTdoEditorForm.initializeWithTdo.");
        }
        this.tdo.copyFrom(this.originalTdo);
        this.updateCaptionForNewTdoName();
        this.updateForChangeToNumberOfPoints();
        //v1.6b1
        this.centerDrawingClick(this);
    }
    
    public void destroy() {
        this.tdo.free;
        this.tdo = null;
        this.commandList.free;
        this.commandList = null;
        // don't free paint boxes because we are their owner 
        super.destroy();
    }
    
    // -------------------------------------------------------------------------------- *command list 
    public void undoLastClick(TObject Sender) {
        if (this.lastCommandWasApply) {
            UNRESOLVED.MainForm.MenuEditUndoClick(UNRESOLVED.MainForm);
            this.lastCommandWasUndoApply = true;
            this.lastCommandWasApply = false;
            this.updateButtonsForUndoRedo();
        } else {
            this.commandList.undoLast;
            this.updateButtonsForUndoRedo();
            this.updateForChangeToTdo();
        }
    }
    
    public void redoLastClick(TObject Sender) {
        if (this.lastCommandWasUndoApply) {
            UNRESOLVED.MainForm.MenuEditRedoClick(UNRESOLVED.MainForm);
            this.lastCommandWasUndoApply = false;
            this.lastCommandWasApply = true;
            this.updateButtonsForUndoRedo();
        } else {
            this.commandList.redoLast;
            this.updateButtonsForUndoRedo();
            this.updateForChangeToTdo();
        }
    }
    
    // updating 
    // ------------------------------------------------------------------------------- *updating 
    public void updateButtonsForUndoRedo() {
        if (this.lastCommandWasApply) {
            this.undoLast.Enabled = true;
            this.undoLast.Caption = "&Undo apply";
        } else if (this.lastCommandWasUndoApply) {
            this.redoLast.Enabled = true;
            this.redoLast.Caption = "&Redo apply";
        } else {
            if (this.commandList.isUndoEnabled) {
                this.undoLast.Enabled = true;
                this.undoLast.Caption = "&Undo " + this.commandList.undoDescription;
            } else {
                this.undoLast.Enabled = false;
                this.undoLast.Caption = "Can't undo";
            }
            if (this.commandList.isRedoEnabled) {
                this.redoLast.Enabled = true;
                this.redoLast.Caption = "&Redo " + this.commandList.redoDescription;
            } else {
                this.redoLast.Enabled = false;
                this.redoLast.Caption = "Can't redo";
            }
        }
    }
    
    public void updateForChangeToTdo() {
        this.updateButtonsForUndoRedo();
        this.updateForChangeToNumberOfPoints();
        this.updateForChangeToConnectionPointIndex();
        this.clearTdo.Enabled = (this.tdo != null) && (this.tdo.pointsInUse > 0);
        if ((this.editPaintBox != null) && (this.viewPaintBoxOne != null) && (this.viewPaintBoxTwo != null)) {
            this.editPaintBox.Paint();
            this.viewPaintBoxOne.Paint();
            this.viewPaintBoxTwo.Paint();
        }
    }
    
    public void updateForChangeToClickedOnPaintBox() {
        this.updateButtonsForUndoRedo();
        if (this.paintBoxClickedIn != null) {
            this.paintBoxClickedIn.Paint();
        }
    }
    
    public void updateCaptionForNewTdoName() {
        this.Caption = "3D object editor - " + this.tdo.getName;
        this.Invalidate();
    }
    
    public void updateForChangeToNumberOfPoints() {
        this.internalChange = true;
        this.connectionPoint.Value = this.tdo.originPointIndex + 1;
        this.connectionPoint.MaxValue = this.tdo.pointsInUse;
        this.connectionPointLabel.Caption = "Connection point (1-" + IntToStr(this.connectionPoint.MaxValue) + ")";
        this.internalChange = false;
    }
    
    public void updateForChangeToConnectionPointIndex() {
        TPoint oldPoint = new TPoint();
        TPoint newPoint = new TPoint();
        
        this.internalChange = true;
        this.connectionPoint.Value = this.tdo.originPointIndex + 1;
        this.internalChange = false;
        //
        //  // adjust drawing point so 3D object does not move
        //  if connectionPoint.value - 1 <> tdo.originPointIndex then
        //    begin
        //    if (tdo.originPointIndex >= 0) and (tdo.originPointIndex <= numEditPoints - 1) then
        //      oldPoint := editPoints[tdo.originPointIndex]
        //    else
        //      oldPoint := Point(0, 0);
        //    if (connectionPoint.value - 1 >= 0) and (connectionPoint.value - 1 <= numEditPoints - 1) then
        //      newPoint := editPoints[connectionPoint.value - 1]
        //    else
        //      newPoint := Point(0, 0);
        //    editPaintBox.drawPosition.x := editPaintBox.drawPosition.x + (newPoint.x - oldPoint.x);
        //    editPaintBox.drawPosition.y := editPaintBox.drawPosition.y + (newPoint.y - oldPoint.y);
        //    end;
        //  tdo.setOriginPointIndex(connectionPoint.value - 1);
        //  if editPaintBox <> nil then editPaintBox.paint;
        //  
    }
    
    // -------------------------------------------------------------------------------------- *buttons 
    public void okClick(TObject Sender) {
        this.ModalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    public void FormClose(TObject Sender, TCloseAction Action) {
        // save settings to domain even if they clicked cancel or clicked the close box
        UNRESOLVED.domain.tdoEditorWindowRect = Rect(this.Left, this.Top, this.Width, this.Height);
        UNRESOLVED.domain.options.circlePointSizeInTdoEditor = this.circlePointSize.Value;
        UNRESOLVED.domain.options.partsInTdoEditor = this.plantParts.Value;
        UNRESOLVED.domain.options.fillTrianglesInTdoEditor = this.fillTriangles.Checked;
        UNRESOLVED.domain.options.drawLinesInTdoEditor = this.drawLines.Checked;
    }
    
    public void applyClick(TObject Sender) {
        UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeTdoValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.tdo, this.param.fieldNumber, this.param.regrow));
        this.lastCommandWasApply = true;
        this.updateButtonsForUndoRedo();
    }
    
    public void renameTdoClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        ansistring newName = new ansistring();
        
        newName = this.tdo.getName;
        if (!InputQuery("Enter new name", "Type a new name for " + newName + ".", newName)) {
            return;
        }
        newCommand = PdRenameTdoCommand().createWithTdoAndNewName(this.tdo, newName);
        this.doCommand(newCommand);
    }
    
    public void clearTdoClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = PdClearAllPointsCommand().createWithTdo(this.tdo);
        this.doCommand(newCommand);
    }
    
    public void writeToDXFClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        String suggestedName = "";
        
        suggestedName = "export.dxf";
        if (!UNRESOLVED.getFileSaveInfo(UNRESOLVED.kFileTypeDXF, UNRESOLVED.kAskForFileName, suggestedName, fileInfo)) {
            return;
        }
        try {
            UNRESOLVED.startFileSave(fileInfo);
            this.tdo.writeToDXFFile(fileInfo.tempFile, UNRESOLVED.kTdoForeColor, UNRESOLVED.kTdoBackColor);
            fileInfo.writingWasSuccessful = true;
        } finally {
            UNRESOLVED.cleanUpAfterFileSave(fileInfo);
        }
    }
    
    public void ReadFromDXFClick(TObject Sender) {
        String fileNameWithPath = "";
        KfObject3D newTdo = new KfObject3D();
        TextFile inputFile = new TextFile();
        PdCommand newCommand = new PdCommand();
        
        newTdo = null;
        fileNameWithPath = UNRESOLVED.getFileOpenInfo(UNRESOLVED.kFileTypeDXF, "input.dxf", "Choose a DXF file");
        if (fileNameWithPath == "") {
            return;
        }
        try {
            uwait.startWaitMessage("Reading " + ExtractFileName(fileNameWithPath));
            AssignFile(inputFile, fileNameWithPath);
            try {
                // v1.5
                UNRESOLVED.setDecimalSeparator;
                Reset(inputFile);
                newTdo = UNRESOLVED.KfObject3D.create;
                newTdo.readFromDXFFile(inputFile);
                // v1.6b1
                newTdo.setName(UNRESOLVED.stringUpTo(ExtractFileName(fileNameWithPath), "."));
            } finally {
                CloseFile(inputFile);
            }
        } catch (Exception E) {
            uwait.stopWaitMessage();
            ShowMessage(E.message);
            ShowMessage("Could not load file " + fileNameWithPath);
            return;
        }
        if (newTdo != null) {
            newCommand = PdLoadTdoFromDXFCommand().createWithOldAndNewTdo(this.tdo, newTdo);
            this.doCommand(newCommand);
        }
        uwait.stopWaitMessage();
    }
    
    public void writeToPOVClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        String suggestedName = "";
        
        suggestedName = UNRESOLVED.replacePunctuationWithUnderscores(this.tdo.getName) + ".inc";
        if (!UNRESOLVED.getFileSaveInfo(UNRESOLVED.kFileTypeINC, UNRESOLVED.kAskForFileName, suggestedName, fileInfo)) {
            return;
        }
        try {
            UNRESOLVED.startFileSave(fileInfo);
            this.tdo.writeToPOV_INCFile(fileInfo.tempFile, UNRESOLVED.kTdoForeColor, UNRESOLVED.kEmbeddedInPlant, this.plantParts.Value);
            fileInfo.writingWasSuccessful = true;
        } finally {
            UNRESOLVED.cleanUpAfterFileSave(fileInfo);
        }
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Editing_3D_objects");
    }
    
    // mouse handling 
    // ------------------------------------------------------------------------------------- *mouse handling 
    public void imagesMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        PdCommand newCommand = new PdCommand();
        TPoint anchorPoint = new TPoint();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.paintBoxClickedIn == null) {
            return;
        }
        if (this.actionInProgress) {
            try {
                //error somewhere - user did weird things with mouse buttons - teminate action...
                this.imagesMouseUp(Sender, Button, Shift, X, Y);
            } finally {
                this.actionInProgress = false;
            }
        }
        // makes shift-click work as right-click
        this.commandList.rightButtonDown = (Button == delphi_compatability.TMouseButton.mbRight) || (delphi_compatability.TShiftStateEnum.ssShift in Shift);
        switch (this.cursorMode) {
            case kCursorModeMagnify:
                if (this.commandList.rightButtonDown) {
                    this.paintBoxClickedIn.Cursor = ucursor.crMagMinus;
                }
                break;
            case kCursorModeScroll:
                if (this.commandList.rightButtonDown) {
                    return;
                }
                this.scrolling = true;
                this.startDragPoint = Point(X, Y);
                this.scrollStartPosition = this.paintBoxClickedIn.drawPosition;
                break;
            case kCursorModeRotate:
                if (this.paintBoxClickedIn != this.editPaintBox) {
                    this.rotating = true;
                    this.startDragPoint = Point(X, Y);
                    this.rotateDirection = UNRESOLVED.kRotateNotInitialized;
                    if (this.commandList.rightButtonDown) {
                        this.paintBoxClickedIn.Cursor = delphi_compatability.crSizeWE;
                    }
                }
                break;
            case kCursorModeAddTriangles:
                if (this.numNewPoints >= 3) {
                    this.numNewPoints = 0;
                }
                break;
            default:
                if ((this.commandList.rightButtonDown) && (this.cursorMode != kCursorModeDragPoints)) {
                    return;
                }
                anchorPoint = Point(X, Y);
                this.actionInProgress = true;
                newCommand = this.makeMouseCommand(anchorPoint, (delphi_compatability.TShiftStateEnum.ssShift in Shift), (delphi_compatability.TShiftStateEnum.ssCtrl in Shift));
                if (newCommand != null) {
                    this.actionInProgress = this.commandList.mouseDown(newCommand, anchorPoint);
                } else {
                    this.actionInProgress = false;
                }
                if (this.actionInProgress) {
                    this.updateForChangeToTdo();
                }
                break;
    }
    
    public void imagesMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if ((Sender == this.editPaintBox)) {
            switch (this.cursorMode) {
                case kCursorModeAddTriangles:
                    if (this.numNewPoints == 0) {
                        this.lightUpPointAtMouse(X, Y, UNRESOLVED.kDrawNow);
                    }
                    break;
                case kCursorModeDragPoints:
                    if (this.numNewPoints == 0) {
                        this.lightUpPointAtMouse(X, Y, UNRESOLVED.kDrawNow);
                    }
                    break;
                case kCursorModeDeleteTriangles:
                    this.lightUpTriangleAtMouse(X, Y);
                    break;
                case kCursorModeFlipTriangles:
                    this.lightUpTriangleAtMouse(X, Y);
                    break;
        }
        if (this.paintBoxClickedIn == null) {
            return;
        }
        if (Sender != this.paintBoxClickedIn) {
            return;
        }
        switch (this.cursorMode) {
            case kCursorModeMagnify:
                if (this.scrolling) {
                    this.scrollBy(X, Y);
                }
                break;
            case kCursorModeScroll:
                if (this.scrolling) {
                    this.scrollBy(X, Y);
                }
                break;
            case kCursorModeRotate:
                if (this.rotating) {
                    this.rotateBy(X, Y);
                }
                break;
            case kCursorModeAddTriangles:
                if (Sender == this.editPaintBox) {
                    if ((this.numNewPoints == 1) || (this.numNewPoints == 2)) {
                        this.lightUpAddingLineAtMouse(X, Y);
                    }
                }
                break;
            default:
                if (this.actionInProgress) {
                    this.commandList.mouseMove(Point(X, Y));
                    this.updateForChangeToTdo();
                }
                break;
    }
    
    public void imagesMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        KfIndexTriangle triangle = new KfIndexTriangle();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.paintBoxClickedIn == null) {
            return;
        }
        if (this.cursorMode != kCursorModeAddTriangles) {
            this.numNewPoints = 0;
        }
        try {
            switch (this.cursorMode) {
                case kCursorModeMagnify:
                    if ((this.commandList.rightButtonDown)) {
                        this.paintBoxClickedIn.magnifyOrReduce(this.paintBoxClickedIn.scale * 0.75, Point(X, Y));
                        if (!(delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                            this.paintBoxClickedIn.Cursor = ucursor.crMagPlus;
                        }
                    } else if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                        this.paintBoxClickedIn.magnifyOrReduce(this.paintBoxClickedIn.scale * 0.75, Point(X, Y));
                    } else {
                        this.paintBoxClickedIn.magnifyOrReduce(this.paintBoxClickedIn.scale * 1.5, Point(X, Y));
                    }
                    break;
                case kCursorModeScroll:
                    if (this.scrolling) {
                        this.scrollBy(X, Y);
                    }
                    break;
                case kCursorModeRotate:
                    if (this.rotating) {
                        this.rotateBy(X, Y);
                    }
                    if (this.paintBoxClickedIn != this.editPaintBox) {
                        this.paintBoxClickedIn.Cursor = ucursor.crRotate;
                    }
                    break;
                case kCursorModeFlipTriangles:
                    if (this.paintBoxClickedIn == this.editPaintBox) {
                        triangle = this.triangleAtMouse(X, Y);
                        if (triangle != null) {
                            triangle.flip;
                            this.updateForChangeToTdo();
                        }
                    }
                    break;
                case kCursorModeAddTriangles:
                    if (this.paintBoxClickedIn == this.editPaintBox) {
                        this.addTrianglePoints(X, Y);
                    }
                    break;
                default:
                    if (this.actionInProgress) {
                        this.commandList.mouseUp(Point(X, Y));
                        this.actionInProgress = false;
                        this.updateForChangeToTdo();
                    }
                    break;
        } finally {
            this.scrolling = false;
            this.rotating = false;
            this.commandList.rightButtonDown = false;
            this.actionInProgress = false;
            this.draggingPoint = false;
        }
    }
    
    public void editPaintBoxMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.paintBoxClickedIn = this.editPaintBox;
        this.imagesMouseDown(Sender, Button, Shift, X, Y);
    }
    
    public void viewPaintBoxOneMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.paintBoxClickedIn = this.viewPaintBoxOne;
        this.imagesMouseDown(Sender, Button, Shift, X, Y);
    }
    
    public void viewPaintBoxTwoMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.paintBoxClickedIn = this.viewPaintBoxTwo;
        this.imagesMouseDown(Sender, Button, Shift, X, Y);
    }
    
    // -------------------------------------------------------------------------------- *finding and lighting up 
    public void lightUpPointAtMouse(int x, int y, boolean immediate) {
        short i = 0;
        short pointFound = 0;
        
        pointFound = -1;
        if (this.draggingPoint) {
            if ((this.pointIndexBeingDragged >= 0) && (this.pointIndexBeingDragged <= this.numEditPoints - 1)) {
                pointFound = this.pointIndexBeingDragged;
            }
        } else {
            pointFound = this.pointIndexAtMouse(x, y);
        }
        if (pointFound >= 0) {
            this.editPaintBox.bitmap.Canvas.Pen.Color = kLightUpColor;
            this.editPaintBox.bitmap.Canvas.Brush.Color = kLightUpColor;
            this.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
            this.editPaintBox.bitmap.Canvas.Ellipse(this.editPoints[pointFound].X - this.pointRadius, this.editPoints[pointFound].Y - this.pointRadius, this.editPoints[pointFound].X + this.pointRadius, this.editPoints[pointFound].Y + this.pointRadius);
        } else {
            if (!this.draggingPoint) {
                if (this.numEditPoints > 0) {
                    for (i = 0; i <= this.numEditPoints - 1; i++) {
                        if (i == this.tdo.originPointIndex) {
                            this.editPaintBox.bitmap.Canvas.Pen.Color = kOriginPointColor;
                            this.editPaintBox.bitmap.Canvas.Brush.Color = kOriginPointColor;
                        } else {
                            this.editPaintBox.bitmap.Canvas.Pen.Color = kConnectedPointColor;
                            this.editPaintBox.bitmap.Canvas.Brush.Color = kConnectedPointColor;
                        }
                        this.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
                        this.editPaintBox.bitmap.Canvas.Ellipse(this.editPoints[i].X - this.pointRadius, this.editPoints[i].Y - this.pointRadius, this.editPoints[i].X + this.pointRadius, this.editPoints[i].Y + this.pointRadius);
                    }
                }
            }
        }
        if (immediate) {
            this.drawPaintBoxBitmapOnCanvas(this.editPaintBox);
        }
    }
    
    public short pointIndexAtMouse(int x, int y) {
        result = 0;
        short i = 0;
        
        result = -1;
        if (this.numEditPoints > 0) {
            for (i = 0; i <= this.numEditPoints - 1; i++) {
                if ((abs(x - this.editPoints[i].X) <= this.pointRadius) && (abs(y - this.editPoints[i].Y) <= this.pointRadius)) {
                    result = i;
                    return result;
                }
            }
        }
        return result;
    }
    
    public void lightUpTriangleAtMouse(int x, int y) {
        KfIndexTriangle triangle = new KfIndexTriangle();
         aPolygon = [0] * (range(0, 2 + 1) + 1);
        
        this.drawTdoOnTdoPaintBox(this.editPaintBox, UNRESOLVED.kDontDrawYet);
        triangle = this.triangleAtMouse(x, y);
        if (triangle != null) {
            this.editPaintBox.bitmap.Canvas.Pen.Color = kLightUpColor;
            this.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
            aPolygon[0] = this.editPoints[triangle.pointIndexes[0] - 1];
            aPolygon[1] = this.editPoints[triangle.pointIndexes[1] - 1];
            aPolygon[2] = this.editPoints[triangle.pointIndexes[2] - 1];
            this.editPaintBox.bitmap.Canvas.Polygon(aPolygon);
        }
        this.drawPaintBoxBitmapOnCanvas(this.editPaintBox);
    }
    
    public KfIndexTriangle triangleAtMouse(int x, int y) {
        result = new KfIndexTriangle();
        short i = 0;
        KfIndexTriangle triangle = new KfIndexTriangle();
         polygon = [0] * (range(0, 2 + 1) + 1);
        HRgn hPolygon = new HRgn();
        boolean inTriangle = false;
        
        result = null;
        if (this.tdo.triangles.count > 0) {
            for (i = 0; i <= this.tdo.triangles.count - 1; i++) {
                triangle = UNRESOLVED.KfIndexTriangle(this.tdo.triangles.items[i]);
                polygon[0] = this.editPoints[triangle.pointIndexes[0] - 1];
                polygon[1] = this.editPoints[triangle.pointIndexes[1] - 1];
                polygon[2] = this.editPoints[triangle.pointIndexes[2] - 1];
                hPolygon = UNRESOLVED.createPolygonRgn(polygon, 3, delphi_compatability.ALTERNATE);
                UNRESOLVED.selectObject(this.Handle, hPolygon);
                try {
                    inTriangle = UNRESOLVED.ptInRegion(hPolygon, x, y);
                } finally {
                    UNRESOLVED.deleteObject(hPolygon);
                }
                if (inTriangle) {
                    result = UNRESOLVED.KfIndexTriangle(this.tdo.triangles.items[i]);
                    return result;
                }
            }
        }
        return result;
    }
    
    public void scrollBy(int x, int y) {
        this.paintBoxClickedIn.drawPosition.X = this.scrollStartPosition.X + x - this.startDragPoint.X;
        this.paintBoxClickedIn.drawPosition.Y = this.scrollStartPosition.Y + y - this.startDragPoint.Y;
        this.updateForChangeToClickedOnPaintBox();
    }
    
    public void rotateBy(int x, int y) {
        if ((this.rotateDirection == UNRESOLVED.kRotateNotInitialized) && ((abs(x - this.startDragPoint.X) > 5) || (abs(y - this.startDragPoint.Y) > 5))) {
            if (this.commandList.rightButtonDown) {
                // don't initialize for first few pixels so any wobbling at the start doesn't start you out
                //    in the wrong direction 
                this.rotateDirection = UNRESOLVED.kRotateZ;
            } else if (abs(x - this.startDragPoint.X) > abs(y - this.startDragPoint.Y)) {
                this.rotateDirection = UNRESOLVED.kRotateX;
            } else {
                this.rotateDirection = UNRESOLVED.kRotateY;
            }
            switch (this.rotateDirection) {
                case UNRESOLVED.kRotateX:
                    this.rotateStartAngle = this.paintBoxClickedIn.xRotation;
                    break;
                case UNRESOLVED.kRotateY:
                    this.rotateStartAngle = this.paintBoxClickedIn.yRotation;
                    break;
                case UNRESOLVED.kRotateZ:
                    this.rotateStartAngle = this.paintBoxClickedIn.zRotation;
                    break;
        }
        switch (this.rotateDirection) {
            case UNRESOLVED.kRotateX:
                this.paintBoxClickedIn.xRotation = UNRESOLVED.min(360, UNRESOLVED.max(-360, this.rotateStartAngle + (x - this.startDragPoint.X) * 0.5));
                break;
            case UNRESOLVED.kRotateY:
                this.paintBoxClickedIn.yRotation = UNRESOLVED.min(360, UNRESOLVED.max(-360, this.rotateStartAngle + (y - this.startDragPoint.Y) * 0.5));
                break;
            case UNRESOLVED.kRotateZ:
                this.paintBoxClickedIn.zRotation = UNRESOLVED.min(360, UNRESOLVED.max(-360, this.rotateStartAngle + (this.startDragPoint.X - x) * 0.5));
                break;
        this.updateForChangeToClickedOnPaintBox();
    }
    
    public void addTrianglePoints(short x, short y) {
        short pointIndex = 0;
        PdCommand newCommand = new PdCommand();
        TRect circleRect = new TRect();
        TPoint newPoint = new TPoint();
        
        this.numNewPoints += 1;
        pointIndex = this.pointIndexAtMouse(x, y);
        this.newPointIndexes[this.numNewPoints - 1] = pointIndex;
        if (pointIndex >= 0) {
            this.newPoints[this.numNewPoints - 1] = this.tdo.points[pointIndex];
        } else {
            this.newPoints[this.numNewPoints - 1].x = (x - this.editPaintBox.drawPosition.X) / this.editPaintBox.scale;
            this.newPoints[this.numNewPoints - 1].y = (y - this.editPaintBox.drawPosition.Y) / this.editPaintBox.scale;
            this.newPoints[this.numNewPoints - 1].z = 0;
        }
        this.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        this.editPaintBox.bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid;
        this.editPaintBox.bitmap.Canvas.Brush.Color = kUnconnectedPointColor;
        this.editPaintBox.bitmap.Canvas.Pen.Color = kUnconnectedPointColor;
        newPoint.X = this.editPaintBox.drawPosition.X + intround(this.newPoints[this.numNewPoints - 1].x * this.editPaintBox.scale);
        newPoint.Y = this.editPaintBox.drawPosition.Y + intround(this.newPoints[this.numNewPoints - 1].y * this.editPaintBox.scale);
        circleRect = Rect(newPoint.X - this.pointRadius, newPoint.Y - this.pointRadius, newPoint.X + this.pointRadius, newPoint.Y + this.pointRadius);
        this.editPaintBox.bitmap.Canvas.Ellipse(circleRect.Left, circleRect.Top, circleRect.Right, circleRect.Bottom);
        if (this.numNewPoints >= 3) {
            newCommand = PdAddTdoTriangleCommand().createWithTdoAndNewPoints(this.tdo, this.newPointIndexes, this.newPoints);
            this.numNewPoints = 0;
            this.newPointIndexes[0] = 0;
            this.newPointIndexes[1] = 0;
            this.newPointIndexes[2] = 0;
            this.doCommand(newCommand);
        }
        if (this.numNewPoints < 3) {
            this.drawPaintBoxBitmapOnCanvas(this.editPaintBox);
        }
    }
    
    public void drawPaintBoxBitmapOnCanvas(PdTdoPaintBox aPaintBox) {
        if (aPaintBox != null) {
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(aPaintBox.bitmap, aPaintBox.Canvas, Rect(0, 0, 0, 0));
        }
    }
    
    public void lightUpAddingLineAtMouse(short x, short y) {
        TPoint firstPoint = new TPoint();
        TPoint secondPoint = new TPoint();
        
        this.editPaintBox.bitmap.Canvas.Brush.Color = delphi_compatability.clWindow;
        this.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        this.editPaintBox.bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear;
        this.editPaintBox.bitmap.Canvas.FillRect(Rect(0, 0, this.editPaintBox.Width, this.editPaintBox.Height));
        this.drawTdoOnTdoPaintBox(this.editPaintBox, UNRESOLVED.kDontDrawYet);
        this.lightUpPointAtMouse(x, y, UNRESOLVED.kDontDrawYet);
        firstPoint.X = this.editPaintBox.drawPosition.X + intround(this.newPoints[0].x * this.editPaintBox.scale);
        firstPoint.Y = this.editPaintBox.drawPosition.Y + intround(this.newPoints[0].y * this.editPaintBox.scale);
        if (this.numNewPoints > 1) {
            secondPoint.X = this.editPaintBox.drawPosition.X + intround(this.newPoints[1].x * this.editPaintBox.scale);
            secondPoint.Y = this.editPaintBox.drawPosition.Y + intround(this.newPoints[1].y * this.editPaintBox.scale);
        }
        this.editPaintBox.bitmap.Canvas.Pen.Color = kUnconnectedPointColor;
        this.editPaintBox.bitmap.Canvas.MoveTo(firstPoint.X, firstPoint.Y);
        if (this.numNewPoints > 1) {
            this.editPaintBox.bitmap.Canvas.LineTo(secondPoint.X, secondPoint.Y);
        }
        this.editPaintBox.bitmap.Canvas.LineTo(x, y);
        this.editPaintBox.bitmap.Canvas.Pen.Color = kUnconnectedPointColor;
        this.editPaintBox.bitmap.Canvas.Brush.Color = kUnconnectedPointColor;
        this.editPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        this.editPaintBox.bitmap.Canvas.Ellipse(firstPoint.X - this.pointRadius, firstPoint.Y - this.pointRadius, firstPoint.X + this.pointRadius, firstPoint.Y + this.pointRadius);
        if (this.numNewPoints > 1) {
            this.editPaintBox.bitmap.Canvas.Ellipse(secondPoint.X - this.pointRadius, secondPoint.Y - this.pointRadius, secondPoint.X + this.pointRadius, secondPoint.Y + this.pointRadius);
        }
        this.editPaintBox.bitmap.Canvas.Ellipse(x - this.pointRadius + 1, y - this.pointRadius + 1, x + this.pointRadius - 1, y + this.pointRadius - 1);
        this.drawPaintBoxBitmapOnCanvas(this.editPaintBox);
    }
    
    public PdCommand makeMouseCommand(TPoint point, boolean shift, boolean ctrl) {
        result = new PdCommand();
        result = null;
        if (this.paintBoxClickedIn != this.editPaintBox) {
            return result;
        }
        switch (this.cursorMode) {
            case kCursorModeAddTriangles:
                break;
            case kCursorModeDeleteTriangles:
                if (this.paintBoxClickedIn == this.editPaintBox) {
                    //handled in mouse up
                    result = PdRemoveTdoTriangleCommand().createWithTdo(this.tdo);
                }
                break;
            case kCursorModeDragPoints:
                if (this.paintBoxClickedIn == this.editPaintBox) {
                    result = PdDragTdoPointCommand().createWithTdoAndScale(this.tdo, this.paintBoxClickedIn.scale);
                }
                break;
        return result;
    }
    
    // drawing 
    // ------------------------------------------------------------------------------------- *drawing 
    public void editPaintBoxPaint(TObject Sender) {
        this.checkImageForBitmapSizeAndFill(this.editPaintBox);
        this.drawTdoOnTdoPaintBox(this.editPaintBox, UNRESOLVED.kDrawNow);
    }
    
    public void viewPaintBoxOnePaint(TObject Sender) {
        this.checkImageForBitmapSizeAndFill(this.viewPaintBoxOne);
        this.drawTdoOnTdoPaintBox(this.viewPaintBoxOne, UNRESOLVED.kDrawNow);
    }
    
    public void viewPaintBoxTwoPaint(TObject Sender) {
        this.checkImageForBitmapSizeAndFill(this.viewPaintBoxTwo);
        this.drawTdoOnTdoPaintBox(this.viewPaintBoxTwo, UNRESOLVED.kDrawNow);
    }
    
    public void checkImageForBitmapSizeAndFill(PdTdoPaintBox aPaintBox) {
        if ((aPaintBox.bitmap.Width != aPaintBox.Width) || (aPaintBox.bitmap.Height != aPaintBox.Height)) {
            try {
                aPaintBox.bitmap.Width = aPaintBox.Width;
                aPaintBox.bitmap.Height = aPaintBox.Height;
            } catch (Exception e) {
                aPaintBox.bitmap.Width = 1;
                aPaintBox.bitmap.Height = 1;
            }
        }
        aPaintBox.bitmap.Canvas.Brush.Color = delphi_compatability.clWindow;
        aPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        aPaintBox.bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear;
        aPaintBox.bitmap.Canvas.FillRect(Rect(0, 0, aPaintBox.Width, aPaintBox.Height));
    }
    
    public void drawTdoOnTdoPaintBox(PdTdoPaintBox aPaintBox, boolean immediate) {
        KfTurtle turtle = new KfTurtle();
        short i = 0;
        short parts = 0;
        boolean wasFillingTriangles = false;
        TPoint pointOfConnection = new TPoint();
        
        if (this.tdo == null) {
            return;
        }
        turtle = UNRESOLVED.KfTurtle.defaultStartUsing;
        try {
            // set up turtle
            turtle.drawingSurface.pane = aPaintBox.bitmap.Canvas;
            turtle.setDrawOptionsForDrawingTdoOnly;
            //FIX unresolved WITH expression: turtle.drawOptions
            this.drawLines = this.drawLines.Checked;
            UNRESOLVED.wireFrame = !this.fillTriangles.Checked;
            UNRESOLVED.circlePoints = aPaintBox == this.editPaintBox;
            if (aPaintBox == this.editPaintBox) {
                turtle.drawOptions.circlePointRadius = this.pointRadius;
                turtle.drawingSurface.circleColor = kConnectedPointColor;
            }
            // must be after pane and draw options set 
            turtle.reset;
            turtle.xyz(aPaintBox.drawPosition.X, aPaintBox.drawPosition.Y, 0);
            turtle.resetBoundsRect(aPaintBox.drawPosition);
            turtle.rotateX(aPaintBox.yRotation * 256 / 360);
            turtle.rotateY(aPaintBox.xRotation * 256 / 360);
            turtle.rotateZ(aPaintBox.zRotation * 256 / 360);
            // draw parts
            parts = this.plantParts.Value;
            if (aPaintBox == this.editPaintBox) {
                parts = 1;
            }
            if (parts == 0) {
                throw new GeneralException.create("Zero parts not allowed.");
            }
            turtle.drawingSurface.recordingStart;
            if (parts > 1) {
                turtle.rotateZ(-64);
            }
            for (i = 0; i <= parts - 1; i++) {
                if (parts > 1) {
                    turtle.rotateX(256 / parts);
                    turtle.push;
                    turtle.rotateY(64);
                    turtle.rotateX(64);
                }
                this.tdo.draw(turtle, aPaintBox.scale, "", "", 0, 0);
                if ((this.mirrorHalf.Checked) && (!(aPaintBox == this.editPaintBox))) {
                    turtle.push;
                    turtle.rotateY(256 / 2);
                    this.tdo.reverseZValues;
                    turtle.drawingSurface.foreColor = UNRESOLVED.rgb(255, 255, 200);
                    turtle.drawingSurface.backColor = UNRESOLVED.rgb(255, 255, 200);
                    turtle.drawingSurface.lineColor = delphi_compatability.clBlack;
                    this.tdo.draw(turtle, aPaintBox.scale, "", "", 0, 0);
                    turtle.drawingSurface.foreColor = UNRESOLVED.kTdoForeColor;
                    turtle.drawingSurface.backColor = UNRESOLVED.kTdoBackColor;
                    this.tdo.reverseZValues;
                    turtle.pop;
                }
                if (parts > 1) {
                    turtle.pop;
                }
            }
            turtle.drawingSurface.recordingStop;
            turtle.drawingSurface.recordingDraw;
            turtle.drawingSurface.clearTriangles;
            if (aPaintBox == this.editPaintBox) {
                // if edit panel, get new locations of edit points
                this.numEditPoints = turtle.recordedPointsInUse;
                if (this.numEditPoints > 0) {
                    for (i = 0; i <= this.numEditPoints - 1; i++) {
                        this.editPoints[i] = Point(intround(turtle.recordedPoints[i].x), intround(turtle.recordedPoints[i].y));
                    }
                }
                if (this.numEditPoints > 0) {
                    // draw connection point circle in black over rest
                    aPaintBox.bitmap.Canvas.Brush.Color = kOriginPointColor;
                    aPaintBox.bitmap.Canvas.Pen.Color = kOriginPointColor;
                    pointOfConnection = this.editPoints[this.tdo.originPointIndex];
                    aPaintBox.bitmap.Canvas.Ellipse(pointOfConnection.X - this.pointRadius, pointOfConnection.Y - this.pointRadius, pointOfConnection.X + this.pointRadius, pointOfConnection.Y + this.pointRadius);
                }
                if (this.draggingPoint) {
                    this.lightUpPointAtMouse(this.commandList.previousPoint.x, this.commandList.previousPoint.y, UNRESOLVED.kDontDrawYet);
                }
            }
            // get bounds rect from turtle
            aPaintBox.tdoBoundsRect = turtle.boundsRect;
            // draw border
            aPaintBox.bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
            aPaintBox.bitmap.Canvas.Pen.Color = UNRESOLVED.clBtnText;
            aPaintBox.bitmap.Canvas.Rectangle(0, 0, aPaintBox.Width, aPaintBox.Height);
            if (immediate) {
                // draw
                this.drawPaintBoxBitmapOnCanvas(aPaintBox);
            }
        } finally {
            UNRESOLVED.KfTurtle.defaultStopUsing;
        }
    }
    
    public void centerDrawingInPaintBox(PdTdoPaintBox aPaintBox) {
        float newScaleX = 0.0;
        float newScaleY = 0.0;
        TPoint centerPointOfTdoBoundsRect = new TPoint();
        TPoint centerOfPaintBox = new TPoint();
        TPoint offset = new TPoint();
        
        if (aPaintBox == null) {
            return;
        }
        // set high so it will never be too small
        aPaintBox.scale = 100.0;
        // 1. draw to determine new scale 
        this.drawTdoOnTdoPaintBox(aPaintBox, UNRESOLVED.kDontDrawYet);
        newScaleX = UNRESOLVED.safedivExcept(0.95 * aPaintBox.scale * aPaintBox.Width, UNRESOLVED.rWidth(aPaintBox.tdoBoundsRect), 0.1);
        newScaleY = UNRESOLVED.safedivExcept(0.95 * aPaintBox.scale * aPaintBox.Height, UNRESOLVED.rHeight(aPaintBox.tdoBoundsRect), 0.1);
        aPaintBox.scale = UNRESOLVED.min(newScaleX, newScaleY);
        // 2. draw to determine shift of drawPosition if any - fill in case this is last draw 
        aPaintBox.bitmap.Canvas.Brush.Color = delphi_compatability.clWhite;
        aPaintBox.bitmap.Canvas.FillRect(Rect(0, 0, aPaintBox.Width, aPaintBox.Height));
        this.drawTdoOnTdoPaintBox(aPaintBox, UNRESOLVED.kDontDrawYet);
        // v2 improved how this is done
        centerPointOfTdoBoundsRect = Point(aPaintBox.tdoBoundsRect.Left + (aPaintBox.tdoBoundsRect.Right - aPaintBox.tdoBoundsRect.Left) / 2, aPaintBox.tdoBoundsRect.Top + (aPaintBox.tdoBoundsRect.Bottom - aPaintBox.tdoBoundsRect.Top) / 2);
        centerOfPaintBox = Point(aPaintBox.Width / 2, aPaintBox.Height / 2);
        offset = Point(centerOfPaintBox.X - centerPointOfTdoBoundsRect.X, centerOfPaintBox.Y - centerPointOfTdoBoundsRect.Y);
        aPaintBox.drawPosition.X = aPaintBox.drawPosition.X + offset.X;
        aPaintBox.drawPosition.Y = aPaintBox.drawPosition.Y + offset.Y;
        // 3. draw with new scale and position if position changed 
        aPaintBox.bitmap.Canvas.Brush.Color = delphi_compatability.clWhite;
        aPaintBox.bitmap.Canvas.FillRect(Rect(0, 0, aPaintBox.Width, aPaintBox.Height));
        this.drawTdoOnTdoPaintBox(aPaintBox, UNRESOLVED.kDontDrawYet);
        this.drawPaintBoxBitmapOnCanvas(aPaintBox);
    }
    
    // ------------------------------------------------------------------------ *toolbar 
    public void scrollCursorModeClick(TObject Sender) {
        this.cursorMode = kCursorModeScroll;
        if ((this.editPaintBox != null) && (this.viewPaintBoxOne != null) && (this.viewPaintBoxTwo != null)) {
            this.editPaintBox.Cursor = ucursor.crScroll;
            this.viewPaintBoxOne.Cursor = ucursor.crScroll;
            this.viewPaintBoxTwo.Cursor = ucursor.crScroll;
        }
    }
    
    public void magnifyCursorModeClick(TObject Sender) {
        this.cursorMode = kCursorModeMagnify;
        this.editPaintBox.Cursor = ucursor.crMagPlus;
        this.viewPaintBoxOne.Cursor = ucursor.crMagPlus;
        this.viewPaintBoxTwo.Cursor = ucursor.crMagPlus;
    }
    
    public void rotateCursorModeClick(TObject Sender) {
        this.cursorMode = kCursorModeRotate;
        //can't rotate edit picture
        this.editPaintBox.Cursor = delphi_compatability.crDefault;
        this.viewPaintBoxOne.Cursor = ucursor.crRotate;
        this.viewPaintBoxTwo.Cursor = ucursor.crRotate;
    }
    
    public void addTrianglePointsCursorModeClick(TObject Sender) {
        this.cursorMode = kCursorModeAddTriangles;
        this.editPaintBox.Cursor = ucursor.crAddTriangle;
        this.viewPaintBoxOne.Cursor = delphi_compatability.crDefault;
        this.viewPaintBoxTwo.Cursor = delphi_compatability.crDefault;
    }
    
    public void removeTriangleCursorModeClick(TObject Sender) {
        this.cursorMode = kCursorModeDeleteTriangles;
        this.editPaintBox.Cursor = ucursor.crDeleteTriangle;
        this.viewPaintBoxOne.Cursor = delphi_compatability.crDefault;
        this.viewPaintBoxTwo.Cursor = delphi_compatability.crDefault;
    }
    
    public void dragCursorModeClick(TObject Sender) {
        this.cursorMode = kCursorModeDragPoints;
        this.editPaintBox.Cursor = ucursor.crDragPoint;
        this.viewPaintBoxOne.Cursor = delphi_compatability.crDefault;
        this.viewPaintBoxTwo.Cursor = delphi_compatability.crDefault;
    }
    
    public void flipTriangleCursorModeClick(TObject Sender) {
        this.cursorMode = kCursorModeFlipTriangles;
        this.editPaintBox.Cursor = ucursor.crFlipTriangle;
        this.viewPaintBoxOne.Cursor = delphi_compatability.crDefault;
        this.viewPaintBoxTwo.Cursor = delphi_compatability.crDefault;
    }
    
    public void FormKeyDown(TObject Sender, byte Key, TShiftState Shift) {
        if (Key == delphi_compatability.VK_SHIFT) {
            if (this.cursorMode == kCursorModeMagnify) {
                this.editPaintBox.Cursor = ucursor.crMagMinus;
                this.viewPaintBoxOne.Cursor = ucursor.crMagMinus;
                this.viewPaintBoxTwo.Cursor = ucursor.crMagMinus;
            }
        }
        return Key;
    }
    
    public void FormKeyUp(TObject Sender, byte Key, TShiftState Shift) {
        if (Key == delphi_compatability.VK_SHIFT) {
            if (this.cursorMode == kCursorModeMagnify) {
                this.editPaintBox.Cursor = ucursor.crMagPlus;
                this.viewPaintBoxOne.Cursor = ucursor.crMagPlus;
                this.viewPaintBoxTwo.Cursor = ucursor.crMagPlus;
            }
        }
        return Key;
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
    public void magnifyPlusClick(TObject Sender) {
        if (this.editPaintBox != null) {
            this.editPaintBox.magnifyOrReduce(this.editPaintBox.scale * 1.5, this.editPaintBox.drawPosition);
        }
        if (this.viewPaintBoxOne != null) {
            this.viewPaintBoxOne.magnifyOrReduce(this.viewPaintBoxOne.scale * 1.5, this.viewPaintBoxOne.drawPosition);
        }
        if (this.viewPaintBoxTwo != null) {
            this.viewPaintBoxTwo.magnifyOrReduce(this.viewPaintBoxTwo.scale * 1.5, this.viewPaintBoxTwo.drawPosition);
        }
    }
    
    public void magnifyMinusClick(TObject Sender) {
        if (this.editPaintBox != null) {
            this.editPaintBox.magnifyOrReduce(this.editPaintBox.scale * 0.75, this.editPaintBox.drawPosition);
        }
        if (this.viewPaintBoxOne != null) {
            this.viewPaintBoxOne.magnifyOrReduce(this.viewPaintBoxOne.scale * 0.75, this.viewPaintBoxOne.drawPosition);
        }
        if (this.viewPaintBoxTwo != null) {
            this.viewPaintBoxTwo.magnifyOrReduce(this.viewPaintBoxTwo.scale * 0.75, this.viewPaintBoxTwo.drawPosition);
        }
    }
    
    public void centerDrawingClick(TObject Sender) {
        if (this.editPaintBox != null) {
            this.centerDrawingInPaintBox(this.editPaintBox);
        }
        if (this.viewPaintBoxOne != null) {
            this.centerDrawingInPaintBox(this.viewPaintBoxOne);
        }
        if (this.viewPaintBoxTwo != null) {
            this.centerDrawingInPaintBox(this.viewPaintBoxTwo);
        }
    }
    
    public void resetRotationsClick(TObject Sender) {
        if (this.editPaintBox != null) {
            this.editPaintBox.resetRotations();
        }
        if (this.viewPaintBoxOne != null) {
            this.viewPaintBoxOne.resetRotations();
        }
        if (this.viewPaintBoxTwo != null) {
            this.viewPaintBoxTwo.resetRotations();
        }
    }
    
    public void mirrorTdoClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = PdMirrorTdoCommand().createWithTdo(this.tdo);
        this.doCommand(newCommand);
    }
    
    public void reverseZValuesClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = PdReverseZValuesTdoCommand().createWithTdo(this.tdo);
        this.doCommand(newCommand);
    }
    
    // --------------------------------------------------------------------------------------- *resizing and splitting 
    public void FormResize(TObject Sender) {
        short newTop = 0;
        short newLeft = 0;
        short widthBeforeButtons = 0;
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.tdo == null) {
            return;
        }
        if (this.WindowState == delphi_compatability.TWindowState.wsMinimized) {
            return;
        }
        this.verticalSplitter.Visible = false;
        this.horizontalSplitter.Visible = false;
        widthBeforeButtons = UNRESOLVED.intMax(0, this.ClientWidth - this.ok.Width - kBetweenGap * 2);
        // pictures panel 
        this.picturesPanel.SetBounds(0, this.toolbarPanel.Height, widthBeforeButtons, UNRESOLVED.intMax(0, this.ClientHeight - this.optionsPanel.Height - this.toolbarPanel.Height - 4));
        if (this.lastPicturesPanelWidth != 0) {
            // vertical splitter 
            newLeft = intround(1.0 * this.verticalSplitter.Left * this.picturesPanel.Width / this.lastPicturesPanelWidth);
        } else {
            newLeft = this.picturesPanel.Width / 2;
        }
        if (newLeft >= this.picturesPanel.Width) {
            newLeft = this.picturesPanel.Width - 1;
        }
        if (newLeft < 0) {
            newLeft = 0;
        }
        this.verticalSplitter.SetBounds(newLeft, 0, this.verticalSplitter.Width, this.picturesPanel.Height);
        if (this.lastPicturesPanelHeight != 0) {
            // horizontal splitter 
            newTop = intround(1.0 * this.horizontalSplitter.Top * this.picturesPanel.Height / this.lastPicturesPanelHeight);
        } else {
            newTop = this.picturesPanel.Height / 2;
        }
        if (newTop >= this.picturesPanel.Height) {
            newTop = this.picturesPanel.Height - 1;
        }
        if (newTop < 0) {
            newTop = 0;
        }
        this.horizontalSplitter.SetBounds(this.verticalSplitter.Left + this.verticalSplitter.Width, newTop, UNRESOLVED.intMax(0, this.picturesPanel.Width - this.verticalSplitter.Left - this.verticalSplitter.Width), this.horizontalSplitter.Height);
        this.internalChange = true;
        this.resizeImagesToVerticalSplitter();
        this.resizeImagesToHorizontalSplitter();
        this.internalChange = false;
        this.setInitialDrawPositionsIfNotSet();
        // rest of window 
        this.toolbarPanel.SetBounds(0, 0, this.picturesPanel.Width, this.toolbarPanel.Height);
        this.optionsPanel.SetBounds(0, this.picturesPanel.Top + this.picturesPanel.Height + 4, this.picturesPanel.Width, this.optionsPanel.Height);
        this.ok.Left = this.ClientWidth - this.ok.Width - kBetweenGap;
        this.cancel.Left = this.ok.Left;
        this.undoLast.Left = this.ok.Left;
        this.redoLast.Left = this.ok.Left;
        this.renameTdo.Left = this.ok.Left;
        this.clearTdo.Left = this.ok.Left;
        this.writeToDXF.Left = this.ok.Left;
        this.ReadFromDXF.Left = this.ok.Left;
        this.writeToPOV.Left = this.ok.Left;
        this.helpButton.Left = this.ok.Left;
        this.lastPicturesPanelWidth = this.picturesPanel.Width;
        this.lastPicturesPanelHeight = this.picturesPanel.Height;
        this.verticalSplitter.Visible = true;
        this.horizontalSplitter.Visible = true;
    }
    
    public void resizeImagesToVerticalSplitter() {
        short newLeft = 0;
        
        if (this.editPaintBox != null) {
            this.editPaintBox.SetBounds(0, 0, this.verticalSplitter.Left, this.picturesPanel.Height);
        }
        newLeft = this.verticalSplitter.Left + this.verticalSplitter.Width;
        this.horizontalSplitter.SetBounds(newLeft, this.horizontalSplitter.Top, UNRESOLVED.intMax(0, this.picturesPanel.Width - newLeft), this.horizontalSplitter.Height);
        if (this.viewPaintBoxOne != null) {
            this.viewPaintBoxOne.SetBounds(newLeft, this.viewPaintBoxOne.Top, UNRESOLVED.intMax(0, this.picturesPanel.Width - newLeft), this.viewPaintBoxOne.Height);
        }
        if (this.viewPaintBoxTwo != null) {
            this.viewPaintBoxTwo.SetBounds(newLeft, this.viewPaintBoxTwo.Top, UNRESOLVED.intMax(0, this.picturesPanel.Width - newLeft), this.viewPaintBoxTwo.Height);
        }
        if (!this.internalChange) {
            this.updateForChangeToTdo();
        }
    }
    
    public void resizeImagesToHorizontalSplitter() {
        short newTop = 0;
        
        if (this.viewPaintBoxOne != null) {
            this.viewPaintBoxOne.SetBounds(this.viewPaintBoxOne.Left, 0, this.viewPaintBoxOne.Width, this.horizontalSplitter.Top);
        }
        newTop = this.horizontalSplitter.Top + this.horizontalSplitter.Height;
        if (this.viewPaintBoxTwo != null) {
            this.viewPaintBoxTwo.SetBounds(this.viewPaintBoxTwo.Left, newTop, this.viewPaintBoxTwo.Width, UNRESOLVED.intMax(0, this.picturesPanel.Height - newTop));
        }
        if (!this.internalChange) {
            this.updateForChangeToTdo();
        }
    }
    
    public void setInitialDrawPositionsIfNotSet() {
        if (this.editPaintBox != null) {
            if ((this.editPaintBox.drawPosition.X == 0) && (this.editPaintBox.drawPosition.Y == 0)) {
                this.editPaintBox.drawPosition = Point(this.editPaintBox.Width / 2, this.editPaintBox.Height - 10);
                this.editPaintBox.Paint();
            }
        }
        if (this.viewPaintBoxOne != null) {
            if ((this.viewPaintBoxOne.drawPosition.X == 0) && (this.viewPaintBoxOne.drawPosition.Y == 0)) {
                this.viewPaintBoxOne.drawPosition = Point(this.viewPaintBoxOne.Width / 2, this.viewPaintBoxOne.Height - 10);
                this.viewPaintBoxOne.Paint();
            }
        }
        if (this.viewPaintBoxTwo != null) {
            if ((this.viewPaintBoxTwo.drawPosition.X == 0) && (this.viewPaintBoxTwo.drawPosition.Y == 0)) {
                this.viewPaintBoxTwo.drawPosition = Point(this.viewPaintBoxTwo.Width / 2, this.viewPaintBoxTwo.Height - 10);
                this.viewPaintBoxTwo.Paint();
            }
        }
    }
    
    public void verticalSplitterMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.verticalSplitterDragging = true;
        this.verticalSplitterStartPos = X;
        this.verticalSplitterLastDrawPos = -1;
        this.verticalSplitterNeedToRedraw = true;
    }
    
    public void verticalSplitterMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        if (this.verticalSplitterDragging && (this.verticalSplitter.Left + X >= kSplitterDragToLeftMinPixels) && (this.verticalSplitter.Left + X < this.picturesPanel.Width - kSplitterDragToRightMinPixels)) {
            this.undrawVerticalSplitterLine();
            this.verticalSplitterLastDrawPos = this.drawVerticalSplitterLine(X);
        }
    }
    
    public void verticalSplitterMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        if (this.verticalSplitterDragging) {
            this.undrawVerticalSplitterLine();
            this.verticalSplitter.Left = this.verticalSplitter.Left - (this.verticalSplitterStartPos - X);
            if (this.verticalSplitter.Left < kSplitterDragToLeftMinPixels) {
                this.verticalSplitter.Left = kSplitterDragToLeftMinPixels;
            }
            if (this.verticalSplitter.Left > this.picturesPanel.Width - kSplitterDragToRightMinPixels) {
                this.verticalSplitter.Left = this.picturesPanel.Width - kSplitterDragToRightMinPixels;
            }
            this.resizeImagesToVerticalSplitter();
            this.verticalSplitterDragging = false;
        }
    }
    
    public int drawVerticalSplitterLine(int pos) {
        result = 0;
        HDC theDC = new HDC();
        
        theDC = UNRESOLVED.getDC(0);
        result = this.ClientOrigin.X + this.verticalSplitter.Left + pos + 2;
        UNRESOLVED.patBlt(theDC, result, this.ClientOrigin.Y + this.picturesPanel.Top + this.verticalSplitter.Top, 1, this.verticalSplitter.Height, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.verticalSplitterNeedToRedraw = true;
        return result;
    }
    
    public void undrawVerticalSplitterLine() {
        HDC theDC = new HDC();
        
        if (!this.verticalSplitterNeedToRedraw) {
            return;
        }
        theDC = UNRESOLVED.getDC(0);
        UNRESOLVED.patBlt(theDC, this.verticalSplitterLastDrawPos, this.ClientOrigin.Y + this.picturesPanel.Top + this.verticalSplitter.Top, 1, this.verticalSplitter.Height, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.verticalSplitterNeedToRedraw = false;
    }
    
    public void horizontalSplitterMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.horizontalSplitterDragging = true;
        this.horizontalSplitterStartPos = Y;
        this.horizontalSplitterLastDrawPos = -1;
        this.horizontalSplitterNeedToRedraw = true;
    }
    
    public void horizontalSplitterMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        if (this.horizontalSplitterDragging && (this.horizontalSplitter.Top + Y >= kSplitterDragToTopMinPixels) && (this.horizontalSplitter.Top + Y < this.picturesPanel.Height - kSplitterDragToBottomMinPixels)) {
            this.undrawHorizontalSplitterLine();
            this.horizontalSplitterLastDrawPos = this.drawHorizontalSplitterLine(Y);
        }
    }
    
    public void horizontalSplitterMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        if (this.horizontalSplitterDragging) {
            this.undrawHorizontalSplitterLine();
            this.horizontalSplitter.Top = this.horizontalSplitter.Top - (this.horizontalSplitterStartPos - Y);
            if (this.horizontalSplitter.Top < kSplitterDragToTopMinPixels) {
                this.horizontalSplitter.Top = kSplitterDragToTopMinPixels;
            }
            if (this.horizontalSplitter.Top > this.picturesPanel.Height - kSplitterDragToBottomMinPixels) {
                this.horizontalSplitter.Top = this.picturesPanel.Height - kSplitterDragToBottomMinPixels;
            }
            this.resizeImagesToHorizontalSplitter();
            this.horizontalSplitterDragging = false;
        }
    }
    
    // splitting 
    public int drawHorizontalSplitterLine(int pos) {
        result = 0;
        HDC theDC = new HDC();
        
        theDC = UNRESOLVED.getDC(0);
        result = this.ClientOrigin.Y + this.horizontalSplitter.Top + pos + 2;
        UNRESOLVED.patBlt(theDC, this.ClientOrigin.X + this.horizontalSplitter.Left, result, this.horizontalSplitter.Width, 1, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.horizontalSplitterNeedToRedraw = true;
        return result;
    }
    
    public void undrawHorizontalSplitterLine() {
        HDC theDC = new HDC();
        
        if (!this.horizontalSplitterNeedToRedraw) {
            return;
        }
        theDC = UNRESOLVED.getDC(0);
        UNRESOLVED.patBlt(theDC, this.ClientOrigin.X + this.horizontalSplitter.Left, this.horizontalSplitterLastDrawPos, this.horizontalSplitter.Width, 1, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.horizontalSplitterNeedToRedraw = false;
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 456;
        UNRESOLVED.ptMinTrackSize.y = 260;
    }
    
    public void fillTrianglesClick(TObject Sender) {
        if (!this.fillTriangles.Checked) {
            this.drawLines.Checked = true;
            this.drawLines.Enabled = false;
        } else {
            this.drawLines.Enabled = true;
        }
        if (this.internalChange) {
            return;
        }
        this.updateForChangeToTdo();
    }
    
    public void mirrorHalfClick(TObject Sender) {
        this.updateForChangeToTdo();
    }
    
    public void drawLinesClick(TObject Sender) {
        if (this.internalChange) {
            return;
        }
        this.updateForChangeToTdo();
    }
    
    public void plantPartsChange(TObject Sender) {
        if (this.internalChange) {
            return;
        }
        this.updateForChangeToTdo();
    }
    
    public void circlePointSizeChange(TObject Sender) {
        if (this.internalChange) {
            return;
        }
        this.pointRadius = this.circlePointSize.Value / 2;
        this.updateForChangeToTdo();
    }
    
    public void connectionPointChange(TObject Sender) {
        TPoint oldPoint = new TPoint();
        TPoint newPoint = new TPoint();
        
        if (this.internalChange) {
            return;
        }
        if (this.connectionPoint.Value - 1 != this.tdo.originPointIndex) {
            if ((this.tdo.originPointIndex >= 0) && (this.tdo.originPointIndex <= this.numEditPoints - 1)) {
                // adjust drawing point so 3D object does not move
                oldPoint = this.editPoints[this.tdo.originPointIndex];
            } else {
                oldPoint = Point(0, 0);
            }
            if ((this.connectionPoint.Value - 1 >= 0) && (this.connectionPoint.Value - 1 <= this.numEditPoints - 1)) {
                newPoint = this.editPoints[this.connectionPoint.Value - 1];
            } else {
                newPoint = Point(0, 0);
            }
            this.editPaintBox.drawPosition.X = this.editPaintBox.drawPosition.X + (newPoint.X - oldPoint.X);
            this.editPaintBox.drawPosition.Y = this.editPaintBox.drawPosition.Y + (newPoint.Y - oldPoint.Y);
        }
        this.tdo.setOriginPointIndex(this.connectionPoint.Value - 1);
        if (this.editPaintBox != null) {
            this.editPaintBox.Paint();
        }
        this.updateForChangeToConnectionPointIndex();
    }
    
    // commands 
    // ------------------------------------------------------------------------ *commands 
    public void doCommand(PdCommand command) {
        this.commandList.doCommand(command);
        this.updateButtonsForUndoRedo();
        this.updateForChangeToTdo();
    }
    
}
class PdTdoCommand extends PdCommand {
    public KfObject3D tdo;
    public boolean lastCommandWasApply;
    public boolean lastCommandWasUndoApply;
    
    // ------------------------------------------------------------------------ PdTdoCommand 
    public void createWithTdo(KfObject3D aTdo) {
        super.create();
        UNRESOLVED.commandChangesPlantFile = false;
        this.tdo = aTdo;
        this.lastCommandWasApply = TdoEditorForm.lastCommandWasApply;
        this.lastCommandWasUndoApply = TdoEditorForm.lastCommandWasUndoApply;
    }
    
    public void doCommand() {
        super.doCommand();
        TdoEditorForm.lastCommandWasApply = false;
        TdoEditorForm.lastCommandWasUndoApply = false;
    }
    
    public void undoCommand() {
        super.undoCommand();
        TdoEditorForm.lastCommandWasApply = this.lastCommandWasApply;
        TdoEditorForm.lastCommandWasUndoApply = this.lastCommandWasUndoApply;
    }
    
}
class PdDragTdoPointCommand extends PdTdoCommand {
    public float scale;
    public short movingPointIndex;
    public TPoint dragStartPoint;
    public KfPoint3D oldPoint3D;
    public KfPoint3D newPoint3D;
    
    // -------------------------------------------------------------------- PdDragTdoPointCommand 
    public void createWithTdoAndScale(KfObject3D aTdo, float aScale) {
        super.createWithTdo(aTdo);
        this.scale = aScale;
    }
    
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        result = this;
        if (aTrackPhase == UNRESOLVED.trackPress) {
            this.movingPointIndex = TdoEditorForm.pointIndexAtMouse(nextPoint.X, nextPoint.Y);
            TdoEditorForm.draggingPoint = true;
            TdoEditorForm.pointIndexBeingDragged = this.movingPointIndex;
            if (this.movingPointIndex < 0) {
                result = null;
                this.free;
            } else {
                this.dragStartPoint = nextPoint;
                this.oldPoint3D = this.tdo.points[this.movingPointIndex];
                this.newPoint3D = this.oldPoint3D;
            }
        } else if (aTrackPhase == UNRESOLVED.trackMove) {
            if (rightButtonDown) {
                this.newPoint3D.z = this.oldPoint3D.z - (nextPoint.Y - this.dragStartPoint.Y) / this.scale;
            } else {
                this.newPoint3D.x = this.oldPoint3D.x + (nextPoint.X - this.dragStartPoint.X) / this.scale;
                this.newPoint3D.y = this.oldPoint3D.y + (nextPoint.Y - this.dragStartPoint.Y) / this.scale;
            }
            this.tdo.points[this.movingPointIndex] = this.newPoint3D;
        } else if (aTrackPhase == UNRESOLVED.trackRelease) {
            if (!mouseDidMove) {
                result = null;
                this.free;
            }
        }
        return result;
    }
    
    public void undoCommand() {
        super.undoCommand();
        this.tdo.points[this.movingPointIndex] = this.oldPoint3D;
    }
    
    public void redoCommand() {
        super.doCommand();
        this.tdo.points[this.movingPointIndex] = this.newPoint3D;
    }
    
    public String description() {
        result = "";
        result = "drag";
        return result;
    }
    
}
class PdRenameTdoCommand extends PdTdoCommand {
    public String oldName;
    public String newName;
    
    // --------------------------------------------------------------------------- PdRenameTdoCommand 
    public void createWithTdoAndNewName(KfObject3D aTdo, String aName) {
        super.createWithTdo(aTdo);
        this.oldName = this.tdo.getName;
        this.newName = aName;
    }
    
    public void doCommand() {
        this.tdo.setName(this.newName);
        TdoEditorForm.updateCaptionForNewTdoName();
        super.doCommand();
    }
    
    public void undoCommand() {
        this.tdo.setName(this.oldName);
        TdoEditorForm.updateCaptionForNewTdoName();
        super.undoCommand();
    }
    
    public String description() {
        result = "";
        result = "rename";
        return result;
    }
    
}
class PdReplaceTdoCommand extends PdTdoCommand {
    public KfObject3D oldTdo;
    public KfObject3D newTdo;
    
    // ------------------------------------------------------------------------ PdReplaceTdoCommand 
    public void createWithTdo(KfObject3D aTdo) {
        super.createWithTdo(aTdo);
        this.oldTdo = UNRESOLVED.KfObject3D.create;
        this.newTdo = UNRESOLVED.KfObject3D.create;
        this.oldTdo.copyFrom(this.tdo);
        this.newTdo.copyFrom(this.tdo);
    }
    
    public void destroy() {
        this.oldTdo.free;
        this.oldTdo = null;
        this.newTdo.free;
        this.newTdo = null;
        super.destroy();
    }
    
    public void undoCommand() {
        super.undoCommand();
        this.tdo.copyFrom(this.oldTdo);
        // v1.6
        TdoEditorForm.updateForChangeToTdo();
    }
    
    public void redoCommand() {
        super.doCommand();
        this.tdo.copyFrom(this.newTdo);
        // v1.6
        TdoEditorForm.updateForChangeToTdo();
    }
    
}
class PdAddTdoTriangleCommand extends PdReplaceTdoCommand {
    public  newPoints;
    public  newPointIndexes;
    public KfIndexTriangle newTriangle;
    
    // -------------------------------------------------------------------- PdAddTdoTriangleCommand 
    public void createWithTdoAndNewPoints(KfObject3D aTdo,  aNewPointIndexes,  aNewPoints) {
        short i = 0;
        
        super.createWithTdo(aTdo);
        for (i = 0; i <= 2; i++) {
            this.newPointIndexes[i] = aNewPointIndexes[i];
            this.newPoints[i] = aNewPoints[i];
        }
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        for (i = 0; i <= 2; i++) {
            if (this.newPointIndexes[i] < 0) {
                this.newPointIndexes[i] = this.newTdo.addPoint(this.newPoints[i]) - 1;
            }
        }
        this.newTriangle = UNRESOLVED.KfIndexTriangle.createABC(this.newPointIndexes[0] + 1, this.newPointIndexes[1] + 1, this.newPointIndexes[2] + 1);
        //newTdo will free newTriangle
        this.newTdo.triangles.add(this.newTriangle);
        this.tdo.copyFrom(this.newTdo);
        TdoEditorForm.updateForChangeToNumberOfPoints();
    }
    
    public void undoCommand() {
        super.undoCommand();
        TdoEditorForm.updateForChangeToNumberOfPoints();
    }
    
    public void redoCommand() {
        super.redoCommand();
        TdoEditorForm.updateForChangeToNumberOfPoints();
    }
    
    public String description() {
        result = "";
        result = "add";
        return result;
    }
    
}
class PdRemoveTdoTriangleCommand extends PdReplaceTdoCommand {
    public KfIndexTriangle triangle;
    
    // ----------------------------------------------------------------------- PdRemoveTdoTriangleCommand 
    public void doCommand() {
        super.doCommand();
        TdoEditorForm.updateForChangeToNumberOfPoints();
    }
    
    public void undoCommand() {
        super.undoCommand();
        TdoEditorForm.updateForChangeToNumberOfPoints();
    }
    
    public void redoCommand() {
        super.redoCommand();
        TdoEditorForm.updateForChangeToNumberOfPoints();
    }
    
    public void destroy() {
        if (this.done) {
            // since triangle was removed from, not added to, newTdo, we must free it ourselves 
            this.triangle.free;
        }
        this.triangle = null;
        super.destroy();
    }
    
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        KfIndexTriangle triangleInTdo = new KfIndexTriangle();
        short index = 0;
        
        result = this;
        if (aTrackPhase == UNRESOLVED.trackPress) {
            pass
        } else if (aTrackPhase == UNRESOLVED.trackMove) {
            pass
        } else if (aTrackPhase == UNRESOLVED.trackRelease) {
            triangleInTdo = TdoEditorForm.triangleAtMouse(nextPoint.X, nextPoint.Y);
            index = this.tdo.triangles.indexOf(triangleInTdo);
            if ((index >= 0) && (index <= this.newTdo.triangles.count - 1)) {
                this.triangle = UNRESOLVED.KfIndexTriangle(this.newTdo.triangles.items[index]);
                //we will free triangle
                this.newTdo.removeTriangle(this.triangle);
                this.tdo.copyFrom(this.newTdo);
            } else {
                result = null;
                this.free;
            }
        }
        return result;
    }
    
    public String description() {
        result = "";
        result = "delete";
        return result;
    }
    
}
class PdMirrorTdoCommand extends PdReplaceTdoCommand {
    
    // -------------------------------------------------------------------- PdMirrorTdoCommand 
    public void doCommand() {
        this.newTdo.makeMirrorTriangles;
        this.tdo.copyFrom(this.newTdo);
        super.doCommand();
    }
    
    public String description() {
        result = "";
        result = "mirror";
        return result;
    }
    
}
class PdReverseZValuesTdoCommand extends PdReplaceTdoCommand {
    
    // -------------------------------------------------------------------- PdReverseZValuesTdoCommand 
    public void doCommand() {
        this.newTdo.reverseZValues;
        this.tdo.copyFrom(this.newTdo);
        super.doCommand();
    }
    
    public String description() {
        result = "";
        result = "reverse";
        return result;
    }
    
}
class PdClearAllPointsCommand extends PdReplaceTdoCommand {
    
    // -------------------------------------------------------------------- PdClearAllPointsCommand 
    public void doCommand() {
        this.newTdo.clearPoints;
        this.tdo.copyFrom(this.newTdo);
        super.doCommand();
    }
    
    public String description() {
        result = "";
        result = "clear";
        return result;
    }
    
}
class PdLoadTdoFromDXFCommand extends PdReplaceTdoCommand {
    
    // -------------------------------------------------------------------- PdLoadTdoFromDXFCommand 
    public void createWithOldAndNewTdo(KfObject3D anOldTdo, KfObject3D aNewTdo) {
        super.createWithTdo(anOldTdo);
        this.oldTdo = UNRESOLVED.KfObject3D.create;
        this.newTdo = UNRESOLVED.KfObject3D.create;
        this.oldTdo.copyFrom(anOldTdo);
        this.newTdo.copyFrom(aNewTdo);
    }
    
    public void doCommand() {
        this.tdo.copyFrom(this.newTdo);
        TdoEditorForm.updateCaptionForNewTdoName();
        //v1.6b1
        TdoEditorForm.centerDrawingClick(TdoEditorForm);
        super.doCommand();
    }
    
    public void undoCommand() {
        super.undoCommand();
        TdoEditorForm.updateCaptionForNewTdoName();
        //v1.6b1
        TdoEditorForm.centerDrawingClick(TdoEditorForm);
    }
    
    public void redoCommand() {
        super.redoCommand();
        TdoEditorForm.updateCaptionForNewTdoName();
        //v1.6b1
        TdoEditorForm.centerDrawingClick(TdoEditorForm);
    }
    
    public String description() {
        result = "";
        result = "DXF";
        return result;
    }
    
}
