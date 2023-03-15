from datetime import datetime
from os import makedirs, path
from typing import Optional, Tuple

import pandas as pd
import requests

import reddit_auth

TOKEN = reddit_auth.get_token()


def fetch_posts(
    post_quantity: int = 3, page: str = None
) -> Tuple[pd.DataFrame, Optional[str]]:
    """Fetches post_quantity of posts, starting at page reference.

    Args:
      number: Max number of posts to fetch from reddit API.
      page: The string ID of the page to fetch from reddit API.

    Returns: Dataframe of posts from the given page and the next_page ID if more
      posts exist on the next page.
    """

    params = {"limit": post_quantity}
    if page:
        params["after"] = page

    headers = {
        "User-Agent": "ProductsFromReddit/0.0.1",
        "Authorization": f"bearer {TOKEN}",
    }
    res = requests.get(
        "https://oauth.reddit.com/r/hardwareswap/new",
        headers=headers,
        params=params,
    )

    if not res.ok:
        raise Exception(
            f"API HTTP Error {res.status_code} Message: {res.reason}"
        )
  
    # Dump response data posts into dataframe for manipulation
    posts = pd.json_normalize(res.json()['data']['children'])
    posts.columns = posts.columns.str.replace('data.', '', regex=True)

    next_page = res.json()["data"]["after"]

    return posts, next_page


def save_posts_to_pickle(posts: pd.DataFrame):
    """Writes posts as a single dataframe in data/posts."""

    if not path.exists("data"):
        makedirs("data")

    file_name = "data/posts.pkl"

    posts.to_pickle(file_name)


def save_posts_to_json(posts: pd.DataFrame):
    """Writes posts to separate json files in data/ directory."""

    if not path.exists("data"):
        makedirs("data")

    for index, row in posts.iterrows():
        post_id = row["id"]
        with open(f"data/{post_id}.json", "w") as outfile:
            outfile.write(row.to_json())


def full_crawl(start_time: datetime):
    """Fetches all posts after specified datetime, saving posts to disk.
    Excessive posts are saved, not trimmed."""

    posts = pd.DataFrame()

    try:
        fetched, next_page = fetch_posts(100)
    except Exception as e:
        print(e)
        return
    posts = fetched

    # Determine if crawling has completed entire duration
    last_index_time = datetime.utcfromtimestamp(fetched.iloc[-1]["created_utc"])
    incomplete = last_index_time >= start_time

    while incomplete and next_page:
        # When listing is maxed out (usually close to 1000 posts),
        # next_page = None so loop will break
        fetched, next_page = fetch_posts(100, next_page)

        # Check if empty dataset has been fetched
        if fetched.empty:
            assert next_page is None, (
                f"Fetching next_page {next_page} returned an empty dataframe."
                "This is unexpected behavior and might require debugging."
            )

            break

        posts = pd.concat([posts, fetched])

        # Determine if crawling has completed entire duration
        last_index_time = datetime.utcfromtimestamp(
            fetched.iloc[-1]["created_utc"]
        )
        incomplete = last_index_time >= start_time

    save_posts_to_pickle(posts)
    save_posts_to_json(posts)

    print(f"Crawled {len(posts)} posts")

    return
