import os
from langchain.chat_models import init_chat_model
from google.oauth2 import service_account
from langchain_core.prompts import PromptTemplate
from .save_data import SaveData
import re
import ast
import json

from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = str(os.getenv("MODEL_NAME"))

CREDENTIALS = service_account.Credentials.from_service_account_file('./credentials.json')
class Model(SaveData):
    def __init__(self, data, log):
        self.model_name = os.getenv("model_name")
        self.model = any
        self.ranking_prompt, self.summary_prompt = self.define_prompt()
        self.log = log
        self.content = ""
        super().__init__(data)

    def create_model(self, occur, temperature, top_k, top_p, max_tokens):
        self.occur = "First" if occur == 1 else "Second"
        self.model = init_chat_model(
            MODEL_NAME,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            timeout=30,
            max_tokens=max_tokens,
            credentials=CREDENTIALS,
        )
        self.log.info = f"{self.occur} model created"
    def define_prompt(self):
        with open("prompts/ranking.txt", "r") as f:
            template_ranking = f.read()
        with open("prompts/summary.txt", "r") as f:
            template_summary = f.read()
        return template_ranking, template_summary
    
    def save_data(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def define_ranking(self):
        self.create_model(1, 0.2, 2, 0.5, 800)
        template_ranking = PromptTemplate.from_template(self.ranking_prompt).format(input=self.title)
        response = self.model.invoke(template_ranking)
        score_match = re.search(r'OUTPUT_SCORE\s*=\s*(\[[^\]]+\])', response.content)
        repeated_match = re.search(r'OUTPUT_REPEATED\s*=\s*(\[[^\]]+\])', response.content)

        # Converte true/false para True/False (Python)
        repeated_str = repeated_match.group(1).replace("true", "True").replace("false", "False")

        # Converte string para lista Python
        score_list = ast.literal_eval(score_match.group(1))
        repeated_list = ast.literal_eval(repeated_str)
        for i, score in enumerate(score_list):
            self.data[i]["score"] = float(score)
            self.data[i]["no_repeated"] = repeated_list[i]
        
        self.log.info = f"Ranking Defined"
        self.save_data(self.data, 'data.json')
    
    def summary_news(self):
        relevant_news = [news for news in self.data if news["no_repeated"] and news["score"] >= 0.55]
        self.save_data(relevant_news, 'relevant_news.json')
            
        self.create_model(2, 0.9, 5, 0.5, 1500)
        template_summary = PromptTemplate.from_template(self.summary_prompt).format(input=relevant_news)
        response = self.model.invoke(template_summary)
        
        self.content = response.content
        self.log.info = f"Summary Done"
        
        
            
    def init(self):
        self.define_ranking()
        self.summary_news()
        
        print(self.content)
    
        