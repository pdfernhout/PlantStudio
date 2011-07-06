# unit upp_lis

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
kItemFirstChoice = 1
kMaxNumChoices = 20

class PdListParameterPanel(PdParameterPanel):
    def __init__(self):
        self.hasRadioButtons = false
        self.currentChoice = 0
        self.choiceStrings = TStringList()
        self.choiceRects = [0] * (range(0, kMaxNumChoices + 1) + 1)
        self.choiceChecks = [0] * (range(0, kMaxNumChoices + 1) + 1)
        self.editEnabled = false
    
    def initialize(self):
        self.currentChoice = 0
        self.editEnabled = false
        self.choiceStrings = delphi_compatability.TStringList.create
        self.hasRadioButtons = uplant.PdPlant.fillEnumStringList(self.choiceStrings, self.param.fieldNumber, self.hasRadioButtons)
    
    def destroy(self):
        self.choiceStrings.free
        self.choiceStrings = None
        PdParameterPanel.destroy(self)
    
    def updateEnabling(self):
        PdParameterPanel.updateEnabling(self)
        self.editEnabled = not ((self.plant == None) or (self.readOnly))
    
    def updatePlantValues(self):
        oldChoice = 0
        
        if self.plant == None:
            return
        if self.param.collapsed:
            return
        oldChoice = self.currentChoice
        self.updateCurrentValue(-1)
        if not self.hasRadioButtons or (oldChoice != self.currentChoice):
            self.updateDisplay()
            self.Invalidate()
    
    def updateCurrentValue(self, aFieldIndex):
        i = 0
        
        if (self.plant == None) or (self.param.fieldType != uparams.kFieldEnumeratedList):
            self.currentChoice = 0
            self.clearChecks()
            self.editEnabled = false
        else:
            if self.hasRadioButtons:
                self.currentChoice = self.plant.transferField(umath.kGetField, self.currentChoice, self.param.fieldNumber, uparams.kFieldSmallint, uparams.kNotArray, false, None)
            elif self.choiceStrings.Count > 0:
                for i in range(0, self.choiceStrings.Count):
                    self.choiceChecks[i] = self.plant.transferField(umath.kGetField, self.choiceChecks[i], self.param.fieldNumber, uparams.kFieldBoolean, i, false, None)
    
    def updateDisplay(self):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldEnumeratedList):
            self.Invalidate()
        else:
            self.editEnabled = false
    
    def clearChecks(self):
        i = 0
        
        for i in range(0, kMaxNumChoices + 1):
            self.choiceChecks[i] = false
    
    def doMouseUp(self, Sender, Button, Shift, X, Y):
        i = 0
        thePoint = TPoint()
        
        # must always call this first because it sets the focus 
        PdParameterPanel.doMouseUp(self, Sender, Button, Shift, X, Y)
        if (self.editEnabled):
            thePoint = Point(X, Y)
            if self.choiceStrings.Count > 0:
                for i in range(0, self.choiceStrings.Count):
                    if delphi_compatability.PtInRect(self.choiceRects[i], thePoint):
                        self.setNewValue(i)
                        self.selectedItemIndex = kItemFirstChoice + self.currentChoice
                        break
            self.Invalidate()
    
    def doKeyDown(self, sender, key, shift):
        PdParameterPanel.doKeyDown(self, sender, key, shift)
        if (self.editEnabled) and (key == delphi_compatability.VK_RETURN) and (self.selectedItemIndex >= kItemFirstChoice):
            self.setNewValue(self.selectedItemIndex - kItemFirstChoice)
            self.Invalidate()
        return key
    
    def setNewValue(self, index):
        if self.hasRadioButtons:
            self.currentChoice = index
            umain.MainForm.doCommand(updcom.PdChangeSmallintValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentChoice, self.param.fieldNumber, uparams.kNotArray, self.param.regrow))
        else:
            self.choiceChecks[index] = not self.choiceChecks[index]
            umain.MainForm.doCommand(updcom.PdChangeBooleanValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.choiceChecks[index], self.param.fieldNumber, index, self.param.regrow))
    
    def firstCheckedString(self):
        result = ""
        i = 0
        
        result = ""
        if self.choiceStrings.Count > 0:
            for i in range(0, self.choiceStrings.Count):
                if self.hasRadioButtons:
                    if self.currentChoice == i:
                        result = self.choiceStrings.Strings[i]
                        return result
                else:
                    if self.choiceChecks[i]:
                        result = self.choiceStrings.Strings[i]
                        return result
        return result
    
    def maxWidth(self):
        result = 0
        i = 0
        maxWidth = 0
        
        result = 0
        for i in range(0, self.choiceStrings.Count):
            result = umath.intMax(maxWidth, umain.TMainForm(self.Owner).Canvas.TextWidth(self.choiceStrings.Strings[i]))
        result = umath.intMax(uppanel.kLeftRightGap * 2 + self.labelWidth, +uppanel.kRadioButtonLeftGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap + maxWidth + uppanel.kLeftRightGap)
        return result
    
    def minWidth(self, requestedWidth):
        result = 0
        i = 0
        longestWidth = 0
        minAllowed = 0
        
        longestWidth = 0
        for i in range(0, self.choiceStrings.Count):
            longestWidth = umath.intMax(longestWidth, umain.TMainForm(self.Owner).Canvas.TextWidth(self.choiceStrings.Strings[i]))
        minAllowed = umath.intMax(uppanel.kLeftRightGap * 2 + self.longestLabelWordWidth, +uppanel.kRadioButtonLeftGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap + longestWidth + uppanel.kLeftRightGap)
        if requestedWidth > minAllowed:
            result = -1
        else:
            result = minAllowed
        return result
    
    def uncollapsedHeight(self):
        result = 0
        result = self.collapsedHeight() + self.textHeight * self.choiceStrings.Count + uppanel.kTopBottomGap
        return result
    
    def maxSelectedItemIndex(self):
        result = 0
        if (not self.param.collapsed) and (self.editEnabled):
            result = kItemFirstChoice + self.choiceStrings.Count - 1
        else:
            result = uppanel.kItemLabel
        return result
    
    def resizeElements(self):
        pass
        # do nothing 
    
    def paint(self):
        i = 0
        rect = TRect()
        circleRects = [0] * (range(0, kMaxNumChoices + 1) + 1)
        textRects = [0] * (range(0, kMaxNumChoices + 1) + 1)
        
        if delphi_compatability.Application.terminated:
            return
        PdParameterPanel.paint(self)
        if (self.param.collapsed):
            self.drawExtraValueCaptionWithString(self.firstCheckedString(), "")
            return
        Rect = self.GetClientRect()
        if self.choiceStrings.Count > 0:
            for i in range(0, self.choiceStrings.Count):
                circleRects[i].Left = Rect.left + uppanel.kRadioButtonLeftGap
                circleRects[i].Right = circleRects[i].Left + uppanel.kRadioButtonWidth
                circleRects[i].Top = Rect.top + self.collapsedHeight() + self.textHeight * i + (self.textHeight / 2 - uppanel.kRadioButtonWidth / 2)
                circleRects[i].Bottom = circleRects[i].Top + uppanel.kRadioButtonWidth
                textRects[i].Left = Rect.left + uppanel.kRadioButtonLeftGap + uppanel.kRadioButtonWidth + uppanel.kRadioButtonBeforeTextGap
                textRects[i].Right = textRects[i].Left + self.Canvas.TextWidth(self.choiceStrings.Strings[i])
                textRects[i].Top = Rect.top + self.collapsedHeight() + self.textHeight * i
                textRects[i].Bottom = textRects[i].Top + self.textHeight
                if self.hasRadioButtons:
                    self.drawRadioButton((self.currentChoice == i), self.editEnabled, circleRects[i])
                else:
                    self.drawCheckBox(self.choiceChecks[i], self.editEnabled, circleRects[i])
                self.drawText(self.choiceStrings.Strings[i], textRects[i], true, (self.selectedItemIndex == kItemFirstChoice + i) and (self.editEnabled), false)
                delphi_compatability.UnionRect(self.choiceRects[i], circleRects[i], textRects[i])
    
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
        if enabled:
            self.Canvas.Pen.Color = UNRESOLVED.clBtnText
        else:
            self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
        # FIX unresolved WITH expression: Rect
        self.Canvas.Ellipse(self.Left, self.Top, UNRESOLVED.right, UNRESOLVED.bottom)
        self.Canvas.Brush.Color = brushColor
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
    
    def drawCheckBox(self, value, enabled, rect):
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        if enabled:
            self.Canvas.Pen.Color = UNRESOLVED.clBtnText
        else:
            self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
        # FIX unresolved WITH expression: Rect
        self.Canvas.Rectangle(self.Left, self.Top, UNRESOLVED.right, UNRESOLVED.bottom)
        if value:
            # FIX unresolved WITH expression: Rect
            self.Canvas.MoveTo(self.Left, self.Top)
            self.Canvas.LineTo(UNRESOLVED.right, UNRESOLVED.bottom)
            self.Canvas.MoveTo(self.Left, UNRESOLVED.bottom)
            self.Canvas.LineTo(UNRESOLVED.right, self.Top)
    
