// unit uppanel

from conversion_common import *;
import upp_hed;
import udebug;
import delphi_compatability;

// const
kBetweenGap = 3;
kTopBottomGap = 4;
kLeftRightGap = 6;
kRadioButtonLeftGap = 10;
kRadioButtonWidth = 10;
kRadioButtonBetweenGap = 10;
kRadioButtonBeforeTextGap = 5;
kSliderSpaceGap = 10;
kEditMaxWidth = 100;
kEditMinWidth = 50;
kNotSelectedString = "(not selected)";
kGraphHeight = 100;
kMaxDisplayDigitsToLeftOfDecimal = 7;
kMaxDisplayDigitsToRightOfDecimal = 6;
kMaxDisplayDigits = 9;
kArrowPictureSize = 13;
kOverridePictureSize = 0;
kItemNone = -1;
kItemLabel = 0;



//200;
//150;
//150;
// 13
class PdParameterPanel extends TPanel {
    public PdPlant plant;
    public PdParameter param;
    public boolean readOnly;
    public int labelWidth;
    public int textHeight;
    public TRect labelRect;
    public TRect pictureRect;
    public TRect overrideRect;
    public int wrappedLabelHeight;
    public int longestLabelWordWidth;
    public int selectedItemIndex;
    
    public void create(TComponent anOwner) {
        super.create(anOwner);
        this.plant = null;
        this.ParentFont = true;
        this.OnMouseDown = this.doMouseDown;
        this.OnMouseMove = this.doMouseMove;
        this.OnMouseUp = this.doMouseUp;
        this.OnKeyDown = this.doKeyDown;
        this.OnEnter = this.doOnEnter;
        this.OnExit = this.doOnExit;
        this.TabStop = true;
        this.Enabled = true;
        if (UNRESOLVED.MainForm != null) {
            this.PopupMenu = UNRESOLVED.MainForm.paramPopupMenu;
        }
    }
    
    public void createForParameter(TComponent anOwner, PdParameter aParameter) {
        this.create(anOwner);
        this.param = aParameter;
        this.readOnly = this.param.readOnly;
        this.Caption = this.param.getName;
        this.initialize();
        this.updateDisplay();
        this.updateEnabling();
        this.selectedItemIndex = -1;
        this.BevelInner = UNRESOLVED.bvRaised;
        this.BevelOuter = UNRESOLVED.bvNone;
    }
    
    public long formTextHeight() {
        result = 0;
        TCustomForm theForm = new TCustomForm();
        int oldSize = 0;
        
        theForm = UNRESOLVED.getParentForm(this);
        if (theForm == null) {
            //default
            result = 16;
        } else if (theForm.Canvas == null) {
            //default
            result = 16;
        } else {
            result = 16;
            theForm.Canvas.Font = theForm.Font;
            result = theForm.Canvas.TextHeight("W");
        }
        return result;
    }
    
    public long formTextWidth(String aString) {
        result = 0;
        TCustomForm theForm = new TCustomForm();
        
        theForm = UNRESOLVED.getParentForm(this);
        if (theForm == null) {
            //default
            result = 50;
        } else if (theForm.Canvas == null) {
            //default
            result = 50;
        } else {
            result = len(aString) * 8;
            theForm.Canvas.Font = theForm.Font;
            result = theForm.Canvas.TextWidth(aString);
        }
        return result;
    }
    
    public void calculateTextDimensions() {
        // use form canvas for this because when component is first created, doesn't know what font it has 
        this.textHeight = this.formTextHeight();
        this.labelWidth = this.formTextWidth(UNRESOLVED.trimLeftAndRight(this.Caption));
        this.longestLabelWordWidth = this.calculateLongestLabelWordWidth();
    }
    
    public void doMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        if (!this.Focused()) {
            this.SetFocus();
        }
        if (X < this.pictureRect.Right) {
            this.collapseOrExpand(Y);
        }
        if (!this.Focused()) {
            this.SetFocus();
        }
        if (this.param != null) {
            if (this.param.collapsed) {
                this.selectedItemIndex = kItemLabel;
            }
        }
    }
    
    public void doMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        pass
        // subclasses can override 
    }
    
    public void doMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        pass
        // subclasses can override 
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        TCustomForm Form = new TCustomForm();
        
        if ((key == delphi_compatability.VK_TAB)) {
            if (shift == {delphi_compatability.TShiftStateEnum.ssShift, }) {
                // subclasses should override and respond to enter events when different items are selected 
                // subclasses should call inherited 
                this.tabThroughItems(false);
            } else {
                this.tabThroughItems(true);
            }
            if (this.selectedItemIndex == kItemNone) {
                Form = UNRESOLVED.getParentForm(this);
                if (Form != null) {
                    if (shift == {delphi_compatability.TShiftStateEnum.ssShift, }) {
                        UNRESOLVED.TMainForm(Form).backTabbingInParametersPanel = true;
                        //previous
                        Form.Perform(UNRESOLVED.wm_NextDlgCtl, 1, 0);
                    } else {
                        Form.Perform(UNRESOLVED.wm_NextDlgCtl, 0, 0);
                    }
                }
            }
        } else if ((key == delphi_compatability.VK_RETURN) && (this.selectedItemIndex == kItemLabel)) {
            //give it a y as if the label was clicked on
            this.collapseOrExpand(0);
        }
        return key;
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        // subclasses should override 
        result = 0;
        return result;
    }
    
    public void tabThroughItems(boolean goForward) {
        // subclasses need not override this if they override maxSelectedItemIndex 
        this.selectedItemIndex = this.nextSelectedItemIndex(goForward);
        if (this.selectedItemIndex > this.maxSelectedItemIndex()) {
            this.selectedItemIndex = kItemNone;
        }
        this.Invalidate();
    }
    
    public int nextSelectedItemIndex(boolean goForward) {
        result = 0;
        if (goForward) {
            result = this.selectedItemIndex + 1;
        } else {
            result = this.selectedItemIndex - 1;
        }
        return result;
    }
    
    public void WMGetDlgCode(TWMGetDlgCode message) {
        super.WMGetDlgCode();
        // want arrows allows us to pass arrow keys on to slider or combo box 
        message.Result = message.Result || delphi_compatability.DLGC_WANTTAB || delphi_compatability.DLGC_WANTARROWS;
    }
    
    public void initialize() {
        pass
        // sublasses can override 
    }
    
    public void doOnEnter(TObject sender) {
        UNRESOLVED.TMainForm(this.Owner).enteringAParameterPanel(this);
        if (UNRESOLVED.TMainForm(this.Owner).backTabbingInParametersPanel) {
            this.selectedItemIndex = this.maxSelectedItemIndex();
            UNRESOLVED.TMainForm(this.Owner).backTabbingInParametersPanel = false;
        }
        if (this.selectedItemIndex == kItemNone) {
            this.selectedItemIndex = kItemLabel;
        }
        this.Invalidate();
    }
    
    public void doOnExit(TObject sender) {
        UNRESOLVED.TMainForm(this.Owner).leavingAParameterPanel(this);
        this.selectedItemIndex = kItemNone;
        this.Invalidate();
    }
    
    //plant has changed
    public void updatePlant(PdPlant newPlant) {
        if (this.plant != newPlant) {
            this.plant = newPlant;
            this.updateEnabling();
            // -1 means update all 
            this.updateCurrentValue(-1);
            this.updateDisplay();
            this.Invalidate();
        }
    }
    
    public void updatePlantValues() {
        pass
        // subclasses should override 
    }
    
    public void updateEnabling() {
        // subclasses should call this when they do their enabling 
        this.Enabled = (this.plant != null);
    }
    
    public void updateCurrentValue(int aFieldIndex) {
        pass
        // subclasses may override 
    }
    
    public void updateFromUpdateEventList(TListCollection updateList) {
        long i = 0;
        PdPlantUpdateEvent updateEvent = new PdPlantUpdateEvent();
        boolean shouldUpdate = false;
        
        if (updateList.count <= 0) {
            return;
        }
        if (this.plant == null) {
            return;
        }
        shouldUpdate = false;
        updateEvent = null;
        for (i = 0; i <= updateList.count - 1; i++) {
            updateEvent = UNRESOLVED.PdPlantUpdateEvent(updateList.items[i]);
            if (updateEvent == null) {
                continue;
            }
            if (updateEvent.plant == null) {
                continue;
            }
            if ((updateEvent.plant == this.plant) && (updateEvent.fieldID == this.param.fieldNumber)) {
                shouldUpdate = true;
                break;
            }
        }
        if (shouldUpdate && (updateEvent != null)) {
            // could put check in descendents to only update if value is different from current 
            this.updateCurrentValue(updateEvent.fieldIndex);
            this.updateDisplay();
            this.Invalidate();
        }
    }
    
    public void updateDisplay() {
        pass
        // subclasses should override 
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        // subclasses must override 
        result = 0;
        return result;
    }
    
    public int maxWidth() {
        result = 0;
        // subclasses must override 
        result = 0;
        return result;
    }
    
    public int uncollapsedHeight() {
        result = 0;
        // subclasses must override 
        result = 0;
        return result;
    }
    
    public void resizeElements() {
        pass
        // subclasses must override 
    }
    
    public int editHeight() {
        result = 0;
        result = this.textHeight + 8;
        return result;
    }
    
    public int calculateLongestLabelWordWidth() {
        result = 0;
        int i = 0;
        int lastSpace = 0;
        int maxLength = 0;
        
        // o: xxxxx xxxxxxxxx xx 
        lastSpace = 3;
        maxLength = 0;
        for (i = 4; i <= len(this.Caption); i++) {
            if ((this.Caption[i] == " ") || (i == len(this.Caption))) {
                if (i - lastSpace > maxLength) {
                    maxLength = i - lastSpace;
                }
                lastSpace = i;
            }
        }
        result = this.formTextWidth("w") * maxLength;
        return result;
    }
    
    public void calculateHeight() {
        TRect fullRect = new TRect();
        
        fullRect = this.GetClientRect();
        this.labelRect.Left = fullRect.Left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap;
        this.labelRect.Right = fullRect.Right - kLeftRightGap;
        this.labelRect.Top = fullRect.Top + 2;
        this.labelRect.Bottom = this.labelRect.Top + this.textHeight;
        this.wrappedLabelHeight = this.measureText(this.Caption, this.labelRect);
        if (this.param != null) {
            if (this.param.collapsed) {
                this.Height = this.collapsedHeight();
            } else {
                this.Height = this.uncollapsedHeight();
            }
        }
    }
    
    public void collapseOrExpand(int y) {
        if (y > this.collapsedHeight()) {
            return;
        }
        if (this.param != null) {
            if (!this.param.collapsed) {
                this.collapse();
            } else {
                this.expand();
            }
        }
        if ((this.Owner != null) && (!UNRESOLVED.TMainForm(this.Owner).internalChange)) {
            UNRESOLVED.TMainForm(this.Owner).repositionParameterPanels;
        }
    }
    
    public void collapse() {
        if (this.param != null) {
            this.param.collapsed = true;
        }
        this.Height = this.collapsedHeight();
    }
    
    public void expand() {
        if (this.param != null) {
            this.param.collapsed = false;
        }
        this.Height = this.uncollapsedHeight();
        //  updateCurrentValue(-1); 
        //cfk don't think i need this anymore
    }
    
    public void paint() {
        TRect fullRect = new TRect();
        
        // copied from TCustomPanel.paint and location of caption text changed 
        // can't call inherited paint because it wants to put the caption in the middle 
        this.fillWithBevels();
        fullRect = this.GetClientRect();
        this.Canvas.Font = this.Font;
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        this.labelRect.Left = fullRect.Left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap;
        this.labelRect.Right = this.labelRect.Left + this.Width - kLeftRightGap * 2 - kArrowPictureSize - kOverridePictureSize;
        this.labelRect.Top = fullRect.Top + 2;
        this.labelRect.Bottom = this.labelRect.Top + this.textHeight;
        this.wrappedLabelHeight = this.drawText(this.Caption, this.labelRect, false, false, false);
        this.pictureRect.Left = fullRect.Left + kLeftRightGap;
        this.pictureRect.Right = this.pictureRect.Left + kArrowPictureSize;
        this.pictureRect.Top = this.labelRect.Top + 1;
        this.pictureRect.Bottom = this.pictureRect.Top + kArrowPictureSize;
        if ((this.plant != null) && (this.param != null)) {
            if (this.param.collapsed) {
                //
                //    with overrideRect do
                //      begin
                //      left := pictureRect.right;
                //      right := left + kOverridePictureSize;
                //      top := labelRect.top + 1;
                //      bottom := top + kOverridePictureSize;
                //      end;
                //      
                this.Canvas.Draw(this.pictureRect.Left, this.pictureRect.Top, UNRESOLVED.MainForm.paramPanelClosedArrowImage.picture.bitmap);
            } else {
                this.Canvas.Draw(this.pictureRect.Left, this.pictureRect.Top, UNRESOLVED.MainForm.paramPanelOpenArrowImage.picture.bitmap);
            }
            //
            //      if (not param.cannotOverride) and (param.isOverridden) then
            //        draw(overrideRect.left, overrideRect.top, MainForm.paramOverride.picture.bitmap)
            //      else
            //        draw(overrideRect.left, overrideRect.top, MainForm.paramOverrideNot.picture.bitmap);
            //        
        }
        if ((this.selectedItemIndex == kItemLabel)) {
            this.Canvas.Rectangle(this.pictureRect.Left, this.pictureRect.Top, this.pictureRect.Right, this.pictureRect.Bottom);
        }
    }
    
    public void drawExtraValueCaptionWithString(String valueString, String unitString) {
        TRect rect = new TRect();
        TRect collapsedExtraRect = new TRect();
        String stringToDisplay = "";
        
        if ((this.wrappedLabelHeight > this.textHeight)) {
            return;
        }
        stringToDisplay = ":  " + valueString;
        if (unitString != "(no unit)") {
            stringToDisplay = stringToDisplay + " " + unitString;
        }
        Rect = this.GetClientRect();
        collapsedExtraRect.Left = Rect.left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap + this.Canvas.TextWidth(this.Caption);
        collapsedExtraRect.Right = Rect.right;
        collapsedExtraRect.Top = Rect.top + 2;
        collapsedExtraRect.Bottom = collapsedExtraRect.Top + this.textHeight;
        if (UNRESOLVED.rWidth(collapsedExtraRect) <= this.Canvas.TextWidth(stringToDisplay)) {
            return;
        }
        this.drawText(stringToDisplay, collapsedExtraRect, false, false, false);
    }
    
    public void fillWithBevels() {
        TRect fullRect = new TRect();
        TColor TopColor = new TColor();
        TColor BottomColor = new TColor();
        TCustomForm theForm = new TCustomForm();
        
        // PDF PORT moved function inline 
        // procedure AdjustColors(Bevel: TPanelBevel);
        //  begin
        //  TopColor := clBtnHighlight;
        //  if Bevel = bvLowered then TopColor := clBtnShadow;
        //  BottomColor := clBtnShadow;
        //  if Bevel = bvLowered then BottomColor := clBtnHighlight;
        //  end;
        fullRect = this.GetClientRect();
        this.Canvas.Brush.Color = UNRESOLVED.clBtnFace;
        theForm = UNRESOLVED.getParentForm(this);
        if ((theForm != null) && (theForm instanceof UNRESOLVED.TMainForm) && (((UNRESOLVED.TMainForm)theForm).selectedParameterPanel == this)) {
            this.Canvas.Pen.Color = UNRESOLVED.clHighlight;
            this.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid;
            // pen.width := 2; 
            this.Canvas.Rectangle(fullRect.Left + 2, fullRect.Top + 2, fullRect.Right - 1, fullRect.Bottom - 1);
        } else {
            this.Canvas.FillRect(fullRect);
        }
        this.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        if (this.BevelOuter != UNRESOLVED.bvNone) {
            // AdjustColors(BevelOuter);
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
            // AdjustColors(BevelInner);
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
    
    public int measureText(String text, TRect drawRect) {
        result = 0;
         cText = [0] * (range(0, 255 + 1) + 1);
        TCustomForm theForm = new TCustomForm();
        TRect useRect = new TRect();
        
        theForm = UNRESOLVED.getParentForm(this);
        if (theForm == null) {
            //default
            result = 16;
        } else {
            if (theForm.Canvas == null) {
                //default
                result = 16;
            } else {
                theForm.Canvas.Font = theForm.Font;
                useRect = drawRect;
                UNRESOLVED.strPCopy(cText, text);
                // returns height of rectangle 
                result = UNRESOLVED.winprocs.drawText(theForm.Canvas.Handle, cText, len(cText), useRect, delphi_compatability.DT_LEFT || delphi_compatability.DT_WORDBREAK || delphi_compatability.DT_CALCRECT);
            }
        }
        // cfk change v1.6b1 -- taken out, dealt with problem by using form to get size
        // deal with large fonts by increasing label height -- kludge
        //if screen.pixelsPerInch >= 120 then // large fonts
        //  result := round(result * 1.5);
        return result;
    }
    
    public int drawText(String text, TRect drawRect, boolean isSelectable, boolean isSelected, boolean italicize) {
        result = 0;
         cText = [0] * (range(0, 255 + 1) + 1);
        
        this.Canvas.Font = this.Font;
        if (this.plant != null) {
            if (this instanceof upp_hed.PdHeaderParameterPanel) {
                this.Canvas.Font.Color = delphi_compatability.clWhite;
            } else if (text == this.Caption) {
                this.Canvas.Font.Color = delphi_compatability.clBlue;
            } else {
                this.Canvas.Font.Color = UNRESOLVED.clBtnText;
            }
        } else {
            if (this instanceof upp_hed.PdHeaderParameterPanel) {
                this.Canvas.Font.Color = UNRESOLVED.clBtnFace;
            } else {
                this.Canvas.Font.Color = UNRESOLVED.clBtnShadow;
            }
        }
        if (italicize) {
            this.Canvas.Font.Style = {UNRESOLVED.fsItalic, };
        }
        if (this instanceof upp_hed.PdHeaderParameterPanel) {
            this.Canvas.Font.Style = {UNRESOLVED.fsBold, };
        }
        UNRESOLVED.strPCopy(cText, text);
        result = UNRESOLVED.winprocs.drawText(this.Canvas.Handle, cText, len(cText), drawRect, delphi_compatability.DT_LEFT || delphi_compatability.DT_WORDBREAK || delphi_compatability.DT_NOCLIP);
        drawRect.Bottom = drawRect.Top + result;
        if ((isSelected)) {
            this.drawTextSelectedBox(drawRect);
        } else if ((isSelectable)) {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
            this.Canvas.MoveTo(drawRect.Left, drawRect.Bottom - 3);
            this.Canvas.LineTo(drawRect.Right, drawRect.Bottom - 3);
        }
        return result;
    }
    
    public void drawTextSelectedBox(TRect rect) {
        this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
        this.Canvas.MoveTo(Rect.right + 2, Rect.top);
        this.Canvas.LineTo(Rect.left - 2, Rect.top);
        this.Canvas.LineTo(Rect.left - 2, Rect.bottom - 2);
        this.Canvas.LineTo(Rect.right + 2, Rect.bottom - 2);
        this.Canvas.LineTo(Rect.right + 2, Rect.top);
    }
    
    public void drawTextLabel(String text, TRect drawRect, boolean drawBox) {
         cText = [0] * (range(0, 255 + 1) + 1);
        
        this.Canvas.Font = this.Font;
        this.Canvas.Font.Color = UNRESOLVED.clBtnText;
        UNRESOLVED.strPCopy(cText, text);
        UNRESOLVED.winprocs.drawText(this.Canvas.Handle, cText, len(cText), drawRect, delphi_compatability.DT_LEFT || delphi_compatability.DT_WORDBREAK);
        if (drawBox) {
            this.drawTextSelectedBox(drawRect);
        }
    }
    
    public int collapsedHeight() {
        result = 0;
        result = this.wrappedLabelHeight + kTopBottomGap;
        result = UNRESOLVED.intMax(result, kArrowPictureSize + 5);
        return result;
    }
    
    public int minScaleWidthWithBounds(int unitSet, int unitPlant, float softMin, float softMax) {
        result = 0;
        int i = 0;
        int numeralChars = 0;
        int letterChars = 0;
        int maxLengthSoftMin = 0;
        int maxLengthSoftMax = 0;
        float minValue = 0.0;
        float maxValue = 0.0;
        
        // value number of chars (always use max) 
        //+ kMaxDisplayDigitsToRightOfDecimal + 1
        numeralChars = kMaxDisplayDigitsToLeftOfDecimal;
        // unit string number of chars (get max for set) 
        letterChars = UNRESOLVED.maxUnitStringLengthForSet(unitSet);
        // bounds number of chars (use actual bounds, but calculate max for set) 
        maxLengthSoftMin = 0;
        maxLengthSoftMax = 0;
        for (i = 1; i <= UNRESOLVED.GetLastUnitEnumInUnitSet(unitSet) - 1; i++) {
            minValue = UNRESOLVED.Convert(unitSet, unitPlant, i, softMin);
            maxValue = UNRESOLVED.Convert(unitSet, unitPlant, i, softMax);
            maxLengthSoftMin = UNRESOLVED.intMax(maxLengthSoftMin, len(UNRESOLVED.digitValueString(minValue)));
            maxLengthSoftMax = UNRESOLVED.intMax(maxLengthSoftMax, len(UNRESOLVED.digitValueString(maxValue)));
        }
        numeralChars = numeralChars + maxLengthSoftMin + maxLengthSoftMax;
        // calc min scale width from number of chars 
        result = this.formTextWidth("i") * letterChars + this.formTextWidth("1") * numeralChars + kBetweenGap * 3 + kLeftRightGap * 2;
        return result;
    }
    
    public int minScaleWidthWithoutBounds(int unitSet, int unitPlant) {
        result = 0;
        int numeralChars = 0;
        int letterChars = 0;
        
        // value number of chars (always use max) 
        //+ kMaxDisplayDigitsToRightOfDecimal + 1
        numeralChars = kMaxDisplayDigitsToLeftOfDecimal;
        // unit string number of chars (get max for set) 
        letterChars = UNRESOLVED.maxUnitStringLengthForSet(unitSet);
        // calc min scale width from number of chars 
        result = this.formTextWidth("i") * letterChars + this.formTextWidth("1") * numeralChars + kBetweenGap + kLeftRightGap * 2;
        return result;
    }
    
}
