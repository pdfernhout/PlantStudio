# unit Urandom

from conversion_common import *
import uclasses
import umath
import ufiler
import delphi_compatability

class PdRandom(PdStreamableObject):
    def __init__(self):
        self.seed = 0L
    
    def createFromTime(self):
        self.create()
        self.seed = self.randomSeedFromTime()
        return self
    
    def setSeed(self, aSeed):
        self.seed = aSeed
    
    def setSeedFromSmallint(self, aSeed):
        #same as setSeed but making conversion here from smallint to longint
        self.seed = aSeed
    
    def randomSeedFromTime(self):
        result = 0L
        Present = TDateTime()
        Year = 0
        Month = 0
        Day = 0
        Hour = 0
        Min = 0
        Sec = 0
        MSec = 0
        longintVar = 0L
        
        Present = UNRESOLVED.Now
        UNRESOLVED.DecodeDate(Present, Year, Month, Day)
        UNRESOLVED.DecodeTime(Present, Hour, Min, Sec, MSec)
        # was (Hour * 24 * 60 * 60 * 100) + 
        longintVar = 1
        result = longintVar * Hour * 24 * 60 * 60 + longintVar * Min * 60 * 60 * 100 + longintVar * Sec * 100 + longintVar * MSec
        return result
    
    def randomSmallintSeedFromTime(self):
        result = 0
        Present = TDateTime()
        Year = 0
        Month = 0
        Day = 0
        Hour = 0
        Min = 0
        Sec = 0
        MSec = 0
        smallintVar = 0
        
        Present = UNRESOLVED.Now
        UNRESOLVED.DecodeDate(Present, Year, Month, Day)
        UNRESOLVED.DecodeTime(Present, Hour, Min, Sec, MSec)
        smallintVar = 1
        result = smallintVar * Sec * 100 + smallintVar * MSec
        # so things too close in time are not too similar, modify it randomly 
        result = intround(result * self.zeroToOne())
        return result
    
    def initialize(self, aLong):
        self.seed = aLong
    
    def randomNormalWithStdDev(self, mean, stdDev):
        result = 0.0
        randomNumber = 0.0
        i = 0
        
        randomNumber = 0.0
        for i in range(1, 12 + 1):
            randomNumber = randomNumber + self.zeroToOne()
        result = (randomNumber - 6.0) * stdDev + mean
        return result
    
    def randomNormal(self, mean):
        result = 0.0
        randomNumber = 0.0
        i = 0
        
        #return normal random number based on mean (and std dev of half mean)
        randomNumber = 0.0
        for i in range(1, 12 + 1):
            randomNumber = randomNumber + self.zeroToOne()
        result = (randomNumber - 6.0) * (mean / 2.0) + mean
        return result
    
    def randomNormalBoundedZeroToOne(self, mean):
        result = 0.0
        #return normal random number based on mean (and std dev of half mean)
        result = umath.max(0.0, (umath.min(1.0, (self.randomNormal(mean)))))
        return result
    
    def randomNormalPercent(self, mean):
        result = 0.0
        #return normal random number based on mean (and std dev of half mean) bounded at 0 and 100
        result = umath.max(0, (umath.min(100, intround(self.randomNormal(mean / 100.0) * 100.0))))
        return result
    
    def randomPercent(self):
        result = 0.0
        k = 0.0
        
        k = intround(self.seed / 127773)
        self.seed = intround((16807 * (self.seed - (k * 127773))) - (k * 2846))
        if (self.seed < 0.0):
            self.seed = self.seed + 2147483647
        result = intround(umath.max(0, (umath.min(100, (self.seed * 0.0000000004656612875 * 100.0)))))
        return result
    
    def zeroToOne(self):
        result = 0.0
        k = 0.0
        
        k = intround(self.seed / 127773)
        self.seed = intround((16807 * (self.seed - (k * 127773))) - (k * 2846))
        if (self.seed < 0.0):
            self.seed = self.seed + 2147483647
        result = (umath.max(0.0, (umath.min(1.0, (self.seed * 0.0000000004656612875))))) * 1.0
        return result
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.KPdRandom
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        self.seed = filer.streamLongint(self.seed)
    
