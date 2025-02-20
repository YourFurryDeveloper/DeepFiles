import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

class FileExplorerApp:
    def __init__(self, root, fs_data):
        self.root = root
        self.root.title("File Explorer")
        
        # Create a label at the top for showing the selected file path
        self.path_label = tk.Label(self.root, text="Select a file", anchor="w", padx=10)
        self.path_label.pack(fill="x")

        # Treeview widget
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)

        self.content_frame = tk.Frame(self.root, height=15)
        self.content_frame.pack(fill="x", expand=False)

        # Insert the root of the file system into the tree
        self.insert_data("", fs_data)
        
        # Bind the select event to update the file path
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def insert_data(self, parent, data, current_path=""):
        """
        Recursively inserts files and directories into the tree view.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{current_path}/{key}" if current_path else key
                if isinstance(value, dict):  # It's a directory
                    node = self.tree.insert(parent, "end", text=key, open=False)
                    self.insert_data(node, value, new_path)  # Recursively insert files/folders
                elif isinstance(value, str):  # It's a file
                    self.tree.insert(parent, "end", text=value, iid=new_path)  # Insert the file name with its path

    def on_select(self, event):
        """Event handler for treeview item selection."""
        selected_item = self.tree.selection()
        global parent_directory
        global item_name
        if selected_item:
            selected_item = selected_item[0]
            selected_path = selected_item  # Full path is stored in the iid of the item
            item_name = self.tree.item(selected_item, "text")  # The item text (file or directory name)
            
            # Remove the file name or directory name from the path, getting the parent directory
            parent_directory = os.path.dirname(selected_path)
            value = parent_directory + "/" + item_name
            # Update the label with both the parent directory and item value (content for directories, filename for files)
            self.path_label.config(text=f"Selected item: {parent_directory}/{item_name}")
            if isinstance(value, str):  # If it's a file
                self.display_file_content(selected_path)
    
    def get_value_from_path(self, path):
        """Given a path, retrieve the value from the fs_data."""
        keys = path.strip('/').split('/')
        data = self.fs_data
        
        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None  # Path not found

        # Return the value of the last key (which could be a file or directory contents)
        return data if isinstance(data, str) else ', '.join(data.keys())

    def display_file_content(self, file_path):
        """Display the content of the selected file based on its type."""
        # Clear any previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        file_path = parent_directory + "/" + item_name
        file_extension = os.path.splitext(file_path)[1].lower()  # Get file extension

        file_path = parent_directory + "/" + item_name
        if file_extension in ['.txt', '.css']:
            self.display_text_file(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
            self.display_image(file_path)
        elif file_extension == '.py':
            self.display_python_file(file_path)
        else:
            self.display_unknown_file(file_path)
    
    def display_text_file(self, file_path):
        """Display the content of a text file."""
        try:
            with open(file_path, "r") as file:
                contents = file.read()

            text_widget = tk.Text(self.content_frame, wrap="word", height=10)
            text_widget.pack(fill="both", expand=True)
            text_widget.insert(tk.END, contents)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

    def display_image(self, file_path):
        """Display an image file."""
        from PIL import Image, ImageTk  # Pillow library for image handling

        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Resize image to fit into the window
            img_tk = ImageTk.PhotoImage(img)
            
            img_label = tk.Label(self.content_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to the image object
            img_label.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening image: {e}")

    def display_python_file(self, file_path):
        """Display a Python file content in a syntax-highlighted way."""
        try:
            with open(file_path, "r") as file:
                contents = file.read()

            text_widget = tk.Text(self.content_frame, wrap="word", height=10)
            text_widget.pack(fill="both", expand=True)
            text_widget.insert(tk.END, contents)

            # Here you can add some syntax highlighting, etc.
        except Exception as e:
            messagebox.showerror("Error", f"Error reading Python file: {e}")

    def display_unknown_file(self, file_path):
        """Handle unknown file types."""
        label = tk.Label(self.content_frame, text="Unsupported file type", fg="red")
        label.pack()

def load_fs_data(filename="fs.json"):
    """Load file system data from a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

def run_app():
    fs_data = load_fs_data()  # Load the file system data from fs.json
    
    root = tk.Tk()  # Initialize Tkinter root window
    app = FileExplorerApp(root, fs_data)  # Initialize the File Explorer app
    root.geometry("1200x800")  # Set window size
    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    run_app()
