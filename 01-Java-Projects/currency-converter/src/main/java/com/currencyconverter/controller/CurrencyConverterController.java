package com.currencyconverter.controller;

import com.currencyconverter.model.HistoricalRate;
import com.currencyconverter.service.ExchangeRateService;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.*;

import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.List;

/**
 * Controller per l'interfaccia del Currency Converter.
 * Gestisce la conversione, il fetch dei dati e il grafico storico.
 */
public class CurrencyConverterController {

    @FXML
    private ComboBox<String> fromCurrencyCombo;

    @FXML
    private ComboBox<String> toCurrencyCombo;

    @FXML
    private TextField amountTextField;

    @FXML
    private Label resultLabel;

    @FXML
    private Label rateLabel;

    @FXML
    private Label lastUpdateLabel;

    @FXML
    private LineChart<String, Number> historyChart;

    @FXML
    private CategoryAxis xAxis;

    @FXML
    private NumberAxis yAxis;

    @FXML
    private ProgressIndicator loadingIndicator;

    @FXML
    private Button convertButton;

    @FXML
    private Button refreshButton;

    @FXML
    private Button swapButton;

    private final ExchangeRateService rateService;
    private final DecimalFormat decimalFormat;
    private final SimpleDateFormat dateTimeFormat;

    public CurrencyConverterController() {
        this.rateService = new ExchangeRateService();
        this.decimalFormat = new DecimalFormat("#,##0.00####");
        this.dateTimeFormat = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
    }

    @FXML
    public void initialize() {
        // Inizializza le combo box
        fromCurrencyCombo.setItems(FXCollections.observableArrayList(rateService.getSupportedCurrencies()));
        toCurrencyCombo.setItems(FXCollections.observableArrayList(rateService.getSupportedCurrencies()));

        // Seleziona valute di default
        fromCurrencyCombo.getSelectionModel().select("EUR");
        toCurrencyCombo.getSelectionModel().select("USD");

        // Nascondi l'indicatore di caricamento
        loadingIndicator.setVisible(false);

        // Imposta il grafico
        setupChart();

        // Abilita il pulsante Converti solo quando c'è un importo
        convertButton.disableProperty().bind(amountTextField.textProperty().isEmpty());

        // Listener per abilitare il pulsante Converti con Invio
        amountTextField.setOnAction(event -> handleConvert());

        // Carica i tassi iniziali
        fetchRatesAndChart();
    }

    /**
     * Configura il grafico storico.
     */
    private void setupChart() {
        historyChart.setTitle("Andamento Tasso di Cambio - Ultimi 7 Giorni");
        historyChart.setLegendVisible(false);
        historyChart.setAnimated(true);

        xAxis.setLabel("Data");
        yAxis.setLabel("Tasso di Cambio");
        yAxis.setForceZeroInRange(false);
    }

    /**
     * Gestisce la conversione di valuta.
     */
    @FXML
    private void handleConvert() {
        String from = fromCurrencyCombo.getValue();
        String to = toCurrencyCombo.getValue();
        String amountText = amountTextField.getText();

        if (from == null || to == null || amountText.isEmpty()) {
            showAlert("Errore", "Seleziona le valute e inserisci un importo.");
            return;
        }

        try {
            double amount = Double.parseDouble(amountText.replace(",", "."));

            if (amount <= 0) {
                showAlert("Errore", "L'importo deve essere maggiore di zero.");
                return;
            }

            // Esegui la conversione
            performConversion(from, to, amount);

        } catch (NumberFormatException e) {
            showAlert("Errore", "Inserisci un importo valido.");
        }
    }

    /**
     * Esegue la conversione in un thread separato.
     */
    private void performConversion(String from, String to, double amount) {
        showLoading(true);

        Task<Void> task = new Task<Void>() {
            @Override
            protected Void call() {
                try {
                    double rate = rateService.getCurrentRate(from, to).getRate();
                    double result = amount * rate;

                    Platform.runLater(() -> {
                        resultLabel.setText(decimalFormat.format(result));
                        rateLabel.setText(String.format("Tasso: 1 %s = %.4f %s", from, rate, to));
                        lastUpdateLabel.setText("Aggiornamento: " + dateTimeFormat.format(new java.util.Date()));
                        showLoading(false);
                    });

                } catch (Exception e) {
                    Platform.runLater(() -> {
                        showAlert("Errore", "Impossibile effettuare la conversione: " + e.getMessage());
                        showLoading(false);
                    });
                }

                return null;
            }
        };

        Thread thread = new Thread(task);
        thread.setDaemon(true);
        thread.start();
    }

    /**
     * Recupera i tassi e aggiorna il grafico.
     */
    @FXML
    private void handleRefresh() {
        fetchRatesAndChart();
    }

    /**
     * Scambia le valute selezionate.
     */
    @FXML
    private void handleSwap() {
        String temp = fromCurrencyCombo.getValue();
        fromCurrencyCombo.setValue(toCurrencyCombo.getValue());
        toCurrencyCombo.setValue(temp);

        // Se c'è già un risultato, ricalcola
        if (!resultLabel.getText().isEmpty()) {
            handleConvert();
        }
    }

    /**
     * Recupera i tassi e aggiorna il grafico in background.
     */
    private void fetchRatesAndChart() {
        String from = fromCurrencyCombo.getValue();
        String to = toCurrencyCombo.getValue();

        if (from == null || to == null) {
            return;
        }

        showLoading(true);

        Task<Void> task = new Task<Void>() {
            @Override
            protected Void call() {
                try {
                    // Recupera i dati storici
                    List<HistoricalRate> historicalRates = rateService.getHistoricalRates(from, to);

                    // Recupera il tasso corrente
                    double currentRate = rateService.getCurrentRate(from, to).getRate();

                    Platform.runLater(() -> {
                        updateChart(historicalRates);
                        rateLabel.setText(String.format("Tasso: 1 %s = %.4f %s", from, currentRate, to));
                        lastUpdateLabel.setText("Aggiornamento: " + dateTimeFormat.format(new java.util.Date()));
                        showLoading(false);
                    });

                } catch (Exception e) {
                    Platform.runLater(() -> {
                        showAlert("Errore", "Impossibile recuperare i dati: " + e.getMessage());
                        showLoading(false);
                    });
                }

                return null;
            }
        };

        Thread thread = new Thread(task);
        thread.setDaemon(true);
        thread.start();
    }

    /**
     * Aggiorna il grafico con i dati storici.
     */
    private void updateChart(List<HistoricalRate> historicalRates) {
        historyChart.getData().clear();

        XYChart.Series<String, Number> series = new XYChart.Series<>();
        series.setName(fromCurrencyCombo.getValue() + " -> " + toCurrencyCombo.getValue());

        for (HistoricalRate hr : historicalRates) {
            series.getData().add(new XYChart.Data<>(hr.getDate(), hr.getRate()));
        }

        historyChart.getData().add(series);
    }

    /**
     * Mostra o nasconde l'indicatore di caricamento.
     */
    private void showLoading(boolean loading) {
        loadingIndicator.setVisible(loading);
        convertButton.setDisable(loading);
        refreshButton.setDisable(loading);
        swapButton.setDisable(loading);
        fromCurrencyCombo.setDisable(loading);
        toCurrencyCombo.setDisable(loading);
    }

    /**
     * Mostra un alert di informazione/errore.
     */
    private void showAlert(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
}
