package server;

import java.io.*;
import java.net.*;

/**
 * Gestisce la connessione con un singolo client.
 * Ogni client ha il proprio thread per gestire i messaggi in entrata.
 */
public class ClientHandler implements Runnable {
    private Socket clientSocket;
    private ChatServer server;
    private PrintWriter out;
    private BufferedReader in;
    private String nickname;
    private volatile boolean running = true;

    public ClientHandler(Socket socket, ChatServer server) {
        this.clientSocket = socket;
        this.server = server;
        try {
            out = new PrintWriter(clientSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        } catch (IOException e) {
            System.err.println("Errore nella creazione degli stream: " + e.getMessage());
        }
    }

    @Override
    public void run() {
        try {
            // Attesa del nickname
            String firstLine = in.readLine();
            if (firstLine == null) {
                close();
                return;
            }

            if (firstLine.startsWith("NICK ")) {
                nickname = firstLine.substring(5).trim();
                if (nickname.isEmpty()) {
                    sendMessage("ERROR Nickname non valido");
                    close();
                    return;
                }

                if (!server.registerClient(nickname, this)) {
                    sendMessage("ERROR Nickname già in uso");
                    close();
                    return;
                }

                sendMessage("OK Benvenuto nella chat! Room corrente: general");
                sendMessage("INFO Usa /join <room>, /leave, /whisper <nick> <msg>, /list, /quit");
            } else {
                sendMessage("ERROR Protocollo non valido. Usa: NICK nickname");
                close();
                return;
            }

            // Loop di gestione dei messaggi
            String inputLine;
            while (running && (inputLine = in.readLine()) != null) {
                handleMessage(inputLine);
            }
        } catch (SocketException e) {
            // Connessione chiusa dal client
            System.out.println("Client disconnesso: " + nickname);
        } catch (IOException e) {
            System.err.println("Errore nella comunicazione con il client: " + e.getMessage());
        } finally {
            if (nickname != null) {
                server.removeClient(nickname);
            }
            close();
        }
    }

    private void handleMessage(String message) {
        if (message.startsWith("/")) {
            handleCommand(message);
        } else if (message.startsWith("MSG ")) {
            handleChatMessage(message.substring(4));
        } else {
            sendMessage("ERROR Comando non valido. Usa /help per aiuto");
        }
    }

    private void handleCommand(String command) {
        String[] parts = command.split(" ", 2);
        String cmd = parts[0].toLowerCase();

        switch (cmd) {
            case "/join":
                if (parts.length < 2) {
                    sendMessage("ERROR Uso: /join <room>");
                    return;
                }
                String roomName = parts[1];
                server.joinRoom(nickname, roomName);
                String currentRoom = server.getUserRoom(nickname);
                sendMessage("OK Entrato nella room: " + currentRoom);
                sendMessage("INFO " + String.join(" ", server.getRoomMembers(currentRoom)));
                break;

            case "/leave":
                if (server.leaveRoom(nickname)) {
                    server.joinRoom(nickname, "general");
                    sendMessage("OK Tornato nella room: general");
                } else {
                    sendMessage("ERROR Non sei in alcuna room");
                }
                break;

            case "/whisper":
                if (parts.length < 2) {
                    sendMessage("ERROR Uso: /whisper <nick> <messaggio>");
                    return;
                }
                String[] whisperParts = parts[1].split(" ", 2);
                if (whisperParts.length < 2) {
                    sendMessage("ERROR Uso: /whisper <nick> <messaggio>");
                    return;
                }
                String targetNick = whisperParts[0];
                String whisperMsg = whisperParts[1];
                if (server.sendWhisper(nickname, targetNick, whisperMsg)) {
                    sendMessage("OK Messaggio privato inviato a " + targetNick);
                    server.logChatMessage(nickname, "[WHISPER to " + targetNick + "] " + whisperMsg);
                } else {
                    sendMessage("ERROR Utente " + targetNick + " non trovato");
                }
                break;

            case "/list":
                StringBuilder sb = new StringBuilder("INFO Room disponibili: ");
                sb.append(String.join(", ", server.getAllRooms()));
                sendMessage(sb.toString());
                break;

            case "/users":
                String userRoom = server.getUserRoom(nickname);
                if (userRoom != null) {
                    StringBuilder usersSb = new StringBuilder("INFO Utenti in " + userRoom + ": ");
                    usersSb.append(String.join(", ", server.getRoomMembers(userRoom)));
                    sendMessage(usersSb.toString());
                }
                break;

            case "/quit":
                sendMessage("OK Arrivederci!");
                running = false;
                break;

            case "/help":
                sendMessage("INFO Comandi disponibili:");
                sendMessage("INFO  /join <room>  - Entra in una room");
                sendMessage("INFO  /leave        - Esci dalla room corrente");
                sendMessage("INFO  /whisper <nick> <msg> - Messaggio privato");
                sendMessage("INFO  /list         - Lista delle room");
                sendMessage("INFO  /users        - Lista utenti nella room corrente");
                sendMessage("INFO  /quit         - Esci dalla chat");
                break;

            default:
                sendMessage("ERROR Comando non riconosciuto. Usa /help");
        }
    }

    private void handleChatMessage(String text) {
        String currentRoom = server.getUserRoom(nickname);
        if (currentRoom != null) {
            String message = String.format("MSG %s: %s", nickname, text);
            server.broadcastToRoom(currentRoom, message);
            server.logChatMessage(nickname, "[" + currentRoom + "] " + text);
        }
    }

    public void sendMessage(String message) {
        if (out != null) {
            out.println(message);
        }
    }

    public void close() {
        running = false;
        try {
            if (in != null) in.close();
            if (out != null) out.close();
            if (clientSocket != null && !clientSocket.isClosed()) clientSocket.close();
        } catch (IOException e) {
            System.err.println("Errore nella chiusura della connessione: " + e.getMessage());
        }
    }
}
