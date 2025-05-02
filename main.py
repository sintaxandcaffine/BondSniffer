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

TREASURY_API_URL = "https://fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/savings_bonds/savings_bonds_value_files"
TREASURY_DOWNLOAD_FOLDER = "treasury_data"

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
            return file_path, False  # File already exists

        file_response = requests.get(latest_file_url)
        file_response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(file_response.content)

        return file_path, True

    except Exception as e:
        msg.showerror("Error", f"Failed to fetch latest bond values:\n{e}")
        return None, False


class BondSnifferApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BondSniffer GUI - Nerdvana")
        self.geometry("1000x700")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        self.bond_csv_path = ctk.StringVar()
        self.status = ctk.StringVar(value="Ready.")
        self.dataframe = None

        self.create_menu()
        self.create_widgets()

        # Auto-fetch bond values at startup
        self.after(1000, self.auto_fetch_bond_values)

    def create_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Bond CSV", command=self.load_csv)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        datamenu = tk.Menu(menubar, tearoff=0)
        datamenu.add_command(label="Fetch Latest Bond Values", command=self.fetch_and_notify)
        menubar.add_cascade(label="Data", menu=datamenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About BondSniffer", command=self.show_about)
        helpmenu.add_command(label="Treasury Help", command=lambda: self.open_link("https://www.treasurydirect.gov/savings-bonds/"))
        helpmenu.add_command(label="More from Nerdvana", command=lambda: self.open_link("https://github.com/SinTaxAndCaffeine/"))
        helpmenu.add_command(label="More about BondSniffer", command=lambda: self.open_link("https://github.com/SinTaxAndCaffeine/BondSniffer-GUI"))
        helpmenu.add_separator()
        helpmenu.add_command(label="Report a Problem", command=lambda: self.open_link("https://github.com/SinTaxAndCaffeine/BondSniffer-GUI/issues/new?title=[Bug%20Report]&body=Please%20describe%20the%20problem%20you%20encountered%20with%20BondSniffer."))
        helpmenu.add_command(label="Got an Idea, Question, or Concern?", command=lambda: self.open_link("https://github.com/SinTaxAndCaffeine/BondSniffer-GUI/issues/new?title=[Idea/Question]&body=Tell%20us%20about%20your%20idea,%20question,%20or%20concern!"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    def create_widgets(self):
        ctk.CTkLabel(self, text="BondSniffer - U.S. Savings Bond Valuation Tool", font=("Arial", 30, "bold")).pack(pady=12)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=12)
        ctk.CTkButton(frame, text="Choose Bond CSV", font=("Arial", 20, "bold"), command=self.load_csv).pack(side="left", padx=12)
        ctk.CTkLabel(frame, textvariable=self.bond_csv_path, width=400).pack(side="left")

        ctk.CTkButton(self, text="Process and Save Bonds", font=("Arial", 20, "bold"), command=self.process_bonds).pack(pady=12)
        ctk.CTkLabel(self, textvariable=self.status, font=("Arial", 20, "bold")).pack(pady=12)

        self.table_frame = ctk.CTkScrollableFrame(self, width=800, height=300)
        self.table_frame.pack(pady=10)

        binary_line = "01001011 01100101 01101001 01101110 01100101 00100000 01010100 01110010 01100001 01110101 01100010 01100101 01101110 00101100 00100000 01101110 01110101 01110010 00100000 01110011 01101111 00100000 01100010 01101100 01100001 01110101 01100101 00100000 01001110 11000011 10100100 01100111 01100101 01101100"
        ctk.CTkLabel(self, text=binary_line, font=("Arial", 20), text_color="#222222").pack(pady=2)

    def auto_fetch_bond_values(self):
        self.status.set("Fetching latest Treasury bond values...")
        path, downloaded = fetch_latest_bond_value_file()
        if path:
            result_msg = "Downloaded new bond values." if downloaded else "Using cached bond values."
            msg.showinfo("Bond Values Ready", result_msg)
            self.status.set("Bond values loaded.")
        else:
            self.status.set("Failed to load bond values.")

    def fetch_and_notify(self):
        self.status.set("Checking for latest bond value file...")
        path, downloaded = fetch_latest_bond_value_file()
        if path:
            result_msg = "Downloaded new bond values." if downloaded else "Already up to date."
            msg.showinfo("Bond Values", result_msg)
            self.status.set("Bond values refreshed.")
        else:
            self.status.set("Failed to fetch new bond values.")

    def load_csv(self):
        file_path = fd.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.bond_csv_path.set(file_path)
            self.status.set("File loaded.")
            self.dataframe = pd.read_csv(file_path)
            self.display_table()

    def display_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        if self.dataframe is not None:
            for idx, col in enumerate(self.dataframe.columns):
                ctk.CTkLabel(self.table_frame, text=col, font=("Arial", 16, "bold")).grid(row=0, column=idx, padx=5, pady=5)
            for row_idx, row in self.dataframe.iterrows():
                for col_idx, value in enumerate(row):
                    ctk.CTkLabel(self.table_frame, text=str(value), font=("Arial", 14)).grid(row=row_idx+1, column=col_idx, padx=5, pady=2)

    def process_bonds(self):
        if self.dataframe is None:
            self.status.set("No bond data loaded.")
            return
        self.dataframe["Calculated Value"] = self.dataframe["Denom"].apply(lambda x: "$99.99 (mock)")
        save_path = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            self.dataframe.to_csv(save_path, index=False)
            self.status.set(f"Processed! Saved to {save_path}")

    def show_about(self):
        msg.showinfo("About BondSniffer", "BondSniffer GUI\nVersion 2.1\nCreated by SinTaxAndCaffeine\nPart of the Nerdvana Project\n\u00a9 2025")

    def open_link(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    app = BondSnifferApp()
    app.mainloop()
