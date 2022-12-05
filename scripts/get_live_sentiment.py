# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:17:33 2022

@author: Akhilesh
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_compound(text):
    sid_obj = SentimentIntensityAnalyzer()    
    sentiment_dict = sid_obj.polarity_scores(text)
    compound = sentiment_dict["compound"]
    return sentiment_dict, compound

def get_sent_score(sentiment_dict):
    
    compound = sentiment_dict["compound"]
    if (compound > 0.2) & (compound < 1.0):
        return "Positive"
    elif (compound < 0.2) & (compound > -0.2):
        return "Neutral"
    elif (compound > -1.0) & (compound < -0.2):
        return "Negative"
    '''del sentiment_dict["compound"]
    sentiment_max = max(sentiment_dict, key=sentiment_dict.get) 
    
    if sentiment_max == "neu":
        return "Neutral"
    elif sentiment_max == "pos":
        return "Positive"
    else:
        return "Negative"'''
    