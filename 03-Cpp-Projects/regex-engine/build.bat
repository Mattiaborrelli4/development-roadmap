@echo off
REM Build script per Regex Engine (Windows)

echo.
echo ========================================
echo   Regex Engine - Build Script
echo ========================================
echo.

REM Verifica se CMake è disponibile
where cmake >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] CMake trovato. Utilizzo CMake per la build...
    echo.

    REM Crea directory build
    if not exist build mkdir build
    cd build

    REM Configura con CMake
    cmake .. -G "NMake Makefiles" 2>nul
    if %ERRORLEVEL% NEQ 0 (
        cmake .. -G "MinGW Makefiles" 2>nul
    )
    if %ERRORLEVEL% NEQ 0 (
        cmake ..
    )

    if %ERRORLEVEL% EQU 0 (
        echo.
        cmake --build . --config Release
        echo.
        echo [SUCCESS] Build completata!
        echo Eseguibile: build\regex.exe ^(o regex.exe^)
        echo.
    ) else (
        echo [ERROR] Configurazione CMake fallita.
        echo.
        goto :manual_build
    )

    cd ..
) else (
    echo [INFO] CMake non trovato. Tentativo build manuale...
    echo.
    goto :manual_build
)

goto :end

:manual_build
REM Build manuale con g++ se disponibile
where g++ >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Utilizzo g++ per compilare...
    echo.
    g++ --version | findstr "g++"
    echo.
    g++ -std=c++17 -O2 -Wall regex.cpp nfa.cpp dfa.cpp main.cpp -o regex.exe

    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [SUCCESS] Build completata!
        echo Eseguibile: regex.exe
        echo.
    ) else (
        echo [ERROR] Compilazione fallita. Controlla gli errori sopra.
        echo.
    )
) else (
    REM Build manuale con cl (MSVC) se disponibile
    where cl >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo [INFO] Utilizzo MSVC cl per compilare...
        echo.
        call cl /EHsc /std:c++17 /O2 regex.cpp nfa.cpp dfa.cpp main.cpp /Fe:regex.exe

        if %ERRORLEVEL% EQU 0 (
            echo.
            echo [SUCCESS] Build completata!
            echo Eseguibile: regex.exe
            echo.
        ) else (
            echo [ERROR] Compilazione fallita. Controlla gli errori sopra.
            echo.
        )
    ) else (
        echo [ERROR] Nessun compilatore trovato ^(g++ o cl^).
        echo [INFO] Installa MinGW, MSVC, o CMake per compilare.
        echo.
    )
)

:end
pause
