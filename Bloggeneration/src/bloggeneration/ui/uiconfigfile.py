from configparser import ConfigParser

class Config:
    def __init__(self, config_file="./src/bloggeneration/ui/uiconfigfile.ini"):
        self.config=ConfigParser()
        self.config.optionxform = str # to automatically converts all the config inputs to uppercase
        self.config.read(config_file)
 
    def get_categories(self):
        """
        Return a list of all top-level categories
        """
        if "Categories" not in self.config:
            return []
        return list(self.config["Categories"].keys())

    def get_subcategories(self, category: str):
        """
        Return a list of subcategories for the given category
        """
        if "Categories" not in self.config:
            return []
        if category not in self.config["Categories"]:
            return []
        value = self.config["Categories"][category].strip()
        if not value:
            return []
        # Split comma-separated subcategories
        return [x.strip() for x in value.split(",")]
    
    def get_blog_topic(self):
        if type(self.config["DEFAULT"].get("BLOG_TOPIC"))==None:
            return self.config["DEFAULT"].get("BLOG_TOPIC")
        else:
            return self.config["DEFAULT"].get("BLOG_TOPIC").split(", ")  
    
    def get_llm_option(self):
        if type(self.config["DEFAULT"].get("LLM_OPTIONS"))==None:
            return self.config["DEFAULT"].get("LLM_OPTIONS")
        else:
            return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")    
        
    def get_groqmodel_option(self):
        if type(self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS"))==None:
            return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS")
        else:
            return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")  