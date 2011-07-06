# unit uabout

from conversion_common import *
import uprginfo
import umath
import usupport
import uregister
import udomain
import delphi_compatability

# var
AboutForm = TAboutForm()

class TAboutForm(TForm):
    def __init__(self):
        self.close = TButton()
        self.registerIt = TButton()
        self.readLicense = TButton()
        self.cancel = TButton()
        self.whyRegister = TButton()
        self.versionLabel = TLabel()
        self.registrationInfoPanel = TPanel()
        self.noDistributeLabel = TLabel()
        self.timeWarningLabel = TLabel()
        self.hoursLabel = TLabel()
        self.Label4 = TLabel()
        self.Label5 = TLabel()
        self.Label6 = TLabel()
        self.unregistered2DExportReminder = TImage()
        self.Label7 = TLabel()
        self.Label1 = TLabel()
        self.splashScreenPicture = TImage()
        self.Label2 = TLabel()
        self.unregistered3DExportReminder = TImage()
        self.supportButton = TButton()
        self.exportRestrictionLabel = TLabel()
    
    #$R *.DFM
    def initializeWithWhetherClosingProgram(self, closingProgram):
        if closingProgram:
            self.close.Caption = "Quit"
        else:
            self.close.Caption = "Close"
        self.cancel.Visible = closingProgram
    
    def FormActivate(self, Sender):
        timeBetween = TDateTime()
        hours = 0
        minutes = 0
        seconds = 0
        milliseconds = 0
        smallHours = 0
        randomNumber = 0
        i = 0
        
        self.versionLabel.Caption = usupport.gVersionName
        self.exportRestrictionLabel.Caption = "- restricting the number of exports to " + IntToStr(udomain.kMaxUnregExportsAllowed) + " at first, then " + IntToStr(udomain.kMaxUnregExportsPerSessionAfterMaxReached) + " per session"
        self.ActiveControl = self.registerIt
        UNRESOLVED.randomize
        for i in range(0, 100 + 1):
            UNRESOLVED.random
        randomNumber = UNRESOLVED.random(2)
        if randomNumber == 0:
            self.close.Top = 4
            self.registerIt.Top = self.close.Top + self.close.Height + 3
        elif randomNumber == 1:
            self.registerIt.Top = 4
            self.close.Top = self.registerIt.Top + self.registerIt.Height + 3
        self.hoursLabel.Caption = "You have been evaluating PlantStudio for "
        timeBetween = umath.max((UNRESOLVED.Now - udomain.domain.startTimeThisSession), 0) + udomain.domain.accumulatedUnregisteredTime
        UNRESOLVED.DecodeTime(timeBetween, smallHours, minutes, seconds, milliseconds)
        hours = smallHours
        if timeBetween >= 1.0:
            hours = hours + trunc(timeBetween) * 24
        if (minutes < 1) and (hours < 1):
            self.hoursLabel.Caption = self.hoursLabel.Caption + "less than one minute."
        elif (minutes == 1) and (hours < 1):
            self.hoursLabel.Caption = self.hoursLabel.Caption + "one minute."
        elif hours < 1:
            self.hoursLabel.Caption = self.hoursLabel.Caption + IntToStr(minutes) + " minutes."
        elif hours == 1:
            self.hoursLabel.Caption = self.hoursLabel.Caption + IntToStr(hours) + " hour and " + IntToStr(minutes) + " minutes."
        else:
            self.hoursLabel.Caption = self.hoursLabel.Caption + IntToStr(hours) + " hours and " + IntToStr(minutes) + " minutes."
        self.timeWarningLabel.Caption = "If you have been using PlantStudio for " + IntToStr(usupport.kMaxEvaluationTime_hours) + " hours or more (in total), you are legally required to register it."
        if hours >= usupport.kMaxEvaluationTime_hours:
            self.timeWarningLabel.Font.Color = delphi_compatability.clGreen
            self.timeWarningLabel.Font.Style = [UNRESOLVED.fsBold, ]
    
    def closeClick(self, Sender):
        self.ModalResult = mrOK
    
    def registerItClick(self, Sender):
        if uregister.RegistrationForm.ShowModal() == mrOK:
            self.ModalResult = mrCancel
    
    def readLicenseClick(self, Sender):
        delphi_compatability.Application.HelpJump("License")
    
    def whyRegisterClick(self, Sender):
        delphi_compatability.Application.HelpJump("Why_register?")
    
    def supportButtonClick(self, Sender):
        infoForm = TProgramInfoForm()
        
        infoForm = uprginfo.TProgramInfoForm().create(delphi_compatability.Application)
        try:
            infoForm.ShowModal()
        finally:
            infoForm.free
            infoForm = None
    
