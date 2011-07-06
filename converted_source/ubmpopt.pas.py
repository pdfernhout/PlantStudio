# unit ubmpopt

from conversion_common import *
import udebug
import uborders
import umain
import umath
import usupport
import updform
import udomain
import delphi_compatability

# const
kCopyingDrawing = 0
kPrintingDrawing = 1
kSavingDrawingToBmp = 2
kSavingDrawingToJpeg = 3

# const
kTransferLoad = 1
kTransferSave = 2
kSpinNone = 0
kSpinUp = 1
kSpinDown = -1
kEditIsInteger = 0
kEditIsFloat = 1
kWidthWasChanged = 0
kHeightWasChanged = 1
kHeightAndWidthWereChanged = 2
kEditBoxHasInteger = 0
kEditBoxHasFloat = 1
kTooManyMegabytesOfMemory = 10.0

#$R *.DFM
def floatStr(value):
    result = ""
    result = FloatToStrF(value, UNRESOLVED.ffFixed, 7, 2)
    return result

class TBitmapOptionsForm(PdForm):
    def __init__(self):
        self.Close = TButton()
        self.cancel = TButton()
        self.printBox = TGroupBox()
        self.outputBox = TGroupBox()
        self.resolutionLabel = TLabel()
        self.sizePixelsLabel = TLabel()
        self.sizeInchesLabel = TLabel()
        self.inchWidthEdit = TEdit()
        self.inchHeightEdit = TEdit()
        self.colorType = TComboBox()
        self.colorsLabel = TLabel()
        self.printSetup = TButton()
        self.printPreserveAspectRatio = TCheckBox()
        self.plantsBox = TGroupBox()
        self.useSelectedPlants = TRadioButton()
        self.useAllPlants = TRadioButton()
        self.useDrawingAreaContents = TRadioButton()
        self.useVisiblePlants = TRadioButton()
        self.resolutionEdit = TEdit()
        self.pixelWidthEdit = TEdit()
        self.pixelHeightEdit = TEdit()
        self.resolutionSpin = TSpinButton()
        self.pixelWidthSpin = TSpinButton()
        self.pixelHeightSpin = TSpinButton()
        self.inchHeightSpin = TSpinButton()
        self.inchWidthSpin = TSpinButton()
        self.PrintDialog = TPrintDialog()
        self.preserveAspectRatio = TCheckBox()
        self.inchHeightLabel = TLabel()
        self.pixelWidthLabel = TLabel()
        self.pixelHeightLabel = TLabel()
        self.borders = TButton()
        self.currentStuffPanel = TPanel()
        self.selectedImageInfoLabel = TLabel()
        self.screenInfoLabel = TLabel()
        self.printerOrFileTypeInfoLabel = TLabel()
        self.sizeLabel = TLabel()
        self.printWidthLabel = TLabel()
        self.printWidthEdit = TEdit()
        self.printWidthSpin = TSpinButton()
        self.printHeightLabel = TLabel()
        self.printHeightEdit = TEdit()
        self.printHeightSpin = TSpinButton()
        self.marginsLabel = TLabel()
        self.printLeftMarginLabel = TLabel()
        self.printTopMarginLabel = TLabel()
        self.printLeftMarginEdit = TEdit()
        self.printTopMarginEdit = TEdit()
        self.printLeftMarginSpin = TSpinButton()
        self.printTopMarginSpin = TSpinButton()
        self.printRightMarginLabel = TLabel()
        self.printBottomMarginLabel = TLabel()
        self.printRightMarginEdit = TEdit()
        self.printBottomMarginEdit = TEdit()
        self.printRightMarginSpin = TSpinButton()
        self.printBottomMarginSpin = TSpinButton()
        self.printCenter = TButton()
        self.printUseWholePage = TButton()
        self.suggestPrintSize = TButton()
        self.printImagePanel = TPanel()
        self.wholePageImage = TImage()
        self.inchWidthLabel = TLabel()
        self.helpButton = TSpeedButton()
        self.memoryUseInfoLabel = TLabel()
        self.jpgCompressionLabel = TLabel()
        self.jpgCompressionEdit = TEdit()
        self.jpgCompressionSpin = TSpinButton()
        self.options = BitmapOptionsStructure()
        self.transferDirection = 0
        self.optionsChanged = false
        self.copySavePrintType = 0
        self.startingUp = false
        self.sideEffect = false
        self.selectionRectFromMainWindow = TRect()
        self.printPageWidth_in = 0.0
        self.printPageHeight_in = 0.0
        self.wholePageWidth_in = 0.0
        self.wholePageHeight_in = 0.0
        self.printMinMarginLeft_in = 0.0
        self.printMinMarginTop_in = 0.0
        self.printMinMarginRight_in = 0.0
        self.printMinMarginBottom_in = 0.0
        self.pictureWidth_px = 0.0
        self.pictureHeight_px = 0.0
        self.pictureResolution_pxPin = 0.0
        self.smallestPrintResolution_pxPin = 0.0
        self.pictureWidth_in = 0.0
        self.pictureHeight_in = 0.0
        self.printWidth_in = 0.0
        self.printHeight_in = 0.0
        self.printLeftMargin_in = 0.0
        self.printTopMargin_in = 0.0
        self.printRightMargin_in = 0.0
        self.printBottomMargin_in = 0.0
        self.jpegCompression = 0.0
        self.aspectRatio = 0.0
        self.megabytesOfMemoryNeeded = 0.0
    
    # ----------------------------------------------------------------------------------------- initialize 
    def initializeWithTypeAndOptions(self, aType, anOptions):
        displayString = ""
        
        self.startingUp = true
        self.options = anOptions
        self.copySavePrintType = aType
        displayString = self.nameForCopySavePrintType(self.copySavePrintType)
        if self.copySavePrintType == kPrintingDrawing:
            # must be done before transfer
            self.updateForPrinterInfo()
        self.transferDirection = kTransferLoad
        self.transferFields()
        self.updateForImageSelection()
        self.maintainAspectRatioPixelsAndInches(self.pixelWidthEdit)
        self.updateBorderThickness()
        self.printSetup.Visible = self.copySavePrintType == kPrintingDrawing
        self.borders.Visible = self.copySavePrintType == kPrintingDrawing
        self.printerOrFileTypeInfoLabel.Visible = self.copySavePrintType != kCopyingDrawing
        if self.copySavePrintType == kSavingDrawingToJpeg:
            self.jpgCompressionLabel.Visible = true
            self.colorsLabel.Visible = false
            self.jpgCompressionLabel.SetBounds(self.colorsLabel.Left, self.colorsLabel.Top, self.jpgCompressionLabel.Width, self.jpgCompressionLabel.Height)
            self.jpgCompressionEdit.Visible = true
            self.colorType.Visible = false
            self.jpgCompressionEdit.SetBounds(self.colorType.Left, self.colorType.Top, self.jpgCompressionEdit.Width, self.jpgCompressionEdit.Height)
            self.jpgCompressionSpin.Visible = true
            self.jpgCompressionSpin.SetBounds(self.jpgCompressionEdit.Left + self.jpgCompressionEdit.Width + 4, self.jpgCompressionEdit.Top, self.jpgCompressionSpin.Width, self.jpgCompressionSpin.Height)
        if (self.copySavePrintType == kSavingDrawingToBmp) or (self.copySavePrintType == kSavingDrawingToJpeg):
            if (self.copySavePrintType == kSavingDrawingToBmp):
                self.printerOrFileTypeInfoLabel.Caption = "Saving to: BMP"
            elif (self.copySavePrintType == kSavingDrawingToJpeg):
                self.printerOrFileTypeInfoLabel.Caption = "Saving to: JPEG"
        if self.copySavePrintType == kPrintingDrawing:
            self.ClientHeight = self.printBox.Top + self.printBox.Height
            self.suggestPrintSizeClick(self)
        else:
            self.ClientHeight = self.outputBox.Top + self.outputBox.Height
        if self.copySavePrintType == kCopyingDrawing:
            self.Close.Caption = "&Copy"
        elif self.copySavePrintType == kPrintingDrawing:
            self.Close.Caption = "&Print"
        elif self.copySavePrintType == kSavingDrawingToBmp:
            self.Close.Caption = "&Save"
        elif self.copySavePrintType == kSavingDrawingToJpeg:
            self.Close.Caption = "&Save"
        self.helpButton.Hint = "Get help with setting " + lowercase(displayString) + " picture options."
        self.cancel.Hint = "Close this window and don't " + lowercase(displayString) + " a picture."
        self.Close.Hint = displayString + " the selected picture using the options specified in this window."
        self.startingUp = false
    
    def updateForPrinterInfo(self):
        xResolution_pixelsPerInch = 0
        yResolution_pixelsPerInch = 0
        portraitOrLandscape = ""
        printerDC = HDC()
        printerColorBits = 0
        printerColors = 0
        
        xResolution_pixelsPerInch = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSX)
        yResolution_pixelsPerInch = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSY)
        self.smallestPrintResolution_pxPin = umath.intMin(xResolution_pixelsPerInch, yResolution_pixelsPerInch)
        self.printPageWidth_in = umath.safedivExcept(UNRESOLVED.Printer.pageWidth - 1, xResolution_pixelsPerInch, 0)
        self.printPageHeight_in = umath.safedivExcept(UNRESOLVED.Printer.pageHeight - 1, yResolution_pixelsPerInch, 0)
        self.wholePageWidth_in = umath.safedivExcept(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PHYSICALWIDTH), xResolution_pixelsPerInch, 0)
        self.wholePageHeight_in = umath.safedivExcept(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PHYSICALHEIGHT), xResolution_pixelsPerInch, 0)
        self.printMinMarginLeft_in = umath.safedivExcept(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PhysicalOffsetX), xResolution_pixelsPerInch, 0)
        self.printMinMarginTop_in = umath.safedivExcept(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PhysicalOffsetY), xResolution_pixelsPerInch, 0)
        self.printMinMarginRight_in = self.wholePageWidth_in - self.printPageWidth_in - self.printMinMarginLeft_in
        self.printMinMarginBottom_in = self.wholePageHeight_in - self.printPageHeight_in - self.printMinMarginTop_in
        if UNRESOLVED.Printer.orientation == UNRESOLVED.poPortrait:
            portraitOrLandscape = "Portrait"
        else:
            portraitOrLandscape = "Landscape"
        printerDC = UNRESOLVED.CreateCompatibleDC(UNRESOLVED.Printer.Handle)
        try:
            printerColorBits = (UNRESOLVED.GetDeviceCaps(printerDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(printerDC, delphi_compatability.PLANES))
        finally:
            UNRESOLVED.ReleaseDC(0, printerDC)
            UNRESOLVED.DeleteDC(printerDC)
        if printerColorBits != 32:
            printerColors = 1 << printerColorBits
        else:
            printerColors = intround(umath.power(2.0, printerColorBits))
        self.printerOrFileTypeInfoLabel.Caption = "Printer:  " + IntToStr(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSX)) + " x " + IntToStr(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSY)) + " pixels/inch, " + IntToStr(printerColors) + " colors (" + IntToStr(printerColorBits) + " bits)"
        #+ portraitOrLandscape;
        #printerInfoLabel.hint := 'Printer name: ' + Printer.Printers[Printer.printerIndex];
        self.updatePrintPreview()
    
    def updateForImageSelection(self):
        pixelWidth = 0
        pixelHeight = 0
        screenColorBits = 0
        screenColors = 0L
        inchWidth = 0.0
        inchHeight = 0.0
        screenDC = HDC()
        megabytesNeeded = 0.0
        
        self.updateSelectionRectFromMainWindow()
        # fill in labels
        pixelWidth = usupport.rWidth(self.selectionRectFromMainWindow)
        pixelHeight = usupport.rHeight(self.selectionRectFromMainWindow)
        inchWidth = umath.safedivExcept(pixelWidth, delphi_compatability.Screen.PixelsPerInch, 0)
        inchHeight = umath.safedivExcept(pixelHeight, delphi_compatability.Screen.PixelsPerInch, 0)
        self.selectedImageInfoLabel.Caption = "Selection:  " + IntToStr(pixelWidth) + " x " + IntToStr(pixelHeight) + " pixels,  " + floatStr(inchWidth) + " x " + floatStr(inchHeight) + " inches"
        screenDC = UNRESOLVED.GetDC(0)
        try:
            screenColorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES))
        finally:
            UNRESOLVED.ReleaseDC(0, screenDC)
        if screenColorBits != 32:
            screenColors = 1 << screenColorBits
            self.screenInfoLabel.Caption = "Screen:  " + IntToStr(delphi_compatability.Screen.PixelsPerInch) + " pixels/inch,  " + IntToStr(screenColors) + " colors (" + IntToStr(screenColorBits) + " bits)"
        else:
            self.screenInfoLabel.Caption = "Screen:  " + IntToStr(delphi_compatability.Screen.PixelsPerInch) + " pixels/inch,  " + "true color (" + IntToStr(screenColorBits) + " bits)"
        # used to be only in suggest size button, now doing automatically
        self.setValue(self.inchWidthEdit, inchWidth)
        self.setValue(self.inchHeightEdit, inchHeight)
        self.calculatePixelsFromResolutionAndInches()
        if self.copySavePrintType == kPrintingDrawing:
            self.suggestPrintSizeClick(self)
            self.updatePrintPreview()
        self.reportOnMemoryNeeded()
    
    def reportOnMemoryNeeded(self):
        if self.copySavePrintType == kSavingDrawingToJpeg:
            # report memory needed -- do after calculating resolution-affected size
            # make no size estimation for JPG
            self.memoryUseInfoLabel.Visible = false
            return
        self.calculatePixelsFromResolutionAndInches()
        self.calculateMegabytesOfMemoryNeededConsideringColorBitsAndResolution()
        if self.megabytesOfMemoryNeeded < 1.0:
            self.memoryUseInfoLabel.Caption = "Estimated memory needed: " + usupport.digitValueString(self.megabytesOfMemoryNeeded * 1024) + " K"
        else:
            self.memoryUseInfoLabel.Caption = "Estimated memory needed: " + usupport.digitValueString(self.megabytesOfMemoryNeeded) + " MB"
        if self.megabytesOfMemoryNeeded > kTooManyMegabytesOfMemory:
            self.memoryUseInfoLabel.Font.Style = [UNRESOLVED.fsBold, ]
        else:
            self.memoryUseInfoLabel.Font.Style = []
    
    def calculateMegabytesOfMemoryNeededConsideringColorBitsAndResolution(self):
        colorBits = 0
        screenDC = HDC()
        outputPixelWidth = 0.0
        outputPixelHeight = 0.0
        
        outputPixelWidth = self.pictureWidth_in * self.pictureResolution_pxPin
        outputPixelHeight = self.pictureHeight_in * self.pictureResolution_pxPin
        colorBits = 0
        if self.colorType.ItemIndex == delphi_compatability.TPixelFormat.pfDevice:
            screenDC = UNRESOLVED.GetDC(0)
            try:
                colorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES))
            finally:
                UNRESOLVED.ReleaseDC(0, screenDC)
        elif self.colorType.ItemIndex == delphi_compatability.TPixelFormat.pf1bit:
            colorBits = 1
        elif self.colorType.ItemIndex == delphi_compatability.TPixelFormat.pf4bit:
            colorBits = 4
        elif self.colorType.ItemIndex == delphi_compatability.TPixelFormat.pf8bit:
            colorBits = 8
        elif self.colorType.ItemIndex == delphi_compatability.TPixelFormat.pf15bit:
            colorBits = 15
        elif self.colorType.ItemIndex == delphi_compatability.TPixelFormat.pf16bit:
            colorBits = 16
        elif self.colorType.ItemIndex == delphi_compatability.TPixelFormat.pf24bit:
            colorBits = 24
        elif self.colorType.ItemIndex == delphi_compatability.TPixelFormat.pf32bit:
            colorBits = 32
        self.megabytesOfMemoryNeeded = (1.0 * outputPixelWidth * outputPixelHeight * (colorBits / 8) + FIX_sizeof(delphi_compatability.TBitmapInfo)) / (1024 * 1024)
    
    def updateSelectionRectFromMainWindow(self):
        excludeInvisiblePlants = false
        excludeNonSelectedPlants = false
        
        excludeInvisiblePlants = not self.useAllPlants.Checked
        excludeNonSelectedPlants = self.useSelectedPlants.Checked
        if self.useDrawingAreaContents.Checked:
            self.selectionRectFromMainWindow = Rect(0, 0, umain.MainForm.drawingPaintBox.Width, umain.MainForm.drawingPaintBox.Height)
        else:
            self.selectionRectFromMainWindow = udomain.domain.plantManager.combinedPlantBoundsRects(umain.MainForm.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants)
        self.aspectRatio = umath.safedivExcept(usupport.rWidth(self.selectionRectFromMainWindow), usupport.rHeight(self.selectionRectFromMainWindow), 1.0)
    
    def updatePrintPreview(self):
        scaleX_pxPin = 0.0
        scaleY_pxPin = 0.0
        scale_pxPin = 0.0
        borderThickness_in = 0.0
        availableWidth_px = 0
        availableHeight_px = 0
        marginRect = TRect()
        
        availableWidth_px = self.sizeLabel.Left - self.wholePageImage.Left - 10
        availableHeight_px = self.printBox.Height - self.wholePageImage.Top - 10
        scaleX_pxPin = umath.safedivExcept(1.0 * availableWidth_px, self.wholePageWidth_in, 5)
        scaleY_pxPin = umath.safedivExcept(1.0 * availableHeight_px, self.wholePageHeight_in, 5)
        scale_pxPin = umath.min(scaleX_pxPin, scaleY_pxPin)
        self.wholePageImage.Width = intround(self.wholePageWidth_in * scale_pxPin)
        self.wholePageImage.Height = intround(self.wholePageHeight_in * scale_pxPin)
        if (self.wholePageImage.Picture.Bitmap.Width != self.wholePageImage.Width) or (self.wholePageImage.Picture.Bitmap.Height != self.wholePageImage.Height):
            try:
                self.wholePageImage.Picture.Bitmap.Width = self.wholePageImage.Width
                self.wholePageImage.Picture.Bitmap.Height = self.wholePageImage.Height
            except:
                self.wholePageImage.Picture.Bitmap.Width = 1
                self.wholePageImage.Picture.Bitmap.Height = 1
        marginRect.Left = intround(self.printMinMarginLeft_in * scale_pxPin)
        marginRect.Top = intround(self.printMinMarginTop_in * scale_pxPin)
        # subtract 1 from right and bottom because last pixel is not drawn
        marginRect.Right = self.wholePageImage.Width - intround(self.printMinMarginRight_in * scale_pxPin) - 1
        marginRect.Bottom = self.wholePageImage.Height - intround(self.printMinMarginBottom_in * scale_pxPin) - 1
        self.wholePageImage.Picture.Bitmap.Canvas.Brush.Color = delphi_compatability.clWindow
        self.wholePageImage.Picture.Bitmap.Canvas.FillRect(Rect(0, 0, self.wholePageImage.Width, self.wholePageImage.Height))
        self.wholePageImage.Picture.Bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.wholePageImage.Picture.Bitmap.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
        self.wholePageImage.Picture.Bitmap.Canvas.MoveTo(0, marginRect.Top)
        self.wholePageImage.Picture.Bitmap.Canvas.LineTo(self.wholePageImage.Width, marginRect.Top)
        self.wholePageImage.Picture.Bitmap.Canvas.MoveTo(marginRect.Left, 0)
        self.wholePageImage.Picture.Bitmap.Canvas.LineTo(marginRect.Left, self.wholePageImage.Height)
        self.wholePageImage.Picture.Bitmap.Canvas.MoveTo(marginRect.Right, 0)
        self.wholePageImage.Picture.Bitmap.Canvas.LineTo(marginRect.Right, self.wholePageImage.Height)
        self.wholePageImage.Picture.Bitmap.Canvas.MoveTo(0, marginRect.Bottom)
        self.wholePageImage.Picture.Bitmap.Canvas.LineTo(self.wholePageImage.Width, marginRect.Bottom)
        self.wholePageImage.Picture.Bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        self.wholePageImage.Picture.Bitmap.Canvas.Rectangle(0, 0, self.wholePageImage.Width, self.wholePageImage.Height)
        borderThickness_in = umath.safedivExcept(self.options.borderThickness, self.smallestPrintResolution_pxPin, 0)
        self.printImagePanel.SetBounds(intround(self.wholePageImage.Left + (self.printLeftMargin_in - borderThickness_in) * scale_pxPin), intround(self.wholePageImage.Top + (self.printTopMargin_in - borderThickness_in) * scale_pxPin), intround((self.printWidth_in + borderThickness_in * 2) * scale_pxPin), intround((self.printHeight_in + borderThickness_in * 2) * scale_pxPin))
    
    def updateBorderThickness(self):
        self.options.borderThickness = 0
        self.options.borderGap = 0
        if self.options.printBorderInner:
            # cfk the 2.5 is arbitrary
            self.options.borderGap = intround(self.options.printBorderWidthInner * 2.5)
            self.options.borderThickness += self.options.printBorderWidthInner + self.options.borderGap
        if self.options.printBorderOuter:
            self.options.borderThickness += self.options.printBorderWidthOuter
    
    # ----------------------------------------------------------------------------------------- transfer 
    def transferFields(self):
        if self.transferDirection == kTransferLoad:
            if self.options.exportType == udomain.kIncludeSelectedPlants:
                # plantBox
                self.useSelectedPlants.Checked = true
            elif self.options.exportType == udomain.kIncludeVisiblePlants:
                self.useVisiblePlants.Checked = true
            elif self.options.exportType == udomain.kIncludeAllPlants:
                self.useAllPlants.Checked = true
            elif self.options.exportType == udomain.kIncludeDrawingAreaContents:
                self.useDrawingAreaContents.Checked = true
        elif self.transferDirection == kTransferSave:
            self.options.exportType = self.currentExportOption()
        if self.copySavePrintType != kSavingDrawingToJpeg:
            # output
            self.transferTPixelFormatComboBox(self.colorType, self.options.colorType)
        self.options.resolution_pixelsPerInch = self.transferSmallintEditBox(self.resolutionEdit, self.options.resolution_pixelsPerInch)
        self.options.width_pixels = self.transferSmallintEditBox(self.pixelWidthEdit, self.options.width_pixels)
        self.options.height_pixels = self.transferSmallintEditBox(self.pixelHeightEdit, self.options.height_pixels)
        self.options.width_in = self.transferSingleEditBox(self.inchWidthEdit, self.options.width_in)
        self.options.height_in = self.transferSingleEditBox(self.inchHeightEdit, self.options.height_in)
        self.options.preserveAspectRatio = self.transferCheckBox(self.preserveAspectRatio, self.options.preserveAspectRatio)
        if self.copySavePrintType == kSavingDrawingToJpeg:
            self.options.jpegCompressionRatio = self.transferSmallintEditBox(self.jpgCompressionEdit, self.options.jpegCompressionRatio)
        if self.copySavePrintType != kPrintingDrawing:
            # printing
            return
        self.options.printPreserveAspectRatio = self.transferCheckBox(self.printPreserveAspectRatio, self.options.printPreserveAspectRatio)
        self.options.printWidth_in = self.transferSingleEditBox(self.printWidthEdit, self.options.printWidth_in)
        self.options.printHeight_in = self.transferSingleEditBox(self.printHeightEdit, self.options.printHeight_in)
        self.options.printLeftMargin_in = self.transferSingleEditBox(self.printLeftMarginEdit, self.options.printLeftMargin_in)
        self.options.printTopMargin_in = self.transferSingleEditBox(self.printTopMarginEdit, self.options.printTopMargin_in)
        self.options.printRightMargin_in = self.transferSingleEditBox(self.printRightMarginEdit, self.options.printRightMargin_in)
        self.options.printBottomMargin_in = self.transferSingleEditBox(self.printBottomMarginEdit, self.options.printBottomMargin_in)
    
    # ----------------------------------------------------------------------------------------- interactions-first panel 
    def selectionChoiceClick(self, sender):
        if self.startingUp or self.sideEffect:
            return
        self.updateForImageSelection()
    
    def preserveAspectRatioClick(self, Sender):
        if self.startingUp or self.sideEffect:
            return
        if self.preserveAspectRatio.Checked:
            # arbitrarily picked pixelWidthEdit here
            self.maintainAspectRatioPixelsAndInches(self.pixelWidthEdit)
    
    def colorTypeChange(self, Sender):
        if self.startingUp or self.sideEffect:
            return
        self.updateForImageSelection()
    
    # ----------------------------------------------------------------------------------------- interactions-second panel 
    def exitEditBox(self, sender):
        self.adjustValue(sender, kSpinNone)
    
    def spinUp(self, sender):
        self.adjustValue(sender, kSpinUp)
    
    def spinDown(self, sender):
        self.adjustValue(sender, kSpinDown)
    
    def adjustValue(self, sender, spin):
        editBox = TEdit()
        
        if self.startingUp or self.sideEffect:
            return
        editBox = None
        if (sender.__class__ is delphi_compatability.TSpinButton):
            # if spin button clicked, adjust corresponding edit (focusControl)
            self.adjustEditBoxValueForSpin(sender, spin)
        if (sender.__class__ is delphi_compatability.TEdit):
            # get edit box
            editBox = sender as delphi_compatability.TEdit
        elif (sender.__class__ is delphi_compatability.TSpinButton):
            editBox = (sender as delphi_compatability.TSpinButton).focusControl as delphi_compatability.TEdit
        if editBox == None:
            return
        # use set method to check edit box entry against bounds
        self.setValue(editBox, self.getEnteredValue(editBox))
        if self.preserveAspectRatio.Checked:
            if (editBox == self.inchWidthEdit) or (editBox == self.inchHeightEdit) or (editBox == self.pixelWidthEdit) or (editBox == self.pixelHeightEdit):
                # if image width/height changed, maintain aspect ratio
                self.maintainAspectRatioPixelsAndInches(editBox)
        if self.printPreserveAspectRatio.Checked:
            if (editBox == self.printWidthEdit) or (editBox == self.printHeightEdit):
                if editBox == self.printWidthEdit:
                    # if print width/height changed, maintain printing aspect ratio
                    self.resizePrintBasedOnAspectRatio(kWidthWasChanged)
                else:
                    self.resizePrintBasedOnAspectRatio(kHeightWasChanged)
        if (editBox == self.inchWidthEdit) or (editBox == self.inchHeightEdit) or (editBox == self.resolutionEdit):
            # interaction between image inches, pixels, resolution
            self.reportOnMemoryNeeded()
        elif (editBox == self.pixelWidthEdit) or (editBox == self.pixelHeightEdit):
            # interaction between print size and margins
            self.reportOnMemoryNeeded()
        elif (editBox == self.printWidthEdit) or (editBox == self.printHeightEdit):
            self.changePrintMarginsToFitPrintSize()
        elif (editBox == self.printLeftMarginEdit) or (editBox == self.printTopMarginEdit) or (editBox == self.printRightMarginEdit) or (editBox == self.printBottomMarginEdit):
            self.changePrintSizeToFitPrintMargins(editBox)
    
    def adjustEditBoxValueForSpin(self, sender, spin):
        editBox = TEdit()
        newValue = 0.0
        
        if (sender == None) or (not (sender.__class__ is delphi_compatability.TSpinButton)):
            return
        editBox = None
        editBox = (sender as delphi_compatability.TSpinButton).focusControl as delphi_compatability.TEdit
        if editBox == None:
            return
        # edit tag is 1 if float
        # spin tag is spin increment * 100 (10 for floats (0.1), 1000 for ints (10))
        newValue = 0
        if (sender as delphi_compatability.TSpinButton).focusControl.tag == kEditIsFloat:
            newValue = self.getValue(editBox) + 1.0 * (sender as delphi_compatability.TSpinButton).Tag / 100 * spin
        else:
            newValue = self.getValue(editBox) + (sender as delphi_compatability.TSpinButton).Tag / 100 * spin
        self.setValue(editBox, newValue)
    
    def maintainAspectRatioPixelsAndInches(self, editBox):
        if (editBox == self.inchWidthEdit):
            self.setValue(self.inchHeightEdit, self.heightForWidthAndAspectRatio(self.pictureWidth_in, self.aspectRatio))
        elif (editBox == self.inchHeightEdit):
            self.setValue(self.inchWidthEdit, self.widthForHeightAndAspectRatio(self.pictureHeight_in, self.aspectRatio))
        elif (editBox == self.pixelWidthEdit):
            self.setValue(self.pixelHeightEdit, self.heightForWidthAndAspectRatio(self.pictureWidth_px, self.aspectRatio))
        elif (editBox == self.pixelHeightEdit):
            self.setValue(self.pixelWidthEdit, self.widthForHeightAndAspectRatio(self.pictureHeight_px, self.aspectRatio))
    
    def heightForWidthAndAspectRatio(self, width, ratio):
        result = 0.0
        result = umath.safedivExcept(width, ratio, 0)
        return result
    
    def widthForHeightAndAspectRatio(self, height, ratio):
        result = 0.0
        result = height * ratio
        return result
    
    def calculatePixelsFromResolutionAndInches(self):
        self.setValue(self.pixelWidthEdit, self.pictureWidth_in * self.pictureResolution_pxPin)
        self.setValue(self.pixelHeightEdit, self.pictureHeight_in * self.pictureResolution_pxPin)
    
    def calculateInchesFromResolutionAndPixels(self):
        self.setValue(self.inchWidthEdit, umath.safedivExcept(1.0 * self.pictureWidth_px, 1.0 * self.pictureResolution_pxPin, 0))
        self.setValue(self.inchHeightEdit, umath.safedivExcept(1.0 * self.pictureHeight_px, 1.0 * self.pictureResolution_pxPin, 0))
    
    def calculateResolutionFromInchesAndPixels(self):
        xRes = 0.0
        yRes = 0.0
        
        xRes = umath.safedivExcept(self.pictureWidth_px, self.pictureWidth_in, delphi_compatability.Screen.PixelsPerInch)
        yRes = umath.safedivExcept(self.pictureHeight_px, self.pictureHeight_in, delphi_compatability.Screen.PixelsPerInch)
        self.setValue(self.resolutionEdit, intround(umath.min(xRes, yRes)))
        self.calculatePixelsFromResolutionAndInches()
    
    def suggestCopySizeClick(self, Sender):
        self.updateSelectionRectFromMainWindow()
        self.setValue(self.pixelWidthEdit, usupport.rWidth(self.selectionRectFromMainWindow))
        self.setValue(self.pixelHeightEdit, usupport.rHeight(self.selectionRectFromMainWindow))
        self.calculateInchesFromResolutionAndPixels()
    
    # -------------------------------------------------------------------- calculations of print size/margins 
    def changePrintMarginsToFitPrintSize(self):
        self.setValue(self.printRightMarginEdit, umath.max(0, self.wholePageWidth_in - self.printLeftMargin_in - self.printWidth_in))
        self.setValue(self.printBottomMarginEdit, umath.max(0, self.wholePageHeight_in - self.printTopMargin_in - self.printHeight_in))
        if self.printPreserveAspectRatio.Checked:
            self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
        else:
            self.updatePrintPreview()
    
    def changePrintSizeToFitPrintMargins(self, editBox):
        if editBox == self.printLeftMarginEdit:
            # keep print size same to start, just offset other margin
            self.setValue(self.printRightMarginEdit, umath.max(0, self.wholePageWidth_in - self.printLeftMargin_in - self.printWidth_in))
        elif editBox == self.printRightMarginEdit:
            self.setValue(self.printLeftMarginEdit, umath.max(0, self.wholePageWidth_in - self.printRightMargin_in - self.printWidth_in))
        elif editBox == self.printTopMarginEdit:
            self.setValue(self.printBottomMarginEdit, umath.max(0, self.wholePageHeight_in - self.printTopMargin_in - self.printHeight_in))
        elif editBox == self.printBottomMarginEdit:
            self.setValue(self.printTopMarginEdit, umath.max(0, self.wholePageHeight_in - self.printBottomMargin_in - self.printHeight_in))
        # now set print size
        self.setValue(self.printWidthEdit, umath.max(0, self.wholePageWidth_in - self.printRightMargin_in - self.printLeftMargin_in))
        self.setValue(self.printHeightEdit, umath.max(0, self.wholePageHeight_in - self.printBottomMargin_in - self.printTopMargin_in))
        if self.printPreserveAspectRatio.Checked:
            # now check aspect ratio
            self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
        else:
            self.updatePrintPreview()
    
    def resizePrintBasedOnAspectRatio(self, whatWasChanged):
        newWidth_in = 0.0
        newHeight_in = 0.0
        newRight_in = 0.0
        newBottom_in = 0.0
        maxWidth_in = 0.0
        maxHeight_in = 0.0
        
        newWidth_in = self.printWidth_in
        newHeight_in = self.printHeight_in
        self.updateSelectionRectFromMainWindow()
        if whatWasChanged == kHeightWasChanged:
            newWidth_in = newHeight_in * self.aspectRatio
        elif whatWasChanged == kWidthWasChanged:
            newHeight_in = umath.safedivExcept(newWidth_in, self.aspectRatio, newHeight_in)
        elif whatWasChanged == kHeightAndWidthWereChanged:
            if newWidth_in > newHeight_in:
                newWidth_in = newHeight_in * self.aspectRatio
            else:
                newHeight_in = umath.safedivExcept(newWidth_in, self.aspectRatio, newHeight_in)
        # bound size at page, using left/top margins already set
        maxWidth_in = self.wholePageWidth_in - self.printLeftMargin_in - self.printMinMarginRight_in
        maxHeight_in = self.wholePageHeight_in - self.printTopMargin_in - self.printMinMarginBottom_in
        if newWidth_in > maxWidth_in:
            newWidth_in = maxWidth_in
            newHeight_in = umath.safedivExcept(newWidth_in, self.aspectRatio, newHeight_in)
        if newHeight_in > maxHeight_in:
            newHeight_in = maxHeight_in
            newWidth_in = newHeight_in * self.aspectRatio
        newRight_in = umath.max(self.printMinMarginRight_in, self.wholePageWidth_in - self.printLeftMargin_in - newWidth_in)
        newBottom_in = umath.max(self.printMinMarginBottom_in, self.wholePageHeight_in - self.printTopMargin_in - newHeight_in)
        # set values in edits
        self.setValue(self.printWidthEdit, newWidth_in)
        self.setValue(self.printHeightEdit, newHeight_in)
        self.setValue(self.printRightMarginEdit, newRight_in)
        self.setValue(self.printBottomMarginEdit, newBottom_in)
        self.updatePrintPreview()
    
    # -------------------------------------------------------------------- interactions - printing panel 
    def printCenterClick(self, Sender):
        self.setValue(self.printLeftMarginEdit, umath.max(self.printMinMarginLeft_in, self.wholePageWidth_in / 2.0 - self.printWidth_in / 2.0))
        self.setValue(self.printRightMarginEdit, umath.max(self.printMinMarginRight_in, self.wholePageWidth_in / 2.0 - self.printWidth_in / 2.0))
        self.setValue(self.printTopMarginEdit, umath.max(self.printMinMarginTop_in, self.wholePageHeight_in / 2.0 - self.printHeight_in / 2.0))
        self.setValue(self.printBottomMarginEdit, umath.max(self.printMinMarginBottom_in, self.wholePageHeight_in / 2.0 - self.printHeight_in / 2.0))
        if self.printPreserveAspectRatio.Checked:
            self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
        else:
            self.updatePrintPreview()
    
    def suggestPrintSizeClick(self, Sender):
        bestMargin_in = 0.0
        bestWidth_in = 0.0
        bestHeight_in = 0.0
        newWidth_in = 0.0
        newHeight_in = 0.0
        maxMinMargin_in = 0.0
        
        # calculate best margin: for 10 inches, 1.0 inches, for 5 inches, 0.5 inches;
        # keep to multiples of 0.25 inches
        maxMinMargin_in = umath.max(self.printMinMarginLeft_in, umath.max(self.printMinMarginTop_in, umath.max(self.printMinMarginRight_in, self.printMinMarginBottom_in)))
        bestMargin_in = umath.max(maxMinMargin_in, intround(4.0 * umath.min(self.wholePageWidth_in, self.wholePageHeight_in) / 10.0) / 4.0)
        bestWidth_in = self.wholePageWidth_in - bestMargin_in * 2
        bestHeight_in = self.wholePageHeight_in - bestMargin_in * 2
        # preserve aspect ratio - reduce the larger dimension so it still fits on the page
        self.updateSelectionRectFromMainWindow()
        newHeight_in = bestHeight_in
        newWidth_in = bestHeight_in * self.aspectRatio
        if newWidth_in > bestWidth_in:
            newWidth_in = bestWidth_in
            newHeight_in = umath.safedivExcept(bestWidth_in, self.aspectRatio, bestHeight_in)
        # set original picture size to fit on page using printer resolution
        self.setValue(self.inchWidthEdit, newWidth_in)
        self.setValue(self.inchHeightEdit, newHeight_in)
        self.setValue(self.resolutionEdit, self.smallestPrintResolution_pxPin)
        self.calculatePixelsFromResolutionAndInches()
        # set print size same as picture size
        self.setValue(self.printWidthEdit, newWidth_in)
        self.setValue(self.printHeightEdit, newHeight_in)
        # center picture
        self.printCenterClick(self)
    
    def printUseWholePageClick(self, Sender):
        borderThickness_in = 0.0
        
        borderThickness_in = umath.safedivExcept(self.options.borderThickness, self.smallestPrintResolution_pxPin, 0)
        self.setValue(self.printLeftMarginEdit, self.printMinMarginLeft_in + borderThickness_in)
        self.setValue(self.printRightMarginEdit, self.printMinMarginRight_in + borderThickness_in)
        self.setValue(self.printTopMarginEdit, self.printMinMarginTop_in + borderThickness_in)
        self.setValue(self.printBottomMarginEdit, self.printMinMarginBottom_in + borderThickness_in)
        self.setValue(self.printWidthEdit, self.wholePageWidth_in - self.printLeftMargin_in - self.printRightMargin_in)
        self.setValue(self.printHeightEdit, self.wholePageHeight_in - self.printTopMargin_in - self.printBottomMargin_in)
        if self.printPreserveAspectRatio.Checked:
            # check new size for aspect ratio (if 'preserve aspect ratio' checked)
            self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
        else:
            self.updatePrintPreview()
    
    def printPreserveAspectRatioClick(self, Sender):
        if self.startingUp or self.sideEffect:
            return
        if self.printPreserveAspectRatio.Checked:
            self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
    
    # ----------------------------------------------------------------------------------------- buttons 
    def bordersClick(self, Sender):
        bordersForm = TPrintBordersForm()
        
        bordersForm = uborders.TPrintBordersForm().create(self)
        if bordersForm == None:
            raise GeneralException.create("Problem: Could not create print borders window.")
        try:
            bordersForm.initializeWithOptions(self.options)
            if bordersForm.ShowModal() == mrOK:
                # just copy whole options, because you can't change this form while borders form is up
                self.options = bordersForm.options
                self.updateBorderThickness()
                self.updatePrintPreview()
        finally:
            bordersForm.free
    
    def printSetupClick(self, Sender):
        self.PrintDialog.execute
        self.updateForPrinterInfo()
        self.suggestPrintSizeClick(self)
    
    def CloseClick(self, Sender):
        insertString = ""
        
        if (self.colorType.ItemIndex == 0) and ((self.copySavePrintType == kSavingDrawingToBmp) or (self.copySavePrintType == kSavingDrawingToJpeg)):
            # don't let them save the file as a device-dependent bitmap.
            MessageDialog("You cannot save a picture with the \"From screen\" color depth." + chr(13) + "Please change the color depth to another choice in the list.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            return
        if (self.useSelectedPlants.Checked) and (umain.MainForm.selectedPlants.Count <= 0):
            # don't let them finish with no plants
            MessageDialog("You chose \"selected\" for \"Draw which plants\", but no plants are selected." + chr(13) + "You should make another choice, or click Cancel and select some plants.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            return
        if self.copySavePrintType != kSavingDrawingToJpeg:
            if self.megabytesOfMemoryNeeded > kTooManyMegabytesOfMemory:
                if self.copySavePrintType == kCopyingDrawing:
                    # warn about a really big operation
                    insertString = "copy to the clipboard"
                elif self.copySavePrintType == kPrintingDrawing:
                    insertString = "print"
                elif self.copySavePrintType == kSavingDrawingToBmp:
                    insertString = "save"
                if MessageDialog("You are about to " + insertString + " a " + usupport.digitValueString(self.megabytesOfMemoryNeeded) + " MB bitmap." + chr(13) + "This could place stress on your system." + chr(13) + "We recommend closing any non-essential programs." + chr(13) + "Also, choosing fewer colors or a smaller picture will use less memory." + chr(13) + chr(13) + "To proceed, click OK. To go back and make changes, click Cancel.", mtWarning, [mbOK, mbCancel, ], 0) == delphi_compatability.IDCANCEL:
                    return
        self.transferDirection = kTransferSave
        self.transferFields()
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    # ----------------------------------------------------------- methods to get/set edit values 
    def setValue(self, editBox, newValue):
        maxWidth_in = 0.0
        maxHeight_in = 0.0
        
        self.sideEffect = true
        maxWidth_in = self.wholePageWidth_in - self.printMinMarginLeft_in - self.printMinMarginRight_in
        maxHeight_in = self.wholePageHeight_in - self.printMinMarginTop_in - self.printMinMarginBottom_in
        if editBox == self.pixelWidthEdit:
            newValue = umath.max(udomain.kMinPixels, umath.min(udomain.kMaxPixels, newValue))
            self.pictureWidth_px = newValue
        elif editBox == self.pixelHeightEdit:
            newValue = umath.max(udomain.kMinPixels, umath.min(udomain.kMaxPixels, newValue))
            self.pictureHeight_px = newValue
        elif editBox == self.inchWidthEdit:
            newValue = umath.max(udomain.kMinInches, umath.min(udomain.kMaxInches, newValue))
            self.pictureWidth_in = newValue
        elif editBox == self.inchHeightEdit:
            newValue = umath.max(udomain.kMinInches, umath.min(udomain.kMaxInches, newValue))
            self.pictureHeight_in = newValue
        elif editBox == self.resolutionEdit:
            newValue = umath.max(udomain.kMinResolution, umath.min(udomain.kMaxResolution, newValue))
            self.pictureResolution_pxPin = newValue
        elif editBox == self.printWidthEdit:
            newValue = umath.max(udomain.kMinInches, umath.min(newValue, maxWidth_in))
            self.printWidth_in = newValue
        elif editBox == self.printHeightEdit:
            newValue = umath.max(udomain.kMinInches, umath.min(newValue, maxHeight_in))
            self.printHeight_in = newValue
        elif editBox == self.printLeftMarginEdit:
            newValue = umath.max(udomain.kMinInches, umath.min(newValue, maxWidth_in))
            self.printLeftMargin_in = newValue
        elif editBox == self.printTopMarginEdit:
            newValue = umath.max(udomain.kMinInches, umath.min(newValue, maxHeight_in))
            self.printTopMargin_in = newValue
        elif editBox == self.printRightMarginEdit:
            newValue = umath.max(udomain.kMinInches, umath.min(newValue, maxWidth_in))
            self.printRightMargin_in = newValue
        elif editBox == self.printBottomMarginEdit:
            newValue = umath.max(udomain.kMinInches, umath.min(newValue, maxHeight_in))
            self.printBottomMargin_in = newValue
        elif editBox == self.jpgCompressionEdit:
            newValue = umath.max(1, umath.min(100, newValue))
            self.jpegCompression = newValue
        if editBox.Tag == kEditBoxHasInteger:
            editBox.Text = IntToStr(intround(newValue))
        elif editBox.Tag == kEditBoxHasFloat:
            editBox.Text = floatStr(newValue)
        self.sideEffect = false
    
    def getValue(self, editBox):
        result = 0.0
        result = 0
        if editBox == self.pixelWidthEdit:
            result = self.pictureWidth_px
        elif editBox == self.pixelHeightEdit:
            result = self.pictureHeight_px
        elif editBox == self.inchWidthEdit:
            result = self.pictureWidth_in
        elif editBox == self.inchHeightEdit:
            result = self.pictureHeight_in
        elif editBox == self.resolutionEdit:
            result = self.pictureResolution_pxPin
        elif editBox == self.printWidthEdit:
            result = self.printWidth_in
        elif editBox == self.printHeightEdit:
            result = self.printHeight_in
        elif editBox == self.printLeftMarginEdit:
            result = self.printLeftMargin_in
        elif editBox == self.printTopMarginEdit:
            result = self.printTopMargin_in
        elif editBox == self.printRightMarginEdit:
            result = self.printRightMargin_in
        elif editBox == self.printBottomMarginEdit:
            result = self.printBottomMargin_in
        elif editBox == self.jpgCompressionEdit:
            result = self.jpegCompression
        return result
    
    def getEnteredValue(self, editBox):
        result = 0.0
        result = 0
        try:
            if editBox.Tag == kEditBoxHasInteger:
                result = StrToInt(editBox.Text)
            elif editBox.Tag == kEditBoxHasFloat:
                result = StrToFloat(editBox.Text)
        except exception, e:
            ShowMessage("Invalid value: " + e.message)
            result = 0
        return result
    
    # ------------------------------------------------------------------------- transfer functions 
    def currentExportOption(self):
        result = 0
        result = udomain.kIncludeSelectedPlants
        if self.useSelectedPlants.Checked:
            result = udomain.kIncludeSelectedPlants
        elif self.useVisiblePlants.Checked:
            result = udomain.kIncludeVisiblePlants
        elif self.useAllPlants.Checked:
            result = udomain.kIncludeAllPlants
        elif self.useDrawingAreaContents.Checked:
            result = udomain.kIncludeDrawingAreaContents
        return result
    
    def nameForCopySavePrintType(self, aType):
        result = ""
        result = ""
        if aType == kCopyingDrawing:
            result = "Copy"
        elif aType == kPrintingDrawing:
            result = "Print"
        elif aType == kSavingDrawingToBmp:
            result = "Save"
        elif aType == kSavingDrawingToJpeg:
            result = "Save"
        return result
    
    def transferCheckBox(self, checkBox, value):
        if self.transferDirection == kTransferLoad:
            checkBox.Checked = value
        elif self.transferDirection == kTransferSave:
            if value != checkBox.Checked:
                self.optionsChanged = true
            value = checkBox.Checked
        return value
    
    def transferSmallintEditBox(self, editBox, value):
        if self.transferDirection == kTransferLoad:
            # sets up vars at start
            self.setValue(editBox, value)
        elif self.transferDirection == kTransferSave:
            if value != StrToIntDef(editBox.Text, 0):
                self.optionsChanged = true
            value = StrToIntDef(editBox.Text, 0)
        return value
    
    def transferSingleEditBox(self, editBox, value):
        newValue = 0.0
        
        if self.transferDirection == kTransferLoad:
            # sets up vars at start
            self.setValue(editBox, value)
        elif self.transferDirection == kTransferSave:
            try:
                newValue = StrToFloat(editBox.Text)
            except:
                newValue = value
            if newValue != value:
                self.optionsChanged = true
            value = newValue
        return value
    
    def transferComboBox(self, comboBox, value):
        if self.transferDirection == kTransferLoad:
            comboBox.ItemIndex = value
        elif self.transferDirection == kTransferSave:
            if value != comboBox.ItemIndex:
                self.optionsChanged = true
            value = comboBox.ItemIndex
        return value
    
    def transferTPixelFormatComboBox(self, comboBox, value):
        raise "method transferTPixelFormatComboBox had assigned to var parameter value not added to return; fixup manually"
        if self.transferDirection == kTransferLoad:
            if value == delphi_compatability.TPixelFormat.pfCustom:
                value = delphi_compatability.TPixelFormat.pfDevice
            comboBox.ItemIndex = ord(value)
        elif self.transferDirection == kTransferSave:
            if value != UNRESOLVED.TPixelFormat(comboBox.ItemIndex):
                self.optionsChanged = true
            value = UNRESOLVED.TPixelFormat(comboBox.ItemIndex)
    
    def colorTypeDrawItem(self, Control, index, Rect, State):
        selected = false
        cText = [0] * (range(0, 255 + 1) + 1)
        
        if delphi_compatability.Application.terminated:
            return
        selected = (delphi_compatability.TOwnerDrawStateType.odSelected in State)
        self.colorType.Canvas.Font = self.colorType.Font
        if selected:
            self.colorType.Canvas.Brush.Color = UNRESOLVED.clHighlight
            self.colorType.Canvas.Font.Color = UNRESOLVED.clHighlightText
        else:
            self.colorType.Canvas.Brush.Color = self.colorType.Color
            self.colorType.Canvas.Font.Color = UNRESOLVED.clBtnText
        if (index == 0) and ((self.copySavePrintType == kSavingDrawingToBmp) or (self.copySavePrintType == kSavingDrawingToJpeg)):
            self.colorType.Canvas.Font.Color = UNRESOLVED.clBtnShadow
        self.colorType.Canvas.FillRect(Rect)
        UNRESOLVED.strPCopy(cText, self.colorType.Items[index])
        # margin for text 
        Rect.left = Rect.left + 2
        UNRESOLVED.drawText(self.colorType.Canvas.Handle, cText, len(cText), Rect, delphi_compatability.DT_LEFT)
    
    def helpButtonClick(self, Sender):
        if self.copySavePrintType == kCopyingDrawing:
            delphi_compatability.Application.HelpJump("Copying_pictures")
        elif self.copySavePrintType == kPrintingDrawing:
            delphi_compatability.Application.HelpJump("Printing_pictures")
        elif self.copySavePrintType == kSavingDrawingToBmp:
            delphi_compatability.Application.HelpJump("Saving_pictures")
        elif self.copySavePrintType == kSavingDrawingToJpeg:
            delphi_compatability.Application.HelpJump("Saving_pictures")
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
