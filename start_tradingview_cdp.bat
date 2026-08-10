@echo off
echo Stopping TradingView...
taskkill /IM TradingView.exe /F >nul 2>&1
timeout /t 2 /nobreak >nul
echo.
echo Looking for TradingView...
set TV=
if exist "%LOCALAPPDATA%\TradingView\TradingView.exe" set "TV=%LOCALAPPDATA%\TradingView\TradingView.exe"
if exist "%LOCALAPPDATA%\Programs\TradingView\TradingView.exe" set "TV=%LOCALAPPDATA%\Programs\TradingView\TradingView.exe"
if exist "%ProgramFiles%\TradingView\TradingView.exe" set "TV=%ProgramFiles%\TradingView\TradingView.exe"
if "%TV%"=="" (
  echo.
  echo Store app detected or path not found.
  echo BEST FIX: install TradingView Desktop from https://www.tradingview.com/desktop/  ^(not Microsoft Store^)
  echo Then re-run this bat.
  echo.
  echo Or try starting Store app with debug flag ^(often fails^):
  for /d %%D in ("%ProgramFiles%\WindowsApps\TradingView.Desktop_*") do set "TV=%%D\TradingView.exe"
)
if not "%TV%"=="" (
  echo Starting: %TV%
  echo with --remote-debugging-port=9222
  start "" "%TV%" --remote-debugging-port=9222
  timeout /t 4 /nobreak >nul
  echo.
  echo Testing CDP...
  curl -s http://127.0.0.1:9222/json/version
  echo.
  if errorlevel 1 echo CDP NOT UP - install non-Store Desktop build.
) else (
  echo No executable found.
)
pause
