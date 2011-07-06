unit Udrawingsurface;

interface

uses Windows, Graphics, SysUtils, 
  ucollect, utdo, u3dsupport;

const
  kInitialDrawingSurfaceTriangles = 1000;

type

	KfDrawingSurface = class(TObject)
    public
    pane: TCanvas;
    lineContrastIndex: smallint;
    drawingLines, fillingTriangles, circlingPoints: boolean;
    foreColor, backColor, lineColor, circleColor: TColor;
    numTrianglesUsed: longint;
    triangles: TListCollection;
    recording: boolean;
    lineWidth: single;
    circlePointRadius: smallint;
    sortTdosAsOneItem: boolean;
    constructor create; virtual;
    destructor destroy; override;
    procedure draw3DFace(point1, point2, point3, point4: KfPoint3D); virtual;
		procedure basicDrawLineFromTo(const startPoint: KfPoint3D; const endPoint: KfPoint3D); virtual;
		procedure basicDrawTriangle(triangle: KfTriangle); virtual;
    procedure clearTriangles;
		function allocateTriangle: KfTriangle;
		procedure sortTrianglesConsideringTdos;
		procedure sortTriangles(left: integer; right: integer);
		procedure recordingStart;
		procedure recordingStop;
		procedure trianglesDraw;
 		procedure recordingDraw;
    function drawLineFromTo(const startPoint: KfPoint3D; const endPoint: KfPoint3D): KfTriangle;
		procedure drawLastTriangle;
		procedure initialize;
    function plantPartIDForPoint(point: TPoint): longint;
  	end;

implementation

{ ----------------------------------------------------------------------------- *KfDrawingSurface creating/destroying }
constructor KfDrawingSurface.create;
  var i: longint;
	begin
  inherited create;
  triangles := TListCollection.create;
  numTrianglesUsed := 0;
  fillingTriangles := true;
  self.initialize;
  { start with a bunch of triangles }
  for i := 0 to kInitialDrawingSurfaceTriangles do
    triangles.add(KfTriangle.create);
  end;

destructor KfDrawingSurface.destroy;
	begin
  triangles.free;
  inherited destroy;
  end;

procedure KfDrawingSurface.initialize;
  begin
  {backColor := clLtGray;
  foreColor := clLtGray;
  lineColor := clLtGray;}
  lineWidth := 1.0;
  recording := false;
  clearTriangles;
  if self.pane <> nil then
    begin
    if fillingTriangles then
      self.pane.brush.style := bsSolid
    else
      self.pane.brush.style := bsClear;
    end;
  end;

{ ----------------------------------------------------------------------------- KfDrawingSurface managing triangles }
procedure KfDrawingSurface.clearTriangles;
  var i: longint;
  begin
  for i := 0 to numTrianglesUsed - 1 do
    KfTriangle(triangles.items[i]).tdo := nil;
  numTrianglesUsed := 0;
  end;

function KfDrawingSurface.plantPartIDForPoint(point: TPoint): longint;
  var
    i: longint;
    triangle: KfTriangle;
    points: array[0..2] of TPoint;
    widenedPoints: array[0..2] of TPoint;
    width: integer;
    thisDistance, closestDistanceSoFar: single;
    closestPartID: longint;
    centerX, centerY, x, y: single;
  begin
  x := point.x;
  y := point.y;
  result := -1;
  closestDistanceSoFar := 0;
  closestPartID := -1;
  for i := 0 to triangles.count - 1 do
    begin
    triangle := KfTriangle(triangles.items[i]);
    if triangle.isLine then
      begin
      centerX := (triangle.points[0].x + triangle.points[1].x) / 2.0;
      centerY := (triangle.points[0].y + triangle.points[1].y) / 2.0;
      thisDistance := (centerX - x) * (centerX - x) + (centerY - y) * (centerY - y);
      if (closestPartID = -1) or (thisDistance < closestDistanceSoFar) then
        begin
        closestDistanceSoFar := thisDistance;
        closestPartID := triangle.plantPartID;
        end;
      end
    else
      begin
      points[0].x := round(triangle.points[0].x); points[0].y := round(triangle.points[0].y);
      points[1].x := round(triangle.points[1].x); points[1].y := round(triangle.points[1].y);
      points[2].x := round(triangle.points[2].x); points[2].y := round(triangle.points[2].y);
      if pointInTriangle(point, points) then
        begin
        result := triangle.plantPartID;
        exit;
        end;
      end;
     end;
   result := closestPartID;
  end;

function KfDrawingSurface.allocateTriangle: KfTriangle;
  begin
  result := nil;
  if numTrianglesUsed < triangles.count then
    result := triangles.items[numTrianglesUsed]
  else
    begin
    result := KfTriangle.create;
    triangles.add(result);
    end;
  inc(numTrianglesUsed);
  end;

procedure KfDrawingSurface.sortTrianglesConsideringTdos;
  var
    i: longint;
    triangle: KfTriangle;
    oldValue: single;
	begin
  if numTrianglesUsed <= 1 then exit;
  if sortTdosAsOneItem then
    for i := 0 to numTrianglesUsed - 1 do
      begin
      triangle := KfTriangle(triangles.items[i]);
      if not triangle.isLine then
        begin
        oldValue := triangle.zForSorting;
        // the 0.01 is to keep the polygons inside the tdo in order but still (usually) separate from other tdos
        // could produce errors if the z value is really small already
        if triangle.tdo <> nil then
          try
            triangle.zForSorting := triangle.tdo.zForSorting + triangle.zForSorting * 0.01;
          except
            triangle.zForSorting := oldValue;
          end;
        // have to clear out tdo pointer afterward because triangles are reused
        triangle.tdo := nil;
        end;
      end;
  self.sortTriangles(0, numTrianglesUsed - 1);
  end;

procedure KfDrawingSurface.sortTriangles(left: integer; right: integer);
  var
    i, j: integer;
    z: single;
  begin
  if right > left then
  	begin
    z := KfTriangle(triangles.items[right]).zForSorting;
    i := left - 1;
    j := right;
    while true do
      begin
      repeat
        i := i + 1;
        until not (KfTriangle(triangles.items[i]).zForSorting < z);
      repeat
        j := j - 1;
        until (j < i) or (not (KfTriangle(triangles.items[j]).zForSorting > z));
      if i >= j then break;
      triangles.exchange(i,j);
      end;
    triangles.exchange(i, right);
    sortTriangles(left, j);
    sortTriangles(i + 1, right);
    end;
	end;

{ ----------------------------------------------------------------------------- KfDrawingSurface drawing }
procedure KfDrawingSurface.trianglesDraw;
	var i: integer;
	begin
  if numTrianglesUsed > 0 then
  	for i := 0 to numTrianglesUsed - 1 do
    	self.basicDrawTriangle(triangles.items[i]);
  end;

function KfDrawingSurface.drawLineFromTo(const startPoint: KfPoint3D; const endPoint: KfPoint3D): KfTriangle;
  var triangle: KfTriangle;
  begin
  result := nil;
  if self.recording then
  	begin
    {store triangle}
    triangle := self.allocateTriangle;
    triangle.points[0] := startPoint;
    triangle.points[1] := endPoint;
    triangle.isLine := true;
    {need to handle drawing surface colors}
    triangle.foreColor := foreColor;
    triangle.backColor := backColor;
    triangle.lineColor := lineColor;
    triangle.lineWidth := lineWidth;
    triangle.computeZ;  
    result := triangle;
    end
  else
    self.basicDrawLineFromTo(startPoint, endPoint);
  end;

procedure KfDrawingSurface.basicDrawLineFromTo(const startPoint: KfPoint3D; const endPoint: KfPoint3D);
  begin
  {assuming pen color and width is saved and restored elsewhere}
  if self.pane = nil then exit;
  try
    self.pane.pen.width := round(self.lineWidth) mod 1000;
    self.pane.pen.color := self.lineColor;
    self.pane.pen.style := psSolid;
    self.pane.moveTo(round(startPoint.x) mod 32767, round(startPoint.y) mod 32767);
    self.pane.lineTo(round(endPoint.x) mod 32767, round(endPoint.y) mod 32767);
  except
    {do nothing if rounding fails}
  end;
  end;

procedure KfDrawingSurface.draw3DFace(point1, point2, point3, point4: KfPoint3D);
  begin
  // subclasses must override
  raise exception.create('Problem: draw3DFace method not supported in base class; in method KfDrawingSurface.draw3DFace.');
  end;

{terminology is different: drawing surface frontColor is pen line color }
{ and drawing surface backColor (which should be back-facing triangle) is fill color}
{drawing surface draws the last triangle allocated - and deallocates it if needed}
procedure KfDrawingSurface.drawLastTriangle;
  var triangle: KfTriangle;
  begin
  triangle := triangles.items[numTrianglesUsed - 1]; {last allocated triangle}
  triangle.isLine := false;
  triangle.updateGeometry;
  triangle.lineWidth := lineWidth; {PDF FIX - maybe should scale this?}
  triangle.lineColor := lineColor;
  triangle.foreColor := foreColor;
  triangle.backColor := backColor;
  if self.recording then
  	begin
    {"store triangle"}
    {do nothing as already stored}
    end
  else
  	begin
    self.basicDrawTriangle(triangle);
    {deallocate it}
    dec(numTrianglesUsed);
    end;
  end;

{pdf - draw the triangle object - assume it is reasonably flat"
{can only draw triangles for now}
{needs fixed size for array - would need to allocate for variable sizes}
{or could use direct windows triangle call and larger array but pass number of points}
{terminology is different: drawing surface frontColor is pen line color}
{and drawing surface backColor (which should be back-facing triangle) is fill color"}
{restricting range of coordingates to 32767 to prevent possible out of range errors when drawing}
procedure KfDrawingSurface.basicDrawTriangle(triangle: KfTriangle);
  var
    startPoint: KfPoint3D;
    endPoint: KfPoint3D;
    aPoint: KfPoint3D;
    pointArray: array[0..3] of TPoint;
    i: integer;
  begin
  if self.pane = nil then exit;
  if (triangle.isLine) then
    begin
    {draw line}
    try
      self.pane.pen.width := round(triangle.lineWidth);
      self.pane.pen.color := triangle.lineColor;
      self.pane.pen.style := psSolid;
      startPoint := triangle.points[0];
      endPoint := triangle.points[1];
      self.pane.moveTo(round(startPoint.x) mod 32767, round(startPoint.y) mod 32767);
      self.pane.lineTo(round(endPoint.x) mod 32767, round(endPoint.y) mod 32767);
    except
      {do nothing if round fails or assign to integer fails}
    end;
    exit;
    end;
  for i := 0 to 3 do
    begin
    // make last point same as first for drawing lines around whole polygon
    if i < 3 then
      aPoint := triangle.points[i]
    else
      aPoint := triangle.points[0];
    try
      pointArray[i].x := round(aPoint.x) mod 32767;
      pointArray[i].y := round(aPoint.y) mod 32767;
    except
      {maybe could test sign to put in negative big numbers? watch out for NaNs!}
      pointArray[i].x := 32767;
      pointArray[i].y := 32767;
    end;
    end;
  self.pane.pen.style := psSolid;
  self.pane.brush.color := triangle.visibleSurfaceColor;
  if self.drawingLines then
    begin
    if fillingTriangles then
      self.pane.pen.color := triangle.drawLinesColor(lineContrastIndex)
    else
      self.pane.pen.color := triangle.visibleSurfaceColor;
    end
  else
    self.pane.pen.color := triangle.visibleSurfaceColor;
  self.pane.pen.width := 1;
  if fillingTriangles then
    self.pane.polygon(pointArray)
  else
    self.pane.polyLine(pointArray);   
  if self.circlingPoints then
    begin
    self.pane.pen.color := circleColor;
    self.pane.brush.color := circleColor;
    for i := 0 to 2 do
      self.pane.ellipse(pointArray[i].x - circlePointRadius, pointArray[i].y - circlePointRadius,
          pointArray[i].x + circlePointRadius, pointArray[i].y + circlePointRadius);
    end;
	end;

{ ----------------------------------------------------------------------------- KfDrawingSurface recording }
procedure KfDrawingSurface.recordingStart;
	begin
  self.clearTriangles;
  recording := true;
  end;

procedure KfDrawingSurface.recordingStop;
	begin
  recording := false;
  end;

procedure KfDrawingSurface.recordingDraw;
	begin
  self.sortTrianglesConsideringTdos;
  self.trianglesDraw;
  end;

end.
 