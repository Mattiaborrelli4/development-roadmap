package com.taskmanager.gui;

import com.taskmanager.model.ProcessInfo;
import com.taskmanager.service.ProcessMonitorService;

import javax.swing.*;
import javax.swing.table.TableRowSorter;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.util.List;
import java.util.prefs.Preferences;

/**
 * Finestra principale del Task Manager
 */
public class TaskManagerFrame extends JFrame {
    private final ProcessMonitorService monitorService;
    private final ProcessTableModel tableModel;
    private final JTable processTable;
    private final JTextField filterField;
    private final JLabel statusLabel;
    private final JLabel cpuLabel;
    private final JLabel memoryLabel;
    private final PerformanceChartPanel chartPanel;
    private final TableRowSorter<ProcessTableModel> sorter;

    private Preferences prefs;
    private TrayIcon trayIcon;

    public TaskManagerFrame(ProcessMonitorService monitorService) {
        this.monitorService = monitorService;
        this.tableModel = new ProcessTableModel();
        this.processTable = new JTable(tableModel);
        this.filterField = new JTextField();
        this.statusLabel = new JLabel("Pronto");
        this.cpuLabel = new JLabel("CPU: 0.0%");
        this.memoryLabel = new JLabel("Memoria: 0 MB");
        this.chartPanel = new PerformanceChartPanel();
        this.sorter = new TableRowSorter<>(tableModel);

        initializeUI();
        setupMonitoring();
        setupSystemTray();
    }

    private void initializeUI() {
        setTitle("Task Manager - Monitoraggio Processi");
        setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        setSize(1000, 700);
        setLocationRelativeTo(null);

        // Pannello principale
        JPanel mainPanel = new JPanel(new BorderLayout(10, 10));
        mainPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Pannello filtro
        JPanel filterPanel = createFilterPanel();
        mainPanel.add(filterPanel, BorderLayout.NORTH);

        // Tabella processi
        JScrollPane tableScrollPane = new JScrollPane(processTable);
        tableScrollPane.setPreferredSize(new Dimension(800, 400));
        mainPanel.add(tableScrollPane, BorderLayout.CENTER);

        // Pannello bottoni azione
        JPanel buttonPanel = createActionPanel();
        mainPanel.add(buttonPanel, BorderLayout.SOUTH);

        // Pannello performance (grafico)
        JPanel performancePanel = createPerformancePanel();
        mainPanel.add(performancePanel, BorderLayout.EAST);

        // Status bar
        JPanel statusBar = new JPanel(new BorderLayout());
        statusBar.add(statusLabel, BorderLayout.WEST);
        statusBar.add(cpuLabel, BorderLayout.CENTER);
        statusBar.add(memoryLabel, BorderLayout.EAST);
        statusBar.setBorder(BorderFactory.createEtchedBorder());
        add(statusBar, BorderLayout.SOUTH);

        add(mainPanel);

        // Configura tabella
        setupTable();

        // Window listener
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                onClose();
            }

            @Override
            public void windowIconified(WindowEvent e) {
                // Minimizza nella system tray se disponibile
                if (SystemTray.isSupported()) {
                    setVisible(false);
                }
            }
        });
    }

    private JPanel createFilterPanel() {
        JPanel panel = new JPanel(new BorderLayout(10, 5));
        panel.setBorder(BorderFactory.createTitledBorder("Filtra Processi"));

        JLabel label = new JLabel("Nome processo:");
        panel.add(label, BorderLayout.WEST);

        panel.add(filterField, BorderLayout.CENTER);

        JButton clearButton = new JButton("Pulisci");
        clearButton.addActionListener(e -> {
            filterField.setText("");
            sorter.setRowFilter(null);
        });
        panel.add(clearButton, BorderLayout.EAST);

        // Listener per filtro
        filterField.getDocument().addDocumentListener(new javax.swing.event.DocumentListener() {
            public void changedUpdate(javax.swing.event.DocumentEvent e) { updateFilter(); }
            public void insertUpdate(javax.swing.event.DocumentEvent e) { updateFilter(); }
            public void removeUpdate(javax.swing.event.DocumentEvent e) { updateFilter(); }

            private void updateFilter() {
                String text = filterField.getText();
                if (text.trim().isEmpty()) {
                    sorter.setRowFilter(null);
                } else {
                    sorter.setRowFilter(RowFilter.regexFilter("(?i)" + text));
                }
            }
        });

        return panel;
    }

    private JPanel createActionPanel() {
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 5));
        panel.setBorder(BorderFactory.createTitledBorder("Azioni"));

        JButton refreshButton = new JButton("Aggiorna");
        refreshButton.addActionListener(e -> refreshProcesses());
        panel.add(refreshButton);

        JButton killButton = new JButton("Termina Processo Selezionato");
        killButton.addActionListener(e -> killSelectedProcess());
        panel.add(killButton);

        JButton forceKillButton = new JButton("Forza Terminazione");
        forceKillButton.addActionListener(e -> forceKillSelectedProcess());
        panel.add(forceKillButton);

        return panel;
    }

    private JPanel createPerformancePanel() {
        JPanel panel = new JPanel(new BorderLayout(5, 5));
        panel.setBorder(BorderFactory.createTitledBorder("Performance Real-Time"));
        panel.setPreferredSize(new Dimension(450, 250));

        panel.add(chartPanel, BorderLayout.CENTER);

        return panel;
    }

    private void setupTable() {
        processTable.setRowSorter(sorter);
        processTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        processTable.setAutoCreateRowSorter(true);

        // Configura colonne
        processTable.getColumnModel().getColumn(0).setPreferredWidth(80);
        processTable.getColumnModel().getColumn(1).setPreferredWidth(150);
        processTable.getColumnModel().getColumn(2).setPreferredWidth(100);
        processTable.getColumnModel().getColumn(3).setPreferredWidth(300);
        processTable.getColumnModel().getColumn(4).setPreferredWidth(100);
        processTable.getColumnModel().getColumn(5).setPreferredWidth(80);

        // Header font
        processTable.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));

        // Row height
        processTable.setRowHeight(25);

        // Popup menu
        JPopupMenu popupMenu = new JPopupMenu();
        JMenuItem killItem = new JMenuItem("Termina Processo");
        JMenuItem forceKillItem = new JMenuItem("Forza Terminazione");
        JMenuItem refreshItem = new JMenuItem("Aggiorna");

        killItem.addActionListener(e -> killSelectedProcess());
        forceKillItem.addActionListener(e -> forceKillSelectedProcess());
        refreshItem.addActionListener(e -> refreshProcesses());

        popupMenu.add(killItem);
        popupMenu.add(forceKillItem);
        popupMenu.addSeparator();
        popupMenu.add(refreshItem);

        processTable.setComponentPopupMenu(popupMenu);

        // Double click
        processTable.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) {
                    showProcessDetails();
                }
            }
        });
    }

    private void setupMonitoring() {
        // Callback per aggiornamento processi
        monitorService.setProcessUpdateCallback(processes -> SwingUtilities.invokeLater(() -> {
            tableModel.setProcesses(processes);
            statusLabel.setText(String.format("Processi attivi: %d", processes.size()));
        }));

        // Callback per aggiornamento CPU
        monitorService.setCpuUpdateCallback(cpuUsage -> SwingUtilities.invokeLater(() -> {
            cpuLabel.setText(String.format("CPU: %.1f%%", cpuUsage));
            chartPanel.updateCpuUsage(cpuUsage);
        }));

        // Callback per aggiornamento Memoria
        monitorService.setMemoryUpdateCallback(memoryUsage -> SwingUtilities.invokeLater(() -> {
            double memoryMB = memoryUsage / (1024.0 * 1024.0);
            memoryLabel.setText(String.format("Memoria: %.1f MB", memoryMB));
            chartPanel.updateMemoryUsage(memoryUsage);
        }));
    }

    private void setupSystemTray() {
        if (!SystemTray.isSupported()) {
            return;
        }

        SystemTray tray = SystemTray.getSystemTray();

        // Crea icona
        Image image = createTrayIconImage();
        trayIcon = new TrayIcon(image, "Task Manager");
        trayIcon.setImageAutoSize(true);

        // Popup menu
        PopupMenu popup = new PopupMenu();
        MenuItem showItem = new MenuItem("Mostra");
        MenuItem exitItem = new MenuItem("Esci");

        showItem.addActionListener(e -> SwingUtilities.invokeLater(() -> {
            setVisible(true);
            setExtendedState(JFrame.NORMAL);
        }));

        exitItem.addActionListener(e -> exitApplication());

        popup.add(showItem);
        popup.addSeparator();
        popup.add(exitItem);

        trayIcon.setPopupMenu(popup);

        // Double click per mostrare
        trayIcon.addActionListener(e -> SwingUtilities.invokeLater(() -> {
            setVisible(true);
            setExtendedState(JFrame.NORMAL);
        }));

        try {
            tray.add(trayIcon);
        } catch (AWTException e) {
            System.err.println("Impossibile aggiungere icona alla system tray: " + e.getMessage());
        }
    }

    private Image createTrayIconImage() {
        // Crea icona semplice
        int size = 16;
        BufferedImage image = new BufferedImage(size, size, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2d = image.createGraphics();

        g2d.setColor(Color.BLUE);
        g2d.fillRect(2, 2, size - 4, size - 4);
        g2d.setColor(Color.WHITE);
        g2d.drawString("TM", 3, 12);

        g2d.dispose();
        return image;
    }

    private void refreshProcesses() {
        statusLabel.setText("Aggiornamento...");
        new SwingWorker<Void, Void>() {
            @Override
            protected Void doInBackground() {
                // Il monitoraggio è già automatico, questo è solo refresh manuale
                return null;
            }

            @Override
            protected void done() {
                statusLabel.setText("Aggiornato");
            }
        }.execute();
    }

    private void killSelectedProcess() {
        int selectedRow = processTable.getSelectedRow();
        if (selectedRow < 0) {
            JOptionPane.showMessageDialog(this,
                    "Seleziona un processo dalla tabella",
                    "Nessuna Selezione",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        int modelRow = processTable.convertRowIndexToModel(selectedRow);
        ProcessInfo process = tableModel.getProcessAt(modelRow);

        int confirm = JOptionPane.showConfirmDialog(this,
                String.format("Terminare il processo '%s' (PID: %d)?", process.getName(), process.getPid()),
                "Conferma Terminazione",
                JOptionPane.YES_NO_OPTION,
                JOptionPane.QUESTION_MESSAGE);

        if (confirm == JOptionPane.YES_OPTION) {
            boolean success = monitorService.terminateProcess(process.getPid());
            if (success) {
                JOptionPane.showMessageDialog(this,
                        "Processo terminato con successo",
                        "Successo",
                        JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this,
                        "Impossibile terminare il processo.\nPotrebbe richiedere permessi elevati.",
                        "Errore",
                        JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void forceKillSelectedProcess() {
        int selectedRow = processTable.getSelectedRow();
        if (selectedRow < 0) {
            JOptionPane.showMessageDialog(this,
                    "Seleziona un processo dalla tabella",
                    "Nessuna Selezione",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        int modelRow = processTable.convertRowIndexToModel(selectedRow);
        ProcessInfo process = tableModel.getProcessAt(modelRow);

        int confirm = JOptionPane.showConfirmDialog(this,
                String.format("FORZARE la terminazione del processo '%s' (PID: %d)?\n\nATTENZIONE: Questo può causare perdita di dati!",
                        process.getName(), process.getPid()),
                "Conferma Terminazione Forzata",
                JOptionPane.YES_NO_OPTION,
                JOptionPane.WARNING_MESSAGE);

        if (confirm == JOptionPane.YES_OPTION) {
            boolean success = monitorService.killProcess(process.getPid());
            if (success) {
                JOptionPane.showMessageDialog(this,
                        "Processo terminato forzatamente",
                        "Successo",
                        JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this,
                        "Impossibile terminare il processo.\nPotrebbe richiedere permessi elevati.",
                        "Errore",
                        JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void showProcessDetails() {
        int selectedRow = processTable.getSelectedRow();
        if (selectedRow < 0) {
            return;
        }

        int modelRow = processTable.convertRowIndexToModel(selectedRow);
        ProcessInfo process = tableModel.getProcessAt(modelRow);

        String details = String.format(
                "<html><b>Dettagli Processo</b><br><br>" +
                "<b>PID:</b> %d<br>" +
                "<b>Nome:</b> %s<br>" +
                "<b>Utente:</b> %s<br>" +
                "<b>Comando:</b> %s<br>" +
                "<b>Memoria:</b> %s<br>" +
                "<b>CPU:</b> %s</html>",
                process.getPid(),
                process.getName(),
                process.getUser(),
                process.getCommand(),
                process.getFormattedMemory(),
                process.getFormattedCpu()
        );

        JOptionPane.showMessageDialog(this, details, "Dettagli Processo", JOptionPane.INFORMATION_MESSAGE);
    }

    private void onClose() {
        int confirm = JOptionPane.showConfirmDialog(this,
                "Minimizzare nella system tray invece di chiudere?",
                "Conferma Chiusura",
                JOptionPane.YES_NO_CANCEL_OPTION);

        if (confirm == JOptionPane.YES_OPTION) {
            if (SystemTray.isSupported()) {
                setVisible(false);
            } else {
                exitApplication();
            }
        } else if (confirm == JOptionPane.NO_OPTION) {
            exitApplication();
        }
        // CANCEL non fa nulla
    }

    private void exitApplication() {
        monitorService.stopMonitoring();
        System.exit(0);
    }
}