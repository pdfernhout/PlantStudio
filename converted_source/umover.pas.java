// unit Umover

from conversion_common import *;
import ubmpsupport;
import ucursor;
import updform;
import uplantmn;
import delphi_compatability;

// const
kLeft = 0;
kRight = 1;
kNewPlantFileName = "untitled.pla";
kThisManager = true;
kOtherManager = false;


// var
TMoverForm MoverForm = new TMoverForm();


// const
kBetweenGap = 4;



class TMoverForm extends PdForm {
    public TEdit leftPlantFileNameEdit;
    public TButton leftOpenClose;
    public TEdit rightPlantFileNameEdit;
    public TButton rightOpenClose;
    public TButton newFile;
    public TButton transfer;
    public TButton close;
    public TImage previewImage;
    public TButton undo;
    public TButton redo;
    public TButton cut;
    public TButton copy;
    public TButton paste;
    public TButton rename;
    public TButton duplicate;
    public TButton delete;
    public TImage leftPlantFileChangedIndicator;
    public TImage rightPlantFileChangedIndicator;
    public TDrawGrid leftPlantList;
    public TDrawGrid rightPlantList;
    public TSpeedButton helpButton;
    public String leftPlantFileName;
    public String rightPlantFileName;
    public PdPlantManager leftManager;
    public PdPlantManager rightManager;
    public boolean leftPlantFileChanged;
    public boolean rightPlantFileChanged;
    public int lastLeftSingleClickPlantIndex;
    public int lastRightSingleClickPlantIndex;
    public short leftOrRight;
    public boolean changedCurrentPlantFile;
    public PdCommandList commandList;
    public TList selectedPlants;
    public String untitledDomainFileSavedAs;
    public int dragItemsY;
    public boolean justDoubleClickedOnLeftGrid;
    public boolean justDoubleClickedOnRightGrid;
    
    //$R *.DFM
    // -------------------------------------------------------------------------------------------- *creation/destruction 
    public void create(TComponent AOwner) {
        super.create(AOwner);
        MoverForm = this;
        this.leftManager = uplantmn.PdPlantManager().create();
        this.rightManager = uplantmn.PdPlantManager().create();
        this.commandList = UNRESOLVED.PdCommandList.create;
        this.selectedPlants = delphi_compatability.TList().Create();
        this.commandList.setNewUndoLimit(UNRESOLVED.domain.options.undoLimit);
        this.commandList.setNewObjectUndoLimit(UNRESOLVED.domain.options.undoLimitOfPlants);
        this.updateButtonsForUndoRedo();
        if (len(UNRESOLVED.domain.plantFileName) > 0) {
            // load current plant file into left side to start 
            this.openPlantFileForManager(this.leftManager, UNRESOLVED.domain.plantFileName);
        } else {
            this.closePlantFileForManager(this.leftManager);
        }
        // right side is empty to start 
        this.closePlantFileForManager(this.rightManager);
        this.updatePasteButtonForClipboardContents();
    }
    
    public void FormCreate(TObject Sender) {
        this.leftPlantList.DragCursor = ucursor.crDragPlant;
        this.rightPlantList.DragCursor = ucursor.crDragPlant;
    }
    
    public void destroy() {
        this.leftManager.free;
        this.leftManager = null;
        this.rightManager.free;
        this.rightManager = null;
        this.selectedPlants.free;
        this.selectedPlants = null;
        this.commandList.free;
        this.commandList = null;
        super.destroy();
    }
    
    public void FormClose(TObject Sender, TCloseAction Action) {
        if (this.ModalResult == mrOK) {
            return;
        }
        // same as exit, but can't call exit because we have to set the action flag 
        Action = delphi_compatability.TCloseAction.caNone;
        if (!this.askToSaveManagerAndProceed(this.leftManager)) {
            return;
        }
        if (!this.askToSaveManagerAndProceed(this.rightManager)) {
            return;
        }
        Action = delphi_compatability.TCloseAction.caFree;
    }
    
    public void FormKeyDown(TObject Sender, byte Key, TShiftState Shift) {
        switch (Key) {
            case delphi_compatability.VK_DELETE:
                this.deleteClick(this);
                break;
        if (!(delphi_compatability.TShiftStateEnum.ssCtrl in Shift)) {
            return Key;
        }
        switch (Character(Key)) {
            case "C":
                this.copyClick(this);
                Key = 0;
                break;
            case "c":
                this.copyClick(this);
                Key = 0;
                break;
            case "X":
                this.cutClick(this);
                Key = 0;
                break;
            case "x":
                this.cutClick(this);
                Key = 0;
                break;
            case "V":
                this.pasteClick(this);
                Key = 0;
                break;
            case "v":
                this.pasteClick(this);
                Key = 0;
                break;
            case "Z":
                if (delphi_compatability.TShiftStateEnum.ssShift in Shift) {
                    this.redoClick(this);
                } else {
                    this.undoClick(this);
                }
                Key = 0;
                break;
            case "z":
                if (delphi_compatability.TShiftStateEnum.ssShift in Shift) {
                    this.redoClick(this);
                } else {
                    this.undoClick(this);
                }
                Key = 0;
                break;
        return Key;
    }
    
    // ----------------------------------------------------------------------------------------- *buttons 
    public void undoClick(TObject Sender) {
        this.commandList.undoLast;
        this.updateButtonsForUndoRedo();
        this.updateForChangeToSelectedPlants();
    }
    
    public void redoClick(TObject Sender) {
        this.commandList.redoLast;
        this.updateButtonsForUndoRedo();
        this.updateForChangeToSelectedPlants();
    }
    
    public void cutClick(TObject Sender) {
        PdPlantManager manager = new PdPlantManager();
        PdCommand newCommand = new PdCommand();
        
        manager = this.selectedManager(kThisManager);
        if ((manager == null) || (this.selectedPlants.Count <= 0)) {
            return;
        }
        newCommand = PdMoverRemoveCommand().createWithListOfPlantsManagerAndClipboardFlag(this.selectedPlants, manager, UNRESOLVED.kCopyToClipboard);
        this.doCommand(newCommand);
    }
    
    public void copyClick(TObject Sender) {
        this.copySelectedPlantsToClipboard();
    }
    
    public void pasteClick(TObject Sender) {
        PdPlantManager manager = new PdPlantManager();
        PdCommand newCommand = new PdCommand();
        TList newPlants = new TList();
        
        manager = this.selectedManager(kThisManager);
        if (manager == null) {
            return;
        }
        newPlants = delphi_compatability.TList().Create();
        UNRESOLVED.domain.plantManager.pastePlantsFromPrivatePlantClipboardToList(newPlants);
        newCommand = PdMoverPasteCommand().createWithListOfPlantsAndManager(newPlants, manager);
        this.doCommand(newCommand);
        //command has its own list, so we need to free this one
        newPlants.free;
    }
    
    public void closeClick(TObject Sender) {
        if (!this.askToSaveManagerAndProceed(this.leftManager)) {
            return;
        }
        if (!this.askToSaveManagerAndProceed(this.rightManager)) {
            return;
        }
        // cannot cancel 
        this.ModalResult = mrOK;
    }
    
    public void leftOpenCloseClick(TObject Sender) {
        if (this.haveLeftFile()) {
            //file open
            //no file
            this.closePlantFileForManager(this.leftManager);
        } else {
            this.openPlantFileForManager(this.leftManager, "");
        }
    }
    
    public void rightOpenCloseClick(TObject Sender) {
        if (this.haveRightFile()) {
            //file open
            //no file
            this.closePlantFileForManager(this.rightManager);
        } else {
            this.openPlantFileForManager(this.rightManager, "");
        }
    }
    
    public void newFileClick(TObject Sender) {
        this.newPlantFileForManager(this.rightManager);
    }
    
    public void transferClick(TObject Sender) {
        PdPlantManager manager = new PdPlantManager();
        PdPlantManager otherManager = new PdPlantManager();
        PdCommand newCommand = new PdCommand();
        TList newPlants = new TList();
        PdPlant plant = new PdPlant();
        PdPlant newPlant = new PdPlant();
        short i = 0;
        
        manager = this.selectedManager(kThisManager);
        otherManager = this.selectedManager(kOtherManager);
        if ((manager == null) || (otherManager == null) || (this.selectedPlants.Count <= 0)) {
            return;
        }
        if (this.selectedPlants.Count > 0) {
            //command will free
            newPlants = delphi_compatability.TList().Create();
            for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                plant = UNRESOLVED.PdPlant(this.selectedPlants.Items[i]);
                newPlant = UNRESOLVED.PdPlant.create;
                plant.copyTo(newPlant);
                newPlants.Add(newPlant);
            }
            newCommand = PdMoverPasteCommand().createWithListOfPlantsAndManager(newPlants, otherManager);
            ((PdMoverPasteCommand)newCommand).isTransfer = true;
            this.doCommand(newCommand);
            //command has its own list, so we need to free this one
            newPlants.free;
        }
    }
    
    public void duplicateClick(TObject Sender) {
        PdPlantManager manager = new PdPlantManager();
        PdCommand newCommand = new PdCommand();
        
        manager = this.selectedManager(kThisManager);
        if ((manager == null) || (this.selectedPlants.Count <= 0)) {
            return;
        }
        newCommand = PdMoverDuplicateCommand().createWithListOfPlantsAndManager(this.selectedPlants, manager);
        this.doCommand(newCommand);
    }
    
    public void renameClick(TObject Sender) {
        PdPlant plant = new PdPlant();
        PdPlantManager manager = new PdPlantManager();
        ansistring newName = new ansistring();
        PdCommand newCommand = new PdCommand();
        
        // can only rename one plant at a time 
        manager = this.selectedManager(kThisManager);
        plant = this.focusedPlant();
        if ((plant == null) || (manager == null)) {
            return;
        }
        newName = plant.getName;
        if (!InputQuery("Enter new name", "Type a new name for " + newName + ".", newName)) {
            return;
        }
        newCommand = PdMoverRenameCommand().createWithPlantNewNameAndManager(plant, newName, manager);
        this.doCommand(newCommand);
    }
    
    public void deleteClick(TObject Sender) {
        PdPlantManager manager = new PdPlantManager();
        PdCommand newCommand = new PdCommand();
        
        manager = this.selectedManager(kThisManager);
        if ((manager == null) || (this.selectedPlants.Count <= 0)) {
            return;
        }
        newCommand = PdMoverRemoveCommand().createWithListOfPlantsManagerAndClipboardFlag(this.selectedPlants, manager, UNRESOLVED.kDontCopyToClipboard);
        this.doCommand(newCommand);
    }
    
    // -------------------------------------------------------------------------------------- *list box actions 
    public void leftPlantListDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        this.drawLineInGrid(this.leftPlantList, this.leftManager, Row, Rect, State);
    }
    
    public void rightPlantListDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        this.drawLineInGrid(this.rightPlantList, this.rightManager, Row, Rect, State);
    }
    
    public void drawLineInGrid(TDrawGrid grid, PdPlantManager manager, int index, TRect rect, TGridDrawState state) {
        PdPlant plant = new PdPlant();
        boolean selected = false;
         cText = [0] * (range(0, 255 + 1) + 1);
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        grid.Canvas.Brush.Color = grid.Color;
        grid.Canvas.FillRect(Rect);
        if ((manager.plants.count <= 0) || (index < 0) || (index > manager.plants.count - 1)) {
            return;
        }
        // set up plant pointer 
        plant = UNRESOLVED.PdPlant(manager.plants.items[index]);
        if (plant == null) {
            return;
        }
        selected = this.selectedPlants.IndexOf(plant) >= 0;
        grid.Canvas.Font = grid.Font;
        if (selected) {
            grid.Canvas.Brush.Color = UNRESOLVED.clHighlight;
            grid.Canvas.Font.Color = UNRESOLVED.clHighlightText;
        } else {
            grid.Canvas.Brush.Color = grid.Color;
            grid.Canvas.Font.Color = UNRESOLVED.clBtnText;
        }
        grid.Canvas.FillRect(Rect);
        UNRESOLVED.strPCopy(cText, plant.getName);
        // margin for text 
        Rect.left = Rect.left + 2;
        UNRESOLVED.winprocs.drawText(grid.Canvas.Handle, cText, len(cText), Rect, delphi_compatability.DT_LEFT);
        if (plant == this.focusedPlant()) {
            // put back 
            Rect.left = Rect.left - 2;
            UNRESOLVED.drawFocusRect(Rect);
        }
    }
    
    // left list mouse handling
    public void leftPlantListMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        int col = 0;
        int row = 0;
        
        if (this.justDoubleClickedOnLeftGrid) {
            this.justDoubleClickedOnLeftGrid = false;
            return;
        } else {
            this.justDoubleClickedOnLeftGrid = false;
        }
        if (this.leftManager.plants.count > 0) {
            if (this.leftOrRight == kRight) {
                this.selectedPlants.Clear();
                this.lastRightSingleClickPlantIndex = -1;
                this.rightPlantList.Invalidate();
            }
            this.leftOrRight = kLeft;
            col, row = this.leftPlantList.MouseToCell(X, Y, col, row);
            this.selectPlantAtIndex(Shift, row);
            this.updateForChangeToSelectedPlants();
            this.leftPlantList.BeginDrag(false);
        }
    }
    
    public void leftPlantListDragOver(TObject Sender, TObject Source, int X, int Y, TDragState State, boolean Accept) {
        Accept = (Source != null) && (Sender != null);
        if (Source == this.rightPlantList) {
            Accept = Accept && this.haveLeftFile();
        } else {
            Accept = Accept && (Source == Sender);
        }
        return Accept;
    }
    
    public void leftPlantListEndDrag(TObject Sender, TObject Target, int X, int Y) {
        if ((Target == this.rightPlantList)) {
            this.transferClick(this);
        }
    }
    
    public void leftPlantListDblClick(TObject Sender) {
        this.renameClick(this);
        this.leftPlantList.endDrag(false);
        this.justDoubleClickedOnLeftGrid = true;
    }
    
    // right list mouse handling
    public void rightPlantListMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        int col = 0;
        int row = 0;
        
        if (this.justDoubleClickedOnRightGrid) {
            this.justDoubleClickedOnRightGrid = false;
            return;
        } else {
            this.justDoubleClickedOnRightGrid = false;
        }
        if (this.rightManager.plants.count > 0) {
            if (this.leftOrRight == kLeft) {
                this.selectedPlants.Clear();
                this.lastLeftSingleClickPlantIndex = -1;
                this.leftPlantList.Invalidate();
            }
            this.leftOrRight = kRight;
            col, row = this.rightPlantList.MouseToCell(X, Y, col, row);
            this.selectPlantAtIndex(Shift, row);
            this.updateForChangeToSelectedPlants();
            this.rightPlantList.BeginDrag(false);
        }
    }
    
    public void rightPlantListDragOver(TObject Sender, TObject Source, int X, int Y, TDragState State, boolean Accept) {
        Accept = (Source != null) && (Sender != null);
        if (Source == this.leftPlantList) {
            Accept = Accept && this.haveRightFile();
        } else {
            Accept = Accept && (Source == Sender);
        }
        return Accept;
    }
    
    public void rightPlantListEndDrag(TObject Sender, TObject Target, int X, int Y) {
        if ((Target == this.leftPlantList)) {
            this.transferClick(this);
        }
    }
    
    public void rightPlantListDblClick(TObject Sender) {
        this.renameClick(this);
        this.rightPlantList.endDrag(false);
        this.justDoubleClickedOnRightGrid = true;
    }
    
    public void selectPlantAtIndex(TShiftState Shift, int index) {
        short i = 0;
        PdPlant plant = new PdPlant();
        PdPlantManager manager = new PdPlantManager();
        int lastSingleClickPlantIndex = 0;
        int lastRow = 0;
        TDrawGrid grid = new TDrawGrid();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        manager = this.selectedManager(kThisManager);
        if (manager == null) {
            return;
        }
        if ((index < 0)) {
            this.selectedPlants.Clear();
            this.redrawSelectedGrid();
            return;
        }
        plant = UNRESOLVED.PdPlant(manager.plants.items[index]);
        if (plant == null) {
            return;
        }
        if ((delphi_compatability.TShiftStateEnum.ssCtrl in Shift)) {
            if (this.selectedPlants.IndexOf(plant) >= 0) {
                this.selectedPlants.Remove(plant);
            } else {
                this.selectedPlants.Add(plant);
            }
        } else if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
            if (this.leftOrRight == kLeft) {
                lastSingleClickPlantIndex = this.lastLeftSingleClickPlantIndex;
            } else {
                lastSingleClickPlantIndex = this.lastRightSingleClickPlantIndex;
            }
            if ((lastSingleClickPlantIndex >= 0) && (lastSingleClickPlantIndex <= manager.plants.count - 1) && (lastSingleClickPlantIndex != index)) {
                if (lastSingleClickPlantIndex < index) {
                    for (i = lastSingleClickPlantIndex; i <= index; i++) {
                        if (this.selectedPlants.IndexOf(manager.plants.items[i]) < 0) {
                            this.selectedPlants.Add(manager.plants.items[i]);
                        }
                    }
                } else if (lastSingleClickPlantIndex > index) {
                    for (i = lastSingleClickPlantIndex; i >= index; i--) {
                        if (this.selectedPlants.IndexOf(manager.plants.items[i]) < 0) {
                            this.selectedPlants.Add(manager.plants.items[i]);
                        }
                    }
                }
            }
            // just a click
        } else {
            if (this.selectedPlants.IndexOf(plant) <= 0) {
                this.selectedPlants.Clear();
                this.redrawSelectedGrid();
                this.selectedPlants.Add(plant);
                if (this.leftOrRight == kLeft) {
                    this.lastLeftSingleClickPlantIndex = index;
                } else {
                    this.lastRightSingleClickPlantIndex = index;
                }
                grid = this.gridForManager(manager);
                if (grid == null) {
                    return;
                }
                lastRow = grid.TopRow + grid.VisibleRowCount - 1;
                if (index > lastRow) {
                    grid.TopRow = grid.TopRow + (index - lastRow);
                }
                if (index < grid.TopRow) {
                    grid.TopRow = index;
                }
            }
        }
        this.redrawSelectedGrid();
    }
    
    public void leftPlantListKeyDown(TObject Sender, byte Key, TShiftState Shift) {
        Key = this.listKeyDown(Key, Shift);
        return Key;
    }
    
    public void rightPlantListKeyDown(TObject Sender, byte Key, TShiftState shift) {
        Key = this.listKeyDown(Key, shift);
        return Key;
    }
    
    public void listKeyDown(byte Key, TShiftState Shift) {
        switch (Key) {
            case delphi_compatability.VK_DOWN:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.moveSelectedPlantsDown();
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKey(this.focusedPlantIndexInManager() + 1);
                }
                break;
            case delphi_compatability.VK_RIGHT:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.moveSelectedPlantsDown();
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKey(this.focusedPlantIndexInManager() + 1);
                }
                break;
            case delphi_compatability.VK_UP:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.moveSelectedPlantsUp();
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKey(this.focusedPlantIndexInManager() - 1);
                }
                break;
            case delphi_compatability.VK_LEFT:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.moveSelectedPlantsUp();
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKey(this.focusedPlantIndexInManager() - 1);
                }
                break;
            case delphi_compatability.VK_RETURN:
                Key = 0;
                this.renameClick(this);
                break;
        return Key;
    }
    
    public void moveUpOrDownWithKey(short indexAfterMove) {
        PdPlantManager manager = new PdPlantManager();
        
        manager = this.selectedManager(kThisManager);
        if (manager == null) {
            return;
        }
        if (indexAfterMove > manager.plants.count - 1) {
            // loop around 
            indexAfterMove = 0;
        }
        if (indexAfterMove < 0) {
            indexAfterMove = manager.plants.count - 1;
        }
        if ((indexAfterMove >= 0) && (indexAfterMove <= manager.plants.count - 1)) {
            this.deselectAllPlants();
            //no shift
            this.selectPlantAtIndex({}, indexAfterMove);
            this.drawPreview(this.focusedPlant());
        }
    }
    
    public void moveSelectedPlantsDown() {
        PdPlantManager manager = new PdPlantManager();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        manager = this.selectedManager(kThisManager);
        if (manager == null) {
            return;
        }
        if (manager.plants.count > 1) {
            // start at next to last one because you can't move last one down any more 
            i = manager.plants.count - 2;
            while (i >= 0) {
                plant = UNRESOLVED.PdPlant(manager.plants.items[i]);
                if (this.selectedPlants.IndexOf(plant) >= 0) {
                    manager.plants.move(i, i + 1);
                }
                i -= 1;
            }
        }
        this.redrawSelectedGrid();
        // reordering makes change flag true
        this.setChangedFlagForPlantManager(true, this.selectedManager(kThisManager));
    }
    
    public void moveSelectedPlantsUp() {
        PdPlantManager manager = new PdPlantManager();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        manager = this.selectedManager(kThisManager);
        if (manager == null) {
            return;
        }
        if (manager.plants.count > 1) {
            // start at 1 because you can't move first one up any more 
            i = 1;
            while (i <= manager.plants.count - 1) {
                plant = UNRESOLVED.PdPlant(manager.plants.items[i]);
                if (this.selectedPlants.IndexOf(plant) >= 0) {
                    manager.plants.move(i, i - 1);
                }
                i += 1;
            }
        }
        this.redrawSelectedGrid();
        // reordering makes change flag true
        this.setChangedFlagForPlantManager(true, this.selectedManager(kThisManager));
    }
    
    public void redrawSelectedGrid() {
        if (this.leftOrRight == kLeft) {
            this.leftPlantList.Invalidate();
        } else {
            this.rightPlantList.Invalidate();
        }
    }
    
    // -------------------------------------------------------------------------------------------- *updating 
    public void updateForNewFile(String newFileName, PdPlantManager manager) {
        this.clearCommandList();
        this.setFileNameForManager(newFileName, manager);
        this.updatePlantListForManager(manager);
        this.setChangedFlagForPlantManager(false, manager);
        this.deselectAllPlants();
        if (newFileName != "") {
            if (manager == this.leftManager) {
                this.leftOrRight = kLeft;
            } else {
                this.leftOrRight = kRight;
            }
        }
        this.updateForChangeToSelectedPlants();
    }
    
    public void deselectAllPlants() {
        this.selectedPlants.Clear();
        this.redrawSelectedGrid();
    }
    
    public void updatePasteButtonForClipboardContents() {
        this.paste.Enabled = (UNRESOLVED.domain.plantManager.privatePlantClipboard.count > 0);
    }
    
    public String leftRightString(String leftString, String rightString) {
        result = "";
        if (this.leftOrRight == kLeft) {
            result = leftString;
        } else {
            result = rightString;
        }
        return result;
    }
    
    public void updateForChangeToSelectedPlants() {
        boolean atLeastOnePlantSelected = false;
        boolean atLeastOneFile = false;
        
        this.leftPlantList.Invalidate();
        this.rightPlantList.Invalidate();
        if (this.leftOrRight == kLeft) {
            if (this.haveLeftFile()) {
                this.leftOpenClose.Caption = "&Close";
            } else {
                this.leftOpenClose.Caption = "&Open...";
            }
            this.leftPlantFileNameEdit.Color = delphi_compatability.clAqua;
            this.leftPlantFileNameEdit.Refresh();
            this.rightPlantFileNameEdit.Color = UNRESOLVED.clBtnFace;
            this.rightPlantFileNameEdit.Refresh();
            this.drawPreview(this.focusedPlant());
        } else {
            if (this.haveRightFile()) {
                this.rightOpenClose.Caption = "&Close";
            } else {
                this.rightOpenClose.Caption = "&Open...";
            }
            this.leftPlantFileNameEdit.Color = UNRESOLVED.clBtnFace;
            this.leftPlantFileNameEdit.Refresh();
            this.rightPlantFileNameEdit.Color = delphi_compatability.clAqua;
            this.rightPlantFileNameEdit.Refresh();
            this.drawPreview(this.focusedPlant());
        }
        atLeastOneFile = this.haveLeftFile() || this.haveRightFile();
        atLeastOnePlantSelected = (this.selectedPlants.Count > 0);
        this.transfer.Enabled = this.haveLeftFile() && this.haveRightFile() && atLeastOnePlantSelected;
        this.transfer.Caption = this.leftRightString("&Transfer >>", "<< &Transfer");
        this.cut.Enabled = atLeastOneFile && atLeastOnePlantSelected;
        this.copy.Enabled = atLeastOneFile && atLeastOnePlantSelected;
        this.duplicate.Enabled = atLeastOneFile && atLeastOnePlantSelected;
        this.delete.Enabled = atLeastOneFile && atLeastOnePlantSelected;
        this.rename.Enabled = atLeastOneFile && atLeastOnePlantSelected;
    }
    
    public void updateButtonsForUndoRedo() {
        if (this.commandList.isUndoEnabled) {
            this.undo.Enabled = true;
            this.undo.Caption = "Undo " + this.commandList.undoDescription;
        } else {
            this.undo.Enabled = false;
            this.undo.Caption = "Can't undo";
        }
        if (this.commandList.isRedoEnabled) {
            this.redo.Enabled = true;
            this.redo.Caption = "Redo " + this.commandList.redoDescription;
        } else {
            this.redo.Enabled = false;
            this.redo.Caption = "Can't redo";
        }
    }
    
    public void updatePlantListForManager(PdPlantManager manager) {
        TDrawGrid grid = new TDrawGrid();
        
        grid = this.gridForManager(manager);
        if (grid == null) {
            return;
        }
        grid.RowCount = manager.plants.count;
        grid.Invalidate();
    }
    
    public void drawPreview(PdPlant plant) {
        if (plant == null) {
            this.previewImage.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
            this.previewImage.Canvas.Brush.Color = delphi_compatability.clWindow;
        } else {
            if (!plant.previewCacheUpToDate) {
                try {
                    ucursor.cursor_startWait();
                    plant.drawPreviewIntoCache(Point(this.previewImage.Width, this.previewImage.Height), UNRESOLVED.kDontConsiderDomainScale, UNRESOLVED.kDrawNow);
                } finally {
                    ucursor.cursor_stopWait();
                }
            }
            plant.previewCache.transparent = false;
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(plant.previewCache, this.previewImage.Canvas, Rect(0, 0, 0, 0));
            UNRESOLVED.realizePalette(this.previewImage.Canvas.Handle);
            this.previewImage.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        }
        this.previewImage.Canvas.Pen.Color = UNRESOLVED.clBtnText;
        this.previewImage.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid;
        this.previewImage.Canvas.Rectangle(0, 0, this.previewImage.Width, this.previewImage.Height);
    }
    
    // ------------------------------------------------------------------------------------------ *selecting 
    public PdPlant focusedPlant() {
        result = new PdPlant();
        result = null;
        if (this.selectedPlants.Count > 0) {
            result = UNRESOLVED.PdPlant(this.selectedPlants.Items[0]);
        }
        return result;
    }
    
    public short focusedPlantIndexInManager() {
        result = 0;
        PdPlantManager manager = new PdPlantManager();
        
        result = -1;
        manager = this.selectedManager(kThisManager);
        if (manager == null) {
            return result;
        }
        if (this.selectedPlants.Count > 0) {
            result = manager.plants.indexOf(this.selectedPlants.Items[0]);
        }
        return result;
    }
    
    public boolean haveLeftFile() {
        result = false;
        result = len(this.leftPlantFileName) != 0;
        return result;
    }
    
    public boolean haveRightFile() {
        result = false;
        result = len(this.rightPlantFileName) != 0;
        return result;
    }
    
    public PdPlantManager selectedManager(boolean thisManager) {
        result = new PdPlantManager();
        result = null;
        if (this.leftOrRight == kLeft) {
            if (thisManager) {
                result = this.leftManager;
            } else {
                result = this.rightManager;
            }
        } else {
            if (thisManager) {
                result = this.rightManager;
            } else {
                result = this.leftManager;
            }
        }
        return result;
    }
    
    public String getFileNameForManager(PdPlantManager manager) {
        result = "";
        if (manager == this.leftManager) {
            result = this.leftPlantFileName;
        } else {
            result = this.rightPlantFileName;
        }
        return result;
    }
    
    public String getFileNameForOtherManager(PdPlantManager manager) {
        result = "";
        if (manager == this.rightManager) {
            result = this.leftPlantFileName;
        } else {
            result = this.rightPlantFileName;
        }
        return result;
    }
    
    public void setFileNameForManager(String newName, PdPlantManager manager) {
        if (manager == this.leftManager) {
            this.leftPlantFileName = newName;
            this.leftPlantFileNameEdit.Text = newName;
            this.leftPlantFileNameEdit.SelStart = len(newName);
        } else {
            this.rightPlantFileName = newName;
            this.rightPlantFileNameEdit.Text = newName;
            this.rightPlantFileNameEdit.SelStart = len(newName);
        }
    }
    
    public TDrawGrid gridForManager(PdPlantManager manager) {
        result = new TDrawGrid();
        result = null;
        if (manager == this.leftManager) {
            result = this.leftPlantList;
        } else if (manager == this.rightManager) {
            result = this.rightPlantList;
        }
        return result;
    }
    
    public boolean managerHasChanged(PdPlantManager manager) {
        result = false;
        if (manager == this.leftManager) {
            result = this.leftPlantFileChanged;
        } else {
            result = this.rightPlantFileChanged;
        }
        return result;
    }
    
    public void setChangedFlagForPlantManager(boolean value, PdPlantManager manager) {
        if (manager == this.leftManager) {
            this.leftPlantFileChanged = value;
            if (this.leftPlantFileChanged) {
                this.leftPlantFileChangedIndicator.Picture = UNRESOLVED.MainForm.fileChangedImage.picture;
            } else {
                this.leftPlantFileChangedIndicator.Picture = UNRESOLVED.MainForm.fileNotChangedImage.picture;
            }
        } else {
            this.rightPlantFileChanged = value;
            if (this.rightPlantFileChanged) {
                this.rightPlantFileChangedIndicator.Picture = UNRESOLVED.MainForm.fileChangedImage.picture;
            } else {
                this.rightPlantFileChangedIndicator.Picture = UNRESOLVED.MainForm.fileNotChangedImage.picture;
            }
        }
    }
    
    // ------------------------------------------------------------------------------------------- *copying 
    public PdPlant copyPlantToPlantManager(PdPlant plant, PdPlantManager toPlantManager) {
        result = new PdPlant();
        if (plant == null) {
            result = null;
        } else {
            result = toPlantManager.copyFromPlant(plant);
        }
        return result;
    }
    
    public void copySelectedPlantsToClipboard() {
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        UNRESOLVED.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(this.selectedPlants);
        this.updatePasteButtonForClipboardContents();
    }
    
    // ------------------------------------------------------------------------ *opening, closing and saving 
    public void openPlantFileForManager(PdPlantManager manager, String fileNameToStart) {
        String fileNameWithPath = "";
        
        if (!this.askToSaveManagerAndProceed(manager)) {
            return;
        }
        if (fileNameToStart == "") {
            fileNameWithPath = UNRESOLVED.getFileOpenInfo(UNRESOLVED.kFileTypePlant, UNRESOLVED.kNoSuggestedFile, "Choose a plant file");
        } else {
            fileNameWithPath = fileNameToStart;
        }
        if (fileNameWithPath == "") {
            this.updateForNewFile(fileNameWithPath, manager);
        } else {
            if (fileNameWithPath == this.getFileNameForOtherManager(manager)) {
                ShowMessage("The file you chose is already open on the other side.");
                return;
            }
            try {
                ucursor.cursor_startWait();
                if (FileExists(fileNameWithPath)) {
                    manager.loadPlantsFromFile(fileNameWithPath, UNRESOLVED.kInPlantMover);
                } else {
                    this.newPlantFileForManager(manager);
                }
                // PDF PORT -- added semicolon
                this.updateForNewFile(fileNameWithPath, manager);
            } finally {
                ucursor.cursor_stopWait();
            }
        }
    }
    
    public void closePlantFileForManager(PdPlantManager manager) {
        if (!this.askToSaveManagerAndProceed(manager)) {
            return;
        }
        manager.plants.clear;
        this.updateForNewFile("", manager);
    }
    
    public void newPlantFileForManager(PdPlantManager manager) {
        if (!this.askToSaveManagerAndProceed(manager)) {
            return;
        }
        manager.plants.clear;
        this.updateForNewFile(kNewPlantFileName, manager);
    }
    
    public void managerSaveOrSaveAs(PdPlantManager manager, boolean askForFileName) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        String fileName = "";
        boolean askForFileNameConsideringUntitled = false;
        
        fileName = this.getFileNameForManager(manager);
        if (fileName == kNewPlantFileName) {
            askForFileNameConsideringUntitled = true;
        } else {
            askForFileNameConsideringUntitled = askForFileName;
        }
        if (!UNRESOLVED.getFileSaveInfo(UNRESOLVED.kFileTypePlant, askForFileNameConsideringUntitled, fileName, fileInfo)) {
            return;
        }
        try {
            ucursor.cursor_startWait();
            manager.savePlantsToFile(fileInfo.tempFile, UNRESOLVED.kInPlantMover);
            fileInfo.writingWasSuccessful = true;
        } finally {
            ucursor.cursor_stopWait();
            UNRESOLVED.cleanUpAfterFileSave(fileInfo);
            this.updateForNewFile(kNewPlantFileName, manager);
            if ((fileInfo.newFile == UNRESOLVED.domain.plantFileName)) {
                this.changedCurrentPlantFile = true;
            }
            if ((fileName == kNewPlantFileName) && (UNRESOLVED.domain.plantFileName == kNewPlantFileName)) {
                // deal with case of: started mover with untitled file, changed file, returned
                this.changedCurrentPlantFile = true;
                this.untitledDomainFileSavedAs = fileInfo.newFile;
            }
        }
    }
    
    public boolean askToSaveManagerAndProceed(PdPlantManager manager) {
        result = false;
        byte response = 0;
        String prompt = "";
        
        // returns false if user cancelled action 
        result = true;
        if (!this.managerHasChanged(manager)) {
            return result;
        }
        prompt = "Save changes to " + ExtractFileName(this.getFileNameForManager(manager)) + "?";
        response = MessageDialog(prompt, mtConfirmation, mbYesNoCancel, 0);
        switch (response) {
            case mrYes:
                this.managerSaveOrSaveAs(manager, UNRESOLVED.kDontAskForFileName);
                break;
            case mrNo:
                result = true;
                break;
            case mrCancel:
                result = false;
                break;
        return result;
    }
    
    // ------------------------------------------------------------------------------------------ *resizing 
    public void FormResize(TObject Sender) {
        short midWidth = 0;
        short listBoxWidth = 0;
        short listBoxTop = 0;
        short openCloseTop = 0;
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.leftManager == null) {
            return;
        }
        if (this.rightManager == null) {
            return;
        }
        if (this.selectedPlants == null) {
            return;
        }
        midWidth = this.ClientWidth / 2;
        //same as right
        listBoxWidth = this.leftPlantList.Width;
        listBoxTop = kBetweenGap + this.leftPlantFileNameEdit.Height + kBetweenGap + this.leftOpenClose.Height + kBetweenGap;
        // list boxes 
        this.leftPlantList.SetBounds(kBetweenGap, listBoxTop, listBoxWidth, UNRESOLVED.intMax(0, this.ClientHeight - listBoxTop - kBetweenGap));
        this.leftPlantList.DefaultColWidth = this.leftPlantList.ClientWidth;
        this.rightPlantList.SetBounds(UNRESOLVED.intMax(0, this.ClientWidth - listBoxWidth - kBetweenGap), listBoxTop, listBoxWidth, UNRESOLVED.intMax(0, this.ClientHeight - listBoxTop - kBetweenGap));
        this.rightPlantList.DefaultColWidth = this.rightPlantList.ClientWidth;
        // edits and buttons at top 
        this.leftPlantFileNameEdit.SetBounds(kBetweenGap, kBetweenGap, listBoxWidth - kBetweenGap * 2, this.leftPlantFileNameEdit.Height);
        this.leftPlantFileChangedIndicator.SetBounds(kBetweenGap, this.leftPlantFileNameEdit.Top + this.leftPlantFileNameEdit.Height + kBetweenGap, this.leftPlantFileChangedIndicator.Width, this.leftPlantFileChangedIndicator.Height);
        this.rightPlantFileNameEdit.SetBounds(this.rightPlantList.Left, kBetweenGap, listBoxWidth - kBetweenGap * 2, this.rightPlantFileNameEdit.Height);
        this.rightPlantFileChangedIndicator.SetBounds(this.rightPlantList.Left, this.rightPlantFileNameEdit.Top + this.rightPlantFileNameEdit.Height + kBetweenGap, this.rightPlantFileChangedIndicator.Width, this.rightPlantFileChangedIndicator.Height);
        openCloseTop = this.leftPlantFileNameEdit.Top + this.leftPlantFileNameEdit.Height + kBetweenGap;
        this.leftOpenClose.SetBounds(this.leftPlantFileChangedIndicator.Left + this.leftPlantFileChangedIndicator.Width + kBetweenGap, openCloseTop, this.leftOpenClose.Width, this.leftOpenClose.Height);
        this.rightOpenClose.SetBounds(this.rightPlantFileChangedIndicator.Left + this.rightPlantFileChangedIndicator.Width + kBetweenGap, openCloseTop, this.rightOpenClose.Width, this.rightOpenClose.Height);
        this.newFile.SetBounds(this.rightOpenClose.Left + this.rightOpenClose.Width + kBetweenGap, openCloseTop, this.newFile.Width, this.newFile.Height);
        // buttons in middle 
        this.close.SetBounds(midWidth - this.close.Width / 2, UNRESOLVED.intMax(0, this.ClientHeight - this.close.Height - kBetweenGap), this.close.Width, this.close.Height);
        this.helpButton.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.close.Top - this.helpButton.Height - kBetweenGap), this.helpButton.Width, this.helpButton.Height);
        this.redo.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.helpButton.Top - this.redo.Height - kBetweenGap), this.redo.Width, this.redo.Height);
        this.undo.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.redo.Top - this.undo.Height - kBetweenGap), this.undo.Width, this.undo.Height);
        this.rename.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.undo.Top - this.rename.Height - kBetweenGap), this.rename.Width, this.rename.Height);
        this.delete.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.rename.Top - this.delete.Height - kBetweenGap), this.delete.Width, this.delete.Height);
        this.duplicate.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.delete.Top - this.duplicate.Height - kBetweenGap), this.duplicate.Width, this.duplicate.Height);
        this.paste.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.duplicate.Top - this.paste.Height - kBetweenGap), this.paste.Width, this.paste.Height);
        this.copy.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.paste.Top - this.copy.Height - kBetweenGap), this.copy.Width, this.copy.Height);
        this.cut.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.copy.Top - this.cut.Height - kBetweenGap), this.cut.Width, this.cut.Height);
        this.transfer.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.cut.Top - this.transfer.Height - kBetweenGap), this.transfer.Width, this.transfer.Height);
        this.previewImage.SetBounds(listBoxWidth + kBetweenGap * 2, kBetweenGap, UNRESOLVED.intMax(0, this.ClientWidth - listBoxWidth * 2 - kBetweenGap * 4), this.transfer.Top - kBetweenGap * 2);
        this.resizePreviewImage();
    }
    
    public void resizePreviewImage() {
        short i = 0;
        PdPlantManager manager = new PdPlantManager();
        
        try {
            this.previewImage.Picture.Bitmap.Height = this.previewImage.Height;
            this.previewImage.Picture.Bitmap.Width = this.previewImage.Width;
        } catch (Exception e) {
            this.previewImage.Picture.Bitmap.Height = 1;
            this.previewImage.Picture.Bitmap.Width = 1;
        }
        // must invalidate preview cache for both sets of plants
        manager = this.selectedManager(kThisManager);
        if (manager.plants.count > 0) {
            for (i = 0; i <= manager.plants.count - 1; i++) {
                UNRESOLVED.PdPlant(manager.plants.items[i]).previewCacheUpToDate = false;
            }
        }
        manager = this.selectedManager(kOtherManager);
        if (manager.plants.count > 0) {
            for (i = 0; i <= manager.plants.count - 1; i++) {
                UNRESOLVED.PdPlant(manager.plants.items[i]).previewCacheUpToDate = false;
            }
        }
        this.drawPreview(this.focusedPlant());
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 400;
        UNRESOLVED.ptMinTrackSize.y = 420;
    }
    
    // ----------------------------------------------------------------------------------------- command list 
    public void clearCommandList() {
        this.commandList.free;
        this.commandList = null;
        this.commandList = UNRESOLVED.PdCommandList.create;
        this.updateButtonsForUndoRedo();
    }
    
    public void doCommand(PdCommand command) {
        this.commandList.doCommand(command);
        this.updateButtonsForUndoRedo();
        this.updateForChangeToSelectedPlants();
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Using_the_plant_mover");
    }
    
}
class PdMoverRenameCommand extends PdCommand {
    public PdPlant plant;
    public String oldName;
    public String newName;
    public PdPlantManager manager;
    public boolean managerChangedBeforeCommand;
    
    // ------------------------------------------------------------------------------ *commands 
    // ------------------------------------------------------------------- PdMoverRenameCommand 
    public void createWithPlantNewNameAndManager(PdPlant aPlant, String aNewName, PdPlantManager aManager) {
        super.create();
        UNRESOLVED.commandChangesPlantFile = false;
        this.plant = aPlant;
        this.oldName = this.plant.getName;
        this.newName = aNewName;
        this.manager = aManager;
        this.managerChangedBeforeCommand = MoverForm.managerHasChanged(this.manager);
    }
    
    public void doCommand() {
        //not redo
        super.doCommand();
        this.plant.setName(this.newName);
        MoverForm.setChangedFlagForPlantManager(true, this.manager);
    }
    
    public void undoCommand() {
        super.undoCommand();
        this.plant.setName(this.oldName);
        MoverForm.setChangedFlagForPlantManager(this.managerChangedBeforeCommand, this.manager);
    }
    
    public String description() {
        result = "";
        result = "rename";
        return result;
    }
    
}
//use for cut and delete
class PdMoverRemoveCommand extends PdCommandWithListOfPlants {
    public TList removedPlants;
    public boolean copyToClipboard;
    public PdPlantManager manager;
    public boolean managerChangedBeforeCommand;
    
    // ----------------------------------------------------------------------- PdMoverRemoveCommand 
    public void createWithListOfPlantsManagerAndClipboardFlag(TList aList, PdPlantManager aManager, boolean aCopyToClipboard) {
        super.createWithListOfPlants(aList);
        UNRESOLVED.commandChangesPlantFile = false;
        this.manager = aManager;
        this.managerChangedBeforeCommand = MoverForm.managerHasChanged(this.manager);
        this.copyToClipboard = aCopyToClipboard;
        this.removedPlants = delphi_compatability.TList().Create();
    }
    
    public void destroy() {
        short i = 0;
        
        if ((UNRESOLVED.done) && (this.removedPlants != null) && (this.removedPlants.Count > 0)) {
            for (i = 0; i <= this.removedPlants.Count - 1; i++) {
                // free copies of cut plants if change was done 
                UNRESOLVED.plant = UNRESOLVED.PdPlant(this.removedPlants.Items[i]);
                UNRESOLVED.plant.free;
            }
        }
        this.removedPlants.free;
        this.removedPlants = null;
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        
        //not redo
        super.doCommand();
        if (UNRESOLVED.plantList.count <= 0) {
            return;
        }
        if (this.copyToClipboard) {
            // copy plants 
            MoverForm.copySelectedPlantsToClipboard();
        }
        // save copy of plants before deleting 
        this.removedPlants.Clear();
        for (i = 0; i <= UNRESOLVED.plantList.count - 1; i++) {
            // don't remove plants from manager until all indexes have been recorded 
            UNRESOLVED.plant = UNRESOLVED.PdPlant(UNRESOLVED.plantList.items[i]);
            this.removedPlants.Add(UNRESOLVED.plant);
            UNRESOLVED.plant.indexWhenRemoved = this.manager.plants.indexOf(UNRESOLVED.plant);
            UNRESOLVED.plant.selectedIndexWhenRemoved = MoverForm.selectedPlants.IndexOf(UNRESOLVED.plant);
        }
        for (i = 0; i <= UNRESOLVED.plantList.count - 1; i++) {
            this.manager.plants.remove(UNRESOLVED.PdPlant(UNRESOLVED.plantList.items[i]));
        }
        for (i = 0; i <= UNRESOLVED.plantList.count - 1; i++) {
            MoverForm.selectedPlants.Remove(UNRESOLVED.PdPlant(UNRESOLVED.plantList.items[i]));
        }
        MoverForm.updatePlantListForManager(this.manager);
        MoverForm.setChangedFlagForPlantManager(true, this.manager);
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.removedPlants.Count > 0) {
            for (i = 0; i <= this.removedPlants.Count - 1; i++) {
                UNRESOLVED.plant = UNRESOLVED.PdPlant(this.removedPlants.Items[i]);
                if ((UNRESOLVED.plant.indexWhenRemoved >= 0) && (UNRESOLVED.plant.indexWhenRemoved <= this.manager.plants.count - 1)) {
                    this.manager.plants.insert(UNRESOLVED.plant.indexWhenRemoved, UNRESOLVED.plant);
                } else {
                    this.manager.plants.add(UNRESOLVED.plant);
                }
                if ((UNRESOLVED.plant.selectedIndexWhenRemoved >= 0) && (UNRESOLVED.plant.selectedIndexWhenRemoved <= MoverForm.selectedPlants.Count - 1)) {
                    // all removed plants must have been selected, so also add them to the selected list 
                    MoverForm.selectedPlants.Insert(UNRESOLVED.plant.selectedIndexWhenRemoved, UNRESOLVED.plant);
                } else {
                    MoverForm.selectedPlants.Add(UNRESOLVED.plant);
                }
            }
            MoverForm.updatePlantListForManager(this.manager);
            MoverForm.setChangedFlagForPlantManager(this.managerChangedBeforeCommand, this.manager);
        }
    }
    
    public String description() {
        result = "";
        if (this.copyToClipboard) {
            result = "cut";
        } else {
            result = "delete";
        }
        return result;
    }
    
}
//use for transfer and paste
class PdMoverPasteCommand extends PdCommandWithListOfPlants {
    public boolean isTransfer;
    public PdPlantManager manager;
    public boolean managerChangedBeforeCommand;
    
    // ------------------------------------------------------------------ PdMoverPasteCommand 
    public void createWithListOfPlantsAndManager(TList aList, PdPlantManager aManager) {
        super.createWithListOfPlants(aList);
        UNRESOLVED.commandChangesPlantFile = false;
        this.manager = aManager;
        this.managerChangedBeforeCommand = MoverForm.managerHasChanged(this.manager);
    }
    
    public void destroy() {
        short i = 0;
        
        if ((!UNRESOLVED.done) && (UNRESOLVED.plantList != null) && (UNRESOLVED.plantList.count > 0)) {
            for (i = 0; i <= UNRESOLVED.plantList.count - 1; i++) {
                // free copies of pasted plants if change was undone 
                UNRESOLVED.plant = UNRESOLVED.PdPlant(UNRESOLVED.plantList.items[i]);
                UNRESOLVED.plant.free;
            }
        }
        //will free plantList
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        
        //not redo
        super.doCommand();
        if (UNRESOLVED.plantList.count > 0) {
            MoverForm.deselectAllPlants();
            for (i = 0; i <= UNRESOLVED.plantList.count - 1; i++) {
                UNRESOLVED.plant = UNRESOLVED.PdPlant(UNRESOLVED.plantList.items[i]);
                this.manager.plants.add(UNRESOLVED.plant);
                MoverForm.selectedPlants.Add(UNRESOLVED.plant);
            }
            MoverForm.updatePlantListForManager(this.manager);
            MoverForm.setChangedFlagForPlantManager(true, this.manager);
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (UNRESOLVED.plantList.count > 0) {
            for (i = 0; i <= UNRESOLVED.plantList.count - 1; i++) {
                UNRESOLVED.plant = UNRESOLVED.PdPlant(UNRESOLVED.plantList.items[i]);
                this.manager.plants.remove(UNRESOLVED.plant);
                MoverForm.selectedPlants.Remove(UNRESOLVED.plant);
            }
            MoverForm.updatePlantListForManager(this.manager);
            MoverForm.setChangedFlagForPlantManager(this.managerChangedBeforeCommand, this.manager);
        }
    }
    
    public String description() {
        result = "";
        if (this.isTransfer) {
            result = "transfer";
        } else {
            result = "paste";
        }
        return result;
    }
    
}
class PdMoverDuplicateCommand extends PdCommandWithListOfPlants {
    public TList newPlants;
    public PdPlantManager manager;
    public boolean managerChangedBeforeCommand;
    
    // ------------------------------------------------------------------------------ PdMoverDuplicateCommand 
    public void createWithListOfPlantsAndManager(TList aList, PdPlantManager aManager) {
        super.createWithListOfPlants(aList);
        UNRESOLVED.commandChangesPlantFile = false;
        this.newPlants = delphi_compatability.TList().Create();
        this.manager = aManager;
        this.managerChangedBeforeCommand = MoverForm.managerHasChanged(this.manager);
    }
    
    public void destroy() {
        short i = 0;
        
        if ((!UNRESOLVED.done) && (this.newPlants != null) && (this.newPlants.Count > 0)) {
            for (i = 0; i <= this.newPlants.Count - 1; i++) {
                // free copies of created plants if change was undone 
                UNRESOLVED.plant = UNRESOLVED.PdPlant(this.newPlants.Items[i]);
                UNRESOLVED.plant.free;
            }
        }
        this.newPlants.free;
        this.newPlants = null;
        //will free plantList
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        PdPlant plantCopy = new PdPlant();
        
        super.doCommand();
        if (UNRESOLVED.plantList.count > 0) {
            MoverForm.deselectAllPlants();
            for (i = 0; i <= UNRESOLVED.plantList.count - 1; i++) {
                UNRESOLVED.plant = UNRESOLVED.PdPlant(UNRESOLVED.plantList.items[i]);
                plantCopy = UNRESOLVED.PdPlant.create;
                UNRESOLVED.plant.copyTo(plantCopy);
                plantCopy.setName("Copy of " + plantCopy.getName);
                this.newPlants.Add(plantCopy);
                this.manager.plants.add(plantCopy);
                MoverForm.selectedPlants.Add(plantCopy);
            }
            MoverForm.updatePlantListForManager(this.manager);
            MoverForm.setChangedFlagForPlantManager(true, this.manager);
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.newPlants.Count > 0) {
            for (i = 0; i <= this.newPlants.Count - 1; i++) {
                UNRESOLVED.plant = UNRESOLVED.PdPlant(this.newPlants.Items[i]);
                this.manager.plants.remove(UNRESOLVED.plant);
                MoverForm.selectedPlants.Remove(UNRESOLVED.plant);
            }
            MoverForm.updatePlantListForManager(this.manager);
            MoverForm.setChangedFlagForPlantManager(this.managerChangedBeforeCommand, this.manager);
        }
    }
    
    public void redoCommand() {
        short i = 0;
        
        //not redo
        super.doCommand();
        if (this.newPlants.Count > 0) {
            MoverForm.deselectAllPlants();
            for (i = 0; i <= this.newPlants.Count - 1; i++) {
                UNRESOLVED.plant = UNRESOLVED.PdPlant(this.newPlants.Items[i]);
                this.manager.plants.add(UNRESOLVED.plant);
                MoverForm.selectedPlants.Add(UNRESOLVED.plant);
            }
            MoverForm.updatePlantListForManager(this.manager);
            MoverForm.setChangedFlagForPlantManager(true, this.manager);
        }
    }
    
    public String description() {
        result = "";
        result = "duplicate";
        return result;
    }
    
}
// tried this - big mess
//procedure TMoverForm.drawDragItemLine(listBox: TListBox; y: integer);
//  begin
//  if listBox = leftPlantList then
//    begin
//    leftDragItemLastDrawY := y;
//    self.drawOrUndrawDragItemLine(listBox, y);
//    self.leftDragItemLineNeedToRedraw := true;
//    end
//  else
//    begin
//    rightDragItemLastDrawY := y;
//    self.drawOrUndrawDragItemLine(listBox, y);
//    self.rightDragItemLineNeedToRedraw := true;
//    end;
//  end;
//
//procedure TMoverForm.undrawDragItemLine(listBox: TListBox);
//  begin
//  if listBox = leftPlantList then
//    begin
//    if not leftDragItemLineNeedToRedraw then exit;
//    self.drawOrUndrawDragItemLine(listBox, leftDragItemLastDrawY);
//    self.leftDragItemLineNeedToRedraw := false;
//    end
//  else
//    begin
//    if not rightDragItemLineNeedToRedraw then exit;
//    self.drawOrUndrawDragItemLine(listBox, rightDragItemLastDrawY);
//    self.rightDragItemLineNeedToRedraw := false;
//    end;
//  end;
//
//procedure TMoverForm.drawOrUndrawDragItemLine(listBox: TListBox; y: integer);
//  var
//    theDC: HDC;
//    drawRect: TRect;
//  begin
//  theDC := getDC(0);
//  with drawRect do
//    begin
//    left := self.clientOrigin.x + listBox.left;
//    right := self.clientOrigin.x + listBox.left + listBox.width;
//    top := self.clientOrigin.y + listBox.top + y;
//    end;
//  with drawRect do
//    patBlt(theDC, left, top, right - left, 1, dstInvert);
//  releaseDC(0, theDC);
//  end;
//
//{ -------------------------------------------------------------------------------------------- *up and down }
//procedure TMoverForm.moveItemsUpOrDown(listBox: TListBox; y: integer);
//  var
//    rows, i: integer;
//  begin
//  if self.dragItemsY <> 0 then
//    begin
//    rows := abs(y - self.dragItemsY) div listBox.itemHeight;
//    if rows > 0 then
//      begin
//      if (y - self.dragItemsY) > 0 then
//        for i := 0 to rows - 1 do self.moveItemsDown(listBox)
//      else
//        for i := 0 to rows - 1 do self.moveItemsUp(listBox);
//      end;
//    self.dragItemsY := y;
//    end;
//  end;
//
//procedure TMoverForm.moveItemsDown(listBox: TListBox);
//  var
//    i: integer;
//  begin
//  if listBox.items.count > 1 then
//    begin
//    i := listBox.items.count - 2;  { start at next to last one because you can't move last one down any more }
//    while i >= 0 do
//      begin
//      if listBox.selected[i] then
//        begin
//        listBox.items.move(i, i + 1);
//        listBox.selected[i+1] := true;
//        end;
//      dec(i);
//      end;
//    end;
//  end;
//
//procedure TMoverForm.moveItemsUp(listBox: TListBox);
//  var
//    i: integer;
//  begin
//  if listBox.items.count > 1 then
//    begin
//    i := 1;  { start at 1 because you can't move first one up any more }
//    while i <= listBox.items.count - 1 do
//      begin
//      if listBox.selected[i] then
//        begin
//        listBox.items.move(i, i - 1);
//        listBox.selected[i-1] := true;
//        end;
//      inc(i);
//      end;
//    end;
//  end;
//
//
