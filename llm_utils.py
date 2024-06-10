import google.generativeai as genai
from dotenv import dotenv_values
import time

class LLM:
    def __init__(self, model, temperature=0.9, max_tries=10):
        self.dotenv_configs = dotenv_values('.env')

        available_models = {"gemini-1.5-flash-latest", }
        if model not in available_models:
            raise ValueError(
                f"{model}: model not available!!\nAvailable models: {available_models}"
            )
        
        self.model = model
        self.temperature = temperature
        self.max_tries = max_tries
        # choose which api to use
        self.api = self.choose_api()
        

    def choose_api(self):
        if 'gemini' in self.model:
            gemini_key = self.dotenv_configs['GEMINI_API_KEY']
            genai.configure(api_key=gemini_key)
            generation_config = genai.types.GenerationConfig(
                temperature=self.temperature
            )
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
            api = genai.GenerativeModel(
                self.model, 
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            return api
        
        
    def get_response(self, text):
        if 'gemini' in self.model:
            for _ in range(self.max_tries):
                response = self.api.generate_content(text)
                try:
                    return response.text
                except ValueError as e:
                    print(response)
                    print(e, 'Not valid response')
                    time.sleep(1.0)
            raise ValueError('API not working')
        
def main():
    llm = LLM('gemini-1.5-flash-latest')
    response = llm.get_response('Hi')
    print(response)

if __name__ == '__main__':
    main()