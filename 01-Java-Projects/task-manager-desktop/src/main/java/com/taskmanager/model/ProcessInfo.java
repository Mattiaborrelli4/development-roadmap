package com.taskmanager.model;

import java.lang.management.ManagementFactory;

/**
 * Rappresenta le informazioni di un processo
 */
public class ProcessInfo {
    private final long pid;
    private final String name;
    private final String command;
    private final long memoryUsage;
    private final double cpuUsage;
    private final String user;

    public ProcessInfo(long pid, String name, String command, long memoryUsage, double cpuUsage, String user) {
        this.pid = pid;
        this.name = name;
        this.command = command;
        this.memoryUsage = memoryUsage;
        this.cpuUsage = cpuUsage;
        this.user = user;
    }

    public long getPid() {
        return pid;
    }

    public String getName() {
        return name;
    }

    public String getCommand() {
        return command;
    }

    public long getMemoryUsage() {
        return memoryUsage;
    }

    public double getCpuUsage() {
        return cpuUsage;
    }

    public String getUser() {
        return user;
    }

    public String getFormattedMemory() {
        if (memoryUsage < 1024) {
            return memoryUsage + " B";
        } else if (memoryUsage < 1024 * 1024) {
            return String.format("%.2f KB", memoryUsage / 1024.0);
        } else if (memoryUsage < 1024 * 1024 * 1024) {
            return String.format("%.2f MB", memoryUsage / (1024.0 * 1024.0));
        } else {
            return String.format("%.2f GB", memoryUsage / (1024.0 * 1024.0 * 1024.0));
        }
    }

    public String getFormattedCpu() {
        return String.format("%.2f%%", cpuUsage);
    }

    @Override
    public String toString() {
        return String.format("ProcessInfo{pid=%d, name='%s', memory=%s, cpu=%s}",
                pid, name, getFormattedMemory(), getFormattedCpu());
    }
}
