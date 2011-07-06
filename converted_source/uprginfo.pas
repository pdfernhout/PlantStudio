unit uprginfo;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Buttons, updform;

type
  TProgramInfoForm = class(PdForm)
    Close: TButton;
    saveListAs: TButton;
    copyToClipboard: TButton;
    helpButton: TSpeedButton;
    infoList: TMemo;
    procedure FormResize(Sender: TObject);
    procedure FormCreate(Sender: TObject);           
    procedure saveListAsClick(Sender: TObject);
    procedure CloseClick(Sender: TObject);
    procedure copyToClipboardClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
    procedure saveInfoListToFile(fileName: string);
    function stringForMemoryInK(kilobytes: extended): string;
    procedure GetOSInfo;
    procedure describePlant(describeString: string; plantProxy: TObject);
  end;

implementation

uses Ubreedr, uplant, ugener, udomain, utimeser, usupport, umath, ubitmap;

{$R *.DFM}

procedure TProgramInfoForm.FormCreate(Sender: TObject);
  var
    numParams, numSections, numHints, numPlants, numPlantsInPrivateClipboard: integer;
    scale, offsetX, offsetY: single;
    memoryStatus: TMemoryStatus;
    diskSpace: longint;
    screenColorBits: integer;
    screenColors: longint;                          
    screenDC: HDC;
    i, genCount, plCount: integer;
    plant: PdPlant;
    generation: PdGeneration;
    totalMemory_K: double;
  begin
  infoList.lines.clear;
  infoList.lines.add('');
  infoList.lines.add('PlantStudio Program Information');
  infoList.lines.add(gVersionName);
  infoList.lines.add('-------------------------------------------');
  // OS info
  infoList.lines.add('');
  infoList.lines.add('Operating system');
  infoList.lines.add('-------------------------------------------');
  self.GetOSInfo;
  memoryStatus.dwLength := sizeOf(memoryStatus);
  GlobalMemoryStatus(memoryStatus);
  infoList.lines.add('Percent memory in use: ' + intToStr(memoryStatus.dwMemoryLoad));
  infoList.lines.add('Total physical memory: ' + intToStr(memoryStatus.dwTotalPhys div 1024) + ' K');
  infoList.lines.add('Available physical memory: ' + intToStr(memoryStatus.dwAvailPhys div 1024) + ' K');
  infoList.lines.add('Total paging file: ' + intToStr(memoryStatus.dwTotalPageFile div 1024) + ' K');
  infoList.lines.add('Available paging file: ' + intToStr(memoryStatus.dwAvailPageFile div 1024) + ' K');
  infoList.lines.add('Total user memory: ' + intToStr(memoryStatus.dwTotalVirtual div 1024) + ' K');
  infoList.lines.add('Available user memory: ' + intToStr(memoryStatus.dwAvailVirtual div 1024) + ' K');
  // disk info
  infoList.lines.add('');
  infoList.lines.add('Hard disk');
  infoList.lines.add('-------------------------------------------');
  diskSpace := DiskFree(0);
  infoList.lines.add('Disk space on current drive: ' + intToStr(diskSpace div (1024 * 1024)) + ' MB');
  // screen info
  infoList.lines.add('');
  infoList.lines.add('Screen');
  infoList.lines.add('-------------------------------------------');
  screenDC := GetDC(0);
  try
    screenColorBits := (GetDeviceCaps(screenDC, BITSPIXEL) * GetDeviceCaps(screenDC, PLANES));
  finally
    ReleaseDC(0, screenDC);
  end;
  if screenColorBits <> 32 then
    begin
    screenColors := 1 shl screenColorBits;
    infoList.lines.add('Colors: ' + intToStr(screenColors) + ' (' + intToStr(screenColorBits) + ' bits)');
    end
  else
    begin
    infoList.lines.add('Colors: true color (' + intToStr(screenColorBits) + ' bits)')
    end;
  infoList.lines.add('Size: ' + intToStr(Screen.width) + ' x ' + intToStr(Screen.height));
  infoList.lines.add('Resolution: ' + intToStr(Screen.pixelsPerInch) + ' pixels/inch');
  // domain info
  infoList.lines.add('');
  infoList.lines.add('Global settings');
  infoList.lines.add('-------------------------------------------');
  infoList.lines.add('Sections: ' + intToStr(domain.sectionManager.sections.count));
  infoList.lines.add('Parameters: ' + intToStr(domain.parameterManager.parameters.count));
  infoList.lines.add('Hints: ' + intToStr(domain.hintManager.hints.count));
  infoList.lines.add('Drawing scale: ' + digitValueString(domain.plantManager.plantDrawScale_PixelsPerMm));
  infoList.lines.add('Drawing offset: ' + digitValueString(domain.plantManager.plantDrawOffset_mm.x)
    + ' x ' + digitValueString(domain.plantManager.plantDrawOffset_mm.y));
  infoList.lines.add('');
  infoList.lines.add('Plants in file');
  infoList.lines.add('-------------------------------------------');
  // plant info
  infoList.lines.add('Plants in file: ' + intToStr(domain.plantManager.plants.count));
  infoList.lines.add('Plants in private clipboard: ' + intToStr(domain.plantManager.privatePlantClipboard.count));
  if domain.plantManager.plants.count > 0 then
    begin
    totalMemory_K := 0;
    infoList.lines.add('');
    for i := 0 to domain.plantManager.plants.count - 1 do
      begin
      plant := PdPlant(domain.plantManager.plants.items[i]);
      if plant = nil then continue;
      self.describePlant('Main window', plant);
      totalMemory_K := totalMemory_K + plant.totalMemoryUsed_K;
      end;
    if totalMemory_K > 0 then
      infoList.lines.add('Total memory used by plants in main window: ' + self.stringForMemoryInK(totalMemory_K));
    end;
  // breeder info
  if (BreederForm <> nil) and (BreederForm.generations.count > 0) then
    begin
    infoList.lines.add('');
    infoList.lines.add('Breeder plants');
    infoList.lines.add('-------------------------------------------');
    totalMemory_K := 0;
    for genCount := 0 to BreederForm.generations.count - 1 do
      begin
      generation := PdGeneration(BreederForm.generations.items[genCount]);
      if generation.plants.count > 0 then for plCount := 0 to generation.plants.count - 1 do
        begin
        plant := PdPlant(generation.plants.items[plCount]);
        if plant = nil then continue;
        self.describePlant('Breeder', plant);
        totalMemory_K := totalMemory_K + plant.totalMemoryUsed_K;
        end;
      end;
    if totalMemory_K > 0 then
      infoList.lines.add('Total memory used by plants in breeder: ' + self.stringForMemoryInK(totalMemory_K));
    end;
  // time series info
  if (TimeSeriesForm <> nil) and (TimeSeriesForm.plants.count > 0) then
    begin
    infoList.lines.add('');
    infoList.lines.add('Time series plants');
    infoList.lines.add('-------------------------------------------');
    totalMemory_K := 0;
    for i := 0 to TimeSeriesForm.plants.count - 1 do
      begin
      plant := PdPlant(TimeSeriesForm.plants.items[i]);
      if plant = nil then continue;
      self.describePlant('Time Series', plant);
      totalMemory_K := totalMemory_K + plant.totalMemoryUsed_K;
      end;
    if totalMemory_K > 0 then
      infoList.lines.add('Total memory used by plants in time series window: ' + self.stringForMemoryInK(totalMemory_K));
    end;
  end;

procedure TProgramInfoForm.describePlant(describeString: string; plantProxy: TObject);
  var
    plant: PdPlant;
    theRect: TRect;
    totalMemUse, baseMemUse, hangingMemUse, tdoMemUse, cacheMemUse, partsMemUse: extended;
  begin
  if plantProxy = nil then exit;
  plant := plantProxy as PdPlant;
  plant.countPlantParts;
  infoList.lines.add(describeString + ' plant: ' + plant.name);
  // memory
  totalMemUse := plant.calculateTotalMemorySize;
  baseMemUse := plant.instanceSize / 1024.0;
  hangingMemUse := plant.hangingObjectsMemoryUse_K;
  tdoMemUse := plant.tdoMemoryUse_K;
  if plant.previewCache <> nil then
    cacheMemUse := BitmapMemorySize(plant.previewCache) / 1024.0
  else
    cacheMemUse := 0;
  partsMemUse := totalMemUse - baseMemUse - hangingMemUse - tdoMemUse - cacheMemUse;
  infoList.lines.add('  total memory use ' + self.stringForMemoryInK(totalMemUse));
  infoList.lines.add('    base memory with parameters ' + self.stringForMemoryInK(baseMemUse));
  infoList.lines.add('    posing and random number generators ' + self.stringForMemoryInK(hangingMemUse));
  infoList.lines.add('    memory for 3D objects ' + self.stringForMemoryInK(tdoMemUse));
  infoList.lines.add('    memory for drawing cache ' + self.stringForMemoryInK(cacheMemUse));
  infoList.lines.add('    memory for plant parts ' + self.stringForMemoryInK(partsMemUse));
  // status
  infoList.lines.add('  age ' + intToStr(plant.age));
  infoList.lines.add('  maturity ' + intToStr(plant.pGeneral.ageAtMaturity));
  infoList.lines.add('  scale ' + digitValueString(plant.drawingScale_PixelsPerMm));
  if plant.previewCache <> nil then
    infoList.lines.add('  cache ' + intToStr(plant.previewCache.width) + 'x' + intToStr(plant.previewCache.height))
  else
    infoList.lines.add('  no cache');
  infoList.lines.add('  base ' + digitValueString(plant.basePoint_mm.x) + 'x' + digitValueString(plant.basePoint_mm.y));
  infoList.lines.add('  hidden ' + boolToStr(plant.hidden));
  infoList.lines.add('  random number seed ' + intToStr(plant.pGeneral.startingSeedForRandomNumberGenerator));
  theRect := plant.boundsRect_pixels;
  infoList.lines.add('  bounds ' + intToStr(theRect.left)
    + 'x' + intToStr(theRect.top)
    + 'x' + intToStr(theRect.right)
    + 'x' + intToStr(theRect.bottom)
    + ' (' + intToStr(rWidth(theRect))
    + 'x' + intToStr(rHeight(theRect)) + ')');
  infoList.lines.add('  parts ' + intToStr(plant.totalPlantParts));
  infoList.lines.add('');

  end;

function TProgramInfoForm.stringForMemoryInK(kilobytes: extended): string;
  begin
  if kilobytes <= 1024 then
    result := digitValueString(kilobytes) + ' K'
  else
    result := digitValueString(kilobytes / 1024.0) + ' MB';
  end;

procedure TProgramInfoForm.GetOSInfo;
var
  Platform: string;
  BuildNumber: Integer;
begin
  case Win32Platform of
    VER_PLATFORM_WIN32_WINDOWS:
      begin
        Platform := 'Windows 95';
        BuildNumber := Win32BuildNumber and $0000FFFF;
      end;
    VER_PLATFORM_WIN32_NT:
      begin
        Platform := 'Windows NT';
        BuildNumber := Win32BuildNumber;
      end;
      else
      begin
        Platform := 'Windows';
        BuildNumber := 0;
      end;
  end;
  if (Win32Platform = VER_PLATFORM_WIN32_WINDOWS) or
    (Win32Platform = VER_PLATFORM_WIN32_NT) then
  begin
    if Win32CSDVersion = '' then
      infoList.lines.add(Format('%s %d.%d (Build %d)', [Platform, Win32MajorVersion,
        Win32MinorVersion, BuildNumber]))
    else
      infoList.lines.add(Format('%s %d.%d (Build %d: %s)', [Platform, Win32MajorVersion,
        Win32MinorVersion, BuildNumber, Win32CSDVersion]));
  end
  else
    infoList.lines.add(Format('%s %d.%d', [Platform, Win32MajorVersion,
      Win32MinorVersion]));
end;

procedure TProgramInfoForm.saveListAsClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
	begin
  if infoList.lines.count <= 0 then exit;
  if not getFileSaveInfo(kFileTypeProgramInfo, kAskForFileName, 'PStudio.txt', fileInfo) then exit;
  try
    self.saveInfoListToFile(fileInfo.tempFile);
    fileInfo.writingWasSuccessful := true;
  finally
    cleanUpAfterFileSave(fileInfo);
  end;
	end;

procedure TProgramInfoForm.saveInfoListToFile(fileName: string);
  var
    i: longint;
    outputFile: TextFile;
  begin
	assignFile(outputFile, fileName);
  setDecimalSeparator; // v1.5
	rewrite(outputFile);
  try
  if infoList.lines.count > 0 then
    for i := 0 to infoList.lines.count - 1 do
      writeln(outputFile, infoList.lines[i]);
  finally
    closeFile(outputFile);
  end;
  end;

const kBetweenGap = 4;

procedure TProgramInfoForm.FormResize(Sender: TObject);
  begin
  if Application.terminated then exit;
  close.left := self.clientWidth - close.width - kBetweenGap;
  saveListAs.left := close.left;
  copyToClipboard.left := close.left;
  helpButton.left := close.left;
  with infoList do setBounds(kBetweenGap, kBetweenGap,
    close.left - kBetweenGap * 2, intMax(0, self.clientHeight - kBetweenGap * 2));
  end;

procedure TProgramInfoForm.CloseClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TProgramInfoForm.copyToClipboardClick(Sender: TObject);
  begin
  infoList.selectAll;
  infoList.copyToClipboard;
  end;

procedure TProgramInfoForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Getting_diagnostic_information');
  end;

end.


