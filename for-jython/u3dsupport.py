# unit U3dsupport
import copy
import delphi_compatability
from conversion_common import *

#import utdo
import usupport

# const
kFastTrigArraySize = 256
kDirectionClockwise = 1
kDirectionCounterClockwise = -1
kDirectionUnknown = 0

initialized = False

# var
SinCache = [0] * (kFastTrigArraySize + 1)
CosCache = [0] * (kFastTrigArraySize + 1)

#if you change this - you need to change angleX etc. functions
# record
class TRealRect:
    def __init__(self):
        self.top = 0.0
        self.left = 0.0
        self.bottom = 0.0
        self.right = 0.0

# record
class Vertex:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

# record
class VertexTriangle:
    def __init__(self):
        self.vertex1 = 0
        self.vertex2 = 0
        self.vertex3 = 0

# ------------------------------------------------------------------- global functions 
def fastTrigInitialize():
    for i in range(0, kFastTrigArraySize):
        #Approach: sine and cosine arrays are used for speed. Angles are 0 - 255 instead of 0 to 359
        #PDF - maybe want to expand this to 0 - 1023? - would impact rotate callers
        SinCache[i] = sin(i * 2 * 3.141592654 / kFastTrigArraySize)
        CosCache[i] = cos(i * 2 * 3.141592654 / kFastTrigArraySize)

#these functions are no longer called here but are available for other uses
#they were bundled directly into rotate
#moved bounding angle into cache range into functions to decrease function overhead
#copied these functions into rotate to decrease overhead there - both of function call and of bounding angle twice
def fastTrigCos(angle):
    try:
        boundedAngle = intround(angle) % kFastTrigArraySize
    except:
        boundedAngle = 0
    if (boundedAngle < 0):
        boundedAngle = kFastTrigArraySize + boundedAngle
    result = CosCache[boundedAngle]
    return result

def fastTrigSin(angle):
    try:
        boundedAngle = intround(angle) % kFastTrigArraySize
    except:
        boundedAngle = 0
    if (boundedAngle < 0):
        boundedAngle = kFastTrigArraySize + boundedAngle
    result = SinCache[boundedAngle]
    return result

def clockwise(point0, point1, point2):
    dx1 = point1.X - point0.X
    dy1 = point1.Y - point0.Y
    dx2 = point2.X - point0.X
    dy2 = point2.Y - point0.Y
    if (dx1 * dy2) > (dy1 * dx2):
        result = kDirectionClockwise
    elif (dx1 * dy2) < (dy1 * dx2):
        result = kDirectionCounterClockwise
    elif ((dx1 * dx2) < 0) or ((dy1 * dy2) < 0):
        result = kDirectionCounterClockwise
    elif ((dx1 * dx1) + (dy1 * dy1)) < ((dx2 * dx2) + (dy2 * dy2)):
        result = kDirectionClockwise
    else:
        result = kDirectionUnknown
    return result

def pointInTriangle(point, triangle):
    result = False
    if (triangle[0].X == triangle[1].X) and (triangle[1].X == triangle[2].X) and (triangle[0].Y == triangle[1].Y) and (triangle[1].Y == triangle[2].Y):
        return result
    first = clockwise(point, triangle[0], triangle[1])
    second = clockwise(point, triangle[1], triangle[2])
    third = clockwise(point, triangle[2], triangle[0])
    result = (first == second) and (second == third)
    return result

# ---------------------------------------------------------------------------------- KfPoint3D 
class KfPoint3D:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

def KfPoint3D_setXYZ(thePoint, aX, aY, aZ):
    thePoint.x = aX
    thePoint.y = aY
    thePoint.z = aZ

def KfPoint3D_addXYZ(thePoint, xOffset, yOffset, zOffset):
    #pdf - shift point by x y and z.
    thePoint.x = thePoint.x + xOffset
    thePoint.y = thePoint.y + yOffset
    thePoint.z = thePoint.z + zOffset

def KfPoint3D_scaleBy(thePoint, aScale):
    #pdf - multiply point by scale.
    thePoint.x = thePoint.x * aScale
    thePoint.y = thePoint.y * aScale
    thePoint.z = thePoint.z * aScale

def KfPoint3D_subtract(thePoint, aPoint):
    #pdf - subtract point from this point.
    thePoint.x = thePoint.x - aPoint.x
    thePoint.y = thePoint.y - aPoint.y
    thePoint.z = thePoint.z - aPoint.z

def KfPoint3D_matchXYZ(pointOne, pointTwo, matchDistance):
    result = False
    # v1.6b1 added
    result = (abs(pointOne.x - pointTwo.x) <= matchDistance) and (abs(pointOne.y - pointTwo.y) <= matchDistance) and (abs(pointOne.z - pointTwo.z) <= matchDistance)
    return result

def KfPoint3D_addPointToBoundsRect(boundsRect, aPoint):
    try:
        x = intround(aPoint.x)
    except:
        x = 0
    try:
        y = intround(aPoint.y)
    except:
        y = 0
    if (boundsRect.Left == 0) and (boundsRect.Right == 0) and (boundsRect.Top == 0) and (boundsRect.Bottom == 0):
        # on first point entered, initialize bounds rect
        boundsRect.Left = x
        boundsRect.Right = x
        boundsRect.Top = y
        boundsRect.Bottom = y
    else:
        if x < boundsRect.Left:
            boundsRect.Left = x
        elif x > boundsRect.Right:
            boundsRect.Right = x
        if y < boundsRect.Top:
            boundsRect.Top = y
        elif y > boundsRect.Bottom:
            boundsRect.Bottom = y

class KfMatrix:
    def __init__(self):
        self.a0 = 0.0
        self.a1 = 0.0
        self.a2 = 0.0
        self.b0 = 0.0
        self.b1 = 0.0
        self.b2 = 0.0
        self.c0 = 0.0
        self.c1 = 0.0
        self.c2 = 0.0
        self.position = KfPoint3D()
        
    def __repr__(self):
        return "KfMatrix: (%f %f %f) (%f %f %f) (%f %f %f)" %(self.a0, self.a1, self.a2, self.b0, self.b1, self.b2, self.c0, self.c1, self.c2)
    
    # ---------------------------------------------------------------------------------- *KfMatrix imitializing and copying 
    def initializeAsUnitMatrix(self):
        self.a0 = 1.0
        self.a1 = 0.0
        self.a2 = 0.0
        self.b0 = 0.0
        self.b1 = 1.0
        self.b2 = 0.0
        self.c0 = 0.0
        self.c1 = 0.0
        self.c2 = 1.0
        self.position.x = 0.0
        self.position.y = 0.0
        self.position.z = 0.0
    
    def deepCopy(self):
        result = KfMatrix()
        result.position.x = self.position.x
        result.position.y = self.position.y
        result.position.z = self.position.z
        result.a0 = self.a0
        result.a1 = self.a1
        result.a2 = self.a2
        result.b0 = self.b0
        result.b1 = self.b1
        result.b2 = self.b2
        result.c0 = self.c0
        result.c1 = self.c1
        result.c2 = self.c2
        return result
    
    def copyTo(self, otherMatrix):
        otherMatrix.position.x = self.position.x
        otherMatrix.position.y = self.position.y
        otherMatrix.position.z = self.position.z
        otherMatrix.a0 = self.a0
        otherMatrix.a1 = self.a1
        otherMatrix.a2 = self.a2
        otherMatrix.b0 = self.b0
        otherMatrix.b1 = self.b1
        otherMatrix.b2 = self.b2
        otherMatrix.c0 = self.c0
        otherMatrix.c1 = self.c1
        otherMatrix.c2 = self.c2
    
    # ---------------------------------------------------------------------------- KfMatrix moving and transforming 
    def move(self, distance):
        #pdf - move a distance by multiplying matrix values
        #   movement is along x axis (d, 0, 0, 1);
        self.position.x = self.position.x + distance * self.a0
        self.position.y = self.position.y + distance * self.b0
        self.position.z = self.position.z + distance * self.c0
    
    # transform the point, including offsetting it by the current position
    #Alters the point's contents
    def transform(self, aPoint3D):
        x = aPoint3D.x
        y = aPoint3D.y
        z = aPoint3D.z
        aPoint3D.x = (x * self.a0) + (y * self.a1) + (z * self.a2) + self.position.x
        aPoint3D.y = (x * self.b0) + (y * self.b1) + (z * self.b2) + self.position.y
        aPoint3D.z = (x * self.c0) + (y * self.c1) + (z * self.c2) + self.position.z
        
    # ---------------------------------------------------------------------------------- KfMatrix rotating 
    def rotateX(self, angle):
        #bound angle and convert to index
        #not doing try except around round for speed here - could fail ...
        boundedAngleIndex = intround(angle) % kFastTrigArraySize
        if (boundedAngleIndex < 0):
            boundedAngleIndex = kFastTrigArraySize + boundedAngleIndex
        if (boundedAngleIndex < 0):
            raise "Still negative"
        cosAngle = CosCache[boundedAngleIndex]
        sinAngle = SinCache[boundedAngleIndex]
        #moved minuses to middle to optimize
        self.a0 = self.a0
        temp1 = (self.a1 * cosAngle) - (self.a2 * sinAngle)
        self.a2 = (self.a1 * sinAngle) + (self.a2 * cosAngle)
        self.a1 = temp1
        self.b0 = self.b0
        temp1 = (self.b1 * cosAngle) - (self.b2 * sinAngle)
        self.b2 = (self.b1 * sinAngle) + (self.b2 * cosAngle)
        self.b1 = temp1
        self.c0 = self.c0
        temp1 = (self.c1 * cosAngle) - (self.c2 * sinAngle)
        self.c2 = (self.c1 * sinAngle) + (self.c2 * cosAngle)
        self.c1 = temp1
    
    def rotateY(self, angle):
        #bound angle and convert to index
        #not doing try except around round for speed here - could fail ...
        boundedAngleIndex = intround(angle) % kFastTrigArraySize
        if (boundedAngleIndex < 0):
            boundedAngleIndex = kFastTrigArraySize + boundedAngleIndex
        if (boundedAngleIndex < 0):
            raise "Still negative"
        cosAngle = CosCache[boundedAngleIndex]
        sinAngle = SinCache[boundedAngleIndex]
        temp0 = (self.a0 * cosAngle) + (self.a2 * sinAngle)
        self.a1 = self.a1
        #flipped to put minus in middle
        self.a2 = (self.a2 * cosAngle) - (self.a0 * sinAngle)
        self.a0 = temp0
        temp0 = (self.b0 * cosAngle) + (self.b2 * sinAngle)
        self.b1 = self.b1
        #flipped to put minus in middle
        self.b2 = (self.b2 * cosAngle) - (self.b0 * sinAngle)
        self.b0 = temp0
        temp0 = (self.c0 * cosAngle) + (self.c2 * sinAngle)
        self.c1 = self.c1
        #flipped to put minus in middle
        self.c2 = (self.c2 * cosAngle) - (self.c0 * sinAngle)
        self.c0 = temp0
    
    def rotateZ(self, angle):
        #
        #  {bound angle and convert to index}
        #	{not doing try except around round for speed here - could fail ...}
        #  {boundedAngleIndex := round(angle) mod kFastTrigArraySize;
        #  if (boundedAngleIndex  < 0) then
        #  	boundedAngleIndex := kFastTrigArraySize + boundedAngleIndex;
        #	cosAngle := CosCache[boundedAngleIndex];
        #  sinAngle := SinCache[boundedAngleIndex];}
        #                          { cfk try at replacing rounding with using all floating point }
        #  cosAngle := cos(angle * 2.0 * 3.14159 / 256.0);
        #  sinAngle := sin(angle * 2.0 * 3.14159 / 256.0);
        #
        #  {minuses moved to middle to optimize}
        #  temp0  :=(a0 * cosAngle) - (a1 * sinAngle);
        #  a1 := (a0 * sinAngle) + (a1 * cosAngle);
        #  a2 := a2;
        #  a0 := temp0;
        #  temp0 := (b0 * cosAngle) - (b1 * sinAngle);
        #  b1 := (b0 * sinAngle) + (b1 * cosAngle);
        #  b2 := b2;
        #  b0 := temp0;
        #  temp0 := (c0 * cosAngle) - (c1 * sinAngle);
        #  c1 :=  (c0 * sinAngle) + (c1 * cosAngle);
        #  c2 := c2;
        #  c0 := temp0;
        
        #bound angle and convert to index
        #not doing try except around round for speed here - could fail ...
        boundedAngleIndex = intround(angle) % kFastTrigArraySize
        if (boundedAngleIndex < 0):
            boundedAngleIndex = kFastTrigArraySize + boundedAngleIndex
        if (boundedAngleIndex < 0):
            raise "Still negative"
        cosAngle = CosCache[boundedAngleIndex]
        sinAngle = SinCache[boundedAngleIndex]
        #minuses moved to middle to optimize
        temp0 = (self.a0 * cosAngle) - (self.a1 * sinAngle)
        self.a1 = (self.a0 * sinAngle) + (self.a1 * cosAngle)
        self.a2 = self.a2
        self.a0 = temp0
        temp0 = (self.b0 * cosAngle) - (self.b1 * sinAngle)
        self.b1 = (self.b0 * sinAngle) + (self.b1 * cosAngle)
        self.b2 = self.b2
        self.b0 = temp0
        temp0 = (self.c0 * cosAngle) - (self.c1 * sinAngle)
        self.c1 = (self.c0 * sinAngle) + (self.c1 * cosAngle)
        self.c2 = self.c2
        self.c0 = temp0
    
    #class SinCache CosCache
    # ---------------------------------------------------------------------------------- KfMatrix returning current angles 
    #PDF FIX - potential bug
    # these do not take in account kFastTrigArraySize could be different from 256
    def angleX(self):
        try:
            result = 0
            temp = (self.a2 * self.a2) + (self.c2 * self.c2)
            if (temp < 0.0):
                temp = 0.0
            temp = sqrt(temp)
            if (temp == 0.0):
                if (self.b2 < 0):
                    result = 64
                else:
                    result = 256 - 64
            else:
                temp = self.b2 / temp
                temp = arctan(temp)
                result = intround(-temp * 256 / (2 * 3.1415926))
        except:
            result = 0
        return result
    
    def angleY(self):
        try:
            result = 0
            temp = (self.a0 * self.a0) + (self.c0 * self.c0)
            if (temp < 0.0):
                temp = 0.0
            temp = sqrt(temp)
            if (temp == 0.0):
                if (self.b0 < 0):
                    result = 64
                else:
                    result = 256 - 64
            else:
                temp = self.b0 / temp
                temp = arctan(temp)
                result = intround(-temp * 256 / (2 * 3.1415926))
        except:
            result = 0
        return result
    
    def angleZ(self): 
        try:
            result = 0
            temp = (self.a1 * self.a1) + (self.c1 * self.c1)
            if (temp < 0.0):
                temp = 0.0
            temp = sqrt(temp)
            if (temp == 0.0):
                if (self.b1 < 0):
                    result = 64
                else:
                    result = 256 - 64
            else:
                temp = self.b1 / temp
                temp = arctan(temp)
                result = intround(-temp * 256 / (2 * 3.1415926))
        except:
            result = 0
        return result
    
#these can only be triangular
class KfTriangle:
    def __init__(self):
        self.foreColor = delphi_compatability.EmptyColor
        self.backColor = delphi_compatability.EmptyColor
        self.lineColor = delphi_compatability.EmptyColor
        self.zForSorting = 0.0
        self.backFacing = False
        self.lineWidth = 0.0
        self.isLine = False
        self.points = []
        for i in range(3):
            self.points.append(KfPoint3D())
        self.tdo = None
        self.plantPartID = 0L
    
    # ---------------------------------------------------------------------------------- KfTriangle updating 
    def updateGeometry(self):
        self.computeBackFacing()
        self.computeZ()
    
    def computeBackFacing(self):    
        self.backFacing = False
        if self.isLine:
            return
        point0 = self.points[0]
        point1 = self.points[1]
        point2 = self.points[2]
        backfacingResult = ((point1.x - point0.x) * (point2.y - point0.y)) - ((point1.y - point0.y) * (point2.x - point0.x))
        self.backFacing = (backfacingResult < 0)
    
    def computeZ(self):
        if self.isLine:
            minZ = self.points[0].z
            if self.points[1].z < minZ:
                minZ = self.points[1].z
        else:
            minZ = self.points[0].z
            if self.points[1].z < minZ:
                minZ = self.points[1].z
            if self.points[2].z < minZ:
                minZ = self.points[2].z
        self.zForSorting = minZ
    
    def visibleSurfaceColor(self):
        if self.backFacing:
            result = self.backColor
        else:
            result = self.foreColor
        return result
    
    def invisibleSurfaceColor(self):
        if self.backFacing:
            result = self.foreColor
        else:
            result = self.backColor
        return result
    
    def drawLinesColor(self, lineContrastIndex):
        if self.backFacing:
            result = self.backColor
        else:
            result = self.foreColor
        if lineContrastIndex > 0:
            result = usupport.darkerColorWithSubtraction(result, 10 * lineContrastIndex)
        return result
  
# do this only once
if not initialized:
    fastTrigInitialize()
    initialized = 1  
