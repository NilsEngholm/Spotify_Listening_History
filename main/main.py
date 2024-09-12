import requests
import yaml
import json
import base64
import os
import webbrowser
import pandas as pd
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timedelta

# load tokens
with open('main\\token_container\\secret.yaml', 'r') as file:
    token = yaml.safe_load(file)

clientID = token['clientID']
clientSecret = token['clientSecret']
redirectUri = "https://open.spotify.com"

# endpoint urls
baseUrl = 'https://api.spotify.com/v1'
authUrl = "https://accounts.spotify.com/authorize"
tokenUrl = "https://accounts.spotify.com/api/token"

def getAuthorization():
    # define request parameters | tokens, scopes, etc
    params = {
        "client_id": clientID,
        "response_type": "code",
        "redirect_uri": redirectUri,
        "scope": "user-read-recently-played",
        "show_dialog": True
    }

    #format request url then open in browser
    authUrlWithParams = f"{authUrl}?{urlencode(params)}"
    webbrowser.open(authUrlWithParams)

    # you just have to copy paste the url it sent you to into the console
    print("Paste the URL you were redirected to after login:")
    redirectResponse = input()

    # confirm that the authorization was successful
    try:
        urlParts = urlparse(redirectResponse)
        queryDict = parse_qs(urlParts.query)
        code = queryDict.get('code')
        if not code:
            raise ValueError("Authorization code not found in the URL.")
        return code[0]
    except Exception as e:
        print(f"Error parsing authorization code: {e}")
        return None

def getToken(code):
    authString = f"{clientID}:{clientSecret}"
    authBytes = authString.encode('utf-8')
    authBase64 = base64.b64encode(authBytes).decode('utf-8')

    headers = {
        "Authorization": "Basic " + authBase64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirectUri
    }
    
    response = requests.post(tokenUrl, headers=headers, data=data)
    
    if response.status_code != 200:
        print(f"Failed to get token: {response.status_code} {response.text}")
        return None, None
    
    token_info = response.json()
    return token_info['access_token'], token_info.get('refresh_token')

def getRecentlyPlayed(token):
    url = f"{baseUrl}/me/player/recently-played?limit=50"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to get recently played: {response.status_code} {response.text}")
        return None

    try:
        return response.json()
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        return None

# Execute authorization and fetch songs
authCode = getAuthorization()
if authCode:
    accessToken, refresh_token = getToken(authCode)
    if accessToken:
        recentlyPlayed = getRecentlyPlayed(accessToken)
        if recentlyPlayed:
            print(json.dumps(recentlyPlayed, indent=2))

            timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H.%M')
            data = recentlyPlayed['items']

            with open(os.path.join('main', 'data', 'test.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
