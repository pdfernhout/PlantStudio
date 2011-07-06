unit Udxfclr;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, StdCtrls, Grids,
  updform;

type
  TChooseDXFColorForm = class(PdForm)
    colorsDrawGrid: TDrawGrid;
    Close: TButton;
    cancel: TButton;
    procedure colorsDrawGridSelectCell(Sender: TObject; Col, Row: Longint;
      var CanSelect: Boolean);
    procedure CloseClick(Sender: TObject);
    procedure cancelClick(Sender: TObject);
    procedure colorsDrawGridDrawCell(Sender: TObject; Col, Row: Longint;
      Rect: TRect; State: TGridDrawState);
    procedure FormActivate(Sender: TObject);
    procedure colorsDrawGridDblClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    color: TColorRef;
    colorIndex: smallint;
  end;

implementation

{$R *.DFM}

uses uturtle, u3dexport;

const kBetweenGap = 4;

procedure TChooseDXFColorForm.FormActivate(Sender: TObject);
  var
    sRect: TGridRect;
  begin
  { change to do rows also when there are more numbers }
  colorsDrawGrid.colCount := kLastDxfColorIndex + 1;
  with colorsDrawGrid do setBounds(kBetweenGap, kBetweenGap, width, height);
  colorsDrawGrid.clientWidth := colorsDrawGrid.cellRect(colorsDrawGrid.colCount - 1, 0).right;
  self.clientWidth := colorsDrawGrid.width + close.width + kBetweenGap * 3;
  close.left := self.clientWidth - close.width - kBetweenGap;
  cancel.left := close.left;
  sRect.left := self.colorIndex;
  sRect.right := self.colorIndex;
  sRect.top := 0;
  sRect.bottom := 0;
  colorsDrawGrid.selection := sRect;
  end;

procedure TChooseDXFColorForm.CloseClick(Sender: TObject);
  begin
  modalResult := mrOk;
  end;

procedure TChooseDXFColorForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TChooseDXFColorForm.colorsDrawGridDblClick(Sender: TObject);
  begin
  self.closeClick(self);
  end;

procedure TChooseDXFColorForm.colorsDrawGridSelectCell(Sender: TObject;
  Col, Row: Longint; var CanSelect: Boolean);
  begin
  color := dxfColors[col];
  colorIndex := col;
  end;

procedure TChooseDXFColorForm.colorsDrawGridDrawCell(Sender: TObject; Col,
    Row: Longint; Rect: TRect; State: TGridDrawState);
  begin
  colorsDrawGrid.canvas.brush.color := dxfColors[col];
  colorsDrawGrid.canvas.fillRect(rect);
  if (gdSelected in state) then
    begin
    colorsDrawGrid.canvas.brush.style := bsClear;
    colorsDrawGrid.canvas.pen.color := clBlack;
    with rect do colorsDrawGrid.canvas.rectangle(left, top, right, bottom);
    end;
  end;

end.
