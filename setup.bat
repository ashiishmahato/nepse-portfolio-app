@echo off
REM Smart NEPSE Investor
REM Windows setup script

echo ======================================
echo Smart NEPSE Investor Setup
echo ======================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8+
    exit /b 1
)
echo OK - Python found
echo.

REM Setup Backend
echo [2/5] Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
    echo OK - Virtual environment created
) else (
    echo OK - Virtual environment exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install -q -r requirements.txt
echo OK - Backend dependencies installed
echo.

REM Initialize database
echo [3/5] Initializing database...
python -c "from app.database import init_db; init_db()"
echo OK - Database initialized
echo.

REM Go back
cd ..

REM Setup Frontend
echo [4/5] Setting up frontend...
cd frontend

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed. Please install Node.js 16+
    exit /b 1
)

REM Install dependencies
npm install -q
echo OK - Frontend dependencies installed
echo.

cd ..

REM Final instructions
echo [5/5] Setup complete!
echo.
echo ================================================
echo Smart NEPSE Investor is ready to run!
echo ================================================
echo.
echo To start the application, run these commands in separate terminals:
echo.
echo Terminal 1 - Backend Server:
echo    cd backend
echo    python -m uvicorn app.main:app --reload
echo.
echo Terminal 2 - Frontend Server:
echo    cd frontend
echo    npm run dev
echo.
echo Terminal 3 - Background Scheduler (optional):
echo    cd backend
echo    python scheduler.py
echo.
echo Then open: http://localhost:3000
echo.
pause
