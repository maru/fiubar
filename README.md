fiubar
======

Administrador de materias para FIUBA.

De manera simple y ordenada, podés organizar tu carrera y decidir qué materias cursar.

# Para acceder a fiubar: http://fiubar.tk/

Participá:

https://fiubar.slack.com/messages/general/

https://groups.google.com/forum/#!forum/fiubar-dev

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
    docker-compose run --rm django python manage.py loaddata fixtures/fiubar.json
    docker-compose run --rm django python manage.py createsuperuser

Ejecutar el servidor web provisto por Django:

    docker-compose up -d

... y abrir el navegador en http://127.0.0.1:8000/ :)

Testing
=======

Para correr los tests, utilizamos las siguientes versiones de selenium y del
navegador Firefox:

  pip install selenium==2.53.6

  wget 'https://ftp.mozilla.org/pub/firefox/releases/44.0/linux-x86_64/en-GB/firefox-44.0.tar.bz2'
  tar jxf firefox-44.0.tar.bz2

Instalar Firefox y setear las siguientes variables de entorno en la terminal,
por ejemplo:

  export TEST_FIREFOX_PATH=/usr/local/bin/firefox-44.0/firefox
  export TEST_SERVER_NAME=http://localhost:8000/

Ejecutar los tests:

  python tests/run.py
