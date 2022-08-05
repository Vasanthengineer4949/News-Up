from newspaper import Article


class NewsContent():

    def __init__(self, news_url):
        self.news_url = news_url
    
    def parse_article(self):
        article = Article(self.news_url)
        article.download()
        article.parse()
        article.nlp()
        return article 
    
    def get_news_content(self):
        article_content = self.parse_article()
        return article_content.text
    
    def get_news_summary(self):
        article_content = self.parse_article()
        return article_content.summary
    
                
