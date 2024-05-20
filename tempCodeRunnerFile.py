# Adding a logo image
        self.logo = ImageTk.PhotoImage(Image.open("images/logo.png"))
        self.logo_label = tk.Label(self.root, image=self.logo, bg='white')
        self.logo_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)