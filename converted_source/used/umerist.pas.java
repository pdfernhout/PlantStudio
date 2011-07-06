// unit umerist

from conversion_common import *;
import usupport;
import uleaf;
import uinflor;
import umath;
import utdo;
import udomain;
import u3dexport;
import uturtle;
import utravers;
import ufiler;
import uplant;
import uintern;
import upart;
import delphi_compatability;


class PdMeristem extends PdPlantPart {
    public PdInternode phytomerAttachedTo;
    public long daysCreatingThisPlantPart;
    public boolean isActive;
    public boolean isApical;
    public boolean isReproductive;
    public short gender;
    
    public void newWithPlant(PdPlant aPlant) {
        this.create();
        this.InitializeWithPlant(aPlant);
    }
    
    public void destroy() {
        if (this.isReproductive) {
            if (this.isActive) {
                if (this.isApical) {
                    //not isApical
                    this.plant.numApicalActiveReproductiveMeristemsOrInflorescences -= 1;
                } else {
                    this.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences -= 1;
                }
                //not isActive
            } else {
                if (this.isApical) {
                    //not isApical
                    this.plant.numApicalInactiveReproductiveMeristems -= 1;
                } else {
                    this.plant.numAxillaryInactiveReproductiveMeristems -= 1;
                }
            }
        }
        super.destroy();
    }
    
    public void InitializeWithPlant(PdPlant aPlant) {
        // v1.6b1 removed inherited
        this.initialize(aPlant);
        // don't need to call any setIf... functions here because lists don't need to be changed yet 
        this.isApical = true;
        this.liveBiomass_pctMPB = 0.0;
        this.deadBiomass_pctMPB = 0.0;
        this.biomassDemand_pctMPB = 0.0;
        this.daysCreatingThisPlantPart = 0;
        this.isActive = false;
        this.isReproductive = false;
        this.gender = uplant.kGenderFemale;
        if (this.plant.floweringHasStarted && (this.plant.randomNumberGenerator.zeroToOne() <= this.plant.pMeristem.determinateProbability)) {
            this.setIfReproductive(true);
        }
    }
    
    public String getName() {
        result = "";
        result = "meristem";
        return result;
    }
    
    public void nextDay() {
        try {
            super.nextDay();
            if (this.isActive) {
                this.daysCreatingThisPlantPart += 1;
                if (!this.isReproductive) {
                    this.accumulateOrCreatePhytomer();
                } else {
                    this.accumulateOrCreateInflorescence();
                }
            } else {
                if (!this.isApical && !this.isReproductive && this.contemplateBranching()) {
                    this.setIfActive(true);
                }
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdMeristem.nextDay");
        }
    }
    
    public boolean contemplateBranching() {
        result = false;
        float decisionPercent = 0.0;
        float randomPercent = 0.0;
        PdInternode firstOnBranch = new PdInternode();
        
        if (this.plant.pMeristem.branchingIndex == 0) {
            //Decide if this meristem is going to become active and branch (start demanding photosynthate).
            //This method is called once per day to create a large pool of random tests, each with
            //very small probability, leading to a small number of occurrences with small variation.
            result = false;
            return result;
        }
        if (!this.plant.pMeristem.secondaryBranchingIsAllowed) {
            firstOnBranch = this.phytomerAttachedTo.firstPhytomerOnBranch();
            if ((firstOnBranch != this.plant.firstPhytomer)) {
                result = false;
                return result;
            }
        }
        if (this.plant.pMeristem.branchingIndex == 100) {
            result = true;
            return result;
        }
        if (this.phytomerAttachedTo.distanceFromApicalMeristem() < this.plant.pMeristem.branchingDistance) {
            if (this.plant.pMeristem.branchingDistance == 0) {
                decisionPercent = this.plant.pMeristem.branchingIndex;
            } else {
                decisionPercent = this.plant.pMeristem.branchingIndex * umath.min(1.0, umath.max(0.0, umath.safedivExcept(this.phytomerAttachedTo.distanceFromApicalMeristem(), this.plant.pMeristem.branchingDistance, 0)));
            }
            randomPercent = this.plant.randomNumberGenerator.randomPercent();
            result = randomPercent < decisionPercent;
        } else {
            decisionPercent = this.plant.pMeristem.branchingIndex;
            randomPercent = this.plant.randomNumberGenerator.randomPercent();
            result = randomPercent < decisionPercent;
        }
        return result;
    }
    
    public float optimalInitialPhytomerBiomass_pctMPB() {
        result = 0.0;
        result = uintern.PdInternode.optimalInitialBiomass_pctMPB(this.plant) + uleaf.PdLeaf.optimalInitialBiomass_pctMPB(this.plant);
        if (this.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementOpposite) {
            result = result + uleaf.PdLeaf.optimalInitialBiomass_pctMPB(this.plant);
        }
        return result;
    }
    
    public void accumulateOrCreatePhytomer() {
        float optimalInitialBiomass_pctMPB = 0.0;
        float minBiomassNeeded_pctMPB = 0.0;
        float fractionOfOptimalSize = 0.0;
        boolean shouldCreatePhytomer = false;
        
        try {
            shouldCreatePhytomer = false;
            optimalInitialBiomass_pctMPB = this.optimalInitialPhytomerBiomass_pctMPB();
            if ((this.liveBiomass_pctMPB >= optimalInitialBiomass_pctMPB)) {
                shouldCreatePhytomer = true;
            } else {
                minBiomassNeeded_pctMPB = optimalInitialBiomass_pctMPB * this.plant.pInternode.minFractionOfOptimalInitialBiomassToCreateInternode_frn;
                if ((this.liveBiomass_pctMPB >= minBiomassNeeded_pctMPB) && (this.daysCreatingThisPlantPart >= this.plant.pInternode.maxDaysToCreateInternodeIfOverMinFraction)) {
                    shouldCreatePhytomer = true;
                }
            }
            if (shouldCreatePhytomer) {
                fractionOfOptimalSize = umath.safedivExcept(this.liveBiomass_pctMPB, optimalInitialBiomass_pctMPB, 0);
                this.createPhytomer(fractionOfOptimalSize);
                this.liveBiomass_pctMPB = 0.0;
                this.daysCreatingThisPlantPart = 0;
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdMeristem.accumulateOrCreatePhytomer");
        }
    }
    
    public void accumulateOrCreateInflorescence() {
        float optimalInitialBiomass_pctMPB = 0.0;
        float minBiomassNeeded_pctMPB = 0.0;
        float fractionOfOptimalSize = 0.0;
        boolean shouldCreateInflorescence = false;
        
        try {
            if (this.phytomerAttachedTo.isFirstPhytomer || !this.isReproductive || !this.isActive) {
                return;
            }
            shouldCreateInflorescence = false;
            optimalInitialBiomass_pctMPB = uinflor.PdInflorescence.optimalInitialBiomass_pctMPB(this.plant, this.gender);
            if ((this.liveBiomass_pctMPB >= optimalInitialBiomass_pctMPB)) {
                shouldCreateInflorescence = true;
            } else {
                minBiomassNeeded_pctMPB = optimalInitialBiomass_pctMPB * this.plant.pInternode.minFractionOfOptimalInitialBiomassToCreateInternode_frn;
                if ((this.liveBiomass_pctMPB >= minBiomassNeeded_pctMPB) && (this.daysCreatingThisPlantPart >= this.plant.pInflor[this.gender].maxDaysToCreateInflorescenceIfOverMinFraction)) {
                    shouldCreateInflorescence = true;
                }
            }
            if (shouldCreateInflorescence) {
                fractionOfOptimalSize = umath.safedivExcept(this.liveBiomass_pctMPB, optimalInitialBiomass_pctMPB, 0);
                this.createInflorescence(fractionOfOptimalSize);
                this.liveBiomass_pctMPB = 0.0;
                this.daysCreatingThisPlantPart = 0;
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdMeristem.accumulateOrCreateInflorescence");
        }
    }
    
    public void traverseActivity(int mode, TObject traverserProxy) {
        PdTraverser traverser = new PdTraverser();
        float optimalBiomass_pctMPB = 0.0;
        float biomassToRemove_pctMPB = 0.0;
        
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
                    if ((!this.isActive) || (this.isReproductive)) {
                        // return vegetative demand to create a phytomer. no demand if meristem is inactive, meristem is
                        // in reproductive mode, or if meristem is axillary and attached to the first phytomer
                        // and there is NOT sympodial branching.
                        return;
                    }
                    if (((!this.isApical) && (this.phytomerAttachedTo.isFirstPhytomer) && (!this.plant.pMeristem.branchingIsSympodial))) {
                        return;
                    }
                    try {
                        optimalBiomass_pctMPB = uintern.PdInternode.optimalInitialBiomass_pctMPB(this.plant) + uleaf.PdLeaf.optimalInitialBiomass_pctMPB(this.plant);
                        if (this.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementOpposite) {
                            optimalBiomass_pctMPB = optimalBiomass_pctMPB + uleaf.PdLeaf.optimalInitialBiomass_pctMPB(this.plant);
                        }
                        this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, optimalBiomass_pctMPB, this.plant.pInternode.minDaysToCreateInternode);
                        traverser.total = traverser.total + this.biomassDemand_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (vegetative demand)");
                    }
                    break;
                case utravers.kActivityDemandReproductive:
                    if ((!this.isActive) || (!this.isReproductive)) {
                        // return reproductive demand to create an inflorescence. no demand if meristem is inactive,
                        // if it is in vegetative mode, or if it is attached to the first phytomer.
                        return;
                    }
                    if ((this.phytomerAttachedTo.isFirstPhytomer) && (!this.isApical)) {
                        return;
                    }
                    try {
                        this.biomassDemand_pctMPB = utravers.linearGrowthResult(this.liveBiomass_pctMPB, this.plant.pInflor[self.gender].optimalBiomass_pctMPB, this.plant.pInflor[self.gender].minDaysToCreateInflorescence);
                        traverser.total = traverser.total + this.biomassDemand_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (reproductive demand)");
                    }
                    break;
                case utravers.kActivityGrowVegetative:
                    if (!(this.isActive)) {
                        //Allocate new biomass by portion of demand. A phytomer cannot be made before the minimum number
                        //      of days has passed to make one phytomer.
                        return;
                    }
                    if (this.isReproductive) {
                        return;
                    }
                    try {
                        this.liveBiomass_pctMPB = this.liveBiomass_pctMPB + this.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (vegetative growth)");
                    }
                    break;
                case utravers.kActivityGrowReproductive:
                    if ((!this.isActive) || (!this.isReproductive)) {
                        return;
                    }
                    try {
                        this.liveBiomass_pctMPB = this.liveBiomass_pctMPB + this.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (reproductive growth)");
                    }
                    break;
                case utravers.kActivityStartReproduction:
                    this.startReproduction();
                    break;
                case utravers.kActivityFindPlantPartAtPosition:
                    if (umath.pointsAreCloseEnough(traverser.point, this.position())) {
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
                    if (!this.isActive) {
                        //called by phytomer
                        // free called by phytomer or inflorescence 
                        return;
                    }
                    if ((mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved) && (this.isReproductive)) {
                        return;
                    }
                    if ((mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved) && (!this.isReproductive)) {
                        return;
                    }
                    try {
                        // a meristem can lose all of its biomass 
                        traverser.total = traverser.total + this.liveBiomass_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (removal request)");
                    }
                    break;
                case utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                    if (!this.isActive) {
                        //called by phytomer
                        // free called by phytomer or inflorescence 
                        return;
                    }
                    if ((mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved) && (this.isReproductive)) {
                        return;
                    }
                    if ((mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved) && (!this.isReproductive)) {
                        return;
                    }
                    try {
                        // a meristem can lose all of its biomass 
                        traverser.total = traverser.total + this.liveBiomass_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (removal request)");
                    }
                    break;
                case utravers.kActivityRemoveVegetativeBiomass:
                    if (!this.isActive) {
                        return;
                    }
                    if ((mode == utravers.kActivityRemoveVegetativeBiomass) && (this.isReproductive)) {
                        return;
                    }
                    if ((mode == utravers.kActivityRemoveReproductiveBiomass) && (!this.isReproductive)) {
                        return;
                    }
                    try {
                        biomassToRemove_pctMPB = this.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
                        this.liveBiomass_pctMPB = this.liveBiomass_pctMPB - biomassToRemove_pctMPB;
                        this.deadBiomass_pctMPB = this.deadBiomass_pctMPB + biomassToRemove_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (removal)");
                    }
                    break;
                case utravers.kActivityRemoveReproductiveBiomass:
                    if (!this.isActive) {
                        return;
                    }
                    if ((mode == utravers.kActivityRemoveVegetativeBiomass) && (this.isReproductive)) {
                        return;
                    }
                    if ((mode == utravers.kActivityRemoveReproductiveBiomass) && (!this.isReproductive)) {
                        return;
                    }
                    try {
                        biomassToRemove_pctMPB = this.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass;
                        this.liveBiomass_pctMPB = this.liveBiomass_pctMPB - biomassToRemove_pctMPB;
                        this.deadBiomass_pctMPB = this.deadBiomass_pctMPB + biomassToRemove_pctMPB;
                    } catch (Exception e) {
                        usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (removal)");
                    }
                    break;
                case utravers.kActivityGatherStatistics:
                    this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAxillaryBud);
                    if (this.isReproductive) {
                        this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllReproductive);
                    } else {
                        this.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllVegetative);
                    }
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
                    throw new GeneralException.create("Problem: Unhandled mode in method PdMeristem.traverseActivity.");
                    break;
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdMeristem.traverseActivity");
        }
    }
    
    public void countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(PdTraverser traverser) {
        if (traverser == null) {
            return;
        }
        if (this.plant.pAxillaryBud.tdoParams.scaleAtFullSize > 0) {
            traverser.total3DExportPointsIn3DObjects += this.plant.pAxillaryBud.tdoParams.object3D.pointsInUse * this.plant.pAxillaryBud.tdoParams.repetitions;
            traverser.total3DExportTrianglesIn3DObjects += this.plant.pAxillaryBud.tdoParams.object3D.triangles.Count * this.plant.pAxillaryBud.tdoParams.repetitions;
            this.addExportMaterial(traverser, u3dexport.kExportPartMeristem, -1);
        }
    }
    
    public void report() {
        super.report();
        //debugPrint('meristem, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
        //DebugForm.printNested(plant.turtle.stackSize, 'meristem, age ' + IntToStr(age) + ' biomass '
        //    + floatToStr(liveBiomass_pctMPB));
    }
    
    public PdMeristem createAxillaryMeristem(int direction) {
        result = new PdMeristem();
        PdMeristem newMeristem = new PdMeristem();
        
        // create new axillary meristem attached to the same phytomer as this apical meristem is attached to.
        newMeristem = PdMeristem().create();
        newMeristem.InitializeWithPlant(this.plant);
        newMeristem.setIfApical(false);
        newMeristem.phytomerAttachedTo = this.phytomerAttachedTo;
        if ((direction == uplant.kDirectionLeft)) {
            this.phytomerAttachedTo.leftBranchPlantPart = newMeristem;
        } else {
            this.phytomerAttachedTo.rightBranchPlantPart = newMeristem;
        }
        result = newMeristem;
        return result;
    }
    
    public void setIfActive(boolean active) {
        if (this.isActive != active) {
            this.isActive = active;
            if (this.isReproductive) {
                if (this.isApical) {
                    if (this.isActive) {
                        this.plant.numApicalActiveReproductiveMeristemsOrInflorescences += 1;
                        this.plant.numApicalInactiveReproductiveMeristems -= 1;
                        //not isActive
                    } else {
                        this.plant.numApicalInactiveReproductiveMeristems += 1;
                        this.plant.numApicalActiveReproductiveMeristemsOrInflorescences -= 1;
                    }
                    //not isApical
                } else {
                    if (this.isActive) {
                        this.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences += 1;
                        this.plant.numAxillaryInactiveReproductiveMeristems -= 1;
                        //not isActive
                    } else {
                        this.plant.numAxillaryInactiveReproductiveMeristems += 1;
                        this.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences -= 1;
                    }
                }
            }
        }
    }
    
    public void setIfApical(boolean apical) {
        if (this.isApical != apical) {
            this.isApical = apical;
            if (this.isReproductive) {
                if (this.isActive) {
                    if (this.isApical) {
                        this.plant.numApicalActiveReproductiveMeristemsOrInflorescences += 1;
                        this.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences -= 1;
                        //not isApical
                    } else {
                        this.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences += 1;
                        this.plant.numApicalActiveReproductiveMeristemsOrInflorescences -= 1;
                    }
                    //not isActive
                } else {
                    if (this.isApical) {
                        this.plant.numApicalInactiveReproductiveMeristems += 1;
                        this.plant.numAxillaryInactiveReproductiveMeristems -= 1;
                        //not isApical
                    } else {
                        this.plant.numAxillaryInactiveReproductiveMeristems += 1;
                        this.plant.numApicalInactiveReproductiveMeristems -= 1;
                    }
                }
            }
        }
    }
    
    public void setIfReproductive(boolean reproductive) {
        if (this.isReproductive != reproductive) {
            //assume can only become reproductive and not go other way
            this.isReproductive = reproductive;
            if (this.isActive) {
                if (this.isApical) {
                    //not isApical
                    this.plant.numApicalActiveReproductiveMeristemsOrInflorescences += 1;
                } else {
                    this.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences += 1;
                }
                //not isActive
            } else {
                if (this.isApical) {
                    //not isApical
                    this.plant.numApicalInactiveReproductiveMeristems += 1;
                } else {
                    this.plant.numAxillaryInactiveReproductiveMeristems += 1;
                }
            }
        }
    }
    
    // create first phytomer of plant with optimal biomass. return phytomer created so plant can hold on to it.
    public PdInternode createFirstPhytomer() {
        result = new PdInternode();
        result = null;
        try {
            //CreatePhytomer(self.optimalInitialPhytomerBiomass_pctMPB);
            // v1.6b1 -- biomass was wrong, should be fraction
            this.createPhytomer(1.0);
            result = this.phytomerAttachedTo;
            if (this.plant.pGeneral.isDicot) {
                result.makeSecondSeedlingLeaf(this.optimalInitialPhytomerBiomass_pctMPB());
            }
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdMeristem.createFirstPhytomer");
        }
        return result;
    }
    
    // create new inflorescence. attach new inflor to phytomer this meristem is attached to,
    // then unattach this meristem from the phytomer and tell inflor pointer to self so inflor can free self
    // when it is freed.
    public void createInflorescence(float fractionOfOptimalSize) {
        PdInflorescence newInflorescence = new PdInflorescence();
        
        if (this.plant.partsCreated > udomain.domain.options.maxPartsPerPlant_thousands * 1000) {
            // v1.6b1
            return;
        }
        newInflorescence = uinflor.PdInflorescence().create();
        newInflorescence.initializeGenderApicalOrAxillary(this.plant, this.gender, this.isApical, fractionOfOptimalSize);
        newInflorescence.meristemThatCreatedMe = this;
        newInflorescence.phytomerAttachedTo = this.phytomerAttachedTo;
        if (this.isApical) {
            this.phytomerAttachedTo.nextPlantPart = newInflorescence;
        } else if (this.phytomerAttachedTo.leftBranchPlantPart == this) {
            this.phytomerAttachedTo.leftBranchPlantPart = newInflorescence;
        } else if (this.phytomerAttachedTo.rightBranchPlantPart == this) {
            this.phytomerAttachedTo.rightBranchPlantPart = newInflorescence;
        } else {
            throw new GeneralException.create("Problem: Branching incorrect in method PdMeristem.createInflorescence.");
        }
        this.phytomerAttachedTo = null;
    }
    
    public void createPhytomer(float fractionOfFullSize) {
        PdInternode newPhytomer = new PdInternode();
        PdMeristem leftMeristem = new PdMeristem();
        PdMeristem rightMeristem = new PdMeristem();
        
        if (this.plant.partsCreated > udomain.domain.options.maxPartsPerPlant_thousands * 1000) {
            // create new phytomer. fraction of full size is the amount of biomass the meristem accumulated
            // (in the number of days it had to create a phytomer) divided by the optimal biomass of a phytomer.
            // v1.6b1
            return;
        }
        newPhytomer = uintern.PdInternode.NewWithPlantFractionOfInitialOptimalSize(this.plant, fractionOfFullSize);
        newPhytomer.phytomerAttachedTo = this.phytomerAttachedTo;
        if ((this.phytomerAttachedTo != null)) {
            if (this.isApical) {
                this.phytomerAttachedTo.nextPlantPart = newPhytomer;
                if ((this.plant.pMeristem.branchingIsSympodial)) {
                    this.setIfActive(false);
                }
                // axillary 
            } else {
                if (this.phytomerAttachedTo.leftBranchPlantPart == this) {
                    this.phytomerAttachedTo.leftBranchPlantPart = newPhytomer;
                } else if (this.phytomerAttachedTo.rightBranchPlantPart == this) {
                    this.phytomerAttachedTo.rightBranchPlantPart = newPhytomer;
                } else {
                    throw new GeneralException.create("Problem: Branching incorrect in method PdMeristem.createPhytomer.");
                }
                this.setIfApical(true);
            }
            // set up pointers
            this.phytomerAttachedTo = newPhytomer;
            this.phytomerAttachedTo.nextPlantPart = this;
            if (this.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementAlternate) {
                leftMeristem = this.createAxillaryMeristem(uplant.kDirectionLeft);
                if (this.plant.pMeristem.branchingIsSympodial) {
                    leftMeristem.setIfActive(true);
                }
            } else {
                leftMeristem = this.createAxillaryMeristem(uplant.kDirectionLeft);
                rightMeristem = this.createAxillaryMeristem(uplant.kDirectionRight);
                if (this.plant.pMeristem.branchingIsSympodial) {
                    if ((this.plant.randomNumberGenerator.zeroToOne() < 0.5)) {
                        leftMeristem.setIfActive(true);
                    } else {
                        rightMeristem.setIfActive(true);
                    }
                }
            }
            // phytomerAttachedTo = nil (means this is first phytomer)
        } else {
            this.setIfApical(true);
            this.setIfActive(!this.plant.pMeristem.branchingIsSympodial);
            // set up pointers
            this.phytomerAttachedTo = newPhytomer;
            this.phytomerAttachedTo.nextPlantPart = this;
            if (this.plant.pMeristem.branchingIsSympodial) {
                if (this.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementAlternate) {
                    leftMeristem = this.createAxillaryMeristem(uplant.kDirectionLeft);
                    leftMeristem.setIfActive(true);
                } else {
                    leftMeristem = this.createAxillaryMeristem(uplant.kDirectionLeft);
                    rightMeristem = this.createAxillaryMeristem(uplant.kDirectionRight);
                    if ((this.plant.randomNumberGenerator.zeroToOne() < 0.5)) {
                        leftMeristem.setIfActive(true);
                    } else {
                        rightMeristem.setIfActive(true);
                    }
                }
            }
        }
    }
    
    public void draw() {
        int i = 0;
        
        KfTurtle turtle = new KfTurtle();
        float scale = 0.0;
        float daysToFullSize = 0.0;
        int numParts = 0;
        KfObject3D tdo = new KfObject3D();
        float minZ = 0.0;
        
        if ((this.plant.pAxillaryBud.tdoParams.scaleAtFullSize == 0)) {
            return;
        }
        //Draw meristem (only if buds are enlarged as in Brussels sprouts). Since this only very rarely happens,
        //  have these buds increase to maximum size in a constant number of days (5). Number of sections drawn
        //  (of the 3D object being rotated) is also set to a constant (5).
        turtle = this.plant.turtle;
        if ((turtle == null)) {
            return;
        }
        this.boundsRect = Rect(0, 0, 0, 0);
        if (this.hiddenByAmendment()) {
            return;
        } else {
            this.applyAmendmentRotations();
        }
        daysToFullSize = 5;
        scale = (this.plant.pAxillaryBud.tdoParams.scaleAtFullSize / 100.0) * (umath.min(1.0, umath.safedivExcept(this.age, daysToFullSize, 0)));
        if (this.isApical) {
            return;
        }
        try {
            numParts = 5;
            minZ = 0;
            tdo = this.plant.pAxillaryBud.tdoParams.object3D;
            turtle.ifExporting_startPlantPart(this.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartMeristem), this.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartMeristem));
            if (numParts > 0) {
                for (i = 0; i <= numParts - 1; i++) {
                    turtle.rotateX(256 / numParts);
                    turtle.push();
                    turtle.rotateZ(-64);
                    if (tdo != null) {
                        turtle.rotateX(this.angleWithSway(this.plant.pAxillaryBud.tdoParams.xRotationBeforeDraw));
                        turtle.rotateY(this.angleWithSway(this.plant.pAxillaryBud.tdoParams.yRotationBeforeDraw));
                        turtle.rotateZ(this.angleWithSway(this.plant.pAxillaryBud.tdoParams.zRotationBeforeDraw));
                        this.draw3DObject(tdo, scale, this.plant.pAxillaryBud.tdoParams.faceColor, this.plant.pAxillaryBud.tdoParams.backfaceColor, u3dexport.kExportPartMeristem);
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
            turtle.ifExporting_endPlantPart();
        } catch (Exception e) {
            usupport.messageForExceptionType(e, "PdMeristem.draw");
        }
    }
    
    public void startReproduction() {
        if ((this.plant.randomNumberGenerator.zeroToOne() <= this.plant.pMeristem.determinateProbability)) {
            //Decide gender and activity based on whether the plant has hermaphroditic or separate flowers, and if
            //    hermaphroditic, female and/or male flowers are located terminally or axially.
            this.setIfReproductive(true);
        }
        if (!this.isReproductive) {
            return;
        }
        this.setIfActive(false);
        this.gender = uplant.kGenderFemale;
        if (!this.plant.pGeneral.maleFlowersAreSeparate) {
            if (this.decideIfActiveHermaphroditic()) {
                this.gender = uplant.kGenderFemale;
            }
        } else {
            if (this.decideIfActiveMale()) {
                this.gender = uplant.kGenderMale;
            }
            if (this.decideIfActiveFemale()) {
                this.gender = uplant.kGenderFemale;
            }
        }
        if (this.willCreateInflorescence()) {
            this.setIfActive(true);
        }
    }
    
    public boolean decideIfActiveFemale() {
        result = false;
        //For the case of separate male and female flowers, decide if this meristem will be able to create
        //  a female inflorescence. Called by decideReproductiveGenderAndActivity.
        //If meristem is already male, then both male and female flowers are apical (or axillary).
        //  in that case, override with female only half the time.
        result = (this.isApical == this.plant.pInflor[uplant.kGenderFemale].isTerminal);
        if (result && (this.gender == uplant.kGenderMale)) {
            result = (this.plant.randomNumberGenerator.zeroToOne() < 0.5);
        }
        return result;
    }
    
    public boolean decideIfActiveHermaphroditic() {
        result = false;
        //For the case of hermaphroditic flowers, decide if this meristem will be able to create
        //  a hermaphroditic inflorescence (if flowers are hermaphroditic, female parameters are used).
        //  Called by decideReproductiveGenderAndActivity.
        result = (this.isApical == this.plant.pInflor[uplant.kGenderFemale].isTerminal);
        return result;
    }
    
    public boolean decideIfActiveMale() {
        result = false;
        //For the case of separate male and female flowers, decide if this meristem will be able to create
        //  a male inflorescence. Called by decideReproductiveGenderAndActivity.
        result = (this.isApical == this.plant.pInflor[uplant.kGenderMale].isTerminal);
        return result;
    }
    
    public int partType() {
        result = 0;
        result = uplant.kPartTypeMeristem;
        return result;
    }
    
    public boolean willCreateInflorescence() {
        result = false;
        float inflorProb = 0.0;
        float numExpected = 0.0;
        float numAlready = 0.0;
        
        try {
            if ((this.phytomerAttachedTo.isFirstPhytomer) && (!this.isApical)) {
                //Determine probability that this meristem will produce an inflorescence, which is
                //  number of inflorescences left to be placed on plant / number of meristems open to develop
                //  (apical meristems if flowering is apical, or axillary meristems if flowering is axillary).
                //  First phytomer on plant is for seedling leaves and cannot produce inflorescences.
                result = false;
                return result;
            }
            if (this.isApical) {
                numExpected = this.plant.pGeneral.numApicalInflors;
                numAlready = this.plant.numApicalActiveReproductiveMeristemsOrInflorescences;
                inflorProb = umath.safedivExcept(numExpected - numAlready, this.plant.numApicalInactiveReproductiveMeristems, 0);
            } else {
                numExpected = this.plant.pGeneral.numAxillaryInflors;
                numAlready = this.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences;
                inflorProb = umath.safedivExcept(numExpected - numAlready, this.plant.numAxillaryInactiveReproductiveMeristems, 0);
            }
            if ((numExpected <= 3)) {
                //If there are only a few inflorescences on the plant, don't mess with probability; place on
                //  first few meristems.
                inflorProb = 1.0;
            }
            if ((this.plant.randomNumberGenerator.zeroToOne() < inflorProb)) {
                //Check that the expected number of inflorescences hasn't been created already.
                result = (numAlready < numExpected);
            } else {
                result = false;
            }
        } catch (Exception e) {
            result = false;
            usupport.messageForExceptionType(e, "PdMeristem.willCreateInflorescence");
        }
        return result;
    }
    
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.kPdMeristem;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        super.streamDataWithFiler(filer, cvir);
        this.daysCreatingThisPlantPart = filer.streamLongint(this.daysCreatingThisPlantPart);
        this.isActive = filer.streamBoolean(this.isActive);
        this.isApical = filer.streamBoolean(this.isApical);
        this.isReproductive = filer.streamBoolean(this.isReproductive);
        this.gender = filer.streamSmallint(this.gender);
    }
    
}
