unit Uwait;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, StdCtrls, ExtCtrls;

type
  TWaitForm = class(TForm)
    Panel1: TPanel;
    messageLabel: TLabel;
    Image1: TImage;
  private
    { Private declarations }
  public
    { Public declarations }
    procedure CreateParams(var Params: TCreateParams); override;
  end;

procedure startWaitMessage(messageString: string);
procedure stopWaitMessage;

var WaitForm: TWaitForm;

implementation

{$R *.DFM}

procedure TWaitForm.CreateParams(var Params: TCreateParams);
  begin
  inherited CreateParams(Params);
  with Params do
    Style :=  Style or WS_BORDER or WS_EX_DLGMODALFRAME;
  end;

procedure startWaitMessage(messageString: string);
  begin
  if messageString = '' then exit;
  if WaitForm = nil then exit;
  if WaitForm.messageLabel = nil then exit;
  if WaitForm.messageLabel.canvas = nil then exit;
  with WaitForm.messageLabel do
    begin
    caption := messageString;
    WaitForm.clientWidth := left + width + 12;
    if WaitForm.clientHeight < canvas.textHeight('W') + 8 then
      WaitForm.clientHeight := canvas.textHeight('W') + 8;
    invalidate;
    end;
  WaitForm.show;
  application.processMessages;
  end;

procedure stopWaitMessage;
  begin
  waitForm.hide;
  application.processMessages;
  end;

end.
