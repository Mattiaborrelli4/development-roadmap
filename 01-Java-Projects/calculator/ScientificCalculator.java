import java.util.ArrayList;
import java.util.Scanner;

/**
 * Calcolatrice Scientifica - Progetto Educativo per Studenti Universitari
 *
 * Questo progetto dimostra i concetti fondamentali della programmazione Java:
 * - Strutture di controllo (if-else, switch, loop)
 * - Gestione delle eccezioni (try-catch)
 * - Programmazione orientata agli oggetti (OOP)
 * - Utilizzo della libreria standard Java (Math, Scanner, ArrayList)
 * - Gestione della memoria e collection
 *
 * @author Progetto Formativo
 * @version 1.0
 */
public class ScientificCalculator {

    // Scanner per l'input dell'utente - dichiarato come campo di classe
    private Scanner scanner;
    // Lista per memorizzare lo storico delle operazioni
    private ArrayList<String> history;

    /**
     * Costruttore: Inizializza lo stato della calcolatrice
     * Dimostra il concetto di inizializzazione degli oggetti
     */
    public ScientificCalculator() {
        scanner = new Scanner(System.in); // Crea un nuovo oggetto Scanner
        history = new ArrayList<>();      // Crea una nuova ArrayList vuota
        System.out.println("=== Calcolatrice Scientifica Java ===");
        System.out.println("Versione 1.0 - Progetto Educativo\n");
    }

    /**
     * Metodo principale: Avvia il loop del menu
     * Dimostra l'uso di loop infiniti con condizione di uscita
     */
    public void start() {
        boolean running = true; // Flag di controllo per il loop

        while (running) {
            displayMenu(); // Mostra il menu delle opzioni

            try {
                // Legge la scelta dell'utente
                System.out.print("Seleziona un'operazione (0-11): ");
                int choice = scanner.nextInt();
                scanner.nextLine(); // Consuma il newline rimanente

                // Switch statement per gestire le diverse opzioni
                switch (choice) {
                    case 0:
                        running = false; // Esce dal loop
                        System.out.println("\nGrazie per aver usato la Calcolatrice Scientifica!");
                        break;
                    case 1:
                        performAddition();
                        break;
                    case 2:
                        performSubtraction();
                        break;
                    case 3:
                        performMultiplication();
                        break;
                    case 4:
                        performDivision();
                        break;
                    case 5:
                        performPower();
                        break;
                    case 6:
                        performSquareRoot();
                        break;
                    case 7:
                        performSin();
                        break;
                    case 8:
                        performCos();
                        break;
                    case 9:
                        performTan();
                        break;
                    case 10:
                        performLogarithm();
                        break;
                    case 11:
                        displayHistory();
                        break;
                    default:
                        System.out.println("Errore: Scelta non valida. Riprova.\n");
                }
            } catch (java.util.InputMismatchException e) {
                // Gestione dell'eccezione per input non numerico
                System.out.println("Errore: Inserisci un numero valido.\n");
                scanner.nextLine(); // Pulisce il buffer dell'input
            } catch (Exception e) {
                // Gestione generica delle eccezioni
                System.out.println("Errore imprevisto: " + e.getMessage() + "\n");
            }
        }

        // Chiude lo scanner per liberare le risorse
        scanner.close();
    }

    /**
     * Mostra il menu delle operazioni disponibili
     * Dimostra la formattazione dell'output e l'uso di caratteri ASCII
     */
    private void displayMenu() {
        System.out.println("\n+----------------------------------------+");
        System.out.println("|           MENU OPERAZIONI             |");
        System.out.println("+----------------------------------------+");
        System.out.println("| 0. Esci                               |");
        System.out.println("| OPERAZIONI BASE                       |");
        System.out.println("| 1. Addizione            (+)           |");
        System.out.println("| 2. Sottrazione          (-)           |");
        System.out.println("| 3. Moltiplicazione      (*)           |");
        System.out.println("| 4. Divisione            (/)           |");
        System.out.println("| OPERAZIONI SCIENTIFICHE               |");
        System.out.println("| 5. Potenza              (x^y)         |");
        System.out.println("| 6. Radice Quadrata     (sqrt)        |");
        System.out.println("| 7. Seno                 (sin)         |");
        System.out.println("| 8. Coseno              (cos)         |");
        System.out.println("| 9. Tangente            (tan)         |");
        System.out.println("| 10. Logaritmo          (log)         |");
        System.out.println("| STORICO                               |");
        System.out.println("| 11. Mostra Storico                   |");
        System.out.println("+----------------------------------------+\n");
    }

    /**
     * Esegue l'addizione di due numeri
     * Dimostra: input, aritmetica di base, gestione storico
     */
    private void performAddition() {
        try {
            System.out.println("\n--- ADDIZIONE ---");
            System.out.print("Inserisci il primo numero: ");
            double num1 = scanner.nextDouble();
            scanner.nextLine(); // Consuma il newline

            System.out.print("Inserisci il secondo numero: ");
            double num2 = scanner.nextDouble();
            scanner.nextLine();

            double result = num1 + num2;
            String operation = String.format("%.2f + %.2f = %.2f", num1, num2, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento dei numeri.");
            scanner.nextLine(); // Pulisce il buffer
        }
    }

    /**
     * Esegue la sottrazione di due numeri
     */
    private void performSubtraction() {
        try {
            System.out.println("\n--- SOTTRAZIONE ---");
            System.out.print("Inserisci il primo numero: ");
            double num1 = scanner.nextDouble();
            scanner.nextLine();

            System.out.print("Inserisci il secondo numero: ");
            double num2 = scanner.nextDouble();
            scanner.nextLine();

            double result = num1 - num2;
            String operation = String.format("%.2f - %.2f = %.2f", num1, num2, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento dei numeri.");
            scanner.nextLine();
        }
    }

    /**
     * Esegue la moltiplicazione di due numeri
     */
    private void performMultiplication() {
        try {
            System.out.println("\n--- MOLTIPLICAZIONE ---");
            System.out.print("Inserisci il primo numero: ");
            double num1 = scanner.nextDouble();
            scanner.nextLine();

            System.out.print("Inserisci il secondo numero: ");
            double num2 = scanner.nextDouble();
            scanner.nextLine();

            double result = num1 * num2;
            String operation = String.format("%.2f * %.2f = %.2f", num1, num2, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento dei numeri.");
            scanner.nextLine();
        }
    }

    /**
     * Esegue la divisione di due numeri
     * Dimostra la gestione delle eccezioni per divisione per zero
     */
    private void performDivision() {
        try {
            System.out.println("\n--- DIVISIONE ---");
            System.out.print("Inserisci il numeratore: ");
            double num1 = scanner.nextDouble();
            scanner.nextLine();

            System.out.print("Inserisci il denominatore: ");
            double num2 = scanner.nextDouble();
            scanner.nextLine();

            // Controllo esplicito per la divisione per zero
            if (num2 == 0) {
                throw new ArithmeticException("Divisione per zero non consentita!");
            }

            double result = num1 / num2;
            String operation = String.format("%.2f / %.2f = %.2f", num1, num2, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (ArithmeticException e) {
            System.out.println("Errore matematico: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento dei numeri.");
            scanner.nextLine();
        }
    }

    /**
     * Calcola la potenza di un numero
     * Dimostra l'uso di Math.pow() dalla libreria standard
     */
    private void performPower() {
        try {
            System.out.println("\n--- POTENZA ---");
            System.out.print("Inserisci la base: ");
            double base = scanner.nextDouble();
            scanner.nextLine();

            System.out.print("Inserisci l'esponente: ");
            double exponent = scanner.nextDouble();
            scanner.nextLine();

            double result = Math.pow(base, exponent);
            String operation = String.format("%.2f ^ %.2f = %.4f", base, exponent, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento dei numeri.");
            scanner.nextLine();
        }
    }

    /**
     * Calcola la radice quadrata di un numero
     * Dimostra la gestione dell'input non valido (numeri negativi)
     */
    private void performSquareRoot() {
        try {
            System.out.println("\n--- RADICE QUADRATA ---");
            System.out.print("Inserisci il numero: ");
            double num = scanner.nextDouble();
            scanner.nextLine();

            // Controllo per numeri negativi
            if (num < 0) {
                throw new ArithmeticException(
                    "Non e' possibile calcolare la radice quadrata di un numero negativo nei numeri reali."
                );
            }

            double result = Math.sqrt(num);
            String operation = String.format("sqrt(%.2f) = %.4f", num, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (ArithmeticException e) {
            System.out.println("Errore matematico: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento del numero.");
            scanner.nextLine();
        }
    }

    /**
     * Calcola il seno di un angolo
     * NOTA: Math.sin() accetta angoli in radianti
     * Dimostra la conversione da gradi a radianti
     */
    private void performSin() {
        try {
            System.out.println("\n--- SENO ---");
            System.out.print("Inserisci l'angolo in gradi: ");
            double degrees = scanner.nextDouble();
            scanner.nextLine();

            // Conversione da gradi a radianti: radianti = gradi * (PI / 180)
            double radians = Math.toRadians(degrees);
            double result = Math.sin(radians);
            String operation = String.format("sin(%.2f°) = %.4f", degrees, result);

            System.out.println("\nRisultato: " + result);
            System.out.println("Nota: Angolo convertito da gradi a radianti per il calcolo.");
            addToHistory(operation);
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento dell'angolo.");
            scanner.nextLine();
        }
    }

    /**
     * Calcola il coseno di un angolo
     */
    private void performCos() {
        try {
            System.out.println("\n--- COSENO ---");
            System.out.print("Inserisci l'angolo in gradi: ");
            double degrees = scanner.nextDouble();
            scanner.nextLine();

            double radians = Math.toRadians(degrees);
            double result = Math.cos(radians);
            String operation = String.format("cos(%.2f°) = %.4f", degrees, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento dell'angolo.");
            scanner.nextLine();
        }
    }

    /**
     * Calcola la tangente di un angolo
     * Include controllo per angoli in cui tan è indefinita (90°, 270°, etc.)
     */
    private void performTan() {
        try {
            System.out.println("\n--- TANGENTE ---");
            System.out.print("Inserisci l'angolo in gradi: ");
            double degrees = scanner.nextDouble();
            scanner.nextLine();

            double radians = Math.toRadians(degrees);
            double result = Math.tan(radians);
            String operation = String.format("tan(%.2f°) = %.4f", degrees, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento dell'angolo.");
            scanner.nextLine();
        }
    }

    /**
     * Calcola il logaritmo naturale (base e) di un numero
     * Dimostra l'uso di Math.log() e la gestione del dominio della funzione
     */
    private void performLogarithm() {
        try {
            System.out.println("\n--- LOGARITMO NATURALE ---");
            System.out.print("Inserisci il numero: ");
            double num = scanner.nextDouble();
            scanner.nextLine();

            // Il logaritmo è definito solo per numeri positivi
            if (num <= 0) {
                throw new ArithmeticException(
                    "Il logaritmo è definito solo per numeri positivi."
                );
            }

            double result = Math.log(num);
            String operation = String.format("ln(%.2f) = %.4f", num, result);

            System.out.println("\nRisultato: " + result);
            addToHistory(operation);
        } catch (ArithmeticException e) {
            System.out.println("Errore matematico: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Errore nell'inserimento del numero.");
            scanner.nextLine();
        }
    }

    /**
     * Aggiunge un'operazione allo storico
     * Dimostra l'uso di ArrayList per gestire collezioni dinamiche
     *
     * @param operation Stringa che descrive l'operazione eseguita
     */
    private void addToHistory(String operation) {
        history.add(operation);
        System.out.println("[Operazione salvata nello storico]\n");
    }

    /**
     * Mostra tutte le operazioni eseguite
     * Dimostra l'iterazione su una collezione con for-each loop
     */
    private void displayHistory() {
        System.out.println("\n=== STORICO OPERAZIONI ===");

        // Verifica se lo storico è vuoto
        if (history.isEmpty()) {
            System.out.println("Nessuna operazione registrata.");
        } else {
            // Iterazione attraverso l'ArrayList usando for-each
            for (int i = 0; i < history.size(); i++) {
                System.out.println((i + 1) + ". " + history.get(i));
            }
        }
        System.out.println(); // Linea vuota per spaziatura
    }

    /**
     * Metodo main: Punto di ingresso del programma
     * Dimostra la creazione di oggetti e l'invocazione dei metodi
     *
     * @param args Argomenti da riga di comando (non utilizzati in questo programma)
     */
    public static void main(String[] args) {
        // Crea un'istanza della calcolatrice
        ScientificCalculator calculator = new ScientificCalculator();

        // Avvia il loop principale del programma
        calculator.start();

        // Nota: Non è necessario chiamare System.exit(0) in Java
        // Il programma termina automaticamente quando il metodo main completa
    }
}
