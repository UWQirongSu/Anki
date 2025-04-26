import unittest
from unittest.mock import patch, mock_open
import sys
import os
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Add the root directory to the Python path
from anki import AnkiWord, AnkiDictionary, anki_parse

class TestAnkiDictionary(unittest.TestCase):

    def setUp(self):
        # Runs before each test
        self.d = AnkiDictionary()
        self.w1 = AnkiWord("001", "你", "妳", "nǐ", "you", "you (singular)", "", "", False)
        self.w2 = AnkiWord("002", "好", "", "hǎo", "good", "good", "", "", False)
        self.d.words = [self.w1, self.w2]

    def test_clearTags(self):
        # Ensure clearTags clears all tags
        self.w1.tag = True
        self.w2.tag = True
        self.d.clearTags()
        self.assertFalse(self.w1.tag)
        self.assertFalse(self.w2.tag)

    def test_tagFromFile(self):
        # Test tagging words from a file
        with patch("builtins.open", mock_open(read_data="你好你好")):
            self.d.tagFromFile("temp.txt", requiredCount=2)
        self.assertTrue(self.w1.tag)
        self.assertTrue(self.w2.tag)

    def test_tagsAndNot(self):
        # Ensure tagsAndNot works as expected
        history = AnkiDictionary()
        history.words = [AnkiWord("001", "你", "妳", "", "", "", "", "", False)]
        self.w1.tag = True
        self.d.tagsAndNot(history)
        self.assertFalse(self.w1.tag)

    def test_tagsOr(self):
        # Ensure tagsOr works as expected
        history = AnkiDictionary()
        self.w1.tag = True
        self.d.tagsOr(history)
        self.assertIn(self.w1, history.words)

    def test_getTagged(self):
        # Ensure getTagged returns only tagged words
        self.w1.tag = True
        tagged = self.d.getTagged()
        self.assertIn(self.w1, tagged)
        self.assertNotIn(self.w2, tagged)

    def test_appendWords(self):
        # Test appending words to the dictionary
        new_word = AnkiWord("003", "是", "", "", "", "", "", "", False)
        self.d.appendWords([new_word])
        self.assertIn(new_word, self.d.words)

    def test_addWord(self):
        # Test adding a single word to the dictionary
        new_word = AnkiWord("004", "不", "", "", "", "", "", "", False)
        self.d.addWord(new_word)
        self.assertIn(new_word, self.d.words)

    def test_wordFromId(self):
        # Test retrieving a word by ID
        found = self.d.wordFromId("001")
        self.assertEqual(found, self.w1)

    def test_loadFromFile_and_saveAllToFile(self):
        # Test loading from and saving to a file
        self.d.saveAllToFile("test_output.tsv")
        self.d.words = []  # Clear the words
        self.d.loadFromFile("test_output.tsv")
        self.assertEqual(len(self.d.words), 2)

    def test_saveTrueToFile(self):
        # Test saving only tagged words to file
        self.w1.tag = True
        self.d.saveTrueToFile("test_true.tsv")
        with open("test_true.tsv", encoding="utf-8") as f:
            contents = f.read()
            self.assertIn("你", contents)
            self.assertNotIn("好", contents)


# class TestAnkiParseFunction(unittest.TestCase):
    # @patch("builtins.open", new_callable=mock_open, read_data="你好你好")
    # def test_anki_parse(self, mock_file):
    #     # Assuming you are testing anki_parse
    #     text_files = ["text1.txt"]
    #     dictionary_file = "mock_tsv.tsv"
    #     required_count = 2
    #     history_file = "mock_history.tsv"
    #     disable_history = False
    #     debug = False
        
    #     # Call the function you want to test
    #     anki_parse(text_files, dictionary_file, required_count, history_file, disable_history, debug)
        
    #     # Assert the file is being opened with the correct parameters
    #     mock_file.assert_called_with("text1.txt", encoding="utf-8")
        
    # @patch("builtins.open", new_callable=mock_open, read_data="你好你好")
    # def test_anki_parse_history_disabled(self, mock_file):
    #     # Adjust test parameters
    #     text_files = ["text1.txt"]
    #     dictionary_file = "mock_tsv.tsv"
    #     required_count = 2
    #     history_file = "mock_history.tsv"
    #     disable_history = True
    #     debug = True
        
    #     # Call the function with the updated arguments
    #     anki_parse(text_files, dictionary_file, required_count, history_file, disable_history, debug)
        
    #     # Add assertions based on what you expect the behavior to be
    #     mock_file.assert_called_with("text1.txt", encoding="utf-8")

if __name__ == "__main__":
    unittest.main()
