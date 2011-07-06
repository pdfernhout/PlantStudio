
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class DebugWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JList DebugList;
    JButton Close;
    JButton saveListAs;
    JButton clearList;
    JPanel optionsPanel;
    JLabel exceptionLabel;
    JCheckBox showOnExceptionCheckBox;
    JCheckBox logToFile;
    JButton supportButton;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public DebugWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Messages");
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
        this.setBounds(365, 308, 427, 165  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnDestroy = FormDestroy;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.AutoScroll = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poDefaultPosOnly;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/DebugForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(364, 99, 61, 25);
        
        this.DebugList = new JList(new DefaultListModel());
        this.DebugList.setFixedCellHeight(14);
        this.DebugList.setBounds(-136, -110, 497, 249);
        
        this.Close = new JButton("Close");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.Close.setMnemonic(KeyEvent.VK_C);
        this.getRootPane().setDefaultButton(this.Close);
        this.Close.setBounds(364, 4, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.Close.Cancel = True;
        
        this.saveListAs = new JButton("Save as...");
        this.saveListAs.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                saveListAsClick(event);
            }
        });
        this.saveListAs.setMnemonic(KeyEvent.VK_S);
        this.saveListAs.setBounds(365, 39, 60, 21);
        
        this.clearList = new JButton("Clear");
        this.clearList.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                clearListClick(event);
            }
        });
        this.clearList.setMnemonic(KeyEvent.VK_L);
        this.clearList.setBounds(364, 63, 60, 21);
        
        this.exceptionLabel = new JLabel("On message:");
        this.exceptionLabel.setBounds(8, 5, 64, 14);
        
        this.showOnExceptionCheckBox = new JCheckBox("appear");
        this.showOnExceptionCheckBox.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                showOnExceptionCheckBoxClick(event);
            }
        });
        this.showOnExceptionCheckBox.setMnemonic(KeyEvent.VK_A);
        this.showOnExceptionCheckBox.setBounds(83, 5, 68, 17);
        
        this.logToFile = new JCheckBox("log to file");
        this.logToFile.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                logToFileClick(event);
            }
        });
        this.logToFile.setMnemonic(KeyEvent.VK_O);
        this.logToFile.setBounds(146, 5, 77, 17);
        
        this.optionsPanel = new JPanel(null);
        // -- this.optionsPanel.setLayout(new BoxLayout(this.optionsPanel, BoxLayout.Y_AXIS));
        this.optionsPanel.add(exceptionLabel);
        this.optionsPanel.add(showOnExceptionCheckBox);
        this.optionsPanel.add(logToFile);
        this.optionsPanel.setBounds(0, 140, 361, 25);
        
        this.supportButton = new JButton("Info...");
        this.supportButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                supportButtonClick(event);
            }
        });
        this.supportButton.setMnemonic(KeyEvent.VK_I);
        this.supportButton.setBounds(364, 133, 60, 21);
        
        delphiPanel.add(helpButton);
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(-136, -110, 497, 249);;
        scroller1.setViewportView(DebugList);
        delphiPanel.add(scroller1);
        delphiPanel.add(Close);
        delphiPanel.add(saveListAs);
        delphiPanel.add(clearList);
        delphiPanel.add(optionsPanel);
        delphiPanel.add(supportButton);
        return delphiPanel;
    }
    
        
    public void CloseClick(ActionEvent event) {
        System.out.println("CloseClick");
    }
        
    public void clearListClick(ActionEvent event) {
        System.out.println("clearListClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void logToFileClick(ActionEvent event) {
        System.out.println("logToFileClick");
    }
        
    public void saveListAsClick(ActionEvent event) {
        System.out.println("saveListAsClick");
    }
        
    public void showOnExceptionCheckBoxClick(ActionEvent event) {
        System.out.println("showOnExceptionCheckBoxClick");
    }
        
    public void supportButtonClick(ActionEvent event) {
        System.out.println("supportButtonClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                DebugWindow thisClass = new DebugWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
