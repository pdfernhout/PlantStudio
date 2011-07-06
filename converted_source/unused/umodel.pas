unit Umodel;

interface

const
  kGetField = 0;
  kSetField = 1;
  kModelNameLength = 80;

type

  PdModel = class
  	public
    name: string[kModelNameLength];
    function getName: string; override;
    procedure setName(newName: string); override;
    wholeModelUpdateNeeded: boolean;
    procedure transferField(direction: integer; var value; fieldID, fieldType: smallint;
      updateList: TListCollection);
    procedure directTransferField(direction: integer; var value; fieldID, fieldType: smallint;
      updateList: TListCollection);
    procedure addToUpdateList(fieldID: integer; fieldIndex: integer; updateList: TListCollection);
		procedure MFD(var objectValue; var value; fieldType: integer; direction: integer);
   end;

  PdModelUpdateEvent = class
    public
    model: PdModel;
    fieldID: integer;
    fieldIndex: integer;
    end;

implementation

uses uclasses, usupport;

{ --------------------------------------------------------------------- PdModel}
function PdModel.getName: string;
  begin
  result := self.name;
  end;

procedure PdModel.setName(newName: string);
  begin
  name := copy(newName, 1, kModelNameLength);
  end;

procedure PdModel.transferField(direction: integer; var value; fieldID, fieldType: smallint;
    updateList: TListCollection);
  {var
    oldSingle: single;
    oldInteger: integer; }
	begin
  { MOST SIMPLE CASE - JUST CALL directTransferField }
  {oldSingle := 0.0;
  oldInteger := 0;
  if d = kSetField then
    begin
    if ft = kFieldFloat then
      directTransferField(kGetField, oldSingle, fieldID, ft, index, deriveMethod, updateList)
    else if ft = kFieldInt then
      directTransferField(kGetField, oldInteger, fieldID, ft, index, deriveMethod, updateList);
    end; }
  self.directTransferField(direction, value, fieldID, fieldType, updateList);
  {case fieldID of
     add special cases here - special cases may use oldSingle or oldInteger values
    end;}
  end;

procedure PdModel.directTransferField(direction: integer; var value; fieldID, fieldType: smallint;
    updateList: TListCollection);
	begin
  {do nothing - subclass can override}
  end;

procedure PdModel.addToUpdateList(fieldID: integer; updateList: TListCollection);
  var updateEvent: PdModelUpdateEvent;
	begin
  if updateList = nil then exit;
  updateEvent := PdModelUpdateEvent.create;
  updateEvent.model := self;
  updateEvent.fieldID := fieldID;
  updateList.add(updateEvent);
  end;

{may need to limit length of string copy?}
{MFD = MoveFieldData}
procedure PdModel.MFD(var objectValue; var value; fieldType: integer; direction: integer);
	begin
  if direction = kGetField then
    case fieldType of
  		kFieldFloat: 					single(value) := single(objectValue);
  		kFieldInt:   					smallint(value) := smallint(objectValue);
  		kFieldUnsignedLong:   longint(value) := longint(objectValue); {unsigned?}
  		kFieldUnsignedChar:   byte(value) := byte(objectValue);
  		kFieldString:         string(value) := string(objectValue);
  		kFieldFileString:     string(value) := string(objectValue);
  		kFieldColor:          TColorRef(value) := TColorRef(objectValue);
  		kFieldBoolean:        boolean(value) := boolean(objectValue);
      kFieldEnumeratedList: smallint(value) := smallint(objectValue);
    else
      raise Exception.create('Unsupported model transfer to field ' + IntToStr(fieldType));
    end
  else if direction = kSetField then
    case fieldType of
  		kFieldFloat: 					single(objectValue) := single(value);
  		kFieldInt:   					smallint(objectValue) := smallint(value);
  		kFieldUnsignedLong:   longint(objectValue) := longint(value); {unsigned?}
  		kFieldUnsignedChar:   byte(objectValue) := byte(value);
  		kFieldString:         string(objectValue) := string(value);
  		kFieldFileString:     string(objectValue) := string(value);
  		kFieldColor:          TColorRef(objectValue) := TColorRef(value);
  		kFieldBoolean:        boolean(objectValue) := boolean(value);
      kFieldEnumeratedList: smallint(objectValue) := smallint(value);
    else
      raise Exception.create('Unsupported model transfer to field ' + IntToStr(fieldType));
    end
	end;

end.
