// unit Udebug

from conversion_common import *;
import uprginfo;
import updform;
import delphi_compatability;

// var
TDebugForm DebugForm = new TDebugForm();


//$R *.DFM
public void DebugPrint(String aMessage) {
    if (DebugForm != null) {
        DebugForm.print(aMessage);
    }
}

// const
kBetweenGap = 4;



class TDebugForm extends PdForm {
    public TListBox DebugList;
    public TButton Close;
    public TButton saveListAs;
    public TButton clearList;
    public TPanel optionsPanel;
    public TLabel exceptionLabel;
    public TCheckBox showOnExceptionCheckBox;
    public TCheckBox logToFile;
    public TSpeedButton helpButton;
    public TButton supportButton;
    public TextFile outputFile;
    public boolean logging;
    
    public void FormCreate(TObject Sender) {
        TRect tempBoundsRect = new TRect();
        
        // keep window on screen - left corner of title bar 
        tempBoundsRect = UNRESOLVED.domain.debugWindowRect;
        if ((tempBoundsRect.Left != 0) || (tempBoundsRect.Right != 0) || (tempBoundsRect.Top != 0) || (tempBoundsRect.Bottom != 0)) {
            if (tempBoundsRect.Left > delphi_compatability.Screen.Width - UNRESOLVED.kMinWidthOnScreen) {
                tempBoundsRect.Left = delphi_compatability.Screen.Width - UNRESOLVED.kMinWidthOnScreen;
            }
            if (tempBoundsRect.Top > delphi_compatability.Screen.Height - UNRESOLVED.kMinHeightOnScreen) {
                tempBoundsRect.Top = delphi_compatability.Screen.Height - UNRESOLVED.kMinHeightOnScreen;
            }
            this.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom);
        }
        this.showOnExceptionCheckBox.Checked = UNRESOLVED.domain.options.showWindowOnException;
        this.logToFile.Checked = UNRESOLVED.domain.options.logToFileOnException;
        // this will make the list box create a horizontal scroll bar 
        UNRESOLVED.sendMessage(this.DebugList.Handle, UNRESOLVED.LB_SETHORIZONTALEXTENT, 1000, 0);
    }
    
    public void FormDestroy(TObject Sender) {
        this.stopLogging();
    }
    
    public void startLogging(String fileName) {
        String dateString = "";
        
        if (this.logging) {
            return;
        }
        AssignFile(this.outputFile, fileName);
        if (!FileExists(fileName)) {
            // v1.5
            UNRESOLVED.setDecimalSeparator;
            Rewrite(this.outputFile);
        } else {
            // v1.5
            UNRESOLVED.setDecimalSeparator;
            UNRESOLVED.append(this.outputFile);
            dateString = UNRESOLVED.formatDateTime("m/d/yyyy, h:m am/pm", UNRESOLVED.now);
            writeln(this.outputFile, "---- log start (" + dateString + ") ----");
        }
        this.logging = true;
    }
    
    public void stopLogging() {
        if (!this.logging) {
            return;
        }
        writeln(this.outputFile, "---- log stop ----");
        CloseFile(this.outputFile);
        this.logging = false;
    }
    
    public void saveExceptionListToFile(String fileName) {
        long i = 0;
        
        AssignFile(this.outputFile, fileName);
        // v1.5
        UNRESOLVED.setDecimalSeparator;
        Rewrite(this.outputFile);
        try {
            if (this.DebugList.Items.Count > 0) {
                for (i = 0; i <= this.DebugList.Items.Count - 1; i++) {
                    writeln(this.outputFile, this.DebugList.Items[i]);
                }
            }
        } finally {
            CloseFile(this.outputFile);
        }
    }
    
    public void printNested(long level, String aString) {
        long i = 0;
        ansistring prefix = new ansistring();
        
        if (level > 40) {
            level = 40;
        }
        prefix = "";
        if (level > 0) {
            for (i = 1; i <= level; i++) {
                UNRESOLVED.AppendStr(prefix, "..");
            }
        }
        this.print(prefix + aString);
    }
    
    public void print(String aString) {
        if (this.logging) {
            writeln(this.outputFile, aString);
            Flush(this.outputFile);
        }
        if (UNRESOLVED.domain.options.showWindowOnException) {
            this.Visible = true;
            this.BringToFront();
        }
        if (this.DebugList.Items.Count > 1000) {
            this.DebugList.Items.Clear();
        }
        try {
            this.DebugList.Items.Add(aString);
        } catch (EOutOfResources e) {
            this.DebugList.Items.Clear();
        }
        this.DebugList.ItemIndex = this.DebugList.Items.Count - 1;
        this.DebugList.Invalidate();
        this.DebugList.Refresh();
    }
    
    public void clear() {
        this.Visible = false;
        this.DebugList.Items.Clear();
    }
    
    public void CloseClick(TObject Sender) {
        this.Visible = false;
    }
    
    public void saveListAsClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        
        if (this.DebugList.Items.Count <= 0) {
            return;
        }
        if (!UNRESOLVED.getFileSaveInfo(UNRESOLVED.kFileTypeExceptionList, UNRESOLVED.kAskForFileName, "pstudio.nex", fileInfo)) {
            return;
        }
        try {
            this.saveExceptionListToFile(fileInfo.tempFile);
            fileInfo.writingWasSuccessful = true;
        } finally {
            UNRESOLVED.cleanUpAfterFileSave(fileInfo);
        }
    }
    
    public void clearListClick(TObject Sender) {
        if (this.DebugList.Items.Count <= 0) {
            return;
        }
        this.DebugList.Items.Clear();
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Numerical_exceptions");
    }
    
    public void FormResize(TObject Sender) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        this.Close.Left = this.ClientWidth - this.Close.Width - kBetweenGap;
        this.saveListAs.Left = this.Close.Left;
        this.clearList.Left = this.Close.Left;
        this.helpButton.Left = this.Close.Left;
        this.supportButton.Left = this.Close.Left;
        this.DebugList.SetBounds(kBetweenGap, kBetweenGap, this.Close.Left - kBetweenGap * 2, UNRESOLVED.intMax(0, this.ClientHeight - this.optionsPanel.Height - kBetweenGap * 3));
        this.optionsPanel.SetBounds(kBetweenGap, UNRESOLVED.intMax(0, this.ClientHeight - this.optionsPanel.Height - kBetweenGap), this.Close.Left - kBetweenGap * 2, this.optionsPanel.Height);
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 350;
        UNRESOLVED.ptMinTrackSize.y = 190;
    }
    
    public void logToFileClick(TObject Sender) {
        UNRESOLVED.domain.options.logToFileOnException = this.logToFile.Checked;
        if (!this.logging) {
            this.startLogging(ExtractFilePath(delphi_compatability.Application.exeName) + "errors.nex");
        } else {
            this.stopLogging();
        }
        this.logging = this.logToFile.Checked;
    }
    
    public void showOnExceptionCheckBoxClick(TObject Sender) {
        UNRESOLVED.domain.options.showWindowOnException = this.showOnExceptionCheckBox.Checked;
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
