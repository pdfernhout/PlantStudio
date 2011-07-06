unit Uoptions;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, Buttons, StdCtrls, Spin, ExtCtrls, TabNotBk,
  udomain, updform, ComCtrls;

type
  TOptionsForm = class(PdForm) 
    Close: TButton;
    cancel: TButton;
    optionsNotebook: TTabbedNotebook;
    drawWithOpenGL: TCheckBox;
    wholeProgramBox: TGroupBox;
    backgroundColor: TPanel;
    backgroundColorLabel: TLabel;
    showPlantDrawingProgress: TCheckBox;
    GroupBox1: TGroupBox;
    firstSelectionRectangleColorLabel: TLabel;
    multiSelectionRectangleColorLabel: TLabel;
    firstSelectionRectangleColor: TPanel;
    multiSelectionRectangleColor: TPanel;
    GroupBox2: TGroupBox;
    rotationIncrementLabel: TLabel;
    nudgeDistanceLabel: TLabel;
    rotationIncrement: TSpinEdit;
    nudgeDistance: TSpinEdit;
    GroupBox6: TGroupBox;
    parametersFontSizeLabel: TLabel;
    useMetricUnits: TCheckBox;
    parametersFontSize: TSpinEdit;
    GroupBox7: TGroupBox;
    pauseBeforeHintLabel: TLabel;
    pauseDuringHintLabel: TLabel;
    openMostRecentFileAtStart: TCheckBox;
    pauseBeforeHint: TSpinEdit;
    pauseDuringHint: TSpinEdit;
    helpButton: TSpeedButton;
    resizeKeyUpMultiplierPercent: TSpinEdit;
    resizeDistanceLabel: TLabel;
    mainWindowDrawingOptionsBox: TGroupBox;
    customDrawOptions: TButton;
    Label1: TLabel;
    transparentColor: TPanel;
    transparentColorLabel: TLabel;
    memoryLimitForPlantBitmaps_MB: TSpinEdit;
    memoryLimitLabel: TLabel;
    Panel1: TPanel;
    Image1: TImage;
    pasteRectSize: TSpinEdit;
    pasteRectSizeLabel: TLabel;
    GroupBox4: TGroupBox;
    Label9: TLabel;
    Label10: TLabel;
    ghostingColor: TPanel;
    nonHiddenPosedColor: TPanel;
    selectedPosedColor: TPanel;
    Label3: TLabel;
    GroupBox5: TGroupBox;
    undoLimitLabel: TLabel;
    undoLimitOfPlantsLabel: TLabel;
    undoLimit: TSpinEdit;
    undoLimitOfPlants: TSpinEdit;
    resizeRectSize: TSpinEdit;
    resizeRectSizeLabel: TLabel;
    ignoreWindowSettingsInFile: TCheckBox;
    procedure FormActivate(Sender: TObject);
    procedure CloseClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure backgroundColorMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure firstSelectionRectangleColorMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure multiSelectionRectangleColorMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure FormCreate(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure customDrawOptionsClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure transparentColorMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure Image1Click(Sender: TObject);
    procedure ghostingColorMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure nonHiddenPosedColorMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure selectedPosedColorMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  private
    { Private declarations }
  public
    { Public declarations }
    transferDirection: smallint;
    options: DomainOptionsStructure;
    optionsChanged: boolean;
    messageShown: smallint;
    procedure transferFields;
    procedure transferCheckBox(checkBox: TCheckBox; var value: boolean);
    procedure transferColor(colorPanel: TPanel; var value: TColorRef);
    procedure transferSmallintSpinEditBox(editBox: TSpinEdit; var value: smallint);
    procedure transferFloatEditBox(editBox: TEdit; var value: single);
  end;

implementation

{$R *.DFM}

uses usupport, umath, ucustdrw, u3dexport;

const
  kTransferLoad = 1;
  kTransferSave = 2;

procedure TOptionsForm.FormCreate(Sender: TObject);
  begin
  optionsNotebook.pageIndex := 0;
  end;

procedure TOptionsForm.FormActivate(Sender: TObject);
  begin
  transferDirection := kTransferLoad;
	self.transferFields;
  end;

procedure TOptionsForm.CloseClick(Sender: TObject);
  begin
  transferDirection := kTransferSave;
	self.transferFields;
  modalResult := mrOK;
  end;

procedure TOptionsForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TOptionsForm.transferFields;
  begin
  // DRAWING
  transferSmallintSpinEditBox(memoryLimitForPlantBitmaps_MB, options.memoryLimitForPlantBitmaps_MB);
  transferColor(backgroundColor, options.backgroundColor);
  transferColor(transparentColor, options.transparentColor);
  transferCheckBox(showPlantDrawingProgress, options.showPlantDrawingProgress);
  // SELECTING
  transferColor(firstSelectionRectangleColor, options.firstSelectionRectangleColor);
  transferColor(multiSelectionRectangleColor, options.multiSelectionRectangleColor);
  transferSmallintSpinEditBox(resizeRectSize, options.resizeRectSize);
  transferColor(ghostingColor, options.ghostingColor);
  transferColor(nonHiddenPosedColor, options.nonHiddenPosedColor);
  transferColor(selectedPosedColor, options.selectedPosedColor);
  // EDITING
  transferSmallintSpinEditBox(rotationIncrement, options.rotationIncrement);
  transferSmallintSpinEditBox(nudgeDistance, options.nudgeDistance);
  transferSmallintSpinEditBox(resizeKeyUpMultiplierPercent, options.resizeKeyUpMultiplierPercent);
  transferSmallintSpinEditBox(pasteRectSize, options.pasteRectSize);
  // UNDOING
  transferSmallintSpinEditBox(undoLimit, options.undoLimit);
  transferSmallintSpinEditBox(undoLimitOfPlants, options.undoLimitOfPlants);
  // MISCELLANEOUS
  transferCheckBox(openMostRecentFileAtStart, options.openMostRecentFileAtStart);
  transferCheckBox(ignoreWindowSettingsInFile, options.ignoreWindowSettingsInFile); // v2.1
  transferCheckBox(useMetricUnits, options.useMetricUnits);
  transferSmallintSpinEditBox(parametersFontSize, options.parametersFontSize);
  transferSmallintSpinEditBox(pauseBeforeHint, options.pauseBeforeHint);
  transferSmallintSpinEditBox(pauseDuringHint, options.pauseDuringHint);
  end;

procedure TOptionsForm.transferCheckBox(checkBox: TCheckBox; var value: boolean);
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

procedure TOptionsForm.transferColor(colorPanel: TPanel; var value: TColorRef);
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

procedure TOptionsForm.transferSmallintSpinEditBox(editBox: TSpinEdit; var value: smallint);
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

procedure TOptionsForm.transferFloatEditBox(editBox: TEdit; var value: single);
  var
    oldValue, newValue: single;
  begin
  if transferDirection = kTransferLoad then
    editBox.text := digitValueString(value)
  else if transferDirection = kTransferSave then
    begin
    oldValue := value;
    try
      newValue := strToFloat(editBox.text);
    except
      newValue := oldValue;
    end;
    if value <> newValue then
      optionsChanged := true;
    value := newValue;
    end;
  end;

procedure TOptionsForm.backgroundColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  backgroundColor.color := domain.getColorUsingCustomColors(backgroundColor.color);
  end;

procedure TOptionsForm.transparentColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  // leave this enabled even if not using private bitmaps
  transparentColor.color := domain.getColorUsingCustomColors(transparentColor.color);
  end;

procedure TOptionsForm.firstSelectionRectangleColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  firstSelectionRectangleColor.color := domain.getColorUsingCustomColors(firstSelectionRectangleColor.color);
  end;

procedure TOptionsForm.multiSelectionRectangleColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  multiSelectionRectangleColor.color := domain.getColorUsingCustomColors(multiSelectionRectangleColor.color);
  end;

procedure TOptionsForm.ghostingColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  ghostingColor.color := domain.getColorUsingCustomColors(ghostingColor.color);
  end;

procedure TOptionsForm.nonHiddenPosedColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  nonHiddenPosedColor.color := domain.getColorUsingCustomColors(nonHiddenPosedColor.color);
  end;

procedure TOptionsForm.selectedPosedColorMouseUp(
  Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  selectedPosedColor.color := domain.getColorUsingCustomColors(selectedPosedColor.color);
  end;

procedure TOptionsForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

procedure TOptionsForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Changing_preferences');
  end;

procedure TOptionsForm.customDrawOptionsClick(Sender: TObject);
  var
    customDrawForm: TCustomDrawOptionsForm;
    response: integer;
  begin
  customDrawForm := TCustomDrawOptionsForm.create(self);
  if customDrawForm = nil then
    raise Exception.create('Problem: Could not create 3D object mover window.');
  try
    customDrawForm.options := self.options;
    response := customDrawForm.showModal;
    if (response = mrOK) and (customDrawForm.optionsChanged) then
      begin
      self.options := customDrawForm.options;
      optionsChanged := true;
      end;
  finally
    customDrawForm.free;
  end;
  end;

procedure TOptionsForm.Image1Click(Sender: TObject);
  begin
  case messageShown of
    0: showMessage('We would like to take this opportunity'
        + chr(13) + 'to say thank you to our excellent testers, '
        + chr(13) + 'especially Ana, Joanne and Randy.');
    1: showMessage('Thanks to our parents and families.');
    2: showMessage('Thanks to our dogs Maize and Comet' + chr(13) + 'for their many interesting suggestions.');
    3: showMessage('Thanks to those who have graciously supported our work.');
    4: showMessage('Thanks to everyone who sent letters.');
    5: showMessage('Thanks to those who have spread the word about PlantStudio.');
    6: showMessage('And thank YOU for trying PlantStudio!');
    end;
  inc(messageShown);
  end;

end.
