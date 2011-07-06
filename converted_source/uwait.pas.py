# unit Uwait

from conversion_common import *
import delphi_compatability

# var
WaitForm = TWaitForm()

def startWaitMessage(messageString):
    if messageString == "":
        return
    if WaitForm == None:
        return
    if WaitForm.messageLabel == None:
        return
    if WaitForm.messageLabel.Canvas == None:
        return
    WaitForm.messageLabel.Caption = messageString
    WaitForm.ClientWidth = WaitForm.messageLabel.Left + WaitForm.messageLabel.Width + 12
    if WaitForm.ClientHeight < WaitForm.messageLabel.Canvas.TextHeight("W") + 8:
        WaitForm.ClientHeight = WaitForm.messageLabel.Canvas.TextHeight("W") + 8
    WaitForm.messageLabel.Invalidate()
    WaitForm.Show()
    delphi_compatability.Application.ProcessMessages()

def stopWaitMessage():
    WaitForm.Hide()
    delphi_compatability.Application.ProcessMessages()

class TWaitForm(TForm):
    def __init__(self):
        self.Panel1 = TPanel()
        self.messageLabel = TLabel()
        self.Image1 = TImage()
    
    #$R *.DFM
    def CreateParams(self, Params):
        TForm.CreateParams(self, Params)
        Params.Style = Params.Style or delphi_compatability.WS_BORDER or delphi_compatability.WS_EX_DLGMODALFRAME
    
