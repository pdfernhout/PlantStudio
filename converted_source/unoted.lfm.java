
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class NoteEditWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JButton OK;
    JButton cancel;
    JTextArea noteEditMemo;
    JCheckBox wrapLines;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public NoteEditWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Edit note for plant");
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
        this.setBounds(609, 214, 356, 294  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 13;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/NoteEditForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(265, 64, 80, 21);
        
        this.OK = new JButton("OK");
        this.OK.setMnemonic(KeyEvent.VK_O);
        this.OK.setBounds(265, 2, 80, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.OK.ModalResult = 1;
        
        this.cancel = new JButton("Cancel");
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(265, 25, 80, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.ModalResult = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.noteEditMemo = new JTextArea(10, 10);
        this.noteEditMemo.setBounds(2, 2, 259, 261);
        //  --------------- UNHANDLED ATTRIBUTE: this.noteEditMemo.ScrollBars = ssVertical;
        
        this.wrapLines = new JCheckBox("wrap lines");
        this.wrapLines.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                wrapLinesClick(event);
            }
        });
        this.wrapLines.setMnemonic(KeyEvent.VK_W);
        this.wrapLines.setBounds(272, 92, 75, 17);
        
        delphiPanel.add(helpButton);
        delphiPanel.add(OK);
        delphiPanel.add(cancel);
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(2, 2, 259, 261);;
        scroller1.setViewportView(noteEditMemo);
        delphiPanel.add(scroller1);
        delphiPanel.add(wrapLines);
        return delphiPanel;
    }
    
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void wrapLinesClick(ActionEvent event) {
        System.out.println("wrapLinesClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                NoteEditWindow thisClass = new NoteEditWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
