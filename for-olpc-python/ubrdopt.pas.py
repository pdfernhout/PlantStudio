# unit Ubrdopt

from conversion_common import *
import ucursor
import updcom
import ucommand
import usupport
import usection
import umain
import uwinsliders
import updform
import udomain
import ubrstrat
import uplant
import delphi_compatability

# const
kBetweenGap = 4
kMaxPlantNameLength = 20

class TBreedingOptionsForm(PdForm):
    def __init__(self):
        self.ok = TButton()
        self.cancel = TButton()
        self.upImage = TImage()
        self.downImage = TImage()
        self.breedingOptions = TTabbedNotebook()
        self.treatColorsAsNumbers = TCheckBox()
        self.chooseTdosRandomly = TCheckBox()
        self.currentTdoLibraryFileName = TEdit()
        self.weightLabel = TLabel()
        self.weightAmountLabel = TLabel()
        self.weightZero = TLabel()
        self.weightSlider = KfWinSlider()
        self.weightOneHundred = TLabel()
        self.weightSelectAll = TButton()
        self.weightSelectNone = TButton()
        self.weightSections = TListBox()
        self.mutationLabel = TLabel()
        self.mutationAmountLabel = TLabel()
        self.mutationZero = TLabel()
        self.mutationSlider = KfWinSlider()
        self.mutationOneHundred = TLabel()
        self.mutationSections = TListBox()
        self.mutationSelectAll = TButton()
        self.mutationSelectNone = TButton()
        self.nonNumericLabel = TLabel()
        self.firstPlantIfEqualLabel = TLabel()
        self.alwaysCopyFromFirstPlant = TRadioButton()
        self.alwaysCopyFromSecondPlant = TRadioButton()
        self.copyRandomlyBasedOnWeights = TRadioButton()
        self.copyBasedOnWeightsIfEqualFirstPlant = TRadioButton()
        self.copyBasedOnWeightsIfEqualSecondPlant = TRadioButton()
        self.copyBasedOnWeightsIfEqualChooseRandomly = TRadioButton()
        self.helpButton = TSpeedButton()
        self.mutationShowSections = TSpeedButton()
        self.weightShowSections = TSpeedButton()
        self.changeTdoLibrary = TSpeedButton()
        self.GroupBox1 = TGroupBox()
        self.Label4 = TLabel()
        self.Label1 = TLabel()
        self.Label2 = TLabel()
        self.thumbnailWidth = TSpinEdit()
        self.thumbnailHeight = TSpinEdit()
        self.GroupBox2 = TGroupBox()
        self.Label3 = TLabel()
        self.plantsPerGeneration = TSpinEdit()
        self.Label6 = TLabel()
        self.maxGenerations = TSpinEdit()
        self.Label8 = TLabel()
        self.Label7 = TLabel()
        self.percentMaxAge = TSpinEdit()
        self.maxPartsPerPlant_thousands = TSpinEdit()
        self.Label9 = TLabel()
        self.GroupBox3 = TGroupBox()
        self.numTimeSeriesStages = TSpinEdit()
        self.Label5 = TLabel()
        self.updateTimeSeriesPlantsOnParameterChange = TCheckBox()
        self.options = BreedingAndTimeSeriesOptionsStructure()
        self.domainOptions = DomainOptionsStructure()
        self.draggingMutationSlider = false
        self.draggingWeightSlider = false
        self.mutationSectionsOpen = false
        self.weightSectionsOpen = false
    
    #$R *.DFM
    # ---------------------------------------------------------------------------------------- create/destroy 
    def FormCreate(self, Sender):
        self.breedingOptions.pageIndex = 0
        self.mutationSections.Visible = false
        self.mutationSelectAll.Visible = false
        self.mutationSelectNone.Visible = false
        self.weightSections.Visible = false
        self.weightSelectAll.Visible = false
        self.weightSelectNone.Visible = false
        self.loadSectionsIntoListBoxes()
        self.currentTdoLibraryFileName.Text = udomain.domain.defaultTdoLibraryFileName
        self.currentTdoLibraryFileName.SelStart = len(self.currentTdoLibraryFileName.Text)
    
    def initializeWithBreedingAndTimeSeriesOptionsAndDomainOptions(self, anOptions, aDomainOptions):
        self.options = anOptions
        self.domainOptions = aDomainOptions
        self.updateComponentsFromOptions()
    
    # ------------------------------------------------------------------------------- buttons 
    def okClick(self, Sender):
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    # ---------------------------------------------------------------------------- reading breeding options 
    def updateComponentsFromOptions(self):
        self.mutationSections.Invalidate()
        self.weightSections.Invalidate()
        self.mutationSectionsClick(self)
        self.weightSectionsClick(self)
        if self.radioButtonForChoiceIndex(self.options.getNonNumericalParametersFrom) != None:
            self.radioButtonForChoiceIndex(self.options.getNonNumericalParametersFrom).Checked = true
        self.treatColorsAsNumbers.Checked = self.options.mutateAndBlendColorValues
        self.chooseTdosRandomly.Checked = self.options.chooseTdosRandomlyFromCurrentLibrary
        # v2.0
        self.plantsPerGeneration.Value = self.options.plantsPerGeneration
        self.thumbnailWidth.Value = self.options.thumbnailWidth
        self.thumbnailHeight.Value = self.options.thumbnailHeight
        self.maxGenerations.Value = self.options.maxGenerations
        self.numTimeSeriesStages.Value = self.options.numTimeSeriesStages
        self.percentMaxAge.Value = self.options.percentMaxAge
        # v2.0 domain options moved from main options dialog
        self.maxPartsPerPlant_thousands.Value = self.domainOptions.maxPartsPerPlant_thousands
        self.updateTimeSeriesPlantsOnParameterChange.Checked = self.domainOptions.updateTimeSeriesPlantsOnParameterChange
    
    def radioButtonForChoiceIndex(self, index):
        result = TRadioButton()
        result = None
        if index == ubrstrat.kFromFirstPlant:
            result = self.alwaysCopyFromFirstPlant
        elif index == ubrstrat.kFromSecondPlant:
            result = self.alwaysCopyFromSecondPlant
        elif index == ubrstrat.kFromProbabilityBasedOnWeightsForSection:
            result = self.copyRandomlyBasedOnWeights
        elif index == ubrstrat.kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant:
            result = self.copyBasedOnWeightsIfEqualFirstPlant
        elif index == ubrstrat.kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant:
            result = self.copyBasedOnWeightsIfEqualSecondPlant
        elif index == ubrstrat.kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly:
            result = self.copyBasedOnWeightsIfEqualChooseRandomly
        return result
    
    def choiceIndexForRadioButton(self, radio):
        result = 0
        result = 0
        if radio == self.alwaysCopyFromFirstPlant:
            result = ubrstrat.kFromFirstPlant
        elif radio == self.alwaysCopyFromSecondPlant:
            result = ubrstrat.kFromSecondPlant
        elif radio == self.copyRandomlyBasedOnWeights:
            result = ubrstrat.kFromProbabilityBasedOnWeightsForSection
        elif radio == self.copyBasedOnWeightsIfEqualFirstPlant:
            result = ubrstrat.kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant
        elif radio == self.copyBasedOnWeightsIfEqualSecondPlant:
            result = ubrstrat.kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant
        elif radio == self.copyBasedOnWeightsIfEqualChooseRandomly:
            result = ubrstrat.kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly
        return result
    
    # ------------------------------------------------------------ changing breeding strategy 
    def mutationSliderMouseDown(self, Sender, Button, Shift, X, Y):
        if (self.firstSelectedIndex(self.mutationSections) >= 0) or (not self.mutationSectionsOpen):
            self.draggingMutationSlider = true
    
    def mutationSliderMouseMove(self, Sender, Shift, X, Y):
        if self.draggingMutationSlider:
            self.mutationAmountLabel.Caption = IntToStr(self.mutationSlider.CurrentValue) + "%"
            self.updateMutationOrWeightFromSlider(ubrstrat.kMutation, self.mutationSectionsOpen, self.mutationSections, self.mutationSlider)
    
    def mutationSliderMouseUp(self, Sender, Button, Shift, X, Y):
        self.draggingMutationSlider = false
        self.updateMutationOrWeightFromSlider(ubrstrat.kMutation, self.mutationSectionsOpen, self.mutationSections, self.mutationSlider)
    
    def mutationSliderKeyUp(self, Sender, Key, Shift):
        self.updateMutationOrWeightFromSlider(ubrstrat.kMutation, self.mutationSectionsOpen, self.mutationSections, self.mutationSlider)
        return Key
    
    def weightSliderMouseDown(self, Sender, Button, Shift, X, Y):
        if (self.firstSelectedIndex(self.weightSections) >= 0) or (not self.weightSectionsOpen):
            self.draggingWeightSlider = true
    
    def weightSliderMouseMove(self, Sender, Shift, X, Y):
        if self.draggingWeightSlider:
            self.weightAmountLabel.Caption = IntToStr(self.weightSlider.CurrentValue) + "%"
    
    def weightSliderMouseUp(self, Sender, Button, Shift, X, Y):
        self.draggingWeightSlider = false
        self.updateMutationOrWeightFromSlider(ubrstrat.kWeight, self.weightSectionsOpen, self.weightSections, self.weightSlider)
    
    def weightSliderKeyUp(self, Sender, Key, Shift):
        self.updateMutationOrWeightFromSlider(ubrstrat.kWeight, self.weightSectionsOpen, self.weightSections, self.weightSlider)
        return Key
    
    def updateMutationOrWeightFromSlider(self, which, isOpen, aListBox, aSlider):
        i = 0
        
        if aListBox.Items.Count > 0:
            for i in range(0, aListBox.Items.Count):
                if aListBox.Selected[i] or (not isOpen):
                    if which == ubrstrat.kMutation:
                        self.options.mutationStrengths[i] = aSlider.CurrentValue
                    else:
                        self.options.firstPlantWeights[i] = aSlider.CurrentValue
        aListBox.Invalidate()
    
    def alwaysCopyFromFirstPlantClick(self, Sender):
        self.updateOptionsForNonNumericChoice()
    
    def alwaysCopyFromSecondPlantClick(self, Sender):
        self.updateOptionsForNonNumericChoice()
    
    def copyRandomlyBasedOnWeightsClick(self, Sender):
        self.updateOptionsForNonNumericChoice()
    
    def copyBasedOnWeightsIfEqualFirstPlantClick(self, Sender):
        self.updateOptionsForNonNumericChoice()
    
    def copyBasedOnWeightsIfEqualSecondPlantClick(self, Sender):
        self.updateOptionsForNonNumericChoice()
    
    def copyBasedOnWeightsIfEqualChooseRandomlyClick(self, Sender):
        self.updateOptionsForNonNumericChoice()
    
    def updateOptionsForNonNumericChoice(self):
        i = 0
        radio = TRadioButton()
        
        if self.breedingOptions.controlCount > 0:
            for i in range(1, self.breedingOptions.controlCount):
                if (self.breedingOptions.controls[i].__class__ is delphi_compatability.TRadioButton):
                    # this will work so long as there are no other radio buttons on the notebook
                    radio = (self.breedingOptions.controls[i] as delphi_compatability.TRadioButton)
                    if radio.Checked:
                        self.options.getNonNumericalParametersFrom = self.choiceIndexForRadioButton(radio)
                    break
    
    def treatColorsAsNumbersClick(self, Sender):
        self.options.mutateAndBlendColorValues = self.treatColorsAsNumbers.Checked
    
    def chooseTdosRandomlyClick(self, Sender):
        self.options.chooseTdosRandomlyFromCurrentLibrary = self.chooseTdosRandomly.Checked
    
    # ------------------------------------------------------------------ sections list boxes 
    def loadSectionsIntoListBoxes(self):
        section = PdSection()
        i = 0
        
        if (udomain.domain == None) or (udomain.domain.sectionManager == None):
            return
        self.mutationSections.Clear()
        self.weightSections.Clear()
        if udomain.domain.sectionManager.sections.Count > 0:
            for i in range(0, udomain.domain.sectionManager.sections.Count):
                section = usection.PdSection(udomain.domain.sectionManager.sections.Items[i])
                if section.showInParametersWindow:
                    self.mutationSections.Items.AddObject(section.getName(), section)
                    self.weightSections.Items.AddObject(section.getName(), section)
    
    def mutationSectionsDrawItem(self, Control, index, Rect, State):
        self.drawSectionsListBoxItem(Control, index, Rect, State)
    
    def weightSectionsDrawItem(self, Control, index, Rect, State):
        self.drawSectionsListBoxItem(Control, index, Rect, State)
    
    def drawSectionsListBoxItem(self, Control, index, Rect, State):
        sectionsListBox = TListBox()
        section = PdSection()
        selected = false
        cText = [0] * (range(0, 255 + 1) + 1)
        
        if delphi_compatability.Application.terminated:
            return
        sectionsListBox = Control as delphi_compatability.TListBox
        if sectionsListBox == None:
            return
        if (sectionsListBox.Items.Count <= 0) or (index < 0) or (index > sectionsListBox.Items.Count - 1):
            return
        selected = (delphi_compatability.TOwnerDrawStateType.odSelected in State)
        # set up section pointer 
        section = sectionsListBox.Items.Objects[index] as usection.PdSection
        if section == None:
            return
        sectionsListBox.Canvas.Font = sectionsListBox.Font
        if selected:
            sectionsListBox.Canvas.Brush.Color = UNRESOLVED.clHighlight
            sectionsListBox.Canvas.Font.Color = UNRESOLVED.clHighlightText
        else:
            sectionsListBox.Canvas.Brush.Color = sectionsListBox.Color
            sectionsListBox.Canvas.Font.Color = UNRESOLVED.clBtnText
        sectionsListBox.Canvas.FillRect(Rect)
        if sectionsListBox == self.mutationSections:
            UNRESOLVED.strPCopy(cText, section.getName() + " " + IntToStr(self.options.mutationStrengths[index]) + "%")
        else:
            UNRESOLVED.strPCopy(cText, section.getName() + " " + IntToStr(self.options.firstPlantWeights[index]) + "/" + IntToStr(100 - self.options.firstPlantWeights[index]))
        # margin for text 
        Rect.left = Rect.left + 2
        UNRESOLVED.winprocs.drawText(sectionsListBox.Canvas.Handle, cText, len(cText), Rect, delphi_compatability.DT_LEFT)
    
    def mutationSectionsClick(self, Sender):
        self.updateSliderForSelectedSections(ubrstrat.kMutation, self.mutationSectionsOpen, self.mutationSlider, self.mutationSections, self.mutationAmountLabel)
    
    def weightSectionsClick(self, Sender):
        self.updateSliderForSelectedSections(ubrstrat.kWeight, self.weightSectionsOpen, self.weightSlider, self.weightSections, self.weightAmountLabel)
    
    def updateSliderForSelectedSections(self, which, isOpen, aSlider, aListBox, aLabel):
        firstSelectedIndex = 0
        
        if isOpen:
            firstSelectedIndex = self.firstSelectedIndex(aListBox)
        else:
            firstSelectedIndex = 0
        aSlider.Enabled = (firstSelectedIndex >= 0) or (not isOpen)
        if firstSelectedIndex >= 0:
            if which == ubrstrat.kMutation:
                aSlider.CurrentValue = self.options.mutationStrengths[firstSelectedIndex]
            else:
                aSlider.CurrentValue = self.options.firstPlantWeights[firstSelectedIndex]
        else:
            aSlider.CurrentValue = 0
        aLabel.Caption = IntToStr(aSlider.CurrentValue) + "%"
        aLabel.Enabled = aSlider.Enabled
        aSlider.Invalidate()
    
    def firstSelectedIndex(self, aListBox):
        result = 0
        i = 0
        
        result = -1
        if aListBox.Items.Count <= 0:
            return result
        if aListBox.SelCount < 1:
            return result
        for i in range(0, aListBox.Items.Count):
            if aListBox.Selected[i]:
                result = i
                return result
        return result
    
    def mutationShowSectionsClick(self, Sender):
        self.mutationSectionsOpen = not self.mutationSectionsOpen
        if self.mutationSectionsOpen:
            self.mutationShowSections.Glyph = self.upImage.Picture.Bitmap
            self.mutationSections.Visible = true
            self.mutationSelectAll.Visible = true
            self.mutationSelectNone.Visible = true
            # select all 
            self.mutationSelectAllClick(self)
            self.mutationSectionsClick(self)
        else:
            self.mutationSections.Visible = false
            self.mutationSelectAll.Visible = false
            self.mutationSelectNone.Visible = false
            self.mutationShowSections.Glyph = self.downImage.Picture.Bitmap
            self.mutationSectionsClick(self)
        self.mutationSections.Visible = self.mutationSectionsOpen
    
    def weightShowSectionsClick(self, Sender):
        self.weightSectionsOpen = not self.weightSectionsOpen
        if self.weightSectionsOpen:
            self.weightShowSections.Glyph = self.upImage.Picture.Bitmap
            self.weightSections.Visible = true
            self.weightSelectAll.Visible = true
            self.weightSelectNone.Visible = true
            # select all 
            self.weightSelectAllClick(self)
            self.weightSectionsClick(self)
        else:
            self.weightSections.Visible = false
            self.weightSelectAll.Visible = false
            self.weightSelectNone.Visible = false
            self.weightShowSections.Glyph = self.downImage.Picture.Bitmap
            self.weightSectionsClick(self)
        self.weightSections.Visible = self.weightSectionsOpen
    
    def mutationSelectAllClick(self, Sender):
        i = 0
        
        if self.mutationSections.Items.Count > 0:
            for i in range(0, self.mutationSections.Items.Count):
                self.mutationSections.Selected[i] = true
    
    def mutationSelectNoneClick(self, Sender):
        i = 0
        
        if self.mutationSections.Items.Count > 0:
            for i in range(0, self.mutationSections.Items.Count):
                self.mutationSections.Selected[i] = false
    
    def weightSelectAllClick(self, Sender):
        i = 0
        
        if self.weightSections.Items.Count > 0:
            for i in range(0, self.weightSections.Items.Count):
                self.weightSections.Selected[i] = true
    
    def weightSelectNoneClick(self, Sender):
        i = 0
        
        if self.weightSections.Items.Count > 0:
            for i in range(0, self.weightSections.Items.Count):
                self.weightSections.Selected[i] = false
    
    def changeTdoLibraryClick(self, Sender):
        fileNameWithPath = ""
        
        fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypeTdo, udomain.domain.defaultTdoLibraryFileName, "Choose a 3D object library (tdo) file")
        if fileNameWithPath == "":
            return
        self.currentTdoLibraryFileName.Text = fileNameWithPath
        udomain.domain.defaultTdoLibraryFileName = self.currentTdoLibraryFileName.Text
        self.currentTdoLibraryFileName.SelStart = len(self.currentTdoLibraryFileName.Text)
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Changing_breeding_options")
    
    def plantsPerGenerationChange(self, Sender):
        oldValue = 0
        
        oldValue = self.options.plantsPerGeneration
        try:
            self.options.plantsPerGeneration = self.plantsPerGeneration.Value
        except:
            self.options.plantsPerGeneration = oldValue
    
    def thumbnailWidthChange(self, Sender):
        oldValue = 0
        
        oldValue = self.options.thumbnailWidth
        try:
            self.options.thumbnailWidth = self.thumbnailWidth.Value
        except:
            self.options.thumbnailWidth = oldValue
    
    def thumbnailHeightChange(self, Sender):
        oldValue = 0
        
        oldValue = self.options.thumbnailHeight
        try:
            self.options.thumbnailHeight = self.thumbnailHeight.Value
        except:
            self.options.thumbnailHeight = oldValue
    
    def maxGenerationsChange(self, Sender):
        oldValue = 0
        
        oldValue = self.options.maxGenerations
        try:
            self.options.maxGenerations = self.maxGenerations.Value
        except:
            self.options.maxGenerations = oldValue
    
    def numTimeSeriesStagesChange(self, Sender):
        oldValue = 0
        
        oldValue = self.options.numTimeSeriesStages
        try:
            self.options.numTimeSeriesStages = self.numTimeSeriesStages.Value
        except:
            self.options.numTimeSeriesStages = oldValue
    
    def percentMaxAgeChange(self, Sender):
        oldValue = 0
        
        oldValue = self.options.percentMaxAge
        try:
            self.options.percentMaxAge = self.percentMaxAge.Value
        except:
            self.options.percentMaxAge = oldValue
    
    def maxPartsPerPlant_thousandsChange(self, Sender):
        oldValue = 0
        
        oldValue = self.domainOptions.maxPartsPerPlant_thousands
        try:
            self.domainOptions.maxPartsPerPlant_thousands = self.maxPartsPerPlant_thousands.Value
        except:
            self.domainOptions.maxPartsPerPlant_thousands = oldValue
    
    def updateTimeSeriesPlantsOnParameterChangeClick(self, Sender):
        self.domainOptions.updateTimeSeriesPlantsOnParameterChange = self.updateTimeSeriesPlantsOnParameterChange.Checked
    
