import numpy as np
import matplotlib.pyplot as plt

# --- Discovery Diary: Step 16 - Riemann's Wire (RLC) ---
# Every prime is like a resistor in a magical cosmic wire.

def simulate_riemann_wire(num_primes=50):
    print("Welcome to Step 16: The RLC Transmission Line!")
    
    # 1. Primes and their resistance (log scale)
    # The 'Impedance' of a prime p is proportional to log(p)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    log_p = np.log(primes)
    
    # 2. Resonance Pulse
    # In an RLC circuit, resonance happens at a specific frequency
    # For Zeta, this frequency is the Z-zero (t approx 14.13)
    t = 14.1347
    
    # 3. Phase Shift
    # Delta Phase = t * log(p)
    phases = t * log_p
    
    # Plotting the 'Pulse' of the wire
    plt.figure(figsize=(10, 6))
    plt.stem(primes, np.sin(phases), basefmt=" ", label="Resonance Pulse (sin(t*ln p))")
    plt.plot(primes, np.sin(phases), 'r--', alpha=0.3)
    
    plt.title("Step 16: The Heartbeat of Riemann's Wire")
    plt.xlabel("Prime Number (p)")
    plt.ylabel("Pulse Amplitude")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    print(f"Notice how the 'Pulse' oscillates but follows a predictable path.")
    print(f"This is how information travels through the primes!")
    
    plt.show()

if __name__ == "__main__":
    simulate_riemann_wire()
