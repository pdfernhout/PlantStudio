// unit Uplantmn

from conversion_common import *;
import udebug;
import usplash;
import ucursor;
import delphi_compatability;

public void checkVersionNumberInPlantNameLine(String aLine) {
    String versionNumberString = "";
    String plantName = "";
    int versionNumber = 0;
    
    // assumes line given is plant start line
    // e.g., >>> [rose] start PlantStudio plant <v1.0>
    plantName = UNRESOLVED.stringBetween("[", "]", aLine);
    versionNumberString = UNRESOLVED.stringBetween("<", ">", aLine);
    versionNumberString = UNRESOLVED.stringBetween("v", ".", versionNumberString);
    versionNumber = StrToIntDef(versionNumberString, 0);
    if (versionNumber > 2) {
        ShowMessage("The plant \"" + plantName + "\" has a major version number of " + IntToStr(versionNumber) + "," + chr(13) + "which is higher than this major version of PlantStudio (2)." + chr(13) + chr(13) + "That means that although I may be able to read the plant," + chr(13) + "it will probably look better in the most up-to-date version of PlantStudio," + chr(13) + "which you can get at the PlantStudio web site.");
    }
}


class PdPlantManager extends TObject {
    public TListCollection plants;
    public TListCollection privatePlantClipboard;
    public SinglePoint plantDrawOffset_mm;
    public float plantDrawScale_PixelsPerMm;
    public boolean fitInVisibleAreaForConcentrationChange;
    public short mainWindowOrientation;
    public boolean showBoundsRectangle;
    public short mainWindowViewMode;
    
    public void create() {
        super.create();
        this.plants = UNRESOLVED.TListCollection.create;
        this.privatePlantClipboard = UNRESOLVED.TListCollection.create;
        this.plantDrawScale_PixelsPerMm = 1.0;
    }
    
    public void destroy() {
        this.plants.free;
        this.plants = null;
        this.privatePlantClipboard.free;
        this.privatePlantClipboard = null;
        super.destroy();
    }
    
    public void addPlant(PdPlant newPlant) {
        this.plants.add(newPlant);
    }
    
    public boolean removePlant(PdPlant aPlant) {
        result = false;
        // remove returns index of object in list before removal 
        result = (this.plants.remove(aPlant) >= 0);
        return result;
    }
    
    public PdPlant copyFromPlant(PdPlant plant) {
        result = new PdPlant();
        PdPlant newPlant = new PdPlant();
        
        if (plant == null) {
            throw new GeneralException.create("Problem: Nil plant in method PdPlantManager.copyFromPlant.");
        }
        newPlant = UNRESOLVED.PdPlant.create;
        plant.copyTo(newPlant);
        this.plants.add(newPlant);
        result = newPlant;
        return result;
    }
    
    public PdPlant plantForIndex(long index) {
        result = new PdPlant();
        result = UNRESOLVED.PdPlant(this.plants.items[index]);
        return result;
    }
    
    public PdPlant findPlantAtPoint(TPoint aPoint) {
        result = new PdPlant();
        PdPlant plant = new PdPlant();
        short i = 0;
        
        result = null;
        if (this.plants.count > 0) {
            for (i = 0; i <= this.plants.count - 1; i++) {
                plant = UNRESOLVED.PdPlant(this.plants.items[i]);
                if (plant.hidden) {
                    continue;
                }
                if (plant.includesPoint(aPoint)) {
                    result = plant;
                    return result;
                }
            }
        }
        return result;
    }
    
    public PdPlant findFirstPlantWithBoundsRectAtPoint(TPoint aPoint) {
        result = new PdPlant();
        PdPlant plant = new PdPlant();
        short plantIndex = 0;
        
        result = null;
        if (this.plants.count > 0) {
            for (plantIndex = this.plants.count - 1; plantIndex >= 0; plantIndex--) {
                // go through list backwards because list order is drawing order is from front to back
                plant = UNRESOLVED.PdPlant(this.plants.items[plantIndex]);
                if (plant.hidden) {
                    continue;
                }
                if (plant.pointInBoundsRect(aPoint)) {
                    result = plant;
                    return result;
                }
            }
        }
        return result;
    }
    
    public void loadPlantObjectsIntoTStrings(TStrings stringList) {
        int i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.plants.count > 0) {
            for (i = 0; i <= this.plants.count - 1; i++) {
                plant = UNRESOLVED.PdPlant(this.plants.items[i]);
                stringList.AddObject(plant.getName, plant);
            }
        }
    }
    
    // --------------------------------------------------------------------------------------- input/output 
    public void loadPlantsFromFile(String fileName, boolean inPlantMover) {
        TextFile inputFile = new TextFile();
        PdPlant plant = new PdPlant();
        String aLine = "";
        String plantName = "";
        boolean concentratedInFile = false;
        boolean concentratedLastTimeSaved = false;
        int lineCount = 0;
        
        AssignFile(inputFile, fileName);
        try {
            // v1.5
            UNRESOLVED.setDecimalSeparator;
            Reset(inputFile);
            this.plants.clear;
            // defaults in case things are missing from file
            this.plantDrawOffset_mm = UNRESOLVED.SetSinglePoint(0, 0);
            this.plantDrawScale_PixelsPerMm = 1.0;
            this.mainWindowViewMode = UNRESOLVED.domain.options.mainWindowViewMode;
            this.mainWindowOrientation = UNRESOLVED.domain.options.mainWindowOrientation;
            this.showBoundsRectangle = UNRESOLVED.domain.options.showBoundsRectangle;
            concentratedLastTimeSaved = false;
            this.fitInVisibleAreaForConcentrationChange = false;
            while (!UNRESOLVED.eof(inputFile)) {
                // cfk testing
                UNRESOLVED.tolerantReadln(inputFile, aLine);
                if ((aLine == "") || (UNRESOLVED.pos(";", aLine) == 1)) {
                    continue;
                }
                if (UNRESOLVED.pos("offset=", aLine) == 1) {
                    this.plantDrawOffset_mm = UNRESOLVED.stringToSinglePoint(UNRESOLVED.stringBeyond(aLine, "="));
                } else if (UNRESOLVED.pos("scale=", aLine) == 1) {
                    try {
                        this.plantDrawScale_PixelsPerMm = intround(StrToFloat(UNRESOLVED.stringBeyond(aLine, "=")) * 100.0) / 100.0;
                    } catch (Exception e) {
                        this.plantDrawScale_PixelsPerMm = 1.0;
                    }
                } else if (UNRESOLVED.pos("concentrated=", aLine) == 1) {
                    concentratedLastTimeSaved = UNRESOLVED.domain.viewPlantsInMainWindowOnePlantAtATime;
                    if (UNRESOLVED.domain.options.ignoreWindowSettingsInFile) {
                        // v2.1 if ignoring settings in file, use current settings, otherwise use what is in file
                        concentratedInFile = (this.mainWindowViewMode == UNRESOLVED.kViewPlantsInMainWindowOneAtATime);
                    } else {
                        concentratedInFile = UNRESOLVED.strToBool(UNRESOLVED.stringBeyond(aLine, "="));
                    }
                    if (concentratedInFile) {
                        this.mainWindowViewMode = UNRESOLVED.kViewPlantsInMainWindowOneAtATime;
                    } else {
                        this.mainWindowViewMode = UNRESOLVED.kViewPlantsInMainWindowFreeFloating;
                    }
                    if (!inPlantMover) {
                        UNRESOLVED.domain.options.mainWindowViewMode = this.mainWindowViewMode;
                    }
                    this.fitInVisibleAreaForConcentrationChange = concentratedInFile && !concentratedLastTimeSaved;
                } else if (UNRESOLVED.pos("orientation (top/side)=", aLine) == 1) {
                    if (!UNRESOLVED.domain.options.ignoreWindowSettingsInFile) {
                        // v2.1 only read if not ignoring settings in file
                        this.mainWindowOrientation = StrToInt(UNRESOLVED.stringBeyond(aLine, "="));
                    }
                } else if (UNRESOLVED.pos("boxes=", aLine) == 1) {
                    this.showBoundsRectangle = UNRESOLVED.strToBool(UNRESOLVED.stringBeyond(aLine, "="));
                    if (!inPlantMover) {
                        UNRESOLVED.domain.options.showBoundsRectangle = this.showBoundsRectangle;
                    }
                    if ((UNRESOLVED.MainForm != null) && (!UNRESOLVED.MainForm.inFormCreation) && (!inPlantMover)) {
                        UNRESOLVED.MainForm.updateForChangeToDomainOptions;
                        UNRESOLVED.MainForm.copyDrawingBitmapToPaintBox;
                    }
                } else if (UNRESOLVED.pos("[", aLine) == 1) {
                    // plant start line
                    checkVersionNumberInPlantNameLine(aLine);
                    plant = UNRESOLVED.PdPlant.create;
                    plantName = UNRESOLVED.stringBeyond(aLine, "[");
                    plantName = UNRESOLVED.stringUpTo(plantName, "]");
                    plant.setName(plantName);
                    UNRESOLVED.domain.parameterManager.setAllReadFlagsToFalse;
                    // cfk change v1.3
                    // changed reading end of plant to read "end PlantStudio plant" instead of empty line because
                    // sometimes text wrapping puts empty lines in, not a good measure of completion.
                    // now end of plant must be there to be read. could produce endless loop if no end
                    // of plant, so stop at absolute cutoff of 300 non-empty, non-comment lines (there are now 215 parameters).
                    // also stop reading if reach next plant square bracket or end of file.
                    // v2.0 increased number of params to 350 so 300 is problem, changed to 3000 to avoid this in future, oops
                    lineCount = 0;
                    while ((UNRESOLVED.pos(UNRESOLVED.kPlantAsTextEndString, aLine) <= 0) && (lineCount <= 3000)) {
                        // aLine <> '' do
                        UNRESOLVED.tolerantReadln(inputFile, aLine);
                        if ((UNRESOLVED.pos("[", aLine) == 1) || (UNRESOLVED.eof(inputFile))) {
                            // v1.60 reversed order of the next two lines -- fixes infinite loop when no end of plant
                            // v1.3 added check for next plant or eof
                            break;
                        }
                        if ((trim(aLine) == "") || (UNRESOLVED.pos(";", aLine) == 1)) {
                            // v1.3 added skip empty lines
                            continue;
                        }
                        plant.readLineAndTdoFromPlantFile(aLine, inputFile);
                        lineCount = lineCount + 1;
                    }
                    plant.finishLoadingOrDefaulting(UNRESOLVED.kCheckForUnreadParams);
                    this.plants.add(plant);
                }
            }
        } finally {
            CloseFile(inputFile);
        }
    }
    
    public void savePlantsToFile(String fileName, boolean inPlantMover) {
        TextFile outputFile = new TextFile();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.plants.count <= 0) {
            return;
        }
        AssignFile(outputFile, fileName);
        try {
            // v1.5
            UNRESOLVED.setDecimalSeparator;
            if (!inPlantMover) {
                // update before writing out (keep as read in if in mover)
                // plantDrawOffset_mm is used from here
                // plantDrawScale_PixelsPerMm is used from here
                this.mainWindowViewMode = UNRESOLVED.domain.options.mainWindowViewMode;
                this.mainWindowOrientation = UNRESOLVED.domain.options.mainWindowOrientation;
                this.showBoundsRectangle = UNRESOLVED.domain.options.showBoundsRectangle;
            }
            Rewrite(outputFile);
            // v2.0
            writeln(outputFile, "; PlantStudio version 2.0 plant file");
            writeln(outputFile, "offset=" + UNRESOLVED.singlePointToString(this.plantDrawOffset_mm));
            writeln(outputFile, "scale=" + UNRESOLVED.digitValueString(this.plantDrawScale_PixelsPerMm));
            if (this.mainWindowViewMode == UNRESOLVED.kViewPlantsInMainWindowOneAtATime) {
                writeln(outputFile, "concentrated=true");
            } else {
                writeln(outputFile, "concentrated=false");
            }
            // v2.0
            writeln(outputFile, "orientation (top/side)=" + IntToStr(this.mainWindowOrientation));
            // v2.0
            writeln(outputFile, "boxes=" + UNRESOLVED.boolToStr(this.showBoundsRectangle));
            writeln(outputFile);
            for (i = 0; i <= this.plants.count - 1; i++) {
                plant = UNRESOLVED.PdPlant(this.plants.items[i]);
                if (plant == null) {
                    continue;
                }
                plant.writeToPlantFile(outputFile);
            }
        } finally {
            CloseFile(outputFile);
        }
    }
    
    // v1.11
    public int reconcileFileWithTdoLibrary(String plantFileName, String tdoLibrary) {
        result = 0;
        TListCollection plantFileTdos = new TListCollection();
        TListCollection libraryFileTdos = new TListCollection();
        TextFile plantFile = new TextFile();
        TextFile tdoFile = new TextFile();
        TextFile outputTdoFile = new TextFile();
        short i = 0;
        short j = 0;
        KfObject3d tdo = new KfObject3d();
        KfObject3d plantFileTdo = new KfObject3d();
        KfObject3d libraryTdo = new KfObject3d();
        boolean matchInLibrary = false;
        String aLine = "";
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        
        result = 0;
        if (!FileExists(plantFileName)) {
            // check that files exist
            plantFileName = UNRESOLVED.getFileOpenInfo(UNRESOLVED.kFileTypePlant, plantFileName, "Choose a plant file");
            if (plantFileName == "") {
                return result;
            }
        }
        if (!FileExists(tdoLibrary)) {
            tdoLibrary = UNRESOLVED.getFileOpenInfo(UNRESOLVED.kFileTypeTdo, tdoLibrary, "Choose a 3D object library (tdo) file");
            if (tdoLibrary == "") {
                return result;
            }
        }
        plantFileTdos = UNRESOLVED.TListCollection.create;
        libraryFileTdos = UNRESOLVED.TListCollection.create;
        try {
            ucursor.cursor_startWait();
            // read tdos from plants
            AssignFile(plantFile, plantFileName);
            try {
                // v1.5
                UNRESOLVED.setDecimalSeparator;
                Reset(plantFile);
                while (!UNRESOLVED.eof(plantFile)) {
                    UNRESOLVED.readln(plantFile, aLine);
                    if (UNRESOLVED.pos(UNRESOLVED.kStartTdoString, aLine) > 0) {
                        tdo = UNRESOLVED.KfObject3d.create;
                        tdo.readFromFileStream(plantFile, UNRESOLVED.kInTdoLibrary);
                        plantFileTdos.add(tdo);
                    }
                }
            } finally {
                CloseFile(plantFile);
            }
            // read tdos from library
            AssignFile(tdoFile, tdoLibrary);
            try {
                // v1.5
                UNRESOLVED.setDecimalSeparator;
                Reset(tdoFile);
                while (!UNRESOLVED.eof(tdoFile)) {
                    tdo = UNRESOLVED.KfObject3D.create;
                    tdo.readFromFileStream(tdoFile, UNRESOLVED.kInTdoLibrary);
                    libraryFileTdos.add(tdo);
                }
            } finally {
                CloseFile(tdoFile);
            }
            if (plantFileTdos.count > 0) {
                for (i = 0; i <= plantFileTdos.count - 1; i++) {
                    // add plant tdos not in library list to library list
                    plantFileTdo = UNRESOLVED.KfObject3D(plantFileTdos.items[i]);
                    matchInLibrary = false;
                    if (libraryFileTdos.count > 0) {
                        for (j = 0; j <= libraryFileTdos.count - 1; j++) {
                            libraryTdo = UNRESOLVED.KfObject3d(libraryFileTdos.items[j]);
                            if (plantFileTdo.isSameAs(libraryTdo)) {
                                matchInLibrary = true;
                                break;
                            }
                        }
                    }
                    if (!matchInLibrary) {
                        tdo = UNRESOLVED.KfObject3D.create;
                        tdo.copyFrom(plantFileTdo);
                        libraryFileTdos.add(tdo);
                        result += 1;
                    }
                }
            }
            if (result > 0) {
                if (UNRESOLVED.getFileSaveInfo(UNRESOLVED.kFileTypeTdo, UNRESOLVED.kDontAskForFileName, tdoLibrary, fileInfo)) {
                    // if any tdos in plant file but not in library, rewrite library
                    AssignFile(outputTdoFile, fileInfo.tempFile);
                    try {
                        // v1.5
                        UNRESOLVED.setDecimalSeparator;
                        Rewrite(outputTdoFile);
                        UNRESOLVED.startFileSave(fileInfo);
                        if (libraryFileTdos.count > 0) {
                            for (i = 0; i <= libraryFileTdos.count - 1; i++) {
                                tdo = (UNRESOLVED.KfObject3D)UNRESOLVED.TObject(libraryFileTdos.items[i]);
                                if (tdo == null) {
                                    continue;
                                }
                                tdo.writeToFileStream(outputTdoFile, UNRESOLVED.kInTdoLibrary);
                            }
                        }
                        fileInfo.writingWasSuccessful = true;
                    } finally {
                        CloseFile(outputTdoFile);
                        UNRESOLVED.cleanUpAfterFileSave(fileInfo);
                    }
                }
            }
        } finally {
            plantFileTdos.free;
            libraryFileTdos.free;
            ucursor.cursor_stopWait();
        }
        return result;
    }
    
    public short visiblePlantCount() {
        result = 0;
        short i = 0;
        
        result = 0;
        if (this.plants.count > 0) {
            for (i = 0; i <= this.plants.count - 1; i++) {
                if (!UNRESOLVED.PdPlant(this.plants.items[i]).hidden) {
                    result += 1;
                }
            }
        }
        return result;
    }
    
    // --------------------------------------------------------------------------------------- drawing 
    public void drawOnInvalidRect(TCanvas destCanvas, TList selectedPlants, TRect invalidRect, boolean excludeInvisiblePlants, boolean excludeNonSelectedPlants) {
        int plantIndex = 0;
        PdPlant plant = new PdPlant();
        TRect intersection = new TRect();
        TRect plantRect = new TRect();
        longbool intersectResult = new longbool();
        boolean includePlant = false;
        long partsDrawn = 0;
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        partsDrawn = 0;
        if (this.plants.count > 0) {
            for (plantIndex = this.plants.count - 1; plantIndex >= 0; plantIndex--) {
                // go through list backwards because list order is drawing order is from front to back
                plant = UNRESOLVED.PdPlant(this.plants.items[plantIndex]);
                includePlant = false;
                plantRect = plant.boundsRect_pixels;
                if ((plantRect.Left == 0) && (plantRect.Right == 0) && (plantRect.Top == 0) && (plantRect.Bottom == 0)) {
                    // if plant has just been read in, recalculate bounds rect by drawing it 
                    includePlant = true;
                }
                intersectResult = delphi_compatability.IntersectRect(intersection, plantRect, invalidRect);
                includePlant = includePlant || intersectResult;
                if (excludeInvisiblePlants) {
                    includePlant = includePlant && !plant.hidden;
                }
                if (excludeNonSelectedPlants) {
                    includePlant = includePlant && (selectedPlants.IndexOf(plant) >= 0);
                }
                if (includePlant) {
                    plant.plantPartsDrawnAtStart = partsDrawn;
                    try {
                        plant.computeBounds = true;
                        if ((UNRESOLVED.domain.options.cachePlantBitmaps) && (!UNRESOLVED.domain.drawingToMakeCopyBitmap)) {
                            destCanvas.Draw(plantRect.Left, plantRect.Top, plant.previewCache);
                        } else {
                            plant.drawOn(destCanvas);
                        }
                    } finally {
                        plant.computeBounds = false;
                    }
                    partsDrawn = partsDrawn + plant.totalPlantParts;
                }
            }
        }
    }
    
    //procedure drawWithOpenGLOnInvalidRect(form: TForm; selectedPlants: TList; invalidRect: TRect;
    //  glRect: TRect; excludeInvisiblePlants, excludeNonSelectedPlants: boolean);
    public long totalPlantPartCountInInvalidRect(TList selectedPlants, TRect invalidRect, boolean excludeInvisiblePlants, boolean excludeNonSelectedPlants) {
        result = 0;
        int plantIndex = 0;
        PdPlant plant = new PdPlant();
        TRect intersection = new TRect();
        TRect plantRect = new TRect();
        longbool intersectResult = new longbool();
        boolean includePlant = false;
        
        result = 0;
        if (delphi_compatability.Application.terminated) {
            return result;
        }
        if (this.plants.count > 0) {
            for (plantIndex = this.plants.count - 1; plantIndex >= 0; plantIndex--) {
                plant = UNRESOLVED.PdPlant(this.plants.items[plantIndex]);
                includePlant = false;
                plantRect = plant.boundsRect_pixels;
                if ((plantRect.Left == 0) && (plantRect.Right == 0) && (plantRect.Top == 0) && (plantRect.Bottom == 0)) {
                    // if plant has just been read in, recalculate bounds rect by drawing it 
                    includePlant = true;
                }
                intersectResult = delphi_compatability.IntersectRect(intersection, plantRect, invalidRect);
                includePlant = includePlant || intersectResult;
                if (excludeInvisiblePlants) {
                    includePlant = includePlant && !plant.hidden;
                }
                if (excludeNonSelectedPlants) {
                    includePlant = includePlant && (selectedPlants.IndexOf(plant) >= 0);
                }
                if (includePlant) {
                    plant.countPlantParts;
                    result = result + plant.totalPlantParts;
                }
            }
        }
        return result;
    }
    
    public void zeroAllBoundsRectsToForceRedraw() {
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.plants.count > 0) {
            for (i = 0; i <= this.plants.count - 1; i++) {
                plant = UNRESOLVED.PdPlant(this.plants.items[i]);
                plant.setBoundsRect_pixels(Rect(0, 0, 0, 0));
            }
        }
    }
    
    public void fillListWithPlantsInRectangle(TRect aRect, TList aList) {
        int plantIndex = 0;
        PdPlant plant = new PdPlant();
        TRect intersection = new TRect();
        longbool intersectResult = new longbool();
        boolean includePlant = false;
        
        if (aList == null) {
            throw new GeneralException.create("Problem: Nil list in method PdPlantManager.fillListWithPlantsInRectangle.");
        }
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.plants.count > 0) {
            for (plantIndex = 0; plantIndex <= this.plants.count - 1; plantIndex++) {
                plant = UNRESOLVED.PdPlant(this.plants.items[plantIndex]);
                includePlant = false;
                intersectResult = delphi_compatability.IntersectRect(intersection, plant.boundsRect_pixels, aRect);
                includePlant = includePlant || intersectResult;
                includePlant = includePlant && !plant.hidden;
                if (includePlant) {
                    aList.Add(plant);
                }
            }
        }
    }
    
    public void write3DOutputFileToFileName(TList selectedPlants, boolean excludeInvisiblePlants, boolean excludeNonSelectedPlants, String fileName, short outputType) {
        PdPlant plant = new PdPlant();
        int i = 0;
        boolean includePlant = false;
        TRect includeRect = new TRect();
        TList includedPlants = new TList();
        boolean translatePlants = false;
        KfTurtle turtle = new KfTurtle();
        
        UNRESOLVED.setDecimalSeparator;
        includedPlants = null;
        includeRect = this.combinedPlantBoundsRects(selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants);
        if ((UNRESOLVED.rWidth(includeRect) <= 0) || (UNRESOLVED.rHeight(includeRect) <= 0)) {
            return;
        }
        includedPlants = delphi_compatability.TList().Create();
        turtle = UNRESOLVED.KfTurtle.createFor3DOutput(outputType, fileName);
        try {
            turtle.start3DExportFile;
            if (this.plants.count > 0) {
                for (i = 0; i <= this.plants.count - 1; i++) {
                    // count the plants to be drawn so we know if there is more than one
                    plant = UNRESOLVED.PdPlant(this.plants.items[i]);
                    includePlant = true;
                    if (excludeInvisiblePlants) {
                        includePlant = includePlant && !plant.hidden;
                    }
                    if (excludeNonSelectedPlants) {
                        includePlant = includePlant && (selectedPlants.IndexOf(plant) >= 0);
                    }
                    if (includePlant) {
                        includedPlants.Add(plant);
                    }
                }
            }
            if (includedPlants.Count <= 1) {
                // if only one plant, don't translate or scale
                translatePlants = false;
            } else {
                translatePlants = UNRESOLVED.domain.exportOptionsFor3D[outputType].translatePlantsToWindowPositions;
            }
            if (includedPlants.Count > 0) {
                for (i = 0; i <= includedPlants.Count - 1; i++) {
                    // iterate over included plants
                    UNRESOLVED.PdPlant(includedPlants.Items[i]).saveToGlobal3DOutputFile(i, translatePlants, includeRect, outputType, turtle);
                }
            }
        } finally {
            turtle.end3DExportFile;
            turtle.free;
            turtle = null;
            includedPlants.free;
            includedPlants = null;
        }
    }
    
    public TRect combinedPlantBoundsRects(TList selectedPlants, boolean excludeInvisiblePlants, boolean excludeNonSelectedPlants) {
        result = new TRect();
        PdPlant plant = new PdPlant();
        int plantIndex = 0;
        boolean includePlant = false;
        
        result = delphi_compatability.Bounds(0, 0, 0, 0);
        if (this.plants.count > 0) {
            for (plantIndex = 0; plantIndex <= this.plants.count - 1; plantIndex++) {
                plant = UNRESOLVED.PdPlant(this.plants.items[plantIndex]);
                includePlant = true;
                if (excludeInvisiblePlants) {
                    includePlant = includePlant && !plant.hidden;
                }
                if (excludeNonSelectedPlants) {
                    includePlant = includePlant && (selectedPlants.IndexOf(plant) >= 0);
                }
                if (includePlant) {
                    delphi_compatability.UnionRect(result, result, plant.boundsRect_pixels);
                }
            }
        }
        return result;
    }
    
    public TRect largestPlantBoundsRect(TList selectedPlants, boolean excludeInvisiblePlants, boolean excludeNonSelectedPlants) {
        result = new TRect();
        PdPlant plant = new PdPlant();
        int plantIndex = 0;
        boolean includePlant = false;
        TRect plantRect = new TRect();
        
        result = delphi_compatability.Bounds(0, 0, 0, 0);
        if (this.plants.count > 0) {
            for (plantIndex = 0; plantIndex <= this.plants.count - 1; plantIndex++) {
                plant = UNRESOLVED.PdPlant(this.plants.items[plantIndex]);
                includePlant = true;
                if (excludeInvisiblePlants) {
                    includePlant = includePlant && !plant.hidden;
                }
                if (excludeNonSelectedPlants) {
                    includePlant = includePlant && (selectedPlants.IndexOf(plant) >= 0);
                }
                if (includePlant) {
                    plantRect = plant.boundsRect_pixels;
                    if (UNRESOLVED.rWidth(plantRect) > result.Right) {
                        result.Right = UNRESOLVED.rWidth(plantRect);
                    }
                    if (UNRESOLVED.rHeight(plantRect) > result.Bottom) {
                        result.Bottom = UNRESOLVED.rHeight(plantRect);
                    }
                }
            }
        }
        return result;
    }
    
    // --------------------------------------------------------------------------------------- private clipboard 
    public void copyPlantsInListToPrivatePlantClipboard(TList aList) {
        short i = 0;
        PdPlant plant = new PdPlant();
        PdPlant newPlant = new PdPlant();
        
        this.privatePlantClipboard.clear;
        if (aList.Count > 0) {
            for (i = 0; i <= aList.Count - 1; i++) {
                plant = UNRESOLVED.PdPlant(aList.Items[i]);
                newPlant = UNRESOLVED.PdPlant.create;
                plant.copyTo(newPlant);
                newPlant.setName("Copy of " + newPlant.getName);
                this.privatePlantClipboard.add(newPlant);
            }
        }
    }
    
    public void setCopiedFromMainWindowFlagInClipboardPlants() {
        short i = 0;
        
        if (this.privatePlantClipboard.count > 0) {
            for (i = 0; i <= this.privatePlantClipboard.count - 1; i++) {
                UNRESOLVED.PdPlant(this.privatePlantClipboard.items[i]).justCopiedFromMainWindow = true;
            }
        }
    }
    
    public void pastePlantsFromPrivatePlantClipboardToList(TList aList) {
        short i = 0;
        PdPlant plant = new PdPlant();
        PdPlant newPlant = new PdPlant();
        
        if (this.privatePlantClipboard.count > 0) {
            for (i = 0; i <= this.privatePlantClipboard.count - 1; i++) {
                // caller takes responsibility of freeing plants 
                plant = UNRESOLVED.PdPlant(this.privatePlantClipboard.items[i]);
                newPlant = UNRESOLVED.PdPlant.create;
                plant.copyTo(newPlant);
                newPlant.moveBy(Point(UNRESOLVED.kPasteMoveDistance, 0));
                aList.Add(newPlant);
            }
        }
    }
    
    public void pasteFirstPlantFromPrivatePlantClipboardToPlant(PdPlant newPlant) {
        PdPlant plant = new PdPlant();
        
        if (newPlant == null) {
            // this is used by the breeder and grower windows 
            // caller creates newPlant first 
            return;
        }
        if (this.privatePlantClipboard.count > 0) {
            // caller takes responsibility of freeing plants 
            plant = UNRESOLVED.PdPlant(this.privatePlantClipboard.items[0]);
            plant.copyTo(newPlant);
        }
    }
    
}
