unit Ubrdopt;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, Buttons, StdCtrls, Spin, ExtCtrls, TabNotBk, ComCtrls,
  uplant, ubrstrat, udomain, updform, UWinSliders;

type
  TBreedingOptionsForm = class(PdForm)
    ok: TButton;
    cancel: TButton;
    upImage: TImage;
    downImage: TImage;
    breedingOptions: TTabbedNotebook;
    treatColorsAsNumbers: TCheckBox;
    chooseTdosRandomly: TCheckBox;
    currentTdoLibraryFileName: TEdit;
    weightLabel: TLabel;
    weightAmountLabel: TLabel;
    weightZero: TLabel;
    weightSlider: KfWinSlider;
    weightOneHundred: TLabel;
    weightSelectAll: TButton;
    weightSelectNone: TButton;
    weightSections: TListBox;
    mutationLabel: TLabel;
    mutationAmountLabel: TLabel;
    mutationZero: TLabel;
    mutationSlider: KfWinSlider;
    mutationOneHundred: TLabel;
    mutationSections: TListBox;
    mutationSelectAll: TButton;
    mutationSelectNone: TButton;
    nonNumericLabel: TLabel;
    firstPlantIfEqualLabel: TLabel;
    alwaysCopyFromFirstPlant: TRadioButton;
    alwaysCopyFromSecondPlant: TRadioButton;
    copyRandomlyBasedOnWeights: TRadioButton;
    copyBasedOnWeightsIfEqualFirstPlant: TRadioButton;
    copyBasedOnWeightsIfEqualSecondPlant: TRadioButton;
    copyBasedOnWeightsIfEqualChooseRandomly: TRadioButton;
    helpButton: TSpeedButton;
    mutationShowSections: TSpeedButton;
    weightShowSections: TSpeedButton;
    changeTdoLibrary: TSpeedButton;
    GroupBox1: TGroupBox;
    Label4: TLabel;
    Label1: TLabel;
    Label2: TLabel;
    thumbnailWidth: TSpinEdit;
    thumbnailHeight: TSpinEdit;
    GroupBox2: TGroupBox;
    Label3: TLabel;
    plantsPerGeneration: TSpinEdit;
    Label6: TLabel;
    maxGenerations: TSpinEdit;
    Label8: TLabel;
    Label7: TLabel;
    percentMaxAge: TSpinEdit;
    maxPartsPerPlant_thousands: TSpinEdit;
    Label9: TLabel;
    GroupBox3: TGroupBox;
    numTimeSeriesStages: TSpinEdit;
    Label5: TLabel;
    updateTimeSeriesPlantsOnParameterChange: TCheckBox;
    procedure FormCreate(Sender: TObject);
    procedure mutationShowSectionsClick(Sender: TObject);
    procedure weightShowSectionsClick(Sender: TObject);
    procedure mutationSectionsDrawItem(Control: TWinControl;
      Index: Integer; Rect: TRect; State: TOwnerDrawState);
    procedure weightSectionsDrawItem(Control: TWinControl; Index: Integer;
      Rect: TRect; State: TOwnerDrawState);
    procedure mutationSelectAllClick(Sender: TObject);
    procedure mutationSelectNoneClick(Sender: TObject);
    procedure weightSelectAllClick(Sender: TObject);
    procedure weightSelectNoneClick(Sender: TObject);
    procedure copyBasedOnWeightsIfEqualFirstPlantClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure alwaysCopyFromFirstPlantClick(Sender: TObject);
    procedure alwaysCopyFromSecondPlantClick(Sender: TObject);
    procedure copyRandomlyBasedOnWeightsClick(Sender: TObject);
    procedure copyBasedOnWeightsIfEqualSecondPlantClick(Sender: TObject);
    procedure copyBasedOnWeightsIfEqualChooseRandomlyClick(
      Sender: TObject);
    procedure mutationSectionsClick(Sender: TObject);
    procedure weightSectionsClick(Sender: TObject);
    procedure okClick(Sender: TObject);
    procedure treatColorsAsNumbersClick(Sender: TObject);
    procedure chooseTdosRandomlyClick(Sender: TObject);
    procedure weightSliderMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure weightSliderMouseMove(Sender: TObject; Shift: TShiftState; X,
      Y: Integer);
    procedure weightSliderMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure weightSliderKeyUp(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure mutationSliderMouseDown(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure mutationSliderMouseMove(Sender: TObject; Shift: TShiftState;
      X, Y: Integer);
    procedure mutationSliderMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure mutationSliderKeyUp(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure changeTdoLibraryClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure plantsPerGenerationChange(Sender: TObject);
    procedure thumbnailWidthChange(Sender: TObject);
    procedure thumbnailHeightChange(Sender: TObject);
    procedure maxGenerationsChange(Sender: TObject);
    procedure numTimeSeriesStagesChange(Sender: TObject);
    procedure percentMaxAgeChange(Sender: TObject);
    procedure maxPartsPerPlant_thousandsChange(Sender: TObject);
    procedure updateTimeSeriesPlantsOnParameterChangeClick(
      Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    options: BreedingAndTimeSeriesOptionsStructure;
    domainOptions: DomainOptionsStructure;
    draggingMutationSlider, draggingWeightSlider: boolean;
    mutationSectionsOpen, weightSectionsOpen: boolean;
    procedure initializeWithBreedingAndTimeSeriesOptionsAndDomainOptions(
      anOptions: BreedingAndTimeSeriesOptionsStructure; aDomainOptions: DomainOptionsStructure);
    procedure loadSectionsIntoListBoxes;
    procedure drawSectionsListBoxItem(Control: TWinControl; Index: Integer; Rect: TRect; State: TOwnerDrawState);
    procedure updateComponentsFromOptions;
    procedure updateSliderForSelectedSections(which: smallint; isOpen: boolean;
        aSlider: KfWinSlider; aListBox: TListBox; aLabel: TLabel);
    function firstSelectedIndex(aListBox: TListBox): smallint;
    procedure updateOptionsForNonNumericChoice;
    function radioButtonForChoiceIndex(index: smallint): TRadioButton;
    function choiceIndexForRadioButton(radio: TRadioButton): smallint;
    procedure updateMutationOrWeightFromSlider(which: smallint; isOpen: boolean; aListBox: TListBox; aSlider: KfWinSlider);
    end;

implementation

{$R *.DFM}

uses
  umain, usection, usupport, ucommand, updcom, ucursor;

const
  kBetweenGap = 4;
  kMaxPlantNameLength = 20;

{ ---------------------------------------------------------------------------------------- create/destroy }
procedure TBreedingOptionsForm.FormCreate(Sender: TObject);
  begin
  breedingOptions.pageIndex := 0;
  mutationSections.visible := false;
  mutationSelectAll.visible := false;
  mutationSelectNone.visible := false;
  weightSections.visible := false;
  weightSelectAll.visible := false;
  weightSelectNone.visible := false;
  self.loadSectionsIntoListBoxes;
  currentTdoLibraryFileName.text := domain.defaultTdoLibraryFileName;
  currentTdoLibraryFileName.selStart := length(currentTdoLibraryFileName.text);
  end;

procedure TBreedingOptionsForm.initializeWithBreedingAndTimeSeriesOptionsAndDomainOptions(
    anOptions: BreedingAndTimeSeriesOptionsStructure; aDomainOptions: DomainOptionsStructure);
  begin
  options := anOptions;
  domainOptions := aDomainOptions;
  self.updateComponentsFromOptions;
  end;

{ ------------------------------------------------------------------------------- buttons }
procedure TBreedingOptionsForm.okClick(Sender: TObject);
  begin
  modalResult := mrOk;
  end;

procedure TBreedingOptionsForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

{ ---------------------------------------------------------------------------- reading breeding options }
procedure TBreedingOptionsForm.updateComponentsFromOptions;
  begin
  mutationSections.invalidate;
  weightSections.invalidate;
  self.mutationSectionsClick(self);
  self.weightSectionsClick(self);
  if self.radioButtonForChoiceIndex(options.getNonNumericalParametersFrom) <> nil then
    self.radioButtonForChoiceIndex(options.getNonNumericalParametersFrom).checked := true;
  treatColorsAsNumbers.checked := options.mutateAndBlendColorValues;
  chooseTdosRandomly.checked := options.chooseTdosRandomlyFromCurrentLibrary;
  // v2.0
  plantsPerGeneration.value := options.plantsPerGeneration;
  thumbnailWidth.value := options.thumbnailWidth;
  thumbnailHeight.value := options.thumbnailHeight;
  maxGenerations.value := options.maxGenerations;
  numTimeSeriesStages.value := options.numTimeSeriesStages;
  percentMaxAge.value := options.percentMaxAge;
  // v2.0 domain options moved from main options dialog
  maxPartsPerPlant_thousands.value := domainOptions.maxPartsPerPlant_thousands;
  updateTimeSeriesPlantsOnParameterChange.checked := domainOptions.updateTimeSeriesPlantsOnParameterChange;
  end;

function TBreedingOptionsForm.radioButtonForChoiceIndex(index: smallint): TRadioButton;
  begin
  result := nil;
  case index of
    kFromFirstPlant: result := alwaysCopyFromFirstPlant;
    kFromSecondPlant: result := alwaysCopyFromSecondPlant;
    kFromProbabilityBasedOnWeightsForSection: result := copyRandomlyBasedOnWeights;
    kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant: result := copyBasedOnWeightsIfEqualFirstPlant;
    kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant: result := copyBasedOnWeightsIfEqualSecondPlant;
    kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly: result := copyBasedOnWeightsIfEqualChooseRandomly;
    end;
  end;

function TBreedingOptionsForm.choiceIndexForRadioButton(radio: TRadioButton): smallint;
  begin
  result := 0;
  if radio = alwaysCopyFromFirstPlant then
    result := kFromFirstPlant
  else if radio = alwaysCopyFromSecondPlant then
    result := kFromSecondPlant
  else if radio = copyRandomlyBasedOnWeights then
    result := kFromProbabilityBasedOnWeightsForSection
  else if radio = copyBasedOnWeightsIfEqualFirstPlant then
    result := kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant
  else if radio = copyBasedOnWeightsIfEqualSecondPlant then
    result := kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant
  else if radio = copyBasedOnWeightsIfEqualChooseRandomly then
    result := kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly;
  end;

{ ------------------------------------------------------------ changing breeding strategy }
procedure TBreedingOptionsForm.mutationSliderMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  if (self.firstSelectedIndex(mutationSections) >= 0) or (not mutationSectionsOpen) then
    draggingMutationSlider := true;
  end;

procedure TBreedingOptionsForm.mutationSliderMouseMove(Sender: TObject;
  Shift: TShiftState; X, Y: Integer);
  begin
  if draggingMutationSlider then
    begin
    mutationAmountLabel.caption := intToStr(mutationSlider.currentValue) + '%';
    self.updateMutationOrWeightFromSlider(kMutation, mutationSectionsOpen, mutationSections, mutationSlider);
    end;
  end;

procedure TBreedingOptionsForm.mutationSliderMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  draggingMutationSlider := false;
  self.updateMutationOrWeightFromSlider(kMutation, mutationSectionsOpen, mutationSections, mutationSlider);
  end;

procedure TBreedingOptionsForm.mutationSliderKeyUp(Sender: TObject;
  var Key: Word; Shift: TShiftState);
  begin
  self.updateMutationOrWeightFromSlider(kMutation, mutationSectionsOpen, mutationSections, mutationSlider);
  end;

procedure TBreedingOptionsForm.weightSliderMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  if (self.firstSelectedIndex(weightSections) >= 0) or (not weightSectionsOpen) then
    draggingWeightSlider := true;
  end;

procedure TBreedingOptionsForm.weightSliderMouseMove(Sender: TObject;
  Shift: TShiftState; X, Y: Integer);
  begin
  if draggingWeightSlider then
    weightAmountLabel.caption := intToStr(weightSlider.currentValue) + '%';
  end;

procedure TBreedingOptionsForm.weightSliderMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  draggingWeightSlider := false;
  self.updateMutationOrWeightFromSlider(kWeight, weightSectionsOpen, weightSections, weightSlider);
  end;

procedure TBreedingOptionsForm.weightSliderKeyUp(Sender: TObject;
  var Key: Word; Shift: TShiftState);
  begin
  self.updateMutationOrWeightFromSlider(kWeight, weightSectionsOpen, weightSections, weightSlider);
  end;

procedure TBreedingOptionsForm.updateMutationOrWeightFromSlider(which: smallint; isOpen: boolean;
    aListBox: TListBox; aSlider: KfWinSlider);
  var
    i: smallint;
  begin
  if aListBox.items.count > 0 then for i := 0 to aListBox.items.count - 1 do
    begin
    if aListBox.selected[i] or (not isOpen) then
      begin
      if which = kMutation then
        options.mutationStrengths[i] := aSlider.currentValue
      else
        options.firstPlantWeights[i] := aSlider.currentValue;
      end;
    end;
  aListBox.invalidate;
  end;

procedure TBreedingOptionsForm.alwaysCopyFromFirstPlantClick(Sender: TObject);
  begin
  self.updateOptionsForNonNumericChoice;
  end;

procedure TBreedingOptionsForm.alwaysCopyFromSecondPlantClick(Sender: TObject);
  begin
  self.updateOptionsForNonNumericChoice;
  end;

procedure TBreedingOptionsForm.copyRandomlyBasedOnWeightsClick(Sender: TObject);
  begin
  self.updateOptionsForNonNumericChoice;
  end;

procedure TBreedingOptionsForm.copyBasedOnWeightsIfEqualFirstPlantClick(Sender: TObject);
  begin
  self.updateOptionsForNonNumericChoice;
  end;

procedure TBreedingOptionsForm.copyBasedOnWeightsIfEqualSecondPlantClick(Sender: TObject);
  begin
  self.updateOptionsForNonNumericChoice;
  end;

procedure TBreedingOptionsForm.copyBasedOnWeightsIfEqualChooseRandomlyClick(Sender: TObject);
  begin
  self.updateOptionsForNonNumericChoice;
  end;

procedure TBreedingOptionsForm.updateOptionsForNonNumericChoice;
  var
    i: smallint;
    radio: TRadioButton;
  begin
  // this will work so long as there are no other radio buttons on the notebook
  if breedingOptions.controlCount > 0 then for i := 1 to breedingOptions.controlCount - 1 do
    if (breedingOptions.controls[i] is TRadioButton) then
      begin
      radio := (breedingOptions.controls[i] as TRadioButton);
      if radio.checked then
        options.getNonNumericalParametersFrom := choiceIndexForRadioButton(radio);
      break;
      end;
  end;

procedure TBreedingOptionsForm.treatColorsAsNumbersClick(Sender: TObject);
  begin
  options.mutateAndBlendColorValues := treatColorsAsNumbers.checked;
  end;

procedure TBreedingOptionsForm.chooseTdosRandomlyClick(Sender: TObject);
  begin
  options.chooseTdosRandomlyFromCurrentLibrary := chooseTdosRandomly.checked;
  end;

{ ------------------------------------------------------------------ sections list boxes }
procedure TBreedingOptionsForm.loadSectionsIntoListBoxes;
  var
    section: PdSection;
    i: smallint;
  begin
  if (domain = nil) or (domain.sectionManager = nil) then exit;
  mutationSections.clear;
  weightSections.clear;
  if domain.sectionManager.sections.count > 0 then
    for i := 0 to domain.sectionManager.sections.count - 1 do
      begin
      section := PdSection(domain.sectionManager.sections.items[i]);
      if section.showInParametersWindow then
        begin
        mutationSections.items.addObject(section.getName, section);
        weightSections.items.addObject(section.getName, section);
        end;
      end;
  end;

procedure TBreedingOptionsForm.mutationSectionsDrawItem(Control: TWinControl;
  Index: Integer; Rect: TRect; State: TOwnerDrawState);
  begin
  self.drawSectionsListBoxItem(control, index, rect, state);
  end;

procedure TBreedingOptionsForm.weightSectionsDrawItem(Control: TWinControl;
  Index: Integer; Rect: TRect; State: TOwnerDrawState);
  begin
  self.drawSectionsListBoxItem(control, index, rect, state);
  end;

procedure TBreedingOptionsForm.drawSectionsListBoxItem(Control: TWinControl;
  Index: Integer; Rect: TRect; State: TOwnerDrawState);
  var
    sectionsListBox: TListBox;
	  section: PdSection;
    selected: boolean;
    cText: array[0..255] of Char;
  begin
  if Application.terminated then exit;
  sectionsListBox := control as TListBox;
  if sectionsListBox = nil then exit;
  if (sectionsListBox.items.count <= 0) or (index < 0) or (index > sectionsListBox.items.count - 1) then exit;
  selected := (odSelected in state);
  { set up section pointer }
  section := sectionsListBox.items.objects[index] as PdSection;
  if section = nil then exit;
  with sectionsListBox.canvas do
    begin
    font := sectionsListBox.font;
    if selected then
      begin
      brush.color := clHighlight;
      font.color := clHighlightText;
      end
    else
      begin
      brush.color := sectionsListBox.color;
      font.color := clBtnText;
      end;
    fillRect(rect);
    if sectionsListBox = mutationSections then
      strPCopy(cText, section.getName + ' ' + intToStr(options.mutationStrengths[index]) + '%')
    else
      strPCopy(cText, section.getName + ' '
          + intToStr(options.firstPlantWeights[index]) + '/'
          + intToStr(100 - options.firstPlantWeights[index]));
    rect.left := rect.left + 2; { margin for text }
    winprocs.drawText(handle, cText, strLen(cText), rect, DT_LEFT);
    end;
  end;

procedure TBreedingOptionsForm.mutationSectionsClick(Sender: TObject);
  begin
  self.updateSliderForSelectedSections(kMutation, mutationSectionsOpen,
      mutationSlider, mutationSections, mutationAmountLabel);
  end;

procedure TBreedingOptionsForm.weightSectionsClick(Sender: TObject);
  begin
  self.updateSliderForSelectedSections(kWeight, weightSectionsOpen,
      weightSlider, weightSections, weightAmountLabel);
  end;

procedure TBreedingOptionsForm.updateSliderForSelectedSections(which: smallint; isOpen: boolean;
    aSlider: KfWinSlider; aListBox: TListBox; aLabel: TLabel);
  var
    firstSelectedIndex: smallint;
  begin
  if isOpen then
    firstSelectedIndex := self.firstSelectedIndex(aListBox)
  else
    firstSelectedIndex := 0;
  aSlider.enabled := (firstSelectedIndex >= 0) or (not isOpen);
  if firstSelectedIndex >= 0 then
    begin
    if which = kMutation then
      aSlider.currentValue := options.mutationStrengths[firstSelectedIndex]
    else
      aSlider.currentValue := options.firstPlantWeights[firstSelectedIndex];
    end
  else
    aSlider.currentValue := 0;
  aLabel.caption := intToStr(aSlider.currentValue) + '%';
  aLabel.enabled := aSlider.enabled;
  aSlider.invalidate;
  end;

function TBreedingOptionsForm.firstSelectedIndex(aListBox: TListBox): smallint;
  var
    i: smallint;
  begin
  result := -1;
  if aListBox.items.count <= 0 then exit;
  if aListBox.selCount < 1 then exit;
  for i := 0 to aListBox.items.count - 1 do
    if aListBox.selected[i] then
      begin
      result := i;
      exit;
      end;
  end;

procedure TBreedingOptionsForm.mutationShowSectionsClick(Sender: TObject);
  begin
  mutationSectionsOpen := not mutationSectionsOpen;
  if mutationSectionsOpen then
    begin
    mutationShowSections.glyph := upImage.picture.bitmap;
    mutationSections.visible := true;
    mutationSelectAll.visible := true;
    mutationSelectNone.visible := true;
    { select all }
    self.mutationSelectAllClick(self);
    self.mutationSectionsClick(self);
    end
  else
    begin
    mutationSections.visible := false;
    mutationSelectAll.visible := false;
    mutationSelectNone.visible := false;
    mutationShowSections.glyph := downImage.picture.bitmap;
    self.mutationSectionsClick(self);
    end;
    mutationSections.visible := mutationSectionsOpen;
  end;

procedure TBreedingOptionsForm.weightShowSectionsClick(Sender: TObject);
  begin
  weightSectionsOpen := not weightSectionsOpen;
  if weightSectionsOpen then
    begin
    weightShowSections.glyph := upImage.picture.bitmap;
    weightSections.visible := true;
    weightSelectAll.visible := true;
    weightSelectNone.visible := true;
    { select all }
    self.weightSelectAllClick(self);
    self.weightSectionsClick(self);
    end
  else
    begin
    weightSections.visible := false;
    weightSelectAll.visible := false;
    weightSelectNone.visible := false;
    weightShowSections.glyph := downImage.picture.bitmap;
    self.weightSectionsClick(self);
    end;
  weightSections.visible := weightSectionsOpen;
  end;

procedure TBreedingOptionsForm.mutationSelectAllClick(Sender: TObject);
  var
    i: smallint;
  begin
  if mutationSections.items.count > 0 then for i := 0 to mutationSections.items.count - 1 do
    mutationSections.selected[i] := true;
  end;

procedure TBreedingOptionsForm.mutationSelectNoneClick(Sender: TObject);
  var
    i: smallint;
  begin
  if mutationSections.items.count > 0 then for i := 0 to mutationSections.items.count - 1 do
    mutationSections.selected[i] := false;
  end;

procedure TBreedingOptionsForm.weightSelectAllClick(Sender: TObject);
  var
    i: smallint;
  begin
  if weightSections.items.count > 0 then for i := 0 to weightSections.items.count - 1 do
    weightSections.selected[i] := true;
  end;

procedure TBreedingOptionsForm.weightSelectNoneClick(Sender: TObject);
  var
    i: smallint;
  begin
  if weightSections.items.count > 0 then for i := 0 to weightSections.items.count - 1 do
    weightSections.selected[i] := false;
  end;

procedure TBreedingOptionsForm.changeTdoLibraryClick(Sender: TObject);
   var
    fileNameWithPath: string;
  begin
  fileNameWithPath := getFileOpenInfo(kFileTypeTdo, domain.defaultTdoLibraryFileName,
      'Choose a 3D object library (tdo) file');
  if fileNameWithPath = '' then exit;
  currentTdoLibraryFileName.text := fileNameWithPath;
  domain.defaultTdoLibraryFileName := currentTdoLibraryFileName.text;
  currentTdoLibraryFileName.selStart := length(currentTdoLibraryFileName.text);
  end;

procedure TBreedingOptionsForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Changing_breeding_options');
  end;

procedure TBreedingOptionsForm.plantsPerGenerationChange(Sender: TObject);
  var oldValue: smallint;
  begin
  oldValue := options.plantsPerGeneration;
  try
    options.plantsPerGeneration := plantsPerGeneration.value;
  except
    options.plantsPerGeneration := oldValue;
  end;
  end;

procedure TBreedingOptionsForm.thumbnailWidthChange(Sender: TObject);
  var oldValue: smallint;
  begin
  oldValue := options.thumbnailWidth;
  try
    options.thumbnailWidth := thumbnailWidth.value;
  except
    options.thumbnailWidth := oldValue;
  end;
  end;

procedure TBreedingOptionsForm.thumbnailHeightChange(Sender: TObject);
  var oldValue: smallint;
  begin
  oldValue := options.thumbnailHeight;
  try
    options.thumbnailHeight := thumbnailHeight.value;
  except
    options.thumbnailHeight := oldValue;
  end;
  end;

procedure TBreedingOptionsForm.maxGenerationsChange(Sender: TObject);
  var oldValue: smallint;
  begin
  oldValue := options.maxGenerations;
  try
    options.maxGenerations := maxGenerations.value;
  except
    options.maxGenerations := oldValue;
  end;
  end;

procedure TBreedingOptionsForm.numTimeSeriesStagesChange(Sender: TObject);
  var oldValue: smallint;
  begin
  oldValue := options.numTimeSeriesStages;
  try
    options.numTimeSeriesStages := numTimeSeriesStages.value;
  except
    options.numTimeSeriesStages := oldValue;
  end;
  end;

procedure TBreedingOptionsForm.percentMaxAgeChange(Sender: TObject);
  var oldValue: smallint;
  begin
  oldValue := options.percentMaxAge;
  try
    options.percentMaxAge := percentMaxAge.value;
  except
    options.percentMaxAge := oldValue;
  end;
  end;

procedure TBreedingOptionsForm.maxPartsPerPlant_thousandsChange(Sender: TObject);
  var oldValue: smallint;
  begin
  oldValue := domainOptions.maxPartsPerPlant_thousands;
  try
    domainOptions.maxPartsPerPlant_thousands := maxPartsPerPlant_thousands.value;
  except
    domainOptions.maxPartsPerPlant_thousands := oldValue;
  end;
  end;

procedure TBreedingOptionsForm.updateTimeSeriesPlantsOnParameterChangeClick(Sender: TObject);
  begin
  domainOptions.updateTimeSeriesPlantsOnParameterChange := updateTimeSeriesPlantsOnParameterChange.checked;
  end;

end.
