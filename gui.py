import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OG:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AI File Organizer")
        self.root.geometry("1200x800")
        
        self.config_frame = ctk.CTkFrame(self.root)
        self.config_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        self.provider_var = ctk.StringVar(value="Ollama")
        self.provider_menu = ctk.CTkOptionMenu(self.config_frame, values=["Ollama", "OpenRouter"], variable=self.provider_var)
        self.provider_menu.pack(side="left", padx=10, pady=10)
        
        self.model_var = ctk.StringVar(value="qwen3.5:2b")
        self.model_entry = ctk.CTkEntry(self.config_frame, textvariable=self.model_var, placeholder_text="Model Name")
        self.model_entry.pack(side="left", padx=10, pady=10)
        
        self.api_key_var = ctk.StringVar(value="")
        self.api_key_entry = ctk.CTkEntry(self.config_frame, textvariable=self.api_key_var, placeholder_text="OpenRouter API Key", show="*")
        self.api_key_entry.pack(side="left", expand=True, fill="x", padx=10, pady=10)
        
        self.start_button = ctk.CTkButton(self.config_frame, text="Start Organizing")
        self.start_button.pack(side="right", padx=10, pady=10)
        
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", expand=True, fill="both", padx=(0, 10))

        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side="right", expand=True, fill="both", padx=(10, 0))

        self.file_label = ctk.CTkLabel(self.left_frame, text="File Name:", font=("Arial", 18, "bold"))
        self.file_label.pack(anchor="w", padx=20, pady=(20, 10))

        self.content_text = ctk.CTkTextbox(self.left_frame, font=("Arial", 14), wrap="word")
        self.content_text.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.image_label = ctk.CTkLabel(self.left_frame, text="")

        self.category_label = ctk.CTkLabel(self.right_frame, text="Assigned Category: -", font=("Arial", 20, "bold"), text_color="#2ECC71")
        self.category_label.pack(anchor="w", padx=20, pady=(20, 10))

        self.response_label = ctk.CTkLabel(self.right_frame, text="AI Response:", font=("Arial", 18, "bold"))
        self.response_label.pack(anchor="w", padx=20, pady=(10, 10))

        self.response_text = ctk.CTkTextbox(self.right_frame, font=("Arial", 14), wrap="word")
        self.response_text.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.progress_bar = ctk.CTkProgressBar(self.root)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 20))
        self.progress_bar.set(0)

