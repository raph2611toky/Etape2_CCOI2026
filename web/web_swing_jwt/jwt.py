from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import itertools

cipher_hex = "f9d4eb5e5624e806367ff34eb6985e0c773b11c1331065c365b4dbf13d7bf600245edd792dd53228c8d589d3c1c676da"
ciphertext = bytes.fromhex(cipher_hex)

first_names = ["Antoine", "Mathys"]
last_names  = ["JOUARY", "Lopinto", "LOPINTO", "Jouary"]

def generate_variants(first, last):
    variants = []

    combos = [
        first + last,
        first + last.upper(),
        first.upper() + last,
        first.upper() + last.upper(),
        first.lower() + last.lower(),
        first.lower() + last.upper(),
        first + "_" + last,
        first + "-" + last
    ]

    for c in combos:
        variants.append(c)

    return variants

def derive_keys(identity):
    keys = []

    # SHA256 → 16 bytes
    sha = hashlib.sha256(identity.encode()).digest()
    keys.append(sha[:16])

    # MD5
    md5 = hashlib.md5(identity.encode()).digest()
    keys.append(md5)

    # raw padded
    raw = identity.encode()
    if len(raw) <= 16:
        keys.append(raw.ljust(16, b'\x00'))

    return keys

def derive_ivs(identity):
    ivs = []

    ivs.append(hashlib.md5(identity.encode()).digest())
    ivs.append(hashlib.sha256(identity.encode()).digest()[:16])
    ivs.append(b"\x00" * 16)

    return ivs

for first, last in itertools.product(first_names, last_names):
    for identity in generate_variants(first, last):

        if len(identity) != 14:
            continue

        keys = derive_keys(identity)
        ivs  = derive_ivs(identity)

        for key in keys:
            for iv in ivs:
                try:
                    cipher = AES.new(key, AES.MODE_CBC, iv)
                    plaintext = unpad(cipher.decrypt(ciphertext), 16)

                    print("FOUND!")
                    print("Identity:", identity)
                    print("Plaintext:", plaintext.decode(errors="ignore"))
                    exit()

                except:
                    pass

print("Nothing found.")