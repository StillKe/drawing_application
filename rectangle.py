# rectangle.py

class Rectangle:
    def __init__(self, width, height, x, y, color="blue"):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def to_dictionary(self):
        return {
            "type": "Rectangle",
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "color": self.color
        }

    @staticmethod
    def from_dictionary(data):
        return Rectangle(data["width"], data["height"], data["x"], data["y"], data["color"])
