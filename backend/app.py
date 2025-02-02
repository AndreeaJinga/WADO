from flask import Flask
import psycopg2
from psycopg2 import sql
import os
from dotenv import dotenv_values, load_dotenv
# Import Blueprints
from apis.auth_api import auth_blueprint
from apis.ontology_api import ontology_blueprint
from services.ontology_service import OntologyService
from services.user_service import UserService
from services.email_service import EmailService
from flask_cors import CORS


config = dotenv_values(".env")

def create_database():
    """Create the PostgreSQL database and user table if it does not exist."""
    conn = psycopg2.connect(
        dbname=config.get("POSTGRES_DB"),
        user=config.get("POSTGRES_USER"),
        password=config.get("POSTGRES_PASSWORD"),
        host=config.get("POSTGRES_HOST"),
        port=config.get("POSTGRES_PORT")
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def create_app():
    global config
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.get('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = config.get('JWT_SECRET_KEY')
    app.config['BASE_URL'] = config.get('BASE_URL')
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['DATABASE'] = {
        "dbname": config.get("POSTGRES_DB"),
        "user": config.get("POSTGRES_USER"),
        "password": config.get("POSTGRES_PASSWORD"),
        "host": config.get("POSTGRES_HOST"),
        "port": config.get("POSTGRES_PORT")
    }

    create_database()

    app.config['USER_SERVICE'] = UserService(app.config['DATABASE'])
    app.config['ONTOLOGY_SERVICE'] = OntologyService(config.get('ontology_path'))
    
    smtp_server = config.get('SMTP_SERVER')
    smtp_port = config.get('SMTP_PORT')
    smtp_user = config.get('SMTP_USER')
    smtp_pass = config.get('SMTP_PASS')
    app.config['EMAIL_SERVICE'] = EmailService(smtp_server, smtp_port, smtp_user, smtp_pass)

    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(ontology_blueprint, url_prefix='/api/ontology')

    return app


if __name__ == "__main__":
    flask_app = create_app()
    # Run in debug for development; remove debug=True in production
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
