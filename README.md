fiubar
======

Administrador de materias para FIUBA.

De manera simple y ordenada, podés organizar tu carrera y decidir qué materias cursar.

# Para acceder a fiubar: http://fiubar.tk/

Participá!
----------

Tenemos una lista de discusión:
http://groups.google.com/d/forum/fiubar-dev

¿*Encontraste un error*? Por favor incluí la mayor cantidad de información
posible, como el link de la página y los pasos que hay que seguir para
reproducir el error.

También podés reportar errores usando la plataforma de github: https://github.com/maru/fiubar/issues

¿Se te ocurrió una *excelente idea* para Fiubar? ¡Contanos!

Se aceptan *contribuciones de código*: https://github.com/maru/fiubar/pulls

¿Tenés ganas de participar y no sabés por dónde empezar?
  - Usamos Django (python): https://tutorial.djangogirls.org/es/
  - Probá de bajar el código de fiubar e instalarlo en tu computadora.
  - Si tenés una duda, ¡podés escribirnos en esta lista!

Chat:
https://fiubar.slack.com/messages/general/

Instalación
-----------

    git clone https://github.com/maru/fiubar.git
    cd fiubar/

Si usás [docker](https://docs.docker.com/get-started/), crear la imagen y ejecutar el container:

    docker build -t fiubar .
    docker run -it -p 8000:8000 --rm --name fiubar-local fiubar

... y abrir el navegador en http://127.0.0.1:8000/ :smile:

Testing
-------

Para correr los tests, primero creamos un [entorno virtual](https://tutorial.djangogirls.org/es/django_installation/#entorno-virtual):

    python3 -m venv fiubarenv
    source fiubarenv/bin/activate

Resultado, terminal con prefijo:

    (fiubarenv) $

Luego es necesario instalar los siguientes programas:

- Django, Selenium y otros requerimientos:

      pip install -r requirements.txt

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

- Firefox:

    Si no tenés Firefox instalado, podés bajarlo de https://www.mozilla.org/firefox/.
    En Linux, podés instalarlo con tu gestor de paquetes.

Setear las siguientes variables de entorno en la terminal, por ejemplo:

    export TEST_FIREFOX_PATH=/usr/bin/firefox
    export TEST_SERVER_NAME=http://localhost:8000/

Ejecutar los tests (el servidor tiene que estar corriendo :smile:):

    python tests/run.py
