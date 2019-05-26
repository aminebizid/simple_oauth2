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
