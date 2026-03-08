@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Digital Nalanda - Complete Startup
echo ========================================
echo.

echo Starting Docker containers...
docker compose up -d

echo Waiting for services to initialize...
timeout /t 8 /nobreak

echo.
echo Checking backend health...
set maxAttempts=30
set attempt=0

:healthcheck
if %attempt% geq %maxAttempts% goto timeout
timeout /t 2 /nobreak
set /a attempt+=1

for /f %%A in ('powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8080/health' -ErrorAction SilentlyContinue; if ($r.StatusCode -eq 200) { Write-Host 'ready' } } catch { }"') do (
    if "%%A"=="ready" (
        echo Backend is ready!
        goto ready
    )
)

echo Waiting... (attempt %attempt%/%maxAttempts%)
goto healthcheck

:timeout
echo Backend is taking longer than expected, but continuing...

:ready
echo.
echo ========================================
echo Services Status:
echo ========================================
docker compose ps
echo.

echo Starting frontend development server...
echo Frontend will be available at: http://localhost:3000
echo.

start cmd /k "cd frontend && npm run dev"

timeout /t 5 /nobreak

echo Opening website in browser...
start http://localhost:3000

echo.
echo ========================================
echo All Services Started Successfully!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8080
echo.
echo The frontend development server is running in a separate window.
echo You can close this window or keep it open to monitor services.
