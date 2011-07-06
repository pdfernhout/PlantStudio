unit uamendmt;

interface

uses WinTypes, StdCtrls, ufiler;

type

PdPlantDrawingAmendment = class(PdStreamableObject)
  public
  partID: longint;
  typeOfPart: string[30];
  hide: boolean;
  changeColors: boolean;
  propagateColors: boolean;
  faceColor, backfaceColor, lineColor: TColorRef;
  addRotations: boolean;
  xRotation, yRotation, zRotation: single;
  multiplyScale: boolean;
  propagateScale: boolean;
  scaleMultiplier_pct, lengthMultiplier_pct, widthMultiplier_pct: smallint;
  applyAtAge: smallint;
  constructor create; override;
  procedure readFromTextFile(var inputFile: TextFile);
  procedure readFromMemo(aMemo: TMemo; var readingMemoLine: longint);
  function setField(varName, varValue: string): boolean;
  procedure writeToTextFile(var outputFile: TextFile);
  procedure writeToMemo(aMemo: TMemo);
  function getFullName: string;
  procedure streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord); override;
  procedure classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord); override;
  end;

const
  kStartAmendmentString = 'start posing change';
  kEndAmendmentString = 'end posing change';

implementation

uses SysUtils, uplant, usupport, uclasses;

constructor PdPlantDrawingAmendment.create;
  begin
  scaleMultiplier_pct := 100;
  lengthMultiplier_pct := 100;
  widthMultiplier_pct := 100;
  xRotation := 0;
  yRotation := 0;
  zRotation := 0;
  faceColor := support_rgb(50, 200, 50);
  backfaceColor := support_rgb(20, 150, 20);
  lineColor := support_rgb(40, 100, 40);
  end;

procedure PdPlantDrawingAmendment.readFromTextFile(var inputFile: TextFile);
  var
    inputLine, varName, varValue: string;
  begin
  // plant reads start line; just continue from there
  while not eof(inputFile) do
    begin
    readln(inputFile, inputLine);
    if (trim(inputLine) = '') then continue;
    varName := stringUpTo(inputLine, '=');
    varValue := stringBeyond(inputLine, '=');
    if not setField(varName, varValue) then
      break;
    end;
  if pos(upperCase(kEndAmendmentString), upperCase(inputLine)) <= 0 then
    raise Exception.create('Problem: Expected end of posing change.');
  end;

procedure PdPlantDrawingAmendment.readFromMemo(aMemo: TMemo; var readingMemoLine: longint);
  var
    inputLine, varName, varValue: string;
  begin
  // plant reads start line; just continue from there
  while readingMemoLine <= aMemo.lines.count - 1 do
    begin
    inputLine := aMemo.lines.strings[readingMemoLine];
    if (trim(inputLine) = '') then continue;
    varName := stringUpTo(inputLine, '=');
    varValue := stringBeyond(inputLine, '=');
    if not setField(varName, varValue) then
      break;
    inc(readingMemoLine); 
    end;
  if pos(upperCase(kEndAmendmentString), upperCase(inputLine)) <= 0 then
    raise Exception.create('Problem: Expected end of posing change.');
  end;

function PdPlantDrawingAmendment.setField(varName, varValue: string): boolean;
  begin
  result := true;
    if pos('part number', varName) > 0 then
      self.partID := strToIntDef(varValue, 0) // how deal with problem?
    else if pos('part type', varName) > 0 then
      self.typeOfPart := varValue
    else if pos('hide', varName) > 0 then
      self.hide := strToBool(varValue)
    else if pos('change colors', varName) > 0 then
      // read these for possible backward compatibility later, but don't do anything with them
      result := true // self.changeColors := strToBool(varValue)
    else if pos('propagate colors up stem', varName) > 0 then
      result := true // self.propagateColors := strToBool(varValue)
    else if pos('front face color', varName) > 0 then
      result := true // self.faceColor := strToIntDef(varValue, 0)
    else if pos('back face color', varName) > 0 then
      result := true // self.backfaceColor := strToIntDef(varValue, 0)
    else if pos('line color', varName) > 0 then
      result := true // self.lineColor := strToIntDef(varValue, 0)
    else if pos('rotate', varName) > 0 then
      self.addRotations := strToBool(varValue)
    else if pos('x rotation', varName) > 0 then
      self.xRotation := strToInt(varValue) * 1.0
    else if pos('y rotation', varName) > 0 then
      self.yRotation := strToInt(varValue) * 1.0
    else if pos('z rotation', varName) > 0 then
      self.zRotation := strToInt(varValue) * 1.0
    else if pos('change scale', varName) > 0 then
      self.multiplyScale := strToBool(varValue)
    else if pos('propagate scale change up stem', varName) > 0 then
      self.propagateScale := strToBool(varValue)
    else if pos('3d object scale multiplier', varName) > 0 then
      self.scaleMultiplier_pct := strToIntDef(varValue, 100)
    else if pos('line length multiplier', varName) > 0 then
      self.lengthMultiplier_pct := strToIntDef(varValue, 100)
    else if pos('line width multiplier', varName) > 0 then
      self.widthMultiplier_pct := strToIntDef(varValue, 100)
    else if pos('apply at age', varName) > 0 then
      // read these for possible backward compatibility later, but don't do anything with them
      result := true // self.applyAtAge := strToIntDef(varValue, 0)
    else
      result := false;
  end;

procedure PdPlantDrawingAmendment.writeToTextFile(var outputFile: TextFile);
  begin
  writeln(outputFile, kStartAmendmentString);
  writeln(outputFile, '  part number =' + intToStr(partID));
  writeln(outputFile, '  part type =' + typeOfPart);
  writeln(outputFile, '  hide =' + boolToStr(hide));
  (*
  writeln(outputFile, '  change colors =' + boolToStr(changeColors));
  writeln(outputFile, '  propagate colors up stem =' + boolToStr(propagateColors));
  writeln(outputFile, '  front face color =' + intToStr(faceColor));
  writeln(outputFile, '  back face color =' + intToStr(backfaceColor));
  writeln(outputFile, '  line color =' + intToStr(lineColor));
  *)
  writeln(outputFile, '  rotate =' + boolToStr(addRotations));
  writeln(outputFile, '  x rotation =' + intToStr(round(xRotation)));
  writeln(outputFile, '  y rotation =' + intToStr(round(yRotation)));
  writeln(outputFile, '  z rotation =' + intToStr(round(zRotation)));
  writeln(outputFile, '  change scale =' + boolToStr(multiplyScale));
  writeln(outputFile, '  propagate scale change up stem =' + boolToStr(propagateScale));
  writeln(outputFile, '  3d object scale multiplier =' + intToStr(scaleMultiplier_pct));
  writeln(outputFile, '  line length multiplier =' + intToStr(lengthMultiplier_pct));
  writeln(outputFile, '  line width multiplier =' + intToStr(widthMultiplier_pct));
  (*
  writeln(outputFile, '  apply at age =' + intToStr(applyAtAge));
  *)
  writeln(outputFile, kEndAmendmentString);
  end;

procedure PdPlantDrawingAmendment.writeToMemo(aMemo: TMemo);
  begin
  aMemo.lines.add(kStartAmendmentString);
  aMemo.lines.add('  part number =' + intToStr(partID));
  aMemo.lines.add('  part type =' + typeOfPart);
  aMemo.lines.add('  hide =' + boolToStr(hide));
  (*
  aMemo.lines.add('  change colors =' + boolToStr(changeColors));
  aMemo.lines.add('  propagate colors up stem =' + boolToStr(propagateColors));
  aMemo.lines.add('  front face color =' + intToStr(faceColor));
  aMemo.lines.add('  back face color =' + intToStr(backfaceColor));
  aMemo.lines.add('  line color =' + intToStr(lineColor));
  *)
  aMemo.lines.add('  rotate =' + boolToStr(addRotations));
  aMemo.lines.add('  x rotation =' + intToStr(round(xRotation)));
  aMemo.lines.add('  y rotation =' + intToStr(round(yRotation)));
  aMemo.lines.add('  z rotation =' + intToStr(round(zRotation)));
  aMemo.lines.add('  change scale =' + boolToStr(multiplyScale));
  aMemo.lines.add('  propagate scale change up stem =' + boolToStr(propagateScale));
  aMemo.lines.add('  3d object scale multiplier =' + intToStr(scaleMultiplier_pct));
  aMemo.lines.add('  line length multiplier =' + intToStr(lengthMultiplier_pct));
  aMemo.lines.add('  line width multiplier =' + intToStr(widthMultiplier_pct));
  (*
  aMemo.lines.add('  apply at age =' + intToStr(applyAtAge));
  *)
  aMemo.lines.add(kEndAmendmentString);
  end;

function PdPlantDrawingAmendment.getFullName: string;
  begin
  result := intToStr(self.partID) + ' (' + self.typeOfPart + ')';
  if hide then result := result + ', hidden';
  if changeColors then result := result + ', colored';
  if addRotations then result := result + ', rotated';
  if multiplyScale then result := result + ', scaled';
  if applyAtAge <> 0 then
    result := result + ' at age ' + intToStr(applyAtAge);
  end;

procedure PdPlantDrawingAmendment.streamDataWithFiler(filer: PdFiler; const cvir: PdClassAndVersionInformationRecord);
	begin
  inherited streamDataWithFiler(filer, cvir);
  with filer do
    begin
    streamLongint(partID);
    streamShortString(typeOfPart);
    streamBoolean(hide);
    streamBoolean(changeColors);
    streamBoolean(propagateColors);
    streamColorRef(faceColor);
    streamColorRef(backfaceColor);
    streamColorRef(lineColor);
    streamBoolean(addRotations);
    streamSingle(xRotation);
    streamSingle(yRotation);
    streamSingle(zRotation);
    streamBoolean(multiplyScale);
    streamBoolean(propagateScale);
    streamSmallint(scaleMultiplier_pct);
    streamSmallint(lengthMultiplier_pct);
    streamSmallint(widthMultiplier_pct);
    streamSmallint(applyAtAge);
    end;
  end;

procedure PdPlantDrawingAmendment.classAndVersionInformation(var cvir: PdClassAndVersionInformationRecord);
  begin
  cvir.classNumber := kPdPlantDrawingAmendment;
  cvir.versionNumber := 0;
  cvir.additionNumber := 0;
  end;

end.
