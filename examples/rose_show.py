
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

# -------------------------
# 1) 对应 R: x <- seq(0,24)/24
# -------------------------
x = np.arange(0, 25) / 24.0  # 25 points

# -------------------------
# 2) 对应 R: t <- seq(0,575,by=0.5)/575*20*pi + 4*pi
# -------------------------
t = (np.arange(0, 575.0 + 0.5, 0.5) / 575.0) * 20.0 * np.pi + 4.0 * np.pi  # 1151 points

# -------------------------
# 3) 对应 R: expand.grid + matrix(..., ncol=25, byrow=TRUE)
#    每一行是同一个 t，每一列是 x
# -------------------------
X = np.tile(x, (t.size, 1))                 # shape (1151, 25)
T = np.tile(t.reshape(-1, 1), (1, x.size))  # shape (1151, 25)

# -------------------------
# 4) 对应 R 的全部公式
# -------------------------
p = (np.pi / 2.0) * np.exp(-T / (8.0 * np.pi))
change = np.sin(15.0 * T) / 150.0

# R: u <- 1 - (1 - (3.6*t) %% (2*pi) / pi)^4 / 2 + change
u = 1.0 - (1.0 - (np.mod(3.6 * T, 2.0 * np.pi) / np.pi))**4 / 2.0 + change

# R: y <- 2 * (x^2 - x)^2 * sin(p)
y = 2.0 * (X**2 - X)**2 * np.sin(p)

# R: r <- u * (x*sin(p) + y*cos(p))
r = u * (X * np.sin(p) + y * np.cos(p))

# R: persp3D(x=r*cos(t), y=r*sin(t), z=u*(x*cos(p)-y*sin(p)))
X3 = r * np.cos(T)
Y3 = r * np.sin(T)
Z3 = u * (X * np.cos(p) - y * np.sin(p))

# -------------------------
# 5) 颜色：对应 R 的 colorRampPalette(c("#e4e9f6","#e54b4b"))(100)
# -------------------------
cmap = LinearSegmentedColormap.from_list("r_palette", ["#e4e9f6", "#e54b4b"], N=100)

# 用 Z 做渐变（也最像 R 的效果）
Zn = (Z3 - Z3.min()) / (Z3.max() - Z3.min() + 1e-12)
facecolors = cmap(Zn)
facecolors[..., 3] = 0.55  # 半透明：接近你截图那种“雾感”

# -------------------------
# 6) 画图（3D）
# -------------------------
fig = plt.figure(figsize=(7, 7), dpi=240)
ax = fig.add_subplot(111, projection="3d")
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.plot_surface(
    X3, Y3, Z3,
    facecolors=facecolors,
    rstride=1, cstride=1,
    linewidth=0.1, edgecolor=(0.85, 0.85, 0.85, 0.6),  # border="grey85", lwd=0.1
    antialiased=True,
    shade=False
)

# 对应 R: theta=-60, phi=45
ax.view_init(elev=45, azim=-60)

# 标题/坐标轴（对应 R: main/xlab/ylab/zlab）
ax.set_title("To my love", pad=18, fontweight="bold")
ax.set_xlabel("You", labelpad=8)
ax.set_ylabel("Love", labelpad=8)
ax.set_zlabel("")

ax.grid(True)

# 保存到桌面（避免只读目录）
save_path = "media/rose.png"
plt.savefig(save_path, bbox_inches="tight", pad_inches=0.2, facecolor="white")
plt.show()

print("Saved to:", save_path)