import math
import os
import ucursor

# PDF Added

def string_match(a, b, find=0, uppercase=1, strip=1, startsWith=0):
    if strip:
        a = a.strip()
        b = b.strip()   
    if uppercase:
        a = a.upper()
        b = b.upper()     
    if find:
        return b.find(a) != -1
    elif startsWith:
        return b.find(a) == 0
    else:
        return a == b
    
def string_startsWith(a, b, find=0, uppercase=1, strip=1):
    return string_match(a, b, find, uppercase, strip, 1)
        
def makesmallint(x):
    return x % 32768

   
class SinglePoint:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        
UnassignedColor = None
    
def Cursor_StartWait():
    ucursor.cursor_startWait()
                    
def Cursor_StopWait():
    ucursor.cursor_stopWait()
    
# PDF PORT FIX 
class TPixelFormat:
    pass
    
###############################################
        
# string to number conversion

def IntToStr(value):
    return "%d" % value

def IntToStrDef(value, default):
    try:
        return IntToStr(value)
    except TypeError:
        return default
    
def StrToInt(value):
    return int(value)

def StrToIntDef(value, default):
    try:
        return StrToInt(value)
    except ValueError:
        return default
    
def FloatToStr(value):
    return "%f" % value
    
def FloatToStrF(value, conversionType, a, b):
    return "%f" % value
    
def StrToFloat(value):
    return float(value)
            
# math

def intround(x):
    return int(long(round(x)) & 0xFFFFFFFF)

def odd(x):
    return x % 2 == 1

def even(x):
    return x % 2 == 0

def trunc(x):
    return int(math.floor(x))

def sqrt(x):
    return math.sqrt(x)

def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

def arctan(x):
    return math.atan(x)
    
# delphi files

class TextFile:
    def __init__(self):
        self.fileName = None
        self.fp = None
        self.reading = 0
        self.writing = 0

def writeln(textFile, *args):
    write(textFile, *args)
    if isinstance(textFile, TextFile):
        fp = textFile.fp
    else:
        fp = textFile
    fp.write("\n")
    
# returns None if at end
def readln(textfile):
    result = textfile.fp.readline()
    if not result:
        return None
    # remove possible ending chracted or newline and return
    if (result[-1] == '\n') or (result[-1] == '\r'):
        result = result[:-1]
    # may be in either order, so do twice to be sure
    if result:
        if (result[-1] == '\n') or (result[-1] == '\r'):
            result = result[:-1]
    return result  

def write(textFile, *args):
    if isinstance(textFile, TextFile):
        fp = textFile.fp
    else:
        fp = textFile
    for arg in args:
        try:
            fp.write(arg)
        except TypeError:
            # handle numbers
            fp.write(`arg`)
            
def AssignFile(textFile, fileName):
    textFile.fileName = fileName
    if textFile.fp:
        textFile.fp.close()
    textFile.fp = None
    textFile.reading = 0
    textFile.writing = 0

# open file for reading
def Reset(textFile):
    if textFile.fp:
        textFile.fp.close()
    textFile.fp = file(textFile.fileName)
    textFile.reading = 1

# open file for writing
def Rewrite(textFile):
    if textFile.fp:
        textFile.fp.close()
    textFile.fp = file(textFile.fileName, "w")
    textFile.writing = 1

def Flush(textFile):
    if isinstance(textFile, TextFile):
        fp = textFile.fp
    else:
        fp = textFile
    fp.flush()
    
def CloseFile(textFile):
    if isinstance(textFile, TextFile):
        fp = textFile.fp
    else:
        fp = textFile
    if fp:
        fp.close()

ExpandFileName = os.path.abspath
ExtractFilePath = os.path.dirname
FileExists = os.path.isfile
DirectoryExists = os.path.isdir
ExtractFileName = os.path.basename
ExtractDirName = os.path.dirname

def RenameFile(oldName, newName):
    try:
        os.rename(oldName, newName)
        return 1
    except OSError:
        return 0

def DeleteFile(fileName):
   try:
       os.remove(fileName)
       return 1
   except OSError:
       return 0

# extension includes dot
def ExtractFileExt(fileName):
    pos = fileName.rfind(".")
    if pos == -1:
        extension = ""
    else:
        extension = fileName[pos:]
    return extension

def ChangeFileExt(fileName, newExtension):
    pos = fileName.rfind(".")
    if pos == -1:
        result = fileName + newExtension
    else:
        result = fileName[:pos] + newExtension
    return result

def IsReadOnly(fileName):
    #NOT UNDER JYTHON: return not os.access(fileName, os.W_OK)
    # NOT HAPPY WITH FOLLOWING WAY OF TESTIGN -- BUT ONLY GENERAL APPROACH for Mac?
    try:
        f = open(fileName, "r+")
        f.close()
        return 0
    except:
        return 1

# strings
    
def uppercase(text):
    return text.upper()

def lowercase(text):
    return text.lower()

def trim(text):
    return text.strip()

# support classes

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
       
class Rect:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        
    def getWidth(self):
        return self.right - self.left
    
    def getHeight(self):
        return self.bottom - self.top
    
    def __getattr__(self, name):
        if name == "width":
            return self.getWidth()
        elif name == "height":
            return self.getHeight()
        else:
            raise AttributeError(name) 
        
class ApplicationException(Exception):
    def create(text):
        return ApplicationException(text)
    create = staticmethod(create)
        
# simple GUI things

def ShowMessage(aString, parentComponent=None):
    JOptionPane.showMessageDialog(parentComponent, aString, "Message", JOptionPane.PLAIN_MESSAGE)
    
mtWarning = 1
mtError = 2
mtInformation = 3
mtConfirmation = 4
mtCustom = 5

mrNo = "no"
mbNo = "no"

mrYes = "yes"
mbYes = "yes"
 
mrCancel = "cancel"
mbCancel = "cancel" 

mrOK = "ok"
mbOK = "ok"

mbYesNoCancel = [mbYes, mbNo, mbCancel]

def InputQuery(component, title, prompt, default):
    return JOptionPane.showInputDialog(component, prompt, title, JOptionPane.QUESTION_MESSAGE, None, None, default)

def MessageDialog(prompt, typeFromDelphi, options, helpContextIgnored, parent=None):
    # could have better handlign of mroe options
    # Good explaination of options: http://www.delphibasics.co.uk/RTL.asp?Name=MessageDlg
    for option in options:
        if not option in [mbNo, mbYes, mbCancel, mbOK]:
            raise "unhandled option"
    if typeFromDelphi == mtConfirmation:
        optionType = JOptionPane.YES_NO_OPTION
        if mbCancel in mbCancel:
            optionType = JOptionPane.YES_NO_CANCEL_OPTION
        result = JOptionPane.showConfirmDialog(parent, prompt, "Confirm?", optionType)
    elif typeFromDelphi == mtError:
        JOptionPane.showMessageDialog(parent, prompt, "Error", JOptionPane.ERROR_MESSAGE)
        result = JOptionPane.OK_OPTION
    elif typeFromDelphi == mtWarning:
        JOptionPane.showMessageDialog(parent, prompt, "Warning", JOptionPane.WARNING_MESSAGE)
        result = JOptionPane.OK_OPTION
    elif typeFromDelphi == mtInformation:
        JOptionPane.showMessageDialog(parent, prompt, "Information", JOptionPane.PLAIN_MESSAGE)
        result = JOptionPane.OK_OPTION
    elif typeFromDelphi == mtCustom:
        JOptionPane.showMessageDialog(parent, prompt, "Message", JOptionPane.PLAIN_MESSAGE)
        result = JOptionPane.OK_OPTION
    else:
        raise "unknown message type: " + `typeFromDelphi`
        #type = JOptionPane.ERROR_MESSAGE
        #JOptionPane.showMessageDialog(parent, prompt, "message", type)
        return None
    if result == JOptionPane.YES_OPTION:
        result = mrYes
    elif result == JOptionPane.NO_OPTION:
        result = mrNo
    elif result == JOptionPane.CANCEL_OPTION or result == -1:
        result = mrCancel
    elif result == JOptionPane.OK_OPTION:
        result = mrOK
    elif result == JOptionPane.CLOSED_OPTION:
        result = mrCancel
    else:
        raise "unknown result from dialog " + `result`
        result = mrCancel
    return result    
    

      