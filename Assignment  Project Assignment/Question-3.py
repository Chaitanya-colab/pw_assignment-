# Implement OAuth2 authentication to allow users to log in using their Google or Facebook accounts.


from flask import Flask, redirect, url_for, session, request, jsonify
import requests
import json
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
discovery_url = "https://accounts.google.com/.well-known/openid-configuration"
client = WebApplicationClient(client_id)

def get_google_provider_cfg():
    return requests.get(discovery_url).json()

@app.route("/")
def index():
    if 'google_id' in session:
        return (
            f"Hello, {session['name']}! You're logged in! <br>"
            f"<a href='/logout'>Logout</a>"
        )
    else:
        return '<a href="/login">Google Login</a>'

@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(client_id, client_secret),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))


    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    userinfo = userinfo_response.json()
    if userinfo.get("email_verified"):
        session['google_id'] = userinfo["sub"]
        session['name'] = userinfo["given_name"]
        session['email'] = userinfo["email"]
    else:
        return "User email not available or not verified by Google.", 400

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
