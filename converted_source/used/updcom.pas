unit updcom;

interface

uses SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls, Forms, Dialogs, StdCtrls, ExtCtrls,
  ucollect, usupport, ucommand, uparams, uplant, utdo, ugener, ubrstrat, udomain, uturtle, u3dexport, uamendmt;

const
  kRotateNotInitialized = 0; kRotateX = 1; kRotateY = 2; kRotateZ = 3;
  kCopyToClipboard = true; kDontCopyToClipboard = false;
  kNewPlantAge = 5;
  kNewPlantPosition = 100;
  kHide = true; kShow = false;
  kSendBackward = true; kBringForward = false;
  kPasteMoveDistance = 40; 
  kCreateFirstGeneration = true; kDontCreateFirstGeneration = false;
  kAddAtEnd = -1;
  kUp = 0;  kDown = 1; kLeft = 2; kRight = 3;
  kChangeWidth = true; kChangeHeight = false;

var
  numPlantsCreatedThisSession: longint;

type

{ value classes to save information about each plant in list }
PdBooleanValue = class
  public
  saveBoolean: boolean;
  constructor createWithBoolean(aBoolean: boolean);
  end;

PdPointValue = class
  public
  savePoint: TPoint;
  constructor createWithPoint(aPoint: TPoint);
  end;

PdSingleValue = class
  public
  saveSingle: single;
  constructor createWithSingle(aSingle: single);
  end;

PdSinglePointValue = class
  public
  x, y: single;
  constructor createWithSingleXY(anX, aY: single);
  end;

PdXYZValue = class
  public
  x, y, z: single;
  constructor createWithXYZ(anX, aY, aZ: single);
  end;

PdSmallintValue = class
  public
  saveSmallint: smallint;
  constructor createWithSmallint(aSmallint: smallint);
  end;

PdLongintValue = class
  public
  saveLongint: longint;
  constructor createWithLongint(aLongint: longint);
  end;

PdColorValue = class
  public
  saveColor: TColorRef;
  constructor createWithColor(aColor: TColorRef);
  end;

{ -------------------------------------- commands that affect only the drawing area (and domain options) }
PdScrollCommand = class(PdCommand)
  public
  dragStartPoint: TPoint;
  oldOffset_mm, newOffSet_mm: SinglePoint;
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand; override;
	procedure undoCommand; override;
	procedure redoCommand; override;
  function description: string; override;
  end;

PdChangeMagnificationCommand = class(PdCommand)
  public
  startDragPoint: TPoint;
  oldScale_PixelsPerMm, newScale_pixelsPerMm: single;
  oldOffset_mm, newOffset_mm, clickPoint: SinglePoint;
  shift: boolean;
  constructor createWithNewScaleAndPoint(aNewScale: single; aPoint: TPoint);
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand; override;
  procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdCenterDrawingCommand = class(PdCommand)
  public
  oldScale_PixelsPerMm, newScale_pixelsPerMm: single;
  oldOffset_mm, newOffset_mm: SinglePoint;
	procedure doCommand; override;
	procedure undoCommand; override;
	procedure redoCommand; override;
  function description: string; override;
  end;

PdChangeMainWindowOrientationCommand = class(PdCommand)
  public
  oldScale_PixelsPerMm, newScale_pixelsPerMm: single;
  oldOffset_mm, newOffset_mm: SinglePoint;
  oldWindowOrientation, newWindowOrientation: smallint;
  constructor createWithNewOrientation(aNewOrientation: smallint);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

{ ------------------------------------------------------------------ commands that affect only the domain }
PdChangeDomainOptionsCommand = class(PdCommand)
  public
  oldOptions, newOptions: DomainOptionsStructure;
  constructor createWithOptions(aNewOptions: DomainOptionsStructure);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdChangeDomain3DOptionsCommand = class(PdCommand)
  public
  outputType: smallint;
  oldOptions, newOptions: FileExport3DOptionsStructure;
  constructor createWithOptionsAndType(aNewOptions: FileExport3DOptionsStructure; anOutputType: smallint);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

{ ------------------------------------------------------------------- commands that affect one plant only }
PdRenameCommand = class(PdCommand)
  public
  plant: PdPlant;
  oldName, newName: string;
  constructor createWithPlantAndNewName(aPlant: PdPlant; aNewName: string);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdEditNoteCommand = class(PdCommand)
  public
  plant: PdPlant;
  oldStrings, newStrings: TStringList;
  constructor createWithPlantAndNewTStrings(aPlant: PdPlant; aNewStrings: TStrings);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdNewCommand = class(PdCommand)
  public
  newPlant: PdPlant;
  useWizardPlant: boolean;
  wizardPlant: PdPlant;
  oldSelectedList: TList;  // v2.0
  constructor createWithWizardPlantAndOldSelectedList(aPlant: PdPlant; anOldSelectedList: TList);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
	procedure redoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

PdSendBackwardOrForwardCommand = class(PdCommand)
  public
  backward: boolean;
  constructor createWithBackwardOrForward(aBackward: boolean);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdCreateAmendmentCommand = class(PdCommand)
  public
  plant: PdPlant;
  newAmendment: PdPlantDrawingAmendment;
  constructor createWithPlantAndAmendment(aPlant: PdPlant; aNewAmendment: PdPlantDrawingAmendment);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdDeleteAmendmentCommand = class(PdCommand)
  public
  plant: PdPlant;
  amendment: PdPlantDrawingAmendment;
  constructor createWithPlantAndAmendment(aPlant: PdPlant; anAmendment: PdPlantDrawingAmendment);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdEditAmendmentCommand = class(PdCommand)
  public
  plant: PdPlant;
  field: string;
  oldAmendment, newAmendment: PdPlantDrawingAmendment;
  constructor createWithPlantAndAmendmentAndField(aPlant: PdPlant; aNewAmendment: PdPlantDrawingAmendment; aField: string);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdSelectPosingPartCommand = class(PdCommand)
  public
  plant: PdPlant;
  newPartID, oldPartID: longint;
  oldPartType, newPartType: string;
  constructor createWithPlantAndPartIDsAndTypes(aPlant: PdPlant; aNewPartID, anOldPartID: longint;
      aNewPartType, anOldPartType: string);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

{ ---------------------------------- commands that affect a list of plants, usually in a minor way }
PdCommandWithListOfPlants = class(PdCommand)
  public
  plantList: TList;
  values: TListCollection;
  plant: PdPlant; {for temporary use}
  removesPlantAmendments: boolean;
  listOfAmendmentLists: TList;
  constructor createWithListOfPlants(aList: TList); virtual;
  destructor destroy; override;
  procedure setUpToRemoveAmendmentsWhenDone;
	procedure doCommand; override;
	procedure undoCommand; override;
  procedure invalidateCombinedPlantRects; virtual;
  end;

PdChangeSelectedPlantsCommand = class(PdCommandWithListOfPlants)
  public
  newList: TList;
  constructor createWithOldListOFPlantsAndNewList(aList: TList; aNewList: TList);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdSelectOrDeselectAllCommand = class(PdCommandWithListOfPlants)
  public
  deselect: boolean;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdResizePlantsCommand = class(PdCommandWithListOfPlants)
  public
  initialized, doneInMouseCommand: boolean;
  newValues, oldSizes, aspectRatios: TListCollection;
  dragStartPoint, offset: TPoint;
  multiplier, newValue: single;
  constructor createWithListOfPlants(aList: TList); override;
  constructor createWithListOfPlantsAndMultiplier(aList: TList; aMultiplier: single);
  constructor createWithListOfPlantsAndNewValue(aList: TList; aNewValue: single);
  destructor destroy; override;
  procedure saveInitialValues;
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  procedure redoCommand; override;
  function description: string; override;
  end;

PdResizePlantsToSameWidthOrHeightCommand = class(PdCommandWithListOfPlants)
  public
  newValues, oldSizes: TListCollection;
  newWidth, newHeight: single;
  changeWidth: boolean;
  constructor createWithListOfPlantsAndNewWidthOrHeight(aList: TList; aNewWidth, aNewHeight: single; aChangeWidth: boolean);
  destructor destroy; override;
  procedure saveInitialValues;
	procedure doCommand; override;
	procedure undoCommand; override;
  procedure redoCommand; override;
  function description: string; override;
  end;

PdPackPlantsCommand = class(PdCommandWithListOfPlants)
  public
  newScales, oldSizes, newPoints, oldPoints: TListCollection;
  focusRect: TRect;
  constructor createWithListOfPlantsAndFocusRect(aList: TList; aFocusRect: TRect);
  destructor destroy; override;
  procedure saveInitialValues;
	procedure doCommand; override;
	procedure undoCommand; override;
  procedure redoCommand; override;
  function description: string; override;
  end;

PdChangeMainWindowViewingOptionCommand = class(PdCommandWithListOfPlants)
  public
  selectedList: TList;
  oldScale_PixelsPerMm, newScale_pixelsPerMm: single;
  oldOffset_mm, newOffset_mm: SinglePoint;
  oldMainWindowViewingOption: smallint;
  newMainWindowViewingOption: smallint;
  constructor createWithListOfPlantsAndSelectedPlantsAndNewOption(aList: TList; aSelectedList: TList; aNewOption: smallint);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdDragCommand = class(PdCommandWithListOfPlants)
  public
  initialized, doneInMouseCommand, dragAllPlantsToOnePoint: boolean;
  dragStartPoint, offset, newPoint: TPoint;
  constructor createWithListOfPlantsAndDragOffset(aList: TList; anOffset: TPoint);
  constructor createWithListOfPlantsAndNewPoint(aList: TList; aNewPoint: TPoint);
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand; override;
	procedure doCommand; override;
	procedure redoCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdAlignPlantsCommand = class(PdCommandWithListOfPlants)
  public
  newPoints: TListCollection;
  focusRect: TRect;
  alignDirection: smallint;
  constructor createWithListOfPlantsRectAndDirection(aList: TList; aRect: TRect; aDirection: smallint);
  destructor destroy; override;
	procedure doCommand; override;
	procedure redoCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdRotateCommand = class(PdCommandWithListOfPlants)
  public
  rotateDirection: smallint;
  newRotation, offsetRotation: single;
  startDragPoint: TPoint;
  constructor createWithListOfPlantsDirectionAndNewRotation(aList: TList;
    aRotateDirection, aNewRotation: smallint);
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdResetRotationsCommand = class(PdCommandWithListOfPlants)
  public
  oldX, oldY, oldZ: single;
  procedure doCommand; override;
	procedure redoCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdChangeDrawingScaleCommand = class(PdCommandWithListOfPlants)
  public
  newScale: single;
  constructor createWithListOfPlantsAndNewScale(aList: TList; aNewScale: single);
  procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdChangePlantAgeCommand = class(PdCommandWithListOfPlants)
  public
  newAge: smallint;
  constructor createWithListOfPlantsAndNewAge(aList: TList; aNewAge: smallint);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdAnimatePlantCommand = class(PdCommandWithListOfPlants)
  public
  age, oldestAgeAtMaturity: smallint;
  constructor createWithListOfPlants(aList: TList); override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  procedure animateOneDay;
  end;

PdHideOrShowCommand = class(PdCommandWithListOfPlants)
  public
  hide: boolean;
  newValues: TListCollection;
  constructor createWithListOfPlantsAndHideOrShow(aList: TList; aHide: boolean);
  constructor createWithListOfPlantsAndListOfHides(aList: TList; aHideList: TListCollection);
  destructor destroy; override;
  procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdRandomizeCommand = class(PdCommandWithListOfPlants)
  public
  oldSeeds, oldBreedingSeeds, newSeeds, newBreedingSeeds, oldXRotations, newXRotations: TListCollection;
  isInBreeder, isRandomizeAllInBreeder: boolean;
  constructor createWithListOfPlants(aList: TList); override;
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
	procedure redoCommand; override;
  function description: string; override;
  end;

{ -------------------------------------------------------------- commands that add plants, no special superclass }
PdPasteCommand = class(PdCommandWithListOfPlants)
  public
  { doesn't use values, but uses plantList }
  useSpecialPastePosition: boolean;
  oldSelectedList: TList; // v2.0
  constructor createWithListOfPlantsAndOldSelectedList(aList, anOldSelectedList: TList);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

PdDuplicateCommand = class(PdCommandWithListOfPlants)
  public
  startDragPoint, offset: TPoint;
  newPlants: TList;
  inTrackMouse: boolean;
  constructor createWithListOfPlants(aList: TList); override;
  destructor destroy; override;
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand; override;
	procedure doCommand; override;
	procedure undoCommand; override;
	procedure redoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

{ -------------------------------------------------------------------------------- remove command is unique }
PdRemoveCommand = class(PdCommandWithListOfPlants) 
  public
  { doesn't use values, but uses plantList }
  removedPlants: TList;
  copyToClipboard: boolean;
  constructor createWithListOfPlantsAndClipboardFlag(aList: TList; aCopyToClipboard: boolean);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

{ ---------------------------------------------------------------------------------- domain change commands }
PdChangeValueCommand = class(PdCommandWithListOfPlants)
  public
  fieldNumber: smallint;
  regrow: boolean;
  constructor createCommandWithListOfPlants(aList: TList; aFieldNumber: smallint; aRegrow: boolean);
  function description: string; override;
  end;

PdChangeRealValueCommand = class(PdChangeValueCommand)
  public
  newValue: single;
  arrayIndex: smallint;
  constructor createCommandWithListOfPlants(aList: TList; aNewValue: single;
    aFieldNumber, anArrayIndex: smallint; aRegrow: boolean);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdChangeSCurvePointValueCommand = class(PdChangeValueCommand)
  public
  newX, newY: single;
  pointIndex: smallint;
  constructor createCommandWithListOfPlants(aList: TList; aNewX, aNewY: single;
    aFieldNumber, aPointIndex: smallint; aRegrow: boolean);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdChangeColorValueCommand = class(PdChangeValueCommand)
  public
  newColor: TColorRef;
  constructor createCommandWithListOfPlants(aList: TList; aNewValue: TColorRef;
    aFieldNumber, anArrayIndex: smallint; aRegrow: boolean);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdChangeTdoValueCommand = class(PdChangeValueCommand)
  public
  newTdo: KfObject3D;
  constructor createCommandWithListOfPlants(aList: TList; aNewValue: KfObject3D;
    aFieldNumber: smallint; aRegrow: boolean);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdChangeSmallintValueCommand = class(PdChangeValueCommand)
  public
  newValue, arrayIndex: smallint;
  constructor createCommandWithListOfPlants(aList: TList; aNewValue: smallint;
    aFieldNumber, anArrayIndex: smallint; aRegrow: boolean);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdChangeBooleanValueCommand = class(PdChangeValueCommand)
  public
  newValue: boolean;
  arrayIndex: smallint;
  constructor createCommandWithListOfPlants(aList: TList; aNewValue: boolean;
    aFieldNumber, anArrayIndex: smallint; aRegrow: boolean);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

{ ---------------------------------------------------------------------------- breeder commands }
PdBreedFromParentsCommand = class(PdCommand)
  public
  firstParent, secondParent: PdPlant;
  fractionOfMaxAge: single;
  row: smallint;
  oldGenerations: TList;
  newGeneration, firstGeneration: PdGeneration;
  createFirstGeneration: boolean;
  rowSelectedAtStart: smallint;
  constructor createWithInfo(existingGenerations: TListCollection;
    aFirstParent, aSecondParent: PdPlant; aRow: smallint; aFractionOfMaxAge: single; aCreateFirstGeneration: boolean);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
	procedure redoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

PdReplaceBreederPlant = class(PdCommand)
  public
  originalPlant, newPlant, plantDraggedFrom: PdPlant;
  row, column: smallint;
  constructor createWithPlantRowAndColumn(aPlant: PdPlant; aRow, aColumn: smallint);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
	procedure redoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

PdMakeTimeSeriesCommand = class(PdCommand)
  public
  oldPlants, newPlants: TList;
  newPlant: PdPlant;
  isPaste: boolean;
  constructor createWithNewPlant(aNewPlant: PdPlant);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
	procedure redoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

PdChangeBreedingAndTimeSeriesOptionsCommand = class(PdCommand)
  public
  oldOptions, newOptions: BreedingAndTimeSeriesOptionsStructure;
  oldDomainOptions, newDomainOptions: DomainOptionsStructure;
  constructor createWithOptionsAndDomainOptions(anOptions: BreedingAndTimeSeriesOptionsStructure;
    aDomainOptions: DomainOptionsStructure);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdDeleteBreederGenerationCommand = class(PdCommand)
  public
  generation: PdGeneration;
  row: smallint;
  constructor createWithGeneration(aGeneration: PdGeneration);
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

PdDeleteAllBreederGenerationsCommand = class(PdCommand)
  public
  generations: TListCollection;
  constructor create;
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

{ ------------------------------------------------------------------------ time series }
PdChangeNumberOfTimeSeriesStagesCommand = class(PdCommand)
  public
  newNumber, oldNumber: smallint;
  constructor createWithNewNumberOfStages(aNumber: smallint);
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  end;

PdDeleteTimeSeriesCommand = class(PdCommand)
  public
  plants: TListCollection;
  constructor create;
  destructor destroy; override;
	procedure doCommand; override;
	procedure undoCommand; override;
  function description: string; override;
  function numberOfStoredLargeObjects: longint; override;
  end;

implementation

uses uplantmn, umain, ubreedr, ucursor, umath, utimeser;

{ ------------------------------------------------------------------------ local functions }
function plantNamesForDescription(aList: TList): string;
  var
    firstPlant: PdPlant;
	begin
  result := '';
  if (aList = nil) or (aList.count <= 0) then exit;
  firstPlant := PdPlant(aList.items[0]);
  if firstPlant <> nil then
    begin
    result := ' plant "' + firstPlant.getName + '"';
    if aList.count > 1 then
      result := result + ', others';
    end;
  end;

{ ------------------------------------------------------------------------ value objects }
constructor PdBooleanValue.createWithBoolean(aBoolean: boolean);
  begin
  saveBoolean := aBoolean;
  end;

constructor PdPointValue.createWithPoint(aPoint: TPoint);
  begin
  savePoint := aPoint;
  end;

constructor PdSingleValue.createWithSingle(aSingle: single);
  begin
  saveSingle := aSingle;
  end;

constructor PdSinglePointValue.createWithSingleXY(anX, aY: single);
  begin
  x := anX;
  y := aY;
  end;

constructor PdXYZValue.createWithXYZ(anX, aY, aZ: single);
  begin
  x := anX;
  y := aY;
  z := aZ;
  end;

constructor PdSmallintValue.createWithSmallint(aSmallint: smallint);
  begin
  saveSmallint := aSmallint;
  end;

constructor PdLongintValue.createWithLongint(aLongint: longint);
  begin
  saveLongint := aLongint;
  end;

constructor PdColorValue.createWithColor(aColor: TColorRef);
  begin
  saveColor := aColor;
  end;

{ -------------------------------------------------------- PdChangeDomainOptionsCommand }
constructor PdChangeDomainOptionsCommand.createWithOptions(aNewOptions: DomainOptionsStructure);
  begin
  inherited create;
  commandChangesPlantFile := false;
  newOptions := aNewOptions;
  oldOptions := domain.options;
  end;

procedure PdChangeDomainOptionsCommand.doCommand;
  begin
  inherited doCommand;
  domain.options := newOptions;
  MainForm.updateForChangeToDomainOptions;
  end;

procedure PdChangeDomainOptionsCommand.undoCommand;
  begin
  inherited undoCommand;
  domain.options := oldOptions;
  MainForm.updateForChangeToDomainOptions;
  end;

function PdChangeDomainOptionsCommand.description: string;
	begin
  result := 'change preferences';
  end;

{ -------------------------------------------------------- PdChangeDomain3DOptionsCommand }
constructor PdChangeDomain3DOptionsCommand.createWithOptionsAndType(aNewOptions: FileExport3DOptionsStructure;
    anOutputType: smallint);
  begin
  inherited create;
  outputType := anOutputType;
  commandChangesPlantFile := false;
  newOptions := aNewOptions;
  oldOptions := domain.exportOptionsFor3D[outputType];
  end;

procedure PdChangeDomain3DOptionsCommand.doCommand;
  begin
  inherited doCommand;
  domain.exportOptionsFor3D[outputType] := newOptions;
  end;

procedure PdChangeDomain3DOptionsCommand.undoCommand;
  begin
  inherited undoCommand;
  domain.exportOptionsFor3D[outputType] := oldOptions;
  end;

function PdChangeDomain3DOptionsCommand.description: string;
	begin
  result := 'change ' + nameStringForFileType(fileTypeFor3DExportType(outputType)) + ' output options';
  end;

{ ------------------------------------------------------------ PdCommandWithListOfPlants }
constructor PdCommandWithListOfPlants.createWithListOfPlants(aList: TList);
  var
    i: smallint;
  begin
  inherited create;
  plantList := TList.create;
  if aList.count > 0 then for i := 0 to aList.count - 1 do
    plantList.add(aList.items[i]);
  values := TListCollection.create;
  listOfAmendmentLists := nil;
  end;

procedure PdCommandWithListOfPlants.setUpToRemoveAmendmentsWhenDone;
  var
    i, j: integer;
    plant: PdPlant;
    aList: TList;
  begin
  // call this method after create method if the command should remove amendments
  removesPlantAmendments := true;
  listOfAmendmentLists := TList.create;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    aList := TList.create;
    if plant.amendments.count > 0 then for j := 0 to plant.amendments.count - 1 do
      aList.add(PdPlantDrawingAmendment(plant.amendments.items[j]));
    listOfAmendmentLists.add(aList);
    end;
  end;

destructor PdCommandWithListOfPlants.destroy;
  var
    i, j: integer;
    amendment: PdPlantDrawingAmendment;
    aList: TList;
  begin
  plantList.free;
  plantList := nil;
  values.free;
  values := nil;
  if (self.done) and (self.removesPlantAmendments) then
    if (listOfAmendmentLists <> nil) and (listOfAmendmentLists.count > 0) then
    for i := 0 to listOfAmendmentLists.count - 1 do
      begin
      aList := TList(listOfAmendmentLists.items[i]);
      if aList.count > 0 then for j := 0 to aList.count - 1 do
        begin
        amendment := PdPlantDrawingAmendment(aList.items[j]);
        amendment.free;
        end;
      aList.free;
      end;
  listOfAmendmentLists.free;
  listOfAmendmentLists := nil;
  inherited destroy;
  end;

procedure PdCommandWithListOfPlants.doCommand;
  var
    i: integer;
    atLeastOnePlantHadAmendments: boolean;
    aList: TList;
  begin
  inherited doCommand;
  if not removesPlantAmendments then exit;
  atLeastOnePlantHadAmendments := false;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    aList := TList(listOfAmendmentLists.items[i]);
    if aList.count > 0 then
      begin
      atLeastOnePlantHadAmendments := true;
      PdPlant(plantList.items[i]).clearPointersToAllAmendments;
      end;
    end;
  if atLeastOnePlantHadAmendments then
    MainForm.updatePosingForFirstSelectedPlant;
  end;

procedure PdCommandWithListOfPlants.undoCommand;
  var
    i: integer;
    atLeastOnePlantHadAmendments: boolean;
    aList: TList;
  begin
  inherited undoCommand;
  if not removesPlantAmendments then exit;
  atLeastOnePlantHadAmendments := false;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    aList := TList(listOfAmendmentLists.items[i]);
    if aList.count > 0 then
      begin
      atLeastOnePlantHadAmendments := true;
      PdPlant(plantList.items[i]).restoreAmendmentPointersToList(aList);
      end;
    end;
  if atLeastOnePlantHadAmendments then
    MainForm.updatePosingForFirstSelectedPlant;
  end;

procedure PdCommandWithListOfPlants.invalidateCombinedPlantRects;
  var
    redrawRect: TRect;
    i: smallint;
  begin
  redrawRect := bounds(0,0,0,0);
  if plantList.count > 0 then
    for i := 0 to plantList.count - 1 do
      unionRect(redrawRect, redrawRect, PdPlant(plantList.items[i]).boundsRect_pixels);
  MainForm.invalidateDrawingRect(redrawRect);
  end;

{ ------------------------------------------------------------ PdDragCommand }
constructor PdDragCommand.createWithListOfPlantsAndDragOffset(aList: TList; anOffset: TPoint);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    values.add(PdPointValue.createWithPoint(plant.basePoint_pixels));
    end;
  offset := anOffset;
  initialized := true;
  end;

constructor PdDragCommand.createWithListOfPlantsAndNewPoint(aList: TList; aNewPoint: TPoint);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  dragAllPlantsToOnePoint := true;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    values.add(PdPointValue.createWithPoint(plant.basePoint_pixels));
    end;
  newPoint := aNewPoint;
  initialized := true;
  end;

function PdDragCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand;
  var
    i: smallint;
  begin
  result := self;
  if aTrackPhase = trackPress then
  	begin
    dragStartPoint := nextPoint;
    end
  else if aTrackPhase = trackMove then
  	begin
    if (not initialized) and mouseDidMove then
      begin
      if plantList.count > 0 then for i := 0 to plantList.count - 1 do
        begin
        plant := PdPlant(plantList.items[i]);
        values.add(PdPointValue.createWithPoint(plant.basePoint_pixels));
        end;
      initialized := true;
      inherited doCommand;
      end;
    if initialized then
      begin
      offset.x := nextPoint.x - dragStartPoint.x;
      offset.y := nextPoint.y - dragStartPoint.y;
      self.invalidateCombinedPlantRects;
      if plantList.count > 0 then for i := 0 to plantList.count - 1 do
        begin
        plant := PdPlant(plantList.items[i]);
        plant.moveTo(PdPointValue(values.items[i]).savePoint);
        plant.moveBy(offset);
        if domain.options.cachePlantBitmaps then
          plant.recalculateBoundsForOffsetChange;
        end;
      MainForm.updateForChangeToSelectedPlantsLocation;
      self.invalidateCombinedPlantRects;
      doneInMouseCommand := true;
      end;
  	end
  else if aTrackPhase = trackRelease then
  	begin
    if not mouseDidMove then
      begin
      result := nil;
      self.free;
      end;
  	end;
	end;

procedure PdDragCommand.doCommand;
  var
    i: smallint;
  begin
  if doneInMouseCommand then exit; {only used if not done by mouse command-otherwise done in trackMouse}
  inherited doCommand;
  self.invalidateCombinedPlantRects;
  if dragAllPlantsToOnePoint then
    begin
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.moveTo(newPoint);
      if domain.options.cachePlantBitmaps then
        plant.recalculateBoundsForOffsetChange;
      end
    end
  else
    begin
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.moveBy(offset);
      if domain.options.cachePlantBitmaps then
        plant.recalculateBoundsForOffsetChange;
      end
    end;
  MainForm.updateForChangeToSelectedPlantsLocation;
  self.invalidateCombinedPlantRects;
  end;

procedure PdDragCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.moveTo(PdPointValue(values.items[i]).savePoint);
    if domain.options.cachePlantBitmaps then
      plant.recalculateBoundsForOffsetChange;
    end;
  MainForm.updateForChangeToSelectedPlantsLocation;
  self.invalidateCombinedPlantRects;
  end;

procedure PdDragCommand.redoCommand;
  var
    i: smallint;
  begin
  if not initialized then exit;
  inherited doCommand;
  self.invalidateCombinedPlantRects;
  if dragAllPlantsToOnePoint then
    begin
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.moveTo(newPoint);
      if domain.options.cachePlantBitmaps then
        plant.recalculateBoundsForOffsetChange;
      end
    end
  else
    begin
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.moveBy(offset);
      if domain.options.cachePlantBitmaps then
        plant.recalculateBoundsForOffsetChange;
      end
    end;
  MainForm.updateForChangeToSelectedPlantsLocation;
  self.invalidateCombinedPlantRects;
  end;

function PdDragCommand.description: string;
	begin
  if dragAllPlantsToOnePoint then
    result := 'make bouquet'
  else
    result := 'drag' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdAlignPlantsCommand }
constructor PdAlignPlantsCommand.createWithListOfPlantsRectAndDirection(aList: TList;
    aRect: TRect; aDirection: smallint);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    values.add(PdPointValue.createWithPoint(plant.basePoint_pixels));
    end;
  newPoints := TListCollection.create;
  focusRect := aRect;
  alignDirection := aDirection;
  end;

destructor PdAlignPlantsCommand.destroy;
  begin
  newPoints.free;
  newPoints := nil;
  inherited destroy;
  end;

const kGapBetweenArrangedPlants = 5;

procedure PdAlignPlantsCommand.doCommand;
  var
    i: smallint;
    newPoint, offset: TPoint;
  begin
  inherited doCommand;
  newPoints.clear;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    newPoint := plant.basePoint_pixels;
    offset.x := plant.basePoint_pixels.x - plant.boundsRect_pixels.left;
    offset.y := plant.basePoint_pixels.y - plant.boundsRect_pixels.top;
    case alignDirection of
      kUp: newPoint.y := focusRect.top + offset.y;
      kDown: newPoint.y := focusRect.bottom - (rHeight(plant.boundsRect_pixels) - offset.y);
      kLeft: newPoint.x := focusRect.left + offset.x;
      kRight: newPoint.x := focusRect.right - (rWidth(plant.boundsRect_pixels) - offset.x);
      end;
    plant.moveTo(newPoint);
    newPoints.add(PdPointValue.createWithPoint(plant.basePoint_pixels));
    if domain.options.cachePlantBitmaps then
      plant.recalculateBoundsForOffsetChange;
    end;
  MainForm.updateForChangeToSelectedPlantsLocation;
  self.invalidateCombinedPlantRects;
  end;

procedure PdAlignPlantsCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.moveTo(PdPointValue(values.items[i]).savePoint);
    if domain.options.cachePlantBitmaps then
      plant.recalculateBoundsForOffsetChange;
    end;
  MainForm.updateForChangeToSelectedPlantsLocation;
  self.invalidateCombinedPlantRects;
  end;

procedure PdAlignPlantsCommand.redoCommand;
  var
    i: smallint;
  begin
  inherited doCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.moveTo(PdPointValue(newPoints.items[i]).savePoint);
    if domain.options.cachePlantBitmaps then
      plant.recalculateBoundsForOffsetChange;
    end;
  MainForm.updateForChangeToSelectedPlantsLocation;
  self.invalidateCombinedPlantRects;
  end;

function PdAlignPlantsCommand.description: string;
	begin
  result := 'align' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdResizePlantsCommand }
constructor PdResizePlantsCommand.createWithListOfPlants(aList: TList);
  begin
  inherited createWithListOfPlants(aList);
  newValues := TListCollection.create;
  oldSizes := TListCollection.create;
  aspectRatios := TListCollection.create;
  end;

constructor PdResizePlantsCommand.createWithListOfPlantsAndMultiplier(aList: TList; aMultiplier: single);
  begin
  self.createWithListOfPlants(aList);
  self.saveInitialValues;
  multiplier := aMultiplier;
  end;

constructor PdResizePlantsCommand.createWithListOfPlantsAndNewValue(aList: TList; aNewValue: single);
  begin
  self.createWithListOfPlants(aList);
  self.saveInitialValues;
  newValue := aNewValue;
  end;

procedure PdResizePlantsCommand.saveInitialValues;
  var
    i: smallint;
    aspectRatio: single;
  begin
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    if rHeight(plant.boundsRect_pixels) <> 0 then
      aspectRatio := 1.0 * rWidth(plant.boundsRect_pixels) / rHeight(plant.boundsRect_pixels)
    else
      aspectRatio := 1.0;
    aspectRatios.add(PdSingleValue.createWithSingle(aspectRatio));
    values.add(PdSingleValue.createWithSingle(plant.drawingScale_pixelsPerMm));
    oldSizes.add(PdPointValue.createWithPoint(
        Point(rWidth(plant.boundsRect_pixels), rHeight(plant.boundsRect_pixels))));
    end;
  end;

destructor PdResizePlantsCommand.destroy;
  begin
  newValues.free;
  newValues := nil;
  oldSizes.free;
  oldSizes := nil;
  aspectRatios.free;
  aspectRatios := nil;
  inherited destroy;
  end;

function PdResizePlantsCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand;
  begin
  result := self;
  if aTrackPhase = trackPress then
  	begin
      dragStartPoint := nextPoint;
    end
  else if (aTrackPhase = trackMove) and (mouseDidMove) then
  	begin
    if not initialized then
      begin
      self.saveInitialValues;
      initialized := true;
      doneInMouseCommand := true;
      offset := Point(0, 0);
      inherited doCommand;
      exit;
      end;
    if initialized then
      begin
      offset.x := nextPoint.x - dragStartPoint.x;
      offset.y := nextPoint.y - dragStartPoint.y;
      self.doCommand;
      end;
  	end
  else if aTrackPhase = trackRelease then
  	begin
    if (not mouseDidMove) or (not initialized) then
      begin
      result := nil;
      self.free;
      end;
  	end;
	end;

procedure PdResizePlantsCommand.doCommand;
  var
    i: smallint;
    newSize, oldSize: TPoint;
    aspectRatio, oldScale: single;
  begin
  if not doneInMouseCommand then
    inherited doCommand;
  if plantList.count <= 0 then exit;
  if (offset.x = 0) and (offset.y = 0) and (multiplier = 0) and (newValue = 0) then exit;
  try
  if not doneInMouseCommand then
    cursor_startWait;
  self.invalidateCombinedPlantRects;
  newValues.clear;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    if multiplier <> 0 then
      begin
      plant.drawingScale_pixelsPerMm := plant.drawingScale_pixelsPerMm * multiplier;
      end
    else if newValue <> 0 then
      begin
      plant.drawingScale_pixelsPerMm := newValue;
      end
    else
      begin
      oldSize := PdPointValue(oldSizes.items[i]).savePoint;
      aspectRatio := PdSingleValue(aspectRatios.items[i]).saveSingle;
      oldScale := PdSingleValue(values.items[i]).saveSingle;
      newSize.y := intMax(10, oldSize.y - offset.y); // 10 pixels is arbitrary minimum
      newSize.x := round(newSize.y * aspectRatio);
      plant.calculateDrawingScaleToFitSize(newSize);
      // this is to counteract a bug that when you resize down, it resizes up the first mouse move, then down
      // can't figure out why, just putting in this ugly fix to stop it from doing that
      if (plant.drawingScale_pixelsPerMm > oldScale) and (offset.y > 0) then
        plant.drawingScale_pixelsPerMm := oldScale;
      end;
    newValues.add(PdSingleValue.createWithSingle(plant.drawingScale_pixelsPerMm));
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  finally
  if not doneInMouseCommand then
    cursor_stopWait;
  end;
  end;

procedure PdResizePlantsCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  try
    cursor_startWait;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.drawingScale_pixelsPerMm := PdSingleValue(values.items[i]).saveSingle;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdResizePlantsCommand.redoCommand;
  var
    i: smallint;
  begin
  if not initialized then exit;
  inherited undoCommand;
  try
    cursor_startWait;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.drawingScale_pixelsPerMm := PdSingleValue(newValues.items[i]).saveSingle;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  finally
    cursor_stopWait;
  end;
  end;

function PdResizePlantsCommand.description: string;
	begin
  result := 'resize' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdResizePlantsToSameWidthOrHeightCommand }
constructor PdResizePlantsToSameWidthOrHeightCommand.createWithListOfPlantsAndNewWidthOrHeight(
    aList: TList; aNewWidth, aNewHeight: single; aChangeWidth: boolean);
  begin
  inherited createWithListOfPlants(aList);
  newValues := TListCollection.create;
  oldSizes := TListCollection.create;
  self.saveInitialValues;
  newWidth := aNewWidth;
  newHeight := aNewHeight;
  changeWidth := aChangeWidth;
  end;

procedure PdResizePlantsToSameWidthOrHeightCommand.saveInitialValues;
  var
    i: smallint;
  begin
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    values.add(PdSingleValue.createWithSingle(plant.drawingScale_pixelsPerMm));
    oldSizes.add(PdPointValue.createWithPoint(
        Point(rWidth(plant.boundsRect_pixels), rHeight(plant.boundsRect_pixels))));
    end;
  end;

destructor PdResizePlantsToSameWidthOrHeightCommand.destroy;
  begin
  newValues.free;
  newValues := nil;
  oldSizes.free;
  oldSizes := nil;
  inherited destroy;
  end;

procedure PdResizePlantsToSameWidthOrHeightCommand.doCommand;
  var
    i: smallint;
    newScaleX, newScaleY: single;
  begin
  inherited doCommand;
  if plantList.count <= 0 then exit;
  try
    cursor_startWait;
  self.invalidateCombinedPlantRects;
  newValues.clear;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.recalculateBounds(kDontDrawYet);
    if changeWidth then
      plant.drawingScale_PixelsPerMm := safedivExcept(plant.drawingScale_PixelsPerMm * newWidth,
          rWidth(plant.boundsRect_pixels), 0.1)
    else
      plant.drawingScale_PixelsPerMm := safedivExcept(plant.drawingScale_PixelsPerMm * newHeight,
          rHeight(plant.boundsRect_pixels), 0.1);
    newValues.add(PdSingleValue.createWithSingle(plant.drawingScale_pixelsPerMm));
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdResizePlantsToSameWidthOrHeightCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.drawingScale_pixelsPerMm := PdSingleValue(values.items[i]).saveSingle;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  end;

procedure PdResizePlantsToSameWidthOrHeightCommand.redoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.drawingScale_pixelsPerMm := PdSingleValue(newValues.items[i]).saveSingle;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  end;

function PdResizePlantsToSameWidthOrHeightCommand.description: string;
	begin
  result := 'scale' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdPackPlantsCommand }
constructor PdPackPlantsCommand.createWithListOfPlantsAndFocusRect(aList: TList; aFocusRect: TRect);
  begin
  inherited createWithListOfPlants(aList);
  newScales := TListCollection.create;
  oldSizes := TListCollection.create;
  newPoints := TListCollection.create;
  oldPoints := TListCollection.create;
  self.saveInitialValues;
  focusRect := aFocusRect;
  end;

procedure PdPackPlantsCommand.saveInitialValues;
  var
    i: smallint;
  begin
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    values.add(PdSingleValue.createWithSingle(plant.drawingScale_pixelsPerMm));
    oldPoints.add(PdPointValue.createWithPoint(plant.basePoint_pixels));
    oldSizes.add(PdPointValue.createWithPoint(
        Point(rWidth(plant.boundsRect_pixels), rHeight(plant.boundsRect_pixels))));
    end;
  end;

destructor PdPackPlantsCommand.destroy;
  begin
  newScales.free;
  newScales := nil;
  oldSizes.free;
  oldSizes := nil;
  newPoints.free;
  newPoints := nil;
  oldPoints.free;
  oldPoints := nil;
  inherited destroy;
  end;

procedure PdPackPlantsCommand.doCommand;
  var
    i: smallint;
    newScaleX, newScaleY: single;
    widestBox, tallestBox, tallestHeight: integer;
    offset, newPoint: TPoint;
    lastPlant: PdPlant;
    totalHeight, averageHeight, remainingX: integer;
    plantScaleChanged: boolean;
    newScale: single;
  begin
  inherited doCommand;
  if plantList.count <= 0 then exit;
  self.invalidateCombinedPlantRects;
  newScales.clear;
  newPoints.clear;
  lastPlant := nil;
  totalHeight := 0;
  tallestHeight := 0;
  try
    cursor_startWait;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    totalHeight := totalHeight + rHeight(plant.boundsRect_pixels);
    end;
    averageHeight := totalHeight div plantList.count;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.recalculateBounds(kDontDrawYet);
    plantScaleChanged := false;
    // calculate new scale (resize based on average height)
    newScale := safedivExcept(plant.drawingScale_PixelsPerMm * averageHeight,
          rHeight(plant.boundsRect_pixels) * 1.0, 0.1);
    // don't rescale and redraw plant if scale hardly changes
    if abs(newScale - plant.drawingScale_PixelsPerMm) > plant.drawingScale_PixelsPerMm / 20.0 then
      begin
      plantScaleChanged := true;
      plant.drawingScale_PixelsPerMm := newScale;
      plant.recalculateBounds(kDontDrawYet);
      end;
    newScales.add(PdSingleValue.createWithSingle(plant.drawingScale_pixelsPerMm));
    // calculate new position
    offset.x := plant.basePoint_pixels.x - plant.boundsRect_pixels.left;
    offset.y := plant.basePoint_pixels.y - plant.boundsRect_pixels.top;
    remainingX := rWidth(plant.boundsRect_pixels) - offset.x;
    if (i <= 0) or (lastPlant = nil) then
      begin
      newPoint.x := offset.x + kGapBetweenArrangedPlants;
      newPoint.y := offset.y + kGapBetweenArrangedPlants;
      end
    else
      begin
      newPoint.x := lastPlant.boundsRect_pixels.right + kGapBetweenArrangedPlants + offset.x;
      newPoint.y := lastPlant.boundsRect_pixels.top + offset.y;
      end;
    if newPoint.x + remainingX > MainForm.drawingPaintBox.width then
      begin
      newPoint.x := offset.x + kGapBetweenArrangedPlants;
      newPoint.y := tallestHeight + kGapBetweenArrangedPlants + offset.y;
      end;
    plant.moveTo(newPoint);
    newPoints.add(PdPointValue.createWithPoint(plant.basePoint_pixels));
    if plantScaleChanged then
      plant.recalculateBounds(kDrawNow)
    else
      plant.recalculateBoundsForOffsetChange;
    lastPlant := plant;
    if plant.boundsRect_pixels.bottom > tallestHeight then
      tallestHeight := plant.boundsRect_pixels.bottom;
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdPackPlantsCommand.undoCommand;
  var
    i: smallint;
    oldScale: single;
  begin
  inherited undoCommand;
  try
    cursor_startWait;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    oldScale := plant.drawingScale_pixelsPerMm;
    plant.drawingScale_pixelsPerMm := PdSingleValue(values.items[i]).saveSingle;
    plant.moveTo(PdPointValue(oldPoints.items[i]).savePoint);
    // don't rescale and redraw plant if scale hardly changes
    if abs(plant.drawingScale_PixelsPerMm - oldScale) > plant.drawingScale_PixelsPerMm / 20.0 then
      plant.recalculateBounds(kDrawNow)
    else
      plant.recalculateBoundsForOffsetChange;
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdPackPlantsCommand.redoCommand;
  var
    i: smallint;
    oldScale: single;
  begin
  inherited undoCommand;
  try
    cursor_startWait;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    oldScale := plant.drawingScale_pixelsPerMm;
    plant.drawingScale_pixelsPerMm := PdSingleValue(newScales.items[i]).saveSingle;
    plant.moveTo(PdPointValue(newPoints.items[i]).savePoint);
    // don't rescale and redraw plant if scale hardly changes
    if abs(plant.drawingScale_PixelsPerMm - oldScale) > plant.drawingScale_PixelsPerMm / 20.0 then
      plant.recalculateBounds(kDrawNow)
    else
      plant.recalculateBoundsForOffsetChange;
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToSelectedPlantsDrawingScale;
  finally
    cursor_stopWait;
  end;
  end;

function PdPackPlantsCommand.description: string;
	begin
  result := 'pack' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdRotateCommand }
constructor PdRotateCommand.createWithListOfPlantsDirectionAndNewRotation(aList: TList;
    aRotateDirection, aNewRotation: smallint);
  var
    i: smallint;
  begin
  { create using this constructor if this is from clicking on a spinEdit }
  inherited createWithListOfPlants(aList);
  rotateDirection := aRotateDirection;
  newRotation := aNewRotation;
  if newRotation < -360 then newRotation := -360;
  if newRotation > 360 then newRotation := 360;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    case rotateDirection of
      kRotateX: values.add(PdSingleValue.createWithSingle(plant.xRotation));
      kRotateY: values.add(PdSingleValue.createWithSingle(plant.yRotation));
      kRotateZ: values.add(PdSingleValue.createWithSingle(plant.zRotation));
      end;
    end;
  end;

function PdRotateCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand;
  var
    i: smallint;
    newRotation: single;
  begin
  result := self;
  { assume that if this function is called, the command was not already initialized
    from clicking on a spinEdit, so we have no values and no rotateDirection }
  if aTrackPhase = trackPress then
    begin
    startDragPoint := nextPoint;
    self.invalidateCombinedPlantRects;
    inherited doCommand;
    end
  else if aTrackPhase = trackMove then
  	begin
    if rotateDirection = kRotateNotInitialized then
      begin
      if rightButtonDown then
        rotateDirection := kRotateZ
      else if abs(nextPoint.x - startDragPoint.x) > abs(nextPoint.y - startDragPoint.y) then
        rotateDirection := kRotateX
      else
        rotateDirection := kRotateY;
      if plantList.count > 0 then for i := 0 to plantList.count - 1 do
        begin
        plant := PdPlant(plantList.items[i]);
        case rotateDirection of
          kRotateX: values.add(PdSingleValue.createWithSingle(plant.xRotation));
          kRotateY: values.add(PdSingleValue.createWithSingle(plant.yRotation));
          kRotateZ: values.add(PdSingleValue.createWithSingle(plant.zRotation));
          end;
        end;
      end;
    self.invalidateCombinedPlantRects;
    case rotateDirection of
      kRotateX: offsetRotation := (nextPoint.x - startDragPoint.x) * 0.5;
      kRotateY: offsetRotation := (nextPoint.y - startDragPoint.y) * 0.5;
      kRotateZ: offsetRotation := (nextPoint.x - startDragPoint.x) * 0.5;
      end;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      newRotation := PdSingleValue(values.items[i]).saveSingle + offsetRotation;
      if newRotation < -360 then newRotation := 360 - (abs(newRotation) - 360);
      if newRotation > 360 then newRotation := -360 + (newRotation - 360);
      case rotateDirection of
        kRotateX: plant.xRotation := newRotation;
        kRotateY: plant.yRotation := newRotation;
        kRotateZ: plant.zRotation := newRotation;
        end;
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
    MainForm.updateForChangeToPlantRotations;
  	end
  else if aTrackPhase = trackRelease then
  	begin
    if not mouseDidMove then
      begin
      // if they just clicked, rotate ten degrees anyway
      self.invalidateCombinedPlantRects;
      if plantList.count > 0 then for i := 0 to plantList.count - 1 do
        begin
        plant := PdPlant(plantList.items[i]);
        values.add(PdSingleValue.createWithSingle(plant.xRotation));
        end;
      rotateDirection := kRotateX;
      // v2.0 if they just clicked with the right mouse button, rotate -10 degrees
      // v2.0 use the domain rotation increment instead of always 10 degrees
      if rightButtonDown then
        offsetRotation := -domain.options.rotationIncrement
      else
        offsetRotation := domain.options.rotationIncrement;
      if plantList.count > 0 then for i := 0 to plantList.count - 1 do
        begin
        plant := PdPlant(plantList.items[i]);
        newRotation := PdSingleValue(values.items[i]).saveSingle + offsetRotation;
        if newRotation < -360 then newRotation := 360 - (abs(newRotation) - 360);
        if newRotation > 360 then newRotation := -360 + (newRotation - 360);
        plant.xRotation := newRotation;
        plant.recalculateBounds(kDrawNow);
        end;
      self.invalidateCombinedPlantRects;
      MainForm.updateForChangeToPlantRotations;
  	  end;
  	end;
	end;

procedure PdRotateCommand.doCommand;
  var
    i: smallint;
  begin
  if self.done then exit; {if done in mousemove }
  inherited doCommand; 
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    case rotateDirection of
      kRotateX:
        if offsetRotation <> 0 then
          plant.xRotation := min(360, max(-360, PdSingleValue(values.items[i]).saveSingle + offsetRotation))
        else
          plant.xRotation := newRotation;
      kRotateY: 
        if offsetRotation <> 0 then
          plant.yRotation := min(360, max(-360, PdSingleValue(values.items[i]).saveSingle + offsetRotation))
        else
          plant.yRotation := newRotation;
      kRotateZ:
        if offsetRotation <> 0 then
          plant.zRotation := min(360, max(-360, PdSingleValue(values.items[i]).saveSingle + offsetRotation))
        else
          plant.zRotation := newRotation;
      end;
    plant.recalculateBounds(kDrawNow);
    end;
  MainForm.updateForChangeToPlantRotations;
  self.invalidateCombinedPlantRects;
  end;

procedure PdRotateCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    case rotateDirection of
      kRotateX: plant.xRotation := PdSingleValue(values.items[i]).saveSingle;
      kRotateY: plant.yRotation := PdSingleValue(values.items[i]).saveSingle;
      kRotateZ: plant.zRotation := PdSingleValue(values.items[i]).saveSingle;
      end;
    plant.recalculateBounds(kDrawNow);
    end;
  MainForm.updateForChangeToPlantRotations;
  self.invalidateCombinedPlantRects;
  end;

function nameForDirection(direction: smallint): string;
  begin
  result := '';
  case direction of
    kRotateX: result := 'X';
    kRotateY: result := 'Y';
    kRotateZ: result := 'Z';
    end;
  end;

function PdRotateCommand.description: string;
	begin
  result := nameForDirection(rotateDirection) + ' rotate' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdResetRotationsCommand }
procedure PdResetRotationsCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; 
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    values.add(PdXYZValue.createWithXYZ(plant.xRotation, plant.yRotation, plant.zRotation));
    plant.xRotation := 0;
    plant.yRotation := 0;
    plant.zRotation := 0;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToPlantRotations;
  end;

procedure PdResetRotationsCommand.redoCommand;
  var
    i: smallint;
  begin
  inherited doCommand; 
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.xRotation := 0;
    plant.yRotation := 0;
    plant.zRotation := 0;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToPlantRotations;
  end;

procedure PdResetRotationsCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.xRotation := PdXYZValue(values.items[i]).x;
    plant.yRotation := PdXYZValue(values.items[i]).y;
    plant.zRotation := PdXYZValue(values.items[i]).z;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  MainForm.updateForChangeToPlantRotations;
  end;

function PdResetRotationsCommand.description: string;
	begin
  result := 'reset rotation for' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdChangeDrawingScaleCommand }
constructor PdChangeDrawingScaleCommand.createWithListOfPlantsAndNewScale(aList: TList; aNewScale: single);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  newScale := aNewScale;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    values.add(PdSingleValue.createWithSingle(PdPlant(plantList.items[i]).drawingScale_PixelsPerMm));
  end;

procedure PdChangeDrawingScaleCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; 
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.drawingScale_PixelsPerMm := newScale;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  end;

procedure PdChangeDrawingScaleCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.drawingScale_PixelsPerMm := PdSingleValue(values.items[i]).saveSingle;
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  end;

function PdChangeDrawingScaleCommand.description: string;
	begin
  result := 'change scale for' + plantNamesForDescription(plantList);

  end;

{ ----------------------------------------------------------------------- PdChangePlantAgeCommand }
constructor PdChangePlantAgeCommand.createWithListOfPlantsAndNewAge(aList: TList; aNewAge: smallint);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  newAge := aNewAge;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    values.add(PdSmallintValue.createWithSmallint(PdPlant(plantList.items[i]).age));
  end;

procedure PdChangePlantAgeCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; 
  try
    cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      { if primary selected plant has longer lifespan than other selected plants, cut off age
        at max for those plants }
      plant.setAge(intMin(newAge, plant.pGeneral.ageAtMaturity));
      plant.recalculateBounds(kDrawNow);
    end;
    self.invalidateCombinedPlantRects;
    MainForm.updateForChangeToSelectedPlantsLocation;
    { changing age causes life cycle panel to need to redraw }
    MainForm.updateLifeCyclePanelForFirstSelectedPlant;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdChangePlantAgeCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  try
    cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.setAge(PdSmallintValue(values.items[i]).saveSmallint);
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
    MainForm.updateForChangeToSelectedPlantsLocation;
    { changing age causes life cycle panel to need to redraw }
    MainForm.updateLifeCyclePanelForFirstSelectedPlant;
  finally
    cursor_stopWait;
  end;
  end;

{ redo is same as do }
function PdChangePlantAgeCommand.description: string;
	begin
  result := 'change age to ' + intToStr(newAge) + ' for' + plantNamesForDescription(plantList);

  end;

{ ----------------------------------------------------------------------- PdAnimatePlantCommand }
constructor PdAnimatePlantCommand.createWithListOfPlants(aList: TList);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    values.add(PdSmallintValue.createWithSmallint(PdPlant(plantList.items[i]).age));
  end;

procedure PdAnimatePlantCommand.doCommand;
  var
    i: smallint;
    plant: PdPlant;
  begin
  inherited doCommand; 
  if plantList.count <= 0 then exit;
  age := 0;
  { find oldest age }
  oldestAgeAtMaturity := 0;
  for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    if (i = 0) or (plant.pGeneral.ageAtMaturity > oldestAgeAtMaturity) then
      oldestAgeAtMaturity := plant.pGeneral.ageAtMaturity;
    end;
  { reset all plants to age zero and draw them }
  domain.temporarilyHideSelectionRectangles := true;
  self.invalidateCombinedPlantRects;
  try
    for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.reset;
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
    MainForm.updateForPossibleChangeToDrawing;
  finally
    domain.temporarilyHideSelectionRectangles := false;
  end;
  MainForm.animateCommand := self;
  MainForm.startAnimation;
  end;

procedure PdAnimatePlantCommand.animateOneDay;
  var
    i: smallint;
    plant: PdPlant;
  begin
  { grow all plants one day }
  domain.temporarilyHideSelectionRectangles := true;
  try
    self.invalidateCombinedPlantRects;
    for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      if age < plant.pGeneral.ageAtMaturity then
        begin
        plant.nextDay;
        plant.recalculateBounds(kDrawNow);
        end;
      end;
    self.invalidateCombinedPlantRects;
    { don't want to update params, because they don't change during animation }
    if MainForm.lifeCycleShowing then
      MainForm.updateLifeCyclePanelForFirstSelectedPlant
    else if MainForm.statsShowing then
      MainForm.updateStatisticsPanelForFirstSelectedPlant;
    MainForm.updateForPossibleChangeToDrawing;
    inc(age);
  finally
    domain.temporarilyHideSelectionRectangles := false;
  end;
  if age >= oldestAgeAtMaturity then
    MainForm.stopAnimation;
  MainForm.updateForChangeToSelectedPlantsLocation;
  end;

procedure PdAnimatePlantCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  try
    cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.setAge(PdSmallintValue(values.items[i]).saveSmallint);
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
    MainForm.updateForChangeToSelectedPlantsLocation;
    { changing age causes life cycle panel to need to redraw }
    MainForm.updateLifeCyclePanelForFirstSelectedPlant;
  finally
    cursor_stopWait;
  end;
  end;

{ redo is same as do }
function PdAnimatePlantCommand.description: string;
	begin
  result := 'animate' + plantNamesForDescription(plantList);

  end;

{ ------------------------------------------------------------ PdHideOrShowCommand }
constructor PdHideOrShowCommand.createWithListOfPlantsAndHideOrShow(aList: TList; aHide: boolean);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  commandChangesPlantFile := false; {hidden flag not saved}
  hide := aHide;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    values.add(PdBooleanValue.createWithBoolean(PdPlant(plantList.items[i]).hidden));
  end;

constructor PdHideOrShowCommand.createWithListOfPlantsAndListOfHides(aList: TList; aHideList: TListCollection);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  commandChangesPlantFile := false; {hidden flag not saved}
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    values.add(PdBooleanValue.createWithBoolean(PdPlant(plantList.items[i]).hidden));
  newValues := TListCollection.create;
  if aHideList.count > 0 then for i := 0 to aHideList.count - 1 do
    newValues.add(PdBooleanValue.createWithBoolean(PdBooleanValue(aHideList.items[i]).saveBoolean));
  end;

destructor PdHideOrShowCommand.destroy;
  begin
  newValues.free;
  newValues := nil;
  inherited destroy;
  end;

procedure PdHideOrShowCommand.doCommand;
  begin
  inherited doCommand;
  MainForm.hideOrShowSomePlants(plantList, newValues, hide, kDontDrawYet);
  end;

procedure PdHideOrShowCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  MainForm.hideOrShowSomePlants(plantList, values, hide, kDontDrawYet);
  end;

function PdHideOrShowCommand.description: string;
	begin
  if (newValues <> nil) and (newValues.count > 0) then
    result := 'hide others'
  else if hide then
    result := 'hide' + plantNamesForDescription(plantList)
  else
    result := 'show' + plantNamesForDescription(plantList);
  end;

{ --------------------------------------------------------------------------------------------- PdNewCommand }
constructor PdNewCommand.createWithWizardPlantAndOldSelectedList(aPlant: PdPlant; anOldSelectedList: TList);
  var i: integer;
  begin
  inherited create;
  useWizardPlant := true;
  wizardPlant := aPlant;
  // selected list is just pointers, this doesn't take control of them
  oldSelectedList := TList.create;
  if (anOldSelectedList <> nil) and (anOldSelectedList.count > 0) then
    for i := 0 to anOldSelectedList.count - 1 do
      oldSelectedList.add(anOldSelectedList.items[i]);
  end;

destructor PdNewCommand.destroy;
  begin
  oldSelectedList.free;
  oldSelectedList := nil;
  { free created plant if change was undone }
  if (not done) and (newPlant <> nil) then
    begin
    newPlant.free;
    newPlant := nil;
    end;
  if (useWizardPlant) and (wizardPlant <> nil) then
    begin
    wizardPlant.free;
    wizardPlant := nil;
    end;
  inherited destroy;
  end;

function PdNewCommand.numberOfStoredLargeObjects: longint;
  begin
  result := 0;
  if (not done) and (newPlant <> nil) then
    inc(result);
  if (useWizardPlant) and (wizardPlant <> nil) then
    inc(result);
  end;

procedure PdNewCommand.doCommand;
  begin
  inherited doCommand; 
  newPlant := PdPlant.create;
  try
    cursor_startWait;
    if (useWizardPlant) and (wizardPlant <> nil) then
      wizardPlant.copyTo(newPlant)
    else
      begin
      newPlant.defaultAllParameters;
      newPlant.setName('New plant ' + intToStr(numPlantsCreatedThisSession + 1));
      inc(numPlantsCreatedThisSession);
      end;
    newPlant.randomize;
    newPlant.moveTo(MainForm.standardPastePosition);
    newPlant.calculateDrawingScaleToLookTheSameWithDomainScale;
    newPlant.recalculateBounds(kDrawNow);
    { put new plant at end of plant manager list }
    domain.plantManager.plants.add(newPlant);
    { make new plant the only selected plant }
    MainForm.deselectAllPlants;
    MainForm.addSelectedPlant(newPlant, kAddAtEnd);
    MainForm.updateForChangeToPlantList;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdNewCommand.undoCommand;
  var i: integer;
  begin
  inherited undoCommand;
  domain.plantManager.plants.remove(newPlant);
  MainForm.removeSelectedPlant(newPlant);
  // put back selections from before new plant was added
  if oldSelectedList.count > 0 then
    for i := 0 to oldSelectedList.count - 1 do
      MainForm.selectedPlants.add(oldSelectedList.items[i]);
  MainForm.updateForChangeToPlantList;
  end;

procedure PdNewCommand.redoCommand;
  begin
  inherited doCommand;
  MainForm.deselectAllPlants;
  domain.plantManager.plants.add(newPlant);
  MainForm.addSelectedPlant(newPlant, kAddAtEnd);
  MainForm.updateForChangeToPlantList;
  end;

function PdNewCommand.description: string;
	begin
  result := 'create new plant';
  end;

{ ------------------------------------------------------------ PdEditNoteCommand }
constructor PdEditNoteCommand.createWithPlantAndNewTStrings(aPlant: PdPlant; aNewStrings: TStrings);
  begin
  inherited create;
  plant := aPlant;
  oldStrings := plant.noteLines;
  newStrings := aNewStrings as TStringList; // we take ownership of this list and delete it if undone
  end;

destructor PdEditNoteCommand.destroy;
  begin
  if done then
    begin
    oldStrings.free;
    oldStrings := nil;
    end
  else
    begin
    newStrings.free;
    newStrings := nil;
    end;
  end;

procedure PdEditNoteCommand.doCommand;
  begin
  inherited doCommand;
  plant.noteLines := newStrings;
  MainForm.updateForChangeToPlantNote(plant);
  end;

procedure PdEditNoteCommand.undoCommand;
  begin
  inherited undoCommand;
  plant.noteLines := oldStrings;
  MainForm.updateForChangeToPlantNote(plant);
  end;

function PdEditNoteCommand.description: string;
	begin
  result := 'change note for "' + plant.getName + '"';
  end;

{ ------------------------------------------------------------ PdCreateAmendmentCommand }
constructor PdCreateAmendmentCommand.createWithPlantAndAmendment(aPlant: PdPlant;
    aNewAmendment: PdPlantDrawingAmendment);
  begin
  inherited create;
  plant := aPlant;
  if aNewAmendment = nil then
    raise exception.create('Problem: Nil new amendment; in PdCreateAmendmentCommand.createWithPlantAndAmendment.');
  newAmendment := aNewAmendment; // we take ownership of this and delete it if undone
  end;

destructor PdCreateAmendmentCommand.destroy;
  begin
  if not done then
    begin
    newAmendment.free;
    newAmendment := nil;
    end;
  end;

procedure PdCreateAmendmentCommand.doCommand;
  begin
  inherited doCommand;
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  plant.addAmendment(newAmendment);
  plant.recalculateBounds(kDrawNow);
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  MainForm.addAmendedPartToList(newAmendment.partID, newAmendment.typeOfPart);
  end;

procedure PdCreateAmendmentCommand.undoCommand;
  begin
  inherited undoCommand;
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  plant.removeAmendment(newAmendment);
  plant.recalculateBounds(kDrawNow);
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  MainForm.removeAmendedPartFromList(newAmendment.partID, newAmendment.typeOfPart);
  end;

function PdCreateAmendmentCommand.description: string;
	begin
  result := 'pose part ' + intToStr(newAmendment.partID) + ' in plant "' + plant.getName + '"';
  end;

{ ------------------------------------------------------------ PdDeleteAmendmentCommand }
constructor PdDeleteAmendmentCommand.createWithPlantAndAmendment(aPlant: PdPlant;
    anAmendment: PdPlantDrawingAmendment);
  begin
  inherited create;
  plant := aPlant;
  if anAmendment = nil then
    raise exception.create('Problem: Nil amendment; in PdDeleteAmendmentCommand.createWithPlantAndAmendment.');
  amendment := anAmendment; // we take ownership of this and delete it if done
  end;

destructor PdDeleteAmendmentCommand.destroy;
  begin
  if done then
    begin
    amendment.free;
    amendment := nil;
    end;
  end;

procedure PdDeleteAmendmentCommand.doCommand;
  begin
  inherited doCommand;
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  plant.removeAmendment(amendment);
  plant.recalculateBounds(kDrawNow);
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  MainForm.removeAmendedPartFromList(amendment.partID, amendment.typeOfPart);
  end;

procedure PdDeleteAmendmentCommand.undoCommand;
  begin
  inherited undoCommand;
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  plant.addAmendment(amendment);
  plant.recalculateBounds(kDrawNow);
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  MainForm.addAmendedPartToList(amendment.partID, amendment.typeOfPart);
  end;

function PdDeleteAmendmentCommand.description: string;
	begin
  result := 'unpose part ' + intToStr(amendment.partID) + ' in plant "' + plant.getName + '"';
  end;

{ ------------------------------------------------------------ PdEditAmendmentCommand }
constructor PdEditAmendmentCommand.createWithPlantAndAmendmentAndField(aPlant: PdPlant;
    aNewAmendment: PdPlantDrawingAmendment; aField: string);
  begin
  inherited create;
  plant := aPlant;
  field := aField;
  if aNewAmendment = nil then
    raise exception.create('nil new amendment');
  newAmendment := aNewAmendment; // we take ownership of this and delete it if undone
  oldAmendment := plant.amendmentForPartID(newAmendment.partID);
  end;

destructor PdEditAmendmentCommand.destroy;
  begin
  if done then
    begin
    oldAmendment.free;
    oldAmendment := nil;
    end
  else
    begin
    newAmendment.free;
    newAmendment := nil;
    end;
  end;

procedure PdEditAmendmentCommand.doCommand;
  var
    index, oldItemIndex: integer;
  begin
  inherited doCommand;
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  if oldAmendment <> nil then
    plant.removeAmendment(oldAmendment);
  plant.addAmendment(newAmendment);
  plant.recalculateBounds(kDrawNow);
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  MainForm.updatePoseInfo;
  end;

procedure PdEditAmendmentCommand.undoCommand;
  var
    oldString: string;
    index, oldItemIndex: integer;
  begin
  inherited undoCommand;
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  plant.removeAmendment(newAmendment);
  if oldAmendment <> nil then
    plant.addAmendment(oldAmendment);
  plant.recalculateBounds(kDrawNow);
  MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
  MainForm.updatePoseInfo;
  end;

function PdEditAmendmentCommand.description: string;
  var fullString: string;
	begin
  if field = 'hide' then
    begin
    if newAmendment.hide then fullString := 'hide' else fullString := 'show';
    end
  else if field = 'rotate' then
    begin
    if newAmendment.addRotations then fullString := 'rotate' else fullString := 'remove rotation for';
    end
  else if field = 'scale' then
    begin
    if newAmendment.multiplyScale then fullString := 'scale' else fullString := 'remove scaling for';
    end
  else if field = 'scale above' then
    begin
    if newAmendment.propagateScale then fullString := 'scale-this-part-and-above'
      else fullString := 'remove scale-this-part-and-above for';
    end
  else
    fullString := 'change ' + field + ' for';
  result := 'posing: ' + fullString + ' part ' + intToStr(newAmendment.partID) + ' in plant "' + plant.getName + '"';
  end;

{ ------------------------------------------------------------ PdRenameCommand }
constructor PdRenameCommand.createWithPlantAndNewName(aPlant: PdPlant; aNewName: string);
  begin
  inherited create;
  plant := aPlant;
  oldName := plant.getName;
  newName := aNewName;
  end;

procedure PdRenameCommand.doCommand;
  begin
  inherited doCommand;
  plant.setName(newName);
  MainForm.updateForRenamingPlant(plant);
  end;

procedure PdRenameCommand.undoCommand;
  begin
  inherited undoCommand;
  plant.setName(oldName);
  MainForm.updateForRenamingPlant(plant);
  end;

function PdRenameCommand.description: string;
	begin
  result := 'rename "' + oldName + '" to "' + newName + '"';
  end;

{ ------------------------------------------------------------ PdChangeSelectedPlantsCommand }
constructor PdChangeSelectedPlantsCommand.createWithOldListOFPlantsAndNewList(aList: TList; aNewList: TList);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  commandChangesPlantFile := false; {which plants are selected not saved}
  newList := TList.create;
  if aNewList.count > 0 then for i := 0 to aNewList.count - 1 do
    newList.add(aNewList.items[i]);
  end;

destructor PdChangeSelectedPlantsCommand.destroy;
  begin
  newList.free;
  newList := nil;
  inherited destroy;
  end;

procedure PdChangeSelectedPlantsCommand.doCommand;
  var
    i: smallint;
  begin
  commandChangesPlantFile := false; {which plants are selected not saved}
  inherited doCommand;
 // MainForm.deselectAllPlants; // don't want this, it updates, and we will be updating soon
  MainForm.selectedPlants.clear;
  if newList.count > 0 then
    begin
    MainForm.selectedPlants.add(newList.items[0]);
    if domain.viewPlantsInMainWindowOnePlantAtATime then
      MainForm.showOnePlantExclusively(kDontDrawYet)
    else
      begin
      if newList.count > 1 then for i := 1 to newList.count - 1 do
        MainForm.selectedPlants.add(newList.items[i]);
      end;
    end;
  MainForm.updateForChangeToPlantSelections;
  end;

procedure PdChangeSelectedPlantsCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  // MainForm.deselectAllPlants; // don't want this, it updates, and we will be updating soon
  MainForm.selectedPlants.clear;
  if plantList.count > 0 then
    begin
    MainForm.selectedPlants.add(plantList.items[0]);
    if domain.viewPlantsInMainWindowOnePlantAtATime then
      MainForm.showOnePlantExclusively(kDontDrawYet)
    else
      begin
      if plantList.count > 1 then for i := 1 to plantList.count - 1 do
        MainForm.selectedPlants.add(plantList.items[i]);
      end;
    end;
  MainForm.updateForChangeToPlantSelections;
  end;

function PdChangeSelectedPlantsCommand.description: string;
	begin
  if newList.count <= 0 then
    result := 'deselect all plants'
  else
    result := 'select' + plantNamesForDescription(newList);
  end;

{ ------------------------------------------------------------ PdSelectPosingPartCommand }
constructor PdSelectPosingPartCommand.createWithPlantAndPartIDsAndTypes(aPlant: PdPlant; aNewPartID, anOldPartID: longint;
      aNewPartType, anOldPartType: string);
  var
    i: smallint;
  begin
  inherited create;
  commandChangesPlantFile := false; // selected posed part not saved
  plant := aPlant;
  newPartID := aNewPartID;
  oldPartID := anOldPartID;
  newPartType := aNewPartType;
  oldPartType := anOldPartType;
  end;

procedure PdSelectPosingPartCommand.doCommand;
  begin
  commandChangesPlantFile := false; // selected posed part not saved
  inherited doCommand;
  MainForm.selectedPlantPartID := newPartID;
  MainForm.selectedPlantPartType := newPartType;
  MainForm.updatePosingForSelectedPlantPart;
  MainForm.redrawFocusedPlantOnly(kDrawNow);
  end;

procedure PdSelectPosingPartCommand.undoCommand;
  begin
  inherited undoCommand;
  MainForm.selectedPlantPartID := oldPartID;
  MainForm.selectedPlantPartType := oldPartType;
  MainForm.updatePosingForSelectedPlantPart;
  MainForm.redrawFocusedPlantOnly(kDrawNow);
  end;

function PdSelectPosingPartCommand.description: string;
	begin
  if newPartID < 0 then
    result := 'deselect all parts of plant ' + plant.getName
  else
    result := 'select part ' + intToStr(newPartID) + ' of plant ' + plant.getName;
  end;

{ ------------------------------------------------------------ PdSelectOrDeselectAllCommand }
procedure PdSelectOrDeselectAllCommand.doCommand;
  var
    i: smallint;
  begin
  commandChangesPlantFile := false; {which plants are selected not saved}
  inherited doCommand;
  // MainForm.deselectAllPlants;
  if deselect then
    MainForm.deselectAllPlants
  else
    MainForm.selectedPlants.clear;
  if not deselect then
    with domain.plantManager.plants do
      if count > 0 then for i := 0 to count - 1 do
        MainForm.selectedPlants.add(items[i]);
  MainForm.updateForChangeToPlantSelections;
  end;

procedure PdSelectOrDeselectAllCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  // MainForm.deselectAllPlants;
  if not deselect then
    MainForm.deselectAllPlants
  else
    MainForm.selectedPlants.clear;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      MainForm.selectedPlants.add(plantList.items[i]);
  MainForm.updateForChangeToPlantSelections;
  end;

function PdSelectOrDeselectAllCommand.description: string;
	begin
  if deselect then
    result := 'deselect all plants'
  else
    result := 'select all plants';
  end;

{ ------------------------------------------------------------ PdChangeMainWindowViewingOptionCommand }
constructor PdChangeMainWindowViewingOptionCommand.createWithListOfPlantsAndSelectedPlantsAndNewOption(aList: TList;
    aSelectedList: TList; aNewOption: smallint);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  commandChangesPlantFile := false; {hidden flag not saved}
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    values.add(PdBooleanValue.createWithBoolean(PdPlant(plantList.items[i]).hidden));
  selectedList := TList.create;
  if aSelectedList.count > 0 then for i := 0 to aSelectedList.count - 1 do
    selectedList.add(PdPlant(aSelectedList.items[i]));
  oldMainWindowViewingOption := domain.options.mainWindowViewMode;
  newMainWindowViewingOption := aNewOption;
  end;


destructor PdChangeMainWindowViewingOptionCommand.destroy;
  begin
  selectedList.free;
  selectedList := nil;
  inherited destroy;
  end;

procedure PdChangeMainWindowViewingOptionCommand.doCommand;
  begin
  inherited doCommand;
  try
    cursor_startWait;
    domain.options.mainWindowViewMode :=  newMainWindowViewingOption;
    case newMainWindowViewingOption of
      kViewPlantsInMainWindowOneAtATime:
        begin
        oldScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
        oldOffset_mm := domain.plantDrawOffset_mm;
        MainForm.deselectAllPlantsButFirst;
        MainForm.showOnePlantExclusively(kDontDrawYet); {hides all plants but first; calls fitVisiblePlantsInDrawingArea}
        MainForm.recalculateSelectedPlantsBoundsRects(kDrawNow);
        MainForm.invalidateEntireDrawing;
        MainForm.updateForChangeToPlantSelections;
        newScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
        newOffset_mm := domain.plantDrawOffset_mm;
        end;
      kViewPlantsInMainWindowFreeFloating:
        begin
        oldScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
        oldOffset_mm := domain.plantDrawOffset_mm;
        MainForm.hideOrShowSomePlants(plantList, nil, kShow, kDontDrawYet);
        MainForm.fitVisiblePlantsInDrawingArea(kDontDrawYet, kScaleAndMove, kAlwaysMove);
        // first drawing gets correct bounds rects so numbers get counted for progress bar - messy
        MainForm.recalculateAllPlantBoundsRects(kDontDrawYet);
        MainForm.recalculateAllPlantBoundsRects(kDrawNow);
        MainForm.invalidateEntireDrawing;
        newScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
        newOffset_mm := domain.plantDrawOffset_mm;
        end;
      end;
    MainForm.updateMenusForChangeToViewingOption;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdChangeMainWindowViewingOptionCommand.undoCommand;
  var i: smallint;
  begin
  inherited doCommand;
  try
    cursor_startWait;
    domain.options.mainWindowViewMode := oldMainWindowViewingOption;
    case newMainWindowViewingOption of
      kViewPlantsInMainWindowOneAtATime:
        begin
        MainForm.recalculateAllPlantBoundsRects(kDrawNow);
        MainForm.invalidateSelectedPlantRectangles;
        domain.plantManager.plantDrawScale_PixelsPerMm := oldScale_PixelsPerMm;
        domain.plantManager.plantDrawOffset_mm := oldOffset_mm;
        { restore original hidden flags - all plants }
        MainForm.hideOrShowSomePlants(plantList, values, false{not used}, kDontDrawYet);
        MainForm.fitVisiblePlantsInDrawingArea(kDontDrawYet, kScaleAndMove, kAlwaysMove);
        MainForm.recalculateAllPlantBoundsRects(kDrawNow);
        MainForm.invalidateEntireDrawing;//MainForm.invalidateSelectedPlantRectangles;
        { restore original selection - selected plants only }
        MainForm.selectedPlants.clear;
        if selectedList.count > 0 then for i := 0 to selectedList.count - 1 do
          MainForm.selectedPlants.add(PdPlant(selectedList.items[i]));
        MainForm.updateForChangeToPlantSelections;
        end;
      kViewPlantsInMainWindowFreeFloating:
        begin
        domain.plantManager.plantDrawScale_PixelsPerMm := oldScale_PixelsPerMm;
        domain.plantManager.plantDrawOffset_mm := oldOffset_mm;
        { restore original hidden flags - all plants }
        MainForm.hideOrShowSomePlants(plantList, values, false{not used}, kDontDrawYet);
        MainForm.fitVisiblePlantsInDrawingArea(kDontDrawYet, kScaleAndMove, kAlwaysMove);
        MainForm.recalculateAllPlantBoundsRects(kDrawNow);
        MainForm.invalidateEntireDrawing;//MainForm.invalidateSelectedPlantRectangles;
        MainForm.updateForChangeToPlantSelections;
        end;
      end;
    MainForm.updateMenusForChangeToViewingOption;
  finally
    cursor_stopWait;
  end;
  end;

function PdChangeMainWindowViewingOptionCommand.description: string;
	begin
  result := 'change view all/one option in main window';
  end;

{ ------------------------------------------------------------ PdChangeMainWindowOrientationCommand }
constructor PdChangeMainWindowOrientationCommand.createWithNewOrientation(aNewOrientation: smallint);
  begin
  inherited create;
  commandChangesPlantFile := false; {hidden flag not saved}
  newWindowOrientation := aNewOrientation;
  oldWindowOrientation := domain.options.mainWindowOrientation;
  end;

procedure PdChangeMainWindowOrientationCommand.doCommand;
  begin
  inherited doCommand;
  try
    cursor_startWait;
    domain.options.mainWindowOrientation := newWindowOrientation;
    MainForm.updateForChangeToOrientation;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdChangeMainWindowOrientationCommand.undoCommand;
  begin
  inherited undoCommand;
  try
    cursor_startWait;
    domain.options.mainWindowOrientation := oldWindowOrientation;
    MainForm.updateForChangeToOrientation;
  finally
    cursor_stopWait;
  end;
  end;

function PdChangeMainWindowOrientationCommand.description: string;
	begin
  result := 'change top/side orientation in main window';
  end;

{ -------------------------------------------------------- PdCenterDrawingCommand }
procedure PdCenterDrawingCommand.doCommand;
  begin
  inherited doCommand; 
  oldScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
  oldOffset_mm := domain.plantDrawOffset_mm;
  MainForm.fitVisiblePlantsInDrawingArea(kDrawNow, kScaleAndMove, kAlwaysMove);
  MainForm.recalculateAllPlantBoundsRects(kDontDrawNow);
  newScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
  newOffset_mm := domain.plantDrawOffset_mm;
  end;

procedure PdCenterDrawingCommand.undoCommand;
  begin
  inherited undoCommand;
  domain.plantManager.plantDrawOffset_mm := oldOffset_mm;
  MainForm.recalculateAllPlantBoundsRects(kDrawNow);
  if oldScale_PixelsPerMm <> 0.0 then
    MainForm.magnifyOrReduce(oldScale_PixelsPerMm, Point(0, 0), kDrawNow);
  end;

procedure PdCenterDrawingCommand.redoCommand;
  begin
  inherited doCommand;
  domain.plantManager.plantDrawOffset_mm := newOffset_mm;
  MainForm.recalculateAllPlantBoundsRects(kDrawNow);
  if newScale_PixelsPerMm <> 0.0 then
    MainForm.magnifyOrReduce(newScale_pixelsPerMm, Point(0, 0), kDrawNow);
  end;

function PdCenterDrawingCommand.description: string;
  begin
  result := 'scale to fit in main window';
  end;

{ -------------------------------------------------------- PdChangeMagnificationCommand }
constructor PdChangeMagnificationCommand.createWithNewScaleAndPoint(aNewScale: single; aPoint: TPoint);
  begin
  inherited create;
  newScale_pixelsPerMm := aNewScale;
  oldScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
  oldOffset_mm := domain.plantDrawOffset_mm;
  clickPoint.x := aPoint.x;
  clickPoint.y := aPoint.y;
  end;

function PdChangeMagnificationCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand;
  var
    size: TPoint;
    newScaleX, newScaleY: single;
  begin
  result := self;
  if aTrackPhase = trackPress then
    begin
    startDragPoint := nextPoint;
    end
  else if aTrackPhase = trackMove then
  	begin
  	end
  else if aTrackPhase = trackRelease then
  	begin
    size := Point(abs(nextPoint.x - startDragPoint.x), abs(startDragPoint.y - nextPoint.y));
    if (size.x > 10) and (size.y > 10) then // have min size in case they move the mouse by mistake
      begin
      clickPoint.x := min(nextPoint.x, startDragPoint.x) + abs(nextPoint.x - startDragPoint.x) div 2;
      clickPoint.y := min(nextPoint.y, startDragPoint.y) + abs(nextPoint.y - startDragPoint.y) div 2;
      newScaleX := safedivExcept(domain.plantDrawScale_PixelsPerMm * MainForm.drawingPaintBox.width, size.x, 1.0);
      newScaleY := safedivExcept(domain.plantDrawScale_PixelsPerMm * MainForm.drawingPaintBox.height, size.y, 1.0);
      self.oldScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
      self.oldOffset_mm := domain.plantDrawOffset_mm;
      self.newScale_pixelsPerMm := min(newScaleX, newScaleY);
      end
    else
      begin
      clickPoint.x := nextPoint.x;
      clickPoint.y := nextPoint.y;
      self.oldScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
      self.oldOffset_mm := domain.plantDrawOffset_mm;
      if shift then
        self.newScale_pixelsPerMm := oldScale_PixelsPerMm * 0.75
      else
        self.newScale_pixelsPerMm := oldScale_PixelsPerMm * 1.5;
      end;
  	end;
	end;

procedure PdChangeMagnificationCommand.doCommand;
  var
    clickTPoint: TPoint;
  begin
  inherited doCommand;
  if newScale_pixelsPerMm <> 0.0 then
    begin
    clickTPoint.x := round(clickPoint.x);
    clickTPoint.y := round(clickPoint.y);
    MainForm.magnifyOrReduce(newScale_pixelsPerMm, clickTPoint, kDrawNow);
    end;
  self.newOffset_mm := domain.plantDrawOffset_mm;
  end;

procedure PdChangeMagnificationCommand.undoCommand;
  begin
  inherited undoCommand;
  domain.plantManager.plantDrawOffset_mm := oldOffset_mm;
  if oldScale_PixelsPerMm <> 0.0 then
    MainForm.magnifyOrReduce(oldScale_PixelsPerMm, Point(0,0), kDrawNow);
  end;

function PdChangeMagnificationCommand.description: string;
  begin
  if newScale_pixelsPerMm > oldScale_PixelsPerMm then
    result := 'enlarge in main window'
  else
    result := 'reduce in main window';
  end;

{ ------------------------------------------------------------ PdScrollCommand }
function PdScrollCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
    mouseDidMove, rightButtonDown: boolean): PdCommand;
  begin
  result := self;
  if aTrackPhase = trackPress then
  	begin
    dragStartPoint := nextPoint;
    oldOffset_mm := domain.plantDrawOffset_mm;
    end
  else if aTrackPhase = trackMove then
  	begin
  	if mouseDidMove then
      begin
      newOffset_mm.x := oldOffset_mm.x + (nextPoint.x - dragStartPoint.x) / domain.plantDrawScale_PixelsPerMm;
      newOffset_mm.y := oldOffset_mm.y + (nextPoint.y - dragStartPoint.y) / domain.plantDrawScale_PixelsPerMm;
      domain.plantManager.plantDrawOffset_mm := newOffset_mm;
      MainForm.recalculateAllPlantBoundsRectsForOffsetChange;
      MainForm.invalidateEntireDrawing;
      end;
  	end
  else if aTrackPhase = trackRelease then
  	begin
  	end;
	end;

{ PdDragCommand.doCommand should do nothing}
procedure PdScrollCommand.redoCommand;
  begin
  inherited doCommand; {not redo}
  domain.plantManager.plantDrawOffset_mm := newOffset_mm;
  MainForm.recalculateAllPlantBoundsRectsForOffsetChange;
  MainForm.invalidateEntireDrawing;
  end;

procedure PdScrollCommand.undoCommand;
  begin
  inherited undoCommand;
  domain.plantManager.plantDrawOffset_mm := oldOffset_mm;
  MainForm.recalculateAllPlantBoundsRectsForOffsetChange;
  MainForm.invalidateEntireDrawing;
  end;

function PdScrollCommand.description: string;
	begin
  result := 'scroll in main window';
  end;

{ --------------------------------------------------------------------------------------------- PdRemoveCommand }
constructor PdRemoveCommand.createWithListOfPlantsAndClipboardFlag(aList: TList; aCopyToClipboard: boolean);
  begin
  inherited createWithListOfPlants(aList);
  removedPlants := TList.create;
  copyToClipboard := aCopyToClipboard;
  end;

destructor PdRemoveCommand.destroy;
  var
    i: smallint;
  begin
  { free copies of cut plants if change was done }
  if (done) and (removedPlants <> nil) and (removedPlants.count > 0) then
    for i := 0 to removedPlants.count - 1 do
    	begin
    	plant := PdPlant(removedPlants.items[i]);
    	plant.free;
    	end;
  removedPlants.free;
  removedPlants := nil;
  inherited destroy;
  end;

function PdRemoveCommand.numberOfStoredLargeObjects: longint;
  begin
  result := 0;
  if (done) and (removedPlants <> nil) then
    result := removedPlants.count;
  end;

procedure PdRemoveCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; 
  if plantList.count <= 0 then exit;
  { copy plants }
  if copyToClipboard then
    MainForm.copySelectedPlantsToClipboard;
  { save copy of plants before deleting }
  removedPlants.clear;
  { don't remove plants from plant manager and MainForm.selectedPlants until all indexes have been recorded }
  for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    removedPlants.add(plant);
    plant.indexWhenRemoved := domain.plantManager.plants.indexOf(plant);
    plant.selectedIndexWhenRemoved := MainForm.selectedPlants.indexOf(plant);
    end;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    domain.plantManager.plants.remove(plant);
    MainForm.removeSelectedPlant(plant);
    end;
  MainForm.updateForChangeToPlantList;
  // if only looking at one, select first in list so you are not left with nothing
  if domain.viewPlantsInMainWindowOnePlantAtATime then
    begin
    MainForm.selectFirstPlantInPlantList;
    MainForm.showOnePlantExclusively(kDrawNow);
    end;
  end;

procedure PdRemoveCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if domain.viewPlantsInMainWindowOnePlantAtATime then
    MainForm.deselectAllPlants; // remove selection if created
  if removedPlants.count > 0 then for i := 0 to removedPlants.count - 1 do
    begin
    plant := PdPlant(removedPlants.items[i]);
    if (plant.indexWhenRemoved >= 0) and (plant.indexWhenRemoved <= domain.plantManager.plants.count - 1) then
      domain.plantManager.plants.insert(plant.indexWhenRemoved, plant)
    else
      domain.plantManager.plants.add(plant);
    { all removed plants must have been selected, so also add them to the selected list }
    MainForm.addSelectedPlant(plant, plant.selectedIndexWhenRemoved);
    end;
  MainForm.updateForChangeToPlantList;
  end;

function PdRemoveCommand.description: string;
	begin
  if copyToClipboard then
    result := 'cut' + plantNamesForDescription(plantList)
  else
    result := 'delete' + plantNamesForDescription(plantList);
  end;

{ --------------------------------------------------------------------------------------------- PdPasteCommand }
constructor PdPasteCommand.createWithListOfPlantsAndOldSelectedList(aList, anOldSelectedList: TList);
  var
    i: smallint;
  begin
  inherited createWithListOfPlants(aList);
  // selected list is just pointers, this doesn't take control of them
  oldSelectedList := TList.create;
  if (anOldSelectedList <> nil) and (anOldSelectedList.count > 0) then
    for i := 0 to anOldSelectedList.count - 1 do
      oldSelectedList.add(anOldSelectedList.items[i]);
  end;

destructor PdPasteCommand.destroy;
  var
    i: smallint;
  begin
  oldSelectedList.free;
  oldSelectedList := nil;
  { free copies of pasted plants if change was undone }
  if (not done) and (plantList <> nil) and (plantList.count > 0) then
    for i := 0 to plantList.count - 1 do
    	begin
    	plant := PdPlant(plantList.items[i]);
    	plant.free;
    	end;
  inherited destroy; {will free plantList TList}
  end;

function PdPasteCommand.numberOfStoredLargeObjects: longint;
  begin
  result := 0;
  if (not done) and (plantList <> nil) then
    result := plantList.count;
  end;

procedure PdPasteCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; 
  if plantList.count <= 0 then exit;
  { make new plants the only selected plants }
  MainForm.deselectAllPlants;
  for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    { put new plants at end of plant manager list }
    domain.plantManager.plants.add(plant);
    if not self.useSpecialPastePosition then
      begin
      if not domain.viewPlantsInMainWindowOnePlantAtATime then
        begin
        plant.moveTo(MainForm.standardPastePosition);
        if not plant.justCopiedFromMainWindow then
          plant.calculateDrawingScaleToLookTheSameWithDomainScale;
        end;
      end;
    plant.recalculateBounds(kDrawNow);
    MainForm.addSelectedPlant(plant, kAddAtEnd);
    end;
  MainForm.updateForChangeToPlantList;
  end;

procedure PdPasteCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if plantList.count <= 0 then exit;
  for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    domain.plantManager.plants.remove(plant);
    MainForm.removeSelectedPlant(plant);
    end;
  // put back selections from before paste
  if oldSelectedList.count > 0 then
    for i := 0 to oldSelectedList.count - 1 do
      MainForm.selectedPlants.add(oldSelectedList.items[i]);
  MainForm.updateForChangeToPlantList;
  end;

function PdPasteCommand.description: string;
	begin
  result := 'paste' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------------------ PdDuplicateCommand }
constructor PdDuplicateCommand.createWithListOfPlants(aList: TList);
  begin
  inherited createWithListOfPlants(aList);
  newPlants := TList.create;
  end;

destructor PdDuplicateCommand.destroy;
  var
    i: smallint;
  begin
  { free copies of created plants if change was undone }
  if (not done) and (newPlants <> nil) and (newPlants.count > 0) then
    for i := 0 to newPlants.count - 1 do
    	begin
    	plant := PdPlant(newPlants.items[i]);
    	plant.free;
    	end;
  newPlants.free;
  newPlants := nil;
  inherited destroy; {will free plantList}
  end;

function PdDuplicateCommand.numberOfStoredLargeObjects: longint;
  begin
  result := 0;
  if (not done) and (newPlants <> nil) then
    result := newPlants.count;
  end;

function PdDuplicateCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
  mouseDidMove, rightButtonDown: boolean): PdCommand;
  var
    i: smallint;
    originalPlant: PdPlant;
  begin
  result := self;
  if aTrackPhase = trackPress then
  	begin
    end
  else if aTrackPhase = trackMove then
  	begin
    if not done and mouseDidMove then
      begin
      startDragPoint := nextPoint;
      self.inTrackMouse := true;
      self.doCommand;
      end;
    if not done then exit;
    if not ptInRect(MainForm.drawingPaintBox.clientRect, nextPoint) then
      begin
      self.undoCommand;
      result := nil;
      self.free;
      end
  	else
      begin
      offset.x := nextPoint.x - startDragPoint.x;
      offset.y := nextPoint.y - startDragPoint.y;
      if newPlants.count > 0 then for i := 0 to newPlants.count - 1 do
        begin
        plant := PdPlant(newPlants.items[i]);
        if (i <= plantList.count - 1) then
          begin
          originalPlant := PdPlant(plantList.items[i]);
          MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
          plant.moveTo(originalPlant.basePoint_pixels);
          plant.moveBy(offset);
          plant.recalculateBounds(plant.previewCache.width < 5); // only draw if don't have picture yet
          MainForm.invalidateDrawingRect(plant.boundsRect_pixels);
          end;
        end;
      end;
  	end
  else if aTrackPhase = trackRelease then
  	begin
    if not mouseDidMove then
      begin
      result := nil;
      self.free;
      end;
   	end;
  end;

procedure PdDuplicateCommand.doCommand;
  var
    i: smallint;
    plantCopy: PdPlant;
  begin
  { should have been done in the mouse down, unless it was done by a menu command }
  if self.done then exit;
  inherited doCommand;
  if plantList.count <= 0 then exit;
  { make new plants only selected plants }
  MainForm.deselectAllPlants;
  for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plantCopy := PdPlant.create;
    plant.copyTo(plantCopy);
    plantCopy.shrinkPreviewCache;
    plantCopy.setName('Copy of ' + plantCopy.getName);
    if not inTrackMouse then
      plantCopy.moveBy(point(kPasteMoveDistance, 0));
    plantCopy.recalculateBounds(kDrawNow);
    newPlants.add(plantCopy);
    domain.plantManager.addPlant(plantCopy);
    MainForm.addSelectedPlant(plantCopy, kAddAtEnd);
    end;
  MainForm.updateForChangeToPlantList;
  end;

procedure PdDuplicateCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if newPlants.count <= 0 then exit;
  for i := 0 to newPlants.count - 1 do
    begin
    plant := PdPlant(newPlants.items[i]);
    domain.plantManager.plants.remove(plant);
    MainForm.removeSelectedPlant(plant);
    end;
  MainForm.updateForChangeToPlantList;
  end;

procedure PdDuplicateCommand.redoCommand;
  var
    i: smallint;
  begin
  inherited doCommand; 
  if newPlants.count <= 0 then exit;
  MainForm.deselectAllPlants;
  for i := 0 to newPlants.count - 1 do
    begin
    plant := PdPlant(newPlants.items[i]);
    domain.plantManager.addPlant(plant);
    MainForm.addSelectedPlant(plant, kAddAtEnd);
    end;
  MainForm.updateForChangeToPlantList;
  end;

function PdDuplicateCommand.description: string;
	begin
  result := 'duplicate' + plantNamesForDescription(plantList);
  end;

{ ----------------------------------------------------------------------- PdRandomizeCommand }
constructor PdRandomizeCommand.createWithListOfPlants(aList: TList);
  begin
  inherited createWithListOfPlants(aList);
  oldSeeds := TListCollection.create;
  oldBreedingSeeds := TListCollection.create;
  newSeeds := TListCollection.create;
  newBreedingSeeds := TListCollection.create;
  oldXRotations := TListCollection.create;
  newXRotations := TListCollection.create;
  self.setUpToRemoveAmendmentsWhenDone;
  end;

destructor PdRandomizeCommand.destroy;
  begin
  oldSeeds.free;
  oldSeeds := nil;
  oldBreedingSeeds.free;
  oldBreedingSeeds := nil;
  newSeeds.free;
  newSeeds := nil;
  newBreedingSeeds.free;
  newBreedingSeeds := nil;
  oldXRotations.free;
  oldXRotations := nil;
  newXRotations.free;
  newXRotations := nil;
  end;

procedure PdRandomizeCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand;
  try
    cursor_startWait;                     
    if not isInBreeder then
      self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      oldSeeds.add(PdSmallintValue.createWithSmallint(plant.pGeneral.startingSeedForRandomNumberGenerator));
      oldBreedingSeeds.add(PdLongintValue.createWithLongint(plant.breedingGenerator.seed));
      oldXRotations.add(PdSingleValue.createWithSingle(plant.xRotation));
      plant.randomize;
      newSeeds.add(PdSmallintValue.createWithSmallint(plant.pGeneral.startingSeedForRandomNumberGenerator));
      newBreedingSeeds.add(PdLongintValue.createWithLongint(plant.breedingGenerator.seed));
      newXRotations.add(PdSingleValue.createWithSingle(plant.xRotation));
      if isInBreeder then                           
        plant.previewCacheUpToDate := false
      else
        plant.recalculateBounds(kDrawNow);
      end;
    if isInBreeder then
      begin
      if plantList.count = 1 then
        begin
        plant := PdPlant(plantList.items[0]);
        BreederForm.updateForChangeToPlant(plant);
        end
      else
        BreederForm.updateForChangeToGenerations;
      end
    else
      begin
      self.invalidateCombinedPlantRects;
      MainForm.updateForChangeToPlantRotations;
      end;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdRandomizeCommand.undoCommand;
  var
    i: smallint;
    seed: smallint;
    breedingSeed: longint;
    xRotation: single;
  begin
  inherited undoCommand;
  try
    cursor_startWait;
    if not isInBreeder then
      self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      seed := PdSmallintValue(oldSeeds.items[i]).saveSmallint;
      breedingSeed := PdLongintValue(oldBreedingSeeds.items[i]).saveLongint;
      xRotation := PdSingleValue(oldXRotations.items[i]).saveSingle;
      plant.randomizeWithSeedsAndXRotation(seed, breedingSeed, xRotation);
      if isInBreeder then
        plant.previewCacheUpToDate := false
      else
        plant.recalculateBounds(kDrawNow);
      end;
    if isInBreeder then
      begin
      if plantList.count = 1 then
        begin
        plant := PdPlant(plantList.items[0]);
        BreederForm.updateForChangeToPlant(plant);
        end
      else
        BreederForm.updateForChangeToGenerations;
      end
    else
      begin
      self.invalidateCombinedPlantRects;
      MainForm.updateForChangeToPlantRotations;
      end;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdRandomizeCommand.redoCommand;
  var
    i: smallint;
    seed: smallint;
    breedingSeed: longint;
    xRotation: single;
  begin
  inherited doCommand;
  try
    cursor_startWait;
    if not isInBreeder then
      self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      seed := PdSmallintValue(newSeeds.items[i]).saveSmallint;
      breedingSeed := PdLongintValue(newBreedingSeeds.items[i]).saveLongint;
      xRotation := PdSingleValue(newXRotations.items[i]).saveSingle;
      plant.randomizeWithSeedsAndXRotation(seed, breedingSeed, xRotation);
      if isInBreeder then
        plant.previewCacheUpToDate := false
      else
        plant.recalculateBounds(kDrawNow);
      end;
    if isInBreeder then
      begin
      if plantList.count = 1 then
        begin
        plant := PdPlant(plantList.items[0]);
        BreederForm.updateForChangeToPlant(plant);
        end
      else
        BreederForm.updateForChangeToGenerations;
      end
    else
      begin
      self.invalidateCombinedPlantRects;
      MainForm.updateForChangeToPlantRotations;
      end;
  finally
    cursor_stopWait;
  end;
  end;

function PdRandomizeCommand.description: string;
	begin
  if isRandomizeAllInBreeder then
    result := 'randomize all in breeder'
  else if isInBreeder then
    result := 'randomize in breeder'
  else
    result := 'randomize' + plantNamesForDescription(plantList);
  end;

{ ----------------------------------------------------------- PdSendBackwardOrForwardCommand }
constructor PdSendBackwardOrForwardCommand.createWithBackwardOrForward(aBackward: boolean);
  begin
  inherited create;
  backward := aBackward;
  end;

procedure PdSendBackwardOrForwardCommand.doCommand;
  begin
  { assumption here is that selected plants list doesn't change between this command and undo }
  if backward then
    MainForm.moveSelectedPlantsDown
  else
    MainForm.moveSelectedPlantsUp;
  end;

procedure PdSendBackwardOrForwardCommand.undoCommand;
  begin
  if backward then
    MainForm.moveSelectedPlantsUp
  else
    MainForm.moveSelectedPlantsDown;
  end;

function PdSendBackwardOrForwardCommand.description: string;
  begin
  if backward then
    result := 'send backward in main window'
  else
    result := 'bring forward in main window';
  end;

{ ------------------------------------------------------------------------------- value change commands }
{ -------------------------------------------------------------------------------- PdChangeValueCommand }
constructor PdChangeValueCommand.createCommandWithListOfPlants(aList: TList; aFieldNumber: smallint; aRegrow: boolean);
  begin
  inherited createWithListOfPlants(aList);
  fieldNumber := aFieldNumber;
  regrow := aRegrow;
  if regrow then self.setUpToRemoveAmendmentsWhenDone;
  end;

function PdChangeValueCommand.description: string;
  var
    param: PdParameter;
  begin
  result := '';
  param := nil;
  { subclasses may want to call }
  if (domain <> nil) and (domain.parameterManager <> nil) then
    begin
    param := domain.parameterManager.parameterForFieldNumber(fieldNumber);
    if (param <> nil) then
      result := '"' + param.getName + '"';
    end;
  end;

{ ------------------------------------------------------------ PdChangeRealValueCommand }
constructor PdChangeRealValueCommand.createCommandWithListOfPlants(aList: TList; aNewValue: single;
    aFieldNumber, anArrayIndex: smallint; aRegrow: boolean);
  var
    oldValue: single;
    i: smallint;
	begin
  inherited createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
  newValue := aNewValue;
  arrayIndex := anArrayIndex;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.editTransferField(kGetField, oldValue, fieldNumber, kFieldFloat, arrayIndex, regrow);
    values.add(PdSingleValue.createWithSingle(oldValue));
    end;
  end;

procedure PdChangeRealValueCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand;
  try
    if regrow then cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.editTransferField(kSetField, newValue, fieldNumber, kFieldFloat, arrayIndex, regrow);
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
  finally
    if regrow then cursor_stopWait;
  end;
  end;

procedure PdChangeRealValueCommand.undoCommand;
  var
    oldValue: single;
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    oldValue := PdSingleValue(values.items[i]).saveSingle;
    plant.editTransferField(kSetField, oldValue, fieldNumber, kFieldFloat, arrayIndex, regrow);
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  end;

function PdChangeRealValueCommand.description: string;
	begin
  result := inherited description;
  result := 'change ' + result;
  if arrayIndex <> -1 then
    result := result + ' (' + intToStr(arrayIndex + 1) + ')';
  result := result + ' to ' + digitValueString(newValue) + ' in ' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdChangeSCurvePointValueCommand }
constructor PdChangeSCurvePointValueCommand.createCommandWithListOfPlants(aList: TList; aNewX, aNewY: single;
    aFieldNumber, aPointIndex: smallint; aRegrow: boolean);
  var
    oldX, oldY: single;
    i: smallint;
	begin
  inherited createCommandWithListOfPlants(aList, afieldNumber, aRegrow);
  newX := aNewX;
  newY := aNewY;
  pointIndex := aPointIndex;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.editTransferField(kGetField, oldX, fieldNumber, kFieldFloat, pointIndex * 2, regrow);
    plant.editTransferField(kGetField, oldY, fieldNumber, kFieldFloat, pointIndex * 2 + 1, regrow);
    values.add(PdSinglePointValue.createWithSingleXY(oldX, oldY));
    end;
  end;

procedure PdChangeSCurvePointValueCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand;
  try
    if regrow then cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      // first time, set values without calculating
      plant.changingWholeSCurves := true;
      plant.editTransferField(kSetField, newX, fieldNumber, kFieldFloat, pointIndex * 2, regrow);
      plant.editTransferField(kSetField, newY, fieldNumber, kFieldFloat, pointIndex * 2 + 1, regrow);
      // second time, now that both values are set, set first one again to calc s curve
      plant.changingWholeSCurves := false;
      plant.editTransferField(kSetField, newX, fieldNumber, kFieldFloat, pointIndex * 2, regrow);
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
  finally
    if regrow then cursor_stopWait;
  end;
  end;

procedure PdChangeSCurvePointValueCommand.undoCommand;
  var
    oldX, oldY: single;
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    oldX := PdSinglePointValue(values.items[i]).x;
    oldY := PdSinglePointValue(values.items[i]).y;
    plant.editTransferField(kSetField, oldX, fieldNumber, kFieldFloat, pointIndex * 2, regrow);
    plant.editTransferField(kSetField, oldY, fieldNumber, kFieldFloat, pointIndex * 2 + 1, regrow);
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  end;

function PdChangeSCurvePointValueCommand.description: string;
	begin
  result := inherited description;
  result := 'change ' + result + ' point ' + intToStr(pointIndex + 1)
    + ' to (' + digitValueString(newX) + ', ' + digitValueString(newY) + ')' + ' in ' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdChangeColorValueCommand }
constructor PdChangeColorValueCommand.createCommandWithListOfPlants(aList: TList; aNewValue: TColorRef;
    aFieldNumber, anArrayIndex: smallint; aRegrow: boolean);
  var
    oldValue: TColorRef;
    i: smallint;
	begin
  inherited createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
  newColor := aNewValue;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.editTransferField(kGetField, oldValue, fieldNumber, kFieldColor, kNotArray, regrow);
    values.add(PdColorValue.createWithColor(oldValue));
    end;
  end;

procedure PdChangeColorValueCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand;
  try
    if regrow then cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.editTransferField(kSetField, newColor, fieldNumber, kFieldColor, kNotArray, regrow);
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
  finally
    if regrow then cursor_stopWait;
  end;
  end;

procedure PdChangeColorValueCommand.undoCommand;
  var
    oldValue: TColorRef;
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    oldValue := PdColorValue(values.items[i]).saveColor;
    plant.editTransferField(kSetField, oldValue, fieldNumber, kFieldColor, kNotArray, regrow);
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  end;

function PdChangeColorValueCommand.description: string;
	begin
  result := inherited description;
  result := 'change ' + result
    + ' to (R ' + intToStr(getRValue(newColor))
    + ', G ' + intToStr(getGValue(newColor))
    + ', B ' + intToStr(getBValue(newColor)) + ')' + ' in ' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdChangeTdoValueCommand }
constructor PdChangeTdoValueCommand.createCommandWithListOfPlants(aList: TList; aNewValue: KfObject3D;
    aFieldNumber: smallint; aRegrow: boolean);
  var
    valueTdo: KfObject3D;
    i: smallint;
	begin
  inherited createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
  newTdo := KfObject3d.create;
  newTdo.copyFrom(aNewValue);
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    valueTdo := KfObject3D.create;
    plant := PdPlant(plantList.items[i]);
    plant.editTransferField(kGetField, valueTdo, fieldNumber, kFieldThreeDObject, kNotArray, regrow);
    values.add(valueTdo); 
    end;
  end;

destructor PdChangeTdoValueCommand.destroy;
  begin
  newTdo.free;
  newTdo := nil;
  { value tdos will be freed by values listCollection }
  inherited destroy;
  end;

procedure PdChangeTdoValueCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand;
  try
    if regrow then cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.editTransferField(kSetField, newTdo, fieldNumber, kFieldThreeDObject, kNotArray, regrow);
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
  finally
    if regrow then cursor_stopWait;
  end;
  end;

procedure PdChangeTdoValueCommand.undoCommand;
  var
    oldValue: KfObject3D;
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    oldValue := KfObject3D(values.items[i]);
    plant.editTransferField(kSetField, oldValue, fieldNumber, kFieldThreeDObject, kNotArray, regrow);
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  end;

function PdChangeTdoValueCommand.description: string;
	begin
  result := inherited description;
  result := 'change ' + result + ' to "' + newTdo.getName + '" in ' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdChangeSmallintValueCommand }
constructor PdChangeSmallintValueCommand.createCommandWithListOfPlants(aList: TList; aNewValue: smallint;
    aFieldNumber, anArrayIndex: smallint; aRegrow: boolean);
  var
    oldValue: smallint;
    i: smallint;
	begin
  inherited createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
  newValue := aNewValue;
  arrayIndex := anArrayIndex;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.editTransferField(kGetField, oldValue, fieldNumber, kFieldSmallint, arrayIndex, regrow);
    values.add(PdSmallintValue.createWithSmallint(oldValue));
    end;
  end;

procedure PdChangeSmallintValueCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand;
  try
    if regrow then cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.editTransferField(kSetField, newValue, fieldNumber, kFieldSmallint, arrayIndex, regrow);
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
  finally
    if regrow then cursor_stopWait;
  end;
  end;

procedure PdChangeSmallintValueCommand.undoCommand;
  var
    oldValue: smallint;
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    oldValue := PdSmallintValue(values.items[i]).saveSmallint;
    plant.editTransferField(kSetField, oldValue, fieldNumber, kFieldSmallint, arrayIndex, regrow);
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  end;

function PdChangeSmallintValueCommand.description: string;
	begin
  result := inherited description;
  result := 'change ' + result + ' to ' + IntToStr(newValue) + ' in ' + plantNamesForDescription(plantList);
  end;

{ ------------------------------------------------------------ PdChangeBooleanValueCommand }
constructor PdChangeBooleanValueCommand.createCommandWithListOfPlants(aList: TList; aNewValue: boolean;
    aFieldNumber, anArrayIndex: smallint; aRegrow: boolean);
  var
    oldValue: boolean;
    i: smallint;
	begin
  inherited createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
  newValue := aNewValue;
  arrayIndex := anArrayIndex;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    plant.editTransferField(kGetField, oldValue, fieldNumber, kFieldBoolean, arrayIndex, regrow);
    values.add(PdBooleanValue.createWithBoolean(oldValue));
    end;
  end;

procedure PdChangeBooleanValueCommand.doCommand;
   var
    i: smallint;
  begin
  inherited doCommand;
  try
    if regrow then cursor_startWait;
    self.invalidateCombinedPlantRects;
    if plantList.count > 0 then for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plant.editTransferField(kSetField, newValue, fieldNumber, kFieldBoolean, arrayIndex, regrow);
      plant.recalculateBounds(kDrawNow);
      end;
    self.invalidateCombinedPlantRects;
  finally
    if regrow then cursor_stopWait;
  end;
  end;

procedure PdChangeBooleanValueCommand.undoCommand;
  var
    oldValue: boolean;
    i: smallint;
  begin
  inherited undoCommand;
  self.invalidateCombinedPlantRects;
  if plantList.count > 0 then for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    oldValue := PdBooleanValue(values.items[i]).saveBoolean;
    plant.editTransferField(kSetField, oldValue, fieldNumber, kFieldBoolean, arrayIndex, regrow);
    plant.recalculateBounds(kDrawNow);
    end;
  self.invalidateCombinedPlantRects;
  end;

function PdChangeBooleanValueCommand.description: string;
  var
    newValueString: string[10];
	begin
  result := inherited description;
  if newValue then
    newValueString := 'yes'
  else
    newValueString := 'no';
  result := 'change ' + result + ' to ' + newValueString + ' in ' + plantNamesForDescription(plantList);
  end;

{ ---------------------------------------------------------------------------- PdBreedFromTwoParentsCommand }
constructor PdBreedFromParentsCommand.createWithInfo(existingGenerations: TListCollection;
    aFirstParent, aSecondParent: PdPlant; aRow: smallint; aFractionOfMaxAge: single; aCreateFirstGeneration: boolean);
  var
    i: smallint;
  begin
  inherited create;
  commandChangesPlantFile := false;
  firstParent := aFirstParent;
  if firstParent = nil then
    raise Exception.create('Problem: Need at least one parent in method PdBreedFromParentsCommand.createWithInfo.');
  secondParent := aSecondParent;
  fractionOfMaxAge := aFractionOfMaxAge;
  row := aRow;
  createFirstGeneration := aCreateFirstGeneration;
  if row < 0 then {from main window }
    row := BreederForm.selectedRow;
  oldGenerations := TList.create;
  if existingGenerations.count > 0 then for i := 0 to existingGenerations.count - 1 do
    oldGenerations.add(PdGeneration(existingGenerations.items[i]));
  end;

destructor PdBreedFromParentsCommand.destroy;
  var
    lastGeneration: PdGeneration;
  begin
  if done then { free all generations below row }
    begin
    while oldGenerations.count - 1 > row do
      begin
      lastGeneration := PdGeneration(oldGenerations.items[oldGenerations.count - 1]);
      oldGenerations.remove(lastGeneration);
      lastGeneration.free;
      end;
    end
  else { free new generation (and first generation if created, if not it will be nil) }
    begin
    firstGeneration.free;
    firstGeneration := nil;
    newGeneration.free;
    newGeneration := nil;
    end;
  oldGenerations.free;
  oldGenerations := nil;
  inherited destroy;
  end;

function PdBreedFromParentsCommand.numberOfStoredLargeObjects: longint;
  var
    i: smallint;
    generation: PdGeneration;
  begin
  result := 0;
  if done then
    begin
    if oldGenerations.count > 0 then for i := 0 to oldGenerations.count - 1 do
      begin
      generation := PdGeneration(oldGenerations.items[i]);
      result := result + generation.plants.count;
      end;
    end
  else
    begin
    if firstGeneration <> nil then
      result := firstGeneration.plants.count;
    if newGeneration <> nil then
      result := newGeneration.plants.count;
    end;
  end;

procedure PdBreedFromParentsCommand.doCommand;
  var
    generationBred: PdGeneration;
  begin
  inherited doCommand;
  try
    cursor_startWait;
    rowSelectedAtStart := BreederForm.selectedRow;
    { if command created from main window, create first generation to put in breeder }
    if createFirstGeneration then
      firstGeneration := PdGeneration.createWithParents(firstParent, secondParent, fractionOfMaxAge);
    { create generation that is outcome of breeding and do breeding }
    newGeneration := PdGeneration.create;
    newGeneration.breedFromParents(firstParent, secondParent, fractionOfMaxAge);
    { tell breeder to forget about other generations below the selected row  }
    BreederForm.forgetGenerationsListBelowRow(row);
    if firstGeneration <> nil then
      begin
      BreederForm.addGeneration(firstGeneration);
      BreederForm.selectGeneration(firstGeneration);
      end;
    BreederForm.updateForChangeToGenerations;
    { set the firstParent and secondParent pointers in the generation that was bred (either the firstGeneration
      or the generation selected in the breeder) }
    if row <= oldGenerations.count - 1 then
      begin
      generationBred := PdGeneration(oldGenerations.items[row]);
      generationBred.firstParent := generationBred.firstSelectedPlant;
      generationBred.secondParent := generationBred.secondSelectedPlant;
      end;
    { add and select the new generation in the breeder }
    BreederForm.addGeneration(newGeneration);
    BreederForm.selectGeneration(newGeneration);
    BreederForm.updateForChangeToGenerations;
  finally
    cursor_stopWait;
  end;
  end;

procedure PdBreedFromParentsCommand.undoCommand;
  var
    generationBred: PdGeneration;
  begin
  inherited undoCommand;
  { tell the breeder to forget about the generation(s) created by this command, and if there were any generations
    wiped out by it, tell the breeder to restore pointers to all generations that were forgotten }
  BreederForm.forgetLastGeneration;
  if firstGeneration <> nil then
    BreederForm.forgetLastGeneration;
  BreederForm.updateForChangeToGenerations;
  BreederForm.addGenerationsFromListBelowRow(row, oldGenerations);
  BreederForm.selectedRow := rowSelectedAtStart;
  { set parent pointers of generation that was bred (firstGeneration or generation selected) to nil }
  if row <= oldGenerations.count - 1 then
    begin
    generationBred := PdGeneration(oldGenerations.items[row]);
    generationBred.firstParent := nil;
    generationBred.secondParent := nil;
    end;
  BreederForm.updateForChangeToGenerations;
  end;

procedure PdBreedFromParentsCommand.redoCommand;
  var
    generationBred: PdGeneration;
  begin
  inherited doCommand;
  { tell breeder to forget about other generations below the selected row (the whole list if from the main window) }
  BreederForm.forgetGenerationsListBelowRow(row);
  if firstGeneration <> nil then
    begin
    BreederForm.addGeneration(firstGeneration);
    BreederForm.selectGeneration(firstGeneration);
    end;
  BreederForm.updateForChangeToGenerations;
  { set the firstParent and secondParent pointers in the generation that was bred (either the firstGeneration
    or the generation selected in the breeder) }
  if row <= oldGenerations.count - 1 then
    begin
    generationBred := PdGeneration(oldGenerations.items[row]);
    generationBred.firstParent := generationBred.firstSelectedPlant;
    generationBred.secondParent := generationBred.secondSelectedPlant;
    end;
  { add and select the new generation in the breeder }
  BreederForm.addGeneration(newGeneration);
  BreederForm.selectGeneration(newGeneration);
  BreederForm.updateForChangeToGenerations;
  end;

function PdBreedFromParentsCommand.description: string;
	begin
  if createFirstGeneration then // plant(s) from main window
    begin
    result := 'breed';
    if firstParent <> nil then result := result + ' "' + firstParent.getName + '"';
    if secondParent <> nil then result := result + ', "' + secondParent.getName + '"';
    end
  else
    result := 'breed from breeder row ' + intToStr(row + 1);
  end;

{ ------------------------------------------------------------------- PdReplaceBreederPlant }
constructor PdReplaceBreederPlant.createWithPlantRowAndColumn(aPlant: PdPlant; aRow, aColumn: smallint);
  begin
  inherited create;
  commandChangesPlantFile := false;
  plantDraggedFrom := aPlant;
  if plantDraggedFrom = nil then
    raise Exception.create('Problem: Nil plant dragged from in method PdReplaceBreederPlant.createWithPlantRowAndColumn.');
  row := aRow;
  column := aColumn;
  end;

destructor PdReplaceBreederPlant.destroy;
  begin
  if done then
    begin
    originalPlant.free;
    originalPlant := nil
    end
  else
    begin
    newPlant.free;
    newPlant := nil
    end;
  inherited destroy;
  end;

function PdReplaceBreederPlant.numberOfStoredLargeObjects: longint;
  begin
  result := 1;  {has one plant in either case (done or undone)}
  end;

procedure PdReplaceBreederPlant.doCommand;
  begin
  inherited doCommand;
  originalPlant := BreederForm.plantForRowAndColumn(row, column);
  if originalPlant = nil then
    raise Exception.create('Problem: Invalid row and column in method PdReplaceBreederPlant.doCommand.');
  newPlant := PdPlant.create;
  plantDraggedFrom.copyTo(newPlant);
  BreederForm.replacePlantInRow(originalPlant, newPlant, row);
  end;

procedure PdReplaceBreederPlant.undoCommand;
  begin
  inherited undoCommand;
  BreederForm.replacePlantInRow(newPlant, originalPlant, row);
  end;

procedure PdReplaceBreederPlant.redoCommand;
  begin
  inherited doCommand; 
  BreederForm.replacePlantInRow(originalPlant, newPlant, row);
  end;

function PdReplaceBreederPlant.description: string;
  begin
  result := 'replace breeder plant in row ' + intToStr(row + 1) + ', column ' + intToStr(column);
  end;

{ ------------------------------------------------------------------- PdMakeTimeSeriesCommand }
constructor PdMakeTimeSeriesCommand.createWithNewPlant(aNewPlant: PdPlant);
  begin
  inherited create;
  commandChangesPlantFile := false;
  newPlant := aNewPlant;
  if newPlant = nil then
    raise Exception.create('Problem: Nil plant in method PdMakeTimeSeriesCommand.createWithNewPlant.');
  oldPlants := TList.create;
  newPlants := TList.create;
  end;

destructor PdMakeTimeSeriesCommand.destroy;
  var i: smallint;
  begin
  if done then
    begin
    if (oldPlants <> nil) and (oldPlants.count > 0) then
      for i := 0 to oldPlants.count - 1 do
    	  PdPlant(oldPlants.items[i]).free;
    end
  else
    begin
    if (newPlants <> nil) and (newPlants.count > 0) then
      for i := 0 to newPlants.count - 1 do
    	  PdPlant(newPlants.items[i]).free;
    end;
  oldPlants.free;
  oldPlants := nil;
  newPlants.free;
  newPlants := nil;
  inherited destroy;
  end;

function PdMakeTimeSeriesCommand.numberOfStoredLargeObjects: longint;
  begin
  result := 0;
  if done then
    begin
    if oldPlants <> nil then
      result := oldPlants.count;
    end
  else
    begin
    if newPlants <> nil then
      result := newPlants.count;
    end;
  end;

procedure PdMakeTimeSeriesCommand.doCommand;
  var i: smallint;
  begin
  inherited doCommand;
  if TimeSeriesForm.plants.count > 0 then for i := 0 to TimeSeriesForm.plants.count - 1 do
    oldPlants.add(TimeSeriesForm.plants.items[i]);
  TimeSeriesForm.plants.clearPointersWithoutDeletingObjects;
  TimeSeriesForm.initializeWithPlant(newPlant, kDontDrawYet); //redraws in updateForChangeToPlants
  if TimeSeriesForm.plants.count > 0 then for i := 0 to TimeSeriesForm.plants.count - 1 do
    newPlants.add(TimeSeriesForm.plants.items[i]);
  TimeSeriesForm.updateForChangeToPlants(kRecalculateScale);
  end;

procedure PdMakeTimeSeriesCommand.undoCommand;
  var i: smallint;
  begin
  inherited undoCommand;
  TimeSeriesForm.plants.clearPointersWithoutDeletingObjects;
  if oldPlants.count > 0 then for i := 0 to oldPlants.count - 1 do
    TimeSeriesForm.plants.add(oldPlants.items[i]);
  TimeSeriesForm.updateForChangeToPlants(kDontRecalculateScale);
  end;

procedure PdMakeTimeSeriesCommand.redoCommand;
  var i: smallint;
  begin
  inherited doCommand; 
  TimeSeriesForm.plants.clearPointersWithoutDeletingObjects;
  if newPlants.count > 0 then for i := 0 to newPlants.count - 1 do
    TimeSeriesForm.plants.add(newPlants.items[i]);
  TimeSeriesForm.updateForChangeToPlants(kDontRecalculateScale);
  end;

function PdMakeTimeSeriesCommand.description: string;
  begin
  if isPaste then
    result := 'paste into time series window'
  else
    begin
    result := 'make time series';
    if newPlant <> nil then result := result + ' for plant "' + newPlant.getName + '"';
    end;
  end;

{ -------------------------------------------------------- PdChangeNumberOfTimeSeriesStagesCommand }
constructor PdChangeNumberOfTimeSeriesStagesCommand.createWithNewNumberOfStages(aNumber: smallint);
  begin
  inherited create;
  commandChangesPlantFile := false;
  newNumber := aNumber;
  oldNumber := domain.breedingAndTimeSeriesOptions.numTimeSeriesStages;
  end;

procedure PdChangeNumberOfTimeSeriesStagesCommand.doCommand;
  begin
  inherited doCommand;
  domain.breedingAndTimeSeriesOptions.numTimeSeriesStages := newNumber;
  TimeSeriesForm.updateForChangeToDomainOptions;
  end;

procedure PdChangeNumberOfTimeSeriesStagesCommand.undoCommand;
  begin
  inherited undoCommand;
  domain.breedingAndTimeSeriesOptions.numTimeSeriesStages := oldNumber;
  TimeSeriesForm.updateForChangeToDomainOptions;
  end;

function PdChangeNumberOfTimeSeriesStagesCommand.description: string;
	begin
  result := 'change number of time series stages';
  end;

{ -------------------------------------------------------- PdDeleteTimeSeriesCommand }
constructor PdDeleteTimeSeriesCommand.create;
  var
    i: smallint;
  begin
  plants := TListCollection.create;
  if TimeSeriesForm.plants.count > 0 then for i := 0 to TimeSeriesForm.plants.count - 1 do
    plants.add(TimeSeriesForm.plants.items[i]);
  end;

destructor PdDeleteTimeSeriesCommand.destroy;
  begin
  if not done then
    plants.clearPointersWithoutDeletingObjects;
  plants.free;
  plants := nil;
  inherited destroy;
  end;

function PdDeleteTimeSeriesCommand.numberOfStoredLargeObjects: longint;
  begin
  if done then
    result := plants.count
  else
    result := 0;
  end;

procedure PdDeleteTimeSeriesCommand.doCommand;
  begin
  inherited doCommand;
  TimeSeriesForm.plants.clearPointersWithoutDeletingObjects;
  TimeSeriesForm.updateForChangeToPlants(kDontRecalculateScale);
  end;

procedure PdDeleteTimeSeriesCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if plants.count > 0 then for i := 0 to plants.count - 1 do
    TimeSeriesForm.plants.add(plants.items[i]);
  TimeSeriesForm.updateForChangeToPlants(kDontRecalculateScale);
  end;

{redo same as do}
function PdDeleteTimeSeriesCommand.description: string;
  begin
  result := 'delete time series';
  end;

{ -------------------------------------------------------------- PdChangeBreederOptionsCommand }
constructor PdChangeBreedingAndTimeSeriesOptionsCommand.createWithOptionsAndDomainOptions(
    anOptions: BreedingAndTimeSeriesOptionsStructure; aDomainOptions: DomainOptionsStructure);
  begin
  inherited create;
  commandChangesPlantFile := false;
  newOptions := anOptions;
  oldOptions := domain.breedingAndTimeSeriesOptions;
  newDomainOptions := aDomainOptions;
  oldDomainOptions := domain.options;
  end;

procedure PdChangeBreedingAndTimeSeriesOptionsCommand.doCommand;
  begin
  inherited doCommand;
  domain.breedingAndTimeSeriesOptions := newOptions;
  domain.options := newDomainOptions;
  BreederForm.updateForChangeToDomainOptions;
  TimeSeriesForm.updateForChangeToDomainOptions;
  end;

procedure PdChangeBreedingAndTimeSeriesOptionsCommand.undoCommand;
  begin
  inherited undoCommand;
  domain.breedingAndTimeSeriesOptions := oldOptions;
  domain.options := oldDomainOptions;
  BreederForm.updateForChangeToDomainOptions;
  TimeSeriesForm.updateForChangeToDomainOptions;
  end;

{ redo is same as do }
function PdChangeBreedingAndTimeSeriesOptionsCommand.description: string;
	begin
  result := 'change breeding and time series options';
  end;

{ ------------------------------------------------------------------------ PdDeleteBreederGenerationCommand }
constructor PdDeleteBreederGenerationCommand.createWithGeneration(aGeneration: PdGeneration);
  begin
  inherited create;
  commandChangesPlantFile := false;
  generation := aGeneration;
  if generation = nil then
    raise Exception.create('Problem: Nil generation in method PdDeleteBreederGenerationCommand.createWithGeneration.');
  row := BreederForm.generations.indexOf(generation);
  if row < 0 then
    raise Exception.create('Problem: Generation not in list in method PdDeleteBreederGenerationCommand.createWithGeneration.');
  end;

destructor PdDeleteBreederGenerationCommand.destroy;
  begin
  if done then
    begin
    generation.free;
    generation := nil;
    end;
  inherited destroy;
  end;

function PdDeleteBreederGenerationCommand.numberOfStoredLargeObjects: longint;
  begin
  result := 0;
  if (done) and (generation <> nil) then
    result := generation.plants.count;
  end;

procedure PdDeleteBreederGenerationCommand.doCommand;
  var
    index: smallint;
  begin
  inherited doCommand;
  index := BreederForm.generations.indexOf(generation);
  BreederForm.generations.remove(generation);
  if index > 0 then BreederForm.selectedRow := index - 1;
  BreederForm.updateForChangeToGenerations;
  end;

procedure PdDeleteBreederGenerationCommand.undoCommand;
  begin
  inherited undoCommand;
  BreederForm.generations.insert(row, generation);
  BreederForm.selectedRow := BreederForm.generations.indexOf(generation);
  BreederForm.updateForChangeToGenerations;
  end;

function PdDeleteBreederGenerationCommand.description: string;
  begin
  result := 'delete breeder generation';
  end;

{ ------------------------------------------------------------------- PdDeleteAllBreederGenerationsCommand }
constructor PdDeleteAllBreederGenerationsCommand.create;
  var
    i: smallint;
  begin
  generations := TListCollection.create;
  if BreederForm.generations.count > 0 then for i := 0 to BreederForm.generations.count - 1 do
    generations.add(BreederForm.generations.items[i]);
  end;

destructor PdDeleteAllBreederGenerationsCommand.destroy;
  begin
  if not done then
    generations.clearPointersWithoutDeletingObjects;
  generations.free;
  generations := nil;
  inherited destroy;
  end;

function PdDeleteAllBreederGenerationsCommand.numberOfStoredLargeObjects: longint;
  var
    i: smallint;
    generation: PdGeneration;
  begin
  result := 0;
  if done then
    begin
    if generations.count > 0 then for i := 0 to generations.count - 1 do
      begin
      generation := PdGeneration(generations.items[i]);
      result := result + generation.plants.count;
      end;
    end;
  end;

procedure PdDeleteAllBreederGenerationsCommand.doCommand;
  begin
  inherited doCommand;
  BreederForm.generations.clearPointersWithoutDeletingObjects;
  BreederForm.updateForChangeToGenerations;
  end;

procedure PdDeleteAllBreederGenerationsCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if generations.count > 0 then for i := 0 to generations.count - 1 do
    BreederForm.generations.add(generations.items[i]);
  BreederForm.updateForChangeToGenerations;
  end;

{redo same as do}
function PdDeleteAllBreederGenerationsCommand.description: string;
  begin
  result := 'delete all breeder generations';
  end;

begin
numPlantsCreatedThisSession := 0;
end.


