# unit Ucollect

"""
from conversion_common import *
import ufiler
import delphi_compatability
"""

def addToListIfAbsent(list, item):
    if item == None:
        return
    if list.IndexOf(item) < 0:
        list.Add(item)

# Pdf port (TList)

class TListCollection:
    def __init__(self, *args):
        self.list = []
        for arg in args:
            self.list.append(arg)
            
    def Clear(self):
        self.list = []
            
    def Add(self, item):
        self.list.append(item)

    def Remove(self, item):
        self.list.remove(item)
                
    def IndexOf(self, item):
        try:
            return self.list.index(item)
        except ValueError:
            return -1
            
    #note this should be virtual in TList but it isn't
    def clear(self):
        self.list = []
    
    def clearPointersWithoutDeletingObjects(self):
        self.list = []
    
    def ForEach(self, proc, data):
        for item in self.list:
            proc(item, data)
    
    def FirstThat(self, testFunc, data):
        result = None
        for item in self.list:
            if testFunc(item, data):
                result = item
                break
        return result
    
    def LastThat(self, testFunc, data):
        result = None
        for i in range(len(self.list) - 1, -1, -1):
            if testFunc(self.list[i], data):
                result = self.list[i]
                break
        return result
    
    def streamUsingFiler(self, filer, classForCreating):
        countOnStream = 0L
        if filer.isReading():
            self.clear()
            countOnStream = filer.streamLongint(countOnStream)
            if countOnStream > 0:
                self.SetCapacity(countOnStream)
                for i in range(0, countOnStream):
                    streamableObject = classForCreating.create
                    streamableObject.streamUsingFiler(filer)
                    self.Add(streamableObject)
        #filer is writing or counting
        else:
            countOnStream = len(self.list)
            filer.streamLongint(countOnStream)
            for streamableObject in self.list:
                streamableObject.streamUsingFiler(filer)
                
    def append(self, item):
        self.list.append(item)
        
    # make it look like a regular Python list
    # probably could subclass from regular list, but not sure would work OK under Jython 
    def __len__(self):
        return len(self.list)
    
    def __getitem__(self, key):
        return self.list[key]
    
    def __setitem__(self, key, value):
        self.list[key] = value
        
    def __delitem__(self, index):
        del self.list[index]
        
    def __iter__(self):
        return self.list.__iter__()
    
    def __contains__(self, item):
        return item in self.list
    
# functions for global clipboard transfer, not using
#    procedure copyToClipboard(classForCreating: PdStreamableObjectClass; format: word);
#    procedure getFromClipboard(classForCreating: PdStreamableObjectClass; format: word);
#
#procedure TListCollection.copyToClipboard(classForCreating: PdStreamableObjectClass; format: word);
#  var
#    memoryStream: TMemoryStream;
#    filer: PdFiler;
#    handleToBuffer: THandle;
#    pointerToBuffer: Pointer;
#  begin
#  memoryStream := TMemoryStream.create;
#  filer := PdFiler.createWithStream(memoryStream);
#  try
#    filer.setToWritingMode;
#    self.streamUsingFiler(filer, classForCreating);
#    handleToBuffer := GlobalAlloc(GMEM_MOVEABLE, memoryStream.size);
#    try
#      pointerToBuffer := GlobalLock(handleToBuffer);
#      try
#        System.Move(memoryStream.memory^, pointerToBuffer^, memoryStream.size);
#        Clipboard.setAsHandle(format, handleToBuffer);
#      finally
#        GlobalUnlock(handleToBuffer);
#      end;
#    except
#      GlobalFree(handleToBuffer);
#      raise;
#    end;
#  finally
#    memoryStream.free;
#    filer.free;
#  end;
#end;
#
#procedure TListCollection.getFromClipboard(classForCreating: PdStreamableObjectClass; format: word);
#  var
#    memoryStream : TMemoryStream;
#    filer: PdFiler;
#    handleToBuffer: THandle;
#    pointerToBuffer: Pointer;
#  begin
#  handleToBuffer := Clipboard.GetAsHandle(format);
#  if handleToBuffer <> 0 then begin
#    pointerToBuffer := GlobalLock(handleToBuffer);
#    if pointerToBuffer <> nil then begin
#      try
#        memoryStream := TMemoryStream.Create;
#        try
#          memoryStream.writeBuffer(pointerToBuffer^, GlobalSize(handleToBuffer));
#          memoryStream.position := 0;
#          filer := PdFiler.createWithStream(memoryStream);
#          filer.setToReadingMode;
#          self.streamUsingFiler(filer, classForCreating);
#        finally
#          memoryStream.free;
#          filer.free;
#        end;
#      finally
#        GlobalUnlock(handleToBuffer);
#      end;
#    end;
#  end;
#end;
#
