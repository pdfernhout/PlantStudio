// unit uprginfo

from conversion_common import *;
import utimeser;
import updform;
import delphi_compatability;

// const
kBetweenGap = 4;



class TProgramInfoForm extends PdForm {
    public TButton Close;
    public TButton saveListAs;
    public TButton copyToClipboard;
    public TSpeedButton helpButton;
    public TMemo infoList;
    
    //$R *.DFM
    public void FormCreate(TObject Sender) {
        int numParams = 0;
        int numSections = 0;
        int numHints = 0;
        int numPlants = 0;
        int numPlantsInPrivateClipboard = 0;
        float scale = 0.0;
        float offsetX = 0.0;
        float offsetY = 0.0;
        TMemoryStatus memoryStatus = new TMemoryStatus();
        long diskSpace = 0;
        int screenColorBits = 0;
        long screenColors = 0;
        HDC screenDC = new HDC();
        int i = 0;
        int genCount = 0;
        int plCount = 0;
        PdPlant plant = new PdPlant();
        PdGeneration generation = new PdGeneration();
        double totalMemory_K = 0.0;
        
        this.infoList.Lines.Clear();
        this.infoList.Lines.Add("");
        this.infoList.Lines.Add("PlantStudio Program Information");
        this.infoList.Lines.Add(UNRESOLVED.gVersionName);
        this.infoList.Lines.Add("-------------------------------------------");
        // OS info
        this.infoList.Lines.Add("");
        this.infoList.Lines.Add("Operating system");
        this.infoList.Lines.Add("-------------------------------------------");
        this.GetOSInfo();
        memoryStatus.dwLength = FIX_sizeof(memoryStatus);
        UNRESOLVED.GlobalMemoryStatus(memoryStatus);
        this.infoList.Lines.Add("Percent memory in use: " + IntToStr(memoryStatus.dwMemoryLoad));
        this.infoList.Lines.Add("Total physical memory: " + IntToStr(memoryStatus.dwTotalPhys / 1024) + " K");
        this.infoList.Lines.Add("Available physical memory: " + IntToStr(memoryStatus.dwAvailPhys / 1024) + " K");
        this.infoList.Lines.Add("Total paging file: " + IntToStr(memoryStatus.dwTotalPageFile / 1024) + " K");
        this.infoList.Lines.Add("Available paging file: " + IntToStr(memoryStatus.dwAvailPageFile / 1024) + " K");
        this.infoList.Lines.Add("Total user memory: " + IntToStr(memoryStatus.dwTotalVirtual / 1024) + " K");
        this.infoList.Lines.Add("Available user memory: " + IntToStr(memoryStatus.dwAvailVirtual / 1024) + " K");
        // disk info
        this.infoList.Lines.Add("");
        this.infoList.Lines.Add("Hard disk");
        this.infoList.Lines.Add("-------------------------------------------");
        diskSpace = UNRESOLVED.DiskFree(0);
        this.infoList.Lines.Add("Disk space on current drive: " + IntToStr(diskSpace / (1024 * 1024)) + " MB");
        // screen info
        this.infoList.Lines.Add("");
        this.infoList.Lines.Add("Screen");
        this.infoList.Lines.Add("-------------------------------------------");
        screenDC = UNRESOLVED.GetDC(0);
        try {
            screenColorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES));
        } finally {
            UNRESOLVED.ReleaseDC(0, screenDC);
        }
        if (screenColorBits != 32) {
            screenColors = 1 << screenColorBits;
            this.infoList.Lines.Add("Colors: " + IntToStr(screenColors) + " (" + IntToStr(screenColorBits) + " bits)");
        } else {
            this.infoList.Lines.Add("Colors: true color (" + IntToStr(screenColorBits) + " bits)");
        }
        this.infoList.Lines.Add("Size: " + IntToStr(delphi_compatability.Screen.Width) + " x " + IntToStr(delphi_compatability.Screen.Height));
        this.infoList.Lines.Add("Resolution: " + IntToStr(delphi_compatability.Screen.PixelsPerInch) + " pixels/inch");
        // domain info
        this.infoList.Lines.Add("");
        this.infoList.Lines.Add("Global settings");
        this.infoList.Lines.Add("-------------------------------------------");
        this.infoList.Lines.Add("Sections: " + IntToStr(UNRESOLVED.domain.sectionManager.sections.count));
        this.infoList.Lines.Add("Parameters: " + IntToStr(UNRESOLVED.domain.parameterManager.parameters.count));
        this.infoList.Lines.Add("Hints: " + IntToStr(UNRESOLVED.domain.hintManager.hints.count));
        this.infoList.Lines.Add("Drawing scale: " + UNRESOLVED.digitValueString(UNRESOLVED.domain.plantManager.plantDrawScale_PixelsPerMm));
        this.infoList.Lines.Add("Drawing offset: " + UNRESOLVED.digitValueString(UNRESOLVED.domain.plantManager.plantDrawOffset_mm.x) + " x " + UNRESOLVED.digitValueString(UNRESOLVED.domain.plantManager.plantDrawOffset_mm.y));
        this.infoList.Lines.Add("");
        this.infoList.Lines.Add("Plants in file");
        this.infoList.Lines.Add("-------------------------------------------");
        // plant info
        this.infoList.Lines.Add("Plants in file: " + IntToStr(UNRESOLVED.domain.plantManager.plants.count));
        this.infoList.Lines.Add("Plants in private clipboard: " + IntToStr(UNRESOLVED.domain.plantManager.privatePlantClipboard.count));
        if (UNRESOLVED.domain.plantManager.plants.count > 0) {
            totalMemory_K = 0;
            this.infoList.Lines.Add("");
            for (i = 0; i <= UNRESOLVED.domain.plantManager.plants.count - 1; i++) {
                plant = UNRESOLVED.PdPlant(UNRESOLVED.domain.plantManager.plants.items[i]);
                if (plant == null) {
                    continue;
                }
                this.describePlant("Main window", plant);
                totalMemory_K = totalMemory_K + plant.totalMemoryUsed_K;
            }
            if (totalMemory_K > 0) {
                this.infoList.Lines.Add("Total memory used by plants in main window: " + this.stringForMemoryInK(totalMemory_K));
            }
        }
        if ((UNRESOLVED.BreederForm != null) && (UNRESOLVED.BreederForm.generations.count > 0)) {
            // breeder info
            this.infoList.Lines.Add("");
            this.infoList.Lines.Add("Breeder plants");
            this.infoList.Lines.Add("-------------------------------------------");
            totalMemory_K = 0;
            for (genCount = 0; genCount <= UNRESOLVED.BreederForm.generations.count - 1; genCount++) {
                generation = UNRESOLVED.PdGeneration(UNRESOLVED.BreederForm.generations.items[genCount]);
                if (generation.plants.count > 0) {
                    for (plCount = 0; plCount <= generation.plants.count - 1; plCount++) {
                        plant = UNRESOLVED.PdPlant(generation.plants.items[plCount]);
                        if (plant == null) {
                            continue;
                        }
                        this.describePlant("Breeder", plant);
                        totalMemory_K = totalMemory_K + plant.totalMemoryUsed_K;
                    }
                }
            }
            if (totalMemory_K > 0) {
                this.infoList.Lines.Add("Total memory used by plants in breeder: " + this.stringForMemoryInK(totalMemory_K));
            }
        }
        if ((utimeser.TimeSeriesForm != null) && (utimeser.TimeSeriesForm.plants.count > 0)) {
            // time series info
            this.infoList.Lines.Add("");
            this.infoList.Lines.Add("Time series plants");
            this.infoList.Lines.Add("-------------------------------------------");
            totalMemory_K = 0;
            for (i = 0; i <= utimeser.TimeSeriesForm.plants.count - 1; i++) {
                plant = UNRESOLVED.PdPlant(utimeser.TimeSeriesForm.plants.items[i]);
                if (plant == null) {
                    continue;
                }
                this.describePlant("Time Series", plant);
                totalMemory_K = totalMemory_K + plant.totalMemoryUsed_K;
            }
            if (totalMemory_K > 0) {
                this.infoList.Lines.Add("Total memory used by plants in time series window: " + this.stringForMemoryInK(totalMemory_K));
            }
        }
    }
    
    public void describePlant(String describeString, TObject plantProxy) {
        PdPlant plant = new PdPlant();
        TRect theRect = new TRect();
        double totalMemUse = 0.0;
        double baseMemUse = 0.0;
        double hangingMemUse = 0.0;
        double tdoMemUse = 0.0;
        double cacheMemUse = 0.0;
        double partsMemUse = 0.0;
        
        if (plantProxy == null) {
            return;
        }
        plant = (UNRESOLVED.PdPlant)plantProxy;
        plant.countPlantParts;
        this.infoList.Lines.Add(describeString + " plant: " + plant.name);
        // memory
        totalMemUse = plant.calculateTotalMemorySize;
        baseMemUse = plant.instanceSize / 1024.0;
        hangingMemUse = plant.hangingObjectsMemoryUse_K;
        tdoMemUse = plant.tdoMemoryUse_K;
        if (plant.previewCache != null) {
            cacheMemUse = UNRESOLVED.BitmapMemorySize(plant.previewCache) / 1024.0;
        } else {
            cacheMemUse = 0;
        }
        partsMemUse = totalMemUse - baseMemUse - hangingMemUse - tdoMemUse - cacheMemUse;
        this.infoList.Lines.Add("  total memory use " + this.stringForMemoryInK(totalMemUse));
        this.infoList.Lines.Add("    base memory with parameters " + this.stringForMemoryInK(baseMemUse));
        this.infoList.Lines.Add("    posing and random number generators " + this.stringForMemoryInK(hangingMemUse));
        this.infoList.Lines.Add("    memory for 3D objects " + this.stringForMemoryInK(tdoMemUse));
        this.infoList.Lines.Add("    memory for drawing cache " + this.stringForMemoryInK(cacheMemUse));
        this.infoList.Lines.Add("    memory for plant parts " + this.stringForMemoryInK(partsMemUse));
        // status
        this.infoList.Lines.Add("  age " + IntToStr(plant.age));
        this.infoList.Lines.Add("  maturity " + IntToStr(plant.pGeneral.ageAtMaturity));
        this.infoList.Lines.Add("  scale " + UNRESOLVED.digitValueString(plant.drawingScale_PixelsPerMm));
        if (plant.previewCache != null) {
            this.infoList.Lines.Add("  cache " + IntToStr(plant.previewCache.width) + "x" + IntToStr(plant.previewCache.height));
        } else {
            this.infoList.Lines.Add("  no cache");
        }
        this.infoList.Lines.Add("  base " + UNRESOLVED.digitValueString(plant.basePoint_mm.x) + "x" + UNRESOLVED.digitValueString(plant.basePoint_mm.y));
        this.infoList.Lines.Add("  hidden " + UNRESOLVED.boolToStr(plant.hidden));
        this.infoList.Lines.Add("  random number seed " + IntToStr(plant.pGeneral.startingSeedForRandomNumberGenerator));
        theRect = plant.boundsRect_pixels;
        this.infoList.Lines.Add("  bounds " + IntToStr(theRect.Left) + "x" + IntToStr(theRect.Top) + "x" + IntToStr(theRect.Right) + "x" + IntToStr(theRect.Bottom) + " (" + IntToStr(UNRESOLVED.rWidth(theRect)) + "x" + IntToStr(UNRESOLVED.rHeight(theRect)) + ")");
        this.infoList.Lines.Add("  parts " + IntToStr(plant.totalPlantParts));
        this.infoList.Lines.Add("");
    }
    
    public String stringForMemoryInK(double kilobytes) {
        result = "";
        if (kilobytes <= 1024) {
            result = UNRESOLVED.digitValueString(kilobytes) + " K";
        } else {
            result = UNRESOLVED.digitValueString(kilobytes / 1024.0) + " MB";
        }
        return result;
    }
    
    public void GetOSInfo() {
        String Platform = "";
        int BuildNumber = 0;
        
        switch (UNRESOLVED.Win32Platform) {
            case UNRESOLVED.VER_PLATFORM_WIN32_WINDOWS:
                Platform = "Windows 95";
                BuildNumber = UNRESOLVED.Win32BuildNumber && 0x0000FFFF;
                break;
            case UNRESOLVED.VER_PLATFORM_WIN32_NT:
                Platform = "Windows NT";
                BuildNumber = UNRESOLVED.Win32BuildNumber;
                break;
            default:
                Platform = "Windows";
                BuildNumber = 0;
                break;
        if ((UNRESOLVED.Win32Platform == UNRESOLVED.VER_PLATFORM_WIN32_WINDOWS) || (UNRESOLVED.Win32Platform == UNRESOLVED.VER_PLATFORM_WIN32_NT)) {
            if (UNRESOLVED.Win32CSDVersion == "") {
                this.infoList.Lines.Add(UNRESOLVED.Format("%s %d.%d (Build %d)", {Platform, UNRESOLVED.Win32MajorVersion, UNRESOLVED.Win32MinorVersion, BuildNumber, }));
            } else {
                this.infoList.Lines.Add(UNRESOLVED.Format("%s %d.%d (Build %d: %s)", {Platform, UNRESOLVED.Win32MajorVersion, UNRESOLVED.Win32MinorVersion, BuildNumber, UNRESOLVED.Win32CSDVersion, }));
            }
        } else {
            this.infoList.Lines.Add(UNRESOLVED.Format("%s %d.%d", {Platform, UNRESOLVED.Win32MajorVersion, UNRESOLVED.Win32MinorVersion, }));
        }
    }
    
    public void saveListAsClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        
        if (this.infoList.Lines.Count <= 0) {
            return;
        }
        if (!UNRESOLVED.getFileSaveInfo(UNRESOLVED.kFileTypeProgramInfo, UNRESOLVED.kAskForFileName, "PStudio.txt", fileInfo)) {
            return;
        }
        try {
            this.saveInfoListToFile(fileInfo.tempFile);
            fileInfo.writingWasSuccessful = true;
        } finally {
            UNRESOLVED.cleanUpAfterFileSave(fileInfo);
        }
    }
    
    public void saveInfoListToFile(String fileName) {
        long i = 0;
        TextFile outputFile = new TextFile();
        
        AssignFile(outputFile, fileName);
        // v1.5
        UNRESOLVED.setDecimalSeparator;
        Rewrite(outputFile);
        try {
            if (this.infoList.Lines.Count > 0) {
                for (i = 0; i <= this.infoList.Lines.Count - 1; i++) {
                    writeln(outputFile, this.infoList.Lines[i]);
                }
            }
        } finally {
            CloseFile(outputFile);
        }
    }
    
    public void FormResize(TObject Sender) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        this.Close.Left = this.ClientWidth - this.Close.Width - kBetweenGap;
        this.saveListAs.Left = this.Close.Left;
        this.copyToClipboard.Left = this.Close.Left;
        this.helpButton.Left = this.Close.Left;
        this.infoList.SetBounds(kBetweenGap, kBetweenGap, this.Close.Left - kBetweenGap * 2, UNRESOLVED.intMax(0, this.ClientHeight - kBetweenGap * 2));
    }
    
    public void CloseClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    public void copyToClipboardClick(TObject Sender) {
        this.infoList.SelectAll();
        this.infoList.CopyToClipboard();
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Getting_diagnostic_information");
    }
    
}
