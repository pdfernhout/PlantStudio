unit uborders;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Spin, ExtCtrls, Buttons, udomain, updform;

type
  TPrintBordersForm = class(PdForm)
    Close: TButton;
    cancel: TButton;
    printBorderInner: TCheckBox;
    printBorderOuter: TCheckBox;
    printBorderColorInnerLabel: TLabel;
    printBorderColorInner: TPanel;
    printBorderColorOuter: TPanel;
    printBorderColorOuterLabel: TLabel;
    printBorderWidthInnerLabel: TLabel;
    printBorderWidthOuterLabel: TLabel;
    printBorderWidthInner: TSpinEdit;
    printBorderWidthOuter: TSpinEdit;
    helpButton: TSpeedButton;
    procedure printBorderColorInnerMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure printBorderColorOuterMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure printBorderInnerClick(Sender: TObject);
    procedure printBorderOuterClick(Sender: TObject);
    procedure CloseClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
  public
    { Public declarations }
    options: BitmapOptionsStructure;
    transferDirection: smallint;
    optionsChanged: boolean;
    procedure initializeWithOptions(anOptions: BitmapOptionsStructure);
    procedure transferFields;
    procedure transferCheckBox(checkBox: TCheckBox; var value: boolean);
    procedure transferColor(colorPanel: TPanel; var value: TColorRef);
    procedure transferSmallintSpinEditBox(editBox: TSpinEdit; var value: smallint);
  end;

implementation

{$R *.DFM}

uses usupport;

const
  kTransferLoad = 1; kTransferSave = 2;

procedure TPrintBordersForm.initializeWithOptions(anOptions: BitmapOptionsStructure);
  begin
  options := anOptions;
  transferDirection := kTransferLoad;
	self.transferFields;
  // simple interaction, so just put it in here
  printBorderColorInner.enabled := printBorderInner.checked;
  printBorderWidthInner.enabled := printBorderInner.checked;
  printBorderColorInnerLabel.enabled := printBorderInner.checked;
  printBorderWidthInnerLabel.enabled := printBorderInner.checked;
  printBorderColorOuter.enabled := printBorderOuter.checked;
  printBorderWidthOuter.enabled := printBorderOuter.checked;
  printBorderColorOuterLabel.enabled := printBorderOuter.checked;
  printBorderWidthOuterLabel.enabled := printBorderOuter.checked;
  end;

procedure TPrintBordersForm.transferFields;
  begin
  self.transferCheckBox(printBorderInner, options.printBorderInner);
  self.transferCheckBox(printBorderOuter, options.printBorderOuter);
  self.transferColor(printBorderColorInner, options.printBorderColorInner);
  self.transferColor(printBorderColorOuter, options.printBorderColorOuter);
  self.transferSmallintSpinEditBox(printBorderWidthInner, options.printBorderWidthInner);
  self.transferSmallintSpinEditBox(printBorderWidthOuter, options.printBorderWidthOuter);
  end;

procedure TPrintBordersForm.transferCheckBox(checkBox: TCheckBox; var value: boolean);
  begin
  if transferDirection = kTransferLoad then
    checkBox.checked := value
  else if transferDirection = kTransferSave then
    begin
    if value <> checkBox.checked then
      optionsChanged := true;
    value := checkBox.checked;
    end;
  end;

procedure TPrintBordersForm.transferColor(colorPanel: TPanel; var value: TColorRef);
  begin
  if transferDirection = kTransferLoad then
    colorPanel.color := value
  else if transferDirection = kTransferSave then
    begin
    if value <> colorPanel.color then
      optionsChanged := true;
    value := colorPanel.color;
    end;
  end;

procedure TPrintBordersForm.transferSmallintSpinEditBox(editBox: TSpinEdit; var value: smallint);
  begin
  if transferDirection = kTransferLoad then
    editBox.text := intToStr(value)
  else if transferDirection = kTransferSave then
    begin
    if value <> strToIntDef(editBox.text, 0) then
      optionsChanged := true;
    value := strToIntDef(editBox.text, 0);
    end;
  end;

procedure TPrintBordersForm.printBorderColorInnerMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  printBorderColorInner.color := domain.getColorUsingCustomColors(printBorderColorInner.color);
  end;

procedure TPrintBordersForm.printBorderColorOuterMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  printBorderColorOuter.color := domain.getColorUsingCustomColors(printBorderColorOuter.color);
  end;

procedure TPrintBordersForm.printBorderInnerClick(Sender: TObject);
  begin
  printBorderColorInner.enabled := printBorderInner.checked;
  printBorderWidthInner.enabled := printBorderInner.checked;
  printBorderColorInnerLabel.enabled := printBorderInner.checked;
  printBorderWidthInnerLabel.enabled := printBorderInner.checked;
  end;

procedure TPrintBordersForm.printBorderOuterClick(Sender: TObject);
  begin
  printBorderColorOuter.enabled := printBorderOuter.checked;
  printBorderWidthOuter.enabled := printBorderOuter.checked;
  printBorderColorOuterLabel.enabled := printBorderOuter.checked;
  printBorderWidthOuterLabel.enabled := printBorderOuter.checked;
  end;

procedure TPrintBordersForm.CloseClick(Sender: TObject);
  begin
  transferDirection := kTransferSave;
  self.transferFields;
  modalResult := mrOK;
  end;

procedure TPrintBordersForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TPrintBordersForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Drawing_a_print_border');
  end;

procedure TPrintBordersForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

end.
