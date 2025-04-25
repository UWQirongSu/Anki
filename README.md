# Anki Flashcard Tagging Program

This Python program helps integrate vocabulary learning from a book into Anki, a spaced-repetition flashcard app. The goal is to learn words you encounter while reading a book in the target language using Anki's spaced-repetition system, without constantly looking up words in a dictionary.

## Purpose

This program tags words in an Anki deck based on their presence in a book's text, allowing you to:

- **Learn vocabulary specific to the book you are reading**.
- **Minimize dictionary lookups** by having the words pre-tagged in your Anki deck.
- **Build your vocabulary** using Anki's spaced-repetition system.
- **Learn new words chapter by chapter** without overwhelming yourself with too many new words.

## Intended Workflow

1. **Pick a Book To Read**: Get the text in .txt format.
2. **Tag the vocabulary**: The program will tag the words in your Anki deck based on their occurrences in the book. You can set the tags by chapter, so each chapter’s words are learned individually.
3. **Learn new words**: Learn words in Anki that appear in the current chapter and learn them using the spaced-repetition system.
4. **Read The Book With Minimal Dictionary Use** Enjoy the content of the book without needing to refer to a dictionary
5. **Review Saved Words** Words get saved into the Anki History and new books will exclude these words.

### Important Notes

- **Text Format**: The book should be in plain .txt format for now
- **Anki Deck**: Your Anki deck should be exported in TSV format and contain the vocabulary words you want to tag.
- **Language Support**: The program was originally designed to work with Chinese but could be adapted for other languages with additional tweaks.

## Features Yet to Be Implemented

- **Lemmatization**: While the program currently works for Chinese, it has not been fully implemented for languages like Spanish or other Germanic languages. The ability to handle lemmas (base forms of words) is still under development.
- **OCR for Comics**: There are plans to expand the program to extract text from comics using OCR, allowing language learners to learn vocabulary from visual media such as comics or movies.
- **Single Executable**: It would be ideal for this program to be able to be compiled into a single executable for ALL platforms (currently single executable available only for windows)

## How to Use

### Basic Command

```bash
python anki.py <text_file> <_tsv_file>
```

Parameters:
<text_file>: Path to the text file (corpus) that contains the content to search for words.
<tsv_file>: Path to the TSV file containing the word list. This file is both an input and output (it holds the words and their tags).

### Flags

- `-history <history_file>`:  
  **Optional**. Path to a TSV file that stores previously learned words. This file helps ensure that you don't tag words you've already learned in the past. if unspecified, it defaults to anki_history.tsv. Can be disabled with the `--disable-history` flag.

- `--disable-history`:  
  **Optional**. Disables storing history. If used, the program will not update or use the history file.

- `--required-count <number>`:  
  **Optional**. The minimum number of occurrences required for a word to be tagged. By default, it is set to `1`.

### Example 1: Basic Usage

```bash
python anki.py assets/text.txt assets/dictionary.tsv
```

### Example 2: With History

```bash
python anki.py assets/text.txt assets/dictionary.tsv -history assets/ankihistory.tsv
```

### Example 3: With Required Count

```bash
python anki.py assets/text.txt assets/dictionary.tsv --required-count 3

```

### Example 4: With Disabled History

```bash
python anki.py assets/text.txt assets/dictionary.tsv --disable-history


```
