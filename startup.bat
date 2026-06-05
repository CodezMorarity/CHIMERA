@echo off
setlocal EnableExtensions
title CHIMERA Startup

cd /d "%~dp0"
set "ROOT=%~dp0"
set "RUST_DIR=%ROOT%rust_core"
set "CHIMERA_EXE=%RUST_DIR%\target\debug\chimera_core.exe"
set "DASHBOARD_APP=%ROOT%dashboard\app.py"
set "REQUIREMENTS=%ROOT%python_engine\requirements.txt"
set "RESULT_DIR=%ROOT%Result"
set "BUNDLED_PYTHON=C:\Users\TEJAS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

echo.
echo ============================================================
echo  CHIMERA Startup
echo  Chaotic Hybrid Matrix Encryption with Randomized DNA Encoding
echo ============================================================
echo.

if not exist "%RESULT_DIR%" mkdir "%RESULT_DIR%"

call :find_python
if errorlevel 1 goto fatal

call :check_cargo
if errorlevel 1 goto fatal

echo [1/3] Python bridge:
echo       %CHIMERA_PYTHON%
echo.

echo [2/3] Building Rust core...
pushd "%RUST_DIR%" >nul
cargo build
if errorlevel 1 (
    popd >nul
    echo.
    echo ERROR: Rust build failed.
    goto fatal
)
popd >nul
if not exist "%CHIMERA_EXE%" (
    echo.
    echo ERROR: Built executable was not found at:
    echo %CHIMERA_EXE%
    goto fatal
)

echo.
echo [3/3] CHIMERA is ready.
echo.

goto menu

:menu
echo ------------------------------------------------------------
echo  Choose an action
echo ------------------------------------------------------------
echo  1. Encrypt a file
echo  2. Decrypt a .chimera file
echo  3. Run demo round-trip
echo  4. Start Streamlit dashboard
echo  5. Run tests
echo  0. Exit
echo.
set /p "CHOICE=Enter choice: "

if "%CHOICE%"=="1" goto encrypt
if "%CHOICE%"=="2" goto decrypt
if "%CHOICE%"=="3" goto demo
if "%CHOICE%"=="4" goto dashboard
if "%CHOICE%"=="5" goto tests
if "%CHOICE%"=="0" goto end

echo Invalid choice.
echo.
goto menu

:encrypt
echo.
set "INPUT_FILE="
set "OUTPUT_FILE="
set "PASSWORD="
set /p "INPUT_FILE=Input file path: "
set /p "OUTPUT_FILE=Output .chimera filename/path [blank = Result\encrypted.chimera]: "
set /p "PASSWORD=Password: "
if not exist "%INPUT_FILE%" (
    echo.
    echo ERROR: Input file does not exist:
    echo   %INPUT_FILE%
    echo For encryption, choose your original file, for example:
    echo   D:\CHIMERA\test.txt
    echo.
    pause
    goto menu
)
if exist "%INPUT_FILE%\" (
    echo.
    echo ERROR: Input path is a folder, but encryption needs a file.
    echo.
    pause
    goto menu
)
call :resolve_encrypt_output
echo.
"%CHIMERA_EXE%" encrypt "%INPUT_FILE%" "%OUTPUT_FILE%" "%PASSWORD%"
echo.
pause
goto menu

:decrypt
echo.
set "INPUT_FILE="
set "OUTPUT_FILE="
set "PASSWORD="
set /p "INPUT_FILE=Input .chimera path: "
set /p "OUTPUT_FILE=Restored output filename/path [blank = Result\decrypted_output]: "
set /p "PASSWORD=Password: "
if not exist "%INPUT_FILE%" (
    echo.
    echo ERROR: Input .chimera file does not exist:
    echo   %INPUT_FILE%
    echo For decryption, choose an existing encrypted file, for example:
    echo   D:\CHIMERA\encrypted.chimera
    echo.
    pause
    goto menu
)
if exist "%INPUT_FILE%\" (
    echo.
    echo ERROR: Input path is a folder, but decryption needs a .chimera file.
    echo.
    pause
    goto menu
)
call :resolve_decrypt_output
echo.
"%CHIMERA_EXE%" decrypt "%INPUT_FILE%" "%OUTPUT_FILE%" "%PASSWORD%"
echo.
pause
goto menu

:demo
echo.
echo Running a sample encrypt/decrypt round-trip...
set "DEMO_DIR=%ROOT%demo_workspace"
if not exist "%DEMO_DIR%" mkdir "%DEMO_DIR%"
set "DEMO_INPUT=%DEMO_DIR%\sample_input.txt"
set "DEMO_ENCRYPTED=%RESULT_DIR%\sample_output.chimera"
set "DEMO_RESTORED=%RESULT_DIR%\sample_restored.txt"
> "%DEMO_INPUT%" echo Hello from CHIMERA hybrid Rust plus Python encryption.
"%CHIMERA_EXE%" encrypt "%DEMO_INPUT%" "%DEMO_ENCRYPTED%" "demo-password"
if errorlevel 1 (
    echo Demo encryption failed.
    pause
    goto menu
)
"%CHIMERA_EXE%" decrypt "%DEMO_ENCRYPTED%" "%DEMO_RESTORED%" "demo-password"
if errorlevel 1 (
    echo Demo decryption failed.
    pause
    goto menu
)
echo.
echo Demo complete:
echo   %DEMO_INPUT%
echo   %DEMO_ENCRYPTED%
echo   %DEMO_RESTORED%
echo.
pause
goto menu

:dashboard
echo.
echo Checking dashboard dependencies...
"%CHIMERA_PYTHON%" -c "import streamlit, matplotlib, pandas" >nul 2>nul
if errorlevel 1 (
    echo Dashboard dependencies are missing.
    echo Trying to install them from python_engine\requirements.txt...
    "%CHIMERA_PYTHON%" -m pip install -r "%REQUIREMENTS%"
)

"%CHIMERA_PYTHON%" -c "import streamlit, matplotlib, pandas" >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Streamlit dashboard dependencies are still unavailable.
    echo You can still use encryption, decryption, demo, and tests from this launcher.
    echo.
    pause
    goto menu
)

echo Starting dashboard at http://localhost:8501
echo Close the Streamlit window or press Ctrl+C here to stop it.
echo.
"%CHIMERA_PYTHON%" -m streamlit run "%DASHBOARD_APP%"
echo.
pause
goto menu

:tests
echo.
pushd "%RUST_DIR%" >nul
cargo test
popd >nul
echo.
pause
goto menu

:resolve_encrypt_output
if "%OUTPUT_FILE%"=="" (
    set "OUTPUT_FILE=%RESULT_DIR%\encrypted.chimera"
    echo Output left blank. Using:
    call echo   %%OUTPUT_FILE%%
    exit /b 0
)
if exist "%OUTPUT_FILE%\" (
    set "OUTPUT_FILE=%OUTPUT_FILE%\encrypted.chimera"
    echo Output path is a folder. Using:
    call echo   %%OUTPUT_FILE%%
    exit /b 0
)
if "%OUTPUT_FILE:~1,1%"==":" exit /b 0
if not "%OUTPUT_FILE:\=%"=="%OUTPUT_FILE%" exit /b 0
set "OUTPUT_FILE=%RESULT_DIR%\%OUTPUT_FILE%"
echo Saving output in Result:
call echo   %%OUTPUT_FILE%%
exit /b 0

:resolve_decrypt_output
if "%OUTPUT_FILE%"=="" (
    set "OUTPUT_FILE=%RESULT_DIR%\decrypted_output"
    echo Output left blank. Using:
    call echo   %%OUTPUT_FILE%%
    exit /b 0
)
if exist "%OUTPUT_FILE%\" (
    set "OUTPUT_FILE=%OUTPUT_FILE%\restored_output"
    echo Output path is a folder. Using:
    call echo   %%OUTPUT_FILE%%
    exit /b 0
)
if "%OUTPUT_FILE:~1,1%"==":" exit /b 0
if not "%OUTPUT_FILE:\=%"=="%OUTPUT_FILE%" exit /b 0
set "OUTPUT_FILE=%RESULT_DIR%\%OUTPUT_FILE%"
echo Saving output in Result:
call echo   %%OUTPUT_FILE%%
exit /b 0

:find_python
if defined CHIMERA_PYTHON (
    "%CHIMERA_PYTHON%" --version >nul 2>nul
    if not errorlevel 1 exit /b 0
)

if exist "%BUNDLED_PYTHON%" (
    set "CHIMERA_PYTHON=%BUNDLED_PYTHON%"
    exit /b 0
)

for %%P in (python.exe python3.exe py.exe) do (
    where %%P >nul 2>nul
    if not errorlevel 1 (
        for /f "delims=" %%F in ('where %%P 2^>nul') do (
            "%%F" --version >nul 2>nul
            if not errorlevel 1 (
                set "CHIMERA_PYTHON=%%F"
                exit /b 0
            )
        )
    )
)

echo ERROR: No working Python interpreter was found.
echo Install Python 3 or set CHIMERA_PYTHON to python.exe.
exit /b 1

:check_cargo
where cargo >nul 2>nul
if errorlevel 1 (
    echo ERROR: Cargo was not found on PATH.
    echo Install Rust from https://rustup.rs/ and reopen this launcher.
    exit /b 1
)
exit /b 0

:fatal
echo.
echo Startup could not continue. Fix the message above and run startup.bat again.
echo.
pause
exit /b 1

:end
echo Goodbye.
endlocal
