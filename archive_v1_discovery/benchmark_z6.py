import numpy as np

def compute_precise_depth(t_zero, N):
    # Using the precise formula from the research logic
    # Depth = Average_Background / Minimum_at_Zero
    
    n = np.arange(1, N + 1)
    
    def get_val(t):
        S = np.sum(n**(-0.5 + 1j * t))
        mag = np.abs(S) / np.sqrt(N)
        return mag

    # Calculate zero magnitude
    val_zero = get_val(t_zero)
    
    # Calculate background magnitude in a wider window
    # We take 100 points in t_zero +/- 0.5
    background_points = np.linspace(t_zero - 0.5, t_zero + 0.5, 100)
    vals = [get_val(t) for t in background_points]
    
    mean_val = np.mean(vals)
    min_val = np.min(vals)
    depth = mean_val / (min_val + 1e-15)
    
    return depth, min_val

if __name__ == "__main__":
    # Z6 from research records
    z6 = 37.5861781588
    n_test = 20
    
    # Micro-scan to find the absolute minimum point
    scan_points = np.linspace(z6 - 0.001, z6 + 0.001, 1000)
    n = np.arange(1, n_test + 1)
    mags = [np.abs(np.sum(n**(-0.5 + 1j * t))) / np.sqrt(n_test) for t in scan_points]
    true_z6 = scan_points[np.argmin(mags)]
    
    depth, min_val = compute_precise_depth(true_z6, n_test)
    print(f"Z6 Center found at: {true_z6:.12f}")
    print(f"Calculated Depth: {depth:.2f}")
    print(f"Minimum Magnitude found: {min_val:.6e}")
    print("-" * 30)
    print("Target Depth from Research: 712.37")
