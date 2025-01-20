# Roams Backend API Test
A continuación se describe los pasos a seguir para la utilización de la API implementada, esta puede ser accedida desde el navegador, ya que se ha implementado una interfaz para poder probarse.

Para la ejecución de la API, seguir los siguientes pasos:

0. Se puede obtener el link del repositorio así:

    ![alt text](image.png)

1. Clonar el repositorio:

    ```sh
    git clone https://github.com/dedetheprogrammer/roams-test-monorepo.git
    ```

2. Moverse a la carpeta roams-test-monorepo y ejecutar alguno de los scripts. **Cualquiera de las tres formas es válida** y solo se requiere de una:

    1. Si se tiene Linux o se pueden ejecutar shell scripts en Windows:

        ```sh
        chmod 0700 run.sh # Unicamente en Linux, no es necesario en Windows.
        ./run.sh
        ```

    2. Si se tiene Windows o no se pueden ejecutar shell scripts:

        ```
        run.ps1
        ```
    
    3. Si se tiene Docker instalado:

        ```sh
        docker 
        ```

3. Una vez ejecutado, la dirección definida por defecto es http://localhost:5000 o http://127.0.0.1:5000 que será accesible desde el navegador.


