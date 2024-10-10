import os

# def load_config(app, overrides):
#     if os.path.exists(os.path.join('./App', 'custom_config.py')):
#         app.config.from_object('App.custom_config')
#     else:
#         app.config.from_object('App.default_config')
#     app.config.from_prefixed_env()
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['TEMPLATES_AUTO_RELOAD'] = True
#     app.config['PREFERRED_URL_SCHEME'] = 'https'
#     app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
#     app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
#     app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
#     app.config["JWT_COOKIE_SECURE"] = True
#     app.config["JWT_COOKIE_CSRF_PROTECT"] = False
#     app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
#     for key in overrides:
#         app.config[key] = overrides[key]

# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...