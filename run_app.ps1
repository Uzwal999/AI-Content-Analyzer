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

function Test-PortAvailable {
    param([int]$Port)
    $listener = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Parse("127.0.0.1"), $Port)
        $listener.Start()
        return $true
    }
    catch {
        return $false
    }
    finally {
        if ($listener -ne $null) {
            $listener.Stop()
        }
    }
}

function Get-OpenPort {
    param(
        [int]$Start,
        [int]$End
    )
    for ($port = $Start; $port -le $End; $port++) {
        if (Test-PortAvailable -Port $port) {
            return $port
        }
    }
    throw "No open port found between $Start and $End."
}

function Test-BackendHealth {
    param([int]$Port)
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/" -TimeoutSec 2
        return ($response.message -like "*EverVFX AI Brand Content Analyzer API is running*")
    }
    catch {
        return $false
    }
}

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$PythonExe = Join-Path $Backend ".venv\Scripts\python.exe"
$Requirements = Join-Path $Backend "requirements.txt"
$DepsMarker = Join-Path $Backend ".venv\.deps-installed"

Write-Host "EverVFX AI Brand Content Analyzer - Easy Launcher" -ForegroundColor Green
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

$BackendPort = 8000
$BackendAlreadyRunning = Test-BackendHealth -Port $BackendPort
if (-not $BackendAlreadyRunning -and -not (Test-PortAvailable -Port $BackendPort)) {
    $BackendPort = Get-OpenPort -Start 8001 -End 8010
}

$FrontendPort = Get-OpenPort -Start 3000 -End 3010
$ApiUrl = "http://127.0.0.1:$BackendPort"
$AppUrl = "http://localhost:$FrontendPort"

Write-Step "Starting backend and frontend"

if ($BackendAlreadyRunning) {
    Write-Host "Backend is already running at $ApiUrl" -ForegroundColor Green
}
else {
    $BackendCommand = "cd $(Quote-Path $Backend); .\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port $BackendPort"
    Start-Process powershell -ArgumentList @("-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $BackendCommand)

    Write-Step "Waiting for backend health check"
    $BackendReady = $false
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 1
        if (Test-BackendHealth -Port $BackendPort) {
            $BackendReady = $true
            break
        }
    }

    if (-not $BackendReady) {
        Write-Host "Backend did not respond yet. Check the backend PowerShell window for errors." -ForegroundColor Yellow
    }
}

$FrontendCommand = "cd $(Quote-Path $Frontend); `$env:NEXT_PUBLIC_API_URL=$(Quote-Path $ApiUrl); npm run dev -- --port $FrontendPort"
Start-Process powershell -ArgumentList @("-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $FrontendCommand)

Write-Step "Opening the app"
Start-Sleep -Seconds 6
Start-Process $AppUrl

Write-Host ""
Write-Host "App URL:     $AppUrl" -ForegroundColor Green
Write-Host "Backend API: $ApiUrl/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Keep the two PowerShell server windows open while using the app."
Write-Host "Close those windows when you want to stop the app."

