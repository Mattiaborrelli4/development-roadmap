package com.organizer;

import java.io.*;
import java.nio.file.*;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.logging.*;

/**
 * FileOrganizer - Applicazione automatica per organizzare file per estensione
 * Utilizza WatchService per monitorare una cartella e organizzare i file in tempo reale
 * VERSION: Fixed without external dependencies - uses Properties instead of JSON
 */
public class FileOrganizer {
    private WatchService watchService;
    private Map<String, String> rules;
    private Map<String, WatchKey> watchKeys;
    private Logger logger;
    private Path watchDir;
    private boolean running;

    public FileOrganizer(Path configPath, Path logPath) throws IOException {
        this.watchService = FileSystems.getDefault().newWatchService();
        this.watchKeys = new HashMap<>();
        this.running = false;

        // Inizializza logger
        setupLogger(logPath);

        // Carica regole di configurazione
        loadRules(configPath);
    }

    /**
     * Configura il logger per scrivere su file e console
     */
    private void setupLogger(Path logPath) throws IOException {
        logger = Logger.getLogger("FileOrganizer");

        // Rimuovi handler di default
        Logger rootLogger = Logger.getLogger("");
        Handler[] handlers = rootLogger.getHandlers();
        if (handlers.length > 0 && handlers[0] instanceof ConsoleHandler) {
            rootLogger.removeHandler(handlers[0]);
        }

        // File handler
        FileHandler fileHandler = new FileHandler(logPath.toString(), true);
        fileHandler.setFormatter(new CustomFormatter());
        logger.addHandler(fileHandler);

        // Console handler
        ConsoleHandler consoleHandler = new ConsoleHandler();
        consoleHandler.setFormatter(new CustomFormatter());
        logger.addHandler(consoleHandler);

        logger.setLevel(Level.ALL);
    }

    /**
     * Carica le regole di organizzazione dal file Properties
     * Formato: cartella=est1,est2,est3
     */
    private void loadRules(Path configPath) throws IOException {
        Properties props = new Properties();

        try (InputStream input = Files.newInputStream(configPath)) {
            props.load(input);
        }

        // Converti la configurazione in map estensione -> cartella
        rules = new HashMap<>();

        for (String folder : props.stringPropertyNames()) {
            String extensions = props.getProperty(folder);
            String[] extArray = extensions.split(",");

            for (String extension : extArray) {
                String ext = extension.trim().toLowerCase();
                if (!ext.isEmpty()) {
                    rules.put(ext, folder);
                }
            }
        }

        logger.info("Regole caricate: " + rules.size() + " estensioni configurate");
    }

    /**
     * Avvia il monitoraggio della directory specificata
     */
    public void startWatching(Path directory) throws IOException {
        this.watchDir = directory.normalize();
        this.running = true;

        logger.info("=== AVVIO FILE ORGANIZER ===");
        logger.info("Directory monitorata: " + watchDir.toAbsolutePath());

        // Crea le sottocartelle per le categorie
        createCategoryFolders();

        // Registra la directory per il monitoraggio
        registerDirectory(watchDir);

        // Organizza i file esistenti
        organizeExistingFiles();

        logger.info("Monitoraggio attivo. Premi CTRL+C per terminare.\n");

        // Loop di monitoraggio
        processEvents();
    }

    /**
     * Crea le sottocartelle per ogni categoria se non esistono
     */
    private void createCategoryFolders() throws IOException {
        Set<String> folders = new HashSet<>(rules.values());
        for (String folder : folders) {
            Path categoryPath = watchDir.resolve(folder);
            if (!Files.exists(categoryPath)) {
                Files.createDirectories(categoryPath);
                logger.info("Creata cartella: " + folder);
            }
        }
    }

    /**
     * Registra una directory per il monitoraggio con WatchService
     */
    private void registerDirectory(Path dir) throws IOException {
        if (!Files.exists(dir)) {
            logger.warning("Directory non trovata: " + dir);
            return;
        }

        WatchKey key = dir.register(
            watchService,
            StandardWatchEventKinds.ENTRY_CREATE,
            StandardWatchEventKinds.ENTRY_MODIFY
        );

        watchKeys.put(key.toString(), key);
        logger.info("Directory registrata per il monitoraggio: " + dir);
    }

    /**
     * Organizza i file già presenti nella directory
     */
    private void organizeExistingFiles() throws IOException {
        logger.info("Organizzazione file esistenti...");

        int count = 0;
        try (DirectoryStream<Path> stream = Files.newDirectoryStream(watchDir)) {
            for (Path entry : stream) {
                if (Files.isRegularFile(entry)) {
                    if (organizeFile(entry)) {
                        count++;
                    }
                }
            }
        }

        logger.info("File esistenti organizzati: " + count);
    }

    /**
     * Loop principale di elaborazione degli eventi
     */
    private void processEvents() {
        while (running) {
            WatchKey key;
            try {
                key = watchService.take();
            } catch (InterruptedException e) {
                logger.severe("Monitoraggio interrotto: " + e.getMessage());
                return;
            }

            for (WatchEvent<?> event : key.pollEvents()) {
                WatchEvent.Kind<?> kind = event.kind();

                if (kind == StandardWatchEventKinds.OVERFLOW) {
                    continue;
                }

                @SuppressWarnings("unchecked")
                WatchEvent<Path> ev = (WatchEvent<Path>) event;
                Path filename = ev.context();

                Path fullPath = ((Path) key.watchable()).resolve(filename);

                // Ignora le cartelle
                if (Files.isDirectory(fullPath)) {
                    continue;
                }

                if (kind == StandardWatchEventKinds.ENTRY_CREATE) {
                    logger.info("Nuovo file rilevato: " + filename);
                    organizeFile(fullPath);
                }
            }

            boolean valid = key.reset();
            if (!valid) {
                watchKeys.remove(key.toString());
                if (watchKeys.isEmpty()) {
                    break;
                }
            }
        }
    }

    /**
     * Organizza un singolo file nella cartella appropriata
     */
    private boolean organizeFile(Path file) {
        try {
            String fileName = file.getFileName().toString();
            String extension = getFileExtension(fileName);

            if (extension.isEmpty()) {
                logger.warning("File senza estensione: " + fileName);
                return false;
            }

            String targetFolder = rules.get(extension.toLowerCase());

            if (targetFolder == null) {
                logger.warning("Nessuna regola per estensione ." + extension + " (" + fileName + ")");
                return false;
            }

            Path targetDir = watchDir.resolve(targetFolder);
            Path targetFile = targetDir.resolve(fileName);

            // Gestione conflitti di nomi
            if (Files.exists(targetFile)) {
                targetFile = handleDuplicate(targetDir, fileName);
            }

            // Sposta il file
            Files.move(file, targetFile, StandardCopyOption.REPLACE_EXISTING);

            logger.info(String.format("[SPSTATO] %s -> %s/", fileName, targetFolder));
            return true;

        } catch (IOException e) {
            logger.severe("Errore organizzazione file " + file + ": " + e.getMessage());
            return false;
        }
    }

    /**
     * Gestisce i file duplicati aggiungendo un suffisso numerico
     */
    private Path handleDuplicate(Path dir, String fileName) {
        String baseName = fileName;
        String extension = "";

        int dotIndex = fileName.lastIndexOf('.');
        if (dotIndex > 0) {
            baseName = fileName.substring(0, dotIndex);
            extension = fileName.substring(dotIndex);
        }

        int counter = 1;
        Path newPath;
        do {
            newPath = dir.resolve(baseName + "_" + counter + extension);
            counter++;
        } while (Files.exists(newPath));

        return newPath;
    }

    /**
     * Estrae l'estensione del file
     */
    private String getFileExtension(String fileName) {
        int lastDot = fileName.lastIndexOf('.');
        if (lastDot > 0 && lastDot < fileName.length() - 1) {
            return fileName.substring(lastDot + 1);
        }
        return "";
    }

    /**
     * Ferta il monitoraggio
     */
    public void stop() {
        running = false;
        try {
            watchService.close();
            logger.info("=== FILE ORGANIZER TERMINATO ===");
        } catch (IOException e) {
            logger.severe("Errore chiusura: " + e.getMessage());
        }
    }

    /**
     * Formatter personalizzato per i log con timestamp
     */
    private class CustomFormatter extends java.util.logging.Formatter {
        private final SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        @Override
        public String format(LogRecord record) {
            String timestamp = dateFormat.format(new Date(record.getMillis()));
            return String.format("[%s] [%s] %s%n",
                timestamp,
                record.getLevel().getName(),
                record.getMessage()
            );
        }
    }

    /**
     * Metodo main - punto di ingresso dell'applicazione
     */
    public static void main(String[] args) {
        try {
            // Percorsi di default
            String userDir = System.getProperty("user.dir");
            Path configPath = Paths.get(userDir, "config.properties");
            Path logPath = Paths.get(userDir, "organizer.log");

            // Directory da monitorare (Downloads dell'utente)
            Path downloadsDir = Paths.get(System.getProperty("user.home"), "Downloads");

            // Consenti override da riga di comando
            if (args.length >= 1) {
                downloadsDir = Paths.get(args[0]);
            }
            if (args.length >= 2) {
                configPath = Paths.get(args[1]);
            }

            // Verifica che il config esista
            if (!Files.exists(configPath)) {
                System.err.println("ERRORE: File config.properties non trovato in: " + configPath);
                System.err.println("Creazione file config.properties di default...");
                createDefaultConfig(configPath);
            }

            // Avvia l'organizer
            FileOrganizer organizer = new FileOrganizer(configPath, logPath);

            // Aggiungi shutdown hook
            Runtime.getRuntime().addShutdownHook(new Thread(organizer::stop));

            organizer.startWatching(downloadsDir);

        } catch (Exception e) {
            System.err.println("ERRORE CRITICO: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    /**
     * Crea un file config.properties di default
     */
    private static void createDefaultConfig(Path configPath) throws IOException {
        String defaultConfig = """
            # File Organizer - Configuration
            # Format: FolderName=ext1,ext2,ext3

            Documenti=pdf,doc,docx,txt,odt,xls,xlsx,ppt,pptx
            Immagini=jpg,jpeg,png,gif,bmp,svg,webp
            Video=mp4,avi,mkv,mov,wmv,flv,webm
            Musica=mp3,flac,wav,aac,ogg,wma
            Archivi=zip,rar,7z,tar,gz,bz2
            Codice=java,py,js,html,css,cpp,c,json,xml
            """;

        Files.write(configPath, defaultConfig.getBytes());
        System.out.println("File config.properties creato con successo!");
    }
}
