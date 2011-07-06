unit upart;

interface 

uses Windows, Classes,
  uplant, umath, usupport, ufiler, utdo, uamendmt;

const
  kAddingBiomassToPlant = true; kRemovingBiomassFromPlant = false;
  kDontTaper = -1.0;
  kUseAmendment = true; kDontUseAmendment = false;

type
  PdPlantPart = class(PdStreamableObject)
  public
  plant: PdPlant;
  liveBiomass_pctMPB: single;
  deadBiomass_pctMPB: single;
  biomassDemand_pctMPB: single;
  gender: smallint;
  age: longint;
  randomSwayIndex: single;
  hasFallenOff: boolean;
  isSeedlingLeaf: boolean;
  partID: longint;
  boundsRect: TRect;
  amendment: PdPlantDrawingAmendment;
  parentAmendment: PdPlantDrawingAmendment;
  biomassOfMeAndAllPartsAboveMe_pctMPB: single;
	procedure draw; virtual;
  function getName: string; virtual;
  function getFullName: string;
  procedure report; virtual;
  procedure drawStemSegment(length, width, angleZ, angleY: single;
    color: TColorRef; taperIndex: single; dxfIndex: smallint; useAmendment: boolean);
  function tdoToSortLinesWith: KfObject3D; virtual;
  procedure write3DExportLine(partID: smallint; length, startWidth, endWidth: single; segmentNumber: smallint);
	procedure initialize(thePlant: PdPlant);
	procedure nextDay; virtual;
  function partType: integer; virtual;
  function genderString: string;
  procedure traverseActivity(mode: integer; traverserProxy: TObject); virtual;
  function isPhytomer: boolean; virtual;
  function totalBiomass_pctMPB: single;
  function fractionLive: single;
  procedure addOrRemove(addOrRemoveFlag: boolean); virtual;
  procedure addDependentPartsToList(aList: TList); virtual;
  procedure addExportMaterial(traverserProxy: TObject; femaleIndex, maleIndex: smallint);
  procedure addToStatistics(statisticsProxy: TObject; partType: smallint);
  procedure calculateColors;
  procedure blendColorsStrength(aColor: TColorRef; aStrength: single); virtual;
  procedure setColorsToParameters; virtual;
  function angleWithSway(angle: single): single;
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  procedure draw3DObject(tdo: KfObject3D; scale: single;
    faceColor, backfaceColor: TColorRef; dxfIndex: smallint);
  function longNameForDXFPartConsideringGenderEtc(index: smallint): string;
  function shortNameForDXFPartConsideringGenderEtc(index: smallint): string;
  function realDxfIndexForBaseDXFPart(index: smallint): smallint;
 // procedure fillInInfoForDXFPart(index: smallint; var realIndex: smallint; var longName: string; var shortName: string);
  function position: TPoint;
  procedure determineAmendmentAndAlsoForChildrenIfAny; virtual;
  function hiddenByAmendment: boolean;
  procedure applyAmendmentRotations;
  function setColorsWithAmendmentAndReturnTrueIfNoOverrides(drawingTdo: boolean): boolean;
  function rotateAngleConsideringAmendment(rotateWhat: smallint; useAmendment: boolean; angle: single): single;
  function scaleMultiplierConsideringAmendments: single;
  function lengthMultiplierConsideringAmendments: single;
  function widthMultiplierConsideringAmendments: single;
  end;

implementation

uses SysUtils, Graphics,
  utravers, uturtle, u3dexport, u3dsupport, uclasses, udomain, udebug, umain;

const
  kDrawingTdo = true; kDrawingLine = false;
  kRotateX = 0; kRotateY = 1; kRotateZ = 2;

{ ---------------------------------------------------------------------------------- initialize }
procedure PdPlantPart.Initialize(thePlant: PdPlant);
  begin
  {initialize generic plant part}
  plant := thePlant;
  inc(plant.partsCreated);  // v1.6b1
  partID := plant.partsCreated;
  age := 0;
  gender := kGenderFemale;
  hasFallenOff := false;
  randomSwayIndex := plant.randomNumberGenerator.zeroToOne;
  end;

procedure PdPlantPart.nextDay;
  begin
  {next day procedure for generic plant part}
  inc(age);
  end;

function PdPlantPart.getName: string;
  begin
  // subclasses should override
  result := 'plant part';
  end;

function PdPlantPart.getFullName: string;
  begin
  result := 'part ' + intToStr(self.partID) + ' (' + self.getName + ')';
  end;

{ ---------------------------------------------------------------------------------- traversing }
procedure PdPlantPart.traverseActivity(mode: integer; traverserProxy: TObject);
  var
    traverser: PdTraverser;
    biomassToRemove_pctMPB: single;
  begin
  traverser := PdTraverser(traverserProxy);
  if traverser = nil then exit;
  case mode of
    kActivityNone: ;
    kActivityNextDay: 
      {inc(traverser.totalPlantParts)};
    kActivityDemandVegetative: self.biomassDemand_pctMPB := 0.0;
    kActivityDemandReproductive: self.biomassDemand_pctMPB := 0.0;
    kActivityGrowVegetative: ;
    kActivityGrowReproductive: ;
    kActivityStartReproduction: ;
    kActivityFindPlantPartAtPosition: ;
    kActivityDraw:
      begin
      inc(traverser.totalPlantParts);
      self.determineAmendmentAndAlsoForChildrenIfAny;
      end;
    kActivityReport: self.report;
    kActivityStream: ;
    kActivityFree: ;
    kActivityVegetativeBiomassThatCanBeRemoved: ;
    kActivityRemoveVegetativeBiomass: ;
    kActivityReproductiveBiomassThatCanBeRemoved: ;
    kActivityRemoveReproductiveBiomass: ;
    kActivityStandingDeadBiomassThatCanBeRemoved:
      traverser.total := traverser.total + self.deadBiomass_pctMPB;
    kActivityRemoveStandingDeadBiomass:
      begin
      biomassToRemove_pctMPB := self.deadBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
      self.deadBiomass_pctMPB := self.deadBiomass_pctMPB - biomassToRemove_pctMPB;
      end;
    kActivityGatherStatistics: ;
    kActivityCountPlantParts:
      inc(traverser.totalPlantParts);
    kActivityFindPartForPartID:
      if traverser.partID = self.partID then
        begin
        traverser.foundPlantPart := self;
        traverser.finished := true;
        end;
    kActivityCountTotalMemoryUse: ;
    kActivityCalculateBiomassForGravity: self.biomassOfMeAndAllPartsAboveMe_pctMPB := self.totalBiomass_pctMPB;
    kActivityCountPointsAndTrianglesFor3DExport:
      inc(traverser.totalPlantParts);
    else
      raise Exception.create('Problem: Unhandled mode in method PdPlantPart.traverseActivity.');
    end;
  end;

function PdPlantPart.position: TPoint;
  begin
  with self.boundsRect do
    result := Point(left + (right - left) div 2, top + (bottom - top) div 2);
  end;

procedure PdPlantPart.addExportMaterial(traverserProxy: TObject; femaleIndex, maleIndex: smallint);
  var
    traverser: PdTraverser;
  begin
  // remember that this is not a true count; each part only adds at LEAST one
  // if you wanted to use this for a true export-type-part count you would have to amend some code
  traverser := PdTraverser(traverserProxy);
  if traverser = nil then exit;
  if maleIndex < 0 then // means to ignore gender
    inc(traverser.exportTypeCounts[femaleIndex])
  else if self.gender = kGenderFemale then
    inc(traverser.exportTypeCounts[femaleIndex])
  else
    inc(traverser.exportTypeCounts[maleIndex]);
  end;

procedure PdPlantPart.addToStatistics(statisticsProxy: TObject; partType: smallint);
  var
    statistics: PdPlantStatistics;
  begin
  statistics := PdPlantStatistics(statisticsProxy);
  if statistics = nil then exit;
  if hasFallenOff then exit;
  with statistics do
    begin
    count[partType] := count[partType] + 1;
    liveBiomass_pctMPB[partType] := liveBiomass_pctMPB[partType] + self.liveBiomass_pctMPB;
    deadBiomass_pctMPB[partType] := deadBiomass_pctMPB[partType] + self.deadBiomass_pctMPB;
    end;
  end;

function PdPlantPart.totalBiomass_pctMPB: single;
  begin
  result := liveBiomass_pctMPB + deadBiomass_pctMPB;
  end;

function PdPlantPart.fractionLive: single;
  begin
  result := 0.0;
  try
  if self.totalBiomass_pctMPB > 0.0 then
    result := safedivExcept(self.liveBiomass_pctMPB, self.totalBiomass_pctMPB, 0)
  else
    result := 0.0;
  except
    on e: Exception do messageForExceptionType(e, 'PdPlantPart.fractionLive');
  end;
  end;

procedure PdPlantPart.draw;
  begin
  { implemented by subclasses }
  end;

function PdPlantPart.isPhytomer: boolean;
  begin
  result := false;
  end;

procedure PdPlantPart.addOrRemove(addOrRemoveFlag: boolean);
  begin
  if addOrRemoveFlag = kAddingBiomassToPlant then
    hasFallenOff := false
  else
    hasFallenOff := true;
  end;
                              
procedure PdPlantPart.setColorsToParameters;
  begin
  {subclasses can override}
  end;

function PdPlantPart.genderString: string;
  begin
  if self.gender = kGenderFemale then
    result := 'primary'
  else
    result := 'secondary';
  end;

procedure PdPlantPart.report;
  var partName: string;
  begin                                              
  case self.partType of
    kPartTypeFlowerFruit: partName := 'flower/fruit';
    kPartTypeInflorescence: partName := 'inflorescence';
    kPartTypeMeristem: partName := 'meristem';
    kPartTypePhytomer: partName := 'internode';
    kPartTypeLeaf: partName := 'leaf';
    end;
  debugPrint('Part ' + intToStr(self.partID) + ', ' + partName);
  end;

{ ---------------------------------------------------------------------------------- drawing }
procedure PdPlantPart.draw3DObject(tdo: KfObject3D; scale: single;
    faceColor, backfaceColor: TColorRef; dxfIndex: smallint);
  var
    realScale: single;
    turtle: KfTurtle;
  begin
  if tdo = nil then exit;
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  if self.setColorsWithAmendmentAndReturnTrueIfNoOverrides(kDrawingTdo) then
    begin
    turtle.setForeColorBackColor(faceColor, backfaceColor);
    turtle.setLineColor(darkerColor(faceColor));
    end;
  realScale := scale * self.scaleMultiplierConsideringAmendments;
  turtle.setLineWidth(1.0);
  tdo.draw(turtle, realScale, self.longNameForDXFPartConsideringGenderEtc(dxfIndex),
      self.shortNameForDXFPartConsideringGenderEtc(dxfIndex), 
      self.realDxfIndexForBaseDXFPart(dxfIndex), self.partID);
  end;

procedure PdPlantPart.drawStemSegment(length, width, angleZ, angleY: single;
    color: TColorRef; taperIndex: single; dxfIndex: smallint; useAmendment: boolean);
  var
    turtle: KfTurtle;
    turnPortionZ, turnPortionY, drawPortion, segmentLength, segmentTurnZ, segmentTurnY: single;
    realAngleX, realAngleY, realAngleZ: single;
    lineDivisions, i: smallint;
    triangleMade: KfTriangle;
    startWidth, endWidth, startPortionWidth, endPortionWidth: single;
    isLastSegment: boolean;
    realLength, realWidth: single;
  begin
  turtle := plant.turtle;
  if (turtle = nil) then exit;
  if turtle.ifExporting_ExcludeStem(length) then exit;
  if self.setColorsWithAmendmentAndReturnTrueIfNoOverrides(kDrawingLine) then
    turtle.setLineColor(color);
  realLength := length * self.lengthMultiplierConsideringAmendments;
  realWidth := width * self.widthMultiplierConsideringAmendments;
  // set up for export
  turtle.ifExporting_startStemSegment(self.longNameForDXFPartConsideringGenderEtc(dxfIndex),
    self.shortNameForDXFPartConsideringGenderEtc(dxfIndex), color,
    realWidth / 2.0 {for POV you want radius not diameter}, dxfIndex);
  // get number of segments
  if turtle.drawOptions.straightLinesOnly then
    lineDivisions := 1
  else
    lineDivisions := plant.pGeneral.lineDivisions;
  // figure length and turn of each segment
  realAngleX := self.rotateAngleConsideringAmendment(kRotateX, useAmendment, 0);
  realAngleY := self.rotateAngleConsideringAmendment(kRotateY, useAmendment, angleY);
  realAngleZ := self.rotateAngleConsideringAmendment(kRotateZ, useAmendment, angleZ);
  if lineDivisions > 1 then
    begin
    turnPortionZ := realAngleZ / lineDivisions;
    turnPortionY := realAngleY / lineDivisions;
    drawPortion := realLength / lineDivisions;
    end
  else
    begin
    turnPortionZ := realAngleZ;
    turnPortionY := realAngleY;
    drawPortion := realLength;
    end;
  // figure width for tapering
  startWidth := realWidth;
  if taperIndex > 0 then
    endWidth := startWidth * taperIndex / 100.0
  else
    endWidth := realWidth;
  startPortionWidth := startWidth;
  endPortionWidth := startPortionWidth;
  if realAngleX <> 0 then turtle.rotateX(realAngleX);
  for i := 0 to lineDivisions - 1 do
    begin
    isLastSegment := (i >= lineDivisions - 1);
    // because of rounding, last segment uses leftover, not equal portion
    if not isLastSegment then
      begin
      segmentTurnZ := turnPortionZ;
      segmentTurnY := turnPortionY;
      segmentLength := drawPortion;
      end
    else
      begin
      segmentTurnZ := (realAngleZ - (turnPortionZ * (lineDivisions - 1)));
      segmentTurnY := (realAngleY - (turnPortionY * (lineDivisions - 1)));
      segmentLength := (realLength - (drawPortion * (lineDivisions - 1)));
      end;
    // figure tapering for section
    if (taperIndex > 0) and (lineDivisions > 1) then  // lineDivisions part added in v1.6b3
      begin
      startPortionWidth := startWidth - (i / (lineDivisions - 1)) * (startWidth - endWidth);
      if not isLastSegment then
        endPortionWidth := startWidth - ((i+1) / (lineDivisions - 1)) * (startWidth - endWidth)
      else
        endPortionWidth := endWidth;
      end;
    // set width, rotate, draw line
    turtle.setLineWidth(startPortionWidth);
    turtle.RotateY(segmentTurnY);
    turtle.RotateZ(segmentTurnZ);
    if turtle.exportingToFile then
      self.write3DExportLine(self.partID, segmentLength, startPortionWidth, endPortionWidth, i)
    else
      begin
      triangleMade := turtle.drawInMillimeters(segmentLength, self.partID);
      if (turtle.drawOptions.sortTdosAsOneItem) and (triangleMade <> nil) then
        triangleMade.tdo := self.tdoToSortLinesWith;
      end
    end;
  turtle.ifExporting_endStemSegment;
  end;

const kMaxLineOutputPoints = 200;

procedure PdPlantPart.write3DExportLine(partID: smallint; length, startWidth, endWidth: single; segmentNumber: smallint);
  var
    turtle: KfTurtle;
    angle, pipeRadius, faceWidth: single;
    i, faces: smallint;
    startPoints, endPoints: array[0..kMaxLineOutputPoints] of KfPoint3D;
  begin
  turtle := plant.turtle;
  if turtle = nil then exit;
  // POV draws cylinders directly, not with faces
  if turtle.writingToPOV then
    begin
    turtle.drawInMillimeters(length, partID);
    exit;
    end;
  faces := turtle.ifExporting_stemCylinderFaces;
  if faces = 0 then exit;
  // get startWidth points; if done before, copy from last endWidth points
  if segmentNumber <= 0 then
    begin
    pipeRadius := 0.5 * startWidth;
    for i := 0 to faces - 1 do
      begin
      turtle.push;
      turtle.rotateX(i * 256 / faces);
      turtle.rotateZ(64);
      turtle.moveInMillimeters(pipeRadius);
      startPoints[i] := turtle.position;
      turtle.pop;
      end;
    end
  else
    for i := 0 to faces - 1 do startPoints[i] := endPoints[i];
  turtle.moveInMillimeters(length);
  // get endWidth points
  pipeRadius := 0.5 * endWidth;
  for i := 0 to faces - 1 do
    begin
    turtle.push;
    turtle.rotateX(i * 256 / faces);
    turtle.rotateZ(64);
    turtle.moveInMillimeters(pipeRadius);
    endPoints[i] := turtle.position;
    turtle.pop;
    end;
  // draw pipe faces from stored points
  turtle.drawFileExportPipeFaces(startPoints, endPoints, faces, segmentNumber);
  end;

function PdPlantPart.tdoToSortLinesWith: KfObject3D;
  begin
  // subclasses can override
  result := nil;
  end;

function PdPlantPart.partType: integer;
  begin
  { implemented by subclasses }
  result := 0;
  end;

function PdPlantPart.angleWithSway(angle: single): single;
  begin
  result := angle;
  if plant = nil then exit;
  result := angle + ((self.randomSwayIndex - 0.5) * plant.pGeneral.randomSway);
  end;

{ ---------------------------------------------------------------------------------- amendments }
procedure PdPlantPart.determineAmendmentAndAlsoForChildrenIfAny;
  begin
  amendment := plant.amendmentForPartID(partID);
  end;

function PdPlantPart.hiddenByAmendment: boolean;
  var
    iHaveAnAmendment, iDontHaveAnAmendment, myParentHasAnAmendment, myAmendmentSaysIAmHidden,
      myParentsAmendmentSaysIAmHidden, drawingToMainWindow: boolean;
  begin
  result := false;
  if not domain.options.showPosingAtAll then exit;
  if plant.turtle = nil then exit;
  iHaveAnAmendment := amendment <> nil;
  iDontHaveAnAmendment := amendment = nil;
  myParentHasAnAmendment := parentAmendment <> nil;
  myAmendmentSaysIAmHidden := (amendment <> nil) and (amendment.hide);
  myParentsAmendmentSaysIAmHidden := (parentAmendment <> nil) and (parentAmendment.hide);
  drawingToMainWindow := (plant.turtle.writingTo = kScreen) and (not domain.drawingToMakeCopyBitmap);

  if (iHaveAnAmendment and myAmendmentSaysIAmHidden) or
      (iDontHaveAnAmendment and myParentHasAnAmendment and myParentsAmendmentSaysIAmHidden) then
    if drawingToMainWindow then
      result := not domain.options.showGhostingForHiddenParts
    else
      result := true;
  end;

procedure PdPlantPart.applyAmendmentRotations;
  begin
  if (amendment <> nil) and (amendment.addRotations) and (domain.options.showPosingAtAll) then
    begin
    plant.turtle.rotateX(amendment.xRotation * 256 / 360);  
    plant.turtle.rotateY(amendment.yRotation * 256 / 360);
    plant.turtle.rotateZ(amendment.zRotation * 256 / 360);
    end;
  end;

function PdPlantPart.setColorsWithAmendmentAndReturnTrueIfNoOverrides(drawingTdo: boolean): boolean;
  var
    amendmentToUse: PdPlantDrawingAmendment;
    color, backfaceColor, lineColor: TColorRef;
    iHaveAnAmendment, iDontHaveAnAmendment, myParentHasAnAmendment, myAmendmentSaysIAmHidden,
      myParentsAmendmentSaysIAmHidden, iAmSelectedInTheMainWindow, showHighlights: boolean;
  begin
  result := true;
  if not domain.options.showPosingAtAll then exit;
  if plant.turtle = nil then exit;
  color := 0;
  backFaceColor := 0;
  lineColor := 0;
  iHaveAnAmendment := amendment <> nil;
  iDontHaveAnAmendment := amendment = nil;
  myParentHasAnAmendment := parentAmendment <> nil;
  myAmendmentSaysIAmHidden := (amendment <> nil) and (amendment.hide);
  myParentsAmendmentSaysIAmHidden := (parentAmendment <> nil) and (parentAmendment.hide);
  iAmSelectedInTheMainWindow := (self.partID = MainForm.selectedPlantPartID) and (MainForm.focusedPlant = plant);
  showHighlights := domain.options.showHighlightingForNonHiddenPosedParts
    and (plant.turtle.writingTo = kScreen) and (not domain.drawingToMakeCopyBitmap) and (not plant.drawingIntoPreviewCache);

  if iHaveAnAmendment or myParentHasAnAmendment then
    begin
    result := false;
    if (iHaveAnAmendment and iAmSelectedInTheMainWindow and showHighlights) then
      color := domain.options.selectedPosedColor
    else if (iHaveAnAmendment and myAmendmentSaysIAmHidden) or
      (iDontHaveAnAmendment and myParentHasAnAmendment and myParentsAmendmentSaysIAmHidden) then
      color := domain.options.ghostingColor
    else if (iHaveAnAmendment and showHighlights) then
      color := domain.options.nonHiddenPosedColor
    else
      result := true;
    end;

  if result = false then
    begin
    if backFaceColor = 0 then backFaceColor := color;
    if lineColor = 0 then lineColor := color;
    if drawingTdo then
      begin
      plant.turtle.setForeColorBackColor(color, backFaceColor);
      plant.turtle.setLineColor(darkerColor(color));
      end
    else
      plant.turtle.setLineColor(lineColor);
    end;
  end;

  // posed color part > if put this back, put it AFTER ghostingColor and BEFORE nonHiddenPosedColor
        (*
    else if ((amendment <> nil) and (amendment.changeColors))
        or ((parentAmendment <> nil) and (parentAmendment.changeColors) and (parentAmendment.propagateColors)) then
      begin
      // directly changed colors take precedence over highlighting
      if amendment <> nil then amendmentToUse := amendment else amendmentToUse := parentAmendment;
      color := amendmentToUse.faceColor;
      backFaceColor := amendmentToUse.backfaceColor;
      lineColor := amendmentToUse.lineColor;
      end
      *)


function PdPlantPart.rotateAngleConsideringAmendment(rotateWhat: smallint; useAmendment: boolean; angle: single): single;
  begin
  result := angle;
  if (useAmendment) and (self.amendment <> nil) and (self.amendment.addRotations)
    and (domain.options.showPosingAtAll) then
    case rotateWhat of
      kRotateX: result := angle + self.amendment.xRotation * 256 / 360;
      kRotateY: result := angle + self.amendment.yRotation * 256 / 360;
      kRotateZ: result := angle + self.amendment.zRotation * 256 / 360;
      end;
  end;

function PdPlantPart.scaleMultiplierConsideringAmendments: single;
  var amendmentToUse: PdPlantDrawingAmendment;
  begin
  result := 1.0;
  if not domain.options.showPosingAtAll then exit;
  if (amendment <> nil) or (parentAmendment <> nil) then
    if ((amendment <> nil) and (amendment.multiplyScale))
        or ((parentAmendment <> nil) and (parentAmendment.multiplyScale) and (parentAmendment.propagateScale)) then
    begin
    if amendment <> nil then amendmentToUse := amendment else amendmentToUse := parentAmendment;
    result := 1.0 * amendmentToUse.scaleMultiplier_pct / 100.0;
    end;
  end;

function PdPlantPart.lengthMultiplierConsideringAmendments: single;
  var amendmentToUse: PdPlantDrawingAmendment;
  begin
  result := 1.0;
  if not domain.options.showPosingAtAll then exit;
  if (amendment <> nil) or (parentAmendment <> nil) then
    if ((amendment <> nil) and (amendment.multiplyScale))
        or ((parentAmendment <> nil) and (parentAmendment.multiplyScale) and (parentAmendment.propagateScale)) then
    begin
    if amendment <> nil then amendmentToUse := amendment else amendmentToUse := parentAmendment;
    result := 1.0 * amendmentToUse.lengthMultiplier_pct / 100.0;
    end;
  end;

function PdPlantPart.widthMultiplierConsideringAmendments: single;
  var amendmentToUse: PdPlantDrawingAmendment;
  begin
  result := 1.0;
  if not domain.options.showPosingAtAll then exit;
  if (amendment <> nil) or (parentAmendment <> nil) then
    if ((amendment <> nil) and (amendment.multiplyScale))
        or ((parentAmendment <> nil) and (parentAmendment.multiplyScale) and (parentAmendment.propagateScale)) then
    begin
    if amendment <> nil then amendmentToUse := amendment else amendmentToUse := parentAmendment;
    result := 1.0 * amendmentToUse.widthMultiplier_pct / 100.0;
    end;
  end;

{ ---------------------------------------------------------------------------------- streaming }
procedure PdPlantPart.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdPlantPart;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

{this will stream entire the entire object -
but the included object references need to be fixed up afterwards
or the objects streamed out separately afterwards - subclasses overrides
need to call inherited to get this behavior}
procedure PdPlantPart.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  begin
  inherited streamDataWithFiler(filer, cvir);
  filer.streamSingle(liveBiomass_pctMPB);
  filer.streamSingle(deadBiomass_pctMPB);
  filer.streamSingle(biomassDemand_pctMPB);
  filer.streamSmallint(gender);
  filer.streamLongint(age);
  filer.streamBoolean(hasFallenOff);
  filer.streamBoolean(isSeedlingLeaf);
  filer.streamLongint(partID);
  filer.streamSingle(biomassOfMeAndAllPartsAboveMe_pctMPB);
  filer.streamSingle(randomSwayIndex);
  end;

procedure PdPlantPart.addDependentPartsToList(aList: TList);
  begin
  { subclasses can override }
  end;

procedure PdPlantPart.BlendColorsStrength(aColor: TColorRef; aStrength: single);
  begin
  {subclasses can override}
  end;

procedure PdPlantPart.calculateColors;
  begin
  setColorsToParameters;
  end;

function PdPlantPart.longNameForDXFPartConsideringGenderEtc(index: smallint): string;
  begin
  result := longNameForDXFPartType(self.realDxfIndexForBaseDXFPart(index));
  end;

function PdPlantPart.shortNameForDXFPartConsideringGenderEtc(index: smallint): string;
  begin
  result := shortNameForDXFPartType(self.realDxfIndexForBaseDXFPart(index));
  end;

function PdPlantPart.realDxfIndexForBaseDXFPart(index: smallint): smallint;
  begin
  result := index;
  case index of
    kExportPartLeaf: if self.isSeedlingLeaf then result := kExportPartSeedlingLeaf;
    kExportPartPetiole: if self.isSeedlingLeaf then result := kExportPartFirstPetiole;
    kExportPartInflorescenceStalkFemale: if self.gender = kGenderMale then result := kExportPartInflorescenceStalkMale;
    kExportPartInflorescenceInternodeFemale: if self.gender = kGenderMale then result := kExportPartInflorescenceInternodeMale;
    kExportPartInflorescenceBractFemale: if self.gender = kGenderMale then result := kExportPartInflorescenceBractMale;
    kExportPartPedicelFemale: if self.gender = kGenderMale then result := kExportPartPedicelMale;
    kExportPartFlowerBudFemale: if self.gender = kGenderMale then result := kExportPartFlowerBudMale;
    kExportPartFilamentFemale: if self.gender = kGenderMale then result := kExportPartFilamentMale;
    kExportPartAntherFemale: if self.gender = kGenderMale then result := kExportPartAntherMale;
    kExportPartFirstPetalsFemale: if self.gender = kGenderMale then result := kExportPartFirstPetalsMale;
    kExportPartSepalsFemale: if self.gender = kGenderMale then result := kExportPartSepalsMale;
    end;
  end;

end.
