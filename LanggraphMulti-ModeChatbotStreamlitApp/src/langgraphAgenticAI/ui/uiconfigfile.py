from configparser import ConfigParser

class Config:
    def __init__(self, config_file="./src/langgraphAgenticAI/ui/uiconfigfile.ini"):
        self.config=ConfigParser()
        self.config.read(config_file)
    def get_llm_options(self):
        if type(self.config["DEFAULT"].get("LLM_OPTIONS"))==None:
            return self.config["DEFAULT"].get("LLM_OPTIONS")
        else:
            return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    def get_usecase_options(self):
        if type(self.config["DEFAULT"].get("USECASE_OPTIONS"))==None:
            return self.config["DEFAULT"].get("USECASE_OPTIONS")
        else:
            return self.config["DEFAULT"].get("USECASE_OPTIONS").split(", ") 
        
    def get_groqmodel_options(self):
        if type(self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS"))==None:
            return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS")
        else:
            return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")  
        
    def get_pagetitle_option(self):
        if type(self.config["DEFAULT"].get("PAGE_TITLE"))==None:
            return self.config["DEFAULT"].get("PAGE_TITLE")
        else:
            return self.config["DEFAULT"].get("PAGE_TITLE").split(", ")   
        
        