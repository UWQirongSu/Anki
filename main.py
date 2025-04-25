import os
import re
import argparse

def anki_parse(textFile, tagsFile, searchIdx, tagIdx):  # Entry Point
    print(f"textFile: {textFile}, tagsFile: {tagsFile}, Search Index: {searchIdx}, Tag Index: {tagIdx}")
    
    anki_tagsClear(tagsFile, tagIdx)
    anki_searchAndTag("extras", "chapter1", 1, searchIdx, tagIdx)
    # anki_searchAndTag("extras", "chapter2", 1, searchIdx, tagIdx)
    # anki_searchAndTag("extras", "chapter3", 1, searchIdx, tagIdx)
    # anki_searchAndTag("extras", "chapter4", 1, searchIdx, tagIdx)
    # anki_searchAndTag("extras", "wholeBook", 2, searchIdx, tagIdx)

def anki_getFileList(directory):
    fileList = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            fileList.append(f)
    print(f"Files in directory: {fileList}")
    return fileList

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

def anki_saveWordList(wordList, tagsFile):
    with open(tagsFile, "w", encoding="utf8") as outputFile:
        for word in wordList:
            outputFile.write("\t".join(word))
    print("Word list saved.")

def anki_searchAndTag(directory, tag, requiredCount, wordList, tagsFile, searchIdx, tagIdx):
    fileList = anki_getFileList(directory)
    index = 0
    count = 0
    for word in wordList:
        index += 1
        if len(word) >= tagIdx:
            searchWord = word[searchIdx]
            if isInCorpus(searchWord, fileList, requiredCount):
                tags = word[tagIdx].split(" ")
                if tag not in tags:
                    tags.append(tag)
                    word[tagIdx] = " ".join(tags)
                count += 1
            if index % 500 == 0:
                print(f"{index}: {count}/{index}")
    anki_saveWordList(wordList, tagsFile)

def anki_tagsClear(tagsFile, tagIdx):
    wordList = anki_getWordList(tagsFile)
    for word in wordList:
        word[tagIdx] = ""  # Clear all tags
    anki_saveWordList(wordList, tagsFile)

def anki_removeTag(tag, wordList, tagsFile, tagIdx):
    for word in wordList:
        tags = word[tagIdx].split(" ")
        if tag in tags:
            tags.remove(tag)
        word[tagIdx] = " ".join(tags)
    anki_saveWordList(wordList, tagsFile)

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
