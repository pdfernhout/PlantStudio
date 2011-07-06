# unit Udrawingsurface

from conversion_common import *
import u3dsupport
import utdo
import ucollect
import delphi_compatability

# const
kInitialDrawingSurfaceTriangles = 1000

class KfDrawingSurface(TObject):
    def __init__(self):
        self.pane = TCanvas()
        self.lineContrastIndex = 0
        self.drawingLines = false
        self.fillingTriangles = false
        self.circlingPoints = false
        self.foreColor = TColor()
        self.backColor = TColor()
        self.lineColor = TColor()
        self.circleColor = TColor()
        self.numTrianglesUsed = 0L
        self.triangles = TListCollection()
        self.recording = false
        self.lineWidth = 0.0
        self.circlePointRadius = 0
        self.sortTdosAsOneItem = false
    
    # ----------------------------------------------------------------------------- *KfDrawingSurface creating/destroying 
    def create(self):
        i = 0L
        
        TObject.create(self)
        self.triangles = ucollect.TListCollection().Create()
        self.numTrianglesUsed = 0
        self.fillingTriangles = true
        self.initialize()
        for i in range(0, kInitialDrawingSurfaceTriangles + 1):
            # start with a bunch of triangles 
            self.triangles.Add(u3dsupport.KfTriangle.create)
        return self
    
    def destroy(self):
        self.triangles.free
        TObject.destroy(self)
    
    def initialize(self):
        #backColor := clLtGray;
        #  foreColor := clLtGray;
        #  lineColor := clLtGray;
        self.lineWidth = 1.0
        self.recording = false
        self.clearTriangles()
        if self.pane != None:
            if self.fillingTriangles:
                self.pane.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
            else:
                self.pane.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
    
    # ----------------------------------------------------------------------------- KfDrawingSurface managing triangles 
    def clearTriangles(self):
        i = 0L
        
        for i in range(0, self.numTrianglesUsed):
            u3dsupport.KfTriangle(self.triangles.Items[i]).tdo = None
        self.numTrianglesUsed = 0
    
    def plantPartIDForPoint(self, point):
        result = 0L
        i = 0L
        triangle = KfTriangle()
        points = [0] * (range(0, 2 + 1) + 1)
        widenedPoints = [0] * (range(0, 2 + 1) + 1)
        width = 0
        thisDistance = 0.0
        closestDistanceSoFar = 0.0
        closestPartID = 0L
        centerX = 0.0
        centerY = 0.0
        x = 0.0
        y = 0.0
        
        x = Point.x
        y = Point.y
        result = -1
        closestDistanceSoFar = 0
        closestPartID = -1
        for i in range(0, self.triangles.Count):
            triangle = u3dsupport.KfTriangle(self.triangles.Items[i])
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
                if u3dsupport.pointInTriangle(Point, points):
                    result = triangle.plantPartID
                    return result
        result = closestPartID
        return result
    
    def allocateTriangle(self):
        result = KfTriangle()
        result = None
        if self.numTrianglesUsed < self.triangles.Count:
            result = self.triangles.Items[self.numTrianglesUsed]
        else:
            result = u3dsupport.KfTriangle.create
            self.triangles.Add(result)
        self.numTrianglesUsed += 1
        return result
    
    def sortTrianglesConsideringTdos(self):
        i = 0L
        triangle = KfTriangle()
        oldValue = 0.0
        
        if self.numTrianglesUsed <= 1:
            return
        if self.sortTdosAsOneItem:
            for i in range(0, self.numTrianglesUsed):
                triangle = u3dsupport.KfTriangle(self.triangles.Items[i])
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
        self.sortTriangles(0, self.numTrianglesUsed - 1)
    
    def sortTriangles(self, left, right):
        i = 0
        j = 0
        z = 0.0
        
        if right > left:
            z = u3dsupport.KfTriangle(self.triangles.Items[right]).zForSorting
            i = left - 1
            j = right
            while true:
                while 1:
                    i = i + 1
                    if not (u3dsupport.KfTriangle(self.triangles.Items[i]).zForSorting < z): break
                while 1:
                    j = j - 1
                    if (j < i) or (not (u3dsupport.KfTriangle(self.triangles.Items[j]).zForSorting > z)): break
                if i >= j:
                    break
                self.triangles.Exchange(i, j)
            self.triangles.Exchange(i, right)
            self.sortTriangles(left, j)
            self.sortTriangles(i + 1, right)
    
    # ----------------------------------------------------------------------------- KfDrawingSurface drawing 
    def trianglesDraw(self):
        i = 0
        
        if self.numTrianglesUsed > 0:
            for i in range(0, self.numTrianglesUsed):
                self.basicDrawTriangle(self.triangles.Items[i])
    
    def drawLineFromTo(self, startPoint, endPoint):
        result = KfTriangle()
        triangle = KfTriangle()
        
        result = None
        if self.recording:
            #store triangle
            triangle = self.allocateTriangle()
            triangle.points[0] = startPoint
            triangle.points[1] = endPoint
            triangle.isLine = true
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
        if self.pane == None:
            #assuming pen color and width is saved and restored elsewhere
            return
        #do nothing if rounding fails
        try:
            self.pane.Pen.Width = intround(self.lineWidth) % 1000
            self.pane.Pen.Color = self.lineColor
            self.pane.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
            self.pane.MoveTo(intround(startPoint.x) % 32767, intround(startPoint.y) % 32767)
            self.pane.LineTo(intround(endPoint.x) % 32767, intround(endPoint.y) % 32767)
        except:
            pass
    
    def draw3DFace(self, point1, point2, point3, point4):
        # subclasses must override
        raise GeneralException.create("Problem: draw3DFace method not supported in base class; in method KfDrawingSurface.draw3DFace.")
    
    #terminology is different: drawing surface frontColor is pen line color 
    # and drawing surface backColor (which should be back-facing triangle) is fill color
    #drawing surface draws the last triangle allocated - and deallocates it if needed
    def drawLastTriangle(self):
        triangle = KfTriangle()
        
        #last allocated triangle
        triangle = self.triangles.Items[self.numTrianglesUsed - 1]
        triangle.isLine = false
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
            self.numTrianglesUsed -= 1
    
    #pdf - draw the triangle object - assume it is reasonably flat"
    #{can only draw triangles for now
    #needs fixed size for array - would need to allocate for variable sizes
    #or could use direct windows triangle call and larger array but pass number of points
    #terminology is different: drawing surface frontColor is pen line color
    #and drawing surface backColor (which should be back-facing triangle) is fill color"
    #restricting range of coordingates to 32767 to prevent possible out of range errors when drawing
    def basicDrawTriangle(self, triangle):
        startPoint = KfPoint3D()
        endPoint = KfPoint3D()
        aPoint = KfPoint3D()
        pointArray = [0] * (range(0, 3 + 1) + 1)
        i = 0
        
        if self.pane == None:
            return
        if (triangle.isLine):
            #do nothing if round fails or assign to integer fails
            try:
                #draw line
                self.pane.Pen.Width = intround(triangle.lineWidth)
                self.pane.Pen.Color = triangle.lineColor
                self.pane.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
                startPoint = triangle.points[0]
                endPoint = triangle.points[1]
                self.pane.MoveTo(intround(startPoint.x) % 32767, intround(startPoint.y) % 32767)
                self.pane.LineTo(intround(endPoint.x) % 32767, intround(endPoint.y) % 32767)
            except:
                pass
            return
        for i in range(0, 3 + 1):
            if i < 3:
                # make last point same as first for drawing lines around whole polygon
                aPoint = triangle.points[i]
            else:
                aPoint = triangle.points[0]
            try:
                pointArray[i].X = intround(aPoint.x) % 32767
                pointArray[i].Y = intround(aPoint.y) % 32767
            except:
                #maybe could test sign to put in negative big numbers? watch out for NaNs!
                pointArray[i].X = 32767
                pointArray[i].Y = 32767
        self.pane.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        self.pane.Brush.Color = triangle.visibleSurfaceColor()
        if self.drawingLines:
            if self.fillingTriangles:
                self.pane.Pen.Color = triangle.drawLinesColor(self.lineContrastIndex)
            else:
                self.pane.Pen.Color = triangle.visibleSurfaceColor()
        else:
            self.pane.Pen.Color = triangle.visibleSurfaceColor()
        self.pane.Pen.Width = 1
        if self.fillingTriangles:
            self.pane.Polygon(pointArray)
        else:
            self.pane.Polyline(pointArray)
        if self.circlingPoints:
            self.pane.Pen.Color = self.circleColor
            self.pane.Brush.Color = self.circleColor
            for i in range(0, 2 + 1):
                self.pane.Ellipse(pointArray[i].X - self.circlePointRadius, pointArray[i].Y - self.circlePointRadius, pointArray[i].X + self.circlePointRadius, pointArray[i].Y + self.circlePointRadius)
    
    # ----------------------------------------------------------------------------- KfDrawingSurface recording 
    def recordingStart(self):
        self.clearTriangles()
        self.recording = true
    
    def recordingStop(self):
        self.recording = false
    
    def recordingDraw(self):
        self.sortTrianglesConsideringTdos()
        self.trianglesDraw()
    
