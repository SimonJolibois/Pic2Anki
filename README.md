# Pic2Excel
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
1. Git clone the repository
2. Run `install_conda.bat` which will create an environnement "OCR_japonais" and install required packages of `requirements.txt`
3. On https://ocr.space/, create an account that will give you for free 500 requests pre month through an API key.
4. In `main.py`, replace "MY-API-KEY" by your OCR space key.

### How to Use
1. Put images in the `Input` folder
2. Run main.bat
3. Wait for the two output Excel spreadsheets "words.xlsx" and "verbs.xlsx"

