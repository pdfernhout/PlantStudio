unit Udomain;

interface

uses SysUtils, WinTypes, WinProcs, Graphics, Classes,
  uplantmn, uplant, uparams, usection, uhints, u3dexport, usupport;

const
  kMaxWizardQuestions = 30;
  kMaxWizardColors = 2;
  kMaxWizardTdos = 3;
  kMainWindowOrientationHorizontal = 0; kMainWindowOrientationVertical = 1; kMaxMainWindowOrientations = 1;
  kIncludeSelectedPlants = 0; kIncludeVisiblePlants = 1; kIncludeAllPlants = 2; kIncludeDrawingAreaContents = 3;
    kMaxIncludeOption = 3;
  kBreederVariationLow = 0; kBreederVariationMedium = 1; kBreederVariationHigh = 2; kBreederVariationCustom = 3;
    kBreederVariationNoNumeric = 4;
  kNoMutation = 0; kLowMutation = 20; kMediumMutation = 60; kHighMutation = 100;
  kMaxColorOption = 7; //pf32bit 
  kMinResolution = 10; kMaxResolution = 10000; kDefaultResolution = 200;
  kMinPixels = 10; kMaxPixels = 10000;
  kMinInches = 0.0; kMaxInches = 100;
  kExcludeInvisiblePlants = true; kIncludeInvisiblePlants = false;
  kExcludeNonSelectedPlants = true; kIncludeNonSelectedPlants = false;
  kMaxCustomColors = 16;
  kAnimateByXRotation = 0; kAnimateByAge = 1;
  kDrawFast = 0; kDrawMedium = 1; kDrawBest = 2; kDrawCustom = 3;
  kMinOutputCylinderFaces = 3; kMaxOutputCylinderFaces = 20;
  kDefaultV1IniFileName = 'PlantStudio.ini';
  kDefaultV2IniFileName = 'PlantStudio2.ini';
  kV2IniAddition = '_v2';
  kMaxRecentFiles = 10; // v1.60
  kViewPlantsInMainWindowFreeFloating = 1; kViewPlantsInMainWindowOneAtATime = 2;
  kMaxUnregExportsAllowed = 20; kMaxUnregExportsPerSessionAfterMaxReached = 2;
  kInPlantMover = true; kNotInPlantMover = false;

type

  BitmapOptionsStructure = record
    exportType: smallint;
    colorType: TPixelFormat;
    resolution_pixelsPerInch: smallint;
    width_pixels, height_pixels: smallint;
    width_in, height_in: single;
    preserveAspectRatio: boolean;
    jpegCompressionRatio: smallint; // 1 to 100
    printPreserveAspectRatio, printBorderInner, printBorderOuter: boolean;
    printWidth_in, printHeight_in: single;
    printLeftMargin_in, printTopMargin_in, printRightMargin_in, printBottomMargin_in: single;
    printBorderWidthInner, printBorderWidthOuter: smallint;
    borderThickness, borderGap: smallint; // don't save these, they are for storing to use during printing only
    printBorderColorInner, printBorderColorOuter: TColorRef;
    end;

  NozzleOptionsStructure = record
    exportType: smallint;
    resolution_pixelsPerInch: smallint;
    colorType: TPixelFormat;
    backgroundColor: TColorRef;
    cellSize: TPoint;      // don't save in settings
    cellCount: smallint;   // don't save in settings
    end;

  NumberedAnimationOptionsStructure = record
    animateBy: smallint;
    xRotationIncrement: smallint;
    ageIncrement: smallint;
    resolution_pixelsPerInch: smallint;
    colorType: TPixelFormat;
    frameCount: smallint; // don't save in settings
    scaledSize: TPoint; // don't save in settings
    fileSize: longint; // don't save in settings
    end;

  DomainOptionsStructure = record
    hideWelcomeForm: boolean;
    openMostRecentFileAtStart: boolean;
    ignoreWindowSettingsInFile: boolean; // v2.1
    cachePlantBitmaps: boolean;
    memoryLimitForPlantBitmaps_MB: smallint;
    maxPartsPerPlant_thousands: smallint;
    backgroundColor: TColorRef;
    transparentColor: TColorRef;
    showSelectionRectangle: boolean;
    showBoundsRectangle: boolean; // v2.0
    resizeRectSize: smallint;
    pasteRectSize: smallint;
    firstSelectionRectangleColor: TColorRef;
    multiSelectionRectangleColor: TColorRef;
    draw3DObjects: boolean;
    drawStems: boolean;
    fillPolygons: boolean;
    drawSpeed: smallint;
    drawLinesBetweenPolygons: boolean;
    sortPolygons: boolean;
    draw3DObjectsAsBoundingRectsOnly: boolean;
    showPlantDrawingProgress: boolean;
    useMetricUnits: boolean;
    undoLimit: smallint;
    undoLimitOfPlants: smallint;
    rotationIncrement: smallint;
    showLongHintsForButtons: boolean;
    showHintsForParameters: boolean;
    pauseBeforeHint: smallint; {seconds}
    pauseDuringHint: smallint; {seconds}
    noteEditorWrapLines: boolean; // v1.4
    updateTimeSeriesPlantsOnParameterChange: boolean;
    mainWindowViewMode: smallint;
    nudgeDistance: smallint;
    resizeKeyUpMultiplierPercent: smallint;
    parametersFontSize: smallint;
    mainWindowOrientation: smallint;
    lineContrastIndex: smallint;
    sortTdosAsOneItem: boolean;
    circlePointSizeInTdoEditor: smallint;
    partsInTdoEditor: smallint;
    fillTrianglesInTdoEditor: boolean;
    drawLinesInTdoEditor: boolean;
    showGhostingForHiddenParts: boolean;
    showHighlightingForNonHiddenPosedParts: boolean;
    showPosingAtAll: boolean;
    ghostingColor: TColorRef;
    nonHiddenPosedColor: TColorRef;
    selectedPosedColor: TColorRef;
    showWindowOnException: boolean;
    logToFileOnException: boolean;
    wizardChoices: array[1..kMaxWizardQuestions] of string[40];  {cfk change length if needed}
    wizardColors: array[1..kMaxWizardColors] of TColorRef;
    wizardTdoNames: array[1..kMaxWizardTdos] of string;
    wizardShowFruit: boolean;
    customColors: array[0..kMaxCustomColors-1] of TColorRef;
    recentFiles: array[0..kMaxRecentFiles-1] of string;
    end;

  PdDomain = class
    public
    plantFileName, lastOpenedPlantFileName: string;
    plantFileLoaded: boolean;
    options: DomainOptionsStructure;
    breedingAndTimeSeriesOptions: BreedingAndTimeSeriesOptionsStructure;
    bitmapOptions: BitmapOptionsStructure;
    exportOptionsFor3D: array[1..k3DExportTypeLast] of FileExport3DOptionsStructure;
    nozzleOptions: NozzleOptionsStructure;
    animationOptions: NumberedAnimationOptionsStructure;
    // registration
    registered, justRegistered: boolean;
    startTimeThisSession, accumulatedUnregisteredTime: TDateTime;
    registrationName, registrationCode: string;
    unregisteredExportCountBeforeThisSession, unregisteredExportCountThisSession: smallint;
    { managers }
    plantManager: PdPlantManager;
    parameterManager: PdParameterManager;
    sectionManager: PdSectionManager;
    hintManager: PdHintManager;
    { support files }
    iniFileName, iniFileBackupName: string;
    useIniFile: boolean;
    defaultTdoLibraryFileName: string;
    { for remembering settings }
    mainWindowRect: TRect;
    horizontalSplitterPos, verticalSplitterPos: smallint;
    breederWindowRect: TRect;
    timeSeriesWindowRect: TRect;
    debugWindowRect: TRect;
    undoRedoListWindowRect: TRect;
    tdoEditorWindowRect: TRect;
    { for temporary use while drawing }
    temporarilyHideSelectionRectangles: boolean;
    { for making copy bitmap with different resolution than screen }
    drawingToMakeCopyBitmap: boolean;
    plantDrawScaleWhenDrawingCopy_PixelsPerMm: single;
    plantDrawOffsetWhenDrawingCopy_mm: SinglePoint;
    iniLines: TStringList;
    gotInfoFromV1IniFile: boolean;
    class function createDefault: boolean;
    class procedure destroyDefault;
    constructor create; 
    destructor destroy; override;
    function startupLoading: boolean;
    procedure load(fileName: string);          
    procedure save(fileName: string);
    procedure resetForEmptyPlantFile;
    function totalUnregisteredExportsAtThisMoment: smallint;
    procedure updateRecentFileNames(const aFileName: string);
    procedure resetForNoPlantFile;
    function checkForExistingDefaultTdoLibrary: boolean;
    procedure storeProfileInformation;
    procedure getProfileInformationFromFile(fileName: string);
    procedure boundProfileInformation;
    function buildFileNameInPath(const fileName: string): string;
    function nameIsAbsolute(const fileName: string): boolean;
    function isFileInPath(const fileName: string): boolean;
    function firstUnusedUnsavedFileName: string;
    function unsavedFileNameForNumber(aNumber: smallint): string;
    function getColorUsingCustomColors(originalColor: TColorRef): TColorRef;
    function plantDrawOffset_mm: SinglePoint;
    function plantDrawScale_PixelsPerMm: single;
    function windowsDirectory: string;
    function viewPlantsInMainWindowFreeFloating: boolean;
    function viewPlantsInMainWindowOnePlantAtATime: boolean;
    function sectionNumberFor3DExportType(anOutputType: smallint): smallint;
    function sectionStartIndexInIniLines(section: string): integer;
    function stringForSectionAndKey(section, key, defaultString: string): string;
    procedure setStringForSectionAndKey(section, key, newString: string);
    procedure readSectionKeysOrValues(section: string; aList: TStringList; getKeys: boolean);
    procedure removeSectionFromIniLines(section: string);
    end;

var
  domain: PdDomain;

const
  kUnsavedFileName = 'untitled';
  kSectionFiles = 0;
  kSectionPrefs = 1;
  kSectionSettings = 2;
  kSectionDXF = 3;
  kSectionWizard = 4;
  kSectionExport = 5;
  kSectionPrinting = 6;
  kCustomColors = 7;
  kSectionBreeding = 8;
  kSectionNozzle = 9;
  kSectionAnimation = 10;
  kSectionRegistration = 11;
  kSectionOverrides = 12;
  kSectionPOV = 13;
  kSection3DS = 14;
  kSectionOBJ = 15;
  kSectionVRML = 16;
  kSectionLWO = 17;
  kSectionOtherRecentFiles = 18;
  kLastSectionNumber = 18;

  iniSections: array[0..kLastSectionNumber] of string =
  ('Files', 'Preferences', 'Settings',
   'DXF', 'Wizard', 'Picture export', 'Printing', 'Custom colors', 'Breeding', 'Nozzles', 'Animation',
   'Registration', 'Overrides', 'POV', '3DS', 'OBJ', 'VRML', 'LWO', 'Other recent files');

  kStandardTdoLibraryFileName = '3D object library.tdo';
  kEncryptingMultiplierForAccumulatedUnregisteredTime = 20;
  kEncryptingMultiplierForUnregisteredExportCount = 149;
  kKeyForAccumulatedUnregisteredTime = 'Time scale fraction';
  kKeyForUnregisteredExportCount = 'Frame count';
  kGetKeys = true; kGetValues = false;

implementation

uses Dialogs, Controls, Forms, 
  umath, usplash, utimeser, umain, uwizard, URegisterSupport, usstream, uwait;

// ------------------------------------------------------------------------------- creation/destruction
class function PdDomain.createDefault: boolean;
	begin
  domain := PdDomain.create;
  result := domain.startupLoading;
  end;

class procedure PdDomain.destroyDefault;
	begin
  domain.free;
  domain := nil;
  end;

constructor PdDomain.create;
	begin
  inherited create;
  setDecimalSeparator; // v1.5
  { create empty managers }
  plantManager := PdPlantManager.create;
  parameterManager := PdParameterManager.create;
  sectionManager := PdSectionManager.create;
  hintManager := PdHintManager.create;
  iniLines := TStringList.create;
  { non-standard defaults }
  plantManager.plantDrawScale_PixelsPerMm := 1.0;
  plantDrawScaleWhenDrawingCopy_PixelsPerMm := 1.0;
  end;

destructor PdDomain.destroy;
  begin
  plantManager.free;
  plantManager := nil;
  parameterManager.free;
  parameterManager := nil;
  sectionManager.free;
  sectionManager := nil;
  hintManager.free;
  hintManager := nil;
  iniLines.free;
  iniLines := nil;
  inherited destroy;
  end;

function PdDomain.windowsDirectory: string;
  var
    cString: array[0..255] of char;
  begin
  result := '';
  getWindowsDirectory(cString, 256);
  result := strPas(cString);
  end;

// ------------------------------------------------------------------------------- loading
function PdDomain.startupLoading: boolean;
  var
    i: smallint;
    iniFileFound: boolean;
    year, month, day: word;
    v1IniFileName: string;
   begin
  result := true;
  iniFileName := kDefaultV2IniFileName;
  useIniFile := true;
  plantFileName := '';
  if splashForm <> nil then splashForm.showLoadingString('Starting...');
  { ============= parse command line options }
  if ParamCount > 0 then
    begin
    for i := 1 to ParamCount do
      if uppercase(ParamStr(i)) = '/I=' then
        useIniFile := false
      else if uppercase(ParamStr(i)) = '/I' then
        useIniFile := false
      else if pos('/I=', uppercase(ParamStr(i))) = 1 then
        iniFileName := copy(ParamStr(i), 4, length(ParamStr(i)))
      else if pos('/I', uppercase(ParamStr(i))) = 1 then
        iniFileName := copy(ParamStr(i), 3, length(ParamStr(i)))
      else
      if (plantFileName = '') and (pos('/', uppercase(ParamStr(i))) <> 1) then
        plantFileName := ParamStr(i)
      else
        ShowMessage('Improper parameter string ' + ParamStr(i));
    end;
  // make parameters
  parameterManager.makeParameters;
  // make hints
  hintManager.makeHints;
  // v2.0
  // reconcile v2 and v1 ini files
  // only do this if they did NOT specify an alternate file
  // if they specified an alternate file, there is no way to know what version it is;
  // just read it as v1 and write it as v2 (do not expect this to be common use)
  // if they asked NOT to read any ini file, skip doing this
  gotInfoFromV1IniFile := false;
  if (useIniFile) and (iniFileName = kDefaultV2IniFileName) then
    begin
    // if no v2 ini file but there is a v1 ini file, read the v1 ini file NOW but do not change the name for writing out
    if not fileExists(windowsDirectory + '\' + iniFileName) then
      begin
      v1IniFileName := windowsDirectory + '\' + kDefaultV1IniFileName;
      if fileExists(v1IniFileName) then
        begin
        self.getProfileInformationFromFile(v1IniFileName);
        gotInfoFromV1IniFile := true;
        end;
      end;
    end;
  { find out if ini file exists now, because if it doesn't we should save the profile info when leaving
    even if it did not change. if iniFileName does not have a directory, use Windows directory }
  if extractFilePath(iniFileName) <> '' then
    begin
    iniFileFound := fileExists(iniFileName);
    if not iniFileFound then
      begin
      ShowMessage('Could not find alternate settings file ' + chr(13) + chr(13)
        + '  ' + iniFileName + chr(13) + chr(13)
        + 'Using standard settings file in Windows directory instead.');
      iniFileName := kDefaultV2IniFileName;
      iniFileFound := fileExists(windowsDirectory + '\' + iniFileName);
      iniFileName := windowsDirectory + '\' + iniFileName;
      end;
    end
  else
    begin
    iniFileFound := fileExists(windowsDirectory + '\' + iniFileName);
    iniFileName := windowsDirectory + '\' + iniFileName;
    end;
  iniFileChanged := not iniFileFound;
  { ============= if ini file doesn't exist or don't want, set default options; otherwise read options from ini file }
  // if already read options from v1 ini file, don't default - v2.0
  if iniFileFound and useIniFile then
    self.getProfileInformationFromFile(iniFileName)
  else if not gotInfoFromV1IniFile then
    self.getProfileInformationFromFile(''); // defaults options
  startTimeThisSession := Now;
  { ============= load plant file from command line if found }
  if plantFileName <> '' then
    try
       if splashForm <> nil then splashForm.showLoadingString('Reading startup file...');
       plantFileName := buildFileNameInPath(plantFileName);
       self.load(plantFileName);
    except on E: Exception do
      begin
      ShowMessage(E.message);
      ShowMessage('Could not open plant file from command line ' + plantFileName);
      end;
    end
  else
    { ============= if most recent plant file in INI try it unless -I option }
    // assume ini file has been read by now
    if (useIniFile) and (options.openMostRecentFileAtStart) then
      begin
      plantFileName := stringForSectionAndKey('Files', 'Recent', plantFileName);
      plantFileName := buildFileNameInPath(plantFileName);
      if (plantFileName <> '') and self.isFileInPath(plantFileName) then
        try
          if splashForm <> nil then splashForm.showLoadingString('Reading most recent file...');
          self.load(plantFileName);
        except on E: Exception do
          begin
          ShowMessage(E.message);
          ShowMessage('Could not load most recently saved plant file ' + plantFileName);
          end;
        end;
      end;
  // show obsolete warning if unregistered
  DecodeDate(Now, year, month, day);
  if (not registered) and (year >= 2003) then   
    MessageDlg('This version of PlantStudio was released some time ago.' + chr(13) + chr(13) +
    	'Please check for an newer version at:'  + chr(13) +
      '  http://www.kurtz-fernhout.com'  + chr(13) +  chr(13) +
      'The web site may also have updated pricing information.' + chr(13) + chr(13) +
      'You can still register this copy of the software if you want to, though;' + chr(13) +
      'this message will disappear when this copy is registered.', mtInformation, [mbOK], 0);
  end;

// --------------------------------------------------------------------------------- ini file methods referred to
function PdDomain.sectionStartIndexInIniLines(section: string): integer;
  var
    i: integer;
    aLine: string;
  begin
  result := -1;
  i := 0;
  while i <= iniLines.count - 1 do
    begin
    aLine := trim(iniLines.strings[i]);
    if '[' + section + ']' = aLine then
      begin
      result := i;
      exit;
      end
    else
      inc(i);
    end;
  end;

function PdDomain.stringForSectionAndKey(section, key, defaultString: string): string;
  var
    i: integer;
    aLine: string;
  begin
  result := defaultString;
  if (iniLines = nil) or (iniLines.count <= 0) then exit;
  i := self.sectionStartIndexInIniLines(section);
  if i < 0 then exit;
  inc(i); // move to next after section
  // only read up until next section - don't want to get same name from different section
  while (i <= iniLines.count - 1) do
    begin
    aLine := trim(iniLines.strings[i]);
    if (length(aLine) > 0) and (aLine[1] = '[') then exit;
    if key = trim(stringUpTo(aLine, '=')) then
      begin
      result := stringBeyond(iniLines.strings[i], '=');
      exit;
      end
    else
      inc(i);
    end;
  end;

procedure PdDomain.setStringForSectionAndKey(section, key, newString: string);
  var
    i: integer;
    found: boolean;
    aLine: string;
  begin
  if (iniLines = nil) then exit;
  i := self.sectionStartIndexInIniLines(section);
  // if no section found, add section at end and add this one item to it
  if i < 0 then
    begin
    iniLines.add('[' + section + ']');
    iniLines.add(key + '=' + newString);
    end
  else // section found
    begin
    found := false;
    inc(i); // move to next after section
    // only read up until next section - don't want to get same name from different section
    while (i <= iniLines.count - 1) do
      begin
      aLine := trim(iniLines.strings[i]);
      if (length(aLine) > 0) and (aLine[1] = '[') then break;
      if key = trim(stringUpTo(iniLines.strings[i], '=')) then
        begin
        iniLines.strings[i] := key + '=' + newString;
        found := true;
        break;
        end
      else
        inc(i);
      end;
    // if there was no match for the key, ADD a line to the section
    if not found then
      if i <= iniLines.count - 1 then
        iniLines.insert(i, key + '=' + newString)
      else
        iniLines.add(key + '=' + newString);
    end;
  end;

procedure PdDomain.readSectionKeysOrValues(section: string; aList: TStringList; getKeys: boolean);
  var
    i: integer;
    aLine: string;
  begin
  if (iniLines = nil) or (iniLines.count <= 0) then exit;
  i := self.sectionStartIndexInIniLines(section);
  if i < 0 then exit;
  inc(i); // move to next after section
  while i <= iniLines.count - 1 do
    begin
    aLine := trim(iniLines.strings[i]);
    if (length(aLine) > 0) and (aLine[1] = '[') then break;
    if getKeys then
      aList.add(trim(stringUpTo(iniLines.strings[i], '=')))
    else // values
      aList.add(stringBeyond(iniLines.strings[i], '='));
    inc(i);
    end;
  end;

procedure PdDomain.removeSectionFromIniLines(section: string);
  var
    i: integer;
    aLine: string;
  begin
  if (iniLines = nil) or (iniLines.count <= 0) then exit;
  i := self.sectionStartIndexInIniLines(section);
  if i < 0 then exit;
  iniLines.delete(i);
  while (i <= iniLines.count - 1) do
    begin
    aLine := trim(iniLines.strings[i]);
    if (length(aLine) > 0) and (aLine[1] = '[') then break;
    iniLines.delete(i);
    end;
  end;

// --------------------------------------------------------------------------------- ini file load/save
procedure PdDomain.getProfileInformationFromFile(fileName: string);
  var
    i, j: smallint;
    section, typeName, timeString, key, value, sectionName, paramName: string;
    readNumber: single;
    readInt: integer;
    overrideKeys: TStringList;
    overrideValues: TStringList;
    param: PdParameter;
    stream: KfStringStream;
  begin
  if fileName <> '' then
    iniLines.loadFromFile(fileName);
  with options do
    begin
    // ------------------------------------------- files
    section := iniSections[kSectionFiles];
    defaultTdoLibraryFileName := stringForSectionAndKey(section, '3D object library',
        extractFilePath(Application.exeName) + '3D object library.tdo');
    // ------------------------------------------- recent files
    section := iniSections[kSectionOtherRecentFiles];
    for i := 0 to kMaxRecentFiles - 1 do
      recentFiles[i] := stringForSectionAndKey(section, 'File' + intToStr(i+1), '');
    // ------------------------------------------- preferences
    section := iniSections[kSectionPrefs];
    openMostRecentFileAtStart := strToBool(stringForSectionAndKey(section, 'Open most recent file at start', 'true'));
    ignoreWindowSettingsInFile := strToBool(stringForSectionAndKey(section, 'Ignore window settings saved in files', 'false'));
    cachePlantBitmaps := strToBool(stringForSectionAndKey(section, 'Draw plants into separate bitmaps', 'true'));
    memoryLimitForPlantBitmaps_MB := strToInt(stringForSectionAndKey(section, 'Memory limit for plant bitmaps (in MB)', '5'));
    maxPartsPerPlant_thousands := strToInt(stringForSectionAndKey(section, 'Max parts per plant (in thousands)', '10'));
    hideWelcomeForm := strToBool(stringForSectionAndKey(section, 'Hide welcome window', 'false'));
    backgroundColor := strToInt(stringForSectionAndKey(section, 'Background color', intToStr(clWhite)));
    transparentColor := strToInt(stringForSectionAndKey(section, 'Transparent color', intToStr(clWhite)));
    showSelectionRectangle := strToBool(stringForSectionAndKey(section, 'Show selection rectangle', 'true'));
    showBoundsRectangle := strToBool(stringForSectionAndKey(section, 'Show bounding rectangle', 'false'));
    resizeRectSize := strToInt(stringForSectionAndKey(section, 'Resizing rectangle size', '6'));
    pasteRectSize := strToInt(stringForSectionAndKey(section, 'Paste rectangle size', '100'));
    firstSelectionRectangleColor := strToInt(stringForSectionAndKey(section, 'First selection rectangle color', intToStr(clRed)));
    multiSelectionRectangleColor := strToInt(stringForSectionAndKey(section, 'Multi selection rectangle color', intToStr(clBlue)));
    draw3DObjects := strToBool(stringForSectionAndKey(section, 'Draw 3D objects', 'true'));
    drawStems := strToBool(stringForSectionAndKey(section, 'Draw stems', 'true'));
    fillPolygons := strToBool(stringForSectionAndKey(section, 'Fill polygons', 'true'));
    drawSpeed := strToInt(stringForSectionAndKey(section, 'Draw speed (boxes/frames/solids)', intToStr(kDrawBest)));
    drawLinesBetweenPolygons := strToBool(stringForSectionAndKey(section, 'Draw lines between polygons', 'true'));
    sortPolygons := strToBool(stringForSectionAndKey(section, 'Sort polygons', 'true'));
    draw3DObjectsAsBoundingRectsOnly := strToBool(stringForSectionAndKey(section, 'Draw 3D objects as squares', 'false'));
    showPlantDrawingProgress := strToBool(stringForSectionAndKey(section, 'Show drawing progress', 'true'));
    useMetricUnits := strToBool(stringForSectionAndKey(section, 'Use metric units', 'true'));
    undoLimit := strToInt(stringForSectionAndKey(section, 'Actions to keep in undo list', '50'));
    undoLimitOfPlants := strToInt(stringForSectionAndKey(section, 'Plants to keep in undo list', '10'));
    rotationIncrement := strToInt(stringForSectionAndKey(section, 'Rotation button increment', '10'));
    showLongHintsForButtons := strToBool(stringForSectionAndKey(section, 'Show long hints for buttons', 'true'));
    showHintsForParameters := strToBool(stringForSectionAndKey(section, 'Show hints for parameters', 'true'));
    pauseBeforeHint := strToInt(stringForSectionAndKey(section, 'Pause before hint', '1'));
    pauseDuringHint := strToInt(stringForSectionAndKey(section, 'Pause during hint', '60'));
    noteEditorWrapLines := strToBool(stringForSectionAndKey(section, 'Wrap lines in note editor', 'true'));
    updateTimeSeriesPlantsOnParameterChange := strToBool(stringForSectionAndKey(section, 'Update time series plants on parameter change', 'true'));
    mainWindowViewMode := strToInt(stringForSectionAndKey(section, 'Main window view option (all/one)', '0'));
    nudgeDistance := strToInt(stringForSectionAndKey(section, 'Distance plant moves with Control-arrow key', '5'));
    resizeKeyUpMultiplierPercent := strToInt(stringForSectionAndKey(section, 'Percent size increase with Control-Shift-up-arrow key', '110'));
    parametersFontSize := strToInt(stringForSectionAndKey(section, 'Parameter panels font size', '8'));
    mainWindowOrientation := strToInt(stringForSectionAndKey(section, 'Main window orientation (horiz/vert)', '0'));
    lineContrastIndex := strToInt(stringForSectionAndKey(section, 'Contrast index for lines on polygons', '3'));
    sortTdosAsOneItem := strToBool(stringForSectionAndKey(section, 'Sort 3D objects as one item', 'true'));
    circlePointSizeInTdoEditor := strToInt(stringForSectionAndKey(section, '3D object editor point size', '8'));
    partsInTdoEditor := strToInt(stringForSectionAndKey(section, '3D object editor parts', '1'));
    fillTrianglesInTdoEditor := strToBool(stringForSectionAndKey(section, '3D object editor fill triangles', 'true'));
    drawLinesInTdoEditor := strToBool(stringForSectionAndKey(section, '3D object editor draw lines','true'));
    showWindowOnException := strToBool(stringForSectionAndKey(section, 'Show numerical exceptions window on exception', 'false'));
    logToFileOnException := strToBool(stringForSectionAndKey(section, 'Log to file on exception', 'false'));
    showGhostingForHiddenParts := strToBool(stringForSectionAndKey(section, 'Ghost hidden parts', 'false'));
    showHighlightingForNonHiddenPosedParts := strToBool(stringForSectionAndKey(section, 'Highlight posed parts', 'true'));
    showPosingAtAll := strToBool(stringForSectionAndKey(section, 'Show posing', 'true'));
    ghostingColor := strToInt(stringForSectionAndKey(section, 'Ghosting color', intToStr(clSilver)));
    nonHiddenPosedColor := strToInt(stringForSectionAndKey(section, 'Posed color', intToStr(clBlue)));
    selectedPosedColor := strToInt(stringForSectionAndKey(section, 'Posed selected color', intToStr(clRed)));
    // ------------------------------------------- settings
    section := iniSections[kSectionSettings];
    mainWindowRect := stringToRect(stringForSectionAndKey(section, 'Window position', '50 50 500 350'));
    horizontalSplitterPos := strToInt(stringForSectionAndKey(section, 'Horizontal split', '200'));
    verticalSplitterPos := strToInt(stringForSectionAndKey(section, 'Vertical split', '200'));
    debugWindowRect := stringToRect(stringForSectionAndKey(section, 'Numerical exceptions window position', '75 75 400 200'));
    undoRedoListWindowRect := stringToRect(stringForSectionAndKey(section, 'Undo/redo list window position', '100 100 400 300'));
    tdoEditorWindowRect := stringToRect(stringForSectionAndKey(section, '3D object editor window position', '100 100 400 400'));
    breederWindowRect := stringToRect(stringForSectionAndKey(section, 'Breeder position', '100 100 400 350'));
    timeSeriesWindowRect := stringToRect(stringForSectionAndKey(section, 'Time series position', '150 150 250 150'));
    // ------------------------------------------- 3d export options
    for i := 1 to k3DExportTypeLast do with exportOptionsFor3D[i] do
      begin
      section := iniSections[self.sectionNumberFor3DExportType(i)];
      typeName := nameFor3DExportType(i);
      // ------------------------------------------- options in common for all
      exportType := strToInt(stringForSectionAndKey(section, typeName + ' which plants to draw (selected/visible/all)', '0'));
      layeringOption := strToInt(stringForSectionAndKey(section, typeName + ' layering option (all/by type/by part)', '1'));
      stemCylinderFaces := strToInt(stringForSectionAndKey(section, typeName + ' stem cylinder sides', '5'));
      translatePlantsToWindowPositions := strToBool(stringForSectionAndKey(section, typeName + ' translate plants to match window positions', 'true'));
      if i = k3DS then
        lengthOfShortName := strToInt(stringForSectionAndKey(section, typeName + ' length of plant name', '2'))
      else
        lengthOfShortName := strToInt(stringForSectionAndKey(section, typeName + ' length of plant name', '8'));
      writePlantNumberInFrontOfName := strToBool(stringForSectionAndKey(section, typeName + ' write plant number in front of name', 'false'));
      writeColors := strToBool(stringForSectionAndKey(section, typeName + ' write colors', 'true'));
      xRotationBeforeDraw := strToInt(stringForSectionAndKey(section, typeName + ' X rotation before drawing', '0'));
      overallScalingFactor_pct := strToInt(stringForSectionAndKey(section, typeName + ' scaling factor (percent)', '100'));
      pressPlants := strToBool(stringForSectionAndKey(section, typeName + ' press plants', 'false'));
      directionToPressPlants := strToInt(stringForSectionAndKey(section, typeName + ' press dimension (x/y/z)', intToStr(kY)));
      makeTrianglesDoubleSided := strToBool(stringForSectionAndKey(section, typeName + ' double sided', 'true'));
      // ------------------------------------------- special options
      if i = kDXF then
        begin
        dxf_whereToGetColors := strToInt(stringForSectionAndKey(section, 'DXF colors option (by type/by part/all)', '0'));
        dxf_wholePlantColorIndex := strToInt(stringForSectionAndKey(section, 'DXF whole plant color index', '2')); // lime
        for j := 0 to kExportPartLast do
          dxf_plantPartColorIndexes[j] := strToInt(stringForSectionAndKey(section, 'DXF color indexes ' + intToStr(j+1), '2')); // lime
        end
      else if i = kPOV then
        begin
        pov_minLineLengthToWrite := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'POV minimum line length to write (mm)', '0.01'));
        pov_minTdoScaleToWrite := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'POV minimum 3D object scale to write', '0.01'));
        pov_commentOutUnionAtEnd := strToBool(stringForSectionAndKey(section, 'POV comment out union of plants at end', 'false'));
        end
      else if i = kVRML then
        begin
        vrml_version := strToInt(stringForSectionAndKey(section, 'VRML version', '1'));
        end;
      if (i = kPOV) or (i = kVRML) then
        begin
        nest_LeafAndPetiole := strToBool(stringForSectionAndKey(section, typeName + ' nest leaves with petioles', 'true'));
        nest_CompoundLeaf := strToBool(stringForSectionAndKey(section, typeName + ' compound leaves', 'true'));
        nest_Inflorescence := strToBool(stringForSectionAndKey(section, typeName + ' nest inflorescences', 'true'));
        nest_PedicelAndFlowerFruit := strToBool(stringForSectionAndKey(section, typeName + ' nest flowers/fruits with pedicels', 'true'));
        nest_FloralLayers := strToBool(stringForSectionAndKey(section, typeName + ' nest pistils and stamens', 'true'));
        end;
      end;
    // ------------------------------------------- wizard
    section := iniSections[kSectionWizard];
    // meristems
    wizardChoices[kMeristem_AlternateOrOpposite] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kMeristem_AlternateOrOpposite), 'leavesAlternate');
    wizardChoices[kMeristem_BranchIndex] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kMeristem_BranchIndex), 'branchNone');
    wizardChoices[kMeristem_SecondaryBranching] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kMeristem_SecondaryBranching), 'secondaryBranchingNo');
    wizardChoices[kMeristem_BranchAngle] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kMeristem_BranchAngle), 'branchAngleSmall');
    // internodes
    wizardChoices[kInternode_Curviness] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInternode_Curviness), 'curvinessLittle');
    wizardChoices[kInternode_Length] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInternode_Length), 'internodesMedium');
    wizardChoices[kInternode_Thickness] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInternode_Thickness), 'internodeWidthThin');
    // leaves
    wizardChoices[kLeaves_Scale] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kLeaves_Scale), 'leafScaleMedium');
    wizardChoices[kLeaves_PetioleLength] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kLeaves_PetioleLength), 'petioleMedium');
    wizardChoices[kLeaves_Angle] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kLeaves_Angle), 'leafAngleMedium');
    // compound leaves
    wizardChoices[kLeaflets_Number] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kLeaflets_Number), 'leafletsOne');
    wizardChoices[kLeaflets_Shape] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kLeaflets_Shape), 'leafletsPinnate');
    wizardChoices[kLeaflets_Spread] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kLeaflets_Spread), 'leafletSpacingMedium');
    // inflor placement
    wizardChoices[kInflorPlace_NumApical] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInflorPlace_NumApical), 'apicalInflorsNone');
    wizardChoices[kInflorPlace_ApicalStalkLength] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInflorPlace_ApicalStalkLength), 'apicalStalkMedium');
    wizardChoices[kInflorPlace_NumAxillary] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInflorPlace_NumAxillary), 'axillaryInflorsNone');
    wizardChoices[kInflorPlace_AxillaryStalkLength] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInflorPlace_AxillaryStalkLength), 'axillaryStalkMedium');
    // inflor drawing
    wizardChoices[kInflorDraw_NumFlowers] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInflorDraw_NumFlowers), 'inflorFlowersThree');
    wizardChoices[kInflorDraw_Shape] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInflorDraw_Shape), 'inflorShapeRaceme');
    wizardChoices[kInflorDraw_Thickness] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kInflorDraw_Thickness), 'inflorWidthThin');
    // flowers
    wizardChoices[kFlowers_NumPetals] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kFlowers_NumPetals), 'petalsFive');
    wizardChoices[kFlowers_Scale] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kFlowers_Scale), 'petalScaleSmall');
    wizardColors[1] := strToInt(stringForSectionAndKey(section, 'Wizard colors 1', intToStr(clFuchsia)));
    // fruit
    wizardChoices[kFruit_NumSections] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kFruit_NumSections), 'fruitSectionsFive');
    wizardChoices[kFruit_Scale] :=
      stringForSectionAndKey(section, 'Wizard question ' + intToStr(kFruit_Scale), 'fruitScaleSmall');
    wizardColors[2] := strToInt(stringForSectionAndKey(section, 'Wizard colors 2', intToStr(clRed)));
    // the wizard will default the tdo names when it comes up, we don't have to do it here
    for i := 1 to kMaxWizardTdos do
      wizardTdoNames[i] := stringForSectionAndKey(section, 'Wizard 3D objects ' + intToStr(i), '');
    wizardShowFruit := strToBool(stringForSectionAndKey(section, 'Wizard show fruit', 'false'));
    // ------------------------------------------- custom colors
    section := iniSections[kCustomColors];
    for i := 0 to kMaxCustomColors-1 do
      customColors[i] := strToInt(stringForSectionAndKey(section, 'Custom color ' + intToStr(i+1), '0'));
    end; // with options
  with bitmapOptions do
    begin
    // -------------------------------------------  export (2D)
    section := iniSections[kSectionExport];
    exportType := strToInt(stringForSectionAndKey(section, 'Which plants to draw (selected/visible/all/drawing)', intToStr(kIncludeSelectedPlants)));
    colorType := TPixelFormat(strToInt(stringForSectionAndKey(section, 'Colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)', '6')));
    resolution_pixelsPerInch := strToInt(stringForSectionAndKey(section, 'Resolution (pixels per inch)', intToStr(kDefaultResolution)));
    width_pixels := strToInt(stringForSectionAndKey(section, 'Picture width (pixels)', '400'));
    height_pixels := strToInt(stringForSectionAndKey(section, 'Picture height (pixels)', '400'));
    width_in := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'Picture width (inches)', '2.0'));
    height_in := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'Picture height (inches)', '2.0'));
    preserveAspectRatio := strToBool(stringForSectionAndKey(section, 'Preserve aspect ratio', 'true'));
    jpegCompressionRatio := strToInt(stringForSectionAndKey(section, 'JPEG compression quality ratio (1-100)', '50'));
    // -------------------------------------------  printing
    section := iniSections[kSectionPrinting];
    printPreserveAspectRatio := strToBool(stringForSectionAndKey(section, 'Preserve aspect ratio', 'true'));
    printWidth_in := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'Print width (inches)', '4.0'));
    printHeight_in := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'Print height (inches)', '4.0'));
    printLeftMargin_in := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'Print left margin (inches)', '1.0'));
    printTopMargin_in := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'Print top margin (inches)', '1.0'));
    printRightMargin_in := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'Print right margin (inches)', '1.0'));
    printBottomMargin_in := strToFloatWithCommaCheck(stringForSectionAndKey(section, 'Print bottom margin (inches)', '1.0'));
    printBorderInner := strToBool(stringForSectionAndKey(section, 'Print inner border', 'false'));
    printBorderOuter := strToBool(stringForSectionAndKey(section, 'Print outer border', 'false'));
    printBorderWidthInner := strToInt(stringForSectionAndKey(section, 'Inner border width (pixels)', '1'));
    printBorderWidthOuter := strToInt(stringForSectionAndKey(section, 'Outer border width (pixels)', '1'));
    printBorderColorInner := strToInt(stringForSectionAndKey(section, 'Inner border color', '0'));
    printBorderColorOuter := strToInt(stringForSectionAndKey(section, 'Outer border color', '0'));
    end;
  // -------------------------------------------  breeding
  with breedingAndTimeSeriesOptions do
    begin
    section := iniSections[kSectionBreeding];
    plantsPerGeneration := strToInt(stringForSectionAndKey(section, 'Plants per generation', '5'));
    percentMaxAge := strToInt(stringForSectionAndKey(section, 'Percent max age', '100'));
    variationType := strToInt(stringForSectionAndKey(section, 'Variation (low/med/high/custom/none)', '1'));
    thumbnailWidth := strToInt(stringForSectionAndKey(section, 'Thumbnail width', '40'));
    thumbnailHeight := strToInt(stringForSectionAndKey(section, 'Thumbnail height', '80'));
    maxGenerations := strToInt(stringForSectionAndKey(section, 'Max generations', '30'));
    numTimeSeriesStages := strToInt(stringForSectionAndKey(section, 'Time series stages', '5'));
    for i := 0 to kMaxBreedingSections - 1 do
      mutationStrengths[i] := strToInt(stringForSectionAndKey(section, 'Mutation ' + intToStr(i+1), intToStr(kMediumMutation)));
    for i := 0 to kMaxBreedingSections - 1 do
      firstPlantWeights[i] := strToInt(stringForSectionAndKey(section, 'First plant weight ' + intToStr(i+1), '50'));
    getNonNumericalParametersFrom := strToInt(stringForSectionAndKey(section, 'Non-numeric', '5'));
    mutateAndBlendColorValues := strToBool(stringForSectionAndKey(section, 'Vary colors', 'false'));
    chooseTdosRandomlyFromCurrentLibrary := strToBool(stringForSectionAndKey(section, 'Vary 3D objects', 'false'));
    end;
  // -------------------------------------------  nozzles
  with nozzleOptions do
    begin
    section := iniSections[kSectionNozzle];
    exportType := strToInt(stringForSectionAndKey(section, 'Which plants to make nozzle from (selected/visible/all)', '0'));
    resolution_pixelsPerInch := strToInt(stringForSectionAndKey(section, 'Nozzle resolution', intToStr(kDefaultResolution)));
    colorType := TPixelFormat(strToInt(stringForSectionAndKey(section, 'Nozzle colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)', '6')));
    backgroundColor := strToInt(stringForSectionAndKey(section, 'Nozzle background color', intToStr(clWhite)));
    end;
  // -------------------------------------------  animations
  with animationOptions do
    begin
    section := iniSections[kSectionAnimation];
    animateBy := strToInt(stringForSectionAndKey(section, 'Animate by (x rotation/age)', '0'));
    xRotationIncrement := strToInt(stringForSectionAndKey(section, 'X rotation increment', '10'));
    ageIncrement := strToInt(stringForSectionAndKey(section, 'Age increment', '5'));
    resolution_pixelsPerInch := strToInt(stringForSectionAndKey(section, 'Resolution', intToStr(kDefaultResolution)));
    colorType := TPixelFormat(strToInt(stringForSectionAndKey(section, 'Animation colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)', '6')));  // 24 bit
    end;
  // -------------------------------------------  registration
  section := iniSections[kSectionRegistration];
  registrationName := stringForSectionAndKey(section, 'R4', '');
  registrationName := hexUnencode(registrationName);
  registrationCode := stringForSectionAndKey(section, 'R2', '');
  registrationCode := hexUnencode(registrationCode);
  registered := RegistrationMatch(registrationName, registrationCode);
  if not registered then
    begin
    section := iniSections[kSectionPrefs];
    timeString := stringForSectionAndKey(section, kKeyForAccumulatedUnregisteredTime, '0');
    readNumber := max(strToFloatWithCommaCheck(timeString), 0);
    accumulatedUnregisteredTime := readNumber / kEncryptingMultiplierForAccumulatedUnregisteredTime;
    section := iniSections[kSectionBreeding];
    readInt := strToInt(stringForSectionAndKey(section, kKeyForUnregisteredExportCount, '0'));
    unregisteredExportCountBeforeThisSession := readInt div kEncryptingMultiplierForUnregisteredExportCount;
    unregisteredExportCountThisSession := 0;
    end;
  // -------------------------------------------  parameter overrides
  section := iniSections[kSectionOverrides];
  overrideKeys := TStringList.create;
  overrideValues := TStringList.create;
  try
    self.readSectionKeysOrValues(section, overrideKeys, kGetKeys);
    self.readSectionKeysOrValues(section, overrideValues, kGetValues);
    if overrideKeys.count > 0 then
      for i := 0 to overrideKeys.count - 1 do
        begin
        key := overrideKeys.strings[i];
        // v2.1 changed to require section and param name for overrides
        sectionName := trim(stringUpTo(key, ':'));
        paramName := trim(stringBeyond(key, ':'));
        value := overrideValues.strings[i];
        value := stringBeyond(value, '=');
        param := nil;
        param := sectionManager.parameterForSectionAndName(sectionName, paramName);
        if (param = nil) or (param.cannotOverride) then continue;
        stream := KfStringStream.create;
        try
          stream.onStringSeparator(value, ' ');
          try
            param.lowerBoundOverride := strToFloatWithCommaCheck(stream.nextToken);
            param.upperBoundOverride := strToFloatWithCommaCheck(stream.nextToken);
            param.defaultValueStringOverride := stringBetween('(', ')', stream.remainder);
            param.isOverridden := true;
          except
            param.isOverridden := false;
          end;
        finally
          stream.free;
        end;
      end;
  finally
    overrideKeys.free;
    overrideValues.free;
  end;
  self.boundProfileInformation;
  end;

procedure PdDomain.storeProfileInformation;
  var
    i, j: smallint;
    section, typeName: string;
    saveNumber: single;
    saveInt: integer;
    param: PdParameter;
  begin
  try
    setDecimalSeparator; // v1.5
    if gotInfoFromV1IniFile then // remove two sections gotten rid of in v2
      begin
      self.removeSectionFromIniLines('Breeder');
      self.removeSectionFromIniLines('Time series');
      end;
    with options do
    begin
    { files }
    section := iniSections[kSectionFiles];
    if pos(upperCase(kUnsavedFileName), upperCase(lastOpenedPlantFileName)) = 0 then
      setStringForSectionAndKey(section, 'Recent', lastOpenedPlantFileName)
    else
      setStringForSectionAndKey(section, 'Recent', '');
    setStringForSectionAndKey(section, '3D object library', defaultTdoLibraryFileName);
    // recent files
    section := iniSections[kSectionOtherRecentFiles];
    for i := 0 to kMaxRecentFiles - 1 do
      if recentFiles[i] <> '' then setStringForSectionAndKey(section, 'File' + intToStr(i+1), recentFiles[i]);
    { preferences }
    section := iniSections[kSectionPrefs];
    setStringForSectionAndKey(section, 'Hide welcome window', boolToStr(hideWelcomeForm));
    setStringForSectionAndKey(section, 'Open most recent file at start', boolToStr(openMostRecentFileAtStart));
    setStringForSectionAndKey(section, 'Ignore window settings saved in files', boolToStr(ignoreWindowSettingsInFile));
    setStringForSectionAndKey(section, 'Draw plants into separate bitmaps', boolToStr(cachePlantBitmaps));
    setStringForSectionAndKey(section, 'Memory limit for plant bitmaps (in MB)', intToStr(memoryLimitForPlantBitmaps_MB));
    setStringForSectionAndKey(section, 'Max parts per plant (in thousands)', intToStr(maxPartsPerPlant_thousands));
    setStringForSectionAndKey(section, 'Background color', intToStr(backgroundColor));
    setStringForSectionAndKey(section, 'Transparent color', intToStr(transparentColor));
    setStringForSectionAndKey(section, 'Show selection rectangle', boolToStr(showSelectionRectangle));
    setStringForSectionAndKey(section, 'Show bounding rectangle', boolToStr(showBoundsRectangle));
    setStringForSectionAndKey(section, 'Resizing rectangle size', intToStr(resizeRectSize));
    setStringForSectionAndKey(section, 'Paste rectangle size', intToStr(pasteRectSize));
    setStringForSectionAndKey(section, 'First selection rectangle color', intToStr(firstSelectionRectangleColor));
    setStringForSectionAndKey(section, 'Multi selection rectangle color', intToStr(multiSelectionRectangleColor));
    setStringForSectionAndKey(section, 'Draw 3D objects', boolToStr(draw3DObjects));
    setStringForSectionAndKey(section, 'Draw stems', boolToStr(drawStems));
    setStringForSectionAndKey(section, 'Fill polygons', boolToStr(fillPolygons));
    setStringForSectionAndKey(section, 'Draw speed (boxes/frames/solids)', intToStr(drawSpeed));
    setStringForSectionAndKey(section, 'Draw lines between polygons', boolToStr(drawLinesBetweenPolygons));
    setStringForSectionAndKey(section, 'Sort polygons', boolToStr(sortPolygons));
    setStringForSectionAndKey(section, 'Draw 3D objects as squares', boolToStr(draw3DObjectsAsBoundingRectsOnly));
    setStringForSectionAndKey(section, 'Show drawing progress', boolToStr(showPlantDrawingProgress));
    setStringForSectionAndKey(section, 'Use metric units', boolToStr(useMetricUnits));
    setStringForSectionAndKey(section, 'Actions to keep in undo list', intToStr(undoLimit));
    setStringForSectionAndKey(section, 'Plants to keep in undo list', intToStr(undoLimitOfPlants));
    setStringForSectionAndKey(section, 'Rotation button increment', intToStr(rotationIncrement));
    setStringForSectionAndKey(section, 'Show long hints for buttons', boolToStr(showLongHintsForButtons));
    setStringForSectionAndKey(section, 'Show hints for parameters', boolToStr(showHintsForParameters));
    setStringForSectionAndKey(section, 'Pause before hint', intToStr(pauseBeforeHint));
    setStringForSectionAndKey(section, 'Pause during hint', intToStr(pauseDuringHint));
    setStringForSectionAndKey(section, 'Wrap lines in note editor', boolToStr(noteEditorWrapLines));
    // registration, embedded here to hide time scale fraction
    if justRegistered then
      begin
      section := iniSections[kSectionRegistration];
      setStringForSectionAndKey(section, 'R1', 'RQBBBOYUMMBIHYMBB');
      setStringForSectionAndKey(section, 'R2', hexEncode(registrationCode));
      setStringForSectionAndKey(section, 'R3', 'YWEHZBBIUWOPBCDVXBQB');
      setStringForSectionAndKey(section, 'R4', hexEncode(registrationName));
     end
    else if not registered then
      begin
      section := iniSections[kSectionPrefs];
    	accumulatedUnregisteredTime := accumulatedUnregisteredTime + max((now - startTimeThisSession), 0);
    	saveNumber := accumulatedUnregisteredTime * kEncryptingMultiplierForAccumulatedUnregisteredTime;
    	setStringForSectionAndKey(section, kKeyForAccumulatedUnregisteredTime, floatToStr(saveNumber));
      section := iniSections[kSectionBreeding]; // hide this elsewhere
    	saveInt := (unregisteredExportCountBeforeThisSession + unregisteredExportCountThisSession) * kEncryptingMultiplierForUnregisteredExportCount;
      setStringForSectionAndKey(section, kKeyForUnregisteredExportCount, intToStr(saveInt));
      end;
    section := iniSections[kSectionPrefs];
    setStringForSectionAndKey(section, 'Update time series plants on parameter change', boolToStr(updateTimeSeriesPlantsOnParameterChange));
    setStringForSectionAndKey(section, 'Main window view option (all/one)', intToStr(mainWindowViewMode));
    setStringForSectionAndKey(section, 'Distance plant moves with Control-arrow key', intToStr(nudgeDistance));
    setStringForSectionAndKey(section, 'Percent size increase with Control-Shift-up-arrow key', intToStr(resizeKeyUpMultiplierPercent));
    setStringForSectionAndKey(section, 'Parameter panels font size', intToStr(parametersFontSize));
    setStringForSectionAndKey(section, 'Main window orientation (horiz/vert)', intToStr(mainWindowOrientation));
    setStringForSectionAndKey(section, 'Contrast index for lines on polygons', intToStr(lineContrastIndex));
    setStringForSectionAndKey(section, 'Sort 3D objects as one item', boolToStr(sortTdosAsOneItem));
    setStringForSectionAndKey(section, '3D object editor point size', intTostr(circlePointSizeInTdoEditor));
    setStringForSectionAndKey(section, '3D object editor parts', intTostr(partsInTdoEditor));
    setStringForSectionAndKey(section, '3D object editor fill triangles', boolToStr(fillTrianglesInTdoEditor));
    setStringForSectionAndKey(section, '3D object editor draw lines', boolToStr(drawLinesInTdoEditor));
    setStringForSectionAndKey(section, 'Show numerical exceptions window on exception', boolToStr(showWindowOnException));
    setStringForSectionAndKey(section, 'Log to file on exception', boolToStr(logToFileOnException));
    setStringForSectionAndKey(section, 'Ghost hidden parts', boolToStr(showGhostingForHiddenParts));
    setStringForSectionAndKey(section, 'Highlight posed parts', boolToStr(showHighlightingForNonHiddenPosedParts));
    setStringForSectionAndKey(section, 'Show posing', boolToStr(showPosingAtAll));
    setStringForSectionAndKey(section, 'Ghosting color', intToStr(ghostingColor));
    setStringForSectionAndKey(section, 'Posed color', intToStr(nonHiddenPosedColor));
    setStringForSectionAndKey(section, 'Posed selected color', intToStr(selectedPosedColor));
    { settings }
    section := iniSections[kSectionSettings];
    setStringForSectionAndKey(section, 'Window position', rectToString(mainWindowRect));
    setStringForSectionAndKey(section, 'Horizontal split', intToStr(horizontalSplitterPos));
    setStringForSectionAndKey(section, 'Vertical split', intToStr(verticalSplitterPos));
    setStringForSectionAndKey(section, 'Numerical exceptions window position', rectToString(debugWindowRect));
    setStringForSectionAndKey(section, 'Undo/redo list window position', rectToString(undoRedoListWindowRect));
    setStringForSectionAndKey(section, '3D object editor window position', rectToString(tdoEditorWindowRect));
    setStringForSectionAndKey(section, 'Breeder position', rectToString(breederWindowRect));
    setStringForSectionAndKey(section, 'Time series position', rectToString(timeSeriesWindowRect));
    // 3d export options
    for i := 1 to k3DExportTypeLast do with exportOptionsFor3D[i] do
      begin
      section := iniSections[self.sectionNumberFor3DExportType(i)];
      typeName := nameFor3DExportType(i);
      // options in common for all
      setStringForSectionAndKey(section, typeName + ' which plants to draw (selected/visible/all)', intToStr(exportType));
      setStringForSectionAndKey(section, typeName + ' layering option (all/by type/by part)', intToStr(layeringOption));
      setStringForSectionAndKey(section, typeName + ' stem cylinder sides', intToStr(stemCylinderFaces));
      setStringForSectionAndKey(section, typeName + ' translate plants to match window positions', boolToStr(translatePlantsToWindowPositions));
      setStringForSectionAndKey(section, typeName + ' length of plant name', intToStr(lengthOfShortName));
      setStringForSectionAndKey(section, typeName + ' write plant number in front of name', boolToStr(writePlantNumberInFrontOfName));
      setStringForSectionAndKey(section, typeName + ' write colors', boolToStr(writeColors));
      setStringForSectionAndKey(section, typeName + ' X rotation before drawing', intToStr(xRotationBeforeDraw));
      setStringForSectionAndKey(section, typeName + ' scaling factor (percent)', intToStr(overallScalingFactor_pct));
      setStringForSectionAndKey(section, typeName + ' press plants', boolToStr(pressPlants));
      setStringForSectionAndKey(section, typeName + ' press dimension (x/y/z)', intToStr(directionToPressPlants));
      setStringForSectionAndKey(section, typeName + ' double sided', boolToStr(makeTrianglesDoubleSided));
      // special options
      if i = kDXF then
        begin
        setStringForSectionAndKey(section, 'DXF colors option (by type/by part/all)', intToStr(dxf_whereToGetColors));
        setStringForSectionAndKey(section, 'DXF whole plant color index', intToStr(dxf_wholePlantColorIndex));
        for j := 0 to kExportPartLast do
          setStringForSectionAndKey(section, 'DXF color indexes ' + intToStr(j+1), intToStr(dxf_plantPartColorIndexes[j]));
        end
      else if i = kPOV then
        begin
        setStringForSectionAndKey(section, 'POV minimum line length to write (mm)', digitValueString(pov_minLineLengthToWrite));
        setStringForSectionAndKey(section, 'POV minimum 3D object scale to write', digitValueString(pov_minTdoScaleToWrite));
        setStringForSectionAndKey(section, 'POV comment out union of plants at end', boolToStr(pov_commentOutUnionAtEnd));
        end
      else if i = kVRML then
        begin
        setStringForSectionAndKey(section, 'VRML version', intToStr(vrml_version));
        end;
      if (i = kPOV) or (i = kVRML) then
        begin
        setStringForSectionAndKey(section, typeName + ' nest leaves with petioles', boolToStr(nest_LeafAndPetiole));
        setStringForSectionAndKey(section, typeName + ' compound leaves', boolToStr(nest_CompoundLeaf));
        setStringForSectionAndKey(section, typeName + ' nest inflorescences', boolToStr(nest_Inflorescence));
        setStringForSectionAndKey(section, typeName + ' nest flowers/fruits with pedicels', boolToStr(nest_PedicelAndFlowerFruit));
        setStringForSectionAndKey(section, typeName + ' nest pistils and stamens', boolToStr(nest_FloralLayers));
        end;
      end;
    { wizard }
    section := iniSections[kSectionWizard];
    for i := 1 to kMaxWizardQuestions do
      setStringForSectionAndKey(section, 'Wizard question ' + intToStr(i), wizardChoices[i]);
    for i := 1 to kMaxWizardColors do
      setStringForSectionAndKey(section, 'Wizard colors ' + intToStr(i), intToStr(wizardColors[i]));
    for i := 1 to kMaxWizardTdos do
      setStringForSectionAndKey(section, 'Wizard 3D objects ' + intToStr(i), wizardTdoNames[i]);
    setStringForSectionAndKey(section, 'Wizard show fruit', boolToStr(wizardShowFruit));
    // custom colors
    section := iniSections[kCustomColors];
    for i := 0 to kMaxCustomColors-1 do
      setStringForSectionAndKey(section, 'Custom color ' + intToStr(i+1), intToStr(customColors[i]));
    end;
  with bitmapOptions do
    begin
    { export }
    section := iniSections[kSectionExport];
    setStringForSectionAndKey(section, 'Which plants to draw (selected/visible/all/drawing)', intToStr(exportType));
    setStringForSectionAndKey(section, 'Colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)', intToStr(ord(colorType)));
    setStringForSectionAndKey(section, 'Resolution (pixels per inch)', intToStr(resolution_pixelsPerInch));
    setStringForSectionAndKey(section, 'Picture width (pixels)', intToStr(width_pixels));
    setStringForSectionAndKey(section, 'Picture height (pixels)', intToStr(height_pixels));
    setStringForSectionAndKey(section, 'Picture width (inches)', digitValueString(width_in));
    setStringForSectionAndKey(section, 'Picture height (inches)', digitValueString(height_in));
    setStringForSectionAndKey(section, 'Preserve aspect ratio', boolToStr(preserveAspectRatio));
    setStringForSectionAndKey(section, 'JPEG compression quality ratio (1-100)', intToStr(jpegCompressionRatio));
    { printing }
    section := iniSections[kSectionPrinting];
    setStringForSectionAndKey(section, 'Preserve aspect ratio', boolToStr(printPreserveAspectRatio));
    setStringForSectionAndKey(section, 'Print width (inches)', digitValueString(printWidth_in));
    setStringForSectionAndKey(section, 'Print height (inches)', digitValueString(printHeight_in));
    setStringForSectionAndKey(section, 'Print left margin (inches)', digitValueString(printLeftMargin_in));
    setStringForSectionAndKey(section, 'Print top margin (inches)', digitValueString(printTopMargin_in));
    setStringForSectionAndKey(section, 'Print right margin (inches)', digitValueString(printRightMargin_in));
    setStringForSectionAndKey(section, 'Print bottom margin (inches)', digitValueString(printBottomMargin_in));
    setStringForSectionAndKey(section, 'Print inner border', boolToStr(printBorderInner));
    setStringForSectionAndKey(section, 'Print outer border', boolToStr(printBorderOuter));
    setStringForSectionAndKey(section, 'Inner border width (pixels)', intToStr(printBorderWidthInner));
    setStringForSectionAndKey(section, 'Outer border width (pixels)', intToStr(printBorderWidthOuter));
    setStringForSectionAndKey(section, 'Inner border color', intToStr(printBorderColorInner));
    setStringForSectionAndKey(section, 'Outer border color', intToStr(printBorderColorOuter));
    end;
  with breedingAndTimeSeriesOptions do
    begin
    section := iniSections[kSectionBreeding];
    setStringForSectionAndKey(section, 'Plants per generation', intToStr(plantsPerGeneration));
    setStringForSectionAndKey(section, 'Variation (low/med/high/custom/none)', intToStr(variationType));
    setStringForSectionAndKey(section, 'Percent max age', intToStr(percentMaxAge));
    setStringForSectionAndKey(section, 'Thumbnail width', intToStr(thumbnailWidth));
    setStringForSectionAndKey(section, 'Thumbnail height', intToStr(thumbnailHeight));
    setStringForSectionAndKey(section, 'Max generations', intToStr(maxGenerations));
    setStringForSectionAndKey(section, 'Time series stages', intToStr(numTimeSeriesStages));
    for i := 0 to kMaxBreedingSections - 1 do
      setStringForSectionAndKey(section, 'Mutation ' + intToStr(i+1), intToStr(mutationStrengths[i]));
    for i := 0 to kMaxBreedingSections - 1 do
      setStringForSectionAndKey(section, 'First plant weight ' + intToStr(i+1), intToStr(firstPlantWeights[i]));
    setStringForSectionAndKey(section, 'Non-numeric', intToStr(getNonNumericalParametersFrom));
    setStringForSectionAndKey(section, 'Vary colors', boolToStr(mutateAndBlendColorValues));
    setStringForSectionAndKey(section, 'Vary 3D objects', boolToStr(chooseTdosRandomlyFromCurrentLibrary));
    end;
  with nozzleOptions do
    begin
    section := iniSections[kSectionNozzle];
    setStringForSectionAndKey(section, 'Which plants to make nozzle from (selected/visible/all)', intToStr(exportType));
    setStringForSectionAndKey(section, 'Nozzle resolution', intToStr(resolution_pixelsPerInch));
    setStringForSectionAndKey(section, 'Nozzle colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)', intToStr(ord(colorType)));
    setStringForSectionAndKey(section, 'Nozzle background color', intToStr(backgroundColor));
    end;
  with animationOptions do
    begin
    section := iniSections[kSectionAnimation];
    setStringForSectionAndKey(section, 'Animate by (x rotation/age)', intToStr(animateBy));
    setStringForSectionAndKey(section, 'X rotation increment', intToStr(xRotationIncrement));
    setStringForSectionAndKey(section, 'Age increment', intToStr(ageIncrement));
    setStringForSectionAndKey(section, 'Resolution', intToStr(resolution_pixelsPerInch));
    setStringForSectionAndKey(section, 'Animation colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)', intToStr(ord(colorType)));
    end;
  // write parameter overrides
  section := iniSections[kSectionOverrides];
  if parameterManager.parameters.count > 0 then
    for i := 0 to parameterManager.parameters.count - 1 do
      begin
      param := PdParameter(parameterManager.parameters.items[i]);
      if (not param.cannotOverride) and (param.isOverridden) then
        // v2.1 added section name to override key
        setStringForSectionAndKey(section, param.originalSectionName + ': ' + param.name,
          digitValueString(param.lowerBoundOverride) + ' ' +
          digitValueString(param.upperBoundOverride) + ' ' +
          '(' + param.defaultValueStringOverride + ')');
      end;
  iniLines.saveToFile(iniFileName);
  finally
    iniFileChanged := false;
  end;
  end;
                   
procedure PdDomain.boundProfileInformation;
  var
    i, j: smallint;
  begin
  with options do
    begin
    resizeRectSize := intMax(2, intMin(20, resizeRectSize));
    pasteRectSize := intMax(50, intMin(500, pasteRectSize));
    memoryLimitForPlantBitmaps_MB := intMax(1, intMin(200, memoryLimitForPlantBitmaps_MB));
    maxPartsPerPlant_thousands := intMax(1, intMin(100, maxPartsPerPlant_thousands));
    horizontalSplitterPos := intMax(50, horizontalSplitterPos);
    verticalSplitterPos := intMax(30, verticalSplitterPos);
    nudgeDistance := intMax(1, intMin(100, nudgeDistance));
    resizeKeyUpMultiplierPercent := intMax(100, intMin(200, resizeKeyUpMultiplierPercent));
    parametersFontSize := intMax(6, intMin(20, parametersFontSize));
    mainWindowOrientation := intMax(0, intMin(kMaxMainWindowOrientations, mainWindowOrientation));
    undoLimit := intMax(0, intMin(1000, undoLimit));
    undoLimitOfPlants := intMax(0, intMin(500, undoLimitOfPlants));
    circlePointSizeInTdoEditor := intMax(1, intMin(30, circlePointSizeInTdoEditor));
    partsInTdoEditor := intMax(1, intMin(30, partsInTdoEditor));
    lineContrastIndex := intMax(0, intMin(10, lineContrastIndex));
    drawSpeed := intMax(0, intMin(kDrawCustom, drawSpeed));
    end;
  with bitmapOptions do
    begin
    exportType := intMax(0, intMin(kMaxIncludeOption, exportType));
    colorType := TPixelFormat(intMax(0, intMin(kMaxColorOption, ord(colorType))));
    resolution_pixelsPerInch := intMax(kMinResolution, intMin(kMaxResolution, resolution_pixelsPerInch));
    width_pixels := intMax(kMinPixels, intMin(kMaxPixels, width_pixels));
    height_pixels := intMax(kMinPixels, intMin(kMaxPixels, height_pixels));
    width_in := max(kMinInches, min(kMaxInches, width_in));
    height_in := max(kMinInches, min(kMaxInches, height_in));
    printWidth_in := max(kMinInches, min(kMaxInches, printWidth_in));
    printHeight_in := max(kMinInches, min(kMaxInches, printHeight_in));
    printLeftMargin_in := max(kMinInches, min(kMaxInches, printLeftMargin_in));
    printTopMargin_in := max(kMinInches, min(kMaxInches, printTopMargin_in));
    printRightMargin_in := max(kMinInches, min(kMaxInches, printRightMargin_in));
    printBottomMargin_in := max(kMinInches, min(kMaxInches, printBottomMargin_in));
    printBorderWidthInner := intMax(0, intMin(1000, printBorderWidthInner));
    printBorderWidthOuter := intMax(0, intMin(1000, printBorderWidthOuter));
    end;
  with breedingAndTimeSeriesOptions do
    begin
    plantsPerGeneration := intMax(1, intMin(100, plantsPerGeneration));
    variationType := intMax(0, intMin(4, variationType));
    percentMaxAge := intMax(1, intMin(100, percentMaxAge));
    thumbnailWidth := intMin(200, intMax(30, thumbnailWidth));
    thumbnailHeight := intMin(200, intMax(30, thumbnailHeight));
    maxGenerations := intMax(20, intMin(500, maxGenerations));
    numTimeSeriesStages := intMax(1, intMin(100, numTimeSeriesStages)); 
    for i := 0 to kMaxBreedingSections - 1 do
      mutationStrengths[i] := intMax(0, intMin(100, mutationStrengths[i]));
    for i := 0 to kMaxBreedingSections - 1 do
      firstPlantWeights[i] := intMax(0, intMin(100, firstPlantWeights[i]));
    getNonNumericalParametersFrom := intMax(0, intMin(5, getNonNumericalParametersFrom));
    end;
  with nozzleOptions do
    begin
    exportType := intMax(0, intMin(kIncludeAllPlants, exportType));
    resolution_pixelsPerInch := intMax(kMinResolution, intMin(kMaxResolution, resolution_pixelsPerInch));
    end;
  with animationOptions do
    begin
    animateBy := intMax(0, intMin(kAnimateByAge, animateBy));
    xRotationIncrement := intMax(-360, intMin(360, xRotationIncrement));
    ageIncrement := intMax(0, intMin(1000, ageIncrement)); // will check against max plant age later
    resolution_pixelsPerInch := intMax(kMinResolution, intMin(kMaxResolution, resolution_pixelsPerInch));
    end;
  for i := 1 to k3DExportTypeLast do with exportOptionsFor3D[i] do
    begin
    exportType := intMax(0, intMin(kIncludeAllPlants, exportType));
    layeringOption := intMax(kLayerOutputAllTogether, intMin(kLayerOutputByPlantPart, layeringOption));
    stemCylinderFaces := intMax(kMinOutputCylinderFaces, intMin(kMaxOutputCylinderFaces, stemCylinderFaces));
    lengthOfShortName := intMax(1, intMin(60, lengthOfShortName));
    xRotationBeforeDraw := intMax(-180, intMin(180, xRotationBeforeDraw));
    overallScalingFactor_pct := intMax(1, intMin(10000, overallScalingFactor_pct));
    directionToPressPlants := intMax(kX, intMin(kZ, directionToPressPlants));
    dxf_whereToGetColors := intMax(kColorDXFFromPlantPartType, intMin(kColorDXFFromOneColor, dxf_whereToGetColors));
    dxf_wholePlantColorIndex := intMax(0, intMin(kLastDxfColorIndex, dxf_wholePlantColorIndex));
    for j := 0 to kExportPartLast do
      dxf_plantPartColorIndexes[j] := intMax(0, intMin(kLastDxfColorIndex, dxf_plantPartColorIndexes[j]));
    pov_minLineLengthToWrite := max(0.0, min(100.0, pov_minLineLengthToWrite));
    pov_minTdoScaleToWrite := max(0.0, min(100.0, pov_minTdoScaleToWrite));
    vrml_version := intMax(kVRMLVersionOne, intMin(kVRMLVersionTwo, vrml_version));
    end;
  end;

{ --------------------------------------------------------------------------- plant file i/o }
procedure PdDomain.load(fileName: string);
  var extension: string;
  begin
  plantFileLoaded := false;
  try
    plantFileName := fileName;
    plantFileName := ExpandFileName(plantFileName);
    // v2.1 check for file extension - when opening file on startup or send to
    extension := lowerCase(stringBeyond(ExtractFileName(plantFileName), '.'));
    if extension <> 'pla' then
      showMessage('The file (' + plantFileName + ') does not have the correct extension (pla).')
    else
      begin
      plantManager.loadPlantsFromFile(fileName, kNotInPlantMover);
      plantFileLoaded := true;
      if MainForm <> nil then MainForm.setPlantFileChanged(false);
      lastOpenedPlantFileName := plantFileName;
      lastOpenedPlantFileName := trim(lastOpenedPlantFileName);
      self.updateRecentFileNames(lastOpenedPlantFileName);  // v1.60
      end;
  except
    plantFileLoaded := false;
    raise; {callers need exception}
  end;
  end;
                                                            
procedure PdDomain.save(fileName: string);
  begin
  plantManager.savePlantsToFile(fileName, kNotInPlantMover);
  end;

// v1.60
procedure PdDomain.updateRecentFileNames(const aFileName: string);
  var
    i: smallint;
    saved: boolean;
  begin
  // first look to see if the file is already there, and if so don't record it twice
  for i := 0 to kMaxRecentFiles - 1 do if options.recentFiles[i] = aFileName then exit;
  // now look for an empty spot in the array
  saved := false;
  for i := 0 to kMaxRecentFiles - 1 do
    if options.recentFiles[i] = '' then
      begin
      options.recentFiles[i] := aFileName;
      saved := true;
      break;
      end;
  // if there was no empty spot, shift the files up one and add it to the end
  if not saved then
    for i := 0 to kMaxRecentFiles - 1 do
      if i < kMaxRecentFiles - 1 then
        options.recentFiles[i] := options.recentFiles[i+1]
      else
        options.recentFiles[i] := aFileName;
  // PDF PORTING -- maybe syntax error in original -- had empty parens -- unless intended as procedure or fucntion call from pointer? Probably nt
  if MainForm <> nil then MainForm.updateFileMenuForOtherRecentFiles;
  end;

procedure PdDomain.resetForEmptyPlantFile;
  begin
  plantManager.plants.clear;
  plantFileLoaded := true;
  plantFileName := kUnsavedFileName + '.' + extensionForFileType(kFileTypePlant);
  lastOpenedPlantFileName := '';
  if MainForm <> nil then MainForm.setPlantFileChanged(false);
  end;

procedure PdDomain.resetForNoPlantFile;
  begin
  plantManager.plants.clear;
  plantFileLoaded := false;
  plantFileName := '';
  lastOpenedPlantFileName := '';
  if MainForm <> nil then MainForm.setPlantFileChanged(false);
  end;

function PdDomain.checkForExistingDefaultTdoLibrary: boolean;
  begin
  // returns false if user wants to cancel action
  result := true;
  if not fileExists(defaultTdoLibraryFileName) then
    begin
    messageDlg('No 3D object library has been chosen.' + chr(13) + chr(13)
      + 'In order to continue with what you are doing,' + chr(13)
      + 'you need to choose a 3D object library' + chr(13)
      + 'from the dialog that follows this one.',
      mtWarning, [mbOk], 0);
    defaultTdoLibraryFileName := getFileOpenInfo(kFileTypeTdo, defaultTdoLibraryFileName,
      'Choose a 3D object library (tdo) file');
    result := defaultTdoLibraryFileName <> '';
    end;
 end;

function PdDomain.totalUnregisteredExportsAtThisMoment: smallint;
  begin
  result := unregisteredExportCountBeforeThisSession + unregisteredExportCountThisSession;
  end;

{ ------------------------------------------------------------------- file/directory utilities }
function PdDomain.nameIsAbsolute(const fileName: string): boolean;
  begin
  result := ((pos('\', fileName) = 1) or (pos(':', fileName) = 2));
  end;

function PdDomain.isFileInPath(const fileName: string): boolean;
  var
    qualifiedName: string;
  begin
  result := true;
  {see if file exists}
  qualifiedName := fileName;
  if not FileExists(qualifiedName) then
    begin
    {this merging process could be more sophisticated in case
     file name has leading drive or leading slash - just not merging for now}
    if not self.nameIsAbsolute(fileName) then
      qualifiedName := ExtractFilePath(Application.exeName) + fileName;
    if not FileExists(qualifiedName) then
      begin
      result := false;
      end;
    end;
  end;

{searches for file according to name, and then in exe directory, and then gives up}
function PdDomain.buildFileNameInPath(const fileName: string): string;
  begin
  result := ExpandFileName(fileName);
  if FileExists(result) then exit;
  result := ExtractFilePath(Application.exeName) + ExtractFileName(fileName);
  if FileExists(result) then exit;
  result := fileName;
  end;

function PdDomain.firstUnusedUnsavedFileName: string;
  var
    fileNumber: smallint;
  begin
  result := '';
  fileNumber := 1;
  while fileNumber < 100 do
    begin
    result := ExtractFilePath(Application.exeName) + unsavedFileNameForNumber(fileNumber);
    if not fileExists(result) then
      exit;
    inc(fileNumber);
    end;
  showMessage('Too many unnamed plant files. Delete some to reuse names.');
  end;

function PdDomain.unsavedFileNameForNumber(aNumber: smallint): string;
  var
    numberString: string;
  begin
  numberString := intToStr(aNumber);
  if length(numberString) = 1 then
    numberString := '0' + numberString;
  result := kUnsavedFileName + numberString + '.pla';
  end;

function PdDomain.getColorUsingCustomColors(originalColor: TColorRef): TColorRef;
  var
    colorDialog: TColorDialog;
    i: smallint;
    colorString: string;
    color: TColorRef;
  begin
  // may be more efficient to do this from main window, because a colorDialog component on the form
  // would keep the custom colors between uses without having to change the domain colors
  result := originalColor;
  colorDialog := TColorDialog.create(Application);
  colorDialog.color := originalColor;
  colorDialog.customColors.clear;
  // add new color to custom colors if not already there and there is room
  // (this assumes they don't want black as a custom color)
  for i := 0 to kMaxCustomColors-1 do
    begin
    if options.customColors[i] = originalColor then
      break;
    if options.customColors[i] = clBlack then
      begin
      options.customColors[i] := originalColor;
      break;
      end;
    end;
  // load our custom colors into color dialog custom colors
  for i := 0 to kMaxCustomColors-1 do
    begin
    colorString := 'Color' + chr(ord('A') + i) + '=' + Format('%.6x', [options.customColors[i]]);
    colorDialog.customColors.add(colorString);
    end;
  colorDialog.options := [cdFullOpen];
  try
    if colorDialog.execute then
      begin
      result := colorDialog.color;
      for i := 0 to colorDialog.customColors.count - 1 do
        begin
        colorString := colorDialog.customColors[i];
        colorString := stringBeyond(colorString, '=');
        color := strToIntDef('$' + colorString, 0);
        options.customColors[i] := color;
        end;
      end;
  finally
    colorDialog.free;
  end;
  end;

function PdDomain.sectionNumberFor3DExportType(anOutputType: smallint): smallint;
  begin
  case anOutputType of
    kDXF: result := kSectionDXF;
    kPOV: result := kSectionPOV;
    k3DS: result := kSection3DS;
    kOBJ: result := kSectionOBJ;
    kVRML: result := kSectionVRML;
    kLWO: result := kSectionLWO;
    else raise Exception.create('Problem: Invalid type in PdDomain.sectionNumberFor3DExportType.');
    end;
  end;

function PdDomain.plantDrawOffset_mm: SinglePoint;
  begin
  result := setSinglePoint(0, 0);
  if plantManager = nil then exit;
  result := plantManager.plantDrawOffset_mm;
  end;

function PdDomain.plantDrawScale_PixelsPerMm: single;
  begin
  result := 1.0;
  if plantManager = nil then exit;
  result := plantManager.plantDrawScale_PixelsPerMm;
  end;

function PdDomain.viewPlantsInMainWindowFreeFloating: boolean;
  begin
  result := options.mainWindowViewMode =  kViewPlantsInMainWindowFreeFloating;
  end;

function PdDomain.viewPlantsInMainWindowOnePlantAtATime: boolean;
  begin
  result := options.mainWindowViewMode =  kViewPlantsInMainWindowOneAtATime;
  end;

end.
