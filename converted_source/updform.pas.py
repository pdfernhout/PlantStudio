# unit Updform

from conversion_common import *
import uhints
import delphi_compatability

class PdForm(TForm):
    def __init__(self):
        pass
    
    def create(self, anOwner):
        TForm.create(self, anOwner)
        uhints.makeAllFormComponentsHaveHints(self)
        return self
    
