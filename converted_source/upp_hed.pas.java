// unit Upp_hed

from conversion_common import *;
import udebug;
import uppanel;
import delphi_compatability;


class PdHeaderParameterPanel extends PdParameterPanel {
    
    public void collapseOrExpand(int y) {
        if ((this.Owner != null)) {
            UNRESOLVED.TMainForm(this.Owner).collapseOrExpandParameterPanelsUntilNextHeader(this);
        }
        //don't need to change height
        this.param.collapsed = !this.param.collapsed;
    }
    
    public void collapse() {
        if (this.param.collapsed) {
            return;
        }
        if ((this.Owner != null)) {
            UNRESOLVED.TMainForm(this.Owner).collapseOrExpandParameterPanelsUntilNextHeader(this);
        }
        this.param.collapsed = true;
    }
    
    public void expand() {
        if (!this.param.collapsed) {
            return;
        }
        if ((this.Owner != null)) {
            UNRESOLVED.TMainForm(this.Owner).collapseOrExpandParameterPanelsUntilNextHeader(this);
        }
        this.param.collapsed = false;
    }
    
    public void initialize() {
        pass
        // nothing 
    }
    
    public void updateEnabling() {
        super.updateEnabling();
        // grey out if no plant, but nothing else 
    }
    
    public void updatePlantValues() {
        pass
        // nothing 
    }
    
    public void updateCurrentValue(int aFieldIndex) {
        pass
        // nothing 
    }
    
    public void updateDisplay() {
        pass
        // nothing 
    }
    
    public void doMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        // must always call this first because it sets the focus 
        super.doMouseDown(Sender, Button, Shift, X, Y);
        // nothing else; inherited will do collapse/expand 
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        super.doKeyDown(sender, key, shift);
        // nothing else; inherited will do collapse/expand 
        return key;
    }
    
    public int maxWidth() {
        result = 0;
        result = uppanel.kLeftRightGap * 2 + this.longestLabelWordWidth;
        return result;
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        int minAllowed = 0;
        
        minAllowed = uppanel.kLeftRightGap * 2 + this.longestLabelWordWidth;
        if (requestedWidth > minAllowed) {
            result = -1;
        } else {
            result = minAllowed;
        }
        return result;
    }
    
    public int uncollapsedHeight() {
        result = 0;
        result = this.collapsedHeight();
        return result;
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        result = uppanel.kItemLabel;
        return result;
    }
    
    public void resizeElements() {
        pass
        // do nothing 
    }
    
    public void paint() {
        TRect fullRect = new TRect();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        // copied from TCustomPanel.paint and location of caption text changed 
        // can't call inherited paint because it wants to put the caption in the middle 
        this.fillWithBevels();
        fullRect = this.GetClientRect();
        this.Canvas.Font = this.Font;
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        this.labelRect.Left = fullRect.Left + uppanel.kLeftRightGap + uppanel.kArrowPictureSize + udebug.kBetweenGap * 2;
        this.labelRect.Right = this.labelRect.Left + this.Width - uppanel.kLeftRightGap * 2;
        this.labelRect.Top = fullRect.Top + 2;
        this.labelRect.Bottom = this.labelRect.Top + this.textHeight;
        //  with labelRect do
        //      begin
        //      right := fullRect.right - kleftRightGap * 4;
        //      left := right - textWidth(caption);
        //      top := fullRect.top + 2;
        //      bottom := top + self.textHeight;
        //      end;  
        this.wrappedLabelHeight = this.drawText(this.Caption, this.labelRect, false, false, false);
        this.pictureRect.Left = fullRect.Left + uppanel.kLeftRightGap;
        this.pictureRect.Right = this.pictureRect.Left + uppanel.kArrowPictureSize;
        this.pictureRect.Top = this.labelRect.Top + 1;
        this.pictureRect.Bottom = this.pictureRect.Top + uppanel.kArrowPictureSize;
        if (this.plant != null) {
            if (this.param.collapsed) {
                this.Canvas.Draw(this.pictureRect.Left, this.pictureRect.Top, UNRESOLVED.MainForm.paramPanelClosedArrowImage.picture.bitmap);
            } else {
                this.Canvas.Draw(this.pictureRect.Left, this.pictureRect.Top, UNRESOLVED.MainForm.paramPanelOpenArrowImage.picture.bitmap);
            }
        }
        if ((this.selectedItemIndex == uppanel.kItemLabel)) {
            this.Canvas.Rectangle(this.pictureRect.Left, this.pictureRect.Top, this.pictureRect.Right, this.pictureRect.Bottom);
        }
        //
        //    if plant <> nil then
        //      begin
        //      pen.width := 1;
        //      pen.color := clBlue;
        //      moveTo({pictureRect.right + kLeftRightGap * 2}labelRect.left + textWidth(caption) + kLeftRightGap * 2,
        //        labelRect.top + rHeight(labelRect) div 2 - pen.width div 2);
        //      lineTo({labelRect.left - kLeftRightGap * 2}fullRect.right - kLeftRightGap * 2,
        //        labelRect.top + rHeight(labelRect) div 2 - pen.width div 2);
        //      end;
        //      
    }
    
    public void fillWithBevels() {
        TRect fullRect = new TRect();
        TColor TopColor = new TColor();
        TColor BottomColor = new TColor();
        
        // PDF PORT -- moved nested function inline
        //procedure AdjustColors(Bevel: TPanelBevel);
        //  begin
        //  TopColor := clBtnHighlight;
        //  if Bevel = bvLowered then TopColor := clBtnShadow;
        //  BottomColor := clBtnShadow;
        //  if Bevel = bvLowered then BottomColor := clBtnHighlight;
        //  end;
        fullRect = this.GetClientRect();
        if (this.plant != null) {
            this.Canvas.Brush.Color = delphi_compatability.clNavy;
        } else {
            this.Canvas.Brush.Color = UNRESOLVED.clBtnShadow;
        }
        this.Canvas.FillRect(fullRect);
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        if (this.BevelOuter != UNRESOLVED.bvNone) {
            //AdjustColors(BevelOuter);
            TopColor = UNRESOLVED.clBtnHighlight;
            if (this.BevelOuter == UNRESOLVED.bvLowered) {
                TopColor = UNRESOLVED.clBtnShadow;
            }
            BottomColor = UNRESOLVED.clBtnShadow;
            if (this.BevelOuter == UNRESOLVED.bvLowered) {
                BottomColor = UNRESOLVED.clBtnHighlight;
            }
            UNRESOLVED.Frame3D(this.Canvas, fullRect, TopColor, BottomColor, this.BevelWidth);
        }
        UNRESOLVED.Frame3D(this.Canvas, fullRect, this.Color, this.Color, this.BorderWidth);
        if (this.BevelInner != UNRESOLVED.bvNone) {
            UNRESOLVED.AdjustColors(this.BevelInner);
            TopColor = UNRESOLVED.clBtnHighlight;
            if (this.BevelInner == UNRESOLVED.bvLowered) {
                TopColor = UNRESOLVED.clBtnShadow;
            }
            BottomColor = UNRESOLVED.clBtnShadow;
            if (this.BevelInner == UNRESOLVED.bvLowered) {
                BottomColor = UNRESOLVED.clBtnHighlight;
            }
            UNRESOLVED.Frame3D(this.Canvas, fullRect, TopColor, BottomColor, this.BevelWidth);
        }
    }
    
}
