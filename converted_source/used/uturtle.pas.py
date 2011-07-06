# unit Uturtle

from conversion_common import *
import udebug
import umain
import utravers
import umath
import usupport
import u3dexport
import u3dsupport
import udrawingsurface
import utdo
import ucollect
import delphi_compatability

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
        self.sortPolygons = false
        self.drawLines = false
        self.lineContrastIndex = 0
        self.wireFrame = false
        self.straightLinesOnly = false
        self.simpleLeavesOnly = false
        self.drawStems = false
        self.draw3DObjects = false
        self.draw3DObjectsAsRects = false
        self.circlePoints = false
        self.circlePointRadius = 0
        self.sortTdosAsOneItem = false
        self.drawingToMainWindow = false
        self.drawBoundsRectsOnPlantParts = false

# var
gDefaultTurtle = KfTurtle()
gDefaultTurtleInUse = false

#if the DEBUG_TURTLE flag is defined then draw axis information
# PDF PORT Issue
def debugDrawInMillimeters(turtle, mm):
    oldPosition = KfPoint3d()
    newPosition = KfPoint3d()
    
    oldPosition = turtle.currentMatrix.position
    turtle.currentMatrix.move(turtle.millimetersToPixels(mm))
    newPosition = turtle.currentMatrix.position
    turtle.addToRealBoundsRect(newPosition)

def debugDrawAxis(turtle, pixels):
    oldPosition = KfPoint3d()
    newPosition = KfPoint3d()
    
    oldPosition = turtle.currentMatrix.position
    turtle.currentMatrix.move(pixels)
    newPosition = turtle.currentMatrix.position
    if turtle.drawOptions.drawStems:
        turtle.drawingSurface.drawLineFromTo(oldPosition, newPosition)

# speed optimizations 
#PDF FIX - may want to think about size of recorded points
class KfTurtle(TObject):
    def __init__(self):
        self.matrixStack = TListCollection()
        self.numMatrixesUsed = 0L
        self.currentMatrix = KfMatrix()
        self.recordedPoints = [0] * (range(0, utdo.kMaximumRecordedPoints + 1) + 1)
        self.recordedPointsInUse = 0L
        self.scale_pixelsPerMm = 0.0
        self.drawingSurface = KfDrawingSurface()
        self.tempPosition = KfPoint3d()
        self.realBoundsRect = TRealRect()
        self.drawOptions = PlantDrawOptionsStructure()
        self.writingTo = 0
    
    #for darkerColor
    #temp
    # ---------------------------------------------------------------------------------- *KfTurtle creating/destroying 
    def create(self):
        i = 0L
        
        TObject.create(self)
        # v1.60final looked at giving hint with plant part name again; still has problem
        # that what you record is only points, and what you need to record is rects
        # it can be done, but the plant parts have to change to record rects, and they
        # have to deal with all their different ways of drawing. not worth doing at this time.
        self.matrixStack = ucollect.TListCollection().Create()
        self.currentMatrix = u3dsupport.KfMatrix.create
        self.currentMatrix.initializeAsUnitMatrix()
        self.matrixStack.Add(self.currentMatrix)
        self.numMatrixesUsed = 1
        for i in range(0, kInitialTurtleMatrixStackDepth + 1):
            #start with a bunch of matrixes
            self.matrixStack.Add(u3dsupport.KfMatrix.create)
        self.recordedPointsInUse = 0
        self.drawingSurface = udrawingsurface.KfDrawingSurface().create()
        self.scale_pixelsPerMm = 1.0
        return self
    
    def destroy(self):
        self.matrixStack.free
        self.matrixStack = None
        self.drawingSurface.free
        self.drawingSurface = None
        TObject.destroy(self)
    
    # 3d file export
    def createFor3DOutput(self, anOutputType, aFileName):
        self.create()
        #already created
        self.drawingSurface.free
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
            (self.drawingSurface as u3dexport.KfFileExportSurface).startFile()
    
    def end3DExportFile(self):
        if (self.drawingSurface != None) and (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).endFile()
    
    # -------------------------------------------------------------------------- KfTurtle initializing and setting values 
    def reset(self):
        self.numMatrixesUsed = 1
        self.currentMatrix = self.matrixStack.Items[0]
        self.currentMatrix.initializeAsUnitMatrix()
        self.recordedPointsInUse = 0
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
        self.drawOptions.draw3DObjects = true
        self.drawOptions.draw3DObjectsAsRects = false
        self.drawOptions.drawLines = true
        self.drawOptions.lineContrastIndex = utdo.kTdoLineContrastIndex
        self.drawOptions.wireFrame = false
        self.drawOptions.sortPolygons = true
        self.drawOptions.sortTdosAsOneItem = false
        self.drawOptions.circlePoints = false
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
        result = KfTriangle()
        result = u3dsupport.KfTriangle.create
        result.points[0] = self.recordedPoints[aPointIndex]
        result.points[1] = self.recordedPoints[bPointIndex]
        result.points[2] = self.recordedPoints[cPointIndex]
        return result
    
    def positionCopy(self):
        result = KfPoint3D()
        #suspicious things that call this may not clean up copy
        result = self.currentMatrix.position
        return result
    
    def exportingToFile(self):
        result = false
        # cfk update this if create any mode that is NOT screen and NOT file
        result = self.writingTo != u3dexport.kScreen
        return result
    
    def writingToDXF(self):
        result = false
        result = self.writingTo == u3dexport.kDXF
        return result
    
    def writingToPOV(self):
        result = false
        result = self.writingTo == u3dexport.kPOV
        return result
    
    def writingTo3DS(self):
        result = false
        result = self.writingTo == u3dexport.k3DS
        return result
    
    def writingToOBJ(self):
        result = false
        result = self.writingTo == u3dexport.kOBJ
        return result
    
    def writingToVRML(self):
        result = false
        result = self.writingTo == u3dexport.kVRML
        return result
    
    def writingToLWO(self):
        result = false
        result = self.writingTo == u3dexport.kLWO
        return result
    
    def fileExportSurface(self):
        result = KfFileExportSurface()
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            result = self.drawingSurface as u3dexport.KfFileExportSurface
        else:
            result = None
        return result
    
    def ifExporting_startNestedGroupOfPlantParts(self, groupName, shortName, nestingType):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).startNestedGroupOfPlantParts(groupName, shortName, nestingType)
    
    def ifExporting_endNestedGroupOfPlantParts(self, nestingType):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).endNestedGroupOfPlantParts(nestingType)
    
    def ifExporting_startPlantPart(self, aLongName, aShortName):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).startPlantPart(aLongName, aShortName)
    
    def ifExporting_endPlantPart(self):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).endPlantPart()
    
    def ifExporting_excludeStem(self, length):
        result = false
        result = false
        if (self.drawingSurface.__class__ is u3dexport.KfDrawingSurfaceForPOV):
            result = (len <= (self.drawingSurface as u3dexport.KfDrawingSurfaceForPOV).options.pov_minLineLengthToWrite)
        return result
    
    def ifExporting_exclude3DObject(self, scale):
        result = false
        result = false
        if (self.drawingSurface.__class__ is u3dexport.KfDrawingSurfaceForPOV):
            result = (scale <= (self.drawingSurface as u3dexport.KfDrawingSurfaceForPOV).options.pov_minTdoScaleToWrite)
        return result
    
    def ifExporting_startStemSegment(self, aLongName, aShortName, color, width, index):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).startStemSegment(aLongName, aShortName, color, width, index)
    
    def ifExporting_endStemSegment(self):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).endStemSegment()
    
    def ifExporting_stemCylinderFaces(self):
        result = 0
        result = 0
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            result = (self.drawingSurface as u3dexport.KfFileExportSurface).options.stemCylinderFaces
        return result
    
    def drawFileExportPipeFaces(self, startPoints, endPoints, faces, segmentNumber):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).drawPipeFaces(startPoints, endPoints, faces, segmentNumber)
    
    def ifExporting_start3DObject(self, aLongName, aShortName, color, index):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).start3DObject(aLongName, aShortName, color, index)
    
    def ifExporting_end3DObject(self):
        if (self.drawingSurface.__class__ is u3dexport.KfFileExportSurface):
            (self.drawingSurface as u3dexport.KfFileExportSurface).end3DObject()
    
    # ---------------------------------------------------------------------------------- KfTurtle returning values 
    def millimetersToPixels(self, mm):
        result = 0.0
        result = mm * self.scale_pixelsPerMm
        return result
    
    def angleX(self):
        result = 0
        result = self.currentMatrix.angleX()
        return result
    
    def angleY(self):
        result = 0
        result = self.currentMatrix.angleY()
        return result
    
    def angleZ(self):
        result = 0
        result = self.currentMatrix.angleZ()
        return result
    
    def lineColor(self):
        result = TColor()
        result = self.drawingSurface.lineColor
        return result
    
    def lineWidth(self):
        result = 0.0
        result = self.drawingSurface.lineWidth
        return result
    
    def position(self):
        result = KfPoint3d()
        self.tempPosition = self.currentMatrix.position
        result = self.tempPosition
        return result
    
    def boundsRect(self):
        result = TRect()
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
        self.recordedPointsInUse = 0
        self.recordPosition()
    
    def clearRecording(self):
        self.recordedPointsInUse = 0
    
    def recordPosition(self):
        newPoint = KfPoint3D()
        
        if self.recordedPointsInUse >= utdo.kMaximumRecordedPoints:
            return
        newPoint = self.currentMatrix.position
        self.recordedPoints[self.recordedPointsInUse] = newPoint
        self.recordedPointsInUse += 1
        self.addToRealBoundsRect(newPoint)
    
    def recordPositionPoint(self, aPoint):
        if self.recordedPointsInUse >= utdo.kMaximumRecordedPoints:
            return
        self.recordedPoints[self.recordedPointsInUse] = aPoint
        self.recordedPointsInUse += 1
        self.addToRealBoundsRect(aPoint)
    
    def transformAndRecord(self, originalPoint3D, theScale_pixelsPerMm):
        result = KfPoint3d()
        #transform and scale point and record the new location without moving
        result = originalPoint3D
        utdo.KfPoint3D_scaleBy(result, theScale_pixelsPerMm * self.scale_pixelsPerMm)
        self.currentMatrix.transform(result)
        self.recordPositionPoint(result)
        return result
    
    def moveAndRecordScale(self, originalPoint3D, theScale_pixelsPerMm):
        aPoint3d = KfPoint3D()
        
        aPoint3d = originalPoint3D
        utdo.KfPoint3D_scaleBy(aPoint3d, theScale_pixelsPerMm * self.scale_pixelsPerMm)
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
        oldPosition = KfPoint3d()
        newPosition = KfPoint3d()
        
        oldPosition = self.currentMatrix.position
        self.currentMatrix.move(pixels)
        newPosition = self.currentMatrix.position
        if self.drawOptions.drawStems:
            self.drawingSurface.drawLineFromTo(oldPosition, newPosition)
        self.addToRealBoundsRect(newPosition)
    
    # PDF PORT added to deal with alternatives
    # PDF PORT --Alternative -- changed name of alternative function -- Will not be called
    def drawInMillimeters_debug(self, mm):
        oldColor = TColorRef()
        oldWidth = 0.0
        
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
        result = KfTriangle()
        oldPosition = KfPoint3d()
        newPosition = KfPoint3d()
        
        result = None
        oldPosition = self.currentMatrix.position
        self.currentMatrix.move(self.millimetersToPixels(mm))
        newPosition = self.currentMatrix.position
        if self.drawOptions.drawStems:
            result = self.drawingSurface.drawLineFromTo(oldPosition, newPosition)
            if result != None:
                result.plantPartID = partID
        self.addToRealBoundsRect(newPosition)
        return result
    
    def drawTriangleFromIndexes(self, aPointIndex, bPointIndex, cPointIndex, partID):
        result = KfTriangle()
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
        aTriangle = KfTriangle()
        
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
        triangle = KfTriangle()
        
        if self.recordedPointsInUse != 3:
            raise GeneralException.create("Problem: Triangle made without three points in method KfTurtle.drawTriangle.")
        #drawing surface owns triangle
        triangle = self.drawingSurface.allocateTriangle()
        triangle.points[0] = self.recordedPoints[0]
        triangle.points[1] = self.recordedPoints[1]
        triangle.points[2] = self.recordedPoints[2]
        self.drawingSurface.drawLastTriangle()
        self.recordedPointsInUse = 0
    
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
        if self.numMatrixesUsed >= self.matrixStack.Count:
            self.matrixStack.Add(self.currentMatrix.deepCopy())
        else:
            self.currentMatrix.copyTo(u3dsupport.KfMatrix(self.matrixStack.Items[self.numMatrixesUsed]))
        self.numMatrixesUsed += 1
        self.currentMatrix = self.matrixStack.Items[self.numMatrixesUsed - 1]
    
    def pop(self):
        if self.numMatrixesUsed < 1:
            return
        self.numMatrixesUsed -= 1
        self.currentMatrix = self.matrixStack.Items[self.numMatrixesUsed - 1]
    
    def stackSize(self):
        result = 0L
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
        result = KfTurtle()
        if gDefaultTurtleInUse:
            raise GeneralException.create("Problem: turtle is already in use; in method KfTurtle.defaultStartUsing.")
        gDefaultTurtleInUse = true
        result = gDefaultTurtle
        return result
    
    def defaultStopUsing(self):
        gDefaultTurtleInUse = false
    
    def defaultAllocate(self):
        gDefaultTurtle = None
        gDefaultTurtle = KfTurtle().create()
        gDefaultTurtleInUse = false
    
    def defaultFree(self):
        gDefaultTurtle.free
        gDefaultTurtle = None
    
#need to default free somewhere in project
