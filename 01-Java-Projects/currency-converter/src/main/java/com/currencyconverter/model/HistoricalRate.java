package com.currencyconverter.model;

/**
 * Rappresenta un tasso di cambio storico per il grafico.
 */
public class HistoricalRate {
    private final String date;
    private final double rate;

    public HistoricalRate(String date, double rate) {
        this.date = date;
        this.rate = rate;
    }

    public String getDate() {
        return date;
    }

    public double getRate() {
        return rate;
    }

    @Override
    public String toString() {
        return String.format("%s: %.4f", date, rate);
    }
}
