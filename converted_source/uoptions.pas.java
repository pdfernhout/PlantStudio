// unit Uoptions

from conversion_common import *;
import ucustdrw;
import updform;
import delphi_compatability;

// const
kTransferLoad = 1;
kTransferSave = 2;



class TOptionsForm extends PdForm {
    public TButton Close;
    public TButton cancel;
    public TTabbedNotebook optionsNotebook;
    public TCheckBox drawWithOpenGL;
    public TGroupBox wholeProgramBox;
    public TPanel backgroundColor;
    public TLabel backgroundColorLabel;
    public TCheckBox showPlantDrawingProgress;
    public TGroupBox GroupBox1;
    public TLabel firstSelectionRectangleColorLabel;
    public TLabel multiSelectionRectangleColorLabel;
    public TPanel firstSelectionRectangleColor;
    public TPanel multiSelectionRectangleColor;
    public TGroupBox GroupBox2;
    public TLabel rotationIncrementLabel;
    public TLabel nudgeDistanceLabel;
    public TSpinEdit rotationIncrement;
    public TSpinEdit nudgeDistance;
    public TGroupBox GroupBox6;
    public TLabel parametersFontSizeLabel;
    public TCheckBox useMetricUnits;
    public TSpinEdit parametersFontSize;
    public TGroupBox GroupBox7;
    public TLabel pauseBeforeHintLabel;
    public TLabel pauseDuringHintLabel;
    public TCheckBox openMostRecentFileAtStart;
    public TSpinEdit pauseBeforeHint;
    public TSpinEdit pauseDuringHint;
    public TSpeedButton helpButton;
    public TSpinEdit resizeKeyUpMultiplierPercent;
    public TLabel resizeDistanceLabel;
    public TGroupBox mainWindowDrawingOptionsBox;
    public TButton customDrawOptions;
    public TLabel Label1;
    public TPanel transparentColor;
    public TLabel transparentColorLabel;
    public TSpinEdit memoryLimitForPlantBitmaps_MB;
    public TLabel memoryLimitLabel;
    public TPanel Panel1;
    public TImage Image1;
    public TSpinEdit pasteRectSize;
    public TLabel pasteRectSizeLabel;
    public TGroupBox GroupBox4;
    public TLabel Label9;
    public TLabel Label10;
    public TPanel ghostingColor;
    public TPanel nonHiddenPosedColor;
    public TPanel selectedPosedColor;
    public TLabel Label3;
    public TGroupBox GroupBox5;
    public TLabel undoLimitLabel;
    public TLabel undoLimitOfPlantsLabel;
    public TSpinEdit undoLimit;
    public TSpinEdit undoLimitOfPlants;
    public TSpinEdit resizeRectSize;
    public TLabel resizeRectSizeLabel;
    public TCheckBox ignoreWindowSettingsInFile;
    public short transferDirection;
    public DomainOptionsStructure options;
    public boolean optionsChanged;
    public short messageShown;
    
    //$R *.DFM
    public void FormCreate(TObject Sender) {
        this.optionsNotebook.pageIndex = 0;
    }
    
    public void FormActivate(TObject Sender) {
        this.transferDirection = kTransferLoad;
        this.transferFields();
    }
    
    public void CloseClick(TObject Sender) {
        this.transferDirection = kTransferSave;
        this.transferFields();
        this.ModalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    public void transferFields() {
        // DRAWING
        this.options.memoryLimitForPlantBitmaps_MB = this.transferSmallintSpinEditBox(this.memoryLimitForPlantBitmaps_MB, this.options.memoryLimitForPlantBitmaps_MB);
        this.transferColor(this.backgroundColor, this.options.backgroundColor);
        this.transferColor(this.transparentColor, this.options.transparentColor);
        this.options.showPlantDrawingProgress = this.transferCheckBox(this.showPlantDrawingProgress, this.options.showPlantDrawingProgress);
        // SELECTING
        this.transferColor(this.firstSelectionRectangleColor, this.options.firstSelectionRectangleColor);
        this.transferColor(this.multiSelectionRectangleColor, this.options.multiSelectionRectangleColor);
        this.options.resizeRectSize = this.transferSmallintSpinEditBox(this.resizeRectSize, this.options.resizeRectSize);
        this.transferColor(this.ghostingColor, this.options.ghostingColor);
        this.transferColor(this.nonHiddenPosedColor, this.options.nonHiddenPosedColor);
        this.transferColor(this.selectedPosedColor, this.options.selectedPosedColor);
        // EDITING
        this.options.rotationIncrement = this.transferSmallintSpinEditBox(this.rotationIncrement, this.options.rotationIncrement);
        this.options.nudgeDistance = this.transferSmallintSpinEditBox(this.nudgeDistance, this.options.nudgeDistance);
        this.options.resizeKeyUpMultiplierPercent = this.transferSmallintSpinEditBox(this.resizeKeyUpMultiplierPercent, this.options.resizeKeyUpMultiplierPercent);
        this.options.pasteRectSize = this.transferSmallintSpinEditBox(this.pasteRectSize, this.options.pasteRectSize);
        // UNDOING
        this.options.undoLimit = this.transferSmallintSpinEditBox(this.undoLimit, this.options.undoLimit);
        this.options.undoLimitOfPlants = this.transferSmallintSpinEditBox(this.undoLimitOfPlants, this.options.undoLimitOfPlants);
        // MISCELLANEOUS
        this.options.openMostRecentFileAtStart = this.transferCheckBox(this.openMostRecentFileAtStart, this.options.openMostRecentFileAtStart);
        // v2.1
        this.options.ignoreWindowSettingsInFile = this.transferCheckBox(this.ignoreWindowSettingsInFile, this.options.ignoreWindowSettingsInFile);
        this.options.useMetricUnits = this.transferCheckBox(this.useMetricUnits, this.options.useMetricUnits);
        this.options.parametersFontSize = this.transferSmallintSpinEditBox(this.parametersFontSize, this.options.parametersFontSize);
        this.options.pauseBeforeHint = this.transferSmallintSpinEditBox(this.pauseBeforeHint, this.options.pauseBeforeHint);
        this.options.pauseDuringHint = this.transferSmallintSpinEditBox(this.pauseDuringHint, this.options.pauseDuringHint);
    }
    
    public void transferCheckBox(TCheckBox checkBox, boolean value) {
        if (this.transferDirection == kTransferLoad) {
            checkBox.Checked = value;
        } else if (this.transferDirection == kTransferSave) {
            if (value != checkBox.Checked) {
                this.optionsChanged = true;
            }
            value = checkBox.Checked;
        }
        return value;
    }
    
    public void transferColor(TPanel colorPanel, TColorRef value) {
        raise "method transferColor had assigned to var parameter value not added to return; fixup manually"
        if (this.transferDirection == kTransferLoad) {
            colorPanel.Color = value;
        } else if (this.transferDirection == kTransferSave) {
            if (value != colorPanel.Color) {
                this.optionsChanged = true;
            }
            value = colorPanel.Color;
        }
    }
    
    public void transferSmallintSpinEditBox(TSpinEdit editBox, short value) {
        if (this.transferDirection == kTransferLoad) {
            editBox.Text = IntToStr(value);
        } else if (this.transferDirection == kTransferSave) {
            if (value != StrToIntDef(editBox.Text, 0)) {
                this.optionsChanged = true;
            }
            value = StrToIntDef(editBox.Text, 0);
        }
        return value;
    }
    
    public void transferFloatEditBox(TEdit editBox, float value) {
        float oldValue = 0.0;
        float newValue = 0.0;
        
        if (this.transferDirection == kTransferLoad) {
            editBox.Text = UNRESOLVED.digitValueString(value);
        } else if (this.transferDirection == kTransferSave) {
            oldValue = value;
            try {
                newValue = StrToFloat(editBox.Text);
            } catch (Exception e) {
                newValue = oldValue;
            }
            if (value != newValue) {
                this.optionsChanged = true;
            }
            value = newValue;
        }
        return value;
    }
    
    public void backgroundColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.backgroundColor.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.backgroundColor.Color);
    }
    
    public void transparentColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        // leave this enabled even if not using private bitmaps
        this.transparentColor.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.transparentColor.Color);
    }
    
    public void firstSelectionRectangleColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.firstSelectionRectangleColor.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.firstSelectionRectangleColor.Color);
    }
    
    public void multiSelectionRectangleColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.multiSelectionRectangleColor.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.multiSelectionRectangleColor.Color);
    }
    
    public void ghostingColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.ghostingColor.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.ghostingColor.Color);
    }
    
    public void nonHiddenPosedColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.nonHiddenPosedColor.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.nonHiddenPosedColor.Color);
    }
    
    public void selectedPosedColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.selectedPosedColor.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.selectedPosedColor.Color);
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Changing_preferences");
    }
    
    public void customDrawOptionsClick(TObject Sender) {
        TCustomDrawOptionsForm customDrawForm = new TCustomDrawOptionsForm();
        int response = 0;
        
        customDrawForm = ucustdrw.TCustomDrawOptionsForm().create(this);
        if (customDrawForm == null) {
            throw new GeneralException.create("Problem: Could not create 3D object mover window.");
        }
        try {
            customDrawForm.options = this.options;
            response = customDrawForm.ShowModal();
            if ((response == mrOK) && (customDrawForm.optionsChanged)) {
                this.options = customDrawForm.options;
                this.optionsChanged = true;
            }
        } finally {
            customDrawForm.free;
        }
    }
    
    public void Image1Click(TObject Sender) {
        switch (this.messageShown) {
            case 0:
                ShowMessage("We would like to take this opportunity" + chr(13) + "to say thank you to our excellent testers, " + chr(13) + "especially Ana, Joanne and Randy.");
                break;
            case 1:
                ShowMessage("Thanks to our parents and families.");
                break;
            case 2:
                ShowMessage("Thanks to our dogs Maize and Comet" + chr(13) + "for their many interesting suggestions.");
                break;
            case 3:
                ShowMessage("Thanks to those who have graciously supported our work.");
                break;
            case 4:
                ShowMessage("Thanks to everyone who sent letters.");
                break;
            case 5:
                ShowMessage("Thanks to those who have spread the word about PlantStudio.");
                break;
            case 6:
                ShowMessage("And thank YOU for trying PlantStudio!");
                break;
        this.messageShown += 1;
    }
    
}
