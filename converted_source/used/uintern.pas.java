// unit uintern

from conversion_common import *;
import uamendmt;
import uinflor;
import umerist;
import umath;
import utdo;
import u3dexport;
import uturtle;
import usupport;
import utravers;
import ufiler;
import uleaf;
import uplant;
import upart;
import delphi_compatability;


class PdInternode extends PdPlantPart {
    public PdPlantPart leftBranchPlantPart;
    public PdPlantPart rightBranchPlantPart;
    public PdPlantPart nextPlantPart;
    public PdInternode phytomerAttachedTo;
    public PdLeaf leftLeaf;
    public PdLeaf rightLeaf;
    public TColorRef internodeColor;
    public float internodeAngle;
    public float lengthExpansion;
    public float widthExpansion;
    public float boltingExpansion;
    public float fractionOfOptimalInitialBiomassAtCreation_frn;
    public byte traversingDirection;
    public boolean isFirstPhytomer;
    public float newBiomassForDay_pctMPB;
    public long distanceFromFirstPhytomer;
    
    public PdInternode NewWithPlantFractionOfInitialOptimalSize(PdPlant aPlant, float aFraction) {
        result = new PdInternode();
        result = this.create();
        result.InitializeFractionOfInitialOptimalSize(aPlant, aFraction);
        return result;
    }
    
    //???
    public void InitializeFractionOfInitialOptimalSize(PdPlant thePlant, float aFraction) {
        this.initialize(thePlant);
        //Plant sets this from outside on first phytomer.
        this.isFirstPhytomer = false;
        this.calculateInternodeAngle();
        this.lengthExpansion = 1.0;
        this.widthExpansion = 1.0;
        this.boltingExpansion = 1.0;
        this.fractionOfOptimalInitialBiomassAtCreation_frn = aFraction;
        this.liveBiomass_pctMPB = aFraction * PdInternode.optimalInitialBiomass_pctMPB(this.plant);
        this.deadBiomass_pctMPB = 0.0;
        this.internodeColor = this.plant.pInternode.faceColor;
        this.leftLeaf = uleaf.PdLeaf.NewWithPlantFractionOfOptimalSize(this.plant, aFraction);
        if (this.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementOpposite) {
            this.rightLeaf = uleaf.PdLeaf.NewWithPlantFractionOfOptimalSize(this.plant, aFraction);
        }
    }
    
    public String getName() {
        result = "";
        result = "internode";
        return result;
    }
    
    public void makeSecondSeedlingLeaf(float aFraction) {
        if (this.rightLeaf == null) {
            this.rightLeaf = uleaf.PdLeaf.NewWithPlantFractionOfOptimalSize(this.plant, aFraction);
        }
        if (this.rightLeaf != null) {
            this.rightLeaf.isSeedlingLeaf = true;
        }
    }
    
    public void destroy() {
        //note that if branch parts were phytomers they will have been
        //  freed and set to nil by the traverser
        this.nextPlantPart.free;
        this.nextPlantPart = null;
        this.leftBranchPlantPart.free;
        this.leftBranchPlantPart = null;
        this.rightBranchPlantPart.free;
        this.rightBranchPlantPart = null;
        this.leftLeaf.free;
        this.leftLeaf = null;
        this.rightLeaf.free;
        this.rightLeaf = null;
        super.destroy();
    }
    
    public void setAsFirstPhytomer() {
        this.isFirstPhytomer = true;
        if (this.leftLeaf != null) {
            this.leftLeaf.isSeedlingLeaf = true;
        }
        if (this.rightLeaf != null) {
            this.rightLeaf.isSeedlingLeaf = true;
        }
        this.calculateInternodeAngle();
    }
    
    public void determineAmendmentAndAlsoForChildrenIfAny() {
        PdPlantDrawingAmendment amendmentToPass = new PdPlantDrawingAmendment();
        
        super.determineAmendmentAndAlsoForChildrenIfAny();
        if (this.amendment != null) {
            amendmentToPass = this.amendment;
        } else {
            amendmentToPass = this.parentAmendment;
        }
        if (this.leftBranchPlantPart != null) {
            this.leftBranchPlantPart.parentAmendment = amendmentToPass;
        }
        if (this.rightBranchPlantPart != null) {
            this.rightBranchPlantPart.parentAmendment = amendmentToPass;
        }
        if (this.nextPlantPart != null) {
            this.nextPlantPart.parentAmendment = amendmentToPass;
        }
        if (this.leftLeaf != null) {
            // amendment must be passed to leaves explicitly since they are not strictly speaking children
            this.leftLeaf.parentAmendment = amendmentToPass;
        }
        if (this.rightLeaf != null) {
            this.leftLeaf.parentAmendment = amendmentToPass;
        }
    }
    
    public void nextDay() {
        float tryExpansion = 0.0;
        
        try {
            super.nextDay();
            if (this.liveBiomass_pctMPB > 0) {
                try {
                    // length and width expansion adjustment from new biomass (always decreases because new biomass is compact) 
                    // if liveBiomass_pctMPB is extremely small, these divisions may produce an overflow 
                    // must bound these because some accounting error is causing problems that should be fixed later 
                    tryExpansion = umath.max(0.0, umath.min(500.0, umath.safedivExcept(this.liveBiomass_pctMPB - this.newBiomassForDay_pctMPB, this.liveBiomass_pctMPB, 0) * this.lengthExpansion + umath.safedivExcept(this.newBiomassForDay_pctMPB, this.liveBiomass_pctMPB, 0) * 1.0));
                    this.lengthExpansion = tryExpansion;
                } catch (Exception e) {
                    // pass
                }
                try {
                    tryExpansion = umath.max(0.0, umath.min(50.0, umath.safedivExcept(this.liveBiomass_pctMPB - this.newBiomassForDay_pctMPB, this.liveBiomass_pctMPB, 0) * this.widthExpansion + umath.safedivExcept(this.newBiomassForDay_pctMPB, this.liveBiomass_pctMPB, 0) * 1.0));
                    this.widthExpansion = tryExpansion;
                } catch (Exception e) {
                    // pass
                }
                if (this.plant.floweringHasStarted) {
                    // not using this version
                    //    { length and width expansion increase due to water uptake }
                    //    with plant.pInternode do
                    //      if self.age <= plant.pInternode.maxDaysToExpand then
                    //        begin
                    //        linearGrowthWithFactor(self.lengthExpansion,
                    //            lengthMultiplierDueToExpansion, minDaysToExpand, 1.0); {1.0 was water stress factor}
                    //        linearGrowthWithFactor(self.widthExpansion,
                    //            widthMultiplierDueToExpansion, minDaysToExpand, 1.0);
                    //        end;
                    //    
                    //and
                    //      (plant.age - plant.ageAtWhichFloweringStarted <= plant.pInternode.maxDaysToBolt)
                    this.boltingExpansion = utravers.linearGrowthWithFactor(this.boltingExpansion, this.plant.pInternode.lengthMultiplierDueToBolting, this.plant.pInternode.minDaysToBolt, 1.0);
                }
            }
            this.checkIfSeedlingLeavesHaveAbscissed();
            this.calculateDistanceFromFirstPhytomer();
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInternode.nextDay");
        }
    }
    
    public float optimalInitialBiomass_pctMPB(PdPlant plant) {
        result = 0.0;
        result = umath.safedivExcept(plant.pInternode.optimalFinalBiomass_pctMPB, plant.pInternode.lengthMultiplierDueToBiomassAccretion * plant.pInternode.widthMultiplierDueToBiomassAccretion, 0);
        return result;
    }
    
    public float propFullLength() {
        result = 0.0;
        result = umath.safedivExcept(this.totalBiomass_pctMPB() * this.lengthExpansion * this.boltingExpansion, this.plant.pInternode.optimalFinalBiomass_pctMPB, 0);
        return result;
    }
    
    public float propFullWidth() {
        result = 0.0;
        result = umath.safedivExcept(this.totalBiomass_pctMPB() * this.widthExpansion, this.plant.pInternode.optimalFinalBiomass_pctMPB, 0);
        return result;
    }
    
    public void traverseActivity(int mode, TObject traverserProxy) {
        PdTraverser traverser = new PdTraverser();
        float biomassToRemove_pctMPB = 0.0;
        float targetBiomass_pctMPB = 0.0;
        
        super.traverseActivity(mode, traverserProxy);
        traverser = utravers.PdTraverser(traverserProxy);
        if (traverser == null) {
            return;
        }
        if (this.hasFallenOff && (mode != utravers.kActivityStream) && (mode != utravers.kActivityFree)) {
            return;
        }
        try {
            if ((mode != utravers.kActivityDraw)) {
                if (this.leftLeaf != null) {
                    this.leftLeaf.traverseActivity(mode, traverser);
                }
                if (this.rightLeaf != null) {
                    this.rightLeaf.traverseActivity(mode, traverser);
                }
            }
            switch (mode) {
                case utravers.kActivityNone:
                    break;
                case utravers.kActivityNextDay:
                    this.nextDay();
                    if (this.age < traverser.ageOfYoungestPhytomer) {
                        traverser.ageOfYoungestPhytomer = this.age;
                    }
                    break;
                case utravers.kActivityDemandVegetative:
                    if (this.age > this.plant.pInternode.maxDaysToAccumulateBiomass) {
                        this.biomassDemand_pctMPB = 0.0;
                        return;
                    }
                    try {
                        if (this.plant.pInternode.canRecoverFromStuntingDuringCreation) {
                            targetBiomass_pctMPB = this.plant.pInternode.optimalFinalBiomass_pctMPB;
                        } else {
                            targetBiomass_pctMPB = this.plant.pInternode.optimalFinalBiomass_pctMPB * this.fractionOfOptimalInitialBiomassAtCreation_frn;
                        }
                        this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, targetBiomass_pctMPB, this.plant.pInternode.minDaysToAccumulateBiomass);
                        traverser.total = traverser.total + this.biomassDemand_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdInternode.traverseActivity (vegetative demand)");
                    }
                    break;
                case utravers.kActivityDemandReproductive:
                    break;
                case utravers.kActivityGrowVegetative:
                    if (this.age > this.plant.pInternode.maxDaysToAccumulateBiomass) {
                        //Return reproductive demand recursively from all reproductive meristems and fruits connected to
                        //      this phytomer. Phytomers, inflorescences, and flowers themselves have no demands.
                        return;
                    }
                    try {
                        this.newBiomassForDay_pctMPB = umath.max(0.0, this.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass);
                        this.liveBiomass_pctMPB = this.liveBiomass_pctMPB + this.newBiomassForDay_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdInternode.traverseActivity (vegetative growth)");
                    }
                    break;
                case utravers.kActivityGrowReproductive:
                    break;
                case utravers.kActivityStartReproduction:
                    break;
                case utravers.kActivityFindPlantPartAtPosition:
                    if (umath.pointsAreCloseEnough(traverser.point, this.position())) {
                        //Recurse available photosynthate allocated to reproductive growth to all plant parts.
                        //      Only meristems and fruits will incorporate it.
                        //Send signal to consider reproductive mode to all meristems on plant.
                        traverser.foundPlantPart = this;
                        traverser.finished = true;
                    }
                    break;
                case utravers.kActivityDraw:
                    this.draw();
                    break;
                case utravers.kActivityReport:
                    break;
                case utravers.kActivityStream:
                    this.streamUsingFiler(traverser.filer);
                    break;
                case utravers.kActivityFree:
                    break;
                case utravers.kActivityVegetativeBiomassThatCanBeRemoved:
                    // free called by traverser 
                    traverser.total = traverser.total + this.liveBiomass_pctMPB;
                    break;
                case utravers.kActivityRemoveVegetativeBiomass:
                    biomassToRemove_pctMPB = this.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
                    this.liveBiomass_pctMPB = this.liveBiomass_pctMPB - biomassToRemove_pctMPB;
                    this.deadBiomass_pctMPB = this.deadBiomass_pctMPB + biomassToRemove_pctMPB;
                    break;
                case utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                    break;
                case utravers.kActivityRemoveReproductiveBiomass:
                    break;
                case utravers.kActivityGatherStatistics:
                    // none 
                    // none 
                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeStem);
                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllVegetative);
                    break;
                case utravers.kActivityCountPlantParts:
                    break;
                case utravers.kActivityFindPartForPartID:
                    break;
                case utravers.kActivityCountTotalMemoryUse:
                    traverser.totalMemorySize += this.instanceSize;
                    break;
                case utravers.kActivityCalculateBiomassForGravity:
                    if (this.traversingDirection == utravers.kTraverseDone) {
                        // on way up, do nothing; on way down, total up accumulated biomass
                        this.biomassOfMeAndAllPartsAboveMe_pctMPB = this.biomassOfMeAndAllPartsConnectedToMe_pctMPB() + this.biomassOfPartsImmediatelyAboveMe_pctMPB();
                    }
                    break;
                case utravers.kActivityCountPointsAndTrianglesFor3DExport:
                    this.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser);
                    break;
                default:
                    throw new GeneralException.create("Problem: Unhandled mode in method PdInternode.traverseActivity.");
                    break;
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInternode.traverseActivity");
        }
    }
    
    public void countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(PdTraverser traverser) {
        if (traverser == null) {
            return;
        }
        traverser.total3DExportStemSegments += 1;
        this.addExportMaterial(traverser, u3dexport.kExportPartInternode, -1);
        if (this.plant.pRoot.tdoParams.scaleAtFullSize > 0) {
            this.addExportMaterial(traverser, u3dexport.kExportPartRootTop, -1);
        }
    }
    
    public boolean isPhytomer() {
        result = false;
        result = true;
        return result;
    }
    
    public void blendColorsStrength(TColorRef aColor, float aStrength) {
        if (aStrength <= 0.0) {
            return;
        }
        this.internodeColor = usupport.blendColors(this.internodeColor, aColor, aStrength);
    }
    
    public void setColorsToParameters() {
        //Initialize phytomer colors at those in plant parameters, before stresses are considered.
        this.internodeColor = this.plant.pInternode.faceColor;
    }
    
    public void calculateInternodeAngle() {
        if (this.isFirstPhytomer) {
            if ((this.plant.pInternode.firstInternodeCurvingIndex == 0)) {
                this.internodeAngle = 0;
            } else {
                this.internodeAngle = 64.0 / 100.0 * (this.plant.randomNumberGenerator.randomNormalPercent(this.plant.pInternode.firstInternodeCurvingIndex));
            }
        } else {
            if ((this.plant.pInternode.curvingIndex == 0)) {
                this.internodeAngle = 0;
            } else {
                this.internodeAngle = 64.0 / 100.0 * (this.plant.randomNumberGenerator.randomNormalPercent(this.plant.pInternode.curvingIndex));
            }
        }
        this.internodeAngle = this.angleWithSway(this.internodeAngle);
    }
    
    public long distanceFromApicalMeristem() {
        result = 0;
        PdInternode aPhytomer = new PdInternode();
        
        //Count phytomers along this apex until you reach an apical meristem or inflorescence.
        result = 0;
        if ((this.nextPlantPart.isPhytomer())) {
            aPhytomer = PdInternode(this.nextPlantPart);
        } else {
            aPhytomer = null;
        }
        while (aPhytomer != null) {
            result += 1;
            if ((aPhytomer.nextPlantPart.isPhytomer())) {
                aPhytomer = PdInternode(aPhytomer.nextPlantPart);
            } else {
                aPhytomer = null;
            }
        }
        return result;
    }
    
    public void calculateDistanceFromFirstPhytomer() {
        PdInternode aPhytomer = new PdInternode();
        long result = 0;
        
        //Count phytomers backwards along this apex until you reach the first.
        result = 0;
        if (this.isFirstPhytomer) {
            return;
        }
        aPhytomer = this.phytomerAttachedTo;
        while (aPhytomer != null) {
            result += 1;
            aPhytomer = aPhytomer.phytomerAttachedTo;
        }
        this.distanceFromFirstPhytomer = result;
    }
    
    public PdInternode firstPhytomerOnBranch() {
        result = new PdInternode();
        result = this;
        while (result != null) {
            if ((result.phytomerAttachedTo != null) && (result.phytomerAttachedTo.nextPlantPart == result)) {
                result = PdInternode(result.phytomerAttachedTo);
            } else {
                break;
            }
        }
        if (result == this) {
            result = null;
        }
        return result;
    }
    
    public float biomassOfMeAndAllPartsConnectedToMe_pctMPB() {
        result = 0.0;
        result = this.totalBiomass_pctMPB();
        if (this.leftLeaf != null) {
            result = result + this.leftLeaf.totalBiomass_pctMPB();
        }
        if (this.rightLeaf != null) {
            result = result + this.rightLeaf.totalBiomass_pctMPB();
        }
        return result;
    }
    
    public float biomassOfPartsImmediatelyAboveMe_pctMPB() {
        result = 0.0;
        result = 0;
        if (this.leftBranchPlantPart != null) {
            result = result + this.leftBranchPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB;
        }
        if (this.rightBranchPlantPart != null) {
            result = result + this.rightBranchPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB;
        }
        if (this.nextPlantPart != null) {
            result = result + this.nextPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB;
        }
        return result;
    }
    
    public void draw() {
        KfTurtle turtle = new KfTurtle();
        
        //Draw all parts of phytomer. Consider if the phytomer is the first (has the seedling leaves) and whether
        //    the leaves attached to this phytomer have abscissed (and are not drawn).
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        this.boundsRect = Rect(0, 0, 0, 0);
        if (this.hiddenByAmendment()) {
            if (this.leftLeaf != null) {
                // if internode is hidden the leaves could still be drawn, if they are posed.
                // if they are themselves hidden, they will pop back out without drawing.
                this.leftLeaf.drawWithDirection(uplant.kDirectionLeft);
            }
            if (this.rightLeaf != null) {
                this.rightLeaf.drawWithDirection(uplant.kDirectionRight);
            }
            // amendment rotations handled in drawStemSegment
            return;
        }
        try {
            if (this.plant.needToRecalculateColors) {
                this.calculateColors();
            }
            if ((this.isFirstPhytomer) && (this.plant.pRoot.showsAboveGround)) {
                this.drawRootTop();
            }
            this.drawInternode();
            if (this.leftLeaf != null) {
                this.leftLeaf.drawWithDirection(uplant.kDirectionLeft);
            }
            if (this.rightLeaf != null) {
                this.rightLeaf.drawWithDirection(uplant.kDirectionRight);
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInternode.draw");
        }
    }
    
    public void drawInternode() {
        float length = 0.0;
        float width = 0.0;
        float zAngle = 0.0;
        
        if ((this.plant.turtle == null)) {
            return;
        }
        zAngle = this.internodeAngle;
        if ((this.phytomerAttachedTo != null)) {
            if ((this.phytomerAttachedTo.leftBranchPlantPart == this)) {
                zAngle = zAngle + this.plant.pMeristem.branchingAngle;
            } else if ((this.phytomerAttachedTo.rightBranchPlantPart == this)) {
                zAngle = zAngle + this.plant.pMeristem.branchingAngle;
                this.plant.turtle.rotateX(128);
            }
        }
        len = umath.max(0.0, this.propFullLength() * this.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm);
        width = umath.max(0.0, this.propFullWidth() * this.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm);
        this.drawStemSegment(len, width, zAngle, 0, this.internodeColor, upart.kDontTaper, u3dexport.kExportPartInternode, upart.kUseAmendment);
    }
    
    public void drawRootTop() {
        KfTurtle turtle = new KfTurtle();
        float scale = 0.0;
        int numParts = 0;
        KfObject3D tdo = new KfObject3D();
        float minZ = 0.0;
        int i = 0;
        
        //Draw top of root above ground, if it can be seen. Adjust size for heat unit index of plant. 
        //constant
        numParts = 5;
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        scale = umath.safedivExcept(this.plant.age, this.plant.pGeneral.ageAtMaturity, 0) * this.plant.pRoot.tdoParams.scaleAtFullSize / 100.0;
        turtle.push();
        minZ = 0;
        tdo = this.plant.pRoot.tdoParams.object3D;
        turtle.ifExporting_startPlantPart(this.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartRootTop), this.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartRootTop));
        if (numParts > 0) {
            for (i = 0; i <= numParts - 1; i++) {
                turtle.rotateX(256 / numParts);
                turtle.push();
                turtle.rotateZ(64);
                turtle.rotateY(-64);
                if (tdo != null) {
                    turtle.rotateX(this.angleWithSway(this.plant.pRoot.tdoParams.xRotationBeforeDraw));
                    turtle.rotateY(this.angleWithSway(this.plant.pRoot.tdoParams.yRotationBeforeDraw));
                    turtle.rotateZ(this.angleWithSway(this.plant.pRoot.tdoParams.zRotationBeforeDraw));
                    this.draw3DObject(tdo, scale, this.plant.pRoot.tdoParams.faceColor, this.plant.pRoot.tdoParams.backfaceColor, u3dexport.kExportPartRootTop);
                    if (i == 1) {
                        minZ = tdo.zForSorting;
                    } else if (tdo.zForSorting < minZ) {
                        minZ = tdo.zForSorting;
                    }
                }
                turtle.pop();
            }
        }
        if (tdo != null) {
            tdo.zForSorting = minZ;
        }
        turtle.pop();
        turtle.ifExporting_endPlantPart();
    }
    
    public void report() {
        super.report();
        //debugPrint('internode, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
        //DebugForm.printNested(plant.turtle.stackSize, 'phytomer, age ' + IntToStr(age));
    }
    
    public void checkIfSeedlingLeavesHaveAbscissed() {
        if ((!this.isFirstPhytomer)) {
            //If first phytomer, only want to draw seedling leaves for some time after emergence.
            //  For monopodial plant, stop drawing seedling leaves some number of nodes after emergence (parameter).
            //  For sympodial plant, this doesn't work; use age of meristem instead; age is set as constant.
            return;
        }
        if ((this.plant.pMeristem.branchingIsSympodial)) {
            if ((this.age < 10)) {
                return;
            }
        } else {
            if ((this.distanceFromApicalMeristem() <= this.plant.pSeedlingLeaf.nodesOnStemWhenFallsOff)) {
                return;
            }
        }
        if (umath.safedivExcept(this.plant.age, this.plant.pGeneral.ageAtMaturity, 0) < 0.25) {
            // absolute cut-off 
            return;
        }
        if (this.leftLeaf != null) {
            // CFK FIX - should really have removed biomass in seedling leaves from model plant 
            this.leftLeaf.hasFallenOff = true;
        }
        if (this.rightLeaf != null) {
            this.rightLeaf.hasFallenOff = true;
        }
    }
    
    public int partType() {
        result = 0;
        result = uplant.kPartTypePhytomer;
        return result;
    }
    
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kPdInternode;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        super.streamDataWithFiler(filer, cvir);
        filer.streamColorRef(this.internodeColor);
        this.internodeAngle = filer.streamSingle(this.internodeAngle);
        this.lengthExpansion = filer.streamSingle(this.lengthExpansion);
        this.widthExpansion = filer.streamSingle(this.widthExpansion);
        this.boltingExpansion = filer.streamSingle(this.boltingExpansion);
        this.fractionOfOptimalInitialBiomassAtCreation_frn = filer.streamSingle(this.fractionOfOptimalInitialBiomassAtCreation_frn);
        this.traversingDirection = filer.streamByte(this.traversingDirection);
        this.isFirstPhytomer = filer.streamBoolean(this.isFirstPhytomer);
        this.newBiomassForDay_pctMPB = filer.streamSingle(this.newBiomassForDay_pctMPB);
        //reading or writing the plant part subobject phytomers will be done by traverser
        //for now, just need to create these objects if needed and set plant and phytomerAttachedTo
        //if it is an inflorescence - read it now
        this.streamPlantPart(filer, this.leftBranchPlantPart);
        this.streamPlantPart(filer, this.rightBranchPlantPart);
        this.streamPlantPart(filer, this.nextPlantPart);
        this.streamPlantPart(filer, upart.PdPlantPart(this.leftLeaf));
        this.streamPlantPart(filer, upart.PdPlantPart(this.rightLeaf));
    }
    
    public void streamPlantPart(PdFiler filer, PdPlantPart plantPart) {
        raise "method streamPlantPart had assigned to var parameter plantPart not added to return; fixup manually"
        short partType = 0;
        
        if (filer.isWriting()) {
            if (plantPart == null) {
                partType = uplant.kPartTypeNone;
            } else {
                partType = plantPart.partType();
            }
            partType = filer.streamSmallint(partType);
            switch (partType) {
                case uplant.kPartTypeMeristem:
                    plantPart.streamUsingFiler(filer);
                    break;
                case uplant.kPartTypeInflorescence:
                    plantPart.streamUsingFiler(filer);
                    break;
                case uplant.kPartTypeLeaf:
                    plantPart.streamUsingFiler(filer);
                    break;
        } else if (filer.isReading()) {
            partType = filer.streamSmallint(partType);
            switch (partType) {
                case uplant.kPartTypeNone:
                    plantPart = null;
                    break;
                case uplant.kPartTypeMeristem:
                    plantPart = umerist.PdMeristem().create();
                    plantPart.plant = this.plant;
                    umerist.PdMeristem(plantPart).phytomerAttachedTo = this;
                    plantPart.streamUsingFiler(filer);
                    break;
                case uplant.kPartTypeInflorescence:
                    plantPart = uinflor.PdInflorescence().create();
                    plantPart.plant = this.plant;
                    uinflor.PdInflorescence(plantPart).phytomerAttachedTo = this;
                    plantPart.streamUsingFiler(filer);
                    break;
                case uplant.kPartTypePhytomer:
                    plantPart = PdInternode().create();
                    plantPart.plant = this.plant;
                    PdInternode(plantPart).phytomerAttachedTo = this;
                    //will be streamed in by traverser
                    break;
                case uplant.kPartTypeLeaf:
                    plantPart = uleaf.PdLeaf().create();
                    plantPart.plant = this.plant;
                    plantPart.streamUsingFiler(filer);
                    // PDF PORT inserted semicolon
                    break;
                default:
                    GeneralException.create("PdInternode: unknown plant part type " + IntToStr(partType));
                    break;
        }
    }
    
}
