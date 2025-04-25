# Anki Flashcard Tagging Program

This Python program helps integrate vocabulary learning from a book into Anki, a spaced-repetition flashcard app. The goal is to learn words you encounter while reading a book in the target language using Anki's spaced-repetition system, without constantly looking up words in a dictionary.

## Purpose

This program tags words in an Anki deck based on their presence in a book's text, allowing you to:

- **Learn vocabulary specific to the book you are reading**.
- **Minimize dictionary lookups** by having the words pre-tagged in your Anki deck.
- **Build your vocabulary** using Anki's spaced-repetition system.
- **Learn new words chapter by chapter** without overwhelming yourself with too many new words.

## Intended Workflow

1. **Prepare your Anki deck**: Export your Anki deck to a TSV format.
2. **Choose a book**: Pick a book you want to read. Ideally, it should be in a .txt format (you can copy-paste if needed).
3. **Tag the vocabulary**: The program will tag the words in your Anki deck based on their occurrences in the book. You can set the tags by chapter, so each chapter’s words are learned individually.
4. **Learn new words**: Review words in Anki that appear in the current chapter and learn them using the spaced-repetition system.
5. **Read The Book With Minimal Dictionary Use** Enjoy the content of the book without needing to refer to a dictionary

### Important Notes

- **Text Format**: The book should be in plain .txt format for now
- **Anki Deck**: Your Anki deck should be exported in TSV format and contain the vocabulary words you want to tag.
- **Language Support**: The program was originally designed to work with Chinese but could be adapted for other languages with additional tweaks.

## Features Yet to Be Implemented

- **Lemmatization**: While the program currently works for Chinese, it has not been fully implemented for languages like Spanish or other Germanic languages. The ability to handle lemmas (base forms of words) is still under development.
- **OCR for Comics**: There are plans to expand the program to extract text from comics using OCR, allowing language learners to learn vocabulary from visual media such as comics or movies.
- **Single Executable**: It would be ideal for this program to be able to be compiled into a single executable for all platforms

## How to Use

### Running the Program

1. Export your Anki deck to a TSV file.
2. Prepare your book in .txt format (you can copy-paste from any source).
3. Run the Python program with the text file and the Anki TSV file as input:

```bash
python anki.py assets/text.txt assets/dictionary.tsv 7 6
```
