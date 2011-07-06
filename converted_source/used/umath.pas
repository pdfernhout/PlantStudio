unit umath;

interface

uses WinTypes, usupport;

type
SCurveStructure = record
  x1: single;
  y1: single;
  x2: single;
  y2: single;
  c1: single;
  c2: single;
  end;

const
  kPi =  3.141596;
  kLowestFloatAboveZero = 10e-12;
  kLowestQuantityFloat = 10e-6;

function ErrorMessage(errorString: string): single;  {returns zero for convenience}
function sqr(x: single): single;
function min(a: single; b: single): single;
function max(a: single; b: single): single;
function intMin(a: integer; b: integer): integer;
function intMax(a: integer; b: integer): integer;
function pow(number: extended; exponent: extended): extended;
function power(number: extended; exponent: extended): extended;
function tan(x: extended): extended;
function arcCos(x: extended): extended;
function arcSin(x: extended): extended;
function log10(x: extended): extended;
function safeLn(x: extended): extended;
function safeLnWithResult(x: extended; var failed: boolean): extended;
function safeExp(x: extended): extended;
function safeExpWithResult(x: extended; var failed: boolean): extended;
function safediv(x: single; y: single): single;
function safedivExcept(x: single; y: single; exceptionResult: single): single;
function safedivWithResult(x: single; y: single; var failed: boolean): single;
{ s curves }
function scurve(x: extended; c1: extended; c2: extended): extended;
function scurveWithResult(x: extended; c1: extended; c2: extended; var failed: boolean): extended;
procedure calcSCurveCoeffs(var sCurve: SCurveStructure);
procedure calcSCurveCoeffsWithResult(var sCurve: SCurveStructure; var failed: boolean);
procedure transferSCurveValue(direction: integer; var param: sCurveStructure; index: integer; var value);
function stringToSCurve(aString: string): SCurveStructure;
function sCurveToString(sCurve: SCurveStructure): string;
{ graphics }
function pointsAreCloseEnough(point1: TPoint; point2: TPoint): boolean;

implementation

uses Dialogs, SysUtils,
  uunits, udebug, usstream, uparams;

{these consts are really defined in uplant.pas but we don't want to include it - keep current}
const
	kGetField = 0;
	kSetField = 1;

{ error message - returns zero for convenience}
function ErrorMessage(errorString: string): single;
  begin
  result := 0.0;
  DebugPrint(errorString);
  end;

{ ---------------------------------------------------------------------------------------------- math functions }
function sqr(x: single): single;
  begin
  result := x * x;
  end;

function min(a: single; b: single): single;
  begin
  if (a < b) then result := a else result := b;
  end;

function max(a: single; b: single): single;
  begin
  if (a > b) then result := a else result := b;
  end;

function intMin(a: integer; b: integer): integer;
  begin
  if (a < b) then result := a else result := b;
  end;

function intMax(a: integer; b: integer): integer;
  begin
  if (a > b) then result := a else result := b;
  end;

{ RE-RAISES EXCEPTION }
function pow(number: extended; exponent: extended): extended;
	begin
  try
  	result := safeExp(exponent * safeLn(number));
  except
    ErrorMessage('Invalid number for power function: ' + floatToStr(number) + ' to the power ' + floatToStr(exponent));
    result := 1.0;
    raise;
  end;
	end;

{ this function is needed to get around a bug in the development environment: if a negative
number is raised to a non-integer power, an exception should be raised but the environment
instead crashes. }
{ RE-RAISES EXCEPTION }
function power(number: extended; exponent: extended): extended;
  begin
  try
  if (number > 0.0) then
    result := pow(number, exponent)
  else if (number = 0.0) then
    begin
    if exponent = 0.0 then
      begin
      result := 1.0;
      raise Exception.create('Problem: Zero raised to zero power.');
      end
    else
      result := 0.0;
    end
  else
    begin
    result := 0.0;
    raise Exception.create('Problem: Negative number to non-integer power: ' + floatToStr(number) + ' to ' + floatToStr(exponent));
    end;
  except
    result := errorMessage('Problem: Uncaught error in power function: ' + floatToStr(number) + ' to ' + floatToStr(exponent));
    raise;
  end;
  end;

{ RE-RAISES EXCEPTION }
function tan(x: extended): extended;
  begin
  try
  result := sin(x) / cos(x);
  except
    result := errorMessage('Uncaught error in tangent function: ' + floatToStr(x));
    raise;
  end;
  end;

{ RE-RAISES EXCEPTION }
function arcCos(x: extended): extended;
  begin
  { this was in the Delphi help but doesn't seem to work }
  { result := arcTan(sqrt(1.0 - sqr(x)) / x); }
  try
  result := kPi / 2.0 - arcSin(x);  { from Smalltalk/V }
  except
    result := ErrorMessage('Invalid number for arcCos: ' + floatToStr(x));
    raise;
  end;
  end;

{ RE-RAISES EXCEPTION }
function arcSin(x: extended): extended;
  begin
  try
  result := arcTan(x / sqrt(1.0 - sqr(x)));
  except
    result := ErrorMessage('Invalid number for arcSin: ' + floatToStr(x));
    raise;
  end;
  end;

const
  oneOverNaturalLogOfTen: extended = 0.434294481;

{ RE-RAISES EXCEPTION }
{ uses notion that logN(x) = ln(x) / ln(N) }
function log10(x: extended): extended;
  begin
  try
	if x > 0.0 then
		result := oneOverNaturalLogOfTen * safeLn(x)
  else
    begin
    result := -1;
    raise Exception.create('Problem: Tried to take log (base 10) of zero or negative number.');
    end;
  except
    result := ErrorMessage('Problem: Invalid number for log (base 10): ' + floatToStr(x) + '.');
    raise;
  end;
  end;

{ RE-RAISES EXCEPTION }
function safeLn(x: extended): extended;
  begin
  if x > 0.0 then
    try
    // PDF PORT added semicolon
    result := ln(x);
  	except
    	ErrorMessage('Invalid number for natural log: ' + floatToStr(x));
    	result := 1.0;
      raise;
  	end
  else
    begin
    raise Exception.create('Problem: Tried to take ln of zero or negative number: ' + floatToStr(x) + '.');
    end;
  end;

{ same as safeLn but does not show an errorMessage or re-raise the exception; just returns whether it failed;
  used inside paint methods where you don't want error dialogs popping up }
function safeLnWithResult(x: extended; var failed: boolean): extended;
  var temp: extended;
  begin
  failed := true;
  result := 0.0;
  temp := 0.0;
  if x <= 0.0 then exit;
  try
    temp := ln(x);
  except
    result := 1.0;
    exit;
  end;
  result := temp;
  failed := false;
  end;

{ RE-RAISES EXCEPTION }
function safeExp(x: extended): extended;
  begin
  try
    // PDF PORT added semicolon
    result := exp(x);
  except
    result := ErrorMessage('Invalid number for exponential function: ' + floatToStr(x));
    raise;
  end;
  end;

{ same as safeExp but does not show an errorMessage or re-raise the exception; just returns whether it failed;
  used inside paint methods where you don't want error dialogs popping up }
function safeExpWithResult(x: extended; var failed: boolean): extended;
  var temp: extended;
  begin
  failed := true;
  result := 0.0;
  temp := 0.0;
  try
    temp := exp(x);
  except
    exit;
  end;
  result := temp;
  failed := false;
  end;

{this function catches a divide by zero before it produces a not-a-number.
this can happen because of an underflow, an error in the code, or an unexpected condition.
this is a different approach than EPIC's which is basically to divide by the number plus a tiny float
for all cases (like 1e-20 or 1e-10)}
{ RE-RAISES EXCEPTION }
function safediv(x: single; y: single): single;
  begin
  try
  if (y <> 0.0) then
    result := x / y
  else
    begin
    result := 0.0;
    raise Exception.create('Problem: Divide by zero.');
    end;
  except
    result := ErrorMessage('Problem: Unspecified problem with dividing ' + floatToStr(x) + ' by ' + floatToStr(y) + '.');
    raise;
  end;
  end;

{ RE-RAISES EXCEPTION }
{ same as safediv except that the user specifies what to return if the denominator is zero }
function safedivExcept(x: single; y: single; exceptionResult: single): single;
  begin
  try
  if (y <> 0.0) then
    result := x / y
  else
    result := exceptionResult;
  except
    result := ErrorMessage('Problem in dividing ' + floatToStr(x) + ' by ' + floatToStr(y));
    raise;
  end;
  end;

{ same as safediv but does not show an errorMessage or re-raise the exception; just returns whether it failed;
  used inside paint methods where you don't want error dialogs popping up }
function safedivWithResult(x: single; y: single; var failed: boolean): single;
  var temp: extended;
  begin
  failed := true;
  result := 0.0;
  temp := 0.0;
  if y = 0.0 then exit;
  try
    temp := x / y;
  except
    exit;
  end;
  result := temp;
  failed := false;
  end;

{ RE-RAISES EXCEPTION }
{ this function carries out a structure found in many EPIC equations. }
function scurve(x: extended; c1: extended; c2: extended): extended;
  var temp: extended;
  begin
  try
  temp := c1 - c2 * x;
  if temp > 85.0 then
    begin
    temp := 85.0;
    raise exception.create('Problem: Exponent of number would have gone out of float range.');
    end;
  result := safediv(x, x + safeExp(temp));
  except
    result := errorMessage('Problem in s curve: numbers are ' + floatToStr(x)
        + ', ' + floatToStr(c1) + ', and ' + floatToStr(c2));
    raise;
  end;
  end;

{ same as scurve but does not show an errorMessage or re-raise the exception; just returns whether it failed;
  used inside paint methods where you don't want error dialogs popping up }
function scurveWithResult(x: extended; c1: extended; c2: extended; var failed: boolean): extended;
  var temp: extended;
  begin
  failed := true;
  result := 0.0;
  temp := 0.0;
  try
    temp := c1 - c2 * x;
    if temp > 85.0 then exit;
    temp := safeExpWithResult(temp, failed);
    if failed then exit;
    temp := safedivWithResult(x, x + temp, failed);
    if failed then exit;
  except
    exit;
  end;
  failed := false;
  result := temp;
  end;

{ s curve params }
{ RE-RAISES EXCEPTION }
// deal with zero s curve values by defaulting whole curve to hard-coded values
procedure calcSCurveCoeffs(var sCurve: SCurveStructure);
  var xx: extended;
  begin
  try
  with sCurve do
    begin
    if (x1 <= 0.0) or (y1 <= 0.0) or (x2 <= 0.0) or (y2 <= 0.0)
        or (x1 >= 1.0) or (y1 >= 1.0) or (x2 >= 1.0) or (y2 >= 1.0) then
      begin
      // instead of raising exception, just hard-code whole curve to acceptable values
      // don't use Parameters.tab default in case that was read in wrong also
      x1 := 0.25;
      y1 := 0.1;
      x2 := 0.65;
      y2 := 0.85;
      end;
    xx := safeLn(safediv(x1, y1) - x1);
    c2 := safediv((xx - safeLn(safediv(x2, y2) - x2)), x2 - x1);
    c1 := xx + x1 * c2;
    end;
  except
    on e: Exception do
      begin
      { set s curve to all acceptable values - safest }
      scurve.x1 := 0.25;
      scurve.y1 := 0.1;
      sCurve.x2 := 0.65;
      sCurve.y2 := 0.85;
      raise;
      end;
  end;
  end;

{ same as Utils_CalcSCurveCoeffs but does not show an errorMessage or re-raise the exception;
  just returns whether it failed; used inside paint methods where you don't want error dialogs popping up }
procedure calcSCurveCoeffsWithResult(var sCurve: SCurveStructure; var failed: boolean);
  var
    quotientX1Y1, lnQuotientX1Y1MinusX1, quotientX2Y2, lnQuotientX2Y2MinusX2, c1temp, c2temp: extended;
  begin
  failed := true;
  try
  with sCurve do
    begin
    quotientX1Y1 := safedivWithResult(x1, y1, failed);
    if failed then exit;
    lnQuotientX1Y1MinusX1 := safeLnWithResult(quotientX1Y1 - x1, failed);
    if failed then exit;
    quotientX2Y2 := safedivWithResult(x2, y2, failed);
    if failed then exit;
    lnQuotientX2Y2MinusX2 := safeLnWithResult(quotientX2Y2 - x2, failed);
    if failed then exit;
    c2temp := safedivWithResult(lnQuotientX1Y1MinusX1 - lnQuotientX2Y2MinusX2, x2 - x1, failed);
    if failed then exit;
    c1temp := lnQuotientX1Y1MinusX1 + x1 * c2temp;
    end;
  except
    exit;
  end;
  sCurve.c1 := c1temp;
  sCurve.c2 := c2temp;
  failed := false;
  end;

procedure transferSCurveValue(direction: integer; var param: sCurveStructure; index: integer; var value);
  begin
  if (direction = kGetField) then
    begin
    case index of
      0: single(value) := param.x1;
      1: single(value) := param.y1;
      2: single(value) := param.x2;
      3: single(value) := param.y2;
      end;
    end
  else
    begin
    { direction == kSetField }
    case index of
      0: param.x1 := single(value);
      1: param.y1 := single(value);
      2: param.x2 := single(value);
      3: param.y2 := single(value);
    end;
  end;
end;

function stringToSCurve(aString: string): SCurveStructure;
	var
    stream: KfStringStream;
  begin
  result.x1 := 0; result.y1 := 0; result.x2 := 0; result.y2 := 0; result.c1 := 0; result.c2 := 0;
  { format is x1 y1 x2 y2 }
  stream := KfStringStream.create;
  try
    stream.onStringSeparator(aString, ' ');
    boundForString(stream.nextToken, kFieldFloat, result.x1);
    boundForString(stream.nextToken, kFieldFloat, result.y1);
    boundForString(stream.nextToken, kFieldFloat, result.x2);
    boundForString(stream.nextToken, kFieldFloat, result.y2);
  finally
    stream.free;
  end;
  end;

function sCurveToString(sCurve: SCurveStructure): string;
  begin
  result := digitValueString(sCurve.x1) + ' ' + digitValueString(sCurve.y1) + ' '
      + digitValueString(sCurve.x2)  + ' ' + digitValueString(sCurve.y2);
  end;

const kPlantProximityNeeded = 4;
  {CFK NOTE you may want to change this if you use this function
  to actually click on plant parts }
  // this is not being used to select plant parts, the drawing surface is doing it

function pointsAreCloseEnough(point1: TPoint; point2: TPoint): boolean;
  begin
  result := (abs(point1.x - point2.x) < kPlantProximityNeeded)
    and (abs(point1.y - point2.y) < kPlantProximityNeeded);
  end;

end.
