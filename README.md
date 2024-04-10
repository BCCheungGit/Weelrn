# Weelrn

## Set-up
1. Clone the repository locally.
2. Set up python virtual environment
3. Install packages from requirements.txt after activating the env.
```
pip install -r requirements.txt
```
4. Run the program

Note that all code should work as intended for the live version, as long as you change the API keys, currently they are set up for the production environment. I have other keys for the live version [https://weelrntest.discourse.group/](https://weelrntest.discourse.group/). If you would like to set up a production environment as well (highly recommended), please contact me or try following the steps below.

Username key is the same, but change PROD to the normal versions, found in the env. I only pushed the env file because the repository is private, later if it goes public I will add ```.env``` to the ```.gitignore.```

---
## Set-up Production Environment using Docker and Ubuntu/Linux based system
First, install Docker and Ubuntu (Either through WSL or through another method).


In Ubuntu, install docker using the following linux commands.
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
```

Next, clone the discourse repository to your environment.
```
git clone https://github.com/discourse/discourse.git
cd discourse
```

Once in the repository, boot up docker.
```
d/boot_dev --init
```

In one terminal, start the Ruby on Rails server:
```
d/rails s
```

In a separate Ubuntu terminal, start the ember cli
```
d/ember-cli
```
You will need to create an email-password combo for the local env.

Open a browser to [http://localhost:4200](http://localhost:4200)

Note that for API calls, you will need to send the requests to [http://localhost:3000](http://localhost:3000), and you may need a new API key.
