# unit UWinSliders

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

# Published declarations 
# must be at least 4 more than dragger height 
# should be odd number 
# PDF PORT -- not used anyway
def Register1():
    UNRESOLVED.RegisterComponents("Samples", [KfWinSlider, ])

class KfWinSlider(TCustomControl):
    def __init__(self):
        self.draggerHeight = 0
        self.draggerWidth = 0
        self.FMinValue = 0
        self.FMaxValue = 0
        self.FReadOnly = false
        self.FCurrentValue = 0
        self.dragging = false
        self.dragStart = 0
        self.originalValue = 0
        self.draggerRect = TRect()
    
    def create(self, AnOwner):
        TCustomControl.create(self, AnOwner)
        self.Width = 140
        self.Height = 35
        self.MinValue = 0
        self.MaxValue = 100
        self.draggerHeight = kSliderDraggerHeight
        self.draggerWidth = kSliderDraggerWidth
        self.ReadOnly = false
        self.CurrentValue = 0
        self.dragging = false
        self.TabStop = true
        self.useDefaultSizeAndDraggerSize()
        return self
    
    def useDefaultSizeAndDraggerSize(self):
        if self.ReadOnly:
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
        TCustomControl.CMFocusChanged(self)
        self.Repaint()
    
    def WMGetDlgCode(self, message):
        message.result = delphi_compatability.DLGC_WANTARROWS
    
    #returns true if current value changed
    def setValue(self, newValue):
        result = false
        result = false
        if newValue > self.MaxValue:
            newValue = self.MaxValue
        if newValue < self.MinValue:
            newValue = self.MinValue
        if newValue == self.CurrentValue:
            return result
        self.CurrentValue = newValue
        #repaint;   
        result = true
        return result
    
    def keyDown(self, Key, shift):
        newValue = 0L
        
        TCustomControl.keyDown(self)
        if not self.ReadOnly:
            if Key == delphi_compatability.VK_LEFT:
                newValue = self.CurrentValue - 1
            elif Key == delphi_compatability.VK_RIGHT:
                newValue = self.CurrentValue + 1
            elif Key == delphi_compatability.VK_UP:
                newValue = self.CurrentValue + 1
            elif Key == delphi_compatability.VK_DOWN:
                newValue = self.CurrentValue - 1
            elif Key == delphi_compatability.VK_NEXT:
                #page up
                newValue = self.CurrentValue - 5
            elif Key == delphi_compatability.VK_PRIOR:
                #page down
                newValue = self.CurrentValue + 5
            else :
                return Key
            self.Invalidate()
            self.Refresh()
            self.setValue(newValue)
        return Key
    
    def pointOnDragger(self, x, y):
        result = false
        result = delphi_compatability.PtInRect(self.draggerRect, Point(x, y))
        return result
    
    def mouseDown(self, Button, Shift, X, Y):
        TCustomControl.mouseDown(self)
        self.SetFocus()
        if not self.ReadOnly:
            if (Button == delphi_compatability.TMouseButton.mbLeft):
                #and (pointOnDragger(x, y))
                self.dragging = true
                self.dragStart = X
                self.originalValue = self.CurrentValue
            self.Invalidate()
            self.Refresh()
    
    def mouseMove(self, Shift, X, Y):
        delta = 0L
        newValue = 0L
        lineLength = 0L
        
        TCustomControl.mouseMove(self)
        if self.dragging:
            delta = X - self.dragStart
            #pdf fix - won't snap to grid - will just change relative...
            lineLength = self.Width - 2 * (self.draggerWidth / 2)
            newValue = self.originalValue + intround(delta * (self.MaxValue - self.MinValue) / lineLength)
            self.Invalidate()
            self.Refresh()
            self.setValue(newValue)
    
    def mouseUp(self, Button, Shift, X, Y):
        TCustomControl.mouseUp(self)
        if self.dragging:
            self.dragging = false
    
    def xDistanceFromCurrentValue(self, distanceInPixels):
        result = 0L
        proportion = 0.0
        
        proportion = (self.CurrentValue - self.MinValue) / (self.MaxValue - self.MinValue)
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
        if not self.ReadOnly:
            #draw dragger if not read only 
            KfDrawButton(self.Canvas, self.draggerRect, self.Focused(), self.Enabled)
        if (self.Focused()):
            self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
            self.Canvas.MoveTo(fullRect.Right - 1, fullRect.Top)
            self.Canvas.LineTo(fullRect.Left, fullRect.Top)
            self.Canvas.LineTo(fullRect.Left, fullRect.Bottom - 1)
            self.Canvas.LineTo(fullRect.Right - 1, fullRect.Bottom - 1)
            self.Canvas.LineTo(fullRect.Right - 1, fullRect.Top)
    
