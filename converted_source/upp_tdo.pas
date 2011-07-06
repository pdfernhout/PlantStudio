unit upp_tdo;

interface

uses ExtCtrls, Classes, StdCtrls, Controls, WinTypes, WinProcs, Graphics, Messages,
    uplant, uparams, uppanel, utdo, uturtle;

const
  kItemFileName = 1;
  kItemTdo = 2;
  kItemTurnLeft = 3;  {<}
  kItemTurnRight = 4; {>}
  kItemEnlarge = 5;   {+}
  kItemReduce = 6;    {-}
  kTdoSize = 64;

type
  PdTdoParameterPanel = class(PdParameterPanel)
	public
  tdo: KfObject3D;
  fileNameRect, tdoRect, turnLeftRect, turnRightRect, enlargeRect, reduceRect: TRect;
  rotateAngle: integer;
  scale: single;
  position: TPoint;
  editEnabled: boolean;
  movingTdo: boolean;
  moveStart, moveStartPosition: TPoint;
  constructor create(anOwner: TComponent); override;
  destructor destroy; override;
  procedure initialize; override;
	procedure updateEnabling; override;
  procedure updatePlantValues; override;
  procedure updateCurrentValue(aFieldIndex: integer); override;
  procedure updateDisplay; override;
  function minWidth(requestedWidth: integer): integer; override;
  function maxWidth: integer; override;
  function uncollapsedHeight: integer; override;
  procedure resizeElements; override;
  procedure paint; override;
  procedure doMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer); override;
  procedure doMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer); override;
  procedure doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer); override;
  procedure doKeyDown(sender: TObject; var key: word; shift: TShiftState); override;
  function maxSelectedItemIndex: integer; override;
  procedure pickTdo;
  procedure drawTdo;
  procedure recenterTdo;
  end;

implementation

uses SysUtils, Dialogs, Forms,
  updcom, umath, uunits, usupport, udomain, udebug, utdoedit, upicktdo, ubmpsupport;

constructor PdTdoParameterPanel.create(anOwner: TComponent);
  begin
  inherited create(anOwner);
  tdo := KfObject3d.create;
  end;

destructor PdTdoParameterPanel.destroy;
  begin
  tdo.free;
  tdo := nil;  
  end;

procedure PdTdoParameterPanel.initialize;
	begin
  rotateAngle := 0;
  scale := 0.2;
  position := Point(0, 0);
  movingTdo := false;
  end;

procedure PdTdoParameterPanel.updateEnabling;
	begin
  inherited updateEnabling;
  if (plant = nil) or (self.readOnly) then
    editEnabled := false
  else
    editEnabled := true;
  end;

procedure PdTdoParameterPanel.updatePlantValues;
  begin
  { this won't ever be changed by the simulation, so don't respond }
  end;

procedure PdTdoParameterPanel.updateCurrentValue(aFieldIndex: integer);
	begin
  if (plant <> nil) and (param.fieldType = kFieldThreeDObject) then
    begin
    plant.transferField(kGetField, tdo, param.fieldNumber, kFieldThreeDObject, kNotArray, false, nil);
    self.recenterTdo;
    end
  else
    editEnabled := false;
  end;

procedure PdTdoParameterPanel.updateDisplay;
	begin
  if (plant <> nil) and (param.fieldType = kFieldThreeDObject) then
    self.invalidate
  else
    editEnabled := false;
  end;

procedure PdTdoParameterPanel.doMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    thePoint: TPoint;
  begin
  if Application.terminated then exit;
  { must always call this first because it sets the focus }
  inherited doMouseDown(sender, button, shift, x, y);
  if (editEnabled) then
    begin
    thePoint := Point(x, y);
    if ptInRect(tdoRect, thePoint) and (ssCtrl in shift) then //(button = mbRight) then
      begin
      movingTdo := true;
      moveStart := thePoint;
      moveStartPosition := position;
      end;
    end;
  end;

procedure PdTdoParameterPanel.doMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
  begin
  if movingTdo then
    begin
    self.position.x := self.moveStartPosition.x + (x - moveStart.x);
    self.position.y := self.moveStartPosition.y + (y - moveStart.y);
    self.invalidate;
    end;
  end;

procedure PdTdoParameterPanel.doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    thePoint: TPoint;
  begin
  if Application.terminated then exit;
  inherited doMouseUp(sender, button, shift, x, y);
  if (editEnabled) then
    begin
    thePoint := Point(x, y);
    if ptInRect(fileNameRect, thePoint) then
      begin
      self.selectedItemIndex := kItemFileName;
      self.pickTdo;
      end
    else if ptInRect(tdoRect, thePoint) then
      begin
      self.selectedItemIndex := kItemTdo;
      if movingTdo then
        begin
        movingTdo := false;
        self.position.x := self.moveStartPosition.x + (x - moveStart.x);
        self.position.y := self.moveStartPosition.y + (y - moveStart.y);
        moveStart := point(0,0);
        self.invalidate;
        end
      else if button = mbLeft then
        self.pickTdo;
      end
    else if ptInRect(turnLeftRect, thePoint) then
      begin
      self.selectedItemIndex := kItemTurnLeft;
      rotateAngle := rotateAngle + 10;
      end
    else if ptInRect(turnRightRect, thePoint) then
      begin
      self.selectedItemIndex := kItemTurnRight;
      rotateAngle := rotateAngle - 10;
      end
    else if ptInRect(enlargeRect, thePoint) then
      begin
      self.selectedItemIndex := kItemEnlarge;
      scale := scale + 0.1;
      self.recenterTdo;
      end
    else if ptInRect(reduceRect, thePoint) then
      begin
      self.selectedItemIndex := kItemReduce;
      scale := scale - 0.1;
      self.recenterTdo;
      end;
    self.invalidate;
    end;
  end;

procedure PdTdoParameterPanel.doKeyDown(sender: TObject; var key: word; shift: TShiftState);
  begin
  if Application.terminated then exit;
  inherited doKeyDown(sender, key, shift);
  if (key = VK_RETURN) and (editEnabled) then
    begin
    case self.selectedItemIndex of
      kItemFileName: self.pickTdo;
      kItemTdo: self.pickTdo;
      end;
    end;
  end;

procedure PdTdoParameterPanel.pickTdo;
  var
    tdoPicker: TPickTdoForm;
    plantName: string;
  begin
  if (tdo = nil) or (plant = nil) or (param = nil) then exit;
  tdoPicker := TPickTdoForm.create(self);
  if tdoPicker = nil then
    raise Exception.create('Problem: Could not create 3D object chooser window.');
  try
    plantName := plant.getName;
    if tdoPicker.initializeWithTdoParameterAndPlantName(self.tdo, self.param, plantName) then
      // if false, user canceled picking a 3D object library
      tdoPicker.showModal;
  finally
    tdoPicker.free;
    tdoPicker := nil;
  end;
  end;

function PdTdoParameterPanel.maxWidth: integer;
  begin
  result := intMax(kLeftRightGap * 2 + self.labelWidth,
    kLeftRightGap + self.formTextWidth('wwwwwwww.www') + kLeftRightGap + kTdoSize + kLeftRightGap);
  end;

function PdTdoParameterPanel.minWidth(requestedWidth: integer): integer;
  var minAllowed: integer;
  begin
  minAllowed := kLeftRightGap * 2 + intMax(self.longestLabelWordWidth,
      self.formTextWidth('wwwwwwww.www') + kBetweenGap + kTdoSize);
  if requestedWidth > minAllowed then
    result := -1
  else
    result := minAllowed;
  end;

function PdTdoParameterPanel.uncollapsedHeight: integer;
  begin
  result := self.collapsedHeight + kTdoSize + kBetweenGap + self.textHeight + kTopBottomGap * 3;
  end;

function PdTdoParameterPanel.maxSelectedItemIndex: integer;
  begin
  if (not param.collapsed) and (self.editEnabled) then
    result := kItemReduce
  else
    result := kItemLabel;
  end;

procedure PdTdoParameterPanel.resizeElements;
  begin
  { do nothing }
  end;

procedure PdTdoParameterPanel.paint;
  var
    rect: TRect;
  begin
  if Application.terminated then exit;
  inherited paint;
  if (param.collapsed) then
    begin
    self.drawExtraValueCaptionWithString(tdo.getName, '');
    exit;
    end;
  rect := getClientRect;
  with tdoRect do
    begin
    left := rect.left + kLeftRightGap;
    right := left + kTdoSize;
    top := self.collapsedHeight + kTopBottomGap;
    bottom := top + kTdoSize;
    end;
  with fileNameRect do
    begin
    left := tdoRect.right + kLeftRightGap;
    right := left + self.canvas.textWidth(tdo.getName);
    top := tdoRect.top + kTdoSize div 2 - self.textHeight div 2;
    bottom := top + self.textHeight;
    end;
  with turnLeftRect do
    begin
    left := tdoRect.left + (tdoRect.right - tdoRect.left) div 2
      - (self.canvas.textWidth('>') * 4 + kLeftRightGap * 3) div 2;
    right := left + self.canvas.textWidth('<');
    top := tdoRect.bottom + kBetweenGap;
    bottom := top + self.textHeight;
    end;
  with turnRightRect do
    begin
    left := turnLeftRect.right + kLeftRightGap;
    right := left + self.canvas.textWidth('>');
    top := turnLeftRect.top;
    bottom := top + self.textHeight;
    end;
  with enlargeRect do
    begin
    left := turnRightRect.right + kLeftRightGap;
    right := left + self.canvas.textWidth('+');
    top := turnLeftRect.top;
    bottom := top + self.textHeight;
    end;
  with reduceRect do
    begin
    left := enlargeRect.right + kLeftRightGap;
    right := left + self.canvas.textWidth('-');
    top := turnLeftRect.top;
    bottom := top + self.textHeight;
    end;
  with Canvas do
    begin
    if plant <> nil then
      self.drawText(tdo.getName, fileNameRect, true,
        (self.selectedItemIndex = kItemFileName) and (self.editEnabled), false);
    self.drawText('<', turnLeftRect, true, self.selectedItemIndex = kItemTurnLeft, false);
    self.drawText('>', turnRightRect, true, self.selectedItemIndex = kItemTurnRight, false);
    self.drawText('+', enlargeRect, true, self.selectedItemIndex = kItemEnlarge, false);
    self.drawText('-', reduceRect, true, self.selectedItemIndex = kItemReduce, false);
    self.drawTdo;
    if (self.selectedItemIndex <> kItemTdo) then
      begin
      pen.color := clBtnShadow;
      pen.width := 1;
      end
    else
      begin
      pen.color := clBtnText;
      pen.width := 3;
      end;
    brush.style := bsClear;
    pen.width := 1;
    rectangle(tdoRect.left - 1, tdoRect.top - 1, tdoRect.right + 1, tdoRect.bottom + 1);
    end;
end;

procedure PdTdoParameterPanel.recenterTdo;
  var
    turtle: KfTurtle;
  begin
  if plant = nil then exit;
  if tdo = nil then exit;
  turtle := KfTurtle.defaultStartUsing;
  try
    turtle.drawingSurface.pane := nil;
    turtle.reset; { must be after pane and draw options set }
    position := tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(kTdoSize, kTdoSize), scale);
  finally
    KfTurtle.defaultStopUsing;
    turtle := nil;
  end;
  end;

procedure PdTdoParameterPanel.drawTdo;
  var
    turtle: KfTurtle;
    bitmap: TBitmap;
  begin
  if plant = nil then exit;
  if tdo = nil then exit;
  { set up clipping bitmap }
  bitmap := TBitmap.create;
  bitmap.width := kTdoSize;
  bitmap.height := kTdoSize;
  bitmap.canvas.brush.color := clWhite;
  bitmap.canvas.rectangle(0, 0, bitmap.width, bitmap.height);
  { set up turtle }
  turtle := KfTurtle.defaultStartUsing;
  try
    turtle.drawingSurface.pane := bitmap.canvas;
    turtle.setDrawOptionsForDrawingTdoOnly;
    turtle.reset; { must be after pane and draw options set }
    turtle.xyz(position.x, position.y, 0);
    try
	    turtle.push;
	    turtle.rotateY(rotateAngle);
      turtle.drawingSurface.recordingStart;
      tdo.draw(turtle, scale, '', '', 0, 0);
      turtle.drawingSurface.recordingStop;
      turtle.drawingSurface.recordingDraw;
      turtle.drawingSurface.clearTriangles;
	    turtle.pop;
      except
	      on e: Exception do
          begin
          messageForExceptionType(e, 'PdTdoParameterPanel.drawTdo');
          bitmap.free;
          end;
      end;
    copyBitmapToCanvasWithGlobalPalette(bitmap, self.canvas, tdoRect);
  finally
    KfTurtle.defaultStopUsing;
    turtle := nil;
    bitmap.free;
  end;
  end;

end.
