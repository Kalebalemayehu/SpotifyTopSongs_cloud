import requests
import webbrowser
from urllib.parse import urlencode

def my_top_songs(access_token, term):
    endpoint = f"https://api.spotify.com/v1/me/top/tracks?time_range={term}&limit=20"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(endpoint, headers=headers)
    
    if response.status_code == 200:
        json_result = response.json()["items"]
        result = {}
        for item in json_result:
            artist = item['album']['artists'][0]['name']
            song = item['name']
            result[song] = artist
        return result
    else:
        print("Error fetching top songs:", response.content)
        return None

def get_token(client_id, client_secret, code):
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:5000/"
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

# Spotify API credentials
client_id = "a46764aa00b1466186824d3dbb6d62a7"
client_secret = "2daad7947d4b464fa92bb93e52dac7ed"

# Authorization URL
auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://127.0.0.1:5000/",
    "scope": "user-top-read"
}
auth_url = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)

# Open the authorization URL in a browser tab
webbrowser.open(auth_url)

# Retrieve the authorization code manually
authorization_code = input("Enter the Authorization Code from the browser: ")

# Get access token using the authorization code
access_token = get_token(client_id, client_secret, authorization_code)
print(access_token)

periods = ["short_term", "medium_term", "long_term"]
for period in periods:
    top_songs_data = my_top_songs(access_token, period)
    print(top_songs_data)

