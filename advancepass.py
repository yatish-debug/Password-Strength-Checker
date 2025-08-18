import re
import random
import string

def evaluate_password(password: str) -> tuple:
    suggestions = []
    score = 0

    # Check length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")
    
    # Check for lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter.")

    # Check for uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter.")

    # Check for digit
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add at least one digit.")

    # Check for special character
    if re.search(r"[!@#$%^&*()\-_=+]", password):
        score += 1
    else:
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


if __name__ == "__main__":
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
