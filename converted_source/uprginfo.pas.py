# unit uprginfo

from conversion_common import *
import ubitmap
import umath
import usupport
import utimeser
import udomain
import ugener
import uplant
import ubreedr
import updform
import delphi_compatability

# const
kBetweenGap = 4

class TProgramInfoForm(PdForm):
    def __init__(self):
        self.Close = TButton()
        self.saveListAs = TButton()
        self.copyToClipboard = TButton()
        self.helpButton = TSpeedButton()
        self.infoList = TMemo()
    
    #$R *.DFM
    def FormCreate(self, Sender):
        numParams = 0
        numSections = 0
        numHints = 0
        numPlants = 0
        numPlantsInPrivateClipboard = 0
        scale = 0.0
        offsetX = 0.0
        offsetY = 0.0
        memoryStatus = TMemoryStatus()
        diskSpace = 0L
        screenColorBits = 0
        screenColors = 0L
        screenDC = HDC()
        i = 0
        genCount = 0
        plCount = 0
        plant = PdPlant()
        generation = PdGeneration()
        totalMemory_K = 0.0
        
        self.infoList.Lines.Clear()
        self.infoList.Lines.Add("")
        self.infoList.Lines.Add("PlantStudio Program Information")
        self.infoList.Lines.Add(usupport.gVersionName)
        self.infoList.Lines.Add("-------------------------------------------")
        # OS info
        self.infoList.Lines.Add("")
        self.infoList.Lines.Add("Operating system")
        self.infoList.Lines.Add("-------------------------------------------")
        self.GetOSInfo()
        memoryStatus.dwLength = FIX_sizeof(memoryStatus)
        UNRESOLVED.GlobalMemoryStatus(memoryStatus)
        self.infoList.Lines.Add("Percent memory in use: " + IntToStr(memoryStatus.dwMemoryLoad))
        self.infoList.Lines.Add("Total physical memory: " + IntToStr(memoryStatus.dwTotalPhys / 1024) + " K")
        self.infoList.Lines.Add("Available physical memory: " + IntToStr(memoryStatus.dwAvailPhys / 1024) + " K")
        self.infoList.Lines.Add("Total paging file: " + IntToStr(memoryStatus.dwTotalPageFile / 1024) + " K")
        self.infoList.Lines.Add("Available paging file: " + IntToStr(memoryStatus.dwAvailPageFile / 1024) + " K")
        self.infoList.Lines.Add("Total user memory: " + IntToStr(memoryStatus.dwTotalVirtual / 1024) + " K")
        self.infoList.Lines.Add("Available user memory: " + IntToStr(memoryStatus.dwAvailVirtual / 1024) + " K")
        # disk info
        self.infoList.Lines.Add("")
        self.infoList.Lines.Add("Hard disk")
        self.infoList.Lines.Add("-------------------------------------------")
        diskSpace = UNRESOLVED.DiskFree(0)
        self.infoList.Lines.Add("Disk space on current drive: " + IntToStr(diskSpace / (1024 * 1024)) + " MB")
        # screen info
        self.infoList.Lines.Add("")
        self.infoList.Lines.Add("Screen")
        self.infoList.Lines.Add("-------------------------------------------")
        screenDC = UNRESOLVED.GetDC(0)
        try:
            screenColorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES))
        finally:
            UNRESOLVED.ReleaseDC(0, screenDC)
        if screenColorBits != 32:
            screenColors = 1 << screenColorBits
            self.infoList.Lines.Add("Colors: " + IntToStr(screenColors) + " (" + IntToStr(screenColorBits) + " bits)")
        else:
            self.infoList.Lines.Add("Colors: true color (" + IntToStr(screenColorBits) + " bits)")
        self.infoList.Lines.Add("Size: " + IntToStr(delphi_compatability.Screen.Width) + " x " + IntToStr(delphi_compatability.Screen.Height))
        self.infoList.Lines.Add("Resolution: " + IntToStr(delphi_compatability.Screen.PixelsPerInch) + " pixels/inch")
        # domain info
        self.infoList.Lines.Add("")
        self.infoList.Lines.Add("Global settings")
        self.infoList.Lines.Add("-------------------------------------------")
        self.infoList.Lines.Add("Sections: " + IntToStr(udomain.domain.sectionManager.sections.Count))
        self.infoList.Lines.Add("Parameters: " + IntToStr(udomain.domain.parameterManager.parameters.Count))
        self.infoList.Lines.Add("Hints: " + IntToStr(udomain.domain.hintManager.hints.Count))
        self.infoList.Lines.Add("Drawing scale: " + usupport.digitValueString(udomain.domain.plantManager.plantDrawScale_PixelsPerMm))
        self.infoList.Lines.Add("Drawing offset: " + usupport.digitValueString(udomain.domain.plantManager.plantDrawOffset_mm.x) + " x " + usupport.digitValueString(udomain.domain.plantManager.plantDrawOffset_mm.y))
        self.infoList.Lines.Add("")
        self.infoList.Lines.Add("Plants in file")
        self.infoList.Lines.Add("-------------------------------------------")
        # plant info
        self.infoList.Lines.Add("Plants in file: " + IntToStr(udomain.domain.plantManager.plants.Count))
        self.infoList.Lines.Add("Plants in private clipboard: " + IntToStr(udomain.domain.plantManager.privatePlantClipboard.Count))
        if udomain.domain.plantManager.plants.Count > 0:
            totalMemory_K = 0
            self.infoList.Lines.Add("")
            for i in range(0, udomain.domain.plantManager.plants.Count):
                plant = uplant.PdPlant(udomain.domain.plantManager.plants.Items[i])
                if plant == None:
                    continue
                self.describePlant("Main window", plant)
                totalMemory_K = totalMemory_K + plant.totalMemoryUsed_K
            if totalMemory_K > 0:
                self.infoList.Lines.Add("Total memory used by plants in main window: " + self.stringForMemoryInK(totalMemory_K))
        if (ubreedr.BreederForm != None) and (ubreedr.BreederForm.generations.Count > 0):
            # breeder info
            self.infoList.Lines.Add("")
            self.infoList.Lines.Add("Breeder plants")
            self.infoList.Lines.Add("-------------------------------------------")
            totalMemory_K = 0
            for genCount in range(0, ubreedr.BreederForm.generations.Count):
                generation = ugener.PdGeneration(ubreedr.BreederForm.generations.Items[genCount])
                if generation.plants.Count > 0:
                    for plCount in range(0, generation.plants.Count):
                        plant = uplant.PdPlant(generation.plants.Items[plCount])
                        if plant == None:
                            continue
                        self.describePlant("Breeder", plant)
                        totalMemory_K = totalMemory_K + plant.totalMemoryUsed_K
            if totalMemory_K > 0:
                self.infoList.Lines.Add("Total memory used by plants in breeder: " + self.stringForMemoryInK(totalMemory_K))
        if (utimeser.TimeSeriesForm != None) and (utimeser.TimeSeriesForm.plants.Count > 0):
            # time series info
            self.infoList.Lines.Add("")
            self.infoList.Lines.Add("Time series plants")
            self.infoList.Lines.Add("-------------------------------------------")
            totalMemory_K = 0
            for i in range(0, utimeser.TimeSeriesForm.plants.Count):
                plant = uplant.PdPlant(utimeser.TimeSeriesForm.plants.Items[i])
                if plant == None:
                    continue
                self.describePlant("Time Series", plant)
                totalMemory_K = totalMemory_K + plant.totalMemoryUsed_K
            if totalMemory_K > 0:
                self.infoList.Lines.Add("Total memory used by plants in time series window: " + self.stringForMemoryInK(totalMemory_K))
    
    def describePlant(self, describeString, plantProxy):
        plant = PdPlant()
        theRect = TRect()
        totalMemUse = 0.0
        baseMemUse = 0.0
        hangingMemUse = 0.0
        tdoMemUse = 0.0
        cacheMemUse = 0.0
        partsMemUse = 0.0
        
        if plantProxy == None:
            return
        plant = plantProxy as uplant.PdPlant
        plant.countPlantParts()
        self.infoList.Lines.Add(describeString + " plant: " + plant.name)
        # memory
        totalMemUse = plant.calculateTotalMemorySize()
        baseMemUse = plant.instanceSize / 1024.0
        hangingMemUse = plant.hangingObjectsMemoryUse_K()
        tdoMemUse = plant.tdoMemoryUse_K()
        if plant.previewCache != None:
            cacheMemUse = ubitmap.BitmapMemorySize(plant.previewCache) / 1024.0
        else:
            cacheMemUse = 0
        partsMemUse = totalMemUse - baseMemUse - hangingMemUse - tdoMemUse - cacheMemUse
        self.infoList.Lines.Add("  total memory use " + self.stringForMemoryInK(totalMemUse))
        self.infoList.Lines.Add("    base memory with parameters " + self.stringForMemoryInK(baseMemUse))
        self.infoList.Lines.Add("    posing and random number generators " + self.stringForMemoryInK(hangingMemUse))
        self.infoList.Lines.Add("    memory for 3D objects " + self.stringForMemoryInK(tdoMemUse))
        self.infoList.Lines.Add("    memory for drawing cache " + self.stringForMemoryInK(cacheMemUse))
        self.infoList.Lines.Add("    memory for plant parts " + self.stringForMemoryInK(partsMemUse))
        # status
        self.infoList.Lines.Add("  age " + IntToStr(plant.age))
        self.infoList.Lines.Add("  maturity " + IntToStr(plant.pGeneral.ageAtMaturity))
        self.infoList.Lines.Add("  scale " + usupport.digitValueString(plant.drawingScale_PixelsPerMm))
        if plant.previewCache != None:
            self.infoList.Lines.Add("  cache " + IntToStr(plant.previewCache.Width) + "x" + IntToStr(plant.previewCache.Height))
        else:
            self.infoList.Lines.Add("  no cache")
        self.infoList.Lines.Add("  base " + usupport.digitValueString(plant.basePoint_mm.x) + "x" + usupport.digitValueString(plant.basePoint_mm.y))
        self.infoList.Lines.Add("  hidden " + usupport.boolToStr(plant.hidden))
        self.infoList.Lines.Add("  random number seed " + IntToStr(plant.pGeneral.startingSeedForRandomNumberGenerator))
        theRect = plant.boundsRect_pixels()
        self.infoList.Lines.Add("  bounds " + IntToStr(theRect.Left) + "x" + IntToStr(theRect.Top) + "x" + IntToStr(theRect.Right) + "x" + IntToStr(theRect.Bottom) + " (" + IntToStr(usupport.rWidth(theRect)) + "x" + IntToStr(usupport.rHeight(theRect)) + ")")
        self.infoList.Lines.Add("  parts " + IntToStr(plant.totalPlantParts))
        self.infoList.Lines.Add("")
    
    def stringForMemoryInK(self, kilobytes):
        result = ""
        if kilobytes <= 1024:
            result = usupport.digitValueString(kilobytes) + " K"
        else:
            result = usupport.digitValueString(kilobytes / 1024.0) + " MB"
        return result
    
    def GetOSInfo(self):
        Platform = ""
        BuildNumber = 0
        
        if UNRESOLVED.Win32Platform == UNRESOLVED.VER_PLATFORM_WIN32_WINDOWS:
            Platform = "Windows 95"
            BuildNumber = UNRESOLVED.Win32BuildNumber and 0x0000FFFF
        elif UNRESOLVED.Win32Platform == UNRESOLVED.VER_PLATFORM_WIN32_NT:
            Platform = "Windows NT"
            BuildNumber = UNRESOLVED.Win32BuildNumber
        else :
            Platform = "Windows"
            BuildNumber = 0
        if (UNRESOLVED.Win32Platform == UNRESOLVED.VER_PLATFORM_WIN32_WINDOWS) or (UNRESOLVED.Win32Platform == UNRESOLVED.VER_PLATFORM_WIN32_NT):
            if UNRESOLVED.Win32CSDVersion == "":
                self.infoList.Lines.Add(UNRESOLVED.Format("%s %d.%d (Build %d)", [Platform, UNRESOLVED.Win32MajorVersion, UNRESOLVED.Win32MinorVersion, BuildNumber, ]))
            else:
                self.infoList.Lines.Add(UNRESOLVED.Format("%s %d.%d (Build %d: %s)", [Platform, UNRESOLVED.Win32MajorVersion, UNRESOLVED.Win32MinorVersion, BuildNumber, UNRESOLVED.Win32CSDVersion, ]))
        else:
            self.infoList.Lines.Add(UNRESOLVED.Format("%s %d.%d", [Platform, UNRESOLVED.Win32MajorVersion, UNRESOLVED.Win32MinorVersion, ]))
    
    def saveListAsClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        
        if self.infoList.Lines.Count <= 0:
            return
        if not usupport.getFileSaveInfo(usupport.kFileTypeProgramInfo, usupport.kAskForFileName, "PStudio.txt", fileInfo):
            return
        try:
            self.saveInfoListToFile(fileInfo.tempFile)
            fileInfo.writingWasSuccessful = true
        finally:
            usupport.cleanUpAfterFileSave(fileInfo)
    
    def saveInfoListToFile(self, fileName):
        i = 0L
        outputFile = TextFile()
        
        AssignFile(outputFile, fileName)
        # v1.5
        usupport.setDecimalSeparator()
        Rewrite(outputFile)
        try:
            if self.infoList.Lines.Count > 0:
                for i in range(0, self.infoList.Lines.Count):
                    writeln(outputFile, self.infoList.Lines[i])
        finally:
            CloseFile(outputFile)
    
    def FormResize(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        self.Close.Left = self.ClientWidth - self.Close.Width - kBetweenGap
        self.saveListAs.Left = self.Close.Left
        self.copyToClipboard.Left = self.Close.Left
        self.helpButton.Left = self.Close.Left
        self.infoList.SetBounds(kBetweenGap, kBetweenGap, self.Close.Left - kBetweenGap * 2, umath.intMax(0, self.ClientHeight - kBetweenGap * 2))
    
    def CloseClick(self, Sender):
        self.ModalResult = mrCancel
    
    def copyToClipboardClick(self, Sender):
        self.infoList.SelectAll()
        self.infoList.CopyToClipboard()
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Getting_diagnostic_information")
    
