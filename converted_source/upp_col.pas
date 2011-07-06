unit upp_col;

interface

uses ExtCtrls, Classes, StdCtrls, Controls, WinTypes, WinProcs, Graphics, Messages,
    uplant, uparams, uppanel, usliders;

const
  kItemColorRect = 1;
  kItemRedSlider = 2;
  kItemGreenSlider = 3;
  kItemBlueSlider = 4;
  kColorRectSize = 40;
  kMinSliderLength = 30;

type
  PdColorParameterPanel = class(PdParameterPanel)
	public
  currentColor, colorWhileDragging: TColorRef;
  redSlider: KfSlider;
  greenSlider: KfSlider;
  blueSlider: KfSlider;
  colorRect: TRect;
  procedure initialize; override;
  procedure initSlider(slider: KfSlider);
	procedure updateEnabling; override;
  procedure updatePlantValues; override;
  procedure updateCurrentValue(aFieldIndex: integer); override;
  procedure updateDisplay; override;
  procedure sliderMouseDown(Sender: TObject);
  procedure sliderMouseMove(Sender: TObject);
  procedure sliderMouseUp(Sender: TObject);
  procedure sliderKeyDown(sender: TObject);
  function minWidth(requestedWidth: integer): integer; override;
  function maxWidth: integer; override;
  function uncollapsedHeight: integer; override;
  procedure resizeElements; override;
  procedure paint; override;
  function maxSelectedItemIndex: integer; override;
  procedure doKeyDown(sender: TObject; var key: word; shift: TShiftState); override;
  procedure disableSliders;
  procedure doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer); override;
  function GetPalette: HPALETTE; override;
  procedure fillRectWithColor(aRect: TRect; aColor: TColorRef);
  end;

implementation

uses SysUtils, Dialogs, Forms,
  umain, updcom, umath, uunits, usupport, udomain, udebug, ubmpsupport;

function PdColorParameterPanel.GetPalette: HPALETTE;
  begin
  result := MainForm.paletteImage.picture.bitmap.palette;
  end;

procedure PdColorParameterPanel.initialize;
	begin
	{assuming sliders will be deleted automatically by owner - self - otherwise would have destructor}
  redSlider := KfSlider.create(self);
  self.initSlider(redSlider);
  greenSlider := KfSlider.create(self);
  self.initSlider(greenSlider);
  blueSlider := KfSlider.create(self);
  self.initSlider(blueSlider);
  self.onMouseUp := self.doMouseUp;
  end;

procedure PdColorParameterPanel.initSlider(slider: KfSlider);
  begin
  with slider do
    begin
    parent := self;
    FOnMouseDown := self.sliderMouseDown;
    FOnMouseMove := self.sliderMouseMove;
    FOnMouseUp := self.sliderMouseUp;
    FOnKeyDown := self.sliderKeyDown;
    readOnly := param.readOnly;
    useDefaultSizeAndDraggerSize;
    minValue := 0;
    maxValue := 255;
    end;
  end;

procedure PdColorParameterPanel.doKeyDown(sender: TObject; var key: word; shift: TShiftState);
  begin
  { process slider arrow keys first }
  if (plant <> nil) and (not self.readOnly) then
    case key of
    VK_HOME, VK_END, VK_DOWN, VK_LEFT, VK_UP, VK_RIGHT, VK_NEXT, VK_PRIOR, VK_RETURN:
      case self.selectedItemIndex of
        kItemRedSlider:
          begin
          redSlider.doKeyDown(sender, key, shift);
          exit;
          end;
        kItemGreenSlider:
          begin
          greenSlider.doKeyDown(sender, key, shift);
          exit;
          end;
        kItemBlueSlider:
          begin
          blueSlider.doKeyDown(sender, key, shift);
          exit;
          end;
        kItemColorRect:
          begin
          self.doMouseUp(self, mbLeft, [], colorRect.left + 1, colorRect.top + 1);
          end;
        end;
      end;
  inherited doKeyDown(sender, key, shift);
  end;

procedure PdColorParameterPanel.doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    thePoint: TPoint;
    newColor: TColorRef;
  begin
  { must always call this first because it sets the focus }
  inherited doMouseUp(sender, button, shift, x, y);
  if (plant = nil) or (self.readOnly) then exit;
  thePoint := point(x,y);
  if ptInRect(colorRect, thePoint) then
    begin
    self.selectedItemIndex := kItemColorRect;
    newColor := domain.getColorUsingCustomColors(currentColor);
    if newColor <> currentColor then
      begin
      currentColor := newColor;
      MainForm.doCommand(
        PdChangeColorValueCommand.createCommandWithListOfPlants(
          MainForm.selectedPlants, currentColor, param.fieldNumber, kNotArray, param.regrow));
      self.updateDisplay;
      self.invalidate;
      end;
    end;
  end;

procedure PdColorParameterPanel.updateEnabling;
	begin
  inherited updateEnabling;
  redSlider.enabled := plant <> nil;
  greenSlider.enabled := plant <> nil;
  blueSlider.enabled := plant <> nil;
  redSlider.readOnly := self.readOnly;
  greenSlider.readOnly := self.readOnly;
  blueSlider.readOnly := self.readOnly;
  end;

procedure PdColorParameterPanel.updatePlantValues;
  var oldColor: TColorRef;
  begin
  if plant = nil then exit;
  if param.collapsed then exit;
  oldColor := currentColor;
  self.updateCurrentValue(-1);
  if oldColor <> currentColor then
    begin
    self.updateDisplay;
    self.invalidate;
    end;
  end;

procedure PdColorParameterPanel.updateCurrentValue(aFieldIndex: integer);
	begin
  if (plant <> nil) and (param.fieldType = kFieldColor) then
    begin
    plant.transferField(kGetField, currentColor, param.fieldNumber, kFieldColor, kNotArray, false, nil);
    end
  else
    self.disableSliders;
  end;

procedure PdColorParameterPanel.disableSliders;
  begin
  redSlider.currentValue := 0;
  redSlider.enabled := false;
  greenSlider.currentValue := 0;
  greenSlider.enabled := false;
  blueSlider.currentValue := 0;
  blueSlider.enabled := false;
  end;

procedure PdColorParameterPanel.updateDisplay;
	begin
  if (plant <> nil) and (param.fieldType = kFieldColor) then
    begin
    redSlider.currentValue := getRValue(currentColor);
    greenSlider.currentValue := getGValue(currentColor);
    blueSlider.currentValue := getBValue(currentColor);
    end
  else
    self.disableSliders;
  end;

procedure PdColorParameterPanel.sliderMouseDown(Sender: TObject);
  begin
  if plant = nil then exit;
  colorWhileDragging := support_rgb(redSlider.currentValue, greenSlider.currentValue, blueSlider.currentValue);
  if sender = redSlider then
    self.selectedItemIndex := kItemRedSlider
  else if sender = greenSlider then
    self.selectedItemIndex := kItemGreenSlider
  else if sender = blueSlider then
    self.selectedItemIndex := kItemBlueSlider;
  if not self.focused then
    self.setFocus
  else
    self.invalidate;
  { paint method updates unofficial focus flags in sliders }
  end;

procedure PdColorParameterPanel.sliderMouseMove(Sender: TObject);
	begin
  if plant <> nil then
    begin
    colorWhileDragging := support_rgb(redSlider.currentValue, greenSlider.currentValue, blueSlider.currentValue);
    { don't make change permanent yet, not until mouse up }
    self.repaint;
    end
  else
    self.disableSliders;
  end;

procedure PdColorParameterPanel.sliderMouseUp(Sender: TObject);
	begin
  if plant <> nil then
    begin
    currentColor := support_rgb(redSlider.currentValue, greenSlider.currentValue, blueSlider.currentValue);
    MainForm.doCommand(
      PdChangeColorValueCommand.createCommandWithListOfPlants(
        MainForm.selectedPlants, currentColor, param.fieldNumber, kNotArray, param.regrow));
    self.updateDisplay;
    self.invalidate;
    end
  else
    self.disableSliders;
  end;

procedure PdColorParameterPanel.sliderKeyDown(sender: TOBject);
  begin
  self.sliderMouseUp(sender);
  end;

function PdColorParameterPanel.maxWidth: integer;
  begin
  result := kLeftRightGap * 2 + intMax(self.labelWidth, kEditMaxWidth);
  end;

function PdColorParameterPanel.minWidth(requestedWidth: integer): integer;
  var minAllowed: integer;
  begin
  minAllowed := kLeftRightGap * 2 + intMax(self.longestLabelWordWidth,
    kColorRectSize + kMinSliderLength + kBetweenGap);
  if requestedWidth > minAllowed then
    result := -1
  else
    result := minAllowed;
  end;

function PdColorParameterPanel.uncollapsedHeight: integer;
  begin
  result := self.collapsedHeight + intMax(redSlider.height, self.textHeight) * 3 + kBetweenGap * 2 + kTopBottomGap * 3;
  end;

procedure PdColorParameterPanel.resizeElements;
  begin
	redSlider.left := kLeftRightGap + kColorRectSize + self.formTextWidth('W') + kLeftRightGap * 2;
  redSlider.width := intMax(0, self.width - redSlider.left - kLeftRightGap);
	redSlider.top := self.collapsedHeight + kTopBottomGap + self.canvas.textHeight('r') div 2 - redSlider.height div 2;
	greenSlider.left := redSlider.left;
  greenSlider.width := redSlider.width;
	greenSlider.top := redSlider.top + self.textHeight + self.canvas.textHeight('r') div 2 - greenSlider.height div 2;
	blueSlider.left := redSlider.left;
  blueSlider.width := redSlider.width;
	blueSlider.top := greenSlider.top + self.textHeight + self.canvas.textHeight('r') div 2 - blueSlider.height div 2;
  end;

function PdColorParameterPanel.maxSelectedItemIndex: integer;
  begin
  if (not param.collapsed) and (redSlider.enabled) then
    result := kItemBlueSlider
  else
    result := kItemLabel;
  end;

procedure PdColorParameterPanel.Paint;
  var
    aRect, rTextRect, gTextRect, bTextRect, collapsedColorRect: TRect;
  begin
  if Application.terminated then exit;
  { ask sliders to update themselves based on whether they are selected }
  redSlider.hasUnofficialFocus := (self.selectedItemIndex = kItemRedSlider);
  greenSlider.hasUnofficialFocus := (self.selectedItemIndex = kItemGreenSlider);
  blueSlider.hasUnofficialFocus := (self.selectedItemIndex = kItemBlueSlider);
  inherited paint;
  aRect := getClientRect;
  if (param.collapsed) and (plant <> nil) then
    begin
    with collapsedColorRect do
      begin
      left := aRect.left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap
          + self.canvas.textWidth(self.caption) + kLeftRightGap;
      right := left + self.textHeight * 2;
      top := aRect.top + 2;
      bottom := top + self.textHeight;
      end;
    inflateRect(collapsedColorRect, -2, -2);
    self.fillRectWithColor(collapsedColorRect, currentColor);
    exit;
    end;
  with rTextRect do
    begin
    left := aRect.left + kLeftRightGap + kColorRectSize + kLeftRightGap * 2;
    right := left + self.canvas.textWidth('W');
    top := self.collapsedHeight + kTopBottomGap;
    bottom := top + self.textHeight;
    end;
  gTextRect := rTextRect;
  with gTextRect do
    begin
    top := rTextRect.bottom + kBetweenGap;
    bottom := top + self.textHeight;
    end;
  bTextRect := rTextRect;
  with bTextRect do
    begin
    top := gTextRect.bottom + kBetweenGap;
    bottom := top + self.textHeight;
    end;
  with colorRect do
    begin
    left := kLeftRightGap * 2;
    right := rTextRect.left - kLeftRightGap * 2;
    top := self.collapsedHeight + kTopBottomGap;
    bottom := self.uncollapsedHeight - kTopBottomGap * 2;
    end;
  with Canvas do
    begin
    self.drawText('r', rTextRect, false, false, false);
    self.drawText('g', gTextRect, false, false, false);
    self.drawText('b', bTextRect, false, false, false);
    if (redSlider.dragging) or (greenSlider.dragging) or (blueSlider.dragging) then
      self.fillRectWithColor(colorRect, colorWhileDragging)
    else if plant = nil then
      self.fillRectWithColor(colorRect, clBtnFace)
    else
      self.fillRectWithColor(colorRect, currentColor);
    pen.color := clBtnShadow;
    if (self.selectedItemIndex <> kItemColorRect) then
      begin
      pen.width := 1;
      pen.color := clBtnShadow;
      end
    else
      begin
      pen.width := 3;
      pen.color := clBtnHighlight;
      end;
    pen.width := 1;
    brush.style := bsClear;
    rectangle(colorRect.left - 1, colorRect.top - 1, colorRect.right + 1, colorRect.bottom + 1);
    end;
end;

procedure PdColorParameterPanel.fillRectWithColor(aRect: TRect; aColor: TColorRef);
  var
    bitmap: TBitmap;
  begin
  bitmap := TBitmap.create;
  try
    try
      bitmap.width := rWidth(aRect);
      bitmap.height := rHeight(aRect);
    except
      bitmap.width := 1;
      bitmap.height := 1;
    end;
    setPixelFormatBasedOnScreenForBitmap(bitmap);
    bitmap.canvas.brush.color := aColor;
    bitmap.canvas.fillRect(Rect(0, 0, bitmap.width, bitmap.height));
    copyBitmapToCanvasWithGlobalPalette(bitmap, self.canvas, aRect);
  finally
    bitmap.free;
  end;
  end;

end.

