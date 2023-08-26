from flask import *
import json
import requests
import base64
import webbrowser
from urllib.parse import urlencode


def get_token(client_id, client_secret, code):
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:5000/users"
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data=token_data,
        headers=token_headers,
        auth=(client_id, client_secret)
    )

    if response.status_code == 200:
        data = response.json()
        return data['access_token']
    else:
        print("Token response content:", response.content)
        print("Token response status code:", response.status_code)
        return None


def my_profile(access_token):
    endpoint = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer " + access_token}

    response = requests.get(endpoint, headers=headers)
    json_result = response.json()

    name = json_result['display_name']
    link = json_result['external_urls']["spotify"]
    profile_picture_url = json_result['images'][1]['url']

    result = {
        "Name": name,
        "Profile": link,
        "ProfilePicture": profile_picture_url
    }

    return result

def my_top_songs(access_token, term):
    endpoint = f"https://api.spotify.com/v1/me/top/tracks?time_range={term}&limit=20"
    headers = {"Authorization": "Bearer " + access_token}

    response = requests.get(endpoint, headers=headers)
    json_result = response.json()["items"]

    result = {}
    for item in json_result:
        artist = item['album']['artists'][0]['name']
        song = item['name']
        result[song] = artist

    return result
app = Flask(__name__)
app.secret_key = "kalebssession"  # Set a secret key for session management

cid = "a46764aa00b1466186824d3dbb6d62a7"
secret = "2daad7947d4b464fa92bb93e52dac7ed"

authorization_code = None

@app.route('/')
def login():
    if 'my_token' in session:
        return redirect('/users')
    else:
        auth_headers = {
            "client_id": cid,
            "response_type": "code",
            "redirect_uri": "http://127.0.0.1:5000/users",
            "scope": "user-top-read"
        }
        auth_url = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)
        return redirect(auth_url)
    
@app.route('/users')
def redirect_page():
    authorization_code = request.args.get('code')
    #session['authorization_code'] = authorization_code 
    my_token = get_token(cid, secret, authorization_code)
    if my_token is None:
        auth_headers = {
            "client_id": cid,
            "response_type": "code",
            "redirect_uri": "http://127.0.0.1:5000/users",
            "scope": "user-top-read"
        }
        auth_url = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)
        return redirect(auth_url)
        authorization_code = request.args.get('code')
    
    session['my_token'] = my_token
    my_profile_result = my_profile(my_token)
    image = my_profile_result['ProfilePicture']
    name = my_profile_result['Name']

    return render_template('main.html', profile_picture=image, display_name=name)

@app.route('/users/get_top_songs/<time_range>')
def get_top_songs(time_range):
    my_token2 = session.get('my_token')
    user_music = {}  
    periods = ["short_term", "medium_term", "long_term"]
    for period in periods:
        top_songs_data = my_top_songs(my_token2, period)
        user_music[period] = top_songs_data

    if time_range in user_music:
        return jsonify(user_music[time_range])
    else:
        return jsonify({})
    




if __name__ == '__main__':
    app.run(debug=True)
