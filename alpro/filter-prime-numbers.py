
# Nomor 2
def find_primes(arr):
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    primes = []
    for num in arr:
        if is_prime(num):
            primes.append(num)
    return primes

print(find_primes([10, 15, 2, 3, 5, 7, 8, 11, 13, 14]))
