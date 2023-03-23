# brainFart
## General
* Secrets and keys stored as environment variables 
* `prompted_gpt3.py` runs first.

## Run the following to Deploy
* Login first with 
    * `aws ecr get-login-password | docker login --username AWS --password-stdin 832214191436.dkr.ecr.ap-south-1.amazonaws.com`
* One time 
    * `aws ecr create-repository --repository-name brainfart`
* Build docker image with 
    * `docker build -t brainfart .`
* `docker tag brainfart:latest 832214191436.dkr.ecr.ap-south-1.amazonaws.com/brainfart:latest`
* `docker push 832214191436.dkr.ecr.ap-south-1.amazonaws.com/brainfart:latest`