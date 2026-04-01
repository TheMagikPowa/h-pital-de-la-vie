import hashlib

# It does a simple hash.
def hashing (pw):
    return hashlib.sha256(pw.encode()).hexdigest()