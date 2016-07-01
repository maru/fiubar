fiubar
======

Administrador de materias para FIUBA.

De manera simple y ordenada, podés organizar tu carrera y decidir qué materias cursar.

# Para acceder a fiubar: http://fiubar.tk/


Instalación
===========

    git clone https://github.com/maru/fiubar.git

    cd fiubar/

Crear las imágenes docker

    docker-compose build

Iniciar la base de datos Postgresql

    docker-compose up -d db

Crear las tablas en la base de datos y un usuario administrador:

    docker-compose run --rm django python manage.py migrate
    docker-compose run --rm django python manage.py loaddata fiubar.json
    docker-compose run --rm django python manage.py createsuperuser

Ejecutar el servidor web provisto por Django:

    docker-compose up -d

... y abrir el navegador en http://127.0.0.1:8000/ :)
