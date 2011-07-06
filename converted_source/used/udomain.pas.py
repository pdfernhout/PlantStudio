# unit Udomain

from conversion_common import *
import uwait
import usstream
import uregistersupport
import uwizard
import umain
import utimeser
import usplash
import umath
import usupport
import u3dexport
import uhints
import usection
import uparams
import uplant
import uplantmn
import delphi_compatability

# const
kMaxWizardQuestions = 30
kMaxWizardColors = 2
kMaxWizardTdos = 3
kMainWindowOrientationHorizontal = 0
kMainWindowOrientationVertical = 1
kMaxMainWindowOrientations = 1
kIncludeSelectedPlants = 0
kIncludeVisiblePlants = 1
kIncludeAllPlants = 2
kIncludeDrawingAreaContents = 3
kMaxIncludeOption = 3
kBreederVariationLow = 0
kBreederVariationMedium = 1
kBreederVariationHigh = 2
kBreederVariationCustom = 3
kBreederVariationNoNumeric = 4
kNoMutation = 0
kLowMutation = 20
kMediumMutation = 60
kHighMutation = 100
kMaxColorOption = 7
kMinResolution = 10
kMaxResolution = 10000
kDefaultResolution = 200
kMinPixels = 10
kMaxPixels = 10000
kMinInches = 0.0
kMaxInches = 100
kExcludeInvisiblePlants = true
kIncludeInvisiblePlants = false
kExcludeNonSelectedPlants = true
kIncludeNonSelectedPlants = false
kMaxCustomColors = 16
kAnimateByXRotation = 0
kAnimateByAge = 1
kDrawFast = 0
kDrawMedium = 1
kDrawBest = 2
kDrawCustom = 3
kMinOutputCylinderFaces = 3
kMaxOutputCylinderFaces = 20
kDefaultV1IniFileName = "PlantStudio.ini"
kDefaultV2IniFileName = "PlantStudio2.ini"
kV2IniAddition = "_v2"
kMaxRecentFiles = 10
kViewPlantsInMainWindowFreeFloating = 1
kViewPlantsInMainWindowOneAtATime = 2
kMaxUnregExportsAllowed = 20
kMaxUnregExportsPerSessionAfterMaxReached = 2
kInPlantMover = true
kNotInPlantMover = false

#pf32bit 
# v1.60
# record
class BitmapOptionsStructure:
    def __init__(self):
        self.exportType = 0
        self.colorType = TPixelFormat()
        self.resolution_pixelsPerInch = 0
        self.width_pixels = 0
        self.height_pixels = 0
        self.width_in = 0.0
        self.height_in = 0.0
        self.preserveAspectRatio = false
        self.jpegCompressionRatio = 0
        self.printPreserveAspectRatio = false
        self.printBorderInner = false
        self.printBorderOuter = false
        self.printWidth_in = 0.0
        self.printHeight_in = 0.0
        self.printLeftMargin_in = 0.0
        self.printTopMargin_in = 0.0
        self.printRightMargin_in = 0.0
        self.printBottomMargin_in = 0.0
        self.printBorderWidthInner = 0
        self.printBorderWidthOuter = 0
        self.borderThickness = 0
        self.borderGap = 0
        self.printBorderColorInner = TColorRef()
        self.printBorderColorOuter = TColorRef()

# 1 to 100
# don't save these, they are for storing to use during printing only
# record
class NozzleOptionsStructure:
    def __init__(self):
        self.exportType = 0
        self.resolution_pixelsPerInch = 0
        self.colorType = TPixelFormat()
        self.backgroundColor = TColorRef()
        self.cellSize = TPoint()
        self.cellCount = 0

# don't save in settings
# don't save in settings
# record
class NumberedAnimationOptionsStructure:
    def __init__(self):
        self.animateBy = 0
        self.xRotationIncrement = 0
        self.ageIncrement = 0
        self.resolution_pixelsPerInch = 0
        self.colorType = TPixelFormat()
        self.frameCount = 0
        self.scaledSize = TPoint()
        self.fileSize = 0L

# don't save in settings
# don't save in settings
# don't save in settings
# record
class DomainOptionsStructure:
    def __init__(self):
        self.hideWelcomeForm = false
        self.openMostRecentFileAtStart = false
        self.ignoreWindowSettingsInFile = false
        self.cachePlantBitmaps = false
        self.memoryLimitForPlantBitmaps_MB = 0
        self.maxPartsPerPlant_thousands = 0
        self.backgroundColor = TColorRef()
        self.transparentColor = TColorRef()
        self.showSelectionRectangle = false
        self.showBoundsRectangle = false
        self.resizeRectSize = 0
        self.pasteRectSize = 0
        self.firstSelectionRectangleColor = TColorRef()
        self.multiSelectionRectangleColor = TColorRef()
        self.draw3DObjects = false
        self.drawStems = false
        self.fillPolygons = false
        self.drawSpeed = 0
        self.drawLinesBetweenPolygons = false
        self.sortPolygons = false
        self.draw3DObjectsAsBoundingRectsOnly = false
        self.showPlantDrawingProgress = false
        self.useMetricUnits = false
        self.undoLimit = 0
        self.undoLimitOfPlants = 0
        self.rotationIncrement = 0
        self.showLongHintsForButtons = false
        self.showHintsForParameters = false
        self.pauseBeforeHint = 0
        self.pauseDuringHint = 0
        self.noteEditorWrapLines = false
        self.updateTimeSeriesPlantsOnParameterChange = false
        self.mainWindowViewMode = 0
        self.nudgeDistance = 0
        self.resizeKeyUpMultiplierPercent = 0
        self.parametersFontSize = 0
        self.mainWindowOrientation = 0
        self.lineContrastIndex = 0
        self.sortTdosAsOneItem = false
        self.circlePointSizeInTdoEditor = 0
        self.partsInTdoEditor = 0
        self.fillTrianglesInTdoEditor = false
        self.drawLinesInTdoEditor = false
        self.showGhostingForHiddenParts = false
        self.showHighlightingForNonHiddenPosedParts = false
        self.showPosingAtAll = false
        self.ghostingColor = TColorRef()
        self.nonHiddenPosedColor = TColorRef()
        self.selectedPosedColor = TColorRef()
        self.showWindowOnException = false
        self.logToFileOnException = false
        self.wizardChoices = [0] * (range(1, kMaxWizardQuestions + 1) + 1)
        self.wizardColors = [0] * (range(1, kMaxWizardColors + 1) + 1)
        self.wizardTdoNames = [0] * (range(1, kMaxWizardTdos + 1) + 1)
        self.wizardShowFruit = false
        self.customColors = [0] * (range(0, kMaxCustomColors) + 1)
        self.recentFiles = [0] * (range(0, kMaxRecentFiles) + 1)

# var
domain = PdDomain()

# const
kUnsavedFileName = "untitled"
kSectionFiles = 0
kSectionPrefs = 1
kSectionSettings = 2
kSectionDXF = 3
kSectionWizard = 4
kSectionExport = 5
kSectionPrinting = 6
kCustomColors = 7
kSectionBreeding = 8
kSectionNozzle = 9
kSectionAnimation = 10
kSectionRegistration = 11
kSectionOverrides = 12
kSectionPOV = 13
kSection3DS = 14
kSectionOBJ = 15
kSectionVRML = 16
kSectionLWO = 17
kSectionOtherRecentFiles = 18
kLastSectionNumber = 18
iniSections = ["Files", "Preferences", "Settings", "DXF", "Wizard", "Picture export", "Printing", "Custom colors", "Breeding", "Nozzles", "Animation", "Registration", "Overrides", "POV", "3DS", "OBJ", "VRML", "LWO", "Other recent files", ]
kStandardTdoLibraryFileName = "3D object library.tdo"
kEncryptingMultiplierForAccumulatedUnregisteredTime = 20
kEncryptingMultiplierForUnregisteredExportCount = 149
kKeyForAccumulatedUnregisteredTime = "Time scale fraction"
kKeyForUnregisteredExportCount = "Frame count"
kGetKeys = true
kGetValues = false

# v2.1
# v2.0
#seconds
#seconds
# v1.4
#cfk change length if needed
class PdDomain(TObject):
    def __init__(self):
        self.plantFileName = ""
        self.lastOpenedPlantFileName = ""
        self.plantFileLoaded = false
        self.options = DomainOptionsStructure()
        self.breedingAndTimeSeriesOptions = BreedingAndTimeSeriesOptionsStructure()
        self.bitmapOptions = BitmapOptionsStructure()
        self.exportOptionsFor3D = [0] * (range(1, u3dexport.k3DExportTypeLast + 1) + 1)
        self.nozzleOptions = NozzleOptionsStructure()
        self.animationOptions = NumberedAnimationOptionsStructure()
        self.registered = false
        self.justRegistered = false
        self.startTimeThisSession = TDateTime()
        self.accumulatedUnregisteredTime = TDateTime()
        self.registrationName = ""
        self.registrationCode = ""
        self.unregisteredExportCountBeforeThisSession = 0
        self.unregisteredExportCountThisSession = 0
        self.plantManager = PdPlantManager()
        self.parameterManager = PdParameterManager()
        self.sectionManager = PdSectionManager()
        self.hintManager = PdHintManager()
        self.iniFileName = ""
        self.iniFileBackupName = ""
        self.useIniFile = false
        self.defaultTdoLibraryFileName = ""
        self.mainWindowRect = TRect()
        self.horizontalSplitterPos = 0
        self.verticalSplitterPos = 0
        self.breederWindowRect = TRect()
        self.timeSeriesWindowRect = TRect()
        self.debugWindowRect = TRect()
        self.undoRedoListWindowRect = TRect()
        self.tdoEditorWindowRect = TRect()
        self.temporarilyHideSelectionRectangles = false
        self.drawingToMakeCopyBitmap = false
        self.plantDrawScaleWhenDrawingCopy_PixelsPerMm = 0.0
        self.plantDrawOffsetWhenDrawingCopy_mm = SinglePoint()
        self.iniLines = TStringList()
        self.gotInfoFromV1IniFile = false
    
    # registration
    # managers 
    # support files 
    # for remembering settings 
    # for temporary use while drawing 
    # for making copy bitmap with different resolution than screen 
    # ------------------------------------------------------------------------------- creation/destruction
    def createDefault(self):
        result = false
        domain = PdDomain().create()
        result = domain.startupLoading()
        return result
    
    def destroyDefault(self):
        domain.free
        domain = None
    
    def create(self):
        TObject.create(self)
        # v1.5
        usupport.setDecimalSeparator()
        # create empty managers 
        self.plantManager = uplantmn.PdPlantManager().create()
        self.parameterManager = uparams.PdParameterManager().create()
        self.sectionManager = usection.PdSectionManager().create()
        self.hintManager = uhints.PdHintManager().create()
        self.iniLines = delphi_compatability.TStringList.create
        # non-standard defaults 
        self.plantManager.plantDrawScale_PixelsPerMm = 1.0
        self.plantDrawScaleWhenDrawingCopy_PixelsPerMm = 1.0
        return self
    
    def destroy(self):
        self.plantManager.free
        self.plantManager = None
        self.parameterManager.free
        self.parameterManager = None
        self.sectionManager.free
        self.sectionManager = None
        self.hintManager.free
        self.hintManager = None
        self.iniLines.free
        self.iniLines = None
        TObject.destroy(self)
    
    def windowsDirectory(self):
        result = ""
        cString = [0] * (range(0, 255 + 1) + 1)
        
        result = ""
        UNRESOLVED.getWindowsDirectory(cString, 256)
        result = UNRESOLVED.strPas(cString)
        return result
    
    # ------------------------------------------------------------------------------- loading
    def startupLoading(self):
        result = false
        i = 0
        iniFileFound = false
        year = 0
        month = 0
        day = 0
        v1IniFileName = ""
        
        result = true
        self.iniFileName = kDefaultV2IniFileName
        self.useIniFile = true
        self.plantFileName = ""
        if usplash.splashForm != None:
            usplash.splashForm.showLoadingString("Starting...")
        if UNRESOLVED.ParamCount > 0:
            for i in range(1, UNRESOLVED.ParamCount + 1):
                if uppercase(UNRESOLVED.ParamStr(i)) == "/I=":
                    # ============= parse command line options 
                    self.useIniFile = false
                elif uppercase(UNRESOLVED.ParamStr(i)) == "/I":
                    self.useIniFile = false
                elif UNRESOLVED.pos("/I=", uppercase(UNRESOLVED.ParamStr(i))) == 1:
                    self.iniFileName = UNRESOLVED.copy(UNRESOLVED.ParamStr(i), 4, len(UNRESOLVED.ParamStr(i)))
                elif UNRESOLVED.pos("/I", uppercase(UNRESOLVED.ParamStr(i))) == 1:
                    self.iniFileName = UNRESOLVED.copy(UNRESOLVED.ParamStr(i), 3, len(UNRESOLVED.ParamStr(i)))
                elif (self.plantFileName == "") and (UNRESOLVED.pos("/", uppercase(UNRESOLVED.ParamStr(i))) != 1):
                    self.plantFileName = UNRESOLVED.ParamStr(i)
                else:
                    ShowMessage("Improper parameter string " + UNRESOLVED.ParamStr(i))
        # make parameters
        self.parameterManager.makeParameters()
        # make hints
        self.hintManager.makeHints()
        # v2.0
        # reconcile v2 and v1 ini files
        # only do this if they did NOT specify an alternate file
        # if they specified an alternate file, there is no way to know what version it is;
        # just read it as v1 and write it as v2 (do not expect this to be common use)
        # if they asked NOT to read any ini file, skip doing this
        self.gotInfoFromV1IniFile = false
        if (self.useIniFile) and (self.iniFileName == kDefaultV2IniFileName):
            if not FileExists(self.windowsDirectory() + "\\" + self.iniFileName):
                # if no v2 ini file but there is a v1 ini file, read the v1 ini file NOW but do not change the name for writing out
                v1IniFileName = self.windowsDirectory() + "\\" + kDefaultV1IniFileName
                if FileExists(v1IniFileName):
                    self.getProfileInformationFromFile(v1IniFileName)
                    self.gotInfoFromV1IniFile = true
        if ExtractFilePath(self.iniFileName) != "":
            # find out if ini file exists now, because if it doesn't we should save the profile info when leaving
            #    even if it did not change. if iniFileName does not have a directory, use Windows directory 
            iniFileFound = FileExists(self.iniFileName)
            if not iniFileFound:
                ShowMessage("Could not find alternate settings file " + chr(13) + chr(13) + "  " + self.iniFileName + chr(13) + chr(13) + "Using standard settings file in Windows directory instead.")
                self.iniFileName = kDefaultV2IniFileName
                iniFileFound = FileExists(self.windowsDirectory() + "\\" + self.iniFileName)
                self.iniFileName = self.windowsDirectory() + "\\" + self.iniFileName
        else:
            iniFileFound = FileExists(self.windowsDirectory() + "\\" + self.iniFileName)
            self.iniFileName = self.windowsDirectory() + "\\" + self.iniFileName
        usupport.iniFileChanged = not iniFileFound
        if iniFileFound and self.useIniFile:
            # ============= if ini file doesn't exist or don't want, set default options; otherwise read options from ini file 
            # if already read options from v1 ini file, don't default - v2.0
            self.getProfileInformationFromFile(self.iniFileName)
        elif not self.gotInfoFromV1IniFile:
            # defaults options
            self.getProfileInformationFromFile("")
        self.startTimeThisSession = UNRESOLVED.Now
        if self.plantFileName != "":
            try:
                if usplash.splashForm != None:
                    # ============= load plant file from command line if found 
                    usplash.splashForm.showLoadingString("Reading startup file...")
                self.plantFileName = self.buildFileNameInPath(self.plantFileName)
                self.load(self.plantFileName)
            except Exception, E:
                ShowMessage(E.message)
                ShowMessage("Could not open plant file from command line " + self.plantFileName)
        elif (self.useIniFile) and (self.options.openMostRecentFileAtStart):
            # ============= if most recent plant file in INI try it unless -I option 
            # assume ini file has been read by now
            self.plantFileName = self.stringForSectionAndKey("Files", "Recent", self.plantFileName)
            self.plantFileName = self.buildFileNameInPath(self.plantFileName)
            if (self.plantFileName != "") and self.isFileInPath(self.plantFileName):
                try:
                    if usplash.splashForm != None:
                        usplash.splashForm.showLoadingString("Reading most recent file...")
                    self.load(self.plantFileName)
                except Exception, E:
                    ShowMessage(E.message)
                    ShowMessage("Could not load most recently saved plant file " + self.plantFileName)
        # show obsolete warning if unregistered
        UNRESOLVED.DecodeDate(UNRESOLVED.Now, year, month, day)
        if (not self.registered) and (year >= 2003):
            MessageDialog("This version of PlantStudio was released some time ago." + chr(13) + chr(13) + "Please check for an newer version at:" + chr(13) + "  http://www.kurtz-fernhout.com" + chr(13) + chr(13) + "The web site may also have updated pricing information." + chr(13) + chr(13) + "You can still register this copy of the software if you want to, though;" + chr(13) + "this message will disappear when this copy is registered.", mtInformation, [mbOK, ], 0)
        return result
    
    # --------------------------------------------------------------------------------- ini file methods referred to
    def sectionStartIndexInIniLines(self, section):
        result = 0
        i = 0
        aLine = ""
        
        result = -1
        i = 0
        while i <= self.iniLines.Count - 1:
            aLine = trim(self.iniLines.Strings[i])
            if "[" + section + "]" == aLine:
                result = i
                return result
            else:
                i += 1
        return result
    
    def stringForSectionAndKey(self, section, key, defaultString):
        result = ""
        i = 0
        aLine = ""
        
        result = defaultString
        if (self.iniLines == None) or (self.iniLines.Count <= 0):
            return result
        i = self.sectionStartIndexInIniLines(section)
        if i < 0:
            return result
        # move to next after section
        i += 1
        while (i <= self.iniLines.Count - 1):
            # only read up until next section - don't want to get same name from different section
            aLine = trim(self.iniLines.Strings[i])
            if (len(aLine) > 0) and (aLine[1] == "["):
                return result
            if key == trim(usupport.stringUpTo(aLine, "=")):
                result = usupport.stringBeyond(self.iniLines.Strings[i], "=")
                return result
            else:
                i += 1
        return result
    
    def setStringForSectionAndKey(self, section, key, newString):
        i = 0
        found = false
        aLine = ""
        
        if (self.iniLines == None):
            return
        i = self.sectionStartIndexInIniLines(section)
        if i < 0:
            # if no section found, add section at end and add this one item to it
            self.iniLines.Add("[" + section + "]")
            self.iniLines.Add(key + "=" + newString)
            # section found
        else:
            found = false
            # move to next after section
            i += 1
            while (i <= self.iniLines.Count - 1):
                # only read up until next section - don't want to get same name from different section
                aLine = trim(self.iniLines.Strings[i])
                if (len(aLine) > 0) and (aLine[1] == "["):
                    break
                if key == trim(usupport.stringUpTo(self.iniLines.Strings[i], "=")):
                    self.iniLines.Strings[i] = key + "=" + newString
                    found = true
                    break
                else:
                    i += 1
            if not found:
                if i <= self.iniLines.Count - 1:
                    # if there was no match for the key, ADD a line to the section
                    self.iniLines.Insert(i, key + "=" + newString)
                else:
                    self.iniLines.Add(key + "=" + newString)
    
    def readSectionKeysOrValues(self, section, aList, getKeys):
        i = 0
        aLine = ""
        
        if (self.iniLines == None) or (self.iniLines.Count <= 0):
            return
        i = self.sectionStartIndexInIniLines(section)
        if i < 0:
            return
        # move to next after section
        i += 1
        while i <= self.iniLines.Count - 1:
            aLine = trim(self.iniLines.Strings[i])
            if (len(aLine) > 0) and (aLine[1] == "["):
                break
            if getKeys:
                # values
                aList.Add(trim(usupport.stringUpTo(self.iniLines.Strings[i], "=")))
            else:
                aList.Add(usupport.stringBeyond(self.iniLines.Strings[i], "="))
            i += 1
    
    def removeSectionFromIniLines(self, section):
        i = 0
        aLine = ""
        
        if (self.iniLines == None) or (self.iniLines.Count <= 0):
            return
        i = self.sectionStartIndexInIniLines(section)
        if i < 0:
            return
        self.iniLines.Delete(i)
        while (i <= self.iniLines.Count - 1):
            aLine = trim(self.iniLines.Strings[i])
            if (len(aLine) > 0) and (aLine[1] == "["):
                break
            self.iniLines.Delete(i)
    
    # --------------------------------------------------------------------------------- ini file load/save
    def getProfileInformationFromFile(self, fileName):
        i = 0
        j = 0
        section = ""
        typeName = ""
        timeString = ""
        key = ""
        value = ""
        sectionName = ""
        paramName = ""
        readNumber = 0.0
        readInt = 0
        overrideKeys = TStringList()
        overrideValues = TStringList()
        param = PdParameter()
        stream = KfStringStream()
        
        if fileName != "":
            self.iniLines.LoadFromFile(fileName)
        # ------------------------------------------- files
        section = iniSections[kSectionFiles]
        self.defaultTdoLibraryFileName = self.stringForSectionAndKey(section, "3D object library", ExtractFilePath(delphi_compatability.Application.exeName) + "3D object library.tdo")
        # ------------------------------------------- recent files
        section = iniSections[kSectionOtherRecentFiles]
        for i in range(0, kMaxRecentFiles):
            self.options.recentFiles[i] = self.stringForSectionAndKey(section, "File" + IntToStr(i + 1), "")
        # ------------------------------------------- preferences
        section = iniSections[kSectionPrefs]
        self.options.openMostRecentFileAtStart = usupport.strToBool(self.stringForSectionAndKey(section, "Open most recent file at start", "true"))
        self.options.ignoreWindowSettingsInFile = usupport.strToBool(self.stringForSectionAndKey(section, "Ignore window settings saved in files", "false"))
        self.options.cachePlantBitmaps = usupport.strToBool(self.stringForSectionAndKey(section, "Draw plants into separate bitmaps", "true"))
        self.options.memoryLimitForPlantBitmaps_MB = StrToInt(self.stringForSectionAndKey(section, "Memory limit for plant bitmaps (in MB)", "5"))
        self.options.maxPartsPerPlant_thousands = StrToInt(self.stringForSectionAndKey(section, "Max parts per plant (in thousands)", "10"))
        self.options.hideWelcomeForm = usupport.strToBool(self.stringForSectionAndKey(section, "Hide welcome window", "false"))
        self.options.backgroundColor = StrToInt(self.stringForSectionAndKey(section, "Background color", IntToStr(delphi_compatability.clWhite)))
        self.options.transparentColor = StrToInt(self.stringForSectionAndKey(section, "Transparent color", IntToStr(delphi_compatability.clWhite)))
        self.options.showSelectionRectangle = usupport.strToBool(self.stringForSectionAndKey(section, "Show selection rectangle", "true"))
        self.options.showBoundsRectangle = usupport.strToBool(self.stringForSectionAndKey(section, "Show bounding rectangle", "false"))
        self.options.resizeRectSize = StrToInt(self.stringForSectionAndKey(section, "Resizing rectangle size", "6"))
        self.options.pasteRectSize = StrToInt(self.stringForSectionAndKey(section, "Paste rectangle size", "100"))
        self.options.firstSelectionRectangleColor = StrToInt(self.stringForSectionAndKey(section, "First selection rectangle color", IntToStr(delphi_compatability.clRed)))
        self.options.multiSelectionRectangleColor = StrToInt(self.stringForSectionAndKey(section, "Multi selection rectangle color", IntToStr(delphi_compatability.clBlue)))
        self.options.draw3DObjects = usupport.strToBool(self.stringForSectionAndKey(section, "Draw 3D objects", "true"))
        self.options.drawStems = usupport.strToBool(self.stringForSectionAndKey(section, "Draw stems", "true"))
        self.options.fillPolygons = usupport.strToBool(self.stringForSectionAndKey(section, "Fill polygons", "true"))
        self.options.drawSpeed = StrToInt(self.stringForSectionAndKey(section, "Draw speed (boxes/frames/solids)", IntToStr(kDrawBest)))
        self.options.drawLinesBetweenPolygons = usupport.strToBool(self.stringForSectionAndKey(section, "Draw lines between polygons", "true"))
        self.options.sortPolygons = usupport.strToBool(self.stringForSectionAndKey(section, "Sort polygons", "true"))
        self.options.draw3DObjectsAsBoundingRectsOnly = usupport.strToBool(self.stringForSectionAndKey(section, "Draw 3D objects as squares", "false"))
        self.options.showPlantDrawingProgress = usupport.strToBool(self.stringForSectionAndKey(section, "Show drawing progress", "true"))
        self.options.useMetricUnits = usupport.strToBool(self.stringForSectionAndKey(section, "Use metric units", "true"))
        self.options.undoLimit = StrToInt(self.stringForSectionAndKey(section, "Actions to keep in undo list", "50"))
        self.options.undoLimitOfPlants = StrToInt(self.stringForSectionAndKey(section, "Plants to keep in undo list", "10"))
        self.options.rotationIncrement = StrToInt(self.stringForSectionAndKey(section, "Rotation button increment", "10"))
        self.options.showLongHintsForButtons = usupport.strToBool(self.stringForSectionAndKey(section, "Show long hints for buttons", "true"))
        self.options.showHintsForParameters = usupport.strToBool(self.stringForSectionAndKey(section, "Show hints for parameters", "true"))
        self.options.pauseBeforeHint = StrToInt(self.stringForSectionAndKey(section, "Pause before hint", "1"))
        self.options.pauseDuringHint = StrToInt(self.stringForSectionAndKey(section, "Pause during hint", "60"))
        self.options.noteEditorWrapLines = usupport.strToBool(self.stringForSectionAndKey(section, "Wrap lines in note editor", "true"))
        self.options.updateTimeSeriesPlantsOnParameterChange = usupport.strToBool(self.stringForSectionAndKey(section, "Update time series plants on parameter change", "true"))
        self.options.mainWindowViewMode = StrToInt(self.stringForSectionAndKey(section, "Main window view option (all/one)", "0"))
        self.options.nudgeDistance = StrToInt(self.stringForSectionAndKey(section, "Distance plant moves with Control-arrow key", "5"))
        self.options.resizeKeyUpMultiplierPercent = StrToInt(self.stringForSectionAndKey(section, "Percent size increase with Control-Shift-up-arrow key", "110"))
        self.options.parametersFontSize = StrToInt(self.stringForSectionAndKey(section, "Parameter panels font size", "8"))
        self.options.mainWindowOrientation = StrToInt(self.stringForSectionAndKey(section, "Main window orientation (horiz/vert)", "0"))
        self.options.lineContrastIndex = StrToInt(self.stringForSectionAndKey(section, "Contrast index for lines on polygons", "3"))
        self.options.sortTdosAsOneItem = usupport.strToBool(self.stringForSectionAndKey(section, "Sort 3D objects as one item", "true"))
        self.options.circlePointSizeInTdoEditor = StrToInt(self.stringForSectionAndKey(section, "3D object editor point size", "8"))
        self.options.partsInTdoEditor = StrToInt(self.stringForSectionAndKey(section, "3D object editor parts", "1"))
        self.options.fillTrianglesInTdoEditor = usupport.strToBool(self.stringForSectionAndKey(section, "3D object editor fill triangles", "true"))
        self.options.drawLinesInTdoEditor = usupport.strToBool(self.stringForSectionAndKey(section, "3D object editor draw lines", "true"))
        self.options.showWindowOnException = usupport.strToBool(self.stringForSectionAndKey(section, "Show numerical exceptions window on exception", "false"))
        self.options.logToFileOnException = usupport.strToBool(self.stringForSectionAndKey(section, "Log to file on exception", "false"))
        self.options.showGhostingForHiddenParts = usupport.strToBool(self.stringForSectionAndKey(section, "Ghost hidden parts", "false"))
        self.options.showHighlightingForNonHiddenPosedParts = usupport.strToBool(self.stringForSectionAndKey(section, "Highlight posed parts", "true"))
        self.options.showPosingAtAll = usupport.strToBool(self.stringForSectionAndKey(section, "Show posing", "true"))
        self.options.ghostingColor = StrToInt(self.stringForSectionAndKey(section, "Ghosting color", IntToStr(delphi_compatability.clSilver)))
        self.options.nonHiddenPosedColor = StrToInt(self.stringForSectionAndKey(section, "Posed color", IntToStr(delphi_compatability.clBlue)))
        self.options.selectedPosedColor = StrToInt(self.stringForSectionAndKey(section, "Posed selected color", IntToStr(delphi_compatability.clRed)))
        # ------------------------------------------- settings
        section = iniSections[kSectionSettings]
        self.mainWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Window position", "50 50 500 350"))
        self.horizontalSplitterPos = StrToInt(self.stringForSectionAndKey(section, "Horizontal split", "200"))
        self.verticalSplitterPos = StrToInt(self.stringForSectionAndKey(section, "Vertical split", "200"))
        self.debugWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Numerical exceptions window position", "75 75 400 200"))
        self.undoRedoListWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Undo/redo list window position", "100 100 400 300"))
        self.tdoEditorWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "3D object editor window position", "100 100 400 400"))
        self.breederWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Breeder position", "100 100 400 350"))
        self.timeSeriesWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Time series position", "150 150 250 150"))
        for i in range(1, u3dexport.k3DExportTypeLast + 1):
            # ------------------------------------------- 3d export options
            section = iniSections[self.sectionNumberFor3DExportType(i)]
            typeName = u3dexport.nameFor3DExportType(i)
            # ------------------------------------------- options in common for all
            self.exportOptionsFor3D[i].exportType = StrToInt(self.stringForSectionAndKey(section, typeName + " which plants to draw (selected/visible/all)", "0"))
            self.exportOptionsFor3D[i].layeringOption = StrToInt(self.stringForSectionAndKey(section, typeName + " layering option (all/by type/by part)", "1"))
            self.exportOptionsFor3D[i].stemCylinderFaces = StrToInt(self.stringForSectionAndKey(section, typeName + " stem cylinder sides", "5"))
            self.exportOptionsFor3D[i].translatePlantsToWindowPositions = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " translate plants to match window positions", "true"))
            if i == u3dexport.k3DS:
                self.exportOptionsFor3D[i].lengthOfShortName = StrToInt(self.stringForSectionAndKey(section, typeName + " length of plant name", "2"))
            else:
                self.exportOptionsFor3D[i].lengthOfShortName = StrToInt(self.stringForSectionAndKey(section, typeName + " length of plant name", "8"))
            self.exportOptionsFor3D[i].writePlantNumberInFrontOfName = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " write plant number in front of name", "false"))
            self.exportOptionsFor3D[i].writeColors = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " write colors", "true"))
            self.exportOptionsFor3D[i].xRotationBeforeDraw = StrToInt(self.stringForSectionAndKey(section, typeName + " X rotation before drawing", "0"))
            self.exportOptionsFor3D[i].overallScalingFactor_pct = StrToInt(self.stringForSectionAndKey(section, typeName + " scaling factor (percent)", "100"))
            self.exportOptionsFor3D[i].pressPlants = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " press plants", "false"))
            self.exportOptionsFor3D[i].directionToPressPlants = StrToInt(self.stringForSectionAndKey(section, typeName + " press dimension (x/y/z)", IntToStr(u3dexport.kY)))
            self.exportOptionsFor3D[i].makeTrianglesDoubleSided = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " double sided", "true"))
            if i == u3dexport.kDXF:
                # ------------------------------------------- special options
                self.exportOptionsFor3D[i].dxf_whereToGetColors = StrToInt(self.stringForSectionAndKey(section, "DXF colors option (by type/by part/all)", "0"))
                # lime
                self.exportOptionsFor3D[i].dxf_wholePlantColorIndex = StrToInt(self.stringForSectionAndKey(section, "DXF whole plant color index", "2"))
                for j in range(0, u3dexport.kExportPartLast + 1):
                    # lime
                    self.exportOptionsFor3D[i].dxf_plantPartColorIndexes[j] = StrToInt(self.stringForSectionAndKey(section, "DXF color indexes " + IntToStr(j + 1), "2"))
            elif i == u3dexport.kPOV:
                self.exportOptionsFor3D[i].pov_minLineLengthToWrite = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "POV minimum line length to write (mm)", "0.01"))
                self.exportOptionsFor3D[i].pov_minTdoScaleToWrite = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "POV minimum 3D object scale to write", "0.01"))
                self.exportOptionsFor3D[i].pov_commentOutUnionAtEnd = usupport.strToBool(self.stringForSectionAndKey(section, "POV comment out union of plants at end", "false"))
            elif i == u3dexport.kVRML:
                self.exportOptionsFor3D[i].vrml_version = StrToInt(self.stringForSectionAndKey(section, "VRML version", "1"))
            if (i == u3dexport.kPOV) or (i == u3dexport.kVRML):
                self.exportOptionsFor3D[i].nest_LeafAndPetiole = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " nest leaves with petioles", "true"))
                self.exportOptionsFor3D[i].nest_CompoundLeaf = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " compound leaves", "true"))
                self.exportOptionsFor3D[i].nest_Inflorescence = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " nest inflorescences", "true"))
                self.exportOptionsFor3D[i].nest_PedicelAndFlowerFruit = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " nest flowers/fruits with pedicels", "true"))
                self.exportOptionsFor3D[i].nest_FloralLayers = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " nest pistils and stamens", "true"))
        # ------------------------------------------- wizard
        section = iniSections[kSectionWizard]
        # meristems
        self.options.wizardChoices[uwizard.kMeristem_AlternateOrOpposite] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kMeristem_AlternateOrOpposite), "leavesAlternate")
        self.options.wizardChoices[uwizard.kMeristem_BranchIndex] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kMeristem_BranchIndex), "branchNone")
        self.options.wizardChoices[uwizard.kMeristem_SecondaryBranching] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kMeristem_SecondaryBranching), "secondaryBranchingNo")
        self.options.wizardChoices[uwizard.kMeristem_BranchAngle] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kMeristem_BranchAngle), "branchAngleSmall")
        # internodes
        self.options.wizardChoices[uwizard.kInternode_Curviness] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInternode_Curviness), "curvinessLittle")
        self.options.wizardChoices[uwizard.kInternode_Length] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInternode_Length), "internodesMedium")
        self.options.wizardChoices[uwizard.kInternode_Thickness] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInternode_Thickness), "internodeWidthThin")
        # leaves
        self.options.wizardChoices[uwizard.kLeaves_Scale] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kLeaves_Scale), "leafScaleMedium")
        self.options.wizardChoices[uwizard.kLeaves_PetioleLength] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kLeaves_PetioleLength), "petioleMedium")
        self.options.wizardChoices[uwizard.kLeaves_Angle] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kLeaves_Angle), "leafAngleMedium")
        # compound leaves
        self.options.wizardChoices[uwizard.kLeaflets_Number] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kLeaflets_Number), "leafletsOne")
        self.options.wizardChoices[uwizard.kLeaflets_Shape] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kLeaflets_Shape), "leafletsPinnate")
        self.options.wizardChoices[uwizard.kLeaflets_Spread] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kLeaflets_Spread), "leafletSpacingMedium")
        # inflor placement
        self.options.wizardChoices[uwizard.kInflorPlace_NumApical] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInflorPlace_NumApical), "apicalInflorsNone")
        self.options.wizardChoices[uwizard.kInflorPlace_ApicalStalkLength] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInflorPlace_ApicalStalkLength), "apicalStalkMedium")
        self.options.wizardChoices[uwizard.kInflorPlace_NumAxillary] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInflorPlace_NumAxillary), "axillaryInflorsNone")
        self.options.wizardChoices[uwizard.kInflorPlace_AxillaryStalkLength] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInflorPlace_AxillaryStalkLength), "axillaryStalkMedium")
        # inflor drawing
        self.options.wizardChoices[uwizard.kInflorDraw_NumFlowers] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInflorDraw_NumFlowers), "inflorFlowersThree")
        self.options.wizardChoices[uwizard.kInflorDraw_Shape] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInflorDraw_Shape), "inflorShapeRaceme")
        self.options.wizardChoices[uwizard.kInflorDraw_Thickness] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kInflorDraw_Thickness), "inflorWidthThin")
        # flowers
        self.options.wizardChoices[uwizard.kFlowers_NumPetals] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kFlowers_NumPetals), "petalsFive")
        self.options.wizardChoices[uwizard.kFlowers_Scale] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kFlowers_Scale), "petalScaleSmall")
        self.options.wizardColors[1] = StrToInt(self.stringForSectionAndKey(section, "Wizard colors 1", IntToStr(delphi_compatability.clFuchsia)))
        # fruit
        self.options.wizardChoices[uwizard.kFruit_NumSections] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kFruit_NumSections), "fruitSectionsFive")
        self.options.wizardChoices[uwizard.kFruit_Scale] = self.stringForSectionAndKey(section, "Wizard question " + IntToStr(uwizard.kFruit_Scale), "fruitScaleSmall")
        self.options.wizardColors[2] = StrToInt(self.stringForSectionAndKey(section, "Wizard colors 2", IntToStr(delphi_compatability.clRed)))
        for i in range(1, kMaxWizardTdos + 1):
            # the wizard will default the tdo names when it comes up, we don't have to do it here
            self.options.wizardTdoNames[i] = self.stringForSectionAndKey(section, "Wizard 3D objects " + IntToStr(i), "")
        self.options.wizardShowFruit = usupport.strToBool(self.stringForSectionAndKey(section, "Wizard show fruit", "false"))
        # ------------------------------------------- custom colors
        section = iniSections[kCustomColors]
        for i in range(0, kMaxCustomColors):
            self.options.customColors[i] = StrToInt(self.stringForSectionAndKey(section, "Custom color " + IntToStr(i + 1), "0"))
        # with options
        # -------------------------------------------  export (2D)
        section = iniSections[kSectionExport]
        self.bitmapOptions.exportType = StrToInt(self.stringForSectionAndKey(section, "Which plants to draw (selected/visible/all/drawing)", IntToStr(kIncludeSelectedPlants)))
        self.bitmapOptions.colorType = UNRESOLVED.TPixelFormat(StrToInt(self.stringForSectionAndKey(section, "Colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "6")))
        self.bitmapOptions.resolution_pixelsPerInch = StrToInt(self.stringForSectionAndKey(section, "Resolution (pixels per inch)", IntToStr(kDefaultResolution)))
        self.bitmapOptions.width_pixels = StrToInt(self.stringForSectionAndKey(section, "Picture width (pixels)", "400"))
        self.bitmapOptions.height_pixels = StrToInt(self.stringForSectionAndKey(section, "Picture height (pixels)", "400"))
        self.bitmapOptions.width_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Picture width (inches)", "2.0"))
        self.bitmapOptions.height_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Picture height (inches)", "2.0"))
        self.bitmapOptions.preserveAspectRatio = usupport.strToBool(self.stringForSectionAndKey(section, "Preserve aspect ratio", "true"))
        self.bitmapOptions.jpegCompressionRatio = StrToInt(self.stringForSectionAndKey(section, "JPEG compression quality ratio (1-100)", "50"))
        # -------------------------------------------  printing
        section = iniSections[kSectionPrinting]
        self.bitmapOptions.printPreserveAspectRatio = usupport.strToBool(self.stringForSectionAndKey(section, "Preserve aspect ratio", "true"))
        self.bitmapOptions.printWidth_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print width (inches)", "4.0"))
        self.bitmapOptions.printHeight_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print height (inches)", "4.0"))
        self.bitmapOptions.printLeftMargin_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print left margin (inches)", "1.0"))
        self.bitmapOptions.printTopMargin_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print top margin (inches)", "1.0"))
        self.bitmapOptions.printRightMargin_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print right margin (inches)", "1.0"))
        self.bitmapOptions.printBottomMargin_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print bottom margin (inches)", "1.0"))
        self.bitmapOptions.printBorderInner = usupport.strToBool(self.stringForSectionAndKey(section, "Print inner border", "false"))
        self.bitmapOptions.printBorderOuter = usupport.strToBool(self.stringForSectionAndKey(section, "Print outer border", "false"))
        self.bitmapOptions.printBorderWidthInner = StrToInt(self.stringForSectionAndKey(section, "Inner border width (pixels)", "1"))
        self.bitmapOptions.printBorderWidthOuter = StrToInt(self.stringForSectionAndKey(section, "Outer border width (pixels)", "1"))
        self.bitmapOptions.printBorderColorInner = StrToInt(self.stringForSectionAndKey(section, "Inner border color", "0"))
        self.bitmapOptions.printBorderColorOuter = StrToInt(self.stringForSectionAndKey(section, "Outer border color", "0"))
        # -------------------------------------------  breeding
        section = iniSections[kSectionBreeding]
        self.breedingAndTimeSeriesOptions.plantsPerGeneration = StrToInt(self.stringForSectionAndKey(section, "Plants per generation", "5"))
        self.breedingAndTimeSeriesOptions.percentMaxAge = StrToInt(self.stringForSectionAndKey(section, "Percent max age", "100"))
        self.breedingAndTimeSeriesOptions.variationType = StrToInt(self.stringForSectionAndKey(section, "Variation (low/med/high/custom/none)", "1"))
        self.breedingAndTimeSeriesOptions.thumbnailWidth = StrToInt(self.stringForSectionAndKey(section, "Thumbnail width", "40"))
        self.breedingAndTimeSeriesOptions.thumbnailHeight = StrToInt(self.stringForSectionAndKey(section, "Thumbnail height", "80"))
        self.breedingAndTimeSeriesOptions.maxGenerations = StrToInt(self.stringForSectionAndKey(section, "Max generations", "30"))
        self.breedingAndTimeSeriesOptions.numTimeSeriesStages = StrToInt(self.stringForSectionAndKey(section, "Time series stages", "5"))
        for i in range(0, uplant.kMaxBreedingSections):
            self.breedingAndTimeSeriesOptions.mutationStrengths[i] = StrToInt(self.stringForSectionAndKey(section, "Mutation " + IntToStr(i + 1), IntToStr(kMediumMutation)))
        for i in range(0, uplant.kMaxBreedingSections):
            self.breedingAndTimeSeriesOptions.firstPlantWeights[i] = StrToInt(self.stringForSectionAndKey(section, "First plant weight " + IntToStr(i + 1), "50"))
        self.breedingAndTimeSeriesOptions.getNonNumericalParametersFrom = StrToInt(self.stringForSectionAndKey(section, "Non-numeric", "5"))
        self.breedingAndTimeSeriesOptions.mutateAndBlendColorValues = usupport.strToBool(self.stringForSectionAndKey(section, "Vary colors", "false"))
        self.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary = usupport.strToBool(self.stringForSectionAndKey(section, "Vary 3D objects", "false"))
        # -------------------------------------------  nozzles
        section = iniSections[kSectionNozzle]
        self.nozzleOptions.exportType = StrToInt(self.stringForSectionAndKey(section, "Which plants to make nozzle from (selected/visible/all)", "0"))
        self.nozzleOptions.resolution_pixelsPerInch = StrToInt(self.stringForSectionAndKey(section, "Nozzle resolution", IntToStr(kDefaultResolution)))
        self.nozzleOptions.colorType = UNRESOLVED.TPixelFormat(StrToInt(self.stringForSectionAndKey(section, "Nozzle colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "6")))
        self.nozzleOptions.backgroundColor = StrToInt(self.stringForSectionAndKey(section, "Nozzle background color", IntToStr(delphi_compatability.clWhite)))
        # -------------------------------------------  animations
        section = iniSections[kSectionAnimation]
        self.animationOptions.animateBy = StrToInt(self.stringForSectionAndKey(section, "Animate by (x rotation/age)", "0"))
        self.animationOptions.xRotationIncrement = StrToInt(self.stringForSectionAndKey(section, "X rotation increment", "10"))
        self.animationOptions.ageIncrement = StrToInt(self.stringForSectionAndKey(section, "Age increment", "5"))
        self.animationOptions.resolution_pixelsPerInch = StrToInt(self.stringForSectionAndKey(section, "Resolution", IntToStr(kDefaultResolution)))
        # 24 bit
        self.animationOptions.colorType = UNRESOLVED.TPixelFormat(StrToInt(self.stringForSectionAndKey(section, "Animation colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "6")))
        # -------------------------------------------  registration
        section = iniSections[kSectionRegistration]
        self.registrationName = self.stringForSectionAndKey(section, "R4", "")
        self.registrationName = usupport.hexUnencode(self.registrationName)
        self.registrationCode = self.stringForSectionAndKey(section, "R2", "")
        self.registrationCode = usupport.hexUnencode(self.registrationCode)
        self.registered = uregistersupport.RegistrationMatch(self.registrationName, self.registrationCode)
        if not self.registered:
            section = iniSections[kSectionPrefs]
            timeString = self.stringForSectionAndKey(section, kKeyForAccumulatedUnregisteredTime, "0")
            readNumber = umath.max(usupport.strToFloatWithCommaCheck(timeString), 0)
            self.accumulatedUnregisteredTime = readNumber / kEncryptingMultiplierForAccumulatedUnregisteredTime
            section = iniSections[kSectionBreeding]
            readInt = StrToInt(self.stringForSectionAndKey(section, kKeyForUnregisteredExportCount, "0"))
            self.unregisteredExportCountBeforeThisSession = readInt / kEncryptingMultiplierForUnregisteredExportCount
            self.unregisteredExportCountThisSession = 0
        # -------------------------------------------  parameter overrides
        section = iniSections[kSectionOverrides]
        overrideKeys = delphi_compatability.TStringList.create
        overrideValues = delphi_compatability.TStringList.create
        try:
            self.readSectionKeysOrValues(section, overrideKeys, kGetKeys)
            self.readSectionKeysOrValues(section, overrideValues, kGetValues)
            if overrideKeys.Count > 0:
                for i in range(0, overrideKeys.Count):
                    key = overrideKeys.Strings[i]
                    # v2.1 changed to require section and param name for overrides
                    sectionName = trim(usupport.stringUpTo(key, ":"))
                    paramName = trim(usupport.stringBeyond(key, ":"))
                    value = overrideValues.Strings[i]
                    value = usupport.stringBeyond(value, "=")
                    param = None
                    param = self.sectionManager.parameterForSectionAndName(sectionName, paramName)
                    if (param == None) or (param.cannotOverride):
                        continue
                    stream = usstream.KfStringStream.create
                    try:
                        stream.onStringSeparator(value, " ")
                        try:
                            param.lowerBoundOverride = usupport.strToFloatWithCommaCheck(stream.nextToken())
                            param.upperBoundOverride = usupport.strToFloatWithCommaCheck(stream.nextToken())
                            param.defaultValueStringOverride = usupport.stringBetween("(", ")", stream.remainder)
                            param.isOverridden = true
                        except:
                            param.isOverridden = false
                    finally:
                        stream.free
        finally:
            overrideKeys.free
            overrideValues.free
        self.boundProfileInformation()
    
    def storeProfileInformation(self):
        i = 0
        j = 0
        section = ""
        typeName = ""
        saveNumber = 0.0
        saveInt = 0
        param = PdParameter()
        
        try:
            # v1.5
            usupport.setDecimalSeparator()
            if self.gotInfoFromV1IniFile:
                # remove two sections gotten rid of in v2
                self.removeSectionFromIniLines("Breeder")
                self.removeSectionFromIniLines("Time series")
            # files 
            section = iniSections[kSectionFiles]
            if UNRESOLVED.pos(uppercase(kUnsavedFileName), uppercase(self.lastOpenedPlantFileName)) == 0:
                self.setStringForSectionAndKey(section, "Recent", self.lastOpenedPlantFileName)
            else:
                self.setStringForSectionAndKey(section, "Recent", "")
            self.setStringForSectionAndKey(section, "3D object library", self.defaultTdoLibraryFileName)
            # recent files
            section = iniSections[kSectionOtherRecentFiles]
            for i in range(0, kMaxRecentFiles):
                if self.options.recentFiles[i] != "":
                    self.setStringForSectionAndKey(section, "File" + IntToStr(i + 1), self.options.recentFiles[i])
            # preferences 
            section = iniSections[kSectionPrefs]
            self.setStringForSectionAndKey(section, "Hide welcome window", usupport.boolToStr(self.options.hideWelcomeForm))
            self.setStringForSectionAndKey(section, "Open most recent file at start", usupport.boolToStr(self.options.openMostRecentFileAtStart))
            self.setStringForSectionAndKey(section, "Ignore window settings saved in files", usupport.boolToStr(self.options.ignoreWindowSettingsInFile))
            self.setStringForSectionAndKey(section, "Draw plants into separate bitmaps", usupport.boolToStr(self.options.cachePlantBitmaps))
            self.setStringForSectionAndKey(section, "Memory limit for plant bitmaps (in MB)", IntToStr(self.options.memoryLimitForPlantBitmaps_MB))
            self.setStringForSectionAndKey(section, "Max parts per plant (in thousands)", IntToStr(self.options.maxPartsPerPlant_thousands))
            self.setStringForSectionAndKey(section, "Background color", IntToStr(self.options.backgroundColor))
            self.setStringForSectionAndKey(section, "Transparent color", IntToStr(self.options.transparentColor))
            self.setStringForSectionAndKey(section, "Show selection rectangle", usupport.boolToStr(self.options.showSelectionRectangle))
            self.setStringForSectionAndKey(section, "Show bounding rectangle", usupport.boolToStr(self.options.showBoundsRectangle))
            self.setStringForSectionAndKey(section, "Resizing rectangle size", IntToStr(self.options.resizeRectSize))
            self.setStringForSectionAndKey(section, "Paste rectangle size", IntToStr(self.options.pasteRectSize))
            self.setStringForSectionAndKey(section, "First selection rectangle color", IntToStr(self.options.firstSelectionRectangleColor))
            self.setStringForSectionAndKey(section, "Multi selection rectangle color", IntToStr(self.options.multiSelectionRectangleColor))
            self.setStringForSectionAndKey(section, "Draw 3D objects", usupport.boolToStr(self.options.draw3DObjects))
            self.setStringForSectionAndKey(section, "Draw stems", usupport.boolToStr(self.options.drawStems))
            self.setStringForSectionAndKey(section, "Fill polygons", usupport.boolToStr(self.options.fillPolygons))
            self.setStringForSectionAndKey(section, "Draw speed (boxes/frames/solids)", IntToStr(self.options.drawSpeed))
            self.setStringForSectionAndKey(section, "Draw lines between polygons", usupport.boolToStr(self.options.drawLinesBetweenPolygons))
            self.setStringForSectionAndKey(section, "Sort polygons", usupport.boolToStr(self.options.sortPolygons))
            self.setStringForSectionAndKey(section, "Draw 3D objects as squares", usupport.boolToStr(self.options.draw3DObjectsAsBoundingRectsOnly))
            self.setStringForSectionAndKey(section, "Show drawing progress", usupport.boolToStr(self.options.showPlantDrawingProgress))
            self.setStringForSectionAndKey(section, "Use metric units", usupport.boolToStr(self.options.useMetricUnits))
            self.setStringForSectionAndKey(section, "Actions to keep in undo list", IntToStr(self.options.undoLimit))
            self.setStringForSectionAndKey(section, "Plants to keep in undo list", IntToStr(self.options.undoLimitOfPlants))
            self.setStringForSectionAndKey(section, "Rotation button increment", IntToStr(self.options.rotationIncrement))
            self.setStringForSectionAndKey(section, "Show long hints for buttons", usupport.boolToStr(self.options.showLongHintsForButtons))
            self.setStringForSectionAndKey(section, "Show hints for parameters", usupport.boolToStr(self.options.showHintsForParameters))
            self.setStringForSectionAndKey(section, "Pause before hint", IntToStr(self.options.pauseBeforeHint))
            self.setStringForSectionAndKey(section, "Pause during hint", IntToStr(self.options.pauseDuringHint))
            self.setStringForSectionAndKey(section, "Wrap lines in note editor", usupport.boolToStr(self.options.noteEditorWrapLines))
            if self.justRegistered:
                # registration, embedded here to hide time scale fraction
                section = iniSections[kSectionRegistration]
                self.setStringForSectionAndKey(section, "R1", "RQBBBOYUMMBIHYMBB")
                self.setStringForSectionAndKey(section, "R2", usupport.hexEncode(self.registrationCode))
                self.setStringForSectionAndKey(section, "R3", "YWEHZBBIUWOPBCDVXBQB")
                self.setStringForSectionAndKey(section, "R4", usupport.hexEncode(self.registrationName))
            elif not self.registered:
                section = iniSections[kSectionPrefs]
                self.accumulatedUnregisteredTime = self.accumulatedUnregisteredTime + umath.max((UNRESOLVED.now - self.startTimeThisSession), 0)
                saveNumber = self.accumulatedUnregisteredTime * kEncryptingMultiplierForAccumulatedUnregisteredTime
                self.setStringForSectionAndKey(section, kKeyForAccumulatedUnregisteredTime, FloatToStr(saveNumber))
                # hide this elsewhere
                section = iniSections[kSectionBreeding]
                saveInt = (self.unregisteredExportCountBeforeThisSession + self.unregisteredExportCountThisSession) * kEncryptingMultiplierForUnregisteredExportCount
                self.setStringForSectionAndKey(section, kKeyForUnregisteredExportCount, IntToStr(saveInt))
            section = iniSections[kSectionPrefs]
            self.setStringForSectionAndKey(section, "Update time series plants on parameter change", usupport.boolToStr(self.options.updateTimeSeriesPlantsOnParameterChange))
            self.setStringForSectionAndKey(section, "Main window view option (all/one)", IntToStr(self.options.mainWindowViewMode))
            self.setStringForSectionAndKey(section, "Distance plant moves with Control-arrow key", IntToStr(self.options.nudgeDistance))
            self.setStringForSectionAndKey(section, "Percent size increase with Control-Shift-up-arrow key", IntToStr(self.options.resizeKeyUpMultiplierPercent))
            self.setStringForSectionAndKey(section, "Parameter panels font size", IntToStr(self.options.parametersFontSize))
            self.setStringForSectionAndKey(section, "Main window orientation (horiz/vert)", IntToStr(self.options.mainWindowOrientation))
            self.setStringForSectionAndKey(section, "Contrast index for lines on polygons", IntToStr(self.options.lineContrastIndex))
            self.setStringForSectionAndKey(section, "Sort 3D objects as one item", usupport.boolToStr(self.options.sortTdosAsOneItem))
            self.setStringForSectionAndKey(section, "3D object editor point size", IntToStr(self.options.circlePointSizeInTdoEditor))
            self.setStringForSectionAndKey(section, "3D object editor parts", IntToStr(self.options.partsInTdoEditor))
            self.setStringForSectionAndKey(section, "3D object editor fill triangles", usupport.boolToStr(self.options.fillTrianglesInTdoEditor))
            self.setStringForSectionAndKey(section, "3D object editor draw lines", usupport.boolToStr(self.options.drawLinesInTdoEditor))
            self.setStringForSectionAndKey(section, "Show numerical exceptions window on exception", usupport.boolToStr(self.options.showWindowOnException))
            self.setStringForSectionAndKey(section, "Log to file on exception", usupport.boolToStr(self.options.logToFileOnException))
            self.setStringForSectionAndKey(section, "Ghost hidden parts", usupport.boolToStr(self.options.showGhostingForHiddenParts))
            self.setStringForSectionAndKey(section, "Highlight posed parts", usupport.boolToStr(self.options.showHighlightingForNonHiddenPosedParts))
            self.setStringForSectionAndKey(section, "Show posing", usupport.boolToStr(self.options.showPosingAtAll))
            self.setStringForSectionAndKey(section, "Ghosting color", IntToStr(self.options.ghostingColor))
            self.setStringForSectionAndKey(section, "Posed color", IntToStr(self.options.nonHiddenPosedColor))
            self.setStringForSectionAndKey(section, "Posed selected color", IntToStr(self.options.selectedPosedColor))
            # settings 
            section = iniSections[kSectionSettings]
            self.setStringForSectionAndKey(section, "Window position", usupport.rectToString(self.mainWindowRect))
            self.setStringForSectionAndKey(section, "Horizontal split", IntToStr(self.horizontalSplitterPos))
            self.setStringForSectionAndKey(section, "Vertical split", IntToStr(self.verticalSplitterPos))
            self.setStringForSectionAndKey(section, "Numerical exceptions window position", usupport.rectToString(self.debugWindowRect))
            self.setStringForSectionAndKey(section, "Undo/redo list window position", usupport.rectToString(self.undoRedoListWindowRect))
            self.setStringForSectionAndKey(section, "3D object editor window position", usupport.rectToString(self.tdoEditorWindowRect))
            self.setStringForSectionAndKey(section, "Breeder position", usupport.rectToString(self.breederWindowRect))
            self.setStringForSectionAndKey(section, "Time series position", usupport.rectToString(self.timeSeriesWindowRect))
            for i in range(1, u3dexport.k3DExportTypeLast + 1):
                # 3d export options
                section = iniSections[self.sectionNumberFor3DExportType(i)]
                typeName = u3dexport.nameFor3DExportType(i)
                # options in common for all
                self.setStringForSectionAndKey(section, typeName + " which plants to draw (selected/visible/all)", IntToStr(self.exportOptionsFor3D[i].exportType))
                self.setStringForSectionAndKey(section, typeName + " layering option (all/by type/by part)", IntToStr(self.exportOptionsFor3D[i].layeringOption))
                self.setStringForSectionAndKey(section, typeName + " stem cylinder sides", IntToStr(self.exportOptionsFor3D[i].stemCylinderFaces))
                self.setStringForSectionAndKey(section, typeName + " translate plants to match window positions", usupport.boolToStr(self.exportOptionsFor3D[i].translatePlantsToWindowPositions))
                self.setStringForSectionAndKey(section, typeName + " length of plant name", IntToStr(self.exportOptionsFor3D[i].lengthOfShortName))
                self.setStringForSectionAndKey(section, typeName + " write plant number in front of name", usupport.boolToStr(self.exportOptionsFor3D[i].writePlantNumberInFrontOfName))
                self.setStringForSectionAndKey(section, typeName + " write colors", usupport.boolToStr(self.exportOptionsFor3D[i].writeColors))
                self.setStringForSectionAndKey(section, typeName + " X rotation before drawing", IntToStr(self.exportOptionsFor3D[i].xRotationBeforeDraw))
                self.setStringForSectionAndKey(section, typeName + " scaling factor (percent)", IntToStr(self.exportOptionsFor3D[i].overallScalingFactor_pct))
                self.setStringForSectionAndKey(section, typeName + " press plants", usupport.boolToStr(self.exportOptionsFor3D[i].pressPlants))
                self.setStringForSectionAndKey(section, typeName + " press dimension (x/y/z)", IntToStr(self.exportOptionsFor3D[i].directionToPressPlants))
                self.setStringForSectionAndKey(section, typeName + " double sided", usupport.boolToStr(self.exportOptionsFor3D[i].makeTrianglesDoubleSided))
                if i == u3dexport.kDXF:
                    # special options
                    self.setStringForSectionAndKey(section, "DXF colors option (by type/by part/all)", IntToStr(self.exportOptionsFor3D[i].dxf_whereToGetColors))
                    self.setStringForSectionAndKey(section, "DXF whole plant color index", IntToStr(self.exportOptionsFor3D[i].dxf_wholePlantColorIndex))
                    for j in range(0, u3dexport.kExportPartLast + 1):
                        self.setStringForSectionAndKey(section, "DXF color indexes " + IntToStr(j + 1), IntToStr(self.exportOptionsFor3D[i].dxf_plantPartColorIndexes[j]))
                elif i == u3dexport.kPOV:
                    self.setStringForSectionAndKey(section, "POV minimum line length to write (mm)", usupport.digitValueString(self.exportOptionsFor3D[i].pov_minLineLengthToWrite))
                    self.setStringForSectionAndKey(section, "POV minimum 3D object scale to write", usupport.digitValueString(self.exportOptionsFor3D[i].pov_minTdoScaleToWrite))
                    self.setStringForSectionAndKey(section, "POV comment out union of plants at end", usupport.boolToStr(self.exportOptionsFor3D[i].pov_commentOutUnionAtEnd))
                elif i == u3dexport.kVRML:
                    self.setStringForSectionAndKey(section, "VRML version", IntToStr(self.exportOptionsFor3D[i].vrml_version))
                if (i == u3dexport.kPOV) or (i == u3dexport.kVRML):
                    self.setStringForSectionAndKey(section, typeName + " nest leaves with petioles", usupport.boolToStr(self.exportOptionsFor3D[i].nest_LeafAndPetiole))
                    self.setStringForSectionAndKey(section, typeName + " compound leaves", usupport.boolToStr(self.exportOptionsFor3D[i].nest_CompoundLeaf))
                    self.setStringForSectionAndKey(section, typeName + " nest inflorescences", usupport.boolToStr(self.exportOptionsFor3D[i].nest_Inflorescence))
                    self.setStringForSectionAndKey(section, typeName + " nest flowers/fruits with pedicels", usupport.boolToStr(self.exportOptionsFor3D[i].nest_PedicelAndFlowerFruit))
                    self.setStringForSectionAndKey(section, typeName + " nest pistils and stamens", usupport.boolToStr(self.exportOptionsFor3D[i].nest_FloralLayers))
            # wizard 
            section = iniSections[kSectionWizard]
            for i in range(1, kMaxWizardQuestions + 1):
                self.setStringForSectionAndKey(section, "Wizard question " + IntToStr(i), self.options.wizardChoices[i])
            for i in range(1, kMaxWizardColors + 1):
                self.setStringForSectionAndKey(section, "Wizard colors " + IntToStr(i), IntToStr(self.options.wizardColors[i]))
            for i in range(1, kMaxWizardTdos + 1):
                self.setStringForSectionAndKey(section, "Wizard 3D objects " + IntToStr(i), self.options.wizardTdoNames[i])
            self.setStringForSectionAndKey(section, "Wizard show fruit", usupport.boolToStr(self.options.wizardShowFruit))
            # custom colors
            section = iniSections[kCustomColors]
            for i in range(0, kMaxCustomColors):
                self.setStringForSectionAndKey(section, "Custom color " + IntToStr(i + 1), IntToStr(self.options.customColors[i]))
            # export 
            section = iniSections[kSectionExport]
            self.setStringForSectionAndKey(section, "Which plants to draw (selected/visible/all/drawing)", IntToStr(self.bitmapOptions.exportType))
            self.setStringForSectionAndKey(section, "Colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", IntToStr(ord(self.bitmapOptions.colorType)))
            self.setStringForSectionAndKey(section, "Resolution (pixels per inch)", IntToStr(self.bitmapOptions.resolution_pixelsPerInch))
            self.setStringForSectionAndKey(section, "Picture width (pixels)", IntToStr(self.bitmapOptions.width_pixels))
            self.setStringForSectionAndKey(section, "Picture height (pixels)", IntToStr(self.bitmapOptions.height_pixels))
            self.setStringForSectionAndKey(section, "Picture width (inches)", usupport.digitValueString(self.bitmapOptions.width_in))
            self.setStringForSectionAndKey(section, "Picture height (inches)", usupport.digitValueString(self.bitmapOptions.height_in))
            self.setStringForSectionAndKey(section, "Preserve aspect ratio", usupport.boolToStr(self.bitmapOptions.preserveAspectRatio))
            self.setStringForSectionAndKey(section, "JPEG compression quality ratio (1-100)", IntToStr(self.bitmapOptions.jpegCompressionRatio))
            # printing 
            section = iniSections[kSectionPrinting]
            self.setStringForSectionAndKey(section, "Preserve aspect ratio", usupport.boolToStr(self.bitmapOptions.printPreserveAspectRatio))
            self.setStringForSectionAndKey(section, "Print width (inches)", usupport.digitValueString(self.bitmapOptions.printWidth_in))
            self.setStringForSectionAndKey(section, "Print height (inches)", usupport.digitValueString(self.bitmapOptions.printHeight_in))
            self.setStringForSectionAndKey(section, "Print left margin (inches)", usupport.digitValueString(self.bitmapOptions.printLeftMargin_in))
            self.setStringForSectionAndKey(section, "Print top margin (inches)", usupport.digitValueString(self.bitmapOptions.printTopMargin_in))
            self.setStringForSectionAndKey(section, "Print right margin (inches)", usupport.digitValueString(self.bitmapOptions.printRightMargin_in))
            self.setStringForSectionAndKey(section, "Print bottom margin (inches)", usupport.digitValueString(self.bitmapOptions.printBottomMargin_in))
            self.setStringForSectionAndKey(section, "Print inner border", usupport.boolToStr(self.bitmapOptions.printBorderInner))
            self.setStringForSectionAndKey(section, "Print outer border", usupport.boolToStr(self.bitmapOptions.printBorderOuter))
            self.setStringForSectionAndKey(section, "Inner border width (pixels)", IntToStr(self.bitmapOptions.printBorderWidthInner))
            self.setStringForSectionAndKey(section, "Outer border width (pixels)", IntToStr(self.bitmapOptions.printBorderWidthOuter))
            self.setStringForSectionAndKey(section, "Inner border color", IntToStr(self.bitmapOptions.printBorderColorInner))
            self.setStringForSectionAndKey(section, "Outer border color", IntToStr(self.bitmapOptions.printBorderColorOuter))
            section = iniSections[kSectionBreeding]
            self.setStringForSectionAndKey(section, "Plants per generation", IntToStr(self.breedingAndTimeSeriesOptions.plantsPerGeneration))
            self.setStringForSectionAndKey(section, "Variation (low/med/high/custom/none)", IntToStr(self.breedingAndTimeSeriesOptions.variationType))
            self.setStringForSectionAndKey(section, "Percent max age", IntToStr(self.breedingAndTimeSeriesOptions.percentMaxAge))
            self.setStringForSectionAndKey(section, "Thumbnail width", IntToStr(self.breedingAndTimeSeriesOptions.thumbnailWidth))
            self.setStringForSectionAndKey(section, "Thumbnail height", IntToStr(self.breedingAndTimeSeriesOptions.thumbnailHeight))
            self.setStringForSectionAndKey(section, "Max generations", IntToStr(self.breedingAndTimeSeriesOptions.maxGenerations))
            self.setStringForSectionAndKey(section, "Time series stages", IntToStr(self.breedingAndTimeSeriesOptions.numTimeSeriesStages))
            for i in range(0, uplant.kMaxBreedingSections):
                self.setStringForSectionAndKey(section, "Mutation " + IntToStr(i + 1), IntToStr(self.breedingAndTimeSeriesOptions.mutationStrengths[i]))
            for i in range(0, uplant.kMaxBreedingSections):
                self.setStringForSectionAndKey(section, "First plant weight " + IntToStr(i + 1), IntToStr(self.breedingAndTimeSeriesOptions.firstPlantWeights[i]))
            self.setStringForSectionAndKey(section, "Non-numeric", IntToStr(self.breedingAndTimeSeriesOptions.getNonNumericalParametersFrom))
            self.setStringForSectionAndKey(section, "Vary colors", usupport.boolToStr(self.breedingAndTimeSeriesOptions.mutateAndBlendColorValues))
            self.setStringForSectionAndKey(section, "Vary 3D objects", usupport.boolToStr(self.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary))
            section = iniSections[kSectionNozzle]
            self.setStringForSectionAndKey(section, "Which plants to make nozzle from (selected/visible/all)", IntToStr(self.nozzleOptions.exportType))
            self.setStringForSectionAndKey(section, "Nozzle resolution", IntToStr(self.nozzleOptions.resolution_pixelsPerInch))
            self.setStringForSectionAndKey(section, "Nozzle colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", IntToStr(ord(self.nozzleOptions.colorType)))
            self.setStringForSectionAndKey(section, "Nozzle background color", IntToStr(self.nozzleOptions.backgroundColor))
            section = iniSections[kSectionAnimation]
            self.setStringForSectionAndKey(section, "Animate by (x rotation/age)", IntToStr(self.animationOptions.animateBy))
            self.setStringForSectionAndKey(section, "X rotation increment", IntToStr(self.animationOptions.xRotationIncrement))
            self.setStringForSectionAndKey(section, "Age increment", IntToStr(self.animationOptions.ageIncrement))
            self.setStringForSectionAndKey(section, "Resolution", IntToStr(self.animationOptions.resolution_pixelsPerInch))
            self.setStringForSectionAndKey(section, "Animation colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", IntToStr(ord(self.animationOptions.colorType)))
            # write parameter overrides
            section = iniSections[kSectionOverrides]
            if self.parameterManager.parameters.Count > 0:
                for i in range(0, self.parameterManager.parameters.Count):
                    param = uparams.PdParameter(self.parameterManager.parameters.Items[i])
                    if (not param.cannotOverride) and (param.isOverridden):
                        # v2.1 added section name to override key
                        self.setStringForSectionAndKey(section, param.originalSectionName + ": " + param.name, usupport.digitValueString(param.lowerBoundOverride) + " " + usupport.digitValueString(param.upperBoundOverride) + " " + "(" + param.defaultValueStringOverride + ")")
            self.iniLines.SaveToFile(self.iniFileName)
        finally:
            usupport.iniFileChanged = false
    
    def boundProfileInformation(self):
        i = 0
        j = 0
        
        self.options.resizeRectSize = umath.intMax(2, umath.intMin(20, self.options.resizeRectSize))
        self.options.pasteRectSize = umath.intMax(50, umath.intMin(500, self.options.pasteRectSize))
        self.options.memoryLimitForPlantBitmaps_MB = umath.intMax(1, umath.intMin(200, self.options.memoryLimitForPlantBitmaps_MB))
        self.options.maxPartsPerPlant_thousands = umath.intMax(1, umath.intMin(100, self.options.maxPartsPerPlant_thousands))
        self.horizontalSplitterPos = umath.intMax(50, self.horizontalSplitterPos)
        self.verticalSplitterPos = umath.intMax(30, self.verticalSplitterPos)
        self.options.nudgeDistance = umath.intMax(1, umath.intMin(100, self.options.nudgeDistance))
        self.options.resizeKeyUpMultiplierPercent = umath.intMax(100, umath.intMin(200, self.options.resizeKeyUpMultiplierPercent))
        self.options.parametersFontSize = umath.intMax(6, umath.intMin(20, self.options.parametersFontSize))
        self.options.mainWindowOrientation = umath.intMax(0, umath.intMin(kMaxMainWindowOrientations, self.options.mainWindowOrientation))
        self.options.undoLimit = umath.intMax(0, umath.intMin(1000, self.options.undoLimit))
        self.options.undoLimitOfPlants = umath.intMax(0, umath.intMin(500, self.options.undoLimitOfPlants))
        self.options.circlePointSizeInTdoEditor = umath.intMax(1, umath.intMin(30, self.options.circlePointSizeInTdoEditor))
        self.options.partsInTdoEditor = umath.intMax(1, umath.intMin(30, self.options.partsInTdoEditor))
        self.options.lineContrastIndex = umath.intMax(0, umath.intMin(10, self.options.lineContrastIndex))
        self.options.drawSpeed = umath.intMax(0, umath.intMin(kDrawCustom, self.options.drawSpeed))
        self.bitmapOptions.exportType = umath.intMax(0, umath.intMin(kMaxIncludeOption, self.bitmapOptions.exportType))
        self.bitmapOptions.colorType = UNRESOLVED.TPixelFormat(umath.intMax(0, umath.intMin(kMaxColorOption, ord(self.bitmapOptions.colorType))))
        self.bitmapOptions.resolution_pixelsPerInch = umath.intMax(kMinResolution, umath.intMin(kMaxResolution, self.bitmapOptions.resolution_pixelsPerInch))
        self.bitmapOptions.width_pixels = umath.intMax(kMinPixels, umath.intMin(kMaxPixels, self.bitmapOptions.width_pixels))
        self.bitmapOptions.height_pixels = umath.intMax(kMinPixels, umath.intMin(kMaxPixels, self.bitmapOptions.height_pixels))
        self.bitmapOptions.width_in = umath.max(kMinInches, umath.min(kMaxInches, self.bitmapOptions.width_in))
        self.bitmapOptions.height_in = umath.max(kMinInches, umath.min(kMaxInches, self.bitmapOptions.height_in))
        self.bitmapOptions.printWidth_in = umath.max(kMinInches, umath.min(kMaxInches, self.bitmapOptions.printWidth_in))
        self.bitmapOptions.printHeight_in = umath.max(kMinInches, umath.min(kMaxInches, self.bitmapOptions.printHeight_in))
        self.bitmapOptions.printLeftMargin_in = umath.max(kMinInches, umath.min(kMaxInches, self.bitmapOptions.printLeftMargin_in))
        self.bitmapOptions.printTopMargin_in = umath.max(kMinInches, umath.min(kMaxInches, self.bitmapOptions.printTopMargin_in))
        self.bitmapOptions.printRightMargin_in = umath.max(kMinInches, umath.min(kMaxInches, self.bitmapOptions.printRightMargin_in))
        self.bitmapOptions.printBottomMargin_in = umath.max(kMinInches, umath.min(kMaxInches, self.bitmapOptions.printBottomMargin_in))
        self.bitmapOptions.printBorderWidthInner = umath.intMax(0, umath.intMin(1000, self.bitmapOptions.printBorderWidthInner))
        self.bitmapOptions.printBorderWidthOuter = umath.intMax(0, umath.intMin(1000, self.bitmapOptions.printBorderWidthOuter))
        self.breedingAndTimeSeriesOptions.plantsPerGeneration = umath.intMax(1, umath.intMin(100, self.breedingAndTimeSeriesOptions.plantsPerGeneration))
        self.breedingAndTimeSeriesOptions.variationType = umath.intMax(0, umath.intMin(4, self.breedingAndTimeSeriesOptions.variationType))
        self.breedingAndTimeSeriesOptions.percentMaxAge = umath.intMax(1, umath.intMin(100, self.breedingAndTimeSeriesOptions.percentMaxAge))
        self.breedingAndTimeSeriesOptions.thumbnailWidth = umath.intMin(200, umath.intMax(30, self.breedingAndTimeSeriesOptions.thumbnailWidth))
        self.breedingAndTimeSeriesOptions.thumbnailHeight = umath.intMin(200, umath.intMax(30, self.breedingAndTimeSeriesOptions.thumbnailHeight))
        self.breedingAndTimeSeriesOptions.maxGenerations = umath.intMax(20, umath.intMin(500, self.breedingAndTimeSeriesOptions.maxGenerations))
        self.breedingAndTimeSeriesOptions.numTimeSeriesStages = umath.intMax(1, umath.intMin(100, self.breedingAndTimeSeriesOptions.numTimeSeriesStages))
        for i in range(0, uplant.kMaxBreedingSections):
            self.breedingAndTimeSeriesOptions.mutationStrengths[i] = umath.intMax(0, umath.intMin(100, self.breedingAndTimeSeriesOptions.mutationStrengths[i]))
        for i in range(0, uplant.kMaxBreedingSections):
            self.breedingAndTimeSeriesOptions.firstPlantWeights[i] = umath.intMax(0, umath.intMin(100, self.breedingAndTimeSeriesOptions.firstPlantWeights[i]))
        self.breedingAndTimeSeriesOptions.getNonNumericalParametersFrom = umath.intMax(0, umath.intMin(5, self.breedingAndTimeSeriesOptions.getNonNumericalParametersFrom))
        self.nozzleOptions.exportType = umath.intMax(0, umath.intMin(kIncludeAllPlants, self.nozzleOptions.exportType))
        self.nozzleOptions.resolution_pixelsPerInch = umath.intMax(kMinResolution, umath.intMin(kMaxResolution, self.nozzleOptions.resolution_pixelsPerInch))
        self.animationOptions.animateBy = umath.intMax(0, umath.intMin(kAnimateByAge, self.animationOptions.animateBy))
        self.animationOptions.xRotationIncrement = umath.intMax(-360, umath.intMin(360, self.animationOptions.xRotationIncrement))
        # will check against max plant age later
        self.animationOptions.ageIncrement = umath.intMax(0, umath.intMin(1000, self.animationOptions.ageIncrement))
        self.animationOptions.resolution_pixelsPerInch = umath.intMax(kMinResolution, umath.intMin(kMaxResolution, self.animationOptions.resolution_pixelsPerInch))
        for i in range(1, u3dexport.k3DExportTypeLast + 1):
            self.exportOptionsFor3D[i].exportType = umath.intMax(0, umath.intMin(kIncludeAllPlants, self.exportOptionsFor3D[i].exportType))
            self.exportOptionsFor3D[i].layeringOption = umath.intMax(u3dexport.kLayerOutputAllTogether, umath.intMin(u3dexport.kLayerOutputByPlantPart, self.exportOptionsFor3D[i].layeringOption))
            self.exportOptionsFor3D[i].stemCylinderFaces = umath.intMax(kMinOutputCylinderFaces, umath.intMin(kMaxOutputCylinderFaces, self.exportOptionsFor3D[i].stemCylinderFaces))
            self.exportOptionsFor3D[i].lengthOfShortName = umath.intMax(1, umath.intMin(60, self.exportOptionsFor3D[i].lengthOfShortName))
            self.exportOptionsFor3D[i].xRotationBeforeDraw = umath.intMax(-180, umath.intMin(180, self.exportOptionsFor3D[i].xRotationBeforeDraw))
            self.exportOptionsFor3D[i].overallScalingFactor_pct = umath.intMax(1, umath.intMin(10000, self.exportOptionsFor3D[i].overallScalingFactor_pct))
            self.exportOptionsFor3D[i].directionToPressPlants = umath.intMax(u3dexport.kX, umath.intMin(u3dexport.kZ, self.exportOptionsFor3D[i].directionToPressPlants))
            self.exportOptionsFor3D[i].dxf_whereToGetColors = umath.intMax(u3dexport.kColorDXFFromPlantPartType, umath.intMin(u3dexport.kColorDXFFromOneColor, self.exportOptionsFor3D[i].dxf_whereToGetColors))
            self.exportOptionsFor3D[i].dxf_wholePlantColorIndex = umath.intMax(0, umath.intMin(u3dexport.kLastDxfColorIndex, self.exportOptionsFor3D[i].dxf_wholePlantColorIndex))
            for j in range(0, u3dexport.kExportPartLast + 1):
                self.exportOptionsFor3D[i].dxf_plantPartColorIndexes[j] = umath.intMax(0, umath.intMin(u3dexport.kLastDxfColorIndex, self.exportOptionsFor3D[i].dxf_plantPartColorIndexes[j]))
            self.exportOptionsFor3D[i].pov_minLineLengthToWrite = umath.max(0.0, umath.min(100.0, self.exportOptionsFor3D[i].pov_minLineLengthToWrite))
            self.exportOptionsFor3D[i].pov_minTdoScaleToWrite = umath.max(0.0, umath.min(100.0, self.exportOptionsFor3D[i].pov_minTdoScaleToWrite))
            self.exportOptionsFor3D[i].vrml_version = umath.intMax(u3dexport.kVRMLVersionOne, umath.intMin(u3dexport.kVRMLVersionTwo, self.exportOptionsFor3D[i].vrml_version))
    
    # --------------------------------------------------------------------------- plant file i/o 
    def load(self, fileName):
        extension = ""
        
        self.plantFileLoaded = false
        try:
            self.plantFileName = fileName
            self.plantFileName = ExpandFileName(self.plantFileName)
            # v2.1 check for file extension - when opening file on startup or send to
            extension = lowercase(usupport.stringBeyond(ExtractFileName(self.plantFileName), "."))
            if extension != "pla":
                ShowMessage("The file (" + self.plantFileName + ") does not have the correct extension (pla).")
            else:
                self.plantManager.loadPlantsFromFile(fileName, kNotInPlantMover)
                self.plantFileLoaded = true
                if umain.MainForm != None:
                    umain.MainForm.setPlantFileChanged(false)
                self.lastOpenedPlantFileName = self.plantFileName
                self.lastOpenedPlantFileName = trim(self.lastOpenedPlantFileName)
                # v1.60
                self.updateRecentFileNames(self.lastOpenedPlantFileName)
        except:
            self.plantFileLoaded = false
            #callers need exception
            raise
    
    def save(self, fileName):
        self.plantManager.savePlantsToFile(fileName, kNotInPlantMover)
    
    # v1.60
    def updateRecentFileNames(self, aFileName):
        i = 0
        saved = false
        
        for i in range(0, kMaxRecentFiles):
            if self.options.recentFiles[i] == aFileName:
                # first look to see if the file is already there, and if so don't record it twice
                return
        # now look for an empty spot in the array
        saved = false
        for i in range(0, kMaxRecentFiles):
            if self.options.recentFiles[i] == "":
                self.options.recentFiles[i] = aFileName
                saved = true
                break
        if not saved:
            for i in range(0, kMaxRecentFiles):
                if i < kMaxRecentFiles - 1:
                    # if there was no empty spot, shift the files up one and add it to the end
                    self.options.recentFiles[i] = self.options.recentFiles[i + 1]
                else:
                    self.options.recentFiles[i] = aFileName
        if umain.MainForm != None:
            # PDF PORTING -- maybe syntax error in original -- had empty parens -- unless intended as procedure or fucntion call from pointer? Probably nt
            umain.MainForm.updateFileMenuForOtherRecentFiles()
    
    def resetForEmptyPlantFile(self):
        self.plantManager.plants.clear()
        self.plantFileLoaded = true
        self.plantFileName = kUnsavedFileName + "." + usupport.extensionForFileType(usupport.kFileTypePlant)
        self.lastOpenedPlantFileName = ""
        if umain.MainForm != None:
            umain.MainForm.setPlantFileChanged(false)
    
    def resetForNoPlantFile(self):
        self.plantManager.plants.clear()
        self.plantFileLoaded = false
        self.plantFileName = ""
        self.lastOpenedPlantFileName = ""
        if umain.MainForm != None:
            umain.MainForm.setPlantFileChanged(false)
    
    def checkForExistingDefaultTdoLibrary(self):
        result = false
        # returns false if user wants to cancel action
        result = true
        if not FileExists(self.defaultTdoLibraryFileName):
            MessageDialog("No 3D object library has been chosen." + chr(13) + chr(13) + "In order to continue with what you are doing," + chr(13) + "you need to choose a 3D object library" + chr(13) + "from the dialog that follows this one.", mtWarning, [mbOK, ], 0)
            self.defaultTdoLibraryFileName = usupport.getFileOpenInfo(usupport.kFileTypeTdo, self.defaultTdoLibraryFileName, "Choose a 3D object library (tdo) file")
            result = self.defaultTdoLibraryFileName != ""
        return result
    
    def totalUnregisteredExportsAtThisMoment(self):
        result = 0
        result = self.unregisteredExportCountBeforeThisSession + self.unregisteredExportCountThisSession
        return result
    
    # ------------------------------------------------------------------- file/directory utilities 
    def nameIsAbsolute(self, fileName):
        result = false
        result = ((UNRESOLVED.pos("\\", fileName) == 1) or (UNRESOLVED.pos(":", fileName) == 2))
        return result
    
    def isFileInPath(self, fileName):
        result = false
        qualifiedName = ""
        
        result = true
        #see if file exists
        qualifiedName = fileName
        if not FileExists(qualifiedName):
            if not self.nameIsAbsolute(fileName):
                #this merging process could be more sophisticated in case
                #     file name has leading drive or leading slash - just not merging for now
                qualifiedName = ExtractFilePath(delphi_compatability.Application.exeName) + fileName
            if not FileExists(qualifiedName):
                result = false
        return result
    
    #searches for file according to name, and then in exe directory, and then gives up
    def buildFileNameInPath(self, fileName):
        result = ""
        result = ExpandFileName(fileName)
        if FileExists(result):
            return result
        result = ExtractFilePath(delphi_compatability.Application.exeName) + ExtractFileName(fileName)
        if FileExists(result):
            return result
        result = fileName
        return result
    
    def firstUnusedUnsavedFileName(self):
        result = ""
        fileNumber = 0
        
        result = ""
        fileNumber = 1
        while fileNumber < 100:
            result = ExtractFilePath(delphi_compatability.Application.exeName) + self.unsavedFileNameForNumber(fileNumber)
            if not FileExists(result):
                return result
            fileNumber += 1
        ShowMessage("Too many unnamed plant files. Delete some to reuse names.")
        return result
    
    def unsavedFileNameForNumber(self, aNumber):
        result = ""
        numberString = ""
        
        numberString = IntToStr(aNumber)
        if len(numberString) == 1:
            numberString = "0" + numberString
        result = kUnsavedFileName + numberString + ".pla"
        return result
    
    def getColorUsingCustomColors(self, originalColor):
        result = TColorRef()
        colorDialog = TColorDialog()
        i = 0
        colorString = ""
        color = TColorRef()
        
        # may be more efficient to do this from main window, because a colorDialog component on the form
        # would keep the custom colors between uses without having to change the domain colors
        result = originalColor
        colorDialog = delphi_compatability.TColorDialog().Create(delphi_compatability.Application)
        colorDialog.Color = originalColor
        colorDialog.customColors.clear
        for i in range(0, kMaxCustomColors):
            if self.options.customColors[i] == originalColor:
                # add new color to custom colors if not already there and there is room
                # (this assumes they don't want black as a custom color)
                break
            if self.options.customColors[i] == delphi_compatability.clBlack:
                self.options.customColors[i] = originalColor
                break
        for i in range(0, kMaxCustomColors):
            # load our custom colors into color dialog custom colors
            colorString = "Color" + chr(ord("A") + i) + "=" + UNRESOLVED.Format("%.6x", [self.options.customColors[i], ])
            colorDialog.customColors.add(colorString)
        colorDialog.options = [UNRESOLVED.cdFullOpen, ]
        try:
            if colorDialog.Execute():
                result = colorDialog.Color
                for i in range(0, colorDialog.customColors.count):
                    colorString = colorDialog.customColors[i]
                    colorString = usupport.stringBeyond(colorString, "=")
                    color = StrToIntDef("$" + colorString, 0)
                    self.options.customColors[i] = color
        finally:
            colorDialog.free
        return result
    
    def sectionNumberFor3DExportType(self, anOutputType):
        result = 0
        if anOutputType == u3dexport.kDXF:
            result = kSectionDXF
        elif anOutputType == u3dexport.kPOV:
            result = kSectionPOV
        elif anOutputType == u3dexport.k3DS:
            result = kSection3DS
        elif anOutputType == u3dexport.kOBJ:
            result = kSectionOBJ
        elif anOutputType == u3dexport.kVRML:
            result = kSectionVRML
        elif anOutputType == u3dexport.kLWO:
            result = kSectionLWO
        else :
            raise GeneralException.create("Problem: Invalid type in PdDomain.sectionNumberFor3DExportType.")
        return result
    
    def plantDrawOffset_mm(self):
        result = SinglePoint()
        result = usupport.setSinglePoint(0, 0)
        if self.plantManager == None:
            return result
        result = self.plantManager.plantDrawOffset_mm
        return result
    
    def plantDrawScale_PixelsPerMm(self):
        result = 0.0
        result = 1.0
        if self.plantManager == None:
            return result
        result = self.plantManager.plantDrawScale_PixelsPerMm
        return result
    
    def viewPlantsInMainWindowFreeFloating(self):
        result = false
        result = self.options.mainWindowViewMode == kViewPlantsInMainWindowFreeFloating
        return result
    
    def viewPlantsInMainWindowOnePlantAtATime(self):
        result = false
        result = self.options.mainWindowViewMode == kViewPlantsInMainWindowOneAtATime
        return result
    
