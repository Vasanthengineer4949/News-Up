from keybert import KeyBERT

k_model = KeyBERT(model="key_ext")
text = "The US is the largest country in the world. Data Science is the best way to learn."
keywords = k_model.extract_keywords(text,
                                    keyphrase_ngram_range=(1, 2), 
                                    stop_words='english', 
                                    highlight=False,
                                    top_n=5)
# Extract only kewords not prob
keywords = [keyword[0] for keyword in keywords]
print(keywords)