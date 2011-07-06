# unit Usliders

from conversion_common import *
import delphi_compatability

# const
kSliderHeightReadOnly = 5
kSliderHeightNotReadOnly = 11
kSliderDraggerHeight = 7
kSliderDraggerWidth = 5
kSliderGrayLineThickness = 1
kSliderBlueLineThickness = 3
kSliderDefaultWidth = 20
kMinDragDistance = 1

def KfDrawButton(aCanvas, aRect, selected, enabled):
    internalRect = TRect()
    
    aCanvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
    if enabled:
        aCanvas.Pen.Color = delphi_compatability.clBlack
        aCanvas.Brush.Color = delphi_compatability.clWhite
    else:
        aCanvas.Brush.Color = UNRESOLVED.clBtnShadow
        aCanvas.Pen.Color = UNRESOLVED.clBtnShadow
    aCanvas.Rectangle(aRect.Left, aRect.Top, aRect.Right, aRect.Bottom)
    if selected:
        internalRect = aRect
        UNRESOLVED.inflateRect(internalRect, -1, -1)
        aCanvas.Brush.Color = delphi_compatability.clAqua
        aCanvas.FillRect(internalRect)

class KfSlider(TGraphicControl):
    def __init__(self):
        self.FOnKeyDown = TNotifyEvent()
        self.FOnMouseDown = TNotifyEvent()
        self.FOnMouseMove = TNotifyEvent()
        self.FOnMouseUp = TNotifyEvent()
        self.draggerHeight = 0L
        self.draggerWidth = 0L
        self.minValue = 0L
        self.maxValue = 0L
        self.hasUnofficialFocus = false
        self.readOnly = false
        self.currentValue = 0L
        self.dragging = false
        self.dragStart = 0L
        self.originalValue = 0L
        self.draggerRect = TRect()
    
    #function valueForPosition(x: longint): longint;  
    # must be at least 4 more than dragger height 
    # should be odd number 
    def create(self, AnOwner):
        TGraphicControl.create(self, AnOwner)
        self.Width = 140
        self.Height = 35
        self.minValue = 0
        self.maxValue = 100
        self.draggerHeight = kSliderDraggerHeight
        self.draggerWidth = kSliderDraggerWidth
        self.readOnly = false
        self.currentValue = 0
        self.dragging = false
        self.useDefaultSizeAndDraggerSize()
        return self
    
    def useDefaultSizeAndDraggerSize(self):
        if self.readOnly:
            # assumes that readOnly is already set, and assumes that value of readOnly will not be changed
            #    unless this is called again afterward 
            self.Height = kSliderHeightReadOnly
            self.Width = kSliderDefaultWidth
            self.draggerHeight = 0
            self.draggerWidth = 0
        else:
            self.Height = kSliderHeightNotReadOnly
            self.Width = kSliderDefaultWidth
            self.draggerHeight = kSliderDraggerHeight
            self.draggerWidth = kSliderDraggerWidth
    
    def CMFocusChanged(self, message):
        TGraphicControl.CMFocusChanged(self)
        #repaint;  
    
    def WMGetDlgCode(self, message):
        message.result = delphi_compatability.DLGC_WANTARROWS
    
    #returns true if current value changed
    def setValue(self, newValue):
        result = false
        result = false
        if newValue > self.maxValue:
            newValue = self.maxValue
        if newValue < self.minValue:
            newValue = self.minValue
        if newValue == self.currentValue:
            return result
        self.currentValue = newValue
        #repaint;   
        result = true
        return result
    
    def doKeyDown(self, sender, Key, shift):
        newValue = 0L
        
        if self.readOnly:
            return Key
        if Key == delphi_compatability.VK_LEFT:
            newValue = self.currentValue - 1
        elif Key == delphi_compatability.VK_RIGHT:
            newValue = self.currentValue + 1
        else :
            newValue = self.currentValue
        self.Invalidate()
        self.Refresh()
        if self.setValue(newValue) and delphi_compatability.Assigned(self.FOnKeyDown):
            self.FOnKeyDown(self)
        return Key
    
    def pointOnDragger(self, x, y):
        result = false
        result = delphi_compatability.PtInRect(self.draggerRect, Point(x, y))
        return result
    
    def mouseDown(self, Button, Shift, X, Y):
        TGraphicControl.mouseDown(self, Button, Shift, X, Y)
        if self.readOnly:
            if delphi_compatability.Assigned(self.FOnMouseDown):
                self.FOnMouseDown(self)
            return
        if (Button == delphi_compatability.TMouseButton.mbLeft):
            #and (pointOnDragger(x, y))
            self.dragging = true
            self.dragStart = X
            self.originalValue = self.currentValue
            #pdf fix - may want to do more here
            self.hasUnofficialFocus = true
        self.Invalidate()
        self.Refresh()
        if delphi_compatability.Assigned(self.FOnMouseDown):
            self.FOnMouseDown(self)
    
    def mouseMove(self, Shift, X, Y):
        delta = 0L
        newValue = 0L
        lineLength = 0L
        
        TGraphicControl.mouseMove(self, Shift, X, Y)
        if self.readOnly:
            return
        if self.dragging:
            delta = X - self.dragStart
            #pdf fix - won't snap to grid - will just change relative...
            lineLength = self.Width - 2 * (self.draggerWidth / 2)
            newValue = self.originalValue + intround(1.0 * delta * (self.maxValue - self.minValue) / lineLength)
            self.Invalidate()
            self.Refresh()
            if self.setValue(newValue) and delphi_compatability.Assigned(self.FOnMouseMove):
                self.FOnMouseMove(self)
    
    def mouseUp(self, Button, Shift, X, Y):
        TGraphicControl.mouseUp(self, Button, Shift, X, Y)
        if self.readOnly:
            return
        if (Button == delphi_compatability.TMouseButton.mbLeft) and self.dragging:
            self.dragging = false
        if abs(X - self.dragStart) < kMinDragDistance:
            return
        self.dragStart = 0
        if delphi_compatability.Assigned(self.FOnMouseUp):
            self.FOnMouseUp(self)
    
    def xDistanceFromCurrentValue(self, distanceInPixels):
        result = 0L
        proportion = 0.0
        
        proportion = (self.currentValue - self.minValue) / (self.maxValue - self.minValue)
        try:
            result = intround(proportion * distanceInPixels)
        except:
            result = 0
        return result
    
    def paint(self):
        grayRect = TRect()
        blueRect = TRect()
        fullRect = TRect()
        lineRect = TRect()
        distance = 0L
        
        fullRect = self.GetClientRect()
        # start with total fill 
        self.Canvas.Brush.Color = UNRESOLVED.clBtnFace
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        self.Canvas.FillRect(fullRect)
        # rect for line 
        lineRect = fullRect
        lineRect.Left = lineRect.Left + self.draggerWidth / 2 + 2
        lineRect.Right = lineRect.Right - self.draggerWidth / 2 - 1
        lineRect.Top = lineRect.Top + (lineRect.Bottom - lineRect.Top) / 2 - kSliderBlueLineThickness / 2
        lineRect.Bottom = lineRect.Top + kSliderBlueLineThickness
        # rect for dragger 
        distance = self.xDistanceFromCurrentValue(lineRect.Right - lineRect.Left)
        self.draggerRect.Left = lineRect.Left + distance - self.draggerWidth / 2 - self.draggerWidth % 2
        self.draggerRect.Right = self.draggerRect.Left + self.draggerWidth
        self.draggerRect.Top = lineRect.Top - self.draggerHeight / 2 + kSliderBlueLineThickness / 2
        self.draggerRect.Bottom = self.draggerRect.Top + self.draggerHeight
        # blue rect 
        blueRect = lineRect
        blueRect.Right = blueRect.Left + distance
        # gray rect 
        grayRect = lineRect
        grayRect.Top = grayRect.Top + (grayRect.Bottom - grayRect.Top) / 2
        grayRect.Bottom = grayRect.Top + kSliderGrayLineThickness
        if self.Enabled:
            grayRect.Left = blueRect.Right + 1
        #draw gray line
        self.Canvas.Brush.Color = UNRESOLVED.clBtnShadow
        self.Canvas.FillRect(grayRect)
        if self.Enabled:
            #draw blue line
            self.Canvas.Brush.Color = delphi_compatability.clBlue
            self.Canvas.FillRect(blueRect)
        if not self.readOnly:
            #draw dragger if not read only 
            KfDrawButton(self.Canvas, self.draggerRect, self.hasUnofficialFocus, self.Enabled)
        if (self.hasUnofficialFocus):
            self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
            self.Canvas.MoveTo(fullRect.Right - 1, fullRect.Top)
            self.Canvas.LineTo(fullRect.Left, fullRect.Top)
            self.Canvas.LineTo(fullRect.Left, fullRect.Bottom - 1)
            self.Canvas.LineTo(fullRect.Right - 1, fullRect.Bottom - 1)
            self.Canvas.LineTo(fullRect.Right - 1, fullRect.Top)
    
