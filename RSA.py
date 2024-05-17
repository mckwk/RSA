import random
import hashlib
import sympy
from TRNG.TRNG import divide_into_bits

def generate_prime(bits):
    nums = divide_into_bits("random_sequence_array.txt", bits)
    primes = []
    for num in nums:
        if sympy.isprime(num):
            primes.append(num)
    return primes

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(bits):
    p = random.choice(generate_prime(bits // 2))
    q = random.choice(generate_prime(bits // 2))
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Common choice for e
    d = mod_inverse(e, phi)
    return ((n, e), (n, d))

def rsa_encrypt_decrypt(message, key):
    n, e_or_d = key
    return pow(message, e_or_d, n)

def hash_message_sha3(message):
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(message.encode('utf-8'))
    return sha3_256.hexdigest()

# Test the hash function
message = "boże to działa!!!"


def message_content_change(message1, message2):
    public_key, private_key = generate_keypair(512)
    message_hash = int(hash_message_sha3(message1),16)
    print("\nOriginal message:", message1)
    print("SHA3-256 hash:", message_hash)
    cipher = rsa_encrypt_decrypt(message_hash, private_key)
    print("Encrypted:", cipher)

    public_key, private_key = generate_keypair(512)
    message_hash = int(hash_message_sha3(message2),16)
    print("\nOriginal message:", message2)
    print("SHA3-256 hash:", message_hash)
    cipher = rsa_encrypt_decrypt(message_hash, private_key)
    print("Encrypted:", cipher, '\n')

def hash_encrypt_decrypt(message):
    message_hash = hash_message_sha3(message)
    print("\nOriginal message:", message, '\n')
    print("SHA3-256 hash:", message_hash)

    public_key, private_key = generate_keypair(512)

    message_hash_int = int(message_hash, 16)

    cipher = rsa_encrypt_decrypt(message_hash_int, private_key)
    print("Encrypted:", cipher)

    decrypted_hash_int = rsa_encrypt_decrypt(cipher, public_key)
    decrypted_hash = hex(decrypted_hash_int)[2:].zfill(64)
    print("Decrypted:", decrypted_hash)
    print("\nHash match:", message_hash == decrypted_hash, '\n')

def wrong_pub_key(message):
    message_hash = hash_message_sha3(message)
    print("\nOriginal message:", message, '\n')
    print("SHA3-256 hash:", message_hash)

    public_key, private_key = generate_keypair(512)
    public_key_but_wrong, private_key_but_wrong = generate_keypair(512)

    message_hash_int = int(message_hash, 16)

    cipher = rsa_encrypt_decrypt(message_hash_int, private_key)
    print("Encrypted:", cipher)

    decrypted_hash_int = rsa_encrypt_decrypt(cipher, public_key_but_wrong)
    decrypted_hash = hex(decrypted_hash_int)[2:].zfill(64)
    print("Decrypted:", decrypted_hash)
    print("\nHash match:", message_hash == decrypted_hash, '\n')

def main():
    #message_content_change("wiadomość pierwsza", "wiadomość druga")
    hash_encrypt_decrypt("działa!")
    #wrong_pub_key("nie działa!")

if __name__ == "__main__":
    main()