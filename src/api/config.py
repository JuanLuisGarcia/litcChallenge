import os, sys
from flask import Flask
from flask_migrate import Migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

basedir = os.path.abspath(os.path.dirname(__file__))
MIGRATION_DIR = os.path.join(basedir, 'migrations')

app = Flask(__name__)
app.config['GENERATED_DIR'] = os.getenv("GENERATED_DIR", "./generated")
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(app.config['GENERATED_DIR'], 'database.db')
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATION_DIR)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/api/swagger.json'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
)

app.register_blueprint(swaggerui_blueprint)

command_line = ' '.join(sys.argv)
is_running_server = ('flask run' in command_line) or ('gunicorn' in command_line) or ('app.py' in command_line)

if is_running_server:
    with app.app_context():
        upgrade(directory=os.path.join(basedir, 'migrations'))
