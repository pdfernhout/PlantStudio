unit UWinSliders;

interface

uses Wintypes, WinProcs, Messages, Classes, Forms, StdCtrls, ExtCtrls, Controls,
     Graphics, SysUtils, Dialogs, Menus;

procedure KfDrawButton(aCanvas: TCanvas; aRect: TRect; selected: boolean;  enabled: boolean);

type KfWinSlider = class(TCustomControl)
	public
    draggerHeight, draggerWidth: integer;
    FMinValue: integer;
    FMaxValue: integer;
    FReadOnly: boolean;
    FCurrentValue: integer;
    dragging: boolean;
    dragStart: integer;
    originalValue: integer;
    draggerRect: TRect;
    constructor create(AnOwner: TComponent); override;
    procedure CMFocusChanged(var Message: TCMFocusChanged);  message CM_FocusChanged;
    procedure WMGetDlgCode(var Message: TWMGetDlgCode);  message WM_GETDLGCODE;
    function setValue(newValue: longint): boolean;
    procedure keyDown(var Key: word; shift: TShiftState); override;
    procedure mouseDown(Button: TMouseButton;  Shift: TShiftState;  X, Y: Integer); override;
    procedure mouseMove(Shift: TShiftState;  X, Y: Integer); override;
    procedure mouseUp(Button: TMouseButton;  Shift: TShiftState;  X, Y: Integer); override;
    procedure paint;  override;
    function pointOnDragger(x, y: longint): boolean;
    function xDistanceFromCurrentValue(distanceInPixels: longint): longint;
    procedure useDefaultSizeAndDraggerSize;
  published
    { Published declarations }
    property OnMouseDown;
    property OnMouseMove;
    property OnMouseUp;
    property OnKeyDown;
    property OnKeyUp;
    property CurrentValue: integer read FCurrentValue write FCurrentValue default 50;
    property MinValue: integer read FMinValue write FMinValue default 0;
    property MaxValue: integer read FMaxValue write FMaxValue default 100;
    property ReadOnly: boolean read FReadOnly write FReadOnly default False;
  end;

const
  kSliderHeightReadOnly = 5;
  kSliderHeightNotReadOnly = 11; { must be at least 4 more than dragger height }
  kSliderDraggerHeight = 7;  { should be odd number }
  kSliderDraggerWidth = 5;
  kSliderGrayLineThickness = 1;
  kSliderBlueLineThickness = 3;
  kSliderDefaultWidth = 20;

// PDF PORT -- not used anyway
procedure Register1;

implementation

constructor KfWinSlider.create(AnOwner: TComponent);
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
  TabStop := True;
  useDefaultSizeAndDraggerSize;
  end;

procedure KfWinSlider.useDefaultSizeAndDraggerSize;
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

procedure KfWinSlider.CMFocusChanged(var Message: TCMFocusChanged);
  begin
  inherited;
  repaint;
  end;

procedure KfWinSlider.WMGetDlgCode(var Message: TWMGetDlgCode);
  begin
  Message.result := DLGC_WANTARROWS;
  end;

{returns true if current value changed}
function KfWinSlider.setValue(newValue: longint): boolean;
  begin
  result := false;
  if newValue > maxValue then newValue := maxValue;
  if newValue < minValue then newValue := minValue;
  if newValue = currentValue then exit;
  currentValue := newValue;
  {repaint;   }
  result := true;
  end;

procedure KfWinSlider.KeyDown(var Key: word; shift: TShiftState);
  var
    newValue: longint;
  begin
  inherited;
  if not self.readOnly then
    begin
    case key of
      VK_LEFT: newValue := currentValue - 1;
      VK_RIGHT: newValue := currentValue + 1;
      VK_UP: newValue := currentValue + 1;
      VK_DOWN: newValue := currentValue - 1;
      VK_NEXT: newValue := currentValue - 5; {page up}
      VK_PRIOR: newValue := currentValue + 5; {page down}
      else
        exit;
      end;
    self.invalidate;
    self.refresh;
    self.setValue(newValue);
    end;
  end;

function KfWinSlider.pointOnDragger(x, y: longint): boolean;
  begin
  result := ptInRect(draggerRect, Point(x,y)); 
  end;

procedure KfWinSlider.mouseDown(Button: TMouseButton;  Shift: TShiftState;  X, Y: Integer);
  begin
  inherited;
  self.setFocus;
  if not self.readOnly then
    begin
    if (Button = mbLeft) {and (pointOnDragger(x, y))} then
      begin
      dragging := true;
      dragStart := x;
      originalValue := currentValue;
      end;
    self.invalidate;
    self.refresh;
    end;
  end;

procedure KfWinSlider.MouseMove(Shift: TShiftState;  X, Y: Integer);
  var
    delta, newValue, lineLength: longint;
  begin
  inherited;
  if dragging then
    begin
    delta := x - dragStart;
    {pdf fix - won't snap to grid - will just change relative...}
    lineLength := self.width - 2 * (draggerWidth div 2);
    newValue := originalValue + round(delta * (maxValue - minValue) / lineLength);
    self.invalidate;
    self.refresh;
    self.setValue(newValue);
    end;
  end;

procedure KfWinSlider.MouseUp(Button: TMouseButton;  Shift: TShiftState;  X, Y: Integer);
  begin
  inherited;
  if dragging then
    dragging := false;
  end;

function KfWinSlider.xDistanceFromCurrentValue(distanceInPixels: longint): longint;
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

procedure KfWinSlider.paint;
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
			KfDrawButton(Canvas, draggerRect, self.focused, self.enabled);
    if (self.focused) then
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

procedure Register1;
begin
  RegisterComponents('Samples', [KfWinSlider]);
end;

end.
