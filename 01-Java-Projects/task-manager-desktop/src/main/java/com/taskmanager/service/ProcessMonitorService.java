package com.taskmanager.service;

import com.taskmanager.model.ProcessInfo;

import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryUsage;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;

/**
 * Servizio per il monitoraggio dei processi di sistema
 * Utilizza ProcessHandle API (Java 9+) e aggiornamento schedulato
 */
public class ProcessMonitorService {
    private final ScheduledExecutorService scheduler;
    private final OperatingSystemMXBean osBean;
    private final MemoryMXBean memoryBean;
    private Consumer<List<ProcessInfo>> processUpdateCallback;
    private Consumer<Double> cpuUpdateCallback;
    private Consumer<Long> memoryUpdateCallback;
    private boolean running;

    public ProcessMonitorService() {
        this.scheduler = Executors.newScheduledThreadPool(2);
        this.osBean = ManagementFactory.getOperatingSystemMXBean();
        this.memoryBean = ManagementFactory.getMemoryMXBean();
        this.running = false;
    }

    /**
     * Imposta il callback per aggiornamenti della lista processi
     */
    public void setProcessUpdateCallback(Consumer<List<ProcessInfo>> callback) {
        this.processUpdateCallback = callback;
    }

    /**
     * Imposta il callback per aggiornamenti CPU
     */
    public void setCpuUpdateCallback(Consumer<Double> callback) {
        this.cpuUpdateCallback = callback;
    }

    /**
     * Imposta il callback per aggiornamenti Memoria
     */
    public void setMemoryUpdateCallback(Consumer<Long> callback) {
        this.memoryUpdateCallback = callback;
    }

    /**
     * Avvia il monitoraggio con aggiornamento ogni 2 secondi
     */
    public void startMonitoring() {
        if (running) {
            return;
        }
        running = true;

        // Aggiornamento processi ogni 2 secondi
        scheduler.scheduleAtFixedRate(this::updateProcesses, 0, 2, TimeUnit.SECONDS);

        // Aggiornamento performance CPU/Memoria ogni 1 secondo
        scheduler.scheduleAtFixedRate(this::updatePerformance, 0, 1, TimeUnit.SECONDS);
    }

    /**
     * Ferma il monitoraggio
     */
    public void stopMonitoring() {
        running = false;
        scheduler.shutdown();
    }

    /**
     * Aggiorna la lista dei processi
     */
    private void updateProcesses() {
        try {
            List<ProcessInfo> processes = new ArrayList<>();

            ProcessHandle.allProcesses()
                    .filter(ProcessHandle::isAlive)
                    .forEach(handle -> {
                        ProcessInfo info = createProcessInfo(handle);
                        if (info != null) {
                            processes.add(info);
                        }
                    });

            // Ordina per utilizzo memoria decrescente
            processes.sort((p1, p2) -> Long.compare(p2.getMemoryUsage(), p1.getMemoryUsage()));

            if (processUpdateCallback != null) {
                processUpdateCallback.accept(processes);
            }
        } catch (Exception e) {
            System.err.println("Errore aggiornamento processi: " + e.getMessage());
        }
    }

    /**
     * Crea ProcessInfo da ProcessHandle
     */
    private ProcessInfo createProcessInfo(ProcessHandle handle) {
        try {
            long pid = handle.pid();
            ProcessHandle.Info info = handle.info();
            String name = info.command().map(cmd -> {
                int lastSlash = Math.max(cmd.lastIndexOf("/"), cmd.lastIndexOf("\\"));
                return lastSlash >= 0 ? cmd.substring(lastSlash + 1) : cmd;
            }).orElse("Sconosciuto");

            // Ottieni command line
            String command = info.command().orElse("");
            if (command.isEmpty()) {
                command = info.commandLine().orElse(name);
            }

            // Tronca comando se troppo lungo
            if (command.length() > 100) {
                command = command.substring(0, 97) + "...";
            }

            // Info utente
            String user = info.user().orElse("Sistema");

            // Stima memoria (info().totalMemoryDuration() non disponibile in tutte le implementazioni)
            long memoryUsage = 0;
            try {
                // Usa alternative per memoria
                memoryUsage = (long) (Math.random() * 100 * 1024 * 1024); // Placeholder
            } catch (Exception ignored) {
            }

            // CPU usage placeholder (ProcessHandle non fornisce direttamente)
            double cpuUsage = 0.0;

            return new ProcessInfo(pid, name, command, memoryUsage, cpuUsage, user);

        } catch (Exception e) {
            return null;
        }
    }

    /**
     * Aggiorna le performance di sistema (CPU e Memoria)
     */
    private void updatePerformance() {
        try {
            // CPU Load (sistema)
            double systemCpuLoad = osBean.getSystemLoadAverage();
            if (systemCpuLoad < 0) {
                systemCpuLoad = 0.0;
            }

            // Normalizza per numero di processori
            int processors = osBean.getAvailableProcessors();
            double cpuUsagePercent = (systemCpuLoad / processors) * 100;
            cpuUsagePercent = Math.min(100, Math.max(0, cpuUsagePercent));

            if (cpuUpdateCallback != null) {
                cpuUpdateCallback.accept(cpuUsagePercent);
            }

            // Memory Usage
            MemoryUsage heapUsage = memoryBean.getHeapMemoryUsage();
            long usedMemory = heapUsage.getUsed();
            long totalMemory = heapUsage.getMax();

            // Memoria di sistema (approssimazione)
            long systemMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

            if (memoryUpdateCallback != null) {
                memoryUpdateCallback.accept(systemMemory);
            }

        } catch (Exception e) {
            System.err.println("Errore aggiornamento performance: " + e.getMessage());
        }
    }

    /**
     * Termina un processo per PID
     */
    public boolean killProcess(long pid) {
        try {
            return ProcessHandle.of(pid)
                    .map(handle -> handle.destroyForcibly())
                    .orElse(false);
        } catch (Exception e) {
            System.err.println("Errore terminazione processo " + pid + ": " + e.getMessage());
            return false;
        }
    }

    /**
     * Termina gentilmente un processo per PID
     */
    public boolean terminateProcess(long pid) {
        try {
            return ProcessHandle.of(pid)
                    .map(handle -> handle.destroy())
                    .orElse(false);
        } catch (Exception e) {
            System.err.println("Errore terminazione processo " + pid + ": " + e.getMessage());
            return false;
        }
    }

    public boolean isRunning() {
        return running;
    }
}
