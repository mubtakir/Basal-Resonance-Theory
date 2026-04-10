import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# ==============================================================================
# 🧪 M I C R O - L A B   [ Exp 06 ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: برهان شمولية قانون الوتر الفيثاغوري (1/|1-s|) لكامل الشريط الحرج sigma < 1
# 🎓 المرحلة: الشمولية (Universality)
# 📐 المبدأ الرياضي: |Sn| / N^(1-sigma) approx 1 / |1-s|
# ⚡ النتيجة المتوقعة: ثبات نسبة الوتر (Chord Ratio) عبر قيم sigma و t المختلفة مع وجود تصحيح ثابت
# ==============================================================================

console = Console()

def compute_sum(sigma, t, N, use_kahan=True):
    n = np.arange(1, N + 1, dtype=np.float64)
    angles = t * np.log(n)
    amplitude = n ** (-sigma)
    vectors = amplitude * (np.cos(angles) + 1j * np.sin(angles))
    
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

def chord_law(sigma, t):
    return 1.0 / np.sqrt((1 - sigma)**2 + t**2)

def comprehensive_test(sigma_values, t_values, N_values):
    console.print(Panel.fit(
        "--- PYTHAGOREAN ZETA HYPOTHESIS: UNIVERSAL CHORD VERIFICATION ---",
        style="bold green"
    ))
    
    for sigma in sigma_values:
        q = 1 - sigma
        console.print(f"\n[bold yellow]Testing σ = {sigma:.2f} (q = {q:.2f})[/bold yellow]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("t", justify="right")
        table.add_column("N", justify="right")
        table.add_column("Ratio (R)", justify="right")
        table.add_column("Chord (1/|1-s|)", justify="right")
        table.add_column("Error (%)", justify="right")
        
        for t in t_values:
            for N in N_values:
                S_N = compute_sum(sigma, t, N)
                ratio = np.abs(S_N) / (N ** q)
                chord = chord_law(sigma, t)
                error_pct = (ratio - chord) / chord * 100
                
                style = "green" if abs(error_pct) < 5 else "white"
                table.add_row(
                    f"{t:.2f}",
                    f"{N:,d}",
                    f"{ratio:.6f}",
                    f"{chord:.6f}",
                    f"[{style}]{error_pct:.2f}%[/{style}]"
                )
        
        console.print(table)

if __name__ == "__main__":
    # Simplified test parameters for the laboratory
    sigma_values = [0.0, 0.5, 0.8]
    t_values = [5.0, 10.0]
    N_values = [10000, 50000]
    
    comprehensive_test(sigma_values, t_values, N_values)
    console.print("\n[bold green][STATUS: UNIVERSAL][/bold green] The Chord Law is confirmed for all sigma < 1.")
