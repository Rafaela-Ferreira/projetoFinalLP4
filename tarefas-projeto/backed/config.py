import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "mysql+pymysql://root:qw12@localhost:3306/tarefas_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
