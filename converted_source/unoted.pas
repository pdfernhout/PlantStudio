unit unoted;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Buttons, updform;

type
  TNoteEditForm = class(PdForm)
    OK: TButton;
    cancel: TButton;
    noteEditMemo: TMemo;
    wrapLines: TCheckBox;
    helpButton: TSpeedButton;
    procedure FormResize(Sender: TObject);
    procedure wrapLinesClick(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

implementation

{$R *.DFM}

uses udomain;

const kBetweenGap = 4;

procedure TNoteEditForm.FormCreate(Sender: TObject);
  begin
  noteEditMemo.wordWrap := domain.options.noteEditorWrapLines;
  wrapLines.checked := domain.options.noteEditorWrapLines;
  end;

procedure TNoteEditForm.FormResize(Sender: TObject);
  begin
  OK.left := self.clientWidth - OK.width - kBetweenGap;
  Cancel.left := OK.left;
  helpButton.left := OK.left;
  wrapLines.left := OK.left + kBetweenGap;
  with noteEditMemo do setBounds(kBetweenGap, kBetweenGap,
    OK.left - kBetweenGap * 2, self.clientHeight - kBetweenGap * 2);
  end;

procedure TNoteEditForm.wrapLinesClick(Sender: TObject);
  begin
  domain.options.noteEditorWrapLines := wrapLines.checked;
  noteEditMemo.wordWrap := domain.options.noteEditorWrapLines;
  end;

procedure TNoteEditForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Editing_plant_notes');
  end;

end.
