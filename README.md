# Pic2Anki
## What is Pic2Anki?
When reading a japanese book to train, one may encounter words with unknown meaning and/or pronounciations. Usually one would write the furigana next to the kanjis and the definition somewhere on the page, but it ends up impacting the lisibility as a whole. Pic2Anki aims to solve this problem by moving the kanji learning phase ahead of the reading phase, importing all kanjis to an Excel spreadsheet that can be used to create an Anki deck to learn all problematic words.

With [OCR Space](https://ocr.space/), pictures are analyzed to extract text. The [Nagisa](https://github.com/taishi-i/nagisa) package then segments the strings into individual words and give their POS tagging. Words are translated thanks to Google Translate API, while verbs' translations are scraped on [Takoboto](https://takoboto.jp/) to make sure even conjugated forms are recognized. Finally, all is stored in a Excel spreadsheet that can be directly in Anki to create a Deck. The original sentence in which each word was contained can also make a good example to clarify the definition.

### Misc.:
- The final Excel spreadsheet isn't curated. You need to manually remove all elements you don't want in the Deck.
- The OCR of images are stored in individual .txt files to save on the 500 requests/month cap.
- A analysis.txt file is created each time, containing data of all steps of the scripts for debugging purposes.
- Translation steps on Google Translate and Takoboto may be a bit long (10 pages ~ 6-10min) as the services limit the request rate

## How to Install
Seems like the .bat files don't for some reasons. For now, here is the workflow:
1. Git clone the repository 
2. ~~Run install.bat to create a virtual environnement install all required packages~~ 
3. In a command prompt, run the following commands:
```
pip install virtualenv
virtualenv C:\Users\%USERNAME%\Pic2AnkiEnv --python=python3.8
C:\Users\%USERNAME%\Pic2AnkiEnv\Scripts\activate
pip install -r requirements.txt
```
*\*Adapt the path of main.py to where your Pic2Anki folder is* 

4. On https://ocr.space/, create an account that will give you for free 500 requests pre month through an API key. 
5. In `main.py`, replace "MY-API-KEY" by your OCR space key.

## How to Use
1. Put images in the `Input` folder 
2. ~~Run main.bat~~ 
3. In a command prompt, run the following commands:
```
C:\Users\%USERNAME%\Pic2AnkiEnv\Scripts\activate
python main.py
```
*\*Adapt the path of main.py to where your Pic2Anki folder is*  

4. Wait for the two output Excel spreadsheets "words.xlsx" and "verbs.xlsx"

## Packages and services employed:
- nagisa      https://github.com/taishi-i/nagisa 
- googletrans https://pypi.org/project/googletrans/
- Jamdict     https://github.com/neocl/jamdict
- OCRSpace    https://ocr.space/

## Requirements
Requires Python 3.8 for Nagisa
