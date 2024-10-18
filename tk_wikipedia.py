import warnings
from bs4 import GuessedAtParserWarning
warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

from tkinter import *
import wikipedia

class WikipediaSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wikipedia Search")
        
        # Create the interface elements
        self.create_widgets()

    def create_widgets(self):
        # Label frame for search entry
        self.my_label_frame = LabelFrame(self.root, text="Search Wikipedia")
        self.my_label_frame.pack(padx=20, pady=20, fill=X)

        # Entry for the search term
        self.my_entry = Entry(self.my_label_frame)
        self.my_entry.pack(padx=20, pady=20, fill=X)

        # Frame for text area with scrollbars
        self.text_frame = Frame(self.root)
        self.text_frame.pack(padx=20, fill=BOTH, expand=True)

        # Scrollbars for the text area
        self.vertical_scroll = Scrollbar(self.text_frame, orient="vertical")
        self.vertical_scroll.pack(side=RIGHT, fill=Y)

        self.horizontal_scroll = Scrollbar(self.text_frame, orient="horizontal")
        self.horizontal_scroll.pack(side=BOTTOM, fill=X)

        # Text widget for displaying the search results
        self.my_text = Text(self.text_frame, yscrollcommand=self.vertical_scroll.set, 
                            xscrollcommand=self.horizontal_scroll.set, wrap="none")
        self.my_text.pack(fill=BOTH, expand=True)

        self.vertical_scroll.config(command=self.my_text.yview)
        self.horizontal_scroll.config(command=self.my_text.xview)

        # Frame for buttons (Search and Clear)
        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=10)

        self.search_button = Button(self.button_frame, text="Search", font=("Helvetica", 12), 
                                    padx=10, pady=5, command=self.search)
        self.search_button.grid(row=0, column=0, padx=10)

        self.clear_button = Button(self.button_frame, text="Clear", font=("Helvetica", 12), 
                                   padx=10, pady=5, command=self.clear)
        self.clear_button.grid(row=0, column=1, padx=10)

    def clear(self):
        """Clear the text entry and text box."""
        self.my_entry.delete(0, END)
        self.my_text.delete(0.0, END)

    def search(self):
        """Perform the Wikipedia search and display the result."""
        wikipedia.set_lang("en")
        try:
            # Get the search term from the entry
            search_term = self.my_entry.get()
            result = wikipedia.page(search_term)
            self.clear()
            # Insert the summary into the text box
            content_to_display = result.summary
            self.my_text.insert(0.0, content_to_display)
        except wikipedia.exceptions.DisambiguationError as e:
            self.clear()
            self.my_text.insert(0.0, f"Multiple results found: {e.options}")
        except wikipedia.exceptions.PageError:
            self.clear()
            self.my_text.insert(0.0, "No page found for the entered search term.")
        except Exception as e:
            self.clear()
            self.my_text.insert(0.0, f"An error occurred: {e}")

# Create the application window and run the app
if __name__ == "__main__":
    root = Tk()
    app = WikipediaSearchApp(root)
    root.mainloop()
