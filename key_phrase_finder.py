import boto3
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

class KeyPhraseFinder:
    def __init__(self, access_key, secret_key, session_token):
        self.porter_stemmer = PorterStemmer()
        nltk.download('punkt_tab')
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
        return re.sub(r'[^a-zA-Z0-9 ]', '', key_phrase_object['Text'])
    
    def treat_phrase(self, phrase):
        tokens = word_tokenize(phrase.lower())
        tokens_without_stopwords = [t for t in tokens if t not in self.english_stopwords]
        phrase_without_stopwords = ''.join(tokens_without_stopwords)
        return {
            'originalPhrase':  phrase,
            'stemmedPhrase': self.porter_stemmer.stem(phrase_without_stopwords)
        }

    def removeDuplicatedStemmedPhrases(self, theme, phrases):
        seen_stemmed = set()
        unique_phrases = []

        for phrase in phrases:
            if phrase['stemmedPhrase'] not in seen_stemmed:
                if phrase['stemmedPhrase'] == theme['stemmedPhrase']:
                    continue
                seen_stemmed.add(phrase['stemmedPhrase'])
                tokens = word_tokenize(phrase['originalPhrase'])
                if tokens[0] in self.english_stopwords:
                    tokens = tokens[1:]
                    phrase['originalPhrase'] = ' '.join(tokens)
                if tokens[-1] in self.english_stopwords:
                    tokens = tokens[:-1]
                    phrase['originalPhrase'] = ' '.join(tokens)

                unique_phrases.append(phrase['originalPhrase'])

        return unique_phrases

    def get_key_phrases(self, theme, content):
        response = self.client.detect_key_phrases(
            Text=content,
            LanguageCode='en'
        )

        treated_theme = self.treat_phrase(theme)

        key_phrases_list = list(map(self.separate_term_from_key_phrase_object, response['KeyPhrases']))

        treated_phrases_list = list(map(self.treat_phrase, key_phrases_list))

        unique_phrases = self.removeDuplicatedStemmedPhrases(treated_theme, treated_phrases_list)

        return unique_phrases