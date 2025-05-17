from dotenv import load_dotenv
import os

load_dotenv()

print("Cargando .env desde:", os.path.abspath('.env'))
print("SECRET_KEY:", os.getenv('SECRET_KEY'))
print("DATABASE_URI:", os.getenv('DATABASE_URI'))

if not os.getenv('SECRET_KEY'):
    raise ValueError("SECRET_KEY no está definida en .env")
if not os.getenv('DATABASE_URI'):
    raise ValueError("DATABASE_URI no está definida en .env")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False