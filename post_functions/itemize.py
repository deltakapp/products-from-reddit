import pandas as pd

# string representations of common currencies
# NOT YET USED
# currencies = {
#     '$', 'USD', 'CAD', 'AUD', 'NZD', 'MXN', 'dollars', 'bucks', 'pesos'
#     '£', 'GBP', 'pounds',
#     '¥', 'RMB', 'JPY' 'yuan', 'renmenbi', 'yen',
#     '€', 'EUR', 'euro', 'euros',
#     '₹', 'INR', 'PKR', 'rupees',
#     '₽', 'RUB', 'BYN', 'rubles',
#     'R$', 'BRL', 'reais' }

def extract_prices(posts: pd.DataFrame) -> pd.DataFrame:
    """Extract prices from post text based on price-like strings"""

    # Regex: non-letter, $, (1-5 digits), whitespace
    pattern = r"\s\$(\d{1,5}(?:.\d\d)?)\s"
    return posts.assign(prices=posts["selftext"].str.split(pattern))


def split_by_commas(posts: pd.DataFrame) -> pd.DataFrame:
    """Separate title sections by comma separation"""
        
    #If BUY or TRADE, split "want" column by commas or "or"
    posts = posts.assign(wants_bool=posts["transaction_type"].str.match(r"(?:BUY|TRADE)"))
    posts = posts.assign(wants_split=posts["want"].str.split(r"(?:,|or)")) # unexpected: triggered by game title "Dead or Alive"
    posts["wants_bool"] = posts["wants_bool"].mask(posts["wants_bool"], posts["wants_split"], axis=0)

    #If SELL or TRADE, split "have" column by commas or "and"
    posts = posts.assign(haves_bool=posts["transaction_type"].str.match(r"(?:SELL|TRADE)"))
    posts = posts.assign(haves_split=posts["have"].str.split(r"(?:,|and)"))
    posts["haves_bool"] = posts["haves_bool"].mask(posts["haves_bool"], posts["haves_split"], axis=0)

    # Rename transformed wants_bool and haves_bool
    posts.rename(columns={"wants_bool": "items wanted", "haves_bool": "items_for_sale"})

    # Count number of prices obtained
    # posts = posts.assign(prices_count)

    # Count number of items obtained in wants or haves
    # posts = posts.assign(items_count)
    
    # Compare those counts for equality to estimate accuracy of split
    # posts = posts.assign(item_count_heuristic=)

    return posts


def itemize(posts: pd.DataFrame) -> pd.DataFrame:
    """Creates a dataframe of item(s) from a single post
    
    Args:
        posts: a dataframe of posts
      
    Returns:
        Dataframe of items being bought or sold
    """

    posts = extract_prices(posts)
    print(posts.head())
    items = split_by_commas(posts)
    return items

