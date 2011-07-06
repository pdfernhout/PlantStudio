unit Urandom;

interface

uses ufiler;

type
PdRandom = class(PdStreamableObject)
  public
  seed: longint;
  constructor createFromTime;
  procedure setSeed(aSeed: longint);
  procedure setSeedFromSmallint(aSeed: smallint);
  function randomSeedFromTime: longint;
  function randomSmallintSeedFromTime: smallint;
	procedure initialize(aLong: longint);
	function randomNormal(mean: single): single;
  function randomNormalWithStdDev(mean, stdDev: single): single;
	function randomNormalBoundedZeroToOne(mean: single): single;
	function randomNormalPercent(mean: single): single;
	function randomPercent: single;
	function zeroToOne: single;
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  end;

implementation

uses SysUtils,
  umath, uclasses;

constructor PdRandom.createFromTime;
	begin
  self.create;
  self.seed := self.randomSeedFromTime;
  end;

procedure PdRandom.setSeed(aSeed: longint);
  begin
  self.seed := aSeed;
  end;

procedure PdRandom.setSeedFromSmallint(aSeed: smallint);
  begin
  self.seed := aSeed; {same as setSeed but making conversion here from smallint to longint}
  end;

function PdRandom.randomSeedFromTime: longint;
	var
    Present: TDateTime;
    Year, Month, Day, Hour, Min, Sec, MSec: Word;
    longintVar: longint;
	begin
  Present:= Now;
  DecodeDate(Present, Year, Month, Day);
  DecodeTime(Present, Hour, Min, Sec, MSec);
  { was (Hour * 24 * 60 * 60 * 100) + }
  longintVar := 1;
  result := longintVar * Hour * 24 * 60 * 60 + longintVar * Min * 60 * 60 * 100
    + longintVar * Sec * 100 + longintVar * MSec;
  end;

function PdRandom.randomSmallintSeedFromTime: smallint;
	var
    Present: TDateTime;
    Year, Month, Day, Hour, Min, Sec, MSec: Word;
    smallintVar: smallint;
	begin
  Present:= Now;
  DecodeDate(Present, Year, Month, Day);
  DecodeTime(Present, Hour, Min, Sec, MSec);
  smallintVar := 1;
  result := smallintVar * Sec * 100 + smallintVar * MSec;
  { so things too close in time are not too similar, modify it randomly }
  result := round(result * self.zeroToOne);
  end;

procedure PdRandom.Initialize(aLong: longint);
  begin
  seed := aLong;
  end;

function PdRandom.RandomNormalWithStdDev(mean, stdDev: single): single;
  var
    randomNumber: single;
  	i: integer;
  begin
  randomNumber := 0.0;
  for i := 1 to 12 do
    begin
		randomNumber := randomNumber + zeroToOne;
    end;
  result := (randomNumber - 6.0) * stdDev + mean;
  end;

function PdRandom.RandomNormal(mean: single): single;
  var
    randomNumber: single;
  	i: integer;
  begin
  {return normal random number based on mean (and std dev of half mean)}
  randomNumber := 0.0;
  for i := 1 to 12 do
    begin
		randomNumber := randomNumber + zeroToOne;
    end;
  result := (randomNumber - 6.0) * (mean / 2.0) + mean;
  end;

function PdRandom.RandomNormalBoundedZeroToOne(mean: single): single;
  begin
  {return normal random number based on mean (and std dev of half mean)}
  result := max(0.0, (min(1.0, (randomNormal(mean)))));
  end;

function PdRandom.RandomNormalPercent(mean: single): single;
  begin
  {return normal random number based on mean (and std dev of half mean) bounded at 0 and 100}
  result := max(0, (min(100, round(randomNormal(mean / 100.0) * 100.0))));
  end;

function PdRandom.randomPercent: single;
  var
    k: single;
  begin
  k := round(seed / 127773);
  seed := round((16807  * (seed - (k * 127773))) - (k * 2846));
  if (seed < 0.0) then seed := seed + 2147483647;
  result := round(max(0, (min(100, (seed * 0.0000000004656612875  * 100.0)))));
  end;

function PdRandom.zeroToOne: single;
  var
    k: single;
  begin
  k := round (seed / 127773);
  seed := round((16807  * (seed - (k * 127773))) - (k * 2846));
  if (seed < 0.0) then seed := seed + 2147483647;
  result := (max(0.0, (min(1.0, (seed * 0.0000000004656612875))))) * 1.0;
  end;

procedure PdRandom.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := KPdRandom;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

procedure PdRandom.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
  begin
  filer.streamLongint(seed);
  end;

end.
