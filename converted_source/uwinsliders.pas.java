// unit UWinSliders

from conversion_common import *;
import delphi_compatability;

// const
kSliderHeightReadOnly = 5;
kSliderHeightNotReadOnly = 11;
kSliderDraggerHeight = 7;
kSliderDraggerWidth = 5;
kSliderGrayLineThickness = 1;
kSliderBlueLineThickness = 3;
kSliderDefaultWidth = 20;


public void KfDrawButton(TCanvas aCanvas, TRect aRect, boolean selected, boolean enabled) {
    TRect internalRect = new TRect();
    
    aCanvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
    if (enabled) {
        aCanvas.Pen.Color = delphi_compatability.clBlack;
        aCanvas.Brush.Color = delphi_compatability.clWhite;
    } else {
        aCanvas.Brush.Color = UNRESOLVED.clBtnShadow;
        aCanvas.Pen.Color = UNRESOLVED.clBtnShadow;
    }
    aCanvas.Rectangle(aRect.Left, aRect.Top, aRect.Right, aRect.Bottom);
    if (selected) {
        internalRect = aRect;
        UNRESOLVED.inflateRect(internalRect, -1, -1);
        aCanvas.Brush.Color = delphi_compatability.clAqua;
        aCanvas.FillRect(internalRect);
    }
}

// Published declarations 
// must be at least 4 more than dragger height 
// should be odd number 
// PDF PORT -- not used anyway
public void Register1() {
    UNRESOLVED.RegisterComponents("Samples", {KfWinSlider, });
}


class KfWinSlider extends TCustomControl {
    public int draggerHeight;
    public int draggerWidth;
    public int FMinValue;
    public int FMaxValue;
    public boolean FReadOnly;
    public int FCurrentValue;
    public boolean dragging;
    public int dragStart;
    public int originalValue;
    public TRect draggerRect;
    
    public void create(TComponent AnOwner) {
        super.create(AnOwner);
        this.Width = 140;
        this.Height = 35;
        this.MinValue = 0;
        this.MaxValue = 100;
        this.draggerHeight = kSliderDraggerHeight;
        this.draggerWidth = kSliderDraggerWidth;
        this.ReadOnly = false;
        this.CurrentValue = 0;
        this.dragging = false;
        this.TabStop = true;
        this.useDefaultSizeAndDraggerSize();
    }
    
    public void useDefaultSizeAndDraggerSize() {
        if (this.ReadOnly) {
            // assumes that readOnly is already set, and assumes that value of readOnly will not be changed
            //    unless this is called again afterward 
            this.Height = kSliderHeightReadOnly;
            this.Width = kSliderDefaultWidth;
            this.draggerHeight = 0;
            this.draggerWidth = 0;
        } else {
            this.Height = kSliderHeightNotReadOnly;
            this.Width = kSliderDefaultWidth;
            this.draggerHeight = kSliderDraggerHeight;
            this.draggerWidth = kSliderDraggerWidth;
        }
    }
    
    public void CMFocusChanged(TCMFocusChanged message) {
        super.CMFocusChanged();
        this.Repaint();
    }
    
    public void WMGetDlgCode(TWMGetDlgCode message) {
        message.result = delphi_compatability.DLGC_WANTARROWS;
    }
    
    //returns true if current value changed
    public boolean setValue(long newValue) {
        result = false;
        result = false;
        if (newValue > this.MaxValue) {
            newValue = this.MaxValue;
        }
        if (newValue < this.MinValue) {
            newValue = this.MinValue;
        }
        if (newValue == this.CurrentValue) {
            return result;
        }
        this.CurrentValue = newValue;
        //repaint;   
        result = true;
        return result;
    }
    
    public void keyDown(byte Key, TShiftState shift) {
        long newValue = 0;
        
        super.keyDown();
        if (!this.ReadOnly) {
            switch (Key) {
                case delphi_compatability.VK_LEFT:
                    newValue = this.CurrentValue - 1;
                    break;
                case delphi_compatability.VK_RIGHT:
                    newValue = this.CurrentValue + 1;
                    break;
                case delphi_compatability.VK_UP:
                    newValue = this.CurrentValue + 1;
                    break;
                case delphi_compatability.VK_DOWN:
                    newValue = this.CurrentValue - 1;
                    break;
                case delphi_compatability.VK_NEXT:
                    //page up
                    newValue = this.CurrentValue - 5;
                    break;
                case delphi_compatability.VK_PRIOR:
                    //page down
                    newValue = this.CurrentValue + 5;
                    break;
                default:
                    return Key;
                    break;
            this.Invalidate();
            this.Refresh();
            this.setValue(newValue);
        }
        return Key;
    }
    
    public boolean pointOnDragger(long x, long y) {
        result = false;
        result = delphi_compatability.PtInRect(this.draggerRect, Point(x, y));
        return result;
    }
    
    public void mouseDown(TMouseButton Button, TShiftState Shift, int X, int Y) {
        super.mouseDown();
        this.SetFocus();
        if (!this.ReadOnly) {
            if ((Button == delphi_compatability.TMouseButton.mbLeft)) {
                //and (pointOnDragger(x, y))
                this.dragging = true;
                this.dragStart = X;
                this.originalValue = this.CurrentValue;
            }
            this.Invalidate();
            this.Refresh();
        }
    }
    
    public void mouseMove(TShiftState Shift, int X, int Y) {
        long delta = 0;
        long newValue = 0;
        long lineLength = 0;
        
        super.mouseMove();
        if (this.dragging) {
            delta = X - this.dragStart;
            //pdf fix - won't snap to grid - will just change relative...
            lineLength = this.Width - 2 * (this.draggerWidth / 2);
            newValue = this.originalValue + intround(delta * (this.MaxValue - this.MinValue) / lineLength);
            this.Invalidate();
            this.Refresh();
            this.setValue(newValue);
        }
    }
    
    public void mouseUp(TMouseButton Button, TShiftState Shift, int X, int Y) {
        super.mouseUp();
        if (this.dragging) {
            this.dragging = false;
        }
    }
    
    public long xDistanceFromCurrentValue(long distanceInPixels) {
        result = 0;
        float proportion = 0.0;
        
        proportion = (this.CurrentValue - this.MinValue) / (this.MaxValue - this.MinValue);
        try {
            result = intround(proportion * distanceInPixels);
        } catch (Exception e) {
            result = 0;
        }
        return result;
    }
    
    public void paint() {
        TRect grayRect = new TRect();
        TRect blueRect = new TRect();
        TRect fullRect = new TRect();
        TRect lineRect = new TRect();
        long distance = 0;
        
        fullRect = this.GetClientRect();
        // start with total fill 
        this.Canvas.Brush.Color = UNRESOLVED.clBtnFace;
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        this.Canvas.FillRect(fullRect);
        // rect for line 
        lineRect = fullRect;
        lineRect.Left = lineRect.Left + this.draggerWidth / 2 + 2;
        lineRect.Right = lineRect.Right - this.draggerWidth / 2 - 1;
        lineRect.Top = lineRect.Top + (lineRect.Bottom - lineRect.Top) / 2 - kSliderBlueLineThickness / 2;
        lineRect.Bottom = lineRect.Top + kSliderBlueLineThickness;
        // rect for dragger 
        distance = this.xDistanceFromCurrentValue(lineRect.Right - lineRect.Left);
        this.draggerRect.Left = lineRect.Left + distance - this.draggerWidth / 2 - this.draggerWidth % 2;
        this.draggerRect.Right = this.draggerRect.Left + this.draggerWidth;
        this.draggerRect.Top = lineRect.Top - this.draggerHeight / 2 + kSliderBlueLineThickness / 2;
        this.draggerRect.Bottom = this.draggerRect.Top + this.draggerHeight;
        // blue rect 
        blueRect = lineRect;
        blueRect.Right = blueRect.Left + distance;
        // gray rect 
        grayRect = lineRect;
        grayRect.Top = grayRect.Top + (grayRect.Bottom - grayRect.Top) / 2;
        grayRect.Bottom = grayRect.Top + kSliderGrayLineThickness;
        if (this.Enabled) {
            grayRect.Left = blueRect.Right + 1;
        }
        //draw gray line
        this.Canvas.Brush.Color = UNRESOLVED.clBtnShadow;
        this.Canvas.FillRect(grayRect);
        if (this.Enabled) {
            //draw blue line
            this.Canvas.Brush.Color = delphi_compatability.clBlue;
            this.Canvas.FillRect(blueRect);
        }
        if (!this.ReadOnly) {
            //draw dragger if not read only 
            KfDrawButton(this.Canvas, this.draggerRect, this.Focused(), this.Enabled);
        }
        if ((this.Focused())) {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
            this.Canvas.MoveTo(fullRect.Right - 1, fullRect.Top);
            this.Canvas.LineTo(fullRect.Left, fullRect.Top);
            this.Canvas.LineTo(fullRect.Left, fullRect.Bottom - 1);
            this.Canvas.LineTo(fullRect.Right - 1, fullRect.Bottom - 1);
            this.Canvas.LineTo(fullRect.Right - 1, fullRect.Top);
        }
    }
    
}
