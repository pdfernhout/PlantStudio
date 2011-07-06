// unit Uclasses

from conversion_common import *;
import delphi_compatability;

// const
kTNil = 14501;
kPdStreamableObject = 14502;
kPdPlant = 14503;
kPdPlantPart = 14505;
kPdInternode = 14506;
kPdLeaf = 14507;
kPdMeristem = 14508;
kPdInflorescence = 14509;
kPdFlowerFruit = 14510;
kKfObject3D = 14511;
kKfIndexTriangle = 14512;
KPdRandom = 14513;
kPdBreedingStrategy = 14514;
kPdPlantDrawingAmendment = 14515;


// kPdDayPlant = 14504;
public PdStreamableObject CreateStreamableObjectFromClassAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
    result = new PdStreamableObject();
    switch (cvir.classNumber) {
        case kTNil:
            result = null;
            break;
        case kPdStreamableObject:
            throw new GeneralException.create("Problem: Should not stream PdStreamableObject abstract class " + IntToStr(cvir.classNumber));
            break;
        default:
            throw new GeneralException.create("Problem: Unknown class " + IntToStr(cvir.classNumber));
            result = null;
            break;
    return result;
}


