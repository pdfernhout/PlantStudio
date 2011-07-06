// unit Urandom

from conversion_common import *;
import umath;
import ufiler;
import delphi_compatability;


class PdRandom extends PdStreamableObject {
    public long seed;
    
    public void createFromTime() {
        this.create();
        this.seed = this.randomSeedFromTime();
    }
    
    public void setSeed(long aSeed) {
        this.seed = aSeed;
    }
    
    public void setSeedFromSmallint(short aSeed) {
        //same as setSeed but making conversion here from smallint to longint
        this.seed = aSeed;
    }
    
    public long randomSeedFromTime() {
        result = 0;
        TDateTime Present = new TDateTime();
        byte Year = 0;
        byte Month = 0;
        byte Day = 0;
        byte Hour = 0;
        byte Min = 0;
        byte Sec = 0;
        byte MSec = 0;
        long longintVar = 0;
        
        Present = UNRESOLVED.Now;
        UNRESOLVED.DecodeDate(Present, Year, Month, Day);
        UNRESOLVED.DecodeTime(Present, Hour, Min, Sec, MSec);
        // was (Hour * 24 * 60 * 60 * 100) + 
        longintVar = 1;
        result = longintVar * Hour * 24 * 60 * 60 + longintVar * Min * 60 * 60 * 100 + longintVar * Sec * 100 + longintVar * MSec;
        return result;
    }
    
    public short randomSmallintSeedFromTime() {
        result = 0;
        TDateTime Present = new TDateTime();
        byte Year = 0;
        byte Month = 0;
        byte Day = 0;
        byte Hour = 0;
        byte Min = 0;
        byte Sec = 0;
        byte MSec = 0;
        short smallintVar = 0;
        
        Present = UNRESOLVED.Now;
        UNRESOLVED.DecodeDate(Present, Year, Month, Day);
        UNRESOLVED.DecodeTime(Present, Hour, Min, Sec, MSec);
        smallintVar = 1;
        result = smallintVar * Sec * 100 + smallintVar * MSec;
        // so things too close in time are not too similar, modify it randomly 
        result = intround(result * this.zeroToOne());
        return result;
    }
    
    public void initialize(long aLong) {
        this.seed = aLong;
    }
    
    public float randomNormalWithStdDev(float mean, float stdDev) {
        result = 0.0;
        float randomNumber = 0.0;
        int i = 0;
        
        randomNumber = 0.0;
        for (i = 1; i <= 12; i++) {
            randomNumber = randomNumber + this.zeroToOne();
        }
        result = (randomNumber - 6.0) * stdDev + mean;
        return result;
    }
    
    public float randomNormal(float mean) {
        result = 0.0;
        float randomNumber = 0.0;
        int i = 0;
        
        //return normal random number based on mean (and std dev of half mean)
        randomNumber = 0.0;
        for (i = 1; i <= 12; i++) {
            randomNumber = randomNumber + this.zeroToOne();
        }
        result = (randomNumber - 6.0) * (mean / 2.0) + mean;
        return result;
    }
    
    public float randomNormalBoundedZeroToOne(float mean) {
        result = 0.0;
        //return normal random number based on mean (and std dev of half mean)
        result = umath.max(0.0, (umath.min(1.0, (this.randomNormal(mean)))));
        return result;
    }
    
    public float randomNormalPercent(float mean) {
        result = 0.0;
        //return normal random number based on mean (and std dev of half mean) bounded at 0 and 100
        result = umath.max(0, (umath.min(100, intround(this.randomNormal(mean / 100.0) * 100.0))));
        return result;
    }
    
    public float randomPercent() {
        result = 0.0;
        float k = 0.0;
        
        k = intround(this.seed / 127773);
        this.seed = intround((16807 * (this.seed - (k * 127773))) - (k * 2846));
        if ((this.seed < 0.0)) {
            this.seed = this.seed + 2147483647;
        }
        result = intround(umath.max(0, (umath.min(100, (this.seed * 0.0000000004656612875 * 100.0)))));
        return result;
    }
    
    public float zeroToOne() {
        result = 0.0;
        float k = 0.0;
        
        k = intround(this.seed / 127773);
        this.seed = intround((16807 * (this.seed - (k * 127773))) - (k * 2846));
        if ((this.seed < 0.0)) {
            this.seed = this.seed + 2147483647;
        }
        result = (umath.max(0.0, (umath.min(1.0, (this.seed * 0.0000000004656612875))))) * 1.0;
        return result;
    }
    
    public void classAndVersionInformation(PdClassAndVersionInformationRecord cvir) {
        cvir.classNumber = UNRESOLVED.KPdRandom;
        cvir.versionNumber = 0;
        cvir.additionNumber = 0;
    }
    
    public void streamDataWithFiler(PdFiler filer, PdClassAndVersionInformationRecord cvir) {
        this.seed = filer.streamLongint(this.seed);
    }
    
}
