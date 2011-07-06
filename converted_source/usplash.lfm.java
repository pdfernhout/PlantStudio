
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class SplashWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    ImagePanel splashImage256Colors;
    JLabel versionLabel;
    JLabel loadingLabel;
    JLabel codeLabel;
    ImagePanel splashImageTrueColor;
    SpeedButton close;
    SpeedButton supportButton;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public SplashWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("FIX WINDOW TITLE");
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
        this.setBounds(349, 213, 379, 269  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsNone;
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
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        this.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                FormMouseDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        this.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                FormClick(event);
            }
        });
        
        
        Image splashImage256ColorsImage = toolkit.createImage("../resources/SplashForm_splashImage256Colors.png");
        this.splashImage256Colors = new ImagePanel(new ImageIcon(splashImage256ColorsImage));
        this.splashImage256Colors.setBounds(0, 0, 382, 270);
        this.splashImage256Colors.setVisible(false);
        this.splashImage256Colors.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                splashImage256ColorsClick(event);
            }
        });
        
        this.versionLabel = new JLabel("version 0.1");
        this.versionLabel.setBounds(13, 81, 68, 16);
        this.versionLabel.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                controlClick(event);
            }
        });
        
        this.loadingLabel = new JLabel("Registered to:");
        this.loadingLabel.setBounds(33, 107, 88, 16);
        this.loadingLabel.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                controlClick(event);
            }
        });
        
        this.codeLabel = new JLabel("Name");
        this.codeLabel.setBounds(127, 107, 37, 16);
        this.codeLabel.setVisible(false);
        this.codeLabel.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                controlClick(event);
            }
        });
        
        Image splashImageTrueColorImage = toolkit.createImage("../resources/SplashForm_splashImageTrueColor.png");
        this.splashImageTrueColor = new ImagePanel(new ImageIcon(splashImageTrueColorImage));
        this.splashImageTrueColor.setBounds(109, -167, 382, 270);
        this.splashImageTrueColor.setVisible(false);
        this.splashImageTrueColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                splashImage256ColorsClick(event);
            }
        });
        
        Image closeImage = toolkit.createImage("../resources/SplashForm_close.png");
        this.close = new SpeedButton(new ImageIcon(closeImage));
        this.close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                closeClick(event);
            }
        });
        this.close.setBounds(274, 134, 92, 29);
        //  --------------- UNHANDLED ATTRIBUTE: this.close.Flat = True;
        this.close.setVisible(false);
        
        Image supportButtonImage = toolkit.createImage("../resources/SplashForm_supportButton.png");
        this.supportButton = new SpeedButton(new ImageIcon(supportButtonImage));
        this.supportButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                supportButtonClick(event);
            }
        });
        this.supportButton.setBounds(274, 171, 92, 26);
        //  --------------- UNHANDLED ATTRIBUTE: this.supportButton.Flat = True;
        this.supportButton.setVisible(false);
        
        delphiPanel.add(splashImage256Colors);
        delphiPanel.add(versionLabel);
        delphiPanel.add(loadingLabel);
        delphiPanel.add(codeLabel);
        delphiPanel.add(splashImageTrueColor);
        delphiPanel.add(close);
        delphiPanel.add(supportButton);
        return delphiPanel;
    }
    
        
    public void FormClick(MouseEvent event) {
        System.out.println("FormClick");
    }
        
    public void FormKeyDown(KeyEvent event) {
        System.out.println("FormKeyDown");
    }
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void FormMouseDown(MouseEvent event) {
        System.out.println("FormMouseDown");
    }
        
    public void closeClick(ActionEvent event) {
        System.out.println("closeClick");
    }
        
    public void controlClick(MouseEvent event) {
        System.out.println("controlClick");
    }
        
    public void splashImage256ColorsClick(MouseEvent event) {
        System.out.println("splashImage256ColorsClick");
    }
        
    public void supportButtonClick(ActionEvent event) {
        System.out.println("supportButtonClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                SplashWindow thisClass = new SplashWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
