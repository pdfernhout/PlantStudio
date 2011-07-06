unit uunits;
{Copyright (c) 1997 Paul D. Fernhout and Cynthia F. Kurtz All rights reserved
http://www.gardenwithinsight.com. See the license file for details on redistribution.
=====================================================================================
uunits: Functions for conversion of units in whole system. There are 32 unit sets,
and each unit set contains units that are inter-convertible. For example, the
temperature unit set contains degrees C and degrees F. The unit set must be saved
and given during any conversion so the function knows which code to use to convert
the units. Numbers cannot be converted between unit sets. The file also contains
information for displaying the units (the string to show, etc).}

interface

uses StdCtrls;

function GetUnitSetString(unitSet: integer): string;
function DisplayUnitSetString(unitSet: integer): string;
function GetNextUnitEnumInUnitSet(unitSet: integer; currentUnit: integer): integer;
function GetPreviousUnitEnumInUnitSet(unitSet: integer; currentUnit: integer): integer;
function GetLastUnitEnumInUnitSet(unitSet: integer): integer;
function UnitStringForEnum(unitSetEnum: integer; unitEnum: integer): string;
function Convert(unitSet: integer; unitFrom: integer; unitTo: integer; value: single): single;
procedure LoadUnitsInSetIntoComboBox(units: TComboBox; unitSet: integer);
function maxUnitStringLengthForSet(unitSet: integer): integer;
function calcMaxUnitStringLengthForSet(unitSet, unitStart, unitEnd: integer): integer;
procedure setUpMaxUnitStringLengthsArray;
function unitIsMetric(unitSetEnum: integer; unitEnum: integer): boolean;

const
	kRangeOK = 0;
	kRangeTooLow = 1;
	kRangeTooHigh = 2;
	kRangeBounds = 3;
	kRangeMustBeInteger = 4;

  kDefaultFloatMin = -100000000000.0;
  kDefaultFloatMax = 100000000000.0;

  kMaxUnitStringLength = 12; { if change any unit string to make it longer than this, update } 

{ unit sets  }
const
  kDimensionless = 1;
  kLength = 2;
  kObsoleteLength = 3; { obsolete }
  kAngle = 4;
  kTemperature = 5;
  kMass = 6;  
  kObsoleteMass = 7;  { obsolete }
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

var
  maxUnitStringLengths: array[kDimensionless..kLastUnitSet] of integer;

{length (base unit: m) }
{ note: length used to be split into small and large,
  but these two have been combined so the user doesn't see them. }
const
  kLengthFirstUnit = 1;
  kLengthMicrons = 1;
  kLengthMillimeters = 2;
  kLengthCentimeters = 3;
  kLengthMeters = 4;
  kLengthKilometers = 5; { was inches }
  kLengthInches = 6;  { was feet }
  kLengthFeet = 7;  { was yards }
  kLengthYards = 8;  { was large meters }
  kLengthMiles = 9; { was large km }
  kLengthLastUnit = 10;
  { 10 was large yards }
  { 11 was large miles }

{ angle (base unit: radians)}
const
  kAngleFirstUnit = 1;
  kAngleRadians = 1;
  kAngleDegrees = 2;
  kAngleLastUnit = 3;

{ temperature (base unit: deg C)  }
const
  kTemperatureFirstUnit = 1;
  kTemperatureDegreesC = 1;
  kTemperatureDegreesF = 2;
  kTemperatureLastUnit = 3;

{ Mass (base unit: kg) (both small and large) }
{ note: these two have been combined so the user doesn't see them. }
const
  kMassFirstUnit = 1;
  kMassMilligrams = 1;
  kMassGrams = 2;
  kMassKilograms = 3;
  kMassMetricTons = 4;  { was ounces }
  kMassOunces = 5;      { was pounds }
  kMassPounds = 6;      { was large kg }
  kMassEnglishTons = 7; { was large metric tons }
  kMassLastUnit = 8;
  { 8 was large pounds }
  { 9 was large english tons }

{ area (base unit: m2)  }
const
  kAreaFirstUnit = 1;
  kAreaHectares = 1;
  kAreaSquareMeters = 2;
  kAreaSquareKilometers = 3;
  kAreaSquareFeet = 4;
  kAreaSquareYards = 5;
  kAreaAcres = 6;
  kAreaSquareMiles = 7;
  kAreaLastUnit = 8;

{ Mass over area (base unit: kg/ha) }
const
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

{ radiation (base unit: MJ/m2) }
const
  kRadiationFirstUnit = 1;
  kRadiationMegaJoulesPSquareMeter = 1;
  kRadiationKilowattHoursPSquareMeter = 2;
  kRadiationCaloriesPerSquareMeter = 3;
  kRadiationLangleys = 4;
  kRadiationMegaJoulesPSquareFoot = 5;
  kRadiationKilowattHoursPSquareFoot = 6;
  kRadiationCaloriesPerSquareFoot = 7;
  kRadiationLastUnit = 8;

{ volume (base unit: liter) }
const
  kVolumeFirstUnit = 1;
  kVolumeMilliliters = 1;
  kVolumeLiters = 2;
  kVolumeCubicMeters = 3;
  kVolumeQuarts = 4;
  kVolumeGallons = 5;
  kVolumeOunces = 6;
  kVolumeLastUnit = 7;
  
{ depth of water (precipitation) (base unit: mm) }
const
  kDepthOfWaterFirstUnit = 1;
  kDepthOfWaterMillimeters = 1;
  kDepthOfWaterInches = 2;
  kDepthOfWaterLastUnit = 3;

{ velocity (base unit: m/sec) }
const
  kVelocityFirstUnit = 1;
  kVelocityMetersPSecond = 1;
  kVelocityMillimetersPHour = 2;
  kVelocityMilesPHour = 3;
  kVelocityFeetPSecond = 4;
  kVelocityInchesPHour = 5;
  kVelocityLastUnit = 6;

{ pressure (base unit: Pa)}
const
  kPressureFirstUnit = 1;
  kPressurePascals = 1;
  kPressureKilopascals = 2;
  kPressureMegapascals = 3;
  kPressureKilogramsPSquareCentimeter = 4;
  kPressureAtmospheres = 5;
  kPressureBars = 6;
  kPressurePoundsPSquareInch = 7;
  kPressureLastUnit = 8;

{ density (base unit: g/cm3) (also concentration) }
const
  kDensityFirstUnit = 1;
  kDensityGramsPCubicCentimeter = 1;
  kDensityKilogramsPCubicMeter = 2;
  kDensityMetricTonsPCubicMeter = 3;
  kDensityPoundsPCubicFoot = 4;
  kDensityPoundsPAcreFoot = 5;
  kDensityLastUnit = 6;

{ concentration (base unit: g/t) }
const
  kConcentrationFirstUnit = 1;
  kConcentrationGramsPMetricTon = 1;
  kConcentrationGramsPKilogram = 2;
  kConcentrationMilligramsPMetricTon = 3;
  kConcentrationPoundsPEnglishTon = 4;
  kConcentrationOuncesPEnglishTon = 5;
  kConcentrationLastUnit = 6;

var
  { length }
  m_to_microns, microns_to_m,
  m_to_mm, mm_to_m,
  m_to_cm, cm_to_m,
  cm_to_mm, mm_to_cm,
  km_to_m, m_to_km,
  in_to_cm, cm_to_in,
  ft_to_in, in_to_ft,
  yd_to_ft, ft_to_yd,
  mi_to_ft, ft_to_mi,
  { mass }
  t_to_kg, kg_to_t,
  kg_to_g, g_to_kg,
  g_to_mg, mg_to_g,
  oz_to_g, g_to_oz,
  lb_to_oz, oz_to_lb,
  T_to_lb, lb_to_T,
  { area }
  ha_to_m2, m2_to_ha,
  km2_to_m2,  m2_to_km2,
  m2_to_cm2, cm2_to_m2,
  m2_to_ft2, ft2_to_m2,
  in2_to_cm2, cm2_to_in2,
  yd2_to_ft2, ft2_to_yd2,
  ac_to_ft2, ft2_to_ac,
  mi2_to_ac, ac_to_mi2,
  { energy }
  kWh_to_MJ, MJ_to_kWh,
  MJ_to_joule, joule_to_MJ,
  cal_to_joule, joule_to_cal,
  MJPm2_to_langleys, langleys_to_MJPm2,
  { volume }
  l_to_ml,  ml_to_l,
  m3_to_l,  l_to_m3,
  qt_to_l, l_to_qt,
  gal_to_qt, qt_to_gal,
  qt_to_floz, floz_to_qt,
  m3_to_ft3, ft3_to_m3,
  acft_to_ft3, ft3_to_acft,
  { pressure }
  kPa_to_pa, pa_to_kPa,
  MPa_to_kPa, kPa_to_MPa,
  psi_to_pa, pa_to_psi,
  atm_to_pa, pa_to_atm,
  bars_to_pa, pa_to_bars,
  { other }
  hr_to_min,  min_to_hr,
  min_to_sec, sec_to_min,
  rad_to_deg, deg_to_rad,
  frn_to_pct, pct_to_frn: single;

implementation

uses SysUtils, usupport, umath;

procedure setUnitConstants;
  begin
  { length }
  m_to_microns := 1000000.0; microns_to_m := 1.0 / m_to_microns;
  m_to_mm := 1000.0;         mm_to_m := 1.0 / m_to_mm;
  m_to_cm := 100.0;          cm_to_m := 1.0 / m_to_cm;
  cm_to_mm := 10.0;          mm_to_cm := 1.0 / cm_to_mm;
  km_to_m := 1000.0;         m_to_km := 1.0 / km_to_m;
  in_to_cm := 2.54;          cm_to_in := 1.0 / in_to_cm;
  ft_to_in := 12.0;          in_to_ft := 1.0 / ft_to_in;
  yd_to_ft := 3.0;           ft_to_yd := 1.0 / yd_to_ft;
  mi_to_ft := 5280.0;        ft_to_mi := 1.0 / mi_to_ft;
  { mass }
  t_to_kg := 1000.0;         kg_to_t := 1.0 / t_to_kg;
  kg_to_g := 1000.0;         g_to_kg := 1.0 / kg_to_g;
  g_to_mg := 1000.0;         mg_to_g := 1.0 / g_to_mg;
  oz_to_g := 28.35;          g_to_oz := 1.0 / oz_to_g;
  lb_to_oz := 16.0;          oz_to_lb := 1.0 / lb_to_oz;
  T_to_lb := 2000.0;         lb_to_T := 1.0 / T_to_lb;
  { area }
  ha_to_m2 := 10000.0;       m2_to_ha := 1.0 / ha_to_m2;
  km2_to_m2 := 1000000.0;    m2_to_km2 := 1.0 / km2_to_m2;
  m2_to_cm2 := 10000.0;      cm2_to_m2 := 1 / m2_to_cm2;
  m2_to_ft2 := 10.7639;      ft2_to_m2 := 1.0 / m2_to_ft2;
  in2_to_cm2 := 6.4516;      cm2_to_in2 := 1.0 / in2_to_cm2;
  yd2_to_ft2 := 9.0;         ft2_to_yd2 := 1.0 / yd2_to_ft2;
  ac_to_ft2 := 43560.0;      ft2_to_ac := 1.0 / ac_to_ft2;
  mi2_to_ac := 640.0;        ac_to_mi2 := 1.0 / mi2_to_ac;
  { energy }
  kWh_to_MJ := 3.6;          MJ_to_kWh := 1.0 / kWh_to_MJ;
  MJ_to_joule := 1000000.0;  joule_to_MJ := 1.0 / MJ_to_joule;
  cal_to_joule := 4.1868;    joule_to_cal := 1.0 / cal_to_joule;
  MJPm2_to_langleys := 23.8846; langleys_to_MJPm2 := 1.0 / MJPm2_to_langleys;
  { volume }
  l_to_ml := 1000.0;         ml_to_l := 1.0 / l_to_ml;
  m3_to_l := 1000.0;         l_to_m3 := 1.0 / m3_to_l;
  qt_to_l := 0.946;          l_to_qt := 1.0 / qt_to_l;
  gal_to_qt := 4.0;          qt_to_gal := 1.0 / gal_to_qt;
  qt_to_floz := 32.0;        floz_to_qt := 1.0 / qt_to_floz;
  m3_to_ft3 := 35.32;        ft3_to_m3 := 1.0 / m3_to_ft3;
  acft_to_ft3 := 43560.0;    ft3_to_acft := 1.0 / acft_to_ft3;
  { pressure }
  kPa_to_pa := 1000.0;       pa_to_kPa := 1.0 / kPa_to_pa;
  MPa_to_kPa := 1000.0;      kPa_to_MPa := 1.0 / MPa_to_kPa;
  psi_to_pa := 6894.76;      pa_to_psi := 1.0 / psi_to_pa;
  atm_to_pa := 101325.0;     pa_to_atm := 1.0 / atm_to_pa;
  bars_to_pa := 100000;      pa_to_bars := 1.0 / bars_to_pa;
  { other }
  hr_to_min := 60.0;         min_to_hr := 1.0 / hr_to_min;
  min_to_sec := 60.0;        sec_to_min := 1.0 / min_to_sec;
  rad_to_deg := 57.296;      deg_to_rad := 1.0 / rad_to_deg;
  frn_to_pct := 100.0;       pct_to_frn := 1.0 / frn_to_pct;
  end;

function Convert(unitSet: integer; unitFrom: integer; unitTo: integer; value: single): single;
  var
	  base: extended;
  begin
  base := 0.0;
  { default result to same value if something goes wrong }
  result := value;
  { if no conversion, exit }
  if (unitFrom = unitTo) or (value = kMaxSingle) or (value = kMinSingle) then
    exit;
  { special check for overflow (for bounds) to avoid exception-handling system }
  if value = kMaxSingle then
    begin
    result := kMaxSingle;
    exit;
    end;
  if value = -kMaxSingle then
    begin
    result := -kMaxSingle;
    exit;
    end;
  try
  case unitSet of
    kDimensionless: result := value;
    kLength:  
  	  begin
      {base unit: meters}
      case unitFrom of
        kLengthMicrons:      base := value * microns_to_m;
        kLengthMillimeters:  base := value * mm_to_m;
        kLengthCentimeters:  base := value * cm_to_m;
        kLengthMeters:       base := value;
        kLengthKilometers:   base := value * km_to_m;
        kLengthInches:       base := value * in_to_cm * cm_to_m;
        kLengthFeet:         base := value * ft_to_in * in_to_cm * cm_to_m;
        kLengthYards:        base := value * yd_to_ft * ft_to_in * in_to_cm * cm_to_m;
        kLengthMiles:        base := value * mi_to_ft * ft_to_in * in_to_cm * cm_to_m;
        end;
      case unitTo of
        kLengthMicrons:      result := base * m_to_microns;
        kLengthMillimeters:  result := base * m_to_mm;
        kLengthCentimeters:  result := base * m_to_cm;
        kLengthMeters:       result := base;
        kLengthKilometers:   result := base * m_to_km;
        kLengthInches:       result := base * m_to_cm * cm_to_in;
        kLengthFeet:         result := base * m_to_cm * cm_to_in * in_to_ft;
        kLengthYards:        result := base * m_to_cm * cm_to_in * in_to_ft * ft_to_yd;
        kLengthMiles:        result := base * m_to_cm * cm_to_in * in_to_ft * ft_to_mi;
        end;
      end;
    kAngle:
      begin
      {base unit: radians}
      case unitFrom of
        kAngleRadians: base := value;
        kAngleDegrees: base := value * deg_to_rad;
        end;
      case unitTo of
        kAngleRadians: result := base;
        kAngleDegrees: result := base * rad_to_deg;
        end;
      end;
    kTemperature:
      begin
      {base unit: degrees C}
      case unitFrom of
        kTemperatureDegreesC: base := value;
        kTemperatureDegreesF: base := (value - 32.0) / 1.8;
        end;
      case unitTo of
        kTemperatureDegreesC: result := base;
        kTemperatureDegreesF: result := base * 1.8 + 32.0;
        end;
      end;
    kMass:
      begin
      {base unit: milligrams}
      case unitFrom of
        kMassMilligrams: base := value * mg_to_g * g_to_kg;
        kMassGrams:      base := value * g_to_kg;
        kMassKilograms:  base := value;
        kMassMetricTons:   base := value * t_to_kg;
        kMassOunces:     base := value * oz_to_g * g_to_kg;
        kMassPounds:     base := value * lb_to_oz * oz_to_g * g_to_kg;
        kMassEnglishTons:  base := value * T_to_lb * lb_to_oz * oz_to_g * g_to_kg;
       end;
      case unitTo of
        kMassMilligrams: result := base * kg_to_g * g_to_mg;
        kMassGrams:      result := base * kg_to_g;
        kMassKilograms:  result := base;
        kMassMetricTons:   result := base * kg_to_t;
        kMassOunces:     result := base * kg_to_g * g_to_oz;
        kMassPounds:     result := base * kg_to_g * g_to_oz * oz_to_lb;
        kMassEnglishTons:  result := base * kg_to_g * g_to_oz * oz_to_lb * lb_to_T;
        end;
      end;
    kArea:
      begin
      {base unit: square meters}
      case unitFrom of
        kAreaSquareMeters:      base := value;
        kAreaHectares:          base := value * ha_to_m2;
        kAreaSquareKilometers:  base := value * km2_to_m2;
        kAreaSquareFeet:        base := value * ft2_to_m2;
        kAreaSquareYards:       base := value * yd2_to_ft2 * ft2_to_m2;
        kAreaAcres:             base := value * ac_to_ft2 * ft2_to_m2;   
        kAreaSquareMiles:       base := value * mi2_to_ac * ac_to_ft2 * ft2_to_m2;
        end;
      case unitTo of
        kAreaSquareMeters:      result := base;
        kAreaHectares:          result := base * m2_to_ha;
        kAreaSquareKilometers:  result := base * m2_to_km2;
        kAreaSquareFeet:        result := base * m2_to_ft2;
        kAreaSquareYards:       result := base * m2_to_ft2 * ft2_to_yd2;
        kAreaAcres:             result := base * m2_to_ft2 * ft2_to_ac;
        kAreaSquareMiles:       result := base * m2_to_ft2 * ft2_to_ac * ac_to_mi2;
        end;
      end;
    kMassOverArea:
      begin
      {base unit: kg/ha}
      case unitFrom of
        kMassOverAreaKilogramsPHectare:       base := value;
        kMassOverAreaMetricTonsPHectare:      base := value * t_to_kg;
        kMassOverAreaKilogramsPSquareMeter:   base := value / (m2_to_ha);
        kMassOverAreaGramsPSquareMeter:       base := value * g_to_kg / (m2_to_ha);
        kMassOverAreaGramsPSquareCentimeter:  base := value * g_to_kg / (cm2_to_m2 * m2_to_ha);
        kMassOverAreaPoundsPAcre:
          base := value * (lb_to_oz * oz_to_g * g_to_kg) / (ac_to_ft2 * ft2_to_m2 * m2_to_ha);
        kMassOverAreaEnglishTonsPAcre:
          base := value * (T_to_lb * lb_to_oz * oz_to_g * g_to_kg) / (ac_to_ft2 * ft2_to_m2 * m2_to_ha);
        kMassOverAreaPoundsPSquareYard:
          base := value * (lb_to_oz * oz_to_g * g_to_kg) / (yd2_to_ft2 * ft2_to_m2 * m2_to_ha);
        kMassOverAreaPoundsPSquareFoot:
          base := value * (lb_to_oz * oz_to_g * g_to_kg) / (ft2_to_m2 * m2_to_ha);
        kMassOverAreaOuncesPSquareFoot:
          base := value * (oz_to_g * g_to_kg) / (ft2_to_m2 * m2_to_ha);
        end;
      case unitTo of
        kMassOverAreaKilogramsPHectare:       result := base;
        kMassOverAreaMetricTonsPHectare:      result := base * kg_to_t;
        kMassOverAreaKilogramsPSquareMeter:   result := base / (ha_to_m2);
        kMassOverAreaGramsPSquareMeter:       result := base * kg_to_g / (ha_to_m2);
        kMassOverAreaGramsPSquareCentimeter:  result := base * kg_to_g / (ha_to_m2 * m2_to_cm2);
        kMassOverAreaPoundsPAcre:
          result := base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2 * ft2_to_ac);
        kMassOverAreaEnglishTonsPAcre:
          result := base * (kg_to_g * g_to_oz * oz_to_lb * lb_to_T) / (ha_to_m2 * m2_to_ft2 * ft2_to_ac);
        kMassOverAreaPoundsPSquareYard:
          result := base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2 * ft2_to_yd2);
        kMassOverAreaPoundsPSquareFoot:
          result := base * (kg_to_g * g_to_oz * oz_to_lb) / (ha_to_m2 * m2_to_ft2);
        kMassOverAreaOuncesPSquareFoot:
          result := base * (kg_to_g * g_to_oz) / (ha_to_m2 * m2_to_ft2);
        end;
      end;
    kRadiation:
      begin
      {base unit: MJ/m2}
      case unitFrom of
        kRadiationMegaJoulesPSquareMeter:     base := value;
        kRadiationKilowattHoursPSquareMeter:  base := value * kWh_to_MJ;
        kRadiationCaloriesPerSquareMeter:     base := value * cal_to_joule * joule_to_MJ;
        kRadiationLangleys:                   base := value * langleys_to_MJPm2;
        kRadiationMegaJoulesPSquareFoot:      base := value / (ft2_to_m2);
        kRadiationKilowattHoursPSquareFoot:   base := value * kWh_to_MJ / (ft2_to_m2);
        kRadiationCaloriesPerSquareFoot:      base := value * cal_to_joule * joule_to_MJ / (ft2_to_m2);
        end;
      case unitTo of
        kRadiationMegaJoulesPSquareMeter:     result := base;
        kRadiationKilowattHoursPSquareMeter:  result := base * MJ_to_kWh;
        kRadiationCaloriesPerSquareMeter:     result := base * MJ_to_joule * joule_to_cal;
        kRadiationLangleys:                   result := base * MJPm2_to_langleys;
        kRadiationMegaJoulesPSquareFoot:      result := base / (m2_to_ft2);
        kRadiationKilowattHoursPSquareFoot:   result := base * MJ_to_kWh / (m2_to_ft2);
        kRadiationCaloriesPerSquareFoot:      result := base * MJ_to_joule * joule_to_cal / (m2_to_ft2);
        end;
      end;
    kVolume:
      begin
      {base unit: liters}
      case unitFrom of
        kVolumeLiters:      base := value;
        kVolumeMilliliters: base := value * ml_to_l;
        kVolumeCubicMeters: base := value * m3_to_l;
        kVolumeQuarts:      base := value * qt_to_l;
        kVolumeGallons:     base := value * gal_to_qt * qt_to_l;
        kVolumeOunces:      base := value * floz_to_qt * qt_to_l;
        end;
      case unitTo of
        kVolumeLiters:      result := base;
        kVolumeMilliliters: result := base * l_to_ml;
        kVolumeCubicMeters: result := base * l_to_m3;
        kVolumeQuarts:      result := base * l_to_qt;
        kVolumeGallons:     result := base * l_to_qt * qt_to_gal;
        kVolumeOunces:      result := base * l_to_qt * qt_to_floz;
        end;
      end;
    kDepthOfWater:
      begin
      {base unit: mm}
      case unitFrom of
        kDepthOfWaterMillimeters: base := value;
        kDepthOfWaterInches:      base := value * in_to_cm * cm_to_mm;
        end;
      case unitTo of
        kDepthOfWaterMillimeters: result := base;
        kDepthOfWaterInches:      result := base * mm_to_cm * cm_to_in;
        end;
      end;
    kVelocity:
      begin
      {base unit: m/sec}
      case unitFrom of
        kVelocityMetersPSecond:     base := value;
        kVelocityMillimetersPHour:  base := value * mm_to_m / (hr_to_min * min_to_sec);
        kVelocityMilesPHour:
            base := value * (mi_to_ft * ft_to_in * in_to_cm * cm_to_m) / (hr_to_min * min_to_sec);
        kVelocityFeetPSecond:       base := value * ft_to_in * in_to_cm * cm_to_m;
        kVelocityInchesPHour:       base := value * (in_to_cm * cm_to_m) / (hr_to_min * min_to_sec);
        end;
      case unitTo of
        kVelocityMetersPSecond:     result := base;
        kVelocityMillimetersPHour:  result := base * m_to_mm / (sec_to_min * min_to_hr);
        kVelocityMilesPHour:
            result := base * (m_to_cm * cm_to_in * in_to_ft * ft_to_mi) / (sec_to_min * min_to_hr);
        kVelocityFeetPSecond:       result := base * m_to_cm * cm_to_in * in_to_ft;
        kVelocityInchesPHour:       result := base * (m_to_cm * cm_to_in) / (sec_to_min * min_to_hr);
        end;
      end;
    kPressure:
      begin
      {base unit: pascal}
      case unitFrom of
        kPressurePascals:                     base := value;
        kPressureKilopascals:                 base := value * kPa_to_pa;
        kPressureMegapascals:                 base := value * MPa_to_kPa * kPa_to_pa;
        kPressureKilogramsPSquareCentimeter:
            base := value * (kg_to_g * g_to_oz * oz_to_lb / cm2_to_in2) * psi_to_pa;
        kPressureAtmospheres:                 base := value * atm_to_pa;
        kPressureBars:                        base := value * bars_to_pa;
        kPressurePoundsPSquareInch:           base := value * psi_to_pa;
        end;
      case unitTo of
        kPressurePascals:                     result := base;
        kPressureKilopascals:                 result := base * pa_to_kPa;
        kPressureMegapascals:                 result := base * pa_to_kPa * kPa_to_MPa;
        kPressureKilogramsPSquareCentimeter:
            result := base * pa_to_psi * (lb_to_oz * oz_to_g * g_to_kg / in2_to_cm2);
        kPressureAtmospheres:                 result := base * pa_to_atm;
        kPressureBars:                        result := base * pa_to_bars;
        kPressurePoundsPSquareInch:           result := base * pa_to_psi;
        end;
      end;
    kDensity:
      begin
      {base unit: t/m3}
      case unitFrom of
        kDensityMetricTonsPCubicMeter:  base := value;
        kDensityGramsPCubicCentimeter:  base := value;
        kDensityKilogramsPCubicMeter:   base := value * kg_to_t;
        kDensityPoundsPCubicFoot:
            base := value * (lb_to_oz * oz_to_g * g_to_kg * kg_to_t) / (ft3_to_m3);
        kDensityPoundsPAcreFoot:
            base := value * (lb_to_oz * oz_to_g * g_to_kg * kg_to_t) / (acft_to_ft3 * ft3_to_m3);
        end;
      case unitTo of
        kDensityMetricTonsPCubicMeter:  result := base;
        kDensityGramsPCubicCentimeter:  result := base;
        kDensityKilogramsPCubicMeter:   result := base * t_to_kg;
        kDensityPoundsPCubicFoot:
            result := base * (t_to_kg * kg_to_g * g_to_oz * oz_to_lb) / (m3_to_ft3);
        kDensityPoundsPAcreFoot:
            result := base * (t_to_kg * kg_to_g * g_to_oz * oz_to_lb) / (m3_to_ft3 * ft3_to_acft);
        end;
      end;
    kConcentration:
      {base unit: g/t}
      begin
      case unitFrom of
        kConcentrationGramsPMetricTon:      base := value;
        kConcentrationGramsPKilogram:       base := value / (kg_to_t);
        kConcentrationMilligramsPMetricTon: base := value * mg_to_g;
        kConcentrationPoundsPEnglishTon:
            base := value * (lb_to_oz * oz_to_g) / (T_to_lb * lb_to_oz * oz_to_g * g_to_kg * kg_to_t);
         kConcentrationOuncesPEnglishTon:
            base := value * (oz_to_g) / (T_to_lb * lb_to_oz * oz_to_g * g_to_kg * kg_to_t);
        end;
      case unitTo of
        kConcentrationGramsPMetricTon:      result := base;
        kConcentrationGramsPKilogram:       result := base / (t_to_kg);
        kConcentrationMilligramsPMetricTon: result := base * g_to_mg;
        kConcentrationPoundsPEnglishTon:
            result := base * (g_to_oz * oz_to_lb) / (t_to_kg * kg_to_g * g_to_oz * oz_to_lb * lb_to_T);
        kConcentrationOuncesPEnglishTon:
            result := base * (g_to_oz) / (t_to_kg * kg_to_g * g_to_oz * oz_to_lb * lb_to_T);
        end;
      end;
	  else {non changing unit}
  	  result := value;
	  end;
  except
    on EOverflow do result := kMaxSingle;
    on EUnderflow do result := kLowestFloatAboveZero;
  end;
end;

procedure LoadUnitsInSetIntoComboBox(units: TComboBox; unitSet: integer);
  var
    unitEnum: integer;
    unitString: string;
  begin
  unitEnum := GetNextUnitEnumInUnitSet(unitSet, 0);
  if unitEnum <> 0 then
    begin
    unitString := UnitStringForEnum(unitSet, unitEnum);
    units.items.add(unitString);
    unitEnum := GetNextUnitEnumInUnitSet(unitSet, unitEnum);
    unitString := UnitStringForEnum(unitSet, unitEnum);
    units.items.add(unitString);
    while unitEnum <> 1 do
      begin
      unitEnum := GetNextUnitEnumInunitSet(unitSet, unitEnum);
      if unitEnum <> 1 then
        begin
        unitString := UnitStringForEnum(unitSet, unitEnum);
        units.items.add(unitString);
        end;
      end;
    end
  else
    units.enabled := false;
  end;

{ if any unit set string in this function becomes longer than 12 chars, update constant at top of file }
function UnitStringForEnum(unitSetEnum: integer; unitEnum: integer) : string;
  var problem: boolean;
  begin
  problem := false;
  result := '(no unit)';
  case unitSetEnum of
  kDimensionless: result := '(no unit)';
  kLength:
    case unitEnum of 
      kLengthMicrons: result := 'microns';
      kLengthMillimeters: result := 'mm';
      kLengthCentimeters: result := 'cm';
      kLengthMeters: result := 'm';
      kLengthKilometers: result := 'km';
      kLengthInches: result := 'in';
      kLengthFeet: result := 'ft';
      kLengthYards: result := 'yd';
      kLengthMiles: result := 'mi';
      else problem := true;
     end;
  kAngle:
    case unitEnum of
      kAngleRadians: result := 'radians';
      kAngleDegrees: result := 'degrees';
      else problem := true;
      end;
  kTemperature:
    case unitEnum of
      kTemperatureDegreesC: result := 'degrees C';
      kTemperatureDegreesF: result := 'degrees F';
      else problem := true;
      end;
  kMass:
    case unitEnum of
      kMassMilligrams: result := 'mg';
      kMassGrams: result := 'g';
      kMassKilograms: result := 'kg';
      kMassMetricTons: result := 't';
      kMassOunces: result := 'oz';
      kMassPounds: result := 'lb';
      kMassEnglishTons: result := 'T';
      else problem := true;
      end;
  kArea:
    case unitEnum of
      kAreaHectares: result := 'ha';
      { superscript 2 is chr(178); superscript 3 is chr(179) }
      kAreaSquareMeters: result := 'm2';  
      kAreaSquareKilometers: result := 'km2';
      kAreaSquareFeet: result := 'ft2';
      kAreaSquareYards: result := 'yd2';
      kAreaAcres: result := 'ac';
      kAreaSquareMiles: result := 'mi2';
      else problem := true;
      end;
  kMassOverArea:
    case unitEnum of 
      kMassOverAreaKilogramsPHectare: result := 'kg/ha';
      kMassOverAreaMetricTonsPHectare: result := 't/ha';
      kMassOverAreaKilogramsPSquareMeter: result := 'kg/m2';
      kMassOverAreaGramsPSquareMeter: result := 'g/m2';
      kMassOverAreaGramsPSquareCentimeter: result := 'g/cm2';
      kMassOverAreaPoundsPAcre: result := 'lb/ac';
      kMassOverAreaEnglishTonsPAcre: result := 'T/ac';
      kMassOverAreaPoundsPSquareYard: result := 'lb/yd2';
      kMassOverAreaPoundsPSquareFoot: result := 'lb/ft2';
      kMassOverAreaOuncesPSquareFoot: result := 'oz/ft2';
      else problem := true;
      end;
  kRadiation:
    case unitEnum of 
      kRadiationMegaJoulesPSquareMeter: result := 'MJ/m2';
      kRadiationKilowattHoursPSquareMeter: result := 'kWh/m2';
      kRadiationCaloriesPerSquareMeter: result := 'cal/m2';
      kRadiationLangleys: result := 'langleys';
      kRadiationMegaJoulesPSquareFoot: result := 'MJ/ft2';
      kRadiationKilowattHoursPSquareFoot: result := 'kWh/ft2';
      kRadiationCaloriesPerSquareFoot: result := 'cal/ft2';
      else problem := true;
      end;
  kVolume:
    case unitEnum of
      kVolumeMilliliters: result := 'ml';
      kVolumeLiters: result := 'liters';
      kVolumeCubicMeters: result := 'm3';
      kVolumeQuarts: result := 'qt';
      kVolumeGallons: result := 'gal';
      kVolumeOunces: result := 'oz';
      else problem := true;
      end;
  kDepthOfWater:
    case unitEnum of
      kDepthOfWaterMillimeters: result := 'mm (liquid)';
      kDepthOfWaterInches: result := 'in (liquid)';
      else problem := true;
      end;
  kVelocity:
    case unitEnum of
      kVelocityMetersPSecond: result := 'm/sec';
      kVelocityMillimetersPHour: result := 'mm/hr';
      kVelocityMilesPHour: result := 'mi/hr';
      kVelocityFeetPSecond: result := 'ft/sec';
      kVelocityInchesPHour: result := 'in/hr';
      else problem := true;
      end;
  kPressure:
    case unitEnum of 
      kPressurePascals: result := 'Pa';
      kPressureKilopascals: result := 'kPa';
      kPressureMegapascals: result := 'MPa';
      kPressureKilogramsPSquareCentimeter: result := 'kg/cm2';
      kPressureAtmospheres: result := 'atm';
      kPressureBars: result := 'bars';
      kPressurePoundsPSquareInch: result := 'lb/in2';
      else problem := true;
      end;
  kDensity:
    case unitEnum of
      kDensityGramsPCubicCentimeter: result := 'g/cm3';
      kDensityKilogramsPCubicMeter: result := 'kg/m3';
      kDensityMetricTonsPCubicMeter: result := 't/m3';
      kDensityPoundsPCubicFoot: result := 'lb/ft3';
      kDensityPoundsPAcreFoot: result := 'lb/ac ft';
      else problem := true;
      end;
  kConcentration:
    case unitEnum of
      kConcentrationGramsPMetricTon: result := 'g/t';
      kConcentrationGramsPKilogram: result := 'g/kg';
      kConcentrationMilligramsPMetricTon: result := 'mg/t';
      kConcentrationPoundsPEnglishTon: result := 'lb/T';
      kConcentrationOuncesPEnglishTon: result := 'oz/T';
      else problem := true;
      end;
    kNonChangingUnitHundredsOfMolesPKilogram: result := 'cmol/kg';
    kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter: result := 'kg/ha/MJ/m2';
    kNonChangingUnitKiloPascalPDegreeC: result := 'kPa/deg C';
    kNonChangingUnitMegaJoulePKilogram: result := 'MJ/kg';
    kNonChangingUnitKilogramPKilogram: result := 'kg/kg';
    kNonChangingUnitMetersPMeter: result := 'm/m';
    kNonChangingUnitYears: result := 'years';
    kNonChangingUnitDays: result := 'days';
    kNonChangingUnitHours: result := 'hours';
    kNonChangingUnitPartsPMillion: result := 'ppm';
    kNonChangingUnitFraction: result := 'fraction';
    kNonChangingUnitPercent: result := '%';
    kNonChangingUnitGramsPMetricTon: result := 'g/t';
    kNonChangingUnitCubicMetersPSecond: result := 'm3/sec';
    kNonChangingUnitBoolean: result := 'True/False';
  else
    begin
		result := '(no unit)';
  {  raise Exception.create('Unsupported unit set: ' + intToStr(unitSetEnum));  }
    end;
  end;
  if problem then
  {  raise Exception.create('Unsupported unit ' + intToStr(unitEnum)
      + ' for unit set ' + intToStr(unitSetEnum)); }
      // PDF PORT -- added null statement
      NIL;
  end;

function calcMaxUnitStringLengthForSet(unitSet, unitStart, unitEnd: integer): integer;
  var
    unitString: string[80];
    i: integer;
  begin
  result := 0;
  for i := unitStart to unitEnd do
    begin
    unitString := UnitStringForEnum(unitSet, i);
    if length(unitString) > result then result := length(unitString);
    end;
  end;

procedure setUpMaxUnitStringLengthsArray;
  begin
  maxUnitStringLengths[kDimensionless] := length(UnitStringForEnum(kDimensionless, 0));
  maxUnitStringLengths[kLength] := calcMaxUnitStringLengthForSet(kLength, kLengthFirstUnit, kLengthLastUnit-1);
  maxUnitStringLengths[kObsoleteLength] := calcMaxUnitStringLengthForSet(kLength, kLengthFirstUnit, kLengthLastUnit-1);
  maxUnitStringLengths[kAngle] := calcMaxUnitStringLengthForSet(kAngle, kAngleFirstUnit, kAngleLastUnit-1);
  maxUnitStringLengths[kTemperature] :=
    calcMaxUnitStringLengthForSet(kTemperature, kTemperatureFirstUnit, kTemperatureLastUnit-1);
  maxUnitStringLengths[kMass] := calcMaxUnitStringLengthForSet(kMass, kMassFirstUnit, kMassLastUnit-1);
  maxUnitStringLengths[kObsoleteMass] := calcMaxUnitStringLengthForSet(kMass, kMassFirstUnit, kMassLastUnit-1);
  maxUnitStringLengths[kArea] := calcMaxUnitStringLengthForSet(kArea, kAreaFirstUnit, kAreaLastUnit-1);
  maxUnitStringLengths[kMassOverArea] :=
    calcMaxUnitStringLengthForSet(kMassOverArea, kMassOverAreaFirstUnit, kMassOverAreaLastUnit-1);
  maxUnitStringLengths[kRadiation] := calcMaxUnitStringLengthForSet(kRadiation, kRadiationFirstUnit, kRadiationLastUnit-1);
  maxUnitStringLengths[kVolume] := calcMaxUnitStringLengthForSet(kVolume, kVolumeFirstUnit, kVolumeLastUnit-1);
  maxUnitStringLengths[kDepthOfWater] :=
    calcMaxUnitStringLengthForSet(kDepthOfWater, kDepthOfWaterFirstUnit, kDepthOfWaterLastUnit-1);
  maxUnitStringLengths[kVelocity] := calcMaxUnitStringLengthForSet(kVelocity, kVelocityFirstUnit, kVelocityLastUnit-1);
  maxUnitStringLengths[kPressure] := calcMaxUnitStringLengthForSet(kPressure, kPressureFirstUnit, kPressureLastUnit-1);
  maxUnitStringLengths[kDensity] := calcMaxUnitStringLengthForSet(kDensity, kDensityFirstUnit, kDensityLastUnit-1);
  maxUnitStringLengths[kConcentration] :=
    calcMaxUnitStringLengthForSet(kConcentration, kConcentrationFirstUnit, kConcentrationLastUnit-1);
  maxUnitStringLengths[kNonChangingUnitHundredsOfMolesPKilogram] :=
    length(UnitStringForEnum(kNonChangingUnitHundredsOfMolesPKilogram, 0));
  maxUnitStringLengths[kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter] :=
    length(UnitStringForEnum(kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter, 0));
  maxUnitStringLengths[kNonChangingUnitKiloPascalPDegreeC] :=
    length(UnitStringForEnum(kNonChangingUnitKiloPascalPDegreeC, 0));
  maxUnitStringLengths[kNonChangingUnitMegaJoulePKilogram] := length(UnitStringForEnum(kNonChangingUnitMegaJoulePKilogram, 0));
  maxUnitStringLengths[kNonChangingUnitKilogramPKilogram] := length(UnitStringForEnum(kNonChangingUnitKilogramPKilogram, 0));
  maxUnitStringLengths[kNonChangingUnitMetersPMeter] := length(UnitStringForEnum(kNonChangingUnitMetersPMeter, 0));
  maxUnitStringLengths[kNonChangingUnitYears] := length(UnitStringForEnum(kNonChangingUnitYears, 0));
  maxUnitStringLengths[kNonChangingUnitDays] := length(UnitStringForEnum(kNonChangingUnitDays, 0));
  maxUnitStringLengths[kNonChangingUnitHours] := length(UnitStringForEnum(kNonChangingUnitHours, 0));
  maxUnitStringLengths[kNonChangingUnitPartsPMillion] := length(UnitStringForEnum(kNonChangingUnitPartsPMillion, 0));
  maxUnitStringLengths[kNonChangingUnitFraction] := length(UnitStringForEnum(kNonChangingUnitFraction, 0));
  maxUnitStringLengths[kNonChangingUnitPercent] := length(UnitStringForEnum(kNonChangingUnitPercent, 0));
  maxUnitStringLengths[kNonChangingUnitGramsPMetricTon] := length(UnitStringForEnum(kNonChangingUnitGramsPMetricTon, 0));
  maxUnitStringLengths[kNonChangingUnitCubicMetersPSecond] := length(UnitStringForEnum(kNonChangingUnitCubicMetersPSecond, 0));
  maxUnitStringLengths[kNonChangingUnitBoolean] := length(UnitStringForEnum(kNonChangingUnitBoolean, 0));
  end;

function maxUnitStringLengthForSet(unitSet: integer): integer;
  begin
  result := 0;
  if (unitSet < kDimensionless) or (unitSet >= kLastUnitSet) then
    raise Exception.create('Problem: Unsupported unit set ' + intToStr(unitSet) + ' in method maxUnitStringLengthForSet.')
  else
    result := maxUnitStringLengths[unitSet];
  end;

function GetNextUnitEnumInUnitSet(unitSet: integer; currentUnit: integer): integer;
begin
case unitSet of
  kDimensionless:
    result := 0;
  kLength:
   if (currentUnit = kLengthMiles) then result := kLengthMicrons
   else result := currentUnit + 1;
  kAngle:
    if (currentUnit = kAngleRadians) then result := kAngleDegrees
    else result := kAngleRadians;
  kTemperature:
    if (currentUnit = kTemperatureDegreesC) then result := kTemperatureDegreesF
    else result := kTemperatureDegreesC;
  kMass:
    if (currentUnit = kMassEnglishTons) then result := kMassMilligrams
    else result := currentUnit + 1;
  kArea:
    if (currentUnit = kAreaSquareMiles) then result := kAreaHectares
    else result := currentUnit + 1;
  kMassOverArea:
    if (currentUnit = kMassOverAreaOuncesPSquareFoot) then result := kMassOverAreaKilogramsPHectare
    else result := currentUnit + 1;
  kRadiation:
    if (currentUnit = kRadiationCaloriesPerSquareFoot) then result := kRadiationMegaJoulesPSquareMeter
    else result := currentUnit + 1;
  kVolume:
    if (currentUnit = kVolumeOunces) then result := kVolumeMilliliters
    else result := currentUnit + 1;
  kDepthOfWater:
    if (currentUnit = kDepthOfWaterInches) then result := kDepthOfWaterMillimeters
    else result := kDepthOfWaterInches;
   kVelocity:
     if (currentUnit = kVelocityInchesPHour) then result := kVelocityMetersPSecond
    else result := currentUnit + 1;
   kPressure:
     if (currentUnit = kPressurePoundsPSquareInch) then result := kPressurePascals
    else result := currentUnit + 1;
   kDensity:
     if (currentUnit = kDensityPoundsPAcreFoot) then result := kDensityGramsPCubicCentimeter
    else result := currentUnit + 1;
   kConcentration:
     if (currentUnit = kConcentrationOuncesPEnglishTon) then result := kConcentrationGramsPMetricTon
     else result := currentUnit + 1;
   else  { non-changing unit set }
   	result := currentUnit;
   end;
end;

function GetPreviousUnitEnumInUnitSet(unitSet: integer; currentUnit: integer): integer;
begin
case unitSet of
  kDimensionless:
    result := 0;
  kLength:
   if (currentUnit = kLengthMicrons) then result := kLengthMiles
   else result := currentUnit - 1;
  kAngle:
    { same as next }
    if (currentUnit = kAngleRadians) then result := kAngleDegrees
    else result := kAngleRadians;
  kTemperature:
    { same as next }
    if (currentUnit = kTemperatureDegreesC) then result := kTemperatureDegreesF
    else result := kTemperatureDegreesC;
  kMass:
    if (currentUnit = kMassMilligrams) then result := kMassEnglishTons
    else result := currentUnit - 1;
  kArea:
    if (currentUnit = kAreaHectares) then result := kAreaSquareMiles
    else result := currentUnit - 1;
  kMassOverArea:
    if (currentUnit = kMassOverAreaKilogramsPHectare) then result := kMassOverAreaOuncesPSquareFoot
    else result := currentUnit - 1;
  kRadiation:
    if (currentUnit = kRadiationMegaJoulesPSquareMeter) then result := kRadiationCaloriesPerSquareFoot
    else result := currentUnit - 1;
  kVolume:
    if (currentUnit = kVolumeMilliliters) then result := kVolumeOunces
    else result := currentUnit - 1;
  kDepthOfWater:
    { same as next }
    if (currentUnit = kDepthOfWaterInches) then result := kDepthOfWaterMillimeters
    else result := kDepthOfWaterInches;
   kVelocity:
     if (currentUnit = kVelocityMetersPSecond) then result := kVelocityInchesPHour
    else result := currentUnit - 1;
   kPressure:
     if (currentUnit = kPressurePascals) then result := kPressurePoundsPSquareInch
    else result := currentUnit - 1;
   kDensity:
     if (currentUnit = kDensityGramsPCubicCentimeter) then result := kDensityPoundsPAcreFoot
    else result := currentUnit - 1;
   kConcentration:
     if (currentUnit = kConcentrationGramsPMetricTon) then result := kConcentrationOuncesPEnglishTon
     else result := currentUnit - 1;
   else  { non-changing unit set }
   	result := currentUnit;
   end;
end;

function GetUnitSetString(unitSet: integer): string;
	begin
  case unitSet of
  kDimensionless: result := 'kDimensionless';
  kLength: result := 'kLength';
  kObsoleteLength: result := 'kObsoleteLength';
  kAngle: result := 'kAngle';
  kTemperature: result := 'kTemperature';
  kMass: result := 'kMass';
  kObsoleteMass: result := 'kObsoleteMass';
  kArea: result := 'kArea';
  kMassOverArea: result := 'kMassOverArea';
  kRadiation: result := 'kRadiation';
  kVolume: result := 'kVolume';
  kDepthOfWater: result := 'kDepthOfWater';
  kVelocity: result := 'kVelocity';
  kPressure: result := 'kPressure';
  kDensity: result := 'kDensity';
  kConcentration: result := 'kConcentration';
  kNonChangingUnitHundredsOfMolesPKilogram: result := 'kNonChangingUnitHundredsOfMolesPKilogram';
  kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter: result := 'kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter';
  kNonChangingUnitKiloPascalPDegreeC: result := 'kNonChangingUnitKiloPascalPDegreeC';
  kNonChangingUnitMegaJoulePKilogram: result := 'kNonChangingUnitMegaJoulePKilogram';
  kNonChangingUnitKilogramPKilogram: result := 'kNonChangingUnitKilogramPKilogram';
  kNonChangingUnitMetersPMeter: result := 'kNonChangingUnitMetersPMeter';
  kNonChangingUnitYears: result := 'kNonChangingUnitYears';
  kNonChangingUnitDays: result := 'kNonChangingUnitDays';
  kNonChangingUnitHours: result := 'kNonChangingUnitHours';
  kNonChangingUnitPartsPMillion: result := 'kNonChangingUnitPartsPMillion';
  kNonChangingUnitFraction: result := 'kNonChangingUnitFraction';
  kNonChangingUnitPercent: result := 'kNonChangingUnitPercent';
  kNonChangingUnitGramsPMetricTon: result := 'kNonChangingUnitGramsPMetricTon';
  kNonChangingUnitCubicMetersPSecond: result := 'kNonChangingUnitCubicMetersPSecond';
  kNonChangingUnitBoolean: result := 'kNonChangingUnitBoolean';
  else
    begin
    result := '';
    raise Exception.create('Problem: Unsupported unit set ' + intToStr(unitSet) + ' in method GetUnitSetString.');
    end;
  end;
end;

function DisplayUnitSetString(unitSet: integer): string;
	begin
  case unitSet of
  kDimensionless: result := '(no unit)';
  kLength: result := 'length (e.g., m)';
  kObsoleteLength: result := 'length (e.g., m)';
  kAngle: result := 'angle (degrees or radians)';
  kTemperature: result := 'temperature (degrees C or F)';
  kMass: result := 'mass (e.g., kg)';
  kObsoleteMass: result := 'mass (e.g., kg)';
  kArea: result := 'area (e.g., m2)';
  kMassOverArea: result := 'mass over area (e.g., kg/ha)';
  kRadiation: result := 'radiation (e.g., MJ/m2)';
  kVolume: result := 'volume (e.g., liters)';
  kDepthOfWater: result := 'depth of liquid (e.g., mm H20)';
  kVelocity: result := 'velocity (e.g., mm/hr)';
  kPressure: result := 'pressure (e.g. kPa)';
  kDensity: result := 'density (e.g., g/cm3)';
  kConcentration: result := 'concentration (e.g., g/t)';
  kNonChangingUnitHundredsOfMolesPKilogram: result := 'cmol/kg';
  kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter: result := 'MJ/m2';
  kNonChangingUnitKiloPascalPDegreeC: result := 'kPa/deg C';
  kNonChangingUnitMegaJoulePKilogram: result := 'MJ/kg';
  kNonChangingUnitKilogramPKilogram: result := 'kg/kg';
  kNonChangingUnitMetersPMeter: result := 'm/m';
  kNonChangingUnitYears: result := 'years';
  kNonChangingUnitDays: result := 'days';
  kNonChangingUnitHours: result := 'hours';
  kNonChangingUnitPartsPMillion: result := 'ppm';
  kNonChangingUnitFraction: result := 'fraction';
  kNonChangingUnitPercent: result := 'percent';
  kNonChangingUnitGramsPMetricTon: result := 'g/t';
  kNonChangingUnitCubicMetersPSecond: result := 'm3/sec';
  kNonChangingUnitBoolean: result := 'yes/no';
  else
    begin
    result := '';
    raise Exception.create('Problem: Unsupported unit set ' + intToStr(unitSet) + ' in method DisplayUnitSetString.');
    end;
  end;
end;

function GetLastUnitEnumInUnitSet(unitSet: integer): integer;
	begin
  case unitSet of
    kDimensionless: result := 2;
    kLength: result := kLengthLastUnit;
    kObsoleteLength: result := kLengthLastUnit;
    kAngle: result := kAngleLastUnit;
    kTemperature: result := kTemperatureLastUnit;
    kMass: result := kMassLastUnit;
    kObsoleteMass: result := kMassLastUnit;
    kArea: result := kAreaLastUnit;
    kMassOverArea: result := kMassOverAreaLastUnit;
    kRadiation: result := kRadiationLastUnit;
    kVolume: result := kVolumeLastUnit;
    kDepthOfWater: result := kDepthOfWaterLastUnit;
    kVelocity: result := kVelocityLastUnit;
    kPressure: result := kPressureLastUnit;
    kDensity: result := kDensityLastUnit;
    kConcentration: result := kConcentrationLastUnit;
    else
      result := 2;
    end;
  end;

function unitIsMetric(unitSetEnum: integer; unitEnum: integer): boolean;
  begin
  result := false;
  case unitSetEnum of
    kDimensionless: result := false;
    kLength:
      case unitEnum of
        kLengthMicrons,
        kLengthMillimeters,
        kLengthCentimeters,
        kLengthMeters,
        kLengthKilometers:
          result := true;
        end;
    kAngle: result := true;
    kTemperature: if unitEnum = kTemperatureDegreesC then result := true;
    kMass:
      case unitEnum of
        kMassMilligrams,
        kMassGrams,
        kMassKilograms,
        kMassMetricTons:
          result := true;
        end;
    kArea:
      case unitEnum of
        kAreaHectares,
        kAreaSquareMeters,
        kAreaSquareKilometers:
          result := true;
        end;
    kMassOverArea:
      case unitEnum of
        kMassOverAreaKilogramsPHectare,
        kMassOverAreaMetricTonsPHectare,
        kMassOverAreaKilogramsPSquareMeter,
        kMassOverAreaGramsPSquareMeter,
        kMassOverAreaGramsPSquareCentimeter:
          result := true;
        end;
    kRadiation:
      case unitEnum of
        kRadiationMegaJoulesPSquareMeter,
        kRadiationKilowattHoursPSquareMeter,
        kRadiationCaloriesPerSquareMeter,
        kRadiationLangleys:
          result := true;
        end;
    kVolume:
      case unitEnum of
        kVolumeMilliliters,
        kVolumeLiters,
        kVolumeCubicMeters:
          result := true;
        end;
    kDepthOfWater: if unitEnum = kDepthOfWaterMillimeters then result := true;
    kVelocity:
      case unitEnum of
        kVelocityMetersPSecond,
        kVelocityMillimetersPHour:
          result := true;
        end;
    kPressure:
      case unitEnum of
        kPressurePascals,
        kPressureKilopascals,
        kPressureMegapascals,
        kPressureKilogramsPSquareCentimeter:
          result := true;
        end;
    kDensity:
      case unitEnum of
        kDensityGramsPCubicCentimeter,
        kDensityKilogramsPCubicMeter,
        kDensityMetricTonsPCubicMeter:
          result := true;
        end;
    kConcentration:
      case unitEnum of
        kConcentrationGramsPMetricTon,
        kConcentrationGramsPKilogram,
        kConcentrationMilligramsPMetricTon:
          result := true;
        end;
    kNonChangingUnitHundredsOfMolesPKilogram: result := true;
    kNonChangingUnitKilogramsPHectarePMegaJoulePSquareMeter: result := true;
    kNonChangingUnitKiloPascalPDegreeC: result := true;
    kNonChangingUnitMegaJoulePKilogram: result := true;
    kNonChangingUnitKilogramPKilogram: result := true;
    kNonChangingUnitMetersPMeter: result := true;
    kNonChangingUnitGramsPMetricTon: result := true;
    kNonChangingUnitCubicMetersPSecond: result := true;
    end;
  end;

begin
setUnitConstants; 
setUpMaxUnitStringLengthsArray;
end.
