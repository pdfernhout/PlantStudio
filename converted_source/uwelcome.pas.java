// unit uwelcome

from conversion_common import *;
import updform;
import delphi_compatability;

// const
kReadSuperSpeedTour = 0;
kReadTutorial = 1;
kMakeNewPlant = 2;
kOpenPlantLibrary = 3;
kStartUsingProgram = 4;



class TWelcomeForm extends PdForm {
    public TCheckBox hideWelcomeForm;
    public TLabel Label3;
    public TLabel Label1;
    public TImage Image1;
    public TButton readQuickStartTipList;
    public TButton readTutorial;
    public TButton makeNewPlant;
    public TButton openPlantLibrary;
    public TButton startUsingProgram;
    public short whatToDo;
    
    //$R *.DFM
    public void CreateParams(TCreateParams Params) {
        super.CreateParams(Params);
        Params.Style = Params.Style || delphi_compatability.WS_BORDER || delphi_compatability.WS_EX_DLGMODALFRAME;
    }
    
    public void readQuickStartTipListClick(TObject Sender) {
        this.whatToDo = kReadSuperSpeedTour;
        this.ModalResult = mrOK;
    }
    
    public void readTutorialClick(TObject Sender) {
        this.whatToDo = kReadTutorial;
        this.ModalResult = mrOK;
    }
    
    public void makeNewPlantClick(TObject Sender) {
        this.whatToDo = kMakeNewPlant;
        this.ModalResult = mrOK;
    }
    
    public void openPlantLibraryClick(TObject Sender) {
        this.whatToDo = kOpenPlantLibrary;
        this.ModalResult = mrOK;
    }
    
    public void startUsingProgramClick(TObject Sender) {
        this.whatToDo = kStartUsingProgram;
        this.ModalResult = mrOK;
    }
    
}
