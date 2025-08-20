import re
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog   # CH: added simpledialog for custom filename
import csv
import json
import hashlib
import math
import sqlite3
import time

# CH: Modified evaluate_password with balance & reuse checks
def evaluate_password(password: str, min_length=8, require_upper=True,
                      require_lower=True, require_digit=True, require_special=True,
                      dictionary_check=True, previous_passwords=None) -> tuple:
    suggestions = []
    score = 0

    # Length check
    if len(password) >= max(12, min_length):
        score += 2
    elif len(password) >= min_length:
        score += 1
    else:
        suggestions.append(f"Use at least {min_length} characters.")
    
    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    elif require_lower:
        suggestions.append("Add at least one lowercase letter.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    elif require_upper:
        suggestions.append("Add at least one uppercase letter.")

    # Digits
    if re.search(r"[0-9]", password):
        score += 1
    elif require_digit:
        suggestions.append("Add at least one digit.")

    # Special chars
    if re.search(r"[!@#$%^&*()\\-_=+]", password):
        score += 1
    elif require_special:
        suggestions.append("Add at least one special character (!@#$%^&*()-_+=).")

    # Dictionary check
    if dictionary_check:
        common_words = ["password", "admin", "welcome", "123456", "qwerty"]
        if password.lower() in common_words:
            suggestions.append("Avoid using common dictionary words (e.g., password, admin).")
            score = max(0, score - 1)

    # NEW: Character balance analysis
    if password:
        if password.isdigit() or password.isalpha():
            suggestions.append("Mix letters, digits, and symbols for better balance.")
        elif sum(c.isdigit() for c in password) > len(password) // 2:
            suggestions.append("Too many digits, balance with letters/symbols.")
        elif sum(c.isupper() for c in password) > len(password) // 2:
            suggestions.append("Too many uppercase letters, balance with lowercase/symbols.")

    # NEW: Password reuse check
    if previous_passwords and password in previous_passwords:
        suggestions.append("⚠️ You have used this password before. Avoid reusing old passwords.")
        score = max(0, score - 1)

    # Entropy calculation
    def password_entropy(pwd):
        pool = 0
        if re.search(r"[a-z]", pwd): pool += 26
        if re.search(r"[A-Z]", pwd): pool += 26
        if re.search(r"[0-9]", pwd): pool += 10
        if re.search(r"[!@#$%^&*()\\-_=+]", pwd): pool += 14
        if pool == 0:
            return 0
        return len(pwd) * math.log2(pool)

    entropy_bits = password_entropy(password)
    combinations = 2 ** entropy_bits
    guesses_per_second = 1e9
    crack_time_seconds = combinations / guesses_per_second

    def time_format(seconds):
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.2f} days"
        else:
            return f"{seconds/31536000:.2f} years"

    crack_time = time_format(crack_time_seconds)

    if score <= 2:
        strength = "Very Weak"
    elif score == 3:
        strength = "Weak"
    elif score == 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, suggestions, score, entropy_bits, combinations, crack_time

def generate_strong_password(length=12) -> str:
    if length < 12:
        length = 12
    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_+="
    return ''.join(random.choice(characters) for _ in range(length))

# CH: Modified for custom filename
def export_report(password, strength, tips, filetype="csv", entropy=0, crack_time="N/A", filename="password_report"):
    data = {"Password": password, "Strength": strength, "Entropy": f"{entropy:.2f} bits",
            "Crack Time": crack_time, "Suggestions": tips}
    if filetype == "csv":
        with open(f"{filename}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data.keys())
            writer.writerow([data["Password"], data["Strength"], data["Entropy"], data["Crack Time"],
                             "; ".join(data["Suggestions"])])
    elif filetype == "json":
        with open(f"{filename}.json", "w") as f:
            json.dump(data, f, indent=4)

def log_to_db(password, strength, entropy, crack_time):
    conn = sqlite3.connect("password_logs.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS logs (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   password TEXT,
                   strength TEXT,
                   entropy REAL,
                   crack_time TEXT,
                   timestamp TEXT)""")
    cur.execute("INSERT INTO logs (password, strength, entropy, crack_time, timestamp) VALUES (?, ?, ?, ?, ?)",
                (password, strength, entropy, crack_time, time.ctime()))
    conn.commit()
    conn.close()

# NEW: fetch previous passwords for reuse check and history
def fetch_previous_passwords():
    conn = sqlite3.connect("password_logs.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS logs (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   password TEXT,
                   strength TEXT,
                   entropy REAL,
                   crack_time TEXT,
                   timestamp TEXT)""")
    cur.execute("SELECT password FROM logs")
    data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data

# NEW: get statistics summary
def get_statistics():
    conn = sqlite3.connect("password_logs.db")
    cur = conn.cursor()
    cur.execute("SELECT strength, COUNT(*) FROM logs GROUP BY strength")
    stats = cur.fetchall()
    conn.close()
    return stats

def run_gui():
    def toggle_password():
        if entry.cget("show") == "":
            entry.config(show="*")
            toggle_btn.config(text="👁️ Show")
        else:
            entry.config(show="")
            toggle_btn.config(text="🙈 Hide")

    def check_password():
        pwd = entry.get()
        prev_pwds = fetch_previous_passwords()  # NEW
        strength, tips, score, entropy, combinations, crack_time = evaluate_password(pwd, previous_passwords=prev_pwds)
        result.set(f"Password Strength: {strength}\nEntropy: {entropy:.2f} bits\nPossible Combinations: {combinations:.2e}\nCrack Time: {crack_time}")
        suggestions_text.delete(1.0, tk.END)
        if tips:
            suggestions_text.insert(tk.END, "\n".join(tips))
        else:
            suggestions_text.insert(tk.END, "✅ Your password is strong!")

        progress['value'] = min(score * 20, 100)
        if score <= 2:
            progress.configure(style="Red.Horizontal.TProgressbar")
        elif score == 3:
            progress.configure(style="Orange.Horizontal.TProgressbar")
        elif score == 4:
            progress.configure(style="Yellow.Horizontal.TProgressbar")
        else:
            progress.configure(style="Green.Horizontal.TProgressbar")

        log_to_db(pwd, strength, entropy, crack_time)

    def generate_password():
        pwd = generate_strong_password()
        entry.delete(0, tk.END)
        entry.insert(0, pwd)
        result.set("Generated a strong password!")

    def copy_password():
        pwd = entry.get()
        root.clipboard_clear()
        root.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    def save_report(filetype):
        pwd = entry.get()
        filename = simpledialog.askstring("Save Report", "Enter filename (without extension):")  # NEW
        if not filename:
            filename = "password_report"
        strength, tips, _, entropy, _, crack_time = evaluate_password(pwd)
        export_report(pwd, strength, tips, filetype, entropy, crack_time, filename)
        messagebox.showinfo("Report Saved", f"Password report saved as {filename}.{filetype}")

    # NEW: view password history
    def view_history():
        history = fetch_previous_passwords()
        top = tk.Toplevel(root)
        top.title("Password History")
        text = tk.Text(top, width=60, height=15)
        text.pack()
        if history:
            for i, pw in enumerate(history, 1):
                text.insert(tk.END, f"{i}. {pw}\n")
        else:
            text.insert(tk.END, "No history available.")

    # NEW: view statistics
    def view_statistics():
        stats = get_statistics()
        top = tk.Toplevel(root)
        top.title("Statistics")
        text = tk.Text(top, width=40, height=10)
        text.pack()
        if stats:
            for strength, count in stats:
                text.insert(tk.END, f"{strength}: {count}\n")
        else:
            text.insert(tk.END, "No data available.")

    # NEW: dark/light theme toggle
    def toggle_theme():
        current_bg = root.cget("bg")
        if current_bg == "SystemButtonFace":  # default light
            root.configure(bg="black")
            style.configure("TLabel", foreground="white", background="black")
            style.configure("TButton", background="gray20", foreground="white")
        else:  # switch back to light
            root.configure(bg="SystemButtonFace")
            style.configure("TLabel", foreground="black", background="SystemButtonFace")
            style.configure("TButton", background="SystemButtonFace", foreground="black")

    global root
    root = tk.Tk()
    root.title("AdvancePass - Password Checker")
    root.geometry("560x650")
    root.resizable(False, False)

    style = ttk.Style(root)
    style.configure("TButton", font=("Arial", 11), padding=5)
    style.configure("Header.TLabel", font=("Arial", 14, "bold"))
    style.configure("Red.Horizontal.TProgressbar", troughcolor="white", background="red")
    style.configure("Orange.Horizontal.TProgressbar", troughcolor="white", background="orange")
    style.configure("Yellow.Horizontal.TProgressbar", troughcolor="white", background="yellow")
    style.configure("Green.Horizontal.TProgressbar", troughcolor="white", background="green")

    ttk.Label(root, text="🔐 AdvancePass - Password Strength Checker", style="Header.TLabel").pack(pady=10)

    frame = ttk.Frame(root)
    frame.pack(pady=5)
    ttk.Label(frame, text="Enter Password:").grid(row=0, column=0, padx=5)
    entry = ttk.Entry(frame, width=30, show="*")
    entry.grid(row=0, column=1, padx=5)
    toggle_btn = ttk.Button(frame, text="👁️ Show", command=toggle_password)
    toggle_btn.grid(row=0, column=2, padx=5)

    result = tk.StringVar()
    ttk.Label(root, textvariable=result, foreground="blue").pack(pady=5)

    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.pack(pady=10)

    ttk.Button(root, text="Check Password", command=check_password).pack(pady=5)
    ttk.Button(root, text="Generate Strong Password", command=generate_password).pack(pady=5)
    ttk.Button(root, text="📋 Copy Password", command=copy_password).pack(pady=5)
    ttk.Button(root, text="Save Report (CSV)", command=lambda: save_report("csv")).pack(pady=5)
    ttk.Button(root, text="Save Report (JSON)", command=lambda: save_report("json")).pack(pady=5)
    ttk.Button(root, text="View History", command=view_history).pack(pady=5)   # NEW
    ttk.Button(root, text="View Statistics", command=view_statistics).pack(pady=5)   # NEW
    ttk.Button(root, text="Toggle Dark/Light Theme", command=toggle_theme).pack(pady=5)   # NEW

    ttk.Label(root, text="Suggestions:").pack(pady=5)
    suggestions_text = tk.Text(root, height=6, width=55, wrap="word", font=("Arial", 10))
    suggestions_text.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    mode = input("Choose mode: (1) CLI  (2) GUI\n> ").strip()

    if mode == "1":
        user_password = input("Enter your password to check: ").strip()
        prev_pwds = fetch_previous_passwords()  # NEW
        strength, tips, score, entropy, combinations, crack_time = evaluate_password(user_password, previous_passwords=prev_pwds)

        print(f"\nPassword Strength: {strength}")
        print(f"Entropy: {entropy:.2f} bits")
        print(f"Possible Combinations: {combinations:.2e}")
        print(f"Estimated Crack Time: {crack_time}")

        if strength == "Strong":
            print("✅ Your password is strong!")
        else:
            print("⚠️ Suggestions to improve your password:")
            for tip in tips:
                print(f"  - {tip}")
            suggested_password = generate_strong_password()
            print(f"\n💡 Suggested Strong Password: {suggested_password}")

        save_choice = input("Save report? (csv/json/skip): ").strip().lower()
        if save_choice in ["csv", "json"]:
            filename = input("Enter filename (without extension): ").strip() or "password_report"   # NEW
            export_report(user_password, strength, tips, save_choice, entropy, crack_time, filename)
            print(f"📂 Report saved as {filename}.{save_choice.upper()}.")

        log_to_db(user_password, strength, entropy, crack_time)

        # NEW: show DB statistics in CLI
        stats = get_statistics()
        print("\n📊 Password Strength Statistics:")
        if stats:
            for s, c in stats:
                print(f"{s}: {c}")
        else:
            print("No data available.")

    elif mode == "2":
        run_gui()
    else:
        print("Invalid choice. Exiting.")
