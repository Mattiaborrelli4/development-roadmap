@echo off
REM Build script per Windows con CMake

echo Building C++ Memory Allocator...

if not exist build mkdir build
cd build

echo Running CMake...
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release

if %ERRORLEVEL% NEQ 0 (
    echo CMake configuration failed!
    exit /b 1
)

echo Building...
mingw32-make

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b 1
)

echo.
echo ========================================
echo Build completato con successo!
echo Eseguibile: build\bin\allocator.exe
echo ========================================

cd ..
pause
