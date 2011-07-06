unit uanimate;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Spin, StdCtrls, ExtCtrls, Buttons, udomain, uplant, updform;

type
  TAnimationFilesOptionsForm = class(PdForm)
    helpButton: TSpeedButton;
    Close: TButton;
    cancel: TButton;
    Panel1: TPanel;
    fileNumberLabel: TLabel;
    animationSizeLabel: TLabel;
    fileSizeLabel: TLabel;
    Panel2: TPanel;
    Label4: TLabel;
    focusedPlantName: TLabel;
    Label5: TLabel;
    GroupBox1: TGroupBox;
    Label1: TLabel;
    resolutionLabel: TLabel;
    incrementLabel: TLabel;
    plantMaxAgeLabel: TLabel;
    colorsLabel: TLabel;
    animateByAge: TRadioButton;
    animateByXRotation: TRadioButton;
    incrementEdit: TSpinEdit;
    resolution: TSpinEdit;
    colorType: TComboBox;
    procedure animateByAgeClick(Sender: TObject);
    procedure animateByXRotationClick(Sender: TObject);
    procedure incrementEditChange(Sender: TObject);
    procedure resolutionChange(Sender: TObject);
    procedure colorTypeChange(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
  public
    { Public declarations }
    options: NumberedAnimationOptionsStructure;
    plant: PdPlant;
    internalChange: boolean;
    procedure initializeWithOptionsAndPlant(anOptions: NumberedAnimationOptionsStructure; aPlant: PdPlant);
    procedure changeQuestionsBasedOnAnimationType;
    procedure calculateNumberOfFrames;
  end;

implementation

{$R *.DFM}

uses umath, usupport;

procedure TAnimationFilesOptionsForm.initializeWithOptionsAndPlant(
    anOptions: NumberedAnimationOptionsStructure; aPlant: PdPlant);
  begin
  internalChange := true;
  if aPlant = nil then
    raise Exception.create('Problem: Nil plant in method TAnimationFilesOptionsForm.initializeWithOptionsAndPlant.');
  plant := aPlant;
  options := anOptions;
  focusedPlantName.caption := plant.getName;
  if options.animateBy = kAnimateByAge then
    animateByAge.checked := true
  else if options.animateBy = kAnimateByXRotation then
    animateByXRotation.checked := true;
  self.changeQuestionsBasedOnAnimationType;
  resolution.value := options.resolution_pixelsPerInch;
  colorType.itemIndex := ord(options.colorType);
  self.changeQuestionsBasedOnAnimationType;
  self.calculateNumberOfFrames;
  internalChange := false;
  end;

procedure TAnimationFilesOptionsForm.changeQuestionsBasedOnAnimationType;
  begin
  internalChange := true;
  if animateByAge.checked then
    begin
    incrementLabel.caption := 'Age increment between &frames (days)';
    incrementEdit.value := options.ageIncrement;
    end
  else
    begin
    incrementLabel.caption := 'Rotation increment between &frames (degrees)';
    incrementEdit.value := options.xRotationIncrement;
    end;
  internalChange := false;
  end;

procedure TAnimationFilesOptionsForm.animateByAgeClick(Sender: TObject);
  begin
  if internalChange then exit;
  if animateByAge.checked then
    options.animateBy := kAnimateByAge
  else
    options.animateBy := kAnimateByXRotation;
  self.changeQuestionsBasedOnAnimationType;
  self.calculateNumberOfFrames;
  end;

procedure TAnimationFilesOptionsForm.animateByXRotationClick(Sender: TObject);
  begin
  if internalChange then exit;
  if animateByAge.checked then
    options.animateBy := kAnimateByAge
  else
    options.animateBy := kAnimateByXRotation;
  self.changeQuestionsBasedOnAnimationType;
  self.calculateNumberOfFrames;
  end;

procedure TAnimationFilesOptionsForm.incrementEditChange(Sender: TObject);
  var oldValue: smallint;
  begin
  if internalChange then exit;
  if animateByAge.checked then
    oldValue := options.ageIncrement
  else
    oldValue := options.xRotationIncrement;
  try
    if animateByAge.checked then
      options.ageIncrement := incrementEdit.value
    else
      options.xRotationIncrement := incrementEdit.value;
  except
    if animateByAge.checked then
      options.ageIncrement := oldValue
    else
      options.xRotationIncrement := oldValue;
  end;
  self.calculateNumberOfFrames;
  end;

procedure TAnimationFilesOptionsForm.resolutionChange(Sender: TObject);
  var oldValue: smallint;
  begin
  if internalChange then exit;
  oldValue := options.resolution_pixelsPerInch;
  try
    options.resolution_pixelsPerInch := resolution.value;
  except
    options.resolution_pixelsPerInch := oldValue;
  end;
  self.calculateNumberOfFrames;
  end;

procedure TAnimationFilesOptionsForm.calculateNumberOfFrames;
  var
    scaleMultiplier: single;
  begin
  if options.animateBy = kAnimateByAge then
    begin
    plantMaxAgeLabel.caption := 'Maximum age = ' + intToStr(plant.pGeneral.ageAtMaturity);
    plantMaxAgeLabel.visible := true;
    options.frameCount := plant.pGeneral.ageAtMaturity div options.ageIncrement + 1;
    end
  else if options.animateBy = kAnimateByXRotation then
    begin
    plantMaxAgeLabel.visible := false;
    options.frameCount := 360 div abs(options.xRotationIncrement);
    end;
  fileNumberLabel.caption := 'Number of files:  ' + intToStr(options.frameCount);
  scaleMultiplier := safedivExcept(1.0 * options.resolution_pixelsPerInch,
    1.0 * Screen.pixelsPerInch, 1.0);
  options.scaledSize := Point(round(rWidth(plant.boundsRect_pixels) * scaleMultiplier),
    round(rHeight(plant.boundsRect_pixels) * scaleMultiplier));
  animationSizeLabel.caption := 'Animation size:  ' + intToStr(options.scaledSize.x) + ' x '
    + intToStr(options.scaledSize.y);
  options.fileSize := round(options.frameCount * options.scaledSize.x * options.scaledSize.y
    * bitsPerPixelForColorType(options.colorType) / 8.0)
    + sizeOf(TBitmapInfo);
  if options.fileSize < 1024 then
    fileSizeLabel.caption := 'Estimated total size:  ' + intToStr(options.fileSize) + ' bytes'
  else if options.fileSize < 1024 * 1024 then
    fileSizeLabel.caption := 'Estimated total size:  ' + intToStr(options.fileSize div 1024) + ' KB'
  else
    fileSizeLabel.caption := 'Estimated total size:  '
      + floatToStrF(options.fileSize / (1024 * 1024), ffFixed, 7, 1) + ' MB';
  if options.fileSize >= 10.0 * 1024 * 1024 then
    fileSizeLabel.font.style := [fsBold]
  else
    fileSizeLabel.font.style := [];
  end;

procedure TAnimationFilesOptionsForm.colorTypeChange(Sender: TObject);
  begin
  options.colorType := TPixelFormat(colorType.itemIndex);
  self.calculateNumberOfFrames;
  end;

procedure TAnimationFilesOptionsForm.helpButtonClick(Sender: TObject);
  begin
  Application.helpJump('Making_numbered_animation_files');
  end;

procedure TAnimationFilesOptionsForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

end.
