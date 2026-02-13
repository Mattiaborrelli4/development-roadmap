# File Organizer - Quick Reference Card

## Status: ✓ READY TO USE

All compilation errors fixed. No external dependencies needed.

---

## Build & Run

### Windows
```batch
build-simple.bat
run-simple.bat
```

### Linux/Mac
```bash
./build-simple.sh
./run-simple.sh
```

### Manual (Any OS)
```bash
javac -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
java -cp out com.organizer.FileOrganizer
```

---

## What Was Fixed

### 1. Gson Dependency Removed
- **Before**: Required `gson-*.jar` in lib/
- **After**: Uses standard Java `Properties` class

### 2. Formatter Ambiguity Fixed
- **Before**: `extends Formatter` (ambiguous)
- **After**: `extends java.util.logging.Formatter` (explicit)

### 3. Configuration Simplified
- **Before**: JSON format with nested arrays
- **After**: Simple properties file

---

## Configuration Format

### config.properties
```properties
FolderName=ext1,ext2,ext3

Documenti=pdf,doc,txt
Immagini=jpg,png,gif
Video=mp4,avi,mkv
```

Lines starting with `#` are comments.

---

## Command Line Options

```bash
# Default: monitor ~/Downloads
java -cp out com.organizer.FileOrganizer

# Custom folder
java -cp out com.organizer.FileOrganizer /path/to/folder

# Custom folder + config
java -cp out com.organizer.FileOrganizer /path/to/folder /path/to/config.properties
```

---

## File Locations

| File | Location |
|------|----------|
| Source | `src/main/java/com/organizer/FileOrganizer.java` |
| Config | `src/main/resources/config.properties` |
| Compiled | `out/com/organizer/FileOrganizer.class` |
| Logs | `organizer.log` (in current dir) |

---

## Key Features

- Real-time file monitoring
- Automatic organization by extension
- Duplicate handling (filename_1.ext, filename_2.ext, etc.)
- Comprehensive logging
- Zero external dependencies
- Cross-platform

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "class file has wrong version" | Use Java 11+ |
| "config.properties not found" | Run from project root or provide full path |
| Files not organizing | Check extensions match config (case-insensitive) |

---

## Migration from JSON

### Before (config.json)
```json
{
  "Documents": ["pdf", "doc", "txt"]
}
```

### After (config.properties)
```properties
Documents=pdf,doc,txt
```

---

## Requirements

- Java JDK 11+
- No external libraries

---

## Verification

```bash
$ javac -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
$ echo $?
0
```

Exit code 0 = Success!

---

## Documentation

- **README_FIXED.md** - Complete guide
- **FIXED_VERSION.md** - Detailed documentation
- **COMPILATION_FIXES.md** - Technical details of fixes

---

**Project Location:**
`C:\Users\matti\Desktop\Project Ideas Portfolio\01-Java-Projects\file-organizer`

**Status:** ✓ All errors fixed, compiles successfully, ready to use!
