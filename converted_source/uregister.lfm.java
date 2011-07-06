
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class RegistrationWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    JLabel Label11;
    JLabel Label1;
    JLabel Label2;
    JLabel Label5;
    JLabel Label6;
    JPanel Panel1;
    JTextField registrationNameEdit;
    JLabel Label3;
    JTextField registrationCodeEdit;
    JLabel Label4;
    JTextField orderPageEdit;
    JButton openBrowser;
    JButton close;
    JButton readLicense;
    JButton moreInfo;
    JButton registerMe;
    JButton PrintButton;
    JTextArea thankYou;
    // UNHANDLED_TYPE PrintDialog;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public RegistrationWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("PlantStudio Registration");
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
        this.setBounds(296, 154, 436, 255  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCloseQuery = FormCloseQuery;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent event) {
                FormKeyPress(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        
        
        this.Label11 = new JLabel("Enter your registration name and personalized registration code below, EXACTLY as they appear in the confirmation you received.");
        this.Label11.setBounds(8, 129, 320, 28);
        
        this.Label1 = new JLabel("To purchase a registration code, go to our web site at:");
        this.Label1.setBounds(8, 11, 263, 14);
        
        this.Label2 = new JLabel("and follow the directions there.");
        this.Label2.setBounds(8, 53, 150, 14);
        
        this.Label5 = new JLabel("(Clicking ''Open browser'' may not work depending on your system setup. If it doesn''t, open your browser yourself, copy the address above, and paste it into the address area of your browser.)");
        this.Label5.setBounds(8, 77, 322, 42);
        
        this.Label6 = new JLabel("Then click here ----->");
        this.Label6.setBounds(65, 231, 102, 14);
        
        this.registrationNameEdit = new JTextField("");
        this.registrationNameEdit.setBounds(101, 7, 222, 22);
        
        this.Label3 = new JLabel("Registration Name", displayedMnemonic=KeyEvent.VK_N, labelFor=this.registrationNameEdit);
        this.Label3.setBounds(8, 9, 87, 14);
        //  --------------- UNHANDLED ATTRIBUTE: this.Label3.Alignment = taRightJustify;
        
        this.registrationCodeEdit = new JTextField("");
        this.registrationCodeEdit.setBounds(101, 31, 222, 22);
        
        this.Label4 = new JLabel("Registration Code", displayedMnemonic=KeyEvent.VK_D, labelFor=this.registrationCodeEdit);
        this.Label4.setBounds(10, 33, 85, 14);
        //  --------------- UNHANDLED ATTRIBUTE: this.Label4.Alignment = taRightJustify;
        
        this.Panel1 = new JPanel(null);
        // -- this.Panel1.setLayout(new BoxLayout(this.Panel1, BoxLayout.Y_AXIS));
        this.Panel1.add(registrationNameEdit);
        this.Panel1.add(Label3);
        this.Panel1.add(registrationCodeEdit);
        this.Panel1.add(Label4);
        this.Panel1.setBounds(8, 159, 328, 59);
        
        this.orderPageEdit = new JTextField("http://www.kurtz-fernhout.com/order.htm");
        this.orderPageEdit.setEditable(false);
        this.orderPageEdit.setBounds(8, 29, 220, 22);
        
        this.openBrowser = new JButton("Open browser");
        this.openBrowser.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                openBrowserClick(event);
            }
        });
        this.openBrowser.setMnemonic(KeyEvent.VK_O);
        this.openBrowser.setBounds(234, 29, 87, 21);
        
        this.close = new JButton("Close");
        this.close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                closeClick(event);
            }
        });
        this.close.setMnemonic(KeyEvent.VK_C);
        this.close.setBounds(343, 4, 90, 21);
        
        this.readLicense = new JButton("Read License");
        this.readLicense.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                readLicenseClick(event);
            }
        });
        this.readLicense.setMnemonic(KeyEvent.VK_L);
        this.readLicense.setBounds(343, 67, 90, 21);
        
        this.moreInfo = new JButton("Why Register?");
        this.moreInfo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                moreInfoClick(event);
            }
        });
        this.moreInfo.setMnemonic(KeyEvent.VK_W);
        this.moreInfo.setBounds(343, 40, 90, 23);
        
        this.registerMe = new JButton("Register Me!");
        this.registerMe.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                registerMeClick(event);
            }
        });
        this.registerMe.setMnemonic(KeyEvent.VK_R);
        this.registerMe.setBounds(169, 227, 109, 21);
        
        this.PrintButton = new JButton("Print");
        this.PrintButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PrintButtonClick(event);
            }
        });
        this.PrintButton.setMnemonic(KeyEvent.VK_P);
        this.PrintButton.setBounds(343, 103, 90, 21);
        this.PrintButton.setVisible(false);
        
        this.thankYou = new JTextArea(10, 10);
        this.thankYou.setBounds(344, 234, 333, 250);
        this.thankYou.setEditable(false);
        //  --------------- UNHANDLED ATTRIBUTE: this.thankYou.ScrollBars = ssVertical;
        
        //  ------- UNHANDLED TYPE TPrintDialog: PrintDialog 
        //  --------------- UNHANDLED ATTRIBUTE: this.PrintDialog.Top = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.PrintDialog.Left = 308;
        
        delphiPanel.add(Label11);
        delphiPanel.add(Label1);
        delphiPanel.add(Label2);
        delphiPanel.add(Label5);
        delphiPanel.add(Label6);
        delphiPanel.add(Panel1);
        delphiPanel.add(orderPageEdit);
        delphiPanel.add(openBrowser);
        delphiPanel.add(close);
        delphiPanel.add(readLicense);
        delphiPanel.add(moreInfo);
        delphiPanel.add(registerMe);
        delphiPanel.add(PrintButton);
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(344, 234, 333, 250);;
        scroller1.setViewportView(thankYou);
        delphiPanel.add(scroller1);
        return delphiPanel;
    }
    
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void PrintButtonClick(ActionEvent event) {
        System.out.println("PrintButtonClick");
    }
        
    public void closeClick(ActionEvent event) {
        System.out.println("closeClick");
    }
        
    public void moreInfoClick(ActionEvent event) {
        System.out.println("moreInfoClick");
    }
        
    public void openBrowserClick(ActionEvent event) {
        System.out.println("openBrowserClick");
    }
        
    public void readLicenseClick(ActionEvent event) {
        System.out.println("readLicenseClick");
    }
        
    public void registerMeClick(ActionEvent event) {
        System.out.println("registerMeClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                RegistrationWindow thisClass = new RegistrationWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
