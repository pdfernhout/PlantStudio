unit Ucollect;

interface

uses Classes,
  ufiler;

type
  TForEachProc = procedure(each: TObject; data: TObject);
  TFirstLastFunc = function(each: TObject; data: TObject): Boolean;

  TListCollection = class(TList)
    public
    destructor Destroy; override;
    procedure ForEach(Proc: TForEachProc; data: TObject);
    function FirstThat(TestFunc: TFirstLastFunc; data: TObject): TObject;
    function LastThat(TestFunc: TFirstLastFunc; data: TObject): TObject;
    procedure streamUsingFiler(filer: PdFiler; classForCreating: PdStreamableObjectClass);
    procedure clear; {note this should be virtual in TList but it isn't}
    procedure clearPointersWithoutDeletingObjects;
    end;

procedure addToListIfAbsent(list: TList; item: TObject);

implementation

uses ClipBrd, WinTypes, WinProcs;

procedure addToListIfAbsent(list: TList; item: TObject);
  begin
  if item = nil then exit;
  if list.indexOf(item) < 0 then
    list.add(item);
  end;

procedure TListCollection.clear;
  var
    i: integer;
    temp: TObject;
  begin
  if count > 0 then
  	for i:= 0 to count - 1 do
    	begin
    	temp := items[i];
      items[i] := nil;
    	temp.free;
    	end;
  inherited clear;
  end;

procedure TListCollection.clearPointersWithoutDeletingObjects;
  var
    i: integer;
  begin
  if count > 0 then
  	for i:= 0 to count - 1 do
      items[i] := nil;
  inherited clear;
  end;

destructor TListCollection.Destroy;
  begin
  {pdf - clear will be called twice since inherited destroy also clears - but minor problem}
	self.clear;
  inherited Destroy;
  end;

procedure TListCollection.ForEach(proc: TForEachProc; data: TObject);
  var
    i: integer;
  begin
  if count > 0 then
 	 	for i := 0 to count - 1 do
    	proc(items[i], data);
  end;

function TListCollection.FirstThat(testFunc: TFirstLastFunc; data: TObject): TObject;
  var
    i: integer;
  begin
  result := nil;
  if count > 0 then
  	for i := 0 to count - 1 do
    	if testFunc(items[i], data) then
        begin
      	result := items[i];
      	break;
    	  end;
  end;

function TListCollection.LastThat(testFunc: TFirstLastFunc; data: TObject): TObject;
  var
    i: integer;
  begin
  result := nil;
  if count > 0 then
  	for i := count - 1 downto 0 do
    	if testFunc(Items[i], data) then
        begin
      	result := items[i];
      	break;
    	  end;
  end;

procedure TListCollection.streamUsingFiler(filer: PdFiler; classForCreating: PdStreamableObjectClass);
  var
  	countOnStream: longint;
  	i: longint;
    streamableObject: PdStreamableObject;
	begin
  if filer.isReading then
  	begin
    self.clear;
    filer.streamLongint(countOnStream);
    if countOnStream > 0 then
      begin
      self.setCapacity(countOnStream);
			for i := 0 to countOnStream - 1 do
    		begin
      	streamableObject := classForCreating.create;
      	streamableObject.streamUsingFiler(filer);
    		self.add(streamableObject);
      	end;
      end;
    end
  else {filer is writing or counting}
    begin
    countOnStream := count;
    filer.streamLongint(countOnStream);
    if countOnStream > 0 then
    	for i := 0 to countOnStream - 1 do
    		begin
      	streamableObject := PdStreamableObject(self.items[i]);
      	streamableObject.streamUsingFiler(filer);
      	end;
    end;
  end;

end.

(* functions for global clipboard transfer, not using
    procedure copyToClipboard(classForCreating: PdStreamableObjectClass; format: word);
    procedure getFromClipboard(classForCreating: PdStreamableObjectClass; format: word);

procedure TListCollection.copyToClipboard(classForCreating: PdStreamableObjectClass; format: word);
  var
    memoryStream: TMemoryStream;
    filer: PdFiler;
    handleToBuffer: THandle;
    pointerToBuffer: Pointer;
  begin
  memoryStream := TMemoryStream.create;
  filer := PdFiler.createWithStream(memoryStream);
  try
    filer.setToWritingMode;
    self.streamUsingFiler(filer, classForCreating);
    handleToBuffer := GlobalAlloc(GMEM_MOVEABLE, memoryStream.size);
    try
      pointerToBuffer := GlobalLock(handleToBuffer);
      try
        System.Move(memoryStream.memory^, pointerToBuffer^, memoryStream.size);
        Clipboard.setAsHandle(format, handleToBuffer);
      finally
        GlobalUnlock(handleToBuffer);
      end;
    except
      GlobalFree(handleToBuffer);
      raise;
    end;
  finally
    memoryStream.free;
    filer.free;
  end;
end;

procedure TListCollection.getFromClipboard(classForCreating: PdStreamableObjectClass; format: word);
  var
    memoryStream : TMemoryStream;
    filer: PdFiler;
    handleToBuffer: THandle;
    pointerToBuffer: Pointer;
  begin
  handleToBuffer := Clipboard.GetAsHandle(format);
  if handleToBuffer <> 0 then begin
    pointerToBuffer := GlobalLock(handleToBuffer);
    if pointerToBuffer <> nil then begin
      try
        memoryStream := TMemoryStream.Create;
        try
          memoryStream.writeBuffer(pointerToBuffer^, GlobalSize(handleToBuffer));
          memoryStream.position := 0;
          filer := PdFiler.createWithStream(memoryStream);
          filer.setToReadingMode;
          self.streamUsingFiler(filer, classForCreating);
        finally
          memoryStream.free;
          filer.free;
        end;
      finally
        GlobalUnlock(handleToBuffer);
      end;
    end;
  end;
end;
*)

