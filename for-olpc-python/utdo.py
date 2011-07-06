# unit Utdo

from conversion_common import *
import copy
import delphi_compatability
import usstream
import u3dsupport
import ucollect

"""
import u3dexport
import uplant
import udebug
import usupport
import uclasses
import uturtle
import ufiler
"""

# const
kMaximumRecordedPoints = 10000
kAdjustForOrigin = True
kDontAdjustForOrigin = False
kEmbeddedInPlant = True
kInTdoLibrary = False
kStandAloneFile = False
kTdoForeColor = delphi_compatability.clSilver
kTdoBackColor = delphi_compatability.clGray
kTdoLineContrastIndex = 10
kStartTdoString = "start 3D object"
kEndTdoString = "end 3D object"

# v1.6b2 changed from 200 to 1000 ; v2.0 changed to 10000 (not in tdo anymore)
# v1.11 moved up here
# v1.11 moved up here
# record
# const

def betweenBrackets(aString):
    # lose letter and [ on front, lose ] on back 
    result = aString[2:-1]
    return result

#class KfIndexTriangle(PdStreamableObject):
class KfIndexTriangle:
    def __init__(self):
        self.pointIndexes = [0] * 3
    
    # ---------------------------------------------------------------------------------- KfIndexTriangle 
    def createABC(self, a, b, c):
        self.pointIndexes[0] = a
        self.pointIndexes[1] = b
        self.pointIndexes[2] = c
        return self
    
    def flip(self):
        savePoint = self.pointIndexes[0]
        self.pointIndexes[0] = self.pointIndexes[2]
        self.pointIndexes[2] = savePoint
    
    def copyFrom(self, aTriangle):
        if aTriangle == None:
            return
        self.pointIndexes[0] = aTriangle.pointIndexes[0]
        self.pointIndexes[1] = aTriangle.pointIndexes[1]
        self.pointIndexes[2] = aTriangle.pointIndexes[2]
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kKfIndexTriangle
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.pointIndexes = filer.streamBytes(self.pointIndexes, FIX_sizeof(self.pointIndexes))
    
#class KfObject3D(PdStreamableObject):
# doesn't need to be streamed, only used while drawing
# ---------------------------------------------------------------------------------- KfObject3D 
class KfObject3D:
    def __init__(self):
        self.points = []
        self.originPointIndex = 0
        self.triangles = ucollect.TListCollection()
        self.name = ""
        self.originalIfCopy = None
        self.inUse = False
        self.zForSorting = 0.0
        self.indexWhenRemoved = 0
        self.selectedIndexWhenRemoved = 0
        self.boundsRect = delphi_compatability.TRect()
    
    def getPoint(self, index):
        return self.pointData[index]
    
    def setPoint(self, index, aPoint):
        if self.pointData == None:
            raise GeneralException.create("Problem: Nil pointer in method KfObject3D.setPoint.")
        self.pointData[index] = aPoint
    
    def clear(self):
        self.clearPoints()
        self.name = ""
    
    def clearPoints(self):
        self.points = []
        self.originPointIndex = 0
        self.triangles.clear()
    
    def copyFrom(self, original):
        if original == None:
            return
        self.setName(original.name)
        self.points = []
        for point in original.points:
            self.points.append(copy.copy(point))
        self.originPointIndex = original.originPointIndex
        self.triangles.clear()
        for theTriangle in original.triangles:
            self.addTriangle(KfIndexTriangle().createABC(theTriangle.pointIndexes[0], theTriangle.pointIndexes[1], theTriangle.pointIndexes[2]))
        self.inUse = original.inUse
    
    def isSameAs(self, other):
        #False if fails any test
        if self.name != other.name:
            return False
        if len(self.points) != len(other.points):
            return False
        if self.originPointIndex != other.originPointIndex:
            return False
        if len(self.triangles) != len(other.triangles):
            return False
        for i in range(0, len(self.points)):
            thePoint = self.points[i]
            otherPoint = other.points[i]
            if (intround(thePoint.x) != intround(otherPoint.x)) or (intround(thePoint.y) != intround(otherPoint.y)) or (intround(thePoint.z) != intround(otherPoint.z)):
                # round these because otherwise i/o inaccuracies could make a tdo seem different when it isn't,
                # and most numbers are far enough to be integers anyway
                return False
        for i in range(0, len(self.triangles)):
            theTriangle = self.triangles[i]
            otherTriangle = other.triangles[i]
            for j in range(0, 3):
                if theTriangle.pointIndexes[j] != otherTriangle.pointIndexes[j]:
                    return False
        #passed all the tests
        return True
    
    def getName(self):
        result = ""
        result = self.name
        return result
    
    def setName(self, newName):
        # PDF PORT -- limited to 80 characters for some reason?
        self.name = newName[0:80]
    
    def addPoint(self, aPoint):
        result = 0
        # PDF ADDED - doing copy instead of taking it as is -- is this needed always?
        self.points.append(copy.copy(aPoint))
        return len(self.points)
    
    def removePoint(self, pointIndex):
        del self.points[pointIndex]
        self.deletePointIndexInTriangles(pointIndex)
        if self.originPointIndex > pointIndex:
            self.originPointIndex = self.originPointIndex - 1
    
    def addPointIfNoMatch(self, aPoint, matchDistance):
        for i in range(0, len(self.points)):
            if u3dsupport.KfPoint3D_matchXYZ(aPoint, self.points[i], matchDistance):
                #add 1 because triangle indexes start at 1
                return i + 1
        return self.addPoint(aPoint)
    
    def pointForIndex(self, anIndex):
        if (anIndex < 1) or (anIndex >= len(self.points)):
            raise GeneralException.create("Problem: Point index out of range in method KfObject3D.pointForIndex.")
        result = self.points[anIndex - 1]
        return result
    
    def addTriangle(self, aTriangle):
        self.triangles.append(aTriangle)
    
    # PDF PORT __ REMOVED FOR SPEED AND NOT NEEDED ANYMORE?
    #def triangleForIndex(self, anIndex):
    #    if (anIndex < 0) or (anIndex >= len(self.triangles)):
    #        raise GeneralException.create("Problem: Triangle index out of range in method KfObject3D.triangleForIndex.")
    #    result = self.triangles[anIndex]
    #    return result
    
    #adjust all points for origin, which is assumed to be at the first point
    #in terms of plant organs, this means the first point is
    #where the organ is attached to the plant
    def adjustForOrigin(self):
        if len(self.points) == 0:
            raise "no points"
        if self.originPointIndex < 0:
            self.originPointIndex = 0
        if self.originPointIndex >= len(self.points):
            self.originPointIndex = len(self.points) - 1
        for i in range(0, len(self.points)):
            if i != self.originPointIndex:
                u3dsupport.KfPoint3D_subtract(self.points[i], self.points[self.originPointIndex])
        #makes the first point zero
        u3dsupport.KfPoint3D_setXYZ(self.points[self.originPointIndex], 0.0, 0.0, 0.0)
    
    def setOriginPointIndex(self, newOriginPointIndex):
        changed = (self.originPointIndex != newOriginPointIndex)
        self.originPointIndex = newOriginPointIndex
        if changed:
            self.adjustForOrigin()
    
    def makeMirrorTriangles(self):
        newPointIndexes = [0] * 3
        self.adjustForOrigin()
        for triangle in self.triangles:
            for j in range(0, 3):
                aPoint = self.pointForIndex(triangle.pointIndexes[j])
                aPoint.x = -1 * aPoint.x
                newPointIndexes[j] = self.addPointIfNoMatch(aPoint, 1.0)
            # reversing order of points makes triangle have correct facing for opposite side
            self.addTriangle(KfIndexTriangle().createABC(newPointIndexes[2], newPointIndexes[1], newPointIndexes[0]))
    
    def reverseZValues(self):
        self.adjustForOrigin()
        for point in self.points:
            point.z = -1 * point.z
    
    def bestPointForDrawingAtScale(self, turtleProxy, origin, bitmapSize, scale):
        turtle = turtleProxy
        self.boundsRect = delphi_compatability.TRect()
        turtle.reset()
        for point in self.points:
            u3dsupport.KfPoint3D_addPointToBoundsRect(self.boundsRect, turtle.transformAndRecord(point, scale))
            # PDF FIX -- no TPOINT?
        result = delphi_compatability.TPoint()
        result.X = origin.X + bitmapSize.X / 2 - usupport.rWidth(self.boundsRect) / 2 - self.boundsRect.Left
        result.Y = origin.Y + bitmapSize.Y / 2 - usupport.rHeight(self.boundsRect) / 2 - self.boundsRect.Top
        return result
    
    def draw(self, turtleProxy, scale, longName, shortName, dxfIndex, partID):
        result = delphi_compatability.TRect()
        minZ = 0.0
        self.zForSorting = 0
        turtle = turtleProxy
        if turtle.ifExporting_exclude3DObject(scale):
            return result
        turtle.clearRecording()
        self.boundsRect = delphi_compatability.TRect()
        for point in self.points:
            u3dsupport.KfPoint3D_addPointToBoundsRect(self.boundsRect, turtle.transformAndRecord(point, scale))
        result = self.boundsRect
        if not turtle.drawOptions.draw3DObjects:
            return result
        if turtle.drawOptions.draw3DObjectsAsRects:
            turtle.drawTrianglesFromBoundsRect(self.boundsRect)
            return result
        # prepare
        turtle.ifExporting_start3DObject(longName + " 3D object", shortName, turtle.drawingSurface.foreColor, dxfIndex)
        if turtle.exportingToFile():
            # draw
            self.write3DExportElements(turtle, scale, partID)
        elif len(self.triangles) > 0:
            first = 1
            for triangle in self.triangles:
                realTriangle = turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[1], triangle.pointIndexes[2], partID)
                if (turtle.drawOptions.sortPolygons) and (turtle.drawOptions.sortTdosAsOneItem) and (realTriangle != None):
                    if first:
                        minZ = realTriangle.zForSorting
                        first= 0
                    elif realTriangle.zForSorting < minZ:
                        minZ = realTriangle.zForSorting
                    realTriangle.tdo = self
        self.zForSorting = minZ
        turtle.ifExporting_end3DObject()
        return result
    
    def overlayBoundsRect(self, turtleProxy, scale):
        turtle = turtleProxy
        oldSetting = turtle.drawingSurface.fillingTriangles
        turtle.drawingSurface.fillingTriangles = False
        turtle.drawTrianglesFromBoundsRect(self.boundsRect)
        turtle.drawingSurface.fillingTriangles = oldSetting
    
    def write3DExportElements(self, turtleProxy, scale, partID):
        firstPtIndex = 0L
        
        # do NOT pass the array on because a tdo could be really big
        # some write out lists of points then triangles; some draw each triangle
        turtle = turtleProxy
        fileExportSurface = turtle.fileExportSurface()
        if fileExportSurface == None:
            raise GeneralException.create("Problem: No 3D drawing surface in method KfObject3D.write3DExportElements.")
        if turtle.writingTo == u3dexport.k3DS:
            fileExportSurface.startVerticesAndTriangles()
            if turtle.writingToLWO():
                firstPtIndex = fileExportSurface.numPoints
            else:
                firstPtIndex = 0
            for point in self.points:
                fileExportSurface.addPoint(turtle.transformAndRecord(point, scale))
            for triangle in self.triangles:
                fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1)
            fileExportSurface.endVerticesAndTriangles()
            # PDF PORT -- added semicolon
        elif turtle.writingTo == u3dexport.kOBJ:
            fileExportSurface.startVerticesAndTriangles()
            if turtle.writingToLWO():
                firstPtIndex = fileExportSurface.numPoints
            else:
                firstPtIndex = 0
            for point in self.points:
                fileExportSurface.addPoint(turtle.transformAndRecord(point, scale))
            for triangle in self.triangles:
                fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1)
            fileExportSurface.endVerticesAndTriangles()
            # PDF PORT -- added semicolon
        elif turtle.writingTo == u3dexport.kVRML:
            fileExportSurface.startVerticesAndTriangles()
            if turtle.writingToLWO():
                firstPtIndex = fileExportSurface.numPoints
            else:
                firstPtIndex = 0
            for point in self.points:
                fileExportSurface.addPoint(turtle.transformAndRecord(point, scale))
            for triangle in self.triangles:
                fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1)
            fileExportSurface.endVerticesAndTriangles()
            # PDF PORT -- added semicolon
        elif turtle.writingTo == u3dexport.kLWO:
            fileExportSurface.startVerticesAndTriangles()
            if turtle.writingToLWO():
                firstPtIndex = fileExportSurface.numPoints
            else:
                firstPtIndex = 0
            for point in self.points:
                fileExportSurface.addPoint(turtle.transformAndRecord(point, scale))
            for triangle in self.triangles:
                fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1)
            fileExportSurface.endVerticesAndTriangles()
            # PDF PORT -- added semicolon
        else :
            for triangle in self.triangles:
                turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[1], triangle.pointIndexes[2], partID)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[2], triangle.pointIndexes[1], partID)
    
    def addTriangleWithVerticesABC(self, a, b, c):
        self.addTriangle(KfIndexTriangle().createABC(a, b, c))
    
    def removeTriangle(self, aTriangle):
        self.triangles.Remove(aTriangle)
        self.removePointsNotInUse()
    
    def removePointsNotInUse(self):
        if not len(self.points):
            return
        nextPointIndexToCheck = 0
        while nextPointIndexToCheck < len(self.points):
            if not self.pointIsReallyInUse(nextPointIndexToCheck):
                self.removePoint(nextPointIndexToCheck)
            else:
                nextPointIndexToCheck += 1
    
    def pointIsReallyInUse(self, pointIndex):
        # triangle indexes start at 1, not 0 
        adjustedPointIndex = pointIndex + 1
        for triangle in self.triangles:
            for i in range(0, 3):
                if triangle.pointIndexes[i] == adjustedPointIndex:
                    return True
        return False
    
    def deletePointIndexInTriangles(self, oldPointIndex):
        triangle = KfIndexTriangle()
        i = 0
        j = 0
        adjustedOldPointIndex = 0
        
        # triangle indexes start at 1, not 0 
        adjustedOldPointIndex = oldPointIndex + 1
        if len(self.triangles) > 0:
            for i in range(0, len(self.triangles)):
                triangle = self.triangles[i]
                for j in range(0, 3):
                    if triangle.pointIndexes[j] > adjustedOldPointIndex:
                        triangle.pointIndexes[j] = triangle.pointIndexes[j] - 1
    
    #parse string into xyz positions and add point to collection
    def addPointString(self, stream):
        aPoint3D = u3dsupport.KfPoint3D()
        x = stream.nextInteger()
        y = stream.nextInteger()
        z = stream.nextInteger()
        u3dsupport.KfPoint3D_setXYZ(aPoint3D, x, y, z)
        self.addPoint(aPoint3D)
    
    #parse string into three point indexes and add triangle to collection
    def addTriangleString(self, stream):
        p1 = stream.nextInteger()
        p2 = stream.nextInteger()
        p3 = stream.nextInteger()
        lenPoints = len(self.points)
        if (p1 == 0) or (p2 == 0) or (p3 == 0) or (p1 > lenPoints) or (p2 > lenPoints) or (p3 > lenPoints):
            MessageDialog("Bad triangle: " + IntToStr(p1) + " " + IntToStr(p2) + " " + IntToStr(p3) + ". Point indexes must be between 1 and " + IntToStr(lenPoints) + ".", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
        else:
            self.addTriangle(KfIndexTriangle().createABC(p1, p2, p3))
    
    def writeToFile(self, fileName):
        outputFile = TextFile()
        
        AssignFile(outputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(outputFile)
            self.writeToFileStream(outputFile, kStandAloneFile)
        finally:
            CloseFile(outputFile)
    
    def readFromFile(self, fileName):
        inputFile = TextFile()
        
        AssignFile(inputFile, fileName)
        try:
            # v1.5
            # PDF FIX THIS LATER _ _ COMMENTED OUT FOR NOW
            # usupport.setDecimalSeparator()
            Reset(inputFile)
            self.readFromFileStream(inputFile, kStandAloneFile)
        finally:
            CloseFile(inputFile)
    
    def writeToMemo(self, aMemo):
        aMemo.Lines.Add("  " + kStartTdoString)
        aMemo.Lines.Add("  Name=" + self.getName())
        for point in self.points:
            aMemo.Lines.Add("  Point=" + IntToStr(intround(point.x)) + " " + IntToStr(intround(point.y)) + " " + IntToStr(intround(point.z)))
        aMemo.Lines.Add("; Origin=" + IntToStr(self.originPointIndex))
        for triangle in self.triangles:
            aMemo.Lines.Add("  Triangle=" + IntToStr(triangle.pointIndexes[0]) + " " + IntToStr(triangle.pointIndexes[1]) + " " + IntToStr(triangle.pointIndexes[2]))
        aMemo.Lines.Add("  " + kEndTdoString)
    
    def writeToFileStream(self, outputFile, embeddedInPlant):
        if embeddedInPlant:
            writeln(outputFile, "  " + kStartTdoString)
        if embeddedInPlant:
            write(outputFile, "  ")
        writeln(outputFile, "Name=" + self.getName())
        for point in self.points:
            writeln(outputFile, "  Point=" + IntToStr(intround(point.x)) + " " + IntToStr(intround(point.y)) + " " + IntToStr(intround(point.z)))
        writeln(outputFile, "; Origin=" + IntToStr(self.originPointIndex))
        for triangle in self.triangles:
            writeln(outputFile, "  Triangle=" + IntToStr(triangle.pointIndexes[0]) + " " + IntToStr(triangle.pointIndexes[1]) + " " + IntToStr(triangle.pointIndexes[2]))
        if embeddedInPlant:
            writeln(outputFile, "  " + kEndTdoString)
        else:
            writeln(outputFile)
    
    def readFromFileStream(self, inputFile, embeddedInPlant):
        self.points = []
        self.originPointIndex = 0
        self.triangles.clear()
        if embeddedInPlant:
            inputLine = readln(inputFile)
            if (embeddedInPlant) and (trim(inputLine) == ""):
                # cfk change for v1.3 added '' case
                inputLine = readln(inputFile)
            if inputLine and (inputLine[0] == ";") and not string_match("ORIGIN",inputLine, find=1):
                # cfk change for v1.6b2 mistake with origin, placed with comment
                inputLine = readln(inputFile)
            if not string_match(kStartTdoString, inputLine):
                raise GeneralException.create("Problem: Expected start of 3D object.")

        #read info for 3D object from file at current position
        stream = usstream.KfStringStream()
        inputLine = readln(inputFile)
        while inputLine != None:
            if (embeddedInPlant) and (trim(inputLine) == ""):
                # cfk change v1.3 added '' case
                pass
            elif inputLine and (inputLine[0] == ";") and (not string_match("ORIGIN", inputLine, find=1)):
                # cfk change for v1.6b2 mistake with origin, placed with comment
                pass
            elif (not embeddedInPlant) and (string_match("[", inputLine, find=1)):
                #ignore old thing in brackets
                pass
            else:
                stream.onStringSeparator(inputLine, "=")
                fieldType = stream.nextToken()
                stream.spaceSeparator()
                if string_match("POINT", fieldType):
                    self.addPointString(stream)
                elif string_match("ORIGIN", fieldType, find=1):
                    self.setOriginPointIndex(StrToIntDef(stream.remainder, 0))
                elif string_match("TRIANGLE", fieldType):
                    self.addTriangleString(stream)
                elif string_match("NAME", fieldType):
                    self.setName(stream.remainder)
                else:
                    break
            inputLine = readln(inputFile)
        self.adjustForOrigin()
        if embeddedInPlant:
            if not string_match(kEndTdoString, inputLine):
                raise GeneralException.create("Problem: Expected end of 3D object.")

    
    def readFromDXFFile(self, inputFile):
        newPoints = [KfPoint3D(), KfPoint3D(), KfPoint3D()]
        newTriangleIndexes = [0, 0, 0]
        self.points = []
        self.originPointIndex = 0
        pointsRead = 0
        self.triangles.clear()
        newPoints[0].x = 0
        newPoints[0].y = 0
        newPoints[0].z = 0
        newPoints[1].x = 0
        newPoints[1].y = 0
        newPoints[1].z = 0
        newPoints[2].x = 0
        newPoints[2].y = 0
        newPoints[2].z = 0
        
        identifierLine = readln(inputFile)
        while identifierLine != None:
            identifierLine = trim(identifierLine)
            valueLine = readln(inputFile)
            if valueLine == None:
                # PDF PORT -- unexpected case
                break
            valueLine = trim(valueLine)
            if identifierLine == "10":
                # v1.60final changed this from else to all ifs; something wrong in Delphi, I think
                # first point
                newPoints[0].x = StrToFloat(valueLine)
            if identifierLine == "20":
                newPoints[0].y = -1 * StrToFloat(valueLine)
            if identifierLine == "30":
                newPoints[0].z = StrToFloat(valueLine)
            if identifierLine == "11":
                # second point
                newPoints[1].x = StrToFloat(valueLine)
            if identifierLine == "21":
                newPoints[1].y = -1 * StrToFloat(valueLine)
            if identifierLine == "31":
                newPoints[1].z = StrToFloat(valueLine)
            if identifierLine == "12":
                # third point
                newPoints[2].x = StrToFloat(valueLine)
            if identifierLine == "22":
                newPoints[2].y = -1 * StrToFloat(valueLine)
            if identifierLine == "32":
                newPoints[2].z = StrToFloat(valueLine)
            if identifierLine == "13":
                # end (ignoring fourth point)
                pointsRead += 3
                # make new triangle
                newTriangleIndexes[0] = self.addPointIfNoMatch(newPoints[0], 0.1)
                newTriangleIndexes[1] = self.addPointIfNoMatch(newPoints[1], 0.1)
                newTriangleIndexes[2] = self.addPointIfNoMatch(newPoints[2], 0.1)
                self.addTriangle(KfIndexTriangle().createABC(newTriangleIndexes[0], newTriangleIndexes[1], newTriangleIndexes[2]))
                # reset points for next time
                newPoints[0].x = 0
                newPoints[0].y = 0
                newPoints[0].z = 0
                newPoints[1].x = 0
                newPoints[1].y = 0
                newPoints[1].z = 0
                newPoints[2].x = 0
                newPoints[2].y = 0
                newPoints[2].z = 0
            identifierLine = readln(inputFile)
        self.adjustForOrigin()
    
    def readFromMemo(self, aMemo, readingMemoLine):
        inputLine = ""
        fieldType = ""
        stream = KfStringStream()
        
        self.pointss = []
        self.originPointIndex = 0
        self.triangles.clear()
        inputLine = aMemo.Lines.Strings[readingMemoLine]
        readingMemoLine += 1
        if trim(inputLine) == "":
            # cfk change v1.60final added '' case
            # skip commented lines 
            inputLine = aMemo.Lines.Strings[readingMemoLine]
            readingMemoLine += 1
        if inputLine and (inputLine[0] == ";") and (not string_match("ORIGIN", inputLine, find=1)):
            # cfk change for v1.6b2 mistake with origin, placed with comment
            # skip commented lines 
            inputLine = aMemo.Lines.Strings[readingMemoLine]
            readingMemoLine += 1
        if not string_match(kStartTdoString, inputLine):
            raise GeneralException.create("Problem: Expected start of 3D object.")
        stream = None
        try:
            #read info for 3D object from file at current position
            stream = usstream.KfStringStream.create
            while readingMemoLine <= len(aMemo.Lines) - 1:
                inputLine = aMemo.Lines.Strings[readingMemoLine]
                readingMemoLine += 1
                if trim(inputLine) == "":
                    # cfk change v1.60final added '' case
                    continue
                if inputLine and (inputLine[0] == ";") and (not string_match("ORIGIN", inputLine, find=1)):
                    # cfk change for v1.6b2 mistake with origin, placed with comment
                    # skip commented lines 
                    continue
                stream.onStringSeparator(inputLine, "=")
                fieldType = stream.nextToken()
                stream.spaceSeparator()
                if string_match("POINT", fieldType):
                    self.addPointString(stream)
                elif string_match("ORIGIN", fieldType, find=1):
                    self.setOriginPointIndex(StrToIntDef(stream.remainder, 0))
                elif string_match("TRIANGLE", fieldType):
                    self.addTriangleString(stream)
                elif string_match("NAME", fieldType):
                    self.setName(stream.remainder)
                else:
                    break
            self.adjustForOrigin()
            if not string_match(kEndTdoString, inputLine):
                raise GeneralException.create("Problem: Expected end of 3D object.")
        finally:
            stream.free
        return readingMemoLine
    
    def readFromInputString(self, aString, doAdjustForOrigin):
        part = ""
        firstLetter = ""
        stream = KfStringStream()
        partStream = KfStringStream()
        
        # format is n[name],p[# # #],p[# # #],p[# # #],t[# # #],t[# # #],t[# # #] 
        self.points = []
        self.originPointIndex = 0
        self.triangles.clear()
        stream = usstream.KfStringStream.create
        partStream = usstream.KfStringStream.create
        try:
            stream.onStringSeparator(aString, ",")
            part = "none"
            while part != "":
                part = stream.nextToken()
                firstLetter = UNRESOLVED.copy(part, 1, 1)
                if uppercase(firstLetter) == "N":
                    self.setName(betweenBrackets(part))
                elif uppercase(firstLetter) == "P":
                    partStream.onStringSeparator(betweenBrackets(part), " ")
                    self.addPointString(partStream)
                elif uppercase(firstLetter) == "T":
                    partStream.onStringSeparator(betweenBrackets(part), " ")
                    self.addTriangleString(partStream)
            if doAdjustForOrigin:
                self.adjustForOrigin()
        finally:
            stream.free
            partStream.free
    
    # ------------------------------------------------------------------------- data transfer for binary copy 
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kKfObject3D
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        i = 0
        tempPoint = KfPoint3d()
        
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.name = filer.streamShortString(self.name)
        pointsInUse = len(self.points)
        pointsInUse = filer.streamLongint(pointsInUse)
        self.originPointIndex = filer.streamLongint(self.originPointIndex)
        if pointsInUse > 0:
            for i in range(0, pointsInUse):
                if filer.isWriting():
                    tempPoint = self.points[i]
                tempPoint = filer.streamBytes(tempPoint, FIX_sizeof(tempPoint))
                if filer.isReading():
                    self.points[i] = tempPoint
        if filer.isReading():
            #may have triangles already, because we are keeping them around now
            self.triangles.clear()
        self.triangles.streamUsingFiler(filer, KfIndexTriangle)
    
    def totalMemorySize(self):
        # PDF FIX THIS
        result = self.instanceSize
        result = result + self.triangles.instanceSize
        if len(self.triangles) > 0:
            for i in range(0, len(self.triangles)):
                result = result + KfIndexTriangle(self.triangles[i]).instanceSize
        result = result + len(pointData) * FIX_sizeof(KfPoint3D)
        return result
    
    def writeToDXFFile(self, fileName, frontFaceColor, backFaceColor):
        outputFile = TextFile()
        i = 0
        triangle = KfIndexTriangle()
        colorToDraw = UnassignedColor
        
        AssignFile(outputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(outputFile)
            writeln(outputFile, "0")
            writeln(outputFile, "SECTION")
            writeln(outputFile, "2")
            writeln(outputFile, "ENTITIES")
            for triangle in self.triangles:
                if self.triangleIsBackFacing(triangle):
                    colorToDraw = backFaceColor
                else:
                    colorToDraw = frontFaceColor
                self.writeTriangleToDXFFIle(outputFile, self.points[triangle.pointIndexes[0] - 1], self.points[triangle.pointIndexes[1] - 1], self.points[triangle.pointIndexes[2] - 1], colorToDraw)
            writeln(outputFile, "0")
            writeln(outputFile, "ENDSEC")
            writeln(outputFile, "0")
            writeln(outputFile, "EOF")
        finally:
            CloseFile(outputFile)
    
    def writeTriangleToDXFFIle(self, outputFile, p1, p2, p3, color):
        writeln(outputFile, "0")
        writeln(outputFile, "3DFACE")
        writeln(outputFile, "8")
        writeln(outputFile, "3dObject")
        writeln(outputFile, "62")
        writeln(outputFile, IntToStr(color))
        # v1.60final changed intToStr(round(p|.|)) to digitValueString(p|.|)
        # can't see that there was ever any reason to round these; it's probably left over from
        # when I didn't understand DXF very well
        writeln(outputFile, "10")
        writeln(outputFile, usupport.digitValueString(p1.x))
        writeln(outputFile, "20")
        writeln(outputFile, usupport.digitValueString(-p1.y))
        writeln(outputFile, "30")
        writeln(outputFile, usupport.digitValueString(p1.z))
        writeln(outputFile, "11")
        writeln(outputFile, usupport.digitValueString(p2.x))
        writeln(outputFile, "21")
        writeln(outputFile, usupport.digitValueString(-p2.y))
        writeln(outputFile, "31")
        writeln(outputFile, usupport.digitValueString(p2.z))
        writeln(outputFile, "12")
        writeln(outputFile, usupport.digitValueString(p3.x))
        writeln(outputFile, "22")
        writeln(outputFile, usupport.digitValueString(-p3.y))
        writeln(outputFile, "32")
        writeln(outputFile, usupport.digitValueString(p3.z))
        writeln(outputFile, "13")
        writeln(outputFile, usupport.digitValueString(p3.x))
        writeln(outputFile, "23")
        writeln(outputFile, usupport.digitValueString(-p3.y))
        writeln(outputFile, "33")
        writeln(outputFile, usupport.digitValueString(p3.z))
    
    def writeToPOV_INCFile(self, fileName, frontFaceColor, embeddedInPlant, rotateCount):
        outputFile = TextFile()
        i = 0
        triangle = KfIndexTriangle()
        colorToDraw = UnassignedColor
        nameString = ""
        
        AssignFile(outputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(outputFile)
            nameString = usupport.replacePunctuationWithUnderscores(self.getName())
            writeln(outputFile, "// POV-format INC file of PlantStudio v1.x 3D object")
            writeln(outputFile, "//     \"" + self.getName() + "\"")
            if (not embeddedInPlant):
                writeln(outputFile, "// include this file in a POV file thus to use it:")
                writeln(outputFile, "//     #include \"" + usupport.stringUpTo(ExtractFileName(fileName), ".") + ".inc\"")
                writeln(outputFile, "//     object { " + nameString + " }")
                if rotateCount > 1:
                    writeln(outputFile, "//  or")
                    writeln(outputFile, "//     object { " + nameString + "_rotated }")
                writeln(outputFile)
            writeln(outputFile, "#declare " + nameString + "=mesh {")
            for triangle in self.triangles:
                self.writeTriangleToPOV_INCFIle(outputFile, self.points[triangle.pointIndexes[0] - 1], self.points[triangle.pointIndexes[1] - 1], self.points[triangle.pointIndexes[2] - 1])
            writeln(outputFile, chr(9) + "pigment { color rgb <" + usupport.digitValueString(UNRESOLVED.getRValue(frontFaceColor) / 256.0) + ", " + usupport.digitValueString(UNRESOLVED.getGValue(frontFaceColor) / 256.0) + ", " + usupport.digitValueString(UNRESOLVED.getBValue(frontFaceColor) / 256.0) + "> }")
            writeln(outputFile, "}")
            if rotateCount > 1:
                writeln(outputFile)
                writeln(outputFile, "#declare " + nameString + "_rotated=union {")
                writeln(outputFile, chr(9) + "object { " + nameString + " }")
                for i in range(1, rotateCount):
                    writeln(outputFile, chr(9) + "object { " + nameString + " rotate " + IntToStr(i) + "*365/" + IntToStr(rotateCount) + "*y }")
                writeln(outputFile, "}")
        finally:
            CloseFile(outputFile)
    
    def writeTriangleToPOV_INCFIle(self, outputFile, p1, p2, p3):
        write(outputFile, chr(9) + "triangle { <")
        # all y values must be negative because it seems our coordinate systems are different
        write(outputFile, IntToStr(intround(p1.x)) + ", " + IntToStr(-intround(p1.y)) + ", " + IntToStr(intround(p1.z)) + ">, <")
        write(outputFile, IntToStr(intround(p2.x)) + ", " + IntToStr(-intround(p2.y)) + ", " + IntToStr(intround(p2.z)) + ">, <")
        writeln(outputFile, IntToStr(intround(p3.x)) + ", " + IntToStr(-intround(p3.y)) + ", " + IntToStr(intround(p3.z)) + "> }")
    
    def triangleIsBackFacing(self, aTriangle):
        result = False
        point0 = self.points[aTriangle.pointIndexes[0] - 1]
        point1 = self.points[aTriangle.pointIndexes[1] - 1]
        point2 = self.points[aTriangle.pointIndexes[2] - 1]
        backfacingResult = ((point1.x - point0.x) * (point2.y - point0.y)) - ((point1.y - point0.y) * (point2.x - point0.x))
        result = (backfacingResult < 0)
        return result

