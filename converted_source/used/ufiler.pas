unit Ufiler;

interface

uses StdCtrls, Forms, Classes, SysUtils, WinTypes, Graphics, LZExpand, Controls, usupport;

type

  {
  For every streamable object,
  	Set class number to constant from uclasses.
    Increment version number if change streamed structure (watch out for base class streaming changes!).
    Increment addition number if add new field and older program versions can ignore it and you can default it.
      In addition case, check additions number in streamDataWithFiler.
      When create new version, you should usually reset additions to zero and
      	remove additions testing code in streaming.
  }
  PdClassAndVersionInformationRecord = record
    classNumber: smallint;
    versionNumber: smallint;
    additionNumber: smallint;
    end;

  PdFilerMode = (filerModeReading, filerModeWriting, filerModeCounting);
  PdStreamableObject = class;

	PdFiler = class(TObject)
    public
    stream: TStream;
  	mode: PdFilerMode;
    bytesStreamed : longInt;
    resourceProvider: TObject; {an object that can be used to look up shared resource references}
    constructor createWithStream(aStream: TStream);
    procedure setToReadingMode;
    procedure setToWritingMode;
    procedure setToCountingMode;
    function isReading : boolean;
    function isWriting: boolean;
    function isCounting: boolean;
    {simple types}
    procedure streamBytes(var bytes; size: longInt);
    procedure streamClassAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
		procedure streamShortString(var aString: shortstring);
    procedure streamAnsiString(var aString: ansistring);
    procedure streamPChar(var aPChar: PChar);
    procedure streamChar(var aChar: char);
    procedure streamBoolean(var aBoolean: boolean);
    procedure streamByteBool(var aByteBool: bytebool);
    procedure streamWordBool(var aWordBool: wordbool);
    procedure streamLongBool(var aLongBool: longbool);
    procedure streamBooleanArray(var anArray: array of boolean);
    procedure streamShortint(var aShortint: shortint);
    procedure streamSmallint(var aSmallint: smallint);
    procedure streamLongint(var aLongint: longint);
    procedure streamByte(var aByte: byte);
    procedure streamWord(var aWord: word);
    procedure streamReal(var aReal: real);
    procedure streamSingle(var aSingle: single);
    procedure streamSingleArray(var anArray: array of single);
    procedure streamDouble(var aDouble: double);
    procedure streamExtended(var anExtended: extended);
    procedure streamComp(var aComp: comp);
    {common types}
    procedure streamPoint(var aPoint: TPoint);
    procedure streamSinglePoint(var aPoint: SinglePoint);
    procedure streamRect(var aRect: TRect);
    procedure streamBigPoint(var aPoint: TPoint);
    procedure streamBigRect(var aRect: TRect);
    procedure streamColor(var aColor: TColor);
    procedure streamColorRef(var aColorRef: TColorRef);
    procedure streamRGB(var aRGB: longint);
    procedure streamPenStyle(var aPenStyle: TPenStyle);
    procedure streamWindowState(var aWindowState: TWindowState);
    procedure streamStringList(aStringList: TStringList);
    procedure streamListOfLongints(aList: TList);
    procedure streamCursor(var aCursor: TCursor);
    procedure streamIcon(anIcon: TIcon);
    {class save/load functions}
		class procedure load(fileName: string; objectToLoad: PdStreamableObject);
		class procedure save(fileName: string; objectToSave: PdStreamableObject);
    class function relativize(const  fileName: string): string;
		procedure streamNilObject;
		procedure streamOrCreateObject(var anObject: PdStreamableObject);
    function getStreamPosition: longint;
    procedure setStreamPosition(position: longint);
		end;

	PdStreamableObject = class(TObject)
  	public
    procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); virtual;
		function verifyClassAndVersionInformation(
    	filer: PdFiler; size: longint; const cvirRead, cvirClass: PdClassAndVersionInformationRecord): boolean; virtual;
  	procedure streamUsingFiler(filer: PdFiler);
  	procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); virtual;
    constructor create; virtual; {don't forget to use override in subclasses!}
    procedure copyTo(newCopy: PdStreamableObject); virtual;
    function countSize: longint;
  end;

  PdStreamableObjectClass = class of PdStreamableObject;

  PdExceptionFiler = class(Exception)
    public
    size: longint;
    constructor createWithSizeAndMessage(theSize: longint; const theMessage: string);
    end;

  PdExceptionFilerUnexpectedClassNumber = class(PdExceptionFiler)
    public
    end;

  PdExceptionFilerUnexpectedVersionNumber = class(PdExceptionFiler)
    public
    end;

  PdExceptionFilerReadPastEndOfObject = class(PdExceptionFiler)
    public
    end;

procedure StreamFormPositionInfoWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord; form: TForm);
procedure StreamComboBoxItemIndexWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord;
    comboBox: TComboBox);
procedure StreamComboBoxItemIndexToTempVarWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord;
    comboBox: TComboBox; var saveIndex: longint);

implementation

uses Consts, uclasses;

const
  kMinWidthOnScreen = 40;
  kMinHeightOnScreen = 20;

{ global functions }
procedure StreamFormPositionInfoWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord; form: TForm);
  var
    tempBoundsRect: TRect;
    tempVisible: boolean;
    tempWindowState: TWindowState;
  begin
  if filer = nil then exit;
  if form = nil then exit;
  if filer.isReading then form.visible := false;
  if filer.isReading then
    begin
    filer.streamRect(tempBoundsRect);
    { keep window on screen - left corner of title bar }
    if tempBoundsRect.left > Screen.width - kMinWidthOnScreen then
      tempBoundsRect.left := Screen.width - kMinWidthOnScreen;
    if tempBoundsRect.top > Screen.height - kMinHeightOnScreen then
      tempBoundsRect.top := Screen.height - kMinHeightOnScreen;
    form.position := poDesigned;
    with tempBoundsRect do form.setBounds(left, top, right - left, bottom - top);  
    end
  else
    begin
    tempBoundsRect := form.boundsRect;
    filer.streamRect(tempBoundsRect);
    end;
  if filer.isReading then
    begin
    filer.streamBoolean(tempVisible);
    filer.streamWindowState(tempWindowState);
    form.windowState := tempWindowState;
    { make visible last }
    form.visible := tempVisible;
    end
  else
    begin
    tempVisible := form.visible;
    filer.streamBoolean(tempVisible);
    tempWindowState := form.windowState;
    filer.streamWindowState(tempWindowState);
    end;
  end;

procedure StreamComboBoxItemIndexWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord;
    comboBox: TComboBox);
  var
    tempItemIndex: longint;
  begin
  if filer.isReading then
    begin
    tempItemIndex := -1;
    filer.streamLongint(tempItemIndex);
    if (comboBox.items.count > 0) and (tempItemIndex >= 0) and (tempItemIndex <= comboBox.items.count - 1) then
      comboBox.itemIndex := tempItemIndex;
    end
  else
    begin
    tempItemIndex := comboBox.itemIndex;
    filer.streamLongint(tempItemIndex);
    end;
  end;

procedure StreamComboBoxItemIndexToTempVarWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord;
    comboBox: TComboBox; var saveIndex: longint);
  var
    tempItemIndex: longint;
  begin
  if filer.isReading then
    begin
    tempItemIndex := -1;
    filer.streamLongint(tempItemIndex);
    saveIndex := tempItemIndex;
    end
  else
    begin
    tempItemIndex := comboBox.itemIndex;
    filer.streamLongint(tempItemIndex);
    end;
  end;

{ PdFiler }
constructor PdExceptionFiler.createWithSizeAndMessage(theSize: longint; const theMessage: string);
  begin
  self.create(theMessage);
  size := theSize;
  end;

constructor PdFiler.createWithStream(aStream: TStream);
	begin
  stream := aStream;
  if stream = nil then self.setToCountingMode;
  {should test type of stream to auomatically set reading or writing mode}
  end;

procedure PdFiler.setToReadingMode;
	begin
  mode := filerModeReading;
  bytesStreamed := 0;
  if stream = nil then raise EReadError.create(SReadError);  // was LoadStr( )
  end;

procedure PdFiler.setToWritingMode;
	begin
  mode := filerModeWriting;
  bytesStreamed := 0;
  if stream = nil then raise EWriteError.create(SWriteError); // was LoadStr( )
  end;

procedure PdFiler.setToCountingMode;
	begin
  mode := filerModeCounting;
  bytesStreamed := 0;
  end;

function PdFiler.isReading : boolean;
	begin
  result := mode = filerModeReading;
  end;

function PdFiler.isWriting: boolean;
	begin
  result := mode = filerModeWriting;
  end;

function PdFiler.isCounting: boolean;
	begin
  result := mode = filerModeCounting;
  end;

{simple types}
procedure PdFiler.streamBytes(var bytes; size: longInt);
	begin
  case mode of
  	filerModeReading: stream.read(bytes, size);
    filerModeWriting: stream.write(bytes, size);
    filerModeCounting: bytesStreamed := bytesStreamed + size;
  end;
	end;

procedure PdFiler.streamClassAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  case mode of
  	filerModeReading: stream.read(cvir, sizeof(PdClassAndVersionInformationRecord));
    filerModeWriting: stream.write(cvir, sizeof(PdClassAndVersionInformationRecord));
    filerModeCounting: bytesStreamed := bytesStreamed + sizeof(PdClassAndVersionInformationRecord);
  end;
  end;

procedure PdFiler.streamShortString(var aString: shortstring);
	begin
  case mode of
    filerModeReading:
    	begin
  		self.streamBytes(aString[0], 1);
  		self.streamBytes(aString[1], Ord(aString[0]));
      end;
  	filerModeWriting: self.streamBytes(aString, length(aString) + 1);
    filerModeCounting: bytesStreamed := bytesStreamed + length(aString) + 1;
 	  end;
  end;

procedure PdFiler.streamAnsiString(var aString: ansistring);
  var
  	theLength: longint;
	begin
  {make sure write out extra zero at end}
  case mode of
    filerModeReading:
    	begin
  		self.streamLongint(theLength);
      setlength(aString, theLength);
      if theLength > 0 then
  			self.streamBytes(PChar(aString)^, theLength+1);
      end;
  	filerModeWriting:
      begin
      theLength := Length(aString);
			self.streamLongint(theLength);
      if theLength > 0 then
      	self.streamBytes(Pchar(aString)^, theLength+1);
      end;
    filerModeCounting: bytesStreamed := bytesStreamed + length(aString) + 1;
  end;
  end;

{maybe problem in 32 bits - depends how big a string string alloc can return}
{need to stream "aPChar^" not just "aPChar".  The first is the array,
the second is just the space occupied by the pointer - and is a bug}
procedure PdFiler.streamPChar(var aPChar: PChar);
	var
    stringLength : longint;
	begin
  case mode of
  	filerModeReading:
    	begin
    	if aPChar <> nil then
     	 begin
      	StrDispose(aPChar);
      	aPChar := nil;
      	end;
  		self.streamBytes(stringLength, sizeOf(longint));
      if stringLength > 0 then
        begin
        aPChar := StrAlloc(stringLength);
        if aPChar = nil then raise Exception.create('Problem: Out of memory.');
   		  self.streamBytes(aPChar^, stringLength);
        end;
      end;
    filerModeWriting:
    	begin
      if aPChar = nil then
        stringLength := 0
      else
      	stringLength := StrLen(aPChar) + 1;
  		self.streamBytes(stringLength, sizeOf(longint));
      if stringLength > 0 then
      	self.streamBytes(aPChar^, stringLength);
      end;
    filerModeCounting: bytesStreamed := bytesStreamed + sizeOf(longint) + StrLen(aPChar) + 1;
  	end;
  end;

procedure PdFiler.streamChar(var aChar: char);
	begin
  self.streamBytes(aChar, sizeOf(char));
  end;

procedure PdFiler.streamBoolean(var aBoolean: boolean);
	begin
  self.streamBytes(aBoolean, sizeOf(boolean));
  end;

procedure PdFiler.streamByteBool(var aByteBool: bytebool);
	begin
  self.streamBytes(aByteBool, sizeOf(bytebool));
  end;

procedure PdFiler.streamWordBool(var aWordBool: wordbool);
	begin
  self.streamBytes(aWordBool, sizeOf(wordbool));
  end;

procedure PdFiler.streamLongBool(var aLongBool: longbool);
	begin
  self.streamBytes(aLongBool, sizeOf(longbool));
  end;

procedure PdFiler.streamShortint(var aShortint: shortint);
	begin
  self.streamBytes(aShortint, sizeOf(shortint));
  end;

procedure PdFiler.streamSmallint(var aSmallint: smallint);
	begin
  self.streamBytes(aSmallint, sizeOf(smallint));
  end;

procedure PdFiler.streamLongint(var aLongint: longint);
	begin
  self.streamBytes(aLongint, sizeOf(longint));
  end;

procedure PdFiler.streamByte(var aByte: byte);
	begin
  self.streamBytes(aByte, sizeOf(byte));
  end;

procedure PdFiler.streamWord(var aWord: word);
	begin
  self.streamBytes(aWord, sizeOf(word));
  end;

procedure PdFiler.streamReal(var aReal: real);
	begin
  self.streamBytes(aReal, sizeOf(real));
  end;

procedure PdFiler.streamSingle(var aSingle: single);
	begin
  self.streamBytes(aSingle, sizeOf(single));
  end;

procedure PdFiler.streamSingleArray(var anArray: array of single);
  {var i: integer;}
  begin
  self.streamBytes(anArray, sizeOf(anArray));
  {if this doesn't work, use loop}
  {for i := 0 to high(anArray) do self.streamSingle(anArray[i]);}
  end;

procedure PdFiler.streamBooleanArray(var anArray: array of boolean);
  begin
  self.streamBytes(anArray, sizeOf(anArray));
  end;

procedure PdFiler.streamDouble(var aDouble: double);
	begin
  self.streamBytes(aDouble, sizeOf(double));
  end;

procedure PdFiler.streamExtended(var anExtended: extended);
	begin
  self.streamBytes(anExtended, sizeOf(extended));
  end;

procedure PdFiler.streamComp(var aComp: comp);
	begin
  self.streamBytes(aComp, sizeOf(comp));
  end;

{common types}

{win 32 defines these to be made of longints, so just stream smalls..}
procedure PdFiler.streamPoint(var aPoint: TPoint);
  var x, y: smallint;
	begin
  if self.isReading then
    begin
  	self.streamSmallint(x);
  	self.streamSmallint(y);
    aPoint := Point(x, y);
    end
  else
    begin
    x := aPoint.x;
    y := aPoint.y;
  	self.streamSmallint(x);
  	self.streamSmallint(y);
    end;
  end;

procedure PdFiler.streamSinglePoint(var aPoint: SinglePoint);
  var x, y: single;
	begin
  if self.isReading then
    begin
  	self.streamSingle(x);
  	self.streamSingle(y);
    aPoint := setSinglePoint(x, y);
    end
  else
    begin
    x := aPoint.x;
    y := aPoint.y;
  	self.streamSingle(x);
  	self.streamSingle(y);
    end;
  end;
  
procedure PdFiler.streamRect(var aRect: TRect);
  var top, left, bottom, right: smallint;
	begin
  if self.isReading then
    begin
  	self.streamSmallint(left);
  	self.streamSmallint(top);
  	self.streamSmallint(right);
  	self.streamSmallint(bottom);
    aRect := Rect(left, top, right, bottom);
    end
  else
    begin
    left := aRect.left;
    top := aRect.top;
    right := aRect.right;
    bottom := aRect.bottom;
  	self.streamSmallint(left);
  	self.streamSmallint(top);
  	self.streamSmallint(right);
  	self.streamSmallint(bottom);
    end;
  end;

{streams 32 bit locations}
procedure PdFiler.streamBigPoint(var aPoint: TPoint);
	begin
  self.streamBytes(aPoint, sizeOf(TPoint));
  end;

{streams 32 bit locations}
procedure PdFiler.streamBigRect(var aRect: TRect);
	begin
  self.streamBytes(aRect, sizeOf(TRect));
  end;

procedure PdFiler.streamColor(var aColor: TColor);
	begin
  self.streamBytes(aColor, sizeOf(TColor));
  end;

procedure PdFiler.streamColorRef(var aColorRef: TColorRef);
	begin
  self.streamBytes(aColorRef, sizeOf(TColorRef));
  end;

procedure PdFiler.streamRGB(var aRGB: longint);
	begin
  self.streamBytes(aRGB, sizeOf(longint));
  end;

procedure PdFiler.streamPenStyle(var aPenStyle: TPenStyle);
  begin
  self.streamBytes(aPenStyle, sizeof(TPenStyle));
  end;

procedure PdFiler.streamWindowState(var aWindowState: TWindowState);
  begin
  self.streamBytes(aWindowState, sizeof(TWindowState));
  end;

{this function assumes the objects in the string list are nil or are
StreamableObject subclasses and are listed in the CreateStreamableObject function}
procedure PdFiler.streamStringList(aStringList: TStringList);
  var
    theCount: longint;
    i: longint;
    aStreamableObject: PdStreamableObject;
    theString: shortstring;
  begin
  if self.isWriting then
    begin
    theCount := aStringList.count;
    self.streamLongint(theCount);
  	if theCount > 0 then for i := 0 to theCount - 1 do
  		begin
      theString := aStringList.strings[i];
      self.streamShortString(theString);  {could stream ansi ? - won't work in gsim}
      aStreamableObject := aStringList.objects[i] as PdStreamableObject;
      self.streamOrCreateObject(aStreamableObject);
    	end;
    end
  else if self.isReading then
    begin
    aStringList.clear;
    self.streamLongint(theCount);
  	if theCount > 0 then for i := 0 to theCount - 1 do
  		begin
      self.streamShortString(theString);  {could stream ansi ? - won't work in gsim}
      aStringList.add(theString);
      aStreamableObject := nil;   {needs to be nil when passed to next call for a read}
      streamOrCreateObject(aStreamableObject);
      if aStreamableObject <> nil then
       	aStringList.objects[i] := aStreamableObject;
    	end;
    end;
  end;

procedure PdFiler.streamListOfLongints(aList: TList);
  var
    theCount: longint;
    i: longint;
    theValue: longint;
  begin
  if self.isWriting then
    begin
    theCount := aList.count;
    self.streamLongint(theCount);
  	if theCount > 0 then for i := 0 to theCount - 1 do
  		begin
      theValue := longint(aList.items[i]);
      self.streamLongint(theValue);
      end;
    end
  else if self.isReading then
    begin
    aList.clear;
    self.streamLongint(theCount);
  	if theCount > 0 then for i := 0 to theCount - 1 do
  		begin
      self.streamLongint(theValue);
      aList.add(Pointer(theValue));
      end;
    end;
  end;

procedure PdFiler.streamCursor(var aCursor: TCursor);
	begin
  self.streamBytes(aCursor, sizeOf(TCursor));
  end;

{uses memory stream which is somewhat inefficient because
of the double copying and memory allocation.
TIcon cannot be written mre easily because of
private fields which would need to be accessed for size and data.
Unfortunately TIcon only provides ways to read and write assuming
the whole stream is made of the icon}
{copy from is also inefficient because it allocates a buffer -
probably could copy more directly from one stream to another
since one is a memory stream and is already in memory}
procedure PdFiler.streamIcon(anIcon: TIcon);
  var
  memoryStream: TMemoryStream;
  iconSize: longint;
  begin
  memoryStream := TMemoryStream.create;
  if self.isReading then
    begin
    self.streamLongint(iconSize);
    {put icon in memory stream}
    memoryStream.copyFrom(stream, iconSize);
    memoryStream.position := 0;
    anIcon.loadFromStream(memoryStream);
    end
  else if self.isWriting then
    begin
    anIcon.SaveToStream(memoryStream);
    memoryStream.position := 0;
    iconSize := memoryStream.size;
    self.streamLongint(iconSize);
    {put memory stream in other stream}
    stream.copyFrom(memoryStream, iconSize);
    end;
  memoryStream.free;
  end;

{class level streaming}
class procedure PdFiler.save(fileName: string; objectToSave: PdStreamableObject);
	var
  	fileStream: TFileStream;
		filer: PdFiler;
	begin
	fileStream := TFileStream.create(fileName, fmOpenWrite or fmCreate);
	try
		filer := PdFiler.createWithStream(fileStream);
    filer.setToWritingMode;
    try
    objectToSave.streamUsingFiler(filer);
    finally
		filer.free;
    end;
	finally
		fileStream.free;
	end;
	end;

class procedure PdFiler.load(fileName: string; objectToLoad: PdStreamableObject);
	var
  	fileStream: TFileStream;
		filer: PdFiler;
	begin
	fileStream := TFileStream.create(fileName, fmOpenRead);
	try
		filer := PdFiler.createWithStream(fileStream);
    filer.setToReadingMode;
    try
    objectToLoad.streamUsingFiler(filer);
    finally
		filer.free;
    end;
	finally
		fileStream.free;
	end;
	end;

class function PdFiler.relativize(const filename: string): string;
  var
    path: string;
    currentDirectory, exeDirectory: string;
  begin
  result := filename;
  path := ExtractFilePath(filename);
  currentDirectory := ExtractFilePath(ExpandFileName('junk.tmp'));
  exeDirectory := ExtractFilePath(Application.exeName);
  if (CompareText(currentDirectory, copy(path, 1, length(currentDirectory))) = 0) then
    result := copy(filename, length(currentDirectory) + 1, 256)
  else if (CompareText(exeDirectory, copy(path, 1, length(exeDirectory))) = 0) then
    begin
    result := copy(filename, length(exeDirectory) + 1, 256);
    {don't relativize if file is also in current directory}
    if FileExists(currentDirectory + result) then
      result := filename;
    end;
  end;

procedure PdFiler.streamNilObject;
  var
    cvir: PdClassAndVersionInformationRecord;
  begin
  cvir.classNumber := KTNil;
  cvir.versionNumber := 0;
  self.streamClassAndVersionInformation(cvir);
  end;

procedure PdFiler.streamOrCreateObject(var anObject: PdStreamableObject);
  var
    cvir: PdClassAndVersionInformationRecord;
    oldPosition: longint;
  begin
  if (self.isReading) and (anObject <> nil) then
    raise Exception.create('Problem: Argument should be nil if reading; in method PdFiler.streamOrCreateObject.');
  if self.isWriting then
    begin
    if anObject = nil then
      self.streamNilObject
    else
    	anObject.streamUsingFiler(self);
    end
  else if self.isReading then
    begin
    oldPosition := self.getStreamPosition;
    self.streamClassAndVersionInformation(cvir);
    anObject := CreateStreamableObjectFromClassAndVersionInformation(cvir);
    if anObject <> nil then
      begin
      {reset the stream because object will reread its information}
      self.setStreamPosition(oldPosition);
    	anObject.streamUsingFiler(self);
      end;
    end;
  end;

function PdFiler.getStreamPosition: longint;
  begin
  result := self.stream.position;
  end;

procedure PdFiler.setStreamPosition(position: longint);
  begin
  self.stream.position := position;
  end;

{PdStreamableObject}
{use for auto creating classes when type not known}
{use for checking if structure has changed}
procedure PdStreamableObject.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := KPdStreamableObject;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  raise Exception.create('Problem: Subclass should override; in method PdStreamableObject.classAndVersionInformation.');
  end;

procedure PdStreamableObject.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  begin
  {does nothing for this class - sublcasses should override}
  end;

{return true if should read data - false if this function read it}
{this fuction needs to be overriden if it will read the data instead of raising exception}
{exception handlers need to skip over data if desired}
{skip it code - filer.setStreamPosition(filer.getStreamPosition + size); - note this might fail
if size is some crazy number outside of stream.  The might not get nic error message...}
function PdStreamableObject.verifyClassAndVersionInformation(
	filer: PdFiler; size: longint; const cvirRead, cvirClass: PdClassAndVersionInformationRecord): boolean;
  begin
  if cvirRead.classNumber <> cvirClass.classNumber then
    begin
    raise PdExceptionFilerUnexpectedClassNumber.createWithSizeAndMessage(size,
    	'Problem reading file.  This file may be corrupt. (Expected class ' +
      IntToStr(cvirClass.classNumber) + ' read class ' +
      IntToStr(cvirRead.classNumber) + ')');
    {filer.setStreamPosition(filer.getStreamPosition + size);
  	result := false;
    exit;  }
    end;
    {assuming that later can read earlier or will issue error}
    {if caller wants to recover - can manually create object and read size bytes}
  if cvirRead.versionNumber <> cvirClass.versionNumber then
    begin
    raise PdExceptionFilerUnexpectedVersionNumber.createWithSizeAndMessage(size,
    	'Problem reading file.  This file is of a different version than the program. (Class ' + IntToStr(cvirClass.classNumber) +
    	' version ' + IntToStr(cvirClass.versionNumber) +
    	' cannot read version ' + IntToStr(cvirRead.versionNumber) + ')');
    {filer.setStreamPosition(filer.getStreamPosition + size);
  	result := false;
    exit;}
    end;
  result := true;
  end;

{stream out class ref num which can be used for loading}
procedure PdStreamableObject.streamUsingFiler(filer: PdFiler);
  var
    theSize: longint;
    endPosition, sizePosition, startPosition: longint;
    cvirClass: PdClassAndVersionInformationRecord;
    cvirRead: PdClassAndVersionInformationRecord;
	begin
  self.classAndVersionInformation(cvirClass);
  if filer.isWriting then
    begin
  	filer.streamClassAndVersionInformation(cvirClass);
    theSize := -1;
    sizePosition := filer.getStreamPosition;
  	filer.streamLongint(theSize);
    startPosition := filer.getStreamPosition;
    self.streamDataWithFiler(filer, cvirClass);
    endPosition := filer.getStreamPosition;
    filer.setStreamPosition(sizePosition);
    {size does not include itself or object header}
    theSize := endPosition - startPosition;
  	filer.streamLongint(theSize);
    filer.setStreamPosition(endPosition);
    end
  else if filer.isReading then
    begin
  	filer.streamClassAndVersionInformation(cvirRead);
  	filer.streamLongint(theSize);
    startPosition := filer.getStreamPosition;
    if verifyClassAndVersionInformation(filer, theSize, cvirRead, cvirClass) then
      self.streamDataWithFiler(filer, cvirRead);
    endPosition := filer.getStreamPosition;
    {handle if haven't read everything due to additions or other version handling...}
    if endPosition < startPosition + theSize then
      filer.setStreamPosition(startPosition + theSize)
    else if endPosition > startPosition + theSize then
      raise PdExceptionFilerReadPastEndOfObject.create('Problem reading file: Read past the end of class '
      	+ IntToStr(cvirRead.classNumber)
      	+  ' ver ' + IntToStr(cvirRead.versionNumber)
      	+  ' add ' + IntToStr(cvirRead.additionNumber));
    end;
  end;

{sublasses that include references to other subcomponent objects should instantiate them in an oveeride of this method}
{don't forget to use override in subclasses!}
constructor PdStreamableObject.create;
	begin
  inherited create;
  end;

{copy this object to another.  This uses a memory stream rather than
field by field copies.  This is done because it is easier to maintain
(especiallyf for complex objects like the drawing plant).  Otherwise
every change to an objects fields would necessitae maintaining a copy
function.  This is slightly less efficient than field by field,
however presumeably copy won't be called that often so the speed difference
(double the time or more?) will not be noticed.  Note that this can fail
if there is no memory for the stream or filer or any subobjects in
the copy}
{when using this for plants, be careful to set the soil patch
in the copy to something desireable before calling}
procedure PdStreamableObject.copyTo(newCopy: PdStreamableObject);
  var
    memoryStream: TMemoryStream;
    filer: PdFiler;
  begin
  if self.classType <> newCopy.classType then
    raise exception.create('Problem: copyTo can only be used with objects of identical class types; in method PdStreamableObject.copyTo.');
  memoryStream := TMemoryStream.create;
  filer := PdFiler.createWithStream(memoryStream);
  filer.setToWritingMode;
  self.streamUsingFiler(filer);
  memoryStream.seek(0,0); {move to start of stream}
  filer.setToReadingMode;
  newCopy.streamUsingFiler(filer);
  filer.free;
  memoryStream.free;
  end;

function PdStreamableObject.countSize: longint;
  var
    memoryStream: TMemoryStream;
    filer: PdFiler;
  begin
  memoryStream := TMemoryStream.create;
  filer := PdFiler.createWithStream(memoryStream);
  filer.setToCountingMode;
  self.streamUsingFiler(filer);
  result := filer.bytesStreamed;
  filer.free;
  memoryStream.free;
  end;

end.

(*
{ when i switched to all 32-bit, i looked at this and it was all commented out and never used. so
  i am taking it out. }
    class procedure copyFile(Source, Dest: shortstring);
class procedure PdFiler.copyFile(Source, Dest: shortstring);
(*var
  SourceHand, DestHand: Integer;
  OpenBuf: TOFStruct;
begin
  { Place null-terminators at the end of the strings, so we can emulate a }
  { PChar.  Note that (for safety) this will truncate a string if it is   }
  { 255 characters long, but that's beyond the DOS filename limit anyway. }
  { Open source file, and pass our psuedo-PChar as the filename }
  SourceHand := LZOpenFile(pchar(Source), OpenBuf, of_Share_Deny_Write or of_Read);
  { raise an exception on error }
  if SourceHand = -1 then
    raise EInOutError.Create('Error opening source file');
  { Open destination file, and pass our psuedo-PChar as the filename }
  DestHand := LZOpenFile(pchar(Dest), OpenBuf, of_Share_Exclusive or of_Write
                         or of_Create);
  { close source and raise exception on error }
  if DestHand = -1 then begin
    LZClose(SourceHand);
    raise EInOutError.Create('Error opening destination file');
  end;
  try
    { copy source to dest, raise exception on error }
    if LZCopy(SourceHand, DestHand) < 0 then
      raise EInOutError.Create('Error copying file');
  finally
    { whether or not an exception occurs, we need to close the files }
    LZClose(SourceHand);
    LZClose(DestHand);
  end;
end; *)
