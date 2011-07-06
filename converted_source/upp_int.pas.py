# unit upp_int

from conversion_common import *
import udebug
import udomain
import usupport
import uunits
import umath
import updcom
import umain
import usliders
import uppanel
import uparams
import uplant
import delphi_compatability

# const
kItemValueText = 1
kItemSlider = 2

#  kItemUnitText = 2;    
class PdSmallintParameterPanel(PdParameterPanel):
    def __init__(self):
        self.currentValue = 0
        self.currentValueWhileSliding = 0
        self.minValue = 0
        self.maxValue = 0
        self.slider = KfSlider()
        self.unitIndex = 0
        self.minTextRect = TRect()
        self.maxTextRect = TRect()
        self.valueTextRect = TRect()
        self.unitTextRect = TRect()
        self.drawWithoutBounds = false
    
    def initialize(self):
        #assuming slider will be deleted automatically by owner - self - otherwise would have destructor
        self.slider = usliders.KfSlider().create(self)
        self.slider.Parent = self
        self.slider.FOnMouseDown = self.sliderMouseDown
        self.slider.FOnMouseMove = self.sliderMouseMove
        self.slider.FOnMouseUp = self.sliderMouseUp
        self.slider.FOnKeyDown = self.sliderKeyDown
        self.slider.readOnly = self.param.readOnly
        self.slider.useDefaultSizeAndDraggerSize()
        self.minValue = intround(self.param.lowerBound())
        self.maxValue = intround(self.param.upperBound())
        self.slider.minValue = self.minValue
        self.slider.maxValue = self.maxValue
    
    def checkValueAgainstBounds(self, value):
        result = 0
        result = value
        if result < self.minValue:
            result = self.minValue
        if result > self.maxValue:
            result = self.maxValue
        return result
    
    def doMouseUp(self, Sender, Button, Shift, X, Y):
        thePoint = TPoint()
        
        # must always call this first because it sets the focus 
        PdParameterPanel.doMouseUp(self, Sender, Button, Shift, X, Y)
        thePoint = Point(X, Y)
        if delphi_compatability.PtInRect(self.valueTextRect, thePoint):
            if self.slider.Enabled and not self.slider.readOnly:
                self.selectedItemIndex = kItemValueText
                self.Invalidate()
                self.adjustValue()
    
    def doKeyDown(self, sender, key, shift):
        if self.slider.Enabled:
            if key == delphi_compatability.VK_HOME:
                if (self.selectedItemIndex == kItemSlider):
                    # process slider arrow keys first 
                    key = self.slider.doKeyDown(sender, key, shift)
                    return key
            elif key == delphi_compatability.VK_END:
                if (self.selectedItemIndex == kItemSlider):
                    # process slider arrow keys first 
                    key = self.slider.doKeyDown(sender, key, shift)
                    return key
            elif key == delphi_compatability.VK_DOWN:
                if (self.selectedItemIndex == kItemSlider):
                    # process slider arrow keys first 
                    key = self.slider.doKeyDown(sender, key, shift)
                    return key
            elif key == delphi_compatability.VK_LEFT:
                if (self.selectedItemIndex == kItemSlider):
                    # process slider arrow keys first 
                    key = self.slider.doKeyDown(sender, key, shift)
                    return key
            elif key == delphi_compatability.VK_UP:
                if (self.selectedItemIndex == kItemSlider):
                    # process slider arrow keys first 
                    key = self.slider.doKeyDown(sender, key, shift)
                    return key
            elif key == delphi_compatability.VK_RIGHT:
                if (self.selectedItemIndex == kItemSlider):
                    # process slider arrow keys first 
                    key = self.slider.doKeyDown(sender, key, shift)
                    return key
            elif key == delphi_compatability.VK_NEXT:
                if (self.selectedItemIndex == kItemSlider):
                    # process slider arrow keys first 
                    key = self.slider.doKeyDown(sender, key, shift)
                    return key
            elif key == delphi_compatability.VK_PRIOR:
                if (self.selectedItemIndex == kItemSlider):
                    # process slider arrow keys first 
                    key = self.slider.doKeyDown(sender, key, shift)
                    return key
        if (self.selectedItemIndex == kItemValueText) and (key == delphi_compatability.VK_RETURN):
            key = 0
            self.Invalidate()
            self.adjustValue()
            return key
        PdParameterPanel.doKeyDown(self, sender, key, shift)
        if self.slider.Enabled:
            if (key == delphi_compatability.VK_RETURN) and (self.selectedItemIndex == kItemSlider):
                key = self.slider.doKeyDown(sender, key, shift)
        return key
    
    def adjustValue(self):
        newString = ansistring()
        oldValue = 0
        newValue = 0
        oldString = ""
        prompt = ""
        nameString = ""
        unitString = ""
        
        oldValue = self.currentValue
        newString = IntToStr(self.currentValue)
        oldString = newString
        nameString = UNRESOLVED.copy(self.Caption, 1, 30)
        if len(nameString) == 30:
            nameString = nameString + "..."
        unitString = uunits.UnitStringForEnum(self.param.unitSet, self.unitIndex)
        prompt = "Type a new value."
        if InputQuery("Enter value", prompt, newString):
            if (newString != oldString):
                newValue = StrToIntDef(newString, 0)
                if self.checkValueAgainstBounds(newValue) == newValue:
                    self.currentValue = newValue
                    umain.MainForm.doCommand(updcom.PdChangeSmallintValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValue, self.param.fieldNumber, uparams.kNotArray, self.param.regrow))
                    self.updateDisplay()
                    self.Invalidate()
    
    def updateEnabling(self):
        PdParameterPanel.updateEnabling(self)
        self.slider.Enabled = self.plant != None
        self.slider.readOnly = self.readOnly
    
    def updatePlantValues(self):
        oldValue = 0
        
        if self.plant == None:
            return
        if self.param.collapsed:
            return
        oldValue = self.currentValue
        self.updateCurrentValue(-1)
        if oldValue != self.currentValue:
            self.updateDisplay()
            self.Invalidate()
    
    def updateCurrentValue(self, aFieldIndex):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldSmallint):
            self.currentValue = self.plant.transferField(umath.kGetField, self.currentValue, self.param.fieldNumber, uparams.kFieldSmallint, uparams.kNotArray, false, None)
            if self.currentValue < self.minValue:
                self.minValue = self.currentValue
                self.slider.minValue = self.minValue
            if self.currentValue > self.maxValue:
                self.maxValue = self.currentValue
                self.slider.maxValue = self.maxValue
        else:
            self.currentValue = 0
    
    def updateDisplay(self):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldSmallint):
            self.slider.currentValue = self.currentValue
        else:
            self.slider.currentValue = 0
            self.slider.Enabled = false
    
    def sliderMouseDown(self, Sender):
        if self.plant == None:
            return
        self.selectedItemIndex = kItemSlider
        self.slider.hasUnofficialFocus = true
        self.currentValueWhileSliding = self.slider.currentValue
        self.Invalidate()
        if not self.Focused():
            self.SetFocus()
    
    def sliderMouseMove(self, Sender):
        if self.plant == None:
            return
        self.currentValueWhileSliding = self.slider.currentValue
        self.Invalidate()
    
    def sliderMouseUp(self, Sender):
        if self.plant != None:
            self.currentValue = self.slider.currentValue
            umain.MainForm.doCommand(updcom.PdChangeSmallintValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValue, self.param.fieldNumber, uparams.kNotArray, self.param.regrow))
            self.updateDisplay()
            self.Invalidate()
        else:
            self.slider.currentValue = 0
            self.slider.Enabled = false
    
    def sliderKeyDown(self, sender):
        self.sliderMouseUp(sender)
    
    def maxWidth(self):
        result = 0
        result = uppanel.kLeftRightGap * 2 + umath.intMax(self.labelWidth, self.minScaleWidthWithBounds())
        return result
    
    def minWidth(self, requestedWidth):
        result = 0
        widthForLongestWord = 0
        widthWithBounds = 0
        widthWithoutBounds = 0
        
        widthForLongestWord = uppanel.kLeftRightGap * 2 + self.longestLabelWordWidth
        widthWithBounds = self.minScaleWidthWithBounds()
        widthWithoutBounds = self.minScaleWidthWithoutBounds()
        result = -1
        if requestedWidth < widthForLongestWord:
            result = widthForLongestWord
        if requestedWidth < widthWithBounds:
            self.drawWithoutBounds = true
            if requestedWidth < widthWithoutBounds:
                result = umath.intMax(result, widthWithoutBounds)
        else:
            self.drawWithoutBounds = false
        return result
    
    def minScaleWidthWithBounds(self):
        result = 0
        minString = ""
        valueString = ""
        unitString = ""
        maxString = ""
        
        minString = IntToStr(self.minValue)
        valueString = IntToStr(self.currentValue) + "  "
        unitString = uunits.UnitStringForEnum(self.param.unitSet, self.unitIndex)
        maxString = IntToStr(self.maxValue)
        result = self.formTextWidth(minString + valueString + unitString + maxString) + udebug.kBetweenGap * 3
        return result
    
    def minScaleWidthWithoutBounds(self):
        result = 0
        valueString = ""
        unitString = ""
        
        valueString = IntToStr(self.currentValue) + "  "
        unitString = uunits.UnitStringForEnum(self.param.unitSet, self.unitIndex)
        result = self.formTextWidth(valueString + unitString) + udebug.kBetweenGap
        return result
    
    def uncollapsedHeight(self):
        result = 0
        result = self.collapsedHeight() + self.textHeight + uppanel.kTopBottomGap
        return result
    
    def resizeElements(self):
        self.paint()
        self.slider.Left = self.minTextRect.Right + uppanel.kSliderSpaceGap
        self.slider.Top = self.collapsedHeight() + self.textHeight / 2 - self.slider.Height / 2
        self.slider.Width = umath.intMax(0, self.maxTextRect.Left - self.minTextRect.Right - uppanel.kSliderSpaceGap * 2)
    
    def maxSelectedItemIndex(self):
        result = 0
        if (not self.param.collapsed) and (self.slider.Enabled):
            result = kItemSlider
        else:
            result = uppanel.kItemLabel
        return result
    
    def paint(self):
        Rect = TRect()
        minString = ""
        valueString = ""
        maxString = ""
        unitString = ""
        
        if delphi_compatability.Application.terminated:
            return
        if (self.selectedItemIndex == kItemSlider):
            # ask slider to update itself based on whether it is selected 
            self.slider.hasUnofficialFocus = true
        else:
            self.slider.hasUnofficialFocus = false
        PdParameterPanel.paint(self)
        self.slider.Visible = not self.param.collapsed
        if (self.param.collapsed):
            self.drawExtraValueCaptionWithString(IntToStr(self.currentValue), uunits.UnitStringForEnum(self.param.unitSet, self.unitIndex))
            return
        Rect = self.GetClientRect()
        minString = IntToStr(self.minValue)
        if self.slider.dragging:
            valueString = IntToStr(self.currentValueWhileSliding)
        else:
            valueString = IntToStr(self.currentValue)
        unitString = uunits.UnitStringForEnum(self.param.unitSet, self.unitIndex)
        maxString = IntToStr(self.maxValue)
        self.valueTextRect.Left = uppanel.kLeftRightGap
        self.valueTextRect.Right = self.valueTextRect.Left + self.Canvas.TextWidth(valueString)
        self.valueTextRect.Top = self.collapsedHeight() + 1
        self.valueTextRect.Bottom = self.valueTextRect.Top + self.textHeight
        self.unitTextRect = self.valueTextRect
        self.unitTextRect.Left = self.valueTextRect.Right + 5
        self.unitTextRect.Right = self.unitTextRect.Left + self.Canvas.TextWidth(unitString)
        self.minTextRect = self.valueTextRect
        self.minTextRect.Left = self.unitTextRect.Right + 5
        self.minTextRect.Right = self.minTextRect.Left + self.Canvas.TextWidth(minString)
        self.maxTextRect = self.valueTextRect
        self.maxTextRect.Right = Rect.right - uppanel.kLeftRightGap
        self.maxTextRect.Left = self.maxTextRect.Right - self.Canvas.TextWidth(maxString)
        self.drawText(minString, self.minTextRect, false, false, true)
        self.drawText(valueString, self.valueTextRect, not self.readOnly, (self.selectedItemIndex == kItemValueText), false)
        self.drawText(unitString, self.unitTextRect, false, false, false)
        self.drawText(maxString, self.maxTextRect, false, false, true)
    
