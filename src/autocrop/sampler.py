# SPDX-License-Identifier: GPL-3.0-only
# Copyright 2011 Michael Saavedra
# Derived from msaavedra/autocrop commit 87992d775133109ad57c01d31e417df539e04dd8.


class ReachedEdge(StopIteration):
    pass


class PixelSampler:
    """Muestrea píxeles regularmente y permite recorrer vecinos."""

    def __init__(self, image, dpi, precision=50):
        self.image = image
        self.width, self.height = image.size
        self.data = image.load()
        self.dpi = dpi
        if precision > dpi:
            self.precision = dpi
        elif precision == 0:
            self.precision = 1
        else:
            self.precision = precision
        self.step = max(1, int(self.dpi / self.precision))

    def __iter__(self):
        for x, y, _, _, _ in self.run(self.down, self.step, self.step):
            for result in self.run(self.right, x, y, self.step):
                yield result

    def update_image(self, image):
        self.image = image
        self.data = image.load()

    def run(self, direction, x, y, distance=0, maximum=0):
        if distance == 0:
            distance = self.step
        distance = max(1, int(distance))
        x = int(x)
        y = int(y)
        count = 0
        red, green, blue = self.data[x, y][:3]
        yield (x, y, red, green, blue)
        while True:
            try:
                result = direction(x, y, distance)
            except ReachedEdge:
                return
            yield result
            if maximum:
                count += 1
                if count == maximum:
                    break
            x, y = result[:2]

    def up(self, x, y, distance=0):
        distance = max(1, int(distance or self.step))
        x = int(x)
        y = int(y)
        if y == distance:
            raise ReachedEdge(x, y)
        y -= distance
        if y < distance:
            y = distance
        red, green, blue = self.data[x, y][:3]
        return (x, y, red, green, blue)

    def down(self, x, y, distance=0):
        distance = max(1, int(distance or self.step))
        x = int(x)
        y = int(y)
        max_y = self.height - distance - 1
        if y == max_y:
            raise ReachedEdge(x, y)
        y += distance
        if y > max_y:
            y = max_y
        red, green, blue = self.data[x, y][:3]
        return (x, y, red, green, blue)

    def left(self, x, y, distance=0):
        distance = max(1, int(distance or self.step))
        x = int(x)
        y = int(y)
        if x == distance:
            raise ReachedEdge(x, y)
        x -= distance
        if x < distance:
            x = distance
        red, green, blue = self.data[x, y][:3]
        return (x, y, red, green, blue)

    def right(self, x, y, distance=0):
        distance = max(1, int(distance or self.step))
        x = int(x)
        y = int(y)
        max_x = self.width - distance - 1
        if x == max_x:
            raise ReachedEdge(x, y)
        x += distance
        if x > max_x:
            x = max_x
        red, green, blue = self.data[x, y][:3]
        return (x, y, red, green, blue)

    def around(self, x, y, distance=0):
        for function in (self.up, self.right, self.down, self.left):
            try:
                yield function(x, y, distance)
            except ReachedEdge:
                continue
