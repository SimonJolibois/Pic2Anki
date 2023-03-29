# Pic2Anki
Take pictures of Japanese text, and process everything in a Excel spreadsheet that can be used to create Anki decks.

### Packages and services employed:
- nagisa      https://github.com/taishi-i/nagisa 
- googletrans https://pypi.org/project/googletrans/
- Jamdict     https://github.com/neocl/jamdict
- OCRSpace    https://ocr.space/

### Requirements
Requires Python 3.8 for Nagisa
For now .bat suppose you are using conda

## How to Install
Seems like the .bat files don't for some reasons. For now, here is the workflow:
1. Git clone the repository  
~~2. Run install.bat to create a virtual environnement install all required packages~~

2. In a command prompt, run the following commands:
```
pip install virtualenv
virtualenv C:\Users\%USERNAME%\Pic2AnkiEnv --python=python3.8
C:\Users\%USERNAME%\Pic2AnkiEnv\Scripts\activate
pip install -r requirements.txt
```
*\*Adapt the path of main.py to where your Pic2Anki folder is*  
3. On https://ocr.space/, create an account that will give you for free 500 requests pre month through an API key.
4. In `main.py`, replace "MY-API-KEY" by your OCR space key.

### How to Use
1. Put images in the `Input` folder  
~~2. Run main.bat~~

2. In a command prompt, run the following commands:
```
C:\Users\%USERNAME%\Pic2AnkiEnv\Scripts\activate
python main.py
```
*\*Adapt the path of main.py to where your Pic2Anki folder is*  
3. Wait for the two output Excel spreadsheets "words.xlsx" and "verbs.xlsx"

