# unit upp_boo

from conversion_common import *
import udebug
import udomain
import usupport
import uunits
import umath
import updcom
import umain
import uppanel
import uparams
import uplant
import delphi_compatability

# const
kItemYes = 1
kItemNo = 2

class PdBooleanParameterPanel(PdParameterPanel):
    def __init__(self):
        self.currentValue = false
        self.yesRect = TRect()
        self.noRect = TRect()
        self.editEnabled = false
    
    def initialize(self):
        self.currentValue = false
        self.editEnabled = false
    
    def updateEnabling(self):
        PdParameterPanel.updateEnabling(self)
        if (self.plant == None) or (self.readOnly):
            self.editEnabled = false
        else:
            self.editEnabled = true
    
    def updatePlantValues(self):
        if self.plant == None:
            return
        if self.param.collapsed:
            return
        self.updateCurrentValue(-1)
        self.updateDisplay()
        self.Invalidate()
    
    def updateCurrentValue(self, aFieldIndex):
        if self.plant != None:
            if self.param.fieldType == uparams.kFieldBoolean:
                self.currentValue = self.plant.transferField(umath.kGetField, self.currentValue, self.param.fieldNumber, uparams.kFieldBoolean, uparams.kNotArray, false, None)
                self.updateDisplay()
        else:
            self.currentValue = false
            self.editEnabled = false
    
    def updateDisplay(self):
        if self.plant != None:
            if self.param.fieldType == uparams.kFieldBoolean:
                self.Invalidate()
        else:
            self.editEnabled = false
    
    def doMouseDown(self, Sender, Button, Shift, X, Y):
        thePoint = TPoint()
        newValue = false
        
        # must always call this first because it sets the focus 
        PdParameterPanel.doMouseDown(self, Sender, Button, Shift, X, Y)
        if (self.editEnabled):
            thePoint = Point(X, Y)
            newValue = self.currentValue
            if delphi_compatability.PtInRect(self.yesRect, thePoint):
                newValue = true
                self.selectedItemIndex = kItemYes
            elif delphi_compatability.PtInRect(self.noRect, thePoint):
                newValue = false
                self.selectedItemIndex = kItemNo
            self.Invalidate()
            if (newValue != self.currentValue):
                self.negateValue()
    
    def doKeyDown(self, sender, key, shift):
        newValue = false
        
        PdParameterPanel.doKeyDown(self, sender, key, shift)
        if (key == delphi_compatability.VK_RETURN) and (self.editEnabled):
            newValue = self.currentValue
            if self.selectedItemIndex == kItemYes:
                newValue = true
            elif self.selectedItemIndex == kItemNo:
                newValue = false
            if (newValue != self.currentValue):
                self.negateValue()
        return key
    
    def negateValue(self):
        self.currentValue = not self.currentValue
        if self.plant != None:
            umain.MainForm.doCommand(updcom.PdChangeBooleanValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValue, self.param.fieldNumber, uparams.kNotArray, self.param.regrow))
        self.Invalidate()
    
    def maxWidth(self):
        result = 0
        result = umath.intMax(uppanel.kLeftRightGap * 2 + self.longestLabelWordWidth, uppanel.kRadioButtonLeftGap + (self.yesRect.Right - self.yesRect.Left) + uppanel.kRadioButtonBetweenGap + (self.noRect.Right - self.noRect.Left) + uppanel.kLeftRightGap)
        return result
    
    def minWidth(self, requestedWidth):
        result = 0
        minAllowed = 0
        
        minAllowed = umath.intMax(uppanel.kLeftRightGap * 2 + self.longestLabelWordWidth, uppanel.kRadioButtonLeftGap + (self.yesRect.Right - self.yesRect.Left) + uppanel.kRadioButtonBetweenGap + (self.noRect.Right - self.noRect.Left) + uppanel.kLeftRightGap)
        if requestedWidth > minAllowed:
            result = -1
        else:
            result = minAllowed
        return result
    
    def uncollapsedHeight(self):
        result = 0
        result = self.collapsedHeight() + self.textHeight + uppanel.kTopBottomGap
        return result
    
    def maxSelectedItemIndex(self):
        result = 0
        if (not self.param.collapsed) and (self.editEnabled):
            result = kItemNo
        else:
            result = uppanel.kItemLabel
        return result
    
    def resizeElements(self):
        pass
        # do nothing 
    
    def paint(self):
        rect = TRect()
        circleYesRect = TRect()
        circleNoRect = TRect()
        yesTextRect = TRect()
        noTextRect = TRect()
        
        PdParameterPanel.paint(self)
        if (self.param.collapsed):
            if self.currentValue:
                self.drawExtraValueCaptionWithString("yes", "")
            else:
                self.drawExtraValueCaptionWithString("no", "")
            return
        Rect = self.GetClientRect()
        self.Canvas.Font = self.Font
        circleYesRect.Left = Rect.left + uppanel.kRadioButtonLeftGap
        circleYesRect.Right = circleYesRect.Left + uppanel.kRadioButtonWidth
        circleYesRect.Top = Rect.top + self.collapsedHeight() + (self.textHeight / 2 - uppanel.kRadioButtonWidth / 2)
        circleYesRect.Bottom = circleYesRect.Top + uppanel.kRadioButtonWidth
        yesTextRect.Left = Rect.left + uppanel.kRadioButtonLeftGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap
        yesTextRect.Right = yesTextRect.Left + self.Canvas.TextWidth("yes")
        yesTextRect.Top = Rect.top + self.collapsedHeight()
        yesTextRect.Bottom = yesTextRect.Top + self.textHeight
        circleNoRect = circleYesRect
        circleNoRect.Left = yesTextRect.Right + uppanel.kRadioButtonBetweenGap
        circleNoRect.Right = circleNoRect.Left + uppanel.kRadioButtonWidth
        noTextRect = yesTextRect
        noTextRect.Left = yesTextRect.Right + uppanel.kRadioButtonBetweenGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap
        noTextRect.Right = noTextRect.Left + self.Canvas.TextWidth("no")
        self.drawRadioButton(self.currentValue, self.editEnabled, circleYesRect)
        self.drawText("yes", yesTextRect, true, (self.selectedItemIndex == kItemYes) and (self.editEnabled), false)
        self.drawRadioButton(not self.currentValue, self.editEnabled, circleNoRect)
        self.drawText("no", noTextRect, true, (self.selectedItemIndex == kItemNo) and (self.editEnabled), false)
        delphi_compatability.UnionRect(self.yesRect, circleYesRect, yesTextRect)
        delphi_compatability.UnionRect(self.noRect, circleNoRect, noTextRect)
    
    def drawRadioButton(self, value, enabled, rect):
        brushColor = TColor()
        
        brushColor = self.Canvas.Brush.Color
        if value:
            if enabled:
                self.Canvas.Brush.Color = UNRESOLVED.clBtnText
            else:
                self.Canvas.Brush.Color = UNRESOLVED.clBtnShadow
        else:
            self.Canvas.Brush.Color = UNRESOLVED.clBtnFace
        # FIX unresolved WITH expression: Rect
        self.Canvas.Ellipse(self.Left, self.Top, UNRESOLVED.right, UNRESOLVED.bottom)
        self.Canvas.Brush.Color = brushColor
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
    
