package com.taskmanager;

import com.taskmanager.gui.TaskManagerFrame;
import com.taskmanager.service.ProcessMonitorService;

import javax.swing.*;

/**
 * Classe principale dell'applicazione Task Manager
 */
public class TaskManagerApp {
    public static void main(String[] args) {
        // Set System Look and Feel per aspetto nativo
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            System.err.println("Impossibile impostare System Look and Feel: " + e.getMessage());
        }

        // Avvia applicazione nell'EDT
        SwingUtilities.invokeLater(() -> {
            try {
                // Crea servizio di monitoraggio
                ProcessMonitorService monitorService = new ProcessMonitorService();

                // Crea e mostra GUI
                TaskManagerFrame frame = new TaskManagerFrame(monitorService);
                frame.setVisible(true);

                // Avvia monitoraggio
                monitorService.startMonitoring();

            } catch (Exception e) {
                e.printStackTrace();
                JOptionPane.showMessageDialog(null,
                        "Errore durante l'avvio dell'applicazione: " + e.getMessage(),
                        "Errore",
                        JOptionPane.ERROR_MESSAGE);
                System.exit(1);
            }
        });
    }
}
