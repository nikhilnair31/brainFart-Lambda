import os
import json
import time
import random
import logging
import openai
import firebase_admin
from firebase_admin import credentials, firestore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

gpt3_api_key = os.environ.get("GPT3_API_KEY")

my_credentials = {
    "type": "service_account",
    "project_id": "ideahub31",
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY").replace(r'\n', '\n'),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL")
}
cred = credentials.Certificate(my_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

data_path = 'data/example_data.json'
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

        with open(data_path) as f:
            prompt_data = json.load(f)
        openai.api_key = gpt3_api_key

        messages=[
            {
                "role": "system", 
                "content": prompt_data[prompt_index]["system"]
            }
        ]
        response = openai.ChatCompletion.create(
            model=event["engine_name"],
            max_tokens=event["max_tok"],
            temperature=event["temp"],
            messages = messages
        )
        updated_output_text = response["choices"][0]["message"]["content"]
        logger.info(f'updated_output_text: {updated_output_text}\n\n')

        db.collection('posts').add({
            'displayName': 'GPT4-Bot', 
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