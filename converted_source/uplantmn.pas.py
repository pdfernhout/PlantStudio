# unit Uplantmn

from conversion_common import *
import udebug
import utdo
import usplash
import umain
import u3dexport
import uturtle
import updcom
import udomain
import ucursor
import usupport
import uplant
import ucollect
import delphi_compatability

def checkVersionNumberInPlantNameLine(aLine):
    versionNumberString = ""
    plantName = ""
    versionNumber = 0
    
    # assumes line given is plant start line
    # e.g., >>> [rose] start PlantStudio plant <v1.0>
    plantName = usupport.stringBetween("[", "]", aLine)
    versionNumberString = usupport.stringBetween("<", ">", aLine)
    versionNumberString = usupport.stringBetween("v", ".", versionNumberString)
    versionNumber = StrToIntDef(versionNumberString, 0)
    if versionNumber > 2:
        ShowMessage("The plant \"" + plantName + "\" has a major version number of " + IntToStr(versionNumber) + "," + chr(13) + "which is higher than this major version of PlantStudio (2)." + chr(13) + chr(13) + "That means that although I may be able to read the plant," + chr(13) + "it will probably look better in the most up-to-date version of PlantStudio," + chr(13) + "which you can get at the PlantStudio web site.")

class PdPlantManager(TObject):
    def __init__(self):
        self.plants = TListCollection()
        self.privatePlantClipboard = TListCollection()
        self.plantDrawOffset_mm = SinglePoint()
        self.plantDrawScale_PixelsPerMm = 0.0
        self.fitInVisibleAreaForConcentrationChange = false
        self.mainWindowOrientation = 0
        self.showBoundsRectangle = false
        self.mainWindowViewMode = 0
    
    def create(self):
        TObject.create(self)
        self.plants = ucollect.TListCollection().Create()
        self.privatePlantClipboard = ucollect.TListCollection().Create()
        self.plantDrawScale_PixelsPerMm = 1.0
        return self
    
    def destroy(self):
        self.plants.free
        self.plants = None
        self.privatePlantClipboard.free
        self.privatePlantClipboard = None
        TObject.destroy(self)
    
    def addPlant(self, newPlant):
        self.plants.Add(newPlant)
    
    def removePlant(self, aPlant):
        result = false
        # remove returns index of object in list before removal 
        result = (self.plants.Remove(aPlant) >= 0)
        return result
    
    def copyFromPlant(self, plant):
        result = PdPlant()
        newPlant = PdPlant()
        
        if plant == None:
            raise GeneralException.create("Problem: Nil plant in method PdPlantManager.copyFromPlant.")
        newPlant = uplant.PdPlant().create()
        plant.copyTo(newPlant)
        self.plants.Add(newPlant)
        result = newPlant
        return result
    
    def plantForIndex(self, index):
        result = PdPlant()
        result = uplant.PdPlant(self.plants.Items[index])
        return result
    
    def findPlantAtPoint(self, aPoint):
        result = PdPlant()
        plant = PdPlant()
        i = 0
        
        result = None
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if plant.hidden:
                    continue
                if plant.includesPoint(aPoint):
                    result = plant
                    return result
        return result
    
    def findFirstPlantWithBoundsRectAtPoint(self, aPoint):
        result = PdPlant()
        plant = PdPlant()
        plantIndex = 0
        
        result = None
        if self.plants.Count > 0:
            for plantIndex in range(self.plants.Count - 1, 0 + 1):
                # go through list backwards because list order is drawing order is from front to back
                plant = uplant.PdPlant(self.plants.Items[plantIndex])
                if plant.hidden:
                    continue
                if plant.pointInBoundsRect(aPoint):
                    result = plant
                    return result
        return result
    
    def loadPlantObjectsIntoTStrings(self, stringList):
        i = 0
        plant = PdPlant()
        
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                stringList.AddObject(plant.getName(), plant)
    
    # --------------------------------------------------------------------------------------- input/output 
    def loadPlantsFromFile(self, fileName, inPlantMover):
        inputFile = TextFile()
        plant = PdPlant()
        aLine = ""
        plantName = ""
        concentratedInFile = false
        concentratedLastTimeSaved = false
        lineCount = 0
        
        AssignFile(inputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Reset(inputFile)
            self.plants.clear()
            # defaults in case things are missing from file
            self.plantDrawOffset_mm = usupport.setSinglePoint(0, 0)
            self.plantDrawScale_PixelsPerMm = 1.0
            self.mainWindowViewMode = udomain.domain.options.mainWindowViewMode
            self.mainWindowOrientation = udomain.domain.options.mainWindowOrientation
            self.showBoundsRectangle = udomain.domain.options.showBoundsRectangle
            concentratedLastTimeSaved = false
            self.fitInVisibleAreaForConcentrationChange = false
            while not UNRESOLVED.eof(inputFile):
                # cfk testing
                aLine = usupport.tolerantReadln(inputFile, aLine)
                if (aLine == "") or (UNRESOLVED.pos(";", aLine) == 1):
                    continue
                if UNRESOLVED.pos("offset=", aLine) == 1:
                    self.plantDrawOffset_mm = usupport.stringToSinglePoint(usupport.stringBeyond(aLine, "="))
                elif UNRESOLVED.pos("scale=", aLine) == 1:
                    try:
                        self.plantDrawScale_PixelsPerMm = intround(StrToFloat(usupport.stringBeyond(aLine, "=")) * 100.0) / 100.0
                    except:
                        self.plantDrawScale_PixelsPerMm = 1.0
                elif UNRESOLVED.pos("concentrated=", aLine) == 1:
                    concentratedLastTimeSaved = udomain.domain.viewPlantsInMainWindowOnePlantAtATime()
                    if udomain.domain.options.ignoreWindowSettingsInFile:
                        # v2.1 if ignoring settings in file, use current settings, otherwise use what is in file
                        concentratedInFile = (self.mainWindowViewMode == udomain.kViewPlantsInMainWindowOneAtATime)
                    else:
                        concentratedInFile = usupport.strToBool(usupport.stringBeyond(aLine, "="))
                    if concentratedInFile:
                        self.mainWindowViewMode = udomain.kViewPlantsInMainWindowOneAtATime
                    else:
                        self.mainWindowViewMode = udomain.kViewPlantsInMainWindowFreeFloating
                    if not inPlantMover:
                        udomain.domain.options.mainWindowViewMode = self.mainWindowViewMode
                    self.fitInVisibleAreaForConcentrationChange = concentratedInFile and not concentratedLastTimeSaved
                elif UNRESOLVED.pos("orientation (top/side)=", aLine) == 1:
                    if not udomain.domain.options.ignoreWindowSettingsInFile:
                        # v2.1 only read if not ignoring settings in file
                        self.mainWindowOrientation = StrToInt(usupport.stringBeyond(aLine, "="))
                elif UNRESOLVED.pos("boxes=", aLine) == 1:
                    self.showBoundsRectangle = usupport.strToBool(usupport.stringBeyond(aLine, "="))
                    if not inPlantMover:
                        udomain.domain.options.showBoundsRectangle = self.showBoundsRectangle
                    if (umain.MainForm != None) and (not umain.MainForm.inFormCreation) and (not inPlantMover):
                        umain.MainForm.updateForChangeToDomainOptions()
                        umain.MainForm.copyDrawingBitmapToPaintBox()
                elif UNRESOLVED.pos("[", aLine) == 1:
                    # plant start line
                    checkVersionNumberInPlantNameLine(aLine)
                    plant = uplant.PdPlant().create()
                    plantName = usupport.stringBeyond(aLine, "[")
                    plantName = usupport.stringUpTo(plantName, "]")
                    plant.setName(plantName)
                    udomain.domain.parameterManager.setAllReadFlagsToFalse()
                    # cfk change v1.3
                    # changed reading end of plant to read "end PlantStudio plant" instead of empty line because
                    # sometimes text wrapping puts empty lines in, not a good measure of completion.
                    # now end of plant must be there to be read. could produce endless loop if no end
                    # of plant, so stop at absolute cutoff of 300 non-empty, non-comment lines (there are now 215 parameters).
                    # also stop reading if reach next plant square bracket or end of file.
                    # v2.0 increased number of params to 350 so 300 is problem, changed to 3000 to avoid this in future, oops
                    lineCount = 0
                    while (UNRESOLVED.pos(uplant.kPlantAsTextEndString, aLine) <= 0) and (lineCount <= 3000):
                        # aLine <> '' do
                        aLine = usupport.tolerantReadln(inputFile, aLine)
                        if (UNRESOLVED.pos("[", aLine) == 1) or (UNRESOLVED.eof(inputFile)):
                            # v1.60 reversed order of the next two lines -- fixes infinite loop when no end of plant
                            # v1.3 added check for next plant or eof
                            break
                        if (trim(aLine) == "") or (UNRESOLVED.pos(";", aLine) == 1):
                            # v1.3 added skip empty lines
                            continue
                        plant.readLineAndTdoFromPlantFile(aLine, inputFile)
                        lineCount = lineCount + 1
                    plant.finishLoadingOrDefaulting(uplant.kCheckForUnreadParams)
                    self.plants.Add(plant)
        finally:
            CloseFile(inputFile)
    
    def savePlantsToFile(self, fileName, inPlantMover):
        outputFile = TextFile()
        i = 0
        plant = PdPlant()
        
        if self.plants.Count <= 0:
            return
        AssignFile(outputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            if not inPlantMover:
                # update before writing out (keep as read in if in mover)
                # plantDrawOffset_mm is used from here
                # plantDrawScale_PixelsPerMm is used from here
                self.mainWindowViewMode = udomain.domain.options.mainWindowViewMode
                self.mainWindowOrientation = udomain.domain.options.mainWindowOrientation
                self.showBoundsRectangle = udomain.domain.options.showBoundsRectangle
            Rewrite(outputFile)
            # v2.0
            writeln(outputFile, "; PlantStudio version 2.0 plant file")
            writeln(outputFile, "offset=" + usupport.singlePointToString(self.plantDrawOffset_mm))
            writeln(outputFile, "scale=" + usupport.digitValueString(self.plantDrawScale_PixelsPerMm))
            if self.mainWindowViewMode == udomain.kViewPlantsInMainWindowOneAtATime:
                writeln(outputFile, "concentrated=true")
            else:
                writeln(outputFile, "concentrated=false")
            # v2.0
            writeln(outputFile, "orientation (top/side)=" + IntToStr(self.mainWindowOrientation))
            # v2.0
            writeln(outputFile, "boxes=" + usupport.boolToStr(self.showBoundsRectangle))
            writeln(outputFile)
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                if plant == None:
                    continue
                plant.writeToPlantFile(outputFile)
        finally:
            CloseFile(outputFile)
    
    # v1.11
    def reconcileFileWithTdoLibrary(self, plantFileName, tdoLibrary):
        result = 0
        plantFileTdos = TListCollection()
        libraryFileTdos = TListCollection()
        plantFile = TextFile()
        tdoFile = TextFile()
        outputTdoFile = TextFile()
        i = 0
        j = 0
        tdo = KfObject3d()
        plantFileTdo = KfObject3d()
        libraryTdo = KfObject3d()
        matchInLibrary = false
        aLine = ""
        fileInfo = SaveFileNamesStructure()
        
        result = 0
        if not FileExists(plantFileName):
            # check that files exist
            plantFileName = usupport.getFileOpenInfo(usupport.kFileTypePlant, plantFileName, "Choose a plant file")
            if plantFileName == "":
                return result
        if not FileExists(tdoLibrary):
            tdoLibrary = usupport.getFileOpenInfo(usupport.kFileTypeTdo, tdoLibrary, "Choose a 3D object library (tdo) file")
            if tdoLibrary == "":
                return result
        plantFileTdos = ucollect.TListCollection().Create()
        libraryFileTdos = ucollect.TListCollection().Create()
        try:
            ucursor.cursor_startWait()
            # read tdos from plants
            AssignFile(plantFile, plantFileName)
            try:
                # v1.5
                usupport.setDecimalSeparator()
                Reset(plantFile)
                while not UNRESOLVED.eof(plantFile):
                    UNRESOLVED.readln(plantFile, aLine)
                    if UNRESOLVED.pos(utdo.kStartTdoString, aLine) > 0:
                        tdo = utdo.KfObject3D().create()
                        tdo.readFromFileStream(plantFile, utdo.kInTdoLibrary)
                        plantFileTdos.Add(tdo)
            finally:
                CloseFile(plantFile)
            # read tdos from library
            AssignFile(tdoFile, tdoLibrary)
            try:
                # v1.5
                usupport.setDecimalSeparator()
                Reset(tdoFile)
                while not UNRESOLVED.eof(tdoFile):
                    tdo = utdo.KfObject3D().create()
                    tdo.readFromFileStream(tdoFile, utdo.kInTdoLibrary)
                    libraryFileTdos.Add(tdo)
            finally:
                CloseFile(tdoFile)
            if plantFileTdos.Count > 0:
                for i in range(0, plantFileTdos.Count):
                    # add plant tdos not in library list to library list
                    plantFileTdo = utdo.KfObject3D(plantFileTdos.Items[i])
                    matchInLibrary = false
                    if libraryFileTdos.Count > 0:
                        for j in range(0, libraryFileTdos.Count):
                            libraryTdo = utdo.KfObject3D(libraryFileTdos.Items[j])
                            if plantFileTdo.isSameAs(libraryTdo):
                                matchInLibrary = true
                                break
                    if not matchInLibrary:
                        tdo = utdo.KfObject3D().create()
                        tdo.copyFrom(plantFileTdo)
                        libraryFileTdos.Add(tdo)
                        result += 1
            if result > 0:
                if usupport.getFileSaveInfo(usupport.kFileTypeTdo, usupport.kDontAskForFileName, tdoLibrary, fileInfo):
                    # if any tdos in plant file but not in library, rewrite library
                    AssignFile(outputTdoFile, fileInfo.tempFile)
                    try:
                        # v1.5
                        usupport.setDecimalSeparator()
                        Rewrite(outputTdoFile)
                        usupport.startFileSave(fileInfo)
                        if libraryFileTdos.Count > 0:
                            for i in range(0, libraryFileTdos.Count):
                                tdo = UNRESOLVED.TObject(libraryFileTdos.Items[i]) as utdo.KfObject3D
                                if tdo == None:
                                    continue
                                tdo.writeToFileStream(outputTdoFile, utdo.kInTdoLibrary)
                        fileInfo.writingWasSuccessful = true
                    finally:
                        CloseFile(outputTdoFile)
                        usupport.cleanUpAfterFileSave(fileInfo)
        finally:
            plantFileTdos.free
            libraryFileTdos.free
            ucursor.cursor_stopWait()
        return result
    
    def visiblePlantCount(self):
        result = 0
        i = 0
        
        result = 0
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                if not uplant.PdPlant(self.plants.Items[i]).hidden:
                    result += 1
        return result
    
    # --------------------------------------------------------------------------------------- drawing 
    def drawOnInvalidRect(self, destCanvas, selectedPlants, invalidRect, excludeInvisiblePlants, excludeNonSelectedPlants):
        plantIndex = 0
        plant = PdPlant()
        intersection = TRect()
        plantRect = TRect()
        intersectResult = longbool()
        includePlant = false
        partsDrawn = 0L
        
        if delphi_compatability.Application.terminated:
            return
        partsDrawn = 0
        if self.plants.Count > 0:
            for plantIndex in range(self.plants.Count - 1, 0 + 1):
                # go through list backwards because list order is drawing order is from front to back
                plant = uplant.PdPlant(self.plants.Items[plantIndex])
                includePlant = false
                plantRect = plant.boundsRect_pixels()
                if (plantRect.Left == 0) and (plantRect.Right == 0) and (plantRect.Top == 0) and (plantRect.Bottom == 0):
                    # if plant has just been read in, recalculate bounds rect by drawing it 
                    includePlant = true
                intersectResult = delphi_compatability.IntersectRect(intersection, plantRect, invalidRect)
                includePlant = includePlant or intersectResult
                if excludeInvisiblePlants:
                    includePlant = includePlant and not plant.hidden
                if excludeNonSelectedPlants:
                    includePlant = includePlant and (selectedPlants.IndexOf(plant) >= 0)
                if includePlant:
                    plant.plantPartsDrawnAtStart = partsDrawn
                    try:
                        plant.computeBounds = true
                        if (udomain.domain.options.cachePlantBitmaps) and (not udomain.domain.drawingToMakeCopyBitmap):
                            destCanvas.Draw(plantRect.Left, plantRect.Top, plant.previewCache)
                        else:
                            plant.drawOn(destCanvas)
                    finally:
                        plant.computeBounds = false
                    partsDrawn = partsDrawn + plant.totalPlantParts
    
    #procedure drawWithOpenGLOnInvalidRect(form: TForm; selectedPlants: TList; invalidRect: TRect;
    #  glRect: TRect; excludeInvisiblePlants, excludeNonSelectedPlants: boolean);
    def totalPlantPartCountInInvalidRect(self, selectedPlants, invalidRect, excludeInvisiblePlants, excludeNonSelectedPlants):
        result = 0L
        plantIndex = 0
        plant = PdPlant()
        intersection = TRect()
        plantRect = TRect()
        intersectResult = longbool()
        includePlant = false
        
        result = 0
        if delphi_compatability.Application.terminated:
            return result
        if self.plants.Count > 0:
            for plantIndex in range(self.plants.Count - 1, 0 + 1):
                plant = uplant.PdPlant(self.plants.Items[plantIndex])
                includePlant = false
                plantRect = plant.boundsRect_pixels()
                if (plantRect.Left == 0) and (plantRect.Right == 0) and (plantRect.Top == 0) and (plantRect.Bottom == 0):
                    # if plant has just been read in, recalculate bounds rect by drawing it 
                    includePlant = true
                intersectResult = delphi_compatability.IntersectRect(intersection, plantRect, invalidRect)
                includePlant = includePlant or intersectResult
                if excludeInvisiblePlants:
                    includePlant = includePlant and not plant.hidden
                if excludeNonSelectedPlants:
                    includePlant = includePlant and (selectedPlants.IndexOf(plant) >= 0)
                if includePlant:
                    plant.countPlantParts()
                    result = result + plant.totalPlantParts
        return result
    
    def zeroAllBoundsRectsToForceRedraw(self):
        i = 0
        plant = PdPlant()
        
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[i])
                plant.setBoundsRect_pixels(Rect(0, 0, 0, 0))
    
    def fillListWithPlantsInRectangle(self, aRect, aList):
        plantIndex = 0
        plant = PdPlant()
        intersection = TRect()
        intersectResult = longbool()
        includePlant = false
        
        if aList == None:
            raise GeneralException.create("Problem: Nil list in method PdPlantManager.fillListWithPlantsInRectangle.")
        if delphi_compatability.Application.terminated:
            return
        if self.plants.Count > 0:
            for plantIndex in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[plantIndex])
                includePlant = false
                intersectResult = delphi_compatability.IntersectRect(intersection, plant.boundsRect_pixels(), aRect)
                includePlant = includePlant or intersectResult
                includePlant = includePlant and not plant.hidden
                if includePlant:
                    aList.Add(plant)
    
    def write3DOutputFileToFileName(self, selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants, fileName, outputType):
        plant = PdPlant()
        i = 0
        includePlant = false
        includeRect = TRect()
        includedPlants = TList()
        translatePlants = false
        turtle = KfTurtle()
        
        usupport.setDecimalSeparator()
        includedPlants = None
        includeRect = self.combinedPlantBoundsRects(selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants)
        if (usupport.rWidth(includeRect) <= 0) or (usupport.rHeight(includeRect) <= 0):
            return
        includedPlants = delphi_compatability.TList().Create()
        turtle = uturtle.KfTurtle().createFor3DOutput(outputType, fileName)
        try:
            turtle.start3DExportFile()
            if self.plants.Count > 0:
                for i in range(0, self.plants.Count):
                    # count the plants to be drawn so we know if there is more than one
                    plant = uplant.PdPlant(self.plants.Items[i])
                    includePlant = true
                    if excludeInvisiblePlants:
                        includePlant = includePlant and not plant.hidden
                    if excludeNonSelectedPlants:
                        includePlant = includePlant and (selectedPlants.IndexOf(plant) >= 0)
                    if includePlant:
                        includedPlants.Add(plant)
            if includedPlants.Count <= 1:
                # if only one plant, don't translate or scale
                translatePlants = false
            else:
                translatePlants = udomain.domain.exportOptionsFor3D[outputType].translatePlantsToWindowPositions
            if includedPlants.Count > 0:
                for i in range(0, includedPlants.Count):
                    # iterate over included plants
                    uplant.PdPlant(includedPlants.Items[i]).saveToGlobal3DOutputFile(i, translatePlants, includeRect, outputType, turtle)
        finally:
            turtle.end3DExportFile()
            turtle.free
            turtle = None
            includedPlants.free
            includedPlants = None
    
    def combinedPlantBoundsRects(self, selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants):
        result = TRect()
        plant = PdPlant()
        plantIndex = 0
        includePlant = false
        
        result = delphi_compatability.Bounds(0, 0, 0, 0)
        if self.plants.Count > 0:
            for plantIndex in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[plantIndex])
                includePlant = true
                if excludeInvisiblePlants:
                    includePlant = includePlant and not plant.hidden
                if excludeNonSelectedPlants:
                    includePlant = includePlant and (selectedPlants.IndexOf(plant) >= 0)
                if includePlant:
                    delphi_compatability.UnionRect(result, result, plant.boundsRect_pixels())
        return result
    
    def largestPlantBoundsRect(self, selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants):
        result = TRect()
        plant = PdPlant()
        plantIndex = 0
        includePlant = false
        plantRect = TRect()
        
        result = delphi_compatability.Bounds(0, 0, 0, 0)
        if self.plants.Count > 0:
            for plantIndex in range(0, self.plants.Count):
                plant = uplant.PdPlant(self.plants.Items[plantIndex])
                includePlant = true
                if excludeInvisiblePlants:
                    includePlant = includePlant and not plant.hidden
                if excludeNonSelectedPlants:
                    includePlant = includePlant and (selectedPlants.IndexOf(plant) >= 0)
                if includePlant:
                    plantRect = plant.boundsRect_pixels()
                    if usupport.rWidth(plantRect) > result.Right:
                        result.Right = usupport.rWidth(plantRect)
                    if usupport.rHeight(plantRect) > result.Bottom:
                        result.Bottom = usupport.rHeight(plantRect)
        return result
    
    # --------------------------------------------------------------------------------------- private clipboard 
    def copyPlantsInListToPrivatePlantClipboard(self, aList):
        i = 0
        plant = PdPlant()
        newPlant = PdPlant()
        
        self.privatePlantClipboard.clear()
        if aList.Count > 0:
            for i in range(0, aList.Count):
                plant = uplant.PdPlant(aList.Items[i])
                newPlant = uplant.PdPlant().create()
                plant.copyTo(newPlant)
                newPlant.setName("Copy of " + newPlant.getName())
                self.privatePlantClipboard.Add(newPlant)
    
    def setCopiedFromMainWindowFlagInClipboardPlants(self):
        i = 0
        
        if self.privatePlantClipboard.Count > 0:
            for i in range(0, self.privatePlantClipboard.Count):
                uplant.PdPlant(self.privatePlantClipboard.Items[i]).justCopiedFromMainWindow = true
    
    def pastePlantsFromPrivatePlantClipboardToList(self, aList):
        i = 0
        plant = PdPlant()
        newPlant = PdPlant()
        
        if self.privatePlantClipboard.Count > 0:
            for i in range(0, self.privatePlantClipboard.Count):
                # caller takes responsibility of freeing plants 
                plant = uplant.PdPlant(self.privatePlantClipboard.Items[i])
                newPlant = uplant.PdPlant().create()
                plant.copyTo(newPlant)
                newPlant.moveBy(Point(updcom.kPasteMoveDistance, 0))
                aList.Add(newPlant)
    
    def pasteFirstPlantFromPrivatePlantClipboardToPlant(self, newPlant):
        plant = PdPlant()
        
        if newPlant == None:
            # this is used by the breeder and grower windows 
            # caller creates newPlant first 
            return
        if self.privatePlantClipboard.Count > 0:
            # caller takes responsibility of freeing plants 
            plant = uplant.PdPlant(self.privatePlantClipboard.Items[0])
            plant.copyTo(newPlant)
    
