// unit unozzle

from conversion_common import *;
import updform;
import delphi_compatability;


class TNozzleOptionsForm extends PdForm {
    public TGroupBox GroupBox1;
    public TLabel cellCountLabel;
    public TLabel cellSizeLabel;
    public TSpeedButton helpButton;
    public TButton Close;
    public TButton cancel;
    public TColorDialog ColorDialog;
    public TLabel fileSizeLabel;
    public TPanel Panel1;
    public TLabel Label4;
    public TGroupBox GroupBox2;
    public TLabel resolutionLabel;
    public TLabel Label3;
    public TLabel colorsLabel;
    public TLabel Label1;
    public TPanel backgroundColorPanel;
    public TSpinEdit resolutionEdit;
    public TComboBox colorType;
    public TGroupBox GroupBox3;
    public TRadioButton useSelectedPlants;
    public TRadioButton useVisiblePlants;
    public TRadioButton useAllPlants;
    public NozzleOptionsStructure options;
    
    //$R *.DFM
    public void initializeWithOptions(NozzleOptionsStructure anOptions) {
        this.options = anOptions;
        switch (this.options.exportType) {
            case UNRESOLVED.kIncludeSelectedPlants:
                this.useSelectedPlants.Checked = true;
                break;
            case UNRESOLVED.kIncludeVisiblePlants:
                this.useVisiblePlants.Checked = true;
                break;
            case UNRESOLVED.kIncludeAllPlants:
                this.useAllPlants.Checked = true;
                break;
        this.resolutionEdit.Text = IntToStr(intround(this.options.resolution_pixelsPerInch));
        this.backgroundColorPanel.Color = this.options.backgroundColor;
        this.colorType.ItemIndex = ord(this.options.colorType);
        this.updateCellSizeAndCountForSelection();
    }
    
    public void updateCellSizeAndCountForSelection() {
        boolean excludeInvisiblePlants = false;
        boolean excludeNonSelectedPlants = false;
        TRect cellRect = new TRect();
        float scaleMultiplier = 0.0;
        long fileSize = 0;
        
        excludeInvisiblePlants = !this.useAllPlants.Checked;
        excludeNonSelectedPlants = this.useSelectedPlants.Checked;
        cellRect = UNRESOLVED.domain.plantManager.largestPlantBoundsRect(UNRESOLVED.MainForm.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants);
        scaleMultiplier = UNRESOLVED.safedivExcept(1.0 * this.options.resolution_pixelsPerInch, 1.0 * delphi_compatability.Screen.PixelsPerInch, 1.0);
        this.options.cellSize = Point(intround(UNRESOLVED.rWidth(cellRect) * scaleMultiplier), intround(UNRESOLVED.rHeight(cellRect) * scaleMultiplier));
        if (this.useAllPlants.Checked) {
            this.options.cellCount = UNRESOLVED.domain.plantManager.plants.count;
        } else if (this.useVisiblePlants.Checked) {
            this.options.cellCount = UNRESOLVED.domain.plantManager.visiblePlantCount;
        } else if (this.useSelectedPlants.Checked) {
            this.options.cellCount = UNRESOLVED.MainForm.selectedPlants.count;
        }
        this.cellSizeLabel.Caption = "Nozzle/tube cell width:  " + IntToStr(this.options.cellSize.x) + " height:  " + IntToStr(this.options.cellSize.y);
        this.cellCountLabel.Caption = "Number of items:  " + IntToStr(this.options.cellCount);
        fileSize = intround(this.options.cellCount * this.options.cellSize.x * this.options.cellSize.y * UNRESOLVED.bitsPerPixelForColorType(this.options.colorType) / 8.0) + FIX_sizeof(delphi_compatability.TBitmapInfo);
        if (fileSize < 1024) {
            this.fileSizeLabel.Caption = "Estimated file size:  " + IntToStr(fileSize) + " bytes";
        } else if (fileSize < 1024 * 1024) {
            this.fileSizeLabel.Caption = "Estimated file size:  " + IntToStr(fileSize / 1024) + " KB";
        } else {
            this.fileSizeLabel.Caption = "Estimated file size:  " + FloatToStrF(fileSize / (1024 * 1024), UNRESOLVED.ffFixed, 7, 1) + " MB";
        }
        if (fileSize >= 10.0 * 1024 * 1024) {
            this.fileSizeLabel.Font.Style = {UNRESOLVED.fsBold, };
        } else {
            this.fileSizeLabel.Font.Style = {};
        }
    }
    
    public void changeSelection(TObject Sender) {
        if (Sender == this.useSelectedPlants) {
            this.options.exportType = UNRESOLVED.kIncludeSelectedPlants;
        } else if (Sender == this.useVisiblePlants) {
            this.options.exportType = UNRESOLVED.kIncludeVisiblePlants;
        } else if (Sender == this.useAllPlants) {
            this.options.exportType = UNRESOLVED.kIncludeAllPlants;
        }
        this.updateCellSizeAndCountForSelection();
    }
    
    public void backgroundColorPanelClick(TObject Sender) {
        this.backgroundColorPanel.Color = UNRESOLVED.domain.getColorUsingCustomColors(this.backgroundColorPanel.Color);
        this.options.backgroundColor = this.backgroundColorPanel.Color;
    }
    
    public void resolutionEditChange(TObject Sender) {
        this.options.resolution_pixelsPerInch = StrToIntDef(this.resolutionEdit.Text, intround(this.options.resolution_pixelsPerInch));
        this.updateCellSizeAndCountForSelection();
    }
    
    public void colorTypeChange(TObject Sender) {
        this.options.colorType = UNRESOLVED.TPixelFormat(this.colorType.ItemIndex);
        this.updateCellSizeAndCountForSelection();
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Making_a_nozzle_or_tube");
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
    public void CloseClick(TObject Sender) {
        if ((this.options.exportType == UNRESOLVED.kIncludeSelectedPlants) && (UNRESOLVED.MainForm.selectedPlants.count <= 0)) {
            MessageDialog("You chose \"selected\" for \"Draw which plants\", but no plants are selected." + chr(13) + "You should make another choice, or click Cancel and select some plants.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
        } else {
            this.ModalResult = mrOK;
        }
    }
    
}
