# unit Upp_hed

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

class PdHeaderParameterPanel(PdParameterPanel):
    def __init__(self):
        pass
    
    def collapseOrExpand(self, y):
        if (self.Owner != None):
            umain.TMainForm(self.Owner).collapseOrExpandParameterPanelsUntilNextHeader(self)
        #don't need to change height
        self.param.collapsed = not self.param.collapsed
    
    def collapse(self):
        if self.param.collapsed:
            return
        if (self.Owner != None):
            umain.TMainForm(self.Owner).collapseOrExpandParameterPanelsUntilNextHeader(self)
        self.param.collapsed = true
    
    def expand(self):
        if not self.param.collapsed:
            return
        if (self.Owner != None):
            umain.TMainForm(self.Owner).collapseOrExpandParameterPanelsUntilNextHeader(self)
        self.param.collapsed = false
    
    def initialize(self):
        pass
        # nothing 
    
    def updateEnabling(self):
        PdParameterPanel.updateEnabling(self)
        # grey out if no plant, but nothing else 
    
    def updatePlantValues(self):
        pass
        # nothing 
    
    def updateCurrentValue(self, aFieldIndex):
        pass
        # nothing 
    
    def updateDisplay(self):
        pass
        # nothing 
    
    def doMouseDown(self, Sender, Button, Shift, X, Y):
        # must always call this first because it sets the focus 
        PdParameterPanel.doMouseDown(self, Sender, Button, Shift, X, Y)
        # nothing else; inherited will do collapse/expand 
    
    def doKeyDown(self, sender, key, shift):
        PdParameterPanel.doKeyDown(self, sender, key, shift)
        # nothing else; inherited will do collapse/expand 
        return key
    
    def maxWidth(self):
        result = 0
        result = uppanel.kLeftRightGap * 2 + self.longestLabelWordWidth
        return result
    
    def minWidth(self, requestedWidth):
        result = 0
        minAllowed = 0
        
        minAllowed = uppanel.kLeftRightGap * 2 + self.longestLabelWordWidth
        if requestedWidth > minAllowed:
            result = -1
        else:
            result = minAllowed
        return result
    
    def uncollapsedHeight(self):
        result = 0
        result = self.collapsedHeight()
        return result
    
    def maxSelectedItemIndex(self):
        result = 0
        result = uppanel.kItemLabel
        return result
    
    def resizeElements(self):
        pass
        # do nothing 
    
    def paint(self):
        fullRect = TRect()
        
        if delphi_compatability.Application.terminated:
            return
        # copied from TCustomPanel.paint and location of caption text changed 
        # can't call inherited paint because it wants to put the caption in the middle 
        self.fillWithBevels()
        fullRect = self.GetClientRect()
        self.Canvas.Font = self.Font
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.labelRect.Left = fullRect.Left + uppanel.kLeftRightGap + uppanel.kArrowPictureSize + udebug.kBetweenGap * 2
        self.labelRect.Right = self.labelRect.Left + self.Width - uppanel.kLeftRightGap * 2
        self.labelRect.Top = fullRect.Top + 2
        self.labelRect.Bottom = self.labelRect.Top + self.textHeight
        #  with labelRect do
        #      begin
        #      right := fullRect.right - kleftRightGap * 4;
        #      left := right - textWidth(caption);
        #      top := fullRect.top + 2;
        #      bottom := top + self.textHeight;
        #      end;  
        self.wrappedLabelHeight = self.drawText(self.Caption, self.labelRect, false, false, false)
        self.pictureRect.Left = fullRect.Left + uppanel.kLeftRightGap
        self.pictureRect.Right = self.pictureRect.Left + uppanel.kArrowPictureSize
        self.pictureRect.Top = self.labelRect.Top + 1
        self.pictureRect.Bottom = self.pictureRect.Top + uppanel.kArrowPictureSize
        if self.plant != None:
            if self.param.collapsed:
                self.Canvas.Draw(self.pictureRect.Left, self.pictureRect.Top, umain.MainForm.paramPanelClosedArrowImage.Picture.Bitmap)
            else:
                self.Canvas.Draw(self.pictureRect.Left, self.pictureRect.Top, umain.MainForm.paramPanelOpenArrowImage.Picture.Bitmap)
        if (self.selectedItemIndex == uppanel.kItemLabel):
            self.Canvas.Rectangle(self.pictureRect.Left, self.pictureRect.Top, self.pictureRect.Right, self.pictureRect.Bottom)
        #
        #    if plant <> nil then
        #      begin
        #      pen.width := 1;
        #      pen.color := clBlue;
        #      moveTo({pictureRect.right + kLeftRightGap * 2}labelRect.left + textWidth(caption) + kLeftRightGap * 2,
        #        labelRect.top + rHeight(labelRect) div 2 - pen.width div 2);
        #      lineTo({labelRect.left - kLeftRightGap * 2}fullRect.right - kLeftRightGap * 2,
        #        labelRect.top + rHeight(labelRect) div 2 - pen.width div 2);
        #      end;
        #      
    
    def fillWithBevels(self):
        fullRect = TRect()
        TopColor = TColor()
        BottomColor = TColor()
        
        # PDF PORT -- moved nested function inline
        #procedure AdjustColors(Bevel: TPanelBevel);
        #  begin
        #  TopColor := clBtnHighlight;
        #  if Bevel = bvLowered then TopColor := clBtnShadow;
        #  BottomColor := clBtnShadow;
        #  if Bevel = bvLowered then BottomColor := clBtnHighlight;
        #  end;
        fullRect = self.GetClientRect()
        if self.plant != None:
            self.Canvas.Brush.Color = delphi_compatability.clNavy
        else:
            self.Canvas.Brush.Color = UNRESOLVED.clBtnShadow
        self.Canvas.FillRect(fullRect)
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        if self.BevelOuter != UNRESOLVED.bvNone:
            #AdjustColors(BevelOuter);
            TopColor = UNRESOLVED.clBtnHighlight
            if self.BevelOuter == UNRESOLVED.bvLowered:
                TopColor = UNRESOLVED.clBtnShadow
            BottomColor = UNRESOLVED.clBtnShadow
            if self.BevelOuter == UNRESOLVED.bvLowered:
                BottomColor = UNRESOLVED.clBtnHighlight
            UNRESOLVED.Frame3D(self.Canvas, fullRect, TopColor, BottomColor, self.BevelWidth)
        UNRESOLVED.Frame3D(self.Canvas, fullRect, self.Color, self.Color, self.BorderWidth)
        if self.BevelInner != UNRESOLVED.bvNone:
            UNRESOLVED.AdjustColors(self.BevelInner)
            TopColor = UNRESOLVED.clBtnHighlight
            if self.BevelInner == UNRESOLVED.bvLowered:
                TopColor = UNRESOLVED.clBtnShadow
            BottomColor = UNRESOLVED.clBtnShadow
            if self.BevelInner == UNRESOLVED.bvLowered:
                BottomColor = UNRESOLVED.clBtnHighlight
            UNRESOLVED.Frame3D(self.Canvas, fullRect, TopColor, BottomColor, self.BevelWidth)
    
