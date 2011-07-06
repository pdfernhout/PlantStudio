// unit upp_tdo

from conversion_common import *;
import ubmpsupport;
import upicktdo;
import utdoedit;
import udebug;
import uppanel;
import delphi_compatability;

// const
kItemFileName = 1;
kItemTdo = 2;
kItemTurnLeft = 3;
kItemTurnRight = 4;
kItemEnlarge = 5;
kItemReduce = 6;
kTdoSize = 64;



//<
//>
//+
//-
class PdTdoParameterPanel extends PdParameterPanel {
    public KfObject3D tdo;
    public TRect fileNameRect;
    public TRect tdoRect;
    public TRect turnLeftRect;
    public TRect turnRightRect;
    public TRect enlargeRect;
    public TRect reduceRect;
    public int rotateAngle;
    public float scale;
    public TPoint position;
    public boolean editEnabled;
    public boolean movingTdo;
    public TPoint moveStart;
    public TPoint moveStartPosition;
    
    public void create(TComponent anOwner) {
        super.create(anOwner);
        this.tdo = UNRESOLVED.KfObject3d.create;
    }
    
    public void destroy() {
        this.tdo.free;
        this.tdo = null;
    }
    
    public void initialize() {
        this.rotateAngle = 0;
        this.scale = 0.2;
        this.position = Point(0, 0);
        this.movingTdo = false;
    }
    
    public void updateEnabling() {
        super.updateEnabling();
        if ((this.plant == null) || (this.readOnly)) {
            this.editEnabled = false;
        } else {
            this.editEnabled = true;
        }
    }
    
    public void updatePlantValues() {
        pass
        // this won't ever be changed by the simulation, so don't respond 
    }
    
    public void updateCurrentValue(int aFieldIndex) {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldThreeDObject)) {
            this.plant.transferField(UNRESOLVED.kGetField, this.tdo, this.param.fieldNumber, UNRESOLVED.kFieldThreeDObject, UNRESOLVED.kNotArray, false, null);
            this.recenterTdo();
        } else {
            this.editEnabled = false;
        }
    }
    
    public void updateDisplay() {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldThreeDObject)) {
            this.Invalidate();
        } else {
            this.editEnabled = false;
        }
    }
    
    public void doMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint thePoint = new TPoint();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        // must always call this first because it sets the focus 
        super.doMouseDown(Sender, Button, Shift, X, Y);
        if ((this.editEnabled)) {
            thePoint = Point(X, Y);
            if (delphi_compatability.PtInRect(this.tdoRect, thePoint) && (delphi_compatability.TShiftStateEnum.ssCtrl in Shift)) {
                //(button = mbRight) then
                this.movingTdo = true;
                this.moveStart = thePoint;
                this.moveStartPosition = this.position;
            }
        }
    }
    
    public void doMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        if (this.movingTdo) {
            this.position.X = this.moveStartPosition.X + (X - this.moveStart.X);
            this.position.Y = this.moveStartPosition.Y + (Y - this.moveStart.Y);
            this.Invalidate();
        }
    }
    
    public void doMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint thePoint = new TPoint();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        super.doMouseUp(Sender, Button, Shift, X, Y);
        if ((this.editEnabled)) {
            thePoint = Point(X, Y);
            if (delphi_compatability.PtInRect(this.fileNameRect, thePoint)) {
                this.selectedItemIndex = kItemFileName;
                this.pickTdo();
            } else if (delphi_compatability.PtInRect(this.tdoRect, thePoint)) {
                this.selectedItemIndex = kItemTdo;
                if (this.movingTdo) {
                    this.movingTdo = false;
                    this.position.X = this.moveStartPosition.X + (X - this.moveStart.X);
                    this.position.Y = this.moveStartPosition.Y + (Y - this.moveStart.Y);
                    this.moveStart = Point(0, 0);
                    this.Invalidate();
                } else if (Button == delphi_compatability.TMouseButton.mbLeft) {
                    this.pickTdo();
                }
            } else if (delphi_compatability.PtInRect(this.turnLeftRect, thePoint)) {
                this.selectedItemIndex = kItemTurnLeft;
                this.rotateAngle = this.rotateAngle + 10;
            } else if (delphi_compatability.PtInRect(this.turnRightRect, thePoint)) {
                this.selectedItemIndex = kItemTurnRight;
                this.rotateAngle = this.rotateAngle - 10;
            } else if (delphi_compatability.PtInRect(this.enlargeRect, thePoint)) {
                this.selectedItemIndex = kItemEnlarge;
                this.scale = this.scale + 0.1;
                this.recenterTdo();
            } else if (delphi_compatability.PtInRect(this.reduceRect, thePoint)) {
                this.selectedItemIndex = kItemReduce;
                this.scale = this.scale - 0.1;
                this.recenterTdo();
            }
            this.Invalidate();
        }
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        if (delphi_compatability.Application.terminated) {
            return key;
        }
        super.doKeyDown(sender, key, shift);
        if ((key == delphi_compatability.VK_RETURN) && (this.editEnabled)) {
            switch (this.selectedItemIndex) {
                case kItemFileName:
                    this.pickTdo();
                    break;
                case kItemTdo:
                    this.pickTdo();
                    break;
        }
        return key;
    }
    
    public void pickTdo() {
        TPickTdoForm tdoPicker = new TPickTdoForm();
        String plantName = "";
        
        if ((this.tdo == null) || (this.plant == null) || (this.param == null)) {
            return;
        }
        tdoPicker = upicktdo.TPickTdoForm().create(this);
        if (tdoPicker == null) {
            throw new GeneralException.create("Problem: Could not create 3D object chooser window.");
        }
        try {
            plantName = this.plant.getName;
            if (tdoPicker.initializeWithTdoParameterAndPlantName(this.tdo, this.param, plantName)) {
                // if false, user canceled picking a 3D object library
                tdoPicker.ShowModal();
            }
        } finally {
            tdoPicker.free;
            tdoPicker = null;
        }
    }
    
    public int maxWidth() {
        result = 0;
        result = UNRESOLVED.intMax(uppanel.kLeftRightGap * 2 + this.labelWidth, uppanel.kLeftRightGap + this.formTextWidth("wwwwwwww.www") + uppanel.kLeftRightGap + kTdoSize + uppanel.kLeftRightGap);
        return result;
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        int minAllowed = 0;
        
        minAllowed = uppanel.kLeftRightGap * 2 + UNRESOLVED.intMax(this.longestLabelWordWidth, this.formTextWidth("wwwwwwww.www") + utdoedit.kBetweenGap + kTdoSize);
        if (requestedWidth > minAllowed) {
            result = -1;
        } else {
            result = minAllowed;
        }
        return result;
    }
    
    public int uncollapsedHeight() {
        result = 0;
        result = this.collapsedHeight() + kTdoSize + utdoedit.kBetweenGap + this.textHeight + uppanel.kTopBottomGap * 3;
        return result;
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        if ((!this.param.collapsed) && (this.editEnabled)) {
            result = kItemReduce;
        } else {
            result = uppanel.kItemLabel;
        }
        return result;
    }
    
    public void resizeElements() {
        pass
        // do nothing 
    }
    
    public void paint() {
        TRect rect = new TRect();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        super.paint();
        if ((this.param.collapsed)) {
            this.drawExtraValueCaptionWithString(this.tdo.getName, "");
            return;
        }
        Rect = this.GetClientRect();
        this.tdoRect.Left = Rect.left + uppanel.kLeftRightGap;
        this.tdoRect.Right = this.tdoRect.Left + kTdoSize;
        this.tdoRect.Top = this.collapsedHeight() + uppanel.kTopBottomGap;
        this.tdoRect.Bottom = this.tdoRect.Top + kTdoSize;
        this.fileNameRect.Left = this.tdoRect.Right + uppanel.kLeftRightGap;
        this.fileNameRect.Right = this.fileNameRect.Left + this.Canvas.TextWidth(this.tdo.getName);
        this.fileNameRect.Top = this.tdoRect.Top + kTdoSize / 2 - this.textHeight / 2;
        this.fileNameRect.Bottom = this.fileNameRect.Top + this.textHeight;
        this.turnLeftRect.Left = this.tdoRect.Left + (this.tdoRect.Right - this.tdoRect.Left) / 2 - (this.Canvas.TextWidth(">") * 4 + uppanel.kLeftRightGap * 3) / 2;
        this.turnLeftRect.Right = this.turnLeftRect.Left + this.Canvas.TextWidth("<");
        this.turnLeftRect.Top = this.tdoRect.Bottom + utdoedit.kBetweenGap;
        this.turnLeftRect.Bottom = this.turnLeftRect.Top + this.textHeight;
        this.turnRightRect.Left = this.turnLeftRect.Right + uppanel.kLeftRightGap;
        this.turnRightRect.Right = this.turnRightRect.Left + this.Canvas.TextWidth(">");
        this.turnRightRect.Top = this.turnLeftRect.Top;
        this.turnRightRect.Bottom = this.turnRightRect.Top + this.textHeight;
        this.enlargeRect.Left = this.turnRightRect.Right + uppanel.kLeftRightGap;
        this.enlargeRect.Right = this.enlargeRect.Left + this.Canvas.TextWidth("+");
        this.enlargeRect.Top = this.turnLeftRect.Top;
        this.enlargeRect.Bottom = this.enlargeRect.Top + this.textHeight;
        this.reduceRect.Left = this.enlargeRect.Right + uppanel.kLeftRightGap;
        this.reduceRect.Right = this.reduceRect.Left + this.Canvas.TextWidth("-");
        this.reduceRect.Top = this.turnLeftRect.Top;
        this.reduceRect.Bottom = this.reduceRect.Top + this.textHeight;
        if (this.plant != null) {
            this.drawText(this.tdo.getName, this.fileNameRect, true, (this.selectedItemIndex == kItemFileName) && (this.editEnabled), false);
        }
        this.drawText("<", this.turnLeftRect, true, this.selectedItemIndex == kItemTurnLeft, false);
        this.drawText(">", this.turnRightRect, true, this.selectedItemIndex == kItemTurnRight, false);
        this.drawText("+", this.enlargeRect, true, this.selectedItemIndex == kItemEnlarge, false);
        this.drawText("-", this.reduceRect, true, this.selectedItemIndex == kItemReduce, false);
        this.drawTdo();
        if ((this.selectedItemIndex != kItemTdo)) {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
            this.Canvas.Pen.Width = 1;
        } else {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnText;
            this.Canvas.Pen.Width = 3;
        }
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        this.Canvas.Pen.Width = 1;
        this.Canvas.Rectangle(this.tdoRect.Left - 1, this.tdoRect.Top - 1, this.tdoRect.Right + 1, this.tdoRect.Bottom + 1);
    }
    
    public void recenterTdo() {
        KfTurtle turtle = new KfTurtle();
        
        if (this.plant == null) {
            return;
        }
        if (this.tdo == null) {
            return;
        }
        turtle = UNRESOLVED.KfTurtle.defaultStartUsing;
        try {
            turtle.drawingSurface.pane = null;
            // must be after pane and draw options set 
            turtle.reset;
            this.position = this.tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(kTdoSize, kTdoSize), this.scale);
        } finally {
            UNRESOLVED.KfTurtle.defaultStopUsing;
            turtle = null;
        }
    }
    
    public void drawTdo() {
        KfTurtle turtle = new KfTurtle();
        TBitmap bitmap = new TBitmap();
        
        if (this.plant == null) {
            return;
        }
        if (this.tdo == null) {
            return;
        }
        // set up clipping bitmap 
        bitmap = delphi_compatability.TBitmap().Create();
        bitmap.Width = kTdoSize;
        bitmap.Height = kTdoSize;
        bitmap.Canvas.Brush.Color = delphi_compatability.clWhite;
        bitmap.Canvas.Rectangle(0, 0, bitmap.Width, bitmap.Height);
        // set up turtle 
        turtle = UNRESOLVED.KfTurtle.defaultStartUsing;
        try {
            turtle.drawingSurface.pane = bitmap.Canvas;
            turtle.setDrawOptionsForDrawingTdoOnly;
            // must be after pane and draw options set 
            turtle.reset;
            turtle.xyz(this.position.X, this.position.Y, 0);
            try {
                turtle.push;
                turtle.rotateY(this.rotateAngle);
                turtle.drawingSurface.recordingStart;
                this.tdo.draw(turtle, this.scale, "", "", 0, 0);
                turtle.drawingSurface.recordingStop;
                turtle.drawingSurface.recordingDraw;
                turtle.drawingSurface.clearTriangles;
                turtle.pop;
            } catch (Exception e) {
                UNRESOLVED.messageForExceptionType(e, "PdTdoParameterPanel.drawTdo");
                bitmap.free;
            }
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(bitmap, this.Canvas, this.tdoRect);
        } finally {
            UNRESOLVED.KfTurtle.defaultStopUsing;
            turtle = null;
            bitmap.free;
        }
    }
    
}
