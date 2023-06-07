def get_prime(n):
    prime = 2
    count = 0
    while count < n:
        prime += 1
        for i in range(2, int(prime ** 1/2) + 1):
            if prime % i == 0:
                break
        else:
            count += 1
    return prime

def calculate_const(len_of_list:int, root:int):
    """Calculates the K and H Constants used in the SHA-256 algorithm."""
    C = []
    for i in range(0,len_of_list):
        prime = get_prime(i)
        prime = prime ** (1/root)
        prime = prime - int(prime) 
        prime = int((prime * (2**32)) % (2**32))   
        C.append(prime)

    return C


if __name__ == "__main__":
    import pickle

    print("\n####################################################################################################")
    print("Constants K, First 32 bits of the fractional parts of the cube roots of the first 64 primes:\n")
    K = calculate_const(64, 3)
    k = []

    for i in K:
        k.append(hex(i))
    
    print(k)


    print("\n####################################################################################################")
    print("Hash Values, First 32 bits of the fractional parts of the square roots of the first 8 primes:")
    H = calculate_const(8, 2)
    h = []
    for i in H:
        h.append(hex(i))
    
    print(h)


    with open("constants.pkl", "wb") as f:
        pickle.dump(K, f)

    with open("hashes.pkl", "wb") as f:
        pickle.dump(H, f)