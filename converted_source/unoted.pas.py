# unit unoted

from conversion_common import *
import udomain
import updform
import delphi_compatability

# const
kBetweenGap = 4

class TNoteEditForm(PdForm):
    def __init__(self):
        self.OK = TButton()
        self.cancel = TButton()
        self.noteEditMemo = TMemo()
        self.wrapLines = TCheckBox()
        self.helpButton = TSpeedButton()
    
    #$R *.DFM
    def FormCreate(self, Sender):
        self.noteEditMemo.WordWrap = udomain.domain.options.noteEditorWrapLines
        self.wrapLines.Checked = udomain.domain.options.noteEditorWrapLines
    
    def FormResize(self, Sender):
        self.OK.Left = self.ClientWidth - self.OK.Width - kBetweenGap
        self.cancel.Left = self.OK.Left
        self.helpButton.Left = self.OK.Left
        self.wrapLines.Left = self.OK.Left + kBetweenGap
        self.noteEditMemo.SetBounds(kBetweenGap, kBetweenGap, self.OK.Left - kBetweenGap * 2, self.ClientHeight - kBetweenGap * 2)
    
    def wrapLinesClick(self, Sender):
        udomain.domain.options.noteEditorWrapLines = self.wrapLines.Checked
        self.noteEditMemo.WordWrap = udomain.domain.options.noteEditorWrapLines
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Editing_plant_notes")
    
