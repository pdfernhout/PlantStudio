unit Uexcept;

interface

procedure FailNil(anObject: TObject);
procedure FailNilPtr(aPointer: Pointer);
procedure FailNilPChar(aPointer: PChar);

implementation
uses SysUtils;

procedure FailNil(anObject: TObject);
	begin
  if anObject = nil then raise Exception.create('Problem: Not enough memory to carry out that operation.');
  end;

procedure FailNilPtr(aPointer: Pointer);
	begin
  if aPointer = nil then raise Exception.create('Problem: Not enough memory to carry out that operation.');
  end;

procedure FailNilPChar(aPointer: PChar);
	begin
  if aPointer = nil then raise Exception.create('Problem: Not enough memory to carry out that operation.');
  end;

end.
