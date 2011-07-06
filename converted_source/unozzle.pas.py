# unit unozzle

from conversion_common import *
import umath
import usupport
import umain
import updform
import udomain
import delphi_compatability

class TNozzleOptionsForm(PdForm):
    def __init__(self):
        self.GroupBox1 = TGroupBox()
        self.cellCountLabel = TLabel()
        self.cellSizeLabel = TLabel()
        self.helpButton = TSpeedButton()
        self.Close = TButton()
        self.cancel = TButton()
        self.ColorDialog = TColorDialog()
        self.fileSizeLabel = TLabel()
        self.Panel1 = TPanel()
        self.Label4 = TLabel()
        self.GroupBox2 = TGroupBox()
        self.resolutionLabel = TLabel()
        self.Label3 = TLabel()
        self.colorsLabel = TLabel()
        self.Label1 = TLabel()
        self.backgroundColorPanel = TPanel()
        self.resolutionEdit = TSpinEdit()
        self.colorType = TComboBox()
        self.GroupBox3 = TGroupBox()
        self.useSelectedPlants = TRadioButton()
        self.useVisiblePlants = TRadioButton()
        self.useAllPlants = TRadioButton()
        self.options = NozzleOptionsStructure()
    
    #$R *.DFM
    def initializeWithOptions(self, anOptions):
        self.options = anOptions
        if self.options.exportType == udomain.kIncludeSelectedPlants:
            self.useSelectedPlants.Checked = true
        elif self.options.exportType == udomain.kIncludeVisiblePlants:
            self.useVisiblePlants.Checked = true
        elif self.options.exportType == udomain.kIncludeAllPlants:
            self.useAllPlants.Checked = true
        self.resolutionEdit.Text = IntToStr(intround(self.options.resolution_pixelsPerInch))
        self.backgroundColorPanel.Color = self.options.backgroundColor
        self.colorType.ItemIndex = ord(self.options.colorType)
        self.updateCellSizeAndCountForSelection()
    
    def updateCellSizeAndCountForSelection(self):
        excludeInvisiblePlants = false
        excludeNonSelectedPlants = false
        cellRect = TRect()
        scaleMultiplier = 0.0
        fileSize = 0L
        
        excludeInvisiblePlants = not self.useAllPlants.Checked
        excludeNonSelectedPlants = self.useSelectedPlants.Checked
        cellRect = udomain.domain.plantManager.largestPlantBoundsRect(umain.MainForm.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants)
        scaleMultiplier = umath.safedivExcept(1.0 * self.options.resolution_pixelsPerInch, 1.0 * delphi_compatability.Screen.PixelsPerInch, 1.0)
        self.options.cellSize = Point(intround(usupport.rWidth(cellRect) * scaleMultiplier), intround(usupport.rHeight(cellRect) * scaleMultiplier))
        if self.useAllPlants.Checked:
            self.options.cellCount = udomain.domain.plantManager.plants.Count
        elif self.useVisiblePlants.Checked:
            self.options.cellCount = udomain.domain.plantManager.visiblePlantCount()
        elif self.useSelectedPlants.Checked:
            self.options.cellCount = umain.MainForm.selectedPlants.Count
        self.cellSizeLabel.Caption = "Nozzle/tube cell width:  " + IntToStr(self.options.cellSize.X) + " height:  " + IntToStr(self.options.cellSize.Y)
        self.cellCountLabel.Caption = "Number of items:  " + IntToStr(self.options.cellCount)
        fileSize = intround(self.options.cellCount * self.options.cellSize.X * self.options.cellSize.Y * usupport.bitsPerPixelForColorType(self.options.colorType) / 8.0) + FIX_sizeof(delphi_compatability.TBitmapInfo)
        if fileSize < 1024:
            self.fileSizeLabel.Caption = "Estimated file size:  " + IntToStr(fileSize) + " bytes"
        elif fileSize < 1024 * 1024:
            self.fileSizeLabel.Caption = "Estimated file size:  " + IntToStr(fileSize / 1024) + " KB"
        else:
            self.fileSizeLabel.Caption = "Estimated file size:  " + FloatToStrF(fileSize / (1024 * 1024), UNRESOLVED.ffFixed, 7, 1) + " MB"
        if fileSize >= 10.0 * 1024 * 1024:
            self.fileSizeLabel.Font.Style = [UNRESOLVED.fsBold, ]
        else:
            self.fileSizeLabel.Font.Style = []
    
    def changeSelection(self, Sender):
        if Sender == self.useSelectedPlants:
            self.options.exportType = udomain.kIncludeSelectedPlants
        elif Sender == self.useVisiblePlants:
            self.options.exportType = udomain.kIncludeVisiblePlants
        elif Sender == self.useAllPlants:
            self.options.exportType = udomain.kIncludeAllPlants
        self.updateCellSizeAndCountForSelection()
    
    def backgroundColorPanelClick(self, Sender):
        self.backgroundColorPanel.Color = udomain.domain.getColorUsingCustomColors(self.backgroundColorPanel.Color)
        self.options.backgroundColor = self.backgroundColorPanel.Color
    
    def resolutionEditChange(self, Sender):
        self.options.resolution_pixelsPerInch = StrToIntDef(self.resolutionEdit.Text, intround(self.options.resolution_pixelsPerInch))
        self.updateCellSizeAndCountForSelection()
    
    def colorTypeChange(self, Sender):
        self.options.colorType = UNRESOLVED.TPixelFormat(self.colorType.ItemIndex)
        self.updateCellSizeAndCountForSelection()
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Making_a_nozzle_or_tube")
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
    def CloseClick(self, Sender):
        if (self.options.exportType == udomain.kIncludeSelectedPlants) and (umain.MainForm.selectedPlants.Count <= 0):
            MessageDialog("You chose \"selected\" for \"Draw which plants\", but no plants are selected." + chr(13) + "You should make another choice, or click Cancel and select some plants.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
        else:
            self.ModalResult = mrOK
    
