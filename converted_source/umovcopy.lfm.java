
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class TemplateMoverWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    JList leftTemplatesList;
    JList rightTemplatesList;
    JButton Done;
    JButton CopyTemplate;
    JButton DeleteTemplate;
    JComboBox ObjectTypeToShow;
    JButton helpButton;
    JButton renameTemplate;
    JButton Import;
    JButton Export;
    JButton copyLeftToRight;
    JButton copyRightToLeft;
    JButton chooseFont;
    JTextField leftTemplatesFileNameEdit;
    JButton leftTemplatesFileOpen;
    JButton leftTemplatesFileNew;
    JButton leftTemplatesFileSave;
    JTextField rightTemplatesFileNameEdit;
    JButton rightTemplatesFileOpen;
    JButton rightTemplatesFileNew;
    JButton rightTemplatesFileSave;
    JButton leftTemplatesFileSaveAs;
    JButton rightTemplatesFileSaveAs;
    JButton exportText;
    JButton importText;
    // UNHANDLED_TYPE FontDialog1;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public TemplateMoverWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Template Mover");
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
        this.setBounds(320, 203, 589, 348  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        
        
        this.leftTemplatesList = new JList(new DefaultListModel());
        this.leftTemplatesList.setFixedCellHeight(16);
        this.leftTemplatesList.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                leftTemplatesListClick(event);
            }
        });
        this.leftTemplatesList.setBounds(4, 56, 235, 290);
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTemplatesList.IntegralHeight = True;
        
        this.rightTemplatesList = new JList(new DefaultListModel());
        this.rightTemplatesList.setFixedCellHeight(16);
        this.rightTemplatesList.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                rightTemplatesListClick(event);
            }
        });
        this.rightTemplatesList.setBounds(266, 56, 235, 290);
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTemplatesList.IntegralHeight = True;
        
        this.Done = new JButton("Done");
        this.Done.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                DoneClick(event);
            }
        });
        this.Done.setMnemonic(KeyEvent.VK_D);
        this.getRootPane().setDefaultButton(this.Done);
        this.Done.setBounds(505, 6, 80, 24);
        //  --------------- UNHANDLED ATTRIBUTE: this.Done.Cancel = True;
        
        this.CopyTemplate = new JButton("Copy...");
        this.CopyTemplate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CopyTemplateClick(event);
            }
        });
        this.CopyTemplate.setMnemonic(KeyEvent.VK_C);
        this.CopyTemplate.setBounds(505, 86, 80, 24);
        
        this.DeleteTemplate = new JButton("Delete");
        this.DeleteTemplate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                DeleteTemplateClick(event);
            }
        });
        this.DeleteTemplate.setMnemonic(KeyEvent.VK_D);
        this.DeleteTemplate.setBounds(505, 116, 80, 24);
        
        this.ObjectTypeToShow = new JComboBox(new DefaultComboBoxModel());
        this.ObjectTypeToShow.setBounds(10, 364, 77, 24);
        //  --------------- UNHANDLED ATTRIBUTE: this.ObjectTypeToShow.Style = csDropDownList;
        ((DefaultComboBoxModel)this.ObjectTypeToShow.getModel()).addElement("Bag");
        ((DefaultComboBoxModel)this.ObjectTypeToShow.getModel()).addElement("Soil Type");
        ((DefaultComboBoxModel)this.ObjectTypeToShow.getModel()).addElement("Climate");
        ((DefaultComboBoxModel)this.ObjectTypeToShow.getModel()).addElement("Cultivar");
        ((DefaultComboBoxModel)this.ObjectTypeToShow.getModel()).addElement("Pesticide Type");
        //  --------------- UNHANDLED ATTRIBUTE: this.ObjectTypeToShow.ItemHeight = 16;
        this.ObjectTypeToShow.setVisible(false);
        //  --------------- UNHANDLED ATTRIBUTE: this.ObjectTypeToShow.TabStop = False;
        
        Image helpButtonImage = toolkit.createImage("../resources/TemplateMoverForm_helpButton.png");
        this.helpButton = new JButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.helpButton.setBounds(505, 236, 80, 24);
        
        this.renameTemplate = new JButton("Rename...");
        this.renameTemplate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                renameTemplateClick(event);
            }
        });
        this.renameTemplate.setMnemonic(KeyEvent.VK_R);
        this.renameTemplate.setBounds(505, 56, 80, 24);
        
        this.Import = new JButton("Import...");
        this.Import.setBounds(10, 390, 80, 24);
        this.Import.setVisible(false);
        
        this.Export = new JButton("Export...");
        this.Export.setBounds(10, 416, 80, 24);
        this.Export.setVisible(false);
        
        Image copyLeftToRightImage = toolkit.createImage("../resources/TemplateMoverForm_copyLeftToRight.png");
        this.copyLeftToRight = new JButton(new ImageIcon(copyLeftToRightImage));
        this.copyLeftToRight.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyLeftToRightClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.copyLeftToRight.setBounds(241, 183, 22, 22);
        this.copyLeftToRight.setToolTipText("Copy from left to right");
        
        Image copyRightToLeftImage = toolkit.createImage("../resources/TemplateMoverForm_copyRightToLeft.png");
        this.copyRightToLeft = new JButton(new ImageIcon(copyRightToLeftImage));
        this.copyRightToLeft.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyRightToLeftClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.copyRightToLeft.setBounds(241, 211, 22, 22);
        this.copyRightToLeft.setToolTipText("Copy from right to left");
        
        Image chooseFontImage = toolkit.createImage("../resources/TemplateMoverForm_chooseFont.png");
        this.chooseFont = new JButton("Font", new ImageIcon(chooseFontImage));
        this.chooseFont.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                chooseFontClick(event);
            }
        });
        this.chooseFont.setMnemonic(KeyEvent.VK_F);
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.chooseFont.setBounds(505, 146, 80, 24);
        this.chooseFont.setToolTipText("Change font");
        
        this.leftTemplatesFileNameEdit = new JTextField("");
        this.leftTemplatesFileNameEdit.setEditable(false);
        this.leftTemplatesFileNameEdit.setBounds(4, 4, 233, 24);
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTemplatesFileNameEdit.TabStop = False;
        
        this.leftTemplatesFileOpen = new JButton("Open...");
        this.leftTemplatesFileOpen.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leftTemplatesFileOpenClick(event);
            }
        });
        this.leftTemplatesFileOpen.setBounds(3, 29, 61, 25);
        
        this.leftTemplatesFileNew = new JButton("New...");
        this.leftTemplatesFileNew.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leftTemplatesFileNewClick(event);
            }
        });
        this.leftTemplatesFileNew.setBounds(64, 29, 59, 25);
        
        this.leftTemplatesFileSave = new JButton("Save");
        this.leftTemplatesFileSave.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leftTemplatesFileSaveClick(event);
            }
        });
        this.leftTemplatesFileSave.setBounds(122, 29, 43, 25);
        
        this.rightTemplatesFileNameEdit = new JTextField("");
        this.rightTemplatesFileNameEdit.setEditable(false);
        this.rightTemplatesFileNameEdit.setBounds(268, 4, 233, 24);
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTemplatesFileNameEdit.TabStop = False;
        
        this.rightTemplatesFileOpen = new JButton("Open...");
        this.rightTemplatesFileOpen.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                rightTemplatesFileOpenClick(event);
            }
        });
        this.rightTemplatesFileOpen.setBounds(268, 29, 57, 25);
        
        this.rightTemplatesFileNew = new JButton("New...");
        this.rightTemplatesFileNew.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                rightTemplatesFileNewClick(event);
            }
        });
        this.rightTemplatesFileNew.setBounds(325, 29, 65, 25);
        
        this.rightTemplatesFileSave = new JButton("Save");
        this.rightTemplatesFileSave.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                rightTemplatesFileSaveClick(event);
            }
        });
        this.rightTemplatesFileSave.setBounds(390, 29, 43, 25);
        
        this.leftTemplatesFileSaveAs = new JButton("Save as ...");
        this.leftTemplatesFileSaveAs.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leftTemplatesFileSaveAsClick(event);
            }
        });
        this.leftTemplatesFileSaveAs.setBounds(164, 29, 73, 25);
        
        this.rightTemplatesFileSaveAs = new JButton("Save as...");
        this.rightTemplatesFileSaveAs.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                rightTemplatesFileSaveAsClick(event);
            }
        });
        this.rightTemplatesFileSaveAs.setBounds(432, 29, 69, 25);
        
        this.exportText = new JButton("Export...");
        this.exportText.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                exportTextClick(event);
            }
        });
        this.exportText.setMnemonic(KeyEvent.VK_E);
        this.exportText.setBounds(505, 176, 80, 24);
        
        this.importText = new JButton("Import...");
        this.importText.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                importTextClick(event);
            }
        });
        this.importText.setMnemonic(KeyEvent.VK_I);
        this.importText.setBounds(505, 206, 80, 24);
        
        //  ------- UNHANDLED TYPE TFontDialog: FontDialog1 
        //  --------------- UNHANDLED ATTRIBUTE: this.FontDialog1.MinFontSize = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.FontDialog1.Font.Style = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.FontDialog1.MaxFontSize = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.FontDialog1.Top = 364;
        //  --------------- UNHANDLED ATTRIBUTE: this.FontDialog1.Font.Name = 'System';
        //  --------------- UNHANDLED ATTRIBUTE: this.FontDialog1.Font.Height = -13;
        //  --------------- UNHANDLED ATTRIBUTE: this.FontDialog1.Font.Color = clWindowText;
        //  --------------- UNHANDLED ATTRIBUTE: this.FontDialog1.Left = 104;
        
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(4, 56, 235, 290);;
        scroller1.setViewportView(leftTemplatesList);
        delphiPanel.add(scroller1);
        JScrollPane scroller2 = new JScrollPane();
        scroller2.setBounds(266, 56, 235, 290);;
        scroller2.setViewportView(rightTemplatesList);
        delphiPanel.add(scroller2);
        delphiPanel.add(Done);
        delphiPanel.add(CopyTemplate);
        delphiPanel.add(DeleteTemplate);
        delphiPanel.add(ObjectTypeToShow);
        delphiPanel.add(helpButton);
        delphiPanel.add(renameTemplate);
        delphiPanel.add(Import);
        delphiPanel.add(Export);
        delphiPanel.add(copyLeftToRight);
        delphiPanel.add(copyRightToLeft);
        delphiPanel.add(chooseFont);
        delphiPanel.add(leftTemplatesFileNameEdit);
        delphiPanel.add(leftTemplatesFileOpen);
        delphiPanel.add(leftTemplatesFileNew);
        delphiPanel.add(leftTemplatesFileSave);
        delphiPanel.add(rightTemplatesFileNameEdit);
        delphiPanel.add(rightTemplatesFileOpen);
        delphiPanel.add(rightTemplatesFileNew);
        delphiPanel.add(rightTemplatesFileSave);
        delphiPanel.add(leftTemplatesFileSaveAs);
        delphiPanel.add(rightTemplatesFileSaveAs);
        delphiPanel.add(exportText);
        delphiPanel.add(importText);
        return delphiPanel;
    }
    
        
    public void CopyTemplateClick(ActionEvent event) {
        System.out.println("CopyTemplateClick");
    }
        
    public void DeleteTemplateClick(ActionEvent event) {
        System.out.println("DeleteTemplateClick");
    }
        
    public void DoneClick(ActionEvent event) {
        System.out.println("DoneClick");
    }
        
    public void chooseFontClick(ActionEvent event) {
        System.out.println("chooseFontClick");
    }
        
    public void copyLeftToRightClick(ActionEvent event) {
        System.out.println("copyLeftToRightClick");
    }
        
    public void copyRightToLeftClick(ActionEvent event) {
        System.out.println("copyRightToLeftClick");
    }
        
    public void exportTextClick(ActionEvent event) {
        System.out.println("exportTextClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void importTextClick(ActionEvent event) {
        System.out.println("importTextClick");
    }
        
    public void leftTemplatesFileNewClick(ActionEvent event) {
        System.out.println("leftTemplatesFileNewClick");
    }
        
    public void leftTemplatesFileOpenClick(ActionEvent event) {
        System.out.println("leftTemplatesFileOpenClick");
    }
        
    public void leftTemplatesFileSaveAsClick(ActionEvent event) {
        System.out.println("leftTemplatesFileSaveAsClick");
    }
        
    public void leftTemplatesFileSaveClick(ActionEvent event) {
        System.out.println("leftTemplatesFileSaveClick");
    }
        
    public void leftTemplatesListClick(MouseEvent event) {
        System.out.println("leftTemplatesListClick");
    }
        
    public void renameTemplateClick(ActionEvent event) {
        System.out.println("renameTemplateClick");
    }
        
    public void rightTemplatesFileNewClick(ActionEvent event) {
        System.out.println("rightTemplatesFileNewClick");
    }
        
    public void rightTemplatesFileOpenClick(ActionEvent event) {
        System.out.println("rightTemplatesFileOpenClick");
    }
        
    public void rightTemplatesFileSaveAsClick(ActionEvent event) {
        System.out.println("rightTemplatesFileSaveAsClick");
    }
        
    public void rightTemplatesFileSaveClick(ActionEvent event) {
        System.out.println("rightTemplatesFileSaveClick");
    }
        
    public void rightTemplatesListClick(MouseEvent event) {
        System.out.println("rightTemplatesListClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                TemplateMoverWindow thisClass = new TemplateMoverWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
