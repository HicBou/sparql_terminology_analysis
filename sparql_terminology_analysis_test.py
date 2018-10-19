# -*- coding: utf-8 -*-
"""
@author: HicBou
@keywords : Semantic Web, Natural Language Processing, SPARQL
@copyright :  Copyright 2018, HicBou
@license : https://creativecommons.org/licenses/by/4.0/
@version : 0.1
@bibliography : http://ramiro.org/notebook/us-presidents-causes-of-death/ 

Script to test the other one : sparql_terminology_analysis.py
"""

from sparql_terminology_analysis import get_upper_domains
from sparql_terminology_analysis import compare_full_segments
from sparql_terminology_analysis import personalized_f1_score

#TEST PART OF SPARQL_TERMINOLOGY_ANALYSIS.PY

print("Github's Example Part -----------------------------")
print("grave @en ==> \n", get_upper_domains("grave", "fr"))
print("grave @fr ==> \n", get_upper_domains("a", "en"))

print("'grave accident' @fr VS 'a grave' @en : ", compare_full_segments("grave accident", "fr", "a grave", "en", 2, False))
print("'grave accident' @fr VS 'a grave' @en : \n F1 Measure : \n ", personalized_f1_score("grave accident", "fr", "a grave", "en", 2, False))

print("\n\nAnother example -----------------------------")
print("Madère @fr ==> \n", get_upper_domains("Madère", "fr"))
print("Madeira @en ==> \n", get_upper_domains("Madeira", "en"))   

print("\n\nAnother example -----------------------------")
print("'Je suis le Victor Hugo' @fr VS 'I am Victor Hugo' @en : ", compare_full_segments("Je suis le Victor Hugo", "fr", "I am Victor Hugo", "en", 3, True))
print("'Victor Hugo Je suis le fameux' @fr VS 'Victor Hugo I am' @en : ", compare_full_segments("Victor Hugo Je suis le fameux", "fr", "Victor Hugo I am ", "en", 3, True))

print("'Je suis le Victor Hugo' @fr VS 'I am Victor Hugo' @en : ", compare_full_segments("Je suis le Victor Hugo", "fr", "I am Victor Hugo", "en", 3, False))
print("'Victor Hugo Je suis le fameux' @fr VS 'Victor Hugo I am' @en : ", compare_full_segments("Victor Hugo Je suis le fameux", "fr", "Victor Hugo I am ", "en", 3, True))

print("'Victor Hugo' @fr VS 'Victor Hugo' @en : ", compare_full_segments("Victor Hugo", "fr", "Victor Hugo", "en", 3, True))
print("'Victor Hugo' @fr VS 'Victor Hugo' @en : ", compare_full_segments("Victor Hugo", "fr", "Victor Hugo", "en", 3, False))

print("'Victor Hugo' @fr VS 'Victor Hugo' @en : ", compare_full_segments("Victor Hugo", "fr", "Victor Hugo", "en", 5, True))
print("'Victor Hugo' @fr VS 'Victor Hugo' @en : ", compare_full_segments("Victor Hugo", "fr", "Victor Hugo", "en", 1, False))
print("'Victor Hugo' @fr VS 'Victor Hugo' @en : ", compare_full_segments("Victor Hugo", "fr", "Victor Hugo", "en", 0, False))

print("'Victor Hugo' @fr VS 'Victor Hugo' @en \n F1 Measure : \n ", personalized_f1_score("Victor Hugo", "fr", "Victor Hugo", "en", 5, True))
print("'Victor Hugo' @fr VS 'Victor Hugo' @en \n F1 Measure : \n ", personalized_f1_score("Victor Hugo", "fr", "Victor Hugo", "en", 3, True))
