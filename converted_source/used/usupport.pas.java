// unit Usupport

from conversion_common import *;
import umain;
import udomain;
import usstream;
import umath;
import uparams;
import delphi_compatability;

// var
boolean iniFileChanged = false;
String gVersionName = "";


// const
kMaxEvaluationTime_hours = 10;


// record
class SinglePoint {
    public float x;
    public float y;
    public float reservedZ;
}

// record
class SaveFileNamesStructure {
    public short fileType;
    public String tempFile;
    public String newFile;
    public String backupFile;
    public boolean writingWasSuccessful;
}

// const
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
kNoSuggestedFile = "";
kAskForFileName = true;
kDontAskForFileName = false;


// const
kMinSingle = -3.4e38;
kMaxSingle = 3.4e38;


// const
kIncludeAllFiles = true;
kDontIncludeAllFiles = false;


// don't like using constants for these, but can't find any functions that provide them 
public String rotateEncodeBy7(String aString) {
    result = "";
    int i = 0;
    char letter = ' ';
    
    result = "";
    for (i = 0; i <= len(aString) - 1; i++) {
        letter = aString[i + 1];
        result = result + chr((ord(letter) + 1) % 256);
    }
    return result;
}

public String hexEncode(String aString) {
    result = "";
    int i = 0;
    char letter = ' ';
    
    result = "";
    for (i = 0; i <= len(aString) - 1; i++) {
        // ((i+4) mod length(aString))
        letter = aString[i + 1];
        result = result + chr(ord("A") + (ord(letter) / 32));
        result = result + chr(ord("A") + (ord(letter) % 32));
    }
    return result;
}

public String hexUnencode(String encodedString) {
    result = "";
    int i = 0;
    char letter = ' ';
    int value = 0;
    
    result = "";
    value = 0;
    for (i = 0; i <= len(encodedString) - 1; i++) {
        letter = encodedString[i + 1];
        if (i % 2 == 0) {
            value = (ord(letter) - ord("A")) * 32;
        } else {
            value = value + (ord(letter) - ord("A"));
            result = result + chr(value);
        }
    }
    return result;
}

public double strToFloatWithCommaCheck(String aString) {
    result = 0.0;
    if (found(",", aString)) {
        aString = replaceCommasWithPeriods(aString);
    }
    result = StrToFloat(aString);
    return result;
}

public void makeEnterWorkAsTab(TForm form, TControl activeControl, char key) {
    if (form == null) {
        // this is to make enter work as tab in edit boxes on the form 
        return key;
    }
    if (activeControl == null) {
        return key;
    }
    if (!((activeControl instanceof delphi_compatability.TEdit) || (activeControl instanceof delphi_compatability.TComboBox) || (activeControl instanceof delphi_compatability.TSpinEdit))) {
        return key;
    }
    if (key == Character(13)) {
        key = Character(0);
        //next control
        UNRESOLVED.sendMessage(form.Handle, UNRESOLVED.Wm_NextDlgCtl, 0, 0);
    }
    return key;
}

public short bitsPerPixelForColorType(TPixelFormat colorType) {
    result = 0;
    HDC screenDC = new HDC();
    
    // default to max
    result = 32;
    switch (colorType) {
        case delphi_compatability.TPixelFormat.pfDevice:
            screenDC = UNRESOLVED.GetDC(0);
            try {
                result = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES));
            } finally {
                UNRESOLVED.ReleaseDC(0, screenDC);
            }
            break;
        case delphi_compatability.TPixelFormat.pf1bit:
            result = 1;
            break;
        case delphi_compatability.TPixelFormat.pf4bit:
            result = 4;
            break;
        case delphi_compatability.TPixelFormat.pf8bit:
            result = 8;
            break;
        case delphi_compatability.TPixelFormat.pf15bit:
            result = 15;
            break;
        case delphi_compatability.TPixelFormat.pf16bit:
            result = 16;
            break;
        case delphi_compatability.TPixelFormat.pf24bit:
            result = 24;
            break;
        case delphi_compatability.TPixelFormat.pf32bit:
            result = 32;
            break;
        case delphi_compatability.TPixelFormat.pfCustom:
            // just use largest
            result = 32;
            break;
    return result;
}

//, extraCharToCarryOver
public void tolerantReadln(TextFile aFile, String aString) {
    UNRESOLVED.readln(aFile, aString);
    return aString;
}

// text handling 
// CFK unfinished - was trying to deal with text files that have irregular line endings
// such as CR but not LF or just LF
// did not finish - not often found
// got files from user frank salinas as test cases - look at these (in PS longterm) if look at this again later
//  var aChar: char;
//
//  aString := '';
//  aChar := chr(32);
//  // chr(26) is returned if read reaches eof
//  while (not eof(aFile)) and (not (aChar in [#0, #10, #13, #26])) do
//    begin
//    read(aFile, aChar);
//    if not (aChar in [#0, #10, #13, #26]) then
//      aString := aString + aChar
//    else
//      begin
//      read(aFile, aChar);
//      if not (aChar in [#0, #10, #13, #26]) then
//        extraCharToCarryOver := '' + aChar;
//      end;
//    end;
//
//  aChar := chr(32);
//  aString := '';
//  while not eof(aFile) do
//    begin
//    read(aFile, aChar);
//    if not (aChar in [#0, #10, #13, #26]) then
//      result := result + aChar
//    else
//      begin
//      if (aChar = chr(13)) and not eof(aFile) then
//        begin
//        read(theTextFile, aChar);
//        if aChar <> chr(10) then
//          raise Exception.create('Problem in file input');
//        end;
//      break;
//      end;
//    end;
//
//
//  end;
//  
//
//  Start := BufPtr;
//  while not (BufPtr^ in [#13, #26]) do Inc(BufPtr);
//  SetString(S, Start, Integer(BufPtr - Start));
//  if BufPtr^ = #13 then Inc(BufPtr);
//  if BufPtr^ = #10 then Inc(BufPtr);
//  Result := BufPtr;
//  
//
//    aChar := chr(0);
//  result := '';
//  while not eof(theTextFile) do
//    begin
//    read(theTextFile, aChar);
//    if (aChar <> kTextFilerDelimiter) and (aChar <> chr(9)) and (aChar <> chr(10)) and (aChar <> chr(13)) then
//      result := result + aChar
//    else
//      begin
//      if (aChar = chr(13)) and not eof(theTextFile) then
//        begin
//        read(theTextFile, aChar);
//        if aChar <> chr(10) then
//          raise Exception.create('Problem in file input');
//        end;
//      break;
//      end;
//    end;
//  atEndOfFile := eof(theTextFile);
//
// ------------------------------------------------------------------------ text handling 
public String limitString(String aString, short maxChars) {
    result = "";
    result = aString;
    if (len(aString) > maxChars) {
        result = UNRESOLVED.copy(aString, 1, maxChars - 3) + "...";
    }
    return result;
}

public String replacePunctuationWithUnderscores(String aString) {
    result = "";
    int i = 0;
    String lowerCaseString = "";
    boolean isAlpha = false;
    
    result = "";
    lowerCaseString = lowercase(aString);
    if (len(aString) > 0) {
        for (i = 1; i <= len(aString); i++) {
            isAlpha = (ord(lowerCaseString[i]) >= ord("a")) && (ord(lowerCaseString[i]) <= ord("z")) || (ord(lowerCaseString[i]) >= ord("0")) && (ord(lowerCaseString[i]) <= ord("9"));
            if (isAlpha) {
                result = result + aString[i];
            } else {
                result = result + "_";
            }
        }
    }
    return result;
}

public String replaceCommasWithPeriods(String aString) {
    result = "";
    int i = 0;
    boolean isComma = false;
    
    result = "";
    if (len(aString) > 0) {
        for (i = 1; i <= len(aString); i++) {
            isComma = aString[i] == ",";
            if (!isComma) {
                result = result + aString[i];
            } else {
                result = result + ".";
            }
        }
    }
    return result;
}

public boolean found(String substring, String fullString) {
    result = false;
    result = UNRESOLVED.pos(substring, fullString) > 0;
    return result;
}

public String trimQuotesFromFirstAndLast(String theString) {
    result = "";
    result = theString;
    if (len(result) <= 0) {
        return result;
    }
    if (result[1] == "\"") {
        result = UNRESOLVED.copy(result, 2, len(result) - 1);
    }
    if (result[len(result)] == "\"") {
        UNRESOLVED.setLength(result, len(result) - 1);
    }
    return result;
}

public String capitalize(String aString) {
    result = "";
    result = "";
    if (len(aString) <= 0) {
        return result;
    }
    if (len(aString) == 1) {
        result = uppercase(aString);
    } else {
        result = uppercase(UNRESOLVED.copy(aString, 1, 1)) + UNRESOLVED.copy(aString, 2, len(aString) - 1);
    }
    return result;
}

public String readUntilTab(textFile theFile) {
    result = "";
    char aChar = ' ';
    
    aChar = chr(0);
    result = "";
    while (!UNRESOLVED.eof(theFile)) {
        UNRESOLVED.read(theFile, aChar);
        if ((aChar != chr(9)) && (aChar != chr(10)) && (aChar != chr(13))) {
            result = result + aChar;
        } else {
            if ((aChar == chr(13)) && !UNRESOLVED.eof(theFile)) {
                UNRESOLVED.read(theFile, aChar);
                if (aChar != chr(10)) {
                    throw new GeneralException.create("Problem: Something unexpected in file input.");
                }
            }
            break;
        }
    }
    if ((UNRESOLVED.copy(result, 1, 1) == "\"") && (UNRESOLVED.copy(result, len(result), 1) == "\"")) {
        // remove quotes placed by spreadsheet around string if it has a comma in it 
        //if (result[1] = '"') and (result[length(result)] = '"') then 
        result = UNRESOLVED.copy(result, 2, len(result) - 2);
    }
    return result;
}

public String readShortStringToTab(TextFile fileRef) {
    result = "";
    String temp = "";
    
    temp = readUntilTab(fileRef);
    result = UNRESOLVED.copy(temp, 1, 80);
    return result;
}

public short readSmallintToTab(TextFile fileRef) {
    result = 0;
    String ignore = "";
    
    result = 0;
    UNRESOLVED.read(fileRef, result);
    ignore = readUntilTab(fileRef);
    return result;
}

public float readSingleToTab(TextFile fileRef) {
    result = 0.0;
    String temp = "";
    
    result = 0.0;
    temp = readUntilTab(fileRef);
    // boundForString returns false if unsuccessful, but not doing anything with result yet 
    result = boundForString(temp, uparams.kFieldFloat, result);
    return result;
}

public boolean readBooleanToTab(TextFile fileRef) {
    result = false;
    String booleanString = "";
    
    booleanString = readUntilTab(fileRef);
    if ((uppercase(booleanString) == "TRUE")) {
        result = true;
    } else if ((uppercase(booleanString) == "FALSE")) {
        result = false;
    } else {
        throw new GeneralException.create("Problem: Improper file format for boolean; found: " + booleanString);
    }
    return result;
}

public boolean boundForString(String boundString, int fieldType, FIX_MISSING_ARG_TYPE number) {
    raise "method boundForString with preexisting function result had var parameters added to return; fixup manually"
    result = false;
    float piTimesTwo = 0.0;
    
    //returns whether conversion was successful
    result = true;
    if ((boundString == "MIN") || (boundString == "FLT_MIN")) {
        if (fieldType == uparams.kFieldFloat) {
            number = kMinSingle;
        } else {
            number = -32768;
        }
    } else if ((boundString == "MAX") || (boundString == "FLT_MAX")) {
        if (fieldType == uparams.kFieldFloat) {
            number = kMaxSingle;
        } else {
            number = 32767;
        }
    } else if ((boundString == "PI*2") && (fieldType == uparams.kFieldFloat)) {
        piTimesTwo = UNRESOLVED.pi * 2.0;
        number = piTimesTwo;
    } else if ((boundString == "")) {
        if (fieldType == uparams.kFieldFloat) {
            number = 0.0;
        } else {
            number = 0;
        }
    } else {
        try {
            if (fieldType == uparams.kFieldFloat) {
                number = StrToFloat(boundString);
            } else {
                number = StrToInt(boundString);
            }
        } catch (EConvertError e) {
            result = false;
            if (fieldType == uparams.kFieldFloat) {
                number = 0.0;
            } else {
                number = 0;
            }
        }
    }
    return result, number;
}

public String trimLeftAndRight(String theString) {
    result = "";
    result = trim(theString);
    return result;
}

public String stringUpTo(String aString, String aDelimiter) {
    result = "";
    short delimiterPos = 0;
    
    if (len(aString) == 0) {
        result = "";
        return result;
    }
    delimiterPos = UNRESOLVED.pos(aDelimiter, aString);
    if (delimiterPos == 0) {
        result = aString;
    } else if (delimiterPos == 1) {
        result = "";
    } else {
        result = UNRESOLVED.copy(aString, 1, delimiterPos - 1);
    }
    return result;
}

public String stringBeyond(String aString, String aDelimiter) {
    result = "";
    short delimiterPos = 0;
    
    if (len(aString) == 0) {
        result = "";
        return result;
    }
    delimiterPos = UNRESOLVED.pos(aDelimiter, aString);
    if (delimiterPos == 0) {
        result = aString;
    } else if (delimiterPos == len(aString)) {
        result = "";
    } else {
        result = UNRESOLVED.copy(aString, delimiterPos + 1, len(aString) - delimiterPos);
    }
    return result;
}

public String stringBetween(String startString, String endString, String wholeString) {
    result = "";
    result = stringUpTo(stringBeyond(trim(wholeString), startString), endString);
    return result;
}

// didn't use, don't know if works
//function listOfStringsBetweenDelimiters(aString, aDelimiter: string): TStrings;
//  var token: string;
//  begin
//  result := TStrings.create; // caller must free this
//  while length(aString) > 0 do
//    begin
//    token := stringUpTo(aString, aDelimiter);
//    aString := stringBeyond(aString, aDelimiter);
//    result.add(token);
//    end;
//  end;
//     
public String boolToStr(boolean value) {
    result = "";
    if (value) {
        result = "true";
    } else {
        result = "false";
    }
    return result;
}

public boolean strToBool(String booleanString) {
    result = false;
    result = false;
    if (booleanString == "") {
        return result;
    }
    if ((uppercase(booleanString) == "TRUE")) {
        result = true;
    } else if ((uppercase(booleanString) == "FALSE")) {
        result = false;
    }
    return result;
}

public void messageForExceptionType(Exception e, String methodName) {
    String errorString = "";
    
    if (e == null) {
        return;
    }
    if ((e instanceof UNRESOLVED.EZeroDivide)) {
        errorString = "Problem: Floating-point divide by zero error in method " + methodName + ".";
    } else if ((e instanceof UNRESOLVED.EDivByZero)) {
        errorString = "Problem: Integer divide by zero in method " + methodName + ".";
    } else if ((e instanceof UNRESOLVED.EInvalidOp)) {
        errorString = "Problem: Invalid floating-point operation in method " + methodName + ".";
    } else if ((e instanceof UNRESOLVED.EOverFlow)) {
        errorString = "Problem: Floating-point overflow in method " + methodName + ".";
    } else if ((e instanceof UNRESOLVED.EUnderFlow)) {
        errorString = "Problem: Floating-point underflow in method " + methodName + ".";
    } else {
        errorString = "Problem in method " + methodName + ".";
    }
    errorString = errorString + chr(13) + chr(13) + e.message;
    umath.ErrorMessage(errorString);
}

// float to text conversion 
// ---------------------------------------------------------------------------- float to text conversion 
public String removeTrailingZeros(String theString) {
    result = "";
    while ((len(theString) > 1) && (theString[len(theString)] == "0") && (theString[len(theString) - 1] != ".")) {
        //dec(theString[0]);  
        UNRESOLVED.setLength(theString, len(theString) - 1);
    }
    result = theString;
    return result;
}

public String shortenLongNonZeroDigitsAfterDecimal(String theString, int maxDigits) {
    result = "";
    long pointPos = 0;
    long firstNonZeroDigit = 0;
    long digitsToGetRidOf = 0;
    
    result = theString;
    pointPos = UNRESOLVED.pos(".", result);
    if (pointPos != 0) {
        firstNonZeroDigit = pointPos + 1;
        while ((firstNonZeroDigit <= len(theString)) && (theString[firstNonZeroDigit] == "0")) {
            firstNonZeroDigit += 1;
        }
        if (firstNonZeroDigit < len(theString)) {
            digitsToGetRidOf = len(theString) - firstNonZeroDigit + 1 - maxDigits;
            if (digitsToGetRidOf > 0) {
                result = UNRESOLVED.copy(result, 1, len(theString) - digitsToGetRidOf);
            }
        }
    }
    return result;
}

public String digitValueString(float value) {
    result = "";
    result = removeTrailingZeros(shortenLongNonZeroDigitsAfterDecimal(FloatToStrF(value, UNRESOLVED.ffFixed, 7, 8), 2));
    return result;
}

public String valueString(float value) {
    result = "";
    result = removeTrailingZeros(shortenLongNonZeroDigitsAfterDecimal(FloatToStrF(value, UNRESOLVED.ffFixed, 7, 8), 4));
    return result;
}

// graphics 
// ---------------------------------------------------------------------------- graphics 
public TRect clientRectToScreenRect(HWnd handle, TRect clientRect) {
    result = new TRect();
    TPoint p1 = new TPoint();
    TPoint p2 = new TPoint();
    
    p1 = Point(clientRect.Left, clientRect.Top);
    UNRESOLVED.clientToScreen(handle, p1);
    p2 = Point(clientRect.Right, clientRect.Bottom);
    UNRESOLVED.clientToScreen(handle, p2);
    result = Rect(p1.X, p1.Y, p2.X, p2.Y);
    return result;
}

public long support_rgb(byte R, byte G, byte B) {
    result = 0;
    //var screenDC: HDC;
    //result := RGB(r, g, b);  
    //try
    //  screenDC := GetDC(0);
    //  result := GetNearestColor(screenDC, PALETTERGB(r, g, b));
    //finally
    //   releaseDC(0, screenDC);
    //end;
    result = UNRESOLVED.PALETTERGB(R, G, B);
    return result;
}

public TRect combineRects(TRect rect1, TRect rect2) {
    result = new TRect();
    result.Left = umath.intMin(rect1.Left, rect2.Left);
    result.Right = umath.intMax(rect1.Right, rect2.Right);
    result.Top = umath.intMin(rect1.Top, rect2.Top);
    result.Bottom = umath.intMax(rect1.Bottom, rect2.Bottom);
    return result;
}

public void addRectToBoundsRect(TRect boundsRect, TRect newRect) {
    if ((boundsRect.Left == 0) && (boundsRect.Right == 0) && (boundsRect.Top == 0) && (boundsRect.Bottom == 0)) {
        // on first rect entered, initialize bounds rect
        boundsRect.Left = newRect.Left;
        boundsRect.Right = newRect.Right;
        boundsRect.Top = newRect.Top;
        boundsRect.Bottom = newRect.Bottom;
    } else {
        if (newRect.Left < boundsRect.Left) {
            // deal with possibility of rectangle being flipped, so left > right or top > bottom
            // expand rectangle to include left side x
            boundsRect.Left = newRect.Left;
        } else if (newRect.Left > boundsRect.Right) {
            boundsRect.Right = newRect.Left;
        }
        if (newRect.Right < boundsRect.Left) {
            // expand rectangle to include right side x
            boundsRect.Left = newRect.Right;
        } else if (newRect.Right > boundsRect.Right) {
            boundsRect.Right = newRect.Right;
        }
        if (newRect.Top < boundsRect.Top) {
            // expand rectangle to include top y
            boundsRect.Top = newRect.Top;
        } else if (newRect.Top > boundsRect.Bottom) {
            boundsRect.Bottom = newRect.Top;
        }
        if (newRect.Bottom < boundsRect.Top) {
            // expand rectangle to include bottom y
            boundsRect.Top = newRect.Bottom;
        } else if (newRect.Bottom > boundsRect.Bottom) {
            boundsRect.Bottom = newRect.Bottom;
        }
    }
}

public int rWidth(TRect rect) {
    result = 0;
    result = Rect.right - Rect.left;
    return result;
}

public int rHeight(TRect rect) {
    result = 0;
    result = Rect.bottom - Rect.top;
    return result;
}

public boolean zeroRect(TRect rect) {
    result = false;
    //FIX unresolved WITH expression: Rect
    result = (UNRESOLVED.left == 0) && (UNRESOLVED.top == 0) && (UNRESOLVED.right == 0) && (UNRESOLVED.bottom == 0);
    return result;
}

public boolean rectsAreIdentical(TRect oneRect, TRect twoRect) {
    result = false;
    result = (oneRect.Top == twoRect.Top) && (oneRect.Bottom == twoRect.Bottom) && (oneRect.Left == twoRect.Left) && (oneRect.Right == twoRect.Right);
    return result;
}

public String rectToString(TRect aRect) {
    result = "";
    result = IntToStr(aRect.Left) + " " + IntToStr(aRect.Top) + " " + IntToStr(aRect.Right) + " " + IntToStr(aRect.Bottom);
    return result;
}

public TRect stringToRect(String aString) {
    result = new TRect();
    KfStringStream stream = new KfStringStream();
    
    result = Rect(0, 0, 0, 0);
    stream = usstream.KfStringStream.create;
    try {
        stream.onStringSeparator(aString, " ");
        result.Left = StrToIntDef(stream.nextToken(), 0);
        result.Top = StrToIntDef(stream.nextToken(), 0);
        result.Right = StrToIntDef(stream.nextToken(), 0);
        result.Bottom = StrToIntDef(stream.nextToken(), 0);
    } finally {
        stream.free;
    }
    return result;
}

public String pointToString(TPoint aPoint) {
    result = "";
    result = IntToStr(aPoint.X) + "  " + IntToStr(aPoint.Y);
    return result;
}

public TPoint stringToPoint(String aString) {
    result = new TPoint();
    KfStringStream stream = new KfStringStream();
    
    result = Point(0, 0);
    stream = usstream.KfStringStream.create;
    try {
        stream.onStringSeparator(aString, " ");
        result.X = StrToIntDef(stream.nextToken(), 0);
        result.Y = StrToIntDef(stream.nextToken(), 0);
    } finally {
        stream.free;
    }
    return result;
}

public SinglePoint setSinglePoint(float x, float y) {
    result = new SinglePoint();
    result.x = x;
    result.y = y;
    return result;
}

public String singlePointToString(SinglePoint aPoint) {
    result = "";
    result = digitValueString(aPoint.x) + "  " + digitValueString(aPoint.y);
    return result;
}

public SinglePoint stringToSinglePoint(String aString) {
    result = new SinglePoint();
    KfStringStream stream = new KfStringStream();
    String token = "";
    
    result = setSinglePoint(0, 0);
    stream = usstream.KfStringStream.create;
    try {
        stream.onStringSeparator(aString, " ");
        token = stream.nextToken();
        if (UNRESOLVED.pos(".", token) == 0) {
            // if it was written as an integer, deal with that
            result.x = StrToIntDef(token, 0);
        } else {
            try {
                result.x = StrToFloat(token);
            } catch (Exception e) {
                result.x = 0.0;
            }
        }
        token = stream.nextToken();
        if (UNRESOLVED.pos(".", token) == 0) {
            result.y = StrToIntDef(token, 0);
        } else {
            try {
                result.y = StrToFloat(token);
            } catch (Exception e) {
                result.y = 0.0;
            }
        }
    } finally {
        stream.free;
    }
    return result;
}

public String colorToRGBString(TColorRef color) {
    result = "";
    result = IntToStr(UNRESOLVED.getRValue(color)) + " " + IntToStr(UNRESOLVED.getGValue(color)) + " " + IntToStr(UNRESOLVED.getBValue(color));
    return result;
}

public TColorRef rgbStringToColor(String aString) {
    result = new TColorRef();
    KfStringStream stream = new KfStringStream();
    byte r = 0;
    byte g = 0;
    byte b = 0;
    
    // format is r g b 
    result = 0;
    r = 0;
    g = 0;
    b = 0;
    stream = usstream.KfStringStream.create;
    try {
        stream.onStringSeparator(aString, " ");
        r = StrToIntDef(stream.nextToken(), 0);
        g = StrToIntDef(stream.nextToken(), 0);
        b = StrToIntDef(stream.nextToken(), 0);
        result = UNRESOLVED.rgb(r, g, b);
    } finally {
        stream.free;
    }
    return result;
}

// ---------------------------------------------------------------------------------- color functions 
public TColorRef blendColors(TColorRef firstColor, TColorRef secondColor, float aStrength) {
    result = new TColorRef();
    byte r1 = 0;
    byte g1 = 0;
    byte b1 = 0;
    byte r2 = 0;
    byte g2 = 0;
    byte b2 = 0;
    
    //blend first color with second color,
    //   weighting the second color by aStrength (0-1) and first color by (1 - aStrength).
    aStrength = umath.max(0.0, umath.min(1.0, aStrength));
    r1 = umath.intMax(0, umath.intMin(255, UNRESOLVED.GetRValue(firstColor)));
    g1 = umath.intMax(0, umath.intMin(255, UNRESOLVED.GetGValue(firstColor)));
    b1 = umath.intMax(0, umath.intMin(255, UNRESOLVED.GetBValue(firstColor)));
    r2 = umath.intMax(0, umath.intMin(255, UNRESOLVED.GetRValue(secondColor)));
    g2 = umath.intMax(0, umath.intMin(255, UNRESOLVED.GetGValue(secondColor)));
    b2 = umath.intMax(0, umath.intMin(255, UNRESOLVED.GetBValue(secondColor)));
    result = support_rgb(intround(r1 * (1.0 - aStrength) + r2 * aStrength), intround(g1 * (1.0 - aStrength) + g2 * aStrength), intround(b1 * (1.0 - aStrength) + b2 * aStrength));
    return result;
}

public TColorRef darkerColor(TColorRef aColor) {
    result = new TColorRef();
    byte r = 0;
    byte g = 0;
    byte b = 0;
    
    r = umath.intMax(0, UNRESOLVED.GetRValue(aColor) - 10);
    g = umath.intMax(0, UNRESOLVED.GetGValue(aColor) - 10);
    b = umath.intMax(0, UNRESOLVED.GetBValue(aColor) - 10);
    result = support_rgb(r, g, b);
    //result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); 
    return result;
}

public TColorRef darkerColorWithSubtraction(TColorRef aColor, short subtract) {
    result = new TColorRef();
    byte r = 0;
    byte g = 0;
    byte b = 0;
    
    r = umath.intMax(0, UNRESOLVED.GetRValue(aColor) - subtract);
    g = umath.intMax(0, UNRESOLVED.GetGValue(aColor) - subtract);
    b = umath.intMax(0, UNRESOLVED.GetBValue(aColor) - subtract);
    result = support_rgb(r, g, b);
    //result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); 
    return result;
}

public TColorRef lighterColor(TColorRef aColor) {
    result = new TColorRef();
    byte r = 0;
    byte g = 0;
    byte b = 0;
    
    r = umath.intMin(255, intround(UNRESOLVED.GetRValue(aColor) * 1.5));
    g = umath.intMin(255, intround(UNRESOLVED.GetGValue(aColor) * 1.5));
    b = umath.intMin(255, intround(UNRESOLVED.GetBValue(aColor) * 1.5));
    result = support_rgb(r, g, b);
    //result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); 
    return result;
}

public void drawButton(TCanvas aCanvas, TRect aRect, boolean selected, boolean enabled) {
    TRect internalRect = new TRect();
    
    aCanvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
    if (enabled) {
        aCanvas.Pen.Color = delphi_compatability.clBlack;
        aCanvas.Brush.Color = delphi_compatability.clWhite;
    } else {
        aCanvas.Brush.Color = UNRESOLVED.clBtnShadow;
        aCanvas.Pen.Color = UNRESOLVED.clBtnShadow;
    }
    aCanvas.Rectangle(aRect.Left, aRect.Top, aRect.Right, aRect.Bottom);
    if (selected) {
        internalRect = aRect;
        UNRESOLVED.inflateRect(internalRect, -1, -1);
        aCanvas.Brush.Color = delphi_compatability.clAqua;
        aCanvas.FillRect(internalRect);
    }
}

public TRect draw3DButton(TCanvas ACanvas, TRect Client, boolean Selected, boolean Pressed) {
    result = new TRect();
    ACanvas.Brush.Color = delphi_compatability.clWindowFrame;
    if (Selected) {
        ACanvas.FrameRect(Client);
        UNRESOLVED.InflateRect(Client, -1, -1);
    }
    if (!Pressed) {
        ACanvas.Frame3d(ACanvas, Client, UNRESOLVED.clBtnHighlight, UNRESOLVED.clBtnShadow, 2);
    } else {
        ACanvas.Pen.Color = UNRESOLVED.clBtnShadow;
        ACanvas.Polyline({Point(Client.Left, Client.Bottom - 1), Point(Client.Left, Client.Top), Point(Client.Right, Client.Top), });
        Client = Rect(Client.Left + 3, Client.Top + 3, Client.Right - 1, Client.Bottom - 1);
    }
    ACanvas.Brush.Color = UNRESOLVED.clBtnFace;
    ACanvas.FillRect(Client);
    result = Client;
    return result;
}

// combo and list box utilities 
// ---------------------------------------------------------------------------- combo and list box utilities 
public TObject currentObjectInComboBox(TComboBox comboBox) {
    result = new TObject();
    if (comboBox.Items.Count == 0) {
        result = null;
    } else if (comboBox.ItemIndex != -1) {
        result = comboBox.Items.Objects[comboBox.ItemIndex];
    } else {
        result = null;
    }
    return result;
}

public TObject currentObjectInListBox(TListBox listBox) {
    result = new TObject();
    if (listBox.Items.Count == 0) {
        result = null;
    } else if (listBox.ItemIndex != -1) {
        result = listBox.Items.Objects[listBox.ItemIndex];
    } else {
        result = null;
    }
    return result;
}

// file i/o 
// ---------------------------------------------------------------------------- file i/o 
public String makeFileNameFrom(String aString) {
    result = "";
    boolean done = false;
    short spacePos = 0;
    
    result = aString;
    done = false;
    while (!done) {
        spacePos = UNRESOLVED.pos(" ", result);
        done = (spacePos <= 0);
        if (!done) {
            UNRESOLVED.delete(result, spacePos, 1);
        }
    }
    return result;
}

public String nameStringForFileType(short fileType) {
    result = "";
    switch (fileType) {
        case kFileTypeAny:
            result = "";
            break;
        case kFileTypePlant:
            result = "Plant";
            break;
        case kFileTypeTabbedText:
            result = "Tabbed text";
            break;
        case kFileTypeStrategy:
            result = "Strategy";
            break;
        case kFileTypeIni:
            result = "Ini";
            break;
        case kFileTypeExceptionList:
            result = "Exception list";
            break;
        case kFileTypeBitmap:
            result = "Bitmap";
            break;
        case kFileTypeTdo:
            result = "3D object";
            break;
        case kFileTypeDXF:
            result = "DXF";
            break;
        case kFileTypeINC:
            result = "POV Include file";
            break;
        case kFileType3DS:
            result = "3DS";
            break;
        case kFileTypeProgramInfo:
            result = "Program Info";
            break;
        case kFileTypeJPEG:
            result = "JPEG";
            break;
        case kFileTypeOBJ:
            result = "OBJ";
            break;
        case kFileTypeMTL:
            result = "MTL";
            break;
        case kFileTypeVRML:
            result = "VRML";
            break;
        case kFileTypeLWO:
            result = "LWO";
            break;
    return result;
}

public String extensionForFileType(short fileType) {
    result = "";
    result = "";
    switch (fileType) {
        case kFileTypeAny:
            result = "*";
            break;
        case kFileTypePlant:
            result = "pla";
            break;
        case kFileTypeTabbedText:
            result = "tab";
            break;
        case kFileTypeStrategy:
            result = "str";
            break;
        case kFileTypeIni:
            result = "ini";
            break;
        case kFileTypeExceptionList:
            result = "nex";
            break;
        case kFileTypeBitmap:
            result = "bmp";
            break;
        case kFileTypeTdo:
            result = "tdo";
            break;
        case kFileTypeDXF:
            result = "dxf";
            break;
        case kFileTypeINC:
            result = "inc";
            break;
        case kFileType3DS:
            result = "3ds";
            break;
        case kFileTypeProgramInfo:
            result = "txt";
            break;
        case kFileTypeJPEG:
            result = "jpg";
            break;
        case kFileTypeOBJ:
            result = "obj";
            break;
        case kFileTypeMTL:
            result = "mtl";
            break;
        case kFileTypeVRML:
            result = "wrl";
            break;
        case kFileTypeLWO:
            result = "lwo";
            break;
    return result;
}

public String filterStringForFileType(short fileType, boolean includeAllFiles) {
    result = "";
    String extension = "";
    
    extension = extensionForFileType(fileType);
    if (fileType == kFileTypeAny) {
        result = "All files (*.*)|*.*";
    } else if (includeAllFiles) {
        result = nameStringForFileType(fileType) + " files (*." + extension + ")|*." + extension + "|All files (*.*)|*.*";
    } else {
        result = nameStringForFileType(fileType) + " files (*." + extension + ")|*." + extension;
    }
    return result;
}

public String getFileOpenInfo(short fileType, String suggestedFile, String aTitle) {
    result = "";
    String fullSuggestedFileName = "";
    TOpenDialog openDialog = new TOpenDialog();
    String nameString = "";
    
    result = "";
    openDialog = delphi_compatability.TOpenDialog().Create(delphi_compatability.Application);
    try {
        if (suggestedFile == "") {
            openDialog.FileName = "*." + extensionForFileType(fileType);
        } else {
            fullSuggestedFileName = ExpandFileName(suggestedFile);
            // if directory does not exist, will leave as it was 
            openDialog.InitialDir = ExtractFilePath(fullSuggestedFileName);
            if (FileExists(fullSuggestedFileName)) {
                openDialog.FileName = ExtractFileName(fullSuggestedFileName);
            }
        }
        nameString = nameStringForFileType(fileType);
        if (len(aTitle) > 0) {
            openDialog.Title = aTitle;
        } else if (nameString[1] in {"A", "E", "I", "O", "U", }) {
            openDialog.Title = "Choose an " + nameString + " file";
        } else {
            openDialog.Title = "Choose a " + nameString + " file";
        }
        openDialog.Filter = filterStringForFileType(fileType, kIncludeAllFiles);
        openDialog.DefaultExt = extensionForFileType(fileType);
        openDialog.Options = openDialog.Options + {delphi_compatability.TOpenOption.ofPathMustExist, delphi_compatability.TOpenOption.ofFileMustExist, delphi_compatability.TOpenOption.ofHideReadOnly, };
        if (openDialog.Execute()) {
            if ((delphi_compatability.TOpenOption.ofExtensionDifferent in openDialog.Options) && (fileType != kFileTypeAny)) {
                ShowMessage("The file (" + openDialog.FileName + ") does not have the correct extension (" + openDialog.DefaultExt + ").");
                return result;
            } else {
                result = openDialog.FileName;
            }
        }
    } finally {
        openDialog.free;
    }
    return result;
}

public boolean fileNameIsOkayForSaving(String suggestedFile) {
    result = false;
    String fullSuggestedFileName = "";
    
    result = false;
    if (len(suggestedFile) == 0) {
        return result;
    }
    fullSuggestedFileName = ExpandFileName(suggestedFile);
    if (!UNRESOLVED.directoryExists(ExtractFilePath(fullSuggestedFileName))) {
        // check if directory exists 
        ShowMessage("The directory " + ExtractFilePath(fullSuggestedFileName) + " does not exist.");
        return result;
    }
    if (FileExists(fullSuggestedFileName) && UNRESOLVED.FileGetAttr(fullSuggestedFileName) && UNRESOLVED.faReadOnly) {
        // if file exists and is writable, it's ok because Save (not Save As) should not ask to rewrite 
        // if file exists but is read-only, quit  
        ShowMessage("The file " + fullSuggestedFileName + " exists and is read-only.");
        return result;
    }
    result = true;
    return result;
}

public boolean getFileSaveInfo(short fileType, boolean askForFileName, String suggestedFile, SaveFileNamesStructure fileInfo) {
    result = false;
    TSaveDialog saveDialog = new TSaveDialog();
    String tryBackupName = "";
    String tryTempName = "";
    String fullSuggestedFileName = "";
    String prompt = "";
    String extension = "";
    short index = 0;
    long tempFileHandle = 0;
    boolean userAbortedSave = false;
    
    fileInfo.fileType = fileType;
    result = false;
    userAbortedSave = false;
    // default info 
    fileInfo.tempFile = "";
    fileInfo.newFile = "";
    fileInfo.backupFile = "";
    fileInfo.writingWasSuccessful = false;
    if (!askForFileName) {
        // if this is a Save, try to set the file name from the suggestedFile given; if file name
        //    is invalid, set flag to move into Save As instead 
        askForFileName = !fileNameIsOkayForSaving(suggestedFile);
        if (!askForFileName) {
            fileInfo.newFile = ExpandFileName(suggestedFile);
        }
    }
    if (askForFileName) {
        // if this is a Save As, or if this is a Save and the file in suggestedFile is invalid,
        //    ask user for a file name 
        saveDialog = delphi_compatability.TSaveDialog().Create(delphi_compatability.Application);
        try {
            if (len(suggestedFile) > 0) {
                fullSuggestedFileName = ExpandFileName(suggestedFile);
                // if directory does not exist, will leave as it was 
                saveDialog.InitialDir = ExtractFilePath(fullSuggestedFileName);
                if (UNRESOLVED.directoryExists(ExtractFilePath(fullSuggestedFileName))) {
                    // don't check if file exists (because saving); check if dir exists 
                    saveDialog.FileName = ExtractFileName(fullSuggestedFileName);
                }
            }
            saveDialog.Filter = filterStringForFileType(fileType, kDontIncludeAllFiles);
            saveDialog.DefaultExt = extensionForFileType(fileType);
            saveDialog.Options = saveDialog.Options + {delphi_compatability.TOpenOption.ofPathMustExist, delphi_compatability.TOpenOption.ofOverwritePrompt, delphi_compatability.TOpenOption.ofHideReadOnly, delphi_compatability.TOpenOption.ofNoReadOnlyReturn, };
            userAbortedSave = !saveDialog.Execute();
            if (!userAbortedSave) {
                fileInfo.newFile = saveDialog.FileName;
            }
        } finally {
            saveDialog.free;
            saveDialog = null;
        }
    }
    if (userAbortedSave) {
        return result;
    }
    try {
        // set backup file name, check if read-only 
        // changed backup file extension to put tilde first because it is better to have all backup files sort together 
        // includes dot 
        extension = ExtractFileExt(fileInfo.newFile);
        extension = ".~" + UNRESOLVED.copy(extension, 2, 2);
    } catch (Exception e) {
        extension = ".bak";
    }
    tryBackupName = ChangeFileExt(fileInfo.newFile, extension);
    if (FileExists(tryBackupName)) {
        if ((UNRESOLVED.fileGetAttr(tryBackupName) && UNRESOLVED.faReadOnly)) {
            prompt = "The backup file " + tryBackupName + " is read-only. Continue?";
            if (MessageDialog(prompt, mtConfirmation, {mbYes, mbNo, }, 0) != mrYes) {
                return result;
            }
        }
    } else {
        fileInfo.backupFile = tryBackupName;
    }
    for (index = 100; index <= 999; index++) {
        // set temp file name 
        tryTempName = ChangeFileExt(fileInfo.newFile, "." + IntToStr(index));
        if (!FileExists(tryTempName)) {
            fileInfo.tempFile = tryTempName;
            break;
        }
    }
    if (fileInfo.tempFile == "") {
        // if can't find unused temp file, quit 
        ShowMessage("Could not create temporary file " + tryTempName + ".");
        return result;
    }
    // test whether temp file can be created 
    tempFileHandle = UNRESOLVED.fileCreate(fileInfo.tempFile);
    if (tempFileHandle > 0) {
        UNRESOLVED.fileClose(tempFileHandle);
        if (!DeleteFile(fileInfo.tempFile)) {
            ShowMessage("Problem with temporary file " + fileInfo.tempFile + ".");
            return result;
        }
    } else {
        ShowMessage("Could not write to temporary file " + fileInfo.tempFile + ".");
        return result;
    }
    result = true;
    return result;
}

public void startFileSave(SaveFileNamesStructure fileInfo) {
    UNRESOLVED.cursor_startWait;
}

public boolean fileIsExportFile(short fileType) {
    result = false;
    result = false;
    switch (fileType) {
        case kFileTypeBitmap:
            result = true;
            break;
        case kFileTypeDXF:
            result = true;
            break;
        case kFileTypeINC:
            result = true;
            break;
        case kFileType3DS:
            result = true;
            break;
        case kFileTypeJPEG:
            result = true;
            break;
        case kFileTypeOBJ:
            result = true;
            break;
        case kFileTypeVRML:
            result = true;
            break;
        case kFileTypeLWO:
            result = true;
            break;
    return result;
}

public void cleanUpAfterFileSave(SaveFileNamesStructure fileInfo) {
    boolean useBackup = false;
    boolean renamingFailed = false;
    boolean deletingFailed = false;
    String prompt = "";
    
    UNRESOLVED.cursor_stopWait;
    UNRESOLVED.stopWaitMessage;
    useBackup = true;
    if (!fileInfo.writingWasSuccessful) {
        //if couldn't write, then remove temp file and exit without warning
        DeleteFile(fileInfo.tempFile);
        return;
    }
    if (fileInfo.backupFile != "") {
        if (FileExists(fileInfo.backupFile)) {
            //remove backup file if exists from prior backup
            //try to delete backup file
            deletingFailed = !DeleteFile(fileInfo.backupFile);
            if (deletingFailed) {
                //couldn't delete backup file
                prompt = "Could not write backup file " + fileInfo.backupFile + ". Continue?";
                if (MessageDialog(prompt, mtConfirmation, {mbYes, mbNo, }, 0) != mrYes) {
                    //user doesn't want to proceed - so cleanup temp file
                    DeleteFile(fileInfo.tempFile);
                    return;
                } else {
                    useBackup = false;
                }
            }
        }
    } else {
        useBackup = false;
    }
    if (FileExists(fileInfo.newFile)) {
        if (useBackup) {
            //if original file exists make backup if requested...
            //rename old copy of new file to make backup
            renamingFailed = !RenameFile(fileInfo.newFile, fileInfo.backupFile);
            if (renamingFailed) {
                prompt = "Could not rename old file to backup file " + fileInfo.backupFile + ". Continue?";
                if (MessageDialog(prompt, mtConfirmation, {mbYes, mbNo, }, 0) != mrYes) {
                    //user doesn't want to proceed - so cleanup temp file
                    DeleteFile(fileInfo.tempFile);
                    return;
                } else {
                    useBackup = false;
                }
            }
        }
        if (!useBackup) {
            //could not create backup file - so just delete old file instead of renaming
            deletingFailed = !DeleteFile(fileInfo.newFile);
            if (deletingFailed) {
                ShowMessage("Could not write file " + fileInfo.newFile);
                return;
            }
        }
    }
    //rename temp file to newFile name
    renamingFailed = !RenameFile(fileInfo.tempFile, fileInfo.newFile);
    if (renamingFailed) {
        //clean up by removing temp file
        ShowMessage("Could not write file " + fileInfo.newFile + " from " + fileInfo.tempFile);
        DeleteFile(fileInfo.tempFile);
        return;
    }
    if ((!udomain.domain.registered) && (fileInfo.writingWasSuccessful) && (fileIsExportFile(fileInfo.fileType))) {
        umain.MainForm.incrementUnregisteredExportCount();
    }
}

// v1.5
// v1.5
public void setDecimalSeparator() {
    // called before opening any file for reading or writing
    // to prevent problem with european comma separation
    UNRESOLVED.DecimalSeparator = ".";
}


