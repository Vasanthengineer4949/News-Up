import os
import streamlit as st
from utils.newscontent import NewsContent
from utils.data_api import NewsData
from keybert import KeyBERT
from annotated_text import annotated_text
from annotated_text import annotation
from utils.summarizer import Summarizer
from utils.tts import NewsSpeech
from utils.ner import NER
import nltk
nltk.download('punkt')
nltk.download('stopwords')


@st.cache(show_spinner=True, allow_output_mutation=True)
def load_model():
    k_model = KeyBERT(model="key_ext_small")
    return k_model

def news_card(credits, headline, url_to_news, url_to_image, publish_date, publish_time, content, news_num, model):
    k_model = model
    if content is not None:
        with st.container():
            st.subheader(headline)
            st.text(credits)
            st.text(publish_date + " " + publish_time)
            try:
                st.image(url_to_image, width=600, use_column_width=True)
            except:
                pass
            news_article = NewsContent(url_to_news)
            news_content = news_article.get_news_content()
            keywords = k_model.extract_keywords(news_content,
                                    keyphrase_ngram_range=(1, 1), 
                                    stop_words='english', 
                                    highlight=False,
                                    top_n=4)
            keywords = [keyword[0] for keyword in keywords]
            # Five best #colorkey for white background
            annotated_text("Tags: ", 
                                    annotation(keywords[0], "1", color="#f5f5f5"), 
                                    annotation(keywords[1], "2", color="#faafff"), 
                                    annotation(keywords[2], "3", color="#afafff"), 
                                    annotation(keywords[3], "4", color="#feafff"))
            summarizer = Summarizer(news_content)
            summary = summarizer.get_summary()
            st.markdown(" ")
            entities = NER(news_content).get_entities()
            # Bold the entities in the summary
            summary_out = summary
            for entity in entities:
                summary_out = summary_out.replace(entity.text, "<b>" + entity.text + "</b>")
            st.markdown(summary_out, unsafe_allow_html=True)
            # tts = NewsSpeech(summary)
            # aud = tts.speak()
            # aud.save(f"tts{news_num}.mp3")
            # st.audio(f"tts{news_num}.mp3", format="audio/mp3")
            # os.remove(f"tts{news_num}.mp3")
            st.markdown("[Read More](" + url_to_news + ")")


def news_render(news, num, model):
    credits = news["source"]["name"]
    headline = news["title"]
    url_to_news = news["url"]
    url_to_image = news["urlToImage"]
    publish_date = news["publishedAt"][:11]
    publish_time = news["publishedAt"][12:20]
    content = news["content"]
    news_number = num
    key_model = model
    news_card(credits, headline, url_to_news, url_to_image, publish_date, publish_time, content, news_number, key_model)

if __name__ == "__main__":
    import time
    start_time = time.time()
    st.title("News Up")
    st.spinner("Model Loading")
    model = load_model()
    st.sidebar.title("News Up")
    st.sidebar.markdown("This News Up is an application that takes trending news from the web and provides you with a summary of the news." + 
    "Along with the news, it also provides you with a list of keywords that are associated with the news." +
    "Some of the entities in the news are also highlighted in the summary.It also provides you with a sound clip of the news.You can also play the sound clip of the news.")
    st.sidebar.markdown("Made with ❤️ by Vasanth", unsafe_allow_html=True)
    st.sidebar.markdown("[![Github](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/Vasanthengineer4949/) [![LinkedIn](https://badgen.net/badge/icon/LinkedIn?icon=linkedin&label)](https://www.linkedin.com/in/vasanth-engineer-4949/)")
    st.subheader("**__Trending News__**")
    news = NewsData()
    for i in range(10):
        news_data = news["articles"][i]
        news_render(news_data, i, model)
    

