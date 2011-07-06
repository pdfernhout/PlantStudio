unit Usection;

interface

uses ucollect, uparams;

const kMaxSectionItems = 200; // v2.0 increased

type
PdSection = class
  public
  numSectionItems: smallint;
  sectionItems: array[0..kMaxSectionItems] of smallint;
  name: string;
  showInParametersWindow: boolean;
  expanded: boolean;
  isOrthogonal: boolean; // v2.1
  procedure addSectionItem(newSectionItem: smallint);
  function getName: string;
  procedure setName(newName: string);
  end;

PdSectionManager = class
 	public
  sections: TListCollection;
  orthogonalSections: TListCollection;
	constructor create; 
  destructor destroy; override;
	function addSection(aName: string): PdSection;
	function addOrthogonalSection(aName: string): PdSection;
  function sectionForName(aName: string): PdSection;
  function parameterForSectionAndName(aSectionName, aParameterName: string): PdParameter;
  end;

implementation

uses SysUtils, udomain, udebug;

{ ----------------------------------------------------------------- PdSection }
procedure PdSection.addSectionItem(newSectionItem: smallint);
  begin
  inc(numSectionItems);
  sectionItems[numSectionItems-1] := newSectionItem;
  end;

function PdSection.getName: string;
  begin
  result := self.name;
  end;

procedure PdSection.setName(newName: string);
  begin
  name := newName;
  end;

{ ----------------------------------------------------------------- PdSectionManager }
constructor PdSectionManager.create;
  begin
  inherited create;
  sections := TListCollection.create;
  // v2.1
  orthogonalSections := TListCollection.create;
  end;

destructor PdSectionManager.destroy;
	begin
  sections.free;
  sections := nil;
  // v2.1
  orthogonalSections.free;
  orthogonalSections := nil;
  inherited destroy;
  end;

function PdSectionManager.addSection(aName: string): PdSection;
	var
		section: PdSection;
	begin
  section := PdSection.create;
  section.name := aName;
  sections.add(section);
  result := section;
  end;

// v2.1
function PdSectionManager.addOrthogonalSection(aName: string): PdSection;
	var
		section: PdSection;
    i: smallint;
	begin
  section := PdSection.create;
  section.name := aName;
  orthogonalSections.add(section);
  // put in one header param so they can easily open and close all the items
  domain.parameterManager.addParameterForSection(section.name, '',
    PdParameter.make(1000 + orthogonalSections.count, 'header', section.name,
    7{header type}, 0, 0, 0, 0, 0, 0.00000000, 0.00000000, '', false, false, '', 0,
    'These parameters can also be found in other (main) sections, but you may want to look at together here.'));
  result := section;
  end;

function PdSectionManager.sectionForName(aName: string): PdSection;
  var
    i: smallint;
    section: PdSection;
  begin
  result := nil;
  if sections.count > 0 then
    for i := 0 to sections.count - 1 do
      begin
      section := PdSection(sections.items[i]);
      if aName = section.name then
        begin
        result := section;
        exit;
        end;
      end;
  // v2.1
  if orthogonalSections.count > 0 then
    for i := 0 to orthogonalSections.count - 1 do
      begin
      section := PdSection(orthogonalSections.items[i]);
      if aName = section.name then
        begin
        result := section;
        exit;
        end;
      end;
  end;

// v2.1 override changed to use section and parameter name
function PdSectionManager.parameterForSectionAndName(aSectionName, aParameterName: string): PdParameter;
  var
    i, j, fieldNumber: smallint;
    section: PdSection;
    parameter: PdParameter;
  begin
  result := nil;
  // a stab at backward compatibility - if no section name, try to find param anyway
  if aSectionName = '' then
    begin
    parameter := nil;
    parameter := domain.parameterManager.parameterForName(aParameterName);
    if parameter <> nil then
      begin
      result := parameter;
      exit;
      end;
    end
  else if sections.count > 0 then
    for i := 0 to sections.count - 1 do
      begin
      section := PdSection(sections.items[i]);
      if aSectionName = section.name then
        begin
        for j := 0 to section.numSectionItems - 1 do
          begin
          fieldNumber := section.sectionItems[j];
          parameter := nil;
          parameter := domain.parameterManager.parameterForFieldNumber(fieldNumber);
          if (parameter <> nil) and (parameter.name = aParameterName) then
            begin
            result := parameter;
            exit;
            end;
          end;
        end;
      end;
  end;

         
end.
