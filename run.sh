#!/bin/bash
###############################################################################
# Author:
#   Devid Dokash
# Description:
#   A bash script that prepares a virtual environment and installs
#   all the required dependencies for starting and running the API.
###############################################################################
# Verificar que el script esta en la misma carpeta que la aplicacion
###############################################################################
SERVER_NAME=app
if [ ! -d "$SERVER_NAME" ]; then
    echo "[ERROR] Please run or move this script to the root directory containing the '$SERVER_NAME' folder."
    exit 1
fi
###############################################################################
# Verificar que el fichero de dependencias existe
###############################################################################
if [ ! -f "$SERVER_NAME/requirements.txt" ]; then
    echo "[ERROR] No 'requirements.txt' file? Please re-download the source code."
    exit 1
fi
###############################################################################
# Creacion del entorno virtual
###############################################################################
FATAL_ERROR=true
VENV_NAME=roams-venv
VENV_PATH=$(pwd)/$VENV_NAME
PYTHONVERSE=("python3" "py3" "python" "py")
echo "[INFO] Attempting to create a virtual environment..."
for PYTHON in "${PYTHONVERSE[@]}"; do
    echo "  -> Trying with '$PYTHON' (ignore errors for now)..."
    $PYTHON -m venv $VENV_NAME 
    if [ $? -eq 0 ]; then
        echo "[SUCCESS] Virtual environment created at: $VENV_PATH" 
        FATAL_ERROR=false
        break
    fi
done
if [ $FATAL_ERROR = true ]; then
    echo "[ERROR] Python is not installed or not found. Please check the errors above."
    exit 1
fi
###############################################################################
# Copiar la aplicacion al nuevo entorno virtual creado
###############################################################################
echo -e "\n[INFO] Copying the application to the new virtual environment..."
cp -r $SERVER_NAME $VENV_PATH
###############################################################################
# Moverse al nuevo entorno virtual y activarlo
###############################################################################
echo -e "\n[INFO] Activating the virtual environment..."
cd $VENV_PATH && source ./Scripts/activate
###############################################################################
# Moverse al nuevo entorno virtual y activarlo
###############################################################################
echo -e "\n[INFO] Installing Python dependencies..."
$PYTHON -m pip install -r $SERVER_NAME/requirements.txt
###############################################################################
# Ejecutar la API
###############################################################################
echo -e "\n[INFO] Starting the API..."
$PYTHON $VENV_PATH/$SERVER_NAME/server.py
###############################################################################
# Salir del entorno virtual
###############################################################################
echo -e "\n[INFO] Deactivating the virtual environment and cleaning up..."
deactivate && cd ..
###############################################################################
# Limpiar restos
###############################################################################
echo "[INFO] Removing virtual environment directory..."
rm -r $VENV_PATH
echo "[DONE] Setup process completed successfully."










