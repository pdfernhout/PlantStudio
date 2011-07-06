
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class ChooseDXFColorWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    JTable colorsDrawGrid;
    JButton Close;
    JButton cancel;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public ChooseDXFColorWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Choose DXF color");
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
        this.setBounds(409, 127, 273, 62  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [biSystemMenu, biMaximize];
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        
        
        this.colorsDrawGrid = new JTable(new DefaultTableModel());
        this.colorsDrawGrid.setBounds(2, 4, 206, 57);
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.OnDrawCell = colorsDrawGridDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.OnSelectCell = colorsDrawGridSelectCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.RowCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.FixedRows = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.DefaultColWidth = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.ColCount = 12;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.DefaultRowHeight = 54;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.ScrollBars = ssNone;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.OnDblClick = colorsDrawGridDblClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsDrawGrid.Options = [goFixedVertLine, goFixedHorzLine, goVertLine, goHorzLine];
        
        this.Close = new JButton("OK");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.getRootPane().setDefaultButton(this.Close);
        this.Close.setBounds(212, 4, 60, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setBounds(212, 27, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        delphiPanel.add(colorsDrawGrid);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        return delphiPanel;
    }
    
        
    public void CloseClick(ActionEvent event) {
        System.out.println("CloseClick");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                ChooseDXFColorWindow thisClass = new ChooseDXFColorWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
