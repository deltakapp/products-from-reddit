from datetime import datetime, timedelta
from os import makedirs, path

import pandas as pd
import requests

import reddit_auth

TOKEN = reddit_auth.get_token()


def fetch_posts(number: int = 3, page: str = None):
    """fetches # of posts, starting at page reference"""

    params = {"limit": number}
    if page:
        params["after"] = page

    headers = {
        "User-Agent": "ProductsFromReddit/0.0.1",
        "Authorization": f"bearer {TOKEN}",
    }
    res = requests.get(
        "https://oauth.reddit.com/r/hardwareswap/new", headers=headers, params=params
    )

    # Dump response data posts into dataframe for manipulation
    posts = pd.json_normalize(res.json()["data"]["children"])
    posts.columns = posts.columns.str.replace("data.", "", regex=True)

    next_page = res.json()["data"]["after"]

    return posts, next_page


def save_posts_to_json(posts):
    "writes posts to separate json files in data/ directory"

    if not path.exists("data"):
        makedirs("data")

    for index, row in posts.iterrows():
        post_id = row["id"]
        with open(f"data/{post_id}.json", "w") as outfile:
            outfile.write(row.to_json())


def full_crawl(start_time: datetime):
    "fetches all posts within specified duration"

    posts = pd.DataFrame()

    fetched, next_page = fetch_posts(100)
    posts = fetched

    # determine if crawling has completed entire duration
    last_index_time = datetime.utcfromtimestamp(fetched.iloc[-1]["created_utc"])
    incomplete = last_index_time >= start_time

    while incomplete and next_page:
        # when listing is maxed out (usually close to 1000 posts) next_page = None
        # so loop will break
        fetched, next_page = fetch_posts(100, next_page)
        posts = pd.concat([posts, fetched])

        # determine if crawling has completed entire duration
        last_index_time = datetime.utcfromtimestamp(fetched.iloc[-1]["created_utc"])
        incomplete = last_index_time >= start_time

    save_posts_to_json(posts)

    return
