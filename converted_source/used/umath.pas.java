// unit umath

from conversion_common import *;
import uparams;
import usstream;
import uunits;
import usupport;
import delphi_compatability;

// record
class SCurveStructure {
    public float x1;
    public float y1;
    public float x2;
    public float y2;
    public float c1;
    public float c2;
}

// const
kPi = 3.141596;
kLowestFloatAboveZero = 10e-12;
kLowestQuantityFloat = 10e-6;


// const
kGetField = 0;
kSetField = 1;


//returns zero for convenience
//these consts are really defined in uplant.pas but we don't want to include it - keep current
// error message - returns zero for convenience
public float ErrorMessage(String errorString) {
    result = 0.0;
    result = 0.0;
    UNRESOLVED.DebugPrint(errorString);
    return result;
}

// ---------------------------------------------------------------------------------------------- math functions 
public float sqr(float x) {
    result = 0.0;
    result = x * x;
    return result;
}

public float min(float a, float b) {
    result = 0.0;
    if ((a < b)) {
        result = a;
    } else {
        result = b;
    }
    return result;
}

public float max(float a, float b) {
    result = 0.0;
    if ((a > b)) {
        result = a;
    } else {
        result = b;
    }
    return result;
}

public int intMin(int a, int b) {
    result = 0;
    if ((a < b)) {
        result = a;
    } else {
        result = b;
    }
    return result;
}

public int intMax(int a, int b) {
    result = 0;
    if ((a > b)) {
        result = a;
    } else {
        result = b;
    }
    return result;
}

// RE-RAISES EXCEPTION 
public double pow(double number, double exponent) {
    result = 0.0;
    try {
        result = safeExp(exponent * safeLn(number));
    } catch (Exception e) {
        ErrorMessage("Invalid number for power function: " + FloatToStr(number) + " to the power " + FloatToStr(exponent));
        result = 1.0;
        throw new Exception();
    }
    return result;
}

// this function is needed to get around a bug in the development environment: if a negative
//number is raised to a non-integer power, an exception should be raised but the environment
//instead crashes. 
// RE-RAISES EXCEPTION 
public double power(double number, double exponent) {
    result = 0.0;
    try {
        if ((number > 0.0)) {
            result = pow(number, exponent);
        } else if ((number == 0.0)) {
            if (exponent == 0.0) {
                result = 1.0;
                throw new GeneralException.create("Problem: Zero raised to zero power.");
            } else {
                result = 0.0;
            }
        } else {
            result = 0.0;
            throw new GeneralException.create("Problem: Negative number to non-integer power: " + FloatToStr(number) + " to " + FloatToStr(exponent));
        }
    } catch (Exception e) {
        result = ErrorMessage("Problem: Uncaught error in power function: " + FloatToStr(number) + " to " + FloatToStr(exponent));
        throw new Exception();
    }
    return result;
}

// RE-RAISES EXCEPTION 
public double tan(double x) {
    result = 0.0;
    try {
        result = sin(x) / cos(x);
    } catch (Exception e) {
        result = ErrorMessage("Uncaught error in tangent function: " + FloatToStr(x));
        throw new Exception();
    }
    return result;
}

// RE-RAISES EXCEPTION 
public double arcCos(double x) {
    result = 0.0;
    try {
        // this was in the Delphi help but doesn't seem to work 
        // result := arcTan(sqrt(1.0 - sqr(x)) / x); 
        // from Smalltalk/V 
        result = kPi / 2.0 - arcSin(x);
    } catch (Exception e) {
        result = ErrorMessage("Invalid number for arcCos: " + FloatToStr(x));
        throw new Exception();
    }
    return result;
}

// RE-RAISES EXCEPTION 
public double arcSin(double x) {
    result = 0.0;
    try {
        result = arctan(x / sqrt(1.0 - sqr(x)));
    } catch (Exception e) {
        result = ErrorMessage("Invalid number for arcSin: " + FloatToStr(x));
        throw new Exception();
    }
    return result;
}

// const
oneOverNaturalLogOfTen = 0.434294481;


// RE-RAISES EXCEPTION 
// uses notion that logN(x) = ln(x) / ln(N) 
public double log10(double x) {
    result = 0.0;
    try {
        if (x > 0.0) {
            result = oneOverNaturalLogOfTen * safeLn(x);
        } else {
            result = -1;
            throw new GeneralException.create("Problem: Tried to take log (base 10) of zero or negative number.");
        }
    } catch (Exception e) {
        result = ErrorMessage("Problem: Invalid number for log (base 10): " + FloatToStr(x) + ".");
        throw new Exception();
    }
    return result;
}

// RE-RAISES EXCEPTION 
public double safeLn(double x) {
    result = 0.0;
    if (x > 0.0) {
        try {
            // PDF PORT added semicolon
            result = UNRESOLVED.ln(x);
        } catch (Exception e) {
            ErrorMessage("Invalid number for natural log: " + FloatToStr(x));
            result = 1.0;
            throw new Exception();
        }
    } else {
        throw new GeneralException.create("Problem: Tried to take ln of zero or negative number: " + FloatToStr(x) + ".");
    }
    return result;
}

// same as safeLn but does not show an errorMessage or re-raise the exception; just returns whether it failed;
//  used inside paint methods where you don't want error dialogs popping up 
public double safeLnWithResult(double x, boolean failed) {
    raise "method safeLnWithResult with preexisting function result had var parameters added to return; fixup manually"
    result = 0.0;
    double temp = 0.0;
    
    failed = true;
    result = 0.0;
    temp = 0.0;
    if (x <= 0.0) {
        return result, failed;
    }
    try {
        temp = UNRESOLVED.ln(x);
    } catch (Exception e) {
        result = 1.0;
        return result, failed;
    }
    result = temp;
    failed = false;
    return result, failed;
}

// RE-RAISES EXCEPTION 
public double safeExp(double x) {
    result = 0.0;
    try {
        // PDF PORT added semicolon
        result = UNRESOLVED.exp(x);
    } catch (Exception e) {
        result = ErrorMessage("Invalid number for exponential function: " + FloatToStr(x));
        throw new Exception();
    }
    return result;
}

// same as safeExp but does not show an errorMessage or re-raise the exception; just returns whether it failed;
//  used inside paint methods where you don't want error dialogs popping up 
public double safeExpWithResult(double x, boolean failed) {
    raise "method safeExpWithResult with preexisting function result had var parameters added to return; fixup manually"
    result = 0.0;
    double temp = 0.0;
    
    failed = true;
    result = 0.0;
    temp = 0.0;
    try {
        temp = UNRESOLVED.exp(x);
    } catch (Exception e) {
        return result, failed;
    }
    result = temp;
    failed = false;
    return result, failed;
}

//this function catches a divide by zero before it produces a not-a-number.
//this can happen because of an underflow, an error in the code, or an unexpected condition.
//this is a different approach than EPIC's which is basically to divide by the number plus a tiny float
//for all cases (like 1e-20 or 1e-10)
// RE-RAISES EXCEPTION 
public float safediv(float x, float y) {
    result = 0.0;
    try {
        if ((y != 0.0)) {
            result = x / y;
        } else {
            result = 0.0;
            throw new GeneralException.create("Problem: Divide by zero.");
        }
    } catch (Exception e) {
        result = ErrorMessage("Problem: Unspecified problem with dividing " + FloatToStr(x) + " by " + FloatToStr(y) + ".");
        throw new Exception();
    }
    return result;
}

// RE-RAISES EXCEPTION 
// same as safediv except that the user specifies what to return if the denominator is zero 
public float safedivExcept(float x, float y, float exceptionResult) {
    result = 0.0;
    try {
        if ((y != 0.0)) {
            result = x / y;
        } else {
            result = exceptionResult;
        }
    } catch (Exception e) {
        result = ErrorMessage("Problem in dividing " + FloatToStr(x) + " by " + FloatToStr(y));
        throw new Exception();
    }
    return result;
}

// same as safediv but does not show an errorMessage or re-raise the exception; just returns whether it failed;
//  used inside paint methods where you don't want error dialogs popping up 
public float safedivWithResult(float x, float y, boolean failed) {
    raise "method safedivWithResult with preexisting function result had var parameters added to return; fixup manually"
    result = 0.0;
    double temp = 0.0;
    
    failed = true;
    result = 0.0;
    temp = 0.0;
    if (y == 0.0) {
        return result, failed;
    }
    try {
        temp = x / y;
    } catch (Exception e) {
        return result, failed;
    }
    result = temp;
    failed = false;
    return result, failed;
}

// s curves 
// RE-RAISES EXCEPTION 
// this function carries out a structure found in many EPIC equations. 
public double scurve(double x, double c1, double c2) {
    result = 0.0;
    double temp = 0.0;
    
    try {
        temp = c1 - c2 * x;
        if (temp > 85.0) {
            temp = 85.0;
            throw new GeneralException.create("Problem: Exponent of number would have gone out of float range.");
        }
        result = safediv(x, x + safeExp(temp));
    } catch (Exception e) {
        result = ErrorMessage("Problem in s curve: numbers are " + FloatToStr(x) + ", " + FloatToStr(c1) + ", and " + FloatToStr(c2));
        throw new Exception();
    }
    return result;
}

// same as scurve but does not show an errorMessage or re-raise the exception; just returns whether it failed;
//  used inside paint methods where you don't want error dialogs popping up 
public double scurveWithResult(double x, double c1, double c2, boolean failed) {
    raise "method scurveWithResult with preexisting function result had var parameters added to return; fixup manually"
    result = 0.0;
    double temp = 0.0;
    
    failed = true;
    result = 0.0;
    temp = 0.0;
    try {
        temp = c1 - c2 * x;
        if (temp > 85.0) {
            return result, failed;
        }
        temp = safeExpWithResult(temp, failed);
        if (failed) {
            return result, failed;
        }
        temp = safedivWithResult(x, x + temp, failed);
        if (failed) {
            return result, failed;
        }
    } catch (Exception e) {
        return result, failed;
    }
    failed = false;
    result = temp;
    return result, failed;
}

// s curve params 
// RE-RAISES EXCEPTION 
// deal with zero s curve values by defaulting whole curve to hard-coded values
public void calcSCurveCoeffs(SCurveStructure sCurve) {
    double xx = 0.0;
    
    try {
        if ((sCurve.x1 <= 0.0) || (sCurve.y1 <= 0.0) || (sCurve.x2 <= 0.0) || (sCurve.y2 <= 0.0) || (sCurve.x1 >= 1.0) || (sCurve.y1 >= 1.0) || (sCurve.x2 >= 1.0) || (sCurve.y2 >= 1.0)) {
            // instead of raising exception, just hard-code whole curve to acceptable values
            // don't use Parameters.tab default in case that was read in wrong also
            sCurve.x1 = 0.25;
            sCurve.y1 = 0.1;
            sCurve.x2 = 0.65;
            sCurve.y2 = 0.85;
        }
        xx = safeLn(safediv(sCurve.x1, sCurve.y1) - sCurve.x1);
        sCurve.c2 = safediv((xx - safeLn(safediv(sCurve.x2, sCurve.y2) - sCurve.x2)), sCurve.x2 - sCurve.x1);
        sCurve.c1 = xx + sCurve.x1 * sCurve.c2;
    } catch (Exception e) {
        // set s curve to all acceptable values - safest 
        sCurve.x1 = 0.25;
        sCurve.y1 = 0.1;
        sCurve.x2 = 0.65;
        sCurve.y2 = 0.85;
        throw new Exception();
    }
}

// same as Utils_CalcSCurveCoeffs but does not show an errorMessage or re-raise the exception;
//  just returns whether it failed; used inside paint methods where you don't want error dialogs popping up 
public void calcSCurveCoeffsWithResult(SCurveStructure sCurve, boolean failed) {
    double quotientX1Y1 = 0.0;
    double lnQuotientX1Y1MinusX1 = 0.0;
    double quotientX2Y2 = 0.0;
    double lnQuotientX2Y2MinusX2 = 0.0;
    double c1temp = 0.0;
    double c2temp = 0.0;
    
    failed = true;
    try {
        quotientX1Y1 = safedivWithResult(sCurve.x1, sCurve.y1, failed);
        if (failed) {
            return failed;
        }
        lnQuotientX1Y1MinusX1 = safeLnWithResult(quotientX1Y1 - sCurve.x1, failed);
        if (failed) {
            return failed;
        }
        quotientX2Y2 = safedivWithResult(sCurve.x2, sCurve.y2, failed);
        if (failed) {
            return failed;
        }
        lnQuotientX2Y2MinusX2 = safeLnWithResult(quotientX2Y2 - sCurve.x2, failed);
        if (failed) {
            return failed;
        }
        c2temp = safedivWithResult(lnQuotientX1Y1MinusX1 - lnQuotientX2Y2MinusX2, sCurve.x2 - sCurve.x1, failed);
        if (failed) {
            return failed;
        }
        c1temp = lnQuotientX1Y1MinusX1 + sCurve.x1 * c2temp;
    } catch (Exception e) {
        return failed;
    }
    sCurve.c1 = c1temp;
    sCurve.c2 = c2temp;
    failed = false;
    return failed;
}

public void transferSCurveValue(int direction, sCurveStructure param, int index, FIX_MISSING_ARG_TYPE value) {
    if ((direction == kGetField)) {
        switch (index) {
            case 0:
                value = param.x1;
                break;
            case 1:
                value = param.y1;
                break;
            case 2:
                value = param.x2;
                break;
            case 3:
                value = param.y2;
                break;
    } else {
        switch (index) {
            case 0:
                // direction == kSetField 
                param.x1 = value;
                break;
            case 1:
                param.y1 = value;
                break;
            case 2:
                param.x2 = value;
                break;
            case 3:
                param.y2 = value;
                break;
    }
    return value;
}

public SCurveStructure stringToSCurve(String aString) {
    result = new SCurveStructure();
    KfStringStream stream = new KfStringStream();
    
    result.x1 = 0;
    result.y1 = 0;
    result.x2 = 0;
    result.y2 = 0;
    result.c1 = 0;
    result.c2 = 0;
    // format is x1 y1 x2 y2 
    stream = usstream.KfStringStream.create;
    try {
        stream.onStringSeparator(aString, " ");
        result.x1 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat, result.x1);
        result.y1 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat, result.y1);
        result.x2 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat, result.x2);
        result.y2 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat, result.y2);
    } finally {
        stream.free;
    }
    return result;
}

public String sCurveToString(SCurveStructure sCurve) {
    result = "";
    result = usupport.digitValueString(sCurve.x1) + " " + usupport.digitValueString(sCurve.y1) + " " + usupport.digitValueString(sCurve.x2) + " " + usupport.digitValueString(sCurve.y2);
    return result;
}

// const
kPlantProximityNeeded = 4;


// graphics 
//CFK NOTE you may want to change this if you use this function
//  to actually click on plant parts 
// this is not being used to select plant parts, the drawing surface is doing it
public boolean pointsAreCloseEnough(TPoint point1, TPoint point2) {
    result = false;
    result = (abs(point1.X - point2.X) < kPlantProximityNeeded) && (abs(point1.Y - point2.Y) < kPlantProximityNeeded);
    return result;
}


