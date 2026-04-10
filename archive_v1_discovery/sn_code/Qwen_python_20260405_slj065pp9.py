from mpl_toolkits.mplot3d import Axes3D

# شبكة من القيم
sigma_vals = np.linspace(0.3, 0.7, 50)
t_vals = np.linspace(10, 30, 100)
Sigma, T = np.meshgrid(sigma_vals, t_vals)

# حساب الخطأ لكل نقطة
Errors = np.zeros_like(Sigma)
for i in range(len(sigma_vals)):
    for j in range(len(t_vals)):
        Errors[j, i] = error_function(Sigma[j, i], T[j, i], N=10000)

# رسم ثلاثي الأبعاد
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(Sigma, T, np.log10(Errors), 
                       cmap='viridis', edgecolor='none')
ax.set_xlabel('σ')
ax.set_ylabel('t')
ax.set_zlabel('log₁₀(E_N)')
ax.set_title('سطح الخطأ في المستوى (σ, t)')
plt.colorbar(surf, label='log₁₀(الخطأ)')
plt.show()