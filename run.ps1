###############################################################################
# Author:
#   Devid Dokash
# Description:
#   A powershell script that prepares a virtual environment and installs
#   all the required dependencies for starting and running the API.
###############################################################################
# Verificar que el script esta en la misma carpeta que la aplicacion
###############################################################################
$SERVER_NAME = "app"
if (-Not (Test-Path $SERVER_NAME)) {
    Write-Host "[ERROR] Please run or move this script to the root directory containing the '$SERVER_NAME' folder." -ForegroundColor Red
    exit 1
}

###############################################################################
# Verificar que el fichero de dependencias existe
###############################################################################
if (-Not (Test-Path "$SERVER_NAME\requirements.txt")) {
    Write-Host "[ERROR] No 'requirements.txt' file? Please re-download the source code." -ForegroundColor Red
    exit 1
}

###############################################################################
# Creacion del entorno virtual
###############################################################################
$FATAL_ERROR = $true
$VENV_NAME = "roams-venv"
$VENV_PATH = (Get-Location).Path + "\" + $VENV_NAME
$PYTHONVERSIONS = @("python3", "py3", "python", "py")

Write-Host "[INFO] Attempting to create a virtual environment..."
foreach ($PYTHON in $PYTHONVERSIONS) {
    Write-Host "  -> Trying with '$PYTHON' (ignore errors for now)..."
    try {
        & $PYTHON -m venv $VENV_NAME
        Write-Host "[SUCCESS] Virtual environment created at: $VENV_PATH" -ForegroundColor Green
        $FATAL_ERROR = $false
        break
    } catch {
        Write-Host $_.Exception.Message
    }
}

if ($FATAL_ERROR -eq $true) {
    Write-Host "[ERROR] Python is not installed or not found. Please check the errors above." -ForegroundColor Red
    exit 1
}

###############################################################################
# Copiar la aplicacion al nuevo entorno virtual creado
###############################################################################
Write-Host "`n[INFO] Copying the application to the new virtual environment..."
Copy-Item -Recurse -Path $SERVER_NAME -Destination $VENV_PATH

###############################################################################
# Moverse al nuevo entorno virtual y activarlo
###############################################################################
Write-Host "`n[INFO] Activating the virtual environment..."
Set-Location -Path $VENV_PATH
& .\Scripts\Activate.ps1

###############################################################################
# Moverse al nuevo entorno virtual y activarlo
###############################################################################
Write-Host "`n[INFO] Installing Python dependencies..."
& $PYTHON -m pip install -r "$SERVER_NAME\requirements.txt"

###############################################################################
# Ejecutar la API
###############################################################################
Write-Host "`n[INFO] Starting the API..."
& $PYTHON "$VENV_PATH\$SERVER_NAME\server.py"

###############################################################################
# Salir del entorno virtual
###############################################################################
Write-Host "`n[INFO] Deactivating the virtual environment and cleaning up..."
deactivate
Set-Location -Path (Get-Location).Path

###############################################################################
# Limpiar restos
###############################################################################
Write-Host "[INFO] Removing virtual environment directory..."
Remove-Item -Recurse -Force $VENV_PATH
Write-Host "[DONE] Setup process completed successfully." -ForegroundColor Green