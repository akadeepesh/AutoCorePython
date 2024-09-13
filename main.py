import random
import matplotlib.pyplot as plt
from typing import List, Tuple

class Rectangle:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.rotated = False

    def rotate(self):
        self.width, self.height = self.height, self.width
        self.rotated = not self.rotated

    def area(self):
        return self.width * self.height

def generate_rectangles(num: int) -> List[Rectangle]:
    return [Rectangle(random.randint(1, 20), random.randint(1, 20)) for _ in range(num)]

def can_place_rectangle(space: Tuple[int, int, int, int], rect: Rectangle) -> bool:
    return space[2] - space[0] >= rect.width + 2 and space[3] - space[1] >= rect.height + 2

def place_rectangles(space: Tuple[int, int, int, int], rectangles: List[Rectangle]) -> bool:
    if not rectangles:
        return True

    x, y, width, height = space
    rect = rectangles[0]

    for rotation in [False, True]:
        if rotation:
            rect.rotate()

        if can_place_rectangle(space, rect):
            rect.x = x + 1
            rect.y = y + 1

            # Try to place the rectangle in the current position
            remaining_space = [
                (x, y + rect.height + 2, width, height - rect.height - 2),  # Top
                (x + rect.width + 2, y, width - rect.width - 2, height)  # Right
            ]

            for subspace in remaining_space:
                if place_rectangles(subspace, rectangles[1:]):
                    return True

            # If placement fails, reset the rectangle's position
            rect.x = 0
            rect.y = 0

        if rotation:
            rect.rotate()  # Rotate back if we rotated earlier

    return False

def optimize_placement(rectangles: List[Rectangle], space_size: int) -> Tuple[bool, int, int]:
    min_width = space_size
    min_height = space_size
    success = False

    for _ in range(100):  # Try different random arrangements
        random.shuffle(rectangles)
        if place_rectangles((0, 0, space_size, space_size), rectangles):
            success = True
            max_x = max(rect.x + rect.width for rect in rectangles)
            max_y = max(rect.y + rect.height for rect in rectangles)
            if max_x <= min_width and max_y <= min_height:
                min_width = max_x
                min_height = max_y

    return success, min_width, min_height

def plot_results(rectangles: List[Rectangle], width: int, height: int):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)

    for rect in rectangles:
        color = (random.random(), random.random(), random.random())
        rectangle = plt.Rectangle((rect.x, rect.y), rect.width, rect.height, 
                                  fill=False, edgecolor=color)
        ax.add_patch(rectangle)
        ax.text(rect.x + rect.width/2, rect.y + rect.height/2, 
                f"{rect.width}x{rect.height}\nRotated: {rect.rotated}",
                ha='center', va='center')

    ax.set_aspect('equal', adjustable='box')
    plt.title(f"Optimized Rectangle Placement ({width}x{height})")
    plt.show()

def main():
    space_size = 100
    rectangles = generate_rectangles(5)
    success, min_width, min_height = optimize_placement(rectangles, space_size)

    if success:
        print(f"Placement successful. Minimal area: {min_width}x{min_height}")
        plot_results(rectangles, min_width, min_height)
    else:
        print("Error: Unable to place all rectangles within the given space.")

if __name__ == "__main__":
    main()