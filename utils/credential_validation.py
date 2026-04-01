
# Let's check if the fields are empty.
def format_validation(dictionary):
    for w in dictionary.values():
        if not w:
            return False
    return True

# Example of mail validation.
def email_validation(email):
    if email.count('@') != 1 or ' ' in email:
        return False
    if not email.endswith(('.it', '.fr', '.ch', '.com')):
        return False
    
    return True

# It will return false if the password doesn't have requirements, true if it does.
def password_validation(password):  
    if not password[0].isalpha() and not password[0].isupper():
        return False
    characters= ('-', '@', '!')
    if not any(c in password for c in characters):
        return False
    if len(password)<8:
        return False
    
    return True