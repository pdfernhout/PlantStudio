// unit unoted

from conversion_common import *;
import updform;
import delphi_compatability;

// const
kBetweenGap = 4;



class TNoteEditForm extends PdForm {
    public TButton OK;
    public TButton cancel;
    public TMemo noteEditMemo;
    public TCheckBox wrapLines;
    public TSpeedButton helpButton;
    
    //$R *.DFM
    public void FormCreate(TObject Sender) {
        this.noteEditMemo.WordWrap = UNRESOLVED.domain.options.noteEditorWrapLines;
        this.wrapLines.Checked = UNRESOLVED.domain.options.noteEditorWrapLines;
    }
    
    public void FormResize(TObject Sender) {
        this.OK.Left = this.ClientWidth - this.OK.Width - kBetweenGap;
        this.cancel.Left = this.OK.Left;
        this.helpButton.Left = this.OK.Left;
        this.wrapLines.Left = this.OK.Left + kBetweenGap;
        this.noteEditMemo.SetBounds(kBetweenGap, kBetweenGap, this.OK.Left - kBetweenGap * 2, this.ClientHeight - kBetweenGap * 2);
    }
    
    public void wrapLinesClick(TObject Sender) {
        UNRESOLVED.domain.options.noteEditorWrapLines = this.wrapLines.Checked;
        this.noteEditMemo.WordWrap = UNRESOLVED.domain.options.noteEditorWrapLines;
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Editing_plant_notes");
    }
    
}
