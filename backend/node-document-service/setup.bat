@echo off
echo ========================================
echo Document Management Module - Setup
echo ========================================
echo.

echo [1/4] Installing Node.js dependencies...
cd backend\node-document-service
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [2/4] Creating uploads directory...
if not exist "uploads" mkdir uploads
echo Uploads directory ready
echo.

echo [3/4] Checking MongoDB connection...
echo Please ensure MongoDB is running on localhost:27017
echo.

echo [4/4] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Start MongoDB: mongod
echo 2. Start service: npm start
echo 3. Test API: node test-api.js
echo 4. Open React app and use DocumentManagement component
echo.
echo For detailed instructions, see QUICKSTART.md
echo ========================================
pause
