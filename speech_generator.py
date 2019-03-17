
import os as os
import random
import re

# read in the text

# we read in each folder in 'speeches' as its own training set
# and treat each individual speech as if it's just part of one big long one
os.listdir(os.getcwd())


files_list = os.listdir(os.path.join(os.getcwd(), 'Speeches'))

raw_input(files_list)

training_sets = [x[0] for x in os.walk(os.path.join(os.getcwd(), 'Speeches'))]

del training_sets[0] #first one is always the speeches directory itself
raw_input(training_sets)

training_files=[]
for set_folder in training_sets:
    training_files_in_set = [f for f in os.listdir(set_folder)
                             if os.path.isfile(os.path.join(set_folder, f))]
    if training_files_in_set:
        training_files.append((set_folder, training_files_in_set))
        
    

training_texts = []

for author in training_files:
    training_texts.append([author[0], "", []])
    print(author[0])
    for speech in author[1]:
        speech_path = os.path.join(author[0], speech)
        if os.path.isfile(speech_path):
            #add the speech contents to one big string
            f = open(speech_path, "r")
            speech_lines = f.readlines()
            f.close()
            for line in speech_lines:
                training_texts[-1][1] = training_texts[-1][1] + " " + line
            

def MakeIntoTextList(lines):
    #print(lines[0:100])
    text = []
    for word in re.split("[, \ - ! ? ; : ( ) .]+", lines):
        if len(word.strip()) > 0:
            text.append(word)
    return text


for dataset in training_texts:
    dataset[2] = MakeIntoTextList(dataset[1])
                          
def MakeTree(text):            
    # make a start node 
    d = dict(start = [])
    # make a node for each word (that has a word after it)
    for i_word in range(len(text)):
        if i_word < 1:
            continue
        this_word = text[i_word]
        previous_word = text[i_word -1]
        
        # if the previous word has a period after it, add our word to the start node.
        if '\n' in previous_word:
            d['start'].append(this_word)
            continue
        
        # go through each word and add it to the node of the previous word    
        if previous_word not in d and len(this_word.strip()) > 0:
            d[previous_word] = [this_word]
        else:
            d[previous_word].append(this_word)
    return d

dictionaries = []
for dataset in training_texts:
    dictionaries.append([dataset[0], MakeTree(dataset[2])])

# make our text
def MakeText(num_chars = 1390, dict_index = -1):

    d= dictionaries[dict_index][1]
    k = sorted(d.keys())
    out = ""
    r = random.randint(0, len(d['start'])-1)
    current_word=d['start'][r]
    words = 0
    
    lines = 0
    while len(out) < num_chars:
        out = out + current_word + " "
        #our first word should always be in here
        if current_word in d.keys():
            r = random.randint(0, len(d[current_word])-1)
            current_word = d[current_word][r]
        else: #seed a new sentence
            lines = lines +1
            #r = np.random.randint(0, len(d['start']))
            current_word = k[random.randint(0,len(k)-1)]
        words = words +1
    return out
    
    
print(MakeText(1980))
for i in range(len(dictionaries)):
    f=open(str(i)+".txt", 'w')
    f.write(files_list[i] + '\n')
    f.write(MakeText(1390, i))
    f.close()

raw_input('here')
