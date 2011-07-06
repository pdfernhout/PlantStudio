// unit Utdo

from conversion_common import *;
import u3dexport;
import u3dsupport;
import uplant;
import usupport;
import uturtle;
import ufiler;
import usstream;
import ucollect;
import delphi_compatability;

// const
kMaximumRecordedPoints = 10000;
kAdjustForOrigin = true;
kDontAdjustForOrigin = false;
kEmbeddedInPlant = true;
kInTdoLibrary = false;
kStandAloneFile = false;
kTdoForeColor = delphi_compatability.clSilver;
kTdoBackColor = delphi_compatability.clGray;
kTdoLineContrastIndex = 10;
kStartTdoString = "start 3D object";
kEndTdoString = "end 3D object";


// v1.6b2 changed from 200 to 1000 ; v2.0 changed to 10000 (not in tdo anymore)
// v1.11 moved up here
// v1.11 moved up here
// record
class KfPoint3D {
    public float x;
    public float y;
    public float z;
}



// ---------------------------------------------------------------------------------- KfPoint3D 
public void KfPoint3D_setXYZ(KfPoint3D thePoint, float aX, float aY, float aZ) {
    thePoint.x = aX;
    thePoint.y = aY;
    thePoint.z = aZ;
}

public void KfPoint3D_addXYZ(KfPoint3D thePoint, float xOffset, float yOffset, float zOffset) {
    //pdf - shift point by x y and z.
    thePoint.x = thePoint.x + xOffset;
    thePoint.y = thePoint.y + yOffset;
    thePoint.z = thePoint.z + zOffset;
}

public void KfPoint3D_scaleBy(KfPoint3D thePoint, float aScale) {
    //pdf - multiply point by scale.
    thePoint.x = thePoint.x * aScale;
    thePoint.y = thePoint.y * aScale;
    thePoint.z = thePoint.z * aScale;
}

public void KfPoint3D_subtract(KfPoint3D thePoint, KfPoint3D aPoint) {
    //pdf - subtract point from this point.
    thePoint.x = thePoint.x - aPoint.x;
    thePoint.y = thePoint.y - aPoint.y;
    thePoint.z = thePoint.z - aPoint.z;
}

public boolean KfPoint3D_matchXYZ(KfPoint3D pointOne, KfPoint3D pointTwo, float matchDistance) {
    result = false;
    // v1.6b1 added
    result = (abs(pointOne.x - pointTwo.x) <= matchDistance) && (abs(pointOne.y - pointTwo.y) <= matchDistance) && (abs(pointOne.z - pointTwo.z) <= matchDistance);
    return result;
}

public void KfPoint3D_addPointToBoundsRect(TRect boundsRect, KfPoint3d aPoint) {
    long x = 0;
    long y = 0;
    
    try {
        x = intround(aPoint.x);
    } catch (Exception e) {
        x = 0;
    }
    try {
        y = intround(aPoint.y);
    } catch (Exception e) {
        y = 0;
    }
    if ((boundsRect.Left == 0) && (boundsRect.Right == 0) && (boundsRect.Top == 0) && (boundsRect.Bottom == 0)) {
        // on first point entered, initialize bounds rect
        boundsRect.Left = x;
        boundsRect.Right = x;
        boundsRect.Top = y;
        boundsRect.Bottom = y;
    } else {
        if (x < boundsRect.Left) {
            boundsRect.Left = x;
        } else if (x > boundsRect.Right) {
            boundsRect.Right = x;
        }
        if (y < boundsRect.Top) {
            boundsRect.Top = y;
        } else if (y > boundsRect.Bottom) {
            boundsRect.Bottom = y;
        }
    }
}

// const
kPointAllocationIncrement = 8;


public String betweenBrackets(String aString) {
    result = "";
    // lose letter and [ on front, lose ] on back 
    result = UNRESOLVED.copy(aString, 3, len(aString) - 3);
    return result;
}


class KfIndexTriangle extends PdStreamableObject {
    public  pointIndexes;
    
    // ---------------------------------------------------------------------------------- KfIndexTriangle 
    public void createABC(long a, long b, long c) {
        this.create();
        this.pointIndexes[0] = a;
        this.pointIndexes[1] = b;
        this.pointIndexes[2] = c;
    }
    
    public void flip() {
        long savePoint = 0;
        
        savePoint = this.pointIndexes[0];
        this.pointIndexes[0] = this.pointIndexes[2];
        this.pointIndexes[2] = savePoint;
    }
    
    public void copyFrom(KfIndexTriangle aTriangle) {
        if (aTriangle == null) {
            return;
        }
        this.pointIndexes[0] = aTriangle.pointIndexes[0];
        this.pointIndexes[1] = aTriangle.pointIndexes[1];
        this.pointIndexes[2] = aTriangle.pointIndexes[2];
    }
    
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kKfIndexTriangle;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        super.streamDataWithFiler(filer, cvir);
        this.pointIndexes = filer.streamBytes(this.pointIndexes, FIX_sizeof(this.pointIndexes));
    }
    
}
class KfObject3D extends PdStreamableObject {
    public PKfPoint3DArray pointData;
    public long pointsInUse;
    public long pointsAllocated;
    public long originPointIndex;
    public TListCollection triangles;
    public String name;
    public KfObject3D originalIfCopy;
    public boolean inUse;
    public float zForSorting;
    public short indexWhenRemoved;
    public short selectedIndexWhenRemoved;
    public TRect boundsRect;
    
    // doesn't need to be streamed, only used while drawing
    // ---------------------------------------------------------------------------------- KfObject3D 
    public void create() {
        super.create();
        this.triangles = ucollect.TListCollection().Create();
    }
    
    public void destroy() {
        this.triangles.free;
        this.triangles = null;
        if (this.pointData != null) {
            UNRESOLVED.FreeMem(this.pointData);
        }
        super.destroy();
    }
    
    public void ensureEnoughSpaceForNewPointData(long totalNumberOfPointsToBeUsed) {
        if (this.pointsAllocated >= totalNumberOfPointsToBeUsed) {
            return;
        }
        if (this.pointData == null) {
            if (totalNumberOfPointsToBeUsed < kPointAllocationIncrement) {
                totalNumberOfPointsToBeUsed = kPointAllocationIncrement;
            }
            // assuming this throws its own memory exception
            UNRESOLVED.GetMem(this.pointData, totalNumberOfPointsToBeUsed * FIX_sizeof(KfPoint3D));
        } else {
            if (totalNumberOfPointsToBeUsed % kPointAllocationIncrement != 0) {
                totalNumberOfPointsToBeUsed = totalNumberOfPointsToBeUsed + kPointAllocationIncrement - (totalNumberOfPointsToBeUsed % kPointAllocationIncrement);
            }
            UNRESOLVED.ReallocMem(this.pointData, totalNumberOfPointsToBeUsed * FIX_sizeof(KfPoint3D));
            // assuming this throws its own memory exception
        }
        this.pointsAllocated = totalNumberOfPointsToBeUsed;
    }
    
    public KfPoint3d getPoint(int index) {
        result = new KfPoint3d();
        result = this.pointData.PDF_FIX_POINTER_ACCESS[index];
        return result;
    }
    
    public void setPoint(int index, KfPoint3d aPoint) {
        if (this.pointData == null) {
            throw new GeneralException.create("Problem: Nil pointer in method KfObject3D.setPoint.");
        }
        this.pointData.PDF_FIX_POINTER_ACCESS[index] = aPoint;
    }
    
    public void clear() {
        this.clearPoints();
        this.name = "";
    }
    
    public void clearPoints() {
        this.pointsInUse = 0;
        this.originPointIndex = 0;
        this.triangles.clear();
    }
    
    public void copyFrom(KfObject3D original) {
        int i = 0;
        KfIndexTriangle theTriangle = new KfIndexTriangle();
        
        if (original == null) {
            return;
        }
        this.setName(original.name);
        this.ensureEnoughSpaceForNewPointData(original.pointsInUse);
        if (original.pointsInUse > 0) {
            for (i = 0; i <= original.pointsInUse - 1; i++) {
                this.points[i] = original.points[i];
            }
        }
        this.pointsInUse = original.pointsInUse;
        this.originPointIndex = original.originPointIndex;
        this.triangles.clear();
        if (original.triangles.Count > 0) {
            for (i = 0; i <= original.triangles.Count - 1; i++) {
                theTriangle = original.triangles.Items[i];
                this.addTriangle(KfIndexTriangle().createABC(theTriangle.pointIndexes[0], theTriangle.pointIndexes[1], theTriangle.pointIndexes[2]));
            }
        }
        this.inUse = original.inUse;
    }
    
    public boolean isSameAs(KfObject3D other) {
        result = false;
        long i = 0;
        long j = 0;
        KfPoint3d thePoint = new KfPoint3d();
        KfIndexTriangle theTriangle = new KfIndexTriangle();
        KfPoint3d otherPoint = new KfPoint3d();
        KfIndexTriangle otherTriangle = new KfIndexTriangle();
        
        //false if fails any test
        result = false;
        if (this.name != other.name) {
            return result;
        }
        if (this.pointsInUse != other.pointsInUse) {
            return result;
        }
        if (this.originPointIndex != other.originPointIndex) {
            return result;
        }
        if (this.triangles.Count != other.triangles.Count) {
            return result;
        }
        if (this.pointsInUse > 0) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                thePoint = this.points[i];
                otherPoint = other.points[i];
                if ((intround(thePoint.x) != intround(otherPoint.x)) || (intround(thePoint.y) != intround(otherPoint.y)) || (intround(thePoint.z) != intround(otherPoint.z))) {
                    // round these because otherwise i/o inaccuracies could make a tdo seem different when it isn't,
                    // and most numbers are far enough to be integers anyway
                    return result;
                }
            }
        }
        if (this.triangles.Count > 0) {
            for (i = 0; i <= this.triangles.Count - 1; i++) {
                theTriangle = this.triangles.Items[i];
                otherTriangle = other.triangles.Items[i];
                for (j = 0; j <= 2; j++) {
                    if (theTriangle.pointIndexes[j] != otherTriangle.pointIndexes[j]) {
                        return result;
                    }
                }
            }
        }
        //passed all the tests
        result = true;
        return result;
    }
    
    public String getName() {
        result = "";
        result = this.name;
        return result;
    }
    
    public void setName(String newName) {
        this.name = UNRESOLVED.copy(newName, 1, 80);
    }
    
    public short addPoint(KfPoint3d aPoint) {
        result = 0;
        // v2.0 removed this check
        //if pointsInUse >= kMaximumRecordedPoints then
        //  raise Exception.create('Problem: Too many points in 3D object.');
        this.ensureEnoughSpaceForNewPointData(this.pointsInUse + 1);
        this.points[this.pointsInUse] = aPoint;
        this.pointsInUse += 1;
        result = this.pointsInUse;
        return result;
    }
    
    public void removePoint(short point) {
        short i = 0;
        
        if (Point <= this.pointsInUse - 2) {
            for (i = Point; i <= this.pointsInUse - 2; i++) {
                this.points[i] = this.points[i + 1];
            }
        }
        this.deletePointIndexInTriangles(Point);
        // never releasing memory until entire object freed
        this.pointsInUse -= 1;
        if (this.originPointIndex > this.pointsInUse - 1) {
            this.originPointIndex = this.pointsInUse - 1;
        }
    }
    
    public short addPointIfNoMatch(KfPoint3d aPoint, float matchDistance) {
        result = 0;
        short i = 0;
        
        if (this.pointsInUse > 0) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                if (KfPoint3D_matchXYZ(aPoint, this.points[i], matchDistance)) {
                    //add 1 because triangle indexes start at 1
                    result = i + 1;
                    return result;
                }
            }
        }
        result = this.addPoint(aPoint);
        return result;
    }
    
    //PDF FIX - may want to optimize this to use var to pass around result rather than assign
    public KfPoint3D pointForIndex(long anIndex) {
        result = new KfPoint3D();
        if ((anIndex < 1) || (anIndex > this.pointsInUse)) {
            throw new GeneralException.create("Problem: Point index out of range in method KfObject3D.pointForIndex.");
        }
        result = this.points[anIndex - 1];
        return result;
    }
    
    public void addTriangle(KfIndexTriangle aTriangle) {
        this.triangles.Add(aTriangle);
    }
    
    public KfIndexTriangle triangleForIndex(long anIndex) {
        result = new KfIndexTriangle();
        if ((anIndex < 1) || (anIndex > this.triangles.Count)) {
            throw new GeneralException.create("Problem: Triangle index out of range in method KfObject3D.triangleForIndex.");
        }
        result = this.triangles.Items[anIndex - 1];
        return result;
    }
    
    //adjust all points for origin, which is assumed to be at the first point
    //in terms of plant organs, this means the first point is
    //where the organ is attached to the plant
    public void adjustForOrigin() {
        long i = 0;
        KfPoint3d tempPoint = new KfPoint3d();
        
        if (this.pointsInUse < 1) {
            return;
        }
        if (this.originPointIndex < 0) {
            this.originPointIndex = 0;
        }
        if (this.originPointIndex > this.pointsInUse - 1) {
            this.originPointIndex = this.pointsInUse - 1;
        }
        if (this.pointsInUse > 1) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                if (i != this.originPointIndex) {
                    tempPoint = this.points[i];
                    KfPoint3D_subtract(tempPoint, this.points[this.originPointIndex]);
                    this.points[i] = tempPoint;
                }
            }
        }
        //makes the first point zero
        tempPoint = this.points[this.originPointIndex];
        KfPoint3D_setXYZ(tempPoint, 0.0, 0.0, 0.0);
        this.points[this.originPointIndex] = tempPoint;
    }
    
    public void setOriginPointIndex(int newOriginPointIndex) {
        boolean changed = false;
        
        changed = (this.originPointIndex != newOriginPointIndex);
        this.originPointIndex = newOriginPointIndex;
        if (changed) {
            this.adjustForOrigin();
        }
    }
    
    public void makeMirrorTriangles() {
        short triangleCountAtStart = 0;
         newPointIndexes = [0] * (range(0, 2 + 1) + 1);
        short i = 0;
        short j = 0;
        KfPoint3D aPoint = new KfPoint3D();
        KfIndexTriangle triangle = new KfIndexTriangle();
        
        this.adjustForOrigin();
        triangleCountAtStart = this.triangles.Count;
        if (triangleCountAtStart > 0) {
            for (i = 0; i <= triangleCountAtStart - 1; i++) {
                triangle = KfIndexTriangle(this.triangles[i]);
                for (j = 0; j <= 2; j++) {
                    aPoint = this.pointForIndex(triangle.pointIndexes[j]);
                    aPoint.x = -1 * aPoint.x;
                    newPointIndexes[j] = this.addPointIfNoMatch(aPoint, 1.0);
                }
                // reversing order of points makes triangle have correct facing for opposite side
                this.addTriangle(KfIndexTriangle().createABC(newPointIndexes[2], newPointIndexes[1], newPointIndexes[0]));
            }
        }
    }
    
    public void reverseZValues() {
        short i = 0;
        KfPoint3d tempPoint = new KfPoint3d();
        
        this.adjustForOrigin();
        if (this.pointsInUse > 0) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                tempPoint = this.points[i];
                tempPoint.z = -1 * tempPoint.z;
                this.points[i] = tempPoint;
            }
        }
    }
    
    public TPoint bestPointForDrawingAtScale(TObject turtleProxy, TPoint origin, TPoint bitmapSize, float scale) {
        result = new TPoint();
        long i = 0;
        KfTurtle turtle = new KfTurtle();
        
        turtle = uturtle.KfTurtle(turtleProxy);
        this.boundsRect = Rect(0, 0, 0, 0);
        turtle.reset();
        if (this.pointsInUse > 0) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                KfPoint3D_addPointToBoundsRect(this.boundsRect, turtle.transformAndRecord(this.points[i], scale));
            }
        }
        result.X = origin.X + bitmapSize.X / 2 - usupport.rWidth(this.boundsRect) / 2 - this.boundsRect.Left;
        result.Y = origin.Y + bitmapSize.Y / 2 - usupport.rHeight(this.boundsRect) / 2 - this.boundsRect.Top;
        return result;
    }
    
    public TRect draw(TObject turtleProxy, float scale, String longName, String shortName, short dxfIndex, long partID) {
        result = new TRect();
        long i = 0;
        KfIndexTriangle triangle = new KfIndexTriangle();
        KfTriangle realTriangle = new KfTriangle();
        KfTurtle turtle = new KfTurtle();
        float minZ = 0.0;
        
        result = Rect(0, 0, 0, 0);
        minZ = 0;
        this.zForSorting = 0;
        turtle = uturtle.KfTurtle(turtleProxy);
        if (turtle.ifExporting_exclude3DObject(scale)) {
            return result;
        }
        turtle.clearRecording();
        this.boundsRect = Rect(0, 0, 0, 0);
        if (this.pointsInUse > 0) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                KfPoint3D_addPointToBoundsRect(this.boundsRect, turtle.transformAndRecord(this.points[i], scale));
            }
        }
        result = this.boundsRect;
        if (!turtle.drawOptions.draw3DObjects) {
            return result;
        }
        if (turtle.drawOptions.draw3DObjectsAsRects) {
            turtle.drawTrianglesFromBoundsRect(this.boundsRect);
            return result;
        }
        // prepare
        turtle.ifExporting_start3DObject(longName + " 3D object", shortName, turtle.drawingSurface.foreColor, dxfIndex);
        if (turtle.exportingToFile()) {
            // draw
            this.write3DExportElements(turtle, scale, partID);
        } else if (this.triangles.Count > 0) {
            for (i = 1; i <= this.triangles.Count; i++) {
                triangle = this.triangleForIndex(i);
                realTriangle = turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[1], triangle.pointIndexes[2], partID);
                if ((turtle.drawOptions.sortPolygons) && (turtle.drawOptions.sortTdosAsOneItem) && (realTriangle != null)) {
                    if (i == 1) {
                        minZ = realTriangle.zForSorting;
                    } else if (realTriangle.zForSorting < minZ) {
                        minZ = realTriangle.zForSorting;
                    }
                    realTriangle.tdo = this;
                }
            }
        }
        this.zForSorting = minZ;
        turtle.ifExporting_end3DObject();
        return result;
    }
    
    public void overlayBoundsRect(TObject turtleProxy, float scale) {
        long i = 0;
        KfTurtle turtle = new KfTurtle();
        boolean oldSetting = false;
        
        turtle = uturtle.KfTurtle(turtleProxy);
        oldSetting = turtle.drawingSurface.fillingTriangles;
        turtle.drawingSurface.fillingTriangles = false;
        turtle.drawTrianglesFromBoundsRect(this.boundsRect);
        turtle.drawingSurface.fillingTriangles = oldSetting;
    }
    
    public void write3DExportElements(TObject turtleProxy, float scale, short partID) {
        KfFileExportSurface fileExportSurface = new KfFileExportSurface();
        short i = 0;
        KfTurtle turtle = new KfTurtle();
        KfIndexTriangle triangle = new KfIndexTriangle();
        long firstPtIndex = 0;
        
        // do NOT pass the array on because a tdo could be really big
        // some write out lists of points then triangles; some draw each triangle
        turtle = uturtle.KfTurtle(turtleProxy);
        fileExportSurface = turtle.fileExportSurface();
        if (fileExportSurface == null) {
            throw new GeneralException.create("Problem: No 3D drawing surface in method KfObject3D.write3DExportElements.");
        }
        switch (turtle.writingTo) {
            case u3dexport.k3DS:
                fileExportSurface.startVerticesAndTriangles();
                if (turtle.writingToLWO()) {
                    firstPtIndex = fileExportSurface.numPoints;
                } else {
                    firstPtIndex = 0;
                }
                if (this.pointsInUse > 0) {
                    for (i = 0; i <= this.pointsInUse - 1; i++) {
                        fileExportSurface.addPoint(turtle.transformAndRecord(this.points[i], scale));
                    }
                }
                for (i = 1; i <= this.triangles.Count; i++) {
                    triangle = this.triangleForIndex(i);
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1);
                    if (fileExportSurface.options.makeTrianglesDoubleSided) {
                        fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1);
                    }
                }
                fileExportSurface.endVerticesAndTriangles();
                // PDF PORT -- added semicolon
                break;
            case u3dexport.kOBJ:
                fileExportSurface.startVerticesAndTriangles();
                if (turtle.writingToLWO()) {
                    firstPtIndex = fileExportSurface.numPoints;
                } else {
                    firstPtIndex = 0;
                }
                if (this.pointsInUse > 0) {
                    for (i = 0; i <= this.pointsInUse - 1; i++) {
                        fileExportSurface.addPoint(turtle.transformAndRecord(this.points[i], scale));
                    }
                }
                for (i = 1; i <= this.triangles.Count; i++) {
                    triangle = this.triangleForIndex(i);
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1);
                    if (fileExportSurface.options.makeTrianglesDoubleSided) {
                        fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1);
                    }
                }
                fileExportSurface.endVerticesAndTriangles();
                // PDF PORT -- added semicolon
                break;
            case u3dexport.kVRML:
                fileExportSurface.startVerticesAndTriangles();
                if (turtle.writingToLWO()) {
                    firstPtIndex = fileExportSurface.numPoints;
                } else {
                    firstPtIndex = 0;
                }
                if (this.pointsInUse > 0) {
                    for (i = 0; i <= this.pointsInUse - 1; i++) {
                        fileExportSurface.addPoint(turtle.transformAndRecord(this.points[i], scale));
                    }
                }
                for (i = 1; i <= this.triangles.Count; i++) {
                    triangle = this.triangleForIndex(i);
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1);
                    if (fileExportSurface.options.makeTrianglesDoubleSided) {
                        fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1);
                    }
                }
                fileExportSurface.endVerticesAndTriangles();
                // PDF PORT -- added semicolon
                break;
            case u3dexport.kLWO:
                fileExportSurface.startVerticesAndTriangles();
                if (turtle.writingToLWO()) {
                    firstPtIndex = fileExportSurface.numPoints;
                } else {
                    firstPtIndex = 0;
                }
                if (this.pointsInUse > 0) {
                    for (i = 0; i <= this.pointsInUse - 1; i++) {
                        fileExportSurface.addPoint(turtle.transformAndRecord(this.points[i], scale));
                    }
                }
                for (i = 1; i <= this.triangles.Count; i++) {
                    triangle = this.triangleForIndex(i);
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1);
                    if (fileExportSurface.options.makeTrianglesDoubleSided) {
                        fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1);
                    }
                }
                fileExportSurface.endVerticesAndTriangles();
                // PDF PORT -- added semicolon
                break;
            default:
                for (i = 1; i <= this.triangles.Count; i++) {
                    triangle = this.triangleForIndex(i);
                    turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[1], triangle.pointIndexes[2], partID);
                    if (fileExportSurface.options.makeTrianglesDoubleSided) {
                        turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[2], triangle.pointIndexes[1], partID);
                    }
                }
                break;
    }
    
    public void addTriangleWithVerticesABC(long a, long b, long c) {
        this.addTriangle(KfIndexTriangle().createABC(a, b, c));
    }
    
    public void removeTriangle(KfIndexTriangle aTriangle) {
        this.triangles.Remove(aTriangle);
        this.removePointsNotInUse();
    }
    
    public void removePointsNotInUse() {
        short i = 0;
        short pointToRemove = 0;
        boolean done = false;
        
        if (this.pointsInUse <= 0) {
            return;
        }
        done = false;
        while (!done) {
            pointToRemove = -1;
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                if (!this.pointIsReallyInUse(i)) {
                    pointToRemove = i;
                    break;
                }
            }
            if (pointToRemove >= 0) {
                this.removePoint(pointToRemove);
            } else {
                done = true;
            }
        }
    }
    
    public boolean pointIsReallyInUse(short point) {
        result = false;
        KfIndexTriangle triangle = new KfIndexTriangle();
        short i = 0;
        short j = 0;
        short adjustedPoint = 0;
        
        result = false;
        // triangle indexes start at 1, not 0 
        adjustedPoint = Point + 1;
        if (this.triangles.Count > 0) {
            for (i = 0; i <= this.triangles.Count - 1; i++) {
                triangle = KfIndexTriangle(this.triangles.Items[i]);
                for (j = 0; j <= 2; j++) {
                    if (triangle.pointIndexes[j] == adjustedPoint) {
                        result = true;
                        return result;
                    }
                }
            }
        }
        return result;
    }
    
    public void deletePointIndexInTriangles(short oldPointIndex) {
        KfIndexTriangle triangle = new KfIndexTriangle();
        short i = 0;
        short j = 0;
        short adjustedOldPointIndex = 0;
        
        // triangle indexes start at 1, not 0 
        adjustedOldPointIndex = oldPointIndex + 1;
        if (this.triangles.Count > 0) {
            for (i = 0; i <= this.triangles.Count - 1; i++) {
                triangle = KfIndexTriangle(this.triangles.Items[i]);
                for (j = 0; j <= 2; j++) {
                    if (triangle.pointIndexes[j] > adjustedOldPointIndex) {
                        triangle.pointIndexes[j] = triangle.pointIndexes[j] - 1;
                    }
                }
            }
        }
    }
    
    //parse string into xyz positions and add point to collection
    public void addPointString(KfStringStream stream) {
        KfPoint3D aPoint3D = new KfPoint3D();
        int x = 0;
        int y = 0;
        int z = 0;
        
        x = 0;
        y = 0;
        z = 0;
        x = stream.nextInteger();
        y = stream.nextInteger();
        z = stream.nextInteger();
        KfPoint3D_setXYZ(aPoint3D, x, y, z);
        this.addPoint(aPoint3D);
    }
    
    //parse string into three point indexes and add triangle to collection
    public void addTriangleString(KfStringStream stream) {
        int p1 = 0;
        int p2 = 0;
        int p3 = 0;
        
        p1 = 0;
        p2 = 0;
        p3 = 0;
        p1 = stream.nextInteger();
        p2 = stream.nextInteger();
        p3 = stream.nextInteger();
        if ((p1 == 0) || (p2 == 0) || (p3 == 0) || (p1 > this.pointsInUse) || (p2 > this.pointsInUse) || (p3 > this.pointsInUse)) {
            MessageDialog("Bad triangle: " + IntToStr(p1) + " " + IntToStr(p2) + " " + IntToStr(p3) + ". Point indexes must be between 1 and " + IntToStr(this.pointsInUse) + ".", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
        } else {
            this.addTriangle(KfIndexTriangle().createABC(p1, p2, p3));
        }
    }
    
    public void writeToFile(String fileName) {
        TextFile outputFile = new TextFile();
        
        AssignFile(outputFile, fileName);
        try {
            // v1.5
            usupport.setDecimalSeparator();
            Rewrite(outputFile);
            this.writeToFileStream(outputFile, kStandAloneFile);
        } finally {
            CloseFile(outputFile);
        }
    }
    
    public void readFromFile(String fileName) {
        TextFile inputFile = new TextFile();
        
        AssignFile(inputFile, fileName);
        try {
            // v1.5
            usupport.setDecimalSeparator();
            Reset(inputFile);
            this.readFromFileStream(inputFile, kStandAloneFile);
        } finally {
            CloseFile(inputFile);
        }
    }
    
    public void writeToMemo(TMemo aMemo) {
        short i = 0;
        KfIndexTriangle triangle = new KfIndexTriangle();
        
        aMemo.Lines.Add("  " + kStartTdoString);
        aMemo.Lines.Add("  Name=" + this.getName());
        if (this.pointsInUse > 0) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                aMemo.Lines.Add("  Point=" + IntToStr(intround(this.points[i].x)) + " " + IntToStr(intround(this.points[i].y)) + " " + IntToStr(intround(this.points[i].z)));
            }
        }
        aMemo.Lines.Add("; Origin=" + IntToStr(this.originPointIndex));
        if (this.triangles.Count > 0) {
            for (i = 0; i <= this.triangles.Count - 1; i++) {
                triangle = KfIndexTriangle(this.triangles[i]);
                aMemo.Lines.Add("  Triangle=" + IntToStr(triangle.pointIndexes[0]) + " " + IntToStr(triangle.pointIndexes[1]) + " " + IntToStr(triangle.pointIndexes[2]));
            }
        }
        aMemo.Lines.Add("  " + kEndTdoString);
    }
    
    public void writeToFileStream(TextFile outputFile, boolean embeddedInPlant) {
        short i = 0;
        KfIndexTriangle triangle = new KfIndexTriangle();
        
        if (embeddedInPlant) {
            writeln(outputFile, "  " + kStartTdoString);
        }
        if (embeddedInPlant) {
            write(outputFile, "  ");
        }
        writeln(outputFile, "Name=" + this.getName());
        if (this.pointsInUse > 0) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                writeln(outputFile, "  Point=" + IntToStr(intround(this.points[i].x)) + " " + IntToStr(intround(this.points[i].y)) + " " + IntToStr(intround(this.points[i].z)));
            }
        }
        writeln(outputFile, "; Origin=" + IntToStr(this.originPointIndex));
        if (this.triangles.Count > 0) {
            for (i = 0; i <= this.triangles.Count - 1; i++) {
                triangle = KfIndexTriangle(this.triangles[i]);
                writeln(outputFile, "  Triangle=" + IntToStr(triangle.pointIndexes[0]) + " " + IntToStr(triangle.pointIndexes[1]) + " " + IntToStr(triangle.pointIndexes[2]));
            }
        }
        if (embeddedInPlant) {
            writeln(outputFile, "  " + kEndTdoString);
        } else {
            writeln(outputFile);
        }
    }
    
    public void readFromFileStream(TextFile inputFile, boolean embeddedInPlant) {
        String inputLine = "";
        String fieldType = "";
        KfStringStream stream = new KfStringStream();
        
        this.pointsInUse = 0;
        this.originPointIndex = 0;
        this.triangles.clear();
        if (embeddedInPlant) {
            UNRESOLVED.readln(inputFile, inputLine);
            if ((embeddedInPlant) && (trim(inputLine) == "")) {
                // cfk change for v1.3 added '' case
                UNRESOLVED.readln(inputFile, inputLine);
            }
            if ((UNRESOLVED.copy(inputLine, 1, 1) == ";") && (UNRESOLVED.pos("ORIGIN", uppercase(inputLine)) <= 0)) {
                // cfk change for v1.6b2 mistake with origin, placed with comment
                UNRESOLVED.readln(inputFile, inputLine);
            }
            if (UNRESOLVED.pos(uppercase(kStartTdoString), uppercase(inputLine)) <= 0) {
                throw new GeneralException.create("Problem: Expected start of 3D object.");
            }
        }
        stream = null;
        try {
            //read info for 3D object from file at current position
            stream = usstream.KfStringStream.create;
            while (!UNRESOLVED.eof(inputFile)) {
                UNRESOLVED.readln(inputFile, inputLine);
                if ((embeddedInPlant) && (trim(inputLine) == "")) {
                    // cfk change v1.3 added '' case
                    continue;
                }
                if ((UNRESOLVED.copy(inputLine, 1, 1) == ";") && (UNRESOLVED.pos("ORIGIN", uppercase(inputLine)) <= 0)) {
                    // cfk change for v1.6b2 mistake with origin, placed with comment
                    continue;
                }
                if ((!embeddedInPlant) && (UNRESOLVED.pos("[", inputLine) == 1)) {
                    //ignore old thing in brackets
                    continue;
                }
                stream.onStringSeparator(inputLine, "=");
                fieldType = stream.nextToken();
                stream.spaceSeparator();
                if (UNRESOLVED.pos("POINT", uppercase(fieldType)) > 0) {
                    this.addPointString(stream);
                } else if (UNRESOLVED.pos("ORIGIN", uppercase(fieldType)) > 0) {
                    this.setOriginPointIndex(StrToIntDef(stream.remainder, 0));
                } else if (UNRESOLVED.pos("TRIANGLE", uppercase(fieldType)) > 0) {
                    this.addTriangleString(stream);
                } else if (UNRESOLVED.pos("NAME", uppercase(fieldType)) > 0) {
                    this.setName(stream.remainder);
                } else {
                    break;
                }
            }
            this.adjustForOrigin();
            if (embeddedInPlant) {
                if (UNRESOLVED.pos(uppercase(kEndTdoString), uppercase(inputLine)) <= 0) {
                    throw new GeneralException.create("Problem: Expected end of 3D object.");
                }
            }
        } finally {
            stream.free;
        }
    }
    
    public void readFromDXFFile(TextFile inputFile) {
        String identifierLine = "";
        String valueLine = "";
         newPoints = [0] * (range(0, 2 + 1) + 1);
         newTriangleIndexes = [0] * (range(0, 2 + 1) + 1);
        int pointsRead = 0;
        
        this.pointsInUse = 0;
        this.originPointIndex = 0;
        pointsRead = 0;
        this.triangles.clear();
        newPoints[0].x = 0;
        newPoints[0].y = 0;
        newPoints[0].z = 0;
        newPoints[1].x = 0;
        newPoints[1].y = 0;
        newPoints[1].z = 0;
        newPoints[2].x = 0;
        newPoints[2].y = 0;
        newPoints[2].z = 0;
        while (!UNRESOLVED.eof(inputFile)) {
            UNRESOLVED.readln(inputFile, identifierLine);
            identifierLine = trim(identifierLine);
            UNRESOLVED.readln(inputFile, valueLine);
            valueLine = trim(valueLine);
            if (identifierLine == "10") {
                // v1.60final changed this from else to all ifs; something wrong in Delphi, I think
                // first point
                newPoints[0].x = StrToFloat(valueLine);
            }
            if (identifierLine == "20") {
                newPoints[0].y = -1 * StrToFloat(valueLine);
            }
            if (identifierLine == "30") {
                newPoints[0].z = StrToFloat(valueLine);
            }
            if (identifierLine == "11") {
                // second point
                newPoints[1].x = StrToFloat(valueLine);
            }
            if (identifierLine == "21") {
                newPoints[1].y = -1 * StrToFloat(valueLine);
            }
            if (identifierLine == "31") {
                newPoints[1].z = StrToFloat(valueLine);
            }
            if (identifierLine == "12") {
                // third point
                newPoints[2].x = StrToFloat(valueLine);
            }
            if (identifierLine == "22") {
                newPoints[2].y = -1 * StrToFloat(valueLine);
            }
            if (identifierLine == "32") {
                newPoints[2].z = StrToFloat(valueLine);
            }
            if (identifierLine == "13") {
                // end (ignoring fourth point)
                pointsRead += 3;
                // make new triangle
                newTriangleIndexes[0] = this.addPointIfNoMatch(newPoints[0], 0.1);
                newTriangleIndexes[1] = this.addPointIfNoMatch(newPoints[1], 0.1);
                newTriangleIndexes[2] = this.addPointIfNoMatch(newPoints[2], 0.1);
                this.addTriangle(KfIndexTriangle().createABC(newTriangleIndexes[0], newTriangleIndexes[1], newTriangleIndexes[2]));
                // reset points for next time
                newPoints[0].x = 0;
                newPoints[0].y = 0;
                newPoints[0].z = 0;
                newPoints[1].x = 0;
                newPoints[1].y = 0;
                newPoints[1].z = 0;
                newPoints[2].x = 0;
                newPoints[2].y = 0;
                newPoints[2].z = 0;
            }
        }
        this.adjustForOrigin();
    }
    
    public void readFromMemo(TMemo aMemo, long readingMemoLine) {
        String inputLine = "";
        String fieldType = "";
        KfStringStream stream = new KfStringStream();
        
        this.pointsInUse = 0;
        this.originPointIndex = 0;
        this.triangles.clear();
        inputLine = aMemo.Lines.Strings[readingMemoLine];
        readingMemoLine += 1;
        if (trim(inputLine) == "") {
            // cfk change v1.60final added '' case
            // skip commented lines 
            inputLine = aMemo.Lines.Strings[readingMemoLine];
            readingMemoLine += 1;
        }
        if ((UNRESOLVED.copy(inputLine, 1, 1) == ";") && (UNRESOLVED.pos("ORIGIN", uppercase(inputLine)) <= 0)) {
            // cfk change for v1.6b2 mistake with origin, placed with comment
            // skip commented lines 
            inputLine = aMemo.Lines.Strings[readingMemoLine];
            readingMemoLine += 1;
        }
        if (UNRESOLVED.pos(uppercase(kStartTdoString), uppercase(inputLine)) <= 0) {
            throw new GeneralException.create("Problem: Expected start of 3D object.");
        }
        stream = null;
        try {
            //read info for 3D object from file at current position
            stream = usstream.KfStringStream.create;
            while (readingMemoLine <= aMemo.Lines.Count - 1) {
                inputLine = aMemo.Lines.Strings[readingMemoLine];
                readingMemoLine += 1;
                if (trim(inputLine) == "") {
                    // cfk change v1.60final added '' case
                    continue;
                }
                if ((UNRESOLVED.copy(inputLine, 1, 1) == ";") && (UNRESOLVED.pos("ORIGIN", uppercase(inputLine)) <= 0)) {
                    // cfk change for v1.6b2 mistake with origin, placed with comment
                    // skip commented lines 
                    continue;
                }
                stream.onStringSeparator(inputLine, "=");
                fieldType = stream.nextToken();
                stream.spaceSeparator();
                if (UNRESOLVED.pos("POINT", uppercase(fieldType)) > 0) {
                    this.addPointString(stream);
                } else if (UNRESOLVED.pos("ORIGIN", uppercase(fieldType)) > 0) {
                    this.setOriginPointIndex(StrToIntDef(stream.remainder, 0));
                } else if (UNRESOLVED.pos("TRIANGLE", uppercase(fieldType)) > 0) {
                    this.addTriangleString(stream);
                } else if (UNRESOLVED.pos("NAME", uppercase(fieldType)) > 0) {
                    this.setName(stream.remainder);
                } else {
                    break;
                }
            }
            this.adjustForOrigin();
            if (UNRESOLVED.pos(uppercase(kEndTdoString), uppercase(inputLine)) <= 0) {
                throw new GeneralException.create("Problem: Expected end of 3D object.");
            }
        } finally {
            stream.free;
        }
        return readingMemoLine;
    }
    
    public void readFromInputString(String aString, boolean doAdjustForOrigin) {
        String part = "";
        String firstLetter = "";
        KfStringStream stream = new KfStringStream();
        KfStringStream partStream = new KfStringStream();
        
        // format is n[name],p[# # #],p[# # #],p[# # #],t[# # #],t[# # #],t[# # #] 
        this.pointsInUse = 0;
        this.originPointIndex = 0;
        this.triangles.clear();
        stream = usstream.KfStringStream.create;
        partStream = usstream.KfStringStream.create;
        try {
            stream.onStringSeparator(aString, ",");
            part = "none";
            while (part != "") {
                part = stream.nextToken();
                firstLetter = UNRESOLVED.copy(part, 1, 1);
                if (uppercase(firstLetter) == "N") {
                    this.setName(betweenBrackets(part));
                } else if (uppercase(firstLetter) == "P") {
                    partStream.onStringSeparator(betweenBrackets(part), " ");
                    this.addPointString(partStream);
                } else if (uppercase(firstLetter) == "T") {
                    partStream.onStringSeparator(betweenBrackets(part), " ");
                    this.addTriangleString(partStream);
                }
            }
            if (doAdjustForOrigin) {
                this.adjustForOrigin();
            }
        } finally {
            stream.free;
            partStream.free;
        }
    }
    
    // ------------------------------------------------------------------------- data transfer for binary copy 
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kKfObject3D;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        short i = 0;
        KfPoint3d tempPoint = new KfPoint3d();
        
        super.streamDataWithFiler(filer, cvir);
        this.name = filer.streamShortString(this.name);
        this.pointsInUse = filer.streamLongint(this.pointsInUse);
        this.originPointIndex = filer.streamLongint(this.originPointIndex);
        this.ensureEnoughSpaceForNewPointData(this.pointsInUse);
        if (this.pointsInUse > 0) {
            for (i = 0; i <= this.pointsInUse - 1; i++) {
                if (filer.isWriting()) {
                    tempPoint = this.points[i];
                }
                tempPoint = filer.streamBytes(tempPoint, FIX_sizeof(tempPoint));
                if (filer.isReading()) {
                    this.points[i] = tempPoint;
                }
            }
        }
        if (filer.isReading()) {
            //may have triangles already, because we are keeping them around now
            this.triangles.clear();
        }
        this.triangles.streamUsingFiler(filer, KfIndexTriangle);
    }
    
    public long totalMemorySize() {
        result = 0;
        long i = 0;
        
        result = this.instanceSize;
        result = result + this.triangles.instanceSize;
        if (this.triangles.Count > 0) {
            for (i = 0; i <= this.triangles.Count - 1; i++) {
                result = result + KfIndexTriangle(this.triangles.Items[i]).instanceSize;
            }
        }
        result = result + this.pointsAllocated * FIX_sizeof(KfPoint3D);
        return result;
    }
    
    public void writeToDXFFile(String fileName, TColorRef frontFaceColor, TColorRef backFaceColor) {
        TextFile outputFile = new TextFile();
        short i = 0;
        KfIndexTriangle triangle = new KfIndexTriangle();
        TColorRef colorToDraw = new TColorRef();
        
        AssignFile(outputFile, fileName);
        try {
            // v1.5
            usupport.setDecimalSeparator();
            Rewrite(outputFile);
            writeln(outputFile, "0");
            writeln(outputFile, "SECTION");
            writeln(outputFile, "2");
            writeln(outputFile, "ENTITIES");
            for (i = 0; i <= this.triangles.Count - 1; i++) {
                triangle = KfIndexTriangle(this.triangles.Items[i]);
                if (this.triangleIsBackFacing(triangle)) {
                    colorToDraw = backFaceColor;
                } else {
                    colorToDraw = frontFaceColor;
                }
                this.writeTriangleToDXFFIle(outputFile, this.points[triangle.pointIndexes[0] - 1], this.points[triangle.pointIndexes[1] - 1], this.points[triangle.pointIndexes[2] - 1], colorToDraw);
            }
            writeln(outputFile, "0");
            writeln(outputFile, "ENDSEC");
            writeln(outputFile, "0");
            writeln(outputFile, "EOF");
        } finally {
            CloseFile(outputFile);
        }
    }
    
    public void writeTriangleToDXFFIle(TextFile outputFile, KfPoint3D p1, KfPoint3D p2, KfPoint3D p3, TColorRef color) {
        writeln(outputFile, "0");
        writeln(outputFile, "3DFACE");
        writeln(outputFile, "8");
        writeln(outputFile, "3dObject");
        writeln(outputFile, "62");
        writeln(outputFile, IntToStr(color));
        // v1.60final changed intToStr(round(p|.|)) to digitValueString(p|.|)
        // can't see that there was ever any reason to round these; it's probably left over from
        // when I didn't understand DXF very well
        writeln(outputFile, "10");
        writeln(outputFile, usupport.digitValueString(p1.x));
        writeln(outputFile, "20");
        writeln(outputFile, usupport.digitValueString(-p1.y));
        writeln(outputFile, "30");
        writeln(outputFile, usupport.digitValueString(p1.z));
        writeln(outputFile, "11");
        writeln(outputFile, usupport.digitValueString(p2.x));
        writeln(outputFile, "21");
        writeln(outputFile, usupport.digitValueString(-p2.y));
        writeln(outputFile, "31");
        writeln(outputFile, usupport.digitValueString(p2.z));
        writeln(outputFile, "12");
        writeln(outputFile, usupport.digitValueString(p3.x));
        writeln(outputFile, "22");
        writeln(outputFile, usupport.digitValueString(-p3.y));
        writeln(outputFile, "32");
        writeln(outputFile, usupport.digitValueString(p3.z));
        writeln(outputFile, "13");
        writeln(outputFile, usupport.digitValueString(p3.x));
        writeln(outputFile, "23");
        writeln(outputFile, usupport.digitValueString(-p3.y));
        writeln(outputFile, "33");
        writeln(outputFile, usupport.digitValueString(p3.z));
    }
    
    public void writeToPOV_INCFile(String fileName, TColorRef frontFaceColor, boolean embeddedInPlant, int rotateCount) {
        TextFile outputFile = new TextFile();
        short i = 0;
        KfIndexTriangle triangle = new KfIndexTriangle();
        TColorRef colorToDraw = new TColorRef();
        String nameString = "";
        
        AssignFile(outputFile, fileName);
        try {
            // v1.5
            usupport.setDecimalSeparator();
            Rewrite(outputFile);
            nameString = usupport.replacePunctuationWithUnderscores(this.getName());
            writeln(outputFile, "// POV-format INC file of PlantStudio v1.x 3D object");
            writeln(outputFile, "//     \"" + this.getName() + "\"");
            if ((!embeddedInPlant)) {
                writeln(outputFile, "// include this file in a POV file thus to use it:");
                writeln(outputFile, "//     #include \"" + usupport.stringUpTo(ExtractFileName(fileName), ".") + ".inc\"");
                writeln(outputFile, "//     object { " + nameString + " }");
                if (rotateCount > 1) {
                    writeln(outputFile, "//  or");
                    writeln(outputFile, "//     object { " + nameString + "_rotated }");
                }
                writeln(outputFile);
            }
            writeln(outputFile, "#declare " + nameString + "=mesh {");
            for (i = 0; i <= this.triangles.Count - 1; i++) {
                triangle = KfIndexTriangle(this.triangles.Items[i]);
                this.writeTriangleToPOV_INCFIle(outputFile, this.points[triangle.pointIndexes[0] - 1], this.points[triangle.pointIndexes[1] - 1], this.points[triangle.pointIndexes[2] - 1]);
            }
            writeln(outputFile, chr(9) + "pigment { color rgb <" + usupport.digitValueString(UNRESOLVED.getRValue(frontFaceColor) / 256.0) + ", " + usupport.digitValueString(UNRESOLVED.getGValue(frontFaceColor) / 256.0) + ", " + usupport.digitValueString(UNRESOLVED.getBValue(frontFaceColor) / 256.0) + "> }");
            writeln(outputFile, "}");
            if (rotateCount > 1) {
                writeln(outputFile);
                writeln(outputFile, "#declare " + nameString + "_rotated=union {");
                writeln(outputFile, chr(9) + "object { " + nameString + " }");
                for (i = 1; i <= rotateCount - 1; i++) {
                    writeln(outputFile, chr(9) + "object { " + nameString + " rotate " + IntToStr(i) + "*365/" + IntToStr(rotateCount) + "*y }");
                }
                writeln(outputFile, "}");
            }
        } finally {
            CloseFile(outputFile);
        }
    }
    
    public void writeTriangleToPOV_INCFIle(TextFile outputFile, KfPoint3D p1, KfPoint3D p2, KfPoint3D p3) {
        write(outputFile, chr(9) + "triangle { <");
        // all y values must be negative because it seems our coordinate systems are different
        write(outputFile, IntToStr(intround(p1.x)) + ", " + IntToStr(-intround(p1.y)) + ", " + IntToStr(intround(p1.z)) + ">, <");
        write(outputFile, IntToStr(intround(p2.x)) + ", " + IntToStr(-intround(p2.y)) + ", " + IntToStr(intround(p2.z)) + ">, <");
        writeln(outputFile, IntToStr(intround(p3.x)) + ", " + IntToStr(-intround(p3.y)) + ", " + IntToStr(intround(p3.z)) + "> }");
    }
    
    public boolean triangleIsBackFacing(KfIndexTriangle aTriangle) {
        result = false;
        KfPoint3d point0 = new KfPoint3d();
        KfPoint3d point1 = new KfPoint3d();
        KfPoint3d point2 = new KfPoint3d();
        float backfacingResult = 0.0;
        
        result = false;
        point0 = this.points[aTriangle.pointIndexes[0] - 1];
        point1 = this.points[aTriangle.pointIndexes[1] - 1];
        point2 = this.points[aTriangle.pointIndexes[2] - 1];
        backfacingResult = ((point1.x - point0.x) * (point2.y - point0.y)) - ((point1.y - point0.y) * (point2.x - point0.x));
        result = (backfacingResult < 0);
        return result;
    }
    
}
// not using
//procedure KfObject3D.insertPoint(newPointIndex: smallint; newPoint: KfPoint3d);
//  var
//    i: smallint;
//  begin
//  inc(pointsInUse);
//  if newPointIndex <= pointsInUse - 1 then for i := newPointIndex to pointsInUse - 1 do
//    begin
//    self.changePointIndexInTriangles(i+1, i);
//    points[i+1] := points[i];
//    end;
//  points[newPointIndex] := newPoint;
//  end;
//
//
//    writeln(outputFile, '#declare camera_' + nameString + '= camera {');
//    writeln(outputFile, chr(9) + 'location  <0, 0, ' + intToStr(round(lowestZ)) + '>');
//    writeln(outputFile, chr(9) + 'look_at <'
//      + intToStr(round(totalX / (triangles.count * 3)))
//      + ', ' + intToStr(round(totalY / (triangles.count * 3)))
//      + ', ' + intToStr(round(totalZ / (triangles.count * 3))) + '>');
//    writeln(outputFile, chr(9) + 'angle 90');
//    writeln(outputFile, '}');
//    
