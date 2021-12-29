# GPT3 Idea_Generator

## General
* Keys folder has autheticationn json stuff for
    * Firestore service account titled `ideahub31-firebase-adminsdk-yl59k-f6da5b2634.json` 
    * GPT3 API keys titled `gpt3_keys.json`.
* `firepush.py` accepts json.dump as event then
    * Deletes all documents in collection
    * Pushes all data recieved to Firestore collection
    * returns event values with 200 status

## Run the following to Deploy
* Login first with `aws ecr get-login-password | docker login --username AWS --password-stdin 832214191436.dkr.ecr.ap-south-1.amazonaws.com`
* One time `aws ecr create-repository --repository-name brainfart`
* Build docker image with `docker build -t <container_name> .`
    * eg. `docker build -t brainfart .`
* `docker tag <repository_name>:<container_tag> 832214191436.dkr.ecr.ap-south-1.amazonaws.com/lambda-docker-fire:<container_tag>`
* `docker push 832214191436.dkr.ecr.ap-south-1.amazonaws.com/lambda-docker-fire:<container_tag>`

## Test Image Locally
* Build image first
* Run built image with `docker run -d -p 8080:8080 <container_name>`
* Test with `curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations" -d """{id:123}""" ` in command prompt