import os
import json
import openai

input_text = 'Make a game that'
engine_name = 'curie'
key_path = 'src/keys/gpt3_keys.json'

if __name__ == '__main__':
    with open(key_path) as f:
        data = json.load(f)
    api_key = data["api_key"]

    openai.api_key = api_key
    response = openai.Completion.create(engine=engine_name, prompt=input_text, max_tokens=128)

    print(json.dumps(response))