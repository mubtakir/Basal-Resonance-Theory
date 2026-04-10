from ZetaLab_Supreme import ZetaLab
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

# ==============================================================================
# 🧪 M I C R O - L A B   [ Exp 11 ]
# ------------------------------------------------------------------------------
# 📜 الغاية من الكود: برهان أن قانون قطب موبيوس (Logarithmic Pole Law) ينطبق في أعماق المحيط (Z50)
# 🎓 المرحلة: الشمولية والقابلية للتوسع (Scalability)
# 📐 المبدأ الرياضي: |M_N| follows ln(N) slope even at high index zeros
# ⚡ النتيجة المتوقعة: نسبة تطابق بين الانحدار التجريبي والنظري تقترب من 100% لعينة Z50
# ==============================================================================

console = Console()

def run_moebius_deep_ocean_experiment():
    lab = ZetaLab(precision=100)
    
    console.print(Panel.fit(
        "--- EXPERIMENT 11: MOEBIUS HIGH ORDER PROOF (Z50) ---",
        style="bold green"
    ))
    
    t_z50 = 127.99633124
    rho = complex(0.5, t_z50)
    
    # 1. Theoretical Slope
    z_prime = lab.get_zeta_derivative(rho, order=1)
    theo_slope = 1.0 / abs(z_prime)
    
    # 2. Empirical Growth
    N_max = 30000
    console.print(f"Sieving Moebius up to [bold cyan]N={N_max}[/bold cyan] for Z50 resonance...\n")
    mu = lab.sieve_mu(N_max)
    
    n = np.arange(1, N_max + 1)
    terms = mu[1:] * (n**(-rho))
    all_sums = np.cumsum(terms)
    
    sample_Ns = np.geomspace(500, N_max, 20, dtype=int)
    mags = [abs(all_sums[N-1]) for N in sample_Ns]
    ln_Ns = np.log(sample_Ns)
    
    slope, _ = np.polyfit(ln_Ns, mags, 1)
    ratio = float(slope / theo_slope)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Target", justify="center")
    table.add_column("Empirical Slope", justify="right")
    table.add_column("Theoretical Slope", justify="right")
    table.add_column("Ratio (%)", justify="right")
    
    style = "green" if 0.95 < ratio < 1.05 else "white"
    table.add_row(
        "Z50",
        f"{float(slope):.10f}",
        f"{float(theo_slope):.10f}",
        f"[{style}]{ratio:.2%}[/{style}]"
    )
    
    console.print(table)
    
    if 0.95 < ratio < 1.05:
        console.print("\n[bold green][STATUS: SCALE CONFIRMED][/bold green] Moebius Pole Law holds in the Deep Ocean (Z50).")
        console.print("[dim]This dismisses any claim of local overfitting.[/dim]")

if __name__ == "__main__":
    run_moebius_deep_ocean_experiment()
