unit uintern;

interface

uses WinProcs, WinTypes,
  upart, uplant, uleaf, ufiler, utravers;
                           
type

PdInternode = class(PdPlantPart)
  public
  leftBranchPlantPart: PdPlantPart;
  rightBranchPlantPart: PdPlantPart;
  nextPlantPart: PdPlantPart;
  phytomerAttachedTo: PdInternode;
  leftLeaf: PdLeaf;
  rightLeaf: PdLeaf;
  internodeColor: TColorRef;
  internodeAngle: single;
  lengthExpansion: single;
  widthExpansion: single;
  boltingExpansion: single;
  fractionOfOptimalInitialBiomassAtCreation_frn: single;
  traversingDirection: byte;
  isFirstPhytomer: boolean;
  newBiomassForDay_pctMPB: single;
  distanceFromFirstPhytomer: longint;
  destructor destroy; override;
  function getName: string; override;
  class function NewWithPlantFractionOfInitialOptimalSize(aPlant: PdPlant; aFraction: single): PdInternode;
  procedure blendColorsStrength(aColor: TColorRef; aStrength: single); override;
  procedure setColorsToParameters; override;
	procedure calculateInternodeAngle;
	function distanceFromApicalMeristem: longint;
  procedure calculateDistanceFromFirstPhytomer;
  function firstPhytomerOnBranch: PdInternode;
  function biomassOfMeAndAllPartsConnectedToMe_pctMPB: single;
  function biomassOfPartsImmediatelyAboveMe_pctMPB: single;
	procedure draw; override;
	procedure drawInternode;
	procedure drawRootTop;
	procedure InitializeFractionOfInitialOptimalSize(thePlant: PdPlant; aFraction: single); {???}
  procedure makeSecondSeedlingLeaf(aFraction: single);
	procedure nextDay;  override;
	procedure report; override;
	function partType: integer; override;
  procedure traverseActivity(mode: integer; traverserProxy: TObject); override;
  function isPhytomer: boolean; override;
  procedure checkIfSeedlingLeavesHaveAbscissed;
  function propFullLength: single;
  function propFullWidth: single;
  class function optimalInitialBiomass_pctMPB(plant: PdPlant): single;
  procedure setAsFirstPhytomer;
  procedure countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser); 
  procedure determineAmendmentAndAlsoForChildrenIfAny; override;
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure streamPlantPart(filer: PdFiler; var plantPart: PdPlantPart);
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  end;

implementation

uses SysUtils, Dialogs, Classes, Graphics, usupport,
  udebug, uturtle, u3dexport, utdo, umath, umerist, uinflor, uclasses, uamendmt;

class function PdInternode.NewWithPlantFractionOfInitialOptimalSize(aPlant: PdPlant;
    aFraction: single): PdInternode;
  begin
  result := create;
  result.InitializeFractionOfInitialOptimalSize(aPlant, aFraction);
  end;

procedure PdInternode.initializeFractionOfInitialOptimalSize(thePlant: PdPlant; aFraction: single);
  begin
  Initialize(thePlant);
  IsFirstPhytomer := false; {Plant sets this from outside on first phytomer.}
  calculateInternodeAngle;
  self.lengthExpansion := 1.0;
  self.widthExpansion := 1.0;
  self.boltingExpansion := 1.0;
  self.fractionOfOptimalInitialBiomassAtCreation_frn := aFraction;
  self.liveBiomass_pctMPB := aFraction * PdInternode.optimalInitialBiomass_pctMPB(plant);
  self.deadBiomass_pctMPB := 0.0;
  internodeColor := plant.pInternode.faceColor;
  leftLeaf := PdLeaf.NewWithPlantFractionOfOptimalSize(plant, aFraction);
  if plant.pMeristem.branchingAndLeafArrangement = kArrangementOpposite then
    rightLeaf := PdLeaf.NewWithPlantFractionOfOptimalSize(plant, aFraction);
  end;

function PdInternode.getName: string;
  begin
  result := 'internode';
  end;

procedure PdInternode.makeSecondSeedlingLeaf(aFraction: single);
  begin
  if rightLeaf = nil then
    rightLeaf := PdLeaf.NewWithPlantFractionOfOptimalSize(plant, aFraction);
  if rightLeaf <> nil then rightLeaf.isSeedlingLeaf := true;
  end;

destructor PdInternode.destroy;
	begin
  {note that if branch parts were phytomers they will have been
  freed and set to nil by the traverser}
  nextPlantPart.free;
  nextPlantPart := nil;
  leftBranchPlantPart.free;
  leftBranchPlantPart := nil;
  rightBranchPlantPart.free;
  rightBranchPlantPart := nil;
  leftLeaf.free;
  leftLeaf := nil;
  rightLeaf.free;
  rightLeaf := nil;
  inherited destroy;
  end;
                                               
procedure PdInternode.setAsFirstPhytomer;
  begin
  self.isFirstPhytomer := true;
  if leftLeaf <> nil then leftLeaf.isSeedlingLeaf := true;
  if rightLeaf <> nil then rightLeaf.isSeedlingLeaf := true;
  self.calculateInternodeAngle;
  end;

procedure PdInternode.determineAmendmentAndAlsoForChildrenIfAny;
  var amendmentToPass: PdPlantDrawingAmendment;
  begin
  inherited determineAmendmentAndAlsoForChildrenIfAny;
  if amendment <> nil then
    amendmentToPass := amendment
  else
    amendmentToPass := parentAmendment;
  if leftBranchPlantPart <> nil then leftBranchPlantPart.parentAmendment := amendmentToPass;
  if rightBranchPlantPart <> nil then rightBranchPlantPart.parentAmendment := amendmentToPass;
  if nextPlantPart <> nil then nextPlantPart.parentAmendment := amendmentToPass;
  // amendment must be passed to leaves explicitly since they are not strictly speaking children
  if leftLeaf <> nil then leftLeaf.parentAmendment := amendmentToPass;
  if rightLeaf <> nil then leftLeaf.parentAmendment := amendmentToPass;
  end;

procedure PdInternode.nextDay;
  var
    tryExpansion: single;
  begin
  try
  inherited nextDay;
  { length and width expansion adjustment from new biomass (always decreases because new biomass is compact) }
  if liveBiomass_pctMPB > 0 then
    begin
    { if liveBiomass_pctMPB is extremely small, these divisions may produce an overflow }
    { must bound these because some accounting error is causing problems that should be fixed later }
    try
      tryExpansion :=
            max(0.0, min(500.0, safedivExcept(liveBiomass_pctMPB - newBiomassForDay_pctMPB, liveBiomass_pctMPB, 0) * lengthExpansion
          + safedivExcept(newBiomassForDay_pctMPB, liveBiomass_pctMPB, 0) * 1.0));
      lengthExpansion := tryExpansion;
    except
    end;
    try
      tryExpansion :=
            max(0.0, min(50.0, safedivExcept(liveBiomass_pctMPB - newBiomassForDay_pctMPB, liveBiomass_pctMPB, 0) * widthExpansion
          + safedivExcept(newBiomassForDay_pctMPB, liveBiomass_pctMPB, 0) * 1.0));
      widthExpansion := tryExpansion;
    except
    end;

    (* not using this version
    { length and width expansion increase due to water uptake }
    with plant.pInternode do
      if self.age <= plant.pInternode.maxDaysToExpand then
        begin
        linearGrowthWithFactor(self.lengthExpansion,
            lengthMultiplierDueToExpansion, minDaysToExpand, 1.0); {1.0 was water stress factor}
        linearGrowthWithFactor(self.widthExpansion,
            widthMultiplierDueToExpansion, minDaysToExpand, 1.0);
        end;
    *)
    if plant.floweringHasStarted {and
      (plant.age - plant.ageAtWhichFloweringStarted <= plant.pInternode.maxDaysToBolt)} then
      with plant.pInternode do
        linearGrowthWithFactor(self.boltingExpansion, lengthMultiplierDueToBolting, minDaysToBolt, 1.0);
    end;
  self.checkIfSeedlingLeavesHaveAbscissed;
  self.calculateDistanceFromFirstPhytomer;
  except
    on e: Exception do messageForExceptionType(e, 'PdInternode.nextDay');
  end;
  end;

class function PdInternode.optimalInitialBiomass_pctMPB(plant: PdPlant): single;
  begin
  with plant.pInternode do
    result := safedivExcept(optimalFinalBiomass_pctMPB,
          lengthMultiplierDueToBiomassAccretion * widthMultiplierDueToBiomassAccretion, 0);
  end;

function PdInternode.propFullLength: single;
  begin
  with plant.pInternode do
    result := safedivExcept(self.totalBiomass_pctMPB * self.lengthExpansion * self.boltingExpansion,
      optimalFinalBiomass_pctMPB, 0);
  end;

function PdInternode.propFullWidth: single;
  begin
  with plant.pInternode do
    result := safedivExcept(self.totalBiomass_pctMPB * self.widthExpansion,
      optimalFinalBiomass_pctMPB, 0);
  end;

procedure PdInternode.traverseActivity(mode: integer; traverserProxy: TObject);
  var
    traverser: PdTraverser;
    biomassToRemove_pctMPB: single;
    targetBiomass_pctMPB: single;
  begin
  inherited traverseActivity(mode, traverserProxy);
  traverser := PdTraverser(traverserProxy);
  if traverser = nil then exit;
  if self.hasFallenOff and (mode <> kActivityStream) and (mode <> kActivityFree) then exit;
  begin
  try
  if (mode <> kActivityDraw) then
    begin
    if leftLeaf <> nil then leftLeaf.traverseActivity(mode, traverser);
    if rightLeaf <> nil then rightLeaf.traverseActivity(mode, traverser);
    end;
  case mode of
    kActivityNone: ;
    kActivityNextDay:
      begin
      self.nextDay;
      if self.age < traverser.ageOfYoungestPhytomer then traverser.ageOfYoungestPhytomer := self.age;
      end;
    kActivityDemandVegetative:
      begin
      if self.age > plant.pInternode.maxDaysToAccumulateBiomass then
        begin
        self.biomassDemand_pctMPB := 0.0;
        exit;
        end;
      try
      with plant.pInternode do
        begin
        if canRecoverFromStuntingDuringCreation then
          targetBiomass_pctMPB := optimalFinalBiomass_pctMPB
        else
          targetBiomass_pctMPB := optimalFinalBiomass_pctMPB * fractionOfOptimalInitialBiomassAtCreation_frn;
        self.biomassDemand_pctMPB := linearGrowthResult(self.liveBiomass_pctMPB,
            targetBiomass_pctMPB, minDaysToAccumulateBiomass);
        end;
      traverser.total := traverser.total + self.biomassDemand_pctMPB;
      except
        on e: Exception do messageForExceptionType(e, 'PdInternode.traverseActivity (vegetative demand)');
      end
      end;
    kActivityDemandReproductive:;
	    {Return reproductive demand recursively from all reproductive meristems and fruits connected to
      this phytomer. Phytomers, inflorescences, and flowers themselves have no demands.}
    kActivityGrowVegetative:
	    begin
      if self.age > plant.pInternode.maxDaysToAccumulateBiomass then exit;
      try
      self.newBiomassForDay_pctMPB := max(0.0, self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass);
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB + self.newBiomassForDay_pctMPB;
      except
        on e: Exception do messageForExceptionType(e, 'PdInternode.traverseActivity (vegetative growth)');
      end;
      end;
    kActivityGrowReproductive: ;
	    {Recurse available photosynthate allocated to reproductive growth to all plant parts.
      Only meristems and fruits will incorporate it.}
    kActivityStartReproduction: ;
     {Send signal to consider reproductive mode to all meristems on plant.}
    kActivityFindPlantPartAtPosition:
      begin
      if pointsAreCloseEnough(traverser.point, self.position) then
        begin
        traverser.foundPlantPart := self;
        traverser.finished := true;
        end;
      end;
    kActivityDraw: self.draw;
    kActivityReport: ;
    kActivityStream: self.streamUsingFiler(traverser.filer);
    kActivityFree: { free called by traverser };
    kActivityVegetativeBiomassThatCanBeRemoved:
      traverser.total := traverser.total + self.liveBiomass_pctMPB;
    kActivityRemoveVegetativeBiomass:
      begin
      biomassToRemove_pctMPB := self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB - biomassToRemove_pctMPB;
      self.deadBiomass_pctMPB := self.deadBiomass_pctMPB + biomassToRemove_pctMPB;
      end;
    kActivityReproductiveBiomassThatCanBeRemoved: { none };
    kActivityRemoveReproductiveBiomass: { none };
    kActivityGatherStatistics:
      begin
      self.addToStatistics(traverser.statistics, kStatisticsPartTypeStem);
      self.addToStatistics(traverser.statistics, kStatisticsPartTypeAllVegetative);
      end;
    kActivityCountPlantParts: ;
    kActivityFindPartForPartID: ;
    kActivityCountTotalMemoryUse: inc(traverser.totalMemorySize, self.instanceSize);
    kActivityCalculateBiomassForGravity:
      // on way up, do nothing; on way down, total up accumulated biomass
      if self.traversingDirection = kTraverseDone then
        self.biomassOfMeAndAllPartsAboveMe_pctMPB :=
          self.biomassOfMeAndAllPartsConnectedToMe_pctMPB + self.biomassOfPartsImmediatelyAboveMe_pctMPB;
    kActivityCountPointsAndTrianglesFor3DExport:
      begin
      self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser);
      end;
   else
      raise Exception.create('Problem: Unhandled mode in method PdInternode.traverseActivity.');
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdInternode.traverseActivity');
  end;
  end;
  end;

procedure PdInternode.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser);
  begin
  if traverser = nil then exit;
  inc(traverser.total3DExportStemSegments);
  addExportMaterial(traverser, kExportPartInternode, -1);
  if plant.pRoot.tdoParams.scaleAtFullSize > 0 then addExportMaterial(traverser, kExportPartRootTop, -1);
  end;

function PdInternode.isPhytomer: boolean;
  begin
  result := true;
  end;

procedure PdInternode.BlendColorsStrength(aColor: TColorRef; aStrength: single);
  begin
  if aStrength <= 0.0 then exit;
  internodeColor := blendColors(internodeColor, aColor, aStrength);
  end;

procedure PdInternode.setColorsToParameters;
  begin
  {Initialize phytomer colors at those in plant parameters, before stresses are considered.}
  internodeColor := plant.pInternode.faceColor;
  end;

procedure PdInternode.calculateInternodeAngle;
  begin
  if isFirstPhytomer then
    begin
    if (plant.pInternode.firstInternodeCurvingIndex = 0) then
      internodeAngle := 0
    else
      internodeAngle := 64.0  / 100.0  *
        (plant.randomNumberGenerator.randomNormalPercent(plant.pInternode.firstInternodeCurvingIndex));
    end
  else
    begin
    if (plant.pInternode.curvingIndex = 0) then
      internodeAngle := 0
    else
      internodeAngle := 64.0  / 100.0  *
        (plant.randomNumberGenerator.randomNormalPercent(plant.pInternode.curvingIndex));
    end;
  internodeAngle := self.angleWithSway(internodeAngle);
  end;

function PdInternode.distanceFromApicalMeristem: longint;
  var
    aPhytomer: PdInternode;
  begin
  {Count phytomers along this apex until you reach an apical meristem or inflorescence.}
  result := 0;
  if (self.nextPlantPart.isPhytomer) then
    aPhytomer := PdInternode(self.nextPlantPart)
  else
    aPhytomer := nil;
  while aPhytomer <> nil do
    begin
    inc(result);
    if (aPhytomer.nextPlantPart.isPhytomer) then
      aPhytomer := PdInternode(aPhytomer.nextPlantPart)
    else
      aPhytomer := nil;
    end;
  end;

procedure PdInternode.calculateDistanceFromFirstPhytomer;
  var
    aPhytomer: PdInternode;
    result: longint;
  begin
  {Count phytomers backwards along this apex until you reach the first.}
  result := 0;
  if isFirstPhytomer then exit;
  aPhytomer := phytomerAttachedTo;
  while aPhytomer <> nil do
    begin
    inc(result);
    aPhytomer := aPhytomer.phytomerAttachedTo;
    end;
  self.distanceFromFirstPhytomer := result;
  end;

function PdInternode.firstPhytomerOnBranch: PdInternode;
  begin
  result := self;
  while result <> nil do
    begin
    if (result.phytomerAttachedTo <> nil) and (result.phytomerAttachedTo.nextPlantPart = result) then
      result := PdInternode(result.phytomerAttachedTo)
    else
      break;
    end;
  if result = self then
    result := nil;
  end;

function PdInternode.biomassOfMeAndAllPartsConnectedToMe_pctMPB: single;
  begin
  result := self.totalBiomass_pctMPB;
  if leftLeaf <> nil then result := result + leftLeaf.totalBiomass_pctMPB;
  if rightLeaf <> nil then result := result + rightLeaf.totalBiomass_pctMPB;
  end;

function PdInternode.biomassOfPartsImmediatelyAboveMe_pctMPB: single;
  begin
  result := 0;
  if leftBranchPlantPart <> nil then
     result := result + leftBranchPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB;
  if rightBranchPlantPart <> nil then
     result := result + rightBranchPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB;
  if nextPlantPart <> nil then
     result := result + nextPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB;
  end;

procedure PdInternode.draw;
  var
    turtle: KfTurtle;
  begin
  {Draw all parts of phytomer. Consider if the phytomer is the first (has the seedling leaves) and whether
    the leaves attached to this phytomer have abscissed (and are not drawn).}
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  self.boundsRect := Rect(0, 0, 0, 0);
  if self.hiddenByAmendment then
    begin
    // if internode is hidden the leaves could still be drawn, if they are posed.
    // if they are themselves hidden, they will pop back out without drawing.
    if leftLeaf <> nil then leftLeaf.drawWithDirection(kDirectionLeft);
    if rightLeaf <> nil then rightLeaf.drawWithDirection(kDirectionRight);
    exit;  // amendment rotations handled in drawStemSegment
    end;
  try
    if plant.needToRecalculateColors then self.calculateColors;
    if (isFirstPhytomer) and (plant.pRoot.showsAboveGround) then drawRootTop;
    drawInternode;
    if leftLeaf <> nil then leftLeaf.drawWithDirection(kDirectionLeft);
    if rightLeaf <> nil then rightLeaf.drawWithDirection(kDirectionRight);
  except
    on e: Exception do messageForExceptionType(e, 'PdInternode.draw');
  end;
  end;

procedure PdInternode.drawInternode;
  var
    length, width, zAngle: single;
  begin
  if (plant.turtle = nil) then exit;
  zAngle := internodeAngle;
  if (self.phytomerAttachedTo <> nil) then
    begin
    if (self.phytomerAttachedTo.leftBranchPlantPart = self) then
      zAngle := zAngle + plant.pMeristem.branchingAngle
    else if (self.phytomerAttachedTo.rightBranchPlantPart = self) then
      begin
      zAngle := zAngle + plant.pMeristem.branchingAngle;
      plant.turtle.RotateX(128);
      end
    end;
  length := max(0.0, propFullLength * plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm);
  width := max(0.0, propFullWidth * plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm);
  self.drawStemSegment(length, width, zAngle, 0, internodeColor, kDontTaper,
      kExportPartInternode, kUseAmendment);
  end;

procedure PdInternode.drawRootTop;
  var
    turtle: KfTurtle;
    scale: single;
    numParts: integer;
    tdo: KfObject3D;
    minZ: single;
    i: integer;
  begin
  {Draw top of root above ground, if it can be seen. Adjust size for heat unit index of plant. }
  numParts := 5; {constant}
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  scale := safedivExcept(plant.age, plant.pGeneral.ageAtMaturity, 0) * plant.pRoot.tdoParams.scaleAtFullSize / 100.0;
  turtle.push;
  minZ := 0;
  tdo := plant.pRoot.tdoParams.object3D;
  turtle.ifExporting_startPlantPart(self.longNameForDXFPartConsideringGenderEtc(kExportPartRootTop),
      self.longNameForDXFPartConsideringGenderEtc(kExportPartRootTop));
  if numParts > 0 then
    for i := 0 to numParts  - 1 do
      begin
		  turtle.RotateX(256 div numParts);
      turtle.push;
      turtle.RotateZ(64);
      turtle.RotateY(-64);
      if tdo <> nil then
        begin
        turtle.rotateX(self.angleWithSway(plant.pRoot.tdoParams.xRotationBeforeDraw));
        turtle.rotateY(self.angleWithSway(plant.pRoot.tdoParams.yRotationBeforeDraw));
        turtle.rotateZ(self.angleWithSway(plant.pRoot.tdoParams.zRotationBeforeDraw));
        with plant.pRoot.tdoParams do
          self.draw3DObject(tdo, scale, faceColor, backfaceColor, kExportPartRootTop);
        if i = 1 then
          minZ := tdo.zForSorting
        else if tdo.zForSorting < minZ then
          minZ := tdo.zForSorting;
        end;
      turtle.pop;
      end;
  if tdo <> nil then tdo.zForSorting := minZ;
  turtle.pop;
  turtle.ifExporting_endPlantPart;
  end;

procedure PdInternode.report;
  begin
  inherited report;
  //debugPrint('internode, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
  {DebugForm.printNested(plant.turtle.stackSize, 'phytomer, age ' + IntToStr(age));}
  end;

procedure PdInternode.checkIfSeedlingLeavesHaveAbscissed;
  begin
  {If first phytomer, only want to draw seedling leaves for some time after emergence.
  For monopodial plant, stop drawing seedling leaves some number of nodes after emergence (parameter).
  For sympodial plant, this doesn't work; use age of meristem instead; age is set as constant.}
  if (not isFirstPhytomer) then exit;
  if (plant.pMeristem.branchingIsSympodial) then
    begin
    if (age < 10) then exit;
    end
  else
    begin
    if (self.distanceFromApicalMeristem <= plant.pSeedlingLeaf.nodesOnStemWhenFallsOff) then exit;
    end;
  { absolute cut-off }
  if safedivExcept(plant.age, plant.pGeneral.ageAtMaturity, 0) < 0.25 then exit;
  { CFK FIX - should really have removed biomass in seedling leaves from model plant }
  if leftLeaf <> nil then leftLeaf.hasFallenOff := true;
  if rightLeaf <> nil then rightLeaf.hasFallenOff := true;
  end;

function PdInternode.partType: integer;
  begin
  result := kPartTypePhytomer;
  end;

procedure PdInternode.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdInternode;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure PdInternode.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
    streamColorRef(internodeColor);
    streamSingle(internodeAngle);
    streamSingle(lengthExpansion);
    streamSingle(widthExpansion);
    streamSingle(boltingExpansion);
    streamSingle(fractionOfOptimalInitialBiomassAtCreation_frn);
    streamByte(traversingDirection);
    streamBoolean(isFirstPhytomer);
    streamSingle(newBiomassForDay_pctMPB);
    end;
  {reading or writing the plant part subobject phytomers will be done by traverser}
  {for now, just need to create these objects if needed and set plant and phytomerAttachedTo}
  {if it is an inflorescence - read it now}
  self.streamPlantPart(filer, leftBranchPlantPart);
  self.streamPlantPart(filer, rightBranchPlantPart);
  self.streamPlantPart(filer, nextPlantPart);
  self.streamPlantPart(filer, PdPlantPart(leftLeaf));
  self.streamPlantPart(filer, PdPlantPart(rightLeaf));
  end;

procedure PdInternode.streamPlantPart(filer: PdFiler; var plantPart: PdPlantPart);
  var
   partType: smallint;
  begin
  if filer.isWriting then
    begin
    if plantPart = nil then
      partType := kPartTypeNone
    else
      partType := plantPart.partType;
    filer.streamSmallint(partType);
    case partType of
      kPartTypeMeristem, kPartTypeInflorescence, kPartTypeLeaf:
        plantPart.streamUsingFiler(filer);
      end;
    end
  else if filer.isReading then
    begin
    filer.streamSmallint(partType);
    case partType of
  		kPartTypeNone:
        plantPart := nil; 
  		kPartTypeMeristem:
        begin
        plantPart := PdMeristem.create;
        plantPart.plant := self.plant;
        PdMeristem(plantPart).phytomerAttachedTo := self;
        plantPart.streamUsingFiler(filer);
        end;
  		kPartTypeInflorescence:
        begin
        plantPart := PdInflorescence.create;
        plantPart.plant := self.plant;
        PdInflorescence(plantPart).phytomerAttachedTo := self;
        plantPart.streamUsingFiler(filer);
        end;
  		kPartTypePhytomer:
        begin
        plantPart := PdInternode.create;
        plantPart.plant := self.plant;
        PdInternode(plantPart).phytomerAttachedTo := self;
        {will be streamed in by traverser}
        end;
  		kPartTypeLeaf:
        begin
        plantPart := PdLeaf.create;
        plantPart.plant := self.plant;
        plantPart.streamUsingFiler(filer);
        // PDF PORT inserted semicolon
        end;
      else
        Exception.create('PdInternode: unknown plant part type ' + intToStr(partType));
    end;
    end;
  end;

end.
