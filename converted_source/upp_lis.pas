unit upp_lis;

interface

uses ExtCtrls, Classes, StdCtrls, Controls, WinTypes, Graphics, WinProcs, Messages,
    uplant, uparams, uppanel;

const
  kItemFirstChoice = 1;
  kMaxNumChoices = 20; 

type
  PdListParameterPanel = class(PdParameterPanel)
	public
  hasRadioButtons: boolean;
  currentChoice: integer;
  choiceStrings: TStringList;
  choiceRects: array[0..kMaxNumChoices] of TRect;
  choiceChecks: array[0..kMaxNumChoices] of boolean;
  editEnabled: boolean;
  procedure initialize; override;
  destructor destroy; override;
	procedure updateEnabling; override;
  procedure updatePlantValues; override;
  procedure updateCurrentValue(aFieldIndex: integer); override;
  procedure updateDisplay; override;
  function minWidth(requestedWidth: integer): integer; override;
  function maxWidth: integer; override;
  function uncollapsedHeight: integer; override;
  procedure resizeElements; override;
  procedure paint; override;
  procedure doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer); override;
  procedure doKeyDown(sender: TObject; var key: word; shift: TShiftState); override;
  procedure drawRadioButton(value: boolean; enabled: boolean; rect: TRect);
  procedure drawCheckBox(value: boolean; enabled: boolean; rect: TRect);
  function maxSelectedItemIndex: integer; override;
  procedure clearChecks;
  procedure setNewValue(index: integer);
  function firstCheckedString: string;
  end;

implementation

uses SysUtils, Dialogs, Forms,
  umain, updcom, umath, uunits, usupport, udomain, udebug;

procedure PdListParameterPanel.initialize;
	begin
  currentChoice := 0;
  editEnabled := false;
  choiceStrings := TStringList.create;
  PdPlant.fillEnumStringList(choiceStrings, param.fieldNumber, hasRadioButtons);
  end;

destructor PdListParameterPanel.destroy;
  begin
  choiceStrings.free;
  choiceStrings := nil;
  inherited destroy;
  end;

procedure PdListParameterPanel.updateEnabling;
	begin
  inherited updateEnabling;
  editEnabled := not ((plant = nil) or (self.readOnly));
  end;

procedure PdListParameterPanel.updatePlantValues;
  var oldChoice: integer;
  begin
  if plant = nil then exit;
  if param.collapsed then exit;
  oldChoice := currentChoice;
  self.updateCurrentValue(-1);
  if not hasRadioButtons or (oldChoice <> currentChoice) then
    begin
    updateDisplay;
    invalidate;
    end;
  end;

procedure PdListParameterPanel.updateCurrentValue(aFieldIndex: integer);
  var
    i: smallint;
	begin
  if (plant = nil) or (param.fieldType <> kFieldEnumeratedList) then
    begin
    currentChoice := 0;
    self.clearChecks;
    editEnabled := false;
    end
  else
    begin
    if hasRadioButtons then
      plant.transferField(kGetField, currentChoice, param.fieldNumber, kFieldSmallint, kNotArray, false, nil)
    else
      if choiceStrings.count > 0 then
        for i := 0 to choiceStrings.count - 1 do
          plant.transferField(kGetField, choiceChecks[i], param.fieldNumber, kFieldBoolean, i, false, nil);
    end;
  end;

procedure PdListParameterPanel.updateDisplay;
	begin
  if (plant <> nil) and (param.fieldType = kFieldEnumeratedList) then
    self.invalidate
  else
    editEnabled := false;
  end;

procedure PdListParameterPanel.clearChecks;
  var i: smallint;
  begin
  for i := 0 to kMaxNumChoices do choiceChecks[i] := false;
  end;

procedure PdListParameterPanel.doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y:
  Integer);
  var
    i: integer;
    thePoint: TPoint;
  begin
  { must always call this first because it sets the focus }
  inherited doMouseUp(sender, button, shift, x, y);
  if (editEnabled) then
    begin
    thePoint := Point(x, y);
    if choiceStrings.count > 0 then for i := 0 to choiceStrings.count - 1 do
      if ptInRect(choiceRects[i], thePoint) then
        begin
        self.setNewValue(i);
        self.selectedItemIndex := kItemFirstChoice + currentChoice;
        break;
        end;
    self.invalidate;
    end;
  end;

procedure PdListParameterPanel.doKeyDown(sender: TObject; var key: word; shift: TShiftState);
  begin
  inherited doKeyDown(sender, key, shift);
  if (editEnabled) and (key = VK_RETURN) and (self.selectedItemIndex >= kItemFirstChoice) then
    begin
    self.setNewValue(self.selectedItemIndex - kItemFirstChoice);
    self.invalidate;
    end;
  end;

procedure PdListParameterPanel.setNewValue(index: integer);
  begin
  if hasRadioButtons then
    begin
    currentChoice := index;
    MainForm.doCommand(
      PdChangeSmallintValueCommand.createCommandWithListOfPlants(
        MainForm.selectedPlants, currentChoice, param.fieldNumber, kNotArray, param.regrow));
    end
  else
    begin
    choiceChecks[index] := not choiceChecks[index];
    MainForm.doCommand(
      PdChangeBooleanValueCommand.createCommandWithListOfPlants(
        MainForm.selectedPlants, choiceChecks[index], param.fieldNumber, index, param.regrow));
    end;
  end;

function PdListParameterPanel.firstCheckedString: string;
  var
    i: smallint;
  begin
  result := '';
  if choiceStrings.count > 0 then for i := 0 to choiceStrings.count - 1 do
    begin
    if hasRadioButtons then
      begin
      if currentChoice = i then
        begin
        result := choiceStrings.strings[i];
        exit;
        end;
      end
    else
      begin
      if choiceChecks[i] then
        begin
        result := choiceStrings.strings[i];
        exit;
        end;
      end;
    end;
  end;

function PdListParameterPanel.maxWidth: integer;
  var
    i, maxWidth: integer;
  begin
  maxWidth := 0;
  with TMainForm(owner).canvas do for i := 0 to choiceStrings.count - 1 do
    maxWidth := intMax(maxWidth, textWidth(choiceStrings.strings[i]));
  result := intMax(kLeftRightGap * 2 + self.labelWidth,
    + kRadioButtonLeftGap + kRadioButtonWidth + kRadioButtonBeforeTextGap + maxWidth + kLeftRightGap);
  end;

function PdListParameterPanel.minWidth(requestedWidth: integer): integer;
  var
    i, longestWidth, minAllowed: integer;
  begin
  longestWidth := 0;
  with TMainForm(owner).canvas do for i := 0 to choiceStrings.count - 1 do
    longestWidth := intMax(longestWidth, textWidth(choiceStrings.strings[i]));
  minAllowed := intMax(kLeftRightGap * 2 + self.longestLabelWordWidth,
    + kRadioButtonLeftGap + kRadioButtonWidth + kRadioButtonBeforeTextGap + longestWidth + kLeftRightGap);
  if requestedWidth > minAllowed then
    result := -1
  else
    result := minAllowed;
  end;

function PdListParameterPanel.uncollapsedHeight: integer;
  begin
  result := self.collapsedHeight + self.textHeight * choiceStrings.count + kTopBottomGap;
  end;

function PdListParameterPanel.maxSelectedItemIndex: integer;
  begin
  if (not param.collapsed) and (self.editEnabled) then
    result := kItemFirstChoice + choiceStrings.count - 1
  else
    result := kItemLabel;
  end;

procedure PdListParameterPanel.resizeElements;
  begin
  { do nothing }
  end;

procedure PdListParameterPanel.paint;
  var
    i: integer;
    rect: TRect;
    circleRects: array[0..kMaxNumChoices] of TRect;
    textRects: array[0..kMaxNumChoices] of TRect;
  begin
  if Application.terminated then exit;
  inherited paint;
  if (param.collapsed) then
    begin
    self.drawExtraValueCaptionWithString(self.firstCheckedString, '');
    exit;
    end;
  rect := GetClientRect;
  if choiceStrings.count > 0 then for i := 0 to choiceStrings.count - 1 do
    begin
    with circleRects[i] do
      begin
      left := rect.left + kRadioButtonLeftGap;
      right := left + kRadioButtonWidth;
      top := rect.top + self.collapsedHeight + self.textHeight * i
        + (self.textHeight div 2 - kRadioButtonWidth div 2);
      bottom := top + kRadioButtonWidth;
      end;
    with textRects[i] do
      begin
      left := rect.left + kRadioButtonLeftGap + kRadioButtonWidth + kRadioButtonBeforeTextGap;
      right := left + self.canvas.textWidth(choiceStrings.strings[i]);
      top := rect.top + self.collapsedHeight + self.textHeight * i;
      bottom := top + self.textHeight;
      end;
    if hasRadioButtons then
      self.drawRadioButton((currentChoice = i), editEnabled, circleRects[i])
    else
      self.drawCheckBox(choiceChecks[i], editEnabled, circleRects[i]);
    self.drawText(choiceStrings.strings[i], textRects[i], true,
      (self.selectedItemIndex = kItemFirstChoice + i) and (self.editEnabled), false);
    unionRect(choiceRects[i], circleRects[i], textRects[i]);
    end;
  end;

procedure PdListParameterPanel.drawRadioButton(value: boolean; enabled: boolean; rect: TRect);
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
    if enabled then
      pen.color := clBtnText
    else
      pen.color := clBtnShadow;
    with rect do ellipse(left, top, right, bottom);
    brush.color := brushColor;
    brush.style := bsClear;
    end;
  end;

procedure PdListParameterPanel.drawCheckBox(value: boolean; enabled: boolean; rect: TRect);
  begin
  with self.canvas do
    begin
    brush.style := bsClear;
    if enabled then
      pen.color := clBtnText
    else
      pen.color := clBtnShadow;
    with rect do rectangle(left, top, right, bottom);
    if value then with rect do
      begin
      moveTo(left, top);
      lineTo(right, bottom);
      moveTo(left, bottom);
      lineTo(right, top);
      end;
    end;
  end;

end.
