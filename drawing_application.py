# drawing_application.py

import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
import json
from rectangle import Rectangle
from square import Square

class DrawingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Application")

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill="both")

        self.shapes = []
        self.selected_shape = None
        self.selected_color = "blue"
        self.start_x = None
        self.start_y = None

        self.create_buttons()

    def create_buttons(self):
        self.rect_button = tk.Button(self.root, text="Rectangle", command=self.create_rectangle)
        self.rect_button.pack(side="left", padx=10)

        self.square_button = tk.Button(self.root, text="Square", command=self.create_square)
        self.square_button.pack(side="left", padx=10)

        self.color_button = tk.Button(self.root, text="Color", command=self.pick_color)
        self.color_button.pack(side="left", padx=10)

        self.save_button = tk.Button(self.root, text="Save", command=self.save_drawing)
        self.save_button.pack(side="right", padx=10)

        self.load_button = tk.Button(self.root, text="Load", command=self.load_drawing)
        self.load_button.pack(side="right", padx=10)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)
        self.canvas.bind("<Button-3>", self.select_shape)

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw_shape(self, event):
        if self.selected_shape:
            self.canvas.delete("current_shape")
        x0, y0 = self.start_x, self.start_y
        x1, y1 = event.x, event.y
        if self.selected_shape == "rectangle":
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.selected_color, tags="current_shape")
        elif self.selected_shape == "square":
            size = min(abs(x1 - x0), abs(y1 - y0))
            if x1 < x0:
                x0 -= size
            if y1 < y0:
                y0 -= size
            self.canvas.create_rectangle(x0, y0, x0 + size, y0 + size, fill=self.selected_color, tags="current_shape")

    def finish_draw(self, event):
        shape = self.canvas.find_withtag("current_shape")
        if shape:
            self.shapes.extend(shape)

    def create_rectangle(self):
        self.selected_shape = "rectangle"
        self.selected_color = "blue"

    def create_square(self):
        self.selected_shape = "square"
        self.selected_color = "blue"

    def select_shape(self, event):
        shape = self.canvas.find_closest(event.x, event.y)
        if shape:
            self.selected_shape = shape[0]
            self.selected_color = self.canvas.itemcget(self.selected_shape, "fill")
            self.canvas.itemconfig(self.selected_shape, outline="black", width=2)

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.selected_color = color

    def save_drawing(self):
    data = []
    for shape in self.shapes:
        if self.canvas.coords(shape):  # Check if shape exists
            x0, y0, x1, y1 = self.canvas.coords(shape)
            color = self.canvas.itemcget(shape, "fill")
            if x1 - x0 == y1 - y0:  # Square
                data.append(Square(x1 - x0, x0, y0, color).to_dictionary())
            else:  # Rectangle
                data.append(Rectangle(x1 - x0, y1 - y0, x0, y0, color).to_dictionary())

    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filename:
        with open(filename, "w") as file:
            json.dump(data, file)
        messagebox.showinfo("Save Successful", "Drawing saved successfully.")


    def load_drawing(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r") as file:
                data = json.load(file)
            for shape_data in data:
                if shape_data["type"] == "Rectangle":
                    shape = Rectangle.from_dictionary(shape_data)
                elif shape_data["type"] == "Square":
                    shape = Square.from_dictionary(shape_data)
                self.shapes.append(self.canvas.create_rectangle(shape.x, shape.y, shape.x + shape.width, shape.y + shape.height, fill=shape.color))
            messagebox.showinfo("Load Successful", "Drawing loaded successfully.")

def main():
    root = tk.Tk()
    app = DrawingApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
