// unit Uwait

from conversion_common import *;
import delphi_compatability;

// var
TWaitForm WaitForm = new TWaitForm();


public void startWaitMessage(String messageString) {
    if (messageString == "") {
        return;
    }
    if (WaitForm == null) {
        return;
    }
    if (WaitForm.messageLabel == null) {
        return;
    }
    if (WaitForm.messageLabel.Canvas == null) {
        return;
    }
    WaitForm.messageLabel.Caption = messageString;
    WaitForm.ClientWidth = WaitForm.messageLabel.Left + WaitForm.messageLabel.Width + 12;
    if (WaitForm.ClientHeight < WaitForm.messageLabel.Canvas.TextHeight("W") + 8) {
        WaitForm.ClientHeight = WaitForm.messageLabel.Canvas.TextHeight("W") + 8;
    }
    WaitForm.messageLabel.Invalidate();
    WaitForm.Show();
    delphi_compatability.Application.ProcessMessages();
}

public void stopWaitMessage() {
    WaitForm.Hide();
    delphi_compatability.Application.ProcessMessages();
}


class TWaitForm extends TForm {
    public TPanel Panel1;
    public TLabel messageLabel;
    public TImage Image1;
    
    //$R *.DFM
    public void CreateParams(TCreateParams Params) {
        super.CreateParams(Params);
        Params.Style = Params.Style || delphi_compatability.WS_BORDER || delphi_compatability.WS_EX_DLGMODALFRAME;
    }
    
}
