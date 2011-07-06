unit uabout;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  ExtCtrls, StdCtrls;

type
  TAboutForm = class(TForm)
    close: TButton;
    registerIt: TButton;
    readLicense: TButton;
    cancel: TButton;
    whyRegister: TButton;
    versionLabel: TLabel;
    registrationInfoPanel: TPanel;
    noDistributeLabel: TLabel;
    timeWarningLabel: TLabel;
    hoursLabel: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Label6: TLabel;
    unregistered2DExportReminder: TImage;
    Label7: TLabel;
    Label1: TLabel;
    splashScreenPicture: TImage;
    Label2: TLabel;
    unregistered3DExportReminder: TImage;
    supportButton: TButton;
    exportRestrictionLabel: TLabel;
    procedure FormActivate(Sender: TObject);
    procedure closeClick(Sender: TObject);
    procedure readLicenseClick(Sender: TObject);
    procedure registerItClick(Sender: TObject);
    procedure whyRegisterClick(Sender: TObject);
    procedure supportButtonClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    procedure initializeWithWhetherClosingProgram(closingProgram: boolean);
  end;

var
  AboutForm: TAboutForm;

implementation

{$R *.DFM}

uses udomain, uregister, usupport, umath, uprginfo;

procedure TAboutForm.initializeWithWhetherClosingProgram(closingProgram: boolean);
  begin
  if closingProgram then
    close.caption := 'Quit'
  else
    close.caption := 'Close';
  cancel.visible := closingProgram;
  end;

procedure TAboutForm.FormActivate(Sender: TObject);
  var
    timeBetween: TDateTime;
    hours, minutes, seconds, milliseconds, smallHours: word;
    randomNumber: integer;
    i: smallint;
  begin
  versionLabel.caption := gVersionName;
  exportRestrictionLabel.caption := '- restricting the number of exports to '
    + intToStr(kMaxUnregExportsAllowed) + ' at first, then ' + intToStr(kMaxUnregExportsPerSessionAfterMaxReached)
    + ' per session';
  activeControl := registerIt;
  randomize;
  for i := 0 to 100 do random;
  randomNumber := random(2);
  case randomNumber of
    0:
      begin
      close.top := 4;
      registerIt.top := close.top + close.height + 3;
      end;
    1:
      begin
      registerIt.top := 4;
      close.top := registerIt.top + registerIt.height + 3;
      end;
    end;
  hoursLabel.caption := 'You have been evaluating PlantStudio for ';
  timeBetween := max((Now - domain.startTimeThisSession), 0) + domain.accumulatedUnregisteredTime;
  DecodeTime(timeBetween, smallHours, minutes, seconds, milliseconds);
  hours := smallHours;
  if timeBetween >= 1.0 then
    hours := hours + trunc(timeBetween) * 24;
  if (minutes < 1) and (hours < 1) then
    hoursLabel.caption := hoursLabel.caption + 'less than one minute.'
  else if (minutes = 1) and (hours < 1) then
    hoursLabel.caption := hoursLabel.caption + 'one minute.'
  else if hours < 1 then
    hoursLabel.caption := hoursLabel.caption + intToStr(minutes) + ' minutes.'
  else if hours = 1 then
    hoursLabel.caption := hoursLabel.caption + intToStr(hours) + ' hour and ' + intToStr(minutes) + ' minutes.'
  else
    hoursLabel.caption := hoursLabel.caption + intToStr(hours) + ' hours and ' + intToStr(minutes) + ' minutes.';
  timeWarningLabel.caption := 'If you have been using PlantStudio for '
    + intToStr(kMaxEvaluationTime_hours)
    + ' hours or more (in total), you are legally required to register it.';
  if hours >= kMaxEvaluationTime_hours then
    begin
  	timeWarningLabel.font.color := clGreen;
  	timeWarningLabel.font.style := [fsBold];
    end;
  end;

procedure TAboutForm.closeClick(Sender: TObject);
  begin
  modalResult := mrOK;
  end;

procedure TAboutForm.registerItClick(Sender: TObject);
  begin
  if RegistrationForm.showModal = mrOK then
    modalResult := mrCancel;
  end;

procedure TAboutForm.readLicenseClick(Sender: TObject);
  begin
  application.helpJump('License');
  end;

procedure TAboutForm.whyRegisterClick(Sender: TObject);
  begin
  application.helpJump('Why_register?'); 
  end;

procedure TAboutForm.supportButtonClick(Sender: TObject);
  var infoForm: TProgramInfoForm;
  begin
  infoForm := TProgramInfoForm.create(Application);
  try
    infoForm.showModal;
  finally
    infoForm.free;
    infoForm := nil;
  end;
  end;

end.
