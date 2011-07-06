# unit Uexcept

from conversion_common import *
import delphi_compatability

def FailNil(anObject):
    if anObject == None:
        raise GeneralException.create("Problem: Not enough memory to carry out that operation.")

def FailNilPtr(aPointer):
    if aPointer == None:
        raise GeneralException.create("Problem: Not enough memory to carry out that operation.")

def FailNilPChar(aPointer):
    if aPointer == None:
        raise GeneralException.create("Problem: Not enough memory to carry out that operation.")

