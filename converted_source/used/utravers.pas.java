// unit Utravers

from conversion_common import *;
import ubreedr;
import umain;
import uintern;
import umath;
import usupport;
import u3dexport;
import ufiler;
import upart;
import uplant;
import delphi_compatability;

// const
kTraverseNone = 0;
kTraverseLeft = 1;
kTraverseRight = 2;
kTraverseNext = 3;
kTraverseDone = 4;
kActivityNone = 0;
kActivityNextDay = 1;
kActivityDemandVegetative = 2;
kActivityDemandReproductive = 3;
kActivityGrowVegetative = 4;
kActivityGrowReproductive = 5;
kActivityStartReproduction = 6;
kActivityFindPlantPartAtPosition = 7;
kActivityDraw = 8;
kActivityReport = 9;
kActivityStream = 10;
kActivityFree = 11;
kActivityVegetativeBiomassThatCanBeRemoved = 12;
kActivityRemoveVegetativeBiomass = 13;
kActivityReproductiveBiomassThatCanBeRemoved = 14;
kActivityRemoveReproductiveBiomass = 15;
kActivityGatherStatistics = 16;
kActivityStandingDeadBiomassThatCanBeRemoved = 17;
kActivityRemoveStandingDeadBiomass = 18;
kActivityCountPlantParts = 19;
kActivityFindPartForPartID = 20;
kActivityCountTotalMemoryUse = 21;
kActivityCalculateBiomassForGravity = 22;
kActivityCountPointsAndTrianglesFor3DExport = 23;


// const
kStatisticsPartTypeSeedlingLeaf = 0;
kStatisticsPartTypeLeaf = 1;
kStatisticsPartTypeFemaleInflorescence = 2;
kStatisticsPartTypeMaleInflorescence = 3;
kStatisticsPartTypeFemaleFlower = 4;
kStatisticsPartTypeFemaleFlowerBud = 5;
kStatisticsPartTypeMaleFlower = 6;
kStatisticsPartTypeMaleFlowerBud = 7;
kStatisticsPartTypeAxillaryBud = 8;
kStatisticsPartTypeFruit = 9;
kStatisticsPartTypeStem = 10;
kStatisticsPartTypeUnripeFruit = 11;
kStatisticsPartTypeFallenFruit = 12;
kStatisticsPartTypeUnallocatedNewVegetativeBiomass = 13;
kStatisticsPartTypeUnremovedDeadVegetativeBiomass = 14;
kStatisticsPartTypeUnallocatedNewReproductiveBiomass = 15;
kStatisticsPartTypeUnremovedDeadReproductiveBiomass = 16;
kStatisticsPartTypeFallenFlower = 17;
kStatisticsPartTypeAllVegetative = 18;
kStatisticsPartTypeAllReproductive = 19;
kStatisticsPartTypeLast = 19;


// var
boolean cancelDrawing = false;
TColorRef worstNStressColor = new TColorRef();
TColorRef worstPStressColor = new TColorRef();
TColorRef worstDeadColor = new TColorRef();


// -------------------------------------------------------------------------- linear growth functions 
public float linearGrowthWithFactorResult(float current, float optimal, int minDays, float growthFactor) {
    result = 0.0;
    float amountNeeded = 0.0;
    float maxPossible = 0.0;
    
    result = 0.0;
    try {
        amountNeeded = optimal - current;
        maxPossible = umath.safedivExcept(optimal, minDays, optimal);
        amountNeeded = umath.max(0.0, umath.min(amountNeeded, maxPossible));
        result = amountNeeded * growthFactor;
    } catch (Exception e) {
        usupport.messageForExceptionType(e, "linearGrowthWithFactorResult");
    }
    return result;
}

public void linearGrowthWithFactor(float current, float optimal, int minDays, float growthFactor) {
    float amountNeeded = 0.0;
    float maxPossible = 0.0;
    
    try {
        amountNeeded = optimal - current;
        maxPossible = umath.safedivExcept(optimal, minDays, optimal);
        amountNeeded = umath.max(0.0, umath.min(amountNeeded, maxPossible));
        current = current + amountNeeded * growthFactor;
    } catch (Exception e) {
        usupport.messageForExceptionType(e, "linearGrowthWithFactor");
    }
    return current;
}

public float linearGrowthResult(float current, float optimal, int minDays) {
    result = 0.0;
    float amountNeeded = 0.0;
    float maxPossible = 0.0;
    
    result = 0.0;
    try {
        amountNeeded = optimal - current;
        maxPossible = umath.safedivExcept(optimal, minDays, optimal);
        amountNeeded = umath.max(0.0, umath.min(amountNeeded, maxPossible));
        result = amountNeeded;
    } catch (Exception e) {
        usupport.messageForExceptionType(e, "linearGrowthResult");
    }
    return result;
}

public void linearGrowth(float current, float optimal, int minDays) {
    float amountNeeded = 0.0;
    float maxPossible = 0.0;
    
    try {
        amountNeeded = optimal - current;
        maxPossible = umath.safedivExcept(optimal, minDays, optimal);
        amountNeeded = umath.max(0.0, umath.min(amountNeeded, maxPossible));
        current = current + amountNeeded;
    } catch (Exception e) {
        usupport.messageForExceptionType(e, "linearGrowth");
    }
    return current;
}


// meristems
class PdPlantStatistics extends TObject {
    public  count;
    public  liveBiomass_pctMPB;
    public  deadBiomass_pctMPB;
    
    // ---------------------------------------------------------------------------------- statistics object 
    public void zeroAllFields() {
        short i = 0;
        
        for (i = 0; i <= kStatisticsPartTypeLast; i++) {
            this.count[i] = 0;
            this.liveBiomass_pctMPB[i] = 0.0;
            this.deadBiomass_pctMPB[i] = 0.0;
        }
    }
    
    public float totalBiomass_pctMPB() {
        result = 0.0;
        short i = 0;
        
        result = 0.0;
        for (i = 0; i <= kStatisticsPartTypeLast; i++) {
            result = result + this.liveBiomass_pctMPB[i];
            result = result + this.deadBiomass_pctMPB[i];
        }
        return result;
    }
    
}
class PdTraverser extends TObject {
    public PdPlant plant;
    public PdFiler filer;
    public TObject currentPhytomer;
    public TPoint point;
    public float total;
    public float fractionOfPotentialBiomass;
    public long ageOfYoungestPhytomer;
    public short mode;
    public boolean finished;
    public PdPlantPart foundPlantPart;
    public TList foundList;
    public PdPlantStatistics statistics;
    public long totalPlantParts;
    public long total3DExportPointsIn3DObjects;
    public long total3DExportTrianglesIn3DObjects;
    public long total3DExportStemSegments;
    public boolean showDrawingProgress;
    public long plantPartsDrawnAtStart;
    public long partID;
    public long totalMemorySize;
    public  exportTypeCounts;
    
    // ---------------------------------------------------------------------------------- traversing object 
    public void createWithPlant(PdPlant thePlant) {
        this.create;
        this.plant = thePlant;
    }
    
    public void beginTraversal(int aMode) {
        this.mode = aMode;
        this.currentPhytomer = this.plant.firstPhytomer;
        this.total = 0.0;
        this.finished = false;
        this.foundPlantPart = null;
        this.totalPlantParts = 0;
        if (this.currentPhytomer != null) {
            uintern.PdInternode(this.currentPhytomer).traversingDirection = kTraverseLeft;
            uintern.PdInternode(this.currentPhytomer).traverseActivity(this.mode, this);
            //reset afterwards in case read in differently
            uintern.PdInternode(this.currentPhytomer).traversingDirection = kTraverseLeft;
        }
    }
    
    public void traverseWholePlant(int aMode) {
        this.beginTraversal(aMode);
        this.traversePlant(0);
    }
    
    public void traversePlant(long traversalCount) {
        long i = 0;
        PdInternode lastPhytomer = new PdInternode();
        PdInternode phytomerTraversing = new PdInternode();
        
        if ((this.currentPhytomer == null)) {
            return;
        }
        phytomerTraversing = uintern.PdInternode(this.currentPhytomer);
        i = 0;
        while (i <= traversalCount) {
            if (this.finished) {
                return;
            }
            switch (phytomerTraversing.traversingDirection) {
                case kTraverseLeft:
                    phytomerTraversing.traversingDirection += 1;
                    if (phytomerTraversing.leftBranchPlantPart != null) {
                        if ((this.mode == kActivityDraw)) {
                            this.plant.turtle.push();
                        }
                        phytomerTraversing.leftBranchPlantPart.traverseActivity(this.mode, this);
                        if ((phytomerTraversing.leftBranchPlantPart.isPhytomer())) {
                            phytomerTraversing = uintern.PdInternode(phytomerTraversing.leftBranchPlantPart);
                            phytomerTraversing.traversingDirection = kTraverseLeft;
                        } else if ((this.mode == kActivityDraw)) {
                            this.plant.turtle.pop();
                        }
                    }
                    break;
                case kTraverseRight:
                    phytomerTraversing.traversingDirection += 1;
                    if (phytomerTraversing.rightBranchPlantPart != null) {
                        if ((this.mode == kActivityDraw)) {
                            this.plant.turtle.push();
                        }
                        phytomerTraversing.rightBranchPlantPart.traverseActivity(this.mode, this);
                        if ((phytomerTraversing.rightBranchPlantPart.isPhytomer())) {
                            phytomerTraversing = uintern.PdInternode(phytomerTraversing.rightBranchPlantPart);
                            phytomerTraversing.traversingDirection = kTraverseLeft;
                        } else if ((this.mode == kActivityDraw)) {
                            this.plant.turtle.pop();
                        }
                    }
                    break;
                case kTraverseNext:
                    phytomerTraversing.traversingDirection += 1;
                    if (phytomerTraversing.nextPlantPart != null) {
                        if ((this.mode == kActivityDraw)) {
                            this.plant.turtle.push();
                            this.plant.turtle.rotateX(this.plant.pGeneral.phyllotacticRotationAngle * 256 / 360);
                        }
                        phytomerTraversing.nextPlantPart.traverseActivity(this.mode, this);
                        if ((phytomerTraversing.nextPlantPart.isPhytomer())) {
                            phytomerTraversing = uintern.PdInternode(phytomerTraversing.nextPlantPart);
                            phytomerTraversing.traversingDirection = kTraverseLeft;
                        } else if ((this.mode == kActivityDraw)) {
                            this.plant.turtle.pop();
                        }
                    }
                    break;
                case kTraverseDone:
                    phytomerTraversing.traversingDirection = kTraverseNone;
                    lastPhytomer = phytomerTraversing;
                    phytomerTraversing = phytomerTraversing.phytomerAttachedTo;
                    if ((this.mode == kActivityFree)) {
                        lastPhytomer.free;
                        if (phytomerTraversing != null) {
                            if ((phytomerTraversing.traversingDirection == kTraverseLeft + 1)) {
                                phytomerTraversing.leftBranchPlantPart = null;
                            } else if ((phytomerTraversing.traversingDirection == kTraverseRight + 1)) {
                                phytomerTraversing.rightBranchPlantPart = null;
                            } else if ((phytomerTraversing.traversingDirection == kTraverseNext + 1)) {
                                phytomerTraversing.nextPlantPart = null;
                            }
                        }
                    }
                    if (phytomerTraversing == null) {
                        break;
                    }
                    if ((this.mode == kActivityDraw)) {
                        //special drawing stuff - if returning from left or right branch draw, pop turtle
                        //	if (phytomerTraversing.traversingDirection = kTraverseLeft + 1)
                        //           or (phytomerTraversing.traversingDirection =  kTraverseRight + 1)  then 
                        this.plant.turtle.pop();
                    }
                    if ((this.mode == kActivityCalculateBiomassForGravity)) {
                        phytomerTraversing.traverseActivity(this.mode, this);
                    }
                    break;
                case kTraverseNone:
                    throw new GeneralException.create("Problem: kTraverseNone encountered in method PdTraverser.traversePlant.");
                    break;
            if ((traversalCount != 0)) {
                i += 1;
            }
            if ((this.mode == kActivityDraw) && (this.showDrawingProgress)) {
                if (this.totalPlantParts % 4 != 0) {
                    continue;
                }
                if ((umain.MainForm != null) && (umain.MainForm.drawing)) {
                    umain.MainForm.showDrawProgress(this.plantPartsDrawnAtStart + this.totalPlantParts);
                }
            }
        }
    }
    
}
