unit ubmpopt;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Spin, ExtCtrls, Buttons,
  udomain, updform;

type
  TBitmapOptionsForm = class(PdForm)
    Close: TButton;
    cancel: TButton;
    printBox: TGroupBox;
    outputBox: TGroupBox;
    resolutionLabel: TLabel;
    sizePixelsLabel: TLabel;
    sizeInchesLabel: TLabel;
    inchWidthEdit: TEdit;
    inchHeightEdit: TEdit;
    colorType: TComboBox;
    colorsLabel: TLabel;
    printSetup: TButton;
    printPreserveAspectRatio: TCheckBox;
    plantsBox: TGroupBox;
    useSelectedPlants: TRadioButton;
    useAllPlants: TRadioButton;
    useDrawingAreaContents: TRadioButton;
    useVisiblePlants: TRadioButton;
    resolutionEdit: TEdit;
    pixelWidthEdit: TEdit;
    pixelHeightEdit: TEdit;
    resolutionSpin: TSpinButton;
    pixelWidthSpin: TSpinButton;
    pixelHeightSpin: TSpinButton;
    inchHeightSpin: TSpinButton;
    inchWidthSpin: TSpinButton;
    PrintDialog: TPrintDialog;
    preserveAspectRatio: TCheckBox;
    inchHeightLabel: TLabel;
    pixelWidthLabel: TLabel;
    pixelHeightLabel: TLabel;
    borders: TButton;
    currentStuffPanel: TPanel;
    selectedImageInfoLabel: TLabel;
    screenInfoLabel: TLabel;
    printerOrFileTypeInfoLabel: TLabel;
    sizeLabel: TLabel;
    printWidthLabel: TLabel;
    printWidthEdit: TEdit;
    printWidthSpin: TSpinButton;
    printHeightLabel: TLabel;
    printHeightEdit: TEdit;
    printHeightSpin: TSpinButton;
    marginsLabel: TLabel;
    printLeftMarginLabel: TLabel;
    printTopMarginLabel: TLabel;
    printLeftMarginEdit: TEdit;
    printTopMarginEdit: TEdit;
    printLeftMarginSpin: TSpinButton;
    printTopMarginSpin: TSpinButton;
    printRightMarginLabel: TLabel;
    printBottomMarginLabel: TLabel;
    printRightMarginEdit: TEdit;
    printBottomMarginEdit: TEdit;
    printRightMarginSpin: TSpinButton;
    printBottomMarginSpin: TSpinButton;
    printCenter: TButton;
    printUseWholePage: TButton;
    suggestPrintSize: TButton;
    printImagePanel: TPanel;
    wholePageImage: TImage;
    inchWidthLabel: TLabel;
    helpButton: TSpeedButton;
    memoryUseInfoLabel: TLabel;
    jpgCompressionLabel: TLabel;
    jpgCompressionEdit: TEdit;
    jpgCompressionSpin: TSpinButton;
    procedure exitEditBox(sender: TObject);
    procedure selectionChoiceClick(sender: TObject);
    procedure spinUp(sender: TObject);
    procedure spinDown(sender: TObject);
    procedure printSetupClick(Sender: TObject);
    procedure CloseClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure preserveAspectRatioClick(Sender: TObject);
    procedure printCenterClick(Sender: TObject);
    procedure printUseWholePageClick(Sender: TObject);
    procedure printPreserveAspectRatioClick(Sender: TObject);
    procedure bordersClick(Sender: TObject);
    procedure suggestCopySizeClick(Sender: TObject);
    procedure suggestPrintSizeClick(Sender: TObject);
    procedure colorTypeDrawItem(Control: TWinControl; Index: Integer;
      Rect: TRect; State: TOwnerDrawState);
    procedure helpButtonClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure colorTypeChange(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    options: BitmapOptionsStructure;
    transferDirection: smallint;
    optionsChanged: boolean;
    copySavePrintType: smallint;
    startingUp, sideEffect: boolean;
    selectionRectFromMainWindow: TRect;
    printPageWidth_in, printPageHeight_in: single;
    wholePageWidth_in, wholePageHeight_in: single;
    printMinMarginLeft_in, printMinMarginTop_in, printMinMarginRight_in, printMinMarginBottom_in: single;
    pictureWidth_px, pictureHeight_px: single;
    pictureResolution_pxPin, smallestPrintResolution_pxPin: single;
    pictureWidth_in, pictureHeight_in: single;
    printWidth_in, printHeight_in: single;
    printLeftMargin_in, printTopMargin_in, printRightMargin_in, printBottomMargin_in: single;
    jpegCompression: single;
    aspectRatio: single;
    megabytesOfMemoryNeeded: single;
    procedure initializeWithTypeAndOptions(aType: smallint; anOptions: BitmapOptionsStructure);
    function nameForCopySavePrintType(aType: smallint): string;
    function currentExportOption: smallint;
    procedure updateForPrinterInfo;
    procedure transferFields;
    procedure transferCheckBox(checkBox: TCheckBox; var value: boolean);
    procedure transferSmallintEditBox(editBox: TEdit; var value: smallint);
    procedure transferSingleEditBox(editBox: TEdit; var value: single);
    procedure transferComboBox(comboBox: TComboBox; var value: smallint);
    procedure transferTPixelFormatComboBox(comboBox: TComboBox; var value: TPixelFormat);
    procedure adjustValue(sender: TObject; spin: smallint);
    procedure adjustEditBoxValueForSpin(sender: TObject; spin: smallint);
    procedure maintainAspectRatioPixelsAndInches(editBox: TEdit);
    function heightForWidthAndAspectRatio(width, ratio: single): single;
    function widthForHeightAndAspectRatio(height, ratio: single): single;
    procedure calculatePixelsFromResolutionAndInches;
    procedure calculateInchesFromResolutionAndPixels;
    procedure calculateResolutionFromInchesAndPixels;
    procedure setValue(editBox: TEdit; newValue: single);
    function getValue(editBox: TEdit): single;
    function getEnteredValue(editBox: TEdit): single;
    procedure updateForImageSelection;
    procedure updateSelectionRectFromMainWindow;
    procedure resizePrintBasedOnAspectRatio(whatWasChanged: smallint);
    procedure updatePrintPreview;
    procedure changePrintMarginsToFitPrintSize;
    procedure changePrintSizeToFitPrintMargins(editBox: TEdit);
    procedure updateBorderThickness;
    procedure reportOnMemoryNeeded;
    procedure calculateMegabytesOfMemoryNeededConsideringColorBitsAndResolution;
  end;

const
  kCopyingDrawing = 0;
  kPrintingDrawing = 1;
  kSavingDrawingToBmp = 2;
  kSavingDrawingToJpeg = 3;

implementation

{$R *.DFM}

uses Printers, usupport, umath, umain, uborders, udebug;

const
  kTransferLoad = 1; kTransferSave = 2;
  kSpinNone = 0; kSpinUp = 1; kSpinDown = -1;
  kEditIsInteger = 0; kEditIsFloat = 1;
  kWidthWasChanged = 0; kHeightWasChanged = 1; kHeightAndWidthWereChanged = 2;
  kEditBoxHasInteger = 0; kEditBoxHasFloat = 1;
  kTooManyMegabytesOfMemory = 10.0; 

function floatStr(value: single): string;
  begin
  result := floatToStrF(value, ffFixed, 7, 2);
  end;

{ ----------------------------------------------------------------------------------------- initialize }
procedure TBitmapOptionsForm.initializeWithTypeAndOptions(aType: smallint; anOptions: BitmapOptionsStructure);
  var
    displayString: string;
  begin
  startingUp := true;
  options := anOptions;
  copySavePrintType := aType;
  displayString := self.nameForCopySavePrintType(copySavePrintType);
  if copySavePrintType = kPrintingDrawing then
    self.updateForPrinterInfo; // must be done before transfer
  transferDirection := kTransferLoad;
	self.transferFields;
  self.updateForImageSelection;
  self.maintainAspectRatioPixelsAndInches(pixelWidthEdit);
  self.updateBorderThickness;
  printSetup.visible := copySavePrintType = kPrintingDrawing;
  borders.visible := copySavePrintType = kPrintingDrawing;
  printerOrFileTypeInfoLabel.visible := copySavePrintType <> kCopyingDrawing;
  if copySavePrintType = kSavingDrawingToJpeg then
    begin
    jpgCompressionLabel.visible := true;
    colorsLabel.visible := false;
    with jpgCompressionLabel do setBounds(colorsLabel.left, colorsLabel.top, width, height);
    jpgCompressionEdit.visible := true;
    colorType.visible := false;
    with jpgCompressionEdit do setBounds(colorType.left, colorType.top, width, height);
    jpgCompressionSpin.visible := true;
    with jpgCompressionSpin do setBounds(jpgCompressionEdit.left + jpgCompressionEdit.width + 4,
        jpgCompressionEdit.top, width, height);
    end;
  if (copySavePrintType = kSavingDrawingToBmp) or (copySavePrintType = kSavingDrawingToJpeg) then
    begin
    if (copySavePrintType = kSavingDrawingToBmp) then
      printerOrFileTypeInfoLabel.caption := 'Saving to: BMP'
    else if (copySavePrintType = kSavingDrawingToJpeg) then
      printerOrFileTypeInfoLabel.caption := 'Saving to: JPEG';
    end;
  if copySavePrintType = kPrintingDrawing then
    begin
    self.clientHeight := printBox.top + printBox.height;
    self.suggestPrintSizeClick(self);
    end
  else
    self.clientHeight := outputBox.top + outputBox.height;
  case copySavePrintType of
    kCopyingDrawing: close.caption := '&Copy';
    kPrintingDrawing: close.caption := '&Print';
    kSavingDrawingToBmp, kSavingDrawingToJpeg: close.caption := '&Save';
	  end;
  helpButton.hint := 'Get help with setting ' + lowerCase(displayString) + ' picture options.';
  cancel.hint := 'Close this window and don''t ' + lowerCase(displayString) + ' a picture.';
  close.hint := displayString + ' the selected picture using the options specified in this window.';
  startingUp := false;
  end;

procedure TBitmapOptionsForm.updateForPrinterInfo;
  var
    xResolution_pixelsPerInch, yResolution_pixelsPerInch: integer;
    portraitOrLandscape: string;
    printerDC: HDC;
    printerColorBits, printerColors: integer;
  begin
  xResolution_pixelsPerInch := GetDeviceCaps(Printer.Handle, LogPixelsX);
  yResolution_pixelsPerInch := GetDeviceCaps(Printer.Handle, LogPixelsY);
  smallestPrintResolution_pxPin := intMin(xResolution_pixelsPerInch, yResolution_pixelsPerInch);
  printPageWidth_in := safedivExcept(Printer.pageWidth - 1,  xResolution_pixelsPerInch, 0);
  printPageHeight_in := safedivExcept(Printer.pageHeight - 1,  yResolution_pixelsPerInch, 0);
  wholePageWidth_in := safedivExcept(GetDeviceCaps(Printer.Handle, PHYSICALWIDTH), xResolution_pixelsPerInch, 0);
  wholePageHeight_in := safedivExcept(GetDeviceCaps(Printer.Handle, PHYSICALHEIGHT), xResolution_pixelsPerInch, 0);
  printMinMarginLeft_in := safedivExcept(GetDeviceCaps(Printer.Handle, PhysicalOffsetX), xResolution_pixelsPerInch, 0);
  printMinMarginTop_in := safedivExcept(GetDeviceCaps(Printer.Handle, PhysicalOffsetY), xResolution_pixelsPerInch, 0);
  printMinMarginRight_in := wholePageWidth_in - printPageWidth_in - printMinMarginLeft_in;
  printMinMarginBottom_in := wholePageHeight_in - printPageHeight_in - printMinMarginTop_in;
  if Printer.orientation = poPortrait then
    portraitOrLandscape := 'Portrait'
  else
    portraitOrLandscape := 'Landscape';
  printerDC := CreateCompatibleDC(Printer.Handle);
  try
    printerColorBits := (GetDeviceCaps(printerDC, BITSPIXEL) * GetDeviceCaps(printerDC, PLANES));
  finally
    ReleaseDC(0, printerDC);
    DeleteDC(printerDC);
  end;
  if printerColorBits <> 32 then
    printerColors := 1 shl printerColorBits
  else
    printerColors := round(power(2.0, printerColorBits));
  printerOrFileTypeInfoLabel.caption := 'Printer:  '
   + intToStr(GetDeviceCaps(Printer.Handle, LogPixelsX)) + ' x '
   + intToStr(GetDeviceCaps(Printer.Handle, LogPixelsY)) + ' pixels/inch, '
   + intToStr(printerColors) + ' colors (' + intToStr(printerColorBits) + ' bits)';
  //+ portraitOrLandscape;
  //printerInfoLabel.hint := 'Printer name: ' + Printer.Printers[Printer.printerIndex];
  self.updatePrintPreview;
  end;

procedure TBitmapOptionsForm.updateForImageSelection;
  var
    pixelWidth, pixelHeight, screenColorBits: integer;
    screenColors: longint;
    inchWidth, inchHeight: single;
    screenDC: HDC;
    megabytesNeeded: single;
  begin
  self.updateSelectionRectFromMainWindow;
  // fill in labels
  pixelWidth := rWidth(selectionRectFromMainWindow);
  pixelHeight := rHeight(selectionRectFromMainWindow);
  inchWidth := safedivExcept(pixelWidth, Screen.pixelsPerInch, 0);
  inchHeight := safedivExcept(pixelHeight, Screen.pixelsPerInch, 0);
  selectedImageInfoLabel.caption := 'Selection:  '
    + intToStr(pixelWidth) + ' x ' + intToStr(pixelHeight) + ' pixels,  '
    + floatStr(inchWidth) + ' x ' + floatStr(inchHeight) + ' inches';
  screenDC := GetDC(0);
  try
    screenColorBits := (GetDeviceCaps(screenDC, BITSPIXEL) * GetDeviceCaps(screenDC, PLANES));
  finally
    ReleaseDC(0, screenDC);
  end;
  if screenColorBits <> 32 then
    begin
    screenColors := 1 shl screenColorBits;
    screenInfoLabel.caption := 'Screen:  ' + intToStr(Screen.pixelsPerInch) + ' pixels/inch,  '
      + intToStr(screenColors) + ' colors (' + intToStr(screenColorBits) + ' bits)'
    end
  else
    begin
    screenInfoLabel.caption := 'Screen:  ' + intToStr(Screen.pixelsPerInch) + ' pixels/inch,  '
      + 'true color (' + intToStr(screenColorBits) + ' bits)'
    end;
  // used to be only in suggest size button, now doing automatically
  setValue(inchWidthEdit, inchWidth);
  setValue(inchHeightEdit, inchHeight);
  self.calculatePixelsFromResolutionAndInches;
  if copySavePrintType = kPrintingDrawing then
    begin
    self.suggestPrintSizeClick(self);
    self.updatePrintPreview;
    end;
  self.reportOnMemoryNeeded;
  end;

procedure TBitmapOptionsForm.reportOnMemoryNeeded;
  begin
  // report memory needed -- do after calculating resolution-affected size
  // make no size estimation for JPG
  if copySavePrintType = kSavingDrawingToJpeg then
    begin
    memoryUseInfoLabel.visible := false;
    exit;
    end;
  self.calculatePixelsFromResolutionAndInches;
  self.calculateMegabytesOfMemoryNeededConsideringColorBitsAndResolution;
  if megabytesOfMemoryNeeded < 1.0 then
    memoryUseInfoLabel.caption := 'Estimated memory needed: ' + digitValueString(megabytesOfMemoryNeeded * 1024) + ' K'
  else
    memoryUseInfoLabel.caption := 'Estimated memory needed: ' + digitValueString(megabytesOfMemoryNeeded) + ' MB';
  if megabytesOfMemoryNeeded > kTooManyMegabytesOfMemory then
    memoryUseInfoLabel.font.style := [fsBold]
  else
    memoryUseInfoLabel.font.style := [];
  end;

procedure TBitmapOptionsForm.calculateMegabytesOfMemoryNeededConsideringColorBitsAndResolution;
  var
    colorBits: smallint;
    screenDC: HDC;
    outputPixelWidth, outputPixelHeight: single;
  begin
  outputPixelWidth := pictureWidth_in * pictureResolution_pxPin;
  outputPixelHeight := pictureHeight_in * pictureResolution_pxPin;
  colorBits := 0;
  case colorType.itemIndex of
    Integer(pfDevice):
      begin
      screenDC := GetDC(0);
      try
        colorBits := (GetDeviceCaps(screenDC, BITSPIXEL) * GetDeviceCaps(screenDC, PLANES));
      finally
       ReleaseDC(0, screenDC);
      end;
      end;
    Integer(pf1bit): colorBits := 1;
    Integer(pf4bit): colorBits := 4;
    Integer(pf8bit): colorBits := 8;
    Integer(pf15bit): colorBits := 15;
    Integer(pf16bit): colorBits := 16;
    Integer(pf24bit): colorBits := 24;
    Integer(pf32bit): colorBits := 32;
    end;
  self.megabytesOfMemoryNeeded := (1.0 * outputPixelWidth * outputPixelHeight
    * (colorBits / 8) + sizeOf(TBitmapInfo)) / (1024 * 1024);
  end;

procedure TBitmapOptionsForm.updateSelectionRectFromMainWindow;
  var
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean;
  begin
  excludeInvisiblePlants := not useAllPlants.checked;
  excludeNonSelectedPlants := useSelectedPlants.checked;
  if useDrawingAreaContents.checked then
    self.selectionRectFromMainWindow := rect(0, 0,
        MainForm.drawingPaintBox.width, MainForm.drawingPaintBox.height)
  else
    self.selectionRectFromMainWindow := domain.plantManager.combinedPlantBoundsRects(MainForm.selectedPlants,
        excludeInvisiblePlants, excludeNonSelectedPlants);
  aspectRatio := safedivExcept(rWidth(selectionRectFromMainWindow), rHeight(selectionRectFromMainWindow), 1.0);
  end;

procedure TBitmapOptionsForm.updatePrintPreview;
  var
    scaleX_pxPin, scaleY_pxPin, scale_pxPin, borderThickness_in: single;
    availableWidth_px, availableHeight_px: smallint;
    marginRect: TRect;
  begin
  availableWidth_px := sizeLabel.left - wholePageImage.left - 10;
  availableHeight_px := printBox.height - wholePageImage.top - 10;
  scaleX_pxPin := safedivExcept(1.0 * availableWidth_px, wholePageWidth_in, 5);
  scaleY_pxPin := safedivExcept(1.0 * availableHeight_px, wholePageHeight_in, 5);
  scale_pxPin := min(scaleX_pxPin, scaleY_pxPin);
  wholePageImage.width := round(wholePageWidth_in * scale_pxPin);
  wholePageImage.height := round(wholePageHeight_in * scale_pxPin);
  if (wholePageImage.picture.bitmap.width <> wholePageImage.width)
      or (wholePageImage.picture.bitmap.height <> wholePageImage.height) then
    try
      wholePageImage.picture.bitmap.width := wholePageImage.width;
      wholePageImage.picture.bitmap.height := wholePageImage.height;
    except
      wholePageImage.picture.bitmap.width := 1;
      wholePageImage.picture.bitmap.height := 1;
    end;
  with marginRect do
    begin
    left := round(printMinMarginLeft_in * scale_pxPin);
    top := round(printMinMarginTop_in * scale_pxPin);
    // subtract 1 from right and bottom because last pixel is not drawn
    right := wholePageImage.width - round(printMinMarginRight_in * scale_pxPin) - 1;
    bottom := wholePageImage.height - round(printMinMarginBottom_in * scale_pxPin) - 1;
    end;
  with wholePageImage.picture.bitmap.canvas, marginRect do
    begin
    brush.color := clWindow;
    fillRect(rect(0, 0, wholePageImage.width, wholePageImage.height));
    brush.style := bsClear;
    pen.color := clBtnShadow;
    moveTo(0, top);     lineTo(wholePageImage.width, top);
    moveTo(left, 0);    lineTo(left, wholePageImage.height);
    moveTo(right, 0);   lineTo(right, wholePageImage.height);
    moveTo(0, bottom);  lineTo(wholePageImage.width, bottom);
    pen.style := psSolid;
    rectangle(0, 0, wholePageImage.width, wholePageImage.height);
    end;
  borderThickness_in := safedivExcept(options.borderThickness, smallestPrintResolution_pxPin, 0);
  with printImagePanel do setBounds(
    round(wholePageImage.left + (printLeftMargin_in - borderThickness_in) * scale_pxPin),
    round(wholePageImage.top + (printTopMargin_in - borderThickness_in) * scale_pxPin),
    round((printWidth_in + borderThickness_in * 2) * scale_pxPin),
    round((printHeight_in + borderThickness_in * 2) * scale_pxPin));
  end;

procedure TBitmapOptionsForm.updateBorderThickness;
  begin
  with options do
    begin
    borderThickness := 0;
    borderGap := 0;
    if printBorderInner then
      begin
      borderGap := round(printBorderWidthInner * 2.5); // cfk the 2.5 is arbitrary
      inc(borderThickness, printBorderWidthInner + borderGap);
      end;
    if options.printBorderOuter then
      inc(borderThickness, printBorderWidthOuter);
    end;
  end;

{ ----------------------------------------------------------------------------------------- transfer }
procedure TBitmapOptionsForm.transferFields;
  begin
  // plantBox
  if transferDirection = kTransferLoad then
    begin
    case options.exportType of
      kIncludeSelectedPlants: useSelectedPlants.checked := true;
      kIncludeVisiblePlants: useVisiblePlants.checked := true;
      kIncludeAllPlants: useAllPlants.checked := true;
      kIncludeDrawingAreaContents: useDrawingAreaContents.checked := true;
      end;
    end
  else if transferDirection = kTransferSave then
    options.exportType := self.currentExportOption;
  // output
  if copySavePrintType <> kSavingDrawingToJpeg then
    self.transferTPixelFormatComboBox(colorType, options.colorType);
  self.transferSmallintEditBox(resolutionEdit, options.resolution_pixelsPerInch);
  self.transferSmallintEditBox(pixelWidthEdit, options.width_pixels);
  self.transferSmallintEditBox(pixelHeightEdit, options.height_pixels);
  self.transferSingleEditBox(inchWidthEdit, options.width_in);
  self.transferSingleEditBox(inchHeightEdit, options.height_in);
  self.transferCheckBox(preserveAspectRatio, options.preserveAspectRatio);
  if copySavePrintType = kSavingDrawingToJpeg then
    self.transferSmallintEditBox(jpgCompressionEdit, options.jpegCompressionRatio);
  // printing
  if copySavePrintType <> kPrintingDrawing then exit;
  self.transferCheckBox(printPreserveAspectRatio, options.printPreserveAspectRatio);
  self.transferSingleEditBox(printWidthEdit, options.printWidth_in);
  self.transferSingleEditBox(printHeightEdit, options.printHeight_in);
  self.transferSingleEditBox(printLeftMarginEdit, options.printLeftMargin_in);
  self.transferSingleEditBox(printTopMarginEdit, options.printTopMargin_in);
  self.transferSingleEditBox(printRightMarginEdit, options.printRightMargin_in);
  self.transferSingleEditBox(printBottomMarginEdit, options.printBottomMargin_in);
  end;

{ ----------------------------------------------------------------------------------------- interactions-first panel }
procedure TBitmapOptionsForm.selectionChoiceClick(sender: TObject);
  begin
  if startingUp or sideEffect then exit;
  self.updateForImageSelection;
  end;

procedure TBitmapOptionsForm.preserveAspectRatioClick(Sender: TObject);
  begin
  if startingUp or sideEffect then exit;
  // arbitrarily picked pixelWidthEdit here
  if preserveAspectRatio.checked then
    self.maintainAspectRatioPixelsAndInches(pixelWidthEdit);
  end;

procedure TBitmapOptionsForm.colorTypeChange(Sender: TObject);
  begin
  if startingUp or sideEffect then exit;
  self.updateForImageSelection;
  end;

{ ----------------------------------------------------------------------------------------- interactions-second panel }
procedure TBitmapOptionsForm.exitEditBox(sender: TObject);
  begin
  self.adjustValue(sender, kSpinNone);
  end;

procedure TBitmapOptionsForm.spinUp(sender: TObject);
  begin
  self.adjustValue(sender, kSpinUp);
  end;

procedure TBitmapOptionsForm.spinDown(sender: TObject);
  begin
  self.adjustValue(sender, kSpinDown);
  end;

procedure TBitmapOptionsForm.adjustValue(sender: TObject; spin: smallint);
  var
    editBox: TEdit;
  begin
  if startingUp or sideEffect then exit;
  editBox := nil;
  // if spin button clicked, adjust corresponding edit (focusControl)
  if (sender is TSpinButton) then
    self.adjustEditBoxValueForSpin(sender, spin);
  // get edit box
  if (sender is TEdit) then
    editBox := sender as TEdit
  else if (sender is TSpinButton) then
    editBox := (sender as TSpinButton).focusControl as TEdit;
  if editBox = nil then exit;
  // use set method to check edit box entry against bounds
  setValue(editBox, getEnteredValue(editBox));
  // if image width/height changed, maintain aspect ratio
  if preserveAspectRatio.checked then
    if (editBox = inchWidthEdit) or (editBox = inchHeightEdit)
        or (editBox = pixelWidthEdit) or (editBox = pixelHeightEdit) then
      self.maintainAspectRatioPixelsAndInches(editBox);
  // if print width/height changed, maintain printing aspect ratio
  if printPreserveAspectRatio.checked then
    if (editBox = printWidthEdit) or (editBox = printHeightEdit) then
      begin
      if editBox = printWidthEdit then
        self.resizePrintBasedOnAspectRatio(kWidthWasChanged)
      else
        self.resizePrintBasedOnAspectRatio(kHeightWasChanged);
      end;
  // interaction between image inches, pixels, resolution
  if (editBox = inchWidthEdit) or (editBox = inchHeightEdit) or (editBox = resolutionEdit) then
    self.reportOnMemoryNeeded
  else if (editBox = pixelWidthEdit) or (editBox = pixelHeightEdit) then
    self.reportOnMemoryNeeded
  // interaction between print size and margins
  else if (editBox = printWidthEdit) or (editBox = printHeightEdit) then
    self.changePrintMarginsToFitPrintSize
  else if (editBox = printLeftMarginEdit) or (editBox = printTopMarginEdit)
      or (editBox = printRightMarginEdit) or (editBox = printBottomMarginEdit) then
    self.changePrintSizeToFitPrintMargins(editBox);
  end;

procedure TBitmapOptionsForm.adjustEditBoxValueForSpin(sender: TObject; spin: smallint);
  var
    editBox: TEdit;
    newValue: single;
  begin
  if (sender = nil) or (not (sender is TSpinButton)) then exit;
  editBox := nil;
  editBox := (sender as TSpinButton).focusControl as TEdit;
  if editBox = nil then exit;
  // edit tag is 1 if float
  // spin tag is spin increment * 100 (10 for floats (0.1), 1000 for ints (10))
  newValue := 0;
  if (sender as TSpinButton).focusControl.tag = kEditIsFloat then
    newValue := getValue(editBox) + 1.0 * (sender as TSpinButton).tag / 100 * spin
  else
    newValue := getValue(editBox) + (sender as TSpinButton).tag div 100 * spin;
  setValue(editBox, newValue);
  end;

procedure TBitmapOptionsForm.maintainAspectRatioPixelsAndInches(editBox: TEdit);
  begin
  if (editBox = inchWidthEdit) then
    setValue(inchHeightEdit, heightForWidthAndAspectRatio(pictureWidth_in, aspectRatio))
  else if (editBox = inchHeightEdit) then
    setValue(inchWidthEdit, widthForHeightAndAspectRatio(pictureHeight_in, aspectRatio))
  else if (editBox = pixelWidthEdit) then
    setValue(pixelHeightEdit, heightForWidthAndAspectRatio(pictureWidth_px, aspectRatio))
  else if (editBox = pixelHeightEdit) then
    setValue(pixelWidthEdit, widthForHeightAndAspectRatio(pictureHeight_px, aspectRatio));
  end;

function TBitmapOptionsForm.heightForWidthAndAspectRatio(width, ratio: single): single;
  begin
  result := safedivExcept(width, ratio, 0);
  end;

function TBitmapOptionsForm.widthForHeightAndAspectRatio(height, ratio: single): single;
  begin
  result := height * ratio;
  end;

procedure TBitmapOptionsForm.calculatePixelsFromResolutionAndInches;
  begin
  setValue(pixelWidthEdit, pictureWidth_in * pictureResolution_pxPin);
  setValue(pixelHeightEdit, pictureHeight_in * pictureResolution_pxPin);
  end;

procedure TBitmapOptionsForm.calculateInchesFromResolutionAndPixels;
  begin
  setValue(inchWidthEdit, safedivExcept(1.0 * pictureWidth_px, 1.0 * pictureResolution_pxPin, 0));
  setValue(inchHeightEdit, safedivExcept(1.0 * pictureHeight_px, 1.0 * pictureResolution_pxPin, 0));
  end;

procedure TBitmapOptionsForm.calculateResolutionFromInchesAndPixels;
  var
    xRes, yRes: single;
  begin
  xRes := safedivExcept(pictureWidth_px, pictureWidth_in, Screen.PixelsPerInch);
  yRes := safedivExcept(pictureHeight_px, pictureHeight_in, Screen.PixelsPerInch);
  setValue(resolutionEdit, round(min(xRes, yRes)));
  self.calculatePixelsFromResolutionAndInches;
  end;

procedure TBitmapOptionsForm.suggestCopySizeClick(Sender: TObject);
  begin
  self.updateSelectionRectFromMainWindow;
  setValue(pixelWidthEdit, rWidth(selectionRectFromMainWindow));
  setValue(pixelHeightEdit, rHeight(selectionRectFromMainWindow));
  self.calculateInchesFromResolutionAndPixels;
  end;

{ -------------------------------------------------------------------- calculations of print size/margins }
procedure TBitmapOptionsForm.changePrintMarginsToFitPrintSize;
  begin
  setValue(printRightMarginEdit, max(0, wholePageWidth_in - printLeftMargin_in - printWidth_in));
  setValue(printBottomMarginEdit, max(0, wholePageHeight_in - printTopMargin_in - printHeight_in));
  if printPreserveAspectRatio.checked then
    self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
  else
    self.updatePrintPreview;
  end;

procedure TBitmapOptionsForm.changePrintSizeToFitPrintMargins(editBox: TEdit);
  begin
  // keep print size same to start, just offset other margin
  if editBox = printLeftMarginEdit then
    setValue(printRightMarginEdit, max(0, wholePageWidth_in - printLeftMargin_in - printWidth_in))
  else if editBox = printRightMarginEdit then
    setValue(printLeftMarginEdit, max(0, wholePageWidth_in - printRightMargin_in - printWidth_in))
  else if editBox = printTopMarginEdit then
    setValue(printBottomMarginEdit, max(0, wholePageHeight_in - printTopMargin_in - printHeight_in))
  else if editBox = printBottomMarginEdit then
    setValue(printTopMarginEdit, max(0, wholePageHeight_in - printBottomMargin_in - printHeight_in));
  // now set print size
  setValue(printWidthEdit, max(0, wholePageWidth_in - printRightMargin_in - printLeftMargin_in));
  setValue(printHeightEdit, max(0, wholePageHeight_in - printBottomMargin_in - printTopMargin_in));
  // now check aspect ratio
  if printPreserveAspectRatio.checked then
    self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
  else
    self.updatePrintPreview;
  end;

procedure TBitmapOptionsForm.resizePrintBasedOnAspectRatio(whatWasChanged: smallint);
  var
    newWidth_in, newHeight_in, newRight_in, newBottom_in, maxWidth_in, maxHeight_in: single;
  begin
  newWidth_in := printWidth_in;
  newHeight_in := printHeight_in;
  self.updateSelectionRectFromMainWindow;
  case whatWasChanged of
    kHeightWasChanged: newWidth_in := newHeight_in * aspectRatio;
    kWidthWasChanged: newHeight_in := safedivExcept(newWidth_in, aspectRatio, newHeight_in);
    kHeightAndWidthWereChanged:
      begin
      if newWidth_in > newHeight_in then
        newWidth_in := newHeight_in * aspectRatio
      else
        newHeight_in := safedivExcept(newWidth_in, aspectRatio, newHeight_in);
      end;
    end;
  // bound size at page, using left/top margins already set
  maxWidth_in := wholePageWidth_in - printLeftMargin_in - printMinMarginRight_in;
  maxHeight_in := wholePageHeight_in - printTopMargin_in - printMinMarginBottom_in;
  if newWidth_in > maxWidth_in then
    begin
    newWidth_in := maxWidth_in;
    newHeight_in := safedivExcept(newWidth_in, aspectRatio, newHeight_in);
    end;
  if newHeight_in > maxHeight_in then
    begin
    newHeight_in := maxHeight_in;
    newWidth_in := newHeight_in * aspectRatio;
    end;
  newRight_in := max(printMinMarginRight_in, wholePageWidth_in - printLeftMargin_in - newWidth_in);
  newBottom_in := max(printMinMarginBottom_in, wholePageHeight_in - printTopMargin_in - newHeight_in);
  // set values in edits
  setValue(printWidthEdit, newWidth_in);
  setValue(printHeightEdit, newHeight_in);
  setValue(printRightMarginEdit, newRight_in);
  setValue(printBottomMarginEdit, newBottom_in);
  self.updatePrintPreview;
  end;

{ -------------------------------------------------------------------- interactions - printing panel }
procedure TBitmapOptionsForm.printCenterClick(Sender: TObject);
  begin
  setValue(printLeftMarginEdit, max(printMinMarginLeft_in, wholePageWidth_in / 2.0 - printWidth_in / 2.0));
  setValue(printRightMarginEdit, max(printMinMarginRight_in, wholePageWidth_in / 2.0 - printWidth_in / 2.0));
  setValue(printTopMarginEdit, max(printMinMarginTop_in, wholePageHeight_in / 2.0 - printHeight_in / 2.0));
  setValue(printBottomMarginEdit, max(printMinMarginBottom_in, wholePageHeight_in / 2.0 - printHeight_in / 2.0));
  if printPreserveAspectRatio.checked then
    self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
  else
    self.updatePrintPreview;
  end;

procedure TBitmapOptionsForm.suggestPrintSizeClick(Sender: TObject);
  var
    bestMargin_in, bestWidth_in, bestHeight_in, newWidth_in, newHeight_in: single;
    maxMinMargin_in: single;
  begin
  // calculate best margin: for 10 inches, 1.0 inches, for 5 inches, 0.5 inches;
  // keep to multiples of 0.25 inches
  maxMinMargin_in := max(printMinMarginLeft_in, max(printMinMarginTop_in, max(printMinMarginRight_in, printMinMarginBottom_in)));
  bestMargin_in := max(maxMinMargin_in, round(4.0 * min(wholePageWidth_in, wholePageHeight_in) / 10.0) / 4.0);
  bestWidth_in := wholePageWidth_in - bestMargin_in * 2;
  bestHeight_in := wholePageHeight_in - bestMargin_in * 2;
  // preserve aspect ratio - reduce the larger dimension so it still fits on the page
  self.updateSelectionRectFromMainWindow;
  newHeight_in := bestHeight_in;
  newWidth_in := bestHeight_in * aspectRatio;
  if newWidth_in > bestWidth_in then
    begin
    newWidth_in := bestWidth_in;
    newHeight_in := safedivExcept(bestWidth_in, aspectRatio, bestHeight_in);
    end;
  // set original picture size to fit on page using printer resolution
  setValue(inchWidthEdit, newWidth_in);
  setValue(inchHeightEdit, newHeight_in);
  setValue(resolutionEdit, smallestPrintResolution_pxPin);
  self.calculatePixelsFromResolutionAndInches;
  // set print size same as picture size
  setValue(printWidthEdit, newWidth_in);
  setValue(printHeightEdit, newHeight_in);
  // center picture
  self.printCenterClick(self);
  end;

procedure TBitmapOptionsForm.printUseWholePageClick(Sender: TObject);
  var
    borderThickness_in: single;
  begin
  borderThickness_in := safedivExcept(options.borderThickness, smallestPrintResolution_pxPin, 0);
  setValue(printLeftMarginEdit, printMinMarginLeft_in + borderThickness_in);
  setValue(printRightMarginEdit, printMinMarginRight_in + borderThickness_in);
  setValue(printTopMarginEdit, printMinMarginTop_in + borderThickness_in);
  setValue(printBottomMarginEdit, printMinMarginBottom_in + borderThickness_in);
  setValue(printWidthEdit, wholePageWidth_in - printLeftMargin_in - printRightMargin_in);
  setValue(printHeightEdit, wholePageHeight_in - printTopMargin_in - printBottomMargin_in);
  // check new size for aspect ratio (if 'preserve aspect ratio' checked)
  if printPreserveAspectRatio.checked then
    self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged)
  else
    self.updatePrintPreview;
  end;

procedure TBitmapOptionsForm.printPreserveAspectRatioClick(Sender: TObject);
  begin
  if startingUp or sideEffect then exit;
  if printPreserveAspectRatio.checked then
    self.resizePrintBasedOnAspectRatio(kHeightAndWidthWereChanged);
  end;

{ ----------------------------------------------------------------------------------------- buttons }
procedure TBitmapOptionsForm.bordersClick(Sender: TObject);
  var
    bordersForm: TPrintBordersForm;
  begin
  bordersForm := TPrintBordersForm.create(self);
  if bordersForm = nil then
    raise Exception.create('Problem: Could not create print borders window.');
  try
    bordersForm.initializeWithOptions(options);
    if bordersForm.showModal = mrOK then
      begin
      // just copy whole options, because you can't change this form while borders form is up
      self.options := bordersForm.options;
      self.updateBorderThickness;
      self.updatePrintPreview;
      end;
  finally
    bordersForm.free;
  end;
  end;

procedure TBitmapOptionsForm.printSetupClick(Sender: TObject);
  begin
  PrintDialog.execute;
  self.updateForPrinterInfo;
  self.suggestPrintSizeClick(self);
  end;

procedure TBitmapOptionsForm.CloseClick(Sender: TObject);
  var
    insertString: string;
  begin
  // don't let them save the file as a device-dependent bitmap.
  if (colorType.itemIndex = 0)
    and ((copySavePrintType = kSavingDrawingToBmp) or (copySavePrintType = kSavingDrawingToJpeg)) then
    begin
    MessageDlg('You cannot save a picture with the "From screen" color depth.'
      + chr(13) + 'Please change the color depth to another choice in the list.',
      mtError, [mbOK], 0);
    exit;
    end;
  // don't let them finish with no plants
  if (useSelectedPlants.checked) and (MainForm.selectedPlants.count <= 0) then
    begin
    MessageDlg('You chose "selected" for "Draw which plants", but no plants are selected.' + chr(13)
      + 'You should make another choice, or click Cancel and select some plants.', mtError, [mbOK], 0);
    exit;
    end;
  // warn about a really big operation
  if copySavePrintType <> kSavingDrawingToJpeg then
    if megabytesOfMemoryNeeded > kTooManyMegabytesOfMemory then
      begin
      case copySavePrintType of
        kCopyingDrawing: insertString := 'copy to the clipboard';
        kPrintingDrawing: insertString := 'print';
        kSavingDrawingToBmp: insertString := 'save';
        end;
      if MessageDlg('You are about to ' + insertString
          + ' a ' + digitValueString(megabytesOfMemoryNeeded) + ' MB bitmap.' + chr(13)
          + 'This could place stress on your system.' + chr(13)
          + 'We recommend closing any non-essential programs.' + chr(13)
          + 'Also, choosing fewer colors or a smaller picture will use less memory.' + chr(13) + chr(13)
          + 'To proceed, click OK. To go back and make changes, click Cancel.', mtWarning, [mbOK, mbCancel], 0) = IDCANCEL then
          exit;
      end;
  transferDirection := kTransferSave;
	self.transferFields;
  modalResult := mrOK;
  end;

procedure TBitmapOptionsForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

{ ----------------------------------------------------------- methods to get/set edit values }
procedure TBitmapOptionsForm.setValue(editBox: TEdit; newValue: single);
  var
    maxWidth_in, maxHeight_in: single;
  begin
  sideEffect := true;
  maxWidth_in := wholePageWidth_in - printMinMarginLeft_in - printMinMarginRight_in;
  maxHeight_in := wholePageHeight_in - printMinMarginTop_in - printMinMarginBottom_in;
  if editBox = pixelWidthEdit then
    begin
    newValue := max(kMinPixels, min(kMaxPixels, newValue));
    pictureWidth_px := newValue;
    end
  else if editBox = pixelHeightEdit then
    begin
    newValue := max(kMinPixels, min(kMaxPixels, newValue));
    pictureHeight_px := newValue;
    end
  else if editBox = inchWidthEdit then
    begin
    newValue := max(kMinInches, min(kMaxInches, newValue));
    pictureWidth_in := newValue;
    end
  else if editBox = inchHeightEdit then
    begin
    newValue := max(kMinInches, min(kMaxInches, newValue));
    pictureHeight_in := newValue;
    end
  else if editBox = resolutionEdit then
    begin
    newValue := max(kMinResolution, min(kMaxResolution, newValue));
    pictureResolution_pxPin := newValue;
    end
  else if editBox = printWidthEdit then
    begin
    newValue := max(kMinInches, min(newValue, maxWidth_in));
    printWidth_in := newValue;
    end
  else if editBox = printHeightEdit then
    begin
    newValue := max(kMinInches, min(newValue, maxHeight_in));
    printHeight_in := newValue;
    end
  else if editBox = printLeftMarginEdit then
    begin
    newValue := max(kMinInches, min(newValue, maxWidth_in));
    printLeftMargin_in := newValue;
    end
  else if editBox = printTopMarginEdit then
    begin
    newValue := max(kMinInches, min(newValue, maxHeight_in));
    printTopMargin_in := newValue;
    end
  else if editBox = printRightMarginEdit then
    begin
    newValue := max(kMinInches, min(newValue, maxWidth_in));
    printRightMargin_in := newValue;
    end
  else if editBox = printBottomMarginEdit then
    begin
    newValue := max(kMinInches, min(newValue, maxHeight_in));
    printBottomMargin_in := newValue;
    end
  else if editBox = jpgCompressionEdit then
    begin
    newValue := max(1, min(100, newValue));
    jpegCompression := newValue;
    end;
  if editBox.tag = kEditBoxHasInteger then
    editBox.text := intToStr(round(newValue))
  else if editBox.tag = kEditBoxHasFloat then
    editBox.text := floatStr(newValue);
  sideEffect := false;
  end;

function TBitmapOptionsForm.getValue(editBox: TEdit): single;
  begin
  result := 0;
  if editBox = pixelWidthEdit then
    result := pictureWidth_px
  else if editBox = pixelHeightEdit then
    result := pictureHeight_px
  else if editBox = inchWidthEdit then
    result := pictureWidth_in
  else if editBox = inchHeightEdit then
    result := pictureHeight_in
  else if editBox = resolutionEdit then
    result := pictureResolution_pxPin
  else if editBox = printWidthEdit then
    result := printWidth_in
  else if editBox = printHeightEdit then
    result := printHeight_in
  else if editBox = printLeftMarginEdit then
    result := printLeftMargin_in
  else if editBox = printTopMarginEdit then
    result := printTopMargin_in
  else if editBox = printRightMarginEdit then
    result := printRightMargin_in
  else if editBox = printBottomMarginEdit then
    result := printBottomMargin_in
  else if editBox = jpgCompressionEdit then
    result := jpegCompression
  end;

function TBitmapOptionsForm.getEnteredValue(editBox: TEdit): single;
  begin
  result := 0;
  try
  if editBox.tag = kEditBoxHasInteger then
    result := strToInt(editBox.text)
  else if editBox.tag = kEditBoxHasFloat then
    result := strToFloat(editBox.text);
  except on e: exception do
    begin
    showMessage('Invalid value: ' + e.message);
    result := 0;
    end;
  end;
  end;

{ ------------------------------------------------------------------------- transfer functions }
function TBitmapOptionsForm.currentExportOption: smallint;
  begin
  result := kIncludeSelectedPlants;
  if useSelectedPlants.checked then result := kIncludeSelectedPlants
  else if useVisiblePlants.checked then result := kIncludeVisiblePlants
  else if useAllPlants.checked then result := kIncludeAllPlants
  else if useDrawingAreaContents.checked then
    result := kIncludeDrawingAreaContents;
  end;

function TBitmapOptionsForm.nameForCopySavePrintType(aType: smallint): string;
  begin
  result := '';
  case aType of
    kCopyingDrawing: result := 'Copy';
    kPrintingDrawing: result := 'Print';
    kSavingDrawingToBmp, kSavingDrawingToJpeg: result := 'Save';
    end;
  end;

procedure TBitmapOptionsForm.transferCheckBox(checkBox: TCheckBox; var value: boolean);
  begin
  if transferDirection = kTransferLoad then
    checkBox.checked := value
  else if transferDirection = kTransferSave then
    begin
    if value <> checkBox.checked then
      optionsChanged := true;
    value := checkBox.checked;
    end;
  end;

procedure TBitmapOptionsForm.transferSmallintEditBox(editBox: TEdit; var value: smallint);
  begin
  if transferDirection = kTransferLoad then
    setValue(editBox, value) // sets up vars at start
  else if transferDirection = kTransferSave then
    begin
    if value <> strToIntDef(editBox.text, 0) then
      optionsChanged := true;
    value := strToIntDef(editBox.text, 0);
    end;
  end;

procedure TBitmapOptionsForm.transferSingleEditBox(editBox: TEdit; var value: single);
  var
    newValue: single;
  begin
  if transferDirection = kTransferLoad then
    setValue(editBox, value) // sets up vars at start
  else if transferDirection = kTransferSave then
    begin
    try
      newValue := strToFloat(editBox.text);
    except
      newValue := value;
    end;
    if newValue <> value then
      optionsChanged := true;
    value := newValue;
    end;
  end;

procedure TBitmapOptionsForm.transferComboBox(comboBox: TComboBox; var value: smallint);
  begin
  if transferDirection = kTransferLoad then
    comboBox.itemIndex := value
  else if transferDirection = kTransferSave then
    begin
    if value <> comboBox.itemIndex then
      optionsChanged := true;
    value := comboBox.itemIndex;
    end;
  end;

procedure TBitmapOptionsForm.transferTPixelFormatComboBox(comboBox: TComboBox; var value: TPixelFormat);
  begin
  if transferDirection = kTransferLoad then
    begin
    if value = pfCustom then value := pfDevice;
    comboBox.itemIndex := ord(value)
    end
  else if transferDirection = kTransferSave then
    begin
    if value <> TPixelFormat(comboBox.itemIndex) then
      optionsChanged := true;
    value := TPixelFormat(comboBox.itemIndex);
    end;
  end;

procedure TBitmapOptionsForm.colorTypeDrawItem(Control: TWinControl;
    Index: Integer; Rect: TRect; State: TOwnerDrawState);
  var
    selected: boolean;
    cText: array[0..255] of Char;
  begin
  if Application.terminated then exit;
  selected := (odSelected in state);
  with colorType.canvas do
    begin
    font := colorType.font;
    if selected then
      begin
      brush.color := clHighlight;
      font.color := clHighlightText;
      end
    else
      begin
      brush.color := colorType.color;
      font.color := clBtnText;
      end;
    if (index = 0)
      and ((copySavePrintType = kSavingDrawingToBmp) or (copySavePrintType = kSavingDrawingToJpeg)) then
      font.color := clBtnShadow;
    fillRect(rect);
    strPCopy(cText, colorType.items[index]);
    rect.left := rect.left + 2; { margin for text }
    drawText(handle, cText, strLen(cText), rect, DT_LEFT);
    end;
  end;

procedure TBitmapOptionsForm.helpButtonClick(Sender: TObject);
  begin
  case copySavePrintType of
    kCopyingDrawing: application.helpJump('Copying_pictures');
    kPrintingDrawing: application.helpJump('Printing_pictures');
    kSavingDrawingToBmp, kSavingDrawingToJpeg: application.helpJump('Saving_pictures');
	  end;
  end;

procedure TBitmapOptionsForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

end.
