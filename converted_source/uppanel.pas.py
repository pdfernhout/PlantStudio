# unit uppanel

from conversion_common import *
import upp_hed
import udebug
import udomain
import usupport
import uunits
import umath
import updcom
import umain
import uplant
import ucollect
import usection
import uparams
import delphi_compatability

# const
kBetweenGap = 3
kTopBottomGap = 4
kLeftRightGap = 6
kRadioButtonLeftGap = 10
kRadioButtonWidth = 10
kRadioButtonBetweenGap = 10
kRadioButtonBeforeTextGap = 5
kSliderSpaceGap = 10
kEditMaxWidth = 100
kEditMinWidth = 50
kNotSelectedString = "(not selected)"
kGraphHeight = 100
kMaxDisplayDigitsToLeftOfDecimal = 7
kMaxDisplayDigitsToRightOfDecimal = 6
kMaxDisplayDigits = 9
kArrowPictureSize = 13
kOverridePictureSize = 0
kItemNone = -1
kItemLabel = 0

#200;
#150;
#150;
# 13
class PdParameterPanel(TPanel):
    def __init__(self):
        self.plant = PdPlant()
        self.param = PdParameter()
        self.readOnly = false
        self.labelWidth = 0
        self.textHeight = 0
        self.labelRect = TRect()
        self.pictureRect = TRect()
        self.overrideRect = TRect()
        self.wrappedLabelHeight = 0
        self.longestLabelWordWidth = 0
        self.selectedItemIndex = 0
    
    def create(self, anOwner):
        TPanel.create(self, anOwner)
        self.plant = None
        self.ParentFont = true
        self.OnMouseDown = self.doMouseDown
        self.OnMouseMove = self.doMouseMove
        self.OnMouseUp = self.doMouseUp
        self.OnKeyDown = self.doKeyDown
        self.OnEnter = self.doOnEnter
        self.OnExit = self.doOnExit
        self.TabStop = true
        self.Enabled = true
        if umain.MainForm != None:
            self.PopupMenu = umain.MainForm.paramPopupMenu
        return self
    
    def createForParameter(self, anOwner, aParameter):
        self.create(anOwner)
        self.param = aParameter
        self.readOnly = self.param.readOnly
        self.Caption = self.param.getName()
        self.initialize()
        self.updateDisplay()
        self.updateEnabling()
        self.selectedItemIndex = -1
        self.BevelInner = UNRESOLVED.bvRaised
        self.BevelOuter = UNRESOLVED.bvNone
        return self
    
    def formTextHeight(self):
        result = 0L
        theForm = TCustomForm()
        oldSize = 0
        
        theForm = UNRESOLVED.getParentForm(self)
        if theForm == None:
            #default
            result = 16
        elif theForm.Canvas == None:
            #default
            result = 16
        else:
            result = 16
            theForm.Canvas.Font = theForm.Font
            result = theForm.Canvas.TextHeight("W")
        return result
    
    def formTextWidth(self, aString):
        result = 0L
        theForm = TCustomForm()
        
        theForm = UNRESOLVED.getParentForm(self)
        if theForm == None:
            #default
            result = 50
        elif theForm.Canvas == None:
            #default
            result = 50
        else:
            result = len(aString) * 8
            theForm.Canvas.Font = theForm.Font
            result = theForm.Canvas.TextWidth(aString)
        return result
    
    def calculateTextDimensions(self):
        # use form canvas for this because when component is first created, doesn't know what font it has 
        self.textHeight = self.formTextHeight()
        self.labelWidth = self.formTextWidth(usupport.trimLeftAndRight(self.Caption))
        self.longestLabelWordWidth = self.calculateLongestLabelWordWidth()
    
    def doMouseDown(self, Sender, Button, Shift, X, Y):
        if not self.Focused():
            self.SetFocus()
        if X < self.pictureRect.Right:
            self.collapseOrExpand(Y)
        if not self.Focused():
            self.SetFocus()
        if self.param != None:
            if self.param.collapsed:
                self.selectedItemIndex = kItemLabel
    
    def doMouseMove(self, Sender, Shift, X, Y):
        pass
        # subclasses can override 
    
    def doMouseUp(self, Sender, Button, Shift, X, Y):
        pass
        # subclasses can override 
    
    def doKeyDown(self, sender, key, shift):
        Form = TCustomForm()
        
        if (key == delphi_compatability.VK_TAB):
            if shift == [delphi_compatability.TShiftStateEnum.ssShift, ]:
                # subclasses should override and respond to enter events when different items are selected 
                # subclasses should call inherited 
                self.tabThroughItems(false)
            else:
                self.tabThroughItems(true)
            if self.selectedItemIndex == kItemNone:
                Form = UNRESOLVED.getParentForm(self)
                if Form != None:
                    if shift == [delphi_compatability.TShiftStateEnum.ssShift, ]:
                        umain.TMainForm(Form).backTabbingInParametersPanel = true
                        #previous
                        Form.Perform(UNRESOLVED.wm_NextDlgCtl, 1, 0)
                    else:
                        Form.Perform(UNRESOLVED.wm_NextDlgCtl, 0, 0)
        elif (key == delphi_compatability.VK_RETURN) and (self.selectedItemIndex == kItemLabel):
            #give it a y as if the label was clicked on
            self.collapseOrExpand(0)
        return key
    
    def maxSelectedItemIndex(self):
        result = 0
        # subclasses should override 
        result = 0
        return result
    
    def tabThroughItems(self, goForward):
        # subclasses need not override this if they override maxSelectedItemIndex 
        self.selectedItemIndex = self.nextSelectedItemIndex(goForward)
        if self.selectedItemIndex > self.maxSelectedItemIndex():
            self.selectedItemIndex = kItemNone
        self.Invalidate()
    
    def nextSelectedItemIndex(self, goForward):
        result = 0
        if goForward:
            result = self.selectedItemIndex + 1
        else:
            result = self.selectedItemIndex - 1
        return result
    
    def WMGetDlgCode(self, message):
        TPanel.WMGetDlgCode(self)
        # want arrows allows us to pass arrow keys on to slider or combo box 
        message.Result = message.Result or delphi_compatability.DLGC_WANTTAB or delphi_compatability.DLGC_WANTARROWS
    
    def initialize(self):
        pass
        # sublasses can override 
    
    def doOnEnter(self, sender):
        umain.TMainForm(self.Owner).enteringAParameterPanel(self)
        if umain.TMainForm(self.Owner).backTabbingInParametersPanel:
            self.selectedItemIndex = self.maxSelectedItemIndex()
            umain.TMainForm(self.Owner).backTabbingInParametersPanel = false
        if self.selectedItemIndex == kItemNone:
            self.selectedItemIndex = kItemLabel
        self.Invalidate()
    
    def doOnExit(self, sender):
        umain.TMainForm(self.Owner).leavingAParameterPanel(self)
        self.selectedItemIndex = kItemNone
        self.Invalidate()
    
    #plant has changed
    def updatePlant(self, newPlant):
        if self.plant != newPlant:
            self.plant = newPlant
            self.updateEnabling()
            # -1 means update all 
            self.updateCurrentValue(-1)
            self.updateDisplay()
            self.Invalidate()
    
    def updatePlantValues(self):
        pass
        # subclasses should override 
    
    def updateEnabling(self):
        # subclasses should call this when they do their enabling 
        self.Enabled = (self.plant != None)
    
    def updateCurrentValue(self, aFieldIndex):
        pass
        # subclasses may override 
    
    def updateFromUpdateEventList(self, updateList):
        i = 0L
        updateEvent = PdPlantUpdateEvent()
        shouldUpdate = false
        
        if updateList.Count <= 0:
            return
        if self.plant == None:
            return
        shouldUpdate = false
        updateEvent = None
        for i in range(0, updateList.Count):
            updateEvent = uplant.PdPlantUpdateEvent(updateList.Items[i])
            if updateEvent == None:
                continue
            if updateEvent.plant == None:
                continue
            if (updateEvent.plant == self.plant) and (updateEvent.fieldID == self.param.fieldNumber):
                shouldUpdate = true
                break
        if shouldUpdate and (updateEvent != None):
            # could put check in descendents to only update if value is different from current 
            self.updateCurrentValue(updateEvent.fieldIndex)
            self.updateDisplay()
            self.Invalidate()
    
    def updateDisplay(self):
        pass
        # subclasses should override 
    
    def minWidth(self, requestedWidth):
        result = 0
        # subclasses must override 
        result = 0
        return result
    
    def maxWidth(self):
        result = 0
        # subclasses must override 
        result = 0
        return result
    
    def uncollapsedHeight(self):
        result = 0
        # subclasses must override 
        result = 0
        return result
    
    def resizeElements(self):
        pass
        # subclasses must override 
    
    def editHeight(self):
        result = 0
        result = self.textHeight + 8
        return result
    
    def calculateLongestLabelWordWidth(self):
        result = 0
        i = 0
        lastSpace = 0
        maxLength = 0
        
        # o: xxxxx xxxxxxxxx xx 
        lastSpace = 3
        maxLength = 0
        for i in range(4, len(self.Caption) + 1):
            if (self.Caption[i] == " ") or (i == len(self.Caption)):
                if i - lastSpace > maxLength:
                    maxLength = i - lastSpace
                lastSpace = i
        result = self.formTextWidth("w") * maxLength
        return result
    
    def calculateHeight(self):
        fullRect = TRect()
        
        fullRect = self.GetClientRect()
        self.labelRect.Left = fullRect.Left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap
        self.labelRect.Right = fullRect.Right - kLeftRightGap
        self.labelRect.Top = fullRect.Top + 2
        self.labelRect.Bottom = self.labelRect.Top + self.textHeight
        self.wrappedLabelHeight = self.measureText(self.Caption, self.labelRect)
        if self.param != None:
            if self.param.collapsed:
                self.Height = self.collapsedHeight()
            else:
                self.Height = self.uncollapsedHeight()
    
    def collapseOrExpand(self, y):
        if y > self.collapsedHeight():
            return
        if self.param != None:
            if not self.param.collapsed:
                self.collapse()
            else:
                self.expand()
        if (self.Owner != None) and (not umain.TMainForm(self.Owner).internalChange):
            umain.TMainForm(self.Owner).repositionParameterPanels()
    
    def collapse(self):
        if self.param != None:
            self.param.collapsed = true
        self.Height = self.collapsedHeight()
    
    def expand(self):
        if self.param != None:
            self.param.collapsed = false
        self.Height = self.uncollapsedHeight()
        #  updateCurrentValue(-1); 
        #cfk don't think i need this anymore
    
    def paint(self):
        fullRect = TRect()
        
        # copied from TCustomPanel.paint and location of caption text changed 
        # can't call inherited paint because it wants to put the caption in the middle 
        self.fillWithBevels()
        fullRect = self.GetClientRect()
        self.Canvas.Font = self.Font
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.labelRect.Left = fullRect.Left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap
        self.labelRect.Right = self.labelRect.Left + self.Width - kLeftRightGap * 2 - kArrowPictureSize - kOverridePictureSize
        self.labelRect.Top = fullRect.Top + 2
        self.labelRect.Bottom = self.labelRect.Top + self.textHeight
        self.wrappedLabelHeight = self.drawText(self.Caption, self.labelRect, false, false, false)
        self.pictureRect.Left = fullRect.Left + kLeftRightGap
        self.pictureRect.Right = self.pictureRect.Left + kArrowPictureSize
        self.pictureRect.Top = self.labelRect.Top + 1
        self.pictureRect.Bottom = self.pictureRect.Top + kArrowPictureSize
        if (self.plant != None) and (self.param != None):
            if self.param.collapsed:
                #
                #    with overrideRect do
                #      begin
                #      left := pictureRect.right;
                #      right := left + kOverridePictureSize;
                #      top := labelRect.top + 1;
                #      bottom := top + kOverridePictureSize;
                #      end;
                #      
                self.Canvas.Draw(self.pictureRect.Left, self.pictureRect.Top, umain.MainForm.paramPanelClosedArrowImage.Picture.Bitmap)
            else:
                self.Canvas.Draw(self.pictureRect.Left, self.pictureRect.Top, umain.MainForm.paramPanelOpenArrowImage.Picture.Bitmap)
            #
            #      if (not param.cannotOverride) and (param.isOverridden) then
            #        draw(overrideRect.left, overrideRect.top, MainForm.paramOverride.picture.bitmap)
            #      else
            #        draw(overrideRect.left, overrideRect.top, MainForm.paramOverrideNot.picture.bitmap);
            #        
        if (self.selectedItemIndex == kItemLabel):
            self.Canvas.Rectangle(self.pictureRect.Left, self.pictureRect.Top, self.pictureRect.Right, self.pictureRect.Bottom)
    
    def drawExtraValueCaptionWithString(self, valueString, unitString):
        rect = TRect()
        collapsedExtraRect = TRect()
        stringToDisplay = ""
        
        if (self.wrappedLabelHeight > self.textHeight):
            return
        stringToDisplay = ":  " + valueString
        if unitString != "(no unit)":
            stringToDisplay = stringToDisplay + " " + unitString
        Rect = self.GetClientRect()
        collapsedExtraRect.Left = Rect.left + kLeftRightGap + kArrowPictureSize + kOverridePictureSize + kBetweenGap + self.Canvas.TextWidth(self.Caption)
        collapsedExtraRect.Right = Rect.right
        collapsedExtraRect.Top = Rect.top + 2
        collapsedExtraRect.Bottom = collapsedExtraRect.Top + self.textHeight
        if usupport.rWidth(collapsedExtraRect) <= self.Canvas.TextWidth(stringToDisplay):
            return
        self.drawText(stringToDisplay, collapsedExtraRect, false, false, false)
    
    def fillWithBevels(self):
        fullRect = TRect()
        TopColor = TColor()
        BottomColor = TColor()
        theForm = TCustomForm()
        
        # PDF PORT moved function inline 
        # procedure AdjustColors(Bevel: TPanelBevel);
        #  begin
        #  TopColor := clBtnHighlight;
        #  if Bevel = bvLowered then TopColor := clBtnShadow;
        #  BottomColor := clBtnShadow;
        #  if Bevel = bvLowered then BottomColor := clBtnHighlight;
        #  end;
        fullRect = self.GetClientRect()
        self.Canvas.Brush.Color = UNRESOLVED.clBtnFace
        theForm = UNRESOLVED.getParentForm(self)
        if (theForm != None) and (theForm.__class__ is umain.TMainForm) and ((theForm as umain.TMainForm).selectedParameterPanel == self):
            self.Canvas.Pen.Color = UNRESOLVED.clHighlight
            self.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
            # pen.width := 2; 
            self.Canvas.Rectangle(fullRect.Left + 2, fullRect.Top + 2, fullRect.Right - 1, fullRect.Bottom - 1)
        else:
            self.Canvas.FillRect(fullRect)
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        if self.BevelOuter != UNRESOLVED.bvNone:
            # AdjustColors(BevelOuter);
            TopColor = UNRESOLVED.clBtnHighlight
            if self.BevelOuter == UNRESOLVED.bvLowered:
                TopColor = UNRESOLVED.clBtnShadow
            BottomColor = UNRESOLVED.clBtnShadow
            if self.BevelOuter == UNRESOLVED.bvLowered:
                BottomColor = UNRESOLVED.clBtnHighlight
            UNRESOLVED.Frame3D(self.Canvas, fullRect, TopColor, BottomColor, self.BevelWidth)
        UNRESOLVED.Frame3D(self.Canvas, fullRect, self.Color, self.Color, self.BorderWidth)
        if self.BevelInner != UNRESOLVED.bvNone:
            # AdjustColors(BevelInner);
            TopColor = UNRESOLVED.clBtnHighlight
            if self.BevelInner == UNRESOLVED.bvLowered:
                TopColor = UNRESOLVED.clBtnShadow
            BottomColor = UNRESOLVED.clBtnShadow
            if self.BevelInner == UNRESOLVED.bvLowered:
                BottomColor = UNRESOLVED.clBtnHighlight
            UNRESOLVED.Frame3D(self.Canvas, fullRect, TopColor, BottomColor, self.BevelWidth)
    
    def measureText(self, text, drawRect):
        result = 0
        cText = [0] * (range(0, 255 + 1) + 1)
        theForm = TCustomForm()
        useRect = TRect()
        
        theForm = UNRESOLVED.getParentForm(self)
        if theForm == None:
            #default
            result = 16
        else:
            if theForm.Canvas == None:
                #default
                result = 16
            else:
                theForm.Canvas.Font = theForm.Font
                useRect = drawRect
                UNRESOLVED.strPCopy(cText, text)
                # returns height of rectangle 
                result = UNRESOLVED.winprocs.drawText(theForm.Canvas.Handle, cText, len(cText), useRect, delphi_compatability.DT_LEFT or delphi_compatability.DT_WORDBREAK or delphi_compatability.DT_CALCRECT)
        # cfk change v1.6b1 -- taken out, dealt with problem by using form to get size
        # deal with large fonts by increasing label height -- kludge
        #if screen.pixelsPerInch >= 120 then // large fonts
        #  result := round(result * 1.5);
        return result
    
    def drawText(self, text, drawRect, isSelectable, isSelected, italicize):
        result = 0
        cText = [0] * (range(0, 255 + 1) + 1)
        
        self.Canvas.Font = self.Font
        if self.plant != None:
            if self.__class__ is upp_hed.PdHeaderParameterPanel:
                self.Canvas.Font.Color = delphi_compatability.clWhite
            elif text == self.Caption:
                self.Canvas.Font.Color = delphi_compatability.clBlue
            else:
                self.Canvas.Font.Color = UNRESOLVED.clBtnText
        else:
            if self.__class__ is upp_hed.PdHeaderParameterPanel:
                self.Canvas.Font.Color = UNRESOLVED.clBtnFace
            else:
                self.Canvas.Font.Color = UNRESOLVED.clBtnShadow
        if italicize:
            self.Canvas.Font.Style = [UNRESOLVED.fsItalic, ]
        if self.__class__ is upp_hed.PdHeaderParameterPanel:
            self.Canvas.Font.Style = [UNRESOLVED.fsBold, ]
        UNRESOLVED.strPCopy(cText, text)
        result = UNRESOLVED.winprocs.drawText(self.Canvas.Handle, cText, len(cText), drawRect, delphi_compatability.DT_LEFT or delphi_compatability.DT_WORDBREAK or delphi_compatability.DT_NOCLIP)
        drawRect.Bottom = drawRect.Top + result
        if (isSelected):
            self.drawTextSelectedBox(drawRect)
        elif (isSelectable):
            self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
            self.Canvas.MoveTo(drawRect.Left, drawRect.Bottom - 3)
            self.Canvas.LineTo(drawRect.Right, drawRect.Bottom - 3)
        return result
    
    def drawTextSelectedBox(self, rect):
        self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
        self.Canvas.MoveTo(Rect.right + 2, Rect.top)
        self.Canvas.LineTo(Rect.left - 2, Rect.top)
        self.Canvas.LineTo(Rect.left - 2, Rect.bottom - 2)
        self.Canvas.LineTo(Rect.right + 2, Rect.bottom - 2)
        self.Canvas.LineTo(Rect.right + 2, Rect.top)
    
    def drawTextLabel(self, text, drawRect, drawBox):
        cText = [0] * (range(0, 255 + 1) + 1)
        
        self.Canvas.Font = self.Font
        self.Canvas.Font.Color = UNRESOLVED.clBtnText
        UNRESOLVED.strPCopy(cText, text)
        UNRESOLVED.winprocs.drawText(self.Canvas.Handle, cText, len(cText), drawRect, delphi_compatability.DT_LEFT or delphi_compatability.DT_WORDBREAK)
        if drawBox:
            self.drawTextSelectedBox(drawRect)
    
    def collapsedHeight(self):
        result = 0
        result = self.wrappedLabelHeight + kTopBottomGap
        result = umath.intMax(result, kArrowPictureSize + 5)
        return result
    
    def minScaleWidthWithBounds(self, unitSet, unitPlant, softMin, softMax):
        result = 0
        i = 0
        numeralChars = 0
        letterChars = 0
        maxLengthSoftMin = 0
        maxLengthSoftMax = 0
        minValue = 0.0
        maxValue = 0.0
        
        # value number of chars (always use max) 
        #+ kMaxDisplayDigitsToRightOfDecimal + 1
        numeralChars = kMaxDisplayDigitsToLeftOfDecimal
        # unit string number of chars (get max for set) 
        letterChars = uunits.maxUnitStringLengthForSet(unitSet)
        # bounds number of chars (use actual bounds, but calculate max for set) 
        maxLengthSoftMin = 0
        maxLengthSoftMax = 0
        for i in range(1, uunits.GetLastUnitEnumInUnitSet(unitSet)):
            minValue = uunits.Convert(unitSet, unitPlant, i, softMin)
            maxValue = uunits.Convert(unitSet, unitPlant, i, softMax)
            maxLengthSoftMin = umath.intMax(maxLengthSoftMin, len(usupport.digitValueString(minValue)))
            maxLengthSoftMax = umath.intMax(maxLengthSoftMax, len(usupport.digitValueString(maxValue)))
        numeralChars = numeralChars + maxLengthSoftMin + maxLengthSoftMax
        # calc min scale width from number of chars 
        result = self.formTextWidth("i") * letterChars + self.formTextWidth("1") * numeralChars + kBetweenGap * 3 + kLeftRightGap * 2
        return result
    
    def minScaleWidthWithoutBounds(self, unitSet, unitPlant):
        result = 0
        numeralChars = 0
        letterChars = 0
        
        # value number of chars (always use max) 
        #+ kMaxDisplayDigitsToRightOfDecimal + 1
        numeralChars = kMaxDisplayDigitsToLeftOfDecimal
        # unit string number of chars (get max for set) 
        letterChars = uunits.maxUnitStringLengthForSet(unitSet)
        # calc min scale width from number of chars 
        result = self.formTextWidth("i") * letterChars + self.formTextWidth("1") * numeralChars + kBetweenGap + kLeftRightGap * 2
        return result
    
