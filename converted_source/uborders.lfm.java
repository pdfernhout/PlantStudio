
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class PrintBordersWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    JLabel printBorderColorInnerLabel;
    JLabel printBorderColorOuterLabel;
    JLabel printBorderWidthInnerLabel;
    JLabel printBorderWidthOuterLabel;
    SpeedButton helpButton;
    JButton Close;
    JButton cancel;
    JCheckBox printBorderInner;
    JCheckBox printBorderOuter;
    JPanel printBorderColorInner;
    JPanel printBorderColorOuter;
    JSpinner printBorderWidthInner;
    JSpinner printBorderWidthOuter;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public PrintBordersWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Print Border");
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
        this.setBounds(616, 226, 274, 103  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [biSystemMenu];
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent event) {
                FormKeyPress(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        
        
        this.printBorderColorInnerLabel = new JLabel("color");
        this.printBorderColorInnerLabel.setBounds(25, 27, 24, 14);
        
        this.printBorderColorOuterLabel = new JLabel("color");
        this.printBorderColorOuterLabel.setBounds(25, 78, 24, 14);
        
        this.printBorderWidthInnerLabel = new JLabel("thickness (pixels)");
        this.printBorderWidthInnerLabel.setBounds(77, 27, 85, 14);
        
        this.printBorderWidthOuterLabel = new JLabel("thickness (pixels)");
        this.printBorderWidthOuterLabel.setBounds(77, 78, 85, 14);
        
        Image helpButtonImage = toolkit.createImage("../resources/PrintBordersForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(211, 63, 60, 21);
        
        this.Close = new JButton("OK");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.Close.setBounds(211, 4, 60, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setBounds(211, 27, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.printBorderInner = new JCheckBox("Draw inner border");
        this.printBorderInner.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                printBorderInnerClick(event);
            }
        });
        this.printBorderInner.setBounds(3, 5, 118, 17);
        
        this.printBorderOuter = new JCheckBox("Draw outer border");
        this.printBorderOuter.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                printBorderOuterClick(event);
            }
        });
        this.printBorderOuter.setBounds(3, 58, 112, 17);
        
        this.printBorderColorInner = new JPanel(null);
        // -- this.printBorderColorInner.setLayout(new BoxLayout(this.printBorderColorInner, BoxLayout.Y_AXIS));
        this.printBorderColorInner.setBounds(53, 26, 15, 15);
        this.printBorderColorInner.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                printBorderColorInnerMouseUp(event);
            }
        });
        
        this.printBorderColorOuter = new JPanel(null);
        // -- this.printBorderColorOuter.setLayout(new BoxLayout(this.printBorderColorOuter, BoxLayout.Y_AXIS));
        this.printBorderColorOuter.setBounds(53, 77, 15, 15);
        this.printBorderColorOuter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                printBorderColorOuterMouseUp(event);
            }
        });
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.printBorderWidthInner = new JSpinner(SpinnerNumberModel(0, 0, 0, 1));
        this.printBorderWidthInner.setBounds(163, 22, 39, 22);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.printBorderWidthOuter = new JSpinner(SpinnerNumberModel(0, 0, 0, 1));
        this.printBorderWidthOuter.setBounds(163, 73, 39, 22);
        
        delphiPanel.add(printBorderColorInnerLabel);
        delphiPanel.add(printBorderColorOuterLabel);
        delphiPanel.add(printBorderWidthInnerLabel);
        delphiPanel.add(printBorderWidthOuterLabel);
        delphiPanel.add(helpButton);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        delphiPanel.add(printBorderInner);
        delphiPanel.add(printBorderOuter);
        delphiPanel.add(printBorderColorInner);
        delphiPanel.add(printBorderColorOuter);
        delphiPanel.add(printBorderWidthInner);
        delphiPanel.add(printBorderWidthOuter);
        return delphiPanel;
    }
    
        
    public void CloseClick(ActionEvent event) {
        System.out.println("CloseClick");
    }
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void printBorderColorInnerMouseUp(MouseEvent event) {
        System.out.println("printBorderColorInnerMouseUp");
    }
        
    public void printBorderColorOuterMouseUp(MouseEvent event) {
        System.out.println("printBorderColorOuterMouseUp");
    }
        
    public void printBorderInnerClick(ActionEvent event) {
        System.out.println("printBorderInnerClick");
    }
        
    public void printBorderOuterClick(ActionEvent event) {
        System.out.println("printBorderOuterClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                PrintBordersWindow thisClass = new PrintBordersWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
