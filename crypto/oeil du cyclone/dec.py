import hashlib

p      = 2**521 - 1          # Mersenne prime M521
TARGET = "f687cb74fdcefefc"  # SHA256(flag)[:16]

points = [
    (1, 0xd0393fd5aa76c02f53757a5883d97a0f0ade112cffc590c8378f2b5a6696a284dcc1ef10c29f7275958952bca3c40922f75258f47e808d587aca867f48f0d798f5),
    (2, 0xa0deb8650c459c78e99ca5ae29c1399c8221723e6c966a4a4494ec69bcb20399336bba13c10998b4b0b554cffdaec9b8b536e6fa9ea4eefa7321782797b84672e4),
    (3, 0x9dc6d639cbda2c6893efafe086027e1f9126a9e27f2d342e45e8090675c2eca7e4ae330b163f8f059fa665a20ea4be41a4de9fe882ac3b08387ba8649622293745),
    (4, 0xff3a80c762b7a71ee3793ed87a7951f819960a86b067cefbe94cac78b9f556291ebf42ae21395da1a5e9d3d426624b6cf5bebb4487d9311737417749e401c0cb57),
    (5, 0x748755843bdf0733e28882bb8f096fdd4c4ae2142cba5fb2ea4ba7e65a7b007a75f34a4f7a94b4b8e5b9d425d415b5750066cb52e451f11933b086614b816d4ecb),
]

flooded = [
    (6, 0x18e91e304d2372e99ce65481f4a15284c423aa9ac47a25b639109b2c0c5d60cb6ba133679b80d2d34cfdc2c2968c5b83977eaa1b6e5ad7ed0368e3d0a9639300000),
    (7, 0x2a67e416cef50a7fd1040a3c88f446f6955c3564ef1992c7311eab32fc23958dcbb2918c2ff4897a9380dcf879b81f599b4c34142f81454279da4cdb6245300000),
    (8, 0xdbd27adc2803b734baba0522d86af830f98ee4051f093dd8a86cd68f8366481c71859657bcaaf62d8e20cde862d85e4e66e580aff9ee9a2e558135fef75c500000),
    (9, 0x57e86be63e6ca409bbf147ebcd20ae61d581cec154bd076cddf821be5bd0fcc42db742bb80174af1bb5c773ec91e2884c5d273125030417e2c0ecb961be6800000),
]

xs = [pt[0] for pt in points]
ys = [pt[1] for pt in points]


def lagrange_eval(x_eval):
    result = 0
    for i in range(len(xs)):
        num = ys[i]
        den = 1
        for j in range(len(xs)):
            if i != j:
                num = num * (x_eval - xs[j]) % p
                den = den * (xs[i] - xs[j]) % p
        result = (result + num * pow(den, p - 2, p)) % p
    return result


def W(x):
    r = 1
    for xj in xs:
        r = r * (x - xj) % p
    return r


print("[*] Calcul des bases Lagrange...")
g_0 = lagrange_eval(0)   # g(0)
W_0 = W(0)              
print(f"    g(0) = {hex(g_0)[:30]}...")
print(f"    W(0) = p - 120 = {W_0 == p - 120}\n")


print(f"[*] Brute-force (2^20 = {1 << 20} candidats/station)\n")

for xi, y_partial in flooded:
    g_xi    = lagrange_eval(xi)
    W_xi    = W(xi)
    W_xi_inv = pow(W_xi, p - 2, p)

    a5_base     = (y_partial - g_xi) * W_xi_inv % p
    secret      = (g_0 + a5_base * W_0) % p
    delta       = W_xi_inv * W_0 % p

    print(f"[*] Station x={xi}...")
    found = False

    for bits in range(1 << 20):
        try:
            nb   = (secret.bit_length() + 7) // 8 or 1
            flag = secret.to_bytes(nb, 'big').lstrip(b'\x00').decode('ascii')
            if hashlib.sha256(flag.encode()).hexdigest()[:16] == TARGET:
                print(f"    [+] TROUVÉ ! bits manquants = {bits} ({bits:#07x})")
                print(f"    [FLAG] {flag}\n")
                found = True
                break
        except (ValueError, UnicodeDecodeError):
            pass

        secret = (secret + delta) % p

    if not found:
        print(f"    [-] Non trouvé pour x={xi}\n")