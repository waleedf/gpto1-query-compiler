import tkinter as tk
from tkinter import filedialog, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import os
import json
from datetime import datetime
import threading
import queue

class FuturisticCodeConsolidator:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Consolidator by Waleed Faruki")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)  # Set minimum window size
        
        # Message queue for thread communication
        self.message_queue = queue.Queue()
        
        # Set theme
        self.style = ttk.Style("darkly")
        
        # Default patterns
        self.default_patterns = {
            "include": ["*.py", "*.js", "*.jsx", "*.ts", "*.tsx", "*.html", "*.css", "*.java", "*.cpp", "*.h", "*.c"],
            "exclude": ["node_modules/*", "venv/*", "*.pyc", "__pycache__/*", "*.git/*", "build/*", "dist/*"]
        }
        
        # Load saved settings
        self.settings = self.load_settings()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        # Main tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text='Main')
        
        # Settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text='Settings')
        
        self.setup_main_tab()
        self.setup_settings_tab()
        
        # Start message checking
        self.check_messages()
        
    def check_messages(self):
        try:
            while True:
                msg = self.message_queue.get_nowait()
                if msg['type'] == 'info':
                    Messagebox.show_info(msg['message'], "Success")
                elif msg['type'] == 'error':
                    Messagebox.show_error(msg['message'], "Error")
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_messages)
            
    def load_settings(self):
        try:
            if os.path.exists('consolidator_settings.json'):
                with open('consolidator_settings.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'include_patterns': self.default_patterns['include'],
            'exclude_patterns': self.default_patterns['exclude'],
            'default_header': "# Code Review Instructions\n\nPlease review the following codebase and provide feedback on:",
            'theme': 'darkly'
        }
        
    def setup_main_tab(self):
        # Directory Selection
        dir_frame = ttk.Frame(self.main_tab)
        dir_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(dir_frame, text="Project Directory:", font=("Helvetica", 10, "bold")).pack(side=LEFT)
        self.dir_entry = ttk.Entry(dir_frame, font=("Consolas", 10))
        self.dir_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory, bootstyle="outline-primary")
        browse_btn.pack(side=LEFT)
        
        # Instructions Card
        instructions_frame = ttk.LabelFrame(self.main_tab, text="Instructions for GPT", padding=10)
        instructions_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        self.header_text = scrolledtext.ScrolledText(
            instructions_frame,
            font=("Consolas", 10),
            height=10,
            background="#2b3e50",
            foreground="#ffffff",
            insertbackground="#ffffff"
        )
        self.header_text.pack(fill=BOTH, expand=YES)
        self.header_text.insert(END, self.settings['default_header'])
        
        # Output Configuration
        output_frame = ttk.LabelFrame(self.main_tab, text="Output Configuration", padding=10)
        output_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output File:").pack(side=LEFT)
        self.output_entry = ttk.Entry(output_frame, font=("Consolas", 10))
        self.output_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
        self.output_entry.insert(0, "consolidated_code.txt")
        
        # Generate Button
        generate_btn = ttk.Button(
            self.main_tab,
            text="🚀 Generate Consolidated Code",
            command=self.generate_with_progress,
            bootstyle="success",
            padding=10
        )
        generate_btn.pack(fill=X, padx=10, pady=10)
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(
            self.main_tab,
            bootstyle="success-striped",
            mode='indeterminate'
        )
        
        # Copyright
        copyright_frame = ttk.Frame(self.main_tab)
        copyright_frame.pack(side=BOTTOM, fill=X, pady=10)
        
        copyright_label = ttk.Label(
            copyright_frame,
            text=f"Created by Waleed Faruki © {datetime.now().year}",
            font=("Helvetica", 9, "bold"),
            bootstyle="secondary"
        )
        copyright_label.pack(expand=True)
        
    def setup_settings_tab(self):
        # File Patterns
        patterns_frame = ttk.LabelFrame(self.settings_tab, text="File Patterns", padding=10)
        patterns_frame.pack(fill=X, padx=10, pady=5)
        
        # Include patterns
        include_frame = ttk.Frame(patterns_frame)
        include_frame.pack(fill=X, pady=5)
        
        ttk.Label(include_frame, text="Include Patterns:", font=("Helvetica", 10, "bold")).pack(anchor=W)
        self.include_entry = ttk.Entry(include_frame, font=("Consolas", 10))
        self.include_entry.pack(fill=X, pady=2)
        self.include_entry.insert(0, ", ".join(self.settings['include_patterns']))
        
        ttk.Label(
            include_frame,
            text="Comma-separated glob patterns for files to include",
            bootstyle="secondary",
            font=("Helvetica", 8)
        ).pack(anchor=W)
        
        # Exclude patterns
        exclude_frame = ttk.Frame(patterns_frame)
        exclude_frame.pack(fill=X, pady=10)
        
        ttk.Label(exclude_frame, text="Exclude Patterns:", font=("Helvetica", 10, "bold")).pack(anchor=W)
        self.exclude_entry = ttk.Entry(exclude_frame, font=("Consolas", 10))
        self.exclude_entry.pack(fill=X, pady=2)
        self.exclude_entry.insert(0, ", ".join(self.settings['exclude_patterns']))
        
        ttk.Label(
            exclude_frame,
            text="Comma-separated glob patterns for files to exclude",
            bootstyle="secondary",
            font=("Helvetica", 8)
        ).pack(anchor=W)
        
        # Pattern Preview
        preview_frame = ttk.LabelFrame(self.settings_tab, text="Pattern Preview", padding=10)
        preview_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            font=("Consolas", 10),
            height=8,
            background="#2b3e50",
            foreground="#ffffff"
        )
        self.preview_text.pack(fill=BOTH, expand=YES)
        
        # Update preview when patterns change
        self.include_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        self.exclude_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        self.update_preview()
        
        # Buttons
        btn_frame = ttk.Frame(self.settings_tab)
        btn_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Button(
            btn_frame,
            text="Reset to Defaults",
            command=self.reset_to_defaults,
            bootstyle="outline-warning"
        ).pack(side=LEFT)
        
        ttk.Button(
            btn_frame,
            text="Save Settings",
            command=self.save_settings,
            bootstyle="success"
        ).pack(side=RIGHT)
        
    def update_preview(self):
        self.preview_text.delete(1.0, END)
        self.preview_text.insert(END, "Files that will be included:\n\n")
        
        include_patterns = [p.strip() for p in self.include_entry.get().split(",")]
        exclude_patterns = [p.strip() for p in self.exclude_entry.get().split(",")]
        
        self.preview_text.insert(END, "Include patterns:\n")
        for pattern in include_patterns:
            self.preview_text.insert(END, f"  • {pattern}\n")
            
        self.preview_text.insert(END, "\nExclude patterns:\n")
        for pattern in exclude_patterns:
            self.preview_text.insert(END, f"  • {pattern}\n")
        
    def reset_to_defaults(self):
        self.include_entry.delete(0, END)
        self.include_entry.insert(0, ", ".join(self.default_patterns["include"]))
        self.exclude_entry.delete(0, END)
        self.exclude_entry.insert(0, ", ".join(self.default_patterns["exclude"]))
        self.update_preview()
        
    def save_settings(self):
        settings = {
            'include_patterns': [p.strip() for p in self.include_entry.get().split(",")],
            'exclude_patterns': [p.strip() for p in self.exclude_entry.get().split(",")],
            'default_header': self.header_text.get("1.0", END),
            'theme': 'darkly'
        }
        try:
            with open('consolidator_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            Messagebox.show_info("Settings saved successfully!", "Success")
        except Exception as e:
            Messagebox.show_error(f"Failed to save settings: {str(e)}", "Error")
            
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, END)
            self.dir_entry.insert(0, directory)
            
    def should_include_file(self, file_path, include_patterns, exclude_patterns):
        from fnmatch import fnmatch
        
        for pattern in exclude_patterns:
            if fnmatch(file_path, pattern):
                return False
                
        for pattern in include_patterns:
            if fnmatch(file_path, pattern):
                return True
                
        return False
        
    def generate_consolidated_file(self):
        directory = self.dir_entry.get()
        output_file = self.output_entry.get()
        header = self.header_text.get("1.0", END)
        
        include_patterns = [p.strip() for p in self.include_entry.get().split(",")]
        exclude_patterns = [p.strip() for p in self.exclude_entry.get().split(",")]
        
        if not directory:
            self.message_queue.put({
                'type': 'error',
                'message': "Please select a project directory"
            })
            return
            
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(header + "\n\n")
                f.write("=" * 80 + "\n\n")
                
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, directory)
                        
                        if self.should_include_file(rel_path, include_patterns, exclude_patterns):
                            try:
                                with open(file_path, 'r', encoding='utf-8') as source_file:
                                    content = source_file.read()
                                    f.write(f"File: {rel_path}\n")
                                    f.write("=" * 80 + "\n")
                                    f.write(content)
                                    f.write("\n\n")
                            except Exception as e:
                                print(f"Error reading file {file_path}: {str(e)}")
                                
            self.message_queue.put({
                'type': 'info',
                'message': f"Generated consolidated code file: {output_file}"
            })
            
        except Exception as e:
            self.message_queue.put({
                'type': 'error',
                'message': f"Failed to generate file: {str(e)}"
            })
            
    def generate_with_progress(self):
        self.progress.pack(fill=X, padx=10, pady=(0, 10))
        self.progress.start()
        
        thread = threading.Thread(target=self.threaded_generate)
        thread.start()
        
    def threaded_generate(self):
        self.generate_consolidated_file()
        self.progress.stop()
        self.progress.pack_forget()

if __name__ == "__main__":
    root = ttk.Window()
    app = FuturisticCodeConsolidator(root)
    root.mainloop()
