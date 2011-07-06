// unit Usplash

from conversion_common import *;
import uprginfo;
import delphi_compatability;

// var
TSplashForm splashForm = new TSplashForm();



class TSplashForm extends TForm {
    public TLabel versionLabel;
    public TLabel loadingLabel;
    public TLabel codeLabel;
    public TImage splashImage256Colors;
    public TImage splashImageTrueColor;
    public TSpeedButton close;
    public TSpeedButton supportButton;
    
    //$R *.DFM
    public void CreateParams(TCreateParams Params) {
        super.CreateParams(Params);
        Params.Style = Params.Style || delphi_compatability.WS_BORDER || delphi_compatability.WS_EX_DLGMODALFRAME;
    }
    
    public void FormCreate(TObject Sender) {
        this.versionLabel.Caption = UNRESOLVED.gVersionName;
    }
    
    public void showLoadingString(String aString) {
        if ((len(aString) > 1) && (aString[len(aString)] == ",")) {
            // remove possible comma at end from registration program
            aString = UNRESOLVED.copy(aString, 1, len(aString) - 1);
        }
        this.loadingLabel.Caption = aString;
        this.Update();
    }
    
    public void showCodeString(String aString) {
        this.codeLabel.Caption = aString;
        this.codeLabel.Show();
        this.Update();
    }
    
    public void goAway() {
        this.ModalResult = mrOK;
    }
    
    public void FormClick(TObject Sender) {
        this.goAway();
    }
    
    public void programNameLabelClick(TObject Sender) {
        this.goAway();
    }
    
    public void controlClick(TObject Sender) {
        this.goAway();
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        this.goAway();
        return Key;
    }
    
    public void FormKeyDown(TObject Sender, byte Key, TShiftState Shift) {
        this.goAway();
        return Key;
    }
    
    public void FormMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.goAway();
    }
    
    public void splashImage256ColorsClick(TObject Sender) {
        this.goAway();
    }
    
    public void OKClick(TObject Sender) {
        this.goAway();
    }
    
    public void FormActivate(TObject Sender) {
        int screenColorBits = 0;
        HDC screenDC = new HDC();
        
        screenDC = UNRESOLVED.GetDC(0);
        try {
            screenColorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES));
        } finally {
            UNRESOLVED.ReleaseDC(0, screenDC);
        }
        if (screenColorBits > 8) {
            this.splashImageTrueColor.Visible = true;
            this.splashImage256Colors.Visible = false;
            this.splashImageTrueColor.Left = 0;
            this.splashImageTrueColor.Top = 0;
            this.splashImageTrueColor.SendToBack();
        } else {
            this.splashImage256Colors.Visible = true;
            this.splashImageTrueColor.Visible = false;
            this.splashImage256Colors.Left = 0;
            this.splashImage256Colors.Top = 0;
            this.splashImage256Colors.SendToBack();
        }
    }
    
    public void closeClick(TObject Sender) {
        this.ModalResult = mrOK;
    }
    
    public void supportButtonClick(TObject Sender) {
        TProgramInfoForm infoForm = new TProgramInfoForm();
        
        infoForm = uprginfo.TProgramInfoForm().create(delphi_compatability.Application);
        try {
            infoForm.ShowModal();
        } finally {
            infoForm.free;
            infoForm = null;
        }
    }
    
}
