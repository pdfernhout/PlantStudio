unit Uclasses;

interface

uses ufiler;

const
	kTNil = 14501;
	kPdStreamableObject = 14502;
  kPdPlant = 14503;
  // kPdDayPlant = 14504;
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

function CreateStreamableObjectFromClassAndVersionInformation(
	const cvir: PdClassAndVersionInformationRecord): PdStreamableObject;

implementation

uses SysUtils;

function CreateStreamableObjectFromClassAndVersionInformation(
		const cvir: PdClassAndVersionInformationRecord): PdStreamableObject;
  begin
  case cvir.classNumber of
  	kTNil: result := nil;
  	kPdStreamableObject:
      raise Exception.create('Problem: Should not stream PdStreamableObject abstract class ' + IntToStr(cvir.classNumber));
  	else
      begin
      raise Exception.create('Problem: Unknown class ' + IntToStr(cvir.classNumber));
      result := nil;
      end;
    end;
  end;
end.
