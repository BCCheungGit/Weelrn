# Weelrn

A series of Python Scripts for Weelrn, to run automated learning cycles on the discussion platform [Discourse](https://www.discourse.org)

---
Docker Image for Discourse

The image for Discourse that was created for Weelrn can be found at this dockerhub link: [DockerHub](https://hub.docker.com/repository/docker/cheungben/weelrn_discourse/general)

---
## Set-up Production Environment using Docker and Ubuntu/Linux based system
1. First, install Docker and Ubuntu (Either through WSL or through another method).


2. In Ubuntu, install docker using the following linux commands.
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
```

3. Next, clone the discourse repository to your environment.
```
git clone https://github.com/discourse/discourse.git
cd discourse
```

4. Once in the repository, boot up docker.
```
d/boot_dev --init
```

5. In one terminal, start the Ruby on Rails server:
```
d/rails s
```

6. In a separate Ubuntu terminal, start the ember cli
```
d/ember-cli
```
You will need to create an email-password combo for the local env.

Open a browser to [http://localhost:4200](http://localhost:4200)

Note that for API calls, you will need to send the requests to [http://localhost:3000](http://localhost:3000), and you will need to add api keys.
```
DISCOURSE_USERNAME = "username created at first start-up"
DISCOURSE_HOST = "http://localhost:3000"
DISCOURSE_KEY = "Go to API and create a new key"
```

Once these steps are complete, you will be able to run the Python Scripts in this repository.

For future use, you will need to start the docker container, then open two Ubuntu terminals and run the commands in steps 5 and 6 again.

## Running Scripts
1. Before running scripts, please set up the local environment following the above steps.
2. Clone the repository locally.
3. Set up python virtual environment
Example for Windows / Git Bash (What I use):
``` 
pythom -m venv venv
source venv/Scripts/Activate
```
4. Install packages from requirements.txt after activating the env.
```
pip install -r requirements.txt
```
5. Run the program
```
flask run
```

## Tech Stack:
- Flask
- Natural Language Toolkit
- Docker
- Discourse API, Google Sheets API
- Pandas/Numpy

## TODO:
- [x] Dockerize Main Application
- [x] Run Learning Cycle successfully
- [x] Sentiment Analysis (NLTK)
- [x] Flask Frontend
- [ ] Documentation