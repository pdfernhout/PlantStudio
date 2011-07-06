unit ucustdrw;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Spin, updform, Buttons, udomain;

type
  TCustomDrawOptionsForm = class(PdForm)
    helpButton: TSpeedButton;
    Close: TButton;
    cancel: TButton;
    GroupBox1: TGroupBox;
    sortPolygons: TCheckBox;
    sortTdosAsOneItem: TCheckBox;
    GroupBox2: TGroupBox;
    lineContrastIndexLabel: TLabel;
    fillPolygons: TCheckBox;
    drawLinesBetweenPolygons: TCheckBox;
    lineContrastIndex: TSpinEdit;
    GroupBox3: TGroupBox;
    draw3DObjects: TCheckBox;
    drawStems: TCheckBox;
    draw3DObjectsAsBoundingRectsOnly: TCheckBox;
    procedure FormActivate(Sender: TObject);
    procedure CloseClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure fillPolygonsClick(Sender: TObject);
    procedure drawLinesBetweenPolygonsClick(Sender: TObject);
    procedure sortPolygonsClick(Sender: TObject);
    procedure draw3DObjectsClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
  private
    { Private declarations }
  public
    { Public declarations }
    options: DomainOptionsStructure;
    transferDirection: smallint;
    optionsChanged: boolean;
    procedure transferFields;
    procedure transferCheckBox(checkBox: TCheckBox; var value: boolean);
    procedure transferSmallintSpinEditBox(editBox: TSpinEdit; var value: smallint);
  end;

implementation

{$R *.DFM}

uses usupport;

const
  kTransferLoad = 1;
  kTransferSave = 2;

procedure TCustomDrawOptionsForm.FormActivate(Sender: TObject);
  begin
  transferDirection := kTransferLoad;
	self.transferFields;
  // interactions
  drawLinesBetweenPolygons.enabled := fillPolygons.checked;
  lineContrastIndex.enabled := drawLinesBetweenPolygons.enabled and drawLinesBetweenPolygons.checked;
  lineContrastIndexLabel.enabled := lineContrastIndex.enabled;
  sortTdosAsOneItem.enabled := sortPolygons.checked;
  draw3DObjectsAsBoundingRectsOnly.enabled := draw3DObjects.checked;
  end;

procedure TCustomDrawOptionsForm.CloseClick(Sender: TObject);
  begin
  transferDirection := kTransferSave;
	self.transferFields;
  modalResult := mrOK;
  end;

procedure TCustomDrawOptionsForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TCustomDrawOptionsForm.transferFields;
  begin
  transferCheckBox(drawStems, options.drawStems);
  transferCheckBox(draw3DObjects, options.draw3DObjects);
  transferCheckBox(draw3DObjectsAsBoundingRectsOnly, options.draw3DObjectsAsBoundingRectsOnly);
  transferCheckBox(fillPolygons, options.fillPolygons);
  transferCheckBox(drawLinesBetweenPolygons, options.drawLinesBetweenPolygons);
  transferSmallintSpinEditBox(lineContrastIndex, options.lineContrastIndex);
  transferCheckBox(sortPolygons, options.sortPolygons);
  transferCheckBox(sortTdosAsOneItem, options.sortTdosAsOneItem);
  end;

procedure TCustomDrawOptionsForm.transferCheckBox(checkBox: TCheckBox; var value: boolean);
  begin
  if transferDirection = kTransferLoad then
    checkBox.checked := value
  else if transferDirection = kTransferSave then
    begin
    if value <> checkBox.checked then
      optionsChanged := true;
    value := checkBox.checked;
    end;
  end;

procedure TCustomDrawOptionsForm.transferSmallintSpinEditBox(editBox: TSpinEdit; var value: smallint);
  begin
  if transferDirection = kTransferLoad then
    editBox.text := intToStr(value)
  else if transferDirection = kTransferSave then
    begin
    if value <> strToIntDef(editBox.text, 0) then
      optionsChanged := true;
    value := strToIntDef(editBox.text, 0);
    end;
  end;

procedure TCustomDrawOptionsForm.draw3DObjectsClick(Sender: TObject);
  begin
  draw3DObjectsAsBoundingRectsOnly.enabled := draw3DObjects.checked;
  end;

procedure TCustomDrawOptionsForm.fillPolygonsClick(Sender: TObject);
  begin
  drawLinesBetweenPolygons.enabled := (fillPolygons.checked);// and (not drawWithOpenGL.checked);
  lineContrastIndex.enabled := drawLinesBetweenPolygons.enabled and drawLinesBetweenPolygons.checked;
  lineContrastIndexLabel.enabled := lineContrastIndex.enabled;
  end;

procedure TCustomDrawOptionsForm.drawLinesBetweenPolygonsClick(Sender: TObject);
  begin
  lineContrastIndex.enabled := drawLinesBetweenPolygons.enabled and drawLinesBetweenPolygons.checked;
  lineContrastIndexLabel.enabled := lineContrastIndex.enabled;
  end;

procedure TCustomDrawOptionsForm.sortPolygonsClick(Sender: TObject);
  begin
  sortTdosAsOneItem.enabled := sortPolygons.checked;
  end;

procedure TCustomDrawOptionsForm.helpButtonClick(Sender: TObject);
  begin
  Application.helpJump('Changing_the_drawing_speed');
  end;

procedure TCustomDrawOptionsForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

end.

(*
procedure TOptionsForm.drawWithOpenGLClick(Sender: TObject);
  begin
  //drawLinesBetweenPolygons.enabled := (fillPolygons.checked) and (not drawWithOpenGL.checked);
  //sortPolygons.enabled := not drawWithOpenGL.checked;
  end;
*)

