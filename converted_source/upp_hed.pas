unit Upp_hed;

interface

uses ExtCtrls, Classes, StdCtrls, Controls, WinTypes, Graphics, WinProcs, Messages,
  uplant, uparams, uppanel;

type
  PdHeaderParameterPanel = class(PdParameterPanel)
	public
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
  function maxSelectedItemIndex: integer; override;
  procedure fillWithBevels;
  procedure collapseOrExpand(y: integer); override;
  procedure collapse; override;
  procedure expand; override;
  end;

implementation

uses SysUtils, Dialogs, Forms,
  umain, updcom, umath, uunits, usupport, udomain, udebug;

procedure PdHeaderParameterPanel.collapseOrExpand(y: integer);
  begin
  if (owner <> nil) then
    TMainForm(owner).collapseOrExpandParameterPanelsUntilNextHeader(self);
  param.collapsed := not param.collapsed; {don't need to change height}
  end;

procedure PdHeaderParameterPanel.collapse;
  begin
  if param.collapsed then exit;
  if (owner <> nil) then
    TMainForm(owner).collapseOrExpandParameterPanelsUntilNextHeader(self);
  param.collapsed := true;
  end;

procedure PdHeaderParameterPanel.expand;
  begin
  if not param.collapsed then exit;
  if (owner <> nil) then
    TMainForm(owner).collapseOrExpandParameterPanelsUntilNextHeader(self);
  param.collapsed := false;
  end;

procedure PdHeaderParameterPanel.initialize;
	begin
  { nothing }
  end;

procedure PdHeaderParameterPanel.updateEnabling;
	begin
  inherited updateEnabling;
  { grey out if no plant, but nothing else }
  end;

procedure PdHeaderParameterPanel.updatePlantValues;
  begin
  { nothing }
  end;

procedure PdHeaderParameterPanel.updateCurrentValue(aFieldIndex: integer);
	begin
  { nothing }
  end;

procedure PdHeaderParameterPanel.updateDisplay;
	begin
  { nothing }
  end;

procedure PdHeaderParameterPanel.doMouseDown(
    Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  { must always call this first because it sets the focus }
  inherited doMouseDown(sender, button, shift, x, y);
  { nothing else; inherited will do collapse/expand }
  end;

procedure PdHeaderParameterPanel.doKeyDown(sender: TObject; var key: word; shift: TShiftState);
  begin
  inherited doKeyDown(sender, key, shift);
  { nothing else; inherited will do collapse/expand }
  end;

function PdHeaderParameterPanel.maxWidth: integer;
  begin
  result := kLeftRightGap * 2 + self.longestLabelWordWidth;
  end;

function PdHeaderParameterPanel.minWidth(requestedWidth: integer): integer;
  var minAllowed: integer;
  begin
  minAllowed := kLeftRightGap * 2 + self.longestLabelWordWidth;
  if requestedWidth > minAllowed then
    result := -1
  else
    result := minAllowed;
  end;

function PdHeaderParameterPanel.uncollapsedHeight: integer;
  begin
  result := self.collapsedHeight;
  end;

function PdHeaderParameterPanel.maxSelectedItemIndex: integer;
  begin
  result := kItemLabel;
  end;

procedure PdHeaderParameterPanel.resizeElements;
  begin
  { do nothing }
  end;

procedure PdHeaderParameterPanel.paint;
  var
    fullRect: TRect;
  begin
  if Application.terminated then exit;
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
      left := fullRect.left + kLeftRightGap + kArrowPictureSize + kBetweenGap * 2;
      right := left + self.width - kLeftRightGap * 2;
      top := fullRect.top + 2;
      bottom := top + self.textHeight;
      end;
  {  with labelRect do
      begin
      right := fullRect.right - kleftRightGap * 4;
      left := right - textWidth(caption);
      top := fullRect.top + 2;
      bottom := top + self.textHeight;
      end;  }
    self.wrappedLabelHeight := self.drawText(self.caption, labelRect, false, false, false);
    with pictureRect do
      begin
      left := fullRect.left + kLeftRightGap;
      right := left + kArrowPictureSize;
      top := labelRect.top + 1;
      bottom := top + kArrowPictureSize;
      end;
    if plant <> nil then
      begin
      if param.collapsed then
        draw(pictureRect.left, pictureRect.top, MainForm.paramPanelClosedArrowImage.picture.bitmap)
      else
        draw(pictureRect.left, pictureRect.top, MainForm.paramPanelOpenArrowImage.picture.bitmap);
      end;
    if (self.selectedItemIndex = kItemLabel) then
      with pictureRect do rectangle(left, top, right, bottom);
      (*
    if plant <> nil then
      begin
      pen.width := 1;
      pen.color := clBlue;
      moveTo({pictureRect.right + kLeftRightGap * 2}labelRect.left + textWidth(caption) + kLeftRightGap * 2,
        labelRect.top + rHeight(labelRect) div 2 - pen.width div 2);
      lineTo({labelRect.left - kLeftRightGap * 2}fullRect.right - kLeftRightGap * 2,
        labelRect.top + rHeight(labelRect) div 2 - pen.width div 2);
      end;
      *)
    end;
  end;

procedure PdHeaderParameterPanel.fillWithBevels;
  var
    fullRect: TRect;
    TopColor, BottomColor: TColor;

  // PDF PORT -- moved nested function inline
  //procedure AdjustColors(Bevel: TPanelBevel);
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
    if self.plant <> nil then
      brush.color := clNavy
    else
      brush.color := clBtnShadow;
    fillRect(fullRect);
    brush.style := bsClear;
    end;
  if BevelOuter <> bvNone then
    begin
    //AdjustColors(BevelOuter);
    TopColor := clBtnHighlight;
    if BevelOuter = bvLowered then TopColor := clBtnShadow;
    BottomColor := clBtnShadow;
    if BevelOuter = bvLowered then BottomColor := clBtnHighlight;
    Frame3D(Canvas, fullRect, TopColor, BottomColor, BevelWidth);
    end;
  Frame3D(Canvas, fullRect, Color, Color, BorderWidth);
  if BevelInner <> bvNone then
    begin
    AdjustColors(BevelInner);
    TopColor := clBtnHighlight;
    if BevelInner = bvLowered then TopColor := clBtnShadow;
    BottomColor := clBtnShadow;
    if BevelInner = bvLowered then BottomColor := clBtnHighlight;
    Frame3D(Canvas, fullRect, TopColor, BottomColor, BevelWidth);
    end;
  end;


end.

