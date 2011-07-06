unit Usplash;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, StdCtrls, ExtCtrls, Buttons;

type
  TSplashForm = class(TForm)
    versionLabel: TLabel;
    loadingLabel: TLabel;
    codeLabel: TLabel;
    splashImage256Colors: TImage;
    splashImageTrueColor: TImage;
    close: TSpeedButton;
    supportButton: TSpeedButton;
    procedure FormCreate(Sender: TObject);
    procedure FormClick(Sender: TObject);
    procedure programNameLabelClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure FormKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure FormMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure controlClick(Sender: TObject);
    procedure splashImage256ColorsClick(Sender: TObject);
    procedure OKClick(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure closeClick(Sender: TObject);
    procedure supportButtonClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    procedure CreateParams(var Params: TCreateParams); override;
    procedure goAway;
    procedure showLoadingString(aString: string);
    procedure showCodeString(aString: string);
  end;

var
  splashForm: TSplashForm;

implementation

{$R *.DFM}

uses usupport, uprginfo;

procedure TSplashForm.CreateParams(var Params: TCreateParams);
  begin
  inherited CreateParams(Params);
  with Params do
    Style :=  Style or WS_BORDER or WS_EX_DLGMODALFRAME;
  end;

procedure TSplashForm.FormCreate(Sender: TObject);
  begin
  versionLabel.caption := gVersionName;
  end;

procedure TSplashForm.showLoadingString(aString: string);
  begin
  // remove possible comma at end from registration program
  if (length(aString) > 1) and (aString[length(aString)] = ',')  then
    aString := copy(aString, 1, length(aString) - 1);
  loadingLabel.caption := aString;
  self.update;
  end;

procedure TSplashForm.showCodeString(aString: string);
  begin
  codeLabel.caption := aString;
  codeLabel.show;
  self.update;
  end;

procedure TSplashForm.goAway;
  begin
  modalResult := mrOk;
  end;

procedure TSplashForm.FormClick(Sender: TObject);
  begin
  self.goAway;
  end;

procedure TSplashForm.programNameLabelClick(Sender: TObject);
  begin
  self.goAway;
  end;

procedure TSplashForm.controlClick(Sender: TObject);
  begin
  self.goAway;
  end;

procedure TSplashForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  self.goAway;
  end;

procedure TSplashForm.FormKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  self.goAway;
  end;

procedure TSplashForm.FormMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  self.goAway;
  end;

procedure TSplashForm.splashImage256ColorsClick(Sender: TObject);
  begin
  self.goAway;
  end;

procedure TSplashForm.OKClick(Sender: TObject);
  begin
  self.goAway;
  end;

procedure TSplashForm.FormActivate(Sender: TObject);
  var
    screenColorBits: integer;
    screenDC: HDC;
  begin
  screenDC := GetDC(0);
  try
    screenColorBits := (GetDeviceCaps(screenDC, BITSPIXEL) * GetDeviceCaps(screenDC, PLANES));
  finally
    ReleaseDC(0, screenDC);
  end;
  if screenColorBits > 8 then
    begin
    splashImageTrueColor.visible := true;
    splashImage256Colors.visible := false;
    splashImageTrueColor.left := 0;
    splashImageTrueColor.top := 0;
    splashImageTrueColor.sendToBack;
    end
  else
    begin
    splashImage256Colors.visible := true;
    splashImageTrueColor.visible := false;
    splashImage256Colors.left := 0;
    splashImage256Colors.top := 0;
    splashImage256Colors.sendToBack;
    end;
  end;

procedure TSplashForm.closeClick(Sender: TObject);
  begin
  modalResult := mrOK;
  end;

procedure TSplashForm.supportButtonClick(Sender: TObject);
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
