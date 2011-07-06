// unit uleaf

from conversion_common import *;
import usupport;
import u3dexport;
import uturtle;
import utravers;
import utdo;
import ufiler;
import umath;
import uplant;
import upart;
import delphi_compatability;

// const
kNumCompoundLeafRandomSwayIndexes = 49;



class PdLeaf extends PdPlantPart {
    public SCurveStructure sCurveParams;
    public float propFullSize;
    public float biomassAtCreation_pctMPB;
    public  compoundLeafRandomSwayIndexes;
    
    public PdLeaf NewWithPlantFractionOfOptimalSize(PdPlant aPlant, float aFraction) {
        result = new PdLeaf();
        result = this.create();
        result.initializeFractionOfOptimalSize(aPlant, aFraction);
        return result;
    }
    
    public void initializeFractionOfOptimalSize(PdPlant thePlant, float aFraction) {
        int i = 0;
        
        try {
            this.initialize(thePlant);
            //Plant sets this from outside on first phytomer.
            this.isSeedlingLeaf = false;
            this.liveBiomass_pctMPB = aFraction * PdLeaf.optimalInitialBiomass_pctMPB(this.plant);
            this.deadBiomass_pctMPB = 0.0;
            this.propFullSize = umath.safedivExcept(this.liveBiomass_pctMPB, this.plant.pLeaf.optimalBiomass_pctMPB, 1.0);
            if (this.plant.pLeaf.compoundNumLeaflets > 1) {
                for (i = 0; i <= kNumCompoundLeafRandomSwayIndexes; i++) {
                    this.compoundLeafRandomSwayIndexes[i] = this.plant.randomNumberGenerator.zeroToOne();
                }
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdLeaf.initializeFractionOfOptimalSize");
        }
    }
    
    public float optimalInitialBiomass_pctMPB(PdPlant drawingPlant) {
        result = 0.0;
        result = drawingPlant.pLeaf.optimalFractionOfOptimalBiomassAtCreation_frn * drawingPlant.pLeaf.optimalBiomass_pctMPB;
        return result;
    }
    
    public String getName() {
        result = "";
        result = "leaf";
        return result;
    }
    
    public void nextDay() {
        try {
            super.nextDay();
            this.checkIfHasAbscissed();
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdLeaf.nextDay");
        }
    }
    
    public void traverseActivity(int mode, TObject traverserProxy) {
        PdTraverser traverser = new PdTraverser();
        float propFullSizeWanted = 0.0;
        float newBiomass_pctMPB = 0.0;
        float biomassToRemove_pctMPB = 0.0;
        float fractionOfMaxAge_frn = 0.0;
        KfTurtle turtle = new KfTurtle();
        
        super.traverseActivity(mode, traverserProxy);
        traverser = utravers.PdTraverser(traverserProxy);
        if (traverser == null) {
            return;
        }
        if (this.hasFallenOff && (mode != utravers.kActivityStream) && (mode != utravers.kActivityFree)) {
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
                    if (this.age > this.plant.pLeaf.maxDaysToGrow) {
                        this.biomassDemand_pctMPB = 0.0;
                        return;
                    }
                    fractionOfMaxAge_frn = umath.safedivExcept(this.age + 1, this.plant.pLeaf.maxDaysToGrow, 0.0);
                    propFullSizeWanted = umath.max(0.0, umath.min(1.0, umath.scurve(fractionOfMaxAge_frn, this.plant.pLeaf.sCurveParams.c1, this.plant.pLeaf.sCurveParams.c2)));
                    this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, propFullSizeWanted * this.plant.pLeaf.optimalBiomass_pctMPB, this.plant.pLeaf.minDaysToGrow);
                    traverser.total = traverser.total + this.biomassDemand_pctMPB;
                    break;
                case utravers.kActivityDemandReproductive:
                    break;
                case utravers.kActivityGrowVegetative:
                    if (this.age > this.plant.pLeaf.maxDaysToGrow) {
                        // no repro. demand
                        return;
                    }
                    newBiomass_pctMPB = this.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
                    this.liveBiomass_pctMPB = this.liveBiomass_pctMPB + newBiomass_pctMPB;
                    this.propFullSize = umath.min(1.0, umath.safedivExcept(this.totalBiomass_pctMPB(), this.plant.pLeaf.optimalBiomass_pctMPB, 0));
                    break;
                case utravers.kActivityGrowReproductive:
                    break;
                case utravers.kActivityStartReproduction:
                    break;
                case utravers.kActivityFindPlantPartAtPosition:
                    if (umath.pointsAreCloseEnough(traverser.point, this.position())) {
                        // no repro. growth
                        // no response 
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
                    // phytomer will control drawing 
                    //streaming will be done by internode
                    // free will be called by phytomer 
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
                    if (this.isSeedlingLeaf) {
                        // none 
                        // none 
                        this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeSeedlingLeaf);
                    } else {
                        this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeLeaf);
                    }
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
                    break;
                case utravers.kActivityCountPointsAndTrianglesFor3DExport:
                    this.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser);
                    break;
                default:
                    throw new GeneralException.create("Problem: Unhandled mode in method PdLeaf.traverseActivity.");
                    break;
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdLeaf.traverseActivity");
        }
    }
    
    public void checkIfHasAbscissed() {
        pass
        // if enough biomass removed (parameter), absciss leaf or leaves 
        // not doing anymore
        //if (self.fractionLive < plant.pLeaf.fractionOfLiveBiomassWhenAbscisses_frn) and (not self.hasFallenOff) then
        //  self.hasFallenOff := true;
    }
    
    public void destroy() {
        super.destroy();
    }
    
    public boolean isPhytomer() {
        result = false;
        result = false;
        return result;
    }
    
    public void countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(PdTraverser traverser) {
        if (traverser == null) {
            return;
        }
        if (this.hasFallenOff) {
            return;
        }
        if (this.propFullSize <= 0) {
            return;
        }
        if (this.isSeedlingLeaf) {
            if (this.plant.pSeedlingLeaf.leafTdoParams.scaleAtFullSize > 0) {
                // seedling leaf
                traverser.total3DExportPointsIn3DObjects += this.plant.pSeedlingLeaf.leafTdoParams.object3D.pointsInUse;
                traverser.total3DExportTrianglesIn3DObjects += this.plant.pSeedlingLeaf.leafTdoParams.object3D.triangles.Count;
                this.addExportMaterial(traverser, u3dexport.kExportPartSeedlingLeaf, -1);
            }
            // not seedling leaf
        } else {
            if (this.plant.pLeaf.leafTdoParams.scaleAtFullSize > 0) {
                // leaf (considering compound leaf)
                traverser.total3DExportPointsIn3DObjects += this.plant.pLeaf.leafTdoParams.object3D.pointsInUse * this.plant.pLeaf.compoundNumLeaflets;
                traverser.total3DExportTrianglesIn3DObjects += this.plant.pLeaf.leafTdoParams.object3D.triangles.Count * this.plant.pLeaf.compoundNumLeaflets;
                this.addExportMaterial(traverser, u3dexport.kExportPartLeaf, -1);
            }
            if (this.plant.pLeaf.stipuleTdoParams.scaleAtFullSize > 0) {
                // stipule
                traverser.total3DExportPointsIn3DObjects += this.plant.pLeaf.stipuleTdoParams.object3D.pointsInUse;
                traverser.total3DExportTrianglesIn3DObjects += this.plant.pLeaf.stipuleTdoParams.object3D.triangles.Count;
                this.addExportMaterial(traverser, u3dexport.kExportPartLeafStipule, -1);
            }
        }
        if (this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm > 0) {
            // petiole
            traverser.total3DExportStemSegments += 1;
            if (this.isSeedlingLeaf) {
                this.addExportMaterial(traverser, u3dexport.kExportPartFirstPetiole, -1);
            } else {
                this.addExportMaterial(traverser, u3dexport.kExportPartPetiole, -1);
            }
            if (this.plant.pLeaf.compoundNumLeaflets > 1) {
                // petiolets + compound leaf internodes
                traverser.total3DExportStemSegments += this.plant.pLeaf.compoundNumLeaflets * 2;
            }
        }
    }
    
    public KfObject3D tdoToSortLinesWith() {
        result = new KfObject3D();
        result = null;
        if (this.plant == null) {
            return result;
        }
        if (this.isSeedlingLeaf) {
            result = this.plant.pSeedlingLeaf.leafTdoParams.object3D;
        } else {
            result = this.plant.pLeaf.leafTdoParams.object3D;
        }
        return result;
    }
    
    public void drawWithDirection(float direction) {
        float scale = 0.0;
        float length = 0.0;
        float width = 0.0;
        float angle = 0.0;
        KfTurtle turtle = new KfTurtle();
        
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        this.boundsRect = Rect(0, 0, 0, 0);
        if (this.hasFallenOff) {
            return;
        }
        turtle.push();
        this.determineAmendmentAndAlsoForChildrenIfAny();
        if (this.hiddenByAmendment()) {
            // amendment rotations handled in drawStemSegment for petiole
            turtle.pop();
            return;
        }
        try {
            if (this.plant.needToRecalculateColors) {
                this.calculateColors();
            }
            this.plant.turtle.push();
            if ((direction == uplant.kDirectionRight)) {
                turtle.rotateX(128);
            }
            len = this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * this.propFullSize;
            if ((this.isSeedlingLeaf)) {
                len = len / 2;
            }
            width = this.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * this.propFullSize;
            angle = this.angleWithSway(this.plant.pLeaf.petioleAngle);
            turtle.ifExporting_startNestedGroupOfPlantParts("leaf, petiole and stipule", "LeafPetiole", u3dexport.kNestingTypeLeafAndPetiole);
            if (this.isSeedlingLeaf) {
                this.drawStemSegment(len, width, angle, 0, this.plant.pLeaf.petioleColor, this.plant.pLeaf.petioleTaperIndex, u3dexport.kExportPartPetiole, upart.kUseAmendment);
                scale = (this.propFullSize * (this.plant.pSeedlingLeaf.leafTdoParams.scaleAtFullSize / 100.0)) * 1.0;
                this.DrawLeafOrLeaflet(scale);
            } else {
                if ((this.plant.pLeaf.stipuleTdoParams.scaleAtFullSize > 0)) {
                    this.drawStipule();
                }
                if ((this.plant.pLeaf.compoundNumLeaflets <= 1) || this.plant.turtle.drawOptions.simpleLeavesOnly) {
                    this.drawStemSegment(len, width, angle, 0, this.plant.pLeaf.petioleColor, this.plant.pLeaf.petioleTaperIndex, u3dexport.kExportPartPetiole, upart.kUseAmendment);
                    scale = this.propFullSize * this.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0;
                    this.DrawLeafOrLeaflet(scale);
                } else {
                    this.drawStemSegment(len, width, angle, 0, this.plant.pLeaf.petioleColor, upart.kDontTaper, u3dexport.kExportPartPetiole, upart.kUseAmendment);
                    turtle.ifExporting_startNestedGroupOfPlantParts("compound leaf", "CompoundLeaf", u3dexport.kNestingTypeCompoundLeaf);
                    if ((this.plant.pLeaf.compoundPinnateOrPalmate == uplant.kCompoundLeafPinnate)) {
                        this.drawCompoundLeafPinnate();
                    } else {
                        this.drawCompoundLeafPalmate();
                    }
                    turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeCompoundLeaf);
                }
            }
            turtle.pop();
            turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeLeafAndPetiole);
            turtle.pop();
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdLeaf.drawWithDirection");
        }
    }
    
    public void wiltLeaf() {
        if ((this.plant.turtle == null)) {
            //  var
            //    angle: integer; 
            return;
        }
        // angle := round(abs(plant.turtle.angleX + 32) * plant.pGeneral.wiltingPercent / 100.0);
        //  if plant.turtle.angleX > -32 then
        //    angle := -angle;
        //  plant.turtle.rotateX(angle); 
    }
    
    public void drawStipule() {
        KfTurtle turtle = new KfTurtle();
        float scale = 0.0;
        int i = 0;
        int turnPortion = 0;
        int leftOverDegrees = 0;
        int addThisTime = 0;
        float addition = 0.0;
        float carryOver = 0.0;
        
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        if (this.isSeedlingLeaf) {
            return;
        }
        turtle.push();
        turtle.rotateX(this.angleWithSway(this.plant.pLeaf.stipuleTdoParams.xRotationBeforeDraw));
        turtle.rotateY(this.angleWithSway(this.plant.pLeaf.stipuleTdoParams.yRotationBeforeDraw));
        turtle.rotateZ(this.angleWithSway(this.plant.pLeaf.stipuleTdoParams.zRotationBeforeDraw));
        scale = (this.propFullSize * (this.plant.pLeaf.stipuleTdoParams.scaleAtFullSize / 100.0)) * 1.0;
        if (this.plant.pLeaf.stipuleTdoParams.repetitions > 1) {
            turnPortion = 256 / this.plant.pLeaf.stipuleTdoParams.repetitions;
            leftOverDegrees = 256 - turnPortion * this.plant.pLeaf.stipuleTdoParams.repetitions;
            if (leftOverDegrees > 0) {
                addition = leftOverDegrees / this.plant.pLeaf.stipuleTdoParams.repetitions;
            } else {
                addition = 0;
            }
            carryOver = 0;
            for (i = 1; i <= this.plant.pLeaf.stipuleTdoParams.repetitions; i++) {
                addThisTime = trunc(addition + carryOver);
                carryOver = carryOver + addition - addThisTime;
                if (carryOver < 0) {
                    carryOver = 0;
                }
                turtle.rotateY(turnPortion + addThisTime);
                if (this.plant.pLeaf.stipuleTdoParams.object3D != null) {
                    this.draw3DObject(this.plant.pLeaf.stipuleTdoParams.object3D, scale, this.plant.pLeaf.stipuleTdoParams.faceColor, this.plant.pLeaf.stipuleTdoParams.backfaceColor, u3dexport.kExportPartLeafStipule);
                }
            }
        } else if (this.plant.pLeaf.stipuleTdoParams.object3D != null) {
            this.draw3DObject(this.plant.pLeaf.stipuleTdoParams.object3D, scale, this.plant.pLeaf.stipuleTdoParams.faceColor, this.plant.pLeaf.stipuleTdoParams.backfaceColor, u3dexport.kExportPartLeafStipule);
        }
        turtle.pop();
    }
    
    public void DrawLeafOrLeaflet(float aScale) {
        KfTurtle turtle = new KfTurtle();
        float rotateAngle = 0.0;
        KfObject3D tdo = new KfObject3D();
        TColorRef useFaceColor = new TColorRef();
        TColorRef useBackfaceColor = new TColorRef();
        
        //Draw leaf only. If seedling leaf (on first phytomer), draw seedling leaf 3D object and colors instead.
        //    Wilt leaf according to water stress and age.
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        if (this.isSeedlingLeaf) {
            turtle.setLineWidth(1.0);
            useFaceColor = this.plant.pSeedlingLeaf.leafTdoParams.faceColor;
            useBackfaceColor = this.plant.pSeedlingLeaf.leafTdoParams.backfaceColor;
        } else {
            turtle.setLineWidth(1.0);
            useFaceColor = this.plant.pLeaf.leafTdoParams.faceColor;
            useBackfaceColor = this.plant.pLeaf.leafTdoParams.backfaceColor;
        }
        if (this.isSeedlingLeaf) {
            //this aligns the 3D object as stored in the file to the way it should draw on the plant
            // turtle.RotateX(64)  // flip over; in 3D designer you design the leaf from the underside
            //rotateAngle := self.angleWithSway(plant.pLeaf.object3DXRotationBeforeDraw * 256 / 360);
            //turtle.rotateX(rotateAngle);
            // no longer doing this because default X rotation is 90 degrees
            turtle.rotateX(this.angleWithSway(this.plant.pSeedlingLeaf.leafTdoParams.xRotationBeforeDraw));
            turtle.rotateY(this.angleWithSway(this.plant.pSeedlingLeaf.leafTdoParams.yRotationBeforeDraw));
            turtle.rotateZ(this.angleWithSway(this.plant.pSeedlingLeaf.leafTdoParams.zRotationBeforeDraw));
        } else {
            turtle.rotateX(this.angleWithSway(this.plant.pLeaf.leafTdoParams.xRotationBeforeDraw));
            turtle.rotateY(this.angleWithSway(this.plant.pLeaf.leafTdoParams.yRotationBeforeDraw));
            turtle.rotateZ(this.angleWithSway(this.plant.pLeaf.leafTdoParams.zRotationBeforeDraw));
        }
        //pull leaf up to plane of petiole (is perpendicular)
        turtle.rotateZ(-64);
        this.wiltLeaf();
        if (this.isSeedlingLeaf) {
            tdo = this.plant.pSeedlingLeaf.leafTdoParams.object3D;
        } else {
            tdo = this.plant.pLeaf.leafTdoParams.object3D;
        }
        if (tdo != null) {
            this.draw3DObject(tdo, aScale, useFaceColor, useBackfaceColor, u3dexport.kExportPartLeaf);
        }
    }
    
    public void drawCompoundLeafPinnate() {
        KfTurtle turtle = new KfTurtle();
        float scale = 0.0;
        int i = 0;
        
        //Draw compound leaf. Use recursion structure we used to use for whole plant, with no branching.
        //    Leaflets decrease in size as you move up the leaf, simulating a gradual appearance of leaflets.
        //    Note that seedling leaves are never compound.
        turtle = this.plant.turtle;
        if (turtle == null) {
            return;
        }
        if (this.plant.pLeaf.compoundNumLeaflets <= 0) {
            return;
        }
        for (i = this.plant.pLeaf.compoundNumLeaflets; i >= 1; i--) {
            if ((this.plant.pLeaf.compoundPinnateLeafletArrangement == uplant.kArrangementOpposite)) {
                if ((i != 1) && (i % 2 == 1)) {
                    // v2 added opposite leaflets
                    this.drawCompoundLeafInternode(i);
                }
            } else if ((i != 1)) {
                this.drawCompoundLeafInternode(i);
            }
            turtle.push();
            scale = this.propFullSize * this.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0;
            this.DrawCompoundLeafPetioletCount(scale, i);
            this.DrawLeafOrLeaflet(scale);
            turtle.pop();
        }
    }
    
    public void drawCompoundLeafInternode(int count) {
        float length = 0.0;
        float width = 0.0;
        float angleZ = 0.0;
        float angleY = 0.0;
        
        //Draw internode of leaflet (portion of rachis). This is almost identical to drawing the petiole, etc,
        //   but a bit of random drift is included to make the compound leaf look more single.
        len = this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * this.propFullSize * this.plant.pLeaf.compoundRachisToPetioleRatio / 100.0;
        width = this.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * this.propFullSize;
        // v1.6b3
        angleZ = this.compoundLeafAngleWithSway(this.bendAngleForCompoundLeaf(count), count);
        angleY = this.compoundLeafAngleWithSway(0, count);
        this.drawStemSegment(len, width, angleZ, angleY, this.plant.pLeaf.petioleColor, upart.kDontTaper, u3dexport.kExportPartPetiole, upart.kDontUseAmendment);
    }
    
    // v1.6b3
    public float bendAngleForCompoundLeaf(int count) {
        result = 0.0;
        float leafletNumberEffect = 0.0;
        float propFullSizeThisLeaflet = 0.0;
        float difference = 0.0;
        
        result = 0;
        if (this.plant == null) {
            return result;
        }
        difference = abs(this.plant.pLeaf.compoundCurveAngleAtFullSize - this.plant.pLeaf.compoundCurveAngleAtStart);
        leafletNumberEffect = 0.75 + 0.25 * umath.safedivExcept(count, this.plant.pLeaf.compoundNumLeaflets - 1, 0);
        propFullSizeThisLeaflet = umath.max(0.0, umath.min(1.0, (0.25 + 0.75 * this.propFullSize) * leafletNumberEffect));
        if (this.plant.pLeaf.compoundCurveAngleAtFullSize > this.plant.pLeaf.compoundCurveAngleAtStart) {
            result = this.plant.pLeaf.compoundCurveAngleAtStart + difference * propFullSizeThisLeaflet;
        } else {
            result = this.plant.pLeaf.compoundCurveAngleAtStart - difference * propFullSizeThisLeaflet;
        }
        return result;
    }
    
    public void DrawCompoundLeafPetioletCount(float scale, int aCount) {
        float length = 0.0;
        float width = 0.0;
        float angle = 0.0;
        
        //Draw petiolet, which is the leaflet stem coming off the compound leaf rachis.
        len = scale * this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * this.propFullSize;
        width = scale * this.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * this.propFullSize;
        if ((aCount == 1)) {
            angle = 0;
        } else {
            if ((odd(aCount))) {
                angle = 32;
            } else {
                angle = -32;
            }
        }
        angle = this.compoundLeafAngleWithSway(angle, aCount);
        this.drawStemSegment(len, width, 0, angle, this.plant.pLeaf.petioleColor, this.plant.pLeaf.petioleTaperIndex, u3dexport.kExportPartPetiole, upart.kDontUseAmendment);
    }
    
    public float compoundLeafAngleWithSway(float angle, int count) {
        result = 0.0;
        float randomNumber = 0.0;
        
        result = angle;
        if (this.plant == null) {
            return result;
        }
        if (count < 0) {
            count = 0;
        }
        count = count % kNumCompoundLeafRandomSwayIndexes;
        randomNumber = this.compoundLeafRandomSwayIndexes[count];
        result = angle + ((randomNumber - 0.5) * this.plant.pGeneral.randomSway);
        return result;
    }
    
    public void drawCompoundLeafPalmate() {
        KfTurtle turtle = new KfTurtle();
        float scale = 0.0;
        float angle = 0.0;
        float angleOne = 0.0;
        float length = 0.0;
        float width = 0.0;
        
        int i = 0;
        
        //Draw palmate compound leaf. Use recursion structure we used to use for whole plant, with no branching.
        //    In a palmate leaf, leaflets increase in size as you move toward the middle of the leaf.
        //    Note that seedling leaves are never compound.
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        angleOne = umath.safedivExcept(64, this.plant.pLeaf.compoundNumLeaflets, 0);
        if (this.plant.pLeaf.compoundNumLeaflets > 0) {
            for (i = this.plant.pLeaf.compoundNumLeaflets; i >= 1; i--) {
                turtle.push();
                if ((i == 1)) {
                    angle = 0;
                } else if ((odd(i))) {
                    angle = angleOne * i * -1;
                } else {
                    angle = angleOne * i * 1;
                }
                len = this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * this.propFullSize * this.plant.pLeaf.compoundRachisToPetioleRatio / 100.0;
                width = this.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * this.propFullSize;
                this.drawStemSegment(len, width, 0, angle, this.plant.pLeaf.petioleColor, this.plant.pLeaf.petioleTaperIndex, u3dexport.kExportPartPetiole, upart.kDontUseAmendment);
                scale = this.propFullSize * this.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0;
                //scale := safedivExcept(scale, plant.pLeaf.compoundNumLeaflets, 0); 
                this.DrawLeafOrLeaflet(scale);
                turtle.pop();
            }
        }
    }
    
    public void report() {
        super.report();
        //debugPrint('leaf, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
        //DebugForm.printNested(plant.turtle.stackSize, 'leaf, age ' + IntToStr(age));
    }
    
    public int partType() {
        result = 0;
        result = uplant.kPartTypeLeaf;
        return result;
    }
    
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kPdLeaf;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        super.streamDataWithFiler(filer, cvir);
        this.sCurveParams = filer.streamBytes(this.sCurveParams, FIX_sizeof(this.sCurveParams));
        this.propFullSize = filer.streamSingle(this.propFullSize);
        this.biomassAtCreation_pctMPB = filer.streamSingle(this.biomassAtCreation_pctMPB);
        this.isSeedlingLeaf = filer.streamBoolean(this.isSeedlingLeaf);
    }
    
}
