# unit uwelcome

from conversion_common import *
import updform
import delphi_compatability

# const
kReadSuperSpeedTour = 0
kReadTutorial = 1
kMakeNewPlant = 2
kOpenPlantLibrary = 3
kStartUsingProgram = 4

class TWelcomeForm(PdForm):
    def __init__(self):
        self.hideWelcomeForm = TCheckBox()
        self.Label3 = TLabel()
        self.Label1 = TLabel()
        self.Image1 = TImage()
        self.readQuickStartTipList = TButton()
        self.readTutorial = TButton()
        self.makeNewPlant = TButton()
        self.openPlantLibrary = TButton()
        self.startUsingProgram = TButton()
        self.whatToDo = 0
    
    #$R *.DFM
    def CreateParams(self, Params):
        PdForm.CreateParams(self, Params)
        Params.Style = Params.Style or delphi_compatability.WS_BORDER or delphi_compatability.WS_EX_DLGMODALFRAME
    
    def readQuickStartTipListClick(self, Sender):
        self.whatToDo = kReadSuperSpeedTour
        self.ModalResult = mrOK
    
    def readTutorialClick(self, Sender):
        self.whatToDo = kReadTutorial
        self.ModalResult = mrOK
    
    def makeNewPlantClick(self, Sender):
        self.whatToDo = kMakeNewPlant
        self.ModalResult = mrOK
    
    def openPlantLibraryClick(self, Sender):
        self.whatToDo = kOpenPlantLibrary
        self.ModalResult = mrOK
    
    def startUsingProgramClick(self, Sender):
        self.whatToDo = kStartUsingProgram
        self.ModalResult = mrOK
    
