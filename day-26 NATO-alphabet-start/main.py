student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

#Looping through dictionaries:
for (key, value) in student_dict.items():
    #Access key and value
    pass

import pandas
from pathlib import Path
ruta_base = Path(__file__).parent
student_data_frame = pandas.DataFrame(student_dict)

#Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    #Access index and row
    #Access row.student or row.score
    pass

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

#TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

df = pandas.read_csv(ruta_base / 'nato_phonetic_alphabet.csv')

dict = {row.letter: row.code for (index, row) in df.iterrows()}

def generate_phonetic():
    input_word = input("Enter a word: ").upper()
    try:
      output_list = [dict[letter] for letter in input_word]
    except KeyError:
        print("sorry only letters in the alphabet please")
        generate_phonetic()
    else:
      print(output_list)

generate_phonetic()
