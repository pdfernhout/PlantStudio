# unit upp_col

from conversion_common import *
import ubmpsupport
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
kItemColorRect = 1
kItemRedSlider = 2
kItemGreenSlider = 3
kItemBlueSlider = 4
kColorRectSize = 40
kMinSliderLength = 30

class PdColorParameterPanel(PdParameterPanel):
    def __init__(self):
        self.currentColor = TColorRef()
        self.colorWhileDragging = TColorRef()
        self.redSlider = KfSlider()
        self.greenSlider = KfSlider()
        self.blueSlider = KfSlider()
        self.colorRect = TRect()
    
    def GetPalette(self):
        result = HPALETTE()
        result = umain.MainForm.paletteImage.Picture.Bitmap.Palette
        return result
    
    def initialize(self):
        #assuming sliders will be deleted automatically by owner - self - otherwise would have destructor
        self.redSlider = usliders.KfSlider().create(self)
        self.initSlider(self.redSlider)
        self.greenSlider = usliders.KfSlider().create(self)
        self.initSlider(self.greenSlider)
        self.blueSlider = usliders.KfSlider().create(self)
        self.initSlider(self.blueSlider)
        self.OnMouseUp = self.doMouseUp
    
    def initSlider(self, slider):
        slider.Parent = self
        slider.FOnMouseDown = self.sliderMouseDown
        slider.FOnMouseMove = self.sliderMouseMove
        slider.FOnMouseUp = self.sliderMouseUp
        slider.FOnKeyDown = self.sliderKeyDown
        slider.readOnly = self.param.readOnly
        slider.useDefaultSizeAndDraggerSize()
        slider.minValue = 0
        slider.maxValue = 255
    
    def doKeyDown(self, sender, key, shift):
        if (self.plant != None) and (not self.readOnly):
            if key == delphi_compatability.VK_HOME:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
            elif key == delphi_compatability.VK_END:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
            elif key == delphi_compatability.VK_DOWN:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
            elif key == delphi_compatability.VK_LEFT:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
            elif key == delphi_compatability.VK_UP:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
            elif key == delphi_compatability.VK_RIGHT:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
            elif key == delphi_compatability.VK_NEXT:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
            elif key == delphi_compatability.VK_PRIOR:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
            elif key == delphi_compatability.VK_RETURN:
                if self.selectedItemIndex == kItemRedSlider:
                    # process slider arrow keys first 
                    key = self.redSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemGreenSlider:
                    key = self.greenSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemBlueSlider:
                    key = self.blueSlider.doKeyDown(sender, key, shift)
                    return key
                elif self.selectedItemIndex == kItemColorRect:
                    self.doMouseUp(self, delphi_compatability.TMouseButton.mbLeft, [], self.colorRect.Left + 1, self.colorRect.Top + 1)
        PdParameterPanel.doKeyDown(self, sender, key, shift)
        return key
    
    def doMouseUp(self, Sender, Button, Shift, X, Y):
        thePoint = TPoint()
        newColor = TColorRef()
        
        # must always call this first because it sets the focus 
        PdParameterPanel.doMouseUp(self, Sender, Button, Shift, X, Y)
        if (self.plant == None) or (self.readOnly):
            return
        thePoint = Point(X, Y)
        if delphi_compatability.PtInRect(self.colorRect, thePoint):
            self.selectedItemIndex = kItemColorRect
            newColor = udomain.domain.getColorUsingCustomColors(self.currentColor)
            if newColor != self.currentColor:
                self.currentColor = newColor
                umain.MainForm.doCommand(updcom.PdChangeColorValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentColor, self.param.fieldNumber, uparams.kNotArray, self.param.regrow))
                self.updateDisplay()
                self.Invalidate()
    
    def updateEnabling(self):
        PdParameterPanel.updateEnabling(self)
        self.redSlider.Enabled = self.plant != None
        self.greenSlider.Enabled = self.plant != None
        self.blueSlider.Enabled = self.plant != None
        self.redSlider.readOnly = self.readOnly
        self.greenSlider.readOnly = self.readOnly
        self.blueSlider.readOnly = self.readOnly
    
    def updatePlantValues(self):
        oldColor = TColorRef()
        
        if self.plant == None:
            return
        if self.param.collapsed:
            return
        oldColor = self.currentColor
        self.updateCurrentValue(-1)
        if oldColor != self.currentColor:
            self.updateDisplay()
            self.Invalidate()
    
    def updateCurrentValue(self, aFieldIndex):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldColor):
            self.currentColor = self.plant.transferField(umath.kGetField, self.currentColor, self.param.fieldNumber, uparams.kFieldColor, uparams.kNotArray, false, None)
        else:
            self.disableSliders()
    
    def disableSliders(self):
        self.redSlider.currentValue = 0
        self.redSlider.Enabled = false
        self.greenSlider.currentValue = 0
        self.greenSlider.Enabled = false
        self.blueSlider.currentValue = 0
        self.blueSlider.Enabled = false
    
    def updateDisplay(self):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldColor):
            self.redSlider.currentValue = UNRESOLVED.getRValue(self.currentColor)
            self.greenSlider.currentValue = UNRESOLVED.getGValue(self.currentColor)
            self.blueSlider.currentValue = UNRESOLVED.getBValue(self.currentColor)
        else:
            self.disableSliders()
    
    def sliderMouseDown(self, Sender):
        if self.plant == None:
            return
        self.colorWhileDragging = usupport.support_rgb(self.redSlider.currentValue, self.greenSlider.currentValue, self.blueSlider.currentValue)
        if Sender == self.redSlider:
            self.selectedItemIndex = kItemRedSlider
        elif Sender == self.greenSlider:
            self.selectedItemIndex = kItemGreenSlider
        elif Sender == self.blueSlider:
            self.selectedItemIndex = kItemBlueSlider
        if not self.Focused():
            self.SetFocus()
        else:
            self.Invalidate()
        # paint method updates unofficial focus flags in sliders 
    
    def sliderMouseMove(self, Sender):
        if self.plant != None:
            self.colorWhileDragging = usupport.support_rgb(self.redSlider.currentValue, self.greenSlider.currentValue, self.blueSlider.currentValue)
            # don't make change permanent yet, not until mouse up 
            self.Repaint()
        else:
            self.disableSliders()
    
    def sliderMouseUp(self, Sender):
        if self.plant != None:
            self.currentColor = usupport.support_rgb(self.redSlider.currentValue, self.greenSlider.currentValue, self.blueSlider.currentValue)
            umain.MainForm.doCommand(updcom.PdChangeColorValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.currentColor, self.param.fieldNumber, uparams.kNotArray, self.param.regrow))
            self.updateDisplay()
            self.Invalidate()
        else:
            self.disableSliders()
    
    def sliderKeyDown(self, sender):
        self.sliderMouseUp(sender)
    
    def maxWidth(self):
        result = 0
        result = uppanel.kLeftRightGap * 2 + umath.intMax(self.labelWidth, uppanel.kEditMaxWidth)
        return result
    
    def minWidth(self, requestedWidth):
        result = 0
        minAllowed = 0
        
        minAllowed = uppanel.kLeftRightGap * 2 + umath.intMax(self.longestLabelWordWidth, kColorRectSize + kMinSliderLength + udebug.kBetweenGap)
        if requestedWidth > minAllowed:
            result = -1
        else:
            result = minAllowed
        return result
    
    def uncollapsedHeight(self):
        result = 0
        result = self.collapsedHeight() + umath.intMax(self.redSlider.Height, self.textHeight) * 3 + udebug.kBetweenGap * 2 + uppanel.kTopBottomGap * 3
        return result
    
    def resizeElements(self):
        self.redSlider.Left = uppanel.kLeftRightGap + kColorRectSize + self.formTextWidth("W") + uppanel.kLeftRightGap * 2
        self.redSlider.Width = umath.intMax(0, self.Width - self.redSlider.Left - uppanel.kLeftRightGap)
        self.redSlider.Top = self.collapsedHeight() + uppanel.kTopBottomGap + self.Canvas.TextHeight("r") / 2 - self.redSlider.Height / 2
        self.greenSlider.Left = self.redSlider.Left
        self.greenSlider.Width = self.redSlider.Width
        self.greenSlider.Top = self.redSlider.Top + self.textHeight + self.Canvas.TextHeight("r") / 2 - self.greenSlider.Height / 2
        self.blueSlider.Left = self.redSlider.Left
        self.blueSlider.Width = self.redSlider.Width
        self.blueSlider.Top = self.greenSlider.Top + self.textHeight + self.Canvas.TextHeight("r") / 2 - self.blueSlider.Height / 2
    
    def maxSelectedItemIndex(self):
        result = 0
        if (not self.param.collapsed) and (self.redSlider.Enabled):
            result = kItemBlueSlider
        else:
            result = uppanel.kItemLabel
        return result
    
    def paint(self):
        aRect = TRect()
        rTextRect = TRect()
        gTextRect = TRect()
        bTextRect = TRect()
        collapsedColorRect = TRect()
        
        if delphi_compatability.Application.terminated:
            return
        # ask sliders to update themselves based on whether they are selected 
        self.redSlider.hasUnofficialFocus = (self.selectedItemIndex == kItemRedSlider)
        self.greenSlider.hasUnofficialFocus = (self.selectedItemIndex == kItemGreenSlider)
        self.blueSlider.hasUnofficialFocus = (self.selectedItemIndex == kItemBlueSlider)
        PdParameterPanel.paint(self)
        aRect = self.GetClientRect()
        if (self.param.collapsed) and (self.plant != None):
            collapsedColorRect.Left = aRect.Left + uppanel.kLeftRightGap + uppanel.kArrowPictureSize + uppanel.kOverridePictureSize + udebug.kBetweenGap + self.Canvas.TextWidth(self.Caption) + uppanel.kLeftRightGap
            collapsedColorRect.Right = collapsedColorRect.Left + self.textHeight * 2
            collapsedColorRect.Top = aRect.Top + 2
            collapsedColorRect.Bottom = collapsedColorRect.Top + self.textHeight
            UNRESOLVED.inflateRect(collapsedColorRect, -2, -2)
            self.fillRectWithColor(collapsedColorRect, self.currentColor)
            return
        rTextRect.Left = aRect.Left + uppanel.kLeftRightGap + kColorRectSize + uppanel.kLeftRightGap * 2
        rTextRect.Right = rTextRect.Left + self.Canvas.TextWidth("W")
        rTextRect.Top = self.collapsedHeight() + uppanel.kTopBottomGap
        rTextRect.Bottom = rTextRect.Top + self.textHeight
        gTextRect = rTextRect
        gTextRect.Top = rTextRect.Bottom + udebug.kBetweenGap
        gTextRect.Bottom = gTextRect.Top + self.textHeight
        bTextRect = rTextRect
        bTextRect.Top = gTextRect.Bottom + udebug.kBetweenGap
        bTextRect.Bottom = bTextRect.Top + self.textHeight
        self.colorRect.Left = uppanel.kLeftRightGap * 2
        self.colorRect.Right = rTextRect.Left - uppanel.kLeftRightGap * 2
        self.colorRect.Top = self.collapsedHeight() + uppanel.kTopBottomGap
        self.colorRect.Bottom = self.uncollapsedHeight() - uppanel.kTopBottomGap * 2
        self.drawText("r", rTextRect, false, false, false)
        self.drawText("g", gTextRect, false, false, false)
        self.drawText("b", bTextRect, false, false, false)
        if (self.redSlider.dragging) or (self.greenSlider.dragging) or (self.blueSlider.dragging):
            self.fillRectWithColor(self.colorRect, self.colorWhileDragging)
        elif self.plant == None:
            self.fillRectWithColor(self.colorRect, UNRESOLVED.clBtnFace)
        else:
            self.fillRectWithColor(self.colorRect, self.currentColor)
        self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
        if (self.selectedItemIndex != kItemColorRect):
            self.Canvas.Pen.Width = 1
            self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
        else:
            self.Canvas.Pen.Width = 3
            self.Canvas.Pen.Color = UNRESOLVED.clBtnHighlight
        self.Canvas.Pen.Width = 1
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.Canvas.Rectangle(self.colorRect.Left - 1, self.colorRect.Top - 1, self.colorRect.Right + 1, self.colorRect.Bottom + 1)
    
    def fillRectWithColor(self, aRect, aColor):
        bitmap = TBitmap()
        
        bitmap = delphi_compatability.TBitmap().Create()
        try:
            try:
                bitmap.Width = usupport.rWidth(aRect)
                bitmap.Height = usupport.rHeight(aRect)
            except:
                bitmap.Width = 1
                bitmap.Height = 1
            ubmpsupport.setPixelFormatBasedOnScreenForBitmap(bitmap)
            bitmap.Canvas.Brush.Color = aColor
            bitmap.Canvas.FillRect(Rect(0, 0, bitmap.Width, bitmap.Height))
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(bitmap, self.Canvas, aRect)
        finally:
            bitmap.free
    
