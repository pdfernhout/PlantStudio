# unit upp_rea

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
kItemSlider = 1
kItemValueText = 2
kItemUnitText = 3

class PdRealParameterPanel(PdParameterPanel):
    def __init__(self):
        self.currentValue = 0.0
        self.currentValueWhileSliding = 0.0
        self.minValue = 0.0
        self.maxValue = 0.0
        self.slider = KfSlider()
        self.currentUnitIndex = 0
        self.valueTextRect = TRect()
        self.unitTextRect = TRect()
        self.minTextRect = TRect()
        self.maxTextRect = TRect()
        self.drawWithoutBounds = false
        self.arrayIndex = 0
    
    def initialize(self):
        #assuming slider will be deleted automatically by owner - self - otherwise would have destructor
        self.slider = usliders.KfSlider().create(self)
        self.slider.Parent = self
        self.slider.FOnMouseDown = self.sliderMouseDown
        self.slider.FOnMouseMove = self.sliderMouseMove
        self.slider.FOnMouseUp = self.sliderMouseUp
        self.slider.FOnKeyDown = self.sliderKeyDown
        # make it a percentage move 
        self.slider.maxValue = 100
        self.slider.minValue = 0
        self.slider.readOnly = self.param.readOnly
        self.slider.useDefaultSizeAndDraggerSize()
        self.arrayIndex = uparams.kNotArray
        if udomain.domain.options.useMetricUnits:
            self.currentUnitIndex = self.param.unitMetric
        else:
            self.currentUnitIndex = self.param.unitEnglish
        self.minValue = self.param.lowerBound()
        self.maxValue = self.param.upperBound()
    
    def adjustValue(self):
        newString = ansistring()
        oldValueInCurrentUnit = 0.0
        newValue = 0.0
        newValueInPlantUnit = 0.0
        oldString = ""
        prompt = ""
        nameString = ""
        unitString = ""
        minString = ""
        maxString = ""
        outOfRange = false
        
        oldValueInCurrentUnit = self.toCurrentUnit(self.currentValue)
        newString = usupport.digitValueString(oldValueInCurrentUnit)
        oldString = newString
        nameString = UNRESOLVED.copy(self.Caption, 1, 30)
        if len(nameString) == 30:
            nameString = nameString + "..."
        unitString = uunits.UnitStringForEnum(self.param.unitSet, self.currentUnitIndex)
        minString = usupport.digitValueString(self.toCurrentUnit(self.minValue))
        maxString = usupport.digitValueString(self.toCurrentUnit(self.maxValue))
        prompt = "Type a new value."
        if InputQuery("Enter value", prompt, newString):
            if (newString != oldString) and (usupport.boundForString(newString, self.param.fieldType, newValue)):
                newValueInPlantUnit = self.toPlantUnit(newValue)
                outOfRange = self.checkValueAgainstBounds(newValueInPlantUnit)
                if not outOfRange:
                    self.currentValue = newValueInPlantUnit
                    umain.MainForm.doCommand(updcom.PdChangeRealValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValue, self.param.fieldNumber, self.arrayIndex, self.param.regrow))
                    self.updateDisplay()
                    self.Invalidate()
    
    def toPlantUnit(self, value):
        result = 0.0
        result = uunits.Convert(self.param.unitSet, self.currentUnitIndex, self.param.unitModel, value)
        return result
    
    def toCurrentUnit(self, value):
        result = 0.0
        result = uunits.Convert(self.param.unitSet, self.param.unitModel, self.currentUnitIndex, value)
        return result
    
    def checkValueAgainstBounds(self, aValue):
        result = false
        result = (aValue < self.minValue) or (aValue > self.maxValue)
        return result
    
    def selectNextUnitInSet(self, shift, ctrl):
        if shift:
            self.currentUnitIndex = uunits.GetPreviousUnitEnumInUnitSet(self.param.unitSet, self.currentUnitIndex)
        else:
            self.currentUnitIndex = uunits.GetNextUnitEnumInUnitSet(self.param.unitSet, self.currentUnitIndex)
        self.updateCurrentValue(-1)
        self.updateDisplay()
        self.Invalidate()
    
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
        elif delphi_compatability.PtInRect(self.unitTextRect, thePoint):
            self.selectedItemIndex = kItemUnitText
            self.Invalidate()
            self.selectNextUnitInSet(delphi_compatability.TShiftStateEnum.ssShift in Shift, delphi_compatability.TShiftStateEnum.ssCtrl in Shift)
    
    def doKeyDown(self, sender, key, shift):
        if self.slider.Enabled and not self.slider.readOnly:
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
        PdParameterPanel.doKeyDown(self, sender, key, shift)
        if (key == delphi_compatability.VK_RETURN):
            if self.selectedItemIndex == kItemSlider:
                if self.slider.Enabled and not self.slider.readOnly:
                    key = self.slider.doKeyDown(sender, key, shift)
            elif self.selectedItemIndex == kItemValueText:
                if self.slider.Enabled and not self.slider.readOnly:
                    self.adjustValue()
            elif self.selectedItemIndex == kItemUnitText:
                self.selectNextUnitInSet(delphi_compatability.TShiftStateEnum.ssShift in shift, delphi_compatability.TShiftStateEnum.ssCtrl in shift)
        return key
    
    def sliderPositionFromValue(self, value):
        result = 0
        if self.maxValue - self.minValue == 0.0:
            result = 0
        elif value <= self.minValue:
            result = 0
        elif value >= self.maxValue:
            result = 100
        else:
            result = intround(100.0 * (value - self.minValue) / (self.maxValue - self.minValue))
        return result
    
    def valueFromSliderPosition(self):
        result = 0.0
        sliderPosition = 0.0
        
        sliderPosition = self.slider.currentValue
        result = self.minValue + sliderPosition / 100.0 * (self.maxValue - self.minValue)
        return result
    
    def updateEnabling(self):
        PdParameterPanel.updateEnabling(self)
        self.slider.Enabled = self.plant != None
        self.slider.readOnly = self.readOnly
    
    def updatePlantValues(self):
        oldValue = 0.0
        
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
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldFloat):
            self.currentValue = self.plant.transferField(umath.kGetField, self.currentValue, self.param.fieldNumber, uparams.kFieldFloat, self.arrayIndex, false, None)
            if self.currentValue < self.minValue:
                self.currentValue = self.minValue
            if self.currentValue > self.maxValue:
                self.currentValue = self.maxValue
        else:
            self.currentValue = 0.0
    
    def updateDisplay(self):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldFloat):
            self.slider.currentValue = self.sliderPositionFromValue(self.currentValue)
        else:
            self.slider.currentValue = 0
            self.slider.Enabled = false
    
    def sliderMouseDown(self, Sender):
        if self.plant == None:
            return
        self.selectedItemIndex = kItemSlider
        self.slider.hasUnofficialFocus = true
        self.currentValueWhileSliding = self.valueFromSliderPosition()
        self.Invalidate()
        if not self.Focused():
            self.SetFocus()
    
    def sliderMouseMove(self, Sender):
        if self.plant == None:
            return
        self.currentValueWhileSliding = self.valueFromSliderPosition()
        self.Invalidate()
    
    def sliderMouseUp(self, Sender):
        if self.plant == None:
            return
        self.currentValue = self.valueFromSliderPosition()
        umain.MainForm.doCommand(updcom.PdChangeRealValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValue, self.param.fieldNumber, self.arrayIndex, self.param.regrow))
        self.Invalidate()
    
    def sliderKeyDown(self, Sender):
        self.sliderMouseUp(Sender)
    
    def maxWidth(self):
        result = 0
        result = umath.intMax(uppanel.kLeftRightGap * 2 + self.labelWidth, self.minScaleWidthWithBounds(self.param.unitSet, self.param.unitModel, self.minValue, self.maxValue))
        return result
    
    def minWidth(self, requestedWidth):
        result = 0
        widthForLongestWord = 0
        widthWithBounds = 0
        widthWithoutBounds = 0
        
        # 1. test if width given is less than labelWidth.
        #       if not, move on
        #       if so, test if width given is less than width of longest full word in labelWidth.
        #         if not, move on
        #         if so, give back width of longest full word in labelWidth as minWidth.
        #    2. test if width given is less than minScaleWidthWithBounds.
        #       if not, move on (set flag to draw bounds)
        #       if so, test if width given is less than minScaleWidthWithoutBounds.
        #         if not, move on (set flag to not draw bounds)
        #         if so, give back minScaleWidthWithoutBounds as minWidth.
        #  
        widthForLongestWord = uppanel.kLeftRightGap * 2 + self.longestLabelWordWidth
        widthWithBounds = self.minScaleWidthWithBounds(self.param.unitSet, self.param.unitModel, self.minValue, self.maxValue)
        widthWithoutBounds = self.minScaleWidthWithoutBounds(self.param.unitSet, self.param.unitModel)
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
        if (not self.param.collapsed) and (self.plant != None):
            result = kItemUnitText
        else:
            result = uppanel.kItemLabel
        return result
    
    def nextSelectedItemIndex(self, goForward):
        result = 0
        result = uppanel.kItemNone
        if self.selectedItemIndex == uppanel.kItemNone:
            result = self.selectedItemIndex
        elif self.selectedItemIndex == uppanel.kItemLabel:
            if goForward:
                result = kItemValueText
            else:
                result = uppanel.kItemNone
        elif self.selectedItemIndex == kItemSlider:
            if goForward:
                result = uppanel.kItemNone
            else:
                result = kItemUnitText
        elif self.selectedItemIndex == kItemValueText:
            if goForward:
                result = kItemUnitText
            else:
                result = uppanel.kItemLabel
        elif self.selectedItemIndex == kItemUnitText:
            if goForward:
                result = kItemSlider
            else:
                result = kItemValueText
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
            self.drawExtraValueCaptionWithString(usupport.digitValueString(self.toCurrentUnit(self.currentValue)), uunits.UnitStringForEnum(self.param.unitSet, self.currentUnitIndex))
            return
        Rect = self.GetClientRect()
        minString = usupport.digitValueString(self.toCurrentUnit(self.minValue))
        maxString = usupport.digitValueString(self.toCurrentUnit(self.maxValue))
        if self.slider.dragging:
            valueString = usupport.digitValueString(self.toCurrentUnit(self.currentValueWhileSliding))
        else:
            valueString = usupport.digitValueString(self.toCurrentUnit(self.currentValue))
        unitString = uunits.UnitStringForEnum(self.param.unitSet, self.currentUnitIndex)
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
        self.drawText(unitString, self.unitTextRect, true, (self.selectedItemIndex == kItemUnitText), false)
        self.drawText(maxString, self.maxTextRect, false, false, true)
    
