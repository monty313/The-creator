@echo off
echo Stopping TradingView...
taskkill /IM TradingView.exe /F >nul 2>&1
timeout /t 2 /nobreak >nul
echo Starting TradingView with remote debugging (port 9222)...
start "" "C:\Users\user\AppData\Local\tradingview-mcp\TradingView.Desktop_3.3.0.7992_x64__n534cwy3pjxzj\TradingView.exe" --remote-debugging-port=9222
timeout /t 5 /nobreak >nul
echo.
echo Checking CDP...
curl -s http://127.0.0.1:9222/json/version
echo.
echo If you see JSON above, CDP is UP. Leave this TradingView window open.
pause
