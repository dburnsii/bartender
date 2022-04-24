
def rgb_multiply(color, intensity=1):
    return tuple(map(lambda x: x * max(intensity, 0), color))


def simulate_pixels(pixels):
    print("\r", end="")
    led_template = "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m"
    for pixel in pixels:
        print(led_template.format(int(pixel[0]),
                                  int(pixel[1]),
                                  int(pixel[2]),
                                  "O"),
              end='', sep='', flush=True)


def color_to_tuple(color):
    b = color % 256
    color >>= 8
    g = color % 256
    color >>= 8
    r = color
    return (r, g, b)


def mix(color_a, color_b):
    # TODO: Add logic to this to do a better job of matching intensity
    return ((min(color_a[0] + color_b[0], 255),
             min(color_a[1] + color_b[1], 255),
             min(color_a[2] + color_b[2], 255)))
