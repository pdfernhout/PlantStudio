# unit umath
import math

import usstream
import usupport
from conversion_common import *
import uparams

"""
import udebug
import uunits
import delphi_compatability
"""

# record
class SCurveStructure:
    def __init__(self):
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0
        self.c1 = 0.0
        self.c2 = 0.0

# const
kPi = 3.141596
kLowestFloatAboveZero = 10e-12
kLowestQuantityFloat = 10e-6

# const
kGetField = 0
kSetField = 1

#returns zero for convenience
#these consts are really defined in uplant.pas but we don't want to include it - keep current
# error message - returns zero for convenience
def ErrorMessage(errorString):
    result = 0.0
    udebug.DebugPrint(errorString)
    return result

# ---------------------------------------------------------------------------------------------- math functions 
def sqr(x):
    result = x * x
    return result

def min(a, b):
    if (a < b):
        result = a
    else:
        result = b
    return result

def max(a, b):
    if (a > b):
        result = a
    else:
        result = b
    return result

def intMin(a, b):
    if (a < b):
        result = a
    else:
        result = b
    return result

def intMax(a, b):
    if (a > b):
        result = a
    else:
        result = b
    return result

# RE-RAISES EXCEPTION 
def pow(number, exponent):
    try:
        result = safeExp(exponent * safeLn(number))
    except:
        ErrorMessage("Invalid number for power function: " + FloatToStr(number) + " to the power " + FloatToStr(exponent))
        result = 1.0
        raise
    return result

# this function is needed to get around a bug in the development environment: if a negative
#number is raised to a non-integer power, an exception should be raised but the environment
#instead crashes. 
# RE-RAISES EXCEPTION 
def power(number, exponent):
    try:
        if (number > 0.0):
            result = pow(number, exponent)
        elif (number == 0.0):
            if exponent == 0.0:
                result = 1.0
                raise GeneralException.create("Problem: Zero raised to zero power.")
            else:
                result = 0.0
        else:
            result = 0.0
            raise GeneralException.create("Problem: Negative number to non-integer power: " + FloatToStr(number) + " to " + FloatToStr(exponent))
    except:
        result = ErrorMessage("Problem: Uncaught error in power function: " + FloatToStr(number) + " to " + FloatToStr(exponent))
        raise
    return result

# RE-RAISES EXCEPTION 
def tan(x):
    try:
        result = sin(x) / cos(x)
    except:
        result = ErrorMessage("Uncaught error in tangent function: " + FloatToStr(x))
        raise
    return result

# RE-RAISES EXCEPTION 
def arcCos(x):
    try:
        # this was in the Delphi help but doesn't seem to work 
        # result := arcTan(sqrt(1.0 - sqr(x)) / x); 
        # from Smalltalk/V 
        result = kPi / 2.0 - arcSin(x)
    except:
        result = ErrorMessage("Invalid number for arcCos: " + FloatToStr(x))
        raise
    return result

# RE-RAISES EXCEPTION 
def arcSin(x):
    try:
        result = arctan(x / sqrt(1.0 - sqr(x)))
    except:
        result = ErrorMessage("Invalid number for arcSin: " + FloatToStr(x))
        raise
    return result

# const
oneOverNaturalLogOfTen = 0.434294481

# RE-RAISES EXCEPTION 
# uses notion that logN(x) = ln(x) / ln(N) 
def log10(x):
    try:
        if x > 0.0:
            result = oneOverNaturalLogOfTen * safeLn(x)
        else:
            result = -1
            raise GeneralException.create("Problem: Tried to take log (base 10) of zero or negative number.")
    except:
        result = ErrorMessage("Problem: Invalid number for log (base 10): " + FloatToStr(x) + ".")
        raise
    return result

# RE-RAISES EXCEPTION 
def safeLn(x):
    if x > 0.0:
        try:
            result = math.log(x)
        except:
            ErrorMessage("Invalid number for natural log: " + FloatToStr(x))
            result = 1.0
            raise
    else:
        raise GeneralException.create("Problem: Tried to take ln of zero or negative number: " + FloatToStr(x) + ".")
    return result

# same as safeLn but does not show an errorMessage or re-raise the exception; just returns whether it failed;
#  used inside paint methods where you don't want error dialogs popping up 
def safeLnWithResult(x, failed):
    raise "function safeLnWithResult with preexisting result had var parameters added to return; fixup manually"
    
    failed = true
    result = 0.0
    temp = 0.0
    if x <= 0.0:
        return result, failed
    try:
        temp = math.log(x)
    except:
        result = 1.0
        return result, failed
    result = temp
    failed = false
    return result, failed

# RE-RAISES EXCEPTION 
def safeExp(x):
    try:
        result = math.exp(x)
    except:
        result = ErrorMessage("Invalid number for exponential function: " + FloatToStr(x))
        raise
    return result

# same as safeExp but does not show an errorMessage or re-raise the exception; just returns whether it failed;
#  used inside paint methods where you don't want error dialogs popping up 
def safeExpWithResult(x, failed):
    raise "function safeExpWithResult with preexisting result had var parameters added to return; fixup manually"

    failed = true
    result = 0.0
    temp = 0.0
    try:
        temp = math.exp(x)
    except:
        return result, failed
    result = temp
    failed = false
    return result, failed

#this function catches a divide by zero before it produces a not-a-number.
#this can happen because of an underflow, an error in the code, or an unexpected condition.
#this is a different approach than EPIC's which is basically to divide by the number plus a tiny float
#for all cases (like 1e-20 or 1e-10)
# RE-RAISES EXCEPTION 
def safediv(x, y):
    try:
        if (y != 0.0):
            result = 1.0 * x / y
        else:
            result = 0.0
            raise GeneralException.create("Problem: Divide by zero.")
    except:
        result = ErrorMessage("Problem: Unspecified problem with dividing " + FloatToStr(x) + " by " + FloatToStr(y) + ".")
        raise
    return result

# RE-RAISES EXCEPTION 
# same as safediv except that the user specifies what to return if the denominator is zero 
def safedivExcept(x, y, exceptionResult):
    try:
        if (y != 0.0):
            result = 1.0 * x / y
        else:
            result = exceptionResult
    except:
        result = ErrorMessage("Problem in dividing " + FloatToStr(x) + " by " + FloatToStr(y))
        raise
    return result

# same as safediv but does not show an errorMessage or re-raise the exception; just returns whether it failed;
#  used inside paint methods where you don't want error dialogs popping up 
def safedivWithResult(x, y, failed):
    raise "function safedivWithResult with preexisting result had var parameters added to return; fixup manually"

    failed = true
    result = 0.0
    temp = 0.0
    if y == 0.0:
        return result, failed
    try:
        temp = 1.0 * x / y
    except:
        return result, failed
    result = temp
    failed = false
    return result, failed

# s curves 
# RE-RAISES EXCEPTION 
# this function carries out a structure found in many EPIC equations. 
def scurve(x, c1, c2):
    try:
        temp = c1 - c2 * x
        if temp > 85.0:
            temp = 85.0
            raise GeneralException.create("Problem: Exponent of number would have gone out of float range.")
        result = safediv(x, x + safeExp(temp))
    except:
        # PDF PORT TEST
        raise
        result = ErrorMessage("Problem in s curve: numbers are " + FloatToStr(x) + ", " + FloatToStr(c1) + ", and " + FloatToStr(c2))
        raise
    return result

# same as scurve but does not show an errorMessage or re-raise the exception; just returns whether it failed;
#  used inside paint methods where you don't want error dialogs popping up 
def scurveWithResult(x, c1, c2, failed):
    raise "function scurveWithResult with preexisting result had var parameters added to return; fixup manually"

    failed = true
    result = 0.0
    temp = 0.0
    try:
        temp = c1 - c2 * x
        if temp > 85.0:
            return result, failed
        temp = safeExpWithResult(temp, failed)
        if failed:
            return result, failed
        temp = safedivWithResult(x, x + temp, failed)
        if failed:
            return result, failed
    except:
        return result, failed
    failed = false
    result = temp
    return result, failed

# s curve params 
# RE-RAISES EXCEPTION 
# deal with zero s curve values by defaulting whole curve to hard-coded values
def calcSCurveCoeffs(sCurve):
    try:
        if (sCurve.x1 <= 0.0) or (sCurve.y1 <= 0.0) or (sCurve.x2 <= 0.0) or (sCurve.y2 <= 0.0) or (sCurve.x1 >= 1.0) or (sCurve.y1 >= 1.0) or (sCurve.x2 >= 1.0) or (sCurve.y2 >= 1.0):
            # instead of raising exception, just hard-code whole curve to acceptable values
            # don't use Parameters.tab default in case that was read in wrong also
            sCurve.x1 = 0.25
            sCurve.y1 = 0.1
            sCurve.x2 = 0.65
            sCurve.y2 = 0.85
        xx = safeLn(safediv(sCurve.x1, sCurve.y1) - sCurve.x1)
        sCurve.c2 = safediv((xx - safeLn(safediv(sCurve.x2, sCurve.y2) - sCurve.x2)), sCurve.x2 - sCurve.x1)
        sCurve.c1 = xx + sCurve.x1 * sCurve.c2
    except Exception, e:
        # set s curve to all acceptable values - safest 
        sCurve.x1 = 0.25
        sCurve.y1 = 0.1
        sCurve.x2 = 0.65
        sCurve.y2 = 0.85
        raise

# same as Utils_CalcSCurveCoeffs but does not show an errorMessage or re-raise the exception;
#  just returns whether it failed; used inside paint methods where you don't want error dialogs popping up 
def calcSCurveCoeffsWithResult(sCurve, failed):
    failed = true
    try:
        quotientX1Y1 = safedivWithResult(sCurve.x1, sCurve.y1, failed)
        if failed:
            return failed
        lnQuotientX1Y1MinusX1 = safeLnWithResult(quotientX1Y1 - sCurve.x1, failed)
        if failed:
            return failed
        quotientX2Y2 = safedivWithResult(sCurve.x2, sCurve.y2, failed)
        if failed:
            return failed
        lnQuotientX2Y2MinusX2 = safeLnWithResult(quotientX2Y2 - sCurve.x2, failed)
        if failed:
            return failed
        c2temp = safedivWithResult(lnQuotientX1Y1MinusX1 - lnQuotientX2Y2MinusX2, sCurve.x2 - sCurve.x1, failed)
        if failed:
            return failed
        c1temp = lnQuotientX1Y1MinusX1 + sCurve.x1 * c2temp
    except:
        return failed
    sCurve.c1 = c1temp
    sCurve.c2 = c2temp
    failed = false
    return failed

def transferSCurveValue(direction, param, index, value):
    if (direction == kGetField):
        if index == 0:
            value = param.x1
        elif index == 1:
            value = param.y1
        elif index == 2:
            value = param.x2
        elif index == 3:
            value = param.y2
    else:
        if index == 0:
            # direction == kSetField 
            param.x1 = value
        elif index == 1:
            param.y1 = value
        elif index == 2:
            param.x2 = value
        elif index == 3:
            param.y2 = value
    return value

def stringToSCurve(aString):
    result = SCurveStructure()
    
    result.x1 = 0
    result.y1 = 0
    result.x2 = 0
    result.y2 = 0
    result.c1 = 0
    result.c2 = 0
    # format is x1 y1 x2 y2 
    stream = usstream.KfStringStream()
    stream.onStringSeparator(aString, " ")
    succesful, result.x1 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat)
    succesful, result.y1 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat)
    succesful, result.x2 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat)
    succesful, result.y2 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat)
    return result

def sCurveToString(sCurve):
    result = usupport.digitValueString(sCurve.x1) + " " + usupport.digitValueString(sCurve.y1) + " " + usupport.digitValueString(sCurve.x2) + " " + usupport.digitValueString(sCurve.y2)
    return result

# const
kPlantProximityNeeded = 4

# graphics 
#CFK NOTE you may want to change this if you use this function
#  to actually click on plant parts 
# this is not being used to select plant parts, the drawing surface is doing it
def pointsAreCloseEnough(point1, point2):
    result = false
    result = (abs(point1.X - point2.X) < kPlantProximityNeeded) and (abs(point1.Y - point2.Y) < kPlantProximityNeeded)
    return result

