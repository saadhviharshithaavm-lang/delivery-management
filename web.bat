@echo off
REM Start Web server
echo Starting Web server...
echo Server will be available at http://localhost:8080
echo.
python -m http.server 8080
pause