// unit ufruit

from conversion_common import *;
import u3dexport;
import uturtle;
import usupport;
import utravers;
import ufiler;
import utdo;
import uplant;
import umath;
import upart;
import delphi_compatability;

// const
kDrawFlowerAsOpening = true;
kDontDrawFlowerAsOpening = false;
kLine = true;
kNotLine = false;


// const
kDrawTDOOpen = true;
kDrawTDOClosed = false;



//  kBud = 0; kPistil = 1; kStamens = 2; kFirstPetals = 3; kSecondPetals = 4; kThirdPetals = 5; kSepals = 6;
class PdFlowerFruit extends PdPlantPart {
    public float propFullSize;
    public short stage;
    public boolean hasBeenDrawn;
    public long daysAccumulatingFruitBiomass;
    public long daysOpen;
    
    public void initializeGender(PdPlant aPlant, int aGender) {
        this.initialize(aPlant);
        this.gender = aGender;
        this.propFullSize = 0.0;
        this.liveBiomass_pctMPB = 0.0;
        this.deadBiomass_pctMPB = 0.0;
        this.biomassDemand_pctMPB = 0.0;
        this.stage = uplant.kStageFlowerBud;
        this.hasBeenDrawn = false;
    }
    
    public String getName() {
        result = "";
        result = "flower/fruit";
        return result;
    }
    
    public void nextDay() {
        float anthesisLoss_pctMPB = 0.0;
        float biomassToMakeFruit_pctMPB = 0.0;
        boolean minDaysWithOptimalBiomass = false;
        boolean maxDaysWithMinFraction = false;
        
        if (this.hasFallenOff) {
            return;
        }
        try {
            super.nextDay();
            switch (this.stage) {
                case uplant.kStageFlowerBud:
                    if (((this.liveBiomass_pctMPB >= this.plant.pFlower[self.gender].minFractionOfOptimalBiomassToOpenFlower_frn * this.plant.pFlower[self.gender].optimalBiomass_pctMPB) || (this.age > this.plant.pFlower[self.gender].maxDaysToGrowIfOverMinFraction)) && (this.age > this.plant.pFlower[self.gender].minDaysToOpenFlower)) {
                        //if over required fraction of optimal or over max days to grow, open bud
                        this.stage = uplant.kStageOpenFlower;
                        this.daysOpen = 0;
                    }
                    break;
                case uplant.kStageOpenFlower:
                    //if over optimal or over min fraction to create fruit and over max days to grow, set fruit
                    this.daysOpen += 1;
                    if (this.daysOpen > this.plant.pFlower[this.gender].daysBeforeDrop) {
                        this.hasFallenOff = true;
                    } else if (this.gender != uplant.kGenderMale) {
                        if (this.age > this.plant.pFlower[self.gender].minDaysBeforeSettingFruit) {
                            // limit on time to set fruit (as opposed to grow) if want to keep flowers on plant longer
                            // upper limit on growth; must be at least as old as minDaysToGrow unless there is optimal biomass
                            minDaysWithOptimalBiomass = (this.age > this.plant.pFlower[self.gender].minDaysToGrow) && (this.liveBiomass_pctMPB >= this.plant.pFlower[self.gender].optimalBiomass_pctMPB);
                            // lower limit on growth; if don't have enough to make fruit, give up after max days and make anyway
                            biomassToMakeFruit_pctMPB = this.plant.pFlower[self.gender].minFractionOfOptimalBiomassToCreateFruit_frn * this.plant.pFlower[self.gender].optimalBiomass_pctMPB;
                            maxDaysWithMinFraction = (this.age > this.plant.pFlower[self.gender].maxDaysToGrowIfOverMinFraction) || (this.liveBiomass_pctMPB >= biomassToMakeFruit_pctMPB);
                            if (maxDaysWithMinFraction || minDaysWithOptimalBiomass) {
                                this.stage = uplant.kStageUnripeFruit;
                                this.daysAccumulatingFruitBiomass = 0;
                                // flower biomass drops off, 50% goes into developing fruit (ovary) 
                                // choice of 50% is arbitrary - could be parameter in future depending on size of flower parts/ovary 
                                anthesisLoss_pctMPB = this.liveBiomass_pctMPB * 0.5;
                                this.liveBiomass_pctMPB = this.liveBiomass_pctMPB - anthesisLoss_pctMPB;
                                this.deadBiomass_pctMPB = this.deadBiomass_pctMPB + anthesisLoss_pctMPB;
                                this.propFullSize = (umath.min(1.0, umath.safedivExcept(this.totalBiomass_pctMPB(), this.plant.pFruit.optimalBiomass_pctMPB, 0.0)));
                            }
                        }
                    }
                    break;
                case uplant.kStageUnripeFruit:
                    if ((this.stage == uplant.kStageUnripeFruit) && (this.daysAccumulatingFruitBiomass >= this.plant.pFruit.daysToRipen)) {
                        this.stage = uplant.kStageRipeFruit;
                    }
                    this.daysAccumulatingFruitBiomass += 1;
                    break;
                case uplant.kStageRipeFruit:
                    if ((this.stage == uplant.kStageUnripeFruit) && (this.daysAccumulatingFruitBiomass >= this.plant.pFruit.daysToRipen)) {
                        this.stage = uplant.kStageRipeFruit;
                    }
                    this.daysAccumulatingFruitBiomass += 1;
                    break;
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdFlowerFruit.nextDay");
        }
    }
    
    public void traverseActivity(int mode, TObject traverserProxy) {
        PdTraverser traverser = new PdTraverser();
        float newPropFullSize = 0.0;
        float newBiomass_pctMPB = 0.0;
        float newOptimalBiomass_pctMPB = 0.0;
        float biomassToRemove_pctMPB = 0.0;
        float fractionOfMaxAge_frn = 0.0;
        
        super.traverseActivity(mode, traverserProxy);
        traverser = utravers.PdTraverser(traverserProxy);
        if (traverser == null) {
            return;
        }
        if (this.hasFallenOff && (mode != utravers.kActivityStream) && (mode != utravers.kActivityFree) && (mode != utravers.kActivityGatherStatistics)) {
            return;
        }
        try {
            switch (mode) {
                case utravers.kActivityNone:
                    break;
                case utravers.kActivityNextDay:
                    this.nextDay();
                    break;
                case utravers.kActivityDemandVegetative:
                    break;
                case utravers.kActivityDemandReproductive:
                    switch (this.stage) {
                        case uplant.kStageFlowerBud:
                            // has no vegetative demand 
                            // accum. biomass for flower 
                            this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, this.plant.pFlower[self.gender].optimalBiomass_pctMPB, this.plant.pFlower[self.gender].minDaysToGrow);
                            traverser.total = traverser.total + this.biomassDemand_pctMPB;
                            break;
                        case uplant.kStageOpenFlower:
                            // has no vegetative demand 
                            // accum. biomass for flower 
                            this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, this.plant.pFlower[self.gender].optimalBiomass_pctMPB, this.plant.pFlower[self.gender].minDaysToGrow);
                            traverser.total = traverser.total + this.biomassDemand_pctMPB;
                            break;
                        case uplant.kStageUnripeFruit:
                            if (this.daysAccumulatingFruitBiomass > this.plant.pFruit.maxDaysToGrow) {
                                // accum. biomass for fruit 
                                this.biomassDemand_pctMPB = 0.0;
                            } else {
                                fractionOfMaxAge_frn = umath.safedivExcept(this.daysAccumulatingFruitBiomass + 1, this.plant.pFruit.maxDaysToGrow, 0.0);
                                newPropFullSize = umath.max(0.0, umath.min(1.0, umath.scurve(fractionOfMaxAge_frn, this.plant.pFruit.sCurveParams.c1, this.plant.pFruit.sCurveParams.c2)));
                                newOptimalBiomass_pctMPB = newPropFullSize * this.plant.pFruit.optimalBiomass_pctMPB;
                                this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, newOptimalBiomass_pctMPB, 1);
                                traverser.total = traverser.total + this.biomassDemand_pctMPB;
                            }
                            break;
                        case uplant.kStageRipeFruit:
                            if (this.daysAccumulatingFruitBiomass > this.plant.pFruit.maxDaysToGrow) {
                                // accum. biomass for fruit 
                                this.biomassDemand_pctMPB = 0.0;
                            } else {
                                fractionOfMaxAge_frn = umath.safedivExcept(this.daysAccumulatingFruitBiomass + 1, this.plant.pFruit.maxDaysToGrow, 0.0);
                                newPropFullSize = umath.max(0.0, umath.min(1.0, umath.scurve(fractionOfMaxAge_frn, this.plant.pFruit.sCurveParams.c1, this.plant.pFruit.sCurveParams.c2)));
                                newOptimalBiomass_pctMPB = newPropFullSize * this.plant.pFruit.optimalBiomass_pctMPB;
                                this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, newOptimalBiomass_pctMPB, 1);
                                traverser.total = traverser.total + this.biomassDemand_pctMPB;
                            }
                            break;
                    break;
                case utravers.kActivityGrowVegetative:
                    break;
                case utravers.kActivityGrowReproductive:
                    // cannot grow vegetatively 
                    //Allocate portion of total new biomass based on this demand over total demand.
                    newBiomass_pctMPB = this.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
                    this.liveBiomass_pctMPB = this.liveBiomass_pctMPB + newBiomass_pctMPB;
                    switch (this.stage) {
                        case uplant.kStageFlowerBud:
                            this.propFullSize = (umath.min(1.0, umath.safedivExcept(this.totalBiomass_pctMPB(), this.plant.pFlower[this.gender].optimalBiomass_pctMPB, 0.0)));
                            break;
                        case uplant.kStageOpenFlower:
                            this.propFullSize = (umath.min(1.0, umath.safedivExcept(this.totalBiomass_pctMPB(), this.plant.pFlower[this.gender].optimalBiomass_pctMPB, 0.0)));
                            break;
                        case uplant.kStageUnripeFruit:
                            this.propFullSize = (umath.min(1.0, umath.safedivExcept(this.totalBiomass_pctMPB(), this.plant.pFruit.optimalBiomass_pctMPB, 0.0)));
                            break;
                        case uplant.kStageRipeFruit:
                            this.propFullSize = (umath.min(1.0, umath.safedivExcept(this.totalBiomass_pctMPB(), this.plant.pFruit.optimalBiomass_pctMPB, 0.0)));
                            break;
                    break;
                case utravers.kActivityStartReproduction:
                    break;
                case utravers.kActivityFindPlantPartAtPosition:
                    if (umath.pointsAreCloseEnough(traverser.point, this.position())) {
                        // can't switch because has no vegetative mode 
                        traverser.foundPlantPart = this;
                        traverser.finished = true;
                    }
                    break;
                case utravers.kActivityDraw:
                    break;
                case utravers.kActivityReport:
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
                    // inflorescence should handle telling flowers to draw 
                    //streaming called by inflorescence
                    // free called by inflorescence 
                    // none 
                    // do nothing 
                    traverser.total = traverser.total + this.liveBiomass_pctMPB;
                    break;
                case utravers.kActivityRemoveReproductiveBiomass:
                    if (this.liveBiomass_pctMPB <= 0.0) {
                        return;
                    }
                    biomassToRemove_pctMPB = this.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
                    this.liveBiomass_pctMPB = this.liveBiomass_pctMPB - biomassToRemove_pctMPB;
                    this.deadBiomass_pctMPB = this.deadBiomass_pctMPB + biomassToRemove_pctMPB;
                    if (this.liveBiomass_pctMPB <= 0.0) {
                        if ((this.stage == uplant.kStageUnripeFruit) || (this.stage == uplant.kStageRipeFruit)) {
                            this.hasFallenOff = true;
                        }
                    }
                    break;
                case utravers.kActivityGatherStatistics:
                    switch (this.stage) {
                        case uplant.kStageFlowerBud:
                            if (this.gender == uplant.kGenderMale) {
                                if (this.hasFallenOff) {
                                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFlower);
                                } else {
                                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeMaleFlowerBud);
                                }
                            } else {
                                if (this.hasFallenOff) {
                                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFlower);
                                } else {
                                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFemaleFlowerBud);
                                }
                            }
                            break;
                        case uplant.kStageOpenFlower:
                            if (this.gender == uplant.kGenderMale) {
                                if (this.hasFallenOff) {
                                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFlower);
                                } else {
                                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeMaleFlower);
                                }
                            } else {
                                if (this.hasFallenOff) {
                                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFlower);
                                } else {
                                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFemaleFlower);
                                }
                            }
                            break;
                        case uplant.kStageUnripeFruit:
                            if (this.hasFallenOff) {
                                this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFruit);
                            } else {
                                this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeUnripeFruit);
                            }
                            break;
                        case uplant.kStageRipeFruit:
                            if (this.hasFallenOff) {
                                this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFruit);
                            } else {
                                this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFruit);
                            }
                            break;
                        default:
                            throw new GeneralException.create("Problem: Invalid fruit stage in method PdFlowerFruit.traverseActivity.");
                            break;
                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllReproductive);
                    break;
                case utravers.kActivityCountPlantParts:
                    break;
                case utravers.kActivityFindPartForPartID:
                    break;
                case utravers.kActivityCountTotalMemoryUse:
                    traverser.totalMemorySize += this.instanceSize;
                    break;
                case utravers.kActivityCalculateBiomassForGravity:
                    break;
                case utravers.kActivityCountPointsAndTrianglesFor3DExport:
                    this.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser);
                    break;
                default:
                    throw new GeneralException.create("Problem: Unhandled mode for plant draw activity in method PdFlowerFruit.traverseActivity.");
                    break;
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdFlowerFruit.traverseActivity");
        }
    }
    
    public void report() {
        super.report();
        // DebugPrint(' flower/fruit, age '  + IntToStr(age) + ' biomass '  + floatToStr(self.liveBiomass_pctMPB));
    }
    
    public short dxfIndexForFloralLayerType(short aType, boolean line) {
        result = 0;
        result = 0;
        switch (aType) {
            case uplant.kBud:
                result = u3dexport.kExportPartFlowerBudFemale;
                break;
            case uplant.kPistils:
                if (line) {
                    result = u3dexport.kExportPartStyleFemale;
                } else {
                    result = u3dexport.kExportPartStigmaFemale;
                }
                break;
            case uplant.kStamens:
                if (line) {
                    result = u3dexport.kExportPartFilamentFemale;
                } else {
                    result = u3dexport.kExportPartAntherFemale;
                }
                break;
            case uplant.kFirstPetals:
                result = u3dexport.kExportPartFirstPetalsFemale;
                break;
            case uplant.kSecondPetals:
                result = u3dexport.kExportPartSecondPetalsFemale;
                break;
            case uplant.kThirdPetals:
                result = u3dexport.kExportPartThirdPetalsFemale;
                break;
            case uplant.kFourthPetals:
                result = u3dexport.kExportPartFourthPetalsFemale;
                break;
            case uplant.kFifthPetals:
                result = u3dexport.kExportPartFifthPetalsFemale;
                break;
            case uplant.kSepals:
                result = u3dexport.kExportPartSepalsFemale;
                break;
        return result;
    }
    
    public void draw() {
        float scale = 0.0;
        float length = 0.0;
        float width = 0.0;
        KfTurtle turtle = new KfTurtle();
        
        if ((this.plant.turtle == null)) {
            return;
        }
        turtle = this.plant.turtle;
        this.boundsRect = Rect(0, 0, 0, 0);
        if (this.hasFallenOff) {
            return;
        }
        turtle.push();
        this.determineAmendmentAndAlsoForChildrenIfAny();
        if (this.hiddenByAmendment()) {
            turtle.pop();
            return;
        } else {
            this.applyAmendmentRotations();
        }
        try {
            switch (this.stage) {
                case uplant.kStageFlowerBud:
                    switch (this.plant.pFlower[this.gender].budDrawingOption) {
                        case uplant.kDrawNoBud:
                            // kDrawNoBud = 0; kDrawSingleTdoBud = 1; kDrawOpeningFlower = 2;
                            return;
                            break;
                        case uplant.kDrawSingleTdoBud:
                            scale = ((this.plant.pFlower[self.gender].tdoParams[uplant.kBud].scaleAtFullSize / 100.0) * this.propFullSize);
                            turtle.rotateX(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kBud].xRotationBeforeDraw));
                            turtle.rotateY(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kBud].yRotationBeforeDraw));
                            turtle.rotateZ(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kBud].zRotationBeforeDraw));
                            this.drawCircleOfTdos(this.plant.pFlower[self.gender].tdoParams[uplant.kBud].object3D, this.plant.pFlower[self.gender].tdoParams[uplant.kBud].faceColor, this.plant.pFlower[self.gender].tdoParams[uplant.kBud].backfaceColor, this.plant.pFlower[self.gender].tdoParams[uplant.kBud].pullBackAngle, scale, this.plant.pFlower[self.gender].tdoParams[uplant.kBud].repetitions, this.plant.pFlower[self.gender].tdoParams[uplant.kBud].radiallyArranged, kDrawTDOClosed, u3dexport.kExportPartFlowerBudFemale);
                            break;
                        case uplant.kDrawOpeningFlower:
                            this.drawFlower(kDrawFlowerAsOpening);
                            break;
                    break;
                case uplant.kStageOpenFlower:
                    this.drawFlower(kDontDrawFlowerAsOpening);
                    break;
                case uplant.kStageUnripeFruit:
                    // ripe color is regular color; alternate color is unripe color
                    scale = ((this.plant.pFruit.tdoParams.scaleAtFullSize / 100.0) * this.propFullSize);
                    turtle.rotateX(this.angleWithSway(this.plant.pFruit.tdoParams.xRotationBeforeDraw));
                    turtle.rotateY(this.angleWithSway(this.plant.pFruit.tdoParams.yRotationBeforeDraw));
                    turtle.rotateZ(this.angleWithSway(this.plant.pFruit.tdoParams.zRotationBeforeDraw));
                    this.drawCircleOfTdos(this.plant.pFruit.tdoParams.object3D, this.plant.pFruit.tdoParams.alternateFaceColor, this.plant.pFruit.tdoParams.alternateBackfaceColor, this.plant.pFruit.tdoParams.pullBackAngle, scale, this.plant.pFruit.tdoParams.repetitions, this.plant.pFruit.tdoParams.radiallyArranged, kDrawTDOClosed, u3dexport.kExportPartUnripeFruit);
                    break;
                case uplant.kStageRipeFruit:
                    scale = ((this.plant.pFruit.tdoParams.scaleAtFullSize / 100.0) * this.propFullSize);
                    turtle.rotateX(this.angleWithSway(this.plant.pFruit.tdoParams.xRotationBeforeDraw));
                    turtle.rotateY(this.angleWithSway(this.plant.pFruit.tdoParams.yRotationBeforeDraw));
                    turtle.rotateZ(this.angleWithSway(this.plant.pFruit.tdoParams.zRotationBeforeDraw));
                    this.drawCircleOfTdos(this.plant.pFruit.tdoParams.object3D, this.plant.pFruit.tdoParams.faceColor, this.plant.pFruit.tdoParams.backfaceColor, this.plant.pFruit.tdoParams.pullBackAngle, scale, this.plant.pFruit.tdoParams.repetitions, this.plant.pFruit.tdoParams.radiallyArranged, kDrawTDOClosed, u3dexport.kExportPartRipeFruit);
                    break;
            this.hasBeenDrawn = true;
            turtle.pop();
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdFlowerFruit.draw");
        }
    }
    
    public void drawFlower(boolean drawAsOpening) {
        KfTurtle turtle = new KfTurtle();
        float angle = 0.0;
        float scale = 0.0;
        short layerType = 0;
        
        if ((this.plant.turtle == null)) {
            return;
        }
        turtle = this.plant.turtle;
        this.drawPistilsAndStamens(drawAsOpening);
        for (layerType = uplant.kFirstPetals; layerType <= uplant.kSepals; layerType++) {
            turtle.push();
            scale = ((this.plant.pFlower[self.gender].tdoParams[layerType].scaleAtFullSize / 100.0) * this.propFullSize);
            angle = this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle);
            if (drawAsOpening) {
                angle = angle * this.propFullSize * 2;
                if (angle > this.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle) {
                    angle = this.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle;
                }
            }
            turtle.rotateX(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[layerType].xRotationBeforeDraw));
            turtle.rotateY(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[layerType].yRotationBeforeDraw));
            turtle.rotateZ(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[layerType].zRotationBeforeDraw));
            this.drawCircleOfTdos(this.plant.pFlower[self.gender].tdoParams[layerType].object3D, this.plant.pFlower[self.gender].tdoParams[layerType].faceColor, this.plant.pFlower[self.gender].tdoParams[layerType].backfaceColor, angle, scale, this.plant.pFlower[self.gender].tdoParams[layerType].repetitions, this.plant.pFlower[self.gender].tdoParams[layerType].radiallyArranged, kDrawTDOOpen, this.dxfIndexForFloralLayerType(layerType, kNotLine));
            turtle.pop();
        }
    }
    
    public void drawPistilsAndStamens(boolean drawAsOpening) {
        float scale = 0.0;
        float length = 0.0;
        float width = 0.0;
        float angle = 0.0;
        KfTurtle turtle = new KfTurtle();
        short i = 0;
        int turnPortion = 0;
        int leftOverDegrees = 0;
        int addThisTime = 0;
        float addition = 0.0;
        float carryOver = 0.0;
        
        if ((this.plant.turtle == null)) {
            return;
        }
        turtle = this.plant.turtle;
        turtle.push();
        if ((this.plant.pFlower[self.gender].numPistils > 0)) {
            if (((this.plant.pFlower[self.gender].styleLength_mm > 0) && (this.plant.pFlower[self.gender].styleWidth_mm > 0)) || (this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].scaleAtFullSize > 0)) {
                turtle.ifExporting_startNestedGroupOfPlantParts("pistils", "Pistils", u3dexport.kNestingTypeFloralLayers);
            }
            turnPortion = 256 / this.plant.pFlower[self.gender].numPistils;
            leftOverDegrees = 256 - turnPortion * this.plant.pFlower[self.gender].numPistils;
            if (leftOverDegrees > 0) {
                addition = umath.safedivExcept(leftOverDegrees, this.plant.pFlower[self.gender].numPistils, 0);
            } else {
                addition = 0;
            }
            carryOver = 0;
            for (i = 0; i <= this.plant.pFlower[self.gender].numPistils - 1; i++) {
                turtle.push();
                if ((this.plant.pFlower[self.gender].styleLength_mm > 0) && (this.plant.pFlower[self.gender].styleWidth_mm > 0)) {
                    len = umath.max(0.0, this.propFullSize * this.plant.pFlower[self.gender].styleLength_mm);
                    width = umath.max(0.0, this.propFullSize * this.plant.pFlower[self.gender].styleWidth_mm);
                    angle = this.angleWithSway(this.plant.pFlower[this.gender].tdoParams[uplant.kPistils].pullBackAngle);
                    if (drawAsOpening) {
                        angle = angle * this.propFullSize;
                    }
                    this.drawStemSegment(len, width, angle, 0, this.plant.pFlower[self.gender].styleColor, this.plant.pFlower[self.gender].styleTaperIndex, this.dxfIndexForFloralLayerType(uplant.kPistils, kLine), upart.kDontUseAmendment);
                }
                scale = ((this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].scaleAtFullSize / 100.0) * this.propFullSize);
                turtle.rotateX(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].xRotationBeforeDraw));
                turtle.rotateY(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].yRotationBeforeDraw));
                turtle.rotateZ(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].zRotationBeforeDraw));
                this.drawCircleOfTdos(this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].object3D, this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].faceColor, this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].backfaceColor, 0, scale, this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].repetitions, this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].radiallyArranged, kDrawTDOOpen, this.dxfIndexForFloralLayerType(uplant.kPistils, kNotLine));
                turtle.pop();
                addThisTime = trunc(addition + carryOver);
                carryOver = carryOver + addition - addThisTime;
                if (carryOver < 0) {
                    carryOver = 0;
                }
                turtle.rotateX(turnPortion + addThisTime);
            }
            if (((this.plant.pFlower[self.gender].styleLength_mm > 0) && (this.plant.pFlower[self.gender].styleWidth_mm > 0)) || (this.plant.pFlower[self.gender].tdoParams[uplant.kPistils].scaleAtFullSize > 0)) {
                turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeFloralLayers);
            }
        }
        turtle.pop();
        // stamens
        turtle.push();
        if (this.plant.pFlower[self.gender].numStamens > 0) {
            if (((this.plant.pFlower[self.gender].filamentLength_mm > 0) && (this.plant.pFlower[self.gender].filamentWidth_mm > 0)) || (this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].scaleAtFullSize > 0)) {
                if (this.gender == uplant.kGenderFemale) {
                    turtle.ifExporting_startNestedGroupOfPlantParts("primary stamens", "1Stamens", u3dexport.kNestingTypeFloralLayers);
                } else {
                    turtle.ifExporting_startNestedGroupOfPlantParts("secondary stamens", "2Stamens", u3dexport.kNestingTypeFloralLayers);
                }
            }
            turnPortion = 256 / this.plant.pFlower[self.gender].numStamens;
            leftOverDegrees = 256 - turnPortion * this.plant.pFlower[self.gender].numStamens;
            if (leftOverDegrees > 0) {
                addition = umath.safedivExcept(leftOverDegrees, this.plant.pFlower[self.gender].numStamens, 0);
            } else {
                addition = 0;
            }
            carryOver = 0;
            for (i = 0; i <= this.plant.pFlower[self.gender].numStamens - 1; i++) {
                turtle.push();
                if ((this.plant.pFlower[self.gender].filamentLength_mm > 0) && (this.plant.pFlower[self.gender].filamentWidth_mm > 0)) {
                    len = umath.max(0.0, this.propFullSize * this.plant.pFlower[self.gender].filamentLength_mm);
                    width = umath.max(0.0, this.propFullSize * this.plant.pFlower[self.gender].filamentWidth_mm);
                    angle = this.angleWithSway(this.plant.pFlower[this.gender].tdoParams[uplant.kStamens].pullBackAngle);
                    if (drawAsOpening) {
                        angle = angle * this.propFullSize;
                    }
                    this.drawStemSegment(len, width, angle, 0, this.plant.pFlower[self.gender].filamentColor, this.plant.pFlower[self.gender].filamentTaperIndex, this.dxfIndexForFloralLayerType(uplant.kStamens, kLine), upart.kDontUseAmendment);
                }
                scale = ((this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].scaleAtFullSize / 100.0) * this.propFullSize);
                turtle.rotateX(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].xRotationBeforeDraw));
                turtle.rotateY(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].yRotationBeforeDraw));
                turtle.rotateZ(this.angleWithSway(this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].zRotationBeforeDraw));
                this.drawCircleOfTdos(this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].object3D, this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].faceColor, this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].backfaceColor, 0, scale, this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].repetitions, this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].radiallyArranged, kDrawTDOOpen, this.dxfIndexForFloralLayerType(uplant.kStamens, kNotLine));
                turtle.pop();
                addThisTime = trunc(addition + carryOver);
                carryOver = carryOver + addition - addThisTime;
                if (carryOver < 0) {
                    carryOver = 0;
                }
                turtle.rotateX(turnPortion + addThisTime);
            }
            if (((this.plant.pFlower[self.gender].filamentLength_mm > 0) && (this.plant.pFlower[self.gender].filamentWidth_mm > 0)) || (this.plant.pFlower[self.gender].tdoParams[uplant.kStamens].scaleAtFullSize > 0)) {
                turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeFloralLayers);
            }
        }
        turtle.pop();
    }
    
    public void countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(PdTraverser traverser) {
        int numLines = 0;
        
        if (traverser == null) {
            return;
        }
        if (this.propFullSize <= 0) {
            return;
        }
        if (this.hasFallenOff) {
            return;
        }
        switch (this.stage) {
            case uplant.kStageFlowerBud:
                switch (this.plant.pFlower[this.gender].budDrawingOption) {
                    case uplant.kDrawNoBud:
                        break;
                    case uplant.kDrawSingleTdoBud:
                        if (this.plant.pFlower[self.gender].tdoParams[uplant.kBud].scaleAtFullSize > 0) {
                            traverser.total3DExportPointsIn3DObjects += this.plant.pFlower[self.gender].tdoParams[uplant.kBud].object3D.pointsInUse * this.plant.pFlower[self.gender].tdoParams[uplant.kBud].repetitions;
                            traverser.total3DExportTrianglesIn3DObjects += this.plant.pFlower[self.gender].tdoParams[uplant.kBud].object3D.triangles.Count * this.plant.pFlower[self.gender].tdoParams[uplant.kBud].repetitions;
                            this.addExportMaterial(traverser, u3dexport.kExportPartFlowerBudFemale, u3dexport.kExportPartFlowerBudMale);
                        }
                        break;
                    case uplant.kDrawOpeningFlower:
                        this.addFloralPartsCountsToTraverser(traverser);
                        break;
                break;
            case uplant.kStageOpenFlower:
                this.addFloralPartsCountsToTraverser(traverser);
                break;
            case uplant.kStageUnripeFruit:
                if (this.plant.pFruit.tdoParams.scaleAtFullSize > 0) {
                    traverser.total3DExportPointsIn3DObjects += this.plant.pFruit.tdoParams.object3D.pointsInUse * this.plant.pFruit.tdoParams.repetitions;
                    traverser.total3DExportTrianglesIn3DObjects += this.plant.pFruit.tdoParams.object3D.triangles.Count * this.plant.pFruit.tdoParams.repetitions;
                    if (this.stage == uplant.kStageUnripeFruit) {
                        this.addExportMaterial(traverser, u3dexport.kExportPartUnripeFruit, -1);
                    } else {
                        this.addExportMaterial(traverser, u3dexport.kExportPartRipeFruit, -1);
                    }
                }
                break;
            case uplant.kStageRipeFruit:
                if (this.plant.pFruit.tdoParams.scaleAtFullSize > 0) {
                    traverser.total3DExportPointsIn3DObjects += this.plant.pFruit.tdoParams.object3D.pointsInUse * this.plant.pFruit.tdoParams.repetitions;
                    traverser.total3DExportTrianglesIn3DObjects += this.plant.pFruit.tdoParams.object3D.triangles.Count * this.plant.pFruit.tdoParams.repetitions;
                    if (this.stage == uplant.kStageUnripeFruit) {
                        this.addExportMaterial(traverser, u3dexport.kExportPartUnripeFruit, -1);
                    } else {
                        this.addExportMaterial(traverser, u3dexport.kExportPartRipeFruit, -1);
                    }
                }
                break;
        // pedicel handled by inflorescence
    }
    
    public void addFloralPartsCountsToTraverser(PdTraverser traverser) {
        int partType = 0;
        
        for (partType = uplant.kPistils; partType <= uplant.kSepals; partType++) {
            if (this.plant.pFlower[self.gender].tdoParams[partType].scaleAtFullSize > 0) {
                if (partType == uplant.kPistils) {
                    traverser.total3DExportPointsIn3DObjects += this.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * this.plant.pFlower[self.gender].tdoParams[partType].repetitions * this.plant.pFlower[this.gender].numPistils;
                    traverser.total3DExportTrianglesIn3DObjects += this.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * this.plant.pFlower[self.gender].tdoParams[partType].repetitions * this.plant.pFlower[this.gender].numPistils;
                    this.addExportMaterial(traverser, u3dexport.kExportPartStyleFemale, -1);
                    this.addExportMaterial(traverser, u3dexport.kExportPartStigmaFemale, -1);
                } else if (partType == uplant.kStamens) {
                    traverser.total3DExportPointsIn3DObjects += this.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * this.plant.pFlower[self.gender].tdoParams[partType].repetitions * this.plant.pFlower[this.gender].numStamens;
                    traverser.total3DExportTrianglesIn3DObjects += this.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * this.plant.pFlower[self.gender].tdoParams[partType].repetitions * this.plant.pFlower[this.gender].numStamens;
                    this.addExportMaterial(traverser, u3dexport.kExportPartFilamentFemale, u3dexport.kExportPartFilamentMale);
                    this.addExportMaterial(traverser, u3dexport.kExportPartAntherFemale, u3dexport.kExportPartAntherMale);
                } else {
                    traverser.total3DExportPointsIn3DObjects += this.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * this.plant.pFlower[self.gender].tdoParams[partType].repetitions;
                    traverser.total3DExportTrianglesIn3DObjects += this.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * this.plant.pFlower[self.gender].tdoParams[partType].repetitions;
                    switch (partType) {
                        case uplant.kFirstPetals:
                            this.addExportMaterial(traverser, u3dexport.kExportPartFirstPetalsFemale, u3dexport.kExportPartFirstPetalsMale);
                            break;
                        case uplant.kSecondPetals:
                            this.addExportMaterial(traverser, u3dexport.kExportPartSecondPetalsFemale, -1);
                            break;
                        case uplant.kThirdPetals:
                            this.addExportMaterial(traverser, u3dexport.kExportPartThirdPetalsFemale, -1);
                            break;
                        case uplant.kFourthPetals:
                            this.addExportMaterial(traverser, u3dexport.kExportPartFourthPetalsFemale, -1);
                            break;
                        case uplant.kFifthPetals:
                            this.addExportMaterial(traverser, u3dexport.kExportPartFifthPetalsFemale, -1);
                            break;
                        case uplant.kSepals:
                            this.addExportMaterial(traverser, u3dexport.kExportPartSepalsFemale, u3dexport.kExportPartSepalsMale);
                            break;
                }
            }
        }
    }
    
    public int triangleCountInFloralParts() {
        result = 0;
        int partType = 0;
        
        result = 0;
        for (partType = uplant.kPistils; partType <= uplant.kSepals; partType++) {
            if (this.plant.pFlower[self.gender].tdoParams[partType].scaleAtFullSize > 0) {
                if (partType == uplant.kPistils) {
                    result = result + this.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * this.plant.pFlower[self.gender].tdoParams[partType].repetitions * this.plant.pFlower[this.gender].numPistils;
                } else if (partType == uplant.kStamens) {
                    result = result + this.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * this.plant.pFlower[self.gender].tdoParams[partType].repetitions * this.plant.pFlower[this.gender].numStamens;
                } else {
                    result = result + this.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * this.plant.pFlower[self.gender].tdoParams[partType].repetitions;
                }
            }
        }
        return result;
    }
    
    public KfObject3D tdoToSortLinesWith() {
        result = new KfObject3D();
        result = null;
        if (this.plant == null) {
            return result;
        }
        if (this.hasFallenOff) {
            return result;
        }
        switch (this.stage) {
            case uplant.kStageFlowerBud:
                result = this.plant.pFlower[this.gender].tdoParams[uplant.kBud].object3D;
                break;
            case uplant.kStageOpenFlower:
                result = this.plant.pFlower[this.gender].tdoParams[uplant.kFirstPetals].object3D;
                break;
            case uplant.kStageUnripeFruit:
                result = this.plant.pFruit.tdoParams.object3D;
                break;
            case uplant.kStageRipeFruit:
                result = this.plant.pFruit.tdoParams.object3D;
                break;
        return result;
    }
    
    public void drawCircleOfTdos(KfObject3D tdo, TColorRef faceColor, TColorRef backfaceColor, float pullBackAngle, float scale, int numParts, boolean partsArranged, boolean open, short dxfIndex) {
        KfTurtle turtle = new KfTurtle();
        int i = 0;
        float minZ = 0.0;
        int turnPortion = 0;
        int leftOverDegrees = 0;
        int addThisTime = 0;
        float addition = 0.0;
        float carryOver = 0.0;
        
        try {
            if ((scale <= 0.0)) {
                // v1.3
                // v1.3
                return;
            }
            turtle = this.plant.turtle;
            if ((turtle == null)) {
                return;
            }
            turtle.push();
            minZ = 0;
            if ((partsArranged) && (numParts > 0)) {
                turtle.ifExporting_startPlantPart(this.longNameForDXFPartConsideringGenderEtc(dxfIndex), this.shortNameForDXFPartConsideringGenderEtc(dxfIndex));
                turnPortion = 256 / numParts;
                leftOverDegrees = 256 - turnPortion * numParts;
                if (leftOverDegrees > 0) {
                    addition = umath.safedivExcept(leftOverDegrees, numParts, 0);
                } else {
                    addition = 0;
                }
                carryOver = 0;
                for (i = 1; i <= numParts; i++) {
                    addThisTime = trunc(addition + carryOver);
                    carryOver = carryOver + addition - addThisTime;
                    if (carryOver < 0) {
                        carryOver = 0;
                    }
                    turtle.rotateX(turnPortion + addThisTime);
                    turtle.push();
                    //aligns object as stored in the file to way should draw on plant
                    turtle.rotateZ(-64);
                    if (open) {
                        //pulls petal up to plane of stalk (is perpendicular)
                        turtle.rotateY(32);
                    }
                    turtle.rotateX(pullBackAngle);
                    if (tdo != null) {
                        this.draw3DObject(tdo, scale, faceColor, backfaceColor, dxfIndex);
                        if (i == 1) {
                            minZ = tdo.zForSorting;
                        } else if (tdo.zForSorting < minZ) {
                            minZ = tdo.zForSorting;
                        }
                    }
                    turtle.pop();
                }
                if (tdo != null) {
                    tdo.zForSorting = minZ;
                }
                turtle.ifExporting_endPlantPart();
            } else {
                turtle.push();
                if ((this.stage == uplant.kStageUnripeFruit) || (this.stage == uplant.kStageRipeFruit)) {
                    turtle.rotateZ(-64);
                } else {
                    //pulls petal up to plane of stalk (is perpendicular)
                    turtle.rotateZ(-pullBackAngle);
                }
                if (tdo != null) {
                    this.draw3DObject(tdo, scale, faceColor, backfaceColor, dxfIndex);
                }
                turtle.pop();
            }
            turtle.pop();
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdFlowerFruit.drawCircleOfTdos");
        }
    }
    
    public int partType() {
        result = 0;
        result = uplant.kPartTypeFlowerFruit;
        return result;
    }
    
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kPdFlowerFruit;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        super.streamDataWithFiler(filer, cvir);
        this.propFullSize = filer.streamSingle(this.propFullSize);
        this.stage = filer.streamSmallint(this.stage);
        this.hasBeenDrawn = filer.streamBoolean(this.hasBeenDrawn);
        this.daysAccumulatingFruitBiomass = filer.streamLongint(this.daysAccumulatingFruitBiomass);
        this.daysOpen = filer.streamLongint(this.daysOpen);
    }
    
}
// cfk remember this 
// ---------------------------------------------------------------------- wilting/falling down 
//procedure PdFlowerFruit.dragDownFromWeight;
//  begin
//  end; 
//procedure PdFlowerFruit.dragDownFromWeight;
//  var
//    fractionOfOptimalFruitWeight_frn: single;
//    angle: integer;
//  begin
//  if (plant.turtle = nil) then exit;
//  fractionOfOptimalFruitWeight_frn := safedivExcept(liveBiomass_pctMPB, plant.pFruit.optimalBiomass_pctMPB, 0.0);
//  angle := round(abs(plant.turtle.angleZ + 32) * fractionOfOptimalFruitWeight_frn
//      * min(1.0, max(0.0, 100 - plant.pFruit.stalkStrengthIndex) / 100.0));
//  angle := -angle;
//  if plant.turtle.angleZ > -32 then
//    angle := -angle;
//  plant.turtle.rotateZ(angle);
//  end;  
