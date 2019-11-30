import requests
def main():

	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "2j7EUzQg96bbhWH9tyuv7A", "isbns": "080213825X"})
	if res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")

	data=res.json()
	# print(data)

if __name__ == "__main__":
	main()
