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

@st.cache(show_spinner=True, allow_output_mutation=True)
def load_model():
    k_model = KeyBERT(model="key_ext")
    return k_model

def news_card(credits, headline, url_to_news, url_to_image, publish_date, publish_time, content, news_num):
    if content is not None:
        with st.container():
            st.subheader(headline)
            st.text(credits)
            st.text(publish_date + " " + publish_time)
            try:
                st.image(url_to_image, width=600)
            except:
                pass
            news_article = NewsContent(url_to_news)
            news_content = news_article.get_news_content()
            k_model = load_model()
            keywords = k_model.extract_keywords(news_content,
                                    keyphrase_ngram_range=(1, 1), 
                                    stop_words='english', 
                                    highlight=False,
                                    top_n=5)
            keywords = [keyword[0] for keyword in keywords]
            # Five best #colorkey for white background
            
            a = annotation(keywords[0], "1", color="#f5f5f5")
            b = annotation(keywords[1], "2", color="#faafff")
            c = annotation(keywords[2], "3", color="#afafff")
            d = annotation(keywords[3], "4", color="#feafff")
            e = annotation(keywords[4], "5", color="#8effff")
            annotated_text("Tags: ", a, b, c, d, e)
            summarizer = Summarizer(news_content)
            summary = summarizer.get_summary()
            st.markdown(" ")
            entities = NER(news_content).get_entities()
            # Bold the entities in the summary
            summary_out = summary
            for entity in entities:
                summary_out = summary_out.replace(entity.text, "<b>" + entity.text + "</b>")
            st.markdown(summary_out, unsafe_allow_html=True)
            tts = NewsSpeech(summary)
            aud = tts.speak()
            aud.save(f"tts{news_num}.mp3")
            st.audio(f"tts{news_num}.mp3", format="audio/mp3")
            os.remove(f"tts{news_num}.mp3")
            # st.write(summary)
            st.markdown("[Read More](" + url_to_news + ")")

def news_render(news, num):
    credits = news["source"]["name"]
    headline = news["title"]
    url_to_news = news["url"]
    url_to_image = news["urlToImage"]
    publish_date = news["publishedAt"][:11]
    publish_time = news["publishedAt"][12:20]
    content = news["content"]
    news_number = num
    news_card(credits, headline, url_to_news, url_to_image, publish_date, publish_time, content, news_number)

if __name__ == "__main__":
    st.title("News Up")
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
        news_render(news_data, i)
        
    

