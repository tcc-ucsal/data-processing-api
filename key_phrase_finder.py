import boto3
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

class KeyPhraseFinder:
    def __init__(self, access_key, secret_key, session_token):
        self.porter_stemmer = PorterStemmer()
        nltk.download('stopwords')
        self.english_stopwords = stopwords.words('english')
        self.access_key = access_key
        self.secret_key = secret_key
        self.session_token = session_token
        self.client = boto3.client(
            'comprehend',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_token,
            region_name='us-east-1'
        )

    def separate_term_from_key_phrase_object(self, key_phrase_object):
        return re.sub(r'[^a-zA-Z0-9 ]', '', key_phrase_object["Text"])
    
    def treat_phrase(self, phrase):
        tokens = word_tokenize(phrase.lower())
        tokens_without_stopwords = [t for t in tokens if t not in self.english_stopwords]
        phrase_without_stopwords = ''.join(tokens_without_stopwords)
        return self.porter_stemmer.stem(phrase_without_stopwords) 

    def get_key_phrases(self, content):
        response = self.client.detect_key_phrases(
            Text=content,
            LanguageCode='en'
        )

        key_phrases_list = list(map(self.separate_term_from_key_phrase_object, response["KeyPhrases"]))

        treated_phrases_list = list(map(self.treat_phrase, key_phrases_list))

        print(treated_phrases_list)

        return list(set(key_phrases_list))