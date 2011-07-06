unit URegisterSupport;

interface

type
	RegisterStruct = record
  	s1, s2, s3, s4: integer;
		end;
procedure GenerateFromCommandLine;
function RegistrationMatch(const name: string; const code: string): boolean;

implementation

uses Windows, SysUtils, Forms, Dialogs;

const
  codeArraySize = 9;

procedure WriteCodeFile(const userName: string; const code: string; const fileNameMaybeLeadingPipe: string);
  var
  	success: integer;
  	CodeFile: TextFile;
    tempFileName: string;
    tempFilePath: string;
    fileName: string;
    warningIfExists: boolean;
	begin
  warningIfExists := true;
  if fileNameMaybeLeadingPipe[1] = '|' then
    begin
  	fileName := copy(fileNameMaybeLeadingPipe, 2, length(fileNameMaybeLeadingPipe));
    warningIfExists := false;
    end
  else
    fileName := fileNameMaybeLeadingPipe;
  tempFilePath := ExtractFilePath(fileName);
  if tempFilePath = '' then
    begin
    SetLength(tempFilePath, MAX_PATH + 2);
    GetTempPath(MAX_PATH, pchar(tempFilePath));
    SetLength(tempFilePath, strlen(pchar(tempFilePath))); // maybe plus one??
    end;

  SetLength(tempFileName, MAX_PATH + 2);
  success := GetTempFileName(
    pchar(tempFilePath),	// address of directory name for temporary file
    'shr',	// address of filename prefix
    0,	// number used to create temporary filename
    pchar(tempFileName) 	// address of buffer that receives the new filename
   );

  if success = 0 then
    begin
    ShowMessage(ExtractFileName(Application.ExeName) + ' Unable to generate temporary file name for StoryHarp registration');
    exit;
    end;

  SetLength(tempFileName, strlen(pchar(tempFileName))); // maybe plus one??

	AssignFile(CodeFile, tempFileName);
  Rewrite(CodeFile);
  try
   	writeln(CodeFile, 'StoryHarp 1.x registration information');
 	  writeln(CodeFile, 'Registration Name: ', userName);
  	writeln(CodeFile, 'Registration Code: ', code);
   	Flush(CodeFile);
  finally
		CloseFile(CodeFile);
  end;
  // questionable?
  if FileExists(fileName) then
    begin
    if warningIfExists then
    	begin
			if MessageDlg(
    	 	ExtractFileName(Application.ExeName) +  ': ' + chr(13) +
        		'A problem has occured in the coordination of the PsL order-entry system and' + chr(13) +
       			'the program which generates the StoryHarp registration code output file. ' + chr(13) + chr(13) +
						'The requested output file "' + fileName + '" already exists, and it should not exist.' + chr(13) +
        		'The existing file will be deleted and then created again if you press OK.' + chr(13) +
        		'(If you press Cancel the file will be left as is.)' + chr(13) + chr(13) +
        		'However, because the PsL order-entry system is supposed to be waiting right now' + chr(13) +
        		'for a file with this name to appear, something improper is happening' + chr(13) +
        		'If you see this error, it is possible a registration code for someone else ' + chr(13) +
        		'has already been given to the customer "' + userName + '".'  + chr(13) + chr(13) +
        		'This is a serious error in the way PsL uses this program and should be reported and corrected.' + chr(13) + chr(13) +
        		'If you wish to never see this error again (not recommended), ' + chr(13) +
        		'you can bypass it by putting a "|" at the start of the file path in the second argument.' + chr(13) +
        		'Contact Paul or Cynthia at http://www.kurtz-fernhout.com for details.',
            mtError, [mbOK, mbCancel], 0) <> idOK then
    	exit;
      end;
  	DeleteFile(fileName);
    end;
	AssignFile(CodeFile, tempFileName);
  Rename(CodeFile, fileName);
  end;

function nextRandom(var generator: RegisterStruct): integer;
  var
  	newValue: integer;
	begin
  with generator do
  	begin
  	newValue := s1 +  s2 + 1;   // one added to defeat case of all zeroing out seeds
  	s1 := s2;
 	  s2 := s3;
  	s3 := s4;
  	s4 := newValue mod 65536;
  	result := s1 mod 256;
    end;
	end;

// only used to calculate initial seeds
procedure WarmUp(var generator: RegisterStruct);
  var i: integer;
	begin
  with generator do
    begin
		// SH 897
  	for i := 0 to 897 do
    	nextRandom(generator);
    end;
	end;

procedure ResetGenerator(var generator: RegisterStruct);
	begin
  with generator do
    begin
  	// SH   37903 61164  59082  16777
  	s1 := 37903;
  	s2 := 61164;
  	s3 := 59082;
  	s4 := 16777;
    end;
	end;

// Maybe PS ??? 234    34432    4356   7
function generate(const name: string): string;
  var
    i, j: integer;
    n, nmod: integer;
    letter: char;
    reorganizedName: string;
    remainingLetters: string;
    nameWithOnlyChars: string;
    lowerCaseName: string;
    codeArray: array [0.. (codeArraySize - 1)] of integer;
    generator: RegisterStruct;
  begin
  ResetGenerator(generator);
  with generator do
  	begin
  	result := '';
  	nameWithOnlyChars := '';
  	lowerCaseName := trim(lowercase(name));
  	for i := 1 to length(lowerCaseName) do
    	begin
    	if (ord(lowerCaseName[i]) >= ord('a')) and (ord(lowerCaseName[i]) <= ord('z')) or
    			(ord(lowerCaseName[i]) >= ord('0')) and (ord(lowerCaseName[i]) <= ord('9')) then
     	 nameWithOnlyChars := nameWithOnlyChars + lowerCaseName[i];
    	end;
  	remainingLetters := nameWithOnlyChars;
  	reorganizedName := '';
  	for i := 1 to length(nameWithOnlyChars) do
    	begin
    	letter := nameWithOnlyChars[length(nameWithOnlyChars) + 1 - i];
    	for j := 0 to (ord(letter)) do   //  + i * 7
      	nextRandom(generator);
    	n :=  nextRandom(generator);
    	nmod := n mod length(remainingLetters);
    	reorganizedName := reorganizedName + remainingLetters[nmod + 1];
    	Delete(remainingLetters, nmod + 1, 1);
    	end;
  	for i := 0 to codeArraySize - 1 do
    	codeArray[i] := nextRandom(generator);
  	for i := 1 to length(reorganizedName) do
    	begin
    	letter := reorganizedName[length(reorganizedName) + 1 - i];
    	if letter = ' ' then continue;
    	for j := 0 to (ord(letter)) do   //  + i * 7
      	nextRandom(generator);
    	n :=  nextRandom(generator);
    	nmod := n mod 10;
    	codeArray[i mod codeArraySize] := codeArray[i mod codeArraySize] + nmod;
   	 end;
  	result := '3';
  	for i := 0 to codeArraySize - 1 do
    	result := result + chr(ord('0') + (codeArray[i] mod 10));
    end;
  end;

procedure GenerateFromCommandLine;
  var userName, fileName, code: string;
  begin
  if ParamCount <> 2 then
    begin
    ShowMessage(
    		'Useage: ' + ExtractFileName(Application.ExeName) + ' "user name"  "file name"' + chr(13) + chr(13) +
        'The key code generator ' + ExtractFileName(Application.ExeName) + ' expects two arguments.' + chr(13) +
    		'The first is the user name, and the second is the name of a text file to store the code in.' + chr(13) +
        'Arguments that can have embedded spaces like the user name' + chr(13) + 'must be surrounded by double quotes.'  + chr(13) + chr(13) +
        'Example: ' + ExtractFileName(Application.ExeName) + ' "Joe User"  "C:\temp\dir with spaces\regfile.txt"' + chr(13) + chr(13) +
        'Contact us at http://www.kurtz-fernhout.com for details' + chr(13) + chr(13) +
        'This program operates under the expectation the output file does not exist.' + chr(13) +
        'If for some reason the output file exists when the program is started' + chr(13) +
        'a warning dialog will pop-up requiring OK or Cancel to be pressed.' + chr(13) +
        '(unless you have disabled that warning as explained on that dialog).' + chr(13) + chr(13) +
        'This program is Copyright 1998 Paul D. Fernhout and Cynthia F. Kurtz'  + chr(13) +
        'This key generator is confidential intellectual property of the authors'   + chr(13) +
        'and is intended only for use only by the Nelson Ford and his staff'  + chr(13) +
        'at the Public Software Library (PsL) for generation of keys '  + chr(13) +
        'for StoryHarp users who have paid a registration fee.');
    exit;
    end;
  userName := ParamStr(1);
  fileName := ParamStr(2);
  code := generate(userName);

  WriteCodeFile(userName, code, fileName);
  end;

function RegistrationMatch(const name: string; const code: string): boolean;
  var
  	collapsedCode: string;
  	i: integer;
  begin
  collapsedCode := '';
  for i := 1 to length(code) do
    begin
    if (ord(code[i]) >= ord('0')) and (ord(code[i]) <= ord('9')) then
    	collapsedCode := collapsedCode + code[i];
    end;
  result := collapsedCode = generate(name)
  end;

end.
 