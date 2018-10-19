from flask import Flask

from FlaskQt import init_app
from routes import register_routes

app = Flask(__name__)
app.config.from_object('flask_config')
register_routes(app)

if __name__ == '__main__':
	init_app(app)
