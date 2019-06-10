import spacy
import nltk
from nltk.tokenize import word_tokenize

category = {
    "First Party Collection" : ['use', 'collect', 'demographic', 'location', 'address', 'survey', 'service'],
    "Third Party Sharing" : ['party', 'share', 'sell', 'disclose', 'company', 'advertises'],
    "User Choice / Control" : ['opt', 'unsubscribe', 'disable', 'choose', 'choice', 'consent'],
    "User Access, Edit & Delete" : ['delete', 'profile', 'correct', 'account', 'change', 'update'],
    "Data Retention" : ['retain', 'store', 'delete', 'database', 'participate', 'keep'],
    "Data Security" : ['secure', 'seal', 'safeguard', 'protect', 'ensure'],
    "Policy Change" : ['change privacy', 'policy time', 'current', 'policy agreement'],
    "Do Not Track" : ['signal', 'track', 'track request', 'respond', 'browser', 'advertising']
}
nlp = spacy.load('en')

class User_Query:
    def __init__(self, sentence):
        self.sentence = sentence

    def category_search(self, dictionary, search):
        self.dictionary = dictionary
        self.search = search
        for key, value in dictionary.items():
            for j in value:
                if search.lower() == j:
                    return key

    def name_recognition(self, sentence):
        self.sentence = sentence
        organization = {}
        count = 0
        doc = nlp(sentence)
        org = [(X.text, X.label_) for X in doc.ents]
        for i in org:
            if i[1] == 'ORG':
                organization[count] = {'type' : 'ORGANIZATION', 'name' : i[0]}
                count+=1
            elif i[1] == 'PRODUCT':
                organization[count] = {'type' : 'PRODUCT', 'name' : i[0]}
                count+=1
        return organization

    def get_user_query(self, sentence):
        self.sentence = sentence
        query_class = {}
        count=0
        Tokens = nltk.word_tokenize(sentence)
        bigrams = list(nltk.bigrams(Tokens))
        for i in Tokens: #Single Word Category Checking
            v = i
            res = self.category_search(category, v)
            if res != None:
                query_class[count] = {'class' : res, 'word' : v}
                count+=1
        for bigram_el in bigrams: #Double Word Category Checking
            concat_value = ' '.join(bigram_el)
            #print(v)
            result = self.category_search(category, concat_value)
            if result != None:
                query_class[count] = {'class' : result, 'word' : concat_value}
                count+=1
        return query_class
