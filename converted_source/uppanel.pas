unit uppanel;

interface

uses ExtCtrls, Classes, StdCtrls, Controls, WinTypes, Graphics, WinProcs, Messages,
  uparams, usection, ucollect, uplant;


const
  kBetweenGap = 3;
  kTopBottomGap = 4;
  kLeftRightGap = 6;
  kRadioButtonLeftGap = 10; 
  kRadioButtonWidth = 10;
  kRadioButtonBetweenGap = 10;
  kRadioButtonBeforeTextGap = 5;
  kSliderSpaceGap = 10;
  kEditMaxWidth = 100; {200;}
  kEditMinWidth = 50; {150;}
  kNotSelectedString = '(not selected)';
  kGraphHeight = 100; {150;}
  kMaxDisplayDigitsToLeftOfDecimal = 7;
  kMaxDisplayDigitsToRightOfDecimal = 6;
  kMaxDisplayDigits = 9;
  kArrowPictureSize = 13;
  kOverridePictureSize = 0; // 13

  kItemNone = -1;
  kItemLabel = 0;

type
  PdParameterPanel = class(TPanel)
	public
  plant: PdPlant;
  param: PdParameter;
  readOnly: boolean;
  labelWidth: integer;
  textHeight: integer;
  labelRect, pictureRect, overrideRect: TRect;
  wrappedLabelHeight: integer;
  longestLabelWordWidth: integer;
  selectedItemIndex: integer;
  constructor create(anOwner: TComponent); override;
  constructor createForParameter(anOwner: TComponent; aParameter: PdParameter);
  procedure initialize; virtual;
  procedure updatePlant(newPlant: PdPlant); virtual;
  procedure updatePlantValues; virtual;
	procedure updateEnabling; virtual;
  procedure updateFromUpdateEventList(updateList: TListCollection); virtual;
  procedure updateCurrentValue(aFieldIndex: integer); virtual;
  procedure updateDisplay; virtual;
  procedure collapseOrExpand(y: integer); virtual;
  procedure collapse; virtual;
  procedure expand; virtual;
  procedure paint; override;
  procedure fillWithBevels;
  function collapsedHeight: integer; virtual;
  function minWidth(requestedWidth: integer): integer; virtual;
  function maxWidth: integer; virtual;
  function uncollapsedHeight: integer; virtual;
  procedure resizeElements; virtual;
  function editHeight: integer;
  procedure calculateTextDimensions; virtual;
  procedure calculateHeight;
  procedure doOnEnter(sender: TObject);
  procedure doOnExit(sender: TObject);
  procedure WMGetDlgCode(var Message: TWMGetDlgCode); message WM_GETDLGCODE;
  procedure doMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer); virtual;
  procedure doKeyDown(sender: TObject; var key: word; shift: TShiftState); virtual;
  procedure doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer); virtual;
  procedure doMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer); virtual;
  procedure tabThroughItems(goForward: boolean); virtual;
  function nextSelectedItemIndex(goForward: boolean): integer; virtual;
  function maxSelectedItemIndex: integer; virtual;
	function measureText(text: string; drawRect: TRect): integer;
  function drawText(text: string; drawRect: TRect; isSelectable, isSelected, italicize: boolean): integer;
  procedure drawTextSelectedBox(rect: TRect);
  procedure drawTextLabel(text: string; drawRect: TRect; drawBox: boolean);
  function minScaleWidthWithBounds(unitSet, unitPlant: integer; softMin, softMax: single): integer;
  function minScaleWidthWithoutBounds(unitSet, unitPlant: integer): integer;
  function calculateLongestLabelWordWidth: integer;
  function formTextHeight: longint;
  function formTextWidth(aString: string): longint;
  procedure drawExtraValueCaptionWithString(valueString, unitString: string);
  end;

implementation

uses SysUtils, Dialogs, Forms,
  umain, updcom, umath, uunits, usupport, udomain, udebug, upp_hed;

constructor PdParameterPanel.create(anOwner: TComponent);
  begin
  inherited create(anOwner);
  self.plant := nil;
  self.parentFont := true;
  self.onMouseDown := self.doMouseDown;
  self.onMouseMove := self.doMouseMove;
  self.onMouseUp := self.doMouseUp;
  self.onKeyDown := self.doKeyDown;
  self.onEnter := self.doOnEnter;
  self.onExit := self.doOnExit;
  self.tabStop := true;
  self.enabled := true;
  if MainForm <> nil then
    self.popupMenu := MainForm.paramPopupMenu;
  end;

constructor PdParameterPanel.createForParameter(anOwner: TComponent; aParameter: PdParameter);
	begin
  self.create(anOwner);
	param := aParameter;
  self.readOnly := param.readOnly;
  self.caption := param.getName;
  self.initialize;
  self.updateDisplay;
  self.updateEnabling;
  self.selectedItemIndex := -1;
  self.bevelInner := bvRaised;
  self.bevelOuter := bvNone;
  end;

function PdParameterPanel.formTextHeight: longint;
  var
    theForm: TCustomForm;
    oldSize: integer;
  begin
  theForm := getParentForm(self);
  if theForm = nil then
    result := 16 {default}
  else if theForm.canvas = nil then
    result := 16 {default}
  else
    begin
    result := 16;
    theForm.canvas.font := theForm.font;
    result := theForm.canvas.textHeight('W');
    end;
  end;

function PdParameterPanel.formTextWidth(aString: string): longint;
  var
    theForm: TCustomForm;
  begin
  theForm := getParentForm(self);
  if theForm = nil then
    result := 50 {default}
  else if theForm.canvas = nil then
    result := 50 {default}
  else
    begin
    result := length(aString) * 8;
    theForm.canvas.font := theForm.font;
    result := theForm.canvas.textWidth(aString);
    end;
  end;

procedure PdParameterPanel.calculateTextDimensions;
  begin
  { use form canvas for this because when component is first created, doesn't know what font it has }
  self.textHeight := self.formTextHeight;
  self.labelWidth := self.formTextWidth(trimLeftAndRight(self.caption));
  self.longestLabelWordWidth := self.calculateLongestLabelWordWidth;
  end;

procedure PdParameterPanel.doMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  if not self.focused then self.setFocus;
  if x < pictureRect.right then
    self.collapseOrExpand(y);
  if not self.focused then self.setFocus;
  if param <> nil then
    if param.collapsed then self.selectedItemIndex := kItemLabel;
  end;

procedure PdParameterPanel.doMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
  begin
  { subclasses can override }
  end;

procedure PdParameterPanel.doMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  { subclasses can override }
  end;

procedure PdParameterPanel.doKeyDown(sender: TObject; var key: word; shift: TShiftState);
{ subclasses should override and respond to enter events when different items are selected }
{ subclasses should call inherited }
  var
    Form: TCustomForm;
  begin
  if (key = VK_TAB) then
    begin
    if shift = [ssShift] then
      self.tabThroughItems(false)
    else
      self.tabThroughItems(true);
    if self.selectedItemIndex = kItemNone then
      begin
      form := getParentForm(self);
      if form <> nil then
        if shift = [ssShift] then
          begin
          TMainForm(form).backTabbingInParametersPanel := true;
          form.perform(wm_NextDlgCtl, 1, 0); {previous}
          end
        else
          form.perform(wm_NextDlgCtl, 0, 0);
      end;
    end
  else
    if (key = VK_RETURN) and (self.selectedItemIndex = kItemLabel) then
      self.collapseOrExpand(0); {give it a y as if the label was clicked on}
  end;

function PdParameterPanel.maxSelectedItemIndex: integer;
  begin
  { subclasses should override }
  result := 0;
  end;

procedure PdParameterPanel.tabThroughItems(goForward: boolean);
  begin
  { subclasses need not override this if they override maxSelectedItemIndex }
  self.selectedItemIndex := self.nextSelectedItemIndex(goForward);
  if self.selectedItemIndex > self.maxSelectedItemIndex then
    self.selectedItemIndex := kItemNone;
  self.invalidate;
  end;

function PdParameterPanel.nextSelectedItemIndex(goForward: boolean): integer;
  begin
  if goForward then
    result := self.selectedItemIndex + 1
  else
    result := self.selectedItemIndex - 1;
  end;

procedure PdParameterPanel.WMGetDlgCode(var Message: TWMGetDlgCode);
  begin
  inherited;
  { want arrows allows us to pass arrow keys on to slider or combo box }
  Message.Result := Message.Result or DLGC_WANTTAB or DLGC_WANTARROWS;
  end;

procedure PdParameterPanel.initialize;
	begin
  { sublasses can override }
  end;

procedure PdParameterPanel.doOnEnter(sender: TObject);
  begin
  TMainForm(owner).enteringAParameterPanel(self);
  if TMainForm(owner).backTabbingInParametersPanel then
    begin
    self.selectedItemIndex := self.maxSelectedItemIndex;
    TMainForm(owner).backTabbingInParametersPanel := false;
    end;
  if self.selectedItemIndex = kItemNone then self.selectedItemIndex := kItemLabel;
  self.invalidate;
  end;

procedure PdParameterPanel.doOnExit(sender: TObject);
  begin
  TMainForm(owner).leavingAParameterPanel(self);
  self.selectedItemIndex := kItemNone;
  self.invalidate;
  end;

{plant has changed}
procedure PdParameterPanel.updatePlant(newPlant: PdPlant);
	begin
  if plant <> newPlant then
  	begin
    plant := newPlant;
    self.updateEnabling;
    self.updateCurrentValue(-1);  { -1 means update all }
    self.updateDisplay;
    self.invalidate;
    end
  end;

procedure PdParameterPanel.updatePlantValues;
  begin
  { subclasses should override }
  end;

procedure PdParameterPanel.updateEnabling;
	begin
  { subclasses should call this when they do their enabling }
  self.enabled := (self.plant <> nil);
  end;

procedure PdParameterPanel.updateCurrentValue(aFieldIndex: integer);
	begin
  { subclasses may override }
  end;

procedure PdParameterPanel.updateFromUpdateEventList(updateList: TListCollection);
  var
    i: longint;
    updateEvent: PdPlantUpdateEvent;
    shouldUpdate: boolean;
  begin
  if updateList.count <= 0 then exit;
  if self.plant = nil then exit;
  shouldUpdate := false;
  updateEvent := nil;
  for i := 0 to updateList.count - 1 do
    begin
    updateEvent := PdPlantUpdateEvent(updateList.items[i]);
    if updateEvent = nil then continue;
    if updateEvent.plant = nil then continue;
    if (updateEvent.plant = self.plant) and (updateEvent.fieldID = param.fieldNumber) then
      begin
      shouldUpdate := true;
      break;
      end;
    end;
  if shouldUpdate and (updateEvent <> nil) then
    begin
    { could put check in descendents to only update if value is different from current }
    self.updateCurrentValue(updateEvent.fieldIndex);
    self.updateDisplay;
    self.invalidate;
    end;
  end;

procedure PdParameterPanel.updateDisplay;
	begin
  { subclasses should override }
  end;

function PdParameterPanel.minWidth(requestedWidth: integer): integer;
  begin
  { subclasses must override }
  result := 0;
  end;

function PdParameterPanel.maxWidth: integer;
  begin
  { subclasses must override }
  result := 0;
  end;

function PdParameterPanel.uncollapsedHeight: integer;
  begin
  { subclasses must override }
  result := 0;
  end;

procedure PdParameterPanel.resizeElements;
  begin
  { subclasses must override }
  end;

function PdParameterPanel.editHeight: integer;
  begin
  result := self.textHeight + 8;
  end;

function PdParameterPanel.calculateLongestLabelWordWidth: integer;
  var
    i, lastSpace, maxLength: integer;
  begin
  { o: xxxxx xxxxxxxxx xx }
  lastSpace := 3;
  maxLength := 0;
  for i := 4 to length(self.caption) do
    begin
    if (caption[i] = ' ') or (i = length(self.caption)) then
      begin
      if i - lastSpace > maxLength then maxLength := i - lastSpace;
      lastSpace := i;
      end;
    end;
  result := self.formTextWidth('w') * maxLength;
  end;

procedure PdParameterPanel.calculateHeight;
  var
    fullRect: TRect;
  begin
  fullRect := getClientRect;
  with labelRect do
    begin
    left := fullRect.left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap;
    right := fullRect.right - kLeftRightGap;
    top := fullRect.top + 2;
    bottom := top + self.textHeight;
    end;
  self.wrappedLabelHeight := self.measureText(self.caption, labelRect);
  if param <> nil then
    begin
    if param.collapsed then
      self.height := self.collapsedHeight
    else
      self.height := self.uncollapsedHeight;
    end;
  end;

procedure PdParameterPanel.collapseOrExpand(y: integer);
  begin
  if y > self.collapsedHeight then exit;
  if param <> nil then
    begin
    if not param.collapsed then
      self.collapse
    else
      self.expand;
    end;
  if (owner <> nil) and (not TMainForm(owner).internalChange) then
    TMainForm(owner).repositionParameterPanels;
  end;

procedure PdParameterPanel.collapse;
  begin
  if param <> nil then param.collapsed := true;
  self.height := self.collapsedHeight;
  end;

procedure PdParameterPanel.expand;
  begin
  if param <> nil then param.collapsed := false;
  self.height := self.uncollapsedHeight;
{  updateCurrentValue(-1); } {cfk don't think i need this anymore}
  end;

procedure PdParameterPanel.Paint;
  var
    fullRect: TRect;
  begin
  { copied from TCustomPanel.paint and location of caption text changed }
  { can't call inherited paint because it wants to put the caption in the middle }
  self.fillWithBevels;
  fullRect := getClientRect;
  with canvas do
    begin
    font := self.font;
    brush.style := bsClear;
    with labelRect do
      begin
      left := fullRect.left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap;
      right := left + self.width - kLeftRightGap * 2 - kArrowPictureSize - kOverridePictureSize;
      top := fullRect.top + 2;
      bottom := top + self.textHeight;
      end;
    self.wrappedLabelHeight := self.drawText(self.caption, labelRect, false, false, false);
    with pictureRect do
      begin
      left := fullRect.left + kLeftRightGap;
      right := left + kArrowPictureSize;
      top := labelRect.top + 1;
      bottom := top + kArrowPictureSize;
      end;
      {
    with overrideRect do
      begin
      left := pictureRect.right;
      right := left + kOverridePictureSize;
      top := labelRect.top + 1;
      bottom := top + kOverridePictureSize;
      end;
      }
    if (self.plant <> nil) and (param <> nil) then
      begin
      if param.collapsed then
        draw(pictureRect.left, pictureRect.top, MainForm.paramPanelClosedArrowImage.picture.bitmap)
      else
        draw(pictureRect.left, pictureRect.top, MainForm.paramPanelOpenArrowImage.picture.bitmap);
        {
      if (not param.cannotOverride) and (param.isOverridden) then
        draw(overrideRect.left, overrideRect.top, MainForm.paramOverride.picture.bitmap)
      else
        draw(overrideRect.left, overrideRect.top, MainForm.paramOverrideNot.picture.bitmap);
        }
      end;
    if (self.selectedItemIndex = kItemLabel) then
      with pictureRect do rectangle(left, top, right, bottom);
    end;
  end;

procedure PdParameterPanel.drawExtraValueCaptionWithString(valueString, unitString: string);
  var
    rect, collapsedExtraRect: TRect;
    stringToDisplay: string;
  begin
  if (self.wrappedLabelHeight > self.textHeight) then exit;
  stringToDisplay := ':  ' + valueString;
  if unitString <> '(no unit)' then
    stringToDisplay := stringToDisplay + ' ' + unitString;
  rect := self.getClientRect;
  with collapsedExtraRect do
    begin
    left := rect.left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize
        + kBetweenGap + self.canvas.textWidth(self.caption);
    right := rect.right;
    top := rect.top + 2;
    bottom := top + self.textHeight;
    end;
  if rWidth(collapsedExtraRect) <= self.canvas.textWidth(stringToDisplay) then exit;
  self.drawText(stringToDisplay, collapsedExtraRect, false, false, false);
  end;

procedure PdParameterPanel.fillWithBevels;
  var
    fullRect: TRect;
    TopColor, BottomColor: TColor;
    theForm: TCustomForm;

  // PDF PORT moved function inline 
  // procedure AdjustColors(Bevel: TPanelBevel);
  //  begin
  //  TopColor := clBtnHighlight;
  //  if Bevel = bvLowered then TopColor := clBtnShadow;
  //  BottomColor := clBtnShadow;
  //  if Bevel = bvLowered then BottomColor := clBtnHighlight;
  //  end;

  begin
  fullRect := getClientRect;
  with canvas do
    begin
    brush.color := clBtnFace;
    theForm := getParentForm(self);
    if (theForm <> nil) and (theForm is TMainForm) and ((theForm as TMainForm).selectedParameterPanel = self) then
      begin
      pen.color := clHighlight;
      pen.style := psSolid;
     { pen.width := 2; }
      with fullRect do rectangle(left+2, top+2, right-1, bottom-1);
      end
    else
      fillRect(fullRect);
    brush.style := bsClear;
    end;
  if BevelOuter <> bvNone then
    begin
    // AdjustColors(BevelOuter);
    TopColor := clBtnHighlight;
    if BevelOuter = bvLowered then TopColor := clBtnShadow;
    BottomColor := clBtnShadow;
    if BevelOuter = bvLowered then BottomColor := clBtnHighlight;
    Frame3D(Canvas, fullRect, TopColor, BottomColor, BevelWidth);
    end;
  Frame3D(Canvas, fullRect, Color, Color, BorderWidth);
  if BevelInner <> bvNone then
    begin
    // AdjustColors(BevelInner);
    TopColor := clBtnHighlight;
    if BevelInner = bvLowered then TopColor := clBtnShadow;
    BottomColor := clBtnShadow;
    if BevelInner = bvLowered then BottomColor := clBtnHighlight;
    Frame3D(Canvas, fullRect, TopColor, BottomColor, BevelWidth);
    end;   
  end;

function PdParameterPanel.measureText(text: string; drawRect: TRect): integer;
  var
    cText: array[0..255] of Char;
    theForm: TCustomForm;
    useRect: TRect;
  begin
  theForm := getParentForm(self);
  if theForm = nil then
    result := 16 {default}
  else
    begin
    if theForm.canvas = nil then
      result := 16 {default}
    else
      with theForm.canvas do
        begin
        font := theForm.font;
        useRect := drawRect;
        strPCopy(cText, text);
        { returns height of rectangle }
        result := winprocs.drawText(handle, cText, strLen(cText), useRect,
          DT_LEFT or DT_WORDBREAK or DT_CALCRECT);
        end;
    end;
    // cfk change v1.6b1 -- taken out, dealt with problem by using form to get size
  // deal with large fonts by increasing label height -- kludge
  //if screen.pixelsPerInch >= 120 then // large fonts
  //  result := round(result * 1.5);
  end;

function PdParameterPanel.drawText(text: string; drawRect: TRect;
      isSelectable, isSelected, italicize: boolean): integer;
  var
    cText: array[0..255] of Char;
  begin
  with self.canvas do
    begin
    font := self.font;
    if self.plant <> nil then
      begin
      if self is PdHeaderParameterPanel then
        font.color := clWhite
      else if text = self.caption then
        font.color := clBlue
      else
        font.color := clBtnText;
      end
    else
      begin
      if self is PdHeaderParameterPanel then
        font.color := clBtnFace
      else
        font.color := clBtnShadow;
      end;
    if italicize then
      font.style := [fsItalic];
    if self is PdHeaderParameterPanel then
      font.style := [fsBold];
    strPCopy(cText, text);
    result := winprocs.drawText(handle, cText, strLen(cText), drawRect,
      DT_LEFT or DT_WORDBREAK or DT_NOCLIP);
    drawRect.bottom := drawRect.top + result;
    if (isSelected) then
      self.drawTextSelectedBox(drawRect)
    else if (isSelectable) then
      begin
      pen.color := clBtnShadow;
      moveTo(drawRect.left, drawRect.bottom - 3);
      lineTo(drawRect.right, drawRect.bottom - 3);
      end;
    end;
  end;

procedure PdParameterPanel.drawTextSelectedBox(rect: TRect);
  begin
  with canvas do
    begin
    pen.color := clBtnShadow;
    moveTo(rect.right + 2, rect.top);
    lineTo(rect.left - 2, rect.top);
    lineTo(rect.left - 2, rect.bottom - 2);
    lineTo(rect.right + 2, rect.bottom - 2);
    lineTo(rect.right + 2, rect.top);
    end;
  end;

procedure PdParameterPanel.drawTextLabel(text: string; drawRect: TRect; drawBox: boolean);
  var
    cText: array[0..255] of Char;
  begin
  with self.canvas do
    begin
    font := self.font;
    font.color := clBtnText;
    strPCopy(cText, text);
    winprocs.drawText(handle, cText, strLen(cText), drawRect, DT_LEFT or DT_WORDBREAK);
    end;
  if drawBox then self.drawTextSelectedBox(drawRect);
  end;

function PdParameterPanel.collapsedHeight: integer;
  begin
  result := self.wrappedLabelHeight + kTopBottomGap;
  result := intMax(result, kArrowPictureSize + 5);
  end;

function PdParameterPanel.minScaleWidthWithBounds(unitSet, unitPlant: integer; softMin, softMax: single): integer;
  var
    i, numeralChars, letterChars, maxLengthSoftMin, maxLengthSoftMax: integer;
    minValue, maxValue: single;
  begin
  { value number of chars (always use max) }
  numeralChars := kMaxDisplayDigitsToLeftOfDecimal {+ kMaxDisplayDigitsToRightOfDecimal + 1};
  { unit string number of chars (get max for set) }
  letterChars := maxUnitStringLengthForSet(unitSet);
  { bounds number of chars (use actual bounds, but calculate max for set) }
  maxLengthSoftMin := 0;
  maxLengthSoftMax := 0;
  for i := 1 to GetLastUnitEnumInUnitSet(unitSet) - 1 do
    begin
    minValue := Convert(unitSet, unitPlant, i, softMin);
    maxValue := Convert(unitSet, unitPlant, i, softMax);
    maxLengthSoftMin := intMax(maxLengthSoftMin, length(digitValueString(minValue)));
    maxLengthSoftMax := intMax(maxLengthSoftMax, length(digitValueString(maxValue)));
    end;
  numeralChars := numeralChars + maxLengthSoftMin + maxLengthSoftMax;
  { calc min scale width from number of chars }
  result := self.formTextWidth('i') * letterChars
    + self.formTextWidth('1') * numeralChars
    + kBetweenGap * 3 + kLeftRightGap * 2;
  end;

function PdParameterPanel.minScaleWidthWithoutBounds(unitSet, unitPlant: integer): integer;
  var
    numeralChars, letterChars: integer;
  begin
  { value number of chars (always use max) }
  numeralChars := kMaxDisplayDigitsToLeftOfDecimal {+ kMaxDisplayDigitsToRightOfDecimal + 1};
  { unit string number of chars (get max for set) }
  letterChars := maxUnitStringLengthForSet(unitSet);
  { calc min scale width from number of chars }
  result := self.formTextWidth('i') * letterChars
    + self.formTextWidth('1') * numeralChars
    + kBetweenGap + kLeftRightGap * 2;
  end;

end.

