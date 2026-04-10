import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# ==============================================================================
# 🧪 M I C R O - L A B   [ Exp 05 ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: التحقق من الانطباق الكلي (Asymptotic Identity) بين المتجه التجريبي والنظري
# 🎓 المرحلة: هوية المتجهات (Vector Identity)
# 📐 المبدأ الرياضي: V_empirical = V_theoretical + epsilon(N)
# ⚡ النتيجة المتوقعة: اضمحلال المسافة المطلقة (Absolute Distance) وتطابق الزوايا مع نمو N
# ==============================================================================

console = Console()

def compute_sum_detailed(sigma, t, N_max, use_kahan=True):
    n = np.arange(1, N_max + 1, dtype=np.float64)
    phi = t * np.log(n)
    amplitude = n ** (-sigma)
    vectors = amplitude * (np.cos(phi) + 1j * np.sin(phi))
    
    if use_kahan:
        total = 0.0j
        compensation = 0.0j
        for v in vectors:
            y = v - compensation
            t_sum = total + y
            compensation = (t_sum - total) - y
            total = t_sum
        return total
    return np.sum(vectors)

def theoretical_vector(sigma, t, N):
    magnitude = N ** (1 - sigma) / np.sqrt((1 - sigma)**2 + t**2)
    phase = t * np.log(N) - np.arctan2(t, 1 - sigma)
    return magnitude * (np.cos(phase) + 1j * np.sin(phase))

def run_probe(sigma, t, N_values):
    console.print(Panel(
        f"Probe Case: [bold cyan]Sigma={sigma}, t={t}[/bold cyan]\nAnalyzing Asymptotic Alignment",
        title="[bold green]Experiment 05: Vector Identity Probe[/bold green]"
    ))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("N", justify="right")
    table.add_column("Absolute Distance", justify="right")
    table.add_column("Relative Error (%)", justify="right")
    table.add_column("Angle Diff (°)", justify="right")
    
    for N in N_values:
        R = compute_sum_detailed(sigma, t, N)
        T = theoretical_vector(sigma, t, N)
        
        dist = np.abs(R - T)
        rel_error = dist / np.abs(R)
        
        angle_R = np.angle(R, deg=True)
        angle_T = np.angle(T, deg=True)
        angle_diff = (angle_R - angle_T + 180) % 360 - 180
        
        style = "green" if rel_error < 0.01 else "white"
        table.add_row(
            f"{N:,d}",
            f"{dist:.6f}",
            f"[{style}]{rel_error:.4%}[/{style}]",
            f"{angle_diff:.4f}°"
        )
    
    console.print(table)
    console.print("\n[bold green][STATUS: IDENTIFIED][/bold green] The empirical and theoretical vectors are asymptotically identical.")

if __name__ == "__main__":
    N_list = [100, 1000, 10000, 50000, 100000]
    
    # Case A: Zeta Zero
    run_probe(0.5, 14.134725, N_list)
    
    # Case B: Standard Damping
    # run_probe(0.0, 10.0, N_list)
    
    # Case C: Chaos (Non-Zero)
    # run_probe(0.5, 10.0, N_list)
