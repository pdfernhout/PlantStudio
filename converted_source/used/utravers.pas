unit Utravers;

interface

uses WinTypes, Classes,
  uplant, upart, ufiler, u3dexport;

const
  kTraverseNone = 0; kTraverseLeft = 1; kTraverseRight = 2; kTraverseNext = 3; kTraverseDone = 4;
  kActivityNone = 0; 
  kActivityNextDay = 1; 
  kActivityDemandVegetative = 2;
  kActivityDemandReproductive = 3;
  kActivityGrowVegetative = 4;
  kActivityGrowReproductive = 5;
  kActivityStartReproduction = 6;
  kActivityFindPlantPartAtPosition = 7;
  kActivityDraw = 8;
  kActivityReport = 9;
  kActivityStream = 10;
  kActivityFree = 11;
  kActivityVegetativeBiomassThatCanBeRemoved = 12;
  kActivityRemoveVegetativeBiomass = 13;
  kActivityReproductiveBiomassThatCanBeRemoved = 14;
  kActivityRemoveReproductiveBiomass = 15;
  kActivityGatherStatistics = 16;
  kActivityStandingDeadBiomassThatCanBeRemoved = 17;
  kActivityRemoveStandingDeadBiomass = 18;
  kActivityCountPlantParts = 19;
  kActivityFindPartForPartID = 20;
  kActivityCountTotalMemoryUse = 21;
  kActivityCalculateBiomassForGravity = 22;
  kActivityCountPointsAndTrianglesFor3DExport = 23;

const
  kStatisticsPartTypeSeedlingLeaf = 0;
  kStatisticsPartTypeLeaf = 1;
  kStatisticsPartTypeFemaleInflorescence = 2;
  kStatisticsPartTypeMaleInflorescence = 3;
  kStatisticsPartTypeFemaleFlower = 4;
  kStatisticsPartTypeFemaleFlowerBud = 5;
  kStatisticsPartTypeMaleFlower = 6;
  kStatisticsPartTypeMaleFlowerBud = 7;
  kStatisticsPartTypeAxillaryBud = 8;  // meristems
  kStatisticsPartTypeFruit = 9;
  kStatisticsPartTypeStem = 10;
  kStatisticsPartTypeUnripeFruit = 11;
  kStatisticsPartTypeFallenFruit = 12;
  kStatisticsPartTypeUnallocatedNewVegetativeBiomass = 13;
  kStatisticsPartTypeUnremovedDeadVegetativeBiomass = 14;
  kStatisticsPartTypeUnallocatedNewReproductiveBiomass = 15;
  kStatisticsPartTypeUnremovedDeadReproductiveBiomass = 16;
  kStatisticsPartTypeFallenFlower = 17;
  kStatisticsPartTypeAllVegetative = 18;
  kStatisticsPartTypeAllReproductive = 19;
  kStatisticsPartTypeLast = 19;

type
PdPlantStatistics = class
  public
  count: array[0..kStatisticsPartTypeLast] of longint;
  liveBiomass_pctMPB: array[0..kStatisticsPartTypeLast] of single;
  deadBiomass_pctMPB: array[0..kStatisticsPartTypeLast] of single;
  procedure zeroAllFields;
  function totalBiomass_pctMPB: single;
  end;

PdTraverser = class(TObject)
  public
  plant: PdPlant;
  filer: PdFiler;
  currentPhytomer: TObject;
  point: TPoint;
  total: single;
  fractionOfPotentialBiomass: single;
  ageOfYoungestPhytomer: longint;
  mode: smallint;
  finished: boolean;
  foundPlantPart: PdPlantPart;
  foundList: TList;
  statistics: PdPlantStatistics;
  totalPlantParts: longint;
  total3DExportPointsIn3DObjects: longint;
  total3DExportTrianglesIn3DObjects: longint;
  total3DExportStemSegments: longint;
  showDrawingProgress: boolean;
  plantPartsDrawnAtStart: longint;
  partID: longint;
  totalMemorySize: longint;
  exportTypeCounts: array[0..kExportPartLast] of longint;
  constructor createWithPlant(thePlant: PdPlant);
  procedure traversePlant(traversalCount: longint);
  procedure beginTraversal(aMode: integer);
  procedure traverseWholePlant(aMode: integer);
  end;

var
  cancelDrawing: boolean;
  worstNStressColor: TColorRef;
  worstPStressColor: TColorRef;
  worstDeadColor: TColorRef;

function linearGrowthWithFactorResult(current, optimal: single; minDays: integer; growthFactor: single): single;
procedure linearGrowthWithFactor(var current: single; optimal: single; minDays: integer; growthFactor: single);
function linearGrowthResult(current, optimal: single; minDays: integer): single;
procedure linearGrowth(var current: single; optimal: single; minDays: integer);

implementation

uses WinProcs, SysUtils, Forms,
  usupport, umath, udebug, uintern, umain, utimeser, ubreedr;

{ -------------------------------------------------------------------------- linear growth functions }
function linearGrowthWithFactorResult(current, optimal: single; minDays: integer; growthFactor: single): single;
  var
    amountNeeded, maxPossible: single;
  begin
  result := 0.0;
  try
    amountNeeded := optimal - current;
    maxPossible := safedivExcept(optimal, minDays, optimal);
    amountNeeded := max(0.0, min(amountNeeded, maxPossible));
    result := amountNeeded * growthFactor;
  except
    on e: Exception do messageForExceptionType(e, 'linearGrowthWithFactorResult');
  end;
  end;

procedure linearGrowthWithFactor(var current: single; optimal: single; minDays: integer; growthFactor: single);
  var
    amountNeeded, maxPossible: single;
  begin
  try
    amountNeeded := optimal - current;
    maxPossible := safedivExcept(optimal, minDays, optimal);
    amountNeeded := max(0.0, min(amountNeeded, maxPossible));
    current := current + amountNeeded * growthFactor;
  except
    on e: Exception do messageForExceptionType(e, 'linearGrowthWithFactor');
  end;
  end;

function linearGrowthResult(current, optimal: single; minDays: integer): single;
  var
    amountNeeded, maxPossible: single;
  begin
  result := 0.0;
  try
    amountNeeded := optimal - current;
    maxPossible := safedivExcept(optimal, minDays, optimal);
    amountNeeded := max(0.0, min(amountNeeded, maxPossible));
    result := amountNeeded;
  except
    on e: Exception do messageForExceptionType(e, 'linearGrowthResult');
  end;
  end;

procedure linearGrowth(var current: single; optimal: single; minDays: integer);
  var
    amountNeeded, maxPossible: single;
  begin
  try
    amountNeeded := optimal - current;
    maxPossible := safedivExcept(optimal, minDays, optimal);
    amountNeeded := max(0.0, min(amountNeeded, maxPossible));
    current := current + amountNeeded;
  except
    on e: Exception do messageForExceptionType(e, 'linearGrowth');
  end;
  end;

{ ---------------------------------------------------------------------------------- traversing object }
constructor PdTraverser.createWithPlant(thePlant: PdPlant);
  begin
  self.create;
  plant := thePlant;
  end;

procedure PdTraverser.beginTraversal(aMode: integer);
  begin
  mode := aMode;
  currentPhytomer := plant.firstPhytomer;
  self.total := 0.0;
  self.finished := false;
  foundPlantPart := nil;
  totalPlantParts := 0;
  if currentPhytomer <> nil then
    begin
    PdInternode(currentPhytomer).traversingDirection := kTraverseLeft;
    PdInternode(currentPhytomer).traverseActivity(mode, self);
    {reset afterwards in case read in differently}
    PdInternode(currentPhytomer).traversingDirection := kTraverseLeft;
    end;
  end;

procedure PdTraverser.traverseWholePlant(aMode: integer);
  begin                
  self.beginTraversal(aMode);
  self.traversePlant(0);
  end;

procedure PdTraverser.traversePlant(traversalCount: longint);
  var
    i: longint;
    lastPhytomer: PdInternode;
    phytomerTraversing: PdInternode;
  begin
  if (currentPhytomer = nil) then exit;
  phytomerTraversing := PdInternode(currentPhytomer);
  i := 0;
  while i <= traversalCount do
    begin
    if self.finished then exit;
    case phytomerTraversing.traversingDirection of
      kTraverseLeft:
        begin
        inc(phytomerTraversing.traversingDirection);
        if phytomerTraversing.leftBranchPlantPart <> nil then
          begin
          if (mode = kActivityDraw) then plant.turtle.push;
          phytomerTraversing.leftBranchPlantPart.traverseActivity(mode, self);
          if (phytomerTraversing.leftBranchPlantPart.isPhytomer) then
            begin
            phytomerTraversing := PdInternode(phytomerTraversing.leftBranchPlantPart);
            phytomerTraversing.traversingDirection := kTraverseLeft;
            end
          else
            if (mode = kActivityDraw) then plant.turtle.pop;
          end;
        end;
      kTraverseRight:
        begin
        inc(phytomerTraversing.traversingDirection);
        if phytomerTraversing.rightBranchPlantPart <> nil then
          begin
          if (mode = kActivityDraw) then plant.turtle.push;
          phytomerTraversing.rightBranchPlantPart.traverseActivity(mode, self);
          if (phytomerTraversing.rightBranchPlantPart.isPhytomer) then
            begin
            phytomerTraversing := PdInternode(phytomerTraversing.rightBranchPlantPart);
            phytomerTraversing.traversingDirection := kTraverseLeft;
            end
          else
            if (mode = kActivityDraw) then plant.turtle.pop;
          end;
        end;
      kTraverseNext:
        begin
        inc(phytomerTraversing.traversingDirection);
        if phytomerTraversing.nextPlantPart <> nil then
          begin
          if (mode = kActivityDraw) then
            begin
            plant.turtle.push;
            plant.turtle.RotateX(plant.pGeneral.phyllotacticRotationAngle * 256 / 360);
            end;
          phytomerTraversing.nextPlantPart.traverseActivity(mode, self);
          if (phytomerTraversing.nextPlantPart.isPhytomer) then
            begin
            phytomerTraversing := PdInternode(phytomerTraversing.nextPlantPart);
            phytomerTraversing.traversingDirection := kTraverseLeft;
            end
          else
            if (mode = kActivityDraw) then plant.turtle.pop;
          end;
        end;
      kTraverseDone:
        begin
        phytomerTraversing.traversingDirection := kTraverseNone;
        lastPhytomer := phytomerTraversing;
        phytomerTraversing := phytomerTraversing.phytomerAttachedTo;
        if (mode = kActivityFree) then
          begin
          lastPhytomer.free;
          if phytomerTraversing <> nil then
            begin
        	  if (phytomerTraversing.traversingDirection = kTraverseLeft + 1) then
              phytomerTraversing.leftBranchPlantPart := nil
            else if (phytomerTraversing.traversingDirection =  kTraverseRight + 1)  then
              phytomerTraversing.rightBranchPlantPart := nil
            else if (phytomerTraversing.traversingDirection =  kTraverseNext + 1)  then
              phytomerTraversing.nextPlantPart := nil;
            end;
          end;
        if phytomerTraversing = nil then break;
        {special drawing stuff - if returning from left or right branch draw, pop turtle}
        if (mode = kActivityDraw) then
          begin
         {	if (phytomerTraversing.traversingDirection = kTraverseLeft + 1)
           or (phytomerTraversing.traversingDirection =  kTraverseRight + 1)  then }
           plant.turtle.pop;
          end;
        if (mode = kActivityCalculateBiomassForGravity) then
          phytomerTraversing.traverseActivity(mode, self);
        end;
      kTraverseNone:
        raise Exception.create('Problem: kTraverseNone encountered in method PdTraverser.traversePlant.');
      end;
    if (traversalCount <> 0) then inc(i);
    if (mode = kActivityDraw) and (showDrawingProgress) then
      begin
      if totalPlantParts mod 4 <> 0 then continue;
      if (MainForm <> nil) and (MainForm.drawing) then
        MainForm.showDrawProgress(self.plantPartsDrawnAtStart + self.totalPlantParts);
      end;
    end;
  end;

{ ---------------------------------------------------------------------------------- statistics object }
procedure PdPlantStatistics.zeroAllFields;
  var i: smallint;
  begin
  for i := 0 to kStatisticsPartTypeLast do
    begin
    count[i] := 0;
    liveBiomass_pctMPB[i] := 0.0;
    deadBiomass_pctMPB[i] := 0.0;
    end;
  end;

function PdPlantStatistics.totalBiomass_pctMPB: single;
  var i: smallint;
  begin
  result := 0.0;
  for i := 0 to kStatisticsPartTypeLast do
    begin
    result := result + liveBiomass_pctMPB[i];
    result := result + deadBiomass_pctMPB[i];
    end;
  end;

end.
