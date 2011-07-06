
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class ProgramInfoWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JButton Close;
    JButton saveListAs;
    JButton copyToClipboard;
    JTextArea infoList;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public ProgramInfoWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Program Information");
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
        this.setBounds(310, 266, 450, 301  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 13;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.AutoScroll = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/ProgramInfoForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(332, 135, 113, 25);
        
        this.Close = new JButton("Close");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.Close.setMnemonic(KeyEvent.VK_C);
        this.Close.setBounds(332, 4, 113, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.Close.Cancel = True;
        
        this.saveListAs = new JButton("Save as...");
        this.saveListAs.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                saveListAsClick(event);
            }
        });
        this.saveListAs.setMnemonic(KeyEvent.VK_S);
        this.saveListAs.setBounds(332, 83, 113, 21);
        
        this.copyToClipboard = new JButton("Copy to Clipboard");
        this.copyToClipboard.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyToClipboardClick(event);
            }
        });
        this.copyToClipboard.setMnemonic(KeyEvent.VK_P);
        this.copyToClipboard.setBounds(332, 55, 113, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.copyToClipboard.Cancel = True;
        
        this.infoList = new JTextArea(10, 10);
        this.infoList.setBounds(2, 2, 323, 295);
        //  --------------- UNHANDLED ATTRIBUTE: this.infoList.ScrollBars = ssVertical;
        
        delphiPanel.add(helpButton);
        delphiPanel.add(Close);
        delphiPanel.add(saveListAs);
        delphiPanel.add(copyToClipboard);
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(2, 2, 323, 295);;
        scroller1.setViewportView(infoList);
        delphiPanel.add(scroller1);
        return delphiPanel;
    }
    
        
    public void CloseClick(ActionEvent event) {
        System.out.println("CloseClick");
    }
        
    public void copyToClipboardClick(ActionEvent event) {
        System.out.println("copyToClipboardClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void saveListAsClick(ActionEvent event) {
        System.out.println("saveListAsClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                ProgramInfoWindow thisClass = new ProgramInfoWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
