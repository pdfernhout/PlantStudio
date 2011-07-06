unit upicktdo;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Buttons, Grids, ExtCtrls,
  ucollect, utdo, uparams, updform;

type
  TPickTdoForm = class(PdForm)
    grid: TDrawGrid;
    Close: TButton;
    cancel: TButton;
    newTdo: TButton;
    libraryGroupBox: TGroupBox;
    fileChangedImage: TImage;
    libraryFileName: TEdit;
    apply: TButton;
    helpButton: TSpeedButton;
    sectionTdosChangeLibrary: TSpeedButton;
    editTdo: TButton;
    mover: TButton;
    copyTdo: TButton;
    deleteTdo: TButton;
    tdos: TComboBox;
    procedure gridDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure sectionTdosChangeLibraryClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure CloseClick(Sender: TObject);
    procedure applyClick(Sender: TObject);
    procedure gridDblClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure editTdoClick(Sender: TObject);
    procedure newTdoClick(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure gridSelectCell(Sender: TObject; Col, Row: Integer;
      var CanSelect: Boolean);
    procedure FormResize(Sender: TObject);
    procedure moverClick(Sender: TObject);
    procedure copyTdoClick(Sender: TObject);
    procedure deleteTdoClick(Sender: TObject);
    procedure tdosChange(Sender: TObject);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
  public
    param: PdParameter;
    originalTdo: KfObject3D;
    tdoSelectionChanged, libraryChanged, editedTdo: boolean;
    internalChange: boolean;
    { Public declarations }
    procedure loadNewTdoLibrary;
    function readTdosFromFile: boolean;
    procedure saveTdosToLibrary;
    function tdoForIndex(index: smallint): KfObject3D;
    function initializeWithTdoParameterAndPlantName(aTdo: KfObject3d; aParam: PdParameter; const aName: string): boolean;
    function selectedTdo: KfObject3D;
    procedure selectTdoAtIndex(indexToSelect: smallint);
    function hintForTdosDrawGridAtPoint(aComponent: TComponent; aPoint: TPoint; var cursorRect: TRect): string;
    procedure setLibraryChanged(fileChanged: boolean);
    procedure chooseTdoFromList(index: smallint);
    procedure selectTdoBasedOn(aTdo: KfObject3D);
  end;

implementation

uses usupport, udomain, uturtle, umain, utdoedit, updcom, utdomove;

{$R *.DFM}
function TPickTdoForm.initializeWithTdoParameterAndPlantName(aTdo: KfObject3d;
    aParam: PdParameter; const aName: string): boolean;
  begin
  // returns false if user canceled action
  result := true;
  if not self.readTdosFromFile then
    begin
    messageDlg('You cannot change or edit this 3D object' + chr(13)
      + 'until you choose a 3D object library.',
      mtWarning, [mbOk], 0);
    result := false;
    exit;
    end;
  libraryFileName.text := domain.defaultTdoLibraryFileName;
  libraryFileName.selStart := length(libraryFileName.text);
  originalTdo := aTdo;
  if originalTdo = nil then
    raise Exception.create('Problem: Nil 3D object in method TPickTdoForm.initializeWithTdoParameterAndPlantName.');
  param := aParam;
  if param = nil then
    raise Exception.create('Problem: Nil parameter in method TPickTdoForm.initializeWithTdoParameterAndPlantName.');
  self.caption := param.name + ' for ' + aName;
  end;

procedure TPickTdoForm.FormActivate(Sender: TObject);
  begin
  self.selectTdoBasedOn(originalTdo);
  end;

procedure TPickTdoForm.selectTdoBasedOn(aTdo: KfObject3D);
  var
    indexToSelect, i: integer;
    tdo: KfObject3D;
  begin
  // assumes initialize already called and tdos already in list
  indexToSelect := -1;
  if tdos.items.count > 0 then for i := 0 to tdos.items.count - 1 do
    begin
    tdo := KfObject3d(tdos.items.objects[i]);
    if tdo.isSameAs(aTdo) then
      begin
      indexToSelect := i;
      break;
      end;
    end;
  if indexToSelect < 0 then
    begin
    if MessageDlg('This 3D object is not in the current library.'
      + chr(13) + 'Its name or shape is different from the 3D objects in the list.'
      + chr(13)
      + chr(13) + 'Do you want to add this 3D object to the library?', mtWarning, [mbYes, mbNo], 0) = IDNO then
      exit;
    tdo := KfObject3D.create;
    tdo.copyFrom(aTdo);
    tdos.items.addObject(tdo.name, tdo);
    grid.rowCount := tdos.items.count div grid.colCount + 1;
    libraryGroupBox.caption := 'The current library has ' + intToStr(tdos.items.count) + ' object(s)';
    self.setLibraryChanged(true);
    indexToSelect := tdos.items.count - 1;
    end;
  if indexToSelect >= 0 then
    self.selectTdoAtIndex(indexToSelect);
  end;

procedure TPickTdoForm.selectTdoAtIndex(indexToSelect: smallint);
  var
    gridRect: TGridRect;
    lastRow: integer;
  begin
  self.chooseTdoFromList(indexToSelect);
  if (indexToSelect < 0) or (indexToSelect > tdos.items.count - 1) then
    begin
    gridRect.left := -1;
    gridRect.top := -1;
    end
  else
    begin
    gridRect.left := indexToSelect mod grid.colCount;
    gridRect.top := indexToSelect div grid.colCount;
    end;
  gridRect.right := gridRect.left;
  gridRect.bottom := gridRect.top;
  grid.selection := gridRect;
  // keep selection in view
  lastRow := grid.topRow + grid.visibleRowCount - 1;
  if gridRect.top > lastRow then
    grid.topRow := grid.topRow + (gridRect.top - lastRow);
  end;

function TPickTdoForm.selectedTdo: KfObject3D;
  var index: integer;
  begin
  result := nil;
  index := grid.selection.top * grid.colCount + grid.selection.left;
  if (index >= 0) and (index <= tdos.items.count - 1) then
    result := TObject(tdos.items.objects[index]) as KfObject3D;
  end;

procedure TPickTdoForm.chooseTdoFromList(index: smallint);
  begin
  if (index >= 0) and (index <= tdos.items.count - 1) then
    tdos.itemIndex := index;
  end;

procedure TPickTdoForm.CloseClick(Sender: TObject);
  begin
  if (tdoSelectionChanged or editedTdo) and (self.selectedTdo <> nil) then
    self.applyClick(self);
  modalResult := mrOK;
  end;

procedure TPickTdoForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TPickTdoForm.applyClick(Sender: TObject);
  begin
  if self.selectedTdo <> nil then
    MainForm.doCommand(
      PdChangeTdoValueCommand.createCommandWithListOfPlants(
        MainForm.selectedPlants, self.selectedTdo, param.fieldNumber, param.regrow));
  end;

procedure TPickTdoForm.loadNewTdoLibrary;
   var
    fileNameWithPath: string;
  begin
  fileNameWithPath := getFileOpenInfo(kFileTypeTdo, domain.defaultTdoLibraryFileName,
      'Choose a 3D object library (tdo) file');
  if fileNameWithPath = '' then exit;
  domain.defaultTdoLibraryFileName := fileNameWithPath;
  self.readTdosFromFile;
  end;

function TPickTdoForm.readTdosFromFile: boolean;
  var
    newTdo: KfObject3D;
    inputFile: TextFile;
  begin
  // returns false if file could not be found and user canceled finding another
  result := true;
  tdos.clear;
  if domain = nil then exit;
  if not domain.checkForExistingDefaultTdoLibrary then
    begin
    result := false;
    exit;
    end;
  assignFile(inputFile, domain.defaultTdoLibraryFileName);
  try
    setDecimalSeparator; // v1.5
    reset(inputFile);
    while not eof(inputFile) do
      begin
      newTdo := KfObject3D.create;
      newTdo.readFromFileStream(inputFile, kInTdoLibrary);
      tdos.items.addObject(newTdo.name, newTdo);
      end;
  finally
    closeFile(inputFile);
    grid.rowCount := tdos.items.count div grid.colCount + 1;
    libraryGroupBox.caption := 'The current library has ' + intToStr(tdos.items.count) + ' object(s)';
  end;
  end;

procedure TPickTdoForm.saveTdosToLibrary;
  var
    fileInfo: SaveFileNamesStructure;
    suggestedName: string;
    outputFile: TextFile;
    i: smallint;
    tdo: KfObject3D;
  begin
  suggestedName := domain.defaultTdoLibraryFileName;
  if not getFileSaveInfo(kFileTypeTdo, kDontAskForFileName, suggestedName, fileInfo) then exit;
  assignFile(outputFile, fileInfo.tempFile);
  try
    setDecimalSeparator; // v1.5
    rewrite(outputFile);
    startFileSave(fileInfo);
    if tdos.items.count > 0 then for i := 0 to tdos.items.count - 1 do
      begin
      tdo := TObject(tdos.items.objects[i]) as KfObject3D;
      if tdo = nil then continue;
      tdo.writeToFileStream(outputFile, kInTdoLibrary);
      end;
    fileInfo.writingWasSuccessful := true;
  finally
    closeFile(outputFile);
    cleanUpAfterFileSave(fileInfo);
    setLibraryChanged(false);
  end;
  end;

procedure TPickTdoForm.setLibraryChanged(fileChanged: boolean);
  begin
  libraryChanged := fileChanged;
  if libraryChanged then
    fileChangedImage.picture := MainForm.fileChangedImage.picture
  else
    fileChangedImage.picture := MainForm.fileNotChangedImage.picture;
  end;

function TPickTdoForm.tdoForIndex(index: smallint): KfObject3D;
  begin
  result := nil;
  if (index >= 0) and (index <= tdos.items.count - 1) then
    result := KfObject3D(tdos.items.objects[index]);
  end;

procedure TPickTdoForm.gridDrawCell(Sender: TObject; Col, Row: Integer; Rect: TRect; State: TGridDrawState);
  var
    tdo: KfObject3d;
    turtle: KfTurtle;
    selected: boolean;
    index: smallint;
    bitmap: TBitmap;
    bestPoint: TPoint;
  begin
  grid.canvas.brush.color := grid.color;
  grid.canvas.pen.style := psClear;
  grid.canvas.fillRect(rect);
  selected := gdSelected in state;
  tdo := nil;
  index := row * grid.colCount + col;
  tdo := self.tdoForIndex(index);
  if tdo = nil then exit;
  { draw tdo }
  turtle := KfTurtle.defaultStartUsing;
  bitmap := TBitmap.create;
  try
    bitmap.width := grid.defaultColWidth;
    bitmap.height := grid.defaultRowHeight;
  except
    bitmap.width := 1;
    bitmap.height := 1;
  end;
  if not selected then
    bitmap.canvas.brush.color := clWhite
  else
    bitmap.canvas.brush.color := clHighlight;
  bitmap.canvas.fillRect(classes.Rect(0, 0, bitmap.width, bitmap.height));
  try
    turtle.drawingSurface.pane := bitmap.canvas;//grid.canvas;
    turtle.setDrawOptionsForDrawingTdoOnly;
    turtle.reset; { must be after pane and draw options set }
    // v1.6b1 added method for centering tdo
    bestPoint := tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(bitmap.width, bitmap.height), 0.3);
    turtle.xyz(bestPoint.x, bestPoint.y, 0);
    turtle.drawingSurface.recordingStart;
    tdo.draw(turtle, 0.3, '', '', 0, 0);//0.15);
    turtle.drawingSurface.recordingStop;
    turtle.drawingSurface.recordingDraw;
    turtle.drawingSurface.clearTriangles;
    grid.canvas.draw(rect.left, rect.top, bitmap);
    grid.canvas.brush.style := bsClear;
    grid.canvas.pen.color := clSilver;
    grid.canvas.pen.style := psSolid;
    with rect do grid.canvas.rectangle(left, top, right, bottom);
  finally
    KfTurtle.defaultStopUsing;
    bitmap.free;
  end;
  end;

procedure TPickTdoForm.gridSelectCell(Sender: TObject; Col, Row: Integer; var CanSelect: Boolean);
  begin
  if internalChange then exit;
  tdoSelectionChanged := true;
  chooseTdoFromList(row * grid.colCount + col);
  end;

procedure TPickTdoForm.tdosChange(Sender: TObject);
  begin
  internalChange := true;
  tdoSelectionChanged := true;
  grid.row := tdos.itemIndex div grid.colCount;
  grid.col := tdos.itemIndex mod grid.colCount;
  internalChange := false;
  end;

function TPickTdoForm.hintForTdosDrawGridAtPoint(aComponent: TComponent; aPoint: TPoint; var cursorRect: TRect): string;
  var
    col, row, index: integer;
    tdo: KfObject3D;
  begin
  result := '';
  grid.mouseToCell(aPoint.x, aPoint.y, col, row);
  index := row * grid.colCount + col;
  tdo := self.tdoForIndex(index);
  if tdo = nil then exit;
  result := tdo.getName;
  { change hint if cursor moves out of the current item's rectangle }
  cursorRect := grid.cellRect(col, row);
  end;

procedure TPickTdoForm.sectionTdosChangeLibraryClick(Sender: TObject);
  begin
  self.loadNewTdoLibrary;
  grid.invalidate;
  libraryFileName.text := domain.defaultTdoLibraryFileName;
  libraryFileName.selStart := length(libraryFileName.text);
  end;

procedure TPickTdoForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Using_3D_object_parameter_panels');
  end;

procedure TPickTdoForm.FormClose(Sender: TObject; var Action: TCloseAction);
  var
    response: integer;
  begin
  if libraryChanged then
    begin
    if modalResult = mrOK then
      self.saveTdosToLibrary
    else if modalResult = mrCancel then
      begin
      response := messageDlg('Do you want to save the changes you made' + chr(13)
          + 'to the 3D object library?', mtConfirmation, [mbYes, mbNo, mbCancel], 0);
      case response of
        IDYES: begin self.saveTdosToLibrary; action := caFree; end;
        IDNO: action := caFree;
        IDCANCEL: action := caNone;
        end;
      end;
    end;
  end;

procedure TPickTdoForm.gridDblClick(Sender: TObject);
  begin
  self.applyClick(self);
  end;

procedure TPickTdoForm.editTdoClick(Sender: TObject);
  var
    tdoEditorForm: TTdoEditorForm;
    response: integer;
  begin
  if self.selectedTdo = nil then exit;
  tdoEditorForm := TTdoEditorForm.create(self);
  if tdoEditorForm = nil then
    raise Exception.create('Problem: Could not create 3D object editor window.');
  try
    tdoEditorForm.initializeWithTdo(self.selectedTdo);
    response := tdoEditorForm.showModal;
    if response = mrOK then
      begin
      self.selectedTdo.copyFrom(tdoEditorForm.tdo);
      editedTdo := true;
      grid.invalidate;
      self.setLibraryChanged(true);
      self.chooseTdoFromList(tdos.items.indexOfObject(selectedTdo));
      end;
   finally
    tdoEditorForm.free;
    tdoEditorForm := nil;
  end;
  end;

procedure TPickTdoForm.newTdoClick(Sender: TObject);
  var
    tdoEditorForm: TTdoEditorForm;
    response: integer;
    newTdo: KfObject3D;
    newName: string;
  begin
  newName := '';
  newTdo := KfObject3D.create;
  newTdo.setName('New 3D object');
  tdoEditorForm := TTdoEditorForm.create(self);
  if tdoEditorForm = nil then
    raise Exception.create('Problem: Could not create 3D object editor window.');
  try
    tdoEditorForm.initializeWithTdo(newTdo);
    response := tdoEditorForm.showModal;
    if response = mrOK then
      begin
      if newTdo.getName = 'New 3D object' then
        if inputQuery('Name 3D object', 'Enter a name for the new 3D object', newName) then
          newTdo.setName(newName)
        else
          newTdo.setName('Unnamed 3D object');
      newTdo.copyFrom(tdoEditorForm.tdo);
      editedTdo := true;
      tdos.items.addObject(newTdo.name, newTdo);
      grid.rowCount := tdos.items.count div grid.colCount + 1;
      self.selectTdoAtIndex(tdos.items.count - 1);
      libraryGroupBox.caption := 'The current library has ' + intToStr(tdos.items.count) + ' object(s)';
      self.setLibraryChanged(true);
      self.chooseTdoFromList(tdos.items.indexOfObject(selectedTdo));
      end;
   finally
    tdoEditorForm.free;
    tdoEditorForm := nil;
  end;
  end;

procedure TPickTdoForm.copyTdoClick(Sender: TObject);
  var
    newTdo: KfObject3D;
    newName: string;
  begin
  if selectedTdo = nil then exit;
  newName := 'Copy of ' + selectedTdo.getName;
  if not inputQuery('Enter name for copy', 'Type a name for the copy of ' + selectedTdo.getName, newName) then exit;
  newTdo := KfObject3D.create;
  selectedTdo.copyTo(newTdo);
  newTdo.setName(newName);
  tdos.items.addObject(newTdo.name, newTdo);
  grid.rowCount := tdos.items.count div grid.colCount + 1;
  self.selectTdoAtIndex(tdos.items.count - 1);
  libraryGroupBox.caption := 'The current library has ' + intToStr(tdos.items.count) + ' object(s)';
  self.setLibraryChanged(true);
  self.chooseTdoFromList(tdos.items.indexOfObject(selectedTdo));
  end;

procedure TPickTdoForm.deleteTdoClick(Sender: TObject);
  var
    oldIndex: integer;
    nameToShow: string;
  begin
  if selectedTdo = nil then exit;
  nameToShow := selectedTdo.getName;
  if nameToShow = '' then nameToShow := '[unnamed]';
  if MessageDlg('Really delete the 3D object named ' + nameToShow + '?'
      + chr(13) + chr(13) + '(You cannot undo this action,'
      + chr(13) + 'but you can close the window and not save your changes'
      + chr(13) +  'if you need to get this 3D object back.)',
    mtConfirmation, [mbYes, mbNo], 0) = IDNO then
    exit;
  oldIndex := tdos.items.indexOfObject(selectedTdo);
  tdos.items.delete(oldIndex);
  grid.rowCount := tdos.items.count div grid.colCount + 1;
  self.selectTdoAtIndex(oldIndex);
  libraryGroupBox.caption := 'The current library has ' + intToStr(tdos.items.count) + ' object(s)';
  self.setLibraryChanged(true);
  self.chooseTdoFromList(tdos.items.indexOfObject(selectedTdo));
  grid.invalidate;
  end;

procedure TPickTdoForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 404;
    ptMaxTrackSize.x := 404; // only resizes vertically
    ptMinTrackSize.y := 303;
    end;
  end;

procedure TPickTdoForm.FormResize(Sender: TObject);
  var
    resizeGridHeight, rowsToShow, integralGridHeight: integer;
  begin
  // only resizes vertically
  if Application.terminated then exit;
  if param = nil then exit;
  if originalTdo = nil then exit;
  with tdos do setBounds(left, 4, width, height);
  resizeGridHeight := self.clientHeight - libraryGroupBox.height - tdos.height - 4 * 4;
  rowsToShow := resizeGridHeight div grid.defaultRowHeight;
  integralGridHeight := grid.defaultRowHeight * rowsToShow + grid.gridLineWidth * (rowsToShow - 1) + 2;
  with grid do setBounds(left, tdos.top + tdos.height + 4, width, integralGridHeight);
  with libraryGroupBox do setBounds(left, self.clientHeight - libraryGroupBox.height - 4, width, height);
  end;

procedure TPickTdoForm.moverClick(Sender: TObject);
  var
    tdoMoverForm: TTdoMoverForm;
    response: integer;
  begin
  if libraryChanged then
    begin
    response := MessageDlg('Do you want to save your changes to '
        + extractFileName(domain.defaultTdoLibraryFileName)
        + chr(13) + 'before you use the 3D object mover?'
        + chr(13) + chr(13) + 'If not, they will be lost.',
        mtConfirmation, mbYesNoCancel, 0);
    case response of
      idCancel: exit;
      idYes: self.saveTdosToLibrary;
      idNo: ;
      end;
    end;
  tdoMoverForm := TTdoMoverForm.create(self);
  if tdoMoverForm = nil then
    raise Exception.create('Problem: Could not create 3D object mover window.');
  try
    tdoMoverForm.showModal;
    self.readTdosFromFile;
    self.selectTdoAtIndex(-1);
  finally
    tdoMoverForm.free;
    tdoMoverForm := nil;
  end;
  end;

end.
