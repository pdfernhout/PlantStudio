"""
ReloaderWindow

Author: Paul D. Fernhout 
Copyright 2005, 2007
Released under the Python/Jython license
Version 0.1 2005-12-31 -- Initial release
Version 0.2 2006-01-14 -- Improved copying (using Michael Spencer's suggestions and code ideas) and removed custom file parsing
May now be able to do recursive updates. No longer dependent on parsing a specifically indented file.
Version 0.3 2007-08-24 added support for GTK

Inspired by how Smalltalk handles method changes...

This does a special reload of modules to update the functions in existing classes.
In order to work as expected the reloaded module probably should not be too fancy
in terms of producing a lot of side effects in the system 
when loaded other than defining classes.

Note: this was written for Jython/Swing, 
but this technique should also work for Python with a different GUI

Note: All top level variable definitions are now updated. 
This could pose a problem for you if you store program sate in such globals in moduels you intend to reload.
One solution might be to store such global data in a special module with just globals which you never reload.

Note: May support updating nested classes or nested function definitions (not tested, but code is recursive).

Note: You will likely still need to restart your program occasionally, 
and also  otherwise close and open windows to get changes for new components in __init__,
but maybe only one tenth the time when you can't reload
assuming most changes are adding or changing methods of windows.

Note: if you delete a class or function from your source file,
it will still be available after special reloading, so you need
to restart completely to make it go away.

Note: If your program starts behaving oddly after using the reloader, 
completely restart it to be sure it is not a reloading introduced problem.

Note: if your program uses threads or in some other way
might be doing things with the code when it is reloaded,
I am not sure what will happen.

Note: This code assumes your project runs where the source code is located. 
It only shows you modules in the current directory to reload.

Note: trying to reload the reloader window is not recommended, but may sometimes work.
Any exceptions when reloading fixes to a buggy reloader version may be confusing 
as Python will be running the old code to load the new until it succeeeds
which may be impossible without a clean restart if you broke the reloader.
Also, any changes to the initialization of the reloader window would not
be seen until the window is closed and reopened (which currently exits the JVM).

TO USE: add this code to your startup script under Jython
    import reloader
    window = reloader.ReloaderWindow()
    window.setVisible(1)
    
Under GTK:
    import reloader
    application = MainWindow()
    helper = reloader.ReloaderWindow()
    gtk.main()
"""

# PROBLEMS: when change number of args in function (var args?) in jython
# CALLING SUPER AFTER RELOAD WITH DOUBLE UNDERSCORE
# When add a method, gets first argument wrong

try:
    import java
    jython = 1
except ImportError:
    jython = 0

if jython:
    import java
    from javax.swing import JFrame, JMenuBar, JMenu, JMenuItem, JList, DefaultListModel, JScrollPane, JButton, JPanel, JOptionPane
    from java.awt import BorderLayout
    import org
    BaseWindowClass = JFrame
else:
    import pygtk
    pygtk.require('2.0')
    import gtk
    from gtk_helpers import *
    BaseWindowClass = object
    
import sys
import glob

class ReloaderWindow(BaseWindowClass):
    def __init__(self, title="Development Reloader Window"):
        if jython:
            JFrame.__init__(self, title, windowClosing=self.OnClose)
            self.setBounds(0, 0, 300, 550)
        else:
            self.window = MakeWindow("pyGTK Python Reloader window", 200, 500)
            
        self.BuildWindow()

    def BuildWindow(self):
        if jython:
            contentPane = self.getContentPane()
            contentPane.setLayout(BorderLayout())
            self.fileListUpdateButton = JButton("Update file list", actionPerformed=self.OnUpdateFileList)
            self.fileNamesList = JList(DefaultListModel(), mouseClicked=self.mouseClicked)
            self.specialReloadButton = JButton("Special reload module (or double click)", actionPerformed=self.OnSpecialReloadOfModule)
            self.regularReloadButton = JButton("Regular reload module", actionPerformed=self.OnRegularReloadOfModule)
            contentPane.add("North", self.fileListUpdateButton)
            contentPane.add("Center", JScrollPane(self.fileNamesList))
            reloadButtonPanel = JPanel(BorderLayout())
            reloadButtonPanel.add("North", self.specialReloadButton)
            reloadButtonPanel.add("South", self.regularReloadButton)
            contentPane.add("South", reloadButtonPanel)
        else:
            vbox = MakeVerticalBox(self.window)
            self.fileListUpdateButton = MakeButton(vbox, "Update file list", self.OnUpdateFileList)

            self.fileNamesList = MakeList(vbox, "Python module", None)
            self.fileNamesList.connect("button-press-event", self.mouseClicked)
            
            self.specialReloadButton = MakeButton(vbox, "Special reload module (or double click)", self.OnSpecialReloadOfModule)
            self.regularReloadButton = MakeButton(vbox, "Regular reload module", self.OnRegularReloadOfModule)
           
            ShowWindow(self.window)
        self.loadFileList()

    def loadFileList(self):
        pythonFileNames = glob.glob("./*.py")
        pythonFileNames.sort()
        localModuleNames = []
        for pythonFileName in pythonFileNames:
            localModuleNames.append(pythonFileName[2:-3])
        if jython:
            self.fileNamesList.getModel().clear()
            for moduleName in localModuleNames:
                self.fileNamesList.getModel().addElement(moduleName)
        else:
            tuples = []
            for moduleName in localModuleNames:
                theTuple = (moduleName, moduleName)
                tuples.append(theTuple)
            FillList(self.fileNamesList, tuples)
        
    def mouseClicked(self, eventOrWidget, gtkEvent=None):
        if jython:
            isDoubleClick = eventOrWidget.clickCount == 2
        else:
            isDoubleClick = gtkEvent.type == gtk.gdk._2BUTTON_PRESS
        if isDoubleClick:
            self.OnSpecialReloadOfModule(eventOrWidget)
            
    def OnUpdateFileList(self, event):
        self.loadFileList()
            
    def OnSpecialReloadOfModule(self, event):
        if jython:
            moduleName = self.fileNamesList.getSelectedValue()
        else:
            moduleName = GetListSelection(self.fileNamesList)
        print "Module to reload:", moduleName
        if moduleName:
            self.SpecialReloadForModule(moduleName)

    def OnRegularReloadOfModule(self, event):
        if jython:
            moduleName = self.fileNamesList.getSelectedValue()
        else:
            moduleName = GetListSelection(self.fileNamesList)
        print "Module to reload:", moduleName
        if moduleName:
            warning = """You are about to do a regular reload of module %s.
If you do this, any currently open windows defined in that specific module
will no longer respond to special reloads until the entire program is restarted.
Any other module will not neccessarily use the reloaded code unless it too is reloaded.
Any subsequently opened windows will only use the new code regularly reloaded in this module
if the calling module does an explicit import of the reloaded module before referencing the window and
if the code snippet opening the new window explicitely accesses the reloaded module's window class
as a "module.className()" reference, as opposed to "from module import name" and "className()"
(where the classname would then still point to the previous version).
Confusing? Yes! I'm still not sure I understand it thoroughly myself. :-)
Proceed anyway?""" % moduleName
            title = "Confirm regular reload"
            if jython:
                result = JOptionPane.showConfirmDialog(self, warning, title, JOptionPane.YES_NO_CANCEL_OPTION)
                proceed = (result == JOptionPane.YES_OPTION)
            else:
                proceed = AskYesNoDialog(self.window, warning, title)
            if proceed:
                print "==== starting regular reload of module", moduleName
                reload(sys.modules[moduleName])
                print "== done with regular reload\n"
            else:
                print "reload cancelled"
    # but only if the module that opens them is also regularly reloaded and so on (useless, really)
    
    def OnTestSpecialReloadOfModule(self, event):
        print "do some special test thing here if menu enabled"
        
    def OnClose(self, event):
        #print "Shutting down"
        if jython:
            java.lang.System.exit(0)
        else:
            raise "unfinished"

    def SpecialReloadForModule(self, moduleName):
        print "==== starting special reload of module", moduleName
        oldModule = sys.modules[moduleName]
         # temporarily remove old module and later restore it
        del sys.modules[moduleName]
        try:
            newModule = __import__(moduleName)
        finally:
            sys.modules[moduleName] = oldModule
        print "== special reload of module using update function"
        topLevelNames = newModule.__dict__.keys()
        #print "updating: ",
        for topLevelName in topLevelNames:
            #print "%s; " % topLevelName,
            # Leave deleted functions and globals for now to clutter up.
            # Update all top level variables in module in old module (e.g. classes, functions, imports) 
            # to point to possibly new implementations.
            newObject = newModule.__dict__[topLevelName]
            try:
                oldObject = oldModule.__dict__[topLevelName]
            except KeyError:
                #print "\nnew definition for %s" % (topLevelName)
                oldModule.__dict__[topLevelName] = newObject
                continue
            try:
                update(oldObject, newObject)
                #print "OK"
            except UpdateCopyNeededException:
                #print "could not update %s (class %s), so assigning" % (topLevelName, newObject.__class__)
                oldModule.__dict__[topLevelName] = newObject
            except UpdateException:
                #print "could not update %s (class %s), so assigning" % (topLevelName, newObject.__class__)
                oldModule.__dict__[topLevelName] = newObject
        print "\n===== done with special reload\n"  

indentationString = "    "

# the following recursive update function is from Michael Spencer 
# (with some changes PDF added to run with Jython, and some renaming, and some debugging stuff)
import types 
     
class UpdateException(Exception): pass
class UpdateCopyNeededException(Exception): pass

def update(old_obj, new_obj, nesting=0):
    """Update certain mutable objects (list, dict, function, class, method)
    with new attributes.  This enables adjustments to running code.
    Experimental"""

    if old_obj is new_obj:
        return

    type_obj = type(old_obj)
    
    if type_obj != type(new_obj):
        print indentationString * nesting, "differing types", type_obj, type(new_obj)
        print indentationString * nesting, dir(old_obj)
        print indentationString * nesting, dir(new_obj)
        raise UpdateException("differing types")

    if type_obj == str:
        raise UpdateCopyNeededException("string")
    
    elif jython and (type_obj == org.python.core.PyReflectedFunction):
        raise UpdateCopyNeededException("reflectedfunction")
         
    elif type_obj == list:
        print indentationString * nesting, "list"
        old_obj[:] = new_obj

    elif type_obj == dict:
        print indentationString * nesting, "dict"
        old_obj.clear()
        # PDF -- think the following line will fail?
        old_obj.update(new_obj)

    elif type_obj == types.FunctionType:
        print indentationString * nesting, "types.FunctionType"
        old_obj.func_code = new_obj.func_code
        # PDF func_defaults is readonly in jython version using: so commented out
        # old_obj.func_defaults = new_obj.func_defaults
        old_obj.func_dict = new_obj.func_dict
        old_obj.func_doc = new_obj.func_doc

    elif type_obj is type or type_obj is types.ClassType:
        print indentationString * nesting, "types.ClassType"
        
        DONOTCOPY = ("__name__","__bases__","__base__","__dict__", "__doc__","__weakref__")
        olddict = old_obj.__dict__
        newdict = new_obj.__dict__
        [delattr(old_obj,attr) for attr in olddict.keys()
            if not((attr in newdict) or (attr in DONOTCOPY)) ]
        # PDF changed iteritems to items on nextline as Jython version using does not have that
        for new_attr_contained, new_obj_contained in newdict.items(): 
            print indentationString * nesting, new_attr_contained
            if new_attr_contained in DONOTCOPY:
                continue
            # turns out methods are returned differently in newdict vs. getattr
            new_obj_contained = getattr(new_obj, new_attr_contained)
            try:
                old_obj_contained = getattr(old_obj, new_attr_contained)
                #if new_obj_contained != new_obj_contained2:
                #    raise "Bogus!"
            except AttributeError:
                # New attribute
                setattr(old_obj, new_attr_contained, new_obj_contained)
                continue
            try:
                #print indentationString * nesting, "recursive update call"
                update(old_obj_contained, new_obj_contained, nesting + 1)
            except UpdateCopyNeededException:
                setattr(old_obj, new_attr_contained, new_obj_contained)
            except UpdateException:
                print indentationString * nesting, "except", sys.exc_info()[0]
                setattr(old_obj, new_attr_contained, new_obj_contained)

    elif type_obj is types.MethodType:
        print indentationString * nesting, "types.MethodType"
        #func = new_obj.im_func
        #cls = old_obj.im_class
        #setattr(cls, func.func_name, types.MethodType(func, None, cls))
        update(old_obj.im_func, new_obj.im_func, nesting + 1)

    else:
        print indentationString * nesting, "unknown type", type_obj
        raise UpdateException("Unknown type")

def main():
    application = ReloaderWindow()
    gtk.main()
    
if __name__ == "__main__":
    main()
    