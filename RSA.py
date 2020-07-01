import random
import math

neg = 10000 # global variable for jacobi. should be 1 or -1 after use

def generate_public_key (num_bits):
    ar = []
    i = 0
    while len(ar) < 2:
        i += 1
        num = random.getrandbits(int(num_bits/2))
        if (num%2==0):
            continue
        fpt = SS_primality(num, 5)
        if fpt:
            ar.append(num)
            print("Primes: {}/2 (count = {})".format(len(ar), i) )


    p = ar[0]
    q = ar[1]
    n = p*q
    phi_n = (p-1) * (q-1)
    e = get_random_coprime (phi_n)

    d = modinv(e, phi_n)

    return n, e, d

def phi(n):
    totient = n
    for factor in prime_factors(n):
        totient -= totient // factor
    return totient

def get_random_coprime (n):
    a = random.randrange(2, n+1)

    while math.gcd(a, n) != 1:
        a = random.randrange(2, n + 1)

    return a

def modinv(a, m):
    return pow(a, -1, m)

def modular_exp (a, x, m):
    ar = [a]
    exp = 2
    num = a
    while exp < x:
        num = num ** 2 % m
        exp *= 2
        ar.append(num)

    x_b = bin(x)[2:][::-1]
    n = 1
    for i in range(len(x_b)):
        if int(x_b[i]) == 1:
            n *= ar[i] % m
    n = n % m
    return n

def SS_single_primality (n, a):
    if a <= 1 or a >= n-1:
        raise Exception("Invalid value of a")

    if math.gcd(a, n) != 1:
        return False

    eu = modular_exp (a, int((n-1)//2), n)
    if eu != 1 and eu != n-1:
        return False

    jac = jac2(a, n)

    if jac % n != eu:
        return False

    return True


def SS_primality (n, t):
    for _ in range(t):
        a = random.randrange(2, n-1)
        if not SS_single_primality(n, a):
            return False

    return True


def jac2(a, n):
    if a == 1:
        return 1
    if a % 2 == 0:
        neg = 1
        if n % 8 == 3 or n % 8 == 5:
            neg = -1
        return neg*jac2( int(a//2), n )
    if n % 2 != 0:
        neg = 1
        if a % 4 == 3 and n % 4 == 3:
            neg = -1
        return neg*jac2( n % a, a )

    else:
        return 0

def ascii_to_str(hex_str):
    return bytes.fromhex(hex_str).decode('utf-8')

def str_to_ascii(str):
    return [ord(c) for c in str]


print ("---------------------------")

b = True

sep = 214

while b:
    b = False
    inp = input("User.. Do you want to: \na) Create a public Key?\nb) Encrypt Plaintext? or\nc) Decrypt Ciphertext?\n")
    if inp == 'a':
        size = int(input("Enter Num Bits.\n"))
        print("Generating Key...")
        num_bits = size
        k1, k2, d = generate_public_key(num_bits)
        print("n:", k1)
        print("e:", k2)
        print("d:", d)

    elif inp == 'b':
        filename = input("Enter Filename.\n")
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        n = int(content[0].partition(' ')[0])
        e = int(content[0].partition(' ')[2])

        message = [content[i] for i in range(1, len(content))]

        print(message)
        print(len(message))
        nums = []
        for line in message:
            num = str_to_ascii(line)
            nums.append(num)

        tx = "0x"
        for nu in nums:
            for el in nu:
                tx += hex(el)[2:]

        print(tx)
        s = tx[2:]

        indices = [i * sep for i in range(int(len(s) / sep) + 1)]
        parts = [s[i:j] for i, j in zip(indices, indices[1:] + [None])]

        texes = parts

        print("Len: ", len(texes))
        for tex in texes:
            numb = int(tex, 16)
            print (modular_exp(numb, e, n))

    elif inp == 'c':
        filename = input("Enter Filename.\n")
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        n = int(content[0].partition(' ')[0])
        d = int(content[0].partition(' ')[2])

        nums = [content[i] for i in range(1, len(content))]

        for el in nums:
            for i in range(len(nums)):
                nums[i] = int(nums[i])
                nums[i] = modular_exp(nums[i], d, n)

            tx = "0x"
            for el in nums:
                tx += hex(el)[2:]

            messages = []
            for i in range(1, len(tx)):
                b_hex = tx[2 * i:2 * i + 2]
                c = ascii_to_str(b_hex)
                messages.append(c)

            print(''.join(messages))

    else:
        b = True

