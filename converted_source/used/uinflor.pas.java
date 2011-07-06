// unit uinflor

from conversion_common import *;
import usupport;
import uamendmt;
import umath;
import udomain;
import u3dexport;
import uturtle;
import utravers;
import ufiler;
import ucollect;
import ufruit;
import uplant;
import uintern;
import upart;
import delphi_compatability;


class PdInflorescence extends PdPlantPart {
    public TListCollection flowers;
    public short numFlowers;
    public short numFlowersEachDay;
    public short daysBetweenFlowerAppearances;
    public short daysSinceLastFlowerAppeared;
    public short daysSinceStartedMakingFlowers;
    public boolean isApical;
    public PdPlantPart meristemThatCreatedMe;
    public PdInternode phytomerAttachedTo;
    public float fractionOfOptimalSizeWhenCreated;
    
    public void create() {
        super.create();
        this.flowers = ucollect.TListCollection().Create();
        this.meristemThatCreatedMe = null;
    }
    
    public void destroy() {
        this.flowers.free;
        this.flowers = null;
        this.meristemThatCreatedMe.free;
        this.meristemThatCreatedMe = null;
        super.destroy();
    }
    
    public String getName() {
        result = "";
        result = "inflorescence";
        return result;
    }
    
    public void determineAmendmentAndAlsoForChildrenIfAny() {
        int i = 0;
        PdPlantDrawingAmendment amendmentToPass = new PdPlantDrawingAmendment();
        
        super.determineAmendmentAndAlsoForChildrenIfAny();
        if (this.amendment != null) {
            amendmentToPass = this.amendment;
        } else {
            amendmentToPass = this.parentAmendment;
        }
        if (this.flowers.Count > 0) {
            for (i = 0; i <= this.flowers.Count - 1; i++) {
                ufruit.PdFlowerFruit(this.flowers.Items[i]).parentAmendment = amendmentToPass;
            }
        }
    }
    
    public void initializeGenderApicalOrAxillary(PdPlant aPlant, int aGender, boolean initAsApical, float fractionOfOptimalSize) {
        float daysToAllFlowers = 0.0;
        
        try {
            this.initialize(aPlant);
            this.gender = aGender;
            this.isApical = initAsApical;
            this.daysSinceLastFlowerAppeared = 0;
            this.daysSinceStartedMakingFlowers = 0;
            this.fractionOfOptimalSizeWhenCreated = umath.min(1.0, fractionOfOptimalSize);
            //The inflorescence must know whether it produces flowers slowly (over a greater number of days than flowers)
            //  or produces many flowers in a few days.
            daysToAllFlowers = this.plant.pInflor[this.gender].daysToAllFlowersCreated;
            this.numFlowers = this.plant.pInflor[self.gender].numFlowersOnMainBranch + this.plant.pInflor[self.gender].numFlowersPerBranch * this.plant.pInflor[self.gender].numBranches;
            this.daysBetweenFlowerAppearances = 0;
            this.numFlowersEachDay = 0;
            if (this.numFlowers > 0) {
                if (this.numFlowers == 1) {
                    this.numFlowersEachDay = 1;
                } else if (this.numFlowers == daysToAllFlowers) {
                    this.numFlowersEachDay = 1;
                } else if (this.numFlowers > daysToAllFlowers) {
                    this.numFlowersEachDay = intround(umath.safedivExcept(1.0 * this.numFlowers, 1.0 * daysToAllFlowers, 0));
                } else {
                    this.daysBetweenFlowerAppearances = intround(umath.safedivExcept(1.0 * daysToAllFlowers, 1.0 * this.numFlowers, 0));
                }
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInflorescence.InitializeGenderApicalOrAxillary");
        }
    }
    
    public float optimalInitialBiomass_pctMPB(PdPlant drawingPlant, int gender) {
        result = 0.0;
        if ((gender < 0) || (gender > 1)) {
            result = 0.0;
        } else {
            result = drawingPlant.pInflor[gender].optimalBiomass_pctMPB * drawingPlant.pInflor[gender].minFractionOfOptimalBiomassToCreateInflorescence_frn;
        }
        return result;
    }
    
    public void nextDay() {
        int i = 0;
        int numFlowersToCreateToday = 0;
        float biomassToMakeFlowers_pctMPB = 0.0;
        
        try {
            super.nextDay();
            if (this.flowers.Count > 0) {
                for (i = 0; i <= this.flowers.Count - 1; i++) {
                    ufruit.PdFlowerFruit(this.flowers.Items[i]).nextDay();
                }
            }
            //if self.age < plant.pInflor[gender].maxDaysToGrow then
            biomassToMakeFlowers_pctMPB = this.plant.pInflor[this.gender].minFractionOfOptimalBiomassToMakeFlowers_frn * this.plant.pInflor[this.gender].optimalBiomass_pctMPB;
            if (this.liveBiomass_pctMPB >= biomassToMakeFlowers_pctMPB) {
                this.daysSinceStartedMakingFlowers += 1;
                if ((this.flowers.Count <= 0) && (this.numFlowers > 0)) {
                    // make first flower on first day
                    this.createFlower();
                } else if ((this.flowers.Count < this.numFlowers)) {
                    if ((this.daysBetweenFlowerAppearances > 0)) {
                        if ((this.daysSinceLastFlowerAppeared >= this.daysBetweenFlowerAppearances)) {
                            this.createFlower();
                            this.daysSinceLastFlowerAppeared = 0;
                        } else {
                            this.daysSinceLastFlowerAppeared += 1;
                        }
                    } else {
                        numFlowersToCreateToday = umath.intMin(this.numFlowersEachDay, this.numFlowers - this.flowers.Count);
                        if (numFlowersToCreateToday > 0) {
                            for (i = 0; i <= numFlowersToCreateToday - 1; i++) {
                                this.createFlower();
                            }
                        }
                        this.daysSinceLastFlowerAppeared = 0;
                    }
                }
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInflorescence.nextDay");
        }
    }
    
    public void traverseActivity(int mode, TObject traverserProxy) {
        PdTraverser traverser = new PdTraverser();
        float newBiomass_pctMPB = 0.0;
        float biomassToRemove_pctMPB = 0.0;
        int i = 0;
        int numLines = 0;
        
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
                if (this.flowers.Count > 0) {
                    for (i = 0; i <= this.flowers.Count - 1; i++) {
                        (ufruit.PdFlowerFruit(this.flowers.Items[i])).traverseActivity(mode, traverser);
                    }
                }
            }
            switch (mode) {
                case utravers.kActivityNone:
                    break;
                case utravers.kActivityNextDay:
                    this.nextDay();
                    break;
                case utravers.kActivityDemandVegetative:
                    break;
                case utravers.kActivityDemandReproductive:
                    if ((this.age > this.plant.pInflor[this.gender].maxDaysToGrow)) {
                        // no vegetative demand 
                        this.biomassDemand_pctMPB = 0.0;
                        return;
                    }
                    try {
                        this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, this.plant.pInflor[this.gender].optimalBiomass_pctMPB, this.plant.pInflor[this.gender].minDaysToGrow);
                        traverser.total = traverser.total + this.biomassDemand_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdInflorescence.traverseActivity (reproductive demand)");
                    }
                    break;
                case utravers.kActivityGrowVegetative:
                    break;
                case utravers.kActivityGrowReproductive:
                    if (this.age > this.plant.pInflor[this.gender].maxDaysToGrow) {
                        // no vegetative growth 
                        return;
                    }
                    newBiomass_pctMPB = this.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
                    this.liveBiomass_pctMPB = this.liveBiomass_pctMPB + newBiomass_pctMPB;
                    break;
                case utravers.kActivityStartReproduction:
                    break;
                case utravers.kActivityFindPlantPartAtPosition:
                    if (umath.pointsAreCloseEnough(traverser.point, this.position())) {
                        // cannot switch 
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
                    break;
                case utravers.kActivityFree:
                    break;
                case utravers.kActivityVegetativeBiomassThatCanBeRemoved:
                    break;
                case utravers.kActivityRemoveVegetativeBiomass:
                    break;
                case utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                    //streaming called by phytomer
                    // free called by phytomer 
                    // none 
                    // none 
                    traverser.total = traverser.total + this.liveBiomass_pctMPB;
                    break;
                case utravers.kActivityRemoveReproductiveBiomass:
                    biomassToRemove_pctMPB = this.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
                    this.liveBiomass_pctMPB = this.liveBiomass_pctMPB - biomassToRemove_pctMPB;
                    this.deadBiomass_pctMPB = this.deadBiomass_pctMPB + biomassToRemove_pctMPB;
                    break;
                case utravers.kActivityGatherStatistics:
                    if (this.gender == uplant.kGenderMale) {
                        this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeMaleInflorescence);
                    } else {
                        this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFemaleInflorescence);
                    }
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
                    this.biomassOfMeAndAllPartsAboveMe_pctMPB = this.biomassOfMeAndAllPartsConnectedToMe_pctMPB();
                    break;
                case utravers.kActivityCountPointsAndTrianglesFor3DExport:
                    this.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser);
                    break;
                default:
                    throw new GeneralException.create("Problem: Unhandled mode in method PdInflorescence.traverseActivity.");
                    break;
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInflorescence.traverseActivity");
        }
    }
    
    public void countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(PdTraverser traverser) {
        int numLines = 0;
        
        if (traverser == null) {
            return;
        }
        if (this.plant.pInflor[self.gender].bractTdoParams.scaleAtFullSize > 0) {
            // bracts
            traverser.total3DExportPointsIn3DObjects += this.plant.pInflor[self.gender].bractTdoParams.object3D.pointsInUse * this.plant.pInflor[self.gender].bractTdoParams.repetitions;
            traverser.total3DExportTrianglesIn3DObjects += this.plant.pInflor[self.gender].bractTdoParams.object3D.triangles.Count * this.plant.pInflor[self.gender].bractTdoParams.repetitions;
            this.addExportMaterial(traverser, u3dexport.kExportPartInflorescenceBractFemale, u3dexport.kExportPartInflorescenceBractMale);
        }
        // pedicels and inflorescence internodes
        numLines = this.plant.pInflor[this.gender].numBranches;
        if (!this.plant.pInflor[this.gender].branchesAreAlternate) {
            numLines = numLines * 2;
        }
        if (this.plant.pInflor[this.gender].internodeLength_mm > 0) {
            this.addExportMaterial(traverser, u3dexport.kExportPartInflorescenceInternodeFemale, u3dexport.kExportPartInflorescenceInternodeMale);
        }
        // peduncle
        numLines += 1;
        traverser.total3DExportStemSegments += numLines;
        if (this.plant.pInflor[this.gender].peduncleLength_mm > 0) {
            this.addExportMaterial(traverser, u3dexport.kExportPartInflorescenceStalkFemale, u3dexport.kExportPartInflorescenceStalkMale);
        }
    }
    
    public void report() {
        super.report();
        UNRESOLVED.debugPrint(IntToStr(this.numFlowers) + " flowers");
        // note flowers will print first 
        // debugPrint('inflorescence, age '  + IntToStr(age));
        //DebugForm.printNested(plant.turtle.stackSize, 'inflorescence, age '  + IntToStr(age));
    }
    
    public float biomassOfMeAndAllPartsConnectedToMe_pctMPB() {
        result = 0.0;
        int i = 0;
        
        result = this.totalBiomass_pctMPB();
        if (this.flowers.Count > 0) {
            for (i = 0; i <= this.flowers.Count - 1; i++) {
                result = result + (ufruit.PdFlowerFruit(this.flowers.Items[i])).totalBiomass_pctMPB();
            }
        }
        return result;
    }
    
    public boolean allFlowersHaveBeenDrawn() {
        result = false;
        int i = 0;
        
        result = true;
        if (this.flowers.Count > 0) {
            for (i = 0; i <= this.flowers.Count - 1; i++) {
                if (!((ufruit.PdFlowerFruit(this.flowers.Items[i])).hasBeenDrawn)) {
                    result = false;
                    return result;
                }
            }
        }
        return result;
    }
    
    public void addDependentPartsToList(TList aList) {
        long i = 0;
        
        if (this.flowers.Count > 0) {
            for (i = 0; i <= this.flowers.Count - 1; i++) {
                aList.Add(this.flowers.Items[i]);
            }
        }
    }
    
    public void createFlower() {
        PdFlowerFruit aFlowerFruit = new PdFlowerFruit();
        
        if (this.plant.partsCreated > udomain.domain.options.maxPartsPerPlant_thousands * 1000) {
            // create new flower/fruit object 
            // v1.6b1
            return;
        }
        aFlowerFruit = ufruit.PdFlowerFruit().create();
        aFlowerFruit.initializeGender(this.plant, this.gender);
        this.flowers.Add(aFlowerFruit);
    }
    
    public void deleteFlower(PdFlowerFruit theFlower) {
        // remove flower object from list 
        this.flowers.Remove(theFlower);
    }
    
    public void draw() {
        int i = 0;
        KfTurtle turtle = new KfTurtle();
        
        if (!this.shouldDraw()) {
            return;
        }
        turtle = this.plant.turtle;
        this.boundsRect = Rect(0, 0, 0, 0);
        turtle.push();
        if (this.hiddenByAmendment()) {
            // amendment rotation handled in drawStemSegment for peduncle
            turtle.pop();
            return;
        }
        try {
            if (this.flowers.Count > 0) {
                for (i = 0; i <= this.flowers.Count - 1; i++) {
                    ufruit.PdFlowerFruit(this.flowers.Items[i]).hasBeenDrawn = false;
                }
            }
            this.calculateColors();
            turtle.ifExporting_startNestedGroupOfPlantParts(this.genderString() + " inflorescence", this.genderString() + "Inflor", u3dexport.kNestingTypeInflorescence);
            if ((this.flowers.Count > 0)) {
                this.drawBracts();
                this.drawPeduncle();
                if ((this.plant.pInflor[this.gender].isHead)) {
                    this.drawHead();
                } else {
                    this.drawApex(this.plant.pInflor[this.gender].numFlowersOnMainBranch, 0, true);
                }
            }
            turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeInflorescence);
            turtle.pop();
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInflorescence.draw");
        }
    }
    
    public boolean shouldDraw() {
        result = false;
        long i = 0;
        PdFlowerFruit flowerFruit = new PdFlowerFruit();
        
        // if inflorescence has at least one flower or non-fallen fruit, should draw 
        result = true;
        if (this.flowers.Count > 0) {
            for (i = 0; i <= this.flowers.Count - 1; i++) {
                flowerFruit = ufruit.PdFlowerFruit(this.flowers.Items[i]);
                if (flowerFruit == null) {
                    continue;
                }
                if (!flowerFruit.hasFallenOff) {
                    return result;
                }
            }
        }
        result = false;
        return result;
    }
    
    public void drawApex(int internodeCount, int flowerIndexOffset, boolean mainBranch) {
        KfTurtle turtle = new KfTurtle();
        
        short i = 0;
        short branchesDrawn = 0;
        
        i = 0;
        //Draw inflorescence in raceme, panicle, or umbel form. This method uses the recursive algorithm
        //     we first developed to draw the entire plant.
        turtle = this.plant.turtle;
        if (turtle == null) {
            return;
        }
        branchesDrawn = 0;
        if (internodeCount > 0) {
            if (mainBranch) {
                // draw the flowers on the main stem first, because if any are not going to be drawn for
                // want of available flowers, the branches should lose them.
                turtle.push();
            }
            if (mainBranch) {
                while (branchesDrawn < this.plant.pInflor[this.gender].numBranches) {
                    this.drawInternode(i);
                    branchesDrawn += 1;
                }
            }
            // draw flowers on main stem first
            i = internodeCount;
            while (i >= 1) {
                if (this.plant.pInflor[this.gender].flowersSpiralOnStem) {
                    //param
                    turtle.rotateX(98);
                }
                this.drawInternode(i);
                turtle.push();
                this.drawFlower(flowerIndexOffset + i);
                turtle.pop();
                i -= 1;
            }
            if (mainBranch) {
                turtle.pop();
            }
        }
        branchesDrawn = 0;
        if (mainBranch) {
            while (branchesDrawn < this.plant.pInflor[this.gender].numBranches) {
                if (this.plant.pInflor[this.gender].flowersSpiralOnStem) {
                    // draw branches
                    //param
                    turtle.rotateX(98);
                }
                this.drawInternode(i);
                this.drawAxillaryBud(this.plant.pInflor[this.gender].numFlowersPerBranch, this.plant.pInflor[this.gender].numFlowersOnMainBranch + branchesDrawn * this.plant.pInflor[this.gender].numFlowersPerBranch);
                branchesDrawn += 1;
                if ((!this.plant.pInflor[this.gender].branchesAreAlternate) && (branchesDrawn < this.plant.pInflor[this.gender].numBranches)) {
                    turtle.push();
                    turtle.rotateX(128);
                    this.drawAxillaryBud(this.plant.pInflor[this.gender].numFlowersPerBranch, this.plant.pInflor[this.gender].numFlowersOnMainBranch + branchesDrawn * this.plant.pInflor[this.gender].numFlowersPerBranch);
                    branchesDrawn += 1;
                    turtle.pop();
                }
            }
        }
    }
    
    public void drawBracts() {
        float scale = 0.0;
        float length = 0.0;
        float width = 0.0;
        float angle = 0.0;
        float propFullSize = 0.0;
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
        if (this.plant.pInflor[this.gender].bractTdoParams.scaleAtFullSize <= 0) {
            return;
        }
        turtle = this.plant.turtle;
        turtle.push();
        turtle.ifExporting_startNestedGroupOfPlantParts(this.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartInflorescenceBractFemale), this.shortNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartInflorescenceBractFemale), u3dexport.kNestingTypeInflorescence);
        propFullSize = umath.safedivExcept(this.liveBiomass_pctMPB, this.plant.pInflor[this.gender].optimalBiomass_pctMPB, 0);
        scale = ((this.plant.pInflor[self.gender].bractTdoParams.scaleAtFullSize / 100.0) * propFullSize);
        turtle.rotateX(this.angleWithSway(this.plant.pInflor[self.gender].bractTdoParams.xRotationBeforeDraw));
        turtle.rotateY(this.angleWithSway(this.plant.pInflor[self.gender].bractTdoParams.yRotationBeforeDraw));
        turtle.rotateZ(this.angleWithSway(this.plant.pInflor[self.gender].bractTdoParams.zRotationBeforeDraw));
        if ((this.plant.pInflor[self.gender].bractTdoParams.radiallyArranged) && (this.plant.pInflor[self.gender].bractTdoParams.repetitions > 0)) {
            turnPortion = 256 / this.plant.pInflor[self.gender].bractTdoParams.repetitions;
            leftOverDegrees = 256 - turnPortion * this.plant.pInflor[self.gender].bractTdoParams.repetitions;
            if (leftOverDegrees > 0) {
                addition = umath.safedivExcept(leftOverDegrees, this.plant.pInflor[self.gender].bractTdoParams.repetitions, 0);
            } else {
                addition = 0;
            }
            carryOver = 0;
            for (i = 0; i <= this.plant.pInflor[self.gender].bractTdoParams.repetitions - 1; i++) {
                turtle.push();
                //aligns object as stored in the file to way should draw on plant
                turtle.rotateY(-64);
                // why? i don't know.
                turtle.rotateX(64);
                turtle.rotateX(this.plant.pInflor[self.gender].bractTdoParams.pullBackAngle);
                this.draw3DObject(this.plant.pInflor[self.gender].bractTdoParams.object3D, scale, this.plant.pInflor[self.gender].bractTdoParams.faceColor, this.plant.pInflor[self.gender].bractTdoParams.backfaceColor, u3dexport.kExportPartInflorescenceBractFemale);
                turtle.pop();
                addThisTime = trunc(addition + carryOver);
                carryOver = carryOver + addition - addThisTime;
                if (carryOver < 0) {
                    carryOver = 0;
                }
                turtle.rotateX(turnPortion + addThisTime);
            }
        } else {
            turtle.push();
            //aligns object as stored in the file to way should draw on plant
            turtle.rotateY(-64);
            // why? i don't know.
            turtle.rotateX(64);
            turtle.rotateX(this.plant.pInflor[self.gender].bractTdoParams.pullBackAngle);
            this.draw3DObject(this.plant.pInflor[self.gender].bractTdoParams.object3D, scale, this.plant.pInflor[self.gender].bractTdoParams.faceColor, this.plant.pInflor[self.gender].bractTdoParams.backfaceColor, u3dexport.kExportPartInflorescenceBractFemale);
            turtle.pop();
        }
        turtle.pop();
        turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeInflorescence);
    }
    
    public void drawPeduncle() {
        float length = 0.0;
        float width = 0.0;
        float zAngle = 0.0;
        float propFullSize = 0.0;
        
        try {
            //Draw peduncle, which is the primary inflorescence stalk. If the inflorescence has only one flower,
            //     this is the only part drawn. If the inflorescence is apical, the stalk may be longer (e.g. in bolting
            //     plants) and is specified by a different parameter.
            zAngle = 0;
            if ((this.phytomerAttachedTo != null)) {
                if ((this.phytomerAttachedTo.leftBranchPlantPart == this)) {
                    zAngle = this.plant.pInflor[self.gender].peduncleAngleFromVegetativeStem;
                } else if ((this.phytomerAttachedTo.rightBranchPlantPart == this)) {
                    zAngle = this.plant.pInflor[self.gender].peduncleAngleFromVegetativeStem;
                    this.plant.turtle.rotateX(128);
                } else if (this.isApical) {
                    zAngle = this.plant.pInflor[self.gender].apicalStalkAngleFromVegetativeStem;
                }
            }
            propFullSize = umath.safedivExcept(this.liveBiomass_pctMPB, this.plant.pInflor[this.gender].optimalBiomass_pctMPB, 0);
            if (this.isApical) {
                len = this.lengthOrWidthAtAgeForFraction(this.plant.pInflor[self.gender].terminalStalkLength_mm, propFullSize);
            } else {
                len = this.lengthOrWidthAtAgeForFraction(this.plant.pInflor[self.gender].peduncleLength_mm, propFullSize);
            }
            width = this.lengthOrWidthAtAgeForFraction(this.plant.pInflor[self.gender].internodeWidth_mm, propFullSize);
            //Use no angle here because phytomer makes the rotation before the inflorescence is drawn.
            this.drawStemSegment(len, width, zAngle, 0, this.plant.pInflor[self.gender].stalkColor, upart.kDontTaper, u3dexport.kExportPartInflorescenceStalkFemale, upart.kUseAmendment);
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInflorescence.drawPeduncle");
        }
    }
    
    public void drawAxillaryBud(int internodeCount, int flowerIndexOffset) {
        KfTurtle turtle = new KfTurtle();
        float angle = 0.0;
        
        //This message is sent when the inflorescence is branched. The decision to create a branch is
        //     made before the message is sent. Note the check if all flowers have been drawn; this prevents
        //     scrawly lines with no flowers.
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        if ((this.allFlowersHaveBeenDrawn())) {
            return;
        }
        angle = this.angleWithSway(this.plant.pInflor[this.gender].branchAngle);
        turtle.push();
        turtle.rotateZ(angle);
        this.drawApex(internodeCount, flowerIndexOffset, false);
        turtle.pop();
    }
    
    public void drawFlower(int internodeCount) {
        float length = 0.0;
        float width = 0.0;
        float angle = 0.0;
        float propFullSize = 0.0;
        int flowerIndex = 0;
        
        try {
            if ((this.allFlowersHaveBeenDrawn())) {
                //Draw one flower, remembering that internodeCount goes from flowers size down to 1,
                //  but flowers are in the order formed.
                //  If the oldest flowers on the inflorescence are at the bottom (acropetal),
                //  draw the flowers in reverse order from internodeCount (which is in the order they were formed).
                //  If the oldest flowers on the inflorescence are at the top (basipetal),
                //  draw the flowers in the order presented by internodeCount
                //     which is in reverse order to how they were formed).
                //  In most plants the older flowers are lower.
                return;
            }
            propFullSize = umath.safedivExcept(this.liveBiomass_pctMPB, this.plant.pInflor[this.gender].optimalBiomass_pctMPB, 0);
            len = this.lengthOrWidthAtAgeForFraction(this.plant.pInflor[self.gender].pedicelLength_mm, propFullSize);
            width = this.lengthOrWidthAtAgeForFraction(this.plant.pInflor[self.gender].internodeWidth_mm, propFullSize);
            angle = this.angleWithSway(this.plant.pInflor[self.gender].pedicelAngle);
            if ((this.plant.pInflor[this.gender].flowersDrawTopToBottom)) {
                flowerIndex = internodeCount;
            } else {
                flowerIndex = this.flowers.Count - internodeCount + 1;
            }
            this.plant.turtle.ifExporting_startNestedGroupOfPlantParts(this.genderString() + " pedicel and flower/fruit", this.genderString() + "PedicelFlower", u3dexport.kNestingTypePedicelAndFlowerFruit);
            this.drawStemSegment(len, width, angle, 0, this.plant.pInflor[self.gender].pedicelColor, this.plant.pInflor[self.gender].pedicelTaperIndex, u3dexport.kExportPartPedicelFemale, upart.kDontUseAmendment);
            if ((flowerIndex - 1 >= 0) && (flowerIndex - 1 <= this.flowers.Count - 1)) {
                ufruit.PdFlowerFruit(this.flowers.Items[flowerIndex - 1]).draw();
            }
            this.plant.turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypePedicelAndFlowerFruit);
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInflorescence.drawFlower");
        }
    }
    
    public void drawHead() {
        KfTurtle turtle = new KfTurtle();
        int i = 0;
        int turnPortion = 0;
        int leftOverDegrees = 0;
        int addThisTime = 0;
        float addition = 0.0;
        float carryOver = 0.0;
        
        // v1.4
        // v1.4
        //Draw the inflorescences in a radial pattern; this is for a head such as a sunflower.
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        turtle.rotateY(64);
        turtle.rotateZ(64);
        // give a little angle down to make it look more natural 
        turtle.rotateY(32);
        if (this.flowers.Count > 0) {
            // new v1.4
            turnPortion = 256 / this.flowers.Count;
            leftOverDegrees = 256 - turnPortion * this.flowers.Count;
            if (leftOverDegrees > 0) {
                addition = umath.safedivExcept(leftOverDegrees, this.flowers.Count, 0);
            } else {
                addition = 0;
            }
            carryOver = 0;
            for (i = this.flowers.Count - 1; i >= 0; i--) {
                addThisTime = trunc(addition + carryOver);
                carryOver = carryOver + addition - addThisTime;
                if (carryOver < 0) {
                    carryOver = 0;
                }
                // was 256 / flowers.count
                turtle.rotateZ(turnPortion + addThisTime);
                turtle.push();
                // v1.4 added one, was bug, was not drawing first flower
                this.drawFlower(i + 1);
                turtle.pop();
            }
        }
    }
    
    public void drawInternode(int internodeCount) {
        float length = 0.0;
        float width = 0.0;
        float zAngle = 0.0;
        float yAngle = 0.0;
        float propFullSize = 0.0;
        
        try {
            if ((this.allFlowersHaveBeenDrawn())) {
                //Draw the inflorescence internode, which is the portion of inflorescence stem between where successive
                //  flower pedicels come off. Note that this is not drawn if all flowers have been drawn; this prevents
                //  straggly lines in branched inflorescences.
                return;
            }
            if ((this.plant.pInflor[self.gender].internodeLength_mm == 0.0)) {
                return;
            }
            propFullSize = umath.safedivExcept(this.liveBiomass_pctMPB, this.plant.pInflor[this.gender].optimalBiomass_pctMPB, 0);
            len = this.lengthOrWidthAtAgeForFraction(this.plant.pInflor[self.gender].internodeLength_mm, propFullSize);
            width = this.lengthOrWidthAtAgeForFraction(this.plant.pInflor[self.gender].internodeWidth_mm, propFullSize);
            zAngle = this.angleWithSway(this.plant.pInflor[self.gender].angleBetweenInternodes);
            yAngle = this.angleWithSway(0);
            this.drawStemSegment(len, width, zAngle, yAngle, this.plant.pInflor[self.gender].stalkColor, upart.kDontTaper, u3dexport.kExportPartInflorescenceInternodeFemale, upart.kDontUseAmendment);
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInflorescence.drawInternode");
        }
    }
    
    public float lengthOrWidthAtAgeForFraction(float starting, float fraction) {
        result = 0.0;
        float ageBounded = 0.0;
        
        result = 0.0;
        try {
            ageBounded = umath.min(this.plant.pInflor[self.gender].daysToAllFlowersCreated, this.daysSinceStartedMakingFlowers);
            if (this.plant.pInflor[self.gender].daysToAllFlowersCreated != 0) {
                result = umath.safedivExcept(starting * ageBounded, this.plant.pInflor[self.gender].daysToAllFlowersCreated, 0) * fraction;
            } else {
                result = starting * ageBounded * fraction;
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdInflorescence.lengthOrWidthAtAgeForFraction");
        }
        return result;
    }
    
    public PdFlowerFruit flower(int index) {
        result = new PdFlowerFruit();
        result = this.flowers.Items[index];
        return result;
    }
    
    public int partType() {
        result = 0;
        result = uplant.kPartTypeInflorescence;
        return result;
    }
    
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kPdInflorescence;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        long i = 0;
        
        super.streamDataWithFiler(filer, cvir);
        this.daysSinceStartedMakingFlowers = filer.streamSmallint(this.daysSinceStartedMakingFlowers);
        this.numFlowersEachDay = filer.streamSmallint(this.numFlowersEachDay);
        this.numFlowers = filer.streamSmallint(this.numFlowers);
        this.daysBetweenFlowerAppearances = filer.streamSmallint(this.daysBetweenFlowerAppearances);
        this.daysSinceLastFlowerAppeared = filer.streamSmallint(this.daysSinceLastFlowerAppeared);
        this.isApical = filer.streamBoolean(this.isApical);
        this.fractionOfOptimalSizeWhenCreated = filer.streamSingle(this.fractionOfOptimalSizeWhenCreated);
        if (filer.isReading()) {
            this.meristemThatCreatedMe = null;
        }
        this.flowers.streamUsingFiler(filer, ufruit.PdFlowerFruit);
        if (filer.isReading() && (this.flowers.Count > 0)) {
            for (i = 0; i <= this.flowers.Count - 1; i++) {
                // fix up plant in flowers if needed 
                (ufruit.PdFlowerFruit(this.flowers.Items[i])).plant = this.plant;
            }
        }
    }
    
}
//The inflorescence is very simple; it creates a specified number of flowers over a specified period
//  of days. Each inflorescence on the plant has the same number of flowers. Since an inflorescence is
//  created by a meristem which accumulates biomass, nothing stands in the way of the inflorescence
//  producing the flowers according to schedule.
//  This method must act differently for inflorescences that produce flowers slowly (over a greater
//  number of days than flowers) than for those that produce many flowers in a few days.
//  The inflorescence can create no flowers until it reaches a specified fraction of its optimal biomass.
//Survey flowers and return true if all flowers have been drawn (they know), false if any have not been
//   drawn. This is mostly so a branched inflorescence can know if there are any flowers left to place
//   on its branched structure.
