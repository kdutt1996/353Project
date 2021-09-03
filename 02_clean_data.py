import sys
import os
import pandas as pd
import numpy as np
import re
import emoji
import textstat

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(' ', text)


def remove_at(text):
	return re.sub('@[^\s]+', ' ', text)


def remove_symbols(text):
	return re.sub("[^'.,a-zA-Z0-9 ]", ' ', text)


def remove_whitespace(text):
	text = text.lstrip()
	text = text.rstrip()
	return text


def remove_doublespaces(text):
	return re.sub(' +', ' ', text)


def remove_links(text):
	return re.sub('http\S+|www.\S+', ' ', text)


def dale_chall(text):
	return textstat.dale_chall_readability_score(text)


def flesch_kincaid(text):
	return textstat.flesch_kincaid_grade(text)


def automated_readability(text):
	return textstat.automated_readability_index(text)


def flesch_reading_ease(text):
	return textstat.flesch_reading_ease(text)


def sentence_count(text):
	return textstat.sentence_count(text)


def coleman_liau_index(text):
	return textstat.coleman_liau_index(text)


def basedonall(text):
	return textstat.text_standard(text, float_output=False)



def main():
	
	files = [i for i in os.listdir("user_tweets") if i.endswith("csv")]
	
	for file in files:
		#read each csv file one at a time and process them
		data = pd.read_csv("user_tweets/"+str(file))
	
		#remove emojis
		data['text'] = data['text'].apply(lambda j: remove_emoji(j))

		#remove links
		data['text'] = data['text'].apply(lambda k: remove_links(k))

		#remove @
		data['text'] = data['text'].apply(lambda l: remove_at(l))

		#remove symbols
		data['text'] = data['text'].apply(lambda n: remove_symbols(n))

		#remove retweets
		data = data[~data.text.str.startswith('RT')]

		#clean white spaces
		data = data[~data['text'].apply(lambda l: l.isspace())]
		data['text'] = data['text'].apply(lambda p: remove_whitespace(p))
		data['text'] = data['text'].apply(lambda z: remove_doublespaces(z))
		
		#calculate reading levels
		data['dale_chall_readability_score'] = data['text'].apply(lambda y: dale_chall(y))
		data['flesch_kincaid'] = data['text'].apply(lambda a: flesch_kincaid(a))
		data['automated_readability'] = data['text'].apply(lambda b: automated_readability(b))
		data['flesch_reading'] = data['text'].apply(lambda c: flesch_reading_ease(c))
		data['sentence_count'] = data['text'].apply(lambda d: sentence_count(d))
		data['coleman_liau_index'] = data['text'].apply(lambda e: coleman_liau_index(e))
		data['based_on_all_algorithms'] = data['text'].apply(lambda f: basedonall(f))

		#Write to CSV
		data.to_csv("Cleaned_user_tweets/Cleaned_"+str(file), index=False)

if __name__ == '__main__':
    main()