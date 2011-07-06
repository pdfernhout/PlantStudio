
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class AboutWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    ImagePanel splashScreenPicture;
    JLabel versionLabel;
    JButton close;
    JButton registerIt;
    JButton readLicense;
    JButton cancel;
    JButton whyRegister;
    JPanel registrationInfoPanel;
    JLabel noDistributeLabel;
    JLabel timeWarningLabel;
    JLabel hoursLabel;
    JLabel Label4;
    JLabel Label5;
    JLabel Label6;
    ImagePanel unregistered2DExportReminder;
    JLabel Label7;
    JLabel Label1;
    JLabel Label2;
    ImagePanel unregistered3DExportReminder;
    JLabel exportRestrictionLabel;
    JButton supportButton;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public AboutWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle(" ");
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
        this.setBounds(242, 199, 483, 356  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.ActiveControl = registerIt;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        
        
        Image splashScreenPictureImage = toolkit.createImage("../resources/AboutForm_splashScreenPicture.png");
        this.splashScreenPicture = new ImagePanel(new ImageIcon(splashScreenPictureImage));
        this.splashScreenPicture.setBounds(2, 3, 382, 270);
        
        this.versionLabel = new JLabel("version 2.0");
        this.versionLabel.setBounds(13, 75, 68, 16);
        
        this.close = new JButton("Close");
        this.close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                closeClick(event);
            }
        });
        this.close.setMnemonic(KeyEvent.VK_C);
        this.close.setBounds(390, 4, 90, 21);
        
        this.registerIt = new JButton("Register");
        this.registerIt.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                registerItClick(event);
            }
        });
        this.registerIt.setMnemonic(KeyEvent.VK_R);
        this.getRootPane().setDefaultButton(this.registerIt);
        this.registerIt.setBounds(390, 28, 90, 23);
        
        this.readLicense = new JButton("Read License");
        this.readLicense.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                readLicenseClick(event);
            }
        });
        this.readLicense.setMnemonic(KeyEvent.VK_L);
        this.readLicense.setBounds(390, 93, 90, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.setMnemonic(KeyEvent.VK_A);
        this.cancel.setBounds(390, 129, 90, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.ModalResult = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.whyRegister = new JButton("Why Register?");
        this.whyRegister.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                whyRegisterClick(event);
            }
        });
        this.whyRegister.setMnemonic(KeyEvent.VK_W);
        this.getRootPane().setDefaultButton(this.whyRegister);
        this.whyRegister.setBounds(390, 66, 90, 23);
        
        this.noDistributeLabel = new JLabel("Under no circumstances are you licensed to distribute any output or data files created using an unregistered copy of PlantStudio.");
        this.noDistributeLabel.setBounds(8, 221, 327, 28);
        
        this.timeWarningLabel = new JLabel("If you have been using PlantStudio for ten hours or more (in total), you are legally required to register it.");
        this.timeWarningLabel.setBounds(8, 40, 320, 28);
        
        this.hoursLabel = new JLabel("You have been evaluating PlantStudio for 8 hours.");
        this.hoursLabel.setBounds(8, 22, 242, 14);
        
        this.Label4 = new JLabel(" We will remind you to register PlantStudio by");
        this.Label4.setBounds(8, 81, 217, 14);
        
        this.Label5 = new JLabel("- showing you this window when you leave PlantStudio");
        this.Label5.setBounds(26, 121, 270, 14);
        
        this.Label6 = new JLabel("- adding a little picture to your 2D output, like this: ");
        this.Label6.setBounds(26, 141, 238, 14);
        
        Image unregistered2DExportReminderImage = toolkit.createImage("../resources/AboutForm_unregistered2DExportReminder.png");
        this.unregistered2DExportReminder = new ImagePanel(new ImageIcon(unregistered2DExportReminderImage));
        this.unregistered2DExportReminder.setBounds(264, 140, 17, 16);
        
        this.Label7 = new JLabel("These reminders and restrictions will disappear on registration.");
        this.Label7.setBounds(8, 187, 304, 14);
        
        this.Label1 = new JLabel("Thank you for evaluating PlantStudio!");
        this.Label1.setBounds(8, 4, 177, 14);
        
        this.Label2 = new JLabel("- addling a little rectangle to your 3D output, like this:");
        this.Label2.setBounds(26, 162, 249, 14);
        
        Image unregistered3DExportReminderImage = toolkit.createImage("../resources/AboutForm_unregistered3DExportReminder.png");
        this.unregistered3DExportReminder = new ImagePanel(new ImageIcon(unregistered3DExportReminderImage));
        this.unregistered3DExportReminder.setBounds(277, 159, 31, 21);
        
        this.exportRestrictionLabel = new JLabel("- restricting the number of exports to 20 at first, then 2 per session");
        this.exportRestrictionLabel.setBounds(26, 101, 322, 14);
        
        this.registrationInfoPanel = new JPanel(null);
        // -- this.registrationInfoPanel.setLayout(new BoxLayout(this.registrationInfoPanel, BoxLayout.Y_AXIS));
        this.registrationInfoPanel.add(noDistributeLabel);
        this.registrationInfoPanel.add(timeWarningLabel);
        this.registrationInfoPanel.add(hoursLabel);
        this.registrationInfoPanel.add(Label4);
        this.registrationInfoPanel.add(Label5);
        this.registrationInfoPanel.add(Label6);
        this.registrationInfoPanel.add(unregistered2DExportReminder);
        this.registrationInfoPanel.add(Label7);
        this.registrationInfoPanel.add(Label1);
        this.registrationInfoPanel.add(Label2);
        this.registrationInfoPanel.add(unregistered3DExportReminder);
        this.registrationInfoPanel.add(exportRestrictionLabel);
        this.registrationInfoPanel.setBounds(2, 96, 383, 257);
        
        this.supportButton = new JButton("Program Info...");
        this.supportButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                supportButtonClick(event);
            }
        });
        this.supportButton.setMnemonic(KeyEvent.VK_P);
        this.supportButton.setBounds(390, 281, 91, 21);
        
        delphiPanel.add(splashScreenPicture);
        delphiPanel.add(versionLabel);
        delphiPanel.add(close);
        delphiPanel.add(registerIt);
        delphiPanel.add(readLicense);
        delphiPanel.add(cancel);
        delphiPanel.add(whyRegister);
        delphiPanel.add(registrationInfoPanel);
        delphiPanel.add(supportButton);
        return delphiPanel;
    }
    
        
    public void closeClick(ActionEvent event) {
        System.out.println("closeClick");
    }
        
    public void readLicenseClick(ActionEvent event) {
        System.out.println("readLicenseClick");
    }
        
    public void registerItClick(ActionEvent event) {
        System.out.println("registerItClick");
    }
        
    public void supportButtonClick(ActionEvent event) {
        System.out.println("supportButtonClick");
    }
        
    public void whyRegisterClick(ActionEvent event) {
        System.out.println("whyRegisterClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                AboutWindow thisClass = new AboutWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
