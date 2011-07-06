// unit upp_lis

from conversion_common import *;
import udebug;
import uppanel;
import delphi_compatability;

// const
kItemFirstChoice = 1;
kMaxNumChoices = 20;



class PdListParameterPanel extends PdParameterPanel {
    public boolean hasRadioButtons;
    public int currentChoice;
    public TStringList choiceStrings;
    public  choiceRects;
    public  choiceChecks;
    public boolean editEnabled;
    
    public void initialize() {
        this.currentChoice = 0;
        this.editEnabled = false;
        this.choiceStrings = delphi_compatability.TStringList.create;
        UNRESOLVED.PdPlant.fillEnumStringList(this.choiceStrings, this.param.fieldNumber, this.hasRadioButtons);
    }
    
    public void destroy() {
        this.choiceStrings.free;
        this.choiceStrings = null;
        super.destroy();
    }
    
    public void updateEnabling() {
        super.updateEnabling();
        this.editEnabled = !((this.plant == null) || (this.readOnly));
    }
    
    public void updatePlantValues() {
        int oldChoice = 0;
        
        if (this.plant == null) {
            return;
        }
        if (this.param.collapsed) {
            return;
        }
        oldChoice = this.currentChoice;
        this.updateCurrentValue(-1);
        if (!this.hasRadioButtons || (oldChoice != this.currentChoice)) {
            this.updateDisplay();
            this.Invalidate();
        }
    }
    
    public void updateCurrentValue(int aFieldIndex) {
        short i = 0;
        
        if ((this.plant == null) || (this.param.fieldType != UNRESOLVED.kFieldEnumeratedList)) {
            this.currentChoice = 0;
            this.clearChecks();
            this.editEnabled = false;
        } else {
            if (this.hasRadioButtons) {
                this.plant.transferField(UNRESOLVED.kGetField, this.currentChoice, this.param.fieldNumber, UNRESOLVED.kFieldSmallint, UNRESOLVED.kNotArray, false, null);
            } else if (this.choiceStrings.Count > 0) {
                for (i = 0; i <= this.choiceStrings.Count - 1; i++) {
                    this.plant.transferField(UNRESOLVED.kGetField, this.choiceChecks[i], this.param.fieldNumber, UNRESOLVED.kFieldBoolean, i, false, null);
                }
            }
        }
    }
    
    public void updateDisplay() {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldEnumeratedList)) {
            this.Invalidate();
        } else {
            this.editEnabled = false;
        }
    }
    
    public void clearChecks() {
        short i = 0;
        
        for (i = 0; i <= kMaxNumChoices; i++) {
            this.choiceChecks[i] = false;
        }
    }
    
    public void doMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        int i = 0;
        TPoint thePoint = new TPoint();
        
        // must always call this first because it sets the focus 
        super.doMouseUp(Sender, Button, Shift, X, Y);
        if ((this.editEnabled)) {
            thePoint = Point(X, Y);
            if (this.choiceStrings.Count > 0) {
                for (i = 0; i <= this.choiceStrings.Count - 1; i++) {
                    if (delphi_compatability.PtInRect(this.choiceRects[i], thePoint)) {
                        this.setNewValue(i);
                        this.selectedItemIndex = kItemFirstChoice + this.currentChoice;
                        break;
                    }
                }
            }
            this.Invalidate();
        }
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        super.doKeyDown(sender, key, shift);
        if ((this.editEnabled) && (key == delphi_compatability.VK_RETURN) && (this.selectedItemIndex >= kItemFirstChoice)) {
            this.setNewValue(this.selectedItemIndex - kItemFirstChoice);
            this.Invalidate();
        }
        return key;
    }
    
    public void setNewValue(int index) {
        if (this.hasRadioButtons) {
            this.currentChoice = index;
            UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeSmallintValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentChoice, this.param.fieldNumber, UNRESOLVED.kNotArray, this.param.regrow));
        } else {
            this.choiceChecks[index] = !this.choiceChecks[index];
            UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeBooleanValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.choiceChecks[index], this.param.fieldNumber, index, this.param.regrow));
        }
    }
    
    public String firstCheckedString() {
        result = "";
        short i = 0;
        
        result = "";
        if (this.choiceStrings.Count > 0) {
            for (i = 0; i <= this.choiceStrings.Count - 1; i++) {
                if (this.hasRadioButtons) {
                    if (this.currentChoice == i) {
                        result = this.choiceStrings.Strings[i];
                        return result;
                    }
                } else {
                    if (this.choiceChecks[i]) {
                        result = this.choiceStrings.Strings[i];
                        return result;
                    }
                }
            }
        }
        return result;
    }
    
    public int maxWidth() {
        result = 0;
        int i = 0;
        int maxWidth = 0;
        
        result = 0;
        //FIX unresolved WITH expression: UNRESOLVED.TMainForm(self.Owner).canvas
        for (i = 0; i <= this.choiceStrings.Count - 1; i++) {
            result = UNRESOLVED.intMax(maxWidth, UNRESOLVED.textWidth(this.choiceStrings.Strings[i]));
        }
        result = UNRESOLVED.intMax(uppanel.kLeftRightGap * 2 + this.labelWidth, +uppanel.kRadioButtonLeftGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap + maxWidth + uppanel.kLeftRightGap);
        return result;
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        int i = 0;
        int longestWidth = 0;
        int minAllowed = 0;
        
        longestWidth = 0;
        //FIX unresolved WITH expression: UNRESOLVED.TMainForm(self.Owner).canvas
        for (i = 0; i <= this.choiceStrings.Count - 1; i++) {
            longestWidth = UNRESOLVED.intMax(longestWidth, UNRESOLVED.textWidth(this.choiceStrings.Strings[i]));
        }
        minAllowed = UNRESOLVED.intMax(uppanel.kLeftRightGap * 2 + this.longestLabelWordWidth, +uppanel.kRadioButtonLeftGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap + longestWidth + uppanel.kLeftRightGap);
        if (requestedWidth > minAllowed) {
            result = -1;
        } else {
            result = minAllowed;
        }
        return result;
    }
    
    public int uncollapsedHeight() {
        result = 0;
        result = this.collapsedHeight() + this.textHeight * this.choiceStrings.Count + uppanel.kTopBottomGap;
        return result;
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        if ((!this.param.collapsed) && (this.editEnabled)) {
            result = kItemFirstChoice + this.choiceStrings.Count - 1;
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
        int i = 0;
        TRect rect = new TRect();
         circleRects = [0] * (range(0, kMaxNumChoices + 1) + 1);
         textRects = [0] * (range(0, kMaxNumChoices + 1) + 1);
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        super.paint();
        if ((this.param.collapsed)) {
            this.drawExtraValueCaptionWithString(this.firstCheckedString(), "");
            return;
        }
        Rect = this.GetClientRect();
        if (this.choiceStrings.Count > 0) {
            for (i = 0; i <= this.choiceStrings.Count - 1; i++) {
                circleRects[i].Left = Rect.left + uppanel.kRadioButtonLeftGap;
                circleRects[i].Right = circleRects[i].Left + uppanel.kRadioButtonWidth;
                circleRects[i].Top = Rect.top + this.collapsedHeight() + this.textHeight * i + (this.textHeight / 2 - uppanel.kRadioButtonWidth / 2);
                circleRects[i].Bottom = circleRects[i].Top + uppanel.kRadioButtonWidth;
                textRects[i].Left = Rect.left + uppanel.kRadioButtonLeftGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap;
                textRects[i].Right = textRects[i].Left + this.Canvas.TextWidth(this.choiceStrings.Strings[i]);
                textRects[i].Top = Rect.top + this.collapsedHeight() + this.textHeight * i;
                textRects[i].Bottom = textRects[i].Top + this.textHeight;
                if (this.hasRadioButtons) {
                    this.drawRadioButton((this.currentChoice == i), this.editEnabled, circleRects[i]);
                } else {
                    this.drawCheckBox(this.choiceChecks[i], this.editEnabled, circleRects[i]);
                }
                this.drawText(this.choiceStrings.Strings[i], textRects[i], true, (this.selectedItemIndex == kItemFirstChoice + i) && (this.editEnabled), false);
                delphi_compatability.UnionRect(this.choiceRects[i], circleRects[i], textRects[i]);
            }
        }
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
        if (enabled) {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnText;
        } else {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
        }
        //FIX unresolved WITH expression: Rect
        this.Canvas.Ellipse(this.Left, this.Top, UNRESOLVED.right, UNRESOLVED.bottom);
        this.Canvas.Brush.Color = brushColor;
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
    }
    
    public void drawCheckBox(boolean value, boolean enabled, TRect rect) {
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        if (enabled) {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnText;
        } else {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
        }
        //FIX unresolved WITH expression: Rect
        this.Canvas.Rectangle(this.Left, this.Top, UNRESOLVED.right, UNRESOLVED.bottom);
        if (value) {
            //FIX unresolved WITH expression: Rect
            this.Canvas.MoveTo(this.Left, this.Top);
            this.Canvas.LineTo(UNRESOLVED.right, UNRESOLVED.bottom);
            this.Canvas.MoveTo(this.Left, UNRESOLVED.bottom);
            this.Canvas.LineTo(UNRESOLVED.right, this.Top);
        }
    }
    
}
