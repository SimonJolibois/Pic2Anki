# Pic2Excel
Take pictures of Japanese text, and process everything in a Excel spreadsheet that can be used to create Anki decks.

### Packages employed:
- nagisa      https://github.com/taishi-i/nagisa 
- googletrans https://pypi.org/project/googletrans/
- Jamdict     https://github.com/neocl/jamdict

### Requirements
Requires Python 3.8 for Nagisa
For now .bat suppose you are using conda

## How to Install
1. Git clone the repository
2. Run `install_conda.bat` which will create an environnement "OCR_japonais" and install required packages of `requirements.txt`

### How to Use
1. Put images in the `Input` folder
2. Run main.bat
3. Wait for the two output Excel spreadsheets "words.xlsx" and "verbs.xlsx"

