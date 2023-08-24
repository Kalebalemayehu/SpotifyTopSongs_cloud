import requests
import webbrowser
from urllib.parse import urlencode
from IPython.display import Image
import base64

class Spotify:

    def __init__(self, client_id: str, client_secret: str):
        self.cid = client_id
        self.secret = client_secret
        self.__get_oauth()
        self.__get_oauth()

    def load_code(self, code):
        self.code = code
        self.__get_token()

    ## METHODS
    def search_for_artist(self, artist_name: str) -> list:
        endpoint = "https://api.spotify.com/v1/search"
        query = f"?q={artist_name}&type=artist&limit=3"

        header = self.auth

        query_url = endpoint + query
        result = requests.get(query_url, headers=header)
        json_result = result.json()["artists"]["items"] # modify depending on what we want to show on frontend
        
        if len(json_result) == 0:
            print("No artist with this name exists.")
            return None
        else:
            names = [artist["name"] for artist in json_result]
            return ', '.join(names)
        
    def search_for_song(self, song_name):
        pass

    def my_profile(self):
        endpoint = "https://api.spotify.com/v1/me"

        header = self.auth

        query_url = endpoint

        try:
            r = requests.get(query_url, headers=header)
            json_result = r.json()

            result = {}
            
            name = json_result['display_name']
            link = json_result['external_urls']["spotify"]
            profile_picture_url = json_result['images'][1]['url']
            

            result["Name"] = name
            result["Profile"] = link
            result["ProfilePicture"] = profile_picture_url
            

            return result
        
        except requests.JSONDecodeError:
            err = self.__status_codes(r.status_code)
            return err

    
    def my_top_songs(self, term: str = "medium_term"):
        endpoint = "https://api.spotify.com/v1/me/top/tracks"
        time = f"?time_range={term}"
        limit = f"&limit=20"

        header = self.auth

        query_url = endpoint + time + limit
        
        try:
            r = requests.get(query_url, headers=header)
            json_result = r.json()["items"]

            result = {}
            for item in json_result:
                artist = item['album']['artists'][0]['name']
                song = item['name']
                result[song] = artist

            return result
        
        except requests.JSONDecodeError:
            err = self.__status_codes(r.status_code)
            return err

    def my_top_artists():
        pass
    
    ## PRIVATE SHIT
    def __status_codes(self, code: str) -> str:
        code = int(code)
        if code in [200, 201, 202, 204]:
            return code, "Accepted"
        elif code == 403:
            return code, "Forbidden request"
        elif code == 404:
            return code, "Request ot found"
        elif code in [500, 502, 503]:
            return code, "Error in the server"
        else:
            "There was an error."

    def __get_oauth(self):
            auth_headers = {
            "client_id": self.cid,
            "response_type": "code",
            "redirect_uri": "http://localhost:5000",
            "scope": "user-top-read"
            }
            
            webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))


    def __get_token(self):
        encoded_credentials = base64.b64encode(self.cid.encode() + b':' + self.secret.encode()).decode("utf-8")

        token_headers = {
            "Authorization": "Basic " + encoded_credentials,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        token_data = {
            "grant_type": "authorization_code",
            "code": self.code,
            "redirect_uri": "http://localhost:5000"
        }

        r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

        if r.status_code == 200:
            data = r.json()
            token = data['access_token']
            self.token = token
            self.auth = {"Authorization": "Bearer " + self.token}


