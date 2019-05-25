# Oauth2 library for python flask and restplus

## Requirements

```text
cryptography
PyJWT>=1.7.1
Flask
```

## 1. Bootstrap flask app and restplus api

### myapp.py

```python
import os
from flask import Flask
from flask_restplus import Api, Resource

api = Api()
app = Flask(__name__)
app.secret_key = os.urandom(32)
api.init_app(app)
```

## 2. Configure your identity server and RBAC

### config.py

```python
oauth_config = {
    'well_known_url': '{well_known_url}',
    'client_id': '{client_id}',
    'redirect_uri': 'http://127.0.0.1:5000/signin-oidc',
    'audience': '{audience}',
    'scopes': '{coma separeted scopes}',
    'whitelist': ['/openbar?']
}
```

*whitelist field declares your open application endpoints

### security/rbac.py

```python
def rbac(client, operation):
    print('client ', client, ' is asking for operation ', operation)
    return True
```

*return True to allow access and False to refuse.

### security/auth.py

```python
from myapp import app
from simple_oauth2 import OAuth
from .rbac import rbac
from config import oauth_config

oauth = OAuth(app, oauth_config, rbac=rbac)

```

## 3. Use OAuth

### main.py

```python
from flask_restplus import Resource
from myapp import app, api
from security.auth import oauth


# flask
# AuthN without AuthZ
@app.route('/')
def slah():
    return 'Hello'

# AuthN & AuthZ
@app.route('/hello')
@oauth.authorize('get_greetings')
def hello():
    return 'hi'

# No AuthN nor AuthZ
@app.route('/openbar')
def openbar():
    return 'Chimay'


# restplus

@api.route('/toto')
class Toto(Resource):
    @oauth.authorize('get_toto')
    def get(self):
        return {'hello': 'world'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


```

## Contributors

Register [here](https://test.pypi.org/account/register/ )

Install required packages

```bash
python -m pip install --user --upgrade setuptools wheel
python -m pip install --user --upgrade twine
```

Package like this:

```bash
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Test install

```bash
pip install -i https://test.pypi.org/simple/ simple-oauth2
```