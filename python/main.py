import requests
from pprint import pprint
from modules.save_data import SaveData
from modules.model import Model
from modules.log import Log
from modules.conn import conn


def GetData() -> list:
    data_request = requests.get("http://localhost:8081/run")
    log.info = "Pulling the data"
    return data_request.json()

if __name__ == "__main__":
    log = Log()
    log.info = "Starting"
    db_conn = conn(log)
    data = GetData()
    model = Model(data, log, db_conn.cursor())
    model.init()
    # log.info = "Ending"
    db_conn.close()
    
