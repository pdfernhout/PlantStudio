// unit Ufiler

from conversion_common import *;
import usupport;
import delphi_compatability;

//
//  For every streamable object,
//  	Set class number to constant from uclasses.
//    Increment version number if change streamed structure (watch out for base class streaming changes!).
//    Increment addition number if add new field and older program versions can ignore it and you can default it.
//      In addition case, check additions number in streamDataWithFiler.
//      When create new version, you should usually reset additions to zero and
//      	remove additions testing code in streaming.
//  
// record
class PdClassAndVersionInformationRecord {
    public short classNumber;
    public short versionNumber;
    public short additionNumber;
}

// FIX enumerated type PdFilerMode
class PdFilerMode:
    filerModeReading, filerModeWriting, filerModeCounting = range(3)


// const
kMinWidthOnScreen = 40;
kMinHeightOnScreen = 20;


// global functions 
public void StreamFormPositionInfoWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir, TForm form) {
    TRect tempBoundsRect = new TRect();
    boolean tempVisible = false;
    TWindowState tempWindowState = new TWindowState();
    
    if (filer == null) {
        return;
    }
    if (form == null) {
        return;
    }
    if (filer.isReading()) {
        form.Visible = false;
    }
    if (filer.isReading()) {
        filer.streamRect(tempBoundsRect);
        if (tempBoundsRect.Left > delphi_compatability.Screen.Width - kMinWidthOnScreen) {
            // keep window on screen - left corner of title bar 
            tempBoundsRect.Left = delphi_compatability.Screen.Width - kMinWidthOnScreen;
        }
        if (tempBoundsRect.Top > delphi_compatability.Screen.Height - kMinHeightOnScreen) {
            tempBoundsRect.Top = delphi_compatability.Screen.Height - kMinHeightOnScreen;
        }
        form.Position = delphi_compatability.TPosition.poDesigned;
        form.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right - tempBoundsRect.Left, tempBoundsRect.Bottom - tempBoundsRect.Top);
    } else {
        tempBoundsRect = form.BoundsRect;
        filer.streamRect(tempBoundsRect);
    }
    if (filer.isReading()) {
        tempVisible = filer.streamBoolean(tempVisible);
        filer.streamWindowState(tempWindowState);
        form.WindowState = tempWindowState;
        // make visible last 
        form.Visible = tempVisible;
    } else {
        tempVisible = form.Visible;
        tempVisible = filer.streamBoolean(tempVisible);
        tempWindowState = form.WindowState;
        filer.streamWindowState(tempWindowState);
    }
}

public void StreamComboBoxItemIndexWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir, TComboBox comboBox) {
    long tempItemIndex = 0;
    
    if (filer.isReading()) {
        tempItemIndex = -1;
        tempItemIndex = filer.streamLongint(tempItemIndex);
        if ((comboBox.Items.Count > 0) && (tempItemIndex >= 0) && (tempItemIndex <= comboBox.Items.Count - 1)) {
            comboBox.ItemIndex = tempItemIndex;
        }
    } else {
        tempItemIndex = comboBox.ItemIndex;
        tempItemIndex = filer.streamLongint(tempItemIndex);
    }
}

public void StreamComboBoxItemIndexToTempVarWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir, TComboBox comboBox, long saveIndex) {
    long tempItemIndex = 0;
    
    if (filer.isReading()) {
        tempItemIndex = -1;
        tempItemIndex = filer.streamLongint(tempItemIndex);
        saveIndex = tempItemIndex;
    } else {
        tempItemIndex = comboBox.ItemIndex;
        tempItemIndex = filer.streamLongint(tempItemIndex);
    }
    return saveIndex;
}


class PdFiler extends TObject {
    public TStream stream;
    public PdFilerMode mode;
    public long bytesStreamed;
    public TObject resourceProvider;
    
    //an object that can be used to look up shared resource references
    public void createWithStream(TStream aStream) {
        this.stream = aStream;
        if (this.stream == null) {
            this.setToCountingMode();
        }
        //should test type of stream to auomatically set reading or writing mode
    }
    
    public void setToReadingMode() {
        this.mode = PdFilerMode.filerModeReading;
        this.bytesStreamed = 0;
        if (this.stream == null) {
            // was LoadStr( )
            throw new delphi_compatability.EReadError.create(UNRESOLVED.SReadError);
        }
    }
    
    public void setToWritingMode() {
        this.mode = PdFilerMode.filerModeWriting;
        this.bytesStreamed = 0;
        if (this.stream == null) {
            // was LoadStr( )
            throw new delphi_compatability.EWriteError.create(UNRESOLVED.SWriteError);
        }
    }
    
    public void setToCountingMode() {
        this.mode = PdFilerMode.filerModeCounting;
        this.bytesStreamed = 0;
    }
    
    public boolean isReading() {
        result = false;
        result = this.mode == PdFilerMode.filerModeReading;
        return result;
    }
    
    public boolean isWriting() {
        result = false;
        result = this.mode == PdFilerMode.filerModeWriting;
        return result;
    }
    
    public boolean isCounting() {
        result = false;
        result = this.mode == PdFilerMode.filerModeCounting;
        return result;
    }
    
    //simple types
    //simple types
    public void streamBytes(FIX_MISSING_ARG_TYPE bytes, long size) {
        switch (this.mode) {
            case PdFilerMode.filerModeReading:
                bytes = this.stream.read(bytes, size);
                break;
            case PdFilerMode.filerModeWriting:
                this.stream.write(bytes, size);
                break;
            case PdFilerMode.filerModeCounting:
                this.bytesStreamed = this.bytesStreamed + size;
                break;
        return bytes;
    }
    
    public void streamClassAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        switch (this.mode) {
            case PdFilerMode.filerModeReading:
                cvir = this.stream.read(cvir, FIX_sizeof(PdClassAndVersionInformationRecord));
                break;
            case PdFilerMode.filerModeWriting:
                this.stream.write(cvir, FIX_sizeof(PdClassAndVersionInformationRecord));
                break;
            case PdFilerMode.filerModeCounting:
                this.bytesStreamed = this.bytesStreamed + FIX_sizeof(PdClassAndVersionInformationRecord);
                break;
    }
    
    public void streamShortString(String aString) {
        switch (this.mode) {
            case PdFilerMode.filerModeReading:
                aString[0] = this.streamBytes(aString[0], 1);
                aString[1] = this.streamBytes(aString[1], ord(aString[0]));
                break;
            case PdFilerMode.filerModeWriting:
                aString = this.streamBytes(aString, len(aString) + 1);
                break;
            case PdFilerMode.filerModeCounting:
                this.bytesStreamed = this.bytesStreamed + len(aString) + 1;
                break;
        return aString;
    }
    
    public void streamAnsiString(ansistring aString) {
        long theLength = 0;
        
        switch (this.mode) {
            case PdFilerMode.filerModeReading:
                //make sure write out extra zero at end
                theLength = this.streamLongint(theLength);
                UNRESOLVED.setlength(aString, theLength);
                if (theLength > 0) {
                    aString.PDF_FIX_POINTER_ACCESS = this.streamBytes(aString.PDF_FIX_POINTER_ACCESS, theLength + 1);
                }
                break;
            case PdFilerMode.filerModeWriting:
                theLength = len(aString);
                theLength = this.streamLongint(theLength);
                if (theLength > 0) {
                    aString.PDF_FIX_POINTER_ACCESS = this.streamBytes(aString.PDF_FIX_POINTER_ACCESS, theLength + 1);
                }
                break;
            case PdFilerMode.filerModeCounting:
                this.bytesStreamed = this.bytesStreamed + len(aString) + 1;
                break;
    }
    
    //maybe problem in 32 bits - depends how big a string string alloc can return
    //need to stream "aPChar^" not just "aPChar".  The first is the array,
    //the second is just the space occupied by the pointer - and is a bug
    public void streamPChar("UNFINISHED_FIX_THIS_PCHAR_INIT" aPChar) {
        long stringLength = 0;
        
        switch (this.mode) {
            case PdFilerMode.filerModeReading:
                if (aPChar != null) {
                    UNRESOLVED.StrDispose(aPChar);
                    aPChar = null;
                }
                stringLength = this.streamBytes(stringLength, FIX_sizeof(longint));
                if (stringLength > 0) {
                    aPChar = UNRESOLVED.StrAlloc(stringLength);
                    if (aPChar == null) {
                        throw new GeneralException.create("Problem: Out of memory.");
                    }
                    aPChar.PDF_FIX_POINTER_ACCESS = this.streamBytes(aPChar.PDF_FIX_POINTER_ACCESS, stringLength);
                }
                break;
            case PdFilerMode.filerModeWriting:
                if (aPChar == null) {
                    stringLength = 0;
                } else {
                    stringLength = len(aPChar) + 1;
                }
                stringLength = this.streamBytes(stringLength, FIX_sizeof(longint));
                if (stringLength > 0) {
                    aPChar.PDF_FIX_POINTER_ACCESS = this.streamBytes(aPChar.PDF_FIX_POINTER_ACCESS, stringLength);
                }
                break;
            case PdFilerMode.filerModeCounting:
                this.bytesStreamed = this.bytesStreamed + FIX_sizeof(longint) + len(aPChar) + 1;
                break;
        return aPChar;
    }
    
    public void streamChar(char aChar) {
        aChar = this.streamBytes(aChar, FIX_sizeof(char));
        return aChar;
    }
    
    public void streamBoolean(boolean aBoolean) {
        aBoolean = this.streamBytes(aBoolean, FIX_sizeof(boolean));
        return aBoolean;
    }
    
    public void streamByteBool(bytebool aByteBool) {
        aByteBool = this.streamBytes(aByteBool, FIX_sizeof(UNRESOLVED.bytebool));
    }
    
    public void streamWordBool(wordbool aWordBool) {
        aWordBool = this.streamBytes(aWordBool, FIX_sizeof(UNRESOLVED.wordbool));
    }
    
    public void streamLongBool(longbool aLongBool) {
        aLongBool = this.streamBytes(aLongBool, FIX_sizeof(UNRESOLVED.longbool));
    }
    
    public void streamShortint(short aShortint) {
        aShortint = this.streamBytes(aShortint, FIX_sizeof(shortint));
        return aShortint;
    }
    
    public void streamSmallint(short aSmallint) {
        aSmallint = this.streamBytes(aSmallint, FIX_sizeof(smallint));
        return aSmallint;
    }
    
    public void streamLongint(long aLongint) {
        aLongint = this.streamBytes(aLongint, FIX_sizeof(longint));
        return aLongint;
    }
    
    public void streamByte(byte aByte) {
        aByte = this.streamBytes(aByte, FIX_sizeof(byte));
        return aByte;
    }
    
    public void streamWord(byte aWord) {
        aWord = this.streamBytes(aWord, FIX_sizeof(word));
        return aWord;
    }
    
    public void streamReal(float aReal) {
        aReal = this.streamBytes(aReal, FIX_sizeof(real));
        return aReal;
    }
    
    public void streamSingle(float aSingle) {
        aSingle = this.streamBytes(aSingle, FIX_sizeof(single));
        return aSingle;
    }
    
    public void streamSingleArray( anArray) {
        //var i: integer;
        anArray = this.streamBytes(anArray, FIX_sizeof(anArray));
        //if this doesn't work, use loop
        //for i := 0 to high(anArray) do self.streamSingle(anArray[i]);
        return anArray;
    }
    
    public void streamBooleanArray( anArray) {
        anArray = this.streamBytes(anArray, FIX_sizeof(anArray));
        return anArray;
    }
    
    public void streamDouble(double aDouble) {
        aDouble = this.streamBytes(aDouble, FIX_sizeof(double));
        return aDouble;
    }
    
    public void streamExtended(double anExtended) {
        anExtended = this.streamBytes(anExtended, FIX_sizeof(extended));
        return anExtended;
    }
    
    public void streamComp("UNFINISHED_FIX_THIS_COMP_INIT" aComp) {
        aComp = this.streamBytes(aComp, FIX_sizeof(comp));
        return aComp;
    }
    
    //common types
    //common types
    //win 32 defines these to be made of longints, so just stream smalls..
    public void streamPoint(TPoint aPoint) {
        raise "method streamPoint had assigned to var parameter aPoint not added to return; fixup manually"
        short x = 0;
        short y = 0;
        
        if (this.isReading()) {
            x = this.streamSmallint(x);
            y = this.streamSmallint(y);
            aPoint = Point(x, y);
        } else {
            x = aPoint.X;
            y = aPoint.Y;
            x = this.streamSmallint(x);
            y = this.streamSmallint(y);
        }
    }
    
    public void streamSinglePoint(SinglePoint aPoint) {
        raise "method streamSinglePoint had assigned to var parameter aPoint not added to return; fixup manually"
        float x = 0.0;
        float y = 0.0;
        
        if (this.isReading()) {
            x = this.streamSingle(x);
            y = this.streamSingle(y);
            aPoint = usupport.setSinglePoint(x, y);
        } else {
            x = aPoint.x;
            y = aPoint.y;
            x = this.streamSingle(x);
            y = this.streamSingle(y);
        }
    }
    
    public void streamRect(TRect aRect) {
        raise "method streamRect had assigned to var parameter aRect not added to return; fixup manually"
        short top = 0;
        short left = 0;
        short bottom = 0;
        short right = 0;
        
        if (this.isReading()) {
            left = this.streamSmallint(left);
            top = this.streamSmallint(top);
            right = this.streamSmallint(right);
            bottom = this.streamSmallint(bottom);
            aRect = Rect(left, top, right, bottom);
        } else {
            left = aRect.Left;
            top = aRect.Top;
            right = aRect.Right;
            bottom = aRect.Bottom;
            left = this.streamSmallint(left);
            top = this.streamSmallint(top);
            right = this.streamSmallint(right);
            bottom = this.streamSmallint(bottom);
        }
    }
    
    //streams 32 bit locations
    public void streamBigPoint(TPoint aPoint) {
        aPoint = this.streamBytes(aPoint, FIX_sizeof(delphi_compatability.TPoint));
    }
    
    //streams 32 bit locations
    public void streamBigRect(TRect aRect) {
        aRect = this.streamBytes(aRect, FIX_sizeof(delphi_compatability.TRect));
    }
    
    public void streamColor(TColor aColor) {
        aColor = this.streamBytes(aColor, FIX_sizeof(delphi_compatability.TColor));
    }
    
    public void streamColorRef(TColorRef aColorRef) {
        aColorRef = this.streamBytes(aColorRef, FIX_sizeof(delphi_compatability.TColorRef));
    }
    
    public void streamRGB(long aRGB) {
        aRGB = this.streamBytes(aRGB, FIX_sizeof(longint));
        return aRGB;
    }
    
    public void streamPenStyle(TPenStyle aPenStyle) {
        aPenStyle = this.streamBytes(aPenStyle, FIX_sizeof(delphi_compatability.TPenStyle));
    }
    
    public void streamWindowState(TWindowState aWindowState) {
        aWindowState = this.streamBytes(aWindowState, FIX_sizeof(UNRESOLVED.TWindowState));
    }
    
    //this function assumes the objects in the string list are nil or are
    //StreamableObject subclasses and are listed in the CreateStreamableObject function
    public void streamStringList(TStringList aStringList) {
        long theCount = 0;
        long i = 0;
        PdStreamableObject aStreamableObject = new PdStreamableObject();
        String theString = "";
        
        if (this.isWriting()) {
            theCount = aStringList.Count;
            theCount = this.streamLongint(theCount);
            if (theCount > 0) {
                for (i = 0; i <= theCount - 1; i++) {
                    theString = aStringList.Strings[i];
                    //could stream ansi ? - won't work in gsim
                    theString = this.streamShortString(theString);
                    aStreamableObject = (PdStreamableObject)aStringList.Objects[i];
                    this.streamOrCreateObject(aStreamableObject);
                }
            }
        } else if (this.isReading()) {
            aStringList.Clear();
            theCount = this.streamLongint(theCount);
            if (theCount > 0) {
                for (i = 0; i <= theCount - 1; i++) {
                    //could stream ansi ? - won't work in gsim
                    theString = this.streamShortString(theString);
                    aStringList.Add(theString);
                    //needs to be nil when passed to next call for a read
                    aStreamableObject = null;
                    this.streamOrCreateObject(aStreamableObject);
                    if (aStreamableObject != null) {
                        aStringList.Objects[i] = aStreamableObject;
                    }
                }
            }
        }
    }
    
    public void streamListOfLongints(TList aList) {
        long theCount = 0;
        long i = 0;
        long theValue = 0;
        
        if (this.isWriting()) {
            theCount = aList.Count;
            theCount = this.streamLongint(theCount);
            if (theCount > 0) {
                for (i = 0; i <= theCount - 1; i++) {
                    theValue = aList.Items[i];
                    theValue = this.streamLongint(theValue);
                }
            }
        } else if (this.isReading()) {
            aList.Clear();
            theCount = this.streamLongint(theCount);
            if (theCount > 0) {
                for (i = 0; i <= theCount - 1; i++) {
                    theValue = this.streamLongint(theValue);
                    aList.Add(UNRESOLVED.Pointer(theValue));
                }
            }
        }
    }
    
    public void streamCursor(TCursor aCursor) {
        aCursor = this.streamBytes(aCursor, FIX_sizeof(delphi_compatability.TCursor));
    }
    
    //uses memory stream which is somewhat inefficient because
    //of the double copying and memory allocation.
    //TIcon cannot be written mre easily because of
    //private fields which would need to be accessed for size and data.
    //Unfortunately TIcon only provides ways to read and write assuming
    //the whole stream is made of the icon
    //copy from is also inefficient because it allocates a buffer -
    //probably could copy more directly from one stream to another
    //since one is a memory stream and is already in memory
    public void streamIcon(TIcon anIcon) {
        TMemoryStream memoryStream = new TMemoryStream();
        long iconSize = 0;
        
        memoryStream = delphi_compatability.TMemoryStream.create;
        if (this.isReading()) {
            iconSize = this.streamLongint(iconSize);
            //put icon in memory stream
            memoryStream.CopyFrom(this.stream, iconSize);
            memoryStream.Position = 0;
            anIcon.LoadFromStream(memoryStream);
        } else if (this.isWriting()) {
            anIcon.SaveToStream(memoryStream);
            memoryStream.Position = 0;
            iconSize = memoryStream.Size;
            iconSize = this.streamLongint(iconSize);
            //put memory stream in other stream
            this.stream.CopyFrom(memoryStream, iconSize);
        }
        memoryStream.free;
    }
    
    //class level streaming
    public void save(String fileName, PdStreamableObject objectToSave) {
        TFileStream fileStream = new TFileStream();
        PdFiler filer = new PdFiler();
        
        fileStream = delphi_compatability.TFileStream().Create(fileName, delphi_compatability.fmOpenWrite || delphi_compatability.fmCreate);
        try {
            filer = PdFiler().createWithStream(fileStream);
            filer.setToWritingMode();
            try {
                objectToSave.streamUsingFiler(filer);
            } finally {
                filer.free;
            }
        } finally {
            fileStream.free;
        }
    }
    
    //class save/load functions
    public void load(String fileName, PdStreamableObject objectToLoad) {
        TFileStream fileStream = new TFileStream();
        PdFiler filer = new PdFiler();
        
        fileStream = delphi_compatability.TFileStream().Create(fileName, delphi_compatability.fmOpenRead);
        try {
            filer = PdFiler().createWithStream(fileStream);
            filer.setToReadingMode();
            try {
                objectToLoad.streamUsingFiler(filer);
            } finally {
                filer.free;
            }
        } finally {
            fileStream.free;
        }
    }
    
    public String relativize(String filename) {
        result = "";
        String path = "";
        String currentDirectory = "";
        String exeDirectory = "";
        
        result = filename;
        path = ExtractFilePath(filename);
        currentDirectory = ExtractFilePath(ExpandFileName("junk.tmp"));
        exeDirectory = ExtractFilePath(delphi_compatability.Application.exeName);
        if ((UNRESOLVED.CompareText(currentDirectory, UNRESOLVED.copy(path, 1, len(currentDirectory))) == 0)) {
            result = UNRESOLVED.copy(filename, len(currentDirectory) + 1, 256);
        } else if ((UNRESOLVED.CompareText(exeDirectory, UNRESOLVED.copy(path, 1, len(exeDirectory))) == 0)) {
            result = UNRESOLVED.copy(filename, len(exeDirectory) + 1, 256);
            if (FileExists(currentDirectory + result)) {
                //don't relativize if file is also in current directory
                result = filename;
            }
        }
        return result;
    }
    
    public void streamNilObject() {
        PdClassAndVersionInformationRecord cvir = new PdClassAndVersionInformationRecord();
        
        cvir.classNumber = UNRESOLVED.KTNil;
        cvir.versionNumber = 0;
        this.streamClassAndVersionInformation(cvir);
    }
    
    public void streamOrCreateObject(PdStreamableObject anObject) {
        raise "method streamOrCreateObject had assigned to var parameter anObject not added to return; fixup manually"
        PdClassAndVersionInformationRecord cvir = new PdClassAndVersionInformationRecord();
        long oldPosition = 0;
        
        if ((this.isReading()) && (anObject != null)) {
            throw new GeneralException.create("Problem: Argument should be nil if reading; in method PdFiler.streamOrCreateObject.");
        }
        if (this.isWriting()) {
            if (anObject == null) {
                this.streamNilObject();
            } else {
                anObject.streamUsingFiler(this);
            }
        } else if (this.isReading()) {
            oldPosition = this.getStreamPosition();
            this.streamClassAndVersionInformation(cvir);
            anObject = UNRESOLVED.CreateStreamableObjectFromClassAndVersionInformation(cvir);
            if (anObject != null) {
                //reset the stream because object will reread its information
                this.setStreamPosition(oldPosition);
                anObject.streamUsingFiler(this);
            }
        }
    }
    
    public long getStreamPosition() {
        result = 0;
        result = this.stream.Position;
        return result;
    }
    
    public void setStreamPosition(long position) {
        this.stream.Position = position;
    }
    
}
class PdStreamableObject extends TObject {
    
    //PdStreamableObject
    //use for auto creating classes when type not known
    //use for checking if structure has changed
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.KPdStreamableObject;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
        throw new GeneralException.create("Problem: Subclass should override; in method PdStreamableObject.classAndVersionInformation.");
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        pass
        //does nothing for this class - sublcasses should override
    }
    
    //return true if should read data - false if this function read it
    //this fuction needs to be overriden if it will read the data instead of raising exception
    //exception handlers need to skip over data if desired
    //skip it code - filer.setStreamPosition(filer.getStreamPosition + size); - note this might fail
    //if size is some crazy number outside of stream.  The might not get nic error message...
    public boolean verifyClassAndVersionInformation(PdFiler filer, long size, PdClassAndVersionInformationRecord cvirRead, PdClassAndVersionInformationRecord cvirClass) {
        result = false;
        if (cvirRead.classNumber != cvirClass.classNumber) {
            throw new PdExceptionFilerUnexpectedClassNumber().createWithSizeAndMessage(size, "Problem reading file.  This file may be corrupt. (Expected class " + IntToStr(cvirClass.classNumber) + " read class " + IntToStr(cvirRead.classNumber) + ")");
            //filer.setStreamPosition(filer.getStreamPosition + size);
            //  	result := false;
            //    exit;  
        }
        if (cvirRead.versionNumber != cvirClass.versionNumber) {
            //assuming that later can read earlier or will issue error
            //if caller wants to recover - can manually create object and read size bytes
            throw new PdExceptionFilerUnexpectedVersionNumber().createWithSizeAndMessage(size, "Problem reading file.  This file is of a different version than the program. (Class " + IntToStr(cvirClass.classNumber) + " version " + IntToStr(cvirClass.versionNumber) + " cannot read version " + IntToStr(cvirRead.versionNumber) + ")");
            //filer.setStreamPosition(filer.getStreamPosition + size);
            //  	result := false;
            //    exit;
        }
        result = true;
        return result;
    }
    
    //stream out class ref num which can be used for loading
    public void streamUsingFiler(PdFiler filer) {
        long theSize = 0;
        long endPosition = 0;
        long sizePosition = 0;
        long startPosition = 0;
        PdClassAndVersionInformationRecord cvirClass = new PdClassAndVersionInformationRecord();
        PdClassAndVersionInformationRecord cvirRead = new PdClassAndVersionInformationRecord();
        
        this.classAndVersionInformation(cvirClass);
        if (filer.isWriting()) {
            filer.streamClassAndVersionInformation(cvirClass);
            theSize = -1;
            sizePosition = filer.getStreamPosition();
            theSize = filer.streamLongint(theSize);
            startPosition = filer.getStreamPosition();
            this.streamDataWithFiler(filer, cvirClass);
            endPosition = filer.getStreamPosition();
            filer.setStreamPosition(sizePosition);
            //size does not include itself or object header
            theSize = endPosition - startPosition;
            theSize = filer.streamLongint(theSize);
            filer.setStreamPosition(endPosition);
        } else if (filer.isReading()) {
            filer.streamClassAndVersionInformation(cvirRead);
            theSize = filer.streamLongint(theSize);
            startPosition = filer.getStreamPosition();
            if (this.verifyClassAndVersionInformation(filer, theSize, cvirRead, cvirClass)) {
                this.streamDataWithFiler(filer, cvirRead);
            }
            endPosition = filer.getStreamPosition();
            if (endPosition < startPosition + theSize) {
                //handle if haven't read everything due to additions or other version handling...
                filer.setStreamPosition(startPosition + theSize);
            } else if (endPosition > startPosition + theSize) {
                throw new PdExceptionFilerReadPastEndOfObject.create("Problem reading file: Read past the end of class " + IntToStr(cvirRead.classNumber) + " ver " + IntToStr(cvirRead.versionNumber) + " add " + IntToStr(cvirRead.additionNumber));
            }
        }
    }
    
    //sublasses that include references to other subcomponent objects should instantiate them in an oveeride of this method
    //don't forget to use override in subclasses!
    public void create() {
        super.create();
    }
    
    //don't forget to use override in subclasses!
    //copy this object to another.  This uses a memory stream rather than
    //field by field copies.  This is done because it is easier to maintain
    //(especiallyf for complex objects like the drawing plant).  Otherwise
    //every change to an objects fields would necessitae maintaining a copy
    //function.  This is slightly less efficient than field by field,
    //however presumeably copy won't be called that often so the speed difference
    //(double the time or more?) will not be noticed.  Note that this can fail
    //if there is no memory for the stream or filer or any subobjects in
    //the copy
    //when using this for plants, be careful to set the soil patch
    //in the copy to something desireable before calling
    public void copyTo(PdStreamableObject newCopy) {
        TMemoryStream memoryStream = new TMemoryStream();
        PdFiler filer = new PdFiler();
        
        if (this.classType != newCopy.classType) {
            throw new GeneralException.create("Problem: copyTo can only be used with objects of identical class types; in method PdStreamableObject.copyTo.");
        }
        memoryStream = delphi_compatability.TMemoryStream.create;
        filer = PdFiler().createWithStream(memoryStream);
        filer.setToWritingMode();
        this.streamUsingFiler(filer);
        //move to start of stream
        memoryStream.Seek(0, 0);
        filer.setToReadingMode();
        newCopy.streamUsingFiler(filer);
        filer.free;
        memoryStream.free;
    }
    
    public long countSize() {
        result = 0;
        TMemoryStream memoryStream = new TMemoryStream();
        PdFiler filer = new PdFiler();
        
        memoryStream = delphi_compatability.TMemoryStream.create;
        filer = PdFiler().createWithStream(memoryStream);
        filer.setToCountingMode();
        this.streamUsingFiler(filer);
        result = filer.bytesStreamed;
        filer.free;
        memoryStream.free;
        return result;
    }
    
}
class PdExceptionFiler extends Exception {
    public long size;
    
    // PdFiler 
    public void createWithSizeAndMessage(long theSize, String theMessage) {
        this.create(theMessage);
        this.size = theSize;
    }
    
}
class PdExceptionFilerUnexpectedClassNumber extends PdExceptionFiler {
    
}
class PdExceptionFilerUnexpectedVersionNumber extends PdExceptionFiler {
    
}
class PdExceptionFilerReadPastEndOfObject extends PdExceptionFiler {
    
}
//
//{ when i switched to all 32-bit, i looked at this and it was all commented out and never used. so
//  i am taking it out. }
//    class procedure copyFile(Source, Dest: shortstring);
//class procedure PdFiler.copyFile(Source, Dest: shortstring);
//(*var
//  SourceHand, DestHand: Integer;
//  OpenBuf: TOFStruct;
//begin
//  { Place null-terminators at the end of the strings, so we can emulate a }
//  { PChar.  Note that (for safety) this will truncate a string if it is   }
//  { 255 characters long, but that's beyond the DOS filename limit anyway. }
//  { Open source file, and pass our psuedo-PChar as the filename }
//  SourceHand := LZOpenFile(pchar(Source), OpenBuf, of_Share_Deny_Write or of_Read);
//  { raise an exception on error }
//  if SourceHand = -1 then
//    raise EInOutError.Create('Error opening source file');
//  { Open destination file, and pass our psuedo-PChar as the filename }
//  DestHand := LZOpenFile(pchar(Dest), OpenBuf, of_Share_Exclusive or of_Write
//                         or of_Create);
//  { close source and raise exception on error }
//  if DestHand = -1 then begin
//    LZClose(SourceHand);
//    raise EInOutError.Create('Error opening destination file');
//  end;
//  try
//    { copy source to dest, raise exception on error }
//    if LZCopy(SourceHand, DestHand) < 0 then
//      raise EInOutError.Create('Error copying file');
//  finally
//    { whether or not an exception occurs, we need to close the files }
//    LZClose(SourceHand);
//    LZClose(DestHand);
//  end;
//end; 
