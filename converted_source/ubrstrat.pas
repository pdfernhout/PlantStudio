unit Ubrstrat;

interface

uses ufiler;

const
  kMutation = 0; kWeight = 1;
  kMaxBreedingSections = 30;
  kFromFirstPlant = 0;
  kFromSecondPlant = 1;
  kFromProbabilityBasedOnWeightsForSection = 2;
  kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant = 3;
  kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant = 4;
  kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly = 5;

type

PdBreedingStrategy = class(PdStreamableObject)
  public
  mutationStrengths: array[0..kMaxBreedingSections] of smallint;
  firstPlantWeights: array[0..kMaxBreedingSections] of smallint;
  getNonNumericalParametersFrom: smallint;
  mutateAndBlendColorValues: boolean;
  chooseTdosRandomlyFromCurrentLibrary: boolean;
  constructor create; override;
  procedure readFromFile(aFileName: string);
  procedure writeToFile(aFileName: string);
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  end;

implementation

uses SysUtils,
  usstream, uclasses, usupport;

constructor PdBreedingStrategy.create;
  var
    i: smallint;
  begin
  { defaults }
  { mutationStrengths default to zero }
  for i := 0 to kMaxBreedingSections - 1 do
    firstPlantWeights[i] := 50;
  getNonNumericalParametersFrom := kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly;
  mutateAndBlendColorValues := true;
  chooseTdosRandomlyFromCurrentLibrary := true;
  end;

procedure PdBreedingStrategy.readFromFile(aFileName: string);
	var
  	inputFile: TextFile;
  	inputLine, lineType: string;
    stream: KfStringStream;
    i: smallint;
  begin
	assignFile(inputFile, aFileName);
  stream := nil;
  try
	  reset(inputFile);
    stream := KfStringStream.create;
    readln(inputFile, inputLine);
    if pos('STRATEGY', upperCase(inputLine)) <= 0 then
      raise Exception.create('Improper format for breeding strategy file');
	  while not eof(inputFile) do
      begin
      readln(inputFile, inputLine);
      stream.onStringSeparator(inputLine, '=');
      lineType := stream.nextToken;
      stream.spaceSeparator;
      if pos('NUMERIC', upperCase(lineType)) > 0 then
        getNonNumericalParametersFrom := strToIntDef(stream.nextToken,
            kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly)
      else if pos('MUTATION', upperCase(lineType)) > 0 then
        for i := 0 to kMaxBreedingSections - 1 do
          mutationStrengths[i] := strToIntDef(stream.nextToken, 0)
      else if pos('WEIGHT', upperCase(lineType)) > 0 then
        for i := 0 to kMaxBreedingSections - 1 do
          firstPlantWeights[i] := strToIntDef(stream.nextToken, 50)
      else if pos('COLORS', upperCase(lineType)) > 0 then
        mutateAndBlendColorValues := strToBool(stream.nextToken)
      else if pos('3D OBJECTS', upperCase(lineType)) > 0 then
        chooseTdosRandomlyFromCurrentLibrary := strToBool(stream.nextToken)
      else
        break;
      end;
  finally
    stream.free;
    closeFile(inputFile);
  end;
	end;

procedure PdBreedingStrategy.writeToFile(aFileName: string);
	var
  	outputFile: TextFile;
    i: smallint;
  begin
  assignFile(outputFile, aFileName);
  try
    rewrite(outputFile);
    writeln(outputFile, '[Breeding strategy]');
    write(outputFile, 'Mutations=');
    for i := 0 to kMaxBreedingSections - 1 do write(outputFile, intToStr(mutationStrengths[i]) + ' ');
    writeln(outputFile);
    write(outputFile, 'Weights=');
    for i := 0 to kMaxBreedingSections - 1 do write(outputFile, intToStr(firstPlantWeights[i]) + ' ');
    writeln(outputFile);
    writeln(outputFile, 'Non-numeric=' + intToStr(getNonNumericalParametersFrom));
    writeln(outputFile, 'Vary colors=' + boolToStr(mutateAndBlendColorValues));
    writeln(outputFile, 'Vary 3D objects=' + boolToStr(chooseTdosRandomlyFromCurrentLibrary));
  finally
    closeFile(outputFile);
  end;
  end;

{ ------------------------------------------------------------------------- data transfer for binary copy }
procedure PdBreedingStrategy.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdBreedingStrategy;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure PdBreedingStrategy.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  var
    i: smallint;
	begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
    streamSmallint(getNonNumericalParametersFrom);
    streamBoolean(mutateAndBlendColorValues);
    streamBoolean(chooseTdosRandomlyFromCurrentLibrary);
    for i := 0 to kMaxBreedingSections - 1 do
      streamSmallint(mutationStrengths[i]);
    for i := 0 to kMaxBreedingSections - 1 do
      streamSmallint(firstPlantWeights[i]);
    end;
  end;

end.
