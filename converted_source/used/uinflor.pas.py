# unit uinflor

from conversion_common import *
import usupport
import uamendmt
import uclasses
import umath
import udomain
import u3dexport
import uturtle
import udebug
import utravers
import ufiler
import ucollect
import ufruit
import uplant
import uintern
import upart
import delphi_compatability

class PdInflorescence(PdPlantPart):
    def __init__(self):
        self.flowers = TListCollection()
        self.numFlowers = 0
        self.numFlowersEachDay = 0
        self.daysBetweenFlowerAppearances = 0
        self.daysSinceLastFlowerAppeared = 0
        self.daysSinceStartedMakingFlowers = 0
        self.isApical = false
        self.meristemThatCreatedMe = PdPlantPart()
        self.phytomerAttachedTo = PdInternode()
        self.fractionOfOptimalSizeWhenCreated = 0.0
    
    def create(self):
        PdPlantPart.create(self)
        self.flowers = ucollect.TListCollection().Create()
        self.meristemThatCreatedMe = None
        return self
    
    def destroy(self):
        self.flowers.free
        self.flowers = None
        self.meristemThatCreatedMe.free
        self.meristemThatCreatedMe = None
        PdPlantPart.destroy(self)
    
    def getName(self):
        result = ""
        result = "inflorescence"
        return result
    
    def determineAmendmentAndAlsoForChildrenIfAny(self):
        i = 0
        amendmentToPass = PdPlantDrawingAmendment()
        
        PdPlantPart.determineAmendmentAndAlsoForChildrenIfAny(self)
        if self.amendment != None:
            amendmentToPass = self.amendment
        else:
            amendmentToPass = self.parentAmendment
        if self.flowers.Count > 0:
            for i in range(0, self.flowers.Count):
                ufruit.PdFlowerFruit(self.flowers.Items[i]).parentAmendment = amendmentToPass
    
    def initializeGenderApicalOrAxillary(self, aPlant, aGender, initAsApical, fractionOfOptimalSize):
        daysToAllFlowers = 0.0
        
        try:
            self.initialize(aPlant)
            self.gender = aGender
            self.isApical = initAsApical
            self.daysSinceLastFlowerAppeared = 0
            self.daysSinceStartedMakingFlowers = 0
            self.fractionOfOptimalSizeWhenCreated = umath.min(1.0, fractionOfOptimalSize)
            #The inflorescence must know whether it produces flowers slowly (over a greater number of days than flowers)
            #  or produces many flowers in a few days.
            daysToAllFlowers = self.plant.pInflor[self.gender].daysToAllFlowersCreated
            self.numFlowers = self.plant.pInflor[self.gender].numFlowersOnMainBranch + self.plant.pInflor[self.gender].numFlowersPerBranch * self.plant.pInflor[self.gender].numBranches
            self.daysBetweenFlowerAppearances = 0
            self.numFlowersEachDay = 0
            if self.numFlowers > 0:
                if self.numFlowers == 1:
                    self.numFlowersEachDay = 1
                elif self.numFlowers == daysToAllFlowers:
                    self.numFlowersEachDay = 1
                elif self.numFlowers > daysToAllFlowers:
                    self.numFlowersEachDay = intround(umath.safedivExcept(1.0 * self.numFlowers, 1.0 * daysToAllFlowers, 0))
                else:
                    self.daysBetweenFlowerAppearances = intround(umath.safedivExcept(1.0 * daysToAllFlowers, 1.0 * self.numFlowers, 0))
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInflorescence.InitializeGenderApicalOrAxillary")
    
    def optimalInitialBiomass_pctMPB(self, drawingPlant, gender):
        result = 0.0
        if (gender < 0) or (gender > 1):
            result = 0.0
        else:
            result = drawingPlant.pInflor[gender].optimalBiomass_pctMPB * drawingPlant.pInflor[gender].minFractionOfOptimalBiomassToCreateInflorescence_frn
        return result
    
    def nextDay(self):
        i = 0
        numFlowersToCreateToday = 0
        biomassToMakeFlowers_pctMPB = 0.0
        
        try:
            PdPlantPart.nextDay(self)
            if self.flowers.Count > 0:
                for i in range(0, self.flowers.Count):
                    ufruit.PdFlowerFruit(self.flowers.Items[i]).nextDay()
            #if self.age < plant.pInflor[gender].maxDaysToGrow then
            biomassToMakeFlowers_pctMPB = self.plant.pInflor[self.gender].minFractionOfOptimalBiomassToMakeFlowers_frn * self.plant.pInflor[self.gender].optimalBiomass_pctMPB
            if self.liveBiomass_pctMPB >= biomassToMakeFlowers_pctMPB:
                self.daysSinceStartedMakingFlowers += 1
                if (self.flowers.Count <= 0) and (self.numFlowers > 0):
                    # make first flower on first day
                    self.createFlower()
                elif (self.flowers.Count < self.numFlowers):
                    if (self.daysBetweenFlowerAppearances > 0):
                        if (self.daysSinceLastFlowerAppeared >= self.daysBetweenFlowerAppearances):
                            self.createFlower()
                            self.daysSinceLastFlowerAppeared = 0
                        else:
                            self.daysSinceLastFlowerAppeared += 1
                    else:
                        numFlowersToCreateToday = umath.intMin(self.numFlowersEachDay, self.numFlowers - self.flowers.Count)
                        if numFlowersToCreateToday > 0:
                            for i in range(0, numFlowersToCreateToday):
                                self.createFlower()
                        self.daysSinceLastFlowerAppeared = 0
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInflorescence.nextDay")
    
    def traverseActivity(self, mode, traverserProxy):
        traverser = PdTraverser()
        newBiomass_pctMPB = 0.0
        biomassToRemove_pctMPB = 0.0
        i = 0
        numLines = 0
        
        PdPlantPart.traverseActivity(self, mode, traverserProxy)
        traverser = utravers.PdTraverser(traverserProxy)
        if traverser == None:
            return
        if self.hasFallenOff and (mode != utravers.kActivityStream) and (mode != utravers.kActivityFree):
            return
        try:
            if (mode != utravers.kActivityDraw):
                if self.flowers.Count > 0:
                    for i in range(0, self.flowers.Count):
                        (ufruit.PdFlowerFruit(self.flowers.Items[i])).traverseActivity(mode, traverser)
            if mode == utravers.kActivityNone:
                pass
            elif mode == utravers.kActivityNextDay:
                self.nextDay()
            elif mode == utravers.kActivityDemandVegetative:
                pass
            elif mode == utravers.kActivityDemandReproductive:
                if (self.age > self.plant.pInflor[self.gender].maxDaysToGrow):
                    # no vegetative demand 
                    self.biomassDemand_pctMPB = 0.0
                    return
                try:
                    self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, self.plant.pInflor[self.gender].minDaysToGrow)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdInflorescence.traverseActivity (reproductive demand)")
            elif mode == utravers.kActivityGrowVegetative:
                pass
            elif mode == utravers.kActivityGrowReproductive:
                if self.age > self.plant.pInflor[self.gender].maxDaysToGrow:
                    # no vegetative growth 
                    return
                newBiomass_pctMPB = self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + newBiomass_pctMPB
            elif mode == utravers.kActivityStartReproduction:
                pass
            elif mode == utravers.kActivityFindPlantPartAtPosition:
                if umath.pointsAreCloseEnough(traverser.point, self.position()):
                    # cannot switch 
                    traverser.foundPlantPart = self
                    traverser.finished = true
            elif mode == utravers.kActivityDraw:
                self.draw()
            elif mode == utravers.kActivityReport:
                pass
            elif mode == utravers.kActivityStream:
                pass
            elif mode == utravers.kActivityFree:
                pass
            elif mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved:
                pass
            elif mode == utravers.kActivityRemoveVegetativeBiomass:
                pass
            elif mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                #streaming called by phytomer
                # free called by phytomer 
                # none 
                # none 
                traverser.total = traverser.total + self.liveBiomass_pctMPB
            elif mode == utravers.kActivityRemoveReproductiveBiomass:
                biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
            elif mode == utravers.kActivityGatherStatistics:
                if self.gender == uplant.kGenderMale:
                    self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeMaleInflorescence)
                else:
                    self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFemaleInflorescence)
                self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllReproductive)
            elif mode == utravers.kActivityCountPlantParts:
                pass
            elif mode == utravers.kActivityFindPartForPartID:
                pass
            elif mode == utravers.kActivityCountTotalMemoryUse:
                traverser.totalMemorySize += self.instanceSize
            elif mode == utravers.kActivityCalculateBiomassForGravity:
                self.biomassOfMeAndAllPartsAboveMe_pctMPB = self.biomassOfMeAndAllPartsConnectedToMe_pctMPB()
            elif mode == utravers.kActivityCountPointsAndTrianglesFor3DExport:
                self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser)
            else :
                raise GeneralException.create("Problem: Unhandled mode in method PdInflorescence.traverseActivity.")
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInflorescence.traverseActivity")
    
    def countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(self, traverser):
        numLines = 0
        
        if traverser == None:
            return
        if self.plant.pInflor[self.gender].bractTdoParams.scaleAtFullSize > 0:
            # bracts
            traverser.total3DExportPointsIn3DObjects += self.plant.pInflor[self.gender].bractTdoParams.object3D.pointsInUse * self.plant.pInflor[self.gender].bractTdoParams.repetitions
            traverser.total3DExportTrianglesIn3DObjects += self.plant.pInflor[self.gender].bractTdoParams.object3D.triangles.Count * self.plant.pInflor[self.gender].bractTdoParams.repetitions
            self.addExportMaterial(traverser, u3dexport.kExportPartInflorescenceBractFemale, u3dexport.kExportPartInflorescenceBractMale)
        # pedicels and inflorescence internodes
        numLines = self.plant.pInflor[self.gender].numBranches
        if not self.plant.pInflor[self.gender].branchesAreAlternate:
            numLines = numLines * 2
        if self.plant.pInflor[self.gender].internodeLength_mm > 0:
            self.addExportMaterial(traverser, u3dexport.kExportPartInflorescenceInternodeFemale, u3dexport.kExportPartInflorescenceInternodeMale)
        # peduncle
        numLines += 1
        traverser.total3DExportStemSegments += numLines
        if self.plant.pInflor[self.gender].peduncleLength_mm > 0:
            self.addExportMaterial(traverser, u3dexport.kExportPartInflorescenceStalkFemale, u3dexport.kExportPartInflorescenceStalkMale)
    
    def report(self):
        PdPlantPart.report(self)
        udebug.DebugPrint(IntToStr(self.numFlowers) + " flowers")
        # note flowers will print first 
        # debugPrint('inflorescence, age '  + IntToStr(age));
        #DebugForm.printNested(plant.turtle.stackSize, 'inflorescence, age '  + IntToStr(age));
    
    def biomassOfMeAndAllPartsConnectedToMe_pctMPB(self):
        result = 0.0
        i = 0
        
        result = self.totalBiomass_pctMPB()
        if self.flowers.Count > 0:
            for i in range(0, self.flowers.Count):
                result = result + (ufruit.PdFlowerFruit(self.flowers.Items[i])).totalBiomass_pctMPB()
        return result
    
    def allFlowersHaveBeenDrawn(self):
        result = false
        i = 0
        
        result = true
        if self.flowers.Count > 0:
            for i in range(0, self.flowers.Count):
                if not ((ufruit.PdFlowerFruit(self.flowers.Items[i])).hasBeenDrawn):
                    result = false
                    return result
        return result
    
    def addDependentPartsToList(self, aList):
        i = 0L
        
        if self.flowers.Count > 0:
            for i in range(0, self.flowers.Count):
                aList.Add(self.flowers.Items[i])
    
    def createFlower(self):
        aFlowerFruit = PdFlowerFruit()
        
        if self.plant.partsCreated > udomain.domain.options.maxPartsPerPlant_thousands * 1000:
            # create new flower/fruit object 
            # v1.6b1
            return
        aFlowerFruit = ufruit.PdFlowerFruit().create()
        aFlowerFruit.initializeGender(self.plant, self.gender)
        self.flowers.Add(aFlowerFruit)
    
    def deleteFlower(self, theFlower):
        # remove flower object from list 
        self.flowers.Remove(theFlower)
    
    def draw(self):
        i = 0
        turtle = KfTurtle()
        
        if not self.shouldDraw():
            return
        turtle = self.plant.turtle
        self.boundsRect = Rect(0, 0, 0, 0)
        turtle.push()
        if self.hiddenByAmendment():
            # amendment rotation handled in drawStemSegment for peduncle
            turtle.pop()
            return
        try:
            if self.flowers.Count > 0:
                for i in range(0, self.flowers.Count):
                    ufruit.PdFlowerFruit(self.flowers.Items[i]).hasBeenDrawn = false
            self.calculateColors()
            turtle.ifExporting_startNestedGroupOfPlantParts(self.genderString() + " inflorescence", self.genderString() + "Inflor", u3dexport.kNestingTypeInflorescence)
            if (self.flowers.Count > 0):
                self.drawBracts()
                self.drawPeduncle()
                if (self.plant.pInflor[self.gender].isHead):
                    self.drawHead()
                else:
                    self.drawApex(self.plant.pInflor[self.gender].numFlowersOnMainBranch, 0, true)
            turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeInflorescence)
            turtle.pop()
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInflorescence.draw")
    
    def shouldDraw(self):
        result = false
        i = 0L
        flowerFruit = PdFlowerFruit()
        
        # if inflorescence has at least one flower or non-fallen fruit, should draw 
        result = true
        if self.flowers.Count > 0:
            for i in range(0, self.flowers.Count):
                flowerFruit = ufruit.PdFlowerFruit(self.flowers.Items[i])
                if flowerFruit == None:
                    continue
                if not flowerFruit.hasFallenOff:
                    return result
        result = false
        return result
    
    def drawApex(self, internodeCount, flowerIndexOffset, mainBranch):
        turtle = KfTurtle()
        
        i = 0
        branchesDrawn = 0
        
        i = 0
        #Draw inflorescence in raceme, panicle, or umbel form. This method uses the recursive algorithm
        #     we first developed to draw the entire plant.
        turtle = self.plant.turtle
        if turtle == None:
            return
        branchesDrawn = 0
        if internodeCount > 0:
            if mainBranch:
                # draw the flowers on the main stem first, because if any are not going to be drawn for
                # want of available flowers, the branches should lose them.
                turtle.push()
            if mainBranch:
                while branchesDrawn < self.plant.pInflor[self.gender].numBranches:
                    self.drawInternode(i)
                    branchesDrawn += 1
            # draw flowers on main stem first
            i = internodeCount
            while i >= 1:
                if self.plant.pInflor[self.gender].flowersSpiralOnStem:
                    #param
                    turtle.rotateX(98)
                self.drawInternode(i)
                turtle.push()
                self.drawFlower(flowerIndexOffset + i)
                turtle.pop()
                i -= 1
            if mainBranch:
                turtle.pop()
        branchesDrawn = 0
        if mainBranch:
            while branchesDrawn < self.plant.pInflor[self.gender].numBranches:
                if self.plant.pInflor[self.gender].flowersSpiralOnStem:
                    # draw branches
                    #param
                    turtle.rotateX(98)
                self.drawInternode(i)
                self.drawAxillaryBud(self.plant.pInflor[self.gender].numFlowersPerBranch, self.plant.pInflor[self.gender].numFlowersOnMainBranch + branchesDrawn * self.plant.pInflor[self.gender].numFlowersPerBranch)
                branchesDrawn += 1
                if (not self.plant.pInflor[self.gender].branchesAreAlternate) and (branchesDrawn < self.plant.pInflor[self.gender].numBranches):
                    turtle.push()
                    turtle.rotateX(128)
                    self.drawAxillaryBud(self.plant.pInflor[self.gender].numFlowersPerBranch, self.plant.pInflor[self.gender].numFlowersOnMainBranch + branchesDrawn * self.plant.pInflor[self.gender].numFlowersPerBranch)
                    branchesDrawn += 1
                    turtle.pop()
    
    def drawBracts(self):
        scale = 0.0
        length = 0.0
        width = 0.0
        angle = 0.0
        propFullSize = 0.0
        turtle = KfTurtle()
        i = 0
        turnPortion = 0
        leftOverDegrees = 0
        addThisTime = 0
        addition = 0.0
        carryOver = 0.0
        
        if (self.plant.turtle == None):
            return
        if self.plant.pInflor[self.gender].bractTdoParams.scaleAtFullSize <= 0:
            return
        turtle = self.plant.turtle
        turtle.push()
        turtle.ifExporting_startNestedGroupOfPlantParts(self.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartInflorescenceBractFemale), self.shortNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartInflorescenceBractFemale), u3dexport.kNestingTypeInflorescence)
        propFullSize = umath.safedivExcept(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, 0)
        scale = ((self.plant.pInflor[self.gender].bractTdoParams.scaleAtFullSize / 100.0) * propFullSize)
        turtle.rotateX(self.angleWithSway(self.plant.pInflor[self.gender].bractTdoParams.xRotationBeforeDraw))
        turtle.rotateY(self.angleWithSway(self.plant.pInflor[self.gender].bractTdoParams.yRotationBeforeDraw))
        turtle.rotateZ(self.angleWithSway(self.plant.pInflor[self.gender].bractTdoParams.zRotationBeforeDraw))
        if (self.plant.pInflor[self.gender].bractTdoParams.radiallyArranged) and (self.plant.pInflor[self.gender].bractTdoParams.repetitions > 0):
            turnPortion = 256 / self.plant.pInflor[self.gender].bractTdoParams.repetitions
            leftOverDegrees = 256 - turnPortion * self.plant.pInflor[self.gender].bractTdoParams.repetitions
            if leftOverDegrees > 0:
                addition = umath.safedivExcept(leftOverDegrees, self.plant.pInflor[self.gender].bractTdoParams.repetitions, 0)
            else:
                addition = 0
            carryOver = 0
            for i in range(0, self.plant.pInflor[self.gender].bractTdoParams.repetitions):
                turtle.push()
                #aligns object as stored in the file to way should draw on plant
                turtle.rotateY(-64)
                # why? i don't know.
                turtle.rotateX(64)
                turtle.rotateX(self.plant.pInflor[self.gender].bractTdoParams.pullBackAngle)
                self.draw3DObject(self.plant.pInflor[self.gender].bractTdoParams.object3D, scale, self.plant.pInflor[self.gender].bractTdoParams.faceColor, self.plant.pInflor[self.gender].bractTdoParams.backfaceColor, u3dexport.kExportPartInflorescenceBractFemale)
                turtle.pop()
                addThisTime = trunc(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                turtle.rotateX(turnPortion + addThisTime)
        else:
            turtle.push()
            #aligns object as stored in the file to way should draw on plant
            turtle.rotateY(-64)
            # why? i don't know.
            turtle.rotateX(64)
            turtle.rotateX(self.plant.pInflor[self.gender].bractTdoParams.pullBackAngle)
            self.draw3DObject(self.plant.pInflor[self.gender].bractTdoParams.object3D, scale, self.plant.pInflor[self.gender].bractTdoParams.faceColor, self.plant.pInflor[self.gender].bractTdoParams.backfaceColor, u3dexport.kExportPartInflorescenceBractFemale)
            turtle.pop()
        turtle.pop()
        turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeInflorescence)
    
    def drawPeduncle(self):
        length = 0.0
        width = 0.0
        zAngle = 0.0
        propFullSize = 0.0
        
        try:
            #Draw peduncle, which is the primary inflorescence stalk. If the inflorescence has only one flower,
            #     this is the only part drawn. If the inflorescence is apical, the stalk may be longer (e.g. in bolting
            #     plants) and is specified by a different parameter.
            zAngle = 0
            if (self.phytomerAttachedTo != None):
                if (self.phytomerAttachedTo.leftBranchPlantPart == self):
                    zAngle = self.plant.pInflor[self.gender].peduncleAngleFromVegetativeStem
                elif (self.phytomerAttachedTo.rightBranchPlantPart == self):
                    zAngle = self.plant.pInflor[self.gender].peduncleAngleFromVegetativeStem
                    self.plant.turtle.rotateX(128)
                elif self.isApical:
                    zAngle = self.plant.pInflor[self.gender].apicalStalkAngleFromVegetativeStem
            propFullSize = umath.safedivExcept(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, 0)
            if self.isApical:
                len = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].terminalStalkLength_mm, propFullSize)
            else:
                len = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].peduncleLength_mm, propFullSize)
            width = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].internodeWidth_mm, propFullSize)
            #Use no angle here because phytomer makes the rotation before the inflorescence is drawn.
            self.drawStemSegment(len, width, zAngle, 0, self.plant.pInflor[self.gender].stalkColor, upart.kDontTaper, u3dexport.kExportPartInflorescenceStalkFemale, upart.kUseAmendment)
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInflorescence.drawPeduncle")
    
    def drawAxillaryBud(self, internodeCount, flowerIndexOffset):
        turtle = KfTurtle()
        angle = 0.0
        
        #This message is sent when the inflorescence is branched. The decision to create a branch is
        #     made before the message is sent. Note the check if all flowers have been drawn; this prevents
        #     scrawly lines with no flowers.
        turtle = self.plant.turtle
        if (turtle == None):
            return
        if (self.allFlowersHaveBeenDrawn()):
            return
        angle = self.angleWithSway(self.plant.pInflor[self.gender].branchAngle)
        turtle.push()
        turtle.rotateZ(angle)
        self.drawApex(internodeCount, flowerIndexOffset, false)
        turtle.pop()
    
    def drawFlower(self, internodeCount):
        length = 0.0
        width = 0.0
        angle = 0.0
        propFullSize = 0.0
        flowerIndex = 0
        
        try:
            if (self.allFlowersHaveBeenDrawn()):
                #Draw one flower, remembering that internodeCount goes from flowers size down to 1,
                #  but flowers are in the order formed.
                #  If the oldest flowers on the inflorescence are at the bottom (acropetal),
                #  draw the flowers in reverse order from internodeCount (which is in the order they were formed).
                #  If the oldest flowers on the inflorescence are at the top (basipetal),
                #  draw the flowers in the order presented by internodeCount
                #     which is in reverse order to how they were formed).
                #  In most plants the older flowers are lower.
                return
            propFullSize = umath.safedivExcept(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, 0)
            len = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].pedicelLength_mm, propFullSize)
            width = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].internodeWidth_mm, propFullSize)
            angle = self.angleWithSway(self.plant.pInflor[self.gender].pedicelAngle)
            if (self.plant.pInflor[self.gender].flowersDrawTopToBottom):
                flowerIndex = internodeCount
            else:
                flowerIndex = self.flowers.Count - internodeCount + 1
            self.plant.turtle.ifExporting_startNestedGroupOfPlantParts(self.genderString() + " pedicel and flower/fruit", self.genderString() + "PedicelFlower", u3dexport.kNestingTypePedicelAndFlowerFruit)
            self.drawStemSegment(len, width, angle, 0, self.plant.pInflor[self.gender].pedicelColor, self.plant.pInflor[self.gender].pedicelTaperIndex, u3dexport.kExportPartPedicelFemale, upart.kDontUseAmendment)
            if (flowerIndex - 1 >= 0) and (flowerIndex - 1 <= self.flowers.Count - 1):
                ufruit.PdFlowerFruit(self.flowers.Items[flowerIndex - 1]).draw()
            self.plant.turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypePedicelAndFlowerFruit)
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInflorescence.drawFlower")
    
    def drawHead(self):
        turtle = KfTurtle()
        i = 0
        turnPortion = 0
        leftOverDegrees = 0
        addThisTime = 0
        addition = 0.0
        carryOver = 0.0
        
        # v1.4
        # v1.4
        #Draw the inflorescences in a radial pattern; this is for a head such as a sunflower.
        turtle = self.plant.turtle
        if (turtle == None):
            return
        turtle.rotateY(64)
        turtle.rotateZ(64)
        # give a little angle down to make it look more natural 
        turtle.rotateY(32)
        if self.flowers.Count > 0:
            # new v1.4
            turnPortion = 256 / self.flowers.Count
            leftOverDegrees = 256 - turnPortion * self.flowers.Count
            if leftOverDegrees > 0:
                addition = umath.safedivExcept(leftOverDegrees, self.flowers.Count, 0)
            else:
                addition = 0
            carryOver = 0
            for i in range(self.flowers.Count - 1, 0 + 1):
                addThisTime = trunc(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                # was 256 / flowers.count
                turtle.rotateZ(turnPortion + addThisTime)
                turtle.push()
                # v1.4 added one, was bug, was not drawing first flower
                self.drawFlower(i + 1)
                turtle.pop()
    
    def drawInternode(self, internodeCount):
        length = 0.0
        width = 0.0
        zAngle = 0.0
        yAngle = 0.0
        propFullSize = 0.0
        
        try:
            if (self.allFlowersHaveBeenDrawn()):
                #Draw the inflorescence internode, which is the portion of inflorescence stem between where successive
                #  flower pedicels come off. Note that this is not drawn if all flowers have been drawn; this prevents
                #  straggly lines in branched inflorescences.
                return
            if (self.plant.pInflor[self.gender].internodeLength_mm == 0.0):
                return
            propFullSize = umath.safedivExcept(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, 0)
            len = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].internodeLength_mm, propFullSize)
            width = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].internodeWidth_mm, propFullSize)
            zAngle = self.angleWithSway(self.plant.pInflor[self.gender].angleBetweenInternodes)
            yAngle = self.angleWithSway(0)
            self.drawStemSegment(len, width, zAngle, yAngle, self.plant.pInflor[self.gender].stalkColor, upart.kDontTaper, u3dexport.kExportPartInflorescenceInternodeFemale, upart.kDontUseAmendment)
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInflorescence.drawInternode")
    
    def lengthOrWidthAtAgeForFraction(self, starting, fraction):
        result = 0.0
        ageBounded = 0.0
        
        result = 0.0
        try:
            ageBounded = umath.min(self.plant.pInflor[self.gender].daysToAllFlowersCreated, self.daysSinceStartedMakingFlowers)
            if self.plant.pInflor[self.gender].daysToAllFlowersCreated != 0:
                result = umath.safedivExcept(starting * ageBounded, self.plant.pInflor[self.gender].daysToAllFlowersCreated, 0) * fraction
            else:
                result = starting * ageBounded * fraction
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInflorescence.lengthOrWidthAtAgeForFraction")
        return result
    
    def flower(self, index):
        result = PdFlowerFruit()
        result = self.flowers.Items[index]
        return result
    
    def partType(self):
        result = 0
        result = uplant.kPartTypeInflorescence
        return result
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdInflorescence
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        i = 0L
        
        PdPlantPart.streamDataWithFiler(self, filer, cvir)
        self.daysSinceStartedMakingFlowers = filer.streamSmallint(self.daysSinceStartedMakingFlowers)
        self.numFlowersEachDay = filer.streamSmallint(self.numFlowersEachDay)
        self.numFlowers = filer.streamSmallint(self.numFlowers)
        self.daysBetweenFlowerAppearances = filer.streamSmallint(self.daysBetweenFlowerAppearances)
        self.daysSinceLastFlowerAppeared = filer.streamSmallint(self.daysSinceLastFlowerAppeared)
        self.isApical = filer.streamBoolean(self.isApical)
        self.fractionOfOptimalSizeWhenCreated = filer.streamSingle(self.fractionOfOptimalSizeWhenCreated)
        if filer.isReading():
            self.meristemThatCreatedMe = None
        self.flowers.streamUsingFiler(filer, ufruit.PdFlowerFruit)
        if filer.isReading() and (self.flowers.Count > 0):
            for i in range(0, self.flowers.Count):
                # fix up plant in flowers if needed 
                (ufruit.PdFlowerFruit(self.flowers.Items[i])).plant = self.plant
    
#The inflorescence is very simple; it creates a specified number of flowers over a specified period
#  of days. Each inflorescence on the plant has the same number of flowers. Since an inflorescence is
#  created by a meristem which accumulates biomass, nothing stands in the way of the inflorescence
#  producing the flowers according to schedule.
#  This method must act differently for inflorescences that produce flowers slowly (over a greater
#  number of days than flowers) than for those that produce many flowers in a few days.
#  The inflorescence can create no flowers until it reaches a specified fraction of its optimal biomass.
#Survey flowers and return true if all flowers have been drawn (they know), false if any have not been
#   drawn. This is mostly so a branched inflorescence can know if there are any flowers left to place
#   on its branched structure.
