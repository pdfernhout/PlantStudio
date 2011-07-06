unit ucursor;

interface

uses WinProcs, WinTypes, ExtCtrls, Classes;

const
  crMagMinus = 1;
  crMagPlus = 2;
  crScroll = 3;
  crRotate = 4;
  crDragPlant = 5;
  crAddTriangle = 6;
  crDeleteTriangle = 7;
  crFlipTriangle = 8;
  crDragPoint = 9;
  crDragTdo = 10;
  crPosingSelect = 11;

procedure cursor_initializeWait;
procedure cursor_startWait;
procedure cursor_startWaitIfNotWaiting;
procedure cursor_stopWait;
procedure cursor_loadCustomCursors;

var
  waitState: integer;

implementation

{$R CURSOR32}

uses SysUtils, Controls, Forms;

procedure cursor_initializeWait;
  begin
  waitState := 0;
  end;

procedure cursor_startWait;
  begin
  inc(waitState);
  screen.cursor := crHourglass;
  end;

procedure cursor_startWaitIfNotWaiting;
  begin
	if waitState = 0 then cursor_startWait;
  end;

procedure cursor_stopWait;
  begin
  if waitState > 0 then
    begin
  	dec(waitState);
  	if waitState = 0 then screen.cursor := crDefault;
    end;
  end;

{Note:	You don't need to call the WinAPI function DestroyCursor when you are finished using the custom
cursor; Delphi does this automatically. }
procedure cursor_loadCustomCursors;
	begin
  Screen.Cursors[crMagMinus] := LoadCursor(HInstance, 'MAGMINUS');
  Screen.Cursors[crMagPlus] := LoadCursor(HInstance, 'MAGPLUS');
  Screen.Cursors[crScroll] := LoadCursor(HInstance, 'SCROLL');
  Screen.Cursors[crRotate] := LoadCursor(HInstance, 'ROTATE');
  Screen.Cursors[crDragPlant] := LoadCursor(HInstance, 'DRAGPLANT');
  Screen.Cursors[crAddTriangle] := LoadCursor(HInstance, 'ADDTRIANGLEPOINT');
  Screen.Cursors[crDeleteTriangle] := LoadCursor(HInstance, 'DELETETRIANGLE');
  Screen.Cursors[crFlipTriangle] := LoadCursor(HInstance, 'FLIPTRIANGLE');
  Screen.Cursors[crDragPoint] := LoadCursor(HInstance, 'DRAGPOINT');
  Screen.Cursors[crDragTdo] := LoadCursor(HInstance, 'DRAGTDO');
  Screen.Cursors[crPosingSelect] := LoadCursor(HInstance, 'POSINGSELECT');
	end;

begin
cursor_initializeWait;
cursor_loadCustomCursors;
end.
