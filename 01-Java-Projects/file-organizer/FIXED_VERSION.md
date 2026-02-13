# File Organizer - Fixed Version (No External Dependencies)

## Overview

This is a FIXED version of the File Organizer that compiles and runs WITHOUT any external JAR files or libraries. It uses only standard Java library features.

## What Was Fixed

### 1. Removed Gson Dependency
- **Problem**: Code required `com.google.gson` package (external library)
- **Solution**: Replaced JSON configuration with simple `.properties` file format
- **Benefit**: No external JARs needed - uses standard Java `Properties` class

### 2. Fixed Formatter Ambiguity
- **Problem**: `CustomFormatter extends Formatter` was ambiguous
- **Solution**: Changed to `extends java.util.logging.Formatter`
- **Benefit**: Explicit, unambiguous class reference

### 3. Simplified Configuration
- **Problem**: Required complex JSON structure with nested arrays
- **Solution**: Simple properties file format: `FolderName=ext1,ext2,ext3`
- **Benefit**: Easier to edit, understand, and maintain

## Quick Start

### Option 1: Using Build Scripts (Windows)

```batch
# Build the project
build-simple.bat

# Run the organizer
run-simple.bat
```

### Option 2: Manual Compilation (Any OS)

```bash
# Compile
javac -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java

# Create default config (or edit src/main/resources/config.properties first)
cp src/main/resources/config.properties out/

# Run
java -cp out com.organizer.FileOrganizer
```

## Configuration

The project uses `config.properties` instead of JSON. Format:

```properties
# Comments start with #
Documenti=pdf,doc,docx,txt,odt,rtf,xls,xlsx,ppt,pptx,csv
Immagini=jpg,jpeg,png,gif,bmp,svg,webp
Video=mp4,avi,mkv,mov,wmv,flv,webm
Musica=mp3,flac,wav,aac,ogg,wma
Archivi=zip,rar,7z,tar,gz,bz2
Codice=java,py,js,html,css,cpp,c,h,cs,php,rb,go,rs
```

### Default Behavior

- **Monitored Directory**: `~/Downloads` (user's Downloads folder)
- **Log File**: `organizer.log` in current directory
- **Config File**: `config.properties` in current directory

### Command Line Arguments

```bash
# Monitor specific directory
java -cp out com.organizer.FileOrganizer /path/to/watch

# Monitor with custom config
java -cp out com.organizer.FileOrganizer /path/to/watch /path/to/config.properties
```

## How It Works

1. **File Detection**: Uses Java's `WatchService` to detect new files
2. **Categorization**: Reads file extension and maps to folder using rules
3. **Organization**: Moves files to appropriate category folders
4. **Duplicate Handling**: Adds numeric suffix to duplicate filenames
5. **Logging**: Writes all actions to `organizer.log`

## Features

- Real-time file monitoring
- Automatic file organization by extension
- Duplicate file handling (filename_1.ext, filename_2.ext, etc.)
- Comprehensive logging to file and console
- Graceful shutdown handling
- Zero external dependencies

## Project Structure

```
file-organizer/
├── src/main/java/com/organizer/
│   └── FileOrganizer.java          # Main application (FIXED)
├── src/main/resources/
│   └── config.properties           # Configuration file (NEW)
├── out/                            # Compiled classes
│   └── com/organizer/
│       ├── FileOrganizer.class
│       └── FileOrganizer$CustomFormatter.class
├── build-simple.bat                # Build script (NO external deps)
├── run-simple.bat                  # Run script (NO external deps)
└── organizer.log                   # Log file (created at runtime)
```

## Technical Changes

### Before (Required Gson):
```java
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

// JSON parsing
Gson gson = new Gson();
Type mapType = new TypeToken<Map<String, List<String>>>(){}.getType();
Map<String, List<String>> config = gson.fromJson(reader, mapType);
```

### After (Standard Java Only):
```java
import java.util.Properties;

// Properties parsing
Properties props = new Properties();
props.load(input);
for (String folder : props.stringPropertyNames()) {
    String extensions = props.getProperty(folder);
    String[] extArray = extensions.split(",");
    // ...
}
```

## Requirements

- Java JDK 11 or higher
- No external libraries required!

## Compilation Verification

The code has been tested and compiles successfully:
```bash
$ javac -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
$ echo $?
0
```

## Troubleshooting

**Issue**: "class file has wrong version"
- **Solution**: Ensure you're using Java 11+: `java -version`

**Issue**: "config.properties not found"
- **Solution**: Run from project root or provide full path to config file

**Issue**: Files not being organized
- **Solution**: Check that file extensions match those in config.properties (case-insensitive)

## Comparison: Original vs Fixed

| Feature | Original | Fixed Version |
|---------|----------|---------------|
| External JARs | Required (Gson) | NONE |
| Config Format | JSON | Properties |
| Formatter | Ambiguous | Explicit |
| Compile Script | Checks for gson-*.jar | Simple javac |
| Portability | Requires lib/ folder | Self-contained |

## License

Same as original project.
