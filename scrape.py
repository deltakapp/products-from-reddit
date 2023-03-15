import pandas as pd

import post_functions.dissect_title as dissect_title
import post_functions.pre_filter as pre_filter
import post_functions.select_fields as select_fields


def scrape_posts(posts: pd.DataFrame = None):
    """Extract useful data from posts"""
    
    try:
        posts = pd.read_pickle("data/posts.pkl")
    except:
        print("Error: data/post.pk not found")
        return
    
    posts = pre_filter.pre_filter(posts)
    posts = select_fields.select_fields(posts)

    posts = dissect_title.dissect_title(posts)
    print(posts.head())
    
    
