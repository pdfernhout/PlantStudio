unit Udebug;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, StdCtrls, Buttons, ExtCtrls,
  updform;
 
type
  TDebugForm = class(PdForm)
    DebugList: TListBox;
    Close: TButton;
    saveListAs: TButton;
    clearList: TButton;
    optionsPanel: TPanel;
    exceptionLabel: TLabel;
    showOnExceptionCheckBox: TCheckBox;
    logToFile: TCheckBox;
    helpButton: TSpeedButton;
    supportButton: TButton;
    procedure CloseClick(Sender: TObject);
    procedure saveListAsClick(Sender: TObject);
    procedure clearListClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure FormResize(Sender: TObject);
    procedure logToFileClick(Sender: TObject);
    procedure FormDestroy(Sender: TObject);
    procedure showOnExceptionCheckBoxClick(Sender: TObject);
    procedure supportButtonClick(Sender: TObject);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
  public
    { Public declarations }
    outputFile: TextFile;
    logging: boolean;
    procedure print(aString: string);
    procedure printNested(level: longint; aString: string);
    procedure clear;
		procedure startLogging(fileName: string);
		procedure stopLogging;
    procedure saveExceptionListToFile(fileName: string);
  end;

procedure DebugPrint(aMessage: string);

var
  DebugForm: TDebugForm;

implementation

{$R *.DFM}

uses udomain, usupport, umath, uprginfo, umain;

procedure DebugPrint(aMessage: string);
	begin
  if debugForm <> nil then DebugForm.print(aMessage);
  end;

procedure TDebugForm.FormCreate(Sender: TObject);
  var tempBoundsRect: TRect;
  begin
  { keep window on screen - left corner of title bar }
  tempBoundsRect := domain.debugWindowRect;
  with tempBoundsRect do
    if (left <> 0) or (right <> 0) or (top <> 0) or (bottom <> 0) then
      begin
      if left > screen.width - kMinWidthOnScreen then left := screen.width - kMinWidthOnScreen;
      if top > screen.height - kMinHeightOnScreen then top := screen.height - kMinHeightOnScreen;
      self.setBounds(left, top, right, bottom);
      end;
  showOnExceptionCheckBox.checked := domain.options.showWindowOnException;
  logToFile.checked := domain.options.logToFileOnException;
  { this will make the list box create a horizontal scroll bar }
  sendMessage(debugList.handle, LB_SETHORIZONTALEXTENT, 1000, longint(0));
  end;

procedure TDebugForm.FormDestroy(Sender: TObject);
  begin
  self.stopLogging;
  end;

procedure TDebugForm.startLogging(fileName: string);
  var dateString: string;
	begin
  if logging then exit;
	assignFile(outputFile, fileName);
	if not fileExists(fileName) then
    begin
    setDecimalSeparator; // v1.5
    rewrite(outputFile);
    end
  else
    begin
    setDecimalSeparator; // v1.5
    append(outputFile);
    dateString := formatDateTime('m/d/yyyy, h:m am/pm', now);
    writeln(outputFile, '---- log start (' + dateString + ') ----');
    end;
  logging := true;
  end;

procedure TDebugForm.stopLogging;
	begin
  if not logging then exit;
  writeln(outputFile, '---- log stop ----');
  closeFile(outputFile);
  logging := false;
	end;

procedure TDebugForm.saveExceptionListToFile(fileName: string);
  var i: longint;
  begin
	assignFile(outputFile, fileName);
  setDecimalSeparator; // v1.5
	rewrite(outputFile);
  try
  if debugList.items.count > 0 then
    for i := 0 to debugList.items.count - 1 do
      writeln(outputFile, debugList.items[i]);
  finally
  closeFile(outputFile);
  end;
  end;

procedure TDebugForm.printNested(level: longint; aString: string);
  var
  i: longint;
  prefix: ansistring;
	begin
  if level > 40 then level := 40;
  prefix := '';
  if level > 0 then
  	for i := 1 to level do
    	AppendStr(prefix, '..');
  print(prefix + aString);
  end;

procedure TDebugForm.print(aString: string);
	begin
  if logging then
  	begin
  	writeln(outputFile, aString);
    flush(outputFile);
    end;
  if domain.options.showWindowOnException then
    begin
    self.visible := true;
    self.bringToFront;
    end;
  if debugList.items.count > 1000 then debugList.items.clear;
  try
    DebugList.items.add(aString);
  except
    on EOutOfResources do
      debugList.items.clear;
  end;
  DebugList.itemIndex := DebugList.items.count - 1;
  debugList.invalidate;
  debugList.refresh;
  end;

procedure TDebugForm.clear;
	begin
  self.visible := false;
  debugList.items.clear;
  end;

procedure TDebugForm.CloseClick(Sender: TObject);
  begin
  self.visible := false;
  end;

procedure TDebugForm.saveListAsClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
	begin
  if debugList.items.count <= 0 then exit;
  if not getFileSaveInfo(kFileTypeExceptionList, kAskForFileName, 'pstudio.nex', fileInfo) then exit;
  try
    self.saveExceptionListToFile(fileInfo.tempFile);
    fileInfo.writingWasSuccessful := true;
  finally
    cleanUpAfterFileSave(fileInfo);
  end;
	end;

procedure TDebugForm.clearListClick(Sender: TObject);
  begin
  if debugList.items.count <= 0 then exit;
  debugList.items.clear;
  end;

procedure TDebugForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Numerical_exceptions');
  end;

const kBetweenGap = 4;

procedure TDebugForm.FormResize(Sender: TObject);
  begin
  if Application.terminated then exit;
  close.left := self.clientWidth - close.width - kBetweenGap;
  saveListAs.left := close.left;
  clearList.left := close.left;
  helpButton.left := close.left;
  supportButton.left := close.left;
  with debugList do setBounds(kBetweenGap, kBetweenGap,
    close.left - kBetweenGap * 2, intMax(0, self.clientHeight - optionsPanel.height - kBetweenGap * 3));
  with optionsPanel do setBounds(kBetweenGap, intMax(0, self.clientHeight - height - kBetweenGap),
    close.left - kBetweenGap * 2, height);
  end;

procedure TDebugForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 350;
    ptMinTrackSize.y := 190;
    end;
  end;

procedure TDebugForm.logToFileClick(Sender: TObject);
  begin
  domain.options.logToFileOnException := logToFile.checked;
  if not logging then
    startLogging(ExtractFilePath(Application.exeName) + 'errors.nex')
  else
    stopLogging;
  logging := logToFile.checked;
  end;

procedure TDebugForm.showOnExceptionCheckBoxClick(Sender: TObject);
  begin
  domain.options.showWindowOnException := showOnExceptionCheckBox.checked;
  end;

procedure TDebugForm.supportButtonClick(Sender: TObject);
  var infoForm: TProgramInfoForm;
  begin
  infoForm := TProgramInfoForm.create(Application);
  try
    infoForm.showModal;
  finally
    infoForm.free;
    infoForm := nil;
  end;
  end;

end.
