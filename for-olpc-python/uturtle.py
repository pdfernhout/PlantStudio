# unit Uturtle

import copy

from conversion_common import *
import delphi_compatability
import utdo
import u3dsupport
import udrawingsurface
import u3dexport

"""
import udebug
import umain
import utravers
import umath
import usupport
import ucollect
"""

# const
kInitialTurtleMatrixStackDepth = 250

#OpenGL,
#if this is defined - turtle will draw axis marks for each line segment
#put spaces before and after the $ to disable
# $ DEFINE DEBUG_TURTLE
# general options 
# record
class PlantDrawOptionsStructure:
    def __init__(self):
        self.sortPolygons = False
        self.drawLines = True
        self.lineContrastIndex = 0
        self.wireFrame = False
        self.straightLinesOnly = False
        self.simpleLeavesOnly = False
        self.drawStems = True
        self.draw3DObjects = True
        self.draw3DObjectsAsRects = False
        self.circlePoints = False
        self.circlePointRadius = 3
        self.sortTdosAsOneItem = False
        self.drawingToMainWindow = False
        self.drawBoundsRectsOnPlantParts = False

#if the DEBUG_TURTLE flag is defined then draw axis information
# PDF PORT Issue
def debugDrawInMillimeters(turtle, mm):
    oldPosition = copy.copy(turtle.currentMatrix.position)
    turtle.currentMatrix.move(turtle.millimetersToPixels(mm))
    newPosition = turtle.currentMatrix.position
    turtle.addToRealBoundsRect(newPosition)

def debugDrawAxis(turtle, pixels):
    oldPosition = copy.copy(turtle.currentMatrix.position)
    turtle.currentMatrix.move(pixels)
    newPosition = turtle.currentMatrix.position
    if turtle.drawOptions.drawStems:
        turtle.drawingSurface.drawLineFromTo(oldPosition, newPosition)

# speed optimizations 
    #for darkerColor
    #temp
    
# ---------------------------------------------------------------------------------- *KfTurtle creating/destroying 
#PDF FIX - may want to think about size of recorded points
class KfTurtle:
    def __init__(self):
        # v1.60final looked at giving hint with plant part name again; still has problem
        # that what you record is only points, and what you need to record is rects
        # it can be done, but the plant parts have to change to record rects, and they
        # have to deal with all their different ways of drawing. not worth doing at this time.
        
        self.matrixStack = []
        self.currentMatrix = u3dsupport.KfMatrix()
        self.currentMatrix.initializeAsUnitMatrix()
        self.matrixStack.append(self.currentMatrix)
        self.numMatrixesUsed = 1
        # start with a bunch of matrixes
        for i in range(0, kInitialTurtleMatrixStackDepth):
            self.matrixStack.append(u3dsupport.KfMatrix())

        self.drawingSurface = udrawingsurface.KfDrawingSurface()
        
        self.scale_pixelsPerMm = 1.0
        
        self.recordedPoints = []

        self.tempPosition = u3dsupport.KfPoint3D()
        self.realBoundsRect = u3dsupport.TRealRect()
        self.drawOptions = PlantDrawOptionsStructure()
        self.writingTo = 0
    
    # 3d file export
    def createFor3DOutput(self, anOutputType, aFileName):
        self.drawingSurface = None
        if anOutputType == u3dexport.kDXF:
            self.drawingSurface = u3dexport.KfDrawingSurfaceForDXF().createWithFileName(aFileName)
        elif anOutputType == u3dexport.kPOV:
            self.drawingSurface = u3dexport.KfDrawingSurfaceForPOV().createWithFileName(aFileName)
        elif anOutputType == u3dexport.k3DS:
            self.drawingSurface = u3dexport.KfDrawingSurfaceFor3DS().createWithFileName(aFileName)
        elif anOutputType == u3dexport.kOBJ:
            self.drawingSurface = u3dexport.KfDrawingSurfaceForOBJ().createWithFileName(aFileName)
        elif anOutputType == u3dexport.kVRML:
            self.drawingSurface = u3dexport.KfDrawingSurfaceForVRML().createWithFileName(aFileName)
        elif anOutputType == u3dexport.kLWO:
            self.drawingSurface = u3dexport.KfDrawingSurfaceForLWO().createWithFileName(aFileName)
        else :
            raise GeneralException.create("KfTurtle.createFor3DOutput: Unrecognized output type")
        return self
    
    def start3DExportFile(self):
        if (self.drawingSurface != None) and (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.startFile()
    
    def end3DExportFile(self):
        if (self.drawingSurface != None) and (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.endFile()
    
    # -------------------------------------------------------------------------- KfTurtle initializing and setting values 
    def reset(self):
        self.numMatrixesUsed = 1
        self.currentMatrix = self.matrixStack[0]
        self.currentMatrix.initializeAsUnitMatrix()
        self.recordedPoints = []
        self.scale_pixelsPerMm = 1.0
        if self.drawingSurface != None:
            self.drawingSurface.fillingTriangles = not self.drawOptions.wireFrame
            self.drawingSurface.drawingLines = self.drawOptions.drawLines
            self.drawingSurface.circlingPoints = self.drawOptions.circlePoints
            self.drawingSurface.lineContrastIndex = self.drawOptions.lineContrastIndex
            self.drawingSurface.circlePointRadius = self.drawOptions.circlePointRadius
            self.drawingSurface.sortTdosAsOneItem = self.drawOptions.sortTdosAsOneItem
            self.drawingSurface.initialize()
    
    def setDrawOptionsForDrawingTdoOnly(self):
        self.drawOptions.draw3DObjects = True
        self.drawOptions.draw3DObjectsAsRects = False
        self.drawOptions.drawLines = True
        self.drawOptions.lineContrastIndex = utdo.kTdoLineContrastIndex
        self.drawOptions.wireFrame = False
        self.drawOptions.sortPolygons = True
        self.drawOptions.sortTdosAsOneItem = False
        self.drawOptions.circlePoints = False
        # when drawing a tdo all by itself, you MUST set the turtle scale to 1.0,
        #    because the tdo multiplies the turtle scale by its own scale (which you are giving it
        #    in the call to draw) 
        # self.setScale_pixelsPerMm(1.0);  actually, this gets done in the reset method
        self.drawingSurface.foreColor = utdo.kTdoForeColor
        self.drawingSurface.backColor = utdo.kTdoBackColor
        self.drawingSurface.lineColor = delphi_compatability.clBlack
    
    def resetBoundsRect(self, basePoint):
        self.realBoundsRect.left = basePoint.X
        self.realBoundsRect.right = basePoint.X
        self.realBoundsRect.top = basePoint.Y
        self.realBoundsRect.bottom = basePoint.Y
    
    def xyz(self, x, y, z):
        self.currentMatrix.position.x = x
        self.currentMatrix.position.y = y
        self.currentMatrix.position.z = z
    
    def setForeColorBackColor(self, frontColor, backColor):
        self.drawingSurface.foreColor = frontColor
        self.drawingSurface.backColor = backColor
    
    def setLineColor(self, aColor):
        self.drawingSurface.lineColor = aColor
    
    def setLineWidth(self, aWidth):
        self.drawingSurface.lineWidth = aWidth * self.scale_pixelsPerMm
        if self.drawingSurface.lineWidth > 16000:
            self.drawingSurface.lineWidth = 16000
    
    def setScale_pixelsPerMm(self, newScale_pixelsPerMm):
        self.scale_pixelsPerMm = newScale_pixelsPerMm
    
    def newTriangleTriangle(self, aPointIndex, bPointIndex, cPointIndex):
        result = u3dsupport.KfTriangle()
        # PDF MAYBE WANT TO COPY?
        result.points[0] = self.recordedPoints[aPointIndex]
        result.points[1] = self.recordedPoints[bPointIndex]
        result.points[2] = self.recordedPoints[cPointIndex]
        return result
    
    def positionCopy(self):
        #suspicious things that call this may not clean up copy
        result = self.currentMatrix.position
        return result
    
    def exportingToFile(self):
        # cfk update this if create any mode that is NOT screen and NOT file
        result = self.writingTo != u3dexport.kScreen
        return result
    
    def writingToDXF(self):
        result = self.writingTo == u3dexport.kDXF
        return result
    
    def writingToPOV(self):
        result = self.writingTo == u3dexport.kPOV
        return result
    
    def writingTo3DS(self):
        result = self.writingTo == u3dexport.k3DS
        return result
    
    def writingToOBJ(self):
        result = self.writingTo == u3dexport.kOBJ
        return result
    
    def writingToVRML(self):
        result = self.writingTo == u3dexport.kVRML
        return result
    
    def writingToLWO(self):
        result = self.writingTo == u3dexport.kLWO
        return result
    
    def fileExportSurface(self):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            result = self.drawingSurface
        else:
            result = None
        return result
    
    def ifExporting_startNestedGroupOfPlantParts(self, groupName, shortName, nestingType):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.startNestedGroupOfPlantParts(groupName, shortName, nestingType)
    
    def ifExporting_endNestedGroupOfPlantParts(self, nestingType):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.endNestedGroupOfPlantParts(nestingType)
    
    def ifExporting_startPlantPart(self, aLongName, aShortName):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.startPlantPart(aLongName, aShortName)
    
    def ifExporting_endPlantPart(self):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.endPlantPart()
    
    def ifExporting_excludeStem(self, length):
        result = False
        if (self.drawingSurface.__class__ is u3dexport.KfDrawingSurfaceForPOV):
            result = (len <= self.drawingSurface.options.pov_minLineLengthToWrite)
        return result
    
    def ifExporting_exclude3DObject(self, scale):
        result = False
        if (self.drawingSurface.__class__ is u3dexport.KfDrawingSurfaceForPOV):
            result = (scale <= self.drawingSurface.options.pov_minTdoScaleToWrite)
        return result
    
    def ifExporting_startStemSegment(self, aLongName, aShortName, color, width, index):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.startStemSegment(aLongName, aShortName, color, width, index)
    
    def ifExporting_endStemSegment(self):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.endStemSegment()
    
    def ifExporting_stemCylinderFaces(self):
        result = 0
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            result = self.drawingSurface.options.stemCylinderFaces
        return result
    
    def drawFileExportPipeFaces(self, startPoints, endPoints, faces, segmentNumber):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.drawPipeFaces(startPoints, endPoints, faces, segmentNumber)
    
    def ifExporting_start3DObject(self, aLongName, aShortName, color, index):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.start3DObject(aLongName, aShortName, color, index)
    
    def ifExporting_end3DObject(self):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            self.drawingSurface.end3DObject()
    
    # ---------------------------------------------------------------------------------- KfTurtle returning values 
    def millimetersToPixels(self, mm):
        result = mm * self.scale_pixelsPerMm
        return result
    
    def angleX(self):
        result = self.currentMatrix.angleX()
        return result
    
    def angleY(self):
        result = self.currentMatrix.angleY()
        return result
    
    def angleZ(self):
        result = self.currentMatrix.angleZ()
        return result
    
    def lineColor(self):
        result = self.drawingSurface.lineColor
        return result
    
    def lineWidth(self):
        result = self.drawingSurface.lineWidth
        return result
    
    def position(self):
        self.tempPosition = self.currentMatrix.position
        result = self.tempPosition
        return result
    
    def boundsRect(self):
        result = delphi_compatability.TRect()
        try:
            result.Top = intround(self.realBoundsRect.top)
            result.Left = intround(self.realBoundsRect.left)
            result.Bottom = intround(self.realBoundsRect.bottom)
            result.Right = intround(self.realBoundsRect.right)
        except:
            #might want to be more precise in assigning a rect
            result.Top = -32767
            result.Left = -32767
            result.Bottom = 32767
            result.Right = 32767
        return result
    
    # ---------------------------------------------------------------------------------- KfTurtle recording 
    def startRecording(self):
        self.recordedPoints = []
        self.recordPosition()
    
    def clearRecording(self):
        self.recordedPoints = []
    
    def recordPosition(self):
        if len(self.recordedPoints) >= utdo.kMaximumRecordedPoints:
            return
        newPoint = copy.copy(self.currentMatrix.position)
        self.recordedPoints.append(newPoint)
        self.addToRealBoundsRect(newPoint)
    
    def recordPositionPoint(self, aPoint):
        if len(self.recordedPoints) >= utdo.kMaximumRecordedPoints:
            return
        self.recordedPoints.append(aPoint)
        self.addToRealBoundsRect(aPoint)
    
    def transformAndRecord(self, originalPoint3D, theScale_pixelsPerMm):
        #transform and scale point and record the new location without moving
        result = copy.copy(originalPoint3D)
        u3dsupport.KfPoint3D_scaleBy(result, theScale_pixelsPerMm * self.scale_pixelsPerMm)
        self.currentMatrix.transform(result)
        self.recordPositionPoint(result)
        return result
    
    def moveAndRecordScale(self, originalPoint3D, theScale_pixelsPerMm):
        aPoint3d = copy.copy(originalPoint3D)
        u3dsupport.KfPoint3D_scaleBy(aPoint3d, theScale_pixelsPerMm * self.scale_pixelsPerMm)
        self.currentMatrix.transform(aPoint3d)
        self.currentMatrix.position = aPoint3d
        self.recordPositionPoint(aPoint3d)
    
    # ---------------------------------------------------------------------------------- KfTurtle moving 
    def moveInMillimeters(self, mm):
        self.currentMatrix.move(self.millimetersToPixels(mm))
    
    def moveInMillimetersAndRecord(self, mm):
        self.currentMatrix.move(self.millimetersToPixels(mm))
        self.recordPosition()
    
    def moveInPixels(self, pixels):
        self.currentMatrix.move(pixels)
    
    def moveInPixelsAndRecord(self, pixels):
        self.currentMatrix.move(pixels)
        self.recordPosition()
    
    # ---------------------------------------------------------------------------------- KfTurtle drawing 
    def drawInPixels(self, pixels):
        oldPosition = copy.copy(self.currentMatrix.position)
        self.currentMatrix.move(pixels)
        newPosition = self.currentMatrix.position
        if self.drawOptions.drawStems:
            self.drawingSurface.drawLineFromTo(oldPosition, newPosition)
        self.addToRealBoundsRect(newPosition)
    
    # PDF PORT added to deal with alternatives
    # PDF PORT --Alternative -- changed name of alternative function -- Will not be called
    def drawInMillimeters_debug(self, mm):
        oldColor = self.drawingSurface.lineColor
        oldWidth = self.drawingSurface.lineWidth
        self.drawingSurface.lineWidth = 2
        self.drawingSurface.lineColor = delphi_compatability.clRed
        self.push()
        #will flip so draw Y (sic)
        self.rotateZ(64)
        debugDrawAxis(self, 100.0)
        self.pop()
        self.drawingSurface.lineWidth = 1
        self.drawingSurface.lineColor = delphi_compatability.clBlue
        self.push()
        #will flip so draw Z (sic)
        self.rotateY(64)
        debugDrawAxis(self, 100.0)
        self.pop()
        self.drawingSurface.lineColor = oldColor
        self.drawingSurface.lineWidth = oldWidth
        debugDrawInMillimeters(self, mm)
    
    def drawInMillimeters(self, mm, partID):
        result = None
        oldPosition = copy.copy(self.currentMatrix.position)
        self.currentMatrix.move(self.millimetersToPixels(mm))
        newPosition = self.currentMatrix.position
        if self.drawOptions.drawStems:
            result = self.drawingSurface.drawLineFromTo(oldPosition, newPosition)
            if result != None:
                result.plantPartID = partID
        self.addToRealBoundsRect(newPosition)
        return result
    
    def drawTriangleFromIndexes(self, aPointIndex, bPointIndex, cPointIndex, partID):
        #drawing surface takes over ownership of triangle
        result = self.drawingSurface.allocateTriangle()
        self.drawingSurface.lineWidth = 1.0
        result.points[0] = self.recordedPoints[aPointIndex - 1]
        result.points[1] = self.recordedPoints[bPointIndex - 1]
        result.points[2] = self.recordedPoints[cPointIndex - 1]
        result.plantPartID = partID
        self.drawingSurface.drawLastTriangle()
        return result
    
    def drawTrianglesFromBoundsRect(self, boundsRect):
        #drawing surface takes over ownership of triangle
        self.drawingSurface.lineWidth = 1.0
        aTriangle = self.drawingSurface.allocateTriangle()
        aTriangle.points[0].x = boundsRect.Left
        aTriangle.points[0].y = boundsRect.Top
        aTriangle.points[1].x = boundsRect.Right
        aTriangle.points[1].y = boundsRect.Top
        aTriangle.points[2].x = boundsRect.Left
        aTriangle.points[2].y = boundsRect.Bottom
        self.drawingSurface.drawLastTriangle()
        aTriangle = self.drawingSurface.allocateTriangle()
        aTriangle.points[0].x = boundsRect.Left
        aTriangle.points[0].y = boundsRect.Bottom
        aTriangle.points[1].x = boundsRect.Right
        aTriangle.points[1].y = boundsRect.Top
        aTriangle.points[2].x = boundsRect.Right
        aTriangle.points[2].y = boundsRect.Bottom
        self.drawingSurface.drawLastTriangle()
    
    def drawTriangle(self):
        if len(self.recordedPoints) != 3:
            raise GeneralException.create("Problem: Triangle made without three points in method KfTurtle.drawTriangle.")
        #drawing surface owns triangle
        triangle = self.drawingSurface.allocateTriangle()
        triangle.points[0] = self.recordedPoints[0]
        triangle.points[1] = self.recordedPoints[1]
        triangle.points[2] = self.recordedPoints[2]
        self.drawingSurface.drawLastTriangle()
        self.recordedPoints = []
    
    def addToRealBoundsRect(self, aPoint):
        if aPoint.x < self.realBoundsRect.left:
            self.realBoundsRect.left = aPoint.x
        elif aPoint.x > self.realBoundsRect.right:
            self.realBoundsRect.right = aPoint.x
        if aPoint.y < self.realBoundsRect.top:
            self.realBoundsRect.top = aPoint.y
        elif aPoint.y > self.realBoundsRect.bottom:
            self.realBoundsRect.bottom = aPoint.y
    
    # ---------------------------------------------------------------------------------- KfTurtle stack 
    def push(self):
        if self.numMatrixesUsed >= len(self.matrixStack):
            self.matrixStack.append(self.currentMatrix.deepCopy())
        else:
            self.currentMatrix.copyTo(self.matrixStack[self.numMatrixesUsed])
        self.numMatrixesUsed += 1
        self.currentMatrix = self.matrixStack[self.numMatrixesUsed - 1]
    
    def pop(self):
        if self.numMatrixesUsed < 1:
            return
        self.numMatrixesUsed -= 1
        self.currentMatrix = self.matrixStack[self.numMatrixesUsed - 1]
    
    def stackSize(self):
        result = self.numMatrixesUsed
        return result
    
    # ---------------------------------------------------------------------------------- KfTurtle rotating 
    def rotateX(self, angle):
        self.currentMatrix.rotateX(angle)
    
    def rotateY(self, angle):
        self.currentMatrix.rotateY(angle)
    
    def rotateZ(self, angle):
        self.currentMatrix.rotateZ(angle)
    
    # ---------------------------------------------------------------------------------- KfTurtle defaulting 
    #where the default turtle is used need a try..finally
    #to ensure defaultStopUsing is called no matter what
    def defaultStartUsing(self):
        global gDefaultTurtleInUse
        if gDefaultTurtleInUse:
            raise GeneralException.create("Problem: turtle is already in use; in method KfTurtle.defaultStartUsing.")
        gDefaultTurtleInUse = True
        result = gDefaultTurtle
        return result
    defaultStartUsing = classmethod(defaultStartUsing)
    
    def defaultStopUsing(self):
        global gDefaultTurtleInUse
        gDefaultTurtleInUse = False
    defaultStopUsing = classmethod(defaultStopUsing)

################################## INITIALIZATION
# var
gDefaultTurtleInUse = False
gDefaultTurtle = KfTurtle()
import gtkdrawingsurface
gDefaultTurtle.drawingSurface = gtkdrawingsurface.GTKDrawingSurface()
