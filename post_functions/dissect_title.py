from collections import defaultdict

import pandas as pd

# A dict mapping from post flairs to transaction type categories
transaction_types = defaultdict(
    lambda: "OTHER"
)  # Default value for missing key
transaction_types.update(
    {"SELLING": "SELL", "BUYING": "BUY", "TRADING": "TRADE"}
)


def dissect_title(posts: pd.DataFrame) -> pd.DataFrame:
    """Extract keys from post titles and assign values to columns

    titles are already semi-structured as:
        [[location]] [[H]] [have] [[W]] [want]
    """

    # 'transaction_type' column translated from link flair
    posts = posts.assign(
        transaction_type=posts["link_flair_text"].map(transaction_types)
    )
    # 'have' column
    posts["have"] = posts["title"].str.extract(
        r"\[H\](.+)\[W\]", expand=False  # Regex: all chars between [H] and [W]
    )
    # 'want' column
    posts["want"] = posts["title"].str.extract(
        r"\[W\](.+)$", expand=False  # Regex: from end, all chars after [W]
    )
    # 'location' column
    posts["location"] = posts["title"].str.extract(
        r"^\[(.{3}(?:-..))\]",  # Regex: from start, 3 chars plus optional -..
        expand=False,
    )

    return posts
