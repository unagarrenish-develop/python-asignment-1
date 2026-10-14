"""Q2: Optimized Password Audit
Run: python Q2_Password_Audit.py < input.txt
Classification order: length, repeated-character pattern, banned substring, composition.
"""
import sys
import re

def has_banned_word(password, banned_words):
    folded = password.casefold()
    return any(word in folded for word in banned_words)

def classify_password(password, banned_words):
    if not 6 <= len(password) <= 12:
        return "WEAK_LENGTH"
    if re.search(r"(.)\1{3,}", password):
        return "WEAK_PATTERN"
    if has_banned_word(password, banned_words):
        return "COMPROMISED"
    if not (re.search(r"[a-z]", password) and re.search(r"[A-Z]", password)
            and re.search(r"\d", password) and re.search(r"[$#@]", password)):
        return "WEAK_PATTERN"
    return "STRONG"

def main():
    lines = sys.stdin.read().splitlines()
    try:
        pos = 0
        b = int(lines[pos].strip()); pos += 1
        if b < 1:
            raise ValueError("At least one banned word is required")
        banned = [lines[pos + i].strip().casefold() for i in range(b)]
        pos += b
        if any(not word for word in banned):
            raise ValueError("Banned words cannot be empty")
        n = int(lines[pos].strip()); pos += 1
        if n < 1 or len(lines) < pos + n:
            raise ValueError("Invalid password count")
        for i, password in enumerate(lines[pos:pos+n], 1):
            print(f"{i}: {classify_password(password.strip(), banned)}")
    except (ValueError, IndexError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
