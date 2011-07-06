unit U3dexport;

interface   

uses Windows, Graphics, SysUtils, Classes,
  usupport, utdo, udrawingsurface, u3dsupport;

const

  // export part types
  // meristem
  kExportPartMeristem = 0;
  // internode
  kExportPartInternode = 1;
  // leaf
  kExportPartSeedlingLeaf = 2;
  kExportPartLeaf = 3;
  kExportPartFirstPetiole = 4;
  kExportPartPetiole = 5;
  kExportPartLeafStipule = 6;  // no stipule on first leaves
  // inflorescence female
  kExportPartInflorescenceStalkFemale = 7;
  kExportPartInflorescenceInternodeFemale = 8;
  kExportPartInflorescenceBractFemale = 9;
  // inflorescence male
  kExportPartInflorescenceStalkMale = 10;
  kExportPartInflorescenceInternodeMale = 11;
  kExportPartInflorescenceBractMale = 12;
  // flower female
  kExportPartPedicelFemale = 13;
  kExportPartFlowerBudFemale = 14;
  kExportPartStyleFemale = 15;
  kExportPartStigmaFemale = 16;
  kExportPartFilamentFemale = 17;
  kExportPartAntherFemale = 18;
  kExportPartFirstPetalsFemale = 19;
  kExportPartSecondPetalsFemale = 20;
  kExportPartThirdPetalsFemale = 21;
  kExportPartFourthPetalsFemale = 22;
  kExportPartFifthPetalsFemale = 23;
  kExportPartSepalsFemale = 24;
  // flower male
  kExportPartPedicelMale = 25;
  kExportPartFlowerBudMale = 26;
  kExportPartFilamentMale = 27;
  kExportPartAntherMale = 28;
  kExportPartFirstPetalsMale = 29;
  kExportPartSepalsMale = 30;
  // fruit
  kExportPartUnripeFruit = 31;
  kExportPartRipeFruit = 32;
  // root top
  kExportPartRootTop = 33;

    kExportPartLast = 33;

  // DXF
  kLastDxfColorIndex = 10;
  dxfColors: array[0..kLastDxfColorIndex] of TColorRef = (clRed, clYellow, clLime, clAqua, clBlue, clPurple, clBlack,
    clOlive, clFuchsia, clTeal, clGray);
  kColorDXFFromPlantPartType = 0; kColorDXFFromRGB = 1; kColorDXFFromOneColor = 3;

  // POV
  kNestingTypeInflorescence = 0;
  kNestingTypeLeafAndPetiole = 1;
  kNestingTypeCompoundLeaf = 2;
  kNestingTypePedicelAndFlowerFruit = 3;
  kNestingTypeFloralLayers = 4;
  kMaxPOVPlants = 1000;  // can't imagine anyone would save more than that

  // 3DS

  // OBJ, LWO
  kMaxStoredMaterials = 1000;

  // VRML
  kVRMLVersionOne = 0; kVRMLVersionTwo = 1;

  // general
  kScreen = 0; kDXF = 1; kPOV = 2; k3DS = 3; kOBJ = 4; kVRML = 5; kLWO = 6; k3DExportTypeLast = 6;

  kLayerOutputAllTogether = 0; kLayerOutputByTypeOfPlantPart = 1; kLayerOutputByPlantPart = 2;
  kWriteColor = true; kDontWriteColor = false;
  kMax3DPoints = 65536; kMax3DFaces = 65536;
  kX = 0; kY = 1; kZ = 2;

type

  Vertex = record
    x: Real;
    y: Real;
    z: Real;
    end;

  Triangle = record
    vertex1: integer;
    vertex2: integer;
    vertex3: integer;
    surfaceID: integer;
    end;

  FileExport3DOptionsStructure = record
    // generic
    exportType: smallint;
    layeringOption: smallint;
    stemCylinderFaces: smallint;
    translatePlantsToWindowPositions: boolean;
    lengthOfShortName: smallint;
    writePlantNumberInFrontOfName: boolean;
    writeColors: boolean;
    overallScalingFactor_pct: smallint;
    fileSize: single; // don't save in settings file
    xRotationBeforeDraw: smallint; // to deal with quirks in other programs
    pressPlants: boolean;
    directionToPressPlants: smallint;
    makeTrianglesDoubleSided: boolean;
    // specific (keep in generic structure so one window can handle all of these)
    dxf_whereToGetColors: smallint;
    dxf_wholePlantColorIndex: smallint;
    dxf_plantPartColorIndexes: array[0..kExportPartLast] of smallint;
    pov_minLineLengthToWrite: single;
    pov_minTdoScaleToWrite: single;
    pov_commentOutUnionAtEnd: boolean;
    nest_Inflorescence: boolean;
    nest_LeafAndPetiole: boolean;
    nest_CompoundLeaf: boolean;
    nest_PedicelAndFlowerFruit: boolean;
    nest_FloralLayers: boolean;
    vrml_version: smallint;
    end;

  KfFileExportSurface = class(KfDrawingSurface)
    public
    fileName: string;
    scale: single;
    options: FileExport3DOptionsStructure;
    currentPlantNameLong, currentPlantNameShort: string;
    currentPlantIsTranslated: boolean;
    currentPlantTranslateX, currentPlantTranslateY: single;
    currentPlantIndex: smallint;
    currentGroupingString: string;
    currentColor: TColorRef;
    plantPartCounts: array[0..kExportPartLast] of smallint;
    numPoints: integer;
    points: array [0..kMax3DPoints] of Vertex;
    numFaces: integer;
    faces: array [0..kMax3DFaces] of Triangle;
    constructor createWithFileName(aFileName: string); virtual;
    destructor destroy; override;
    procedure startFile; virtual;
    procedure endFile; virtual;
    procedure startPlant(aLongName: string; aPlantIndex: smallint); virtual;
    procedure endPlant; virtual;
    procedure writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D); virtual;
    procedure startNestedGroupOfPlantParts(groupName: string; shortName: string; nestingType: smallint); virtual;
    procedure endNestedGroupOfPlantParts(nestingType: smallint); virtual;
    procedure startPlantPart(aLongName, aShortName: string); virtual;
    procedure endPlantPart; virtual;
    procedure startStemSegment(aLongName: string; aShortName: string;
        color: TColorRef; width: single; index: smallint); virtual;
    procedure endStemSegment; virtual;
    procedure start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint); virtual;
    procedure end3DObject; virtual;
    procedure startVerticesAndTriangles; virtual;
    procedure endVerticesAndTriangles; virtual;
    procedure addPoint(point: KfPoint3D); virtual;
    procedure addTriangle(a, b, c: integer); virtual;
    function pressedOrNot(value: single; dimension: smallint): single;
    procedure setTranslationForCurrentPlant(isTranslated: boolean; aTranslateX: single; aTranslateY: single);
    procedure drawPipeFaces(const startPoints: array of KfPoint3D;
        const endPoints: array of KfPoint3D; faces: smallint; segmentNumber: smallint); virtual;
    function outputType: smallint;
    function generateShortName: string;
    procedure setUpGroupingStringForStemSegmentOr3DObject(aShortName: string; index: smallint);
    end;

  KfTextFileExportSurface = class(KfFileExportSurface)
    public
    outputFile: TextFile;
    constructor createWithFileName(aFileName: string); override;
    destructor destroy; override;
    procedure startFile; override;
    procedure endFile; override;
    end;

  KfDrawingSurfaceForDXF = class(KfTextFileExportSurface)
    public
    currentColorIndex: smallint;
    procedure startFile; override;
    procedure endFile; override;
    procedure startPlant(aLongName: string; aPlantIndex: smallint); override;
    procedure drawPipeFaces(const startPoints: array of KfPoint3D;
        const endPoints: array of KfPoint3D; faces: smallint; segmentNumber: smallint); override;
    procedure draw3DFace(point1, point2, point3, point4: KfPoint3D); override;
    procedure startStemSegment(aLongName: string; aShortName: string;
        color: TColorRef; width: single; index: smallint); override;
    procedure start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint); override;
		procedure basicDrawLineFromTo(const startPoint: KfPoint3D; const endPoint: KfPoint3D); override;
		procedure basicDrawTriangle(triangle: KfTriangle); override;
    procedure writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D); override;
    end;

  KfDrawingSurfaceForPOV = class(KfTextFileExportSurface)
    public
    currentComment: string;
    currentWidth: single;
    currentIndentLevel: integer;
    currentRotateString: string;
    numPlantsDrawn: smallint;
    plantNames: array[0..kMaxPOVPlants] of string;
    procedure startFile; override;
    procedure endFile; override;
    procedure startPlant(aLongName: string; aPlantIndex: smallint); override;
    procedure endPlant; override;
    procedure startNestedGroupOfPlantParts(groupName: string; shortName: string; nestingType: smallint); override;
    procedure endNestedGroupOfPlantParts(nestingType: smallint); override;
    procedure startPlantPart(aLongName, aShortName: string); override;
    procedure endPlantPart; override;
    procedure startStemSegment(aLongName: string; aShortName: string;
        color: TColorRef; width: single; index: smallint); override;
    procedure endStemSegment; override;
    procedure start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint); override;
    procedure end3DObject; override;
		procedure basicDrawLineFromTo(const startPoint: KfPoint3D; const endPoint: KfPoint3D); override;
		procedure basicDrawTriangle(triangle: KfTriangle); override;
    procedure startUnionOrMesh(startString: string; aColor: TColorRef; aComment: string);
    procedure writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D); override;
    procedure startUnion(aComment: string);
    procedure startMesh(aColor: TColorRef; aComment: string);
    procedure setColor(aColor: TColorRef);
    procedure endBrace(writeColor: boolean);
    procedure indent;
    procedure unindent;
    procedure doIndenting;
    end;

  KfDrawingSurfaceForVRML = class(KfTextFileExportSurface)
    public
    currentIndentLevel: integer;
    lastPlantPartName, lastMeshName: string;
    procedure startFile; override;
    procedure startPlant(aLongName: string; aPlantIndex: smallint); override;
    procedure endPlant; override;
    procedure startNestedGroupOfPlantParts(groupName: string; shortName: string; nestingType: smallint); override;
    procedure endNestedGroupOfPlantParts(nestingType: smallint); override;
    procedure startPlantPart(aLongName, aShortName: string); override;
    procedure endPlantPart; override;
    procedure startStemSegment(aLongName: string; aShortName: string;
        color: TColorRef; width: single; index: smallint); override;
    procedure endStemSegment; override;
    procedure start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint); override;
    procedure end3DObject; override;
    procedure startMesh;
    procedure endMesh;
    procedure writePointsAndTriangles;
    procedure writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D); override;
    procedure setColor(aColor: TColorRef);
    procedure endBrace(comment: string);
    procedure endBracket(comment: string);
    procedure indent;
    procedure unindent;
    procedure doIndenting;
    procedure writeConsideringIndenting(aString: string);
    procedure indentThenWrite(aString: string);
    procedure writeThenIndent(aString: string);
    end;

  KfDrawingSurfaceForOBJ = class(KfTextFileExportSurface)
    public
    numMaterialsStored: smallint;
    materialColors: array[0..kMaxStoredMaterials] of TColorRef;
    materialNames: array[0..kMaxStoredMaterials] of string;
    materialsFileName: string;
    procedure startFile; override;
    procedure endFile; override;
    procedure startPlant(aLongName: string; aPlantIndex: smallint); override;
    procedure startStemSegment(aLongName: string; aShortName: string;
        color: TColorRef; width: single; index: smallint); override;
    procedure endStemSegment; override;
    procedure start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint); override;
    procedure endVerticesAndTriangles; override;
    procedure writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D); override;
    procedure writeMaterialDescriptionsToFile;
    procedure storeMaterialDescription(aName: string; aColor: TColorRef);
    procedure startGroup(aName: string);
    procedure startColor(aColor: TColorRef; aMaterialName: string);
    end;

  KfBinaryFileExportSurface = class(KfFileExportSurface)
    public
    stream: TFileStream;
    chunkStartStack: TList;
    constructor createWithFileName(aFileName: string); override;
    destructor destroy; override;
    procedure startFile; override;
    procedure endFile; override;
    function isLittleEndian: boolean; virtual;
    procedure writeStringZ(value: string);
    procedure writeByte(value: byte);
    procedure writeWord(value: word);
    procedure writeDword(value: longint);
    procedure writeFloat(value: Single);
    end;

  KfDrawingSurfaceFor3DS = class(KfBinaryFileExportSurface)
    public
    currentMaterialName: string;
    constructor createWithFileName(aFileName: string); override;
    destructor destroy; override;
    procedure startFile; override;
    procedure endFile; override;
    procedure startStemSegment(aLongName: string; aShortName: string;
        color: TColorRef; width: single; index: smallint); override;
    procedure endStemSegment; override;
    procedure start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint); override;
    procedure startVerticesAndTriangles; override;
    procedure endVerticesAndTriangles; override;
    procedure writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D); override;
    procedure writeMaterialDescription(index: smallint; aColor: TColorRef);
    procedure pushChunkStart;
    procedure popChunkStartAndFixupChunkSize;
    procedure startChunk(chunkID: integer);
    procedure finishChunk(chunkType: integer);
    procedure startMeshObject(name: string);
    procedure finishMeshObject;
    procedure writeColorChunk(r: byte; g: byte; b: byte);
    procedure writeMaterialColorChunk(materialName: string; r, g, b: byte);
    end;

  KfDrawingSurfaceForLWO = class(KfBinaryFileExportSurface)
    public
    currentSurfaceID: smallint;
    numSurfacesStored: smallint;
    surfaceColors: array[1..kMaxStoredMaterials] of TColorRef;
    surfaceNames: array[1..kMaxStoredMaterials] of string[80];
    procedure endFile; override;
    function isLittleEndian: boolean; override;
    procedure writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D); override;
    procedure startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
        index: smallint); override;
    function lookUpSurfaceIDForName(aName: string; color: TColorRef): smallint;
    procedure drawPipeFaces(const startPoints: array of KfPoint3D;
        const endPoints: array of KfPoint3D; faces: smallint; segmentNumber: smallint); override;
    procedure start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint); override;
    procedure addTriangle(a, b, c: integer); override;
    procedure addTriangleWithSurface(a, b, c, surfaceID: integer);
    procedure pushChunkStart;
    procedure popChunkStartAndFixupChunkSize;
    procedure startChunk(chunkName: string);
    procedure finishChunk;
    procedure writeTagOfFourCharacters(aString: string);
    end;

function fileTypeFor3DExportType(outputType: smallint): smallint;
function nameFor3DExportType(anOutputType: smallint): string;
function longNameForDXFPartType(index: smallint): string;
function shortNameForDXFPartType(index: smallint): string;
procedure getInfoForDXFPartType(index: smallint; var longName: string; var shortName: string);

implementation

uses udomain, umath;

{ ----------------------------------------------------------------------------- KfFileExportSurface }
constructor KfFileExportSurface.createWithFileName(aFileName: string);
  begin
  inherited create;
  fileName := aFileName;
  options := domain.exportOptionsFor3D[outputType];
  scale := options.overallScalingFactor_pct / 100.0;
  end;

destructor KfFileExportSurface.destroy;
  begin
  // nothing yet
  end;

procedure KfFileExportSurface.startFile;
  begin
  raise Exception.create('subclasses must override');
  end;

procedure KfFileExportSurface.endFile;
  begin
  raise exception.create('subclasses must override');
  end;

procedure KfFileExportSurface.startPlant(aLongName: string; aPlantIndex: smallint);
  begin
  currentPlantIndex := aPlantIndex;
  currentPlantNameLong := aLongName;
  currentPlantNameShort := self.generateShortName;
  end;

procedure KfFileExportSurface.endPlant;
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D);
  begin
  raise Exception.create('subclasses must override');
  end;

procedure KfFileExportSurface.startNestedGroupOfPlantParts(groupName: string; shortName: string; nestingType: smallint);
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.endNestedGroupOfPlantParts(nestingType: smallint);
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.startPlantPart(aLongName, aShortName: string);
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.endPlantPart;
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
    index: smallint);
  begin
  self.setUpGroupingStringForStemSegmentOr3DObject(aShortName, index);
  end;

procedure KfFileExportSurface.start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
  begin
  self.setUpGroupingStringForStemSegmentOr3DObject(aShortName, index);
  end;

procedure KfFileExportSurface.startVerticesAndTriangles;
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.endVerticesAndTriangles;
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.addPoint(point: KfPoint3D);
  begin
  if numPoints >= kMax3DPoints then
      raise Exception.Create('Problem: Too many points in 3D export.');
  points[numPoints].x := pressedOrNot(scale * point.x, kX);
  points[numPoints].y := pressedOrNot(scale * point.y, kY);
  points[numPoints].z := pressedOrNot(scale * point.z, kZ);
  inc(numPoints);
  end;

function KfFileExportSurface.pressedOrNot(value: single; dimension: smallint): single;
  begin
  if (options.pressPlants) and (options.directionToPressPlants = dimension) then
    result := 0
  else
    result := value;
  end;

procedure KfFileExportSurface.addTriangle(a, b, c: integer);
  begin
  if numFaces >= kMax3DFaces then
      raise Exception.Create('Problem: Too many faces in 3D export.');
  faces[numFaces].vertex1 := a;
  faces[numFaces].vertex2 := b;
  faces[numFaces].vertex3 := c;
  inc(numFaces);
  end;

procedure KfFileExportSurface.end3DObject;
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.setUpGroupingStringForStemSegmentOr3DObject(aShortName: string; index: smallint);
  begin
  case options.layeringOption of
    kLayerOutputAllTogether:
      begin
      currentGroupingString := currentPlantNameShort;
      end;
    kLayerOutputByTypeOfPlantPart:
      begin
      currentGroupingString := currentPlantNameShort + '_' + aShortName;
      end;
    kLayerOutputByPlantPart:
      begin
      inc(plantPartCounts[index]);
      currentGroupingString := currentPlantNameShort + '_' + intToStr(plantPartCounts[index]) + '_' + aShortName;
      end;
    end;
  end;
  
procedure KfFileExportSurface.endStemSegment;
  begin
  // subclasses can override
  end;

procedure KfFileExportSurface.drawPipeFaces(const startPoints: array of KfPoint3D;
    const endPoints: array of KfPoint3D; faces: smallint; segmentNumber: smallint);
  var i, disp: longint;
  begin
  // subclasses can override - this works for some
  disp := segmentNumber * faces * 2;
  for i := 0 to faces - 1 do addPoint(startPoints[i]);
  for i := 0 to faces - 1 do addPoint(endPoints[i]);
  for i := 0 to faces - 1 do
    begin
    addTriangle(disp + i, disp + i + faces, disp + (i+1) mod faces);
    addTriangle(disp + (i+1) mod faces, disp + i + faces, disp + (i+1) mod faces + faces);
    end;
  end;

procedure KfFileExportSurface.setTranslationForCurrentPlant(isTranslated: boolean; aTranslateX: single; aTranslateY: single);
  begin
  currentPlantIsTranslated := isTranslated;
  currentPlantTranslateX := aTranslateX;
  currentPlantTranslateY := aTranslateY;
  end;

function KfFileExportSurface.outputType: smallint;
  begin
  result := -1;
  if (self is KfDrawingSurfaceForDXF) then
    result := kDXF
  else if (self is KfDrawingSurfaceForPOV) then
    result := kPOV
  else if (self is KfDrawingSurfaceFor3DS) then
    result := k3DS
  else if (self is KfDrawingSurfaceForOBJ) then
    result := kOBJ
  else if (self is KfDrawingSurfaceForVRML) then
    result := kVRML
  else if (self is KfDrawingSurfaceForLWO) then
    result := kLWO;
  end;

function KfFileExportSurface.generateShortName: string;
  var
    shortNameLength, i: integer;
  begin
  result := '';
  if length(currentPlantNameLong) <= 0 then exit;
  shortNameLength := intMin(options.lengthOfShortName, length(currentPlantNameLong));
  for i := 1 to shortNameLength do
    if currentPlantNameLong[i] <> ' ' then
      result := result + copy(currentPlantNameLong, i, 1);
  if options.writePlantNumberInFrontOfName then
    result := intToStr(currentPlantIndex + 1) + result; 
  end;

{ ----------------------------------------------------------------------------- KfTextFileExportSurface }
constructor KfTextFileExportSurface.createWithFileName(aFileName: string);
  begin
  inherited createWithFileName(aFileName);
  // we assume that the file name has been already okayed by whoever created us
  assignFile(outputFile, fileName);
  end;

destructor KfTextFileExportSurface.destroy;
  begin
  // nothing yet
  end;

procedure KfTextFileExportSurface.startFile;
  begin
  rewrite(outputFile);
  end;

procedure KfTextFileExportSurface.endFile;
  begin
  closeFile(outputFile);
  end;

{ ----------------------------------------------------------------------------- KfDrawingSurfaceForDXF }
procedure KfDrawingSurfaceForDXF.startFile;
  begin
  inherited startFile;
  writeln(outputFile, '999');
  writeln(outputFile, 'DXF created by PlantStudio http://www.kurtz-fernhout.com');
  // v2.0 moved ENTITY section from starting and ending each plant to entire file - may fix bug
  // with programs only recognizing one plant in a file
  writeln(outputFile, '0'); writeln(outputFile, 'SECTION');
  writeln(outputFile, '2'); writeln(outputFile, 'ENTITIES');
  end;

procedure KfDrawingSurfaceForDXF.endFile;
  begin
  // v2.0 moved ENTITY section from starting and ending each plant to entire file - may fix bug
  // with programs only recognizing one plant in a file
  writeln(outputFile, '0');
  writeln(outputFile, 'ENDSEC');
  writeln(outputFile, '0');
  writeln(outputFile, 'EOF');
  inherited endFile;
  end;

procedure KfDrawingSurfaceForDXF.startPlant(aLongName: string; aPlantIndex: smallint);
  begin
  inherited startPlant(aLongName, aPlantIndex);
  if options.layeringOption = kLayerOutputAllTogether then
    currentGroupingString := copy(currentPlantNameLong, 1, 16);
  if options.dxf_whereToGetColors = kColorDXFFromOneColor then
    currentColorIndex := options.dxf_wholePlantColorIndex;
  end;

procedure KfDrawingSurfaceForDXF.startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
    index: smallint);
  begin
  inherited startStemSegment(aLongName, aShortName, color, width, index);
  if options.dxf_whereToGetColors = kColorDXFFromPlantPartType then
    currentColorIndex := options.dxf_plantPartColorIndexes[index]
  else if options.dxf_whereToGetColors = kColorDXFFromRGB then
    currentColor := color;
  end;

procedure KfDrawingSurfaceForDXF.start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
  begin
  inherited start3DObject(aLongName, aShortName, color, index);
  if options.dxf_whereToGetColors = kColorDXFFromPlantPartType then
    currentColorIndex := options.dxf_plantPartColorIndexes[index]
  else if options.dxf_whereToGetColors = kColorDXFFromRGB then
    currentColor := color;
  end;

procedure KfDrawingSurfaceForDXF.drawPipeFaces(const startPoints: array of KfPoint3D;
    const endPoints: array of KfPoint3D; faces: smallint; segmentNumber: smallint);
  var i: smallint;
  begin
  // for this don't have to worry about segment number, we are not adding points and triangles
  for i := 0 to faces - 1 do
    self.draw3DFace(startPoints[i], endPoints[i], endPoints[(i+1) mod faces], startPoints[(i+1) mod faces]);
  end;

procedure KfDrawingSurfaceForDXF.draw3DFace(point1, point2, point3, point4: KfPoint3D);
  begin
  writeln(outputFile, '0');  writeln(outputFile, '3DFACE');
  writeln(outputFile, '8');  writeln(outputFile, self.currentGroupingString);
  if options.writeColors then
    begin
    if options.dxf_whereToGetColors = kColorDXFFromRGB then
      begin
      writeln(outputFile, '62');
      writeln(outputFile, intToStr(self.currentColor));
      end
    else
      begin
      writeln(outputFile, '62');
      writeln(outputFile, intToStr(self.currentColorIndex + 1));
      end;
    end;
  writeln(outputFile, '10'); writeln(outputFile, valueString(pressedOrNot(scale * point1.x, kX)));
  writeln(outputFile, '20'); writeln(outputFile, valueString(pressedOrNot(scale * -point1.y, kY)));
  writeln(outputFile, '30'); writeln(outputFile, valueString(pressedOrNot(scale * point1.z, kZ)));
  writeln(outputFile, '11'); writeln(outputFile, valueString(pressedOrNot(scale * point2.x, kX)));
  writeln(outputFile, '21'); writeln(outputFile, valueString(pressedOrNot(scale * -point2.y, kY)));
  writeln(outputFile, '31'); writeln(outputFile, valueString(pressedOrNot(scale * point2.z, kZ)));
  writeln(outputFile, '12'); writeln(outputFile, valueString(pressedOrNot(scale * point3.x, kX)));
  writeln(outputFile, '22'); writeln(outputFile, valueString(pressedOrNot(scale * -point3.y, kY)));
  writeln(outputFile, '32'); writeln(outputFile, valueString(pressedOrNot(scale * point3.z, kZ)));
  writeln(outputFile, '13'); writeln(outputFile, valueString(pressedOrNot(scale * point4.x, kX)));
  writeln(outputFile, '23'); writeln(outputFile, valueString(pressedOrNot(scale * -point4.y, kY)));
  writeln(outputFile, '33'); writeln(outputFile, valueString(pressedOrNot(scale * point4.z, kZ)));
  end;

procedure KfDrawingSurfaceForDXF.basicDrawLineFromTo(const startPoint: KfPoint3D; const endPoint: KfPoint3D);
  begin
  self.draw3DFace(startPoint, startPoint, endPoint, endPoint);
  end;

procedure KfDrawingSurfaceForDXF.basicDrawTriangle(triangle: KfTriangle);
  begin
  self.draw3DFace(triangle.points[0], triangle.points[1], triangle.points[2], triangle.points[2]);
  end;

procedure KfDrawingSurfaceForDXF.writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D);
  begin
  self.currentGroupingString := currentPlantNameShort + '_rem';
  self.currentColorIndex := kLastDxfColorIndex - 1; // adds one; kLastDxfColorIndex is gray
  self.draw3DFace(p1, p2, p3, p3);
  self.draw3DFace(p1, p3, p4, p4);
  end;

{ ----------------------------------------------------------------------------- KfDrawingSurfaceForPOV }
procedure KfDrawingSurfaceForPOV.startFile;
  begin
  inherited startFile;
  writeln(outputFile, '// INC file for Persistence of Vision (POV) raytracer');
  writeln(outputFile, '// created by PlantStudio http://www.kurtz-fernhout.com');
  writeln(outputFile);
  end;

procedure KfDrawingSurfaceForPOV.endFile;
  var i: smallint;
  begin
  writeln(outputFile);
  if options.pov_commentOutUnionAtEnd then writeln(outputFile, '/* ');
  writeln(outputFile, '#declare allPlants_'
      + replacePunctuationWithUnderscores(stringUpTo(extractFileName(fileName), '.'))
      + ' = union {');
  for i := 0 to numPlantsDrawn - 1 do writeln(outputFile, chr(9) + 'object { ' + plantNames[i] + ' }');
  writeln(outputFile, chr(9) + '}');
  if options.pov_commentOutUnionAtEnd then writeln(outputFile, '*/ ');
  inherited endFile;
  end;

procedure KfDrawingSurfaceForPOV.startPlant(aLongName: string; aPlantIndex: smallint);
  begin
  aLongName := replacePunctuationWithUnderscores(aLongName); // in POV you can't have spaces in names
  inherited startPlant(aLongName, aPlantIndex);
  writeln(outputFile, '#declare ' + currentPlantNameLong + ' = union {');
  currentIndentLevel := 0;
  self.indent;
  plantNames[numPlantsDrawn] := currentPlantNameLong;
  inc(numPlantsDrawn);
  end;

procedure KfDrawingSurfaceForPOV.endPlant;
  begin
  if (currentPlantIsTranslated) and (options.translatePlantsToWindowPositions) then
    writeln(outputFile, 'translate <' + valueString(currentPlantTranslateX) + ', '
      + valueString(currentPlantTranslateY) + ', 0>');
  if not options.writeColors then
    write(outputFile, 'pigment { color rgb <0.8, 0.8, 0.8> }');
  writeln(outputFile, '} // end ' + currentPlantNameLong);
  writeln(outputFile);
  currentIndentLevel := 0;
  inherited endPlant;
  end;

procedure KfDrawingSurfaceForPOV.startNestedGroupOfPlantParts(groupName: string; shortName: string; nestingType: smallint);
  begin
  case nestingType of
    kNestingTypeInflorescence: if not options.nest_Inflorescence then exit;
    kNestingTypeLeafAndPetiole: if not options.nest_LeafAndPetiole then exit;
    kNestingTypeCompoundLeaf: if not options.nest_CompoundLeaf then exit;
    kNestingTypePedicelAndFlowerFruit: if not options.nest_PedicelAndFlowerFruit then exit;
    kNestingTypeFloralLayers: if not options.nest_FloralLayers then exit;
    else
      raise Exception.create('Problem: Unrecognized nesting type in KfDrawingSurfaceForPOV.startNestedGroupOfPlantParts.');
    end;
  self.startUnion(groupName);
  end;

procedure KfDrawingSurfaceForPOV.endNestedGroupOfPlantParts(nestingType: smallint);
  begin
  case nestingType of
    kNestingTypeInflorescence: if not options.nest_Inflorescence then exit;
    kNestingTypeLeafAndPetiole: if not options.nest_LeafAndPetiole then exit;
    kNestingTypeCompoundLeaf: if not options.nest_CompoundLeaf then exit;
    kNestingTypePedicelAndFlowerFruit: if not options.nest_PedicelAndFlowerFruit then exit;
    kNestingTypeFloralLayers: if not options.nest_FloralLayers then exit;
    else
      raise Exception.create('Problem: Unrecognized nesting type in KfDrawingSurfaceForPOV.startNestedGroupOfPlantParts.');
    end;
  self.endBrace(kDontWriteColor);
  end;

procedure KfDrawingSurfaceForPOV.startPlantPart(aLongName, aShortName: string);
  begin
  self.startUnion(aLongName);
  end;

procedure KfDrawingSurfaceForPOV.endPlantPart;
  begin
  self.endBrace(kDontWriteColor);
  end;

procedure KfDrawingSurfaceForPOV.startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
    index: smallint);
  begin
  inherited startStemSegment(aLongName, aShortName, color, width, index);
  startUnion(aLongName);
  setColor(color);
  currentWidth := width;
  end;

procedure KfDrawingSurfaceForPOV.endStemSegment;
  begin
  self.endBrace(kWriteColor);  // DO want to write color for this one
  end;

procedure KfDrawingSurfaceForPOV.start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
  begin
  inherited start3DObject(aLongName, aShortName, color, index);
  startMesh(color, aLongName);
  setColor(color);
  end;

procedure KfDrawingSurfaceForPOV.end3DObject;
  begin
  self.endBrace(kWriteColor);  // DO want to write color for this one
  end;

procedure KfDrawingSurfaceForPOV.indent;
  begin
  inc(currentIndentLevel);
  end;

procedure KfDrawingSurfaceForPOV.unindent;
  begin
  dec(currentIndentLevel);
  if currentIndentLevel < 0 then currentIndentLevel := 0;
  end;

procedure KfDrawingSurfaceForPOV.doIndenting;
  var i: integer;
  begin
  for i := 1 to currentIndentLevel do write(outputFile, chr(9));
  end;

procedure KfDrawingSurfaceForPOV.startUnionOrMesh(startString: string; aColor: TColorRef; aComment: string);
  begin
  if aColor >= 0 then self.currentColor := aColor;
  self.doIndenting;
  write(outputFile, startString + ' {');
  if length(aComment) > 0 then
    writeln(outputFile, ' // ' + aComment)
  else
    writeln(outputFile, ' // ' + currentComment);
  self.indent;
  end;

procedure KfDrawingSurfaceForPOV.startUnion(aComment: string);
  begin
  self.startUnionOrMesh('union', -1, aComment);
  end;

procedure KfDrawingSurfaceForPOV.startMesh(aColor: TColorRef; aComment: string);
  begin
  self.startUnionOrMesh('mesh', aColor, aComment);
  end;

procedure KfDrawingSurfaceForPOV.setColor(aColor: TColorRef);
  begin
  self.currentColor := aColor;
  end;

procedure KfDrawingSurfaceForPOV.endBrace(writeColor: boolean);
  begin
  self.doIndenting;
  if (writeColor) and (options.writeColors) and (currentColor >= 0) then
    write(outputFile, 'pigment { color rgb <'
        + valueString(getRValue(currentColor) / 256.0) + ', '
        + valueString(getGValue(currentColor) / 256.0) + ', '
        + valueString(getBValue(currentColor) / 256.0) + '> }');
  writeln(outputFile, '}');
  self.unindent;
  end;

procedure KfDrawingSurfaceForPOV.basicDrawLineFromTo(const startPoint: KfPoint3D; const endPoint: KfPoint3D);
  var endPointFinal: KfPoint3D;
  begin
  endPointFinal := endPoint;
  self.doIndenting;
  write(outputFile, 'cylinder { ');
  writeln(outputFile,
    '<' + valueString((pressedOrNot(scale * startPoint.x, kX))) + ', '
    + valueString(pressedOrNot(scale * -startPoint.y, kY)) + ', '
    + valueString(pressedOrNot(scale * startPoint.z, kZ)) + '>, <'
    + valueString(pressedOrNot(scale * endPointFinal.x, kX)) + ', '
    + valueString(pressedOrNot(scale * -endPointFinal.y, kY)) + ', '
    + valueString(pressedOrNot(scale * endPointFinal.z, kZ))
    + '>, ' + valueString(scale * currentWidth) + ' }');
  end;

procedure KfDrawingSurfaceForPOV.basicDrawTriangle(triangle: KfTriangle);
  var
    p1, p2, p3: KfPoint3D;
  begin
  p1 := triangle.points[0];
  p2 := triangle.points[1];
  p3 := triangle.points[2];
  self.doIndenting;
  write(outputFile, 'triangle { <');
  // all y values must be negative because it seems our coordinate systems are different
  write(outputFile,
      valueString(pressedOrNot(scale * p1.x, kX)) + ', '
      + valueString(pressedOrNot(scale * -p1.y, kY)) + ', '
      + valueString(pressedOrNot(scale * p1.z, kZ)) + '>, <');
  write(outputFile,
      valueString(pressedOrNot(scale * p2.x, kX)) + ', '
      + valueString(pressedOrNot(scale * -p2.y, kY)) + ', '
      + valueString(pressedOrNot(scale * p2.z, kZ)) + '>, <');
  writeln(outputFile,
      valueString(pressedOrNot(scale * p3.x, kX)) + ', '
      + valueString(pressedOrNot(scale * -p3.y, kY)) + ', '
      + valueString(pressedOrNot(scale * p3.z, kZ)) + '> }');
  end;

procedure KfDrawingSurfaceForPOV.writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D);
  var triangle1, triangle2: KfTriangle;
  begin
  startMesh(rgb(100, 100, 100), currentPlantNameShort + '_reminder');
  triangle1 := KfTriangle.create;
  triangle2 := Kftriangle.create;
  try
    triangle1.points[0] := p1; triangle1.points[1] := p2; triangle1.points[2] := p3;
    self.basicDrawTriangle(triangle1);
    triangle2.points[0] := p1; triangle2.points[1] := p3; triangle2.points[2] := p4;
    self.basicDrawTriangle(triangle2);
  finally
    triangle1.free;
    triangle2.free;
  end;
  endBrace(kWriteColor);
  end;

{ ----------------------------------------------------------------------------- KfDrawingSurfaceForVRML }

procedure KfDrawingSurfaceForVRML.startFile;
  var scaleString: string;
  begin
  inherited startFile;
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      writeln(outputFile, '#VRML V1.0 ascii');
      writeln(outputFile, '#Created by PlantStudio http://www.kurtz-fernhout.com');
      writeln(outputFile);
      end;
    kVRMLVersionTwo:
      begin
      writeln(outputFile, '#VRML V2.0 utf8');
      writeln(outputFile, '#Created by PlantStudio http://www.kurtz-fernhout.com');
      writeln(outputFile);
      end;
    end;
  end;

procedure KfDrawingSurfaceForVRML.startPlant(aLongName: string; aPlantIndex: smallint);
  begin
  aLongName := replacePunctuationWithUnderscores(aLongName); // in VRML you can't have spaces in names
  inherited startPlant(aLongName, aPlantIndex);
  currentIndentLevel := 0;
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      self.writeThenIndent('DEF ' + currentPlantNameShort + ' Group {');
      end;
    kVRMLVersionTwo:
      begin
      self.writeThenIndent('DEF ' + currentPlantNameShort + ' Group {');
      self.writeThenIndent('children [');
      end;
    end;
  end;

procedure KfDrawingSurfaceForVRML.endPlant;
  begin
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      self.endBrace('plant ' + currentPlantNameLong);
      writeln(outputFile);
      end;
    kVRMLVersionTwo:
      begin
      self.endBracket('children');
      self.endBrace('plant ' + currentPlantNameLong);
      writeln(outputFile);
      end;
    end;
  currentIndentLevel := 0;
  inherited endPlant;
  end;

procedure KfDrawingSurfaceForVRML.startNestedGroupOfPlantParts(groupName: string; shortName: string; nestingType: smallint);
  begin
  shortName := self.currentPlantNameShort + '_' + shortName;
  case nestingType of
    kNestingTypeInflorescence: if not options.nest_Inflorescence then exit;
    kNestingTypeLeafAndPetiole: if not options.nest_LeafAndPetiole then exit;
    kNestingTypeCompoundLeaf: if not options.nest_CompoundLeaf then exit;
    kNestingTypePedicelAndFlowerFruit: if not options.nest_PedicelAndFlowerFruit then exit;
    kNestingTypeFloralLayers: if not options.nest_FloralLayers then exit;
    else
      raise Exception.create('Problem: Unrecognized nesting type in KfDrawingSurfaceForVRML.startNestedGroupOfPlantParts.');
    end;
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      self.writeThenIndent('DEF ' + shortName + ' Group {');
      end;
    kVRMLVersionTwo:
      begin
      self.writeThenIndent('DEF ' + shortName + ' Group {');
      self.writeThenIndent('children [');
      end;
    end;
  end;

procedure KfDrawingSurfaceForVRML.endNestedGroupOfPlantParts(nestingType: smallint);
  begin
  case nestingType of
    kNestingTypeInflorescence: if not options.nest_Inflorescence then exit;
    kNestingTypeLeafAndPetiole: if not options.nest_LeafAndPetiole then exit;
    kNestingTypeCompoundLeaf: if not options.nest_CompoundLeaf then exit;
    kNestingTypePedicelAndFlowerFruit: if not options.nest_PedicelAndFlowerFruit then exit;
    kNestingTypeFloralLayers: if not options.nest_FloralLayers then exit;
    else
      raise Exception.create('Problem: Unrecognized nesting type in KfDrawingSurfaceForVRML.endNestedGroupOfPlantParts.');
    end;
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      self.endBrace('nested group');
      writeln(outputFile);
      end;
    kVRMLVersionTwo:
      begin
      self.endBracket('children');
      self.endBrace('nested group');
      writeln(outputFile);
      end;
    end;
  end;

procedure KfDrawingSurfaceForVRML.startPlantPart(aLongName, aShortName: string);
  var shortName: string;
  begin
  shortName := self.currentPlantNameShort + '_' + aShortName;
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      self.writeThenIndent('DEF ' + shortName + ' Group {');
      end;
    kVRMLVersionTwo:
      begin
      self.writeThenIndent('DEF ' + shortName + ' Group {');
      self.writeThenIndent('children [');
      end;
    end;
  lastPlantPartName := shortName;
  end;

procedure KfDrawingSurfaceForVRML.endPlantPart;
  begin
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      self.endBrace('plant part ' + lastPlantPartName);
      writeln(outputFile);
      end;
    kVRMLVersionTwo:
      begin
      self.endBracket('children');
      self.endBrace('plant part ' + lastPlantPartName);
      writeln(outputFile);
      end;
    end;
  end;

procedure KfDrawingSurfaceForVRML.startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
    index: smallint);
  begin
  inherited startStemSegment(aLongName, aShortName, color, width, index);
  self.setColor(color);
  self.startMesh;
  end;

procedure KfDrawingSurfaceForVRML.endStemSegment;
  begin
  self.endMesh;
  end;

procedure KfDrawingSurfaceForVRML.start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
  begin
  inherited start3DObject(aLongName, aShortName, color, index);
  self.setColor(color);
  self.startMesh;
  end;

procedure KfDrawingSurfaceForVRML.end3DObject;
  begin
  self.endMesh;
  end;

procedure KfDrawingSurfaceForVRML.startMesh;
  begin
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      self.writeThenIndent('DEF ' + self.currentGroupingString + ' Group {');
      end;
    kVRMLVersionTwo:
      begin
      self.writeConsideringIndenting('DEF ' + self.currentGroupingString + ' Shape {');
      self.indent;
      if options.writeColors then
        self.writeConsideringIndenting('appearance Appearance { material Material { diffuseColor '
            + valueString(getRValue(currentColor) / 256.0) + ' '
            + valueString(getGValue(currentColor) / 256.0) + ' '
            + valueString(getBValue(currentColor) / 256.0) + ' } }');
      end;
    end;
  lastMeshName := self.currentGroupingString;
  end;

procedure KfDrawingSurfaceForVRML.endMesh;
  begin
  self.writePointsAndTriangles;
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      self.endBrace('mesh ' + lastMeshName);
      writeln(outputFile);
      end;
    kVRMLVersionTwo:
      begin
      self.endBrace('shape ' + lastMeshName);
      writeln(outputFile);
      end;
    end;
  end;

const
  kNumVRMLPointsPerLine = 4;

procedure KfDrawingSurfaceForVRML.writePointsAndTriangles;
  var i: smallint;
  begin
  case options.vrml_version of
    kVRMLVersionOne:
      begin
      // shape hints
	    self.writeThenIndent('ShapeHints {');
	    self.writeConsideringIndenting('vertexOrdering COUNTERCLOCKWISE');
            self.writeConsideringIndenting('shapeType SOLID');
            self.writeConsideringIndenting('faceType CONVEX');
            self.endBrace('ShapeHints');
      // color
      if options.writeColors then
        self.writeConsideringIndenting('Material { diffuseColor [ '
          + valueString(getRValue(currentColor) / 256.0) + ' '
          + valueString(getGValue(currentColor) / 256.0) + ' '
          + valueString(getBValue(currentColor) / 256.0) + ' ] }');
      // coordinate points
      self.writeThenIndent('Coordinate3 {');
      self.writeThenIndent('point [');
      self.doIndenting;
      for i := 0 to numPoints - 1 do
        begin
        write(outputFile,
              valueString(pressedOrNot(scale * points[i].x, kX)) + ' '
            + valueString(pressedOrNot(scale * -points[i].y, kY)) + ' '
            + valueString(pressedOrNot(scale * points[i].z, kZ)));
        if i < numPoints - 1 then write(outputFile, ', ');
        if (i mod kNumVRMLPointsPerLine = 0) or (i = numPoints - 1) then
          begin
          writeln(outputFile);
          if i < numPoints - 1 then self.doIndenting;
          end;
        end;
      self.endBracket('point');
      self.endBrace('Coordinate3');
      // faces
      self.writeThenIndent({'DEF ' + self.currentGroupingString +} 'IndexedFaceSet {');
      self.writeThenIndent('coordIndex [');
      self.doIndenting;
      for i := 0 to numFaces - 1 do
        begin
        write(outputFile, intToStr(faces[i].vertex1) + ', ' + intToStr(faces[i].vertex2) + ', '
            + intToStr(faces[i].vertex3) + ', -1');
        if i < numFaces - 1 then write(outputFile, ', ');
        if (i mod kNumVRMLPointsPerLine = 0) or (i = numFaces - 1) then
          begin
          writeln(outputFile);
          if i < numFaces - 1 then self.doIndenting;
          end;
        end;
      self.endBracket('coordIndex');
      self.endBrace('IndexedFaceSet');
      end;
    kVRMLVersionTwo:
      begin
      self.writeThenIndent('geometry IndexedFaceSet {');
      self.writeThenIndent('coord Coordinate {');
      self.writeThenIndent('point [');
      self.doIndenting;
      for i := 0 to numPoints - 1 do
        begin
        write(outputFile,
              valueString(pressedOrNot(scale * points[i].x, kX)) + ' '
            + valueString(pressedOrNot(scale * -points[i].y, kY)) + ' '
            + valueString(pressedOrNot(scale * points[i].z, kZ)));
        if i < numPoints - 1 then write(outputFile, ', ');
        if (i mod kNumVRMLPointsPerLine = 0) or (i = numPoints - 1) then
          begin
          writeln(outputFile);
          if i < numPoints - 1 then self.doIndenting;
          end;
        end;
      self.endBracket('point');
      self.endBrace('Coordinate');
      self.writeConsideringIndenting('ccw TRUE');
      self.writeConsideringIndenting('colorPerVertex FALSE');
      self.writeThenIndent('coordIndex [');
      self.doIndenting;
      for i := 0 to numFaces - 1 do
        begin
        write(outputFile, intToStr(faces[i].vertex1) + ', ' + intToStr(faces[i].vertex2) + ', '
            + intToStr(faces[i].vertex3) + ', -1');
        if i < numFaces - 1 then write(outputFile, ', ');
        if (i mod kNumVRMLPointsPerLine = 0) or (i = numFaces - 1) then
          begin
          writeln(outputFile);
          if i < numFaces - 1 then self.doIndenting;
          end;
        end;
      self.endBracket('coordIndex');
      self.writeConsideringIndenting('creaseAngle 0.5');
      self.writeConsideringIndenting('normalPerVertex TRUE');
      self.writeConsideringIndenting('solid FALSE');
      self.endBrace('IndexedFaceSet');
      end;
    end;
  numPoints := 0;
  numFaces := 0;
  end;

procedure KfDrawingSurfaceForVRML.setColor(aColor: TColorRef);
  begin
  self.currentColor := aColor;
  end;

procedure KfDrawingSurfaceForVRML.endBrace(comment: string);
  begin
  self.doIndenting;
  writeln(outputFile, '} # ' + comment);
  self.unindent;
  end;

procedure KfDrawingSurfaceForVRML.endBracket(comment: string);
  begin
  self.doIndenting;
  writeln(outputFile, '] # ' + comment);
  self.unindent;
  end;

procedure KfDrawingSurfaceForVRML.indent;
  begin
  inc(currentIndentLevel);
  end;

procedure KfDrawingSurfaceForVRML.unindent;
  begin
  dec(currentIndentLevel);
  if currentIndentLevel < 0 then currentIndentLevel := 0;
  end;

procedure KfDrawingSurfaceForVRML.doIndenting;
  var i: integer;
  begin
  for i := 1 to currentIndentLevel do write(outputFile, '  '); // chr(9));
  end;

procedure KfDrawingSurfaceForVRML.writeConsideringIndenting(aString: string);
  begin
  self.doIndenting;
  writeln(outputFile, aString);
  end;

procedure KfDrawingSurfaceForVRML.indentThenWrite(aString: string);
  begin
  self.indent;
  self.doIndenting;
  writeln(outputFile, aString);
  end;

procedure KfDrawingSurfaceForVRML.writeThenIndent(aString: string);
  begin
  self.doIndenting;
  writeln(outputFile, aString);
  self.indent;
  end;

procedure KfDrawingSurfaceForVRML.writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D);
  var numPointsAtStart: longint;
  begin
  self.setColor(rgb(100, 100, 100));
  self.currentGroupingString := currentPlantNameShort + '_reminder';
  self.startMesh;
  numPointsAtStart := numPoints;
  addPoint(p1); addPoint(p2); addPoint(p3); addPoint(p4);
  addTriangle(numPointsAtStart, numPointsAtStart+1, numPointsAtStart+3);
  addTriangle(numPointsAtStart+1, numPointsAtStart+2, numPointsAtStart+3);
  self.writePointsAndTriangles;
  self.endMesh;
  end;

{ ----------------------------------------------------------------------------- KfDrawingSurfaceForOBJ }
procedure KfDrawingSurfaceForOBJ.startFile;
  begin
  inherited startFile;
  writeln(outputFile, '# OBJ file created by PlantStudio http://www.kurtz-fernhout.com');
  if options.writeColors then
    begin
    self.materialsFileName := ExtractFilePath(fileName) + stringUpTo(ExtractFileName(fileName), '.') + '.mtl';
    writeln(outputFile);
    writeln(outputFile, '# Materials file must be in same directory');
    writeln(outputFile, 'mtllib ' + ExtractFileName(materialsFileName));
    end;
  end;

procedure KfDrawingSurfaceForOBJ.endFile;
  begin
  if options.writeColors then self.writeMaterialDescriptionsToFile;
  inherited endFile;
  end;

procedure KfDrawingSurfaceForOBJ.startPlant(aLongName: string; aPlantIndex: smallint);
  begin
  inherited startPlant(aLongName, aPlantIndex);
  writeln(outputFile);
  writeln(outputFile, '# plant "' + currentPlantNameLong + '"');
  writeln(outputFile, 'o ' + currentPlantNameShort);
  if (domain.registered) and (options.layeringOption = kLayerOutputAllTogether) then
    startGroup(currentPlantNameShort);
  end;

procedure KfDrawingSurfaceForOBJ.startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
    index: smallint);
  begin
  inherited startStemSegment(aLongName, aShortName, color, width, index);
  if (options.layeringOption <> kLayerOutputAllTogether) and (currentGroupingString <> '') then
    startGroup(currentGroupingString);
  // color should always be set by the part type, no matter what grouping setting
  startColor(color, currentPlantNameShort + '_' + aShortName);
  startVerticesAndTriangles;
  end;

procedure KfDrawingSurfaceForOBJ.endStemSegment;
  begin
  endVerticesAndTriangles;
  end;

procedure KfDrawingSurfaceForOBJ.start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
  begin
  inherited start3DObject(aLongName, aShortName, color, index);
  if (options.layeringOption <> kLayerOutputAllTogether) and (currentGroupingString <> '') then
    startGroup(currentGroupingString);
  // color should always be set by the part type, no matter what grouping setting
  startColor(color, currentPlantNameShort + '_' + aShortName);
  end;

procedure KfDrawingSurfaceForOBJ.writeMaterialDescriptionsToFile;
  var
    materialsFile: TextFile;
    i: smallint;
    colorString: string;
    fileInfo: SaveFileNamesStructure;
  begin
  if numMaterialsStored <= 0 then exit;
  if getFileSaveInfo(kFileTypeMTL, kDontAskForFileName, self.materialsFileName, fileInfo) then
    begin
    assignFile(materialsFile, fileInfo.tempFile);
    try
      setDecimalSeparator; 
      rewrite(materialsFile);
      startFileSave(fileInfo);
      writeln(materialsFile, '# Materials for file ' + stringUpTo(ExtractFileName(materialsFileName), '.') + '.obj');
      writeln(materialsFile, '# Created by PlantStudio http://www.kurtz-fernhout.com');
      writeln(materialsFile, '# These files must be in the same directory for the materials to be read correctly.');
      for i := 0 to numMaterialsStored - 1  do
        begin
        //newmtl name
        //Ka  0.1 0.0 0.0
        //Kd  0.4 0.0 0.0
        //Ks  0.4 0.0 0.0
        //Ns  20
        //d  1.0 (0 transparent 1 opaque)
        //illum 1
        if materialNames[i] = '' then continue;
        writeln(materialsFile, 'newmtl ' + materialNames[i]);
        colorString := valueString(GetRValue(materialColors[i]) / 255.0) + ' '
            + valueString(GetGValue(materialColors[i]) / 255.0) + ' '
            + valueString(GetBValue(materialColors[i]) / 255.0);
        writeln(materialsFile, 'Ka  ' + colorString);
        writeln(materialsFile, 'Kd  ' + colorString);
        writeln(materialsFile, 'Ks  ' + colorString);
        writeln(materialsFile, 'd 1.0');
        writeln(materialsFile, 'illum 1');
        writeln(materialsFile);
        end;
      fileInfo.writingWasSuccessful := true;
    finally
      closeFile(materialsFile);
      cleanUpAfterFileSave(fileInfo);
    end;
    end;
  end;

procedure KfDrawingSurfaceForOBJ.storeMaterialDescription(aName: string; aColor: TColorRef);
  var i: smallint;
  begin
  if numMaterialsStored > 0 then
    for i := 0 to numMaterialsStored - 1 do if materialNames[i] = aName then exit;
  if numMaterialsStored >= kMaxStoredMaterials then exit;
  inc(numMaterialsStored);
  materialColors[numMaterialsStored] := aColor;
  materialNames[numMaterialsStored] := aName;
  end;

procedure KfDrawingSurfaceForOBJ.startGroup(aName: string);
  begin
  writeln(outputFile);
  writeln(outputFile, 'g ' + aName);
  writeln(outputFile, 's off');
  end;

procedure KfDrawingSurfaceForOBJ.startColor(aColor: TColorRef; aMaterialName: string);
  begin
  if not options.writeColors then exit;
  writeln(outputFile);
  writeln(outputFile, 'usemtl ' + aMaterialName);
  storeMaterialDescription(aMaterialName, aColor);
  end;

procedure KfDrawingSurfaceForOBJ.endVerticesAndTriangles;
  var i: smallint;
  begin
  writeln(outputFile);
  writeln(outputFile, '# ' + intToStr(numPoints) + ' vertices');
  for i := 0 to numPoints - 1 do
    writeln(outputFile, 'v '
      + valueString(pressedOrNot(scale * points[i].x, kX)) + ' '
      + valueString(pressedOrNot(scale * -points[i].y, kY)) + ' '
      + valueString(pressedOrNot(scale * points[i].z, kZ)));
  writeln(outputFile);
  writeln(outputFile, '# ' + intToStr(numFaces) + ' faces');
  for i := 0 to numFaces - 1 do
    writeln(outputFile, 'f '
      + intToStr(faces[i].vertex1 - numPoints) + ' '
      + intToStr(faces[i].vertex2 - numPoints) + ' '
      + intToStr(faces[i].vertex3 - numPoints) + ' ' );
  numPoints := 0;
  numFaces := 0;
  end;

procedure KfDrawingSurfaceForOBJ.writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D);
  var numPointsAtStart: smallint;
  begin
  startGroup(currentPlantNameShort + '_reminder');
  startColor(rgb(100, 100, 100), 'reminder_gray');
  numPointsAtStart := numPoints;
  startVerticesAndTriangles;
  addPoint(p1); addPoint(p2); addPoint(p3); addPoint(p4);
  addTriangle(numPointsAtStart, numPointsAtStart+1, numPointsAtStart+3);
  addTriangle(numPointsAtStart+1, numPointsAtStart+2, numPointsAtStart+3);
  endVerticesAndTriangles;
  if options.layeringOption = kLayerOutputAllTogether then
    startGroup(currentPlantNameShort);
  end;

{ ----------------------------------------------------------------------------- KfBinaryFileExportSurface }

constructor KfBinaryFileExportSurface.createWithFileName(aFileName: string);
  begin
  inherited createWithFileName(aFileName);
  chunkStartStack := TList.create;
  end;

destructor KfBinaryFileExportSurface.destroy;
  begin
  chunkStartStack.free;
  chunkStartStack := nil;
  stream.free;  // this closes the file
  stream := nil;
  inherited destroy;
  end;

procedure KfBinaryFileExportSurface.startFile;
  begin
  stream := TFileStream.create(fileName, fmCreate or fmShareExclusive);
  end;

procedure KfBinaryFileExportSurface.endFile;
  begin
  raise exception.create('subclasses must override');
  end;

procedure KfBinaryFileExportSurface.writeStringZ(value: string);
  var
    stringBuffer: array [0..1024] of Char;
    i: integer;
  begin
  if length(value) > 1023 then
    raise Exception.Create('Problem: String too long in KfBinaryFileExportSurface.writeStringZ.');
  for i := 1 to Length(value) do
    stringBuffer[i-1] := value[i];
  stringBuffer[Length(value)] := Chr(0);
  stream.WriteBuffer(stringBuffer, Length(value) + 1);
  // maybe should align on four byte boundaries for efficiency of seeks later?
  end;

procedure KfBinaryFileExportSurface.writeByte(value: byte);
  begin
  stream.WriteBuffer(value, 1);
  end;

procedure KfBinaryFileExportSurface.writeWord(value: word);
  var swappedBytes: array[0..1] of byte;
  begin
  if self.isLittleEndian then
    stream.WriteBuffer(value, 2)
  else
    begin
    swappedBytes[1] := value and 255;
    swappedBytes[0] := value shr 8;
    stream.WriteBuffer(swappedBytes, 2);
    end;
  end;

procedure KfBinaryFileExportSurface.writeDword(value: longint);
  var swappedBytes: array[0..3] of byte;
  begin
  if self.isLittleEndian then
    stream.WriteBuffer(value, 4)
  else
    begin
    swappedBytes[3] := value and 255;
    swappedBytes[2] := (value shr 8) and 255;
    swappedBytes[1] := (value shr 16) and 255;
    swappedBytes[0] := (value shr 24) and 255;
    stream.WriteBuffer(swappedBytes, 4);
    end;
  end;

type SingleOverlay =
  record
    case Integer of
      1: (numeric: Single);
      2: (bytes: array[0..3] of byte);
      end;

procedure KfBinaryFileExportSurface.writeFloat(value: Single);
  var
    convert: SingleOverlay;
    swappedBytes: array[0..3] of byte;
  begin
  if self.isLittleEndian then
    stream.WriteBuffer(value, 4)
  else
    begin
    convert.numeric := value;
    swappedBytes[3] := convert.bytes[0];
    swappedBytes[2] := convert.bytes[1];
    swappedBytes[1] := convert.bytes[2];
    swappedBytes[0] := convert.bytes[3];
    stream.WriteBuffer(swappedBytes, 4);
    end;
  end;

function KfBinaryFileExportSurface.isLittleEndian: boolean;
  begin
  // subclasses should override if they need to change this
  result := true;
  end;

{ ----------------------------------------------------------------------------- KfDrawingSurfaceFor3DS }
constructor KfDrawingSurfaceFor3DS.createWithFileName(aFileName: string);
  begin
  // we assume that the file name has been already okayed
  inherited createWithFileName(aFileName);
  currentMaterialName := 'not defined';
  end;

destructor KfDrawingSurfaceFor3DS.destroy;
  begin
  inherited destroy;
  end;

procedure KfDrawingSurfaceFor3DS.startFile;
  begin
  inherited startFile;
  // 4d4dH 	M3DMAGIC; 3DS Magic Number (.3DS file)
  self.startChunk($4D4D);
  // 3d3dH 	MDATA; Mesh Data Magic Number (.3DS files sub of 4d4d)
  self.startChunk($3D3D);
  end;

procedure KfDrawingSurfaceFor3DS.endFile;
  begin
  // 3d3dH 	MDATA; Mesh Data Magic Number (.3DS files sub of 4d4d)
  self.finishChunk($3D3D);
  // 4d4dH 	M3DMAGIC; 3DS Magic Number (.3DS file)
  self.finishChunk($4D4D);
  end;

procedure KfDrawingSurfaceFor3DS.startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
    index: smallint);
  begin
  inherited startStemSegment(aLongName, aShortName, color, width, index);
  currentMaterialName := currentPlantNameShort + '_' + aShortName;
  startVerticesAndTriangles;
  end;

procedure KfDrawingSurfaceFor3DS.endStemSegment;
  begin
  endVerticesAndTriangles;
  end;

procedure KfDrawingSurfaceFor3DS.start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
  begin
  inherited start3DObject(aLongName, aShortName, color, index);
  currentMaterialName := currentPlantNameShort + '_' + aShortName;
  end;

procedure KfDrawingSurfaceFor3DS.startVerticesAndTriangles;
  begin
  startMeshObject(self.currentGroupingString);
  end;

procedure KfDrawingSurfaceFor3DS.endVerticesAndTriangles;
  var i: integer;
  begin
  // 4110H 	POINT_ARRAY short npoints; struct (float x, y, z;) points[npoints];
  self.startChunk($4110);
  self.writeWord(numPoints);
  for i := 0 to numPoints - 1 do
    begin
    self.writeFloat(pressedOrNot(scale * points[i].x, kX));
    self.writeFloat(pressedOrNot(scale * points[i].y, kY));
    self.writeFloat(pressedOrNot(scale * points[i].z, kZ));
    end;
  self.finishChunk($4110);
  // 4120H 	FACE_ARRAY may be followed by smooth_group short nfaces;
  // struct (short vertex1, vertex2, vertex3; short flags;) facearray[nfaces];
  self.startChunk($4120);
  self.writeWord(numFaces);
  for i := 0 to numFaces - 1 do
    begin
    self.writeWord(faces[i].vertex1);
    self.writeWord(faces[i].vertex2);
    self.writeWord(faces[i].vertex3);
    self.writeWord(7);
    end;
  if options.writeColors then
    begin
    // now set all faces to be of same material
    self.startChunk($4130);
    self.writeStringZ(self.currentMaterialName);
    self.writeWord(numFaces);
    for i := 0 to numFaces - 1 do
      self.writeWord(i);
    self.finishChunk($4130);
    end;
  self.finishChunk($4120);  
  // close mesh
  self.finishMeshObject;
  // zero out
  numFaces := 0;
  numPoints := 0;
  end;

procedure KfDrawingSurfaceFor3DS.startMeshObject(name: string);
  begin
  // 4000H 	NAMED_OBJECT cstr name;
  self.startChunk($4000);
  self.writeStringZ(name);
  // 4100H 	N_TRI_OBJECT named triangle object followed by point_array, point_flag_array, mesh_matrix, face_array
  self.startChunk($4100);
  end;

procedure KfDrawingSurfaceFor3DS.finishMeshObject;
  begin
  // 4100H 	N_TRI_OBJECT named triangle object followed by point_array, point_flag_array, mesh_matrix, face_array
  self.finishChunk($4100);
  // 4000H 	NAMED_OBJECT cstr name;
  self.finishChunk($4000);
  end;

procedure KfDrawingSurfaceFor3DS.pushChunkStart;
  var position: integer;
  begin
  position := stream.Position;
  chunkStartStack.Add(Pointer(position));
  end;

procedure KfDrawingSurfaceFor3DS.popChunkStartAndFixupChunkSize;
  var
    chunkSize, startSize, totalSize, lastIndex: integer;
  begin
  totalSize := stream.Size;
  lastIndex := chunkStartStack.Count - 1;
  // should check if -1
  if lastIndex < 0 then
    raise Exception.Create('Problem with stack indexing for 3DS writing in method KfDrawingSurfaceFor3DS.popChunkStartAndFixupChunkSize.');
  startSize := Integer(chunkStartStack.Items[lastIndex]);
  chunkStartStack.Delete(lastIndex);
  chunkSize := totalSize - startSize;
  // skip two to avoid overwriting chunk type
  stream.Seek(startSize + 2, soFromBeginning);
  self.writeDWord(chunkSize);
  stream.Seek(0, soFromEnd);
  end;

procedure KfDrawingSurfaceFor3DS.startChunk(chunkID: integer);
  begin
  self.pushChunkStart;
  self.writeWord(chunkID);
  // write placeholder dword that will be patched later
  self.writeDword(0);
  end;

procedure KfDrawingSurfaceFor3DS.finishChunk(chunkType: integer);
  begin
  self.popChunkStartAndFixupChunkSize;
  end;

procedure KfDrawingSurfaceFor3DS.writeMaterialDescription(index: smallint; aColor: TColorRef);
  begin
  if not options.writeColors then exit;
  if index < 0 then
    writeMaterialColorChunk(currentPlantNameShort + '_rem', getRValue(aColor), getGValue(aColor), getBValue(aColor))
  else
    writeMaterialColorChunk(currentPlantNameShort + '_' + shortNameForDXFPartType(index),
      getRValue(aColor), getGValue(aColor), getBValue(aColor));
  end;

procedure KfDrawingSurfaceFor3DS.writeColorChunk(r: byte; g: byte; b: byte);
  begin
  self.startChunk($0011);
  self.writeByte(r);
  self.writeByte(g);
  self.writeByte(b);
  self.finishChunk($0011);
  end;

procedure KfDrawingSurfaceFor3DS.writeMaterialColorChunk(materialName: string; r, g, b: byte);
  begin
  self.startChunk($AFFF); // Material editor chunk
  self.startChunk($A000); // Material name
  self.writeStringZ(materialName);
  self.finishChunk($A000);
  self.startChunk($A010); // Material ambient color
  self.writeColorChunk(r, g, b);
  self.finishChunk($A010);
  self.startChunk($A020); // Material diffuse color
  self.writeColorChunk(r, g, b);
  self.finishChunk($A020);
  self.finishChunk($AFFF);
  end;

procedure KfDrawingSurfaceFor3DS.writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D);
  var numPointsAtStart: smallint;
  begin
  currentGroupingString := currentPlantNameShort + '_rem';
  currentMaterialName := currentPlantNameShort + '_rem';
  numPointsAtStart := numPoints;
  startVerticesAndTriangles;
  addPoint(p1); addPoint(p2); addPoint(p3); addPoint(p4);
  addTriangle(numPointsAtStart, numPointsAtStart+1, numPointsAtStart+3);
  addTriangle(numPointsAtStart+1, numPointsAtStart+2, numPointsAtStart+3);
  endVerticesAndTriangles;                  
  end;

{ ----------------------------------------------------------------------------- KfDrawingSurfaceForLWO }
procedure KfDrawingSurfaceForLWO.endFile;
  var i: longint;
  begin
  // start file
  self.startChunk('FORM');
  self.writeTagOfFourCharacters('LWOB');
  // points
  self.startChunk('PNTS');
  for i := 0 to numPoints - 1 do
    begin
    self.writeFloat(pressedOrNot(scale * points[i].x, kX));
    self.writeFloat(pressedOrNot(scale * points[i].y, kY));
    self.writeFloat(pressedOrNot(scale * points[i].z, kZ));
    end;
  self.finishChunk;
  // surfaces
  if options.writeColors then
    begin
    self.startChunk('SRFS');
    for i := 1 to numSurfacesStored do
      begin
      self.writeStringZ(surfaceNames[i]);
      if odd(length(surfaceNames[i]) + 1 {1 is for terminating zero}) then self.writeByte(0);
      end;
    self.finishChunk;
    end
  else
    begin
    self.startChunk('SRFS');
    self.writeStringZ('default'); // if you change this to an odd # considering the end zero you must pad it
    self.finishChunk;
    end;
  // faces
  self.startChunk('POLS');
  for i := 0 to numFaces - 1 do
    begin
    self.writeWord(3);
    self.writeWord(faces[i].vertex1);
    self.writeWord(faces[i].vertex2);
    self.writeWord(faces[i].vertex3);
    if options.writeColors then
      self.writeWord(faces[i].surfaceID)
    else
      self.writeWord(1);
    end;
  self.finishChunk;
  if options.writeColors then
    begin
    // surfaces again
    for i := 1 to numSurfacesStored do
      begin
      self.startChunk('SURF');
      self.writeStringZ(surfaceNames[i]);
      if odd(length(surfaceNames[i]) + 1 {terminating zero}) then self.writeByte(0);
      self.writeTagOfFourCharacters('COLR');
      self.writeWord(4);
      self.writeByte(getRValue(surfaceColors[i]));
      self.writeByte(getGValue(surfaceColors[i]));
      self.writeByte(getBValue(surfaceColors[i]));
      self.writeByte(0);
      self.writeTagOfFourCharacters('FLAG');
      self.writeWord(2);
      self.writeWord($0100); // double-sided flag
      self.writeTagOfFourCharacters('DIFF');
      self.writeWord(2);
      self.writeWord(256);
      self.finishChunk;
      end;
    end
  else
    begin
    self.startChunk('SURF');
    self.writeStringZ('default'); // if you change this to an odd # considering the end zero you must pad it
    self.writeTagOfFourCharacters('COLR');
    self.writeWord(4);
    self.writeByte(200);
    self.writeByte(200);
    self.writeByte(200);
    self.writeByte(0);
    self.finishChunk;
    end;
  self.finishChunk; // finishes 'FORM' chunk
  numFaces := 0;
  numPoints := 0;
  end;

function KfDrawingSurfaceForLWO.isLittleEndian: boolean;
  begin
  result := false;
  end;

procedure KfDrawingSurfaceForLWO.startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
    index: smallint);
  begin
  inherited startStemSegment(aLongName, aShortName, color, width, index);
  currentSurfaceID := self.lookUpSurfaceIDForName({currentPlantNameShort + '_' + aShortName}currentGroupingString, color);
  end;

function KfDrawingSurfaceForLWO.lookUpSurfaceIDForName(aName: string; color: TColorRef): smallint;
  var i: longint;
  begin
  for i := 1 to numSurfacesStored do
    if surfaceNames[i] = aName then
      begin
      result := i;
      exit;
      end;
  if numSurfacesStored < kMaxStoredMaterials then
    begin
    inc(numSurfacesStored);
    surfaceNames[numSurfacesStored] := aName;
    surfaceColors[numSurfacesStored] := color;
    end;
  result := numSurfacesStored;
  end;

procedure KfDrawingSurfaceForLWO.drawPipeFaces(const startPoints: array of KfPoint3D;
    const endPoints: array of KfPoint3D; faces: smallint; segmentNumber: smallint);
  var i, firstPtIndex: longint;
  begin
  firstPtIndex := self.numPoints;
  for i := 0 to faces - 1 do addPoint(startPoints[i]);
  for i := 0 to faces - 1 do addPoint(endPoints[i]);
  for i := 0 to faces - 1 do
    begin
    addTriangle(firstPtIndex + i, firstPtIndex + i + faces, firstPtIndex + (i+1) mod faces);
    addTriangle(firstPtIndex + (i+1) mod faces, firstPtIndex + i + faces, firstPtIndex + (i+1) mod faces + faces);
    end;
  end;

procedure KfDrawingSurfaceForLWO.start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
  begin
  inherited start3DObject(aLongName, aShortName, color, index);
  currentSurfaceID := self.lookUpSurfaceIDForName({currentPlantNameShort + '_' + aShortName}currentGroupingString, color);
  end;

procedure KfDrawingSurfaceForLWO.addTriangle(a, b, c: integer);
  begin
  self.addTriangleWithSurface(a, b, c, self.currentSurfaceID);
  end;

procedure KfDrawingSurfaceForLWO.addTriangleWithSurface(a, b, c, surfaceID: integer);
  begin
  if numFaces >= kMax3DFaces then
      raise Exception.Create('Problem: Too many faces in LWO; in method KfDrawingSurfaceFor3DS.addTriangle.');
  faces[numFaces].vertex1 := a;
  faces[numFaces].vertex2 := b;
  faces[numFaces].vertex3 := c;
  faces[numFaces].surfaceID := currentSurfaceID;
  inc(numFaces);
  end;

procedure KfDrawingSurfaceForLWO.pushChunkStart;
  var position: integer;
  begin
  position := stream.Position;
  chunkStartStack.Add(Pointer(position));
  end;

procedure KfDrawingSurfaceForLWO.popChunkStartAndFixupChunkSize;
  var
    chunkSize, startSize, totalSize, lastIndex: integer;
  begin
  totalSize := stream.Size;
  lastIndex := chunkStartStack.Count - 1;
  // should check if -1
  if lastIndex < 0 then
    raise Exception.Create('Problem with stack indexing for 3DS writing in method KfDrawingSurfaceFor3DS.popChunkStartAndFixupChunkSize.');
  startSize := Integer(chunkStartStack.Items[lastIndex]);
  chunkStartStack.Delete(lastIndex);
  chunkSize := totalSize - startSize;
  // skip back four
  stream.Seek(startSize - 4, soFromBeginning);
  // lwo chunk sizes do not include the header
  self.writeDWord(chunkSize);
  stream.Seek(0, soFromEnd);
  end;

procedure KfDrawingSurfaceForLWO.startChunk(chunkName: string);
  begin
  self.writeTagOfFourCharacters(chunkName);
  // write placeholder dword that will be patched later
  self.writeDword(0);
  self.pushChunkStart;
  end;

procedure KfDrawingSurfaceForLWO.finishChunk;
  begin
  self.popChunkStartAndFixupChunkSize;
  end;

procedure KfDrawingSurfaceForLWO.writeTagOfFourCharacters(aString: string);
  begin
  self.writeByte(Byte(aString[1]));
  self.writeByte(Byte(aString[2]));
  self.writeByte(Byte(aString[3]));
  self.writeByte(Byte(aString[4]));
  end;

procedure KfDrawingSurfaceForLWO.writeRegistrationReminder(p1, p2, p3, p4: KFPoint3D);
  var numPointsAtStart: smallint;
  begin
  currentSurfaceID := self.lookUpSurfaceIDForName(currentPlantNameShort + '_rem', rgb(100, 100, 100));
  numPointsAtStart := numPoints;
  addPoint(p1); addPoint(p2); addPoint(p3); addPoint(p4);
  addTriangle(numPointsAtStart, numPointsAtStart+1, numPointsAtStart+3);
  addTriangle(numPointsAtStart+1, numPointsAtStart+2, numPointsAtStart+3);
  end;

{ ------------------------------------------------------------------------------------------ index functions }

function fileTypeFor3DExportType(outputType: smallint): smallint;
  begin
  case outputType of
    kDXF: result := kFileTypeDXF;
    kPOV: result := kFileTypeINC;
    k3DS: result := kFileType3DS;
    kOBJ: result := kFileTypeOBJ;
    kVRML: result := kFileTypeVRML;
    kLWO: result := kFileTypeLWO;
    else raise Exception.create('Problem: Invalid export type in TMainForm.fileTypeFor3DExportType.');
    end;
  end;

function nameFor3DExportType(anOutputType: smallint): string;
  begin
  case anOutputType of
    kDXF: result := 'DXF';
    kPOV: result := 'POV';
    k3DS: result := '3DS';
    kOBJ: result := 'OBJ';
    kVRML: result := 'VRML';
    kLWO: result := 'LWO';
    else raise Exception.create('Problem: Invalid type in PdDomain.sectionNumberFor3DExportType.');
    end;
  end;

function longNameForDXFPartType(index: smallint): string;
  var
    longName, shortName: string;
  begin
  getInfoForDXFPartType(index, longName, shortName);
  result := longName;
  end;

function shortNameForDXFPartType(index: smallint): string;
  var
    longName, shortName: string;
  begin
  getInfoForDXFPartType(index, longName, shortName);
  result := shortName;
  end;

procedure getInfoForDXFPartType(index: smallint; var longName: string; var shortName: string);
  begin
  case index of
    kExportPartMeristem:
      begin longName := 'Meristem'; shortName := 'Mrstm'; end;
    kExportPartInternode:
      begin longName := 'Internode'; shortName := 'Intrnd'; end;
    kExportPartSeedlingLeaf:
      begin longName := 'Seedling leaf'; shortName := '1stLeaf'; end;
    kExportPartLeaf:
      begin longName := 'Leaf'; shortName := 'Leaf'; end;
    kExportPartFirstPetiole:
      begin longName := 'Seedling petiole'; shortName := '1stPetiole'; end;
    kExportPartPetiole:
      begin longName := 'Petiole'; shortName := 'Petiole'; end;
    kExportPartLeafStipule:
      begin longName := 'Leaf stipule'; shortName := 'Stipule'; end;
    kExportPartInflorescenceStalkFemale:
      begin longName := 'Primary inflorescence stalk (peduncle)'; shortName := '1Pdncle'; end;
    kExportPartInflorescenceInternodeFemale:
      begin longName := 'Primary inflorescence internode'; shortName := '1InfInt'; end;
    kExportPartInflorescenceBractFemale:
      begin longName := 'Primary inflorescence bract'; shortName := '1Bract'; end;
    kExportPartInflorescenceStalkMale:
      begin longName := 'Secondary inflorescence stalk (peduncle)'; shortName := '2Pdncle'; end;
    kExportPartInflorescenceInternodeMale:
      begin longName := 'Secondary inflorescence internode'; shortName := '2InfInt'; end;
    kExportPartInflorescenceBractMale:
      begin longName := 'Secondary inflorescence bract'; shortName := '2Bract'; end;
    kExportPartPedicelFemale:
      begin longName := 'Primary flower stalk'; shortName := '1Pdcel'; end;
    kExportPartFlowerBudFemale:
      begin longName := 'Primary flower bud'; shortName := '1Bud'; end;
    kExportPartStyleFemale:
      begin longName := 'Flower style'; shortName := 'Style'; end;
    kExportPartStigmaFemale:
      begin longName := 'Flower stigma'; shortName := 'Stigma'; end;
    kExportPartFilamentFemale:
      begin longName := 'Primary flower filament'; shortName := '1Flmnt'; end;
    kExportPartAntherFemale:
      begin longName := 'Primary flower anther'; shortName := '1Anther'; end;
    kExportPartFirstPetalsFemale:
      begin longName := 'Primary flower petal, first row'; shortName := '1Petal1'; end;
    kExportPartSecondPetalsFemale:
      begin longName := 'Flower petal, second row'; shortName := '1Petal2'; end;
    kExportPartThirdPetalsFemale:
      begin longName := 'Flower petal, third row'; shortName := '1Petal3'; end;
    kExportPartFourthPetalsFemale:
      begin longName := 'Flower petal, fourth row'; shortName := '1Petal4'; end;
    kExportPartFifthPetalsFemale:
      begin longName := 'Flower petal, fifth row'; shortName := '1Petal5'; end;
    kExportPartSepalsFemale:
      begin longName := 'Primary flower sepal'; shortName := '1Sepal'; end;
    kExportPartPedicelMale:
      begin longName := 'Secondary flower stalk'; shortName := '2Pdcel'; end;
    kExportPartFlowerBudMale: 
      begin longName := 'Secondary flower bud'; shortName := '2Bud'; end;
    kExportPartFilamentMale:
      begin longName := 'Secondary flower filament'; shortName := '2Flmnt'; end;
    kExportPartAntherMale: 
      begin longName := 'Secondary flower anther'; shortName := '2Anther'; end;
    kExportPartFirstPetalsMale: 
      begin longName := 'Secondary flower petal'; shortName := '2Petal1'; end;
    kExportPartSepalsMale:
      begin longName := 'Secondary flower sepal'; shortName := '2Sepal'; end;
    kExportPartUnripeFruit:
      begin longName := 'Unripe fruit'; shortName := 'FruitU'; end;
    kExportPartRipeFruit:
      begin longName := 'Ripe fruit'; shortName := 'FruitR'; end;
    kExportPartRootTop:
      begin longName := 'Root top'; shortName := 'Root'; end;
    else
      raise Exception.create('Problem: Invalid part type in method getInfoForDXFPartType.');
    end;
  end;

  // VRML 1.0 spec
(*
DEF plantName Group {
  DEF nestingName Group {
    DEF partName Group {
      Material { diffuseColor [ 0.19 0.39 0.19 ] }
	    ShapeHints {
	      vertexOrdering	COUNTERCLOCKWISE
	      shapeType	SOLID
	      creaseAngle	3.14159
	      } # ShapeHints
      Coordinate3 {
          point [
            49.64	304.6	117.55	,
            56.71	312.51	123.85	,
            ] # point
          } # Coordinate3
      IndexedFaceSet {
        coordIndex [
          0	, 1	, 2	, -1	,
          1	, 3	, 2	, -1	,
          ] # coordIndex
        } # IndexedFaceSet
      } # Group partName
    } # Group nestingName
  } # Group plantName
*)

  // VRML 2.0 spec
  (*
DEF plantName Group {
  children [
  DEF nestingName Group {
    children [
      DEF partName Shape {
        appearance Appearance { material Material { diffuseColor  0.99 0  0.5 } }
        geometry IndexedFaceSet {
          coord Coordinate {
            point [
              49.64	304.6	117.55	,
              56.71	312.51	123.85	,
              ] # point
            } # Coordinate
          ccw TRUE
          colorPerVertex FALSE
          coordIndex [
            0	, 1	, 2	, -1	,
            1	, 3	, 2	, -1	,
            ] # coordIndex
          creaseAngle 0.5
          normalPerVertex TRUE
          solid FALSE
          } #  IndexedFaceSet
        } # Shape
      ] # children nestingName
      } # Group nestingName
    ] # children plantName
  } # Group plantName
*)

end.
 