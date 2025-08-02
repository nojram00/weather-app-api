from mongoengine import *
from dotenv import load_dotenv
import os

load_dotenv()

def init_db():
    connect(host=os.getenv("MONGO_URI"), alias="default", db="pagasa-weather-forecast")