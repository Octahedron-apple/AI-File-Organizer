import tkinter as tk

root = tk.Tk()
root.title("AI File Organizer")
root.geometry("1920x1080")
root.configure(bg="black")

left_frame = tk.Frame(root, bg="black")
left_frame.pack(side="left", expand=True, fill="both", padx=20, pady=20)

right_frame = tk.Frame(root, bg="black")
right_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

file_label = tk.Label(left_frame, text="File Name:", fg="white", bg="black", font=("Arial", 16))
file_label.pack(anchor="w", pady=10)

content_text = tk.Text(left_frame, fg="white", bg="#1a1a1a", insertbackground="white", font=("Arial", 12))
content_text.pack(expand=True, fill="both")

response_label = tk.Label(right_frame, text="AI Response:", fg="white", bg="black", font=("Arial", 16))
response_label.pack(anchor="w", pady=10)

response_text = tk.Text(right_frame, fg="white", bg="#1a1a1a", insertbackground="white", font=("Arial", 12))
response_text.pack(expand=True, fill="both")

root.mainloop()
