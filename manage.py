from flask.cli import FlaskGroup
from app import create_app
from config import config

configuracion = config['development']  # Acceder a la configuración "development"
app = create_app(configuracion)
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
