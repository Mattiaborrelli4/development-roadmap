package com.currencyconverter;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

/**
 * Classe principale dell'applicazione Currency Converter.
 * Avvia l'interfaccia JavaFX.
 */
public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        try {
            // Carica il file FXML
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/com/currencyconverter/currency_converter.fxml"));
            Parent root = loader.load();

            // Configura la scena
            Scene scene = new Scene(root, 900, 700);

            // Aggiungi il foglio di stile CSS
            scene.getStylesheets().add(getClass().getResource("/com/currencyconverter/css/style.css").toExternalForm());

            // Configura e mostra lo stage
            primaryStage.setTitle("Currency Converter - Convertitore di Valuta");
            primaryStage.setScene(scene);
            primaryStage.setResizable(true);
            primaryStage.show();

        } catch (IOException e) {
            System.err.println("Errore nel caricamento dell'interfaccia: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
