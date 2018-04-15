![fiubar](fiubar/static/images/fiubar-logo.png)

Administrador de materias para FIUBA.

De manera simple y ordenada, podés organizar tu carrera y decidir qué materias cursar.

# Para acceder a fiubar: http://fiubar.tk/

:sparkles: ¡Participá! :sparkles:
---------------------------------

Tenemos una lista de discusión:
:computer: http://groups.google.com/d/forum/fiubar-dev

:bug: ¿*Encontraste un error*? Por favor incluí la mayor cantidad de información
posible, como el link de la página y los pasos que hay que seguir para
reproducir el error.

También podés reportar errores usando la plataforma de github: https://github.com/maru/fiubar/issues

:bulb: ¿Se te ocurrió una *excelente idea* para Fiubar? ¡Contanos!

:woman_technologist: Se aceptan *contribuciones de código*: https://github.com/maru/fiubar/pulls

:tired_face: ¿Tenés ganas de participar y no sabés por dónde empezar?
  - Usamos Django (python): https://tutorial.djangogirls.org/es/
  - Probá de bajar el código de fiubar e instalarlo en tu computadora.
  - Si tenés una duda, ¡podés escribirnos a la lista!

Instalación
-----------

    git clone https://github.com/maru/fiubar.git
    cd fiubar/

Podés personalizar ciertos valores de configuración en el siguiente archivo:

    export FIUBAR_SECRET_FILE=local/secret.json

Si usás [docker](https://docs.docker.com/get-started/), creá la imagen y corré el contenedor:

    docker build -t fiubar .
    docker run -it -p 8000:8000 --rm --name fiubar-local fiubar

El servidor se ejecutará automáticamente, y pedirá de crear una cuenta administrador:

    ```bash
    Crear un usuario administrador
    Username: admin
    Email address: admin@example.com
    Password: ****
    Password (again): ****
    Superuser created successfully.
    Performing system checks...

    System check identified no issues (0 silenced).
    April 15, 2018 - 15:20:51
    Django version 2.0.4, using settings 'fiubar.config.settings.local'
    Starting development server at http://0.0.0.0:8000/
    Quit the server with CONTROL-C.
    ```


... y abrí el navegador en http://127.0.0.1:8000/ :smile:


Desarrollar
-----------

Recomendamos crear un [entorno virtual](https://tutorial.djangogirls.org/es/django_installation/#entorno-virtual):

    python3 -m venv fiubarenv
    source fiubarenv/bin/activate

Resultado, terminal con prefijo:

    (fiubarenv) $

Instalar los paquetes necesarios:

    pip install --upgrade pip
    pip install -r requirements_dev.txt

Ejecutar servidor:

    ./local/start.sh


Testing
-------

Es necesario instalar los siguientes programas:

- Firefox:

    Si no tenés Firefox instalado, podés bajarlo de https://www.mozilla.org/firefox/.
    En Linux, podés instalarlo con tu gestor de paquetes.

- geckodriver:

    Bajar la última versión de [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)

    Necesitás extraerla y ponerla en tu PATH (por ejemplo, en /usr/local/bin).

    Para verificar que funciona correctamente, ejecutá en una terminal:

      $ geckodriver --version
      geckodriver 0.20.0

      The source code of this program is available from
      testing/geckodriver in https://hg.mozilla.org/mozilla-central.

      This program is subject to the terms of the Mozilla Public License 2.0.
      You can obtain a copy of the license at https://mozilla.org/MPL/2.0/.

Setear las siguientes variables de entorno en la terminal, por ejemplo:

    export TEST_FIREFOX_PATH=/usr/bin/firefox
    export TEST_SERVER_NAME=http://localhost:8000/

Para ejecutar los tests, podés correr el comando `tox` o ejecutarlos manualmente.

Para hacerlo manualmente, es necesario instalar los paquetes necesarios:

    pip install -r tests/requirements.txt
    python manage.py test --settings=fiubar.config.settings.test
