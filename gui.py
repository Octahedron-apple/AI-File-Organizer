import tkinter as tk

class OG:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI File Organizer")
        self.root.geometry("1920x1080")
        self.root.configure(bg="black")

        self.left_frame = tk.Frame(self.root, bg="black")
        self.left_frame.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        self.right_frame = tk.Frame(self.root, bg="black")
        self.right_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        self.file_label = tk.Label(self.left_frame, text="File Name:", fg="white", bg="black", font=("Arial", 16))
        self.file_label.pack(anchor="w", pady=10)

        self.content_text = tk.Text(self.left_frame, fg="white", bg="#1a1a1a", insertbackground="white", font=("Arial", 12))
        self.content_text.pack(expand=True, fill="both")

        self.image_label = tk.Label(self.left_frame, bg="black")

        self.category_label = tk.Label(self.right_frame, text="Assigned Category: -", fg="green", bg="black", font=("Arial", 18, "bold"))
        self.category_label.pack(anchor="w", pady=10)

        self.response_label = tk.Label(self.right_frame, text="AI Response:", fg="white", bg="black", font=("Arial", 16))
        self.response_label.pack(anchor="w", pady=10)

        self.response_text = tk.Text(self.right_frame, fg="white", bg="#1a1a1a", insertbackground="white", font=("Arial", 12))
        self.response_text.pack(expand=True, fill="both")
