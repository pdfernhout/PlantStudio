// unit utdomove

from conversion_common import *;
import utdoedit;
import ucursor;
import updform;
import uplantmn;
import delphi_compatability;

// const
kLeft = 0;
kRight = 1;
kNewTdoFileName = "untitled.tdo";
kThisList = true;
kOtherList = false;


// var
TTdoMoverForm TdoMoverForm = new TTdoMoverForm();


// const
kBetweenGap = 4;



class TTdoMoverForm extends PdForm {
    public TEdit leftTdoFileNameEdit;
    public TButton leftOpenClose;
    public TEdit rightTdoFileNameEdit;
    public TButton rightOpenClose;
    public TButton newFile;
    public TButton transfer;
    public TButton close;
    public TImage previewImage;
    public TButton undo;
    public TButton redo;
    public TButton rename;
    public TButton duplicate;
    public TButton delete;
    public TImage leftTdoFileChangedIndicator;
    public TImage rightTdoFileChangedIndicator;
    public TDrawGrid leftTdoList;
    public TDrawGrid rightTdoList;
    public TButton editTdo;
    public TSpeedButton helpButton;
    public String leftTdoFileName;
    public String rightTdoFileName;
    public TListCollection leftList;
    public TListCollection rightList;
    public boolean leftTdoFileChanged;
    public boolean rightTdoFileChanged;
    public int lastLeftSingleClickTdoIndex;
    public int lastRightSingleClickTdoIndex;
    public short leftOrRight;
    public PdCommandList commandList;
    public TList selectedTdos;
    public int dragItemsY;
    public boolean justDoubleClickedOnLeftGrid;
    public boolean justDoubleClickedOnRightGrid;
    
    //$R *.DFM
    // -------------------------------------------------------------------------------------------- *creation/destruction 
    public void create(TComponent AOwner) {
        super.create(AOwner);
        TdoMoverForm = this;
        this.leftList = UNRESOLVED.TListCollection.create;
        this.rightList = UNRESOLVED.TListCollection.create;
        this.commandList = UNRESOLVED.PdCommandList.create;
        this.selectedTdos = delphi_compatability.TList().Create();
        this.commandList.setNewUndoLimit(UNRESOLVED.domain.options.undoLimit);
        this.commandList.setNewObjectUndoLimit(UNRESOLVED.domain.options.undoLimitOfPlants);
        this.updateButtonsForUndoRedo();
        if (len(UNRESOLVED.domain.defaultTdoLibraryFileName) > 0) {
            // load current tdo file into left side to start 
            this.openTdoFileForList(this.leftList, UNRESOLVED.domain.defaultTdoLibraryFileName);
        } else {
            this.closeTdoFileForList(this.leftList);
        }
        // right side is empty to start 
        this.closeTdoFileForList(this.rightList);
    }
    
    public void FormCreate(TObject Sender) {
        this.leftTdoList.DragCursor = ucursor.crDragTdo;
        this.rightTdoList.DragCursor = ucursor.crDragTdo;
    }
    
    public void destroy() {
        this.leftList.free;
        this.leftList = null;
        this.rightList.free;
        this.rightList = null;
        this.selectedTdos.free;
        this.selectedTdos = null;
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
        if (!this.askToSaveListAndProceed(this.leftList)) {
            return;
        }
        if (!this.askToSaveListAndProceed(this.rightList)) {
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
        this.updateForChangeToSelectedTdos();
    }
    
    public void redoClick(TObject Sender) {
        this.commandList.redoLast;
        this.updateButtonsForUndoRedo();
        this.updateForChangeToSelectedTdos();
    }
    
    public void closeClick(TObject Sender) {
        if (!this.askToSaveListAndProceed(this.leftList)) {
            return;
        }
        if (!this.askToSaveListAndProceed(this.rightList)) {
            return;
        }
        // cannot cancel 
        this.ModalResult = mrOK;
    }
    
    public void leftOpenCloseClick(TObject Sender) {
        if (this.haveLeftFile()) {
            //file open
            //no file
            this.closeTdoFileForList(this.leftList);
        } else {
            this.openTdoFileForList(this.leftList, "");
        }
    }
    
    public void rightOpenCloseClick(TObject Sender) {
        if (this.haveRightFile()) {
            //file open
            //no file
            this.closeTdoFileForList(this.rightList);
        } else {
            this.openTdoFileForList(this.rightList, "");
        }
    }
    
    public void newFileClick(TObject Sender) {
        this.newTdoFileForList(this.rightList);
    }
    
    public void transferClick(TObject Sender) {
        TListCollection list = new TListCollection();
        TListCollection otherList = new TListCollection();
        PdCommand newCommand = new PdCommand();
        TList newTdos = new TList();
        KfObject3D tdo = new KfObject3D();
        KfObject3D newTdo = new KfObject3D();
        short i = 0;
        
        list = this.selectedList(kThisList);
        otherList = this.selectedList(kOtherList);
        if ((list == null) || (otherList == null) || (this.selectedTdos.Count <= 0)) {
            return;
        }
        if (this.selectedTdos.Count > 0) {
            //command will free
            newTdos = delphi_compatability.TList().Create();
            for (i = 0; i <= this.selectedTdos.Count - 1; i++) {
                tdo = UNRESOLVED.KfObject3D(this.selectedTdos.Items[i]);
                newTdo = UNRESOLVED.KfObject3D.create;
                tdo.copyTo(newTdo);
                newTdos.Add(newTdo);
            }
            newCommand = PdTdoMoverTransferCommand().createWithSelectedTdosAndList(newTdos, otherList);
            this.doCommand(newCommand);
            //command has its own list, so we need to free this one
            newTdos.free;
        }
    }
    
    public void duplicateClick(TObject Sender) {
        TListCollection list = new TListCollection();
        PdCommand newCommand = new PdCommand();
        
        list = this.selectedList(kThisList);
        if ((list == null) || (this.selectedTdos.Count <= 0)) {
            return;
        }
        newCommand = PdTdoMoverDuplicateCommand().createWithSelectedTdosAndList(this.selectedTdos, list);
        this.doCommand(newCommand);
    }
    
    public void renameClick(TObject Sender) {
        KfObject3D tdo = new KfObject3D();
        TListCollection list = new TListCollection();
        ansistring newName = new ansistring();
        PdCommand newCommand = new PdCommand();
        
        // can only rename one tdo at a time 
        list = this.selectedList(kThisList);
        tdo = this.focusedTdo();
        if ((tdo == null) || (list == null)) {
            return;
        }
        newName = tdo.getName;
        if (!InputQuery("Enter new name", "Type a new name for " + newName + ".", newName)) {
            return;
        }
        newCommand = PdTdoMoverRenameCommand().createWithTdoNewNameAndList(tdo, newName, list);
        this.doCommand(newCommand);
    }
    
    public void deleteClick(TObject Sender) {
        TListCollection list = new TListCollection();
        PdCommand newCommand = new PdCommand();
        
        list = this.selectedList(kThisList);
        if ((list == null) || (this.selectedTdos.Count <= 0)) {
            return;
        }
        newCommand = PdTdoMoverRemoveCommand().createWithSelectedTdosAndList(this.selectedTdos, list);
        this.doCommand(newCommand);
    }
    
    public void editTdoClick(TObject Sender) {
        TTdoEditorForm tdoEditorForm = new TTdoEditorForm();
        int response = 0;
        PdCommand newCommand = new PdCommand();
        KfObject3D tempTdo = new KfObject3D();
        
        if (this.focusedTdo() == null) {
            return;
        }
        tdoEditorForm = utdoedit.TTdoEditorForm().create(this);
        if (tdoEditorForm == null) {
            throw new GeneralException.create("Problem: Could not create 3D object editor window.");
        }
        tempTdo = UNRESOLVED.KfObject3D.create;
        try {
            tempTdo.copyFrom(this.focusedTdo());
            tdoEditorForm.initializeWithTdo(tempTdo);
            response = tdoEditorForm.ShowModal();
            if (response == mrOK) {
                // v1.6b1
                tempTdo.copyFrom(tdoEditorForm.tdo);
                newCommand = PdTdoMoverEditCommand().createWithTdoNewTdoAndList(this.focusedTdo(), tempTdo, this.selectedList(kThisList));
                this.doCommand(newCommand);
            }
        } finally {
            tdoEditorForm.free;
            tdoEditorForm = null;
            tempTdo.free;
            tempTdo = null;
        }
    }
    
    public void sortListClick(TObject Sender) {
        pass
    }
    
    // -------------------------------------------------------------------------------------- *list box actions 
    public void leftTdoListDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        this.drawLineInGrid(this.leftTdoList, this.leftList, Row, Rect, State);
    }
    
    public void rightTdoListDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        this.drawLineInGrid(this.rightTdoList, this.rightList, Row, Rect, State);
    }
    
    public void drawLineInGrid(TDrawGrid grid, TListCollection list, int index, TRect rect, TGridDrawState state) {
        KfObject3D tdo = new KfObject3D();
        boolean selected = false;
         cText = [0] * (range(0, 255 + 1) + 1);
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        grid.Canvas.Brush.Color = grid.Color;
        grid.Canvas.FillRect(Rect);
        if ((list.count <= 0) || (index < 0) || (index > list.count - 1)) {
            return;
        }
        // set up tdo pointer 
        tdo = UNRESOLVED.KfObject3D(list.items[index]);
        if (tdo == null) {
            return;
        }
        selected = (list == this.selectedList(kThisList)) && (this.selectedTdos.IndexOf(tdo) >= 0);
        grid.Canvas.Font = grid.Font;
        if (selected) {
            grid.Canvas.Brush.Color = UNRESOLVED.clHighlight;
            grid.Canvas.Font.Color = UNRESOLVED.clHighlightText;
        } else {
            grid.Canvas.Brush.Color = grid.Color;
            grid.Canvas.Font.Color = UNRESOLVED.clBtnText;
        }
        grid.Canvas.FillRect(Rect);
        UNRESOLVED.strPCopy(cText, tdo.getName);
        // margin for text 
        Rect.left = Rect.left + 2;
        UNRESOLVED.winprocs.drawText(grid.Canvas.Handle, cText, len(cText), Rect, delphi_compatability.DT_LEFT);
        if (tdo == this.focusedTdo()) {
            // put back 
            Rect.left = Rect.left - 2;
            UNRESOLVED.drawFocusRect(Rect);
        }
    }
    
    // left list mouse handling
    public void leftTdoListMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        int col = 0;
        int row = 0;
        
        if (this.justDoubleClickedOnLeftGrid) {
            this.justDoubleClickedOnLeftGrid = false;
            return;
        } else {
            this.justDoubleClickedOnLeftGrid = false;
        }
        if (this.leftList.count > 0) {
            if (this.leftOrRight == kRight) {
                this.selectedTdos.Clear();
                this.lastRightSingleClickTdoIndex = -1;
                this.rightTdoList.Invalidate();
            }
            this.leftOrRight = kLeft;
            col, row = this.leftTdoList.MouseToCell(X, Y, col, row);
            this.selectTdoAtIndex(Shift, row);
            this.leftTdoList.Invalidate();
            this.updateForChangeToSelectedTdos();
            this.leftTdoList.BeginDrag(false);
        }
    }
    
    public void leftTdoListDragOver(TObject Sender, TObject Source, int X, int Y, TDragState State, boolean Accept) {
        Accept = (Source != null) && (Sender != null);
        if (Source == this.rightTdoList) {
            Accept = Accept && this.haveLeftFile();
        } else {
            Accept = Accept && (Source == Sender);
        }
        return Accept;
    }
    
    public void leftTdoListEndDrag(TObject Sender, TObject Target, int X, int Y) {
        if ((Target == this.rightTdoList)) {
            this.transferClick(this);
        }
    }
    
    public void leftTdoListDblClick(TObject Sender) {
        this.renameClick(this);
        this.leftTdoList.endDrag(false);
        this.justDoubleClickedOnLeftGrid = true;
    }
    
    // right list mouse handling
    public void rightTdoListMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        int col = 0;
        int row = 0;
        
        if (this.justDoubleClickedOnRightGrid) {
            this.justDoubleClickedOnRightGrid = false;
            return;
        } else {
            this.justDoubleClickedOnRightGrid = false;
        }
        if (this.rightList.count > 0) {
            if (this.leftOrRight == kLeft) {
                this.selectedTdos.Clear();
                this.lastLeftSingleClickTdoIndex = -1;
                this.leftTdoList.Invalidate();
            }
            this.leftOrRight = kRight;
            col, row = this.rightTdoList.MouseToCell(X, Y, col, row);
            this.selectTdoAtIndex(Shift, row);
            this.rightTdoList.Invalidate();
            this.updateForChangeToSelectedTdos();
            this.rightTdoList.BeginDrag(false);
        }
    }
    
    public void rightTdoListDragOver(TObject Sender, TObject Source, int X, int Y, TDragState State, boolean Accept) {
        Accept = (Source != null) && (Sender != null);
        if (Source == this.leftTdoList) {
            Accept = Accept && this.haveRightFile();
        } else {
            Accept = Accept && (Source == Sender);
        }
        return Accept;
    }
    
    public void rightTdoListEndDrag(TObject Sender, TObject Target, int X, int Y) {
        if ((Target == this.leftTdoList)) {
            this.transferClick(this);
        }
    }
    
    public void rightTdoListDblClick(TObject Sender) {
        this.renameClick(this);
        this.rightTdoList.endDrag(false);
        this.justDoubleClickedOnRightGrid = true;
    }
    
    public void selectTdoAtIndex(TShiftState Shift, int index) {
        short i = 0;
        KfObject3D tdo = new KfObject3D();
        TListCollection list = new TListCollection();
        int lastSingleClickTdoIndex = 0;
        int lastRow = 0;
        TDrawGrid grid = new TDrawGrid();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        list = this.selectedList(kThisList);
        if (list == null) {
            return;
        }
        if ((index < 0)) {
            this.selectedTdos.Clear();
            return;
        }
        tdo = UNRESOLVED.KfObject3D(list.items[index]);
        if (tdo == null) {
            return;
        }
        if ((delphi_compatability.TShiftStateEnum.ssCtrl in Shift)) {
            if (this.selectedTdos.IndexOf(tdo) >= 0) {
                this.selectedTdos.Remove(tdo);
            } else {
                this.selectedTdos.Add(tdo);
            }
        } else if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
            if (this.leftOrRight == kLeft) {
                lastSingleClickTdoIndex = this.lastLeftSingleClickTdoIndex;
            } else {
                lastSingleClickTdoIndex = this.lastRightSingleClickTdoIndex;
            }
            if ((lastSingleClickTdoIndex >= 0) && (lastSingleClickTdoIndex <= list.count - 1) && (lastSingleClickTdoIndex != index)) {
                if (lastSingleClickTdoIndex < index) {
                    for (i = lastSingleClickTdoIndex; i <= index; i++) {
                        if (this.selectedTdos.IndexOf(list.items[i]) < 0) {
                            this.selectedTdos.Add(list.items[i]);
                        }
                    }
                } else if (lastSingleClickTdoIndex > index) {
                    for (i = lastSingleClickTdoIndex; i >= index; i--) {
                        if (this.selectedTdos.IndexOf(list.items[i]) < 0) {
                            this.selectedTdos.Add(list.items[i]);
                        }
                    }
                }
            }
            // just a click
        } else {
            if (this.selectedTdos.IndexOf(tdo) <= 0) {
                this.selectedTdos.Clear();
                this.selectedTdos.Add(tdo);
                if (this.leftOrRight == kLeft) {
                    this.lastLeftSingleClickTdoIndex = index;
                } else {
                    this.lastRightSingleClickTdoIndex = index;
                }
            }
            grid = this.gridForList(list);
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
    
    public void leftTdoListKeyDown(TObject Sender, byte Key, TShiftState Shift) {
        Key = this.listKeyDown(Key, Shift);
        return Key;
    }
    
    public void rightTdoListKeyDown(TObject Sender, byte Key, TShiftState Shift) {
        Key = this.listKeyDown(Key, Shift);
        return Key;
    }
    
    public void listKeyDown(byte Key, TShiftState Shift) {
        switch (Key) {
            case delphi_compatability.VK_DOWN:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.moveSelectedTdosDown();
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKey(this.focusedTdoIndexInList() + 1);
                }
                break;
            case delphi_compatability.VK_RIGHT:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.moveSelectedTdosDown();
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKey(this.focusedTdoIndexInList() + 1);
                }
                break;
            case delphi_compatability.VK_UP:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.moveSelectedTdosUp();
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKey(this.focusedTdoIndexInList() - 1);
                }
                break;
            case delphi_compatability.VK_LEFT:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.moveSelectedTdosUp();
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKey(this.focusedTdoIndexInList() - 1);
                }
                break;
            case delphi_compatability.VK_RETURN:
                Key = 0;
                this.renameClick(this);
                break;
        return Key;
    }
    
    public void moveUpOrDownWithKey(short indexAfterMove) {
        TListCollection list = new TListCollection();
        
        list = this.selectedList(kThisList);
        if (list == null) {
            return;
        }
        if (indexAfterMove > list.count - 1) {
            // loop around 
            indexAfterMove = 0;
        }
        if (indexAfterMove < 0) {
            indexAfterMove = list.count - 1;
        }
        if ((indexAfterMove >= 0) && (indexAfterMove <= list.count - 1)) {
            this.deselectAllTdos();
            //no shift
            this.selectTdoAtIndex({}, indexAfterMove);
            this.drawPreview(this.focusedTdo());
        }
    }
    
    public void moveSelectedTdosDown() {
        TListCollection list = new TListCollection();
        short i = 0;
        KfObject3D tdo = new KfObject3D();
        
        if (this.selectedTdos.Count <= 0) {
            return;
        }
        list = this.selectedList(kThisList);
        if (list == null) {
            return;
        }
        if (list.count > 1) {
            // start at next to last one because you can't move last one down any more 
            i = list.count - 2;
            while (i >= 0) {
                tdo = UNRESOLVED.KfObject3D(list.items[i]);
                if (this.selectedTdos.IndexOf(tdo) >= 0) {
                    list.move(i, i + 1);
                }
                i -= 1;
            }
        }
        this.redrawSelectedGrid();
        // reordering makes change flag true
        this.setChangedFlagForTdoList(true, this.selectedList(kThisList));
    }
    
    public void moveSelectedTdosUp() {
        TListCollection list = new TListCollection();
        short i = 0;
        KfObject3D tdo = new KfObject3D();
        
        if (this.selectedTdos.Count <= 0) {
            return;
        }
        list = this.selectedList(kThisList);
        if (list == null) {
            return;
        }
        if (list.count > 1) {
            // start at 1 because you can't move first one up any more 
            i = 1;
            while (i <= list.count - 1) {
                tdo = UNRESOLVED.KfObject3D(list.items[i]);
                if (this.selectedTdos.IndexOf(tdo) >= 0) {
                    list.move(i, i - 1);
                }
                i += 1;
            }
        }
        this.redrawSelectedGrid();
        // reordering makes change flag true
        this.setChangedFlagForTdoList(true, this.selectedList(kThisList));
    }
    
    public void redrawSelectedGrid() {
        if (this.leftOrRight == kLeft) {
            this.leftTdoList.Invalidate();
        } else {
            this.rightTdoList.Invalidate();
        }
    }
    
    // -------------------------------------------------------------------------------------------- *updating 
    public void updateForNewFile(String newFileName, TListCollection list) {
        this.clearCommandList();
        this.setFileNameForList(newFileName, list);
        this.updateTdoListForList(list);
        this.setChangedFlagForTdoList(false, list);
        this.deselectAllTdos();
        if (newFileName != "") {
            if (list == this.leftList) {
                this.leftOrRight = kLeft;
            } else {
                this.leftOrRight = kRight;
            }
        }
        this.updateForChangeToSelectedTdos();
    }
    
    public void deselectAllTdos() {
        this.selectedTdos.Clear();
        this.leftTdoList.Invalidate();
        this.rightTdoList.Invalidate();
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
    
    public void updateForChangeToSelectedTdos() {
        boolean atLeastOneTdoSelected = false;
        boolean atLeastOneFile = false;
        
        this.leftTdoList.Invalidate();
        this.rightTdoList.Invalidate();
        if (this.leftOrRight == kLeft) {
            if (this.haveLeftFile()) {
                this.leftOpenClose.Caption = "&Close";
            } else {
                this.leftOpenClose.Caption = "&Open...";
            }
            this.leftTdoFileNameEdit.Color = delphi_compatability.clAqua;
            this.leftTdoFileNameEdit.Refresh();
            this.rightTdoFileNameEdit.Color = UNRESOLVED.clBtnFace;
            this.rightTdoFileNameEdit.Refresh();
            this.drawPreview(this.focusedTdo());
        } else {
            if (this.haveRightFile()) {
                this.rightOpenClose.Caption = "&Close";
            } else {
                this.rightOpenClose.Caption = "&Open...";
            }
            this.leftTdoFileNameEdit.Color = UNRESOLVED.clBtnFace;
            this.leftTdoFileNameEdit.Refresh();
            this.rightTdoFileNameEdit.Color = delphi_compatability.clAqua;
            this.rightTdoFileNameEdit.Refresh();
            this.drawPreview(this.focusedTdo());
        }
        atLeastOneFile = this.haveLeftFile() || this.haveRightFile();
        atLeastOneTdoSelected = (this.selectedTdos.Count > 0);
        this.transfer.Enabled = this.haveLeftFile() && this.haveRightFile() && atLeastOneTdoSelected;
        this.transfer.Caption = this.leftRightString("&Transfer >>", "<< &Transfer");
        this.duplicate.Enabled = atLeastOneFile && atLeastOneTdoSelected;
        this.delete.Enabled = atLeastOneFile && atLeastOneTdoSelected;
        this.rename.Enabled = atLeastOneFile && atLeastOneTdoSelected;
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
    
    public void updateTdoListForList(TListCollection list) {
        TDrawGrid grid = new TDrawGrid();
        
        grid = this.gridForList(list);
        if (grid == null) {
            return;
        }
        grid.RowCount = list.count;
        grid.Invalidate();
    }
    
    public void drawPreview(KfObject3D tdo) {
        KfTurtle turtle = new KfTurtle();
        float xScale = 0.0;
        float yScale = 0.0;
        TRect tdoBoundsRect = new TRect();
        TPoint currentPosition = new TPoint();
        float currentScale = 0.0;
        
        this.previewImage.Picture.Bitmap.Canvas.Brush.Color = delphi_compatability.clWindow;
        this.previewImage.Picture.Bitmap.Canvas.FillRect(Rect(0, 0, this.previewImage.Width, this.previewImage.Height));
        this.previewImage.Picture.Bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        if (tdo != null) {
            turtle = UNRESOLVED.KfTurtle.defaultStartUsing;
            try {
                currentScale = 100.0;
                currentPosition = Point(this.previewImage.Width / 2, this.previewImage.Height - this.previewImage.Height / 10);
                turtle.drawingSurface.pane = this.previewImage.Picture.Bitmap.Canvas;
                turtle.setDrawOptionsForDrawingTdoOnly;
                turtle.drawOptions.draw3DObjects = false;
                // draw first to get new scale
                // must be after pane and draw options set 
                turtle.reset;
                turtle.xyz(currentPosition.X, currentPosition.Y, 0);
                turtle.drawingSurface.recordingStart;
                tdo.draw(turtle, currentScale, "", "", 0, 0);
                turtle.drawingSurface.recordingStop;
                turtle.drawingSurface.recordingDraw;
                turtle.drawingSurface.clearTriangles;
                // calculate new scale to fit
                tdoBoundsRect = turtle.boundsRect;
                xScale = UNRESOLVED.safedivExcept(0.95 * currentScale * this.previewImage.Width, UNRESOLVED.rWidth(tdoBoundsRect), 0.1);
                yScale = UNRESOLVED.safedivExcept(0.95 * currentScale * this.previewImage.Height, UNRESOLVED.rHeight(tdoBoundsRect), 0.1);
                currentScale = UNRESOLVED.min(xScale, yScale);
                currentPosition = tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(this.previewImage.Width, this.previewImage.Height), currentScale);
                // draw second time for real
                turtle.drawOptions.draw3DObjects = true;
                // must be after pane and draw options set 
                turtle.reset;
                turtle.xyz(currentPosition.X, currentPosition.Y, 0);
                turtle.drawingSurface.recordingStart;
                tdo.draw(turtle, currentScale, "", "", 0, 0);
                turtle.drawingSurface.recordingStop;
                turtle.drawingSurface.recordingDraw;
                turtle.drawingSurface.clearTriangles;
            } finally {
                UNRESOLVED.KfTurtle.defaultStopUsing;
            }
        }
        this.previewImage.Picture.Bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        this.previewImage.Picture.Bitmap.Canvas.Pen.Color = UNRESOLVED.clBtnText;
        this.previewImage.Picture.Bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid;
        this.previewImage.Picture.Bitmap.Canvas.Rectangle(0, 0, this.previewImage.Width, this.previewImage.Height);
    }
    
    public void previewImageMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        pass
    }
    
    // ------------------------------------------------------------------------------------------ *selecting 
    public KfObject3D focusedTdo() {
        result = new KfObject3D();
        result = null;
        if (this.selectedTdos.Count > 0) {
            result = UNRESOLVED.KfObject3D(this.selectedTdos.Items[0]);
        }
        return result;
    }
    
    public short focusedTdoIndexInList() {
        result = 0;
        TListCollection list = new TListCollection();
        
        result = -1;
        list = this.selectedList(kThisList);
        if (list == null) {
            return result;
        }
        if (this.selectedTdos.Count > 0) {
            result = list.indexOf(this.selectedTdos.Items[0]);
        }
        return result;
    }
    
    public boolean haveLeftFile() {
        result = false;
        result = len(this.leftTdoFileName) != 0;
        return result;
    }
    
    public boolean haveRightFile() {
        result = false;
        result = len(this.rightTdoFileName) != 0;
        return result;
    }
    
    public TListCollection selectedList(boolean thisList) {
        result = new TListCollection();
        result = null;
        if (this.leftOrRight == kLeft) {
            if (thisList) {
                result = this.leftList;
            } else {
                result = this.rightList;
            }
        } else {
            if (thisList) {
                result = this.rightList;
            } else {
                result = this.leftList;
            }
        }
        return result;
    }
    
    public String getFileNameForList(TListCollection list) {
        result = "";
        if (list == this.leftList) {
            result = this.leftTdoFileName;
        } else {
            result = this.rightTdoFileName;
        }
        return result;
    }
    
    public String getFileNameForOtherList(TListCollection list) {
        result = "";
        if (list == this.rightList) {
            result = this.leftTdoFileName;
        } else {
            result = this.rightTdoFileName;
        }
        return result;
    }
    
    public void setFileNameForList(String newName, TListCollection list) {
        if (list == this.leftList) {
            this.leftTdoFileName = newName;
            this.leftTdoFileNameEdit.Text = newName;
            this.leftTdoFileNameEdit.SelStart = len(newName);
        } else {
            this.rightTdoFileName = newName;
            this.rightTdoFileNameEdit.Text = newName;
            this.rightTdoFileNameEdit.SelStart = len(newName);
        }
    }
    
    public TDrawGrid gridForList(TListCollection list) {
        result = new TDrawGrid();
        result = null;
        if (list == this.leftList) {
            result = this.leftTdoList;
        } else if (list == this.rightList) {
            result = this.rightTdoList;
        }
        return result;
    }
    
    public boolean listHasChanged(TListCollection list) {
        result = false;
        if (list == this.leftList) {
            result = this.leftTdoFileChanged;
        } else {
            result = this.rightTdoFileChanged;
        }
        return result;
    }
    
    public void setChangedFlagForTdoList(boolean value, TListCollection list) {
        if (list == this.leftList) {
            this.leftTdoFileChanged = value;
            if (this.leftTdoFileChanged) {
                this.leftTdoFileChangedIndicator.Picture = UNRESOLVED.MainForm.fileChangedImage.picture;
            } else {
                this.leftTdoFileChangedIndicator.Picture = UNRESOLVED.MainForm.fileNotChangedImage.picture;
            }
        } else {
            this.rightTdoFileChanged = value;
            if (this.rightTdoFileChanged) {
                this.rightTdoFileChangedIndicator.Picture = UNRESOLVED.MainForm.fileChangedImage.picture;
            } else {
                this.rightTdoFileChangedIndicator.Picture = UNRESOLVED.MainForm.fileNotChangedImage.picture;
            }
        }
    }
    
    // ------------------------------------------------------------------------ *opening, closing and saving 
    public void openTdoFileForList(TListCollection list, String fileNameToStart) {
        String fileNameWithPath = "";
        
        if (!this.askToSaveListAndProceed(list)) {
            return;
        }
        if (fileNameToStart == "") {
            fileNameWithPath = UNRESOLVED.getFileOpenInfo(UNRESOLVED.kFileTypeTdo, UNRESOLVED.kNoSuggestedFile, "Choose a tdo file");
        } else {
            fileNameWithPath = fileNameToStart;
        }
        if (fileNameWithPath == "") {
            this.updateForNewFile(fileNameWithPath, list);
        } else {
            if (fileNameWithPath == this.getFileNameForOtherList(list)) {
                ShowMessage("The file you chose is already open on the other side.");
                return;
            }
            try {
                ucursor.cursor_startWait();
                if (FileExists(fileNameWithPath)) {
                    this.loadTdosFromFile(list, fileNameWithPath);
                } else {
                    this.newTdoFileForList(list);
                }
                // PDF PORT -- added semicolon
                this.updateForNewFile(fileNameWithPath, list);
            } finally {
                ucursor.cursor_stopWait();
            }
        }
    }
    
    public void closeTdoFileForList(TListCollection list) {
        if (!this.askToSaveListAndProceed(list)) {
            return;
        }
        list.clear;
        this.updateForNewFile("", list);
    }
    
    public void newTdoFileForList(TListCollection list) {
        if (!this.askToSaveListAndProceed(list)) {
            return;
        }
        list.clear;
        this.updateForNewFile(kNewTdoFileName, list);
    }
    
    public void loadTdosFromFile(TListCollection list, String fileName) {
        KfObject3D newTdo = new KfObject3D();
        TextFile inputFile = new TextFile();
        
        if (list == null) {
            return;
        }
        list.clear;
        if (fileName == "") {
            return;
        }
        if (!FileExists(fileName)) {
            return;
        }
        AssignFile(inputFile, fileName);
        try {
            // v1.5
            UNRESOLVED.setDecimalSeparator;
            Reset(inputFile);
            while (!UNRESOLVED.eof(inputFile)) {
                newTdo = UNRESOLVED.KfObject3D.create;
                newTdo.readFromFileStream(inputFile, UNRESOLVED.kInTdoLibrary);
                list.add(newTdo);
            }
        } finally {
            CloseFile(inputFile);
        }
    }
    
    public void saveTdosToFile(TListCollection list, String fileName) {
        TextFile outputFile = new TextFile();
        short i = 0;
        KfObject3D tdo = new KfObject3D();
        
        if (list == null) {
            return;
        }
        // assume caller has already verified file name
        AssignFile(outputFile, fileName);
        try {
            // v1.5
            UNRESOLVED.setDecimalSeparator;
            Rewrite(outputFile);
            if (list.count > 0) {
                for (i = 0; i <= list.count - 1; i++) {
                    tdo = (UNRESOLVED.KfObject3D)UNRESOLVED.TObject(list.items[i]);
                    if (tdo == null) {
                        continue;
                    }
                    tdo.writeToFileStream(outputFile, UNRESOLVED.kInTdoLibrary);
                }
            }
        } finally {
            CloseFile(outputFile);
        }
    }
    
    public void listSaveOrSaveAs(TListCollection list, boolean askForFileName) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        String fileName = "";
        boolean askForFileNameConsideringUntitled = false;
        
        fileName = this.getFileNameForList(list);
        if (fileName == kNewTdoFileName) {
            askForFileNameConsideringUntitled = true;
        } else {
            askForFileNameConsideringUntitled = askForFileName;
        }
        if (!UNRESOLVED.getFileSaveInfo(UNRESOLVED.kFileTypeTdo, askForFileNameConsideringUntitled, fileName, fileInfo)) {
            return;
        }
        try {
            ucursor.cursor_startWait();
            this.saveTdosToFile(list, fileInfo.tempFile);
            fileInfo.writingWasSuccessful = true;
        } finally {
            ucursor.cursor_stopWait();
            UNRESOLVED.cleanUpAfterFileSave(fileInfo);
            this.updateForNewFile(kNewTdoFileName, list);
        }
    }
    
    public boolean askToSaveListAndProceed(TListCollection list) {
        result = false;
        byte response = 0;
        String prompt = "";
        
        // returns false if user cancelled action 
        result = true;
        if (!this.listHasChanged(list)) {
            return result;
        }
        prompt = "Save changes to " + ExtractFileName(this.getFileNameForList(list)) + "?";
        response = MessageDialog(prompt, mtConfirmation, mbYesNoCancel, 0);
        switch (response) {
            case mrYes:
                this.listSaveOrSaveAs(list, UNRESOLVED.kDontAskForFileName);
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
        if (this.leftList == null) {
            return;
        }
        if (this.rightList == null) {
            return;
        }
        if (this.selectedTdos == null) {
            return;
        }
        midWidth = this.ClientWidth / 2;
        //same as right
        listBoxWidth = this.leftTdoList.Width;
        listBoxTop = kBetweenGap + this.leftTdoFileNameEdit.Height + kBetweenGap + this.leftOpenClose.Height + kBetweenGap;
        // list boxes 
        this.leftTdoList.SetBounds(kBetweenGap, listBoxTop, listBoxWidth, UNRESOLVED.intMax(0, this.ClientHeight - listBoxTop - kBetweenGap));
        this.leftTdoList.DefaultColWidth = this.leftTdoList.ClientWidth;
        this.rightTdoList.SetBounds(UNRESOLVED.intMax(0, this.ClientWidth - listBoxWidth - kBetweenGap), listBoxTop, listBoxWidth, UNRESOLVED.intMax(0, this.ClientHeight - listBoxTop - kBetweenGap));
        this.rightTdoList.DefaultColWidth = this.rightTdoList.ClientWidth;
        // edits and buttons at top 
        this.leftTdoFileNameEdit.SetBounds(kBetweenGap, kBetweenGap, listBoxWidth - kBetweenGap * 2, this.leftTdoFileNameEdit.Height);
        this.leftTdoFileChangedIndicator.SetBounds(kBetweenGap, this.leftTdoFileNameEdit.Top + this.leftTdoFileNameEdit.Height + kBetweenGap, this.leftTdoFileChangedIndicator.Width, this.leftTdoFileChangedIndicator.Height);
        this.rightTdoFileNameEdit.SetBounds(this.rightTdoList.Left, kBetweenGap, listBoxWidth - kBetweenGap * 2, this.rightTdoFileNameEdit.Height);
        this.rightTdoFileChangedIndicator.SetBounds(this.rightTdoList.Left, this.rightTdoFileNameEdit.Top + this.rightTdoFileNameEdit.Height + kBetweenGap, this.rightTdoFileChangedIndicator.Width, this.rightTdoFileChangedIndicator.Height);
        openCloseTop = this.leftTdoFileNameEdit.Top + this.leftTdoFileNameEdit.Height + kBetweenGap;
        this.leftOpenClose.SetBounds(this.leftTdoFileChangedIndicator.Left + this.leftTdoFileChangedIndicator.Width + kBetweenGap, openCloseTop, this.leftOpenClose.Width, this.leftOpenClose.Height);
        this.rightOpenClose.SetBounds(this.rightTdoFileChangedIndicator.Left + this.rightTdoFileChangedIndicator.Width + kBetweenGap, openCloseTop, this.rightOpenClose.Width, this.rightOpenClose.Height);
        this.newFile.SetBounds(this.rightOpenClose.Left + this.rightOpenClose.Width + kBetweenGap, openCloseTop, this.newFile.Width, this.newFile.Height);
        // buttons in middle 
        this.close.SetBounds(midWidth - this.close.Width / 2, UNRESOLVED.intMax(0, this.ClientHeight - this.close.Height - kBetweenGap), this.close.Width, this.close.Height);
        this.helpButton.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.close.Top - this.helpButton.Height - kBetweenGap), this.helpButton.Width, this.helpButton.Height);
        this.editTdo.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.helpButton.Top - this.editTdo.Height - kBetweenGap), this.editTdo.Width, this.editTdo.Height);
        this.redo.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.editTdo.Top - this.redo.Height - kBetweenGap), this.redo.Width, this.redo.Height);
        this.undo.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.redo.Top - this.undo.Height - kBetweenGap), this.undo.Width, this.undo.Height);
        this.rename.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.undo.Top - this.rename.Height - kBetweenGap), this.rename.Width, this.rename.Height);
        this.delete.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.rename.Top - this.delete.Height - kBetweenGap), this.delete.Width, this.delete.Height);
        this.duplicate.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.delete.Top - this.duplicate.Height - kBetweenGap), this.duplicate.Width, this.duplicate.Height);
        this.transfer.SetBounds(this.close.Left, UNRESOLVED.intMax(0, this.duplicate.Top - this.transfer.Height - kBetweenGap), this.transfer.Width, this.transfer.Height);
        this.previewImage.SetBounds(listBoxWidth + kBetweenGap * 2, kBetweenGap, UNRESOLVED.intMax(0, this.ClientWidth - listBoxWidth * 2 - kBetweenGap * 4), this.transfer.Top - kBetweenGap * 2);
        this.resizePreviewImage();
    }
    
    public void resizePreviewImage() {
        try {
            this.previewImage.Picture.Bitmap.Height = this.previewImage.Height;
            this.previewImage.Picture.Bitmap.Width = this.previewImage.Width;
        } catch (Exception e) {
            this.previewImage.Picture.Bitmap.Height = 1;
            this.previewImage.Picture.Bitmap.Width = 1;
        }
        this.drawPreview(this.focusedTdo());
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 400;
        UNRESOLVED.ptMinTrackSize.y = 315;
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
        this.updateForChangeToSelectedTdos();
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Using_the_3D_object_mover");
    }
    
}
class PdTdoMoverRenameCommand extends PdCommand {
    public KfObject3D tdo;
    public String oldName;
    public String newName;
    public TListCollection list;
    public boolean listChangedBeforeCommand;
    
    // ------------------------------------------------------------------------------ *commands 
    // ------------------------------------------------------------------- PdTdoMoverRenameCommand 
    public void createWithTdoNewNameAndList(KfObject3D aTdo, String aNewName, TListCollection aList) {
        super.create();
        UNRESOLVED.commandChangesPlantFile = false;
        this.tdo = aTdo;
        this.oldName = this.tdo.getName;
        this.newName = aNewName;
        this.list = aList;
        this.listChangedBeforeCommand = TdoMoverForm.listHasChanged(this.list);
    }
    
    public void doCommand() {
        //not redo
        super.doCommand();
        this.tdo.setName(this.newName);
        TdoMoverForm.setChangedFlagForTdoList(true, this.list);
    }
    
    public void undoCommand() {
        super.undoCommand();
        this.tdo.setName(this.oldName);
        TdoMoverForm.setChangedFlagForTdoList(this.listChangedBeforeCommand, this.list);
    }
    
    public String description() {
        result = "";
        result = "rename";
        return result;
    }
    
}
class PdTdoMoverEditCommand extends PdCommand {
    public KfObject3D tdo;
    public KfObject3D oldTdo;
    public KfObject3D newTdo;
    public TListCollection list;
    public boolean listChangedBeforeCommand;
    
    // ----------------------------------------------------------------------- PdTdoMoverEditCommand 
    public void createWithTdoNewTdoAndList(KfObject3D aTdo, KfObject3D aNewTdo, TListCollection aList) {
        super.create();
        UNRESOLVED.commandChangesPlantFile = false;
        this.tdo = aTdo;
        this.oldTdo = UNRESOLVED.KfObject3D.create;
        this.oldTdo.copyFrom(aTdo);
        this.newTdo = UNRESOLVED.KfObject3D.create;
        this.newTdo.copyFrom(aNewTdo);
        this.list = aList;
        this.listChangedBeforeCommand = TdoMoverForm.listHasChanged(this.list);
    }
    
    public void destroy() {
        this.oldTdo.free;
        this.oldTdo = null;
        this.newTdo.free;
        this.newTdo = null;
        super.destroy();
    }
    
    public void doCommand() {
        //not redo
        super.doCommand();
        this.tdo.copyFrom(this.newTdo);
        TdoMoverForm.updateTdoListForList(this.list);
        TdoMoverForm.setChangedFlagForTdoList(true, this.list);
    }
    
    public void undoCommand() {
        super.undoCommand();
        this.tdo.copyFrom(this.oldTdo);
        TdoMoverForm.updateTdoListForList(this.list);
        TdoMoverForm.setChangedFlagForTdoList(this.listChangedBeforeCommand, this.list);
    }
    
    public String description() {
        result = "";
        result = "edit";
        return result;
    }
    
}
class PdCommandWithListOfTdos extends PdCommand {
    public TList tdoList;
    public TListCollection values;
    public KfObject3D tdo;
    
    //for temporary use
    // ----------------------------------------------------------------------- PdCommandWithListOfTdos 
    public void createWithListOfTdos(TList aList) {
        short i = 0;
        
        super.create();
        this.tdoList = delphi_compatability.TList().Create();
        if (aList.Count > 0) {
            for (i = 0; i <= aList.Count - 1; i++) {
                this.tdoList.Add(aList.Items[i]);
            }
        }
        this.values = UNRESOLVED.TListCollection.create;
    }
    
    public void destroy() {
        this.tdoList.free;
        this.tdoList = null;
        this.values.free;
        this.values = null;
        super.destroy();
    }
    
}
//use for cut and delete
class PdTdoMoverRemoveCommand extends PdCommandWithListOfTdos {
    public TList removedTdos;
    public TListCollection list;
    public boolean listChangedBeforeCommand;
    
    // ----------------------------------------------------------------------- PdTdoMoverRemoveCommand 
    public void createWithSelectedTdosAndList(TList listOfTdos, TListCollection aList) {
        super.createWithListOfTdos(listOfTdos);
        UNRESOLVED.commandChangesPlantFile = false;
        this.list = aList;
        this.listChangedBeforeCommand = TdoMoverForm.listHasChanged(this.list);
        this.removedTdos = delphi_compatability.TList().Create();
    }
    
    public void destroy() {
        short i = 0;
        
        if ((UNRESOLVED.done) && (this.removedTdos != null) && (this.removedTdos.Count > 0)) {
            for (i = 0; i <= this.removedTdos.Count - 1; i++) {
                // free copies of cut tdos if change was done 
                this.tdo = UNRESOLVED.KfObject3D(this.removedTdos.Items[i]);
                this.tdo.free;
            }
        }
        this.removedTdos.free;
        this.removedTdos = null;
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        
        //not redo
        super.doCommand();
        if (this.tdoList.Count <= 0) {
            return;
        }
        // save copy of tdos before deleting 
        this.removedTdos.Clear();
        for (i = 0; i <= this.tdoList.Count - 1; i++) {
            // don't remove tdos from list until all indexes have been recorded 
            this.tdo = UNRESOLVED.KfObject3D(this.tdoList.Items[i]);
            this.removedTdos.Add(this.tdo);
            this.tdo.indexWhenRemoved = this.list.indexOf(this.tdo);
            this.tdo.selectedIndexWhenRemoved = TdoMoverForm.selectedTdos.IndexOf(this.tdo);
        }
        for (i = 0; i <= this.tdoList.Count - 1; i++) {
            this.list.remove(UNRESOLVED.KfObject3D(this.tdoList.Items[i]));
        }
        for (i = 0; i <= this.tdoList.Count - 1; i++) {
            TdoMoverForm.selectedTdos.Remove(UNRESOLVED.KfObject3D(this.tdoList.Items[i]));
        }
        TdoMoverForm.updateTdoListForList(this.list);
        TdoMoverForm.setChangedFlagForTdoList(true, this.list);
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.removedTdos.Count > 0) {
            for (i = 0; i <= this.removedTdos.Count - 1; i++) {
                this.tdo = UNRESOLVED.KfObject3D(this.removedTdos.Items[i]);
                if ((this.tdo.indexWhenRemoved >= 0) && (this.tdo.indexWhenRemoved <= this.list.count - 1)) {
                    this.list.insert(this.tdo.indexWhenRemoved, this.tdo);
                } else {
                    this.list.add(this.tdo);
                }
                if ((this.tdo.selectedIndexWhenRemoved >= 0) && (this.tdo.selectedIndexWhenRemoved <= TdoMoverForm.selectedTdos.Count - 1)) {
                    // all removed tdos must have been selected, so also add them to the selected list 
                    TdoMoverForm.selectedTdos.Insert(this.tdo.selectedIndexWhenRemoved, this.tdo);
                } else {
                    TdoMoverForm.selectedTdos.Add(this.tdo);
                }
            }
            TdoMoverForm.updateTdoListForList(this.list);
            TdoMoverForm.setChangedFlagForTdoList(this.listChangedBeforeCommand, this.list);
        }
    }
    
    public String description() {
        result = "";
        result = "delete";
        return result;
    }
    
}
class PdTdoMoverTransferCommand extends PdCommandWithListOfTdos {
    public boolean isTransfer;
    public TListCollection list;
    public boolean listChangedBeforeCommand;
    
    // ------------------------------------------------------------------ PdTdoMoverTransferCommand 
    public void createWithSelectedTdosAndList(TList listOfTdos, TListCollection aList) {
        super.createWithListOfTdos(listOfTdos);
        UNRESOLVED.commandChangesPlantFile = false;
        this.list = aList;
        this.listChangedBeforeCommand = TdoMoverForm.listHasChanged(this.list);
    }
    
    public void destroy() {
        short i = 0;
        
        if ((!UNRESOLVED.done) && (this.tdoList != null) && (this.tdoList.Count > 0)) {
            for (i = 0; i <= this.tdoList.Count - 1; i++) {
                // free copies of pasted tdos if change was undone 
                this.tdo = UNRESOLVED.KfObject3D(this.tdoList.Items[i]);
                this.tdo.free;
            }
        }
        //will free tdoList
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        
        //not redo
        super.doCommand();
        if (this.tdoList.Count > 0) {
            TdoMoverForm.deselectAllTdos();
            for (i = 0; i <= this.tdoList.Count - 1; i++) {
                this.tdo = UNRESOLVED.KfObject3D(this.tdoList.Items[i]);
                this.list.add(this.tdo);
                TdoMoverForm.selectedTdos.Add(this.tdo);
            }
            TdoMoverForm.updateTdoListForList(this.list);
            TdoMoverForm.setChangedFlagForTdoList(true, this.list);
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.tdoList.Count > 0) {
            for (i = 0; i <= this.tdoList.Count - 1; i++) {
                this.tdo = UNRESOLVED.KfObject3D(this.tdoList.Items[i]);
                this.list.remove(this.tdo);
                TdoMoverForm.selectedTdos.Remove(this.tdo);
            }
            TdoMoverForm.updateTdoListForList(this.list);
            TdoMoverForm.setChangedFlagForTdoList(this.listChangedBeforeCommand, this.list);
        }
    }
    
    public String description() {
        result = "";
        result = "transfer";
        return result;
    }
    
}
class PdTdoMoverDuplicateCommand extends PdCommandWithListOfTdos {
    public TList newTdos;
    public TListCollection list;
    public boolean listChangedBeforeCommand;
    
    // ------------------------------------------------------------------------------ PdTdoMoverDuplicateCommand 
    public void createWithSelectedTdosAndList(TList listOfTdos, TListCollection aList) {
        super.createWithListOfTdos(listOfTdos);
        UNRESOLVED.commandChangesPlantFile = false;
        this.newTdos = delphi_compatability.TList().Create();
        this.list = aList;
        this.listChangedBeforeCommand = TdoMoverForm.listHasChanged(this.list);
    }
    
    public void destroy() {
        short i = 0;
        
        if ((!UNRESOLVED.done) && (this.newTdos != null) && (this.newTdos.Count > 0)) {
            for (i = 0; i <= this.newTdos.Count - 1; i++) {
                // free copies of created tdos if change was undone 
                this.tdo = UNRESOLVED.KfObject3D(this.newTdos.Items[i]);
                this.tdo.free;
            }
        }
        this.newTdos.free;
        this.newTdos = null;
        //will free tdoList
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        KfObject3D tdoCopy = new KfObject3D();
        
        super.doCommand();
        if (this.tdoList.Count > 0) {
            TdoMoverForm.deselectAllTdos();
            for (i = 0; i <= this.tdoList.Count - 1; i++) {
                this.tdo = UNRESOLVED.KfObject3D(this.tdoList.Items[i]);
                tdoCopy = UNRESOLVED.KfObject3D.create;
                this.tdo.copyTo(tdoCopy);
                tdoCopy.setName("Copy of " + tdoCopy.getName);
                this.newTdos.Add(tdoCopy);
                this.list.add(tdoCopy);
                TdoMoverForm.selectedTdos.Add(tdoCopy);
            }
            TdoMoverForm.updateTdoListForList(this.list);
            TdoMoverForm.setChangedFlagForTdoList(true, this.list);
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.newTdos.Count > 0) {
            for (i = 0; i <= this.newTdos.Count - 1; i++) {
                this.tdo = UNRESOLVED.KfObject3D(this.newTdos.Items[i]);
                this.list.remove(this.tdo);
                TdoMoverForm.selectedTdos.Remove(this.tdo);
            }
            TdoMoverForm.updateTdoListForList(this.list);
            TdoMoverForm.setChangedFlagForTdoList(this.listChangedBeforeCommand, this.list);
        }
    }
    
    public void redoCommand() {
        short i = 0;
        
        //not redo
        super.doCommand();
        if (this.newTdos.Count > 0) {
            TdoMoverForm.deselectAllTdos();
            for (i = 0; i <= this.newTdos.Count - 1; i++) {
                this.tdo = UNRESOLVED.KfObject3D(this.newTdos.Items[i]);
                this.list.add(this.tdo);
                TdoMoverForm.selectedTdos.Add(this.tdo);
            }
            TdoMoverForm.updateTdoListForList(this.list);
            TdoMoverForm.setChangedFlagForTdoList(true, this.list);
        }
    }
    
    public String description() {
        result = "";
        result = "duplicate";
        return result;
    }
    
}
