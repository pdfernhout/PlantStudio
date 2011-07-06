##########################  GUI helper functions ############################
# Swing version

from common import *

###### MAIN WINDOW AND PACKING SIMPLE WIDGETS #############

def MakeWindow(name, x=500, y=500):
    window = JFrame(name) # , windowClosing=self.OnClose)
    #window.set_default_size(x, y)
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
    return window
    
def ShowWindow(window):
    # according to: http://gtk.php.net/manual1/en/html/gtk.gtkwidget.method.show_all.html 
    # "The extent to which it 'sees' children is system-dependant"
    # window.show_all()
    window.visible = 1
    
class WrappedFunctionForEvent:
    # does not handle None data properly if meant to be passed
    def __init__(self, function, data=None):
        self.function = function
        self.data = data
        
    def __call__(self, event):
        if self.data:
            self.function(event, self.data)
        else:
            self.function(event)
        
def MakeButton(box, name, clickedMethod, data=None):
    button = JButton(name)
    if clickedMethod:
        if data == None:
            button.actionPerformed = clickedMethod
        else:
            button.actionPerformed = WrappedFunctionForEvent(clickedMethod, data)           
    box.add(button) # , False, True, 2)
    button.show()
    return button

def MakeVerticalBox(parent, homogeneous=False):
    vbox = Box.createVerticalBox()
    #if parent.__class__ is gtk.Window:
    parent.add(vbox)
    #else:
    #    parent.pack_start(vbox, False, True, 2) 
    return vbox    
             
def MakeHorizontalBox(parent, homogeneous=True):
    hbox = Box.createHorizontalBox()
    parent.add(hbox)
    #parent.add(hbox, False, True, 2)
    return hbox
            
def PackBox(box, widget, expand=1, border=2):
    #box.pack_start(widget, expand=expand, fill=True, padding=2)
    box.add(widget)
    widget.show()
    
def InvalidateWidget(widget):
    widget.repaint()
    
################# LIST #################

class MyList(JList):
    pass

def MakeList(parent, title, selectionChangedMethod):
    model = DefaultListModel()
    list = MyList(model)
    parent.add(list)
    list.valueChanged = selectionChangedMethod
    return list
    
def FillList(list, nameValuePairs):
    list.values = []
    model = list.model
    model.clear()
    for name, value in nameValuePairs:
        list.values.append(value)
        model.addElement(name)
        
def GetListSelection(list):
    index = list.getSelectedIndex()
    if index == -1:
        return None
    return list.values[index]

############# GRID ###################


    
############### DIALOGS ###############

def AskYesNoDialog(parent, question, title=None):
    if title == None:
        title = question
    msgbox = gtk.MessageDialog(parent, buttons=gtk.BUTTONS_YES_NO, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_QUESTION, message_format=question)
    msgbox.set_title(title)
    result = msgbox.run()
    msgbox.destroy()
    if result == gtk.RESPONSE_YES:
        return True
    else:
        return False
    
  
# example fileTypes = ["*.bmp", "*.png"]
def ChooseFile(parent, fileTypesName="Data", fileTypes=None):
    fileChooser = JFileChooser()
    #if fileTypes:
    #    for fileType in fileTypes:
    #       fileChooser.addChoosableFileFilter(MyFilter())
    returnVal = fileChooser.showOpenDialog(parent)
    if returnVal == JFileChooser.APPROVE_OPTION:
        file = fileChooser.getSelectedFile()
        return file.getName()
    return None

    ################# NO LONGER USED
        
    
    dialog = gtk.FileChooserDialog("Open..",
                               parent,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    
    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    dialog.add_filter(filter)
    
    if fileTypes:
        filter = gtk.FileFilter()
        filter.set_name(fileTypesName)
        for fileType in fileTypes:
            filter.add_pattern(fileType)
            #filter.add_mime_type("image/png")
        dialog.add_filter(filter)
        dialog.set_filter(filter)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        result = dialog.get_filename()
    elif response == gtk.RESPONSE_CANCEL:
        result = None
    dialog.destroy()
    return result

############# DRAWING #####################

def delphi_to_gdk_color(window, value):
    b = (value & 0xff0000) >> 16
    g = (value & 0x00ff00) >> 8
    r = (value & 0x0000ff)
    return Color(r, g, b)

def DrawRectangle(widget, gc, rect, penWidth, penColor, brushColor, filled=1):
    gc.set_line_attributes(penWidth, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)
    gc.set_fill(gtk.gdk.SOLID)
    penColor = delphi_to_gdk_color(widget, penColor)
    brushColor = delphi_to_gdk_color(widget, brushColor)
    gc.set_foreground(brushColor)
    widget.draw_rectangle(gc, filled, rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)

def MeasureTextWidth(widget, gc, text):
    # PDF PORT FIX THIS!!!!
    return len(text) * 12

def MeasureTextHeight(widget, gc, text):
    # PDF PORT FIX THIS!!!!
    return 12

def DrawText(widget, gc, textDrawRect, text, font, brushColor):
    brushColor = delphi_to_gdk_color(widget, brushColor)
    # deprecated -- should use pango layout
    # http://www.moeraki.com/pygtktutorial/pygtk2tutorial/sec-DrawingMethods.html
    gc.set_foreground(brushColor)
    widget.draw_text(font, gc, textDrawRect.left, textDrawRect.top, text)
