unit Umover;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, StdCtrls, Buttons, ExtCtrls,
  uplantmn, uplant, ucommand, updcom, updform, Grids;

type
  TMoverForm = class(PdForm)
    leftPlantFileNameEdit: TEdit;
    leftOpenClose: TButton;
    rightPlantFileNameEdit: TEdit;
    rightOpenClose: TButton;
    newFile: TButton;
    transfer: TButton;
    close: TButton;
    previewImage: TImage;
    undo: TButton;
    redo: TButton;
    cut: TButton;
    copy: TButton;
    paste: TButton;
    rename: TButton;
    duplicate: TButton;
    delete: TButton;
    leftPlantFileChangedIndicator: TImage;
    rightPlantFileChangedIndicator: TImage;
    leftPlantList: TDrawGrid;
    rightPlantList: TDrawGrid;
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
    procedure leftPlantListMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure rightPlantListMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure leftPlantListDblClick(Sender: TObject);
    procedure rightPlantListDblClick(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure cutClick(Sender: TObject);
    procedure copyClick(Sender: TObject);
    procedure pasteClick(Sender: TObject);
    procedure undoClick(Sender: TObject);
    procedure redoClick(Sender: TObject);
    procedure FormKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure leftPlantListDragOver(Sender, Source: TObject; X, Y: Integer;
      State: TDragState; var Accept: Boolean);
    procedure leftPlantListEndDrag(Sender, Target: TObject; X, Y: Integer);
    procedure rightPlantListDragOver(Sender, Source: TObject; X,
      Y: Integer; State: TDragState; var Accept: Boolean);
    procedure rightPlantListEndDrag(Sender, Target: TObject; X,
      Y: Integer);
    procedure leftPlantListDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure rightPlantListDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure FormCreate(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure leftPlantListKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure rightPlantListKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
  public
    { Public declarations }
    leftPlantFileName, rightPlantFileName: string;
    leftManager, rightManager: PdPlantManager;
    leftPlantFileChanged, rightPlantFileChanged: boolean;
    lastLeftSingleClickPlantIndex, lastRightSingleClickPlantIndex: integer;
    leftOrRight: smallint;
    changedCurrentPlantFile: boolean;
    commandList: PdCommandList;
    selectedPlants: TList;
    untitledDomainFileSavedAs: string;
    dragItemsY: integer;
    justDoubleClickedOnLeftGrid, justDoubleClickedOnRightGrid: boolean;
    constructor create(AOwner: TComponent); override;
    destructor destroy; override;
    procedure setFileNameForManager(newName: string; manager: PdPlantManager);
    function getFileNameForManager(manager: PdPlantManager): string;
    function getFileNameForOtherManager(manager: PdPlantManager): string;
    function gridForManager(manager: PdPlantManager): TDrawGrid;
    procedure setChangedFlagForPlantManager(value: boolean; manager: PdPlantManager);
    function managerHasChanged(manager: PdPlantManager): boolean;
    procedure updateForNewFile(newFileName: string; manager: PdPlantManager);
    procedure updateButtonsForUndoRedo;
    procedure updatePlantListForManager(manager: PdPlantManager);
	 	function copyPlantToPlantManager(plant: PdPlant; toPlantManager: PdPlantManager): PdPlant;
    function selectedManager(thisManager: boolean): PdPlantManager;
    function askToSaveManagerAndProceed(manager: PdPlantManager): boolean;
    procedure openPlantFileForManager(manager: PdPlantManager; fileNameToStart: string);
    procedure newPlantFileForManager(manager: PdPlantManager);
    procedure closePlantFileForManager(manager: PdPlantManager);
    procedure managerSaveOrSaveAs(manager: PdPlantManager; askForFileName: boolean);
    function haveLeftFile: boolean;
    function haveRightFile: boolean;
    procedure drawPreview(plant: PdPlant);
    procedure drawLineInGrid(grid: TDrawGrid; manager: PdPlantManager; index: integer; rect: TRect; state: TGridDrawState);
    procedure clearCommandList;
    procedure doCommand(command: PdCommand);
    procedure deselectAllPlants;
    procedure updatePasteButtonForClipboardContents;
    procedure updateForChangeToSelectedPlants;
    procedure copySelectedPlantsToClipboard;
    function leftRightString(leftString, rightString: string): string;
    procedure resizePreviewImage;
    function focusedPlant: PdPlant;
    function focusedPlantIndexInManager: smallint;
    procedure selectPlantAtIndex(Shift: TShiftState; index: Integer);
    procedure listKeyDown(var Key: Word; Shift: TShiftState);
    procedure moveUpOrDownWithKey(indexAfterMove: smallint);
    procedure moveSelectedPlantsDown;
    procedure moveSelectedPlantsUp;
    procedure redrawSelectedGrid;
    end;

  PdMoverRenameCommand = class(PdCommand)
    public
    plant: PdPlant;
    oldName, newName: string;
    manager: PdPlantManager;
    managerChangedBeforeCommand: boolean;
    constructor createWithPlantNewNameAndManager(aPlant: PdPlant; aNewName: string;
      aManager: PdPlantManager);
	  procedure doCommand; override;
	  procedure undoCommand; override;
    function description: string; override;
    end;

  PdMoverRemoveCommand = class(PdCommandWithListOfPlants){use for cut and delete}
    public
    removedPlants: TList;
    copyToClipboard: boolean;
    manager: PdPlantManager;
    managerChangedBeforeCommand: boolean;
    constructor createWithListOfPlantsManagerAndClipboardFlag(aList: TList;
      aManager: PdPlantManager; aCopyToClipboard: boolean);
    destructor destroy; override;
	  procedure doCommand; override;
	  procedure undoCommand; override;
    function description: string; override;
    end;

  PdMoverPasteCommand = class(PdCommandWithListOfPlants) {use for transfer and paste}
    public
    isTransfer: boolean;
    manager: PdPlantManager;
    managerChangedBeforeCommand: boolean;
    constructor createWithListOfPlantsAndManager(aList: TList; aManager: PdPlantManager);
    destructor destroy; override;
	  procedure doCommand; override;
	  procedure undoCommand; override;
    function description: string; override;
    end;

  PdMoverDuplicateCommand = class(PdCommandWithListOfPlants)
    public
    newPlants: TList;
    manager: PdPlantManager;
    managerChangedBeforeCommand: boolean;
    constructor createWithListOfPlantsAndManager(aList: TList; aManager: PdPlantManager);
    destructor destroy; override;
	  procedure doCommand; override;
	  procedure undoCommand; override;
    procedure redoCommand; override;
    function description: string; override;
    end;

implementation

{$R *.DFM}

uses ClipBrd,
  udomain, umain, ucursor, usupport, umath, uturtle, ubmpsupport;

const
  kLeft = 0; kRight = 1;
  kNewPlantFileName = 'untitled.pla';
  kThisManager = true; kOtherManager = false;

var MoverForm: TMoverForm;

{ -------------------------------------------------------------------------------------------- *creation/destruction }
constructor TMoverForm.create(AOwner: TComponent);
  begin
  inherited create(AOwner);
  MoverForm := self;
  leftManager := PdPlantManager.create;
  rightManager := PdPlantManager.create;
  commandList := PdCommandList.create;
  selectedPlants := TList.create;
  commandList.setNewUndoLimit(domain.options.undoLimit);
  commandList.setNewObjectUndoLimit(domain.options.undoLimitOfPlants);
  self.updateButtonsForUndoRedo;
  { load current plant file into left side to start }
  if length(domain.plantFileName) > 0 then
    self.openPlantFileForManager(leftManager, domain.plantFileName)
  else
    self.closePlantFileForManager(leftManager);
  { right side is empty to start }
  self.closePlantFileForManager(rightManager);
  self.updatePasteButtonForClipboardContents;
  end;

procedure TMoverForm.FormCreate(Sender: TObject);
  begin
  leftPlantList.dragCursor := crDragPlant;
  rightPlantList.dragCursor := crDragPlant;
  end;

destructor TMoverForm.destroy;
  begin
  leftManager.free;
  leftManager := nil;
  rightManager.free;
  rightManager := nil;
  selectedPlants.free;
  selectedPlants := nil;
  commandList.free;
  commandList := nil;
  inherited destroy;
  end;

procedure TMoverForm.FormClose(Sender: TObject; var Action: TCloseAction);
  begin
  if modalResult = mrOk then exit;
  { same as exit, but can't call exit because we have to set the action flag }
  action := caNone;
  if not self.askToSaveManagerAndProceed(leftManager) then exit;
  if not self.askToSaveManagerAndProceed(rightManager) then exit;
  action := caFree;
  end;

procedure TMoverForm.FormKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  case key of
    VK_DELETE: self.deleteClick(self);
    end;
  if not (ssCtrl in shift) then exit;
  case char(key) of
    'C', 'c': begin self.copyClick(self); key := 0; end;
    'X', 'x': begin self.cutClick(self); key := 0; end;
    'V', 'v': begin self.pasteClick(self); key := 0; end;
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
procedure TMoverForm.undoClick(Sender: TObject);
  begin
  commandList.undoLast;
  self.updateButtonsForUndoRedo;
  self.updateForChangeToSelectedPlants;
  end;

procedure TMoverForm.redoClick(Sender: TObject);
  begin
  commandList.redoLast;
  self.updateButtonsForUndoRedo;
  self.updateForChangeToSelectedPlants;
  end;

procedure TMoverForm.cutClick(Sender: TObject);
  var
    manager: PdPlantManager;
    newCommand: PdCommand;
  begin
  manager := self.selectedManager(kThisManager);
  if (manager = nil) or (selectedPlants.count <= 0) then exit;
  newCommand := PdMoverRemoveCommand.createWithListOfPlantsManagerAndClipboardFlag(
      selectedPlants, manager, kCopyToClipboard);
  self.doCommand(newCommand);
	end;

procedure TMoverForm.copyClick(Sender: TObject);
  begin
  self.copySelectedPlantsToClipboard;
  end;

procedure TMoverForm.pasteClick(Sender: TObject);
  var
    manager: PdPlantManager;
    newCommand: PdCommand;
    newPlants: TList;
  begin
  manager := self.selectedManager(kThisManager);
  if manager = nil then exit;
  newPlants := TList.create;
  domain.plantManager.pastePlantsFromPrivatePlantClipboardToList(newPlants);
  newCommand := PdMoverPasteCommand.createWithListOfPlantsAndManager(newPlants, manager);
  self.doCommand(newCommand);
  newPlants.free; {command has its own list, so we need to free this one}
	end;

procedure TMoverForm.closeClick(Sender: TObject);
  begin
  if not self.askToSaveManagerAndProceed(leftManager) then exit;
  if not self.askToSaveManagerAndProceed(rightManager) then exit;
  modalResult := mrOk; { cannot cancel }
  end;

procedure TMoverForm.leftOpenCloseClick(Sender: TObject);
  begin
  if haveLeftFile then {file open}
    self.closePlantFileForManager(leftManager)
  else   {no file}
    self.openPlantFileForManager(leftManager, '')
  end;

procedure TMoverForm.rightOpenCloseClick(Sender: TObject);
  begin
  if haveRightFile then {file open}
    self.closePlantFileForManager(rightManager)
  else   {no file}
    self.openPlantFileForManager(rightManager, '')
  end;

procedure TMoverForm.newFileClick(Sender: TObject);
  begin
  self.newPlantFileForManager(rightManager);
  end;

procedure TMoverForm.transferClick(Sender: TObject);
  var
    manager, otherManager: PdPlantManager;
    newCommand: PdCommand;
    newPlants: TList;
    plant, newPlant: PdPlant;
    i: smallint;
  begin
  manager := self.selectedManager(kThisManager);
  otherManager := self.selectedManager(kOtherManager);
  if (manager = nil) or (otherManager = nil) or (selectedPlants.count <= 0) then exit;
  if selectedPlants.count > 0 then
    begin
    newPlants := TList.create; {command will free}
    for i := 0 to selectedPlants.count - 1 do
      begin
      plant := PdPlant(selectedPlants.items[i]);
      newPlant := PdPlant.create;
      plant.copyTo(newPlant);
      newPlants.add(newPlant);
      end;
    newCommand := PdMoverPasteCommand.createWithListOfPlantsAndManager(newPlants, otherManager);
    (newCommand as PdMoverPasteCommand).isTransfer := true;
    self.doCommand(newCommand);
    newPlants.free; {command has its own list, so we need to free this one}
    end;
	end;

procedure TMoverForm.duplicateClick(Sender: TObject);
  var
    manager: PdPlantManager;
    newCommand: PdCommand;
  begin
  manager := self.selectedManager(kThisManager);
  if (manager = nil) or (selectedPlants.count <= 0) then exit;
  newCommand := PdMoverDuplicateCommand.createWithListOfPlantsAndManager(selectedPlants, manager);
  self.doCommand(newCommand);
	end;

procedure TMoverForm.renameClick(Sender: TObject);
  var
    plant: PdPlant;
    manager: PdPlantManager;
    newName: ansistring;
    newCommand: PdCommand;
	begin
  { can only rename one plant at a time }
  manager := self.selectedManager(kThisManager);
  plant := self.focusedPlant;
  if (plant = nil) or (manager = nil) then exit;
  newName := plant.getName;
  if not inputQuery('Enter new name', 'Type a new name for ' + newName + '.', newName) then exit;
  newCommand := PdMoverRenameCommand.createWithPlantNewNameAndManager(plant, newName, manager);
  self.doCommand(newCommand);
	end;

procedure TMoverForm.deleteClick(Sender: TObject);
  var
    manager: PdPlantManager;
    newCommand: PdCommand;
  begin
  manager := self.selectedManager(kThisManager);
  if (manager = nil) or (selectedPlants.count <= 0) then exit;
  newCommand := PdMoverRemoveCommand.createWithListOfPlantsManagerAndClipboardFlag(
      selectedPlants, manager, kDontCopyToClipboard);
  self.doCommand(newCommand);
	end;

{ -------------------------------------------------------------------------------------- *list box actions }
procedure TMoverForm.leftPlantListDrawCell(Sender: TObject; Col,
  Row: Integer; Rect: TRect; State: TGridDrawState);
  begin
  self.drawLineInGrid(leftPlantList, leftManager, row, rect, state);
  end;

procedure TMoverForm.rightPlantListDrawCell(Sender: TObject; Col,
  Row: Integer; Rect: TRect; State: TGridDrawState);
  begin
  self.drawLineInGrid(rightPlantList, rightManager, row, rect, state);
  end;

procedure TMoverForm.drawLineInGrid(grid: TDrawGrid; manager: PdPlantManager;
    index: integer; rect: TRect; state: TGridDrawState);
  var
	  plant: PdPlant;
    selected: boolean;
    cText: array[0..255] of Char;
  begin
  if Application.terminated then exit;
  grid.canvas.brush.color := grid.color;
  grid.canvas.fillRect(rect);
  if (manager.plants.count <= 0) or (index < 0) or (index > manager.plants.count - 1) then exit;
  { set up plant pointer }
  plant := PdPlant(manager.plants.items[index]);
  if plant = nil then exit;
  selected := selectedPlants.indexOf(plant) >= 0;
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
    strPCopy(cText, plant.getName);
    rect.left := rect.left + 2; { margin for text }
    winprocs.drawText(handle, cText, strLen(cText), rect, DT_LEFT);
    if plant = self.focusedPlant then
      begin
      rect.left := rect.left - 2; { put back }
      drawFocusRect(rect);
      end;
    end;
  end;

// left list mouse handling
procedure TMoverForm.leftPlantListMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
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
  if leftManager.plants.count > 0 then
    begin
    if leftOrRight = kRight then
      begin
      selectedPlants.clear;
      lastRightSingleClickPlantIndex := -1;
      rightPlantList.invalidate;
      end;
    leftOrRight := kLeft;
    leftPlantList.mouseToCell(x, y, col, row);
    self.selectPlantAtIndex(shift, row);
    self.updateForChangeToSelectedPlants;
    leftPlantList.beginDrag(false);
    end;
  end;

procedure TMoverForm.leftPlantListDragOver(Sender, Source: TObject; X,
  Y: Integer; State: TDragState; var Accept: Boolean);
  begin
  accept := (source <> nil) and (sender <> nil);
  if source = rightPlantList then
    accept := accept and haveLeftFile
  else
    accept := accept and (source = sender);
  end;

procedure TMoverForm.leftPlantListEndDrag(Sender, Target: TObject; X, Y: Integer);
  begin
  if (target = rightPlantList) then
    self.transferClick(self);
  end;

procedure TMoverForm.leftPlantListDblClick(Sender: TObject);
  begin
  self.renameClick(self);
  leftPlantList.endDrag(false);
  justDoubleClickedOnLeftGrid := true;
  end;

// right list mouse handling
procedure TMoverForm.rightPlantListMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
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
  if rightManager.plants.count > 0 then
    begin
    if leftOrRight = kLeft then
      begin
      selectedPlants.clear;
      lastLeftSingleClickPlantIndex := -1;
      leftPlantList.invalidate;
      end;
    leftOrRight := kRight;
    rightPlantList.mouseToCell(x, y, col, row);
    self.selectPlantAtIndex(shift, row);
    self.updateForChangeToSelectedPlants;
    rightPlantList.beginDrag(false);
    end;
  end;

procedure TMoverForm.rightPlantListDragOver(Sender, Source: TObject; X,
  Y: Integer; State: TDragState; var Accept: Boolean);
  begin
  accept := (source <> nil) and (sender <> nil);
  if source = leftPlantList then
    accept := accept and haveRightFile
  else
    accept := accept and (source = sender);
  end;

procedure TMoverForm.rightPlantListEndDrag(Sender, Target: TObject; X, Y: Integer);
  begin
  if (target = leftPlantList) then
    self.transferClick(self);
  end;

procedure TMoverForm.rightPlantListDblClick(Sender: TObject);
  begin
  self.renameClick(self);
  rightPlantList.endDrag(false);
  justDoubleClickedOnRightGrid := true;
  end;

procedure TMoverForm.selectPlantAtIndex(Shift: TShiftState; index: Integer);
  var
   i: smallint;
   plant: PdPlant;
   manager: PdPlantManager;
   lastSingleClickPlantIndex, lastRow: integer;
   grid: TDrawGrid;
	begin
  if application.terminated then exit;
  manager := self.selectedManager(kThisManager);
  if manager = nil then exit;
  if (index < 0) then
    begin
    selectedPlants.clear;
    self.redrawSelectedGrid;
    exit;
    end;
  plant := PdPlant(manager.plants.items[index]);
  if plant = nil then exit;
  if (ssCtrl in shift) then
    begin
    if selectedPlants.indexOf(plant) >= 0 then
      selectedPlants.remove(plant)
    else
      selectedPlants.add(plant);
    end
  else if (ssShift in shift) then
    begin
    if leftOrRight = kLeft then
      lastSingleClickPlantIndex := lastLeftSingleClickPlantIndex
    else
      lastSingleClickPlantIndex := lastRightSingleClickPlantIndex;
    if (lastSingleClickPlantIndex >= 0) and (lastSingleClickPlantIndex <= manager.plants.count - 1)
        and (lastSingleClickPlantIndex <> index) then
      begin
      if lastSingleClickPlantIndex < index then
        begin
        for i := lastSingleClickPlantIndex to index do
          if selectedPlants.indexOf(manager.plants.items[i]) < 0 then
            selectedPlants.add(manager.plants.items[i]);
        end
      else if lastSingleClickPlantIndex > index then
        begin
        for i := lastSingleClickPlantIndex downto index do
          if selectedPlants.indexOf(manager.plants.items[i]) < 0 then
            selectedPlants.add(manager.plants.items[i]);
        end;
      end;
    end
  else // just a click
    begin
    if selectedPlants.indexOf(plant) <= 0 then
      begin
      selectedPlants.clear;
      self.redrawSelectedGrid;
      selectedPlants.add(plant);
      if leftOrRight = kLeft then
        lastLeftSingleClickPlantIndex := index
      else
        lastRightSingleClickPlantIndex := index;
      grid := gridForManager(manager);
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
  self.redrawSelectedGrid;
	end;

procedure TMoverForm.leftPlantListKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  self.listKeyDown(key, shift);
  end;

procedure TMoverForm.rightPlantListKeyDown(Sender: TObject; var Key: Word; shift: TShiftState);
  begin
  self.listKeyDown(key, shift);
  end;

procedure TMoverForm.listKeyDown(var Key: Word; Shift: TShiftState);
  begin
  case key of
    vk_down, vk_right:
      if (ssShift in shift) then
        begin
        key := 0; {swallow key}
        self.moveSelectedPlantsDown;
        end
      else
        begin
        key := 0;
        self.moveUpOrDownWithKey(self.focusedPlantIndexInManager + 1);
        end;
    vk_up, vk_left:
      if (ssShift in shift) then
        begin
        key := 0; {swallow key}
        self.moveSelectedPlantsUp;
        end
     else
        begin
        key := 0;
        self.moveUpOrDownWithKey(self.focusedPlantIndexInManager - 1);
        end;
    vk_return:
        begin
        key := 0;
        self.renameClick(self);
        end;
    end;
  end;

procedure TMoverForm.moveUpOrDownWithKey(indexAfterMove: smallint);
  var
    manager: PdPlantManager;
  begin
  manager := self.selectedManager(kThisManager);
  if manager = nil then exit;
  { loop around }
  if indexAfterMove > manager.plants.count - 1 then
    indexAfterMove := 0;
  if indexAfterMove < 0 then
    indexAfterMove := manager.plants.count - 1;
  if (indexAfterMove >= 0) and (indexAfterMove <= manager.plants.count - 1) then
    begin
    self.deselectAllPlants;
    self.selectPlantAtIndex([]{no shift}, indexAfterMove);
    self.drawPreview(focusedPlant);
    end;
  end;

procedure TMoverForm.moveSelectedPlantsDown;
  var
    manager: PdPlantManager;
    i: smallint;
    plant: PdPlant;
  begin
  if selectedPlants.count <= 0 then exit;
  manager := self.selectedManager(kThisManager);
  if manager = nil then exit;
  if manager.plants.count > 1 then
    begin
    i := manager.plants.count - 2;  { start at next to last one because you can't move last one down any more }
    while i >= 0 do
      begin
      plant := PdPlant(manager.plants.items[i]);
      if selectedPlants.indexOf(plant) >= 0 then
        manager.plants.move(i, i + 1);
      dec(i);
      end;
    end;
  self.redrawSelectedGrid;
  // reordering makes change flag true
  self.setChangedFlagForPlantManager(true, selectedManager(kThisManager));
  end;

procedure TMoverForm.moveSelectedPlantsUp;
  var
    manager: PdPlantManager;
    i: smallint;
    plant: PdPlant;
  begin
  if selectedPlants.count <= 0 then exit;
  manager := self.selectedManager(kThisManager);
  if manager = nil then exit;
  if manager.plants.count > 1 then
    begin
    i := 1;  { start at 1 because you can't move first one up any more }
    while i <= manager.plants.count - 1 do
      begin
      plant := PdPlant(manager.plants.items[i]);
      if selectedPlants.indexOf(plant) >= 0 then
        manager.plants.move(i, i - 1);
      inc(i);
      end;
    end;
  self.redrawSelectedGrid;
  // reordering makes change flag true
  self.setChangedFlagForPlantManager(true, selectedManager(kThisManager));
  end;

procedure TMoverForm.redrawSelectedGrid;
  begin
  if leftOrRight = kLeft then
    leftPlantList.invalidate
  else
    rightPlantList.invalidate;
  end;

{ -------------------------------------------------------------------------------------------- *updating }
procedure TMoverForm.updateForNewFile(newFileName: string; manager: PdPlantManager);
  begin
  self.clearCommandList;
  self.setFileNameForManager(newFileName, manager);
  self.updatePlantListForManager(manager);
  self.setChangedFlagForPlantManager(false, manager);
  self.deselectAllPlants;
  if newFileName <> '' then
    begin
    if manager = leftManager then
      leftOrRight := kLeft
    else
      leftOrRight := kRight;
    end;
  self.updateForChangeToSelectedPlants;
  end;

procedure TMoverForm.deselectAllPlants;
  begin
  self.selectedPlants.clear;
  self.redrawSelectedGrid;
  end;

procedure TMoverForm.updatePasteButtonForClipboardContents;
  begin
  paste.enabled := (domain.plantManager.privatePlantClipboard.count > 0);
  end;

function TMoverForm.leftRightString(leftString, rightString: string): string;
  begin
  if leftOrRight = kLeft then
   result := leftString
  else
   result := rightString;
  end;

procedure TMoverForm.updateForChangeToSelectedPlants;
  var
    atLeastOnePlantSelected, atLeastOneFile: boolean;
  begin
  leftPlantList.invalidate;
  rightPlantList.invalidate;
  if leftOrRight = kLeft then
    begin
    if haveLeftFile then
      leftOpenClose.caption := '&Close'
    else
      leftOpenClose.caption := '&Open...';
    leftPlantFileNameEdit.color := clAqua;
    leftPlantFileNameEdit.refresh;
    rightPlantFileNameEdit.color := clBtnFace;
    rightPlantFileNameEdit.refresh;
    self.drawPreview(focusedPlant);
    end
  else
    begin
    if haveRightFile then
      rightOpenClose.caption := '&Close'
    else
      rightOpenClose.caption := '&Open...';
    leftPlantFileNameEdit.color := clBtnFace;
    leftPlantFileNameEdit.refresh;
    rightPlantFileNameEdit.color := clAqua;
    rightPlantFileNameEdit.refresh;
    self.drawPreview(focusedPlant);
    end;
  atLeastOneFile := haveLeftFile or haveRightFile;
  atLeastOnePlantSelected := (selectedPlants.count > 0);
  transfer.enabled := haveLeftFile and haveRightFile and atLeastOnePlantSelected;
  transfer.caption := leftRightString('&Transfer >>', '<< &Transfer');
  cut.enabled := atLeastOneFile and atLeastOnePlantSelected;
  copy.enabled := atLeastOneFile and atLeastOnePlantSelected;
  duplicate.enabled := atLeastOneFile and atLeastOnePlantSelected;
  delete.enabled := atLeastOneFile and atLeastOnePlantSelected;
  rename.enabled := atLeastOneFile and atLeastOnePlantSelected;
  end;

procedure TMoverForm.updateButtonsForUndoRedo;
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

procedure TMoverForm.updatePlantListForManager(manager: PdPlantManager);
  var
    grid: TDrawGrid;
  begin
  grid := gridForManager(manager);
  if grid = nil then exit;
  grid.rowCount := manager.plants.count;
  grid.invalidate;
  end;

procedure TMoverForm.drawPreview(plant: PdPlant);
  begin
  with previewImage do
    begin
    if plant = nil then
      begin
      canvas.brush.style := bsSolid;
      canvas.brush.color := clWindow;
      end
    else
      begin
      if not plant.previewCacheUpToDate then
        try
          cursor_startWait;
          plant.drawPreviewIntoCache(Point(width, height), kDontConsiderDomainScale, kDrawNow);
        finally
          cursor_stopWait;
        end;
      plant.previewCache.transparent := false;
      copyBitmapToCanvasWithGlobalPalette(plant.previewCache, previewImage.canvas, rect(0,0,0,0));
      realizePalette(canvas.handle);
      canvas.brush.style := bsClear;
      end;
    canvas.pen.color := clBtnText;
    canvas.pen.style := psSolid;
    canvas.rectangle(0, 0, width, height);
    end;
  end;

{ ------------------------------------------------------------------------------------------ *selecting }
function TMoverForm.focusedPlant: PdPlant;
  begin
  result := nil;
  if selectedPlants.count > 0 then
    result := PdPlant(selectedPlants.items[0]);
  end;

function TMoverForm.focusedPlantIndexInManager: smallint;
  var
    manager: PdPlantManager;
  begin
  result := -1;
  manager := selectedManager(kThisManager);
  if manager = nil then exit;
  if selectedPlants.count > 0 then
    result := manager.plants.indexOf(selectedPlants.items[0]);
  end;

function TMoverForm.haveLeftFile: boolean;
  begin
  result := length(leftPlantFileName) <> 0;
  end;

function TMoverForm.haveRightFile: boolean;
  begin
  result := length(rightPlantFileName) <> 0;
  end;

function TMoverForm.selectedManager(thisManager: boolean): PdPlantManager;
  begin
  result := nil;
  if leftOrRight = kLeft then
    begin
    if thisManager then
      result := leftManager
    else
      result := rightManager;
    end
  else
    begin
    if thisManager then
      result := rightManager
    else
      result := leftManager;
    end;
  end;

function TMoverForm.getFileNameForManager(manager: PdPlantManager): string;
  begin
  if manager = leftManager then
    result := leftPlantFileName
  else
    result := rightPlantFileName;
  end;

function TMoverForm.getFileNameForOtherManager(manager: PdPlantManager): string;
  begin
  if manager = rightManager then
    result := leftPlantFileName
  else
    result := rightPlantFileName;
  end;

procedure TMoverForm.setFileNameForManager(newName: string; manager: PdPlantManager);
  begin
  if manager = leftManager then
    begin
    leftPlantFileName := newName;
    leftPlantFileNameEdit.text := newName;
    leftPlantFileNameEdit.selStart := length(newName);
    end
  else
    begin
    rightPlantFileName := newName;
    rightPlantFileNameEdit.text := newName;
    rightPlantFileNameEdit.selStart := length(newName);
    end;
  end;

function TMoverForm.gridForManager(manager: PdPlantManager): TDrawGrid;
  begin
  result := nil;
  if manager = leftManager then
    result := leftPlantList
  else if manager = rightManager then
    result := rightPlantList;
  end;

function TMoverForm.managerHasChanged(manager: PdPlantManager): boolean;
  begin
  if manager = leftManager then
    result := leftPlantFileChanged
  else
    result := rightPlantFileChanged;
  end;

procedure TMoverForm.setChangedFlagForPlantManager(value: boolean; manager: PdPlantManager);
  begin
  if manager = leftManager then
    begin
    leftPlantFileChanged := value;
    if leftPlantFileChanged then
      leftPlantFileChangedIndicator.picture := MainForm.fileChangedImage.picture
    else
      leftPlantFileChangedIndicator.picture := MainForm.fileNotChangedImage.picture;
    end
  else
    begin
    rightPlantFileChanged := value;
    if rightPlantFileChanged then
      rightPlantFileChangedIndicator.picture := MainForm.fileChangedImage.picture
    else
      rightPlantFileChangedIndicator.picture := MainForm.fileNotChangedImage.picture;
    end;
  end;

{ ------------------------------------------------------------------------------------------- *copying }
function TMoverForm.copyPlantToPlantManager(plant: PdPlant; toPlantManager: PdPlantManager): PdPlant;
   begin
   if plant = nil then
     result := nil
   else
     result := toPlantManager.copyFromPlant(plant);
  end;

procedure TMoverForm.copySelectedPlantsToClipboard;
  begin
  if selectedPlants.count <= 0 then exit;
  domain.plantManager.copyPlantsInListToPrivatePlantClipboard(selectedPlants);
  self.updatePasteButtonForClipboardContents;
  end;

{ ------------------------------------------------------------------------ *opening, closing and saving }
procedure TMoverForm.openPlantFileForManager(manager: PdPlantManager; fileNameToStart: string);
  var
    fileNameWithPath: string;
  begin
  if not self.askToSaveManagerAndProceed(manager) then exit;
  if fileNameToStart = '' then
    fileNameWithPath := getFileOpenInfo(kFileTypePlant, kNoSuggestedFile, 'Choose a plant file')
  else
    fileNameWithPath := fileNameToStart;
  if fileNameWithPath = '' then
    self.updateForNewFile(fileNameWithPath, manager)
  else
  	begin
  	if fileNameWithPath = self.getFileNameForOtherManager(manager) then
    	begin
      showMessage('The file you chose is already open on the other side.');
    	exit;
    	end;
    try
      cursor_startWait;
      if fileExists(fileNameWithPath) then
        manager.loadPlantsFromFile(fileNameWithPath, kInPlantMover)
      else
        self.newPlantFileForManager(manager);
      // PDF PORT -- added semicolon
      self.updateForNewFile(fileNameWithPath, manager);
    finally
      cursor_stopWait;
    end;
    end;
	end;

procedure TMoverForm.closePlantFileForManager(manager: PdPlantManager);
  begin
  if not self.askToSaveManagerAndProceed(manager) then exit;
  manager.plants.clear;
  self.updateForNewFile('', manager);
  end;

procedure TMoverForm.newPlantFileForManager(manager: PdPlantManager);
  begin
  if not self.askToSaveManagerAndProceed(manager) then exit;
  manager.plants.clear;
  self.updateForNewFile(kNewPlantFileName, manager);
  end;

procedure TMoverForm.managerSaveOrSaveAs(manager: PdPlantManager; askForFileName: boolean);
  var
    fileInfo: SaveFileNamesStructure;
    fileName: string;
    askForFileNameConsideringUntitled: boolean;
  begin
  fileName := self.getFileNameForManager(manager);
  if fileName = kNewPlantFileName then
    askForFileNameConsideringUntitled := true
  else
    askForFileNameConsideringUntitled := askForFileName;
  if not getFileSaveInfo(kFileTypePlant, askForFileNameConsideringUntitled, fileName, fileInfo) then exit;
  try
    cursor_startWait;
    manager.savePlantsToFile(fileInfo.tempFile, kInPlantMover);
    fileInfo.writingWasSuccessful := true;
  finally
    cursor_stopWait;
    cleanUpAfterFileSave(fileInfo);
    self.updateForNewFile(kNewPlantFileName, manager);
    if (fileInfo.newFile = domain.plantFileName) then
      changedCurrentPlantFile := true;
    // deal with case of: started mover with untitled file, changed file, returned
    if (fileName = kNewPlantFileName) and (domain.plantFileName = kNewPlantFileName) then
      begin
      changedCurrentPlantFile := true;
      untitledDomainFileSavedAs := fileInfo.newFile;
      end;
  end;
  end;

function TMoverForm.askToSaveManagerAndProceed(manager: PdPlantManager): boolean;
  { returns false if user cancelled action }
  var
    response: word;
    prompt: string;
  begin
  result := true;
  if not self.managerHasChanged(manager) then exit;
  prompt := 'Save changes to ' + extractFileName(self.getFileNameForManager(manager)) + '?';
  response := messageDlg(prompt, mtConfirmation, mbYesNoCancel, 0);
  case response of
    mrYes: self.managerSaveOrSaveAs(manager, kDontAskForFileName);
    mrNo: result := true;
    mrCancel: result := false;
    end;
  end;

{ ------------------------------------------------------------------------------------------ *resizing }
const kBetweenGap = 4;

procedure TMoverForm.FormResize(Sender: TObject);
  var
    midWidth, listBoxWidth, listBoxTop, openCloseTop: smallint;
  begin
  if Application.terminated then exit;
  if leftManager = nil then exit;
  if rightManager = nil then exit;
  if selectedPlants = nil then exit; 
  midWidth := self.clientWidth div 2;
  listBoxWidth := leftPlantList.width; //same as right
  listBoxTop := kBetweenGap + leftPlantFileNameEdit.height + kBetweenGap + leftOpenClose.height + kBetweenGap;
  { list boxes }
  with leftPlantList do setBounds(kBetweenGap, listBoxTop, listBoxWidth,
      intMax(0, self.clientHeight - listBoxTop - kBetweenGap));
  leftPlantList.defaultColWidth := leftPlantList.clientWidth;
  with rightPlantList do setBounds(intMax(0, self.clientWidth - listBoxWidth - kBetweenGap), listBoxTop,
      listBoxWidth, intMax(0, self.clientHeight - listBoxTop - kBetweenGap));
  rightPlantList.defaultColWidth := rightPlantList.clientWidth;
  { edits and buttons at top }
  with leftPlantFileNameEdit do setBounds(kBetweenGap, kBetweenGap, listBoxWidth - kBetweenGap * 2, height);
  with leftPlantFileChangedIndicator do setBounds(
      kBetweenGap, leftPlantFileNameEdit.top + leftPlantFileNameEdit.height + kBetweenGap, width, height);
  with rightPlantFileNameEdit do setBounds(rightPlantList.left, kBetweenGap, listBoxWidth- kBetweenGap * 2, height);
  with rightPlantFileChangedIndicator do setBounds(
      rightPlantList.left, rightPlantFileNameEdit.top + rightPlantFileNameEdit.height + kBetweenGap, width, height);
  openCloseTop := leftPlantFileNameEdit.top + leftPlantFileNameEdit.height + kBetweenGap;
  with leftOpenClose do setBounds(
    leftPlantFileChangedIndicator.left + leftPlantFileChangedIndicator.width + kBetweenGap, openCloseTop, width, height);
  with rightOpenClose do setBounds(
    rightPlantFileChangedIndicator.left + rightPlantFileChangedIndicator.width + kBetweenGap, openCloseTop, width, height);
  with newFile do setBounds(rightOpenClose.left + rightOpenClose.width + kBetweenGap, openCloseTop, width, height);
  { buttons in middle }
  with close do setBounds(midWidth - width div 2, intMax(0, self.clientHeight - height - kBetweenGap), width, height);
  with helpButton do setBounds(close.left, intMax(0, close.top - height - kBetweenGap), width, height);
  with redo do setBounds(close.left, intMax(0, helpButton.top - height - kBetweenGap), width, height);
  with undo do setBounds(close.left, intMax(0, redo.top - height - kBetweenGap), width, height);
  with rename do setBounds(close.left, intMax(0, undo.top - height - kBetweenGap), width, height);
  with delete do setBounds(close.left, intMax(0, rename.top - height - kBetweenGap), width, height);
  with duplicate do setBounds(close.left, intMax(0, delete.top - height - kBetweenGap), width, height);
  with paste do setBounds(close.left, intMax(0, duplicate.top - height - kBetweenGap), width, height);
  with copy do setBounds(close.left, intMax(0, paste.top - height - kBetweenGap), width, height);
  with cut do setBounds(close.left, intMax(0, copy.top - height - kBetweenGap), width, height);
  with transfer do setBounds(close.left, intMax(0, cut.top - height - kBetweenGap), width, height);
  with previewImage do setBounds(listBoxWidth + kBetweenGap * 2, kBetweenGap,
    intMax(0, self.clientWidth - listBoxWidth * 2 - kBetweenGap * 4), transfer.top - kBetweenGap * 2);
  self.resizePreviewImage;
  end;

procedure TMoverForm.resizePreviewImage;
  var
    i: smallint;
    manager: PdPlantManager;
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
  // must invalidate preview cache for both sets of plants
  manager := self.selectedManager(kThisManager);
  if manager.plants.count > 0 then for i := 0 to manager.plants.count - 1 do
    PdPlant(manager.plants.items[i]).previewCacheUpToDate := false;
  manager := self.selectedManager(kOtherManager);
  if manager.plants.count > 0 then for i := 0 to manager.plants.count - 1 do
    PdPlant(manager.plants.items[i]).previewCacheUpToDate := false;
  self.drawPreview(focusedPlant);
  end;

procedure TMoverForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 400;
    ptMinTrackSize.y := 420;
    end;
  end;

{ ----------------------------------------------------------------------------------------- command list }
procedure TMoverForm.clearCommandList;
  begin
  commandList.free;
  commandList := nil;
  commandList := PdCommandList.create;
  self.updateButtonsForUndoRedo;
  end;

procedure TMoverForm.doCommand(command: PdCommand);
	begin
  commandList.doCommand(command);
  self.updateButtonsForUndoRedo;
  self.updateForChangeToSelectedPlants;
  end;

{ ------------------------------------------------------------------------------ *commands }
{ ------------------------------------------------------------------- PdMoverRenameCommand }
constructor PdMoverRenameCommand.createWithPlantNewNameAndManager(aPlant: PdPlant; aNewName: string;
    aManager: PdPlantManager);
  begin
  inherited create;
  commandChangesPlantFile := false;
  plant := aPlant;
  oldName := plant.getName;
  newName := aNewName;
  manager := aManager;
  managerChangedBeforeCommand := MoverForm.managerHasChanged(manager);
  end;

procedure PdMoverRenameCommand.doCommand;
  begin
  inherited doCommand; {not redo}
  plant.setName(newName);
  MoverForm.setChangedFlagForPlantManager(true, manager);
  end;

procedure PdMoverRenameCommand.undoCommand;
  begin
  inherited undoCommand;
  plant.setName(oldName);
  MoverForm.setChangedFlagForPlantManager(managerChangedBeforeCommand, manager);
  end;

function PdMoverRenameCommand.description: string;
	begin
  result := 'rename';
  end;

{ ----------------------------------------------------------------------- PdMoverRemoveCommand }
constructor PdMoverRemoveCommand.createWithListOfPlantsManagerAndClipboardFlag(aList: TList;
    aManager: PdPlantManager; aCopyToClipboard: boolean);
  begin
  inherited createWithListOfPlants(aList);
  commandChangesPlantFile := false;
  manager := aManager;
  managerChangedBeforeCommand := MoverForm.managerHasChanged(manager);
  copyToClipboard := aCopyToClipboard;
  removedPlants := TList.create;
  end;

destructor PdMoverRemoveCommand.destroy;
  var
    i: smallint;
  begin
  { free copies of cut plants if change was done }
  if (done) and (removedPlants <> nil) and (removedPlants.count > 0) then
    for i := 0 to removedPlants.count - 1 do
    	begin
    	plant := PdPlant(removedPlants.items[i]);
    	plant.free;
    	end;
  removedPlants.free;
  removedPlants := nil;
  inherited destroy;
  end;

procedure PdMoverRemoveCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; {not redo}
  if plantList.count <= 0 then exit;
  { copy plants }
  if copyToClipboard then
    MoverForm.copySelectedPlantsToClipboard;
  { save copy of plants before deleting }
  removedPlants.clear;
  { don't remove plants from manager until all indexes have been recorded }
  for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    removedPlants.add(plant);
    plant.indexWhenRemoved := manager.plants.indexOf(plant);
    plant.selectedIndexWhenRemoved := MoverForm.selectedPlants.indexOf(plant);
    end;
  for i := 0 to plantList.count - 1 do
    manager.plants.remove(PdPlant(plantList.items[i]));
  for i := 0 to plantList.count - 1 do
    MoverForm.selectedPlants.remove(PdPlant(plantList.items[i]));
  MoverForm.updatePlantListForManager(manager);
  MoverForm.setChangedFlagForPlantManager(true, manager);
  end;

procedure PdMoverRemoveCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if removedPlants.count > 0 then
    begin
    for i := 0 to removedPlants.count - 1 do
      begin
      plant := PdPlant(removedPlants.items[i]);
      if (plant.indexWhenRemoved >= 0) and (plant.indexWhenRemoved <= manager.plants.count - 1) then
        manager.plants.insert(plant.indexWhenRemoved, plant)
      else
        manager.plants.add(plant);
      { all removed plants must have been selected, so also add them to the selected list }
      if (plant.selectedIndexWhenRemoved >= 0)
          and (plant.selectedIndexWhenRemoved <= MoverForm.selectedPlants.count - 1) then
        MoverForm.selectedPlants.insert(plant.selectedIndexWhenRemoved, plant)
      else
        MoverForm.selectedPlants.add(plant);
      end;
    MoverForm.updatePlantListForManager(manager);
    MoverForm.setChangedFlagForPlantManager(managerChangedBeforeCommand, manager);
    end;
  end;

function PdMoverRemoveCommand.description: string;
	begin
  if copyToClipboard then
    result := 'cut'
  else
    result := 'delete';
  end;

{ ------------------------------------------------------------------ PdMoverPasteCommand }
constructor PdMoverPasteCommand.createWithListOfPlantsAndManager(aList: TList; aManager: PdPlantManager);
  begin
  inherited createWithListOfPlants(aList);
  commandChangesPlantFile := false;
  manager := aManager;
  managerChangedBeforeCommand := MoverForm.managerHasChanged(manager);
  end;

destructor PdMoverPasteCommand.destroy;
  var
    i: smallint;
  begin
  { free copies of pasted plants if change was undone }
  if (not done) and (plantList <> nil) and (plantList.count > 0) then
    for i := 0 to plantList.count - 1 do
    	begin
    	plant := PdPlant(plantList.items[i]);
    	plant.free;
    	end;
  inherited destroy; {will free plantList}
  end;

procedure PdMoverPasteCommand.doCommand;
  var
    i: smallint;
  begin
  inherited doCommand; {not redo}
  if plantList.count > 0 then
    begin
    MoverForm.deselectAllPlants;
    for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      manager.plants.add(plant);
      MoverForm.selectedPlants.add(plant);
      end;
    MoverForm.updatePlantListForManager(manager);
    MoverForm.setChangedFlagForPlantManager(true, manager);
    end;
  end;

procedure PdMoverPasteCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if plantList.count > 0 then
    begin
    for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      manager.plants.remove(plant);
      MoverForm.selectedPlants.remove(plant);
      end;
    MoverForm.updatePlantListForManager(manager);
    MoverForm.setChangedFlagForPlantManager(managerChangedBeforeCommand, manager);
    end;
  end;

function PdMoverPasteCommand.description: string;
	begin
  if self.isTransfer then
    result := 'transfer'
  else
    result := 'paste';
  end;

{ ------------------------------------------------------------------------------ PdMoverDuplicateCommand }
constructor PdMoverDuplicateCommand.createWithListOfPlantsAndManager(aList: TList; aManager: PdPlantManager);
  begin
  inherited createWithListOfPlants(aList);
  commandChangesPlantFile := false;
  newPlants := TList.create;
  manager := aManager;
  managerChangedBeforeCommand := MoverForm.managerHasChanged(manager);
  end;

destructor PdMoverDuplicateCommand.destroy;
  var
    i: smallint;
  begin
  { free copies of created plants if change was undone }
  if (not done) and (newPlants <> nil) and (newPlants.count > 0) then
    for i := 0 to newPlants.count - 1 do
    	begin
    	plant := PdPlant(newPlants.items[i]);
    	plant.free;
    	end;
  newPlants.free;
  newPlants := nil;
  inherited destroy; {will free plantList}
  end;

procedure PdMoverDuplicateCommand.doCommand;
  var
    i: smallint;
    plantCopy: PdPlant;
  begin
  inherited doCommand;
  if plantList.count > 0 then
    begin
    MoverForm.deselectAllPlants;
    for i := 0 to plantList.count - 1 do
      begin
      plant := PdPlant(plantList.items[i]);
      plantCopy := PdPlant.create;
      plant.copyTo(plantCopy);
      plantCopy.setName('Copy of ' + plantCopy.getName);
      newPlants.add(plantCopy);
      manager.plants.add(plantCopy);
      MoverForm.selectedPlants.add(plantCopy);
      end;
    MoverForm.updatePlantListForManager(manager);
    MoverForm.setChangedFlagForPlantManager(true, manager);
    end;
  end;

procedure PdMoverDuplicateCommand.undoCommand;
  var
    i: smallint;
  begin
  inherited undoCommand;
  if newPlants.count > 0 then
    begin
    for i := 0 to newPlants.count - 1 do
      begin
      plant := PdPlant(newPlants.items[i]);
      manager.plants.remove(plant);
      MoverForm.selectedPlants.remove(plant);
      end;
    MoverForm.updatePlantListForManager(manager);
    MoverForm.setChangedFlagForPlantManager(managerChangedBeforeCommand, manager);
    end;
  end;

procedure PdMoverDuplicateCommand.redoCommand;
  var
    i: smallint;
  begin
  inherited doCommand; {not redo}
  if newPlants.count > 0 then
    begin
    MoverForm.deselectAllPlants;
    for i := 0 to newPlants.count - 1 do
      begin
      plant := PdPlant(newPlants.items[i]);
      manager.plants.add(plant);
      MoverForm.selectedPlants.add(plant);
      end;
    MoverForm.updatePlantListForManager(manager);
    MoverForm.setChangedFlagForPlantManager(true, manager);
    end;
  end;

function PdMoverDuplicateCommand.description: string;
	begin
  result := 'duplicate';
  end;

procedure TMoverForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Using_the_plant_mover');
  end;

end.

(* tried this - big mess
procedure TMoverForm.drawDragItemLine(listBox: TListBox; y: integer);
  begin
  if listBox = leftPlantList then
    begin
    leftDragItemLastDrawY := y;
    self.drawOrUndrawDragItemLine(listBox, y);
    self.leftDragItemLineNeedToRedraw := true;
    end
  else
    begin
    rightDragItemLastDrawY := y;
    self.drawOrUndrawDragItemLine(listBox, y);
    self.rightDragItemLineNeedToRedraw := true;
    end;
  end;

procedure TMoverForm.undrawDragItemLine(listBox: TListBox);
  begin
  if listBox = leftPlantList then
    begin
    if not leftDragItemLineNeedToRedraw then exit;
    self.drawOrUndrawDragItemLine(listBox, leftDragItemLastDrawY);
    self.leftDragItemLineNeedToRedraw := false;
    end
  else
    begin
    if not rightDragItemLineNeedToRedraw then exit;
    self.drawOrUndrawDragItemLine(listBox, rightDragItemLastDrawY);
    self.rightDragItemLineNeedToRedraw := false;
    end;
  end;

procedure TMoverForm.drawOrUndrawDragItemLine(listBox: TListBox; y: integer);
  var
    theDC: HDC;
    drawRect: TRect;
  begin
  theDC := getDC(0);
  with drawRect do
    begin
    left := self.clientOrigin.x + listBox.left;
    right := self.clientOrigin.x + listBox.left + listBox.width;
    top := self.clientOrigin.y + listBox.top + y;
    end;
  with drawRect do
    patBlt(theDC, left, top, right - left, 1, dstInvert);
  releaseDC(0, theDC);
  end;

{ -------------------------------------------------------------------------------------------- *up and down }
procedure TMoverForm.moveItemsUpOrDown(listBox: TListBox; y: integer);
  var
    rows, i: integer;
  begin
  if self.dragItemsY <> 0 then
    begin
    rows := abs(y - self.dragItemsY) div listBox.itemHeight;
    if rows > 0 then
      begin
      if (y - self.dragItemsY) > 0 then
        for i := 0 to rows - 1 do self.moveItemsDown(listBox)
      else
        for i := 0 to rows - 1 do self.moveItemsUp(listBox);
      end;
    self.dragItemsY := y;
    end;
  end;

procedure TMoverForm.moveItemsDown(listBox: TListBox);
  var
    i: integer;
  begin
  if listBox.items.count > 1 then
    begin
    i := listBox.items.count - 2;  { start at next to last one because you can't move last one down any more }
    while i >= 0 do
      begin
      if listBox.selected[i] then
        begin
        listBox.items.move(i, i + 1);
        listBox.selected[i+1] := true;
        end;
      dec(i);
      end;
    end;
  end;

procedure TMoverForm.moveItemsUp(listBox: TListBox);
  var
    i: integer;
  begin
  if listBox.items.count > 1 then
    begin
    i := 1;  { start at 1 because you can't move first one up any more }
    while i <= listBox.items.count - 1 do
      begin
      if listBox.selected[i] then
        begin
        listBox.items.move(i, i - 1);
        listBox.selected[i-1] := true;
        end;
      inc(i);
      end;
    end;
  end;

*)
