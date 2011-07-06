import java
from java.lang import Class, Runnable
import javax.swing.filechooser
from javax.swing import SwingUtilities, SwingConstants, WindowConstants, \
        AbstractAction, BorderFactory, Box, BoxLayout, ImageIcon, \
        JDialog, JFrame, JScrollPane, JPanel, JComponent, JSplitPane, \
        JColorChooser, JOptionPane, JFileChooser, \
        JTextArea, JTextField, JLabel, JPasswordField, JEditorPane, JTextPane, \
        JButton, JCheckBox, JRadioButton, JToggleButton, ButtonGroup, \
        JMenuItem, JCheckBoxMenuItem, JRadioButtonMenuItem, JMenuBar, JMenu, JPopupMenu, KeyStroke, \
        JTree, \
        JComboBox, DefaultComboBoxModel, \
        JTable, \
        JList, ListSelectionModel, DefaultListCellRenderer, DefaultListModel, \
        JSlider, \
        JSpinner, SpinnerNumberModel, SpinnerListModel, SpinnerDateModel, JFormattedTextField, \
        JTabbedPane
from javax.swing.table import DefaultTableModel
from javax.swing.event import ChangeListener, TreeSelectionListener, ListSelectionListener, HyperlinkEvent
from java.awt.event import ActionListener, MouseAdapter, MouseMotionAdapter, MouseEvent, WindowFocusListener, MouseListener, KeyEvent
from javax.swing.text.html import HTMLEditorKit, FormView, HTML
from javax.swing.text import StyleConstants, SimpleAttributeSet
from javax.swing.tree import DefaultMutableTreeNode, DefaultTreeModel, DefaultTreeCellRenderer
from javax.swing.border import BevelBorder, TitledBorder

from java.awt import Color, Cursor, BorderLayout, Font, Dimension, Rectangle, Component, Font, Polygon, FlowLayout, Insets
from java.awt.datatransfer import DataFlavor, Transferable
from java.awt.dnd import DropTarget, DnDConstants, DropTargetAdapter, DragSourceListener, \
        DragGestureListener, DragSource, DragSourceAdapter

import sys, traceback
import copy
import os

# in swing, if you make an action, it can be shared by toolbars, menus, buttons, and so on
# so enabling and disabling can be done to the action and all users also enable or disable
class CallbackAction(AbstractAction):
    """ Action that calls a callback method """
    def __init__(self, callback, name, description):
        AbstractAction.__init__(self)
        # kludge for checkbox
        self.menuItem = None
        self.callback = callback
        self.putValue(self.NAME, name)
        if description:
            self.putValue(self.SHORT_DESCRIPTION, description)
 
    def actionPerformed(self, event):
        self.callback(event)
        
    def setMenuItem(self, menuItem):
        self.menuItem = menuItem
        
    def setChecked(self, isChecked):
        self.menuItem.setSelected(isChecked)
        
    def setCaption(self, newCaption):
        self.menuItem.text = newCaption

#example:
# self.actionMyAction = createAction(self.OnMyAction, "My Action", None, self.myMenu, "L", menuItemType="checkbox")   

# basic idea derived from: http://sourceforge.net/mailarchive/forum.php?thread_id=6060968&forum_id=5586
def createAction(callback, name, description=None, menu=None, mnemonic=None, accelerator=None, toolBar=None, menuItemType="standard"):
    action = CallbackAction(callback, name, description)
    if menu:
        if menuItemType == "standard":
            menuItem = JMenuItem(action)
        elif menuItemType == "checkbox":
            menuItem = JCheckBoxMenuItem(action)
        elif menuItemType == "radiobutton":
            menuItem = JRadioButtonMenuItem(action)
        else:
            internal_error("unsupported menu item type %s" % `menuItemType`)
            menuItem = JMenuItem(action)
        if mnemonic:
            menuItem.setMnemonic(mnemonic)
        if accelerator:
            menuItem.setAccelerator(KeyStroke.getKeyStroke(ord(accelerator), Event.CTRL_MASK, 0))
        menu.add(menuItem)
        action.setMenuItem(menuItem)
    if toolBar:
        toolbarButton = JButton(action)
        toolBar.add(toolbarButton)
    return action

# for displaying retrievable data in lists with a specific name  
class NamedDataListItem(java.lang.Object):
    def __init__(self, name, data):
        self.name = name
        self.data = data
        
    def toString(self):
        return self.name
   
# ensure it is only the left button you are handling
# see below for other class for menu handling
# use: component.addMouseListener(CallbackLeftMouseButtonListener(self.myFunction))
class CallbackLeftMouseButtonListener(MouseAdapter):
    def __init__(self, callback):
        self.callback = callback   
    def mousePressed(self, event):
        if SwingUtilities.isLeftMouseButton(event):
            self.callback(event, 1)
    def mouseReleased(self, event):
        if SwingUtilities.isLeftMouseButton(event):
            self.callback(event, 0)
        
class CallbackMouseMotionListener(MouseMotionAdapter):
    def __init__(self, callback):
        self.callback = callback   
    def mouseMoved(self, event):
        self.callback(event, 0)
    def mouseDragged(self, event):
        self.callback(event, 1)
  
# might want to enable/disable menu items before popping it up?
class CallbackPopupMouseListener(MouseAdapter):
    def __init__(self, callback):
        self.callback = callback   
    def mousePressed(self, event):
        self.checkForTriggerEvent(event)
    def mouseReleased(self, event):
        self.checkForTriggerEvent(event)
    def checkForTriggerEvent(self, event):
        if (event.isPopupTrigger()):  
            self.callback(event)
            
# better to use this than handle in mousePressed/mouseReleased yourself
# to ensure both cases are covered (windows and linux differ on which to do it in)
# use: component.addMouseListener(MenuPopupMouseListener(self.myPopupMenu))
class MenuPopupMouseListener(MouseAdapter):
    def __init__(self, popupMenu):
        self.popupMenu = popupMenu
    def mousePressed(self, event):
        self.checkForTriggerEvent(event)
    def mouseReleased(self, event):
        self.checkForTriggerEvent(event)
    def checkForTriggerEvent(self, event):
        if (event.isPopupTrigger()): 
            self.popupMenu.show(event.getComponent(), event.getX(), event.getY())  

# should not take focus
class SpeedButton(JToggleButton):
    pass

# should use JSpinner?
class SpinButton(JButton):
    pass

class ImagePanel(JPanel):
    def __init__(self, imageIcon=None):
        JPanel.__init__(self)
        self.imageIcon = imageIcon
        
    def paintComponent(self, g):
        #JComponent.paintComponent(self, g)

        #draw entire component white
        g.setColor(Color.white)
        g.fillRect(0, 0, self.getWidth(), self.getHeight())

        #yellow circle
        g.setColor(Color.yellow)
        g.fillOval(0, 0, 240, 240)

        #magenta circle
        g.setColor(Color.magenta);
        g.fillOval(160, 160, 240, 240)
        
        if self.imageIcon:
            #i = self.imageIcon.getImage()
            #print "i", i, i.getWidth(self), i.getHeight(self)
            #bi = self.createImage(i.getWidth(self),i.getHeight(self))
            #print "bi", bi
            #g = bi.createGraphics()    # Get a Graphics2D object
            #print "g", g
            #g.drawImage(i, 0, 0, self)    # Draw the Image data into the BufferedImage
        
            self.imageIcon.paintIcon(self, g, 0, 0)
        
        #self.toolX, self.toolY = MouseInfo.getPointerInfo().getLocation()
        #self.toolIcon.paintIcon(self, g, self.toolX-self.hotspotX, self.toolY-self.hotspotY)

    def getPreferredSize(self):
        if not self.imageIcon:
            return Dimension(16, 16)
        else:
            return Dimension(self.imageIcon.image.getWidth(self), self.imageIcon.image.getHeight(self))

    def getMinimumSize(self):
        return self.getPreferredSize()

class FileFilterByExtensions(javax.swing.filechooser.FileFilter):
    def __init__(self, name, extensions):
        self.name = name
        self.extensions = extensions
        if "*" in extensions:
            self.acceptAll = 1
        else:
            self.acceptAll = 0
    def accept(self, f):
        if self.acceptAll:
            return 1
        fileName = f.getName()
        # ext includes period
        ext = os.path.splitext(fileName)[1]
        if ext and ext[0] == '.':
            ext = ext[1:len(ext)]
        match = ext in self.extensions
        return match
    def getDescription(self):
        return self.name
    

# PDF NEXT TWO FOR TESTING
class DoesNothingFunction:
    def __init__(self, className, functionName):
        self.className = className
        self.functionName = functionName
        
    def __call__(self, *args):
        print "DoesNothingFunction called:", self.className, self.functionName
        if self.functionName == "goodPosition":
            import delphi_support
            return delphi_support.point(0, 0)            
        return "TEMP PROXY"
    
class DiscardCallsObject:
    def __init__(self, name):
        self.className = name
        
    def __getattr__(self, attributeName):
        print "DiscardCallsObject", attributeName
        return DoesNothingFunction(self.className, attributeName)
        
#x = DiscardCallsObject("FooClass")
#x.foo()

class CallbackListCellRenderer(DefaultListCellRenderer):
    def __init__(self, callbackFunction):
        self.callbackFunction = callbackFunction
        self.list = None
        self.value = None
        self.index = None
        self.isSelected = None
        self.hasFocus = None
        
    def getListCellRendererComponent(self, list, value, index, isSelected, hasFocus):
        self.list = list
        self.value = value
        self.index = index
        self.isSelected = isSelected
        self.hasFocus = hasFocus
        return self

    def paintComponent(self, g):
        print "paintComponent", self.x, self.y, self.width, self.height, self.index, self.value
        self.callbackFunction(self.list, self.value, self.index, self.isSelected, self.hasFocus, g, self.x, self.y, self.width, self.height)
