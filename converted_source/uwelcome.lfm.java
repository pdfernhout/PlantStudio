
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class WelcomeWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    JLabel Label3;
    JLabel Label1;
    ImagePanel Image1;
    JCheckBox hideWelcomeForm;
    JButton readQuickStartTipList;
    JButton readTutorial;
    JButton makeNewPlant;
    JButton openPlantLibrary;
    JButton startUsingProgram;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public WelcomeWindow() {
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
        this.setBounds(375, 189, 247, 250  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        
        
        this.Label3 = new JLabel(" What would you like to do first?");
        this.Label3.setBounds(42, 51, 155, 14);
        
        this.Label1 = new JLabel(" Welcome to PlantStudio!");
        this.Label1.setBounds(9, 8, 136, 14);
        
        Image Image1Image = toolkit.createImage("../resources/WelcomeForm_Image1.png");
        this.Image1 = new ImagePanel(new ImageIcon(Image1Image));
        this.Image1.setBounds(3, 1, 241, 45);
        
        this.hideWelcomeForm = new JCheckBox("Don''t show this window next time");
        this.hideWelcomeForm.setMnemonic(KeyEvent.VK_D);
        this.hideWelcomeForm.setBounds(29, 230, 190, 17);
        
        this.readQuickStartTipList = new JButton("Read the Super-Speed Tour");
        this.readQuickStartTipList.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                readQuickStartTipListClick(event);
            }
        });
        this.readQuickStartTipList.setMnemonic(KeyEvent.VK_S);
        this.readQuickStartTipList.setBounds(45, 73, 160, 25);
        
        this.readTutorial = new JButton("Read the Tutorial");
        this.readTutorial.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                readTutorialClick(event);
            }
        });
        this.readTutorial.setMnemonic(KeyEvent.VK_T);
        this.readTutorial.setBounds(45, 102, 160, 25);
        
        this.makeNewPlant = new JButton("Make a New Plant");
        this.makeNewPlant.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                makeNewPlantClick(event);
            }
        });
        this.makeNewPlant.setMnemonic(KeyEvent.VK_N);
        this.makeNewPlant.setBounds(45, 133, 160, 25);
        
        this.openPlantLibrary = new JButton("Open a Plant Library");
        this.openPlantLibrary.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                openPlantLibraryClick(event);
            }
        });
        this.openPlantLibrary.setMnemonic(KeyEvent.VK_O);
        this.openPlantLibrary.setBounds(45, 162, 160, 25);
        
        this.startUsingProgram = new JButton("Start Using the Program");
        this.startUsingProgram.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                startUsingProgramClick(event);
            }
        });
        this.startUsingProgram.setMnemonic(KeyEvent.VK_U);
        this.startUsingProgram.setBounds(45, 191, 160, 25);
        
        delphiPanel.add(Label3);
        delphiPanel.add(Label1);
        delphiPanel.add(Image1);
        delphiPanel.add(hideWelcomeForm);
        delphiPanel.add(readQuickStartTipList);
        delphiPanel.add(readTutorial);
        delphiPanel.add(makeNewPlant);
        delphiPanel.add(openPlantLibrary);
        delphiPanel.add(startUsingProgram);
        return delphiPanel;
    }
    
        
    public void makeNewPlantClick(ActionEvent event) {
        System.out.println("makeNewPlantClick");
    }
        
    public void openPlantLibraryClick(ActionEvent event) {
        System.out.println("openPlantLibraryClick");
    }
        
    public void readQuickStartTipListClick(ActionEvent event) {
        System.out.println("readQuickStartTipListClick");
    }
        
    public void readTutorialClick(ActionEvent event) {
        System.out.println("readTutorialClick");
    }
        
    public void startUsingProgramClick(ActionEvent event) {
        System.out.println("startUsingProgramClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                WelcomeWindow thisClass = new WelcomeWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
