# unit uregister

from conversion_common import *
import udebug
import uregistersupport
import usupport
import udomain
import updform
import delphi_compatability

# var
RegistrationForm = TRegistrationForm()

# const
kMaxUnsuccessfulTries = 10

class TRegistrationForm(PdForm):
    def __init__(self):
        self.Label11 = TLabel()
        self.Panel1 = TPanel()
        self.Label3 = TLabel()
        self.Label4 = TLabel()
        self.registrationNameEdit = TEdit()
        self.registrationCodeEdit = TEdit()
        self.Label1 = TLabel()
        self.orderPageEdit = TEdit()
        self.Label2 = TLabel()
        self.Label5 = TLabel()
        self.openBrowser = TButton()
        self.close = TButton()
        self.readLicense = TButton()
        self.moreInfo = TButton()
        self.registerMe = TButton()
        self.Label6 = TLabel()
        self.PrintButton = TButton()
        self.PrintDialog = TPrintDialog()
        self.thankYou = TRichEdit()
        self.printedDetails = false
        self.opened = false
        self.unsuccessfulRegistrationTries = 0
    
    #$R *.DFM
    def FormCreate(self, Sender):
        self.thankYou.visible = true
        self.thankYou.visible = false
        self.unsuccessfulRegistrationTries = 0
    
    def FormActivate(self, Sender):
        self.opened = true
    
    def openBrowserClick(self, Sender):
        UNRESOLVED.ShellExecute(self.Handle, "open", "http://www.kurtz-fernhout.com/order.htm", None, None, delphi_compatability.SW_SHOWNORMAL)
    
    def registerMeClick(self, Sender):
        cr = ""
        correct = false
        
        correct = uregistersupport.RegistrationMatch(self.registrationNameEdit.Text, self.registrationCodeEdit.Text)
        if correct:
            self.registerMe.Hide()
            self.thankYou.clear
            cr = chr(13) + chr(10)
            self.thankYou.text = "PlantStudio version 2.x Registration Details" + cr + "-------------------------------------------" + cr + "Registration name:  " + self.registrationNameEdit.Text + cr + "Registration code:  " + self.registrationCodeEdit.Text + cr + cr + "Welcome to the PlantStudio community!" + cr + "You now own a fully registered copy of PlantStudio version 2.x." + cr + cr + "We will save encoded registration information in your settings file in your Windows directory. You should keep a copy of your name and code in a safe place in case you need to reinstall PlantStudio." + cr + cr + "(You should click Print now to print this message.)" + cr + cr + "Be sure to visit our web site to read the latest news about PlantStudio and to see the PlantStudio plant exchange and gallery. Thank you for your business!" + cr + cr + "--- Cynthia Kurtz and Paul Fernhout" + cr + "Kurtz-Fernhout Software" + cr + "http://www.kurtz-fernhout.com" + cr + "-------------------------------------------"
            self.thankYou.left = 4
            self.thankYou.top = 4
            self.thankYou.show
            self.thankYou.bringToFront
            udomain.domain.registrationName = self.registrationNameEdit.Text
            udomain.domain.registrationCode = self.registrationCodeEdit.Text
            udomain.domain.registered = true
            udomain.domain.justRegistered = true
            self.PrintButton.Visible = true
        else:
            if self.unsuccessfulRegistrationTries >= kMaxUnsuccessfulTries:
                MessageDialog("The registration name and code you entered are incorrect." + chr(13) + "You have attempted to register " + IntToStr(kMaxUnsuccessfulTries) + " times during this session." + chr(13) + chr(13) + "The program will now close." + chr(13) + "Please restart the program and try again." + chr(13) + chr(13) + "If you are sure your information is correct, contact us for help.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
                delphi_compatability.Application.Terminate()
            else:
                MessageDialog("The registration name and code you entered are incorrect." + chr(13) + "Please retype them and try again." + chr(13) + chr(13) + "If you are sure they are correct" + chr(13) + "and you still get this message, contact us.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            self.unsuccessfulRegistrationTries += 1
    
    def FormCloseQuery(self, Sender, CanClose):
        if not self.opened:
            return CanClose
        CanClose = false
        if (not udomain.domain.registered) and ((trim(self.registrationNameEdit.Text) != "") or (trim(self.registrationCodeEdit.Text) != "")):
            # why do this? because people might put in the info, then click OK without clicking Register Me
            # and think they have registered when they have not
            ShowMessage("You entered registration information but didn't finish registering." + chr(13) + "You should click \"Register Me!\" or clear out the registration information.")
            return CanClose
        if (udomain.domain.registered) and (not self.printedDetails):
            if MessageDialog("You registered but didn't print the information." + chr(13) + "Do you want to leave WITHOUT printing your registration information?", mtConfirmation, mbYesNoCancel, 0) != delphi_compatability.IDYES:
                return CanClose
        CanClose = true
        return CanClose
    
    def closeClick(self, Sender):
        if udomain.domain.registered:
            self.ModalResult = mrOK
        else:
            self.ModalResult = mrCancel
    
    def PrintButtonClick(self, Sender):
        if self.PrintDialog.execute:
            self.thankYou.print("PlantStudio version 1.x Registration Details")
            self.printedDetails = true
    
    def moreInfoClick(self, Sender):
        delphi_compatability.Application.HelpJump("Why_register?")
    
    def readLicenseClick(self, Sender):
        delphi_compatability.Application.HelpJump("License")
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
