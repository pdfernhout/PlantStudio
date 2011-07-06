// unit upart

from conversion_common import *;
import umain;
import udomain;
import u3dsupport;
import u3dexport;
import uturtle;
import utravers;
import uamendmt;
import utdo;
import ufiler;
import usupport;
import umath;
import uplant;
import delphi_compatability;

// const
kAddingBiomassToPlant = true;
kRemovingBiomassFromPlant = false;
kDontTaper = -1.0;
kUseAmendment = true;
kDontUseAmendment = false;


// const
kDrawingTdo = true;
kDrawingLine = false;
kRotateX = 0;
kRotateY = 1;
kRotateZ = 2;


// const
kMaxLineOutputPoints = 200;



class PdPlantPart extends PdStreamableObject {
    public PdPlant plant;
    public float liveBiomass_pctMPB;
    public float deadBiomass_pctMPB;
    public float biomassDemand_pctMPB;
    public short gender;
    public long age;
    public float randomSwayIndex;
    public boolean hasFallenOff;
    public boolean isSeedlingLeaf;
    public long partID;
    public TRect boundsRect;
    public PdPlantDrawingAmendment amendment;
    public PdPlantDrawingAmendment parentAmendment;
    public float biomassOfMeAndAllPartsAboveMe_pctMPB;
    
    // ---------------------------------------------------------------------------------- initialize 
    public void initialize(PdPlant thePlant) {
        //initialize generic plant part
        this.plant = thePlant;
        // v1.6b1
        this.plant.partsCreated += 1;
        this.partID = this.plant.partsCreated;
        this.age = 0;
        this.gender = uplant.kGenderFemale;
        this.hasFallenOff = false;
        this.randomSwayIndex = this.plant.randomNumberGenerator.zeroToOne();
    }
    
    public void nextDay() {
        //next day procedure for generic plant part
        this.age += 1;
    }
    
    public String getName() {
        result = "";
        // subclasses should override
        result = "plant part";
        return result;
    }
    
    public String getFullName() {
        result = "";
        result = "part " + IntToStr(this.partID) + " (" + this.getName() + ")";
        return result;
    }
    
    // ---------------------------------------------------------------------------------- traversing 
    public void traverseActivity(int mode, TObject traverserProxy) {
        PdTraverser traverser = new PdTraverser();
        float biomassToRemove_pctMPB = 0.0;
        
        traverser = utravers.PdTraverser(traverserProxy);
        if (traverser == null) {
            return;
        }
        switch (mode) {
            case utravers.kActivityNone:
                break;
            case utravers.kActivityNextDay:
                break;
            case utravers.kActivityDemandVegetative:
                //inc(traverser.totalPlantParts)
                this.biomassDemand_pctMPB = 0.0;
                break;
            case utravers.kActivityDemandReproductive:
                this.biomassDemand_pctMPB = 0.0;
                break;
            case utravers.kActivityGrowVegetative:
                break;
            case utravers.kActivityGrowReproductive:
                break;
            case utravers.kActivityStartReproduction:
                break;
            case utravers.kActivityFindPlantPartAtPosition:
                break;
            case utravers.kActivityDraw:
                traverser.totalPlantParts += 1;
                this.determineAmendmentAndAlsoForChildrenIfAny();
                break;
            case utravers.kActivityReport:
                this.report();
                break;
            case utravers.kActivityStream:
                break;
            case utravers.kActivityFree:
                break;
            case utravers.kActivityVegetativeBiomassThatCanBeRemoved:
                break;
            case utravers.kActivityRemoveVegetativeBiomass:
                break;
            case utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                break;
            case utravers.kActivityRemoveReproductiveBiomass:
                break;
            case utravers.kActivityStandingDeadBiomassThatCanBeRemoved:
                traverser.total = traverser.total + this.deadBiomass_pctMPB;
                break;
            case utravers.kActivityRemoveStandingDeadBiomass:
                biomassToRemove_pctMPB = this.deadBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
                this.deadBiomass_pctMPB = this.deadBiomass_pctMPB - biomassToRemove_pctMPB;
                break;
            case utravers.kActivityGatherStatistics:
                break;
            case utravers.kActivityCountPlantParts:
                traverser.totalPlantParts += 1;
                break;
            case utravers.kActivityFindPartForPartID:
                if (traverser.partID == this.partID) {
                    traverser.foundPlantPart = this;
                    traverser.finished = true;
                }
                break;
            case utravers.kActivityCountTotalMemoryUse:
                break;
            case utravers.kActivityCalculateBiomassForGravity:
                this.biomassOfMeAndAllPartsAboveMe_pctMPB = this.totalBiomass_pctMPB();
                break;
            case utravers.kActivityCountPointsAndTrianglesFor3DExport:
                traverser.totalPlantParts += 1;
                break;
            default:
                throw new GeneralException.create("Problem: Unhandled mode in method PdPlantPart.traverseActivity.");
                break;
    }
    
    // procedure fillInInfoForDXFPart(index: smallint; var realIndex: smallint; var longName: string; var shortName: string);
    public TPoint position() {
        result = new TPoint();
        result = Point(this.boundsRect.Left + (this.boundsRect.Right - this.boundsRect.Left) / 2, this.boundsRect.Top + (this.boundsRect.Bottom - this.boundsRect.Top) / 2);
        return result;
    }
    
    public void addExportMaterial(TObject traverserProxy, short femaleIndex, short maleIndex) {
        PdTraverser traverser = new PdTraverser();
        
        // remember that this is not a true count; each part only adds at LEAST one
        // if you wanted to use this for a true export-type-part count you would have to amend some code
        traverser = utravers.PdTraverser(traverserProxy);
        if (traverser == null) {
            return;
        }
        if (maleIndex < 0) {
            // means to ignore gender
            traverser.exportTypeCounts[femaleIndex] += 1;
        } else if (this.gender == uplant.kGenderFemale) {
            traverser.exportTypeCounts[femaleIndex] += 1;
        } else {
            traverser.exportTypeCounts[maleIndex] += 1;
        }
    }
    
    public void addToStatistics(TObject statisticsProxy, short partType) {
        PdPlantStatistics statistics = new PdPlantStatistics();
        
        statistics = utravers.PdPlantStatistics(statisticsProxy);
        if (statistics == null) {
            return;
        }
        if (this.hasFallenOff) {
            return;
        }
        statistics.count[partType] = statistics.count[partType] + 1;
        statistics.liveBiomass_pctMPB[partType] = statistics.liveBiomass_pctMPB[partType] + this.liveBiomass_pctMPB;
        statistics.deadBiomass_pctMPB[partType] = statistics.deadBiomass_pctMPB[partType] + this.deadBiomass_pctMPB;
    }
    
    public float totalBiomass_pctMPB() {
        result = 0.0;
        result = this.liveBiomass_pctMPB + this.deadBiomass_pctMPB;
        return result;
    }
    
    public float fractionLive() {
        result = 0.0;
        result = 0.0;
        try {
            if (this.totalBiomass_pctMPB() > 0.0) {
                result = umath.safedivExcept(this.liveBiomass_pctMPB, this.totalBiomass_pctMPB(), 0);
            } else {
                result = 0.0;
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdPlantPart.fractionLive");
        }
        return result;
    }
    
    public void draw() {
        pass
        // implemented by subclasses 
    }
    
    public boolean isPhytomer() {
        result = false;
        result = false;
        return result;
    }
    
    public void addOrRemove(boolean addOrRemoveFlag) {
        if (addOrRemoveFlag == kAddingBiomassToPlant) {
            this.hasFallenOff = false;
        } else {
            this.hasFallenOff = true;
        }
    }
    
    public void setColorsToParameters() {
        pass
        //subclasses can override
    }
    
    public String genderString() {
        result = "";
        if (this.gender == uplant.kGenderFemale) {
            result = "primary";
        } else {
            result = "secondary";
        }
        return result;
    }
    
    public void report() {
        String partName = "";
        
        switch (this.partType()) {
            case uplant.kPartTypeFlowerFruit:
                partName = "flower/fruit";
                break;
            case uplant.kPartTypeInflorescence:
                partName = "inflorescence";
                break;
            case uplant.kPartTypeMeristem:
                partName = "meristem";
                break;
            case uplant.kPartTypePhytomer:
                partName = "internode";
                break;
            case uplant.kPartTypeLeaf:
                partName = "leaf";
                break;
        UNRESOLVED.debugPrint("Part " + IntToStr(this.partID) + ", " + partName);
    }
    
    // ---------------------------------------------------------------------------------- drawing 
    public void draw3DObject(KfObject3D tdo, float scale, TColorRef faceColor, TColorRef backfaceColor, short dxfIndex) {
        float realScale = 0.0;
        KfTurtle turtle = new KfTurtle();
        
        if (tdo == null) {
            return;
        }
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        if (this.setColorsWithAmendmentAndReturnTrueIfNoOverrides(kDrawingTdo)) {
            turtle.setForeColorBackColor(faceColor, backfaceColor);
            turtle.setLineColor(usupport.darkerColor(faceColor));
        }
        realScale = scale * this.scaleMultiplierConsideringAmendments();
        turtle.setLineWidth(1.0);
        tdo.draw(turtle, realScale, this.longNameForDXFPartConsideringGenderEtc(dxfIndex), this.shortNameForDXFPartConsideringGenderEtc(dxfIndex), this.realDxfIndexForBaseDXFPart(dxfIndex), this.partID);
    }
    
    public void drawStemSegment(float length, float width, float angleZ, float angleY, TColorRef color, float taperIndex, short dxfIndex, boolean useAmendment) {
        KfTurtle turtle = new KfTurtle();
        float turnPortionZ = 0.0;
        float turnPortionY = 0.0;
        float drawPortion = 0.0;
        float segmentLength = 0.0;
        float segmentTurnZ = 0.0;
        float segmentTurnY = 0.0;
        float realAngleX = 0.0;
        float realAngleY = 0.0;
        float realAngleZ = 0.0;
        short lineDivisions = 0;
        short i = 0;
        KfTriangle triangleMade = new KfTriangle();
        float startWidth = 0.0;
        float endWidth = 0.0;
        float startPortionWidth = 0.0;
        float endPortionWidth = 0.0;
        boolean isLastSegment = false;
        float realLength = 0.0;
        float realWidth = 0.0;
        
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        if (turtle.ifExporting_excludeStem(len)) {
            return;
        }
        if (this.setColorsWithAmendmentAndReturnTrueIfNoOverrides(kDrawingLine)) {
            turtle.setLineColor(color);
        }
        realLength = len * this.lengthMultiplierConsideringAmendments();
        realWidth = width * this.widthMultiplierConsideringAmendments();
        // set up for export
        //for POV you want radius not diameter
        turtle.ifExporting_startStemSegment(this.longNameForDXFPartConsideringGenderEtc(dxfIndex), this.shortNameForDXFPartConsideringGenderEtc(dxfIndex), color, realWidth / 2.0, dxfIndex);
        if (turtle.drawOptions.straightLinesOnly) {
            // get number of segments
            lineDivisions = 1;
        } else {
            lineDivisions = this.plant.pGeneral.lineDivisions;
        }
        // figure length and turn of each segment
        realAngleX = this.rotateAngleConsideringAmendment(kRotateX, useAmendment, 0);
        realAngleY = this.rotateAngleConsideringAmendment(kRotateY, useAmendment, angleY);
        realAngleZ = this.rotateAngleConsideringAmendment(kRotateZ, useAmendment, angleZ);
        if (lineDivisions > 1) {
            turnPortionZ = realAngleZ / lineDivisions;
            turnPortionY = realAngleY / lineDivisions;
            drawPortion = realLength / lineDivisions;
        } else {
            turnPortionZ = realAngleZ;
            turnPortionY = realAngleY;
            drawPortion = realLength;
        }
        // figure width for tapering
        startWidth = realWidth;
        if (taperIndex > 0) {
            endWidth = startWidth * taperIndex / 100.0;
        } else {
            endWidth = realWidth;
        }
        startPortionWidth = startWidth;
        endPortionWidth = startPortionWidth;
        if (realAngleX != 0) {
            turtle.rotateX(realAngleX);
        }
        for (i = 0; i <= lineDivisions - 1; i++) {
            isLastSegment = (i >= lineDivisions - 1);
            if (!isLastSegment) {
                // because of rounding, last segment uses leftover, not equal portion
                segmentTurnZ = turnPortionZ;
                segmentTurnY = turnPortionY;
                segmentLength = drawPortion;
            } else {
                segmentTurnZ = (realAngleZ - (turnPortionZ * (lineDivisions - 1)));
                segmentTurnY = (realAngleY - (turnPortionY * (lineDivisions - 1)));
                segmentLength = (realLength - (drawPortion * (lineDivisions - 1)));
            }
            if ((taperIndex > 0) && (lineDivisions > 1)) {
                // figure tapering for section
                // lineDivisions part added in v1.6b3
                startPortionWidth = startWidth - (i / (lineDivisions - 1)) * (startWidth - endWidth);
                if (!isLastSegment) {
                    endPortionWidth = startWidth - ((i + 1) / (lineDivisions - 1)) * (startWidth - endWidth);
                } else {
                    endPortionWidth = endWidth;
                }
            }
            // set width, rotate, draw line
            turtle.setLineWidth(startPortionWidth);
            turtle.rotateY(segmentTurnY);
            turtle.rotateZ(segmentTurnZ);
            if (turtle.exportingToFile()) {
                this.write3DExportLine(this.partID, segmentLength, startPortionWidth, endPortionWidth, i);
            } else {
                triangleMade = turtle.drawInMillimeters(segmentLength, this.partID);
                if ((turtle.drawOptions.sortTdosAsOneItem) && (triangleMade != null)) {
                    triangleMade.tdo = this.tdoToSortLinesWith();
                }
            }
        }
        turtle.ifExporting_endStemSegment();
    }
    
    public void write3DExportLine(short partID, float length, float startWidth, float endWidth, short segmentNumber) {
        KfTurtle turtle = new KfTurtle();
        float angle = 0.0;
        float pipeRadius = 0.0;
        float faceWidth = 0.0;
        short i = 0;
        short faces = 0;
         startPoints = [0] * (range(0, kMaxLineOutputPoints + 1) + 1);
         endPoints = [0] * (range(0, kMaxLineOutputPoints + 1) + 1);
        
        turtle = this.plant.turtle;
        if (turtle == null) {
            return;
        }
        if (turtle.writingToPOV()) {
            // POV draws cylinders directly, not with faces
            turtle.drawInMillimeters(len, partID);
            return;
        }
        faces = turtle.ifExporting_stemCylinderFaces();
        if (faces == 0) {
            return;
        }
        if (segmentNumber <= 0) {
            // get startWidth points; if done before, copy from last endWidth points
            pipeRadius = 0.5 * startWidth;
            for (i = 0; i <= faces - 1; i++) {
                turtle.push();
                turtle.rotateX(i * 256 / faces);
                turtle.rotateZ(64);
                turtle.moveInMillimeters(pipeRadius);
                startPoints[i] = turtle.position();
                turtle.pop();
            }
        } else {
            for (i = 0; i <= faces - 1; i++) {
                startPoints[i] = endPoints[i];
            }
        }
        turtle.moveInMillimeters(len);
        // get endWidth points
        pipeRadius = 0.5 * endWidth;
        for (i = 0; i <= faces - 1; i++) {
            turtle.push();
            turtle.rotateX(i * 256 / faces);
            turtle.rotateZ(64);
            turtle.moveInMillimeters(pipeRadius);
            endPoints[i] = turtle.position();
            turtle.pop();
        }
        // draw pipe faces from stored points
        turtle.drawFileExportPipeFaces(startPoints, endPoints, faces, segmentNumber);
    }
    
    public KfObject3D tdoToSortLinesWith() {
        result = new KfObject3D();
        // subclasses can override
        result = null;
        return result;
    }
    
    public int partType() {
        result = 0;
        // implemented by subclasses 
        result = 0;
        return result;
    }
    
    public float angleWithSway(float angle) {
        result = 0.0;
        result = angle;
        if (this.plant == null) {
            return result;
        }
        result = angle + ((this.randomSwayIndex - 0.5) * this.plant.pGeneral.randomSway);
        return result;
    }
    
    // ---------------------------------------------------------------------------------- amendments 
    public void determineAmendmentAndAlsoForChildrenIfAny() {
        this.amendment = this.plant.amendmentForPartID(this.partID);
    }
    
    public boolean hiddenByAmendment() {
        result = false;
        boolean iHaveAnAmendment = false;
        boolean iDontHaveAnAmendment = false;
        boolean myParentHasAnAmendment = false;
        boolean myAmendmentSaysIAmHidden = false;
        boolean myParentsAmendmentSaysIAmHidden = false;
        boolean drawingToMainWindow = false;
        
        result = false;
        if (!udomain.domain.options.showPosingAtAll) {
            return result;
        }
        if (this.plant.turtle == null) {
            return result;
        }
        iHaveAnAmendment = this.amendment != null;
        iDontHaveAnAmendment = this.amendment == null;
        myParentHasAnAmendment = this.parentAmendment != null;
        myAmendmentSaysIAmHidden = (this.amendment != null) && (this.amendment.hide);
        myParentsAmendmentSaysIAmHidden = (this.parentAmendment != null) && (this.parentAmendment.hide);
        drawingToMainWindow = (this.plant.turtle.writingTo == u3dexport.kScreen) && (!udomain.domain.drawingToMakeCopyBitmap);
        if ((iHaveAnAmendment && myAmendmentSaysIAmHidden) || (iDontHaveAnAmendment && myParentHasAnAmendment && myParentsAmendmentSaysIAmHidden)) {
            if (drawingToMainWindow) {
                result = !udomain.domain.options.showGhostingForHiddenParts;
            } else {
                result = true;
            }
        }
        return result;
    }
    
    public void applyAmendmentRotations() {
        if ((this.amendment != null) && (this.amendment.addRotations) && (udomain.domain.options.showPosingAtAll)) {
            this.plant.turtle.rotateX(this.amendment.xRotation * 256 / 360);
            this.plant.turtle.rotateY(this.amendment.yRotation * 256 / 360);
            this.plant.turtle.rotateZ(this.amendment.zRotation * 256 / 360);
        }
    }
    
    public boolean setColorsWithAmendmentAndReturnTrueIfNoOverrides(boolean drawingTdo) {
        result = false;
        PdPlantDrawingAmendment amendmentToUse = new PdPlantDrawingAmendment();
        TColorRef color = new TColorRef();
        TColorRef backfaceColor = new TColorRef();
        TColorRef lineColor = new TColorRef();
        boolean iHaveAnAmendment = false;
        boolean iDontHaveAnAmendment = false;
        boolean myParentHasAnAmendment = false;
        boolean myAmendmentSaysIAmHidden = false;
        boolean myParentsAmendmentSaysIAmHidden = false;
        boolean iAmSelectedInTheMainWindow = false;
        boolean showHighlights = false;
        
        result = true;
        if (!udomain.domain.options.showPosingAtAll) {
            return result;
        }
        if (this.plant.turtle == null) {
            return result;
        }
        color = 0;
        backfaceColor = 0;
        lineColor = 0;
        iHaveAnAmendment = this.amendment != null;
        iDontHaveAnAmendment = this.amendment == null;
        myParentHasAnAmendment = this.parentAmendment != null;
        myAmendmentSaysIAmHidden = (this.amendment != null) && (this.amendment.hide);
        myParentsAmendmentSaysIAmHidden = (this.parentAmendment != null) && (this.parentAmendment.hide);
        iAmSelectedInTheMainWindow = (this.partID == umain.MainForm.selectedPlantPartID) && (umain.MainForm.focusedPlant() == this.plant);
        showHighlights = udomain.domain.options.showHighlightingForNonHiddenPosedParts && (this.plant.turtle.writingTo == u3dexport.kScreen) && (!udomain.domain.drawingToMakeCopyBitmap) && (!this.plant.drawingIntoPreviewCache);
        if (iHaveAnAmendment || myParentHasAnAmendment) {
            result = false;
            if ((iHaveAnAmendment && iAmSelectedInTheMainWindow && showHighlights)) {
                color = udomain.domain.options.selectedPosedColor;
            } else if ((iHaveAnAmendment && myAmendmentSaysIAmHidden) || (iDontHaveAnAmendment && myParentHasAnAmendment && myParentsAmendmentSaysIAmHidden)) {
                color = udomain.domain.options.ghostingColor;
            } else if ((iHaveAnAmendment && showHighlights)) {
                color = udomain.domain.options.nonHiddenPosedColor;
            } else {
                result = true;
            }
        }
        if (result == false) {
            if (backfaceColor == 0) {
                backfaceColor = color;
            }
            if (lineColor == 0) {
                lineColor = color;
            }
            if (drawingTdo) {
                this.plant.turtle.setForeColorBackColor(color, backfaceColor);
                this.plant.turtle.setLineColor(usupport.darkerColor(color));
            } else {
                this.plant.turtle.setLineColor(lineColor);
            }
        }
        return result;
    }
    
    // posed color part > if put this back, put it AFTER ghostingColor and BEFORE nonHiddenPosedColor
    //
    //    else if ((amendment <> nil) and (amendment.changeColors))
    //        or ((parentAmendment <> nil) and (parentAmendment.changeColors) and (parentAmendment.propagateColors)) then
    //      begin
    //      // directly changed colors take precedence over highlighting
    //      if amendment <> nil then amendmentToUse := amendment else amendmentToUse := parentAmendment;
    //      color := amendmentToUse.faceColor;
    //      backFaceColor := amendmentToUse.backfaceColor;
    //      lineColor := amendmentToUse.lineColor;
    //      end
    //      
    public float rotateAngleConsideringAmendment(short rotateWhat, boolean useAmendment, float angle) {
        result = 0.0;
        result = angle;
        if ((useAmendment) && (this.amendment != null) && (this.amendment.addRotations) && (udomain.domain.options.showPosingAtAll)) {
            switch (rotateWhat) {
                case kRotateX:
                    result = angle + this.amendment.xRotation * 256 / 360;
                    break;
                case kRotateY:
                    result = angle + this.amendment.yRotation * 256 / 360;
                    break;
                case kRotateZ:
                    result = angle + this.amendment.zRotation * 256 / 360;
                    break;
        }
        return result;
    }
    
    public float scaleMultiplierConsideringAmendments() {
        result = 0.0;
        PdPlantDrawingAmendment amendmentToUse = new PdPlantDrawingAmendment();
        
        result = 1.0;
        if (!udomain.domain.options.showPosingAtAll) {
            return result;
        }
        if ((this.amendment != null) || (this.parentAmendment != null)) {
            if (((this.amendment != null) && (this.amendment.multiplyScale)) || ((this.parentAmendment != null) && (this.parentAmendment.multiplyScale) && (this.parentAmendment.propagateScale))) {
                if (this.amendment != null) {
                    amendmentToUse = this.amendment;
                } else {
                    amendmentToUse = this.parentAmendment;
                }
                result = 1.0 * amendmentToUse.scaleMultiplier_pct / 100.0;
            }
        }
        return result;
    }
    
    public float lengthMultiplierConsideringAmendments() {
        result = 0.0;
        PdPlantDrawingAmendment amendmentToUse = new PdPlantDrawingAmendment();
        
        result = 1.0;
        if (!udomain.domain.options.showPosingAtAll) {
            return result;
        }
        if ((this.amendment != null) || (this.parentAmendment != null)) {
            if (((this.amendment != null) && (this.amendment.multiplyScale)) || ((this.parentAmendment != null) && (this.parentAmendment.multiplyScale) && (this.parentAmendment.propagateScale))) {
                if (this.amendment != null) {
                    amendmentToUse = this.amendment;
                } else {
                    amendmentToUse = this.parentAmendment;
                }
                result = 1.0 * amendmentToUse.lengthMultiplier_pct / 100.0;
            }
        }
        return result;
    }
    
    public float widthMultiplierConsideringAmendments() {
        result = 0.0;
        PdPlantDrawingAmendment amendmentToUse = new PdPlantDrawingAmendment();
        
        result = 1.0;
        if (!udomain.domain.options.showPosingAtAll) {
            return result;
        }
        if ((this.amendment != null) || (this.parentAmendment != null)) {
            if (((this.amendment != null) && (this.amendment.multiplyScale)) || ((this.parentAmendment != null) && (this.parentAmendment.multiplyScale) && (this.parentAmendment.propagateScale))) {
                if (this.amendment != null) {
                    amendmentToUse = this.amendment;
                } else {
                    amendmentToUse = this.parentAmendment;
                }
                result = 1.0 * amendmentToUse.widthMultiplier_pct / 100.0;
            }
        }
        return result;
    }
    
    // ---------------------------------------------------------------------------------- streaming 
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kPdPlantPart;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    //this will stream entire the entire object -
    //but the included object references need to be fixed up afterwards
    //or the objects streamed out separately afterwards - subclasses overrides
    //need to call inherited to get this behavior
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        super.streamDataWithFiler(filer, cvir);
        this.liveBiomass_pctMPB = filer.streamSingle(this.liveBiomass_pctMPB);
        this.deadBiomass_pctMPB = filer.streamSingle(this.deadBiomass_pctMPB);
        this.biomassDemand_pctMPB = filer.streamSingle(this.biomassDemand_pctMPB);
        this.gender = filer.streamSmallint(this.gender);
        this.age = filer.streamLongint(this.age);
        this.hasFallenOff = filer.streamBoolean(this.hasFallenOff);
        this.isSeedlingLeaf = filer.streamBoolean(this.isSeedlingLeaf);
        this.partID = filer.streamLongint(this.partID);
        this.biomassOfMeAndAllPartsAboveMe_pctMPB = filer.streamSingle(this.biomassOfMeAndAllPartsAboveMe_pctMPB);
        this.randomSwayIndex = filer.streamSingle(this.randomSwayIndex);
    }
    
    public void addDependentPartsToList(TList aList) {
        pass
        // subclasses can override 
    }
    
    public void blendColorsStrength(TColorRef aColor, float aStrength) {
        pass
        //subclasses can override
    }
    
    public void calculateColors() {
        this.setColorsToParameters();
    }
    
    public String longNameForDXFPartConsideringGenderEtc(short index) {
        result = "";
        result = u3dexport.longNameForDXFPartType(this.realDxfIndexForBaseDXFPart(index));
        return result;
    }
    
    public String shortNameForDXFPartConsideringGenderEtc(short index) {
        result = "";
        result = u3dexport.shortNameForDXFPartType(this.realDxfIndexForBaseDXFPart(index));
        return result;
    }
    
    public short realDxfIndexForBaseDXFPart(short index) {
        result = 0;
        result = index;
        switch (index) {
            case u3dexport.kExportPartLeaf:
                if (this.isSeedlingLeaf) {
                    result = u3dexport.kExportPartSeedlingLeaf;
                }
                break;
            case u3dexport.kExportPartPetiole:
                if (this.isSeedlingLeaf) {
                    result = u3dexport.kExportPartFirstPetiole;
                }
                break;
            case u3dexport.kExportPartInflorescenceStalkFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartInflorescenceStalkMale;
                }
                break;
            case u3dexport.kExportPartInflorescenceInternodeFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartInflorescenceInternodeMale;
                }
                break;
            case u3dexport.kExportPartInflorescenceBractFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartInflorescenceBractMale;
                }
                break;
            case u3dexport.kExportPartPedicelFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartPedicelMale;
                }
                break;
            case u3dexport.kExportPartFlowerBudFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartFlowerBudMale;
                }
                break;
            case u3dexport.kExportPartFilamentFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartFilamentMale;
                }
                break;
            case u3dexport.kExportPartAntherFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartAntherMale;
                }
                break;
            case u3dexport.kExportPartFirstPetalsFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartFirstPetalsMale;
                }
                break;
            case u3dexport.kExportPartSepalsFemale:
                if (this.gender == uplant.kGenderMale) {
                    result = u3dexport.kExportPartSepalsMale;
                }
                break;
        return result;
    }
    
}
