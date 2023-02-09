from datetime import datetime, timedelta


def func():
  a = 1
  b = 2
  return b, a

b, a = func()

print(a)
print(b)

duration = timedelta(hours = 1, minutes = 1)
start_time = datetime.utcnow() - duration
print(datetime.now())
print(datetime.utcnow())
print(start_time)

# all_posts = pd.DataFrame()

# fetched, next_page = fetch_posts(5)
# all_posts = fetched

# last_index_time = datetime.utcfromtimestamp(fetched.iloc[-1]['created_utc'])
# incomplete = last_index_time >= start_time