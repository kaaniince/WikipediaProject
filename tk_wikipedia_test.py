import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
from tk_wikipedia import WikipediaSearchApp 

class TestWikipediaSearchApp(unittest.TestCase):

    def setUp(self):
        """Set up the Tkinter app instance for testing."""
        self.root = Tk()
        self.app = WikipediaSearchApp(self.root)

    def tearDown(self):
        """Destroy the Tkinter window after each test."""
        self.root.destroy()

    @patch('wikipedia.page')
    def test_search_success(self, mock_wikipedia_page):
        """Test successful search result."""
        mock_result = MagicMock()
        mock_result.summary = "This is a summary."
        mock_wikipedia_page.return_value = mock_result

        self.app.my_entry.insert(0, "Python")
        self.app.search()
        self.assertIn("This is a summary.", self.app.my_text.get("1.0", "end-1c"))

    @patch('wikipedia.page', side_effect=DisambiguationError("Python", ["Python (programming)", "Python (mythology)"]))
    def test_search_disambiguation_error(self, mock_wikipedia_page):
        """Test disambiguation error handling."""
        self.app.my_entry.insert(0, "Python")
        self.app.search()
        self.assertIn("Multiple results found", self.app.my_text.get("1.0", "end-1c"))

    @patch('wikipedia.page', side_effect=PageError("Page not found"))
    def test_search_page_error(self, mock_wikipedia_page):
        """Test page error handling when no page is found."""
        self.app.my_entry.insert(0, "NonExistentPage")
        self.app.search()
        self.assertIn("No page found", self.app.my_text.get("1.0", "end-1c"))

    @patch('wikipedia.page', side_effect=Exception("Unknown error"))
    def test_search_unknown_error(self, mock_wikipedia_page):
        """Test handling of a generic unknown error."""
        self.app.my_entry.insert(0, "SomeTerm")
        self.app.search()
        self.assertIn("An error occurred: Unknown error", self.app.my_text.get("1.0", "end-1c"))

    def test_clear(self):
        """Test that the clear button works correctly."""
        self.app.my_text.insert(0.0, "Some text to clear")
        self.app.clear()
        self.assertEqual(self.app.my_text.get("1.0", "end-1c"), "")

if __name__ == "__main__":
    unittest.main()
