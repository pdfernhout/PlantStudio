// unit uamendmt

from conversion_common import *;
import usupport;
import uplant;
import ufiler;
import delphi_compatability;

// const
kStartAmendmentString = "start posing change";
kEndAmendmentString = "end posing change";



class PdPlantDrawingAmendment extends PdStreamableObject {
    public long partID;
    public String typeOfPart;
    public boolean hide;
    public boolean changeColors;
    public boolean propagateColors;
    public TColorRef faceColor;
    public TColorRef backfaceColor;
    public TColorRef lineColor;
    public boolean addRotations;
    public float xRotation;
    public float yRotation;
    public float zRotation;
    public boolean multiplyScale;
    public boolean propagateScale;
    public short scaleMultiplier_pct;
    public short lengthMultiplier_pct;
    public short widthMultiplier_pct;
    public short applyAtAge;
    
    public void create() {
        this.scaleMultiplier_pct = 100;
        this.lengthMultiplier_pct = 100;
        this.widthMultiplier_pct = 100;
        this.xRotation = 0;
        this.yRotation = 0;
        this.zRotation = 0;
        this.faceColor = usupport.support_rgb(50, 200, 50);
        this.backfaceColor = usupport.support_rgb(20, 150, 20);
        this.lineColor = usupport.support_rgb(40, 100, 40);
    }
    
    public void readFromTextFile(TextFile inputFile) {
        String inputLine = "";
        String varName = "";
        String varValue = "";
        
        while (!UNRESOLVED.eof(inputFile)) {
            // plant reads start line; just continue from there
            UNRESOLVED.readln(inputFile, inputLine);
            if ((trim(inputLine) == "")) {
                continue;
            }
            varName = usupport.stringUpTo(inputLine, "=");
            varValue = usupport.stringBeyond(inputLine, "=");
            if (!this.setField(varName, varValue)) {
                break;
            }
        }
        if (UNRESOLVED.pos(uppercase(kEndAmendmentString), uppercase(inputLine)) <= 0) {
            throw new GeneralException.create("Problem: Expected end of posing change.");
        }
    }
    
    public void readFromMemo(TMemo aMemo, long readingMemoLine) {
        String inputLine = "";
        String varName = "";
        String varValue = "";
        
        while (readingMemoLine <= aMemo.Lines.Count - 1) {
            // plant reads start line; just continue from there
            inputLine = aMemo.Lines.Strings[readingMemoLine];
            if ((trim(inputLine) == "")) {
                continue;
            }
            varName = usupport.stringUpTo(inputLine, "=");
            varValue = usupport.stringBeyond(inputLine, "=");
            if (!this.setField(varName, varValue)) {
                break;
            }
            readingMemoLine += 1;
        }
        if (UNRESOLVED.pos(uppercase(kEndAmendmentString), uppercase(inputLine)) <= 0) {
            throw new GeneralException.create("Problem: Expected end of posing change.");
        }
        return readingMemoLine;
    }
    
    public boolean setField(String varName, String varValue) {
        result = false;
        result = true;
        if (UNRESOLVED.pos("part number", varName) > 0) {
            // how deal with problem?
            this.partID = StrToIntDef(varValue, 0);
        } else if (UNRESOLVED.pos("part type", varName) > 0) {
            this.typeOfPart = varValue;
        } else if (UNRESOLVED.pos("hide", varName) > 0) {
            this.hide = usupport.strToBool(varValue);
        } else if (UNRESOLVED.pos("change colors", varName) > 0) {
            // read these for possible backward compatibility later, but don't do anything with them
            // self.changeColors := strToBool(varValue)
            result = true;
        } else if (UNRESOLVED.pos("propagate colors up stem", varName) > 0) {
            // self.propagateColors := strToBool(varValue)
            result = true;
        } else if (UNRESOLVED.pos("front face color", varName) > 0) {
            // self.faceColor := strToIntDef(varValue, 0)
            result = true;
        } else if (UNRESOLVED.pos("back face color", varName) > 0) {
            // self.backfaceColor := strToIntDef(varValue, 0)
            result = true;
        } else if (UNRESOLVED.pos("line color", varName) > 0) {
            // self.lineColor := strToIntDef(varValue, 0)
            result = true;
        } else if (UNRESOLVED.pos("rotate", varName) > 0) {
            this.addRotations = usupport.strToBool(varValue);
        } else if (UNRESOLVED.pos("x rotation", varName) > 0) {
            this.xRotation = StrToInt(varValue) * 1.0;
        } else if (UNRESOLVED.pos("y rotation", varName) > 0) {
            this.yRotation = StrToInt(varValue) * 1.0;
        } else if (UNRESOLVED.pos("z rotation", varName) > 0) {
            this.zRotation = StrToInt(varValue) * 1.0;
        } else if (UNRESOLVED.pos("change scale", varName) > 0) {
            this.multiplyScale = usupport.strToBool(varValue);
        } else if (UNRESOLVED.pos("propagate scale change up stem", varName) > 0) {
            this.propagateScale = usupport.strToBool(varValue);
        } else if (UNRESOLVED.pos("3d object scale multiplier", varName) > 0) {
            this.scaleMultiplier_pct = StrToIntDef(varValue, 100);
        } else if (UNRESOLVED.pos("line length multiplier", varName) > 0) {
            this.lengthMultiplier_pct = StrToIntDef(varValue, 100);
        } else if (UNRESOLVED.pos("line width multiplier", varName) > 0) {
            this.widthMultiplier_pct = StrToIntDef(varValue, 100);
        } else if (UNRESOLVED.pos("apply at age", varName) > 0) {
            // read these for possible backward compatibility later, but don't do anything with them
            // self.applyAtAge := strToIntDef(varValue, 0)
            result = true;
        } else {
            result = false;
        }
        return result;
    }
    
    public void writeToTextFile(TextFile outputFile) {
        writeln(outputFile, kStartAmendmentString);
        writeln(outputFile, "  part number =" + IntToStr(this.partID));
        writeln(outputFile, "  part type =" + this.typeOfPart);
        writeln(outputFile, "  hide =" + usupport.boolToStr(this.hide));
        //
        //  writeln(outputFile, '  change colors =' + boolToStr(changeColors));
        //  writeln(outputFile, '  propagate colors up stem =' + boolToStr(propagateColors));
        //  writeln(outputFile, '  front face color =' + intToStr(faceColor));
        //  writeln(outputFile, '  back face color =' + intToStr(backfaceColor));
        //  writeln(outputFile, '  line color =' + intToStr(lineColor));
        //  
        writeln(outputFile, "  rotate =" + usupport.boolToStr(this.addRotations));
        writeln(outputFile, "  x rotation =" + IntToStr(intround(this.xRotation)));
        writeln(outputFile, "  y rotation =" + IntToStr(intround(this.yRotation)));
        writeln(outputFile, "  z rotation =" + IntToStr(intround(this.zRotation)));
        writeln(outputFile, "  change scale =" + usupport.boolToStr(this.multiplyScale));
        writeln(outputFile, "  propagate scale change up stem =" + usupport.boolToStr(this.propagateScale));
        writeln(outputFile, "  3d object scale multiplier =" + IntToStr(this.scaleMultiplier_pct));
        writeln(outputFile, "  line length multiplier =" + IntToStr(this.lengthMultiplier_pct));
        writeln(outputFile, "  line width multiplier =" + IntToStr(this.widthMultiplier_pct));
        //
        //  writeln(outputFile, '  apply at age =' + intToStr(applyAtAge));
        //  
        writeln(outputFile, kEndAmendmentString);
    }
    
    public void writeToMemo(TMemo aMemo) {
        aMemo.Lines.Add(kStartAmendmentString);
        aMemo.Lines.Add("  part number =" + IntToStr(this.partID));
        aMemo.Lines.Add("  part type =" + this.typeOfPart);
        aMemo.Lines.Add("  hide =" + usupport.boolToStr(this.hide));
        //
        //  aMemo.lines.add('  change colors =' + boolToStr(changeColors));
        //  aMemo.lines.add('  propagate colors up stem =' + boolToStr(propagateColors));
        //  aMemo.lines.add('  front face color =' + intToStr(faceColor));
        //  aMemo.lines.add('  back face color =' + intToStr(backfaceColor));
        //  aMemo.lines.add('  line color =' + intToStr(lineColor));
        //  
        aMemo.Lines.Add("  rotate =" + usupport.boolToStr(this.addRotations));
        aMemo.Lines.Add("  x rotation =" + IntToStr(intround(this.xRotation)));
        aMemo.Lines.Add("  y rotation =" + IntToStr(intround(this.yRotation)));
        aMemo.Lines.Add("  z rotation =" + IntToStr(intround(this.zRotation)));
        aMemo.Lines.Add("  change scale =" + usupport.boolToStr(this.multiplyScale));
        aMemo.Lines.Add("  propagate scale change up stem =" + usupport.boolToStr(this.propagateScale));
        aMemo.Lines.Add("  3d object scale multiplier =" + IntToStr(this.scaleMultiplier_pct));
        aMemo.Lines.Add("  line length multiplier =" + IntToStr(this.lengthMultiplier_pct));
        aMemo.Lines.Add("  line width multiplier =" + IntToStr(this.widthMultiplier_pct));
        //
        //  aMemo.lines.add('  apply at age =' + intToStr(applyAtAge));
        //  
        aMemo.Lines.Add(kEndAmendmentString);
    }
    
    public String getFullName() {
        result = "";
        result = IntToStr(this.partID) + " (" + this.typeOfPart + ")";
        if (this.hide) {
            result = result + ", hidden";
        }
        if (this.changeColors) {
            result = result + ", colored";
        }
        if (this.addRotations) {
            result = result + ", rotated";
        }
        if (this.multiplyScale) {
            result = result + ", scaled";
        }
        if (this.applyAtAge != 0) {
            result = result + " at age " + IntToStr(this.applyAtAge);
        }
        return result;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        super.streamDataWithFiler(filer, cvir);
        this.partID = filer.streamLongint(this.partID);
        this.typeOfPart = filer.streamShortString(this.typeOfPart);
        this.hide = filer.streamBoolean(this.hide);
        this.changeColors = filer.streamBoolean(this.changeColors);
        this.propagateColors = filer.streamBoolean(this.propagateColors);
        filer.streamColorRef(this.faceColor);
        filer.streamColorRef(this.backfaceColor);
        filer.streamColorRef(this.lineColor);
        this.addRotations = filer.streamBoolean(this.addRotations);
        this.xRotation = filer.streamSingle(this.xRotation);
        this.yRotation = filer.streamSingle(this.yRotation);
        this.zRotation = filer.streamSingle(this.zRotation);
        this.multiplyScale = filer.streamBoolean(this.multiplyScale);
        this.propagateScale = filer.streamBoolean(this.propagateScale);
        this.scaleMultiplier_pct = filer.streamSmallint(this.scaleMultiplier_pct);
        this.lengthMultiplier_pct = filer.streamSmallint(this.lengthMultiplier_pct);
        this.widthMultiplier_pct = filer.streamSmallint(this.widthMultiplier_pct);
        this.applyAtAge = filer.streamSmallint(this.applyAtAge);
    }
    
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kPdPlantDrawingAmendment;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
}
