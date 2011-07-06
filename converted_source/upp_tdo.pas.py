# unit upp_tdo

from conversion_common import *
import ubmpsupport
import upicktdo
import utdoedit
import udebug
import udomain
import usupport
import uunits
import umath
import updcom
import uturtle
import utdo
import uppanel
import uparams
import uplant
import delphi_compatability

# const
kItemFileName = 1
kItemTdo = 2
kItemTurnLeft = 3
kItemTurnRight = 4
kItemEnlarge = 5
kItemReduce = 6
kTdoSize = 64

#<
#>
#+
#-
class PdTdoParameterPanel(PdParameterPanel):
    def __init__(self):
        self.tdo = KfObject3D()
        self.fileNameRect = TRect()
        self.tdoRect = TRect()
        self.turnLeftRect = TRect()
        self.turnRightRect = TRect()
        self.enlargeRect = TRect()
        self.reduceRect = TRect()
        self.rotateAngle = 0
        self.scale = 0.0
        self.position = TPoint()
        self.editEnabled = false
        self.movingTdo = false
        self.moveStart = TPoint()
        self.moveStartPosition = TPoint()
    
    def create(self, anOwner):
        PdParameterPanel.create(self, anOwner)
        self.tdo = utdo.KfObject3D().create()
        return self
    
    def destroy(self):
        self.tdo.free
        self.tdo = None
    
    def initialize(self):
        self.rotateAngle = 0
        self.scale = 0.2
        self.position = Point(0, 0)
        self.movingTdo = false
    
    def updateEnabling(self):
        PdParameterPanel.updateEnabling(self)
        if (self.plant == None) or (self.readOnly):
            self.editEnabled = false
        else:
            self.editEnabled = true
    
    def updatePlantValues(self):
        pass
        # this won't ever be changed by the simulation, so don't respond 
    
    def updateCurrentValue(self, aFieldIndex):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldThreeDObject):
            self.tdo = self.plant.transferField(umath.kGetField, self.tdo, self.param.fieldNumber, uparams.kFieldThreeDObject, uparams.kNotArray, false, None)
            self.recenterTdo()
        else:
            self.editEnabled = false
    
    def updateDisplay(self):
        if (self.plant != None) and (self.param.fieldType == uparams.kFieldThreeDObject):
            self.Invalidate()
        else:
            self.editEnabled = false
    
    def doMouseDown(self, Sender, Button, Shift, X, Y):
        thePoint = TPoint()
        
        if delphi_compatability.Application.terminated:
            return
        # must always call this first because it sets the focus 
        PdParameterPanel.doMouseDown(self, Sender, Button, Shift, X, Y)
        if (self.editEnabled):
            thePoint = Point(X, Y)
            if delphi_compatability.PtInRect(self.tdoRect, thePoint) and (delphi_compatability.TShiftStateEnum.ssCtrl in Shift):
                #(button = mbRight) then
                self.movingTdo = true
                self.moveStart = thePoint
                self.moveStartPosition = self.position
    
    def doMouseMove(self, Sender, Shift, X, Y):
        if self.movingTdo:
            self.position.X = self.moveStartPosition.X + (X - self.moveStart.X)
            self.position.Y = self.moveStartPosition.Y + (Y - self.moveStart.Y)
            self.Invalidate()
    
    def doMouseUp(self, Sender, Button, Shift, X, Y):
        thePoint = TPoint()
        
        if delphi_compatability.Application.terminated:
            return
        PdParameterPanel.doMouseUp(self, Sender, Button, Shift, X, Y)
        if (self.editEnabled):
            thePoint = Point(X, Y)
            if delphi_compatability.PtInRect(self.fileNameRect, thePoint):
                self.selectedItemIndex = kItemFileName
                self.pickTdo()
            elif delphi_compatability.PtInRect(self.tdoRect, thePoint):
                self.selectedItemIndex = kItemTdo
                if self.movingTdo:
                    self.movingTdo = false
                    self.position.X = self.moveStartPosition.X + (X - self.moveStart.X)
                    self.position.Y = self.moveStartPosition.Y + (Y - self.moveStart.Y)
                    self.moveStart = Point(0, 0)
                    self.Invalidate()
                elif Button == delphi_compatability.TMouseButton.mbLeft:
                    self.pickTdo()
            elif delphi_compatability.PtInRect(self.turnLeftRect, thePoint):
                self.selectedItemIndex = kItemTurnLeft
                self.rotateAngle = self.rotateAngle + 10
            elif delphi_compatability.PtInRect(self.turnRightRect, thePoint):
                self.selectedItemIndex = kItemTurnRight
                self.rotateAngle = self.rotateAngle - 10
            elif delphi_compatability.PtInRect(self.enlargeRect, thePoint):
                self.selectedItemIndex = kItemEnlarge
                self.scale = self.scale + 0.1
                self.recenterTdo()
            elif delphi_compatability.PtInRect(self.reduceRect, thePoint):
                self.selectedItemIndex = kItemReduce
                self.scale = self.scale - 0.1
                self.recenterTdo()
            self.Invalidate()
    
    def doKeyDown(self, sender, key, shift):
        if delphi_compatability.Application.terminated:
            return key
        PdParameterPanel.doKeyDown(self, sender, key, shift)
        if (key == delphi_compatability.VK_RETURN) and (self.editEnabled):
            if self.selectedItemIndex == kItemFileName:
                self.pickTdo()
            elif self.selectedItemIndex == kItemTdo:
                self.pickTdo()
        return key
    
    def pickTdo(self):
        tdoPicker = TPickTdoForm()
        plantName = ""
        
        if (self.tdo == None) or (self.plant == None) or (self.param == None):
            return
        tdoPicker = upicktdo.TPickTdoForm().create(self)
        if tdoPicker == None:
            raise GeneralException.create("Problem: Could not create 3D object chooser window.")
        try:
            plantName = self.plant.getName()
            if tdoPicker.initializeWithTdoParameterAndPlantName(self.tdo, self.param, plantName):
                # if false, user canceled picking a 3D object library
                tdoPicker.ShowModal()
        finally:
            tdoPicker.free
            tdoPicker = None
    
    def maxWidth(self):
        result = 0
        result = umath.intMax(uppanel.kLeftRightGap * 2 + self.labelWidth, uppanel.kLeftRightGap + self.formTextWidth("wwwwwwww.www") + uppanel.kLeftRightGap + kTdoSize + uppanel.kLeftRightGap)
        return result
    
    def minWidth(self, requestedWidth):
        result = 0
        minAllowed = 0
        
        minAllowed = uppanel.kLeftRightGap * 2 + umath.intMax(self.longestLabelWordWidth, self.formTextWidth("wwwwwwww.www") + utdoedit.kBetweenGap + kTdoSize)
        if requestedWidth > minAllowed:
            result = -1
        else:
            result = minAllowed
        return result
    
    def uncollapsedHeight(self):
        result = 0
        result = self.collapsedHeight() + kTdoSize + utdoedit.kBetweenGap + self.textHeight + uppanel.kTopBottomGap * 3
        return result
    
    def maxSelectedItemIndex(self):
        result = 0
        if (not self.param.collapsed) and (self.editEnabled):
            result = kItemReduce
        else:
            result = uppanel.kItemLabel
        return result
    
    def resizeElements(self):
        pass
        # do nothing 
    
    def paint(self):
        rect = TRect()
        
        if delphi_compatability.Application.terminated:
            return
        PdParameterPanel.paint(self)
        if (self.param.collapsed):
            self.drawExtraValueCaptionWithString(self.tdo.getName(), "")
            return
        Rect = self.GetClientRect()
        self.tdoRect.Left = Rect.left + uppanel.kLeftRightGap
        self.tdoRect.Right = self.tdoRect.Left + kTdoSize
        self.tdoRect.Top = self.collapsedHeight() + uppanel.kTopBottomGap
        self.tdoRect.Bottom = self.tdoRect.Top + kTdoSize
        self.fileNameRect.Left = self.tdoRect.Right + uppanel.kLeftRightGap
        self.fileNameRect.Right = self.fileNameRect.Left + self.Canvas.TextWidth(self.tdo.getName())
        self.fileNameRect.Top = self.tdoRect.Top + kTdoSize / 2 - self.textHeight / 2
        self.fileNameRect.Bottom = self.fileNameRect.Top + self.textHeight
        self.turnLeftRect.Left = self.tdoRect.Left + (self.tdoRect.Right - self.tdoRect.Left) / 2 - (self.Canvas.TextWidth(">") * 4 + uppanel.kLeftRightGap * 3) / 2
        self.turnLeftRect.Right = self.turnLeftRect.Left + self.Canvas.TextWidth("<")
        self.turnLeftRect.Top = self.tdoRect.Bottom + utdoedit.kBetweenGap
        self.turnLeftRect.Bottom = self.turnLeftRect.Top + self.textHeight
        self.turnRightRect.Left = self.turnLeftRect.Right + uppanel.kLeftRightGap
        self.turnRightRect.Right = self.turnRightRect.Left + self.Canvas.TextWidth(">")
        self.turnRightRect.Top = self.turnLeftRect.Top
        self.turnRightRect.Bottom = self.turnRightRect.Top + self.textHeight
        self.enlargeRect.Left = self.turnRightRect.Right + uppanel.kLeftRightGap
        self.enlargeRect.Right = self.enlargeRect.Left + self.Canvas.TextWidth("+")
        self.enlargeRect.Top = self.turnLeftRect.Top
        self.enlargeRect.Bottom = self.enlargeRect.Top + self.textHeight
        self.reduceRect.Left = self.enlargeRect.Right + uppanel.kLeftRightGap
        self.reduceRect.Right = self.reduceRect.Left + self.Canvas.TextWidth("-")
        self.reduceRect.Top = self.turnLeftRect.Top
        self.reduceRect.Bottom = self.reduceRect.Top + self.textHeight
        if self.plant != None:
            self.drawText(self.tdo.getName(), self.fileNameRect, true, (self.selectedItemIndex == kItemFileName) and (self.editEnabled), false)
        self.drawText("<", self.turnLeftRect, true, self.selectedItemIndex == kItemTurnLeft, false)
        self.drawText(">", self.turnRightRect, true, self.selectedItemIndex == kItemTurnRight, false)
        self.drawText("+", self.enlargeRect, true, self.selectedItemIndex == kItemEnlarge, false)
        self.drawText("-", self.reduceRect, true, self.selectedItemIndex == kItemReduce, false)
        self.drawTdo()
        if (self.selectedItemIndex != kItemTdo):
            self.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
            self.Canvas.Pen.Width = 1
        else:
            self.Canvas.Pen.Color = UNRESOLVED.clBtnText
            self.Canvas.Pen.Width = 3
        self.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.Canvas.Pen.Width = 1
        self.Canvas.Rectangle(self.tdoRect.Left - 1, self.tdoRect.Top - 1, self.tdoRect.Right + 1, self.tdoRect.Bottom + 1)
    
    def recenterTdo(self):
        turtle = KfTurtle()
        
        if self.plant == None:
            return
        if self.tdo == None:
            return
        turtle = uturtle.KfTurtle.defaultStartUsing()
        try:
            turtle.drawingSurface.pane = None
            # must be after pane and draw options set 
            turtle.reset()
            self.position = self.tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(kTdoSize, kTdoSize), self.scale)
        finally:
            uturtle.KfTurtle.defaultStopUsing()
            turtle = None
    
    def drawTdo(self):
        turtle = KfTurtle()
        bitmap = TBitmap()
        
        if self.plant == None:
            return
        if self.tdo == None:
            return
        # set up clipping bitmap 
        bitmap = delphi_compatability.TBitmap().Create()
        bitmap.Width = kTdoSize
        bitmap.Height = kTdoSize
        bitmap.Canvas.Brush.Color = delphi_compatability.clWhite
        bitmap.Canvas.Rectangle(0, 0, bitmap.Width, bitmap.Height)
        # set up turtle 
        turtle = uturtle.KfTurtle.defaultStartUsing()
        try:
            turtle.drawingSurface.pane = bitmap.Canvas
            turtle.setDrawOptionsForDrawingTdoOnly()
            # must be after pane and draw options set 
            turtle.reset()
            turtle.xyz(self.position.X, self.position.Y, 0)
            try:
                turtle.push()
                turtle.rotateY(self.rotateAngle)
                turtle.drawingSurface.recordingStart()
                self.tdo.draw(turtle, self.scale, "", "", 0, 0)
                turtle.drawingSurface.recordingStop()
                turtle.drawingSurface.recordingDraw()
                turtle.drawingSurface.clearTriangles()
                turtle.pop()
            except Exception, e:
                usupport.messageForExceptionType(e, "PdTdoParameterPanel.drawTdo")
                bitmap.free
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(bitmap, self.Canvas, self.tdoRect)
        finally:
            uturtle.KfTurtle.defaultStopUsing()
            turtle = None
            bitmap.free
    
