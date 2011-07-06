unit Uturtle;

interface

uses Windows, Graphics, Forms, Dialogs, SysUtils, Classes, {OpenGL,}
  ucollect, utdo, udrawingsurface, u3dsupport, u3dexport;

{if this is defined - turtle will draw axis marks for each line segment}
{put spaces before and after the $ to disable}
{ $ DEFINE DEBUG_TURTLE}

const

  kInitialTurtleMatrixStackDepth = 250;

type

  PlantDrawOptionsStructure = record
    { general options }
    sortPolygons: boolean;
    drawLines: boolean;
    lineContrastIndex: smallint;
    { speed optimizations }
    wireFrame: boolean;
    straightLinesOnly: boolean;
    simpleLeavesOnly: boolean;
    drawStems: boolean;
    draw3DObjects: boolean;
    draw3DObjectsAsRects: boolean;
    circlePoints: boolean;
    circlePointRadius: smallint;
    sortTdosAsOneItem: boolean;
    drawingToMainWindow: boolean;
    drawBoundsRectsOnPlantParts: boolean;
    end;

  {PDF FIX - may want to think about size of recorded points}
	KfTurtle = class(TObject)
  	public
    matrixStack: TListCollection;
    numMatrixesUsed: longint;
    currentMatrix: KfMatrix;
    recordedPoints: array[0..kMaximumRecordedPoints] of KfPoint3d;
    recordedPointsInUse: longint;
    scale_pixelsPerMm: single;
    drawingSurface: KfDrawingSurface;
    tempPosition: KfPoint3d;
    realBoundsRect: TRealRect;
    drawOptions: PlantDrawOptionsStructure;
    writingTo: smallint;
		constructor create;
		destructor destroy; override;
    class function defaultStartUsing: KfTurtle;
    class procedure defaultStopUsing;
    class procedure defaultAllocate;
    class procedure defaultFree;
    function boundsRect: TRect;
    procedure resetBoundsRect(basePoint: TPoint);
    procedure addToRealBoundsRect(const aPoint: KfPoint3d);
		function angleX: byte;
		function angleY: byte;
		function angleZ: byte;
		procedure clearRecording;
		procedure recordPosition;
		procedure recordPositionPoint(const aPoint: KfPoint3D);
		function millimetersToPixels(mm:single): single;
		procedure setScale_pixelsPerMm(newScale_pixelsPerMm: single);
		procedure moveAndRecordScale(const originalPoint3D: KfPoint3D; theScale_pixelsPerMm: single);
		procedure moveInMillimeters(mm: single);
		procedure moveInMillimetersAndRecord(mm: single);
		procedure moveInPixels(pixels: single);
		procedure moveInPixelsAndRecord(pixels: single);
		function positionCopy: KfPoint3D;
		procedure pop;
		procedure push;
		procedure rotateX(angle: single);
		procedure rotateY(angle: single);
		procedure rotateZ(angle: single);
		function stackSize: longint;
		procedure startRecording;
		function transformAndRecord(const originalPoint3D: KfPoint3D; theScale_pixelsPerMm: single): KfPoint3D;
		function newTriangleTriangle(aPointIndex: longint; bPointIndex: longint; cPointIndex: longint): KfTriangle;
		procedure xyz(x: single; y: single; z: single);
    function drawInMillimeters(mm: single; partID: longint): KfTriangle;
    		procedure drawInMillimeters_debug(mm: single); // PDF PORT added to deal with alternatives
		procedure drawInPixels(pixels: single);
		procedure drawTriangle;
		procedure setForeColorBackColor(frontColor: TColor; backColor: TColor);
		function drawTriangleFromIndexes(aPointIndex: longint; bPointIndex: longint; cPointIndex: longint; partID: longint): KfTriangle;
    procedure drawTrianglesFromBoundsRect(boundsRect: TRect);
		function lineColor: TColor;
		procedure setLineColor(aColor: TColor);
		function lineWidth: single;
		procedure setLineWidth(aWidth: single);
    procedure reset;
    procedure setDrawOptionsForDrawingTdoOnly;
    function position: KfPoint3d;
    // 3d file export
    constructor createFor3DOutput(anOutputType: smallint; aFileName: string);
    procedure start3DExportFile;
    procedure end3DExportFile;
    function exportingToFile: boolean;
    function writingToDXF: boolean;
    function writingToPOV: boolean;
    function writingTo3DS: boolean;
    function writingToOBJ: boolean;
    function writingToVRML: boolean;
    function writingToLWO: boolean;
    function fileExportSurface: KfFileExportSurface;
    procedure ifExporting_startNestedGroupOfPlantParts(groupName: string; shortName: string; nestingType: smallint);
    procedure ifExporting_endNestedGroupOfPlantParts(nestingType: smallint);
    procedure ifExporting_startPlantPart(aLongName, aShortName: string);
    procedure ifExporting_endPlantPart;
    function ifExporting_excludeStem(length: single): boolean;
    function ifExporting_exclude3DObject(scale: single): boolean;
    procedure ifExporting_startStemSegment(aLongName: string; aShortName: string;
        color: TColorRef; width: single; index: smallint);
    procedure ifExporting_endStemSegment;
    function ifExporting_stemCylinderFaces: smallint;
    procedure drawFileExportPipeFaces(const startPoints: array of KfPoint3D;
        const endPoints: array of KfPoint3D; faces: smallint; segmentNumber: smallint);
    procedure ifExporting_start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
    procedure ifExporting_end3DObject;
  	end;

implementation

uses usupport, umath, utravers{for darkerColor}, umain, udebug{temp};

{ ---------------------------------------------------------------------------------- *KfTurtle creating/destroying }
var
  gDefaultTurtle: KfTurtle;
  gDefaultTurtleInUse: boolean;

constructor KfTurtle.create;
  var i: longint;
  begin
  inherited create;
  // v1.60final looked at giving hint with plant part name again; still has problem
  // that what you record is only points, and what you need to record is rects
  // it can be done, but the plant parts have to change to record rects, and they
  // have to deal with all their different ways of drawing. not worth doing at this time.
  matrixStack := TListCollection.create;
  currentMatrix := KfMatrix.create;
  currentMatrix.initializeAsUnitMatrix;
  matrixStack.add(currentMatrix);
  numMatrixesUsed := 1;
  {start with a bunch of matrixes}
  for i := 0 to kInitialTurtleMatrixStackDepth do
    matrixStack.add(KfMatrix.create);
  recordedPointsInUse := 0;
  drawingSurface := KfDrawingSurface.create;
  scale_pixelsPerMm := 1.0;
  end;

destructor KfTurtle.destroy;
	begin
  matrixStack.free;
  matrixStack := nil;
  drawingSurface.free;
  drawingSurface := nil;
  inherited destroy;
  end;

constructor KfTurtle.createFor3DOutput(anOutputType: smallint; aFileName: string);
  begin
  self.create;
  drawingSurface.free; {already created}
  drawingSurface := nil;
  case anOutputType of
    kDXF: drawingSurface := KfDrawingSurfaceForDXF.createWithFileName(aFileName);
    kPOV: drawingSurface := KfDrawingSurfaceForPOV.createWithFileName(aFileName);
    k3DS: drawingSurface := KfDrawingSurfaceFor3DS.createWithFileName(aFileName);
    kOBJ: drawingSurface := KfDrawingSurfaceForOBJ.createWithFileName(aFileName);
    kVRML: drawingSurface := KfDrawingSurfaceForVRML.createWithFileName(aFileName);
    kLWO: drawingSurface := KfDrawingSurfaceForLWO.createWithFileName(aFileName);
    else
      raise Exception.create('KfTurtle.createFor3DOutput: Unrecognized output type');
    end;
  end;

procedure KfTurtle.start3DExportFile;
  begin
  if (drawingSurface <> nil) and (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).startFile;
  end;

procedure KfTurtle.end3DExportFile;
  begin
  if (drawingSurface <> nil) and (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).endFile;
  end;

{ -------------------------------------------------------------------------- KfTurtle initializing and setting values }
procedure KfTurtle.reset;
	begin
  numMatrixesUsed := 1;
  currentMatrix := matrixStack.items[0];
  currentMatrix.initializeAsUnitMatrix;
  recordedPointsInUse := 0;
  scale_pixelsPerMm := 1.0;
  if drawingSurface <> nil then
    begin
    drawingSurface.fillingTriangles := not self.drawOptions.wireFrame;
    drawingSurface.drawingLines := self.drawOptions.drawLines;
    drawingSurface.circlingPoints := self.drawOptions.circlePoints;
    drawingSurface.lineContrastIndex := self.drawOptions.lineContrastIndex;
    drawingSurface.circlePointRadius := self.drawOptions.circlePointRadius;
    drawingSurface.sortTdosAsOneItem := self.drawOptions.sortTdosAsOneItem;
    drawingSurface.initialize;
    end;
  end;

procedure KfTurtle.setDrawOptionsForDrawingTdoOnly;
  begin
  with drawOptions do
    begin
    draw3DObjects := true;
    draw3DObjectsAsRects := false;
    drawLines := true;
    lineContrastIndex := kTdoLineContrastIndex;
    wireFrame := false;
    sortPolygons := true;
    sortTdosAsOneItem := false;
    circlePoints := false;
    end;
  { when drawing a tdo all by itself, you MUST set the turtle scale to 1.0,
    because the tdo multiplies the turtle scale by its own scale (which you are giving it
    in the call to draw) }
  // self.setScale_pixelsPerMm(1.0);  actually, this gets done in the reset method
  drawingSurface.foreColor := kTdoForeColor;
  drawingSurface.backColor := kTdoBackColor;
  drawingSurface.lineColor := clBlack;
  end;

procedure KfTurtle.resetBoundsRect(basePoint: TPoint);
  begin
  realBoundsRect.left := basePoint.x;
  realBoundsRect.right := basePoint.x;
  realBoundsRect.top := basePoint.y;
  realBoundsRect.bottom := basePoint.y;
  end;

procedure KfTurtle.xyz(x: single; y: single; z: single);
	begin
  currentMatrix.position.x := x;
  currentMatrix.position.y := y;
  currentMatrix.position.z := z;
  end;

procedure KfTurtle.setForeColorBackColor(frontColor: TColor; backColor: TColor);
	begin
  drawingSurface.foreColor := frontColor;
  drawingSurface.backColor := backColor;
  end;

procedure KfTurtle.setLineColor(aColor: TColor);
  begin
  drawingSurface.lineColor := aColor;
  end;

procedure KfTurtle.setLineWidth(aWidth: single);
  begin
  drawingSurface.lineWidth := aWidth * scale_pixelsPerMm;
  if drawingSurface.lineWidth > 16000 then drawingSurface.lineWidth := 16000;
  end;

procedure KfTurtle.setScale_pixelsPerMm(newScale_pixelsPerMm: single);
  begin
  scale_pixelsPerMm := newScale_pixelsPerMm;
  end;

function KfTurtle.newTriangleTriangle(aPointIndex: longint; bPointIndex: longint; cPointIndex: longint): KfTriangle;
	begin
	result := KfTriangle.create;
  result.points[0] := recordedPoints[aPointIndex];
  result.points[1] := recordedPoints[bPointIndex];
  result.points[2] := recordedPoints[cPointIndex];
  end;

function KfTurtle.positionCopy: KfPoint3D;
  begin
  {suspicious things that call this may not clean up copy}
  result := currentMatrix.position;
  end;

function KfTurtle.exportingToFile: boolean;
  begin
  // cfk update this if create any mode that is NOT screen and NOT file
  result := self.writingTo <> kScreen; 
  end;

function KfTurtle.writingToDXF: boolean;
  begin
  result := self.writingTo = kDXF;
  end;

function KfTurtle.writingToPOV: boolean;
  begin
  result := self.writingTo = kPOV;
  end;

function KfTurtle.writingTo3DS: boolean;
  begin
  result := self.writingTo = k3DS;
  end;

function KfTurtle.writingToOBJ: boolean;
  begin
  result := self.writingTo = kOBJ;
  end;

function KfTurtle.writingToVRML: boolean;
  begin
  result := self.writingTo = kVRML;
  end;

function KfTurtle.writingToLWO: boolean;
  begin
  result := self.writingTo = kLWO;
  end;

function KfTurtle.fileExportSurface: KfFileExportSurface;
  begin
  if (drawingSurface is KfFileExportSurface) then
    result := drawingSurface as KfFileExportSurface
  else
    result := nil;
  end;

procedure KfTurtle.ifExporting_startNestedGroupOfPlantParts(groupName: string; shortName: string; nestingType: smallint);
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).startNestedGroupOfPlantParts(groupName, shortName, nestingType);
  end;

procedure KfTurtle.ifExporting_endNestedGroupOfPlantParts(nestingType: smallint);
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).endNestedGroupOfPlantParts(nestingType);
  end;

procedure KfTurtle.ifExporting_startPlantPart(aLongName, aShortName: string);
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).startPlantPart(aLongName, aShortName);
  end;

procedure KfTurtle.ifExporting_endPlantPart;
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).endPlantPart;
  end;

function KfTurtle.ifExporting_excludeStem(length: single): boolean;
  begin
  result := false;
  if (drawingSurface is KfDrawingSurfaceForPOV) then
    result := (length <= (drawingSurface as KfDrawingSurfaceForPOV).options.pov_minLineLengthToWrite);
  end;

function KfTurtle.ifExporting_exclude3DObject(scale: single): boolean;
  begin
  result := false;
  if (drawingSurface is KfDrawingSurfaceForPOV) then
    result := (scale <= (drawingSurface as KfDrawingSurfaceForPOV).options.pov_minTdoScaleToWrite);
  end;

procedure KfTurtle.ifExporting_startStemSegment(aLongName: string; aShortName: string; color: TColorRef; width: single;
    index: smallint);
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).startStemSegment(aLongName, aShortName, color, width, index);
  end;

procedure KfTurtle.ifExporting_endStemSegment;
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).endStemSegment;
  end;

function KfTurtle.ifExporting_stemCylinderFaces: smallint;
  begin
  result := 0;
  if (drawingSurface is KfFileExportSurface) then
    result := (drawingSurface as KfFileExportSurface).options.stemCylinderFaces;
  end;

procedure KfTurtle.drawFileExportPipeFaces(const startPoints: array of KfPoint3D;
        const endPoints: array of KfPoint3D; faces: smallint; segmentNumber: smallint);
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).drawPipeFaces(startPoints, endPoints, faces, segmentNumber);
  end;

procedure KfTurtle.ifExporting_start3DObject(aLongName: string; aShortName: string; color: TColorRef; index: smallint);
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).start3DObject(aLongName, aShortName, color, index);
  end;

procedure KfTurtle.ifExporting_end3DObject;
  begin
  if (drawingSurface is KfFileExportSurface) then
    (drawingSurface as KfFileExportSurface).end3DObject;
  end;

{ ---------------------------------------------------------------------------------- KfTurtle returning values }
function KfTurtle.millimetersToPixels(mm: single): single;
  begin
  result := mm * scale_pixelsPerMm;
  end;

function KfTurtle.angleX: byte;
	begin
  result := currentMatrix.angleX;
  end;

function KfTurtle.angleY: byte;
	begin
  result := currentMatrix.angleY;
  end;

function KfTurtle.angleZ: byte;
	begin
  result := currentMatrix.angleZ;
  end;

function KfTurtle.lineColor: TColor;
  begin
  result := drawingSurface.lineColor;
  end;

function KfTurtle.lineWidth: single;
  begin
  result := drawingSurface.lineWidth;
  end;

function KfTurtle.position: KfPoint3d;
  begin
  tempPosition := currentMatrix.position;
  result := tempPosition;
  end;

function KfTurtle.boundsRect: TRect;
  begin
  try
    result.top := round(realBoundsRect.top);
    result.left := round(realBoundsRect.left);
    result.bottom := round(realBoundsRect.bottom);
    result.right := round(realBoundsRect.right);
  except
    {might want to be more precise in assigning a rect}
    result.top := -32767;
    result.left := -32767;
    result.bottom := 32767;
    result.right := 32767;
  end;
  end;

{ ---------------------------------------------------------------------------------- KfTurtle recording }
procedure KfTurtle.startRecording;
  begin
  recordedPointsInUse := 0;
  self.recordPosition;
  end;

procedure KfTurtle.clearRecording;
	begin
 	recordedPointsInUse := 0;
  end;

procedure KfTurtle.recordPosition;
  var newPoint: KfPoint3D;
  begin
  if recordedPointsInUse >= kMaximumRecordedPoints then exit;
  newPoint := currentMatrix.position;
  recordedPoints[recordedPointsInUse] := newPoint;
  inc(recordedPointsInUse);
  self.addToRealBoundsRect(newPoint);
  end;

procedure KfTurtle.recordPositionPoint(const aPoint: KfPoint3D);
  begin
  if recordedPointsInUse >= kMaximumRecordedPoints then
    exit;
  recordedPoints[recordedPointsInUse] := aPoint;
  inc(recordedPointsInUse);
  self.addToRealBoundsRect(aPoint);
  end;

function KfTurtle.transformAndRecord(const originalPoint3D: KfPoint3D; theScale_pixelsPerMm: single): KfPoint3d;
	begin
  {transform and scale point and record the new location without moving}
  result := originalPoint3D;
  KfPoint3d_scaleBy(result, theScale_pixelsPerMm * scale_pixelsPerMm);
  currentMatrix.transform(result);
  self.recordPositionPoint(result);
  end;

procedure KfTurtle.moveAndRecordScale(const originalPoint3D: KfPoint3D; theScale_pixelsPerMm: single);
 	var aPoint3d: KfPoint3D;
  begin
  aPoint3D := originalPoint3D;
  KfPoint3d_scaleBy(aPoint3d, theScale_pixelsPerMm * scale_pixelsPerMm);
  currentMatrix.transform(aPoint3D);
  currentMatrix.position := aPoint3D;
  self.recordPositionPoint(aPoint3D);
  end;

{ ---------------------------------------------------------------------------------- KfTurtle moving }
procedure KfTurtle.moveInMillimeters(mm: single);
  begin
  currentMatrix.move(self.millimetersToPixels(mm));
  end;

procedure KfTurtle.moveInMillimetersAndRecord(mm: single);
  begin
  currentMatrix.move(self.millimetersToPixels(mm));
  self.recordPosition;
  end;

procedure KfTurtle.moveInPixels(pixels: single);
  begin
  currentMatrix.move(pixels);
  end;

procedure KfTurtle.moveInPixelsAndRecord(pixels: single);
  begin
  currentMatrix.move(pixels);
  self.recordPosition;
  end;

{ ---------------------------------------------------------------------------------- KfTurtle drawing }
procedure KfTurtle.drawInPixels(pixels: single);
 	var
  	oldPosition, newPosition: KfPoint3d;
  begin
  oldPosition := currentMatrix.position;
  currentMatrix.move(pixels);
  newPosition := currentMatrix.position;
  if drawOptions.drawStems then
    drawingSurface.drawLineFromTo(oldPosition, newPosition);
  self.addToRealBoundsRect(newPosition);
	end;

{if the DEBUG_TURTLE flag is defined then draw axis information}
// PDF PORT Issue
  procedure debugDrawInMillimeters(turtle: KfTurtle; mm: single);
 	  var
  	  oldPosition, newPosition: KfPoint3d;
    begin
    oldPosition := turtle.currentMatrix.position;
    turtle.currentMatrix.move(turtle.millimetersToPixels(mm));
    newPosition := turtle.currentMatrix.position;
    turtle.addToRealBoundsRect(newPosition);
    end;

  procedure debugDrawAxis(turtle: KfTurtle; pixels: single);
 	  var
  	  oldPosition, newPosition: KfPoint3d;
    begin
    oldPosition := turtle.currentMatrix.position;
    turtle.currentMatrix.move(pixels);
    newPosition := turtle.currentMatrix.position;
    if turtle.drawOptions.drawStems then
      turtle.drawingSurface.drawLineFromTo(oldPosition, newPosition);
    end;

  // PDF PORT --Alternative -- changed name of alternative function -- Will not be called
  procedure KfTurtle.drawInMillimeters_debug(mm: single);
 	  var
      oldColor: TColorRef;
      oldWidth: single;
    begin
    oldColor := drawingSurface.lineColor;
    oldWidth := drawingSurface.lineWidth;
    drawingSurface.lineWidth := 2;
	  drawingSurface.lineColor := clRed;
	  self.push;
	  self.rotateZ(64); {will flip so draw Y (sic)}
	  debugDrawAxis(self, 100.0);
	  self.pop;
    drawingSurface.lineWidth := 1;
	  drawingSurface.lineColor := clBlue;
	  self.push;
	  self.rotateY(64); {will flip so draw Z (sic)}
	  debugDrawAxis(self, 100.0);
	  self.pop;
    drawingSurface.lineColor := oldColor;
    drawingSurface.lineWidth := oldWidth;
    debugDrawInMillimeters(self, mm);
    end;

  function KfTurtle.drawInMillimeters(mm: single; partID: longint): KfTriangle;
 	  var
  	  oldPosition, newPosition: KfPoint3d;
    begin
    result := nil;
    oldPosition := currentMatrix.position;
    currentMatrix.move(self.millimetersToPixels(mm));
    newPosition := currentMatrix.position;
    if drawOptions.drawStems then
      begin
      result := drawingSurface.drawLineFromTo(oldPosition, newPosition);
      if result <> nil then
        result.plantPartID := partID;
      end;
    self.addToRealBoundsRect(newPosition);
    end;

function KfTurtle.drawTriangleFromIndexes(aPointIndex: longint; bPointIndex: longint; cPointIndex: longint; partID: longint): KfTriangle;
	begin
	{drawing surface takes over ownership of triangle}
  result := self.drawingSurface.allocateTriangle;
  drawingSurface.lineWidth := 1.0;
  result.points[0] := recordedPoints[aPointIndex-1];
  result.points[1] := recordedPoints[bPointIndex-1];
  result.points[2] := recordedPoints[cPointIndex-1];
  result.plantPartID := partID;
  drawingSurface.drawLastTriangle;
  end;

procedure KfTurtle.drawTrianglesFromBoundsRect(boundsRect: TRect);
  var aTriangle: KfTriangle;
	begin
	{drawing surface takes over ownership of triangle}
  drawingSurface.lineWidth := 1.0;
  aTriangle := self.drawingSurface.allocateTriangle;
  with aTriangle do
    begin
    points[0].x := boundsRect.left; points[0].y := boundsRect.top;
    points[1].x := boundsRect.right; points[1].y := boundsRect.top;
    points[2].x := boundsRect.left; points[2].y := boundsRect.bottom;
    end;
  drawingSurface.drawLastTriangle;
  aTriangle := self.drawingSurface.allocateTriangle;
  with aTriangle do
    begin
    points[0].x := boundsRect.left; points[0].y := boundsRect.bottom;
    points[1].x := boundsRect.right; points[1].y := boundsRect.top;
    points[2].x := boundsRect.right; points[2].y := boundsRect.bottom;
    end;
  drawingSurface.drawLastTriangle;
  end;

procedure KfTurtle.drawTriangle;
  var triangle: KfTriangle;
  begin
  if recordedPointsInUse <> 3 then
    raise Exception.create('Problem: Triangle made without three points in method KfTurtle.drawTriangle.');
  {drawing surface owns triangle}
  triangle := self.drawingSurface.allocateTriangle;
  triangle.points[0] := recordedPoints[0];
  triangle.points[1] := recordedPoints[1];
  triangle.points[2] := recordedPoints[2];
  self.drawingSurface.drawLastTriangle;
  recordedPointsInUse := 0;
  end;

procedure KfTurtle.addToRealBoundsRect(const aPoint: KfPoint3d);
	begin
  with aPoint do
    with realBoundsRect do
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

{ ---------------------------------------------------------------------------------- KfTurtle stack }
procedure KfTurtle.push;
  begin
  if numMatrixesUsed >= matrixStack.count then
  	matrixStack.add(currentMatrix.deepCopy)
  else
    currentMatrix.copyTo(KfMatrix(matrixStack.items[numMatrixesUsed]));
  inc(numMatrixesUsed);
  currentMatrix := matrixStack.items[numMatrixesUsed-1];
  end;

procedure KfTurtle.pop;
  begin
  if numMatrixesUsed < 1 then exit;
  dec(numMatrixesUsed);
  currentMatrix := matrixStack.items[numMatrixesUsed-1];
  end;

function KfTurtle.stackSize: longint;
 	begin
  result := numMatrixesUsed;
  end;

{ ---------------------------------------------------------------------------------- KfTurtle rotating }
procedure KfTurtle.rotateX(angle: single);
	begin
  currentMatrix.rotateX(angle);
  end;

procedure KfTurtle.rotateY(angle: single);
	begin
  currentMatrix.rotateY(angle);
  end;

procedure KfTurtle.rotateZ(angle: single);
	begin
  currentMatrix.rotateZ(angle);
  end;

{ ---------------------------------------------------------------------------------- KfTurtle defaulting }
{where the default turtle is used need a try..finally
to ensure defaultStopUsing is called no matter what}
class function KfTurtle.defaultStartUsing: KfTurtle;
  begin
  if gDefaultTurtleInUse then
    raise Exception.create('Problem: turtle is already in use; in method KfTurtle.defaultStartUsing.');
	gDefaultTurtleInUse := true;
  result := gDefaultTurtle;
  end;

class procedure KfTurtle.defaultStopUsing;
  begin
	gDefaultTurtleInUse := false;
  end;

class procedure KfTurtle.defaultAllocate;
  begin
	gDefaultTurtle := nil;
	gDefaultTurtle := KfTurtle.create;
	gDefaultTurtleInUse := false;
  end;

class procedure KfTurtle.defaultFree;
  begin
	gDefaultTurtle.free;
	gDefaultTurtle := nil;
  end;


begin
FastTrigInitialize;
KfTurtle.defaultAllocate;
{need to default free somewhere in project}
end.


