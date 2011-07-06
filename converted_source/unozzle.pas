unit unozzle;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  ExtCtrls, StdCtrls, Buttons, Spin,
  udomain, updform;

type
  TNozzleOptionsForm = class(PdForm) 
    GroupBox1: TGroupBox;
    cellCountLabel: TLabel;
    cellSizeLabel: TLabel;
    helpButton: TSpeedButton;
    Close: TButton;
    cancel: TButton;
    ColorDialog: TColorDialog;
    fileSizeLabel: TLabel;
    Panel1: TPanel;
    Label4: TLabel;
    GroupBox2: TGroupBox;
    resolutionLabel: TLabel;
    Label3: TLabel;
    colorsLabel: TLabel;
    Label1: TLabel;
    backgroundColorPanel: TPanel;
    resolutionEdit: TSpinEdit;
    colorType: TComboBox;
    GroupBox3: TGroupBox;
    useSelectedPlants: TRadioButton;
    useVisiblePlants: TRadioButton;
    useAllPlants: TRadioButton;
    procedure changeSelection(Sender: TObject);
    procedure backgroundColorPanelClick(Sender: TObject);
    procedure resolutionEditChange(Sender: TObject);
    procedure colorTypeChange(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure CloseClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    options: NozzleOptionsStructure;
    procedure initializeWithOptions(anOptions: NozzleOptionsStructure);
    procedure updateCellSizeAndCountForSelection;
  end;

implementation

{$R *.DFM}

uses umain, usupport, umath;

procedure TNozzleOptionsForm.initializeWithOptions(anOptions: NozzleOptionsStructure);
  begin
  self.options := anOptions;
  case options.exportType of
    kIncludeSelectedPlants: useSelectedPlants.checked := true;
    kIncludeVisiblePlants: useVisiblePlants.checked := true;
    kIncludeAllPlants: useAllPlants.checked := true;
    end;
  resolutionEdit.text := intToStr(round(options.resolution_pixelsPerInch));
  backgroundColorPanel.color := options.backgroundColor;
  colorType.itemIndex := ord(options.colorType);
  self.updateCellSizeAndCountForSelection;
  end;

procedure TNozzleOptionsForm.updateCellSizeAndCountForSelection;
  var
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean;
    cellRect: TRect;
    scaleMultiplier: single;
    fileSize: longint;
  begin
  excludeInvisiblePlants := not useAllPlants.checked;
  excludeNonSelectedPlants := useSelectedPlants.checked;
  cellRect := domain.plantManager.largestPlantBoundsRect(MainForm.selectedPlants,
    excludeInvisiblePlants, excludeNonSelectedPlants);
  scaleMultiplier := safedivExcept(1.0 * options.resolution_pixelsPerInch, 1.0 * Screen.pixelsPerInch, 1.0);
  options.cellSize := Point(round(rWidth(cellRect) * scaleMultiplier),
      round(rHeight(cellRect) * scaleMultiplier));
  if useAllPlants.checked then
    options.cellCount := domain.plantManager.plants.count
  else if useVisiblePlants.checked then
    options.cellCount := domain.plantManager.visiblePlantCount
  else if useSelectedPlants.checked then
    options.cellCount := MainForm.selectedPlants.count;
  cellSizeLabel.caption := 'Nozzle/tube cell width:  ' + intToStr(options.cellSize.x)
      + ' height:  ' + intToStr(options.cellSize.y);
  cellCountLabel.caption := 'Number of items:  ' + intToStr(options.cellCount);
  fileSize := round(options.cellCount * options.cellSize.x * options.cellSize.y
    * bitsPerPixelForColorType(options.colorType) / 8.0) + sizeOf(TBitmapInfo);
  if fileSize < 1024 then
    fileSizeLabel.caption := 'Estimated file size:  ' + intToStr(fileSize) + ' bytes'
  else if fileSize < 1024 * 1024 then
    fileSizeLabel.caption := 'Estimated file size:  ' + intToStr(fileSize div 1024) + ' KB'
  else
    fileSizeLabel.caption := 'Estimated file size:  ' + floatToStrF(fileSize / (1024 * 1024), ffFixed, 7, 1) + ' MB';
  if fileSize >= 10.0 * 1024 * 1024 then
    fileSizeLabel.font.style := [fsBold]
  else
    fileSizeLabel.font.style := [];
  end;                                                     

procedure TNozzleOptionsForm.changeSelection(Sender: TObject);
  begin
  if sender = useSelectedPlants then
    options.exportType := kIncludeSelectedPlants
  else if sender = useVisiblePlants then
    options.exportType := kIncludeVisiblePlants
  else if sender = useAllPlants then
    options.exportType := kIncludeAllPlants;
  self.updateCellSizeAndCountForSelection;
  end;

procedure TNozzleOptionsForm.backgroundColorPanelClick(Sender: TObject);
  begin
  backgroundColorPanel.color := domain.getColorUsingCustomColors(backgroundColorPanel.color);
  options.backgroundColor := backgroundColorPanel.color;
  end;

procedure TNozzleOptionsForm.resolutionEditChange(Sender: TObject);
  begin
  options.resolution_pixelsPerInch := strToIntDef(resolutionEdit.text, round(options.resolution_pixelsPerInch));
  self.updateCellSizeAndCountForSelection;
  end;

procedure TNozzleOptionsForm.colorTypeChange(Sender: TObject);
  begin
  options.colorType := TPixelFormat(colorType.itemIndex);
  self.updateCellSizeAndCountForSelection;
  end;

procedure TNozzleOptionsForm.helpButtonClick(Sender: TObject);
  begin
  Application.helpJump('Making_a_nozzle_or_tube');
  end;

procedure TNozzleOptionsForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

procedure TNozzleOptionsForm.CloseClick(Sender: TObject);
  begin
  if (options.exportType = kIncludeSelectedPlants) and (MainForm.selectedPlants.count <= 0) then
    MessageDlg('You chose "selected" for "Draw which plants", but no plants are selected.' + chr(13)
      + 'You should make another choice, or click Cancel and select some plants.', mtError, [mbOK], 0)
  else
    modalResult := mrOK;
  end;

end.
