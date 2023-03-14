import requests

import credentials


def get_token():
    """Use credentials to fetch auth token from reddit API"""
    CLIENT_ID = credentials.API.get("CLIENT_ID")
    SECRET_KEY = credentials.API.get("SECRET_KEY")
    USERNAME = credentials.USER.get("USERNAME")
    PASSWORD = credentials.USER.get("PASSWORD")

    # HTTP headers
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    headers = {"User-Agent": "ProductsFromReddit/0.0.1"}
    data = {
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD,
    }

    # Send request for auth token
    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )

    if res.ok:
        TOKEN = res.json()["access_token"]
        return TOKEN

    else:
        return None
