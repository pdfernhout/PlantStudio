# unit Ufiler

from conversion_common import *
import uclasses
import usupport
import delphi_compatability

#
#  For every streamable object,
#  	Set class number to constant from uclasses.
#    Increment version number if change streamed structure (watch out for base class streaming changes!).
#    Increment addition number if add new field and older program versions can ignore it and you can default it.
#      In addition case, check additions number in streamDataWithFiler.
#      When create new version, you should usually reset additions to zero and
#      	remove additions testing code in streaming.
#  
# record
class PdClassAndVersionInformationRecord:
    def __init__(self):
        self.classNumber = 0
        self.versionNumber = 0
        self.additionNumber = 0

# enumerated type PdFilerMode
class PdFilerMode:
    filerModeReading, filerModeWriting, filerModeCounting = range(3)

# const
kMinWidthOnScreen = 40
kMinHeightOnScreen = 20

# global functions 
def StreamFormPositionInfoWithFiler(filer, cvir, form):
    tempBoundsRect = TRect()
    tempVisible = false
    tempWindowState = TWindowState()
    
    if filer == None:
        return
    if form == None:
        return
    if filer.isReading():
        form.Visible = false
    if filer.isReading():
        filer.streamRect(tempBoundsRect)
        if tempBoundsRect.Left > delphi_compatability.Screen.Width - kMinWidthOnScreen:
            # keep window on screen - left corner of title bar 
            tempBoundsRect.Left = delphi_compatability.Screen.Width - kMinWidthOnScreen
        if tempBoundsRect.Top > delphi_compatability.Screen.Height - kMinHeightOnScreen:
            tempBoundsRect.Top = delphi_compatability.Screen.Height - kMinHeightOnScreen
        form.Position = delphi_compatability.TPosition.poDesigned
        form.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right - tempBoundsRect.Left, tempBoundsRect.Bottom - tempBoundsRect.Top)
    else:
        tempBoundsRect = form.BoundsRect
        filer.streamRect(tempBoundsRect)
    if filer.isReading():
        tempVisible = filer.streamBoolean(tempVisible)
        filer.streamWindowState(tempWindowState)
        form.WindowState = tempWindowState
        # make visible last 
        form.Visible = tempVisible
    else:
        tempVisible = form.Visible
        tempVisible = filer.streamBoolean(tempVisible)
        tempWindowState = form.WindowState
        filer.streamWindowState(tempWindowState)

def StreamComboBoxItemIndexWithFiler(filer, cvir, comboBox):
    tempItemIndex = 0L
    
    if filer.isReading():
        tempItemIndex = -1
        tempItemIndex = filer.streamLongint(tempItemIndex)
        if (comboBox.Items.Count > 0) and (tempItemIndex >= 0) and (tempItemIndex <= comboBox.Items.Count - 1):
            comboBox.ItemIndex = tempItemIndex
    else:
        tempItemIndex = comboBox.ItemIndex
        tempItemIndex = filer.streamLongint(tempItemIndex)

def StreamComboBoxItemIndexToTempVarWithFiler(filer, cvir, comboBox, saveIndex):
    tempItemIndex = 0L
    
    if filer.isReading():
        tempItemIndex = -1
        tempItemIndex = filer.streamLongint(tempItemIndex)
        saveIndex = tempItemIndex
    else:
        tempItemIndex = comboBox.ItemIndex
        tempItemIndex = filer.streamLongint(tempItemIndex)
    return saveIndex

class PdFiler(TObject):
    def __init__(self):
        self.stream = TStream()
        self.mode = PdFilerMode()
        self.bytesStreamed = 0L
        self.resourceProvider = TObject()
    
    #an object that can be used to look up shared resource references
    def createWithStream(self, aStream):
        self.stream = aStream
        if self.stream == None:
            self.setToCountingMode()
        #should test type of stream to auomatically set reading or writing mode
        return self
    
    def setToReadingMode(self):
        self.mode = PdFilerMode.filerModeReading
        self.bytesStreamed = 0
        if self.stream == None:
            # was LoadStr( )
            raise delphi_compatability.EReadError.create(UNRESOLVED.SReadError)
    
    def setToWritingMode(self):
        self.mode = PdFilerMode.filerModeWriting
        self.bytesStreamed = 0
        if self.stream == None:
            # was LoadStr( )
            raise delphi_compatability.EWriteError.create(UNRESOLVED.SWriteError)
    
    def setToCountingMode(self):
        self.mode = PdFilerMode.filerModeCounting
        self.bytesStreamed = 0
    
    def isReading(self):
        result = false
        result = self.mode == PdFilerMode.filerModeReading
        return result
    
    def isWriting(self):
        result = false
        result = self.mode == PdFilerMode.filerModeWriting
        return result
    
    def isCounting(self):
        result = false
        result = self.mode == PdFilerMode.filerModeCounting
        return result
    
    #simple types
    #simple types
    def streamBytes(self, bytes, size):
        if self.mode == PdFilerMode.filerModeReading:
            bytes = self.stream.read(bytes, size)
        elif self.mode == PdFilerMode.filerModeWriting:
            self.stream.write(bytes, size)
        elif self.mode == PdFilerMode.filerModeCounting:
            self.bytesStreamed = self.bytesStreamed + size
        return bytes
    
    def streamClassAndVersionInformation(self, cvir):
        if self.mode == PdFilerMode.filerModeReading:
            cvir = self.stream.read(cvir, FIX_sizeof(PdClassAndVersionInformationRecord))
        elif self.mode == PdFilerMode.filerModeWriting:
            self.stream.write(cvir, FIX_sizeof(PdClassAndVersionInformationRecord))
        elif self.mode == PdFilerMode.filerModeCounting:
            self.bytesStreamed = self.bytesStreamed + FIX_sizeof(PdClassAndVersionInformationRecord)
    
    def streamShortString(self, aString):
        if self.mode == PdFilerMode.filerModeReading:
            aString[0] = self.streamBytes(aString[0], 1)
            aString[1] = self.streamBytes(aString[1], ord(aString[0]))
        elif self.mode == PdFilerMode.filerModeWriting:
            aString = self.streamBytes(aString, len(aString) + 1)
        elif self.mode == PdFilerMode.filerModeCounting:
            self.bytesStreamed = self.bytesStreamed + len(aString) + 1
        return aString
    
    def streamAnsiString(self, aString):
        theLength = 0L
        
        if self.mode == PdFilerMode.filerModeReading:
            #make sure write out extra zero at end
            theLength = self.streamLongint(theLength)
            UNRESOLVED.setlength(aString, theLength)
            if theLength > 0:
                aString.PDF_FIX_POINTER_ACCESS = self.streamBytes(aString.PDF_FIX_POINTER_ACCESS, theLength + 1)
        elif self.mode == PdFilerMode.filerModeWriting:
            theLength = len(aString)
            theLength = self.streamLongint(theLength)
            if theLength > 0:
                aString.PDF_FIX_POINTER_ACCESS = self.streamBytes(aString.PDF_FIX_POINTER_ACCESS, theLength + 1)
        elif self.mode == PdFilerMode.filerModeCounting:
            self.bytesStreamed = self.bytesStreamed + len(aString) + 1
    
    #maybe problem in 32 bits - depends how big a string string alloc can return
    #need to stream "aPChar^" not just "aPChar".  The first is the array,
    #the second is just the space occupied by the pointer - and is a bug
    def streamPChar(self, aPChar):
        stringLength = 0L
        
        if self.mode == PdFilerMode.filerModeReading:
            if aPChar != None:
                UNRESOLVED.StrDispose(aPChar)
                aPChar = None
            stringLength = self.streamBytes(stringLength, FIX_sizeof(longint))
            if stringLength > 0:
                aPChar = UNRESOLVED.StrAlloc(stringLength)
                if aPChar == None:
                    raise GeneralException.create("Problem: Out of memory.")
                aPChar.PDF_FIX_POINTER_ACCESS = self.streamBytes(aPChar.PDF_FIX_POINTER_ACCESS, stringLength)
        elif self.mode == PdFilerMode.filerModeWriting:
            if aPChar == None:
                stringLength = 0
            else:
                stringLength = len(aPChar) + 1
            stringLength = self.streamBytes(stringLength, FIX_sizeof(longint))
            if stringLength > 0:
                aPChar.PDF_FIX_POINTER_ACCESS = self.streamBytes(aPChar.PDF_FIX_POINTER_ACCESS, stringLength)
        elif self.mode == PdFilerMode.filerModeCounting:
            self.bytesStreamed = self.bytesStreamed + FIX_sizeof(longint) + len(aPChar) + 1
        return aPChar
    
    def streamChar(self, aChar):
        aChar = self.streamBytes(aChar, FIX_sizeof(char))
        return aChar
    
    def streamBoolean(self, aBoolean):
        aBoolean = self.streamBytes(aBoolean, FIX_sizeof(boolean))
        return aBoolean
    
    def streamByteBool(self, aByteBool):
        aByteBool = self.streamBytes(aByteBool, FIX_sizeof(UNRESOLVED.bytebool))
    
    def streamWordBool(self, aWordBool):
        aWordBool = self.streamBytes(aWordBool, FIX_sizeof(UNRESOLVED.wordbool))
    
    def streamLongBool(self, aLongBool):
        aLongBool = self.streamBytes(aLongBool, FIX_sizeof(UNRESOLVED.longbool))
    
    def streamShortint(self, aShortint):
        aShortint = self.streamBytes(aShortint, FIX_sizeof(shortint))
        return aShortint
    
    def streamSmallint(self, aSmallint):
        aSmallint = self.streamBytes(aSmallint, FIX_sizeof(smallint))
        return aSmallint
    
    def streamLongint(self, aLongint):
        aLongint = self.streamBytes(aLongint, FIX_sizeof(longint))
        return aLongint
    
    def streamByte(self, aByte):
        aByte = self.streamBytes(aByte, FIX_sizeof(byte))
        return aByte
    
    def streamWord(self, aWord):
        aWord = self.streamBytes(aWord, FIX_sizeof(word))
        return aWord
    
    def streamReal(self, aReal):
        aReal = self.streamBytes(aReal, FIX_sizeof(real))
        return aReal
    
    def streamSingle(self, aSingle):
        aSingle = self.streamBytes(aSingle, FIX_sizeof(single))
        return aSingle
    
    def streamSingleArray(self, anArray):
        #var i: integer;
        anArray = self.streamBytes(anArray, FIX_sizeof(anArray))
        #if this doesn't work, use loop
        #for i := 0 to high(anArray) do self.streamSingle(anArray[i]);
        return anArray
    
    def streamBooleanArray(self, anArray):
        anArray = self.streamBytes(anArray, FIX_sizeof(anArray))
        return anArray
    
    def streamDouble(self, aDouble):
        aDouble = self.streamBytes(aDouble, FIX_sizeof(double))
        return aDouble
    
    def streamExtended(self, anExtended):
        anExtended = self.streamBytes(anExtended, FIX_sizeof(extended))
        return anExtended
    
    def streamComp(self, aComp):
        aComp = self.streamBytes(aComp, FIX_sizeof(comp))
        return aComp
    
    #common types
    #common types
    #win 32 defines these to be made of longints, so just stream smalls..
    def streamPoint(self, aPoint):
        raise "method streamPoint had assigned to var parameter aPoint not added to return; fixup manually"
        x = 0
        y = 0
        
        if self.isReading():
            x = self.streamSmallint(x)
            y = self.streamSmallint(y)
            aPoint = Point(x, y)
        else:
            x = aPoint.X
            y = aPoint.Y
            x = self.streamSmallint(x)
            y = self.streamSmallint(y)
    
    def streamSinglePoint(self, aPoint):
        raise "method streamSinglePoint had assigned to var parameter aPoint not added to return; fixup manually"
        x = 0.0
        y = 0.0
        
        if self.isReading():
            x = self.streamSingle(x)
            y = self.streamSingle(y)
            aPoint = usupport.setSinglePoint(x, y)
        else:
            x = aPoint.x
            y = aPoint.y
            x = self.streamSingle(x)
            y = self.streamSingle(y)
    
    def streamRect(self, aRect):
        raise "method streamRect had assigned to var parameter aRect not added to return; fixup manually"
        top = 0
        left = 0
        bottom = 0
        right = 0
        
        if self.isReading():
            left = self.streamSmallint(left)
            top = self.streamSmallint(top)
            right = self.streamSmallint(right)
            bottom = self.streamSmallint(bottom)
            aRect = Rect(left, top, right, bottom)
        else:
            left = aRect.Left
            top = aRect.Top
            right = aRect.Right
            bottom = aRect.Bottom
            left = self.streamSmallint(left)
            top = self.streamSmallint(top)
            right = self.streamSmallint(right)
            bottom = self.streamSmallint(bottom)
    
    #streams 32 bit locations
    def streamBigPoint(self, aPoint):
        aPoint = self.streamBytes(aPoint, FIX_sizeof(delphi_compatability.TPoint))
    
    #streams 32 bit locations
    def streamBigRect(self, aRect):
        aRect = self.streamBytes(aRect, FIX_sizeof(delphi_compatability.TRect))
    
    def streamColor(self, aColor):
        aColor = self.streamBytes(aColor, FIX_sizeof(delphi_compatability.TColor))
    
    def streamColorRef(self, aColorRef):
        aColorRef = self.streamBytes(aColorRef, FIX_sizeof(delphi_compatability.TColorRef))
    
    def streamRGB(self, aRGB):
        aRGB = self.streamBytes(aRGB, FIX_sizeof(longint))
        return aRGB
    
    def streamPenStyle(self, aPenStyle):
        aPenStyle = self.streamBytes(aPenStyle, FIX_sizeof(delphi_compatability.TPenStyle))
    
    def streamWindowState(self, aWindowState):
        aWindowState = self.streamBytes(aWindowState, FIX_sizeof(UNRESOLVED.TWindowState))
    
    #this function assumes the objects in the string list are nil or are
    #StreamableObject subclasses and are listed in the CreateStreamableObject function
    def streamStringList(self, aStringList):
        theCount = 0L
        i = 0L
        aStreamableObject = PdStreamableObject()
        theString = ""
        
        if self.isWriting():
            theCount = aStringList.Count
            theCount = self.streamLongint(theCount)
            if theCount > 0:
                for i in range(0, theCount):
                    theString = aStringList.Strings[i]
                    #could stream ansi ? - won't work in gsim
                    theString = self.streamShortString(theString)
                    aStreamableObject = aStringList.Objects[i] as PdStreamableObject
                    self.streamOrCreateObject(aStreamableObject)
        elif self.isReading():
            aStringList.Clear()
            theCount = self.streamLongint(theCount)
            if theCount > 0:
                for i in range(0, theCount):
                    #could stream ansi ? - won't work in gsim
                    theString = self.streamShortString(theString)
                    aStringList.Add(theString)
                    #needs to be nil when passed to next call for a read
                    aStreamableObject = None
                    self.streamOrCreateObject(aStreamableObject)
                    if aStreamableObject != None:
                        aStringList.Objects[i] = aStreamableObject
    
    def streamListOfLongints(self, aList):
        theCount = 0L
        i = 0L
        theValue = 0L
        
        if self.isWriting():
            theCount = aList.Count
            theCount = self.streamLongint(theCount)
            if theCount > 0:
                for i in range(0, theCount):
                    theValue = aList.Items[i]
                    theValue = self.streamLongint(theValue)
        elif self.isReading():
            aList.Clear()
            theCount = self.streamLongint(theCount)
            if theCount > 0:
                for i in range(0, theCount):
                    theValue = self.streamLongint(theValue)
                    aList.Add(UNRESOLVED.Pointer(theValue))
    
    def streamCursor(self, aCursor):
        aCursor = self.streamBytes(aCursor, FIX_sizeof(delphi_compatability.TCursor))
    
    #uses memory stream which is somewhat inefficient because
    #of the double copying and memory allocation.
    #TIcon cannot be written mre easily because of
    #private fields which would need to be accessed for size and data.
    #Unfortunately TIcon only provides ways to read and write assuming
    #the whole stream is made of the icon
    #copy from is also inefficient because it allocates a buffer -
    #probably could copy more directly from one stream to another
    #since one is a memory stream and is already in memory
    def streamIcon(self, anIcon):
        memoryStream = TMemoryStream()
        iconSize = 0L
        
        memoryStream = delphi_compatability.TMemoryStream.create
        if self.isReading():
            iconSize = self.streamLongint(iconSize)
            #put icon in memory stream
            memoryStream.CopyFrom(self.stream, iconSize)
            memoryStream.Position = 0
            anIcon.LoadFromStream(memoryStream)
        elif self.isWriting():
            anIcon.SaveToStream(memoryStream)
            memoryStream.Position = 0
            iconSize = memoryStream.Size
            iconSize = self.streamLongint(iconSize)
            #put memory stream in other stream
            self.stream.CopyFrom(memoryStream, iconSize)
        memoryStream.free
    
    #class level streaming
    def save(self, fileName, objectToSave):
        fileStream = TFileStream()
        filer = PdFiler()
        
        fileStream = delphi_compatability.TFileStream().Create(fileName, delphi_compatability.fmOpenWrite or delphi_compatability.fmCreate)
        try:
            filer = PdFiler().createWithStream(fileStream)
            filer.setToWritingMode()
            try:
                objectToSave.streamUsingFiler(filer)
            finally:
                filer.free
        finally:
            fileStream.free
    
    #class save/load functions
    def load(self, fileName, objectToLoad):
        fileStream = TFileStream()
        filer = PdFiler()
        
        fileStream = delphi_compatability.TFileStream().Create(fileName, delphi_compatability.fmOpenRead)
        try:
            filer = PdFiler().createWithStream(fileStream)
            filer.setToReadingMode()
            try:
                objectToLoad.streamUsingFiler(filer)
            finally:
                filer.free
        finally:
            fileStream.free
    
    def relativize(self, filename):
        result = ""
        path = ""
        currentDirectory = ""
        exeDirectory = ""
        
        result = filename
        path = ExtractFilePath(filename)
        currentDirectory = ExtractFilePath(ExpandFileName("junk.tmp"))
        exeDirectory = ExtractFilePath(delphi_compatability.Application.exeName)
        if (UNRESOLVED.CompareText(currentDirectory, UNRESOLVED.copy(path, 1, len(currentDirectory))) == 0):
            result = UNRESOLVED.copy(filename, len(currentDirectory) + 1, 256)
        elif (UNRESOLVED.CompareText(exeDirectory, UNRESOLVED.copy(path, 1, len(exeDirectory))) == 0):
            result = UNRESOLVED.copy(filename, len(exeDirectory) + 1, 256)
            if FileExists(currentDirectory + result):
                #don't relativize if file is also in current directory
                result = filename
        return result
    
    def streamNilObject(self):
        cvir = PdClassAndVersionInformationRecord()
        
        cvir.classNumber = uclasses.kTNil
        cvir.versionNumber = 0
        self.streamClassAndVersionInformation(cvir)
    
    def streamOrCreateObject(self, anObject):
        raise "method streamOrCreateObject had assigned to var parameter anObject not added to return; fixup manually"
        cvir = PdClassAndVersionInformationRecord()
        oldPosition = 0L
        
        if (self.isReading()) and (anObject != None):
            raise GeneralException.create("Problem: Argument should be nil if reading; in method PdFiler.streamOrCreateObject.")
        if self.isWriting():
            if anObject == None:
                self.streamNilObject()
            else:
                anObject.streamUsingFiler(self)
        elif self.isReading():
            oldPosition = self.getStreamPosition()
            self.streamClassAndVersionInformation(cvir)
            anObject = uclasses.CreateStreamableObjectFromClassAndVersionInformation(cvir)
            if anObject != None:
                #reset the stream because object will reread its information
                self.setStreamPosition(oldPosition)
                anObject.streamUsingFiler(self)
    
    def getStreamPosition(self):
        result = 0L
        result = self.stream.Position
        return result
    
    def setStreamPosition(self, position):
        self.stream.Position = position
    
class PdStreamableObject(TObject):
    def __init__(self):
        pass
    
    #PdStreamableObject
    #use for auto creating classes when type not known
    #use for checking if structure has changed
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdStreamableObject
        cvir.versionNumber = 0
        cvir.additionNumber = 0
        raise GeneralException.create("Problem: Subclass should override; in method PdStreamableObject.classAndVersionInformation.")
    
    def streamDataWithFiler(self, filer, cvir):
        pass
        #does nothing for this class - sublcasses should override
    
    #return true if should read data - false if this function read it
    #this fuction needs to be overriden if it will read the data instead of raising exception
    #exception handlers need to skip over data if desired
    #skip it code - filer.setStreamPosition(filer.getStreamPosition + size); - note this might fail
    #if size is some crazy number outside of stream.  The might not get nic error message...
    def verifyClassAndVersionInformation(self, filer, size, cvirRead, cvirClass):
        result = false
        if cvirRead.classNumber != cvirClass.classNumber:
            raise PdExceptionFilerUnexpectedClassNumber().createWithSizeAndMessage(size, "Problem reading file.  This file may be corrupt. (Expected class " + IntToStr(cvirClass.classNumber) + " read class " + IntToStr(cvirRead.classNumber) + ")")
            #filer.setStreamPosition(filer.getStreamPosition + size);
            #  	result := false;
            #    exit;  
        if cvirRead.versionNumber != cvirClass.versionNumber:
            #assuming that later can read earlier or will issue error
            #if caller wants to recover - can manually create object and read size bytes
            raise PdExceptionFilerUnexpectedVersionNumber().createWithSizeAndMessage(size, "Problem reading file.  This file is of a different version than the program. (Class " + IntToStr(cvirClass.classNumber) + " version " + IntToStr(cvirClass.versionNumber) + " cannot read version " + IntToStr(cvirRead.versionNumber) + ")")
            #filer.setStreamPosition(filer.getStreamPosition + size);
            #  	result := false;
            #    exit;
        result = true
        return result
    
    #stream out class ref num which can be used for loading
    def streamUsingFiler(self, filer):
        theSize = 0L
        endPosition = 0L
        sizePosition = 0L
        startPosition = 0L
        cvirClass = PdClassAndVersionInformationRecord()
        cvirRead = PdClassAndVersionInformationRecord()
        
        self.classAndVersionInformation(cvirClass)
        if filer.isWriting():
            filer.streamClassAndVersionInformation(cvirClass)
            theSize = -1
            sizePosition = filer.getStreamPosition()
            theSize = filer.streamLongint(theSize)
            startPosition = filer.getStreamPosition()
            self.streamDataWithFiler(filer, cvirClass)
            endPosition = filer.getStreamPosition()
            filer.setStreamPosition(sizePosition)
            #size does not include itself or object header
            theSize = endPosition - startPosition
            theSize = filer.streamLongint(theSize)
            filer.setStreamPosition(endPosition)
        elif filer.isReading():
            filer.streamClassAndVersionInformation(cvirRead)
            theSize = filer.streamLongint(theSize)
            startPosition = filer.getStreamPosition()
            if self.verifyClassAndVersionInformation(filer, theSize, cvirRead, cvirClass):
                self.streamDataWithFiler(filer, cvirRead)
            endPosition = filer.getStreamPosition()
            if endPosition < startPosition + theSize:
                #handle if haven't read everything due to additions or other version handling...
                filer.setStreamPosition(startPosition + theSize)
            elif endPosition > startPosition + theSize:
                raise PdExceptionFilerReadPastEndOfObject.create("Problem reading file: Read past the end of class " + IntToStr(cvirRead.classNumber) + " ver " + IntToStr(cvirRead.versionNumber) + " add " + IntToStr(cvirRead.additionNumber))
    
    #sublasses that include references to other subcomponent objects should instantiate them in an oveeride of this method
    #don't forget to use override in subclasses!
    def create(self):
        TObject.create(self)
        return self
    
    #don't forget to use override in subclasses!
    #copy this object to another.  This uses a memory stream rather than
    #field by field copies.  This is done because it is easier to maintain
    #(especiallyf for complex objects like the drawing plant).  Otherwise
    #every change to an objects fields would necessitae maintaining a copy
    #function.  This is slightly less efficient than field by field,
    #however presumeably copy won't be called that often so the speed difference
    #(double the time or more?) will not be noticed.  Note that this can fail
    #if there is no memory for the stream or filer or any subobjects in
    #the copy
    #when using this for plants, be careful to set the soil patch
    #in the copy to something desireable before calling
    def copyTo(self, newCopy):
        memoryStream = TMemoryStream()
        filer = PdFiler()
        
        if self.classType != newCopy.classType:
            raise GeneralException.create("Problem: copyTo can only be used with objects of identical class types; in method PdStreamableObject.copyTo.")
        memoryStream = delphi_compatability.TMemoryStream.create
        filer = PdFiler().createWithStream(memoryStream)
        filer.setToWritingMode()
        self.streamUsingFiler(filer)
        #move to start of stream
        memoryStream.Seek(0, 0)
        filer.setToReadingMode()
        newCopy.streamUsingFiler(filer)
        filer.free
        memoryStream.free
    
    def countSize(self):
        result = 0L
        memoryStream = TMemoryStream()
        filer = PdFiler()
        
        memoryStream = delphi_compatability.TMemoryStream.create
        filer = PdFiler().createWithStream(memoryStream)
        filer.setToCountingMode()
        self.streamUsingFiler(filer)
        result = filer.bytesStreamed
        filer.free
        memoryStream.free
        return result
    
class PdExceptionFiler(Exception):
    def __init__(self):
        self.size = 0L
    
    # PdFiler 
    def createWithSizeAndMessage(self, theSize, theMessage):
        self.create(theMessage)
        self.size = theSize
        return self
    
class PdExceptionFilerUnexpectedClassNumber(PdExceptionFiler):
    def __init__(self):
        pass
    
class PdExceptionFilerUnexpectedVersionNumber(PdExceptionFiler):
    def __init__(self):
        pass
    
class PdExceptionFilerReadPastEndOfObject(PdExceptionFiler):
    def __init__(self):
        pass
    
#
#{ when i switched to all 32-bit, i looked at this and it was all commented out and never used. so
#  i am taking it out. }
#    class procedure copyFile(Source, Dest: shortstring);
#class procedure PdFiler.copyFile(Source, Dest: shortstring);
#(*var
#  SourceHand, DestHand: Integer;
#  OpenBuf: TOFStruct;
#begin
#  { Place null-terminators at the end of the strings, so we can emulate a }
#  { PChar.  Note that (for safety) this will truncate a string if it is   }
#  { 255 characters long, but that's beyond the DOS filename limit anyway. }
#  { Open source file, and pass our psuedo-PChar as the filename }
#  SourceHand := LZOpenFile(pchar(Source), OpenBuf, of_Share_Deny_Write or of_Read);
#  { raise an exception on error }
#  if SourceHand = -1 then
#    raise EInOutError.Create('Error opening source file');
#  { Open destination file, and pass our psuedo-PChar as the filename }
#  DestHand := LZOpenFile(pchar(Dest), OpenBuf, of_Share_Exclusive or of_Write
#                         or of_Create);
#  { close source and raise exception on error }
#  if DestHand = -1 then begin
#    LZClose(SourceHand);
#    raise EInOutError.Create('Error opening destination file');
#  end;
#  try
#    { copy source to dest, raise exception on error }
#    if LZCopy(SourceHand, DestHand) < 0 then
#      raise EInOutError.Create('Error copying file');
#  finally
#    { whether or not an exception occurs, we need to close the files }
#    LZClose(SourceHand);
#    LZClose(DestHand);
#  end;
#end; 
