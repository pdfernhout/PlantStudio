unit umerist;

interface

uses WinProcs, WinTypes,
  upart, uintern, uplant, ufiler, utravers;

type 

PdMeristem = class(PdPlantPart)
  public 
  phytomerAttachedTo: PdInternode;
  daysCreatingThisPlantPart: longint;
  isActive: boolean;
  isApical: boolean;
  isReproductive: boolean;
  gender: smallint;
	constructor newWithPlant(aPlant: PdPlant);
  function getName: string; override;
	procedure InitializeWithPlant(aPlant: PdPlant);
  procedure setIfActive(active: boolean);
  procedure setIfApical(apical: boolean);
  procedure setIfReproductive(reproductive: boolean);
	function contemplateBranching: boolean;
	function createAxillaryMeristem(direction: integer): PdMeristem;
	function createFirstPhytomer: PdInternode;
	procedure createInflorescence(fractionOfOptimalSize: single);
	procedure createPhytomer(fractionOfFullSize: single);
	function decideIfActiveFemale: boolean;
	function decideIfActiveHermaphroditic: boolean;
	function decideIfActiveMale: boolean;
	procedure draw; override;
	procedure nextDay;  override;
	procedure startReproduction;
  procedure report; override;
	function partType: integer; override;
	function willCreateInflorescence: boolean;
  procedure traverseActivity(mode: integer; traverserProxy: TObject); override;
  destructor destroy; override;
  procedure accumulateOrCreatePhytomer;
  procedure accumulateOrCreateInflorescence;
  function optimalInitialPhytomerBiomass_pctMPB: single;
  procedure countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser);
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  end;

implementation

uses SysUtils, Dialogs, Classes,
  udebug, uturtle, u3dexport, udomain, utdo, umath, uinflor, uleaf, uclasses, usupport;

constructor PdMeristem.NewWithPlant(aPlant: PdPlant);
  begin
  self.create;
  self.InitializeWithPlant(aPlant);
  end;

destructor PdMeristem.destroy;
  begin
  if isReproductive then
    begin
    if isActive then
      begin
      if isApical then
        dec(plant.numApicalActiveReproductiveMeristemsOrInflorescences)
      else {not isApical}
        dec(plant.numAxillaryActiveReproductiveMeristemsOrInflorescences);
      end
    else {not isActive}
      begin
      if isApical then
        dec(plant.numApicalInactiveReproductiveMeristems)
      else {not isApical}
        dec(plant.numAxillaryInactiveReproductiveMeristems);
      end;
    end;
  inherited destroy;
  end;

procedure PdMeristem.InitializeWithPlant(aPlant: PdPlant);
  begin
  initialize(aPlant); // v1.6b1 removed inherited
  { don't need to call any setIf... functions here because lists don't need to be changed yet }
  isApical := true;
  liveBiomass_pctMPB := 0.0;
  deadBiomass_pctMPB := 0.0;
  biomassDemand_pctMPB := 0.0;
  daysCreatingThisPlantPart := 0;
  isActive := false;
  isReproductive := false;
  gender := kGenderFemale;
  if plant.floweringHasStarted and
    (plant.randomNumberGenerator.zeroToOne <= plant.pMeristem.determinateProbability) then
    self.setIfReproductive(true);
  end;

function PdMeristem.getName: string;
  begin
  result := 'meristem';
  end;

procedure PdMeristem.nextDay;
  begin
  try
  inherited nextDay;
  if isActive then
    begin
    inc(self.daysCreatingThisPlantPart);
    if not isReproductive then
      self.accumulateOrCreatePhytomer
    else
      self.accumulateOrCreateInflorescence;
    end
  else
    begin
    if not isApical and not isReproductive and contemplateBranching then self.setIfActive(true);
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdMeristem.nextDay');
  end;
  end;

function PdMeristem.contemplateBranching: boolean;
  var
    decisionPercent, randomPercent: single;
    firstOnBranch: PdInternode;
  begin
  //Decide if this meristem is going to become active and branch (start demanding photosynthate).
  //This method is called once per day to create a large pool of random tests, each with
  //very small probability, leading to a small number of occurrences with small variation.
  if plant.pMeristem.branchingIndex = 0 then
    begin
    result := false;
    exit;
    end;
  if not plant.pMeristem.secondaryBranchingIsAllowed then
    begin
    firstOnBranch := phytomerAttachedTo.firstPhytomerOnBranch;
    if (firstOnBranch <> plant.firstPhytomer) then
      begin
      result := false;
      exit;
      end;
    end;
  if plant.pMeristem.branchingIndex = 100 then
    begin
    result := true;
    exit;
    end;
  if phytomerAttachedTo.distanceFromApicalMeristem < plant.pMeristem.branchingDistance then
    begin
    if plant.pMeristem.branchingDistance = 0 then
      decisionPercent := plant.pMeristem.branchingIndex
    else
      decisionPercent := plant.pMeristem.branchingIndex
        * min(1.0, max(0.0,
          safedivExcept(phytomerAttachedTo.distanceFromApicalMeristem, plant.pMeristem.branchingDistance, 0)));
    randomPercent := plant.randomNumberGenerator.randomPercent;
    result := randomPercent < decisionPercent;
    end
  else
    begin
    decisionPercent := plant.pMeristem.branchingIndex;
    randomPercent := plant.randomNumberGenerator.randomPercent;
    result := randomPercent < decisionPercent;
    end;
  end;

function PdMeristem.optimalInitialPhytomerBiomass_pctMPB: single;
  begin
  result := PdInternode.optimalInitialBiomass_pctMPB(plant) + PdLeaf.optimalInitialBiomass_pctMPB(plant);
  if plant.pMeristem.branchingAndLeafArrangement = kArrangementOpposite then
    result := result + PdLeaf.optimalInitialBiomass_pctMPB(plant);
  end;

procedure PdMeristem.accumulateOrCreatePhytomer;
  var
    optimalInitialBiomass_pctMPB, minBiomassNeeded_pctMPB: single;
    fractionOfOptimalSize: single;
    shouldCreatePhytomer: boolean;
  begin
  try
  shouldCreatePhytomer := false;
  optimalInitialBiomass_pctMPB := self.optimalInitialPhytomerBiomass_pctMPB;
  if (self.liveBiomass_pctMPB >= optimalInitialBiomass_pctMPB) then
    shouldCreatePhytomer := true
  else
    begin
    minBiomassNeeded_pctMPB := optimalInitialBiomass_pctMPB
        * plant.pInternode.minFractionOfOptimalInitialBiomassToCreateInternode_frn;
    if (self.liveBiomass_pctMPB >= minBiomassNeeded_pctMPB)
      and (daysCreatingThisPlantPart >= plant.pInternode.maxDaysToCreateInternodeIfOverMinFraction) then
      shouldCreatePhytomer := true;
    end;
  if shouldCreatePhytomer then
    begin
    fractionOfOptimalSize := safedivExcept(liveBiomass_pctMPB, optimalInitialBiomass_pctMPB, 0);
    self.createPhytomer(fractionOfOptimalSize);
    self.liveBiomass_pctMPB := 0.0;
    self.daysCreatingThisPlantPart := 0;
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdMeristem.accumulateOrCreatePhytomer');
  end;
  end;

procedure PdMeristem.accumulateOrCreateInflorescence;
  var
    optimalInitialBiomass_pctMPB, minBiomassNeeded_pctMPB, fractionOfOptimalSize: single;
    shouldCreateInflorescence: boolean;
  begin
  try
  if phytomerAttachedTo.isFirstPhytomer or not isReproductive or not isActive then exit;
  shouldCreateInflorescence := false;
  optimalInitialBiomass_pctMPB := PdInflorescence.optimalInitialBiomass_pctMPB(plant, gender);
  if (self.liveBiomass_pctMPB >= optimalInitialBiomass_pctMPB) then
    shouldCreateInflorescence := true
  else
    begin
    minBiomassNeeded_pctMPB := optimalInitialBiomass_pctMPB
      * plant.pInternode.minFractionOfOptimalInitialBiomassToCreateInternode_frn;
    if (self.liveBiomass_pctMPB >= minBiomassNeeded_pctMPB)
      and (daysCreatingThisPlantPart >= plant.pInflor[gender].maxDaysToCreateInflorescenceIfOverMinFraction) then
      shouldCreateInflorescence := true;
    end;
  if shouldCreateInflorescence then
    begin
    fractionOfOptimalSize := safedivExcept(liveBiomass_pctMPB, optimalInitialBiomass_pctMPB, 0);
    self.createInflorescence(fractionOfOptimalSize);
    self.liveBiomass_pctMPB := 0.0;
    self.daysCreatingThisPlantPart := 0;
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdMeristem.accumulateOrCreateInflorescence');
  end;
  end;

procedure PdMeristem.traverseActivity(mode: integer; traverserProxy: TObject);
  var
    traverser: PdTraverser;
    optimalBiomass_pctMPB, biomassToRemove_pctMPB: single;
  begin
  inherited traverseActivity(mode, traverserProxy);
  traverser := PdTraverser(traverserProxy);
  if traverser = nil then exit;
  if self.hasFallenOff and (mode <> kActivityStream) and (mode <> kActivityFree) then exit;
  try
  case mode of
    kActivityNone: ;
    kActivityNextDay: self.nextDay;
    kActivityDemandVegetative:
      begin
      // return vegetative demand to create a phytomer. no demand if meristem is inactive, meristem is
      // in reproductive mode, or if meristem is axillary and attached to the first phytomer
      // and there is NOT sympodial branching.
      if (not isActive) or (isReproductive) then exit;
      if ((not isApical) and (phytomerAttachedTo.isFirstPhytomer) and
        (not plant.pMeristem.branchingIsSympodial)) then exit;
      try
      optimalBiomass_pctMPB := PdInternode.optimalInitialBiomass_pctMPB(plant) + PdLeaf.optimalInitialBiomass_pctMPB(plant);
      if plant.pMeristem.branchingAndLeafArrangement = kArrangementOpposite then
        optimalBiomass_pctMPB := optimalBiomass_pctMPB + PdLeaf.optimalInitialBiomass_pctMPB(plant);
      self.biomassDemand_pctMPB := linearGrowthResult(self.liveBiomass_pctMPB,
        optimalBiomass_pctMPB, plant.pInternode.minDaysToCreateInternode);
      traverser.total := traverser.total + self.biomassDemand_pctMPB;
      except
        on e: Exception do messageForExceptionType(e, 'PdMeristem.traverseActivity (vegetative demand)');
      end
      end;
   kActivityDemandReproductive:
      begin
      // return reproductive demand to create an inflorescence. no demand if meristem is inactive,
      // if it is in vegetative mode, or if it is attached to the first phytomer.
      if (not isActive) or (not isReproductive) then exit;
      if (phytomerAttachedTo.isFirstPhytomer) and (not isApical) then exit;
      try
      with plant.pInflor[gender] do
        self.biomassDemand_pctMPB := linearGrowthResult(self.liveBiomass_pctMPB,
          optimalBiomass_pctMPB, minDaysToCreateInflorescence);
      traverser.total := traverser.total + self.biomassDemand_pctMPB;
      except
        on e: Exception do messageForExceptionType(e, 'PdMeristem.traverseActivity (reproductive demand)');
      end
      end;
    kActivityGrowVegetative:
      begin
      {Allocate new biomass by portion of demand. A phytomer cannot be made before the minimum number
      of days has passed to make one phytomer.}
      if not (isActive) then exit;
      if isReproductive then exit;
      try
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB + self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
      except
        on e: Exception do messageForExceptionType(e, 'PdMeristem.traverseActivity (vegetative growth)');
      end;
      end;
    kActivityGrowReproductive:
      begin
      if (not isActive) or (not isReproductive) then exit;
      try
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB + self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
      except
        on e: Exception do messageForExceptionType(e, 'PdMeristem.traverseActivity (reproductive growth)');
      end;
      end;
    kActivityStartReproduction: self.startReproduction;
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
    kActivityStream: {called by phytomer} ;
    kActivityFree: { free called by phytomer or inflorescence };
    kActivityVegetativeBiomassThatCanBeRemoved, kActivityReproductiveBiomassThatCanBeRemoved:
      begin
      if not isActive then exit;
      if (mode = kActivityVegetativeBiomassThatCanBeRemoved) and (isReproductive) then exit;
      if (mode = kActivityReproductiveBiomassThatCanBeRemoved) and (not isReproductive) then exit;
      try
      { a meristem can lose all of its biomass }
      traverser.total := traverser.total + self.liveBiomass_pctMPB;
      except
        on e: Exception do messageForExceptionType(e, 'PdMeristem.traverseActivity (removal request)');
      end;
      end;
    kActivityRemoveVegetativeBiomass, kActivityRemoveReproductiveBiomass:
      begin
      if not isActive then exit;
      if (mode = kActivityRemoveVegetativeBiomass) and (isReproductive) then exit;
      if (mode = kActivityRemoveReproductiveBiomass) and (not isReproductive) then exit;
      try
      biomassToRemove_pctMPB := self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB - biomassToRemove_pctMPB;
      self.deadBiomass_pctMPB := self.deadBiomass_pctMPB + biomassToRemove_pctMPB;
      except
        on e: Exception do messageForExceptionType(e, 'PdMeristem.traverseActivity (removal)');
      end;
      end;
    kActivityGatherStatistics:
      begin
      self.addToStatistics(traverser.statistics, kStatisticsPartTypeAxillaryBud);
      if isReproductive then
        self.addToStatistics(traverser.statistics, kStatisticsPartTypeAllReproductive)
      else
        self.addToStatistics(traverser.statistics, kStatisticsPartTypeAllVegetative);
      end;
    kActivityCountPlantParts: ;
    kActivityFindPartForPartID: ;
    kActivityCountTotalMemoryUse: inc(traverser.totalMemorySize, self.instanceSize);
    kActivityCalculateBiomassForGravity: ;
    kActivityCountPointsAndTrianglesFor3DExport:
      begin
      self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser);
      end;
   else
      raise Exception.create('Problem: Unhandled mode in method PdMeristem.traverseActivity.');
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdMeristem.traverseActivity');
  end;
  end;

procedure PdMeristem.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser);
  begin
  if traverser = nil then exit;
  with plant.pAxillaryBud.tdoParams do if scaleAtFullSize > 0 then
    begin
    inc(traverser.total3DExportPointsIn3DObjects, object3d.pointsInUse * repetitions);
    inc(traverser.total3DExportTrianglesIn3DObjects, object3d.triangles.count * repetitions);
    addExportMaterial(traverser, kExportPartMeristem, -1);
    end;
  end;

procedure PdMeristem.report;
  begin
  inherited report;
  //debugPrint('meristem, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
  {DebugForm.printNested(plant.turtle.stackSize, 'meristem, age ' + IntToStr(age) + ' biomass '
    + floatToStr(liveBiomass_pctMPB));}
  end;

function PdMeristem.createAxillaryMeristem(direction: integer): PdMeristem;
  var
    newMeristem: PdMeristem;
  begin
  // create new axillary meristem attached to the same phytomer as this apical meristem is attached to.
  newMeristem := PdMeristem.create;
  newMeristem.InitializeWithPlant(plant);
  newMeristem.setIfApical(false);
  newMeristem.PhytomerAttachedTo := phytomerAttachedTo;
  if (direction = kDirectionLeft) then
    phytomerAttachedTo.LeftBranchPlantPart := newMeristem
  else
    phytomerAttachedTo.RightBranchPlantPart := newMeristem;
  result := newMeristem;
  end;

procedure PdMeristem.setIfActive(active: boolean);
  begin
  if isActive <> active then
    begin
    isActive := active;
    if isReproductive then
      if isApical then
        begin
        if isActive then
          begin
          inc(plant.numApicalActiveReproductiveMeristemsOrInflorescences);
          dec(plant.numApicalInactiveReproductiveMeristems);
          end
        else {not isActive}
          begin
          inc(plant.numApicalInactiveReproductiveMeristems);
          dec(plant.numApicalActiveReproductiveMeristemsOrInflorescences);
          end;
       end
     else {not isApical}
       begin
       if isActive then
         begin
         inc(plant.numAxillaryActiveReproductiveMeristemsOrInflorescences);
         dec(plant.numAxillaryInactiveReproductiveMeristems);
         end
       else {not isActive}
         begin
         inc(plant.numAxillaryInactiveReproductiveMeristems);
         dec(plant.numAxillaryActiveReproductiveMeristemsOrInflorescences);
         end;
       end;
     end;
  end;

procedure PdMeristem.setIfApical(apical: boolean);
  begin
  if isApical <> apical then
    begin
    isApical := apical;
    if isReproductive then
      if isActive then
        begin
        if isApical then
          begin
          inc(plant.numApicalActiveReproductiveMeristemsOrInflorescences);
          dec(plant.numAxillaryActiveReproductiveMeristemsOrInflorescences);
          end
        else {not isApical}
          begin
          inc(plant.numAxillaryActiveReproductiveMeristemsOrInflorescences);
          dec(plant.numApicalActiveReproductiveMeristemsOrInflorescences);
          end;
       end
     else {not isActive}
       begin
        if isApical then
          begin
          inc(plant.numApicalInactiveReproductiveMeristems);
          dec(plant.numAxillaryInactiveReproductiveMeristems);
          end
        else {not isApical}
          begin
          inc(plant.numAxillaryInactiveReproductiveMeristems);
          dec(plant.numApicalInactiveReproductiveMeristems);
          end;
       end;
     end;
  end;

procedure PdMeristem.setIfReproductive(reproductive: boolean);
  begin
  {assume can only become reproductive and not go other way}
  if isReproductive <> reproductive then
    begin
    isReproductive := reproductive;
    if isActive then
      begin
      if isApical then
        inc(plant.numApicalActiveReproductiveMeristemsOrInflorescences)
      else {not isApical}
        inc(plant.numAxillaryActiveReproductiveMeristemsOrInflorescences);
      end
    else {not isActive}
      begin
      if isApical then
        inc(plant.numApicalInactiveReproductiveMeristems)
      else {not isApical}
        inc(plant.numAxillaryInactiveReproductiveMeristems);
      end;
    end;
  end;

    // create first phytomer of plant with optimal biomass. return phytomer created so plant can hold on to it.
function PdMeristem.createFirstPhytomer: PdInternode;
  begin
  result := nil;
  try
    //CreatePhytomer(self.optimalInitialPhytomerBiomass_pctMPB);
    CreatePhytomer(1.0); // v1.6b1 -- biomass was wrong, should be fraction
    result := phytomerAttachedTo;
    if plant.pGeneral.isDicot then
      result.makeSecondSeedlingLeaf(self.optimalInitialPhytomerBiomass_pctMPB);
  except
    on e: Exception do messageForExceptionType(e, 'PdMeristem.createFirstPhytomer');
  end;
  end;

  // create new inflorescence. attach new inflor to phytomer this meristem is attached to,
  // then unattach this meristem from the phytomer and tell inflor pointer to self so inflor can free self
  // when it is freed.
procedure PdMeristem.createInflorescence(fractionOfOptimalSize: single);
  var
    newInflorescence: PdInflorescence;
  begin
  if plant.partsCreated > domain.options.maxPartsPerPlant_thousands * 1000 then exit;  // v1.6b1
  newInflorescence := PdInflorescence.create;
  newInflorescence.InitializeGenderApicalOrAxillary(plant, gender, isApical, fractionOfOptimalSize);
  newInflorescence.meristemThatCreatedMe := self;
  newInflorescence.phytomerAttachedTo := self.phytomerAttachedTo;
  if isApical then
    phytomerAttachedTo.NextPlantPart := newInflorescence
  else if phytomerAttachedTo.LeftBranchPlantPart = self then
    phytomerAttachedTo.LeftBranchPlantPart := newInflorescence
  else if phytomerAttachedTo.RightBranchPlantPart = self then
    phytomerAttachedTo.RightBranchPlantPart := newInflorescence
  else
    raise Exception.create('Problem: Branching incorrect in method PdMeristem.createInflorescence.');
  PhytomerAttachedTo := nil;
  end;

procedure PdMeristem.createPhytomer(fractionOfFullSize: single);
  var
    newPhytomer: PdInternode;
    leftMeristem, rightMeristem: PdMeristem;
  begin
  // create new phytomer. fraction of full size is the amount of biomass the meristem accumulated
  // (in the number of days it had to create a phytomer) divided by the optimal biomass of a phytomer.
  if plant.partsCreated > domain.options.maxPartsPerPlant_thousands * 1000 then exit;  // v1.6b1
  newPhytomer := PdInternode.NewWithPlantFractionOfInitialOptimalSize(plant, fractionOfFullSize);
  newPhytomer.phytomerAttachedTo := self.phytomerAttachedTo;
  if (phytomerAttachedTo <> nil) then
    begin
    if isApical then
      begin
      phytomerAttachedTo.NextPlantPart := newPhytomer;
      if (plant.pMeristem.branchingIsSympodial) then self.setIfActive(false);
      end
    else { axillary }
      begin
      if phytomerAttachedTo.LeftBranchPlantPart = self then
        phytomerAttachedTo.LeftBranchPlantPart := newPhytomer
      else if phytomerAttachedTo.RightBranchPlantPart = self then
        phytomerAttachedTo.RightBranchPlantPart := newPhytomer
      else
        raise Exception.create('Problem: Branching incorrect in method PdMeristem.createPhytomer.');
      self.setIfApical(true);
      end;
    // set up pointers
    self.phytomerAttachedTo := newPhytomer;
    self.phytomerAttachedTo.NextPlantPart := self;
    if plant.pMeristem.branchingAndLeafArrangement = kArrangementAlternate then
      begin
      leftMeristem := CreateAxillaryMeristem(kDirectionLeft);
      if plant.pMeristem.branchingIsSympodial then leftMeristem.setIfActive(true);
      end
    else
      begin
      leftMeristem := CreateAxillaryMeristem(kDirectionLeft);
      rightMeristem := CreateAxillaryMeristem(kDirectionRight);
      if plant.pMeristem.branchingIsSympodial then
        if (plant.randomNumberGenerator.zeroToOne < 0.5) then
          leftMeristem.setIfActive(true)
        else
          rightMeristem.setIfActive(true);
      end;
    end
  else // phytomerAttachedTo = nil (means this is first phytomer)
    begin
    self.setIfApical(true);
    self.setIfActive(not plant.pMeristem.branchingIsSympodial);
    // set up pointers
    self.phytomerAttachedTo := newPhytomer;
    self.phytomerAttachedTo.NextPlantPart := self;
    if plant.pMeristem.branchingIsSympodial then
      begin
      if plant.pMeristem.branchingAndLeafArrangement = kArrangementAlternate then
        begin
        leftMeristem := CreateAxillaryMeristem(kDirectionLeft);
        leftMeristem.setIfActive(true);
        end
      else
        begin
        leftMeristem := CreateAxillaryMeristem(kDirectionLeft);
        rightMeristem := CreateAxillaryMeristem(kDirectionRight);
        if (plant.randomNumberGenerator.zeroToOne < 0.5) then
          leftMeristem.setIfActive(true)
        else
          rightMeristem.setIfActive(true);
        end;
      end;
    end;
  end;

procedure PdMeristem.draw;
  var i: integer;
  var
    turtle: KfTurtle;
    scale: single;
    daysToFullSize: single;
    numParts: integer;
    tdo: KfObject3D;
    minZ: single;
  begin
  if (plant.paxillaryBud.tdoParams.scaleAtFullSize = 0) then exit;
  {Draw meristem (only if buds are enlarged as in Brussels sprouts). Since this only very rarely happens,
  have these buds increase to maximum size in a constant number of days (5). Number of sections drawn
  (of the 3D object being rotated) is also set to a constant (5).}
  turtle := plant.turtle;                            
  if (turtle = nil) then exit;
  self.boundsRect := Rect(0, 0, 0, 0);
  if self.hiddenByAmendment then exit else self.applyAmendmentRotations;
  daysToFullSize := 5;
  scale := (plant.pAxillaryBud.tdoParams.scaleAtFullSize / 100.0) * (Min(1.0, safedivExcept(age, daysToFullSize, 0)));
  if isApical then exit;
  try
    numParts := 5;
    minZ := 0;
    tdo := plant.pAxillaryBud.tdoParams.object3D;
    turtle.ifExporting_startPlantPart(self.longNameForDXFPartConsideringGenderEtc(kExportPartMeristem),
        self.longNameForDXFPartConsideringGenderEtc(kExportPartMeristem));
    if numParts > 0 then
      for i := 0 to numParts - 1 do
    	  begin
			  turtle.RotateX(256 div numParts);
    	  turtle.push;
    	  turtle.RotateZ(-64);
        if tdo <> nil then
          begin
          turtle.rotateX(self.angleWithSway(plant.pAxillaryBud.tdoParams.xRotationBeforeDraw));
          turtle.rotateY(self.angleWithSway(plant.pAxillaryBud.tdoParams.yRotationBeforeDraw));
          turtle.rotateZ(self.angleWithSway(plant.pAxillaryBud.tdoParams.zRotationBeforeDraw));
          with plant.pAxillaryBud.tdoParams do
            self.draw3DObject(tdo, scale, faceColor, backfaceColor, kExportPartMeristem);
          if i = 1 then
            minZ := tdo.zForSorting
          else if tdo.zForSorting < minZ then
            minZ := tdo.zForSorting;
          end;
    	  turtle.pop;
    	  end;
    if tdo <> nil then tdo.zForSorting := minZ;
    turtle.ifExporting_endPlantPart;
  except
    on e: Exception do messageForExceptionType(e, 'PdMeristem.draw');
  end;
  end;

procedure PdMeristem.startReproduction;
  begin
  {Decide gender and activity based on whether the plant has hermaphroditic or separate flowers, and if
    hermaphroditic, female and/or male flowers are located terminally or axially.}
  if (plant.randomNumberGenerator.zeroToOne <= plant.pMeristem.determinateProbability) then
    self.setIfReproductive(true);
  if not isReproductive then exit;
  self.setIfActive(false);
  gender := kGenderFemale;
  if not plant.pGeneral.maleFlowersAreSeparate then
    begin
    if self.decideIfActiveHermaphroditic then Gender := kGenderFemale;
    end
  else
    begin
    if self.decideIfActiveMale then Gender := kGenderMale;
    if self.decideIfActiveFemale then Gender := kGenderFemale;
    end;
  if self.willCreateInflorescence then
    self.setIfActive(true);
  end;

function PdMeristem.decideIfActiveFemale: boolean;
  begin
  {For the case of separate male and female flowers, decide if this meristem will be able to create
  a female inflorescence. Called by decideReproductiveGenderAndActivity.}
  {If meristem is already male, then both male and female flowers are apical (or axillary).
  in that case, override with female only half the time.}
  result := (isApical = plant.pInflor[kGenderFemale].isTerminal);
  if result and (gender = kGenderMale) then
    result := (plant.randomNumberGenerator.zeroToOne < 0.5);
  end;

function PdMeristem.decideIfActiveHermaphroditic: boolean;
  begin
  {For the case of hermaphroditic flowers, decide if this meristem will be able to create
  a hermaphroditic inflorescence (if flowers are hermaphroditic, female parameters are used).
  Called by decideReproductiveGenderAndActivity.}
  result := (isApical = plant.pInflor[kGenderFemale].isTerminal);
  end;

function PdMeristem.decideIfActiveMale: boolean;
  begin
  {For the case of separate male and female flowers, decide if this meristem will be able to create
  a male inflorescence. Called by decideReproductiveGenderAndActivity.}
  result := (isApical = plant.pInflor[kGenderMale].isTerminal);
  end;

function PdMeristem.partType: integer;
  begin
  result := kPartTypeMeristem;
  end;

function PdMeristem.willCreateInflorescence: boolean;
  var
    inflorProb: single;
    numExpected: single;
    numAlready: single;
  begin
  try
  {Determine probability that this meristem will produce an inflorescence, which is
  number of inflorescences left to be placed on plant / number of meristems open to develop
  (apical meristems if flowering is apical, or axillary meristems if flowering is axillary).
  First phytomer on plant is for seedling leaves and cannot produce inflorescences.}
  if (phytomerAttachedTo.isFirstPhytomer) and (not isApical) then
    begin
    result := false;
    exit;
    end;
  if isApical then
    begin
    numExpected := plant.pGeneral.numApicalInflors;
    numAlready := plant.numApicalActiveReproductiveMeristemsOrInflorescences;
    inflorProb := safedivExcept(numExpected - numAlready, plant.numApicalInactiveReproductiveMeristems, 0);
    end
  else
    begin
    numExpected := plant.pGeneral.numAxillaryInflors;
    numAlready := plant.numAxillaryActiveReproductiveMeristemsOrInflorescences;
    inflorProb := safedivExcept(numExpected - numAlready, plant.numAxillaryInactiveReproductiveMeristems, 0);
    end;
  {If there are only a few inflorescences on the plant, don't mess with probability; place on
  first few meristems.}
  if (numExpected <= 3) then inflorProb := 1.0;
  if (plant.randomNumberGenerator.zeroToOne < inflorProb) then
    {Check that the expected number of inflorescences hasn't been created already.}
     result := (numAlready < numExpected)
  else
    result := false;
  except
    on e: Exception do begin
    result := false;
    messageForExceptionType(e, 'PdMeristem.willCreateInflorescence');
    end;
  end;
  end;

procedure PdMeristem.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdMeristem;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure PdMeristem.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
    streamLongint(daysCreatingThisPlantPart);
    streamBoolean(isActive);
    streamBoolean(isApical);
    streamBoolean(isReproductive);
    streamSmallint(gender);
    end;
  end;

end.
