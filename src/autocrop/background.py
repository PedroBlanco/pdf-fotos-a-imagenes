# SPDX-License-Identifier: GPL-3.0-only
# Copyright 2011 Michael Saavedra
# Derived from msaavedra/autocrop commit 87992d775133109ad57c01d31e417df539e04dd8.

import numpy as np

from .sampler import PixelSampler


class Background:
    """Modelo estadístico del fondo del escáner."""

    def __init__(self, medians=None, std_devs=None):
        self.medians = medians or {
            "red": 245.0,
            "green": 245.0,
            "blue": 245.0,
        }
        self.std_devs = std_devs or {
            "red": 1.5,
            "green": 1.5,
            "blue": 1.5,
        }

    def load_from_image(self, image, dpi):
        """Calcula el fondo a partir de un escaneo vacío."""
        sampler = PixelSampler(image, dpi, precision=4)
        reds, greens, blues = list(zip(*[sample[2:] for sample in sampler]))
        self.medians = {
            "red": np.median(reds),
            "green": np.median(greens),
            "blue": np.median(blues),
        }
        self.std_devs = {
            "red": np.std(reds),
            "green": np.std(greens),
            "blue": np.std(blues),
        }
        return self

    def matches(self, color, spread):
        """Indica si un color es compatible con el fondo."""
        red, green, blue = color
        values = {"red": red, "green": green, "blue": blue}
        for channel in ("red", "green", "blue"):
            delta = abs(self.medians[channel] - values[channel])
            if delta > self.std_devs[channel] * spread:
                return False
        return True
