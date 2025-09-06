import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from collections import defaultdict
from sklearn.model_selection import train_test_split

Randomized_df = pd.read_csv("dataset/Randomized_questions_df.csv")

class Preprocessing:

    def preprocessing(self, df):
        contents = df['content'].tolist()
        cleaned_contents = []
        for content in contents:
            cleaned_content=self._preprocessingText(content)
            cleaned_contents.append(cleaned_content)

        df['content'] = cleaned_contents

    def _preprocessingText(self, text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)

        stop_words = set(stopwords.words('english'))
        stop_words_list = []
        for word in tokens:
            if word not in stop_words:
                stop_words_list.append(word)

        lemmatizer = WordNetLemmatizer()
        lemmatized_list = []
        for word in stop_words_list:
            lemmatized_list.append(lemmatizer.lemmatize(word))

        cleaned_text = ' '.join(lemmatized_list)
        return cleaned_text

class NaiveBayes:

    def fit(self, df):
        word_frequencies_by_tag = self._countWordsForEachTag(df)
        self.word_probabilities_by_tag = self._probabilityOfEachWordByTag(word_frequencies_by_tag)

        self.class_probabilities = {}
        total_samples = len(df)
        for tag, tag_count in df['category'].value_counts().items():
            self.class_probabilities[tag] = tag_count / total_samples
        total_tags = sum(self.class_probabilities.values())
        for tag in self.class_probabilities:
            self.class_probabilities[tag] /= total_tags

    def _countWordsForEachTag(self, df):
        word_frequencies_by_tag = defaultdict(lambda: defaultdict(int))

        for idx, row in df.iterrows():
            content = row['content']
            tags = row['category']  
            tokens = content.split()

            for word in tokens:
                word_frequencies_by_tag[tags][word] += 1

        return word_frequencies_by_tag

    def _probabilityOfEachWordByTag(self, word_frequencies_by_tag):
        word_probabilities_by_tag = defaultdict(lambda: defaultdict(float))

        for tag, word_frequencies in word_frequencies_by_tag.items():
            total_words_in_tag = sum(word_frequencies.values())

            for word, frequency in word_frequencies.items():
                word_probabilities_by_tag[tag][word] = frequency / total_words_in_tag

        return word_probabilities_by_tag


    #? P(A|B) = P(B|A) * P(A)
    #?        = log(P(b1|A) + P(b2|A) + ...) * P(A)
    #todo        ~= (log(P(b1|A)) + log(P(b2|A))...) + log(P(A))
    def predict(self, text):
        max_probability = -1
        predicted_tag = None
        tokens = text.split()
        for tag, word_probabilities in self.word_probabilities_by_tag.items():
            probability = 1.0
            for word in tokens:
                word_probability = word_probabilities.get(word, 1e-10)
                probability += word_probability
                # probability *= word_probability
                # probability += np.log(word_probability)
            # probability += np.log(self.class_probabilities[tag])
            probability = np.log(probability)
            probability *= self.class_probabilities[tag]
            if probability > max_probability or max_probability == -1:
                max_probability = probability
                predicted_tag = tag
        return predicted_tag

    def calcAccuracy(self, df):
        total = len(df)
        counter = 0
        for idx, row in df.iterrows():
            textToPredict = row['content']
            actualTag = row['category']
            predictedTag = self.predict(textToPredict)
            if predictedTag == actualTag:
                counter += 1
        
        accuracy = counter / total * 100
        print(f"Accuracy: {accuracy:.2f}%")


pre = Preprocessing()
pre.preprocessing(Randomized_df)

train_df, test_df = train_test_split(Randomized_df, test_size=0.2, random_state=20)
NB = NaiveBayes()
NB.fit(train_df)
NB.calcAccuracy(test_df)

text_to_predict = 'how can I use boostrap in html'
pre_text_to_predict = pre._preprocessingText(text_to_predict)
# print(pre_text_to_predict)
predicted_tag = NB.predict(pre_text_to_predict)
print("Predicted Tag:", predicted_tag)

