
import customtkinter as ctk

def on_button_click():
    label.config(text="Button Clicked!")

# Initialize the main window with CustomTkinter
app = ctk.CTk()

# Set dark mode and custom purple accent color
ctk.set_appearance_mode("dark")  # Enable dark mode
ctk.set_default_color_theme("dark-blue")  # Set accent color to purple 

# Create a button
button = ctk.CTkButton(master=app, text="Click Me", command=on_button_click)
button.pack(pady=20)

# Create a label
label = ctk.CTkLabel(master=app, text="Hello, CustomTkinter!")
label.pack()

# Run the application
app.mainloop()

