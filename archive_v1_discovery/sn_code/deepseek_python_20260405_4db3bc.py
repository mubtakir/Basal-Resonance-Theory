# اختبار تأثير t لنفس σ
sigma_fixed = 0.3
t_values_test = [1, 2, 5, 10, 14.1347, 20, 30, 50, 100]
N_large = 50000

print("\n" + "="*80)
print(f"اختبار التعميم مع σ = {sigma_fixed} ثابت، N = {N_large}")
print("="*80)
print(f"{'t':>12} | {'C_computed':>12} | {'1/√((1-σ)²+t²)':>20} | {'الفرق':>12}")
print("-"*80)

t_results = []
for t_val in t_values_test:
    C_val = C_generalized(sigma_fixed, t_val, N_large)
    theory = 1 / np.sqrt((1 - sigma_fixed)**2 + t_val**2)
    diff = abs(C_val - theory)
    t_results.append((t_val, C_val, theory, diff))
    print(f"{t_val:12.4f} | {C_val:12.8f} | {theory:20.8f} | {diff:12.8f}")

# رسم بياني
fig, ax = plt.subplots(figsize=(10, 6))

t_vals = [r[0] for r in t_results]
C_vals = [r[1] for r in t_results]
theory_vals = [r[2] for r in t_results]

ax.loglog(t_vals, C_vals, 'bo-', linewidth=2, markersize=8, label='محسوب')
ax.loglog(t_vals, theory_vals, 'r--', linewidth=2, label='نظري: 1/√((1-σ)²+t²)')
ax.set_xlabel('t (مقياس لوغاريتمي)')
ax.set_ylabel('C(σ, t)')
ax.set_title(f'اعتماد C(σ={sigma_fixed}, t) على t')
ax.legend()
ax.grid(True, alpha=0.3)

plt.show()