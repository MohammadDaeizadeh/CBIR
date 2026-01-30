import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Ensure parent directory is in path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector_db.crud import ImageRetriever

class CBIRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Search Engine - ResNet18 & LSH")
        self.root.geometry("1200x750")
        
        # Set modern color scheme
        self.bg_color = "#d3e9ff"
        self.primary_color = "#172c3a"
        self.secondary_color = "#1c5587"
        self.accent_color = "#7a2626"
        self.card_bg = "#ffffff"
        self.border_color = "#dee2e6"
        self.text_color = "#2c3e50"
        self.light_text = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize Logic
        if not os.path.exists("data"):
            os.makedirs("data")
        self.retriever = ImageRetriever(vector_db_path="data/vectors.npy", meta_db_path="data/metadata.json")
        
        self.query_image_path = None
        
        self._setup_ui()

    def _setup_ui(self):
        # --- Header ---
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title and subtitle
        title_container = tk.Frame(header_frame, bg=self.primary_color)
        title_container.pack(side=tk.LEFT, padx=20, pady=10)
        
        title_label = tk.Label(title_container, text="🔍 Content-Based Image Retrieval", 
                              font=("Segoe UI", 16, "bold"), 
                              bg=self.primary_color, fg="white")
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(title_container, text="ResNet18 & LSH", 
                                 font=("Segoe UI", 10), 
                                 bg=self.primary_color, fg="white")
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Credits in header
        credits_label = tk.Label(header_frame, 
                                text="by Sadra Seyedtabaei & Mohammad Daeizadeh",
                                font=("Segoe UI", 9, "italic"), 
                                bg=self.primary_color, fg="white")
        credits_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # --- Control Panel ---
        control_frame = tk.Frame(self.root, bg=self.card_bg, padx=20, pady=12)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Search Method
        method_frame = tk.Frame(control_frame, bg=self.card_bg)
        method_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        tk.Label(method_frame, text="Search Algorithm:", 
                font=("Segoe UI", 10, "bold"), 
                bg=self.card_bg, fg=self.text_color).pack(anchor="w")
        
        self.method_var = tk.StringVar(value="Brute Force")
        method_combo = ttk.Combobox(method_frame, textvariable=self.method_var, 
                                   values=["Brute Force", "LSH (Fast Approximate)"], 
                                   state="readonly", width=25, font=("Segoe UI", 10))
        method_combo.pack(pady=5)
        
        # Buttons Frame
        button_frame = tk.Frame(control_frame, bg=self.card_bg)
        button_frame.pack(side=tk.LEFT, padx=10)
        
        button_style = {"font": ("Segoe UI", 10), "bd": 0, "relief": tk.FLAT, "cursor": "hand2"}
        
        load_btn = tk.Button(button_frame, text="📁 Load Query Image", 
                            command=self.load_image, 
                            bg=self.secondary_color, fg="white",
                            padx=15, pady=8, **button_style)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(button_frame, text="🔍 Search Similar Images", 
                              command=self.search, 
                              bg=self.accent_color, fg="white",
                              padx=15, pady=8, **button_style)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = tk.Label(control_frame, text="Ready", 
                                    font=("Segoe UI", 9, "italic"), 
                                    bg=self.card_bg, fg="#7f8c8d")
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # --- Main Content Area ---
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Left: Query Panel
        query_panel = tk.Frame(content_frame, bg=self.card_bg, 
                              highlightbackground=self.border_color, 
                              highlightthickness=1)
        query_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Query Header
        query_header = tk.Frame(query_panel, bg=self.secondary_color, height=35)
        query_header.pack(fill=tk.X)
        query_header.pack_propagate(False)
        
        tk.Label(query_header, text="Query Image", 
                font=("Segoe UI", 11, "bold"), 
                bg=self.secondary_color, fg="white").pack(pady=10)
        
        # Query Image Display
        query_body = tk.Frame(query_panel, bg=self.card_bg)
        query_body.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.query_label = tk.Label(query_body, text="📸 No image selected\n\nClick 'Load Query Image' to begin", 
                                   font=("Segoe UI", 10), 
                                   bg=self.card_bg, fg=self.text_color,
                                   justify=tk.CENTER)
        self.query_label.pack(expand=True)
        
        # Right: Results Panel
        results_panel = tk.Frame(content_frame, bg=self.card_bg, 
                                highlightbackground=self.border_color, 
                                highlightthickness=1)
        results_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Results Header
        results_header = tk.Frame(results_panel, bg=self.primary_color, height=35)
        results_header.pack(fill=tk.X)
        results_header.pack_propagate(False)
        
        self.results_title = tk.Label(results_header, text="Search Results (0 images)", 
                                     font=("Segoe UI", 11, "bold"), 
                                     bg=self.primary_color, fg="white")
        self.results_title.pack(pady=10)
        
        # Scrollable Results Area
        results_canvas = tk.Canvas(results_panel, bg=self.card_bg, highlightthickness=0)
        results_scrollbar = ttk.Scrollbar(results_panel, orient="vertical", 
                                         command=results_canvas.yview)
        self.results_frame = tk.Frame(results_canvas, bg=self.card_bg)
        
        self.results_frame.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )
        
        results_canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Query Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.query_image_path = file_path
            self.display_image(file_path, self.query_label, size=(300, 300))
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}", fg="#2ecc71")

    def display_image(self, path, label_widget, size=(200, 200)):
        try:
            img = Image.open(path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Create rounded corners effect
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), img.size], radius=15, fill=255)
            
            # Use RGBA for transparency support
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            result = Image.new('RGBA', img.size, (255, 255, 255, 0))
            result.paste(img, mask=mask)
            
            img_tk = ImageTk.PhotoImage(result)
            label_widget.config(image=img_tk, text="", bg=self.card_bg)
            label_widget.image = img_tk
            
        except Exception as e:
            label_widget.config(text=f"Error loading image\n{str(e)}", image="", 
                               bg=self.card_bg)

    def search(self):
        if not self.query_image_path:
            messagebox.showwarning("Warning", "Please select a query image first.")
            return

        method = "brute_force" if "Brute Force" in self.method_var.get() else "lsh"
        
        try:
            self.status_label.config(text="Searching...", fg="#f39c12")
            self.root.update()
            
            results = self.retriever.search(self.query_image_path, k=12, method=method)
            
            # Clear previous results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            if not results:
                tk.Label(self.results_frame, text="No results found.", 
                        font=("Segoe UI", 11), 
                        bg=self.card_bg, fg=self.text_color).pack(pady=50)
                self.results_title.config(text="Search Results (0 images)")
                return
            
            # Update results title
            method_display = "Brute Force" if method == "brute_force" else "LSH"
            self.results_title.config(text=f"Search Results ({len(results)} images) • Method: {method_display}")
            
            # Grid Layout for results
            row = 0
            col = 0
            max_cols = 4
            
            for idx, res in enumerate(results):
                # Create result card
                card = tk.Frame(self.results_frame, bg="#f8f9fa", 
                               highlightbackground=self.border_color, 
                               highlightthickness=1)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                # Image container
                img_container = tk.Frame(card, bg="#f8f9fa", padx=5, pady=5)
                img_container.pack(padx=5, pady=5)
                
                img_label = tk.Label(img_container, bg="#f8f9fa")
                img_label.pack()
                
                if os.path.exists(res['path']):
                    self.display_image(res['path'], img_label, size=(150, 150))
                else:
                    img_label.config(text="Image not found", 
                                    font=("Segoe UI", 9), 
                                    bg="#f8f9fa", fg=self.accent_color)
                
                # Info panel
                info_frame = tk.Frame(card, bg="#f8f9fa")
                info_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
                
                # Distance/Category
                score_text = f"Distance: {res['score']:.4f}"
                tk.Label(info_frame, text=score_text, 
                        font=("Segoe UI", 9), 
                        bg="#f8f9fa", fg=self.text_color).pack(anchor="w")
                
                category_text = f"Category: {res['category']}"
                tk.Label(info_frame, text=category_text, 
                        font=("Segoe UI", 9), 
                        bg="#f8f9fa", fg=self.primary_color).pack(anchor="w")
                
                # Result number
                tk.Label(card, text=f"#{idx+1}", 
                        font=("Segoe UI", 8, "bold"), 
                        bg=self.secondary_color, fg="white",
                        padx=5, pady=1).place(x=5, y=5)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
            
            # Configure grid columns
            for i in range(max_cols):
                self.results_frame.grid_columnconfigure(i, weight=1, uniform="col")
            
            self.status_label.config(text=f"Found {len(results)} results", fg="#27ae60")
            
        except Exception as e:
            self.status_label.config(text="Search failed", fg=self.accent_color)
            messagebox.showerror("Error", f"Search failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set window icon (optional - add if you have icon.ico)
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    # Configure ttk style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox', fieldbackground='white', background='white')
    
    app = CBIRApp(root)
    root.mainloop()