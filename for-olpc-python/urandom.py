# unit Urandom
import time

from conversion_common import *
import umath

"""
import uclasses
import ufiler
import delphi_compatability
"""

class PdRandom:
    def __init__(self):
        self.seed = 0L
    
    def createFromTime(self):
        self.seed = self.randomSeedFromTime()
        return self
    
    def setSeed(self, aSeed):
        self.seed = aSeed
    
    def setSeedFromSmallint(self, aSeed):
        #same as setSeed but making conversion here from smallint to longint
        self.seed = makesmallint(aSeed)
    
    def randomSeedFromTime(self):
        seconds = time.time()
        result = intround(seconds * 100)
        return result
    
    def randomSmallintSeedFromTime(self):        
        seconds = time.time()
        result = intround(seconds * 100)
        
        # so things too close in time are not too similar, modify it randomly 
        result = intround(result * self.zeroToOne())
        # make it a smallint --as if that still matters?
        result = makesmallint(result)
        return result
    
    def initialize(self, aLong):
        self.seed = aLong
    
    def randomNormalWithStdDev(self, mean, stdDev):
        randomNumber = 0.0
        for i in range(0, 12):
            randomNumber = randomNumber + self.zeroToOne()
        result = (randomNumber - 6.0) * stdDev + mean
        return result
    
    def randomNormal(self, mean):
        #return normal random number based on mean (and std dev of half mean)
        randomNumber = 0.0
        for i in range(0, 12):
            randomNumber = randomNumber + self.zeroToOne()
        result = (randomNumber - 6.0) * (mean / 2.0) + mean
        return result
    
    def randomNormalBoundedZeroToOne(self, mean):
        #return normal random number based on mean (and std dev of half mean)
        result = umath.max(0.0, (umath.min(1.0, (self.randomNormal(mean)))))
        return result
    
    def randomNormalPercent(self, mean):
        #return normal random number based on mean (and std dev of half mean) bounded at 0 and 100
        result = umath.max(0, (umath.min(100, intround(self.randomNormal(mean / 100.0) * 100.0))))
        return result
    
    def randomPercent(self):
        k = intround(self.seed / 127773)
        self.seed = intround((16807 * (self.seed - (k * 127773))) - (k * 2846))
        if (self.seed < 0.0):
            self.seed = self.seed + 2147483647
        result = intround(umath.max(0, (umath.min(100, (self.seed * 0.0000000004656612875 * 100.0)))))
        return result
    
    def zeroToOne(self):
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
    
if __name__ == '__main__':
    #tests
    print "test"
    r = PdRandom()
    r.createFromTime()
    print "r.seed", r.seed
    print r.randomPercent()
    print r.randomPercent()
    print r.randomPercent()
    print r.randomPercent()
    print r.randomPercent()