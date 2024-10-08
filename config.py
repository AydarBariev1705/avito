from dotenv import load_dotenv
import os

load_dotenv() 

SERVER_ADDRESS = os.environ.get("SERVER_ADDRESS")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT") 
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE")
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_CONN = f'postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'
