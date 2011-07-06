// unit upp_rea

from conversion_common import *;
import udebug;
import usliders;
import uppanel;
import delphi_compatability;

// const
kItemSlider = 1;
kItemValueText = 2;
kItemUnitText = 3;



class PdRealParameterPanel extends PdParameterPanel {
    public float currentValue;
    public float currentValueWhileSliding;
    public float minValue;
    public float maxValue;
    public KfSlider slider;
    public int currentUnitIndex;
    public TRect valueTextRect;
    public TRect unitTextRect;
    public TRect minTextRect;
    public TRect maxTextRect;
    public boolean drawWithoutBounds;
    public short arrayIndex;
    
    public void initialize() {
        //assuming slider will be deleted automatically by owner - self - otherwise would have destructor
        this.slider = usliders.KfSlider().create(this);
        this.slider.Parent = this;
        this.slider.FOnMouseDown = this.sliderMouseDown;
        this.slider.FOnMouseMove = this.sliderMouseMove;
        this.slider.FOnMouseUp = this.sliderMouseUp;
        this.slider.FOnKeyDown = this.sliderKeyDown;
        // make it a percentage move 
        this.slider.maxValue = 100;
        this.slider.minValue = 0;
        this.slider.readOnly = this.param.readOnly;
        this.slider.useDefaultSizeAndDraggerSize();
        this.arrayIndex = UNRESOLVED.kNotArray;
        if (UNRESOLVED.domain.options.useMetricUnits) {
            this.currentUnitIndex = this.param.unitMetric;
        } else {
            this.currentUnitIndex = this.param.unitEnglish;
        }
        this.minValue = this.param.lowerBound;
        this.maxValue = this.param.upperBound;
    }
    
    public void adjustValue() {
        ansistring newString = new ansistring();
        float oldValueInCurrentUnit = 0.0;
        float newValue = 0.0;
        float newValueInPlantUnit = 0.0;
        String oldString = "";
        String prompt = "";
        String nameString = "";
        String unitString = "";
        String minString = "";
        String maxString = "";
        boolean outOfRange = false;
        
        oldValueInCurrentUnit = this.toCurrentUnit(this.currentValue);
        newString = UNRESOLVED.digitValueString(oldValueInCurrentUnit);
        oldString = newString;
        nameString = UNRESOLVED.copy(this.Caption, 1, 30);
        if (len(nameString) == 30) {
            nameString = nameString + "...";
        }
        unitString = UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.currentUnitIndex);
        minString = UNRESOLVED.digitValueString(this.toCurrentUnit(this.minValue));
        maxString = UNRESOLVED.digitValueString(this.toCurrentUnit(this.maxValue));
        prompt = "Type a new value.";
        if (InputQuery("Enter value", prompt, newString)) {
            if ((newString != oldString) && (UNRESOLVED.boundForString(newString, this.param.fieldType, newValue))) {
                newValueInPlantUnit = this.toPlantUnit(newValue);
                outOfRange = this.checkValueAgainstBounds(newValueInPlantUnit);
                if (!outOfRange) {
                    this.currentValue = newValueInPlantUnit;
                    UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeRealValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValue, this.param.fieldNumber, this.arrayIndex, this.param.regrow));
                    this.updateDisplay();
                    this.Invalidate();
                }
            }
        }
    }
    
    public float toPlantUnit(float value) {
        result = 0.0;
        result = UNRESOLVED.Convert(this.param.unitSet, this.currentUnitIndex, this.param.unitModel, value);
        return result;
    }
    
    public float toCurrentUnit(float value) {
        result = 0.0;
        result = UNRESOLVED.Convert(this.param.unitSet, this.param.unitModel, this.currentUnitIndex, value);
        return result;
    }
    
    public boolean checkValueAgainstBounds(float aValue) {
        result = false;
        result = (aValue < this.minValue) || (aValue > this.maxValue);
        return result;
    }
    
    public void selectNextUnitInSet(boolean shift, boolean ctrl) {
        if (shift) {
            this.currentUnitIndex = UNRESOLVED.GetPreviousUnitEnumInUnitSet(this.param.unitSet, this.currentUnitIndex);
        } else {
            this.currentUnitIndex = UNRESOLVED.GetNextUnitEnumInUnitSet(this.param.unitSet, this.currentUnitIndex);
        }
        this.updateCurrentValue(-1);
        this.updateDisplay();
        this.Invalidate();
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
        } else if (delphi_compatability.PtInRect(this.unitTextRect, thePoint)) {
            this.selectedItemIndex = kItemUnitText;
            this.Invalidate();
            this.selectNextUnitInSet(delphi_compatability.TShiftStateEnum.ssShift in Shift, delphi_compatability.TShiftStateEnum.ssCtrl in Shift);
        }
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        if (this.slider.Enabled && !this.slider.readOnly) {
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
        super.doKeyDown(sender, key, shift);
        if ((key == delphi_compatability.VK_RETURN)) {
            switch (this.selectedItemIndex) {
                case kItemSlider:
                    if (this.slider.Enabled && !this.slider.readOnly) {
                        key = this.slider.doKeyDown(sender, key, shift);
                    }
                    break;
                case kItemValueText:
                    if (this.slider.Enabled && !this.slider.readOnly) {
                        this.adjustValue();
                    }
                    break;
                case kItemUnitText:
                    this.selectNextUnitInSet(delphi_compatability.TShiftStateEnum.ssShift in shift, delphi_compatability.TShiftStateEnum.ssCtrl in shift);
                    break;
        }
        return key;
    }
    
    public int sliderPositionFromValue(float value) {
        result = 0;
        if (this.maxValue - this.minValue == 0.0) {
            result = 0;
        } else if (value <= this.minValue) {
            result = 0;
        } else if (value >= this.maxValue) {
            result = 100;
        } else {
            result = intround(100.0 * (value - this.minValue) / (this.maxValue - this.minValue));
        }
        return result;
    }
    
    public float valueFromSliderPosition() {
        result = 0.0;
        float sliderPosition = 0.0;
        
        sliderPosition = this.slider.currentValue;
        result = this.minValue + sliderPosition / 100.0 * (this.maxValue - this.minValue);
        return result;
    }
    
    public void updateEnabling() {
        super.updateEnabling();
        this.slider.Enabled = this.plant != null;
        this.slider.readOnly = this.readOnly;
    }
    
    public void updatePlantValues() {
        float oldValue = 0.0;
        
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
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldFloat)) {
            this.plant.transferField(UNRESOLVED.kGetField, this.currentValue, this.param.fieldNumber, UNRESOLVED.kFieldFloat, this.arrayIndex, false, null);
            if (this.currentValue < this.minValue) {
                this.currentValue = this.minValue;
            }
            if (this.currentValue > this.maxValue) {
                this.currentValue = this.maxValue;
            }
        } else {
            this.currentValue = 0.0;
        }
    }
    
    public void updateDisplay() {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldFloat)) {
            this.slider.currentValue = this.sliderPositionFromValue(this.currentValue);
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
        this.currentValueWhileSliding = this.valueFromSliderPosition();
        this.Invalidate();
        if (!this.Focused()) {
            this.SetFocus();
        }
    }
    
    public void sliderMouseMove(TObject Sender) {
        if (this.plant == null) {
            return;
        }
        this.currentValueWhileSliding = this.valueFromSliderPosition();
        this.Invalidate();
    }
    
    public void sliderMouseUp(TObject Sender) {
        if (this.plant == null) {
            return;
        }
        this.currentValue = this.valueFromSliderPosition();
        UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeRealValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValue, this.param.fieldNumber, this.arrayIndex, this.param.regrow));
        this.Invalidate();
    }
    
    public void sliderKeyDown(TObject Sender) {
        this.sliderMouseUp(Sender);
    }
    
    public int maxWidth() {
        result = 0;
        result = UNRESOLVED.intMax(uppanel.kLeftRightGap * 2 + this.labelWidth, this.minScaleWidthWithBounds(this.param.unitSet, this.param.unitModel, this.minValue, this.maxValue));
        return result;
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        int widthForLongestWord = 0;
        int widthWithBounds = 0;
        int widthWithoutBounds = 0;
        
        // 1. test if width given is less than labelWidth.
        //       if not, move on
        //       if so, test if width given is less than width of longest full word in labelWidth.
        //         if not, move on
        //         if so, give back width of longest full word in labelWidth as minWidth.
        //    2. test if width given is less than minScaleWidthWithBounds.
        //       if not, move on (set flag to draw bounds)
        //       if so, test if width given is less than minScaleWidthWithoutBounds.
        //         if not, move on (set flag to not draw bounds)
        //         if so, give back minScaleWidthWithoutBounds as minWidth.
        //  
        widthForLongestWord = uppanel.kLeftRightGap * 2 + this.longestLabelWordWidth;
        widthWithBounds = this.minScaleWidthWithBounds(this.param.unitSet, this.param.unitModel, this.minValue, this.maxValue);
        widthWithoutBounds = this.minScaleWidthWithoutBounds(this.param.unitSet, this.param.unitModel);
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
        if ((!this.param.collapsed) && (this.plant != null)) {
            result = kItemUnitText;
        } else {
            result = uppanel.kItemLabel;
        }
        return result;
    }
    
    public int nextSelectedItemIndex(boolean goForward) {
        result = 0;
        result = uppanel.kItemNone;
        switch (this.selectedItemIndex) {
            case uppanel.kItemNone:
                result = this.selectedItemIndex;
                break;
            case uppanel.kItemLabel:
                if (goForward) {
                    result = kItemValueText;
                } else {
                    result = uppanel.kItemNone;
                }
                break;
            case kItemSlider:
                if (goForward) {
                    result = uppanel.kItemNone;
                } else {
                    result = kItemUnitText;
                }
                break;
            case kItemValueText:
                if (goForward) {
                    result = kItemUnitText;
                } else {
                    result = uppanel.kItemLabel;
                }
                break;
            case kItemUnitText:
                if (goForward) {
                    result = kItemSlider;
                } else {
                    result = kItemValueText;
                }
                break;
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
            this.drawExtraValueCaptionWithString(UNRESOLVED.digitValueString(this.toCurrentUnit(this.currentValue)), UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.currentUnitIndex));
            return;
        }
        Rect = this.GetClientRect();
        minString = UNRESOLVED.digitValueString(this.toCurrentUnit(this.minValue));
        maxString = UNRESOLVED.digitValueString(this.toCurrentUnit(this.maxValue));
        if (this.slider.dragging) {
            valueString = UNRESOLVED.digitValueString(this.toCurrentUnit(this.currentValueWhileSliding));
        } else {
            valueString = UNRESOLVED.digitValueString(this.toCurrentUnit(this.currentValue));
        }
        unitString = UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.currentUnitIndex);
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
        this.drawText(unitString, this.unitTextRect, true, (this.selectedItemIndex == kItemUnitText), false);
        this.drawText(maxString, this.maxTextRect, false, false, true);
    }
    
}
