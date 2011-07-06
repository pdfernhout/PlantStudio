# unit U3dexport

from conversion_common import *
import umath
import udomain
import u3dsupport
import udrawingsurface
import utdo
import usupport
import delphi_compatability

# const
kExportPartMeristem = 0
kExportPartInternode = 1
kExportPartSeedlingLeaf = 2
kExportPartLeaf = 3
kExportPartFirstPetiole = 4
kExportPartPetiole = 5
kExportPartLeafStipule = 6
kExportPartInflorescenceStalkFemale = 7
kExportPartInflorescenceInternodeFemale = 8
kExportPartInflorescenceBractFemale = 9
kExportPartInflorescenceStalkMale = 10
kExportPartInflorescenceInternodeMale = 11
kExportPartInflorescenceBractMale = 12
kExportPartPedicelFemale = 13
kExportPartFlowerBudFemale = 14
kExportPartStyleFemale = 15
kExportPartStigmaFemale = 16
kExportPartFilamentFemale = 17
kExportPartAntherFemale = 18
kExportPartFirstPetalsFemale = 19
kExportPartSecondPetalsFemale = 20
kExportPartThirdPetalsFemale = 21
kExportPartFourthPetalsFemale = 22
kExportPartFifthPetalsFemale = 23
kExportPartSepalsFemale = 24
kExportPartPedicelMale = 25
kExportPartFlowerBudMale = 26
kExportPartFilamentMale = 27
kExportPartAntherMale = 28
kExportPartFirstPetalsMale = 29
kExportPartSepalsMale = 30
kExportPartUnripeFruit = 31
kExportPartRipeFruit = 32
kExportPartRootTop = 33
kExportPartLast = 33
kLastDxfColorIndex = 10
dxfColors = [delphi_compatability.clRed, delphi_compatability.clYellow, delphi_compatability.clLime, delphi_compatability.clAqua, delphi_compatability.clBlue, delphi_compatability.clPurple, delphi_compatability.clBlack, delphi_compatability.clOlive, delphi_compatability.clFuchsia, delphi_compatability.clTeal, delphi_compatability.clGray, ]
kColorDXFFromPlantPartType = 0
kColorDXFFromRGB = 1
kColorDXFFromOneColor = 3
kNestingTypeInflorescence = 0
kNestingTypeLeafAndPetiole = 1
kNestingTypeCompoundLeaf = 2
kNestingTypePedicelAndFlowerFruit = 3
kNestingTypeFloralLayers = 4
kMaxPOVPlants = 1000
kMaxStoredMaterials = 1000
kVRMLVersionOne = 0
kVRMLVersionTwo = 1
kScreen = 0
kDXF = 1
kPOV = 2
k3DS = 3
kOBJ = 4
kVRML = 5
kLWO = 6
k3DExportTypeLast = 6
kLayerOutputAllTogether = 0
kLayerOutputByTypeOfPlantPart = 1
kLayerOutputByPlantPart = 2
kWriteColor = true
kDontWriteColor = false
kMax3DPoints = 65536
kMax3DFaces = 65536
kX = 0
kY = 1
kZ = 2

# export part types
# meristem
# internode
# leaf
# no stipule on first leaves
# inflorescence female
# inflorescence male
# flower female
# flower male
# fruit
# root top
# DXF
# POV
# can't imagine anyone would save more than that
# 3DS
# OBJ, LWO
# VRML
# general
# record
class Vertex:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

# record
class Triangle:
    def __init__(self):
        self.vertex1 = 0
        self.vertex2 = 0
        self.vertex3 = 0
        self.surfaceID = 0

# generic
# record
class FileExport3DOptionsStructure:
    def __init__(self):
        self.exportType = 0
        self.layeringOption = 0
        self.stemCylinderFaces = 0
        self.translatePlantsToWindowPositions = false
        self.lengthOfShortName = 0
        self.writePlantNumberInFrontOfName = false
        self.writeColors = false
        self.overallScalingFactor_pct = 0
        self.fileSize = 0.0
        self.xRotationBeforeDraw = 0
        self.pressPlants = false
        self.directionToPressPlants = 0
        self.makeTrianglesDoubleSided = false
        self.dxf_whereToGetColors = 0
        self.dxf_wholePlantColorIndex = 0
        self.dxf_plantPartColorIndexes = [0] * (range(0, kExportPartLast + 1) + 1)
        self.pov_minLineLengthToWrite = 0.0
        self.pov_minTdoScaleToWrite = 0.0
        self.pov_commentOutUnionAtEnd = false
        self.nest_Inflorescence = false
        self.nest_LeafAndPetiole = false
        self.nest_CompoundLeaf = false
        self.nest_PedicelAndFlowerFruit = false
        self.nest_FloralLayers = false
        self.vrml_version = 0

# const
kNumVRMLPointsPerLine = 4

# record
class SingleOverlay:
    def __init__(self):
        pass

# ------------------------------------------------------------------------------------------ index functions 
def fileTypeFor3DExportType(outputType):
    result = 0
    if outputType == kDXF:
        result = usupport.kFileTypeDXF
    elif outputType == kPOV:
        result = usupport.kFileTypeINC
    elif outputType == k3DS:
        result = usupport.kFileType3DS
    elif outputType == kOBJ:
        result = usupport.kFileTypeOBJ
    elif outputType == kVRML:
        result = usupport.kFileTypeVRML
    elif outputType == kLWO:
        result = usupport.kFileTypeLWO
    else :
        raise GeneralException.create("Problem: Invalid export type in TMainForm.fileTypeFor3DExportType.")
    return result

def nameFor3DExportType(anOutputType):
    result = ""
    if anOutputType == kDXF:
        result = "DXF"
    elif anOutputType == kPOV:
        result = "POV"
    elif anOutputType == k3DS:
        result = "3DS"
    elif anOutputType == kOBJ:
        result = "OBJ"
    elif anOutputType == kVRML:
        result = "VRML"
    elif anOutputType == kLWO:
        result = "LWO"
    else :
        raise GeneralException.create("Problem: Invalid type in PdDomain.sectionNumberFor3DExportType.")
    return result

def longNameForDXFPartType(index):
    result = ""
    longName = ""
    shortName = ""
    
    longName, shortName = getInfoForDXFPartType(index, longName, shortName)
    result = longName
    return result

def shortNameForDXFPartType(index):
    result = ""
    longName = ""
    shortName = ""
    
    longName, shortName = getInfoForDXFPartType(index, longName, shortName)
    result = shortName
    return result

def getInfoForDXFPartType(index, longName, shortName):
    if index == kExportPartMeristem:
        longName = "Meristem"
        shortName = "Mrstm"
    elif index == kExportPartInternode:
        longName = "Internode"
        shortName = "Intrnd"
    elif index == kExportPartSeedlingLeaf:
        longName = "Seedling leaf"
        shortName = "1stLeaf"
    elif index == kExportPartLeaf:
        longName = "Leaf"
        shortName = "Leaf"
    elif index == kExportPartFirstPetiole:
        longName = "Seedling petiole"
        shortName = "1stPetiole"
    elif index == kExportPartPetiole:
        longName = "Petiole"
        shortName = "Petiole"
    elif index == kExportPartLeafStipule:
        longName = "Leaf stipule"
        shortName = "Stipule"
    elif index == kExportPartInflorescenceStalkFemale:
        longName = "Primary inflorescence stalk (peduncle)"
        shortName = "1Pdncle"
    elif index == kExportPartInflorescenceInternodeFemale:
        longName = "Primary inflorescence internode"
        shortName = "1InfInt"
    elif index == kExportPartInflorescenceBractFemale:
        longName = "Primary inflorescence bract"
        shortName = "1Bract"
    elif index == kExportPartInflorescenceStalkMale:
        longName = "Secondary inflorescence stalk (peduncle)"
        shortName = "2Pdncle"
    elif index == kExportPartInflorescenceInternodeMale:
        longName = "Secondary inflorescence internode"
        shortName = "2InfInt"
    elif index == kExportPartInflorescenceBractMale:
        longName = "Secondary inflorescence bract"
        shortName = "2Bract"
    elif index == kExportPartPedicelFemale:
        longName = "Primary flower stalk"
        shortName = "1Pdcel"
    elif index == kExportPartFlowerBudFemale:
        longName = "Primary flower bud"
        shortName = "1Bud"
    elif index == kExportPartStyleFemale:
        longName = "Flower style"
        shortName = "Style"
    elif index == kExportPartStigmaFemale:
        longName = "Flower stigma"
        shortName = "Stigma"
    elif index == kExportPartFilamentFemale:
        longName = "Primary flower filament"
        shortName = "1Flmnt"
    elif index == kExportPartAntherFemale:
        longName = "Primary flower anther"
        shortName = "1Anther"
    elif index == kExportPartFirstPetalsFemale:
        longName = "Primary flower petal, first row"
        shortName = "1Petal1"
    elif index == kExportPartSecondPetalsFemale:
        longName = "Flower petal, second row"
        shortName = "1Petal2"
    elif index == kExportPartThirdPetalsFemale:
        longName = "Flower petal, third row"
        shortName = "1Petal3"
    elif index == kExportPartFourthPetalsFemale:
        longName = "Flower petal, fourth row"
        shortName = "1Petal4"
    elif index == kExportPartFifthPetalsFemale:
        longName = "Flower petal, fifth row"
        shortName = "1Petal5"
    elif index == kExportPartSepalsFemale:
        longName = "Primary flower sepal"
        shortName = "1Sepal"
    elif index == kExportPartPedicelMale:
        longName = "Secondary flower stalk"
        shortName = "2Pdcel"
    elif index == kExportPartFlowerBudMale:
        longName = "Secondary flower bud"
        shortName = "2Bud"
    elif index == kExportPartFilamentMale:
        longName = "Secondary flower filament"
        shortName = "2Flmnt"
    elif index == kExportPartAntherMale:
        longName = "Secondary flower anther"
        shortName = "2Anther"
    elif index == kExportPartFirstPetalsMale:
        longName = "Secondary flower petal"
        shortName = "2Petal1"
    elif index == kExportPartSepalsMale:
        longName = "Secondary flower sepal"
        shortName = "2Sepal"
    elif index == kExportPartUnripeFruit:
        longName = "Unripe fruit"
        shortName = "FruitU"
    elif index == kExportPartRipeFruit:
        longName = "Ripe fruit"
        shortName = "FruitR"
    elif index == kExportPartRootTop:
        longName = "Root top"
        shortName = "Root"
    else :
        raise GeneralException.create("Problem: Invalid part type in method getInfoForDXFPartType.")
    return longName, shortName

# don't save in settings file
# to deal with quirks in other programs
# specific (keep in generic structure so one window can handle all of these)
class KfFileExportSurface(KfDrawingSurface):
    def __init__(self):
        self.fileName = ""
        self.scale = 0.0
        self.options = FileExport3DOptionsStructure()
        self.currentPlantNameLong = ""
        self.currentPlantNameShort = ""
        self.currentPlantIsTranslated = false
        self.currentPlantTranslateX = 0.0
        self.currentPlantTranslateY = 0.0
        self.currentPlantIndex = 0
        self.currentGroupingString = ""
        self.currentColor = TColorRef()
        self.plantPartCounts = [0] * (range(0, kExportPartLast + 1) + 1)
        self.numPoints = 0
        self.points = [0] * (range(0, kMax3DPoints + 1) + 1)
        self.numFaces = 0
        self.faces = [0] * (range(0, kMax3DFaces + 1) + 1)
    
    # ----------------------------------------------------------------------------- KfFileExportSurface 
    def createWithFileName(self, aFileName):
        KfDrawingSurface.create(self)
        self.fileName = aFileName
        self.options = udomain.domain.exportOptionsFor3D[self.outputType()]
        self.scale = self.options.overallScalingFactor_pct / 100.0
        return self
    
    def destroy(self):
        pass
        # nothing yet
    
    def startFile(self):
        raise GeneralException.create("subclasses must override")
    
    def endFile(self):
        raise GeneralException.create("subclasses must override")
    
    def startPlant(self, aLongName, aPlantIndex):
        self.currentPlantIndex = aPlantIndex
        self.currentPlantNameLong = aLongName
        self.currentPlantNameShort = self.generateShortName()
    
    def endPlant(self):
        pass
        # subclasses can override
    
    def writeRegistrationReminder(self, p1, p2, p3, p4):
        raise GeneralException.create("subclasses must override")
    
    def startNestedGroupOfPlantParts(self, groupName, shortName, nestingType):
        pass
        # subclasses can override
    
    def endNestedGroupOfPlantParts(self, nestingType):
        pass
        # subclasses can override
    
    def startPlantPart(self, aLongName, aShortName):
        pass
        # subclasses can override
    
    def endPlantPart(self):
        pass
        # subclasses can override
    
    def startStemSegment(self, aLongName, aShortName, color, width, index):
        self.setUpGroupingStringForStemSegmentOr3DObject(aShortName, index)
    
    def start3DObject(self, aLongName, aShortName, color, index):
        self.setUpGroupingStringForStemSegmentOr3DObject(aShortName, index)
    
    def startVerticesAndTriangles(self):
        pass
        # subclasses can override
    
    def endVerticesAndTriangles(self):
        pass
        # subclasses can override
    
    def addPoint(self, point):
        if self.numPoints >= kMax3DPoints:
            raise GeneralException.Create("Problem: Too many points in 3D export.")
        self.points[self.numPoints].x = self.pressedOrNot(self.scale * Point.x, kX)
        self.points[self.numPoints].y = self.pressedOrNot(self.scale * Point.y, kY)
        self.points[self.numPoints].z = self.pressedOrNot(self.scale * Point.z, kZ)
        self.numPoints += 1
    
    def pressedOrNot(self, value, dimension):
        result = 0.0
        if (self.options.pressPlants) and (self.options.directionToPressPlants == dimension):
            result = 0
        else:
            result = value
        return result
    
    def addTriangle(self, a, b, c):
        if self.numFaces >= kMax3DFaces:
            raise GeneralException.Create("Problem: Too many faces in 3D export.")
        self.faces[self.numFaces].vertex1 = a
        self.faces[self.numFaces].vertex2 = b
        self.faces[self.numFaces].vertex3 = c
        self.numFaces += 1
    
    def end3DObject(self):
        pass
        # subclasses can override
    
    def setUpGroupingStringForStemSegmentOr3DObject(self, aShortName, index):
        if self.options.layeringOption == kLayerOutputAllTogether:
            self.currentGroupingString = self.currentPlantNameShort
        elif self.options.layeringOption == kLayerOutputByTypeOfPlantPart:
            self.currentGroupingString = self.currentPlantNameShort + "_" + aShortName
        elif self.options.layeringOption == kLayerOutputByPlantPart:
            self.plantPartCounts[index] += 1
            self.currentGroupingString = self.currentPlantNameShort + "_" + IntToStr(self.plantPartCounts[index]) + "_" + aShortName
    
    def endStemSegment(self):
        pass
        # subclasses can override
    
    def drawPipeFaces(self, startPoints, endPoints, faces, segmentNumber):
        i = 0L
        disp = 0L
        
        # subclasses can override - this works for some
        disp = segmentNumber * faces * 2
        for i in range(0, faces):
            self.addPoint(startPoints[i])
        for i in range(0, faces):
            self.addPoint(endPoints[i])
        for i in range(0, faces):
            self.addTriangle(disp + i, disp + i + faces, disp + (i + 1) % faces)
            self.addTriangle(disp + (i + 1) % faces, disp + i + faces, disp + (i + 1) % faces + faces)
    
    def setTranslationForCurrentPlant(self, isTranslated, aTranslateX, aTranslateY):
        self.currentPlantIsTranslated = isTranslated
        self.currentPlantTranslateX = aTranslateX
        self.currentPlantTranslateY = aTranslateY
    
    def outputType(self):
        result = 0
        result = -1
        if (self.__class__ is KfDrawingSurfaceForDXF):
            result = kDXF
        elif (self.__class__ is KfDrawingSurfaceForPOV):
            result = kPOV
        elif (self.__class__ is KfDrawingSurfaceFor3DS):
            result = k3DS
        elif (self.__class__ is KfDrawingSurfaceForOBJ):
            result = kOBJ
        elif (self.__class__ is KfDrawingSurfaceForVRML):
            result = kVRML
        elif (self.__class__ is KfDrawingSurfaceForLWO):
            result = kLWO
        return result
    
    def generateShortName(self):
        result = ""
        shortNameLength = 0
        i = 0
        
        result = ""
        if len(self.currentPlantNameLong) <= 0:
            return result
        shortNameLength = umath.intMin(self.options.lengthOfShortName, len(self.currentPlantNameLong))
        for i in range(1, shortNameLength + 1):
            if self.currentPlantNameLong[i] != " ":
                result = result + UNRESOLVED.copy(self.currentPlantNameLong, i, 1)
        if self.options.writePlantNumberInFrontOfName:
            result = IntToStr(self.currentPlantIndex + 1) + result
        return result
    
class KfTextFileExportSurface(KfFileExportSurface):
    def __init__(self):
        self.outputFile = TextFile()
    
    # ----------------------------------------------------------------------------- KfTextFileExportSurface 
    def createWithFileName(self, aFileName):
        KfFileExportSurface.createWithFileName(self, aFileName)
        # we assume that the file name has been already okayed by whoever created us
        AssignFile(self.outputFile, self.fileName)
        return self
    
    def destroy(self):
        pass
        # nothing yet
    
    def startFile(self):
        Rewrite(self.outputFile)
    
    def endFile(self):
        CloseFile(self.outputFile)
    
class KfDrawingSurfaceForDXF(KfTextFileExportSurface):
    def __init__(self):
        self.currentColorIndex = 0
    
    # ----------------------------------------------------------------------------- KfDrawingSurfaceForDXF 
    def startFile(self):
        KfTextFileExportSurface.startFile(self)
        writeln(self.outputFile, "999")
        writeln(self.outputFile, "DXF created by PlantStudio http://www.kurtz-fernhout.com")
        # v2.0 moved ENTITY section from starting and ending each plant to entire file - may fix bug
        # with programs only recognizing one plant in a file
        writeln(self.outputFile, "0")
        writeln(self.outputFile, "SECTION")
        writeln(self.outputFile, "2")
        writeln(self.outputFile, "ENTITIES")
    
    def endFile(self):
        # v2.0 moved ENTITY section from starting and ending each plant to entire file - may fix bug
        # with programs only recognizing one plant in a file
        writeln(self.outputFile, "0")
        writeln(self.outputFile, "ENDSEC")
        writeln(self.outputFile, "0")
        writeln(self.outputFile, "EOF")
        KfTextFileExportSurface.endFile(self)
    
    def startPlant(self, aLongName, aPlantIndex):
        KfTextFileExportSurface.startPlant(self, aLongName, aPlantIndex)
        if self.options.layeringOption == kLayerOutputAllTogether:
            self.currentGroupingString = UNRESOLVED.copy(self.currentPlantNameLong, 1, 16)
        if self.options.dxf_whereToGetColors == kColorDXFFromOneColor:
            self.currentColorIndex = self.options.dxf_wholePlantColorIndex
    
    def startStemSegment(self, aLongName, aShortName, color, width, index):
        KfTextFileExportSurface.startStemSegment(self, aLongName, aShortName, color, width, index)
        if self.options.dxf_whereToGetColors == kColorDXFFromPlantPartType:
            self.currentColorIndex = self.options.dxf_plantPartColorIndexes[index]
        elif self.options.dxf_whereToGetColors == kColorDXFFromRGB:
            self.currentColor = color
    
    def start3DObject(self, aLongName, aShortName, color, index):
        KfTextFileExportSurface.start3DObject(self, aLongName, aShortName, color, index)
        if self.options.dxf_whereToGetColors == kColorDXFFromPlantPartType:
            self.currentColorIndex = self.options.dxf_plantPartColorIndexes[index]
        elif self.options.dxf_whereToGetColors == kColorDXFFromRGB:
            self.currentColor = color
    
    def drawPipeFaces(self, startPoints, endPoints, faces, segmentNumber):
        i = 0
        
        for i in range(0, faces):
            # for this don't have to worry about segment number, we are not adding points and triangles
            self.draw3DFace(startPoints[i], endPoints[i], endPoints[(i + 1) % faces], startPoints[(i + 1) % faces])
    
    def draw3DFace(self, point1, point2, point3, point4):
        writeln(self.outputFile, "0")
        writeln(self.outputFile, "3DFACE")
        writeln(self.outputFile, "8")
        writeln(self.outputFile, self.currentGroupingString)
        if self.options.writeColors:
            if self.options.dxf_whereToGetColors == kColorDXFFromRGB:
                writeln(self.outputFile, "62")
                writeln(self.outputFile, IntToStr(self.currentColor))
            else:
                writeln(self.outputFile, "62")
                writeln(self.outputFile, IntToStr(self.currentColorIndex + 1))
        writeln(self.outputFile, "10")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * point1.x, kX)))
        writeln(self.outputFile, "20")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * -point1.y, kY)))
        writeln(self.outputFile, "30")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * point1.z, kZ)))
        writeln(self.outputFile, "11")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * point2.x, kX)))
        writeln(self.outputFile, "21")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * -point2.y, kY)))
        writeln(self.outputFile, "31")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * point2.z, kZ)))
        writeln(self.outputFile, "12")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * point3.x, kX)))
        writeln(self.outputFile, "22")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * -point3.y, kY)))
        writeln(self.outputFile, "32")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * point3.z, kZ)))
        writeln(self.outputFile, "13")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * point4.x, kX)))
        writeln(self.outputFile, "23")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * -point4.y, kY)))
        writeln(self.outputFile, "33")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * point4.z, kZ)))
    
    def basicDrawLineFromTo(self, startPoint, endPoint):
        self.draw3DFace(startPoint, startPoint, endPoint, endPoint)
    
    def basicDrawTriangle(self, triangle):
        self.draw3DFace(triangle.points[0], triangle.points[1], triangle.points[2], triangle.points[2])
    
    def writeRegistrationReminder(self, p1, p2, p3, p4):
        self.currentGroupingString = self.currentPlantNameShort + "_rem"
        # adds one; kLastDxfColorIndex is gray
        self.currentColorIndex = kLastDxfColorIndex - 1
        self.draw3DFace(p1, p2, p3, p3)
        self.draw3DFace(p1, p3, p4, p4)
    
class KfDrawingSurfaceForPOV(KfTextFileExportSurface):
    def __init__(self):
        self.currentComment = ""
        self.currentWidth = 0.0
        self.currentIndentLevel = 0
        self.currentRotateString = ""
        self.numPlantsDrawn = 0
        self.plantNames = [0] * (range(0, kMaxPOVPlants + 1) + 1)
    
    # ----------------------------------------------------------------------------- KfDrawingSurfaceForPOV 
    def startFile(self):
        KfTextFileExportSurface.startFile(self)
        writeln(self.outputFile, "// INC file for Persistence of Vision (POV) raytracer")
        writeln(self.outputFile, "// created by PlantStudio http://www.kurtz-fernhout.com")
        writeln(self.outputFile)
    
    def endFile(self):
        i = 0
        
        writeln(self.outputFile)
        if self.options.pov_commentOutUnionAtEnd:
            writeln(self.outputFile, "/* ")
        writeln(self.outputFile, "#declare allPlants_" + usupport.replacePunctuationWithUnderscores(usupport.stringUpTo(ExtractFileName(self.fileName), ".")) + " = union {")
        for i in range(0, self.numPlantsDrawn):
            writeln(self.outputFile, chr(9) + "object { " + self.plantNames[i] + " }")
        writeln(self.outputFile, chr(9) + "}")
        if self.options.pov_commentOutUnionAtEnd:
            writeln(self.outputFile, "*/ ")
        KfTextFileExportSurface.endFile(self)
    
    def startPlant(self, aLongName, aPlantIndex):
        # in POV you can't have spaces in names
        aLongName = usupport.replacePunctuationWithUnderscores(aLongName)
        KfTextFileExportSurface.startPlant(self, aLongName, aPlantIndex)
        writeln(self.outputFile, "#declare " + self.currentPlantNameLong + " = union {")
        self.currentIndentLevel = 0
        self.indent()
        self.plantNames[self.numPlantsDrawn] = self.currentPlantNameLong
        self.numPlantsDrawn += 1
    
    def endPlant(self):
        if (self.currentPlantIsTranslated) and (self.options.translatePlantsToWindowPositions):
            writeln(self.outputFile, "translate <" + usupport.valueString(self.currentPlantTranslateX) + ", " + usupport.valueString(self.currentPlantTranslateY) + ", 0>")
        if not self.options.writeColors:
            write(self.outputFile, "pigment { color rgb <0.8, 0.8, 0.8> }")
        writeln(self.outputFile, "} // end " + self.currentPlantNameLong)
        writeln(self.outputFile)
        self.currentIndentLevel = 0
        KfTextFileExportSurface.endPlant(self)
    
    def startNestedGroupOfPlantParts(self, groupName, shortName, nestingType):
        if nestingType == kNestingTypeInflorescence:
            if not self.options.nest_Inflorescence:
                return
        elif nestingType == kNestingTypeLeafAndPetiole:
            if not self.options.nest_LeafAndPetiole:
                return
        elif nestingType == kNestingTypeCompoundLeaf:
            if not self.options.nest_CompoundLeaf:
                return
        elif nestingType == kNestingTypePedicelAndFlowerFruit:
            if not self.options.nest_PedicelAndFlowerFruit:
                return
        elif nestingType == kNestingTypeFloralLayers:
            if not self.options.nest_FloralLayers:
                return
        else :
            raise GeneralException.create("Problem: Unrecognized nesting type in KfDrawingSurfaceForPOV.startNestedGroupOfPlantParts.")
        self.startUnion(groupName)
    
    def endNestedGroupOfPlantParts(self, nestingType):
        if nestingType == kNestingTypeInflorescence:
            if not self.options.nest_Inflorescence:
                return
        elif nestingType == kNestingTypeLeafAndPetiole:
            if not self.options.nest_LeafAndPetiole:
                return
        elif nestingType == kNestingTypeCompoundLeaf:
            if not self.options.nest_CompoundLeaf:
                return
        elif nestingType == kNestingTypePedicelAndFlowerFruit:
            if not self.options.nest_PedicelAndFlowerFruit:
                return
        elif nestingType == kNestingTypeFloralLayers:
            if not self.options.nest_FloralLayers:
                return
        else :
            raise GeneralException.create("Problem: Unrecognized nesting type in KfDrawingSurfaceForPOV.startNestedGroupOfPlantParts.")
        self.endBrace(kDontWriteColor)
    
    def startPlantPart(self, aLongName, aShortName):
        self.startUnion(aLongName)
    
    def endPlantPart(self):
        self.endBrace(kDontWriteColor)
    
    def startStemSegment(self, aLongName, aShortName, color, width, index):
        KfTextFileExportSurface.startStemSegment(self, aLongName, aShortName, color, width, index)
        self.startUnion(aLongName)
        self.setColor(color)
        self.currentWidth = width
    
    def endStemSegment(self):
        # DO want to write color for this one
        self.endBrace(kWriteColor)
    
    def start3DObject(self, aLongName, aShortName, color, index):
        KfTextFileExportSurface.start3DObject(self, aLongName, aShortName, color, index)
        self.startMesh(color, aLongName)
        self.setColor(color)
    
    def end3DObject(self):
        # DO want to write color for this one
        self.endBrace(kWriteColor)
    
    def indent(self):
        self.currentIndentLevel += 1
    
    def unindent(self):
        self.currentIndentLevel -= 1
        if self.currentIndentLevel < 0:
            self.currentIndentLevel = 0
    
    def doIndenting(self):
        i = 0
        
        for i in range(1, self.currentIndentLevel + 1):
            write(self.outputFile, chr(9))
    
    def startUnionOrMesh(self, startString, aColor, aComment):
        if aColor >= 0:
            self.currentColor = aColor
        self.doIndenting()
        write(self.outputFile, startString + " {")
        if len(aComment) > 0:
            writeln(self.outputFile, " // " + aComment)
        else:
            writeln(self.outputFile, " // " + self.currentComment)
        self.indent()
    
    def startUnion(self, aComment):
        self.startUnionOrMesh("union", -1, aComment)
    
    def startMesh(self, aColor, aComment):
        self.startUnionOrMesh("mesh", aColor, aComment)
    
    def setColor(self, aColor):
        self.currentColor = aColor
    
    def endBrace(self, writeColor):
        self.doIndenting()
        if (writeColor) and (self.options.writeColors) and (self.currentColor >= 0):
            write(self.outputFile, "pigment { color rgb <" + usupport.valueString(UNRESOLVED.getRValue(self.currentColor) / 256.0) + ", " + usupport.valueString(UNRESOLVED.getGValue(self.currentColor) / 256.0) + ", " + usupport.valueString(UNRESOLVED.getBValue(self.currentColor) / 256.0) + "> }")
        writeln(self.outputFile, "}")
        self.unindent()
    
    def basicDrawLineFromTo(self, startPoint, endPoint):
        endPointFinal = KfPoint3D()
        
        endPointFinal = endPoint
        self.doIndenting()
        write(self.outputFile, "cylinder { ")
        writeln(self.outputFile, "<" + usupport.valueString((self.pressedOrNot(self.scale * startPoint.x, kX))) + ", " + usupport.valueString(self.pressedOrNot(self.scale * -startPoint.y, kY)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * startPoint.z, kZ)) + ">, <" + usupport.valueString(self.pressedOrNot(self.scale * endPointFinal.x, kX)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * -endPointFinal.y, kY)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * endPointFinal.z, kZ)) + ">, " + usupport.valueString(self.scale * self.currentWidth) + " }")
    
    def basicDrawTriangle(self, triangle):
        p1 = KfPoint3D()
        p2 = KfPoint3D()
        p3 = KfPoint3D()
        
        p1 = triangle.points[0]
        p2 = triangle.points[1]
        p3 = triangle.points[2]
        self.doIndenting()
        write(self.outputFile, "triangle { <")
        # all y values must be negative because it seems our coordinate systems are different
        write(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * p1.x, kX)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * -p1.y, kY)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * p1.z, kZ)) + ">, <")
        write(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * p2.x, kX)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * -p2.y, kY)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * p2.z, kZ)) + ">, <")
        writeln(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * p3.x, kX)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * -p3.y, kY)) + ", " + usupport.valueString(self.pressedOrNot(self.scale * p3.z, kZ)) + "> }")
    
    def writeRegistrationReminder(self, p1, p2, p3, p4):
        triangle1 = KfTriangle()
        triangle2 = KfTriangle()
        
        self.startMesh(UNRESOLVED.rgb(100, 100, 100), self.currentPlantNameShort + "_reminder")
        triangle1 = u3dsupport.KfTriangle.create
        triangle2 = u3dsupport.KfTriangle.create
        try:
            triangle1.points[0] = p1
            triangle1.points[1] = p2
            triangle1.points[2] = p3
            self.basicDrawTriangle(triangle1)
            triangle2.points[0] = p1
            triangle2.points[1] = p3
            triangle2.points[2] = p4
            self.basicDrawTriangle(triangle2)
        finally:
            triangle1.free
            triangle2.free
        self.endBrace(kWriteColor)
    
class KfDrawingSurfaceForVRML(KfTextFileExportSurface):
    def __init__(self):
        self.currentIndentLevel = 0
        self.lastPlantPartName = ""
        self.lastMeshName = ""
    
    # ----------------------------------------------------------------------------- KfDrawingSurfaceForVRML 
    def startFile(self):
        scaleString = ""
        
        KfTextFileExportSurface.startFile(self)
        if self.options.vrml_version == kVRMLVersionOne:
            writeln(self.outputFile, "#VRML V1.0 ascii")
            writeln(self.outputFile, "#Created by PlantStudio http://www.kurtz-fernhout.com")
            writeln(self.outputFile)
        elif self.options.vrml_version == kVRMLVersionTwo:
            writeln(self.outputFile, "#VRML V2.0 utf8")
            writeln(self.outputFile, "#Created by PlantStudio http://www.kurtz-fernhout.com")
            writeln(self.outputFile)
    
    def startPlant(self, aLongName, aPlantIndex):
        # in VRML you can't have spaces in names
        aLongName = usupport.replacePunctuationWithUnderscores(aLongName)
        KfTextFileExportSurface.startPlant(self, aLongName, aPlantIndex)
        self.currentIndentLevel = 0
        if self.options.vrml_version == kVRMLVersionOne:
            self.writeThenIndent("DEF " + self.currentPlantNameShort + " Group {")
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.writeThenIndent("DEF " + self.currentPlantNameShort + " Group {")
            self.writeThenIndent("children [")
    
    def endPlant(self):
        if self.options.vrml_version == kVRMLVersionOne:
            self.endBrace("plant " + self.currentPlantNameLong)
            writeln(self.outputFile)
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.endBracket("children")
            self.endBrace("plant " + self.currentPlantNameLong)
            writeln(self.outputFile)
        self.currentIndentLevel = 0
        KfTextFileExportSurface.endPlant(self)
    
    def startNestedGroupOfPlantParts(self, groupName, shortName, nestingType):
        shortName = self.currentPlantNameShort + "_" + shortName
        if nestingType == kNestingTypeInflorescence:
            if not self.options.nest_Inflorescence:
                return
        elif nestingType == kNestingTypeLeafAndPetiole:
            if not self.options.nest_LeafAndPetiole:
                return
        elif nestingType == kNestingTypeCompoundLeaf:
            if not self.options.nest_CompoundLeaf:
                return
        elif nestingType == kNestingTypePedicelAndFlowerFruit:
            if not self.options.nest_PedicelAndFlowerFruit:
                return
        elif nestingType == kNestingTypeFloralLayers:
            if not self.options.nest_FloralLayers:
                return
        else :
            raise GeneralException.create("Problem: Unrecognized nesting type in KfDrawingSurfaceForVRML.startNestedGroupOfPlantParts.")
        if self.options.vrml_version == kVRMLVersionOne:
            self.writeThenIndent("DEF " + shortName + " Group {")
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.writeThenIndent("DEF " + shortName + " Group {")
            self.writeThenIndent("children [")
    
    def endNestedGroupOfPlantParts(self, nestingType):
        if nestingType == kNestingTypeInflorescence:
            if not self.options.nest_Inflorescence:
                return
        elif nestingType == kNestingTypeLeafAndPetiole:
            if not self.options.nest_LeafAndPetiole:
                return
        elif nestingType == kNestingTypeCompoundLeaf:
            if not self.options.nest_CompoundLeaf:
                return
        elif nestingType == kNestingTypePedicelAndFlowerFruit:
            if not self.options.nest_PedicelAndFlowerFruit:
                return
        elif nestingType == kNestingTypeFloralLayers:
            if not self.options.nest_FloralLayers:
                return
        else :
            raise GeneralException.create("Problem: Unrecognized nesting type in KfDrawingSurfaceForVRML.endNestedGroupOfPlantParts.")
        if self.options.vrml_version == kVRMLVersionOne:
            self.endBrace("nested group")
            writeln(self.outputFile)
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.endBracket("children")
            self.endBrace("nested group")
            writeln(self.outputFile)
    
    def startPlantPart(self, aLongName, aShortName):
        shortName = ""
        
        shortName = self.currentPlantNameShort + "_" + aShortName
        if self.options.vrml_version == kVRMLVersionOne:
            self.writeThenIndent("DEF " + shortName + " Group {")
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.writeThenIndent("DEF " + shortName + " Group {")
            self.writeThenIndent("children [")
        self.lastPlantPartName = shortName
    
    def endPlantPart(self):
        if self.options.vrml_version == kVRMLVersionOne:
            self.endBrace("plant part " + self.lastPlantPartName)
            writeln(self.outputFile)
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.endBracket("children")
            self.endBrace("plant part " + self.lastPlantPartName)
            writeln(self.outputFile)
    
    def startStemSegment(self, aLongName, aShortName, color, width, index):
        KfTextFileExportSurface.startStemSegment(self, aLongName, aShortName, color, width, index)
        self.setColor(color)
        self.startMesh()
    
    def endStemSegment(self):
        self.endMesh()
    
    def start3DObject(self, aLongName, aShortName, color, index):
        KfTextFileExportSurface.start3DObject(self, aLongName, aShortName, color, index)
        self.setColor(color)
        self.startMesh()
    
    def end3DObject(self):
        self.endMesh()
    
    def startMesh(self):
        if self.options.vrml_version == kVRMLVersionOne:
            self.writeThenIndent("DEF " + self.currentGroupingString + " Group {")
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.writeConsideringIndenting("DEF " + self.currentGroupingString + " Shape {")
            self.indent()
            if self.options.writeColors:
                self.writeConsideringIndenting("appearance Appearance { material Material { diffuseColor " + usupport.valueString(UNRESOLVED.getRValue(self.currentColor) / 256.0) + " " + usupport.valueString(UNRESOLVED.getGValue(self.currentColor) / 256.0) + " " + usupport.valueString(UNRESOLVED.getBValue(self.currentColor) / 256.0) + " } }")
        self.lastMeshName = self.currentGroupingString
    
    def endMesh(self):
        self.writePointsAndTriangles()
        if self.options.vrml_version == kVRMLVersionOne:
            self.endBrace("mesh " + self.lastMeshName)
            writeln(self.outputFile)
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.endBrace("shape " + self.lastMeshName)
            writeln(self.outputFile)
    
    def writePointsAndTriangles(self):
        i = 0
        
        if self.options.vrml_version == kVRMLVersionOne:
            # shape hints
            self.writeThenIndent("ShapeHints {")
            self.writeConsideringIndenting("vertexOrdering COUNTERCLOCKWISE")
            self.writeConsideringIndenting("shapeType SOLID")
            self.writeConsideringIndenting("faceType CONVEX")
            self.endBrace("ShapeHints")
            if self.options.writeColors:
                # color
                self.writeConsideringIndenting("Material { diffuseColor [ " + usupport.valueString(UNRESOLVED.getRValue(self.currentColor) / 256.0) + " " + usupport.valueString(UNRESOLVED.getGValue(self.currentColor) / 256.0) + " " + usupport.valueString(UNRESOLVED.getBValue(self.currentColor) / 256.0) + " ] }")
            # coordinate points
            self.writeThenIndent("Coordinate3 {")
            self.writeThenIndent("point [")
            self.doIndenting()
            for i in range(0, self.numPoints):
                write(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * self.points[i].x, kX)) + " " + usupport.valueString(self.pressedOrNot(self.scale * -self.points[i].y, kY)) + " " + usupport.valueString(self.pressedOrNot(self.scale * self.points[i].z, kZ)))
                if i < self.numPoints - 1:
                    write(self.outputFile, ", ")
                if (i % kNumVRMLPointsPerLine == 0) or (i == self.numPoints - 1):
                    writeln(self.outputFile)
                    if i < self.numPoints - 1:
                        self.doIndenting()
            self.endBracket("point")
            self.endBrace("Coordinate3")
            # faces
            #'DEF ' + self.currentGroupingString +
            self.writeThenIndent("IndexedFaceSet {")
            self.writeThenIndent("coordIndex [")
            self.doIndenting()
            for i in range(0, self.numFaces):
                write(self.outputFile, IntToStr(self.faces[i].vertex1) + ", " + IntToStr(self.faces[i].vertex2) + ", " + IntToStr(self.faces[i].vertex3) + ", -1")
                if i < self.numFaces - 1:
                    write(self.outputFile, ", ")
                if (i % kNumVRMLPointsPerLine == 0) or (i == self.numFaces - 1):
                    writeln(self.outputFile)
                    if i < self.numFaces - 1:
                        self.doIndenting()
            self.endBracket("coordIndex")
            self.endBrace("IndexedFaceSet")
        elif self.options.vrml_version == kVRMLVersionTwo:
            self.writeThenIndent("geometry IndexedFaceSet {")
            self.writeThenIndent("coord Coordinate {")
            self.writeThenIndent("point [")
            self.doIndenting()
            for i in range(0, self.numPoints):
                write(self.outputFile, usupport.valueString(self.pressedOrNot(self.scale * self.points[i].x, kX)) + " " + usupport.valueString(self.pressedOrNot(self.scale * -self.points[i].y, kY)) + " " + usupport.valueString(self.pressedOrNot(self.scale * self.points[i].z, kZ)))
                if i < self.numPoints - 1:
                    write(self.outputFile, ", ")
                if (i % kNumVRMLPointsPerLine == 0) or (i == self.numPoints - 1):
                    writeln(self.outputFile)
                    if i < self.numPoints - 1:
                        self.doIndenting()
            self.endBracket("point")
            self.endBrace("Coordinate")
            self.writeConsideringIndenting("ccw TRUE")
            self.writeConsideringIndenting("colorPerVertex FALSE")
            self.writeThenIndent("coordIndex [")
            self.doIndenting()
            for i in range(0, self.numFaces):
                write(self.outputFile, IntToStr(self.faces[i].vertex1) + ", " + IntToStr(self.faces[i].vertex2) + ", " + IntToStr(self.faces[i].vertex3) + ", -1")
                if i < self.numFaces - 1:
                    write(self.outputFile, ", ")
                if (i % kNumVRMLPointsPerLine == 0) or (i == self.numFaces - 1):
                    writeln(self.outputFile)
                    if i < self.numFaces - 1:
                        self.doIndenting()
            self.endBracket("coordIndex")
            self.writeConsideringIndenting("creaseAngle 0.5")
            self.writeConsideringIndenting("normalPerVertex TRUE")
            self.writeConsideringIndenting("solid FALSE")
            self.endBrace("IndexedFaceSet")
        self.numPoints = 0
        self.numFaces = 0
    
    def setColor(self, aColor):
        self.currentColor = aColor
    
    def endBrace(self, comment):
        self.doIndenting()
        writeln(self.outputFile, "} # " + comment)
        self.unindent()
    
    def endBracket(self, comment):
        self.doIndenting()
        writeln(self.outputFile, "] # " + comment)
        self.unindent()
    
    def indent(self):
        self.currentIndentLevel += 1
    
    def unindent(self):
        self.currentIndentLevel -= 1
        if self.currentIndentLevel < 0:
            self.currentIndentLevel = 0
    
    def doIndenting(self):
        i = 0
        
        for i in range(1, self.currentIndentLevel + 1):
            # chr(9));
            write(self.outputFile, "  ")
    
    def writeConsideringIndenting(self, aString):
        self.doIndenting()
        writeln(self.outputFile, aString)
    
    def indentThenWrite(self, aString):
        self.indent()
        self.doIndenting()
        writeln(self.outputFile, aString)
    
    def writeThenIndent(self, aString):
        self.doIndenting()
        writeln(self.outputFile, aString)
        self.indent()
    
    def writeRegistrationReminder(self, p1, p2, p3, p4):
        numPointsAtStart = 0L
        
        self.setColor(UNRESOLVED.rgb(100, 100, 100))
        self.currentGroupingString = self.currentPlantNameShort + "_reminder"
        self.startMesh()
        numPointsAtStart = self.numPoints
        self.addPoint(p1)
        self.addPoint(p2)
        self.addPoint(p3)
        self.addPoint(p4)
        self.addTriangle(numPointsAtStart, numPointsAtStart + 1, numPointsAtStart + 3)
        self.addTriangle(numPointsAtStart + 1, numPointsAtStart + 2, numPointsAtStart + 3)
        self.writePointsAndTriangles()
        self.endMesh()
    
class KfDrawingSurfaceForOBJ(KfTextFileExportSurface):
    def __init__(self):
        self.numMaterialsStored = 0
        self.materialColors = [0] * (range(0, kMaxStoredMaterials + 1) + 1)
        self.materialNames = [0] * (range(0, kMaxStoredMaterials + 1) + 1)
        self.materialsFileName = ""
    
    # ----------------------------------------------------------------------------- KfDrawingSurfaceForOBJ 
    def startFile(self):
        KfTextFileExportSurface.startFile(self)
        writeln(self.outputFile, "# OBJ file created by PlantStudio http://www.kurtz-fernhout.com")
        if self.options.writeColors:
            self.materialsFileName = ExtractFilePath(self.fileName) + usupport.stringUpTo(ExtractFileName(self.fileName), ".") + ".mtl"
            writeln(self.outputFile)
            writeln(self.outputFile, "# Materials file must be in same directory")
            writeln(self.outputFile, "mtllib " + ExtractFileName(self.materialsFileName))
    
    def endFile(self):
        if self.options.writeColors:
            self.writeMaterialDescriptionsToFile()
        KfTextFileExportSurface.endFile(self)
    
    def startPlant(self, aLongName, aPlantIndex):
        KfTextFileExportSurface.startPlant(self, aLongName, aPlantIndex)
        writeln(self.outputFile)
        writeln(self.outputFile, "# plant \"" + self.currentPlantNameLong + "\"")
        writeln(self.outputFile, "o " + self.currentPlantNameShort)
        if (udomain.domain.registered) and (self.options.layeringOption == kLayerOutputAllTogether):
            self.startGroup(self.currentPlantNameShort)
    
    def startStemSegment(self, aLongName, aShortName, color, width, index):
        KfTextFileExportSurface.startStemSegment(self, aLongName, aShortName, color, width, index)
        if (self.options.layeringOption != kLayerOutputAllTogether) and (self.currentGroupingString != ""):
            self.startGroup(self.currentGroupingString)
        # color should always be set by the part type, no matter what grouping setting
        self.startColor(color, self.currentPlantNameShort + "_" + aShortName)
        self.startVerticesAndTriangles()
    
    def endStemSegment(self):
        self.endVerticesAndTriangles()
    
    def start3DObject(self, aLongName, aShortName, color, index):
        KfTextFileExportSurface.start3DObject(self, aLongName, aShortName, color, index)
        if (self.options.layeringOption != kLayerOutputAllTogether) and (self.currentGroupingString != ""):
            self.startGroup(self.currentGroupingString)
        # color should always be set by the part type, no matter what grouping setting
        self.startColor(color, self.currentPlantNameShort + "_" + aShortName)
    
    def writeMaterialDescriptionsToFile(self):
        materialsFile = TextFile()
        i = 0
        colorString = ""
        fileInfo = SaveFileNamesStructure()
        
        if self.numMaterialsStored <= 0:
            return
        if usupport.getFileSaveInfo(usupport.kFileTypeMTL, usupport.kDontAskForFileName, self.materialsFileName, fileInfo):
            AssignFile(materialsFile, fileInfo.tempFile)
            try:
                usupport.setDecimalSeparator()
                Rewrite(materialsFile)
                usupport.startFileSave(fileInfo)
                writeln(materialsFile, "# Materials for file " + usupport.stringUpTo(ExtractFileName(self.materialsFileName), ".") + ".obj")
                writeln(materialsFile, "# Created by PlantStudio http://www.kurtz-fernhout.com")
                writeln(materialsFile, "# These files must be in the same directory for the materials to be read correctly.")
                for i in range(0, self.numMaterialsStored):
                    if self.materialNames[i] == "":
                        #newmtl name
                        #Ka  0.1 0.0 0.0
                        #Kd  0.4 0.0 0.0
                        #Ks  0.4 0.0 0.0
                        #Ns  20
                        #d  1.0 (0 transparent 1 opaque)
                        #illum 1
                        continue
                    writeln(materialsFile, "newmtl " + self.materialNames[i])
                    colorString = usupport.valueString(UNRESOLVED.GetRValue(self.materialColors[i]) / 255.0) + " " + usupport.valueString(UNRESOLVED.GetGValue(self.materialColors[i]) / 255.0) + " " + usupport.valueString(UNRESOLVED.GetBValue(self.materialColors[i]) / 255.0)
                    writeln(materialsFile, "Ka  " + colorString)
                    writeln(materialsFile, "Kd  " + colorString)
                    writeln(materialsFile, "Ks  " + colorString)
                    writeln(materialsFile, "d 1.0")
                    writeln(materialsFile, "illum 1")
                    writeln(materialsFile)
                fileInfo.writingWasSuccessful = true
            finally:
                CloseFile(materialsFile)
                usupport.cleanUpAfterFileSave(fileInfo)
    
    def storeMaterialDescription(self, aName, aColor):
        i = 0
        
        if self.numMaterialsStored > 0:
            for i in range(0, self.numMaterialsStored):
                if self.materialNames[i] == aName:
                    return
        if self.numMaterialsStored >= kMaxStoredMaterials:
            return
        self.numMaterialsStored += 1
        self.materialColors[self.numMaterialsStored] = aColor
        self.materialNames[self.numMaterialsStored] = aName
    
    def startGroup(self, aName):
        writeln(self.outputFile)
        writeln(self.outputFile, "g " + aName)
        writeln(self.outputFile, "s off")
    
    def startColor(self, aColor, aMaterialName):
        if not self.options.writeColors:
            return
        writeln(self.outputFile)
        writeln(self.outputFile, "usemtl " + aMaterialName)
        self.storeMaterialDescription(aMaterialName, aColor)
    
    def endVerticesAndTriangles(self):
        i = 0
        
        writeln(self.outputFile)
        writeln(self.outputFile, "# " + IntToStr(self.numPoints) + " vertices")
        for i in range(0, self.numPoints):
            writeln(self.outputFile, "v " + usupport.valueString(self.pressedOrNot(self.scale * self.points[i].x, kX)) + " " + usupport.valueString(self.pressedOrNot(self.scale * -self.points[i].y, kY)) + " " + usupport.valueString(self.pressedOrNot(self.scale * self.points[i].z, kZ)))
        writeln(self.outputFile)
        writeln(self.outputFile, "# " + IntToStr(self.numFaces) + " faces")
        for i in range(0, self.numFaces):
            writeln(self.outputFile, "f " + IntToStr(self.faces[i].vertex1 - self.numPoints) + " " + IntToStr(self.faces[i].vertex2 - self.numPoints) + " " + IntToStr(self.faces[i].vertex3 - self.numPoints) + " ")
        self.numPoints = 0
        self.numFaces = 0
    
    def writeRegistrationReminder(self, p1, p2, p3, p4):
        numPointsAtStart = 0
        
        self.startGroup(self.currentPlantNameShort + "_reminder")
        self.startColor(UNRESOLVED.rgb(100, 100, 100), "reminder_gray")
        numPointsAtStart = self.numPoints
        self.startVerticesAndTriangles()
        self.addPoint(p1)
        self.addPoint(p2)
        self.addPoint(p3)
        self.addPoint(p4)
        self.addTriangle(numPointsAtStart, numPointsAtStart + 1, numPointsAtStart + 3)
        self.addTriangle(numPointsAtStart + 1, numPointsAtStart + 2, numPointsAtStart + 3)
        self.endVerticesAndTriangles()
        if self.options.layeringOption == kLayerOutputAllTogether:
            self.startGroup(self.currentPlantNameShort)
    
class KfBinaryFileExportSurface(KfFileExportSurface):
    def __init__(self):
        self.stream = TFileStream()
        self.chunkStartStack = TList()
    
    # ----------------------------------------------------------------------------- KfBinaryFileExportSurface 
    def createWithFileName(self, aFileName):
        KfFileExportSurface.createWithFileName(self, aFileName)
        self.chunkStartStack = delphi_compatability.TList().Create()
        return self
    
    def destroy(self):
        self.chunkStartStack.free
        self.chunkStartStack = None
        # this closes the file
        self.stream.free
        self.stream = None
        KfFileExportSurface.destroy(self)
    
    def startFile(self):
        self.stream = delphi_compatability.TFileStream().Create(self.fileName, delphi_compatability.fmCreate or UNRESOLVED.fmShareExclusive)
    
    def endFile(self):
        raise GeneralException.create("subclasses must override")
    
    def writeStringZ(self, value):
        stringBuffer = [0] * (range(0, 1024 + 1) + 1)
        i = 0
        
        if len(value) > 1023:
            raise GeneralException.Create("Problem: String too long in KfBinaryFileExportSurface.writeStringZ.")
        for i in range(1, len(value) + 1):
            stringBuffer[i - 1] = value[i]
        stringBuffer[len(value)] = chr(0)
        self.stream.WriteBuffer(stringBuffer, len(value) + 1)
        # maybe should align on four byte boundaries for efficiency of seeks later?
    
    def writeByte(self, value):
        self.stream.WriteBuffer(value, 1)
    
    def writeWord(self, value):
        swappedBytes = [0] * (range(0, 1 + 1) + 1)
        
        if self.isLittleEndian():
            self.stream.WriteBuffer(value, 2)
        else:
            swappedBytes[1] = value and 255
            swappedBytes[0] = value >> 8
            self.stream.WriteBuffer(swappedBytes, 2)
    
    def writeDword(self, value):
        swappedBytes = [0] * (range(0, 3 + 1) + 1)
        
        if self.isLittleEndian():
            self.stream.WriteBuffer(value, 4)
        else:
            swappedBytes[3] = value and 255
            swappedBytes[2] = (value >> 8) and 255
            swappedBytes[1] = (value >> 16) and 255
            swappedBytes[0] = (value >> 24) and 255
            self.stream.WriteBuffer(swappedBytes, 4)
    
    def writeFloat(self, value):
        convert = SingleOverlay()
        swappedBytes = [0] * (range(0, 3 + 1) + 1)
        
        if self.isLittleEndian():
            self.stream.WriteBuffer(value, 4)
        else:
            convert.numeric = value
            swappedBytes[3] = convert.bytes[0]
            swappedBytes[2] = convert.bytes[1]
            swappedBytes[1] = convert.bytes[2]
            swappedBytes[0] = convert.bytes[3]
            self.stream.WriteBuffer(swappedBytes, 4)
    
    def isLittleEndian(self):
        result = false
        # subclasses should override if they need to change this
        result = true
        return result
    
class KfDrawingSurfaceFor3DS(KfBinaryFileExportSurface):
    def __init__(self):
        self.currentMaterialName = ""
    
    # ----------------------------------------------------------------------------- KfDrawingSurfaceFor3DS 
    def createWithFileName(self, aFileName):
        # we assume that the file name has been already okayed
        KfBinaryFileExportSurface.createWithFileName(self, aFileName)
        self.currentMaterialName = "not defined"
        return self
    
    def destroy(self):
        KfBinaryFileExportSurface.destroy(self)
    
    def startFile(self):
        KfBinaryFileExportSurface.startFile(self)
        # 4d4dH 	M3DMAGIC; 3DS Magic Number (.3DS file)
        self.startChunk(0x4D4D)
        # 3d3dH 	MDATA; Mesh Data Magic Number (.3DS files sub of 4d4d)
        self.startChunk(0x3D3D)
    
    def endFile(self):
        # 3d3dH 	MDATA; Mesh Data Magic Number (.3DS files sub of 4d4d)
        self.finishChunk(0x3D3D)
        # 4d4dH 	M3DMAGIC; 3DS Magic Number (.3DS file)
        self.finishChunk(0x4D4D)
    
    def startStemSegment(self, aLongName, aShortName, color, width, index):
        KfBinaryFileExportSurface.startStemSegment(self, aLongName, aShortName, color, width, index)
        self.currentMaterialName = self.currentPlantNameShort + "_" + aShortName
        self.startVerticesAndTriangles()
    
    def endStemSegment(self):
        self.endVerticesAndTriangles()
    
    def start3DObject(self, aLongName, aShortName, color, index):
        KfBinaryFileExportSurface.start3DObject(self, aLongName, aShortName, color, index)
        self.currentMaterialName = self.currentPlantNameShort + "_" + aShortName
    
    def startVerticesAndTriangles(self):
        self.startMeshObject(self.currentGroupingString)
    
    def endVerticesAndTriangles(self):
        i = 0
        
        # 4110H 	POINT_ARRAY short npoints; struct (float x, y, z;) points[npoints];
        self.startChunk(0x4110)
        self.writeWord(self.numPoints)
        for i in range(0, self.numPoints):
            self.writeFloat(self.pressedOrNot(self.scale * self.points[i].x, kX))
            self.writeFloat(self.pressedOrNot(self.scale * self.points[i].y, kY))
            self.writeFloat(self.pressedOrNot(self.scale * self.points[i].z, kZ))
        self.finishChunk(0x4110)
        # 4120H 	FACE_ARRAY may be followed by smooth_group short nfaces;
        # struct (short vertex1, vertex2, vertex3; short flags;) facearray[nfaces];
        self.startChunk(0x4120)
        self.writeWord(self.numFaces)
        for i in range(0, self.numFaces):
            self.writeWord(self.faces[i].vertex1)
            self.writeWord(self.faces[i].vertex2)
            self.writeWord(self.faces[i].vertex3)
            self.writeWord(7)
        if self.options.writeColors:
            # now set all faces to be of same material
            self.startChunk(0x4130)
            self.writeStringZ(self.currentMaterialName)
            self.writeWord(self.numFaces)
            for i in range(0, self.numFaces):
                self.writeWord(i)
            self.finishChunk(0x4130)
        self.finishChunk(0x4120)
        # close mesh
        self.finishMeshObject()
        # zero out
        self.numFaces = 0
        self.numPoints = 0
    
    def startMeshObject(self, name):
        # 4000H 	NAMED_OBJECT cstr name;
        self.startChunk(0x4000)
        self.writeStringZ(name)
        # 4100H 	N_TRI_OBJECT named triangle object followed by point_array, point_flag_array, mesh_matrix, face_array
        self.startChunk(0x4100)
    
    def finishMeshObject(self):
        # 4100H 	N_TRI_OBJECT named triangle object followed by point_array, point_flag_array, mesh_matrix, face_array
        self.finishChunk(0x4100)
        # 4000H 	NAMED_OBJECT cstr name;
        self.finishChunk(0x4000)
    
    def pushChunkStart(self):
        position = 0
        
        position = self.stream.Position
        self.chunkStartStack.Add(UNRESOLVED.Pointer(position))
    
    def popChunkStartAndFixupChunkSize(self):
        chunkSize = 0
        startSize = 0
        totalSize = 0
        lastIndex = 0
        
        totalSize = self.stream.Size
        lastIndex = self.chunkStartStack.Count - 1
        if lastIndex < 0:
            # should check if -1
            raise GeneralException.Create("Problem with stack indexing for 3DS writing in method KfDrawingSurfaceFor3DS.popChunkStartAndFixupChunkSize.")
        startSize = self.chunkStartStack.Items[lastIndex]
        self.chunkStartStack.Delete(lastIndex)
        chunkSize = totalSize - startSize
        # skip two to avoid overwriting chunk type
        self.stream.Seek(startSize + 2, delphi_compatability.soFromBeginning)
        self.writeDword(chunkSize)
        self.stream.Seek(0, delphi_compatability.soFromEnd)
    
    def startChunk(self, chunkID):
        self.pushChunkStart()
        self.writeWord(chunkID)
        # write placeholder dword that will be patched later
        self.writeDword(0)
    
    def finishChunk(self, chunkType):
        self.popChunkStartAndFixupChunkSize()
    
    def writeMaterialDescription(self, index, aColor):
        if not self.options.writeColors:
            return
        if index < 0:
            self.writeMaterialColorChunk(self.currentPlantNameShort + "_rem", UNRESOLVED.getRValue(aColor), UNRESOLVED.getGValue(aColor), UNRESOLVED.getBValue(aColor))
        else:
            self.writeMaterialColorChunk(self.currentPlantNameShort + "_" + shortNameForDXFPartType(index), UNRESOLVED.getRValue(aColor), UNRESOLVED.getGValue(aColor), UNRESOLVED.getBValue(aColor))
    
    def writeColorChunk(self, r, g, b):
        self.startChunk(0x0011)
        self.writeByte(r)
        self.writeByte(g)
        self.writeByte(b)
        self.finishChunk(0x0011)
    
    def writeMaterialColorChunk(self, materialName, r, g, b):
        # Material editor chunk
        self.startChunk(0xAFFF)
        # Material name
        self.startChunk(0xA000)
        self.writeStringZ(materialName)
        self.finishChunk(0xA000)
        # Material ambient color
        self.startChunk(0xA010)
        self.writeColorChunk(r, g, b)
        self.finishChunk(0xA010)
        # Material diffuse color
        self.startChunk(0xA020)
        self.writeColorChunk(r, g, b)
        self.finishChunk(0xA020)
        self.finishChunk(0xAFFF)
    
    def writeRegistrationReminder(self, p1, p2, p3, p4):
        numPointsAtStart = 0
        
        self.currentGroupingString = self.currentPlantNameShort + "_rem"
        self.currentMaterialName = self.currentPlantNameShort + "_rem"
        numPointsAtStart = self.numPoints
        self.startVerticesAndTriangles()
        self.addPoint(p1)
        self.addPoint(p2)
        self.addPoint(p3)
        self.addPoint(p4)
        self.addTriangle(numPointsAtStart, numPointsAtStart + 1, numPointsAtStart + 3)
        self.addTriangle(numPointsAtStart + 1, numPointsAtStart + 2, numPointsAtStart + 3)
        self.endVerticesAndTriangles()
    
class KfDrawingSurfaceForLWO(KfBinaryFileExportSurface):
    def __init__(self):
        self.currentSurfaceID = 0
        self.numSurfacesStored = 0
        self.surfaceColors = [0] * (range(1, kMaxStoredMaterials + 1) + 1)
        self.surfaceNames = [0] * (range(1, kMaxStoredMaterials + 1) + 1)
    
    # ----------------------------------------------------------------------------- KfDrawingSurfaceForLWO 
    def endFile(self):
        i = 0L
        
        # start file
        self.startChunk("FORM")
        self.writeTagOfFourCharacters("LWOB")
        # points
        self.startChunk("PNTS")
        for i in range(0, self.numPoints):
            self.writeFloat(self.pressedOrNot(self.scale * self.points[i].x, kX))
            self.writeFloat(self.pressedOrNot(self.scale * self.points[i].y, kY))
            self.writeFloat(self.pressedOrNot(self.scale * self.points[i].z, kZ))
        self.finishChunk()
        if self.options.writeColors:
            # surfaces
            self.startChunk("SRFS")
            for i in range(1, self.numSurfacesStored + 1):
                self.writeStringZ(self.surfaceNames[i])
                if odd(len(self.surfaceNames[i]) + 1):
                    #1 is for terminating zero
                    self.writeByte(0)
            self.finishChunk()
        else:
            self.startChunk("SRFS")
            # if you change this to an odd # considering the end zero you must pad it
            self.writeStringZ("default")
            self.finishChunk()
        # faces
        self.startChunk("POLS")
        for i in range(0, self.numFaces):
            self.writeWord(3)
            self.writeWord(self.faces[i].vertex1)
            self.writeWord(self.faces[i].vertex2)
            self.writeWord(self.faces[i].vertex3)
            if self.options.writeColors:
                self.writeWord(self.faces[i].surfaceID)
            else:
                self.writeWord(1)
        self.finishChunk()
        if self.options.writeColors:
            for i in range(1, self.numSurfacesStored + 1):
                # surfaces again
                self.startChunk("SURF")
                self.writeStringZ(self.surfaceNames[i])
                if odd(len(self.surfaceNames[i]) + 1):
                    #terminating zero
                    self.writeByte(0)
                self.writeTagOfFourCharacters("COLR")
                self.writeWord(4)
                self.writeByte(UNRESOLVED.getRValue(self.surfaceColors[i]))
                self.writeByte(UNRESOLVED.getGValue(self.surfaceColors[i]))
                self.writeByte(UNRESOLVED.getBValue(self.surfaceColors[i]))
                self.writeByte(0)
                self.writeTagOfFourCharacters("FLAG")
                self.writeWord(2)
                # double-sided flag
                self.writeWord(0x0100)
                self.writeTagOfFourCharacters("DIFF")
                self.writeWord(2)
                self.writeWord(256)
                self.finishChunk()
        else:
            self.startChunk("SURF")
            # if you change this to an odd # considering the end zero you must pad it
            self.writeStringZ("default")
            self.writeTagOfFourCharacters("COLR")
            self.writeWord(4)
            self.writeByte(200)
            self.writeByte(200)
            self.writeByte(200)
            self.writeByte(0)
            self.finishChunk()
        # finishes 'FORM' chunk
        self.finishChunk()
        self.numFaces = 0
        self.numPoints = 0
    
    def isLittleEndian(self):
        result = false
        result = false
        return result
    
    def startStemSegment(self, aLongName, aShortName, color, width, index):
        KfBinaryFileExportSurface.startStemSegment(self, aLongName, aShortName, color, width, index)
        #currentPlantNameShort + '_' + aShortName
        self.currentSurfaceID = self.lookUpSurfaceIDForName(self.currentGroupingString, color)
    
    def lookUpSurfaceIDForName(self, aName, color):
        result = 0
        i = 0L
        
        for i in range(1, self.numSurfacesStored + 1):
            if self.surfaceNames[i] == aName:
                result = i
                return result
        if self.numSurfacesStored < kMaxStoredMaterials:
            self.numSurfacesStored += 1
            self.surfaceNames[self.numSurfacesStored] = aName
            self.surfaceColors[self.numSurfacesStored] = color
        result = self.numSurfacesStored
        return result
    
    def drawPipeFaces(self, startPoints, endPoints, faces, segmentNumber):
        i = 0L
        firstPtIndex = 0L
        
        firstPtIndex = self.numPoints
        for i in range(0, faces):
            self.addPoint(startPoints[i])
        for i in range(0, faces):
            self.addPoint(endPoints[i])
        for i in range(0, faces):
            self.addTriangle(firstPtIndex + i, firstPtIndex + i + faces, firstPtIndex + (i + 1) % faces)
            self.addTriangle(firstPtIndex + (i + 1) % faces, firstPtIndex + i + faces, firstPtIndex + (i + 1) % faces + faces)
    
    def start3DObject(self, aLongName, aShortName, color, index):
        KfBinaryFileExportSurface.start3DObject(self, aLongName, aShortName, color, index)
        #currentPlantNameShort + '_' + aShortName
        self.currentSurfaceID = self.lookUpSurfaceIDForName(self.currentGroupingString, color)
    
    def addTriangle(self, a, b, c):
        self.addTriangleWithSurface(a, b, c, self.currentSurfaceID)
    
    def addTriangleWithSurface(self, a, b, c, surfaceID):
        if self.numFaces >= kMax3DFaces:
            raise GeneralException.Create("Problem: Too many faces in LWO; in method KfDrawingSurfaceFor3DS.addTriangle.")
        self.faces[self.numFaces].vertex1 = a
        self.faces[self.numFaces].vertex2 = b
        self.faces[self.numFaces].vertex3 = c
        self.faces[self.numFaces].surfaceID = self.currentSurfaceID
        self.numFaces += 1
    
    def pushChunkStart(self):
        position = 0
        
        position = self.stream.Position
        self.chunkStartStack.Add(UNRESOLVED.Pointer(position))
    
    def popChunkStartAndFixupChunkSize(self):
        chunkSize = 0
        startSize = 0
        totalSize = 0
        lastIndex = 0
        
        totalSize = self.stream.Size
        lastIndex = self.chunkStartStack.Count - 1
        if lastIndex < 0:
            # should check if -1
            raise GeneralException.Create("Problem with stack indexing for 3DS writing in method KfDrawingSurfaceFor3DS.popChunkStartAndFixupChunkSize.")
        startSize = self.chunkStartStack.Items[lastIndex]
        self.chunkStartStack.Delete(lastIndex)
        chunkSize = totalSize - startSize
        # skip back four
        self.stream.Seek(startSize - 4, delphi_compatability.soFromBeginning)
        # lwo chunk sizes do not include the header
        self.writeDword(chunkSize)
        self.stream.Seek(0, delphi_compatability.soFromEnd)
    
    def startChunk(self, chunkName):
        self.writeTagOfFourCharacters(chunkName)
        # write placeholder dword that will be patched later
        self.writeDword(0)
        self.pushChunkStart()
    
    def finishChunk(self):
        self.popChunkStartAndFixupChunkSize()
    
    def writeTagOfFourCharacters(self, aString):
        self.writeByte(aString[1])
        self.writeByte(aString[2])
        self.writeByte(aString[3])
        self.writeByte(aString[4])
    
    def writeRegistrationReminder(self, p1, p2, p3, p4):
        numPointsAtStart = 0
        
        self.currentSurfaceID = self.lookUpSurfaceIDForName(self.currentPlantNameShort + "_rem", UNRESOLVED.rgb(100, 100, 100))
        numPointsAtStart = self.numPoints
        self.addPoint(p1)
        self.addPoint(p2)
        self.addPoint(p3)
        self.addPoint(p4)
        self.addTriangle(numPointsAtStart, numPointsAtStart + 1, numPointsAtStart + 3)
        self.addTriangle(numPointsAtStart + 1, numPointsAtStart + 2, numPointsAtStart + 3)
    
# VRML 1.0 spec
#
#DEF plantName Group {
#  DEF nestingName Group {
#    DEF partName Group {
#      Material { diffuseColor [ 0.19 0.39 0.19 ] }
#	    ShapeHints {
#	      vertexOrdering	COUNTERCLOCKWISE
#	      shapeType	SOLID
#	      creaseAngle	3.14159
#	      } # ShapeHints
#      Coordinate3 {
#          point [
#            49.64	304.6	117.55	,
#            56.71	312.51	123.85	,
#            ] # point
#          } # Coordinate3
#      IndexedFaceSet {
#        coordIndex [
#          0	, 1	, 2	, -1	,
#          1	, 3	, 2	, -1	,
#          ] # coordIndex
#        } # IndexedFaceSet
#      } # Group partName
#    } # Group nestingName
#  } # Group plantName
#
# VRML 2.0 spec
#
#DEF plantName Group {
#  children [
#  DEF nestingName Group {
#    children [
#      DEF partName Shape {
#        appearance Appearance { material Material { diffuseColor  0.99 0  0.5 } }
#        geometry IndexedFaceSet {
#          coord Coordinate {
#            point [
#              49.64	304.6	117.55	,
#              56.71	312.51	123.85	,
#              ] # point
#            } # Coordinate
#          ccw TRUE
#          colorPerVertex FALSE
#          coordIndex [
#            0	, 1	, 2	, -1	,
#            1	, 3	, 2	, -1	,
#            ] # coordIndex
#          creaseAngle 0.5
#          normalPerVertex TRUE
#          solid FALSE
#          } #  IndexedFaceSet
#        } # Shape
#      ] # children nestingName
#      } # Group nestingName
#    ] # children plantName
#  } # Group plantName
#
