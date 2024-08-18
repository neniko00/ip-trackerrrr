import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import urllib.request
import json
import webbrowser
import os
# You need to install this library using pip install pyperclip

class IPAddressLocatorGUI:
    COLORS = {
        'R': '#FF0000',
        'G': '#00FF00',
        'CY': '#00FFFF',
        'W': '#FFFFFF',
        'Y': '#FFFF00'
    }

    def __init__(self, root):
        self.root = root
        self.root.title("IP Address Locator")
        self.root.geometry("600x400")
        self.path = os.path.isfile('/data/data/com.termux/files/usr/bin/bash')
        self.history = []

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        self.header_label = tk.Label(self.root, text="MADE BY-\n\n Shreya", font=("Helvetica", 16))
        self.header_label.pack(pady=10)

        self.option_label = tk.Label(self.root, text="CHOOSE OPTION", font=("Helvetica", 14))
        self.option_label.pack(pady=5)

        self.check_ip_button = tk.Button(self.root, text="CHECK SYSTEM IP", command=self.check_system_ip)
        self.check_ip_button.pack(pady=5)

        self.track_ip_button = tk.Button(self.root, text="TRACK IP", command=self.track_ip)
        self.track_ip_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="COPY DETAILS TO CLIPBOARD", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)

        self.history_button = tk.Button(self.root, text="VIEW HISTORY", command=self.view_history)
        self.history_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="EXIT", command=self.exit_program)
        self.exit_button.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, width=70)
        self.text_area.pack(pady=10)

        self.status_bar = tk.Label(self.root, text="", anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def display_ip_details(self, data):
        details = (
            f"IP ADDRESS: {data['query']}\n"
            f"COUNTRY: {data['country']}\n"
            f"REGION: {data['regionName']}\n"
            f"CITY: {data['city']}\n"
            f"LATITUDE: {data['lat']}\n"
            f"LONGITUDE: {data['lon']}\n"
            f"TELECOM COMPANY: {data['org']}"
        )

        # Updated map link format
        map_link = f'https://www.google.com/maps/search/?api=1&query={data["lat"]},{data["lon"]}'
        
        message = f"{details}\n\nGoogle Map Link: {map_link}"
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, message)

        self.history.append(details + f"\nGoogle Map Link: {map_link}")

        if messagebox.askyesno("IP Details", message + "\n\nDo you want to open this link in the browser?"):
            self.open_browser(map_link)

    def open_browser(self, link):
        if self.path:
            open_command = f'am start -a android.intent.action.VIEW -d {link}'
            os.system(f"{open_command} > /dev/null")
        else:
            webbrowser.open(link, new=0)

    def fetch_ip_details(self, url):
        self.status_bar.config(text="Fetching IP details...")
        try:
            response = urllib.request.urlopen(url)
            data = json.load(response)
            self.display_ip_details(data)
        except KeyError:
            messagebox.showerror("Error", "Invalid IP Address!")
        except urllib.error.URLError:
            messagebox.showerror("Error", "Please check your internet connection!")
        finally:
            self.status_bar.config(text="Ready")

    def track_ip(self):
        ip_address = simpledialog.askstring("Track IP", "Enter IP Address:")
        if ip_address:
            url = f'http://ip-api.com/json/{ip_address}'
            self.fetch_ip_details(url)
        else:
            messagebox.showerror("Error", "Enter a valid IP address!")

    def check_system_ip(self):
        url = 'http://ip-api.com/json/'
        self.fetch_ip_details(url)

    def copy_to_clipboard(self):
        content = self.text_area.get(1.0, tk.END)
        pyperclip.copy(content)
        messagebox.showinfo("Clipboard", "Details copied to clipboard!")

    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("History")
        history_window.geometry("400x300")

        history_text = tk.Text(history_window, wrap=tk.WORD)
        history_text.pack(expand=True, fill=tk.BOTH)

        for entry in self.history:
            history_text.insert(tk.END, entry + "\n\n")

    def exit_program(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = IPAddressLocatorGUI(root)
    root.mainloop()
