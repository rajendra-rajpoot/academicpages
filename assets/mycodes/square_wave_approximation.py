import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import os

plt.style.use("ggplot")

# Create temporary folder
os.makedirs("frames", exist_ok=True)

# Time-domain signal
t = np.linspace(0, 10, 1000)
signal = np.sin(2 * np.pi * 1 * t) + 0.5 * np.sin(2 * np.pi * 2 * t)

# Frequency-domain signal
freq = np.fft.fftfreq(len(t), d=t[1] - t[0])
spectrum = np.abs(np.fft.fft(signal))

# Normalize spectrum for comparison
spectrum = spectrum / np.max(spectrum) * np.max(signal) * 1.2

# Animation steps
steps = 40
frames = []

for i in range(steps):
    alpha = i / (steps - 1)

    fig = plt.figure(figsize=(14, 6))

    # --- Left subplot: 2D plots ---
    ax1 = fig.add_subplot(121)
    ax1.plot(t, signal, color='blue', lw=3, alpha=1 - alpha, label="Time Domain")
    ax1.plot(freq[:len(freq)//2], spectrum[:len(freq)//2],
             color='red', lw=2, alpha=alpha, label="Frequency Domain")
    ax1.set_title("2D Comparison", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Time / Frequency")
    ax1.set_ylabel("Amplitude / Magnitude")
    ax1.set_ylim(-2.5, 2.5)
    ax1.set_xlim(0, 12)
    ax1.legend(fontsize=15)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # --- Right subplot: 3D plot ---
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot(t, signal * 2, zs=-2, zdir='y',
             color='blue', alpha=1 - alpha, lw=2, label="Time Domain")
    ax2.bar(freq[:len(freq)//2], spectrum[:len(freq)//2],
            zs=2, zdir='y', color='red', alpha=alpha*0.8,
            edgecolor='black', linewidth=0.8, label="Frequency Domain")
    ax2.set_title("3D Transition", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Time / Frequency", fontsize=12)
    ax2.set_ylim(-2.5, 2.5)
    ax2.set_xlim(0, 12) 
    ax2.set_ylabel("Domain", fontsize=12)
    ax2.set_zlabel("Amplitude / Magnitude", fontsize=12)
    ax2.view_init(elev=25, azim=30 + i)
    ax2.legend(loc="upper left", fontsize=15)

    plt.tight_layout()
    filename = f"frames/frame_{i:03d}.png"
    plt.savefig(filename, dpi=150)
    plt.close()

    frames.append(Image.open(filename))

# Save GIF
frames[0].save("fourier_transform_2D_3D.gif",
               save_all=True, append_images=frames[1:],
               duration=120, loop=0)

# Cleanup
for file in os.listdir("frames"):
    os.remove(os.path.join("frames", file))
os.rmdir("frames")

print("GIF saved as fourier_transform_2D_3D.gif")

##############################################



import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# Create temporary folder
os.makedirs("frames", exist_ok=True)

# Square wave definition
def square_wave(t):
    return np.sign(np.sin(t))

# Fourier series approximation of square wave
def fourier_series(t, N):
    result = np.zeros_like(t)
    for k in range(1, N+1, 2):  # odd harmonics only
        result += (4/np.pi) * (1/k) * np.sin(k*t)
    return result

# Sigma approximation (Cesàro sum)
def sigma_approx(t, N):
    result = np.zeros_like(t)
    for k in range(1, N+1, 2):
        weight = 1 - k/(N+1)  # Fejér kernel weighting
        result += weight * (4/np.pi) * (1/k) * np.sin(k*t)
    return result

# Time axis
t = np.linspace(0, 2*np.pi, 2000)
signal = square_wave(t)

frames = []
steps = 40  # number of frames

for i in range(1, steps+1):
    fig, ax = plt.subplots(figsize=(12,8))

    # Original square wave
    ax.plot(t, signal, 'r', linewidth=2, label="Square wave")

    # Fourier series approximation
    fs = fourier_series(t, i*2-1)
    ax.plot(t, fs, 'b', linewidth=2, label=f"Fourier series (N={i*2-1})")

    # Sigma approximation
    sa = sigma_approx(t, i*2-1)
    ax.plot(t, sa, 'g', linewidth=2, label=f"Sigma approximation (N={i*2-1})")
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_xlim(0, 2*np.pi)

    ax.set_ylim(-1.5, 1.5)
    ax.set_title("Square Wave Approximation: Fourier vs Sigma")
    ax.legend(loc="upper right", fontsize=15)

    filename = f"frames/frame_{i:03d}.png"
    plt.savefig(filename)
    plt.close()

    frames.append(Image.open(filename))

# Save GIF
frames[0].save("square_wave_approximation.gif",
               save_all=True,
               append_images=frames[1:],
               duration=200,
               loop=0)

# Cleanup
for file in os.listdir("frames"):
    os.remove(os.path.join("frames", file))
os.rmdir("frames")

print("GIF saved as square_wave_approximation.gif")
