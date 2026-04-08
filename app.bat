@echo off
REM Start FastAPI server
echo Starting FastAPI server...
echo Server will be available at http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
cd backend
call venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause