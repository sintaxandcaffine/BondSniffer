# BondSniffer GUI | A Nerdvana Tool
# ─────────────────────────────────────────────
# Crafted with ☕ and 💻 by SinTaxAndCaffeine
# GitHub: github.com/SinTaxAndCaffeine
# Part of the Nerdvana Project – 2025
# Signature: S!nTAx&C@ff|n3 was here... ☕💻💥
# Line 7 Easter Egg (Base64): SmFtbmV5IFRoZSBOZXJkeUJhcmQgQUFG

import customtkinter as ctk
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import tkinter as tk
import webbrowser
import requests
import pandas as pd
import os
from datetime import datetime

# Line 17 Easter Egg (Binary): Keine Trauben, nur so blaue Nägel (hidden elsewhere)

# Line 81 Easter Egg (Gaelic): Go maire an teaghlach (hidden elsewhere)

TREASURY_API_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/savings_bonds/savings_bonds_value_files"
TREASURY_DOWNLOAD_FOLDER = "treasury_data"

# Obfuscated Easter Eggs Below (True Hunt Format)
a = "R28gbWFpcmUgYW4gdGVhZ2hsYWNo"
b = "01001011 01100101 01101001 01101110 01100101 00100000 01010100 01110010 01100001 01110101 01100010 01100101 01101110 00101100 00100000 01101110 01110101 01110010 00100000 01110011 01101111 00100000 01100010 01101100 01100001 01110101 01100101 00100000 01001110 11000011 10100100 01100111 01100101 01101100"

class BondSnifferApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BondSniffer GUI - Nerdvana")
        self.geometry("900x600")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        self.bond_csv_path = ctk.StringVar()
        self.status = ctk.StringVar(value="Ready.")
        self.dataframe = None

        self.create_widgets()
        self.after(1000, self.auto_fetch_bond_values)

    def create_widgets(self):
        menubar = ctk.CTkFrame(self)
        menubar.pack(fill="x")
        ctk.CTkButton(menubar, text="Open Bond CSV", command=self.load_csv).pack(side="left", padx=10)
        ctk.CTkButton(menubar, text="Fetch Latest Bond Values", command=self.handle_api_fetch).pack(side="left", padx=10)
        ctk.CTkButton(menubar, text="Process and Save", command=self.process_and_save).pack(side="left", padx=10)

        self.table = ctk.CTkTextbox(self, height=400)
        self.table.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(self, textvariable=self.status, font=("Arial", 20)).pack(pady=4)

        # Hidden Nerd Easter Egg (Binary Line - visually buried)
        binary_line = "01001011 01100101 01101001 01101110 01100101 00100000 01010100 01110010 01100001 01110101 01100010 01100101 01101110 00101100 00100000 01101110 01110101 01110010 00100000 01110011 01101111 00100000 01100010 01101100 01100001 01110101 01100101"
        ctk.CTkLabel(self, text=binary_line, font=("Arial", 20), text_color="#222222").pack(pady=2)

    def load_csv(self):
        file_path = fd.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.bond_csv_path.set(file_path)
            self.status.set("File loaded.")
            self.dataframe = pd.read_csv(file_path)
            self.update_table_preview()

    def update_table_preview(self):
        if self.dataframe is not None:
            self.table.delete("1.0", "end")
            self.table.insert("end", self.dataframe.to_string(index=False))

    def handle_api_fetch(self):
        file_path, updated = fetch_latest_bond_value_file()
        if file_path:
            self.status.set("Bond values updated." if updated else "Bond values already up-to-date.")
        else:
            self.status.set("Failed to update bond values.")

    def auto_fetch_bond_values(self):
        self.status.set("Checking for latest bond data...")
        self.handle_api_fetch()

    def process_and_save(self):
        if self.dataframe is None:
            self.status.set("No CSV loaded.")
            return
        self.dataframe["Calculated Value"] = self.dataframe["Denom"].apply(lambda x: "$99.99 (mock)")
        output_path = os.path.join(os.path.dirname(self.bond_csv_path.get()), "bond_results.csv")
        self.dataframe.to_csv(output_path, index=False)
        self.status.set(f"Processed! Saved to {output_path}")

def fetch_latest_bond_value_file():
    try:
        os.makedirs(TREASURY_DOWNLOAD_FOLDER, exist_ok=True)
        response = requests.get(TREASURY_API_URL)
        response.raise_for_status()
        data = response.json()

        latest_file_url = None
        latest_date = "1900-01-01"

        for entry in data.get("data", []):
            file_date = entry.get("as_of_date")
            if file_date > latest_date:
                latest_date = file_date
                latest_file_url = entry.get("file_url")

        if not latest_file_url:
            raise Exception("Could not find latest bond value file URL.")

        file_name = f"bond_values_{latest_date}.csv"
        file_path = os.path.join(TREASURY_DOWNLOAD_FOLDER, file_name)

        if os.path.exists(file_path):
            return file_path, False

        file_response = requests.get(latest_file_url)
        file_response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(file_response.content)

        return file_path, True

    except requests.exceptions.HTTPError as http_err:
        msg.showerror("HTTP Error", f"HTTP error occurred:\n{http_err}")
        return None, False
    except Exception as err:
        msg.showerror("Error", f"Failed to fetch latest bond values:\n{err}")
        return None, False

if __name__ == "__main__":
    app = BondSnifferApp()
    app.mainloop()
