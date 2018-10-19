# -*- coding: utf-8 -*-

"""
@author: HicBou
@keywords : Semantic Web, Natural Language Processing, SPARQL
@copyright :  Copyright 2018, HicBou
@license : Apache License 2.0
@version : 0.1
@bibliography : http://ramiro.org/notebook/us-presidents-causes-of-death/ , wikidata, wikipedia

Script to compute an terminology analysis between two expressions, segments
or sentences through SPARQL queries on Wikidata. We actually check the upper 
domains related to both group of words and compare them. If they have the 
same, they match and the final score is improved. Otherwise, it will lead to a
lower result.

"""

import requests
import pandas as pd

#Clean segments (group of words) (remove special char etc...)
def clean_segment(segment):
    #NB : Additional processing and regex techniques could be used. 
    segment = str(segment)
    #Normalize unicode characters
    segment = segment.replace('?', ' ')
    segment = segment.replace(',', ' ')
    segment = segment.replace('.', ' ')
    segment = segment.replace(';', ' ')
    segment = segment.replace(':', ' ')
    segment = segment.replace('!', ' ')
    segment = segment.replace('-', ' ')
    segment = segment.replace('’', ' ')
    return segment.replace("'", " ")

#Tokenize segments into a list of words
def tokenize_segment(cleaned_segment): 
    return list(cleaned_segment.split(" "))

#Clean upper domain IDs of a group of words (segment + its language code) in Wikidata
def get_upper_domains(segment, lang_code):
    segment = clean_segment(segment)
    
    #Query on Wikidata to get upper domains of each segment
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql' #Url of the Wikidata's SPARQL endpoint to query
    segment_query = '''
                    SELECT DISTINCT ?superClass WHERE {
                            ?word wdt:P31/wdt:P279? ?superClass.
                            ?word rdfs:label "''' + str(segment) + '''"@''' + str(lang_code) + '''
                            } 
                    '''
                    #SPARQL Query to get upper domains
                    
    segment_query_result = requests.get(url, params={'query': segment_query, 'format': 'json'}).json() #Query result in JSON
    
    #Put all upper domain IDs found into a list
    segment_domains_list = []
    for item in segment_query_result['results']['bindings']:
                segment_domains_list.append(item['superClass']['value'].replace("http://www.wikidata.org/entity/",""))
    segment_domains_DF = pd.DataFrame(segment_domains_list) #Transform the list into a DataFrame
    
    return segment_domains_DF

#Compare two group of words through a SPARQL query on Wikidata. The function's 
#inputs also contain the language in which the segment is written (lang_code).
    #Available lang_codes : https://www.wikidata.org/wiki/Help:Wikimedia_language_codes/lists/all
def compare_windows(segment1, lang_code1, segment2, lang_code2):
    #Clean and tokenize input segments
    segment1 = clean_segment(segment1)
    segment2 = clean_segment(segment2)
    
    #Queries on Wikidata to get upper domains of each segment
    segment1_domains_DF = get_upper_domains(segment1, lang_code1)
    segment2_domains_DF = get_upper_domains(segment2, lang_code2)
    
    if(len(segment1_domains_DF) > 0 and len(segment2_domains_DF) > 0):
        #Get of the common domain IDs between both segments
        intersection_domains = segment1_domains_DF.merge(segment2_domains_DF) 
        #Get of all the domain IDs
        union_domains = pd.concat([segment1_domains_DF, segment2_domains_DF]).drop_duplicates().reset_index(drop=True)
        
        #Compute the final score : common domains / all domains
        score = float(len(intersection_domains) / len(union_domains))
        return score #The window score
    
    else:
        return 0

#Compare two full segments through a SPARQL query on Wikidata. The function's 
#inputs also contain the language in which the segment is written (lang_code).
#We divide the segments into windows (cf max_window_size) and compare each of them.
#The position of the window (ex: 2 first words of each segment) can be noted as relevant.
#Otherwise we compare all possible windows of same size independently of their position (
#ex: first 2 words of the segment 1 and 2 last words of the segment 2).
#NB : The position independent version of the algorithm is way more expensive and long.

def compare_full_segments(segment1, lang_code1, segment2, lang_code2, max_window_size = 3, position_dependent = False):
    #Avoid errors
    if max_window_size < 1 : return "Please enter a valid maximum size of window, at least 1."
    
    #Initialize the sum of all computed scores
    sum_scores = 0 
    
    #Clean and tokenize input segments
    segment1 = tokenize_segment(clean_segment(segment1))
    segment2 = tokenize_segment(clean_segment(segment2))
    
    #If the comparison is position dependent
    if position_dependent == True:
        #Fullfill shortest segment with empty elements
        segment_length = max(len(segment1), len(segment2))
        if len(segment1) > len(segment2) :
            for i in range(len(segment2), len(segment1)): segment2.append("") 
        elif len(segment1) < len(segment2):
            for i in range(len(segment1), len(segment2)): segment1.append("")
        
        #For all window possibilities
        for i in range(segment_length):
            for j in range(i + 1, min(i + 1 + max_window_size, segment_length + 1)):
                segment1_window = ' '.join([x for x in segment1[i:j] if x != ""]) #Define 1st segment window, empty values being removed
                segment2_window = ' '.join([x for x in segment2[i:j] if x != ""]) #Define 2nd segment window, empty values being removed
                #Compare both windows and add the result to the sum of all scores
                window_size = j - i  #Actual window size for both segments              
                sum_scores += compare_windows(segment1_window, lang_code1, segment2_window, lang_code2) * (window_size/max_window_size) 
                    #Bigger is the window of words, more probably meaningful it will be. 
                    #==> so we multiply the sum_score by the window_size
        
    #If the comparison is NOT position dependent
    else:
       #For all window possibilities
           #of segment 1
       for i in range(len(segment1)):
           for j in range(i + 1, min(i + 1 + max_window_size, len(segment1) + 1)):
           #of segment 2
               for k in range(len(segment2)):
                   for l in range(k + 1, min(k + 1 + max_window_size, len(segment2) + 1)):
                       segment1_window = ' '.join(segment1[i:j]) #Define 1st segment window
                       segment2_window = ' '.join(segment2[k:l]) #Define 2nd segment window


                       #print(i,"/",len(segment1),"  ||  ",k, "/",len(segment2))
                       if len(tokenize_segment(segment1_window)) == len(tokenize_segment(segment2_window)): #If the windows have the same size
                           window_size = l-k
                           sum_scores += compare_windows(segment1_window, lang_code1, segment2_window, lang_code2) * (window_size/max_window_size)
                      
    return sum_scores #The Full Segment Comparison Score

#Compute a metric looking like the F1 measure for information retrieval
def personalized_f1_score(segment1, lang_code1, segment2, lang_code2, max_window_size = 3, position_dependent = True):
    #Compute a sum of scores divided by the length of the first segment
    personalized_precision = compare_full_segments(segment1, lang_code1, segment2, lang_code2, max_window_size, position_dependent) / len(tokenize_segment(segment1))
    
    #Compute a sum of scores divided by the length of the second segment
    personalized_recall = compare_full_segments(segment1, lang_code1, segment2, lang_code2, max_window_size, position_dependent) / len(tokenize_segment(segment2))
    
    #Compute the socalled F1 measure
    f1_score = 2 * personalized_precision * personalized_recall / (personalized_recall + personalized_precision)
    return f1_score #The Personalized F1 Measure


'''
Another version of the SPARQL query is not to use the IDs of the upper
domains but the name of them, as following :
    
        SELECT DISTINCT ?superClassLabel WHERE {
                            ?word wdt:P31/wdt:P279? ?superClass.
                            ?superClass rdfs:label ?superClassLabel.
                            ?word rdfs:label "''' "+ str(segment) +" '''"@''' "+ str(lang_code) +" '''
                            FILTER (lang(?superClassLabel) = 'en')
                            } 

Another version of the SPARQL query is to use directly the IDs of concepts havin the same
name as the given input string. Below the query :
    
        SELECT DISTINCT ?word WHERE {
                    ?word rdfs:label "''' "+ str(segment) +" '''"@''' "+ str(lang_code) +" '''.
                    } 
'''