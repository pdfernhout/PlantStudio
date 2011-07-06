unit Uhints;

interface

uses Forms, Classes, WinTypes, ucollect;

type
  PdHint = class
    public
    formClassName: string;
    componentName: string;
    shortHint: string;
    longHint: string;
    constructor make(aFormClassName, aComponentName, aShortHint, aLongHint: string);
    end;

  PdHintManager = class
    public
    hints: TListCollection;
    constructor create;
    destructor destroy; override;
    function hintForComponentName(var HintInfo: THintInfo; wantLongHint, showParameterHint: boolean): string;
    function quickSimpleHint(component: TComponent; wantLongHint: boolean): string;
    function referredHint(ownerName, componentName: string; wantLongHint: boolean): string;
    procedure cleanUpHint(var HintInfo: THintInfo; var hintStr: string; isParameterHint: boolean);
    procedure makeHints;
    procedure clearHints;
    procedure addHint(aHint: PdHint);
    end;

procedure makeAllFormComponentsHaveHints(aForm: TForm);

implementation

uses SysUtils, Controls, StdCtrls, ExtCtrls, Buttons, Menus, Graphics, Tabs, Grids,
  usupport, uppanel, umain, usliders, uwizard, upicktdo, utdoedit, Spin, UWinSliders, umakeht;

constructor PdHint.make(aFormClassName, aComponentName, aShortHint, aLongHint: string);
  begin
  self.create;
  formClassName := aFormClassName;
  componentName := aComponentName;
  shortHint := aShortHint;
  longHint := aLongHint;
  end;

{ --------------------------------------------------------------------- PdHintManager }
constructor PdHintManager.create;
  begin
  hints := TListCollection.create;
  end;

destructor PdHintManager.destroy;
  begin
  hints.free;
  hints := nil;
  end;

function PdHintManager.hintForComponentName(var HintInfo: THintInfo;
    wantLongHint, showParameterHint: boolean): string;
  var
    component, owner: TComponent;
    parameterPanel: PdParameterPanel;
  begin
  result := '';
  if Application.terminated then exit;
  if hints = nil then exit;
  owner := nil;
  component := TComponent(hintInfo.hintControl);
  if component = nil then
    raise Exception.create('Problem: Nil component in method PdHintManager.hintForComponentName.');
  owner := component.owner;
  if owner = nil then
    raise Exception.create('Problem: Component has nil owner in method PdHintManager.hintForComponentName.');
  { if parameter panel (or slider on it), show hint for parameter pointed to by panel }
  parameterPanel := nil;
  if (owner is TMainForm) and (component is PdParameterPanel) then
    parameterPanel := component as PdParameterPanel
  else if (owner is PdParameterPanel) and (component is KfSlider) then
    parameterPanel := KfSlider(component).parent as PdParameterPanel;
  if parameterPanel <> nil then
    begin
    if parameterPanel.param <> nil then
      begin
      if not showParameterHint then exit;
      result := parameterPanel.param.getHint;
      self.cleanUpHint(hintInfo, result, true);
      end;
    exit;
    end;
  { show hints for tdos in wizard }
  if (owner is TWizardForm) and (component is TDrawGrid) then
    begin
    result := TWizardForm(owner).hintForTdosDrawGridAtPoint(component, hintInfo.cursorPos, hintInfo.cursorRect);
    self.cleanUpHint(hintInfo, result, false);
    exit;
    end;
  { show hints for tdos in tdo chooser }
  if (owner is TPickTdoForm) and (component is TDrawGrid) then
    begin
    result := TPickTdoForm(owner).hintForTdosDrawGridAtPoint(component, hintInfo.cursorPos, hintInfo.cursorRect);
    self.cleanUpHint(hintInfo, result, false);
    exit;
    end;
  { otherwise look up non-parameter hint from hint list }
  result := self.quickSimpleHint(component, wantLongHint);
  if copy(result, 1, 1) = '?' then
    begin
    result := copy(result, 2, length(result) - 1);
    result := self.referredHint(owner.className, result, wantLongHint);
    end;
  self.cleanUpHint(hintInfo, result, false);
  end;

function PdHintManager.quickSimpleHint(component: TComponent; wantLongHint: boolean): string;
  var
    i: longint;
    hint: PdHint;
    owner: TComponent;
    ownerClassName: string;
  begin
  result := '';
  owner := component.owner;
  if owner = nil then
    raise Exception.create('Problem: Component has nil owner in method PdHintManager.quickSimpleHint.');
  if hints.count > 0 then
    for i := 0 to hints.count - 1 do
      begin
      hint := PdHint(hints.items[i]);
      { check both form class and component name,
        so only components in one form need be uniquely named }
      ownerClassName := owner.className;
      if (upperCase(hint.formClassName) = upperCase(ownerClassName)) and
          (upperCase(hint.componentName) = upperCase(component.name)) then
        begin
        if wantLongHint then
          result := hint.longHint
        else
          result := hint.shortHint;
        if result = '(none)' then result := '';
        break;
        end;
      end;
  end;

function PdHintManager.referredHint(ownerName, componentName: string; wantLongHint: boolean): string;
  var
    i: longint;
    hint: PdHint;
  begin
  result := '';
  if hints.count > 0 then
    for i := 0 to hints.count - 1 do
      begin
      hint := PdHint(hints.items[i]);
      { check both form class and component name,
        so only components in one form need be uniquely named }
      if (upperCase(hint.formClassName) = upperCase(ownerName)) and
          (upperCase(hint.componentName) = upperCase(componentName)) then
        begin
        if wantLongHint then
          result := hint.longHint
        else
          result := hint.shortHint;
        if result = '(none)' then result := '';
        break;
        end;
      end;
  end;

procedure PdHintManager.cleanUpHint(var HintInfo: THintInfo; var hintStr: string; isParameterHint: boolean);
  begin
  if hintStr = '(none)' then hintStr := '';
  hintStr := trimQuotesFromFirstAndLast(hintStr); // v2.0
  if isParameterHint then
    hintInfo.hintColor := clAqua;
  end;

procedure PdHintManager.makeHints;
  begin
  CreateHints1(self);
  CreateHints2(self);
  end;

procedure PdHintManager.clearHints;
  begin
  hints.clear;
  end;

procedure PdHintManager.addHint(aHint: PdHint);
  begin
  if aHint <> nil then
    hints.add(aHint);
  end;

    { from utab2asp.pas - these are the component types that have hints
type
componentConstants = (TButton, TBitBtn, TSpeedButton,
  TCheckBox, TRadioButton, TRadioGroup,
  TListBox, TComboBox,
  TEdit, TMemo,
  TPanel, THeader, TGroupBox, TScrollBox,
  TImage, TShape, TPaintBox,
  TSpinEdit,
  TTabSet,
  KfWinSlider,
  TDrawGrid,
  PdTdoPaintBox);
  }

procedure makeAllFormComponentsHaveHints(aForm: TForm);
  var
    i: longint;
    component: TComponent;
  begin
  if aForm.componentCount > 0 then
    for i := 0 to aForm.componentCount - 1 do
      begin
      component := aForm.components[i];
      if (component is TButton) or (component is TBitBtn) or (component is TSpeedButton) or
        (component is TCheckBox) or (component is TRadioButton) or (component is TRadioGroup) or
        (component is TListBox) or (component is TComboBox) or
        (component is TEdit) or (component is TMemo) or
        (component is TPanel) or (component is THeader) or (component is TGroupBox) or (component is TScrollBox) or
        (component is TImage) or (component is TShape) or (component is TPaintBox)
        or (component is TSpinEdit)
        or (component is TTabSet)
        or (component is KfWinSlider)
        or (component is TDrawGrid)
        or (component is PdTdoPaintBox)
        then
        TControl(component).showHint := true;
      end;
  end;

end.
