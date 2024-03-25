# Weelrn

## Set-up
1. Clone the repository locally.
2. Set up python virtual environment
3. Install packages from requirements.txt after activating the env.
```
pip install -r requirements.txt
```
4. Run the program

You may need to change environment variables, currently they are set up for the production environment. I have other keys for the live version [https://weelrntest.discourse.group/](https://weelrntest.discourse.group/)

---
## Set-up using Docker and Ubuntu/Linux based system
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
