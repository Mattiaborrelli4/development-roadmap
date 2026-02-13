package com.taskmanager.gui;

import com.taskmanager.model.ProcessInfo;

import javax.swing.table.AbstractTableModel;
import java.util.ArrayList;
import java.util.List;

/**
 * TableModel per la tabella dei processi
 */
public class ProcessTableModel extends AbstractTableModel {
    private final List<ProcessInfo> processes;
    private final String[] columnNames = {
            "PID",
            "Nome",
            "Utente",
            "Comando",
            "Memoria",
            "CPU %"
    };
    private final Class<?>[] columnTypes = {
            Long.class,
            String.class,
            String.class,
            String.class,
            String.class,
            String.class
    };

    public ProcessTableModel() {
        this.processes = new ArrayList<>();
    }

    public void setProcesses(List<ProcessInfo> processes) {
        this.processes.clear();
        this.processes.addAll(processes);
        fireTableDataChanged();
    }

    public void clear() {
        processes.clear();
        fireTableDataChanged();
    }

    public ProcessInfo getProcessAt(int rowIndex) {
        if (rowIndex >= 0 && rowIndex < processes.size()) {
            return processes.get(rowIndex);
        }
        return null;
    }

    @Override
    public int getRowCount() {
        return processes.size();
    }

    @Override
    public int getColumnCount() {
        return columnNames.length;
    }

    @Override
    public String getColumnName(int column) {
        return columnNames[column];
    }

    @Override
    public Class<?> getColumnClass(int columnIndex) {
        return columnTypes[columnIndex];
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        ProcessInfo process = processes.get(rowIndex);
        if (process == null) {
            return null;
        }

        switch (columnIndex) {
            case 0: return process.getPid();
            case 1: return process.getName();
            case 2: return process.getUser();
            case 3: return process.getCommand();
            case 4: return process.getFormattedMemory();
            case 5: return process.getFormattedCpu();
            default: return null;
        }
    }
}
