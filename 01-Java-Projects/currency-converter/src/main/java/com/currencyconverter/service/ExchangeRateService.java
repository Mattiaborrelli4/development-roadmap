package com.currencyconverter.service;

import com.currencyconverter.model.CurrencyRate;
import com.currencyconverter.model.HistoricalRate;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Servizio per il recupero dei tassi di cambio.
 * Include cache con scadenza di 1 ora e fallback su dati mock.
 */
public class ExchangeRateService {

    private static final String API_BASE_URL = "https://api.exchangerate.host/latest";
    private static final Map<String, CurrencyRate> cache = new ConcurrentHashMap<>();

    // Tassi di cambio mock (fallback)
    private static final Map<String, Double> MOCK_RATES = new HashMap<>();

    static {
        MOCK_RATES.put("EUR_USD", 1.0850);
        MOCK_RATES.put("EUR_GBP", 0.8550);
        MOCK_RATES.put("EUR_JPY", 165.20);
        MOCK_RATES.put("EUR_CHF", 0.9450);
        MOCK_RATES.put("USD_EUR", 0.9215);
        MOCK_RATES.put("GBP_EUR", 1.1690);
        MOCK_RATES.put("JPY_EUR", 0.00605);
        MOCK_RATES.put("CHF_EUR", 1.0580);
    }

    private final Gson gson = new Gson();

    /**
     * Recupera il tasso di cambio corrente.
     * Usa la cache se disponibile e non scaduta.
     */
    public CurrencyRate getCurrentRate(String from, String to) {
        String cacheKey = from + "_" + to;

        // Controlla la cache
        CurrencyRate cached = cache.get(cacheKey);
        if (cached != null && !cached.isExpired()) {
            System.out.println("Tasso recuperato dalla cache: " + cached);
            return cached;
        }

        // Recupera dal API o usa mock data
        CurrencyRate rate = fetchRateFromAPI(from, to);
        if (rate != null) {
            cache.put(cacheKey, rate);
            return rate;
        }

        // Fallback su dati mock
        return getMockRate(from, to);
    }

    /**
     * Recupera il tasso dall'API esterna.
     */
    private CurrencyRate fetchRateFromAPI(String from, String to) {
        try {
            String urlString = API_BASE_URL + "?base=" + from + "&symbols=" + to;
            URL url = new URL(urlString);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setRequestProperty("Accept", "application/json");
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);

            int responseCode = connection.getResponseCode();
            if (responseCode == 200) {
                String response = new Scanner(connection.getInputStream()).useDelimiter("\\A").next();
                JsonObject json = gson.fromJson(response, JsonObject.class);

                if (json.has("rates") && json.getAsJsonObject("rates").has(to)) {
                    double rate = json.getAsJsonObject("rates").get(to).getAsDouble();
                    System.out.println("Tasso recuperato dall'API: " + from + " -> " + to + ": " + rate);
                    return new CurrencyRate(from, to, rate);
                }
            }

            connection.disconnect();

        } catch (IOException e) {
            System.err.println("Errore nel recupero dei dati dall'API: " + e.getMessage());
        }

        return null;
    }

    /**
     * Restituisce un tasso mock (dati simulati).
     */
    private CurrencyRate getMockRate(String from, String to) {
        String key = from + "_" + to;
        Double rate = MOCK_RATES.get(key);

        if (rate == null) {
            // Calcola il tasso inverso se disponibile
            String reverseKey = to + "_" + from;
            Double reverseRate = MOCK_RATES.get(reverseKey);
            if (reverseRate != null) {
                rate = 1.0 / reverseRate;
            } else {
                // Valore di default
                rate = 1.0;
            }
        }

        System.out.println("Tasso mock utilizzato: " + from + " -> " + to + ": " + rate);
        return new CurrencyRate(from, to, rate);
    }

    /**
     * Recupera dati storici per il grafico (mock data per gli ultimi 7 giorni).
     */
    public List<HistoricalRate> getHistoricalRates(String from, String to) {
        List<HistoricalRate> historicalRates = new ArrayList<>();
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM");

        Calendar calendar = Calendar.getInstance();
        String cacheKey = from + "_" + to;
        Double currentRate = MOCK_RATES.get(cacheKey);

        if (currentRate == null) {
            String reverseKey = to + "_" + from;
            Double reverseRate = MOCK_RATES.get(reverseKey);
            currentRate = reverseRate != null ? 1.0 / reverseRate : 1.0;
        }

        // Genera dati mock per gli ultimi 7 giorni
        Random random = new Random();
        double baseRate = currentRate;

        for (int i = 6; i >= 0; i--) {
            calendar = Calendar.getInstance();
            calendar.add(Calendar.DAY_OF_MONTH, -i);

            String date = sdf.format(calendar.getTime());

            // Variazione casuale del tasso (±2%)
            double variation = (random.nextDouble() - 0.5) * 0.04;
            double rate = baseRate * (1 + variation);

            historicalRates.add(new HistoricalRate(date, rate));
        }

        return historicalRates;
    }

    /**
     * Pulisce la cache.
     */
    public void clearCache() {
        cache.clear();
        System.out.println("Cache pulita.");
    }

    /**
     * Restituisce tutte le valute supportate.
     */
    public List<String> getSupportedCurrencies() {
        return Arrays.asList("EUR", "USD", "GBP", "JPY", "CHF");
    }
}
