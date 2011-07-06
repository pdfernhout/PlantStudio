# unit uamendmt

from conversion_common import *
import uclasses
import usupport
import uplant
import ufiler
import delphi_compatability

# const
kStartAmendmentString = "start posing change"
kEndAmendmentString = "end posing change"

class PdPlantDrawingAmendment(PdStreamableObject):
    def __init__(self):
        self.partID = 0L
        self.typeOfPart = ""
        self.hide = false
        self.changeColors = false
        self.propagateColors = false
        self.faceColor = TColorRef()
        self.backfaceColor = TColorRef()
        self.lineColor = TColorRef()
        self.addRotations = false
        self.xRotation = 0.0
        self.yRotation = 0.0
        self.zRotation = 0.0
        self.multiplyScale = false
        self.propagateScale = false
        self.scaleMultiplier_pct = 0
        self.lengthMultiplier_pct = 0
        self.widthMultiplier_pct = 0
        self.applyAtAge = 0
    
    def create(self):
        self.scaleMultiplier_pct = 100
        self.lengthMultiplier_pct = 100
        self.widthMultiplier_pct = 100
        self.xRotation = 0
        self.yRotation = 0
        self.zRotation = 0
        self.faceColor = usupport.support_rgb(50, 200, 50)
        self.backfaceColor = usupport.support_rgb(20, 150, 20)
        self.lineColor = usupport.support_rgb(40, 100, 40)
        return self
    
    def readFromTextFile(self, inputFile):
        inputLine = ""
        varName = ""
        varValue = ""
        
        while not UNRESOLVED.eof(inputFile):
            # plant reads start line; just continue from there
            UNRESOLVED.readln(inputFile, inputLine)
            if (trim(inputLine) == ""):
                continue
            varName = usupport.stringUpTo(inputLine, "=")
            varValue = usupport.stringBeyond(inputLine, "=")
            if not self.setField(varName, varValue):
                break
        if UNRESOLVED.pos(uppercase(kEndAmendmentString), uppercase(inputLine)) <= 0:
            raise GeneralException.create("Problem: Expected end of posing change.")
    
    def readFromMemo(self, aMemo, readingMemoLine):
        inputLine = ""
        varName = ""
        varValue = ""
        
        while readingMemoLine <= aMemo.Lines.Count - 1:
            # plant reads start line; just continue from there
            inputLine = aMemo.Lines.Strings[readingMemoLine]
            if (trim(inputLine) == ""):
                continue
            varName = usupport.stringUpTo(inputLine, "=")
            varValue = usupport.stringBeyond(inputLine, "=")
            if not self.setField(varName, varValue):
                break
            readingMemoLine += 1
        if UNRESOLVED.pos(uppercase(kEndAmendmentString), uppercase(inputLine)) <= 0:
            raise GeneralException.create("Problem: Expected end of posing change.")
        return readingMemoLine
    
    def setField(self, varName, varValue):
        result = false
        result = true
        if UNRESOLVED.pos("part number", varName) > 0:
            # how deal with problem?
            self.partID = StrToIntDef(varValue, 0)
        elif UNRESOLVED.pos("part type", varName) > 0:
            self.typeOfPart = varValue
        elif UNRESOLVED.pos("hide", varName) > 0:
            self.hide = usupport.strToBool(varValue)
        elif UNRESOLVED.pos("change colors", varName) > 0:
            # read these for possible backward compatibility later, but don't do anything with them
            # self.changeColors := strToBool(varValue)
            result = true
        elif UNRESOLVED.pos("propagate colors up stem", varName) > 0:
            # self.propagateColors := strToBool(varValue)
            result = true
        elif UNRESOLVED.pos("front face color", varName) > 0:
            # self.faceColor := strToIntDef(varValue, 0)
            result = true
        elif UNRESOLVED.pos("back face color", varName) > 0:
            # self.backfaceColor := strToIntDef(varValue, 0)
            result = true
        elif UNRESOLVED.pos("line color", varName) > 0:
            # self.lineColor := strToIntDef(varValue, 0)
            result = true
        elif UNRESOLVED.pos("rotate", varName) > 0:
            self.addRotations = usupport.strToBool(varValue)
        elif UNRESOLVED.pos("x rotation", varName) > 0:
            self.xRotation = StrToInt(varValue) * 1.0
        elif UNRESOLVED.pos("y rotation", varName) > 0:
            self.yRotation = StrToInt(varValue) * 1.0
        elif UNRESOLVED.pos("z rotation", varName) > 0:
            self.zRotation = StrToInt(varValue) * 1.0
        elif UNRESOLVED.pos("change scale", varName) > 0:
            self.multiplyScale = usupport.strToBool(varValue)
        elif UNRESOLVED.pos("propagate scale change up stem", varName) > 0:
            self.propagateScale = usupport.strToBool(varValue)
        elif UNRESOLVED.pos("3d object scale multiplier", varName) > 0:
            self.scaleMultiplier_pct = StrToIntDef(varValue, 100)
        elif UNRESOLVED.pos("line length multiplier", varName) > 0:
            self.lengthMultiplier_pct = StrToIntDef(varValue, 100)
        elif UNRESOLVED.pos("line width multiplier", varName) > 0:
            self.widthMultiplier_pct = StrToIntDef(varValue, 100)
        elif UNRESOLVED.pos("apply at age", varName) > 0:
            # read these for possible backward compatibility later, but don't do anything with them
            # self.applyAtAge := strToIntDef(varValue, 0)
            result = true
        else:
            result = false
        return result
    
    def writeToTextFile(self, outputFile):
        writeln(outputFile, kStartAmendmentString)
        writeln(outputFile, "  part number =" + IntToStr(self.partID))
        writeln(outputFile, "  part type =" + self.typeOfPart)
        writeln(outputFile, "  hide =" + usupport.boolToStr(self.hide))
        #
        #  writeln(outputFile, '  change colors =' + boolToStr(changeColors));
        #  writeln(outputFile, '  propagate colors up stem =' + boolToStr(propagateColors));
        #  writeln(outputFile, '  front face color =' + intToStr(faceColor));
        #  writeln(outputFile, '  back face color =' + intToStr(backfaceColor));
        #  writeln(outputFile, '  line color =' + intToStr(lineColor));
        #  
        writeln(outputFile, "  rotate =" + usupport.boolToStr(self.addRotations))
        writeln(outputFile, "  x rotation =" + IntToStr(intround(self.xRotation)))
        writeln(outputFile, "  y rotation =" + IntToStr(intround(self.yRotation)))
        writeln(outputFile, "  z rotation =" + IntToStr(intround(self.zRotation)))
        writeln(outputFile, "  change scale =" + usupport.boolToStr(self.multiplyScale))
        writeln(outputFile, "  propagate scale change up stem =" + usupport.boolToStr(self.propagateScale))
        writeln(outputFile, "  3d object scale multiplier =" + IntToStr(self.scaleMultiplier_pct))
        writeln(outputFile, "  line length multiplier =" + IntToStr(self.lengthMultiplier_pct))
        writeln(outputFile, "  line width multiplier =" + IntToStr(self.widthMultiplier_pct))
        #
        #  writeln(outputFile, '  apply at age =' + intToStr(applyAtAge));
        #  
        writeln(outputFile, kEndAmendmentString)
    
    def writeToMemo(self, aMemo):
        aMemo.Lines.Add(kStartAmendmentString)
        aMemo.Lines.Add("  part number =" + IntToStr(self.partID))
        aMemo.Lines.Add("  part type =" + self.typeOfPart)
        aMemo.Lines.Add("  hide =" + usupport.boolToStr(self.hide))
        #
        #  aMemo.lines.add('  change colors =' + boolToStr(changeColors));
        #  aMemo.lines.add('  propagate colors up stem =' + boolToStr(propagateColors));
        #  aMemo.lines.add('  front face color =' + intToStr(faceColor));
        #  aMemo.lines.add('  back face color =' + intToStr(backfaceColor));
        #  aMemo.lines.add('  line color =' + intToStr(lineColor));
        #  
        aMemo.Lines.Add("  rotate =" + usupport.boolToStr(self.addRotations))
        aMemo.Lines.Add("  x rotation =" + IntToStr(intround(self.xRotation)))
        aMemo.Lines.Add("  y rotation =" + IntToStr(intround(self.yRotation)))
        aMemo.Lines.Add("  z rotation =" + IntToStr(intround(self.zRotation)))
        aMemo.Lines.Add("  change scale =" + usupport.boolToStr(self.multiplyScale))
        aMemo.Lines.Add("  propagate scale change up stem =" + usupport.boolToStr(self.propagateScale))
        aMemo.Lines.Add("  3d object scale multiplier =" + IntToStr(self.scaleMultiplier_pct))
        aMemo.Lines.Add("  line length multiplier =" + IntToStr(self.lengthMultiplier_pct))
        aMemo.Lines.Add("  line width multiplier =" + IntToStr(self.widthMultiplier_pct))
        #
        #  aMemo.lines.add('  apply at age =' + intToStr(applyAtAge));
        #  
        aMemo.Lines.Add(kEndAmendmentString)
    
    def getFullName(self):
        result = ""
        result = IntToStr(self.partID) + " (" + self.typeOfPart + ")"
        if self.hide:
            result = result + ", hidden"
        if self.changeColors:
            result = result + ", colored"
        if self.addRotations:
            result = result + ", rotated"
        if self.multiplyScale:
            result = result + ", scaled"
        if self.applyAtAge != 0:
            result = result + " at age " + IntToStr(self.applyAtAge)
        return result
    
    def streamDataWithFiler(self, filer, cvir):
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.partID = filer.streamLongint(self.partID)
        self.typeOfPart = filer.streamShortString(self.typeOfPart)
        self.hide = filer.streamBoolean(self.hide)
        self.changeColors = filer.streamBoolean(self.changeColors)
        self.propagateColors = filer.streamBoolean(self.propagateColors)
        filer.streamColorRef(self.faceColor)
        filer.streamColorRef(self.backfaceColor)
        filer.streamColorRef(self.lineColor)
        self.addRotations = filer.streamBoolean(self.addRotations)
        self.xRotation = filer.streamSingle(self.xRotation)
        self.yRotation = filer.streamSingle(self.yRotation)
        self.zRotation = filer.streamSingle(self.zRotation)
        self.multiplyScale = filer.streamBoolean(self.multiplyScale)
        self.propagateScale = filer.streamBoolean(self.propagateScale)
        self.scaleMultiplier_pct = filer.streamSmallint(self.scaleMultiplier_pct)
        self.lengthMultiplier_pct = filer.streamSmallint(self.lengthMultiplier_pct)
        self.widthMultiplier_pct = filer.streamSmallint(self.widthMultiplier_pct)
        self.applyAtAge = filer.streamSmallint(self.applyAtAge)
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdPlantDrawingAmendment
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
