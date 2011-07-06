
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class TdoEditorWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JButton ok;
    JButton cancel;
    JButton undoLast;
    JButton redoLast;
    JPanel toolbarPanel;
    SpeedButton dragCursorMode;
    SpeedButton magnifyCursorMode;
    SpeedButton scrollCursorMode;
    SpeedButton addTrianglePointsCursorMode;
    SpeedButton removeTriangleCursorMode;
    SpeedButton flipTriangleCursorMode;
    SpeedButton rotateCursorMode;
    JPanel optionsPanel;
    SpeedButton mirrorTdo;
    SpeedButton reverseZValues;
    SpeedButton centerDrawing;
    SpeedButton resetRotations;
    JLabel connectionPointLabel;
    JCheckBox fillTriangles;
    JSpinner plantParts;
    JLabel drawAsLabel;
    JCheckBox drawLines;
    JSpinner circlePointSize;
    JLabel Label1;
    JCheckBox mirrorHalf;
    JSpinner connectionPoint;
    JPanel picturesPanel;
    JPanel verticalSplitter;
    JPanel horizontalSplitter;
    JButton renameTdo;
    JButton writeToDXF;
    JButton writeToPOV;
    JButton ReadFromDXF;
    JButton clearTdo;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public TdoEditorWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("3D Object Editor");
    }
    
    private JPanel getMainContentPane() {
        if (mainContentPane == null) {
            mainContentPane = new JPanel();
            mainContentPane.setLayout(new BorderLayout());
            mainContentPane.add(getDelphiPanel(), BorderLayout.CENTER);
        }
        return mainContentPane;
    }
    public void OnClose(ActionEvent event) {
        System.out.println("Closed");
    }
    
    public JPanel getDelphiPanel() {
        if (delphiPanel != null) return delphiPanel;
        Toolkit toolkit = java.awt.Toolkit.getDefaultToolkit();
        delphiPanel = new JPanel();
        delphiPanel.setLayout(null);
        // -- delphiPanel.setLayout(BoxLayout(contentPane, BoxLayout.Y_AXIS));
        // Font buttonFont = new Font("Arial Narrow", Font.PLAIN, 9);
        // Insets buttonMargin = new Insets(1, 1, 1, 1);
        this.setBounds(505, 155, 447, 383  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent event) {
                FormKeyPress(event);
            }
        });
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent event) {
                FormKeyDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyReleased(java.awt.event.KeyEvent event) {
                FormKeyUp(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poDefaultPosOnly;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnClose = FormClose;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.AutoScroll = False;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/TdoEditorForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(373, 286, 70, 23);
        
        this.ok = new JButton("OK");
        this.ok.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                okClick(event);
            }
        });
        this.ok.setMnemonic(KeyEvent.VK_O);
        this.ok.setBounds(373, 4, 70, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(373, 27, 70, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.undoLast = new JButton("Undo last");
        this.undoLast.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                undoLastClick(event);
            }
        });
        this.undoLast.setMnemonic(KeyEvent.VK_U);
        this.undoLast.setBounds(373, 100, 70, 21);
        
        this.redoLast = new JButton("Redo last");
        this.redoLast.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                redoLastClick(event);
            }
        });
        this.redoLast.setMnemonic(KeyEvent.VK_R);
        this.redoLast.setBounds(373, 124, 70, 21);
        
        Image dragCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_dragCursorMode.png");
        this.dragCursorMode = new SpeedButton(new ImageIcon(dragCursorModeImage));
        this.dragCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                dragCursorModeClick(event);
            }
        });
        this.dragCursorMode.setBounds(79, 3, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.dragCursorMode.GroupIndex = 1;
        
        Image magnifyCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_magnifyCursorMode.png");
        this.magnifyCursorMode = new SpeedButton(new ImageIcon(magnifyCursorModeImage));
        this.magnifyCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                magnifyCursorModeClick(event);
            }
        });
        this.magnifyCursorMode.setBounds(56, 3, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.magnifyCursorMode.GroupIndex = 1;
        
        Image scrollCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_scrollCursorMode.png");
        this.scrollCursorMode = new SpeedButton(new ImageIcon(scrollCursorModeImage));
        this.scrollCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                scrollCursorModeClick(event);
            }
        });
        this.scrollCursorMode.setBounds(6, 3, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.scrollCursorMode.GroupIndex = 1;
        
        Image addTrianglePointsCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_addTrianglePointsCursorMode.png");
        this.addTrianglePointsCursorMode = new SpeedButton(new ImageIcon(addTrianglePointsCursorModeImage));
        this.addTrianglePointsCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                addTrianglePointsCursorModeClick(event);
            }
        });
        this.addTrianglePointsCursorMode.setBounds(104, 3, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.addTrianglePointsCursorMode.GroupIndex = 1;
        
        Image removeTriangleCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_removeTriangleCursorMode.png");
        this.removeTriangleCursorMode = new SpeedButton(new ImageIcon(removeTriangleCursorModeImage));
        this.removeTriangleCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                removeTriangleCursorModeClick(event);
            }
        });
        this.removeTriangleCursorMode.setBounds(129, 3, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.removeTriangleCursorMode.GroupIndex = 1;
        
        Image flipTriangleCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_flipTriangleCursorMode.png");
        this.flipTriangleCursorMode = new SpeedButton(new ImageIcon(flipTriangleCursorModeImage));
        this.flipTriangleCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                flipTriangleCursorModeClick(event);
            }
        });
        this.flipTriangleCursorMode.setBounds(155, 3, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.flipTriangleCursorMode.GroupIndex = 1;
        
        Image rotateCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_rotateCursorMode.png");
        this.rotateCursorMode = new SpeedButton(new ImageIcon(rotateCursorModeImage));
        this.rotateCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                rotateCursorModeClick(event);
            }
        });
        this.rotateCursorMode.setBounds(31, 3, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.rotateCursorMode.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.rotateCursorMode.GroupIndex = 1;
        
        this.toolbarPanel = new JPanel(null);
        // -- this.toolbarPanel.setLayout(new BoxLayout(this.toolbarPanel, BoxLayout.Y_AXIS));
        this.toolbarPanel.add(dragCursorMode);
        this.toolbarPanel.add(magnifyCursorMode);
        this.toolbarPanel.add(scrollCursorMode);
        this.toolbarPanel.add(addTrianglePointsCursorMode);
        this.toolbarPanel.add(removeTriangleCursorMode);
        this.toolbarPanel.add(flipTriangleCursorMode);
        this.toolbarPanel.add(rotateCursorMode);
        this.toolbarPanel.setBounds(-1, -2, 368, 32);
        
        Image mirrorTdoImage = toolkit.createImage("../resources/TdoEditorForm_mirrorTdo.png");
        this.mirrorTdo = new SpeedButton("Mirror", new ImageIcon(mirrorTdoImage));
        this.mirrorTdo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                mirrorTdoClick(event);
            }
        });
        this.mirrorTdo.setBounds(9, 5, 63, 25);
        
        Image reverseZValuesImage = toolkit.createImage("../resources/TdoEditorForm_reverseZValues.png");
        this.reverseZValues = new SpeedButton("Reverse", new ImageIcon(reverseZValuesImage));
        this.reverseZValues.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                reverseZValuesClick(event);
            }
        });
        this.reverseZValues.setBounds(75, 5, 72, 25);
        
        Image centerDrawingImage = toolkit.createImage("../resources/TdoEditorForm_centerDrawing.png");
        this.centerDrawing = new SpeedButton("Scale to Fit", new ImageIcon(centerDrawingImage));
        this.centerDrawing.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                centerDrawingClick(event);
            }
        });
        this.centerDrawing.setBounds(150, 5, 91, 25);
        
        Image resetRotationsImage = toolkit.createImage("../resources/TdoEditorForm_resetRotations.png");
        this.resetRotations = new SpeedButton("Reset rotations", new ImageIcon(resetRotationsImage));
        this.resetRotations.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                resetRotationsClick(event);
            }
        });
        this.resetRotations.setBounds(244, 5, 115, 25);
        
        this.connectionPointLabel = new JLabel("Connection point (1-xx)");
        this.connectionPointLabel.setBounds(65, 92, 113, 14);
        
        this.fillTriangles = new JCheckBox("Fill triangles with solid");
        this.fillTriangles.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                fillTrianglesClick(event);
            }
        });
        this.fillTriangles.setMnemonic(KeyEvent.VK_I);
        this.fillTriangles.setBounds(194, 36, 136, 17);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.plantParts = new JSpinner(SpinnerNumberModel(1, 1, 30, 1));
        this.plantParts.setBounds(8, 35, 51, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.plantParts.OnChange = plantPartsChange;
        
        this.drawAsLabel = new JLabel("Parts (1-30)", displayedMnemonic=KeyEvent.VK_P, labelFor=this.plantParts);
        this.drawAsLabel.setBounds(65, 39, 58, 14);
        
        this.drawLines = new JCheckBox("Draw lines between triangles");
        this.drawLines.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                drawLinesClick(event);
            }
        });
        this.drawLines.setMnemonic(KeyEvent.VK_D);
        this.drawLines.setBounds(194, 55, 166, 17);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.circlePointSize = new JSpinner(SpinnerNumberModel(1, 1, 30, 1));
        this.circlePointSize.setBounds(8, 62, 51, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.circlePointSize.OnChange = circlePointSizeChange;
        
        this.Label1 = new JLabel("Point size (1-30 pixels)", displayedMnemonic=KeyEvent.VK_S, labelFor=this.circlePointSize);
        this.Label1.setBounds(65, 66, 110, 14);
        
        this.mirrorHalf = new JCheckBox("Show mirror image");
        this.mirrorHalf.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                mirrorHalfClick(event);
            }
        });
        this.mirrorHalf.setMnemonic(KeyEvent.VK_M);
        this.mirrorHalf.setBounds(194, 74, 156, 17);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.connectionPoint = new JSpinner(SpinnerNumberModel(1, 1, 200, 1));
        this.connectionPoint.setBounds(8, 88, 51, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.connectionPoint.OnChange = connectionPointChange;
        
        this.optionsPanel = new JPanel(null);
        // -- this.optionsPanel.setLayout(new BoxLayout(this.optionsPanel, BoxLayout.Y_AXIS));
        this.optionsPanel.add(mirrorTdo);
        this.optionsPanel.add(reverseZValues);
        this.optionsPanel.add(centerDrawing);
        this.optionsPanel.add(resetRotations);
        this.optionsPanel.add(connectionPointLabel);
        this.optionsPanel.add(fillTriangles);
        this.optionsPanel.add(plantParts);
        this.optionsPanel.add(drawAsLabel);
        this.optionsPanel.add(drawLines);
        this.optionsPanel.add(circlePointSize);
        this.optionsPanel.add(Label1);
        this.optionsPanel.add(mirrorHalf);
        this.optionsPanel.add(connectionPoint);
        this.optionsPanel.setBounds(0, 264, 367, 117);
        
        this.verticalSplitter = new JPanel(null);
        // -- this.verticalSplitter.setLayout(new BoxLayout(this.verticalSplitter, BoxLayout.Y_AXIS));
        this.verticalSplitter.setBounds(210, 4, 4, 276);
        //  --------------- UNHANDLED ATTRIBUTE: this.verticalSplitter.Cursor = crHSplit;
        this.verticalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseMoved(java.awt.event.MouseEvent event) {
                verticalSplitterMouseMove(event);
            }
        });
        this.verticalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent event) {
                verticalSplitterMouseMove(event);
            }
        });
        this.verticalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                verticalSplitterMouseUp(event);
            }
        });
        this.verticalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                verticalSplitterMouseDown(event);
            }
        });
        
        this.horizontalSplitter = new JPanel(null);
        // -- this.horizontalSplitter.setLayout(new BoxLayout(this.horizontalSplitter, BoxLayout.Y_AXIS));
        this.horizontalSplitter.setBounds(214, 140, 149, 4);
        //  --------------- UNHANDLED ATTRIBUTE: this.horizontalSplitter.Cursor = crVSplit;
        this.horizontalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseMoved(java.awt.event.MouseEvent event) {
                horizontalSplitterMouseMove(event);
            }
        });
        this.horizontalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent event) {
                horizontalSplitterMouseMove(event);
            }
        });
        this.horizontalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                horizontalSplitterMouseUp(event);
            }
        });
        this.horizontalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                horizontalSplitterMouseDown(event);
            }
        });
        
        this.picturesPanel = new JPanel(null);
        // -- this.picturesPanel.setLayout(new BoxLayout(this.picturesPanel, BoxLayout.Y_AXIS));
        this.picturesPanel.add(verticalSplitter);
        this.picturesPanel.add(horizontalSplitter);
        this.picturesPanel.setBounds(0, 29, 367, 235);
        
        this.renameTdo = new JButton("Rename");
        this.renameTdo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                renameTdoClick(event);
            }
        });
        this.renameTdo.setMnemonic(KeyEvent.VK_N);
        this.renameTdo.setBounds(373, 63, 70, 21);
        
        this.writeToDXF = new JButton("Write DXF...");
        this.writeToDXF.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                writeToDXFClick(event);
            }
        });
        this.writeToDXF.setMnemonic(KeyEvent.VK_X);
        this.writeToDXF.setBounds(373, 196, 70, 21);
        
        this.writeToPOV = new JButton("Write POV...");
        this.writeToPOV.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                writeToPOVClick(event);
            }
        });
        this.writeToPOV.setMnemonic(KeyEvent.VK_P);
        this.writeToPOV.setBounds(373, 251, 70, 21);
        
        this.ReadFromDXF = new JButton("Read DXF...");
        this.ReadFromDXF.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                ReadFromDXFClick(event);
            }
        });
        this.ReadFromDXF.setMnemonic(KeyEvent.VK_F);
        this.ReadFromDXF.setBounds(373, 222, 70, 23);
        
        this.clearTdo = new JButton("Clear points");
        this.clearTdo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                clearTdoClick(event);
            }
        });
        this.clearTdo.setMnemonic(KeyEvent.VK_L);
        this.clearTdo.setBounds(373, 159, 70, 21);
        
        delphiPanel.add(helpButton);
        delphiPanel.add(ok);
        delphiPanel.add(cancel);
        delphiPanel.add(undoLast);
        delphiPanel.add(redoLast);
        delphiPanel.add(toolbarPanel);
        delphiPanel.add(optionsPanel);
        delphiPanel.add(picturesPanel);
        delphiPanel.add(renameTdo);
        delphiPanel.add(writeToDXF);
        delphiPanel.add(writeToPOV);
        delphiPanel.add(ReadFromDXF);
        delphiPanel.add(clearTdo);
        return delphiPanel;
    }
    
        
    public void FormKeyDown(KeyEvent event) {
        System.out.println("FormKeyDown");
    }
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void FormKeyUp(KeyEvent event) {
        System.out.println("FormKeyUp");
    }
        
    public void ReadFromDXFClick(ActionEvent event) {
        System.out.println("ReadFromDXFClick");
    }
        
    public void addTrianglePointsCursorModeClick(ActionEvent event) {
        System.out.println("addTrianglePointsCursorModeClick");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void centerDrawingClick(ActionEvent event) {
        System.out.println("centerDrawingClick");
    }
        
    public void clearTdoClick(ActionEvent event) {
        System.out.println("clearTdoClick");
    }
        
    public void dragCursorModeClick(ActionEvent event) {
        System.out.println("dragCursorModeClick");
    }
        
    public void drawLinesClick(ActionEvent event) {
        System.out.println("drawLinesClick");
    }
        
    public void fillTrianglesClick(ActionEvent event) {
        System.out.println("fillTrianglesClick");
    }
        
    public void flipTriangleCursorModeClick(ActionEvent event) {
        System.out.println("flipTriangleCursorModeClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void horizontalSplitterMouseDown(MouseEvent event) {
        System.out.println("horizontalSplitterMouseDown");
    }
        
    public void horizontalSplitterMouseMove(MouseEvent event) {
        System.out.println("horizontalSplitterMouseMove");
    }
        
    public void horizontalSplitterMouseUp(MouseEvent event) {
        System.out.println("horizontalSplitterMouseUp");
    }
        
    public void magnifyCursorModeClick(ActionEvent event) {
        System.out.println("magnifyCursorModeClick");
    }
        
    public void mirrorHalfClick(ActionEvent event) {
        System.out.println("mirrorHalfClick");
    }
        
    public void mirrorTdoClick(ActionEvent event) {
        System.out.println("mirrorTdoClick");
    }
        
    public void okClick(ActionEvent event) {
        System.out.println("okClick");
    }
        
    public void redoLastClick(ActionEvent event) {
        System.out.println("redoLastClick");
    }
        
    public void removeTriangleCursorModeClick(ActionEvent event) {
        System.out.println("removeTriangleCursorModeClick");
    }
        
    public void renameTdoClick(ActionEvent event) {
        System.out.println("renameTdoClick");
    }
        
    public void resetRotationsClick(ActionEvent event) {
        System.out.println("resetRotationsClick");
    }
        
    public void reverseZValuesClick(ActionEvent event) {
        System.out.println("reverseZValuesClick");
    }
        
    public void rotateCursorModeClick(ActionEvent event) {
        System.out.println("rotateCursorModeClick");
    }
        
    public void scrollCursorModeClick(ActionEvent event) {
        System.out.println("scrollCursorModeClick");
    }
        
    public void undoLastClick(ActionEvent event) {
        System.out.println("undoLastClick");
    }
        
    public void verticalSplitterMouseDown(MouseEvent event) {
        System.out.println("verticalSplitterMouseDown");
    }
        
    public void verticalSplitterMouseMove(MouseEvent event) {
        System.out.println("verticalSplitterMouseMove");
    }
        
    public void verticalSplitterMouseUp(MouseEvent event) {
        System.out.println("verticalSplitterMouseUp");
    }
        
    public void writeToDXFClick(ActionEvent event) {
        System.out.println("writeToDXFClick");
    }
        
    public void writeToPOVClick(ActionEvent event) {
        System.out.println("writeToPOVClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                TdoEditorWindow thisClass = new TdoEditorWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
