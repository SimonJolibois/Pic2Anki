import requests
import json
import nagisa
import pandas as pd
import os
from googletrans import Translator
from bs4 import BeautifulSoup
from tqdm import tqdm
from jamdict import Jamdict
import re


def get_unique(w_list):
    """Get all unique elements of a list"""
    list_unique = []
    for i in range(len(w_list)):
        if not w_list[i] in list_unique:
            list_unique.append(w_list[i])
    return(list_unique)

def clean_list(input_list):
    """Clean a string of all punctuations and newline"""
    for i in range(len(input_list)):
        input_list[i] = re.sub(r'[^\w\s]', '', input_list[i]).replace('\n', '')
    return(input_list)

def image_to_text(adress_string):
    """ Apply OCR to an image and return recognized japanese text"""
    # OCR keys
    url = 'https://api.ocr.space/parse/image'
    payload = {
        'apikey': 'MY-API-KEY',
        'language': 'jpn', # Set the language to Japanese
        'isOverlayRequired': False
    }
    text = ""

    # Check whether the image was already analyzed before
    if not os.path.exists(adress_string[:-4]+".txt"):
        # Process image with OCR
        files = {'image': (adress_string, open(adress_string, 'rb'), 'image/jpeg')}
        response = requests.post(url, files=files, data=payload)
        json_response = json.loads(response.content.decode('utf-8'))
        if json_response['IsErroredOnProcessing'] == False:
            text = json_response['ParsedResults'][0]['ParsedText'].replace('\n','')
        else:
            print('OCR error:', json_response['ErrorMessage'])

        # Save processed text in a .txt file
        with open(adress_string[:-4]+".txt",'w',encoding='utf-8') as file:
            file.write(text)

    else:
        # Load .txt file
        text_file = open(adress_string[:-4]+".txt",'r',encoding='utf-8')
        text = text_file.read()

    return text


def splitter(full_text):
    """Split a string into sentences"""
    d = "。"
    split_text = [e+d for e in full_text.split(d) if e]
    split_text = [elem.replace("\n", "") for elem in split_text]
    return(split_text)

def find_sentence(t_list, w_list):
    """Find for each word of w_list a sentence of t_list containing it"""
    sentence_list = [0]*len(w_list)
    for i, w in enumerate(w_list):
        for j in range(len(t_list)):
            if w in t_list[j]:
                sentence_list[i] = j
                break
    return sentence_list

def translate(list_sentence,language='fr'):
    """Translate a list of sentence to the required language"""
    print("Translating...")
    list_text_trad = []
    p = Translator()
    for sentence in tqdm(list_sentence):
        try:
            p_translated = p.translate(sentence,src='ja', dest=language) 
            list_text_trad.append(str(p_translated.text))
        except:
            print("Translation of the sentence failed: ",sentence)
    return(list_text_trad)

def get_verbs(w_list,l_list):
    """Get all conjugued verbs in w_list using the labels of l_list"""
    verb_list = []
    for i in range(len(l_list)):
        if l_list[i]=="動詞":
            for j in range(i,min(len(l_list),i+4)):
                if l_list[j]=="助動詞":
                    verb_list.append(''.join(w_list[i:j+1]))
    return(verb_list)

def filtering_dataframe(df,w_list,s_text,s_text_trad,s_list):
    """Filter datframe to only keep words in w_list
       Add sentence from splitted text using the labels of sentence list. 
       Also return the rest of the words in a list"""
    print("Filtering dataframe")
    df_filtered = pd.DataFrame(columns=list(df.columns) + ["例文","例文の翻訳"])
    unknown_words = []
    for i, w in tqdm(enumerate(w_list)):
        mask = (df['Word'] == w) | (df['Reading'] == w)
        try:
            first_row = df.loc[mask].iloc[0]
            first_row["例文"] = s_text[s_list[i]]
            first_row["例文の翻訳"] = s_text_trad[s_list[i]]
            temp_df = pd.DataFrame([first_row], columns=df_filtered.columns)
            df_filtered = pd.concat([df_filtered, temp_df], ignore_index=True)
        except:
            unknown_words.append(w)
    return(df_filtered,unknown_words)


def save(text_or,text,words_list,words_list_unique,labels_list,split_text,split_text_trad,verb_list_unique,verb_df):
    with open('analysis.txt','w',encoding='utf-8') as file:
        """Store all data in .txt file"""
        file.write("Word list\n")
        file.write(text_or)

        file.write("\nNagisa processed list\n")
        file.write(str(text))

        file.write("\n\nWords list\n")
        file.write(str(words_list))
        file.write("\nLength: "+ str(len(words_list)))

        file.write("\n\nWords list unique\n")
        file.write(str(words_list_unique))
        file.write("\nLength: "+ str(len(words_list_unique)))

        file.write("\n\nLabels list\n")
        file.write(str(labels_list))

        file.write("\n\nSplit text\n")
        file.write(str(split_text))

        file.write("\n\nSplit text translation\n")
        file.write(str(split_text_trad))

        file.write("\n\nVerbs list unique\n")
        file.write(str(verb_list_unique))

        file.write("\n\nVerbs Takoboto\n")
        file.write(str(verb_df))
    print("Data saved")


def get_takoboto(verb_string):
    url = 'https://takoboto.jp/'
    params = {'q': verb}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        html_content = response.content.decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        result_word = soup.find('div', {'id': 'ResultWord0'})
        dictionary,furigana,translation,example="","","",""

        if result_word:
            dictionary = result_word.find('span').text
            furigana = result_word.find_all('div')[0].find_all('span')[-1].text.replace(",","")
            div_list = result_word.find_all('div')
            translation = ''.join(str(i) for i in div_list[3].find_all('span')[1:])
            translation = translation.replace('<span>','').replace('</span>','')
            example = div_list[-2].find('span').text

    return(dictionary,furigana,translation,example)


def get_jamdict(jam, string):
    result = jam.lookup(string)
    char = result.chars
    list_def=[]
    char_list = []
    try:
        result = result.entries[0]
        text = str(result)[str(result).index(']')+1:str(result).index(':')]
    except: 
        result = ""
        text = ""
    try:
        kana,kanji = text.split('(')
        kana = kana.replace(' ','')
        kanji = kanji.replace(')','').replace(' ','')
    except:
        kana = text
        kanji = ""
    
    try:
        for sense in result.senses:
            sense = str(sense)[:str(sense).index('((')]
            list_def.append(sense)
            def_string = ", ".join(list_def)
    except:
        def_string = ""
    if len(char) > 0:
        char = str(char)[1:-1].split(', ')
        for e in char:
            char_list.append({'kanji':e[0],'definition':e[4:]})
    
    return(kanji, kana, def_string, str(char_list))

if __name__ == '__main__':

    # OCR processing
    print("Processing the images...")
    text_or = ""
    for filename in tqdm(sorted(os.listdir("test"),key=str.lower,reverse=True)):
        if filename.endswith('.jpg'):
            text_or = text_or.rstrip() + image_to_text(adress_string = 'test/'+filename).lstrip()
    
    # Segmentation
    print("Segmentation...")
    text = nagisa.tagging(text_or)
    words_list = text.words
    labels_list = text.postags

    # List of words
    print("Creating dataframes")
    words_list_unique = get_unique(words_list)
    words_list_unique = clean_list(words_list_unique)

    # List of verbs
    verb_list = get_verbs(words_list, labels_list)
    verb_list = clean_list(verb_list)
    verb_list_unique = get_unique(verb_list)

    # List of sentences and traduction
    split_text = splitter(text_or)
    split_text_trad = translate(split_text) #TODO: cache sentences in a file
    split_text_trad = [e.replace("\'","'") for e in split_text_trad]

    # List of sentences indexes for words and verbs
    words_indexes = find_sentence(split_text, words_list_unique)
    verbs_indexes = find_sentence(split_text, verb_list_unique)

    # Dataframe for Words
    print("Dataframe for Words")
    jam = Jamdict()
    word_df = pd.DataFrame(columns=["Word","Reading","Meaning EN","Meaning FR","例文","例文の翻訳","JLPT"])
    for i in tqdm(range(len(words_list_unique))):
        word = words_list_unique[i]
        if word != "":
            kanji, kana, list_def, char_list = get_jamdict(jam, word)
            example = split_text[words_indexes[i]]
            example_trad = split_text_trad[words_indexes[i]]
            temp_df = pd.DataFrame({"Word":kanji,"Reading":kana,"Meaning EN":list_def,"Meaning FR":"","例文":example,"例文の翻訳":example_trad,"JLPT":""},index=[0])
            word_df = pd.concat([word_df,temp_df],ignore_index=True)

    # Dataframe for Verbs
    print("Dataframe for verbs")
    verb_df = pd.DataFrame(columns=["Word","Reading","Meaning EN","Meaning FR","例文","例文の翻訳","JLPT"])
    for i in tqdm(range(len(verb_list_unique))):
        verb = verb_list_unique[i]
        kanji,kana,list_def,example = get_takoboto(verb)
        example = split_text[verbs_indexes[i]]
        example_trad = split_text_trad[verbs_indexes[i]]
        temp_df = pd.DataFrame({"Word":kanji,"Reading":kana,"Meaning EN":list_def,"Meaning FR":"","例文":example,"例文の翻訳":example_trad,"JLPT":""},index=[0])
        verb_df = pd.concat([verb_df,temp_df],ignore_index=True)

    # Cleaning
    print("Cleaning")
    word_df = word_df.drop_duplicates(subset="Word")
    verb_df = verb_df.drop_duplicates(subset="Word")

    # Saving data
    print("Saving data")
    save(text_or,text,words_list,words_list_unique,labels_list,split_text,split_text_trad,verb_list_unique,verb_df)
    word_df.to_excel("words.xlsx",index=False)
    verb_df.to_excel("verbs.xlsx",index=False)
