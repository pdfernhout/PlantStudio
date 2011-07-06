unit ufruit;

interface

uses WinProcs, WinTypes,
  upart, umath, uplant, utdo, ufiler, utravers;

  //  kBud = 0; kPistil = 1; kStamens = 2; kFirstPetals = 3; kSecondPetals = 4; kThirdPetals = 5; kSepals = 6;

type

PdFlowerFruit = class(PdPlantPart)
  public
  propFullSize: single;
  stage: smallint;
  hasBeenDrawn: boolean;
  daysAccumulatingFruitBiomass, daysOpen: longint;
  function getName: string; override;
	procedure draw; override;
  procedure report; override;
  procedure drawFlower(drawAsOpening: boolean);
  procedure drawPistilsAndStamens(drawAsOpening: boolean);
  procedure drawCircleOfTdos(tdo: KfObject3D; faceColor, backfaceColor: TColorRef; pullBackAngle: single;
    scale: single; numParts: integer; partsArranged: boolean; open: boolean; dxfIndex: smallint);
  function dxfIndexForFloralLayerType(aType: smallint; line: boolean): smallint;
  procedure countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser);
  procedure addFloralPartsCountsToTraverser(traverser: PdTraverser);
  function triangleCountInFloralParts: integer;
  function tdoToSortLinesWith: KfObject3D; override;
	procedure initializeGender(aPlant: PdPlant; aGender: integer);
	procedure nextDay; override;
	function partType: integer; override;
  procedure traverseActivity(mode: integer; traverserProxy: TObject); override;
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  end;

implementation

uses SysUtils, Dialogs, Classes,
  udebug, usupport, uturtle, u3dexport, uclasses;

const
  kDrawFlowerAsOpening = true; kDontDrawFlowerAsOpening = false;
  kLine = true; kNotLine = false;

procedure PdFlowerFruit.InitializeGender(aPlant: PdPlant; aGender: integer);
  begin
  self.initialize(aPlant);
  gender := aGender;
  propFullSize := 0.0;
  liveBiomass_pctMPB := 0.0;
  deadBiomass_pctMPB := 0.0;
  biomassDemand_pctMPB := 0.0;
  stage := kStageFlowerBud;
  hasBeenDrawn := false;
  end;

function PdFlowerFruit.getName: string;
  begin
  result := 'flower/fruit';
  end;

procedure PdFlowerFruit.nextDay;
  var
    anthesisLoss_pctMPB, biomassToMakeFruit_pctMPB: single;
    minDaysWithOptimalBiomass, maxDaysWithMinFraction: boolean;
  begin
  if self.hasFallenOff then exit;
  try
  inherited nextDay;
  case self.stage of
    kStageFlowerBud: {if over required fraction of optimal or over max days to grow, open bud}
      begin
      with plant.pFlower[gender] do
        if ((liveBiomass_pctMPB >= minFractionOfOptimalBiomassToOpenFlower_frn * optimalBiomass_pctMPB)
           or (age > maxDaysToGrowIfOverMinFraction)) and (age > minDaysToOpenFlower) then
           begin
           stage := kStageOpenFlower;
           daysOpen := 0;
           end;
      end;
    kStageOpenFlower: {if over optimal or over min fraction to create fruit and over max days to grow, set fruit}
      begin
      inc(daysOpen);
      if self.daysOpen > plant.pFlower[gender].daysBeforeDrop then
        self.hasFallenOff := true
      else if gender <> kGenderMale then
        begin
        with plant.pFlower[gender] do
          begin
          // limit on time to set fruit (as opposed to grow) if want to keep flowers on plant longer
          if age > minDaysBeforeSettingFruit then
            begin
            // upper limit on growth; must be at least as old as minDaysToGrow unless there is optimal biomass
            minDaysWithOptimalBiomass := (age > minDaysToGrow) and (liveBiomass_pctMPB >= optimalBiomass_pctMPB);
            // lower limit on growth; if don't have enough to make fruit, give up after max days and make anyway
            biomassToMakeFruit_pctMPB := minFractionOfOptimalBiomassToCreateFruit_frn * optimalBiomass_pctMPB;
            maxDaysWithMinFraction := (age > maxDaysToGrowIfOverMinFraction) or (liveBiomass_pctMPB >= biomassToMakeFruit_pctMPB);
            if maxDaysWithMinFraction or minDaysWithOptimalBiomass then
              begin
              stage := kStageUnripeFruit;
              daysAccumulatingFruitBiomass := 0;
              { flower biomass drops off, 50% goes into developing fruit (ovary) }
              { choice of 50% is arbitrary - could be parameter in future depending on size of flower parts/ovary }
              anthesisLoss_pctMPB := self.liveBiomass_pctMPB * 0.5;
              liveBiomass_pctMPB := liveBiomass_pctMPB - anthesisLoss_pctMPB;
              deadBiomass_pctMPB := deadBiomass_pctMPB + anthesisLoss_pctMPB;
              propFullSize := (Min(1.0, safedivExcept(self.totalBiomass_pctMPB, plant.pFruit.optimalBiomass_pctMPB, 0.0)));
              end;
            end;
          end;
        end;
      end;
    kStageUnripeFruit, kStageRipeFruit:
      begin
      if (stage = kStageUnripeFruit) and (daysAccumulatingFruitBiomass >= plant.pFruit.daysToRipen) then
        stage := kStageRipeFruit;
      inc(daysAccumulatingFruitBiomass);
      end;
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdFlowerFruit.nextDay');
  end;
  end;

procedure PdFlowerFruit.traverseActivity(mode: integer; traverserProxy: TObject);
  var
    traverser: PdTraverser;
    newPropFullSize, newBiomass_pctMPB, newOptimalBiomass_pctMPB, biomassToRemove_pctMPB: single;
    fractionOfMaxAge_frn: single;
  begin
  inherited traverseActivity(mode, traverserProxy);
  traverser := PdTraverser(traverserProxy);
  if traverser = nil then exit;
  if self.hasFallenOff
    and (mode <> kActivityStream)
    and (mode <> kActivityFree)
    and (mode <> kActivityGatherStatistics) then
    exit;
  try
  case mode of
    kActivityNone: ;
    kActivityNextDay: self.nextDay;
    kActivityDemandVegetative: { has no vegetative demand };
    kActivityDemandReproductive:
      begin
      case self.stage of
        kStageFlowerBud, kStageOpenFlower: { accum. biomass for flower }
          begin
          with plant.pFlower[gender] do
            self.biomassDemand_pctMPB := linearGrowthResult(liveBiomass_pctMPB, optimalBiomass_pctMPB, minDaysToGrow);
          traverser.total := traverser.total + self.biomassDemand_pctMPB;
          end;
        kStageUnripeFruit, kStageRipeFruit: { accum. biomass for fruit }
          begin
          if self.daysAccumulatingFruitBiomass > plant.pFruit.maxDaysToGrow then
            self.biomassDemand_pctMPB := 0.0
          else with plant.pFruit do
            begin
            fractionOfMaxAge_frn := safedivExcept(daysAccumulatingFruitBiomass + 1, maxDaysToGrow, 0.0);
            newPropFullSize := Max(0.0, Min (1.0, scurve(fractionOfMaxAge_frn, sCurveParams.c1, sCurveParams.c2)));
            newOptimalBiomass_pctMPB := newPropFullSize * optimalBiomass_pctMPB;
            with plant.pFruit do
              self.biomassDemand_pctMPB := linearGrowthResult(liveBiomass_pctMPB, newOptimalBiomass_pctMPB, 1);
            traverser.total := traverser.total + self.biomassDemand_pctMPB;
            end;
          end;
        end;
      end;
    kActivityGrowVegetative: { cannot grow vegetatively };
    kActivityGrowReproductive:
      begin
      {Allocate portion of total new biomass based on this demand over total demand.}
      newBiomass_pctMPB := self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB + newBiomass_pctMPB;
      case self.stage of
        kStageFlowerBud, kStageOpenFlower:
          propFullSize := (Min(1.0, safedivExcept(self.totalBiomass_pctMPB, plant.pFlower[gender].optimalBiomass_pctMPB, 0.0)));
        kStageUnripeFruit, kStageRipeFruit:
          propFullSize := (Min(1.0, safedivExcept(self.totalBiomass_pctMPB, plant.pFruit.optimalBiomass_pctMPB, 0.0)));
        end;
      end;
    kActivityStartReproduction: { can't switch because has no vegetative mode };
    kActivityFindPlantPartAtPosition:
      begin
      if pointsAreCloseEnough(traverser.point, self.position) then
        begin
        traverser.foundPlantPart := self;
        traverser.finished := true;
        end;
      end;
    kActivityDraw: { inflorescence should handle telling flowers to draw };
    kActivityReport: ;
    kActivityStream: {streaming called by inflorescence};
    kActivityFree: { free called by inflorescence };
    kActivityVegetativeBiomassThatCanBeRemoved: { none };
    kActivityRemoveVegetativeBiomass: { do nothing };
    kActivityReproductiveBiomassThatCanBeRemoved:
      traverser.total := traverser.total + self.liveBiomass_pctMPB;
    kActivityRemoveReproductiveBiomass:
      begin
      if self.liveBiomass_pctMPB <= 0.0 then exit;
      biomassToRemove_pctMPB := self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
      self.liveBiomass_pctMPB := self.liveBiomass_pctMPB - biomassToRemove_pctMPB;
      self.deadBiomass_pctMPB := self.deadBiomass_pctMPB + biomassToRemove_pctMPB;
      if self.liveBiomass_pctMPB <= 0.0 then
        begin
        if (stage = kStageUnripeFruit) or (stage = kStageRipeFruit) then
          self.hasFallenOff := true;
        end;
      end;
    kActivityGatherStatistics:
      begin
      case stage of
        kStageFlowerBud:
          if gender = kGenderMale then
            begin
            if self.hasFallenOff then
              self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFlower)
            else
              self.addToStatistics(traverser.statistics, kStatisticsPartTypeMaleFlowerBud);
            end
          else
            begin
            if self.hasFallenOff then
              self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFlower)
            else
              self.addToStatistics(traverser.statistics, kStatisticsPartTypeFemaleFlowerBud);
            end;
        kStageOpenFlower:
          if gender = kGenderMale then
            begin
            if self.hasFallenOff then
              self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFlower)
            else
              self.addToStatistics(traverser.statistics, kStatisticsPartTypeMaleFlower);
            end
          else
            begin
            if self.hasFallenOff then
              self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFlower)
            else
              self.addToStatistics(traverser.statistics, kStatisticsPartTypeFemaleFlower);
            end;
        kStageUnripeFruit:
           if self.hasFallenOff then
             self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFruit)
           else
             self.addToStatistics(traverser.statistics, kStatisticsPartTypeUnripeFruit);
        kStageRipeFruit:
           if self.hasFallenOff then
             self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFruit)
           else
             self.addToStatistics(traverser.statistics, kStatisticsPartTypeFruit);
        else
          raise Exception.create('Problem: Invalid fruit stage in method PdFlowerFruit.traverseActivity.');
        end;
      self.addToStatistics(traverser.statistics, kStatisticsPartTypeAllReproductive);
      end;
    kActivityCountPlantParts:  ;
    kActivityFindPartForPartID: ;
    kActivityCountTotalMemoryUse: inc(traverser.totalMemorySize, self.instanceSize);
    kActivityCalculateBiomassForGravity: ;
    kActivityCountPointsAndTrianglesFor3DExport:
      begin
      self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser);
      end;
    else
      raise Exception.create('Problem: Unhandled mode for plant draw activity in method PdFlowerFruit.traverseActivity.');
    end;
  except
    on e: Exception do messageForExceptionType(e, 'PdFlowerFruit.traverseActivity');
  end;
  end;

procedure PdFlowerFruit.report;
  begin
  inherited report;
  // DebugPrint(' flower/fruit, age '  + IntToStr(age) + ' biomass '  + floatToStr(self.liveBiomass_pctMPB));
  end;

function PdFlowerFruit.dxfIndexForFloralLayerType(aType: smallint; line: boolean): smallint;
  begin
  result := 0;
  case aType of
    kBud: result := kExportPartFlowerBudFemale;
    kPistils: if line then result := kExportPartStyleFemale else result := kExportPartStigmaFemale;
    kStamens: if line then result := kExportPartFilamentFemale else result := kExportPartAntherFemale;
    kFirstPetals: result := kExportPartFirstPetalsFemale;
    kSecondPetals: result := kExportPartSecondPetalsFemale;
    kThirdPetals: result := kExportPartThirdPetalsFemale;
    kFourthPetals: result := kExportPartFourthPetalsFemale;
    kFifthPetals: result := kExportPartFifthPetalsFemale;
    kSepals: result := kExportPartSepalsFemale;
    end;
  end;

const
  kDrawTDOOpen = true;
  kDrawTDOClosed = false;

procedure PdFlowerFruit.draw;
  var
    scale, length, width: single;
    turtle: KfTurtle;
  begin
  if (plant.turtle = nil) then exit;
  turtle := plant.turtle;
  self.boundsRect := Rect(0, 0, 0, 0);
  if self.hasFallenOff then exit;
  turtle.push;
  self.determineAmendmentAndAlsoForChildrenIfAny;
  if self.hiddenByAmendment then
    begin
    turtle.pop;
    exit;
    end
  else
    self.applyAmendmentRotations;
  try
  case stage of
    kStageFlowerBud:
      // kDrawNoBud = 0; kDrawSingleTdoBud = 1; kDrawOpeningFlower = 2;
      case plant.pFlower[gender].budDrawingOption of
        kDrawNoBud: exit;
        kDrawSingleTdoBud:
          with plant.pFlower[gender].tdoParams[kBud] do
            begin
            scale := ((scaleAtFullSize / 100.0) * propFullSize);
            turtle.rotateX(self.angleWithSway(xRotationBeforeDraw));
            turtle.rotateY(self.angleWithSway(yRotationBeforeDraw));
            turtle.rotateZ(self.angleWithSway(zRotationBeforeDraw));
            drawCircleOfTdos(object3D, faceColor, backfaceColor, pullBackAngle, scale, repetitions, radiallyArranged,
                kDrawTDOClosed, kExportPartFlowerBudFemale);
            end;
        kDrawOpeningFlower:
          self.drawFlower(kDrawFlowerAsOpening);
        end;
    kStageOpenFlower:
      self.drawFlower(kDontDrawFlowerAsOpening);
    kStageUnripeFruit:
      // ripe color is regular color; alternate color is unripe color
      begin
      with plant.pFruit.tdoParams do
        begin
        scale := ((scaleAtFullSize / 100.0) * propFullSize);
        turtle.rotateX(self.angleWithSway(xRotationBeforeDraw));
        turtle.rotateY(self.angleWithSway(yRotationBeforeDraw));
        turtle.rotateZ(self.angleWithSway(zRotationBeforeDraw));
        drawCircleOfTdos(object3D, alternateFaceColor, alternateBackfaceColor, pullBackAngle, scale, repetitions, radiallyArranged,
          kDrawTDOClosed, kExportPartUnripeFruit);
        end;
      end;
    kStageRipeFruit:
      begin
      with plant.pFruit.tdoParams do
        begin
        scale := ((scaleAtFullSize / 100.0) * propFullSize);
        turtle.rotateX(self.angleWithSway(xRotationBeforeDraw));
        turtle.rotateY(self.angleWithSway(yRotationBeforeDraw));
        turtle.rotateZ(self.angleWithSway(zRotationBeforeDraw));
        drawCircleOfTdos(object3D, faceColor, backfaceColor, pullBackAngle, scale, repetitions, radiallyArranged,
          kDrawTDOClosed, kExportPartRipeFruit);
        end;
     end;
    end;
  hasBeenDrawn := true;
  turtle.pop;
  except
    on e: Exception do messageForExceptionType(e, 'PdFlowerFruit.draw');
  end;
  end;

procedure PdFlowerFruit.drawFlower(drawAsOpening: boolean);
  var
    turtle: KfTurtle;
    angle, scale: single;
    layerType: smallint;
  begin
  if (plant.turtle = nil) then exit;
  turtle := plant.turtle;
  self.drawPistilsAndStamens(drawAsOpening);
  for layerType := kFirstPetals to kSepals do
    begin
    turtle.push;
    with plant.pFlower[gender].tdoParams[layerType] do
      begin
      scale := ((scaleAtFullSize / 100.0) * propFullSize);
      angle := self.angleWithSway(pullBackAngle);
      if drawAsOpening then
        begin
        angle := angle * propFullSize * 2;
        if angle > pullBackAngle then angle := pullBackAngle;
        end;
      turtle.rotateX(self.angleWithSway(xRotationBeforeDraw));
      turtle.rotateY(self.angleWithSway(yRotationBeforeDraw));
      turtle.rotateZ(self.angleWithSway(zRotationBeforeDraw));
      drawCircleOfTdos(object3D, faceColor, backfaceColor, angle, scale, repetitions, radiallyArranged,
        kDrawTDOOpen, self.dxfIndexForFloralLayerType(layerType, kNotLine));
        end;
    turtle.pop;
    end;
  end;

procedure PdFlowerFruit.drawPistilsAndStamens(drawAsOpening: boolean);
  var
    scale, length, width, angle: single;
    turtle: KfTurtle;
    i: smallint;
    turnPortion, leftOverDegrees, addThisTime: integer;
    addition, carryOver: single; 
  begin
  if (plant.turtle = nil) then exit;
  turtle := plant.turtle;
  turtle.push;
  with plant.pFlower[gender] do if (numPistils > 0) then
    begin
    if ((styleLength_mm > 0) and (styleWidth_mm > 0)) or (tdoParams[kPistils].scaleAtFullSize > 0)  then
        turtle.ifExporting_startNestedGroupOfPlantParts('pistils', 'Pistils', kNestingTypeFloralLayers);
    turnPortion := 256 div numPistils;
    leftOverDegrees := 256 - turnPortion * numPistils;
    if leftOverDegrees > 0 then
      addition := safedivExcept(leftOverDegrees, numPistils, 0)
    else
      addition := 0;
    carryOver := 0;
    for i := 0 to numPistils - 1 do
      begin
      turtle.push;
      if (styleLength_mm > 0) and (styleWidth_mm > 0) then
        begin
        length := max(0.0, propFullSize * styleLength_mm);
        width := max(0.0, propFullSize * styleWidth_mm);
        angle := self.angleWithSway(plant.pFlower[gender].tdoParams[kPistils].pullBackAngle);
        if drawAsOpening then angle := angle * propFullSize;
        self.drawStemSegment(length, width, angle, 0, styleColor, styleTaperIndex,
            self.dxfIndexForFloralLayerType(kPistils, kLine), kDontUseAmendment);
        end;
      with plant.pFlower[gender].tdoParams[kPistils] do
        begin
        scale := ((scaleAtFullSize / 100.0) * propFullSize);
        turtle.rotateX(self.angleWithSway(xRotationBeforeDraw));
        turtle.rotateY(self.angleWithSway(yRotationBeforeDraw));
        turtle.rotateZ(self.angleWithSway(zRotationBeforeDraw));
        drawCircleOfTdos(object3D, faceColor, backfaceColor, 0, scale, repetitions, radiallyArranged,
          kDrawTDOOpen, self.dxfIndexForFloralLayerType(kPistils, kNotLine));
        end;
      turtle.pop;
      addThisTime := trunc(addition + carryOver);
      carryOver := carryOver + addition - addThisTime;
      if carryOver < 0 then carryOver := 0;
      turtle.rotateX(turnPortion + addThisTime);
      end;
    if ((styleLength_mm > 0) and (styleWidth_mm > 0)) or (tdoParams[kPistils].scaleAtFullSize > 0)  then
      turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeFloralLayers);
    end;
  turtle.pop;
  // stamens
  turtle.push;
  with plant.pFlower[gender] do if numStamens > 0 then
    begin
    if ((filamentLength_mm > 0) and (filamentWidth_mm > 0)) or (tdoParams[kStamens].scaleAtFullSize > 0)  then
      begin
      if self.gender = kGenderFemale then
        turtle.ifExporting_startNestedGroupOfPlantParts('primary stamens', '1Stamens', kNestingTypeFloralLayers)
      else
        turtle.ifExporting_startNestedGroupOfPlantParts('secondary stamens', '2Stamens', kNestingTypeFloralLayers);
      end;
    turnPortion := 256 div numStamens;
    leftOverDegrees := 256 - turnPortion * numStamens;
    if leftOverDegrees > 0 then
      addition := safedivExcept(leftOverDegrees, numStamens, 0)
    else
      addition := 0;
    carryOver := 0;
    for i := 0 to numStamens - 1 do
      begin
      turtle.push;
      if (filamentLength_mm > 0) and (filamentWidth_mm > 0) then
        begin
        length := max(0.0, propFullSize * filamentLength_mm);
        width := max(0.0, propFullSize * filamentWidth_mm);
        angle := self.angleWithSway(plant.pFlower[gender].tdoParams[kStamens].pullBackAngle);
        if drawAsOpening then angle := angle * propFullSize;
        self.drawStemSegment(length, width, angle, 0, filamentColor, filamentTaperIndex,
            self.dxfIndexForFloralLayerType(kStamens, kLine), kDontUseAmendment);
        end;
      with plant.pFlower[gender].tdoParams[kStamens] do
        begin
        scale := ((scaleAtFullSize / 100.0) * propFullSize);
        turtle.rotateX(self.angleWithSway(xRotationBeforeDraw));
        turtle.rotateY(self.angleWithSway(yRotationBeforeDraw));
        turtle.rotateZ(self.angleWithSway(zRotationBeforeDraw));
        drawCircleOfTdos(object3D, faceColor, backfaceColor, 0, scale, repetitions, radiallyArranged,
          kDrawTDOOpen, self.dxfIndexForFloralLayerType(kStamens, kNotLine));
        end;
      turtle.pop;
      addThisTime := trunc(addition + carryOver);
      carryOver := carryOver + addition - addThisTime;
      if carryOver < 0 then carryOver := 0;
      turtle.rotateX(turnPortion + addThisTime);
      end;
    if ((filamentLength_mm > 0) and (filamentWidth_mm > 0)) or (tdoParams[kStamens].scaleAtFullSize > 0)  then
      turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeFloralLayers);
    end;
  turtle.pop;
  end;

procedure PdFlowerFruit.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser: PdTraverser);
  var numLines: integer;
  begin
  if traverser = nil then exit;
  if propFullSize <= 0 then exit;
  if self.hasFallenOff then exit;
  case stage of
    kStageFlowerBud:
      begin
      case plant.pFlower[gender].budDrawingOption of
        kDrawNoBud: ;
        kDrawSingleTdoBud:
          with plant.pFlower[gender].tdoParams[kBud] do if scaleAtFullSize > 0 then
            begin
            inc(traverser.total3DExportPointsIn3DObjects, object3d.pointsInUse * repetitions);
            inc(traverser.total3DExportTrianglesIn3DObjects, object3d.triangles.count * repetitions);
            addExportMaterial(traverser, kExportPartFlowerBudFemale, kExportPartFlowerBudMale);
            end;
        kDrawOpeningFlower:
          self.addFloralPartsCountsToTraverser(traverser);
        end;
      end;
    kStageOpenFlower: self.addFloralPartsCountsToTraverser(traverser);
    kStageUnripeFruit, kStageRipeFruit:
      with plant.pFruit.tdoParams do if scaleAtFullSize > 0 then
        begin
        inc(traverser.total3DExportPointsIn3DObjects, object3d.pointsInUse * repetitions);
        inc(traverser.total3DExportTrianglesIn3DObjects, object3d.triangles.count * repetitions);
        if stage = kStageUnripeFruit then
          addExportMaterial(traverser, kExportPartUnripeFruit, -1)
        else
          addExportMaterial(traverser, kExportPartRipeFruit, -1)
        end;
    end;
  // pedicel handled by inflorescence
  end;

procedure PdFlowerFruit.addFloralPartsCountsToTraverser(traverser: PdTraverser);
  var partType: integer;
  begin
  for partType := kPistils to kSepals do
    with plant.pFlower[gender].tdoParams[partType] do if scaleAtFullSize > 0 then
      begin
      if partType = kPistils then
        begin
        inc(traverser.total3DExportPointsIn3DObjects,
            object3D.pointsInUse * repetitions * plant.pFlower[gender].numPistils);
        inc(traverser.total3DExportTrianglesIn3DObjects,
            object3D.triangles.count * repetitions * plant.pFlower[gender].numPistils);
        addExportMaterial(traverser, kExportPartStyleFemale, -1);
        addExportMaterial(traverser, kExportPartStigmaFemale, -1);
        end
      else if partType = kStamens then
        begin
        inc(traverser.total3DExportPointsIn3DObjects,
            object3D.pointsInUse * repetitions * plant.pFlower[gender].numStamens);
        inc(traverser.total3DExportTrianglesIn3DObjects,
            object3D.triangles.count * repetitions * plant.pFlower[gender].numStamens);
        addExportMaterial(traverser, kExportPartFilamentFemale, kExportPartFilamentMale);
        addExportMaterial(traverser, kExportPartAntherFemale, kExportPartAntherMale);
        end
      else
        begin
        inc(traverser.total3DExportPointsIn3DObjects, object3D.pointsInUse * repetitions);
        inc(traverser.total3DExportTrianglesIn3DObjects, object3D.triangles.count * repetitions);
        case partType of
          kFirstPetals:  addExportMaterial(traverser, kExportPartFirstPetalsFemale, kExportPartFirstPetalsMale);
          kSecondPetals: addExportMaterial(traverser, kExportPartSecondPetalsFemale, -1);
          kThirdPetals:  addExportMaterial(traverser, kExportPartThirdPetalsFemale, -1);
          kFourthPetals: addExportMaterial(traverser, kExportPartFourthPetalsFemale, -1);
          kFifthPetals:  addExportMaterial(traverser, kExportPartFifthPetalsFemale, -1);
          kSepals:       addExportMaterial(traverser, kExportPartSepalsFemale, kExportPartSepalsMale);
          end;
        end;
      end;
  end;

function PdFlowerFruit.triangleCountInFloralParts: integer;
  var partType: integer;
  begin
  result := 0;
  for partType := kPistils to kSepals do
    with plant.pFlower[gender].tdoParams[partType] do
      if scaleAtFullSize > 0 then
        begin
        if partType = kPistils then
          result := result + object3D.triangles.count * repetitions * plant.pFlower[gender].numPistils
        else if partType = kStamens then
          result := result + object3D.triangles.count * repetitions * plant.pFlower[gender].numStamens
        else
          result := result + object3D.triangles.count * repetitions;
        end;
  end;

function PdFlowerFruit.tdoToSortLinesWith: KfObject3D;
  begin
  result := nil;
  if plant = nil then exit;
  if self.hasFallenOff then exit;
  case stage of
    kStageFlowerBud: result := plant.pFlower[gender].tdoParams[kBud].object3D;
    kStageOpenFlower: result := plant.pFlower[gender].tdoParams[kFirstPetals].object3D;
    kStageUnripeFruit, kStageRipeFruit: result := plant.pFruit.tdoParams.object3D;
    end;
  end;

procedure PdFlowerFruit.drawCircleOfTdos(tdo: KfObject3D; faceColor, backfaceColor: TColorRef; pullBackAngle: single;
    scale: single; numParts: integer; partsArranged: boolean; open: boolean; dxfIndex: smallint);
  var
    turtle: KfTurtle;
    i: integer;
    minZ: single;
    turnPortion, leftOverDegrees, addThisTime: integer; // v1.3
    addition, carryOver: single; // v1.3
  begin
  try
  if (scale <= 0.0) then exit;
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  turtle.push;
  minZ := 0;
  if (partsArranged) and (numParts > 0) then
    begin
    turtle.ifExporting_startPlantPart(self.longNameForDXFPartConsideringGenderEtc(dxfIndex),
        self.shortNameForDXFPartConsideringGenderEtc(dxfIndex));
    turnPortion := 256 div numParts;
    leftOverDegrees := 256 - turnPortion * numParts;
    if leftOverDegrees > 0 then
      addition := safedivExcept(leftOverDegrees, numParts, 0)
    else
      addition := 0;
    carryOver := 0;
    for i := 1 to numParts do
      begin
      addThisTime := trunc(addition + carryOver);
      carryOver := carryOver + addition - addThisTime;
      if carryOver < 0 then carryOver := 0;
			turtle.RotateX(turnPortion + addThisTime);
      turtle.push;
      turtle.RotateZ(-64); {aligns object as stored in the file to way should draw on plant}
      if open then turtle.RotateY(32); {pulls petal up to plane of stalk (is perpendicular)}
      turtle.rotateX(pullBackAngle);
      if tdo <> nil then
        begin
        self.draw3DObject(tdo, scale, faceColor, backfaceColor, dxfIndex);
        if i = 1 then
          minZ := tdo.zForSorting
        else if tdo.zForSorting < minZ then
          minZ := tdo.zForSorting;
        end;
      turtle.pop;
      end;
    if tdo <> nil then tdo.zForSorting := minZ;
    turtle.ifExporting_endPlantPart;
    end
  else
    begin
    turtle.push;
    if (stage = kStageUnripeFruit) or (stage = kStageRipeFruit) then
      turtle.RotateZ(-64)
    else
      turtle.RotateZ(-pullBackAngle); {pulls petal up to plane of stalk (is perpendicular)}
    if tdo <> nil then self.draw3DObject(tdo, scale, faceColor, backfaceColor, dxfIndex);
    turtle.pop;
    end;
  turtle.pop;
except
    on e: Exception do messageForExceptionType(e, 'PdFlowerFruit.drawCircleOfTdos');
end;
  end;

function PdFlowerFruit.partType: integer;
  begin
  result := kPartTypeFlowerFruit;
  end;

procedure PdFlowerFruit.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdFlowerFruit;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure PdFlowerFruit.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
    streamSingle(propFullSize);
    streamSmallint(stage);
    streamBoolean(hasBeenDrawn);
    streamLongint(daysAccumulatingFruitBiomass);
    streamLongint(daysOpen);
    end;
  end;

end.


{ cfk remember this }
{ ---------------------------------------------------------------------- wilting/falling down }
{procedure PdFlowerFruit.dragDownFromWeight;
  begin
  end; }
{procedure PdFlowerFruit.dragDownFromWeight;
  var
    fractionOfOptimalFruitWeight_frn: single;
    angle: integer;
  begin
  if (plant.turtle = nil) then exit;
  fractionOfOptimalFruitWeight_frn := safedivExcept(liveBiomass_pctMPB, plant.pFruit.optimalBiomass_pctMPB, 0.0);
  angle := round(abs(plant.turtle.angleZ + 32) * fractionOfOptimalFruitWeight_frn
      * min(1.0, max(0.0, 100 - plant.pFruit.stalkStrengthIndex) / 100.0));
  angle := -angle;
  if plant.turtle.angleZ > -32 then
    angle := -angle;
  plant.turtle.rotateZ(angle);
  end;  }

