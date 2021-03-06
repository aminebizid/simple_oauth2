# Oauth2 library for python flask and restplus

With this simple library, you can authenticate clients coming from a browser (Implicit Flow) or using Bearer token (Credential flow).
You can manage authorization using rbac function as described here after.

## Requirements

Install these requirements

```text
cryptography
PyJWT==1.7.1
flask-restplus
simple-oauth2
```

## Usage example

```python
import os
from flask import Flask
from flask_restplus import Api, Resource
from simple_oauth2 import OAuth


api = Api()
app = Flask(__name__)
app.secret_key = os.urandom(32)
api.init_app(app)

oauth_config = {
    'well_known_url': '{well_known_url}',
    'client_id': '{client_id}',
    'redirect_uri': '{host:port}/signin-oidc',
    'audience': '{audience}',
    'scopes': '{space separated scopes}',
    'whitelist': ['/openbar?']
}

def rbac(client, operation):
    print('client ', client, ' is asking for operation ', operation)
    return True

oauth = OAuth(app, oauth_config, rbac=rbac)

# flask
@app.route('/')
def slah():
    return 'Hello'


@app.route('/hello')
@oauth.authorize('hello')
def hello():
    return 'hi'


@app.route('/openbar')
def openbar():
    return 'Chimay'


# restplus
@api.route('/toto')
class Toto(Resource):
    @oauth.authorize('toto')
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
