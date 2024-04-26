# square.py

from rectangle import Rectangle

class Square(Rectangle):
    def __init__(self, size, x, y, color="blue"):
        super().__init__(size, size, x, y, color)

    def to_dictionary(self):
        data = super().to_dictionary()
        data["type"] = "Square"
        return data

    @staticmethod
    def from_dictionary(data):
        return Square(data["width"], data["x"], data["y"], data["color"])
