// unit uunits
//Copyright (c) 1997 Paul D. Fernhout and Cynthia F. Kurtz All rights reserved
//http://www.gardenwithinsight.com. See the license file for details on redistribution.
//=====================================================================================
//uunits: Functions for conversion of units in whole system. There are 32 unit sets,
//and each unit set contains units that are inter-convertible. For example, the
//temperature unit set contains degrees C and degrees F. The unit set must be saved
//and given during any conversion so the function knows which code to use to convert
//the units. Numbers cannot be converted between unit sets. The file also contains
//information for displaying the units (the string to show, etc).

from conversion_common import *;
import umath;
import usupport;
import delphi_compatability;

// const
kRangeOK = 0;
kRangeTooLow = 1;
kRangeTooHigh = 2;
kRangeBounds = 3;
kRangeMustBeInteger = 4;
kDefaultFloatMin = -100000000000.0;
kDefaultFloatMax = 100000000000.0;
kMaxUnitStringLength = 12;


// const
kDimensionless = 1;
kLength = 2;
kObsoleteLength = 3;
kAngle = 4;
kTemperature = 5;
kMass = 6;
kObsoleteMass = 7;
kArea = 8;
kMassOverArea = 9;
kRadiation = 10;
kVolume = 11;
kDepthOfWater = 12;
kVelocity = 13;
kPressure = 14;
kDensity = 15;
kNonChangingUnitHundredsOfMolesPKilogram = 16;
kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter = 17;
kNonChangingUnitKiloPascalPDegreeC = 18;
kNonChangingUnitMegaJoulePKilogram = 19;
kNonChangingUnitKilogramPKilogram = 20;
kNonChangingUnitMetersPMeter = 21;
kNonChangingUnitYears = 22;
kNonChangingUnitDays = 23;
kNonChangingUnitHours = 24;
kNonChangingUnitPartsPMillion = 25;
kNonChangingUnitFraction = 26;
kNonChangingUnitPercent = 27;
kNonChangingUnitGramsPMetricTon = 28;
kNonChangingUnitCubicMetersPSecond = 29;
kNonChangingUnitBoolean = 30;
kConcentration = 31;
kLastUnitSet = 32;


// var
 maxUnitStringLengths = [0] * (range(kDimensionless, kLastUnitSet + 1) + 1);


// const
kLengthFirstUnit = 1;
kLengthMicrons = 1;
kLengthMillimeters = 2;
kLengthCentimeters = 3;
kLengthMeters = 4;
kLengthKilometers = 5;
kLengthInches = 6;
kLengthFeet = 7;
kLengthYards = 8;
kLengthMiles = 9;
kLengthLastUnit = 10;


// const
kAngleFirstUnit = 1;
kAngleRadians = 1;
kAngleDegrees = 2;
kAngleLastUnit = 3;


// const
kTemperatureFirstUnit = 1;
kTemperatureDegreesC = 1;
kTemperatureDegreesF = 2;
kTemperatureLastUnit = 3;


// const
kMassFirstUnit = 1;
kMassMilligrams = 1;
kMassGrams = 2;
kMassKilograms = 3;
kMassMetricTons = 4;
kMassOunces = 5;
kMassPounds = 6;
kMassEnglishTons = 7;
kMassLastUnit = 8;


// const
kAreaFirstUnit = 1;
kAreaHectares = 1;
kAreaSquareMeters = 2;
kAreaSquareKilometers = 3;
kAreaSquareFeet = 4;
kAreaSquareYards = 5;
kAreaAcres = 6;
kAreaSquareMiles = 7;
kAreaLastUnit = 8;


// const
kMassOverAreaFirstUnit = 1;
kMassOverAreaKilogramsPHectare = 1;
kMassOverAreaMetricTonsPHectare = 2;
kMassOverAreaKilogramsPSquareMeter = 3;
kMassOverAreaGramsPSquareMeter = 4;
kMassOverAreaGramsPSquareCentimeter = 5;
kMassOverAreaPoundsPAcre = 6;
kMassOverAreaEnglishTonsPAcre = 7;
kMassOverAreaPoundsPSquareYard = 8;
kMassOverAreaPoundsPSquareFoot = 9;
kMassOverAreaOuncesPSquareFoot = 10;
kMassOverAreaLastUnit = 11;


// const
kRadiationFirstUnit = 1;
kRadiationMegaJoulesPSquareMeter = 1;
kRadiationKilowattHoursPSquareMeter = 2;
kRadiationCaloriesPerSquareMeter = 3;
kRadiationLangleys = 4;
kRadiationMegaJoulesPSquareFoot = 5;
kRadiationKilowattHoursPSquareFoot = 6;
kRadiationCaloriesPerSquareFoot = 7;
kRadiationLastUnit = 8;


// const
kVolumeFirstUnit = 1;
kVolumeMilliliters = 1;
kVolumeLiters = 2;
kVolumeCubicMeters = 3;
kVolumeQuarts = 4;
kVolumeGallons = 5;
kVolumeOunces = 6;
kVolumeLastUnit = 7;


// const
kDepthOfWaterFirstUnit = 1;
kDepthOfWaterMillimeters = 1;
kDepthOfWaterInches = 2;
kDepthOfWaterLastUnit = 3;


// const
kVelocityFirstUnit = 1;
kVelocityMetersPSecond = 1;
kVelocityMillimetersPHour = 2;
kVelocityMilesPHour = 3;
kVelocityFeetPSecond = 4;
kVelocityInchesPHour = 5;
kVelocityLastUnit = 6;


// const
kPressureFirstUnit = 1;
kPressurePascals = 1;
kPressureKilopascals = 2;
kPressureMegapascals = 3;
kPressureKilogramsPSquareCentimeter = 4;
kPressureAtmospheres = 5;
kPressureBars = 6;
kPressurePoundsPSquareInch = 7;
kPressureLastUnit = 8;


// const
kDensityFirstUnit = 1;
kDensityGramsPCubicCentimeter = 1;
kDensityKilogramsPCubicMeter = 2;
kDensityMetricTonsPCubicMeter = 3;
kDensityPoundsPCubicFoot = 4;
kDensityPoundsPAcreFoot = 5;
kDensityLastUnit = 6;


// const
kConcentrationFirstUnit = 1;
kConcentrationGramsPMetricTon = 1;
kConcentrationGramsPKilogram = 2;
kConcentrationMilligramsPMetricTon = 3;
kConcentrationPoundsPEnglishTon = 4;
kConcentrationOuncesPEnglishTon = 5;
kConcentrationLastUnit = 6;


// var
float m_to_microns = 0.0;
float microns_to_m = 0.0;
float m_to_mm = 0.0;
float mm_to_m = 0.0;
float m_to_cm = 0.0;
float cm_to_m = 0.0;
float cm_to_mm = 0.0;
float mm_to_cm = 0.0;
float km_to_m = 0.0;
float m_to_km = 0.0;
float in_to_cm = 0.0;
float cm_to_in = 0.0;
float ft_to_in = 0.0;
float in_to_ft = 0.0;
float yd_to_ft = 0.0;
float ft_to_yd = 0.0;
float mi_to_ft = 0.0;
float ft_to_mi = 0.0;
float t_to_kg = 0.0;
float kg_to_t = 0.0;
float kg_to_g = 0.0;
float g_to_kg = 0.0;
float g_to_mg = 0.0;
float mg_to_g = 0.0;
float oz_to_g = 0.0;
float g_to_oz = 0.0;
float lb_to_oz = 0.0;
float oz_to_lb = 0.0;
float T_to_lb = 0.0;
float lb_to_T = 0.0;
float ha_to_m2 = 0.0;
float m2_to_ha = 0.0;
float km2_to_m2 = 0.0;
float m2_to_km2 = 0.0;
float m2_to_cm2 = 0.0;
float cm2_to_m2 = 0.0;
float m2_to_ft2 = 0.0;
float ft2_to_m2 = 0.0;
float in2_to_cm2 = 0.0;
float cm2_to_in2 = 0.0;
float yd2_to_ft2 = 0.0;
float ft2_to_yd2 = 0.0;
float ac_to_ft2 = 0.0;
float ft2_to_ac = 0.0;
float mi2_to_ac = 0.0;
float ac_to_mi2 = 0.0;
float kWh_to_MJ = 0.0;
float MJ_to_kWh = 0.0;
float MJ_to_joule = 0.0;
float joule_to_MJ = 0.0;
float cal_to_joule = 0.0;
float joule_to_cal = 0.0;
float MJPm2_to_langleys = 0.0;
float langleys_to_MJPm2 = 0.0;
float l_to_ml = 0.0;
float ml_to_l = 0.0;
float m3_to_l = 0.0;
float l_to_m3 = 0.0;
float qt_to_l = 0.0;
float l_to_qt = 0.0;
float gal_to_qt = 0.0;
float qt_to_gal = 0.0;
float qt_to_floz = 0.0;
float floz_to_qt = 0.0;
float m3_to_ft3 = 0.0;
float ft3_to_m3 = 0.0;
float acft_to_ft3 = 0.0;
float ft3_to_acft = 0.0;
float kPa_to_pa = 0.0;
float pa_to_kPa = 0.0;
float MPa_to_kPa = 0.0;
float kPa_to_MPa = 0.0;
float psi_to_pa = 0.0;
float pa_to_psi = 0.0;
float atm_to_pa = 0.0;
float pa_to_atm = 0.0;
float bars_to_pa = 0.0;
float pa_to_bars = 0.0;
float hr_to_min = 0.0;
float min_to_hr = 0.0;
float min_to_sec = 0.0;
float sec_to_min = 0.0;
float rad_to_deg = 0.0;
float deg_to_rad = 0.0;
float frn_to_pct = 0.0;
float pct_to_frn = 0.0;


// if change any unit string to make it longer than this, update 
// unit sets  
// obsolete 
// obsolete 
//length (base unit: m) 
// note: length used to be split into small and large,
//  but these two have been combined so the user doesn't see them. 
// was inches 
// was feet 
// was yards 
// was large meters 
// was large km 
// 10 was large yards 
// 11 was large miles 
// angle (base unit: radians)
// temperature (base unit: deg C)  
// Mass (base unit: kg) (both small and large) 
// note: these two have been combined so the user doesn't see them. 
// was ounces 
// was pounds 
// was large kg 
// was large metric tons 
// 8 was large pounds 
// 9 was large english tons 
// area (base unit: m2)  
// Mass over area (base unit: kg/ha) 
// radiation (base unit: MJ/m2) 
// volume (base unit: liter) 
// depth of water (precipitation) (base unit: mm) 
// velocity (base unit: m/sec) 
// pressure (base unit: Pa)
// density (base unit: g/cm3) (also concentration) 
// concentration (base unit: g/t) 
// length 
// mass 
// area 
// energy 
// volume 
// pressure 
// other 
public void setUnitConstants() {
    // length 
    m_to_microns = 1000000.0;
    microns_to_m = 1.0 / m_to_microns;
    m_to_mm = 1000.0;
    mm_to_m = 1.0 / m_to_mm;
    m_to_cm = 100.0;
    cm_to_m = 1.0 / m_to_cm;
    cm_to_mm = 10.0;
    mm_to_cm = 1.0 / cm_to_mm;
    km_to_m = 1000.0;
    m_to_km = 1.0 / km_to_m;
    in_to_cm = 2.54;
    cm_to_in = 1.0 / in_to_cm;
    ft_to_in = 12.0;
    in_to_ft = 1.0 / ft_to_in;
    yd_to_ft = 3.0;
    ft_to_yd = 1.0 / yd_to_ft;
    mi_to_ft = 5280.0;
    ft_to_mi = 1.0 / mi_to_ft;
    // mass 
    t_to_kg = 1000.0;
    kg_to_t = 1.0 / t_to_kg;
    kg_to_g = 1000.0;
    g_to_kg = 1.0 / kg_to_g;
    g_to_mg = 1000.0;
    mg_to_g = 1.0 / g_to_mg;
    oz_to_g = 28.35;
    g_to_oz = 1.0 / oz_to_g;
    lb_to_oz = 16.0;
    oz_to_lb = 1.0 / lb_to_oz;
    T_to_lb = 2000.0;
    lb_to_T = 1.0 / T_to_lb;
    // area 
    ha_to_m2 = 10000.0;
    m2_to_ha = 1.0 / ha_to_m2;
    km2_to_m2 = 1000000.0;
    m2_to_km2 = 1.0 / km2_to_m2;
    m2_to_cm2 = 10000.0;
    cm2_to_m2 = 1 / m2_to_cm2;
    m2_to_ft2 = 10.7639;
    ft2_to_m2 = 1.0 / m2_to_ft2;
    in2_to_cm2 = 6.4516;
    cm2_to_in2 = 1.0 / in2_to_cm2;
    yd2_to_ft2 = 9.0;
    ft2_to_yd2 = 1.0 / yd2_to_ft2;
    ac_to_ft2 = 43560.0;
    ft2_to_ac = 1.0 / ac_to_ft2;
    mi2_to_ac = 640.0;
    ac_to_mi2 = 1.0 / mi2_to_ac;
    // energy 
    kWh_to_MJ = 3.6;
    MJ_to_kWh = 1.0 / kWh_to_MJ;
    MJ_to_joule = 1000000.0;
    joule_to_MJ = 1.0 / MJ_to_joule;
    cal_to_joule = 4.1868;
    joule_to_cal = 1.0 / cal_to_joule;
    MJPm2_to_langleys = 23.8846;
    langleys_to_MJPm2 = 1.0 / MJPm2_to_langleys;
    // volume 
    l_to_ml = 1000.0;
    ml_to_l = 1.0 / l_to_ml;
    m3_to_l = 1000.0;
    l_to_m3 = 1.0 / m3_to_l;
    qt_to_l = 0.946;
    l_to_qt = 1.0 / qt_to_l;
    gal_to_qt = 4.0;
    qt_to_gal = 1.0 / gal_to_qt;
    qt_to_floz = 32.0;
    floz_to_qt = 1.0 / qt_to_floz;
    m3_to_ft3 = 35.32;
    ft3_to_m3 = 1.0 / m3_to_ft3;
    acft_to_ft3 = 43560.0;
    ft3_to_acft = 1.0 / acft_to_ft3;
    // pressure 
    kPa_to_pa = 1000.0;
    pa_to_kPa = 1.0 / kPa_to_pa;
    MPa_to_kPa = 1000.0;
    kPa_to_MPa = 1.0 / MPa_to_kPa;
    psi_to_pa = 6894.76;
    pa_to_psi = 1.0 / psi_to_pa;
    atm_to_pa = 101325.0;
    pa_to_atm = 1.0 / atm_to_pa;
    bars_to_pa = 100000;
    pa_to_bars = 1.0 / bars_to_pa;
    // other 
    hr_to_min = 60.0;
    min_to_hr = 1.0 / hr_to_min;
    min_to_sec = 60.0;
    sec_to_min = 1.0 / min_to_sec;
    rad_to_deg = 57.296;
    deg_to_rad = 1.0 / rad_to_deg;
    frn_to_pct = 100.0;
    pct_to_frn = 1.0 / frn_to_pct;
}

public float Convert(int unitSet, int unitFrom, int unitTo, float value) {
    result = 0.0;
    double base = 0.0;
    
    base = 0.0;
    // default result to same value if something goes wrong 
    result = value;
    if ((unitFrom == unitTo) || (value == usupport.kMaxSingle) || (value == usupport.kMinSingle)) {
        // if no conversion, exit 
        return result;
    }
    if (value == usupport.kMaxSingle) {
        // special check for overflow (for bounds) to avoid exception-handling system 
        result = usupport.kMaxSingle;
        return result;
    }
    if (value == -usupport.kMaxSingle) {
        result = -usupport.kMaxSingle;
        return result;
    }
    try {
        switch (unitSet) {
            case kDimensionless:
                result = value;
                break;
            case kLength:
                switch (unitFrom) {
                    case kLengthMicrons:
                        //base unit: meters
                        base = value * microns_to_m;
                        break;
                    case kLengthMillimeters:
                        base = value * mm_to_m;
                        break;
                    case kLengthCentimeters:
                        base = value * cm_to_m;
                        break;
                    case kLengthMeters:
                        base = value;
                        break;
                    case kLengthKilometers:
                        base = value * km_to_m;
                        break;
                    case kLengthInches:
                        base = value * in_to_cm * cm_to_m;
                        break;
                    case kLengthFeet:
                        base = value * ft_to_in * in_to_cm * cm_to_m;
                        break;
                    case kLengthYards:
                        base = value * yd_to_ft * ft_to_in * in_to_cm * cm_to_m;
                        break;
                    case kLengthMiles:
                        base = value * mi_to_ft * ft_to_in * in_to_cm * cm_to_m;
                        break;
                switch (unitTo) {
                    case kLengthMicrons:
                        result = base * m_to_microns;
                        break;
                    case kLengthMillimeters:
                        result = base * m_to_mm;
                        break;
                    case kLengthCentimeters:
                        result = base * m_to_cm;
                        break;
                    case kLengthMeters:
                        result = base;
                        break;
                    case kLengthKilometers:
                        result = base * m_to_km;
                        break;
                    case kLengthInches:
                        result = base * m_to_cm * cm_to_in;
                        break;
                    case kLengthFeet:
                        result = base * m_to_cm * cm_to_in * in_to_ft;
                        break;
                    case kLengthYards:
                        result = base * m_to_cm * cm_to_in * in_to_ft * ft_to_yd;
                        break;
                    case kLengthMiles:
                        result = base * m_to_cm * cm_to_in * in_to_ft * ft_to_mi;
                        break;
                break;
            case kAngle:
                switch (unitFrom) {
                    case kAngleRadians:
                        //base unit: radians
                        base = value;
                        break;
                    case kAngleDegrees:
                        base = value * deg_to_rad;
                        break;
                switch (unitTo) {
                    case kAngleRadians:
                        result = base;
                        break;
                    case kAngleDegrees:
                        result = base * rad_to_deg;
                        break;
                break;
            case kTemperature:
                switch (unitFrom) {
                    case kTemperatureDegreesC:
                        //base unit: degrees C
                        base = value;
                        break;
                    case kTemperatureDegreesF:
                        base = (value - 32.0) / 1.8;
                        break;
                switch (unitTo) {
                    case kTemperatureDegreesC:
                        result = base;
                        break;
                    case kTemperatureDegreesF:
                        result = base * 1.8 + 32.0;
                        break;
                break;
            case kMass:
                switch (unitFrom) {
                    case kMassMilligrams:
                        //base unit: milligrams
                        base = value * mg_to_g * g_to_kg;
                        break;
                    case kMassGrams:
                        base = value * g_to_kg;
                        break;
                    case kMassKilograms:
                        base = value;
                        break;
                    case kMassMetricTons:
                        base = value * t_to_kg;
                        break;
                    case kMassOunces:
                        base = value * oz_to_g * g_to_kg;
                        break;
                    case kMassPounds:
                        base = value * lb_to_oz * oz_to_g * g_to_kg;
                        break;
                    case kMassEnglishTons:
                        base = value * T_to_lb * lb_to_oz * oz_to_g * g_to_kg;
                        break;
                switch (unitTo) {
                    case kMassMilligrams:
                        result = base * kg_to_g * g_to_mg;
                        break;
                    case kMassGrams:
                        result = base * kg_to_g;
                        break;
                    case kMassKilograms:
                        result = base;
                        break;
                    case kMassMetricTons:
                        result = base * kg_to_t;
                        break;
                    case kMassOunces:
                        result = base * kg_to_g * g_to_oz;
                        break;
                    case kMassPounds:
                        result = base * kg_to_g * g_to_oz * oz_to_lb;
                        break;
                    case kMassEnglishTons:
                        result = base * kg_to_g * g_to_oz * oz_to_lb * lb_to_T;
                        break;
                break;
            case kArea:
                switch (unitFrom) {
                    case kAreaSquareMeters:
                        //base unit: square meters
                        base = value;
                        break;
                    case kAreaHectares:
                        base = value * ha_to_m2;
                        break;
                    case kAreaSquareKilometers:
                        base = value * km2_to_m2;
                        break;
                    case kAreaSquareFeet:
                        base = value * ft2_to_m2;
                        break;
                    case kAreaSquareYards:
                        base = value * yd2_to_ft2 * ft2_to_m2;
                        break;
                    case kAreaAcres:
                        base = value * ac_to_ft2 * ft2_to_m2;
                        break;
                    case kAreaSquareMiles:
                        base = value * mi2_to_ac * ac_to_ft2 * ft2_to_m2;
                        break;
                switch (unitTo) {
                    case kAreaSquareMeters:
                        result = base;
                        break;
                    case kAreaHectares:
                        result = base * m2_to_ha;
                        break;
                    case kAreaSquareKilometers:
                        result = base * m2_to_km2;
                        break;
                    case kAreaSquareFeet:
                        result = base * m2_to_ft2;
                        break;
                    case kAreaSquareYards:
                        result = base * m2_to_ft2 * ft2_to_yd2;
                        break;
                    case kAreaAcres:
                        result = base * m2_to_ft2 * ft2_to_ac;
                        break;
                    case kAreaSquareMiles:
                        result = base * m2_to_ft2 * ft2_to_ac * ac_to_mi2;
                        break;
                break;
            case kMassOverArea:
                switch (unitFrom) {
                    case kMassOverAreaKilogramsPHectare:
                        //base unit: kg/ha
                        base = value;
                        break;
                    case kMassOverAreaMetricTonsPHectare:
                        base = value * t_to_kg;
                        break;
                    case kMassOverAreaKilogramsPSquareMeter:
                        base = value / (m2_to_ha);
                        break;
                    case kMassOverAreaGramsPSquareMeter:
                        base = value * g_to_kg / (m2_to_ha);
                        break;
                    case kMassOverAreaGramsPSquareCentimeter:
                        base = value * g_to_kg / (cm2_to_m2 * m2_to_ha);
                        break;
                    case kMassOverAreaPoundsPAcre:
                        base = value * (lb_to_oz * oz_to_g * g_to_kg) / (ac_to_ft2 * ft2_to_m2 * m2_to_ha);
                        break;
                    case kMassOverAreaEnglishTonsPAcre:
                        base = value * (T_to_lb * lb_to_oz * oz_to_g * g_to_kg) / (ac_to_ft2 * ft2_to_m2 * m2_to_ha);
                        break;
                    case kMassOverAreaPoundsPSquareYard:
                        base = value * (lb_to_oz * oz_to_g * g_to_kg) / (yd2_to_ft2 * ft2_to_m2 * m2_to_ha);
                        break;
                    case kMassOverAreaPoundsPSquareFoot:
                        base = value * (lb_to_oz * oz_to_g * g_to_kg) / (ft2_to_m2 * m2_to_ha);
                        break;
                    case kMassOverAreaOuncesPSquareFoot:
                        base = value * (oz_to_g * g_to_kg) / (ft2_to_m2 * m2_to_ha);
                        break;
                switch (unitTo) {
                    case kMassOverAreaKilogramsPHectare:
                        result = base;
                        break;
                    case kMassOverAreaMetricTonsPHectare:
                        result = base * kg_to_t;
                        break;
                    case kMassOverAreaKilogramsPSquareMeter:
                        result = base / (ha_to_m2);
                        break;
                    case kMassOverAreaGramsPSquareMeter:
                        result = base * kg_to_g / (ha_to_m2);
                        break;
                    case kMassOverAreaGramsPSquareCentimeter:
                        result = base * kg_to_g / (ha_to_m2 * m2_to_cm2);
                        break;
                    case kMassOverAreaPoundsPAcre:
                        result = base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2 * ft2_to_ac);
                        break;
                    case kMassOverAreaEnglishTonsPAcre:
                        result = base * (kg_to_g * g_to_oz * oz_to_lb * lb_to_T) / (ha_to_m2 * m2_to_ft2 * ft2_to_ac);
                        break;
                    case kMassOverAreaPoundsPSquareYard:
                        result = base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2 * ft2_to_yd2);
                        break;
                    case kMassOverAreaPoundsPSquareFoot:
                        result = base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2);
                        break;
                    case kMassOverAreaOuncesPSquareFoot:
                        result = base * (kg_to_g * g_to_oz) / (ha_to_m2 * m2_to_ft2);
                        break;
                break;
            case kRadiation:
                switch (unitFrom) {
                    case kRadiationMegaJoulesPSquareMeter:
                        //base unit: MJ/m2
                        base = value;
                        break;
                    case kRadiationKilowattHoursPSquareMeter:
                        base = value * kWh_to_MJ;
                        break;
                    case kRadiationCaloriesPerSquareMeter:
                        base = value * cal_to_joule * joule_to_MJ;
                        break;
                    case kRadiationLangleys:
                        base = value * langleys_to_MJPm2;
                        break;
                    case kRadiationMegaJoulesPSquareFoot:
                        base = value / (ft2_to_m2);
                        break;
                    case kRadiationKilowattHoursPSquareFoot:
                        base = value * kWh_to_MJ / (ft2_to_m2);
                        break;
                    case kRadiationCaloriesPerSquareFoot:
                        base = value * cal_to_joule * joule_to_MJ / (ft2_to_m2);
                        break;
                switch (unitTo) {
                    case kRadiationMegaJoulesPSquareMeter:
                        result = base;
                        break;
                    case kRadiationKilowattHoursPSquareMeter:
                        result = base * MJ_to_kWh;
                        break;
                    case kRadiationCaloriesPerSquareMeter:
                        result = base * MJ_to_joule * joule_to_cal;
                        break;
                    case kRadiationLangleys:
                        result = base * MJPm2_to_langleys;
                        break;
                    case kRadiationMegaJoulesPSquareFoot:
                        result = base / (m2_to_ft2);
                        break;
                    case kRadiationKilowattHoursPSquareFoot:
                        result = base * MJ_to_kWh / (m2_to_ft2);
                        break;
                    case kRadiationCaloriesPerSquareFoot:
                        result = base * MJ_to_joule * joule_to_cal / (m2_to_ft2);
                        break;
                break;
            case kVolume:
                switch (unitFrom) {
                    case kVolumeLiters:
                        //base unit: liters
                        base = value;
                        break;
                    case kVolumeMilliliters:
                        base = value * ml_to_l;
                        break;
                    case kVolumeCubicMeters:
                        base = value * m3_to_l;
                        break;
                    case kVolumeQuarts:
                        base = value * qt_to_l;
                        break;
                    case kVolumeGallons:
                        base = value * gal_to_qt * qt_to_l;
                        break;
                    case kVolumeOunces:
                        base = value * floz_to_qt * qt_to_l;
                        break;
                switch (unitTo) {
                    case kVolumeLiters:
                        result = base;
                        break;
                    case kVolumeMilliliters:
                        result = base * l_to_ml;
                        break;
                    case kVolumeCubicMeters:
                        result = base * l_to_m3;
                        break;
                    case kVolumeQuarts:
                        result = base * l_to_qt;
                        break;
                    case kVolumeGallons:
                        result = base * l_to_qt * qt_to_gal;
                        break;
                    case kVolumeOunces:
                        result = base * l_to_qt * qt_to_floz;
                        break;
                break;
            case kDepthOfWater:
                switch (unitFrom) {
                    case kDepthOfWaterMillimeters:
                        //base unit: mm
                        base = value;
                        break;
                    case kDepthOfWaterInches:
                        base = value * in_to_cm * cm_to_mm;
                        break;
                switch (unitTo) {
                    case kDepthOfWaterMillimeters:
                        result = base;
                        break;
                    case kDepthOfWaterInches:
                        result = base * mm_to_cm * cm_to_in;
                        break;
                break;
            case kVelocity:
                switch (unitFrom) {
                    case kVelocityMetersPSecond:
                        //base unit: m/sec
                        base = value;
                        break;
                    case kVelocityMillimetersPHour:
                        base = value * mm_to_m / (hr_to_min * min_to_sec);
                        break;
                    case kVelocityMilesPHour:
                        base = value * (mi_to_ft * ft_to_in * in_to_cm * cm_to_m) / (hr_to_min * min_to_sec);
                        break;
                    case kVelocityFeetPSecond:
                        base = value * ft_to_in * in_to_cm * cm_to_m;
                        break;
                    case kVelocityInchesPHour:
                        base = value * (in_to_cm * cm_to_m) / (hr_to_min * min_to_sec);
                        break;
                switch (unitTo) {
                    case kVelocityMetersPSecond:
                        result = base;
                        break;
                    case kVelocityMillimetersPHour:
                        result = base * m_to_mm / (sec_to_min * min_to_hr);
                        break;
                    case kVelocityMilesPHour:
                        result = base * (m_to_cm * cm_to_in * in_to_ft * ft_to_mi) / (sec_to_min * min_to_hr);
                        break;
                    case kVelocityFeetPSecond:
                        result = base * m_to_cm * cm_to_in * in_to_ft;
                        break;
                    case kVelocityInchesPHour:
                        result = base * (m_to_cm * cm_to_in) / (sec_to_min * min_to_hr);
                        break;
                break;
            case kPressure:
                switch (unitFrom) {
                    case kPressurePascals:
                        //base unit: pascal
                        base = value;
                        break;
                    case kPressureKilopascals:
                        base = value * kPa_to_pa;
                        break;
                    case kPressureMegapascals:
                        base = value * MPa_to_kPa * kPa_to_pa;
                        break;
                    case kPressureKilogramsPSquareCentimeter:
                        base = value * (kg_to_g * g_to_oz * oz_to_lb / cm2_to_in2) * psi_to_pa;
                        break;
                    case kPressureAtmospheres:
                        base = value * atm_to_pa;
                        break;
                    case kPressureBars:
                        base = value * bars_to_pa;
                        break;
                    case kPressurePoundsPSquareInch:
                        base = value * psi_to_pa;
                        break;
                switch (unitTo) {
                    case kPressurePascals:
                        result = base;
                        break;
                    case kPressureKilopascals:
                        result = base * pa_to_kPa;
                        break;
                    case kPressureMegapascals:
                        result = base * pa_to_kPa * kPa_to_MPa;
                        break;
                    case kPressureKilogramsPSquareCentimeter:
                        result = base * pa_to_psi * (lb_to_oz * oz_to_g * g_to_kg / in2_to_cm2);
                        break;
                    case kPressureAtmospheres:
                        result = base * pa_to_atm;
                        break;
                    case kPressureBars:
                        result = base * pa_to_bars;
                        break;
                    case kPressurePoundsPSquareInch:
                        result = base * pa_to_psi;
                        break;
                break;
            case kDensity:
                switch (unitFrom) {
                    case kDensityMetricTonsPCubicMeter:
                        //base unit: t/m3
                        base = value;
                        break;
                    case kDensityGramsPCubicCentimeter:
                        base = value;
                        break;
                    case kDensityKilogramsPCubicMeter:
                        base = value * kg_to_t;
                        break;
                    case kDensityPoundsPCubicFoot:
                        base = value * (lb_to_oz * oz_to_g * g_to_kg * kg_to_t) / (ft3_to_m3);
                        break;
                    case kDensityPoundsPAcreFoot:
                        base = value * (lb_to_oz * oz_to_g * g_to_kg * kg_to_t) / (acft_to_ft3 * ft3_to_m3);
                        break;
                switch (unitTo) {
                    case kDensityMetricTonsPCubicMeter:
                        result = base;
                        break;
                    case kDensityGramsPCubicCentimeter:
                        result = base;
                        break;
                    case kDensityKilogramsPCubicMeter:
                        result = base * t_to_kg;
                        break;
                    case kDensityPoundsPCubicFoot:
                        result = base * (t_to_kg * kg_to_g * g_to_oz * oz_to_lb) / (m3_to_ft3);
                        break;
                    case kDensityPoundsPAcreFoot:
                        result = base * (t_to_kg * kg_to_g * g_to_oz * oz_to_lb) / (m3_to_ft3 * ft3_to_acft);
                        break;
                break;
            case kConcentration:
                switch (unitFrom) {
                    case kConcentrationGramsPMetricTon:
                        //base unit: g/t
                        base = value;
                        break;
                    case kConcentrationGramsPKilogram:
                        base = value / (kg_to_t);
                        break;
                    case kConcentrationMilligramsPMetricTon:
                        base = value * mg_to_g;
                        break;
                    case kConcentrationPoundsPEnglishTon:
                        base = value * (lb_to_oz * oz_to_g) / (T_to_lb * lb_to_oz * oz_to_g * g_to_kg * kg_to_t);
                        break;
                    case kConcentrationOuncesPEnglishTon:
                        base = value * (oz_to_g) / (T_to_lb * lb_to_oz * oz_to_g * g_to_kg * kg_to_t);
                        break;
                switch (unitTo) {
                    case kConcentrationGramsPMetricTon:
                        result = base;
                        break;
                    case kConcentrationGramsPKilogram:
                        result = base / (t_to_kg);
                        break;
                    case kConcentrationMilligramsPMetricTon:
                        result = base * g_to_mg;
                        break;
                    case kConcentrationPoundsPEnglishTon:
                        result = base * (g_to_oz * oz_to_lb) / (t_to_kg * kg_to_g * g_to_oz * oz_to_lb * lb_to_T);
                        break;
                    case kConcentrationOuncesPEnglishTon:
                        result = base * (g_to_oz) / (t_to_kg * kg_to_g * g_to_oz * oz_to_lb * lb_to_T);
                        break;
                break;
            default:
                //non changing unit
                result = value;
                break;
    } catch (EOverflow e) {
        result = usupport.kMaxSingle;
    } catch (EUnderflow e) {
        result = umath.kLowestFloatAboveZero;
    }
    return result;
}

public void LoadUnitsInSetIntoComboBox(TComboBox units, int unitSet) {
    int unitEnum = 0;
    String unitString = "";
    
    unitEnum = GetNextUnitEnumInUnitSet(unitSet, 0);
    if (unitEnum != 0) {
        unitString = UnitStringForEnum(unitSet, unitEnum);
        units.Items.Add(unitString);
        unitEnum = GetNextUnitEnumInUnitSet(unitSet, unitEnum);
        unitString = UnitStringForEnum(unitSet, unitEnum);
        units.Items.Add(unitString);
        while (unitEnum != 1) {
            unitEnum = GetNextUnitEnumInUnitSet(unitSet, unitEnum);
            if (unitEnum != 1) {
                unitString = UnitStringForEnum(unitSet, unitEnum);
                units.Items.Add(unitString);
            }
        }
    } else {
        units.Enabled = false;
    }
}

// if any unit set string in this function becomes longer than 12 chars, update constant at top of file 
public String UnitStringForEnum(int unitSetEnum, int unitEnum) {
    result = "";
    boolean problem = false;
    
    problem = false;
    result = "(no unit)";
    switch (unitSetEnum) {
        case kDimensionless:
            result = "(no unit)";
            break;
        case kLength:
            switch (unitEnum) {
                case kLengthMicrons:
                    result = "microns";
                    break;
                case kLengthMillimeters:
                    result = "mm";
                    break;
                case kLengthCentimeters:
                    result = "cm";
                    break;
                case kLengthMeters:
                    result = "m";
                    break;
                case kLengthKilometers:
                    result = "km";
                    break;
                case kLengthInches:
                    result = "in";
                    break;
                case kLengthFeet:
                    result = "ft";
                    break;
                case kLengthYards:
                    result = "yd";
                    break;
                case kLengthMiles:
                    result = "mi";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kAngle:
            switch (unitEnum) {
                case kAngleRadians:
                    result = "radians";
                    break;
                case kAngleDegrees:
                    result = "degrees";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kTemperature:
            switch (unitEnum) {
                case kTemperatureDegreesC:
                    result = "degrees C";
                    break;
                case kTemperatureDegreesF:
                    result = "degrees F";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kMass:
            switch (unitEnum) {
                case kMassMilligrams:
                    result = "mg";
                    break;
                case kMassGrams:
                    result = "g";
                    break;
                case kMassKilograms:
                    result = "kg";
                    break;
                case kMassMetricTons:
                    result = "t";
                    break;
                case kMassOunces:
                    result = "oz";
                    break;
                case kMassPounds:
                    result = "lb";
                    break;
                case kMassEnglishTons:
                    result = "T";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kArea:
            switch (unitEnum) {
                case kAreaHectares:
                    result = "ha";
                    break;
                case kAreaSquareMeters:
                    // superscript 2 is chr(178); superscript 3 is chr(179) 
                    result = "m2";
                    break;
                case kAreaSquareKilometers:
                    result = "km2";
                    break;
                case kAreaSquareFeet:
                    result = "ft2";
                    break;
                case kAreaSquareYards:
                    result = "yd2";
                    break;
                case kAreaAcres:
                    result = "ac";
                    break;
                case kAreaSquareMiles:
                    result = "mi2";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kMassOverArea:
            switch (unitEnum) {
                case kMassOverAreaKilogramsPHectare:
                    result = "kg/ha";
                    break;
                case kMassOverAreaMetricTonsPHectare:
                    result = "t/ha";
                    break;
                case kMassOverAreaKilogramsPSquareMeter:
                    result = "kg/m2";
                    break;
                case kMassOverAreaGramsPSquareMeter:
                    result = "g/m2";
                    break;
                case kMassOverAreaGramsPSquareCentimeter:
                    result = "g/cm2";
                    break;
                case kMassOverAreaPoundsPAcre:
                    result = "lb/ac";
                    break;
                case kMassOverAreaEnglishTonsPAcre:
                    result = "T/ac";
                    break;
                case kMassOverAreaPoundsPSquareYard:
                    result = "lb/yd2";
                    break;
                case kMassOverAreaPoundsPSquareFoot:
                    result = "lb/ft2";
                    break;
                case kMassOverAreaOuncesPSquareFoot:
                    result = "oz/ft2";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kRadiation:
            switch (unitEnum) {
                case kRadiationMegaJoulesPSquareMeter:
                    result = "MJ/m2";
                    break;
                case kRadiationKilowattHoursPSquareMeter:
                    result = "kWh/m2";
                    break;
                case kRadiationCaloriesPerSquareMeter:
                    result = "cal/m2";
                    break;
                case kRadiationLangleys:
                    result = "langleys";
                    break;
                case kRadiationMegaJoulesPSquareFoot:
                    result = "MJ/ft2";
                    break;
                case kRadiationKilowattHoursPSquareFoot:
                    result = "kWh/ft2";
                    break;
                case kRadiationCaloriesPerSquareFoot:
                    result = "cal/ft2";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kVolume:
            switch (unitEnum) {
                case kVolumeMilliliters:
                    result = "ml";
                    break;
                case kVolumeLiters:
                    result = "liters";
                    break;
                case kVolumeCubicMeters:
                    result = "m3";
                    break;
                case kVolumeQuarts:
                    result = "qt";
                    break;
                case kVolumeGallons:
                    result = "gal";
                    break;
                case kVolumeOunces:
                    result = "oz";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kDepthOfWater:
            switch (unitEnum) {
                case kDepthOfWaterMillimeters:
                    result = "mm (liquid)";
                    break;
                case kDepthOfWaterInches:
                    result = "in (liquid)";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kVelocity:
            switch (unitEnum) {
                case kVelocityMetersPSecond:
                    result = "m/sec";
                    break;
                case kVelocityMillimetersPHour:
                    result = "mm/hr";
                    break;
                case kVelocityMilesPHour:
                    result = "mi/hr";
                    break;
                case kVelocityFeetPSecond:
                    result = "ft/sec";
                    break;
                case kVelocityInchesPHour:
                    result = "in/hr";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kPressure:
            switch (unitEnum) {
                case kPressurePascals:
                    result = "Pa";
                    break;
                case kPressureKilopascals:
                    result = "kPa";
                    break;
                case kPressureMegapascals:
                    result = "MPa";
                    break;
                case kPressureKilogramsPSquareCentimeter:
                    result = "kg/cm2";
                    break;
                case kPressureAtmospheres:
                    result = "atm";
                    break;
                case kPressureBars:
                    result = "bars";
                    break;
                case kPressurePoundsPSquareInch:
                    result = "lb/in2";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kDensity:
            switch (unitEnum) {
                case kDensityGramsPCubicCentimeter:
                    result = "g/cm3";
                    break;
                case kDensityKilogramsPCubicMeter:
                    result = "kg/m3";
                    break;
                case kDensityMetricTonsPCubicMeter:
                    result = "t/m3";
                    break;
                case kDensityPoundsPCubicFoot:
                    result = "lb/ft3";
                    break;
                case kDensityPoundsPAcreFoot:
                    result = "lb/ac ft";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kConcentration:
            switch (unitEnum) {
                case kConcentrationGramsPMetricTon:
                    result = "g/t";
                    break;
                case kConcentrationGramsPKilogram:
                    result = "g/kg";
                    break;
                case kConcentrationMilligramsPMetricTon:
                    result = "mg/t";
                    break;
                case kConcentrationPoundsPEnglishTon:
                    result = "lb/T";
                    break;
                case kConcentrationOuncesPEnglishTon:
                    result = "oz/T";
                    break;
                default:
                    problem = true;
                    break;
            break;
        case kNonChangingUnitHundredsOfMolesPKilogram:
            result = "cmol/kg";
            break;
        case kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter:
            result = "kg/ha/MJ/m2";
            break;
        case kNonChangingUnitKiloPascalPDegreeC:
            result = "kPa/deg C";
            break;
        case kNonChangingUnitMegaJoulePKilogram:
            result = "MJ/kg";
            break;
        case kNonChangingUnitKilogramPKilogram:
            result = "kg/kg";
            break;
        case kNonChangingUnitMetersPMeter:
            result = "m/m";
            break;
        case kNonChangingUnitYears:
            result = "years";
            break;
        case kNonChangingUnitDays:
            result = "days";
            break;
        case kNonChangingUnitHours:
            result = "hours";
            break;
        case kNonChangingUnitPartsPMillion:
            result = "ppm";
            break;
        case kNonChangingUnitFraction:
            result = "fraction";
            break;
        case kNonChangingUnitPercent:
            result = "%";
            break;
        case kNonChangingUnitGramsPMetricTon:
            result = "g/t";
            break;
        case kNonChangingUnitCubicMetersPSecond:
            result = "m3/sec";
            break;
        case kNonChangingUnitBoolean:
            result = "True/False";
            break;
        default:
            result = "(no unit)";
            //  raise Exception.create('Unsupported unit set: ' + intToStr(unitSetEnum));  
            break;
    if (problem) {
        //  raise Exception.create('Unsupported unit ' + intToStr(unitEnum)
        //      + ' for unit set ' + intToStr(unitSetEnum)); 
        // PDF PORT -- added null statement
        null;
    }
    return result;
}

public int calcMaxUnitStringLengthForSet(int unitSet, int unitStart, int unitEnd) {
    result = 0;
    String unitString = "";
    int i = 0;
    
    result = 0;
    for (i = unitStart; i <= unitEnd; i++) {
        unitString = UnitStringForEnum(unitSet, i);
        if (len(unitString) > result) {
            result = len(unitString);
        }
    }
    return result;
}

public void setUpMaxUnitStringLengthsArray() {
    maxUnitStringLengths[kDimensionless] = len(UnitStringForEnum(kDimensionless, 0));
    maxUnitStringLengths[kLength] = calcMaxUnitStringLengthForSet(kLength, kLengthFirstUnit, kLengthLastUnit - 1);
    maxUnitStringLengths[kObsoleteLength] = calcMaxUnitStringLengthForSet(kLength, kLengthFirstUnit, kLengthLastUnit - 1);
    maxUnitStringLengths[kAngle] = calcMaxUnitStringLengthForSet(kAngle, kAngleFirstUnit, kAngleLastUnit - 1);
    maxUnitStringLengths[kTemperature] = calcMaxUnitStringLengthForSet(kTemperature, kTemperatureFirstUnit, kTemperatureLastUnit - 1);
    maxUnitStringLengths[kMass] = calcMaxUnitStringLengthForSet(kMass, kMassFirstUnit, kMassLastUnit - 1);
    maxUnitStringLengths[kObsoleteMass] = calcMaxUnitStringLengthForSet(kMass, kMassFirstUnit, kMassLastUnit - 1);
    maxUnitStringLengths[kArea] = calcMaxUnitStringLengthForSet(kArea, kAreaFirstUnit, kAreaLastUnit - 1);
    maxUnitStringLengths[kMassOverArea] = calcMaxUnitStringLengthForSet(kMassOverArea, kMassOverAreaFirstUnit, kMassOverAreaLastUnit - 1);
    maxUnitStringLengths[kRadiation] = calcMaxUnitStringLengthForSet(kRadiation, kRadiationFirstUnit, kRadiationLastUnit - 1);
    maxUnitStringLengths[kVolume] = calcMaxUnitStringLengthForSet(kVolume, kVolumeFirstUnit, kVolumeLastUnit - 1);
    maxUnitStringLengths[kDepthOfWater] = calcMaxUnitStringLengthForSet(kDepthOfWater, kDepthOfWaterFirstUnit, kDepthOfWaterLastUnit - 1);
    maxUnitStringLengths[kVelocity] = calcMaxUnitStringLengthForSet(kVelocity, kVelocityFirstUnit, kVelocityLastUnit - 1);
    maxUnitStringLengths[kPressure] = calcMaxUnitStringLengthForSet(kPressure, kPressureFirstUnit, kPressureLastUnit - 1);
    maxUnitStringLengths[kDensity] = calcMaxUnitStringLengthForSet(kDensity, kDensityFirstUnit, kDensityLastUnit - 1);
    maxUnitStringLengths[kConcentration] = calcMaxUnitStringLengthForSet(kConcentration, kConcentrationFirstUnit, kConcentrationLastUnit - 1);
    maxUnitStringLengths[kNonChangingUnitHundredsOfMolesPKilogram] = len(UnitStringForEnum(kNonChangingUnitHundredsOfMolesPKilogram, 0));
    maxUnitStringLengths[kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter] = len(UnitStringForEnum(kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter, 0));
    maxUnitStringLengths[kNonChangingUnitKiloPascalPDegreeC] = len(UnitStringForEnum(kNonChangingUnitKiloPascalPDegreeC, 0));
    maxUnitStringLengths[kNonChangingUnitMegaJoulePKilogram] = len(UnitStringForEnum(kNonChangingUnitMegaJoulePKilogram, 0));
    maxUnitStringLengths[kNonChangingUnitKilogramPKilogram] = len(UnitStringForEnum(kNonChangingUnitKilogramPKilogram, 0));
    maxUnitStringLengths[kNonChangingUnitMetersPMeter] = len(UnitStringForEnum(kNonChangingUnitMetersPMeter, 0));
    maxUnitStringLengths[kNonChangingUnitYears] = len(UnitStringForEnum(kNonChangingUnitYears, 0));
    maxUnitStringLengths[kNonChangingUnitDays] = len(UnitStringForEnum(kNonChangingUnitDays, 0));
    maxUnitStringLengths[kNonChangingUnitHours] = len(UnitStringForEnum(kNonChangingUnitHours, 0));
    maxUnitStringLengths[kNonChangingUnitPartsPMillion] = len(UnitStringForEnum(kNonChangingUnitPartsPMillion, 0));
    maxUnitStringLengths[kNonChangingUnitFraction] = len(UnitStringForEnum(kNonChangingUnitFraction, 0));
    maxUnitStringLengths[kNonChangingUnitPercent] = len(UnitStringForEnum(kNonChangingUnitPercent, 0));
    maxUnitStringLengths[kNonChangingUnitGramsPMetricTon] = len(UnitStringForEnum(kNonChangingUnitGramsPMetricTon, 0));
    maxUnitStringLengths[kNonChangingUnitCubicMetersPSecond] = len(UnitStringForEnum(kNonChangingUnitCubicMetersPSecond, 0));
    maxUnitStringLengths[kNonChangingUnitBoolean] = len(UnitStringForEnum(kNonChangingUnitBoolean, 0));
}

public int maxUnitStringLengthForSet(int unitSet) {
    result = 0;
    result = 0;
    if ((unitSet < kDimensionless) || (unitSet >= kLastUnitSet)) {
        throw new GeneralException.create("Problem: Unsupported unit set " + IntToStr(unitSet) + " in method maxUnitStringLengthForSet.");
    } else {
        result = maxUnitStringLengths[unitSet];
    }
    return result;
}

public int GetNextUnitEnumInUnitSet(int unitSet, int currentUnit) {
    result = 0;
    switch (unitSet) {
        case kDimensionless:
            result = 0;
            break;
        case kLength:
            if ((currentUnit == kLengthMiles)) {
                result = kLengthMicrons;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kAngle:
            if ((currentUnit == kAngleRadians)) {
                result = kAngleDegrees;
            } else {
                result = kAngleRadians;
            }
            break;
        case kTemperature:
            if ((currentUnit == kTemperatureDegreesC)) {
                result = kTemperatureDegreesF;
            } else {
                result = kTemperatureDegreesC;
            }
            break;
        case kMass:
            if ((currentUnit == kMassEnglishTons)) {
                result = kMassMilligrams;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kArea:
            if ((currentUnit == kAreaSquareMiles)) {
                result = kAreaHectares;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kMassOverArea:
            if ((currentUnit == kMassOverAreaOuncesPSquareFoot)) {
                result = kMassOverAreaKilogramsPHectare;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kRadiation:
            if ((currentUnit == kRadiationCaloriesPerSquareFoot)) {
                result = kRadiationMegaJoulesPSquareMeter;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kVolume:
            if ((currentUnit == kVolumeOunces)) {
                result = kVolumeMilliliters;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kDepthOfWater:
            if ((currentUnit == kDepthOfWaterInches)) {
                result = kDepthOfWaterMillimeters;
            } else {
                result = kDepthOfWaterInches;
            }
            break;
        case kVelocity:
            if ((currentUnit == kVelocityInchesPHour)) {
                result = kVelocityMetersPSecond;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kPressure:
            if ((currentUnit == kPressurePoundsPSquareInch)) {
                result = kPressurePascals;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kDensity:
            if ((currentUnit == kDensityPoundsPAcreFoot)) {
                result = kDensityGramsPCubicCentimeter;
            } else {
                result = currentUnit + 1;
            }
            break;
        case kConcentration:
            if ((currentUnit == kConcentrationOuncesPEnglishTon)) {
                result = kConcentrationGramsPMetricTon;
            } else {
                result = currentUnit + 1;
            }
            break;
        default:
            // non-changing unit set 
            result = currentUnit;
            break;
    return result;
}

public int GetPreviousUnitEnumInUnitSet(int unitSet, int currentUnit) {
    result = 0;
    switch (unitSet) {
        case kDimensionless:
            result = 0;
            break;
        case kLength:
            if ((currentUnit == kLengthMicrons)) {
                result = kLengthMiles;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kAngle:
            if ((currentUnit == kAngleRadians)) {
                // same as next 
                result = kAngleDegrees;
            } else {
                result = kAngleRadians;
            }
            break;
        case kTemperature:
            if ((currentUnit == kTemperatureDegreesC)) {
                // same as next 
                result = kTemperatureDegreesF;
            } else {
                result = kTemperatureDegreesC;
            }
            break;
        case kMass:
            if ((currentUnit == kMassMilligrams)) {
                result = kMassEnglishTons;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kArea:
            if ((currentUnit == kAreaHectares)) {
                result = kAreaSquareMiles;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kMassOverArea:
            if ((currentUnit == kMassOverAreaKilogramsPHectare)) {
                result = kMassOverAreaOuncesPSquareFoot;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kRadiation:
            if ((currentUnit == kRadiationMegaJoulesPSquareMeter)) {
                result = kRadiationCaloriesPerSquareFoot;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kVolume:
            if ((currentUnit == kVolumeMilliliters)) {
                result = kVolumeOunces;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kDepthOfWater:
            if ((currentUnit == kDepthOfWaterInches)) {
                // same as next 
                result = kDepthOfWaterMillimeters;
            } else {
                result = kDepthOfWaterInches;
            }
            break;
        case kVelocity:
            if ((currentUnit == kVelocityMetersPSecond)) {
                result = kVelocityInchesPHour;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kPressure:
            if ((currentUnit == kPressurePascals)) {
                result = kPressurePoundsPSquareInch;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kDensity:
            if ((currentUnit == kDensityGramsPCubicCentimeter)) {
                result = kDensityPoundsPAcreFoot;
            } else {
                result = currentUnit - 1;
            }
            break;
        case kConcentration:
            if ((currentUnit == kConcentrationGramsPMetricTon)) {
                result = kConcentrationOuncesPEnglishTon;
            } else {
                result = currentUnit - 1;
            }
            break;
        default:
            // non-changing unit set 
            result = currentUnit;
            break;
    return result;
}

public String GetUnitSetString(int unitSet) {
    result = "";
    switch (unitSet) {
        case kDimensionless:
            result = "kDimensionless";
            break;
        case kLength:
            result = "kLength";
            break;
        case kObsoleteLength:
            result = "kObsoleteLength";
            break;
        case kAngle:
            result = "kAngle";
            break;
        case kTemperature:
            result = "kTemperature";
            break;
        case kMass:
            result = "kMass";
            break;
        case kObsoleteMass:
            result = "kObsoleteMass";
            break;
        case kArea:
            result = "kArea";
            break;
        case kMassOverArea:
            result = "kMassOverArea";
            break;
        case kRadiation:
            result = "kRadiation";
            break;
        case kVolume:
            result = "kVolume";
            break;
        case kDepthOfWater:
            result = "kDepthOfWater";
            break;
        case kVelocity:
            result = "kVelocity";
            break;
        case kPressure:
            result = "kPressure";
            break;
        case kDensity:
            result = "kDensity";
            break;
        case kConcentration:
            result = "kConcentration";
            break;
        case kNonChangingUnitHundredsOfMolesPKilogram:
            result = "kNonChangingUnitHundredsOfMolesPKilogram";
            break;
        case kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter:
            result = "kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter";
            break;
        case kNonChangingUnitKiloPascalPDegreeC:
            result = "kNonChangingUnitKiloPascalPDegreeC";
            break;
        case kNonChangingUnitMegaJoulePKilogram:
            result = "kNonChangingUnitMegaJoulePKilogram";
            break;
        case kNonChangingUnitKilogramPKilogram:
            result = "kNonChangingUnitKilogramPKilogram";
            break;
        case kNonChangingUnitMetersPMeter:
            result = "kNonChangingUnitMetersPMeter";
            break;
        case kNonChangingUnitYears:
            result = "kNonChangingUnitYears";
            break;
        case kNonChangingUnitDays:
            result = "kNonChangingUnitDays";
            break;
        case kNonChangingUnitHours:
            result = "kNonChangingUnitHours";
            break;
        case kNonChangingUnitPartsPMillion:
            result = "kNonChangingUnitPartsPMillion";
            break;
        case kNonChangingUnitFraction:
            result = "kNonChangingUnitFraction";
            break;
        case kNonChangingUnitPercent:
            result = "kNonChangingUnitPercent";
            break;
        case kNonChangingUnitGramsPMetricTon:
            result = "kNonChangingUnitGramsPMetricTon";
            break;
        case kNonChangingUnitCubicMetersPSecond:
            result = "kNonChangingUnitCubicMetersPSecond";
            break;
        case kNonChangingUnitBoolean:
            result = "kNonChangingUnitBoolean";
            break;
        default:
            result = "";
            throw new GeneralException.create("Problem: Unsupported unit set " + IntToStr(unitSet) + " in method GetUnitSetString.");
            break;
    return result;
}

public String DisplayUnitSetString(int unitSet) {
    result = "";
    switch (unitSet) {
        case kDimensionless:
            result = "(no unit)";
            break;
        case kLength:
            result = "length (e.g., m)";
            break;
        case kObsoleteLength:
            result = "length (e.g., m)";
            break;
        case kAngle:
            result = "angle (degrees or radians)";
            break;
        case kTemperature:
            result = "temperature (degrees C or F)";
            break;
        case kMass:
            result = "mass (e.g., kg)";
            break;
        case kObsoleteMass:
            result = "mass (e.g., kg)";
            break;
        case kArea:
            result = "area (e.g., m2)";
            break;
        case kMassOverArea:
            result = "mass over area (e.g., kg/ha)";
            break;
        case kRadiation:
            result = "radiation (e.g., MJ/m2)";
            break;
        case kVolume:
            result = "volume (e.g., liters)";
            break;
        case kDepthOfWater:
            result = "depth of liquid (e.g., mm H20)";
            break;
        case kVelocity:
            result = "velocity (e.g., mm/hr)";
            break;
        case kPressure:
            result = "pressure (e.g. kPa)";
            break;
        case kDensity:
            result = "density (e.g., g/cm3)";
            break;
        case kConcentration:
            result = "concentration (e.g., g/t)";
            break;
        case kNonChangingUnitHundredsOfMolesPKilogram:
            result = "cmol/kg";
            break;
        case kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter:
            result = "MJ/m2";
            break;
        case kNonChangingUnitKiloPascalPDegreeC:
            result = "kPa/deg C";
            break;
        case kNonChangingUnitMegaJoulePKilogram:
            result = "MJ/kg";
            break;
        case kNonChangingUnitKilogramPKilogram:
            result = "kg/kg";
            break;
        case kNonChangingUnitMetersPMeter:
            result = "m/m";
            break;
        case kNonChangingUnitYears:
            result = "years";
            break;
        case kNonChangingUnitDays:
            result = "days";
            break;
        case kNonChangingUnitHours:
            result = "hours";
            break;
        case kNonChangingUnitPartsPMillion:
            result = "ppm";
            break;
        case kNonChangingUnitFraction:
            result = "fraction";
            break;
        case kNonChangingUnitPercent:
            result = "percent";
            break;
        case kNonChangingUnitGramsPMetricTon:
            result = "g/t";
            break;
        case kNonChangingUnitCubicMetersPSecond:
            result = "m3/sec";
            break;
        case kNonChangingUnitBoolean:
            result = "yes/no";
            break;
        default:
            result = "";
            throw new GeneralException.create("Problem: Unsupported unit set " + IntToStr(unitSet) + " in method DisplayUnitSetString.");
            break;
    return result;
}

public int GetLastUnitEnumInUnitSet(int unitSet) {
    result = 0;
    switch (unitSet) {
        case kDimensionless:
            result = 2;
            break;
        case kLength:
            result = kLengthLastUnit;
            break;
        case kObsoleteLength:
            result = kLengthLastUnit;
            break;
        case kAngle:
            result = kAngleLastUnit;
            break;
        case kTemperature:
            result = kTemperatureLastUnit;
            break;
        case kMass:
            result = kMassLastUnit;
            break;
        case kObsoleteMass:
            result = kMassLastUnit;
            break;
        case kArea:
            result = kAreaLastUnit;
            break;
        case kMassOverArea:
            result = kMassOverAreaLastUnit;
            break;
        case kRadiation:
            result = kRadiationLastUnit;
            break;
        case kVolume:
            result = kVolumeLastUnit;
            break;
        case kDepthOfWater:
            result = kDepthOfWaterLastUnit;
            break;
        case kVelocity:
            result = kVelocityLastUnit;
            break;
        case kPressure:
            result = kPressureLastUnit;
            break;
        case kDensity:
            result = kDensityLastUnit;
            break;
        case kConcentration:
            result = kConcentrationLastUnit;
            break;
        default:
            result = 2;
            break;
    return result;
}

public boolean unitIsMetric(int unitSetEnum, int unitEnum) {
    result = false;
    result = false;
    switch (unitSetEnum) {
        case kDimensionless:
            result = false;
            break;
        case kLength:
            switch (unitEnum) {
                case kLengthMicrons:
                    result = true;
                    break;
                case kLengthMillimeters:
                    result = true;
                    break;
                case kLengthCentimeters:
                    result = true;
                    break;
                case kLengthMeters:
                    result = true;
                    break;
                case kLengthKilometers:
                    result = true;
                    break;
            break;
        case kAngle:
            result = true;
            break;
        case kTemperature:
            if (unitEnum == kTemperatureDegreesC) {
                result = true;
            }
            break;
        case kMass:
            switch (unitEnum) {
                case kMassMilligrams:
                    result = true;
                    break;
                case kMassGrams:
                    result = true;
                    break;
                case kMassKilograms:
                    result = true;
                    break;
                case kMassMetricTons:
                    result = true;
                    break;
            break;
        case kArea:
            switch (unitEnum) {
                case kAreaHectares:
                    result = true;
                    break;
                case kAreaSquareMeters:
                    result = true;
                    break;
                case kAreaSquareKilometers:
                    result = true;
                    break;
            break;
        case kMassOverArea:
            switch (unitEnum) {
                case kMassOverAreaKilogramsPHectare:
                    result = true;
                    break;
                case kMassOverAreaMetricTonsPHectare:
                    result = true;
                    break;
                case kMassOverAreaKilogramsPSquareMeter:
                    result = true;
                    break;
                case kMassOverAreaGramsPSquareMeter:
                    result = true;
                    break;
                case kMassOverAreaGramsPSquareCentimeter:
                    result = true;
                    break;
            break;
        case kRadiation:
            switch (unitEnum) {
                case kRadiationMegaJoulesPSquareMeter:
                    result = true;
                    break;
                case kRadiationKilowattHoursPSquareMeter:
                    result = true;
                    break;
                case kRadiationCaloriesPerSquareMeter:
                    result = true;
                    break;
                case kRadiationLangleys:
                    result = true;
                    break;
            break;
        case kVolume:
            switch (unitEnum) {
                case kVolumeMilliliters:
                    result = true;
                    break;
                case kVolumeLiters:
                    result = true;
                    break;
                case kVolumeCubicMeters:
                    result = true;
                    break;
            break;
        case kDepthOfWater:
            if (unitEnum == kDepthOfWaterMillimeters) {
                result = true;
            }
            break;
        case kVelocity:
            switch (unitEnum) {
                case kVelocityMetersPSecond:
                    result = true;
                    break;
                case kVelocityMillimetersPHour:
                    result = true;
                    break;
            break;
        case kPressure:
            switch (unitEnum) {
                case kPressurePascals:
                    result = true;
                    break;
                case kPressureKilopascals:
                    result = true;
                    break;
                case kPressureMegapascals:
                    result = true;
                    break;
                case kPressureKilogramsPSquareCentimeter:
                    result = true;
                    break;
            break;
        case kDensity:
            switch (unitEnum) {
                case kDensityGramsPCubicCentimeter:
                    result = true;
                    break;
                case kDensityKilogramsPCubicMeter:
                    result = true;
                    break;
                case kDensityMetricTonsPCubicMeter:
                    result = true;
                    break;
            break;
        case kConcentration:
            switch (unitEnum) {
                case kConcentrationGramsPMetricTon:
                    result = true;
                    break;
                case kConcentrationGramsPKilogram:
                    result = true;
                    break;
                case kConcentrationMilligramsPMetricTon:
                    result = true;
                    break;
            break;
        case kNonChangingUnitHundredsOfMolesPKilogram:
            result = true;
            break;
        case kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter:
            result = true;
            break;
        case kNonChangingUnitKiloPascalPDegreeC:
            result = true;
            break;
        case kNonChangingUnitMegaJoulePKilogram:
            result = true;
            break;
        case kNonChangingUnitKilogramPKilogram:
            result = true;
            break;
        case kNonChangingUnitMetersPMeter:
            result = true;
            break;
        case kNonChangingUnitGramsPMetricTon:
            result = true;
            break;
        case kNonChangingUnitCubicMetersPSecond:
            result = true;
            break;
    return result;
}


