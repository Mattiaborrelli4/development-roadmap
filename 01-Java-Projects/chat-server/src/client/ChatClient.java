package client;

import java.io.*;
import java.net.*;
import java.util.Scanner;
import java.util.concurrent.*;

/**
 * Client console per la chat.
 * Supporta comandi per interagire con il server di chat.
 */
public class ChatClient {
    private Socket socket;
    private PrintWriter out;
    private BufferedReader in;
    private String nickname;
    private volatile boolean running = true;
    private ExecutorService executorService;

    public ChatClient(String host, int port, String nickname) {
        this.nickname = nickname;
        try {
            socket = new Socket(host, port);
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            executorService = Executors.newSingleThreadExecutor();
        } catch (IOException e) {
            System.err.println("Errore nella connessione al server: " + e.getMessage());
            System.exit(1);
        }
    }

    public void start() {
        // Invia il nickname
        out.println("NICK " + nickname);

        // Avvia il thread per la ricezione dei messaggi
        executorService.execute(this::receiveMessages);

        // Gestisce l'input dell'utente
        Scanner scanner = new Scanner(System.in);
        System.out.println("\n=== CLIENT DI CHAT ===");
        System.out.println("Comandi disponibili:");
        System.out.println("  /join <room>   - Entra in una room");
        System.out.println("  /leave         - Esci dalla room corrente");
        System.out.println("  /whisper <nick> <msg> - Messaggio privato");
        System.out.println("  /list          - Lista delle room");
        System.out.println("  /users         - Lista utenti nella room corrente");
        System.out.println("  /quit          - Esci dalla chat");
        System.out.println("  Inserisci un messaggio e premi Invio per inviarlo alla room");
        System.out.println("=====================\n");

        while (running) {
            try {
                String input = scanner.nextLine();
                if (input != null && !input.isEmpty()) {
                    if (input.startsWith("/")) {
                        handleCommand(input);
                    } else {
                        out.println("MSG " + input);
                    }
                }
            } catch (Exception e) {
                if (running) {
                    System.err.println("Errore nell'invio del messaggio: " + e.getMessage());
                }
                break;
            }
        }

        stop();
    }

    private void receiveMessages() {
        try {
            String message;
            while (running && (message = in.readLine()) != null) {
                handleServerMessage(message);
            }
        } catch (SocketException e) {
            if (running) {
                System.out.println("\nConnessione con il server persa");
            }
        } catch (IOException e) {
            if (running) {
                System.err.println("Errore nella ricezione dei messaggi: " + e.getMessage());
            }
        } finally {
            running = false;
        }
    }

    private void handleServerMessage(String message) {
        if (message.startsWith("MSG ")) {
            System.out.println(message.substring(4));
        } else if (message.startsWith("WHISPER ")) {
            System.out.println("[PRIVATO] " + message.substring(8));
        } else if (message.startsWith("JOINED ")) {
            System.out.println("[JOIN] " + message.substring(7) + " è entrato nella room");
        } else if (message.startsWith("LEFT ")) {
            System.out.println("[LEFT] " + message.substring(5) + " è uscito dalla room");
        } else if (message.startsWith("OK ")) {
            System.out.println("[SUCCESS] " + message.substring(3));
        } else if (message.startsWith("ERROR ")) {
            System.err.println("[ERRORE] " + message.substring(6));
        } else if (message.startsWith("INFO ")) {
            System.out.println("[INFO] " + message.substring(5));
        } else {
            System.out.println(message);
        }
    }

    private void handleCommand(String command) {
        String[] parts = command.split(" ", 2);
        String cmd = parts[0].toLowerCase();

        switch (cmd) {
            case "/join":
                if (parts.length < 2) {
                    System.out.println("Uso: /join <room>");
                    return;
                }
                out.println("JOIN " + parts[1]);
                break;

            case "/leave":
                out.println("LEAVE");
                break;

            case "/whisper":
                if (parts.length < 2) {
                    System.out.println("Uso: /whisper <nick> <messaggio>");
                    return;
                }
                String[] whisperParts = parts[1].split(" ", 2);
                if (whisperParts.length < 2) {
                    System.out.println("Uso: /whisper <nick> <messaggio>");
                    return;
                }
                out.println("WHISPER " + whisperParts[0] + " " + whisperParts[1]);
                break;

            case "/list":
                out.println("LIST");
                break;

            case "/users":
                out.println("USERS");
                break;

            case "/quit":
                out.println("QUIT");
                running = false;
                System.out.println("Disconnessione...");
                break;

            default:
                System.out.println("Comando non riconosciuto: " + cmd);
        }
    }

    public void stop() {
        running = false;
        try {
            if (executorService != null) {
                executorService.shutdown();
                if (!executorService.awaitTermination(2, TimeUnit.SECONDS)) {
                    executorService.shutdownNow();
                }
            }
            if (in != null) in.close();
            if (out != null) out.close();
            if (socket != null && !socket.isClosed()) socket.close();
        } catch (Exception e) {
            System.err.println("Errore nella chiusura: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        String host = "localhost";
        int port = 9999;
        String nickname = "User" + System.currentTimeMillis() % 10000;

        if (args.length >= 1) {
            nickname = args[0];
        }
        if (args.length >= 2) {
            try {
                host = args[1];
            } catch (Exception e) {
                System.out.println("Host non valido, uso localhost");
            }
        }
        if (args.length >= 3) {
            try {
                port = Integer.parseInt(args[2]);
            } catch (NumberFormatException e) {
                System.out.println("Porta non valida, uso 9999");
            }
        }

        System.out.println("Connessione a " + host + ":" + port + " come " + nickname);

        ChatClient client = new ChatClient(host, port, nickname);

        // Aggiungi shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("\nChiusura del client...");
            client.stop();
        }));

        client.start();
    }
}
