unit upp_rea;

interface

uses ExtCtrls, Classes, StdCtrls, Controls, WinTypes, Graphics, WinProcs, Messages,
    uplant, uparams, uppanel, usliders;

const
  kItemSlider = 1;
  kItemValueText = 2;
  kItemUnitText = 3;

type
  PdRealParameterPanel = class(PdParameterPanel)
	public
  currentValue, currentValueWhileSliding: single;
  minValue: single;
  maxValue: single;
  slider: KfSlider;
  currentUnitIndex: integer;
  valueTextRect: TRect;
  unitTextRect: TRect;
  minTextRect: TRect;
  maxTextRect: TRect;
  drawWithoutBounds: boolean;
  arrayIndex: smallint;
  procedure initialize; override;
	procedure updateEnabling; override;
  procedure updatePlantValues; override;
  procedure updateCurrentValue(aFieldIndex: integer); override;
  procedure updateDisplay; override;
  procedure sliderMouseDown(Sender: TObject);
  procedure sliderMouseMove(Sender: TObject);
  procedure sliderMouseUp(Sender: TObject);
  procedure sliderKeyDown(sender: TOBject);
  function sliderPositionFromValue(value: single): integer;
  function valueFromSliderPosition: single;
  function minWidth(requestedWidth: integer): integer; override;
  function maxWidth: integer; override;
  function uncollapsedHeight: integer; override;
  procedure resizeElements; override;
  procedure paint; override;
  function maxSelectedItemIndex: integer; override;
  function nextSelectedItemIndex(goForward: boolean): integer; override;
  procedure doKeyDown(sender: TObject; var key: word; shift: TShiftState); override;
  procedure doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer); override;
  procedure adjustValue;
  procedure selectNextUnitInSet(shift, ctrl: boolean);
  function checkValueAgainstBounds(aValue: single): boolean;
  function toPlantUnit(value: single): single;
  function toCurrentUnit(value: single): single;
  end;

implementation

uses SysUtils, Dialogs, Forms,
  umain, updcom, umath, uunits, usupport, udomain, udebug;

procedure PdRealParameterPanel.initialize;
	begin
	{assuming slider will be deleted automatically by owner - self - otherwise would have destructor}
	slider := KfSlider.create(self);
  slider.parent := self;
  slider.FOnMouseDown := self.sliderMouseDown;
  slider.FOnMouseMove := self.sliderMouseMove;
  slider.FOnMouseUp := self.sliderMouseUp;
  slider.FOnKeyDown := self.sliderKeyDown;
  slider.maxValue := 100; { make it a percentage move }
  slider.minValue := 0;
  slider.readOnly := param.readOnly;
  slider.useDefaultSizeAndDraggerSize;
  arrayIndex := kNotArray;
  if domain.options.useMetricUnits then
    currentUnitIndex := param.unitMetric
  else
    currentUnitIndex := param.unitEnglish;
  minValue := param.lowerBound;
  maxValue := param.upperBound;
  end;

procedure PdRealParameterPanel.adjustValue;
  var
    newString: ansistring;
    oldValueInCurrentUnit, newValue, newValueInPlantUnit: single;
    oldString, prompt, nameString, unitString, minString, maxString: string;
    outOfRange: boolean;
  begin
  oldValueInCurrentUnit := toCurrentUnit(currentValue);
  newString := digitValueString(oldValueInCurrentUnit);
  oldString := newString;
  nameString := copy(self.caption, 1, 30);
  if length(nameString) = 30 then nameString := nameString + '...';
  unitString := UnitStringForEnum(param.unitSet, currentUnitIndex);
  minString :=  digitValueString(toCurrentUnit(minValue));
  maxString := digitValueString(toCurrentUnit(maxValue));
  prompt := 'Type a new value.';
  if inputQuery('Enter value', prompt, newString) then
    if (newString <> oldString) and (boundForString(newString, param.fieldType, newValue)) then
      begin
      newValueInPlantUnit := toPlantUnit(newValue);
      outOfRange := self.checkValueAgainstBounds(newValueInPlantUnit);
      if not outOfRange then
        begin
        currentValue := newValueInPlantUnit;
        MainForm.doCommand(
          PdChangeRealValueCommand.createCommandWithListOfPlants(
            MainForm.selectedPlants, currentValue, param.fieldNumber, arrayIndex, param.regrow));
        self.updateDisplay;
        self.invalidate;
        end;
      end;
  end;

function PdRealParameterPanel.toPlantUnit(value: single): single;
  begin
  result := Convert(param.unitSet, currentUnitIndex, param.unitModel, value);
  end;

function PdRealParameterPanel.toCurrentUnit(value: single): single;
  begin
  result := Convert(param.unitSet, param.unitModel, currentUnitIndex, value);
  end;

function PdRealParameterPanel.checkValueAgainstBounds(aValue: single): boolean;
  begin
  result := (aValue < minValue) or (aValue > maxValue);
  end;

procedure PdRealParameterPanel.selectNextUnitInSet(shift, ctrl: boolean);
  begin
    if shift then
      currentUnitIndex := GetPreviousUnitEnumInUnitSet(param.unitSet, currentUnitIndex)
    else
      currentUnitIndex := GetNextUnitEnumInUnitSet(param.unitSet, currentUnitIndex);
    self.updateCurrentValue(-1);
    self.updateDisplay;
    self.invalidate;
  end;

procedure PdRealParameterPanel.doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
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
    end
  else if ptInRect(unitTextRect, thePoint) then
    begin
    self.selectedItemIndex := kItemUnitText;
    self.invalidate;
    self.selectNextUnitInSet(ssShift in shift, ssCtrl in shift);
    end;
  end;

procedure PdRealParameterPanel.doKeyDown(sender: TObject; var key: word; shift: TShiftState);
  begin
  { process slider arrow keys first }
  if slider.enabled and not slider.readOnly then
    case key of
      VK_HOME, VK_END, VK_DOWN, VK_LEFT, VK_UP, VK_RIGHT, VK_NEXT, VK_PRIOR:
        if (self.selectedItemIndex = kItemSlider) then
          begin
          slider.doKeyDown(sender, key, shift);
          exit;
          end;
        end;
  inherited doKeyDown(sender, key, shift);
  if (key = VK_RETURN) then
    case self.selectedItemIndex of
      kItemSlider: if slider.enabled and not slider.readOnly then slider.doKeyDown(sender, key, shift);
      kItemValueText: if slider.enabled and not slider.readOnly then self.adjustValue;
      kItemUnitText:  self.selectNextUnitInSet(ssShift in shift, ssCtrl in shift);
      end;
  end;

function PdRealParameterPanel.sliderPositionFromValue(value: single): integer;
  begin
  if maxValue - minValue = 0.0 then
    result := 0
  else if value <= minValue then
    result := 0
  else if value >= maxValue then
    result := 100
  else result := round(100.0 * (value - minValue) / (maxValue - minValue));
  end;

function PdRealParameterPanel.valueFromSliderPosition: single;
  var
    sliderPosition: single;
  begin
  sliderPosition := slider.currentValue;
  result := minValue
    + sliderPosition / 100.0 * (maxValue - minValue);
  end;

procedure PdRealParameterPanel.updateEnabling;
	begin
  inherited updateEnabling;
  slider.enabled := plant <> nil;
  slider.readOnly := self.readOnly;
  end;

procedure PdRealParameterPanel.updatePlantValues;
  var oldValue: single;
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

procedure PdRealParameterPanel.updateCurrentValue(aFieldIndex: integer);
	begin
  if (plant <> nil) and (param.fieldType = kFieldFloat) then
    begin
    plant.transferField(kGetField, currentValue, param.fieldNumber, kFieldFloat, arrayIndex, false, nil);
    if currentValue < minValue then currentValue := minValue;
    if currentValue > maxValue then currentValue := maxValue;
    end
  else
    currentValue := 0.0;
  end;

procedure PdRealParameterPanel.updateDisplay;
	begin
  if (plant <> nil) and (param.fieldType = kFieldFloat) then
    slider.currentValue := self.sliderPositionFromValue(currentValue)
  else
    begin
    slider.currentValue := 0;
    slider.enabled := false;
    end;
  end;

procedure PdRealParameterPanel.sliderMouseDown(Sender: TObject);
  begin
  if plant = nil then exit;
  self.selectedItemIndex := kItemSlider;
  slider.hasUnofficialFocus := true;
  currentValueWhileSliding := self.valueFromSliderPosition;
  self.invalidate;
  if not self.focused then self.setFocus;
  end;

procedure PdRealParameterPanel.sliderMouseMove(Sender: TObject);
  begin
  if plant = nil then exit;
  currentValueWhileSliding := self.valueFromSliderPosition;
  self.invalidate;
  end;

procedure PdRealParameterPanel.sliderMouseUp(Sender: TObject);
	begin
  if plant = nil then exit;
  currentValue := self.valueFromSliderPosition;
  MainForm.doCommand(
    PdChangeRealValueCommand.createCommandWithListOfPlants(
      MainForm.selectedPlants, currentValue, param.fieldNumber, arrayIndex, param.regrow));
  self.invalidate;
  end;

procedure PdRealParameterPanel.sliderKeyDown(Sender: TObject);
  begin
  self.sliderMouseUp(sender);
  end;

function PdRealParameterPanel.maxWidth: integer;
  begin
  result := intMax(kLeftRightGap * 2 + self.labelWidth,
    self.minScaleWidthWithBounds(param.unitSet, param.unitModel, minValue, maxValue));
  end;

function PdRealParameterPanel.minWidth(requestedWidth: integer): integer;
  var
    widthForLongestWord, widthWithBounds, widthWithoutBounds: integer;
  begin
  { 1. test if width given is less than labelWidth.
       if not, move on
       if so, test if width given is less than width of longest full word in labelWidth.
         if not, move on
         if so, give back width of longest full word in labelWidth as minWidth.
    2. test if width given is less than minScaleWidthWithBounds.
       if not, move on (set flag to draw bounds)
       if so, test if width given is less than minScaleWidthWithoutBounds.
         if not, move on (set flag to not draw bounds)
         if so, give back minScaleWidthWithoutBounds as minWidth.
  }
  widthForLongestWord := kLeftRightGap * 2 + self.longestLabelWordWidth;
  widthWithBounds := self.minScaleWidthWithBounds(param.unitSet, param.unitModel, minValue, maxValue);
  widthWithoutBounds := self.minScaleWidthWithoutBounds(param.unitSet, param.unitModel);
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

function PdRealParameterPanel.uncollapsedHeight: integer;
  begin
  result := self.collapsedHeight + self.textHeight + kTopBottomGap;
  end;

procedure PdRealParameterPanel.resizeElements;
  begin
  self.paint;
	slider.left := minTextRect.right + kSliderSpaceGap;
	slider.top := self.collapsedHeight + self.textHeight div 2 - slider.height div 2;
  slider.width := intMax(0, maxTextRect.left - minTextRect.right - kSliderSpaceGap * 2);
  end;

function PdRealParameterPanel.maxSelectedItemIndex: integer;
  begin
  if (not param.collapsed) and (plant <> nil) then
    result := kItemUnitText
  else
    result := kItemLabel;
  end;

function PdRealParameterPanel.nextSelectedItemIndex(goForward: boolean): integer;
  begin
  result := kItemNone;
  case self.selectedItemIndex of
    kItemNone: result := self.selectedItemIndex;
    kItemLabel:
      if goForward then result := kItemValueText else result := kItemNone;
    kItemSlider:
      if goForward then result := kItemNone else result := kItemUnitText;
    kItemValueText:
      if goForward then result := kItemUnitText else result := kItemLabel;
    kItemUnitText:
      if goForward then result := kItemSlider else result := kItemValueText;
    end;
  end;

procedure PdRealParameterPanel.Paint;
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
    self.drawExtraValueCaptionWithString(digitValueString(toCurrentUnit(currentValue)),
      UnitStringForEnum(param.unitSet, currentUnitIndex));
    exit;
    end;
  rect := getClientRect;
  minString := digitValueString(toCurrentUnit(minValue));
  maxString := digitValueString(toCurrentUnit(maxValue));
  if slider.dragging then
    valueString := digitValueString(toCurrentUnit(currentValueWhileSliding))
  else
    valueString := digitValueString(toCurrentUnit(currentValue));
  unitString := UnitStringForEnum(param.unitSet, currentUnitIndex);
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
    self.drawText(unitString, unitTextRect, true, (self.selectedItemIndex = kItemUnitText), false);
    self.drawText(maxString, maxTextRect, false, false, true);
    end;
  end;

end.
