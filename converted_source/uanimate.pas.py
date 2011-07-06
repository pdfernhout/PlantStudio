# unit uanimate

from conversion_common import *
import usupport
import umath
import updform
import uplant
import udomain
import delphi_compatability

class TAnimationFilesOptionsForm(PdForm):
    def __init__(self):
        self.helpButton = TSpeedButton()
        self.Close = TButton()
        self.cancel = TButton()
        self.Panel1 = TPanel()
        self.fileNumberLabel = TLabel()
        self.animationSizeLabel = TLabel()
        self.fileSizeLabel = TLabel()
        self.Panel2 = TPanel()
        self.Label4 = TLabel()
        self.focusedPlantName = TLabel()
        self.Label5 = TLabel()
        self.GroupBox1 = TGroupBox()
        self.Label1 = TLabel()
        self.resolutionLabel = TLabel()
        self.incrementLabel = TLabel()
        self.plantMaxAgeLabel = TLabel()
        self.colorsLabel = TLabel()
        self.animateByAge = TRadioButton()
        self.animateByXRotation = TRadioButton()
        self.incrementEdit = TSpinEdit()
        self.resolution = TSpinEdit()
        self.colorType = TComboBox()
        self.options = NumberedAnimationOptionsStructure()
        self.plant = PdPlant()
        self.internalChange = false
    
    #$R *.DFM
    def initializeWithOptionsAndPlant(self, anOptions, aPlant):
        self.internalChange = true
        if aPlant == None:
            raise GeneralException.create("Problem: Nil plant in method TAnimationFilesOptionsForm.initializeWithOptionsAndPlant.")
        self.plant = aPlant
        self.options = anOptions
        self.focusedPlantName.Caption = self.plant.getName()
        if self.options.animateBy == udomain.kAnimateByAge:
            self.animateByAge.Checked = true
        elif self.options.animateBy == udomain.kAnimateByXRotation:
            self.animateByXRotation.Checked = true
        self.changeQuestionsBasedOnAnimationType()
        self.resolution.Value = self.options.resolution_pixelsPerInch
        self.colorType.ItemIndex = ord(self.options.colorType)
        self.changeQuestionsBasedOnAnimationType()
        self.calculateNumberOfFrames()
        self.internalChange = false
    
    def changeQuestionsBasedOnAnimationType(self):
        self.internalChange = true
        if self.animateByAge.Checked:
            self.incrementLabel.Caption = "Age increment between &frames (days)"
            self.incrementEdit.Value = self.options.ageIncrement
        else:
            self.incrementLabel.Caption = "Rotation increment between &frames (degrees)"
            self.incrementEdit.Value = self.options.xRotationIncrement
        self.internalChange = false
    
    def animateByAgeClick(self, Sender):
        if self.internalChange:
            return
        if self.animateByAge.Checked:
            self.options.animateBy = udomain.kAnimateByAge
        else:
            self.options.animateBy = udomain.kAnimateByXRotation
        self.changeQuestionsBasedOnAnimationType()
        self.calculateNumberOfFrames()
    
    def animateByXRotationClick(self, Sender):
        if self.internalChange:
            return
        if self.animateByAge.Checked:
            self.options.animateBy = udomain.kAnimateByAge
        else:
            self.options.animateBy = udomain.kAnimateByXRotation
        self.changeQuestionsBasedOnAnimationType()
        self.calculateNumberOfFrames()
    
    def incrementEditChange(self, Sender):
        oldValue = 0
        
        if self.internalChange:
            return
        if self.animateByAge.Checked:
            oldValue = self.options.ageIncrement
        else:
            oldValue = self.options.xRotationIncrement
        try:
            if self.animateByAge.Checked:
                self.options.ageIncrement = self.incrementEdit.Value
            else:
                self.options.xRotationIncrement = self.incrementEdit.Value
        except:
            if self.animateByAge.Checked:
                self.options.ageIncrement = oldValue
            else:
                self.options.xRotationIncrement = oldValue
        self.calculateNumberOfFrames()
    
    def resolutionChange(self, Sender):
        oldValue = 0
        
        if self.internalChange:
            return
        oldValue = self.options.resolution_pixelsPerInch
        try:
            self.options.resolution_pixelsPerInch = self.resolution.Value
        except:
            self.options.resolution_pixelsPerInch = oldValue
        self.calculateNumberOfFrames()
    
    def calculateNumberOfFrames(self):
        scaleMultiplier = 0.0
        
        if self.options.animateBy == udomain.kAnimateByAge:
            self.plantMaxAgeLabel.Caption = "Maximum age = " + IntToStr(self.plant.pGeneral.ageAtMaturity)
            self.plantMaxAgeLabel.Visible = true
            self.options.frameCount = self.plant.pGeneral.ageAtMaturity / self.options.ageIncrement + 1
        elif self.options.animateBy == udomain.kAnimateByXRotation:
            self.plantMaxAgeLabel.Visible = false
            self.options.frameCount = 360 / abs(self.options.xRotationIncrement)
        self.fileNumberLabel.Caption = "Number of files:  " + IntToStr(self.options.frameCount)
        scaleMultiplier = umath.safedivExcept(1.0 * self.options.resolution_pixelsPerInch, 1.0 * delphi_compatability.Screen.PixelsPerInch, 1.0)
        self.options.scaledSize = Point(intround(usupport.rWidth(self.plant.boundsRect_pixels()) * scaleMultiplier), intround(usupport.rHeight(self.plant.boundsRect_pixels()) * scaleMultiplier))
        self.animationSizeLabel.Caption = "Animation size:  " + IntToStr(self.options.scaledSize.X) + " x " + IntToStr(self.options.scaledSize.Y)
        self.options.fileSize = intround(self.options.frameCount * self.options.scaledSize.X * self.options.scaledSize.Y * usupport.bitsPerPixelForColorType(self.options.colorType) / 8.0) + FIX_sizeof(delphi_compatability.TBitmapInfo)
        if self.options.fileSize < 1024:
            self.fileSizeLabel.Caption = "Estimated total size:  " + IntToStr(self.options.fileSize) + " bytes"
        elif self.options.fileSize < 1024 * 1024:
            self.fileSizeLabel.Caption = "Estimated total size:  " + IntToStr(self.options.fileSize / 1024) + " KB"
        else:
            self.fileSizeLabel.Caption = "Estimated total size:  " + FloatToStrF(self.options.fileSize / (1024 * 1024), UNRESOLVED.ffFixed, 7, 1) + " MB"
        if self.options.fileSize >= 10.0 * 1024 * 1024:
            self.fileSizeLabel.Font.Style = [UNRESOLVED.fsBold, ]
        else:
            self.fileSizeLabel.Font.Style = []
    
    def colorTypeChange(self, Sender):
        self.options.colorType = UNRESOLVED.TPixelFormat(self.colorType.ItemIndex)
        self.calculateNumberOfFrames()
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Making_numbered_animation_files")
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
