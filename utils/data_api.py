import requests	 
import json

# API_KEY = "4dbc17e007ab436fb66416009dfb59a8"
def NewsData(): 
    main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=3d7d2570874a4de697f837fc650bb57b"
    open_bbc_page = requests.get(main_url).json()
    article = open_bbc_page["articles"]
    with open("news_dict.json", "w") as f:
        json.dump(article, f, indent=4)
    return open_bbc_page


if __name__ == '__main__': 
	NewsData() 
