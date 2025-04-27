from tkinter import Tk, Label, Button
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter.messagebox as messagebox

# Assuming these classes are defined in anki.py
from anki import AnkiWord, AnkiDictionary, anki_parse
DBUG = True

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.step = 0  # Track the current step in the process

        self.textFile = ""
        self.dictionaryFile = ""

        self.flashcards = []  # Start with an empty list for flashcards
        self.flashcardIdx = 0
        self.dictionary = AnkiDictionary()  # Create an AnkiDictionary instance

        # Initializing the UI elements
        self.label = Label(root, text="Step 1: Drag a text file here!", width=40, height=10)
        self.label.pack(padx=10, pady=10)

        self.button = Button(root, text="Next", command=self.next_step)
        self.button.pack(padx=10, pady=10)

        self.text_area = Label(root, text="", width=40, height=10)
        self.text_area.pack(padx=10, pady=10)

        # Register drag and drop
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop_file)

    def next_step(self):
        """Function to proceed to the next step based on the current process state."""
        if self.step == 0:  # First step: show instructions for dropping text file
            self.label.config(text="Step 2: Drag a dictionary .tsv file here!")
            self.step = 1  # Move to next step
        elif self.step == 1:  # Second step: start showing flashcards
            self.display_flashcard()

    def drop_file(self, event):
        dropped_path = event.data
        if self.step == 0:  # Waiting for the text file first
            if dropped_path.endswith('.txt'):
                self.read_text_file(dropped_path)
                self.step = 1
            else:
                messagebox.showerror("Error", "Please drop a valid .txt file first.")
        elif self.step == 1:  # Waiting for the dictionary .tsv file
            if dropped_path.endswith('.tsv'):
                self.read_dict_file(dropped_path)
            else:
                messagebox.showerror("Error", "Please drop a valid .tsv file with dictionary data.")
    
    def read_text_file(self, textFilePath):
        self.textFile = textFilePath
        try:
            with open(textFilePath, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_area.config(text=f"Text file loaded successfully!\n\n{content}")
                self.label.config(text="Step 2: Now drop the dictionary .tsv file here!")
        except Exception as e:
            self.text_area.config(text=f"Error reading text file: {e}")

    def read_dict_file(self, dictionaryFilePath):
        self.dictionaryFile = dictionaryFilePath
        try:
            # Load dictionary data into AnkiDictionary instance
            self.dictionary.loadFromFile(dictionaryFilePath)
            self.dictionary.clearTags()
            self.dictionary.tagFromFile(self.textFile, 1)

            if(DBUG):  print(self.dictionary)

            
            # Get 5 random tagged flashcards
            self.flashcards = self.dictionary.getTaggedRand(5)
            if(DBUG):  print(self.flashcards)

            if not self.flashcards:
                messagebox.showwarning("No Data", "The dictionary file is empty or improperly formatted.")
            else:
                self.flashcardIdx = 0
                self.label.config(text="Flashcards are ready! Press 'Next' to start.")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading dictionary file: {e}")

    def display_flashcard(self):
        """Display the current flashcard."""
        if self.flashcards:
            # Get the current flashcard (word object)
            word = self.flashcards.words[self.flashcardIdx]

            # Show the simplified word and prompt for the user to click 'Next' to see more details
            self.text_area.config(text=f"Simplified: {word.simplified}\n\nPress 'Next' to reveal more...")
            self.button.config(text="Show Details", command=self.show_definition)

    def show_definition(self):
        """Show the full details of the current flashcard."""
        if self.flashcards:
            word = self.flashcards.words[self.flashcardIdx]

            # Display the full details: traditional, pronunciation, meaning, etc.
            self.text_area.config(
                text=(
                    f"Simplified: {word.simplified}\n"
                    f"Traditional: {word.traditional}\n"
                    f"Pronunciation: {word.pronunciation}\n"
                    f"Meaning: {word.meaning}\n"
                    f"Translation: {word.translation}\n"
                    f"Extra 1: {word.extra1}\n"
                    f"Extra 2: {word.extra2}\n"
                )
            )

            # After showing the definition, prompt the user to rate their confidence
            self.button.config(text="Next Flashcard", command=self.get_confidence)

    def get_confidence(self):
        """Prompt the user for their confidence level."""
        if self.flashcards.words:  # Ensure that there are words in the flashcards
            word = self.flashcards.words[self.flashcardIdx]

            # Update the text area to ask for the confidence level
            self.text_area.config(
                text=f"How confident are you you'll remember {word.simplified}? (1=low, 5=high):"
            )

            # Hide the current "Next Flashcard" button and show the confidence buttons
            self.button.config(text="Next Flashcard", command=self.next_flashcard)

            # Remove any existing confidence buttons if they exist
            for widget in self.root.winfo_children():
                if isinstance(widget, Button) and widget not in [self.button]:
                    widget.destroy()

            # Create 5 buttons for the user to rate their confidence (1 to 5)
            for i in range(1, 6):
                confidence_button = Button(self.root, text=str(i), command=lambda i=i: self.save_confidence(i))
                confidence_button.pack(side="left", padx=5)

    def save_confidence(self, confidence):
        """Save the user's confidence and move to the next flashcard."""
        if self.flashcards.words:
            word = self.flashcards.words[self.flashcardIdx]
            word.confidence = confidence  # Save the confidence level
            
            # Move to the next flashcard
            self.next_flashcard()  # Go to the next flashcard

    def next_flashcard(self):
        """Move to the next flashcard."""
        if self.flashcards.words:
            self.flashcardIdx += 1
            if self.flashcardIdx >= len(self.flashcards.words):
                self.flashcardIdx = 0  # Start over once all flashcards are shown
                # Display a message that all flashcards are finished
                self.text_area.config(text="Flashcards finished! You've reviewed all the flashcards.")
                self.button.config(text="Restart", command=self.restart_flashcards)
            else:
                self.display_flashcard()  # Show the next flashcard

    def restart_flashcards(self):
        """Restart the flashcards from the beginning."""
        self.flashcardIdx = 0
        self.display_flashcard()
        self.button.config(text="Next", command=self.next_flashcard)



# Create the main window
root = TkinterDnD.Tk()
root.title("Flashcard App")
root.geometry("400x400")

app = FlashcardApp(root)

root.mainloop()
