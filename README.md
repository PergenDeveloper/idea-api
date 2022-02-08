# IDEA API

Prueba backend planteada desde la empresa

## Guía de instalación

Para realizar los siguientes pasos, debes tener instalado el **docker** y **docker-compose** en tu maquina.

El proyecto cuenta con los siguientes servicios:
- `api:` Servicio que contiene la aplicación y en él corremos la api.
- `db:` Servicio en el que se ejecuta la base de datos.
- `rabbitmq:` Servicio que corre rabbit como broker que usamos para procesar las peticiones de celery.
- `worker:` Servicio que ejecuta celery para el procesamiendo de tareas en segundo plano.
- `mailhog:` Servicio que ejecuta el gestor de mensajes SMTP para desarrollo.

NOTA: El fichero con variables entorno está subido en el repo, pero no es recomendable hacerlo en proyectos reales.


## Instalar y activar un entorno virtual
> `python3 -m venv idea-api`
>
> `source  idea-api/bin/activate`

## Clonar el proyecto
> `git clone https://github.com/PergenDeveloper/idea-api.git`
>
> `cd idea-api`

## Entorno desarrollo
### Aplicar las migraciones (el servicio de base de datos debe estar levantado)
> `docker-compose run api python manage.py migrate`

#### Levantar el proyecto
> `docker-compose up`

### Para desarrollar código
#### Instalar dependencias del proyecto
> `pip install -r requirements.txt`

#### Chequear la calidad de código antes de commit
He preparado el proyecto para que realice un chequeo de la calidad de código antes de cada commit, así nos aseguramos
que el código subido es standard.

Para activarlo ejecutamos:
> `pre-commit install`


#### Test
Los test no he podido añadirlos, pero podríamos escribirlos con pytest.

#### Notificación a usuarios
He implementado el envio de email para notificar a los usuarios sobre una nueva publicación. También
podría ser usado Firebase para este fin.
