// unit uborders

from conversion_common import *;
import updform;
import delphi_compatability;

// const
kTransferLoad = 1;
kTransferSave = 2;



class TPrintBordersForm extends PdForm {
    public TButton Close;
    public TButton cancel;
    public TCheckBox printBorderInner;
    public TCheckBox printBorderOuter;
    public TLabel printBorderColorInnerLabel;
    public TPanel printBorderColorInner;
    public TPanel printBorderColorOuter;
    public TLabel printBorderColorOuterLabel;
    public TLabel printBorderWidthInnerLabel;
    public TLabel printBorderWidthOuterLabel;
    public TSpinEdit printBorderWidthInner;
    public TSpinEdit printBorderWidthOuter;
    public TSpeedButton helpButton;
    public BitmapOptionsStructure options;
    public short transferDirection;
    public boolean optionsChanged;
    
    //$R *.DFM
    public void initializeWithOptions(BitmapOptionsStructure anOptions) {
        this.options = anOptions;
        this.transferDirection = kTransferLoad;
        this.transferFields();
        // simple interaction, so just put it in here
        this.printBorderColorInner.Enabled = this.printBorderInner.Checked;
        this.printBorderWidthInner.Enabled = this.printBorderInner.Checked;
        this.printBorderColorInnerLabel.Enabled = this.printBorderInner.Checked;
        this.printBorderWidthInnerLabel.Enabled = this.printBorderInner.Checked;
        this.printBorderColorOuter.Enabled = this.printBorderOuter.Checked;
        this.printBorderWidthOuter.Enabled = this.printBorderOuter.Checked;
        this.printBorderColorOuterLabel.Enabled = this.printBorderOuter.Checked;
        this.printBorderWidthOuterLabel.Enabled = this.printBorderOuter.Checked;
    }
    
    public void transferFields() {
        this.options.printBorderInner = this.transferCheckBox(this.printBorderInner, this.options.printBorderInner);
        this.options.printBorderOuter = this.transferCheckBox(this.printBorderOuter, this.options.printBorderOuter);
        this.transferColor(this.printBorderColorInner, this.options.printBorderColorInner);
        this.transferColor(this.printBorderColorOuter, this.options.printBorderColorOuter);
        this.options.printBorderWidthInner = this.transferSmallintSpinEditBox(this.printBorderWidthInner, this.options.printBorderWidthInner);
        this.options.printBorderWidthOuter = this.transferSmallintSpinEditBox(this.printBorderWidthOuter, this.options.printBorderWidthOuter);
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
    
    public void printBorderColorInnerMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.printBorderColorInner.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.printBorderColorInner.Color);
    }
    
    public void printBorderColorOuterMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.printBorderColorOuter.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.printBorderColorOuter.Color);
    }
    
    public void printBorderInnerClick(TObject Sender) {
        this.printBorderColorInner.Enabled = this.printBorderInner.Checked;
        this.printBorderWidthInner.Enabled = this.printBorderInner.Checked;
        this.printBorderColorInnerLabel.Enabled = this.printBorderInner.Checked;
        this.printBorderWidthInnerLabel.Enabled = this.printBorderInner.Checked;
    }
    
    public void printBorderOuterClick(TObject Sender) {
        this.printBorderColorOuter.Enabled = this.printBorderOuter.Checked;
        this.printBorderWidthOuter.Enabled = this.printBorderOuter.Checked;
        this.printBorderColorOuterLabel.Enabled = this.printBorderOuter.Checked;
        this.printBorderWidthOuterLabel.Enabled = this.printBorderOuter.Checked;
    }
    
    public void CloseClick(TObject Sender) {
        this.transferDirection = kTransferSave;
        this.transferFields();
        this.ModalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Drawing_a_print_border");
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
}
