import requests
good_reads_rate = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "E7Yw9FVYst3sIPplv6g", "isbns": "9781632168146"}).json()['books'][0]['average_rating']
print(good_reads_rate)
