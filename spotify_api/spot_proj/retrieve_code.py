import webbrowser
import time
from urllib.parse import urlencode
import os


def get_authentication_code(client_id):
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://127.0.0.1:5001",  # Use the correct port here
        "scope": "user-top-read"
    }

    auth_url = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)

    webbrowser.open(auth_url)

    while authorization_code is None:
        time.sleep(1)  # Wait for the authorization code to be captured

    return authorization_code

if __name__ == '__main__':
    client_id = "a6d8a494423946cbb0d531eed91606b1"
    code = get_authentication_code(client_id)
    print(f"Authentication code: {code}")
