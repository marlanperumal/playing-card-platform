import os
from dotenv import load_dotenv
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    DB_TYPE = os.getenv("DB_TYPE")
    if DB_TYPE:
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_DATABASE = os.getenv("DB_DATABASE")
        if DB_TYPE == "postgresql":
            DB_CONN_TYPE = "postgresql"
        elif DB_TYPE == "mysql":
            DB_CONN_TYPE = "mysql+pymysql"
        SQLALCHEMY_DATABASE_URI = (
            f"{DB_CONN_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

    logging.info("Connecting to", SQLALCHEMY_DATABASE_URI)

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
