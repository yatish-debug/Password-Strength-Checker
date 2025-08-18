import re
import random
import string
import tkinter as tk
from tkinter import ttk

# -------------------------
# Password Evaluation Logic
# -------------------------
def evaluate_password(password: str, min_length=8, require_upper=True,
                      require_lower=True, require_digit=True, require_special=True) -> tuple:
    suggestions = []
    score = 0

    # Check length
    if len(password) >= max(12, min_length):
        score += 2
    elif len(password) >= min_length:
        score += 1
    else:
        suggestions.append(f"Use at least {min_length} characters.")
    
    # Check for lowercase
    if re.search(r"[a-z]", password):
        score += 1
    elif require_lower:
        suggestions.append("Add at least one lowercase letter.")

    # Check for uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    elif require_upper:
        suggestions.append("Add at least one uppercase letter.")

    # Check for digit
    if re.search(r"[0-9]", password):
        score += 1
    elif require_digit:
        suggestions.append("Add at least one digit.")

    # Check for special character
    if re.search(r"[!@#$%^&*()\-_=+]", password):
        score += 1
    elif require_special:
        suggestions.append("Add at least one special character (!@#$%^&*()-_+=).")

    # Score interpretation
    if score <= 2:
        strength = "Very Weak"
    elif score == 3:
        strength = "Weak"
    elif score == 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, suggestions


def generate_strong_password(length=12) -> str:
    if length < 12:
        length = 12  # Minimum strong length

    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_+="
    return ''.join(random.choice(characters) for _ in range(length))


# -------------------------
# GUI Support (Tkinter Modern UI)
# -------------------------
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
        strength, tips = evaluate_password(pwd)
        strength_var.set(f"Password Strength: {strength}")
        suggestions_text.delete(1.0, tk.END)
        if tips:
            suggestions_text.insert(tk.END, "\n".join(tips))
        else:
            suggestions_text.insert(tk.END, "✅ Your password is strong!")

    def generate_password():
        pwd = generate_strong_password()
        gen_pwd_var.set(pwd)
        strength_var.set("Generated a strong password!")
        suggestions_text.delete(1.0, tk.END)
        suggestions_text.insert(tk.END, "Use this password for better security.")

    root = tk.Tk()
    root.title("AdvancePass - Password Checker")
    root.geometry("450x400")
    root.resizable(False, False)

    # Style
    style = ttk.Style(root)
    style.configure("TButton", font=("Arial", 11), padding=5)
    style.configure("TLabel", font=("Arial", 11))
    style.configure("Header.TLabel", font=("Arial", 14, "bold"))

    # Heading
    ttk.Label(root, text="🔐 AdvancePass - Password Strength Checker", style="Header.TLabel").pack(pady=10)

    # Password input
    frame = ttk.Frame(root)
    frame.pack(pady=5)
    ttk.Label(frame, text="Enter Password:").grid(row=0, column=0, padx=5)
    entry = ttk.Entry(frame, width=25, show="*")
    entry.grid(row=0, column=1, padx=5)
    toggle_btn = ttk.Button(frame, text="👁️ Show", command=toggle_password)
    toggle_btn.grid(row=0, column=2, padx=5)

    # Strength result
    strength_var = tk.StringVar()
    ttk.Label(root, textvariable=strength_var, foreground="blue").pack(pady=5)

    # Buttons
    ttk.Button(root, text="Check Password", command=check_password).pack(pady=5)
    ttk.Button(root, text="Generate Strong Password", command=generate_password).pack(pady=5)

    # Generated password
    gen_pwd_var = tk.StringVar()
    ttk.Label(root, text="Generated Password:").pack(pady=5)
    ttk.Entry(root, textvariable=gen_pwd_var, width=35).pack(pady=5)

    # Suggestions
    ttk.Label(root, text="Suggestions:").pack(pady=5)
    suggestions_text = tk.Text(root, height=6, width=50, wrap="word", font=("Arial", 10))
    suggestions_text.pack(pady=5)

    root.mainloop()


# -------------------------
# Main Runner
# -------------------------
if __name__ == "__main__":
    mode = input("Choose mode: (1) CLI  (2) GUI\n> ").strip()

    if mode == "1":  # CLI mode
        user_password = input("Enter your password to check: ").strip()
        strength, tips = evaluate_password(user_password)

        print(f"\nPassword Strength: {strength}")
        
        if strength == "Strong":
            print("✅ Your password is strong!")
        else:
            print("⚠️ Suggestions to improve your password:")
            for tip in tips:
                print(f"  - {tip}")
            suggested_password = generate_strong_password()
            print(f"\n💡 Suggested Strong Password: {suggested_password}")

    elif mode == "2":  # GUI mode
        run_gui()

    else:
        print("Invalid choice. Exiting.")

 
