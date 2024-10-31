import time

def count_primes(n):
    if n < 2:
        return 0
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return sum(is_prime)

if __name__ == "__main__":
    n = 100000000
    start_time = time.time()
    prime_count = count_primes(n)
    end_time = time.time()
    duration = end_time - start_time

    print(f"Number of primes between 1 and {n}: {prime_count}")
    print(f"Time taken: {duration} seconds")