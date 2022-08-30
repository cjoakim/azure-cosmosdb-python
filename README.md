# azure-cosmosdb-python

Example of CRUD operations vs CosmosDB with Python.

---

## Quick Start

### Provisioning CosmosDB

Provision Azure CosmosDB SQL API and/or Mongo API accounts.
Or, use your currently existing account(s).

### Environment Variables

Set the following enviornment variables which point to your CosmosDB account(s):

#### SQL API:

You can obtain these values from Azure Portal; see your CosmosDB SQL API account.

```
AZURE_COSMOSDB_SQLDB_URI
AZURE_COSMOSDB_SQLDB_KEY
```

#### Mongo API:

You can obtain these values from Azure Portal; see your CosmosDB Mongo API account.

```
TODO - complete this section
```

## Clone this Repo, create Python Virtual Environment

```
> git clone https://github.com/cjoakim/azure-cosmosdb-python.git
> cd azure-cosmosdb-python

> .\venv.ps1                # create a python virtual environment from the requirements files
> .\venv\Scripts\activate   # activate the python virtual environment

> (venv) PS ...\azure-cosmosdb-python> pip list
Package         Version
--------------- ---------
arrow           1.2.2
azure-core      1.11.0
azure-cosmos    4.2.0
build           0.8.0
certifi         2020.12.5
chardet         4.0.0
click           8.1.3
colorama        0.4.5
docopt          0.6.2
flake8          3.8.4
idna            2.10
mccabe          0.6.1
packaging       21.3
pep517          0.13.0
pip             22.2.2
pip-tools       6.8.0
pipdeptree      2.2.1
pycodestyle     2.6.0
pyflakes        2.2.0
pymongo         3.11.3
pyparsing       3.0.9
python-dateutil 2.8.2
requests        2.25.1
setuptools      58.1.0
six             1.15.0
tomli           2.0.1
urllib3         1.26.3
wheel           0.37.1
```

--- 

## Docs and Notes 

### CosmosDB with Python and SQL API

- pip install azure-cosmos
- https://pypi.org/project/azure-cosmos/
- https://github.com/Azure/azure-cosmos-python
- https://github.com/Azure/azure-cosmos-python/blob/master/samples/CollectionManagement/Program.py

### CosmosDB with Python and Mongo API

- pip install pymongo
- https://pymongo.readthedocs.io/en/stable/
- https://pymongo.readthedocs.io/en/stable/tutorial.html
- https://api.mongodb.com/python/current/api/pymongo/collection.html
