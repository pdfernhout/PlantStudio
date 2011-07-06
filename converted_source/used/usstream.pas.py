# unit Usstream
#Copyright (c) 1997 Paul D. Fernhout and Cynthia F. Kurtz All rights reserved
#http://www.gardenwithinsight.com. See the license file for details on redistribution.
#=====================================================================================
#usstream: String stream. Used by text filer (ufilertx) to parse strings,
#usually those associated with points or arrays (because there are delimiters inside
#the string in these cases). Also used by 3d object (in uturt3d) to read strings from tdo file.

from conversion_common import *
import delphi_compatability

def skipToProfileSection(fileStream, section):
    result = false
    inputLine = ""
    stream = KfStringStream()
    
    stream = KfStringStream.create
    #set separator to ']' so can read sections
    stream.separator = "]"
    result = false
    while not UNRESOLVED.eof(fileStream):
        UNRESOLVED.readln(fileStream, inputLine)
        stream.onString(inputLine)
        stream.skipSpaces()
        if stream.nextCharacter() == "[":
            if stream.nextToken() == section:
                result = true
                break
    stream.free
    return result

class KfStringStream(TObject):
    def __init__(self):
        self.source = ""
        self.remainder = ""
        self.separator = ""
    
    def createFromString(self, aString):
        self.create
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
        while (UNRESOLVED.copy(self.remainder, 1, 1) == " "):
            self.remainder = UNRESOLVED.copy(self.remainder, 2, 255)
    
    def nextToken(self):
        result = ""
        location = 0L
        
        self.skipSpaces()
        location = UNRESOLVED.pos(self.separator, self.remainder)
        if location != 0:
            result = UNRESOLVED.copy(self.remainder, 1, location - 1)
            self.remainder = UNRESOLVED.copy(self.remainder, location + len(self.separator), 255)
        else:
            result = self.remainder
            self.remainder = ""
        return result
    
    def nextInteger(self):
        result = 0L
        token = ""
        
        token = self.nextToken()
        result = StrToIntDef(token, 0)
        return result
    
    def nextSingle(self):
        result = 0.0
        token = ""
        
        result = 0.0
        token = self.nextToken()
        try:
            result = StrToFloat(token)
        except EConvertError:
            result = 0.0
        return result
    
    def nextCharacter(self):
        result = ' '
        result = self.remainder[1]
        self.remainder = UNRESOLVED.copy(self.remainder, 2, 255)
        return result
    
    #return true if next few characters match string
    def match(self, aString):
        result = false
        result = (UNRESOLVED.pos(aString, self.remainder) == 1)
        return result
    
    def skipWhiteSpace(self):
        while (self.remainder[1] == " ") or (self.remainder[1] == chr(9)):
            #tab
            self.remainder = UNRESOLVED.copy(self.remainder, 2, 255)
    
    def empty(self):
        result = false
        result = (self.remainder == "")
        return result
    
