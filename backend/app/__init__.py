from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .celery_worker import celery
from .config import Config
from .database import db
from .auth.views import auth_bp
from .user.views import user_bp
from .program.views import program_bp
from .attribute.views import attribute_bp
from .objective.views import objective_bp
from .relation.views import relation_bp
from .observation.views import observation_bp
from .module.views import module_bp
from .link.views import link_bp
from .tag.views import tag_bp
from .material.views import material_bp
from .comment.views import comment_bp
from .notification.views import notification_bp
from flasgger import Swagger

migrate = Migrate()


def create_app(config_object=Config):
    app = Flask(__name__)
    CORS(app)

    # Load app configuration
    app.config.from_object(config_object)

    # Initialize Celery
    celery.conf.update(app.config)

    # Import and register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(attribute_bp)
    app.register_blueprint(objective_bp)
    app.register_blueprint(relation_bp)
    app.register_blueprint(observation_bp)
    app.register_blueprint(module_bp)
    app.register_blueprint(link_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(notification_bp)

    # Initialize Swagger
    swagger = Swagger(app)

    # Initialize Database and Migrations
    db.init_app(app)
    migrate.init_app(app, db)

    return app
