import os
import re
import argparse

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
def anki_parse(textFile, tagsFile, searchIdx, tagIdx):
    print(f"textFile: {textFile}, tagsFile: {tagsFile}, Search Index: {searchIdx}, Tag Index: {tagIdx}")
    
    wordList = anki_getWordList(tagsFile)  # Get the word list
    anki_tagsClear(tagsFile, tagIdx)  # Clear tags first
    anki_searchAndTag(textFile, "chapter1", 1, wordList, tagsFile, searchIdx, tagIdx)  # Pass wordList and tagsFile
    # You can call the other chapters here if needed
    # anki_searchAndTag(textFile, "chapter2", 1, wordList, tagsFile, searchIdx, tagIdx)
    # anki_searchAndTag(textFile, "chapter3", 1, wordList, tagsFile, searchIdx, tagIdx)
    # anki_searchAndTag(textFile, "chapter4", 1, wordList, tagsFile, searchIdx, tagIdx)
    # anki_searchAndTag(textFile, "wholeBook", 2, wordList, tagsFile, searchIdx, tagIdx)

'''
def anki_getFileList(directory):
Inputs:
    char[] directory : A directory or file path to search for files. If it's a directory, it returns a list of all file paths inside the directory. If it's a file, it adds that file to the list.

Outputs:
    char[][] fileList : A list of file paths (strings) found in the provided directory or the single file if the path is a file.

Purpose:
This function takes a directory or file path and returns a list of file paths. If a directory is passed, it lists all files inside the directory. If a file is passed, it just returns that file in a list.
'''
def anki_getFileList(directory):
    fileList = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            fileList.append(f)
    print(f"Files in directory: {fileList}")
    return fileList

'''
def anki_getWordList(tagsFile):
Inputs:
    char[] tagsFile : The path to the TSV file that contains the word list. Each line is expected to have tab-separated values representing different fields like the word itself and its tag.

Outputs:
    char[][] wordList : A list of lists, where each inner list represents a word entry and contains the columns from the TSV file (like word, translation, tag, etc.).

Purpose:
This function reads the tagsFile (TSV file) and extracts the words and their associated data into a list of lists. It parses each line of the TSV file into columns, handles newline characters, and returns the parsed word list.
'''
def anki_getWordList(tagsFile):
    wordList = []
    with open(tagsFile, encoding="utf8") as wordListFile:
        for line in wordListFile.readlines():
            cells = line.split("\t")
            if cells[-1] != "\n":
                cells[-1] = cells[-1].strip("\n")
                cells.append("\n")
            wordList.append(cells)
    print(f"Word list length: {len(wordList)}")
    print(f"First word entry: {wordList[0]}")
    return wordList

'''
anki_saveWordList(wordList, tagsFile):
Inputs:
    char[][] wordList : A list of word entries to save back to the TSV file. Each entry is a list of columns that correspond to different fields (word, translation, tag, etc.).
    char[] tagsFile : The path to the TSV file where the word list should be saved.

Outputs:
    void : This function does not return any value but saves the updated wordList to the tagsFile.

Purpose:
This function writes the wordList back to the provided tagsFile in a tab-separated format, effectively updating the file with new tags or other modifications.
'''
def anki_saveWordList(wordList, tagsFile):
    with open(tagsFile, "w", encoding="utf8") as outputFile:
        for word in wordList:
            outputFile.write("\t".join(word))
    print("Word list saved.")

'''
def anki_searchAndTag(directory, tag, requiredCount, wordList, tagsFile, searchIdx, tagIdx):
Inputs:
    char[] directory : The directory or file path where the corpus (text file) is located.
    char[] tag : The tag to be added to the words in the wordList if they appear in the textFile.
    int requiredCount : The number of times a word needs to appear in the textFile to be tagged.
    char[][] wordList : The word list (from the TSV file) that contains the words and their current tags.
    char[] tagsFile : The path to the TSV file that contains the word list.
    int searchIdx : The index in each word entry where the search term (the word to find in the corpus) is located.
    int tagIdx : The index in each word entry where the tags are stored.

Outputs:
    void : This function does not return any value but modifies the wordList by adding the tag to the words that appear requiredCount times in the textFile. The updated wordList is saved to the tagsFile.

Purpose:
This function searches for each word in the wordList within the corpus (textFile). If a word appears at least requiredCount times in the textFile, it adds the specified tag to that word's tag field in the wordList. After processing, it saves the updated word list back to the tagsFile.
'''
def anki_searchAndTag(directory, tag, requiredCount, wordList, tagsFile, searchIdx, tagIdx):
    fileList = anki_getFileList(directory)
    index = 0
    count = 0
    for word in wordList:
        index += 1
        if len(word) >= tagIdx:
            searchWord = word[searchIdx]
            if anki_isInCorpus(searchWord, fileList, requiredCount):
                tags = word[tagIdx].split(" ")
                if tag not in tags:
                    tags.append(tag)
                    word[tagIdx] = " ".join(tags)
                count += 1
            if index % 500 == 0:
                print(f"{index}: {count}/{index}")
    anki_saveWordList(wordList, tagsFile)

'''
def anki_tagsClear(tagsFile, tagIdx):
Inputs:
    char[] tagsFile : The path to the TSV file that contains the word list.
    int tagIdx : The index in each word entry where the tags are stored.

Outputs:
    void : This function does not return any value but clears all tags in the tagsFile by setting the tag field (at index tagIdx) for all words to an empty string.

Purpose:
This function clears all tags in the tagsFile. It reads the file, and for each word entry, it resets the tags field to an empty string. Afterward, the word list is saved back to the file.
'''
def anki_tagsClear(tagsFile, tagIdx):
    wordList = anki_getWordList(tagsFile)
    for word in wordList:
        word[tagIdx] = ""  # Clear all tags
    anki_saveWordList(wordList, tagsFile)

'''
def anki_removeTag(tag, wordList, tagsFile, tagIdx):
Inputs:
    char[] tag : The tag to be removed from the word entries.
    char[][] wordList : The word list (from the TSV file) that contains the words and their current tags.
    char[] tagsFile : The path to the TSV file that contains the word list.
    int tagIdx : The index in each word entry where the tags are stored.

Outputs:
    void : This function does not return any value but removes the specified tag from the word list and saves the updated list to the tagsFile.

Purpose:
This function removes the specified tag from the tags field of each word entry in the wordList. Afterward, the updated word list is saved back to the tagsFile.
'''
def anki_removeTag(tag, wordList, tagsFile, tagIdx):
    for word in wordList:
        tags = word[tagIdx].split(" ")
        if tag in tags:
            tags.remove(tag)
        word[tagIdx] = " ".join(tags)
    anki_saveWordList(wordList, tagsFile)

'''
def anki_isInCorpus(word, fileList, requiredCount):
Inputs:
    char[] word : The word to search for in the corpus (text file).
    char[][] fileList : The list of file paths (text files) to search through.
    int requiredCount : The minimum number of occurrences of the word in the corpus required to consider it found.

Outputs:
    True (bool): If the word appears in the corpus at least requiredCount times.
    False (bool): If the word does not appear in the corpus the required number of times.

Purpose:
This function checks whether a given word appears in any of the files in fileList at least requiredCount times. It returns True if the word meets the required count, otherwise, it returns False.
'''
def anki_isInCorpus(word, fileList, requiredCount):
    wordCount = 0
    for fileName in fileList:
        with open(fileName, encoding="utf8") as file:
            wordCount += file.read().count(word)
            if wordCount >= requiredCount:
                return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tag words from a TSV file based on their presence in a text corpus.")
    parser.add_argument("text_file", help="Path to the text file used as the corpus.")
    parser.add_argument("tsv_file", help="Path to the TSV wordlist file (input and output).")
    parser.add_argument("search_index", type=int, help="The index for searching words in the word list.")
    parser.add_argument("tag_index", type=int, help="The index for tagging words in the word list.")
    
    args = parser.parse_args()

    # Running the parse function with the arguments provided
    anki_parse(args.text_file, args.tsv_file, args.search_index, args.tag_index)
