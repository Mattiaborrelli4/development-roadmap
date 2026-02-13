package com.currencyconverter.model;

import java.util.Date;

/**
 * Rappresenta un tasso di cambio con timestamp.
 */
public class CurrencyRate {
    private final String fromCurrency;
    private final String toCurrency;
    private final double rate;
    private final long timestamp;

    public CurrencyRate(String fromCurrency, String toCurrency, double rate) {
        this.fromCurrency = fromCurrency;
        this.toCurrency = toCurrency;
        this.rate = rate;
        this.timestamp = System.currentTimeMillis();
    }

    public String getFromCurrency() {
        return fromCurrency;
    }

    public String getToCurrency() {
        return toCurrency;
    }

    public double getRate() {
        return rate;
    }

    public long getTimestamp() {
        return timestamp;
    }

    /**
     * Controlla se il tasso è scaduto (più vecchio di 1 ora).
     */
    public boolean isExpired() {
        long oneHourInMillis = 60 * 60 * 1000;
        return System.currentTimeMillis() - timestamp > oneHourInMillis;
    }

    @Override
    public String toString() {
        return String.format("%s -> %s: %.4f", fromCurrency, toCurrency, rate);
    }
}
