# unit Udrawingsurface

import u3dsupport
import delphi_compatability
from conversion_common import *

#import utdo
#import ucollect

# const
kInitialDrawingSurfaceTriangles = 1000


# ----------------------------------------------------------------------------- *KfDrawingSurface creating/destroying 

class KfDrawingSurface:
    def __init__(self):
        self.drawingContext = None
        self.lineContrastIndex = 0
        self.drawingLines = False
        self.circlingPoints = False
        self.foreColor = delphi_compatability.EmptyColor
        self.backColor = delphi_compatability.EmptyColor
        self.lineColor = delphi_compatability.EmptyColor
        self.circleColor = delphi_compatability.EmptyColor
        self.triangles = []
        self.recording = False
        self.lineWidth = 0.0
        self.circlePointRadius = 0
        self.sortTdosAsOneItem = False
    
        self.triangles = []
        self.fillingTriangles = True
        self.initialize()
        # start with a bunch of triangles 
        for i in range(0, kInitialDrawingSurfaceTriangles + 1):
            self.triangles.append(u3dsupport.KfTriangle())
    
    def setDrawingContext(self, drawingContext):
        self.drawingContext = drawingContext

    def initialize(self):
        #backColor := clLtGray;
        #  foreColor := clLtGray;
        #  lineColor := clLtGray;
        self.lineWidth = 1.0
        self.recording = False
        self.clearTriangles()
        #if self.drawingContext:
        #    if self.fillingTriangles:
        #        self.drawingContextUseSolidBrush()
        #    else:
        #        self.drawingContextUseClearBrush()
    
    # ----------------------------------------------------------------------------- KfDrawingSurface managing triangles 
    def clearTriangles(self):
        self.triangles = []
    
    def plantPartIDForPoint(self, point):
        points = []
        for i in range(2):
            points.append(u3dsupport.KfPoint3D())

        x = point.x
        y = point.y
        result = -1
        closestDistanceSoFar = 0
        closestPartID = -1
        for triangle in self.triangles:
            if triangle.isLine:
                centerX = (triangle.points[0].x + triangle.points[1].x) / 2.0
                centerY = (triangle.points[0].y + triangle.points[1].y) / 2.0
                thisDistance = (centerX - x) * (centerX - x) + (centerY - y) * (centerY - y)
                if (closestPartID == -1) or (thisDistance < closestDistanceSoFar):
                    closestDistanceSoFar = thisDistance
                    closestPartID = triangle.plantPartID
            else:
                points[0].X = intround(triangle.points[0].x)
                points[0].Y = intround(triangle.points[0].y)
                points[1].X = intround(triangle.points[1].x)
                points[1].Y = intround(triangle.points[1].y)
                points[2].X = intround(triangle.points[2].x)
                points[2].Y = intround(triangle.points[2].y)
                if u3dsupport.pointInTriangle(point, points):
                    result = triangle.plantPartID
                    return result
        result = closestPartID
        return result
    
    def allocateTriangle(self):
        result = u3dsupport.KfTriangle()
        self.triangles.append(result)
        return result
    
    def sortTrianglesConsideringTdos(self):
        if not self.triangles:
            return
        if self.sortTdosAsOneItem:
            for triangle in self.triangles:
                if not triangle.isLine:
                    oldValue = triangle.zForSorting
                    if triangle.tdo != None:
                        try:
                            # the 0.01 is to keep the polygons inside the tdo in order but still (usually) separate from other tdos
                            # could produce errors if the z value is really small already
                            triangle.zForSorting = triangle.tdo.zForSorting + triangle.zForSorting * 0.01
                        except:
                            triangle.zForSorting = oldValue
                    # have to clear out tdo pointer afterward because triangles are reused
                    triangle.tdo = None
        self.sortTriangles(0, len(self.triangles)-1)
    
    def sortTriangles(self, left, right):
        if right > left:
            z = self.triangles[right].zForSorting
            i = left - 1
            j = right
            while True:
                while 1:
                    i = i + 1
                    if not self.triangles[i].zForSorting < z:
                        break
                while 1:
                    j = j - 1
                    if (j < i) or (not self.triangles[j].zForSorting > z):
                        break
                if i >= j:
                    break
                self.triangles[i], self.triangles[j] = self.triangles[j], self.triangles[i]
            self.triangles[i], self.triangles[right] = self.triangles[right], self.triangles[i]
            self.sortTriangles(left, j)
            self.sortTriangles(i + 1, right)
    
    # ----------------------------------------------------------------------------- KfDrawingSurface drawing 
    def trianglesDraw(self):
        for triangle in self.triangles:
            self.basicDrawTriangle(triangle)
    
    def drawLineFromTo(self, startPoint, endPoint):
        result = None
        if self.recording:
            #store triangle
            triangle = self.allocateTriangle()
            triangle.points[0] = startPoint
            triangle.points[1] = endPoint
            triangle.isLine = True
            #need to handle drawing surface colors
            triangle.foreColor = self.foreColor
            triangle.backColor = self.backColor
            triangle.lineColor = self.lineColor
            triangle.lineWidth = self.lineWidth
            triangle.computeZ()
            result = triangle
        else:
            self.basicDrawLineFromTo(startPoint, endPoint)
        return result
    
    def basicDrawLineFromTo(self, startPoint, endPoint):
        if self.drawingContext == None:
            #assuming pen color and width is saved and restored elsewhere
            return
        #do nothing if rounding fails
        try:
            x1 = intround(startPoint.x)
            y1 = intround(startPoint.y)
            x2 = intround(endPoint.x)
            y2 = intround(endPoint.y)
            width = intround(self.lineWidth)
            self.drawingContextDrawSolidLine(x1, y1, x2, y2, width, self.lineColor)
        except:
            # pdf raise for now
            raise
            pass
    
    def draw3DFace(self, point1, point2, point3, point4):
        # subclasses must override
        raise GeneralException.create("Problem: draw3DFace method not supported in base class; in method KfDrawingSurface.draw3DFace.")
    
    #terminology is different: drawing surface frontColor is pen line color 
    # and drawing surface backColor (which should be back-facing triangle) is fill color
    #drawing surface draws the last triangle allocated - and deallocates it if needed
    def drawLastTriangle(self):
        #last allocated triangle
        triangle = self.triangles[-1]
        triangle.isLine = False
        triangle.updateGeometry()
        #PDF FIX - maybe should scale this?
        triangle.lineWidth = self.lineWidth
        triangle.lineColor = self.lineColor
        triangle.foreColor = self.foreColor
        triangle.backColor = self.backColor
        if self.recording:
            pass
            #"store triangle"
            #do nothing as already stored
        else:
            self.basicDrawTriangle(triangle)
            #deallocate it
            del self.triangles[-1]
    
    #pdf - draw the triangle object - assume it is reasonably flat"
    #{can only draw triangles for now
    #needs fixed size for array - would need to allocate for variable sizes
    #or could use direct windows triangle call and larger array but pass number of points
    #terminology is different: drawing surface frontColor is pen line color
    #and drawing surface backColor (which should be back-facing triangle) is fill color"
    #restricting range of coordingates to 32767 to prevent possible out of range errors when drawing
    def basicDrawTriangle(self, triangle):
        if self.drawingContext == None:
            return
        
        if (triangle.isLine):
            #do nothing if round fails or assign to integer fails
            try:
                #draw line
                startPoint = triangle.points[0]
                endPoint = triangle.points[1]
                x1 = intround(startPoint.x)
                y1 = intround(startPoint.y)
                x2 = intround(endPoint.x)
                y2 = intround(endPoint.y)
                width = intround(triangle.lineWidth)
                self.drawingContextDrawSolidLine(x1, y1, x2, y2, width, triangle.lineColor)
            except:
                # PDF FIX raise for now
                raise
                pass
            return
        
        pointArray = []
        for i in range(4):
            pointArray.append(delphi_compatability.TPoint()) # not sure what type of point it shoudl be
        
        # build point array
        for i in range(0, 4):
            if i < 3:
                # make last point same as first for drawing lines around whole polygon
                aPoint = triangle.points[i]
            else:
                aPoint = triangle.points[0]
            try:
                pointArray[i].X = intround(aPoint.x)
                pointArray[i].Y = intround(aPoint.y)
            except:
                #maybe could test sign to put in negative big numbers? watch out for NaNs!
                pointArray[i].X = 32767
                pointArray[i].Y = 32767
        
        interiorColor = triangle.visibleSurfaceColor()
        
        if self.drawingLines:
            if self.fillingTriangles:
                edgeColor = triangle.drawLinesColor(self.lineContrastIndex)
            else:
                edgeColor = triangle.visibleSurfaceColor()
        else:
            edgeColor = triangle.visibleSurfaceColor()
            
        if self.circlingPoints:
            vertextPointColor = self.circleColor
        else:
            vertextPointColor = None
        
        self.drawingContextDrawTriangle(pointArray, interiorColor, edgeColor, 1, self.fillingTriangles, vertextPointColor)

    # ----------------------------------------------------------------------------- KfDrawingSurface recording 
    def recordingStart(self):
        self.clearTriangles()
        self.recording = True
    
    def recordingStop(self):
        self.recording = False
    
    def recordingDraw(self):
        self.sortTrianglesConsideringTdos()
        self.trianglesDraw()
        
    ################# SUBCLASSES MUST IMPLEMENT
    
    #def drawingContextUseSolidBrush(self):
    #    #self.pane.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
    #    raise "Subclass must implement"
    
    #def drawingContextUseClearBrush(self):
    #    #self.pane.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
    #    raise "Subclass must implement"
    
    def drawingContextDrawSolidLine(self, x1, y1, x2, y2, width, color):
        raise "Subclass must implement"
        # Ideas:
        #self.pane.Pen.Width = intround(self.lineWidth)
        #self.pane.Pen.Color = self.lineColor
        #self.pane.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        #self.pane.MoveTo(intround(startPoint.x), intround(startPoint.y))
        #self.pane.LineTo(intround(endPoint.x), intround(endPoint.y))
    
    def drawingContextDrawTriangle(self, points, interiorColor, edgeColor, edgeWidth, drawFilled, vertextPointColor=None):
        raise "Subclass must implement"
        # IDEAS:
        #self.pane.Pen.Color = triangle.visibleSurfaceColor()
        #self.pane.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        #self.pane.Brush.Color = triangle.visibleSurfaceColor()    
        #self.pane.Pen.Width = 1
        
        #if self.fillingTriangles:
        #    self.pane.Polygon(points)
        #else:
        #    self.pane.Polyline(points)
            
        #if self.circlingPoints:
        #    self.pane.Pen.Color = self.circleColor
        #    self.pane.Brush.Color = self.circleColor
        #    for i in range(0, 3):
        #        self.pane.Ellipse(points[i].X - self.circlePointRadius, pointAs[i].Y - self.circlePointRadius, points[i].X + self.circlePointRadius, points[i].Y + self.circlePointRadius)
