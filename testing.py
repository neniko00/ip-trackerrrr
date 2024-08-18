import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import json
import urllib.request
import webbrowser
import os

from main import IPAddressLocatorGUI

class TestIPAddressLocatorGUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = IPAddressLocatorGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('urllib.request.urlopen')
    def test_fetch_ip_details_success(self, mock_urlopen):
        # Mock the response of the URL request
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "query": "8.8.8.8",
            "country": "United States",
            "regionName": "California",
            "city": "Mountain View",
            "lat": 37.386,
            "lon": -122.0838,
            "org": "Google LLC"
        }).encode('utf-8')
        mock_urlopen.return_value = mock_response

        # Test fetching IP details for system IP
        self.app.fetch_ip_details('http://ip-api.com/json/')
        self.assertIn('IP ADDRESS: 8.8.8.8', self.app.text_area.get(1.0, tk.END))

    @patch('urllib.request.urlopen')
    def test_fetch_ip_details_failure(self, mock_urlopen):
        # Mock a URL error
        mock_urlopen.side_effect = urllib.error.URLError('Error')

        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.app.fetch_ip_details('http://ip-api.com/json/')
            mock_showerror.assert_called_with("Error", "Please check your internet connection!")

    @patch('pyperclip.copy')
    def test_copy_to_clipboard(self, mock_pyperclip):
        self.app.text_area.insert(tk.END, "Test content")
        self.app.copy_to_clipboard()
        mock_pyperclip.assert_called_with("Test content\n")

    @patch('webbrowser.open')
    def test_open_browser(self, mock_open_browser):
        self.app.open_browser('http://example.com')
        mock_open_browser.assert_called_with('http://example.com', new=0)

    @patch('tkinter.simpledialog.askstring')
    @patch('urllib.request.urlopen')
    def test_track_ip(self, mock_urlopen, mock_askstring):
        # Mock the response of the URL request
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "query": "8.8.8.8",
            "country": "United States",
            "regionName": "California",
            "city": "Mountain View",
            "lat": 37.386,
            "lon": -122.0838,
            "org": "Google LLC"
        }).encode('utf-8')
        mock_urlopen.return_value = mock_response

        # Mock user input for IP address
        mock_askstring.return_value = "8.8.8.8"

        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.track_ip()

            # Check if the text area has been updated with the IP details
            self.assertIn('IP ADDRESS: 8.8.8.8', self.app.text_area.get(1.0, tk.END))

    def test_view_history(self):
        # Add items to history and check if they appear in the history window
        self.app.history.append("Test history entry")
        
        # Open history window
        history_window = tk.Toplevel(self.root)
        self.app.view_history()
        
        history_text = history_window.children['!text']
        self.assertIn("Test history entry", history_text.get(1.0, tk.END))

if __name__ == "__main__":
    unittest.main()
