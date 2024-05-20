import tkinter as tk
from tkinter import font, ttk, messagebox
from PIL import Image, ImageTk
from treatments import TreatmentManager

class TreatmentApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("Alternative Treatment Service")
        self.root.geometry("1920x1080")

        # Load and display background image
        self.background_img = Image.open("images/background.jpg")
        self.background_img = self.background_img.resize((1920, 1080))  # Resize the image to fit window
        self.background_img = ImageTk.PhotoImage(self.background_img)
        self.background_canvas = tk.Canvas(root, width=1920, height=1080)
        self.background_canvas.create_image(0, 0, anchor=tk.NW, image=self.background_img, tags="bg")
        self.background_canvas.pack()

        self.create_widgets()

    def create_widgets(self):

        # Dropdown for diseases
        self.disease_label = tk.Label(self.root, text="Select Disease:", font=("Helvetica", 14), bg='white')
        self.disease_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.disease_var = tk.StringVar()
        self.disease_dropdown = ttk.Combobox(self.root, textvariable=self.disease_var, font=("Helvetica", 14))
        self.disease_dropdown.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        self.disease_dropdown['values'] = [disease.name for disease in self.manager.list_diseases()]
        self.disease_dropdown.bind("<<ComboboxSelected>>", self.load_treatments)

        # Using a larger font for the listbox
        self.custom_font = font.Font(family="Helvetica", size=14)
        self.listbox = tk.Listbox(self.root, width=50, height=10, font=self.custom_font)
        self.listbox.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.view_button = tk.Button(self.root, text="View Details", command=self.view_treatment, font=self.custom_font)
        self.view_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def load_treatments(self, event=None):
        self.listbox.delete(0, tk.END)
        disease_name = self.disease_var.get()
        disease = self.manager.find_disease(disease_name)
        if disease:
            for treatment in disease.treatments:
                self.listbox.insert(tk.END, f"{treatment.name} ({treatment.category})")

    def view_treatment(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            disease_name = self.disease_var.get()
            disease = self.manager.find_disease(disease_name)
            if disease:
                treatment = disease.treatments[selected_index[0]]
                self.show_treatment_details(treatment)
        else:
            messagebox.showwarning("Warning", "Please select a treatment to view.")

    def show_treatment_details(self, treatment):
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Details of {treatment.name}")
        details_window.geometry("1920x1080")

        details_frame = tk.Frame(details_window, width=1920, height=1080, bg='white')
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Add an image to the top of the details window
        try:
            image_path = f"images/{treatment.name.lower().replace(' ', '_')}.jpg"
            treatment_img = Image.open(image_path)
            treatment_img = treatment_img.resize((600, 400))  # Resize the image to fit window
            treatment_img = ImageTk.PhotoImage(treatment_img)
            img_label = tk.Label(details_frame, image=treatment_img, bg='white')
            img_label.image = treatment_img
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Image for {treatment.name} not found: {e}")

        # Add detailed description to the frame
        details_text = (
            f"Name: {treatment.name}\n\n"
            f"Description: {treatment.description}\n\n"
            f"Category: {treatment.category}\n\n"
            f"Where to get it: Available at most health stores or online"
        )
        details_label = tk.Label(details_frame, text=details_text, font=("Helvetica", 14), justify=tk.LEFT, bg='white')
        details_label.pack(pady=10, padx=10, anchor='w')

if __name__ == "__main__":
    manager = TreatmentManager('data/treatments.json')
    root = tk.Tk()
    app = TreatmentApp(root, manager)
    root.mainloop()
