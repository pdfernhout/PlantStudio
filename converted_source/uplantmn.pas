unit Uplantmn;

interface

uses Windows, Classes, Graphics, Forms,
  ucollect, uplant, usupport;

type

PdPlantManager = class
 	public 
  plants: TListCollection;
  privatePlantClipboard: TListCollection;
  plantDrawOffset_mm: SinglePoint;
  plantDrawScale_PixelsPerMm: single;
  fitInVisibleAreaForConcentrationChange: boolean;
  mainWindowOrientation: smallint;
  showBoundsRectangle: boolean;
  mainWindowViewMode: smallint;
  constructor create;
  destructor destroy; override;
  procedure addPlant(newPlant: PdPlant);
  function removePlant(aPlant: PdPlant): boolean;
  function copyFromPlant(plant: PdPlant): PdPlant;
  function plantForIndex(index: longint): PdPlant;
  procedure loadPlantsFromFile(fileName: string; inPlantMover: boolean);
  procedure savePlantsToFile(fileName: string; inPlantMover: boolean);
  procedure loadPlantObjectsIntoTStrings(stringList: TStrings);
  function visiblePlantCount: smallint;
  procedure drawOnInvalidRect(destCanvas: TCanvas; selectedPlants: TList; invalidRect: TRect;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean);
  //procedure drawWithOpenGLOnInvalidRect(form: TForm; selectedPlants: TList; invalidRect: TRect;
  //  glRect: TRect; excludeInvisiblePlants, excludeNonSelectedPlants: boolean);
  function totalPlantPartCountInInvalidRect(selectedPlants: TList; invalidRect: TRect;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean): longint;
  procedure fillListWithPlantsInRectangle(aRect: TRect; aList: TList);
  function combinedPlantBoundsRects(selectedPlants: TList;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean): TRect;
  function largestPlantBoundsRect(selectedPlants: TList;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean): TRect;
  function findPlantAtPoint(aPoint: TPoint): PdPlant;
  function findFirstPlantWithBoundsRectAtPoint(aPoint: TPoint): PdPlant;
  procedure copyPlantsInListToPrivatePlantClipboard(aList: TList);
  procedure setCopiedFromMainWindowFlagInClipboardPlants;
  procedure pastePlantsFromPrivatePlantClipboardToList(aList: TList);
  procedure pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant: PdPlant);
  procedure zeroAllBoundsRectsToForceRedraw;
  function reconcileFileWithTdoLibrary(plantFileName, tdoLibrary: string): integer;  // v1.11
  procedure write3DOutputFileToFileName(selectedPlants: TList;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean; fileName: string; outputType: smallint);
  end;

  procedure checkVersionNumberInPlantNameLine(aLine: string);

implementation

uses SysUtils, Dialogs,
  ucursor, udomain, updcom, uturtle, u3dexport, umain, usplash, utdo, udebug;

constructor PdPlantManager.create;
  begin
  inherited create;
  plants := TListCollection.create;
  privatePlantClipboard := TListCollection.create;
  plantDrawScale_PixelsPerMm := 1.0;
  end;

destructor PdPlantManager.destroy;
	begin
  plants.free;
  plants := nil;
  privatePlantClipboard.free;
  privatePlantClipboard := nil;
  inherited destroy;
  end;

procedure PdPlantManager.addPlant(newPlant: PdPlant);
	begin
  plants.add(newPlant);
  end;

function PdPlantManager.removePlant(aPlant: PdPlant): boolean;
	begin
  { remove returns index of object in list before removal }
  result := (plants.remove(aPlant) >= 0);
  end;

function PdPlantManager.copyFromPlant(plant: PdPlant): PdPlant;
  var
    newPlant: PdPlant;
	begin
  if plant = nil then
    raise Exception.create('Problem: Nil plant in method PdPlantManager.copyFromPlant.');
  newPlant := PdPlant.create;
  plant.copyTo(newPlant);
  plants.add(newPlant);
  result := newPlant;
	end;

function PdPlantManager.plantForIndex(index: longint): PdPlant;
	begin
  result := PdPlant(plants.items[index]);
  end;

function PdPlantManager.findPlantAtPoint(aPoint: TPoint): PdPlant;
  var
    plant: PdPlant;
    i: smallint;
  begin
  result := nil;
  if plants.count > 0 then
    for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      if plant.hidden then continue;
      if plant.includesPoint(aPoint) then
        begin
        result := plant;
        exit;
        end;
      end;
  end;

function PdPlantManager.findFirstPlantWithBoundsRectAtPoint(aPoint: TPoint): PdPlant;
  var
    plant: PdPlant;
    plantIndex: smallint;
  begin
  result := nil;
  // go through list backwards because list order is drawing order is from front to back
  if plants.count > 0 then for plantIndex := plants.count - 1 downto 0 do
      begin
      plant := PdPlant(plants.items[plantIndex]);
      if plant.hidden then continue;
      if plant.pointInBoundsRect(aPoint) then
        begin
        result := plant;
        exit;
        end;
      end;
  end;

procedure PdPlantManager.loadPlantObjectsIntoTStrings(stringList: TStrings);
  var
    i: integer;
    plant: PdPlant;
	begin
  if plants.count > 0 then
    begin
    for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
  	  stringList.addObject(plant.getName, plant);
      end;
    end;
  end;

{ --------------------------------------------------------------------------------------- input/output }
procedure PdPlantManager.loadPlantsFromFile(fileName: string; inPlantMover: boolean);
  var
    inputFile: TextFile;
    plant: PdPlant;
    aLine, plantName: string;
    concentratedInFile, concentratedLastTimeSaved: boolean;
    lineCount: integer;
  begin
  assignFile(inputFile, fileName);
  try
  setDecimalSeparator; // v1.5
  reset(inputFile);
  plants.clear;
  // defaults in case things are missing from file
  self.plantDrawOffset_mm := SetSinglePoint(0,0);
  self.plantDrawScale_PixelsPerMm := 1.0;
  self.mainWindowViewMode := domain.options.mainWindowViewMode;
  self.mainWindowOrientation := domain.options.mainWindowOrientation;
  self.showBoundsRectangle := domain.options.showBoundsRectangle;
  concentratedLastTimeSaved := false;
  self.fitInVisibleAreaForConcentrationChange := false;
  while not eof(inputFile) do
    begin
    tolerantReadln(inputFile, aLine);   // cfk testing
    if (aLine = '') or (pos(';', aLine) = 1) then continue;
    if pos('offset=', aLine) = 1 then
      self.plantDrawOffset_mm := stringToSinglePoint(stringBeyond(aLine, '='))
    else if pos('scale=', aLine) = 1 then
      try
        self.plantDrawScale_PixelsPerMm := round(strToFloat(stringBeyond(aLine, '=')) * 100.0) / 100.0;
      except
        self.plantDrawScale_PixelsPerMm := 1.0;
      end
    else if pos('concentrated=', aLine) = 1 then
      begin
      concentratedLastTimeSaved := domain.viewPlantsInMainWindowOnePlantAtATime;
      // v2.1 if ignoring settings in file, use current settings, otherwise use what is in file
      if domain.options.ignoreWindowSettingsInFile then
        concentratedInFile := (self.mainWindowViewMode = kViewPlantsInMainWindowOneAtATime)
      else
        concentratedInFile := strToBool(stringBeyond(aLine, '='));
      if concentratedInFile then
        self.mainWindowViewMode := kViewPlantsInMainWindowOneAtATime
      else
        self.mainWindowViewMode := kViewPlantsInMainWindowFreeFloating;
      if not inPlantMover then
        domain.options.mainWindowViewMode := self.mainWindowViewMode;
      self.fitInVisibleAreaForConcentrationChange := concentratedInFile and not concentratedLastTimeSaved;
      end
    else if pos('orientation (top/side)=', aLine) = 1 then
      begin
      // v2.1 only read if not ignoring settings in file
      if not domain.options.ignoreWindowSettingsInFile then
        self.mainWindowOrientation := strToInt(stringBeyond(aLine, '='));
      end
    else if pos('boxes=', aLine) = 1 then
      begin
      self.showBoundsRectangle := strToBool(stringBeyond(aLine, '='));
      if not inPlantMover then
        domain.options.showBoundsRectangle := self.showBoundsRectangle;
      if (MainForm <> nil) and (not MainForm.inFormCreation) and (not inPlantMover) then
        begin
        MainForm.updateForChangeToDomainOptions;
        MainForm.copyDrawingBitmapToPaintBox;
        end;
      end
    else if pos('[', aLine) = 1 then // plant start line
      begin
      checkVersionNumberInPlantNameLine(aLine);
      plant := PdPlant.create;
      plantName := stringBeyond(aLine, '[');
      plantName := stringUpTo(plantName, ']');
      plant.setName(plantName);
      domain.parameterManager.setAllReadFlagsToFalse;
      // cfk change v1.3
      // changed reading end of plant to read "end PlantStudio plant" instead of empty line because
      // sometimes text wrapping puts empty lines in, not a good measure of completion.
      // now end of plant must be there to be read. could produce endless loop if no end
      // of plant, so stop at absolute cutoff of 300 non-empty, non-comment lines (there are now 215 parameters).
      // also stop reading if reach next plant square bracket or end of file.
      // v2.0 increased number of params to 350 so 300 is problem, changed to 3000 to avoid this in future, oops
      lineCount := 0;
      while (pos(kPlantAsTextEndString, aLine) <= 0) and (lineCount <= 3000) do // aLine <> '' do
        begin
        tolerantReadln(inputFile, aLine);
        // v1.60 reversed order of the next two lines -- fixes infinite loop when no end of plant
        if (pos('[', aLine) = 1) or (eof(inputFile)) then break; // v1.3 added check for next plant or eof
        if (trim(aLine) = '') or (pos(';', aLine) = 1) then continue;  // v1.3 added skip empty lines
        plant.readLineAndTdoFromPlantFile(aLine, inputFile);
        lineCount := lineCount + 1;
        end;
      plant.finishLoadingOrDefaulting(kCheckForUnreadParams);
      plants.add(plant);
      end;
    end;
  finally
    closeFile(inputFile);
  end;
  end;

procedure checkVersionNumberInPlantNameLine(aLine: string);
  var
    versionNumberString: string;
    plantName: string;
    versionNumber: integer;
  begin
  // assumes line given is plant start line
  // e.g., >>> [rose] start PlantStudio plant <v1.0>
  plantName := stringBetween('[', ']', aLine);
  versionNumberString := stringBetween('<', '>', aLine);
  versionNumberString := stringBetween('v', '.', versionNumberString);
  versionNumber := strToIntDef(versionNumberString, 0);
  if versionNumber > 2 then
    begin
    showMessage('The plant "' + plantName + '" has a major version number of ' + intToStr(versionNumber) + ',' + chr(13)
      + 'which is higher than this major version of PlantStudio (2).' + chr(13) + chr(13)
      + 'That means that although I may be able to read the plant,' + chr(13)
      + 'it will probably look better in the most up-to-date version of PlantStudio,' + chr(13)
      + 'which you can get at the PlantStudio web site.');
    end;
  end;

procedure PdPlantManager.savePlantsToFile(fileName: string; inPlantMover: boolean);
  var
    outputFile: TextFile;
    i: smallint;
    plant: PdPlant;
  begin
  if plants.count <= 0 then exit;
  assignFile(outputFile, fileName);
  try
    setDecimalSeparator; // v1.5
    if not inPlantMover then  // update before writing out (keep as read in if in mover)
      begin
      // plantDrawOffset_mm is used from here
      // plantDrawScale_PixelsPerMm is used from here
      self.mainWindowViewMode := domain.options.mainWindowViewMode;
      self.mainWindowOrientation := domain.options.mainWindowOrientation;
      self.showBoundsRectangle := domain.options.showBoundsRectangle;
      end;
    rewrite(outputFile);
    writeln(outputFile, '; PlantStudio version 2.0 plant file'); // v2.0
    writeln(outputFile, 'offset=' + singlePointToString(self.plantDrawOffset_mm));
    writeln(outputFile, 'scale=' + digitValueString(self.plantDrawScale_PixelsPerMm));
    if self.mainWindowViewMode = kViewPlantsInMainWindowOneAtATime then
      writeln(outputFile, 'concentrated=true')
    else
      writeln(outputFile, 'concentrated=false');
    writeln(outputFile, 'orientation (top/side)=' + intToStr(self.mainWindowOrientation)); // v2.0
    writeln(outputFile, 'boxes=' + boolToStr(self.showBoundsRectangle)); // v2.0
    writeln(outputFile);
    for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      if plant = nil then continue;
      plant.writeToPlantFile(outputFile);
      end;
  finally
    closeFile(outputFile);
  end;
  end;

function PdPlantManager.reconcileFileWithTdoLibrary(plantFileName, tdoLibrary: string): integer;
  var
    plantFileTdos, libraryFileTdos: TListCollection;
    plantFile: TextFile;
    tdoFile: TextFile;
    outputTdoFile: TextFile;
    i, j: smallint;
    tdo, plantFileTdo, libraryTdo: KfObject3d;
    matchInLibrary: boolean;
    aLine: string;
    fileInfo: SaveFileNamesStructure;
  begin
  result := 0;
  // check that files exist
  if not fileExists(plantFileName) then
    begin
    plantFileName := getFileOpenInfo(kFileTypePlant, plantFileName, 'Choose a plant file');
    if plantFileName = '' then exit;
    end;
  if not fileExists(tdoLibrary) then
    begin
    tdoLibrary := getFileOpenInfo(kFileTypeTdo, tdoLibrary, 'Choose a 3D object library (tdo) file');
    if tdoLibrary = '' then exit;
    end;
  plantFileTdos := TListCollection.create;
  libraryFileTdos := TListCollection.create;
  try
  cursor_startWait;
  // read tdos from plants
  assignFile(plantFile, plantFileName);
  try
    setDecimalSeparator; // v1.5
    reset(plantFile);
    while not eof(plantFile) do
      begin
      readln(plantFile, aLine);
      if pos(kStartTdoString, aLine) > 0 then
        begin
        tdo := KfObject3d.create;
        tdo.readFromFileStream(plantFile, kInTdoLibrary);
        plantFileTdos.add(tdo);
        end;
      end;
  finally
    closeFile(plantFile);
  end;
  // read tdos from library
  assignFile(tdoFile, tdoLibrary);
  try
    setDecimalSeparator; // v1.5
    reset(tdoFile);
    while not eof(tdoFile) do
      begin
      tdo := KfObject3D.create;
      tdo.readFromFileStream(tdoFile, kInTdoLibrary);
      libraryFileTdos.add(tdo);
      end;
  finally
    closeFile(tdoFile);
  end;
  // add plant tdos not in library list to library list
  if plantFileTdos.count > 0 then for i := 0 to plantFileTdos.count - 1 do
    begin
    plantFileTdo := KfObject3D(plantFileTdos.items[i]);
    matchInLibrary := false;
    if libraryFileTdos.count > 0 then for j := 0 to libraryFileTdos.count - 1 do
      begin
      libraryTdo := KfObject3d(libraryFileTdos.items[j]);
      if plantFileTdo.isSameAs(libraryTdo) then
        begin
        matchInLibrary := true;
        break;
        end;
      end;
    if not matchInLibrary then
      begin
      tdo := KfObject3D.create;
      tdo.copyFrom(plantFileTdo);
      libraryFileTdos.add(tdo);
      inc(result);
      end;
    end;
  // if any tdos in plant file but not in library, rewrite library
  if result > 0 then
    begin
    if getFileSaveInfo(kFileTypeTdo, kDontAskForFileName, tdoLibrary, fileInfo) then
      begin
      assignFile(outputTdoFile, fileInfo.tempFile);
      try
        setDecimalSeparator; // v1.5
        rewrite(outputTdoFile);
        startFileSave(fileInfo);
        if libraryFileTdos.count > 0 then for i := 0 to libraryFileTdos.count - 1 do
          begin
          tdo := TObject(libraryFileTdos.items[i]) as KfObject3D;
          if tdo = nil then continue;
          tdo.writeToFileStream(outputTdoFile, kInTdoLibrary);
          end;
        fileInfo.writingWasSuccessful := true;
      finally
        closeFile(outputTdoFile);
        cleanUpAfterFileSave(fileInfo);
      end;
      end;
    end;
  finally
    plantFileTdos.free;
    libraryFileTdos.free;
    cursor_stopWait;
  end;
  end;

function PdPlantManager.visiblePlantCount: smallint;
  var
    i: smallint;
  begin
  result := 0;
  if plants.count > 0 then
    for i := 0 to plants.count - 1 do
      if not PdPlant(plants.items[i]).hidden then inc(result);
  end;

{ --------------------------------------------------------------------------------------- drawing }
procedure PdPlantManager.drawOnInvalidRect(destCanvas: TCanvas; selectedPlants: TList; invalidRect: TRect;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean);
	var
    plantIndex: integer;
    plant: PdPlant;
    intersection, plantRect: TRect;
    intersectResult: longbool;
    includePlant: boolean;
    partsDrawn: longint;
	begin
  if application.terminated then exit;
  partsDrawn := 0;
  // go through list backwards because list order is drawing order is from front to back
  if plants.count > 0 then for plantIndex := plants.count - 1 downto 0 do
    begin
    plant := PdPlant(plants.items[plantIndex]);
    includePlant := false;
    plantRect := plant.boundsRect_pixels;
    with plantRect do
      { if plant has just been read in, recalculate bounds rect by drawing it }
      if (left = 0) and (right = 0) and (top = 0) and (bottom = 0) then
        includePlant := true;
      intersectResult := IntersectRect(intersection, plantRect, invalidRect);
      includePlant := includePlant or intersectResult;
      if excludeInvisiblePlants then includePlant := includePlant and not plant.hidden;
      if excludeNonSelectedPlants then includePlant := includePlant and (selectedPlants.indexOf(plant) >= 0);
      if includePlant then
        begin
        plant.plantPartsDrawnAtStart := partsDrawn;
        try
          plant.computeBounds := true;
          if (domain.options.cachePlantBitmaps) and (not domain.drawingToMakeCopyBitmap) then
            destCanvas.draw(plantRect.left, plantRect.top, plant.previewCache)
          else
            plant.drawOn(destCanvas);
        finally
          plant.computeBounds := false;
        end;
        partsDrawn := partsDrawn + plant.totalPlantParts;
        end;
    end;
  end;

function PdPlantManager.totalPlantPartCountInInvalidRect(selectedPlants: TList; invalidRect: TRect;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean): longint;
	var
    plantIndex: integer;
    plant: PdPlant;
    intersection, plantRect: TRect;
    intersectResult: longbool;
    includePlant: boolean;
	begin
  result := 0;
  if application.terminated then exit;
  if plants.count > 0 then for plantIndex := plants.count - 1 downto 0 do
    begin
    plant := PdPlant(plants.items[plantIndex]);
    includePlant := false;
    plantRect := plant.boundsRect_pixels;
    with plantRect do
      { if plant has just been read in, recalculate bounds rect by drawing it }
      if (left = 0) and (right = 0) and (top = 0) and (bottom = 0) then
        includePlant := true;
    intersectResult := IntersectRect(intersection, plantRect, invalidRect);
    includePlant := includePlant or intersectResult;
    if excludeInvisiblePlants then includePlant := includePlant and not plant.hidden;
    if excludeNonSelectedPlants then includePlant := includePlant and (selectedPlants.indexOf(plant) >= 0);
    if includePlant then
      begin
      plant.countPlantParts;
      result := result + plant.totalPlantParts;
      end;
    end;
  end;

procedure PdPlantManager.zeroAllBoundsRectsToForceRedraw;
  var
    i: smallint;
    plant: PdPlant;
  begin
  if plants.count > 0 then
    for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      plant.setBoundsRect_pixels(rect(0, 0, 0, 0));
      end;
  end;

procedure PdPlantManager.fillListWithPlantsInRectangle(aRect: TRect; aList: TList);
	var
    plantIndex: integer;
    plant: PdPlant;
    intersection: TRect;
    intersectResult: longbool;
    includePlant: boolean;
  begin
  if aList = nil then
    raise Exception.create('Problem: Nil list in method PdPlantManager.fillListWithPlantsInRectangle.');
  if application.terminated then exit;
  if plants.count > 0 then for plantIndex := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[plantIndex]);
    includePlant := false;
    
    intersectResult := IntersectRect(intersection, plant.boundsRect_pixels, aRect);
    includePlant := includePlant or intersectResult;
    includePlant := includePlant and not plant.hidden;
    if includePlant then
      aList.add(plant);
    end;
  end;

procedure PdPlantManager.write3DOutputFileToFileName(selectedPlants: TList;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean; fileName: string; outputType: smallint);
  var
	  plant: PdPlant;
    i: integer;
    includePlant: boolean;
    includeRect: TRect;
    includedPlants: TList;
    translatePlants: boolean;
    turtle: KfTurtle;
  begin
  setDecimalSeparator;
  includedPlants := nil;
  includeRect := self.combinedPlantBoundsRects(selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants);
  if (rWidth(includeRect) <= 0) or (rHeight(includeRect) <= 0) then exit;
  includedPlants := TList.create;
  turtle := KfTurtle.createFor3DOutput(outputType, fileName);
  try
    turtle.start3DExportFile;
    // count the plants to be drawn so we know if there is more than one
    if plants.count > 0 then for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      includePlant := true;
      if excludeInvisiblePlants then includePlant := includePlant and not plant.hidden;
      if excludeNonSelectedPlants then includePlant := includePlant and (selectedPlants.indexOf(plant) >= 0);
      if includePlant then includedPlants.add(plant);
      end;
    // if only one plant, don't translate or scale
    if includedPlants.count <= 1 then
      translatePlants := false
    else
      translatePlants := domain.exportOptionsFor3D[outputType].translatePlantsToWindowPositions;
    // iterate over included plants
    if includedPlants.count > 0 then for i := 0 to includedPlants.count - 1 do
      PdPlant(includedPlants.items[i]).saveToGlobal3DOutputFile(i, translatePlants,
        includeRect, outputType, turtle);
  finally
    turtle.end3DExportFile;
    turtle.free;
    turtle := nil;
    includedPlants.free;
    includedPlants := nil;
  end;
  end;

function PdPlantManager.combinedPlantBoundsRects(selectedPlants: TList;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean): TRect;
  var
	  plant: PdPlant;
    plantIndex: integer;
    includePlant: boolean;
	begin
  result := bounds(0,0,0,0);
  if plants.count > 0 then for plantIndex := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[plantIndex]);
    includePlant := true;
    if excludeInvisiblePlants then includePlant := includePlant and not plant.hidden;
    if excludeNonSelectedPlants then includePlant := includePlant and (selectedPlants.indexOf(plant) >= 0);
    if includePlant then
      unionRect(result, result, plant.boundsRect_pixels);
    end;
  end;

function PdPlantManager.largestPlantBoundsRect(selectedPlants: TList;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean): TRect;
  var
	  plant: PdPlant;
    plantIndex: integer;
    includePlant: boolean;
    plantRect: TRect;
	begin
  result := bounds(0,0,0,0);
  if plants.count > 0 then for plantIndex := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[plantIndex]);
    includePlant := true;
    if excludeInvisiblePlants then includePlant := includePlant and not plant.hidden;
    if excludeNonSelectedPlants then includePlant := includePlant and (selectedPlants.indexOf(plant) >= 0);
    if includePlant then
      begin
      plantRect := plant.boundsRect_pixels;
      if rWidth(plantRect) > result.right then
        result.right := rWidth(plantRect);
      if rHeight(plantRect) > result.bottom then
        result.bottom := rHeight(plantRect);
      end;
    end;
  end;

{ --------------------------------------------------------------------------------------- private clipboard }
procedure PdPlantManager.copyPlantsInListToPrivatePlantClipboard(aList: TList);
  var
    i: smallint;
    plant, newPlant: PdPlant;
  begin
  privatePlantClipboard.clear;
  if aList.count > 0 then for i := 0 to aList.count - 1 do
    begin
    plant := PdPlant(aList.items[i]);
    newPlant := PdPlant.create;
    plant.copyTo(newPlant);
    newPlant.setName('Copy of ' + newPlant.getName);
    privatePlantClipboard.add(newPlant);
    end;
  end;

procedure PdPlantManager.setCopiedFromMainWindowFlagInClipboardPlants;
  var
    i: smallint;
  begin
  if privatePlantClipboard.count > 0 then for i := 0 to privatePlantClipboard.count - 1 do
    PdPlant(privatePlantClipboard.items[i]).justCopiedFromMainWindow := true;
  end;

procedure PdPlantManager.pastePlantsFromPrivatePlantClipboardToList(aList: TList);
  var
    i: smallint;
    plant, newPlant: PdPlant;
  begin
  { caller takes responsibility of freeing plants }
  if privatePlantClipboard.count > 0 then for i := 0 to privatePlantClipboard.count - 1 do
    begin
    plant := PdPlant(privatePlantClipboard.items[i]);
    newPlant := PdPlant.create;
    plant.copyTo(newPlant);
    newPlant.moveBy(point(kPasteMoveDistance, 0));
    aList.add(newPlant);
    end;
  end;

procedure PdPlantManager.pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant: PdPlant);
  var
    plant: PdPlant;
  begin
  { this is used by the breeder and grower windows }
  { caller creates newPlant first }
  if newPlant = nil then exit;
  { caller takes responsibility of freeing plants }
  if privatePlantClipboard.count > 0 then
    begin
    plant := PdPlant(privatePlantClipboard.items[0]);
    plant.copyTo(newPlant);
    end;
  end;

end.
