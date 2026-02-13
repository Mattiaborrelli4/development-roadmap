package com.taskmanager.gui;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.DateAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.data.time.Second;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.time.TimeSeriesCollection;

import javax.swing.*;
import java.awt.*;
import java.util.Date;

/**
 * Pannello con grafico real-time per performance CPU e Memoria
 */
public class PerformanceChartPanel extends JPanel {
    private final TimeSeries cpuSeries;
    private final TimeSeries memorySeries;
    private final TimeSeriesCollection dataset;
    private final JFreeChart chart;
    private final int maxDataPoints = 60; // Mantiene ultimi 60 secondi

    public PerformanceChartPanel() {
        // Crea time series
        this.cpuSeries = new TimeSeries("CPU %");
        this.memorySeries = new TimeSeries("Memoria (MB)");
        this.dataset = new TimeSeriesCollection();
        this.dataset.addSeries(cpuSeries);
        this.dataset.addSeries(memorySeries);

        // Crea grafico
        this.chart = ChartFactory.createTimeSeriesChart(
                "Performance di Sistema",
                "Tempo",
                "Valore",
                dataset,
                true,
                true,
                false
        );

        // Configura asse X
        XYPlot plot = (XYPlot) chart.getPlot();
        DateAxis axis = (DateAxis) plot.getDomainAxis();
        axis.setDateFormatOverride(new java.text.SimpleDateFormat("HH:mm:ss"));

        // Configura renderer
        XYLineAndShapeRenderer renderer = new XYLineAndShapeRenderer();
        renderer.setSeriesShapesVisible(0, false);
        renderer.setSeriesShapesVisible(1, false);
        renderer.setSeriesPaint(0, Color.RED); // CPU in rosso
        renderer.setSeriesPaint(1, Color.BLUE); // Memoria in blu
        plot.setRenderer(renderer);

        // Crea ChartPanel
        ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new Dimension(400, 200));
        chartPanel.setMouseZoomable(true);
        chartPanel.setDomainZoomable(true);
        chartPanel.setRangeZoomable(true);

        setLayout(new BorderLayout());
        add(chartPanel, BorderLayout.CENTER);
    }

    /**
     * Aggiorna dati CPU
     */
    public void updateCpuUsage(double cpuUsage) {
        SwingUtilities.invokeLater(() -> {
            synchronized (cpuSeries) {
                cpuSeries.addOrUpdate(new Second(), cpuUsage);
                limitDataPoints(cpuSeries);
            }
        });
    }

    /**
     * Aggiorna dati Memoria
     */
    public void updateMemoryUsage(long memoryBytes) {
        SwingUtilities.invokeLater(() -> {
            synchronized (memorySeries) {
                double memoryMB = memoryBytes / (1024.0 * 1024.0);
                memorySeries.addOrUpdate(new Second(), memoryMB);
                limitDataPoints(memorySeries);
            }
        });
    }

    /**
     * Mantieni solo ultimi N data points per performance
     */
    private void limitDataPoints(TimeSeries series) {
        while (series.getItemCount() > maxDataPoints) {
            series.delete(0, 0);
        }
    }

    /**
     * Reset dati
     */
    public void clearData() {
        SwingUtilities.invokeLater(() -> {
            synchronized (cpuSeries) {
                cpuSeries.clear();
            }
            synchronized (memorySeries) {
                memorySeries.clear();
            }
        });
    }

    public JFreeChart getChart() {
        return chart;
    }
}
