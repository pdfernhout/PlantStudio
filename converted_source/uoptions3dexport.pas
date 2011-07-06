unit uoptions3dexport;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Buttons, ExtCtrls, StdCtrls, Spin,
  uturtle, u3dexport, Grids,
  updform;

type
  TGeneric3DOptionsForm = class(PdForm)
    drawWhichPlantsGroupBox: TGroupBox;
    useSelectedPlants: TRadioButton;
    useVisiblePlants: TRadioButton;
    useAllPlants: TRadioButton;
    otherGroupBox: TGroupBox;
    translatePlantsToWindowPositions: TCheckBox;
    dxfColorsGroupBox: TGroupBox;
    colorDXFFromRGB: TRadioButton;
    colorDXFFromOneColor: TRadioButton;
    wholePlantColor: TPanel;
    colorDXFFromPlantPartType: TRadioButton;
    colorsByPlantPart: TListBox;
    setPlantPartColor: TButton;
    povLimitsGroupBox: TGroupBox;
    Label4: TLabel;
    Label5: TLabel;
    minLineLengthToWrite: TEdit;
    minTdoScaleToWrite: TEdit;
    nestingGroupBox: TGroupBox;
    nestLeafAndPetiole: TCheckBox;
    nestCompoundLeaf: TCheckBox;
    nestInflorescence: TCheckBox;
    nestPedicelAndFlowerFruit: TCheckBox;
    nestFloralLayers: TCheckBox;
    commentOutUnionAtEnd: TCheckBox;
    layeringOption: TRadioGroup;
    writeColors: TCheckBox;
    Close: TButton;
    cancel: TButton;
    helpButton: TSpeedButton;
    threeDSWarningPanel: TPanel;
    Label6: TLabel;
    plantNameAndCylinderSidesPanel: TPanel;
    Label2: TLabel;
    Label3: TLabel;
    stemCylinderFacesLabel: TLabel;
    sidesLabel: TLabel;
    lengthOfShortName: TSpinEdit;
    stemCylinderFaces: TSpinEdit;
    dxfWriteColors: TCheckBox;
    reorientGroupBox: TGroupBox;
    xRotationBeforeDraw: TSpinEdit;
    writePlantNumberInFrontOfName: TCheckBox;
    vrmlVersionRadioGroup: TRadioGroup;
    Label10: TLabel;
    Label1: TLabel;
    overallScalingFactor_pct: TSpinEdit;
    Label9: TLabel;
    Label7: TLabel;
    estimationStringGrid: TStringGrid;
    pressPlantsPanel: TPanel;
    pressPlants: TCheckBox;
    directionToPressPlants: TComboBox;
    Label8: TLabel;
    makeTrianglesDoubleSided: TCheckBox;
    procedure FormActivate(Sender: TObject);
    procedure CloseClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure colorsByPlantPartDrawItem(Control: TWinControl;
      Index: Integer; Rect: TRect; State: TOwnerDrawState);
    procedure wholePlantColorMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure setPlantPartColorClick(Sender: TObject);
    procedure colorsByPlantPartDblClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure useSelectedPlantsClick(Sender: TObject);
    procedure useVisiblePlantsClick(Sender: TObject);
    procedure useAllPlantsClick(Sender: TObject);
    procedure stemCylinderFacesChange(Sender: TObject);
    procedure dxfWriteColorsClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    outputType: smallint;
    transferDirection: smallint;
    options: FileExport3DOptionsStructure;
    optionsChanged: boolean;
    totalPlants, totalParts, totalPoints, totalTriangles, totalMaterials: longint;
    procedure rearrangeItemsForOutputType;
    procedure transferFields;
    procedure fillPlantPartColors;
    function estimateBytes(numPlants, numParts, numPoints, numTriangles: longint): longint;
    procedure transferRadioButton(radioButton: TRadioButton; var value: smallint; radioIndex: smallint);
    procedure transferCheckBox(checkBox: TCheckBox; var value: boolean);
    procedure transferColor(colorPanel: TPanel; var value: TColorRef);
    procedure transferSmallintSpinEditBox(editBox: TSpinEdit; var value: smallint);
    procedure transferRadioGroup(radioGroup: TRadioGroup; var value: smallint);
    procedure transferComboBox(comboBox: TComboBox; var value: smallint);
    procedure transferSingleEditBox(editBox: TEdit; var value: single);
    procedure updatePredictedSizeDisplay;
  end;

implementation

{$R *.DFM}

uses WinProcs,
  usupport, udxfclr, udomain, umain, uplant;

const
  kTransferLoad = 1;
  kTransferSave = 2;

procedure TGeneric3DOptionsForm.FormActivate(Sender: TObject);
  begin
  // outputType must be set before this is called
  transferDirection := kTransferLoad;
  if outputType = kDXF then self.fillPlantPartColors;
	self.transferFields;
  self.updatePredictedSizeDisplay;
  end;

procedure TGeneric3DOptionsForm.CloseClick(Sender: TObject);
  begin
  // do not let them complete action if no plants are selected
  if (useSelectedPlants.checked) and (MainForm.selectedPlants.count <= 0) then
    begin
    MessageDlg('You chose "selected" for "Draw which plants", but no plants are selected.' + chr(13)
      + 'You should make another choice, or click Cancel and select some plants.', mtError, [mbOK], 0);
    exit;
    end;
  // do not let them complete action if too many points are selected - only for LWO which holds ALL
  // points and faces until the end of the file
  if outputType = kLWO then
    if (totalPoints > kMax3DPoints) or (totalTriangles > kMax3DFaces) then
    begin
    MessageDlg('You have selected too many points or triangles for this file format.' + chr(13)
        + 'A maximum of 65,536 points or triangles can be exported to one LWO file.' + chr(13) + chr(13)
        + 'You should make another choice of plants, or click Cancel and select fewer plants,' + chr(13)
        + 'or export to another format.', mtWarning, [mbOK], 0);
    exit;
    end;
  // warn them if the colors list will be truncated
  case outputType of
    kOBJ, kLWO: // limit of 1000 materials
      if (totalPlants * (kExportPartLast + 1) > kMaxStoredMaterials) then
        begin
        if MessageDlg('You have selected too many materials for this file format.' + chr(13)
          + 'The number of distinct colors will be bounded at ' + intToStr(kMaxStoredMaterials) + '.' + chr(13)
          + 'Some plants may refer to non-existent colors.' + chr(13) + chr(13)
          + 'To proceed anyway, click OK.', mtWarning, [mbOK, mbCancel], 0) = IDCANCEL then
          exit;
        end;
    end;
  transferDirection := kTransferSave;
	self.transferFields;
  modalResult := mrOK;
  end;

procedure TGeneric3DOptionsForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TGeneric3DOptionsForm.rearrangeItemsForOutputType;
  begin
  self.clientHeight := otherGroupBox.top + otherGroupBox.height + 4;
  self.clientWidth := close.left + close.width + 4;
  case outputType of
    kDXF:
      begin
      self.caption := 'Save DXF File';
      writeColors.visible := false;
      makeTrianglesDoubleSided.top := writeColors.top;
      translatePlantsToWindowPositions.top := makeTrianglesDoubleSided.top + makeTrianglesDoubleSided.height + 4;
      otherGroupBox.height := translatePlantsToWindowPositions.top + translatePlantsToWindowPositions.height + 6;
      with dxfColorsGroupBox do setBounds(4, otherGroupBox.top + otherGroupBox.height + 4, width, height);
      dxfColorsGroupBox.visible := true;
      self.clientHeight := dxfColorsGroupBox.top + dxfColorsGroupBox.height + 4;
      end;
    kPOV:
      begin                                                   
      self.caption := 'Save POV Include (INC) File';
      plantNameAndCylinderSidesPanel.visible := false;
      writePlantNumberInFrontOfName.visible := false;
      pressPlantsPanel.top := 16;
      writeColors.top := pressPlantsPanel.top + pressPlantsPanel.height;
      makeTrianglesDoubleSided.top := writeColors.top + writeColors.height + 4;
      translatePlantsToWindowPositions.top := makeTrianglesDoubleSided.top + makeTrianglesDoubleSided.height + 4;
      otherGroupBox.height := translatePlantsToWindowPositions.top + translatePlantsToWindowPositions.height + 6;
      with reorientGroupBox do setBounds(4, drawWhichPlantsGroupBox.top + drawWhichPlantsGroupBox.height + 4, width, height);
      with otherGroupBox do setBounds(4, reorientGroupBox.top + reorientGroupBox.height + 4, width, height);
      with povLimitsGroupBox do setBounds(4, otherGroupBox.top + otherGroupBox.height + 4, width, height);
      povLimitsGroupBox.visible := true;
      with nestingGroupBox do setBounds(4, povLimitsGroupBox.top + povLimitsGroupBox.height + 4, width, height);
      nestingGroupBox.visible := true;
      self.clientHeight := nestingGroupBox.top + nestingGroupBox.height + 4;
      layeringOption.visible := false;
      end;
    k3DS:
      begin
      self.caption := 'Save 3DS File';
      with threeDSWarningPanel do setBounds(4, otherGroupBox.top + otherGroupBox.height + 4, width, height);
      threeDSWarningPanel.visible := true;
      self.clientHeight := threeDSWarningPanel.top + threeDSWarningPanel.height + 4;
      end;
    kOBJ:
      begin
      self.caption := 'Save WaveFront OBJ File (ASCII)';
      end;
    kVRML:
      begin
      self.caption := 'Save VRML File';
      layeringOption.visible := false;
      with reorientGroupBox do setBounds(4, drawWhichPlantsGroupBox.top + drawWhichPlantsGroupBox.height + 4, width, height);
      with otherGroupBox do setBounds(4, reorientGroupBox.top + reorientGroupBox.height + 4, width, height);
      with vrmlVersionRadioGroup do setBounds(4, otherGroupBox.top + otherGroupBox.height + 4, width, height);
      vrmlVersionRadioGroup.visible := true;
      with nestingGroupBox do setBounds(4, vrmlVersionRadioGroup.top + vrmlVersionRadioGroup.height + 4, width, height);
      commentOutUnionAtEnd.visible := false;
      nestingGroupBox.height := nestInflorescence.top + nestInflorescence.height + 6;
      nestingGroupBox.visible := true;
      self.clientHeight := nestingGroupBox.top + nestingGroupBox.height + 4;
      end;
    kLWO:
      self.caption := 'Save Lightwave LWO File';
    end;
  end;

procedure TGeneric3DOptionsForm.transferFields;
  var oldExportType: smallint;
  begin
  // options that work for all types
  if transferDirection = kTransferLoad then
    begin
    case options.exportType of
      kIncludeSelectedPlants: useSelectedPlants.checked := true;
      kIncludeVisiblePlants: useVisiblePlants.checked := true;
      kIncludeAllPlants: useAllPlants.checked := true;
      end;
    end
  else
    begin
    oldExportType := options.exportType;
    if useSelectedPlants.checked then
      options.exportType := kIncludeSelectedPlants
    else if useVisiblePlants.checked then
      options.exportType := kIncludeVisiblePlants
    else if useAllPlants.checked then
      options.exportType := kIncludeAllPlants;
    if (oldExportType <> options.exportType) then
      optionsChanged := true;
    end;
  self.transferRadioGroup(layeringOption, options.layeringOption);
  self.transferSmallintSpinEditBox(stemCylinderFaces, options.stemCylinderFaces);
  self.transferSmallintSpinEditBox(lengthOfShortName, options.lengthOfShortName);
  self.transferSmallintSpinEditBox(xRotationBeforeDraw, options.xRotationBeforeDraw);
  self.transferCheckBox(translatePlantsToWindowPositions, options.translatePlantsToWindowPositions);
  self.transferCheckBox(writePlantNumberInFrontOfName, options.writePlantNumberInFrontOfName);
  self.transferCheckBox(writeColors, options.writeColors);
  self.transferSmallintSpinEditBox(overallScalingFactor_pct, options.overallScalingFactor_pct);
  self.transferCheckBox(pressPlants, options.pressPlants);
  self.transferComboBox(directionToPressPlants, options.directionToPressPlants);
  self.transferCheckBox(makeTrianglesDoubleSided, options.makeTrianglesDoubleSided);
  // options for specific types
  case outputType of
    kDXF:
      begin
      self.transferCheckBox(dxfWriteColors, options.writeColors); // do after general one to override
      if transferDirection = kTransferLoad then
        dxfWriteColorsClick(self);
      self.transferRadioButton(colorDXFFromRGB, options.dxf_whereToGetColors, kColorDXFFromRGB);
      self.transferRadioButton(colorDXFFromOneColor, options.dxf_whereToGetColors, kColorDXFFromOneColor);
      self.transferRadioButton(colorDXFFromPlantPartType, options.dxf_whereToGetColors, kColorDXFFromPlantPartType);
      wholePlantColor.color := dxfColors[options.dxf_wholePlantColorIndex];
      if transferDirection = kTransferLoad then
        colorsByPlantPart.invalidate;
      end;
    kPOV:
      begin
      self.transferSingleEditBox(minLineLengthToWrite, options.pov_minLineLengthToWrite);
      self.transferSingleEditBox(minTdoScaleToWrite, options.pov_minTdoScaleToWrite);
      self.transferCheckbox(commentOutUnionAtEnd, options.pov_commentOutUnionAtEnd);
      self.transferCheckbox(nestInflorescence, options.nest_Inflorescence);
      self.transferCheckbox(nestLeafAndPetiole, options.nest_LeafAndPetiole);
      self.transferCheckbox(nestCompoundLeaf, options.nest_CompoundLeaf);
      self.transferCheckbox(nestPedicelAndFlowerFruit, options.nest_PedicelAndFlowerFruit);
      self.transferCheckbox(nestFloralLayers, options.nest_FloralLayers);
      end;
    k3DS:
      begin
      // nothing special
      end;
    kOBJ:
      begin
      // nothing special
      end;
    kVRML:
      begin
      self.transferCheckbox(nestInflorescence, options.nest_Inflorescence);
      self.transferCheckbox(nestLeafAndPetiole, options.nest_LeafAndPetiole);
      self.transferCheckbox(nestCompoundLeaf, options.nest_CompoundLeaf);
      self.transferCheckbox(nestPedicelAndFlowerFruit, options.nest_PedicelAndFlowerFruit);
      self.transferCheckbox(nestFloralLayers, options.nest_FloralLayers);
      self.transferRadioGroup(vrmlVersionRadioGroup, options.vrml_version);
      end;
    kLWO:
      // nothing yet
      ;
    end;
  end;

procedure TGeneric3DOptionsForm.updatePredictedSizeDisplay;
  var
    i: longint;
    plant: PdPlant;
    plantsString: string;
    estimatedBytes: longint;
  begin
  totalPlants := 0;
  totalPoints := 0;
  totalTriangles := 0;
  totalParts := 0;
  totalMaterials := 0;
  if domain.plantManager.plants.count > 0 then
    for i := 0 to domain.plantManager.plants.count - 1 do
      begin
      plant := PdPlant(domain.plantManager.plants.items[i]);
      if plant = nil then continue;
      if (useSelectedPlants.checked) and (not MainForm.isSelected(plant)) then continue;
      if (useVisiblePlants.checked) and (plant.hidden) then continue;
      plant.countPlantPartsFor3DOutput(outputType, strToIntDef(stemCylinderFaces.text, 20));
      totalPoints := totalPoints + plant.total3DExportPoints;
      totalTriangles := totalTriangles + plant.total3DExportTriangles;
      totalParts := totalParts + plant.totalPlantParts;
      totalMaterials := totalMaterials + plant.total3DExportMaterials;
      inc(totalPlants);
      end;
  estimatedBytes := self.estimateBytes(domain.plantManager.plants.count, totalParts, totalPoints, totalTriangles);
  options.fileSize := 1.0 * estimatedBytes / (1024 * 1024); // in MB
  with estimationStringGrid do
    begin
    cells[0, 0] := ' plants';    cells[0, 1] := ' ' + intToStr(totalPlants);
    colWidths[0] := 36;
    cells[1, 0] := ' parts';     cells[1, 1] := ' ' + intToStr(totalParts);
    colWidths[1] := 36;
    cells[2, 0] := ' points';    cells[2, 1] := ' ' + intToStr(totalPoints);
    colWidths[2] := 44;
    cells[3, 0] := ' polygons';  cells[3, 1] := ' ' + intToStr(totalTriangles);
    colWidths[3] := 50; // polygons is the longest word
    cells[4, 0] := ' colors';    cells[4, 1] := ' ' + intToStr(totalMaterials);
    cells[5, 0] := ' size';
    colWidths[5] := 64;
    if self.options.fileSize > 1.0 then
      cells[5, 1] := ' ' + floatToStrF(self.options.fileSize, ffFixed, 7, 2) + ' MB'
    else
      cells[5, 1] := ' ' + intToStr(round(self.options.fileSize * 1024)) + ' K';
    end;
  translatePlantsToWindowPositions.visible := (totalPlants > 1);
  end;

function TGeneric3DOptionsForm.estimateBytes(numPlants, numParts, numPoints, numTriangles: longint): longint;
  begin
  case outputType of
    kDXF: result := numPoints * 250;
    kPOV: result := numPlants * 25 + numParts * 25 + numTriangles * 150;
    k3DS: result := numPlants * 48 + numParts * 48 + numPoints * 24 + numTriangles * 24;
    kOBJ: result := numPlants * 100 + numParts * 100 + numPoints * 50 + numTriangles * 50;
    kVRML: result := numPlants * 100 + numParts * 100 + numPoints * 80 + numTriangles * 80;
    kLWO: result := numPlants * 600 + numParts * 100 + numPoints * 20 + numTriangles * 20;
    else raise Exception.create('Problem: Invalid 3d export type for size estimation.');
    end;
  end;

procedure TGeneric3DOptionsForm.fillPlantPartColors;
  var
    i: smallint;
    firstPlant: PdPlant;
  begin
  colorsByPlantPart.clear;
  // use first plant to get DXF part type names - there must be at least one plant to bring up this form
  if (domain = nil) or (domain.plantManager = nil) or (domain.plantManager.plants.count < 0) then exit;
  firstPlant := PdPlant(domain.plantManager.plants[0]);
  if firstPlant = nil then exit;
  for i := 0 to kExportPartLast do
    colorsByPlantPart.items.add(longNameForDXFPartType(i));
  end;

procedure TGeneric3DOptionsForm.colorsByPlantPartDrawItem(Control: TWinControl; Index: Integer; Rect: TRect;
  State: TOwnerDrawState);
  var
    selected: boolean;
    colorRect, remainderRect: TRect;
    cText: array[0..255] of Char;
  begin
  if Application.terminated then exit;
  if (colorsByPlantPart.items.count <= 0) or (index < 0) or (index > colorsByPlantPart.items.count - 1) then exit;
  selected := (odSelected in state);
  { set up rectangles }
  colorRect := rect;
  colorRect.right := colorRect.left + colorsByPlantPart.itemHeight;
  remainderRect := rect;
  remainderRect.left := remainderRect.left + colorsByPlantPart.itemHeight;
  { fill first box with white, rest with clHighlight if selected }
  with colorsByPlantPart.canvas do
    begin
    brush.style := bsSolid;
    brush.color := dxfColors[options.dxf_plantPartColorIndexes[index]];
    fillRect(colorRect);
    font := colorsByPlantPart.font;
    if selected then
      begin
      brush.color := clHighlight;
      font.color := clHighlightText;
      end
    else
      begin
      brush.color := clWindow;
      font.color := clBtnText;
      end;
    fillRect(remainderRect);
    strPCopy(cText, colorsByPlantPart.items[index]);
    remainderRect.left := remainderRect.left + 5; { margin for text }
    winprocs.drawText(handle, cText, strLen(cText), remainderRect, DT_LEFT);
    end;
  end;

procedure TGeneric3DOptionsForm.wholePlantColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
  	colorForm: TChooseDXFColorForm;
    response: integer;
  begin
  colorForm := TChooseDXFColorForm.create(self);
  if colorForm = nil then
    raise Exception.create('Problem: Could not create color window.');
  try
    colorForm.colorIndex := options.dxf_wholePlantColorIndex;
    response := colorForm.showModal;
  if response = mrOK then
    begin
    options.dxf_wholePlantColorIndex := colorForm.colorIndex;
    wholePlantColor.color := dxfColors[options.dxf_wholePlantColorIndex];
    wholePlantColor.invalidate;
    optionsChanged := true;
    end;
  finally
    colorForm.free;
    colorForm := nil;
  end;
  end;

procedure TGeneric3DOptionsForm.setPlantPartColorClick(Sender: TObject);
  var
  	colorForm: TChooseDXFColorForm;
    response: integer;
    firstColorIndex: TColorRef;
    i: smallint;
  begin
  firstColorIndex := -1;
  if colorsByPlantPart.items.count > 0 then for i := 0 to colorsByPlantPart.items.count - 1 do
    if colorsByPlantPart.selected[i] then
      if firstColorIndex = -1 then firstColorIndex := options.dxf_plantPartColorIndexes[i];
  if firstColorIndex < 0 then exit;
  colorForm := TChooseDXFColorForm.create(self);
  if colorForm = nil then
    raise Exception.create('Problem: Could not create color window.');
  try
    colorForm.colorIndex := firstColorIndex;
    response := colorForm.showModal;
  if response = mrOK then
    begin
    if colorsByPlantPart.items.count > 0 then for i := 0 to colorsByPlantPart.items.count - 1 do
      if colorsByPlantPart.selected[i] then
        options.dxf_plantPartColorIndexes[i] := colorForm.colorIndex;
    colorsByPlantPart.invalidate;
    optionsChanged := true;
    end;
  finally
    colorForm.free;
    colorForm := nil;
  end;
  end;

procedure TGeneric3DOptionsForm.colorsByPlantPartDblClick(Sender: TObject);
  begin
  self.setPlantPartColorClick(self);
  end;

procedure TGeneric3DOptionsForm.transferRadioButton(radioButton: TRadioButton; var value: smallint; radioIndex: smallint);
  begin
  if transferDirection = kTransferLoad then
    begin
    if value = radioIndex then radioButton.checked := true;
    end
  else if transferDirection = kTransferSave then
    begin
    if (radioButton.checked) and (value <> radioIndex) then
      optionsChanged := true;
    if radioButton.checked then value := radioIndex;
    end;
  end;

procedure TGeneric3DOptionsForm.transferCheckBox(checkBox: TCheckBox; var value: boolean);
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

procedure TGeneric3DOptionsForm.transferColor(colorPanel: TPanel; var value: TColorRef);
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

procedure TGeneric3DOptionsForm.transferSmallintSpinEditBox(editBox: TSpinEdit; var value: smallint);
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

procedure TGeneric3DOptionsForm.transferRadioGroup(radioGroup: TRadioGroup; var value: smallint);
  begin
  if transferDirection = kTransferLoad then
    radioGroup.itemIndex := value
  else if transferDirection = kTransferSave then
    begin
    if value <> radioGroup.itemIndex then
      optionsChanged := true;
    value := radioGroup.itemIndex;
    end;
  end;

procedure TGeneric3DOptionsForm.transferComboBox(comboBox: TComboBox; var value: smallint);
  begin
  if transferDirection = kTransferLoad then
    comboBox.itemIndex := value
  else if transferDirection = kTransferSave then
    begin
    if value <> comboBox.itemIndex then
      optionsChanged := true;
    value := comboBox.itemIndex;
    end;
  end;

procedure TGeneric3DOptionsForm.transferSingleEditBox(editBox: TEdit; var value: single);
  var
    newValue: single;
  begin
  if transferDirection = kTransferLoad then
    editBox.text := valueString(value)
  else if transferDirection = kTransferSave then
    begin
    try
      newValue := strToFloat(editBox.text);
    except
      newValue := value;
    end;
    if newValue <> value then
      optionsChanged := true;
    value := newValue;
    end;
  end;

procedure TGeneric3DOptionsForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Exporting_3D_models_in_general');
  end;

procedure TGeneric3DOptionsForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

procedure TGeneric3DOptionsForm.useSelectedPlantsClick(Sender: TObject);
  begin
  self.updatePredictedSizeDisplay;
  end;

procedure TGeneric3DOptionsForm.useVisiblePlantsClick(Sender: TObject);
  begin
  self.updatePredictedSizeDisplay;
  end;

procedure TGeneric3DOptionsForm.useAllPlantsClick(Sender: TObject);
  begin
  self.updatePredictedSizeDisplay;
  end;

procedure TGeneric3DOptionsForm.stemCylinderFacesChange(Sender: TObject);
  var value: integer;
  begin
  value := strToIntDef(stemCylinderFaces.text, 5);
  if value < kMinOutputCylinderFaces then value := kMinOutputCylinderFaces;
  if value > kMaxOutputCylinderFaces then value := kMaxOutputCylinderFaces;
  stemCylinderFaces.text := intToStr(value);
  self.updatePredictedSizeDisplay;
  end;

procedure TGeneric3DOptionsForm.dxfWriteColorsClick(Sender: TObject);
  begin
  colorDXFFromRGB.visible := dxfWriteColors.checked;
  colorDXFFromOneColor.visible := dxfWriteColors.checked;
  wholePlantColor.visible := dxfWriteColors.checked;
  colorDXFFromPlantPartType.visible := dxfWriteColors.checked;
  colorsByPlantPart.visible := dxfWriteColors.checked;
  setPlantPartColor.visible := dxfWriteColors.checked;
  end;

end.
