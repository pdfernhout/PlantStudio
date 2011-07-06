// unit U3dexport

from conversion_common import *;
import umath;
import udomain;
import u3dsupport;
import udrawingsurface;
import utdo;
import usupport;
import delphi_compatability;

// const
kExportPartMeristem = 0;
kExportPartInternode = 1;
kExportPartSeedlingLeaf = 2;
kExportPartLeaf = 3;
kExportPartFirstPetiole = 4;
kExportPartPetiole = 5;
kExportPartLeafStipule = 6;
kExportPartInflorescenceStalkFemale = 7;
kExportPartInflorescenceInternodeFemale = 8;
kExportPartInflorescenceBractFemale = 9;
kExportPartInflorescenceStalkMale = 10;
kExportPartInflorescenceInternodeMale = 11;
kExportPartInflorescenceBractMale = 12;
kExportPartPedicelFemale = 13;
kExportPartFlowerBudFemale = 14;
kExportPartStyleFemale = 15;
kExportPartStigmaFemale = 16;
kExportPartFilamentFemale = 17;
kExportPartAntherFemale = 18;
kExportPartFirstPetalsFemale = 19;
kExportPartSecondPetalsFemale = 20;
kExportPartThirdPetalsFemale = 21;
kExportPartFourthPetalsFemale = 22;
kExportPartFifthPetalsFemale = 23;
kExportPartSepalsFemale = 24;
kExportPartPedicelMale = 25;
kExportPartFlowerBudMale = 26;
kExportPartFilamentMale = 27;
kExportPartAntherMale = 28;
kExportPartFirstPetalsMale = 29;
kExportPartSepalsMale = 30;
kExportPartUnripeFruit = 31;
kExportPartRipeFruit = 32;
kExportPartRootTop = 33;
kExportPartLast = 33;
kLastDxfColorIndex = 10;
dxfColors = [delphi_compatability.clRed, delphi_compatability.clYellow, delphi_compatability.clLime, delphi_compatability.clAqua, delphi_compatability.clBlue, delphi_compatability.clPurple, delphi_compatability.clBlack, delphi_compatability.clOlive, delphi_compatability.clFuchsia, delphi_compatability.clTeal, delphi_compatability.clGray, ];
kColorDXFFromPlantPartType = 0;
kColorDXFFromRGB = 1;
kColorDXFFromOneColor = 3;
kNestingTypeInflorescence = 0;
kNestingTypeLeafAndPetiole = 1;
kNestingTypeCompoundLeaf = 2;
kNestingTypePedicelAndFlowerFruit = 3;
kNestingTypeFloralLayers = 4;
kMaxPOVPlants = 1000;
kMaxStoredMaterials = 1000;
kVRMLVersionOne = 0;
kVRMLVersionTwo = 1;
kScreen = 0;
kDXF = 1;
kPOV = 2;
k3DS = 3;
kOBJ = 4;
kVRML = 5;
kLWO = 6;
k3DExportTypeLast = 6;
kLayerOutputAllTogether = 0;
kLayerOutputByTypeOfPlantPart = 1;
kLayerOutputByPlantPart = 2;
kWriteColor = true;
kDontWriteColor = false;
kMax3DPoints = 65536;
kMax3DFaces = 65536;
kX = 0;
kY = 1;
kZ = 2;


// export part types
// meristem
// internode
// leaf
// no stipule on first leaves
// inflorescence female
// inflorescence male
// flower female
// flower male
// fruit
// root top
// DXF
// POV
// can't imagine anyone would save more than that
// 3DS
// OBJ, LWO
// VRML
// general
// record
class Vertex {
    public float x;
    public float y;
    public float z;
}

// record
class Triangle {
    public int vertex1;
    public int vertex2;
    public int vertex3;
    public int surfaceID;
}

// generic
// record
class FileExport3DOptionsStructure {
    public short exportType;
    public short layeringOption;
    public short stemCylinderFaces;
    public boolean translatePlantsToWindowPositions;
    public short lengthOfShortName;
    public boolean writePlantNumberInFrontOfName;
    public boolean writeColors;
    public short overallScalingFactor_pct;
    public float fileSize;
    public short xRotationBeforeDraw;
    public boolean pressPlants;
    public short directionToPressPlants;
    public boolean makeTrianglesDoubleSided;
    public short dxf_whereToGetColors;
    public short dxf_wholePlantColorIndex;
    public  dxf_plantPartColorIndexes;
    public float pov_minLineLengthToWrite;
    public float pov_minTdoScaleToWrite;
    public boolean pov_commentOutUnionAtEnd;
    public boolean nest_Inflorescence;
    public boolean nest_LeafAndPetiole;
    public boolean nest_CompoundLeaf;
    public boolean nest_PedicelAndFlowerFruit;
    public boolean nest_FloralLayers;
    public short vrml_version;
}

// const
kNumVRMLPointsPerLine = 4;


// record
class SingleOverlay {
}

// ------------------------------------------------------------------------------------------ index functions 
public short fileTypeFor3DExportType(short outputType) {
    result = 0;
    switch (outputType) {
        case kDXF:
            result = usupport.kFileTypeDXF;
            break;
        case kPOV:
            result = usupport.kFileTypeINC;
            break;
        case k3DS:
            result = usupport.kFileType3DS;
            break;
        case kOBJ:
            result = usupport.kFileTypeOBJ;
            break;
        case kVRML:
            result = usupport.kFileTypeVRML;
            break;
        case kLWO:
            result = usupport.kFileTypeLWO;
            break;
        default:
            throw new GeneralException.create("Problem: Invalid export type in TMainForm.fileTypeFor3DExportType.");
            break;
    return result;
}

public String nameFor3DExportType(short anOutputType) {
    result = "";
    switch (anOutputType) {
        case kDXF:
            result = "DXF";
            break;
        case kPOV:
            result = "POV";
            break;
        case k3DS:
            result = "3DS";
            break;
        case kOBJ:
            result = "OBJ";
            break;
        case kVRML:
            result = "VRML";
            break;
        case kLWO:
            result = "LWO";
            break;
        default:
            throw new GeneralException.create("Problem: Invalid type in PdDomain.sectionNumberFor3DExportType.");
            break;
    return result;
}

public String longNameForDXFPartType(short index) {
    result = "";
    String longName = "";
    String shortName = "";
    
    longName, shortName = getInfoForDXFPartType(index, longName, shortName);
    result = longName;
    return result;
}

public String shortNameForDXFPartType(short index) {
    result = "";
    String longName = "";
    String shortName = "";
    
    longName, shortName = getInfoForDXFPartType(index, longName, shortName);
    result = shortName;
    return result;
}

public void getInfoForDXFPartType(short index, String longName, String shortName) {
    switch (index) {
        case kExportPartMeristem:
            longName = "Meristem";
            shortName = "Mrstm";
            break;
        case kExportPartInternode:
            longName = "Internode";
            shortName = "Intrnd";
            break;
        case kExportPartSeedlingLeaf:
            longName = "Seedling leaf";
            shortName = "1stLeaf";
            break;
        case kExportPartLeaf:
            longName = "Leaf";
            shortName = "Leaf";
            break;
        case kExportPartFirstPetiole:
            longName = "Seedling petiole";
            shortName = "1stPetiole";
            break;
        case kExportPartPetiole:
            longName = "Petiole";
            shortName = "Petiole";
            break;
        case kExportPartLeafStipule:
            longName = "Leaf stipule";
            shortName = "Stipule";
            break;
        case kExportPartInflorescenceStalkFemale:
            longName = "Primary inflorescence stalk (peduncle)";
            shortName = "1Pdncle";
            break;
        case kExportPartInflorescenceInternodeFemale:
            longName = "Primary inflorescence internode";
            shortName = "1InfInt";
            break;
        case kExportPartInflorescenceBractFemale:
            longName = "Primary inflorescence bract";
            shortName = "1Bract";
            break;
        case kExportPartInflorescenceStalkMale:
            longName = "Secondary inflorescence stalk (peduncle)";
            shortName = "2Pdncle";
            break;
        case kExportPartInflorescenceInternodeMale:
            longName = "Secondary inflorescence internode";
            shortName = "2InfInt";
            break;
        case kExportPartInflorescenceBractMale:
            longName = "Secondary inflorescence bract";
            shortName = "2Bract";
            break;
        case kExportPartPedicelFemale:
            longName = "Primary flower stalk";
            shortName = "1Pdcel";
            break;
        case kExportPartFlowerBudFemale:
            longName = "Primary flower bud";
            shortName = "1Bud";
            break;
        case kExportPartStyleFemale:
            longName = "Flower style";
            shortName = "Style";
            break;
        case kExportPartStigmaFemale:
            longName = "Flower stigma";
            shortName = "Stigma";
            break;
        case kExportPartFilamentFemale:
            longName = "Primary flower filament";
            shortName = "1Flmnt";
            break;
        case kExportPartAntherFemale:
            longName = "Primary flower anther";
            shortName = "1Anther";
            break;
        case kExportPartFirstPetalsFemale:
            longName = "Primary flower petal, first row";
            shortName = "1Petal1";
            break;
        case kExportPartSecondPetalsFemale:
            longName = "Flower petal, second row";
            shortName = "1Petal2";
            break;
        case kExportPartThirdPetalsFemale:
            longName = "Flower petal, third row";
            shortName = "1Petal3";
            break;
        case kExportPartFourthPetalsFemale:
            longName = "Flower petal, fourth row";
            shortName = "1Petal4";
            break;
        case kExportPartFifthPetalsFemale:
            longName = "Flower petal, fifth row";
            shortName = "1Petal5";
            break;
        case kExportPartSepalsFemale:
            longName = "Primary flower sepal";
            shortName = "1Sepal";
            break;
        case kExportPartPedicelMale:
            longName = "Secondary flower stalk";
            shortName = "2Pdcel";
            break;
        case kExportPartFlowerBudMale:
            longName = "Secondary flower bud";
            shortName = "2Bud";
            break;
        case kExportPartFilamentMale:
            longName = "Secondary flower filament";
            shortName = "2Flmnt";
            break;
        case kExportPartAntherMale:
            longName = "Secondary flower anther";
            shortName = "2Anther";
            break;
        case kExportPartFirstPetalsMale:
            longName = "Secondary flower petal";
            shortName = "2Petal1";
            break;
        case kExportPartSepalsMale:
            longName = "Secondary flower sepal";
            shortName = "2Sepal";
            break;
        case kExportPartUnripeFruit:
            longName = "Unripe fruit";
            shortName = "FruitU";
            break;
        case kExportPartRipeFruit:
            longName = "Ripe fruit";
            shortName = "FruitR";
            break;
        case kExportPartRootTop:
            longName = "Root top";
            shortName = "Root";
            break;
        default:
            throw new GeneralException.create("Problem: Invalid part type in method getInfoForDXFPartType.");
            break;
    return longName, shortName;
}


// don't save in settings file
// to deal with quirks in other programs
// specific (keep in generic structure so one window can handle all of these)
class KfFileExportSurface extends KfDrawingSurface {
    public String fileName;
    public float scale;
    public FileExport3DOptionsStructure options;
    public String currentPlantNameLong;
    public String currentPlantNameShort;
    public boolean currentPlantIsTranslated;
    public float currentPlantTranslateX;
    public float currentPlantTranslateY;
    public short currentPlantIndex;
    public String currentGroupingString;
    public TColorRef currentColor;
    public  plantPartCounts;
    public int numPoints;
    public  points;
    public int numFaces;
    public  faces;
    
    // ----------------------------------------------------------------------------- KfFileExportSurface 
    public void createWithFileName(String aFileName) {
        super.create();
        this.fileName = aFileName;
        this.options = udomain.domain.exportOptionsFor3D[this.outputType()];
        this.scale = this.options.overallScalingFactor_pct / 100.0;
    }
    
    public void destroy() {
        pass
        // nothing yet
    }
    
    public void startFile() {
        throw new GeneralException.create("subclasses must override");
    }
    
    public void endFile() {
        throw new GeneralException.create("subclasses must override");
    }
    
    public void startPlant(String aLongName, short aPlantIndex) {
        this.currentPlantIndex = aPlantIndex;
        this.currentPlantNameLong = aLongName;
        this.currentPlantNameShort = this.generateShortName();
    }
    
    public void endPlant() {
        pass
        // subclasses can override
    }
    
    public void writeRegistrationReminder(KFPoint3D p1, KFPoint3D p2, KFPoint3D p3, KFPoint3D p4) {
        throw new GeneralException.create("subclasses must override");
    }
    
    public void startNestedGroupOfPlantParts(String groupName, String shortName, short nestingType) {
        pass
        // subclasses can override
    }
    
    public void endNestedGroupOfPlantParts(short nestingType) {
        pass
        // subclasses can override
    }
    
    public void startPlantPart(String aLongName, String aShortName) {
        pass
        // subclasses can override
    }
    
    public void endPlantPart() {
        pass
        // subclasses can override
    }
    
    public void startStemSegment(String aLongName, String aShortName, TColorRef color, float width, short index) {
        this.setUpGroupingStringForStemSegmentOr3DObject(aShortName, index);
    }
    
    public void start3DObject(String aLongName, String aShortName, TColorRef color, short index) {
        this.setUpGroupingStringForStemSegmentOr3DObject(aShortName, index);
    }
    
    public void startVerticesAndTriangles() {
        pass
        // subclasses can override
    }
    
    public void endVerticesAndTriangles() {
        pass
        // subclasses can override
    }
    
    public void addPoint(KfPoint3D point) {
        if (this.numPoints >= kMax3DPoints) {
            throw new GeneralException.Create("Problem: Too many points in 3D export.");
        }
        this.points[this.numPoints].x = this.pressedOrNot(this.scale * Point.x, kX);
        this.points[this.numPoints].y = this.pressedOrNot(this.scale * Point.y, kY);
        this.points[this.numPoints].z = this.pressedOrNot(this.scale * Point.z, kZ);
        this.numPoints += 1;
    }
    
    public float pressedOrNot(float value, short dimension) {
        result = 0.0;
        if ((this.options.pressPlants) && (this.options.directionToPressPlants == dimension)) {
            result = 0;
        } else {
            result = value;
        }
        return result;
    }
    
    public void addTriangle(int a, int b, int c) {
        if (this.numFaces >= kMax3DFaces) {
            throw new GeneralException.Create("Problem: Too many faces in 3D export.");
        }
        this.faces[this.numFaces].vertex1 = a;
        this.faces[this.numFaces].vertex2 = b;
        this.faces[this.numFaces].vertex3 = c;
        this.numFaces += 1;
    }
    
    public void end3DObject() {
        pass
        // subclasses can override
    }
    
    public void setUpGroupingStringForStemSegmentOr3DObject(String aShortName, short index) {
        switch (this.options.layeringOption) {
            case kLayerOutputAllTogether:
                this.currentGroupingString = this.currentPlantNameShort;
                break;
            case kLayerOutputByTypeOfPlantPart:
                this.currentGroupingString = this.currentPlantNameShort + "_" + aShortName;
                break;
            case kLayerOutputByPlantPart:
                this.plantPartCounts[index] += 1;
                this.currentGroupingString = this.currentPlantNameShort + "_" + IntToStr(this.plantPartCounts[index]) + "_" + aShortName;
                break;
    }
    
    public void endStemSegment() {
        pass
        // subclasses can override
    }
    
    public void drawPipeFaces( startPoints,  endPoints, short faces, short segmentNumber) {
        long i = 0;
        long disp = 0;
        
        // subclasses can override - this works for some
        disp = segmentNumber * faces * 2;
        for (i = 0; i <= faces - 1; i++) {
            this.addPoint(startPoints[i]);
        }
        for (i = 0; i <= faces - 1; i++) {
            this.addPoint(endPoints[i]);
        }
        for (i = 0; i <= faces - 1; i++) {
            this.addTriangle(disp + i, disp + i + faces, disp + (i + 1) % faces);
            this.addTriangle(disp + (i + 1) % faces, disp + i + faces, disp + (i + 1) % faces + faces);
        }
    }
    
    public void setTranslationForCurrentPlant(boolean isTranslated, float aTranslateX, float aTranslateY) {
        this.currentPlantIsTranslated = isTranslated;
        this.currentPlantTranslateX = aTranslateX;
        this.currentPlantTranslateY = aTranslateY;
    }
    
    public short outputType() {
        result = 0;
        result = -1;
        if ((this instanceof KfDrawingSurfaceForDXF)) {
            result = kDXF;
        } else if ((this instanceof KfDrawingSurfaceForPOV)) {
            result = kPOV;
        } else if ((this instanceof KfDrawingSurfaceFor3DS)) {
            result = k3DS;
        } else if ((this instanceof KfDrawingSurfaceForOBJ)) {
            result = kOBJ;
        } else if ((this instanceof KfDrawingSurfaceForVRML)) {
            result = kVRML;
        } else if ((this instanceof KfDrawingSurfaceForLWO)) {
            result = kLWO;
        }
        return result;
    }
    
    public String generateShortName() {
        result = "";
        int shortNameLength = 0;
        int i = 0;
        
        result = "";
        if (len(this.currentPlantNameLong) <= 0) {
            return result;
        }
        shortNameLength = umath.intMin(this.options.lengthOfShortName, len(this.currentPlantNameLong));
        for (i = 1; i <= shortNameLength; i++) {
            if (this.currentPlantNameLong[i] != " ") {
                result = result + UNRESOLVED.copy(this.currentPlantNameLong, i, 1);
            }
        }
        if (this.options.writePlantNumberInFrontOfName) {
            result = IntToStr(this.currentPlantIndex + 1) + result;
        }
        return result;
    }
    
}
class KfTextFileExportSurface extends KfFileExportSurface {
    public TextFile outputFile;
    
    // ----------------------------------------------------------------------------- KfTextFileExportSurface 
    public void createWithFileName(String aFileName) {
        super.createWithFileName(aFileName);
        // we assume that the file name has been already okayed by whoever created us
        AssignFile(this.outputFile, this.fileName);
    }
    
    public void destroy() {
        pass
        // nothing yet
    }
    
    public void startFile() {
        Rewrite(this.outputFile);
    }
    
    public void endFile() {
        CloseFile(this.outputFile);
    }
    
}
class KfDrawingSurfaceForDXF extends KfTextFileExportSurface {
    public short currentColorIndex;
    
    // ----------------------------------------------------------------------------- KfDrawingSurfaceForDXF 
    public void startFile() {
        super.startFile();
        writeln(this.outputFile, "999");
        writeln(this.outputFile, "DXF created by PlantStudio http://www.kurtz-fernhout.com");
        // v2.0 moved ENTITY section from starting and ending each plant to entire file - may fix bug
        // with programs only recognizing one plant in a file
        writeln(this.outputFile, "0");
        writeln(this.outputFile, "SECTION");
        writeln(this.outputFile, "2");
        writeln(this.outputFile, "ENTITIES");
    }
    
    public void endFile() {
        // v2.0 moved ENTITY section from starting and ending each plant to entire file - may fix bug
        // with programs only recognizing one plant in a file
        writeln(this.outputFile, "0");
        writeln(this.outputFile, "ENDSEC");
        writeln(this.outputFile, "0");
        writeln(this.outputFile, "EOF");
        super.endFile();
    }
    
    public void startPlant(String aLongName, short aPlantIndex) {
        super.startPlant(aLongName, aPlantIndex);
        if (this.options.layeringOption == kLayerOutputAllTogether) {
            this.currentGroupingString = UNRESOLVED.copy(this.currentPlantNameLong, 1, 16);
        }
        if (this.options.dxf_whereToGetColors == kColorDXFFromOneColor) {
            this.currentColorIndex = this.options.dxf_wholePlantColorIndex;
        }
    }
    
    public void startStemSegment(String aLongName, String aShortName, TColorRef color, float width, short index) {
        super.startStemSegment(aLongName, aShortName, color, width, index);
        if (this.options.dxf_whereToGetColors == kColorDXFFromPlantPartType) {
            this.currentColorIndex = this.options.dxf_plantPartColorIndexes[index];
        } else if (this.options.dxf_whereToGetColors == kColorDXFFromRGB) {
            this.currentColor = color;
        }
    }
    
    public void start3DObject(String aLongName, String aShortName, TColorRef color, short index) {
        super.start3DObject(aLongName, aShortName, color, index);
        if (this.options.dxf_whereToGetColors == kColorDXFFromPlantPartType) {
            this.currentColorIndex = this.options.dxf_plantPartColorIndexes[index];
        } else if (this.options.dxf_whereToGetColors == kColorDXFFromRGB) {
            this.currentColor = color;
        }
    }
    
    public void drawPipeFaces( startPoints,  endPoints, short faces, short segmentNumber) {
        short i = 0;
        
        for (i = 0; i <= faces - 1; i++) {
            // for this don't have to worry about segment number, we are not adding points and triangles
            this.draw3DFace(startPoints[i], endPoints[i], endPoints[(i + 1) % faces], startPoints[(i + 1) % faces]);
        }
    }
    
    public void draw3DFace(KfPoint3D point1, KfPoint3D point2, KfPoint3D point3, KfPoint3D point4) {
        writeln(this.outputFile, "0");
        writeln(this.outputFile, "3DFACE");
        writeln(this.outputFile, "8");
        writeln(this.outputFile, this.currentGroupingString);
        if (this.options.writeColors) {
            if (this.options.dxf_whereToGetColors == kColorDXFFromRGB) {
                writeln(this.outputFile, "62");
                writeln(this.outputFile, IntToStr(this.currentColor));
            } else {
                writeln(this.outputFile, "62");
                writeln(this.outputFile, IntToStr(this.currentColorIndex + 1));
            }
        }
        writeln(this.outputFile, "10");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * point1.x, kX)));
        writeln(this.outputFile, "20");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * -point1.y, kY)));
        writeln(this.outputFile, "30");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * point1.z, kZ)));
        writeln(this.outputFile, "11");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * point2.x, kX)));
        writeln(this.outputFile, "21");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * -point2.y, kY)));
        writeln(this.outputFile, "31");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * point2.z, kZ)));
        writeln(this.outputFile, "12");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * point3.x, kX)));
        writeln(this.outputFile, "22");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * -point3.y, kY)));
        writeln(this.outputFile, "32");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * point3.z, kZ)));
        writeln(this.outputFile, "13");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * point4.x, kX)));
        writeln(this.outputFile, "23");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * -point4.y, kY)));
        writeln(this.outputFile, "33");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * point4.z, kZ)));
    }
    
    public void basicDrawLineFromTo(KfPoint3D startPoint, KfPoint3D endPoint) {
        this.draw3DFace(startPoint, startPoint, endPoint, endPoint);
    }
    
    public void basicDrawTriangle(KfTriangle triangle) {
        this.draw3DFace(triangle.points[0], triangle.points[1], triangle.points[2], triangle.points[2]);
    }
    
    public void writeRegistrationReminder(KFPoint3D p1, KFPoint3D p2, KFPoint3D p3, KFPoint3D p4) {
        this.currentGroupingString = this.currentPlantNameShort + "_rem";
        // adds one; kLastDxfColorIndex is gray
        this.currentColorIndex = kLastDxfColorIndex - 1;
        this.draw3DFace(p1, p2, p3, p3);
        this.draw3DFace(p1, p3, p4, p4);
    }
    
}
class KfDrawingSurfaceForPOV extends KfTextFileExportSurface {
    public String currentComment;
    public float currentWidth;
    public int currentIndentLevel;
    public String currentRotateString;
    public short numPlantsDrawn;
    public  plantNames;
    
    // ----------------------------------------------------------------------------- KfDrawingSurfaceForPOV 
    public void startFile() {
        super.startFile();
        writeln(this.outputFile, "// INC file for Persistence of Vision (POV) raytracer");
        writeln(this.outputFile, "// created by PlantStudio http://www.kurtz-fernhout.com");
        writeln(this.outputFile);
    }
    
    public void endFile() {
        short i = 0;
        
        writeln(this.outputFile);
        if (this.options.pov_commentOutUnionAtEnd) {
            writeln(this.outputFile, "/* ");
        }
        writeln(this.outputFile, "#declare allPlants_" + usupport.replacePunctuationWithUnderscores(usupport.stringUpTo(ExtractFileName(this.fileName), ".")) + " = union {");
        for (i = 0; i <= this.numPlantsDrawn - 1; i++) {
            writeln(this.outputFile, chr(9) + "object { " + this.plantNames[i] + " }");
        }
        writeln(this.outputFile, chr(9) + "}");
        if (this.options.pov_commentOutUnionAtEnd) {
            writeln(this.outputFile, "*/ ");
        }
        super.endFile();
    }
    
    public void startPlant(String aLongName, short aPlantIndex) {
        // in POV you can't have spaces in names
        aLongName = usupport.replacePunctuationWithUnderscores(aLongName);
        super.startPlant(aLongName, aPlantIndex);
        writeln(this.outputFile, "#declare " + this.currentPlantNameLong + " = union {");
        this.currentIndentLevel = 0;
        this.indent();
        this.plantNames[this.numPlantsDrawn] = this.currentPlantNameLong;
        this.numPlantsDrawn += 1;
    }
    
    public void endPlant() {
        if ((this.currentPlantIsTranslated) && (this.options.translatePlantsToWindowPositions)) {
            writeln(this.outputFile, "translate <" + usupport.valueString(this.currentPlantTranslateX) + ", " + usupport.valueString(this.currentPlantTranslateY) + ", 0>");
        }
        if (!this.options.writeColors) {
            write(this.outputFile, "pigment { color rgb <0.8, 0.8, 0.8> }");
        }
        writeln(this.outputFile, "} // end " + this.currentPlantNameLong);
        writeln(this.outputFile);
        this.currentIndentLevel = 0;
        super.endPlant();
    }
    
    public void startNestedGroupOfPlantParts(String groupName, String shortName, short nestingType) {
        switch (nestingType) {
            case kNestingTypeInflorescence:
                if (!this.options.nest_Inflorescence) {
                    return;
                }
                break;
            case kNestingTypeLeafAndPetiole:
                if (!this.options.nest_LeafAndPetiole) {
                    return;
                }
                break;
            case kNestingTypeCompoundLeaf:
                if (!this.options.nest_CompoundLeaf) {
                    return;
                }
                break;
            case kNestingTypePedicelAndFlowerFruit:
                if (!this.options.nest_PedicelAndFlowerFruit) {
                    return;
                }
                break;
            case kNestingTypeFloralLayers:
                if (!this.options.nest_FloralLayers) {
                    return;
                }
                break;
            default:
                throw new GeneralException.create("Problem: Unrecognized nesting type in KfDrawingSurfaceForPOV.startNestedGroupOfPlantParts.");
                break;
        this.startUnion(groupName);
    }
    
    public void endNestedGroupOfPlantParts(short nestingType) {
        switch (nestingType) {
            case kNestingTypeInflorescence:
                if (!this.options.nest_Inflorescence) {
                    return;
                }
                break;
            case kNestingTypeLeafAndPetiole:
                if (!this.options.nest_LeafAndPetiole) {
                    return;
                }
                break;
            case kNestingTypeCompoundLeaf:
                if (!this.options.nest_CompoundLeaf) {
                    return;
                }
                break;
            case kNestingTypePedicelAndFlowerFruit:
                if (!this.options.nest_PedicelAndFlowerFruit) {
                    return;
                }
                break;
            case kNestingTypeFloralLayers:
                if (!this.options.nest_FloralLayers) {
                    return;
                }
                break;
            default:
                throw new GeneralException.create("Problem: Unrecognized nesting type in KfDrawingSurfaceForPOV.startNestedGroupOfPlantParts.");
                break;
        this.endBrace(kDontWriteColor);
    }
    
    public void startPlantPart(String aLongName, String aShortName) {
        this.startUnion(aLongName);
    }
    
    public void endPlantPart() {
        this.endBrace(kDontWriteColor);
    }
    
    public void startStemSegment(String aLongName, String aShortName, TColorRef color, float width, short index) {
        super.startStemSegment(aLongName, aShortName, color, width, index);
        this.startUnion(aLongName);
        this.setColor(color);
        this.currentWidth = width;
    }
    
    public void endStemSegment() {
        // DO want to write color for this one
        this.endBrace(kWriteColor);
    }
    
    public void start3DObject(String aLongName, String aShortName, TColorRef color, short index) {
        super.start3DObject(aLongName, aShortName, color, index);
        this.startMesh(color, aLongName);
        this.setColor(color);
    }
    
    public void end3DObject() {
        // DO want to write color for this one
        this.endBrace(kWriteColor);
    }
    
    public void indent() {
        this.currentIndentLevel += 1;
    }
    
    public void unindent() {
        this.currentIndentLevel -= 1;
        if (this.currentIndentLevel < 0) {
            this.currentIndentLevel = 0;
        }
    }
    
    public void doIndenting() {
        int i = 0;
        
        for (i = 1; i <= this.currentIndentLevel; i++) {
            write(this.outputFile, chr(9));
        }
    }
    
    public void startUnionOrMesh(String startString, TColorRef aColor, String aComment) {
        if (aColor >= 0) {
            this.currentColor = aColor;
        }
        this.doIndenting();
        write(this.outputFile, startString + " {");
        if (len(aComment) > 0) {
            writeln(this.outputFile, " // " + aComment);
        } else {
            writeln(this.outputFile, " // " + this.currentComment);
        }
        this.indent();
    }
    
    public void startUnion(String aComment) {
        this.startUnionOrMesh("union", -1, aComment);
    }
    
    public void startMesh(TColorRef aColor, String aComment) {
        this.startUnionOrMesh("mesh", aColor, aComment);
    }
    
    public void setColor(TColorRef aColor) {
        this.currentColor = aColor;
    }
    
    public void endBrace(boolean writeColor) {
        this.doIndenting();
        if ((writeColor) && (this.options.writeColors) && (this.currentColor >= 0)) {
            write(this.outputFile, "pigment { color rgb <" + usupport.valueString(UNRESOLVED.getRValue(this.currentColor) / 256.0) + ", " + usupport.valueString(UNRESOLVED.getGValue(this.currentColor) / 256.0) + ", " + usupport.valueString(UNRESOLVED.getBValue(this.currentColor) / 256.0) + "> }");
        }
        writeln(this.outputFile, "}");
        this.unindent();
    }
    
    public void basicDrawLineFromTo(KfPoint3D startPoint, KfPoint3D endPoint) {
        KfPoint3D endPointFinal = new KfPoint3D();
        
        endPointFinal = endPoint;
        this.doIndenting();
        write(this.outputFile, "cylinder { ");
        writeln(this.outputFile, "<" + usupport.valueString((this.pressedOrNot(this.scale * startPoint.x, kX))) + ", " + usupport.valueString(this.pressedOrNot(this.scale * -startPoint.y, kY)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * startPoint.z, kZ)) + ">, <" + usupport.valueString(this.pressedOrNot(this.scale * endPointFinal.x, kX)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * -endPointFinal.y, kY)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * endPointFinal.z, kZ)) + ">, " + usupport.valueString(this.scale * this.currentWidth) + " }");
    }
    
    public void basicDrawTriangle(KfTriangle triangle) {
        KfPoint3D p1 = new KfPoint3D();
        KfPoint3D p2 = new KfPoint3D();
        KfPoint3D p3 = new KfPoint3D();
        
        p1 = triangle.points[0];
        p2 = triangle.points[1];
        p3 = triangle.points[2];
        this.doIndenting();
        write(this.outputFile, "triangle { <");
        // all y values must be negative because it seems our coordinate systems are different
        write(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * p1.x, kX)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * -p1.y, kY)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * p1.z, kZ)) + ">, <");
        write(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * p2.x, kX)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * -p2.y, kY)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * p2.z, kZ)) + ">, <");
        writeln(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * p3.x, kX)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * -p3.y, kY)) + ", " + usupport.valueString(this.pressedOrNot(this.scale * p3.z, kZ)) + "> }");
    }
    
    public void writeRegistrationReminder(KFPoint3D p1, KFPoint3D p2, KFPoint3D p3, KFPoint3D p4) {
        KfTriangle triangle1 = new KfTriangle();
        KfTriangle triangle2 = new KfTriangle();
        
        this.startMesh(UNRESOLVED.rgb(100, 100, 100), this.currentPlantNameShort + "_reminder");
        triangle1 = u3dsupport.KfTriangle.create;
        triangle2 = u3dsupport.KfTriangle.create;
        try {
            triangle1.points[0] = p1;
            triangle1.points[1] = p2;
            triangle1.points[2] = p3;
            this.basicDrawTriangle(triangle1);
            triangle2.points[0] = p1;
            triangle2.points[1] = p3;
            triangle2.points[2] = p4;
            this.basicDrawTriangle(triangle2);
        } finally {
            triangle1.free;
            triangle2.free;
        }
        this.endBrace(kWriteColor);
    }
    
}
class KfDrawingSurfaceForVRML extends KfTextFileExportSurface {
    public int currentIndentLevel;
    public String lastPlantPartName;
    public String lastMeshName;
    
    // ----------------------------------------------------------------------------- KfDrawingSurfaceForVRML 
    public void startFile() {
        String scaleString = "";
        
        super.startFile();
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                writeln(this.outputFile, "#VRML V1.0 ascii");
                writeln(this.outputFile, "#Created by PlantStudio http://www.kurtz-fernhout.com");
                writeln(this.outputFile);
                break;
            case kVRMLVersionTwo:
                writeln(this.outputFile, "#VRML V2.0 utf8");
                writeln(this.outputFile, "#Created by PlantStudio http://www.kurtz-fernhout.com");
                writeln(this.outputFile);
                break;
    }
    
    public void startPlant(String aLongName, short aPlantIndex) {
        // in VRML you can't have spaces in names
        aLongName = usupport.replacePunctuationWithUnderscores(aLongName);
        super.startPlant(aLongName, aPlantIndex);
        this.currentIndentLevel = 0;
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                this.writeThenIndent("DEF " + this.currentPlantNameShort + " Group {");
                break;
            case kVRMLVersionTwo:
                this.writeThenIndent("DEF " + this.currentPlantNameShort + " Group {");
                this.writeThenIndent("children [");
                break;
    }
    
    public void endPlant() {
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                this.endBrace("plant " + this.currentPlantNameLong);
                writeln(this.outputFile);
                break;
            case kVRMLVersionTwo:
                this.endBracket("children");
                this.endBrace("plant " + this.currentPlantNameLong);
                writeln(this.outputFile);
                break;
        this.currentIndentLevel = 0;
        super.endPlant();
    }
    
    public void startNestedGroupOfPlantParts(String groupName, String shortName, short nestingType) {
        shortName = this.currentPlantNameShort + "_" + shortName;
        switch (nestingType) {
            case kNestingTypeInflorescence:
                if (!this.options.nest_Inflorescence) {
                    return;
                }
                break;
            case kNestingTypeLeafAndPetiole:
                if (!this.options.nest_LeafAndPetiole) {
                    return;
                }
                break;
            case kNestingTypeCompoundLeaf:
                if (!this.options.nest_CompoundLeaf) {
                    return;
                }
                break;
            case kNestingTypePedicelAndFlowerFruit:
                if (!this.options.nest_PedicelAndFlowerFruit) {
                    return;
                }
                break;
            case kNestingTypeFloralLayers:
                if (!this.options.nest_FloralLayers) {
                    return;
                }
                break;
            default:
                throw new GeneralException.create("Problem: Unrecognized nesting type in KfDrawingSurfaceForVRML.startNestedGroupOfPlantParts.");
                break;
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                this.writeThenIndent("DEF " + shortName + " Group {");
                break;
            case kVRMLVersionTwo:
                this.writeThenIndent("DEF " + shortName + " Group {");
                this.writeThenIndent("children [");
                break;
    }
    
    public void endNestedGroupOfPlantParts(short nestingType) {
        switch (nestingType) {
            case kNestingTypeInflorescence:
                if (!this.options.nest_Inflorescence) {
                    return;
                }
                break;
            case kNestingTypeLeafAndPetiole:
                if (!this.options.nest_LeafAndPetiole) {
                    return;
                }
                break;
            case kNestingTypeCompoundLeaf:
                if (!this.options.nest_CompoundLeaf) {
                    return;
                }
                break;
            case kNestingTypePedicelAndFlowerFruit:
                if (!this.options.nest_PedicelAndFlowerFruit) {
                    return;
                }
                break;
            case kNestingTypeFloralLayers:
                if (!this.options.nest_FloralLayers) {
                    return;
                }
                break;
            default:
                throw new GeneralException.create("Problem: Unrecognized nesting type in KfDrawingSurfaceForVRML.endNestedGroupOfPlantParts.");
                break;
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                this.endBrace("nested group");
                writeln(this.outputFile);
                break;
            case kVRMLVersionTwo:
                this.endBracket("children");
                this.endBrace("nested group");
                writeln(this.outputFile);
                break;
    }
    
    public void startPlantPart(String aLongName, String aShortName) {
        String shortName = "";
        
        shortName = this.currentPlantNameShort + "_" + aShortName;
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                this.writeThenIndent("DEF " + shortName + " Group {");
                break;
            case kVRMLVersionTwo:
                this.writeThenIndent("DEF " + shortName + " Group {");
                this.writeThenIndent("children [");
                break;
        this.lastPlantPartName = shortName;
    }
    
    public void endPlantPart() {
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                this.endBrace("plant part " + this.lastPlantPartName);
                writeln(this.outputFile);
                break;
            case kVRMLVersionTwo:
                this.endBracket("children");
                this.endBrace("plant part " + this.lastPlantPartName);
                writeln(this.outputFile);
                break;
    }
    
    public void startStemSegment(String aLongName, String aShortName, TColorRef color, float width, short index) {
        super.startStemSegment(aLongName, aShortName, color, width, index);
        this.setColor(color);
        this.startMesh();
    }
    
    public void endStemSegment() {
        this.endMesh();
    }
    
    public void start3DObject(String aLongName, String aShortName, TColorRef color, short index) {
        super.start3DObject(aLongName, aShortName, color, index);
        this.setColor(color);
        this.startMesh();
    }
    
    public void end3DObject() {
        this.endMesh();
    }
    
    public void startMesh() {
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                this.writeThenIndent("DEF " + this.currentGroupingString + " Group {");
                break;
            case kVRMLVersionTwo:
                this.writeConsideringIndenting("DEF " + this.currentGroupingString + " Shape {");
                this.indent();
                if (this.options.writeColors) {
                    this.writeConsideringIndenting("appearance Appearance { material Material { diffuseColor " + usupport.valueString(UNRESOLVED.getRValue(this.currentColor) / 256.0) + " " + usupport.valueString(UNRESOLVED.getGValue(this.currentColor) / 256.0) + " " + usupport.valueString(UNRESOLVED.getBValue(this.currentColor) / 256.0) + " } }");
                }
                break;
        this.lastMeshName = this.currentGroupingString;
    }
    
    public void endMesh() {
        this.writePointsAndTriangles();
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                this.endBrace("mesh " + this.lastMeshName);
                writeln(this.outputFile);
                break;
            case kVRMLVersionTwo:
                this.endBrace("shape " + this.lastMeshName);
                writeln(this.outputFile);
                break;
    }
    
    public void writePointsAndTriangles() {
        short i = 0;
        
        switch (this.options.vrml_version) {
            case kVRMLVersionOne:
                // shape hints
                this.writeThenIndent("ShapeHints {");
                this.writeConsideringIndenting("vertexOrdering COUNTERCLOCKWISE");
                this.writeConsideringIndenting("shapeType SOLID");
                this.writeConsideringIndenting("faceType CONVEX");
                this.endBrace("ShapeHints");
                if (this.options.writeColors) {
                    // color
                    this.writeConsideringIndenting("Material { diffuseColor [ " + usupport.valueString(UNRESOLVED.getRValue(this.currentColor) / 256.0) + " " + usupport.valueString(UNRESOLVED.getGValue(this.currentColor) / 256.0) + " " + usupport.valueString(UNRESOLVED.getBValue(this.currentColor) / 256.0) + " ] }");
                }
                // coordinate points
                this.writeThenIndent("Coordinate3 {");
                this.writeThenIndent("point [");
                this.doIndenting();
                for (i = 0; i <= this.numPoints - 1; i++) {
                    write(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * this.points[i].x, kX)) + " " + usupport.valueString(this.pressedOrNot(this.scale * -this.points[i].y, kY)) + " " + usupport.valueString(this.pressedOrNot(this.scale * this.points[i].z, kZ)));
                    if (i < this.numPoints - 1) {
                        write(this.outputFile, ", ");
                    }
                    if ((i % kNumVRMLPointsPerLine == 0) || (i == this.numPoints - 1)) {
                        writeln(this.outputFile);
                        if (i < this.numPoints - 1) {
                            this.doIndenting();
                        }
                    }
                }
                this.endBracket("point");
                this.endBrace("Coordinate3");
                // faces
                //'DEF ' + self.currentGroupingString +
                this.writeThenIndent("IndexedFaceSet {");
                this.writeThenIndent("coordIndex [");
                this.doIndenting();
                for (i = 0; i <= this.numFaces - 1; i++) {
                    write(this.outputFile, IntToStr(this.faces[i].vertex1) + ", " + IntToStr(this.faces[i].vertex2) + ", " + IntToStr(this.faces[i].vertex3) + ", -1");
                    if (i < this.numFaces - 1) {
                        write(this.outputFile, ", ");
                    }
                    if ((i % kNumVRMLPointsPerLine == 0) || (i == this.numFaces - 1)) {
                        writeln(this.outputFile);
                        if (i < this.numFaces - 1) {
                            this.doIndenting();
                        }
                    }
                }
                this.endBracket("coordIndex");
                this.endBrace("IndexedFaceSet");
                break;
            case kVRMLVersionTwo:
                this.writeThenIndent("geometry IndexedFaceSet {");
                this.writeThenIndent("coord Coordinate {");
                this.writeThenIndent("point [");
                this.doIndenting();
                for (i = 0; i <= this.numPoints - 1; i++) {
                    write(this.outputFile, usupport.valueString(this.pressedOrNot(this.scale * this.points[i].x, kX)) + " " + usupport.valueString(this.pressedOrNot(this.scale * -this.points[i].y, kY)) + " " + usupport.valueString(this.pressedOrNot(this.scale * this.points[i].z, kZ)));
                    if (i < this.numPoints - 1) {
                        write(this.outputFile, ", ");
                    }
                    if ((i % kNumVRMLPointsPerLine == 0) || (i == this.numPoints - 1)) {
                        writeln(this.outputFile);
                        if (i < this.numPoints - 1) {
                            this.doIndenting();
                        }
                    }
                }
                this.endBracket("point");
                this.endBrace("Coordinate");
                this.writeConsideringIndenting("ccw TRUE");
                this.writeConsideringIndenting("colorPerVertex FALSE");
                this.writeThenIndent("coordIndex [");
                this.doIndenting();
                for (i = 0; i <= this.numFaces - 1; i++) {
                    write(this.outputFile, IntToStr(this.faces[i].vertex1) + ", " + IntToStr(this.faces[i].vertex2) + ", " + IntToStr(this.faces[i].vertex3) + ", -1");
                    if (i < this.numFaces - 1) {
                        write(this.outputFile, ", ");
                    }
                    if ((i % kNumVRMLPointsPerLine == 0) || (i == this.numFaces - 1)) {
                        writeln(this.outputFile);
                        if (i < this.numFaces - 1) {
                            this.doIndenting();
                        }
                    }
                }
                this.endBracket("coordIndex");
                this.writeConsideringIndenting("creaseAngle 0.5");
                this.writeConsideringIndenting("normalPerVertex TRUE");
                this.writeConsideringIndenting("solid FALSE");
                this.endBrace("IndexedFaceSet");
                break;
        this.numPoints = 0;
        this.numFaces = 0;
    }
    
    public void setColor(TColorRef aColor) {
        this.currentColor = aColor;
    }
    
    public void endBrace(String comment) {
        this.doIndenting();
        writeln(this.outputFile, "} # " + comment);
        this.unindent();
    }
    
    public void endBracket(String comment) {
        this.doIndenting();
        writeln(this.outputFile, "] # " + comment);
        this.unindent();
    }
    
    public void indent() {
        this.currentIndentLevel += 1;
    }
    
    public void unindent() {
        this.currentIndentLevel -= 1;
        if (this.currentIndentLevel < 0) {
            this.currentIndentLevel = 0;
        }
    }
    
    public void doIndenting() {
        int i = 0;
        
        for (i = 1; i <= this.currentIndentLevel; i++) {
            // chr(9));
            write(this.outputFile, "  ");
        }
    }
    
    public void writeConsideringIndenting(String aString) {
        this.doIndenting();
        writeln(this.outputFile, aString);
    }
    
    public void indentThenWrite(String aString) {
        this.indent();
        this.doIndenting();
        writeln(this.outputFile, aString);
    }
    
    public void writeThenIndent(String aString) {
        this.doIndenting();
        writeln(this.outputFile, aString);
        this.indent();
    }
    
    public void writeRegistrationReminder(KFPoint3D p1, KFPoint3D p2, KFPoint3D p3, KFPoint3D p4) {
        long numPointsAtStart = 0;
        
        this.setColor(UNRESOLVED.rgb(100, 100, 100));
        this.currentGroupingString = this.currentPlantNameShort + "_reminder";
        this.startMesh();
        numPointsAtStart = this.numPoints;
        this.addPoint(p1);
        this.addPoint(p2);
        this.addPoint(p3);
        this.addPoint(p4);
        this.addTriangle(numPointsAtStart, numPointsAtStart + 1, numPointsAtStart + 3);
        this.addTriangle(numPointsAtStart + 1, numPointsAtStart + 2, numPointsAtStart + 3);
        this.writePointsAndTriangles();
        this.endMesh();
    }
    
}
class KfDrawingSurfaceForOBJ extends KfTextFileExportSurface {
    public short numMaterialsStored;
    public  materialColors;
    public  materialNames;
    public String materialsFileName;
    
    // ----------------------------------------------------------------------------- KfDrawingSurfaceForOBJ 
    public void startFile() {
        super.startFile();
        writeln(this.outputFile, "# OBJ file created by PlantStudio http://www.kurtz-fernhout.com");
        if (this.options.writeColors) {
            this.materialsFileName = ExtractFilePath(this.fileName) + usupport.stringUpTo(ExtractFileName(this.fileName), ".") + ".mtl";
            writeln(this.outputFile);
            writeln(this.outputFile, "# Materials file must be in same directory");
            writeln(this.outputFile, "mtllib " + ExtractFileName(this.materialsFileName));
        }
    }
    
    public void endFile() {
        if (this.options.writeColors) {
            this.writeMaterialDescriptionsToFile();
        }
        super.endFile();
    }
    
    public void startPlant(String aLongName, short aPlantIndex) {
        super.startPlant(aLongName, aPlantIndex);
        writeln(this.outputFile);
        writeln(this.outputFile, "# plant \"" + this.currentPlantNameLong + "\"");
        writeln(this.outputFile, "o " + this.currentPlantNameShort);
        if ((udomain.domain.registered) && (this.options.layeringOption == kLayerOutputAllTogether)) {
            this.startGroup(this.currentPlantNameShort);
        }
    }
    
    public void startStemSegment(String aLongName, String aShortName, TColorRef color, float width, short index) {
        super.startStemSegment(aLongName, aShortName, color, width, index);
        if ((this.options.layeringOption != kLayerOutputAllTogether) && (this.currentGroupingString != "")) {
            this.startGroup(this.currentGroupingString);
        }
        // color should always be set by the part type, no matter what grouping setting
        this.startColor(color, this.currentPlantNameShort + "_" + aShortName);
        this.startVerticesAndTriangles();
    }
    
    public void endStemSegment() {
        this.endVerticesAndTriangles();
    }
    
    public void start3DObject(String aLongName, String aShortName, TColorRef color, short index) {
        super.start3DObject(aLongName, aShortName, color, index);
        if ((this.options.layeringOption != kLayerOutputAllTogether) && (this.currentGroupingString != "")) {
            this.startGroup(this.currentGroupingString);
        }
        // color should always be set by the part type, no matter what grouping setting
        this.startColor(color, this.currentPlantNameShort + "_" + aShortName);
    }
    
    public void writeMaterialDescriptionsToFile() {
        TextFile materialsFile = new TextFile();
        short i = 0;
        String colorString = "";
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        
        if (this.numMaterialsStored <= 0) {
            return;
        }
        if (usupport.getFileSaveInfo(usupport.kFileTypeMTL, usupport.kDontAskForFileName, this.materialsFileName, fileInfo)) {
            AssignFile(materialsFile, fileInfo.tempFile);
            try {
                usupport.setDecimalSeparator();
                Rewrite(materialsFile);
                usupport.startFileSave(fileInfo);
                writeln(materialsFile, "# Materials for file " + usupport.stringUpTo(ExtractFileName(this.materialsFileName), ".") + ".obj");
                writeln(materialsFile, "# Created by PlantStudio http://www.kurtz-fernhout.com");
                writeln(materialsFile, "# These files must be in the same directory for the materials to be read correctly.");
                for (i = 0; i <= this.numMaterialsStored - 1; i++) {
                    if (this.materialNames[i] == "") {
                        //newmtl name
                        //Ka  0.1 0.0 0.0
                        //Kd  0.4 0.0 0.0
                        //Ks  0.4 0.0 0.0
                        //Ns  20
                        //d  1.0 (0 transparent 1 opaque)
                        //illum 1
                        continue;
                    }
                    writeln(materialsFile, "newmtl " + this.materialNames[i]);
                    colorString = usupport.valueString(UNRESOLVED.GetRValue(this.materialColors[i]) / 255.0) + " " + usupport.valueString(UNRESOLVED.GetGValue(this.materialColors[i]) / 255.0) + " " + usupport.valueString(UNRESOLVED.GetBValue(this.materialColors[i]) / 255.0);
                    writeln(materialsFile, "Ka  " + colorString);
                    writeln(materialsFile, "Kd  " + colorString);
                    writeln(materialsFile, "Ks  " + colorString);
                    writeln(materialsFile, "d 1.0");
                    writeln(materialsFile, "illum 1");
                    writeln(materialsFile);
                }
                fileInfo.writingWasSuccessful = true;
            } finally {
                CloseFile(materialsFile);
                usupport.cleanUpAfterFileSave(fileInfo);
            }
        }
    }
    
    public void storeMaterialDescription(String aName, TColorRef aColor) {
        short i = 0;
        
        if (this.numMaterialsStored > 0) {
            for (i = 0; i <= this.numMaterialsStored - 1; i++) {
                if (this.materialNames[i] == aName) {
                    return;
                }
            }
        }
        if (this.numMaterialsStored >= kMaxStoredMaterials) {
            return;
        }
        this.numMaterialsStored += 1;
        this.materialColors[this.numMaterialsStored] = aColor;
        this.materialNames[this.numMaterialsStored] = aName;
    }
    
    public void startGroup(String aName) {
        writeln(this.outputFile);
        writeln(this.outputFile, "g " + aName);
        writeln(this.outputFile, "s off");
    }
    
    public void startColor(TColorRef aColor, String aMaterialName) {
        if (!this.options.writeColors) {
            return;
        }
        writeln(this.outputFile);
        writeln(this.outputFile, "usemtl " + aMaterialName);
        this.storeMaterialDescription(aMaterialName, aColor);
    }
    
    public void endVerticesAndTriangles() {
        short i = 0;
        
        writeln(this.outputFile);
        writeln(this.outputFile, "# " + IntToStr(this.numPoints) + " vertices");
        for (i = 0; i <= this.numPoints - 1; i++) {
            writeln(this.outputFile, "v " + usupport.valueString(this.pressedOrNot(this.scale * this.points[i].x, kX)) + " " + usupport.valueString(this.pressedOrNot(this.scale * -this.points[i].y, kY)) + " " + usupport.valueString(this.pressedOrNot(this.scale * this.points[i].z, kZ)));
        }
        writeln(this.outputFile);
        writeln(this.outputFile, "# " + IntToStr(this.numFaces) + " faces");
        for (i = 0; i <= this.numFaces - 1; i++) {
            writeln(this.outputFile, "f " + IntToStr(this.faces[i].vertex1 - this.numPoints) + " " + IntToStr(this.faces[i].vertex2 - this.numPoints) + " " + IntToStr(this.faces[i].vertex3 - this.numPoints) + " ");
        }
        this.numPoints = 0;
        this.numFaces = 0;
    }
    
    public void writeRegistrationReminder(KFPoint3D p1, KFPoint3D p2, KFPoint3D p3, KFPoint3D p4) {
        short numPointsAtStart = 0;
        
        this.startGroup(this.currentPlantNameShort + "_reminder");
        this.startColor(UNRESOLVED.rgb(100, 100, 100), "reminder_gray");
        numPointsAtStart = this.numPoints;
        this.startVerticesAndTriangles();
        this.addPoint(p1);
        this.addPoint(p2);
        this.addPoint(p3);
        this.addPoint(p4);
        this.addTriangle(numPointsAtStart, numPointsAtStart + 1, numPointsAtStart + 3);
        this.addTriangle(numPointsAtStart + 1, numPointsAtStart + 2, numPointsAtStart + 3);
        this.endVerticesAndTriangles();
        if (this.options.layeringOption == kLayerOutputAllTogether) {
            this.startGroup(this.currentPlantNameShort);
        }
    }
    
}
class KfBinaryFileExportSurface extends KfFileExportSurface {
    public TFileStream stream;
    public TList chunkStartStack;
    
    // ----------------------------------------------------------------------------- KfBinaryFileExportSurface 
    public void createWithFileName(String aFileName) {
        super.createWithFileName(aFileName);
        this.chunkStartStack = delphi_compatability.TList().Create();
    }
    
    public void destroy() {
        this.chunkStartStack.free;
        this.chunkStartStack = null;
        // this closes the file
        this.stream.free;
        this.stream = null;
        super.destroy();
    }
    
    public void startFile() {
        this.stream = delphi_compatability.TFileStream().Create(this.fileName, delphi_compatability.fmCreate || UNRESOLVED.fmShareExclusive);
    }
    
    public void endFile() {
        throw new GeneralException.create("subclasses must override");
    }
    
    public void writeStringZ(String value) {
         stringBuffer = [0] * (range(0, 1024 + 1) + 1);
        int i = 0;
        
        if (len(value) > 1023) {
            throw new GeneralException.Create("Problem: String too long in KfBinaryFileExportSurface.writeStringZ.");
        }
        for (i = 1; i <= len(value); i++) {
            stringBuffer[i - 1] = value[i];
        }
        stringBuffer[len(value)] = chr(0);
        this.stream.WriteBuffer(stringBuffer, len(value) + 1);
        // maybe should align on four byte boundaries for efficiency of seeks later?
    }
    
    public void writeByte(byte value) {
        this.stream.WriteBuffer(value, 1);
    }
    
    public void writeWord(byte value) {
         swappedBytes = [0] * (range(0, 1 + 1) + 1);
        
        if (this.isLittleEndian()) {
            this.stream.WriteBuffer(value, 2);
        } else {
            swappedBytes[1] = value && 255;
            swappedBytes[0] = value >> 8;
            this.stream.WriteBuffer(swappedBytes, 2);
        }
    }
    
    public void writeDword(long value) {
         swappedBytes = [0] * (range(0, 3 + 1) + 1);
        
        if (this.isLittleEndian()) {
            this.stream.WriteBuffer(value, 4);
        } else {
            swappedBytes[3] = value && 255;
            swappedBytes[2] = (value >> 8) && 255;
            swappedBytes[1] = (value >> 16) && 255;
            swappedBytes[0] = (value >> 24) && 255;
            this.stream.WriteBuffer(swappedBytes, 4);
        }
    }
    
    public void writeFloat(float value) {
        SingleOverlay convert = new SingleOverlay();
         swappedBytes = [0] * (range(0, 3 + 1) + 1);
        
        if (this.isLittleEndian()) {
            this.stream.WriteBuffer(value, 4);
        } else {
            convert.numeric = value;
            swappedBytes[3] = convert.bytes[0];
            swappedBytes[2] = convert.bytes[1];
            swappedBytes[1] = convert.bytes[2];
            swappedBytes[0] = convert.bytes[3];
            this.stream.WriteBuffer(swappedBytes, 4);
        }
    }
    
    public boolean isLittleEndian() {
        result = false;
        // subclasses should override if they need to change this
        result = true;
        return result;
    }
    
}
class KfDrawingSurfaceFor3DS extends KfBinaryFileExportSurface {
    public String currentMaterialName;
    
    // ----------------------------------------------------------------------------- KfDrawingSurfaceFor3DS 
    public void createWithFileName(String aFileName) {
        // we assume that the file name has been already okayed
        super.createWithFileName(aFileName);
        this.currentMaterialName = "not defined";
    }
    
    public void destroy() {
        super.destroy();
    }
    
    public void startFile() {
        super.startFile();
        // 4d4dH 	M3DMAGIC; 3DS Magic Number (.3DS file)
        this.startChunk(0x4D4D);
        // 3d3dH 	MDATA; Mesh Data Magic Number (.3DS files sub of 4d4d)
        this.startChunk(0x3D3D);
    }
    
    public void endFile() {
        // 3d3dH 	MDATA; Mesh Data Magic Number (.3DS files sub of 4d4d)
        this.finishChunk(0x3D3D);
        // 4d4dH 	M3DMAGIC; 3DS Magic Number (.3DS file)
        this.finishChunk(0x4D4D);
    }
    
    public void startStemSegment(String aLongName, String aShortName, TColorRef color, float width, short index) {
        super.startStemSegment(aLongName, aShortName, color, width, index);
        this.currentMaterialName = this.currentPlantNameShort + "_" + aShortName;
        this.startVerticesAndTriangles();
    }
    
    public void endStemSegment() {
        this.endVerticesAndTriangles();
    }
    
    public void start3DObject(String aLongName, String aShortName, TColorRef color, short index) {
        super.start3DObject(aLongName, aShortName, color, index);
        this.currentMaterialName = this.currentPlantNameShort + "_" + aShortName;
    }
    
    public void startVerticesAndTriangles() {
        this.startMeshObject(this.currentGroupingString);
    }
    
    public void endVerticesAndTriangles() {
        int i = 0;
        
        // 4110H 	POINT_ARRAY short npoints; struct (float x, y, z;) points[npoints];
        this.startChunk(0x4110);
        this.writeWord(this.numPoints);
        for (i = 0; i <= this.numPoints - 1; i++) {
            this.writeFloat(this.pressedOrNot(this.scale * this.points[i].x, kX));
            this.writeFloat(this.pressedOrNot(this.scale * this.points[i].y, kY));
            this.writeFloat(this.pressedOrNot(this.scale * this.points[i].z, kZ));
        }
        this.finishChunk(0x4110);
        // 4120H 	FACE_ARRAY may be followed by smooth_group short nfaces;
        // struct (short vertex1, vertex2, vertex3; short flags;) facearray[nfaces];
        this.startChunk(0x4120);
        this.writeWord(this.numFaces);
        for (i = 0; i <= this.numFaces - 1; i++) {
            this.writeWord(this.faces[i].vertex1);
            this.writeWord(this.faces[i].vertex2);
            this.writeWord(this.faces[i].vertex3);
            this.writeWord(7);
        }
        if (this.options.writeColors) {
            // now set all faces to be of same material
            this.startChunk(0x4130);
            this.writeStringZ(this.currentMaterialName);
            this.writeWord(this.numFaces);
            for (i = 0; i <= this.numFaces - 1; i++) {
                this.writeWord(i);
            }
            this.finishChunk(0x4130);
        }
        this.finishChunk(0x4120);
        // close mesh
        this.finishMeshObject();
        // zero out
        this.numFaces = 0;
        this.numPoints = 0;
    }
    
    public void startMeshObject(String name) {
        // 4000H 	NAMED_OBJECT cstr name;
        this.startChunk(0x4000);
        this.writeStringZ(name);
        // 4100H 	N_TRI_OBJECT named triangle object followed by point_array, point_flag_array, mesh_matrix, face_array
        this.startChunk(0x4100);
    }
    
    public void finishMeshObject() {
        // 4100H 	N_TRI_OBJECT named triangle object followed by point_array, point_flag_array, mesh_matrix, face_array
        this.finishChunk(0x4100);
        // 4000H 	NAMED_OBJECT cstr name;
        this.finishChunk(0x4000);
    }
    
    public void pushChunkStart() {
        int position = 0;
        
        position = this.stream.Position;
        this.chunkStartStack.Add(UNRESOLVED.Pointer(position));
    }
    
    public void popChunkStartAndFixupChunkSize() {
        int chunkSize = 0;
        int startSize = 0;
        int totalSize = 0;
        int lastIndex = 0;
        
        totalSize = this.stream.Size;
        lastIndex = this.chunkStartStack.Count - 1;
        if (lastIndex < 0) {
            // should check if -1
            throw new GeneralException.Create("Problem with stack indexing for 3DS writing in method KfDrawingSurfaceFor3DS.popChunkStartAndFixupChunkSize.");
        }
        startSize = this.chunkStartStack.Items[lastIndex];
        this.chunkStartStack.Delete(lastIndex);
        chunkSize = totalSize - startSize;
        // skip two to avoid overwriting chunk type
        this.stream.Seek(startSize + 2, delphi_compatability.soFromBeginning);
        this.writeDword(chunkSize);
        this.stream.Seek(0, delphi_compatability.soFromEnd);
    }
    
    public void startChunk(int chunkID) {
        this.pushChunkStart();
        this.writeWord(chunkID);
        // write placeholder dword that will be patched later
        this.writeDword(0);
    }
    
    public void finishChunk(int chunkType) {
        this.popChunkStartAndFixupChunkSize();
    }
    
    public void writeMaterialDescription(short index, TColorRef aColor) {
        if (!this.options.writeColors) {
            return;
        }
        if (index < 0) {
            this.writeMaterialColorChunk(this.currentPlantNameShort + "_rem", UNRESOLVED.getRValue(aColor), UNRESOLVED.getGValue(aColor), UNRESOLVED.getBValue(aColor));
        } else {
            this.writeMaterialColorChunk(this.currentPlantNameShort + "_" + shortNameForDXFPartType(index), UNRESOLVED.getRValue(aColor), UNRESOLVED.getGValue(aColor), UNRESOLVED.getBValue(aColor));
        }
    }
    
    public void writeColorChunk(byte r, byte g, byte b) {
        this.startChunk(0x0011);
        this.writeByte(r);
        this.writeByte(g);
        this.writeByte(b);
        this.finishChunk(0x0011);
    }
    
    public void writeMaterialColorChunk(String materialName, byte r, byte g, byte b) {
        // Material editor chunk
        this.startChunk(0xAFFF);
        // Material name
        this.startChunk(0xA000);
        this.writeStringZ(materialName);
        this.finishChunk(0xA000);
        // Material ambient color
        this.startChunk(0xA010);
        this.writeColorChunk(r, g, b);
        this.finishChunk(0xA010);
        // Material diffuse color
        this.startChunk(0xA020);
        this.writeColorChunk(r, g, b);
        this.finishChunk(0xA020);
        this.finishChunk(0xAFFF);
    }
    
    public void writeRegistrationReminder(KFPoint3D p1, KFPoint3D p2, KFPoint3D p3, KFPoint3D p4) {
        short numPointsAtStart = 0;
        
        this.currentGroupingString = this.currentPlantNameShort + "_rem";
        this.currentMaterialName = this.currentPlantNameShort + "_rem";
        numPointsAtStart = this.numPoints;
        this.startVerticesAndTriangles();
        this.addPoint(p1);
        this.addPoint(p2);
        this.addPoint(p3);
        this.addPoint(p4);
        this.addTriangle(numPointsAtStart, numPointsAtStart + 1, numPointsAtStart + 3);
        this.addTriangle(numPointsAtStart + 1, numPointsAtStart + 2, numPointsAtStart + 3);
        this.endVerticesAndTriangles();
    }
    
}
class KfDrawingSurfaceForLWO extends KfBinaryFileExportSurface {
    public short currentSurfaceID;
    public short numSurfacesStored;
    public  surfaceColors;
    public  surfaceNames;
    
    // ----------------------------------------------------------------------------- KfDrawingSurfaceForLWO 
    public void endFile() {
        long i = 0;
        
        // start file
        this.startChunk("FORM");
        this.writeTagOfFourCharacters("LWOB");
        // points
        this.startChunk("PNTS");
        for (i = 0; i <= this.numPoints - 1; i++) {
            this.writeFloat(this.pressedOrNot(this.scale * this.points[i].x, kX));
            this.writeFloat(this.pressedOrNot(this.scale * this.points[i].y, kY));
            this.writeFloat(this.pressedOrNot(this.scale * this.points[i].z, kZ));
        }
        this.finishChunk();
        if (this.options.writeColors) {
            // surfaces
            this.startChunk("SRFS");
            for (i = 1; i <= this.numSurfacesStored; i++) {
                this.writeStringZ(this.surfaceNames[i]);
                if (odd(len(this.surfaceNames[i]) + 1)) {
                    //1 is for terminating zero
                    this.writeByte(0);
                }
            }
            this.finishChunk();
        } else {
            this.startChunk("SRFS");
            // if you change this to an odd # considering the end zero you must pad it
            this.writeStringZ("default");
            this.finishChunk();
        }
        // faces
        this.startChunk("POLS");
        for (i = 0; i <= this.numFaces - 1; i++) {
            this.writeWord(3);
            this.writeWord(this.faces[i].vertex1);
            this.writeWord(this.faces[i].vertex2);
            this.writeWord(this.faces[i].vertex3);
            if (this.options.writeColors) {
                this.writeWord(this.faces[i].surfaceID);
            } else {
                this.writeWord(1);
            }
        }
        this.finishChunk();
        if (this.options.writeColors) {
            for (i = 1; i <= this.numSurfacesStored; i++) {
                // surfaces again
                this.startChunk("SURF");
                this.writeStringZ(this.surfaceNames[i]);
                if (odd(len(this.surfaceNames[i]) + 1)) {
                    //terminating zero
                    this.writeByte(0);
                }
                this.writeTagOfFourCharacters("COLR");
                this.writeWord(4);
                this.writeByte(UNRESOLVED.getRValue(this.surfaceColors[i]));
                this.writeByte(UNRESOLVED.getGValue(this.surfaceColors[i]));
                this.writeByte(UNRESOLVED.getBValue(this.surfaceColors[i]));
                this.writeByte(0);
                this.writeTagOfFourCharacters("FLAG");
                this.writeWord(2);
                // double-sided flag
                this.writeWord(0x0100);
                this.writeTagOfFourCharacters("DIFF");
                this.writeWord(2);
                this.writeWord(256);
                this.finishChunk();
            }
        } else {
            this.startChunk("SURF");
            // if you change this to an odd # considering the end zero you must pad it
            this.writeStringZ("default");
            this.writeTagOfFourCharacters("COLR");
            this.writeWord(4);
            this.writeByte(200);
            this.writeByte(200);
            this.writeByte(200);
            this.writeByte(0);
            this.finishChunk();
        }
        // finishes 'FORM' chunk
        this.finishChunk();
        this.numFaces = 0;
        this.numPoints = 0;
    }
    
    public boolean isLittleEndian() {
        result = false;
        result = false;
        return result;
    }
    
    public void startStemSegment(String aLongName, String aShortName, TColorRef color, float width, short index) {
        super.startStemSegment(aLongName, aShortName, color, width, index);
        //currentPlantNameShort + '_' + aShortName
        this.currentSurfaceID = this.lookUpSurfaceIDForName(this.currentGroupingString, color);
    }
    
    public short lookUpSurfaceIDForName(String aName, TColorRef color) {
        result = 0;
        long i = 0;
        
        for (i = 1; i <= this.numSurfacesStored; i++) {
            if (this.surfaceNames[i] == aName) {
                result = i;
                return result;
            }
        }
        if (this.numSurfacesStored < kMaxStoredMaterials) {
            this.numSurfacesStored += 1;
            this.surfaceNames[this.numSurfacesStored] = aName;
            this.surfaceColors[this.numSurfacesStored] = color;
        }
        result = this.numSurfacesStored;
        return result;
    }
    
    public void drawPipeFaces( startPoints,  endPoints, short faces, short segmentNumber) {
        long i = 0;
        long firstPtIndex = 0;
        
        firstPtIndex = this.numPoints;
        for (i = 0; i <= faces - 1; i++) {
            this.addPoint(startPoints[i]);
        }
        for (i = 0; i <= faces - 1; i++) {
            this.addPoint(endPoints[i]);
        }
        for (i = 0; i <= faces - 1; i++) {
            this.addTriangle(firstPtIndex + i, firstPtIndex + i + faces, firstPtIndex + (i + 1) % faces);
            this.addTriangle(firstPtIndex + (i + 1) % faces, firstPtIndex + i + faces, firstPtIndex + (i + 1) % faces + faces);
        }
    }
    
    public void start3DObject(String aLongName, String aShortName, TColorRef color, short index) {
        super.start3DObject(aLongName, aShortName, color, index);
        //currentPlantNameShort + '_' + aShortName
        this.currentSurfaceID = this.lookUpSurfaceIDForName(this.currentGroupingString, color);
    }
    
    public void addTriangle(int a, int b, int c) {
        this.addTriangleWithSurface(a, b, c, this.currentSurfaceID);
    }
    
    public void addTriangleWithSurface(int a, int b, int c, int surfaceID) {
        if (this.numFaces >= kMax3DFaces) {
            throw new GeneralException.Create("Problem: Too many faces in LWO; in method KfDrawingSurfaceFor3DS.addTriangle.");
        }
        this.faces[this.numFaces].vertex1 = a;
        this.faces[this.numFaces].vertex2 = b;
        this.faces[this.numFaces].vertex3 = c;
        this.faces[this.numFaces].surfaceID = this.currentSurfaceID;
        this.numFaces += 1;
    }
    
    public void pushChunkStart() {
        int position = 0;
        
        position = this.stream.Position;
        this.chunkStartStack.Add(UNRESOLVED.Pointer(position));
    }
    
    public void popChunkStartAndFixupChunkSize() {
        int chunkSize = 0;
        int startSize = 0;
        int totalSize = 0;
        int lastIndex = 0;
        
        totalSize = this.stream.Size;
        lastIndex = this.chunkStartStack.Count - 1;
        if (lastIndex < 0) {
            // should check if -1
            throw new GeneralException.Create("Problem with stack indexing for 3DS writing in method KfDrawingSurfaceFor3DS.popChunkStartAndFixupChunkSize.");
        }
        startSize = this.chunkStartStack.Items[lastIndex];
        this.chunkStartStack.Delete(lastIndex);
        chunkSize = totalSize - startSize;
        // skip back four
        this.stream.Seek(startSize - 4, delphi_compatability.soFromBeginning);
        // lwo chunk sizes do not include the header
        this.writeDword(chunkSize);
        this.stream.Seek(0, delphi_compatability.soFromEnd);
    }
    
    public void startChunk(String chunkName) {
        this.writeTagOfFourCharacters(chunkName);
        // write placeholder dword that will be patched later
        this.writeDword(0);
        this.pushChunkStart();
    }
    
    public void finishChunk() {
        this.popChunkStartAndFixupChunkSize();
    }
    
    public void writeTagOfFourCharacters(String aString) {
        this.writeByte(aString[1]);
        this.writeByte(aString[2]);
        this.writeByte(aString[3]);
        this.writeByte(aString[4]);
    }
    
    public void writeRegistrationReminder(KFPoint3D p1, KFPoint3D p2, KFPoint3D p3, KFPoint3D p4) {
        short numPointsAtStart = 0;
        
        this.currentSurfaceID = this.lookUpSurfaceIDForName(this.currentPlantNameShort + "_rem", UNRESOLVED.rgb(100, 100, 100));
        numPointsAtStart = this.numPoints;
        this.addPoint(p1);
        this.addPoint(p2);
        this.addPoint(p3);
        this.addPoint(p4);
        this.addTriangle(numPointsAtStart, numPointsAtStart + 1, numPointsAtStart + 3);
        this.addTriangle(numPointsAtStart + 1, numPointsAtStart + 2, numPointsAtStart + 3);
    }
    
}
// VRML 1.0 spec
//
//DEF plantName Group {
//  DEF nestingName Group {
//    DEF partName Group {
//      Material { diffuseColor [ 0.19 0.39 0.19 ] }
//	    ShapeHints {
//	      vertexOrdering	COUNTERCLOCKWISE
//	      shapeType	SOLID
//	      creaseAngle	3.14159
//	      } # ShapeHints
//      Coordinate3 {
//          point [
//            49.64	304.6	117.55	,
//            56.71	312.51	123.85	,
//            ] # point
//          } # Coordinate3
//      IndexedFaceSet {
//        coordIndex [
//          0	, 1	, 2	, -1	,
//          1	, 3	, 2	, -1	,
//          ] # coordIndex
//        } # IndexedFaceSet
//      } # Group partName
//    } # Group nestingName
//  } # Group plantName
//
// VRML 2.0 spec
//
//DEF plantName Group {
//  children [
//  DEF nestingName Group {
//    children [
//      DEF partName Shape {
//        appearance Appearance { material Material { diffuseColor  0.99 0  0.5 } }
//        geometry IndexedFaceSet {
//          coord Coordinate {
//            point [
//              49.64	304.6	117.55	,
//              56.71	312.51	123.85	,
//              ] # point
//            } # Coordinate
//          ccw TRUE
//          colorPerVertex FALSE
//          coordIndex [
//            0	, 1	, 2	, -1	,
//            1	, 3	, 2	, -1	,
//            ] # coordIndex
//          creaseAngle 0.5
//          normalPerVertex TRUE
//          solid FALSE
//          } #  IndexedFaceSet
//        } # Shape
//      ] # children nestingName
//      } # Group nestingName
//    ] # children plantName
//  } # Group plantName
//
