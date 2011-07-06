// unit Uturtle

from conversion_common import *;
import umain;
import utravers;
import umath;
import usupport;
import u3dexport;
import u3dsupport;
import udrawingsurface;
import utdo;
import ucollect;
import delphi_compatability;

// const
kInitialTurtleMatrixStackDepth = 250;


//OpenGL,
//if this is defined - turtle will draw axis marks for each line segment
//put spaces before and after the $ to disable
// $ DEFINE DEBUG_TURTLE
// general options 
// record
class PlantDrawOptionsStructure {
    public boolean sortPolygons;
    public boolean drawLines;
    public short lineContrastIndex;
    public boolean wireFrame;
    public boolean straightLinesOnly;
    public boolean simpleLeavesOnly;
    public boolean drawStems;
    public boolean draw3DObjects;
    public boolean draw3DObjectsAsRects;
    public boolean circlePoints;
    public short circlePointRadius;
    public boolean sortTdosAsOneItem;
    public boolean drawingToMainWindow;
    public boolean drawBoundsRectsOnPlantParts;
}

// var
KfTurtle gDefaultTurtle = new KfTurtle();
boolean gDefaultTurtleInUse = false;


//if the DEBUG_TURTLE flag is defined then draw axis information
// PDF PORT Issue
public void debugDrawInMillimeters(KfTurtle turtle, float mm) {
    KfPoint3d oldPosition = new KfPoint3d();
    KfPoint3d newPosition = new KfPoint3d();
    
    oldPosition = turtle.currentMatrix.position;
    turtle.currentMatrix.move(turtle.millimetersToPixels(mm));
    newPosition = turtle.currentMatrix.position;
    turtle.addToRealBoundsRect(newPosition);
}

public void debugDrawAxis(KfTurtle turtle, float pixels) {
    KfPoint3d oldPosition = new KfPoint3d();
    KfPoint3d newPosition = new KfPoint3d();
    
    oldPosition = turtle.currentMatrix.position;
    turtle.currentMatrix.move(pixels);
    newPosition = turtle.currentMatrix.position;
    if (turtle.drawOptions.drawStems) {
        turtle.drawingSurface.drawLineFromTo(oldPosition, newPosition);
    }
}


// speed optimizations 
//PDF FIX - may want to think about size of recorded points
class KfTurtle extends TObject {
    public TListCollection matrixStack;
    public long numMatrixesUsed;
    public KfMatrix currentMatrix;
    public  recordedPoints;
    public long recordedPointsInUse;
    public float scale_pixelsPerMm;
    public KfDrawingSurface drawingSurface;
    public KfPoint3d tempPosition;
    public TRealRect realBoundsRect;
    public PlantDrawOptionsStructure drawOptions;
    public short writingTo;
    
    //for darkerColor
    //temp
    // ---------------------------------------------------------------------------------- *KfTurtle creating/destroying 
    public void create() {
        long i = 0;
        
        super.create();
        // v1.60final looked at giving hint with plant part name again; still has problem
        // that what you record is only points, and what you need to record is rects
        // it can be done, but the plant parts have to change to record rects, and they
        // have to deal with all their different ways of drawing. not worth doing at this time.
        this.matrixStack = ucollect.TListCollection().Create();
        this.currentMatrix = u3dsupport.KfMatrix.create;
        this.currentMatrix.initializeAsUnitMatrix();
        this.matrixStack.Add(this.currentMatrix);
        this.numMatrixesUsed = 1;
        for (i = 0; i <= kInitialTurtleMatrixStackDepth; i++) {
            //start with a bunch of matrixes
            this.matrixStack.Add(u3dsupport.KfMatrix.create);
        }
        this.recordedPointsInUse = 0;
        this.drawingSurface = udrawingsurface.KfDrawingSurface().create();
        this.scale_pixelsPerMm = 1.0;
    }
    
    public void destroy() {
        this.matrixStack.free;
        this.matrixStack = null;
        this.drawingSurface.free;
        this.drawingSurface = null;
        super.destroy();
    }
    
    // 3d file export
    public void createFor3DOutput(short anOutputType, String aFileName) {
        this.create();
        //already created
        this.drawingSurface.free;
        this.drawingSurface = null;
        switch (anOutputType) {
            case u3dexport.kDXF:
                this.drawingSurface = u3dexport.KfDrawingSurfaceForDXF().createWithFileName(aFileName);
                break;
            case u3dexport.kPOV:
                this.drawingSurface = u3dexport.KfDrawingSurfaceForPOV().createWithFileName(aFileName);
                break;
            case u3dexport.k3DS:
                this.drawingSurface = u3dexport.KfDrawingSurfaceFor3DS().createWithFileName(aFileName);
                break;
            case u3dexport.kOBJ:
                this.drawingSurface = u3dexport.KfDrawingSurfaceForOBJ().createWithFileName(aFileName);
                break;
            case u3dexport.kVRML:
                this.drawingSurface = u3dexport.KfDrawingSurfaceForVRML().createWithFileName(aFileName);
                break;
            case u3dexport.kLWO:
                this.drawingSurface = u3dexport.KfDrawingSurfaceForLWO().createWithFileName(aFileName);
                break;
            default:
                throw new GeneralException.create("KfTurtle.createFor3DOutput: Unrecognized output type");
                break;
    }
    
    public void start3DExportFile() {
        if ((this.drawingSurface != null) && (this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).startFile;
        }
    }
    
    public void end3DExportFile() {
        if ((this.drawingSurface != null) && (this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).endFile;
        }
    }
    
    // -------------------------------------------------------------------------- KfTurtle initializing and setting values 
    public void reset() {
        this.numMatrixesUsed = 1;
        this.currentMatrix = this.matrixStack.Items[0];
        this.currentMatrix.initializeAsUnitMatrix();
        this.recordedPointsInUse = 0;
        this.scale_pixelsPerMm = 1.0;
        if (this.drawingSurface != null) {
            this.drawingSurface.fillingTriangles = !this.drawOptions.wireFrame;
            this.drawingSurface.drawingLines = this.drawOptions.drawLines;
            this.drawingSurface.circlingPoints = this.drawOptions.circlePoints;
            this.drawingSurface.lineContrastIndex = this.drawOptions.lineContrastIndex;
            this.drawingSurface.circlePointRadius = this.drawOptions.circlePointRadius;
            this.drawingSurface.sortTdosAsOneItem = this.drawOptions.sortTdosAsOneItem;
            this.drawingSurface.initialize();
        }
    }
    
    public void setDrawOptionsForDrawingTdoOnly() {
        this.drawOptions.draw3DObjects = true;
        this.drawOptions.draw3DObjectsAsRects = false;
        this.drawOptions.drawLines = true;
        this.drawOptions.lineContrastIndex = utdo.kTdoLineContrastIndex;
        this.drawOptions.wireFrame = false;
        this.drawOptions.sortPolygons = true;
        this.drawOptions.sortTdosAsOneItem = false;
        this.drawOptions.circlePoints = false;
        // when drawing a tdo all by itself, you MUST set the turtle scale to 1.0,
        //    because the tdo multiplies the turtle scale by its own scale (which you are giving it
        //    in the call to draw) 
        // self.setScale_pixelsPerMm(1.0);  actually, this gets done in the reset method
        this.drawingSurface.foreColor = utdo.kTdoForeColor;
        this.drawingSurface.backColor = utdo.kTdoBackColor;
        this.drawingSurface.lineColor = delphi_compatability.clBlack;
    }
    
    public void resetBoundsRect(TPoint basePoint) {
        this.realBoundsRect.left = basePoint.X;
        this.realBoundsRect.right = basePoint.X;
        this.realBoundsRect.top = basePoint.Y;
        this.realBoundsRect.bottom = basePoint.Y;
    }
    
    public void xyz(float x, float y, float z) {
        this.currentMatrix.position.x = x;
        this.currentMatrix.position.y = y;
        this.currentMatrix.position.z = z;
    }
    
    public void setForeColorBackColor(TColor frontColor, TColor backColor) {
        this.drawingSurface.foreColor = frontColor;
        this.drawingSurface.backColor = backColor;
    }
    
    public void setLineColor(TColor aColor) {
        this.drawingSurface.lineColor = aColor;
    }
    
    public void setLineWidth(float aWidth) {
        this.drawingSurface.lineWidth = aWidth * this.scale_pixelsPerMm;
        if (this.drawingSurface.lineWidth > 16000) {
            this.drawingSurface.lineWidth = 16000;
        }
    }
    
    public void setScale_pixelsPerMm(float newScale_pixelsPerMm) {
        this.scale_pixelsPerMm = newScale_pixelsPerMm;
    }
    
    public KfTriangle newTriangleTriangle(long aPointIndex, long bPointIndex, long cPointIndex) {
        result = new KfTriangle();
        result = u3dsupport.KfTriangle.create;
        result.points[0] = this.recordedPoints[aPointIndex];
        result.points[1] = this.recordedPoints[bPointIndex];
        result.points[2] = this.recordedPoints[cPointIndex];
        return result;
    }
    
    public KfPoint3D positionCopy() {
        result = new KfPoint3D();
        //suspicious things that call this may not clean up copy
        result = this.currentMatrix.position;
        return result;
    }
    
    public boolean exportingToFile() {
        result = false;
        // cfk update this if create any mode that is NOT screen and NOT file
        result = this.writingTo != u3dexport.kScreen;
        return result;
    }
    
    public boolean writingToDXF() {
        result = false;
        result = this.writingTo == u3dexport.kDXF;
        return result;
    }
    
    public boolean writingToPOV() {
        result = false;
        result = this.writingTo == u3dexport.kPOV;
        return result;
    }
    
    public boolean writingTo3DS() {
        result = false;
        result = this.writingTo == u3dexport.k3DS;
        return result;
    }
    
    public boolean writingToOBJ() {
        result = false;
        result = this.writingTo == u3dexport.kOBJ;
        return result;
    }
    
    public boolean writingToVRML() {
        result = false;
        result = this.writingTo == u3dexport.kVRML;
        return result;
    }
    
    public boolean writingToLWO() {
        result = false;
        result = this.writingTo == u3dexport.kLWO;
        return result;
    }
    
    public KfFileExportSurface fileExportSurface() {
        result = new KfFileExportSurface();
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            result = (u3dexport.KfFileExportSurface)this.drawingSurface;
        } else {
            result = null;
        }
        return result;
    }
    
    public void ifExporting_startNestedGroupOfPlantParts(String groupName, String shortName, short nestingType) {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).startNestedGroupOfPlantParts(groupName, shortName, nestingType);
        }
    }
    
    public void ifExporting_endNestedGroupOfPlantParts(short nestingType) {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).endNestedGroupOfPlantParts(nestingType);
        }
    }
    
    public void ifExporting_startPlantPart(String aLongName, String aShortName) {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).startPlantPart(aLongName, aShortName);
        }
    }
    
    public void ifExporting_endPlantPart() {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).endPlantPart;
        }
    }
    
    public boolean ifExporting_excludeStem(float length) {
        result = false;
        result = false;
        if ((this.drawingSurface instanceof u3dexport.KfDrawingSurfaceForPOV)) {
            result = (len <= ((u3dexport.KfDrawingSurfaceForPOV)this.drawingSurface).options.pov_minLineLengthToWrite);
        }
        return result;
    }
    
    public boolean ifExporting_exclude3DObject(float scale) {
        result = false;
        result = false;
        if ((this.drawingSurface instanceof u3dexport.KfDrawingSurfaceForPOV)) {
            result = (scale <= ((u3dexport.KfDrawingSurfaceForPOV)this.drawingSurface).options.pov_minTdoScaleToWrite);
        }
        return result;
    }
    
    public void ifExporting_startStemSegment(String aLongName, String aShortName, TColorRef color, float width, short index) {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).startStemSegment(aLongName, aShortName, color, width, index);
        }
    }
    
    public void ifExporting_endStemSegment() {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).endStemSegment;
        }
    }
    
    public short ifExporting_stemCylinderFaces() {
        result = 0;
        result = 0;
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            result = ((u3dexport.KfFileExportSurface)this.drawingSurface).options.stemCylinderFaces;
        }
        return result;
    }
    
    public void drawFileExportPipeFaces( startPoints,  endPoints, short faces, short segmentNumber) {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).drawPipeFaces(startPoints, endPoints, faces, segmentNumber);
        }
    }
    
    public void ifExporting_start3DObject(String aLongName, String aShortName, TColorRef color, short index) {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).start3DObject(aLongName, aShortName, color, index);
        }
    }
    
    public void ifExporting_end3DObject() {
        if ((this.drawingSurface instanceof u3dexport.KfFileExportSurface)) {
            ((u3dexport.KfFileExportSurface)this.drawingSurface).end3DObject;
        }
    }
    
    // ---------------------------------------------------------------------------------- KfTurtle returning values 
    public float millimetersToPixels(float mm) {
        result = 0.0;
        result = mm * this.scale_pixelsPerMm;
        return result;
    }
    
    public byte angleX() {
        result = 0;
        result = this.currentMatrix.angleX();
        return result;
    }
    
    public byte angleY() {
        result = 0;
        result = this.currentMatrix.angleY();
        return result;
    }
    
    public byte angleZ() {
        result = 0;
        result = this.currentMatrix.angleZ();
        return result;
    }
    
    public TColor lineColor() {
        result = new TColor();
        result = this.drawingSurface.lineColor;
        return result;
    }
    
    public float lineWidth() {
        result = 0.0;
        result = this.drawingSurface.lineWidth;
        return result;
    }
    
    public KfPoint3d position() {
        result = new KfPoint3d();
        this.tempPosition = this.currentMatrix.position;
        result = this.tempPosition;
        return result;
    }
    
    public TRect boundsRect() {
        result = new TRect();
        try {
            result.Top = intround(this.realBoundsRect.top);
            result.Left = intround(this.realBoundsRect.left);
            result.Bottom = intround(this.realBoundsRect.bottom);
            result.Right = intround(this.realBoundsRect.right);
        } catch (Exception e) {
            //might want to be more precise in assigning a rect
            result.Top = -32767;
            result.Left = -32767;
            result.Bottom = 32767;
            result.Right = 32767;
        }
        return result;
    }
    
    // ---------------------------------------------------------------------------------- KfTurtle recording 
    public void startRecording() {
        this.recordedPointsInUse = 0;
        this.recordPosition();
    }
    
    public void clearRecording() {
        this.recordedPointsInUse = 0;
    }
    
    public void recordPosition() {
        KfPoint3D newPoint = new KfPoint3D();
        
        if (this.recordedPointsInUse >= utdo.kMaximumRecordedPoints) {
            return;
        }
        newPoint = this.currentMatrix.position;
        this.recordedPoints[this.recordedPointsInUse] = newPoint;
        this.recordedPointsInUse += 1;
        this.addToRealBoundsRect(newPoint);
    }
    
    public void recordPositionPoint(KfPoint3D aPoint) {
        if (this.recordedPointsInUse >= utdo.kMaximumRecordedPoints) {
            return;
        }
        this.recordedPoints[this.recordedPointsInUse] = aPoint;
        this.recordedPointsInUse += 1;
        this.addToRealBoundsRect(aPoint);
    }
    
    public KfPoint3d transformAndRecord(KfPoint3D originalPoint3D, float theScale_pixelsPerMm) {
        result = new KfPoint3d();
        //transform and scale point and record the new location without moving
        result = originalPoint3D;
        utdo.KfPoint3D_scaleBy(result, theScale_pixelsPerMm * this.scale_pixelsPerMm);
        this.currentMatrix.transform(result);
        this.recordPositionPoint(result);
        return result;
    }
    
    public void moveAndRecordScale(KfPoint3D originalPoint3D, float theScale_pixelsPerMm) {
        KfPoint3D aPoint3d = new KfPoint3D();
        
        aPoint3d = originalPoint3D;
        utdo.KfPoint3D_scaleBy(aPoint3d, theScale_pixelsPerMm * this.scale_pixelsPerMm);
        this.currentMatrix.transform(aPoint3d);
        this.currentMatrix.position = aPoint3d;
        this.recordPositionPoint(aPoint3d);
    }
    
    // ---------------------------------------------------------------------------------- KfTurtle moving 
    public void moveInMillimeters(float mm) {
        this.currentMatrix.move(this.millimetersToPixels(mm));
    }
    
    public void moveInMillimetersAndRecord(float mm) {
        this.currentMatrix.move(this.millimetersToPixels(mm));
        this.recordPosition();
    }
    
    public void moveInPixels(float pixels) {
        this.currentMatrix.move(pixels);
    }
    
    public void moveInPixelsAndRecord(float pixels) {
        this.currentMatrix.move(pixels);
        this.recordPosition();
    }
    
    // ---------------------------------------------------------------------------------- KfTurtle drawing 
    public void drawInPixels(float pixels) {
        KfPoint3d oldPosition = new KfPoint3d();
        KfPoint3d newPosition = new KfPoint3d();
        
        oldPosition = this.currentMatrix.position;
        this.currentMatrix.move(pixels);
        newPosition = this.currentMatrix.position;
        if (this.drawOptions.drawStems) {
            this.drawingSurface.drawLineFromTo(oldPosition, newPosition);
        }
        this.addToRealBoundsRect(newPosition);
    }
    
    // PDF PORT added to deal with alternatives
    // PDF PORT --Alternative -- changed name of alternative function -- Will not be called
    public void drawInMillimeters_debug(float mm) {
        TColorRef oldColor = new TColorRef();
        float oldWidth = 0.0;
        
        oldColor = this.drawingSurface.lineColor;
        oldWidth = this.drawingSurface.lineWidth;
        this.drawingSurface.lineWidth = 2;
        this.drawingSurface.lineColor = delphi_compatability.clRed;
        this.push();
        //will flip so draw Y (sic)
        this.rotateZ(64);
        debugDrawAxis(this, 100.0);
        this.pop();
        this.drawingSurface.lineWidth = 1;
        this.drawingSurface.lineColor = delphi_compatability.clBlue;
        this.push();
        //will flip so draw Z (sic)
        this.rotateY(64);
        debugDrawAxis(this, 100.0);
        this.pop();
        this.drawingSurface.lineColor = oldColor;
        this.drawingSurface.lineWidth = oldWidth;
        debugDrawInMillimeters(this, mm);
    }
    
    public KfTriangle drawInMillimeters(float mm, long partID) {
        result = new KfTriangle();
        KfPoint3d oldPosition = new KfPoint3d();
        KfPoint3d newPosition = new KfPoint3d();
        
        result = null;
        oldPosition = this.currentMatrix.position;
        this.currentMatrix.move(this.millimetersToPixels(mm));
        newPosition = this.currentMatrix.position;
        if (this.drawOptions.drawStems) {
            result = this.drawingSurface.drawLineFromTo(oldPosition, newPosition);
            if (result != null) {
                result.plantPartID = partID;
            }
        }
        this.addToRealBoundsRect(newPosition);
        return result;
    }
    
    public KfTriangle drawTriangleFromIndexes(long aPointIndex, long bPointIndex, long cPointIndex, long partID) {
        result = new KfTriangle();
        //drawing surface takes over ownership of triangle
        result = this.drawingSurface.allocateTriangle();
        this.drawingSurface.lineWidth = 1.0;
        result.points[0] = this.recordedPoints[aPointIndex - 1];
        result.points[1] = this.recordedPoints[bPointIndex - 1];
        result.points[2] = this.recordedPoints[cPointIndex - 1];
        result.plantPartID = partID;
        this.drawingSurface.drawLastTriangle();
        return result;
    }
    
    public void drawTrianglesFromBoundsRect(TRect boundsRect) {
        KfTriangle aTriangle = new KfTriangle();
        
        //drawing surface takes over ownership of triangle
        this.drawingSurface.lineWidth = 1.0;
        aTriangle = this.drawingSurface.allocateTriangle();
        aTriangle.points[0].x = boundsRect.Left;
        aTriangle.points[0].y = boundsRect.Top;
        aTriangle.points[1].x = boundsRect.Right;
        aTriangle.points[1].y = boundsRect.Top;
        aTriangle.points[2].x = boundsRect.Left;
        aTriangle.points[2].y = boundsRect.Bottom;
        this.drawingSurface.drawLastTriangle();
        aTriangle = this.drawingSurface.allocateTriangle();
        aTriangle.points[0].x = boundsRect.Left;
        aTriangle.points[0].y = boundsRect.Bottom;
        aTriangle.points[1].x = boundsRect.Right;
        aTriangle.points[1].y = boundsRect.Top;
        aTriangle.points[2].x = boundsRect.Right;
        aTriangle.points[2].y = boundsRect.Bottom;
        this.drawingSurface.drawLastTriangle();
    }
    
    public void drawTriangle() {
        KfTriangle triangle = new KfTriangle();
        
        if (this.recordedPointsInUse != 3) {
            throw new GeneralException.create("Problem: Triangle made without three points in method KfTurtle.drawTriangle.");
        }
        //drawing surface owns triangle
        triangle = this.drawingSurface.allocateTriangle();
        triangle.points[0] = this.recordedPoints[0];
        triangle.points[1] = this.recordedPoints[1];
        triangle.points[2] = this.recordedPoints[2];
        this.drawingSurface.drawLastTriangle();
        this.recordedPointsInUse = 0;
    }
    
    public void addToRealBoundsRect(KfPoint3d aPoint) {
        if (aPoint.x < this.realBoundsRect.left) {
            this.realBoundsRect.left = aPoint.x;
        } else if (aPoint.x > this.realBoundsRect.right) {
            this.realBoundsRect.right = aPoint.x;
        }
        if (aPoint.y < this.realBoundsRect.top) {
            this.realBoundsRect.top = aPoint.y;
        } else if (aPoint.y > this.realBoundsRect.bottom) {
            this.realBoundsRect.bottom = aPoint.y;
        }
    }
    
    // ---------------------------------------------------------------------------------- KfTurtle stack 
    public void push() {
        if (this.numMatrixesUsed >= this.matrixStack.Count) {
            this.matrixStack.Add(this.currentMatrix.deepCopy());
        } else {
            this.currentMatrix.copyTo(u3dsupport.KfMatrix(this.matrixStack.Items[this.numMatrixesUsed]));
        }
        this.numMatrixesUsed += 1;
        this.currentMatrix = this.matrixStack.Items[this.numMatrixesUsed - 1];
    }
    
    public void pop() {
        if (this.numMatrixesUsed < 1) {
            return;
        }
        this.numMatrixesUsed -= 1;
        this.currentMatrix = this.matrixStack.Items[this.numMatrixesUsed - 1];
    }
    
    public long stackSize() {
        result = 0;
        result = this.numMatrixesUsed;
        return result;
    }
    
    // ---------------------------------------------------------------------------------- KfTurtle rotating 
    public void rotateX(float angle) {
        this.currentMatrix.rotateX(angle);
    }
    
    public void rotateY(float angle) {
        this.currentMatrix.rotateY(angle);
    }
    
    public void rotateZ(float angle) {
        this.currentMatrix.rotateZ(angle);
    }
    
    // ---------------------------------------------------------------------------------- KfTurtle defaulting 
    //where the default turtle is used need a try..finally
    //to ensure defaultStopUsing is called no matter what
    public KfTurtle defaultStartUsing() {
        result = new KfTurtle();
        if (gDefaultTurtleInUse) {
            throw new GeneralException.create("Problem: turtle is already in use; in method KfTurtle.defaultStartUsing.");
        }
        gDefaultTurtleInUse = true;
        result = gDefaultTurtle;
        return result;
    }
    
    public void defaultStopUsing() {
        gDefaultTurtleInUse = false;
    }
    
    public void defaultAllocate() {
        gDefaultTurtle = null;
        gDefaultTurtle = KfTurtle().create();
        gDefaultTurtleInUse = false;
    }
    
    public void defaultFree() {
        gDefaultTurtle.free;
        gDefaultTurtle = null;
    }
    
}
//need to default free somewhere in project
