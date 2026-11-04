# cns.py - all 24 CNS lab programs in one file (run top to bottom; later cells reuse earlier definitions)


# ======================================================================
# 1. DECIMAL <-> BINARY <-> HEX  (no libraries needed in this whole notebook except 'random')
# To take input instead of hardcoding:  n = int(input("Enter number: "))
n = 57                                   # roll no

# --- Using built-in functions ---
print("binary:", bin(n))                 # '0b111001'  (0b means binary)
print("hex   :", hex(n))                 # '0x39'      (0x means hex)
print("binary -> decimal:", int("111001", 2))   # int(text, base)
print("hex    -> decimal:", int("39", 16))

# fraction part: multiply by 2, the integer part is the next bit (0.625 -> 0.101)
fraction = 0.625
bits = ""
while fraction > 0:
    fraction = fraction * 2
    bits += str(int(fraction))
    fraction = fraction - int(fraction)
print("0." + bits)


# ======================================================================
# 2. SUM OF ASCII CODES OF A STRING
# Input version:  text = input("Enter text: ")
text = "HELLO"

total = 0
for ch in text:
    print(ch, "=", ord(ch))              # ord('A')=65, ord('a')=97, chr(65)='A'
    total = total + ord(ch)
print("sum of ASCII =", total)
print("sum mod 57   =", total % 57)      # sums are often reduced with mod (used as a simple hash)

# REAL HASH instead of these toy ones (SHA-256, built into Python, nothing to install):
#   import hashlib
#   digest = hashlib.sha256(text.encode()).hexdigest()   # 64 hex characters
#   number = int(digest, 16) % n                         # hex -> big integer, then shrink it to fit small RSA/DSA numbers
#   hashlib.md5(...) and hashlib.sha1(...) are used the same way
# Hash used in signature cells below: position in alphabet (a=0, b=1 ...) added up, then +1
letters = "abcdefghijklmnopqrstuvwxyz"
h = 0
for ch in text.lower():
    h = h + letters.index(ch)
print("alphabet-position hash =", h + 1)


# ======================================================================
# 3. CAESAR CIPHER
# Encrypt: C = (P + key) mod 26        Decrypt: P = (C - key) mod 26
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
key = 57 % 26                            # = 5.  Input version: key = int(input())

def caesar(text, key):
    result = ""
    for ch in text.upper():
        if ch in letters:
            pos = letters.index(ch)              # A=0 ... Z=25
            result += letters[(pos + key) % 26]  # shift and wrap around
        else:
            result += ch                         # spaces stay as they are
    return result

cipher = caesar("ATTACK AT DAWN", key)
print(cipher)
print(caesar(cipher, -key))                      # decrypting = shifting backwards

# Brute force: only 26 possible keys, try all
for k in range(26):
    print(k, caesar(cipher, -k))


# ======================================================================
# 4. MONOALPHABETIC (SUBSTITUTION) CIPHER - every letter is replaced by another fixed letter
import random
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Option A: key = shuffled alphabet, shuffle is fixed by the seed 57
random.seed(57)
key = list(letters)
random.shuffle(key)
key = "".join(key)
# Option B: give your own key, e.g.  key = "QWERTYUIOPASDFGHJKLZXCVBNM"
print(letters)
print(key)

def mono_encrypt(text, key):
    result = ""
    for ch in text.upper():
        if ch in letters:
            result += key[letters.index(ch)]     # plain letter -> letter at same place in key
        else:
            result += ch
    return result

def mono_decrypt(text, key):
    result = ""
    for ch in text.upper():
        if ch in key:
            result += letters[key.index(ch)]     # opposite direction
        else:
            result += ch
    return result

cipher = mono_encrypt("HELLO WORLD", key)
print(cipher, mono_decrypt(cipher, key))
# Number of possible keys = 26! (too many to brute force, so use frequency analysis)


# ======================================================================
# 5. VIGENERE CIPHER
# Encrypt: C = (P + K) mod 26      Decrypt: P = (C - K) mod 26   (K = letter of the repeating key)
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def vigenere(text, keyword, direction):          # direction = 1 encrypt, -1 decrypt
    result = ""
    j = 0                                        # position in the keyword
    for ch in text.upper():
        if ch in letters:
            shift = letters.index(keyword[j % len(keyword)])   # key letter -> number
            result += letters[(letters.index(ch) + direction * shift) % 26]
            j += 1                               # move to next key letter (only for letters)
        else:
            result += ch
    return result

cipher = vigenere("ATTACK AT DAWN", "LEMON", 1)
print(cipher)                                    # LXFOPV EF RNHR
print(vigenere(cipher, "LEMON", -1))


# ======================================================================
# 6. PLAYFAIR CIPHER (5x5 table, I and J share a cell)
keyword = "MONARCHY"
letters = "ABCDEFGHIKLMNOPQRSTUVWXYZ"             # no J

total = keyword + letters
print("this is total", total)
print(f"this is total: {total}")
total = total.replace("J", "I")

# Step 1: build table = keyword letters (no repeats) + rest of alphabet
table = ""
for ch in total:
    if ch not in table:
        table += ch
for i in range(25):
    print(table[i], end="")
    if i % 5 == 4:                               # after every 5th letter
        print()                                  # new line

def find(ch):                                    # (row, column) of a letter
    index = table.index(ch)
    return index // 5, index % 5

# Step 2: make pairs. Same letter in a pair -> put X between. Odd length -> add X at the end
def make_pairs(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = "X"                              # odd length
        if a == b:
            b = "X"                              # repeated letter
            i += 1
        else:
            i += 2
        pairs.append(a + b)
    return pairs

# Step 3: encrypt each pair (shift = 1) or decrypt (shift = -1)
def play(pair, shift):
    r1, c1 = find(pair[0])
    r2, c2 = find(pair[1])
    if r1 == r2:                                 # same row    -> take letter to the right
        return table[r1*5 + (c1+shift) % 5] + table[r2*5 + (c2+shift) % 5]
    if c1 == c2:                                 # same column -> take letter below
        return table[((r1+shift) % 5)*5 + c1] + table[((r2+shift) % 5)*5 + c2]
    return table[r1*5 + c2] + table[r2*5 + c1]   # rectangle   -> swap the columns

pairs = make_pairs("BALLOONS ARE FUN TOMORROW")  # has LL, OO (repeat), odd length, all 3 rules
print(pairs)
cipher = [play(p, 1) for p in pairs]
print(cipher)
print([play(p, -1) for p in cipher])             # remove the extra X's by hand


# ======================================================================
# 7. HILL CIPHER (2x2) - encryption + decryption, K inverse given (from calculator, mod 26)
# Encrypt: C = K x P mod 26        Decrypt: P = K_inverse x C mod 26

K     = [[3, 3],
         [2, 5]]                     # key matrix
K_inv = [[15, 17],
         [20, 9]]                    # inverse key from calculator (mod 26)
text = "HELP"                        # plaintext

def hill(text, M):
    nums = []
    for ch in text.upper():
        nums.append(ord(ch) - 65)    # A=0 ... Z=25
    if len(nums) % 2 != 0:
        nums.append(23)              # pad with X

    result = ""
    for i in range(0, len(nums), 2):
        p1 = nums[i]
        p2 = nums[i+1]
        c1 = (M[0][0]*p1 + M[0][1]*p2) % 26
        c2 = (M[1][0]*p1 + M[1][1]*p2) % 26
        result += chr(c1 + 65) + chr(c2 + 65)
    return result

cipher = hill(text, K)               # encrypt with K
plain = hill(cipher, K_inv)          # decrypt with K inverse

print("cipher =", cipher)
print("plain  =", plain)


# ======================================================================
# 8. RAILWAY (RAIL FENCE) CIPHER - give every letter a row number (0,1,2,1,0,...), then read row by row
rails = 3                                        # key = number of rows (must be 2 or more)
text = "MEETMEAFTERTHEPARTY"                     # spaces removed

# one full zig-zag: down 0,1,2 then back up 1  ->  [0, 1, 2, 1]  (repeats for the whole text)
cycle = list(range(rails)) + list(range(rails - 2, 0, -1))
cycle = [0, 1, 2, 1]  # hardcoded for rails=3, 2 * (rails - 1)

# row number (tag) of every letter
pattern = []
for i in range(len(text)):
    pattern.append(cycle[i % len(cycle)])
print("cycle   =", cycle)
print("pattern =", pattern)

# ENCRYPT: collect the letters tagged 0, then tagged 1, then tagged 2
cipher = ""
for r in range(rails):
    for i in range(len(text)):
        if pattern[i] == r:
            cipher += text[i]
print("cipher  =", cipher)

# DECRYPT: positions in the order they were read, then put each cipher letter back
order = []
for r in range(rails):
    for i in range(len(text)):
        if pattern[i] == r:
            order.append(i)

plain = [""] * len(text)
for k in range(len(text)):
    plain[order[k]] = cipher[k]                  # k-th cipher letter goes back to position order[k]
print("plain   =", "".join(plain))

# show the zig-zag
for r in range(rails):
    line = ""
    for i in range(len(text)):
        if pattern[i] == r:
            line += text[i]
        else:
            line += "."
    print(line)


# ======================================================================
# 9. ONE TIME PAD - key is random, as long as the message and used only once
# Letter version: C = (P + K) mod 26,  P = (C - K) mod 26
import random
random.seed(57)                                  # same "random" key every run
text = "HELLO"                                   # input: text = input()

key = []
for i in range(len(text)):
    key.append(random.randint(0, 25))            # one random number per letter
cipher = ""
plain = ""
for i in range(len(text)):
    cipher += chr((ord(text[i]) - 65 + key[i]) % 26 + 65)
for i in range(len(text)):
    plain += chr((ord(cipher[i]) - 65 - key[i]) % 26 + 65)
print(key, cipher, plain)

# Binary (XOR) version: C = P xor K, and xor again with K gives P back
cipher_nums = []
for i in range(len(text)):
    k = random.randint(0, 255)
    cipher_nums.append(ord(text[i]) ^ k)         # ^ is XOR
    print(text[i], format(ord(text[i]), "08b"), "xor", format(k, "08b"), "=", format(cipher_nums[-1], "08b"))


# ======================================================================
# 10. EXTENDED EUCLIDEAN ALGORITHM (table method):  gcd(a, b) = a*s + b*t
# Table columns: q | r1 r2 r | s1 s2 s | t1 t2 t
# Every row:  q = r1 // r2 ,  r = r1 - q*r2 ,  s = s1 - q*s2 ,  t = t1 - q*t2
# Next row:   r1 = r2, r2 = r  (same shift for s and t).  Stop when r2 = 0

a, b = 161, 28                                   # input: a, b = int(input()), int(input())

r1, r2 = a, b                                    # first row of the table
s1, s2 = 1, 0
t1, t2 = 0, 1

print("q    r1   r2   r    s1   s2   s    t1   t2   t")
print("-   ", r1, " ", r2, " ", "-", "  ", s1, "  ", s2, "  ", "-", "  ", t1, "  ", t2, "  ", "-")
while r2 != 0:
    q = r1 // r2
    r = r1 - q * r2
    s = s1 - q * s2
    t = t1 - q * t2
    print(q, "   ", r1, " ", r2, " ", r, "  ", s1, "  ", s2, "  ", s, "  ", t1, "  ", t2, "  ", t)
    r1, r2 = r2, r                               # shift to the next row
    s1, s2 = s2, s
    t1, t2 = t2, t

print("gcd =", r1, " s =", s1, " t =", t1)       # a*s + b*t = gcd
print("check:", a * s1 + b * t1)                 # must equal the gcd
if r1 == 1:
    print("inverse of", a, "mod", b, "=", s1 % b)   # if gcd = 1, s (made positive) is the inverse of a mod b
else:
    print("gcd is not 1, so", a, "has no inverse mod", b)


# ======================================================================
# 11. CHINESE REMAINDER THEOREM  x = a1 mod m1, x = a2 mod m2 ... (m's must be coprime)
a = [2, 3, 2]                                    # remainders
m = [3, 5, 7]                                    # moduli

M = 1
for mi in m:
    M = M * mi                                   # M = m1 x m2 x m3
print("M =", M)

x = 0
for i in range(len(m)):
    Mi = M // m[i]                               # Mi = M / mi
    yi = pow(Mi, -1, m[i])                       # yi = inverse of Mi mod mi
    print("Mi =", Mi, " yi =", yi, " a*Mi*yi =", a[i] * Mi * yi)
    x += a[i] * Mi * yi                       # x = sum of a_i x Mi x yi
print("x =", x % M)                              # final answer = sum mod M


# ======================================================================
# 12. FERMAT AND EULER PRIMALITY TESTS
# Fermat: if n is prime then a^(n-1) mod n = 1
def fermat(n, a):
    return pow(a, n - 1, n) == 1

# Euler: if n is prime then a^((n-1)/2) mod n = 1 or -1   (-1 is written as n-1 because pow gives 0..n-1)
def euler(n, a):
    x = pow(a, (n - 1) // 2, n)
    return x == 1 or x == n - 1

for n in [17, 21, 561]:                          # prime, composite, Carmichael number
    print(n, "Fermat a=2:", fermat(n, 2), " Euler a=2:", euler(n, 2))
# 561 = 3*11*17 is composite, but with a=2 both tests wrongly say True (Carmichael number); Rabin-Miller (next cell) catches it


# ======================================================================
# 13. RABIN-MILLER + PRIMITIVE ROOTS + DISCRETE LOG
# --- Rabin-Miller: is n prime?  write n-1 = 2^k x m  (m odd) ---
# b0 = a^m mod n,  b1 = b0^2 mod n,  b2 = b1^2 mod n ...   if b0 = 1 or some b = -1 (n-1) -> probably prime
def miller_rabin(n, a):
    m = n - 1
    k = 0
    while m % 2 == 0:                            # n-1 = 2^k x m
        m = m // 2
        k += 1
    b = pow(a, m, n)                             # b0 = a^m mod n
    print("n-1 = 2^" + str(k), "x", m, " b0 =", b)
    if b == 1 or b == n - 1:
        return True
    for i in range(1, k):
        b = (b * b) % n                          # b_i = b_(i-1)^2 mod n
        print("b" + str(i), "=", b)
        if b == n - 1:
            return True
    return False

for n in [97, 57, 561]:
    print(n, "->", miller_rabin(n, 2))

# --- Primitive root of prime p: its powers g^1 ... g^(p-1) give every number 1..p-1 ---
p = 23
roots = []
for g in range(2, p):
    powers = []
    for k in range(1, p):
        powers.append(pow(g, k, p))
    if len(set(powers)) == p - 1:                # all different -> primitive root
        roots.append(g)
print("primitive roots of", p, "=", roots)

# --- Discrete log: find x so that g^x mod p = h ---
g = 5
h = 57 % p                                       # = 11
for x in range(1, p):
    if pow(g, x, p) == h:
        print("log of", h, "base", g, "mod", p, "=", x)
        break


# ======================================================================
# 14. RSA
# n = p x q      phi = (p-1)(q-1)      e: gcd(e, phi) = 1      d = e^-1 mod phi
# Encrypt: C = M^e mod n       Decrypt: M = C^d mod n
p, q = 53, 61                                    # two primes (input version: p = int(input()))
message = 57                                     # must be smaller than n

n = p * q
phi = (p - 1) * (q - 1)
e = 17                                           # public exponent, should have gcd(e, phi) = 1
d = pow(e, -1, phi)                              # private exponent (modular inverse)
print("n =", n, "phi =", phi, "d =", d)
print("public key (e, n) =", (e, n), " private key (d, n) =", (d, n))

cipher = pow(message, e, n)                      # encrypt with public key
print("cipher =", cipher)
print("decrypted =", pow(cipher, d, n))          # decrypt with private key


# ======================================================================
# 15. RSA WITH PROBABILISTIC PRIME GENERATION: pick random numbers, keep one only if Rabin-Miller says "prime"
import random
random.seed(57)

# Rabin-Miller with base a = 2:  n-1 = 2^k x m,  b0 = a^m mod n,  b1 = b0^2 mod n ...  b = 1 or -1 (n-1) -> probably prime
def rabin_miller(n, a):
    m = n - 1
    k = 0
    while m % 2 == 0:                            # n-1 = 2^k x m
        m = m // 2
        k += 1
    b = pow(a, m, n)                             # b0 = a^m mod n
    if b == 1 or b == n - 1:
        return True
    for i in range(1, k):
        b = (b * b) % n                          # b_i = b_(i-1)^2 mod n
        if b == n - 1:
            return True
    return False

def random_prime():
    while True:
        number = random.randint(2 ** 15, 2 ** 16)    # random 16-bit number
        if rabin_miller(number, 2):                  # test with base 2 only
            return number

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

p = random_prime()
q = random_prime()
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
while gcd(e, phi) != 1:                          # e must be coprime with phi
    e += 2
d = pow(e, -1, phi)
print("p =", p, "q =", q, "n =", n, "e =", e, "d =", d)
cipher = pow(57, e, n)
print("cipher =", cipher, " decrypted =", pow(cipher, d, n))


# ======================================================================
# 16. DIFFIE-HELLMAN KEY EXCHANGE
p = 353                                          # public prime
g = 3                                            # public primitive root of p
a = 57                                           # Alice's secret
b = 233                                          # Bob's secret

A = pow(g, a, p)                                 # Alice sends A = g^a mod p
B = pow(g, b, p)                                 # Bob sends   B = g^b mod p
print("A =", A, "B =", B)
print("Alice's key =", pow(B, a, p))             # B^a mod p
print("Bob's key   =", pow(A, b, p))             # A^b mod p   (both equal g^(ab) mod p)


# ======================================================================
# 17. ELGAMAL ENCRYPTION
p = 467                                          # public prime
g = 2                                            # primitive root
x = 57                                           # receiver's private key
y = pow(g, x, p)                                 # receiver's public key  y = g^x mod p

message = 100                                    # must be less than p
k = 153                                          # sender's random number

c1 = pow(g, k, p)                                # c1 = g^k mod p
c2 = (message * pow(y, k, p)) % p                # c2 = M x y^k mod p
print("public key y =", y, " cipher =", (c1, c2))

s = pow(c1, x, p)                                # s = c1^x mod p  (same as y^k)
print("decrypted =", (c2 * pow(s, -1, p)) % p)   # M = c2 x s^-1 mod p


# ======================================================================
# 18. ELLIPTIC CURVE ARITHMETIC   y^2 = x^3 + a*x + b (mod p)
p = 17
a = 2
b = 2
G = (5, 1)                                       # generator point
order = 19                                       # kG = O (infinity) for k = 19

def add(P, Q):
    if P is None:                                # None means point at infinity (like 0)
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:          # P + (-P) = infinity
        return None
    if P == Q:
        slope = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p)) % p   # doubling: (3x^2 + a) / 2y
    else:
        slope = ((y2 - y1) * pow(x2 - x1, -1, p)) % p          # adding:  (y2 - y1) / (x2 - x1)
    x3 = (slope * slope - x1 - x2) % p           # x3 = slope^2 - x1 - x2
    y3 = (slope * (x1 - x3) - y1) % p            # y3 = slope (x1 - x3) - y1
    return (x3, y3)

def multiply(k, P):                              # k x P by repeated doubling and adding
    result = None
    while k > 0:
        if k % 2 == 1:
            result = add(result, P)
        P = add(P, P)
        k = k // 2
    return result

for k in range(1, 20):
    print(k, "G =", multiply(k, G))              # lists all points of the curve

# Check a point is on the curve:  y^2 = x^3 + ax + b
x, y = G
print((y * y) % p == (x ** 3 + a * x + b) % p)

# Diffie-Hellman with curves (private keys must be less than the order 19)
na, nb = 7, 11
Pa = multiply(na, G)
Pb = multiply(nb, G)
print(multiply(na, Pb), multiply(nb, Pa))        # same shared point


# ======================================================================
# 19. ELLIPTIC CURVE ELGAMAL (message is turned into a point M x G)
# Needs add() and multiply() from the previous cell
private_key = 7                                  # receiver's secret (less than 19)
public_key = multiply(private_key, G)            # P = n x G
message = 5                                      # small number as message (less than 19)
k = 3                                            # sender's random number

message_point = multiply(message, G)             # Pm = M x G
c1 = multiply(k, G)                              # C1 = k x G
c2 = add(message_point, multiply(k, public_key)) # C2 = Pm + k x P
print("cipher =", (c1, c2))

shared = multiply(private_key, c1)               # n x C1
minus_shared = (shared[0], (-shared[1]) % p)     # negative of a point = (x, -y)
decoded = add(c2, minus_shared)                  # Pm = C2 - n x C1
for i in range(1, 20):                           # find which i gives this point
    if multiply(i, G) == decoded:
        print("decrypted message =", i)


# ======================================================================
# 20. DIGITAL SIGNATURE - RSA   (sign with private key d, verify with public key e)
letters = "abcdefghijklmnopqrstuvwxyz"
# REAL HASH (instead of this toy one): add  import hashlib  at the top, then
#   h = int(hashlib.sha256(message.encode()).hexdigest(), 16)   # SHA-256 as a big number
#   (hashlib.md5 / hashlib.sha1 work the same way)
# Our primes are tiny, so shrink it:  h = h % n   (RSA)  /  h % q  (DSA)  /  h % (p-1)  (ElGamal)
def hash_message(message):                       # simple hash: alphabet positions added, +1
    h = 0
    for ch in message.lower():
        h = h + letters.index(ch)
    return h + 1

p, q = 11, 13
n = p * q
phi = (p - 1) * (q - 1)
e = 7
d = pow(e, -1, phi)

h = hash_message("hello")
signature = pow(h, d, n)                         # S = H^d mod n
print("hash =", h, "signature =", signature)
print("verify:", pow(signature, e, n) == h % n)  # S^e mod n must equal H


# ======================================================================
# 21. DIGITAL SIGNATURE - ELGAMAL
letters = "abcdefghijklmnopqrstuvwxyz"
# REAL HASH (instead of this toy one): add  import hashlib  at the top, then
#   h = int(hashlib.sha256(message.encode()).hexdigest(), 16)   # SHA-256 as a big number
#   (hashlib.md5 / hashlib.sha1 work the same way)
# Our primes are tiny, so shrink it:  h = h % n   (RSA)  /  h % q  (DSA)  /  h % (p-1)  (ElGamal)
def hash_message(message):
    h = 0
    for ch in message.lower():
        h = h + letters.index(ch)
    return h + 1

p = 23
g = 5
x = 6                                            # private key
y = pow(g, x, p)                                 # public key
k = 7                                            # random number, gcd(k, p-1) must be 1

h = hash_message("hello")
r = pow(g, k, p)                                 # r = g^k mod p
s = (pow(k, -1, p - 1) * (h - x * r)) % (p - 1)  # s = k^-1 (H - x r) mod (p-1)
print("signature =", (r, s))

left = pow(g, h, p)                              # verify: g^H mod p
right = (pow(y, r, p) * pow(r, s, p)) % p        #         y^r x r^s mod p
print("verify:", left == right)


# ======================================================================
# 22. DIGITAL SIGNATURE - DSA
letters = "abcdefghijklmnopqrstuvwxyz"
# REAL HASH (instead of this toy one): add  import hashlib  at the top, then
#   h = int(hashlib.sha256(message.encode()).hexdigest(), 16)   # SHA-256 as a big number
#   (hashlib.md5 / hashlib.sha1 work the same way)
# Our primes are tiny, so shrink it:  h = h % n   (RSA)  /  h % q  (DSA)  /  h % (p-1)  (ElGamal)
def hash_message(message):
    h = 0
    for ch in message.lower():
        h = h + letters.index(ch)
    return h + 1

p = 23
q = 11                                           # q divides p-1
g = 4                                            # g = h^((p-1)/q) mod p
x = 3                                            # private key (less than q)
y = pow(g, x, p)                                 # public key
k = 4                                            # random number (less than q)

h = hash_message("hi") % q
r = pow(g, k, p) % q                             # r = (g^k mod p) mod q
s = (pow(k, -1, q) * (h + x * r)) % q            # s = k^-1 (H + x r) mod q
print("signature =", (r, s))

w = pow(s, -1, q)                                # verify: w = s^-1 mod q
u1 = (h * w) % q                                 # u1 = H x w mod q
u2 = (r * w) % q                                 # u2 = r x w mod q
v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q    # v = (g^u1 x y^u2 mod p) mod q
print("verify:", v == r)


# ======================================================================
# 23. DIGITAL SIGNATURE - ECDSA (elliptic curve version of DSA)
letters = "abcdefghijklmnopqrstuvwxyz"
# REAL HASH (instead of this toy one): add  import hashlib  at the top, then
#   h = int(hashlib.sha256(message.encode()).hexdigest(), 16)   # SHA-256 as a big number
#   (hashlib.md5 / hashlib.sha1 work the same way)
# Our curve is tiny, so shrink it:  h = h % n   where n = order of G (19 here).
# (Real ECDSA uses the leftmost bits of the hash; for exam-size curves h % n is the simple way.)
def hash_message(message):
    h = 0
    for ch in message.lower():
        h = h + letters.index(ch)
    return h + 1

p, a = 17, 2
G = (5, 1)
n = 19                                           # order of G

def add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        slope = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p)) % p
    else:
        slope = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)

def multiply(k, P):
    result = None
    while k > 0:
        if k % 2 == 1:
            result = add(result, P)
        P = add(P, P)
        k = k // 2
    return result

d = 7                                            # private key
Q = multiply(d, G)                               # public key Q = d x G
k = 3                                            # random number

h = hash_message("hello")
point = multiply(k, G)                           # k x G
r = point[0] % n                                 # r = x-coordinate mod n
s = (pow(k, -1, n) * (h + d * r)) % n            # s = k^-1 (H + d r) mod n
print("signature =", (r, s))

w = pow(s, -1, n)                                # verify: w = s^-1 mod n
u1 = (h * w) % n
u2 = (r * w) % n
P = add(multiply(u1, G), multiply(u2, Q))        # P = u1 x G + u2 x Q
print("verify:", P[0] % n == r)


# ======================================================================
# 24. DIGITAL SIGNATURE - RSA-PSS (Probabilistic Signature Scheme, simplified)
# Plain RSA (cell 20) signs the hash directly. PSS first builds a padded block EM from the hash and a RANDOM salt, then signs EM:
#   Sign:    S = EM^d mod n
#   Verify:  EM = S^e mod n, then check the padding and recompute the hash
import hashlib
import random
from math import gcd
random.seed(57)

# ---- RSA keys: two 256-bit primes, so n is about 512 bits (64 bytes) ----
def rabin_miller(n, a):
    m = n - 1
    k = 0
    while m % 2 == 0:                            # n-1 = 2^k x m
        m = m // 2
        k += 1
    b = pow(a, m, n)                             # b0 = a^m mod n
    if b == 1 or b == n - 1:
        return True
    for i in range(1, k):
        b = (b * b) % n
        if b == n - 1:
            return True
    return False

def random_prime(bits):
    while True:
        number = random.getrandbits(bits) | (1 << (bits - 1)) | 1    # force full length and odd
        if rabin_miller(number, 2):
            return number

p = random_prime(256)
q = random_prime(256)
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
while gcd(e, phi) != 1:
    e += 2
d = pow(e, -1, phi)

# ---- PSS sizes (in bytes) ----
hLen = 32                                        # SHA-256 output length
sLen = 16                                        # salt length
emLen = 63                                       # EM must be smaller than n (n is 64 bytes)

def mgf1(seed, length):                          # mask generator: stretches a hash to any length
    out = b""
    counter = 0
    while len(out) < length:
        out += hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]

def xor(a, b):                                   # xor two byte strings
    return bytes(x ^ y for x, y in zip(a, b))

def pss_sign(message):
    mHash = hashlib.sha256(message.encode()).digest()                    # 1. hash the message
    salt = random.getrandbits(8 * sLen).to_bytes(sLen, "big")            # 2. fresh random salt every time
    H = hashlib.sha256(b"\x00" * 8 + mHash + salt).digest()              # 3. H = hash(8 zero bytes + mHash + salt)
    DB = b"\x00" * (emLen - sLen - hLen - 2) + b"\x01" + salt            # 4. DB = zeros + 01 + salt
    maskedDB = xor(DB, mgf1(H, len(DB)))                                 # 5. hide DB with a mask made from H
    EM = maskedDB + H + b"\xbc"                                          # 6. EM = maskedDB + H + bc
    return pow(int.from_bytes(EM, "big"), d, n)                          # 7. S = EM^d mod n

def pss_verify(message, S):
    mHash = hashlib.sha256(message.encode()).digest()
    m = pow(S, e, n)                                                     # 1. undo the signature: EM = S^e mod n
    if m >= 256 ** emLen:
        return False
    EM = m.to_bytes(emLen, "big")
    if EM[-1] != 0xbc:                                                   # 2. last byte must be bc
        return False
    maskedDB = EM[:emLen - hLen - 1]
    H = EM[emLen - hLen - 1:emLen - 1]
    DB = xor(maskedDB, mgf1(H, len(maskedDB)))                           # 3. remove the mask, get DB back
    salt = DB[-sLen:]                                                    # 4. salt is the last sLen bytes of DB
    padding_ok = DB[:-sLen] == b"\x00" * (len(DB) - sLen - 1) + b"\x01"  # 5. DB must be zeros then 01
    return padding_ok and hashlib.sha256(b"\x00" * 8 + mHash + salt).digest() == H   # 6. recompute H and compare

S1 = pss_sign("hello")
S2 = pss_sign("hello")
print("signature 1 =", hex(S1)[:40], "...")
print("signature 2 =", hex(S2)[:40], "...")
print("same signature twice?", S1 == S2)             # False, because the salt is random
print("verify hello:", pss_verify("hello", S1), pss_verify("hello", S2))
print("verify hellp:", pss_verify("hellp", S1))      # message changed -> False
