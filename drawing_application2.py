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

        # Add buttons for drawing shapes
        self.rect_button = tk.Button(self.root, text="Rectangle", command=lambda: self.set_tool("rectangle"))
        self.rect_button.pack(side="left", padx=10)

        self.circle_button = tk.Button(self.root, text="Circle", command=lambda: self.set_tool("circle"))
        self.circle_button.pack(side="left", padx=10)

        self.arrow_button = tk.Button(self.root, text="Arrow", command=lambda: self.set_tool("arrow"))
        self.arrow_button.pack(side="left", padx=10)

        self.text_button = tk.Button(self.root, text="Text", command=lambda: self.set_tool("text"))
        self.text_button.pack(side="left", padx=10)

        # Add editing tools
        self.move_button = tk.Button(self.root, text="Move", command=self.move_shape)
        self.move_button.pack(side="left", padx=10)

        self.resize_button = tk.Button(self.root, text="Resize", command=self.resize_shape)
        self.resize_button.pack(side="left", padx=10)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_shape)
        self.delete_button.pack(side="left", padx=10)

        # Add color picker button
        self.color_button = tk.Button(self.root, text="Color", command=self.pick_color)
        self.color_button.pack(side="left", padx=10)

        # Add layer controls
        self.layer_up_button = tk.Button(self.root, text="Layer Up", command=self.layer_up)
        self.layer_up_button.pack(side="right", padx=10)

        self.layer_down_button = tk.Button(self.root, text="Layer Down", command=self.layer_down)
        self.layer_down_button.pack(side="right", padx=10)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)

        # Grid and snap settings
        self.grid_enabled = True
        self.snap_enabled = True
        self.grid_size = 20

        # Text annotation variables
        self.text_input = None

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
            elif self.current_tool == "text":
                pass

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

    def move_shape(self):
        if self.selected_shape:
            self.canvas.tag_bind(self.selected_shape, "<ButtonPress-1>", self.start_move)
            self.canvas.tag_bind(self.selected_shape, "<B1-Motion>", self.do_move)
            self.canvas.tag_bind(self.selected_shape, "<ButtonRelease-1>", self.finish_move)

    def start_move(self, event):
        self.start_move_x = event.x
        self.start_move_y = event.y

    def do_move(self, event):
        delta_x = event.x - self.start_move_x
        delta_y = event.y - self.start_move_y
        self.canvas.move(self.selected_shape, delta_x, delta_y)
        self.start_move_x = event.x
        self.start_move_y = event.y

    def finish_move(self, event):
        self.selected_shape = None
        self.canvas.tag_unbind("shape", "<ButtonPress-1>")
        self.canvas.tag_unbind("shape", "<B1-Motion>")
        self.canvas.tag_unbind("shape", "<ButtonRelease-1>")

    def resize_shape(self):
        pass  # Implement resizing shapes

    def delete_shape(self):
        if self.selected_shape:
            self.shapes.remove(self.selected_shape)
            self.canvas.delete(self.selected_shape)
            self.selected_shape = None

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.selected_color = color

    def layer_up(self):
        if self.current_layer < max(self.layers.keys()):
            self.current_layer += 1
            self.canvas.lift(self.layers[self.current_layer])

    def layer_down(self):
        if self.current_layer > 0:
            self.current_layer -= 1
            self.canvas.lower(self.layers[self.current_layer])

    def undo(self):
        if self.shapes:
            shape = self.shapes.pop()
            self.undo_stack.append(shape)
            self.canvas.delete(shape)

    def redo(self):
        if self.undo_stack:
            shape = self.undo_stack.pop()
            self.shapes.append(shape)
            self.canvas.itemconfigure(shape, state="normal")

    def toggle_grid(self):
        self.grid_enabled = not self.grid_enabled
        if self.grid_enabled:
            self.canvas.grid(sticky="news")
        else:
            self.canvas.grid_remove()

    def toggle_snap(self):
        self.snap_enabled = not self.snap_enabled

    def save_drawing(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            data = {"shapes": self.shapes, "layers": self.layers}
            with open(filename, "w") as file:
                json.dump(data, file)
            messagebox.showinfo("Save Successful", "Drawing saved successfully.")

    def load_drawing(self):
        filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r") as file:
                data = json.load(file)
                for shape_id in data["shapes"]:
                    self.shapes.append(shape_id)
                    self.layers[self.current_layer].append(shape_id)
                self.canvas.lift("shape")
            messagebox.showinfo("Load Successful", "Drawing loaded successfully.")

def main():
    root = tk.Tk()
    app = DrawingApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
