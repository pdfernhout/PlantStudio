// unit U3dsupport

from conversion_common import *;
import usupport;
import utdo;
import delphi_compatability;

// const
kFastTrigArraySize = 256;
kDirectionClockwise = 1;
kDirectionCounterClockwise = -1;
kDirectionUnknown = 0;


// var
 SinCache = [0] * (range(0, kFastTrigArraySize) + 1);
 CosCache = [0] * (range(0, kFastTrigArraySize) + 1);


//if you change this - you need to change angleX etc. functions
// record
class TRealRect {
    public float top;
    public float left;
    public float bottom;
    public float right;
}

// record
class Vertex {
    public float x;
    public float y;
    public float z;
}

// record
class VertexTriangle {
    public int vertex1;
    public int vertex2;
    public int vertex3;
}

// ------------------------------------------------------------------- global functions 
public void fastTrigInitialize() {
    int i = 0;
    
    for (i = 0; i <= kFastTrigArraySize - 1; i++) {
        //Approach: sine and cosine arrays are used for speed. Angles are 0 - 255 instead of 0 to 359
        //PDF - maybe want to expand this to 0 - 1023? - would impact rotate callers
        SinCache[i] = sin(i * 2 * 3.141592654 / kFastTrigArraySize);
        CosCache[i] = cos(i * 2 * 3.141592654 / kFastTrigArraySize);
    }
}

//these functions are no longer called here but are available for other uses
//they were bundled directly into rotate
//moved bounding angle into cache range into functions to decrease function overhead
//copied these functions into rotate to decrease overhead there - both of function call and of bounding angle twice
public float fastTrigCos(float angle) {
    result = 0.0;
    int boundedAngle = 0;
    
    try {
        boundedAngle = intround(angle) % kFastTrigArraySize;
    } catch (Exception e) {
        boundedAngle = 0;
    }
    if ((boundedAngle < 0)) {
        boundedAngle = kFastTrigArraySize + boundedAngle;
    }
    result = CosCache[boundedAngle];
    return result;
}

public float fastTrigSin(float angle) {
    result = 0.0;
    int boundedAngle = 0;
    
    try {
        boundedAngle = intround(angle) % kFastTrigArraySize;
    } catch (Exception e) {
        boundedAngle = 0;
    }
    if ((boundedAngle < 0)) {
        boundedAngle = kFastTrigArraySize + boundedAngle;
    }
    result = SinCache[boundedAngle];
    return result;
}

public int clockwise(TPoint point0, TPoint point1, TPoint point2) {
    result = 0;
    float dx1 = 0.0;
    float dy1 = 0.0;
    float dx2 = 0.0;
    float dy2 = 0.0;
    
    dx1 = point1.X - point0.X;
    dy1 = point1.Y - point0.Y;
    dx2 = point2.X - point0.X;
    dy2 = point2.Y - point0.Y;
    if ((dx1 * dy2) > (dy1 * dx2)) {
        result = kDirectionClockwise;
    } else if ((dx1 * dy2) < (dy1 * dx2)) {
        result = kDirectionCounterClockwise;
    } else if (((dx1 * dx2) < 0) || ((dy1 * dy2) < 0)) {
        result = kDirectionCounterClockwise;
    } else if (((dx1 * dx1) + (dy1 * dy1)) < ((dx2 * dx2) + (dy2 * dy2))) {
        result = kDirectionClockwise;
    } else {
        result = kDirectionUnknown;
    }
    return result;
}

public boolean pointInTriangle(TPoint point,  triangle) {
    result = false;
    int first = 0;
    int second = 0;
    int third = 0;
    
    result = false;
    if ((triangle[0].X == triangle[1].X) && (triangle[1].X == triangle[2].X) && (triangle[0].Y == triangle[1].Y) && (triangle[1].Y == triangle[2].Y)) {
        return result;
    }
    first = clockwise(Point, triangle[0], triangle[1]);
    second = clockwise(Point, triangle[1], triangle[2]);
    third = clockwise(Point, triangle[2], triangle[0]);
    result = (first == second) && (second == third);
    return result;
}


class KfMatrix extends TObject {
    public float a0;
    public float a1;
    public float a2;
    public float b0;
    public float b1;
    public float b2;
    public float c0;
    public float c1;
    public float c2;
    public KfPoint3D position;
    
    // ---------------------------------------------------------------------------------- *KfMatrix imitializing and copying 
    public void initializeAsUnitMatrix() {
        this.a0 = 1.0;
        this.a1 = 0;
        this.a2 = 0;
        this.b0 = 0;
        this.b1 = 1.0;
        this.b2 = 0;
        this.c0 = 0;
        this.c1 = 0;
        this.c2 = 1.0;
        this.position.x = 0;
        this.position.y = 0;
        this.position.z = 0;
    }
    
    public KfMatrix deepCopy() {
        result = new KfMatrix();
        result = null;
        result = KfMatrix.create;
        result.position = this.position;
        result.a0 = this.a0;
        result.a1 = this.a1;
        result.a2 = this.a2;
        result.b0 = this.b0;
        result.b1 = this.b1;
        result.b2 = this.b2;
        result.c0 = this.c0;
        result.c1 = this.c1;
        result.c2 = this.c2;
        return result;
    }
    
    public void copyTo(KfMatrix otherMatrix) {
        otherMatrix.position = this.position;
        otherMatrix.a0 = this.a0;
        otherMatrix.a1 = this.a1;
        otherMatrix.a2 = this.a2;
        otherMatrix.b0 = this.b0;
        otherMatrix.b1 = this.b1;
        otherMatrix.b2 = this.b2;
        otherMatrix.c0 = this.c0;
        otherMatrix.c1 = this.c1;
        otherMatrix.c2 = this.c2;
    }
    
    // ---------------------------------------------------------------------------- KfMatrix moving and transforming 
    public void move(float distance) {
        //pdf - move a distance by multiplying matrix values
        //   movement is along x axis (d, 0, 0, 1);
        this.position.x = this.position.x + distance * this.a0;
        this.position.y = this.position.y + distance * this.b0;
        this.position.z = this.position.z + distance * this.c0;
    }
    
    //pdf - transform the point, including offsetting it by the current position
    //Alters the point's contents
    public void transform(KfPoint3D aPoint3D) {
        float x = 0.0;
        float y = 0.0;
        float z = 0.0;
        
        x = aPoint3D.x;
        y = aPoint3D.y;
        z = aPoint3D.z;
        aPoint3D.x = (x * this.a0) + (y * this.a1) + (z * this.a2) + this.position.x;
        aPoint3D.y = (x * this.b0) + (y * this.b1) + (z * this.b2) + this.position.y;
        aPoint3D.z = (x * this.c0) + (y * this.c1) + (z * this.c2) + this.position.z;
    }
    
    // ---------------------------------------------------------------------------------- KfMatrix rotating 
    public void rotateX(float angle) {
        float cosAngle = 0.0;
        float sinAngle = 0.0;
        float temp1 = 0.0;
        int boundedAngleIndex = 0;
        
        //bound angle and convert to index
        //not doing try except around round for speed here - could fail ...
        boundedAngleIndex = intround(angle) % kFastTrigArraySize;
        if ((boundedAngleIndex < 0)) {
            boundedAngleIndex = kFastTrigArraySize + boundedAngleIndex;
        }
        cosAngle = CosCache[boundedAngleIndex];
        sinAngle = SinCache[boundedAngleIndex];
        //moved minuses to middle to optimize
        this.a0 = this.a0;
        temp1 = (this.a1 * cosAngle) - (this.a2 * sinAngle);
        this.a2 = (this.a1 * sinAngle) + (this.a2 * cosAngle);
        this.a1 = temp1;
        this.b0 = this.b0;
        temp1 = (this.b1 * cosAngle) - (this.b2 * sinAngle);
        this.b2 = (this.b1 * sinAngle) + (this.b2 * cosAngle);
        this.b1 = temp1;
        this.c0 = this.c0;
        temp1 = (this.c1 * cosAngle) - (this.c2 * sinAngle);
        this.c2 = (this.c1 * sinAngle) + (this.c2 * cosAngle);
        this.c1 = temp1;
    }
    
    public void rotateY(float angle) {
        float cosAngle = 0.0;
        float sinAngle = 0.0;
        float temp0 = 0.0;
        int boundedAngleIndex = 0;
        
        //bound angle and convert to index
        //not doing try except around round for speed here - could fail ...
        boundedAngleIndex = intround(angle) % kFastTrigArraySize;
        if ((boundedAngleIndex < 0)) {
            boundedAngleIndex = kFastTrigArraySize + boundedAngleIndex;
        }
        cosAngle = CosCache[boundedAngleIndex];
        sinAngle = SinCache[boundedAngleIndex];
        temp0 = (this.a0 * cosAngle) + (this.a2 * sinAngle);
        this.a1 = this.a1;
        //flipped to put minus in middle
        this.a2 = (this.a2 * cosAngle) - (this.a0 * sinAngle);
        this.a0 = temp0;
        temp0 = (this.b0 * cosAngle) + (this.b2 * sinAngle);
        this.b1 = this.b1;
        //flipped to put minus in middle
        this.b2 = (this.b2 * cosAngle) - (this.b0 * sinAngle);
        this.b0 = temp0;
        temp0 = (this.c0 * cosAngle) + (this.c2 * sinAngle);
        this.c1 = this.c1;
        //flipped to put minus in middle
        this.c2 = (this.c2 * cosAngle) - (this.c0 * sinAngle);
        this.c0 = temp0;
    }
    
    public void rotateZ(float angle) {
        float cosAngle = 0.0;
        float sinAngle = 0.0;
        float temp0 = 0.0;
        int boundedAngleIndex = 0;
        
        //
        //  {bound angle and convert to index}
        //	{not doing try except around round for speed here - could fail ...}
        //  {boundedAngleIndex := round(angle) mod kFastTrigArraySize;
        //  if (boundedAngleIndex  < 0) then
        //  	boundedAngleIndex := kFastTrigArraySize + boundedAngleIndex;
        //	cosAngle := CosCache[boundedAngleIndex];
        //  sinAngle := SinCache[boundedAngleIndex];}
        //                          { cfk try at replacing rounding with using all floating point }
        //  cosAngle := cos(angle * 2.0 * 3.14159 / 256.0);
        //  sinAngle := sin(angle * 2.0 * 3.14159 / 256.0);
        //
        //  {minuses moved to middle to optimize}
        //  temp0  :=(a0 * cosAngle) - (a1 * sinAngle);
        //  a1 := (a0 * sinAngle) + (a1 * cosAngle);
        //  a2 := a2;
        //  a0 := temp0;
        //  temp0 := (b0 * cosAngle) - (b1 * sinAngle);
        //  b1 := (b0 * sinAngle) + (b1 * cosAngle);
        //  b2 := b2;
        //  b0 := temp0;
        //  temp0 := (c0 * cosAngle) - (c1 * sinAngle);
        //  c1 :=  (c0 * sinAngle) + (c1 * cosAngle);
        //  c2 := c2;
        //  c0 := temp0;    
        //bound angle and convert to index
        //not doing try except around round for speed here - could fail ...
        boundedAngleIndex = intround(angle) % kFastTrigArraySize;
        if ((boundedAngleIndex < 0)) {
            boundedAngleIndex = kFastTrigArraySize + boundedAngleIndex;
        }
        cosAngle = CosCache[boundedAngleIndex];
        sinAngle = SinCache[boundedAngleIndex];
        //minuses moved to middle to optimize
        temp0 = (this.a0 * cosAngle) - (this.a1 * sinAngle);
        this.a1 = (this.a0 * sinAngle) + (this.a1 * cosAngle);
        this.a2 = this.a2;
        this.a0 = temp0;
        temp0 = (this.b0 * cosAngle) - (this.b1 * sinAngle);
        this.b1 = (this.b0 * sinAngle) + (this.b1 * cosAngle);
        this.b2 = this.b2;
        this.b0 = temp0;
        temp0 = (this.c0 * cosAngle) - (this.c1 * sinAngle);
        this.c1 = (this.c0 * sinAngle) + (this.c1 * cosAngle);
        this.c2 = this.c2;
        this.c0 = temp0;
    }
    
    //class SinCache CosCache
    // ---------------------------------------------------------------------------------- KfMatrix returning current angles 
    //PDF FIX - potential bug
    // these do not take in account kFastTrigArraySize could be different from 256
    public byte angleX() {
        result = 0;
        float temp = 0.0;
        
        try {
            result = 0;
            temp = 0.0;
            temp = (this.a2 * this.a2) + (this.c2 * this.c2);
            if ((temp < 0.0)) {
                temp = 0.0;
            }
            temp = sqrt(temp);
            if ((temp == 0.0)) {
                if ((this.b2 < 0)) {
                    result = 64;
                } else {
                    result = 256 - 64;
                }
            } else {
                temp = this.b2 / temp;
                temp = arctan(temp);
                result = intround(-temp * 256 / (2 * 3.1415926));
            }
        } catch (Exception e) {
            result = 0;
        }
        return result;
    }
    
    public byte angleY() {
        result = 0;
        float temp = 0.0;
        
        try {
            result = 0;
            temp = 0.0;
            temp = (this.a0 * this.a0) + (this.c0 * this.c0);
            if ((temp < 0.0)) {
                temp = 0.0;
            }
            temp = sqrt(temp);
            if ((temp == 0.0)) {
                if ((this.b0 < 0)) {
                    result = 64;
                } else {
                    result = 256 - 64;
                }
            } else {
                temp = this.b0 / temp;
                temp = arctan(temp);
                result = intround(-temp * 256 / (2 * 3.1415926));
            }
        } catch (Exception e) {
            result = 0;
        }
        return result;
    }
    
    public byte angleZ() {
        result = 0;
        float temp = 0.0;
        
        try {
            result = 0;
            temp = 0.0;
            temp = (this.a1 * this.a1) + (this.c1 * this.c1);
            if ((temp < 0.0)) {
                temp = 0.0;
            }
            temp = sqrt(temp);
            if ((temp == 0.0)) {
                if ((this.b1 < 0)) {
                    result = 64;
                } else {
                    result = 256 - 64;
                }
            } else {
                temp = this.b1 / temp;
                temp = arctan(temp);
                result = intround(-temp * 256 / (2 * 3.1415926));
            }
        } catch (Exception e) {
            result = 0;
        }
        return result;
    }
    
}
//these can only be triangular
class KfTriangle extends TObject {
    public TColor foreColor;
    public TColor backColor;
    public TColor lineColor;
    public float zForSorting;
    public boolean backFacing;
    public float lineWidth;
    public boolean isLine;
    public  points;
    public KfObject3D tdo;
    public long plantPartID;
    
    // ---------------------------------------------------------------------------------- KfTriangle updating 
    public void updateGeometry() {
        this.computeBackFacing();
        this.computeZ();
    }
    
    public void computeBackFacing() {
        KfPoint3d point0 = new KfPoint3d();
        KfPoint3d point1 = new KfPoint3d();
        KfPoint3d point2 = new KfPoint3d();
        float backfacingResult = 0.0;
        
        this.backFacing = false;
        if (this.isLine) {
            return;
        }
        point0 = this.points[0];
        point1 = this.points[1];
        point2 = this.points[2];
        backfacingResult = ((point1.x - point0.x) * (point2.y - point0.y)) - ((point1.y - point0.y) * (point2.x - point0.x));
        this.backFacing = (backfacingResult < 0);
    }
    
    public void computeZ() {
        float minZ = 0.0;
        
        if (this.isLine) {
            minZ = this.points[0].z;
            if (this.points[1].z < minZ) {
                minZ = this.points[1].z;
            }
        } else {
            minZ = this.points[0].z;
            if (this.points[1].z < minZ) {
                minZ = this.points[1].z;
            }
            if (this.points[2].z < minZ) {
                minZ = this.points[2].z;
            }
        }
        this.zForSorting = minZ;
    }
    
    public TColor visibleSurfaceColor() {
        result = new TColor();
        if (this.backFacing) {
            result = this.backColor;
        } else {
            result = this.foreColor;
        }
        return result;
    }
    
    public TColor invisibleSurfaceColor() {
        result = new TColor();
        if (this.backFacing) {
            result = this.foreColor;
        } else {
            result = this.backColor;
        }
        return result;
    }
    
    public TColor drawLinesColor(short lineContrastIndex) {
        result = new TColor();
        if (this.backFacing) {
            result = this.backColor;
        } else {
            result = this.foreColor;
        }
        if (lineContrastIndex > 0) {
            result = usupport.darkerColorWithSubtraction(result, 10 * lineContrastIndex);
        }
        return result;
    }
    
}
