# unit Usupport

from conversion_common import *
import usstream
import uparams
import umath

"""
import umain
import udomain
import uwait
import ucursor
import delphi_compatability
"""

# var
iniFileChanged = False
gVersionName = ""

# const
kMaxEvaluationTime_hours = 10

# record
class SinglePoint:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.reservedZ = 0.0

# record
class SaveFileNamesStructure:
    def __init__(self):
        self.fileType = 0
        self.tempFile = ""
        self.newFile = ""
        self.backupFile = ""
        self.writingWasSuccessful = False

# const
kFileTypeAny = 0
kFileTypePlant = 1
kFileTypeTabbedText = 2
kFileTypeStrategy = 3
kFileTypeIni = 4
kFileTypeExceptionList = 5
kFileTypeBitmap = 6
kFileTypeTdo = 7
kFileTypeDXF = 8
kFileTypeINC = 9
kFileType3DS = 10
kFileTypeProgramInfo = 11
kFileTypeJPEG = 12
kFileTypeOBJ = 13
kFileTypeMTL = 14
kFileTypeVRML = 15
kFileTypeLWO = 16
kWritingWasSuccessful = True
kWritingFailed = False
kNoSuggestedFile = ""
kAskForFileName = True
kDontAskForFileName = False

# const
kMinSingle = -3.4e38
kMaxSingle = 3.4e38

# const
kIncludeAllFiles = True
kDontIncludeAllFiles = False

# don't like using constants for these, but can't find any functions that provide them 
def rotateEncodeBy7(aString):
    result = ""
    i = 0
    letter = ' '
    
    result = ""
    for i in range(0, len(aString)):
        letter = aString[i + 1]
        result = result + chr((ord(letter) + 1) % 256)
    return result

def hexEncode(aString):
    result = ""
    i = 0
    letter = ' '
    
    result = ""
    for i in range(0, len(aString)):
        # ((i+4) mod length(aString))
        letter = aString[i + 1]
        result = result + chr(ord("A") + (ord(letter) / 32))
        result = result + chr(ord("A") + (ord(letter) % 32))
    return result

def hexUnencode(encodedString):
    result = ""
    i = 0
    letter = ' '
    value = 0
    
    result = ""
    value = 0
    for i in range(0, len(encodedString)):
        letter = encodedString[i + 1]
        if i % 2 == 0:
            value = (ord(letter) - ord("A")) * 32
        else:
            value = value + (ord(letter) - ord("A"))
            result = result + chr(value)
    return result

def strToFloatWithCommaCheck(aString):
    result = 0.0
    if found(",", aString):
        aString = replaceCommasWithPeriods(aString)
    result = StrToFloat(aString)
    return result

def makeEnterWorkAsTab(form, activeControl, key):
    if form == None:
        # this is to make enter work as tab in edit boxes on the form 
        return key
    if activeControl == None:
        return key
    if not ((activeControl.__class__ is delphi_compatability.TEdit) or (activeControl.__class__ is delphi_compatability.TComboBox) or (activeControl.__class__ is delphi_compatability.TSpinEdit)):
        return key
    if key == chr(13):
        key = chr(0)
        #next control
        UNRESOLVED.sendMessage(form.Handle, UNRESOLVED.Wm_NextDlgCtl, 0, 0)
    return key

def bitsPerPixelForColorType(colorType):
    result = 0
    screenDC = HDC()
    
    # default to max
    result = 32
    if colorType == delphi_compatability.TPixelFormat.pfDevice:
        screenDC = UNRESOLVED.GetDC(0)
        try:
            result = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES))
        finally:
            UNRESOLVED.ReleaseDC(0, screenDC)
    elif colorType == delphi_compatability.TPixelFormat.pf1bit:
        result = 1
    elif colorType == delphi_compatability.TPixelFormat.pf4bit:
        result = 4
    elif colorType == delphi_compatability.TPixelFormat.pf8bit:
        result = 8
    elif colorType == delphi_compatability.TPixelFormat.pf15bit:
        result = 15
    elif colorType == delphi_compatability.TPixelFormat.pf16bit:
        result = 16
    elif colorType == delphi_compatability.TPixelFormat.pf24bit:
        result = 24
    elif colorType == delphi_compatability.TPixelFormat.pf32bit:
        result = 32
    elif colorType == delphi_compatability.TPixelFormat.pfCustom:
        # just use largest
        result = 32
    return result

#, extraCharToCarryOver
def tolerantReadln(aFile, aString):
    UNRESOLVED.readln(aFile, aString)
    return aString

# text handling 
# CFK unfinished - was trying to deal with text files that have irregular line endings
# such as CR but not LF or just LF
# did not finish - not often found
# got files from user frank salinas as test cases - look at these (in PS longterm) if look at this again later
#  var aChar: char;
#
#  aString := '';
#  aChar := chr(32);
#  // chr(26) is returned if read reaches eof
#  while (not eof(aFile)) and (not (aChar in [#0, #10, #13, #26])) do
#    begin
#    read(aFile, aChar);
#    if not (aChar in [#0, #10, #13, #26]) then
#      aString := aString + aChar
#    else
#      begin
#      read(aFile, aChar);
#      if not (aChar in [#0, #10, #13, #26]) then
#        extraCharToCarryOver := '' + aChar;
#      end;
#    end;
#
#  aChar := chr(32);
#  aString := '';
#  while not eof(aFile) do
#    begin
#    read(aFile, aChar);
#    if not (aChar in [#0, #10, #13, #26]) then
#      result := result + aChar
#    else
#      begin
#      if (aChar = chr(13)) and not eof(aFile) then
#        begin
#        read(theTextFile, aChar);
#        if aChar <> chr(10) then
#          raise Exception.create('Problem in file input');
#        end;
#      break;
#      end;
#    end;
#
#
#  end;
#  
#
#  Start := BufPtr;
#  while not (BufPtr^ in [#13, #26]) do Inc(BufPtr);
#  SetString(S, Start, Integer(BufPtr - Start));
#  if BufPtr^ = #13 then Inc(BufPtr);
#  if BufPtr^ = #10 then Inc(BufPtr);
#  Result := BufPtr;
#  
#
#    aChar := chr(0);
#  result := '';
#  while not eof(theTextFile) do
#    begin
#    read(theTextFile, aChar);
#    if (aChar <> kTextFilerDelimiter) and (aChar <> chr(9)) and (aChar <> chr(10)) and (aChar <> chr(13)) then
#      result := result + aChar
#    else
#      begin
#      if (aChar = chr(13)) and not eof(theTextFile) then
#        begin
#        read(theTextFile, aChar);
#        if aChar <> chr(10) then
#          raise Exception.create('Problem in file input');
#        end;
#      break;
#      end;
#    end;
#  atEndOfFile := eof(theTextFile);
#
# ------------------------------------------------------------------------ text handling 
def limitString(aString, maxChars):
    result = ""
    result = aString
    if len(aString) > maxChars:
        result = UNRESOLVED.copy(aString, 1, maxChars - 3) + "..."
    return result

def replacePunctuationWithUnderscores(aString):
    result = ""
    lowerCaseString = lowercase(aString)
    for i in range(0, len(aString)):
        isAlpha = (ord(lowerCaseString[i]) >= ord("a")) and (ord(lowerCaseString[i]) <= ord("z")) or (ord(lowerCaseString[i]) >= ord("0")) and (ord(lowerCaseString[i]) <= ord("9"))
        if isAlpha:
            result = result + aString[i]
        else:
            result = result + "_"
    return result

def replaceCommasWithPeriods(aString):
    result = ""
    for i in range(0, len(aString)):
        isComma = aString[i] == ","
        if not isComma:
            result = result + aString[i]
        else:
            result = result + "."
    return result

def found(substring, fullString):
    result = fullString.find(substring) != -1
    return result

def trimQuotesFromFirstAndLast(theString):
    result = theString
    if len(result) <= 0:
        return result
    if result[0] == "\"":
        result = result[1:]
    if result[-1] == "\"":
        result = result[:-1]
    return result

def capitalize(aString):
    result = ""
    if len(aString) <= 0:
        return result
    if len(aString) == 1:
        result = aString.upper()
    else:
        result = aString[1].upper + aString[1:]
    return result

def readUntilTab(theFile):
    aChar = chr(0)
    result = ""
    while not UNRESOLVED.eof(theFile):
        UNRESOLVED.read(theFile, aChar)
        if (aChar != chr(9)) and (aChar != chr(10)) and (aChar != chr(13)):
            result = result + aChar
        else:
            if (aChar == chr(13)) and not UNRESOLVED.eof(theFile):
                UNRESOLVED.read(theFile, aChar)
                if aChar != chr(10):
                    raise GeneralException.create("Problem: Something unexpected in file input.")
            break
    if (UNRESOLVED.copy(result, 1, 1) == "\"") and (UNRESOLVED.copy(result, len(result), 1) == "\""):
        # remove quotes placed by spreadsheet around string if it has a comma in it 
        #if (result[1] = '"') and (result[length(result)] = '"') then 
        result = UNRESOLVED.copy(result, 2, len(result) - 2)
    return result

def readShortStringToTab(fileRef):
    temp = readUntilTab(fileRef)
    result = temp[:80]
    return result

def readSmallintToTab(fileRef):
    result = 0
    UNRESOLVED.read(fileRef, result)
    ignore = readUntilTab(fileRef)
    return result

def readSingleToTab(fileRef):
    temp = readUntilTab(fileRef)
    # boundForString returns False if unsuccessful, but not doing anything with result yet 
    succesful, result = boundForString(temp, uparams.kFieldFloat)
    return result

def readBooleanToTab(fileRef):
    booleanString = readUntilTab(fileRef)
    if (booleanString.upper() == "TRUE"):
        result = True
    elif (booleanString.upper() == "FALSE"):
        result = False
    else:
        raise GeneralException.create("Problem: Improper file format for boolean; found: " + booleanString)
    return result

# returns tuple of successful, value
def boundForString(boundString, fieldType):
    #returns whether conversion was successful
    result = True
    if (boundString == "MIN") or (boundString == "FLT_MIN"):
        if fieldType == uparams.kFieldFloat:
            number = kMinSingle
        else:
            number = -32768
    elif (boundString == "MAX") or (boundString == "FLT_MAX"):
        if fieldType == uparams.kFieldFloat:
            number = kMaxSingle
        else:
            number = 32767
    elif (boundString == "PI*2") and (fieldType == uparams.kFieldFloat):
        piTimesTwo = umath.pi * 2.0
        number = piTimesTwo
    elif (boundString == ""):
        if fieldType == uparams.kFieldFloat:
            number = 0.0
        else:
            number = 0
    else:
        try:
            if fieldType == uparams.kFieldFloat:
                number = StrToFloat(boundString)
            else:
                number = StrToInt(boundString)
        except: # EConvertError:
            raise
            result = False
            if fieldType == uparams.kFieldFloat:
                number = 0.0
            else:
                number = 0
    return result, number

def trimLeftAndRight(theString):
    result = theString.strip()
    return result

def stringUpTo(aString, aDelimiter):
    if len(aString) == 0:
        result = ""
        return result
    delimiterPos = aString.find(aDelimiter)
    if delimiterPos == -1:
        result = aString
    elif delimiterPos == 0:
        result = ""
    else:
        result = aString[:delimiterPos]
    return result

def stringBeyond(aString, aDelimiter):
    if len(aString) == 0:
        result = ""
        return result
    delimiterPos = aString.find(aDelimiter)
    if delimiterPos == -1:
        result = aString
    elif delimiterPos == len(aString) - 1:
        result = ""
    else:
        result = aString[delimiterPos + 1:]
    return result

def stringBetween(startString, endString, wholeString):
    result = stringUpTo(stringBeyond(trim(wholeString), startString), endString)
    return result

# didn't use, don't know if works
#function listOfStringsBetweenDelimiters(aString, aDelimiter: string): TStrings;
#  var token: string;
#  begin
#  result := TStrings.create; // caller must free this
#  while length(aString) > 0 do
#    begin
#    token := stringUpTo(aString, aDelimiter);
#    aString := stringBeyond(aString, aDelimiter);
#    result.add(token);
#    end;
#  end;
#     
def boolToStr(value):
    if value:
        result = "True"
    else:
        result = "False"
    return result

def strToBool(booleanString):
    result = False
    if booleanString == "":
        return result
    if (booleanString.upper() == "TRUE"):
        result = True
    elif (booleanString.upper() == "FALSE"):
        result = False
    return result

def messageForExceptionType(e, methodName):
    errorString = ""
    
    if e == None:
        return
    if (e.__class__ is UNRESOLVED.EZeroDivide):
        errorString = "Problem: Floating-point divide by zero error in method " + methodName + "."
    elif (e.__class__ is UNRESOLVED.EDivByZero):
        errorString = "Problem: Integer divide by zero in method " + methodName + "."
    elif (e.__class__ is UNRESOLVED.EInvalidOp):
        errorString = "Problem: Invalid floating-point operation in method " + methodName + "."
    elif (e.__class__ is UNRESOLVED.EOverFlow):
        errorString = "Problem: Floating-point overflow in method " + methodName + "."
    elif (e.__class__ is UNRESOLVED.EUnderFlow):
        errorString = "Problem: Floating-point underflow in method " + methodName + "."
    else:
        errorString = "Problem in method " + methodName + "."
    errorString = errorString + chr(13) + chr(13) + e.message
    umath.ErrorMessage(errorString)

# float to text conversion 
# ---------------------------------------------------------------------------- float to text conversion 
def removeTrailingZeros(theString):
    result = ""
    while (len(theString) > 1) and (theString[len(theString)] == "0") and (theString[len(theString) - 1] != "."):
        #dec(theString[0]);  
        UNRESOLVED.setLength(theString, len(theString) - 1)
    result = theString
    return result

def shortenLongNonZeroDigitsAfterDecimal(theString, maxDigits):
    result = ""
    pointPos = 0L
    firstNonZeroDigit = 0L
    digitsToGetRidOf = 0L
    
    result = theString
    pointPos = UNRESOLVED.pos(".", result)
    if pointPos != 0:
        firstNonZeroDigit = pointPos + 1
        while (firstNonZeroDigit <= len(theString)) and (theString[firstNonZeroDigit] == "0"):
            firstNonZeroDigit += 1
        if firstNonZeroDigit < len(theString):
            digitsToGetRidOf = len(theString) - firstNonZeroDigit + 1 - maxDigits
            if digitsToGetRidOf > 0:
                result = UNRESOLVED.copy(result, 1, len(theString) - digitsToGetRidOf)
    return result

def digitValueString(value):
    result = ""
    result = removeTrailingZeros(shortenLongNonZeroDigitsAfterDecimal(FloatToStrF(value, UNRESOLVED.ffFixed, 7, 8), 2))
    return result

def valueString(value):
    result = ""
    result = removeTrailingZeros(shortenLongNonZeroDigitsAfterDecimal(FloatToStrF(value, UNRESOLVED.ffFixed, 7, 8), 4))
    return result

# graphics 
# ---------------------------------------------------------------------------- graphics 
def clientRectToScreenRect(handle, clientRect):
    result = TRect()
    p1 = TPoint()
    p2 = TPoint()
    
    p1 = Point(clientRect.Left, clientRect.Top)
    UNRESOLVED.clientToScreen(handle, p1)
    p2 = Point(clientRect.Right, clientRect.Bottom)
    UNRESOLVED.clientToScreen(handle, p2)
    result = Rect(p1.X, p1.Y, p2.X, p2.Y)
    return result

def support_rgb(R, G, B):
    result = 0L
    #var screenDC: HDC;
    #result := RGB(r, g, b);  
    #try
    #  screenDC := GetDC(0);
    #  result := GetNearestColor(screenDC, PALETTERGB(r, g, b));
    #finally
    #   releaseDC(0, screenDC);
    #end;
    #result = UNRESOLVED.PALETTERGB(R, G, B)
    # PDF PORT MAYBE WRONG
    result = (B << 16) | (G << 8) | R
    return result

def combineRects(rect1, rect2):
    result = TRect()
    result.Left = umath.intMin(rect1.Left, rect2.Left)
    result.Right = umath.intMax(rect1.Right, rect2.Right)
    result.Top = umath.intMin(rect1.Top, rect2.Top)
    result.Bottom = umath.intMax(rect1.Bottom, rect2.Bottom)
    return result

def addRectToBoundsRect(boundsRect, newRect):
    if (boundsRect.Left == 0) and (boundsRect.Right == 0) and (boundsRect.Top == 0) and (boundsRect.Bottom == 0):
        # on first rect entered, initialize bounds rect
        boundsRect.Left = newRect.Left
        boundsRect.Right = newRect.Right
        boundsRect.Top = newRect.Top
        boundsRect.Bottom = newRect.Bottom
    else:
        if newRect.Left < boundsRect.Left:
            # deal with possibility of rectangle being flipped, so left > right or top > bottom
            # expand rectangle to include left side x
            boundsRect.Left = newRect.Left
        elif newRect.Left > boundsRect.Right:
            boundsRect.Right = newRect.Left
        if newRect.Right < boundsRect.Left:
            # expand rectangle to include right side x
            boundsRect.Left = newRect.Right
        elif newRect.Right > boundsRect.Right:
            boundsRect.Right = newRect.Right
        if newRect.Top < boundsRect.Top:
            # expand rectangle to include top y
            boundsRect.Top = newRect.Top
        elif newRect.Top > boundsRect.Bottom:
            boundsRect.Bottom = newRect.Top
        if newRect.Bottom < boundsRect.Top:
            # expand rectangle to include bottom y
            boundsRect.Top = newRect.Bottom
        elif newRect.Bottom > boundsRect.Bottom:
            boundsRect.Bottom = newRect.Bottom

def rWidth(rect):
    try:
        result = rect.right - rect.left
    except AttributeError:
        result = rect.Right - rect.Left
    return result

def rHeight(rect):
    try:
        result = rect.bottom - rect.top
    except AttributeError:
        result = rect.Bottom - rect.Top
    return result

def zeroRect(rect):
    result = (rect.left == 0) and (rect.top == 0) and (rect.right == 0) and (rect.bottom == 0)
    return result

def rectsAreIdentical(oneRect, twoRect):
    result = False
    result = (oneRect.Top == twoRect.Top) and (oneRect.Bottom == twoRect.Bottom) and (oneRect.Left == twoRect.Left) and (oneRect.Right == twoRect.Right)
    return result

def rectToString(aRect):
    result = ""
    result = IntToStr(aRect.Left) + " " + IntToStr(aRect.Top) + " " + IntToStr(aRect.Right) + " " + IntToStr(aRect.Bottom)
    return result

def stringToRect(aString):
    result = Rect(0, 0, 0, 0)
    stream = usstream.KfStringStream()
    stream.onStringSeparator(aString, " ")
    result.Left = StrToIntDef(stream.nextToken(), 0)
    result.Top = StrToIntDef(stream.nextToken(), 0)
    result.Right = StrToIntDef(stream.nextToken(), 0)
    result.Bottom = StrToIntDef(stream.nextToken(), 0)
    return result

def pointToString(aPoint):
    result = IntToStr(aPoint.X) + "  " + IntToStr(aPoint.Y)
    return result

def stringToPoint(aString):
    result = Point(0, 0)
    stream = usstream.KfStringStream()
    stream.onStringSeparator(aString, " ")
    result.X = StrToIntDef(stream.nextToken(), 0)
    result.Y = StrToIntDef(stream.nextToken(), 0)
    return result

def setSinglePoint(x, y):
    result = SinglePoint(x, y)
    return result

def singlePointToString(aPoint):
    result = digitValueString(aPoint.x) + "  " + digitValueString(aPoint.y)
    return result

def stringToSinglePoint(aString):
    result = SinglePoint()
    stream = usstream.KfStringStream()
    stream.onStringSeparator(aString, " ")
    token = stream.nextToken()
    if token.find(".") == -1:
        # if it was written as an integer, deal with that
        result.x = StrToIntDef(token, 0)
    else:
        try:
            result.x = StrToFloat(token)
        except:
            result.x = 0.0
    token = stream.nextToken()
    if token.find(".") == -1:
        result.y = StrToIntDef(token, 0)
    else:
        try:
            result.y = StrToFloat(token)
        except:
            result.y = 0.0

    return result

def colorToRGBString(color):
    result = IntToStr(UNRESOLVED.getRValue(color)) + " " + IntToStr(UNRESOLVED.getGValue(color)) + " " + IntToStr(UNRESOLVED.getBValue(color))
    return result

def rgbStringToColor(aString):
    # format is r g b 
    stream = usstream.KfStringStream()
    stream.onStringSeparator(aString, " ")
    r = StrToIntDef(stream.nextToken(), 0)
    g = StrToIntDef(stream.nextToken(), 0)
    b = StrToIntDef(stream.nextToken(), 0)
    result = support_rgb(r, g, b)
    return result

def GetRValue(color):
    return (color & 0xFF) 

def GetGValue(color):
    return (color & 0xFF00) >> 8

def GetBValue(color):
    return (color & 0xFF0000) >> 16

# ---------------------------------------------------------------------------------- color functions 
def blendColors(firstColor, secondColor, aStrength):
    #blend first color with second color,
    #   weighting the second color by aStrength (0-1) and first color by (1 - aStrength).
    aStrength = umath.max(0.0, umath.min(1.0, aStrength))
    r1 = umath.intMax(0, umath.intMin(255, GetRValue(firstColor)))
    g1 = umath.intMax(0, umath.intMin(255, GetGValue(firstColor)))
    b1 = umath.intMax(0, umath.intMin(255, GetBValue(firstColor)))
    r2 = umath.intMax(0, umath.intMin(255, GetRValue(secondColor)))
    g2 = umath.intMax(0, umath.intMin(255, GetGValue(secondColor)))
    b2 = umath.intMax(0, umath.intMin(255, GetBValue(secondColor)))
    result = support_rgb(intround(r1 * (1.0 - aStrength) + r2 * aStrength), intround(g1 * (1.0 - aStrength) + g2 * aStrength), intround(b1 * (1.0 - aStrength) + b2 * aStrength))
    return result

def darkerColor(aColor):
    r = umath.intMax(0, GetRValue(aColor) - 10)
    g = umath.intMax(0, GetGValue(aColor) - 10)
    b = umath.intMax(0, GetBValue(aColor) - 10)
    result = support_rgb(r, g, b)
    #result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); 
    return result

def darkerColorWithSubtraction(aColor, subtract):
    r = umath.intMax(0, GetRValue(aColor) - subtract)
    g = umath.intMax(0, GetGValue(aColor) - subtract)
    b = umath.intMax(0, GetBValue(aColor) - subtract)
    result = support_rgb(r, g, b)
    #result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); 
    return result

def lighterColor(aColor):
    r = umath.intMin(255, intround(GetRValue(aColor) * 1.5))
    g = umath.intMin(255, intround(GetGValue(aColor) * 1.5))
    b = umath.intMin(255, intround(GetBValue(aColor) * 1.5))
    result = support_rgb(r, g, b)
    #result := support_rgb(GetRValue(aColor) div 2, GetGValue(aColor) div 2, GetBValue(aColor) div 2); 
    return result

def drawButton(aCanvas, aRect, selected, enabled):
    internalRect = TRect()
    
    aCanvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
    if enabled:
        aCanvas.Pen.Color = delphi_compatability.clBlack
        aCanvas.Brush.Color = delphi_compatability.clWhite
    else:
        aCanvas.Brush.Color = UNRESOLVED.clBtnShadow
        aCanvas.Pen.Color = UNRESOLVED.clBtnShadow
    aCanvas.Rectangle(aRect.Left, aRect.Top, aRect.Right, aRect.Bottom)
    if selected:
        internalRect = aRect
        UNRESOLVED.inflateRect(internalRect, -1, -1)
        aCanvas.Brush.Color = delphi_compatability.clAqua
        aCanvas.FillRect(internalRect)

def draw3DButton(ACanvas, Client, Selected, Pressed):
    result = TRect()
    ACanvas.Brush.Color = delphi_compatability.clWindowFrame
    if Selected:
        ACanvas.FrameRect(Client)
        UNRESOLVED.InflateRect(Client, -1, -1)
    if not Pressed:
        ACanvas.Frame3d(ACanvas, Client, UNRESOLVED.clBtnHighlight, UNRESOLVED.clBtnShadow, 2)
    else:
        ACanvas.Pen.Color = UNRESOLVED.clBtnShadow
        ACanvas.Polyline([Point(Client.Left, Client.Bottom - 1), Point(Client.Left, Client.Top), Point(Client.Right, Client.Top), ])
        Client = Rect(Client.Left + 3, Client.Top + 3, Client.Right - 1, Client.Bottom - 1)
    ACanvas.Brush.Color = UNRESOLVED.clBtnFace
    ACanvas.FillRect(Client)
    result = Client
    return result

# combo and list box utilities 
# ---------------------------------------------------------------------------- combo and list box utilities 
def currentObjectInComboBox(comboBox):
    result = TObject()
    if comboBox.Items.Count == 0:
        result = None
    elif comboBox.ItemIndex != -1:
        result = comboBox.Items.Objects[comboBox.ItemIndex]
    else:
        result = None
    return result

def currentObjectInListBox(listBox):
    result = TObject()
    if listBox.Items.Count == 0:
        result = None
    elif listBox.ItemIndex != -1:
        result = listBox.Items.Objects[listBox.ItemIndex]
    else:
        result = None
    return result

# file i/o 
# ---------------------------------------------------------------------------- file i/o 
def makeFileNameFrom(aString):
    result = ""
    done = False
    spacePos = 0
    
    result = aString
    done = False
    while not done:
        spacePos = UNRESOLVED.pos(" ", result)
        done = (spacePos <= 0)
        if not done:
            UNRESOLVED.delete(result, spacePos, 1)
    return result

def nameStringForFileType(fileType):
    result = ""
    if fileType == kFileTypeAny:
        result = ""
    elif fileType == kFileTypePlant:
        result = "Plant"
    elif fileType == kFileTypeTabbedText:
        result = "Tabbed text"
    elif fileType == kFileTypeStrategy:
        result = "Strategy"
    elif fileType == kFileTypeIni:
        result = "Ini"
    elif fileType == kFileTypeExceptionList:
        result = "Exception list"
    elif fileType == kFileTypeBitmap:
        result = "Bitmap"
    elif fileType == kFileTypeTdo:
        result = "3D object"
    elif fileType == kFileTypeDXF:
        result = "DXF"
    elif fileType == kFileTypeINC:
        result = "POV Include file"
    elif fileType == kFileType3DS:
        result = "3DS"
    elif fileType == kFileTypeProgramInfo:
        result = "Program Info"
    elif fileType == kFileTypeJPEG:
        result = "JPEG"
    elif fileType == kFileTypeOBJ:
        result = "OBJ"
    elif fileType == kFileTypeMTL:
        result = "MTL"
    elif fileType == kFileTypeVRML:
        result = "VRML"
    elif fileType == kFileTypeLWO:
        result = "LWO"
    return result

def extensionForFileType(fileType):
    result = ""
    result = ""
    if fileType == kFileTypeAny:
        result = "*"
    elif fileType == kFileTypePlant:
        result = "pla"
    elif fileType == kFileTypeTabbedText:
        result = "tab"
    elif fileType == kFileTypeStrategy:
        result = "str"
    elif fileType == kFileTypeIni:
        result = "ini"
    elif fileType == kFileTypeExceptionList:
        result = "nex"
    elif fileType == kFileTypeBitmap:
        result = "bmp"
    elif fileType == kFileTypeTdo:
        result = "tdo"
    elif fileType == kFileTypeDXF:
        result = "dxf"
    elif fileType == kFileTypeINC:
        result = "inc"
    elif fileType == kFileType3DS:
        result = "3ds"
    elif fileType == kFileTypeProgramInfo:
        result = "txt"
    elif fileType == kFileTypeJPEG:
        result = "jpg"
    elif fileType == kFileTypeOBJ:
        result = "obj"
    elif fileType == kFileTypeMTL:
        result = "mtl"
    elif fileType == kFileTypeVRML:
        result = "wrl"
    elif fileType == kFileTypeLWO:
        result = "lwo"
    return result

def filterStringForFileType(fileType, includeAllFiles):
    result = ""
    extension = ""
    
    extension = extensionForFileType(fileType)
    if fileType == kFileTypeAny:
        result = "All files (*.*)|*.*"
    elif includeAllFiles:
        result = nameStringForFileType(fileType) + " files (*." + extension + ")|*." + extension + "|All files (*.*)|*.*"
    else:
        result = nameStringForFileType(fileType) + " files (*." + extension + ")|*." + extension
    return result

def getFileOpenInfo(fileType, suggestedFile, aTitle):
    result = ""
    fullSuggestedFileName = ""
    openDialog = TOpenDialog()
    nameString = ""
    
    result = ""
    openDialog = delphi_compatability.TOpenDialog().Create(delphi_compatability.Application)
    try:
        if suggestedFile == "":
            openDialog.FileName = "*." + extensionForFileType(fileType)
        else:
            fullSuggestedFileName = ExpandFileName(suggestedFile)
            # if directory does not exist, will leave as it was 
            openDialog.InitialDir = ExtractFilePath(fullSuggestedFileName)
            if FileExists(fullSuggestedFileName):
                openDialog.FileName = ExtractFileName(fullSuggestedFileName)
        nameString = nameStringForFileType(fileType)
        if len(aTitle) > 0:
            openDialog.Title = aTitle
        elif nameString[1] in ["A", "E", "I", "O", "U", ]:
            openDialog.Title = "Choose an " + nameString + " file"
        else:
            openDialog.Title = "Choose a " + nameString + " file"
        openDialog.Filter = filterStringForFileType(fileType, kIncludeAllFiles)
        openDialog.DefaultExt = extensionForFileType(fileType)
        openDialog.Options = openDialog.Options + [delphi_compatability.TOpenOption.ofPathMustExist, delphi_compatability.TOpenOption.ofFileMustExist, delphi_compatability.TOpenOption.ofHideReadOnly, ]
        if openDialog.Execute():
            if (delphi_compatability.TOpenOption.ofExtensionDifferent in openDialog.Options) and (fileType != kFileTypeAny):
                ShowMessage("The file (" + openDialog.FileName + ") does not have the correct extension (" + openDialog.DefaultExt + ").")
                return result
            else:
                result = openDialog.FileName
    finally:
        openDialog.free
    return result

def fileNameIsOkayForSaving(suggestedFile):
    result = False
    fullSuggestedFileName = ""
    
    result = False
    if len(suggestedFile) == 0:
        return result
    fullSuggestedFileName = ExpandFileName(suggestedFile)
    if not UNRESOLVED.directoryExists(ExtractFilePath(fullSuggestedFileName)):
        # check if directory exists 
        ShowMessage("The directory " + ExtractFilePath(fullSuggestedFileName) + " does not exist.")
        return result
    if FileExists(fullSuggestedFileName) and UNRESOLVED.FileGetAttr(fullSuggestedFileName) and UNRESOLVED.faReadOnly:
        # if file exists and is writable, it's ok because Save (not Save As) should not ask to rewrite 
        # if file exists but is read-only, quit  
        ShowMessage("The file " + fullSuggestedFileName + " exists and is read-only.")
        return result
    result = True
    return result

def getFileSaveInfo(fileType, askForFileName, suggestedFile, fileInfo):
    result = False
    saveDialog = TSaveDialog()
    tryBackupName = ""
    tryTempName = ""
    fullSuggestedFileName = ""
    prompt = ""
    extension = ""
    index = 0
    tempFileHandle = 0L
    userAbortedSave = False
    
    fileInfo.fileType = fileType
    result = False
    userAbortedSave = False
    # default info 
    fileInfo.tempFile = ""
    fileInfo.newFile = ""
    fileInfo.backupFile = ""
    fileInfo.writingWasSuccessful = False
    if not askForFileName:
        # if this is a Save, try to set the file name from the suggestedFile given; if file name
        #    is invalid, set flag to move into Save As instead 
        askForFileName = not fileNameIsOkayForSaving(suggestedFile)
        if not askForFileName:
            fileInfo.newFile = ExpandFileName(suggestedFile)
    if askForFileName:
        # if this is a Save As, or if this is a Save and the file in suggestedFile is invalid,
        #    ask user for a file name 
        saveDialog = delphi_compatability.TSaveDialog().Create(delphi_compatability.Application)
        try:
            if len(suggestedFile) > 0:
                fullSuggestedFileName = ExpandFileName(suggestedFile)
                # if directory does not exist, will leave as it was 
                saveDialog.InitialDir = ExtractFilePath(fullSuggestedFileName)
                if UNRESOLVED.directoryExists(ExtractFilePath(fullSuggestedFileName)):
                    # don't check if file exists (because saving); check if dir exists 
                    saveDialog.FileName = ExtractFileName(fullSuggestedFileName)
            saveDialog.Filter = filterStringForFileType(fileType, kDontIncludeAllFiles)
            saveDialog.DefaultExt = extensionForFileType(fileType)
            saveDialog.Options = saveDialog.Options + [delphi_compatability.TOpenOption.ofPathMustExist, delphi_compatability.TOpenOption.ofOverwritePrompt, delphi_compatability.TOpenOption.ofHideReadOnly, delphi_compatability.TOpenOption.ofNoReadOnlyReturn, ]
            userAbortedSave = not saveDialog.Execute()
            if not userAbortedSave:
                fileInfo.newFile = saveDialog.FileName
        finally:
            saveDialog.free
            saveDialog = None
    if userAbortedSave:
        return result
    try:
        # set backup file name, check if read-only 
        # changed backup file extension to put tilde first because it is better to have all backup files sort together 
        # includes dot 
        extension = ExtractFileExt(fileInfo.newFile)
        extension = ".~" + UNRESOLVED.copy(extension, 2, 2)
    except:
        extension = ".bak"
    tryBackupName = ChangeFileExt(fileInfo.newFile, extension)
    if FileExists(tryBackupName):
        if (UNRESOLVED.fileGetAttr(tryBackupName) and UNRESOLVED.faReadOnly):
            prompt = "The backup file " + tryBackupName + " is read-only. Continue?"
            if MessageDialog(prompt, mtConfirmation, [mbYes, mbNo, ], 0) != mrYes:
                return result
    else:
        fileInfo.backupFile = tryBackupName
    for index in range(100, 999 + 1):
        # set temp file name 
        tryTempName = ChangeFileExt(fileInfo.newFile, "." + IntToStr(index))
        if not FileExists(tryTempName):
            fileInfo.tempFile = tryTempName
            break
    if fileInfo.tempFile == "":
        # if can't find unused temp file, quit 
        ShowMessage("Could not create temporary file " + tryTempName + ".")
        return result
    # test whether temp file can be created 
    tempFileHandle = UNRESOLVED.fileCreate(fileInfo.tempFile)
    if tempFileHandle > 0:
        UNRESOLVED.fileClose(tempFileHandle)
        if not DeleteFile(fileInfo.tempFile):
            ShowMessage("Problem with temporary file " + fileInfo.tempFile + ".")
            return result
    else:
        ShowMessage("Could not write to temporary file " + fileInfo.tempFile + ".")
        return result
    result = True
    return result

def startFileSave(fileInfo):
    ucursor.cursor_startWait()

def fileIsExportFile(fileType):
    result = False
    result = False
    if fileType == kFileTypeBitmap:
        result = True
    elif fileType == kFileTypeDXF:
        result = True
    elif fileType == kFileTypeINC:
        result = True
    elif fileType == kFileType3DS:
        result = True
    elif fileType == kFileTypeJPEG:
        result = True
    elif fileType == kFileTypeOBJ:
        result = True
    elif fileType == kFileTypeVRML:
        result = True
    elif fileType == kFileTypeLWO:
        result = True
    return result

def cleanUpAfterFileSave(fileInfo):
    useBackup = False
    renamingFailed = False
    deletingFailed = False
    prompt = ""
    
    ucursor.cursor_stopWait()
    uwait.stopWaitMessage()
    useBackup = True
    if not fileInfo.writingWasSuccessful:
        #if couldn't write, then remove temp file and exit without warning
        DeleteFile(fileInfo.tempFile)
        return
    if fileInfo.backupFile != "":
        if FileExists(fileInfo.backupFile):
            #remove backup file if exists from prior backup
            #try to delete backup file
            deletingFailed = not DeleteFile(fileInfo.backupFile)
            if deletingFailed:
                #couldn't delete backup file
                prompt = "Could not write backup file " + fileInfo.backupFile + ". Continue?"
                if MessageDialog(prompt, mtConfirmation, [mbYes, mbNo, ], 0) != mrYes:
                    #user doesn't want to proceed - so cleanup temp file
                    DeleteFile(fileInfo.tempFile)
                    return
                else:
                    useBackup = False
    else:
        useBackup = False
    if FileExists(fileInfo.newFile):
        if useBackup:
            #if original file exists make backup if requested...
            #rename old copy of new file to make backup
            renamingFailed = not RenameFile(fileInfo.newFile, fileInfo.backupFile)
            if renamingFailed:
                prompt = "Could not rename old file to backup file " + fileInfo.backupFile + ". Continue?"
                if MessageDialog(prompt, mtConfirmation, [mbYes, mbNo, ], 0) != mrYes:
                    #user doesn't want to proceed - so cleanup temp file
                    DeleteFile(fileInfo.tempFile)
                    return
                else:
                    useBackup = False
        if not useBackup:
            #could not create backup file - so just delete old file instead of renaming
            deletingFailed = not DeleteFile(fileInfo.newFile)
            if deletingFailed:
                ShowMessage("Could not write file " + fileInfo.newFile)
                return
    #rename temp file to newFile name
    renamingFailed = not RenameFile(fileInfo.tempFile, fileInfo.newFile)
    if renamingFailed:
        #clean up by removing temp file
        ShowMessage("Could not write file " + fileInfo.newFile + " from " + fileInfo.tempFile)
        DeleteFile(fileInfo.tempFile)
        return
    if (not udomain.domain.registered) and (fileInfo.writingWasSuccessful) and (fileIsExportFile(fileInfo.fileType)):
        umain.MainForm.incrementUnregisteredExportCount()

# v1.5
# v1.5
def setDecimalSeparator():
    # called before opening any file for reading or writing
    # to prevent problem with european comma separation
    UNRESOLVED.DecimalSeparator = "."

