unit Utdoedit;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, StdCtrls, Buttons, ExtCtrls, Spin,
  utdo, ucommand, uparams, updform, uturtle, ToolWin, ComCtrls;

type
  PdTdoPaintBox = class(TPaintBox)
    public
    bitmap: TBitmap;
    canRotate, draggingIn: boolean;
    scale, xRotation, yRotation, zRotation: single;
    drawPosition, startDragPosition: TPoint;
    tdoBoundsRect: TRect;
    constructor create(anOwner: TComponent); override;
    destructor destroy; override;
    procedure magnifyOrReduce(newScale: single; clickPoint: TPoint);
    procedure centerTdo;
    procedure resetRotations;
    end;

  TTdoEditorForm = class(PdForm)
    ok: TButton;
    cancel: TButton;
    undoLast: TButton;
    redoLast: TButton;
    toolbarPanel: TPanel;
    dragCursorMode: TSpeedButton;
    magnifyCursorMode: TSpeedButton;
    scrollCursorMode: TSpeedButton;
    addTrianglePointsCursorMode: TSpeedButton;
    removeTriangleCursorMode: TSpeedButton;
    flipTriangleCursorMode: TSpeedButton;
    rotateCursorMode: TSpeedButton;
    optionsPanel: TPanel;
    fillTriangles: TCheckBox;
    plantParts: TSpinEdit;
    drawAsLabel: TLabel;
    picturesPanel: TPanel;
    verticalSplitter: TPanel;
    horizontalSplitter: TPanel;
    drawLines: TCheckBox;
    writeToDXF: TButton;
    renameTdo: TButton;
    Label1: TLabel;
    circlePointSize: TSpinEdit;
    helpButton: TSpeedButton;
    mirrorTdo: TSpeedButton;
    reverseZValues: TSpeedButton;
    centerDrawing: TSpeedButton;
    resetRotations: TSpeedButton;
    writeToPOV: TButton;
    mirrorHalf: TCheckBox;
    ReadFromDXF: TButton;
    connectionPointLabel: TLabel;
    connectionPoint: TSpinEdit;
    clearTdo: TButton;
    procedure verticalSplitterMouseDown(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure verticalSplitterMouseMove(Sender: TObject;
      Shift: TShiftState; X, Y: Integer);
    procedure verticalSplitterMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure horizontalSplitterMouseDown(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure horizontalSplitterMouseMove(Sender: TObject;
      Shift: TShiftState; X, Y: Integer);
    procedure horizontalSplitterMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure FormResize(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure okClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure fillTrianglesClick(Sender: TObject);
    procedure drawLinesClick(Sender: TObject);
    procedure scrollCursorModeClick(Sender: TObject);
    procedure magnifyCursorModeClick(Sender: TObject);
    procedure rotateCursorModeClick(Sender: TObject);
    procedure addTrianglePointsCursorModeClick(Sender: TObject);
    procedure removeTriangleCursorModeClick(Sender: TObject);
    procedure dragCursorModeClick(Sender: TObject);
    procedure flipTriangleCursorModeClick(Sender: TObject);
    procedure undoLastClick(Sender: TObject);
    procedure redoLastClick(Sender: TObject);
    procedure FormKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure FormKeyUp(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure magnifyPlusClick(Sender: TObject);
    procedure magnifyMinusClick(Sender: TObject);
    procedure centerDrawingClick(Sender: TObject);
    procedure resetRotationsClick(Sender: TObject);
    procedure applyClick(Sender: TObject);
    procedure plantPartsChange(Sender: TObject);
    procedure writeToDXFClick(Sender: TObject);
    procedure mirrorTdoClick(Sender: TObject);
    procedure renameTdoClick(Sender: TObject);
    procedure reverseZValuesClick(Sender: TObject);
    procedure circlePointSizeChange(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure helpButtonClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure writeToPOVClick(Sender: TObject);
    procedure mirrorHalfClick(Sender: TObject);
    procedure ReadFromDXFClick(Sender: TObject);
    procedure connectionPointChange(Sender: TObject);
    procedure clearTdoClick(Sender: TObject);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
  public
    { Public declarations }
    tdo, originalTdo: KfObject3d;
    param: PdParameter;
    editPaintBox: PdTdoPaintBox;
    viewPaintBoxOne: PdTdoPaintBox;
    viewPaintBoxTwo: PdTdoPaintBox;
    paintBoxClickedIn: PdTdoPaintBox;
    commandList: PdCommandList;
    internalChange, actionInProgress, scrolling, rotating: boolean;
    startDragPoint, scrollStartPosition: TPoint;
    draggingPoint: boolean;
    pointIndexBeingDragged: smallint;
    cursorMode, rotateDirection, pointRadius: smallint;
    rotateStartAngle: single;
    lastCommandWasApply, lastCommandWasUndoApply: boolean;
    editPoints: array[0..kMaximumRecordedPoints] of TPoint;
    numEditPoints, numNewPoints: smallint;
    newPointIndexes: array[0..2] of smallint;
    newPoints: array[0..2] of KfPoint3D;
    { resizing and splitting }
    horizontalSplitterDragging, verticalSplitterDragging: boolean;
    horizontalSplitterNeedToRedraw, verticalSplitterNeedToRedraw: boolean;
    horizontalSplitterStartPos, verticalSplitterStartPos: integer;
    horizontalSplitterLastDrawPos, verticalSplitterLastDrawPos: integer;
    lastPicturesPanelWidth, lastPicturesPanelHeight: integer;
    { creation/destruction }
    constructor create(AOwner: TComponent); override;
    destructor destroy; override;
    procedure initializeWithTdoAndParameter(aTdo: KfObject3D; aParam: PdParameter);
    procedure initializeWithTdo(aTdo: KfObject3D);
    { updating }
    procedure updateButtonsForUndoRedo;
    procedure updateForChangeToTdo;
    procedure updateForChangeToClickedOnPaintBox;
    procedure updateCaptionForNewTdoName;
    procedure updateForChangeToNumberOfPoints;
    procedure updateForChangeToConnectionPointIndex;
    { drawing }
    procedure editPaintBoxPaint(Sender: TObject);
    procedure viewPaintBoxOnePaint(Sender: TObject);
    procedure viewPaintBoxTwoPaint(Sender: TObject);
    procedure checkImageForBitmapSizeAndFill(aPaintBox: PdTdoPaintBox);
    procedure drawTdoOnTdoPaintBox(aPaintBox: PdTdoPaintBox; immediate: boolean);
    procedure centerDrawingInPaintBox(aPaintBox: PdTdoPaintBox);
    procedure drawPaintBoxBitmapOnCanvas(aPaintBox: PdTdoPaintBox);
    { mouse handling }
    procedure imagesMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure imagesMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
    procedure imagesMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure addTrianglePoints(x, y: smallint);
    procedure lightUpPointAtMouse(x, y: integer; immediate: boolean);
    procedure lightUpTriangleAtMouse(x, y: integer);
    procedure lightUpAddingLineAtMouse(x, y: smallint);
    function pointIndexAtMouse(x, y: integer): smallint;
    function triangleAtMouse(x, y: integer): KfIndexTriangle;
    procedure scrollBy(x, y: integer);
    procedure rotateBy(x, y: integer);
    function makeMouseCommand(var point: TPoint; shift, ctrl: boolean): PdCommand;
    procedure editPaintBoxMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure viewPaintBoxOneMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure viewPaintBoxTwoMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    { commands }
    procedure doCommand(command: PdCommand);
    { splitting }
    function drawHorizontalSplitterLine(pos: integer): integer;
    function drawVerticalSplitterLine(pos: integer): integer;
    procedure undrawHorizontalSplitterLine;
    procedure undrawVerticalSplitterLine;
    procedure resizeImagesToVerticalSplitter;
    procedure resizeImagesToHorizontalSplitter;
    procedure setInitialDrawPositionsIfNotSet;
  end;

PdTdoCommand = class(PdCommand)
  public
  tdo: KfObject3D;
  lastCommandWasApply, lastCommandWasUndoApply: boolean;
  constructor createWithTdo(aTdo: KfObject3D); virtual;
  procedure doCommand; override;
  procedure undoCommand; override;
  end;

PdDragTdoPointCommand = class(PdTdoCommand)
  public
  scale: single;
  movingPointIndex: smallint;
  dragStartPoint: TPoint;
  oldPoint3D, newPoint3D: KfPoint3D;
  constructor createWithTdoAndScale(aTdo: KfObject3D; aScale: single);
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand; override;
  procedure undoCommand; override;
  procedure redoCommand; override;
  function description: string; override;
  end;

PdRenameTdoCommand = class(PdTdoCommand)
  public
  oldName, newName: string;
  constructor createWithTdoAndNewName(aTdo: KfObject3D; aName: string);
  procedure doCommand; override;
  procedure undoCommand; override;
  function description: string; override;
  end;

PdReplaceTdoCommand = class(PdTdoCommand)
  public
  oldTdo, newTdo: KfObject3D;
  constructor createWithTdo(aTdo: KfObject3D); override;
  destructor destroy; override;
  procedure undoCommand; override;
  procedure redoCommand; override;
  end;

PdAddTdoTriangleCommand = class(PdReplaceTdoCommand)
  public
  newPoints: array[0..2] of KfPoint3D;
  newPointIndexes: array[0..2] of smallint;
  newTriangle: KfIndexTriangle;
  constructor createWithTdoAndNewPoints(aTdo: KfObject3D;
      aNewPointIndexes: array of smallint; aNewPoints: array of KfPoint3D);
  procedure doCommand; override;
  procedure undoCommand; override;
  procedure redoCommand; override;
  function description: string; override;
  end;

PdRemoveTdoTriangleCommand = class(PdReplaceTdoCommand)
  public
  triangle: KfIndexTriangle;
  procedure doCommand; override;
  procedure undoCommand; override;
  procedure redoCommand; override;
  destructor destroy; override;
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand; override;
  function description: string; override;
  end;

PdMirrorTdoCommand = class(PdReplaceTdoCommand)
  public
  procedure doCommand; override;
  function description: string; override;
  end;

PdReverseZValuesTdoCommand = class(PdReplaceTdoCommand)
  public
  procedure doCommand; override;
  function description: string; override;
  end;

PdClearAllPointsCommand = class(PdReplaceTdoCommand)
  public
  procedure doCommand; override;
  function description: string; override;
  end;

PdLoadTdoFromDXFCommand = class(PdReplaceTdoCommand)
  public
  constructor createWithOldAndNewTdo(anOldTdo, aNewTdo: KfObject3D);
  procedure doCommand; override;
  procedure undoCommand; override;
  procedure redoCommand; override;
  function description: string; override;
  end;

implementation

{$R *.DFM}

uses udomain, umain, updcom, ucursor, umath, usupport, uwait, ubmpsupport;

const
  kSplitterDragToTopMinPixels = 50; kSplitterDragToBottomMinPixels = 50;
  kSplitterDragToLeftMinPixels = 100; kSplitterDragToRightMinPixels = 50;
  kBetweenGap = 4;
  kDrawAsLeaf = 0; kDrawAsFlower = 1; kDrawAsFruit = 2;
  kCursorModeScroll = 0; kCursorModeMagnify = 1; kCursorModeRotate = 2;
  kCursorModeAddTriangles = 3; kCursorModeDeleteTriangles = 4; kCursorModeDragPoints = 5; kCursorModeFlipTriangles = 6;
  kLineColor = clBlack;
  kLightUpColor = clRed;
  kConnectedPointColor = clBlue;
  kUnconnectedPointColor = clGreen;
  kOriginPointColor = clBlack;

var TdoEditorForm: TTdoEditorForm;

{ --------------------------------------------------------------------------------- PdTdoImage }
constructor PdTdoPaintBox.create(anOwner: TComponent);
  begin
  inherited create(anOwner);
  bitmap := TBitmap.create;
  end;

destructor PdTdoPaintBox.destroy;
  begin
  bitmap.free;
  bitmap := nil;
  inherited destroy;
  end;

procedure PdTdoPaintBox.magnifyOrReduce(newScale: single; clickPoint: TPoint);
  begin
  drawPosition.x := round(clickPoint.x + (drawPosition.x - clickPoint.x) * newScale / scale);
  drawPosition.y := round(clickPoint.y + (drawPosition.y - clickPoint.y) * newScale / scale);
  scale := newScale;
  self.paint;
  end;

procedure PdTdoPaintBox.centerTdo;
  var
    xScale, yScale, newScale: single;
    turtle: KfTurtle;
  begin
  xScale := safedivExcept(0.75 * scale * width, rWidth(tdoBoundsRect), 0.1);
  yScale := safedivExcept(0.75 * scale * height, rHeight(tdoBoundsRect), 0.1);
  newScale := min(xScale, yScale);
  if TdoEditorForm.tdo <> nil then
    begin
    turtle := KfTurtle.defaultStartUsing;
    try
      drawPosition := TdoEditorForm.tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(width, height), newScale);
    finally
      KfTurtle.defaultStopUsing;
    end;
    end
  else
    drawPosition := Point(width div 2, height - 10);
  self.magnifyOrReduce(newScale, drawPosition);
  end;

procedure PdTdoPaintBox.resetRotations;
  begin
  xRotation := 0;
  yRotation := 0;
  zRotation := 0;
  self.paint;
  end;

{ -------------------------------------------------------------------------------------------- *creation/destruction }
constructor TTdoEditorForm.create(AOwner: TComponent);
  begin
  inherited create(AOwner);
  TdoEditorForm := self;
  tdo := KfObject3D.create;
  commandList := PdCommandList.create;
  commandList.setNewUndoLimit(domain.options.undoLimit);
  commandList.setNewObjectUndoLimit(domain.options.undoLimitOfPlants);
  editPaintBox := PdTdoPaintBox.create(self);
  with editPaintBox do
    begin
    parent := picturesPanel;
    onMouseDown := self.editPaintBoxMouseDown;
    onMouseMove := self.imagesMouseMove;
    onMouseUp := self.imagesMouseUp;
    onPaint := self.editPaintBoxPaint;
    scale := 1.5;
    cursor := crScroll;
    end;
  viewPaintBoxOne := PdTdoPaintBox.create(self);
  with viewPaintBoxOne do
    begin
    parent := picturesPanel;
    onMouseDown := self.viewPaintBoxOneMouseDown;
    onMouseMove := self.imagesMouseMove;
    onMouseUp := self.imagesMouseUp;
    onPaint := self.viewPaintBoxOnePaint;
    scale := 0.5;
    cursor := crScroll;
    end;
  viewPaintBoxTwo := PdTdoPaintBox.create(self);
  with viewPaintBoxTwo do
    begin
    parent := picturesPanel;
    onMouseDown := self.viewPaintBoxTwoMouseDown;
    onMouseMove := self.imagesMouseMove;
    onMouseUp := self.imagesMouseUp;
    onPaint := self.viewPaintBoxTwoPaint;
    scale := 0.5;
    cursor := crScroll;
    end;
  self.updateButtonsForUndoRedo;
  end;

procedure TTdoEditorForm.FormCreate(Sender: TObject);
  var tempBoundsRect: TRect;
  begin
  { keep window on screen - left corner of title bar }
  tempBoundsRect := domain.tdoEditorWindowRect;
  with tempBoundsRect do
    if (left <> 0) or (right <> 0) or (top <> 0) or (bottom <> 0) then
      begin
      if left > screen.width - kMinWidthOnScreen then left := screen.width - kMinWidthOnScreen;
      if top > screen.height - kMinHeightOnScreen then top := screen.height - kMinHeightOnScreen;
      self.setBounds(left, top, right, bottom);
      end;
  scrollCursorMode.down := true;
  self.scrollCursorModeClick(self);
  internalChange := true;
  circlePointSize.value := domain.options.circlePointSizeInTdoEditor;
  plantParts.value := domain.options.partsInTdoEditor;
  fillTriangles.checked := domain.options.fillTrianglesInTdoEditor;
  drawLines.checked := domain.options.drawLinesInTdoEditor;
  internalChange := false;
  pointRadius := circlePointSize.value div 2;
  toolbarPanel.bevelOuter := bvNone;
  //optionsPanel.bevelOuter := bvNone;
  end;

procedure TTdoEditorForm.initializeWithTdoAndParameter(aTdo: KfObject3D; aParam: PdParameter);
  begin
  originalTdo := aTdo;
  if originalTdo = nil then
    raise Exception.create('Problem: Nil 3D object in method TTdoEditorForm.initializeWithTdoAndParameter.');
  param := aParam;
  if param = nil then
    raise Exception.create('Problem: Nil parameter in method TTdoEditorForm.initializeWithTdoAndParameter.');
  tdo.copyFrom(originalTdo);
  self.updateCaptionForNewTdoName;
  self.updateForChangeToNumberOfPoints;
  self.centerDrawingClick(self); //v1.6b1
  end;

procedure TTdoEditorForm.initializeWithTdo(aTdo: KfObject3D);
  begin
  originalTdo := aTdo;
  if originalTdo = nil then
    raise Exception.create('Problem: Nil 3D object in method TTdoEditorForm.initializeWithTdo.');
  tdo.copyFrom(originalTdo);
  self.updateCaptionForNewTdoName;
  self.updateForChangeToNumberOfPoints;
  self.centerDrawingClick(self); //v1.6b1
  end;

destructor TTdoEditorForm.destroy;
  begin
  tdo.free;
  tdo := nil;
  commandList.free;
  commandList := nil;
  { don't free paint boxes because we are their owner }
  inherited destroy;
  end;

{ -------------------------------------------------------------------------------- *command list }
procedure TTdoEditorForm.undoLastClick(Sender: TObject);
  begin
  if lastCommandWasApply then
    begin
    MainForm.MenuEditUndoClick(MainForm);
    lastCommandWasUndoApply := true;
    lastCommandWasApply := false;
    self.updateButtonsForUndoRedo;
    end
  else
    begin
    commandList.undoLast;
    self.updateButtonsForUndoRedo;
    self.updateForChangeToTdo;
    end;
  end;

procedure TTdoEditorForm.redoLastClick(Sender: TObject);
  begin
  if lastCommandWasUndoApply then
    begin
    MainForm.MenuEditRedoClick(MainForm);
    lastCommandWasUndoApply := false;
    lastCommandWasApply := true;
    self.updateButtonsForUndoRedo;
    end
  else
    begin
    commandList.redoLast;
    self.updateButtonsForUndoRedo;
    self.updateForChangeToTdo;
    end;
  end;

{ ------------------------------------------------------------------------------- *updating }
procedure TTdoEditorForm.updateButtonsForUndoRedo;
  begin
  if lastCommandWasApply then
    begin
    undoLast.enabled := true;
    undoLast.caption := '&Undo apply';
    end
  else if lastCommandWasUndoApply then
    begin
    redoLast.enabled := true;
    redoLast.caption := '&Redo apply';
    end
  else
    begin
    if commandList.isUndoEnabled then
  	  begin
      undoLast.enabled := true;
      undoLast.caption := '&Undo ' + commandList.undoDescription;
      end
    else
    	begin
      undoLast.enabled := false;
      undoLast.caption := 'Can''t undo';
      end;
    if commandList.isRedoEnabled then
  	  begin
      redoLast.enabled := true;
      redoLast.caption := '&Redo ' + commandList.redoDescription;
      end
    else
  	  begin
      redoLast.enabled := false;
      redoLast.caption := 'Can''t redo';
      end;
    end;
  end;

procedure TTdoEditorForm.updateForChangeToTdo;
  begin
  self.updateButtonsForUndoRedo;
  self.updateForChangeToNumberOfPoints;
  self.updateForChangeToConnectionPointIndex;
  clearTdo.enabled := (tdo <> nil) and (tdo.pointsInUse > 0);
  if (editPaintBox <> nil) and (viewPaintBoxOne <> nil) and (viewPaintBoxTwo <> nil) then
    begin
    editPaintBox.paint;
    viewPaintBoxOne.paint;
    viewPaintBoxTwo.paint;
    end;
  end;

procedure TTdoEditorForm.updateForChangeToClickedOnPaintBox;
  begin
  self.updateButtonsForUndoRedo;
  if paintBoxClickedIn <> nil then
    paintBoxClickedIn.paint;
  end;

procedure TTdoEditorForm.updateCaptionForNewTdoName;
  begin
  self.caption := '3D object editor - ' + tdo.getName;
  self.invalidate;
  end;

procedure TTdoEditorForm.updateForChangeToNumberOfPoints;
  begin
  internalChange := true;
  connectionPoint.value := tdo.originPointIndex + 1;
  connectionPoint.maxValue := tdo.pointsInUse;
  connectionPointLabel.caption := 'Connection point (1-' + intToStr(connectionPoint.maxValue) + ')';
  internalChange := false;
  end;

procedure TTdoEditorForm.updateForChangeToConnectionPointIndex;
  var
    oldPoint, newPoint: TPoint;
  begin
  internalChange := true;
  connectionPoint.value := tdo.originPointIndex + 1;
  internalChange := false;
  (*
  // adjust drawing point so 3D object does not move
  if connectionPoint.value - 1 <> tdo.originPointIndex then
    begin
    if (tdo.originPointIndex >= 0) and (tdo.originPointIndex <= numEditPoints - 1) then
      oldPoint := editPoints[tdo.originPointIndex]
    else
      oldPoint := Point(0, 0);
    if (connectionPoint.value - 1 >= 0) and (connectionPoint.value - 1 <= numEditPoints - 1) then
      newPoint := editPoints[connectionPoint.value - 1]
    else
      newPoint := Point(0, 0);
    editPaintBox.drawPosition.x := editPaintBox.drawPosition.x + (newPoint.x - oldPoint.x);
    editPaintBox.drawPosition.y := editPaintBox.drawPosition.y + (newPoint.y - oldPoint.y);
    end;
  tdo.setOriginPointIndex(connectionPoint.value - 1);
  if editPaintBox <> nil then editPaintBox.paint;
  *)
  end;

{ -------------------------------------------------------------------------------------- *buttons }
procedure TTdoEditorForm.okClick(Sender: TObject);
  begin
  modalResult := mrOk;
  end;

procedure TTdoEditorForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TTdoEditorForm.FormClose(Sender: TObject; var Action: TCloseAction);
  begin
  // save settings to domain even if they clicked cancel or clicked the close box
  domain.tdoEditorWindowRect := rect(left, top, width, height);
  domain.options.circlePointSizeInTdoEditor := circlePointSize.value;
  domain.options.partsInTdoEditor := plantParts.value;
  domain.options.fillTrianglesInTdoEditor := fillTriangles.checked;
  domain.options.drawLinesInTdoEditor := drawLines.checked;
  end;

procedure TTdoEditorForm.applyClick(Sender: TObject);
  begin
  MainForm.doCommand(
    PdChangeTdoValueCommand.createCommandWithListOfPlants(
      MainForm.selectedPlants, tdo, param.fieldNumber, param.regrow));
  lastCommandWasApply := true;
  self.updateButtonsForUndoRedo;
  end;

procedure TTdoEditorForm.renameTdoClick(Sender: TObject);
  var
    newCommand: PdCommand;
    newName: ansistring;
  begin
  newName := tdo.getName;
  if not inputQuery('Enter new name', 'Type a new name for ' + newName + '.', newName) then exit;
  newCommand := PdRenameTdoCommand.createWithTdoAndNewName(self.tdo, newName);
  self.doCommand(newCommand);
  end;

procedure TTdoEditorForm.clearTdoClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdClearAllPointsCommand.createWithTdo(self.tdo);
  self.doCommand(newCommand);
  end;

procedure TTdoEditorForm.writeToDXFClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
    suggestedName: string;
  begin
  suggestedName := 'export.dxf';
  if not getFileSaveInfo(kFileTypeDXF, kAskForFileName, suggestedName, fileInfo) then exit;
  try
    startFileSave(fileInfo);
    tdo.writeToDXFFile(fileInfo.tempFile, kTdoForeColor, kTdoBackColor);
    fileInfo.writingWasSuccessful := true;
  finally
    cleanUpAfterFileSave(fileInfo);
  end;
	end;

procedure TTdoEditorForm.ReadFromDXFClick(Sender: TObject);
   var
    fileNameWithPath: string;
    newTdo: KfObject3D;
    inputFile: TextFile;
    newCommand: PdCommand;
  begin
  newTdo := nil;
  fileNameWithPath := getFileOpenInfo(kFileTypeDXF, 'input.dxf', 'Choose a DXF file');
  if fileNameWithPath = '' then exit;
  try
    startWaitMessage('Reading ' + extractFileName(fileNameWithPath));
    assignFile(inputFile, fileNameWithPath);
    try
      setDecimalSeparator; // v1.5
      reset(inputFile);
      newTdo := KfObject3D.create;
      newTdo.readFromDXFFile(inputFile);
      newTdo.setName(stringUpTo(extractFileName(fileNameWithPath), '.')); // v1.6b1
    finally
      closeFile(inputFile);
    end;
  except
    on E: Exception do
      begin
      stopWaitMessage;
  		ShowMessage(E.message);
  		ShowMessage('Could not load file ' + fileNameWithPath);
    	exit;
      end;
	end;
  if newTdo <> nil then
    begin
    newCommand := PdLoadTdoFromDXFCommand.createWithOldAndNewTdo(self.tdo, newTdo);
    self.doCommand(newCommand);
    end;
  stopWaitMessage;
  end;

procedure TTdoEditorForm.writeToPOVClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
    suggestedName: string;
  begin
  suggestedName := replacePunctuationWithUnderscores(tdo.getName) + '.inc';
  if not getFileSaveInfo(kFileTypeINC, kAskForFileName, suggestedName, fileInfo) then exit;
  try
    startFileSave(fileInfo);
    tdo.writeToPOV_INCFile(fileInfo.tempFile, kTdoForeColor, kEmbeddedInPlant, plantParts.value);
    fileInfo.writingWasSuccessful := true;
  finally
    cleanUpAfterFileSave(fileInfo);
  end;
	end;

procedure TTdoEditorForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Editing_3D_objects');
  end;

{ ------------------------------------------------------------------------------------- *mouse handling }
procedure TTdoEditorForm.imagesMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    newCommand: PdCommand;
    anchorPoint: TPoint;
  begin
  if application.terminated then exit;
  if paintBoxClickedIn = nil then exit;
  if actionInProgress then
    try    {error somewhere - user did weird things with mouse buttons - teminate action...}
      self.imagesMouseUp(sender, button, shift, x, y);
    finally
      actionInProgress := false;
    end;
  commandList.rightButtonDown := (button = mbRight) or (ssShift in shift); // makes shift-click work as right-click
  case cursorMode of
    kCursorModeMagnify:
      if commandList.rightButtonDown then
        paintBoxClickedIn.cursor := crMagMinus;
    kCursorModeScroll:
      begin
      if commandList.rightButtonDown then exit;
      scrolling := true;
      startDragPoint := Point(x, y);
      scrollStartPosition := paintBoxClickedIn.drawPosition;
      end;
    kCursorModeRotate:
      if paintBoxClickedIn <> editPaintBox then
        begin
        rotating := true;
        startDragPoint := Point(x, y);
        rotateDirection := kRotateNotInitialized;
        if commandList.rightButtonDown then paintBoxClickedIn.cursor := crSizeWE;
        end;
    kCursorModeAddTriangles:
      if numNewPoints >= 3 then
        numNewPoints := 0;
    else
      begin
      if (commandList.rightButtonDown) and (cursorMode <> kCursorModeDragPoints) then exit;
      anchorPoint := Point(x, y);
      actionInProgress := true;
      newCommand := self.makeMouseCommand(anchorPoint, (ssShift in shift), (ssCtrl in shift));
      if newCommand <> nil then
        actionInProgress := commandList.mouseDown(newCommand, anchorPoint)
      else
        actionInProgress := false;
      if actionInProgress then self.updateForChangeToTdo;
      end;
    end;
	end;

procedure TTdoEditorForm.imagesMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
  begin
  if application.terminated then exit;
  if (sender = editPaintBox) then
    case cursorMode of
      kCursorModeAddTriangles, kCursorModeDragPoints:
        if numNewPoints = 0 then self.lightUpPointAtMouse(x, y, kDrawNow);
      kCursorModeDeleteTriangles, kCursorModeFlipTriangles:
        self.lightUpTriangleAtMouse(x, y);
      end;
  if paintBoxClickedIn = nil then exit;
  if sender <> paintBoxClickedIn then exit;
  case cursorMode of
    kCursorModeMagnify: if scrolling then self.scrollBy(x, y);
    kCursorModeScroll: if scrolling then self.scrollBy(x, y);
    kCursorModeRotate: if rotating then self.rotateBy(x, y);
    kCursorModeAddTriangles:
      if sender = editPaintBox then
        if (numNewPoints = 1) or (numNewPoints = 2) then
          self.lightUpAddingLineAtMouse(x, y);
    else if actionInProgress then
      begin
      commandList.mouseMove(Point(x, y));
      self.updateForChangeToTdo;
      end;
    end;
	end;

procedure TTdoEditorForm.imagesMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    triangle: KfIndexTriangle;
	begin
  if application.terminated then exit;
  if paintBoxClickedIn = nil then exit;
  if cursorMode <> kCursorModeAddTriangles then numNewPoints := 0;
  try
  case cursorMode of
    kCursorModeMagnify:
      begin
      if (commandList.rightButtonDown) then
        begin
        paintBoxClickedIn.magnifyOrReduce(paintBoxClickedIn.scale * 0.75, Point(x,y));
        if not (ssShift in shift) then
          paintBoxClickedIn.cursor := crMagPlus;
        end
      else if (ssShift in shift) then
        paintBoxClickedIn.magnifyOrReduce(paintBoxClickedIn.scale * 0.75, Point(x,y))
      else
        paintBoxClickedIn.magnifyOrReduce(paintBoxClickedIn.scale * 1.5, Point(x,y));
      end;
    kCursorModeScroll: if scrolling then self.scrollBy(x, y);
    kCursorModeRotate:
      begin
      if rotating then self.rotateBy(x, y);
      if paintBoxClickedIn <> editPaintBox then paintBoxClickedIn.cursor := crRotate;
      end;
    kCursorModeFlipTriangles:
      begin
      if paintBoxClickedIn = editPaintBox then
        begin
        triangle := self.triangleAtMouse(x, y);
        if triangle <> nil then
          begin
          triangle.flip;
          self.updateForChangeToTdo;
          end;
        end;
      end;
    kCursorModeAddTriangles:
      begin
      if paintBoxClickedIn = editPaintBox then self.addTrianglePoints(x, y);
      end;
    else if actionInProgress then
      begin
      commandList.mouseUp(Point(x, y));
      actionInProgress := false;
      self.updateForChangeToTdo;
      end;
    end;
  finally
    scrolling := false;
    rotating := false;
    commandList.rightButtonDown := false;
    actionInProgress := false;
    draggingPoint := false;
  end;
	end;

procedure TTdoEditorForm.editPaintBoxMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  paintBoxClickedIn := editPaintBox;
  self.imagesMouseDown(sender, button, shift, x, y);
  end;

procedure TTdoEditorForm.viewPaintBoxOneMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  paintBoxClickedIn := viewPaintBoxOne;
  self.imagesMouseDown(sender, button, shift, x, y);
  end;

procedure TTdoEditorForm.viewPaintBoxTwoMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  paintBoxClickedIn := viewPaintBoxTwo;
  self.imagesMouseDown(sender, button, shift, x, y);
  end;

{ -------------------------------------------------------------------------------- *finding and lighting up }
procedure TTdoEditorForm.lightUpPointAtMouse(x, y: integer; immediate: boolean);
  var
    i, pointFound: smallint;
  begin
  pointFound := -1;
  if draggingPoint then
    begin
    if (pointIndexBeingDragged >= 0) and (pointIndexBeingDragged <= numEditPoints - 1) then
      pointFound := pointIndexBeingDragged;
    end
  else
    pointFound := self.pointIndexAtMouse(x, y);
  if pointFound >= 0 then
    begin
    with editPaintBox.bitmap.canvas do
      begin
      pen.color := kLightUpColor;
      brush.color := kLightUpColor;
      brush.style := bsSolid;
      ellipse(editPoints[pointFound].x - pointRadius, editPoints[pointFound].y - pointRadius,
          editPoints[pointFound].x + pointRadius, editPoints[pointFound].y + pointRadius);
      end;
    end
  else
    begin
    if not draggingPoint then if numEditPoints > 0 then for i := 0 to numEditPoints - 1 do
      begin
      with editPaintBox.bitmap.canvas do
        begin
        if i = tdo.originPointIndex then     
          begin
          pen.color := kOriginPointColor;
          brush.color := kOriginPointColor;
          end
        else
          begin
          pen.color := kConnectedPointColor;
          brush.color := kConnectedPointColor;
          end;
        brush.style := bsSolid;
        ellipse(editPoints[i].x - pointRadius, editPoints[i].y - pointRadius,
          editPoints[i].x + pointRadius, editPoints[i].y + pointRadius);
        end;
      end;
    end;
  if immediate then
    self.drawPaintBoxBitmapOnCanvas(editPaintBox);
  end;

function TTdoEditorForm.pointIndexAtMouse(x, y: integer): smallint;
  var
    i: smallint;
  begin
  result := -1;
  if numEditPoints > 0 then for i := 0 to numEditPoints - 1 do
    if (abs(x - editPoints[i].x) <= pointRadius) and (abs(y - editPoints[i].y) <= pointRadius) then
      begin
      result := i;
      exit;
      end;
  end;

procedure TTdoEditorForm.lightUpTriangleAtMouse(x, y: integer);
  var
    triangle: KfIndexTriangle;
    aPolygon: array[0..2] of TPoint;
  begin
  self.drawTdoOnTdoPaintBox(editPaintBox, kDontDrawYet);
  triangle := self.triangleAtMouse(x, y);
  if triangle <> nil then with editPaintBox.bitmap.canvas do
    begin
    pen.color := kLightUpColor;
    brush.style := bsClear;
    aPolygon[0] := editPoints[triangle.pointIndexes[0]-1];
    aPolygon[1] := editPoints[triangle.pointIndexes[1]-1];
    aPolygon[2] := editPoints[triangle.pointIndexes[2]-1];
    polygon(aPolygon);
    end;
  self.drawPaintBoxBitmapOnCanvas(editPaintBox);
  end;

function TTdoEditorForm.triangleAtMouse(x, y: integer): KfIndexTriangle;
  var
    i: smallint;
    triangle: KfIndexTriangle;
    polygon: array[0..2] of TPoint;
    hPolygon: HRgn;
    inTriangle: boolean;
  begin
  result := nil;
  if tdo.triangles.count > 0 then for i := 0 to tdo.triangles.count - 1 do
    begin
    triangle := KfIndexTriangle(tdo.triangles.items[i]);
    polygon[0] := editPoints[triangle.pointIndexes[0]-1];
    polygon[1] := editPoints[triangle.pointIndexes[1]-1];
    polygon[2] := editPoints[triangle.pointIndexes[2]-1];
    hPolygon := createPolygonRgn(polygon, 3, ALTERNATE);
    selectObject(self.handle, hPolygon);
    try
      inTriangle := ptInRegion(hPolygon, x, y);
    finally
      deleteObject(hPolygon);
    end;
    if inTriangle then
      begin
      result := KfIndexTriangle(tdo.triangles.items[i]);
      exit;
      end;
    end;
  end;

procedure TTdoEditorForm.scrollBy(x, y: integer);
  begin
  paintBoxClickedIn.drawPosition.x := scrollStartPosition.x + x - startDragPoint.x;
  paintBoxClickedIn.drawPosition.y := scrollStartPosition.y + y - startDragPoint.y;
  self.updateForChangeToClickedOnPaintBox;
  end;

procedure TTdoEditorForm.rotateBy(x, y: integer);
  begin
  { don't initialize for first few pixels so any wobbling at the start doesn't start you out
    in the wrong direction }
  if (rotateDirection = kRotateNotInitialized) and
      ((abs(x - startDragPoint.x) > 5) or (abs(y - startDragPoint.y) > 5)) then
    begin
    if commandList.rightButtonDown then
      rotateDirection := kRotateZ
    else if abs(x - startDragPoint.x) > abs(y - startDragPoint.y) then
      rotateDirection := kRotateX
    else
      rotateDirection := kRotateY;
    case rotateDirection of
      kRotateX: rotateStartAngle := paintBoxClickedIn.xRotation;
      kRotateY: rotateStartAngle := paintBoxClickedIn.yRotation;
      kRotateZ: rotateStartAngle := paintBoxClickedIn.zRotation;
      end;
    end;
  case rotateDirection of
    kRotateX:
      paintBoxClickedIn.xRotation := min(360, max(-360, rotateStartAngle + (x - startDragPoint.x) * 0.5));
    kRotateY:
      paintBoxClickedIn.yRotation := min(360, max(-360, rotateStartAngle + (y - startDragPoint.y) * 0.5));
    kRotateZ:
      paintBoxClickedIn.zRotation := min(360, max(-360, rotateStartAngle + (startDragPoint.x - x) * 0.5));
    end;
  self.updateForChangeToClickedOnPaintBox;
  end;

procedure TTdoEditorForm.addTrianglePoints(x, y: smallint);
  var
    pointIndex: smallint;
    newCommand: PdCommand;
    circleRect: TRect;
    newPoint: TPoint;
  begin
  inc(numNewPoints);
  pointIndex := self.pointIndexAtMouse(x, y);
  newPointIndexes[numNewPoints-1] := pointIndex;
  if pointIndex >= 0 then
    newPoints[numNewPoints-1] := tdo.points[pointIndex]
  else
    begin
    newPoints[numNewPoints-1].x := (x - editPaintBox.drawPosition.x) / editPaintBox.scale;
    newPoints[numNewPoints-1].y := (y - editPaintBox.drawPosition.y) / editPaintBox.scale;
    newPoints[numNewPoints-1].z := 0;
    end;
  with editPaintBox.bitmap.canvas do
    begin
    brush.style := bsSolid;
    pen.style := psSolid;
    brush.color := kUnconnectedPointColor;
    pen.color := kUnconnectedPointColor;
    newPoint.x := editPaintBox.drawPosition.x + round(newPoints[numNewPoints-1].x * editPaintBox.scale);
    newPoint.y := editPaintBox.drawPosition.y + round(newPoints[numNewPoints-1].y * editPaintBox.scale);
    circleRect := Rect(newPoint.x - pointRadius, newPoint.y - pointRadius,
      newPoint.x + pointRadius, newPoint.y + pointRadius);
    with circleRect do ellipse(left, top, right, bottom);
    if numNewPoints >= 3 then
      begin
      newCommand := PdAddTdoTriangleCommand.createWithTdoAndNewPoints(self.tdo, newPointIndexes, newPoints);
      numNewPoints := 0;
      newPointIndexes[0] := 0;
      newPointIndexes[1] := 0;
      newPointIndexes[2] := 0;
      self.doCommand(newCommand);
      end;
    end;
  if numNewPoints < 3 then
    self.drawPaintBoxBitmapOnCanvas(editPaintBox);
  end;

procedure TTdoEditorForm.drawPaintBoxBitmapOnCanvas(aPaintBox: PdTdoPaintBox);
  begin
  if aPaintBox <> nil then
    copyBitmapToCanvasWithGlobalPalette(aPaintBox.bitmap, aPaintBox.canvas, rect(0,0,0,0));
  end;

procedure TTdoEditorForm.lightUpAddingLineAtMouse(x, y: smallint);
  var
    firstPoint, secondPoint: TPoint;
  begin
  with editPaintBox.bitmap.canvas do
    begin
    brush.color := clWindow;
    brush.style := bsSolid;
    pen.style := psClear;
    fillRect(Rect(0, 0, editPaintBox.width, editPaintBox.height));
    self.drawTdoOnTdoPaintBox(editPaintBox, kDontDrawYet);
    self.lightUpPointAtMouse(x, y, kDontDrawYet);
    firstPoint.x := editPaintBox.drawPosition.x + round(newPoints[0].x * editPaintBox.scale);
    firstPoint.y := editPaintBox.drawPosition.y + round(newPoints[0].y * editPaintBox.scale);
    if numNewPoints > 1 then
      begin
      secondPoint.x := editPaintBox.drawPosition.x + round(newPoints[1].x * editPaintBox.scale);
      secondPoint.y := editPaintBox.drawPosition.y + round(newPoints[1].y * editPaintBox.scale);
      end;
    pen.color := kUnconnectedPointColor;
    moveTo(firstPoint.x, firstPoint.y);
    if numNewPoints > 1 then lineTo(secondPoint.x, secondPoint.y);
    lineTo(x, y);
    pen.color := kUnconnectedPointColor;
    brush.color := kUnconnectedPointColor;
    brush.style := bsSolid;
    with firstPoint do
      ellipse(x - pointRadius, y - pointRadius, x + pointRadius, y + pointRadius);
    if numNewPoints > 1 then with secondPoint do
      ellipse(x - pointRadius, y - pointRadius, x + pointRadius, y + pointRadius);
    ellipse(x - pointRadius+1, y - pointRadius+1, x + pointRadius-1, y + pointRadius-1);
    end;
  self.drawPaintBoxBitmapOnCanvas(editPaintBox);
  end;

function TTdoEditorForm.makeMouseCommand(var point: TPoint; shift, ctrl: boolean): PdCommand;
	begin
  result := nil;
  if paintBoxClickedIn <> editPaintBox then exit;
  case cursorMode of
    kCursorModeAddTriangles: {handled in mouse up};
    kCursorModeDeleteTriangles:
      if paintBoxClickedIn = editPaintBox then
        result := PdRemoveTdoTriangleCommand.createWithTdo(self.tdo);
    kCursorModeDragPoints:
      if paintBoxClickedIn = editPaintBox then
        result := PdDragTdoPointCommand.createWithTdoAndScale(self.tdo, paintBoxClickedIn.scale);
    end;
  end;

{ ------------------------------------------------------------------------------------- *drawing }
procedure TTdoEditorForm.editPaintBoxPaint(Sender: TObject);
  begin
  self.checkImageForBitmapSizeAndFill(editPaintBox);
  self.drawTdoOnTdoPaintBox(editPaintBox, kDrawNow);
  end;

procedure TTdoEditorForm.viewPaintBoxOnePaint(Sender: TObject);
  begin
  self.checkImageForBitmapSizeAndFill(viewPaintBoxOne);
  self.drawTdoOnTdoPaintBox(viewPaintBoxOne, kDrawNow);
  end;

procedure TTdoEditorForm.viewPaintBoxTwoPaint(Sender: TObject);
  begin
  self.checkImageForBitmapSizeAndFill(viewPaintBoxTwo);
  self.drawTdoOnTdoPaintBox(viewPaintBoxTwo, kDrawNow);
  end;

procedure TTdoEditorForm.checkImageForBitmapSizeAndFill(aPaintBox: PdTdoPaintBox);
  begin
  if (aPaintBox.bitmap.width <> aPaintBox.width) or (aPaintBox.bitmap.height <> aPaintBox.height) then
    begin
    try
      aPaintBox.bitmap.width := aPaintBox.width;
      aPaintBox.bitmap.height := aPaintBox.height;
    except
      aPaintBox.bitmap.width := 1;
      aPaintBox.bitmap.height := 1;
    end;
    end;
  with aPaintBox.bitmap.canvas do
    begin
    brush.color := clWindow;
    brush.style := bsSolid;
    pen.style := psClear;
    fillRect(Rect(0, 0, aPaintBox.width, aPaintBox.height));
    end;
  end;

procedure TTdoEditorForm.drawTdoOnTdoPaintBox(aPaintBox: PdTdoPaintBox; immediate: boolean);
  var
    turtle: KfTurtle;
    i, parts: smallint;
    wasFillingTriangles: boolean;
    pointOfConnection: TPoint;
  begin
  if tdo = nil then exit;
  turtle := KfTurtle.defaultStartUsing;
  try
    // set up turtle
    turtle.drawingSurface.pane := aPaintBox.bitmap.canvas;
    turtle.setDrawOptionsForDrawingTdoOnly;
    with turtle.drawOptions do
      begin
      drawLines := self.drawLines.checked;
      wireFrame := not self.fillTriangles.checked;
      circlePoints := aPaintBox = self.editPaintBox;
      if aPaintBox = self.editPaintBox then
        begin
        turtle.drawOptions.circlePointRadius := pointRadius;
        turtle.drawingSurface.circleColor := kConnectedPointColor;
        end;
      end;
    turtle.reset; { must be after pane and draw options set }
    turtle.xyz(aPaintBox.drawPosition.x, aPaintBox.drawPosition.y, 0);
    turtle.resetBoundsRect(aPaintBox.drawPosition);
    turtle.rotateX(aPaintBox.yRotation * 256 / 360);
    turtle.rotateY(aPaintBox.xRotation * 256 / 360);
    turtle.rotateZ(aPaintBox.zRotation * 256 / 360);
    // draw parts
    parts := plantParts.value;
    if aPaintBox = self.editPaintBox then parts := 1;
    if parts = 0 then
      raise Exception.create('Zero parts not allowed.');
    turtle.drawingSurface.recordingStart;
    if parts > 1 then turtle.rotateZ(-64);
    for i := 0 to parts - 1 do
      begin
      if parts > 1 then
        begin
        turtle.rotateX(256 div parts);
        turtle.push;
        turtle.rotateY(64);
        turtle.rotateX(64);
        end;
      tdo.draw(turtle, aPaintBox.scale, '', '',  0, 0);
      if (mirrorHalf.checked) and (not (aPaintBox = self.editPaintBox)) then
        begin
        turtle.push;
        turtle.rotateY(256 div 2);
        tdo.reverseZValues;
        turtle.drawingSurface.foreColor := rgb(255, 255, 200);
        turtle.drawingSurface.backColor := rgb(255, 255, 200);
        turtle.drawingSurface.lineColor := clBlack;
        tdo.draw(turtle, aPaintBox.scale, '', '', 0, 0);
        turtle.drawingSurface.foreColor := kTdoForeColor;
        turtle.drawingSurface.backColor := kTdoBackColor;
        tdo.reverseZValues;
        turtle.pop;
        end;
      if parts > 1 then turtle.pop;
      end;
    turtle.drawingSurface.recordingStop;
    turtle.drawingSurface.recordingDraw;
    turtle.drawingSurface.clearTriangles;
    // if edit panel, get new locations of edit points
    if aPaintBox = self.editPaintBox then
      begin
      numEditPoints := turtle.recordedPointsInUse;
      if numEditPoints > 0 then for i := 0 to numEditPoints - 1 do
        self.editPoints[i] := Point(round(turtle.recordedPoints[i].x), round(turtle.recordedPoints[i].y));
      // draw connection point circle in black over rest
      if numEditPoints > 0 then with aPaintBox.bitmap.canvas do
        begin
        brush.color := kOriginPointColor;
        pen.color := kOriginPointColor;
        pointOfConnection := editPoints[tdo.originPointIndex];
        ellipse(pointOfConnection.x - pointRadius, pointOfConnection.y - pointRadius,
          pointOfConnection.x + pointRadius, pointOfConnection.y + pointRadius);
        end;
      if draggingPoint then
        self.lightUpPointAtMouse(commandList.previousPoint.x, commandList.previousPoint.y, kDontDrawYet);
      end;
    // get bounds rect from turtle
    aPaintBox.tdoBoundsRect := turtle.boundsRect;
    // draw border
    with aPaintBox.bitmap.canvas do
      begin
      brush.style := bsClear;
      pen.color := clBtnText;
      rectangle(0, 0, aPaintBox.width, aPaintBox.height);
      end;
    // draw
    if immediate then
      self.drawPaintBoxBitmapOnCanvas(aPaintBox);
  finally
    KfTurtle.defaultStopUsing;
  end;
  end;

procedure TTdoEditorForm.centerDrawingInPaintBox(aPaintBox: PdTdoPaintBox);
  var
    newScaleX, newScaleY: single;
    centerPointOfTdoBoundsRect, centerOfPaintBox, offset: TPoint;
  begin
  if aPaintBox = nil then exit;
  aPaintBox.scale := 100.0; // set high so it will never be too small
  { 1. draw to determine new scale }
  self.drawTdoOnTdoPaintBox(aPaintBox, kDontDrawYet);
  newScaleX := safedivExcept(0.95 * aPaintBox.scale * aPaintBox.width, rWidth(aPaintBox.tdoBoundsRect), 0.1);
  newScaleY := safedivExcept(0.95 * aPaintBox.scale * aPaintBox.height, rHeight(aPaintBox.tdoBoundsRect), 0.1);
  aPaintBox.scale := min(newScaleX, newScaleY);
  { 2. draw to determine shift of drawPosition if any - fill in case this is last draw }
  aPaintBox.bitmap.canvas.brush.color := clWhite;
  aPaintBox.bitmap.canvas.fillRect(rect(0, 0, aPaintBox.width, aPaintBox.height));
  self.drawTdoOnTdoPaintBox(aPaintBox, kDontDrawYet);
  // v2 improved how this is done
  with aPaintBox do
    begin
    centerPointOfTdoBoundsRect := Point(
        tdoBoundsRect.left + (tdoBoundsRect.right - tdoBoundsRect.left) div 2,
        tdoBoundsRect.top + (tdoBoundsRect.bottom - tdoBoundsRect.top) div 2);
    centerOfPaintBox := Point(width div 2, height div 2);
    offset := Point(centerOfPaintBox.x - centerPointOfTdoBoundsRect.x, centerOfPaintBox.y - centerPointOfTdoBoundsRect.y);
    drawPosition.x := drawPosition.x + offset.x;
    drawPosition.y := drawPosition.y + offset.y;
    end;
  { 3. draw with new scale and position if position changed }
  aPaintBox.bitmap.canvas.brush.color := clWhite;
  aPaintBox.bitmap.canvas.fillRect(rect(0, 0, aPaintBox.width, aPaintBox.height));
  self.drawTdoOnTdoPaintBox(aPaintBox, kDontDrawYet);
  self.drawPaintBoxBitmapOnCanvas(aPaintBox);
  end;

{ ------------------------------------------------------------------------ *toolbar }
procedure TTdoEditorForm.scrollCursorModeClick(Sender: TObject);
  begin
  cursorMode := kCursorModeScroll;
  if (editPaintBox <> nil) and (viewPaintBoxOne <> nil) and (viewPaintBoxTwo <> nil) then
    begin
    editPaintBox.cursor := crScroll;
    viewPaintBoxOne.cursor := crScroll;
    viewPaintBoxTwo.cursor := crScroll;
    end;
  end;

procedure TTdoEditorForm.magnifyCursorModeClick(Sender: TObject);
  begin
  cursorMode := kCursorModeMagnify;
  editPaintBox.cursor := crMagPlus;
  viewPaintBoxOne.cursor := crMagPlus;
  viewPaintBoxTwo.cursor := crMagPlus;
  end;

procedure TTdoEditorForm.rotateCursorModeClick(Sender: TObject);
  begin
  cursorMode := kCursorModeRotate;
  editPaintBox.cursor := crDefault; {can't rotate edit picture}
  viewPaintBoxOne.cursor := crRotate;
  viewPaintBoxTwo.cursor := crRotate;
  end;

procedure TTdoEditorForm.addTrianglePointsCursorModeClick(Sender: TObject);
  begin
  cursorMode := kCursorModeAddTriangles;
  editPaintBox.cursor := crAddTriangle;
  viewPaintBoxOne.cursor := crDefault;
  viewPaintBoxTwo.cursor := crDefault;
  end;

procedure TTdoEditorForm.removeTriangleCursorModeClick(Sender: TObject);
  begin
  cursorMode := kCursorModeDeleteTriangles;
  editPaintBox.cursor := crDeleteTriangle;
  viewPaintBoxOne.cursor := crDefault;
  viewPaintBoxTwo.cursor := crDefault;
  end;

procedure TTdoEditorForm.dragCursorModeClick(Sender: TObject);
  begin
  cursorMode := kCursorModeDragPoints;
  editPaintBox.cursor := crDragPoint;
  viewPaintBoxOne.cursor := crDefault;
  viewPaintBoxTwo.cursor := crDefault;
  end;

procedure TTdoEditorForm.flipTriangleCursorModeClick(Sender: TObject);
  begin
  cursorMode := kCursorModeFlipTriangles;
  editPaintBox.cursor := crFlipTriangle;
  viewPaintBoxOne.cursor := crDefault;
  viewPaintBoxTwo.cursor := crDefault;
  end;

procedure TTdoEditorForm.FormKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  if key = VK_Shift then
    begin
    if cursorMode = kCursorModeMagnify then
      begin
      editPaintBox.cursor := crMagMinus;
      viewPaintBoxOne.cursor := crMagMinus;
      viewPaintBoxTwo.cursor := crMagMinus;
      end;
    end
  end;

procedure TTdoEditorForm.FormKeyUp(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  if key = VK_Shift then
    begin
    if cursorMode = kCursorModeMagnify then
      begin
      editPaintBox.cursor := crMagPlus;
      viewPaintBoxOne.cursor := crMagPlus;
      viewPaintBoxTwo.cursor := crMagPlus;
      end;
    end;
  end;

procedure TTdoEditorForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

procedure TTdoEditorForm.magnifyPlusClick(Sender: TObject);
  begin
  if editPaintBox <> nil then with editPaintBox do magnifyOrReduce(scale * 1.5, drawPosition);
  if viewPaintBoxOne <> nil then with viewPaintBoxOne do magnifyOrReduce(scale * 1.5, drawPosition);
  if viewPaintBoxTwo <> nil then with viewPaintBoxTwo do magnifyOrReduce(scale * 1.5, drawPosition);
  end;

procedure TTdoEditorForm.magnifyMinusClick(Sender: TObject);
  begin
  if editPaintBox <> nil then with editPaintBox do magnifyOrReduce(scale * 0.75, drawPosition);
  if viewPaintBoxOne <> nil then with viewPaintBoxOne do magnifyOrReduce(scale * 0.75, drawPosition);
  if viewPaintBoxTwo <> nil then with viewPaintBoxTwo do magnifyOrReduce(scale * 0.75, drawPosition);
  end;

procedure TTdoEditorForm.centerDrawingClick(Sender: TObject);
  begin
  if editPaintBox <> nil then self.centerDrawingInPaintBox(editPaintBox);
  if viewPaintBoxOne <> nil then self.centerDrawingInPaintBox(viewPaintBoxOne);
  if viewPaintBoxTwo <> nil then self.centerDrawingInPaintBox(viewPaintBoxTwo);
  end;

procedure TTdoEditorForm.resetRotationsClick(Sender: TObject);
  begin
  if editPaintBox <> nil then editPaintBox.resetRotations;
  if viewPaintBoxOne <> nil then viewPaintBoxOne.resetRotations;
  if viewPaintBoxTwo <> nil then viewPaintBoxTwo.resetRotations;
  end;

procedure TTdoEditorForm.mirrorTdoClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdMirrorTdoCommand.createWithTdo(self.tdo);
  self.doCommand(newCommand);
  end;

procedure TTdoEditorForm.reverseZValuesClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdReverseZValuesTdoCommand.createWithTdo(self.tdo);
  self.doCommand(newCommand);
  end;

{ --------------------------------------------------------------------------------------- *resizing and splitting }
procedure TTdoEditorForm.FormResize(Sender: TObject);
  var
    newTop, newLeft, widthBeforeButtons: smallint;
  begin
  if Application.terminated then exit;
  if tdo = nil then exit; 
  if self.WindowState = wsMinimized then exit;
  verticalSplitter.visible := false;
  horizontalSplitter.visible := false;
  widthBeforeButtons := intMax(0, self.clientWidth - ok.width - kBetweenGap * 2);
  { pictures panel }
  with picturesPanel do setBounds(0, toolbarPanel.height, widthBeforeButtons,
    intMax(0, self.clientHeight - optionsPanel.height - toolBarPanel.height - 4));
  { vertical splitter }
  if lastPicturesPanelWidth <> 0 then
    newLeft := round(1.0 * verticalSplitter.left * picturesPanel.width / lastPicturesPanelWidth)
  else
    newLeft := picturesPanel.width div 2;
  if newLeft >= picturesPanel.width then newLeft := picturesPanel.width - 1;
  if newLeft < 0 then newLeft := 0;
  with verticalSplitter do setBounds(newLeft, 0, width, picturesPanel.height);
  { horizontal splitter }
  if lastPicturesPanelHeight <> 0 then
    newTop := round(1.0 * horizontalSplitter.top * picturesPanel.height / lastPicturesPanelHeight)
  else
    newTop := picturesPanel.height div 2;
  if newTop >= picturesPanel.height then newTop := picturesPanel.height - 1;
  if newTop < 0 then newTop := 0;
  with horizontalSplitter do setBounds(
      verticalSplitter.left + verticalSplitter.width, newTop,
      intMax(0, picturesPanel.width - verticalSplitter.left - verticalSplitter.width), height);
  internalChange := true;
  self.resizeImagesToVerticalSplitter;
  self.resizeImagesToHorizontalSplitter;
  internalChange := false;
  self.setInitialDrawPositionsIfNotSet;
  { rest of window }
  with toolbarPanel do setBounds(0, 0, picturesPanel.width, height);
  with optionsPanel do setBounds(0, picturesPanel.top + picturesPanel.height + 4, picturesPanel.width, height);
  ok.left := self.clientWidth - ok.width - kBetweenGap;
  cancel.left := ok.left;
  undoLast.left := ok.left;
  redoLast.left := ok.left;
  renameTdo.left := ok.left;
  clearTdo.left := ok.left;
  writeToDXF.left := ok.left;
  readFromDXF.left := ok.left;
  writeToPOV.left := ok.left;
  helpButton.left := ok.left;
  lastPicturesPanelWidth := picturesPanel.width;
  lastPicturesPanelHeight := picturesPanel.height;
  verticalSplitter.visible := true;
  horizontalSplitter.visible := true;
  end;

procedure TTdoEditorForm.resizeImagesToVerticalSplitter;
  var
    newLeft: smallint;
  begin
  if editPaintBox <> nil then
    with editPaintBox do setBounds(0, 0, verticalSplitter.left, picturesPanel.height);
  newLeft := verticalSplitter.left + verticalSplitter.width;
  with horizontalSplitter do setBounds(newLeft, top, intMax(0, picturesPanel.width - newLeft), height);
  if viewPaintBoxOne <> nil then
    with viewPaintBoxOne do setBounds(newLeft, top, intMax(0, picturesPanel.width - newLeft), height);
  if viewPaintBoxTwo <> nil then
    with viewPaintBoxTwo do setBounds(newLeft, top, intMax(0, picturesPanel.width - newLeft), height);
  if not internalChange then self.updateForChangeToTdo;
  end;

procedure TTdoEditorForm.resizeImagesToHorizontalSplitter;
  var
    newTop: smallint;
  begin
  if viewPaintBoxOne <> nil then
    with viewPaintBoxOne do setBounds(left, 0, width, horizontalSplitter.top);
  newTop := horizontalSplitter.top + horizontalSplitter.height;
  if viewPaintBoxTwo <> nil then
    with viewPaintBoxTwo do setBounds(left, newTop, width, intMax(0, picturesPanel.height - newTop));
  if not internalChange then self.updateForChangeToTdo;
  end;

procedure TTdoEditorForm.setInitialDrawPositionsIfNotSet;
  begin
  if editPaintBox <> nil then
    with editPaintBox do if (drawPosition.x = 0) and (drawPosition.y = 0) then
      begin
      drawPosition := Point(width div 2, height - 10);
      paint;
      end;
  if viewPaintBoxOne <> nil then
    with viewPaintBoxOne do if (drawPosition.x = 0) and (drawPosition.y = 0) then
      begin
      drawPosition := Point(width div 2, height - 10);
      paint;
      end;
  if viewPaintBoxTwo <> nil then
    with viewPaintBoxTwo do if (drawPosition.x = 0) and (drawPosition.y = 0) then
      begin
      drawPosition := Point(width div 2, height - 10);
      paint;
      end;
  end;

procedure TTdoEditorForm.verticalSplitterMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  self.verticalSplitterDragging := true;
  self.verticalSplitterStartPos := x;
  self.verticalSplitterLastDrawPos := -1;
  self.verticalSplitterNeedToRedraw := true;
  end;

procedure TTdoEditorForm.verticalSplitterMouseMove(Sender: TObject;
  Shift: TShiftState; X, Y: Integer);
  begin
  if self.verticalSplitterDragging and
    (verticalSplitter.left + x >= kSplitterDragToLeftMinPixels)
      and (verticalSplitter.left + x < picturesPanel.width - kSplitterDragToRightMinPixels) then
      begin
      self.undrawVerticalSplitterLine;
      self.verticalSplitterLastDrawPos := self.drawVerticalSplitterLine(x);
      end;
  end;

procedure TTdoEditorForm.verticalSplitterMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  if self.verticalSplitterDragging then
    begin
    self.undrawVerticalSplitterLine;
    verticalSplitter.left := verticalSplitter.left - (verticalSplitterStartPos - x);
    if verticalSplitter.left < kSplitterDragToLeftMinPixels then
      verticalSplitter.left := kSplitterDragToLeftMinPixels;
    if verticalSplitter.left > picturesPanel.width - kSplitterDragToRightMinPixels then
      verticalSplitter.left := picturesPanel.width - kSplitterDragToRightMinPixels;
  	self.resizeImagesToVerticalSplitter;
    self.verticalSplitterDragging := false;
    end;
  end;

function TTdoEditorForm.drawVerticalSplitterLine(pos: integer): integer;
  var
    theDC: HDC;
  begin
  theDC := getDC(0);
  result := self.clientOrigin.x + verticalSplitter.left + pos + 2;
  patBlt(theDC, result, self.clientOrigin.y + picturesPanel.top + verticalSplitter.top, 1,
      verticalSplitter.height, dstInvert);
  releaseDC(0, theDC);
  self.verticalSplitterNeedToRedraw := true;
  end;

procedure TTdoEditorForm.undrawVerticalSplitterLine;
  var theDC: HDC;
  begin
  if not self.verticalSplitterNeedToRedraw then exit;
  theDC := getDC(0);
  patBlt(theDC, self.verticalSplitterLastDrawPos,
    self.clientOrigin.y + picturesPanel.top + verticalSplitter.top, 1, verticalSplitter.height, dstInvert);
  releaseDC(0, theDC);
  self.verticalSplitterNeedToRedraw := false;
  end;

procedure TTdoEditorForm.horizontalSplitterMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  self.horizontalSplitterDragging := true;
  self.horizontalSplitterStartPos := y;
  self.horizontalSplitterLastDrawPos := -1;
  self.horizontalSplitterNeedToRedraw := true;
  end;

procedure TTdoEditorForm.horizontalSplitterMouseMove(Sender: TObject;
  Shift: TShiftState; X, Y: Integer);
  begin
  if self.horizontalSplitterDragging and
    (horizontalSplitter.top + y >= kSplitterDragToTopMinPixels)
      and (horizontalSplitter.top + y < picturesPanel.height - kSplitterDragToBottomMinPixels) then
      begin
      self.undrawHorizontalSplitterLine;
      self.horizontalSplitterLastDrawPos := self.drawHorizontalSplitterLine(y);
      end;
  end;

procedure TTdoEditorForm.horizontalSplitterMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  if self.horizontalSplitterDragging then
    begin
    self.undrawHorizontalSplitterLine;
    horizontalSplitter.top := horizontalSplitter.top - (horizontalSplitterStartPos - y);
    if horizontalSplitter.top < kSplitterDragToTopMinPixels then
      horizontalSplitter.top := kSplitterDragToTopMinPixels;
    if horizontalSplitter.top > picturesPanel.height - kSplitterDragToBottomMinPixels then
      horizontalSplitter.top := picturesPanel.height - kSplitterDragToBottomMinPixels;
  	self.resizeImagesToHorizontalSplitter;
    self.horizontalSplitterDragging := false;
    end;
  end;

function TTdoEditorForm.drawHorizontalSplitterLine(pos: integer): integer;
  var
    theDC: HDC;
  begin
  theDC := getDC(0);
  result := self.clientOrigin.y + horizontalSplitter.top + pos + 2;
  patBlt(theDC, self.clientOrigin.x + horizontalSplitter.left, result,
      horizontalSplitter.width, 1, dstInvert);
  releaseDC(0, theDC);
  self.horizontalSplitterNeedToRedraw := true;
  end;

procedure TTdoEditorForm.undrawHorizontalSplitterLine;
  var theDC: HDC;
  begin
  if not self.horizontalSplitterNeedToRedraw then exit;
  theDC := getDC(0);
  patBlt(theDC, self.clientOrigin.x + horizontalSplitter.left,
      self.horizontalSplitterLastDrawPos, horizontalSplitter.width, 1, dstInvert);
  releaseDC(0, theDC);
  self.horizontalSplitterNeedToRedraw := false;
  end;

procedure TTdoEditorForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 456;
    ptMinTrackSize.y := 260;
    end;
  end;

procedure TTdoEditorForm.fillTrianglesClick(Sender: TObject);
  begin
  if not fillTriangles.checked then
    begin
    drawLines.checked := true;
    drawLines.enabled := false;
    end
  else
    drawLines.enabled := true;
  if internalChange then exit;
  self.updateForChangeToTdo;
  end;

procedure TTdoEditorForm.mirrorHalfClick(Sender: TObject);
  begin
  self.updateForChangeToTdo;
  end;

procedure TTdoEditorForm.drawLinesClick(Sender: TObject);
  begin
  if internalChange then exit;
  self.updateForChangeToTdo;
  end;

procedure TTdoEditorForm.plantPartsChange(Sender: TObject);
  begin
  if internalChange then exit;
  self.updateForChangeToTdo;
  end;

procedure TTdoEditorForm.circlePointSizeChange(Sender: TObject);
  begin
  if internalChange then exit;
  pointRadius := circlePointSize.value div 2;
  self.updateForChangeToTdo;
  end;

procedure TTdoEditorForm.connectionPointChange(Sender: TObject);
  var
    oldPoint, newPoint: TPoint;
  begin
  if internalChange then exit;
  // adjust drawing point so 3D object does not move
  if connectionPoint.value - 1 <> tdo.originPointIndex then
    begin
    if (tdo.originPointIndex >= 0) and (tdo.originPointIndex <= numEditPoints - 1) then
      oldPoint := editPoints[tdo.originPointIndex]
    else
      oldPoint := Point(0, 0);
    if (connectionPoint.value - 1 >= 0) and (connectionPoint.value - 1 <= numEditPoints - 1) then
      newPoint := editPoints[connectionPoint.value - 1]
    else
      newPoint := Point(0, 0);
    editPaintBox.drawPosition.x := editPaintBox.drawPosition.x + (newPoint.x - oldPoint.x);
    editPaintBox.drawPosition.y := editPaintBox.drawPosition.y + (newPoint.y - oldPoint.y);
    end;
  tdo.setOriginPointIndex(connectionPoint.value - 1);
  if editPaintBox <> nil then editPaintBox.paint;
  self.updateForChangeToConnectionPointIndex;
  end;

{ ------------------------------------------------------------------------ *commands }
procedure TTdoEditorForm.doCommand(command: PdCommand);
	begin
  commandList.doCommand(command);
  self.updateButtonsForUndoRedo;
  self.updateForChangeToTdo;
  end;

{ ------------------------------------------------------------------------ PdTdoCommand }
constructor PdTdoCommand.createWithTdo(aTdo: KfObject3D);
  begin
  inherited create;
  commandChangesPlantFile := false;
  tdo := aTdo;
  self.lastCommandWasApply := TdoEditorForm.lastCommandWasApply;
  self.lastCommandWasUndoApply := TdoEditorForm.lastCommandWasUndoApply;
  end;

procedure PdTdoCommand.doCommand;
  begin
  inherited doCommand;
  TdoEditorForm.lastCommandWasApply := false;
  TdoEditorForm.lastCommandWasUndoApply := false;
  end;

procedure PdTdoCommand.undoCommand;
  begin
  inherited undoCommand;
  TdoEditorForm.lastCommandWasApply := self.lastCommandWasApply;
  TdoEditorForm.lastCommandWasUndoApply := self.lastCommandWasUndoApply;
  end;

{ -------------------------------------------------------------------- PdDragTdoPointCommand }
constructor PdDragTdoPointCommand.createWithTdoAndScale(aTdo: KfObject3D; aScale: single);
  begin
  inherited createWithTdo(aTdo);
  scale := aScale;
  end;

function PdDragTdoPointCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand;
  begin
  result := self;
  if aTrackPhase = trackPress then
  	begin
    movingPointIndex := TdoEditorForm.pointIndexAtMouse(nextPoint.x, nextPoint.y);
    TdoEditorForm.draggingPoint := true;
    TdoEditorForm.pointIndexBeingDragged := movingPointIndex;
    if movingPointIndex < 0 then
      begin
      result := nil;
      self.free;
      end
    else
      begin
      dragStartPoint := nextPoint;
      oldPoint3D := tdo.points[movingPointIndex];
      newPoint3D := oldPoint3D;
      end;
    end
  else if aTrackPhase = trackMove then
  	begin
    if rightButtonDown then
      newPoint3D.z := oldPoint3D.z - (nextPoint.y - dragStartPoint.y) / scale
    else
      begin
      newPoint3D.x := oldPoint3D.x + (nextPoint.x - dragStartPoint.x) / scale;
      newPoint3D.y := oldPoint3D.y + (nextPoint.y - dragStartPoint.y) / scale;
      end;
    tdo.points[movingPointIndex] := newPoint3D;
  	end
  else if aTrackPhase = trackRelease then
  	begin
    if not mouseDidMove then
      begin
      result := nil;
      self.free;
      end;
  	end;
	end;

procedure PdDragTdoPointCommand.undoCommand;
  begin
  inherited undoCommand;
  tdo.points[movingPointIndex] := oldPoint3D;
  end;

procedure PdDragTdoPointCommand.redoCommand;
  begin
  inherited doCommand;
  tdo.points[movingPointIndex] := newPoint3D;
  end;

function PdDragTdoPointCommand.description: string;
  begin
  result := 'drag';
  end;

{ --------------------------------------------------------------------------- PdRenameTdoCommand }
constructor PdRenameTdoCommand.createWithTdoAndNewName(aTdo: KfObject3D; aName: string);
  begin
  inherited createWithTdo(aTdo);
  oldName := tdo.getName;
  newName := aName;
  end;

procedure PdRenameTdoCommand.doCommand;
  begin
  tdo.setName(newName);
  TdoEditorForm.updateCaptionForNewTdoName;
  inherited doCommand;
  end;

procedure PdRenameTdoCommand.undoCommand;
  begin
  tdo.setName(oldName);
  TdoEditorForm.updateCaptionForNewTdoName;
  inherited undoCommand;
  end;

function PdRenameTdoCommand.description: string;
  begin
  result := 'rename';
  end;

{ ------------------------------------------------------------------------ PdReplaceTdoCommand }
constructor PdReplaceTdoCommand.createWithTdo(aTdo: KfObject3D);
  begin
  inherited createWithTdo(aTdo);
  oldTdo := KfObject3D.create;
  newTdo := KfObject3D.create;
  oldTdo.copyFrom(tdo);
  newTdo.copyFrom(tdo);
  end;

destructor PdReplaceTdoCommand.destroy;
  begin
  oldTdo.free;
  oldTdo := nil;
  newTdo.free;
  newTdo := nil;
  inherited destroy;
  end;

procedure PdReplaceTdoCommand.undoCommand;
  begin
  inherited undoCommand;
  tdo.copyFrom(oldTdo);
  TdoEditorForm.updateForChangeToTdo; // v1.6
  end;

procedure PdReplaceTdoCommand.redoCommand;
  begin
  inherited doCommand;
  tdo.copyFrom(newTdo);
  TdoEditorForm.updateForChangeToTdo;  // v1.6
  end;

{ -------------------------------------------------------------------- PdAddTdoTriangleCommand }
constructor PdAddTdoTriangleCommand.createWithTdoAndNewPoints(aTdo: KfObject3D;
      aNewPointIndexes: array of smallint; aNewPoints: array of KfPoint3D);
  var
    i: smallint;
  begin
  inherited createWithTdo(aTdo);
  for i := 0 to 2 do
    begin
    newPointIndexes[i] := aNewPointIndexes[i];
    newPoints[i] := aNewPoints[i];
    end;
  end;

procedure PdAddTdoTriangleCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand;
  for i := 0 to 2 do
    if newPointIndexes[i] < 0 then
      newPointIndexes[i] := newTdo.addPoint(newPoints[i]) - 1;
  newTriangle := KfIndexTriangle.createABC(newPointIndexes[0]+1, newPointIndexes[1]+1, newPointIndexes[2]+1);
  newTdo.triangles.add(newTriangle); {newTdo will free newTriangle}
  tdo.copyFrom(newTdo);
  TdoEditorForm.updateForChangeToNumberOfPoints;
  end;

procedure PdAddTdoTriangleCommand.undoCommand;
  begin
  inherited undoCommand;
  TdoEditorForm.updateForChangeToNumberOfPoints;
  end;

procedure PdAddTdoTriangleCommand.redoCommand;
  begin
  inherited redoCommand;
  TdoEditorForm.updateForChangeToNumberOfPoints;
  end;

function PdAddTdoTriangleCommand.description: string;
  begin
  result := 'add';
  end;

{ ----------------------------------------------------------------------- PdRemoveTdoTriangleCommand }
procedure PdRemoveTdoTriangleCommand.doCommand;
  begin
  inherited doCommand;
  TdoEditorForm.updateForChangeToNumberOfPoints;
  end;

procedure PdRemoveTdoTriangleCommand.undoCommand;
  begin
  inherited undoCommand;
  TdoEditorForm.updateForChangeToNumberOfPoints;
  end;

procedure PdRemoveTdoTriangleCommand.redoCommand;
  begin
  inherited redoCommand;
  TdoEditorForm.updateForChangeToNumberOfPoints;
  end;

destructor PdRemoveTdoTriangleCommand.destroy;
  begin
  { since triangle was removed from, not added to, newTdo, we must free it ourselves }
  if self.done then
    triangle.free;
  triangle := nil;
  inherited destroy;
  end;

function PdRemoveTdoTriangleCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand;
  var
    triangleInTdo: KfIndexTriangle;
    index: smallint;
  begin
  result := self;
  if aTrackPhase = trackPress then
  	begin
    end
  else if aTrackPhase = trackMove then
  	begin
  	end
  else if aTrackPhase = trackRelease then
  	begin
    triangleInTdo := TdoEditorForm.triangleAtMouse(nextPoint.x, nextPoint.y);
    index := tdo.triangles.indexOf(triangleInTdo);
    if (index >= 0) and (index <= newTdo.triangles.count - 1) then
      begin
      triangle := KfIndexTriangle(newTdo.triangles.items[index]);
      newTdo.removeTriangle(triangle); {we will free triangle}
      tdo.copyFrom(newTdo);
      end
    else
      begin
      result := nil;
      self.free;
      end;
  	end;
	end;

function PdRemoveTdoTriangleCommand.description: string;
  begin
  result := 'delete';
  end;

{ -------------------------------------------------------------------- PdMirrorTdoCommand }
procedure PdMirrorTdoCommand.doCommand;
  begin
  newTdo.makeMirrorTriangles;
  tdo.copyFrom(newTdo);
  inherited doCommand;
	end;

function PdMirrorTdoCommand.description: string;
  begin
  result := 'mirror';
  end;

{ -------------------------------------------------------------------- PdReverseZValuesTdoCommand }
procedure PdReverseZValuesTdoCommand.doCommand;
  begin
  newTdo.reverseZValues;
  tdo.copyFrom(newTdo);
  inherited doCommand;
	end;

function PdReverseZValuesTdoCommand.description: string;
  begin
  result := 'reverse';
  end;

{ -------------------------------------------------------------------- PdClearAllPointsCommand }
procedure PdClearAllPointsCommand.doCommand;
  begin
  newTdo.clearPoints;
  tdo.copyFrom(newTdo);
  inherited doCommand;
	end;

function PdClearAllPointsCommand.description: string;
  begin
  result := 'clear';
  end;

{ -------------------------------------------------------------------- PdLoadTdoFromDXFCommand }
constructor PdLoadTdoFromDXFCommand.createWithOldAndNewTdo(anOldTdo, aNewTdo: KfObject3D);
  begin
  inherited createWithTdo(anOldTdo);
  oldTdo := KfObject3D.create;
  newTdo := KfObject3D.create;
  oldTdo.copyFrom(anOldTdo);
  newTdo.copyFrom(aNewTdo);
  end;

procedure PdLoadTdoFromDXFCommand.doCommand;
  begin
  tdo.copyFrom(newTdo);
  TdoEditorForm.updateCaptionForNewTdoName;
  TdoEditorForm.centerDrawingClick(TdoEditorForm); //v1.6b1
  inherited doCommand;
	end;

procedure PdLoadTdoFromDXFCommand.undoCommand;
  begin
  inherited undoCommand;
  TdoEditorForm.updateCaptionForNewTdoName;
  TdoEditorForm.centerDrawingClick(TdoEditorForm); //v1.6b1
  end;

procedure PdLoadTdoFromDXFCommand.redoCommand;
  begin
  inherited redoCommand;
  TdoEditorForm.updateCaptionForNewTdoName;
  TdoEditorForm.centerDrawingClick(TdoEditorForm); //v1.6b1
  end;

function PdLoadTdoFromDXFCommand.description: string;
  begin
  result := 'DXF';
  end;

end.

