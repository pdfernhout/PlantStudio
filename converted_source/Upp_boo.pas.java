// unit upp_boo

from conversion_common import *;
import udebug;
import uppanel;
import delphi_compatability;

// const
kItemYes = 1;
kItemNo = 2;



class PdBooleanParameterPanel extends PdParameterPanel {
    public boolean currentValue;
    public TRect yesRect;
    public TRect noRect;
    public boolean editEnabled;
    
    public void initialize() {
        this.currentValue = false;
        this.editEnabled = false;
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
        if (this.plant == null) {
            return;
        }
        if (this.param.collapsed) {
            return;
        }
        this.updateCurrentValue(-1);
        this.updateDisplay();
        this.Invalidate();
    }
    
    public void updateCurrentValue(int aFieldIndex) {
        if (this.plant != null) {
            if (this.param.fieldType == UNRESOLVED.kFieldBoolean) {
                this.plant.transferField(UNRESOLVED.kGetField, this.currentValue, this.param.fieldNumber, UNRESOLVED.kFieldBoolean, UNRESOLVED.kNotArray, false, null);
                this.updateDisplay();
            }
        } else {
            this.currentValue = false;
            this.editEnabled = false;
        }
    }
    
    public void updateDisplay() {
        if (this.plant != null) {
            if (this.param.fieldType == UNRESOLVED.kFieldBoolean) {
                this.Invalidate();
            }
        } else {
            this.editEnabled = false;
        }
    }
    
    public void doMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint thePoint = new TPoint();
        boolean newValue = false;
        
        // must always call this first because it sets the focus 
        super.doMouseDown(Sender, Button, Shift, X, Y);
        if ((this.editEnabled)) {
            thePoint = Point(X, Y);
            newValue = this.currentValue;
            if (delphi_compatability.PtInRect(this.yesRect, thePoint)) {
                newValue = true;
                this.selectedItemIndex = kItemYes;
            } else if (delphi_compatability.PtInRect(this.noRect, thePoint)) {
                newValue = false;
                this.selectedItemIndex = kItemNo;
            }
            this.Invalidate();
            if ((newValue != this.currentValue)) {
                this.negateValue();
            }
        }
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        boolean newValue = false;
        
        super.doKeyDown(sender, key, shift);
        if ((key == delphi_compatability.VK_RETURN) && (this.editEnabled)) {
            newValue = this.currentValue;
            switch (this.selectedItemIndex) {
                case kItemYes:
                    newValue = true;
                    break;
                case kItemNo:
                    newValue = false;
                    break;
            if ((newValue != this.currentValue)) {
                this.negateValue();
            }
        }
        return key;
    }
    
    public void negateValue() {
        this.currentValue = !this.currentValue;
        if (this.plant != null) {
            UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeBooleanValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValue, this.param.fieldNumber, UNRESOLVED.kNotArray, this.param.regrow));
        }
        this.Invalidate();
    }
    
    public int maxWidth() {
        result = 0;
        result = UNRESOLVED.intMax(uppanel.kLeftRightGap * 2 + this.longestLabelWordWidth, uppanel.kRadioButtonLeftGap + (this.yesRect.Right - this.yesRect.Left) + uppanel.kRadioButtonBetweenGap + (this.noRect.Right - this.noRect.Left) + uppanel.kLeftRightGap);
        return result;
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        int minAllowed = 0;
        
        minAllowed = UNRESOLVED.intMax(uppanel.kLeftRightGap * 2 + this.longestLabelWordWidth, uppanel.kRadioButtonLeftGap + (this.yesRect.Right - this.yesRect.Left) + uppanel.kRadioButtonBetweenGap + (this.noRect.Right - this.noRect.Left) + uppanel.kLeftRightGap);
        if (requestedWidth > minAllowed) {
            result = -1;
        } else {
            result = minAllowed;
        }
        return result;
    }
    
    public int uncollapsedHeight() {
        result = 0;
        result = this.collapsedHeight() + this.textHeight + uppanel.kTopBottomGap;
        return result;
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        if ((!this.param.collapsed) && (this.editEnabled)) {
            result = kItemNo;
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
        TRect circleYesRect = new TRect();
        TRect circleNoRect = new TRect();
        TRect yesTextRect = new TRect();
        TRect noTextRect = new TRect();
        
        super.paint();
        if ((this.param.collapsed)) {
            if (this.currentValue) {
                this.drawExtraValueCaptionWithString("yes", "");
            } else {
                this.drawExtraValueCaptionWithString("no", "");
            }
            return;
        }
        Rect = this.GetClientRect();
        this.Canvas.Font = this.Font;
        circleYesRect.Left = Rect.left + uppanel.kRadioButtonLeftGap;
        circleYesRect.Right = circleYesRect.Left + uppanel.kRadioButtonWidth;
        circleYesRect.Top = Rect.top + this.collapsedHeight() + (this.textHeight / 2 - uppanel.kRadioButtonWidth / 2);
        circleYesRect.Bottom = circleYesRect.Top + uppanel.kRadioButtonWidth;
        yesTextRect.Left = Rect.left + uppanel.kRadioButtonLeftGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap;
        yesTextRect.Right = yesTextRect.Left + this.Canvas.TextWidth("yes");
        yesTextRect.Top = Rect.top + this.collapsedHeight();
        yesTextRect.Bottom = yesTextRect.Top + this.textHeight;
        circleNoRect = circleYesRect;
        circleNoRect.Left = yesTextRect.Right + uppanel.kRadioButtonBetweenGap;
        circleNoRect.Right = circleNoRect.Left + uppanel.kRadioButtonWidth;
        noTextRect = yesTextRect;
        noTextRect.Left = yesTextRect.Right + uppanel.kRadioButtonBetweenGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap;
        noTextRect.Right = noTextRect.Left + this.Canvas.TextWidth("no");
        this.drawRadioButton(this.currentValue, this.editEnabled, circleYesRect);
        this.drawText("yes", yesTextRect, true, (this.selectedItemIndex == kItemYes) && (this.editEnabled), false);
        this.drawRadioButton(!this.currentValue, this.editEnabled, circleNoRect);
        this.drawText("no", noTextRect, true, (this.selectedItemIndex == kItemNo) && (this.editEnabled), false);
        delphi_compatability.UnionRect(this.yesRect, circleYesRect, yesTextRect);
        delphi_compatability.UnionRect(this.noRect, circleNoRect, noTextRect);
    }
    
    public void drawRadioButton(boolean value, boolean enabled, TRect rect) {
        TColor brushColor = new TColor();
        
        brushColor = this.Canvas.Brush.Color;
        if (value) {
            if (enabled) {
                this.Canvas.Brush.Color = UNRESOLVED.clBtnText;
            } else {
                this.Canvas.Brush.Color = UNRESOLVED.clBtnShadow;
            }
        } else {
            this.Canvas.Brush.Color = UNRESOLVED.clBtnFace;
        }
        //FIX unresolved WITH expression: Rect
        this.Canvas.Ellipse(this.Left, this.Top, UNRESOLVED.right, UNRESOLVED.bottom);
        this.Canvas.Brush.Color = brushColor;
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
    }
    
}
