# Import necessary modules
import tkinter as tk
from tkinter import colorchooser, filedialog

# Define the DrawingApplication class
class DrawingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Application")

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill="both")

        # Add buttons for drawing shapes
        self.rect_button = tk.Button(self.root, text="Rectangle", command=self.draw_rectangle)
        self.rect_button.pack(side="left", padx=10)

        self.square_button = tk.Button(self.root, text="Square", command=self.draw_square)
        self.square_button.pack(side="left", padx=10)

        self.circle_button = tk.Button(self.root, text="Circle", command=self.draw_circle)
        self.circle_button.pack(side="left", padx=10)

        self.ellipse_button = tk.Button(self.root, text="Ellipse", command=self.draw_ellipse)
        self.ellipse_button.pack(side="left", padx=10)

        self.triangle_button = tk.Button(self.root, text="Triangle", command=self.draw_triangle)
        self.triangle_button.pack(side="left", padx=10)

        # Set initial shape to draw
        self.current_shape = "rectangle"

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw_shape(self, event):
        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x, event.y
        if self.current_shape == "rectangle":
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")
        elif self.current_shape == "square":
            size = min(abs(x1 - x0), abs(y1 - y0))
            if x1 < x0:
                x0 -= size
            if y1 < y0:
                y0 -= size
            self.canvas.create_rectangle(x0, y0, x0 + size, y0 + size, outline="black")
        elif self.current_shape == "circle":
            self.canvas.create_oval(x0, y0, x1, y1, outline="black")
        elif self.current_shape == "ellipse":
            self.canvas.create_oval(x0, y0, x1, y1, outline="black")
        elif self.current_shape == "triangle":
            self.canvas.create_polygon(x0, y0, x1, y1, x0 - (x1 - x0), y1, outline="black")

    def finish_draw(self, event):
        pass

    # Methods for drawing different shapes
    def draw_rectangle(self):
        self.current_shape = "rectangle"

    def draw_square(self):
        self.current_shape = "square"

    def draw_circle(self):
        self.current_shape = "circle"

    def draw_ellipse(self):
        self.current_shape = "ellipse"

    def draw_triangle(self):
        self.current_shape = "triangle"

# Main function to create and run the application
def main():
    root = tk.Tk()
    app = DrawingApplication(root)
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
