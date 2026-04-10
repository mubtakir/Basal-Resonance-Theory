import numpy as np
import matplotlib.pyplot as plt

def get_prime_group_numbers(limit):
    """Generate numbers formed by primes 2, 5, 7, 17 up to limit."""
    primes = [2, 5, 7, 17]
    nums = {1}
    for p in primes:
        new_nums = set()
        for n in nums:
            temp = n
            while temp * p <= limit:
                temp *= p
                new_nums.add(temp)
        nums.update(new_nums)
    return sorted(list(nums))

def test_hypothesis(t_zero, N_limit):
    # Group 1: Numbers from the "Prime Group" {2, 5, 7, 17}
    prime_group = get_prime_group_numbers(N_limit)
    # Remove very small N
    prime_group = [n for n in prime_group if n > 10]
    
    # Group 2: Random numbers (sampling same size)
    random_group = np.random.randint(11, N_limit, size=len(prime_group))
    
    def get_errors(group):
        errors = []
        for N in group:
            n = np.arange(1, N + 1)
            S = np.sum(n**(-0.5 + 1j * t_zero))
            emp = np.abs(S) / np.sqrt(N)
            theo = 1.0 / np.sqrt(0.25 + t_zero**2)
            errors.append(np.abs(emp - theo))
        return np.array(errors)

    print(f"Testing Prime Group Hypothesis (Size: {len(prime_group)}) at t={t_zero}")
    
    errors_prime = get_errors(prime_group)
    errors_rand = get_errors(random_group)
    
    print(f"Prime Group Mean Error: {np.mean(errors_prime):.8f}")
    print(f"Random Group Mean Error: {np.mean(errors_rand):.8f}")
    
    ratio = np.mean(errors_rand) / np.mean(errors_prime)
    print(f"Hypothesis Score (Random/Prime Error Ratio): {ratio:.2f}x")
    
    if ratio > 1.0:
        print("✅ SUCCESS: The Prime Group {2, 5, 7, 17} produces cleaner resonance!")
    else:
        print("❌ FAILED: No significant advantage found for the Prime Group.")

if __name__ == "__main__":
    t_one = 14.13472514173469
    test_hypothesis(t_one, N_limit=100000)
