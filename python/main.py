import requests
from pprint import pprint
from modules.save_data import SaveData
from modules.model import Model

import os

from dotenv import load_dotenv
load_dotenv()

def GetData() -> list:
    data_request = requests.get("http://localhost:8080/run")
    return data_request.json()

if __name__ == "__main__":
    data = GetData()
    save_data = SaveData(data)
    model = Model()
    model.create_model()
    model.use_model()
    
