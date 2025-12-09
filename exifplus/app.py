import threading
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

import exifread
from PIL import Image
import pyexiv2
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


class MetadataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Metadata Viewer/Editor (EXIF • XMP • IPTC • Meta Data)")
        self.root.geometry("1000x650")

        self.style = tb.Style("flatly")

        # Top frame
        control_frame = tb.Frame(root, padding=10)
        control_frame.pack(fill=X)

        tb.Button(control_frame, text="Open File", bootstyle=PRIMARY,
                  command=self.open_file).pack(side=LEFT, padx=5)

        tb.Button(control_frame, text="Save Metadata", bootstyle=SUCCESS,
                  command=self.save_metadata).pack(side=LEFT, padx=5)

        tb.Button(control_frame, text="About", bootstyle=INFO,
                  command=self.show_about).pack(side=LEFT, padx=5)

        self.file_label = tb.Label(control_frame, text="No file selected", bootstyle=INFO)
        self.file_label.pack(side=LEFT, padx=10)

        # Table frame
        table_frame = tb.Frame(root, padding=10)
        table_frame.pack(fill=BOTH, expand=True)

        self.tree = tb.Treeview(table_frame, columns=("key", "value"), show="headings")
        self.tree.heading("key", text="Key")
        self.tree.heading("value", text="Value")

        self.tree.column("key", width=300)
        self.tree.column("value", width=600)

        self.tree.pack(fill=BOTH, expand=True)

        # Editable by double-click
        self.tree.bind("<Double-1>", self.edit_cell)

        # Right-click menu for delete
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.edit_window = None
        self.edit_entry = None
        self.editing_item = None
        self.editing_column = None

        self.metadata_dict = {}
        self.current_file = None

    # -----------------------------
    # Context Menu
    # -----------------------------
    def show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            # Create the context menu (right-click menu)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Context Menu")
            # Add "Delete Row" option to the context menu
            menu.add_command(label="Delete Row", command=lambda: self.confirm_delete(row_id))
            # Add "Add Row Below" option to the context menu
            menu.add_command(label="Add Row Below", command=lambda: self.show_add_row_popup(row_id))
            
            # Display the context menu at the position where the right-click happened
            menu.post(event.x_root, event.y_root)
            def close_menu(event):
                menu.unpost()

            # Bind the close_menu function to any click in the window (except on the context menu)
            self.root.bind("<Button-1>", close_menu, add='+')  # Left-click
            self.root.bind("<Button-3>", close_menu, add='+')  # Right-click
            
            # Unbind the close event when the menu is used
            def on_menu_click():
                self.root.unbind("<Button-1>", close_menu)
                self.root.unbind("<Button-3>", close_menu)

            # Bind on_menu_click when a command is clicked
            for menu_item in menu.winfo_children():
                menu_item.config(command=lambda item=menu_item: [item.invoke(), on_menu_click()])

    # -----------------------------
    # Confirm Deletion
    # -----------------------------
    def confirm_delete(self, row_id):
        # Ask the user for confirmation before deleting
        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this row?")
        
        if confirmation:
            # If confirmed, proceed with deletion
            self.delete_row(row_id)
        else:
            # If not confirmed, do nothing
            print("Deletion canceled.")

    # -----------------------------
    # Delete Row
    # -----------------------------
    def delete_row(self, row_id):
        # Delete the row from the treeview and the metadata dictionary
        if row_id in self.metadata_dict:
            del self.metadata_dict[row_id]
        self.tree.delete(row_id)

    # -----------------------------
    # Add Row Below - Show Popup for Type Selection
    # -----------------------------
    def show_add_row_popup(self, row_id):
        # Pop-up to select EXIF, XMP, or IPTC
        popup = tk.Toplevel(self.root)
        popup.title("Select Metadata Type")
        popup.geometry("300x200")
        
        tb.Label(popup, text="Choose Metadata Type").pack(pady=10)
        
        def add_row(metadata_type):
            # Add the selected metadata type row
            self.add_row_below(row_id, metadata_type)
            popup.destroy()

        tb.Button(popup, text="EXIF", bootstyle=PRIMARY, command=lambda: add_row("EXIF")).pack(pady=5)
        tb.Button(popup, text="IPTC", bootstyle=PRIMARY, command=lambda: add_row("IPTC")).pack(pady=5)
        tb.Button(popup, text="XMP", bootstyle=PRIMARY, command=lambda: add_row("XMP")).pack(pady=5)

    # -----------------------------
    # Add Row Below Function
    # -----------------------------
    def add_row_below(self, row_id, metadata_type):
        # Add a new row below the selected row
        # For now, we will add a placeholder key-value pair based on metadata type
        if metadata_type == "EXIF":
            new_key = "Exif.Image.NewField"
            new_value = "New EXIF Data"
        elif metadata_type == "IPTC":
            new_key = "Iptc.Application2.NewField"
            new_value = "New IPTC Data"
        elif metadata_type == "XMP":
            new_key = "Xmp.::NewField"
            new_value = "New XMP Data"
        
        # Insert the new row into the Treeview
        self.metadata_dict[new_key] = new_value
        self.tree.insert("", "end", iid=new_key, values=(new_key, new_value))



    # -----------------------------
    # Open File
    # -----------------------------
    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=(
            ("Images & Video", "*.jpg *.jpeg *.png *.tiff *.mp4 *.mov *.mkv *.avi *.heic"),
            ("All files", "*.*")
        ))

        if filename:
            self.current_file = filename
            self.file_label.config(text=filename)

            for row in self.tree.get_children():
                self.tree.delete(row)

            threading.Thread(target=self.load_metadata, daemon=True).start()

    # -----------------------------
    # Load metadata
    # -----------------------------
    def load_metadata(self):
        self.metadata_dict = {}
        path = self.current_file

        try:
            # Read EXIF
            if path.lower().endswith((".jpg", ".jpeg", ".tiff", ".png", ".heic")):
                with open(path, 'rb') as f:
                    image_bytes = f.read()  # Read the image as bytes
                    with pyexiv2.ImageData(image_bytes) as img:  # Open image from bytes
                        # Read metadata
                        for key, value in img.read_exif().items():
                            self.metadata_dict[key] = str(value)

                        # Read IPTC metadata
                        for key, value in img.read_iptc().items():
                            self.metadata_dict[key] = str(value)

                        # Read XMP metadata
                        for key, value in img.read_xmp().items():
                            self.metadata_dict[key] = str(value)

            # Video metadata
            if path.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
                parser = createParser(path)
                metadata = extractMetadata(parser)
                if metadata:
                    for item in metadata.exportPlaintext():
                        key, val = item.split(":", 1)
                        self.metadata_dict[key.strip()] = val.strip()

        except Exception as e:
            messagebox.showerror("Error", f"Error loading metadata:\n{e}")
            return

        self.refresh_table()

    # -----------------------------
    # Refresh table
    # -----------------------------
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for k, v in self.metadata_dict.items():
            self.tree.insert("", END, iid=k, values=(k, v))

    # -----------------------------
    # Edit table cell
    # -----------------------------
    def edit_cell(self, event):
        row_id = self.tree.focus()
        if not row_id:
            return

        col = self.tree.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1  # 0 = key, 1 = value

        self.editing_item = row_id
        self.editing_column = col_index

        old_value = self.tree.item(row_id)["values"][col_index]

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit")
        self.edit_window.geometry("400x150")

        tb.Label(self.edit_window, text="Editing Cell").pack(pady=10)

        self.edit_entry = tb.Entry(self.edit_window)
        self.edit_entry.insert(0, old_value)
        self.edit_entry.pack(fill=X, padx=20)

        tb.Button(self.edit_window, text="Save", bootstyle=SUCCESS,
                  command=self.apply_edit).pack(pady=10)

    def apply_edit(self):
        new_value = self.edit_entry.get()

        old_key = self.editing_item

        # Editing KEY
        if self.editing_column == 0:
            new_key = new_value

            # Update dict
            if new_key in self.metadata_dict:
                messagebox.showerror("Error", "Key already exists!")
                return

            self.metadata_dict[new_key] = self.metadata_dict.pop(old_key)

            # Update table row
            self.tree.delete(old_key)
            self.tree.insert("", END, iid=new_key, values=(new_key, self.metadata_dict[new_key]))

        else:
            # Editing VALUE
            self.metadata_dict[old_key] = new_value
            self.tree.item(old_key, values=(old_key, new_value))

        self.edit_window.destroy()

    # -----------------------------
    # Save metadata to file
    # -----------------------------
    def save_metadata(self):
        if not self.current_file:
            messagebox.showerror("Error", "No file opened.")
            return

        threading.Thread(target=self._save_metadata_thread, daemon=True).start()

    def _save_metadata_thread(self):
        try:
            with open(self.current_file, 'rb+') as f:
                image_bytes = f.read()  # Read the image as bytes
                with pyexiv2.ImageData(image_bytes) as img:  # Open image from bytes
                    # Prepare the changes dictionary
                    changes = {}

                    # Modify EXIF
                    try:
                        exif_data = img.read_exif()
                        for key, val in self.metadata_dict.items():
                            if key in exif_data:  # Ensure the key exists in EXIF metadata
                                changes[key] = val
                        if changes:
                            img.modify_exif(changes)  # Modify EXIF metadata
                    except Exception as exif_error:
                        print(f"Error modifying EXIF: {exif_error}")

                    # Modify IPTC
                    try:
                        iptc_data = img.read_iptc()
                        for key, val in self.metadata_dict.items():
                            if key in iptc_data:  # Ensure the key exists in IPTC metadata
                                changes[key] = val
                        if changes:
                            img.modify_iptc(changes)  # Modify IPTC metadata
                    except Exception as iptc_error:
                        print(f"Error modifying IPTC: {iptc_error}")

                    # Modify XMP
                    try:
                        xmp_data = img.read_xmp()
                        for key, val in self.metadata_dict.items():
                            if key in xmp_data:  # Ensure the key exists in XMP metadata
                                changes[key] = val
                        if changes:
                            img.modify_xmp(changes)  # Modify XMP metadata
                    except Exception as xmp_error:
                        print(f"Error modifying XMP: {xmp_error}")

                    # Write the modified bytes back to the file
                    f.seek(0)
                    f.truncate()
                    f.write(img.get_bytes())  # Save the modified image bytes

                messagebox.showinfo("Success", "Metadata saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving metadata:\n{e}")


    # -----------------------------
    # About Window
    # -----------------------------
    def show_about(self):
        about = tk.Toplevel(self.root)
        about.title("About")
        about.geometry("400x450")

        tb.Label(about, text="Metadata Viewer & Editor", font=("Arial", 14, "bold")).pack(pady=10)
        tb.Label(about, text="Author: Mohammed Zahid Wadiwale").pack()
        tb.Label(about, text="Company: Webaon").pack()
        tb.Label(about, text="Website: webaon.com", bootstyle=INFO).pack(pady=5)
        # Author section
        tb.Label(
            about,
            text="Developed By:",
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        tb.Label(
            about,
            text="Mohammed Zahid Wadiwale",
            font=("Arial", 12)
        ).pack(pady=2)
        tb.Separator(about, orient="horizontal").pack(fill="x", pady=10)
        # Links section
        tb.Label(
            about,
            text="Official Links",
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        link_style = {"font": ("Arial", 11), "foreground": "blue", "cursor": "hand2"}
        def make_link(label, url):
            widget = tb.Label(about, text=label, **link_style)
            widget.pack()
            widget.bind("<Button-1>", lambda e: subprocess.Popen(["xdg-open", url]))
        make_link("Website: www.webaon.com", "https://www.webaon.com/")
        make_link("GitHub: github.com/ZahidServers", "https://github.com/ZahidServers")
        make_link("Blog: blog.webaon.com", "https://blog.webaon.com/")
        make_link("Academy: academy.webaon.com", "https://academy.webaon.com/")
        tb.Separator(about, orient="horizontal").pack(fill="x", pady=10)

        tb.Button(about, text="OK", bootstyle=PRIMARY,
                  command=about.destroy).pack(pady=15)


def main():
    """Entry point to launch the GUI."""
    root = tb.Window(themename="flatly")
    app = MetadataApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
