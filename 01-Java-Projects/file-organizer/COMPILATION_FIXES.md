# File Organizer - Compilation Fixes Applied

## Summary

All compilation errors have been resolved. The project now compiles and runs using only the standard Java library.

## Errors Fixed

### Error 1: Missing com.google.gson Package
**Original Error:**
```
FileOrganizer.java:3: error: package com.google.gson does not exist
FileOrganizer.java:4: error: package com.google.gson.reflect does not exist
```

**Fix Applied:**
- Removed all Gson imports
- Replaced JSON-based configuration with Java Properties format
- Modified `loadRules()` method to parse properties instead of JSON

**Code Changes:**
```java
// REMOVED:
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;

// ADDED:
import java.util.Properties;  // Already in standard library
```

### Error 2: Ambiguous Formatter Class
**Original Error:**
```
FileOrganizer.java:301: error: Formatter is ambiguous
class CustomFormatter extends Formatter
```

**Fix Applied:**
- Changed `extends Formatter` to `extends java.util.logging.Formatter`
- Explicitly specifies which Formatter class to use

**Code Changes:**
```java
// BEFORE:
private class CustomFormatter extends Formatter {

// AFTER:
private class CustomFormatter extends java.util.logging.Formatter {
```

## Configuration Format Changes

### Before (JSON):
```json
{
  "Documenti": ["pdf", "doc", "docx", "txt"],
  "Immagini": ["jpg", "jpeg", "png", "gif"]
}
```

### After (Properties):
```properties
Documenti=pdf,doc,docx,txt
Immagini=jpg,jpeg,png,gif
```

## Files Modified

1. **FileOrganizer.java** - Main source file
   - Removed Gson imports
   - Fixed Formatter class reference
   - Rewrote `loadRules()` method
   - Updated `main()` to use config.properties
   - Updated `createDefaultConfig()` to create properties file

2. **config.properties** (NEW) - Configuration file
   - Created in `src/main/resources/`
   - Contains default file organization rules

3. **build-simple.bat** (NEW) - Build script
   - No dependency checking for Gson
   - Simple javac compilation

4. **run-simple.bat** (NEW) - Run script
   - No external classpath needed

## Compilation Results

```bash
$ javac -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
# Success - No errors
# Output:
# out/com/organizer/FileOrganizer.class
# out/com/organizer/FileOrganizer$CustomFormatter.class
```

## How to Use

### Build:
```bash
# Windows
build-simple.bat

# Linux/Mac
javac -d out -sourcepath src/main/java src/main/java/com/organizer/FileOrganizer.java
```

### Run:
```bash
# Windows
run-simple.bat

# Linux/Mac
java -cp out com.organizer.FileOrganizer
```

## Verification

Tested with:
- Java JDK 24
- Windows environment
- Standard Java library only

Status: ✓ Compiles successfully
        ✓ No external dependencies required
        ✓ Ready to use

## Migration from Original Version

If you have an existing `config.json`, convert it to `config.properties`:

**Original JSON:**
```json
{
  "Documents": ["pdf", "doc", "txt"],
  "Images": ["jpg", "png", "gif"]
}
```

**New Properties:**
```properties
Documents=pdf,doc,txt
Images=jpg,png,gif
```

Simply list extensions comma-separated after each folder name.
