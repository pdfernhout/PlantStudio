unit upp_int;

interface

uses ExtCtrls, Classes, StdCtrls, Controls, WinTypes, Graphics, WinProcs, Messages,
    uplant, uparams, uppanel, usliders;

const
  kItemValueText = 1;
{  kItemUnitText = 2;    }
  kItemSlider = 2;

type
  PdSmallintParameterPanel = class(PdParameterPanel)
	public
  currentValue, currentValueWhileSliding: smallint;
  minValue: smallint;
  maxValue: smallint;
  slider: KfSlider;
  unitIndex: smallint;
  minTextRect, maxTextRect, valueTextRect, unitTextRect: TRect;
  drawWithoutBounds: boolean;
  procedure initialize; override;
	procedure updateEnabling; override;
  procedure updatePlantValues; override;
  procedure updateCurrentValue(aFieldIndex: integer); override;
  procedure updateDisplay; override;
  procedure sliderMouseDown(Sender: TObject);
  procedure sliderMouseMove(sender: TObject);
  procedure sliderMouseUp(Sender: TObject);
  procedure sliderKeyDown(sender: TOBject);
  function minWidth(requestedWidth: integer): integer; override;
  function maxWidth: integer; override;
  function minScaleWidthWithBounds: integer;
  function minScaleWidthWithoutBounds: integer;
  function uncollapsedHeight: integer; override;
  procedure resizeElements; override;
  procedure paint; override;
  function maxSelectedItemIndex: integer; override;
  procedure doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer); override;
  procedure doKeyDown(sender: TObject; var key: word; shift: TShiftState); override;
  function checkValueAgainstBounds(value: smallint): smallint;
  procedure adjustValue;
  end;

implementation

uses SysUtils, Dialogs, Forms,
  umain, updcom, umath, uunits, usupport, udomain, udebug;

procedure PdSmallintParameterPanel.initialize;
	begin
	{assuming slider will be deleted automatically by owner - self - otherwise would have destructor}
	slider := KfSlider.create(self);
  slider.parent := self;
  slider.FOnMouseDown := self.sliderMouseDown;
  slider.FOnMouseMove := self.sliderMouseMove;
  slider.FOnMouseUp := self.sliderMouseUp;
  slider.FOnKeyDown := self.sliderKeyDown;
  slider.readOnly := param.readOnly;
  slider.useDefaultSizeAndDraggerSize;
  minValue := round(param.lowerBound);
  maxValue := round(param.upperBound);
  slider.minValue := minValue;
  slider.maxValue := maxValue;
  end;

function PdSmallintParameterPanel.checkValueAgainstBounds(value: smallint): smallint;
  begin
  result := value;
  if result < minValue then result := minValue;
  if result > maxValue then result := maxValue;
  end;

procedure PdSmallintParameterPanel.doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    thePoint: TPoint;
  begin
  { must always call this first because it sets the focus }
  inherited doMouseUp(sender, button, shift, x, y);
  thePoint := Point(x, y);
  if ptInRect(valueTextRect, thePoint) then
    begin
    if slider.enabled and not slider.readOnly then
      begin
      self.selectedItemIndex := kItemValueText;
      self.invalidate;
      self.adjustValue;
      end;
    end;
  end;

procedure PdSmallintParameterPanel.doKeyDown(sender: TObject; var key: word; shift: TShiftState);
  begin
  { process slider arrow keys first }
  if slider.enabled then
    case key of
      VK_HOME, VK_END, VK_DOWN, VK_LEFT, VK_UP, VK_RIGHT, VK_NEXT, VK_PRIOR:
        if (self.selectedItemIndex = kItemSlider) then
          begin
          slider.doKeyDown(sender, key, shift);
          exit;
          end;
      end;
  if (self.selectedItemIndex = kItemValueText) and (key = VK_RETURN) then
    begin
    key := 0;
    self.invalidate;
    self.adjustValue;
    exit;
    end;
  inherited doKeyDown(sender, key, shift);
  if slider.enabled then if (key = VK_RETURN) and (self.selectedItemIndex = kItemSlider) then
    slider.doKeyDown(sender, key, shift);
  end;

procedure PdSmallintParameterPanel.adjustValue;
  var
    newString: ansistring;
    oldValue, newValue: smallint;
    oldString, prompt, nameString, unitString: string;
  begin
  oldValue := currentValue;
  newString := intToStr(currentValue);
  oldString := newString;
  nameString := copy(self.caption, 1, 30);
  if length(nameString) = 30 then nameString := nameString + '...';
  unitString := UnitStringForEnum(param.unitSet, unitIndex);
  prompt := 'Type a new value.';
  if inputQuery('Enter value', prompt, newString) then
    if (newString <> oldString) then
      begin
      newValue := strToIntDef(newString, 0);
      if self.checkValueAgainstBounds(newValue) = newValue then
        begin
        currentValue := newValue;
        MainForm.doCommand(
          PdChangeSmallintValueCommand.createCommandWithListOfPlants(
              MainForm.selectedPlants, currentValue, param.fieldNumber, kNotArray, param.regrow));
        self.updateDisplay;
        self.invalidate;
        end;
      end;
  end;

procedure PdSmallintParameterPanel.updateEnabling;
	begin
  inherited updateEnabling;
  slider.enabled := plant <> nil;
  slider.readOnly := self.readOnly;
  end;

procedure PdSmallintParameterPanel.updatePlantValues;
  var oldValue: integer;
  begin
  if plant = nil then exit;
  if param.collapsed then exit;
  oldValue := currentValue;
  self.updateCurrentValue(-1);
  if oldValue <> currentValue then
    begin
    updateDisplay;
    invalidate;
    end;
  end;

procedure PdSmallintParameterPanel.updateCurrentValue(aFieldIndex: integer);
	begin
  if (plant <> nil) and (param.fieldType = kFieldSmallint) then
    begin
    plant.transferField(kGetField, currentValue, param.fieldNumber, kFieldSmallint,  kNotArray, false, nil);
    if currentValue < minValue then
      begin
      minValue := currentValue;
  		slider.minValue := minValue;
      end;
    if currentValue > maxValue then
    	begin
      maxValue := currentValue;
  		slider.maxValue := maxValue;
      end;
    end
  else
    currentValue := 0;
  end;

procedure PdSmallintParameterPanel.updateDisplay;
	begin
  if (plant <> nil) and (param.fieldType = kFieldSmallint) then
    begin
    slider.currentValue := currentValue;
    end
  else
    begin
    slider.currentValue := 0;
    slider.enabled := false;
    end;
  end;

procedure PdSmallintParameterPanel.sliderMouseDown(Sender: TObject);
  begin
  if plant = nil then exit;
  self.selectedItemIndex := kItemSlider;
  slider.hasUnofficialFocus := true;
  currentValueWhileSliding := slider.currentValue;
  self.invalidate;
  if not self.focused then self.setFocus;
  end;

procedure PdSmallintParameterPanel.sliderMouseMove(Sender: TObject);
  begin
  if plant = nil then exit;
  currentValueWhileSliding := slider.currentValue;
  self.invalidate;
  end;

procedure PdSmallintParameterPanel.sliderMouseUp(Sender: TObject);
	begin
  if plant <> nil then
    begin
  	currentValue := slider.currentValue;
    MainForm.doCommand(
      PdChangeSmallintValueCommand.createCommandWithListOfPlants(
        MainForm.selectedPlants, currentValue, param.fieldNumber, kNotArray, param.regrow));
    self.updateDisplay;
    self.invalidate;
    end
  else
    begin
    slider.currentValue := 0;
    slider.enabled := false;
    end;
  end;

procedure PdSmallintParameterPanel.sliderKeyDown(sender: TOBject);
  begin
  self.sliderMouseUp(sender);
  end;

function PdSmallintParameterPanel.maxWidth: integer;
  begin
  result := kLeftRightGap * 2 + intMax(self.labelWidth, minScaleWidthWithBounds);
  end;

function PdSmallintParameterPanel.minWidth(requestedWidth: integer): integer;
  var 
    widthForLongestWord, widthWithBounds, widthWithoutBounds: integer;
  begin
  widthForLongestWord := kLeftRightGap * 2 + self.longestLabelWordWidth;
  widthWithBounds := self.minScaleWidthWithBounds;
  widthWithoutBounds := self.minScaleWidthWithoutBounds;
  result := -1;
  if requestedWidth < widthForLongestWord then
    result := widthForLongestWord;
  if requestedWidth < widthWithBounds then
    begin
    drawWithoutBounds := true;
    if requestedWidth < widthWithoutBounds then
      result := intMax(result, widthWithoutBounds);
    end
  else
    drawWithoutBounds := false;
  end;

function PdSmallintParameterPanel.minScaleWidthWithBounds: integer;
  var
    minString, valueString, unitString, maxString: string[30];
  begin
  minString := intToStr(minValue);
  valueString := intToStr(currentValue) + '  ';
  unitString := UnitStringForEnum(param.unitSet, unitIndex);
  maxString := intToStr(maxValue);
  result := self.formTextWidth(minString + valueString + unitString + maxString)
    + kBetweenGap * 3;
  end;

function PdSmallintParameterPanel.minScaleWidthWithoutBounds: integer;
  var
    valueString, unitString: string[30];
  begin
  valueString := intToStr(currentValue) + '  ';
  unitString := UnitStringForEnum(param.unitSet, unitIndex);
  result := self.formTextWidth(valueString + unitString) + kBetweenGap;
  end;

function PdSmallintParameterPanel.uncollapsedHeight: integer;
  begin
  result := self.collapsedHeight + self.textHeight + kTopBottomGap;
  end;

procedure PdSmallintParameterPanel.resizeElements;
  begin
  self.paint;
	slider.left := minTextRect.right + kSliderSpaceGap;
	slider.top := self.collapsedHeight + self.textHeight div 2 - slider.height div 2;
  slider.width := intMax(0, maxTextRect.left - minTextRect.right - kSliderSpaceGap * 2);
  end;

function PdSmallintParameterPanel.maxSelectedItemIndex: integer;
  begin
  if (not param.collapsed) and (slider.enabled) then
    result := kItemSlider
  else
    result := kItemLabel;
  end;

procedure PdSmallintParameterPanel.Paint;
  var
    Rect: TRect;
    minString, valueString, maxString, unitString: string[30];
  begin
  if Application.terminated then exit;
  { ask slider to update itself based on whether it is selected }
  if (self.selectedItemIndex = kItemSlider) then
    slider.hasUnofficialFocus := true
  else
    slider.hasUnofficialFocus := false;
  inherited paint;
  slider.visible := not param.collapsed;
  if (param.collapsed) then
    begin
    self.drawExtraValueCaptionWithString(intToStr(currentValue),
      UnitStringForEnum(param.unitSet, unitIndex));
    exit;
    end;
  rect := getClientRect;
  minString := intToStr(minValue);
  if slider.dragging then
    valueString := intToStr(currentValueWhileSliding)
  else
    valueString := intToStr(currentValue);
  unitString := UnitStringForEnum(param.unitSet, unitIndex);
  maxString := intToStr(maxValue);
  with valueTextRect do
    begin
    left := kLeftRightGap;
    right := left + self.canvas.textWidth(valueString);
    top := self.collapsedHeight + 1;
    bottom := top + self.textHeight;
    end;
  unitTextRect := valueTextRect;
  unitTextRect.left := valueTextRect.right + 5;
  unitTextRect.right := unitTextRect.left + self.canvas.textWidth(unitString);
  minTextRect := valueTextRect;
  minTextRect.left := unitTextRect.right + 5;
  minTextRect.right := minTextRect.left + self.canvas.textWidth(minString);
  maxTextRect := valueTextRect;
  maxTextRect.right := rect.right - kLeftRightGap;
  maxTextRect.left := maxTextRect.right - self.canvas.textWidth(maxString);
  with Canvas do
    begin
    self.drawText(minString, minTextRect, false, false, true);
    self.drawText(valueString, valueTextRect, not self.readOnly, (self.selectedItemIndex = kItemValueText), false);
    self.drawText(unitString, unitTextRect, false, false, false);
    self.drawText(maxString, maxTextRect, false, false, true);
  end;
end;

end.
