import os
from langchain.chat_models import init_chat_model

class Model():
    os.environ["OPENAI_API_KEY"] = str(os.getenv("OPENAI_KEY"))
    def __init__(self):
        self.model_name = os.getenv("model_name")
        self.model = any

    def create_model(self):
        self.model = init_chat_model(
            self.model_name,
            temperature=0.7,
            timeout=30,
            max_tokens=1000,
        )
    def use_model(self):
        response = self.model.invoke("How much is 5 + 2?")
        print(response)