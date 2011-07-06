unit Uparams;

interface

uses ucollect;

const
  { FieldType }
  kFieldUndefined = 0;
  kFieldFloat = 1;
  kFieldSmallint = 2;
  kFieldColor = 3;
  kFieldBoolean = 4;
  kFieldThreeDObject = 5;
  kFieldEnumeratedList = 6;
  kFieldHeader = 7;
  kFieldLongint = 8;
    {note: the longint type is NOT for use for parameters (in param panels or breeding).
     if you want to use a longint for a parameter, you have to
     update the breeding method and the method that creates param panels. the smallint panel will not
     work correctly with a longint as it is now (but you could subclass it if you need one).}

	{ IndexType - for arrays }               
  kIndexTypeUndefined = 0;
  kIndexTypeNone = 1;
  kIndexTypeSCurve = 3;

  { transferType - how data is transferred to and from model object }
  kTransferTypeUndefined = 0;
  kTransferTypeMFD = 1;  {mfd is short for MoveFieldData}
  kTransferTypeGetSetSCurve = 2;
  kTransferTypeObject3D = 3;

  kNotArray = -1;

type
  PdParameter = class
    public
    fieldNumber: smallint;
    fieldID: string[80];
    name: string[80];
    fieldType, indexType: smallint;
    unitSet, unitModel, unitMetric, unitEnglish: smallint;
    lowerBoundOriginal, upperBoundOriginal: single;
    defaultValueStringOriginal: string; {must be whole string to allow for tdos}
    cannotOverride, isOverridden: boolean;
    lowerBoundOverride, upperBoundOverride: single;
    defaultValueStringOverride: string;
    regrow, readOnly: boolean;
    accessString: string[80];
    transferType: smallint;
    hint: string;
    valueHasBeenReadForCurrentPlant: boolean;
    collapsed: boolean;
    originalSectionName: string[80]; // v2.1
    constructor create;
    constructor make(aFieldNumber: smallint; aFieldID: string; aName: string; aFieldType, anIndexType: smallint; aUnitSet, aUnitModel, aUnitMetric, aUnitEnglish: smallint;
      aLowerBound, anUpperBound: single; aDefaultValueString: string; aRegrow, aReadOnly: boolean; anAccessString: string; aTransferType: smallint; aHint: string);
    function lowerBound: single;
    function upperBound: single;
    function defaultValueString: string;
    function indexCount: integer;
    function getName: string;
    procedure setName(newName: string);
    function getHint: string;
    end;

PdParameterManager = class
 	public
  parameters: TListCollection;
  constructor create;
  destructor destroy; override;
  procedure makeParameters;
  procedure addParameter(newParameter: PdParameter);
  procedure addParameterForSection(sectionName: string; orthogonalSectionName: string; newParameter: PdParameter);
  procedure clearParameters;
  class function fieldTypeName(fieldType: integer): string;
  class function indexTypeName(indexType: integer): string;
  function parameterForIndex(index: longint): PdParameter;
  function parameterForFieldID(fieldID: string): PdParameter;
  function parameterForName(name: string): PdParameter;
  function parameterForFieldNumber(fieldNumber: longint): PdParameter;
  function parameterIndexForFieldNumber(fieldNumber: longint): integer;
  function parameterIndexForFieldID(fieldID: string): integer;
  procedure setAllReadFlagsToFalse;
  end;

implementation

uses SysUtils, Windows, Dialogs,
  uexcept, usupport, usection, uunits, umakepm, udomain;

{ ---------------------------------------------------------- PdParameter }
constructor PdParameter.create;
  begin
  collapsed := true;
  end;

constructor PdParameter.make(aFieldNumber: smallint; aFieldID: string; aName: string; aFieldType, anIndexType: smallint; aUnitSet, aUnitModel, aUnitMetric, aUnitEnglish: smallint;
    aLowerBound, anUpperBound: single; aDefaultValueString: string; aRegrow, aReadOnly: boolean; anAccessString: string; aTransferType: smallint; aHint: string);
  begin
  self.create;
  fieldNumber := aFieldNumber;
  fieldID := copy(aFieldID, 1, 80);
  name := copy(aName, 1, 80);
  fieldType := aFieldType;
  hint := aHint; // v2.0 headers can have hints
  if fieldType = kFieldHeader then exit;
  indexType := anIndexType;
  unitSet := aUnitSet;
  unitModel := aUnitModel;
  unitMetric := aUnitMetric;
  unitEnglish := aUnitEnglish;
  lowerBoundOriginal := aLowerBound;
  upperBoundOriginal := anUpperBound;
  defaultValueStringOriginal := aDefaultValueString;
  regrow := aRegrow;
  readOnly := aReadOnly;
  accessString := copy(anAccessString, 1, 80);
  transferType := aTransferType;
  //hint := aHint;
  end;

function PdParameter.indexCount: integer;
  begin
  result := 1;
  case indexType of
    kIndexTypeUndefined: result := 1;
    kIndexTypeNone: result := 1;
    kIndexTypeSCurve: result := 4;
  else
    raise Exception.create('Problem: Unexpected index type in method PdParameter.indexCount.');
  end;
  end;

function PdParameter.getName: string;
  begin
  result := self.name;
  end;

procedure PdParameter.setName(newName: string);
  begin
  name := copy(newName, 1, 80);
  end;

function PdParameter.lowerBound: single;
  begin
  if (not cannotOverride) and (isOverridden) then
    result := lowerBoundOverride
  else
    result := lowerBoundOriginal;
  end;

function PdParameter.upperBound: single;
  begin
  if (not cannotOverride) and (isOverridden) then
    result := upperBoundOverride
  else
    result := upperBoundOriginal;
  end;

function PdParameter.defaultValueString: string;
  begin
  if (not cannotOverride) and (isOverridden) then
    result := defaultValueStringOverride
  else
    result := defaultValueStringOriginal;
  end;                                               

function PdParameter.getHint: string;
  begin
  result := self.hint;
  end;

{ ---------------------------------------------------- PdParameterManager }
constructor PdParameterManager.create;
  begin
  inherited create;
  parameters := TListCollection.create;
  end;

destructor PdParameterManager.destroy;
	begin
  parameters.free;
  parameters := nil;
  inherited destroy;
  end;

procedure PdParameterManager.addParameter(newParameter: PdParameter);
	begin
  if newParameter <> nil then
    parameters.add(newParameter);
  end;

procedure PdParameterManager.addParameterForSection(sectionName: string; orthogonalSectionName: string;
    newParameter: PdParameter);
  var
    section: PdSection;
  begin
  section := nil;
  section := domain.sectionManager.sectionForName(sectionName);
  if section = nil then
    begin
    section := domain.sectionManager.addSection(sectionName);
    { the 'no section' section is hidden from the parameters window but we still want the section for writing out }
    section.showInParametersWindow := not (upperCase(sectionName) = upperCase('(no section)'));
    end;
  self.addParameter(newParameter);
  if section <> nil then
    begin
    newParameter.originalSectionName := sectionName;
    section.addSectionItem(newParameter.fieldNumber);
    end;
  // v2.1 orthogonal sections
  // limitation - each param can only have one orthogonal section specified
  // if want to add more later, use delimiter and parse
  orthogonalSectionName := trim(orthogonalSectionName);
  if orthogonalSectionName <> '' then
    begin
    section := nil;
    section := domain.sectionManager.sectionForName(orthogonalSectionName);
    if section = nil then
      begin
      section := domain.sectionManager.addOrthogonalSection(orthogonalSectionName);
      section.showInParametersWindow := true;
      section.isOrthogonal := true;
      end;
    if section <> nil then
      section.addSectionItem(newParameter.fieldNumber);
    end;
  end;

class function PdParameterManager.fieldTypeName(fieldType: integer): string;
  begin
  case fieldType of
    kFieldUndefined: result := 'Undefined';
    kFieldFloat: result := 'Single';
    kFieldSmallint: result := 'Smallint';
    kFieldColor: result := 'Color';
    kFieldBoolean: result := 'Boolean';
    kFieldThreeDObject: result := '3D object';
    kFieldEnumeratedList: result := 'List of choices';
    kFieldLongint: result := 'Longint';
    else result := 'not in list';
    end;
  end;

class function PdParameterManager.indexTypeName(indexType: integer): string;
  begin
  case indexType of
    kIndexTypeUndefined: result := 'Undefined';
    kIndexTypeNone: result := 'None';
    kIndexTypeSCurve: result := 'S curve';
    else result := 'not in list';
    end;
  end;

function PdParameterManager.parameterForIndex(index: longint): PdParameter;
	begin
  result := parameters.items[index];
  end;

procedure PdParameterManager.clearParameters;
  begin
  parameters.clear;
  end;

procedure PdParameterManager.setAllReadFlagsToFalse;
  var
    i: smallint;
  begin
  if parameters.count > 0 then
    for i := 0 to parameters.count - 1 do
      PdParameter(parameters.items[i]).valueHasBeenReadForCurrentPlant := false;
  end;

function PdParameterManager.parameterForFieldNumber(fieldNumber: longint): PdParameter;
  var
    i: smallint;
    parameter: PdParameter;
  begin
  result := nil;
  if parameters.count > 0 then
    for i := 0 to parameters.count - 1 do
      begin
      parameter := PdParameter(parameters.items[i]);
      if fieldNumber = parameter.fieldNumber then
        begin
        result := parameter;
        exit;
        end;
      end;
  raise Exception.create('Problem: Parameter not found for field number ' + intToStr(fieldNumber)
      + ' in method PdParameterManager.parameterForFieldNumber.');
  end;

function PdParameterManager.parameterForFieldID(fieldID: string): PdParameter;
  var
    i: smallint;
    parameter: PdParameter;
  begin
  result := nil;
  if parameters.count > 0 then
    for i := 0 to parameters.count - 1 do
      begin
      parameter := PdParameter(parameters.items[i]);
      if trim(upperCase(fieldID)) = trim(upperCase(parameter.fieldID)) then
        begin
        result := parameter;
        exit;
        end;
      end;
  raise Exception.create('Problem: Parameter not found for field ID ' + fieldID
      + ' in method PdParameterManager.parameterForFieldID.');
  end;

function PdParameterManager.parameterForName(name: string): PdParameter;
  var
    i: smallint;
    parameter: PdParameter;
  begin
  result := nil;
  if parameters.count > 0 then
    for i := 0 to parameters.count - 1 do
      begin
      parameter := PdParameter(parameters.items[i]);
      if trim(upperCase(name)) = trim(upperCase(parameter.name)) then
        begin
        result := parameter;
        exit;
        end;
      end;
  raise Exception.create('Problem: Parameter not found for name ' + name
      + ' in method PdParameterManager.parameterForName.');
  end;

function PdParameterManager.parameterIndexForFieldNumber(fieldNumber: longint): integer;
  var
    i: smallint;
    parameter: PdParameter;
  begin
  result := 0;
  if parameters.count > 0 then
    for i := 0 to parameters.count - 1 do
      begin
      parameter := PdParameter(parameters.items[i]);
      if fieldNumber = parameter.fieldNumber then
        begin
        result := i;
        exit;
        end;
      end;
  raise Exception.create('Problem: Parameter index not found for field number ' + intToStr(fieldNumber)
      + ' in method PdParameterManager.parameterIndexForFieldNumber.');
  end;

function PdParameterManager.parameterIndexForFieldID(fieldID: string): integer;
  var
  i: smallint;
  parameter: PdParameter;
  begin
  result := 0;
  if parameters.count > 0 then
    for i := 0 to parameters.count - 1 do
      begin
      parameter := PdParameter(parameters.items[i]);
      if trim(upperCase(fieldID)) = trim(upperCase(parameter.fieldID)) then 
        begin
        result := i;
        exit;
        end;
      end;
  raise Exception.create('Problem: Parameter index not found for field ID ' + fieldID
      + ' in method PdParameterManager.parameterIndexForFieldID.');
  end;

procedure PdParameterManager.makeParameters;
  begin
  CreateParameters(self);
  CreateParameters_SecondHalf(self);
  end;

end.
