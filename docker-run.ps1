###############################################################################
# Author:
#   Devid Dokash
# Description:
#   A Powershell script that prepares a Docker environment and starts the API.
###############################################################################

# Verificar que el script está en la misma carpeta que la aplicación
$SERVER_NAME = "app"
if (-not (Test-Path -Path $SERVER_NAME -ItemType Directory)) {
    Write-Host "[SCRIPT ERROR] Please run or move this script to the root directory containing the '$SERVER_NAME' folder."
    exit 1
}

###############################################################################
# Verificar que el fichero de dependencias existe
###############################################################################
if (-not (Test-Path -Path "$SERVER_NAME\requirements.txt" -ItemType File)) {
    Write-Host "[SCRIPT ERROR] No 'requirements.txt' file? Please re-download the source code."
    exit 1
}

###############################################################################
# Verificar que el fichero de Dockerfile existe
###############################################################################
if (-not (Test-Path -Path "Dockerfile" -ItemType File)) {
    Write-Host "[SCRIPT ERROR] No 'Dockerfile'? Please re-download the source code."
    exit 1
}

###############################################################################
# Construir la imagen
###############################################################################
$IMAGE = "roams-test-monorepo"
Write-Host "[SCRIPT INFO] Attempting to create the docker image..."
docker build -t $IMAGE .

###############################################################################
# Desplegar un contenedor con la API
###############################################################################
Write-Host "`n[SCRIPT INFO] Running the docker image"
docker run -it -p 127.0.0.1:8080:8080 $IMAGE

###############################################################################
# Obtener el contenedor de la imagen una vez terminado
###############################################################################
Write-Host "`n[SCRIPT INFO] Cleaning up the environment"
$CONTAINER = docker ps -a | Select-String -Pattern $IMAGE | ForEach-Object { ($_ -split '\s+')[0] }

###############################################################################
# Limpiar restos
###############################################################################
Write-Host "--> Cleaning up the created container '$CONTAINER'"
docker rm $CONTAINER

Write-Host "--> Cleaning up the created image '$IMAGE'"
docker rmi $IMAGE

Write-Host "[SCRIPT DONE] Setup process completed successfully."
