// unit Ubrstrat

from conversion_common import *;
import uclasses;
import delphi_compatability;

// const
kMutation = 0;
kWeight = 1;
kMaxBreedingSections = 30;
kFromFirstPlant = 0;
kFromSecondPlant = 1;
kFromProbabilityBasedOnWeightsForSection = 2;
kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant = 3;
kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant = 4;
kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly = 5;



class PdBreedingStrategy extends PdStreamableObject {
    public  mutationStrengths;
    public  firstPlantWeights;
    public short getNonNumericalParametersFrom;
    public boolean mutateAndBlendColorValues;
    public boolean chooseTdosRandomlyFromCurrentLibrary;
    
    public void create() {
        short i = 0;
        
        for (i = 0; i <= kMaxBreedingSections - 1; i++) {
            // defaults 
            // mutationStrengths default to zero 
            this.firstPlantWeights[i] = 50;
        }
        this.getNonNumericalParametersFrom = kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly;
        this.mutateAndBlendColorValues = true;
        this.chooseTdosRandomlyFromCurrentLibrary = true;
    }
    
    public void readFromFile(String aFileName) {
        TextFile inputFile = new TextFile();
        String inputLine = "";
        String lineType = "";
        KfStringStream stream = new KfStringStream();
        short i = 0;
        
        AssignFile(inputFile, aFileName);
        stream = null;
        try {
            Reset(inputFile);
            stream = UNRESOLVED.KfStringStream.create;
            UNRESOLVED.readln(inputFile, inputLine);
            if (UNRESOLVED.pos("STRATEGY", uppercase(inputLine)) <= 0) {
                throw new GeneralException.create("Improper format for breeding strategy file");
            }
            while (!UNRESOLVED.eof(inputFile)) {
                UNRESOLVED.readln(inputFile, inputLine);
                stream.onStringSeparator(inputLine, "=");
                lineType = stream.nextToken;
                stream.spaceSeparator;
                if (UNRESOLVED.pos("NUMERIC", uppercase(lineType)) > 0) {
                    this.getNonNumericalParametersFrom = StrToIntDef(stream.nextToken, kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly);
                } else if (UNRESOLVED.pos("MUTATION", uppercase(lineType)) > 0) {
                    for (i = 0; i <= kMaxBreedingSections - 1; i++) {
                        this.mutationStrengths[i] = StrToIntDef(stream.nextToken, 0);
                    }
                } else if (UNRESOLVED.pos("WEIGHT", uppercase(lineType)) > 0) {
                    for (i = 0; i <= kMaxBreedingSections - 1; i++) {
                        this.firstPlantWeights[i] = StrToIntDef(stream.nextToken, 50);
                    }
                } else if (UNRESOLVED.pos("COLORS", uppercase(lineType)) > 0) {
                    this.mutateAndBlendColorValues = UNRESOLVED.strToBool(stream.nextToken);
                } else if (UNRESOLVED.pos("3D OBJECTS", uppercase(lineType)) > 0) {
                    this.chooseTdosRandomlyFromCurrentLibrary = UNRESOLVED.strToBool(stream.nextToken);
                } else {
                    break;
                }
            }
        } finally {
            stream.free;
            CloseFile(inputFile);
        }
    }
    
    public void writeToFile(String aFileName) {
        TextFile outputFile = new TextFile();
        short i = 0;
        
        AssignFile(outputFile, aFileName);
        try {
            Rewrite(outputFile);
            writeln(outputFile, "[Breeding strategy]");
            write(outputFile, "Mutations=");
            for (i = 0; i <= kMaxBreedingSections - 1; i++) {
                write(outputFile, IntToStr(this.mutationStrengths[i]) + " ");
            }
            writeln(outputFile);
            write(outputFile, "Weights=");
            for (i = 0; i <= kMaxBreedingSections - 1; i++) {
                write(outputFile, IntToStr(this.firstPlantWeights[i]) + " ");
            }
            writeln(outputFile);
            writeln(outputFile, "Non-numeric=" + IntToStr(this.getNonNumericalParametersFrom));
            writeln(outputFile, "Vary colors=" + UNRESOLVED.boolToStr(this.mutateAndBlendColorValues));
            writeln(outputFile, "Vary 3D objects=" + UNRESOLVED.boolToStr(this.chooseTdosRandomlyFromCurrentLibrary));
        } finally {
            CloseFile(outputFile);
        }
    }
    
    // ------------------------------------------------------------------------- data transfer for binary copy 
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = uclasses.kPdBreedingStrategy;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        short i = 0;
        
        super.streamDataWithFiler(filer, cvir);
        //FIX unresolved WITH expression: filer
        UNRESOLVED.streamSmallint(this.getNonNumericalParametersFrom);
        UNRESOLVED.streamBoolean(this.mutateAndBlendColorValues);
        UNRESOLVED.streamBoolean(this.chooseTdosRandomlyFromCurrentLibrary);
        for (i = 0; i <= kMaxBreedingSections - 1; i++) {
            UNRESOLVED.streamSmallint(this.mutationStrengths[i]);
        }
        for (i = 0; i <= kMaxBreedingSections - 1; i++) {
            UNRESOLVED.streamSmallint(this.firstPlantWeights[i]);
        }
    }
    
}
