import random
import math
import TRNG.TRNG as TRNG

def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Find r and d such that n-1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform Miller-Rabin test k times
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a large prime number."""
    while True:
        p = random.getrandbits(bits)
        if p % 2 == 0:
            p += 1
        if is_prime(p):
            return p

def gcd(a, b):
    """Calculate the greatest common divisor of two numbers."""
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """Calculate the modular inverse of a modulo m."""
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(bits):
    """Generate RSA key pair."""
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Common choice for e
    d = mod_inverse(e, phi)
    return ((n, e), (n, d))

def encrypt(message, public_key):
    """Encrypt a message using RSA."""
    n, e = public_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher

def decrypt(cipher, private_key):
    """Decrypt a message using RSA."""
    n, d = private_key
    message = ''.join([chr(pow(char, d, n)) for char in cipher])
    return message

# Generate RSA key pair
public_key, private_key = generate_keypair(128)

# Test encryption and decryption
message = "Hello, RSA!"
print("Original message:", message)
cipher = encrypt(message, public_key)
print("Encrypted message:", cipher)
decrypted_message = decrypt(cipher, private_key)
print("Decrypted message:", decrypted_message)
