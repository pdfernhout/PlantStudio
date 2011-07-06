# unit Uundo

from conversion_common import *
import umain
import udomain
import umath
import updform
import ucommand
import delphi_compatability

# const
kBetweenGap = 4

class TUndoRedoListForm(PdForm):
    def __init__(self):
        self.OK = TButton()
        self.cancel = TButton()
        self.helpButton = TSpeedButton()
        self.undoListLabel = TLabel()
        self.redoListLabel = TLabel()
        self.undoList = TListBox()
        self.redoList = TListBox()
    
    #$R *.DFM
    def FormCreate(self, Sender):
        tempBoundsRect = TRect()
        
        # keep window on screen - left corner of title bar 
        tempBoundsRect = udomain.domain.undoRedoListWindowRect
        if (tempBoundsRect.Left != 0) or (tempBoundsRect.Right != 0) or (tempBoundsRect.Top != 0) or (tempBoundsRect.Bottom != 0):
            if tempBoundsRect.Left > delphi_compatability.Screen.Width - umain.kMinWidthOnScreen:
                tempBoundsRect.Left = delphi_compatability.Screen.Width - umain.kMinWidthOnScreen
            if tempBoundsRect.Top > delphi_compatability.Screen.Height - umain.kMinHeightOnScreen:
                tempBoundsRect.Top = delphi_compatability.Screen.Height - umain.kMinHeightOnScreen
            self.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom)
        # make list boxes have horizontal scroll bars
        UNRESOLVED.sendMessage(self.undoList.Handle, UNRESOLVED.LB_SETHORIZONTALEXTENT, 1000, 0)
        UNRESOLVED.sendMessage(self.redoList.Handle, UNRESOLVED.LB_SETHORIZONTALEXTENT, 1000, 0)
    
    def initializeWithCommandList(self, commandList):
        aList = TStringList()
        
        aList = delphi_compatability.TStringList.create
        try:
            commandList.fillListWithUndoableStrings(aList)
            self.undoList.Items.Assign(aList)
            aList.Clear()
            commandList.fillListWithRedoableStrings(aList)
            self.redoList.Items.Assign(aList)
        finally:
            aList.free
        self.OK.Enabled = (self.undoList.SelCount > 0) or (self.redoList.SelCount > 0)
    
    def undoToIndex(self):
        result = 0
        i = 0
        
        result = -1
        if self.undoList.Items.Count > 0:
            for i in range(self.undoList.Items.Count - 1, 0 + 1):
                if self.undoList.Selected[i]:
                    result = i
                    return result
        return result
    
    def redoToIndex(self):
        result = 0
        i = 0
        
        result = -1
        if self.redoList.Items.Count > 0:
            for i in range(self.redoList.Items.Count - 1, 0 + 1):
                if self.redoList.Selected[i]:
                    result = i
                    return result
        return result
    
    def regulateListSelections(self, Sender):
        i = 0
        thisListBox = TListBox()
        otherListBox = TListBox()
        
        if (Sender == None) or (not (Sender.__class__ is delphi_compatability.TListBox)):
            raise GeneralException.create("Problem: Wrong sender in method TUndoRedoListForm.regulateListSelections.")
        thisListBox = Sender as delphi_compatability.TListBox
        if Sender == self.undoList:
            otherListBox = self.redoList
        else:
            otherListBox = self.undoList
        if Sender == self.undoList:
            self.OK.Caption = "Un&do"
        else:
            self.OK.Caption = "Re&do"
        self.OK.Enabled = (self.undoList.SelCount > 0) or (self.redoList.SelCount > 0)
        if thisListBox.ItemIndex >= 0:
            for i in range(0, thisListBox.ItemIndex + 1):
                thisListBox.Selected[i] = true
        if thisListBox.ItemIndex + 1 <= thisListBox.Items.Count - 1:
            for i in range(thisListBox.ItemIndex + 1, thisListBox.Items.Count):
                thisListBox.Selected[i] = false
        if otherListBox.Items.Count > 0:
            for i in range(0, otherListBox.Items.Count):
                otherListBox.Selected[i] = false
        otherListBox.ItemIndex = -1
    
    def OKClick(self, Sender):
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def FormClose(self, Sender, Action):
        udomain.domain.undoRedoListWindowRect = Rect(self.Left, self.Top, self.Width, self.Height)
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Using_the_undo/redo_list")
    
    def FormResize(self, Sender):
        listHeight = 0
        
        if delphi_compatability.Application.terminated:
            return
        self.OK.Left = self.ClientWidth - self.OK.Width - kBetweenGap
        self.cancel.Left = self.OK.Left
        self.helpButton.Left = self.OK.Left
        self.undoListLabel.SetBounds(kBetweenGap, kBetweenGap, self.undoListLabel.Width, self.undoListLabel.Height)
        listHeight = umath.intMax(0, (self.ClientHeight - self.undoListLabel.Height * 2 - kBetweenGap * 5) / 2)
        self.undoList.SetBounds(kBetweenGap, self.undoListLabel.Top + self.undoListLabel.Height + kBetweenGap, self.OK.Left - kBetweenGap * 2, listHeight)
        self.redoListLabel.SetBounds(kBetweenGap, self.undoList.Top + self.undoList.Height + kBetweenGap, self.redoListLabel.Width, self.redoListLabel.Height)
        self.redoList.SetBounds(kBetweenGap, self.redoListLabel.Top + self.redoListLabel.Height + kBetweenGap, self.OK.Left - kBetweenGap * 2, listHeight)
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 220
        UNRESOLVED.ptMinTrackSize.y = 220
    
