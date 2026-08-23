# SPDX-License-Identifier: GPL-3.0-only
# Copyright 2011 Michael Saavedra
# Modified 2026 for Python 3/Pillow compatibility.
# Derived from msaavedra/autocrop commit 87992d775133109ad57c01d31e417df539e04dd8.

from math import atan2, degrees

import numpy
from PIL import Image

from .sampler import PixelSampler


class SkewedImage:
    """Detecta el ángulo de una fotografía y la endereza."""

    def __init__(self, image, background, contrast=10, shrink=0):
        self.image = image
        self.width, self.height = image.size
        self.background = background
        self.contrast = contrast
        self.shrink = shrink
        sampler = PixelSampler(image, dpi=1, precision=1)
        self.sides = (Left(sampler), Top(sampler), Right(sampler), Bottom(sampler))

    def correct(self):
        margins, angles = list(zip(*[self._get_margin(side) for side in self.sides]))
        angle = degrees(numpy.median(angles))
        rotated_img = self.image.rotate(angle, Image.Resampling.BICUBIC)
        shrunk_margins = (
            tuple(value + self.shrink for value in margins[0:2])
            + tuple(value - self.shrink for value in margins[2:4])
        )
        return rotated_img.crop(shrunk_margins), shrunk_margins, angle

    def _get_margin(self, side):
        distances = []
        angles = []
        for start_x, start_y, _, _, _ in side.run_parallel():
            samples = side.run_perpendicular(start_x, start_y)
            x = start_x
            y = start_y
            for x, y, red, green, blue in samples:
                if self.background.matches((red, green, blue), self.contrast):
                    break
                if side.get_distance(x, y) > side.step:
                    samples = side.run_perpendicular(start_x, start_y)
                    break
            for x, y, red, green, blue in samples:
                if not self.background.matches((red, green, blue), self.contrast):
                    break
            if distances:
                angles.append(side.get_angle(distances[-1], x, y))
            distances.append(side.get_distance(x, y))
        return int(numpy.median(distances)), numpy.median(angles)


class Top:
    precision = 6
    count = precision - 2

    def __init__(self, sampler):
        self.sampler = sampler
        self.step = max(1, sampler.width // self.precision)
        self.parallel = sampler.right
        self.perpendicular = sampler.down
        self.x = self.step
        self.y = 0

    def run_parallel(self):
        return self.sampler.run(self.parallel, self.x, self.y, self.step, self.count)

    def run_perpendicular(self, x, y):
        return self.sampler.run(self.perpendicular, x, y, 1)

    def get_distance(self, x, y):
        return y

    def get_angle(self, prev_distance, x, y):
        return atan2(y - prev_distance, self.step)


class Right(Top):
    def __init__(self, sampler):
        self.sampler = sampler
        self.step = max(1, sampler.height // self.precision)
        self.parallel = sampler.down
        self.perpendicular = sampler.left
        self.x = sampler.width - 1
        self.y = self.step

    def get_distance(self, x, y):
        return x

    def get_angle(self, prev_distance, x, y):
        return atan2(prev_distance - x, self.step)


class Bottom(Top):
    def __init__(self, sampler):
        self.sampler = sampler
        self.step = max(1, sampler.width // self.precision)
        self.parallel = sampler.left
        self.perpendicular = sampler.up
        self.x = sampler.width - self.step
        self.y = sampler.height - 1

    def get_distance(self, x, y):
        return y

    def get_angle(self, prev_distance, x, y):
        return atan2(prev_distance - y, self.step)


class Left(Top):
    def __init__(self, sampler):
        self.sampler = sampler
        self.step = max(1, sampler.height // self.precision)
        self.parallel = sampler.up
        self.perpendicular = sampler.right
        self.x = 0
        self.y = sampler.height - self.step

    def get_distance(self, x, y):
        return x

    def get_angle(self, prev_distance, x, y):
        return atan2(x - prev_distance, self.step)
