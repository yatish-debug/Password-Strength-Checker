# 🔐 AdvancePass – Password Strength Evaluator & Generator

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Active-success)
![Security](https://img.shields.io/badge/Type-CLI%20%26%20GUI-orange)

AdvancePass is a **password strength checker and generator** written in Python.  
It evaluates password strength (Very Weak → Strong), provides improvement suggestions,  
and can generate strong passwords instantly.  

Now with a **modern Tkinter GUI**:  
- 👁️ Show/Hide entered password  
- 📋 Display generated password separately  
- 💡 Inline suggestions inside the GUI  
- 🎨 Clean, styled interface with `ttk`  

---

## 📌 Features
- ✅ CLI Mode – check strength & generate passwords from terminal  
- ✅ GUI Mode – interactive Tkinter window  
- ✅ Show/Hide password toggle  
- ✅ Password suggestions displayed inline  
- ✅ Generates strong random passwords (12+ chars)  
- ✅ Beginner-friendly & lightweight  

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yatish-debug/Password-Strength-Checker.git
cd adv3.8.7.py
```

2. Run with Python 3.x:
```bash
python adv3.8.7.py
```

> No external libraries required (uses only standard Python & Tkinter).

---

## ▶️ Usage

When you run the script, you’ll be asked to choose a mode:

```bash
Choose mode: (1) CLI  (2) GUI
```

---

### 1️⃣ CLI Example
```
Enter your password to check: hello123

Password Strength: Weak
⚠️ Suggestions to improve your password:
  - Add at least one uppercase letter.
  - Add at least one special character (!@#$%^&*()-_+=).

💡 Suggested Strong Password: G@7dFs#9X!Lp
```

---

### 2️⃣ GUI Example

- Enter a password and press **Check Password** to see strength & suggestions.  
- Press **Generate Strong Password** to create a secure password.  
- Use the **👁️ Show/Hide button** to toggle password visibility.  
- Suggestions appear in a dedicated text box below.  

🖼️ *GUI Preview (sample screenshot placeholder)*  
```
+------------------------------------------+
| 🔐 AdvancePass - Password Checker        |
|                                          |
| Enter Password: ********   [👁️ Show]     |
|                                          |
| [ Check Password ]  [ Generate Password ]|
|                                          |
| Password Strength: Weak                  |
|                                          |
| Generated Password: G@7dFs#9X!Lp          |
|                                          |
| Suggestions:                             |
| - Add at least one uppercase letter.     |
| - Add at least one special character.    |
+------------------------------------------+
```


## 📂 Project Structure
```
advancepass.py   # Main script
README.md        # Documentation
```



## 🎯 Future Enhancements
- [ ] Add password strength bar (color progress bar in GUI)  
- [ ] Export password reports (CSV/JSON)  
- [ ] Advanced checks (dictionary words, breached password API)  



## 👨‍💻 Author
👨‍💻 **Author**:  
Name: Yatish Bharambe  
Role: Cybersecurity Enthusiast | Python Developer  

⭐ If you find this project useful, please give it a **star** on GitHub!
