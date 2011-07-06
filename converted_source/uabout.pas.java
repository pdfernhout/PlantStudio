// unit uabout

from conversion_common import *;
import uprginfo;
import uregister;
import delphi_compatability;

// var
TAboutForm AboutForm = new TAboutForm();



class TAboutForm extends TForm {
    public TButton close;
    public TButton registerIt;
    public TButton readLicense;
    public TButton cancel;
    public TButton whyRegister;
    public TLabel versionLabel;
    public TPanel registrationInfoPanel;
    public TLabel noDistributeLabel;
    public TLabel timeWarningLabel;
    public TLabel hoursLabel;
    public TLabel Label4;
    public TLabel Label5;
    public TLabel Label6;
    public TImage unregistered2DExportReminder;
    public TLabel Label7;
    public TLabel Label1;
    public TImage splashScreenPicture;
    public TLabel Label2;
    public TImage unregistered3DExportReminder;
    public TButton supportButton;
    public TLabel exportRestrictionLabel;
    
    //$R *.DFM
    public void initializeWithWhetherClosingProgram(boolean closingProgram) {
        if (closingProgram) {
            this.close.Caption = "Quit";
        } else {
            this.close.Caption = "Close";
        }
        this.cancel.Visible = closingProgram;
    }
    
    public void FormActivate(TObject Sender) {
        TDateTime timeBetween = new TDateTime();
        byte hours = 0;
        byte minutes = 0;
        byte seconds = 0;
        byte milliseconds = 0;
        byte smallHours = 0;
        int randomNumber = 0;
        short i = 0;
        
        this.versionLabel.Caption = UNRESOLVED.gVersionName;
        this.exportRestrictionLabel.Caption = "- restricting the number of exports to " + IntToStr(UNRESOLVED.kMaxUnregExportsAllowed) + " at first, then " + IntToStr(UNRESOLVED.kMaxUnregExportsPerSessionAfterMaxReached) + " per session";
        this.ActiveControl = this.registerIt;
        UNRESOLVED.randomize;
        for (i = 0; i <= 100; i++) {
            UNRESOLVED.random;
        }
        randomNumber = UNRESOLVED.random(2);
        switch (randomNumber) {
            case 0:
                this.close.Top = 4;
                this.registerIt.Top = this.close.Top + this.close.Height + 3;
                break;
            case 1:
                this.registerIt.Top = 4;
                this.close.Top = this.registerIt.Top + this.registerIt.Height + 3;
                break;
        this.hoursLabel.Caption = "You have been evaluating PlantStudio for ";
        timeBetween = UNRESOLVED.max((UNRESOLVED.Now - UNRESOLVED.domain.startTimeThisSession), 0) + UNRESOLVED.domain.accumulatedUnregisteredTime;
        UNRESOLVED.DecodeTime(timeBetween, smallHours, minutes, seconds, milliseconds);
        hours = smallHours;
        if (timeBetween >= 1.0) {
            hours = hours + trunc(timeBetween) * 24;
        }
        if ((minutes < 1) && (hours < 1)) {
            this.hoursLabel.Caption = this.hoursLabel.Caption + "less than one minute.";
        } else if ((minutes == 1) && (hours < 1)) {
            this.hoursLabel.Caption = this.hoursLabel.Caption + "one minute.";
        } else if (hours < 1) {
            this.hoursLabel.Caption = this.hoursLabel.Caption + IntToStr(minutes) + " minutes.";
        } else if (hours == 1) {
            this.hoursLabel.Caption = this.hoursLabel.Caption + IntToStr(hours) + " hour and " + IntToStr(minutes) + " minutes.";
        } else {
            this.hoursLabel.Caption = this.hoursLabel.Caption + IntToStr(hours) + " hours and " + IntToStr(minutes) + " minutes.";
        }
        this.timeWarningLabel.Caption = "If you have been using PlantStudio for " + IntToStr(UNRESOLVED.kMaxEvaluationTime_hours) + " hours or more (in total), you are legally required to register it.";
        if (hours >= UNRESOLVED.kMaxEvaluationTime_hours) {
            this.timeWarningLabel.Font.Color = delphi_compatability.clGreen;
            this.timeWarningLabel.Font.Style = {UNRESOLVED.fsBold, };
        }
    }
    
    public void closeClick(TObject Sender) {
        this.ModalResult = mrOK;
    }
    
    public void registerItClick(TObject Sender) {
        if (uregister.RegistrationForm.ShowModal() == mrOK) {
            this.ModalResult = mrCancel;
        }
    }
    
    public void readLicenseClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("License");
    }
    
    public void whyRegisterClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Why_register?");
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
