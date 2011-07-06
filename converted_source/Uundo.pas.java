// unit Uundo

from conversion_common import *;
import updform;
import delphi_compatability;

// const
kBetweenGap = 4;



class TUndoRedoListForm extends PdForm {
    public TButton OK;
    public TButton cancel;
    public TSpeedButton helpButton;
    public TLabel undoListLabel;
    public TLabel redoListLabel;
    public TListBox undoList;
    public TListBox redoList;
    
    //$R *.DFM
    public void FormCreate(TObject Sender) {
        TRect tempBoundsRect = new TRect();
        
        // keep window on screen - left corner of title bar 
        tempBoundsRect = UNRESOLVED.domain.undoRedoListWindowRect;
        if ((tempBoundsRect.Left != 0) || (tempBoundsRect.Right != 0) || (tempBoundsRect.Top != 0) || (tempBoundsRect.Bottom != 0)) {
            if (tempBoundsRect.Left > delphi_compatability.Screen.Width - UNRESOLVED.kMinWidthOnScreen) {
                tempBoundsRect.Left = delphi_compatability.Screen.Width - UNRESOLVED.kMinWidthOnScreen;
            }
            if (tempBoundsRect.Top > delphi_compatability.Screen.Height - UNRESOLVED.kMinHeightOnScreen) {
                tempBoundsRect.Top = delphi_compatability.Screen.Height - UNRESOLVED.kMinHeightOnScreen;
            }
            this.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom);
        }
        // make list boxes have horizontal scroll bars
        UNRESOLVED.sendMessage(this.undoList.Handle, UNRESOLVED.LB_SETHORIZONTALEXTENT, 1000, 0);
        UNRESOLVED.sendMessage(this.redoList.Handle, UNRESOLVED.LB_SETHORIZONTALEXTENT, 1000, 0);
    }
    
    public void initializeWithCommandList(PdCommandList commandList) {
        TStringList aList = new TStringList();
        
        aList = delphi_compatability.TStringList.create;
        try {
            commandList.fillListWithUndoableStrings(aList);
            this.undoList.Items.Assign(aList);
            aList.Clear();
            commandList.fillListWithRedoableStrings(aList);
            this.redoList.Items.Assign(aList);
        } finally {
            aList.free;
        }
        this.OK.Enabled = (this.undoList.SelCount > 0) || (this.redoList.SelCount > 0);
    }
    
    public int undoToIndex() {
        result = 0;
        int i = 0;
        
        result = -1;
        if (this.undoList.Items.Count > 0) {
            for (i = this.undoList.Items.Count - 1; i >= 0; i--) {
                if (this.undoList.Selected[i]) {
                    result = i;
                    return result;
                }
            }
        }
        return result;
    }
    
    public int redoToIndex() {
        result = 0;
        int i = 0;
        
        result = -1;
        if (this.redoList.Items.Count > 0) {
            for (i = this.redoList.Items.Count - 1; i >= 0; i--) {
                if (this.redoList.Selected[i]) {
                    result = i;
                    return result;
                }
            }
        }
        return result;
    }
    
    public void regulateListSelections(TObject Sender) {
        int i = 0;
        TListBox thisListBox = new TListBox();
        TListBox otherListBox = new TListBox();
        
        if ((Sender == null) || (!(Sender instanceof delphi_compatability.TListBox))) {
            throw new GeneralException.create("Problem: Wrong sender in method TUndoRedoListForm.regulateListSelections.");
        }
        thisListBox = (delphi_compatability.TListBox)Sender;
        if (Sender == this.undoList) {
            otherListBox = this.redoList;
        } else {
            otherListBox = this.undoList;
        }
        if (Sender == this.undoList) {
            this.OK.Caption = "Un&do";
        } else {
            this.OK.Caption = "Re&do";
        }
        this.OK.Enabled = (this.undoList.SelCount > 0) || (this.redoList.SelCount > 0);
        if (thisListBox.ItemIndex >= 0) {
            for (i = 0; i <= thisListBox.ItemIndex; i++) {
                thisListBox.Selected[i] = true;
            }
        }
        if (thisListBox.ItemIndex + 1 <= thisListBox.Items.Count - 1) {
            for (i = thisListBox.ItemIndex + 1; i <= thisListBox.Items.Count - 1; i++) {
                thisListBox.Selected[i] = false;
            }
        }
        if (otherListBox.Items.Count > 0) {
            for (i = 0; i <= otherListBox.Items.Count - 1; i++) {
                otherListBox.Selected[i] = false;
            }
        }
        otherListBox.ItemIndex = -1;
    }
    
    public void OKClick(TObject Sender) {
        this.ModalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    public void FormClose(TObject Sender, TCloseAction Action) {
        UNRESOLVED.domain.undoRedoListWindowRect = Rect(this.Left, this.Top, this.Width, this.Height);
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Using_the_undo/redo_list");
    }
    
    public void FormResize(TObject Sender) {
        int listHeight = 0;
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        this.OK.Left = this.ClientWidth - this.OK.Width - kBetweenGap;
        this.cancel.Left = this.OK.Left;
        this.helpButton.Left = this.OK.Left;
        this.undoListLabel.SetBounds(kBetweenGap, kBetweenGap, this.undoListLabel.Width, this.undoListLabel.Height);
        listHeight = UNRESOLVED.intMax(0, (this.ClientHeight - this.undoListLabel.Height * 2 - kBetweenGap * 5) / 2);
        this.undoList.SetBounds(kBetweenGap, this.undoListLabel.Top + this.undoListLabel.Height + kBetweenGap, this.OK.Left - kBetweenGap * 2, listHeight);
        this.redoListLabel.SetBounds(kBetweenGap, this.undoList.Top + this.undoList.Height + kBetweenGap, this.redoListLabel.Width, this.redoListLabel.Height);
        this.redoList.SetBounds(kBetweenGap, this.redoListLabel.Top + this.redoListLabel.Height + kBetweenGap, this.OK.Left - kBetweenGap * 2, listHeight);
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 220;
        UNRESOLVED.ptMinTrackSize.y = 220;
    }
    
}
