

import os, time, threading, queue
import tkinter as tk
from tkinter import filedialog
from zipfile import ZipFile, BadZipFile

def unzip_file_threaded(zip_path, extract_path, status_queue, thread_finished_event):
    start_time = time.time()

    def _update_status(message, is_error=False):
        status_queue.put(("status", message, is_error))

    try:
        if not zip_path:
            _update_status("Error: No input file selected!", is_error=True)
            return	
        if not os.path.exists(zip_path):
            _update_status("Error: ZIP file not found!", is_error=True)
            return
        
        if not extract_path:
            _update_status("No output directory selected!", is_error=True)
            return   
        
        if not os.path.isdir(extract_path): 
            os.makedirs(extract_path, exist_ok=True) 
            _update_status(f"Output directory {extract_path} created.")
        
        _update_status("Unzipping in progress...")

        with ZipFile(zip_path, 'r') as zip_ref:
            if thread_finished_event.is_set():
                _update_status("Unzip operation cancelled.", is_error=True)
                return
            zip_ref.extractall(extract_path)
            _update_status("Unzipped successfully!")
       
    except BadZipFile:
        _update_status("Error: Bad ZIP file!", is_error=True)
    except FileNotFoundError:
        _update_status("Error: ZIP file not found!", is_error=True)
    except Exception as e:
        _update_status(f"Error: {str(e)}", is_error=True)
    
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        _update_status(f"Time taken: {elapsed_time:.3f} seconds")
        thread_finished_event.set()


class UnzipApp:
    def __init__(self, root): 
        self.root = root 
        root.title("My Unzip Tool. Version 0.9") 
        root.geometry("500x400") 
        root.resizable(False, False) 
        self.root.grid_columnconfigure(1, weight=1)

        # --- Instance Variables for Threading and Communication ---
        self.unzip_thread = None
        self.status_queue = queue.Queue()
        self.thread_finished_event = threading.Event()
       
        tk.Label(root, text="Zip File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.zip_input_pdf = tk.Entry(root, width=50)
        self.zip_input_pdf.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        tk.Button(root, text="Browse ...", command=self.browse_zip_file).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.unzip_output_pdf = tk.Entry(root, width=50)
        self.unzip_output_pdf.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        tk.Button(root, text="Browse ....", command=self.browse_output_folder).grid(row=1, column=2, padx=10, pady=5)

        self.unzip_button = tk.Button(root, text="Unzip File", command=self.start_unzip, 
                                      font=("Arial", 12, "bold"), bg="#C0C0C0", fg="#000000",
                                       activebackground="#A0A0A0", activeforeground="#00080F")
        self.unzip_button.grid(row=2, column=0, columnspan=3, pady=20, ipadx=10, ipady=10)

        # ---Stop BUtton----
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_unzip, 
                                     font=("Arial", 12, "bold"), bg="#C0C0C0", fg="#000000",
                                     activebackground="#A0A0A0", activeforeground="#00080F")
        self.stop_button.grid(row=4, column=0, columnspan=3, pady=20, ipadx=10, ipady=10)

        self.status_label = tk.Label(root, text="Ready", fg="green", font=("Arial", 10))
        self.status_label.grid(row=3, column=0, columnspan=3, pady=20)

        # add a flag to track if the final status is being displayed
        self._displaying_final_status = False
      
        self.root.after(20, self._process_queue)
  

    def browse_zip_file(self):
        """Open a file dialog to select a zip file."""
        file_name = filedialog.askopenfilename(
            title="Select a Zip File",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")] # This lets the user filter the file list in the dialog
        )
        if file_name:
            self.zip_input_pdf.delete(0, tk.END)
            self.zip_input_pdf.insert(0, file_name)
            self.update_status("Zip detected!", is_error=False)
    
    def browse_output_folder(self):
        """Open a file dialog to select an output folder."""
        folder_name = filedialog.askdirectory(title="Select an Output Folder")
        if folder_name:
            self.unzip_output_pdf.delete(0, tk.END)
            self.unzip_output_pdf.insert(0, folder_name)
            self.update_status("Output folder detected!", is_error=False)

    def update_status(self, message, is_error=False):
        """IMPORTANT: This method is now called ONLY from the main thread via _process_queue."""
        self.status_label.config(text=message, fg="red" if is_error else "green")

    def _process_queue(self):
        """Processes messages from the background thread's queue."""
        while True:
            try:
                item = self.status_queue.get_nowait()
                msg_type = item[0]

                if msg_type == "status":
                    _, message, is_error = item
                    self.update_status(message, is_error)

            except queue.Empty:
                break

        # Check if the unzip thread has finished
        if self.thread_finished_event.is_set() and self.unzip_thread is not None:
            # Re-enable buttons and clear thread reference
            self.unzip_button.config(state=tk.NORMAL)
            self.zip_input_pdf.config(state=tk.NORMAL)
            self.unzip_output_pdf.config(state=tk.NORMAL)
            self.unzip_thread = None
            self._displaying_final_status = True # Set flag for final status

        # Always re-schedule the next check
        self.root.after(20, self._process_queue)    
    
    def start_unzip(self):
        """Start the unzip operation in a separate thread."""
        zip_path = self.zip_input_pdf.get().strip()
        extract_path = self.unzip_output_pdf.get().strip()

        if not zip_path:
            self.update_status("Error: Please select a zip file.", is_error=True)
            return
        if not extract_path:
            self.update_status("Error: Please select an output folder.", is_error=True)
            return

        if self.unzip_thread and self.unzip_thread.is_alive():
            self.update_status("Unzip operation already in progress!", is_error=False)
            return     
        
        self.unzip_button.config(state=tk.DISABLED)
        self.zip_input_pdf.config(state=tk.DISABLED)
        self.unzip_output_pdf.config(state=tk.DISABLED)

        self.thread_finished_event.clear()

        self.unzip_thread = threading.Thread(               # Call the unzip function
            target=unzip_file_threaded, 
            args=(zip_path, extract_path, self.status_queue, self.thread_finished_event)
            )
        self.unzip_thread.daemon = True
        self.unzip_thread.start()   
    
    def stop_unzip(self):
        """Stop the unzip operation if it's running."""
        if self.unzip_thread and self.unzip_thread.is_alive():
            self.thread_finished_event.set()
            self.update_status("Stopping unzip...", is_error=False)
        else:
            self.update_status("No active unzip operation to stop.", is_error=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = UnzipApp(root)
    root.mainloop()