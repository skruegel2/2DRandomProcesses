import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
u = np.arange(-np.pi, np.pi, 0.1)
v = np.arange(-np.pi, np.pi, 0.1)
u,v = np.meshgrid(u, v)
#Z = np.absolute(0.01/(((1-0.9*(np.cos(u)-1j*np.sin(u)))*(1-0.9*(np.cos(v)-1j*np.sin(v))))))
#Z = np.exp(u*1j)
Z = np.log((1.0/12.)*((3/((1-0.99*np.exp(u*-1j)-0.99*np.exp(v*-1j)+0.9801*np.exp((u+v)*-1j))))**2))
# Plot the surface.
surf = ax.plot_surface(u, v, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
