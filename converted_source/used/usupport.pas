unit Usupport;

interface

uses WinTypes, WinProcs, Forms, Controls, StdCtrls, SysUtils, Graphics, Spin;

var
  iniFileChanged: boolean;
  gVersionName: string;

const
  kMaxEvaluationTime_hours = 10; 

type
  SinglePoint = record
    x: single;
    y: single;
    reservedZ: single;
    end;

  SaveFileNamesStructure = record
    fileType: smallint;
    tempFile: string;
    newFile: string;
    backupFile: string;
    writingWasSuccessful: boolean;
    end;

const
  kFileTypeAny = 0;
  kFileTypePlant = 1;
  kFileTypeTabbedText = 2;
  kFileTypeStrategy = 3;
  kFileTypeIni = 4;
  kFileTypeExceptionList = 5;
  kFileTypeBitmap = 6;
  kFileTypeTdo = 7;
  kFileTypeDXF = 8;
  kFileTypeINC = 9;
  kFileType3DS = 10;
  kFileTypeProgramInfo = 11;
  kFileTypeJPEG = 12;
  kFileTypeOBJ = 13;
  kFileTypeMTL = 14;
  kFileTypeVRML = 15;
  kFileTypeLWO = 16;
  kWritingWasSuccessful = true;
  kWritingFailed = false;
  kNoSuggestedFile = '';
  kAskForFileName = true;
  kDontAskForFileName = false;

function strToFloatWithCommaCheck(aString: string): extended;
function hexEncode(const aString: string): string;
function hexUnencode(const encodedString: string): string;
procedure makeEnterWorkAsTab(form: TForm; activeControl: TControl; var key: char);
function bitsPerPixelForColorType(colorType: TPixelFormat): smallint;
procedure tolerantReadln(var aFile: TextFile; var aString: string);
{ text handling }
function limitString(aString: string; maxChars: smallint): string;
function replacePunctuationWithUnderscores(aString: string): string;
function replaceCommasWithPeriods(aString: string): string;
function found(substring, fullString: string): boolean;
function capitalize(aString: string): string;
function readUntilTab(var theFile: textFile): string;
function readSmallintToTab(var fileRef: TextFile): smallint;
function readSingleToTab(var fileRef: TextFile): single;
function readShortStringToTab(var fileRef: TextFile): string;
function readBooleanToTab(var fileRef: TextFile): boolean;
function boundForString(boundString: string; fieldType: integer; var number): boolean;
function trimQuotesFromFirstAndLast(theString: string): string;
function trimLeftAndRight(theString: string): string;
function boolToStr(value: boolean): string;
function strToBool(booleanString: string): boolean;
function stringUpTo(aString, aDelimiter: string): string;
function stringBeyond(aString, aDelimiter: string): string;
function stringBetween(startString, endString, wholeString: string): string;
procedure messageForExceptionType(e: Exception; methodName: string);
{ float to text conversion }
function removeTrailingZeros(theString: string): string;
function shortenLongNonZeroDigitsAfterDecimal(theString: string; maxDigits: integer): string;
function digitValueString(value: single): string;
function valueString(value: single): string;
{ graphics }
function clientRectToScreenRect(handle: HWnd; clientRect: TRect): TRect;
function support_rgb(R: Byte; G: Byte; B: Byte): LongInt;
function combineRects(rect1, rect2: TRect): TRect;
procedure addRectToBoundsRect(var boundsRect: TRect; const newRect: TRect);
function rWidth(rect: TRect): integer;
function rHeight(rect: TRect): integer;
function zeroRect(rect: TRect): boolean;
function rectsAreIdentical(oneRect, twoRect: TRect): boolean;
function colorToRGBString(color: TColorRef): string;
function rgbStringToColor(aString: string): TColorRef;
function blendColors(firstColor: TColorRef; secondColor: TColorRef; aStrength: single): TColorRef;
function darkerColor(aColor: TColorRef): TColorRef;
function darkerColorWithSubtraction(aColor: TColorRef; subtract: smallint): TColorRef;
function lighterColor(aColor: TColorRef): TColorRef;
function rectToString(aRect: TRect): string;
function stringToRect(aString: string): TRect;
function pointToString(aPoint: TPoint): string;
function stringToPoint(aString: string): TPoint;
function setSinglePoint(x, y: single): SinglePoint;
function singlePointToString(aPoint: SinglePoint): string;
function stringToSinglePoint(aString: string): SinglePoint;
procedure drawButton(aCanvas: TCanvas; aRect: TRect; selected: boolean;  enabled: boolean);
function draw3DButton(ACanvas: TCanvas;  Client: TRect; Selected: Boolean;  Pressed: Boolean): TRect;
{ combo and list box utilities }
function currentObjectInComboBox(comboBox: TComboBox): TObject;
function currentObjectInListBox(listBox: TListBox): TObject;
{ file i/o }
function makeFileNameFrom(aString: string): string;
function nameStringForFileType(fileType: smallint): string;
function extensionForFileType(fileType: smallint): string;
function filterStringForFileType(fileType: smallint; includeAllFiles: boolean): string;
function getFileOpenInfo(fileType: smallint; const suggestedFile: string; aTitle: string): string;
function fileNameIsOkayForSaving(suggestedFile: string): boolean;
function getFileSaveInfo(fileType: smallint; askForFileName: boolean;
  const suggestedFile: string; var fileInfo: SaveFileNamesStructure): boolean;
procedure startFileSave(var fileInfo: SaveFileNamesStructure);
procedure cleanUpAfterFileSave(var fileInfo: SaveFileNamesStructure);
procedure setDecimalSeparator; // v1.5
function rotateEncodeBy7(const aString: string): string;

{ don't like using constants for these, but can't find any functions that provide them }
const
  kMinSingle = -3.4e38;
  kMaxSingle = 3.4e38;

implementation

uses Classes, Dialogs, FileCtrl, ExtCtrls, Messages,
  uparams, umath, usstream, ucursor, uwait, udomain, umain;

const kIncludeAllFiles = true; kDontIncludeAllFiles = false;

function rotateEncodeBy7(const aString: string): string;
  var
  	i: integer;
    letter: char;
   begin
  result := '';
  for i := 0 to length(aString) - 1 do
    begin
    letter := aString[i + 1];
    result := result + chr((ord(letter) + 1) mod 256);
    end;
  end;

function hexEncode(const aString: string): string;
  var
  	i: integer;
    letter: char;
   begin
  result := '';
  for i := 0 to length(aString) - 1 do
    begin
    letter := aString[i + 1]; // ((i+4) mod length(aString))
    result := result + chr(ord('A') + (ord(letter) div 32));
    result := result + chr(ord('A') + (ord(letter) mod 32));
    end;
  end;

function hexUnencode(const encodedString: string): string;
  var
  	i: integer;
    letter: char;
    value: integer;
  begin
  result := '';
  value := 0;
  for i := 0 to length(encodedString) - 1 do
    begin
    letter := encodedString[i + 1];
    if i mod 2 = 0 then
    	value := (ord(letter) - ord('A')) * 32
    else
      begin
   	  value := value + (ord(letter) - ord('A'));
    	result := result + chr(value);
      end;
    end;
  end;

function strToFloatWithCommaCheck(aString: string): extended;
  begin
  if found(',', aString) then
    aString := replaceCommasWithPeriods(aString);
  result := strToFloat(aString);
  end;

procedure makeEnterWorkAsTab(form: TForm; activeControl: TControl; var key: char);
  begin
  { this is to make enter work as tab in edit boxes on the form }
  if form = nil then exit;
  if activeControl = nil then exit;
  if not ((activeControl is TEdit) or (activeControl is TComboBox) or (activeControl is TSpinEdit)) then exit;
  if key = #13 then
    begin
    key := #0;
    sendMessage(form.handle, Wm_NextDlgCtl, 0, 0); {next control}
    end;
  end;

function bitsPerPixelForColorType(colorType: TPixelFormat): smallint;
  var
    screenDC: HDC;
  begin
  result := 32; // default to max
  case colorType of
    pfDevice:
      begin
      screenDC := GetDC(0);
      try
        result := (GetDeviceCaps(screenDC, BITSPIXEL) * GetDeviceCaps(screenDC, PLANES));
      finally
        ReleaseDC(0, screenDC);
      end;
      end;
    pf1bit: result := 1;
    pf4bit: result := 4;
    pf8bit: result := 8;
    pf15bit: result := 15;
    pf16bit: result := 16;
    pf24bit: result := 24;
    pf32bit: result := 32;
    pfCustom: result := 32; // just use largest
    end;
  end;

procedure tolerantReadln(var aFile: TextFile; var aString {, extraCharToCarryOver}: string);
  begin
  readln(aFile, aString);
  end;

// CFK unfinished - was trying to deal with text files that have irregular line endings
// such as CR but not LF or just LF
// did not finish - not often found
// got files from user frank salinas as test cases - look at these (in PS longterm) if look at this again later

//  var aChar: char;
          (*
  aString := '';
  aChar := chr(32);
  // chr(26) is returned if read reaches eof
  while (not eof(aFile)) and (not (aChar in [#0, #10, #13, #26])) do
    begin
    read(aFile, aChar);
    if not (aChar in [#0, #10, #13, #26]) then
      aString := aString + aChar
    else
      begin
      read(aFile, aChar);
      if not (aChar in [#0, #10, #13, #26]) then
        extraCharToCarryOver := '' + aChar;
      end;
    end;

  aChar := chr(32);
  aString := '';
  while not eof(aFile) do
    begin
    read(aFile, aChar);
    if not (aChar in [#0, #10, #13, #26]) then
      result := result + aChar
    else
      begin
      if (aChar = chr(13)) and not eof(aFile) then
        begin
        read(theTextFile, aChar);
        if aChar <> chr(10) then
          raise Exception.create('Problem in file input');
        end;
      break;
      end;
    end;


  end;
  *)

  (*
  Start := BufPtr;
  while not (BufPtr^ in [#13, #26]) do Inc(BufPtr);
  SetString(S, Start, Integer(BufPtr - Start));
  if BufPtr^ = #13 then Inc(BufPtr);
  if BufPtr^ = #10 then Inc(BufPtr);
  Result := BufPtr;
  *)

  (*
    aChar := chr(0);
  result := '';
  while not eof(theTextFile) do
    begin
    read(theTextFile, aChar);
    if (aChar <> kTextFilerDelimiter) and (aChar <> chr(9)) and (aChar <> chr(10)) and (aChar <> chr(13)) then
      result := result + aChar
    else
      begin
      if (aChar = chr(13)) and not eof(theTextFile) then
        begin
        read(theTextFile, aChar);
        if aChar <> chr(10) then
          raise Exception.create('Problem in file input');
        end;
      break;
      end;
    end;
  atEndOfFile := eof(theTextFile);
*)

{ ------------------------------------------------------------------------ text handling }
function limitString(aString: string; maxChars: smallint): string;
  begin
  result := aString;
  if length(aString) > maxChars then
    result := copy(aString, 1, maxChars - 3) + '...';
  end;

function replacePunctuationWithUnderscores(aString: string): string;
  var
    i: integer;
    lowerCaseString: string;
    isAlpha: boolean;
  begin
  result := '';
  lowerCaseString := lowerCase(aString);
  if length(aString) > 0 then
    for i := 1 to length(aString) do
      begin
      isAlpha :=
          (ord(lowerCaseString[i]) >= ord('a')) and (ord(lowerCaseString[i]) <= ord('z')) or
    			(ord(lowerCaseString[i]) >= ord('0')) and (ord(lowerCaseString[i]) <= ord('9'));
      if isAlpha then
        result := result + aString[i]
      else
        result := result + '_';
      end;
  end;

function replaceCommasWithPeriods(aString: string): string;
  var
    i: integer;
    isComma: boolean;
  begin
  result := '';
  if length(aString) > 0 then
    for i := 1 to length(aString) do
      begin
      isComma := aString[i] = ',';
      if not isComma then
        result := result + aString[i]
      else
        result := result + '.';
      end;
  end;

function found(substring, fullString: string): boolean;
  begin
  result := pos(substring, fullString) > 0;
  end;

function trimQuotesFromFirstAndLast(theString: string): string;
  begin
  result := theString;
  if length(result) <= 0 then exit;

  if result[1] = '"' then
    result := copy(result, 2, length(result) - 1);
  if result[length(result)] = '"' then
    setLength(result, length(result) - 1);
  end;

function capitalize(aString: string): string;
  begin
  result := '';
  if length(aString) <= 0 then exit;
  if length(aString) = 1 then
    result := upperCase(aString)
  else
    result := upperCase(copy(aString, 1, 1)) + copy(aString, 2, length(aString) - 1);
  end;

function readUntilTab(var theFile: textFile): string;
  var
    aChar: char;
  begin
  aChar := chr(0);
  result := '';
  while not eof(theFile) do
    begin
    read(theFile, aChar);
    if (aChar <> chr(9)) and (aChar <> chr(10)) and (aChar <> chr(13)) then
      result := result + aChar
    else
      begin
      if (aChar = chr(13)) and not eof(theFile) then
        begin
        read(theFile, aChar);
        if aChar <> chr(10) then
          raise Exception.create('Problem: Something unexpected in file input.');
        end;
      break;
      end;
    end;
  { remove quotes placed by spreadsheet around string if it has a comma in it }
  if (copy(result, 1, 1) = '"') and (copy(result, length(result), 1) = '"') then
  {if (result[1] = '"') and (result[length(result)] = '"') then }
    result := copy(result, 2, length(result) - 2);
  end;

function readShortStringToTab(var fileRef: TextFile): string;
  var temp: string;
  begin
  temp := readUntilTab(fileRef);
  result := copy(temp, 1, 80);
  end;

function readSmallintToTab(var fileRef: TextFile): smallint;
  var ignore: string;
  begin
  result := 0;
  read(fileRef, result);
  ignore := readUntilTab(fileRef);
  end;

function readSingleToTab(var fileRef: TextFile): single;
  var temp: string;
  begin
  result := 0.0;
  temp := readUntilTab(fileRef);
  { boundForString returns false if unsuccessful, but not doing anything with result yet }
  boundForString(temp, kFieldFloat, result);
  end;

function readBooleanToTab(var fileRef: TextFile): boolean;
  var
    booleanString: string;
  begin
  booleanString := readUntilTab(fileRef);
  if (upperCase(booleanString) = 'TRUE') then
    result := true
  else if (upperCase(booleanString) = 'FALSE') then
    result := false
  else
    raise Exception.create('Problem: Improper file format for boolean; found: ' + booleanString);
  end;

function boundForString(boundString: string; fieldType: integer; var number): boolean;
{returns whether conversion was successful}
  var
    piTimesTwo: single;
  begin
  result := true;
  if (boundString = 'MIN') or (boundString = 'FLT_MIN') then
    begin
    if fieldType = kFieldFloat then
      single(number) := kMinSingle
    else
      smallint(number) := -32768
    end
  else if (boundString = 'MAX') or (boundString = 'FLT_MAX')  then
    begin
    if fieldType = kFieldFloat then
      single(number) := kMaxSingle
    else
      smallint(number) := 32767;
    end
  else if (boundString = 'PI*2') and (fieldType = kFieldFloat) then
    begin
    piTimesTwo := pi * 2.0;
    single(number) := piTimesTwo;
    end
  else if (boundString = '')  then
    begin
    if fieldType = kFieldFloat then
      single(number) := 0.0
    else
      smallint(number) := 0;
    end
  else
    try
      if fieldType = kFieldFloat then
        single(number) := StrToFloat(boundString)
      else
        smallint(number) := StrToInt(boundString);
    except
      on EConvertError do
        begin
        result := false;
        if fieldType = kFieldFloat then
          single(number) := 0.0
        else
          smallint(number) := 0;
        end;
    end;
  end;

function trimLeftAndRight(theString: string): string;
  begin
  result := trim(theString);
  end;

function stringUpTo(aString, aDelimiter: string): string;
  var
    delimiterPos: smallint;
  begin
  if length(aString) = 0 then
    begin
    result := '';
    exit;
    end;
  delimiterPos := pos(aDelimiter, aString);
  if delimiterPos = 0 then
    result := aString
  else if delimiterPos = 1 then
    result := ''
  else
    result := copy(aString, 1, delimiterPos - 1);
  end;

function stringBeyond(aString, aDelimiter: string): string;
  var
    delimiterPos: smallint;
  begin
  if length(aString) = 0 then
    begin
    result := '';
    exit;
    end;
  delimiterPos := pos(aDelimiter, aString);
  if delimiterPos = 0 then
    result := aString
  else if delimiterPos = length(aString) then
    result := ''
  else
    result := copy(aString, delimiterPos + 1, length(aString) - delimiterPos);
  end;

function stringBetween(startString, endString, wholeString: string): string;
  begin
  result := stringUpTo(stringBeyond(trim(wholeString), startString), endString);
  end;
  { didn't use, don't know if works
function listOfStringsBetweenDelimiters(aString, aDelimiter: string): TStrings;
  var token: string;
  begin
  result := TStrings.create; // caller must free this
  while length(aString) > 0 do
    begin
    token := stringUpTo(aString, aDelimiter);
    aString := stringBeyond(aString, aDelimiter);
    result.add(token);
    end;
  end;
     }
function boolToStr(value: boolean): string;
  begin
  if value then
    result := 'true'
  else
    result := 'false';
  end;

function strToBool(booleanString: string): boolean;
  begin
  result := false;
  if booleanString = '' then exit;
  if (upperCase(booleanString) = 'TRUE') then
    result := true
  else if (upperCase(booleanString) = 'FALSE') then
    result := false;
  end;

procedure messageForExceptionType(e: Exception; methodName: string);
  var errorString: string;
  begin
  if e = nil then exit;
  if (e is EZeroDivide) then
    errorString := 'Problem: Floating-point divide by zero error in method ' + methodName + '.'
  else if (e is EDivByZero) then
	  errorString := 'Problem: Integer divide by zero in method ' + methodName + '.'
  else if (e is EInvalidOp) then
	  errorString := 'Problem: Invalid floating-point operation in method ' + methodName + '.'
  else if (e is EOverFlow) then
	  errorString := 'Problem: Floating-point overflow in method ' + methodName + '.'
  else if (e is EUnderFlow) then
	  errorString := 'Problem: Floating-point underflow in method ' + methodName + '.'
  else
    errorString := 'Problem in method ' + methodName + '.';
  errorString := errorString + chr(13) + chr(13) + e.message;
  ErrorMessage(errorString);
  end;

{ ---------------------------------------------------------------------------- float to text conversion }
function removeTrailingZeros(theString: string): string;
  begin
  while (length(theString) > 1)
    and (theString[length(theString)] = '0') and (theString[length(theString) - 1] <> '.')
    do {dec(theString[0]);  } setLength(theString, length(theString) - 1);
  result := theString;
  end;

function shortenLongNonZeroDigitsAfterDecimal(theString: string; maxDigits: integer): string;
  var
    pointPos, firstNonZeroDigit, digitsToGetRidOf: longint;
  begin
  result := theString;
  pointPos := pos('.', result);
  if pointPos <> 0 then
    begin
    firstNonZeroDigit := pointPos + 1;
    while (firstNonZeroDigit <= length(theString)) and (theString[firstNonZeroDigit] = '0') do
      inc(firstNonZeroDigit);
    if firstNonZeroDigit < length(theString) then
      begin
      digitsToGetRidOf := length(theString) - firstNonZeroDigit + 1 - maxDigits;
      if digitsToGetRidOf > 0 then
        result := copy(result, 1, length(theString) - digitsToGetRidOf);
      end;
    end;
  end;

function digitValueString(value: single): string;
  begin
  result := removeTrailingZeros(shortenLongNonZeroDigitsAfterDecimal(floatToStrF(value, ffFixed, 7, 8), 2));
  end;

function valueString(value: single): string;
  begin
  result := removeTrailingZeros(shortenLongNonZeroDigitsAfterDecimal(floatToStrF(value, ffFixed, 7, 8), 4));
  end;

{ ---------------------------------------------------------------------------- graphics }
function clientRectToScreenRect(handle: HWnd; clientRect: TRect): TRect;
  var
    p1, p2: TPoint;
  begin
  p1 := point(clientRect.left, clientRect.top);
  clientToScreen(handle, p1);
  p2 := point(clientRect.right, clientRect.bottom);
  clientToScreen(handle, p2);
  result := rect(p1.x, p1.y, p2.x, p2.y);
  end;

function support_rgb(R: Byte; G: Byte; B: Byte): LongInt;
  //var screenDC: HDC;
  begin
  {result := RGB(r, g, b);  }
  //try
  //  screenDC := GetDC(0);
  //  result := GetNearestColor(screenDC, PALETTERGB(r, g, b));
  //finally
 //   releaseDC(0, screenDC);
  //end;
  result := PALETTERGB(r, g, b);
  end;

function combineRects(rect1, rect2: TRect): TRect;
  begin
  with result do
    begin
    left := intMin(rect1.left, rect2.left);
    right := intMax(rect1.right, rect2.right);
    top := intMin(rect1.top, rect2.top);
    bottom := intMax(rect1.bottom, rect2.bottom);
    end;
  end;

procedure addRectToBoundsRect(var boundsRect: TRect; const newRect: TRect);
	begin
  with boundsRect do
    begin
    // on first rect entered, initialize bounds rect
    if (left = 0) and (right = 0) and (top = 0) and (bottom = 0) then
      begin
      left := newRect.left;
      right := newRect.right;
      top := newRect.top;
      bottom := newRect.bottom;
      end
    else
      begin
      // deal with possibility of rectangle being flipped, so left > right or top > bottom
      // expand rectangle to include left side x
  		if newRect.left < left then
  			left := newRect.left
    	else if newRect.left > right then
      	right := newRect.left;
      // expand rectangle to include right side x
  		if newRect.right < left then
  			left := newRect.right
    	else if newRect.right > right then
      	right := newRect.right;
      // expand rectangle to include top y
    	if newRect.top < top then
      	top := newRect.top
    	else if newRect.top > bottom then
      	bottom := newRect.top;
      // expand rectangle to include bottom y
    	if newRect.bottom < top then
      	top := newRect.bottom
    	else if newRect.bottom > bottom then
      	bottom := newRect.bottom;
    	end;
    end;
  end;

function rWidth(rect: TRect): integer;
  begin
  result := rect.right - rect.left;
  end;

function rHeight(rect: TRect): integer;
  begin
  result := rect.bottom - rect.top;
  end;

function zeroRect(rect: TRect): boolean;
  begin
  with rect do result := (left = 0) and (top = 0) and (right = 0) and (bottom = 0);
  end;

function rectsAreIdentical(oneRect, twoRect: TRect): boolean;
  begin
  result := (oneRect.top = twoRect.top) and (oneRect.bottom = twoRect.bottom)
    and (oneRect.left = twoRect.left) and (oneRect.right = twoRect.right);
  end;

function rectToString(aRect: TRect): string;
  begin
  result := intToStr(aRect.left) + ' ' + intToStr(aRect.top) + ' ' + intToStr(aRect.right) + ' ' + intToStr(aRect.bottom);
  end;

function stringToRect(aString: string): TRect;
	var
    stream: KfStringStream;
  begin
  result := rect(0,0,0,0);
  stream := KfStringStream.create;
  try
    stream.onStringSeparator(aString, ' ');
    result.left := strToIntDef(stream.nextToken, 0);
    result.top := strToIntDef(stream.nextToken, 0);
    result.right := strToIntDef(stream.nextToken, 0);
    result.bottom := strToIntDef(stream.nextToken, 0);
  finally
    stream.free;
  end;
  end;

function pointToString(aPoint: TPoint): string;
  begin
  result := intToStr(aPoint.x) + '  ' + intToStr(aPoint.y);
  end;

function stringToPoint(aString: string): TPoint;
	var
    stream: KfStringStream;
  begin
  result := point(0,0);
  stream := KfStringStream.create;
  try
    stream.onStringSeparator(aString, ' ');
    result.x := strToIntDef(stream.nextToken, 0);
    result.y := strToIntDef(stream.nextToken, 0);
  finally
    stream.free;
  end;
  end;

function setSinglePoint(x, y: single): SinglePoint;
  begin
  result.x := x;
  result.y := y;
  end;

function singlePointToString(aPoint: SinglePoint): string;
  begin
  result := digitValueString(aPoint.x) + '  ' + digitValueString(aPoint.y);
  end;

function stringToSinglePoint(aString: string): SinglePoint;
	var
    stream: KfStringStream;
    token: string;
  begin
  result := setSinglePoint(0,0);
  stream := KfStringStream.create;
  try
    stream.onStringSeparator(aString, ' ');
    token := stream.nextToken;
    // if it was written as an integer, deal with that
    if pos('.', token) = 0 then
      result.x := strToIntDef(token, 0)
    else
      try
        result.x := strToFloat(token);
      except
        result.x := 0.0;
      end;
    token := stream.nextToken;
    if pos('.', token) = 0 then
      result.y := strToIntDef(token, 0)
    else
      try
        result.y := strToFloat(token);
      except
        result.y := 0.0;
      end;
  finally
    stream.free;
  end;
  end;

function colorToRGBString(color: TColorRef): string;
  begin
  result := intToStr(getRValue(color)) + ' ' + intToStr(getGValue(color)) + ' ' + intToStr(getBValue(color));
  end;

function rgbStringToColor(aString: string): TColorRef;
	var
    stream: KfStringStream;
    r, g, b: byte;
  begin
  { format is r g b }
  result := 0; r := 0; g := 0; b := 0;
  stream := KfStringStream.create;
  try
    stream.onStringSeparator(aString, ' ');
    r := strToIntDef(stream.nextToken, 0);
    g := strToIntDef(stream.nextToken, 0);
    b := strToIntDef(stream.nextToken, 0);
    result := rgb(r,g,b);
  finally
    stream.free;
  end;
  end;

{ ---------------------------------------------------------------------------------- color functions }
function blendColors(firstColor: TColorRef; secondColor: TColorRef; aStrength: single): TColorRef;
  var
    r1, g1, b1, r2, g2, b2: byte;
  begin
  {blend first color with second color,
   weighting the second color by aStrength (0-1) and first color by (1 - aStrength).}
  aStrength := max(0.0, min(1.0, aStrength));
  r1 := intMax(0, intMin(255, GetRValue(firstColor)));
  g1 := intMax(0, intMin(255, GetGValue(firstColor)));
  b1 := intMax(0, intMin(255, GetBValue(firstColor)));
  r2 := intMax(0, intMin(255, GetRValue(secondColor)));
  g2 := intMax(0, intMin(255, GetGValue(secondColor)));
  b2 := intMax(0, intMin(255, GetBValue(secondColor)));
  result := support_rgb(
    round(r1 * (1.0 - aStrength) + r2 * aStrength),
    round(g1 * (1.0 - aStrength) + g2 * aStrength),
    round(b1 * (1.0 - aStrength) + b2 * aStrength));
  end;

function darkerColor(aColor: TColorRef): TColorRef;
  var r, g, b: word;
  begin
  r := intMax(0, GetRValue(aColor) - 10);
  g := intMax(0, GetGValue(aColor) - 10);
  b := intMax(0, GetBValue(aColor) - 10);
  result := support_rgb(r, g, b);
  {result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); }
  end;

function darkerColorWithSubtraction(aColor: TColorRef; subtract: smallint): TColorRef;
  var r, g, b: word;
  begin
  r := intMax(0, GetRValue(aColor) - subtract);
  g := intMax(0, GetGValue(aColor) - subtract);
  b := intMax(0, GetBValue(aColor) - subtract);
  result := support_rgb(r, g, b);
  {result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); }
  end;

function lighterColor(aColor: TColorRef): TColorRef;
  var r, g, b: word;
  begin
  r := intMin(255, round(GetRValue(aColor) * 1.5));
  g := intMin(255, round(GetGValue(aColor) * 1.5));
  b := intMin(255, round(GetBValue(aColor) * 1.5));
  result := support_rgb(r, g, b);
  {result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); }
  end;

procedure drawButton(aCanvas: TCanvas; aRect: TRect; selected: boolean;  enabled: boolean);
  var
    internalRect: TRect;
  begin
  with aCanvas do
    begin
    brush.style := bsSolid;
    if enabled then
      begin
      pen.color := clBlack;
      brush.color := clWhite;
      end
    else
      begin
      brush.color := clBtnShadow;
      pen.color := clBtnShadow;
      end;
    with aRect do rectangle(left, top, right, bottom);
    if selected then
      begin
      internalRect := aRect;
      inflateRect(internalRect, -1, -1);
      brush.color := clAqua;
      fillRect(internalRect);
      end;
    end;
  end;

function draw3DButton(ACanvas: TCanvas;  Client: TRect; Selected: Boolean;  Pressed: Boolean): TRect;
  begin
  with ACanvas do
    begin
    Brush.Color := clWindowFrame;
    if Selected then
      begin
      FrameRect(Client);
      InflateRect(Client, -1, -1);
      end;
    if not Pressed then
      Frame3d(ACanvas, Client, clBtnHighlight, clBtnShadow, 2)
    else
      with Client do
        begin
        Pen.Color := clBtnShadow;
        PolyLine([Point(Left, Bottom - 1), Point(Left, Top), Point(Right, Top)]);
        Client := Rect(Left + 3, Top + 3, Right - 1, Bottom - 1);
        end;
    brush.Color := clBtnFace;
    FillRect(Client);
    end;
  result := client;
  end;

{ ---------------------------------------------------------------------------- combo and list box utilities }
function currentObjectInComboBox(comboBox: TComboBox): TObject;
  begin
  if comboBox.items.count = 0 then
    result := nil
  else if comboBox.itemIndex <> -1 then
    result := comboBox.items.objects[comboBox.itemIndex]
  else
    result := nil;
  end;

function currentObjectInListBox(listBox: TListBox): TObject;
  begin
  if listBox.items.count = 0 then
    result := nil
  else if listBox.itemIndex <> -1 then
    result := listBox.items.objects[listBox.itemIndex]
  else
    result := nil;
  end;

{ ---------------------------------------------------------------------------- file i/o }
function makeFileNameFrom(aString: string): string;
  var
    done: boolean;
    spacePos: smallint;
  begin
  result := aString;
  done := false;
  while not done do
    begin
    spacePos := pos(' ', result);
    done := (spacePos <= 0);
    if not done then delete(result, spacePos, 1);
    end;
  end;

function nameStringForFileType(fileType: smallint): string;
  begin
  case fileType of
    kFileTypeAny: result := '';
    kFileTypePlant: result := 'Plant';
    kFileTypeTabbedText: result := 'Tabbed text';
    kFileTypeStrategy: result := 'Strategy';
    kFileTypeIni: result := 'Ini';
    kFileTypeExceptionList: result := 'Exception list';
    kFileTypeBitmap: result := 'Bitmap';
    kFileTypeTdo: result := '3D object';
    kFileTypeDXF: result := 'DXF';
    kFileTypeINC: result := 'POV Include file';
    kFileType3DS: result := '3DS';
    kFileTypeProgramInfo: result := 'Program Info';
    kFileTypeJPEG: result := 'JPEG';
    kFileTypeOBJ: result := 'OBJ';
    kFileTypeMTL: result := 'MTL';
    kFileTypeVRML: result := 'VRML';
    kFileTypeLWO: result := 'LWO';
    end;
  end;

function extensionForFileType(fileType: smallint): string;
  begin
  result := '';
  case fileType of
    kFileTypeAny: result := '*';
    kFileTypePlant: result := 'pla';
    kFileTypeTabbedText: result := 'tab';
    kFileTypeStrategy: result := 'str';
    kFileTypeIni: result := 'ini';
    kFileTypeExceptionList: result := 'nex';
    kFileTypeBitmap: result := 'bmp';
    kFileTypeTdo: result := 'tdo';
    kFileTypeDXF: result := 'dxf';
    kFileTypeINC: result := 'inc';
    kFileType3DS: result := '3ds';
    kFileTypeProgramInfo: result := 'txt';
    kFileTypeJPEG: result := 'jpg';
    kFileTypeOBJ: result := 'obj';
    kFileTypeMTL: result := 'mtl';
    kFileTypeVRML: result := 'wrl';
    kFileTypeLWO: result := 'lwo';
    end;
  end;

function filterStringForFileType(fileType: smallint; includeAllFiles: boolean): string;
  var extension: string;
  begin
  extension := extensionForFileType(fileType);
  if fileType = kFileTypeAny then
    result := 'All files (*.*)|*.*'
  else
    if includeAllFiles then
      result := nameStringForFileType(fileType) + ' files (*.' + extension + ')|*.' + extension +
        '|All files (*.*)|*.*'
    else
      result := nameStringForFileType(fileType) + ' files (*.' + extension + ')|*.' + extension;
  end;

function getFileOpenInfo(fileType: smallint; const suggestedFile: string; aTitle: string): string;
  var
    fullSuggestedFileName: string;
    openDialog: TOpenDialog;
    nameString: string;
  begin
  result := '';
  openDialog := TOpenDialog.create(Application);
  try
  with openDialog do
    begin
    if suggestedFile = '' then
      begin
      fileName := '*.' + extensionForFileType(fileType);
      end
    else
      begin
      fullSuggestedFileName := expandFileName(suggestedFile);
      { if directory does not exist, will leave as it was }
      initialDir := extractFilePath(fullSuggestedFileName);
      if fileExists(fullSuggestedFileName) then fileName := extractFileName(fullSuggestedFileName);
      end;
    nameString := nameStringForFileType(fileType);
    if length(aTitle) > 0 then
      title := aTitle
    else if nameString[1] in ['A', 'E', 'I', 'O', 'U'] then
      title := 'Choose an ' + nameString + ' file'
    else
      title := 'Choose a ' + nameString + ' file';
    filter := filterStringForFileType(fileType, kIncludeAllFiles);
    defaultExt := extensionForFileType(fileType);
    options := options + [ofPathMustExist, ofFileMustExist, ofHideReadOnly];
   end;
  if openDialog.execute then
    begin
    if (ofExtensionDifferent in openDialog.options) and (fileType <> kFileTypeAny) then
      begin
      showMessage('The file (' + openDialog.fileName
        + ') does not have the correct extension (' + openDialog.defaultExt + ').');
      exit;
      end
    else
      result := openDialog.fileName;
    end;
  finally
  openDialog.free;
  end;
  end;

function fileNameIsOkayForSaving(suggestedFile: string): boolean;
  var
    fullSuggestedFileName: string;
  begin
  result := false;
  if length(suggestedFile) = 0 then exit;
  fullSuggestedFileName := expandFileName(suggestedFile);
  { check if directory exists }
  if not directoryExists(extractFilePath(fullSuggestedFileName)) then
    begin
    showMessage('The directory ' + extractFilePath(fullSuggestedFileName) + ' does not exist.');
    exit;
    end;
  { if file exists and is writable, it's ok because Save (not Save As) should not ask to rewrite }
  { if file exists but is read-only, quit  }
  if fileExists(fullSuggestedFileName)
      and Boolean(FileGetAttr(fullSuggestedFileName) and faReadOnly) then
    begin
    showMessage('The file ' + fullSuggestedFileName + ' exists and is read-only.');
    exit;
    end;
  result := true;
  end;

function getFileSaveInfo(fileType: smallint; askForFileName: boolean;
    const suggestedFile: string; var fileInfo: SaveFileNamesStructure): boolean;
  var
    saveDialog: TSaveDialog;
    tryBackupName, tryTempName, fullSuggestedFileName, prompt, extension: string;
    index: smallint;
    tempFileHandle: longint;
    userAbortedSave: boolean;
 begin
 fileInfo.fileType := fileType;
  result := false;
  userAbortedSave := false;
  { default info }
  with fileInfo do
    begin
    tempFile := '';
    newFile := '';
    backupFile := '';
    writingWasSuccessful := false;
    end;
  { if this is a Save, try to set the file name from the suggestedFile given; if file name
    is invalid, set flag to move into Save As instead }
  if not askForFileName then
    begin
    askForFileName := not fileNameIsOkayForSaving(suggestedFile);
    if not askForFileName then fileInfo.newFile := expandFileName(suggestedFile);
    end;
  { if this is a Save As, or if this is a Save and the file in suggestedFile is invalid,
    ask user for a file name }
  if askForFileName then
    begin
    saveDialog := TSaveDialog.create(application);
    try
      with saveDialog do
        begin
        if length(suggestedFile) > 0 then
          begin
          fullSuggestedFileName := expandFileName(suggestedFile);
          { if directory does not exist, will leave as it was }
          initialDir := extractFilePath(fullSuggestedFileName);
          { don't check if file exists (because saving); check if dir exists }
          if directoryExists(extractFilePath(fullSuggestedFileName)) then
            fileName := extractFileName(fullSuggestedFileName);
          end;
        filter := filterStringForFileType(fileType, kDontIncludeAllFiles);
        defaultExt := extensionForFileType(fileType);
        options := options + [ofPathMustExist, ofOverwritePrompt, ofHideReadOnly, ofNoReadOnlyReturn];
        end;
    userAbortedSave := not saveDialog.execute;
    if not userAbortedSave then
      fileInfo.newFile := saveDialog.fileName;
    finally
      saveDialog.free;
      saveDialog := nil;
    end;
    end;
  if userAbortedSave then exit;
  { set backup file name, check if read-only }
  { changed backup file extension to put tilde first because it is better to have all backup files sort together }
  try
    extension := extractFileExt(fileInfo.newFile);   { includes dot }
    extension := '.~' + copy(extension, 2, 2);
  except
    extension := '.bak';
  end;
  tryBackupName := changeFileExt(fileInfo.newFile, extension); 
  if fileExists(tryBackupName) then
    begin
    if (boolean(fileGetAttr(tryBackupName) and faReadOnly)) then
      begin
      prompt := 'The backup file ' + tryBackupName + ' is read-only. Continue?';
      if messageDlg(prompt, mtConfirmation, [mbYes, mbNo], 0) <> mrYes then
        exit;
      end;
    end
  else
    fileInfo.backupFile := tryBackupName;
  { set temp file name }
  for index := 100 to 999 do
    begin
    tryTempName := changeFileExt(fileInfo.newFile, '.' + intToStr(index));
    if not fileExists(tryTempName) then
      begin
      fileInfo.tempFile := tryTempName;
      break;
      end;
    end;
  { if can't find unused temp file, quit }
  if fileInfo.tempFile = '' then
    begin
    showMessage('Could not create temporary file ' + tryTempName + '.');
    exit;
    end;
  { test whether temp file can be created }
  tempFileHandle := fileCreate(fileInfo.tempFile);
  if tempFileHandle > 0 then
    begin
    fileClose(tempFileHandle);
    if not deleteFile(fileInfo.tempFile) then
      begin
      showMessage('Problem with temporary file ' + fileInfo.tempFile + '.');
      exit;
      end;
    end
  else
    begin
    showMessage('Could not write to temporary file ' + fileInfo.tempFile + '.');
    exit;
    end;
  result := true;
  end;

procedure startFileSave(var fileInfo: SaveFileNamesStructure);
  begin
  cursor_startWait;
  end;

function fileIsExportFile(fileType: smallint): boolean;
  begin
  result := false;
  case fileType of
    kFileTypeBitmap, kFileTypeDXF, kFileTypeINC,
    kFileType3DS, kFileTypeJPEG, kFileTypeOBJ,
    kFileTypeVRML, kFileTypeLWO: result := true;
    end;
  end;

procedure cleanUpAfterFileSave(var fileInfo: SaveFileNamesStructure);
  var
    useBackup, renamingFailed, deletingFailed: boolean;
    prompt: string;
  begin
  cursor_stopWait;
  stopWaitMessage;
  useBackup := true;
  {if couldn't write, then remove temp file and exit without warning}
  if not fileInfo.writingWasSuccessful then
    begin
    deleteFile(fileInfo.tempFile);
    exit;
    end;
  {remove backup file if exists from prior backup}
  if fileInfo.backupFile <> '' then
    begin
    if fileExists(fileInfo.backupFile) then
      begin
      {try to delete backup file}
      deletingFailed := not deleteFile(fileInfo.backupFile);
      if deletingFailed then
        begin
        {couldn't delete backup file}
        prompt := 'Could not write backup file ' + fileInfo.backupFile + '. Continue?';
        if messageDlg(prompt, mtConfirmation, [mbYes, mbNo], 0) <> mrYes then
          begin
          {user doesn't want to proceed - so cleanup temp file}
          deleteFile(fileInfo.tempFile);
          exit;
          end
        else
          useBackup := false;
        end;
      end
    end
  else
    useBackup := false;
  {if original file exists make backup if requested...}
  if fileExists(fileInfo.newFile) then
    begin
    if useBackup then
      begin
      {rename old copy of new file to make backup}
      renamingFailed := not renameFile(fileInfo.newFile, fileInfo.backupFile);
      if renamingFailed then
        begin
        prompt := 'Could not rename old file to backup file ' + fileInfo.backupFile + '. Continue?';
        if messageDlg(prompt, mtConfirmation, [mbYes, mbNo], 0) <> mrYes then
          begin
          {user doesn't want to proceed - so cleanup temp file}
          deleteFile(fileInfo.tempFile);
          exit;
          end
        else
          useBackup := false;
        end;
      end;
    {could not create backup file - so just delete old file instead of renaming}
    if not useBackup then
      begin
      deletingFailed := not deleteFile(fileInfo.newFile);
      if deletingFailed then
        begin
        ShowMessage('Could not write file ' + fileInfo.newFile);
        exit;
        end;
      end;
    end;
  {rename temp file to newFile name}
  renamingFailed := not renameFile(fileInfo.tempFile, fileInfo.newFile);
  if renamingFailed then
    begin
    {clean up by removing temp file}
    ShowMessage('Could not write file ' + fileInfo.newFile + ' from ' + fileInfo.tempFile);
    DeleteFile(fileInfo.tempFile);
    exit;
    end;
  if (not domain.registered) and (fileInfo.writingWasSuccessful) and (fileIsExportFile(fileInfo.fileType)) then
    MainForm.incrementUnregisteredExportCount;
  end;

procedure setDecimalSeparator; // v1.5
  begin
  // called before opening any file for reading or writing
  // to prevent problem with european comma separation
  DecimalSeparator := '.';
  end;

begin
gVersionName := 'Version 2.10';
iniFileChanged := false;
end.
