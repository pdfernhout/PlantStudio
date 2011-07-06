# unit uunits
#Copyright (c) 1997 Paul D. Fernhout and Cynthia F. Kurtz All rights reserved
#http://www.gardenwithinsight.com. See the license file for details on redistribution.
#=====================================================================================
#uunits: Functions for conversion of units in whole system. There are 32 unit sets,
#and each unit set contains units that are inter-convertible. For example, the
#temperature unit set contains degrees C and degrees F. The unit set must be saved
#and given during any conversion so the function knows which code to use to convert
#the units. Numbers cannot be converted between unit sets. The file also contains
#information for displaying the units (the string to show, etc).

from conversion_common import *
import umath
import usupport
import delphi_compatability

# const
kRangeOK = 0
kRangeTooLow = 1
kRangeTooHigh = 2
kRangeBounds = 3
kRangeMustBeInteger = 4
kDefaultFloatMin = -100000000000.0
kDefaultFloatMax = 100000000000.0
kMaxUnitStringLength = 12

# const
kDimensionless = 1
kLength = 2
kObsoleteLength = 3
kAngle = 4
kTemperature = 5
kMass = 6
kObsoleteMass = 7
kArea = 8
kMassOverArea = 9
kRadiation = 10
kVolume = 11
kDepthOfWater = 12
kVelocity = 13
kPressure = 14
kDensity = 15
kNonChangingUnitHundredsOfMolesPKilogram = 16
kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter = 17
kNonChangingUnitKiloPascalPDegreeC = 18
kNonChangingUnitMegaJoulePKilogram = 19
kNonChangingUnitKilogramPKilogram = 20
kNonChangingUnitMetersPMeter = 21
kNonChangingUnitYears = 22
kNonChangingUnitDays = 23
kNonChangingUnitHours = 24
kNonChangingUnitPartsPMillion = 25
kNonChangingUnitFraction = 26
kNonChangingUnitPercent = 27
kNonChangingUnitGramsPMetricTon = 28
kNonChangingUnitCubicMetersPSecond = 29
kNonChangingUnitBoolean = 30
kConcentration = 31
kLastUnitSet = 32

# var
maxUnitStringLengths = [0] * (range(kDimensionless, kLastUnitSet + 1) + 1)

# const
kLengthFirstUnit = 1
kLengthMicrons = 1
kLengthMillimeters = 2
kLengthCentimeters = 3
kLengthMeters = 4
kLengthKilometers = 5
kLengthInches = 6
kLengthFeet = 7
kLengthYards = 8
kLengthMiles = 9
kLengthLastUnit = 10

# const
kAngleFirstUnit = 1
kAngleRadians = 1
kAngleDegrees = 2
kAngleLastUnit = 3

# const
kTemperatureFirstUnit = 1
kTemperatureDegreesC = 1
kTemperatureDegreesF = 2
kTemperatureLastUnit = 3

# const
kMassFirstUnit = 1
kMassMilligrams = 1
kMassGrams = 2
kMassKilograms = 3
kMassMetricTons = 4
kMassOunces = 5
kMassPounds = 6
kMassEnglishTons = 7
kMassLastUnit = 8

# const
kAreaFirstUnit = 1
kAreaHectares = 1
kAreaSquareMeters = 2
kAreaSquareKilometers = 3
kAreaSquareFeet = 4
kAreaSquareYards = 5
kAreaAcres = 6
kAreaSquareMiles = 7
kAreaLastUnit = 8

# const
kMassOverAreaFirstUnit = 1
kMassOverAreaKilogramsPHectare = 1
kMassOverAreaMetricTonsPHectare = 2
kMassOverAreaKilogramsPSquareMeter = 3
kMassOverAreaGramsPSquareMeter = 4
kMassOverAreaGramsPSquareCentimeter = 5
kMassOverAreaPoundsPAcre = 6
kMassOverAreaEnglishTonsPAcre = 7
kMassOverAreaPoundsPSquareYard = 8
kMassOverAreaPoundsPSquareFoot = 9
kMassOverAreaOuncesPSquareFoot = 10
kMassOverAreaLastUnit = 11

# const
kRadiationFirstUnit = 1
kRadiationMegaJoulesPSquareMeter = 1
kRadiationKilowattHoursPSquareMeter = 2
kRadiationCaloriesPerSquareMeter = 3
kRadiationLangleys = 4
kRadiationMegaJoulesPSquareFoot = 5
kRadiationKilowattHoursPSquareFoot = 6
kRadiationCaloriesPerSquareFoot = 7
kRadiationLastUnit = 8

# const
kVolumeFirstUnit = 1
kVolumeMilliliters = 1
kVolumeLiters = 2
kVolumeCubicMeters = 3
kVolumeQuarts = 4
kVolumeGallons = 5
kVolumeOunces = 6
kVolumeLastUnit = 7

# const
kDepthOfWaterFirstUnit = 1
kDepthOfWaterMillimeters = 1
kDepthOfWaterInches = 2
kDepthOfWaterLastUnit = 3

# const
kVelocityFirstUnit = 1
kVelocityMetersPSecond = 1
kVelocityMillimetersPHour = 2
kVelocityMilesPHour = 3
kVelocityFeetPSecond = 4
kVelocityInchesPHour = 5
kVelocityLastUnit = 6

# const
kPressureFirstUnit = 1
kPressurePascals = 1
kPressureKilopascals = 2
kPressureMegapascals = 3
kPressureKilogramsPSquareCentimeter = 4
kPressureAtmospheres = 5
kPressureBars = 6
kPressurePoundsPSquareInch = 7
kPressureLastUnit = 8

# const
kDensityFirstUnit = 1
kDensityGramsPCubicCentimeter = 1
kDensityKilogramsPCubicMeter = 2
kDensityMetricTonsPCubicMeter = 3
kDensityPoundsPCubicFoot = 4
kDensityPoundsPAcreFoot = 5
kDensityLastUnit = 6

# const
kConcentrationFirstUnit = 1
kConcentrationGramsPMetricTon = 1
kConcentrationGramsPKilogram = 2
kConcentrationMilligramsPMetricTon = 3
kConcentrationPoundsPEnglishTon = 4
kConcentrationOuncesPEnglishTon = 5
kConcentrationLastUnit = 6

# var
m_to_microns = 0.0
microns_to_m = 0.0
m_to_mm = 0.0
mm_to_m = 0.0
m_to_cm = 0.0
cm_to_m = 0.0
cm_to_mm = 0.0
mm_to_cm = 0.0
km_to_m = 0.0
m_to_km = 0.0
in_to_cm = 0.0
cm_to_in = 0.0
ft_to_in = 0.0
in_to_ft = 0.0
yd_to_ft = 0.0
ft_to_yd = 0.0
mi_to_ft = 0.0
ft_to_mi = 0.0
t_to_kg = 0.0
kg_to_t = 0.0
kg_to_g = 0.0
g_to_kg = 0.0
g_to_mg = 0.0
mg_to_g = 0.0
oz_to_g = 0.0
g_to_oz = 0.0
lb_to_oz = 0.0
oz_to_lb = 0.0
T_to_lb = 0.0
lb_to_T = 0.0
ha_to_m2 = 0.0
m2_to_ha = 0.0
km2_to_m2 = 0.0
m2_to_km2 = 0.0
m2_to_cm2 = 0.0
cm2_to_m2 = 0.0
m2_to_ft2 = 0.0
ft2_to_m2 = 0.0
in2_to_cm2 = 0.0
cm2_to_in2 = 0.0
yd2_to_ft2 = 0.0
ft2_to_yd2 = 0.0
ac_to_ft2 = 0.0
ft2_to_ac = 0.0
mi2_to_ac = 0.0
ac_to_mi2 = 0.0
kWh_to_MJ = 0.0
MJ_to_kWh = 0.0
MJ_to_joule = 0.0
joule_to_MJ = 0.0
cal_to_joule = 0.0
joule_to_cal = 0.0
MJPm2_to_langleys = 0.0
langleys_to_MJPm2 = 0.0
l_to_ml = 0.0
ml_to_l = 0.0
m3_to_l = 0.0
l_to_m3 = 0.0
qt_to_l = 0.0
l_to_qt = 0.0
gal_to_qt = 0.0
qt_to_gal = 0.0
qt_to_floz = 0.0
floz_to_qt = 0.0
m3_to_ft3 = 0.0
ft3_to_m3 = 0.0
acft_to_ft3 = 0.0
ft3_to_acft = 0.0
kPa_to_pa = 0.0
pa_to_kPa = 0.0
MPa_to_kPa = 0.0
kPa_to_MPa = 0.0
psi_to_pa = 0.0
pa_to_psi = 0.0
atm_to_pa = 0.0
pa_to_atm = 0.0
bars_to_pa = 0.0
pa_to_bars = 0.0
hr_to_min = 0.0
min_to_hr = 0.0
min_to_sec = 0.0
sec_to_min = 0.0
rad_to_deg = 0.0
deg_to_rad = 0.0
frn_to_pct = 0.0
pct_to_frn = 0.0

# if change any unit string to make it longer than this, update 
# unit sets  
# obsolete 
# obsolete 
#length (base unit: m) 
# note: length used to be split into small and large,
#  but these two have been combined so the user doesn't see them. 
# was inches 
# was feet 
# was yards 
# was large meters 
# was large km 
# 10 was large yards 
# 11 was large miles 
# angle (base unit: radians)
# temperature (base unit: deg C)  
# Mass (base unit: kg) (both small and large) 
# note: these two have been combined so the user doesn't see them. 
# was ounces 
# was pounds 
# was large kg 
# was large metric tons 
# 8 was large pounds 
# 9 was large english tons 
# area (base unit: m2)  
# Mass over area (base unit: kg/ha) 
# radiation (base unit: MJ/m2) 
# volume (base unit: liter) 
# depth of water (precipitation) (base unit: mm) 
# velocity (base unit: m/sec) 
# pressure (base unit: Pa)
# density (base unit: g/cm3) (also concentration) 
# concentration (base unit: g/t) 
# length 
# mass 
# area 
# energy 
# volume 
# pressure 
# other 
def setUnitConstants():
    # length 
    m_to_microns = 1000000.0
    microns_to_m = 1.0 / m_to_microns
    m_to_mm = 1000.0
    mm_to_m = 1.0 / m_to_mm
    m_to_cm = 100.0
    cm_to_m = 1.0 / m_to_cm
    cm_to_mm = 10.0
    mm_to_cm = 1.0 / cm_to_mm
    km_to_m = 1000.0
    m_to_km = 1.0 / km_to_m
    in_to_cm = 2.54
    cm_to_in = 1.0 / in_to_cm
    ft_to_in = 12.0
    in_to_ft = 1.0 / ft_to_in
    yd_to_ft = 3.0
    ft_to_yd = 1.0 / yd_to_ft
    mi_to_ft = 5280.0
    ft_to_mi = 1.0 / mi_to_ft
    # mass 
    t_to_kg = 1000.0
    kg_to_t = 1.0 / t_to_kg
    kg_to_g = 1000.0
    g_to_kg = 1.0 / kg_to_g
    g_to_mg = 1000.0
    mg_to_g = 1.0 / g_to_mg
    oz_to_g = 28.35
    g_to_oz = 1.0 / oz_to_g
    lb_to_oz = 16.0
    oz_to_lb = 1.0 / lb_to_oz
    T_to_lb = 2000.0
    lb_to_T = 1.0 / T_to_lb
    # area 
    ha_to_m2 = 10000.0
    m2_to_ha = 1.0 / ha_to_m2
    km2_to_m2 = 1000000.0
    m2_to_km2 = 1.0 / km2_to_m2
    m2_to_cm2 = 10000.0
    cm2_to_m2 = 1 / m2_to_cm2
    m2_to_ft2 = 10.7639
    ft2_to_m2 = 1.0 / m2_to_ft2
    in2_to_cm2 = 6.4516
    cm2_to_in2 = 1.0 / in2_to_cm2
    yd2_to_ft2 = 9.0
    ft2_to_yd2 = 1.0 / yd2_to_ft2
    ac_to_ft2 = 43560.0
    ft2_to_ac = 1.0 / ac_to_ft2
    mi2_to_ac = 640.0
    ac_to_mi2 = 1.0 / mi2_to_ac
    # energy 
    kWh_to_MJ = 3.6
    MJ_to_kWh = 1.0 / kWh_to_MJ
    MJ_to_joule = 1000000.0
    joule_to_MJ = 1.0 / MJ_to_joule
    cal_to_joule = 4.1868
    joule_to_cal = 1.0 / cal_to_joule
    MJPm2_to_langleys = 23.8846
    langleys_to_MJPm2 = 1.0 / MJPm2_to_langleys
    # volume 
    l_to_ml = 1000.0
    ml_to_l = 1.0 / l_to_ml
    m3_to_l = 1000.0
    l_to_m3 = 1.0 / m3_to_l
    qt_to_l = 0.946
    l_to_qt = 1.0 / qt_to_l
    gal_to_qt = 4.0
    qt_to_gal = 1.0 / gal_to_qt
    qt_to_floz = 32.0
    floz_to_qt = 1.0 / qt_to_floz
    m3_to_ft3 = 35.32
    ft3_to_m3 = 1.0 / m3_to_ft3
    acft_to_ft3 = 43560.0
    ft3_to_acft = 1.0 / acft_to_ft3
    # pressure 
    kPa_to_pa = 1000.0
    pa_to_kPa = 1.0 / kPa_to_pa
    MPa_to_kPa = 1000.0
    kPa_to_MPa = 1.0 / MPa_to_kPa
    psi_to_pa = 6894.76
    pa_to_psi = 1.0 / psi_to_pa
    atm_to_pa = 101325.0
    pa_to_atm = 1.0 / atm_to_pa
    bars_to_pa = 100000
    pa_to_bars = 1.0 / bars_to_pa
    # other 
    hr_to_min = 60.0
    min_to_hr = 1.0 / hr_to_min
    min_to_sec = 60.0
    sec_to_min = 1.0 / min_to_sec
    rad_to_deg = 57.296
    deg_to_rad = 1.0 / rad_to_deg
    frn_to_pct = 100.0
    pct_to_frn = 1.0 / frn_to_pct

def Convert(unitSet, unitFrom, unitTo, value):
    result = 0.0
    base = 0.0
    
    base = 0.0
    # default result to same value if something goes wrong 
    result = value
    if (unitFrom == unitTo) or (value == usupport.kMaxSingle) or (value == usupport.kMinSingle):
        # if no conversion, exit 
        return result
    if value == usupport.kMaxSingle:
        # special check for overflow (for bounds) to avoid exception-handling system 
        result = usupport.kMaxSingle
        return result
    if value == -usupport.kMaxSingle:
        result = -usupport.kMaxSingle
        return result
    try:
        if unitSet == kDimensionless:
            result = value
        elif unitSet == kLength:
            if unitFrom == kLengthMicrons:
                #base unit: meters
                base = value * microns_to_m
            elif unitFrom == kLengthMillimeters:
                base = value * mm_to_m
            elif unitFrom == kLengthCentimeters:
                base = value * cm_to_m
            elif unitFrom == kLengthMeters:
                base = value
            elif unitFrom == kLengthKilometers:
                base = value * km_to_m
            elif unitFrom == kLengthInches:
                base = value * in_to_cm * cm_to_m
            elif unitFrom == kLengthFeet:
                base = value * ft_to_in * in_to_cm * cm_to_m
            elif unitFrom == kLengthYards:
                base = value * yd_to_ft * ft_to_in * in_to_cm * cm_to_m
            elif unitFrom == kLengthMiles:
                base = value * mi_to_ft * ft_to_in * in_to_cm * cm_to_m
            if unitTo == kLengthMicrons:
                result = base * m_to_microns
            elif unitTo == kLengthMillimeters:
                result = base * m_to_mm
            elif unitTo == kLengthCentimeters:
                result = base * m_to_cm
            elif unitTo == kLengthMeters:
                result = base
            elif unitTo == kLengthKilometers:
                result = base * m_to_km
            elif unitTo == kLengthInches:
                result = base * m_to_cm * cm_to_in
            elif unitTo == kLengthFeet:
                result = base * m_to_cm * cm_to_in * in_to_ft
            elif unitTo == kLengthYards:
                result = base * m_to_cm * cm_to_in * in_to_ft * ft_to_yd
            elif unitTo == kLengthMiles:
                result = base * m_to_cm * cm_to_in * in_to_ft * ft_to_mi
        elif unitSet == kAngle:
            if unitFrom == kAngleRadians:
                #base unit: radians
                base = value
            elif unitFrom == kAngleDegrees:
                base = value * deg_to_rad
            if unitTo == kAngleRadians:
                result = base
            elif unitTo == kAngleDegrees:
                result = base * rad_to_deg
        elif unitSet == kTemperature:
            if unitFrom == kTemperatureDegreesC:
                #base unit: degrees C
                base = value
            elif unitFrom == kTemperatureDegreesF:
                base = (value - 32.0) / 1.8
            if unitTo == kTemperatureDegreesC:
                result = base
            elif unitTo == kTemperatureDegreesF:
                result = base * 1.8 + 32.0
        elif unitSet == kMass:
            if unitFrom == kMassMilligrams:
                #base unit: milligrams
                base = value * mg_to_g * g_to_kg
            elif unitFrom == kMassGrams:
                base = value * g_to_kg
            elif unitFrom == kMassKilograms:
                base = value
            elif unitFrom == kMassMetricTons:
                base = value * t_to_kg
            elif unitFrom == kMassOunces:
                base = value * oz_to_g * g_to_kg
            elif unitFrom == kMassPounds:
                base = value * lb_to_oz * oz_to_g * g_to_kg
            elif unitFrom == kMassEnglishTons:
                base = value * T_to_lb * lb_to_oz * oz_to_g * g_to_kg
            if unitTo == kMassMilligrams:
                result = base * kg_to_g * g_to_mg
            elif unitTo == kMassGrams:
                result = base * kg_to_g
            elif unitTo == kMassKilograms:
                result = base
            elif unitTo == kMassMetricTons:
                result = base * kg_to_t
            elif unitTo == kMassOunces:
                result = base * kg_to_g * g_to_oz
            elif unitTo == kMassPounds:
                result = base * kg_to_g * g_to_oz * oz_to_lb
            elif unitTo == kMassEnglishTons:
                result = base * kg_to_g * g_to_oz * oz_to_lb * lb_to_T
        elif unitSet == kArea:
            if unitFrom == kAreaSquareMeters:
                #base unit: square meters
                base = value
            elif unitFrom == kAreaHectares:
                base = value * ha_to_m2
            elif unitFrom == kAreaSquareKilometers:
                base = value * km2_to_m2
            elif unitFrom == kAreaSquareFeet:
                base = value * ft2_to_m2
            elif unitFrom == kAreaSquareYards:
                base = value * yd2_to_ft2 * ft2_to_m2
            elif unitFrom == kAreaAcres:
                base = value * ac_to_ft2 * ft2_to_m2
            elif unitFrom == kAreaSquareMiles:
                base = value * mi2_to_ac * ac_to_ft2 * ft2_to_m2
            if unitTo == kAreaSquareMeters:
                result = base
            elif unitTo == kAreaHectares:
                result = base * m2_to_ha
            elif unitTo == kAreaSquareKilometers:
                result = base * m2_to_km2
            elif unitTo == kAreaSquareFeet:
                result = base * m2_to_ft2
            elif unitTo == kAreaSquareYards:
                result = base * m2_to_ft2 * ft2_to_yd2
            elif unitTo == kAreaAcres:
                result = base * m2_to_ft2 * ft2_to_ac
            elif unitTo == kAreaSquareMiles:
                result = base * m2_to_ft2 * ft2_to_ac * ac_to_mi2
        elif unitSet == kMassOverArea:
            if unitFrom == kMassOverAreaKilogramsPHectare:
                #base unit: kg/ha
                base = value
            elif unitFrom == kMassOverAreaMetricTonsPHectare:
                base = value * t_to_kg
            elif unitFrom == kMassOverAreaKilogramsPSquareMeter:
                base = value / (m2_to_ha)
            elif unitFrom == kMassOverAreaGramsPSquareMeter:
                base = value * g_to_kg / (m2_to_ha)
            elif unitFrom == kMassOverAreaGramsPSquareCentimeter:
                base = value * g_to_kg / (cm2_to_m2 * m2_to_ha)
            elif unitFrom == kMassOverAreaPoundsPAcre:
                base = value * (lb_to_oz * oz_to_g * g_to_kg) / (ac_to_ft2 * ft2_to_m2 * m2_to_ha)
            elif unitFrom == kMassOverAreaEnglishTonsPAcre:
                base = value * (T_to_lb * lb_to_oz * oz_to_g * g_to_kg) / (ac_to_ft2 * ft2_to_m2 * m2_to_ha)
            elif unitFrom == kMassOverAreaPoundsPSquareYard:
                base = value * (lb_to_oz * oz_to_g * g_to_kg) / (yd2_to_ft2 * ft2_to_m2 * m2_to_ha)
            elif unitFrom == kMassOverAreaPoundsPSquareFoot:
                base = value * (lb_to_oz * oz_to_g * g_to_kg) / (ft2_to_m2 * m2_to_ha)
            elif unitFrom == kMassOverAreaOuncesPSquareFoot:
                base = value * (oz_to_g * g_to_kg) / (ft2_to_m2 * m2_to_ha)
            if unitTo == kMassOverAreaKilogramsPHectare:
                result = base
            elif unitTo == kMassOverAreaMetricTonsPHectare:
                result = base * kg_to_t
            elif unitTo == kMassOverAreaKilogramsPSquareMeter:
                result = base / (ha_to_m2)
            elif unitTo == kMassOverAreaGramsPSquareMeter:
                result = base * kg_to_g / (ha_to_m2)
            elif unitTo == kMassOverAreaGramsPSquareCentimeter:
                result = base * kg_to_g / (ha_to_m2 * m2_to_cm2)
            elif unitTo == kMassOverAreaPoundsPAcre:
                result = base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2 * ft2_to_ac)
            elif unitTo == kMassOverAreaEnglishTonsPAcre:
                result = base * (kg_to_g * g_to_oz * oz_to_lb * lb_to_T) / (ha_to_m2 * m2_to_ft2 * ft2_to_ac)
            elif unitTo == kMassOverAreaPoundsPSquareYard:
                result = base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2 * ft2_to_yd2)
            elif unitTo == kMassOverAreaPoundsPSquareFoot:
                result = base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2)
            elif unitTo == kMassOverAreaOuncesPSquareFoot:
                result = base * (kg_to_g * g_to_oz) / (ha_to_m2 * m2_to_ft2)
        elif unitSet == kRadiation:
            if unitFrom == kRadiationMegaJoulesPSquareMeter:
                #base unit: MJ/m2
                base = value
            elif unitFrom == kRadiationKilowattHoursPSquareMeter:
                base = value * kWh_to_MJ
            elif unitFrom == kRadiationCaloriesPerSquareMeter:
                base = value * cal_to_joule * joule_to_MJ
            elif unitFrom == kRadiationLangleys:
                base = value * langleys_to_MJPm2
            elif unitFrom == kRadiationMegaJoulesPSquareFoot:
                base = value / (ft2_to_m2)
            elif unitFrom == kRadiationKilowattHoursPSquareFoot:
                base = value * kWh_to_MJ / (ft2_to_m2)
            elif unitFrom == kRadiationCaloriesPerSquareFoot:
                base = value * cal_to_joule * joule_to_MJ / (ft2_to_m2)
            if unitTo == kRadiationMegaJoulesPSquareMeter:
                result = base
            elif unitTo == kRadiationKilowattHoursPSquareMeter:
                result = base * MJ_to_kWh
            elif unitTo == kRadiationCaloriesPerSquareMeter:
                result = base * MJ_to_joule * joule_to_cal
            elif unitTo == kRadiationLangleys:
                result = base * MJPm2_to_langleys
            elif unitTo == kRadiationMegaJoulesPSquareFoot:
                result = base / (m2_to_ft2)
            elif unitTo == kRadiationKilowattHoursPSquareFoot:
                result = base * MJ_to_kWh / (m2_to_ft2)
            elif unitTo == kRadiationCaloriesPerSquareFoot:
                result = base * MJ_to_joule * joule_to_cal / (m2_to_ft2)
        elif unitSet == kVolume:
            if unitFrom == kVolumeLiters:
                #base unit: liters
                base = value
            elif unitFrom == kVolumeMilliliters:
                base = value * ml_to_l
            elif unitFrom == kVolumeCubicMeters:
                base = value * m3_to_l
            elif unitFrom == kVolumeQuarts:
                base = value * qt_to_l
            elif unitFrom == kVolumeGallons:
                base = value * gal_to_qt * qt_to_l
            elif unitFrom == kVolumeOunces:
                base = value * floz_to_qt * qt_to_l
            if unitTo == kVolumeLiters:
                result = base
            elif unitTo == kVolumeMilliliters:
                result = base * l_to_ml
            elif unitTo == kVolumeCubicMeters:
                result = base * l_to_m3
            elif unitTo == kVolumeQuarts:
                result = base * l_to_qt
            elif unitTo == kVolumeGallons:
                result = base * l_to_qt * qt_to_gal
            elif unitTo == kVolumeOunces:
                result = base * l_to_qt * qt_to_floz
        elif unitSet == kDepthOfWater:
            if unitFrom == kDepthOfWaterMillimeters:
                #base unit: mm
                base = value
            elif unitFrom == kDepthOfWaterInches:
                base = value * in_to_cm * cm_to_mm
            if unitTo == kDepthOfWaterMillimeters:
                result = base
            elif unitTo == kDepthOfWaterInches:
                result = base * mm_to_cm * cm_to_in
        elif unitSet == kVelocity:
            if unitFrom == kVelocityMetersPSecond:
                #base unit: m/sec
                base = value
            elif unitFrom == kVelocityMillimetersPHour:
                base = value * mm_to_m / (hr_to_min * min_to_sec)
            elif unitFrom == kVelocityMilesPHour:
                base = value * (mi_to_ft * ft_to_in * in_to_cm * cm_to_m) / (hr_to_min * min_to_sec)
            elif unitFrom == kVelocityFeetPSecond:
                base = value * ft_to_in * in_to_cm * cm_to_m
            elif unitFrom == kVelocityInchesPHour:
                base = value * (in_to_cm * cm_to_m) / (hr_to_min * min_to_sec)
            if unitTo == kVelocityMetersPSecond:
                result = base
            elif unitTo == kVelocityMillimetersPHour:
                result = base * m_to_mm / (sec_to_min * min_to_hr)
            elif unitTo == kVelocityMilesPHour:
                result = base * (m_to_cm * cm_to_in * in_to_ft * ft_to_mi) / (sec_to_min * min_to_hr)
            elif unitTo == kVelocityFeetPSecond:
                result = base * m_to_cm * cm_to_in * in_to_ft
            elif unitTo == kVelocityInchesPHour:
                result = base * (m_to_cm * cm_to_in) / (sec_to_min * min_to_hr)
        elif unitSet == kPressure:
            if unitFrom == kPressurePascals:
                #base unit: pascal
                base = value
            elif unitFrom == kPressureKilopascals:
                base = value * kPa_to_pa
            elif unitFrom == kPressureMegapascals:
                base = value * MPa_to_kPa * kPa_to_pa
            elif unitFrom == kPressureKilogramsPSquareCentimeter:
                base = value * (kg_to_g * g_to_oz * oz_to_lb / cm2_to_in2) * psi_to_pa
            elif unitFrom == kPressureAtmospheres:
                base = value * atm_to_pa
            elif unitFrom == kPressureBars:
                base = value * bars_to_pa
            elif unitFrom == kPressurePoundsPSquareInch:
                base = value * psi_to_pa
            if unitTo == kPressurePascals:
                result = base
            elif unitTo == kPressureKilopascals:
                result = base * pa_to_kPa
            elif unitTo == kPressureMegapascals:
                result = base * pa_to_kPa * kPa_to_MPa
            elif unitTo == kPressureKilogramsPSquareCentimeter:
                result = base * pa_to_psi * (lb_to_oz * oz_to_g * g_to_kg / in2_to_cm2)
            elif unitTo == kPressureAtmospheres:
                result = base * pa_to_atm
            elif unitTo == kPressureBars:
                result = base * pa_to_bars
            elif unitTo == kPressurePoundsPSquareInch:
                result = base * pa_to_psi
        elif unitSet == kDensity:
            if unitFrom == kDensityMetricTonsPCubicMeter:
                #base unit: t/m3
                base = value
            elif unitFrom == kDensityGramsPCubicCentimeter:
                base = value
            elif unitFrom == kDensityKilogramsPCubicMeter:
                base = value * kg_to_t
            elif unitFrom == kDensityPoundsPCubicFoot:
                base = value * (lb_to_oz * oz_to_g * g_to_kg * kg_to_t) / (ft3_to_m3)
            elif unitFrom == kDensityPoundsPAcreFoot:
                base = value * (lb_to_oz * oz_to_g * g_to_kg * kg_to_t) / (acft_to_ft3 * ft3_to_m3)
            if unitTo == kDensityMetricTonsPCubicMeter:
                result = base
            elif unitTo == kDensityGramsPCubicCentimeter:
                result = base
            elif unitTo == kDensityKilogramsPCubicMeter:
                result = base * t_to_kg
            elif unitTo == kDensityPoundsPCubicFoot:
                result = base * (t_to_kg * kg_to_g * g_to_oz * oz_to_lb) / (m3_to_ft3)
            elif unitTo == kDensityPoundsPAcreFoot:
                result = base * (t_to_kg * kg_to_g * g_to_oz * oz_to_lb) / (m3_to_ft3 * ft3_to_acft)
        elif unitSet == kConcentration:
            if unitFrom == kConcentrationGramsPMetricTon:
                #base unit: g/t
                base = value
            elif unitFrom == kConcentrationGramsPKilogram:
                base = value / (kg_to_t)
            elif unitFrom == kConcentrationMilligramsPMetricTon:
                base = value * mg_to_g
            elif unitFrom == kConcentrationPoundsPEnglishTon:
                base = value * (lb_to_oz * oz_to_g) / (T_to_lb * lb_to_oz * oz_to_g * g_to_kg * kg_to_t)
            elif unitFrom == kConcentrationOuncesPEnglishTon:
                base = value * (oz_to_g) / (T_to_lb * lb_to_oz * oz_to_g * g_to_kg * kg_to_t)
            if unitTo == kConcentrationGramsPMetricTon:
                result = base
            elif unitTo == kConcentrationGramsPKilogram:
                result = base / (t_to_kg)
            elif unitTo == kConcentrationMilligramsPMetricTon:
                result = base * g_to_mg
            elif unitTo == kConcentrationPoundsPEnglishTon:
                result = base * (g_to_oz * oz_to_lb) / (t_to_kg * kg_to_g * g_to_oz * oz_to_lb * lb_to_T)
            elif unitTo == kConcentrationOuncesPEnglishTon:
                result = base * (g_to_oz) / (t_to_kg * kg_to_g * g_to_oz * oz_to_lb * lb_to_T)
        else :
            #non changing unit
            result = value
    except EOverflow:
        result = usupport.kMaxSingle
    except EUnderflow:
        result = umath.kLowestFloatAboveZero
    return result

def LoadUnitsInSetIntoComboBox(units, unitSet):
    unitEnum = 0
    unitString = ""
    
    unitEnum = GetNextUnitEnumInUnitSet(unitSet, 0)
    if unitEnum != 0:
        unitString = UnitStringForEnum(unitSet, unitEnum)
        units.Items.Add(unitString)
        unitEnum = GetNextUnitEnumInUnitSet(unitSet, unitEnum)
        unitString = UnitStringForEnum(unitSet, unitEnum)
        units.Items.Add(unitString)
        while unitEnum != 1:
            unitEnum = GetNextUnitEnumInUnitSet(unitSet, unitEnum)
            if unitEnum != 1:
                unitString = UnitStringForEnum(unitSet, unitEnum)
                units.Items.Add(unitString)
    else:
        units.Enabled = false

# if any unit set string in this function becomes longer than 12 chars, update constant at top of file 
def UnitStringForEnum(unitSetEnum, unitEnum):
    result = ""
    problem = false
    
    problem = false
    result = "(no unit)"
    if unitSetEnum == kDimensionless:
        result = "(no unit)"
    elif unitSetEnum == kLength:
        if unitEnum == kLengthMicrons:
            result = "microns"
        elif unitEnum == kLengthMillimeters:
            result = "mm"
        elif unitEnum == kLengthCentimeters:
            result = "cm"
        elif unitEnum == kLengthMeters:
            result = "m"
        elif unitEnum == kLengthKilometers:
            result = "km"
        elif unitEnum == kLengthInches:
            result = "in"
        elif unitEnum == kLengthFeet:
            result = "ft"
        elif unitEnum == kLengthYards:
            result = "yd"
        elif unitEnum == kLengthMiles:
            result = "mi"
        else :
            problem = true
    elif unitSetEnum == kAngle:
        if unitEnum == kAngleRadians:
            result = "radians"
        elif unitEnum == kAngleDegrees:
            result = "degrees"
        else :
            problem = true
    elif unitSetEnum == kTemperature:
        if unitEnum == kTemperatureDegreesC:
            result = "degrees C"
        elif unitEnum == kTemperatureDegreesF:
            result = "degrees F"
        else :
            problem = true
    elif unitSetEnum == kMass:
        if unitEnum == kMassMilligrams:
            result = "mg"
        elif unitEnum == kMassGrams:
            result = "g"
        elif unitEnum == kMassKilograms:
            result = "kg"
        elif unitEnum == kMassMetricTons:
            result = "t"
        elif unitEnum == kMassOunces:
            result = "oz"
        elif unitEnum == kMassPounds:
            result = "lb"
        elif unitEnum == kMassEnglishTons:
            result = "T"
        else :
            problem = true
    elif unitSetEnum == kArea:
        if unitEnum == kAreaHectares:
            result = "ha"
        elif unitEnum == kAreaSquareMeters:
            # superscript 2 is chr(178); superscript 3 is chr(179) 
            result = "m2"
        elif unitEnum == kAreaSquareKilometers:
            result = "km2"
        elif unitEnum == kAreaSquareFeet:
            result = "ft2"
        elif unitEnum == kAreaSquareYards:
            result = "yd2"
        elif unitEnum == kAreaAcres:
            result = "ac"
        elif unitEnum == kAreaSquareMiles:
            result = "mi2"
        else :
            problem = true
    elif unitSetEnum == kMassOverArea:
        if unitEnum == kMassOverAreaKilogramsPHectare:
            result = "kg/ha"
        elif unitEnum == kMassOverAreaMetricTonsPHectare:
            result = "t/ha"
        elif unitEnum == kMassOverAreaKilogramsPSquareMeter:
            result = "kg/m2"
        elif unitEnum == kMassOverAreaGramsPSquareMeter:
            result = "g/m2"
        elif unitEnum == kMassOverAreaGramsPSquareCentimeter:
            result = "g/cm2"
        elif unitEnum == kMassOverAreaPoundsPAcre:
            result = "lb/ac"
        elif unitEnum == kMassOverAreaEnglishTonsPAcre:
            result = "T/ac"
        elif unitEnum == kMassOverAreaPoundsPSquareYard:
            result = "lb/yd2"
        elif unitEnum == kMassOverAreaPoundsPSquareFoot:
            result = "lb/ft2"
        elif unitEnum == kMassOverAreaOuncesPSquareFoot:
            result = "oz/ft2"
        else :
            problem = true
    elif unitSetEnum == kRadiation:
        if unitEnum == kRadiationMegaJoulesPSquareMeter:
            result = "MJ/m2"
        elif unitEnum == kRadiationKilowattHoursPSquareMeter:
            result = "kWh/m2"
        elif unitEnum == kRadiationCaloriesPerSquareMeter:
            result = "cal/m2"
        elif unitEnum == kRadiationLangleys:
            result = "langleys"
        elif unitEnum == kRadiationMegaJoulesPSquareFoot:
            result = "MJ/ft2"
        elif unitEnum == kRadiationKilowattHoursPSquareFoot:
            result = "kWh/ft2"
        elif unitEnum == kRadiationCaloriesPerSquareFoot:
            result = "cal/ft2"
        else :
            problem = true
    elif unitSetEnum == kVolume:
        if unitEnum == kVolumeMilliliters:
            result = "ml"
        elif unitEnum == kVolumeLiters:
            result = "liters"
        elif unitEnum == kVolumeCubicMeters:
            result = "m3"
        elif unitEnum == kVolumeQuarts:
            result = "qt"
        elif unitEnum == kVolumeGallons:
            result = "gal"
        elif unitEnum == kVolumeOunces:
            result = "oz"
        else :
            problem = true
    elif unitSetEnum == kDepthOfWater:
        if unitEnum == kDepthOfWaterMillimeters:
            result = "mm (liquid)"
        elif unitEnum == kDepthOfWaterInches:
            result = "in (liquid)"
        else :
            problem = true
    elif unitSetEnum == kVelocity:
        if unitEnum == kVelocityMetersPSecond:
            result = "m/sec"
        elif unitEnum == kVelocityMillimetersPHour:
            result = "mm/hr"
        elif unitEnum == kVelocityMilesPHour:
            result = "mi/hr"
        elif unitEnum == kVelocityFeetPSecond:
            result = "ft/sec"
        elif unitEnum == kVelocityInchesPHour:
            result = "in/hr"
        else :
            problem = true
    elif unitSetEnum == kPressure:
        if unitEnum == kPressurePascals:
            result = "Pa"
        elif unitEnum == kPressureKilopascals:
            result = "kPa"
        elif unitEnum == kPressureMegapascals:
            result = "MPa"
        elif unitEnum == kPressureKilogramsPSquareCentimeter:
            result = "kg/cm2"
        elif unitEnum == kPressureAtmospheres:
            result = "atm"
        elif unitEnum == kPressureBars:
            result = "bars"
        elif unitEnum == kPressurePoundsPSquareInch:
            result = "lb/in2"
        else :
            problem = true
    elif unitSetEnum == kDensity:
        if unitEnum == kDensityGramsPCubicCentimeter:
            result = "g/cm3"
        elif unitEnum == kDensityKilogramsPCubicMeter:
            result = "kg/m3"
        elif unitEnum == kDensityMetricTonsPCubicMeter:
            result = "t/m3"
        elif unitEnum == kDensityPoundsPCubicFoot:
            result = "lb/ft3"
        elif unitEnum == kDensityPoundsPAcreFoot:
            result = "lb/ac ft"
        else :
            problem = true
    elif unitSetEnum == kConcentration:
        if unitEnum == kConcentrationGramsPMetricTon:
            result = "g/t"
        elif unitEnum == kConcentrationGramsPKilogram:
            result = "g/kg"
        elif unitEnum == kConcentrationMilligramsPMetricTon:
            result = "mg/t"
        elif unitEnum == kConcentrationPoundsPEnglishTon:
            result = "lb/T"
        elif unitEnum == kConcentrationOuncesPEnglishTon:
            result = "oz/T"
        else :
            problem = true
    elif unitSetEnum == kNonChangingUnitHundredsOfMolesPKilogram:
        result = "cmol/kg"
    elif unitSetEnum == kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter:
        result = "kg/ha/MJ/m2"
    elif unitSetEnum == kNonChangingUnitKiloPascalPDegreeC:
        result = "kPa/deg C"
    elif unitSetEnum == kNonChangingUnitMegaJoulePKilogram:
        result = "MJ/kg"
    elif unitSetEnum == kNonChangingUnitKilogramPKilogram:
        result = "kg/kg"
    elif unitSetEnum == kNonChangingUnitMetersPMeter:
        result = "m/m"
    elif unitSetEnum == kNonChangingUnitYears:
        result = "years"
    elif unitSetEnum == kNonChangingUnitDays:
        result = "days"
    elif unitSetEnum == kNonChangingUnitHours:
        result = "hours"
    elif unitSetEnum == kNonChangingUnitPartsPMillion:
        result = "ppm"
    elif unitSetEnum == kNonChangingUnitFraction:
        result = "fraction"
    elif unitSetEnum == kNonChangingUnitPercent:
        result = "%"
    elif unitSetEnum == kNonChangingUnitGramsPMetricTon:
        result = "g/t"
    elif unitSetEnum == kNonChangingUnitCubicMetersPSecond:
        result = "m3/sec"
    elif unitSetEnum == kNonChangingUnitBoolean:
        result = "True/False"
    else :
        result = "(no unit)"
        #  raise Exception.create('Unsupported unit set: ' + intToStr(unitSetEnum));  
    if problem:
        #  raise Exception.create('Unsupported unit ' + intToStr(unitEnum)
        #      + ' for unit set ' + intToStr(unitSetEnum)); 
        # PDF PORT -- added null statement
        None
    return result

def calcMaxUnitStringLengthForSet(unitSet, unitStart, unitEnd):
    result = 0
    unitString = ""
    i = 0
    
    result = 0
    for i in range(unitStart, unitEnd + 1):
        unitString = UnitStringForEnum(unitSet, i)
        if len(unitString) > result:
            result = len(unitString)
    return result

def setUpMaxUnitStringLengthsArray():
    maxUnitStringLengths[kDimensionless] = len(UnitStringForEnum(kDimensionless, 0))
    maxUnitStringLengths[kLength] = calcMaxUnitStringLengthForSet(kLength, kLengthFirstUnit, kLengthLastUnit - 1)
    maxUnitStringLengths[kObsoleteLength] = calcMaxUnitStringLengthForSet(kLength, kLengthFirstUnit, kLengthLastUnit - 1)
    maxUnitStringLengths[kAngle] = calcMaxUnitStringLengthForSet(kAngle, kAngleFirstUnit, kAngleLastUnit - 1)
    maxUnitStringLengths[kTemperature] = calcMaxUnitStringLengthForSet(kTemperature, kTemperatureFirstUnit, kTemperatureLastUnit - 1)
    maxUnitStringLengths[kMass] = calcMaxUnitStringLengthForSet(kMass, kMassFirstUnit, kMassLastUnit - 1)
    maxUnitStringLengths[kObsoleteMass] = calcMaxUnitStringLengthForSet(kMass, kMassFirstUnit, kMassLastUnit - 1)
    maxUnitStringLengths[kArea] = calcMaxUnitStringLengthForSet(kArea, kAreaFirstUnit, kAreaLastUnit - 1)
    maxUnitStringLengths[kMassOverArea] = calcMaxUnitStringLengthForSet(kMassOverArea, kMassOverAreaFirstUnit, kMassOverAreaLastUnit - 1)
    maxUnitStringLengths[kRadiation] = calcMaxUnitStringLengthForSet(kRadiation, kRadiationFirstUnit, kRadiationLastUnit - 1)
    maxUnitStringLengths[kVolume] = calcMaxUnitStringLengthForSet(kVolume, kVolumeFirstUnit, kVolumeLastUnit - 1)
    maxUnitStringLengths[kDepthOfWater] = calcMaxUnitStringLengthForSet(kDepthOfWater, kDepthOfWaterFirstUnit, kDepthOfWaterLastUnit - 1)
    maxUnitStringLengths[kVelocity] = calcMaxUnitStringLengthForSet(kVelocity, kVelocityFirstUnit, kVelocityLastUnit - 1)
    maxUnitStringLengths[kPressure] = calcMaxUnitStringLengthForSet(kPressure, kPressureFirstUnit, kPressureLastUnit - 1)
    maxUnitStringLengths[kDensity] = calcMaxUnitStringLengthForSet(kDensity, kDensityFirstUnit, kDensityLastUnit - 1)
    maxUnitStringLengths[kConcentration] = calcMaxUnitStringLengthForSet(kConcentration, kConcentrationFirstUnit, kConcentrationLastUnit - 1)
    maxUnitStringLengths[kNonChangingUnitHundredsOfMolesPKilogram] = len(UnitStringForEnum(kNonChangingUnitHundredsOfMolesPKilogram, 0))
    maxUnitStringLengths[kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter] = len(UnitStringForEnum(kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter, 0))
    maxUnitStringLengths[kNonChangingUnitKiloPascalPDegreeC] = len(UnitStringForEnum(kNonChangingUnitKiloPascalPDegreeC, 0))
    maxUnitStringLengths[kNonChangingUnitMegaJoulePKilogram] = len(UnitStringForEnum(kNonChangingUnitMegaJoulePKilogram, 0))
    maxUnitStringLengths[kNonChangingUnitKilogramPKilogram] = len(UnitStringForEnum(kNonChangingUnitKilogramPKilogram, 0))
    maxUnitStringLengths[kNonChangingUnitMetersPMeter] = len(UnitStringForEnum(kNonChangingUnitMetersPMeter, 0))
    maxUnitStringLengths[kNonChangingUnitYears] = len(UnitStringForEnum(kNonChangingUnitYears, 0))
    maxUnitStringLengths[kNonChangingUnitDays] = len(UnitStringForEnum(kNonChangingUnitDays, 0))
    maxUnitStringLengths[kNonChangingUnitHours] = len(UnitStringForEnum(kNonChangingUnitHours, 0))
    maxUnitStringLengths[kNonChangingUnitPartsPMillion] = len(UnitStringForEnum(kNonChangingUnitPartsPMillion, 0))
    maxUnitStringLengths[kNonChangingUnitFraction] = len(UnitStringForEnum(kNonChangingUnitFraction, 0))
    maxUnitStringLengths[kNonChangingUnitPercent] = len(UnitStringForEnum(kNonChangingUnitPercent, 0))
    maxUnitStringLengths[kNonChangingUnitGramsPMetricTon] = len(UnitStringForEnum(kNonChangingUnitGramsPMetricTon, 0))
    maxUnitStringLengths[kNonChangingUnitCubicMetersPSecond] = len(UnitStringForEnum(kNonChangingUnitCubicMetersPSecond, 0))
    maxUnitStringLengths[kNonChangingUnitBoolean] = len(UnitStringForEnum(kNonChangingUnitBoolean, 0))

def maxUnitStringLengthForSet(unitSet):
    result = 0
    result = 0
    if (unitSet < kDimensionless) or (unitSet >= kLastUnitSet):
        raise GeneralException.create("Problem: Unsupported unit set " + IntToStr(unitSet) + " in method maxUnitStringLengthForSet.")
    else:
        result = maxUnitStringLengths[unitSet]
    return result

def GetNextUnitEnumInUnitSet(unitSet, currentUnit):
    result = 0
    if unitSet == kDimensionless:
        result = 0
    elif unitSet == kLength:
        if (currentUnit == kLengthMiles):
            result = kLengthMicrons
        else:
            result = currentUnit + 1
    elif unitSet == kAngle:
        if (currentUnit == kAngleRadians):
            result = kAngleDegrees
        else:
            result = kAngleRadians
    elif unitSet == kTemperature:
        if (currentUnit == kTemperatureDegreesC):
            result = kTemperatureDegreesF
        else:
            result = kTemperatureDegreesC
    elif unitSet == kMass:
        if (currentUnit == kMassEnglishTons):
            result = kMassMilligrams
        else:
            result = currentUnit + 1
    elif unitSet == kArea:
        if (currentUnit == kAreaSquareMiles):
            result = kAreaHectares
        else:
            result = currentUnit + 1
    elif unitSet == kMassOverArea:
        if (currentUnit == kMassOverAreaOuncesPSquareFoot):
            result = kMassOverAreaKilogramsPHectare
        else:
            result = currentUnit + 1
    elif unitSet == kRadiation:
        if (currentUnit == kRadiationCaloriesPerSquareFoot):
            result = kRadiationMegaJoulesPSquareMeter
        else:
            result = currentUnit + 1
    elif unitSet == kVolume:
        if (currentUnit == kVolumeOunces):
            result = kVolumeMilliliters
        else:
            result = currentUnit + 1
    elif unitSet == kDepthOfWater:
        if (currentUnit == kDepthOfWaterInches):
            result = kDepthOfWaterMillimeters
        else:
            result = kDepthOfWaterInches
    elif unitSet == kVelocity:
        if (currentUnit == kVelocityInchesPHour):
            result = kVelocityMetersPSecond
        else:
            result = currentUnit + 1
    elif unitSet == kPressure:
        if (currentUnit == kPressurePoundsPSquareInch):
            result = kPressurePascals
        else:
            result = currentUnit + 1
    elif unitSet == kDensity:
        if (currentUnit == kDensityPoundsPAcreFoot):
            result = kDensityGramsPCubicCentimeter
        else:
            result = currentUnit + 1
    elif unitSet == kConcentration:
        if (currentUnit == kConcentrationOuncesPEnglishTon):
            result = kConcentrationGramsPMetricTon
        else:
            result = currentUnit + 1
    else :
        # non-changing unit set 
        result = currentUnit
    return result

def GetPreviousUnitEnumInUnitSet(unitSet, currentUnit):
    result = 0
    if unitSet == kDimensionless:
        result = 0
    elif unitSet == kLength:
        if (currentUnit == kLengthMicrons):
            result = kLengthMiles
        else:
            result = currentUnit - 1
    elif unitSet == kAngle:
        if (currentUnit == kAngleRadians):
            # same as next 
            result = kAngleDegrees
        else:
            result = kAngleRadians
    elif unitSet == kTemperature:
        if (currentUnit == kTemperatureDegreesC):
            # same as next 
            result = kTemperatureDegreesF
        else:
            result = kTemperatureDegreesC
    elif unitSet == kMass:
        if (currentUnit == kMassMilligrams):
            result = kMassEnglishTons
        else:
            result = currentUnit - 1
    elif unitSet == kArea:
        if (currentUnit == kAreaHectares):
            result = kAreaSquareMiles
        else:
            result = currentUnit - 1
    elif unitSet == kMassOverArea:
        if (currentUnit == kMassOverAreaKilogramsPHectare):
            result = kMassOverAreaOuncesPSquareFoot
        else:
            result = currentUnit - 1
    elif unitSet == kRadiation:
        if (currentUnit == kRadiationMegaJoulesPSquareMeter):
            result = kRadiationCaloriesPerSquareFoot
        else:
            result = currentUnit - 1
    elif unitSet == kVolume:
        if (currentUnit == kVolumeMilliliters):
            result = kVolumeOunces
        else:
            result = currentUnit - 1
    elif unitSet == kDepthOfWater:
        if (currentUnit == kDepthOfWaterInches):
            # same as next 
            result = kDepthOfWaterMillimeters
        else:
            result = kDepthOfWaterInches
    elif unitSet == kVelocity:
        if (currentUnit == kVelocityMetersPSecond):
            result = kVelocityInchesPHour
        else:
            result = currentUnit - 1
    elif unitSet == kPressure:
        if (currentUnit == kPressurePascals):
            result = kPressurePoundsPSquareInch
        else:
            result = currentUnit - 1
    elif unitSet == kDensity:
        if (currentUnit == kDensityGramsPCubicCentimeter):
            result = kDensityPoundsPAcreFoot
        else:
            result = currentUnit - 1
    elif unitSet == kConcentration:
        if (currentUnit == kConcentrationGramsPMetricTon):
            result = kConcentrationOuncesPEnglishTon
        else:
            result = currentUnit - 1
    else :
        # non-changing unit set 
        result = currentUnit
    return result

def GetUnitSetString(unitSet):
    result = ""
    if unitSet == kDimensionless:
        result = "kDimensionless"
    elif unitSet == kLength:
        result = "kLength"
    elif unitSet == kObsoleteLength:
        result = "kObsoleteLength"
    elif unitSet == kAngle:
        result = "kAngle"
    elif unitSet == kTemperature:
        result = "kTemperature"
    elif unitSet == kMass:
        result = "kMass"
    elif unitSet == kObsoleteMass:
        result = "kObsoleteMass"
    elif unitSet == kArea:
        result = "kArea"
    elif unitSet == kMassOverArea:
        result = "kMassOverArea"
    elif unitSet == kRadiation:
        result = "kRadiation"
    elif unitSet == kVolume:
        result = "kVolume"
    elif unitSet == kDepthOfWater:
        result = "kDepthOfWater"
    elif unitSet == kVelocity:
        result = "kVelocity"
    elif unitSet == kPressure:
        result = "kPressure"
    elif unitSet == kDensity:
        result = "kDensity"
    elif unitSet == kConcentration:
        result = "kConcentration"
    elif unitSet == kNonChangingUnitHundredsOfMolesPKilogram:
        result = "kNonChangingUnitHundredsOfMolesPKilogram"
    elif unitSet == kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter:
        result = "kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter"
    elif unitSet == kNonChangingUnitKiloPascalPDegreeC:
        result = "kNonChangingUnitKiloPascalPDegreeC"
    elif unitSet == kNonChangingUnitMegaJoulePKilogram:
        result = "kNonChangingUnitMegaJoulePKilogram"
    elif unitSet == kNonChangingUnitKilogramPKilogram:
        result = "kNonChangingUnitKilogramPKilogram"
    elif unitSet == kNonChangingUnitMetersPMeter:
        result = "kNonChangingUnitMetersPMeter"
    elif unitSet == kNonChangingUnitYears:
        result = "kNonChangingUnitYears"
    elif unitSet == kNonChangingUnitDays:
        result = "kNonChangingUnitDays"
    elif unitSet == kNonChangingUnitHours:
        result = "kNonChangingUnitHours"
    elif unitSet == kNonChangingUnitPartsPMillion:
        result = "kNonChangingUnitPartsPMillion"
    elif unitSet == kNonChangingUnitFraction:
        result = "kNonChangingUnitFraction"
    elif unitSet == kNonChangingUnitPercent:
        result = "kNonChangingUnitPercent"
    elif unitSet == kNonChangingUnitGramsPMetricTon:
        result = "kNonChangingUnitGramsPMetricTon"
    elif unitSet == kNonChangingUnitCubicMetersPSecond:
        result = "kNonChangingUnitCubicMetersPSecond"
    elif unitSet == kNonChangingUnitBoolean:
        result = "kNonChangingUnitBoolean"
    else :
        result = ""
        raise GeneralException.create("Problem: Unsupported unit set " + IntToStr(unitSet) + " in method GetUnitSetString.")
    return result

def DisplayUnitSetString(unitSet):
    result = ""
    if unitSet == kDimensionless:
        result = "(no unit)"
    elif unitSet == kLength:
        result = "length (e.g., m)"
    elif unitSet == kObsoleteLength:
        result = "length (e.g., m)"
    elif unitSet == kAngle:
        result = "angle (degrees or radians)"
    elif unitSet == kTemperature:
        result = "temperature (degrees C or F)"
    elif unitSet == kMass:
        result = "mass (e.g., kg)"
    elif unitSet == kObsoleteMass:
        result = "mass (e.g., kg)"
    elif unitSet == kArea:
        result = "area (e.g., m2)"
    elif unitSet == kMassOverArea:
        result = "mass over area (e.g., kg/ha)"
    elif unitSet == kRadiation:
        result = "radiation (e.g., MJ/m2)"
    elif unitSet == kVolume:
        result = "volume (e.g., liters)"
    elif unitSet == kDepthOfWater:
        result = "depth of liquid (e.g., mm H20)"
    elif unitSet == kVelocity:
        result = "velocity (e.g., mm/hr)"
    elif unitSet == kPressure:
        result = "pressure (e.g. kPa)"
    elif unitSet == kDensity:
        result = "density (e.g., g/cm3)"
    elif unitSet == kConcentration:
        result = "concentration (e.g., g/t)"
    elif unitSet == kNonChangingUnitHundredsOfMolesPKilogram:
        result = "cmol/kg"
    elif unitSet == kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter:
        result = "MJ/m2"
    elif unitSet == kNonChangingUnitKiloPascalPDegreeC:
        result = "kPa/deg C"
    elif unitSet == kNonChangingUnitMegaJoulePKilogram:
        result = "MJ/kg"
    elif unitSet == kNonChangingUnitKilogramPKilogram:
        result = "kg/kg"
    elif unitSet == kNonChangingUnitMetersPMeter:
        result = "m/m"
    elif unitSet == kNonChangingUnitYears:
        result = "years"
    elif unitSet == kNonChangingUnitDays:
        result = "days"
    elif unitSet == kNonChangingUnitHours:
        result = "hours"
    elif unitSet == kNonChangingUnitPartsPMillion:
        result = "ppm"
    elif unitSet == kNonChangingUnitFraction:
        result = "fraction"
    elif unitSet == kNonChangingUnitPercent:
        result = "percent"
    elif unitSet == kNonChangingUnitGramsPMetricTon:
        result = "g/t"
    elif unitSet == kNonChangingUnitCubicMetersPSecond:
        result = "m3/sec"
    elif unitSet == kNonChangingUnitBoolean:
        result = "yes/no"
    else :
        result = ""
        raise GeneralException.create("Problem: Unsupported unit set " + IntToStr(unitSet) + " in method DisplayUnitSetString.")
    return result

def GetLastUnitEnumInUnitSet(unitSet):
    result = 0
    if unitSet == kDimensionless:
        result = 2
    elif unitSet == kLength:
        result = kLengthLastUnit
    elif unitSet == kObsoleteLength:
        result = kLengthLastUnit
    elif unitSet == kAngle:
        result = kAngleLastUnit
    elif unitSet == kTemperature:
        result = kTemperatureLastUnit
    elif unitSet == kMass:
        result = kMassLastUnit
    elif unitSet == kObsoleteMass:
        result = kMassLastUnit
    elif unitSet == kArea:
        result = kAreaLastUnit
    elif unitSet == kMassOverArea:
        result = kMassOverAreaLastUnit
    elif unitSet == kRadiation:
        result = kRadiationLastUnit
    elif unitSet == kVolume:
        result = kVolumeLastUnit
    elif unitSet == kDepthOfWater:
        result = kDepthOfWaterLastUnit
    elif unitSet == kVelocity:
        result = kVelocityLastUnit
    elif unitSet == kPressure:
        result = kPressureLastUnit
    elif unitSet == kDensity:
        result = kDensityLastUnit
    elif unitSet == kConcentration:
        result = kConcentrationLastUnit
    else :
        result = 2
    return result

def unitIsMetric(unitSetEnum, unitEnum):
    result = false
    result = false
    if unitSetEnum == kDimensionless:
        result = false
    elif unitSetEnum == kLength:
        if unitEnum == kLengthMicrons:
            result = true
        elif unitEnum == kLengthMillimeters:
            result = true
        elif unitEnum == kLengthCentimeters:
            result = true
        elif unitEnum == kLengthMeters:
            result = true
        elif unitEnum == kLengthKilometers:
            result = true
    elif unitSetEnum == kAngle:
        result = true
    elif unitSetEnum == kTemperature:
        if unitEnum == kTemperatureDegreesC:
            result = true
    elif unitSetEnum == kMass:
        if unitEnum == kMassMilligrams:
            result = true
        elif unitEnum == kMassGrams:
            result = true
        elif unitEnum == kMassKilograms:
            result = true
        elif unitEnum == kMassMetricTons:
            result = true
    elif unitSetEnum == kArea:
        if unitEnum == kAreaHectares:
            result = true
        elif unitEnum == kAreaSquareMeters:
            result = true
        elif unitEnum == kAreaSquareKilometers:
            result = true
    elif unitSetEnum == kMassOverArea:
        if unitEnum == kMassOverAreaKilogramsPHectare:
            result = true
        elif unitEnum == kMassOverAreaMetricTonsPHectare:
            result = true
        elif unitEnum == kMassOverAreaKilogramsPSquareMeter:
            result = true
        elif unitEnum == kMassOverAreaGramsPSquareMeter:
            result = true
        elif unitEnum == kMassOverAreaGramsPSquareCentimeter:
            result = true
    elif unitSetEnum == kRadiation:
        if unitEnum == kRadiationMegaJoulesPSquareMeter:
            result = true
        elif unitEnum == kRadiationKilowattHoursPSquareMeter:
            result = true
        elif unitEnum == kRadiationCaloriesPerSquareMeter:
            result = true
        elif unitEnum == kRadiationLangleys:
            result = true
    elif unitSetEnum == kVolume:
        if unitEnum == kVolumeMilliliters:
            result = true
        elif unitEnum == kVolumeLiters:
            result = true
        elif unitEnum == kVolumeCubicMeters:
            result = true
    elif unitSetEnum == kDepthOfWater:
        if unitEnum == kDepthOfWaterMillimeters:
            result = true
    elif unitSetEnum == kVelocity:
        if unitEnum == kVelocityMetersPSecond:
            result = true
        elif unitEnum == kVelocityMillimetersPHour:
            result = true
    elif unitSetEnum == kPressure:
        if unitEnum == kPressurePascals:
            result = true
        elif unitEnum == kPressureKilopascals:
            result = true
        elif unitEnum == kPressureMegapascals:
            result = true
        elif unitEnum == kPressureKilogramsPSquareCentimeter:
            result = true
    elif unitSetEnum == kDensity:
        if unitEnum == kDensityGramsPCubicCentimeter:
            result = true
        elif unitEnum == kDensityKilogramsPCubicMeter:
            result = true
        elif unitEnum == kDensityMetricTonsPCubicMeter:
            result = true
    elif unitSetEnum == kConcentration:
        if unitEnum == kConcentrationGramsPMetricTon:
            result = true
        elif unitEnum == kConcentrationGramsPKilogram:
            result = true
        elif unitEnum == kConcentrationMilligramsPMetricTon:
            result = true
    elif unitSetEnum == kNonChangingUnitHundredsOfMolesPKilogram:
        result = true
    elif unitSetEnum == kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter:
        result = true
    elif unitSetEnum == kNonChangingUnitKiloPascalPDegreeC:
        result = true
    elif unitSetEnum == kNonChangingUnitMegaJoulePKilogram:
        result = true
    elif unitSetEnum == kNonChangingUnitKilogramPKilogram:
        result = true
    elif unitSetEnum == kNonChangingUnitMetersPMeter:
        result = true
    elif unitSetEnum == kNonChangingUnitGramsPMetricTon:
        result = true
    elif unitSetEnum == kNonChangingUnitCubicMetersPSecond:
        result = true
    return result

