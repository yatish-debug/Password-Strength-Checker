# 🔐 AdvancePass - Password Strength Checker

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![GitHub stars](https://img.shields.io/github/stars/your-username/AdvancePass?style=social)](https://github.com/your-username/AdvancePass/stargazers)  
[![GitHub forks](https://img.shields.io/github/forks/your-username/AdvancePass?style=social)](https://github.com/your-username/AdvancePass/network/members)  

A powerful **Password Strength Checker & Generator** built in pure **Python 3.8.7 (standard library only)**.  
It helps users evaluate password security, generate strong passwords, analyze entropy, and visualize crack time — all with a **CLI + GUI** interface.

---

## ✨ Features

✅ **Password Strength Analysis**  
- Length, uppercase, lowercase, digits, special characters check  
- Entropy (bits), possible combinations, crack time estimation  

✅ **Advanced Security Features**  
- Dictionary word detection (e.g., `password`, `admin`, `123456`)  
- **Character balance analysis** (avoid too many digits/uppercase)  
- **Password reuse detection** (warns if you’ve used it before)  

✅ **Reporting & Logging**  
- Save detailed reports as **CSV / JSON** (with custom filenames)  
- All password checks are **logged into SQLite DB**  
- **Statistics viewer** (distribution of Weak/Medium/Strong passwords)  
- **Password history viewer** (previously checked passwords)

✅ **User Interfaces**  
- **CLI Mode** (terminal-based analysis & report generation)  
- **GUI Mode** with Tkinter:  
  - Password strength progress bar  
  - Show/Hide password toggle  
  - Dark/Light theme toggle 🌗  
  - Copy password to clipboard  
  - View history & statistics in popup windows  

✅ **Password Generator**  
- Generates secure random passwords (12+ characters by default)  

---

## 📦 Installation

1. Make sure you have **Python 3.8.7** (or later 3.x) installed.  
2. Clone this repository:
   ```bash
   git clone https://github.com/your-username/AdvancePass.git
   cd AdvancePass
````

3. Run the script directly (no external dependencies required):

   ```bash
   python AdvancePass.py
   ```

---

## 🚀 Usage

When you run the script, you can choose **CLI** or **GUI**:

```bash
Choose mode: (1) CLI  (2) GUI
> 
```

### ▶️ CLI Mode

```bash
Enter your password to check: myPass123!
Password Strength: Medium
Entropy: 59.65 bits
Possible Combinations: 1.23e+18
Estimated Crack Time: 39.05 years

⚠️ Suggestions to improve your password:
  - Add at least one special character (!@#$%^&*()-_+=)

💡 Suggested Strong Password: K!d82@FxWqeY
Save report? (csv/json/skip): csv
Enter filename (without extension): myreport
📂 Report saved as myreport.CSV.
```

Also shows **statistics summary** of all stored results.

---

### 🖥️ GUI Mode

* Enter a password and click **Check Password**
* See strength, entropy, crack time & suggestions instantly
* Buttons for:

  * Generate strong password
  * Copy password
  * Save report (CSV/JSON with custom name)
  * View history of all tested passwords
  * View statistics summary
  * Toggle between **Light/Dark theme** 🌗

---

## 📸 Demo Screenshots

📌 *Add your actual screenshots in a `screenshots/` folder.*

Example placeholders:

### GUI - Light Mode

![Light Mode Screenshot](screenshots/light_mode.png)

### GUI - Dark Mode

![Dark Mode Screenshot](screenshots/dark_mode.png)

### CLI Mode

![CLI Screenshot](screenshots/cli_mode.png)

---

## 📊 Database (SQLite)

* All password checks are stored in `password_logs.db`
* Schema:

  ```sql
  CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT,
    strength TEXT,
    entropy REAL,
    crack_time TEXT,
    timestamp TEXT
  );
  ```

---

## 🛠️ Project Structure

```
AdvancePass/
│
├── AdvancePass.py        # Main script (CLI + GUI)
├── password_logs.db      # SQLite database (auto-created)
├── README.md             # Project documentation
└── screenshots/          # Place your screenshots here
```

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork this repo, improve features, or open issues.
