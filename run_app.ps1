$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Quote-Path {
    param([string]$Path)
    return "'" + $Path.Replace("'", "''") + "'"
}

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$PythonExe = Join-Path $Backend ".venv\Scripts\python.exe"
$Requirements = Join-Path $Backend "requirements.txt"
$DepsMarker = Join-Path $Backend ".venv\.deps-installed"

Write-Host "AI Brand Content Analyzer - Easy Launcher" -ForegroundColor Green
Write-Host "Project: $Root"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not installed or not available in PATH."
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "Node.js/npm is not installed or not available in PATH."
}

if (-not (Test-Path $PythonExe)) {
    Write-Step "Creating backend Python virtual environment"
    Push-Location $Backend
    python -m venv .venv
    Pop-Location
}

$ShouldInstallBackend = -not (Test-Path $DepsMarker)
if ((Test-Path $DepsMarker) -and (Test-Path $Requirements)) {
    $ShouldInstallBackend = (Get-Item $Requirements).LastWriteTime -gt (Get-Item $DepsMarker).LastWriteTime
}

if ($ShouldInstallBackend) {
    Write-Step "Installing backend dependencies"
    Push-Location $Backend
    & $PythonExe -m pip install --upgrade pip
    & $PythonExe -m pip install -r requirements.txt
    "installed $(Get-Date -Format s)" | Set-Content -Path $DepsMarker
    Pop-Location
}
else {
    Write-Step "Backend dependencies already installed"
}

if (-not (Test-Path (Join-Path $Frontend "node_modules"))) {
    Write-Step "Installing frontend dependencies"
    Push-Location $Frontend
    npm install
    Pop-Location
}
else {
    Write-Step "Frontend dependencies already installed"
}

Write-Step "Starting backend and frontend"

$BackendCommand = "cd $(Quote-Path $Backend); .\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000"
$FrontendCommand = "cd $(Quote-Path $Frontend); npm run dev"

Start-Process powershell -ArgumentList @("-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $BackendCommand)
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList @("-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $FrontendCommand)

Write-Step "Opening the app"
Start-Sleep -Seconds 6
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "App URL:     http://localhost:3000" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Keep the two PowerShell server windows open while using the app."
Write-Host "Close those windows when you want to stop the app."

