from flask import Flask, render_template, g, redirect, url_for, json
from flask_oidc import OpenIDConnect
from okta import UsersClient
import requests

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile","contacts"]
app.config["SECRET_KEY"] = "Secret key"
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
okta_client = UsersClient("https://dev-685287.okta.com", "00pnofetVEDO7BzxPltCb1pmASZRkxROKYD03gnESE")


@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
        #print("my id is ", + g.user.id)
    else:
        g.user = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))

@app.route("/showinfo")
def showifo():
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'SSWS00pnofetVEDO7BzxPltCb1pmASZRkxROKYD03gnESE'

    }

    response = requests.get('https://dev-685287.okta.com/api/v1/users/{0}'.format(g.user.id), headers=headers)
    print(response)
    json_data = json.loads(response.text)
    #print(json_data)
    for info in json_data:
        #print(info)
        lastName = str(json_data['profile']['lastName'])
        firstName = str(json_data['profile']['firstName'])
        City = str(json_data['profile']['city'])
        Zip_Code = str(json_data['profile']['zipCode'])
        State = str(json_data['profile']['state'])
        UK_Mobile = str(json_data['profile']['ukMob'])
        USA_Mobile = str(json_data['profile']['usaMob'])
        India_Mobile = str(json_data['profile']['mob'])
        return render_template('showinfo.html', lastName = lastName, firstName = firstName, City = City, Zip_Code = Zip_Code, State = State, UK_Mobile = UK_Mobile, USA_Mobile = USA_Mobile, India_Mobile =India_Mobile)


@app.route('/clientcred')
def clientcred():
    url = 'https://dev-685287.okta.com/oauth2/default/v1/token'
    headers = {
        'Accept': 'Application/json',
        'Authorization': 'Basic MG9hY...',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {'grant_type': 'client_credentials', 'scope': 'contacts'}

    response = requests.post(url, params=params, headers=headers, auth=('0oa12og2uwqPDhLxH357', 'j0jeeBr2n2Dh-01Qn8zCyzWR3zDxu21UEx-0-wJr'))
    print(response)
    json_data = json.loads(response.text)
    print('token_type : ' + json_data['token_type'])
    print('expires_in  : ' + str(json_data['expires_in']))
    print('access_token :' + json_data['access_token'])
    print('scope : ' + json_data['scope'])
    return "All the data are in the console"

@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))


if __name__ == '__main__':
    app.run(debug=True)