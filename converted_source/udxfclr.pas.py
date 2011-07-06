# unit Udxfclr

from conversion_common import *
import u3dexport
import uturtle
import updform
import delphi_compatability

# const
kBetweenGap = 4

class TChooseDXFColorForm(PdForm):
    def __init__(self):
        self.colorsDrawGrid = TDrawGrid()
        self.Close = TButton()
        self.cancel = TButton()
        self.color = TColorRef()
        self.colorIndex = 0
    
    #$R *.DFM
    def FormActivate(self, Sender):
        sRect = TGridRect()
        
        # change to do rows also when there are more numbers 
        self.colorsDrawGrid.ColCount = u3dexport.kLastDxfColorIndex + 1
        self.colorsDrawGrid.SetBounds(kBetweenGap, kBetweenGap, self.colorsDrawGrid.Width, self.colorsDrawGrid.Height)
        self.colorsDrawGrid.ClientWidth = self.colorsDrawGrid.CellRect(self.colorsDrawGrid.ColCount - 1, 0).Right
        self.ClientWidth = self.colorsDrawGrid.Width + self.Close.Width + kBetweenGap * 3
        self.Close.Left = self.ClientWidth - self.Close.Width - kBetweenGap
        self.cancel.Left = self.Close.Left
        sRect.left = self.colorIndex
        sRect.right = self.colorIndex
        sRect.top = 0
        sRect.bottom = 0
        self.colorsDrawGrid.Selection = sRect
    
    def CloseClick(self, Sender):
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def colorsDrawGridDblClick(self, Sender):
        self.CloseClick(self)
    
    def colorsDrawGridSelectCell(self, Sender, Col, Row, CanSelect):
        self.color = u3dexport.dxfColors[Col]
        self.colorIndex = Col
        return CanSelect
    
    def colorsDrawGridDrawCell(self, Sender, Col, Row, Rect, State):
        self.colorsDrawGrid.Canvas.Brush.Color = u3dexport.dxfColors[Col]
        self.colorsDrawGrid.Canvas.FillRect(Rect)
        if (UNRESOLVED.gdSelected in State):
            self.colorsDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
            self.colorsDrawGrid.Canvas.Pen.Color = delphi_compatability.clBlack
            # FIX unresolved WITH expression: Rect
            self.colorsDrawGrid.Canvas.Rectangle(self.Left, self.Top, UNRESOLVED.right, UNRESOLVED.bottom)
    
