unit Uundo;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Buttons, ucommand, updform;

type
  TUndoRedoListForm = class(PdForm)
    OK: TButton;
    cancel: TButton;
    helpButton: TSpeedButton;
    undoListLabel: TLabel;
    redoListLabel: TLabel;
    undoList: TListBox;
    redoList: TListBox;
    procedure FormResize(Sender: TObject);
    procedure OKClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure regulateListSelections(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
  public
    { Public declarations }
    procedure initializeWithCommandList(commandList: PdCommandList);
    function undoToIndex: integer;
    function redoToIndex: integer;
  end;

implementation

{$R *.DFM}

uses umath, udomain, umain;

procedure TUndoRedoListForm.FormCreate(Sender: TObject);
  var tempBoundsRect: TRect;
  begin
  { keep window on screen - left corner of title bar }
  tempBoundsRect := domain.undoRedoListWindowRect;
  with tempBoundsRect do
    if (left <> 0) or (right <> 0) or (top <> 0) or (bottom <> 0) then
      begin
      if left > screen.width - kMinWidthOnScreen then left := screen.width - kMinWidthOnScreen;
      if top > screen.height - kMinHeightOnScreen then top := screen.height - kMinHeightOnScreen;
      self.setBounds(left, top, right, bottom);
      end;
  // make list boxes have horizontal scroll bars
  sendMessage(undoList.handle, LB_SETHORIZONTALEXTENT, 1000, longint(0));
  sendMessage(redoList.handle, LB_SETHORIZONTALEXTENT, 1000, longint(0));
  end;

procedure TUndoRedoListForm.initializeWithCommandList(commandList: PdCommandList);
  var aList: TStringList;
  begin
  aList := TStringList.create;
  try
    commandList.fillListWithUndoableStrings(aList);
    undoList.items.assign(aList);
    aList.clear;
    commandList.fillListWithRedoableStrings(aList);
    redoList.items.assign(aList);
  finally
    aList.free;
  end;
  ok.enabled := (undoList.selCount > 0) or (redoList.selCount > 0);
  end;

function TUndoRedoListForm.undoToIndex: integer;
  var i: integer;
  begin
  result := -1;
  if undoList.items.count > 0 then for i := undoList.items.count - 1 downto 0 do
   if undoList.selected[i] then
     begin
     result := i;
     exit;
     end;
  end;

function TUndoRedoListForm.redoToIndex: integer;
  var i: integer;
  begin
  result := -1;
  if redoList.items.count > 0 then for i := redoList.items.count - 1 downto 0 do
   if redoList.selected[i] then
     begin
     result := i;
     exit;
     end;
  end;

procedure TUndoRedoListForm.regulateListSelections(Sender: TObject);
  var
    i: integer;
    thisListBox, otherListBox: TListBox;
  begin
  if (sender = nil) or (not (sender is TListBox)) then
    raise Exception.create('Problem: Wrong sender in method TUndoRedoListForm.regulateListSelections.');
  thisListBox := sender as TListBox;
  if sender = undoList then otherListBox := redoList else otherListBox := undoList;
  if sender = undoList then ok.caption := 'Un&do' else ok.caption := 'Re&do';
  ok.enabled := (undoList.selCount > 0) or (redoList.selCount > 0);
  with thisListBox do
    begin
    if itemIndex >= 0 then for i := 0 to itemIndex do selected[i] := true;
    if itemIndex + 1 <= items.count - 1 then for i := itemIndex + 1 to items.count - 1 do selected[i] := false;
    end;
  with otherListBox do
    begin
    if items.count > 0 then for i := 0 to items.count - 1 do selected[i] := false;
    itemIndex := -1;
    end;
  end;

procedure TUndoRedoListForm.OKClick(Sender: TObject);
  begin
  modalResult := mrOK;
  end;

procedure TUndoRedoListForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TUndoRedoListForm.FormClose(Sender: TObject; var Action: TCloseAction);
  begin
  domain.undoRedoListWindowRect := rect(left, top, width, height);
  end;

procedure TUndoRedoListForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Using_the_undo/redo_list');
  end;

const kBetweenGap = 4;

procedure TUndoRedoListForm.FormResize(Sender: TObject);
  var listHeight: integer;
  begin
  if Application.terminated then exit;
  OK.left := self.clientWidth - OK.width - kBetweenGap;
  cancel.left := OK.left;
  helpButton.left := OK.left;
  with undoListLabel do setBounds(kBetweenGap, kBetweenGap, width, height);
  listHeight := intMax(0, (self.clientHeight - undoListLabel.height * 2 - kBetweenGap * 5) div 2);
  with undoList do setBounds(kBetweenGap, undoListLabel.top + undoListLabel.height + kBetweenGap,
    OK.left - kBetweenGap * 2, listHeight);
  with redoListLabel do setBounds(kBetweenGap, undoList.top + undoList.height + kBetweenGap, width, height);
  with redoList do setBounds(kBetweenGap, redoListLabel.top + redoListLabel.height + kBetweenGap,
    OK.left - kBetweenGap * 2, listHeight);
  end;

procedure TUndoRedoListForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 220;
    ptMinTrackSize.y := 220;
    end;
  end;

end.
