import java.io.*;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Applicazione Console Lista Attività (To-Do List)
 *
 * Una semplice applicazione per gestire attività con priorità.
 * Dimostra l'uso di ArrayList, HashMap, File I/O e Collections.
 *
 * @author Studente Universitario
 * @version 1.0
 */
public class TodoListApp {

    // ArrayList per memorizzare le attività (mantiene l'ordine di inserimento)
    private static ArrayList<String> tasks = new ArrayList<>();

    // HashMap per associare priorità alle attività (chiave: attività, valore: priorità)
    private static HashMap<String, Integer> priorities = new HashMap<>();

    // Scanner per l'input dell'utente
    private static Scanner scanner = new Scanner(System.in);

    // Nome del file per il salvataggio permanente
    private static final String FILE_NAME = "tasks.txt";

    /**
     * Metodo principale - punto di ingresso dell'applicazione
     * Gestisce il ciclo del menu principale
     */
    public static void main(String[] args) {
        // Carica le attività salvate all'avvio
        loadTasksFromFile();

        boolean running = true;

        System.out.println("===========================================");
        System.out.println("   BENVENUTO NELLA LISTA ATTIVITA'");
        System.out.println("===========================================");

        // Ciclo principale del menu
        while (running) {
            displayMenu();
            System.out.print("\nLa tua scelta: ");

            try {
                int choice = scanner.nextInt();
                scanner.nextLine(); // Consuma il newline

                switch (choice) {
                    case 1:
                        addTask();
                        break;
                    case 2:
                        removeTask();
                        break;
                    case 3:
                        viewTasks();
                        break;
                    case 4:
                        viewTasksByPriority();
                        break;
                    case 5:
                        saveTasksToFile();
                        System.out.println("\nAttivita' salvate con successo!");
                        break;
                    case 6:
                        saveTasksToFile();
                        running = false;
                        System.out.println("\nArrivederci! Alla prossima!");
                        break;
                    case 7:
                        loadTasksFromFile();
                        System.out.println("\nAttivita' caricate dal file!");
                        break;
                    default:
                        System.out.println("\n[!] Scelta non valida. Riprova.");
                }
            } catch (InputMismatchException e) {
                System.out.println("\n[!] Errore: Inserisci un numero valido.");
                scanner.nextLine(); // Pulisce il buffer
            }

            // Pausa per chiarezza
            if (running) {
                System.out.println("\nPremi INVIO per continuare...");
                scanner.nextLine();
            }
        }

        scanner.close();
    }

    /**
     * Mostra il menu principale con tutte le opzioni disponibili
     */
    private static void displayMenu() {
        System.out.println("\n===========================================");
        System.out.println("                MENU PRINCIPALE");
        System.out.println("===========================================");
        System.out.println("1. Aggiungi nuova attivita'");
        System.out.println("2. Rimuovi attivita'");
        System.out.println("3. Visualizza tutte le attivita'");
        System.out.println("4. Visualizza attivita' per priorita'");
        System.out.println("5. Salva attivita' su file");
        System.out.println("6. Esci e salva");
        System.out.println("7. Ricarica attivita' dal file");
        System.out.println("===========================================");
    }

    /**
     * Aggiunge una nuova attività con priorità
     * Dimostra l'uso di ArrayList.add() e HashMap.put()
     */
    private static void addTask() {
        System.out.println("\n--- AGGIUNGI NUOVA ATTIVITA' ---");

        System.out.print("Descrizione attivita': ");
        String task = scanner.nextLine().trim();

        if (task.isEmpty()) {
            System.out.println("[!] La descrizione non puo' essere vuota.");
            return;
        }

        // Verifica se l'attività esiste già
        if (tasks.contains(task)) {
            System.out.println("[!] Questa attivita' esiste gia'!");
            return;
        }

        System.out.print("Priorita' (1=ALTA, 2=MEDIA, 3=BASSA): ");
        try {
            int priority = scanner.nextInt();
            scanner.nextLine(); // Consuma il newline

            // Valida la priorità
            if (priority < 1 || priority > 3) {
                System.out.println("[!] Priorita' non valida. Usa 1, 2 o 3.");
                return;
            }

            // Aggiunge all'ArrayList (mantiene l'ordine di inserimento)
            tasks.add(task);

            // Aggiunge al HashMap (associa priorità all'attività)
            priorities.put(task, priority);

            System.out.println("\n[OK] Attivita' aggiunta con successo!");
            System.out.println("    Attivita': " + task);
            System.out.println("    Priorita': " + getPriorityLabel(priority));

        } catch (InputMismatchException e) {
            System.out.println("[!] Errore: Inserisci un numero valido per la priorita'.");
            scanner.nextLine(); // Pulisce il buffer
        }
    }

    /**
     * Rimuove un'attività esistente
     * Dimostra l'uso di ArrayList.remove() e HashMap.remove()
     */
    private static void removeTask() {
        System.out.println("\n--- RIMUOVI ATTIVITA' ---");

        if (tasks.isEmpty()) {
            System.out.println("[!] Nessuna attivita' presente nella lista.");
            return;
        }

        viewTasks();

        System.out.print("\nNumero dell'attivita' da rimuovere: ");
        try {
            int index = scanner.nextInt();
            scanner.nextLine(); // Consuma il newline

            if (index < 1 || index > tasks.size()) {
                System.out.println("[!] Numero non valido.");
                return;
            }

            // Ottieni l'attività (index - 1 perché ArrayList è 0-based)
            String task = tasks.get(index - 1);

            // Rimuovi da entrambe le strutture dati
            tasks.remove(index - 1);
            priorities.remove(task);

            System.out.println("\n[OK] Attivita' rimossa: " + task);

        } catch (InputMismatchException e) {
            System.out.println("[!] Errore: Inserisci un numero valido.");
            scanner.nextLine(); // Pulisce il buffer
        }
    }

    /**
     * Visualizza tutte le attività in ordine di inserimento
     * Dimostra l'iterazione su ArrayList con ciclo for-each
     */
    private static void viewTasks() {
        System.out.println("\n--- TUTTE LE ATTIVITA' (" + tasks.size() + ") ---");

        if (tasks.isEmpty()) {
            System.out.println("Nessuna attivita' presente.");
            return;
        }

        System.out.println("------------------------------------------------");
        System.out.printf("%-5s %-30s %-10s%n", "N.", "ATTIVITA'", "PRIORITA'");
        System.out.println("------------------------------------------------");

        int index = 1;
        for (String task : tasks) {
            // Ottieni la priorità dal HashMap
            int priority = priorities.get(task);
            String priorityLabel = getPriorityLabel(priority);

            System.out.printf("%-5d %-30s %-10s%n", index++, task, priorityLabel);
        }
        System.out.println("------------------------------------------------");
    }

    /**
     * Visualizza le attività ordinate per priorità
     * Dimostra l'uso di Collections.sort() con Comparator personalizzato
     */
    private static void viewTasksByPriority() {
        System.out.println("\n--- ATTIVITA' ORDINATE PER PRIORITA' ---");

        if (tasks.isEmpty()) {
            System.out.println("Nessuna attivita' presente.");
            return;
        }

        // Crea una lista ordinata usando Stream API (Java 8+)
        List<String> sortedTasks = tasks.stream()
                .sorted(Comparator.comparingInt(t -> priorities.get(t)))
                .collect(Collectors.toList());

        System.out.println("------------------------------------------------");
        System.out.printf("%-5s %-30s %-10s%n", "N.", "ATTIVITA'", "PRIORITA'");
        System.out.println("------------------------------------------------");

        int index = 1;
        for (String task : sortedTasks) {
            int priority = priorities.get(task);
            String priorityLabel = getPriorityLabel(priority);

            System.out.printf("%-5d %-30s %-10s%n", index++, task, priorityLabel);
        }
        System.out.println("------------------------------------------------");
    }

    /**
     * Salva le attività su file
     * Dimostra l'uso di FileWriter e BufferedWriter per File I/O
     */
    private static void saveTasksToFile() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_NAME))) {
            for (String task : tasks) {
                int priority = priorities.get(task);
                // Formato: task|priority
                writer.write(task + "|" + priority);
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("[!] Errore durante il salvataggio: " + e.getMessage());
        }
    }

    /**
     * Carica le attività dal file
     * Dimostra l'uso di FileReader e BufferedReader per File I/O
     */
    private static void loadTasksFromFile() {
        File file = new File(FILE_NAME);

        if (!file.exists()) {
            // File non esiste ancora, non è un errore
            return;
        }

        // Pulisce le strutture dati esistenti
        tasks.clear();
        priorities.clear();

        try (BufferedReader reader = new BufferedReader(new FileReader(FILE_NAME))) {
            String line;
            int lineNumber = 0;

            while ((line = reader.readLine()) != null) {
                lineNumber++;

                // Formato: task|priority
                String[] parts = line.split("\\|");

                if (parts.length == 2) {
                    String task = parts[0];
                    int priority = Integer.parseInt(parts[1]);

                    tasks.add(task);
                    priorities.put(task, priority);
                } else {
                    System.out.println("[!] Linea " + lineNumber + " ignorata: formato non valido.");
                }
            }
        } catch (IOException e) {
            System.out.println("[!] Errore durante il caricamento: " + e.getMessage());
        } catch (NumberFormatException e) {
            System.out.println("[!] Errore nel formato della priorita' nel file.");
        }
    }

    /**
     * Converte il numero di priorità in etichetta leggibile
     *
     * @param priority Numero di priorità (1-3)
     * @return Etichetta della priorità
     */
    private static String getPriorityLabel(int priority) {
        switch (priority) {
            case 1:
                return "ALTA";
            case 2:
                return "MEDIA";
            case 3:
                return "BASSA";
            default:
                return "SCONOSCIUTA";
        }
    }
}
