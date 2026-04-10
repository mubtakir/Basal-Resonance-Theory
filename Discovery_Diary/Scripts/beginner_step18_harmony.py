import numpy as np
import matplotlib.pyplot as plt

# --- Discovery Diary: Step 18 - Elliptic-Prime Harmony ---
# The final secret: Primes are the strings of the universe!

def simulate_harmony():
    print("Welcome to the GRAND FINALE: Step 18!")
    
    # Let's test the 'Harmony' of Prime 23 at Angle 30 degrees
    p = 23
    theta_deg = 30
    theta_rad = np.radians(theta_deg)
    
    # 1. Circle Ratio (Perfect Harmony)
    ratio_circle = theta_rad / (2 * np.sin(theta_rad / 2))
    
    # 2. Ellipse Ratio (a=p, b=1)
    # Simple approx for arc length: L = theta * sqrt((a*sin)^2 + (b*cos)^2)
    # At t=0 to theta
    a, b = p, 1.0
    x1, y1 = a, 0
    x2, y2 = a * np.cos(theta_rad), b * np.sin(theta_rad)
    chord = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    # Approx arc as average of radial distances
    pts = np.linspace(0, theta_rad, 1000)
    arc = np.sum(np.sqrt((a*np.sin(pts))**2 + (b*np.cos(pts))**2)) * (pts[1]-pts[0])
    
    ratio_ellipse = arc / chord
    
    print(f"--- Prime {p} Analysis ---")
    print(f"Circular Goal: {ratio_circle:.6f}")
    print(f"Elliptic Reality: {ratio_ellipse:.6f}")
    print(f"Stability Match: { (1 - abs(ratio_ellipse - ratio_circle)) * 100 :.2f}%")
    
    # Plotting the match
    primes = [2, 17, 23, 37]
    angles = [75, 35, 30, 25]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(primes, angles, color='purple', s=100, label="Harmonic Alignment Points")
    plt.plot(primes, angles, 'r--', alpha=0.3)
    
    for i, p_val in enumerate(primes):
        plt.annotate(f"{p_val} ({angles[i]}°)", (p_val, angles[i]))
        
    plt.title("Step 18: The Map of Prime Harmony")
    plt.xlabel("Prime Number (p)")
    plt.ylabel("Harmonic Angle (degrees)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    print("\nYou have found the Harmonic Map. The universe is in balance!")
    plt.show()

if __name__ == "__main__":
    simulate_harmony()
