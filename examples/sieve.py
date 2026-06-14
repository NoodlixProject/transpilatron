from time import perf_counter

def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = None
    is_prime[1] = None
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

start = perf_counter()
primes = sieve(10_000_000)
elapsed = perf_counter() - start

print(f"Found {len(primes)} primes")
print(f"Time: {elapsed:.3f}s")
