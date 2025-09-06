import numpy as np
import re
import string
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


class NaiveBayes:

    def preprocessing(self, text):
        text = text.lower()
        text = " ".join([PorterStemmer().stem(word) for word in text.split()])
        text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text) # removing URL links
        text = re.sub(r"\b\d+\b", " ", text) # removing number 
        text = re.sub(r'<.*?>+', ' ', text) # removing special characters, 
        text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text) # punctuations
        text = re.sub(r'\d{2,}\w+', ' ', text) # numbers before text
        text = re.sub(r'\s{2,}', ' ', text) # duplicated spaces
        return text

    def predict(self, text):
        text = self.preprocessing(text)

        word_probabilities_by_tag = {}
        class_probabilities = {}
        try:
            with open('GogoBot/fitData/wordsProbs.json', 'r') as json_file:
                word_probabilities_by_tag = json.load(json_file)

            with open('GogoBot/fitData/classProbs.json', 'r') as json_file:
                class_probabilities = json.load(json_file)

        except FileNotFoundError:
            print(f'Error: Couldn\'t find the traing data')
            
        max_probability = -1.0
        predicted_tag = None
        tokens = text.split()
        for tag, word_probabilities in word_probabilities_by_tag.items():
            probability = 0.0

            for word in tokens:
                word_probability = word_probabilities.get(word, 1e-10)
                probability += np.log(word_probability)

            probability += np.log(class_probabilities[tag])
            
            if probability > max_probability or max_probability == -1.0:
                max_probability = probability
                predicted_tag = tag

        return predicted_tag