"""
ARCHITECTURE FREQUENCY DETECTION
0.67Hz modulation analysis.
"""

import numpy as np
from scipy import signal, stats

class ArchitectureFrequencyDetector:
    def __init__(self):
        self.target_frequency = 0.67  # Hz
        self.tolerance = 0.01  # ±10ms
        
    def detect_frequency(self, time_series: np.ndarray, 
                        sampling_rate: float) -> Dict:
        """Detect 0.67Hz architecture frequency in data."""
        # Perform spectral analysis
        frequencies, power = signal.periodogram(time_series, 
                                               fs=sampling_rate)
        
        # Find peak near target frequency
        target_idx = np.argmin(np.abs(frequencies - self.target_frequency))
        peak_power = power[target_idx]
        
        # Calculate signal-to-noise ratio
        noise_floor = np.median(power)
        snr = peak_power / noise_floor if noise_floor > 0 else 0
        
        # Statistical significance
        p_value = self.calculate_significance(power, target_idx)
        
        return {
            'frequency_detected': frequencies[target_idx],
            'power': peak_power,
            'snr': snr,
            'p_value': p_value,
            'significant': p_value < 0.05 and snr > 2.0
        }
    
    def calculate_significance(self, power_spectrum: np.ndarray, 
                             target_idx: int) -> float:
        """Calculate statistical significance of frequency detection."""
        # Remove target frequency for background estimation
        background = np.delete(power_spectrum, target_idx)
        
        # One-sample t-test against background
        t_stat, p_value = stats.ttest_1samp(background, 
                                           power_spectrum[target_idx])
        return p_value
