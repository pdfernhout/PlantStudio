# unit upp_scv

from conversion_common import *
import usliders
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
kItemPoint1 = 1
kItemPoint2 = 2
kItemX1 = 3
kItemY1 = 4
kItemX2 = 5
kItemY2 = 6
kItemSCurveUnitText = 7

# var
gRecursing = false

class PdSCurveParameterPanel(PdParameterPanel):
    def __init__(self):
        self.editEnabled = false
        self.draggingPoint = false
        self.currentValues = [0] * (range(0, 3 + 1) + 1)
        self.minXValue = 0.0
        self.maxXValue = 0.0
        self.belowZero = false
        self.currentUnitIndex = 0
        self.graphRect = TRect()
        self.pointRects = [0] * (range(0, 1 + 1) + 1)
        self.valueRects = [0] * (range(0, 3 + 1) + 1)
        self.unitTextRect = TRect()
    
    # ----------------------------------------------------------------------------- initialize 
    def initialize(self):
        temp = 0.0
        
        self.OnMouseDown = self.doMouseDown
        self.OnMouseMove = self.doMouseMove
        self.OnMouseUp = self.doMouseUp
        self.OnKeyDown = self.doKeyDown
        self.draggingPoint = false
        self.currentUnitIndex = 0
        if udomain.domain.options.useMetricUnits:
            self.currentUnitIndex = self.param.unitMetric
        else:
            self.currentUnitIndex = self.param.unitEnglish
        self.minXValue = self.param.lowerBound()
        self.maxXValue = self.param.upperBound()
        self.belowZero = false
        if (self.minXValue < 0.0):
            temp = abs(self.maxXValue)
            self.maxXValue = abs(self.minXValue)
            self.minXValue = temp
            self.belowZero = true
    
    # ------------------------------------------------------------------------ mouse and key 
    def doMouseDown(self, sender, Button, Shift, X, Y):
        thePoint = TPoint()
        i = 0
        
        # must always call this first because it sets the focus 
        PdParameterPanel.doMouseDown(self, sender, Button, Shift, X, Y)
        if not self.editEnabled:
            return
        thePoint = Point(X, Y)
        for i in range(0, 1 + 1):
            if delphi_compatability.PtInRect(self.pointRects[i], thePoint):
                self.selectedItemIndex = kItemPoint1 + i
                self.draggingPoint = true
                # should be only point rect 
                self.Invalidate()
        if not self.Focused():
            self.SetFocus()
    
    def doMouseMove(self, sender, Shift, X, Y):
        i = 0
        index = 0
        saveValues = [0] * (range(0, 3 + 1) + 1)
        failed = false
        points = [0] * (range(0, 1 + 1) + 1)
        
        if not self.draggingPoint:
            return
        if not self.editEnabled:
            return
        for i in range(0, 3 + 1):
            saveValues[i] = self.currentValues[i]
        index = self.selectedItemIndex - kItemPoint1
        # do nothing - to prevent repetitive messages if problem 
        try:
            points[index] = Point(X, Y)
            if index == 0:
                # set other point 
                points[1] = self.pointFromXY(self.currentValues[2], self.currentValues[3])
            else:
                points[0] = self.pointFromXY(self.currentValues[0], self.currentValues[1])
            self.keepPointInGraphRect(points[index])
            self.keepPointsFromCrossing(points[0], points[1], index)
            self.currentValues[index * 2] = self.xValueFromPointPosition(points[index])
            self.currentValues[index * 2 + 1] = self.yValueFromPointPosition(points[index])
            failed = self.drawSCurve(false, failed)
            if failed:
                for i in range(0, 3 + 1):
                    self.currentValues[i] = saveValues[i]
            # whole 
            self.Invalidate()
        except:
            pass
    
    def doMouseUp(self, Sender, Button, Shift, X, Y):
        thePoint = TPoint()
        i = 0
        
        # must always call this first because it sets the focus 
        PdParameterPanel.doMouseUp(self, Sender, Button, Shift, X, Y)
        thePoint = Point(X, Y)
        for i in range(0, 1 + 1):
            if (delphi_compatability.PtInRect(self.pointRects[i], thePoint)) and (self.editEnabled):
                if self.draggingPoint:
                    self.draggingPoint = false
                    self.setPointAfterMouseUp(i, X, Y)
                    self.Invalidate()
                    return
        if self.draggingPoint:
            self.draggingPoint = false
        for i in range(0, 3 + 1):
            if (delphi_compatability.PtInRect(self.valueRects[i], thePoint)) and (self.editEnabled):
                self.selectedItemIndex = i + kItemX1
                self.Invalidate()
                if delphi_compatability.TShiftStateEnum.ssShift in Shift:
                    self.adjustAllValuesAtOnce()
                else:
                    self.adjustValue()
                return
        if delphi_compatability.PtInRect(self.unitTextRect, thePoint):
            # can still do this if disabled 
            self.selectedItemIndex = kItemSCurveUnitText
            self.Invalidate()
            self.selectNextUnitInSet(delphi_compatability.TShiftStateEnum.ssShift in Shift)
    
    def doKeyDown(self, sender, key, shift):
        increment = 0
        index = 0
        
        PdParameterPanel.doKeyDown(self, sender, key, shift)
        increment = 2
        if key == delphi_compatability.VK_RETURN:
            if self.selectedItemIndex == kItemX1:
                if delphi_compatability.TShiftStateEnum.ssShift in shift:
                    self.adjustAllValuesAtOnce()
                else:
                    self.adjustValue()
            elif self.selectedItemIndex == kItemY1:
                if delphi_compatability.TShiftStateEnum.ssShift in shift:
                    self.adjustAllValuesAtOnce()
                else:
                    self.adjustValue()
            elif self.selectedItemIndex == kItemX2:
                if delphi_compatability.TShiftStateEnum.ssShift in shift:
                    self.adjustAllValuesAtOnce()
                else:
                    self.adjustValue()
            elif self.selectedItemIndex == kItemY2:
                if delphi_compatability.TShiftStateEnum.ssShift in shift:
                    self.adjustAllValuesAtOnce()
                else:
                    self.adjustValue()
            elif self.selectedItemIndex == kItemSCurveUnitText:
                self.selectNextUnitInSet(delphi_compatability.TShiftStateEnum.ssShift in shift)
        elif (self.selectedItemIndex == kItemPoint1) or (self.selectedItemIndex == kItemPoint2):
            index = self.selectedItemIndex - kItemPoint1
            if key == delphi_compatability.VK_LEFT:
                self.adjustValueByPixels(index, -increment, 0)
            elif key == delphi_compatability.VK_RIGHT:
                self.adjustValueByPixels(index, increment, 0)
            elif key == delphi_compatability.VK_DOWN:
                self.adjustValueByPixels(index, 0, increment)
            elif key == delphi_compatability.VK_UP:
                self.adjustValueByPixels(index, 0, -increment)
        return key
    
    # --------------------------------------------------------- functions called by mouse and key 
    def adjustValue(self):
        newString = ansistring()
        oldString = ""
        nameString = ""
        prompt = ""
        currentUnitString = ""
        newValue = 0.0
        oldValue = 0.0
        valueInCurrentUnit = 0.0
        index = 0
        failed = false
        points = [0] * (range(0, 1 + 1) + 1)
        
        if self.selectedItemIndex < kItemX1:
            return
        index = self.selectedItemIndex - kItemX1
        oldValue = self.currentValues[index]
        nameString = UNRESOLVED.copy(self.Caption, 1, 30)
        currentUnitString = uunits.UnitStringForEnum(self.param.unitSet, self.currentUnitIndex)
        if len(nameString) == 30:
            nameString = nameString + "..."
        if not odd(index):
            # x 
            valueInCurrentUnit = self.toCurrentUnit(self.currentValues[index])
            newString = usupport.digitValueString(valueInCurrentUnit)
            # y 
            # don't convert y value - is always 0-1 
        else:
            valueInCurrentUnit = self.currentValues[index]
            newString = FloatToStrF(valueInCurrentUnit, UNRESOLVED.ffFixed, 7, 2)
        oldString = newString
        prompt = "Type a new value."
        if InputQuery("Enter value", prompt, newString):
            if (newString != oldString) and (usupport.boundForString(newString, self.param.fieldType, newValue)):
                if not odd(index):
                    self.currentValues[index] = self.toPlantUnit(newValue)
                else:
                    self.currentValues[index] = newValue
                points[0] = self.pointFromXY(self.currentValues[0], self.currentValues[1])
                points[1] = self.pointFromXY(self.currentValues[2], self.currentValues[3])
                self.keepPointInGraphRect(points[(index - 1) / 2])
                self.keepPointsFromCrossing(points[0], points[1], (index - 1) / 2)
                failed = self.drawSCurve(false, failed)
                if failed:
                    self.currentValues[index] = oldValue
                    ShowMessage("Invalid value.")
                else:
                    # don't create change point command here, because only one float is changed 
                    umain.MainForm.doCommand(updcom.PdChangeRealValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValues[index], self.param.fieldNumber, index, self.param.regrow))
                    self.Invalidate()
    
    def adjustAllValuesAtOnce(self):
        newString = ansistring()
        oldString = ""
        prompt = ""
        i = 0
        failed = false
        points = [0] * (range(0, 1 + 1) + 1)
        oldValues = SCurveStructure()
        valuesInCurrentUnit = SCurveStructure()
        newValues = SCurveStructure()
        
        if self.selectedItemIndex < kItemX1:
            return
        oldValues.x1 = self.currentValues[0]
        oldValues.y1 = self.currentValues[1]
        oldValues.x2 = self.currentValues[2]
        oldValues.y2 = self.currentValues[3]
        valuesInCurrentUnit = oldValues
        valuesInCurrentUnit.x1 = self.toCurrentUnit(oldValues.x1)
        valuesInCurrentUnit.x2 = self.toCurrentUnit(oldValues.x2)
        newString = usupport.digitValueString(valuesInCurrentUnit.x1) + " " + usupport.digitValueString(valuesInCurrentUnit.y1) + " " + usupport.digitValueString(valuesInCurrentUnit.x2) + " " + usupport.digitValueString(valuesInCurrentUnit.y2)
        oldString = newString
        prompt = "Edit these four s curve values."
        if InputQuery("Enter value", prompt, newString):
            if (newString != oldString):
                try:
                    newValues = umath.stringToSCurve(newString)
                    self.currentValues[0] = newValues.x1
                    self.currentValues[1] = newValues.y1
                    self.currentValues[2] = newValues.x2
                    self.currentValues[3] = newValues.y2
                except:
                    failed = true
                if not failed:
                    points[0] = self.pointFromXY(self.currentValues[0], self.currentValues[1])
                    points[1] = self.pointFromXY(self.currentValues[2], self.currentValues[3])
                    for i in range(0, 1 + 1):
                        self.keepPointInGraphRect(points[i])
                        self.keepPointsFromCrossing(points[0], points[1], 1)
                    failed = self.drawSCurve(false, failed)
                if failed:
                    self.currentValues[0] = oldValues.x1
                    self.currentValues[1] = oldValues.y1
                    self.currentValues[2] = oldValues.x2
                    self.currentValues[3] = oldValues.y2
                    ShowMessage("Invalid value.")
                else:
                    # don't create change point command here, because only one float is changed 
                    umain.MainForm.doCommand(updcom.PdChangeSCurvePointValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValues[0], self.currentValues[1], self.param.fieldNumber, 0, self.param.regrow))
                    umain.MainForm.doCommand(updcom.PdChangeSCurvePointValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValues[2], self.currentValues[3], self.param.fieldNumber, 1, self.param.regrow))
                    self.Invalidate()
    
    def adjustValueByPixels(self, index, xChange, yChange):
        points = [0] * (range(0, 1 + 1) + 1)
        oldX = 0.0
        oldY = 0.0
        failed = false
        xIndex = 0
        yIndex = 0
        
        xIndex = index * 2
        yIndex = index * 2 + 1
        oldX = self.currentValues[xIndex]
        oldY = self.currentValues[yIndex]
        points[0] = self.pointFromXY(self.currentValues[0], self.currentValues[1])
        points[1] = self.pointFromXY(self.currentValues[2], self.currentValues[3])
        points[index].X = points[index].X + xChange
        points[index].Y = points[index].Y + yChange
        self.keepPointInGraphRect(points[index])
        self.keepPointsFromCrossing(points[0], points[1], index)
        failed = self.drawSCurve(false, failed)
        if failed:
            self.currentValues[xIndex] = oldX
            self.currentValues[yIndex] = oldY
        else:
            self.currentValues[xIndex] = self.xValueFromPointPosition(points[index])
            self.currentValues[yIndex] = self.yValueFromPointPosition(points[index])
            umain.MainForm.doCommand(updcom.PdChangeSCurvePointValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValues[xIndex], self.currentValues[yIndex], self.param.fieldNumber, index, self.param.regrow))
            self.Invalidate()
    
    def selectNextUnitInSet(self, shift):
        if shift:
            # no layer or derivation for this - s curve cannot be layer or absolute/relative 
            self.currentUnitIndex = uunits.GetPreviousUnitEnumInUnitSet(self.param.unitSet, self.currentUnitIndex)
        else:
            self.currentUnitIndex = uunits.GetNextUnitEnumInUnitSet(self.param.unitSet, self.currentUnitIndex)
        self.updateDisplay()
    
    def setPointAfterMouseUp(self, index, x, y):
        xIndex = 0
        yIndex = 0
        thePoint = TPoint()
        
        self.selectedItemIndex = kItemPoint1 + index
        thePoint = Point(x, y)
        xIndex = index * 2
        yIndex = index * 2 + 1
        self.currentValues[xIndex] = self.xValueFromPointPosition(thePoint)
        self.currentValues[yIndex] = self.yValueFromPointPosition(thePoint)
        # change x and y values 
        umain.MainForm.doCommand(updcom.PdChangeSCurvePointValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentValues[xIndex], self.currentValues[yIndex], self.param.fieldNumber, index, self.param.regrow))
    
    def keepPointInGraphRect(self, point):
        if Point.x < self.graphRect.Left:
            Point.x = self.graphRect.Left
        if Point.x > self.graphRect.Right:
            Point.x = self.graphRect.Right
        if Point.y < self.graphRect.Top:
            Point.y = self.graphRect.Top
        if Point.y > self.graphRect.Bottom:
            Point.y = self.graphRect.Bottom
    
    def keepPointsFromCrossing(self, point0, point1, movingPoint):
        closestPoint = TPoint()
        proportion = 0.0
        minDifference = 0.0
        
        proportion = 0.01
        minDifference = (self.maxXValue - self.minXValue) * proportion
        closestPoint = self.pointFromXY(minDifference, 0)
        closestPoint.X = umath.intMax(1, closestPoint.X - self.graphRect.Left)
        if movingPoint == 0:
            if point0.X > point1.X - closestPoint.X:
                point0.X = point1.X - closestPoint.X
        else:
            if point1.X < point0.X + closestPoint.X:
                point1.X = point0.X + closestPoint.X
    
    # ------------------------------------------------------------------------------- updating 
    def updateEnabling(self):
        PdParameterPanel.updateEnabling(self)
        if (self.plant == None) or (self.readOnly):
            self.editEnabled = false
        else:
            self.editEnabled = true
    
    def updatePlantValues(self):
        i = 0
        oldValues = [0] * (range(0, 3 + 1) + 1)
        changed = false
        
        if self.plant == None:
            return
        if self.param.collapsed:
            return
        for i in range(0, 3 + 1):
            oldValues[i] = self.currentValues[i]
        self.updateCurrentValue(-1)
        changed = false
        for i in range(0, 3 + 1):
            if oldValues[i] != self.currentValues[i]:
                changed = true
                break
        if changed:
            self.updateDisplay()
            self.Invalidate()
    
    def updateCurrentValue(self, aFieldIndex):
        i = 0
        
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldFloat):
            if aFieldIndex != -1:
                self.currentValues[aFieldIndex] = self.plant.transferField(umath.kGetField, self.currentValues[aFieldIndex], self.param.fieldNumber, uparams.kFieldFloat, aFieldIndex, false, None)
            else:
                for i in range(0, 3 + 1):
                    self.currentValues[i] = self.plant.transferField(umath.kGetField, self.currentValues[i], self.param.fieldNumber, uparams.kFieldFloat, i, false, None)
            if self.currentValues[0] < self.minXValue:
                self.minXValue = self.currentValues[0]
            if self.currentValues[2] > self.maxXValue:
                self.maxXValue = self.currentValues[2]
        else:
            self.editEnabled = false
    
    def updateDisplay(self):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldFloat):
            self.Invalidate()
        else:
            self.editEnabled = false
    
    # ----------------------------------------------------------------------------------------- painting 
    def paint(self):
        minYTextRect = TRect()
        maxYTextRect = TRect()
        minXTextRect = TRect()
        maxXTextRect = TRect()
        pointTextRect = TRect()
        maxXValueInCurrentUnit = 0.0
        minXValueInCurrentUnit = 0.0
        minXString = ""
        maxXString = ""
        minYString = ""
        maxYString = ""
        currentUnitString = ""
        currentValuesInCurrentUnit = [0] * (range(0, 3 + 1) + 1)
        valueStrings = [0] * (range(0, 3 + 1) + 1)
        i = 0
        xPos = 0
        totalWidth = 0
        thePoint = TPoint()
        failed = false
        
        try:
            if delphi_compatability.Application.terminated:
                return
            PdParameterPanel.paint(self)
            if self.param.collapsed:
                return
            if gRecursing:
                # errorMessage('PdSCurveParameterPanel.Paint: recursion in paint method'); 
                gRecursing = false
                return
            gRecursing = true
            # convert bounds and values from plant to current unit ( don't convert Y value) 
            # this is only for writing strings; use plant unit for drawing points 
            minXValueInCurrentUnit = self.toCurrentUnit(self.minXValue)
            if not self.belowZero:
                maxXValueInCurrentUnit = self.toCurrentUnit(self.maxXValue)
                currentValuesInCurrentUnit[0] = self.toCurrentUnit(self.currentValues[0])
                currentValuesInCurrentUnit[2] = self.toCurrentUnit(self.currentValues[2])
            else:
                maxXValueInCurrentUnit = self.toCurrentUnit(-self.maxXValue)
                currentValuesInCurrentUnit[0] = self.toCurrentUnit(-self.currentValues[0])
                currentValuesInCurrentUnit[2] = self.toCurrentUnit(-self.currentValues[2])
            currentValuesInCurrentUnit[1] = self.currentValues[1]
            currentValuesInCurrentUnit[3] = self.currentValues[3]
            # strings to write for number 
            minXString = usupport.digitValueString(minXValueInCurrentUnit)
            maxXString = usupport.digitValueString(maxXValueInCurrentUnit)
            minYString = "0.0"
            maxYString = "1.0"
            currentUnitString = uunits.UnitStringForEnum(self.param.unitSet, self.currentUnitIndex)
            for i in range(0, 3 + 1):
                if (i == 0) or (i == 2):
                    valueStrings[i] = self.stringForIndex(i) + " " + usupport.digitValueString(currentValuesInCurrentUnit[i])
                else:
                    valueStrings[i] = self.stringForIndex(i) + " " + FloatToStrF(currentValuesInCurrentUnit[i], UNRESOLVED.ffFixed, 7, 2)
            # calculate all rectangles to draw text, points 
            self.graphRect.Left = uppanel.kLeftRightGap + self.Canvas.TextWidth(minYString) + udebug.kBetweenGap
            self.graphRect.Right = self.ClientWidth - uppanel.kLeftRightGap * 2
            self.graphRect.Top = self.collapsedHeight()
            self.graphRect.Bottom = self.Height - self.textHeight * 2 - udebug.kBetweenGap - uppanel.kTopBottomGap * 2
            minXTextRect.Left = self.graphRect.Left
            minXTextRect.Right = minXTextRect.Left + self.Canvas.TextWidth(minXString)
            minXTextRect.Top = self.graphRect.Bottom + 1
            minXTextRect.Bottom = minXTextRect.Top + self.textHeight
            maxXTextRect.Right = self.graphRect.Right
            maxXTextRect.Left = maxXTextRect.Right - self.Canvas.TextWidth(maxXString)
            maxXTextRect.Top = minXTextRect.Top
            maxXTextRect.Bottom = maxXTextRect.Top + self.textHeight
            minYTextRect.Left = self.graphRect.Left - self.Canvas.TextWidth(maxYString) - udebug.kBetweenGap
            minYTextRect.Right = self.graphRect.Left - 1
            minYTextRect.Top = self.graphRect.Bottom - self.textHeight
            minYTextRect.Bottom = self.graphRect.Bottom
            maxYTextRect.Left = self.graphRect.Left - self.Canvas.TextWidth(maxYString) - udebug.kBetweenGap
            maxYTextRect.Right = self.graphRect.Left - 1
            maxYTextRect.Top = self.graphRect.Top
            maxYTextRect.Bottom = maxYTextRect.Top + self.textHeight
            for i in range(0, 1 + 1):
                thePoint = self.pointFromXY(self.currentValues[i * 2], self.currentValues[i * 2 + 1])
                self.pointRects[i].Left = thePoint.X - usliders.kSliderDraggerHeight / 2
                self.pointRects[i].Right = self.pointRects[i].Left + usliders.kSliderDraggerHeight
                self.pointRects[i].Top = thePoint.Y - usliders.kSliderDraggerHeight / 2
                self.pointRects[i].Bottom = self.pointRects[i].Top + usliders.kSliderDraggerHeight
            # center point value texts 
            totalWidth = 0
            #  for i := 0 to 3 do totalWidth := totalWidth + canvas.textWidth(valueStrings[i]);
            #  totalWidth := totalWidth + kBetweenGap * 3;
            #  xPos := self.left + self.width div 2 - totalWidth div 2;  
            xPos = self.graphRect.Left
            for i in range(0, 3 + 1):
                self.valueRects[i].Left = xPos
                self.valueRects[i].Right = self.valueRects[i].Left + self.Canvas.TextWidth(valueStrings[i])
                self.valueRects[i].Top = minXTextRect.Bottom + uppanel.kLeftRightGap / 2
                self.valueRects[i].Bottom = self.valueRects[i].Top + self.textHeight
                xPos = xPos + (self.valueRects[i].Right - self.valueRects[i].Left) + uppanel.kLeftRightGap
            # center unit text 
            self.unitTextRect.Left = self.graphRect.Left + (self.graphRect.Right - self.graphRect.Left) / 2 - self.Canvas.TextWidth(currentUnitString) / 2
            self.unitTextRect.Right = self.unitTextRect.Left + self.Canvas.TextWidth(currentUnitString)
            self.unitTextRect.Top = minXTextRect.Top
            self.unitTextRect.Bottom = self.unitTextRect.Top + self.textHeight
            if self.editEnabled:
                # finally, draw all text 
                # draw lines black if enabled, else gray 
                self.Canvas.Pen.Color = UNRESOLVED.clBtnText
            else:
                self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
            # draw axes 
            self.Canvas.MoveTo(self.graphRect.Left, self.graphRect.Top)
            self.Canvas.LineTo(self.graphRect.Left, self.graphRect.Bottom)
            self.Canvas.LineTo(self.graphRect.Right, self.graphRect.Bottom)
            # draw axis labels 
            self.drawText(minYString, minYTextRect, false, false, true)
            self.drawText(maxYString, maxYTextRect, false, false, true)
            self.drawText(minXString, minXTextRect, false, false, true)
            self.drawText(maxXString, maxXTextRect, false, false, true)
            for i in range(0, 3 + 1):
                # draw value texts 
                self.drawText(valueStrings[i], self.valueRects[i], true, (self.editEnabled) and (i == self.selectedItemIndex - kItemX1), false)
            # draw unit string 
            self.drawText(currentUnitString, self.unitTextRect, true, (self.editEnabled) and (self.selectedItemIndex == kItemSCurveUnitText), false)
            for i in range(0, 1 + 1):
                # draw point rectangles and labels (labels first because brush color will affect them 
                # first put text at lower right of point 
                pointTextRect = Rect(self.pointRects[i].Right + 5, self.pointRects[i].Top, self.pointRects[i].Right + 5 + self.Canvas.TextWidth(IntToStr(i + 1)), self.pointRects[i].Top + self.textHeight)
                if pointTextRect.Right >= self.graphRect.Right:
                    # adjust point text rectangle if could not be seen 
                    delphi_compatability.OffsetRect(pointTextRect, -20, 0)
                if pointTextRect.Bottom >= self.graphRect.Bottom:
                    delphi_compatability.OffsetRect(pointTextRect, 0, -10)
                self.drawText(IntToStr(i + 1), pointTextRect, false, false, false)
            # draw curve 
            failed = self.drawSCurve(true, failed)
            if not failed:
                for i in range(0, 1 + 1):
                    # draw points 
                    usliders.KfDrawButton(self.Canvas, self.pointRects[i], (self.selectedItemIndex == kItemPoint1 + i), self.editEnabled)
        finally:
            gRecursing = false
    
    def drawSCurve(self, draw, failed):
        i = 0
        x = 0.0
        y = 0.0
        thisPoint = TPoint()
        curve = SCurveStructure()
        numPoints = 0
        
        failed = true
        if self.plant == None:
            return failed
        numPoints = 100
        # assumes that zero does NOT fall between x1 and x2, though one of these could be zero 
        curve.x1 = self.currentValues[0]
        curve.y1 = self.currentValues[1]
        curve.x2 = self.currentValues[2]
        curve.y2 = self.currentValues[3]
        if draw:
            self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
        try:
            failed = umath.calcSCurveCoeffsWithResult(curve, failed)
            if failed:
                return failed
            for i in range(0, numPoints):
                # delphi 2.0 wants this 
                x = 0.0
                y = 0.0
                try:
                    x = self.minXValue + (1.0 * i / numPoints) * (self.maxXValue - self.minXValue)
                except:
                    return failed
                y = umath.scurveWithResult(x, curve.c1, curve.c2, failed)
                if failed:
                    return failed
                if draw:
                    thisPoint = self.pointFromXY(x, y)
                    if i == 0:
                        self.Canvas.MoveTo(thisPoint.X, thisPoint.Y)
                    else:
                        self.Canvas.LineTo(thisPoint.X, thisPoint.Y)
        except:
            return failed
        failed = false
        return failed
    
    def maxWidth(self):
        result = 0
        result = uppanel.kLeftRightGap * 2 + umath.intMax(self.labelWidth, uppanel.kEditMaxWidth)
        return result
    
    def minWidth(self, requestedWidth):
        result = 0
        minAllowed = 0
        
        # cfk note: commented out part of this because it is estimating too wide, don't know why 
        #+ kLeftRightGap * 3
        minAllowed = uppanel.kLeftRightGap * 2 + umath.intMax(self.longestLabelWordWidth, self.formTextWidth("0.0") + udebug.kBetweenGap + self.formTextWidth("x2 0.00") * 4 + uppanel.kLeftRightGap)
        if requestedWidth > minAllowed:
            result = -1
        else:
            result = minAllowed
        return result
    
    def uncollapsedHeight(self):
        result = 0
        result = self.collapsedHeight() + uppanel.kGraphHeight + self.textHeight * 3 + udebug.kBetweenGap * 2 + uppanel.kTopBottomGap
        return result
    
    def maxSelectedItemIndex(self):
        result = 0
        if (not self.param.collapsed) and (self.editEnabled):
            result = kItemSCurveUnitText
        else:
            result = uppanel.kItemLabel
        return result
    
    # ---------------------------------------------------------------------------- utilities 
    def toPlantUnit(self, value):
        result = 0.0
        result = uunits.Convert(self.param.unitSet, self.currentUnitIndex, self.param.unitModel, value)
        return result
    
    def toCurrentUnit(self, value):
        result = 0.0
        result = uunits.Convert(self.param.unitSet, self.param.unitModel, self.currentUnitIndex, value)
        return result
    
    def xValueFromPointPosition(self, aPoint):
        result = 0.0
        result = self.minXValue + (self.maxXValue - self.minXValue) * (aPoint.X - self.graphRect.Left) / (self.graphRect.Right - self.graphRect.Left)
        return result
    
    def yValueFromPointPosition(self, aPoint):
        result = 0.0
        result = 1.0 - (aPoint.Y - self.graphRect.Top) / (self.graphRect.Bottom - self.graphRect.Top)
        return result
    
    def pointFromXY(self, x, y):
        result = TPoint()
        result.X = self.graphRect.Left + intround(((x - self.minXValue) / (self.maxXValue - self.minXValue)) * (self.graphRect.Right - self.graphRect.Left))
        result.Y = self.graphRect.Top + intround((1.0 - y) * (self.graphRect.Bottom - self.graphRect.Top))
        return result
    
    def stringForIndex(self, index):
        result = ""
        if index == 0:
            result = "x1"
        elif index == 1:
            result = "y1"
        elif index == 2:
            result = "x2"
        elif index == 3:
            result = "y2"
        return result
    
    def checkPlantValuesAgainstSoftBounds(self, aFieldIndex):
        result = false
        i = 0
        
        result = false
        if aFieldIndex != -1:
            result = self.checkOneValueAgainstSoftBounds(aFieldIndex)
        else:
            for i in range(0, 3 + 1):
                if self.checkOneValueAgainstSoftBounds(i):
                    result = true
        return result
    
    def checkOneValueAgainstSoftBounds(self, i):
        result = false
        oldValue = 0.0
        bound = 0.0
        
        oldValue = self.currentValues[i]
        bound = self.boundForIndex(i, true)
        if self.currentValues[i] < bound:
            bound = self.currentValues[i]
        bound = self.boundForIndex(i, false)
        if self.currentValues[i] > bound:
            bound = self.currentValues[i]
        result = (self.currentValues[i] != oldValue)
        return result
    
    def boundForIndex(self, index, isMinimum):
        result = 0.0
        result = 0.0
        if index == 0:
            if isMinimum:
                # x 
                result = self.minXValue
            else:
                result = self.maxXValue
        elif index == 2:
            if isMinimum:
                # x 
                result = self.minXValue
            else:
                result = self.maxXValue
        elif index == 1:
            if isMinimum:
                # y 
                result = 0.0
            else:
                result = 1.0
        elif index == 3:
            if isMinimum:
                # y 
                result = 0.0
            else:
                result = 1.0
        return result
    
# not using
#procedure PdSCurveParameterPanel.checkPointsForFailure(var movingPoint: TPoint; var nonMovingPoint: TPoint);
#  var
#    failed: boolean;
#    distanceFromLeft, distanceFromRight, distanceFromTop, distanceFromBottom: integer;
#    distanceFromOtherPointX, smallestDistance, increment: integer;
#  begin
#  failed := true;
#  increment := 5;
#  while failed do
#    begin
#    failed := self.drawSCurve(false);
#    if failed then
#      begin
#      distanceFromLeft := movingPoint.x - graphRect.left;
#      distanceFromRight := graphRect.right - movingPoint.x;
#      distanceFromTop := movingPoint.y - graphRect.top;
#      distanceFromBottom := graphRect.bottom - movingPoint.y;
#      distanceFromOtherPointX := movingPoint.x - nonMovingPoint.x;
#      smallestDistance := intMin(distanceFromLeft, intMin(distanceFromRight,
#        intMin(distanceFromTop, intMin(distanceFromBottom, distanceFromOtherPointX))));
#      if smallestDistance = distanceFromLeft then movingPoint.x := movingPoint.x + increment
#      else if smallestDistance = distanceFromRight then movingPoint.x := movingPoint.x - increment
#      else if smallestDistance = distanceFromTop then movingPoint.y := movingPoint.y + increment
#      else if smallestDistance = distanceFromBottom then movingPoint.y := movingPoint.y - increment
#      else if smallestDistance = distanceFromOtherPointX then
#        if distanceFromOtherPointX > 0 then
#          movingPoint.x := movingPoint.x + increment
#        else
#          movingPoint.x := movingPoint.x - increment;
#      end;
#    end;
#  end;
#
