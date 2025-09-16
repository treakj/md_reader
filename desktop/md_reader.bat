@echo off
REM MD Reader Launcher
REM This batch file ensures the Python script runs properly

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Run the Python script with the provided argument (if any)
if "%~1"=="" (
    python "%SCRIPT_DIR%leitor_md.pyw"
) else (
    python "%SCRIPT_DIR%leitor_md.pyw" "%~1"
)

REM Pause only if there was an error (for debugging)
if errorlevel 1 (
    echo.
    echo Erro ao executar o MD Reader.
    echo Verifique se o Python esta instalado e as dependencias foram instaladas.
    echo Execute: pip install -r requirements.txt
    echo.
    pause
)
