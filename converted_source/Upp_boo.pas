unit upp_boo;

interface

uses ExtCtrls, Classes, StdCtrls, Controls, WinTypes, Graphics, WinProcs, Messages,
  uplant, uparams, uppanel;

const
  kItemYes = 1;
  kItemNo = 2;

type
  PdBooleanParameterPanel = class(PdParameterPanel)
	public
  currentValue: boolean;
  yesRect: TRect;
  noRect: TRect;
  editEnabled: boolean;
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
  procedure doKeyDown(sender: TObject; var key: word; shift: TShiftState); override;
  procedure negateValue;
  procedure drawRadioButton(value: boolean; enabled: boolean; rect: TRect);
  function maxSelectedItemIndex: integer; override;
  end;

implementation

uses SysUtils, Dialogs, Forms,
  umain, updcom, umath, uunits, usupport, udomain, udebug;

procedure PdBooleanParameterPanel.initialize;
	begin
  currentValue := false;
  editEnabled := false;
  end;

procedure PdBooleanParameterPanel.updateEnabling;
	begin
  inherited updateEnabling;
  if (plant = nil) or (self.readOnly) then
    editEnabled := false
  else
    editEnabled := true;
  end;

procedure PdBooleanParameterPanel.updatePlantValues;
  begin
  if plant = nil then exit;
  if param.collapsed then exit;
  self.updateCurrentValue(-1);
  updateDisplay;
  invalidate;
  end;

procedure PdBooleanParameterPanel.updateCurrentValue(aFieldIndex: integer);
	begin
  if plant <> nil then
    begin
    if param.fieldType = kFieldBoolean then
      begin
      plant.transferField(kGetField, currentValue, param.fieldNumber, kFieldBoolean,  kNotArray, false, nil);
      self.updateDisplay;
      end;
    end
  else
    begin
    currentValue := false;
    editEnabled := false;
    end;
  end;

procedure PdBooleanParameterPanel.updateDisplay;
	begin
  if plant <> nil then
    begin
    if param.fieldType = kFieldBoolean then
      self.invalidate;
      end
  else
    editEnabled := false;
  end;

procedure PdBooleanParameterPanel.doMouseDown(
    Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    thePoint: TPoint;
    newValue: boolean;
  begin
  { must always call this first because it sets the focus }
  inherited doMouseDown(sender, button, shift, x, y);
  if (editEnabled) then
    begin
    thePoint := Point(x, y);
    newValue := currentValue;
    if ptInRect(yesRect, thePoint) then
      begin
      newValue := true;
     self.selectedItemIndex := kItemYes;
      end
    else if ptInRect(noRect, thePoint) then
      begin
      newValue := false;
      self.selectedItemIndex := kItemNo;
      end;
    self.invalidate;
    if (newValue <> currentValue) then self.negateValue;
    end;
  end;

procedure PdBooleanParameterPanel.doKeyDown(sender: TObject; var key: word; shift: TShiftState);
  var newValue: boolean;
  begin
  inherited doKeyDown(sender, key, shift);
  if (key = VK_RETURN) and (editEnabled) then
    begin
    newValue := currentValue;
    case self.selectedItemIndex of
      kItemYes: newValue := true;
      kItemNo: newValue := false;
      end;
    if (newValue <> currentValue) then self.negateValue;
    end;
  end;

procedure PdBooleanParameterPanel.negateValue;
  begin
  currentValue := not currentValue;
  if plant <> nil then
    MainForm.doCommand(
      PdChangeBooleanValueCommand.createCommandWithListOfPlants(
        MainForm.selectedPlants, currentValue, param.fieldNumber, kNotArray, param.regrow));
  self.invalidate;
  end;

function PdBooleanParameterPanel.maxWidth: integer;
  begin
  result := intMax(kLeftRightGap * 2 + self.longestLabelWordWidth,
    kRadioButtonLeftGap + (yesRect.right - yesRect.left)
    + kRadioButtonBetweenGap + (noRect.right - noRect.left)
    + kLeftRightGap);
  end;

function PdBooleanParameterPanel.minWidth(requestedWidth: integer): integer;
  var minAllowed: integer;
  begin
  minAllowed := intMax(kLeftRightGap * 2 + self.longestLabelWordWidth,
    kRadioButtonLeftGap + (yesRect.right - yesRect.left)
    + kRadioButtonBetweenGap + (noRect.right - noRect.left)
    + kLeftRightGap);
  if requestedWidth > minAllowed then
    result := -1
  else
    result := minAllowed;
  end;

function PdBooleanParameterPanel.uncollapsedHeight: integer;
  begin
  result := self.collapsedHeight + self.textHeight + kTopBottomGap;
  end;

function PdBooleanParameterPanel.maxSelectedItemIndex: integer;
  begin
  if (not param.collapsed) and (self.editEnabled) then
    result := kItemNo
  else
    result := kItemLabel;
  end;

procedure PdBooleanParameterPanel.resizeElements;
  begin
  { do nothing }
  end;

procedure PdBooleanParameterPanel.paint;
  var
    rect, circleYesRect, circleNoRect, yesTextRect, noTextRect: TRect;
  begin
  inherited paint;
  if (param.collapsed) then
    begin
    if currentValue then
      self.drawExtraValueCaptionWithString('yes', '')
    else
      self.drawExtraValueCaptionWithString('no', '');
    exit;
    end;
  rect := GetClientRect;
  with Canvas do
    begin
    font := self.font;
    with circleYesRect do
      begin
      left := rect.left + kRadioButtonLeftGap;
      right := left + kRadioButtonWidth;
      top := rect.top + self.collapsedHeight + (self.textHeight div 2 - kRadioButtonWidth div 2);
      bottom := top + kRadioButtonWidth;
      end;
    with yesTextRect do
      begin
      left := rect.left + kRadioButtonLeftGap + kRadioButtonWidth + kRadioButtonBeforeTextGap;
      right := left + textWidth('yes');
      top := rect.top + self.collapsedHeight;
      bottom := top + self.textHeight;
      end;
    circleNoRect := circleYesRect;
    with circleNoRect do
      begin
      left := yesTextRect.right + kRadioButtonBetweenGap;
      right := left + kRadioButtonWidth;
      end;
    noTextRect := yesTextRect;
    with noTextRect do
      begin
      left := yesTextRect.right + kRadioButtonBetweenGap + kRadioButtonWidth + kRadioButtonBeforeTextGap;
      right := left + textWidth('no');
      end;
    self.drawRadioButton(currentValue, editEnabled, circleYesRect);
    self.drawText('yes', yesTextRect, true, (self.selectedItemIndex = kItemYes) and (self.editEnabled), false);
    self.drawRadioButton(not currentValue, editEnabled, circleNoRect);
    self.drawText('no', noTextRect, true, (self.selectedItemIndex = kItemNo) and (self.editEnabled), false);
    unionRect(yesRect, circleYesRect, yesTextRect);
    unionRect(noRect, circleNoRect, noTextRect);
    end;
end;

procedure PdBooleanParameterPanel.drawRadioButton(value: boolean; enabled: boolean; rect: TRect);
  var
    brushColor: TColor;
  begin
  with self.canvas do
    begin
    brushColor := brush.color;
    if value then
      if enabled then
        brush.color := clBtnText
      else
        brush.color := clBtnShadow
    else
      brush.color := clBtnFace;
    with rect do ellipse(left, top, right, bottom);
    brush.color := brushColor;
    brush.style := bsClear;
    end;
  end;

end.

