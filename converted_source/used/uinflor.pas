unit uinflor;

interface

uses WinProcs, WinTypes, Classes,
  upart, uintern, uplant, ufruit, ucollect, ufiler, utravers;

type

PdInflorescence = class(PdPlantPart)
  public
  flowers: TListCollection; 
  numFlowers, numFlowersEachDay, daysBetweenFlowerAppearances,
    daysSinceLastFlowerAppeared, daysSinceStartedMakingFlowers: smallint;
  isApical: boolean;
  meristemThatCreatedMe: PdPlantPart;
  phytomerAttachedTo: PdInternode;
  fractionOfOptimalSizeWhenCreated: single;
  constructor create; override;
  function getName: string; override;
	function allFlowersHaveBeenDrawn: boolean;
	procedure createFlower;
	procedure deleteFlower(theFlower: PdFlowerFruit);
	procedure draw; override;
  function shouldDraw: boolean;
	procedure drawApex(internodeCount, flowerIndexOffset: integer; mainBranch: boolean);
	procedure drawAxillaryBud(internodeCount, flowerIndexOffset: integer);
	procedure drawFlower(internodeCount: integer);
	procedure drawHead;
	procedure drawInternode(internodeCount: integer);
	procedure drawPeduncle;
  procedure drawBracts;
  function biomassOfMeAndAllPartsConnectedToMe_pctMPB: single;
  function lengthOrWidthAtAgeForFraction(starting, fraction: single): single;
	procedure initializeGenderApicalOrAxillary(aPlant: PdPlant; aGender: integer; initAsApical: boolean;
    fractionOfOptimalSize: single);
	procedure nextDay;  override;
	function partType: integer; override;
  procedure report; override;
  function flower(index: integer): PdFlowerFruit;
  destructor destroy; override;
  procedure traverseActivity(mode: integer; traverserProxy: TObject); override;
  class function optimalInitialBiomass_pctMPB(drawingPlant: PdPlant; gender: integer): single;
  procedure addDependentPartsToList(aList: TList); override;
  procedure countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser);
  procedure determineAmendmentAndAlsoForChildrenIfAny; override;
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  end;

implementation

uses SysUtils, Dialogs,
  udebug, uturtle, u3dexport, udomain, umath, uclasses, uamendmt, usupport;

constructor PdInflorescence.create;
  begin
  inherited create;
  flowers := TListCollection.create;
  meristemThatCreatedMe := nil;
  end;

destructor PdInflorescence.destroy;
	begin
  flowers.free;
  flowers := nil;
  meristemThatCreatedMe.free;
  meristemThatCreatedMe := nil;
  inherited destroy;
  end;

function PdInflorescence.getName: string;
  begin
  result := 'inflorescence';
  end;

procedure PdInflorescence.determineAmendmentAndAlsoForChildrenIfAny;
  var                               
    i: integer;
    amendmentToPass: PdPlantDrawingAmendment;
  begin
  inherited determineAmendmentAndAlsoForChildrenIfAny;
  if amendment <> nil then
    amendmentToPass := amendment
  else
    amendmentToPass := parentAmendment;
  if flowers.count > 0 then
    for i := 0 to flowers.count - 1 do
      PdFlowerFruit(flowers.items[i]).parentAmendment := amendmentToPass;
  end;

procedure PdInflorescence.InitializeGenderApicalOrAxillary(aPlant: PdPlant; aGender: integer;
	  initAsApical: boolean; fractionOfOptimalSize: single);
  var
    daysToAllFlowers: single;
  begin
  try
  Initialize(aPlant);
  gender := aGender;
  isApical := initAsApical;
  daysSinceLastFlowerAppeared := 0;
  daysSinceStartedMakingFlowers := 0;
  self.fractionOfOptimalSizeWhenCreated := min(1.0, fractionOfOptimalSize);
  {The inflorescence must know whether it produces flowers slowly (over a greater number of days than flowers)
  or produces many flowers in a few days.}
  daysToAllFlowers := plant.pInflor[gender].daysToAllFlowersCreated;
  with plant.pInflor[gender] do
    numFlowers := numFlowersOnMainBranch + numFlowersPerBranch * numBranches;
  daysBetweenFlowerAppearances := 0;
  numFlowersEachDay := 0;
  if numFlowers > 0 then
    begin
    if numFlowers = 1 then
      numFlowersEachDay := 1
    else if numFlowers = daysToAllFlowers then
      numFlowersEachDay := 1
    else if numFlowers > daysToAllFlowers then
      numFlowersEachDay := round(safedivExcept(1.0 * numFlowers, 1.0 * daysToAllFlowers, 0))
    else
      daysBetweenFlowerAppearances := round(safedivExcept(1.0 * daysToAllFlowers, 1.0 * numFlowers, 0))
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdInflorescence.InitializeGenderApicalOrAxillary');
  end;
  end;

class function PdInflorescence.optimalInitialBiomass_pctMPB(drawingPlant: PdPlant; gender: integer): single;
  begin
  if (gender < 0) or (gender > 1) then
    result := 0.0
  else
    with drawingPlant.pInflor[gender] do
      result := optimalBiomass_pctMPB * minFractionOfOptimalBiomassToCreateInflorescence_frn;
  end;

procedure PdInflorescence.nextDay;
  var
    i, numFlowersToCreateToday: integer;
    biomassToMakeFlowers_pctMPB: single;
  begin
  try
  inherited nextDay;
  if flowers.count > 0 then for i := 0 to flowers.count - 1 do PdFlowerFruit(flowers.items[i]).nextDay;
  //if self.age < plant.pInflor[gender].maxDaysToGrow then
  biomassToMakeFlowers_pctMPB := plant.pInflor[gender].minFractionOfOptimalBiomassToMakeFlowers_frn
      * plant.pInflor[gender].optimalBiomass_pctMPB;
  if self.liveBiomass_pctMPB >= biomassToMakeFlowers_pctMPB then
    begin
    inc(daysSinceStartedMakingFlowers);
    if (flowers.count <= 0) and (numFlowers > 0) then
      createFlower // make first flower on first day
    else if (flowers.count < numFlowers) then
      begin
      if (daysBetweenFlowerAppearances > 0) then
        begin
        if (daysSinceLastFlowerAppeared >= daysBetweenFlowerAppearances) then
          begin
          createFlower;
          daysSinceLastFlowerAppeared := 0;
          end
        else
          inc(daysSinceLastFlowerAppeared);
        end
      else
        begin
        numFlowersToCreateToday := intMin(numFlowersEachDay, numFlowers - flowers.count);
        if numFlowersToCreateToday > 0 then
          for i := 0 to numFlowersToCreateToday - 1 do
            createFlower;
        daysSinceLastFlowerAppeared := 0;
        end;
      end;
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdInflorescence.nextDay');
  end;
  end;

procedure PdInflorescence.traverseActivity(mode: integer; traverserProxy: TObject);
  var
    traverser: PdTraverser;
    newBiomass_pctMPB, biomassToRemove_pctMPB: single;
    i, numLines: integer;
  begin
  inherited traverseActivity(mode, traverserProxy);
  traverser := PdTraverser(traverserProxy);
  if traverser = nil then exit;
  if self.hasFallenOff and (mode <> kActivityStream) and (mode <> kActivityFree) then exit;
  try
  if (mode <> kActivityDraw) then
    if flowers.count > 0 then
      for i := 0 to flowers.count - 1 do
        (PdFlowerFruit(flowers.items[i])).traverseActivity(mode, traverser);
  case mode of
    kActivityNone: ;
    kActivityNextDay: self.nextDay;
    kActivityDemandVegetative: { no vegetative demand };
    kActivityDemandReproductive:
      begin
      if (self.age > plant.pInflor[gender].maxDaysToGrow) then
        begin
        self.biomassDemand_pctMPB := 0.0;
        exit;
        end;
      try
      self.biomassDemand_pctMPB := linearGrowthResult(self.liveBiomass_pctMPB,
        plant.pInflor[gender].optimalBiomass_pctMPB, plant.pInflor[gender].minDaysToGrow);
      traverser.total := traverser.total + self.biomassDemand_pctMPB;
      except
        on e: Exception do messageForExceptionType(e, 'PdInflorescence.traverseActivity (reproductive demand)');
      end
      end;
    kActivityGrowVegetative: { no vegetative growth };
    kActivityGrowReproductive: 
      begin
      if self.age > plant.pInflor[gender].maxDaysToGrow then exit;
      newBiomass_pctMPB := self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB + newBiomass_pctMPB;
      end;
    kActivityStartReproduction: { cannot switch };
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
    kActivityStream: {streaming called by phytomer};
    kActivityFree: { free called by phytomer };
    kActivityVegetativeBiomassThatCanBeRemoved: { none };
    kActivityRemoveVegetativeBiomass: { none };
    kActivityReproductiveBiomassThatCanBeRemoved:
      begin
      traverser.total := traverser.total + self.liveBiomass_pctMPB;
      end;
    kActivityRemoveReproductiveBiomass:
      begin
      biomassToRemove_pctMPB := self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB - biomassToRemove_pctMPB;
      self.deadBiomass_pctMPB := self.deadBiomass_pctMPB + biomassToRemove_pctMPB;
      end;
    kActivityGatherStatistics:
      begin
      if gender = kGenderMale then
        self.addToStatistics(traverser.statistics, kStatisticsPartTypeMaleInflorescence)
      else
        self.addToStatistics(traverser.statistics, kStatisticsPartTypeFemaleInflorescence);
      self.addToStatistics(traverser.statistics, kStatisticsPartTypeAllReproductive);
      end;
    kActivityCountPlantParts: ;
    kActivityFindPartForPartID: ;
    kActivityCountTotalMemoryUse: inc(traverser.totalMemorySize, self.instanceSize);
    kActivityCalculateBiomassForGravity:
      self.biomassOfMeAndAllPartsAboveMe_pctMPB := self.biomassOfMeAndAllPartsConnectedToMe_pctMPB;
    kActivityCountPointsAndTrianglesFor3DExport:
      begin
      self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser);
      end;
    else
      raise Exception.create('Problem: Unhandled mode in method PdInflorescence.traverseActivity.');
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdInflorescence.traverseActivity');
  end;
  end;

procedure PdInflorescence.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser);
  var numLines: integer;
  begin
  if traverser = nil then exit;
  // bracts
  with plant.pInflor[gender].bractTdoParams do if scaleAtFullSize > 0 then
    begin
    inc(traverser.total3DExportPointsIn3DObjects, object3d.pointsInUse * repetitions);
    inc(traverser.total3DExportTrianglesIn3DObjects, object3d.triangles.count * repetitions);
    addExportMaterial(traverser, kExportPartInflorescenceBractFemale, kExportPartInflorescenceBractMale);
    end;
  // pedicels and inflorescence internodes
  numLines := plant.pInflor[gender].numBranches;
  if not plant.pInflor[gender].branchesAreAlternate then
    numLines := numLines * 2;
  if plant.pInflor[gender].internodeLength_mm > 0 then
    addExportMaterial(traverser, kExportPartInflorescenceInternodeFemale, kExportPartInflorescenceInternodeMale);
  // peduncle
  inc(numLines);
  inc(traverser.total3DExportStemSegments, numLines);
  if plant.pInflor[gender].peduncleLength_mm > 0 then
    addExportMaterial(traverser, kExportPartInflorescenceStalkFemale, kExportPartInflorescenceStalkMale);
  end;

procedure PdInflorescence.report;
  begin
  inherited report;
  debugPrint(intToStr(numFlowers) + ' flowers');
  { note flowers will print first }
  // debugPrint('inflorescence, age '  + IntToStr(age));
  {DebugForm.printNested(plant.turtle.stackSize, 'inflorescence, age '  + IntToStr(age));}
  end;

function PdInflorescence.biomassOfMeAndAllPartsConnectedToMe_pctMPB: single;
  var i: integer;
  begin
  result := self.totalBiomass_pctMPB;
  if flowers.count > 0 then
    for i := 0 to flowers.count - 1 do
      result := result + (PdFlowerFruit(flowers.items[i])).totalBiomass_pctMPB;
  end;

function PdInflorescence.allFlowersHaveBeenDrawn: boolean;
  var i: integer;
  begin
  result := true;
  if flowers.count > 0 then
    for i := 0 to flowers.count - 1 do
      if not ((PdFlowerFruit(flowers.items[i])).hasBeenDrawn) then
        begin
        result := false;
        exit;
        end;
  end;

procedure PdInflorescence.addDependentPartsToList(aList: TList);
  var i: longint;
  begin
  if flowers.count > 0 then
    for i := 0 to flowers.count - 1 do
      aList.add(flowers.items[i]);
  end;

procedure PdInflorescence.createFlower;
	var
	  aFlowerFruit: PdFlowerFruit;
  begin
  { create new flower/fruit object }
  if plant.partsCreated > domain.options.maxPartsPerPlant_thousands * 1000 then exit;  // v1.6b1
  aFlowerFruit := PdFlowerFruit.create;
  aFlowerFruit.InitializeGender(plant, gender);
  flowers.Add(aFlowerFruit);
  end;

procedure PdInflorescence.deleteFlower(theFlower: PdFlowerFruit);
  begin
  { remove flower object from list }
  flowers.Remove(theFlower);
  end;

procedure PdInflorescence.draw;
  var
    i: integer;
    turtle: KfTurtle;
  begin
  if not self.shouldDraw then exit;
  turtle := plant.turtle;
  self.boundsRect := Rect(0, 0, 0, 0);
  turtle.push;
  if self.hiddenByAmendment then // amendment rotation handled in drawStemSegment for peduncle
    begin
    turtle.pop;
    exit;
    end;
  try
    if flowers.count > 0 then
      for i := 0 to flowers.count - 1 do
    	  PdFlowerFruit(flowers.items[i]).HasBeenDrawn := false;
    self.calculateColors;
    turtle.ifExporting_startNestedGroupOfPlantParts(genderString + ' inflorescence',
      genderString + 'Inflor', kNestingTypeInflorescence);
    if (flowers.count > 0) then
      begin
      self.drawBracts;
      self.drawPeduncle;
      if (plant.pInflor[gender].isHead) then
        self.drawHead
      else
        self.DrawApex(plant.pInflor[gender].numFlowersOnMainBranch, 0, true);
      end;
    turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeInflorescence);
    turtle.pop;
  except
    on e: Exception do messageForExceptionType(e, 'PdInflorescence.draw');
  end;
  end;

function PdInflorescence.shouldDraw: boolean;
  var
    i: longint;
    flowerFruit: PdFlowerFruit;
  begin
  { if inflorescence has at least one flower or non-fallen fruit, should draw }
  result := true;
  if flowers.count > 0 then
    for i := 0 to flowers.count - 1 do
      begin
      flowerFruit := PdFlowerFruit(flowers.items[i]);
      if flowerFruit = nil then continue;
      if not flowerFruit.hasFallenOff then
        exit;
      end;
  result := false;
  end;

procedure PdInflorescence.DrawApex(internodeCount, flowerIndexOffset: integer; mainBranch: boolean);
  var
    turtle: KfTurtle;
    var i, branchesDrawn: smallint;
  begin
  i := 0;
  {Draw inflorescence in raceme, panicle, or umbel form. This method uses the recursive algorithm
     we first developed to draw the entire plant.}
  turtle := plant.turtle;
  if turtle = nil then exit;
  branchesDrawn := 0;
  // draw the flowers on the main stem first, because if any are not going to be drawn for
  // want of available flowers, the branches should lose them.
  if internodeCount > 0 then
    begin
    if mainBranch then turtle.push;
    if mainBranch then
      while branchesDrawn < plant.pInflor[gender].numBranches do
        begin
        DrawInternode(i);
        inc(branchesDrawn);
        end;
    // draw flowers on main stem first
    i := internodeCount;
    while i >= 1 do
      begin
      if plant.pInflor[gender].flowersSpiralOnStem then turtle.RotateX(98); {param}
      DrawInternode(i);
      turtle.push;
      DrawFlower(flowerIndexOffset + i);
      turtle.pop;
      dec(i);
      end;
    if mainBranch then turtle.pop;
    end;
  branchesDrawn := 0;
  // draw branches
  if mainBranch then
    while branchesDrawn < plant.pInflor[gender].numBranches do
      begin
      if plant.pInflor[gender].flowersSpiralOnStem then turtle.RotateX(98); {param}
      DrawInternode(i);
      DrawAxillaryBud(
        plant.pInflor[gender].numFlowersPerBranch,
        plant.pInflor[gender].numFlowersOnMainBranch + branchesDrawn * plant.pInflor[gender].numFlowersPerBranch);
      inc(branchesDrawn);
      if (not plant.pInflor[gender].branchesAreAlternate)
          and (branchesDrawn < plant.pInflor[gender].numBranches) then
        begin
        turtle.push;
        turtle.rotateX(128);
        DrawAxillaryBud(
          plant.pInflor[gender].numFlowersPerBranch,
          plant.pInflor[gender].numFlowersOnMainBranch + branchesDrawn * plant.pInflor[gender].numFlowersPerBranch);
        inc(branchesDrawn);
        turtle.pop;
        end;
      end;
  end;

procedure PdInflorescence.drawBracts;
  var
    scale, length, width, angle, propFullSize: single;
    turtle: KfTurtle;
    i: smallint;
    turnPortion, leftOverDegrees, addThisTime: integer;
    addition, carryOver: single; 
  begin
  if (plant.turtle = nil) then exit;
  if plant.pInflor[gender].bractTdoParams.scaleAtFullSize <= 0 then exit;
  turtle := plant.turtle;
  turtle.push;
  turtle.ifExporting_startNestedGroupOfPlantParts(
      self.longNameForDXFPartConsideringGenderEtc(kExportPartInflorescenceBractFemale),
      self.shortNameForDXFPartConsideringGenderEtc(kExportPartInflorescenceBractFemale),
      kNestingTypeInflorescence);
  with plant.pInflor[gender].bractTdoParams do
    begin
    propFullSize := safedivExcept(self.liveBiomass_pctMPB, plant.pInflor[gender].optimalBiomass_pctMPB, 0);
    scale := ((scaleAtFullSize / 100.0) * propFullSize);
    turtle.rotateX(self.angleWithSway(xRotationBeforeDraw));
    turtle.rotateY(self.angleWithSway(yRotationBeforeDraw));
    turtle.rotateZ(self.angleWithSway(zRotationBeforeDraw));
    if (radiallyArranged) and (repetitions > 0) then
      begin
      turnPortion := 256 div repetitions;
      leftOverDegrees := 256 - turnPortion * repetitions;
      if leftOverDegrees > 0 then
        addition := safedivExcept(leftOverDegrees, repetitions, 0)
      else
        addition := 0;
      carryOver := 0;
      for i := 0 to repetitions - 1 do
        begin
        turtle.push;
        turtle.RotateY(-64); {aligns object as stored in the file to way should draw on plant}
        turtle.rotateX(64); // why? i don't know.
        turtle.rotateX(pullBackAngle);
        self.draw3DObject(object3D, scale, faceColor, backfaceColor, kExportPartInflorescenceBractFemale);
        turtle.pop;
        addThisTime := trunc(addition + carryOver);
        carryOver := carryOver + addition - addThisTime;
        if carryOver < 0 then carryOver := 0;
        turtle.rotateX(turnPortion + addThisTime);
        end;
      end
    else
      begin
      turtle.push;
      turtle.RotateY(-64); {aligns object as stored in the file to way should draw on plant}
      turtle.rotateX(64); // why? i don't know.
      turtle.rotateX(pullBackAngle);
      self.draw3DObject(object3D, scale, faceColor, backfaceColor, kExportPartInflorescenceBractFemale);
      turtle.pop;
      end;
    end;
  turtle.pop;
  turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeInflorescence);
  end;

procedure PdInflorescence.drawPeduncle;
  var
    length, width, zAngle, propFullSize: single;
  begin
  try
  {Draw peduncle, which is the primary inflorescence stalk. If the inflorescence has only one flower,
     this is the only part drawn. If the inflorescence is apical, the stalk may be longer (e.g. in bolting
     plants) and is specified by a different parameter.}
  with plant.pInflor[gender] do
    begin
    zAngle := 0;
    if (self.phytomerAttachedTo <> nil) then
      begin
      if (self.phytomerAttachedTo.leftBranchPlantPart = self) then
        zAngle := peduncleAngleFromVegetativeStem
      else if (self.phytomerAttachedTo.rightBranchPlantPart = self) then
        begin
        zAngle := peduncleAngleFromVegetativeStem;
        plant.turtle.RotateX(128);
        end
      else if isApical then zAngle := apicalStalkAngleFromVegetativeStem;
      end;
    propFullSize := safedivExcept(self.liveBiomass_pctMPB, plant.pInflor[gender].optimalBiomass_pctMPB, 0);
    if isApical then
      length := lengthOrWidthAtAgeForFraction(terminalStalkLength_mm, propFullSize)
    else
      length := lengthOrWidthAtAgeForFraction(peduncleLength_mm, propFullSize);
    width := lengthOrWidthAtAgeForFraction(internodeWidth_mm, propFullSize);
    {Use no angle here because phytomer makes the rotation before the inflorescence is drawn.}
    self.drawStemSegment(length, width, zAngle, 0, stalkColor, kDontTaper,
        kExportPartInflorescenceStalkFemale, kUseAmendment);
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdInflorescence.drawPeduncle');
  end;
  end;

procedure PdInflorescence.DrawAxillaryBud(internodeCount, flowerIndexOffset: integer);
  var
    turtle: KfTurtle;
    angle: single;
  begin
  {This message is sent when the inflorescence is branched. The decision to create a branch is
     made before the message is sent. Note the check if all flowers have been drawn; this prevents
     scrawly lines with no flowers.}
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  if (allFlowersHaveBeenDrawn) then exit;
  angle := self.angleWithSway(plant.pInflor[gender].branchAngle);
  turtle.push;
  turtle.RotateZ(angle);
  DrawApex(internodeCount, flowerIndexOffset, false);
  turtle.pop;
  end;

procedure PdInflorescence.DrawFlower(internodeCount: integer);
  var
    length, width, angle, propFullSize: single;
    flowerIndex: integer;
  begin
  try
  {Draw one flower, remembering that internodeCount goes from flowers size down to 1,
  but flowers are in the order formed.
  If the oldest flowers on the inflorescence are at the bottom (acropetal),
  draw the flowers in reverse order from internodeCount (which is in the order they were formed).
  If the oldest flowers on the inflorescence are at the top (basipetal),
  draw the flowers in the order presented by internodeCount
     which is in reverse order to how they were formed).
  In most plants the older flowers are lower.}
  if (allFlowersHaveBeenDrawn) then exit;
  propFullSize := safedivExcept(self.liveBiomass_pctMPB, plant.pInflor[gender].optimalBiomass_pctMPB, 0);
  with plant.pInflor[gender] do
    begin
    length := lengthOrWidthAtAgeForFraction(pedicelLength_mm, propFullSize);
    width := lengthOrWidthAtAgeForFraction(internodeWidth_mm, propFullSize);
    angle := self.angleWithSway(pedicelAngle);
    if (plant.pInflor[gender].flowersDrawTopToBottom) then
      flowerIndex := internodeCount
    else
      flowerIndex := flowers.count - internodeCount + 1;
    plant.turtle.ifExporting_startNestedGroupOfPlantParts(
        genderString + ' pedicel and flower/fruit',
        genderString + 'PedicelFlower', kNestingTypePedicelAndFlowerFruit);
    self.drawStemSegment(length, width, angle, 0, pedicelColor, pedicelTaperIndex,
      kExportPartPedicelFemale, kDontUseAmendment);
    end;
  if (flowerIndex - 1 >= 0) and (flowerIndex - 1 <= flowers.count - 1) then
    PdFlowerFruit(flowers.items[flowerIndex-1]).draw;
  plant.turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypePedicelAndFlowerFruit);
  except
    on e: Exception do messageForExceptionType(e, 'PdInflorescence.drawFlower');
  end;
  end;

procedure PdInflorescence.drawHead;
  var
    turtle: KfTurtle;
    i: integer;
    turnPortion, leftOverDegrees, addThisTime: integer; // v1.4
    addition, carryOver: single; // v1.4
  begin
  {Draw the inflorescences in a radial pattern; this is for a head such as a sunflower.}
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  turtle.RotateY(64);
  turtle.RotateZ(64);
  { give a little angle down to make it look more natural }
  turtle.RotateY(32);
  if flowers.count > 0 then
    begin
    // new v1.4
    turnPortion := 256 div flowers.count;
    leftOverDegrees := 256 - turnPortion * flowers.count;
    if leftOverDegrees > 0 then
      addition := safedivExcept(leftOverDegrees, flowers.count, 0)
    else
      addition := 0;
    carryOver := 0;   
    for i := flowers.count - 1 downto 0 do
    	begin
      addThisTime := trunc(addition + carryOver);
      carryOver := carryOver + addition - addThisTime;
      if carryOver < 0 then carryOver := 0;
			turtle.RotateZ(turnPortion + addThisTime);   // was 256 / flowers.count
    	turtle.push;
    	self.drawFlower(i+1);  // v1.4 added one, was bug, was not drawing first flower
    	turtle.pop;
   	 end;
    end;
  end;

procedure PdInflorescence.DrawInternode(internodeCount: integer);
  var
    length, width, zAngle, yAngle, propFullSize: single;
  begin
  try
  {Draw the inflorescence internode, which is the portion of inflorescence stem between where successive
  flower pedicels come off. Note that this is not drawn if all flowers have been drawn; this prevents
  straggly lines in branched inflorescences.}
  if (allFlowersHaveBeenDrawn) then exit;
  with plant.pInflor[gender] do
    begin
    if (internodeLength_mm = 0.0) then exit;
    propFullSize := safedivExcept(self.liveBiomass_pctMPB, plant.pInflor[gender].optimalBiomass_pctMPB, 0);
    length := lengthOrWidthAtAgeForFraction(internodeLength_mm, propFullSize);
    width :=  lengthOrWidthAtAgeForFraction(internodeWidth_mm, propFullSize);
    zAngle := self.angleWithSway(angleBetweenInternodes);
    yAngle := self.angleWithSway(0);
    self.drawStemSegment(length, width, zAngle, yAngle, stalkColor, kDontTaper,
        kExportPartInflorescenceInternodeFemale, kDontUseAmendment);
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdInflorescence.drawInternode');
  end;
  end;

function PdInflorescence.lengthOrWidthAtAgeForFraction(starting, fraction: single): single;
  var ageBounded: single;
  begin
  result := 0.0;
  try
  with plant.pInflor[gender] do
    begin
    ageBounded := min(daysToAllFlowersCreated, daysSinceStartedMakingFlowers);
    if daysToAllFlowersCreated <> 0 then
      result := safedivExcept(starting * ageBounded, daysToAllFlowersCreated, 0) * fraction
    else
      result := starting * ageBounded * fraction;
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdInflorescence.lengthOrWidthAtAgeForFraction');
  end;
  end;

function PdInflorescence.flower(index: integer): PdFlowerFruit;
	begin
  result := flowers.items[index];
  end;

function PdInflorescence.partType: integer;
  begin
  result := kPartTypeInflorescence;
  end;

procedure PdInflorescence.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdInflorescence;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure PdInflorescence.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  var
   i: longint;
  begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
    streamSmallint(daysSinceStartedMakingFlowers);
    streamSmallint(numFlowersEachDay);
    streamSmallint(numFlowers);
    streamSmallint(daysBetweenFlowerAppearances);
    streamSmallint(daysSinceLastFlowerAppeared);
    streamBoolean(isApical);
    streamSingle(fractionOfOptimalSizeWhenCreated);
    if isReading then
      meristemThatCreatedMe := nil;
    flowers.streamUsingFiler(filer, PdFlowerFruit);
    { fix up plant in flowers if needed }
    if isReading and (flowers.count > 0) then
      for i := 0 to flowers.count - 1 do
        (PdFlowerFruit(flowers.items[i])).plant := self.plant;
    end;
  end;

end.

  {The inflorescence is very simple; it creates a specified number of flowers over a specified period
  of days. Each inflorescence on the plant has the same number of flowers. Since an inflorescence is
  created by a meristem which accumulates biomass, nothing stands in the way of the inflorescence
  producing the flowers according to schedule.
  This method must act differently for inflorescences that produce flowers slowly (over a greater
  number of days than flowers) than for those that produce many flowers in a few days.
  The inflorescence can create no flowers until it reaches a specified fraction of its optimal biomass.}

  {Survey flowers and return true if all flowers have been drawn (they know), false if any have not been
   drawn. This is mostly so a branched inflorescence can know if there are any flowers left to place
   on its branched structure.}

 
