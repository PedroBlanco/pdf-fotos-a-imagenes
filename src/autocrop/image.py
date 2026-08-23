# SPDX-License-Identifier: GPL-3.0-only
# Copyright 2011 Michael Saavedra
# Modified 2026 to avoid debug overlays on the source scan.
# Derived from msaavedra/autocrop commit 87992d775133109ad57c01d31e417df539e04dd8.

from .sampler import PixelSampler
from .skew import SkewedImage


class MultiPartImage:
    """Detecta varias fotografías independientes dentro de un escaneo."""

    def __init__(
        self,
        image,
        background,
        dpi,
        precision=50,
        deskew=True,
        contrast=15,
        shrink=3,
    ):
        self.contrast = contrast
        self.image = image
        self.dpi = dpi
        self.width, self.height = image.size
        self.precision = precision
        self.deskew = deskew
        self.shrink = shrink
        self.samples = PixelSampler(image, dpi, precision)
        self.background = background
        self.sections = self._find_sections()

    def __iter__(self):
        for section in self.sections:
            image = self.image.crop((section.left, section.top, section.right, section.bottom))
            if self.deskew:
                skew = SkewedImage(image, self.background, self.contrast, self.shrink)
                image, _, _ = skew.correct()
            yield image

    def __len__(self):
        return len(self.sections)

    def _find_sections(self):
        sections = []
        for pixel in self.samples:
            color_data = pixel[2:]
            location_data = pixel[:2]
            if self.background.matches(color_data, self.contrast):
                continue
            if any(location_data in section for section in sections):
                continue

            seeds = [location_data]
            pixels = set(seeds)
            for seed in iter(seeds):
                for x, y, red, green, blue in self.samples.around(*seed):
                    location = (x, y)
                    color = (red, green, blue)
                    if location not in pixels:
                        pixels.add(location)
                        if not self.background.matches(color, self.contrast):
                            seeds.append(location)

            new_section = ImageSection(pixels)
            if any(section.merge_if_overlapping(new_section) for section in sections):
                continue
            sections.append(new_section)

        minimum_area = self.dpi**2
        return [section for section in sections if section > minimum_area]


class ImageSection:
    """Área rectangular que contiene una fotografía detectada."""

    def __init__(self, pixels):
        seq_x, seq_y = list(zip(*pixels))
        self.left = min(seq_x)
        self.right = max(seq_x)
        self.top = min(seq_y)
        self.bottom = max(seq_y)
        self.height = self.bottom - self.top
        self.width = self.right - self.left
        self.area = self.height * self.width

    def contains(self, x, y):
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def __contains__(self, pixel):
        return self.contains(*pixel)

    def overlap(self, other):
        if self.top > other.bottom or self.bottom < other.top:
            return 0.0
        if self.right < other.left or self.left > other.right:
            return 0.0
        overlap_width = min(self.right, other.right) - max(self.left, other.left)
        overlap_height = min(self.bottom, other.bottom) - max(self.top, other.top)
        overlap_area = overlap_width * overlap_height
        smaller = min(self.area, other.area)
        return float(overlap_area) / smaller if smaller else 0.0

    def merge(self, other):
        self.top = min(self.top, other.top)
        self.bottom = max(self.bottom, other.bottom)
        self.left = min(self.left, other.left)
        self.right = max(self.right, other.right)
        self.height = self.bottom - self.top
        self.width = self.right - self.left
        self.area = self.height * self.width

    def merge_if_overlapping(self, other, margin=0.15):
        if self.overlap(other) >= margin:
            self.merge(other)
            return True
        return False

    def __gt__(self, minimum_area):
        return self.area > minimum_area
