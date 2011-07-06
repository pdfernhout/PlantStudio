// unit ucustdrw

from conversion_common import *;
import updform;
import delphi_compatability;

// const
kTransferLoad = 1;
kTransferSave = 2;



class TCustomDrawOptionsForm extends PdForm {
    public TSpeedButton helpButton;
    public TButton Close;
    public TButton cancel;
    public TGroupBox GroupBox1;
    public TCheckBox sortPolygons;
    public TCheckBox sortTdosAsOneItem;
    public TGroupBox GroupBox2;
    public TLabel lineContrastIndexLabel;
    public TCheckBox fillPolygons;
    public TCheckBox drawLinesBetweenPolygons;
    public TSpinEdit lineContrastIndex;
    public TGroupBox GroupBox3;
    public TCheckBox draw3DObjects;
    public TCheckBox drawStems;
    public TCheckBox draw3DObjectsAsBoundingRectsOnly;
    public DomainOptionsStructure options;
    public short transferDirection;
    public boolean optionsChanged;
    
    //$R *.DFM
    public void FormActivate(TObject Sender) {
        this.transferDirection = kTransferLoad;
        this.transferFields();
        // interactions
        this.drawLinesBetweenPolygons.Enabled = this.fillPolygons.Checked;
        this.lineContrastIndex.Enabled = this.drawLinesBetweenPolygons.Enabled && this.drawLinesBetweenPolygons.Checked;
        this.lineContrastIndexLabel.Enabled = this.lineContrastIndex.Enabled;
        this.sortTdosAsOneItem.Enabled = this.sortPolygons.Checked;
        this.draw3DObjectsAsBoundingRectsOnly.Enabled = this.draw3DObjects.Checked;
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
        this.options.drawStems = this.transferCheckBox(this.drawStems, this.options.drawStems);
        this.options.draw3DObjects = this.transferCheckBox(this.draw3DObjects, this.options.draw3DObjects);
        this.options.draw3DObjectsAsBoundingRectsOnly = this.transferCheckBox(this.draw3DObjectsAsBoundingRectsOnly, this.options.draw3DObjectsAsBoundingRectsOnly);
        this.options.fillPolygons = this.transferCheckBox(this.fillPolygons, this.options.fillPolygons);
        this.options.drawLinesBetweenPolygons = this.transferCheckBox(this.drawLinesBetweenPolygons, this.options.drawLinesBetweenPolygons);
        this.options.lineContrastIndex = this.transferSmallintSpinEditBox(this.lineContrastIndex, this.options.lineContrastIndex);
        this.options.sortPolygons = this.transferCheckBox(this.sortPolygons, this.options.sortPolygons);
        this.options.sortTdosAsOneItem = this.transferCheckBox(this.sortTdosAsOneItem, this.options.sortTdosAsOneItem);
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
    
    public void draw3DObjectsClick(TObject Sender) {
        this.draw3DObjectsAsBoundingRectsOnly.Enabled = this.draw3DObjects.Checked;
    }
    
    public void fillPolygonsClick(TObject Sender) {
        // and (not drawWithOpenGL.checked);
        this.drawLinesBetweenPolygons.Enabled = (this.fillPolygons.Checked);
        this.lineContrastIndex.Enabled = this.drawLinesBetweenPolygons.Enabled && this.drawLinesBetweenPolygons.Checked;
        this.lineContrastIndexLabel.Enabled = this.lineContrastIndex.Enabled;
    }
    
    public void drawLinesBetweenPolygonsClick(TObject Sender) {
        this.lineContrastIndex.Enabled = this.drawLinesBetweenPolygons.Enabled && this.drawLinesBetweenPolygons.Checked;
        this.lineContrastIndexLabel.Enabled = this.lineContrastIndex.Enabled;
    }
    
    public void sortPolygonsClick(TObject Sender) {
        this.sortTdosAsOneItem.Enabled = this.sortPolygons.Checked;
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Changing_the_drawing_speed");
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
}
//
//procedure TOptionsForm.drawWithOpenGLClick(Sender: TObject);
//  begin
//  //drawLinesBetweenPolygons.enabled := (fillPolygons.checked) and (not drawWithOpenGL.checked);
//  //sortPolygons.enabled := not drawWithOpenGL.checked;
//  end;
//
