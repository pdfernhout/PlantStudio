# unit Ubrstrat

from conversion_common import *
import usupport
import uclasses
import usstream
import ufiler
import delphi_compatability

# const
kMutation = 0
kWeight = 1
kMaxBreedingSections = 30
kFromFirstPlant = 0
kFromSecondPlant = 1
kFromProbabilityBasedOnWeightsForSection = 2
kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant = 3
kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant = 4
kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly = 5

class PdBreedingStrategy(PdStreamableObject):
    def __init__(self):
        self.mutationStrengths = [0] * (range(0, kMaxBreedingSections + 1) + 1)
        self.firstPlantWeights = [0] * (range(0, kMaxBreedingSections + 1) + 1)
        self.getNonNumericalParametersFrom = 0
        self.mutateAndBlendColorValues = false
        self.chooseTdosRandomlyFromCurrentLibrary = false
    
    def create(self):
        i = 0
        
        for i in range(0, kMaxBreedingSections):
            # defaults 
            # mutationStrengths default to zero 
            self.firstPlantWeights[i] = 50
        self.getNonNumericalParametersFrom = kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly
        self.mutateAndBlendColorValues = true
        self.chooseTdosRandomlyFromCurrentLibrary = true
        return self
    
    def readFromFile(self, aFileName):
        inputFile = TextFile()
        inputLine = ""
        lineType = ""
        stream = KfStringStream()
        i = 0
        
        AssignFile(inputFile, aFileName)
        stream = None
        try:
            Reset(inputFile)
            stream = usstream.KfStringStream.create
            UNRESOLVED.readln(inputFile, inputLine)
            if UNRESOLVED.pos("STRATEGY", uppercase(inputLine)) <= 0:
                raise GeneralException.create("Improper format for breeding strategy file")
            while not UNRESOLVED.eof(inputFile):
                UNRESOLVED.readln(inputFile, inputLine)
                stream.onStringSeparator(inputLine, "=")
                lineType = stream.nextToken()
                stream.spaceSeparator()
                if UNRESOLVED.pos("NUMERIC", uppercase(lineType)) > 0:
                    self.getNonNumericalParametersFrom = StrToIntDef(stream.nextToken(), kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly)
                elif UNRESOLVED.pos("MUTATION", uppercase(lineType)) > 0:
                    for i in range(0, kMaxBreedingSections):
                        self.mutationStrengths[i] = StrToIntDef(stream.nextToken(), 0)
                elif UNRESOLVED.pos("WEIGHT", uppercase(lineType)) > 0:
                    for i in range(0, kMaxBreedingSections):
                        self.firstPlantWeights[i] = StrToIntDef(stream.nextToken(), 50)
                elif UNRESOLVED.pos("COLORS", uppercase(lineType)) > 0:
                    self.mutateAndBlendColorValues = usupport.strToBool(stream.nextToken())
                elif UNRESOLVED.pos("3D OBJECTS", uppercase(lineType)) > 0:
                    self.chooseTdosRandomlyFromCurrentLibrary = usupport.strToBool(stream.nextToken())
                else:
                    break
        finally:
            stream.free
            CloseFile(inputFile)
    
    def writeToFile(self, aFileName):
        outputFile = TextFile()
        i = 0
        
        AssignFile(outputFile, aFileName)
        try:
            Rewrite(outputFile)
            writeln(outputFile, "[Breeding strategy]")
            write(outputFile, "Mutations=")
            for i in range(0, kMaxBreedingSections):
                write(outputFile, IntToStr(self.mutationStrengths[i]) + " ")
            writeln(outputFile)
            write(outputFile, "Weights=")
            for i in range(0, kMaxBreedingSections):
                write(outputFile, IntToStr(self.firstPlantWeights[i]) + " ")
            writeln(outputFile)
            writeln(outputFile, "Non-numeric=" + IntToStr(self.getNonNumericalParametersFrom))
            writeln(outputFile, "Vary colors=" + usupport.boolToStr(self.mutateAndBlendColorValues))
            writeln(outputFile, "Vary 3D objects=" + usupport.boolToStr(self.chooseTdosRandomlyFromCurrentLibrary))
        finally:
            CloseFile(outputFile)
    
    # ------------------------------------------------------------------------- data transfer for binary copy 
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdBreedingStrategy
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        i = 0
        
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.getNonNumericalParametersFrom = filer.streamSmallint(self.getNonNumericalParametersFrom)
        self.mutateAndBlendColorValues = filer.streamBoolean(self.mutateAndBlendColorValues)
        self.chooseTdosRandomlyFromCurrentLibrary = filer.streamBoolean(self.chooseTdosRandomlyFromCurrentLibrary)
        for i in range(0, kMaxBreedingSections):
            self.mutationStrengths[i] = filer.streamSmallint(self.mutationStrengths[i])
        for i in range(0, kMaxBreedingSections):
            self.firstPlantWeights[i] = filer.streamSmallint(self.firstPlantWeights[i])
    
