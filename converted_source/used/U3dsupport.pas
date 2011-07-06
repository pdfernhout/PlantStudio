unit U3dsupport;

interface

uses Windows, Graphics,
    utdo, usupport;

const
	kFastTrigArraySize = 256; {if you change this - you need to change angleX etc. functions}
  kDirectionClockwise = 1; kDirectionCounterClockwise = -1; kDirectionUnknown = 0;

var
	SinCache: array [0..kFastTrigArraySize-1] of single;
  CosCache: array [0..kFastTrigArraySize-1] of single;

type

  TRealRect = record
    top, left, bottom, right: single;
    end;

  Vertex = record
    x: Real;
    y: Real;
    z: Real;
    end;

  VertexTriangle = record
    vertex1: integer;
    vertex2: integer;
    vertex3: integer;
    end;

	KfMatrix = class(TObject)
  	public
    a0, a1, a2, b0, b1, b2, c0, c1, c2: single;
    position: KfPoint3D;
	  {class SinCache CosCache}
		function angleX: byte;
		function angleY: byte;
		function angleZ: byte;
		procedure initializeAsUnitMatrix;
		procedure move(distance: single);
		procedure rotateX(angle: single);
		procedure rotateY(angle: single);
		procedure rotateZ(angle: single);
		procedure transform(var aPoint3D: KfPoint3D);
    function deepCopy: KfMatrix;
    procedure copyTo(otherMatrix: KfMatrix);
  	end;

	KfTriangle = class(TObject) {these can only be triangular}
  	public
    foreColor: TColor;
    backColor: TColor;
    lineColor: TColor;
    zForSorting: single;
    backFacing: boolean;
    lineWidth: single;
    isLine: boolean;
    points: array[0..2] of KfPoint3D;
    tdo: KfObject3D;
    plantPartID: longint;
    function visibleSurfaceColor: TColor;
    function invisibleSurfaceColor: TColor;
    function drawLinesColor(lineContrastIndex: smallint): TColor;
		procedure computeBackFacing;
		procedure computeZ;
    procedure updateGeometry;
    end;

function pointInTriangle(const point: TPoint; const triangle: array of TPoint): boolean;
function clockwise (const point0: TPoint; const point1: TPoint; const point2: TPoint): integer;
procedure fastTrigInitialize;
{these functions are no longer called here but are available for other uses}
{they were bundled directly into rotate}
function fastTrigCos(angle: single): single;
function fastTrigSin(angle: single): single;

implementation

{ ------------------------------------------------------------------- global functions }
procedure fastTrigInitialize;
  {Approach: sine and cosine arrays are used for speed. Angles are 0 - 255 instead of 0 to 359}
  {PDF - maybe want to expand this to 0 - 1023? - would impact rotate callers}
  var i: integer;
  begin
  for i := 0 to kFastTrigArraySize - 1 do
    begin
    SinCache[i] := sin(i * 2 * 3.141592654 / kFastTrigArraySize);
    CosCache[i] := cos(i * 2 * 3.141592654 / kFastTrigArraySize);
    end;
  end;

{moved bounding angle into cache range into functions to decrease function overhead}
{copied these functions into rotate to decrease overhead there - both of function call and of bounding angle twice}
function fastTrigCos(angle: single): single;
  var boundedAngle: integer;
  begin
  try
    boundedAngle := round(angle) mod kFastTrigArraySize;
  except
    boundedAngle := 0;
  end;
  if (boundedAngle  < 0) then
  	boundedAngle := kFastTrigArraySize + boundedAngle;
  result := CosCache[boundedAngle];
  end;

function fastTrigSin(angle: single): single;
  var boundedAngle: integer;
  begin
  try
    boundedAngle := round(angle) mod kFastTrigArraySize;
  except
    boundedAngle := 0;
  end;
  if (boundedAngle  < 0) then
  	boundedAngle := kFastTrigArraySize + boundedAngle;
  result := SinCache[boundedAngle];
  end;

function clockwise (const point0: TPoint; const point1: TPoint; const point2: TPoint): integer;
  var dx1, dy1, dx2, dy2: single;
  begin
  dx1 := point1.x - point0.x;
  dy1 := point1.y - point0.y;
  dx2 := point2.x - point0.x;
  dy2 := point2.y - point0.y;
  if (dx1 * dy2) > (dy1 * dx2) then
    result := kDirectionClockwise
  else if (dx1 * dy2) < (dy1 * dx2) then
    result := kDirectionCounterClockwise
  else if ((dx1 * dx2) < 0) Or ((dy1 * dy2) < 0) then
    result := kDirectionCounterClockwise
  else if ((dx1 * dx1) + (dy1 * dy1)) < ((dx2 * dx2) + (dy2 * dy2)) then
    result := kDirectionClockwise
  else
    result := kDirectionUnknown;
	end;

function pointInTriangle(const point: TPoint; const triangle: array of TPoint): boolean;
  var
   first, second, third: integer;
  begin
  result := false;
  if (triangle[0].x = triangle[1].x) and (triangle[1].x = triangle[2].x)
    and (triangle[0].y = triangle[1].y) and (triangle[1].y = triangle[2].y) then
    exit;
  first := clockwise(point, triangle[0], triangle[1]);
  second := clockwise(point, triangle[1], triangle[2]);
  third := clockwise(point, triangle[2], triangle[0]);
  result := (first = second) and (second = third);
  end;

{ ---------------------------------------------------------------------------------- *KfMatrix imitializing and copying }
procedure KfMatrix.initializeAsUnitMatrix;
	begin
	a0 := 1.0; a1 := 0; a2 := 0;
	b0 := 0; b1 := 1.0; b2 := 0;
	c0 := 0; c1 := 0; c2 := 1.0;
	position.x := 0; position.y := 0; position.z := 0;
	end;

function KfMatrix.deepCopy: KfMatrix;
	begin
  result := nil;
  result := KfMatrix.create;
  result.position := position;
  result.a0 := a0; result.a1 := a1; result.a2 := a2;
  result.b0 := b0; result.b1 := b1; result.b2 := b2;
  result.c0 := c0; result.c1 := c1; result.c2 := c2;
  end;

procedure KfMatrix.copyTo(otherMatrix: KfMatrix);
	begin
  otherMatrix.position := position;
  otherMatrix.a0 := a0; otherMatrix.a1 := a1; otherMatrix.a2 := a2;
  otherMatrix.b0 := b0; otherMatrix.b1 := b1; otherMatrix.b2 := b2;
  otherMatrix.c0 := c0; otherMatrix.c1 := c1; otherMatrix.c2 := c2;
  end;

{ ---------------------------------------------------------------------------- KfMatrix moving and transforming }
procedure KfMatrix.move(distance: single);
  begin
  {pdf - move a distance by multiplying matrix values
   movement is along x axis (d, 0, 0, 1);}
  position.x := position.x + distance * a0;
  position.y := position.y + distance * b0;
  position.z := position.z + distance * c0;
  end;

{pdf - transform the point, including offsetting it by the current position}
{Alters the point's contents}
procedure KfMatrix.transform(var aPoint3D: KfPoint3D);
  var
  	x, y, z : single;
	begin
  x := aPoint3D.x;
  y := aPoint3D.y;
  z := aPoint3D.z;
  aPoint3D.x := (x * a0) + (y * a1) + (z * a2) + position.x;
  aPoint3D.y := (x * b0) + (y * b1) + (z * b2) + position.y;
  aPoint3D.z := (x * c0) + (y * c1) + (z * c2) + position.z;
  end;

{ ---------------------------------------------------------------------------------- KfMatrix rotating }
procedure KfMatrix.rotateX(angle: single);
  var
    cosAngle, sinAngle, temp1: single;
    boundedAngleIndex: integer;
  begin
  {bound angle and convert to index}
	{not doing try except around round for speed here - could fail ...}
  boundedAngleIndex := round(angle) mod kFastTrigArraySize;
  if (boundedAngleIndex  < 0) then
  	boundedAngleIndex := kFastTrigArraySize + boundedAngleIndex;
	cosAngle := CosCache[boundedAngleIndex];
  sinAngle := SinCache[boundedAngleIndex];
  {moved minuses to middle to optimize}
  a0 := a0;
  temp1 := (a1 * cosAngle) - (a2 * sinAngle);
  a2 := (a1 * sinAngle) + (a2 * cosAngle);
  a1 := temp1;
  b0 := b0;
  temp1 := (b1 * cosAngle) - (b2 * sinAngle);
  b2 := (b1 * sinAngle) + (b2 * cosAngle);
  b1 := temp1;
  c0 := c0;
  temp1 := (c1 * cosAngle) - (c2 * sinAngle);
  c2 := (c1 * sinAngle) + (c2 * cosAngle);
  c1 := temp1;
	end;

procedure KfMatrix.rotateY(angle: single);
  var
    cosAngle, sinAngle, temp0: single;
    boundedAngleIndex: integer;
  begin
  {bound angle and convert to index}
	{not doing try except around round for speed here - could fail ...}
  boundedAngleIndex := round(angle) mod kFastTrigArraySize;
  if (boundedAngleIndex  < 0) then
  	boundedAngleIndex := kFastTrigArraySize + boundedAngleIndex;
	cosAngle := CosCache[boundedAngleIndex];
  sinAngle := SinCache[boundedAngleIndex];
  temp0 := (a0 * cosAngle) + (a2 * sinAngle);
  a1 := a1;
  a2 := (a2 * cosAngle) - (a0 * sinAngle); {flipped to put minus in middle}
  a0 := temp0;
  temp0 := (b0 * cosAngle) + (b2 * sinAngle);
  b1 := b1;
  b2 := (b2 * cosAngle) - (b0 * sinAngle);  {flipped to put minus in middle}
  b0 := temp0;
  temp0 := (c0 * cosAngle) + (c2 * sinAngle);
  c1 := c1;
  c2 := (c2 * cosAngle) - (c0 * sinAngle); {flipped to put minus in middle}
  c0 := temp0;
  end;

procedure KfMatrix.rotateZ(angle: single);
  var
    cosAngle, sinAngle, temp0: single;
    boundedAngleIndex: integer;
  begin
  (*
  {bound angle and convert to index}
	{not doing try except around round for speed here - could fail ...}
  {boundedAngleIndex := round(angle) mod kFastTrigArraySize;
  if (boundedAngleIndex  < 0) then
  	boundedAngleIndex := kFastTrigArraySize + boundedAngleIndex;
	cosAngle := CosCache[boundedAngleIndex];
  sinAngle := SinCache[boundedAngleIndex];}
                          { cfk try at replacing rounding with using all floating point }
  cosAngle := cos(angle * 2.0 * 3.14159 / 256.0);
  sinAngle := sin(angle * 2.0 * 3.14159 / 256.0);

  {minuses moved to middle to optimize}
  temp0  :=(a0 * cosAngle) - (a1 * sinAngle);
  a1 := (a0 * sinAngle) + (a1 * cosAngle);
  a2 := a2;
  a0 := temp0;
  temp0 := (b0 * cosAngle) - (b1 * sinAngle);
  b1 := (b0 * sinAngle) + (b1 * cosAngle);
  b2 := b2;
  b0 := temp0;
  temp0 := (c0 * cosAngle) - (c1 * sinAngle);
  c1 :=  (c0 * sinAngle) + (c1 * cosAngle);
  c2 := c2;
  c0 := temp0;    *)

    {bound angle and convert to index}
	{not doing try except around round for speed here - could fail ...}
  boundedAngleIndex := round(angle) mod kFastTrigArraySize;
  if (boundedAngleIndex  < 0) then
  	boundedAngleIndex := kFastTrigArraySize + boundedAngleIndex;
	cosAngle := CosCache[boundedAngleIndex];
  sinAngle := SinCache[boundedAngleIndex];
  {minuses moved to middle to optimize}
  temp0  :=(a0 * cosAngle) - (a1 * sinAngle);
  a1 := (a0 * sinAngle) + (a1 * cosAngle);
  a2 := a2;
  a0 := temp0;
  temp0 := (b0 * cosAngle) - (b1 * sinAngle);
  b1 := (b0 * sinAngle) + (b1 * cosAngle);
  b2 := b2;
  b0 := temp0;
  temp0 := (c0 * cosAngle) - (c1 * sinAngle);
  c1 :=  (c0 * sinAngle) + (c1 * cosAngle);
  c2 := c2;
  c0 := temp0;
  end;

{ ---------------------------------------------------------------------------------- KfMatrix returning current angles }
{PDF FIX - potential bug}
{ these do not take in account kFastTrigArraySize could be different from 256}
function KfMatrix.angleX: byte;
	var temp: single;
  begin
  try
    result := 0;
    temp := 0.0;
    temp := (a2 * a2) + (c2 * c2);
    if (temp < 0.0) then temp := 0.0;
    temp := sqrt(temp);
    if (temp = 0.0)then
    	begin
      if (b2 < 0) then result := 64 else result := 256-64;
			end
    else
      begin
      temp := b2 / temp;
      temp := arcTan(temp);
      result := byte(round(-temp * 256 / (2 * 3.1415926)));
      end;
  except
    result := 0;
  end;
	end;

function KfMatrix.angleY: byte;
	var temp: single;
  begin
  try
    result := 0;
    temp := 0.0;
    temp := (a0 * a0) + (c0 * c0);
    if (temp < 0.0) then temp := 0.0;
    temp := sqrt(temp);
    if (temp = 0.0)then
    	begin
      if (b0 < 0) then result := 64 else result := 256-64;
			end
    else
      begin
      temp := b0 / temp;
      temp := arcTan(temp);
      result := byte(round(-temp * 256 / (2 * 3.1415926)));
      end;
  except
    result := 0;
  end;
	end;

function KfMatrix.angleZ: byte;
	var temp: single;
  begin
  try
    result := 0;
    temp := 0.0;
    temp := (a1 * a1) + (c1 * c1);
    if (temp < 0.0) then temp := 0.0;
    temp := sqrt(temp);
    if (temp = 0.0)then
    	begin
      if (b1 < 0) then result := 64 else result := 256-64;
			end
    else
      begin
      temp := b1 / temp;
      temp := arcTan(temp);
      result := byte(round(-temp * 256 / (2 * 3.1415926)));
      end;
  except
    result := 0;
  end;
	end;

{ ---------------------------------------------------------------------------------- KfTriangle updating }
procedure KfTriangle.updateGeometry;
	begin
  self.computeBackFacing;
  self.computeZ;
  end;

procedure KfTriangle.computeBackFacing;
  var
    point0, point1, point2: KfPoint3d;
    backfacingResult: single;
  begin
  self.backFacing := false;
  if self.isLine then exit;
  point0 := self.points[0];
  point1 := self.points[1];
  point2 := self.points[2];
  backfacingResult := ((point1.x - point0.x) * (point2.y - point0.y)) -
  		((point1.y - point0.y) * (point2.x - point0.x));
  self.backFacing := (backfacingResult < 0);
  end;

procedure KfTriangle.computeZ;
  var
  	minZ: single;
	begin
  if self.isLine then
    begin
    minZ := points[0].z;
    if points[1].z < minZ then minZ := points[1].z;
    end
  else
    begin
    minZ := points[0].z;
    if points[1].z < minZ then minZ := points[1].z;
 	 	if points[2].z < minZ then minZ := points[2].z;
    end;
  self.zForSorting := minZ;
  end;

function KfTriangle.visibleSurfaceColor: TColor;
	begin
  if backFacing then result := backColor else result := foreColor;
  end;

function KfTriangle.invisibleSurfaceColor: TColor;
	begin
  if backFacing then result := foreColor else result := backColor;
  end;

function KfTriangle.drawLinesColor(lineContrastIndex: smallint): TColor;
  begin
  if backFacing then result := backColor else result := foreColor;
  if lineContrastIndex > 0 then
    result := darkerColorWithSubtraction(result, 10 * lineContrastIndex);
  end;

end.
