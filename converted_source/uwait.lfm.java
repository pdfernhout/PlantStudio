
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class WaitWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    JPanel Panel1;
    JLabel messageLabel;
    ImagePanel Image1;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public WaitWindow() {
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
        this.setBounds(388, 293, 339, 54  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsNone;
        
        
        this.messageLabel = new JLabel("saving file...");
        this.messageLabel.setBounds(76, 19, 58, 14);
        //  --------------- UNHANDLED ATTRIBUTE: this.messageLabel.Alignment = taCenter;
        
        Image Image1Image = toolkit.createImage("../resources/WaitForm_Image1.png");
        this.Image1 = new ImagePanel(new ImageIcon(Image1Image));
        this.Image1.setBounds(4, 4, 64, 44);
        
        this.Panel1 = new JPanel(null);
        // -- this.Panel1.setLayout(new BoxLayout(this.Panel1, BoxLayout.Y_AXIS));
        this.Panel1.add(messageLabel);
        this.Panel1.add(Image1);
        this.Panel1.setBounds(0, 0, 339, 54);
        
        delphiPanel.add(Panel1);
        return delphiPanel;
    }
    

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                WaitWindow thisClass = new WaitWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
