unit Ugener;

interface

uses Classes,
  uplant, ucollect;

type
  PdGeneration = class
    public
    firstParent, secondParent: PdPlant;
    selectedPlants: TList;
    plants: TListCollection;
    constructor create;
    constructor createWithParents(parentOne, parentTwo: PdPlant; fractionOfMaxAge: single);
    destructor destroy; override;
    procedure breedFromParents(aFirstParent, aSecondParent: PdPlant; fractionOfMaxAge: single);
    procedure selectPlant(aPlant: PdPlant; shift: boolean);
    procedure deselectAllPlants;
    function firstSelectedPlant: PdPlant;
    function secondSelectedPlant: PdPlant;
    function plantForIndex(index: smallint): PdPlant;
    procedure replacePlant(oldPlant, newPlant: PdPlant);
    procedure setLocalOptionsToDomainOptions(var localOptions: BreedingAndTimeSeriesOptionsStructure);
    end;

implementation

uses SysUtils, Dialogs, 
  udomain, umath, utdo, usupport;

{ --------------------------------------------------------------------------------- PdGeneration }
constructor PdGeneration.create;
  begin
  inherited create;
  plants := TListCollection.create;
  selectedPlants := TList.create;
  end;

destructor PdGeneration.destroy;
  begin
  plants.free;
  plants := nil;
  selectedPlants.free;
  selectedPlants := nil;
  inherited destroy;
  end;

constructor PdGeneration.createWithParents(parentOne, parentTwo: PdPlant; fractionOfMaxAge: single);
  var
    newPlant: PdPlant;
  begin
  { note: this is only used right now in the PdBreedFromParentsCommand command, so some things might not
    fit other situations. if you need to use it somewhere else, check that you want to do everything that
    is done here. }
  self.create;
  if parentOne <> nil then
    begin
    newPlant := PdPlant.create;
    if newPlant = nil then exit;
    parentOne.copyTo(newPlant);
    newPlant.removeAllAmendments; // v2.0
    newPlant.setAge(round(newPlant.pGeneral.ageAtMaturity * fractionOfMaxAge));
    plants.add(newPlant);
    firstParent := newPlant;
    { only select parent if this is being done from the breeder and you have the parents already }
    if plants.indexOf(parentOne) >= 0 then
      selectedPlants.add(firstParent);
    end;
  if parentTwo <> nil then
    begin
    newPlant := PdPlant.create;
    if newPlant = nil then exit;
    parentTwo.copyTo(newPlant);
    newPlant.removeAllAmendments; // v2.0
    newPlant.setAge(round(newPlant.pGeneral.ageAtMaturity * fractionOfMaxAge));
    plants.add(newPlant);
    secondParent := newPlant;
    { only select parent if this is being done from the breeder and you have the parents already }
    if plants.indexOf(parentTwo) >= 0 then
      selectedPlants.add(secondParent);
    end;
  end;

procedure PdGeneration.selectPlant(aPlant: PdPlant; shift: boolean);
  begin
  if shift then
    selectedPlants.add(aPlant)
  else
    begin
    selectedPlants.clear;
    selectedPlants.add(aPlant);
    end;
  end;

procedure PdGeneration.deselectAllPlants;
  begin
  selectedPlants.clear;
  end;

function PdGeneration.firstSelectedPlant: PdPlant;
  begin
  result := nil;
  if selectedPlants.count > 0 then
    result := PdPlant(selectedPlants.items[0]);
  end;

function PdGeneration.secondSelectedPlant: PdPlant;
  begin
  result := nil;
  if selectedPlants.count > 1 then
    result := PdPlant(selectedPlants.items[1]);
  end;

procedure PdGeneration.breedFromParents(aFirstParent, aSecondParent: PdPlant; fractionOfMaxAge: single);
  var
    newPlant: PdPlant;
    i, newAge: smallint;
    fileNameWithPath: string;
    newTdo: KfObject3D;
    inputFile: TextFile;
    tdos: TListCollection;
    localOptions: BreedingAndTimeSeriesOptionsStructure;
  begin
  firstParent := aFirstParent;
  if firstParent = nil then exit;
  if domain = nil then exit;
  secondParent := aSecondParent;
  plants.clear;
  selectedPlants.clear;
  tdos := nil;
  if (domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary)
    and (not domain.checkForExistingDefaultTdoLibrary) then
    messageDlg('Because you didn''t choose a 3D object library, the breeder won''t be able' + chr(13)
      + 'to randomly choose 3D objects for your breeding offspring.' + chr(13) + chr(13)
      + 'You can choose a library later by choosing Custom from the Variation menu' + chr(13)
      + 'and choosing a 3D object library there.',
      mtWarning, [mbOk], 0);
  try
    if domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary then
      begin
      tdos := TListCollection.create;
      fileNameWithPath := domain.defaultTdoLibraryFileName;
      if not fileExists(fileNameWithPath) then
        domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary := false
      else
        begin
        { cfk note: is it really ok to read the whole tdo file each time? }
        assignFile(inputFile, fileNameWithPath);
        try
          setDecimalSeparator; // v1.5
          reset(inputFile);
          while not eof(inputFile) do
            begin
            newTdo := KfObject3D.create;
            newTdo.readFromFileStream(inputFile, kInTdoLibrary);
            tdos.add(newTdo);
            end;
        finally
          closeFile(inputFile);
        end;
        end;
      end;
    for i := 0 to domain.breedingAndTimeSeriesOptions.plantsPerGeneration - 1 do
      begin
      newPlant := PdPlant.create;
      plants.add(newPlant);
      newPlant.reset;
      if domain.breedingAndTimeSeriesOptions.variationType <> kBreederVariationNoNumeric then
        newPlant.randomize;
      self.setLocalOptionsToDomainOptions(localOptions);
      newPlant.useBreedingOptionsAndPlantsToSetParameters(localOptions, firstParent, secondParent, tdos);
      newAge := round(newPlant.pGeneral.ageAtMaturity * fractionOfMaxAge);
      newPlant.setAge(intMin(newAge, newPlant.pGeneral.ageAtMaturity));
      // v2.0 plants take rotation angles from first parent
      newPlant.xRotation := firstParent.xRotation;
      newPlant.yRotation := firstParent.yRotation;
      newPlant.zRotation := firstParent.zRotation;   
      end;
  finally
    tdos.free;
  end;
  end;

procedure PdGeneration.setLocalOptionsToDomainOptions(var localOptions: BreedingAndTimeSeriesOptionsStructure);
  var i: smallint;
  begin
  with localOptions do
    begin
    // defaults
    for i := 0 to kMaxBreedingSections do firstPlantWeights[i] := 50;
    getNonNumericalParametersFrom := kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly;
    // copy (done separate from low/med/custom) v2.0
    mutateAndBlendColorValues := domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues;
    chooseTdosRandomlyFromCurrentLibrary := domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary;
    case domain.breedingAndTimeSeriesOptions.variationType of
      kBreederVariationLow:
        begin
        for i := 0 to kMaxBreedingSections do mutationStrengths[i] := kLowMutation;
        end;
      kBreederVariationMedium:
        begin
        for i := 0 to kMaxBreedingSections do mutationStrengths[i] := kMediumMutation;
        end;
      kBreederVariationHigh:
        begin
        for i := 0 to kMaxBreedingSections do mutationStrengths[i] := kHighMutation;
        end;
      kBreederVariationCustom:
        begin
        localOptions := domain.breedingAndTimeSeriesOptions;
        end;
      kBreederVariationNoNumeric:
        begin
        for i := 0 to kMaxBreedingSections do mutationStrengths[i] := kNoMutation;
        end;
      end;
    end;
  end;

function PdGeneration.plantForIndex(index: smallint): PdPlant;
  begin
  result := nil;
  if index < 0 then exit;
  if index > plants.count - 1 then exit;
  if plants.items[index] = nil then exit;
  result := PdPlant(plants.items[index]);
  end;

procedure PdGeneration.replacePlant(oldPlant, newPlant: PdPlant);
  var
    oldPlantIndex: smallint;
  begin
  { no freeing should be going on here }
  oldPlantIndex := plants.indexOf(oldPlant);
  plants.remove(oldPlant);
  if oldPlantIndex >= 0 then
    plants.insert(oldPlantIndex, newPlant)
  else
    plants.add(newPlant);
  newPlant.previewCacheUpToDate := false;
  { do the same for the selectedPlants list }
  oldPlantIndex := selectedPlants.indexOf(oldPlant);
  if oldPlantIndex >= 0 then
    begin
    selectedPlants.remove(oldPlant);
    selectedPlants.insert(oldPlantIndex, newPlant);
    end;
  end;

end.
 