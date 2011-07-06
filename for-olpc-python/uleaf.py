# unit uleaf

from conversion_common import *
import upart
import umath
import usupport
import utravers
import uplant
import u3dexport

"""
import uclasses
import uturtle
import udebug
import utdo
import ufiler
import delphi_compatability
"""

# const
kNumCompoundLeafRandomSwayIndexes = 49

class PdLeaf(upart.PdPlantPart):
    def __init__(self):
        upart.PdPlantPart.__init__(self)
        self.sCurveParams = umath.SCurveStructure()
        self.propFullSize = 0.0
        self.biomassAtCreation_pctMPB = 0.0
        self.compoundLeafRandomSwayIndexes = [0] * (kNumCompoundLeafRandomSwayIndexes + 1)
    
    def NewWithPlantFractionOfOptimalSize(self, aPlant, aFraction):
        self.initializeFractionOfOptimalSize(aPlant, aFraction)
        return self
    
    def initializeFractionOfOptimalSize(self, thePlant, aFraction):
        try:
            self.initialize(thePlant)
            #Plant sets this from outside on first phytomer.
            self.isSeedlingLeaf = False
            self.liveBiomass_pctMPB = aFraction * PdLeaf.optimalInitialBiomass_pctMPB(self.plant)
            self.deadBiomass_pctMPB = 0.0
            self.propFullSize = umath.safedivExcept(self.liveBiomass_pctMPB, self.plant.pLeaf.optimalBiomass_pctMPB, 1.0)
            if self.plant.pLeaf.compoundNumLeaflets > 1:
                for i in range(0, kNumCompoundLeafRandomSwayIndexes + 1):
                    self.compoundLeafRandomSwayIndexes[i] = self.plant.randomNumberGenerator.zeroToOne()
        except Exception, e:
            # PDF PORT __ FOR TESTING
            raise
            usupport.messageForExceptionType(e, "PdLeaf.initializeFractionOfOptimalSize")
    
    def optimalInitialBiomass_pctMPB(self, drawingPlant):
        result = drawingPlant.pLeaf.optimalFractionOfOptimalBiomassAtCreation_frn * drawingPlant.pLeaf.optimalBiomass_pctMPB
        return result
    optimalInitialBiomass_pctMPB = classmethod(optimalInitialBiomass_pctMPB)
    
    def getName(self):
        result = "leaf"
        return result
    
    def nextDay(self):
        try:
            upart.PdPlantPart.nextDay(self)
            self.checkIfHasAbscissed()
        except Exception, e:
            usupport.messageForExceptionType(e, "PdLeaf.nextDay")
    
    def traverseActivity(self, mode, traverserProxy):
        upart.PdPlantPart.traverseActivity(self, mode, traverserProxy)
        traverser = traverserProxy
        if traverser == None:
            return
        if self.hasFallenOff and (mode != utravers.kActivityStream) and (mode != utravers.kActivityFree):
            return
        try:
            if mode == utravers.kActivityNone:
                pass
            elif mode == utravers.kActivityNextDay:
                self.nextDay()
            elif mode == utravers.kActivityDemandVegetative:
                if self.age > self.plant.pLeaf.maxDaysToGrow:
                    self.biomassDemand_pctMPB = 0.0
                    return
                fractionOfMaxAge_frn = umath.safedivExcept(self.age + 1, self.plant.pLeaf.maxDaysToGrow, 0.0)
                propFullSizeWanted = umath.max(0.0, umath.min(1.0, umath.scurve(fractionOfMaxAge_frn, self.plant.pLeaf.sCurveParams.c1, self.plant.pLeaf.sCurveParams.c2)))
                self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, propFullSizeWanted * self.plant.pLeaf.optimalBiomass_pctMPB, self.plant.pLeaf.minDaysToGrow)
                traverser.total = traverser.total + self.biomassDemand_pctMPB
            elif mode == utravers.kActivityDemandReproductive:
                pass
            elif mode == utravers.kActivityGrowVegetative:
                if self.age > self.plant.pLeaf.maxDaysToGrow:
                    # no repro. demand
                    return
                newBiomass_pctMPB = self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + newBiomass_pctMPB
                self.propFullSize = umath.min(1.0, umath.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pLeaf.optimalBiomass_pctMPB, 0))
            elif mode == utravers.kActivityGrowReproductive:
                pass
            elif mode == utravers.kActivityStartReproduction:
                pass
            elif mode == utravers.kActivityFindPlantPartAtPosition:
                if umath.pointsAreCloseEnough(traverser.point, self.position()):
                    # no repro. growth
                    # no response 
                    traverser.foundPlantPart = self
                    traverser.finished = True
            elif mode == utravers.kActivityDraw:
                pass
            elif mode == utravers.kActivityReport:
                pass
            elif mode == utravers.kActivityStream:
                pass
            elif mode == utravers.kActivityFree:
                pass
            elif mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved:
                # phytomer will control drawing 
                #streaming will be done by internode
                # free will be called by phytomer 
                traverser.total = traverser.total + self.liveBiomass_pctMPB
            elif mode == utravers.kActivityRemoveVegetativeBiomass:
                biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
            elif mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                pass
            elif mode == utravers.kActivityRemoveReproductiveBiomass:
                pass
            elif mode == utravers.kActivityGatherStatistics:
                if self.isSeedlingLeaf:
                    # none 
                    # none 
                    self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeSeedlingLeaf)
                else:
                    self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeLeaf)
                self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllVegetative)
            elif mode == utravers.kActivityCountPlantParts:
                pass
            elif mode == utravers.kActivityFindPartForPartID:
                pass
            elif mode == utravers.kActivityCountTotalMemoryUse:
                traverser.totalMemorySize += self.instanceSize
            elif mode == utravers.kActivityCalculateBiomassForGravity:
                pass
            elif mode == utravers.kActivityCountPointsAndTrianglesFor3DExport:
                self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser)
            else :
                raise GeneralException.create("Problem: Unhandled mode in method PdLeaf.traverseActivity.")
        except Exception, e:
            # PDF PORT __ TEMPORARILY ADDED raise FOR TESTING
            raise
            usupport.messageForExceptionType(e, "PdLeaf.traverseActivity")
    
    def checkIfHasAbscissed(self):
        pass
        # if enough biomass removed (parameter), absciss leaf or leaves 
        # not doing anymore
        #if (self.fractionLive < plant.pLeaf.fractionOfLiveBiomassWhenAbscisses_frn) and (not self.hasFallenOff) then
        #  self.hasFallenOff := True;
    
    def destroy(self):
        upart.PdPlantPart.destroy(self)
    
    def isPhytomer(self):
        result = False
        return result
    
    def countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(self, traverser):
        if traverser == None:
            return
        if self.hasFallenOff:
            return
        if self.propFullSize <= 0:
            return
        if self.isSeedlingLeaf:
            if self.plant.pSeedlingLeaf.leafTdoParams.scaleAtFullSize > 0:
                # seedling leaf
                traverser.total3DExportPointsIn3DObjects += self.plant.pSeedlingLeaf.leafTdoParams.object3D.pointsInUse
                traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pSeedlingLeaf.leafTdoParams.object3D.triangles)
                self.addExportMaterial(traverser, u3dexport.kExportPartSeedlingLeaf, -1)
            # not seedling leaf
        else:
            if self.plant.pLeaf.leafTdoParams.scaleAtFullSize > 0:
                # leaf (considering compound leaf)
                traverser.total3DExportPointsIn3DObjects += self.plant.pLeaf.leafTdoParams.object3D.pointsInUse * self.plant.pLeaf.compoundNumLeaflets
                traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pLeaf.leafTdoParams.object3D.triangles) * self.plant.pLeaf.compoundNumLeaflets
                self.addExportMaterial(traverser, u3dexport.kExportPartLeaf, -1)
            if self.plant.pLeaf.stipuleTdoParams.scaleAtFullSize > 0:
                # stipule
                traverser.total3DExportPointsIn3DObjects += self.plant.pLeaf.stipuleTdoParams.object3D.pointsInUse
                traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pLeaf.stipuleTdoParams.object3D.triangles)
                self.addExportMaterial(traverser, u3dexport.kExportPartLeafStipule, -1)
        if self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm > 0:
            # petiole
            traverser.total3DExportStemSegments += 1
            if self.isSeedlingLeaf:
                self.addExportMaterial(traverser, u3dexport.kExportPartFirstPetiole, -1)
            else:
                self.addExportMaterial(traverser, u3dexport.kExportPartPetiole, -1)
            if self.plant.pLeaf.compoundNumLeaflets > 1:
                # petiolets + compound leaf internodes
                traverser.total3DExportStemSegments += self.plant.pLeaf.compoundNumLeaflets * 2
    
    def tdoToSortLinesWith(self):
        result = None
        if self.plant == None:
            return result
        if self.isSeedlingLeaf:
            result = self.plant.pSeedlingLeaf.leafTdoParams.object3D
        else:
            result = self.plant.pLeaf.leafTdoParams.object3D
        return result
    
    def drawWithDirection(self, direction):
        turtle = self.plant.turtle
        if (turtle == None):
            return
        self.boundsRect = Rect(0, 0, 0, 0)
        if self.hasFallenOff:
            return
        turtle.push()
        self.determineAmendmentAndAlsoForChildrenIfAny()
        if self.hiddenByAmendment():
            # amendment rotations handled in drawStemSegment for petiole
            turtle.pop()
            return
        try:
            if self.plant.needToRecalculateColors:
                self.calculateColors()
            self.plant.turtle.push()
            if (direction == uplant.kDirectionRight):
                turtle.rotateX(128)
            length = self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * self.propFullSize
            if (self.isSeedlingLeaf):
                length = length / 2
            width = self.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * self.propFullSize
            angle = self.angleWithSway(self.plant.pLeaf.petioleAngle)
            turtle.ifExporting_startNestedGroupOfPlantParts("leaf, petiole and stipule", "LeafPetiole", u3dexport.kNestingTypeLeafAndPetiole)
            if self.isSeedlingLeaf:
                self.drawStemSegment(length, width, angle, 0, self.plant.pLeaf.petioleColor, self.plant.pLeaf.petioleTaperIndex, u3dexport.kExportPartPetiole, upart.kUseAmendment)
                scale = (self.propFullSize * (self.plant.pSeedlingLeaf.leafTdoParams.scaleAtFullSize / 100.0)) * 1.0
                self.DrawLeafOrLeaflet(scale)
            else:
                if (self.plant.pLeaf.stipuleTdoParams.scaleAtFullSize > 0):
                    self.drawStipule()
                if (self.plant.pLeaf.compoundNumLeaflets <= 1) or self.plant.turtle.drawOptions.simpleLeavesOnly:
                    self.drawStemSegment(length, width, angle, 0, self.plant.pLeaf.petioleColor, self.plant.pLeaf.petioleTaperIndex, u3dexport.kExportPartPetiole, upart.kUseAmendment)
                    scale = self.propFullSize * self.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0
                    self.DrawLeafOrLeaflet(scale)
                else:
                    self.drawStemSegment(length, width, angle, 0, self.plant.pLeaf.petioleColor, upart.kDontTaper, u3dexport.kExportPartPetiole, upart.kUseAmendment)
                    turtle.ifExporting_startNestedGroupOfPlantParts("compound leaf", "CompoundLeaf", u3dexport.kNestingTypeCompoundLeaf)
                    if (self.plant.pLeaf.compoundPinnateOrPalmate == uplant.kCompoundLeafPinnate):
                        self.drawCompoundLeafPinnate()
                    else:
                        self.drawCompoundLeafPalmate()
                    turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeCompoundLeaf)
            turtle.pop()
            turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeLeafAndPetiole)
            turtle.pop()
        except Exception, e:
            # PDF PORT ADDED FOR TESTING
            raise
            usupport.messageForExceptionType(e, "PdLeaf.drawWithDirection")
    
    def wiltLeaf(self):
        if (self.plant.turtle == None):
            #  var
            #    angle: integer; 
            return
        # angle := round(abs(plant.turtle.angleX + 32) * plant.pGeneral.wiltingPercent / 100.0);
        #  if plant.turtle.angleX > -32 then
        #    angle := -angle;
        #  plant.turtle.rotateX(angle); 
    
    def drawStipule(self):
        turtle = self.plant.turtle
        if (turtle == None):
            return
        if self.isSeedlingLeaf:
            return
        turtle.push()
        turtle.rotateX(self.angleWithSway(self.plant.pLeaf.stipuleTdoParams.xRotationBeforeDraw))
        turtle.rotateY(self.angleWithSway(self.plant.pLeaf.stipuleTdoParams.yRotationBeforeDraw))
        turtle.rotateZ(self.angleWithSway(self.plant.pLeaf.stipuleTdoParams.zRotationBeforeDraw))
        scale = (self.propFullSize * (self.plant.pLeaf.stipuleTdoParams.scaleAtFullSize / 100.0)) * 1.0
        if self.plant.pLeaf.stipuleTdoParams.repetitions > 1:
            turnPortion = 256 / self.plant.pLeaf.stipuleTdoParams.repetitions
            leftOverDegrees = 256 - turnPortion * self.plant.pLeaf.stipuleTdoParams.repetitions
            if leftOverDegrees > 0:
                addition = leftOverDegrees / self.plant.pLeaf.stipuleTdoParams.repetitions
            else:
                addition = 0
            carryOver = 0
            for i in range(0, self.plant.pLeaf.stipuleTdoParams.repetitions):
                addThisTime = trunc(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                turtle.rotateY(turnPortion + addThisTime)
                if self.plant.pLeaf.stipuleTdoParams.object3D != None:
                    self.draw3DObject(self.plant.pLeaf.stipuleTdoParams.object3D, scale, self.plant.pLeaf.stipuleTdoParams.faceColor, self.plant.pLeaf.stipuleTdoParams.backfaceColor, u3dexport.kExportPartLeafStipule)
        elif self.plant.pLeaf.stipuleTdoParams.object3D != None:
            self.draw3DObject(self.plant.pLeaf.stipuleTdoParams.object3D, scale, self.plant.pLeaf.stipuleTdoParams.faceColor, self.plant.pLeaf.stipuleTdoParams.backfaceColor, u3dexport.kExportPartLeafStipule)
        turtle.pop()
    
    def DrawLeafOrLeaflet(self, aScale):
        #Draw leaf only. If seedling leaf (on first phytomer), draw seedling leaf 3D object and colors instead.
        #    Wilt leaf according to water stress and age.
        turtle = self.plant.turtle
        if (turtle == None):
            return
        if self.isSeedlingLeaf:
            turtle.setLineWidth(1.0)
            useFaceColor = self.plant.pSeedlingLeaf.leafTdoParams.faceColor
            useBackfaceColor = self.plant.pSeedlingLeaf.leafTdoParams.backfaceColor
        else:
            turtle.setLineWidth(1.0)
            useFaceColor = self.plant.pLeaf.leafTdoParams.faceColor
            useBackfaceColor = self.plant.pLeaf.leafTdoParams.backfaceColor
        if self.isSeedlingLeaf:
            #this aligns the 3D object as stored in the file to the way it should draw on the plant
            # turtle.RotateX(64)  // flip over; in 3D designer you design the leaf from the underside
            #rotateAngle := self.angleWithSway(plant.pLeaf.object3DXRotationBeforeDraw * 256 / 360);
            #turtle.rotateX(rotateAngle);
            # no longer doing this because default X rotation is 90 degrees
            turtle.rotateX(self.angleWithSway(self.plant.pSeedlingLeaf.leafTdoParams.xRotationBeforeDraw))
            turtle.rotateY(self.angleWithSway(self.plant.pSeedlingLeaf.leafTdoParams.yRotationBeforeDraw))
            turtle.rotateZ(self.angleWithSway(self.plant.pSeedlingLeaf.leafTdoParams.zRotationBeforeDraw))
        else:
            turtle.rotateX(self.angleWithSway(self.plant.pLeaf.leafTdoParams.xRotationBeforeDraw))
            turtle.rotateY(self.angleWithSway(self.plant.pLeaf.leafTdoParams.yRotationBeforeDraw))
            turtle.rotateZ(self.angleWithSway(self.plant.pLeaf.leafTdoParams.zRotationBeforeDraw))
        #pull leaf up to plane of petiole (is perpendicular)
        turtle.rotateZ(-64)
        self.wiltLeaf()
        if self.isSeedlingLeaf:
            tdo = self.plant.pSeedlingLeaf.leafTdoParams.object3D
        else:
            tdo = self.plant.pLeaf.leafTdoParams.object3D
        if tdo != None:
            self.draw3DObject(tdo, aScale, useFaceColor, useBackfaceColor, u3dexport.kExportPartLeaf)
    
    def drawCompoundLeafPinnate(self):
        #Draw compound leaf. Use recursion structure we used to use for whole plant, with no branching.
        #    Leaflets decrease in size as you move up the leaf, simulating a gradual appearance of leaflets.
        #    Note that seedling leaves are never compound.
        turtle = self.plant.turtle
        if turtle == None:
            return
        if self.plant.pLeaf.compoundNumLeaflets <= 0:
            return
        # wnats plus one in original source
        for i in range(self.plant.pLeaf.compoundNumLeaflets, 0, -1):
            if (self.plant.pLeaf.compoundPinnateLeafletArrangement == uplant.kArrangementOpposite):
                if (i != 1) and (i % 2 == 1):
                    # v2 added opposite leaflets
                    self.drawCompoundLeafInternode(i)
            elif (i != 1):
                self.drawCompoundLeafInternode(i)
            turtle.push()
            scale = self.propFullSize * self.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0
            self.DrawCompoundLeafPetioletCount(scale, i)
            self.DrawLeafOrLeaflet(scale)
            turtle.pop()
    
    def drawCompoundLeafInternode(self, count):
        #Draw internode of leaflet (portion of rachis). This is almost identical to drawing the petiole, etc,
        #   but a bit of random drift is included to make the compound leaf look more single.
        length = self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * self.propFullSize * self.plant.pLeaf.compoundRachisToPetioleRatio / 100.0
        width = self.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * self.propFullSize
        # v1.6b3
        angleZ = self.compoundLeafAngleWithSway(self.bendAngleForCompoundLeaf(count), count)
        angleY = self.compoundLeafAngleWithSway(0, count)
        self.drawStemSegment(length, width, angleZ, angleY, self.plant.pLeaf.petioleColor, upart.kDontTaper, u3dexport.kExportPartPetiole, upart.kDontUseAmendment)
    
    # v1.6b3
    def bendAngleForCompoundLeaf(self, count):
        result = 0
        if self.plant == None:
            return result
        difference = abs(self.plant.pLeaf.compoundCurveAngleAtFullSize - self.plant.pLeaf.compoundCurveAngleAtStart)
        leafletNumberEffect = 0.75 + 0.25 * umath.safedivExcept(count, self.plant.pLeaf.compoundNumLeaflets - 1, 0)
        propFullSizeThisLeaflet = umath.max(0.0, umath.min(1.0, (0.25 + 0.75 * self.propFullSize) * leafletNumberEffect))
        if self.plant.pLeaf.compoundCurveAngleAtFullSize > self.plant.pLeaf.compoundCurveAngleAtStart:
            result = self.plant.pLeaf.compoundCurveAngleAtStart + difference * propFullSizeThisLeaflet
        else:
            result = self.plant.pLeaf.compoundCurveAngleAtStart - difference * propFullSizeThisLeaflet
        return result
    
    def DrawCompoundLeafPetioletCount(self, scale, aCount):
        #Draw petiolet, which is the leaflet stem coming off the compound leaf rachis.
        length = scale * self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * self.propFullSize
        width = scale * self.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * self.propFullSize
        if (aCount == 1):
            angle = 0
        else:
            if (odd(aCount)):
                angle = 32
            else:
                angle = -32
        angle = self.compoundLeafAngleWithSway(angle, aCount)
        self.drawStemSegment(length, width, 0, angle, self.plant.pLeaf.petioleColor, self.plant.pLeaf.petioleTaperIndex, u3dexport.kExportPartPetiole, upart.kDontUseAmendment)
    
    def compoundLeafAngleWithSway(self, angle, count):
        result = angle
        if self.plant == None:
            return result
        if count < 0:
            count = 0
        count = count % kNumCompoundLeafRandomSwayIndexes
        randomNumber = self.compoundLeafRandomSwayIndexes[count]
        result = angle + ((randomNumber - 0.5) * self.plant.pGeneral.randomSway)
        return result
    
    def drawCompoundLeafPalmate(self):
        #Draw palmate compound leaf. Use recursion structure we used to use for whole plant, with no branching.
        #    In a palmate leaf, leaflets increase in size as you move toward the middle of the leaf.
        #    Note that seedling leaves are never compound.
        turtle = self.plant.turtle
        if (turtle == None):
            return
        angleOne = umath.safedivExcept(64, self.plant.pLeaf.compoundNumLeaflets, 0)
        if self.plant.pLeaf.compoundNumLeaflets > 0:
            for i in range(self.plant.pLeaf.compoundNumLeaflets, 0, -1):
                turtle.push()
                if (i == 1):
                    angle = 0
                elif (odd(i)):
                    angle = angleOne * i * -1
                else:
                    angle = angleOne * i * 1
                length = self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * self.propFullSize * self.plant.pLeaf.compoundRachisToPetioleRatio / 100.0
                width = self.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * self.propFullSize
                self.drawStemSegment(length, width, 0, angle, self.plant.pLeaf.petioleColor, self.plant.pLeaf.petioleTaperIndex, u3dexport.kExportPartPetiole, upart.kDontUseAmendment)
                scale = self.propFullSize * self.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0
                #scale := safedivExcept(scale, plant.pLeaf.compoundNumLeaflets, 0); 
                self.DrawLeafOrLeaflet(scale)
                turtle.pop()
    
    def report(self):
        upart.PdPlantPart.report(self)
        #debugPrint('leaf, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
        #DebugForm.printNested(plant.turtle.stackSize, 'leaf, age ' + IntToStr(age));
    
    def partType(self):
        result = uplant.kPartTypeLeaf
        return result
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdLeaf
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        upart.PdPlantPart.streamDataWithFiler(self, filer, cvir)
        self.sCurveParams = filer.streamBytes(self.sCurveParams, FIX_sizeof(self.sCurveParams))
        self.propFullSize = filer.streamSingle(self.propFullSize)
        self.biomassAtCreation_pctMPB = filer.streamSingle(self.biomassAtCreation_pctMPB)
        self.isSeedlingLeaf = filer.streamBoolean(self.isSeedlingLeaf)
    
