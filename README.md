# Anki Flashcard Tagging Program

This Python program helps integrate vocabulary learning from a book into Anki, a spaced-repetition flashcard app. The goal is to learn words you encounter while reading a book in the target language using Anki's spaced-repetition system, without constantly looking up words in a dictionary.

## Purpose

This program tags words in an Anki deck based on their presence in a book's text, allowing you to:

- **Learn vocabulary specific to the book you are reading**.
- **Minimize dictionary lookups** by having the words pre-tagged in your Anki deck.
- **Build your vocabulary** using Anki's spaced-repetition system.
- **Learn new words chapter by chapter** without overwhelming yourself with too many new words.

This process helps you read books in the target language more naturally while building your vocabulary over time.

## Features

- **Tagging of flashcards**: The program tags words in your Anki deck that appear in the text, making them easy to learn chapter by chapter.
- **Chapter-based learning**: You learn words specific to each chapter, reducing the cognitive load and helping you focus on relevant vocabulary.
- **Spaced-repetition**: The program leverages Anki's spaced-repetition system to ensure that you review words effectively and build long-term retention.

## Workflow

1. **Prepare your Anki deck**: Export your Anki deck to a CSV format.
2. **Choose a book**: Pick a book you want to read. Ideally, it should be in a .txt format (you can copy-paste if needed).
3. **Sync with Anki**: Feed the book's text and the Anki CSV export into the program.
4. **Tag the vocabulary**: The program will tag the words in your Anki deck based on their occurrences in the book. You can set the tags by chapter, so each chapter’s words are learned individually.
5. **Learn new words**: Unsuspend words in Anki that appear in the current chapter and learn them using the spaced-repetition system.
6. **Repeat the process** for each chapter and book, gradually building your vocabulary.

### Important Notes

- **Text Format**: The book should be in plain .txt format for best results.
- **Anki Deck**: Your Anki deck should be exported in CSV format and contain the vocabulary words you want to tag.
- **Language Support**: The program was originally designed to work with Chinese but could be adapted for other languages with additional tweaks.

## Features Yet to Be Implemented

- **Lemmatization**: While the program currently works for Chinese, it has not been fully implemented for languages like Spanish or other Germanic languages. The ability to handle lemmas (base forms of words) is still under development.
- **OCR for Comics**: There are plans to expand the program to extract text from comics using OCR, allowing language learners to learn vocabulary from visual media such as comics or movies.

## How to Use

### Prerequisites

- **Python 3.x**: The program is written in Python and requires Python 3.x.
- **Anki**: You must have Anki installed and use it for vocabulary learning.

### Running the Program

1. Export your Anki deck to a CSV file.
2. Prepare your book in .txt format (you can copy-paste from any source).
3. Run the Python program with the text file and the Anki CSV file as input:

```bash
python anki_flashcard_tagging.py textFile.txt ankiExport.csv 7 6
```
