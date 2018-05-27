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

Ejecutar el servidor:

    ./local/start.sh

### React

Para desarrollar con React, instalamos los packages necesarios con
[npm](https://nodejs.org/es/download/package-manager/):

    npm install

Después de cambios en el código javascript (ver
[fiubar/frontend/src/](https://github.com/maru/fiubar/tree/master/fiubar/frontend/src/)),
utilizamos webpack para crear el archivo final ```fiubar/static/js/main.js```:

    npm run build


Testing
-------

Para ejecutar los tests, podés correr el comando `tox` o ejecutarlos manualmente.

Para hacerlo manualmente, es necesario instalar los paquetes necesarios:

    pip install -r tests/requirements.txt
    python manage.py test --settings=fiubar.config.settings.test
