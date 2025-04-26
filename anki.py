import os
import re
import argparse

class AnkiWord:
    def __init__(self, id, simplified, traditional, pronunciation, meaning, translation, extra1, extra2, tag):
        self.id = id  # ID of the word
        self.simplified = simplified  # Simplified Chinese word
        self.traditional = traditional  # Traditional Chinese word
        self.pronunciation = pronunciation  # Pinyin pronunciation
        self.meaning = meaning  # Meaning of the word in another language
        self.translation = translation  # English translation
        self.extra1 = extra1  # Some extra field (e.g., tags or notes)
        self.extra2 = extra2  # Another extra field
        self.tag = tag  # Boolean tag for tracking if the word meets appearance threshold

    def __repr__(self):
        return f"AnkiWord(id={self.id}, simplified={self.simplified}, traditional={self.traditional}, " \
               f"pronunciation={self.pronunciation}, meaning={self.meaning}, translation={self.translation})"

class AnkiDictionary:
    def __init__(self):
        self.words = []  # List to store AnkiWord objects

    def clearTags(self):
        if not isinstance(self.words, list):
            print("self.words must be a list")
            return
        for word in self.words:
            if hasattr(word, 'tag'):
                word.tag = False

    def tagFromFile(self, file_name, requiredCount: int):
        if not isinstance(file_name, str):
            print("file_name must be a string")
            return
        if not isinstance(requiredCount, int) or requiredCount < 0:
            print("requiredCount must be a non-negative integer")
            return

        try:
            with open(file_name, encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
            return

        for word in self.words:
            # Count how many times either form appears
            simplified_count = text.count(word.simplified)
        
            # Set traditional_count to zero if word.traditional is an empty string
            if word.traditional != "":
                traditional_count = text.count(word.traditional)
            else:
                traditional_count = 0

            total_count = simplified_count + traditional_count
            if(total_count >= requiredCount):
                word.tag = True
                # print(f"FOUND: {word.simplified}/{word.traditional} appeared {total_count} times")

    def tagsAndNot(self, history):
        if not isinstance(history, type(self)):
            print("history must be an instance of the same class")
            return

        known_words = set()
        for word in history.words:
            known_words.add(word.simplified)
            if word.traditional:
                known_words.add(word.traditional)

        for word in self.words:
            if word.tag and (word.simplified in known_words or word.traditional in known_words):
                word.tag = False

    def tagsOr(self, history):
        if not isinstance(history, type(self)):
            print("history must be an instance of the same class")
            return

        new_words = [word for word in self.words if word.tag and word not in history.words]
        history.appendWords(new_words)

    def getTagged(self):
        if not isinstance(self.words, list):
            print("self.words must be a list")
            return []
        return [word for word in self.words if getattr(word, "tag", False)]

    def appendWords(self, new_words):
        if not isinstance(new_words, list):
            print("Input should be a list of AnkiWord instances")
            return

        for word in new_words:
            if isinstance(word, AnkiWord):
                self.words.append(word)
            else:
                print("Only AnkiWord instances can be added")


    def addWord(self, word):
        if isinstance(word, AnkiWord):
            self.words.append(word)
        else:
            print("Only AnkiWord instances can be added")

    def wordFromId(self, word_id):
        if not isinstance(word_id, str):
            print("word_id must be a string")
            return None
        for word in self.words:
            if word.id == word_id:
                return word
        return None

    def loadFromFile(self, file_name):
        if not isinstance(file_name, str):
            print("file_name must be a string")
            return

        try:
            with open(file_name, "r", encoding="utf-8") as file:
                for line_num, line in enumerate(file, start=1):
                    # print(f"Line {line_num}: {line.strip()}")
                    parts = line.strip().split("\t")
                    if len(parts) != 9:
                        # print(f"Skipping line {line_num} due to incorrect number of fields ({len(parts)}).")
                        continue

                    # Convert string "True"/"False" to boolean
                    tag = parts[8].strip().lower() == "true"

                    word = AnkiWord(
                        id=parts[0],
                        simplified=parts[1],
                        traditional=parts[2],
                        pronunciation=parts[3],
                        meaning=parts[4],
                        translation=parts[5],
                        extra1=parts[6],
                        extra2=parts[7],
                        tag=tag  # must match the param in your AnkiWord constructor
                    )
                    self.addWord(word)
        except Exception as e:
            print(f"Error loading file {file_name}: {e}")


    def saveAllToFile(self, file_name):
        if not isinstance(file_name, str):
            print("file_name must be a string")
            return
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                for word in self.words:
                    file.write(f"{word.id}\t{word.simplified}\t{word.traditional}\t{word.pronunciation}\t{word.meaning}"
                            f"\t{word.translation}\t{word.extra1}\t{word.extra2}\t{word.tag}\n")
        except Exception as e:
            print(f"Error saving to file {file_name}: {e}")


    def saveTrueToFile(self, file_name):
        # Save only tagged words to a TSV file
        if not isinstance(file_name, str):
            print("file_name must be a string")
            return
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                for word in self.words:
                    if not getattr(word, 'tag', False):
                        continue
                    file.write(f"{word.id}\t{word.simplified}\t{word.traditional}\t{word.pronunciation}\t{word.meaning}"
                            f"\t{word.translation}\t{word.extra1}\t{word.extra2}\t{word.tag}\n")
        except Exception as e:
            print(f"Error saving to file {file_name}: {e}")



    def __repr__(self):
        return f"AnkiDictionary with {len(self.words)} words"

'''
def anki_parse(textFiles, dictionaryFile, requiredCount):
Inputs:
    char[] textFile : The path to the text file (corpus) that contains the content to search for words.
    char[] dictionaryFile : The path to the TSV file containing the word list. This file is both an input and an output (it holds the words and their tags).
    int requiredCount : The number of times a word has to show up in the text in order for it to be considered tagged

Outputs: 
    void : (modifies the tagsFile by updating the tags based on the words found in the textFile)

Purpose:
This is the entry point of the program. It first clears any tags in the tagsFile using AnkiWord.clearTags(), then searches for words in the textFile using AnkiWord.tagFromFile(). 
After this, the tags in the TSV file are updated accordingly.
'''
def anki_parse(textFiles, dictionaryFile, requiredCount, historyFile, disableHistoryFlag, debug=False):
    # Input validation
    if not textFiles:
        raise ValueError("At least one text file must be provided.")

    for path in textFiles:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Text file not found: {path}")

    if not os.path.isfile(dictionaryFile):
        raise FileNotFoundError(f"Dictionary file not found: {dictionaryFile}")

    if requiredCount < 0:
        raise ValueError("requiredCount must be non-negative.")

    if historyFile and not disableHistoryFlag and os.path.exists(historyFile):
        if not os.access(historyFile, os.R_OK | os.W_OK):
            raise PermissionError(f"Cannot read/write history file: {historyFile}")

    if(debug):  print(f"textFiles: {textFiles}, dictionaryFile: {dictionaryFile}, requiredCount: {requiredCount}, disableHistoryFlag: {disableHistoryFlag}")
    
    dictionary = AnkiDictionary()
    dictionary.loadFromFile(dictionaryFile)
    dictionary.clearTags()
    for textFile in textFiles:
        dictionary.tagFromFile(textFile, requiredCount)

    if(debug):  print(dictionary)
    

    if historyFile and not disableHistoryFlag:
        history = AnkiDictionary()
        if os.path.exists(historyFile): # Check if history file exists, if not initialize an empty history
            history.loadFromFile(historyFile)
            dictionary.tagsAndNot(history)
            if(debug):  print(history)
            
        else:
            if(debug):  print(f"History file {historyFile} does not exist. Starting with an empty history.")

        history.appendWords(dictionary.getTagged())  # Add new learned words to history
        history.saveTrueToFile(historyFile)  # Save the updated history

    dictionary.saveAllToFile(dictionaryFile)

    if(not disableHistoryFlag):
        history.appendWords(dictionary.getTagged()) # add the new learned words to the history
        history.saveTrueToFile(historyFile) # History of learned words

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tag words from a TSV file based on their presence in a text corpus.")
    parser.add_argument("text_file", nargs='+', help="Path to the text files used as the corpus.")
    parser.add_argument("tsv_file", help="Path to the TSV wordlist file (input and output).")
    parser.add_argument("-history", type=str, default="anki_history.tsv", help="Optional path to a TSV file that stores previously learned words")
    parser.add_argument("--disable-history", action="store_true", help="Disable storing history")
    parser.add_argument("--required-count", type=int, default=1, help="Minimum number of occurrences required to tag a word. (default: 1)")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    # Running the parse function with the arguments provided
    anki_parse(args.text_file, args.tsv_file, args.required_count, args.history, args.disable_history, args.debug)
