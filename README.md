# BondSniffer
![version](https://img.shields.io/badge/version-2.1-green) 
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

BondSniffer is a retro-themed GUI application designed to assist users in valuing U.S. Savings Bonds. Developed by [SinTaxAndCaffeine](https://github.com/SinTaxAndCaffeine), it's part of the Nerdvana Project.

---

## ⚙️ Features

- **Import Bond Data**  
  Easily upload your list of U.S. Savings Bonds in CSV format for processing.

- **Data Preview**  
  Scrollable, in-app table view of your bond entries for quick visual inspection.

- **Bond Valuation (Mock for Now)**  
  Calculates placeholder values for each bond entry. Real API-based valuation is in progress for v2.2.

- **CSV Export**  
  Save processed bond data and calculated values to a new CSV file.

- **API Integration (Live Fetching)**  
  Automatically downloads the latest bond value tables from [fiscaldata.treasury.gov](https://fiscaldata.treasury.gov) for use in future calculations.

- **Support and Help Menu**  
  Built-in Treasury links, GitHub issue templates, and contact options for support or feedback.

- **Easter Eggs + Retro Fun**  
  Coming soon: Splash screen with Atari-style Pong mini-game to play while data loads.

---

## 🧪 How To Run

**Prerequisites**:
- Python 3.8 or higher
- pip package manager

**Installation**:
```bash
# Clone the repository
git clone https://github.com/sintaxandcaffine/BondSniffer.git
cd BondSniffer

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 📂 Folder Structure

```
BondSniffer/
├── input/
├── output/
├── treasury_data/
├── main.py
├── README.md
├── requirements.txt
```

---

## 🚀 Repo

[github.com/SinTaxAndCaffeine/BondSniffer](https://github.com/SinTaxAndCaffeine/BondSniffer)

---

## 🤝 Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before submitting a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
