// unit uanimate

from conversion_common import *;
import updform;
import delphi_compatability;


class TAnimationFilesOptionsForm extends PdForm {
    public TSpeedButton helpButton;
    public TButton Close;
    public TButton cancel;
    public TPanel Panel1;
    public TLabel fileNumberLabel;
    public TLabel animationSizeLabel;
    public TLabel fileSizeLabel;
    public TPanel Panel2;
    public TLabel Label4;
    public TLabel focusedPlantName;
    public TLabel Label5;
    public TGroupBox GroupBox1;
    public TLabel Label1;
    public TLabel resolutionLabel;
    public TLabel incrementLabel;
    public TLabel plantMaxAgeLabel;
    public TLabel colorsLabel;
    public TRadioButton animateByAge;
    public TRadioButton animateByXRotation;
    public TSpinEdit incrementEdit;
    public TSpinEdit resolution;
    public TComboBox colorType;
    public NumberedAnimationOptionsStructure options;
    public PdPlant plant;
    public boolean internalChange;
    
    //$R *.DFM
    public void initializeWithOptionsAndPlant(NumberedAnimationOptionsStructure anOptions, PdPlant aPlant) {
        this.internalChange = true;
        if (aPlant == null) {
            throw new GeneralException.create("Problem: Nil plant in method TAnimationFilesOptionsForm.initializeWithOptionsAndPlant.");
        }
        this.plant = aPlant;
        this.options = anOptions;
        this.focusedPlantName.Caption = this.plant.getName;
        if (this.options.animateBy == UNRESOLVED.kAnimateByAge) {
            this.animateByAge.Checked = true;
        } else if (this.options.animateBy == UNRESOLVED.kAnimateByXRotation) {
            this.animateByXRotation.Checked = true;
        }
        this.changeQuestionsBasedOnAnimationType();
        this.resolution.Value = this.options.resolution_pixelsPerInch;
        this.colorType.ItemIndex = ord(this.options.colorType);
        this.changeQuestionsBasedOnAnimationType();
        this.calculateNumberOfFrames();
        this.internalChange = false;
    }
    
    public void changeQuestionsBasedOnAnimationType() {
        this.internalChange = true;
        if (this.animateByAge.Checked) {
            this.incrementLabel.Caption = "Age increment between &frames (days)";
            this.incrementEdit.Value = this.options.ageIncrement;
        } else {
            this.incrementLabel.Caption = "Rotation increment between &frames (degrees)";
            this.incrementEdit.Value = this.options.xRotationIncrement;
        }
        this.internalChange = false;
    }
    
    public void animateByAgeClick(TObject Sender) {
        if (this.internalChange) {
            return;
        }
        if (this.animateByAge.Checked) {
            this.options.animateBy = UNRESOLVED.kAnimateByAge;
        } else {
            this.options.animateBy = UNRESOLVED.kAnimateByXRotation;
        }
        this.changeQuestionsBasedOnAnimationType();
        this.calculateNumberOfFrames();
    }
    
    public void animateByXRotationClick(TObject Sender) {
        if (this.internalChange) {
            return;
        }
        if (this.animateByAge.Checked) {
            this.options.animateBy = UNRESOLVED.kAnimateByAge;
        } else {
            this.options.animateBy = UNRESOLVED.kAnimateByXRotation;
        }
        this.changeQuestionsBasedOnAnimationType();
        this.calculateNumberOfFrames();
    }
    
    public void incrementEditChange(TObject Sender) {
        short oldValue = 0;
        
        if (this.internalChange) {
            return;
        }
        if (this.animateByAge.Checked) {
            oldValue = this.options.ageIncrement;
        } else {
            oldValue = this.options.xRotationIncrement;
        }
        try {
            if (this.animateByAge.Checked) {
                this.options.ageIncrement = this.incrementEdit.Value;
            } else {
                this.options.xRotationIncrement = this.incrementEdit.Value;
            }
        } catch (Exception e) {
            if (this.animateByAge.Checked) {
                this.options.ageIncrement = oldValue;
            } else {
                this.options.xRotationIncrement = oldValue;
            }
        }
        this.calculateNumberOfFrames();
    }
    
    public void resolutionChange(TObject Sender) {
        short oldValue = 0;
        
        if (this.internalChange) {
            return;
        }
        oldValue = this.options.resolution_pixelsPerInch;
        try {
            this.options.resolution_pixelsPerInch = this.resolution.Value;
        } catch (Exception e) {
            this.options.resolution_pixelsPerInch = oldValue;
        }
        this.calculateNumberOfFrames();
    }
    
    public void calculateNumberOfFrames() {
        float scaleMultiplier = 0.0;
        
        if (this.options.animateBy == UNRESOLVED.kAnimateByAge) {
            this.plantMaxAgeLabel.Caption = "Maximum age = " + IntToStr(this.plant.pGeneral.ageAtMaturity);
            this.plantMaxAgeLabel.Visible = true;
            this.options.frameCount = this.plant.pGeneral.ageAtMaturity / this.options.ageIncrement + 1;
        } else if (this.options.animateBy == UNRESOLVED.kAnimateByXRotation) {
            this.plantMaxAgeLabel.Visible = false;
            this.options.frameCount = 360 / abs(this.options.xRotationIncrement);
        }
        this.fileNumberLabel.Caption = "Number of files:  " + IntToStr(this.options.frameCount);
        scaleMultiplier = UNRESOLVED.safedivExcept(1.0 * this.options.resolution_pixelsPerInch, 1.0 * delphi_compatability.Screen.PixelsPerInch, 1.0);
        this.options.scaledSize = Point(intround(UNRESOLVED.rWidth(this.plant.boundsRect_pixels) * scaleMultiplier), intround(UNRESOLVED.rHeight(this.plant.boundsRect_pixels) * scaleMultiplier));
        this.animationSizeLabel.Caption = "Animation size:  " + IntToStr(this.options.scaledSize.x) + " x " + IntToStr(this.options.scaledSize.y);
        this.options.fileSize = intround(this.options.frameCount * this.options.scaledSize.x * this.options.scaledSize.y * UNRESOLVED.bitsPerPixelForColorType(this.options.colorType) / 8.0) + FIX_sizeof(delphi_compatability.TBitmapInfo);
        if (this.options.fileSize < 1024) {
            this.fileSizeLabel.Caption = "Estimated total size:  " + IntToStr(this.options.fileSize) + " bytes";
        } else if (this.options.fileSize < 1024 * 1024) {
            this.fileSizeLabel.Caption = "Estimated total size:  " + IntToStr(this.options.fileSize / 1024) + " KB";
        } else {
            this.fileSizeLabel.Caption = "Estimated total size:  " + FloatToStrF(this.options.fileSize / (1024 * 1024), UNRESOLVED.ffFixed, 7, 1) + " MB";
        }
        if (this.options.fileSize >= 10.0 * 1024 * 1024) {
            this.fileSizeLabel.Font.Style = {UNRESOLVED.fsBold, };
        } else {
            this.fileSizeLabel.Font.Style = {};
        }
    }
    
    public void colorTypeChange(TObject Sender) {
        this.options.colorType = UNRESOLVED.TPixelFormat(this.colorType.ItemIndex);
        this.calculateNumberOfFrames();
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Making_numbered_animation_files");
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
}
