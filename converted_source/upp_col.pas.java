// unit upp_col

from conversion_common import *;
import ubmpsupport;
import udebug;
import usliders;
import uppanel;
import delphi_compatability;

// const
kItemColorRect = 1;
kItemRedSlider = 2;
kItemGreenSlider = 3;
kItemBlueSlider = 4;
kColorRectSize = 40;
kMinSliderLength = 30;



class PdColorParameterPanel extends PdParameterPanel {
    public TColorRef currentColor;
    public TColorRef colorWhileDragging;
    public KfSlider redSlider;
    public KfSlider greenSlider;
    public KfSlider blueSlider;
    public TRect colorRect;
    
    public HPALETTE GetPalette() {
        result = new HPALETTE();
        result = UNRESOLVED.MainForm.paletteImage.picture.bitmap.palette;
        return result;
    }
    
    public void initialize() {
        //assuming sliders will be deleted automatically by owner - self - otherwise would have destructor
        this.redSlider = usliders.KfSlider().create(this);
        this.initSlider(this.redSlider);
        this.greenSlider = usliders.KfSlider().create(this);
        this.initSlider(this.greenSlider);
        this.blueSlider = usliders.KfSlider().create(this);
        this.initSlider(this.blueSlider);
        this.OnMouseUp = this.doMouseUp;
    }
    
    public void initSlider(KfSlider slider) {
        slider.Parent = this;
        slider.FOnMouseDown = this.sliderMouseDown;
        slider.FOnMouseMove = this.sliderMouseMove;
        slider.FOnMouseUp = this.sliderMouseUp;
        slider.FOnKeyDown = this.sliderKeyDown;
        slider.readOnly = this.param.readOnly;
        slider.useDefaultSizeAndDraggerSize();
        slider.minValue = 0;
        slider.maxValue = 255;
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        if ((this.plant != null) && (!this.readOnly)) {
            switch (key) {
                case delphi_compatability.VK_HOME:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
                case delphi_compatability.VK_END:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
                case delphi_compatability.VK_DOWN:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
                case delphi_compatability.VK_LEFT:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
                case delphi_compatability.VK_UP:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
                case delphi_compatability.VK_RIGHT:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
                case delphi_compatability.VK_NEXT:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
                case delphi_compatability.VK_PRIOR:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
                case delphi_compatability.VK_RETURN:
                    switch (this.selectedItemIndex) {
                        case kItemRedSlider:
                            // process slider arrow keys first 
                            key = this.redSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemGreenSlider:
                            key = this.greenSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemBlueSlider:
                            key = this.blueSlider.doKeyDown(sender, key, shift);
                            return key;
                            break;
                        case kItemColorRect:
                            this.doMouseUp(this, delphi_compatability.TMouseButton.mbLeft, {}, this.colorRect.Left + 1, this.colorRect.Top + 1);
                            break;
                    break;
        }
        super.doKeyDown(sender, key, shift);
        return key;
    }
    
    public void doMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint thePoint = new TPoint();
        TColorRef newColor = new TColorRef();
        
        // must always call this first because it sets the focus 
        super.doMouseUp(Sender, Button, Shift, X, Y);
        if ((this.plant == null) || (this.readOnly)) {
            return;
        }
        thePoint = Point(X, Y);
        if (delphi_compatability.PtInRect(this.colorRect, thePoint)) {
            this.selectedItemIndex = kItemColorRect;
            newColor = UNRESOLVED.domain.getColorUsingCustomColors(this.currentColor);
            if (newColor != this.currentColor) {
                this.currentColor = newColor;
                UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeColorValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentColor, this.param.fieldNumber, UNRESOLVED.kNotArray, this.param.regrow));
                this.updateDisplay();
                this.Invalidate();
            }
        }
    }
    
    public void updateEnabling() {
        super.updateEnabling();
        this.redSlider.Enabled = this.plant != null;
        this.greenSlider.Enabled = this.plant != null;
        this.blueSlider.Enabled = this.plant != null;
        this.redSlider.readOnly = this.readOnly;
        this.greenSlider.readOnly = this.readOnly;
        this.blueSlider.readOnly = this.readOnly;
    }
    
    public void updatePlantValues() {
        TColorRef oldColor = new TColorRef();
        
        if (this.plant == null) {
            return;
        }
        if (this.param.collapsed) {
            return;
        }
        oldColor = this.currentColor;
        this.updateCurrentValue(-1);
        if (oldColor != this.currentColor) {
            this.updateDisplay();
            this.Invalidate();
        }
    }
    
    public void updateCurrentValue(int aFieldIndex) {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldColor)) {
            this.plant.transferField(UNRESOLVED.kGetField, this.currentColor, this.param.fieldNumber, UNRESOLVED.kFieldColor, UNRESOLVED.kNotArray, false, null);
        } else {
            this.disableSliders();
        }
    }
    
    public void disableSliders() {
        this.redSlider.currentValue = 0;
        this.redSlider.Enabled = false;
        this.greenSlider.currentValue = 0;
        this.greenSlider.Enabled = false;
        this.blueSlider.currentValue = 0;
        this.blueSlider.Enabled = false;
    }
    
    public void updateDisplay() {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldColor)) {
            this.redSlider.currentValue = UNRESOLVED.getRValue(this.currentColor);
            this.greenSlider.currentValue = UNRESOLVED.getGValue(this.currentColor);
            this.blueSlider.currentValue = UNRESOLVED.getBValue(this.currentColor);
        } else {
            this.disableSliders();
        }
    }
    
    public void sliderMouseDown(TObject Sender) {
        if (this.plant == null) {
            return;
        }
        this.colorWhileDragging = UNRESOLVED.support_rgb(this.redSlider.currentValue, this.greenSlider.currentValue, this.blueSlider.currentValue);
        if (Sender == this.redSlider) {
            this.selectedItemIndex = kItemRedSlider;
        } else if (Sender == this.greenSlider) {
            this.selectedItemIndex = kItemGreenSlider;
        } else if (Sender == this.blueSlider) {
            this.selectedItemIndex = kItemBlueSlider;
        }
        if (!this.Focused()) {
            this.SetFocus();
        } else {
            this.Invalidate();
        }
        // paint method updates unofficial focus flags in sliders 
    }
    
    public void sliderMouseMove(TObject Sender) {
        if (this.plant != null) {
            this.colorWhileDragging = UNRESOLVED.support_rgb(this.redSlider.currentValue, this.greenSlider.currentValue, this.blueSlider.currentValue);
            // don't make change permanent yet, not until mouse up 
            this.Repaint();
        } else {
            this.disableSliders();
        }
    }
    
    public void sliderMouseUp(TObject Sender) {
        if (this.plant != null) {
            this.currentColor = UNRESOLVED.support_rgb(this.redSlider.currentValue, this.greenSlider.currentValue, this.blueSlider.currentValue);
            UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeColorValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentColor, this.param.fieldNumber, UNRESOLVED.kNotArray, this.param.regrow));
            this.updateDisplay();
            this.Invalidate();
        } else {
            this.disableSliders();
        }
    }
    
    public void sliderKeyDown(TOBject sender) {
        this.sliderMouseUp(sender);
    }
    
    public int maxWidth() {
        result = 0;
        result = uppanel.kLeftRightGap * 2 + UNRESOLVED.intMax(this.labelWidth, uppanel.kEditMaxWidth);
        return result;
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        int minAllowed = 0;
        
        minAllowed = uppanel.kLeftRightGap * 2 + UNRESOLVED.intMax(this.longestLabelWordWidth, kColorRectSize + kMinSliderLength + udebug.kBetweenGap);
        if (requestedWidth > minAllowed) {
            result = -1;
        } else {
            result = minAllowed;
        }
        return result;
    }
    
    public int uncollapsedHeight() {
        result = 0;
        result = this.collapsedHeight() + UNRESOLVED.intMax(this.redSlider.Height, this.textHeight) * 3 + udebug.kBetweenGap * 2 + uppanel.kTopBottomGap * 3;
        return result;
    }
    
    public void resizeElements() {
        this.redSlider.Left = uppanel.kLeftRightGap + kColorRectSize + this.formTextWidth("W") + uppanel.kLeftRightGap * 2;
        this.redSlider.Width = UNRESOLVED.intMax(0, this.Width - this.redSlider.Left - uppanel.kLeftRightGap);
        this.redSlider.Top = this.collapsedHeight() + uppanel.kTopBottomGap + this.Canvas.TextHeight("r") / 2 - this.redSlider.Height / 2;
        this.greenSlider.Left = this.redSlider.Left;
        this.greenSlider.Width = this.redSlider.Width;
        this.greenSlider.Top = this.redSlider.Top + this.textHeight + this.Canvas.TextHeight("r") / 2 - this.greenSlider.Height / 2;
        this.blueSlider.Left = this.redSlider.Left;
        this.blueSlider.Width = this.redSlider.Width;
        this.blueSlider.Top = this.greenSlider.Top + this.textHeight + this.Canvas.TextHeight("r") / 2 - this.blueSlider.Height / 2;
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        if ((!this.param.collapsed) && (this.redSlider.Enabled)) {
            result = kItemBlueSlider;
        } else {
            result = uppanel.kItemLabel;
        }
        return result;
    }
    
    public void paint() {
        TRect aRect = new TRect();
        TRect rTextRect = new TRect();
        TRect gTextRect = new TRect();
        TRect bTextRect = new TRect();
        TRect collapsedColorRect = new TRect();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        // ask sliders to update themselves based on whether they are selected 
        this.redSlider.hasUnofficialFocus = (this.selectedItemIndex == kItemRedSlider);
        this.greenSlider.hasUnofficialFocus = (this.selectedItemIndex == kItemGreenSlider);
        this.blueSlider.hasUnofficialFocus = (this.selectedItemIndex == kItemBlueSlider);
        super.paint();
        aRect = this.GetClientRect();
        if ((this.param.collapsed) && (this.plant != null)) {
            collapsedColorRect.Left = aRect.Left + uppanel.kLeftRightGap + uppanel.kArrowPictureSize + uppanel.kOverridePictureSize + udebug.kBetweenGap + this.Canvas.TextWidth(this.Caption) + uppanel.kLeftRightGap;
            collapsedColorRect.Right = collapsedColorRect.Left + this.textHeight * 2;
            collapsedColorRect.Top = aRect.Top + 2;
            collapsedColorRect.Bottom = collapsedColorRect.Top + this.textHeight;
            UNRESOLVED.inflateRect(collapsedColorRect, -2, -2);
            this.fillRectWithColor(collapsedColorRect, this.currentColor);
            return;
        }
        rTextRect.Left = aRect.Left + uppanel.kLeftRightGap + kColorRectSize + uppanel.kLeftRightGap * 2;
        rTextRect.Right = rTextRect.Left + this.Canvas.TextWidth("W");
        rTextRect.Top = this.collapsedHeight() + uppanel.kTopBottomGap;
        rTextRect.Bottom = rTextRect.Top + this.textHeight;
        gTextRect = rTextRect;
        gTextRect.Top = rTextRect.Bottom + udebug.kBetweenGap;
        gTextRect.Bottom = gTextRect.Top + this.textHeight;
        bTextRect = rTextRect;
        bTextRect.Top = gTextRect.Bottom + udebug.kBetweenGap;
        bTextRect.Bottom = bTextRect.Top + this.textHeight;
        this.colorRect.Left = uppanel.kLeftRightGap * 2;
        this.colorRect.Right = rTextRect.Left - uppanel.kLeftRightGap * 2;
        this.colorRect.Top = this.collapsedHeight() + uppanel.kTopBottomGap;
        this.colorRect.Bottom = this.uncollapsedHeight() - uppanel.kTopBottomGap * 2;
        this.drawText("r", rTextRect, false, false, false);
        this.drawText("g", gTextRect, false, false, false);
        this.drawText("b", bTextRect, false, false, false);
        if ((this.redSlider.dragging) || (this.greenSlider.dragging) || (this.blueSlider.dragging)) {
            this.fillRectWithColor(this.colorRect, this.colorWhileDragging);
        } else if (this.plant == null) {
            this.fillRectWithColor(this.colorRect, UNRESOLVED.clBtnFace);
        } else {
            this.fillRectWithColor(this.colorRect, this.currentColor);
        }
        this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
        if ((this.selectedItemIndex != kItemColorRect)) {
            this.Canvas.Pen.Width = 1;
            this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
        } else {
            this.Canvas.Pen.Width = 3;
            this.Canvas.Pen.Color = UNRESOLVED.clBtnHighlight;
        }
        this.Canvas.Pen.Width = 1;
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        this.Canvas.Rectangle(this.colorRect.Left - 1, this.colorRect.Top - 1, this.colorRect.Right + 1, this.colorRect.Bottom + 1);
    }
    
    public void fillRectWithColor(TRect aRect, TColorRef aColor) {
        TBitmap bitmap = new TBitmap();
        
        bitmap = delphi_compatability.TBitmap().Create();
        try {
            try {
                bitmap.Width = UNRESOLVED.rWidth(aRect);
                bitmap.Height = UNRESOLVED.rHeight(aRect);
            } catch (Exception e) {
                bitmap.Width = 1;
                bitmap.Height = 1;
            }
            ubmpsupport.setPixelFormatBasedOnScreenForBitmap(bitmap);
            bitmap.Canvas.Brush.Color = aColor;
            bitmap.Canvas.FillRect(Rect(0, 0, bitmap.Width, bitmap.Height));
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(bitmap, this.Canvas, aRect);
        } finally {
            bitmap.free;
        }
    }
    
}
