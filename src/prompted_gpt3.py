import json
import time
import random
import logging
import openai
from gpt import GPT
from gpt import Example
import firebase_admin
from firebase_admin import credentials, firestore

logger = logging.getLogger()
logger.setLevel(logging.INFO)
cred = credentials.Certificate('keys/ideahub31-firebase-adminsdk-yl59k-f6da5b2634.json') #change path to 'keys/ideahub' during deploy
firebase_admin.initialize_app(cred)
db = firestore.client()

key_path = 'keys/gpt3_keys.json'
data_path = 'data/example_data.json'
engine = ["davinci", "curie", "babbage", "ada"]
tags = ["games", "apps", "startup"]
prompt = ["Game idea", "App idea", "Startup idea"]
min_max = [(0, 3), (3, 6), (6, 9)]
prompt_index = random.randint(0, len(prompt)-1)

def firebasepush(): 
    gen_ref = db.collection("generated")
    post_ref = db.collection("posts")
    query = gen_ref.order_by("utc").limit_to_last(1)
    results = query.get()
    for obj in results:
        objdic = obj.to_dict()
        logger.info(f'objdic: {objdic}\n\n')
        logger.info(f'objdic["utc"]: {objdic["utc"]}\n\n')
        objdic["utc"] = int(time.time())*1000
        logger.info(f'updated objdic["utc"]: {objdic["utc"]}\n\n')
        post_ref.add(objdic)
        obj.reference.delete()
    return {
        'statusCode': 200,
        'body': 'success bish'
    }

def handler(event, context): 
    try:
        logger.info(f'started handler\n\n')
        with open(key_path) as f:
            data = json.load(f)
        openai.api_key = data["api_key"]

        gpt = GPT(engine=engine[event["engine_index"]], temperature=event["temp"], max_tokens=event["max_tok"])

        with open(data_path) as f:
            prompt_data = json.load(f)
        #print(prompt_data[:5])

        for item in prompt_data[min_max[prompt_index][0]:min_max[prompt_index][1]]: #change slice depending on prompt
            gpt.add_example(Example(item["inp"], item["out"]))

        output = gpt.submit_request(prompt[prompt_index])
        logger.info(f'output.choices[0].text: {output.choices[0].text}\n\n')
        split_string = output.choices[0].text.split(' ')  
        if split_string[0] == 'output:':
            new_string_list = split_string[1:] 
        else:
            new_string_list = split_string
        updated_output_text = ' '.join(new_string_list) 
        logger.info(f'updated_output_text: {updated_output_text}\n\n')
        #print(updated_output_text)

        db.collection('posts').add({
            'displayName': 'GPT3-Bot', 
            'uid': '5aCGwn68JWUpOv3QSwduabVqqG62', #d7c3d2e59b835bf1ad098ceb7e5d2123 for gpt3 and 5aCGwn68JWUpOv3QSwduabVqqG62 for sil
            'idea': updated_output_text, 
            'tag': tags[prompt_index], 
            'upvotes': 0, 
            'utc': int(time.time())*1000
        })
        return {
            'statusCode': 200,
            'body': 'success bish'
        }
    except Exception as e: 
        logger.error(f'logging f max: {e}\n\n')
        return {
            'statusCode': 400,
            'body': 'f max'
        }
 
if __name__ == "__main__":
    handler({"engine_index": 0, "temp": 0.8, "max_tok": 128}, None)