import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string
import operator

class Summarizer:

    def __init__(self, text):
        self.text = text
        self.max_sentences = 3
        # List to string
    
    def get_summary(self):
        print(type(self.text))
        sentences_original = sent_tokenize(self.text)
        print("len of original text", len(sentences_original))
        if self.max_sentences > len(sentences_original):
            print("Error, number of requested sentences exceeds number of sentences inputted")
            self.max_sentences = len(sentences_original)
            pass
        s = self.text.replace('\n', " ")
        words_chopped = word_tokenize(s.lower())
        sentences_chopped = sent_tokenize(s.lower())
        stop_words = set(stopwords.words("english"))
        punc = set(string.punctuation)

        filtered_words = []
        for w in words_chopped:
            if w not in stop_words and w not in punc:
                filtered_words.append(w)
        total_words = len(filtered_words)
        word_frequency = {}
        for w in filtered_words:
            if w in word_frequency.keys():
                word_frequency[w] += 1.0  # increment the value: frequency
            else:
                word_frequency[w] = 1.0  # add the word to dictionary

        for word in word_frequency:
            word_frequency[word] = (word_frequency[word]/total_words)
        print(sentences_original)
        # for each sentence add sum of weighted frequency values
        tracker = [0.0] * len(sentences_original)
        for i in range(0, len(sentences_original)):
            for word in word_frequency:
                if word in sentences_original[i]:
                    tracker[i] += word_frequency[word]
                    
        output_sentences = []
        for i in range(0, len(tracker)):
            # pick sentences with max weighted words
            index, value = max(enumerate(tracker), key=operator.itemgetter(1))
            if len(output_sentences) + 1 <= self.max_sentences and sentences_original[index] not in output_sentences:
                output_sentences.append(sentences_original[index])
            if len(output_sentences) > self.max_sentences:
                break
            tracker.remove(tracker[index])
        sorted_output_sentences = self.sort_sentences(sentences_original, output_sentences)
        output = " ".join(sorted_output_sentences)
        return output
    # sort on the basis of original sentence order
    def sort_sentences(self, original, output):
        sorted_sent_arr = []
        sorted_output = []
        for i in range(0, len(output)):
            if output[i] in original:
                sorted_sent_arr.append(original.index(output[i]))
        sorted_sent_arr = sorted(sorted_sent_arr)
        for i in range(0, len(sorted_sent_arr)):
            sorted_output.append(original[sorted_sent_arr[i]])
        print("===== sorted_output======", sorted_output)
        return sorted_output