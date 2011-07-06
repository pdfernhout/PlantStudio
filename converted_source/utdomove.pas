unit utdomove;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, StdCtrls, Buttons, ExtCtrls, Grids,
  uplantmn, utdo, ucommand, updcom, updform, ucollect;

type
  TTdoMoverForm = class(PdForm)
    leftTdoFileNameEdit: TEdit;
    leftOpenClose: TButton;
    rightTdoFileNameEdit: TEdit;
    rightOpenClose: TButton;
    newFile: TButton;
    transfer: TButton;
    close: TButton;
    previewImage: TImage;
    undo: TButton;
    redo: TButton;
    rename: TButton;
    duplicate: TButton;
    delete: TButton;
    leftTdoFileChangedIndicator: TImage;
    rightTdoFileChangedIndicator: TImage;
    leftTdoList: TDrawGrid;
    rightTdoList: TDrawGrid;
    editTdo: TButton;
    helpButton: TSpeedButton;
    procedure leftOpenCloseClick(Sender: TObject);
    procedure rightOpenCloseClick(Sender: TObject);
    procedure newFileClick(Sender: TObject);
    procedure duplicateClick(Sender: TObject);
    procedure renameClick(Sender: TObject);
    procedure closeClick(Sender: TObject);
    procedure transferClick(Sender: TObject);
    procedure deleteClick(Sender: TObject);
    procedure FormResize(Sender: TObject);
    procedure leftTdoListMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure rightTdoListMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure leftTdoListDblClick(Sender: TObject);
    procedure rightTdoListDblClick(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure undoClick(Sender: TObject);
    procedure redoClick(Sender: TObject);
    procedure FormKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure leftTdoListDragOver(Sender, Source: TObject; X, Y: Integer;
      State: TDragState; var Accept: Boolean);
    procedure leftTdoListEndDrag(Sender, Target: TObject; X, Y: Integer);
    procedure rightTdoListDragOver(Sender, Source: TObject; X,
      Y: Integer; State: TDragState; var Accept: Boolean);
    procedure rightTdoListEndDrag(Sender, Target: TObject; X,
      Y: Integer);
    procedure leftTdoListDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure rightTdoListDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure FormCreate(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure editTdoClick(Sender: TObject);
    procedure previewImageMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure leftTdoListKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure rightTdoListKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure sortListClick(Sender: TObject);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
  public
    { Public declarations }
    leftTdoFileName, rightTdoFileName: string;
    leftList, rightList: TListCollection;
    leftTdoFileChanged, rightTdoFileChanged: boolean;
    lastLeftSingleClickTdoIndex, lastRightSingleClickTdoIndex: integer;
    leftOrRight: smallint;
    commandList: PdCommandList;
    selectedTdos: TList;
    dragItemsY: integer;
    justDoubleClickedOnLeftGrid, justDoubleClickedOnRightGrid: boolean;
    constructor create(AOwner: TComponent); override;
    destructor destroy; override;
    procedure setFileNameForList(newName: string; list: TListCollection);
    function getFileNameForList(list: TListCollection): string;
    function getFileNameForOtherList(list: TListCollection): string;
    function gridForList(list: TListCollection): TDrawGrid;
    procedure setChangedFlagForTdoList(value: boolean; list: TListCollection);
    function listHasChanged(list: TListCollection): boolean;
    procedure updateForNewFile(newFileName: string; list: TListCollection);
    procedure updateButtonsForUndoRedo;
    procedure updateTdoListForList(list: TListCollection);
    function selectedList(thisList: boolean): TListCollection;
    function askToSaveListAndProceed(list: TListCollection): boolean;
    procedure openTdoFileForList(list: TListCollection; fileNameToStart: string);
    procedure newTdoFileForList(list: TListCollection);
    procedure closeTdoFileForList(list: TListCollection);
    procedure listSaveOrSaveAs(list: TListCollection; askForFileName: boolean);
    function haveLeftFile: boolean;
    function haveRightFile: boolean;
    procedure drawPreview(tdo: KfObject3D);
    procedure drawLineInGrid(grid: TDrawGrid; list: TListCollection; index: integer; rect: TRect; state: TGridDrawState);
    procedure clearCommandList;
    procedure doCommand(command: PdCommand);
    procedure deselectAllTdos;
    procedure updateForChangeToSelectedTdos;
    function leftRightString(leftString, rightString: string): string;
    procedure resizePreviewImage;
    function focusedTdo: KfObject3D;
    function focusedTdoIndexInList: smallint;
    procedure selectTdoAtIndex(Shift: TShiftState; index: Integer);
    procedure loadTdosFromFile(list: TListCollection; fileName: string);
    procedure saveTdosToFile(list: TListCollection; fileName: string);
    procedure listKeyDown(var Key: Word; Shift: TShiftState);
    procedure moveUpOrDownWithKey(indexAfterMove: smallint);
    procedure moveSelectedTdosDown;
    procedure moveSelectedTdosUp;
    procedure redrawSelectedGrid;
    end;

  PdTdoMoverRenameCommand = class(PdCommand)
    public
    tdo: KfObject3D;
    oldName, newName: string;
    list: TListCollection;
    listChangedBeforeCommand: boolean;
    constructor createWithTdoNewNameAndList(aTdo: KfObject3D; aNewName: string;
      aList: TListCollection);
	  procedure doCommand; override;
	  procedure undoCommand; override;
    function description: string; override;
    end;

  PdTdoMoverEditCommand = class(PdCommand)
    public
    tdo, oldTdo, newTdo: KfObject3D;
    list: TListCollection;
    listChangedBeforeCommand: boolean;
    constructor createWithTdoNewTdoAndList(aTdo, aNewTdo: KfObject3D; aList: TListCollection);
    destructor destroy; override;
	  procedure doCommand; override;
	  procedure undoCommand; override;
    function description: string; override;
    end;

  PdCommandWithListOfTdos = class(PdCommand)
    public
    tdoList: TList;
    values: TListCollection;
    tdo: KfObject3D; {for temporary use}
    constructor createWithListOfTdos(aList: TList); virtual;
    destructor destroy; override;
    end;

  PdTdoMoverRemoveCommand = class(PdCommandWithListOfTdos){use for cut and delete}
    public
    removedTdos: TList;
    list: TListCollection;
    listChangedBeforeCommand: boolean;
    constructor createWithSelectedTdosAndList(listOfTdos: TList; aList: TListCollection);
    destructor destroy; override;
	  procedure doCommand; override;
	  procedure undoCommand; override;
    function description: string; override;
    end;

  PdTdoMoverTransferCommand = class(PdCommandWithListOfTdos) 
    public
    isTransfer: boolean;
    list: TListCollection;
    listChangedBeforeCommand: boolean;
    constructor createWithSelectedTdosAndList(listOfTdos: TList; aList: TListCollection);
    destructor destroy; override;
	  procedure doCommand; override;
	  procedure undoCommand; override;
    function description: string; override;
    end;

  PdTdoMoverDuplicateCommand = class(PdCommandWithListOfTdos)
    public
    newTdos: TList;
    list: TListCollection;
    listChangedBeforeCommand: boolean;
    constructor createWithSelectedTdosAndList(listOfTdos: TList; aList: TListCollection);
    destructor destroy; override;
	  procedure doCommand; override;
	  procedure undoCommand; override;
    procedure redoCommand; override;
    function description: string; override;
    end;

implementation

{$R *.DFM}

uses ClipBrd,
  udomain, umain, ucursor, usupport, umath, uturtle, utdoedit;

const
  kLeft = 0; kRight = 1;
  kNewTdoFileName = 'untitled.tdo';
  kThisList = true; kOtherList = false;

var TdoMoverForm: TTdoMoverForm;

{ -------------------------------------------------------------------------------------------- *creation/destruction }
constructor TTdoMoverForm.create(AOwner: TComponent);
  begin
  inherited create(AOwner);
  TdoMoverForm := self;
  leftList := TListCollection.create;
  rightList := TListCollection.create;
  commandList := PdCommandList.create;
  selectedTdos := TList.create;
  commandList.setNewUndoLimit(domain.options.undoLimit);
  commandList.setNewObjectUndoLimit(domain.options.undoLimitOfPlants);
  self.updateButtonsForUndoRedo;
  { load current tdo file into left side to start }
  if length(domain.defaultTdoLibraryFileName) > 0 then
    self.openTdoFileForList(leftList, domain.defaultTdoLibraryFileName)
  else
    self.closeTdoFileForList(leftList);
  { right side is empty to start }
  self.closeTdoFileForList(rightList);
  end;

procedure TTdoMoverForm.FormCreate(Sender: TObject);
  begin
  leftTdoList.dragCursor := crDragTdo;
  rightTdoList.dragCursor := crDragTdo;
  end;

destructor TTdoMoverForm.destroy;
  begin
  leftList.free;
  leftList := nil;
  rightList.free;
  rightList := nil;
  selectedTdos.free;
  selectedTdos := nil;
  commandList.free;
  commandList := nil;
  inherited destroy;
  end;

procedure TTdoMoverForm.FormClose(Sender: TObject; var Action: TCloseAction);
  begin
  if modalResult = mrOk then exit;
  { same as exit, but can't call exit because we have to set the action flag }
  action := caNone;
  if not self.askToSaveListAndProceed(leftList) then exit;
  if not self.askToSaveListAndProceed(rightList) then exit;
  action := caFree;
  end;

procedure TTdoMoverForm.FormKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  case key of
    VK_DELETE: self.deleteClick(self);
    end;
  if not (ssCtrl in shift) then exit;
  case char(key) of
    'Z', 'z':
      begin
      if ssShift in shift then
        self.redoClick(self)
      else
        self.undoClick(self);
      key := 0;
      end;
    end;
  end;

{ ----------------------------------------------------------------------------------------- *buttons }
procedure TTdoMoverForm.undoClick(Sender: TObject);
  begin
  commandList.undoLast;
  self.updateButtonsForUndoRedo;
  self.updateForChangeToSelectedTdos;
  end;

procedure TTdoMoverForm.redoClick(Sender: TObject);
  begin
  commandList.redoLast;
  self.updateButtonsForUndoRedo;
  self.updateForChangeToSelectedTdos;
  end;

procedure TTdoMoverForm.closeClick(Sender: TObject);
  begin
  if not self.askToSaveListAndProceed(leftList) then exit;
  if not self.askToSaveListAndProceed(rightList) then exit;
  modalResult := mrOk; { cannot cancel }
  end;

procedure TTdoMoverForm.leftOpenCloseClick(Sender: TObject);
  begin
  if haveLeftFile then {file open}
    self.closeTdoFileForList(leftList)
  else   {no file}
    self.openTdoFileForList(leftList, '')
  end;

procedure TTdoMoverForm.rightOpenCloseClick(Sender: TObject);
  begin
  if haveRightFile then {file open}
    self.closeTdoFileForList(rightList)
  else   {no file}
    self.openTdoFileForList(rightList, '')
  end;

procedure TTdoMoverForm.newFileClick(Sender: TObject);
  begin
  self.newTdoFileForList(rightList);
  end;

procedure TTdoMoverForm.transferClick(Sender: TObject);
  var
    list, otherList: TListCollection;
    newCommand: PdCommand;
    newTdos: TList;
    tdo, newTdo: KfObject3D;
    i: smallint;
  begin
  list := self.selectedList(kThisList);
  otherList := self.selectedList(kOtherList);
  if (list = nil) or (otherList = nil) or (selectedTdos.count <= 0) then exit;
  if selectedTdos.count > 0 then
    begin
    newTdos := TList.create; {command will free}
    for i := 0 to selectedTdos.count - 1 do
      begin
      tdo := KfObject3D(selectedTdos.items[i]);
      newTdo := KfObject3D.create;
      tdo.copyTo(newTdo);
      newTdos.add(newTdo);
      end;
    newCommand := PdTdoMoverTransferCommand.createWithSelectedTdosAndList(newTdos, otherList);
    self.doCommand(newCommand);
    newTdos.free; {command has its own list, so we need to free this one}
    end;
	end;

procedure TTdoMoverForm.duplicateClick(Sender: TObject);
  var
    list: TListCollection;
    newCommand: PdCommand;
  begin
  list := self.selectedList(kThisList);
  if (list = nil) or (selectedTdos.count <= 0) then exit;
  newCommand := PdTdoMoverDuplicateCommand.createWithSelectedTdosAndList(selectedTdos, list);
  self.doCommand(newCommand);
	end;

procedure TTdoMoverForm.renameClick(Sender: TObject);
  var
    tdo: KfObject3D;
    list: TListCollection;
    newName: ansistring;
    newCommand: PdCommand;
	begin
  { can only rename one tdo at a time }
  list := self.selectedList(kThisList);
  tdo := self.focusedTdo;
  if (tdo = nil) or (list = nil) then exit;
  newName := tdo.getName;
  if not inputQuery('Enter new name', 'Type a new name for ' + newName + '.', newName) then exit;
  newCommand := PdTdoMoverRenameCommand.createWithTdoNewNameAndList(tdo, newName, list);
  self.doCommand(newCommand);
	end;

procedure TTdoMoverForm.deleteClick(Sender: TObject);
  var
    list: TListCollection;
    newCommand: PdCommand;
  begin
  list := self.selectedList(kThisList);
  if (list = nil) or (selectedTdos.count <= 0) then exit;
  newCommand := PdTdoMoverRemoveCommand.createWithSelectedTdosAndList(selectedTdos, list);
  self.doCommand(newCommand);
	end;

procedure TTdoMoverForm.editTdoClick(Sender: TObject);
  var
    tdoEditorForm: TTdoEditorForm;
    response: integer;
    newCommand: PdCommand;
    tempTdo: KfObject3D;
  begin
  if self.focusedTdo = nil then exit;
  tdoEditorForm := TTdoEditorForm.create(self);
  if tdoEditorForm = nil then
    raise Exception.create('Problem: Could not create 3D object editor window.');
  tempTdo := KfObject3D.create;
  try
    tempTdo.copyFrom(self.focusedTdo);
    tdoEditorForm.initializeWithTdo(tempTdo);
    response := tdoEditorForm.showModal;
    if response = mrOK then
      begin
      tempTdo.copyFrom(tdoEditorForm.tdo); // v1.6b1
      newCommand := PdTdoMoverEditCommand.createWithTdoNewTdoAndList(self.focusedTdo,
        tempTdo, self.selectedList(kThisList));
      self.doCommand(newCommand);
      end;
   finally
    tdoEditorForm.free;
    tdoEditorForm := nil;
    tempTdo.free;
    tempTdo := nil;
  end;
  end;

procedure TTdoMoverForm.sortListClick(Sender: TObject);
  begin
  end;

{ -------------------------------------------------------------------------------------- *list box actions }
procedure TTdoMoverForm.leftTdoListDrawCell(Sender: TObject; Col,
  Row: Integer; Rect: TRect; State: TGridDrawState);
  begin
  self.drawLineInGrid(leftTdoList, leftList, row, rect, state);
  end;

procedure TTdoMoverForm.rightTdoListDrawCell(Sender: TObject; Col,
  Row: Integer; Rect: TRect; State: TGridDrawState);
  begin
  self.drawLineInGrid(rightTdoList, rightList, row, rect, state);
  end;

procedure TTdoMoverForm.drawLineInGrid(grid: TDrawGrid; list: TListCollection;
    index: integer; rect: TRect; state: TGridDrawState);
  var
	  tdo: KfObject3D;
    selected: boolean;
    cText: array[0..255] of Char;
  begin
  if Application.terminated then exit;
  grid.canvas.brush.color := grid.color;
  grid.canvas.fillRect(rect);
  if (list.count <= 0) or (index < 0) or (index > list.count - 1) then exit;
  { set up tdo pointer }
  tdo := KfObject3D(list.items[index]);
  if tdo = nil then exit;
  selected := (list = self.selectedList(kThisList)) and (selectedTdos.indexOf(tdo) >= 0);
  with grid.canvas do
    begin
    font := grid.font;
    if selected then
      begin
      brush.color := clHighlight;
      font.color := clHighlightText;
      end
    else
      begin
      brush.color := grid.color;
      font.color := clBtnText;
      end;
    fillRect(rect);
    strPCopy(cText, tdo.getName);
    rect.left := rect.left + 2; { margin for text }
    winprocs.drawText(handle, cText, strLen(cText), rect, DT_LEFT);
    if tdo = self.focusedTdo then
      begin
      rect.left := rect.left - 2; { put back }
      drawFocusRect(rect);
      end;
    end;
  end;

// left list mouse handling
procedure TTdoMoverForm.leftTdoListMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    col, row: integer;
	begin
  if justDoubleClickedOnLeftGrid then
    begin
    justDoubleClickedOnLeftGrid := false;
    exit;
    end
  else
    justDoubleClickedOnLeftGrid := false;
  if leftList.count > 0 then
    begin
    if leftOrRight = kRight then
      begin
      selectedTdos.clear;
      lastRightSingleClickTdoIndex := -1;
      rightTdoList.invalidate;
      end;
    leftOrRight := kLeft;
    leftTdoList.mouseToCell(x, y, col, row);
    self.selectTdoAtIndex(shift, row);
    leftTdoList.invalidate;
    self.updateForChangeToSelectedTdos;
    leftTdoList.beginDrag(false);
    end;
  end;

procedure TTdoMoverForm.leftTdoListDragOver(Sender, Source: TObject; X,
  Y: Integer; State: TDragState; var Accept: Boolean);
  begin
  accept := (source <> nil) and (sender <> nil);
  if source = rightTdoList then
    accept := accept and haveLeftFile
  else
    accept := accept and (source = sender);
  end;

procedure TTdoMoverForm.leftTdoListEndDrag(Sender, Target: TObject; X, Y: Integer);
  begin
  if (target = rightTdoList) then
    self.transferClick(self);
  end;

procedure TTdoMoverForm.leftTdoListDblClick(Sender: TObject);
  begin
  self.renameClick(self);
  leftTdoList.endDrag(false);
  justDoubleClickedOnLeftGrid := true;
  end;

// right list mouse handling
procedure TTdoMoverForm.rightTdoListMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    col, row: integer;
	begin
  if justDoubleClickedOnRightGrid then
    begin
    justDoubleClickedOnRightGrid := false;
    exit;
    end
  else
    justDoubleClickedOnRightGrid := false;
  if rightList.count > 0 then
    begin
    if leftOrRight = kLeft then
      begin
      selectedTdos.clear;
      lastLeftSingleClickTdoIndex := -1;
      leftTdoList.invalidate;
      end;
    leftOrRight := kRight;
    rightTdoList.mouseToCell(x, y, col, row);
    self.selectTdoAtIndex(shift, row);
    rightTdoList.invalidate;
    self.updateForChangeToSelectedTdos;
    rightTdoList.beginDrag(false);
    end;
  end;

procedure TTdoMoverForm.rightTdoListDragOver(Sender, Source: TObject; X,
  Y: Integer; State: TDragState; var Accept: Boolean);
  begin
  accept := (source <> nil) and (sender <> nil);
  if source = leftTdoList then
    accept := accept and haveRightFile
  else
    accept := accept and (source = sender);
  end;

procedure TTdoMoverForm.rightTdoListEndDrag(Sender, Target: TObject; X, Y: Integer);
  begin
  if (target = leftTdoList) then
    self.transferClick(self);
  end;

procedure TTdoMoverForm.rightTdoListDblClick(Sender: TObject);
  begin
  self.renameClick(self);
  rightTdoList.endDrag(false);
  justDoubleClickedOnRightGrid := true;
  end;

procedure TTdoMoverForm.selectTdoAtIndex(Shift: TShiftState; index: Integer);
  var
   i: smallint;
   tdo: KfObject3D;
   list: TListCollection;
   lastSingleClickTdoIndex, lastRow: integer;
   grid: TDrawGrid;
	begin
  if application.terminated then exit;
  list := self.selectedList(kThisList);
  if list = nil then exit;
  if (index < 0) then
    begin
    selectedTdos.clear;
    exit;
    end;
  tdo := KfObject3D(list.items[index]);
  if tdo = nil then exit;
  if (ssCtrl in shift) then
    begin
    if selectedTdos.indexOf(tdo) >= 0 then
      selectedTdos.remove(tdo)
    else
      selectedTdos.add(tdo);
    end
  else if (ssShift in shift) then
    begin
    if leftOrRight = kLeft then
      lastSingleClickTdoIndex := lastLeftSingleClickTdoIndex
    else
      lastSingleClickTdoIndex := lastRightSingleClickTdoIndex;
    if (lastSingleClickTdoIndex >= 0) and (lastSingleClickTdoIndex <= list.count - 1)
        and (lastSingleClickTdoIndex <> index) then
      begin
      if lastSingleClickTdoIndex < index then
        begin
        for i := lastSingleClickTdoIndex to index do
          if selectedTdos.indexOf(list.items[i]) < 0 then
            selectedTdos.add(list.items[i]);
        end
      else if lastSingleClickTdoIndex > index then
        begin
        for i := lastSingleClickTdoIndex downto index do
          if selectedTdos.indexOf(list.items[i]) < 0 then
            selectedTdos.add(list.items[i]);
        end;
      end;
    end
  else // just a click
    begin
    if selectedTdos.indexOf(tdo) <= 0 then
      begin
      selectedTdos.clear;
      selectedTdos.add(tdo);
      if leftOrRight = kLeft then
        lastLeftSingleClickTdoIndex := index
      else
        lastRightSingleClickTdoIndex := index;
      end;
      grid := gridForList(list);
      if grid = nil then exit;
      with grid do
        begin
        lastRow := topRow + visibleRowCount - 1;
        if index > lastRow then
          topRow := topRow + (index - lastRow);
        if index < topRow then
          topRow := index;
        end;
    end;
	end;

procedure TTdoMoverForm.leftTdoListKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  self.listKeyDown(key, shift);
  end;

procedure TTdoMoverForm.rightTdoListKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  self.listKeyDown(key, shift);
  end;

procedure TTdoMoverForm.listKeyDown(var Key: Word; Shift: TShiftState);
  begin
  case key of
    vk_down, vk_right:
      if (ssShift in shift) then
        begin
        key := 0; {swallow key}
        self.moveSelectedTdosDown;
        end
      else
        begin
        key := 0;
        self.moveUpOrDownWithKey(self.focusedTdoIndexInList + 1);
        end;
    vk_up, vk_left:
      if (ssShift in shift) then
        begin
        key := 0; {swallow key}
        self.moveSelectedTdosUp;
        end
     else
        begin
        key := 0;
        self.moveUpOrDownWithKey(self.focusedTdoIndexInList - 1);
        end;
    vk_return:
        begin
        key := 0;
        self.renameClick(self);
        end;
    end;
  end;

procedure TTdoMoverForm.moveUpOrDownWithKey(indexAfterMove: smallint);
  var
    list: TListCollection;
  begin
  list := self.selectedList(kThisList);
  if list = nil then exit;
  { loop around }
  if indexAfterMove > list.count - 1 then
    indexAfterMove := 0;
  if indexAfterMove < 0 then
    indexAfterMove := list.count - 1;
  if (indexAfterMove >= 0) and (indexAfterMove <= list.count - 1) then
    begin
    self.deselectAllTdos;
    self.selectTdoAtIndex([]{no shift}, indexAfterMove);
    self.drawPreview(focusedTdo);
    end;
  end;

procedure TTdoMoverForm.moveSelectedTdosDown;
  var
    list: TListCollection;
    i: smallint;
    tdo: KfObject3D;
  begin
  if selectedTdos.count <= 0 then exit;
  list := self.selectedList(kThisList);
  if list = nil then exit;
  if list.count > 1 then
    begin
    i := list.count - 2;  { start at next to last one because you can't move last one down any more }
    while i >= 0 do
      begin
      tdo := KfObject3D(list.items[i]);
      if selectedTdos.indexOf(tdo) >= 0 then
        list.move(i, i + 1);
      dec(i);
      end;
    end;
  self.redrawSelectedGrid;
  // reordering makes change flag true
  self.setChangedFlagForTdoList(true, selectedList(kThisList));
  end;

procedure TTdoMoverForm.moveSelectedTdosUp;
  var
    list: TListCollection;
    i: smallint;
    tdo: KfObject3D;
  begin
  if selectedTdos.count <= 0 then exit;
  list := self.selectedList(kThisList);
  if list = nil then exit;
  if list.count > 1 then
    begin
    i := 1;  { start at 1 because you can't move first one up any more }
    while i <= list.count - 1 do
      begin
      tdo := KfObject3D(list.items[i]);
      if selectedTdos.indexOf(tdo) >= 0 then
        list.move(i, i - 1);
      inc(i);
      end;
    end;
  self.redrawSelectedGrid;
  // reordering makes change flag true
  self.setChangedFlagForTdoList(true, selectedList(kThisList));
  end;

procedure TTdoMoverForm.redrawSelectedGrid;
  begin
  if leftOrRight = kLeft then
    leftTdoList.invalidate
  else
    rightTdoList.invalidate;
  end;

{ -------------------------------------------------------------------------------------------- *updating }
procedure TTdoMoverForm.updateForNewFile(newFileName: string; list: TListCollection);
  begin
  self.clearCommandList;
  self.setFileNameForList(newFileName, list);
  self.updateTdoListForList(list);
  self.setChangedFlagForTdoList(false, list);
  self.deselectAllTdos;
  if newFileName <> '' then
    begin
    if list = leftList then
      leftOrRight := kLeft
    else
      leftOrRight := kRight;
    end;
  self.updateForChangeToSelectedTdos;
  end;

procedure TTdoMoverForm.deselectAllTdos;
  begin
  self.selectedTdos.clear;
  leftTdoList.invalidate;
  rightTdoList.invalidate;
  end;

function TTdoMoverForm.leftRightString(leftString, rightString: string): string;
  begin
  if leftOrRight = kLeft then
   result := leftString
  else
   result := rightString;
  end;

procedure TTdoMoverForm.updateForChangeToSelectedTdos;
  var
    atLeastOneTdoSelected, atLeastOneFile: boolean;
  begin
  leftTdoList.invalidate;
  rightTdoList.invalidate;
  if leftOrRight = kLeft then
    begin
    if haveLeftFile then
      leftOpenClose.caption := '&Close'
    else
      leftOpenClose.caption := '&Open...';
    leftTdoFileNameEdit.color := clAqua;
    leftTdoFileNameEdit.refresh;
    rightTdoFileNameEdit.color := clBtnFace;
    rightTdoFileNameEdit.refresh;
    self.drawPreview(focusedTdo);
    end
  else
    begin
    if haveRightFile then
      rightOpenClose.caption := '&Close'
    else
      rightOpenClose.caption := '&Open...';
    leftTdoFileNameEdit.color := clBtnFace;
    leftTdoFileNameEdit.refresh;
    rightTdoFileNameEdit.color := clAqua;
    rightTdoFileNameEdit.refresh;
    self.drawPreview(focusedTdo);
    end;
  atLeastOneFile := haveLeftFile or haveRightFile;
  atLeastOneTdoSelected := (selectedTdos.count > 0);
  transfer.enabled := haveLeftFile and haveRightFile and atLeastOneTdoSelected;
  transfer.caption := leftRightString('&Transfer >>', '<< &Transfer');
  duplicate.enabled := atLeastOneFile and atLeastOneTdoSelected;
  delete.enabled := atLeastOneFile and atLeastOneTdoSelected;
  rename.enabled := atLeastOneFile and atLeastOneTdoSelected;
  end;

procedure TTdoMoverForm.updateButtonsForUndoRedo;
	begin
  if commandList.isUndoEnabled then
  	begin
    undo.enabled := true;
    undo.caption := 'Undo ' + commandList.undoDescription;
    end
  else
  	begin
    undo.enabled := false;
    undo.caption := 'Can''t undo';
    end;
  if commandList.isRedoEnabled then
  	begin
    redo.enabled := true;
    redo.caption := 'Redo ' + CommandList.redoDescription;
    end
  else
  	begin
    redo.enabled := false;
    redo.caption := 'Can''t redo';
    end;
  end;

procedure TTdoMoverForm.updateTdoListForList(list: TListCollection);
  var
    grid: TDrawGrid;
  begin
  grid := gridForList(list);
  if grid = nil then exit;
  grid.rowCount := list.count;
  grid.invalidate;
  end;

procedure TTdoMoverForm.drawPreview(tdo: KfObject3D);
  var
    turtle: KfTurtle;
    xScale, yScale: single;
    tdoBoundsRect: TRect;
    currentPosition: TPoint;
    currentScale: single;
  begin
  with previewImage.picture.bitmap.canvas do
    begin
    brush.color := clWindow;
    fillRect(Rect(0, 0, previewImage.width, previewImage.height));
    brush.style := bsClear;
    if tdo <> nil then
      begin
      turtle := KfTurtle.defaultStartUsing;
      try
        currentScale := 100.0;
        currentPosition := Point(previewImage.width div 2, previewImage.height - previewImage.height div 10);
        turtle.drawingSurface.pane := previewImage.picture.bitmap.canvas;
        turtle.setDrawOptionsForDrawingTdoOnly;
        turtle.drawOptions.draw3DObjects := false;
        // draw first to get new scale
        turtle.reset; { must be after pane and draw options set }
        turtle.xyz(currentPosition.x, currentPosition.y, 0);
        turtle.drawingSurface.recordingStart;
        tdo.draw(turtle, currentScale, '', '', 0, 0);
        turtle.drawingSurface.recordingStop;
        turtle.drawingSurface.recordingDraw;
        turtle.drawingSurface.clearTriangles;
        // calculate new scale to fit
        tdoBoundsRect := turtle.boundsRect;
        xScale := safedivExcept(0.95 * currentScale * previewImage.width, rWidth(tdoBoundsRect), 0.1);
        yScale := safedivExcept(0.95 * currentScale * previewImage.height, rHeight(tdoBoundsRect), 0.1);
        currentScale := min(xScale, yScale);
        currentPosition := tdo.bestPointForDrawingAtScale(turtle, Point(0, 0),
            Point(previewImage.width, previewImage.height), currentScale);
        // draw second time for real
        turtle.drawOptions.draw3DObjects := true;
        turtle.reset; { must be after pane and draw options set }
        turtle.xyz(currentPosition.x, currentPosition.y, 0);
        turtle.drawingSurface.recordingStart;
        tdo.draw(turtle, currentScale, '', '', 0, 0);
        turtle.drawingSurface.recordingStop;
        turtle.drawingSurface.recordingDraw;
        turtle.drawingSurface.clearTriangles;
      finally
        KfTurtle.defaultStopUsing;
      end;
      end;
    brush.style := bsClear;
    pen.color := clBtnText;
    pen.style := psSolid;
    rectangle(0, 0, previewImage.width, previewImage.height);
    end;
  end;

procedure TTdoMoverForm.previewImageMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  end;

{ ------------------------------------------------------------------------------------------ *selecting }
function TTdoMoverForm.focusedTdo: KfObject3D;
  begin
  result := nil;
  if selectedTdos.count > 0 then
    result := KfObject3D(selectedTdos.items[0]);
  end;

function TTdoMoverForm.focusedTdoIndexInList: smallint;
  var
    list: TListCollection;
  begin
  result := -1;
  list := selectedList(kThisList);
  if list = nil then exit;
  if selectedTdos.count > 0 then
    result := list.indexOf(selectedTdos.items[0]);
  end;

function TTdoMoverForm.haveLeftFile: boolean;
  begin
  result := length(leftTdoFileName) <> 0;
  end;

function TTdoMoverForm.haveRightFile: boolean;
  begin
  result := length(rightTdoFileName) <> 0;
  end;

function TTdoMoverForm.selectedList(thisList: boolean): TListCollection;
  begin
  result := nil;
  if leftOrRight = kLeft then
    begin
    if thisList then
      result := leftList
    else
      result := rightList;
    end
  else
    begin
    if thisList then
      result := rightList
    else
      result := leftList;
    end;
  end;

function TTdoMoverForm.getFileNameForList(list: TListCollection): string;
  begin
  if list = leftList then
    result := leftTdoFileName
  else
    result := rightTdoFileName;
  end;

function TTdoMoverForm.getFileNameForOtherList(list: TListCollection): string;
  begin
  if list = rightList then
    result := leftTdoFileName
  else
    result := rightTdoFileName;
  end;

procedure TTdoMoverForm.setFileNameForList(newName: string; list: TListCollection);
  begin
  if list = leftList then
    begin
    leftTdoFileName := newName;
    leftTdoFileNameEdit.text := newName;
    leftTdoFileNameEdit.selStart := length(newName);
    end
  else
    begin
    rightTdoFileName := newName;
    rightTdoFileNameEdit.text := newName;
    rightTdoFileNameEdit.selStart := length(newName);
    end;
  end;

function TTdoMoverForm.gridForList(list: TListCollection): TDrawGrid;
  begin
  result := nil;
  if list = leftList then
    result := leftTdoList
  else if list = rightList then
    result := rightTdoList;
  end;

function TTdoMoverForm.listHasChanged(list: TListCollection): boolean;
  begin
  if list = leftList then
    result := leftTdoFileChanged
  else
    result := rightTdoFileChanged;
  end;

procedure TTdoMoverForm.setChangedFlagForTdoList(value: boolean; list: TListCollection);
  begin
  if list = leftList then
    begin
    leftTdoFileChanged := value;
    if leftTdoFileChanged then
      leftTdoFileChangedIndicator.picture := MainForm.fileChangedImage.picture
    else
      leftTdoFileChangedIndicator.picture := MainForm.fileNotChangedImage.picture;
    end
  else
    begin
    rightTdoFileChanged := value;
    if rightTdoFileChanged then
      rightTdoFileChangedIndicator.picture := MainForm.fileChangedImage.picture
    else
      rightTdoFileChangedIndicator.picture := MainForm.fileNotChangedImage.picture;
    end;
  end;

{ ------------------------------------------------------------------------ *opening, closing and saving }
procedure TTdoMoverForm.openTdoFileForList(list: TListCollection; fileNameToStart: string);
  var
    fileNameWithPath: string;
  begin
  if not self.askToSaveListAndProceed(list) then exit;
  if fileNameToStart = '' then
    fileNameWithPath := getFileOpenInfo(kFileTypeTdo, kNoSuggestedFile, 'Choose a tdo file')
  else
    fileNameWithPath := fileNameToStart;
  if fileNameWithPath = '' then
    self.updateForNewFile(fileNameWithPath, list)
  else
  	begin
  	if fileNameWithPath = self.getFileNameForOtherList(list) then
    	begin
      showMessage('The file you chose is already open on the other side.');
    	exit;
    	end;
    try
      cursor_startWait;
      if fileExists(fileNameWithPath) then
        self.loadTdosFromFile(list, fileNameWithPath)
      else
        self.newTdoFileForList(list);
      // PDF PORT -- added semicolon
      self.updateForNewFile(fileNameWithPath, list);
    finally
      cursor_stopWait;
    end;
    end;
	end;

procedure TTdoMoverForm.closeTdoFileForList(list: TListCollection);
  begin
  if not self.askToSaveListAndProceed(list) then exit;
  list.clear;
  self.updateForNewFile('', list);
  end;

procedure TTdoMoverForm.newTdoFileForList(list: TListCollection);
  begin
  if not self.askToSaveListAndProceed(list) then exit;
  list.clear;
  self.updateForNewFile(kNewTdoFileName, list);
  end;

procedure TTdoMoverForm.loadTdosFromFile(list: TListCollection; fileName: string);
  var
    newTdo: KfObject3D;
    inputFile: TextFile;
  begin
  if list = nil then exit;
  list.clear;
  if fileName = '' then exit;
  if not fileExists(fileName) then exit;
  assignFile(inputFile, fileName);
  try
    setDecimalSeparator; // v1.5
    reset(inputFile);
    while not eof(inputFile) do
      begin
      newTdo := KfObject3D.create;
      newTdo.readFromFileStream(inputFile, kInTdoLibrary);
      list.add(newTdo);
      end;
  finally
    closeFile(inputFile);
  end;
  end;

procedure TTdoMoverForm.saveTdosToFile(list: TListCollection; fileName: string);
  var
    outputFile: TextFile;
    i: smallint;
    tdo: KfObject3D;
  begin
  if list = nil then exit;
  // assume caller has already verified file name
  assignFile(outputFile, fileName);
  try
    setDecimalSeparator; // v1.5
    rewrite(outputFile);
    if list.count > 0 then for i := 0 to list.count - 1 do
      begin
      tdo := TObject(list.items[i]) as KfObject3D;
      if tdo = nil then continue;
      tdo.writeToFileStream(outputFile, kInTdoLibrary);
      end;
  finally
    closeFile(outputFile);
  end;
  end;

procedure TTdoMoverForm.listSaveOrSaveAs(list: TListCollection; askForFileName: boolean);
  var
    fileInfo: SaveFileNamesStructure;
    fileName: string;
    askForFileNameConsideringUntitled: boolean;
  begin
  fileName := self.getFileNameForList(list);
  if fileName = kNewTdoFileName then
    askForFileNameConsideringUntitled := true
  else
    askForFileNameConsideringUntitled := askForFileName;
  if not getFileSaveInfo(kFileTypeTdo, askForFileNameConsideringUntitled, fileName, fileInfo) then exit;
  try
    cursor_startWait;
    self.saveTdosToFile(list, fileInfo.tempFile);
    fileInfo.writingWasSuccessful := true;
  finally
    cursor_stopWait;
    cleanUpAfterFileSave(fileInfo);
    self.updateForNewFile(kNewTdoFileName, list);
  end;
  end;

function TTdoMoverForm.askToSaveListAndProceed(list: TListCollection): boolean;
  { returns false if user cancelled action }
  var
    response: word;
    prompt: string;
  begin
  result := true;
  if not self.listHasChanged(list) then exit;
  prompt := 'Save changes to ' + extractFileName(self.getFileNameForList(list)) + '?';
  response := messageDlg(prompt, mtConfirmation, mbYesNoCancel, 0);
  case response of
    mrYes: self.listSaveOrSaveAs(list, kDontAskForFileName);
    mrNo: result := true;
    mrCancel: result := false;
    end;
  end;

{ ------------------------------------------------------------------------------------------ *resizing }
const kBetweenGap = 4;

procedure TTdoMoverForm.FormResize(Sender: TObject);
  var
    midWidth, listBoxWidth, listBoxTop, openCloseTop: smallint;
  begin
  if Application.terminated then exit;
  if leftList = nil then exit;
  if rightList = nil then exit;
  if selectedTdos = nil then exit;
  midWidth := self.clientWidth div 2;
  listBoxWidth := leftTdoList.width; //same as right
  listBoxTop := kBetweenGap + leftTdoFileNameEdit.height + kBetweenGap + leftOpenClose.height + kBetweenGap;
  { list boxes }
  with leftTdoList do setBounds(kBetweenGap, listBoxTop, listBoxWidth,
      intMax(0, self.clientHeight - listBoxTop - kBetweenGap));
  leftTdoList.defaultColWidth := leftTdoList.clientWidth;
  with rightTdoList do setBounds(intMax(0, self.clientWidth - listBoxWidth - kBetweenGap), listBoxTop,
      listBoxWidth, intMax(0, self.clientHeight - listBoxTop - kBetweenGap));
  rightTdoList.defaultColWidth := rightTdoList.clientWidth;
  { edits and buttons at top }
  with leftTdoFileNameEdit do setBounds(kBetweenGap, kBetweenGap, listBoxWidth - kBetweenGap * 2, height);
  with leftTdoFileChangedIndicator do setBounds(
      kBetweenGap, leftTdoFileNameEdit.top + leftTdoFileNameEdit.height + kBetweenGap, width, height);
  with rightTdoFileNameEdit do setBounds(rightTdoList.left, kBetweenGap, listBoxWidth- kBetweenGap * 2, height);
  with rightTdoFileChangedIndicator do setBounds(
      rightTdoList.left, rightTdoFileNameEdit.top + rightTdoFileNameEdit.height + kBetweenGap, width, height);
  openCloseTop := leftTdoFileNameEdit.top + leftTdoFileNameEdit.height + kBetweenGap;
  with leftOpenClose do setBounds(
    leftTdoFileChangedIndicator.left + leftTdoFileChangedIndicator.width + kBetweenGap, openCloseTop, width, height);
  with rightOpenClose do setBounds(
    rightTdoFileChangedIndicator.left + rightTdoFileChangedIndicator.width + kBetweenGap, openCloseTop, width, height);
  with newFile do setBounds(rightOpenClose.left + rightOpenClose.width + kBetweenGap, openCloseTop, width, height);
  { buttons in middle }
  with close do setBounds(midWidth - width div 2, intMax(0, self.clientHeight - height - kBetweenGap), width, height);
  with helpButton do setBounds(close.left, intMax(0, close.top - height - kBetweenGap), width, height);
  with editTdo do setBounds(close.left, intMax(0, helpButton.top - height - kBetweenGap), width, height);
  with redo do setBounds(close.left, intMax(0, editTdo.top - height - kBetweenGap), width, height);
  with undo do setBounds(close.left, intMax(0, redo.top - height - kBetweenGap), width, height);
  with rename do setBounds(close.left, intMax(0, undo.top - height - kBetweenGap), width, height);
  with delete do setBounds(close.left, intMax(0, rename.top - height - kBetweenGap), width, height);
  with duplicate do setBounds(close.left, intMax(0, delete.top - height - kBetweenGap), width, height);
  with transfer do setBounds(close.left, intMax(0, duplicate.top - height - kBetweenGap), width, height);
  with previewImage do setBounds(listBoxWidth + kBetweenGap * 2, kBetweenGap,
    intMax(0, self.clientWidth - listBoxWidth * 2 - kBetweenGap * 4), transfer.top - kBetweenGap * 2);
  self.resizePreviewImage;
  end;

procedure TTdoMoverForm.resizePreviewImage;
  begin
  with previewImage do
    begin
    try
      picture.bitmap.height := height;
      picture.bitmap.width := width;
    except
      picture.bitmap.height := 1;
      picture.bitmap.width := 1;
    end;
    end;
  self.drawPreview(focusedTdo);
  end;

procedure TTdoMoverForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 400;
    ptMinTrackSize.y := 315;
    end;
  end;

{ ----------------------------------------------------------------------------------------- command list }
procedure TTdoMoverForm.clearCommandList;
  begin
  commandList.free;
  commandList := nil;
  commandList := PdCommandList.create;
  self.updateButtonsForUndoRedo;
  end;

procedure TTdoMoverForm.doCommand(command: PdCommand);
	begin
  commandList.doCommand(command);
  self.updateButtonsForUndoRedo;
  self.updateForChangeToSelectedTdos;
  end;

{ ------------------------------------------------------------------------------ *commands }
{ ------------------------------------------------------------------- PdTdoMoverRenameCommand }
constructor PdTdoMoverRenameCommand.createWithTdoNewNameAndList(aTdo: KfObject3D; aNewName: string;
    aList: TListCollection);
  begin
  inherited create;
  commandChangesPlantFile := false;
  tdo := aTdo;
  oldName := tdo.getName;
  newName := aNewName;
  list := aList;
  listChangedBeforeCommand := TdoMoverForm.listHasChanged(list);
  end;

procedure PdTdoMoverRenameCommand.doCommand;
  begin
  inherited doCommand; {not redo}
  tdo.setName(newName);
  TdoMoverForm.setChangedFlagForTdoList(true, list);
  end;

procedure PdTdoMoverRenameCommand.undoCommand;
  begin
  inherited undoCommand;
  tdo.setName(oldName);
  TdoMoverForm.setChangedFlagForTdoList(listChangedBeforeCommand, list);
  end;

function PdTdoMoverRenameCommand.description: string;
	begin
  result := 'rename';
  end;

{ ----------------------------------------------------------------------- PdTdoMoverEditCommand }
constructor PdTdoMoverEditCommand.createWithTdoNewTdoAndList(aTdo, aNewTdo: KfObject3D; aList: TListCollection);
  begin
  inherited create;
  commandChangesPlantFile := false;
  tdo := aTdo;
  oldTdo := KfObject3D.create;
  oldTdo.copyFrom(aTdo);
  newTdo := KfObject3D.create;
  newTdo.copyFrom(aNewTdo);
  list := aList;
  listChangedBeforeCommand := TdoMoverForm.listHasChanged(list);
  end;

destructor PdTdoMoverEditCommand.destroy;
  begin
  oldTdo.free;
  oldTdo := nil;
  newTdo.free;
  newTdo := nil;
  inherited destroy;
  end;

procedure PdTdoMoverEditCommand.doCommand;
  begin
  inherited doCommand; {not redo}
  tdo.copyFrom(newTdo);
  TdoMoverForm.updateTdoListForList(list);
  TdoMoverForm.setChangedFlagForTdoList(true, list);
  end;

procedure PdTdoMoverEditCommand.undoCommand;
  begin
  inherited undoCommand;
  tdo.copyFrom(oldTdo);
  TdoMoverForm.updateTdoListForList(list);
  TdoMoverForm.setChangedFlagForTdoList(listChangedBeforeCommand, list);
  end;

function PdTdoMoverEditCommand.description: string;
	begin
  result := 'edit';
  end;

{ ----------------------------------------------------------------------- PdCommandWithListOfTdos }
constructor PdCommandWithListOfTdos.createWithListOfTdos(aList: TList);
  var
    i: smallint;
  begin
  inherited create;
  tdoList := TList.create;
  if aList.count > 0 then for i := 0 to aList.count - 1 do
    tdoList.add(aList.items[i]);
  values := TListCollection.create;
  end;

destructor PdCommandWithListOfTdos.destroy;
  begin
  tdoList.free;
  tdoList := nil;
  values.free;
  values := nil;
  inherited destroy;
  end;

{ ----------------------------------------------------------------------- PdTdoMoverRemoveCommand }
constructor PdTdoMoverRemoveCommand.createWithSelectedTdosAndList(listOfTdos: TList; aList: TListCollection);
  begin
  inherited createWithListOfTdos(listOfTdos);
  commandChangesPlantFile := false;
  list := aList;
  listChangedBeforeCommand := TdoMoverForm.listHasChanged(list);
  removedTdos := TList.create;
  end;

destructor PdTdoMoverRemoveCommand.destroy;
  var
    i: smallint;
  begin
  { free copies of cut tdos if change was done }
  if (done) and (removedTdos <> nil) and (removedTdos.count > 0) then
    for i := 0 to removedTdos.count - 1 do
    	begin
    	tdo := KfObject3D(removedTdos.items[i]);
    	tdo.free;
    	end;
  removedTdos.free;
  removedTdos := nil;
  inherited destroy;
  end;

procedure PdTdoMoverRemoveCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; {not redo}
  if tdoList.count <= 0 then exit;
  { save copy of tdos before deleting }
  removedTdos.clear;
  { don't remove tdos from list until all indexes have been recorded }
  for i := 0 to tdoList.count - 1 do
    begin
    tdo := KfObject3D(tdoList.items[i]);
    removedTdos.add(tdo);
    tdo.indexWhenRemoved := list.indexOf(tdo);
    tdo.selectedIndexWhenRemoved := TdoMoverForm.selectedTdos.indexOf(tdo);
    end;
  for i := 0 to tdoList.count - 1 do
    list.remove(KfObject3D(tdoList.items[i]));
  for i := 0 to tdoList.count - 1 do
    TdoMoverForm.selectedTdos.remove(KfObject3D(tdoList.items[i]));
  TdoMoverForm.updateTdoListForList(list);
  TdoMoverForm.setChangedFlagForTdoList(true, list);
  end;

procedure PdTdoMoverRemoveCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if removedTdos.count > 0 then
    begin
    for i := 0 to removedTdos.count - 1 do
      begin
      tdo := KfObject3D(removedTdos.items[i]);
      if (tdo.indexWhenRemoved >= 0) and (tdo.indexWhenRemoved <= list.count - 1) then
        list.insert(tdo.indexWhenRemoved, tdo)
      else
        list.add(tdo);
      { all removed tdos must have been selected, so also add them to the selected list }
      if (tdo.selectedIndexWhenRemoved >= 0)
          and (tdo.selectedIndexWhenRemoved <= TdoMoverForm.selectedTdos.count - 1) then
        TdoMoverForm.selectedTdos.insert(tdo.selectedIndexWhenRemoved, tdo)
      else
        TdoMoverForm.selectedTdos.add(tdo);
      end;
    TdoMoverForm.updateTdoListForList(list);
    TdoMoverForm.setChangedFlagForTdoList(listChangedBeforeCommand, list);
    end;
  end;

function PdTdoMoverRemoveCommand.description: string;
	begin
  result := 'delete';
  end;

{ ------------------------------------------------------------------ PdTdoMoverTransferCommand }
constructor PdTdoMoverTransferCommand.createWithSelectedTdosAndList(listOfTdos: TList; aList: TListCollection);
  begin
  inherited createWithListOfTdos(listOfTdos);
  commandChangesPlantFile := false;
  list := aList;
  listChangedBeforeCommand := TdoMoverForm.listHasChanged(list);
  end;

destructor PdTdoMoverTransferCommand.destroy;
  var
    i: smallint;
  begin
  { free copies of pasted tdos if change was undone }
  if (not done) and (tdoList <> nil) and (tdoList.count > 0) then
    for i := 0 to tdoList.count - 1 do
    	begin
    	tdo := KfObject3D(tdoList.items[i]);
    	tdo.free;
    	end;
  inherited destroy; {will free tdoList}
  end;

procedure PdTdoMoverTransferCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; {not redo}
  if tdoList.count > 0 then
    begin
    TdoMoverForm.deselectAllTdos;
    for i := 0 to tdoList.count - 1 do
      begin
      tdo := KfObject3D(tdoList.items[i]);
      list.add(tdo);
      TdoMoverForm.selectedTdos.add(tdo);
      end;
    TdoMoverForm.updateTdoListForList(list);
    TdoMoverForm.setChangedFlagForTdoList(true, list);
    end;
  end;

procedure PdTdoMoverTransferCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if tdoList.count > 0 then
    begin
    for i := 0 to tdoList.count - 1 do
      begin
      tdo := KfObject3D(tdoList.items[i]);
      list.remove(tdo);
      TdoMoverForm.selectedTdos.remove(tdo);
      end;
    TdoMoverForm.updateTdoListForList(list);
    TdoMoverForm.setChangedFlagForTdoList(listChangedBeforeCommand, list);
    end;
  end;

function PdTdoMoverTransferCommand.description: string;
	begin
  result := 'transfer';
  end;

{ ------------------------------------------------------------------------------ PdTdoMoverDuplicateCommand }
constructor PdTdoMoverDuplicateCommand.createWithSelectedTdosAndList(listOfTdos: TList; aList: TListCollection);
  begin
  inherited createWithListOfTdos(listOfTdos);
  commandChangesPlantFile := false;
  newTdos := TList.create;
  list := aList;
  listChangedBeforeCommand := TdoMoverForm.listHasChanged(list);
  end;

destructor PdTdoMoverDuplicateCommand.destroy;
  var
    i: smallint;
  begin
  { free copies of created tdos if change was undone }
  if (not done) and (newTdos <> nil) and (newTdos.count > 0) then
    for i := 0 to newTdos.count - 1 do
    	begin
    	tdo := KfObject3D(newTdos.items[i]);
    	tdo.free;
    	end;
  newTdos.free;
  newTdos := nil;
  inherited destroy; {will free tdoList}
  end;

procedure PdTdoMoverDuplicateCommand.doCommand;
  var
    i: smallint;
    tdoCopy: KfObject3D;
  begin
  inherited doCommand;
  if tdoList.count > 0 then
    begin
    TdoMoverForm.deselectAllTdos;
    for i := 0 to tdoList.count - 1 do
      begin
      tdo := KfObject3D(tdoList.items[i]);
      tdoCopy := KfObject3D.create;
      tdo.copyTo(tdoCopy);
      tdoCopy.setName('Copy of ' + tdoCopy.getName);
      newTdos.add(tdoCopy);
      list.add(tdoCopy);
      TdoMoverForm.selectedTdos.add(tdoCopy);
      end;
    TdoMoverForm.updateTdoListForList(list);
    TdoMoverForm.setChangedFlagForTdoList(true, list);
    end;
  end;

procedure PdTdoMoverDuplicateCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if newTdos.count > 0 then
    begin
    for i := 0 to newTdos.count - 1 do
      begin
      tdo := KfObject3D(newTdos.items[i]);
      list.remove(tdo);
      TdoMoverForm.selectedTdos.remove(tdo);
      end;
    TdoMoverForm.updateTdoListForList(list);
    TdoMoverForm.setChangedFlagForTdoList(listChangedBeforeCommand, list);
    end;
  end;

procedure PdTdoMoverDuplicateCommand.redoCommand;
  var
    i: smallint;
  begin
  inherited doCommand; {not redo}
  if newTdos.count > 0 then
    begin
    TdoMoverForm.deselectAllTdos;
    for i := 0 to newTdos.count - 1 do
      begin
      tdo := KfObject3D(newTdos.items[i]);
      list.add(tdo);
      TdoMoverForm.selectedTdos.add(tdo);
      end;
    TdoMoverForm.updateTdoListForList(list);
    TdoMoverForm.setChangedFlagForTdoList(true, list);
    end;
  end;

function PdTdoMoverDuplicateCommand.description: string;
	begin
  result := 'duplicate';
  end;

procedure TTdoMoverForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Using_the_3D_object_mover');
  end;

end.
