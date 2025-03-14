# gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from edf_processor import EDFProcessor
from config.settings import settings

def create_gui():
    """
    Creates a graphical user interface for processing EDF files.

    :return: The root window of the application.
    """
    # Create the main window
    root = tk.Tk()
    root.title("EDF Segment Processor")
    root.geometry("1700x700")

    # Configure styles for buttons and frames
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")
    style.configure("TFrame", background="#f0f0f0")

    # Main frame for placing interface elements
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame for settings (minimum segment duration)
    settings_frame = ttk.Frame(main_frame)
    settings_frame.pack(fill=tk.X, pady=(0, 10))

    # Entry field for minimum segment duration
    ttk.Label(settings_frame, text="Min. segment duration (sec):").pack(side=tk.LEFT, padx=5)
    min_duration_entry = ttk.Entry(settings_frame, width=10)
    min_duration_entry.insert(0, str(settings.MIN_SEGMENT_DURATION))  # Set default value
    min_duration_entry.pack(side=tk.LEFT, padx=5)

    def apply_min_duration():
        """
        Applies the minimum segment duration entered by the user.
        """
        try:
            min_duration = float(min_duration_entry.get())
            if min_duration <= 0:
                raise ValueError("Duration must be greater than 0.")
            settings.MIN_SEGMENT_DURATION = min_duration  # Update value in settings
            messagebox.showinfo("Success", f"Minimum duration set: {min_duration} sec.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Button to apply minimum duration
    ttk.Button(settings_frame, text="Apply", command=apply_min_duration).pack(side=tk.LEFT, padx=5)

    # Output text area (ScrolledText)
    output_area = scrolledtext.ScrolledText(main_frame, width=100, height=25, wrap=tk.WORD)
    output_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    def copy_text(event=None):
        """
        Copies selected text from the output area to the clipboard.

        :param event: The event (optional).
        """
        try:
            selected_text = output_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            root.clipboard_clear()
            root.clipboard_append(selected_text)
        except tk.TclError:
            pass  # If no text is selected, do nothing

    # Bind Ctrl+C to the copy function
    output_area.bind("<Control-c>", copy_text)
    output_area.bind("<Control-C>", copy_text)

    # Frame for buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X)

    # Create an instance of EDFProcessor for data processing
    processor = EDFProcessor(output_area)

    def select_file():
        """
        Opens a dialog to select an EDF file and loads its metadata.
        """
        file_path = filedialog.askopenfilename(
            title="Select EDF File",
            filetypes=[("EDF files", "*.edf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                processor.load_metadata(file_path)  # Load metadata
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Show error if something goes wrong

    # "Open EDF File" button
    btn_open = ttk.Button(button_frame, text="Open EDF File", command=select_file)
    btn_open.pack(side=tk.LEFT, padx=5, pady=5)

    # "Split into Segments" button
    btn_process = ttk.Button(button_frame, text="Split into Segments", command=processor.process)
    btn_process.pack(side=tk.LEFT, padx=5, pady=5)

    # "Exit" button
    btn_exit = ttk.Button(button_frame, text="Exit", command=root.destroy)
    btn_exit.pack(side=tk.RIGHT, padx=5, pady=5)

    return root

if __name__ == "__main__":
    # Launch the application
    app = create_gui()
    app.mainloop()