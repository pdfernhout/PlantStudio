// unit Udxfclr

from conversion_common import *;
import updform;
import delphi_compatability;

// const
kBetweenGap = 4;



class TChooseDXFColorForm extends PdForm {
    public TDrawGrid colorsDrawGrid;
    public TButton Close;
    public TButton cancel;
    public TColorRef color;
    public short colorIndex;
    
    //$R *.DFM
    public void FormActivate(TObject Sender) {
        TGridRect sRect = new TGridRect();
        
        // change to do rows also when there are more numbers 
        this.colorsDrawGrid.ColCount = UNRESOLVED.kLastDxfColorIndex + 1;
        this.colorsDrawGrid.SetBounds(kBetweenGap, kBetweenGap, this.colorsDrawGrid.Width, this.colorsDrawGrid.Height);
        this.colorsDrawGrid.ClientWidth = this.colorsDrawGrid.CellRect(this.colorsDrawGrid.ColCount - 1, 0).Right;
        this.ClientWidth = this.colorsDrawGrid.Width + this.Close.Width + kBetweenGap * 3;
        this.Close.Left = this.ClientWidth - this.Close.Width - kBetweenGap;
        this.cancel.Left = this.Close.Left;
        sRect.left = this.colorIndex;
        sRect.right = this.colorIndex;
        sRect.top = 0;
        sRect.bottom = 0;
        this.colorsDrawGrid.Selection = sRect;
    }
    
    public void CloseClick(TObject Sender) {
        this.ModalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    public void colorsDrawGridDblClick(TObject Sender) {
        this.CloseClick(this);
    }
    
    public void colorsDrawGridSelectCell(TObject Sender, long Col, long Row, boolean CanSelect) {
        this.color = UNRESOLVED.dxfColors[Col];
        this.colorIndex = Col;
        return CanSelect;
    }
    
    public void colorsDrawGridDrawCell(TObject Sender, long Col, long Row, TRect Rect, TGridDrawState State) {
        this.colorsDrawGrid.Canvas.Brush.Color = UNRESOLVED.dxfColors[Col];
        this.colorsDrawGrid.Canvas.FillRect(Rect);
        if ((UNRESOLVED.gdSelected in State)) {
            this.colorsDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
            this.colorsDrawGrid.Canvas.Pen.Color = delphi_compatability.clBlack;
            //FIX unresolved WITH expression: Rect
            this.colorsDrawGrid.Canvas.Rectangle(this.Left, this.Top, UNRESOLVED.right, UNRESOLVED.bottom);
        }
    }
    
}
