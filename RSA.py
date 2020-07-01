import random
import math

neg = 10000 # global variable for jacobi. should be 1 or -1 after use

def generate_public_key (num_bits):
    ar = []
    i = 0
    while len(ar) < 2:
        i += 1
        num = random.getrandbits(num_bits)
        fpt = SS_primality(num, 5)
        if fpt:
            ar.append(num)

    p = ar[0]
    q = ar[1]
    n = p*q
    phi_n = (p-1) * (q-1)
    e = get_random_coprime (phi_n)

    d = modinv(e, phi_n)
    # print(e, phi_n, d)

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
        # print("A")
        return False

    eu = modular_exp (a, int((n-1)//2), n)
    if eu != 1 and eu != n-1:
        # print("B")
        return False

    jac = jac2(a, n)

    if jac % n != eu:
        # print("C")
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


# print(SS_primality(171424828496904907443952456616018360467868529363671755984187360030210677848706583927997885120919935350336610851429951495185293260866942640292575031085488461453718404764797919247112357921076234563660516650063210932496325210299421741785404703569069054478785342946614697847055005333761582696434628547499577456893, 50))
#
# print("---")
#
# a = 11974210996840806680435443068402451770602156406704452044825634210662326861932463119592310392269051388285581404285089487154765291175104285889137301707147437202661621311924785574623584730009130290368272926580025764039382097461460477316218919306238819962950241625643257110222820774966110620409660144189875152707
# n = 40039545748783331279163062941531462006638565672722268800153468920915478412465033451942497820462007050213688069953171041013571440623817499542813968152349109839769214999043711066176997207100291483595492437310539006037030219943186613121226685014864252335257624175497703857719000410372454213220379468678395331686
#
# print(jac2(a, n))


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

        # for line in message:
        #     if line == '':
        #         message.remove(line)

        print(message)
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

            # print(nums)

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

