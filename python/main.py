import requests
from pprint import pprint
from modules.save_data import SaveData
from modules.model import Model
from modules.log import Log


def GetData() -> list:
    data_request = requests.get("http://localhost:8080/run")
    log.info = "Pulling the data"
    return data_request.json()

if __name__ == "__main__":
    log = Log()
    log.info = "Starting"
    data = GetData()
    model = Model(data, log)
    model.init()
    
