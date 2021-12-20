#!/bin/env python3

from sys import exit, argv


def load_algorithm_and_image(path):
    with open(path, "r") as f:
        algorithm = load_algorithm(f)
        image = load_image(f)
    return algorithm, image


def load_algorithm(f):
    code = ""
    for line in f:
        line = line.strip()
        if line == "":
            break
        code += line
    algorithm = {}
    for i, out in enumerate(code):
        pattern = f"{i:09b}".translate({ord("0"): ".", ord("1"): "#"})
        matcher = (pattern[0:3], pattern[3:6], pattern[6:9])
        algorithm[matcher] = out
    return algorithm


def load_image(f):
    return [line.strip() for line in f]


def enhance(image, algorithm):
    image = enhance_step(image, algorithm, ".")
    infinite = algorithm[("...", "...", "...")]
    image = enhance_step(image, algorithm, infinite)
    return image


def enhance_step(image, algorithm, infinite):
    image = ensure_image_border(image, algorithm, infinite)
    image = apply_algorithm_to_image(image, algorithm)
    image = strip_unused_border(image)
    return image


def ensure_image_border(image, algorithm, infinite):
    width = len(image[0])
    ver_padding = infinite * (width + 6)
    hor_padding = infinite * 3
    return (
        [ver_padding] * 3
        + [hor_padding + line + hor_padding for line in image]
        + [ver_padding] * 3
    )


def strip_unused_border(image):
    return [line[1:-1] for line in image[1:-1]]


def apply_algorithm_to_image(image, algorithm):
    width = len(image[0])
    height = len(image)
    new_image = []
    for y in range(1, height - 1):
        new_image.append(
            "".join(
                apply_algorithm_to_pixel(image, x, y, algorithm)
                for x in range(1, width - 1)
            )
        )
    return new_image


def apply_algorithm_to_pixel(image, x, y, algorithm):
    lookup = (
        image[y - 1][x - 1 : x + 2],
        image[y][x - 1 : x + 2],
        image[y + 1][x - 1 : x + 2],
    )
    new_pixel = algorithm[lookup]
    return new_pixel


def count_lit_pixels(image):
    return sum(sum(c == "#" for c in line) for line in image)


if len(argv) != 2:
    print(f"Usage: {argv[0]} <filename>")
    exit(1)

algorithm, image = load_algorithm_and_image(argv[1])
image = enhance(image, algorithm)
print(count_lit_pixels(image))
