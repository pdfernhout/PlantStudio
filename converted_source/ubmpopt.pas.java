// unit ubmpopt

from conversion_common import *;
import udebug;
import uborders;
import updform;
import delphi_compatability;

// const
kCopyingDrawing = 0;
kPrintingDrawing = 1;
kSavingDrawingToBmp = 2;
kSavingDrawingToJpeg = 3;


// const
kTransferLoad = 1;
kTransferSave = 2;
kSpinNone = 0;
kSpinUp = 1;
kSpinDown = -1;
kEditIsInteger = 0;
kEditIsFloat = 1;
kWidthWasChanged = 0;
kHeightWasChanged = 1;
kHeightAndWidthWereChanged = 2;
kEditBoxHasInteger = 0;
kEditBoxHasFloat = 1;
kTooManyMegabytesOfMemory = 10.0;


//$R *.DFM
public String floatStr(float value) {
    result = "";
    result = FloatToStrF(value, UNRESOLVED.ffFixed, 7, 2);
    return result;
}


class TBitmapOptionsForm extends PdForm {
    public TButton Close;
    public TButton cancel;
    public TGroupBox printBox;
    public TGroupBox outputBox;
    public TLabel resolutionLabel;
    public TLabel sizePixelsLabel;
    public TLabel sizeInchesLabel;
    public TEdit inchWidthEdit;
    public TEdit inchHeightEdit;
    public TComboBox colorType;
    public TLabel colorsLabel;
    public TButton printSetup;
    public TCheckBox printPreserveAspectRatio;
    public TGroupBox plantsBox;
    public TRadioButton useSelectedPlants;
    public TRadioButton useAllPlants;
    public TRadioButton useDrawingAreaContents;
    public TRadioButton useVisiblePlants;
    public TEdit resolutionEdit;
    public TEdit pixelWidthEdit;
    public TEdit pixelHeightEdit;
    public TSpinButton resolutionSpin;
    public TSpinButton pixelWidthSpin;
    public TSpinButton pixelHeightSpin;
    public TSpinButton inchHeightSpin;
    public TSpinButton inchWidthSpin;
    public TPrintDialog PrintDialog;
    public TCheckBox preserveAspectRatio;
    public TLabel inchHeightLabel;
    public TLabel pixelWidthLabel;
    public TLabel pixelHeightLabel;
    public TButton borders;
    public TPanel currentStuffPanel;
    public TLabel selectedImageInfoLabel;
    public TLabel screenInfoLabel;
    public TLabel printerOrFileTypeInfoLabel;
    public TLabel sizeLabel;
    public TLabel printWidthLabel;
    public TEdit printWidthEdit;
    public TSpinButton printWidthSpin;
    public TLabel printHeightLabel;
    public TEdit printHeightEdit;
    public TSpinButton printHeightSpin;
    public TLabel marginsLabel;
    public TLabel printLeftMarginLabel;
    public TLabel printTopMarginLabel;
    public TEdit printLeftMarginEdit;
    public TEdit printTopMarginEdit;
    public TSpinButton printLeftMarginSpin;
    public TSpinButton printTopMarginSpin;
    public TLabel printRightMarginLabel;
    public TLabel printBottomMarginLabel;
    public TEdit printRightMarginEdit;
    public TEdit printBottomMarginEdit;
    public TSpinButton printRightMarginSpin;
    public TSpinButton printBottomMarginSpin;
    public TButton printCenter;
    public TButton printUseWholePage;
    public TButton suggestPrintSize;
    public TPanel printImagePanel;
    public TImage wholePageImage;
    public TLabel inchWidthLabel;
    public TSpeedButton helpButton;
    public TLabel memoryUseInfoLabel;
    public TLabel jpgCompressionLabel;
    public TEdit jpgCompressionEdit;
    public TSpinButton jpgCompressionSpin;
    public BitmapOptionsStructure options;
    public short transferDirection;
    public boolean optionsChanged;
    public short copySavePrintType;
    public boolean startingUp;
    public boolean sideEffect;
    public TRect selectionRectFromMainWindow;
    public float printPageWidth_in;
    public float printPageHeight_in;
    public float wholePageWidth_in;
    public float wholePageHeight_in;
    public float printMinMarginLeft_in;
    public float printMinMarginTop_in;
    public float printMinMarginRight_in;
    public float printMinMarginBottom_in;
    public float pictureWidth_px;
    public float pictureHeight_px;
    public float pictureResolution_pxPin;
    public float smallestPrintResolution_pxPin;
    public float pictureWidth_in;
    public float pictureHeight_in;
    public float printWidth_in;
    public float printHeight_in;
    public float printLeftMargin_in;
    public float printTopMargin_in;
    public float printRightMargin_in;
    public float printBottomMargin_in;
    public float jpegCompression;
    public float aspectRatio;
    public float megabytesOfMemoryNeeded;
    
    // ----------------------------------------------------------------------------------------- initialize 
    public void initializeWithTypeAndOptions(short aType, BitmapOptionsStructure anOptions) {
        String displayString = "";
        
        this.startingUp = true;
        this.options = anOptions;
        this.copySavePrintType = aType;
        displayString = this.nameForCopySavePrintType(this.copySavePrintType);
        if (this.copySavePrintType == kPrintingDrawing) {
            // must be done before transfer
            this.updateForPrinterInfo();
        }
        this.transferDirection = kTransferLoad;
        this.transferFields();
        this.updateForImageSelection();
        this.maintainAspectRatioPixelsAndInches(this.pixelWidthEdit);
        this.updateBorderThickness();
        this.printSetup.Visible = this.copySavePrintType == kPrintingDrawing;
        this.borders.Visible = this.copySavePrintType == kPrintingDrawing;
        this.printerOrFileTypeInfoLabel.Visible = this.copySavePrintType != kCopyingDrawing;
        if (this.copySavePrintType == kSavingDrawingToJpeg) {
            this.jpgCompressionLabel.Visible = true;
            this.colorsLabel.Visible = false;
            this.jpgCompressionLabel.SetBounds(this.colorsLabel.Left, this.colorsLabel.Top, this.jpgCompressionLabel.Width, this.jpgCompressionLabel.Height);
            this.jpgCompressionEdit.Visible = true;
            this.colorType.Visible = false;
            this.jpgCompressionEdit.SetBounds(this.colorType.Left, this.colorType.Top, this.jpgCompressionEdit.Width, this.jpgCompressionEdit.Height);
            this.jpgCompressionSpin.Visible = true;
            this.jpgCompressionSpin.SetBounds(this.jpgCompressionEdit.Left + this.jpgCompressionEdit.Width + 4, this.jpgCompressionEdit.Top, this.jpgCompressionSpin.Width, this.jpgCompressionSpin.Height);
        }
        if ((this.copySavePrintType == kSavingDrawingToBmp) || (this.copySavePrintType == kSavingDrawingToJpeg)) {
            if ((this.copySavePrintType == kSavingDrawingToBmp)) {
                this.printerOrFileTypeInfoLabel.Caption = "Saving to: BMP";
            } else if ((this.copySavePrintType == kSavingDrawingToJpeg)) {
                this.printerOrFileTypeInfoLabel.Caption = "Saving to: JPEG";
            }
        }
        if (this.copySavePrintType == kPrintingDrawing) {
            this.ClientHeight = this.printBox.Top + this.printBox.Height;
            this.suggestPrintSizeClick(this);
        } else {
            this.ClientHeight = this.outputBox.Top + this.outputBox.Height;
        }
        switch (this.copySavePrintType) {
            case kCopyingDrawing:
                this.Close.Caption = "&Copy";
                break;
            case kPrintingDrawing:
                this.Close.Caption = "&Print";
                break;
            case kSavingDrawingToBmp:
                this.Close.Caption = "&Save";
                break;
            case kSavingDrawingToJpeg:
                this.Close.Caption = "&Save";
                break;
        this.helpButton.Hint = "Get help with setting " + lowercase(displayString) + " picture options.";
        this.cancel.Hint = "Close this window and don't " + lowercase(displayString) + " a picture.";
        this.Close.Hint = displayString + " the selected picture using the options specified in this window.";
        this.startingUp = false;
    }
    
    public void updateForPrinterInfo() {
        int xResolution_pixelsPerInch = 0;
        int yResolution_pixelsPerInch = 0;
        String portraitOrLandscape = "";
        HDC printerDC = new HDC();
        int printerColorBits = 0;
        int printerColors = 0;
        
        xResolution_pixelsPerInch = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSX);
        yResolution_pixelsPerInch = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSY);
        this.smallestPrintResolution_pxPin = UNRESOLVED.intMin(xResolution_pixelsPerInch, yResolution_pixelsPerInch);
        this.printPageWidth_in = UNRESOLVED.safedivExcept(UNRESOLVED.Printer.pageWidth - 1, xResolution_pixelsPerInch, 0);
        this.printPageHeight_in = UNRESOLVED.safedivExcept(UNRESOLVED.Printer.pageHeight - 1, yResolution_pixelsPerInch, 0);
        this.wholePageWidth_in = UNRESOLVED.safedivExcept(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PHYSICALWIDTH), xResolution_pixelsPerInch, 0);
        this.wholePageHeight_in = UNRESOLVED.safedivExcept(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PHYSICALHEIGHT), xResolution_pixelsPerInch, 0);
        this.printMinMarginLeft_in = UNRESOLVED.safedivExcept(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PhysicalOffsetX), xResolution_pixelsPerInch, 0);
        this.printMinMarginTop_in = UNRESOLVED.safedivExcept(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PhysicalOffsetY), xResolution_pixelsPerInch, 0);
        this.printMinMarginRight_in = this.wholePageWidth_in - this.printPageWidth_in - this.printMinMarginLeft_in;
        this.printMinMarginBottom_in = this.wholePageHeight_in - this.printPageHeight_in - this.printMinMarginTop_in;
        if (UNRESOLVED.Printer.orientation == UNRESOLVED.poPortrait) {
            portraitOrLandscape = "Portrait";
        } else {
            portraitOrLandscape = "Landscape";
        }
        printerDC = UNRESOLVED.CreateCompatibleDC(UNRESOLVED.Printer.Handle);
        try {
            printerColorBits = (UNRESOLVED.GetDeviceCaps(printerDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(printerDC, delphi_compatability.PLANES));
        } finally {
            UNRESOLVED.ReleaseDC(0, printerDC);
            UNRESOLVED.DeleteDC(printerDC);
        }
        if (printerColorBits != 32) {
            printerColors = 1 << printerColorBits;
        } else {
            printerColors = intround(UNRESOLVED.power(2.0, printerColorBits));
        }
        this.printerOrFileTypeInfoLabel.Caption = "Printer:  " + IntToStr(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSX)) + " x " + IntToStr(UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSY)) + " pixels/inch, " + IntToStr(printerColors) + " colors (" + IntToStr(printerColorBits) + " bits)";
        //+ portraitOrLandscape;
        //printerInfoLabel.hint := 'Printer name: ' + Printer.Printers[Printer.printerIndex];
        this.updatePrintPreview();
    }
    
    public void updateForImageSelection() {
        int pixelWidth = 0;
        int pixelHeight = 0;
        int screenColorBits = 0;
        long screenColors = 0;
        float inchWidth = 0.0;
        float inchHeight = 0.0;
        HDC screenDC = new HDC();
        float megabytesNeeded = 0.0;
        
        this.updateSelectionRectFromMainWindow();
        // fill in labels
        pixelWidth = UNRESOLVED.rWidth(this.selectionRectFromMainWindow);
        pixelHeight = UNRESOLVED.rHeight(this.selectionRectFromMainWindow);
        inchWidth = UNRESOLVED.safedivExcept(pixelWidth, delphi_compatability.Screen.PixelsPerInch, 0);
        inchHeight = UNRESOLVED.safedivExcept(pixelHeight, delphi_compatability.Screen.PixelsPerInch, 0);
        this.selectedImageInfoLabel.Caption = "Selection:  " + IntToStr(pixelWidth) + " x " + IntToStr(pixelHeight) + " pixels,  " + floatStr(inchWidth) + " x " + floatStr(inchHeight) + " inches";
        screenDC = UNRESOLVED.GetDC(0);
        try {
            screenColorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES));
        } finally {
            UNRESOLVED.ReleaseDC(0, screenDC);
        }
        if (screenColorBits != 32) {
            screenColors = 1 << screenColorBits;
            this.screenInfoLabel.Caption = "Screen:  " + IntToStr(delphi_compatability.Screen.PixelsPerInch) + " pixels/inch,  " + IntToStr(screenColors) + " colors (" + IntToStr(screenColorBits) + " bits)";
        } else {
            this.screenInfoLabel.Caption = "Screen:  " + IntToStr(delphi_compatability.Screen.PixelsPerInch) + " pixels/inch,  " + "true color (" + IntToStr(screenColorBits) + " bits)";
        }
        // used to be only in suggest size button, now doing automatically
        this.setValue(this.inchWidthEdit, inchWidth);
        this.setValue(this.inchHeightEdit, inchHeight);
        this.calculatePixelsFromResolutionAndInches();
        if (this.copySavePrintType == kPrintingDrawing) {
            this.suggestPrintSizeClick(this);
            this.updatePrintPreview();
        }
        this.reportOnMemoryNeeded();
    }
    
    public void reportOnMemoryNeeded() {
        if (this.copySavePrintType == kSavingDrawingToJpeg) {
            // report memory needed -- do after calculating resolution-affected size
            // make no size estimation for JPG
            this.memoryUseInfoLabel.Visible = false;
            return;
        }
        this.calculatePixelsFromResolutionAndInches();
        this.calculateMegabytesOfMemoryNeededConsideringColorBitsAndResolution();
        if (this.megabytesOfMemoryNeeded < 1.0) {
            this.memoryUseInfoLabel.Caption = "Estimated memory needed: " + UNRESOLVED.digitValueString(this.megabytesOfMemoryNeeded * 1024) + " K";
        } else {
            this.memoryUseInfoLabel.Caption = "Estimated memory needed: " + UNRESOLVED.digitValueString(this.megabytesOfMemoryNeeded) + " MB";
        }
        if (this.megabytesOfMemoryNeeded > kTooManyMegabytesOfMemory) {
            this.memoryUseInfoLabel.Font.Style = {UNRESOLVED.fsBold, };
        } else {
            this.memoryUseInfoLabel.Font.Style = {};
        }
    }
    
    public void calculateMegabytesOfMemoryNeededConsideringColorBitsAndResolution() {
        short colorBits = 0;
        HDC screenDC = new HDC();
        float outputPixelWidth = 0.0;
        float outputPixelHeight = 0.0;
        
        outputPixelWidth = this.pictureWidth_in * this.pictureResolution_pxPin;
        outputPixelHeight = this.pictureHeight_in * this.pictureResolution_pxPin;
        colorBits = 0;
        switch (this.colorType.ItemIndex) {
            case (int)delphi_compatability.TPixelFormat.pfDevice:
                screenDC = UNRESOLVED.GetDC(0);
                try {
                    colorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES));
                } finally {
                    UNRESOLVED.ReleaseDC(0, screenDC);
                }
                break;
            case (int)delphi_compatability.TPixelFormat.pf1bit:
                colorBits = 1;
                break;
            case (int)delphi_compatability.TPixelFormat.pf4bit:
                colorBits = 4;
                break;
            case (int)delphi_compatability.TPixelFormat.pf8bit:
                colorBits = 8;
                break;
            case (int)delphi_compatability.TPixelFormat.pf15bit:
                colorBits = 15;
                break;
            case (int)delphi_compatability.TPixelFormat.pf16bit:
                colorBits = 16;
                break;
            case (int)delphi_compatability.TPixelFormat.pf24bit:
                colorBits = 24;
                break;
            case (int)delphi_compatability.TPixelFormat.pf32bit:
                colorBits = 32;
                break;
        this.megabytesOfMemoryNeeded = (1.0 * outputPixelWidth * outputPixelHeight * (colorBits / 8) + FIX_sizeof(delphi_compatability.TBitmapInfo)) / (1024 * 1024);
    }
    
    public void updateSelectionRectFromMainWindow() {
        boolean excludeInvisiblePlants = false;
        boolean excludeNonSelectedPlants = false;
        
        excludeInvisiblePlants = !this.useAllPlants.Checked;
        excludeNonSelectedPlants = this.useSelectedPlants.Checked;
        if (this.useDrawingAreaContents.Checked) {
            this.selectionRectFromMainWindow = Rect(0, 0, UNRESOLVED.MainForm.drawingPaintBox.width, UNRESOLVED.MainForm.drawingPaintBox.height);
        } else {
            this.selectionRectFromMainWindow = UNRESOLVED.domain.plantManager.combinedPlantBoundsRects(UNRESOLVED.MainForm.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants);
        }
        this.aspectRatio = UNRESOLVED.safedivExcept(UNRESOLVED.rWidth(this.selectionRectFromMainWindow), UNRESOLVED.rHeight(this.selectionRectFromMainWindow), 1.0);
    }
    
    public void updatePrintPreview() {
        float scaleX_pxPin = 0.0;
        float scaleY_pxPin = 0.0;
        float scale_pxPin = 0.0;
        float borderThickness_in = 0.0;
        short availableWidth_px = 0;
        short availableHeight_px = 0;
        TRect marginRect = new TRect();
        
        availableWidth_px = this.sizeLabel.Left - this.wholePageImage.Left - 10;
        availableHeight_px = this.printBox.Height - this.wholePageImage.Top - 10;
        scaleX_pxPin = UNRESOLVED.safedivExcept(1.0 * availableWidth_px, this.wholePageWidth_in, 5);
        scaleY_pxPin = UNRESOLVED.safedivExcept(1.0 * availableHeight_px, this.wholePageHeight_in, 5);
        scale_pxPin = UNRESOLVED.min(scaleX_pxPin, scaleY_pxPin);
        this.wholePageImage.Width = intround(this.wholePageWidth_in * scale_pxPin);
        this.wholePageImage.Height = intround(this.wholePageHeight_in * scale_pxPin);
        if ((this.wholePageImage.Picture.Bitmap.Width != this.wholePageImage.Width) || (this.wholePageImage.Picture.Bitmap.Height != this.wholePageImage.Height)) {
            try {
                this.wholePageImage.Picture.Bitmap.Width = this.wholePageImage.Width;
                this.wholePageImage.Picture.Bitmap.Height = this.wholePageImage.Height;
            } catch (Exception e) {
                this.wholePageImage.Picture.Bitmap.Width = 1;
                this.wholePageImage.Picture.Bitmap.Height = 1;
            }
        }
        marginRect.Left = intround(this.printMinMarginLeft_in * scale_pxPin);
        marginRect.Top = intround(this.printMinMarginTop_in * scale_pxPin);
        // subtract 1 from right and bottom because last pixel is not drawn
        marginRect.Right = this.wholePageImage.Width - intround(this.printMinMarginRight_in * scale_pxPin) - 1;
        marginRect.Bottom = this.wholePageImage.Height - intround(this.printMinMarginBottom_in * scale_pxPin) - 1;
        this.wholePageImage.Picture.Bitmap.Canvas.Brush.Color = delphi_compatability.clWindow;
        this.wholePageImage.Picture.Bitmap.Canvas.FillRect(Rect(0, 0, this.wholePageImage.Width, this.wholePageImage.Height));
        this.wholePageImage.Picture.Bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        this.wholePageImage.Picture.Bitmap.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
        this.wholePageImage.Picture.Bitmap.Canvas.MoveTo(0, marginRect.Top);
        this.wholePageImage.Picture.Bitmap.Canvas.LineTo(this.wholePageImage.Width, marginRect.Top);
        this.wholePageImage.Picture.Bitmap.Canvas.MoveTo(marginRect.Left, 0);
        this.wholePageImage.Picture.Bitmap.Canvas.LineTo(marginRect.Left, this.wholePageImage.Height);
        this.wholePageImage.Picture.Bitmap.Canvas.MoveTo(marginRect.Right, 0);
        this.wholePageImage.Picture.Bitmap.Canvas.LineTo(marginRect.Right, this.wholePageImage.Height);
        this.wholePageImage.Picture.Bitmap.Canvas.MoveTo(0, marginRect.Bottom);
        this.wholePageImage.Picture.Bitmap.Canvas.LineTo(this.wholePageImage.Width, marginRect.Bottom);
        this.wholePageImage.Picture.Bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid;
        this.wholePageImage.Picture.Bitmap.Canvas.Rectangle(0, 0, this.wholePageImage.Width, this.wholePageImage.Height);
        borderThickness_in = UNRESOLVED.safedivExcept(this.options.borderThickness, this.smallestPrintResolution_pxPin, 0);
        this.printImagePanel.SetBounds(intround(this.wholePageImage.Left + (this.printLeftMargin_in - borderThickness_in) * scale_pxPin), intround(this.wholePageImage.Top + (this.printTopMargin_in - borderThickness_in) * scale_pxPin), intround((this.printWidth_in + borderThickness_in * 2) * scale_pxPin), intround((this.printHeight_in + borderThickness_in * 2) * scale_pxPin));
    }
    
    public void updateBorderThickness() {
        //FIX unresolved WITH expression: self.options
        UNRESOLVED.borderThickness = 0;
        UNRESOLVED.borderGap = 0;
        if (UNRESOLVED.printBorderInner) {
            // cfk the 2.5 is arbitrary
            UNRESOLVED.borderGap = intround(UNRESOLVED.printBorderWidthInner * 2.5);
            UNRESOLVED.borderThickness += UNRESOLVED.printBorderWidthInner + UNRESOLVED.borderGap;
        }
        if (this.options.printBorderOuter) {
            UNRESOLVED.borderThickness += UNRESOLVED.printBorderWidthOuter;
        }
    }
    
    // ----------------------------------------------------------------------------------------- transfer 
    public void transferFields() {
        if (this.transferDirection == kTransferLoad) {
            switch (this.options.exportType) {
                case UNRESOLVED.kIncludeSelectedPlants:
                    // plantBox
                    this.useSelectedPlants.Checked = true;
                    break;
                case UNRESOLVED.kIncludeVisiblePlants:
                    this.useVisiblePlants.Checked = true;
                    break;
                case UNRESOLVED.kIncludeAllPlants:
                    this.useAllPlants.Checked = true;
                    break;
                case UNRESOLVED.kIncludeDrawingAreaContents:
                    this.useDrawingAreaContents.Checked = true;
                    break;
        } else if (this.transferDirection == kTransferSave) {
            this.options.exportType = this.currentExportOption();
        }
        if (this.copySavePrintType != kSavingDrawingToJpeg) {
            // output
            this.transferTPixelFormatComboBox(this.colorType, this.options.colorType);
        }
        this.options.resolution_pixelsPerInch = this.transferSmallintEditBox(this.resolutionEdit, this.options.resolution_pixelsPerInch);
        this.options.width_pixels = this.transferSmallintEditBox(this.pixelWidthEdit, this.options.width_pixels);
        this.options.height_pixels = this.transferSmallintEditBox(this.pixelHeightEdit, this.options.height_pixels);
        this.options.width_in = this.transferSingleEditBox(this.inchWidthEdit, this.options.width_in);
        this.options.height_in = this.transferSingleEditBox(this.inchHeightEdit, this.options.height_in);
        this.options.preserveAspectRatio = this.transferCheckBox(this.preserveAspectRatio, this.options.preserveAspectRatio);
        if (this.copySavePrintType == kSavingDrawingToJpeg) {
            this.options.jpegCompressionRatio = this.transferSmallintEditBox(this.jpgCompressionEdit, this.options.jpegCompressionRatio);
        }
        if (this.copySavePrintType != kPrintingDrawing) {
            // printing
            return;
        }
        this.options.printPreserveAspectRatio = this.transferCheckBox(this.printPreserveAspectRatio, this.options.printPreserveAspectRatio);
        this.options.printWidth_in = this.transferSingleEditBox(this.printWidthEdit, this.options.printWidth_in);
        this.options.printHeight_in = this.transferSingleEditBox(this.printHeightEdit, this.options.printHeight_in);
        this.options.printLeftMargin_in = this.transferSingleEditBox(this.printLeftMarginEdit, this.options.printLeftMargin_in);
        this.options.printTopMargin_in = this.transferSingleEditBox(this.printTopMarginEdit, this.options.printTopMargin_in);
        this.options.printRightMargin_in = this.transferSingleEditBox(this.printRightMarginEdit, this.options.printRightMargin_in);
        this.options.printBottomMargin_in = this.transferSingleEditBox(this.printBottomMarginEdit, this.options.printBottomMargin_in);
    }
    
    // ----------------------------------------------------------------------------------------- interactions-first panel 
    public void selectionChoiceClick(TObject sender) {
        if (this.startingUp || this.sideEffect) {
            return;
        }
        this.updateForImageSelection();
    }
    
    public void preserveAspectRatioClick(TObject Sender) {
        if (this.startingUp || this.sideEffect) {
            return;
        }
        if (this.preserveAspectRatio.Checked) {
            // arbitrarily picked pixelWidthEdit here
            this.maintainAspectRatioPixelsAndInches(this.pixelWidthEdit);
        }
    }
    
    public void colorTypeChange(TObject Sender) {
        if (this.startingUp || this.sideEffect) {
            return;
        }
        this.updateForImageSelection();
    }
    
    // ----------------------------------------------------------------------------------------- interactions-second panel 
    public void exitEditBox(TObject sender) {
        this.adjustValue(sender, kSpinNone);
    }
    
    public void spinUp(TObject sender) {
        this.adjustValue(sender, kSpinUp);
    }
    
    public void spinDown(TObject sender) {
        this.adjustValue(sender, kSpinDown);
    }
    
    public void adjustValue(TObject sender, short spin) {
        TEdit editBox = new TEdit();
        
        if (this.startingUp || this.sideEffect) {
            return;
        }
        editBox = null;
        if ((sender instanceof delphi_compatability.TSpinButton)) {
            // if spin button clicked, adjust corresponding edit (focusControl)
            this.adjustEditBoxValueForSpin(sender, spin);
        }
        if ((sender instanceof delphi_compatability.TEdit)) {
            // get edit box
            editBox = (delphi_compatability.TEdit)sender;
        } else if ((sender instanceof delphi_compatability.TSpinButton)) {
            editBox = (delphi_compatability.TEdit)((delphi_compatability.TSpinButton)sender).focusControl;
        }
        if (editBox == null) {
            return;
        }
        // use set method to check edit box entry against bounds
        this.setValue(editBox, this.getEnteredValue(editBox));
        if (this.preserveAspectRatio.Checked) {
            if ((editBox == this.inchWidthEdit) || (editBox == this.inchHeightEdit) || (editBox == this.pixelWidthEdit) || (editBox == this.pixelHeightEdit)) {
                // if image width/height changed, maintain aspect ratio
                this.maintainAspectRatioPixelsAndInches(editBox);
            }
        }
        if (this.printPreserveAspectRatio.Checked) {
            if ((editBox == this.printWidthEdit) || (editBox == this.printHeightEdit)) {
                if (editBox == this.printWidthEdit) {
                    // if print width/height changed, maintain printing aspect ratio
                    this.resizePrintBasedOnAspectRatio(kWidthWasChanged);
                } else {
                    this.resizePrintBasedOnAspectRatio(kHeightWasChanged);
                }
            }
        }
        if ((editBox == this.inchWidthEdit) || (editBox == this.inchHeightEdit) || (editBox == this.resolutionEdit)) {
            // interaction between image inches, pixels, resolution
            this.reportOnMemoryNeeded();
        } else if ((editBox == this.pixelWidthEdit) || (editBox == this.pixelHeightEdit)) {
            // interaction between print size and margins
            this.reportOnMemoryNeeded();
        } else if ((editBox == this.printWidthEdit) || (editBox == this.printHeightEdit)) {
            this.changePrintMarginsToFitPrintSize();
        } else if ((editBox == this.printLeftMarginEdit) || (editBox == this.printTopMarginEdit) || (editBox == this.printRightMarginEdit) || (editBox == this.printBottomMarginEdit)) {
            this.changePrintSizeToFitPrintMargins(editBox);
        }
    }
    
    public void adjustEditBoxValueForSpin(TObject sender, short spin) {
        TEdit editBox = new TEdit();
        float newValue = 0.0;
        
        if ((sender == null) || (!(sender instanceof delphi_compatability.TSpinButton))) {
            return;
        }
        editBox = null;
        editBox = (delphi_compatability.TEdit)((delphi_compatability.TSpinButton)sender).focusControl;
        if (editBox == null) {
            return;
        }
        // edit tag is 1 if float
        // spin tag is spin increment * 100 (10 for floats (0.1), 1000 for ints (10))
        newValue = 0;
        if (((delphi_compatability.TSpinButton)sender).focusControl.tag == kEditIsFloat) {
            newValue = this.getValue(editBox) + 1.0 * ((delphi_compatability.TSpinButton)sender).tag / 100 * spin;
        } else {
            newValue = this.getValue(editBox) + ((delphi_compatability.TSpinButton)sender).tag / 100 * spin;
        }
        this.setValue(editBox, newValue);
    }
    
    public void maintainAspectRatioPixelsAndInches(TEdit editBox) {
        if ((editBox == this.inchWidthEdit)) {
            this.setValue(this.inchHeightEdit, this.heightForWidthAndAspectRatio(this.pictureWidth_in, this.aspectRatio));
        } else if ((editBox == this.inchHeightEdit)) {
            this.setValue(this.inchWidthEdit, this.widthForHeightAndAspectRatio(this.pictureHeight_in, this.aspectRatio));
        } else if ((editBox == this.pixelWidthEdit)) {
            this.setValue(this.pixelHeightEdit, this.heightForWidthAndAspectRatio(this.pictureWidth_px, this.aspectRatio));
        } else if ((editBox == this.pixelHeightEdit)) {
            this.setValue(this.pixelWidthEdit, this.widthForHeightAndAspectRatio(this.pictureHeight_px, this.aspectRatio));
        }
    }
    
    public float heightForWidthAndAspectRatio(float width, float ratio) {
        result = 0.0;
        result = UNRESOLVED.safedivExcept(width, ratio, 0);
        return result;
    }
    
    public float widthForHeightAndAspectRatio(float height, float ratio) {
        result = 0.0;
        result = height * ratio;
        return result;
    }
    
    public void calculatePixelsFromResolutionAndInches() {
        this.setValue(this.pixelWidthEdit, this.pictureWidth_in * this.pictureResolution_pxPin);
        this.setValue(this.pixelHeightEdit, this.pictureHeight_in * this.pictureResolution_pxPin);
    }
    
    public void calculateInchesFromResolutionAndPixels() {
        this.setValue(this.inchWidthEdit, UNRESOLVED.safedivExcept(1.0 * this.pictureWidth_px, 1.0 * this.pictureResolution_pxPin, 0));
        this.setValue(this.inchHeightEdit, UNRESOLVED.safedivExcept(1.0 * this.pictureHeight_px, 1.0 * this.pictureResolution_pxPin, 0));
    }
    
    public void calculateResolutionFromInchesAndPixels() {
        float xRes = 0.0;
        float yRes = 0.0;
        
        xRes = UNRESOLVED.safedivExcept(this.pictureWidth_px, this.pictureWidth_in, delphi_compatability.Screen.PixelsPerInch);
        yRes = UNRESOLVED.safedivExcept(this.pictureHeight_px, this.pictureHeight_in, delphi_compatability.Screen.PixelsPerInch);
        this.setValue(this.resolutionEdit, intround(UNRESOLVED.min(xRes, yRes)));
        this.calculatePixelsFromResolutionAndInches();
    }
    
    public void suggestCopySizeClick(TObject Sender) {
        this.updateSelectionRectFromMainWindow();
        this.setValue(this.pixelWidthEdit, UNRESOLVED.rWidth(this.selectionRectFromMainWindow));
        this.setValue(this.pixelHeightEdit, UNRESOLVED.rHeight(this.selectionRectFromMainWindow));
        this.calculateInchesFromResolutionAndPixels();
    }
    
    // -------------------------------------------------------------------- calculations of print size/margins 
    public void changePrintMarginsToFitPrintSize() {
        this.setValue(this.printRightMarginEdit, UNRESOLVED.max(0, this.wholePageWidth_in - this.printLeftMargin_in - this.printWidth_in));
        this.setValue(this.printBottomMarginEdit, UNRESOLVED.max(0, this.wholePageHeight_in - this.printTopMargin_in - this.printHeight_in));
        if (this.printPreserveAspectRatio.Checked) {
            this.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged);
        } else {
            this.updatePrintPreview();
        }
    }
    
    public void changePrintSizeToFitPrintMargins(TEdit editBox) {
        if (editBox == this.printLeftMarginEdit) {
            // keep print size same to start, just offset other margin
            this.setValue(this.printRightMarginEdit, UNRESOLVED.max(0, this.wholePageWidth_in - this.printLeftMargin_in - this.printWidth_in));
        } else if (editBox == this.printRightMarginEdit) {
            this.setValue(this.printLeftMarginEdit, UNRESOLVED.max(0, this.wholePageWidth_in - this.printRightMargin_in - this.printWidth_in));
        } else if (editBox == this.printTopMarginEdit) {
            this.setValue(this.printBottomMarginEdit, UNRESOLVED.max(0, this.wholePageHeight_in - this.printTopMargin_in - this.printHeight_in));
        } else if (editBox == this.printBottomMarginEdit) {
            this.setValue(this.printTopMarginEdit, UNRESOLVED.max(0, this.wholePageHeight_in - this.printBottomMargin_in - this.printHeight_in));
        }
        // now set print size
        this.setValue(this.printWidthEdit, UNRESOLVED.max(0, this.wholePageWidth_in - this.printRightMargin_in - this.printLeftMargin_in));
        this.setValue(this.printHeightEdit, UNRESOLVED.max(0, this.wholePageHeight_in - this.printBottomMargin_in - this.printTopMargin_in));
        if (this.printPreserveAspectRatio.Checked) {
            // now check aspect ratio
            this.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged);
        } else {
            this.updatePrintPreview();
        }
    }
    
    public void resizePrintBasedOnAspectRatio(short whatWasChanged) {
        float newWidth_in = 0.0;
        float newHeight_in = 0.0;
        float newRight_in = 0.0;
        float newBottom_in = 0.0;
        float maxWidth_in = 0.0;
        float maxHeight_in = 0.0;
        
        newWidth_in = this.printWidth_in;
        newHeight_in = this.printHeight_in;
        this.updateSelectionRectFromMainWindow();
        switch (whatWasChanged) {
            case kHeightWasChanged:
                newWidth_in = newHeight_in * this.aspectRatio;
                break;
            case kWidthWasChanged:
                newHeight_in = UNRESOLVED.safedivExcept(newWidth_in, this.aspectRatio, newHeight_in);
                break;
            case kHeightAndWidthWereChanged:
                if (newWidth_in > newHeight_in) {
                    newWidth_in = newHeight_in * this.aspectRatio;
                } else {
                    newHeight_in = UNRESOLVED.safedivExcept(newWidth_in, this.aspectRatio, newHeight_in);
                }
                break;
        // bound size at page, using left/top margins already set
        maxWidth_in = this.wholePageWidth_in - this.printLeftMargin_in - this.printMinMarginRight_in;
        maxHeight_in = this.wholePageHeight_in - this.printTopMargin_in - this.printMinMarginBottom_in;
        if (newWidth_in > maxWidth_in) {
            newWidth_in = maxWidth_in;
            newHeight_in = UNRESOLVED.safedivExcept(newWidth_in, this.aspectRatio, newHeight_in);
        }
        if (newHeight_in > maxHeight_in) {
            newHeight_in = maxHeight_in;
            newWidth_in = newHeight_in * this.aspectRatio;
        }
        newRight_in = UNRESOLVED.max(this.printMinMarginRight_in, this.wholePageWidth_in - this.printLeftMargin_in - newWidth_in);
        newBottom_in = UNRESOLVED.max(this.printMinMarginBottom_in, this.wholePageHeight_in - this.printTopMargin_in - newHeight_in);
        // set values in edits
        this.setValue(this.printWidthEdit, newWidth_in);
        this.setValue(this.printHeightEdit, newHeight_in);
        this.setValue(this.printRightMarginEdit, newRight_in);
        this.setValue(this.printBottomMarginEdit, newBottom_in);
        this.updatePrintPreview();
    }
    
    // -------------------------------------------------------------------- interactions - printing panel 
    public void printCenterClick(TObject Sender) {
        this.setValue(this.printLeftMarginEdit, UNRESOLVED.max(this.printMinMarginLeft_in, this.wholePageWidth_in / 2.0 - this.printWidth_in / 2.0));
        this.setValue(this.printRightMarginEdit, UNRESOLVED.max(this.printMinMarginRight_in, this.wholePageWidth_in / 2.0 - this.printWidth_in / 2.0));
        this.setValue(this.printTopMarginEdit, UNRESOLVED.max(this.printMinMarginTop_in, this.wholePageHeight_in / 2.0 - this.printHeight_in / 2.0));
        this.setValue(this.printBottomMarginEdit, UNRESOLVED.max(this.printMinMarginBottom_in, this.wholePageHeight_in / 2.0 - this.printHeight_in / 2.0));
        if (this.printPreserveAspectRatio.Checked) {
            this.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged);
        } else {
            this.updatePrintPreview();
        }
    }
    
    public void suggestPrintSizeClick(TObject Sender) {
        float bestMargin_in = 0.0;
        float bestWidth_in = 0.0;
        float bestHeight_in = 0.0;
        float newWidth_in = 0.0;
        float newHeight_in = 0.0;
        float maxMinMargin_in = 0.0;
        
        // calculate best margin: for 10 inches, 1.0 inches, for 5 inches, 0.5 inches;
        // keep to multiples of 0.25 inches
        maxMinMargin_in = UNRESOLVED.max(this.printMinMarginLeft_in, UNRESOLVED.max(this.printMinMarginTop_in, UNRESOLVED.max(this.printMinMarginRight_in, this.printMinMarginBottom_in)));
        bestMargin_in = UNRESOLVED.max(maxMinMargin_in, intround(4.0 * UNRESOLVED.min(this.wholePageWidth_in, this.wholePageHeight_in) / 10.0) / 4.0);
        bestWidth_in = this.wholePageWidth_in - bestMargin_in * 2;
        bestHeight_in = this.wholePageHeight_in - bestMargin_in * 2;
        // preserve aspect ratio - reduce the larger dimension so it still fits on the page
        this.updateSelectionRectFromMainWindow();
        newHeight_in = bestHeight_in;
        newWidth_in = bestHeight_in * this.aspectRatio;
        if (newWidth_in > bestWidth_in) {
            newWidth_in = bestWidth_in;
            newHeight_in = UNRESOLVED.safedivExcept(bestWidth_in, this.aspectRatio, bestHeight_in);
        }
        // set original picture size to fit on page using printer resolution
        this.setValue(this.inchWidthEdit, newWidth_in);
        this.setValue(this.inchHeightEdit, newHeight_in);
        this.setValue(this.resolutionEdit, this.smallestPrintResolution_pxPin);
        this.calculatePixelsFromResolutionAndInches();
        // set print size same as picture size
        this.setValue(this.printWidthEdit, newWidth_in);
        this.setValue(this.printHeightEdit, newHeight_in);
        // center picture
        this.printCenterClick(this);
    }
    
    public void printUseWholePageClick(TObject Sender) {
        float borderThickness_in = 0.0;
        
        borderThickness_in = UNRESOLVED.safedivExcept(this.options.borderThickness, this.smallestPrintResolution_pxPin, 0);
        this.setValue(this.printLeftMarginEdit, this.printMinMarginLeft_in + borderThickness_in);
        this.setValue(this.printRightMarginEdit, this.printMinMarginRight_in + borderThickness_in);
        this.setValue(this.printTopMarginEdit, this.printMinMarginTop_in + borderThickness_in);
        this.setValue(this.printBottomMarginEdit, this.printMinMarginBottom_in + borderThickness_in);
        this.setValue(this.printWidthEdit, this.wholePageWidth_in - this.printLeftMargin_in - this.printRightMargin_in);
        this.setValue(this.printHeightEdit, this.wholePageHeight_in - this.printTopMargin_in - this.printBottomMargin_in);
        if (this.printPreserveAspectRatio.Checked) {
            // check new size for aspect ratio (if 'preserve aspect ratio' checked)
            this.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged);
        } else {
            this.updatePrintPreview();
        }
    }
    
    public void printPreserveAspectRatioClick(TObject Sender) {
        if (this.startingUp || this.sideEffect) {
            return;
        }
        if (this.printPreserveAspectRatio.Checked) {
            this.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged);
        }
    }
    
    // ----------------------------------------------------------------------------------------- buttons 
    public void bordersClick(TObject Sender) {
        TPrintBordersForm bordersForm = new TPrintBordersForm();
        
        bordersForm = uborders.TPrintBordersForm().create(this);
        if (bordersForm == null) {
            throw new GeneralException.create("Problem: Could not create print borders window.");
        }
        try {
            bordersForm.initializeWithOptions(this.options);
            if (bordersForm.ShowModal() == mrOK) {
                // just copy whole options, because you can't change this form while borders form is up
                this.options = bordersForm.options;
                this.updateBorderThickness();
                this.updatePrintPreview();
            }
        } finally {
            bordersForm.free;
        }
    }
    
    public void printSetupClick(TObject Sender) {
        this.PrintDialog.execute;
        this.updateForPrinterInfo();
        this.suggestPrintSizeClick(this);
    }
    
    public void CloseClick(TObject Sender) {
        String insertString = "";
        
        if ((this.colorType.ItemIndex == 0) && ((this.copySavePrintType == kSavingDrawingToBmp) || (this.copySavePrintType == kSavingDrawingToJpeg))) {
            // don't let them save the file as a device-dependent bitmap.
            MessageDialog("You cannot save a picture with the \"From screen\" color depth." + chr(13) + "Please change the color depth to another choice in the list.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            return;
        }
        if ((this.useSelectedPlants.Checked) && (UNRESOLVED.MainForm.selectedPlants.count <= 0)) {
            // don't let them finish with no plants
            MessageDialog("You chose \"selected\" for \"Draw which plants\", but no plants are selected." + chr(13) + "You should make another choice, or click Cancel and select some plants.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            return;
        }
        if (this.copySavePrintType != kSavingDrawingToJpeg) {
            if (this.megabytesOfMemoryNeeded > kTooManyMegabytesOfMemory) {
                switch (this.copySavePrintType) {
                    case kCopyingDrawing:
                        // warn about a really big operation
                        insertString = "copy to the clipboard";
                        break;
                    case kPrintingDrawing:
                        insertString = "print";
                        break;
                    case kSavingDrawingToBmp:
                        insertString = "save";
                        break;
                if (MessageDialog("You are about to " + insertString + " a " + UNRESOLVED.digitValueString(this.megabytesOfMemoryNeeded) + " MB bitmap." + chr(13) + "This could place stress on your system." + chr(13) + "We recommend closing any non-essential programs." + chr(13) + "Also, choosing fewer colors or a smaller picture will use less memory." + chr(13) + chr(13) + "To proceed, click OK. To go back and make changes, click Cancel.", mtWarning, {mbOK, mbCancel, }, 0) == delphi_compatability.IDCANCEL) {
                    return;
                }
            }
        }
        this.transferDirection = kTransferSave;
        this.transferFields();
        this.ModalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    // ----------------------------------------------------------- methods to get/set edit values 
    public void setValue(TEdit editBox, float newValue) {
        float maxWidth_in = 0.0;
        float maxHeight_in = 0.0;
        
        this.sideEffect = true;
        maxWidth_in = this.wholePageWidth_in - this.printMinMarginLeft_in - this.printMinMarginRight_in;
        maxHeight_in = this.wholePageHeight_in - this.printMinMarginTop_in - this.printMinMarginBottom_in;
        if (editBox == this.pixelWidthEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinPixels, UNRESOLVED.min(UNRESOLVED.kMaxPixels, newValue));
            this.pictureWidth_px = newValue;
        } else if (editBox == this.pixelHeightEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinPixels, UNRESOLVED.min(UNRESOLVED.kMaxPixels, newValue));
            this.pictureHeight_px = newValue;
        } else if (editBox == this.inchWidthEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinInches, UNRESOLVED.min(UNRESOLVED.kMaxInches, newValue));
            this.pictureWidth_in = newValue;
        } else if (editBox == this.inchHeightEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinInches, UNRESOLVED.min(UNRESOLVED.kMaxInches, newValue));
            this.pictureHeight_in = newValue;
        } else if (editBox == this.resolutionEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinResolution, UNRESOLVED.min(UNRESOLVED.kMaxResolution, newValue));
            this.pictureResolution_pxPin = newValue;
        } else if (editBox == this.printWidthEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinInches, UNRESOLVED.min(newValue, maxWidth_in));
            this.printWidth_in = newValue;
        } else if (editBox == this.printHeightEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinInches, UNRESOLVED.min(newValue, maxHeight_in));
            this.printHeight_in = newValue;
        } else if (editBox == this.printLeftMarginEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinInches, UNRESOLVED.min(newValue, maxWidth_in));
            this.printLeftMargin_in = newValue;
        } else if (editBox == this.printTopMarginEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinInches, UNRESOLVED.min(newValue, maxHeight_in));
            this.printTopMargin_in = newValue;
        } else if (editBox == this.printRightMarginEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinInches, UNRESOLVED.min(newValue, maxWidth_in));
            this.printRightMargin_in = newValue;
        } else if (editBox == this.printBottomMarginEdit) {
            newValue = UNRESOLVED.max(UNRESOLVED.kMinInches, UNRESOLVED.min(newValue, maxHeight_in));
            this.printBottomMargin_in = newValue;
        } else if (editBox == this.jpgCompressionEdit) {
            newValue = UNRESOLVED.max(1, UNRESOLVED.min(100, newValue));
            this.jpegCompression = newValue;
        }
        if (editBox.Tag == kEditBoxHasInteger) {
            editBox.Text = IntToStr(intround(newValue));
        } else if (editBox.Tag == kEditBoxHasFloat) {
            editBox.Text = floatStr(newValue);
        }
        this.sideEffect = false;
    }
    
    public float getValue(TEdit editBox) {
        result = 0.0;
        result = 0;
        if (editBox == this.pixelWidthEdit) {
            result = this.pictureWidth_px;
        } else if (editBox == this.pixelHeightEdit) {
            result = this.pictureHeight_px;
        } else if (editBox == this.inchWidthEdit) {
            result = this.pictureWidth_in;
        } else if (editBox == this.inchHeightEdit) {
            result = this.pictureHeight_in;
        } else if (editBox == this.resolutionEdit) {
            result = this.pictureResolution_pxPin;
        } else if (editBox == this.printWidthEdit) {
            result = this.printWidth_in;
        } else if (editBox == this.printHeightEdit) {
            result = this.printHeight_in;
        } else if (editBox == this.printLeftMarginEdit) {
            result = this.printLeftMargin_in;
        } else if (editBox == this.printTopMarginEdit) {
            result = this.printTopMargin_in;
        } else if (editBox == this.printRightMarginEdit) {
            result = this.printRightMargin_in;
        } else if (editBox == this.printBottomMarginEdit) {
            result = this.printBottomMargin_in;
        } else if (editBox == this.jpgCompressionEdit) {
            result = this.jpegCompression;
        }
        return result;
    }
    
    public float getEnteredValue(TEdit editBox) {
        result = 0.0;
        result = 0;
        try {
            if (editBox.Tag == kEditBoxHasInteger) {
                result = StrToInt(editBox.Text);
            } else if (editBox.Tag == kEditBoxHasFloat) {
                result = StrToFloat(editBox.Text);
            }
        } catch (exception e) {
            ShowMessage("Invalid value: " + e.message);
            result = 0;
        }
        return result;
    }
    
    // ------------------------------------------------------------------------- transfer functions 
    public short currentExportOption() {
        result = 0;
        result = UNRESOLVED.kIncludeSelectedPlants;
        if (this.useSelectedPlants.Checked) {
            result = UNRESOLVED.kIncludeSelectedPlants;
        } else if (this.useVisiblePlants.Checked) {
            result = UNRESOLVED.kIncludeVisiblePlants;
        } else if (this.useAllPlants.Checked) {
            result = UNRESOLVED.kIncludeAllPlants;
        } else if (this.useDrawingAreaContents.Checked) {
            result = UNRESOLVED.kIncludeDrawingAreaContents;
        }
        return result;
    }
    
    public String nameForCopySavePrintType(short aType) {
        result = "";
        result = "";
        switch (aType) {
            case kCopyingDrawing:
                result = "Copy";
                break;
            case kPrintingDrawing:
                result = "Print";
                break;
            case kSavingDrawingToBmp:
                result = "Save";
                break;
            case kSavingDrawingToJpeg:
                result = "Save";
                break;
        return result;
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
    
    public void transferSmallintEditBox(TEdit editBox, short value) {
        if (this.transferDirection == kTransferLoad) {
            // sets up vars at start
            this.setValue(editBox, value);
        } else if (this.transferDirection == kTransferSave) {
            if (value != StrToIntDef(editBox.Text, 0)) {
                this.optionsChanged = true;
            }
            value = StrToIntDef(editBox.Text, 0);
        }
        return value;
    }
    
    public void transferSingleEditBox(TEdit editBox, float value) {
        float newValue = 0.0;
        
        if (this.transferDirection == kTransferLoad) {
            // sets up vars at start
            this.setValue(editBox, value);
        } else if (this.transferDirection == kTransferSave) {
            try {
                newValue = StrToFloat(editBox.Text);
            } catch (Exception e) {
                newValue = value;
            }
            if (newValue != value) {
                this.optionsChanged = true;
            }
            value = newValue;
        }
        return value;
    }
    
    public void transferComboBox(TComboBox comboBox, short value) {
        if (this.transferDirection == kTransferLoad) {
            comboBox.ItemIndex = value;
        } else if (this.transferDirection == kTransferSave) {
            if (value != comboBox.ItemIndex) {
                this.optionsChanged = true;
            }
            value = comboBox.ItemIndex;
        }
        return value;
    }
    
    public void transferTPixelFormatComboBox(TComboBox comboBox, TPixelFormat value) {
        raise "method transferTPixelFormatComboBox had assigned to var parameter value not added to return; fixup manually"
        if (this.transferDirection == kTransferLoad) {
            if (value == delphi_compatability.TPixelFormat.pfCustom) {
                value = delphi_compatability.TPixelFormat.pfDevice;
            }
            comboBox.ItemIndex = ord(value);
        } else if (this.transferDirection == kTransferSave) {
            if (value != UNRESOLVED.TPixelFormat(comboBox.ItemIndex)) {
                this.optionsChanged = true;
            }
            value = UNRESOLVED.TPixelFormat(comboBox.ItemIndex);
        }
    }
    
    public void colorTypeDrawItem(TWinControl Control, int index, TRect Rect, TOwnerDrawState State) {
        boolean selected = false;
         cText = [0] * (range(0, 255 + 1) + 1);
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        selected = (delphi_compatability.TOwnerDrawStateType.odSelected in State);
        this.colorType.Canvas.Font = this.colorType.Font;
        if (selected) {
            this.colorType.Canvas.Brush.Color = UNRESOLVED.clHighlight;
            this.colorType.Canvas.Font.Color = UNRESOLVED.clHighlightText;
        } else {
            this.colorType.Canvas.Brush.Color = this.colorType.Color;
            this.colorType.Canvas.Font.Color = UNRESOLVED.clBtnText;
        }
        if ((index == 0) && ((this.copySavePrintType == kSavingDrawingToBmp) || (this.copySavePrintType == kSavingDrawingToJpeg))) {
            this.colorType.Canvas.Font.Color = UNRESOLVED.clBtnShadow;
        }
        this.colorType.Canvas.FillRect(Rect);
        UNRESOLVED.strPCopy(cText, this.colorType.Items[index]);
        // margin for text 
        Rect.left = Rect.left + 2;
        UNRESOLVED.drawText(this.colorType.Canvas.Handle, cText, len(cText), Rect, delphi_compatability.DT_LEFT);
    }
    
    public void helpButtonClick(TObject Sender) {
        switch (this.copySavePrintType) {
            case kCopyingDrawing:
                delphi_compatability.Application.HelpJump("Copying_pictures");
                break;
            case kPrintingDrawing:
                delphi_compatability.Application.HelpJump("Printing_pictures");
                break;
            case kSavingDrawingToBmp:
                delphi_compatability.Application.HelpJump("Saving_pictures");
                break;
            case kSavingDrawingToJpeg:
                delphi_compatability.Application.HelpJump("Saving_pictures");
                break;
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
}
