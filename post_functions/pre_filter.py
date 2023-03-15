import pandas as pd


def pre_filter(posts: pd.DataFrame) -> pd.DataFrame:
    """Remove meta posts, which do not contain items"""

    pattern = r"\[META\]"
    filter_meta = posts["title"].str.contains(pattern)

    filtered_posts = posts[~filter_meta]  # Returns complement of filter

    return filtered_posts
