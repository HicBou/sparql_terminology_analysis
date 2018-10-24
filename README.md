<h1>A Scoring Method for Terminology Analysis through SPARQL Queries</h1>
The aim of the script given hereby is to compare two sentences or segments (group of words) in terms of terminology, that is to say if 
the words refer to the same concepts. For this purpose, we use SPARQL Queries on the free semantic database (knowledge base) named Wikidata
in order to retrieve the related concepts.

<h2>Terminology Analysis</h2>
Depending on the language, similar terms could have various meanings : if you take by example the noun "a grave" in English and the 
adjective "grave" in French, they don't have the same signification at all. The associated contexts (and concepts) will thus also be 
different. That's why it is important to check to what they are related. That's the aim of the Terminology Analysis.

<h2>Semantic knowledge bases and query languages</h2>

<h4>Semantic Web</h4>
The Semantic Web is an extension of the World Wide Web which promotes specific common data formats and exchange protocols that can
easily read by humans and computers, such as the RDF (Ressource Description Format). 

<h4>Wikidata and knowledge bases</h4>
A knowledge base is a technology used to store complex structured and unstructured information which can be automatically processed, 
a "semantic database" in other words. It contains RDF documents that can be queried. Wikidata, belonging to the Wikimedia 
Foundation (also owning Wikipedia) is one of them.

<h4>SPARQL</h4>
SPARQL is a RDF query language that can notably extract information from RDF Triplestores and knowledge bases. The scripts in Python given in this repository used it to query Wikidata.

<h2>Scoring Method</h2>

<h3>General principle</h3>
Our scoring method/metric tries to estimate a terminology matching rate between 2 segments (sentences or group of words) given as inputs. 
We use therefore SPARQL queries to extract from Wikidata the concepts to what the segments are related, that is to say the "upper" 
domains/elements which contain them. 

To compare 2 complete sentences, we divide each of them into group of words (windows) and compare their associated concepts in Wikidata.
If they have the same ones, they match. Otherwise, they probably don't have the same signification. According to the same principles, more windows match between both input segments, more probably the sentences share the same meaning too. The calculation steps 
are explained below :

<h4>Window Score</h4>
As said, we divide sentences into group of words named "windows" and compare their related concepts. The size of the windows, in number
of words, are always equal between both sentences and their maximum is determined as an input parameter of the Python function.
The "Window Score" is thus given as :

<br/><img src="https://latex.codecogs.com/gif.latex?Window\&space;score\&space;=&space;\frac{Upper\&space;Domains\&space;of\&space;Segment\&space;1\&space;\cap\&space;Upper\&space;Domains\&space;of\&space;Segment\&space;2\&space;}{Upper\&space;Domains\&space;of\&space;Segment\&space;1\&space;\cup\&space;Upper\&space;Domains\&space;of\&space;Segment\&space;2\&space;}" title="Window\ score\ = \frac{Upper\ Domains\ of\ Segment\ 1\ \cap\ Upper\ Domains\ of\ Segment\ 2\ }{Upper\ Domains\ of\ Segment\ 1\ \cup\ Upper\ Domains\ of\ Segment\ 2\ }" />

<h4>Full Segment Comparison Score</h4>

For all possible windows of words from both sentences, we compute the window score. The maximum size of the window is given as input parameter and can be changed by the user. If one sentence is longer than the other, we "fullfill" the shortest one with empty/null words. The user can also provide a condition : the position dependency. If it is activated, the algorithm will compare only windows starting from the same position (i-th word) in the sentence. Otherwise, by default, all combinations will be tested.

Then we add all "Window Scores" as following :

<br/><img src="https://latex.codecogs.com/gif.latex?Full\&space;Segment\&space;Comparison\&space;Score\&space;=&space;\sum_{All\&space;possible\&space;Windows\&space;}^{Total\&space;Segment\&space;Length}&space;\frac{Window\&space;Score\&space;\cdot\&space;Window\&space;Size}{Maximum\&space;Window\&space;Size}" title="Full\ Segment\ Score\ = \sum_{All\ possible\ Windows\ }^{Total\ Segment\ Length} \frac{Window\ Score\ \cdot\ Window\ Size}{Maximum\ Window\ Size}" />

<h4>Personalized F1 Score</h4>

The algorithm provides a metric imitating the F1 measure for information retrieval. To achieve this, we divide the returned "Full 
Segment Comparison Score" by the length of the input sentences 1 & 2. Below the corresponding complete formula :

<img src="https://latex.codecogs.com/gif.latex?Personalized\&space;F1\&space;Measure\&space;=\&space;2&space;\cdot\&space;\frac{&space;\frac{Full\&space;Segment\&space;Comparison\&space;Score}{Segment\&space;1\&space;Size}&space;\cdot\&space;\frac{Full\&space;Segment\&space;Comparison\&space;Score}{Segment\&space;2\&space;Size}}{\frac{Full\&space;Segment\&space;Comparison\&space;Score}{Segment\&space;1\&space;Size}\&space;&plus;\&space;\frac{Full\&space;Segment\&space;Comparison\&space;Score}{Segment\&space;2\&space;Size}&space;}" title="Personalized\ F1\ Measure\ =\ 2 \cdot\ \frac{ \frac{Full\ Segment\ Comparison\ Score}{Segment\ 1\ Size} \cdot\ \frac{Full\ Segment\ Comparison\ Score}{Segment\ 2\ Size}}{\frac{Full\ Segment\ Comparison\ Score}{Segment\ 1\ Size}\ +\ \frac{Full\ Segment\ Comparison\ Score}{Segment\ 2\ Size} }" />

We could simplify it as following :

<img src="https://latex.codecogs.com/gif.latex?Personalized\&space;F1\&space;Measure\&space;=\&space;2&space;\cdot\&space;\frac{&space;Precision\&space;\cdot\&space;Recall}{Precision\&space;&plus;\&space;Recall&space;}" title="Personalized\ F1\ Measure\ =\ 2 \cdot\ \frac{ Precision\ \cdot\ Recall}{Precision\ +\ Recall }" />

<h2>Example</h2>

If we had to compare the simple segments "grave accident" in French and "a grave" in English, the "Full Segment Comparison Score" would
be calculated step by step as following :

| Step 	| Compared Elements                                   	| Upper Domains retrieved                                                                                                                                     	| Common/Total Domain IDs 	| Window Score 	| Actualized Full Segment Comparison Score 	|
|------	|-----------------------------------------------------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------	|-------------------------	|--------------	|------------------------------------------	|
| #1   	| S1 (fr) : "grave" <br/> S2 (en) : "a"               	| S1 (fr) : {Q187588,Q216353,Q355567,Q3647172,Q4120621,Q47574}<br/> S2 (en) : {Q215627,Q863908,Q3910834,Q4833830,Q15644791,Q23828039,Q50365914,Q532,Q7187,Q5} 	| 0 / 16                  	| 0            	| 0                                        	|
| #2   	| S1 (fr) : "grave" <br/> S2 (en) : "a grave"         	| Not the same size, skipped                                                                                                                                  	| -                       	| -            	| 0                                        	|
| #3   	| S1 (fr) : "grave"<br/> S2 (en) : "grave"            	| S1 (fr) : {Q187588,Q216353,Q355567,Q3647172,Q4120621,Q47574}<br/> S2 (en) : {Q3647172,Q47574}                                                               	| 2 / 6                   	| 0.1666       	| 0.1666                                   	|
| #4   	| S1 (fr) : "grave accident"<br/> S2 (en) : "a"       	| Not the same size, skipped                                                                                                                                  	| -                       	| -            	| 0.1666                                   	|
| #5   	| S1 (fr) : "grave accident"<br/> S2 (en) : "a grave" 	| S1 (fr) : {}<br/> S2 (en) : {}                                                                                                                              	| 0                       	| 0            	| 0.1666                                   	|
| #6   	| S1 (fr) : "grave accident"<br/> S2 (en) : "grave"   	| Not the same size, skipped                                                                                                                                  	| -                       	| -            	| 0.1666                                   	|
| #7   	| S1 (fr) : "accident"<br/> S2 (en) : "a"             	| S1 (fr) : {Q179289,Q1931388,Q2438541}<br/> S2 (en) : {Q215627,Q863908,Q3910834,Q4833830,Q15644791,Q23828039,Q50365914,Q532,Q7187,Q5}                        	| 0 / 13                  	| 0            	| 0.1666                                   	|
| #8   	| S1 (fr) : "accident"<br/> S2 (en) : "a grave"       	| Not the same size, skipped                                                                                                                                  	| -                       	| -            	| 0.1666                                   	|
| #9   	| S1 (fr) : "accident"<br/> S2 (en) : "grave"         	| S1 (fr) : {Q179289,Q1931388,Q2438541}<br/> S2 (en) : {Q3647172,Q47574}                                                                                      	| 0 / 5                   	| 0            	| 0.1666                                   	|

Then, we could get the "Personalized F1 Measure" through :

<br/><img src="https://latex.codecogs.com/gif.latex?Personalized\&space;F1\&space;Measure\&space;=\&space;2&space;\cdot\&space;\frac{&space;\frac{0.1666}{2}&space;\cdot\&space;\frac{0.1666}{2}}{\frac{0.1666}{2}&space;&plus;\&space;\frac{0.1666}{2}&space;}&space;=&space;0.08333333333333333" title="Personalized\ F1\ Measure\ =\ 2 \cdot\ \frac{ \frac{0.1666}{2} \cdot\ \frac{0.1666}{2}}{\frac{0.1666}{2} +\ \frac{0.1666}{2} } = 0.08333333333333333" />

<h2>References</h2>

-[Wikipedia](https://fr.wikipedia.org) <br/>
-[Wikidata](https://www.wikidata.org) <br/>
-[Ramiro.org](http://ramiro.org/notebook/us-presidents-causes-of-death/) <br/>


<h2>Credits</h2>

Copyright (c) 2018, HicBoux. Work released under Apache 2.0 License. 

(Please contact me if you wish to use my work in specific conditions not allowed automatically by the Apache 2.0 License.)




