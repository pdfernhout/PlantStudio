// unit upp_int

from conversion_common import *;
import udebug;
import usliders;
import uppanel;
import delphi_compatability;

// const
kItemValueText = 1;
kItemSlider = 2;



//  kItemUnitText = 2;    
class PdSmallintParameterPanel extends PdParameterPanel {
    public short currentValue;
    public short currentValueWhileSliding;
    public short minValue;
    public short maxValue;
    public KfSlider slider;
    public short unitIndex;
    public TRect minTextRect;
    public TRect maxTextRect;
    public TRect valueTextRect;
    public TRect unitTextRect;
    public boolean drawWithoutBounds;
    
    public void initialize() {
        //assuming slider will be deleted automatically by owner - self - otherwise would have destructor
        this.slider = usliders.KfSlider().create(this);
        this.slider.Parent = this;
        this.slider.FOnMouseDown = this.sliderMouseDown;
        this.slider.FOnMouseMove = this.sliderMouseMove;
        this.slider.FOnMouseUp = this.sliderMouseUp;
        this.slider.FOnKeyDown = this.sliderKeyDown;
        this.slider.readOnly = this.param.readOnly;
        this.slider.useDefaultSizeAndDraggerSize();
        this.minValue = intround(this.param.lowerBound);
        this.maxValue = intround(this.param.upperBound);
        this.slider.minValue = this.minValue;
        this.slider.maxValue = this.maxValue;
    }
    
    public short checkValueAgainstBounds(short value) {
        result = 0;
        result = value;
        if (result < this.minValue) {
            result = this.minValue;
        }
        if (result > this.maxValue) {
            result = this.maxValue;
        }
        return result;
    }
    
    public void doMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint thePoint = new TPoint();
        
        // must always call this first because it sets the focus 
        super.doMouseUp(Sender, Button, Shift, X, Y);
        thePoint = Point(X, Y);
        if (delphi_compatability.PtInRect(this.valueTextRect, thePoint)) {
            if (this.slider.Enabled && !this.slider.readOnly) {
                this.selectedItemIndex = kItemValueText;
                this.Invalidate();
                this.adjustValue();
            }
        }
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        if (this.slider.Enabled) {
            switch (key) {
                case delphi_compatability.VK_HOME:
                    if ((this.selectedItemIndex == kItemSlider)) {
                        // process slider arrow keys first 
                        key = this.slider.doKeyDown(sender, key, shift);
                        return key;
                    }
                    break;
                case delphi_compatability.VK_END:
                    if ((this.selectedItemIndex == kItemSlider)) {
                        // process slider arrow keys first 
                        key = this.slider.doKeyDown(sender, key, shift);
                        return key;
                    }
                    break;
                case delphi_compatability.VK_DOWN:
                    if ((this.selectedItemIndex == kItemSlider)) {
                        // process slider arrow keys first 
                        key = this.slider.doKeyDown(sender, key, shift);
                        return key;
                    }
                    break;
                case delphi_compatability.VK_LEFT:
                    if ((this.selectedItemIndex == kItemSlider)) {
                        // process slider arrow keys first 
                        key = this.slider.doKeyDown(sender, key, shift);
                        return key;
                    }
                    break;
                case delphi_compatability.VK_UP:
                    if ((this.selectedItemIndex == kItemSlider)) {
                        // process slider arrow keys first 
                        key = this.slider.doKeyDown(sender, key, shift);
                        return key;
                    }
                    break;
                case delphi_compatability.VK_RIGHT:
                    if ((this.selectedItemIndex == kItemSlider)) {
                        // process slider arrow keys first 
                        key = this.slider.doKeyDown(sender, key, shift);
                        return key;
                    }
                    break;
                case delphi_compatability.VK_NEXT:
                    if ((this.selectedItemIndex == kItemSlider)) {
                        // process slider arrow keys first 
                        key = this.slider.doKeyDown(sender, key, shift);
                        return key;
                    }
                    break;
                case delphi_compatability.VK_PRIOR:
                    if ((this.selectedItemIndex == kItemSlider)) {
                        // process slider arrow keys first 
                        key = this.slider.doKeyDown(sender, key, shift);
                        return key;
                    }
                    break;
        }
        if ((this.selectedItemIndex == kItemValueText) && (key == delphi_compatability.VK_RETURN)) {
            key = 0;
            this.Invalidate();
            this.adjustValue();
            return key;
        }
        super.doKeyDown(sender, key, shift);
        if (this.slider.Enabled) {
            if ((key == delphi_compatability.VK_RETURN) && (this.selectedItemIndex == kItemSlider)) {
                key = this.slider.doKeyDown(sender, key, shift);
            }
        }
        return key;
    }
    
    public void adjustValue() {
        ansistring newString = new ansistring();
        short oldValue = 0;
        short newValue = 0;
        String oldString = "";
        String prompt = "";
        String nameString = "";
        String unitString = "";
        
        oldValue = this.currentValue;
        newString = IntToStr(this.currentValue);
        oldString = newString;
        nameString = UNRESOLVED.copy(this.Caption, 1, 30);
        if (len(nameString) == 30) {
            nameString = nameString + "...";
        }
        unitString = UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.unitIndex);
        prompt = "Type a new value.";
        if (InputQuery("Enter value", prompt, newString)) {
            if ((newString != oldString)) {
                newValue = StrToIntDef(newString, 0);
                if (this.checkValueAgainstBounds(newValue) == newValue) {
                    this.currentValue = newValue;
                    UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeSmallintValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValue, this.param.fieldNumber, UNRESOLVED.kNotArray, this.param.regrow));
                    this.updateDisplay();
                    this.Invalidate();
                }
            }
        }
    }
    
    public void updateEnabling() {
        super.updateEnabling();
        this.slider.Enabled = this.plant != null;
        this.slider.readOnly = this.readOnly;
    }
    
    public void updatePlantValues() {
        int oldValue = 0;
        
        if (this.plant == null) {
            return;
        }
        if (this.param.collapsed) {
            return;
        }
        oldValue = this.currentValue;
        this.updateCurrentValue(-1);
        if (oldValue != this.currentValue) {
            this.updateDisplay();
            this.Invalidate();
        }
    }
    
    public void updateCurrentValue(int aFieldIndex) {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldSmallint)) {
            this.plant.transferField(UNRESOLVED.kGetField, this.currentValue, this.param.fieldNumber, UNRESOLVED.kFieldSmallint, UNRESOLVED.kNotArray, false, null);
            if (this.currentValue < this.minValue) {
                this.minValue = this.currentValue;
                this.slider.minValue = this.minValue;
            }
            if (this.currentValue > this.maxValue) {
                this.maxValue = this.currentValue;
                this.slider.maxValue = this.maxValue;
            }
        } else {
            this.currentValue = 0;
        }
    }
    
    public void updateDisplay() {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldSmallint)) {
            this.slider.currentValue = this.currentValue;
        } else {
            this.slider.currentValue = 0;
            this.slider.Enabled = false;
        }
    }
    
    public void sliderMouseDown(TObject Sender) {
        if (this.plant == null) {
            return;
        }
        this.selectedItemIndex = kItemSlider;
        this.slider.hasUnofficialFocus = true;
        this.currentValueWhileSliding = this.slider.currentValue;
        this.Invalidate();
        if (!this.Focused()) {
            this.SetFocus();
        }
    }
    
    public void sliderMouseMove(TObject Sender) {
        if (this.plant == null) {
            return;
        }
        this.currentValueWhileSliding = this.slider.currentValue;
        this.Invalidate();
    }
    
    public void sliderMouseUp(TObject Sender) {
        if (this.plant != null) {
            this.currentValue = this.slider.currentValue;
            UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeSmallintValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValue, this.param.fieldNumber, UNRESOLVED.kNotArray, this.param.regrow));
            this.updateDisplay();
            this.Invalidate();
        } else {
            this.slider.currentValue = 0;
            this.slider.Enabled = false;
        }
    }
    
    public void sliderKeyDown(TOBject sender) {
        this.sliderMouseUp(sender);
    }
    
    public int maxWidth() {
        result = 0;
        result = uppanel.kLeftRightGap * 2 + UNRESOLVED.intMax(this.labelWidth, this.minScaleWidthWithBounds());
        return result;
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        int widthForLongestWord = 0;
        int widthWithBounds = 0;
        int widthWithoutBounds = 0;
        
        widthForLongestWord = uppanel.kLeftRightGap * 2 + this.longestLabelWordWidth;
        widthWithBounds = this.minScaleWidthWithBounds();
        widthWithoutBounds = this.minScaleWidthWithoutBounds();
        result = -1;
        if (requestedWidth < widthForLongestWord) {
            result = widthForLongestWord;
        }
        if (requestedWidth < widthWithBounds) {
            this.drawWithoutBounds = true;
            if (requestedWidth < widthWithoutBounds) {
                result = UNRESOLVED.intMax(result, widthWithoutBounds);
            }
        } else {
            this.drawWithoutBounds = false;
        }
        return result;
    }
    
    public int minScaleWidthWithBounds() {
        result = 0;
        String minString = "";
        String valueString = "";
        String unitString = "";
        String maxString = "";
        
        minString = IntToStr(this.minValue);
        valueString = IntToStr(this.currentValue) + "  ";
        unitString = UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.unitIndex);
        maxString = IntToStr(this.maxValue);
        result = this.formTextWidth(minString + valueString + unitString + maxString) + udebug.kBetweenGap * 3;
        return result;
    }
    
    public int minScaleWidthWithoutBounds() {
        result = 0;
        String valueString = "";
        String unitString = "";
        
        valueString = IntToStr(this.currentValue) + "  ";
        unitString = UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.unitIndex);
        result = this.formTextWidth(valueString + unitString) + udebug.kBetweenGap;
        return result;
    }
    
    public int uncollapsedHeight() {
        result = 0;
        result = this.collapsedHeight() + this.textHeight + uppanel.kTopBottomGap;
        return result;
    }
    
    public void resizeElements() {
        this.paint();
        this.slider.Left = this.minTextRect.Right + uppanel.kSliderSpaceGap;
        this.slider.Top = this.collapsedHeight() + this.textHeight / 2 - this.slider.Height / 2;
        this.slider.Width = UNRESOLVED.intMax(0, this.maxTextRect.Left - this.minTextRect.Right - uppanel.kSliderSpaceGap * 2);
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        if ((!this.param.collapsed) && (this.slider.Enabled)) {
            result = kItemSlider;
        } else {
            result = uppanel.kItemLabel;
        }
        return result;
    }
    
    public void paint() {
        TRect Rect = new TRect();
        String minString = "";
        String valueString = "";
        String maxString = "";
        String unitString = "";
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if ((this.selectedItemIndex == kItemSlider)) {
            // ask slider to update itself based on whether it is selected 
            this.slider.hasUnofficialFocus = true;
        } else {
            this.slider.hasUnofficialFocus = false;
        }
        super.paint();
        this.slider.Visible = !this.param.collapsed;
        if ((this.param.collapsed)) {
            this.drawExtraValueCaptionWithString(IntToStr(this.currentValue), UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.unitIndex));
            return;
        }
        Rect = this.GetClientRect();
        minString = IntToStr(this.minValue);
        if (this.slider.dragging) {
            valueString = IntToStr(this.currentValueWhileSliding);
        } else {
            valueString = IntToStr(this.currentValue);
        }
        unitString = UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.unitIndex);
        maxString = IntToStr(this.maxValue);
        this.valueTextRect.Left = uppanel.kLeftRightGap;
        this.valueTextRect.Right = this.valueTextRect.Left + this.Canvas.TextWidth(valueString);
        this.valueTextRect.Top = this.collapsedHeight() + 1;
        this.valueTextRect.Bottom = this.valueTextRect.Top + this.textHeight;
        this.unitTextRect = this.valueTextRect;
        this.unitTextRect.Left = this.valueTextRect.Right + 5;
        this.unitTextRect.Right = this.unitTextRect.Left + this.Canvas.TextWidth(unitString);
        this.minTextRect = this.valueTextRect;
        this.minTextRect.Left = this.unitTextRect.Right + 5;
        this.minTextRect.Right = this.minTextRect.Left + this.Canvas.TextWidth(minString);
        this.maxTextRect = this.valueTextRect;
        this.maxTextRect.Right = Rect.right - uppanel.kLeftRightGap;
        this.maxTextRect.Left = this.maxTextRect.Right - this.Canvas.TextWidth(maxString);
        this.drawText(minString, this.minTextRect, false, false, true);
        this.drawText(valueString, this.valueTextRect, !this.readOnly, (this.selectedItemIndex == kItemValueText), false);
        this.drawText(unitString, this.unitTextRect, false, false, false);
        this.drawText(maxString, this.maxTextRect, false, false, true);
    }
    
}
