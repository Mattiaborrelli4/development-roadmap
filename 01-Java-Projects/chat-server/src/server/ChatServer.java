package server;

import java.io.*;
import java.net.*;
import java.util.concurrent.*;
import java.util.*;

/**
 * Server di chat in tempo reale che supporta:
 * - Multi-client connessi simultaneamente
 * - Chat rooms pubbliche
 * - Messaggi privati (whisper)
 * - Persistenza dei messaggi su file
 * - ThreadPoolExecutor per gestione efficiente dei client
 */
public class ChatServer {
    private static final int DEFAULT_PORT = 9999;
    private ServerSocket serverSocket;
    private ThreadPoolExecutor executorService;

    // Map nickname -> ClientHandler
    private ConcurrentHashMap<String, ClientHandler> clients;

    // Map room name -> Set of nicknames
    private ConcurrentHashMap<String, Set<String>> rooms;

    // Map nickname -> current room
    private ConcurrentHashMap<String, String> userRooms;

    private BufferedWriter logWriter;
    private final String logFile = "chat.log";
    private volatile boolean running = true;

    public ChatServer(int port) {
        clients = new ConcurrentHashMap<>();
        rooms = new ConcurrentHashMap<>();
        userRooms = new ConcurrentHashMap<>();

        // Crea la room di default
        rooms.put("general", ConcurrentHashMap.newKeySet());

        try {
            executorService = (ThreadPoolExecutor) Executors.newCachedThreadPool();
            initializeLog();
        } catch (Exception e) {
            System.err.println("Errore nell'inizializzazione: " + e.getMessage());
        }
    }

    private void initializeLog() throws IOException {
        logWriter = new BufferedWriter(new FileWriter(logFile, true));
        logMessage("SERVER", "Server avviato");
    }

    private synchronized void logMessage(String nickname, String message) {
        try {
            String timestamp = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
            String logEntry = String.format("[%s] %s: %s", timestamp, nickname, message);
            logWriter.write(logEntry);
            logWriter.newLine();
            logWriter.flush();
        } catch (IOException e) {
            System.err.println("Errore nel logging: " + e.getMessage());
        }
    }

    public void start(int port) {
        try {
            serverSocket = new ServerSocket(port);
            System.out.println("Chat Server avviato sulla porta " + port);
            System.out.println("In attesa di connessioni...");

            while (running) {
                try {
                    Socket clientSocket = serverSocket.accept();
                    System.out.println("Nuova connessione da: " + clientSocket.getInetAddress());

                    ClientHandler clientHandler = new ClientHandler(clientSocket, this);
                    executorService.execute(clientHandler);
                } catch (SocketException e) {
                    if (running) {
                        System.err.println("Socket exception: " + e.getMessage());
                    }
                }
            }
        } catch (IOException e) {
            if (running) {
                System.err.println("Errore nell'avvio del server: " + e.getMessage());
            }
        } finally {
            stop();
        }
    }

    public synchronized boolean registerClient(String nickname, ClientHandler handler) {
        if (clients.containsKey(nickname)) {
            return false;
        }
        clients.put(nickname, handler);
        joinRoom(nickname, "general");
        System.out.println("Client registrato: " + nickname);
        return true;
    }

    public synchronized void removeClient(String nickname) {
        ClientHandler handler = clients.remove(nickname);
        if (handler != null) {
            String room = userRooms.remove(nickname);
            if (room != null) {
                Set<String> roomMembers = rooms.get(room);
                if (roomMembers != null) {
                    roomMembers.remove(nickname);
                    broadcastToRoom(room, String.format("LEFT %s", nickname));
                }
            }
            System.out.println("Client disconnesso: " + nickname);
        }
    }

    public synchronized boolean joinRoom(String nickname, String roomName) {
        if (!rooms.containsKey(roomName)) {
            rooms.put(roomName, ConcurrentHashMap.newKeySet());
        }

        String currentRoom = userRooms.get(nickname);
        if (currentRoom != null) {
            rooms.get(currentRoom).remove(nickname);
            broadcastToRoom(currentRoom, String.format("LEFT %s", nickname));
        }

        rooms.get(roomName).add(nickname);
        userRooms.put(nickname, roomName);
        broadcastToRoom(roomName, String.format("JOINED %s", nickname));
        return true;
    }

    public synchronized boolean leaveRoom(String nickname) {
        String currentRoom = userRooms.get(nickname);
        if (currentRoom != null) {
            rooms.get(currentRoom).remove(nickname);
            userRooms.remove(nickname);
            broadcastToRoom(currentRoom, String.format("LEFT %s", nickname));
            return true;
        }
        return false;
    }

    public synchronized void broadcastToRoom(String roomName, String message) {
        Set<String> roomMembers = rooms.get(roomName);
        if (roomMembers != null) {
            for (String member : roomMembers) {
                ClientHandler handler = clients.get(member);
                if (handler != null) {
                    handler.sendMessage(message);
                }
            }
        }
    }

    public synchronized boolean sendWhisper(String from, String to, String message) {
        ClientHandler toHandler = clients.get(to);
        if (toHandler != null) {
            toHandler.sendMessage(String.format("WHISPER %s: %s", from, message));
            return true;
        }
        return false;
    }

    public synchronized Set<String> getRoomMembers(String roomName) {
        Set<String> members = rooms.get(roomName);
        return members != null ? new HashSet<>(members) : new HashSet<>();
    }

    public synchronized Set<String> getAllRooms() {
        return new HashSet<>(rooms.keySet());
    }

    public synchronized String getUserRoom(String nickname) {
        return userRooms.get(nickname);
    }

    public void logChatMessage(String nickname, String message) {
        logMessage(nickname, message);
    }

    public void stop() {
        running = false;
        try {
            if (serverSocket != null && !serverSocket.isClosed()) {
                serverSocket.close();
            }
            if (executorService != null) {
                executorService.shutdown();
                if (!executorService.awaitTermination(5, TimeUnit.SECONDS)) {
                    executorService.shutdownNow();
                }
            }
            if (logWriter != null) {
                logMessage("SERVER", "Server arrestato");
                logWriter.close();
            }
        } catch (Exception e) {
            System.err.println("Errore nell'arresto del server: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        int port = DEFAULT_PORT;
        if (args.length > 0) {
            try {
                port = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                System.out.println("Porta non valida, uso porta di default: " + DEFAULT_PORT);
            }
        }

        ChatServer server = new ChatServer(port);

        // Aggiungi shutdown hook per chiusura pulita
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("\nArresto del server in corso...");
            server.stop();
        }));

        server.start(port);
    }
}
