unit uleaf;

interface

uses WinProcs, WinTypes, Graphics,
  upart, uplant, umath, ufiler, utdo, utravers;

const kNumCompoundLeafRandomSwayIndexes = 49;

type 

PdLeaf = class(PdPlantPart)
  public
  sCurveParams: SCurveStructure;
  propFullSize: single;
  biomassAtCreation_pctMPB: single;
  compoundLeafRandomSwayIndexes: array[0..kNumCompoundLeafRandomSwayIndexes] of single;
  function getName: string; override;
  class function NewWithPlantFractionOfOptimalSize(aPlant: PdPlant; aFraction: single): PdLeaf;
  procedure traverseActivity(mode: integer; traverserProxy: TObject); override;
  procedure checkIfHasAbscissed;
  destructor destroy; override;
  function isPhytomer: boolean; override;
  procedure drawWithDirection(direction: single);
  function tdoToSortLinesWith: KfObject3D; override;
  procedure countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser); 
  procedure DrawLeafOrLeaflet(aScale: single);
  procedure drawStipule;
  procedure drawCompoundLeafPinnate;
  procedure drawCompoundLeafInternode(count: integer);
  procedure DrawCompoundLeafPetioletCount(scale: single; aCount: integer);
  procedure drawCompoundLeafPalmate;
  function compoundLeafAngleWithSway(angle: single; count: integer): single;
  function bendAngleForCompoundLeaf(count: integer): single;
  procedure initializeFractionOfOptimalSize(thePlant: PdPlant; aFraction: single);
  procedure nextDay; override;
  procedure report; override;
  function partType: integer; override;
  procedure wiltLeaf;
  class function optimalInitialBiomass_pctMPB(drawingPlant: PdPlant): single;
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  end;

implementation

uses SysUtils, Dialogs, Classes,
  udebug, uturtle, u3dexport, uclasses, usupport;

class function PdLeaf.NewWithPlantFractionOfOptimalSize(aPlant: PdPlant; aFraction: single): PdLeaf;
  begin
  result := create;
  result.initializeFractionOfOptimalSize(aPlant, aFraction);
  end;

procedure PdLeaf.initializeFractionOfOptimalSize(thePlant: PdPlant; aFraction: single);
  var i: integer;
  begin
  try
  initialize(thePlant);
  isSeedlingLeaf := false; {Plant sets this from outside on first phytomer.}
  liveBiomass_pctMPB := aFraction * PdLeaf.optimalInitialBiomass_pctMPB(plant);
  deadBiomass_pctMPB := 0.0;
  propFullSize := safedivExcept(liveBiomass_pctMPB, plant.pLeaf.optimalBiomass_pctMPB, 1.0);
  if plant.pLeaf.compoundNumLeaflets > 1 then
    for i := 0 to kNumCompoundLeafRandomSwayIndexes do
      compoundLeafRandomSwayIndexes[i] := plant.randomNumberGenerator.zeroToOne;
  except
    on e: Exception do messageForExceptionType(e, 'PdLeaf.initializeFractionOfOptimalSize');
  end;
  end;

class function PdLeaf.optimalInitialBiomass_pctMPB(drawingPlant: PdPlant): single;
  begin
  with drawingPlant.pLeaf do
    result := optimalFractionOfOptimalBiomassAtCreation_frn * optimalBiomass_pctMPB;
  end;

function PdLeaf.getName: string;
  begin
  result := 'leaf';
  end;

procedure PdLeaf.nextDay;
  begin
  try
    inherited nextDay;
    self.checkIfHasAbscissed;
  except
    on e: Exception do messageForExceptionType(e, 'PdLeaf.nextDay');
  end;
  end;

procedure PdLeaf.traverseActivity(mode: integer; traverserProxy: TObject);
  var
    traverser: PdTraverser;
    propFullSizeWanted, newBiomass_pctMPB, biomassToRemove_pctMPB: single;
    fractionOfMaxAge_frn: single;

    turtle: KfTurtle;
    
  begin
  inherited traverseActivity(mode, traverserProxy);
  traverser := PdTraverser(traverserProxy);
  if traverser = nil then exit;
  if self.hasFallenOff and (mode <> kActivityStream) and (mode <> kActivityFree) then exit;
  begin
  try
  case mode of
    kActivityNone: ;
    kActivityNextDay: self.nextDay;
    kActivityDemandVegetative:
      begin
      if self.age > plant.pLeaf.maxDaysToGrow then
        begin
        self.biomassDemand_pctMPB := 0.0;
        exit;
        end;
      with plant.pLeaf do
        begin
        fractionOfMaxAge_frn := safedivExcept(age + 1, maxDaysToGrow, 0.0);
        propFullSizeWanted := max(0.0, min (1.0, scurve(fractionOfMaxAge_frn, sCurveParams.c1, sCurveParams.c2)));
        self.biomassDemand_pctMPB := linearGrowthResult(self.liveBiomass_pctMPB,
            propFullSizeWanted * optimalBiomass_pctMPB, minDaysToGrow);
        end;
      traverser.total := traverser.total + self.biomassDemand_pctMPB;
      end;
    kActivityDemandReproductive:;
      { no repro. demand}
    kActivityGrowVegetative: 
      begin
      if self.age > plant.pLeaf.maxDaysToGrow then exit;
      newBiomass_pctMPB := self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB + newBiomass_pctMPB;
      self.propFullSize := Min(1.0, safedivExcept(self.totalBiomass_pctMPB, plant.pLeaf.optimalBiomass_pctMPB, 0));
      end;
    kActivityGrowReproductive: ;
	    { no repro. growth}
    kActivityStartReproduction: ;
     { no response }
    kActivityFindPlantPartAtPosition:
      begin
      if pointsAreCloseEnough(traverser.point, self.position) then
        begin
        traverser.foundPlantPart := self;
        traverser.finished := true;
        end;
      end;
    kActivityDraw: ;
      { phytomer will control drawing }
    kActivityReport: ;
    kActivityStream: ;
      {streaming will be done by internode}
    kActivityFree:
      { free will be called by phytomer };
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
      if self.isSeedlingLeaf then
        self.addToStatistics(traverser.statistics, kStatisticsPartTypeSeedlingLeaf)
      else
        self.addToStatistics(traverser.statistics, kStatisticsPartTypeLeaf);
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
      raise Exception.create('Problem: Unhandled mode in method PdLeaf.traverseActivity.');
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdLeaf.traverseActivity');
  end;
  end;
  end;

procedure PdLeaf.checkIfHasAbscissed;
  begin
  { if enough biomass removed (parameter), absciss leaf or leaves }
  // not doing anymore
  //if (self.fractionLive < plant.pLeaf.fractionOfLiveBiomassWhenAbscisses_frn) and (not self.hasFallenOff) then
  //  self.hasFallenOff := true;
  end;

destructor PdLeaf.destroy;
	begin
  inherited destroy;
  end;

function PdLeaf.isPhytomer: boolean;
  begin
  result := false;
  end;

procedure PdLeaf.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser);
  begin
  if traverser = nil then exit;
  if self.hasFallenOff then exit;
  if propFullSize <= 0 then exit;
  // seedling leaf
  if isSeedlingLeaf then
    begin
    if plant.pSeedlingLeaf.leafTdoParams.scaleAtFullSize > 0 then
      begin
      inc(traverser.total3DExportPointsIn3DObjects, plant.pSeedlingLeaf.leafTdoParams.object3d.pointsInUse);
      inc(traverser.total3DExportTrianglesIn3DObjects, plant.pSeedlingLeaf.leafTdoParams.object3d.triangles.count);
      addExportMaterial(traverser, kExportPartSeedlingLeaf, -1);
      end;
    end
  else // not seedling leaf
    begin
    if plant.pLeaf.leafTdoParams.scaleAtFullSize > 0 then
      begin
      // leaf (considering compound leaf)
      inc(traverser.total3DExportPointsIn3DObjects, plant.pLeaf.leafTdoParams.object3d.pointsInUse
          * plant.pLeaf.compoundNumLeaflets);
      inc(traverser.total3DExportTrianglesIn3DObjects, plant.pLeaf.leafTdoParams.object3d.triangles.count
          * plant.pLeaf.compoundNumLeaflets);
      addExportMaterial(traverser, kExportPartLeaf, -1);  
      end;
    // stipule
    if plant.pLeaf.stipuleTdoParams.scaleAtFullSize > 0 then
      begin
      inc(traverser.total3DExportPointsIn3DObjects, plant.pLeaf.stipuleTdoParams.object3d.pointsInUse);
      inc(traverser.total3DExportTrianglesIn3DObjects, plant.pLeaf.stipuleTdoParams.object3d.triangles.count);
      addExportMaterial(traverser, kExportPartLeafStipule, -1);
      end;
    end;
  // petiole
  if plant.pLeaf.petioleLengthAtOptimalBiomass_mm > 0 then
    begin
    inc(traverser.total3DExportStemSegments);
    if isSeedlingLeaf then
      addExportMaterial(traverser, kExportPartFirstPetiole, -1)
    else
      addExportMaterial(traverser, kExportPartPetiole, -1);
    // petiolets + compound leaf internodes
    if plant.pLeaf.compoundNumLeaflets > 1 then
      inc(traverser.total3DExportStemSegments, plant.pLeaf.compoundNumLeaflets * 2);
    end;
  end;

function PdLeaf.tdoToSortLinesWith: KfObject3D;
  begin
  result := nil;
  if plant = nil then exit;
  if isSeedlingLeaf then
    result := plant.pSeedlingLeaf.leafTdoParams.object3D
  else
    result := plant.pLeaf.leafTdoParams.object3D;
  end;

procedure PdLeaf.drawWithDirection(direction: single);
  var
    scale, length: single;
    width: single;
    angle: single;
    turtle: KfTurtle;
  begin
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  self.boundsRect := Rect(0, 0, 0, 0);
  if self.hasFallenOff then exit;
  turtle.push;
  self.determineAmendmentAndAlsoForChildrenIfAny;
  if self.hiddenByAmendment then // amendment rotations handled in drawStemSegment for petiole
    begin
    turtle.pop;
    exit;
    end;
  try
    if plant.needToRecalculateColors then self.calculateColors;
    plant.turtle.push;
    if (direction = kDirectionRight) then
      turtle.RotateX(128);
    length := plant.pLeaf.petioleLengthAtOptimalBiomass_mm * propFullSize;
    if (isSeedlingLeaf) then length := length / 2;
    width := plant.pLeaf.petioleWidthAtOptimalBiomass_mm * propFullSize;
    angle := self.angleWithSway(plant.pLeaf.petioleAngle);
    turtle.ifExporting_startNestedGroupOfPlantParts('leaf, petiole and stipule',
      'LeafPetiole', kNestingTypeLeafAndPetiole);
    if isSeedlingLeaf then
      begin
      self.drawStemSegment(length, width, angle, 0, plant.pLeaf.petioleColor, plant.pLeaf.petioleTaperIndex,
          kExportPartPetiole, kUseAmendment);
      scale := (propFullSize * (plant.pSeedlingLeaf.leafTdoParams.scaleAtFullSize / 100.0)) * 1.0;
      self.drawLeafOrLeaflet(scale);
      end
    else
      begin
      if (plant.pLeaf.stipuleTdoParams.scaleAtFullSize > 0) then
        self.drawStipule;
      if (plant.pLeaf.compoundNumLeaflets <= 1) or plant.turtle.drawOptions.simpleLeavesOnly then
        begin
        self.drawStemSegment(length, width, angle, 0, plant.pLeaf.petioleColor, plant.pLeaf.petioleTaperIndex,
            kExportPartPetiole, kUseAmendment);
        scale := self.propFullSize * plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0;
        self.drawLeafOrLeaflet(scale);
        end
      else
        begin
        self.drawStemSegment(length, width, angle, 0, plant.pLeaf.petioleColor, kDontTaper, kExportPartPetiole, kUseAmendment);
        turtle.ifExporting_startNestedGroupOfPlantParts('compound leaf', 'CompoundLeaf', kNestingTypeCompoundLeaf);
        if (plant.pLeaf.compoundPinnateOrPalmate = kCompoundLeafPinnate) then
          self.drawCompoundLeafPinnate
        else
          self.drawCompoundLeafPalmate;
        turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeCompoundLeaf);
        end;
      end;
    turtle.pop;
    turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeLeafAndPetiole);
    turtle.pop;
  except
    on e: Exception do messageForExceptionType(e, 'PdLeaf.drawWithDirection');
  end;
  end;

procedure PdLeaf.wiltLeaf;
{  var
    angle: integer; }
  begin
  if (plant.turtle = nil) then exit;
 { angle := round(abs(plant.turtle.angleX + 32) * plant.pGeneral.wiltingPercent / 100.0);
  if plant.turtle.angleX > -32 then
    angle := -angle;
  plant.turtle.rotateX(angle); }
  end;

procedure PdLeaf.drawStipule;
  var
    turtle: KfTurtle;
    scale: single;
    i, turnPortion, leftOverDegrees, addThisTime: integer;
    addition, carryOver: single; 
  begin
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  if isSeedlingLeaf then exit;
  turtle.push;
  with plant.pLeaf.stipuleTdoParams do
    begin
    turtle.rotateX(self.angleWithSway(xRotationBeforeDraw));
    turtle.rotateY(self.angleWithSway(yRotationBeforeDraw));
    turtle.rotateZ(self.angleWithSway(zRotationBeforeDraw));
    scale := (self.propFullSize * (scaleAtFullSize / 100.0)) * 1.0;
    if repetitions > 1 then
      begin
      turnPortion := 256 div repetitions;
      leftOverDegrees := 256 - turnPortion * repetitions;
      if leftOverDegrees > 0 then
        addition := leftOverDegrees / repetitions
      else
        addition := 0;
      carryOver := 0;
      for i := 1 to repetitions do
        begin
        addThisTime := trunc(addition + carryOver);
        carryOver := carryOver + addition - addThisTime;
        if carryOver < 0 then carryOver := 0;
			  turtle.RotateY(turnPortion + addThisTime);
        if object3D <> nil then
          self.draw3DObject(object3D, scale, faceColor, backfaceColor, kExportPartLeafStipule);
        end;
      end
    else
      if object3D <> nil then
        self.draw3DObject(object3D, scale, faceColor, backfaceColor, kExportPartLeafStipule);
    end;
  turtle.pop;
  end;

procedure PdLeaf.DrawLeafOrLeaflet(aScale: single);
  var
    turtle: KfTurtle;
    rotateAngle: single;
    tdo: KfObject3D;
    useFaceColor, useBackfaceColor: TColorRef;
  begin
  {Draw leaf only. If seedling leaf (on first phytomer), draw seedling leaf 3D object and colors instead.
    Wilt leaf according to water stress and age.}
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  if isSeedlingLeaf then
    begin
    turtle.setLineWidth(1.0);
    useFaceColor := plant.pSeedlingLeaf.leafTdoParams.faceColor;
    useBackfaceColor := plant.pSeedlingLeaf.leafTdoParams.backfaceColor;
    end
  else
    begin
    turtle.setLineWidth(1.0);
    useFaceColor := plant.pLeaf.leafTdoParams.faceColor;
    useBackfaceColor := plant.pLeaf.leafTdoParams.backfaceColor;
    end;
  {this aligns the 3D object as stored in the file to the way it should draw on the plant}
  // turtle.RotateX(64)  // flip over; in 3D designer you design the leaf from the underside
  //rotateAngle := self.angleWithSway(plant.pLeaf.object3DXRotationBeforeDraw * 256 / 360);
  //turtle.rotateX(rotateAngle);
  // no longer doing this because default X rotation is 90 degrees
  if isSeedlingLeaf then
    begin
    turtle.rotateX(self.angleWithSway(plant.pSeedlingLeaf.leafTdoParams.xRotationBeforeDraw));
    turtle.rotateY(self.angleWithSway(plant.pSeedlingLeaf.leafTdoParams.yRotationBeforeDraw));
    turtle.rotateZ(self.angleWithSway(plant.pSeedlingLeaf.leafTdoParams.zRotationBeforeDraw));
    end
  else
    begin
    turtle.rotateX(self.angleWithSway(plant.pLeaf.leafTdoParams.xRotationBeforeDraw));
    turtle.rotateY(self.angleWithSway(plant.pLeaf.leafTdoParams.yRotationBeforeDraw));
    turtle.rotateZ(self.angleWithSway(plant.pLeaf.leafTdoParams.zRotationBeforeDraw));
    end;
  turtle.RotateZ(-64); {pull leaf up to plane of petiole (is perpendicular)}
  self.wiltLeaf;
  if isSeedlingLeaf then tdo := plant.pSeedlingLeaf.leafTdoParams.object3D
    else tdo := plant.pLeaf.leafTdoParams.object3D;
  if tdo <> nil then
    self.draw3DObject(tdo, aScale, useFaceColor, useBackfaceColor, kExportPartLeaf);
  end;

procedure PdLeaf.drawCompoundLeafPinnate;
  var
    turtle: KfTurtle;
    scale: single;
    i: integer;
  begin
  {Draw compound leaf. Use recursion structure we used to use for whole plant, with no branching.
    Leaflets decrease in size as you move up the leaf, simulating a gradual appearance of leaflets.
    Note that seedling leaves are never compound.}
  turtle := plant.turtle;
  if turtle = nil then exit;
  if plant.pLeaf.compoundNumLeaflets <= 0 then exit;
  for i := plant.pLeaf.compoundNumLeaflets downto 1 do
    begin
    // v2 added opposite leaflets
    if (plant.pLeaf.compoundPinnateLeafletArrangement = kArrangementOpposite) then
      begin
      if (i <> 1) and (i mod 2 = 1) then
        drawCompoundLeafInternode(i);
      end
    else
      if (i <> 1) then drawCompoundLeafInternode(i);
    turtle.push;
    scale := self.propFullSize * plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0;
    DrawCompoundLeafPetioletCount(scale, i);
    DrawLeafOrLeaflet(scale);
    turtle.pop;
    end;
  end;

procedure PdLeaf.drawCompoundLeafInternode(count: integer);
  var
    length, width, angleZ, angleY: single;
  begin
  {Draw internode of leaflet (portion of rachis). This is almost identical to drawing the petiole, etc,
   but a bit of random drift is included to make the compound leaf look more single.}
  length := plant.pLeaf.petioleLengthAtOptimalBiomass_mm * propFullSize
      * plant.pLeaf.compoundRachisToPetioleRatio / 100.0;
  width := plant.pLeaf.petioleWidthAtOptimalBiomass_mm * propFullSize;
  // v1.6b3
  angleZ := self.compoundLeafAngleWithSway(self.bendAngleForCompoundLeaf(count), count);
  angleY := self.compoundLeafAngleWithSway(0, count);
  self.drawStemSegment(length, width, angleZ, angleY, plant.pLeaf.petioleColor, kDontTaper,
    kExportPartPetiole, kDontUseAmendment);
  end;

  // v1.6b3
function PdLeaf.bendAngleForCompoundLeaf(count: integer): single;
  var
    leafletNumberEffect, propFullSizeThisLeaflet, difference: single;
  begin
  result := 0;
  if plant = nil then exit;
  with plant.pLeaf do
    begin
    difference := abs(compoundCurveAngleAtFullSize - compoundCurveAngleAtStart);
    leafletNumberEffect := 0.75 + 0.25 * safedivExcept(count, compoundNumLeaflets - 1, 0);
    propFullSizeThisLeaflet := max(0.0, min(1.0, (0.25 + 0.75 * propFullSize) * leafletNumberEffect));
    if compoundCurveAngleAtFullSize > compoundCurveAngleAtStart then
      result := compoundCurveAngleAtStart + difference * propFullSizeThisLeaflet
    else
      result := compoundCurveAngleAtStart - difference * propFullSizeThisLeaflet;
    end;
  end;

procedure PdLeaf.DrawCompoundLeafPetioletCount(scale: single; aCount: integer);
  var
    length, width, angle: single;
  begin
  {Draw petiolet, which is the leaflet stem coming off the compound leaf rachis.}
  length := scale * plant.pLeaf.petioleLengthAtOptimalBiomass_mm * propFullSize;
  width := scale * plant.pLeaf.petioleWidthAtOptimalBiomass_mm * propFullSize;
  if (aCount = 1) then
    angle := 0
  else
    begin
    if (odd(aCount)) then
      angle := 32
    else
      angle := -32;
    end;
  angle := self.compoundLeafAngleWithSway(angle, aCount);
  self.drawStemSegment(length, width, 0, angle, plant.pLeaf.petioleColor, plant.pLeaf.petioleTaperIndex,
      kExportPartPetiole, kDontUseAmendment);
  end;

function PdLeaf.compoundLeafAngleWithSway(angle: single; count: integer): single;
  var randomNumber: single;
  begin
  result := angle;
  if plant = nil then exit;
  if count < 0 then count := 0;
  count := count mod kNumCompoundLeafRandomSwayIndexes;
  randomNumber := compoundLeafRandomSwayIndexes[count];
  result := angle + ((randomNumber - 0.5) * plant.pGeneral.randomSway);
  end;

procedure PdLeaf.drawCompoundLeafPalmate;
  var
    turtle: KfTurtle;
    scale: single;
    angle: single;
    angleOne: single;
    length: single;
    width: single;
  var i: integer;
  begin
  {Draw palmate compound leaf. Use recursion structure we used to use for whole plant, with no branching.
    In a palmate leaf, leaflets increase in size as you move toward the middle of the leaf.
    Note that seedling leaves are never compound.}
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  angleOne := safedivExcept(64, plant.pLeaf.compoundNumLeaflets, 0);
  if plant.pLeaf.compoundNumLeaflets > 0 then
    for i := plant.pLeaf.compoundNumLeaflets downto 1 do
	    begin
		  turtle.push;
      if (i = 1) then
        angle := 0
      else if (odd(i)) then
        angle := angleOne * i * -1
      else
        angle := angleOne * i * 1;
      length := plant.pLeaf.petioleLengthAtOptimalBiomass_mm * propFullSize
          * plant.pLeaf.compoundRachisToPetioleRatio / 100.0;
      width := plant.pLeaf.petioleWidthAtOptimalBiomass_mm * propFullSize;
      self.drawStemSegment(length, width, 0, angle, plant.pLeaf.petioleColor, plant.pLeaf.petioleTaperIndex,
          kExportPartPetiole, kDontUseAmendment);
      scale := self.propFullSize * plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0;
      {scale := safedivExcept(scale, plant.pLeaf.compoundNumLeaflets, 0); }
      DrawLeafOrLeaflet(scale);
      turtle.pop;
      end;
  end;

procedure PdLeaf.report;
  begin
  inherited report;
  //debugPrint('leaf, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
  {DebugForm.printNested(plant.turtle.stackSize, 'leaf, age ' + IntToStr(age));}
  end;

function PdLeaf.partType: integer;
  begin
  result := kPartTypeLeaf;
  end;

procedure PdLeaf.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdLeaf;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure PdLeaf.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
  	streamBytes(sCurveParams, sizeof(sCurveParams));
  	streamSingle(propFullSize);
  	streamSingle(biomassAtCreation_pctMPB);
  	streamBoolean(isSeedlingLeaf);
    end;
  end;

end.

