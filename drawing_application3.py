import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import json

class DrawingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagram Drawing Tool")

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill="both")

        self.shapes = []
        self.selected_shape = None
        self.selected_color = "black"
        self.current_tool = "rectangle"
        self.current_layer = 0
        self.layers = {0: []}
        self.undo_stack = []
        self.redo_stack = []

        self.init_buttons()
        self.init_bindings()

    def init_buttons(self):
        self.init_shape_buttons()
        self.init_editing_buttons()
        self.init_color_button()
        self.init_layer_buttons()

    def init_shape_buttons(self):
        shapes = ["Rectangle", "Circle", "Arrow", "Text"]
        for shape in shapes:
            button = tk.Button(self.root, text=shape, command=lambda s=shape.lower(): self.set_tool(s))
            button.pack(side="left", padx=10)

    def init_editing_buttons(self):
        tools = ["Move", "Resize", "Delete"]
        for tool in tools:
            button = tk.Button(self.root, text=tool, command=lambda t=tool.lower(): self.set_tool(t))
            button.pack(side="left", padx=10)

    def init_color_button(self):
        self.color_button = tk.Button(self.root, text="Color", command=self.pick_color)
        self.color_button.pack(side="left", padx=10)

    def init_layer_buttons(self):
        self.layer_up_button = tk.Button(self.root, text="Layer Up", command=self.layer_up)
        self.layer_up_button.pack(side="right", padx=10)

        self.layer_down_button = tk.Button(self.root, text="Layer Down", command=self.layer_down)
        self.layer_down_button.pack(side="right", padx=10)

    def init_bindings(self):
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.current_tool == "text":
            self.text_input = tk.Entry(self.canvas, bd=2)
            self.text_input.place(x=self.start_x, y=self.start_y)
            self.text_input.focus_set()

    def draw_shape(self, event):
        if self.current_tool == "arrow":
            self.canvas.delete("arrow_temp")
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, arrow=tk.LAST, tags="arrow_temp", fill=self.selected_color)
        elif self.current_tool == "text":
            pass
        else:
            self.canvas.delete("current_shape")
            x0, y0 = self.start_x, self.start_y
            x1, y1 = event.x, event.y
            if self.snap_enabled:
                x1 = round(x1 / self.grid_size) * self.grid_size
                y1 = round(y1 / self.grid_size) * self.grid_size
            if self.current_tool == "rectangle":
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.selected_color, tags="current_shape")
            elif self.current_tool == "circle":
                self.canvas.create_oval(x0, y0, x1, y1, fill=self.selected_color, tags="current_shape")

    def finish_draw(self, event):
        if self.current_tool == "arrow":
            self.canvas.delete("arrow_temp")
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, arrow=tk.LAST, fill=self.selected_color, width=2, tags="shape", arrowshape=(8, 10, 3))
        elif self.current_tool == "text":
            self.text_input.place_forget()
            text = self.text_input.get()
            if text:
                self.canvas.create_text(self.start_x, self.start_y, text=text, fill=self.selected_color, anchor=tk.NW, tags="shape")
        else:
            shape = self.canvas.find_withtag("current_shape")
            if shape:
                self.shapes.append(shape[0])
                self.layers[self.current_layer].append(shape[0])

    def set_tool(self, tool):
        self.current_tool = tool

    # Other methods omitted for brevity

def main():
    root = tk.Tk()
    app = DrawingApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
