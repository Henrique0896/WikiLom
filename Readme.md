### Developed by:
Henrique de Lima</br>
<i>Douglas Sales </br>
Caliny</br>
Tiago Campos</br>
</i>

<strong>Many thanks to:</strong></br>
<i>Alessandro Vivas - for incentivating this study.</i>

<i>UNIVERSIDADE FEDERAL DOS VALES DO JEQUITINHONHA E MUCURI (UFVJM) - CAMPUS JK.
</br>March - 2021</i>


### References:
<a href="https://www.br.freelancer.com/community/articles/crud-operations-in-mongodb-using-python">https://www.br.freelancer.com/community/articles/crud-operations-in-mongodb-using-python </a><br />
<a href="https://zetcode.com/python/pymongo/">https://zetcode.com/python/pymongo/ </a><br />
<a href="https://docs.mongodb.com/manual/reference/">https://docs.mongodb.com/manual/reference/ </a><br />
<a href="https://flask.palletsprojects.com/en/1.1.x/">https://flask.palletsprojects.com/en/1.1.x/ </a><br />

### Configuration

First of all, you need to create a virtual environment for your project. You can achieve this by using the following command:
```shell
# Install these packages, case you don't already have it.
sudo apt-get install python3-pip
sudo pip3 install virtualenv 

# Create the Virtual Environment
virtualenv env
```

We still need to activate the virtual environment, we can do this by issuing the following command to the system.
```shell
source env/bin/activate
```

Now that the environment is ready, we can install the project required packages.
```shell
pip install -r requirements.txt
```

Now you need to install MongoDB Server in your machine. You can do this by using:
```shell
sudo apt install -y mongodb
```
Check the installation by:
```shell
sudo systemctl status mongodb
```


### Running the project
Now that we have the project properly configured, you can start the server with:
```shell
python run.py
```
</br>

<strong><h2>HAPPY CODING!</h2></strong>

