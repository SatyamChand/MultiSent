import re, string, pickle
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


#to classify the sentiment
classifier_file=open('nbc.pickle','rb')
classifier=pickle.load(classifier_file)
classifier_file.close()

stop_words = stopwords.words('english')



def make_token_dict(text):
    tokens=[]
    for token,tag in pos_tag(word_tokenize(text)):
        token=re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token=re.sub("(@[A-Za-z0-9_]+)","", token)
        
        if tag.startswith("NN"):
            pos='n'
        elif tag.startswith("VB"):
            pos='v'
        else:
            pos='a'
        lemmatizer=WordNetLemmatizer()
        token=lemmatizer.lemmatize(token,pos)
        
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            tokens.append(token.lower())
        
    return dict([token,True] for token in tokens)








def find_sentiment(text):
	return 'Positive' if classifier.classify( make_token_dict(text) ) == 4 else 'Negative'