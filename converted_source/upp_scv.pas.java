// unit upp_scv

from conversion_common import *;
import usliders;
import udebug;
import uppanel;
import delphi_compatability;

// const
kItemPoint1 = 1;
kItemPoint2 = 2;
kItemX1 = 3;
kItemY1 = 4;
kItemX2 = 5;
kItemY2 = 6;
kItemSCurveUnitText = 7;


// var
boolean gRecursing = false;



class PdSCurveParameterPanel extends PdParameterPanel {
    public boolean editEnabled;
    public boolean draggingPoint;
    public  currentValues;
    public float minXValue;
    public float maxXValue;
    public boolean belowZero;
    public int currentUnitIndex;
    public TRect graphRect;
    public  pointRects;
    public  valueRects;
    public TRect unitTextRect;
    
    // ----------------------------------------------------------------------------- initialize 
    public void initialize() {
        float temp = 0.0;
        
        this.OnMouseDown = this.doMouseDown;
        this.OnMouseMove = this.doMouseMove;
        this.OnMouseUp = this.doMouseUp;
        this.OnKeyDown = this.doKeyDown;
        this.draggingPoint = false;
        this.currentUnitIndex = 0;
        if (UNRESOLVED.domain.options.useMetricUnits) {
            this.currentUnitIndex = this.param.unitMetric;
        } else {
            this.currentUnitIndex = this.param.unitEnglish;
        }
        this.minXValue = this.param.lowerBound;
        this.maxXValue = this.param.upperBound;
        this.belowZero = false;
        if ((this.minXValue < 0.0)) {
            temp = abs(this.maxXValue);
            this.maxXValue = abs(this.minXValue);
            this.minXValue = temp;
            this.belowZero = true;
        }
    }
    
    // ------------------------------------------------------------------------ mouse and key 
    public void doMouseDown(TObject sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint thePoint = new TPoint();
        int i = 0;
        
        // must always call this first because it sets the focus 
        super.doMouseDown(sender, Button, Shift, X, Y);
        if (!this.editEnabled) {
            return;
        }
        thePoint = Point(X, Y);
        for (i = 0; i <= 1; i++) {
            if (delphi_compatability.PtInRect(this.pointRects[i], thePoint)) {
                this.selectedItemIndex = kItemPoint1 + i;
                this.draggingPoint = true;
                // should be only point rect 
                this.Invalidate();
            }
        }
        if (!this.Focused()) {
            this.SetFocus();
        }
    }
    
    public void doMouseMove(TObject sender, TShiftState Shift, int X, int Y) {
        int i = 0;
        int index = 0;
         saveValues = [0] * (range(0, 3 + 1) + 1);
        boolean failed = false;
         points = [0] * (range(0, 1 + 1) + 1);
        
        if (!this.draggingPoint) {
            return;
        }
        if (!this.editEnabled) {
            return;
        }
        for (i = 0; i <= 3; i++) {
            saveValues[i] = this.currentValues[i];
        }
        index = this.selectedItemIndex - kItemPoint1;
        // do nothing - to prevent repetitive messages if problem 
        try {
            points[index] = Point(X, Y);
            if (index == 0) {
                // set other point 
                points[1] = this.pointFromXY(this.currentValues[2], this.currentValues[3]);
            } else {
                points[0] = this.pointFromXY(this.currentValues[0], this.currentValues[1]);
            }
            this.keepPointInGraphRect(points[index]);
            this.keepPointsFromCrossing(points[0], points[1], index);
            this.currentValues[index * 2] = this.xValueFromPointPosition(points[index]);
            this.currentValues[index * 2 + 1] = this.yValueFromPointPosition(points[index]);
            failed = this.drawSCurve(false, failed);
            if (failed) {
                for (i = 0; i <= 3; i++) {
                    this.currentValues[i] = saveValues[i];
                }
            }
            // whole 
            this.Invalidate();
        } catch (Exception e) {
            // pass
        }
    }
    
    public void doMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint thePoint = new TPoint();
        int i = 0;
        
        // must always call this first because it sets the focus 
        super.doMouseUp(Sender, Button, Shift, X, Y);
        thePoint = Point(X, Y);
        for (i = 0; i <= 1; i++) {
            if ((delphi_compatability.PtInRect(this.pointRects[i], thePoint)) && (this.editEnabled)) {
                if (this.draggingPoint) {
                    this.draggingPoint = false;
                    this.setPointAfterMouseUp(i, X, Y);
                    this.Invalidate();
                    return;
                }
            }
        }
        if (this.draggingPoint) {
            this.draggingPoint = false;
        }
        for (i = 0; i <= 3; i++) {
            if ((delphi_compatability.PtInRect(this.valueRects[i], thePoint)) && (this.editEnabled)) {
                this.selectedItemIndex = i + kItemX1;
                this.Invalidate();
                if (delphi_compatability.TShiftStateEnum.ssShift in Shift) {
                    this.adjustAllValuesAtOnce();
                } else {
                    this.adjustValue();
                }
                return;
            }
        }
        if (delphi_compatability.PtInRect(this.unitTextRect, thePoint)) {
            // can still do this if disabled 
            this.selectedItemIndex = kItemSCurveUnitText;
            this.Invalidate();
            this.selectNextUnitInSet(delphi_compatability.TShiftStateEnum.ssShift in Shift);
        }
    }
    
    public void doKeyDown(TObject sender, byte key, TShiftState shift) {
        int increment = 0;
        int index = 0;
        
        super.doKeyDown(sender, key, shift);
        increment = 2;
        if (key == delphi_compatability.VK_RETURN) {
            switch (this.selectedItemIndex) {
                case kItemX1:
                    if (delphi_compatability.TShiftStateEnum.ssShift in shift) {
                        this.adjustAllValuesAtOnce();
                    } else {
                        this.adjustValue();
                    }
                    break;
                case kItemY1:
                    if (delphi_compatability.TShiftStateEnum.ssShift in shift) {
                        this.adjustAllValuesAtOnce();
                    } else {
                        this.adjustValue();
                    }
                    break;
                case kItemX2:
                    if (delphi_compatability.TShiftStateEnum.ssShift in shift) {
                        this.adjustAllValuesAtOnce();
                    } else {
                        this.adjustValue();
                    }
                    break;
                case kItemY2:
                    if (delphi_compatability.TShiftStateEnum.ssShift in shift) {
                        this.adjustAllValuesAtOnce();
                    } else {
                        this.adjustValue();
                    }
                    break;
                case kItemSCurveUnitText:
                    this.selectNextUnitInSet(delphi_compatability.TShiftStateEnum.ssShift in shift);
                    break;
        } else if ((this.selectedItemIndex == kItemPoint1) || (this.selectedItemIndex == kItemPoint2)) {
            index = this.selectedItemIndex - kItemPoint1;
            switch (key) {
                case delphi_compatability.VK_LEFT:
                    this.adjustValueByPixels(index, -increment, 0);
                    break;
                case delphi_compatability.VK_RIGHT:
                    this.adjustValueByPixels(index, increment, 0);
                    break;
                case delphi_compatability.VK_DOWN:
                    this.adjustValueByPixels(index, 0, increment);
                    break;
                case delphi_compatability.VK_UP:
                    this.adjustValueByPixels(index, 0, -increment);
                    break;
        }
        return key;
    }
    
    // --------------------------------------------------------- functions called by mouse and key 
    public void adjustValue() {
        ansistring newString = new ansistring();
        String oldString = "";
        String nameString = "";
        String prompt = "";
        String currentUnitString = "";
        float newValue = 0.0;
        float oldValue = 0.0;
        float valueInCurrentUnit = 0.0;
        int index = 0;
        boolean failed = false;
         points = [0] * (range(0, 1 + 1) + 1);
        
        if (this.selectedItemIndex < kItemX1) {
            return;
        }
        index = this.selectedItemIndex - kItemX1;
        oldValue = this.currentValues[index];
        nameString = UNRESOLVED.copy(this.Caption, 1, 30);
        currentUnitString = UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.currentUnitIndex);
        if (len(nameString) == 30) {
            nameString = nameString + "...";
        }
        if (!odd(index)) {
            // x 
            valueInCurrentUnit = this.toCurrentUnit(this.currentValues[index]);
            newString = UNRESOLVED.digitValueString(valueInCurrentUnit);
            // y 
            // don't convert y value - is always 0-1 
        } else {
            valueInCurrentUnit = this.currentValues[index];
            newString = FloatToStrF(valueInCurrentUnit, UNRESOLVED.ffFixed, 7, 2);
        }
        oldString = newString;
        prompt = "Type a new value.";
        if (InputQuery("Enter value", prompt, newString)) {
            if ((newString != oldString) && (UNRESOLVED.boundForString(newString, this.param.fieldType, newValue))) {
                if (!odd(index)) {
                    this.currentValues[index] = this.toPlantUnit(newValue);
                } else {
                    this.currentValues[index] = newValue;
                }
                points[0] = this.pointFromXY(this.currentValues[0], this.currentValues[1]);
                points[1] = this.pointFromXY(this.currentValues[2], this.currentValues[3]);
                this.keepPointInGraphRect(points[(index - 1) / 2]);
                this.keepPointsFromCrossing(points[0], points[1], (index - 1) / 2);
                failed = this.drawSCurve(false, failed);
                if (failed) {
                    this.currentValues[index] = oldValue;
                    ShowMessage("Invalid value.");
                } else {
                    // don't create change point command here, because only one float is changed 
                    UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeRealValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValues[index], this.param.fieldNumber, index, this.param.regrow));
                    this.Invalidate();
                }
            }
        }
    }
    
    public void adjustAllValuesAtOnce() {
        ansistring newString = new ansistring();
        String oldString = "";
        String prompt = "";
        int i = 0;
        boolean failed = false;
         points = [0] * (range(0, 1 + 1) + 1);
        SCurveStructure oldValues = new SCurveStructure();
        SCurveStructure valuesInCurrentUnit = new SCurveStructure();
        SCurveStructure newValues = new SCurveStructure();
        
        if (this.selectedItemIndex < kItemX1) {
            return;
        }
        oldValues.x1 = this.currentValues[0];
        oldValues.y1 = this.currentValues[1];
        oldValues.x2 = this.currentValues[2];
        oldValues.y2 = this.currentValues[3];
        valuesInCurrentUnit = oldValues;
        valuesInCurrentUnit.x1 = this.toCurrentUnit(oldValues.x1);
        valuesInCurrentUnit.x2 = this.toCurrentUnit(oldValues.x2);
        //FIX unresolved WITH expression: valuesInCurrentUnit
        newString = UNRESOLVED.digitValueString(UNRESOLVED.x1) + " " + UNRESOLVED.digitValueString(UNRESOLVED.y1) + " " + UNRESOLVED.digitValueString(UNRESOLVED.x2) + " " + UNRESOLVED.digitValueString(UNRESOLVED.y2);
        oldString = newString;
        prompt = "Edit these four s curve values.";
        if (InputQuery("Enter value", prompt, newString)) {
            if ((newString != oldString)) {
                try {
                    newValues = UNRESOLVED.stringToSCurve(newString);
                    this.currentValues[0] = newValues.x1;
                    this.currentValues[1] = newValues.y1;
                    this.currentValues[2] = newValues.x2;
                    this.currentValues[3] = newValues.y2;
                } catch (Exception e) {
                    failed = true;
                }
                if (!failed) {
                    points[0] = this.pointFromXY(this.currentValues[0], this.currentValues[1]);
                    points[1] = this.pointFromXY(this.currentValues[2], this.currentValues[3]);
                    for (i = 0; i <= 1; i++) {
                        this.keepPointInGraphRect(points[i]);
                        this.keepPointsFromCrossing(points[0], points[1], 1);
                    }
                    failed = this.drawSCurve(false, failed);
                }
                if (failed) {
                    this.currentValues[0] = oldValues.x1;
                    this.currentValues[1] = oldValues.y1;
                    this.currentValues[2] = oldValues.x2;
                    this.currentValues[3] = oldValues.y2;
                    ShowMessage("Invalid value.");
                } else {
                    // don't create change point command here, because only one float is changed 
                    UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeSCurvePointValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValues[0], this.currentValues[1], this.param.fieldNumber, 0, this.param.regrow));
                    UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeSCurvePointValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValues[2], this.currentValues[3], this.param.fieldNumber, 1, this.param.regrow));
                    this.Invalidate();
                }
            }
        }
    }
    
    public void adjustValueByPixels(int index, int xChange, int yChange) {
         points = [0] * (range(0, 1 + 1) + 1);
        float oldX = 0.0;
        float oldY = 0.0;
        boolean failed = false;
        int xIndex = 0;
        int yIndex = 0;
        
        xIndex = index * 2;
        yIndex = index * 2 + 1;
        oldX = this.currentValues[xIndex];
        oldY = this.currentValues[yIndex];
        points[0] = this.pointFromXY(this.currentValues[0], this.currentValues[1]);
        points[1] = this.pointFromXY(this.currentValues[2], this.currentValues[3]);
        points[index].X = points[index].X + xChange;
        points[index].Y = points[index].Y + yChange;
        this.keepPointInGraphRect(points[index]);
        this.keepPointsFromCrossing(points[0], points[1], index);
        failed = this.drawSCurve(false, failed);
        if (failed) {
            this.currentValues[xIndex] = oldX;
            this.currentValues[yIndex] = oldY;
        } else {
            this.currentValues[xIndex] = this.xValueFromPointPosition(points[index]);
            this.currentValues[yIndex] = this.yValueFromPointPosition(points[index]);
            UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeSCurvePointValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValues[xIndex], this.currentValues[yIndex], this.param.fieldNumber, index, this.param.regrow));
            this.Invalidate();
        }
    }
    
    public void selectNextUnitInSet(boolean shift) {
        if (shift) {
            // no layer or derivation for this - s curve cannot be layer or absolute/relative 
            this.currentUnitIndex = UNRESOLVED.GetPreviousUnitEnumInUnitSet(this.param.unitSet, this.currentUnitIndex);
        } else {
            this.currentUnitIndex = UNRESOLVED.GetNextUnitEnumInUnitSet(this.param.unitSet, this.currentUnitIndex);
        }
        this.updateDisplay();
    }
    
    public void setPointAfterMouseUp(int index, int x, int y) {
        int xIndex = 0;
        int yIndex = 0;
        TPoint thePoint = new TPoint();
        
        this.selectedItemIndex = kItemPoint1 + index;
        thePoint = Point(x, y);
        xIndex = index * 2;
        yIndex = index * 2 + 1;
        this.currentValues[xIndex] = this.xValueFromPointPosition(thePoint);
        this.currentValues[yIndex] = this.yValueFromPointPosition(thePoint);
        // change x and y values 
        UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeSCurvePointValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.currentValues[xIndex], this.currentValues[yIndex], this.param.fieldNumber, index, this.param.regrow));
    }
    
    public void keepPointInGraphRect(TPoint point) {
        if (Point.x < this.graphRect.Left) {
            Point.x = this.graphRect.Left;
        }
        if (Point.x > this.graphRect.Right) {
            Point.x = this.graphRect.Right;
        }
        if (Point.y < this.graphRect.Top) {
            Point.y = this.graphRect.Top;
        }
        if (Point.y > this.graphRect.Bottom) {
            Point.y = this.graphRect.Bottom;
        }
    }
    
    public void keepPointsFromCrossing(TPoint point0, TPoint point1, int movingPoint) {
        TPoint closestPoint = new TPoint();
        float proportion = 0.0;
        float minDifference = 0.0;
        
        proportion = 0.01;
        minDifference = (this.maxXValue - this.minXValue) * proportion;
        closestPoint = this.pointFromXY(minDifference, 0);
        closestPoint.X = UNRESOLVED.intMax(1, closestPoint.X - this.graphRect.Left);
        if (movingPoint == 0) {
            if (point0.X > point1.X - closestPoint.X) {
                point0.X = point1.X - closestPoint.X;
            }
        } else {
            if (point1.X < point0.X + closestPoint.X) {
                point1.X = point0.X + closestPoint.X;
            }
        }
    }
    
    // ------------------------------------------------------------------------------- updating 
    public void updateEnabling() {
        super.updateEnabling();
        if ((this.plant == null) || (this.readOnly)) {
            this.editEnabled = false;
        } else {
            this.editEnabled = true;
        }
    }
    
    public void updatePlantValues() {
        int i = 0;
         oldValues = [0] * (range(0, 3 + 1) + 1);
        boolean changed = false;
        
        if (this.plant == null) {
            return;
        }
        if (this.param.collapsed) {
            return;
        }
        for (i = 0; i <= 3; i++) {
            oldValues[i] = this.currentValues[i];
        }
        this.updateCurrentValue(-1);
        changed = false;
        for (i = 0; i <= 3; i++) {
            if (oldValues[i] != this.currentValues[i]) {
                changed = true;
                break;
            }
        }
        if (changed) {
            this.updateDisplay();
            this.Invalidate();
        }
    }
    
    public void updateCurrentValue(int aFieldIndex) {
        int i = 0;
        
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldFloat)) {
            if (aFieldIndex != -1) {
                this.plant.transferField(UNRESOLVED.kGetField, this.currentValues[aFieldIndex], this.param.fieldNumber, UNRESOLVED.kFieldFloat, aFieldIndex, false, null);
            } else {
                for (i = 0; i <= 3; i++) {
                    this.plant.transferField(UNRESOLVED.kGetField, this.currentValues[i], this.param.fieldNumber, UNRESOLVED.kFieldFloat, i, false, null);
                }
            }
            if (this.currentValues[0] < this.minXValue) {
                this.minXValue = this.currentValues[0];
            }
            if (this.currentValues[2] > this.maxXValue) {
                this.maxXValue = this.currentValues[2];
            }
        } else {
            this.editEnabled = false;
        }
    }
    
    public void updateDisplay() {
        if ((this.plant != null) && (this.param.fieldType == UNRESOLVED.kFieldFloat)) {
            this.Invalidate();
        } else {
            this.editEnabled = false;
        }
    }
    
    // ----------------------------------------------------------------------------------------- painting 
    public void paint() {
        TRect minYTextRect = new TRect();
        TRect maxYTextRect = new TRect();
        TRect minXTextRect = new TRect();
        TRect maxXTextRect = new TRect();
        TRect pointTextRect = new TRect();
        float maxXValueInCurrentUnit = 0.0;
        float minXValueInCurrentUnit = 0.0;
        String minXString = "";
        String maxXString = "";
        String minYString = "";
        String maxYString = "";
        String currentUnitString = "";
         currentValuesInCurrentUnit = [0] * (range(0, 3 + 1) + 1);
         valueStrings = [0] * (range(0, 3 + 1) + 1);
        int i = 0;
        int xPos = 0;
        int totalWidth = 0;
        TPoint thePoint = new TPoint();
        boolean failed = false;
        
        try {
            if (delphi_compatability.Application.terminated) {
                return;
            }
            super.paint();
            if (this.param.collapsed) {
                return;
            }
            if (gRecursing) {
                // errorMessage('PdSCurveParameterPanel.Paint: recursion in paint method'); 
                gRecursing = false;
                return;
            }
            gRecursing = true;
            // convert bounds and values from plant to current unit ( don't convert Y value) 
            // this is only for writing strings; use plant unit for drawing points 
            minXValueInCurrentUnit = this.toCurrentUnit(this.minXValue);
            if (!this.belowZero) {
                maxXValueInCurrentUnit = this.toCurrentUnit(this.maxXValue);
                currentValuesInCurrentUnit[0] = this.toCurrentUnit(this.currentValues[0]);
                currentValuesInCurrentUnit[2] = this.toCurrentUnit(this.currentValues[2]);
            } else {
                maxXValueInCurrentUnit = this.toCurrentUnit(-this.maxXValue);
                currentValuesInCurrentUnit[0] = this.toCurrentUnit(-this.currentValues[0]);
                currentValuesInCurrentUnit[2] = this.toCurrentUnit(-this.currentValues[2]);
            }
            currentValuesInCurrentUnit[1] = this.currentValues[1];
            currentValuesInCurrentUnit[3] = this.currentValues[3];
            // strings to write for number 
            minXString = UNRESOLVED.digitValueString(minXValueInCurrentUnit);
            maxXString = UNRESOLVED.digitValueString(maxXValueInCurrentUnit);
            minYString = "0.0";
            maxYString = "1.0";
            currentUnitString = UNRESOLVED.UnitStringForEnum(this.param.unitSet, this.currentUnitIndex);
            for (i = 0; i <= 3; i++) {
                if ((i == 0) || (i == 2)) {
                    valueStrings[i] = this.stringForIndex(i) + " " + UNRESOLVED.digitValueString(currentValuesInCurrentUnit[i]);
                } else {
                    valueStrings[i] = this.stringForIndex(i) + " " + FloatToStrF(currentValuesInCurrentUnit[i], UNRESOLVED.ffFixed, 7, 2);
                }
            }
            // calculate all rectangles to draw text, points 
            this.graphRect.Left = uppanel.kLeftRightGap + this.Canvas.TextWidth(minYString) + udebug.kBetweenGap;
            this.graphRect.Right = this.ClientWidth - uppanel.kLeftRightGap * 2;
            this.graphRect.Top = this.collapsedHeight();
            this.graphRect.Bottom = this.Height - this.textHeight * 2 - udebug.kBetweenGap - uppanel.kTopBottomGap * 2;
            minXTextRect.Left = this.graphRect.Left;
            minXTextRect.Right = minXTextRect.Left + this.Canvas.TextWidth(minXString);
            minXTextRect.Top = this.graphRect.Bottom + 1;
            minXTextRect.Bottom = minXTextRect.Top + this.textHeight;
            maxXTextRect.Right = this.graphRect.Right;
            maxXTextRect.Left = maxXTextRect.Right - this.Canvas.TextWidth(maxXString);
            maxXTextRect.Top = minXTextRect.Top;
            maxXTextRect.Bottom = maxXTextRect.Top + this.textHeight;
            minYTextRect.Left = this.graphRect.Left - this.Canvas.TextWidth(maxYString) - udebug.kBetweenGap;
            minYTextRect.Right = this.graphRect.Left - 1;
            minYTextRect.Top = this.graphRect.Bottom - this.textHeight;
            minYTextRect.Bottom = this.graphRect.Bottom;
            maxYTextRect.Left = this.graphRect.Left - this.Canvas.TextWidth(maxYString) - udebug.kBetweenGap;
            maxYTextRect.Right = this.graphRect.Left - 1;
            maxYTextRect.Top = this.graphRect.Top;
            maxYTextRect.Bottom = maxYTextRect.Top + this.textHeight;
            for (i = 0; i <= 1; i++) {
                thePoint = this.pointFromXY(this.currentValues[i * 2], this.currentValues[i * 2 + 1]);
                this.pointRects[i].Left = thePoint.X - usliders.kSliderDraggerHeight / 2;
                this.pointRects[i].Right = this.pointRects[i].Left + usliders.kSliderDraggerHeight;
                this.pointRects[i].Top = thePoint.Y - usliders.kSliderDraggerHeight / 2;
                this.pointRects[i].Bottom = this.pointRects[i].Top + usliders.kSliderDraggerHeight;
            }
            // center point value texts 
            totalWidth = 0;
            //  for i := 0 to 3 do totalWidth := totalWidth + canvas.textWidth(valueStrings[i]);
            //  totalWidth := totalWidth + kBetweenGap * 3;
            //  xPos := self.left + self.width div 2 - totalWidth div 2;  
            xPos = this.graphRect.Left;
            for (i = 0; i <= 3; i++) {
                this.valueRects[i].Left = xPos;
                this.valueRects[i].Right = this.valueRects[i].Left + this.Canvas.TextWidth(valueStrings[i]);
                this.valueRects[i].Top = minXTextRect.Bottom + uppanel.kLeftRightGap / 2;
                this.valueRects[i].Bottom = this.valueRects[i].Top + this.textHeight;
                xPos = xPos + (this.valueRects[i].Right - this.valueRects[i].Left) + uppanel.kLeftRightGap;
            }
            // center unit text 
            this.unitTextRect.Left = this.graphRect.Left + (this.graphRect.Right - this.graphRect.Left) / 2 - this.Canvas.TextWidth(currentUnitString) / 2;
            this.unitTextRect.Right = this.unitTextRect.Left + this.Canvas.TextWidth(currentUnitString);
            this.unitTextRect.Top = minXTextRect.Top;
            this.unitTextRect.Bottom = this.unitTextRect.Top + this.textHeight;
            if (this.editEnabled) {
                // finally, draw all text 
                // draw lines black if enabled, else gray 
                this.Canvas.Pen.Color = UNRESOLVED.clBtnText;
            } else {
                this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
            }
            // draw axes 
            this.Canvas.MoveTo(this.graphRect.Left, this.graphRect.Top);
            this.Canvas.LineTo(this.graphRect.Left, this.graphRect.Bottom);
            this.Canvas.LineTo(this.graphRect.Right, this.graphRect.Bottom);
            // draw axis labels 
            this.drawText(minYString, minYTextRect, false, false, true);
            this.drawText(maxYString, maxYTextRect, false, false, true);
            this.drawText(minXString, minXTextRect, false, false, true);
            this.drawText(maxXString, maxXTextRect, false, false, true);
            for (i = 0; i <= 3; i++) {
                // draw value texts 
                this.drawText(valueStrings[i], this.valueRects[i], true, (this.editEnabled) && (i == this.selectedItemIndex - kItemX1), false);
            }
            // draw unit string 
            this.drawText(currentUnitString, this.unitTextRect, true, (this.editEnabled) && (this.selectedItemIndex == kItemSCurveUnitText), false);
            for (i = 0; i <= 1; i++) {
                // draw point rectangles and labels (labels first because brush color will affect them 
                // first put text at lower right of point 
                pointTextRect = Rect(this.pointRects[i].Right + 5, this.pointRects[i].Top, this.pointRects[i].Right + 5 + this.Canvas.TextWidth(IntToStr(i + 1)), this.pointRects[i].Top + this.textHeight);
                if (pointTextRect.Right >= this.graphRect.Right) {
                    // adjust point text rectangle if could not be seen 
                    delphi_compatability.OffsetRect(pointTextRect, -20, 0);
                }
                if (pointTextRect.Bottom >= this.graphRect.Bottom) {
                    delphi_compatability.OffsetRect(pointTextRect, 0, -10);
                }
                this.drawText(IntToStr(i + 1), pointTextRect, false, false, false);
            }
            // draw curve 
            failed = this.drawSCurve(true, failed);
            if (!failed) {
                for (i = 0; i <= 1; i++) {
                    // draw points 
                    usliders.KfDrawButton(this.Canvas, this.pointRects[i], (this.selectedItemIndex == kItemPoint1 + i), this.editEnabled);
                }
            }
        } finally {
            gRecursing = false;
        }
    }
    
    public void drawSCurve(boolean draw, boolean failed) {
        int i = 0;
        float x = 0.0;
        float y = 0.0;
        TPoint thisPoint = new TPoint();
        SCurveStructure curve = new SCurveStructure();
        int numPoints = 0;
        
        failed = true;
        if (this.plant == null) {
            return failed;
        }
        numPoints = 100;
        // assumes that zero does NOT fall between x1 and x2, though one of these could be zero 
        curve.x1 = this.currentValues[0];
        curve.y1 = this.currentValues[1];
        curve.x2 = this.currentValues[2];
        curve.y2 = this.currentValues[3];
        if (draw) {
            this.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
        }
        try {
            UNRESOLVED.calcSCurveCoeffsWithResult(curve, failed);
            if (failed) {
                return failed;
            }
            for (i = 0; i <= numPoints - 1; i++) {
                // delphi 2.0 wants this 
                x = 0.0;
                y = 0.0;
                try {
                    x = this.minXValue + (1.0 * i / numPoints) * (this.maxXValue - this.minXValue);
                } catch (Exception e) {
                    return failed;
                }
                y = UNRESOLVED.scurveWithResult(x, curve.c1, curve.c2, failed);
                if (failed) {
                    return failed;
                }
                if (draw) {
                    thisPoint = this.pointFromXY(x, y);
                    if (i == 0) {
                        this.Canvas.MoveTo(thisPoint.X, thisPoint.Y);
                    } else {
                        this.Canvas.LineTo(thisPoint.X, thisPoint.Y);
                    }
                }
            }
        } catch (Exception e) {
            return failed;
        }
        failed = false;
        return failed;
    }
    
    public int maxWidth() {
        result = 0;
        result = uppanel.kLeftRightGap * 2 + UNRESOLVED.intMax(this.labelWidth, uppanel.kEditMaxWidth);
        return result;
    }
    
    public int minWidth(int requestedWidth) {
        result = 0;
        int minAllowed = 0;
        
        // cfk note: commented out part of this because it is estimating too wide, don't know why 
        //+ kLeftRightGap * 3
        minAllowed = uppanel.kLeftRightGap * 2 + UNRESOLVED.intMax(this.longestLabelWordWidth, this.formTextWidth("0.0") + udebug.kBetweenGap + this.formTextWidth("x2 0.00") * 4 + uppanel.kLeftRightGap);
        if (requestedWidth > minAllowed) {
            result = -1;
        } else {
            result = minAllowed;
        }
        return result;
    }
    
    public int uncollapsedHeight() {
        result = 0;
        result = this.collapsedHeight() + uppanel.kGraphHeight + this.textHeight * 3 + udebug.kBetweenGap * 2 + uppanel.kTopBottomGap;
        return result;
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        if ((!this.param.collapsed) && (this.editEnabled)) {
            result = kItemSCurveUnitText;
        } else {
            result = uppanel.kItemLabel;
        }
        return result;
    }
    
    // ---------------------------------------------------------------------------- utilities 
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
    
    public float xValueFromPointPosition(TPoint aPoint) {
        result = 0.0;
        result = this.minXValue + (this.maxXValue - this.minXValue) * (aPoint.X - this.graphRect.Left) / (this.graphRect.Right - this.graphRect.Left);
        return result;
    }
    
    public float yValueFromPointPosition(TPoint aPoint) {
        result = 0.0;
        result = 1.0 - (aPoint.Y - this.graphRect.Top) / (this.graphRect.Bottom - this.graphRect.Top);
        return result;
    }
    
    public TPoint pointFromXY(float x, float y) {
        result = new TPoint();
        result.X = this.graphRect.Left + intround(((x - this.minXValue) / (this.maxXValue - this.minXValue)) * (this.graphRect.Right - this.graphRect.Left));
        result.Y = this.graphRect.Top + intround((1.0 - y) * (this.graphRect.Bottom - this.graphRect.Top));
        return result;
    }
    
    public String stringForIndex(int index) {
        result = "";
        switch (index) {
            case 0:
                result = "x1";
                break;
            case 1:
                result = "y1";
                break;
            case 2:
                result = "x2";
                break;
            case 3:
                result = "y2";
                break;
        return result;
    }
    
    public boolean checkPlantValuesAgainstSoftBounds(int aFieldIndex) {
        result = false;
        int i = 0;
        
        result = false;
        if (aFieldIndex != -1) {
            result = this.checkOneValueAgainstSoftBounds(aFieldIndex);
        } else {
            for (i = 0; i <= 3; i++) {
                if (this.checkOneValueAgainstSoftBounds(i)) {
                    result = true;
                }
            }
        }
        return result;
    }
    
    public boolean checkOneValueAgainstSoftBounds(int i) {
        result = false;
        float oldValue = 0.0;
        float bound = 0.0;
        
        oldValue = this.currentValues[i];
        bound = this.boundForIndex(i, true);
        if (this.currentValues[i] < bound) {
            bound = this.currentValues[i];
        }
        bound = this.boundForIndex(i, false);
        if (this.currentValues[i] > bound) {
            bound = this.currentValues[i];
        }
        result = (this.currentValues[i] != oldValue);
        return result;
    }
    
    public float boundForIndex(int index, boolean isMinimum) {
        result = 0.0;
        result = 0.0;
        switch (index) {
            case 0:
                if (isMinimum) {
                    // x 
                    result = this.minXValue;
                } else {
                    result = this.maxXValue;
                }
                break;
            case 2:
                if (isMinimum) {
                    // x 
                    result = this.minXValue;
                } else {
                    result = this.maxXValue;
                }
                break;
            case 1:
                if (isMinimum) {
                    // y 
                    result = 0.0;
                } else {
                    result = 1.0;
                }
                break;
            case 3:
                if (isMinimum) {
                    // y 
                    result = 0.0;
                } else {
                    result = 1.0;
                }
                break;
        return result;
    }
    
}
// not using
//procedure PdSCurveParameterPanel.checkPointsForFailure(var movingPoint: TPoint; var nonMovingPoint: TPoint);
//  var
//    failed: boolean;
//    distanceFromLeft, distanceFromRight, distanceFromTop, distanceFromBottom: integer;
//    distanceFromOtherPointX, smallestDistance, increment: integer;
//  begin
//  failed := true;
//  increment := 5;
//  while failed do
//    begin
//    failed := self.drawSCurve(false);
//    if failed then
//      begin
//      distanceFromLeft := movingPoint.x - graphRect.left;
//      distanceFromRight := graphRect.right - movingPoint.x;
//      distanceFromTop := movingPoint.y - graphRect.top;
//      distanceFromBottom := graphRect.bottom - movingPoint.y;
//      distanceFromOtherPointX := movingPoint.x - nonMovingPoint.x;
//      smallestDistance := intMin(distanceFromLeft, intMin(distanceFromRight,
//        intMin(distanceFromTop, intMin(distanceFromBottom, distanceFromOtherPointX))));
//      if smallestDistance = distanceFromLeft then movingPoint.x := movingPoint.x + increment
//      else if smallestDistance = distanceFromRight then movingPoint.x := movingPoint.x - increment
//      else if smallestDistance = distanceFromTop then movingPoint.y := movingPoint.y + increment
//      else if smallestDistance = distanceFromBottom then movingPoint.y := movingPoint.y - increment
//      else if smallestDistance = distanceFromOtherPointX then
//        if distanceFromOtherPointX > 0 then
//          movingPoint.x := movingPoint.x + increment
//        else
//          movingPoint.x := movingPoint.x - increment;
//      end;
//    end;
//  end;
//
