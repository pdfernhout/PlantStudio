// unit uregister

from conversion_common import *;
import udebug;
import uregistersupport;
import updform;
import delphi_compatability;

// var
TRegistrationForm RegistrationForm = new TRegistrationForm();


// const
kMaxUnsuccessfulTries = 10;



class TRegistrationForm extends PdForm {
    public TLabel Label11;
    public TPanel Panel1;
    public TLabel Label3;
    public TLabel Label4;
    public TEdit registrationNameEdit;
    public TEdit registrationCodeEdit;
    public TLabel Label1;
    public TEdit orderPageEdit;
    public TLabel Label2;
    public TLabel Label5;
    public TButton openBrowser;
    public TButton close;
    public TButton readLicense;
    public TButton moreInfo;
    public TButton registerMe;
    public TLabel Label6;
    public TButton PrintButton;
    public TPrintDialog PrintDialog;
    public TRichEdit thankYou;
    public boolean printedDetails;
    public boolean opened;
    public short unsuccessfulRegistrationTries;
    
    //$R *.DFM
    public void FormCreate(TObject Sender) {
        this.thankYou.visible = true;
        this.thankYou.visible = false;
        this.unsuccessfulRegistrationTries = 0;
    }
    
    public void FormActivate(TObject Sender) {
        this.opened = true;
    }
    
    public void openBrowserClick(TObject Sender) {
        UNRESOLVED.ShellExecute(this.Handle, "open", "http://www.kurtz-fernhout.com/order.htm", null, null, delphi_compatability.SW_SHOWNORMAL);
    }
    
    public void registerMeClick(TObject Sender) {
        String cr = "";
        boolean correct = false;
        
        correct = uregistersupport.RegistrationMatch(this.registrationNameEdit.Text, this.registrationCodeEdit.Text);
        if (correct) {
            this.registerMe.Hide();
            this.thankYou.clear;
            cr = chr(13) + chr(10);
            this.thankYou.text = "PlantStudio version 2.x Registration Details" + cr + "-------------------------------------------" + cr + "Registration name:  " + this.registrationNameEdit.Text + cr + "Registration code:  " + this.registrationCodeEdit.Text + cr + cr + "Welcome to the PlantStudio community!" + cr + "You now own a fully registered copy of PlantStudio version 2.x." + cr + cr + "We will save encoded registration information in your settings file in your Windows directory. You should keep a copy of your name and code in a safe place in case you need to reinstall PlantStudio." + cr + cr + "(You should click Print now to print this message.)" + cr + cr + "Be sure to visit our web site to read the latest news about PlantStudio and to see the PlantStudio plant exchange and gallery. Thank you for your business!" + cr + cr + "--- Cynthia Kurtz and Paul Fernhout" + cr + "Kurtz-Fernhout Software" + cr + "http://www.kurtz-fernhout.com" + cr + "-------------------------------------------";
            this.thankYou.left = 4;
            this.thankYou.top = 4;
            this.thankYou.show;
            this.thankYou.bringToFront;
            UNRESOLVED.domain.registrationName = this.registrationNameEdit.Text;
            UNRESOLVED.domain.registrationCode = this.registrationCodeEdit.Text;
            UNRESOLVED.domain.registered = true;
            UNRESOLVED.domain.justRegistered = true;
            this.PrintButton.Visible = true;
        } else {
            if (this.unsuccessfulRegistrationTries >= kMaxUnsuccessfulTries) {
                MessageDialog("The registration name and code you entered are incorrect." + chr(13) + "You have attempted to register " + IntToStr(kMaxUnsuccessfulTries) + " times during this session." + chr(13) + chr(13) + "The program will now close." + chr(13) + "Please restart the program and try again." + chr(13) + chr(13) + "If you are sure your information is correct, contact us for help.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
                delphi_compatability.Application.Terminate();
            } else {
                MessageDialog("The registration name and code you entered are incorrect." + chr(13) + "Please retype them and try again." + chr(13) + chr(13) + "If you are sure they are correct" + chr(13) + "and you still get this message, contact us.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            }
            this.unsuccessfulRegistrationTries += 1;
        }
    }
    
    public void FormCloseQuery(TObject Sender, boolean CanClose) {
        if (!this.opened) {
            return CanClose;
        }
        CanClose = false;
        if ((!UNRESOLVED.domain.registered) && ((trim(this.registrationNameEdit.Text) != "") || (trim(this.registrationCodeEdit.Text) != ""))) {
            // why do this? because people might put in the info, then click OK without clicking Register Me
            // and think they have registered when they have not
            ShowMessage("You entered registration information but didn't finish registering." + chr(13) + "You should click \"Register Me!\" or clear out the registration information.");
            return CanClose;
        }
        if ((UNRESOLVED.domain.registered) && (!this.printedDetails)) {
            if (MessageDialog("You registered but didn't print the information." + chr(13) + "Do you want to leave WITHOUT printing your registration information?", mtConfirmation, mbYesNoCancel, 0) != delphi_compatability.IDYES) {
                return CanClose;
            }
        }
        CanClose = true;
        return CanClose;
    }
    
    public void closeClick(TObject Sender) {
        if (UNRESOLVED.domain.registered) {
            this.ModalResult = mrOK;
        } else {
            this.ModalResult = mrCancel;
        }
    }
    
    public void PrintButtonClick(TObject Sender) {
        if (this.PrintDialog.execute) {
            this.thankYou.print("PlantStudio version 1.x Registration Details");
            this.printedDetails = true;
        }
    }
    
    public void moreInfoClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Why_register?");
    }
    
    public void readLicenseClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("License");
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
}
