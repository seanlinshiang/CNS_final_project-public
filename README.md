# Enviroment
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```
Then, create a .env file containing below:
```
GEMINI_API_KEY=<Gemini_api_key>
CHATGPT_API_KEY=<ChatGPT_api_key>
```

# Files
## llm_utils.py
class LLM for llm api and get_response.

## generate_dataset.py
For generating datasets from the folder "base_datasets". The datasets will be in the folder "datasets".
`$ python3 generate_dataset.py`

## generate_response.py
For generating responses, the responses will be saved in "responses".
`$ python3 generate_response.py -m <model_name> -d <dataset_path>`

## auto_testing.py
For the whole automatic testing process. The response and evaluation results will be saved in "automated_responses".
`$ python3 auto_teseting.py -m <model_name> -b <base_dataset_path>`

# Available models
As of now, only "gemini-1.5-flash-latest" is available.