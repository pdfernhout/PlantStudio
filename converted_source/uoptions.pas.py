# unit Uoptions

from conversion_common import *
import u3dexport
import ucustdrw
import umath
import usupport
import updform
import udomain
import delphi_compatability

# const
kTransferLoad = 1
kTransferSave = 2

class TOptionsForm(PdForm):
    def __init__(self):
        self.Close = TButton()
        self.cancel = TButton()
        self.optionsNotebook = TTabbedNotebook()
        self.drawWithOpenGL = TCheckBox()
        self.wholeProgramBox = TGroupBox()
        self.backgroundColor = TPanel()
        self.backgroundColorLabel = TLabel()
        self.showPlantDrawingProgress = TCheckBox()
        self.GroupBox1 = TGroupBox()
        self.firstSelectionRectangleColorLabel = TLabel()
        self.multiSelectionRectangleColorLabel = TLabel()
        self.firstSelectionRectangleColor = TPanel()
        self.multiSelectionRectangleColor = TPanel()
        self.GroupBox2 = TGroupBox()
        self.rotationIncrementLabel = TLabel()
        self.nudgeDistanceLabel = TLabel()
        self.rotationIncrement = TSpinEdit()
        self.nudgeDistance = TSpinEdit()
        self.GroupBox6 = TGroupBox()
        self.parametersFontSizeLabel = TLabel()
        self.useMetricUnits = TCheckBox()
        self.parametersFontSize = TSpinEdit()
        self.GroupBox7 = TGroupBox()
        self.pauseBeforeHintLabel = TLabel()
        self.pauseDuringHintLabel = TLabel()
        self.openMostRecentFileAtStart = TCheckBox()
        self.pauseBeforeHint = TSpinEdit()
        self.pauseDuringHint = TSpinEdit()
        self.helpButton = TSpeedButton()
        self.resizeKeyUpMultiplierPercent = TSpinEdit()
        self.resizeDistanceLabel = TLabel()
        self.mainWindowDrawingOptionsBox = TGroupBox()
        self.customDrawOptions = TButton()
        self.Label1 = TLabel()
        self.transparentColor = TPanel()
        self.transparentColorLabel = TLabel()
        self.memoryLimitForPlantBitmaps_MB = TSpinEdit()
        self.memoryLimitLabel = TLabel()
        self.Panel1 = TPanel()
        self.Image1 = TImage()
        self.pasteRectSize = TSpinEdit()
        self.pasteRectSizeLabel = TLabel()
        self.GroupBox4 = TGroupBox()
        self.Label9 = TLabel()
        self.Label10 = TLabel()
        self.ghostingColor = TPanel()
        self.nonHiddenPosedColor = TPanel()
        self.selectedPosedColor = TPanel()
        self.Label3 = TLabel()
        self.GroupBox5 = TGroupBox()
        self.undoLimitLabel = TLabel()
        self.undoLimitOfPlantsLabel = TLabel()
        self.undoLimit = TSpinEdit()
        self.undoLimitOfPlants = TSpinEdit()
        self.resizeRectSize = TSpinEdit()
        self.resizeRectSizeLabel = TLabel()
        self.ignoreWindowSettingsInFile = TCheckBox()
        self.transferDirection = 0
        self.options = DomainOptionsStructure()
        self.optionsChanged = false
        self.messageShown = 0
    
    #$R *.DFM
    def FormCreate(self, Sender):
        self.optionsNotebook.pageIndex = 0
    
    def FormActivate(self, Sender):
        self.transferDirection = kTransferLoad
        self.transferFields()
    
    def CloseClick(self, Sender):
        self.transferDirection = kTransferSave
        self.transferFields()
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def transferFields(self):
        # DRAWING
        self.options.memoryLimitForPlantBitmaps_MB = self.transferSmallintSpinEditBox(self.memoryLimitForPlantBitmaps_MB, self.options.memoryLimitForPlantBitmaps_MB)
        self.transferColor(self.backgroundColor, self.options.backgroundColor)
        self.transferColor(self.transparentColor, self.options.transparentColor)
        self.options.showPlantDrawingProgress = self.transferCheckBox(self.showPlantDrawingProgress, self.options.showPlantDrawingProgress)
        # SELECTING
        self.transferColor(self.firstSelectionRectangleColor, self.options.firstSelectionRectangleColor)
        self.transferColor(self.multiSelectionRectangleColor, self.options.multiSelectionRectangleColor)
        self.options.resizeRectSize = self.transferSmallintSpinEditBox(self.resizeRectSize, self.options.resizeRectSize)
        self.transferColor(self.ghostingColor, self.options.ghostingColor)
        self.transferColor(self.nonHiddenPosedColor, self.options.nonHiddenPosedColor)
        self.transferColor(self.selectedPosedColor, self.options.selectedPosedColor)
        # EDITING
        self.options.rotationIncrement = self.transferSmallintSpinEditBox(self.rotationIncrement, self.options.rotationIncrement)
        self.options.nudgeDistance = self.transferSmallintSpinEditBox(self.nudgeDistance, self.options.nudgeDistance)
        self.options.resizeKeyUpMultiplierPercent = self.transferSmallintSpinEditBox(self.resizeKeyUpMultiplierPercent, self.options.resizeKeyUpMultiplierPercent)
        self.options.pasteRectSize = self.transferSmallintSpinEditBox(self.pasteRectSize, self.options.pasteRectSize)
        # UNDOING
        self.options.undoLimit = self.transferSmallintSpinEditBox(self.undoLimit, self.options.undoLimit)
        self.options.undoLimitOfPlants = self.transferSmallintSpinEditBox(self.undoLimitOfPlants, self.options.undoLimitOfPlants)
        # MISCELLANEOUS
        self.options.openMostRecentFileAtStart = self.transferCheckBox(self.openMostRecentFileAtStart, self.options.openMostRecentFileAtStart)
        # v2.1
        self.options.ignoreWindowSettingsInFile = self.transferCheckBox(self.ignoreWindowSettingsInFile, self.options.ignoreWindowSettingsInFile)
        self.options.useMetricUnits = self.transferCheckBox(self.useMetricUnits, self.options.useMetricUnits)
        self.options.parametersFontSize = self.transferSmallintSpinEditBox(self.parametersFontSize, self.options.parametersFontSize)
        self.options.pauseBeforeHint = self.transferSmallintSpinEditBox(self.pauseBeforeHint, self.options.pauseBeforeHint)
        self.options.pauseDuringHint = self.transferSmallintSpinEditBox(self.pauseDuringHint, self.options.pauseDuringHint)
    
    def transferCheckBox(self, checkBox, value):
        if self.transferDirection == kTransferLoad:
            checkBox.Checked = value
        elif self.transferDirection == kTransferSave:
            if value != checkBox.Checked:
                self.optionsChanged = true
            value = checkBox.Checked
        return value
    
    def transferColor(self, colorPanel, value):
        raise "method transferColor had assigned to var parameter value not added to return; fixup manually"
        if self.transferDirection == kTransferLoad:
            colorPanel.Color = value
        elif self.transferDirection == kTransferSave:
            if value != colorPanel.Color:
                self.optionsChanged = true
            value = colorPanel.Color
    
    def transferSmallintSpinEditBox(self, editBox, value):
        if self.transferDirection == kTransferLoad:
            editBox.Text = IntToStr(value)
        elif self.transferDirection == kTransferSave:
            if value != StrToIntDef(editBox.Text, 0):
                self.optionsChanged = true
            value = StrToIntDef(editBox.Text, 0)
        return value
    
    def transferFloatEditBox(self, editBox, value):
        oldValue = 0.0
        newValue = 0.0
        
        if self.transferDirection == kTransferLoad:
            editBox.Text = usupport.digitValueString(value)
        elif self.transferDirection == kTransferSave:
            oldValue = value
            try:
                newValue = StrToFloat(editBox.Text)
            except:
                newValue = oldValue
            if value != newValue:
                self.optionsChanged = true
            value = newValue
        return value
    
    def backgroundColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.backgroundColor.Color = udomain.domain.getColorUsingCustomColors(self.backgroundColor.Color)
    
    def transparentColorMouseUp(self, Sender, Button, Shift, X, Y):
        # leave this enabled even if not using private bitmaps
        self.transparentColor.Color = udomain.domain.getColorUsingCustomColors(self.transparentColor.Color)
    
    def firstSelectionRectangleColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.firstSelectionRectangleColor.Color = udomain.domain.getColorUsingCustomColors(self.firstSelectionRectangleColor.Color)
    
    def multiSelectionRectangleColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.multiSelectionRectangleColor.Color = udomain.domain.getColorUsingCustomColors(self.multiSelectionRectangleColor.Color)
    
    def ghostingColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.ghostingColor.Color = udomain.domain.getColorUsingCustomColors(self.ghostingColor.Color)
    
    def nonHiddenPosedColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.nonHiddenPosedColor.Color = udomain.domain.getColorUsingCustomColors(self.nonHiddenPosedColor.Color)
    
    def selectedPosedColorMouseUp(self, Sender, Button, Shift, X, Y):
        self.selectedPosedColor.Color = udomain.domain.getColorUsingCustomColors(self.selectedPosedColor.Color)
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Changing_preferences")
    
    def customDrawOptionsClick(self, Sender):
        customDrawForm = TCustomDrawOptionsForm()
        response = 0
        
        customDrawForm = ucustdrw.TCustomDrawOptionsForm().create(self)
        if customDrawForm == None:
            raise GeneralException.create("Problem: Could not create 3D object mover window.")
        try:
            customDrawForm.options = self.options
            response = customDrawForm.ShowModal()
            if (response == mrOK) and (customDrawForm.optionsChanged):
                self.options = customDrawForm.options
                self.optionsChanged = true
        finally:
            customDrawForm.free
    
    def Image1Click(self, Sender):
        if self.messageShown == 0:
            ShowMessage("We would like to take this opportunity" + chr(13) + "to say thank you to our excellent testers, " + chr(13) + "especially Ana, Joanne and Randy.")
        elif self.messageShown == 1:
            ShowMessage("Thanks to our parents and families.")
        elif self.messageShown == 2:
            ShowMessage("Thanks to our dogs Maize and Comet" + chr(13) + "for their many interesting suggestions.")
        elif self.messageShown == 3:
            ShowMessage("Thanks to those who have graciously supported our work.")
        elif self.messageShown == 4:
            ShowMessage("Thanks to everyone who sent letters.")
        elif self.messageShown == 5:
            ShowMessage("Thanks to those who have spread the word about PlantStudio.")
        elif self.messageShown == 6:
            ShowMessage("And thank YOU for trying PlantStudio!")
        self.messageShown += 1
    
