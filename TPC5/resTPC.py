# pip install -U spacy
# python -m spacy download en_core_web_sm

'''
NAME
   resTPC - writes down the words present in a file along with their pos_ and lemma_

SYNOPSIS
   python3 restTPC.py input_file

DESCRIPTION
   This script gives out a table like output after processing the input_file. 
   The columns are: word, POS and Normal Form. It uses SpaCy for NLP tasks, as well as a matcher.
   The matcher is used to ID patterns, in this particular case, expressions like "Ponte de Lima".
'''

import spacy
from spacy.matcher import Matcher
import pandas as pd
import json
import sys

# Load Portuguese language model
nlp = spacy.load("pt_core_news_lg")

# Get the filename and directory from command-line arguments
file_path = sys.argv[1]

# Read the content of the file
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# Process text
doc = nlp(text)

# Load patterns from JSON file
with open("patterns.json", "r") as file:
    patterns = json.load(file)

# Initialize matcher
matcher = Matcher(nlp.vocab)
matcher.add("Named_Entity", patterns)

# Extract words, POS, and normal form (word or conjugation)
data = []
with doc.retokenize() as retokenizer:
    for match_id, start, end in matcher(doc):
        span = doc[start:end]
        retokenizer.merge(span)
for token in doc:
    if token.ent_type_:
        #pos = "Localidade"  # or any other POS you prefer for named entities
        pos = token.pos_
        normal_form = token.text  # Keep the entity intact
        data.append([token.text, pos, normal_form])
    else:
        pos = token.pos_
        if pos == "VERB":
            normal_form = token.lemma_
        else:
            normal_form = token.text
        data.append([token.text, pos, normal_form])

# Create DataFrame
df = pd.DataFrame(data, columns=["Word", "POS", "Normal Form"])

# Display DataFrame
print(df)
df.to_json("dataframe_output.json", orient="records") #for a json file output
df.to_csv("dataframe_output.csv", index=False) #for a table like output

# Optionally, you can also save to other formats like Excel, JSON, or pickle
# df.to_excel("dataframe_output.xlsx", index=False)
# df.to_json("dataframe_output.json", orient="records")
# df.to_pickle("dataframe_output.pkl")