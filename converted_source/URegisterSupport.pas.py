# unit URegisterSupport

from conversion_common import *
import delphi_compatability

# record
class RegisterStruct:
    def __init__(self):
        self.s1 = 0
        self.s2 = 0
        self.s3 = 0
        self.s4 = 0

# const
codeArraySize = 9

def WriteCodeFile(userName, code, fileNameMaybeLeadingPipe):
    success = 0
    CodeFile = TextFile()
    tempFileName = ""
    tempFilePath = ""
    fileName = ""
    warningIfExists = false
    
    warningIfExists = true
    if fileNameMaybeLeadingPipe[1] == "|":
        fileName = UNRESOLVED.copy(fileNameMaybeLeadingPipe, 2, len(fileNameMaybeLeadingPipe))
        warningIfExists = false
    else:
        fileName = fileNameMaybeLeadingPipe
    tempFilePath = ExtractFilePath(fileName)
    if tempFilePath == "":
        UNRESOLVED.SetLength(tempFilePath, UNRESOLVED.MAX_PATH + 2)
        UNRESOLVED.GetTempPath(UNRESOLVED.MAX_PATH, tempFilePath)
        # maybe plus one??
        UNRESOLVED.SetLength(tempFilePath, len(tempFilePath))
    UNRESOLVED.SetLength(tempFileName, UNRESOLVED.MAX_PATH + 2)
    # address of directory name for temporary file
    # address of filename prefix
    # number used to create temporary filename
    # address of buffer that receives the new filename
    success = UNRESOLVED.GetTempFileName(tempFilePath, "shr", 0, tempFileName)
    if success == 0:
        ShowMessage(ExtractFileName(delphi_compatability.Application.ExeName) + " Unable to generate temporary file name for StoryHarp registration")
        return
    # maybe plus one??
    UNRESOLVED.SetLength(tempFileName, len(tempFileName))
    AssignFile(CodeFile, tempFileName)
    Rewrite(CodeFile)
    try:
        writeln(CodeFile, "StoryHarp 1.x registration information")
        writeln(CodeFile, "Registration Name: ", userName)
        writeln(CodeFile, "Registration Code: ", code)
        Flush(CodeFile)
    finally:
        CloseFile(CodeFile)
    if FileExists(fileName):
        if warningIfExists:
            if MessageDialog(ExtractFileName(delphi_compatability.Application.ExeName) + ": " + chr(13) + "A problem has occured in the coordination of the PsL order-entry system and" + chr(13) + "the program which generates the StoryHarp registration code output file. " + chr(13) + chr(13) + "The requested output file \"" + fileName + "\" already exists, and it should not exist." + chr(13) + "The existing file will be deleted and then created again if you press OK." + chr(13) + "(If you press Cancel the file will be left as is.)" + chr(13) + chr(13) + "However, because the PsL order-entry system is supposed to be waiting right now" + chr(13) + "for a file with this name to appear, something improper is happening" + chr(13) + "If you see this error, it is possible a registration code for someone else " + chr(13) + "has already been given to the customer \"" + userName + "\"." + chr(13) + chr(13) + "This is a serious error in the way PsL uses this program and should be reported and corrected." + chr(13) + chr(13) + "If you wish to never see this error again (not recommended), " + chr(13) + "you can bypass it by putting a \"|\" at the start of the file path in the second argument." + chr(13) + "Contact Paul or Cynthia at http://www.kurtz-fernhout.com for details.", delphi_compatability.TMsgDlgType.mtError, [mbOK, mbCancel, ], 0) != delphi_compatability.IDOK:
                # questionable?
                return
        DeleteFile(fileName)
    AssignFile(CodeFile, tempFileName)
    UNRESOLVED.Rename(CodeFile, fileName)

def nextRandom(generator):
    result = 0
    newValue = 0
    
    # one added to defeat case of all zeroing out seeds
    newValue = generator.s1 + generator.s2 + 1
    generator.s1 = generator.s2
    generator.s2 = generator.s3
    generator.s3 = generator.s4
    generator.s4 = newValue % 65536
    result = generator.s1 % 256
    return result

# only used to calculate initial seeds
def WarmUp(generator):
    i = 0
    
    for i in range(0, 897 + 1):
        # SH 897
        nextRandom(generator)

def ResetGenerator(generator):
    # SH   37903 61164  59082  16777
    generator.s1 = 37903
    generator.s2 = 61164
    generator.s3 = 59082
    generator.s4 = 16777

# Maybe PS ??? 234    34432    4356   7
def generate(name):
    result = ""
    i = 0
    j = 0
    n = 0
    nmod = 0
    letter = ' '
    reorganizedName = ""
    remainingLetters = ""
    nameWithOnlyChars = ""
    lowerCaseName = ""
    codeArray = [0] * (range(0, (codeArraySize - 1) + 1) + 1)
    generator = RegisterStruct()
    
    ResetGenerator(generator)
    result = ""
    nameWithOnlyChars = ""
    lowerCaseName = trim(lowercase(name))
    for i in range(1, len(lowerCaseName) + 1):
        if (ord(lowerCaseName[i]) >= ord("a")) and (ord(lowerCaseName[i]) <= ord("z")) or (ord(lowerCaseName[i]) >= ord("0")) and (ord(lowerCaseName[i]) <= ord("9")):
            nameWithOnlyChars = nameWithOnlyChars + lowerCaseName[i]
    remainingLetters = nameWithOnlyChars
    reorganizedName = ""
    for i in range(1, len(nameWithOnlyChars) + 1):
        letter = nameWithOnlyChars[len(nameWithOnlyChars) + 1 - i]
        for j in range(0, (ord(letter)) + 1):
            #  + i * 7
            nextRandom(generator)
        n = nextRandom(generator)
        nmod = n % len(remainingLetters)
        reorganizedName = reorganizedName + remainingLetters[nmod + 1]
        UNRESOLVED.Delete(remainingLetters, nmod + 1, 1)
    for i in range(0, codeArraySize):
        codeArray[i] = nextRandom(generator)
    for i in range(1, len(reorganizedName) + 1):
        letter = reorganizedName[len(reorganizedName) + 1 - i]
        if letter == " ":
            continue
        for j in range(0, (ord(letter)) + 1):
            #  + i * 7
            nextRandom(generator)
        n = nextRandom(generator)
        nmod = n % 10
        codeArray[i % codeArraySize] = codeArray[i % codeArraySize] + nmod
    result = "3"
    for i in range(0, codeArraySize):
        result = result + chr(ord("0") + (codeArray[i] % 10))
    return result

def GenerateFromCommandLine():
    userName = ""
    fileName = ""
    code = ""
    
    if UNRESOLVED.ParamCount != 2:
        ShowMessage("Useage: " + ExtractFileName(delphi_compatability.Application.ExeName) + " \"user name\"  \"file name\"" + chr(13) + chr(13) + "The key code generator " + ExtractFileName(delphi_compatability.Application.ExeName) + " expects two arguments." + chr(13) + "The first is the user name, and the second is the name of a text file to store the code in." + chr(13) + "Arguments that can have embedded spaces like the user name" + chr(13) + "must be surrounded by double quotes." + chr(13) + chr(13) + "Example: " + ExtractFileName(delphi_compatability.Application.ExeName) + " \"Joe User\"  \"C:\temp\dir with spaces\regfile.txt\"" + chr(13) + chr(13) + "Contact us at http://www.kurtz-fernhout.com for details" + chr(13) + chr(13) + "This program operates under the expectation the output file does not exist." + chr(13) + "If for some reason the output file exists when the program is started" + chr(13) + "a warning dialog will pop-up requiring OK or Cancel to be pressed." + chr(13) + "(unless you have disabled that warning as explained on that dialog)." + chr(13) + chr(13) + "This program is Copyright 1998 Paul D. Fernhout and Cynthia F. Kurtz" + chr(13) + "This key generator is confidential intellectual property of the authors" + chr(13) + "and is intended only for use only by the Nelson Ford and his staff" + chr(13) + "at the Public Software Library (PsL) for generation of keys " + chr(13) + "for StoryHarp users who have paid a registration fee.")
        return
    userName = UNRESOLVED.ParamStr(1)
    fileName = UNRESOLVED.ParamStr(2)
    code = generate(userName)
    WriteCodeFile(userName, code, fileName)

def RegistrationMatch(name, code):
    result = false
    collapsedCode = ""
    i = 0
    
    collapsedCode = ""
    for i in range(1, len(code) + 1):
        if (ord(code[i]) >= ord("0")) and (ord(code[i]) <= ord("9")):
            collapsedCode = collapsedCode + code[i]
    result = collapsedCode == generate(name)
    return result

