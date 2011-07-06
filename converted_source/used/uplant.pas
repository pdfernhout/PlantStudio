unit Uplant;

interface

uses WinTypes, Classes, Graphics,
  utdo, urandom, ucollect, umath, uturtle, ufiler, uparams, ubitmap, usupport, uamendmt;
 
const
	kGenderMale = 0; kGenderFemale = 1;
	kCompoundLeafPinnate = 0; kCompoundLeafPalmate = 1;
  kArrangementAlternate = 0; kArrangementOpposite = 1;
  kStageFlowerBud = 1; kStageOpenFlower = 2; kStageUnripeFruit = 3; kStageRipeFruit = 4;
  kPartTypeNone = 0; kPartTypeFlowerFruit = 1; kPartTypeInflorescence = 2; kPartTypeMeristem = 3;
    kPartTypePhytomer = 4; kPartTypeLeaf = 5; 
  kDirectionLeft = 0; kDirectionRight = 1;
  kGetField = 0; kSetField = 1;
  kPlantNameLength = 80;
  kCheckForUnreadParams = true; kDontCheckForUnreadParams = false;
  kConsiderDomainScale = true; kDontConsiderDomainScale = false;
  kDrawNow = true; kDontDrawNow = false;
  kMutation = 0; kWeight = 1;
  kMaxBreedingSections = 20;
  kFromFirstPlant = 0; kFromSecondPlant = 1;
  kFromProbabilityBasedOnWeightsForSection = 2;
  kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant = 3;
  kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant = 4;
  kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly = 5;
  kPlantAsTextStartString = 'start PlantStudio plant';
  kPlantAsTextEndString = 'end PlantStudio plant';
  kStartNoteString = '=== start note';
  kEndNoteString = '=== end note';
  kInMainWindow = true; kNotInMainWindow = false;

  kBud = 0; kPistils = 1; kStamens = 2;
  kFirstPetals = 3; kSecondPetals = 4; kThirdPetals = 5; kFourthPetals = 6; kFifthPetals = 7;
  kSepals = 8;
  kHighestFloralPartConstant = kSepals;
  kDrawNoBud = 0; kDrawSingleTdoBud = 1; kDrawOpeningFlower = 2;
  kNotExactAge = false; kExactAge = true;

type

  BreedingAndTimeSeriesOptionsStructure = record
    mutationStrengths: array[0..kMaxBreedingSections] of smallint;
    firstPlantWeights: array[0..kMaxBreedingSections] of smallint;
    getNonNumericalParametersFrom: smallint;
    mutateAndBlendColorValues: boolean;
    chooseTdosRandomlyFromCurrentLibrary: boolean;
    percentMaxAge: smallint;
    // v2.0
    plantsPerGeneration: smallint;
    variationType: smallint;
    thumbnailWidth: smallint;                 
    thumbnailHeight: smallint;
    maxGenerations: smallint;
    numTimeSeriesStages: smallint;
    end;

  TdoParamsStructure = record
    object3D: KfObject3D;
    xRotationBeforeDraw: single;
    yRotationBeforeDraw: single;
    zRotationBeforeDraw: single;
    faceColor: TColorRef;
    backfaceColor: TColorRef;
    alternateFaceColor: TColorRef;     // alternate colors used only for fruit, so far - ripe vs. unripe
    alternateBackfaceColor: TColorRef;
    scaleAtFullSize: single;
    repetitions: smallint;
    radiallyArranged: boolean;
    pullBackAngle: single;
    end;

{ params->start }
{ access->pGeneral }
ParamsGeneral = record
  randomSway: single;
  startingSeedForRandomNumberGenerator: smallint; {was longint, but want it in a param panel}
  numApicalInflors: smallint;
  numAxillaryInflors: smallint;
  lineDivisions: smallint;
  isDicot: boolean;
  maleFlowersAreSeparate: boolean;
  ageAtMaturity: smallint;
  growthSCurve: SCurveStructure;
  ageAtWhichFloweringStarts: smallint;
  fractionReproductiveAllocationAtMaturity_frn: single;
  wiltingPercent: single; {NA} {not using yet}
  phyllotacticRotationAngle: single;
  end;

{ access->pLeaf }
ParamsLeaf = record
  leafTdoParams: TdoParamsStructure;
  stipuleTdoParams: TdoParamsStructure;
  sCurveParams: SCurveStructure;
  petioleColor: TColorRef;
  optimalBiomass_pctMPB: single;
  optimalFractionOfOptimalBiomassAtCreation_frn: single;
  minDaysToGrow: smallint;
  maxDaysToGrow: smallint;
  petioleLengthAtOptimalBiomass_mm: single;
  petioleWidthAtOptimalBiomass_mm: single;
  petioleAngle: single;
  compoundRachisToPetioleRatio: single;
  compoundPinnateOrPalmate: smallint{ENUM};
  compoundNumLeaflets: smallint;
  compoundCurveAngleAtStart: single;
  compoundCurveAngleAtFullSize: single;
  fractionOfLiveBiomassWhenAbscisses_frn: single;
  petioleTaperIndex: smallint;
  compoundPinnateLeafletArrangement: smallint;
  end;

{ access->pSeedlingLeaf }
ParamsSeedlingLeaf = record
  leafTdoParams: TdoParamsStructure;
  nodesOnStemWhenFallsOff: smallint;
  end;

{ access->pInternode }
ParamsInternode = record
  faceColor: TColorRef;
  backfaceColor: TColorRef;
  curvingIndex: single;
  firstInternodeCurvingIndex: single;
  { creation }
  minFractionOfOptimalInitialBiomassToCreateInternode_frn: single;
  minDaysToCreateInternode: smallint;
  maxDaysToCreateInternodeIfOverMinFraction: smallint;
  { growth and expansion }
  optimalFinalBiomass_pctMPB: single;
  canRecoverFromStuntingDuringCreation: boolean;
  minDaysToAccumulateBiomass: smallint;
  maxDaysToAccumulateBiomass: smallint;
  minDaysToExpand: smallint;
  maxDaysToExpand: smallint;
  lengthAtOptimalFinalBiomassAndExpansion_mm: single;
  lengthMultiplierDueToBiomassAccretion: single;
  lengthMultiplierDueToExpansion: single;
  widthAtOptimalFinalBiomassAndExpansion_mm: single;
  widthMultiplierDueToBiomassAccretion: single;
  widthMultiplierDueToExpansion: single;
  { bolting }
  lengthMultiplierDueToBolting: single;
  minDaysToBolt: smallint;
  maxDaysToBolt: smallint;
  end;

{ access->pFlower }
ParamsFlower = record
  //kBud = 0; kPistil = 1; kStamens = 2; kFirstPetals = 3; kSecondPetals = 4; kThirdPetals = 5; kSepals = 6;
  tdoParams: array[kBud..kSepals] of TdoParamsStructure;
  budDrawingOption: smallint;
  optimalBiomass_pctMPB: single;
  minFractionOfOptimalInitialBiomassToCreateFlower_frn: single;
  minDaysToCreateFlowerBud: smallint;
  maxDaysToCreateFlowerBudIfOverMinFraction: smallint;
  minFractionOfOptimalBiomassToOpenFlower_frn: single;
  minDaysToOpenFlower: smallint;
  minDaysToGrow: smallint;
  maxDaysToGrowIfOverMinFraction: smallint;
  minDaysBeforeSettingFruit: smallint;
  daysBeforeDrop: smallint;
  minFractionOfOptimalBiomassToCreateFruit_frn: single;
  numPistils: smallint;
  styleLength_mm: single;
  styleWidth_mm: single;
  styleTaperIndex: smallint;
  styleColor: TColorRef;
  numStamens: smallint;
  filamentLength_mm: single;
  filamentWidth_mm: single;
  filamentTaperIndex: smallint;
  filamentColor: TColorRef;
  end;

{ access->pInflor }
ParamsInflorescence = record
  bractTdoParams: TdoParamsStructure;
  optimalBiomass_pctMPB: single;
  minFractionOfOptimalBiomassToCreateInflorescence_frn: single;
  minDaysToCreateInflorescence: smallint;
  maxDaysToCreateInflorescenceIfOverMinFraction: smallint;
  minFractionOfOptimalBiomassToMakeFlowers_frn: single;
  minDaysToGrow: smallint;
  maxDaysToGrow: smallint;
  peduncleLength_mm: single;
  internodeLength_mm: single;
  internodeWidth_mm: single;
  pedicelLength_mm: single;
  pedicelAngle: single;
  branchAngle: single;
  angleBetweenInternodes: single;
  peduncleAngleFromVegetativeStem: single;
  apicalStalkAngleFromVegetativeStem: single;
  terminalStalkLength_mm: single;
  numFlowersPerBranch: smallint;
  numFlowersOnMainBranch: smallint;
  daysToAllFlowersCreated: smallint;
  numBranches: smallint;
  branchesAreAlternate: boolean;
  isHead: boolean;
  isTerminal: boolean;
  flowersDrawTopToBottom: boolean;
  flowersSpiralOnStem: boolean;
  stalkColor: TColorRef;
  pedicelColor: TColorRef;
  pedicelTaperIndex: smallint;
  end;

{ access->pAxillaryBud }
ParamsAxillaryBud = record
  tdoParams: TdoParamsStructure;
  end;

{ access->pMeristem }
ParamsMeristem = record
  branchingIndex: single;
  branchingDistance: single;
  branchingAngle: single;
  determinateProbability: single;
  branchingIsSympodial: boolean;
  branchingAndLeafArrangement: smallint;
  secondaryBranchingIsAllowed: boolean;
  end;

{ access->pFruit }
ParamsFruit = record
  tdoParams: TdoParamsStructure;
  sCurveParams: SCurveStructure;
  optimalBiomass_pctMPB: single;
  minDaysToGrow: smallint;
  maxDaysToGrow: smallint;
  stalkStrengthIndex: single;
  daysToRipen: smallint;
  end;

{ access->pRoot }
ParamsRoot = record
  tdoParams: TdoParamsStructure;
  showsAboveGround: boolean;
  end;
{ aspects->stop }

PdPlant = class(PdStreamableObject)
  public
  { graphical }
  name: string[kPlantNameLength];
  age: smallint;
  basePoint_mm: SinglePoint;
  xRotation, yRotation, zRotation: single;
  drawingScale_PixelsPerMm: single;
  previewCache: PdBitmap;
  drawingIntoPreviewCache, previewCacheUpToDate: boolean;
  randomNumberGenerator: PdRandom;
  breedingGenerator: PdRandom;
  { parameters }
  pGeneral: ParamsGeneral;
  pMeristem: ParamsMeristem;
  pInternode: ParamsInternode;
  pLeaf: ParamsLeaf;
  pSeedlingLeaf: ParamsSeedlingLeaf;
  pAxillaryBud: ParamsAxillaryBud;
  pInflor: array[0..1] of ParamsInflorescence;
  pFlower: array[0..1] of ParamsFlower;
  pFruit: ParamsFruit;
  pRoot: ParamsRoot;
  selectedWhenLastSaved: boolean;
  hidden: boolean;
  { all vars following don't need to be saved in the plant file (but should be copied when streaming) }
  computeBounds: boolean;
  fixedPreviewScale, justCopiedFromMainWindow: boolean;
  fixedDrawPosition: boolean;
  drawPositionIfFixed: TPoint;
  normalBoundsRect_pixels: TRect;
  indexWhenRemoved: smallint;
  selectedIndexWhenRemoved: smallint;
  needToRecalculateColors: boolean;
  ageOfYoungestPhytomer: smallint;
  writingToMemo: boolean;
  readingFromMemo: boolean;
  readingMemoLine: longint;
  useBestDrawingForPreview: boolean;
  { pointers }
  turtle: KfTurtle;
  firstPhytomer: TObject;
  { biomass and flowering }
  totalBiomass_pctMPB: single;
  reproBiomass_pctMPB: single;
  shootBiomass_pctMPB: single;
  changeInShootBiomassToday_pctMPB: single;
  changeInReproBiomassToday_pctMPB: single;
  ageAtWhichFloweringStarted: smallint;
  floweringHasStarted: boolean;
  totalPlantParts: longint;
  partsCreated: longint;  // v1.6b1
  total3DExportPoints: longint;
  total3DExportTriangles: longint;
  total3DExportMaterials: longint;
  { accounting variables }
  unallocatedNewVegetativeBiomass_pctMPB: single;
  unremovedDeadVegetativeBiomass_pctMPB: single;
  unallocatedNewReproductiveBiomass_pctMPB: single;
  unremovedDeadReproductiveBiomass_pctMPB: single;
  unremovedStandingDeadBiomass_pctMPB: single;
  numApicalActiveReproductiveMeristemsOrInflorescences: longint;
  numAxillaryActiveReproductiveMeristemsOrInflorescences: longint;
  numApicalInactiveReproductiveMeristems: longint;
  numAxillaryInactiveReproductiveMeristems: longint;
  { used in parameter changes }
  wholePlantUpdateNeeded: boolean;
  plantPartsDrawnAtStart: longint;
  changingWholeSCurves: boolean;
  noteLines: TStringList;
  amendments: TListCollection;
  totalMemoryUsed_K: extended;
  constructor create; override;
  destructor destroy; override;
  procedure initialize3DObjects;
  function getName: string;
  function getHint(point: TPoint): string;
  procedure regrow;
  procedure reset;
  procedure setAge(newAge: smallint);
  procedure setName(newName: string);
  procedure initializeCache(cache: PdBitmap);
  procedure enforceMinimumBoundsRect;
  procedure moveTo(const aPoint_pixels: TPoint);
  procedure moveBy(delta_pixels: TPoint);
  procedure expandBoundsRectForLineWidth;
  function includesPoint(const aPoint: TPoint): boolean;
  function boundsRectIncludesPoint(const aPoint: TPoint; boundsRect: TRect; checkResizeRect: boolean): boolean;
  function pointInBoundsRect(const aPoint: TPoint): boolean;
  function pointColorMatch(xPixel, yPixel: longint): boolean;
  function pointColorAdjacentMatch(xPixel, yPixel, position: longint): boolean;
  procedure countPlantParts;
  procedure countPlantPartsFor3DOutput(outputType, stemCylinderFaces: smallint);
  function hangingObjectsMemoryUse_K: extended;
  function tdoMemoryUse_K: extended;
  function calculateTotalMemorySize: extended;
  procedure drawOn(destCanvas: TCanvas);
  procedure setTurtleDrawOptionsForNormalDraw(turtle: KfTurtle);
  //procedure drawOnUsingOpenGL(turtle: KfTurtle; selected, firstSelected: boolean);
  procedure recalculateBounds(drawNow: boolean);
  procedure recalculateBoundsForOffsetChange;
  procedure fakeDrawToGetBounds;
  procedure drawIntoCache(cache: PdBitmap; size: TPoint; considerDomainScale, immediate: boolean);
  procedure drawPreviewIntoCache(size: TPoint; considerDomainScale, immediate: boolean);
  procedure resizeCacheIfNecessary(cache: PdBitmap; size: TPoint; inMainWindow: boolean);
  procedure setTurtleUpForPreview(scale: single; drawPosition: TPoint);
  procedure setTurtleUpForPreviewScratch(scale: single; drawPosition: TPoint);
  function getTurtleBoundsRect: TRect;
  function resizingRect: TRect;
  function pointIsInResizingRect(point: TPoint): boolean;
  procedure draw;
  procedure saveToGlobal3DOutputFile(indexOfPlant: smallint; translate: boolean; rectWithAllPlants: TRect;
      outputType: smallint; aTurtle: KfTurtle);
  procedure setUpTurtleFor3DOutput;
  function maximumLineWidth: single;
  procedure randomize;
  procedure randomizeWithSeedsAndXRotation(generalSeed: smallint; breedingSeed: longint; anXRotation: single);
  procedure useBreedingOptionsAndPlantsToSetParameters(options: BreedingAndTimeSeriesOptionsStructure;
    firstPlant, secondPlant: PdPlant; tdos: TListCollection);
  function pickPlantToCopyNonNumericalParameterFrom(options: BreedingAndTimeSeriesOptionsStructure;
    sectionIndex: smallint): smallint;
  function blendAndMutateColors(options: BreedingAndTimeSeriesOptionsStructure; sectionIndex: smallint;
    haveSecondPlant: boolean; firstColor, secondColor: TColorRef): TColorRef;
  function tdoRandomlyPickedFromCurrentLibrary(tdos: TListCollection): KfObject3D;
  procedure writeToPlantFile(var plantFile: TextFile);
  procedure readLineAndTdoFromPlantFile(aLine: string; var plantFile: TextFile);
  procedure finishLoadingOrDefaulting(checkForUnreadParams: boolean);
  procedure defaultAllParameters;
  procedure defaultParameter(param: PdParameter; writeDebugMessage: boolean);
  procedure editTransferField(d: integer; var value; fieldID, fieldType, fieldIndex: integer; regrow: boolean);
  procedure transferField(d: integer; var v; fieldID, ft, index: smallint; regrow: boolean; updateList: TListCollection);
  procedure transferWholeSCurve(direction: smallint; var value: SCurveStructure; fieldNumber, fieldType: smallint;
    regrow: boolean; updateList: TListCollection);
  class procedure fillEnumStringList(var list: TStringList; fieldID: Integer; var hasRadioButtons: boolean);
  procedure directTransferField(d: integer; var v; fieldID, ft, index: smallint; updateList: TListCollection);
  procedure addToUpdateList(fieldID: integer; updateList: TListCollection);
  procedure MFD(var objectValue; var value; fieldType: integer; direction: integer);
  procedure transferObject3D(direction: integer; myTdo: KfObject3D; otherTdo: KfObject3D);
  function realDrawingScale_pixelsPerMm: single;
  function basePoint_pixels: TPoint;
  procedure setBasePoint_pixels(aPoint_pixels: TPoint);
  function boundsRect_pixels: TRect;
  procedure setBoundsRect_pixels(aRect_pixels: TRect);
  procedure freeAllDrawingPlantParts;
  procedure free3DObjects;
  procedure nextDay;
  procedure allocateOrRemoveBiomassWithTraverser(traverserProxy: TObject);
  procedure allocateOrRemoveParticularBiomass(biomassToAddOrRemove_pctMPB: single;
    var undistributedBiomass_pctMPB: single; askingMode, tellingMode: integer; traverserProxy: TObject);
  function findPlantPartAtPositionByTestingPolygons(point: TPoint): TObject;
  function plantPartForPartID(partID: longint): TObject;
  procedure getInfoForPlantPartAtPoint(point: TPoint; var partID: longint; var partType: string);
  function colorForDXFPartType(index: smallint): TColorRef;
  procedure getPlantStatistics(statisticsProxy: TObject);
  procedure report;
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  procedure shrinkPreviewCache;
  procedure calculateDrawingScaleToFitSize(size: TPoint);
  procedure calculateDrawingScaleToLookTheSameWithDomainScale;
  procedure writeToMainFormMemoAsText;
  procedure writeLine(var plantFile: TextFile; aString: string);
  function amendmentForPartID(partID: longint): PdPlantDrawingAmendment;
  procedure addAmendment(newAmendment: PdPlantDrawingAmendment);
  procedure removeAmendment(oldAmendment: PdPlantDrawingAmendment);
  procedure removeAllAmendments;
  procedure clearPointersToAllAmendments;
  procedure restoreAmendmentPointersToList(aList: TList);
  end;

PdPlantUpdateEvent = class
  public
  plant: PdPlant;
  fieldID: integer;
  fieldIndex: integer;
  end;

implementation

uses WinProcs, SysUtils, ClipBrd, Dialogs, 
  udebug, udomain, umain, u3dexport,
  utravers, upart, umerist, uintern, utransfr, uclasses, usection, utimeser, ucursor, ubmpsupport;

{ -------------------------------------------------------------------------------------- creation/destruction }
constructor PdPlant.create;
  begin
  inherited create;
  turtle := nil;
  firstPhytomer := nil;
  previewCache := PdBitmap.create;
  self.initializeCache(previewCache);
  self.randomNumberGenerator := PdRandom.create;
  self.breedingGenerator := PdRandom.create;
  self.amendments := TListCollection.create;
  breedingGenerator.setSeed(breedingGenerator.randomSeedFromTime);
  noteLines := TStringList.create;
  self.initialize3DObjects;
  drawingScale_PixelsPerMm := 1.0;
  // not using the internode water expansion code this version, meaningless, no water stress, need these
  // these twos mean internodes are hard-coded to increase in width and height twice (from defaults in params.tab)
  pInternode.lengthMultiplierDueToBiomassAccretion := 2.0;
  pInternode.widthMultiplierDueToBiomassAccretion := 2.0;
  pInternode.lengthMultiplierDueToExpansion := 1.0;
  pInternode.widthMultiplierDueToExpansion := 1.0;
  partsCreated := 0; // v1.6b1
  end;

procedure PdPlant.initialize3DObjects;
  var partType: integer;
  begin
  { i think it is best to create these at plant creation, then read into existing ones. }
  pSeedlingLeaf.leafTdoParams.object3D := KfObject3D.create;
  pLeaf.leafTdoParams.object3D := KfObject3D.create;
  pLeaf.stipuleTdoParams.object3D := KfObject3D.create;
  pInflor[kGenderFemale].bractTdoParams.object3D := KfObject3D.create;
  pInflor[kGenderMale].bractTdoParams.object3D := KfObject3D.create;
  for partType := 0 to kHighestFloralPartConstant do
    begin
    pFlower[kGenderFemale].tdoParams[partType].object3D := KfObject3D.create;
    pFlower[kGenderMale].tdoParams[partType].object3D := KfObject3D.create;
    end;
  pAxillaryBud.tdoParams.object3D := KfObject3D.create;
  pFruit.tdoParams.object3D := KfObject3D.create;
  pRoot.tdoParams.object3D := KfObject3D.create;
  end;

destructor PdPlant.destroy;
	begin
  previewCache.free; previewCache := nil;
  randomNumberGenerator.free; randomNumberGenerator := nil;
  breedingGenerator.free; breedingGenerator := nil;
  amendments.free; amendments := nil;
  noteLines.free; noteLines := nil;
  self.free3DObjects;
  self.freeAllDrawingPlantParts;
  inherited destroy;
  end;

procedure PdPlant.freeAllDrawingPlantParts;
  var
    traverser: PdTraverser;
  begin
  if (firstPhytomer <> nil) then
    begin
    traverser := PdTraverser.createWithPlant(self);
    traverser.traverseWholePlant(kActivityFree);
    traverser.free;
    firstPhytomer := nil;
    partsCreated := 0; // v1.6b1
    end;
  end;

procedure PdPlant.initializeCache(cache: PdBitmap);
  begin
  // giving the cache a tiny size at creation forces it to create its canvas etc
  // without this there is a nil pointer at streaming which causes a problem
  cache.width := 1;
  cache.height := 1;
  cache.transparent := true;
  cache.transparentMode := tmFixed;
  cache.transparentColor := domain.options.backgroundColor;
  end;

procedure PdPlant.free3DObjects;
  var partType: integer;
  begin
  pSeedlingLeaf.leafTdoParams.object3D.free; pSeedlingLeaf.leafTdoParams.object3D := nil;
  pLeaf.leafTdoParams.object3D.free; pLeaf.leafTdoParams.object3D := nil;
  pLeaf.stipuleTdoParams.object3D.free; pLeaf.stipuleTdoParams.object3D := nil;
  pInflor[kGenderFemale].bractTdoParams.object3D.free; pInflor[kGenderFemale].bractTdoParams.object3D := nil;
  pInflor[kGenderMale].bractTdoParams.object3D.free; pInflor[kGenderMale].bractTdoParams.object3D := nil;
  for partType := 0 to kHighestFloralPartConstant do
    begin
    with pFlower[kGenderFemale].tdoParams[partType] do
      begin
      object3D.free;
      object3D := nil;
      end;
    with pFlower[kGenderMale].tdoParams[partType] do
      begin
      object3D.free;
      object3D := nil;
      end;
    end;
  pAxillaryBud.tdoParams.object3D.free; pAxillaryBud.tdoParams.object3D := nil;
  pFruit.tdoParams.object3D.free; pFruit.tdoParams.object3D := nil;
  pRoot.tdoParams.object3D.free; pRoot.tdoParams.object3D := nil;
  end;

function PdPlant.getName: string;
  begin
  result := self.name;
  end;

procedure PdPlant.setName(newName: string);
  begin
  name := copy(newName, 1, kPlantNameLength);
  end;

{ ----------------------------------------------------------------------------------------- age management }
procedure PdPlant.regrow;
  begin
  self.setAge(self.age);
  end;

procedure PdPlant.reset;
  begin
  age := 0;
  self.freeAllDrawingPlantParts;
  totalBiomass_pctMPB := 0.0;
  reproBiomass_pctMPB := 0.0;
  shootBiomass_pctMPB := 0.0;
  changeInShootBiomassToday_pctMPB := 0.0;
  changeInReproBiomassToday_pctMPB := 0.0;
  floweringHasStarted := false;
  totalPlantParts := 0;
  ageAtWhichFloweringStarted := 0;
  numApicalActiveReproductiveMeristemsOrInflorescences := 0;
  numAxillaryActiveReproductiveMeristemsOrInflorescences := 0;
  numApicalInactiveReproductiveMeristems := 0;
  numAxillaryInactiveReproductiveMeristems := 0;
  unallocatedNewVegetativeBiomass_pctMPB := 0.0;
  unremovedDeadVegetativeBiomass_pctMPB := 0.0;
  unallocatedNewReproductiveBiomass_pctMPB := 0.0;
  unremovedDeadReproductiveBiomass_pctMPB := 0.0;
  unremovedStandingDeadBiomass_pctMPB := 0.0;
  ageOfYoungestPhytomer := 0;
  needToRecalculateColors := true;
  randomNumberGenerator.setSeedFromSmallint(pGeneral.startingSeedForRandomNumberGenerator);
  end;

procedure PdPlant.setAge(newAge: smallint);
  begin
  newAge := intMax(0, intMin(pGeneral.ageAtMaturity, newAge));
  try
    cursor_startWait;
    self.reset;
    while age < newAge do
      self.nextDay;
  finally
    cursor_stopWait;
  end;
  end;

{ ---------------------------------------------------------------------------------------  drawing and graphics }
procedure PdPlant.draw;
  var
    traverser: PdTraverser;
  begin
  cancelDrawing := false;
  if (turtle = nil) then
    raise exception.create('Problem: Nil turtle in method PdPlant.draw.');
  if turtle.drawingSurface.pane <> nil then
    begin
    turtle.drawingSurface.pane.brush.style := bsSolid;
    turtle.drawingSurface.pane.pen.style := psSolid;
    end;
  turtle.setLineColor(clGreen);
  turtle.push;
  turtle.rotateZ(64);
  turtle.rotateX(xRotation * 256 / 360);
  turtle.rotateY(yRotation * 256 / 360);  { convert here from 360 degrees to 256 turtle degrees }
  turtle.rotateZ(zRotation * 256 / 360);
  turtle.drawingSurface.lineColor := clGreen;
  if (firstPhytomer <> nil) then
    begin
    traverser := PdTraverser.createWithPlant(self);
    try
      traverser.plantPartsDrawnAtStart := self.plantPartsDrawnAtStart;
      // if not drawing 3D objects, probably drawing just to get bounds
      traverser.showDrawingProgress := turtle.drawOptions.draw3DObjects;
      traverser.traverseWholePlant(kActivityDraw);
    finally
      traverser.free;
      traverser := nil;
    end;
    end;
  turtle.pop;
  { recalculating colors occurs during drawing of leaves and internodes if necessary }
  self.needToRecalculateColors := false;
  end;

procedure PdPlant.countPlantParts;
  var
    traverser: PdTraverser;
  begin
  self.totalPlantParts := 0;
  if (firstPhytomer <> nil) then
    begin
    traverser := PdTraverser.createWithPlant(self);
    try
      traverser.traverseWholePlant(kActivityCountPlantParts);
      self.totalPlantParts := traverser.totalPlantParts;
    finally
      traverser.free;
      traverser := nil;
    end;
    end;
  end;

procedure PdPlant.countPlantPartsFor3DOutput(outputType, stemCylinderFaces: smallint);
  var
    traverser: PdTraverser;
    i: smallint;
  begin
  if (firstPhytomer <> nil) then
    begin
    traverser := PdTraverser.createWithPlant(self);
    try
      traverser.traverseWholePlant(kActivityCountPointsAndTrianglesFor3DExport);
      self.totalPlantParts := traverser.totalPlantParts;
      case outputType of
        kPOV: // POV does not use polygon cylinders for lines; it draws them directly
          begin
          self.total3DExportPoints := traverser.total3DExportPointsIn3DObjects
            + traverser.total3DExportStemSegments * pGeneral.lineDivisions * 2;
          self.total3DExportTriangles := traverser.total3DExportTrianglesIn3DObjects;
          end;
        else // for every output type that uses cylinders made of triangles
          begin
          self.total3DExportPoints := traverser.total3DExportPointsIn3DObjects
            + (traverser.total3DExportStemSegments * (pGeneral.lineDivisions + 1) * stemCylinderFaces);
          self.total3DExportTriangles := traverser.total3DExportTrianglesIn3DObjects
            + (traverser.total3DExportStemSegments * pGeneral.lineDivisions * stemCylinderFaces * 2);
          end;
        end;
      // this is only important for LWO and OBJ, but people will like to see it anyway
      self.total3DExportMaterials := 0;
      for i := 0 to kExportPartLast do if traverser.exportTypeCounts[i] > 0 then inc(self.total3DExportMaterials);
    finally
      traverser.free;
      traverser := nil;
    end;
    end;
  end;

function PdPlant.calculateTotalMemorySize: extended;
  var
    traverser: PdTraverser;
  begin
  result := self.instanceSize / 1024.0;
  result := result + self.hangingObjectsMemoryUse_K;
  result := result + self.tdoMemoryUse_K;
  // preview cache
  if previewCache <> nil then result := result + BitmapMemorySize(previewCache) / 1024.0;
  self.totalMemoryUsed_K := result;
  // plant parts
  if (firstPhytomer <> nil) then
    begin
    traverser := PdTraverser.createWithPlant(self);
    try
      traverser.traverseWholePlant(kActivityCountTotalMemoryUse);
      result := result + traverser.totalMemorySize / 1024.0;
      self.totalMemoryUsed_K := result;
    finally
      traverser.free;
      traverser := nil;
    end;
    end;
  end;

function PdPlant.hangingObjectsMemoryUse_K: extended;
  var
    i: smallint;
  begin
  result := 0;
  // random number generators
  if randomNumberGenerator <> nil then result := result + randomNumberGenerator.instanceSize / 1024.0;
  if breedingGenerator <> nil then result := result + breedingGenerator.instanceSize / 1024.0;
  // note
  if noteLines <> nil then result := result + noteLines.instanceSize / 1024.0;
  // amendments
  if amendments <> nil then
    begin
    result := result + amendments.instanceSize / 1024.0;
    if amendments.count > 0 then for i := 0 to amendments.count - 1 do
      result := result + PdPlantDrawingAmendment(amendments.items[i]).instanceSize / 1024.0;
    end;
  end;

function PdPlant.tdoMemoryUse_K: extended;
  var
    partType: smallint;
  begin
  // tdos
  result := 0;
  result := result + pSeedlingLeaf.leafTdoParams.object3D.totalMemorySize / 1024.0;
  result := result + pLeaf.leafTdoParams.object3D.totalMemorySize / 1024.0;
  result := result + pLeaf.stipuleTdoParams.object3D.totalMemorySize / 1024.0;
  result := result + pInflor[kGenderFemale].bractTdoParams.object3D.totalMemorySize / 1024.0;
  result := result + pInflor[kGenderMale].bractTdoParams.object3D.totalMemorySize / 1024.0;
  for partType := 0 to kHighestFloralPartConstant do
    begin
    result := result + pFlower[kGenderFemale].tdoParams[partType].object3D.totalMemorySize / 1024.0;
    result := result + pFlower[kGenderMale].tdoParams[partType].object3D.totalMemorySize / 1024.0;
    end;
  result := result + pAxillaryBud.tdoParams.object3D.totalMemorySize / 1024.0;
  result := result + pFruit.tdoParams.object3D.totalMemorySize / 1024.0;
  result := result + pRoot.tdoParams.object3D.totalMemorySize / 1024.0;
  end;

procedure PdPlant.drawOn(destCanvas: TCanvas);
  var
    realBasePoint_pixels: TPoint;
  begin
  turtle := KfTurtle.defaultStartUsing;
  try
  turtle.drawingSurface.pane := destCanvas;
  self.setTurtleDrawOptionsForNormalDraw(turtle);
  turtle.reset;  { must be after pane and draw options set }
  turtle.setScale_pixelsPerMm(self.realDrawingScale_pixelsPerMm);
  turtle.drawingSurface.foreColor := clGreen;
  turtle.drawingSurface.backColor := clRed;
  turtle.drawingSurface.lineColor := clBlue;
  realBasePoint_pixels := self.basePoint_pixels;
  turtle.xyz(realBasePoint_pixels.x, realBasePoint_pixels.y, 0);
  turtle.resetBoundsRect(realBasePoint_pixels);
  try
	  if turtle.drawOptions.sortPolygons then
		  begin
		  turtle.drawingSurface.recordingStart;
		  self.draw;
		  turtle.drawingSurface.recordingStop;
		  turtle.drawingSurface.recordingDraw;
		  turtle.drawingSurface.clearTriangles;
		  end
	  else
		  begin
		  self.draw;
	    end;
    if (self.computeBounds) and (not domain.drawingToMakeCopyBitmap) then
      begin
      self.setBoundsRect_pixels(self.getTurtleBoundsRect);
      self.enforceMinimumBoundsRect;
			self.expandBoundsRectForLineWidth;
      end;
  except
    on e: Exception do messageForExceptionType(e, 'PdPlant.drawOn');
  end;
  finally
    KfTurtle.defaultStopUsing;
    turtle := nil;
	end;
  end;

procedure PdPlant.setTurtleDrawOptionsForNormalDraw(turtle: KfTurtle);
  begin
  if turtle = nil then exit;
  with turtle.drawOptions do
    begin
    circlePoints := false;
    case domain.options.drawSpeed of
      kDrawFast:
        begin
        draw3DObjects := true;
        draw3DObjectsAsRects := true;
        drawStems := true;
        wireFrame := true;
        sortPolygons := false;
        sortTdosAsOneItem := false;
        end;
      kDrawMedium:
        begin
        draw3DObjects := true;
        draw3DObjectsAsRects := false;
        drawStems := true;
        wireFrame := true;
        sortPolygons := false;
        sortTdosAsOneItem := false;
        end;
      kDrawBest:
        begin
        draw3DObjects := true;
        draw3DObjectsAsRects := false;
        drawStems := true;
        wireFrame := false;
        sortPolygons := true;
        sortTdosAsOneItem := true;
        drawLines := true;
        lineContrastIndex := 3;
        end;
      kDrawCustom:
        begin
        draw3DObjects := domain.options.draw3DObjects;
        draw3DObjectsAsRects := domain.options.draw3DObjectsAsBoundingRectsOnly;
        drawStems := domain.options.drawStems;
        wireFrame := not domain.options.fillPolygons;
        sortPolygons := domain.options.sortPolygons;
        sortTdosAsOneItem := domain.options.sortTdosAsOneItem;
        drawLines := domain.options.drawLinesBetweenPolygons;
        lineContrastIndex := domain.options.lineContrastIndex;
        end;
      end;
    end;
  end;

function PdPlant.resizingRect: TRect;
  var theRect: TRect;
  begin
  theRect := self.boundsRect_pixels;
  with theRect do
    begin
    result := rect(right - domain.options.resizeRectSize, top, right, top + domain.options.resizeRectSize);
    if result.left < left then result.left := left;
    if result.top < top then result.top := top;
    end;
  end;

function PdPlant.pointIsInResizingRect(point: TPoint): boolean;
  var
    theRect: TRect;
  begin
  result := false;
  theRect := self.resizingRect;
  result := (point.x >= theRect.left) and (point.x <= theRect.right)
      and (point.y >= theRect.top) and (point.y <= theRect.bottom);
  end;

procedure PdPlant.recalculateBoundsForOffsetChange;
  var
    drawingRect, intersectRect_pixels: TRect;
    intersectResult: boolean;
  begin
  self.fakeDrawToGetBounds;
  if self.hidden then exit;
  if domain.options.cachePlantBitmaps then
    begin
    drawingRect := Rect(0, 0, MainForm.drawingPaintBox.width, MainForm.drawingPaintBox.height);
    intersectResult := IntersectRect(intersectRect_pixels, self.boundsRect_pixels, drawingRect);
    if (intersectResult) and (not self.hidden) and (previewCache.width < 5) then
      self.recalculateBounds(kDrawNow);
    end;
  end;

procedure PdPlant.recalculateBounds(drawNow: boolean);
  var
    oldBasePoint: TPoint;
    drawingRect, intersectRect_pixels: TRect;
    intersectResult, showProgress: boolean;
    bytesThisBitmapWillBe: longint;
  begin
  self.fakeDrawToGetBounds;
  if not domain.options.cachePlantBitmaps then
    begin
    if previewCache.width > 5 then
      begin
      shrinkPreviewCache;
      MainForm.updateForChangeToPlantBitmaps;
      end;
    exit;
    end;
  if not drawNow then exit;
  if self.hidden then
    begin
    shrinkPreviewCache;
    MainForm.updateForChangeToPlantBitmaps;
    exit;
    end;
  drawingRect := Rect(0, 0, MainForm.drawingPaintBox.width, MainForm.drawingPaintBox.height);
  // on opening file at first, force redraw of cache because drawingPaintBox size might be wrong
  intersectResult := MainForm.inFormCreation or MainForm.inFileOpen
      or IntersectRect(intersectRect_pixels, self.boundsRect_pixels, drawingRect);
  if not intersectResult then
    begin
    self.shrinkPreviewCache;
    MainForm.updateForChangeToPlantBitmaps;           
    exit;
    end;
  bytesThisBitmapWillBe := round(rWidth(boundsRect_pixels) * rHeight(boundsRect_pixels) * MainForm.screenBytesPerPixel);
  if not MainForm.roomForPlantBitmap(self, bytesThisBitmapWillBe) then exit;
  oldBasePoint := self.basePoint_pixels;
  try
    self.setBasePoint_pixels(Point(basePoint_pixels.x - boundsRect_pixels.left,
      basePoint_pixels.y - boundsRect_pixels.top));
    self.resizeCacheIfNecessary(previewCache, Point(rWidth(boundsRect_pixels), rHeight(boundsRect_pixels)), kInMainWindow);
    previewCache.transparentColor := domain.options.transparentColor;
    fillBitmap(previewCache, domain.options.transparentColor);
    // showing progress here is mainly for really complicated plants; most plants won't need it
    showProgress := (not MainForm.drawing) and (domain.options.showPlantDrawingProgress);
    if showProgress then
      begin
      self.plantPartsDrawnAtStart := 0;
      self.countPlantParts;
      showProgress := totalPlantParts > 50;
      if showProgress then MainForm.startDrawProgress(self.totalPlantParts);
      end;
    try
      computeBounds := true;
      self.drawOn(previewCache.canvas);
    finally
      computeBounds := false;
      if showProgress then MainForm.finishDrawProgress;
    end;
  finally
    // have to fake draw again to reset bounds rect
    self.setBasePoint_pixels(oldBasePoint);
    self.fakeDrawToGetBounds;
  end;
  end;

procedure PdPlant.fakeDrawToGetBounds;
  begin
  computeBounds := true;
  turtle := KfTurtle.defaultStartUsing;
  try
    turtle.drawingSurface.pane := nil;
    turtle.drawOptions.drawStems := false;
    turtle.drawOptions.draw3DObjects := false;
    turtle.reset;  { must be after pane and draw options set }
    turtle.setScale_pixelsPerMm(self.realDrawingScale_pixelsPerMm);
    turtle.xyz(self.basePoint_pixels.x, self.basePoint_pixels.y, 0);
    turtle.resetBoundsRect(self.basePoint_pixels);
    try
      self.draw;
    except
      on e: Exception do messageForExceptionType(e, 'PdPlant.fakeDrawToGetBounds');
    end;
    self.setBoundsRect_pixels(self.getTurtleBoundsRect);
    self.enforceMinimumBoundsRect;
    self.expandBoundsRectForLineWidth;
  finally
    KfTurtle.defaultStopUsing;
    turtle := nil;
    computeBounds := false;
	end;
  end;

const kExtraForRootTopProblem = 2;

procedure PdPlant.drawIntoCache(cache: PdBitmap; size: TPoint; considerDomainScale, immediate: boolean);
  var
    newScaleX, newScaleY: single;
    drawPosition: TPoint;
    changed: boolean;
    drawnWidth, drawnHeight: single;
    bestLeft, bestTop: longint;
  begin
  changed := false;
  self.resizeCacheIfNecessary(cache, size, kNotInMainWindow);
  if immediate then
    fillBitmap(cache, domain.options.backgroundColor);
  turtle := KfTurtle.defaultStartUsing;
  try
    { set starting values }
    turtle.drawingSurface.pane := cache.canvas;
    if not fixedPreviewScale then
      begin
      drawingScale_PixelsPerMm := 10.0;
      drawPosition := Point(cache.width div 2, cache.height - 5);
      { 1. draw to figure scale to center boundsRect in cache size }
      self.setTurtleUpForPreviewScratch(drawingScale_PixelsPerMm, drawPosition);
      try self.draw; except {nothing-messes up paint} end;
      self.setBoundsRect_pixels(self.getTurtleBoundsRect);
      { now change the scale to make the boundsRect fit the drawRect }
      drawnWidth := rWidth(boundsRect_pixels);
      drawnHeight := rHeight(boundsRect_pixels);
      if (drawnWidth > 0) and (drawnHeight > 0) then
        begin
        newScaleX := safedivExcept(drawingScale_PixelsPerMm * size.x, drawnWidth, 0.1);
        if considerDomainScale then
          newScaleX := safedivExcept(newScaleX, domain.plantDrawScale_PixelsPerMm, newScaleX)
        else
          newScaleX := newScaleX * 0.9;
        newScaleY := safedivExcept(drawingScale_PixelsPerMm * size.y, drawnHeight, 0.1);
        if considerDomainScale then
          newScaleY := safedivExcept(newScaleY, domain.plantDrawScale_PixelsPerMm, newScaleY)
        else
          newScaleY := newScaleY * 0.9;
        drawingScale_PixelsPerMm := min(newScaleX, newScaleY);
        changed := drawingScale_PixelsPerMm <> 1.0;
        end;
      end;
    if not fixedDrawPosition then
      begin
      { draw to find drawPosition that will center new boundsrect in cache }
      drawPosition := Point(cache.width div 2, cache.height - 5);
      self.setTurtleUpForPreviewScratch(drawingScale_PixelsPerMm, drawPosition);
      try self.draw; except {nothing-messes up paint} end;
      self.setBoundsRect_pixels(self.getTurtleBoundsRect);
      bestLeft := cache.width div 2 - rWidth(boundsRect_pixels) div 2;
      bestTop := cache.height div 2 - rHeight(boundsRect_pixels) div 2;
      drawPosition.x := drawPosition.x - (boundsRect_pixels.left - bestLeft);
      drawPosition.y := drawPosition.y - (boundsRect_pixels.top - bestTop);
      drawPositionIfFixed := drawPosition;
      changed := true;  // assume it will always have to be moved
      end
    else
      drawPosition := drawPositionIfFixed;
    if (fixedPreviewScale or fixedDrawPosition or changed) and (immediate) then
      begin
      { final drawing }
      fillBitmap(cache, domain.options.backgroundColor);
      self.setTurtleUpForPreview(drawingScale_PixelsPerMm, drawPosition);
      try self.draw; except {nothing-messes up paint} end;
      end;
    //self.previewCacheUpToDate := true;
  finally
    KfTurtle.defaultStopUsing;
    turtle := nil;
    self.useBestDrawingForPreview := false;
	end;
  end;

procedure PdPlant.drawPreviewIntoCache(size: TPoint; considerDomainScale, immediate: boolean);
  begin
  try
    self.drawingIntoPreviewCache := true;
    self.drawIntoCache(previewCache, size, considerDomainScale, immediate);
    self.previewCacheUpToDate := true;
  finally
    self.drawingIntoPreviewCache := false;
  end;
  end;

procedure PdPlant.calculateDrawingScaleToFitSize(size: TPoint);
  begin
  self.drawPreviewIntoCache(size, kConsiderDomainScale, kDontDrawNow);
  self.shrinkPreviewCache;
  end;

procedure PdPlant.calculateDrawingScaleToLookTheSameWithDomainScale;
  begin
  drawingScale_PixelsPerMm := safedivExcept(drawingScale_PixelsPerMm, domain.plantManager.plantDrawScale_PixelsPerMm, 0);
  end;

procedure PdPlant.shrinkPreviewCache;
  begin
  { this is to save memory after using the preview cache }
  if previewCache = nil then exit;
  if (previewCache.width > 5) or (previewCache.height > 5) then
    begin
    previewCache.free;
    previewCache := PdBitmap.create;
    with previewCache do
      begin
      width := 1;
      height := 1;
      transparent := true;
      transparentMode := tmFixed;
      transparentColor := domain.options.backgroundColor;
      end;
    end;
  end;

procedure PdPlant.resizeCacheIfNecessary(cache: PdBitmap; size: TPoint; inMainWindow: boolean);
  begin
  if (size.x <= 0) or (size.y <= 0) then exit;
  // special code to make sure pictures come out all right on 256-color monitors.
  // setting the bitmap pixel format to 24-bit and giving it the global palette stops
  // it from dithering and gets the nearest colors from the palette when drawing.
  // you also need to realize the palette anytime you bitblt (copyRect) from this
  // bitmap to a display surface (timage, paint box, draw grid, etc).
  // use the global function copyBitmapToCanvasWithGlobalPalette in umain.
  setPixelFormatBasedOnScreenForBitmap(cache);
  // end special code
  if (cache.width <> size.x) or (cache.height <> size.y) then
    begin
    try
      cache.width := size.x;
      cache.height := size.y;
      if (inMainWindow) and (cache = previewCache) then
        MainForm.updateForChangeToPlantBitmaps;
    except
      cache.width := 1;
      cache.height := 1;
      if (inMainWindow) and (cache = previewCache) then
        MainForm.exceptionResizingPlantBitmap
      else
        showMessage('Problem creating bitmap; probably not enough memory.');
    end;
    end;
  end;

function PdPlant.getTurtleBoundsRect: TRect;
  begin
  result := turtle.boundsRect;
  if pRoot.showsAboveGround then
    result.bottom := result.bottom + kExtraForRootTopProblem;
  end;

procedure PdPlant.setTurtleUpForPreviewScratch(scale: single; drawPosition: TPoint);
  begin
  if turtle = nil then exit;
  with turtle.drawOptions do
    begin
    sortPolygons := false;
    drawLines := false;
    wireFrame := true;
    drawStems := false;
    draw3DObjects := false;
    circlePoints := false;
    end;
  turtle.reset;  { must be after pane and draw options set }
  turtle.setScale_pixelsPerMm(scale);
  turtle.xyz(drawPosition.x, drawPosition.y, 0);
  turtle.resetBoundsRect(drawPosition);
  end;

procedure PdPlant.setTurtleUpForPreview(scale: single; drawPosition: TPoint);
  begin
  if turtle = nil then exit;
  if not self.useBestDrawingForPreview then
    self.setTurtleDrawOptionsForNormalDraw(turtle)
  else
    with turtle.drawOptions do // this is only for the wizard
      begin
      sortPolygons := true;
      sortTdosAsOneItem := true;
      drawLines := true;
      lineContrastIndex := 3;
      wireFrame := false;
      drawStems := true;
      draw3DObjects := true;
      draw3DObjectsAsRects := false;
      circlePoints := false;
      end;
  turtle.reset;  { must be after pane and draw options set }
  turtle.drawingSurface.foreColor := clGreen;
  turtle.drawingSurface.backColor := clRed;
  turtle.drawingSurface.lineColor := clBlue;
  turtle.setScale_pixelsPerMm(scale);
  turtle.xyz(drawPosition.x, drawPosition.y, 0);
  turtle.resetBoundsRect(drawPosition);
  end;

function PdPlant.getHint(point: TPoint): string;
  var
    plantPart: TObject;
    turtle: KfTurtle;
  begin
  result := self.getName;
  if (MainForm.cursorModeForDrawing = kCursorModePosingSelect) and (MainForm.focusedPlant = self) then
    begin
    plantPart := nil;
    plantPart := self.findPlantPartAtPositionByTestingPolygons(point);
    if (plantPart <> nil) and (plantPart is PdPlantPart) then
      result := (plantPart as PdPlantPart).getFullName;
    end;
  end;

function PdPlant.findPlantPartAtPositionByTestingPolygons(point: TPoint): TObject;
  var
    turtle: KfTurtle;
    partID: longint;
  begin
  result := nil;
  self.drawOn(nil);  // if you give it no drawing surface pane, everything happens but the actual drawing
  turtle := KfTurtle.defaultStartUsing;
  if turtle = nil then exit;
  if turtle.drawingSurface = nil then exit;
  try
    partID := turtle.drawingSurface.plantPartIDForPoint(point);
    if partID >= 0 then
      result := self.plantPartForPartID(partID);
  finally
    KfTurtle.defaultStopUsing;
  end;
  end;

function PdPlant.realDrawingScale_pixelsPerMm: single;
  begin
  if domain.drawingToMakeCopyBitmap then
    result := self.drawingScale_PixelsPerMm * domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm
  else
    result := self.drawingScale_PixelsPerMm * domain.plantDrawScale_PixelsPerMm;
  end;

function PdPlant.basePoint_pixels: TPoint;
  begin
  with domain do
    begin
    if not drawingToMakeCopyBitmap then
      begin
      result.x := round((basePoint_mm.x + plantDrawOffset_mm.x) * plantDrawScale_PixelsPerMm);
      result.y := round((basePoint_mm.y  + plantDrawOffset_mm.y) * plantDrawScale_PixelsPerMm);
      end
    else
      begin
      result.x := round((basePoint_mm.x + plantDrawOffsetWhenDrawingCopy_mm.x)
          * plantDrawScaleWhenDrawingCopy_PixelsPerMm);
      result.y := round((basePoint_mm.y  + plantDrawOffsetWhenDrawingCopy_mm.y)
          * plantDrawScaleWhenDrawingCopy_PixelsPerMm);
      end;
    end;
  end;

procedure PdPlant.setBasePoint_pixels(aPoint_pixels: TPoint);
  begin
  with domain do
    begin
    basePoint_mm.x := safedivExcept(aPoint_pixels.x, plantDrawScale_PixelsPerMm, 0) - plantDrawOffset_mm.x;
    basePoint_mm.y := safedivExcept(aPoint_pixels.y, plantDrawScale_PixelsPerMm, 0) - plantDrawOffset_mm.y;
    end;
  end;

procedure PdPlant.setBoundsRect_pixels(aRect_pixels: TRect);
  begin
  normalBoundsRect_pixels := aRect_pixels;
  end;

function PdPlant.boundsRect_pixels: TRect;
  begin
  result := normalBoundsRect_pixels;
  end;

procedure PdPlant.enforceMinimumBoundsRect;
  var theRect: TRect;
  begin
  theRect := self.boundsRect_pixels;
  with theRect do
    begin
    if ((right - left) < 1) then
      begin
      left := basePoint_pixels.x;
      right := left + 1;
      end;
    if ((bottom - top) < 1) then
      begin
      bottom := basePoint_pixels.y;
      top := bottom - 1;
      end;
    end;
  end;

procedure PdPlant.expandBoundsRectForLineWidth;
  var
  	extra: smallint;
    theRect: TRect;
  begin
  extra := round(self.maximumLineWidth * self.realDrawingScale_pixelsPerMm) + 1;
  theRect := self.boundsRect_pixels;
  inflateRect(theRect, extra, extra);
  self.setBoundsRect_pixels(theRect);
  end;

function PdPlant.maximumLineWidth: single;
  begin
  result := 0.0;
  if pLeaf.petioleWidthAtOptimalBiomass_mm > result  then
    result := pLeaf.petioleWidthAtOptimalBiomass_mm;
  if pInternode.widthAtOptimalFinalBiomassAndExpansion_mm > result then
    result := pInternode.widthAtOptimalFinalBiomassAndExpansion_mm;
  if pInflor[kGenderMale].internodeWidth_mm > result  then
    result := pInflor[kGenderMale].internodeWidth_mm;
  if pInflor[kGenderFemale].internodeWidth_mm > result  then
    result := pInflor[kGenderFemale].internodeWidth_mm;
  end;

procedure PdPlant.moveBy(delta_pixels: TPoint);
  var
    delta_mm: SinglePoint;
    theRect: TRect;
  begin
  theRect := boundsRect_pixels;
  with theRect do
    begin
    left := left + delta_pixels.x;
    right := right + delta_pixels.x;
    top := top + delta_pixels.y;
    bottom := bottom + delta_pixels.y;
    end;
  delta_mm.x := safedivExcept(delta_pixels.x, domain.plantDrawScale_PixelsPerMm, 0);
  delta_mm.y := safedivExcept(delta_pixels.y, domain.plantDrawScale_PixelsPerMm, 0);
  basePoint_mm.x := basePoint_mm.x + delta_mm.x;
  basePoint_mm.y := basePoint_mm.y + delta_mm.y;
  end;

procedure PdPlant.moveTo(const aPoint_pixels: TPoint);
  var
    oldBasePoint_pixels: TPoint;
    theRect: TRect;
  begin
  oldBasePoint_pixels := self.basePoint_pixels;
  theRect := boundsRect_pixels;
  with theRect do
    begin
    left := left + aPoint_pixels.x - oldBasePoint_pixels.x;
    right := right + aPoint_pixels.x - oldBasePoint_pixels.x;
    top := top + aPoint_pixels.y - oldBasePoint_pixels.y;
    bottom := bottom + aPoint_pixels.y - oldBasePoint_pixels.y;
    end;
  self.setBasePoint_pixels(aPoint_pixels);
  end;

function PdPlant.includesPoint(const aPoint: TPoint): boolean;
  begin
  result := self.boundsRectIncludesPoint(aPoint, self.boundsRect_pixels, true);
  end;

function PdPlant.boundsRectIncludesPoint(const aPoint: TPoint; boundsRect: TRect; checkResizeRect: boolean): boolean;
	var
    xPixel, yPixel, i: longint;
	begin
  result := ptInRect(boundsRect, aPoint);
  if result and domain.options.cachePlantBitmaps then
    begin
    if checkResizeRect and ptInRect(self.resizingRect, aPoint) then
      result := true
    else
      begin
      xPixel := aPoint.x - boundsRect.left;
      yPixel := aPoint.y - boundsRect.top;
      result := pointColorMatch(xPixel, yPixel);
      if (not result) and (domain.options.cachePlantBitmaps) then
        for i := 0 to 7 do
          if self.pointColorAdjacentMatch(xPixel, yPixel, i) then
            begin
            result := true;
            exit;
            end;
      end;
    end
  end;

function PdPlant.pointInBoundsRect(const aPoint: TPoint): boolean;
  begin
  result := ptInRect(normalBoundsRect_pixels, aPoint);
  end;

function PdPlant.pointColorMatch(xPixel, yPixel: longint): boolean;
	var
    testPixelColor: TColor;
  begin
  testPixelColor := previewCache.canvas.Pixels[xPixel, yPixel];
  result := testPixelColor <> domain.options.transparentColor;
  end;

function PdPlant.pointColorAdjacentMatch(xPixel, yPixel, position: longint): boolean;
	var
    testPixelColor: TColor;
    x, y: longint;
  begin
  x := xPixel; y := yPixel;
  // 0 1 2
  // 3 x 4
  // 5 6 7
  case position of
    0: begin x := xPixel - 1; y := yPixel - 1; end;
    1: begin x := xPixel + 0; y := yPixel - 1; end;
    2: begin x := xPixel + 1; y := yPixel - 1; end;
    3: begin x := xPixel - 1; y := yPixel + 0; end;
    // point x := xPixel + 0; y := yPixel + 0; this is the point already tested
    4: begin x := xPixel + 1; y := yPixel + 0; end;
    5: begin x := xPixel - 1; y := yPixel + 1; end;
    6: begin x := xPixel + 0; y := yPixel + 1; end;
    7: begin x := xPixel + 1; y := yPixel + 1; end;
    end;
  testPixelColor := previewCache.canvas.Pixels[x, y];
  result := testPixelColor <> domain.options.transparentColor;
  end;

procedure PdPlant.saveToGlobal3DOutputFile(indexOfPlant: smallint; translate: boolean; rectWithAllPlants: TRect;
    outputType: smallint; aTurtle: KfTurtle);
  var
    remPoints: array[0..3] of KfPoint3D;
    remWidth: single;
    fileExportSurface: KfFileExportSurface;
    relativeBasePoint_mm: SinglePoint;
    i: integer;
    fixRotation: smallint;
  begin
  if firstPhytomer = nil then exit;
  turtle := aTurtle;
  if turtle = nil then Exception.create('Problem: Nil turtle in PdPlant.saveToGlobal3DOutputFile.');
  fileExportSurface := turtle.fileExportSurface;
  if turtle = nil then Exception.create('Problem: Nil export surface in PdPlant.saveToGlobal3DOutputFile.');
  self.setUpTurtleFor3DOutput;
  if translate then
    begin
    relativeBasePoint_mm.x := safedivExcept(basePoint_pixels.x - rectWithAllPlants.left,
      domain.plantDrawScale_PixelsPerMm, 0) - domain.plantDrawOffset_mm.x;
    relativeBasePoint_mm.y := safedivExcept(basePoint_pixels.y - rectWithAllPlants.top,
      domain.plantDrawScale_PixelsPerMm, 0) - domain.plantDrawOffset_mm.y;
    // move plant to translate, except for for POV, where you translate and scale afterward
    if outputType <> kPOV then
      turtle.xyz(relativeBasePoint_mm.x, relativeBasePoint_mm.y, 0)
    else
      fileExportSurface.setTranslationForCurrentPlant(translate, relativeBasePoint_mm.x, relativeBasePoint_mm.y);
    end;
  turtle.writingTo := outputType;
  fileExportSurface.startPlant(self.name, indexOfPlant);
  // for 3DS need to write out all colors in front especially; must be done before reminder
  if outputType = k3DS then
    begin
    for i := 0 to kExportPartLast do
      (fileExportSurface as KfDrawingSurfaceFor3DS).writeMaterialDescription(i, self.colorForDXFPartType(i));
    if not domain.registered then
      (fileExportSurface as KfDrawingSurfaceFor3DS).writeMaterialDescription(-1, rgb(100, 100, 100));
    end;
  // these rotations are to fix consistent misrotations - the option sits on top of them
  case outputType of
    kDXF: fixRotation := 64; // comes out sideways
    kPOV: fixRotation := 0;  // okay
    k3DS: fixRotation := 64; // comes out sideways
    kOBJ: fixRotation := 0;  // okay
    kVRML: fixRotation := 0;  // okay
    kLWO: fixRotation := 128;  // comes out upside down
    else raise Exception.create('Problem: Invalid export type in PdPlant.saveToGlobal3DOutputFile.');
    end;
  turtle.rotateX(fixRotation);
  // this is a user-specified turn on top of the default
  turtle.rotateX(domain.exportOptionsFor3D[outputType].xRotationBeforeDraw * 256.0 / 360.0);
  if not domain.registered then
    begin
    remWidth := self.realDrawingScale_pixelsPerMm * 5.0;
    turtle.push;
    turtle.moveInMillimeters(remWidth / 2);
    turtle.rotateY(64); turtle.moveInMillimeters(remWidth / 2);
    remPoints[0] := turtle.position;
    turtle.rotateY(64); turtle.moveInMillimeters(remWidth);
    remPoints[1] := turtle.position;
    turtle.rotateY(64); turtle.moveInMillimeters(remWidth);
    remPoints[2] := turtle.position;
    turtle.rotateY(64); turtle.moveInMillimeters(remWidth);
    remPoints[3] := turtle.position;
    turtle.pop;
    fileExportSurface.writeRegistrationReminder(remPoints[0], remPoints[1], remPoints[2], remPoints[3]);
    end;
  self.draw;
  fileExportSurface.endPlant;
  end;

procedure PdPlant.setUpTurtleFor3DOutput;
  begin
  with turtle.drawOptions do
    begin
    sortPolygons := false;
    drawLines := false;
    lineContrastIndex := 0;
    wireFrame := false;
    drawStems := true;
    draw3DObjects := true;
    draw3DObjectsAsRects := false;
    circlePoints := false;
    end;
  turtle.reset;  { must be after pane and draw options set }
  turtle.setScale_pixelsPerMm(self.realDrawingScale_pixelsPerMm);
  turtle.drawingSurface.foreColor := clGreen;
  turtle.drawingSurface.backColor := clRed;
  turtle.drawingSurface.lineColor := clBlue;
  turtle.xyz(0, 0, 0);
  turtle.resetBoundsRect(Point(0, 0));
  end;

{ ----------------------------------------------------------------------------------  i/o and data transfer }
procedure PdPlant.defaultAllParameters;
  var
    param: PdParameter;
    i: smallint;
  begin
  if domain.parameterManager.parameters.count > 0 then
    for i := 0 to domain.parameterManager.parameters.count - 1 do
      begin
      param := PdParameter(domain.parameterManager.parameters.items[i]);
      if param.fieldType <> kFieldHeader then
        self.defaultParameter(param, kDontCheckForUnreadParams);
      end;
  self.finishLoadingOrDefaulting(kDontCheckForUnreadParams);
  end;

procedure PdPlant.defaultParameter(param: PdParameter; writeDebugMessage: boolean);
  var
    tempBoolean: boolean;
    tempSmallint: smallint;
    tempLongint: longint;
    tempFloat: single;
    tempColorRef: TColorRef;
    tempSCurve: SCurveStructure;
    tempTdo: KfObject3D;
  begin
  if param = nil then exit;
  case param.fieldType of
    kFieldBoolean:
    begin
    tempBoolean := strToBool(param.defaultValueString);
    self.transferField(kSetField, tempBoolean, param.fieldNumber, param.fieldType, 0, false, nil);
    end;
  kFieldSmallint, kFieldEnumeratedList:
    begin
    tempSmallint := strToIntDef(stringUpTo(param.defaultValueString, ' '), 0);
    self.transferField(kSetField, tempSmallint, param.fieldNumber, param.fieldType, 0, false, nil);
    end;
  kFieldLongint:
    begin
    tempLongint := strToIntDef(param.defaultValueString, 0);
    self.transferField(kSetField, tempLongint, param.fieldNumber, param.fieldType, 0, false, nil);
    end;
  kFieldColor:
    begin
    tempColorRef := rgbStringToColor(param.defaultValueString);
    self.transferField(kSetField, tempColorRef, param.fieldNumber, param.fieldType, 0, false, nil);
    end;
  kFieldFloat:
    begin
    if param.indexType = kIndexTypeSCurve then {this is the only array}
      begin
      changingWholeSCurves := true;
      tempSCurve := stringToSCurve(param.defaultValueString);
      self.transferWholeSCurve(kSetField, tempSCurve, param.fieldNumber, param.fieldType, false, nil);
      changingWholeSCurves := false;
      end
    else
      begin
      boundForString(param.defaultValueString, kFieldFloat, tempFloat);
      self.transferField(kSetField, tempFloat, param.fieldNumber, param.fieldType, 0, false, nil);
      end;
    end;
  kFieldThreeDObject:
    begin
    tempTdo := KfObject3D.create;
    try
      tempTdo.readFromInputString(param.defaultValueString, kAdjustForOrigin);
      self.transferField(kSetField, tempTdo, param.fieldNumber, param.fieldType, 0, false, nil);
    finally
      tempTdo.free;
      tempTdo := nil;
    end;
    end;
    end;
  if writeDebugMessage then
    debugPrint('Plant <' + self.name + '> parameter <' + param.name
        + '> defaulted to <' + param.defaultValueString + '>');
  end;

procedure PdPlant.writeToMainFormMemoAsText;
  var fakeTextFile: TextFile;
  begin
  writingToMemo := true;
  try
    self.writeToPlantFile(fakeTextFile);
  finally
    writingToMemo := false;
  end;
  end;

procedure PdPlant.writeLine(var plantFile: TextFile; aString: string);
  begin
  if self.writingToMemo then
    MainForm.plantsAsTextMemo.lines.add(aString)
  else
    writeln(plantFile, aString);
  end;

procedure PdPlant.writeToPlantFile(var plantFile: TextFile);
  var
    section: PdSection;
    param: PdParameter;
    i, j: smallint;
    tempBoolean: boolean;
    tempSmallint: smallint;
    tempLongint: longint;
    tempFloat: single;
    tempColorRef: TColorRef;
    tempSCurve: SCurveStructure;
    tempTdo: KfObject3D;
    start, stop: string;
  begin
  // v2.0 saving selection state in main window
  if MainForm <> nil then
    self.selectedWhenLastSaved := MainForm.isSelected(self)
  else
    self.selectedWhenLastSaved := false;
  start := ' [';
  stop := '] =';
  writeLine(plantFile, '[' + self.name + '] ' + kPlantAsTextStartString + ' <v2.0>');  // v2.0
  if noteLines.count > 0 then
    begin
    writeLine(plantFile, kStartNoteString);
    for i := 0 to noteLines.count - 1 do
      writeLine(plantFile, noteLines.strings[i]);
    writeLine(plantFile, kEndNoteString);
    end;
  if domain.sectionManager.sections.count > 0 then
    for i := 0 to domain.sectionManager.sections.count - 1 do
      begin
      section := PdSection(domain.sectionManager.sections.items[i]);
      if section = nil then continue;
      { write out section header with name }
      writeLine(plantFile, '; ------------------------- ' + section.getName);
      { write out params }
      for j := 0 to section.numSectionItems - 1 do
        begin
        param := domain.parameterManager.parameterForFieldNumber(section.sectionItems[j]);
        if param = nil then continue;
        case param.fieldType of
          kFieldHeader: {skip};
          kFieldBoolean:
            begin
            self.transferField(kGetField, tempBoolean, param.fieldNumber, param.fieldType, 0, false, nil);
            writeLine(plantFile, param.name + start + param.fieldID + stop + boolToStr(tempBoolean));
            end;
          kFieldSmallint, kFieldEnumeratedList:
            begin
            self.transferField(kGetField, tempSmallint, param.fieldNumber, param.fieldType, 0, false, nil);
            writeLine(plantFile, param.name + start + param.fieldID + stop + intToStr(tempSmallint));
            end;
          kFieldLongint:
            begin
            self.transferField(kGetField, tempLongint, param.fieldNumber, param.fieldType, 0, false, nil);
            writeLine(plantFile, param.name + start + param.fieldID + stop + intToStr(tempLongint));
            end;
          kFieldColor:
            begin
            self.transferField(kGetField, tempColorRef, param.fieldNumber, param.fieldType, 0, false, nil);
            writeLine(plantFile, param.name + start + param.fieldID + stop + intToStr(tempColorRef));
            end;
          kFieldFloat:
            begin
            if param.indexType = kIndexTypeSCurve then {this is the only array}
              begin
              self.transferWholeSCurve(kGetField, tempSCurve, param.fieldNumber, param.fieldType, false, nil);
              writeLine(plantFile, param.name + start + param.fieldID + stop + sCurveToString(tempSCurve));
              end
            else
              begin
              self.transferField(kGetField, tempFloat, param.fieldNumber, param.fieldType, 0, false, nil);
              writeLine(plantFile, param.name + start + param.fieldID + stop + digitValueString(tempFloat));
              end;
            end;
          kFieldThreeDObject:
            begin
            tempTdo := KfObject3d.create;
            try
              self.transferField(kGetField, tempTdo, param.fieldNumber, param.fieldType, 0, false, nil);
              writeLine(plantFile, param.name + start + param.fieldID + stop + tempTdo.name);
              if self.writingToMemo then
                tempTdo.writeToMemo(MainForm.plantsAsTextMemo)
              else
                tempTdo.writeToFileStream(plantFile, kEmbeddedInPlant);
            finally
              tempTdo.free;
              tempTdo := nil;
            end;
            end;
          end;
        end;
      end;
  if amendments.count > 0 then for i := 0 to amendments.count - 1 do
    if self.writingToMemo then
      PdPlantDrawingAmendment(amendments.items[i]).writeToMemo(MainForm.plantsAsTextMemo)
    else
      PdPlantDrawingAmendment(amendments.items[i]).writeToTextFile(plantFile);
  writeLine(plantFile, '; ------------------------- ' + kPlantAsTextEndString + ' ' + self.getName + ' <v2.0>');  //v2.0
  writeLine(plantFile, '');
  end;

procedure PdPlant.readLineAndTdoFromPlantFile(aLine: string; var plantFile: TextFile);
  var
    tempBoolean: boolean;
    tempSmallint: smallint;
    tempLongint: longint;
    tempFloat: single;
    tempColorRef: TColorRef;
    tempSCurve: SCurveStructure;
    i: smallint;
    param: PdParameter;
    secondLine, noteLine, nameAndFieldID, fieldID, paramValue: string;
    tempTdo: KfObject3d;
    found: boolean;
    newAmendment: PdPlantDrawingAmendment;
  begin
  // read note if this line starts it
  if pos(upperCase(kStartNoteString), upperCase(aLine)) > 0 then // this only will happen if in file
    begin
    noteLines.clear;
    while not eof(plantFile) do
      begin
      tolerantReadln(plantFile, noteLine);
      if (pos(upperCase(kEndNoteString), upperCase(noteLine)) > 0) and (noteLines.count < 5000) then
        break
      else
        noteLines.add(noteLine);
      end;
    exit; // added v2.0, no use reading other stuff when finished with note
    end;
  // read amendment if line is an amendment - v2.0
  if pos(kStartAmendmentString, aLine) > 0 then
    begin
    newAmendment := PdPlantDrawingAmendment.create;
    if self.readingFromMemo then
      newAmendment.readFromMemo(MainForm.plantsAsTextMemo, readingMemoLine)
    else
      newAmendment.readFromTextFile(plantFile);
    self.addAmendment(newAmendment);
    exit;
    end;
  // v2.0 fix lines broken before [ or = (does NOT fix lines broken within strings)
  // this has to come AFTER we deal with notes and amendments; it applies to parameters only
  if (pos('[', aLine) <= 0) or (pos('=', aLine) <= 0) then
    begin
    if self.readingFromMemo then
      secondLine := MainForm.plantsAsTextMemo.lines.strings[readingMemoLine]
    else
      tolerantReadln(plantFile, secondLine);
    inc(readingMemoLine);
    debugPrint('plant <' + self.name + '> line <' + aLine + '> merged with <' + secondLine + '>');
    aLine := aLine + ' ' + secondLine;
    end;
  nameAndFieldID := stringUpTo(aLine, '=');
  fieldID := stringBeyond(nameAndFieldID, '[');
  fieldID := stringUpTo(fieldID, ']');
  if pos('header', fieldID) > 0 then exit;
  paramValue := stringBeyond(aLine, '=');
  found := false;
  param := nil;
  if domain.parameterManager.parameters.count > 0 then
    for i := 0 to domain.parameterManager.parameters.count - 1 do
      begin
      param := PdParameter(domain.parameterManager.parameters.items[i]);
      if param = nil then exit;
      if param.fieldID = fieldID then
        begin
        found := true;
        break;
        end;
      end;
  if not found then exit;
  case param.fieldType of
    kFieldHeader: {skip};
    kFieldBoolean:
      begin
      tempBoolean := strToBool(paramValue);
      self.transferField(kSetField, tempBoolean, param.fieldNumber, param.fieldType, 0, false, nil);
      end;
    kFieldSmallint, kFieldEnumeratedList:
      begin
      tempSmallint := strToIntDef(paramValue, 0);
      { if both bounds are zero, it means not to check them }
      if (param.lowerBound <> 0) or (param.upperBound <> 0) then
        begin
        if tempSmallint < round(param.lowerBound) then
          tempSmallint := round(param.lowerBound);
        if tempSmallint > round(param.upperBound) then
          tempSmallint := round(param.upperBound);
        end;
      self.transferField(kSetField, tempSmallint, param.fieldNumber, param.fieldType, 0, false, nil);
      end;
    kFieldLongint:
      begin
      tempLongint := strToIntDef(paramValue, 0);
      { if both bounds are zero, it means not to check them }
      if (param.lowerBound <> 0) or (param.upperBound <> 0) then
        begin
        if tempLongint < round(param.lowerBound) then
          tempLongint := round(param.lowerBound);
        if tempLongint > round(param.upperBound) then
          tempLongint := round(param.upperBound);
        end;
      if param.fieldNumber = kStateBasePointY then
        tempLongint := tempLongint;
      self.transferField(kSetField, tempLongint, param.fieldNumber, param.fieldType, 0, false, nil);
      end;
    kFieldColor:
      begin
      tempColorRef := strToIntDef(paramValue, 0);
      self.transferField(kSetField, tempColorRef, param.fieldNumber, param.fieldType, 0, false, nil);
      end;
    kFieldFloat:
      begin
      if param.indexType = kIndexTypeSCurve then {this is the only array}
        begin
        changingWholeSCurves := true;
        tempSCurve := stringToSCurve(paramValue);
        // bound s curve
        // all s curve values (x and y) must be between 0 and 1 EXCLUSIVE
        // if not in this range, set whole curve to reasonable values
        with tempSCurve do
          if (x1 <= 0.0) or (y1 <= 0.0) or (x2 <= 0.0) or (y2 <= 0.0)
            or (x1 >= 1.0) or (y1 >= 1.0) or (x2 >= 1.0) or (y2 >= 1.0) then
            begin
            // instead of raising exception, just hard-code whole curve to acceptable values
            // don't use Parameters.tab default in case that was read in wrong also
            x1 := 0.25;
            y1 := 0.1;
            x2 := 0.65;
            y2 := 0.85;
            end;
        self.transferWholeSCurve(kSetField, tempSCurve, param.fieldNumber, param.fieldType, false, nil);
        changingWholeSCurves := false;
        end
      else
        begin
        boundForString(paramValue, kFieldFloat, tempFloat);
        if pos('Drawing scale', param.name) > 0 then
          tempTdo := nil;
        { if both bounds are zero, it means not to check them }
        if (param.lowerBound <> 0) or (param.upperBound <> 0) then
          begin
          if tempFloat < param.lowerBound then tempFloat := param.lowerBound;
          if tempFloat > param.upperBound then tempFloat := param.upperBound;
          end;
        self.transferField(kSetField, tempFloat, param.fieldNumber, param.fieldType, 0, false, nil);
        end;
      end;
    kFieldThreeDObject:
      begin
      tempTdo := KfObject3d.create;
      try
        tempTdo.setName(trimLeftAndRight(paramValue));
        if self.readingFromMemo then
          tempTdo.readFromMemo(MainForm.plantsAsTextMemo, readingMemoLine)
        else
          tempTdo.readFromFileStream(plantFile, kEmbeddedInPlant);
        self.transferField(kSetField, tempTdo, param.fieldNumber, param.fieldType, 0, false, nil);
      finally
        tempTdo.free;
        tempTdo := nil;
      end;
      end;
    end;
  param.valueHasBeenReadForCurrentPlant := true;
  end;

procedure PdPlant.finishLoadingOrDefaulting(checkForUnreadParams: boolean);
  var
    param: PdParameter;
    i: smallint;
  begin
  if checkForUnreadParams then
    if domain.parameterManager.parameters.count > 0 then
      for i := 0 to domain.parameterManager.parameters.count - 1 do
        begin
        param := PdParameter(domain.parameterManager.parameters.items[i]);
        if (not param.valueHasBeenReadForCurrentPlant) and (param.fieldType <> kFieldHeader) then
          self.defaultParameter(param, checkForUnreadParams);
        end;
  pGeneral.ageAtWhichFloweringStarts := intMin(pGeneral.ageAtWhichFloweringStarts, pGeneral.ageAtMaturity);
  age := intMin(age, pGeneral.ageAtMaturity);
  calcSCurveCoeffs(pGeneral.growthSCurve);
  calcSCurveCoeffs(pFruit.sCurveParams);
  calcSCurveCoeffs(pLeaf.sCurveParams);
  self.regrow;
  end;

procedure PdPlant.editTransferField(d: integer; var value; fieldID, fieldType, fieldIndex: integer; regrow: boolean);
  var
    updateList: TListCollection;
	begin
  if fieldType = kFieldHeader then exit;
  if (d = kGetField) then
    self.transferField(d, value, fieldID, fieldType, fieldIndex, regrow, nil)
  else
    begin
    updateList := TListCollection.create;
    try
      self.transferField(d, value, fieldID, fieldType, fieldIndex, regrow, updateList);
      if updateList.count > 0 then
        begin
        MainForm.updateParameterValuesWithUpdateListForPlant(self, updateList);
        if (domain.options.updateTimeSeriesPlantsOnParameterChange) and (TimeSeriesForm <> nil) then
          TimeSeriesForm.updatePlantsFromParent(self);
        end;
    finally
      updateList.free;
      updateList := nil;
    end;
    end;
  if (d = kSetField) and regrow then
    self.regrow;
  end;

procedure PdPlant.transferField(d: integer; var v; fieldID, ft, index: smallint; regrow: boolean;
    updateList: TListCollection);
	begin
  if ft = kFieldHeader then exit;
  self.directTransferField(d, v, fieldID, ft, index, updateList);
  if d = kSetField then
    begin
    case fieldID of
      { cfk fix: should be not allowing to change these to values that don't work }
      kFruitSCurve:
        if not changingWholeSCurves then calcSCurveCoeffs(pFruit.sCurveParams);
      kGeneralGrowthSCurve:
        if not changingWholeSCurves then calcSCurveCoeffs(pGeneral.growthSCurve);
      kLeafSCurve:
        if not changingWholeSCurves then calcSCurveCoeffs(pLeaf.sCurveParams);
      kGeneralAgeAtMaturity:
        if (age > smallint(v)) then self.setAge(smallint(v));
      end;
    if (ft = kFieldColor) then
      self.needToRecalculateColors := true;
    end;
  end;                          

procedure PdPlant.directTransferField(d: integer; var v; fieldID, ft, index: smallint; updateList: TListCollection);
  begin
  // switch-over point is hard-coded and must be identical to that set in PlantStudio Utility program
  // that generates utransfr.pas
  if fieldID <= 200 then
    Plant_directTransferField(self, v, d, fieldID, ft, index, updateList)
  else
    Plant_directTransferField_SecondPart(self, v, d, fieldID, ft, index, updateList);
  if updateList <> nil then addToUpdateList(fieldID, updateList);
  end;
                                     
procedure PdPlant.addToUpdateList(fieldID: integer; updateList: TListCollection);
  var updateEvent: PdPlantUpdateEvent;
	begin
  if updateList = nil then exit;
  updateEvent := PdPlantUpdateEvent.create;
  updateEvent.plant := self;
  updateEvent.fieldID := fieldID;
  updateList.add(updateEvent);
  end;

class procedure PdPlant.fillEnumStringList(var list: TStringList; fieldID: Integer; var hasRadioButtons: boolean);
  begin
  { assumes list being given to it is empty }
  case fieldID of
    kLeafCompoundPinnateOrPalmate:
      begin
      list.add('pinnate (feather-like)');
      list.add('palmate (hand-like)');
      hasRadioButtons := true;
      end;
    kMeristemAndLeafArrangement:
      begin
      list.add('alternate (one per node)');
      list.add('opposite (two per node)');
      hasRadioButtons := true;
      end;
    kLeafCompoundPinnateArrangement:
      begin
      list.add('alternate');
      list.add('opposite');                   
      hasRadioButtons := true;
      end;
    kFlowerFemaleBudOption, kFlowerMaleBudOption:
      begin
      list.add('no bud');                                 
      list.add('single 3D object bud (old style)');
      list.add('unfolding flower (new style)');    
      hasRadioButtons := true;
      end;
  else
    raise Exception.create('Problem: Unknown field for plant string list ' + intToStr(fieldID)
        + ' in method PdPlant.fillEnumStringList.');
  end;
  end;

procedure PdPlant.transferObject3D(direction: integer; myTdo: KfObject3D; otherTdo: KfObject3D);
  begin
  { assumption: both tdos exist }
  if (myTdo = nil) or (otherTdo = nil) then
    raise Exception.create('Problem: Nil 3D object in method PdPlant.transferObject3D.');
  if direction = kSetField then
    myTdo.copyFrom(otherTdo)
  else
    otherTdo.copyFrom(myTdo);
  end;

procedure PdPlant.transferWholeSCurve(direction: smallint; var value: SCurveStructure; fieldNumber, fieldType: smallint;
    regrow: boolean; updateList: TListCollection);
  begin
  self.transferField(direction, value.x1, fieldNumber, fieldType, 0, regrow, updateList);
  self.transferField(direction, value.y1, fieldNumber, fieldType, 1, regrow, updateList);
  self.transferField(direction, value.x2, fieldNumber, fieldType, 2, regrow, updateList);
  self.transferField(direction, value.y2, fieldNumber, fieldType, 3, regrow, updateList);
  end;

procedure PdPlant.MFD(var objectValue; var value; fieldType: integer; direction: integer);
  {MFD = MoveFieldData}
	begin
  if direction = kGetField then
    case fieldType of
  		kFieldFloat: 					single(value) := single(objectValue);
  		kFieldSmallint:   		smallint(value) := smallint(objectValue);
      kFieldLongint:        longint(value) := longint(objectValue);
  		kFieldColor:          TColorRef(value) := TColorRef(objectValue);
  		kFieldBoolean:        boolean(value) := boolean(objectValue);
      kFieldEnumeratedList: smallint(value) := smallint(objectValue);
    else
      raise Exception.create('Problem: Unsupported transfer from field ' + IntToStr(fieldType) + ' in method PdPlant.MFD.');
    end
  else if direction = kSetField then
    case fieldType of
  		kFieldFloat: 					single(objectValue) := single(value);
  		kFieldSmallint:   		smallint(objectValue) := smallint(value);
  		kFieldLongint:   		  longint(objectValue) := longint(value);
  		kFieldColor:          TColorRef(objectValue) := TColorRef(value);
  		kFieldBoolean:        boolean(objectValue) := boolean(value);
      kFieldEnumeratedList: smallint(objectValue) := smallint(value);
    else
      raise Exception.create('Problem: Unsupported transfer to field ' + IntToStr(fieldType) + ' in method PdPlant.MFD.');
    end
	end;

{ ------------------------------------------------------------------------------- breeding }
procedure PdPlant.useBreedingOptionsAndPlantsToSetParameters(options: BreedingAndTimeSeriesOptionsStructure;
    firstPlant, secondPlant: PdPlant; tdos: TListCollection);
  var
    firstBoolean, secondBoolean, newBoolean: boolean;
    firstInteger, secondInteger, newInteger: smallint;
    firstFloat, secondFloat, newFloat: single;
    firstColor, secondColor, newColor: TColorRef;
    firstSCurve, secondSCurve, newSCurve: SCurveStructure;
    firstTdo, secondTdo, newTdo, randomTdo: KfObject3D;
    sectionIndex, paramIndex, saveAge: smallint;
    weight, stdDev: single;
    param: PdParameter;
    section: PdSection;
  begin                                        
  if firstPlant = nil then exit;
  saveAge := self.age;
  self.reset;
  if domain.sectionManager.sections.count > 0 then for sectionIndex := 0 to domain.sectionManager.sections.count - 1 do
    begin
    section := PdSection(domain.sectionManager.sections.items[sectionIndex]);
    if section = nil then continue;
    for paramIndex := 0 to section.numSectionItems - 1 do
      begin
      param := domain.parameterManager.parameterForFieldNumber(section.sectionItems[paramIndex]);
      if (param = nil) or (param.fieldType = kFieldHeader) then continue;
      case param.fieldType of
        kFieldBoolean: {non-numeric}
          begin
          firstPlant.transferField(kGetField, firstBoolean, param.fieldNumber, param.fieldType, 0, false, nil);
          if secondPlant = nil then
            newBoolean := firstBoolean
          else
            begin
            secondPlant.transferField(kGetField, secondBoolean, param.fieldNumber, param.fieldType, 0, false, nil);
            if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) = kFromFirstPlant then
              newBoolean := firstBoolean
            else
              newBoolean := secondBoolean;
            end;
          self.transferField(kSetField, newBoolean, param.fieldNumber, param.fieldType, 0, false, nil);
          end;
        kFieldSmallint: {numeric}
          begin
          newInteger := 0;
          firstPlant.transferField(kGetField, firstInteger, param.fieldNumber, param.fieldType, 0, false, nil);
          if secondPlant = nil then
            newInteger := firstInteger
          else
            begin
            secondPlant.transferField(kGetField, secondInteger, param.fieldNumber, param.fieldType, 0, false, nil);
            if firstInteger = secondInteger then
              newInteger := firstInteger
            else
              begin
              weight := options.firstPlantWeights[sectionIndex] / 100.0;
              newInteger := round(firstInteger * weight + secondInteger * (1.0 - weight));
              end;
            end;
          // extra limit on mutation to stop exceptions
          stdDev := 0.5 * newInteger * options.mutationStrengths[sectionIndex] / 100.0;
          newInteger := round(breedingGenerator.randomNormalWithStdDev(newInteger * 1.0, stdDev));
          newInteger := round(min(param.upperBound, max(param.lowerBound, 1.0 * newInteger)));
          self.transferField(kSetField, newInteger, param.fieldNumber, param.fieldType, 0, false, nil);
          end;
        kFieldLongint:  ;
          { the only numeric fields so far are the plant's position x and y (which is redone anyway)
            and the random number seed, which shouldn't really be bred anyway, so we will do nothing
            here. if you want to add longint parameters later, you will have to copy the smallint stuff
            to put here. }
        kFieldEnumeratedList: {non-numeric}
          begin
          firstPlant.transferField(kGetField, firstInteger, param.fieldNumber, param.fieldType, 0, false, nil);
          if secondPlant = nil then
            newInteger := firstInteger
          else
            begin
            secondPlant.transferField(kGetField, secondInteger, param.fieldNumber, param.fieldType, 0, false, nil);
            if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) = kFromFirstPlant then
              newInteger := firstInteger
            else
              newInteger := secondInteger;
            end;
          self.transferField(kSetField, newInteger, param.fieldNumber, param.fieldType, 0, false, nil);
          end;
        kFieldColor: {numeric if option is set, otherwise non-numeric}
          begin
          firstPlant.transferField(kGetField, firstColor, param.fieldNumber, param.fieldType, 0, false, nil);
          if secondPlant = nil then
            newColor := firstColor
          else
            begin
            secondPlant.transferField(kGetField, secondColor, param.fieldNumber, param.fieldType, 0, false, nil);
            if not options.mutateAndBlendColorValues then
              begin
              if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) = kFromFirstPlant then
                newColor := firstColor
              else
                newColor := secondColor;
              end;
            end;
          if options.mutateAndBlendColorValues then
            newColor := self.blendAndMutateColors(options, sectionIndex, (secondPlant <> nil),
                firstColor, secondColor);
          self.transferField(kSetField, newColor, param.fieldNumber, param.fieldType, 0, false, nil);
          end;
        kFieldFloat:
          begin
          if param.indexType = kIndexTypeSCurve then
            begin
             { considering s curve non-numeric, too much trouble to make sure it is all right, and there are only two }
            changingWholeSCurves := true;
            firstPlant.transferWholeSCurve(kGetField, firstSCurve, param.fieldNumber, param.fieldType, false, nil);
            if secondPlant = nil then
              newSCurve := firstSCurve
            else
              begin
              secondPlant.transferWholeSCurve(kGetField, secondSCurve, param.fieldNumber, param.fieldType, false, nil);
              if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) = kFromFirstPlant then
                newSCurve := firstSCurve
              else
                newSCurve := secondSCurve;
              end;
            self.transferWholeSCurve(kSetField, newSCurve, param.fieldNumber, param.fieldType, false, nil);
            changingWholeSCurves := false;
            end
          else {plain float - numeric}
            begin
            // newFloat := 0.0001;  v2.0 removed this
            firstPlant.transferField(kGetField, firstFloat, param.fieldNumber, param.fieldType, 0, false, nil);
            if secondPlant = nil then
              newFloat := firstFloat
            else
              begin
              secondPlant.transferField(kGetField, secondFloat, param.fieldNumber, param.fieldType, 0, false, nil);
              if firstFloat = secondFloat then
                newFloat := firstFloat
              else
                begin
                weight := options.firstPlantWeights[sectionIndex] / 100.0;
                newFloat := firstFloat * weight + secondFloat * (1.0 - weight);
                end;
              end;
            // extra limit on mutation to stop exceptions
            stdDev := 0.5 * newFloat * options.mutationStrengths[sectionIndex] / 100.0;
            newFloat := breedingGenerator.randomNormalWithStdDev(newFloat * 1.0, stdDev);
            newFloat := min(param.upperBound, max(param.lowerBound, newFloat));
            { for now, don't let float get to zero because it causes problems }
            // newFloat := max(0.0001, newFloat);  v2.0 removed this to enable breeding with no variation
            self.transferField(kSetField, newFloat, param.fieldNumber, param.fieldType, 0, false, nil);
            end;
          end;
        kFieldThreeDObject: {non-numeric}
          begin
          firstTdo := KfObject3D.create;
          secondTdo := KfObject3D.create;
          newTdo := KfObject3D.create;
          try
            firstPlant.transferField(kGetField, firstTdo, param.fieldNumber, param.fieldType, 0, false, nil);
            if secondPlant = nil then
              newTdo.copyFrom(firstTdo)
            else
              begin
              secondPlant.transferField(kGetField, secondTdo, param.fieldNumber, param.fieldType, 0, false, nil);
              if not options.chooseTdosRandomlyFromCurrentLibrary then
                begin
                if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) = kFromFirstPlant then
                  newTdo.copyFrom(firstTdo)
                else
                  newTdo.copyFrom(secondTdo);
                end
              else
                begin
                randomTdo := self.tdoRandomlyPickedFromCurrentLibrary(tdos);
                if randomTdo <> nil then
                  newTdo.copyFrom(randomTdo);
                end;
              end;
            if options.chooseTdosRandomlyFromCurrentLibrary then
              begin
              randomTdo := self.tdoRandomlyPickedFromCurrentLibrary(tdos);
              if randomTdo <> nil then
                newTdo.copyFrom(randomTdo);
              end;
            self.transferField(kSetField, newTdo, param.fieldNumber, param.fieldType, 0, false, nil);
          finally
            firstTdo.free;
            firstTdo := nil;
            secondTdo.free;
            secondTdo := nil;
            newTdo.free;
            newTdo := nil;
          end;
          end;
        else
          { note that longints are not handled here - they are used only for position information
            and not for normal parameters }
          raise Exception.create('Problem: Invalid parameter type in method PdPlant.useBreedingOptionsAndPlantsToSetParameters.');
        end; {case}
      end; {param loop}
    end;  {section loop}
  self.finishLoadingOrDefaulting(kDontCheckForUnreadParams);
  self.setAge(saveAge);
  end;

function PdPlant.pickPlantToCopyNonNumericalParameterFrom(options: BreedingAndTimeSeriesOptionsStructure;
    sectionIndex: smallint): smallint;
  begin
  result := kFromFirstPlant;
  case options.getNonNumericalParametersFrom of
    kFromFirstPlant: result := kFromFirstPlant;
    kFromSecondPlant: result := kFromSecondPlant;
    kFromProbabilityBasedOnWeightsForSection:
      begin
      if breedingGenerator.zeroToOne < options.firstPlantWeights[sectionIndex] / 100.0 then
        result := kFromFirstPlant
      else
        result := kFromSecondPlant;
      end;
    kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant:
      begin
      if options.firstPlantWeights[sectionIndex] >= 50 then
        result := kFromFirstPlant
      else
        result := kFromSecondPlant;
      end;
    kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant:
      begin
      if options.firstPlantWeights[sectionIndex] > 50 then
        result := kFromFirstPlant
      else
        result := kFromSecondPlant;
      end;
    kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly:
      begin
      if options.firstPlantWeights[sectionIndex] > 50 then
        result := kFromFirstPlant
      else if options.firstPlantWeights[sectionIndex] < 50 then
        result := kFromSecondPlant
      else {50/50}
        begin
        if breedingGenerator.zeroToOne <= 0.5 then
          result := kFromFirstPlant
        else
          result := kFromSecondPlant;
        end;
      end;
    end;
  end;

function PdPlant.blendAndMutateColors(options: BreedingAndTimeSeriesOptionsStructure; sectionIndex: smallint;
    haveSecondPlant: boolean; firstColor, secondColor: TColorRef): TColorRef;
  var
    weight, stdDevAsFractionOfMean: single;
    firstColorAsFloat, secondColorAsFloat, resultAsFloat, mutationStrengthToUse: single;
  begin
  firstColorAsFloat := firstColor;
  resultAsFloat := firstColorAsFloat;
  if haveSecondPlant then
    begin
    secondColorAsFloat := secondColor;
    weight := options.firstPlantWeights[sectionIndex] / 100.0;
    resultAsFloat := firstColorAsFloat * weight + secondColorAsFloat * (1.0 - weight);
    end;
  // v2.0 can mutate colors separately from other parameters - if other params not zero, go with that,
  // if other params zero, and mutating colors, use low mutation for colors only
  mutationStrengthToUse := 0;
  if options.mutationStrengths[sectionIndex] > 0 then
    mutationStrengthToUse := options.mutationStrengths[sectionIndex]
  else if options.mutateAndBlendColorValues then
    mutationStrengthToUse := kLowMutation;
  stdDevAsFractionOfMean := mutationStrengthToUse / 100.0;
  { for colors, reduce std dev to 10% of for other things, because the numbers are so huge }
  stdDevAsFractionOfMean := stdDevAsFractionOfMean * 0.1;
  resultAsFloat := breedingGenerator.randomNormalWithStdDev(resultAsFloat, resultAsFloat * stdDevAsFractionOfMean);
  result := round(resultAsFloat);
  end;

function PdPlant.tdoRandomlyPickedFromCurrentLibrary(tdos: TListCollection): KfObject3D;
   var
    index: smallint;
  begin
  result := nil;
  if tdos = nil then exit;
  if tdos.count <= 0 then exit;
  index := intMax(0, intMin(tdos.count - 1, round(breedingGenerator.zeroToOne * tdos.count)));
  result := tdos.items[index];
  end;

{ -------------------------------------------------------------------------------  data transfer for binary copy }
procedure PdPlant.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdPlant;
  cvir.versionNumber := 2;
  cvir.additionNumber := 0;
  end;

procedure PdPlant.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  var
    tdoSeedlingLeaf, tdoLeaf, tdoStipule, tdoAxillaryBud, tdoInflorBractFemale, tdoInflorBractMale, tdoFruit, tdoRoot: KfObject3d;
    femaleFlowerTdos: array[0..kHighestFloralPartConstant] of KfObject3d;
    maleFlowerTdos: array[0..kHighestFloralPartConstant] of KfObject3d;
    traverser: PdTraverser;
    hasFirstPhytomer: boolean;
    partType: integer;
	begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
    streamShortString(name);
    streamSmallint(age);
    streamSinglePoint(basePoint_mm);
    streamSingle(xRotation);
    streamSingle(yRotation);
    streamSingle(zRotation);
    streamSingle(drawingScale_PixelsPerMm);
    streamRect(normalBoundsRect_pixels);
    streamBoolean(hidden);
    streamBoolean(justCopiedFromMainWindow);
    streamSmallint(indexWhenRemoved);
    streamSmallint(selectedIndexWhenRemoved);
    { save pointers to 3d objects if reading because they will get written over during streaming of structures }
    if isReading then
      begin
      tdoSeedlingLeaf := pSeedlingLeaf.leafTdoParams.object3D;
      tdoLeaf := pLeaf.leafTdoParams.object3D;
      tdoStipule := pLeaf.stipuleTdoParams.object3D;
      tdoInflorBractFemale := pInflor[kGenderFemale].bractTdoParams.object3D;
      tdoInflorBractMale := pInflor[kGenderMale].bractTdoParams.object3D;
      for partType := 0 to kHighestFloralPartConstant do
        begin
        femaleFlowerTdos[partType] := pFlower[kGenderFemale].tdoParams[partType].object3D;
        maleFlowerTdos[partType] := pFlower[kGenderMale].tdoParams[partType].object3D;
        end;
      tdoAxillaryBud := pAxillaryBud.tdoParams.object3D;
      tdoFruit := pFruit.tdoParams.object3D;
      tdoRoot := pRoot.tdoParams.object3D;
      end
    else                              
      begin
      tdoSeedlingLeaf := nil;
      tdoLeaf := nil;
      tdoStipule := nil;
      tdoInflorBractFemale := nil;
      tdoInflorBractMale := nil;
      for partType := 0 to kHighestFloralPartConstant do
        begin
        femaleFlowerTdos[partType] := nil;
        maleFlowerTdos[partType] := nil;
        end;
      tdoAxillaryBud := nil;
      tdoFruit := nil;
      tdoRoot := nil;
      end;
    streamBytes(pGeneral, sizeOf(pGeneral));
    streamBytes(pMeristem, sizeOf(pMeristem));
    streamBytes(pInternode, sizeOf(pInternode));
    streamBytes(pLeaf, sizeOf(pLeaf));
    streamBytes(pSeedlingLeaf, sizeOf(pSeedlingLeaf));
    streamBytes(pAxillaryBud, sizeOf(pAxillaryBud));
    streamBytes(pInflor[kGenderMale], sizeOf(pInflor[kGenderMale]));
    streamBytes(pInflor[kGenderFemale], sizeOf(pInflor[kGenderFemale]));
    streamBytes(pFlower[kGenderMale], sizeOf(pFlower[kGenderMale]));
    streamBytes(pFlower[kGenderFemale], sizeOf(pFlower[kGenderFemale]));
    streamBytes(pFruit, sizeOf(pFruit));
    streamBytes(pRoot, sizeOf(pRoot));
    { reset pointers if reading and stream 3d objects }
    with pSeedlingLeaf.leafTdoParams do
      begin
      if isReading then object3D := tdoSeedlingLeaf;
      object3D.streamUsingFiler(filer);
      end;
    with pLeaf.leafTdoParams do
      begin
      if isReading then object3D := tdoLeaf;
      object3D.streamUsingFiler(filer);
      end;
    with pLeaf.stipuleTdoParams do
      begin
      if isReading then object3D := tdoStipule;
      object3D.streamUsingFiler(filer);
      end;
    with pInflor[kGenderFemale].bractTdoParams do
      begin
      if isReading then object3D := tdoInflorBractFemale;
      object3D.streamUsingFiler(filer);
      end;
    with pInflor[kGenderMale].bractTdoParams do
      begin
      if isReading then object3D := tdoInflorBractMale;
      object3D.streamUsingFiler(filer);
      end;
    for partType := 0 to kHighestFloralPartConstant do
      begin
      with pFlower[kGenderFemale].tdoParams[partType] do
        begin
        if isReading then object3D := femaleFlowerTdos[partType];
        object3D.streamUsingFiler(filer);
        end;
      with pFlower[kGenderMale].tdoParams[partType] do
        begin
        if isReading then object3D := maleFlowerTdos[partType];
        object3D.streamUsingFiler(filer);
        end;
      end;
    with pAxillaryBud.tdoParams do
      begin
      if isReading then object3D := tdoAxillaryBud;
      object3D.streamUsingFiler(filer);
      end;
    with pFruit.tdoParams do
      begin
      if isReading then object3D := tdoFruit;
      object3D.streamUsingFiler(filer);
      end;
    with pRoot.tdoParams do
      begin
      if isReading then object3D := tdoRoot;
      object3D.streamUsingFiler(filer);
      end;
    randomNumberGenerator.streamUsingFiler(filer);
    breedingGenerator.streamUsingFiler(filer);
    { biomass info }
    streamSingle(totalBiomass_pctMPB);
    streamSingle(reproBiomass_pctMPB);
    streamSingle(changeInShootBiomassToday_pctMPB);
    streamSingle(changeInReproBiomassToday_pctMPB);
    streamSingle(unallocatedNewVegetativeBiomass_pctMPB);
    streamSingle(unremovedDeadVegetativeBiomass_pctMPB);
    streamSingle(unallocatedNewReproductiveBiomass_pctMPB);
    streamSingle(unremovedDeadReproductiveBiomass_pctMPB);
    streamSingle(unremovedStandingDeadBiomass_pctMPB);
    streamLongint(numApicalActiveReproductiveMeristemsOrInflorescences);
    streamLongint(numAxillaryActiveReproductiveMeristemsOrInflorescences);
    streamLongint(numApicalInactiveReproductiveMeristems);
    streamLongint(numAxillaryInactiveReproductiveMeristems);
    streamSmallint(ageOfYoungestPhytomer);
    streamBoolean(needToRecalculateColors);
    streamSmallint(ageAtWhichFloweringStarted);
    streamBoolean(floweringHasStarted);
    streamLongint(totalPlantParts);
    { plant parts }
    traverser := nil;
    if isReading then
      begin
      streamBoolean(hasFirstPhytomer);
      {don't want to create if not written}
      if firstPhytomer <> nil then
        self.freeAllDrawingPlantParts;
      if hasFirstPhytomer then
        begin
        firstPhytomer := nil;
    	  firstPhytomer := PdInternode.create;
        if firstPhytomer <> nil then
          begin
          PdInternode(firstPhytomer).plant := self;
          end
        else
          raise Exception.create('Problem: Could not create first internode in method PdPlant.streamDataWithFiler.');
        end;
      end
    else if isWriting then
      begin
      hasFirstPhytomer := self.firstPhytomer <> nil;
      streamBoolean(hasFirstPhytomer);
      end;
    if hasFirstPhytomer then
      begin
      traverser := PdTraverser.createWithPlant(self);
      try
        traverser.filer := filer;
  	    traverser.traverseWholePlant(kActivityStream);
      finally
  	    traverser.free;
      end;
      end;
    previewCache.streamUsingFiler(filer);
    if isReading then
      begin
      calcSCurveCoeffs(pFruit.sCurveParams);
      calcSCurveCoeffs(pGeneral.growthSCurve);
      calcSCurveCoeffs(pLeaf.sCurveParams);
      end;
    end;
  amendments.streamUsingFiler(filer, PdPlantDrawingAmendment);
  end;

{ --------------------------------------------------------------------------------  command-related }
procedure PdPlant.randomize;
  var
    seed: smallint;
    breedingSeed: longint;
    anXRotation: single;
  begin
  seed := randomNumberGenerator.randomSmallintSeedFromTime;
  breedingSeed := breedingGenerator.randomSeedFromTime;
  anXRotation := randomNumberGenerator.zeroToOne * 360.0;
  self.randomizeWithSeedsAndXRotation(seed, breedingSeed, anXRotation);
  end;

procedure PdPlant.randomizeWithSeedsAndXRotation(generalSeed: smallint; breedingSeed: longint; anXRotation: single);
  var
    updateList: TListCollection;
    updateEvent: PdPlantUpdateEvent;
  begin
  pGeneral.startingSeedForRandomNumberGenerator := generalSeed;
  breedingGenerator.setSeed(breedingSeed);
  self.xRotation := anXRotation;
  self.regrow;
  { tell main window to update in case showing parameter panel }
  // if this is a breeder plant, it will create the update list, but the main window won't
  // recognize the plant pointer. this is extra memory use, but i'd have to pass a boolean all
  // over to stop it, and the list only has one item
  updateList := TListCollection.create;
  updateEvent := PdPlantUpdateEvent.create;
  try
    updateEvent.plant := self;
    updateEvent.fieldID := kGeneralStartingSeedForRandomNumberGenerator; {hard-coded}
    updateList.add(updateEvent);
    MainForm.updateParameterValuesWithUpdateListForPlant(self, updateList);
  finally
    updateList.free;
    updateList := nil;
  end;
  end;

{ ------------------------------------------------------------------------------------  next day and traverser }
procedure PdPlant.nextDay;
  var
    traverser: PdTraverser;
    newTotalBiomass_pctMPB, changeInTotalBiomassTodayAsPercentOfMPB_pct,
      fractionReproBiomassToday_frn, newReproBiomass_pctMPB, newShootBiomass_pctMPB: single;
    fractionToMaturity_frn: single;
    firstMeristem: PdMeristem;
  begin
  try
  { calculate overall biomass change using s curve }
  fractionToMaturity_frn := safedivExcept(age, pGeneral.ageAtMaturity, 0);
  newTotalBiomass_pctMPB := max(0.0, min(100.0, 100.0 *
    sCurve(fractionToMaturity_frn, pGeneral.growthSCurve.c1, pGeneral.growthSCurve.c2)));
  changeInTotalBiomassTodayAsPercentOfMPB_pct := newTotalBiomass_pctMPB - totalBiomass_pctMPB;
  totalBiomass_pctMPB := newTotalBiomass_pctMPB;
  { divide up change into shoot and fruit, make changes to total shoot/fruit }
  if floweringHasStarted then
    begin
    fractionReproBiomassToday_frn :=
        max(0, pGeneral.fractionReproductiveAllocationAtMaturity_frn
        * safedivExcept(age - ageAtWhichFloweringStarted, pGeneral.ageAtMaturity - ageAtWhichFloweringStarted, 0));
    newReproBiomass_pctMPB := fractionReproBiomassToday_frn * totalBiomass_pctMPB;
    changeInReproBiomassToday_pctMPB := newReproBiomass_pctMPB - reproBiomass_pctMPB;
    reproBiomass_pctMPB := newReproBiomass_pctMPB;
    { rest goes to shoots }
    newShootBiomass_pctMPB := totalBiomass_pctMPB - reproBiomass_pctMPB;
    changeInShootBiomassToday_pctMPB := newShootBiomass_pctMPB - shootBiomass_pctMPB;
    shootBiomass_pctMPB := newShootBiomass_pctMPB;
    end
  else
    begin
    changeInReproBiomassToday_pctMPB := 0.0;
    changeInShootBiomassToday_pctMPB := changeInTotalBiomassTodayAsPercentOfMPB_pct;
    shootBiomass_pctMPB := totalBiomass_pctMPB;
    end;
  if shootBiomass_pctMPB + reproBiomass_pctMPB > 100.0 then
    begin
    shootBiomass_pctMPB := shootBiomass_pctMPB;
    end;
  traverser := PdTraverser.createWithPlant(self);
  try
    if (firstPhytomer = nil) then
      begin
      {If first day, create first phytomer. Assume seed reserves are placed into this phytomer.}
      firstMeristem := PdMeristem.newWithPlant(self);
      firstPhytomer := firstMeristem.createFirstPhytomer;
      {Must tell firstPhytomer to recalculate internode angle because it did not know it was the
      first phytomer until after drawing plant got this pointer back.}
      if firstPhytomer = nil then exit;
      PdInternode(firstPhytomer).setAsFirstPhytomer;
      { reduce changeInShootBiomassToday_pctMPB for amount used to make first phytomer }
      changeInShootBiomassToday_pctMPB := changeInShootBiomassToday_pctMPB
          - firstMeristem.optimalInitialPhytomerBiomass_pctMPB;
      end;
    { decide if flowering has started using params }
    if not floweringHasStarted and (age >= pGeneral.ageAtWhichFloweringStarts) then
      begin
      floweringHasStarted := true;
      ageAtWhichFloweringStarted := age;
      { tell all meristems to switch over }
      traverser.traverseWholePlant(kActivityStartReproduction);
      end;
    self.allocateOrRemoveBiomassWithTraverser(traverser);
    if firstPhytomer <> nil then
      traverser.ageOfYoungestPhytomer := maxLongInt
    else
      traverser.ageOfYoungestPhytomer := 0;
    traverser.traverseWholePlant(kActivityNextDay);
    self.ageOfYoungestPhytomer := traverser.ageOfYoungestPhytomer;
    inc(age);
  finally
    traverser.free;
    traverser := nil;
    self.needToRecalculateColors := true;
  end;
  except
    on e: Exception do messageForExceptionType(e, 'PdPlant.nextDay');
  end;
  end;

procedure cancelOutOppositeAmounts(var amountAdded: single; var amountTakenAway: single);
  begin
  if (amountAdded > 0.0) and (amountTakenAway > 0.0) then
    begin
    if amountAdded = amountTakenAway then
      begin
      amountAdded := 0.0;
      amountTakenAway := 0.0;
      end
    else if amountAdded > amountTakenAway then
      begin
      amountAdded := amountAdded - amountTakenAway;
      amountTakenAway := 0.0;
      end
    else
      begin
      amountTakenAway := amountTakenAway - amountAdded;
      amountAdded := 0.0;
      end;
    end;
  end;

procedure PdPlant.allocateOrRemoveBiomassWithTraverser(traverserProxy: TObject);
  var
    traverser: PdTraverser;
    shootAddition_pctMPB, shootReduction_pctMPB, reproAddition_pctMPB, reproReduction_pctMPB: single;
  begin
  if firstPhytomer = nil then exit;
  traverser := traverserProxy as PdTraverser;
  if traverser = nil then exit;
  { set addition and reduction from changes, and add in amounts rolled over from yesterday }
  if changeInShootBiomassToday_pctMPB > 0 then
    begin
    shootAddition_pctMPB := changeInShootBiomassToday_pctMPB + unallocatedNewVegetativeBiomass_pctMPB;
    unallocatedNewVegetativeBiomass_pctMPB := 0.0;
    shootReduction_pctMPB := 0.0;
    end
  else
    begin
    shootReduction_pctMPB := changeInShootBiomassToday_pctMPB + unremovedDeadVegetativeBiomass_pctMPB;
    unremovedDeadVegetativeBiomass_pctMPB := 0.0;
    shootAddition_pctMPB := 0.0;
    end;
  if changeInReproBiomassToday_pctMPB > 0 then
    begin
    reproAddition_pctMPB := changeInReproBiomassToday_pctMPB + unallocatedNewReproductiveBiomass_pctMPB;
    unallocatedNewReproductiveBiomass_pctMPB := 0.0;
    reproReduction_pctMPB := 0.0;
    end
  else
    begin
    reproReduction_pctMPB := changeInReproBiomassToday_pctMPB + unremovedDeadReproductiveBiomass_pctMPB;
    unremovedDeadReproductiveBiomass_pctMPB := 0.0;
    reproAddition_pctMPB := 0.0;
    end;
  { see if amounts can cancel out to any extent }
  cancelOutOppositeAmounts(shootAddition_pctMPB, shootReduction_pctMPB);
  cancelOutOppositeAmounts(reproAddition_pctMPB, reproReduction_pctMPB);
  { allocate new shoot biomass }
  if shootAddition_pctMPB > 0.0 then
    self.allocateOrRemoveParticularBiomass(shootAddition_pctMPB, unallocatedNewVegetativeBiomass_pctMPB,
    kActivityDemandVegetative, kActivityGrowVegetative, traverser);
  { remove dead shoot biomass }
  if shootReduction_pctMPB > 0.0 then
    self.allocateOrRemoveParticularBiomass(shootReduction_pctMPB, unremovedDeadVegetativeBiomass_pctMPB,
    kActivityVegetativeBiomassThatCanBeRemoved, kActivityRemoveVegetativeBiomass, traverser);
  { allocate new fruit biomass }
  if reproAddition_pctMPB > 0.0 then
    self.allocateOrRemoveParticularBiomass(reproAddition_pctMPB, unallocatedNewReproductiveBiomass_pctMPB,
    kActivityDemandReproductive, kActivityGrowReproductive, traverser);
  { remove dead fruit biomass }
  if reproReduction_pctMPB > 0.0 then
    self.allocateOrRemoveParticularBiomass(reproReduction_pctMPB, unremovedDeadReproductiveBiomass_pctMPB,
    kActivityReproductiveBiomassThatCanBeRemoved, kActivityRemoveReproductiveBiomass, traverser);
  end;

procedure PdPlant.allocateOrRemoveParticularBiomass(biomassToAddOrRemove_pctMPB: single;
  var undistributedBiomass_pctMPB: single; askingMode, tellingMode: integer; traverserProxy: TObject);
  var
    traverser: PdTraverser;
    totalDemandOrAvailableBiomass_pctMPB: single;
  begin
  try
  traverser := traverserProxy as PdTraverser;
  if traverser = nil then exit;
  traverser.traverseWholePlant(askingMode);
  totalDemandOrAvailableBiomass_pctMPB := traverser.total;
  if totalDemandOrAvailableBiomass_pctMPB > 0.0 then
    begin
    if biomassToAddOrRemove_pctMPB > totalDemandOrAvailableBiomass_pctMPB then
      begin
      undistributedBiomass_pctMPB := biomassToAddOrRemove_pctMPB - totalDemandOrAvailableBiomass_pctMPB;
      traverser.fractionOfPotentialBiomass := 1.0;
      end
    else
      traverser.fractionOfPotentialBiomass := safedivExcept(biomassToAddOrRemove_pctMPB,
          totalDemandOrAvailableBiomass_pctMPB, 0);
    traverser.traverseWholePlant(tellingMode);
    end
  else
    begin  { no demand }
    undistributedBiomass_pctMPB := undistributedBiomass_pctMPB + biomassToAddOrRemove_pctMPB;
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdPlant.allocateOrRemoveParticularBiomass');
  end;
  end;

procedure PdPlant.getPlantStatistics(statisticsProxy: TObject);
  var
    statistics: PdPlantStatistics;
    traverser: PdTraverser;
  begin
  statistics := PdPlantStatistics(statisticsProxy);
  if statistics = nil then exit;
  traverser := PdTraverser.createWithPlant(self);
  try
    traverser.statistics := statistics;
    traverser.traverseWholePlant(kActivityGatherStatistics);
  finally
    traverser.free;
  end;
  { set undistributed amounts in statistics }
  statistics.liveBiomass_pctMPB[kStatisticsPartTypeUnallocatedNewVegetativeBiomass] :=
      self.unallocatedNewVegetativeBiomass_pctMPB;
  statistics.deadBiomass_pctMPB[kStatisticsPartTypeUnremovedDeadVegetativeBiomass] :=
      self.unremovedDeadVegetativeBiomass_pctMPB;
  statistics.liveBiomass_pctMPB[kStatisticsPartTypeUnallocatedNewReproductiveBiomass] :=
      self.unallocatedNewReproductiveBiomass_pctMPB;
  statistics.deadBiomass_pctMPB[kStatisticsPartTypeUnremovedDeadReproductiveBiomass] :=
      self.unremovedDeadReproductiveBiomass_pctMPB;
  end;

procedure PdPlant.report;
  var traverser: PdTraverser;
  begin
  if (firstPhytomer <> nil) then
    begin
    DebugPrint('---------------------- Start plant report');
    traverser := PdTraverser.createWithPlant(self);
    try
      traverser.traverseWholePlant(kActivityReport);
    finally
      traverser.free;
    end;
    DebugPrint('---------------------- End plant report');
    end;
  end;

{ --------------------------------------------------------------------------------------------- amendments }
function PdPlant.amendmentForPartID(partID: longint): PdPlantDrawingAmendment;
  var
    i: integer;
    amendment: PdPlantDrawingAmendment;
  begin
  result := nil;
  if amendments.count <= 0 then exit;
  for i := 0 to amendments.count - 1 do
    begin
    amendment := PdPlantDrawingAmendment(amendments.items[i]);
    if (amendment.partID = partID) then
      begin
      result := amendment;
      exit;
      end;
    end;
  end;

procedure PdPlant.addAmendment(newAmendment: PdPlantDrawingAmendment);
  begin
  amendments.add(newAmendment);
  end;

procedure PdPlant.removeAmendment(oldAmendment: PdPlantDrawingAmendment);
  begin
  amendments.remove(oldAmendment);
  end;

procedure PdPlant.removeAllAmendments;
  begin
  amendments.free;
  amendments := nil;
  amendments := TListCollection.create;
  end;

procedure PdPlant.clearPointersToAllAmendments;
  begin
  amendments.clearPointersWithoutDeletingObjects;
  end;

procedure PdPlant.restoreAmendmentPointersToList(aList: TList);
  var i: integer;
  begin
  if (aList <> nil) and (aList.count > 0) then for i := 0 to aList.count - 1 do
    self.addAmendment(PdPlantDrawingAmendment(aList.items[i]));
  end;

function PdPlant.plantPartForPartID(partID: longint): TObject;
  var
    traverser: PdTraverser;
  begin
  result := nil;
  if (firstPhytomer <> nil) then
    begin
    traverser := PdTraverser.createWithPlant(self);
    try
      traverser.foundPlantPart := nil;
      traverser.partID := partID;
      traverser.traverseWholePlant(kActivityFindPartForPartID);
      result := traverser.foundPlantPart;
    finally
      traverser.free;
    end;
    end;
  end;

procedure PdPlant.getInfoForPlantPartAtPoint(point: TPoint; var partID: longint; var partType: string);
  var
    part: PdPlantPart;
  begin
  partID := -1;
  partType := '';
  part := self.findPlantPartAtPositionByTestingPolygons(point) as PdPlantPart;
  if part = nil then exit;
  partID := part.partID;
  partType := part.getName;
  end;

function PdPlant.colorForDXFPartType(index: smallint): TColorRef;
  begin
  case index of
    kExportPartMeristem: result := pAxillaryBud.tdoParams.faceColor;
    kExportPartInternode: result := pInternode.FaceColor;
    kExportPartSeedlingLeaf: result := pSeedlingLeaf.leafTdoParams.FaceColor;
    kExportPartLeaf: result := pLeaf.leafTdoParams.FaceColor;
    kExportPartFirstPetiole: result := pLeaf.PetioleColor;
    kExportPartPetiole: result := pLeaf.PetioleColor;
    kExportPartLeafStipule: result := pLeaf.stipuleTdoParams.FaceColor;
    kExportPartInflorescenceStalkFemale: result := pInflor[kGenderFemale].StalkColor;
    kExportPartInflorescenceInternodeFemale: result := pInflor[kGenderFemale].StalkColor;
    kExportPartInflorescenceBractFemale: result := pInflor[kGenderFemale].bractTdoParams.faceColor;
    kExportPartInflorescenceStalkMale: result := pInflor[kGenderMale].StalkColor;
    kExportPartInflorescenceInternodeMale: result := pInflor[kGenderMale].StalkColor;
    kExportPartInflorescenceBractMale: result := pInflor[kGenderMale].bractTdoParams.faceColor;
    kExportPartPedicelFemale: result := pInflor[kGenderFemale].pedicelColor;
    kExportPartFlowerBudFemale: result := pFlower[kGenderFemale].tdoParams[kBud].faceColor;
    kExportPartStyleFemale: result := pFlower[kGenderFemale].styleColor;
    kExportPartStigmaFemale: result := pFlower[kGenderFemale].tdoParams[kPistils].faceColor;
    kExportPartFilamentFemale: result := pFlower[kGenderFemale].filamentColor;
    kExportPartAntherFemale: result := pFlower[kGenderFemale].tdoParams[kStamens].faceColor;
    kExportPartFirstPetalsFemale: result := pFlower[kGenderFemale].tdoParams[kFirstPetals].FaceColor;
    kExportPartSecondPetalsFemale: result := pFlower[kGenderFemale].tdoParams[kSecondPetals].faceColor;
    kExportPartThirdPetalsFemale: result := pFlower[kGenderFemale].tdoParams[kThirdPetals].faceColor;
    kExportPartFourthPetalsFemale: result := pFlower[kGenderFemale].tdoParams[kFourthPetals].faceColor;
    kExportPartFifthPetalsFemale: result := pFlower[kGenderFemale].tdoParams[kFifthPetals].faceColor;
    kExportPartSepalsFemale: result := pFlower[kGenderFemale].tdoParams[kSepals].faceColor;
    kExportPartPedicelMale: result := pInflor[kGenderMale].pedicelColor;
    kExportPartFlowerBudMale: result := pFlower[kGenderMale].tdoParams[kBud].faceColor;
    kExportPartFilamentMale: result := pFlower[kGenderMale].filamentColor;
    kExportPartAntherMale: result := pFlower[kGenderMale].tdoParams[kStamens].faceColor;
    kExportPartFirstPetalsMale: result := pFlower[kGenderMale].tdoParams[kFirstPetals].FaceColor;
    kExportPartSepalsMale: result := pFlower[kGenderMale].tdoParams[kSepals].faceColor;
    kExportPartUnripeFruit: result := pFruit.tdoParams.alternateFaceColor;
    kExportPartRipeFruit: result := pFruit.tdoParams.faceColor;
    kExportPartRootTop: result := pRoot.tdoParams.faceColor;
    else
      raise Exception.create('Problem: Invalid part type in method colorForDXFPartType.');
    end;
  end;

{ ----------------------------------------------------------- initialization code for colors }
begin
{These worst stress condition colors are constant over all plants.
This makes sense because chlorosis (yellowing) is always yellow;
age is always brown;
and P stress is always dark green.}
worstNStressColor := support_rgb(200, 200, 0);
worstPStressColor := support_rgb(20, 50, 20);
worstDeadColor := support_rgb(100, 100, 0);
end.
