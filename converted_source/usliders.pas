unit Usliders;

interface

uses Wintypes, WinProcs, Messages, Classes, Forms, StdCtrls, ExtCtrls, Controls,
     Graphics, SysUtils, Dialogs, Menus;

procedure KfDrawButton(aCanvas: TCanvas; aRect: TRect; selected: boolean;  enabled: boolean);

type
  KfSlider = class(TGraphicControl)
	public
  FOnKeyDown: TNotifyEvent;
  FOnMouseDown: TNotifyEvent;
  FOnMouseMove: TNotifyEvent;
  FOnMouseUp: TNotifyEvent;
  draggerHeight, draggerWidth: longint;
  minValue, maxValue: longint;
  hasUnofficialFocus: boolean;
  readOnly: boolean;
  currentValue: longint;
  dragging: boolean;
  dragStart: longint;
  originalValue: longint;
  draggerRect: TRect;
  constructor create(AnOwner: TComponent); override;
  procedure CMFocusChanged(var Message: TCMFocusChanged);  message CM_FocusChanged;
  procedure WMGetDlgCode(var Message: TWMGetDlgCode);  message WM_GETDLGCODE;
  function setValue(newValue: longint): boolean;
  procedure doKeyDown(sender: TObject; var Key: word; shift: TShiftState);
  procedure mouseDown(Button: TMouseButton;  Shift: TShiftState;  X, Y: Integer); override;
  procedure mouseMove(Shift: TShiftState;  X, Y: Integer); override;
  procedure mouseUp(Button: TMouseButton;  Shift: TShiftState;  X, Y: Integer); override;
  procedure paint;  override;
  function pointOnDragger(x, y: longint): boolean;
  function xDistanceFromCurrentValue(distanceInPixels: longint): longint;
  procedure useDefaultSizeAndDraggerSize;
  {function valueForPosition(x: longint): longint;  }
  end;

const
  kSliderHeightReadOnly = 5;
  kSliderHeightNotReadOnly = 11; { must be at least 4 more than dragger height }
  kSliderDraggerHeight = 7;  { should be odd number }
  kSliderDraggerWidth = 5;
  kSliderGrayLineThickness = 1;
  kSliderBlueLineThickness = 3;
  kSliderDefaultWidth = 20;
  kMinDragDistance = 1;

implementation

constructor KfSlider.create(AnOwner: TComponent);
  begin
  inherited Create(AnOwner);
  width := 140;
  height := 35;
  minValue := 0;
  maxValue := 100;
  draggerHeight := kSliderDraggerHeight;
  draggerWidth := kSliderDraggerWidth;
  readOnly := false;
  currentValue := 0;
  dragging := false;
  useDefaultSizeAndDraggerSize;
  end;

procedure KfSlider.useDefaultSizeAndDraggerSize;
  begin
  { assumes that readOnly is already set, and assumes that value of readOnly will not be changed
    unless this is called again afterward }
  if readOnly then
    begin
    height := kSliderHeightReadOnly;
    width := kSliderDefaultWidth;
    draggerHeight := 0;
    draggerWidth := 0;
    end
  else
    begin
    height := kSliderHeightNotReadOnly;
    width := kSliderDefaultWidth;
    draggerHeight := kSliderDraggerHeight;
    draggerWidth := kSliderDraggerWidth;
    end;
  end;

procedure KfSlider.CMFocusChanged(var Message: TCMFocusChanged);
  begin
  inherited;
  {repaint;  }
  end;

procedure KfSlider.WMGetDlgCode(var Message: TWMGetDlgCode);
  begin
  Message.result := DLGC_WANTARROWS;
  end;

{returns true if current value changed}
function KfSlider.setValue(newValue: longint): boolean;
  begin
  result := false;
  if newValue > maxValue then newValue := maxValue;
  if newValue < minValue then newValue := minValue;
  if newValue = currentValue then exit;
  currentValue := newValue;
  {repaint;   }
  result := true;
  end;

procedure KfSlider.doKeyDown(sender: TObject; var Key: word; shift: TShiftState);
  var
    newValue: longint;
  begin
  if self.readOnly then exit;
  case key of
    VK_LEFT: newValue := currentValue - 1;
    VK_RIGHT: newValue := currentValue + 1;
    else
      newValue := currentValue;
    end;
  self.invalidate;
  self.refresh;
  if self.setValue(newValue) and Assigned(FOnKeyDown) then
  	FOnKeyDown(self);
   end;

function KfSlider.pointOnDragger(x, y: longint): boolean;
  begin
  result := ptInRect(draggerRect, Point(x,y)); 
  end;

procedure KfSlider.mouseDown(Button: TMouseButton;  Shift: TShiftState;  X, Y: Integer);
  begin
  inherited MouseDown(Button, Shift, X, Y);
  if self.readOnly then
    begin
    if assigned(FOnMouseDown) then FOnMouseDown(self);
    exit;
    end;
  if (Button = mbLeft) {and (pointOnDragger(x, y))} then
    begin
    dragging := true;
    dragStart := x;
    originalValue := currentValue;
    self.hasUnofficialFocus := true;   {pdf fix - may want to do more here}
    end;
  self.invalidate;
  self.refresh;
  if assigned(FOnMouseDown) then FOnMouseDown(self);
  end;

procedure KfSlider.MouseMove(Shift: TShiftState;  X, Y: Integer);
  var
    delta, newValue, lineLength: longint;
  begin
  inherited MouseMove(Shift, X, Y);
  if self.readOnly then exit;
  if dragging then
    begin
    delta := x - dragStart;
    {pdf fix - won't snap to grid - will just change relative...}
    lineLength := self.width - 2 * (draggerWidth div 2);
    newValue := originalValue + round(1.0 * delta * (maxValue - minValue) / lineLength);
    self.invalidate;
    self.refresh;
    if self.setValue(newValue) and assigned(FOnMouseMove) then
    	FOnMouseMove(self);
    end;
  end;

procedure KfSlider.MouseUp(Button: TMouseButton;  Shift: TShiftState;  X, Y: Integer);
  begin
  inherited MouseUp(Button, Shift, X, Y);
  if self.readOnly then exit;
  if (Button = mbLeft) and dragging then
    dragging := false;
  if abs(x - dragStart) < kMinDragDistance then exit;
  dragStart := 0;
  if Assigned(FOnMouseUp) then FOnMouseUp(Self);
  end;

function KfSlider.xDistanceFromCurrentValue(distanceInPixels: longint): longint;
  var proportion: single;
  begin
  proportion := (currentValue - minValue) / (maxValue - minValue);
  try
    result := round(proportion * distanceInPixels);
  except
    result := 0;
  end;
  end;

procedure KfDrawButton(aCanvas: TCanvas; aRect: TRect; selected: boolean;  enabled: boolean);
  var
    internalRect: TRect;
  begin
  with aCanvas do
    begin
    brush.style := bsSolid;
    if enabled then
      begin
      pen.color := clBlack;
      brush.color := clWhite;
      end
    else
      begin
      brush.color := clBtnShadow;
      pen.color := clBtnShadow;
      end;
    with aRect do rectangle(left, top, right, bottom);
    if selected then
      begin
      internalRect := aRect;
      inflateRect(internalRect, -1, -1);
      brush.color := clAqua;
      fillRect(internalRect);
      end;
    end;
  end;

procedure KfSlider.paint;
  var
    grayRect, blueRect, fullRect, lineRect: TRect;
    distance: longint;
  begin
  with Canvas do
    begin
    fullRect := self.getClientRect;
    { start with total fill }
    brush.color := clBtnFace;
    brush.style := bsSolid;
    fillRect(fullRect);
    { rect for line }
    lineRect := fullRect;
    with lineRect do
      begin
      left := left + draggerWidth div 2 + 2;
      right := right - draggerWidth div 2 - 1;
      top := top + (bottom - top) div 2 - kSliderBlueLineThickness div 2;
      bottom := top + kSliderBlueLineThickness;
      end;
    { rect for dragger }
    distance := self.xDistanceFromCurrentValue(lineRect.right - lineRect.left);
    with draggerRect do
      begin
      left := lineRect.left + distance - draggerWidth div 2 - draggerWidth mod 2;
      right := left + draggerWidth;
      top := lineRect.top - draggerHeight div 2 + kSliderBlueLineThickness div 2;
      bottom := top + draggerHeight;
      end;
    { blue rect }
    blueRect := lineRect;
    blueRect.right := blueRect.left + distance;
    { gray rect }
    grayRect := lineRect;
    grayRect.top := grayRect.top + (grayRect.bottom - grayRect.top) div 2;
    grayRect.bottom := grayRect.top + kSliderGrayLineThickness;
    if self.enabled then grayRect.left := blueRect.right + 1;
	  {draw gray line}
    brush.color := clBtnShadow;
    fillRect(grayRect);
	  {draw blue line}
    if self.enabled then
      begin
    	brush.color := clBlue;
    	fillRect(blueRect);
      end;
	  {draw dragger if not read only }
    if not self.readOnly then
			KfDrawButton(Canvas, draggerRect, self.hasUnofficialFocus, self.enabled);
    if (self.hasUnofficialFocus) then
      begin
    	pen.color := clBtnShadow;
      with fullRect do
        begin
    		moveTo(right - 1, top);
    		lineTo(left, top);
    		lineTo(left, bottom - 1);
    		lineTo(right - 1, bottom - 1);
    		lineTo(right - 1, top);
        end;
      end;
    end;
  end;

end.
