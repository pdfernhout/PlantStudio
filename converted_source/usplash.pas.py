# unit Usplash

from conversion_common import *
import uprginfo
import usupport
import delphi_compatability

# var
splashForm = TSplashForm()

class TSplashForm(TForm):
    def __init__(self):
        self.versionLabel = TLabel()
        self.loadingLabel = TLabel()
        self.codeLabel = TLabel()
        self.splashImage256Colors = TImage()
        self.splashImageTrueColor = TImage()
        self.close = TSpeedButton()
        self.supportButton = TSpeedButton()
    
    #$R *.DFM
    def CreateParams(self, Params):
        TForm.CreateParams(self, Params)
        Params.Style = Params.Style or delphi_compatability.WS_BORDER or delphi_compatability.WS_EX_DLGMODALFRAME
    
    def FormCreate(self, Sender):
        self.versionLabel.Caption = usupport.gVersionName
    
    def showLoadingString(self, aString):
        if (len(aString) > 1) and (aString[len(aString)] == ","):
            # remove possible comma at end from registration program
            aString = UNRESOLVED.copy(aString, 1, len(aString) - 1)
        self.loadingLabel.Caption = aString
        self.Update()
    
    def showCodeString(self, aString):
        self.codeLabel.Caption = aString
        self.codeLabel.Show()
        self.Update()
    
    def goAway(self):
        self.ModalResult = mrOK
    
    def FormClick(self, Sender):
        self.goAway()
    
    def programNameLabelClick(self, Sender):
        self.goAway()
    
    def controlClick(self, Sender):
        self.goAway()
    
    def FormKeyPress(self, Sender, Key):
        self.goAway()
        return Key
    
    def FormKeyDown(self, Sender, Key, Shift):
        self.goAway()
        return Key
    
    def FormMouseDown(self, Sender, Button, Shift, X, Y):
        self.goAway()
    
    def splashImage256ColorsClick(self, Sender):
        self.goAway()
    
    def OKClick(self, Sender):
        self.goAway()
    
    def FormActivate(self, Sender):
        screenColorBits = 0
        screenDC = HDC()
        
        screenDC = UNRESOLVED.GetDC(0)
        try:
            screenColorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES))
        finally:
            UNRESOLVED.ReleaseDC(0, screenDC)
        if screenColorBits > 8:
            self.splashImageTrueColor.Visible = true
            self.splashImage256Colors.Visible = false
            self.splashImageTrueColor.Left = 0
            self.splashImageTrueColor.Top = 0
            self.splashImageTrueColor.SendToBack()
        else:
            self.splashImage256Colors.Visible = true
            self.splashImageTrueColor.Visible = false
            self.splashImage256Colors.Left = 0
            self.splashImage256Colors.Top = 0
            self.splashImage256Colors.SendToBack()
    
    def closeClick(self, Sender):
        self.ModalResult = mrOK
    
    def supportButtonClick(self, Sender):
        infoForm = TProgramInfoForm()
        
        infoForm = uprginfo.TProgramInfoForm().create(delphi_compatability.Application)
        try:
            infoForm.ShowModal()
        finally:
            infoForm.free
            infoForm = None
    
