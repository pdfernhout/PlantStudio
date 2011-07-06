unit Utdo;

interface

uses Windows, Classes, SysUtils, Dialogs, Graphics, StdCtrls,
  ucollect, usstream, ufiler;

const
  kMaximumRecordedPoints = 10000; // v1.6b2 changed from 200 to 1000 ; v2.0 changed to 10000 (not in tdo anymore)
  kAdjustForOrigin = true; kDontAdjustForOrigin = false;
  kEmbeddedInPlant = true; kInTdoLibrary = false; kStandAloneFile = false;
  kTdoForeColor = clSilver;
  kTdoBackColor = clGray;
  kTdoLineContrastIndex = 10;
  kStartTdoString = 'start 3D object';    // v1.11 moved up here
  kEndTdoString =  'end 3D object';       // v1.11 moved up here

type
	KfPoint3D = record
    x: single;
    y: single;
    z: single;
    end;

  PKfPoint3DArray = ^TKfPoint3DArray;
  TKfPoint3DArray = array[0..MaxListSize - 1] of KfPoint3D;

	KfIndexTriangle = class(PdStreamableObject)
    public
    pointIndexes: array[0..2] of longint;
    constructor createABC(a: longint; b: longint; c: longint);
    procedure flip;
    procedure copyFrom(aTriangle: KfIndexTriangle);
    procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
    procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
    end;

	KfObject3D = class(PdStreamableObject)
  	public
    pointData: PKfPoint3DArray;
    pointsInUse: longint;
    pointsAllocated: longint;
    originPointIndex: longint;
    triangles: TListCollection;
    name: string[80];
    originalIfCopy: KfObject3D;
    inUse: boolean;
    zForSorting: single; // doesn't need to be streamed, only used while drawing
    indexWhenRemoved, selectedIndexWhenRemoved: smallint;
    boundsRect: TRect;
    constructor create; override;
    destructor destroy; override;
    procedure ensureEnoughSpaceForNewPointData(totalNumberOfPointsToBeUsed: longint);
    function getPoint(index: integer): KfPoint3d;
    procedure setPoint(index: integer; const aPoint: KfPoint3d);
    property points[index: integer]: KfPoint3d read getPoint write setPoint;
    procedure clear;
    procedure clearPoints;
		function addPoint(const aPoint: KfPoint3d): smallint;
    function addPointIfNoMatch(const aPoint: KfPoint3d; matchDistance: single): smallint;
    procedure makeMirrorTriangles;
		function pointForIndex(anIndex: longint): KfPoint3D;
		procedure addTriangle(aTriangle: KfIndexTriangle);
		function triangleForIndex(anIndex: longint): KfIndexTriangle;
		procedure adjustForOrigin;
    procedure setOriginPointIndex(newOriginPointIndex: integer);
    function bestPointForDrawingAtScale(turtleProxy: TObject; origin: TPoint; bitmapSize: TPoint; scale: single): TPoint;
    function draw(turtleProxy: TObject; scale: single;
        longName: string; shortName: string; dxfIndex: smallint; partID: longint): TRect;
    procedure overlayBoundsRect(turtleProxy: TObject; scale: single);
    procedure write3DExportElements(turtleProxy: TObject; scale: single; partID: smallint);
		procedure addTriangleWithVerticesABC(a: longint; b: longint; c: longint);
		procedure addPointString(stream: KfStringStream);
		procedure addTriangleString(stream: KfStringStream);
    procedure readFromInputString(aString: string; doAdjustForOrigin: boolean);
    procedure writeToFile(fileName: string);
    procedure readFromFile(fileName: string);
    procedure writeToFileStream(var outputFile: TextFile; embeddedInPlant: boolean);
    procedure writeToMemo(aMemo: TMemo);
		procedure readFromFileStream(var inputFile: TextFile; embeddedInPlant: boolean);
    procedure readFromDXFFile(var inputFile: TextFile);
    procedure readFromMemo(aMemo: TMemo; var readingMemoLine: longint);
    procedure copyFrom(original: KfObject3D);
    function isSameAs(other: KfObject3D): boolean;
    function getName: string;
    procedure setName(newName: string);
    procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
    procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
    function totalMemorySize: longint;
    procedure removeTriangle(aTriangle: KfIndexTriangle);
    procedure removePointsNotInUse;
    function pointIsReallyInUse(point: smallint): boolean;
    procedure removePoint(point: smallint);
    procedure deletePointIndexInTriangles(oldPointIndex: smallint);
    procedure writeToDXFFile(fileName: string; frontFaceColor, backFaceColor: TColorRef);
    procedure writeTriangleToDXFFIle(var outputFile: TextFile; p1, p2, p3: KfPoint3D; color: TColorRef);
    procedure writeToPOV_INCFile(fileName: string; frontFaceColor: TColorRef; embeddedInPlant: boolean; rotateCount: integer);
    procedure writeTriangleToPOV_INCFIle(var outputFile: TextFile; p1, p2, p3: KfPoint3D);
    function triangleIsBackFacing(aTriangle: KfIndexTriangle): boolean;
    procedure reverseZValues;
  	end;

procedure KfPoint3D_setXYZ(var thePoint: KfPoint3D; aX: single; aY: single; aZ: single);
procedure KfPoint3D_addXYZ(var thePoint: KfPoint3D; xOffset: single; yOffset: single; zOffset: single);
procedure KfPoint3D_scaleBy(var thePoint: KfPoint3D; aScale: single);
procedure KfPoint3D_subtract(var thePoint: KfPoint3D; const aPoint: KfPoint3D);
function KfPoint3D_matchXYZ(const pointOne: KfPoint3D; const pointTwo: KfPoint3D; matchDistance: single): boolean;
procedure KfPoint3D_addPointToBoundsRect(var boundsRect: TRect; const aPoint: KfPoint3d);

implementation

uses uturtle, uclasses, usupport, udebug, uplant, u3dsupport, u3dexport;

{ ---------------------------------------------------------------------------------- KfPoint3D }
procedure KfPoint3D_setXYZ(var thePoint: KfPoint3D; aX: single; aY: single; aZ: single);
	begin
  with thePoint do
    begin
		x := aX;
  	y := aY;
  	z := aZ;
    end;
  end;

procedure KfPoint3D_addXYZ(var thePoint: KfPoint3D; xOffset: single; yOffset: single; zOffset: single);
	begin
  {pdf - shift point by x y and z.}
  with thePoint do
    begin
  	x := x + xOffset;
  	y := y + yOffset;
  	z := z + zOffset;
    end;
  end;

procedure KfPoint3D_scaleBy(var thePoint: KfPoint3D; aScale: single);
  begin
  {pdf - multiply point by scale.}
  with thePoint do
    begin
  	x := x * aScale;
  	y := y * aScale;
  	z := z * aScale;
    end;
  end;

procedure KfPoint3D_subtract(var thePoint: KfPoint3D; const aPoint: KfPoint3D);
  begin
    {pdf - subtract point from this point.}
  with thePoint do
    begin
    x := x - aPoint.x;
    y := y - aPoint.y;
    z := z - aPoint.z;
    end;
  end;

function KfPoint3D_matchXYZ(const pointOne: KfPoint3D; const pointTwo: KfPoint3D; matchDistance: single): boolean;
  begin
  // v1.6b1 added
  result := (abs(pointOne.x - pointTwo.x) <= matchDistance)
    and (abs(pointOne.y - pointTwo.y) <= matchDistance)
    and (abs(pointOne.z - pointTwo.z) <= matchDistance);
  end;

procedure KfPoint3D_addPointToBoundsRect(var boundsRect: TRect; const aPoint: KfPoint3d);
  var
    x, y: longint;
	begin
  try x := round(aPoint.x); except x := 0; end;
  try y := round(aPoint.y); except y := 0; end;
  with boundsRect do
    begin
    // on first point entered, initialize bounds rect
    if (left = 0) and (right = 0) and (top = 0) and (bottom = 0) then
      begin
      left := x;
      right := x;
      top := y;
      bottom := y;
      end
    else
      begin
  		if x < left then
  			left := x
    	else if x > right then
      	right := x;
    	if y < top then
      	top := y
    	else if y > bottom then
      	bottom := y;
    	end;
    end;
  end;

{ ---------------------------------------------------------------------------------- KfIndexTriangle }
constructor KfIndexTriangle.createABC(a: longint; b: longint; c: longint);
	begin
  self.create;
  pointIndexes[0] := a;
  pointIndexes[1] := b;
  pointIndexes[2] := c;
  end;

procedure KfIndexTriangle.flip;
  var
    savePoint: longint;
  begin
  savePoint := pointIndexes[0];
  pointIndexes[0] := pointIndexes[2];
  pointIndexes[2] := savePoint;
  end;

procedure KfIndexTriangle.copyFrom(aTriangle: KfIndexTriangle);
  begin
  if aTriangle = nil then exit;
  pointIndexes[0] := aTriangle.pointIndexes[0];
  pointIndexes[1] := aTriangle.pointIndexes[1];
  pointIndexes[2] := aTriangle.pointIndexes[2];
  end;

procedure KfIndexTriangle.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kKfIndexTriangle;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure KfIndexTriangle.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
	begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    streamBytes(pointIndexes, sizeOf(pointIndexes));
  end;

{ ---------------------------------------------------------------------------------- KfObject3D }
constructor KfObject3D.create;
	begin
  inherited create;
  triangles := TListCollection.create;
  end;

destructor KfObject3D.destroy;
	begin
  triangles.free;
  triangles := nil;
  if pointData <> nil then FreeMem(pointData);
  inherited destroy;
  end;

const kPointAllocationIncrement = 8;

procedure KfObject3D.ensureEnoughSpaceForNewPointData(totalNumberOfPointsToBeUsed: longint);
  begin
  if pointsAllocated >= totalNumberOfPointsToBeUsed then exit;
  if pointData = nil then
    begin
    if totalNumberOfPointsToBeUsed < kPointAllocationIncrement then
      totalNumberOfPointsToBeUsed := kPointAllocationIncrement;
    GetMem(pointData, totalNumberOfPointsToBeUsed * sizeof(KfPoint3D))
    // assuming this throws its own memory exception
    end
  else
    begin
    if totalNumberOfPointsToBeUsed mod kPointAllocationIncrement <> 0 then
      totalNumberOfPointsToBeUsed := totalNumberOfPointsToBeUsed + kPointAllocationIncrement
          - (totalNumberOfPointsToBeUsed mod kPointAllocationIncrement);
    ReallocMem(pointData, totalNumberOfPointsToBeUsed * sizeof(KfPoint3D));
    // assuming this throws its own memory exception
    end;
  pointsAllocated := totalNumberOfPointsToBeUsed;
  end;

function KfObject3D.getPoint(index: integer): KfPoint3d;
  begin
  result := pointData^[index];
  end;

procedure KfObject3D.setPoint(index: integer; const aPoint: KfPoint3d);
  begin
  if pointData = nil then
    raise Exception.create('Problem: Nil pointer in method KfObject3D.setPoint.');
  pointData^[index] := aPoint;
  end;

procedure KfObject3D.clear;
  begin
  self.clearPoints;
  name := '';
  end;

procedure KfObject3D.clearPoints;
  begin
  pointsInUse := 0;
  originPointIndex := 0;
  triangles.clear;
  end;

procedure KfObject3D.copyFrom(original: KfObject3D);
  var
    i: integer;
    theTriangle: KfIndexTriangle;
  begin
  if original = nil then exit;
  self.setName(original.name);
  self.ensureEnoughSpaceForNewPointData(original.pointsInUse);
  if original.pointsInUse > 0 then
    for i := 0 to original.pointsInUse - 1 do
      points[i] := original.points[i];
  self.pointsInUse := original.pointsInUse;
  self.originPointIndex := original.originPointIndex;
  triangles.clear;
  if original.triangles.count > 0 then
    for i := 0 to original.triangles.count - 1 do
      begin
      theTriangle := original.triangles.items[i];
      self.addTriangle(KfIndexTriangle.createABC(
        theTriangle.pointIndexes[0], theTriangle.pointIndexes[1], theTriangle.pointIndexes[2]));
      end;
  inUse := original.inUse;
  end;

function KfObject3D.isSameAs(other: KfObject3D): boolean;
  var
    i: longint;
    j: longint;
    thePoint: KfPoint3d;
    theTriangle: KfIndexTriangle;
    otherPoint: KfPoint3d;
    otherTriangle: KfIndexTriangle;
  begin
  {false if fails any test}
  result := false;
  if self.name <> other.name then exit;
  if self.pointsInUse <> other.pointsInUse then exit;
  if self.originPointIndex <> other.originPointIndex then exit;
  if self.triangles.count <> other.triangles.count then exit;
  if self.pointsInUse > 0 then
    for i := 0 to self.pointsInUse - 1 do
      begin
      thePoint := self.points[i];
      otherPoint := other.points[i];
      // round these because otherwise i/o inaccuracies could make a tdo seem different when it isn't,
      // and most numbers are far enough to be integers anyway
      if (round(thePoint.x) <> round(otherPoint.x))
        or (round(thePoint.y) <> round(otherPoint.y))
        or (round(thePoint.z) <> round(otherPoint.z)) then
        exit;
      end;
  if self.triangles.count > 0 then
    for i := 0 to self.triangles.count - 1 do
      begin
      theTriangle := self.triangles.items[i];
      otherTriangle := other.triangles.items[i];
      for j := 0 to 2 do
        if theTriangle.pointIndexes[j] <> otherTriangle.pointIndexes[j] then exit;
      end;
  {passed all the tests}
  result := true;
  end;

function KfObject3D.getName: string;
  begin
  result := self.name;
  end;

procedure KfObject3D.setName(newName: string);
  begin
  name := copy(newName, 1, 80);
  end;

function KfObject3D.addPoint(const aPoint: KfPoint3d): smallint;
  begin
  // v2.0 removed this check
  //if pointsInUse >= kMaximumRecordedPoints then
  //  raise Exception.create('Problem: Too many points in 3D object.');
  self.ensureEnoughSpaceForNewPointData(self.pointsInUse + 1);
  self.points[self.pointsInUse] := aPoint;
  inc(self.pointsInUse);
  result := self.pointsInUse;
  end;

procedure KfObject3D.removePoint(point: smallint);
  var i: smallint;
  begin
  if point <= pointsInUse - 2 then
    for i := point to pointsInUse - 2 do
      points[i] := points[i+1];
  self.deletePointIndexInTriangles(point);
  // never releasing memory until entire object freed
  dec(self.pointsInUse);
  if originPointIndex > pointsInUse - 1 then originPointIndex := pointsInUse - 1;
  end;

function KfObject3D.addPointIfNoMatch(const aPoint: KfPoint3d; matchDistance: single): smallint;
  var
    i: smallint;
  begin
  if pointsInUse > 0 then for i := 0 to pointsInUse - 1 do
    begin
    if KfPoint3D_matchXYZ(aPoint, points[i], matchDistance) then
      begin
      result := i + 1; {add 1 because triangle indexes start at 1}
      exit;
      end;
    end;
  result := self.addPoint(aPoint);
  end;

{PDF FIX - may want to optimize this to use var to pass around result rather than assign}
function KfObject3D.pointForIndex(anIndex: longint): KfPoint3D;
	begin
	if (anIndex < 1) or (anIndex > self.pointsInUse) then
  	raise Exception.create('Problem: Point index out of range in method KfObject3D.pointForIndex.');
  result := self.points[anIndex - 1];
  end;

procedure KfObject3D.addTriangle(aTriangle: KfIndexTriangle);
  begin
  self.triangles.add(aTriangle);
  end;

function KfObject3D.triangleForIndex(anIndex: longint): KfIndexTriangle;
	begin
	if (anIndex < 1) or (anIndex > self.triangles.count)then
  	raise Exception.create('Problem: Triangle index out of range in method KfObject3D.triangleForIndex.');
  result := self.triangles.items[anIndex - 1];
  end;

{adjust all points for origin, which is assumed to be at the first point}
{in terms of plant organs, this means the first point is
where the organ is attached to the plant}
procedure KfObject3D.adjustForOrigin;
  var
    i: longint;
    tempPoint: KfPoint3d;
  begin
  if pointsInUse < 1 then exit;
  if originPointIndex < 0 then originPointIndex := 0;
  if originPointIndex > pointsInUse - 1 then originPointIndex := pointsInUse - 1;
  if pointsInUse > 1 then for i := 0 to pointsInUse - 1 do
    if i <> originPointIndex then
      begin
      tempPoint := self.points[i];
      KfPoint3D_subtract(tempPoint, self.points[originPointIndex]);
      self.points[i] := tempPoint;
      end;
  {makes the first point zero}
  tempPoint := self.points[originPointIndex];
  KfPoint3D_setXYZ(tempPoint, 0.0, 0.0, 0.0);
  self.points[originPointIndex] := tempPoint;
  end;

procedure KfObject3D.setOriginPointIndex(newOriginPointIndex: integer);
  var changed: boolean;
  begin
  changed := (originPointIndex <> newOriginPointIndex);
  originPointIndex := newOriginPointIndex;
  if changed then
    self.adjustForOrigin;
  end;

procedure KfObject3D.makeMirrorTriangles;
  var
    triangleCountAtStart: smallint;
    newPointIndexes: array[0..2] of smallint;
    i, j: smallint;
    aPoint: KfPoint3D;
    triangle: KfIndexTriangle;
  begin
  self.adjustForOrigin;
  triangleCountAtStart := self.triangles.count;
  if triangleCountAtStart > 0 then for i := 0 to triangleCountAtStart - 1 do
    begin
    triangle := KfIndexTriangle(triangles[i]);
    for j := 0 to 2 do
      begin
      aPoint := self.pointForIndex(triangle.pointIndexes[j]);
      aPoint.x := -1 * aPoint.x;
      newPointIndexes[j] := self.addPointIfNoMatch(aPoint, 1.0);
      end;
    // reversing order of points makes triangle have correct facing for opposite side
    self.addTriangle(KfIndexTriangle.createABC(newPointIndexes[2], newPointIndexes[1], newPointIndexes[0]));
    end;
  end;

procedure KfObject3D.reverseZValues;
  var
    i: smallint;
    tempPoint: KfPoint3d;
  begin
  self.adjustForOrigin;
  if pointsInUse > 0 then for i := 0 to pointsInUse - 1 do
    begin
    tempPoint := points[i];
    tempPoint.z := -1 * tempPoint.z;
    points[i] := tempPoint;
    end;
  end;

function KfObject3D.bestPointForDrawingAtScale(turtleProxy: TObject; origin: TPoint; bitmapSize: TPoint; scale: single): TPoint;
	var
  	i: longint;
    turtle: KfTurtle;
  begin
  turtle := KfTurtle(turtleProxy);
  boundsRect := rect(0, 0, 0, 0);
  turtle.reset;
  if pointsInUse > 0 then
  	for i := 0 to pointsInUse - 1 do
    	KfPoint3D_addPointToBoundsRect(self.boundsRect, turtle.transformAndRecord(self.points[i], scale));
  result.x := origin.x + bitmapSize.x div 2 - rWidth(boundsRect) div 2 - boundsRect.left;
  result.y := origin.y + bitmapSize.y div 2 - rHeight(boundsRect) div 2 - boundsRect.top;
  end;

function KfObject3D.draw(turtleProxy: TObject; scale: single;
    longName: string; shortName: string; dxfIndex: smallint; partID: longint): TRect;
	var
  	i: longint;
    triangle: KfIndexTriangle;
    realTriangle: KfTriangle;
    turtle: KfTurtle;
    minZ: single;
  begin
  result := Rect(0, 0, 0, 0);
  minZ := 0;
  zForSorting := 0;
  turtle := KfTurtle(turtleProxy);
  if turtle.ifExporting_exclude3DObject(scale) then exit;
  turtle.clearRecording;
  boundsRect := rect(0, 0, 0, 0);
  if pointsInUse > 0 then
  	for i := 0 to pointsInUse - 1 do
      KfPoint3D_addPointToBoundsRect(self.boundsRect, turtle.transformAndRecord(self.points[i], scale));
  result := self.boundsRect;
  if not turtle.drawOptions.draw3DObjects then exit;
  if turtle.drawOptions.draw3DObjectsAsRects then
    begin
    turtle.drawTrianglesFromBoundsRect(boundsRect);
    exit;
    end;
  // prepare
  turtle.ifExporting_start3DObject(longName + ' 3D object', shortName, turtle.drawingSurface.foreColor, dxfIndex);
  // draw
  if turtle.exportingToFile then
    self.write3DExportElements(turtle, scale, partID)
  else if triangles.count > 0 then
  	for i := 1 to triangles.count do
      begin
      triangle := triangleForIndex(i);
    	realTriangle := turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[1], triangle.pointIndexes[2], partID);
      if (turtle.drawOptions.sortPolygons) and (turtle.drawOptions.sortTdosAsOneItem)
        and (realTriangle <> nil) then
        begin
        if i = 1 then
          minZ := realTriangle.zForSorting
        else if realTriangle.zForSorting < minZ then
          minZ := realTriangle.zForSorting;
        realTriangle.tdo := self;
        end;
      end;
  zForSorting := minZ;
  turtle.ifExporting_end3DObject;
  end;

procedure KfObject3D.overlayBoundsRect(turtleProxy: TObject; scale: single);
	var
  	i: longint;
    turtle: KfTurtle;
    oldSetting: boolean;
  begin
  turtle := KfTurtle(turtleProxy);
  oldSetting := turtle.drawingSurface.fillingTriangles;
  turtle.drawingSurface.fillingTriangles := false;
  turtle.drawTrianglesFromBoundsRect(self.boundsRect);
  turtle.drawingSurface.fillingTriangles := oldSetting;
  end;

procedure KfObject3D.write3DExportElements(turtleProxy: TObject; scale: single; partID: smallint);
  var
    fileExportSurface: KfFileExportSurface;
    i: smallint;
    turtle: KfTurtle;
    triangle: KfIndexTriangle;
    firstPtIndex: longint;
  begin
  // do NOT pass the array on because a tdo could be really big
  // some write out lists of points then triangles; some draw each triangle
  turtle := KfTurtle(turtleProxy);
  fileExportSurface := turtle.fileExportSurface;
  if fileExportSurface = nil then
    raise Exception.create('Problem: No 3D drawing surface in method KfObject3D.write3DExportElements.');
  case turtle.writingTo of
    k3DS, kOBJ, kVRML, kLWO:
      begin
      fileExportSurface.startVerticesAndTriangles;
      if turtle.writingToLWO then
        firstPtIndex := fileExportSurface.numPoints
      else
        firstPtIndex := 0;
      if pointsInUse > 0 then
  	    for i := 0 to pointsInUse - 1 do
    	    fileExportSurface.addPoint(turtle.transformAndRecord(self.points[i], scale));
      for i := 1 to triangles.count do
        begin
        triangle := triangleForIndex(i);
        fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0]-1,
            firstPtIndex + triangle.pointIndexes[1]-1, firstPtIndex + triangle.pointIndexes[2]-1);
        if fileExportSurface.options.makeTrianglesDoubleSided then
          fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0]-1,
              firstPtIndex + triangle.pointIndexes[2]-1, firstPtIndex + triangle.pointIndexes[1]-1);
        end;
      fileExportSurface.endVerticesAndTriangles;
      // PDF PORT -- added semicolon
      end;
    else
      begin
  	  for i := 1 to triangles.count do
        begin
        triangle := triangleForIndex(i);
    	  turtle.drawTriangleFromIndexes(triangle.pointIndexes[0],
            triangle.pointIndexes[1], triangle.pointIndexes[2], partID);
        if fileExportSurface.options.makeTrianglesDoubleSided then
    	    turtle.drawTriangleFromIndexes(triangle.pointIndexes[0],
              triangle.pointIndexes[2], triangle.pointIndexes[1], partID);
        end;
      end;
    end;
  end;

procedure KfObject3D.addTriangleWithVerticesABC(a: longint; b: longint; c: longint);
	begin
  self.addTriangle(KfIndexTriangle.createABC(a, b, c));
  end;

procedure KfObject3D.removeTriangle(aTriangle: KfIndexTriangle);
  begin
  triangles.remove(aTriangle);
  self.removePointsNotInUse;
  end;

procedure KfObject3D.removePointsNotInUse;
  var
    i, pointToRemove: smallint;
    done: boolean;
  begin
  if pointsInUse <= 0 then exit;
  done := false;
  while not done do
    begin
    pointToRemove := -1;
    for i := 0 to pointsInUse - 1 do
      if not self.pointIsReallyInUse(i) then
        begin
        pointToRemove := i;
        break;
        end;
    if pointToRemove >= 0 then
      self.removePoint(pointToRemove)
    else
      done := true;
    end;
  end;

function KfObject3D.pointIsReallyInUse(point: smallint): boolean;
  var
    triangle: KfIndexTriangle;
    i, j, adjustedPoint: smallint;
  begin
  result := false;
  { triangle indexes start at 1, not 0 }
  adjustedPoint := point + 1;
  if triangles.count > 0 then for i := 0 to triangles.count - 1 do
    begin
    triangle := KfIndexTriangle(triangles.items[i]);
    for j := 0 to 2 do
      if triangle.pointIndexes[j] = adjustedPoint then
        begin
        result := true;
        exit;
        end;
    end;
  end;

procedure KfObject3D.deletePointIndexInTriangles(oldPointIndex: smallint);
  var
    triangle: KfIndexTriangle;
    i, j, adjustedOldPointIndex: smallint;
  begin
  { triangle indexes start at 1, not 0 }
  adjustedOldPointIndex := oldPointIndex + 1;
  if triangles.count > 0 then for i := 0 to triangles.count - 1 do
    begin
    triangle := KfIndexTriangle(triangles.items[i]);
    for j := 0 to 2 do
      if triangle.pointIndexes[j] > adjustedOldPointIndex then
        triangle.pointIndexes[j] := triangle.pointIndexes[j] - 1;
    end;
  end;

{parse string into xyz positions and add point to collection}
procedure KfObject3D.addPointString(stream: KfStringStream);
  var
    aPoint3D: KfPoint3D;
    x,y,z: integer;
	begin
  x := 0; y := 0; z := 0;
  x := stream.nextInteger;
  y := stream.nextInteger;
  z := stream.nextInteger;
  KfPoint3d_setXYZ(aPoint3D, x, y, z);
  self.addPoint(aPoint3D);
  end;

{parse string into three point indexes and add triangle to collection}
procedure KfObject3D.addTriangleString(stream: KfStringStream);
  var
    p1, p2, p3: integer;
  begin
  p1 := 0; p2 := 0; p3 := 0;
  p1 := stream.nextInteger;
  p2 := stream.nextInteger;
  p3 := stream.nextInteger;
  if (p1 = 0) or (p2 = 0) or (p3 = 0)
    or (p1 > pointsInUse) or (p2 > pointsInUse) or (p3 > pointsInUse) then
    messageDlg('Bad triangle: ' + intToStr(p1) + ' ' + intToStr(p2) + ' ' + intToStr(p3)
        + '. Point indexes must be between 1 and ' + intToStr(pointsInUse) + '.', mtError, [mbOK], 0)
  else
    self.addTriangle(KfIndexTriangle.createABC(p1, p2, p3));
  end;

procedure KfObject3D.writeToFile(fileName: string);
	var
  	outputFile: TextFile;
   begin
  assignFile(outputFile, fileName);
  try
    setDecimalSeparator; // v1.5
    rewrite(outputFile);
    self.writeToFileStream(outputFile, kStandAloneFile);
  finally
    closeFile(outputFile);
  end;
  end;

procedure KfObject3D.readFromFile(fileName: string);
	var
  	inputFile: TextFile;
   begin
  assignFile(inputFile, fileName);
  try
    setDecimalSeparator; // v1.5
    reset(inputFile);
    self.readFromFileStream(inputFile, kStandAloneFile);
  finally
    closeFile(inputFile);
  end;
  end;

function betweenBrackets(aString: string): string;
  begin
  { lose letter and [ on front, lose ] on back }
  result := copy(aString, 3, length(aString) - 3);
  end;

procedure KfObject3D.writeToMemo(aMemo: TMemo);
	var
    i: smallint;
    triangle: KfIndexTriangle;
  begin
  aMemo.lines.add('  ' + kStartTdoString);
  aMemo.lines.add('  Name=' + self.getName);
  if self.pointsInUse > 0 then
    for i := 0 to self.pointsInUse - 1 do
      aMemo.lines.add('  Point='
          + intToStr(round(points[i].x)) + ' ' + intToStr(round(points[i].y)) + ' '
          + intToStr(round(points[i].z)));
  aMemo.lines.add('; Origin=' + intToStr(originPointIndex));
  if triangles.count > 0 then
    for i := 0 to triangles.count - 1 do
      begin
      triangle := KfIndexTriangle(triangles[i]);
      aMemo.lines.add('  Triangle='
          + intToStr(triangle.pointIndexes[0]) + ' ' + intToStr(triangle.pointIndexes[1]) + ' '
          + intToStr(triangle.pointIndexes[2]));
      end;
  aMemo.lines.add('  ' + kEndTdoString)
  end;

procedure KfObject3D.writeToFileStream(var outputFile: TextFile; embeddedInPlant: boolean);
	var
    i: smallint;
    triangle: KfIndexTriangle;
  begin
  if embeddedInPlant then
    writeln(outputFile, '  ' + kStartTdoString);
  if embeddedInPlant then
    write(outputFile, '  ');
  writeln(outputFile, 'Name=' + self.getName);
  if self.pointsInUse > 0 then
    for i := 0 to self.pointsInUse - 1 do
      writeln(outputFile, '  Point='
          + intToStr(round(points[i].x)) + ' ' + intToStr(round(points[i].y)) + ' '
          + intToStr(round(points[i].z)));
  writeln(outputFile, '; Origin=' + intToStr(originPointIndex));
  if triangles.count > 0 then
    for i := 0 to triangles.count - 1 do
      begin
      triangle := KfIndexTriangle(triangles[i]);
      writeln(outputFile, '  Triangle='
          + intToStr(triangle.pointIndexes[0]) + ' ' + intToStr(triangle.pointIndexes[1]) + ' '
          + intToStr(triangle.pointIndexes[2]));
      end;
  if embeddedInPlant then
    writeln(outputFile, '  ' + kEndTdoString)
  else
    writeln(outputFile);
  end;

procedure KfObject3D.readFromFileStream(var inputFile: TextFile; embeddedInPlant: boolean);
	var
  	inputLine: string;
    fieldType: string;
    stream: KfStringStream;
  begin
  pointsInUse := 0;
  originPointIndex := 0;
  triangles.clear;
  if embeddedInPlant then
    begin
    readln(inputFile, inputLine);
    // cfk change for v1.3 added '' case
    if (embeddedInPlant) and (trim(inputLine) = '') then readln(inputFile, inputLine);
    // cfk change for v1.6b2 mistake with origin, placed with comment
    if (copy(inputLine, 1, 1) = ';') and (pos('ORIGIN', upperCase(inputLine)) <= 0) then
      readln(inputFile, inputLine);
    if pos(upperCase(kStartTdoString), upperCase(inputLine)) <= 0 then
      raise Exception.create('Problem: Expected start of 3D object.');
    end;
  stream := nil;
  try
    {read info for 3D object from file at current position}
    stream := KfStringStream.create;
	  while not eof(inputFile) do
      begin
      readln(inputFile, inputLine);
      // cfk change v1.3 added '' case
      if (embeddedInPlant) and (trim(inputLine) = '') then continue;
      // cfk change for v1.6b2 mistake with origin, placed with comment
      if (copy(inputLine, 1, 1) = ';') and (pos('ORIGIN', upperCase(inputLine)) <= 0) then
        continue;
      if (not embeddedInPlant) and (pos('[', inputLine) = 1) then continue; {ignore old thing in brackets}
      stream.onStringSeparator(inputLine, '=');
      fieldType := stream.nextToken;
      stream.spaceSeparator;
      if pos('POINT', upperCase(fieldType)) > 0 then
        self.addPointString(stream)
      else if pos('ORIGIN', upperCase(fieldType)) > 0 then
        self.setOriginPointIndex(strToIntDef(stream.remainder, 0))       
      else if pos('TRIANGLE', upperCase(fieldType)) > 0 then
        self.addTriangleString(stream)
      else if pos('NAME', upperCase(fieldType)) > 0 then
        self.setName(stream.remainder)
      else
        break;
      end;
  self.adjustForOrigin;
  if embeddedInPlant then
    if pos(upperCase(kEndTdoString), upperCase(inputLine)) <= 0 then
      raise Exception.create('Problem: Expected end of 3D object.');
  finally
    stream.free;
  end;
  end;

procedure KfObject3D.readFromDXFFile(var inputFile: TextFile);
	var
  	identifierLine, valueLine: string;
    newPoints: array[0..2] of KfPoint3D;
    newTriangleIndexes: array[0..2] of integer;
    pointsRead: integer;
  begin
  pointsInUse := 0;
  originPointIndex := 0;
  pointsRead := 0;
  triangles.clear;
  newPoints[0].x := 0; newPoints[0].y := 0; newPoints[0].z := 0;
  newPoints[1].x := 0; newPoints[1].y := 0; newPoints[1].z := 0;
  newPoints[2].x := 0; newPoints[2].y := 0; newPoints[2].z := 0;
  while not eof(inputFile) do
    begin
    readln(inputFile, identifierLine); identifierLine := trim(identifierLine);
    readln(inputFile, valueLine); valueLine := trim(valueLine);
    // v1.60final changed this from else to all ifs; something wrong in Delphi, I think
    // first point
    if identifierLine = '10' then newPoints[0].x := strToFloat(valueLine);
    if identifierLine = '20' then newPoints[0].y := -1 * strToFloat(valueLine);
    if identifierLine = '30' then newPoints[0].z := strToFloat(valueLine);
    // second point
    if identifierLine = '11' then newPoints[1].x := strToFloat(valueLine);
    if identifierLine = '21' then newPoints[1].y := -1 * strToFloat(valueLine);
    if identifierLine = '31' then newPoints[1].z := strToFloat(valueLine);
    // third point
    if identifierLine = '12' then newPoints[2].x := strToFloat(valueLine);
    if identifierLine = '22' then newPoints[2].y := -1 * strToFloat(valueLine);
    if identifierLine = '32' then newPoints[2].z := strToFloat(valueLine);
    // end (ignoring fourth point)
    if identifierLine = '13' then
      begin
      inc(pointsRead, 3);
      // make new triangle
      newTriangleIndexes[0] := self.addPointIfNoMatch(newPoints[0], 0.1);
      newTriangleIndexes[1] := self.addPointIfNoMatch(newPoints[1], 0.1);
      newTriangleIndexes[2] := self.addPointIfNoMatch(newPoints[2], 0.1);
      self.addTriangle(KfIndexTriangle.createABC(newTriangleIndexes[0], newTriangleIndexes[1], newTriangleIndexes[2]));
      // reset points for next time
      newPoints[0].x := 0; newPoints[0].y := 0; newPoints[0].z := 0;
      newPoints[1].x := 0; newPoints[1].y := 0; newPoints[1].z := 0;
      newPoints[2].x := 0; newPoints[2].y := 0; newPoints[2].z := 0;
      end;
    end;
  self.adjustForOrigin;
  end;

procedure KfObject3D.readFromMemo(aMemo: TMemo; var readingMemoLine: longint);
	var
  	inputLine: string;
    fieldType: string;
    stream: KfStringStream;
  begin
  pointsInUse := 0;
  originPointIndex := 0;
  triangles.clear;
  inputLine := aMemo.lines.strings[readingMemoLine];
  inc(readingMemoLine);
  // cfk change v1.60final added '' case
  if trim(inputLine) = '' then
    begin
    inputLine := aMemo.lines.strings[readingMemoLine]; { skip commented lines }
    inc(readingMemoLine);
    end;
  // cfk change for v1.6b2 mistake with origin, placed with comment
  if (copy(inputLine, 1, 1) = ';') and (pos('ORIGIN', upperCase(inputLine)) <= 0) then
    begin
    inputLine := aMemo.lines.strings[readingMemoLine]; { skip commented lines }
    inc(readingMemoLine);
    end;
  if pos(upperCase(kStartTdoString), upperCase(inputLine)) <= 0 then
    raise Exception.create('Problem: Expected start of 3D object.');
  stream := nil;
  try
    {read info for 3D object from file at current position}
    stream := KfStringStream.create;
	  while readingMemoLine <= aMemo.lines.count - 1 do
      begin
      inputLine := aMemo.lines.strings[readingMemoLine];
      inc(readingMemoLine);
      // cfk change v1.60final added '' case
      if trim(inputLine) = '' then continue;
      // cfk change for v1.6b2 mistake with origin, placed with comment
      if (copy(inputLine, 1, 1) = ';') and (pos('ORIGIN', upperCase(inputLine)) <= 0) then
        continue; { skip commented lines }
      stream.onStringSeparator(inputLine, '=');
      fieldType := stream.nextToken;
      stream.spaceSeparator;
      if pos('POINT', upperCase(fieldType)) > 0 then
        self.addPointString(stream)
      else if pos('ORIGIN', upperCase(fieldType)) > 0 then
        self.setOriginPointIndex(strToIntDef(stream.remainder, 0))
      else if pos('TRIANGLE', upperCase(fieldType)) > 0 then
        self.addTriangleString(stream)
      else if pos('NAME', upperCase(fieldType)) > 0 then
        self.setName(stream.remainder)
      else
        break;
      end;
  self.adjustForOrigin;
  if pos(upperCase(kEndTdoString), upperCase(inputLine)) <= 0 then
    raise Exception.create('Problem: Expected end of 3D object.');
  finally
    stream.free;
  end;
  end;

procedure KfObject3D.readFromInputString(aString: string; doAdjustForOrigin: boolean);
	var
  	part, firstLetter: string;
    stream, partStream: KfStringStream;
  begin
  { format is n[name],p[# # #],p[# # #],p[# # #],t[# # #],t[# # #],t[# # #] }
  pointsInUse := 0;
  originPointIndex := 0;
  triangles.clear;
  stream := KfStringStream.create;
  partStream := KfStringStream.create;
  try
    stream.onStringSeparator(aString, ',');
    part := 'none';
    while part <> '' do
      begin
      part := stream.nextToken;
      firstLetter := copy(part, 1, 1);
      if upperCase(firstLetter) = 'N' then
        self.setName(betweenBrackets(part))
      else if upperCase(firstLetter) = 'P' then
        begin
        partStream.onStringSeparator(betweenBrackets(part), ' ');
        self.addPointString(partStream);
        end
      else if upperCase(firstLetter) = 'T' then
        begin
        partStream.onStringSeparator(betweenBrackets(part), ' ');
        self.addTriangleString(partStream);
        end;
    end;
    if doAdjustForOrigin then
      self.adjustForOrigin;
  finally
    stream.free;
    partStream.free;
  end;
  end;

{ ------------------------------------------------------------------------- data transfer for binary copy }
procedure KfObject3D.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kKfObject3D;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure KfObject3D.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  var
    i: smallint;
    tempPoint: KfPoint3d;
	begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
    streamShortString(name);
    streamLongint(pointsInUse);
    streamLongint(originPointIndex);
    self.ensureEnoughSpaceForNewPointData(pointsInUse);
    if pointsInUse > 0 then for i := 0 to pointsInUse - 1 do
      begin
      if isWriting then tempPoint := points[i];
		  streamBytes(tempPoint, sizeOf(tempPoint));
      if isReading then points[i] := tempPoint;
      end;
    if isReading then triangles.clear; {may have triangles already, because we are keeping them around now}
    triangles.streamUsingFiler(filer, KfIndexTriangle);
    end;
  end;

function KfObject3D.totalMemorySize: longint;
  var i: longint;
  begin
  result := self.instanceSize;
  result := result + triangles.instanceSize;
  if triangles.count > 0 then
    for i := 0 to triangles.count - 1 do
      result := result + KfIndexTriangle(triangles.items[i]).instanceSize;
  result := result +  self.pointsAllocated * sizeof(KfPoint3D);
  end;

procedure KfObject3D.writeToDXFFile(fileName: string; frontFaceColor, backFaceColor: TColorRef);
	var
  	outputFile: TextFile;
    i: smallint;
    triangle: KfIndexTriangle;
    colorToDraw: TColorRef;
   begin
  assignFile(outputFile, fileName);
  try
    setDecimalSeparator; // v1.5
    rewrite(outputFile);
    writeln(outputFile, '0'); writeln(outputFile, 'SECTION');
    writeln(outputFile, '2'); writeln(outputFile, 'ENTITIES');
    for i := 0 to triangles.count - 1 do
      begin
      triangle := KfIndexTriangle(triangles.items[i]);
      if self.triangleIsBackFacing(triangle) then
        colorToDraw := backFaceColor
      else
        colorToDraw := frontFaceColor;
      self.writeTriangleToDXFFIle(outputFile, points[triangle.pointIndexes[0]-1],
          points[triangle.pointIndexes[1]-1],points[triangle.pointIndexes[2]-1], colorToDraw);
      end;
    writeln(outputFile, '0'); writeln(outputFile, 'ENDSEC');
    writeln(outputFile, '0'); writeln(outputFile, 'EOF');
  finally
    closeFile(outputFile);
  end;
  end;

procedure KfObject3D.writeTriangleToDXFFIle(var outputFile: TextFile; p1, p2, p3: KfPoint3D; color: TColorRef);
  begin
  writeln(outputFile, '0');   writeln(outputFile, '3DFACE');
  writeln(outputFile, '8');   writeln(outputFile, '3dObject');
  writeln(outputFile, '62');  writeln(outputFile, intToStr(color));
  // v1.60final changed intToStr(round(p|.|)) to digitValueString(p|.|)
  // can't see that there was ever any reason to round these; it's probably left over from
  // when I didn't understand DXF very well
  writeln(outputFile, '10');  writeln(outputFile, digitValueString(p1.x));
  writeln(outputFile, '20');  writeln(outputFile, digitValueString(-p1.y));
  writeln(outputFile, '30');  writeln(outputFile, digitValueString(p1.z));
  writeln(outputFile, '11');  writeln(outputFile, digitValueString(p2.x));
  writeln(outputFile, '21');  writeln(outputFile, digitValueString(-p2.y));
  writeln(outputFile, '31');  writeln(outputFile, digitValueString(p2.z));
  writeln(outputFile, '12');  writeln(outputFile, digitValueString(p3.x));
  writeln(outputFile, '22');  writeln(outputFile, digitValueString(-p3.y));
  writeln(outputFile, '32');  writeln(outputFile, digitValueString(p3.z));
  writeln(outputFile, '13');  writeln(outputFile, digitValueString(p3.x));
  writeln(outputFile, '23');  writeln(outputFile, digitValueString(-p3.y));
  writeln(outputFile, '33');  writeln(outputFile, digitValueString(p3.z));
  end;

procedure KfObject3D.writeToPOV_INCFile(fileName: string; frontFaceColor: TColorRef; embeddedInPlant: boolean;
    rotateCount: integer);
	var
  	outputFile: TextFile;
    i: smallint;
    triangle: KfIndexTriangle;
    colorToDraw: TColorRef;
    nameString: string;
   begin
  assignFile(outputFile, fileName);
  try
    setDecimalSeparator; // v1.5
    rewrite(outputFile);
    nameString := replacePunctuationWithUnderscores(self.getName);
    writeln(outputFile, '// POV-format INC file of PlantStudio v1.x 3D object');
    writeln(outputFile, '//     "' + self.getName + '"');
    if (not embeddedInPlant) then
      begin
      writeln(outputFile, '// include this file in a POV file thus to use it:');
      writeln(outputFile, '//     #include "' + stringUpTo(extractFileName(fileName), '.') + '.inc"');
      writeln(outputFile, '//     object { ' + nameString + ' }');
      if rotateCount > 1 then
        begin
        writeln(outputFile, '//  or');
      writeln(outputFile, '//     object { ' + nameString + '_rotated }');
        end;
      writeln(outputFile);
      end;
    writeln(outputFile, '#declare ' + nameString + '=mesh {');
    for i := 0 to triangles.count - 1 do
      begin
      triangle := KfIndexTriangle(triangles.items[i]);
      self.writeTriangleToPOV_INCFIle(outputFile, points[triangle.pointIndexes[0]-1],
          points[triangle.pointIndexes[1]-1], points[triangle.pointIndexes[2]-1]);
      end;
    writeln(outputFile, chr(9) + 'pigment { color rgb <'
      + digitValueString(getRValue(frontFaceColor) / 256.0) + ', '
      + digitValueString(getGValue(frontFaceColor) / 256.0) + ', '
      + digitValueString(getBValue(frontFaceColor) / 256.0) + '> }');
    writeln(outputFile, '}');
    if rotateCount > 1 then
      begin
      writeln(outputFile);
      writeln(outputFile, '#declare ' + nameString + '_rotated=union {');
      writeln(outputFile, chr(9) + 'object { ' + nameString + ' }');
      for i := 1 to rotateCount - 1 do
        writeln(outputFile, chr(9) + 'object { ' + nameString
          + ' rotate ' + intToStr(i) + '*365/' + intToStr(rotateCount) + '*y }');
      writeln(outputFile, '}');
      end;
  finally
    closeFile(outputFile);
  end;
  end;

procedure KfObject3D.writeTriangleToPOV_INCFIle(var outputFile: TextFile; p1, p2, p3: KfPoint3D);
  begin
  write(outputFile, chr(9) + 'triangle { <');
  // all y values must be negative because it seems our coordinate systems are different
  write(outputFile, intToStr(round(p1.x)) + ', ' + intToStr(-round(p1.y)) + ', ' + intToStr(round(p1.z)) + '>, <');
  write(outputFile, intToStr(round(p2.x)) + ', ' + intToStr(-round(p2.y)) + ', ' + intToStr(round(p2.z)) + '>, <');
  writeln(outputFile, intToStr(round(p3.x)) + ', ' + intToStr(-round(p3.y)) + ', ' + intToStr(round(p3.z)) + '> }');
  end;

function KfObject3D.triangleIsBackFacing(aTriangle: KfIndexTriangle): boolean;
  var
    point0, point1, point2: KfPoint3d;
    backfacingResult: single;
  begin
  result := false;
  point0 := points[aTriangle.pointIndexes[0]-1];
  point1 := points[aTriangle.pointIndexes[1]-1];
  point2 := points[aTriangle.pointIndexes[2]-1];
  backfacingResult := ((point1.x - point0.x) * (point2.y - point0.y)) -
  		((point1.y - point0.y) * (point2.x - point0.x));
  result := (backfacingResult < 0);
  end;



end.
(* not using
procedure KfObject3D.insertPoint(newPointIndex: smallint; newPoint: KfPoint3d);
  var
    i: smallint;
  begin
  inc(pointsInUse);
  if newPointIndex <= pointsInUse - 1 then for i := newPointIndex to pointsInUse - 1 do
    begin
    self.changePointIndexInTriangles(i+1, i);
    points[i+1] := points[i];
    end;
  points[newPointIndex] := newPoint;
  end;
*)

    (*
    writeln(outputFile, '#declare camera_' + nameString + '= camera {');
    writeln(outputFile, chr(9) + 'location  <0, 0, ' + intToStr(round(lowestZ)) + '>');
    writeln(outputFile, chr(9) + 'look_at <'
      + intToStr(round(totalX / (triangles.count * 3)))
      + ', ' + intToStr(round(totalY / (triangles.count * 3)))
      + ', ' + intToStr(round(totalZ / (triangles.count * 3))) + '>');
    writeln(outputFile, chr(9) + 'angle 90');
    writeln(outputFile, '}');
    *)



