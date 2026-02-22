import requests
from pprint import pprint
from modules.save_data import SaveData

def GetData() -> list:
    data_request = requests.get("http://localhost:8080/run")
    return data_request.json()

if __name__ == "__main__":
    data = GetData()
    save_data = SaveData(data)
