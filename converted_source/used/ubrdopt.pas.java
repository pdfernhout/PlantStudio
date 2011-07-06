// unit Ubrdopt

from conversion_common import *;
import updcom;
import ucommand;
import usupport;
import usection;
import umain;
import udomain;
import uplant;
import delphi_compatability;

// const
kBetweenGap = 4;
kMaxPlantNameLength = 20;



class TBreedingOptionsForm extends PdForm {
    public TButton ok;
    public TButton cancel;
    public TImage upImage;
    public TImage downImage;
    public TTabbedNotebook breedingOptions;
    public TCheckBox treatColorsAsNumbers;
    public TCheckBox chooseTdosRandomly;
    public TEdit currentTdoLibraryFileName;
    public TLabel weightLabel;
    public TLabel weightAmountLabel;
    public TLabel weightZero;
    public KfWinSlider weightSlider;
    public TLabel weightOneHundred;
    public TButton weightSelectAll;
    public TButton weightSelectNone;
    public TListBox weightSections;
    public TLabel mutationLabel;
    public TLabel mutationAmountLabel;
    public TLabel mutationZero;
    public KfWinSlider mutationSlider;
    public TLabel mutationOneHundred;
    public TListBox mutationSections;
    public TButton mutationSelectAll;
    public TButton mutationSelectNone;
    public TLabel nonNumericLabel;
    public TLabel firstPlantIfEqualLabel;
    public TRadioButton alwaysCopyFromFirstPlant;
    public TRadioButton alwaysCopyFromSecondPlant;
    public TRadioButton copyRandomlyBasedOnWeights;
    public TRadioButton copyBasedOnWeightsIfEqualFirstPlant;
    public TRadioButton copyBasedOnWeightsIfEqualSecondPlant;
    public TRadioButton copyBasedOnWeightsIfEqualChooseRandomly;
    public TSpeedButton helpButton;
    public TSpeedButton mutationShowSections;
    public TSpeedButton weightShowSections;
    public TSpeedButton changeTdoLibrary;
    public TGroupBox GroupBox1;
    public TLabel Label4;
    public TLabel Label1;
    public TLabel Label2;
    public TSpinEdit thumbnailWidth;
    public TSpinEdit thumbnailHeight;
    public TGroupBox GroupBox2;
    public TLabel Label3;
    public TSpinEdit plantsPerGeneration;
    public TLabel Label6;
    public TSpinEdit maxGenerations;
    public TLabel Label8;
    public TLabel Label7;
    public TSpinEdit percentMaxAge;
    public TSpinEdit maxPartsPerPlant_thousands;
    public TLabel Label9;
    public TGroupBox GroupBox3;
    public TSpinEdit numTimeSeriesStages;
    public TLabel Label5;
    public TCheckBox updateTimeSeriesPlantsOnParameterChange;
    public BreedingAndTimeSeriesOptionsStructure options;
    public DomainOptionsStructure domainOptions;
    public boolean draggingMutationSlider;
    public boolean draggingWeightSlider;
    public boolean mutationSectionsOpen;
    public boolean weightSectionsOpen;
    
    //$R *.DFM
    // ---------------------------------------------------------------------------------------- create/destroy 
    public void FormCreate(TObject Sender) {
        this.breedingOptions.pageIndex = 0;
        this.mutationSections.Visible = false;
        this.mutationSelectAll.Visible = false;
        this.mutationSelectNone.Visible = false;
        this.weightSections.Visible = false;
        this.weightSelectAll.Visible = false;
        this.weightSelectNone.Visible = false;
        this.loadSectionsIntoListBoxes();
        this.currentTdoLibraryFileName.Text = udomain.domain.defaultTdoLibraryFileName;
        this.currentTdoLibraryFileName.SelStart = len(this.currentTdoLibraryFileName.Text);
    }
    
    public void initializeWithBreedingAndTimeSeriesOptionsAndDomainOptions(BreedingAndTimeSeriesOptionsStructure anOptions, DomainOptionsStructure aDomainOptions) {
        this.options = anOptions;
        this.domainOptions = aDomainOptions;
        this.updateComponentsFromOptions();
    }
    
    // ------------------------------------------------------------------------------- buttons 
    public void okClick(TObject Sender) {
        UNRESOLVED.modalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        UNRESOLVED.modalResult = mrCancel;
    }
    
    // ---------------------------------------------------------------------------- reading breeding options 
    public void updateComponentsFromOptions() {
        this.mutationSections.Invalidate();
        this.weightSections.Invalidate();
        this.mutationSectionsClick(this);
        this.weightSectionsClick(this);
        if (this.radioButtonForChoiceIndex(this.options.getNonNumericalParametersFrom) != null) {
            this.radioButtonForChoiceIndex(this.options.getNonNumericalParametersFrom).Checked = true;
        }
        this.treatColorsAsNumbers.Checked = this.options.mutateAndBlendColorValues;
        this.chooseTdosRandomly.Checked = this.options.chooseTdosRandomlyFromCurrentLibrary;
        // v2.0
        this.plantsPerGeneration.Value = this.options.plantsPerGeneration;
        this.thumbnailWidth.Value = this.options.thumbnailWidth;
        this.thumbnailHeight.Value = this.options.thumbnailHeight;
        this.maxGenerations.Value = this.options.maxGenerations;
        this.numTimeSeriesStages.Value = this.options.numTimeSeriesStages;
        this.percentMaxAge.Value = this.options.percentMaxAge;
        // v2.0 domain options moved from main options dialog
        this.maxPartsPerPlant_thousands.Value = this.domainOptions.maxPartsPerPlant_thousands;
        this.updateTimeSeriesPlantsOnParameterChange.Checked = this.domainOptions.updateTimeSeriesPlantsOnParameterChange;
    }
    
    public TRadioButton radioButtonForChoiceIndex(short index) {
        result = new TRadioButton();
        result = null;
        switch (index) {
            case uplant.kFromFirstPlant:
                result = this.alwaysCopyFromFirstPlant;
                break;
            case uplant.kFromSecondPlant:
                result = this.alwaysCopyFromSecondPlant;
                break;
            case uplant.kFromProbabilityBasedOnWeightsForSection:
                result = this.copyRandomlyBasedOnWeights;
                break;
            case uplant.kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant:
                result = this.copyBasedOnWeightsIfEqualFirstPlant;
                break;
            case uplant.kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant:
                result = this.copyBasedOnWeightsIfEqualSecondPlant;
                break;
            case uplant.kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly:
                result = this.copyBasedOnWeightsIfEqualChooseRandomly;
                break;
        return result;
    }
    
    public short choiceIndexForRadioButton(TRadioButton radio) {
        result = 0;
        result = 0;
        if (radio == this.alwaysCopyFromFirstPlant) {
            result = uplant.kFromFirstPlant;
        } else if (radio == this.alwaysCopyFromSecondPlant) {
            result = uplant.kFromSecondPlant;
        } else if (radio == this.copyRandomlyBasedOnWeights) {
            result = uplant.kFromProbabilityBasedOnWeightsForSection;
        } else if (radio == this.copyBasedOnWeightsIfEqualFirstPlant) {
            result = uplant.kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant;
        } else if (radio == this.copyBasedOnWeightsIfEqualSecondPlant) {
            result = uplant.kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant;
        } else if (radio == this.copyBasedOnWeightsIfEqualChooseRandomly) {
            result = uplant.kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly;
        }
        return result;
    }
    
    // ------------------------------------------------------------ changing breeding strategy 
    public void mutationSliderMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        if ((this.firstSelectedIndex(this.mutationSections) >= 0) || (!this.mutationSectionsOpen)) {
            this.draggingMutationSlider = true;
        }
    }
    
    public void mutationSliderMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        if (this.draggingMutationSlider) {
            this.mutationAmountLabel.Caption = IntToStr(this.mutationSlider.currentValue) + "%";
            this.updateMutationOrWeightFromSlider(uplant.kMutation, this.mutationSectionsOpen, this.mutationSections, this.mutationSlider);
        }
    }
    
    public void mutationSliderMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.draggingMutationSlider = false;
        this.updateMutationOrWeightFromSlider(uplant.kMutation, this.mutationSectionsOpen, this.mutationSections, this.mutationSlider);
    }
    
    public void mutationSliderKeyUp(TObject Sender, byte Key, TShiftState Shift) {
        this.updateMutationOrWeightFromSlider(uplant.kMutation, this.mutationSectionsOpen, this.mutationSections, this.mutationSlider);
        return Key;
    }
    
    public void weightSliderMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        if ((this.firstSelectedIndex(this.weightSections) >= 0) || (!this.weightSectionsOpen)) {
            this.draggingWeightSlider = true;
        }
    }
    
    public void weightSliderMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        if (this.draggingWeightSlider) {
            this.weightAmountLabel.Caption = IntToStr(this.weightSlider.currentValue) + "%";
        }
    }
    
    public void weightSliderMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.draggingWeightSlider = false;
        this.updateMutationOrWeightFromSlider(uplant.kWeight, this.weightSectionsOpen, this.weightSections, this.weightSlider);
    }
    
    public void weightSliderKeyUp(TObject Sender, byte Key, TShiftState Shift) {
        this.updateMutationOrWeightFromSlider(uplant.kWeight, this.weightSectionsOpen, this.weightSections, this.weightSlider);
        return Key;
    }
    
    public void updateMutationOrWeightFromSlider(short which, boolean isOpen, TListBox aListBox, KfWinSlider aSlider) {
        short i = 0;
        
        if (aListBox.Items.Count > 0) {
            for (i = 0; i <= aListBox.Items.Count - 1; i++) {
                if (aListBox.Selected[i] || (!isOpen)) {
                    if (which == uplant.kMutation) {
                        this.options.mutationStrengths[i] = aSlider.currentValue;
                    } else {
                        this.options.firstPlantWeights[i] = aSlider.currentValue;
                    }
                }
            }
        }
        aListBox.Invalidate();
    }
    
    public void alwaysCopyFromFirstPlantClick(TObject Sender) {
        this.updateOptionsForNonNumericChoice();
    }
    
    public void alwaysCopyFromSecondPlantClick(TObject Sender) {
        this.updateOptionsForNonNumericChoice();
    }
    
    public void copyRandomlyBasedOnWeightsClick(TObject Sender) {
        this.updateOptionsForNonNumericChoice();
    }
    
    public void copyBasedOnWeightsIfEqualFirstPlantClick(TObject Sender) {
        this.updateOptionsForNonNumericChoice();
    }
    
    public void copyBasedOnWeightsIfEqualSecondPlantClick(TObject Sender) {
        this.updateOptionsForNonNumericChoice();
    }
    
    public void copyBasedOnWeightsIfEqualChooseRandomlyClick(TObject Sender) {
        this.updateOptionsForNonNumericChoice();
    }
    
    public void updateOptionsForNonNumericChoice() {
        short i = 0;
        TRadioButton radio = new TRadioButton();
        
        if (this.breedingOptions.controlCount > 0) {
            for (i = 1; i <= this.breedingOptions.controlCount - 1; i++) {
                if ((this.breedingOptions.controls[i] instanceof delphi_compatability.TRadioButton)) {
                    // this will work so long as there are no other radio buttons on the notebook
                    radio = ((delphi_compatability.TRadioButton)this.breedingOptions.controls[i]);
                    if (radio.Checked) {
                        this.options.getNonNumericalParametersFrom = this.choiceIndexForRadioButton(radio);
                    }
                    break;
                }
            }
        }
    }
    
    public void treatColorsAsNumbersClick(TObject Sender) {
        this.options.mutateAndBlendColorValues = this.treatColorsAsNumbers.Checked;
    }
    
    public void chooseTdosRandomlyClick(TObject Sender) {
        this.options.chooseTdosRandomlyFromCurrentLibrary = this.chooseTdosRandomly.Checked;
    }
    
    // ------------------------------------------------------------------ sections list boxes 
    public void loadSectionsIntoListBoxes() {
        PdSection section = new PdSection();
        short i = 0;
        
        if ((udomain.domain == null) || (udomain.domain.sectionManager == null)) {
            return;
        }
        this.mutationSections.Clear();
        this.weightSections.Clear();
        if (udomain.domain.sectionManager.sections.Count > 0) {
            for (i = 0; i <= udomain.domain.sectionManager.sections.Count - 1; i++) {
                section = usection.PdSection(udomain.domain.sectionManager.sections.Items[i]);
                if (section.showInParametersWindow) {
                    this.mutationSections.Items.AddObject(section.getName(), section);
                    this.weightSections.Items.AddObject(section.getName(), section);
                }
            }
        }
    }
    
    public void mutationSectionsDrawItem(TWinControl Control, int index, TRect Rect, TOwnerDrawState State) {
        this.drawSectionsListBoxItem(Control, index, Rect, State);
    }
    
    public void weightSectionsDrawItem(TWinControl Control, int index, TRect Rect, TOwnerDrawState State) {
        this.drawSectionsListBoxItem(Control, index, Rect, State);
    }
    
    public void drawSectionsListBoxItem(TWinControl Control, int index, TRect Rect, TOwnerDrawState State) {
        TListBox sectionsListBox = new TListBox();
        PdSection section = new PdSection();
        boolean selected = false;
         cText = [0] * (range(0, 255 + 1) + 1);
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        sectionsListBox = (delphi_compatability.TListBox)Control;
        if (sectionsListBox == null) {
            return;
        }
        if ((sectionsListBox.Items.Count <= 0) || (index < 0) || (index > sectionsListBox.Items.Count - 1)) {
            return;
        }
        selected = (delphi_compatability.TOwnerDrawStateType.odSelected in State);
        // set up section pointer 
        section = (usection.PdSection)sectionsListBox.Items.Objects[index];
        if (section == null) {
            return;
        }
        sectionsListBox.Canvas.Font = sectionsListBox.Font;
        if (selected) {
            sectionsListBox.Canvas.Brush.Color = UNRESOLVED.clHighlight;
            sectionsListBox.Canvas.Font.Color = UNRESOLVED.clHighlightText;
        } else {
            sectionsListBox.Canvas.Brush.Color = sectionsListBox.Color;
            sectionsListBox.Canvas.Font.Color = UNRESOLVED.clBtnText;
        }
        sectionsListBox.Canvas.FillRect(Rect);
        if (sectionsListBox == this.mutationSections) {
            UNRESOLVED.strPCopy(cText, section.getName() + " " + IntToStr(this.options.mutationStrengths[index]) + "%");
        } else {
            UNRESOLVED.strPCopy(cText, section.getName() + " " + IntToStr(this.options.firstPlantWeights[index]) + "/" + IntToStr(100 - this.options.firstPlantWeights[index]));
        }
        // margin for text 
        Rect.left = Rect.left + 2;
        UNRESOLVED.winprocs.drawText(sectionsListBox.Canvas.Handle, cText, len(cText), Rect, delphi_compatability.DT_LEFT);
    }
    
    public void mutationSectionsClick(TObject Sender) {
        this.updateSliderForSelectedSections(uplant.kMutation, this.mutationSectionsOpen, this.mutationSlider, this.mutationSections, this.mutationAmountLabel);
    }
    
    public void weightSectionsClick(TObject Sender) {
        this.updateSliderForSelectedSections(uplant.kWeight, this.weightSectionsOpen, this.weightSlider, this.weightSections, this.weightAmountLabel);
    }
    
    public void updateSliderForSelectedSections(short which, boolean isOpen, KfWinSlider aSlider, TListBox aListBox, TLabel aLabel) {
        short firstSelectedIndex = 0;
        
        if (isOpen) {
            firstSelectedIndex = this.firstSelectedIndex(aListBox);
        } else {
            firstSelectedIndex = 0;
        }
        aSlider.enabled = (firstSelectedIndex >= 0) || (!isOpen);
        if (firstSelectedIndex >= 0) {
            if (which == uplant.kMutation) {
                aSlider.currentValue = this.options.mutationStrengths[firstSelectedIndex];
            } else {
                aSlider.currentValue = this.options.firstPlantWeights[firstSelectedIndex];
            }
        } else {
            aSlider.currentValue = 0;
        }
        aLabel.Caption = IntToStr(aSlider.currentValue) + "%";
        aLabel.Enabled = aSlider.enabled;
        aSlider.invalidate;
    }
    
    public short firstSelectedIndex(TListBox aListBox) {
        result = 0;
        short i = 0;
        
        result = -1;
        if (aListBox.Items.Count <= 0) {
            return result;
        }
        if (aListBox.SelCount < 1) {
            return result;
        }
        for (i = 0; i <= aListBox.Items.Count - 1; i++) {
            if (aListBox.Selected[i]) {
                result = i;
                return result;
            }
        }
        return result;
    }
    
    public void mutationShowSectionsClick(TObject Sender) {
        this.mutationSectionsOpen = !this.mutationSectionsOpen;
        if (this.mutationSectionsOpen) {
            this.mutationShowSections.Glyph = this.upImage.Picture.Bitmap;
            this.mutationSections.Visible = true;
            this.mutationSelectAll.Visible = true;
            this.mutationSelectNone.Visible = true;
            // select all 
            this.mutationSelectAllClick(this);
            this.mutationSectionsClick(this);
        } else {
            this.mutationSections.Visible = false;
            this.mutationSelectAll.Visible = false;
            this.mutationSelectNone.Visible = false;
            this.mutationShowSections.Glyph = this.downImage.Picture.Bitmap;
            this.mutationSectionsClick(this);
        }
        this.mutationSections.Visible = this.mutationSectionsOpen;
    }
    
    public void weightShowSectionsClick(TObject Sender) {
        this.weightSectionsOpen = !this.weightSectionsOpen;
        if (this.weightSectionsOpen) {
            this.weightShowSections.Glyph = this.upImage.Picture.Bitmap;
            this.weightSections.Visible = true;
            this.weightSelectAll.Visible = true;
            this.weightSelectNone.Visible = true;
            // select all 
            this.weightSelectAllClick(this);
            this.weightSectionsClick(this);
        } else {
            this.weightSections.Visible = false;
            this.weightSelectAll.Visible = false;
            this.weightSelectNone.Visible = false;
            this.weightShowSections.Glyph = this.downImage.Picture.Bitmap;
            this.weightSectionsClick(this);
        }
        this.weightSections.Visible = this.weightSectionsOpen;
    }
    
    public void mutationSelectAllClick(TObject Sender) {
        short i = 0;
        
        if (this.mutationSections.Items.Count > 0) {
            for (i = 0; i <= this.mutationSections.Items.Count - 1; i++) {
                this.mutationSections.Selected[i] = true;
            }
        }
    }
    
    public void mutationSelectNoneClick(TObject Sender) {
        short i = 0;
        
        if (this.mutationSections.Items.Count > 0) {
            for (i = 0; i <= this.mutationSections.Items.Count - 1; i++) {
                this.mutationSections.Selected[i] = false;
            }
        }
    }
    
    public void weightSelectAllClick(TObject Sender) {
        short i = 0;
        
        if (this.weightSections.Items.Count > 0) {
            for (i = 0; i <= this.weightSections.Items.Count - 1; i++) {
                this.weightSections.Selected[i] = true;
            }
        }
    }
    
    public void weightSelectNoneClick(TObject Sender) {
        short i = 0;
        
        if (this.weightSections.Items.Count > 0) {
            for (i = 0; i <= this.weightSections.Items.Count - 1; i++) {
                this.weightSections.Selected[i] = false;
            }
        }
    }
    
    public void changeTdoLibraryClick(TObject Sender) {
        String fileNameWithPath = "";
        
        fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypeTdo, udomain.domain.defaultTdoLibraryFileName, "Choose a 3D object library (tdo) file");
        if (fileNameWithPath == "") {
            return;
        }
        this.currentTdoLibraryFileName.Text = fileNameWithPath;
        udomain.domain.defaultTdoLibraryFileName = this.currentTdoLibraryFileName.Text;
        this.currentTdoLibraryFileName.SelStart = len(this.currentTdoLibraryFileName.Text);
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Changing_breeding_options");
    }
    
    public void plantsPerGenerationChange(TObject Sender) {
        short oldValue = 0;
        
        oldValue = this.options.plantsPerGeneration;
        try {
            this.options.plantsPerGeneration = this.plantsPerGeneration.Value;
        } catch (Exception e) {
            this.options.plantsPerGeneration = oldValue;
        }
    }
    
    public void thumbnailWidthChange(TObject Sender) {
        short oldValue = 0;
        
        oldValue = this.options.thumbnailWidth;
        try {
            this.options.thumbnailWidth = this.thumbnailWidth.Value;
        } catch (Exception e) {
            this.options.thumbnailWidth = oldValue;
        }
    }
    
    public void thumbnailHeightChange(TObject Sender) {
        short oldValue = 0;
        
        oldValue = this.options.thumbnailHeight;
        try {
            this.options.thumbnailHeight = this.thumbnailHeight.Value;
        } catch (Exception e) {
            this.options.thumbnailHeight = oldValue;
        }
    }
    
    public void maxGenerationsChange(TObject Sender) {
        short oldValue = 0;
        
        oldValue = this.options.maxGenerations;
        try {
            this.options.maxGenerations = this.maxGenerations.Value;
        } catch (Exception e) {
            this.options.maxGenerations = oldValue;
        }
    }
    
    public void numTimeSeriesStagesChange(TObject Sender) {
        short oldValue = 0;
        
        oldValue = this.options.numTimeSeriesStages;
        try {
            this.options.numTimeSeriesStages = this.numTimeSeriesStages.Value;
        } catch (Exception e) {
            this.options.numTimeSeriesStages = oldValue;
        }
    }
    
    public void percentMaxAgeChange(TObject Sender) {
        short oldValue = 0;
        
        oldValue = this.options.percentMaxAge;
        try {
            this.options.percentMaxAge = this.percentMaxAge.Value;
        } catch (Exception e) {
            this.options.percentMaxAge = oldValue;
        }
    }
    
    public void maxPartsPerPlant_thousandsChange(TObject Sender) {
        short oldValue = 0;
        
        oldValue = this.domainOptions.maxPartsPerPlant_thousands;
        try {
            this.domainOptions.maxPartsPerPlant_thousands = this.maxPartsPerPlant_thousands.Value;
        } catch (Exception e) {
            this.domainOptions.maxPartsPerPlant_thousands = oldValue;
        }
    }
    
    public void updateTimeSeriesPlantsOnParameterChangeClick(TObject Sender) {
        this.domainOptions.updateTimeSeriesPlantsOnParameterChange = this.updateTimeSeriesPlantsOnParameterChange.Checked;
    }
    
}
