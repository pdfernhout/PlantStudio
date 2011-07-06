unit uwelcome;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, updform;

type
  TWelcomeForm = class(PdForm)
    hideWelcomeForm: TCheckBox;
    Label3: TLabel;
    Label1: TLabel;
    Image1: TImage;
    readQuickStartTipList: TButton;
    readTutorial: TButton;
    makeNewPlant: TButton;
    openPlantLibrary: TButton;
    startUsingProgram: TButton;
    procedure readQuickStartTipListClick(Sender: TObject);
    procedure readTutorialClick(Sender: TObject);
    procedure makeNewPlantClick(Sender: TObject);
    procedure openPlantLibraryClick(Sender: TObject);
    procedure startUsingProgramClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    whatToDo: smallint;
    procedure CreateParams(var Params: TCreateParams); override;
  end;

const
  kReadSuperSpeedTour = 0;
  kReadTutorial = 1;
  kMakeNewPlant = 2;
  kOpenPlantLibrary = 3;
  kStartUsingProgram = 4;

implementation

{$R *.DFM}

procedure TWelcomeForm.CreateParams(var Params: TCreateParams);
  begin
  inherited CreateParams(Params);
  with Params do
    Style :=  Style or WS_BORDER or WS_EX_DLGMODALFRAME;
  end;

procedure TWelcomeForm.readQuickStartTipListClick(Sender: TObject);
  begin
  whatToDo := kReadSuperSpeedTour;
  modalResult := mrOk;
  end;

procedure TWelcomeForm.readTutorialClick(Sender: TObject);
  begin
  whatToDo := kReadTutorial;
  modalResult := mrOk;
  end;

procedure TWelcomeForm.makeNewPlantClick(Sender: TObject);
  begin
  whatToDo := kMakeNewPlant;
  modalResult := mrOk;
  end;

procedure TWelcomeForm.openPlantLibraryClick(Sender: TObject);
  begin
  whatToDo := kOpenPlantLibrary;
  modalResult := mrOk;
  end;

procedure TWelcomeForm.startUsingProgramClick(Sender: TObject);
  begin
  whatToDo := kStartUsingProgram;
  modalResult := mrOk;
  end;

end.
