from routes.root import ns as root_blueprint


def register_routes(app):
	app.register_blueprint(root_blueprint)
