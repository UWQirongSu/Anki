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

class AnkiWordList:
    def __init__(self):
        self.words = []  # List to store AnkiWord objects

    def clearTags(self):
        for word in self.words:
            word.tag = False

    def tagFromFile(self, file_name, requiredCount: int):
        # Count character occurrences
        with open(file_name, encoding="utf-8") as f:
            text = f.read()

        for word in self.words:
            # Count how many times either form appears
            simplified_count = text.count(word.simplified)
            traditional_count = text.count(word.traditional)

            total_count = simplified_count + traditional_count
            word.tag = total_count >= requiredCount

            # if word.tag:
                # print(f"FOUND: {word.simplified}/{word.traditional} appeared {total_count} times")


    def addWord(self, word):
        if isinstance(word, AnkiWord):
            self.words.append(word)
        else:
            print("Only AnkiWord instances can be added")

    def wordFromId(self, word_id):
        for word in self.words:
            if word.id == word_id:
                return word
        return None

    def loadFromFile(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                for line_num, line in enumerate(file, start=1):
                    # print(f"Line {line_num}: {line.strip()}")
                    parts = line.strip().split("\t")
                    if len(parts) != 9:
                        print(f"Skipping line {line_num} due to incorrect number of fields ({len(parts)}).")
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


    def saveToFile(self, file_name):
        # Save the word list to a TSV file
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                for word in self.words:
                    file.write(f"{word.id}\t{word.simplified}\t{word.traditional}\t{word.pronunciation}\t{word.meaning}"
                            f"\t{word.translation}\t{word.extra1}\t{word.extra2}\t{word.tag}\n")
        except Exception as e:
            print(f"Error saving to file {file_name}: {e}")


    def __repr__(self):
        return f"AnkiWordList with {len(self.words)} words"

'''
def anki_parse(textFile, tagsFile, searchIdx, tagIdx):
Inputs:
    char[] textFile : The path to the text file (corpus) that contains the content to search for words.
    char[] tagsFile : The path to the TSV file containing the word list. This file is both an input and an output (it holds the words and their tags).
    int searchIdx : The index in the TSV file where the word to search for in the corpus is located.
    int tagIdx : The index in the TSV file where the tag is stored.

Outputs: 
    void : (modifies the tagsFile by updating the tags based on the words found in the textFile)

Purpose:
This is the entry point of the program. It first clears any tags in the tagsFile using anki_tagsClear(), then searches for words in the textFile using anki_searchAndTag(). 
After this, the tags in the TSV file are updated accordingly.
'''
def anki_parse(textFile, dictionaryFile, searchIdx, tagIdx):
    # add input validation
    print(f"textFile: {textFile}, dictionaryFile: {dictionaryFile}, Search Index: {searchIdx}, Tag Index: {tagIdx}")

    dictionary = AnkiWordList()
    dictionary.loadFromFile(dictionaryFile)
    print(dictionary)
    dictionary.clearTags()
    requiredCount = 1
    dictionary.tagFromFile(textFile, requiredCount)
    dictionary.saveToFile(dictionaryFile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tag words from a TSV file based on their presence in a text corpus.")
    parser.add_argument("text_file", help="Path to the text file used as the corpus.")
    parser.add_argument("tsv_file", help="Path to the TSV wordlist file (input and output).")
    parser.add_argument("search_index", type=int, help="The index for searching words in the word list.")
    parser.add_argument("tag_index", type=int, help="The index for tagging words in the word list.")
    args = parser.parse_args()

    # Running the parse function with the arguments provided
    anki_parse(args.text_file, args.tsv_file, args.search_index, args.tag_index)
