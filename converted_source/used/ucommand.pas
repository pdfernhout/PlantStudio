unit Ucommand;

interface

uses Classes, WinTypes,
  ucollect;

type
TrackPhase = (trackPress, trackMove, trackRelease);

PdCommand = class(TObject)
	public
  canUndo: boolean;
  done: boolean;
  commandChangesPlantFile: boolean;
  plantFileChangedBeforeCommand: boolean;
  constructor create;
  destructor destroy; override;
  procedure doCommand; virtual;
  procedure undoCommand; virtual;
  procedure redoCommand; virtual;
  function description: string; virtual;
  function numberOfStoredLargeObjects: longint; virtual;
  function TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
  	mouseDidMove, rightButtonDown: boolean): PdCommand; virtual;
  end;

PdCommandList = class(TObject)
	public
	commands: TListCollection;
	lastDoneCommandIndex: longint;
  undoLimit, objectUndoLimit: longint;
  mouseCommand: PdCommand;
  anchorPoint: TPoint;
  previousPoint: TPoint;
  rightButtonDown: boolean;
  constructor create;
  destructor destroy; override;
  function command(index: longint): PdCommand;
  procedure setNewUndoLimit(newLimit: longint);
  procedure setNewObjectUndoLimit(newObjectLimit: longint);
	procedure freeCommandsAboveLimit(theLimit: longint);
  procedure freeCommandsAboveObjectLimit(objectLimit: longint);
  function objectCountInCommandList: longint;
  procedure doCommand(newCommand: PdCommand);
  function mouseDown(newCommand: PdCommand; point: TPoint): boolean;
  procedure mouseMove(point: TPoint);
  procedure mouseUp(point: TPoint);
  function isUndoEnabled: boolean;
  function isRedoEnabled: boolean;
  function undoDescription: string;
  function redoDescription: string;
  procedure undoLast;
  procedure removeCommand(aCommand: PdCommand);
  procedure redoLast;
  procedure fillListWithUndoableStrings(aList: TStringList);
  procedure fillListWithRedoableStrings(aList: TStringList);
  function lastCommandDone: PdCommand;
  function didMouseMove(point: TPoint): boolean;
  end;

implementation

uses SysUtils, usupport, umain, updcom;

const kMaxDescriptionLength = 40;

function limitDescription(description: string): string;
  begin
  result := description;
  if length(description) > kMaxDescriptionLength then
    result := copy(description, 1, kMaxDescriptionLength - 4) + ' ...';
  end;

constructor PdCommand.create;
	begin
  inherited create;
  canUndo := true;
  done := false;
  { default commandChangesPlantFile to true, since most commands change file,
    if command does not change file, set to false after call to inherited create }
  commandChangesPlantFile := true;
  plantFileChangedBeforeCommand := false;
  end;

destructor PdCommand.destroy;
	begin
  {sublass could override}
  inherited destroy;
  end;

procedure PdCommand.doCommand;
	begin
  self.done := true;
  if commandChangesPlantFile then
    begin
    plantFileChangedBeforeCommand := plantFileChanged;
    if MainForm <> nil then MainForm.setPlantFileChanged(true);
    end;
  {subclass should override and call inherited}
  end;

procedure PdCommand.undoCommand;
	begin
  self.done := false;
  if commandChangesPlantFile then
    if MainForm <> nil then MainForm.setPlantFileChanged(plantFileChangedBeforeCommand);
  {sublass should override and call inherited}
  end;

procedure PdCommand.redoCommand;
	begin
  self.doCommand;
  {sublass may override and call inherited doCommand}
  end;

function PdCommand.description: string;
	begin
  result := '*command description*';
  end;

function PdCommand.numberOfStoredLargeObjects: longint;
  begin
  result := 0;
  {subclasses may override but only if they keep copies of large objects}
  end;

function PdCommand.TrackMouse(aTrackPhase: TrackPhase; var anchorPoint, previousPoint, nextPoint: TPoint;
  	mouseDidMove, rightButtonDown: boolean): PdCommand;
  begin
  {sublasses should override if needed}
  result := self;
  end;

{PdCommandList}
constructor PdCommandList.create;
  begin
  inherited create;
  commands := TListCollection.create;
	lastDoneCommandIndex := -1;
  undoLimit := 50;
  objectUndoLimit := 10;
  end;

destructor PdCommandList.destroy;
	begin
  commands.free;
  commands := nil;
  {if mouseCoOmmand <> nil then error condition - ignoring for now - not released}
  {could only happend if quitting somehow in middle of action}
  inherited destroy;
  end;

function PdCommandList.command(index: longint): PdCommand;
	begin
  result := PdCommand(commands.items[index]);
  end;

procedure PdCommandList.setNewUndoLimit(newLimit: longint);
  begin
  if newLimit <> undoLimit then
    begin
    undoLimit := newLimit;
    self.freeCommandsAboveLimit(undoLimit);
    end;
  end;

procedure PdCommandList.setNewObjectUndoLimit(newObjectLimit: longint);
  begin
  if newObjectLimit <> objectUndoLimit then
    begin
    objectUndoLimit := newObjectLimit;
    self.freeCommandsAboveObjectLimit(objectUndoLimit);
    end;
  end;

{free any command more than the number passed in}
procedure PdCommandList.freeCommandsAboveLimit(theLimit: longint);
  var
    theCommand: PdCommand;
  begin
  while (commands.count > theLimit) and (commands.count > 0) do
  	begin
    theCommand := self.command(0);
    commands.delete(0);
    theCommand.free;
    dec(lastDoneCommandIndex);
    if lastDoneCommandIndex < -1 then lastDoneCommandIndex := -1;
    end;
  end;

procedure PdCommandList.freeCommandsAboveObjectLimit(objectLimit: longint);
  var
    theCommand: PdCommand;
    objectCount: longint;
  begin
  objectCount := self.objectCountInCommandList;
  while (objectCount > objectLimit) and (commands.count > 0) do
  	begin
    theCommand := self.command(0);
    commands.delete(0);
    theCommand.free;
    dec(lastDoneCommandIndex);
    if lastDoneCommandIndex < -1 then lastDoneCommandIndex := -1;
    objectCount := self.objectCountInCommandList;
    end;
  end;

function PdCommandList.objectCountInCommandList: longint;
  var
    i: longint;      
  begin
  result := 0;
  if commands.count <= 0 then exit;
  for i := 0 to commands.count - 1 do
    result := result + command(i).numberOfStoredLargeObjects;
  end;

procedure PdCommandList.doCommand(newCommand: PdCommand);
	var i: longint;
    theCommand: PdCommand;
	begin
  {remove any extra commands after the current}
  {do this first to free memory for command}
  if isRedoEnabled then
  	for i := commands.count - 1 downto lastDoneCommandIndex + 1 do
    	begin
      theCommand := command(i);
      commands.delete(i);
      theCommand.free;
      end;
  { first see if there are too many objects and if so, scroll them }
  self.freeCommandsAboveObjectLimit(objectUndoLimit - 1);
  {see if too many commands are stored and if so, scroll them}
  self.freeCommandsAboveLimit(undoLimit - 1);
  {now do this command}
  newCommand.doCommand; {may fail in which case won't add}
  commands.add(newCommand);
  inc(lastDoneCommandIndex);
  end;

{added nextMouseCommand in these three functions to deal with unhandled exceptions occurring
during mouse commands.  This way, the command will not be further processed.
This may occasionally leak - the mouse command should be the one responsible for freeing
itself and returning nil if a problem occurs}
{returns whether the command finished tracking without freeing itself}
function PdCommandList.mouseDown(newCommand: PdCommand; point: Tpoint): boolean;
  var
    nextMouseCommand: PdCommand;
	begin
  result := false;
  {check if need to clear mouse command}
  if mouseCommand <> nil then
    self.mouseUp(point);
  mouseCommand := nil;
  {save mouse command and start it}
  if newCommand <> nil then
    begin
    anchorPoint := point;
    previousPoint := point;
  	nextMouseCommand := newCommand;
  	mouseCommand := nextMouseCommand.trackMouse(TrackPress, anchorPoint, previousPoint, point, false, rightButtonDown);
    result := (mouseCommand <> nil);
    end;
  end;

const kMinMoveDistance = 2;

procedure PdCommandList.mouseMove(point: TPoint);
  var
    nextMouseCommand: PdCommand;
	begin
  nextMouseCommand := mouseCommand;
  mouseCommand := nil;
  if nextMouseCommand <> nil then
  	mouseCommand := nextMouseCommand.trackMouse(
        trackMove, anchorPoint, previousPoint, point, self.didMouseMove(point), rightButtonDown);
  previousPoint := point;
  end;

procedure PdCommandList.mouseUp(point: TPoint);
  var
    nextMouseCommand: PdCommand;
	begin
  nextMouseCommand := mouseCommand;
  mouseCommand := nil;
  if nextMouseCommand <> nil then
    begin
  	nextMouseCommand := nextMouseCommand.trackMouse(
        trackRelease, anchorPoint, previousPoint, point, self.didMouseMove(point), rightButtonDown);
  	if nextMouseCommand <> nil then
    	doCommand(nextMouseCommand);
    end;
  end;

function PdCommandList.didMouseMove(point: TPoint): boolean;
  begin
  result := (abs(point.x - anchorPoint.x) > kMinMoveDistance)
        or (abs(point.y - anchorPoint.y) > kMinMoveDistance);
  end;

function PdCommandList.isUndoEnabled: boolean;
	begin
  result := lastDoneCommandIndex >= 0;
  end;

function PdCommandList.isRedoEnabled: boolean;
	begin
  result := lastDoneCommandIndex < (commands.count - 1);
  end;

function PdCommandList.undoDescription: string;
	begin
  if lastDoneCommandIndex >= 0 then
    begin
  	result := command(lastDoneCommandIndex).description;
    result := limitDescription(result);
    end
  else
    result := '';
  end;

function PdCommandList.redoDescription: string;
	begin
  if lastDoneCommandIndex < (commands.count - 1) then
    begin
  	result := command(lastDoneCommandIndex+1).description;
    result := limitDescription(result);
    end
  else
    result := '';
  end;

procedure PdCommandList.undoLast;
	begin
  if lastDoneCommandIndex >= 0 then
  	begin
  	command(lastDoneCommandIndex).undoCommand;
    dec(lastDoneCommandIndex);
    end;
  end;

procedure PdCommandList.redoLast;
	begin
  if lastDoneCommandIndex < (commands.count - 1) then
  	begin
  	command(lastDoneCommandIndex+1).redoCommand;
    inc(lastDoneCommandIndex);
    end;
  end;

procedure PdCommandList.fillListWithUndoableStrings(aList: TStringList);
  var i: integer;
  begin
  if aList = nil then exit;
  if lastDoneCommandIndex >= 0 then
    for i := lastDoneCommandIndex downto 0 do
      aList.add(capitalize(command(i).description));
  end;

procedure PdCommandList.fillListWithRedoableStrings(aList: TStringList);
  var i: integer;
  begin
  if aList = nil then exit;
  if lastDoneCommandIndex < (commands.count - 1) then
    for i := lastDoneCommandIndex + 1 to commands.count - 1 do
      aList.add(capitalize(command(i).description));
  end;

function PdCommandList.lastCommandDone: PdCommand;
	begin
  result := nil;
  if lastDoneCommandIndex < (commands.count - 1) then
  	result := command(lastDoneCommandIndex+1);
  end;

procedure PdCommandList.removeCommand(aCommand: PdCommand);
	begin
  { assume this command has been undone previously }
  if aCommand.done then
    raise Exception.create('Problem: Command not undone; in PdCommandList.removeCommand.');
  commands.remove(aCommand);
  end;

end.
