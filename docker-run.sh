#!/bin/bash
###############################################################################
# Author:
#   Devid Dokash
# Description:
#   A bash script that prepares a Docker environment and starts the API.
###############################################################################
# Verificar que el script esta en la misma carpeta que la aplicacion
###############################################################################
SERVER_NAME=app
if [ ! -d "$SERVER_NAME" ]; then
    echo "[SCRIPT ERROR] Please run or move this script to the root directory containing the '$SERVER_NAME' folder."
    exit 1
fi
###############################################################################
# Verificar que el fichero de dependencias existe
###############################################################################
if [ ! -f "$SERVER_NAME/requirements.txt" ]; then
    echo "[SCRIPT ERROR] No 'requirements.txt' file? Please re-download the source code."
    exit 1
fi
###############################################################################
# Verificar que el fichero de Dockerfile existe
###############################################################################
if [ ! -f "Dockerfile" ]; then
    echo "[SCRIPT ERROR] No 'Dockerfile'? Please re-download the source code."
    exit 1
fi
###############################################################################
# Construir la imagen
###############################################################################
IMAGE=roams-test-monorepo
echo "[SCRIPT INFO] Attempting to create the docker image..."
docker build -t $IMAGE .
###############################################################################
# Desplegar un contenedor con la API
###############################################################################
echo -e "\n[SCRIPT INFO] Running the docker image"
docker run -it -p 127.0.0.1:8080:8080 $IMAGE
###############################################################################
# Obtener el contenedor de la imagen una vez terminado
###############################################################################
echo -e "\n[SCRIPT INFO] Cleaning up the environment"
CONTAINER=$(docker ps -a | grep -e $IMAGE | cut -d ' ' -f 1)
###############################################################################
# Limpiar restos
###############################################################################
echo "--> Cleaning up the created container '$CONTAINER'"
docker rm $CONTAINER
echo "--> Cleaning up the created image '$IMAGE'"
docker rmi $IMAGE
echo "[SCRIPT DONE] Setup process completed successfully."
