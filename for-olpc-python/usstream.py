# unit Usstream
#Copyright (c) 1997 Paul D. Fernhout and Cynthia F. Kurtz All rights reserved
#http://www.gardenwithinsight.com. See the license file for details on redistribution.
#=====================================================================================
#usstream: String stream. Used by text filer (ufilertx) to parse strings,
#usually those associated with points or arrays (because there are delimiters inside
#the string in these cases). Also used by 3d object (in uturt3d) to read strings from tdo file.

# PDF THIS IS TERRBILY INEFFICIENT WITH COPYING __ SHOULD IMPORVE EVENTUALLY TO USE AN INDEX

from conversion_common import *
import delphi_compatability

def skipToProfileSection(fileStream, section):
    inputLine = ""
    stream = KfStringStream()
    
    #set separator to ']' so can read sections
    stream.separator = "]"
    result = False
    inputLine = readln(fileStream)
    while inputLine != None:
        stream.onString(inputLine)
        stream.skipSpaces()
        if stream.nextCharacter() == "[":
            if stream.nextToken() == section:
                result = True
                break
        inputLine = readln(fileStream)
    return result

class KfStringStream:
    def __init__(self):
        self.source = ""
        self.remainder = ""
        self.separator = ""
    
    def createFromString(self, aString):
        self.onStringSeparator(aString, " ")
        return self
    
    def onString(self, aString):
        self.source = aString
        self.remainder = aString
    
    def onStringSeparator(self, aString, aSeparator):
        self.source = aString
        self.remainder = aString
        self.separator = aSeparator
    
    def spaceSeparator(self):
        self.separator = " "
    
    def skipSpaces(self):
        while self.remainder and (self.remainder[0] == " "):
            self.remainder = self.remainder[1:]
    
    def nextToken(self):
        self.skipSpaces()
        location = self.remainder.find(self.separator)
        if location != -1:
            result = self.remainder[0: location]
            self.remainder = self.remainder[location + len(self.separator):]
        else:
            result = self.remainder
            self.remainder = ""
        return result
    
    def nextInteger(self):
        token = self.nextToken()
        result = StrToIntDef(token, 0)
        return result
    
    def nextSingle(self):
        result = 0.0
        token = self.nextToken()
        try:
            result = StrToFloat(token)
        except EConvertError:
            result = 0.0
        return result
    
    def nextCharacter(self):
        if not self.remainder:
            return None
        result = self.remainder[0]
        self.remainder = self.remainder[1:]
        return result
    
    #return true if next few characters match string
    def match(self, aString):
        result = self.remainder.find(aString) == 0
        return result
    
    def skipWhiteSpace(self):
        while (self.remainder) and ((self.remainder[0] == " ") or (self.remainder[0] == chr(9))):
            self.remainder = self.remainder[1:]
    
    def empty(self):
        result = (self.remainder == "")
        return result
    
