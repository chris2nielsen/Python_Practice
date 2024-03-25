import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# Parameters for the sine waves
A1, f1, phi1 = 1, 5, 0     # Amplitude, frequency, and phase for the first sine wave
A2, f2, phi2 = 0.5, 10, np.pi/4  # Second sine wave
A3, f3, phi3 = 0.75, 15, np.pi/2  # Third sine wave

# Time array
t = np.linspace(0, 1, 1000, endpoint=True)  # 1 second duration, 1000 points

# Combined sine wave
y = A1*np.sin(2*np.pi*f1*t + phi1) + A2*np.sin(2*np.pi*f2*t + phi2) + A3*np.sin(2*np.pi*f3*t + phi3)

# Plotting the combined sine wave
plt.figure(figsize=(10, 4))
plt.plot(t, y)
plt.title('Combined Sine Wave')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

# Fourier Transform of the combined signal
Y = fft(y)
frequencies = np.linspace(0, len(t) / 2, int(len(t)/2), endpoint=True)  # Frequency axis

# Plotting the magnitude of the Fourier Transform
plt.figure(figsize=(10, 4))
plt.plot(frequencies, 2/len(t) * np.abs(Y[:len(t)//2]))
plt.title('Fourier Transform of the Combined Sine Wave')
plt.xlim([0, 50])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.grid(True)
plt.show()

# Adding random noise to the combined sine wave
np.random.seed(0)  # For reproducibility
noise = np.random.normal(0, 0.5, t.shape)  # Mean = 0, Std dev = 0.5
y_noisy = y + noise

# Fourier Transform of the noisy signal
Y_noisy = fft(y_noisy)

# Plotting the noisy combined sine wave
plt.figure(figsize=(10, 4))
plt.plot(t, y_noisy)
plt.title('Combined Sine Wave with Noise')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

# Plotting the magnitude of the Fourier Transform of the noisy signal
plt.figure(figsize=(10, 4))
plt.plot(frequencies, 2/len(t) * np.abs(Y_noisy[:len(t)//2]))
plt.title('Fourier Transform of the Noisy Combined Sine Wave')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.xlim([0, 50])  # Keeping the x-axis limited to 0-50 Hz for a focused view
plt.grid(True)
plt.show()

import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt

# Assuming 't', 'y', 'y_noisy', 'Y_noisy', and 'frequencies' are already defined as per your provided code

# Set the threshold magnitude (this is where you decide what 'low' means)
magnitude_threshold = 0.1

# Filter out frequencies below the threshold
Y_filtered = np.where(2/len(t) * np.abs(Y_noisy) < magnitude_threshold, 0, Y_noisy)

# Inverse Fourier Transform to convert back to time domain
y_filtered = ifft(Y_filtered)

# Plotting the filtered signal
plt.figure(figsize=(10, 4))
plt.plot(t, y_filtered.real)  # Use the real part of the returned complex numbers
plt.title('Filtered Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

# Plotting the magnitude of the Fourier Transform of the noisy signal
plt.figure(figsize=(10, 4))
plt.plot(frequencies, 2/len(t) * np.abs(Y_filtered[:len(t)//2]))
plt.title('Fourier Transform of the Noisy Combined Sine Wave')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.xlim([0, 50])  # Keeping the x-axis limited to 0-50 Hz for a focused view
plt.grid(True)
plt.show()
