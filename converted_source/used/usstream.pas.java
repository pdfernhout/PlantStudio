// unit Usstream
//Copyright (c) 1997 Paul D. Fernhout and Cynthia F. Kurtz All rights reserved
//http://www.gardenwithinsight.com. See the license file for details on redistribution.
//=====================================================================================
//usstream: String stream. Used by text filer (ufilertx) to parse strings,
//usually those associated with points or arrays (because there are delimiters inside
//the string in these cases). Also used by 3d object (in uturt3d) to read strings from tdo file.

from conversion_common import *;
import delphi_compatability;

public boolean skipToProfileSection(TextFile fileStream, String section) {
    result = false;
    String inputLine = "";
    KfStringStream stream = new KfStringStream();
    
    stream = KfStringStream.create;
    //set separator to ']' so can read sections
    stream.separator = "]";
    result = false;
    while (!UNRESOLVED.eof(fileStream)) {
        UNRESOLVED.readln(fileStream, inputLine);
        stream.onString(inputLine);
        stream.skipSpaces();
        if (stream.nextCharacter() == "[") {
            if (stream.nextToken() == section) {
                result = true;
                break;
            }
        }
    }
    stream.free;
    return result;
}


class KfStringStream extends TObject {
    public String source;
    public String remainder;
    public String separator;
    
    public void createFromString(String aString) {
        this.create;
        this.onStringSeparator(aString, " ");
    }
    
    public void onString(String aString) {
        this.source = aString;
        this.remainder = aString;
    }
    
    public void onStringSeparator(String aString, String aSeparator) {
        this.source = aString;
        this.remainder = aString;
        this.separator = aSeparator;
    }
    
    public void spaceSeparator() {
        this.separator = " ";
    }
    
    public void skipSpaces() {
        while ((UNRESOLVED.copy(this.remainder, 1, 1) == " ")) {
            this.remainder = UNRESOLVED.copy(this.remainder, 2, 255);
        }
    }
    
    public String nextToken() {
        result = "";
        long location = 0;
        
        this.skipSpaces();
        location = UNRESOLVED.pos(this.separator, this.remainder);
        if (location != 0) {
            result = UNRESOLVED.copy(this.remainder, 1, location - 1);
            this.remainder = UNRESOLVED.copy(this.remainder, location + len(this.separator), 255);
        } else {
            result = this.remainder;
            this.remainder = "";
        }
        return result;
    }
    
    public long nextInteger() {
        result = 0;
        String token = "";
        
        token = this.nextToken();
        result = StrToIntDef(token, 0);
        return result;
    }
    
    public float nextSingle() {
        result = 0.0;
        String token = "";
        
        result = 0.0;
        token = this.nextToken();
        try {
            result = StrToFloat(token);
        } catch (EConvertError e) {
            result = 0.0;
        }
        return result;
    }
    
    public char nextCharacter() {
        result = ' ';
        result = this.remainder[1];
        this.remainder = UNRESOLVED.copy(this.remainder, 2, 255);
        return result;
    }
    
    //return true if next few characters match string
    public boolean match(String aString) {
        result = false;
        result = (UNRESOLVED.pos(aString, this.remainder) == 1);
        return result;
    }
    
    public void skipWhiteSpace() {
        while ((this.remainder[1] == " ") || (this.remainder[1] == chr(9))) {
            //tab
            this.remainder = UNRESOLVED.copy(this.remainder, 2, 255);
        }
    }
    
    public boolean empty() {
        result = false;
        result = (this.remainder == "");
        return result;
    }
    
}
