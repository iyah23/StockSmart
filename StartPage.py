import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
import os
import subprocess
import sys

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1200x800")
app.resizable(True, True)
app.title("Start Page")

for col in (0, 1):
    app.grid_columnconfigure(col, weight=1, uniform="half")
app.grid_rowconfigure(0, weight=1)

left_frame = ctk.CTkFrame(app, fg_color="#f9f5eb", corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew")

right_frame = ctk.CTkFrame(app, fg_color="#8094c2", corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.grid_propagate(False)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

right_inner_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
right_inner_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=(30, 0))
right_inner_frame.grid_columnconfigure(0, weight=1)

image_path = os.path.join(os.path.dirname(__file__), "LOGO.png")
light_image = Image.open(image_path)
my_image = CTkImage(light_image=light_image, size=(200, 200))

image_label = ctk.CTkLabel(right_inner_frame, image=my_image, text="")
image_label.grid(row=0, column=0, pady=(15, 0), padx=(50, 0), sticky="ew")

title_label = ctk.CTkLabel(
    right_inner_frame,
    text="Welcome to\nStockSmart!",
    font=ctk.CTkFont(family="Instrument Sans", size=60, weight="bold"),
    text_color="#0f1e46",
    justify="center"
)
title_label.grid(row=1, column=0, pady=(0, 15), padx=(50, 0), sticky="ew")

sub_label = ctk.CTkLabel(
    right_inner_frame,
    text="Please select your role to enter the system",
    font=ctk.CTkFont(family="Instrument Sans", size=20),
    text_color="black"
)
sub_label.grid(row=2, column=0, pady=(10, 20), padx=(50, 0), sticky="ew")

selected_role_label = ctk.CTkLabel(
    right_inner_frame,
    text="",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    text_color="#0f1e46"
)
selected_role_label.grid(row=5, column=0, pady=(10, 0), sticky="ew")

def on_role_selected(role):
    selected_role_label.configure(text=f"You selected: {role}")
    # Launch LoginPage.py and pass the role as an argument
    subprocess.Popen([sys.executable, "StockSmart/LoginPage.py", role])
    app.after(100, app.destroy)

admin_button = ctk.CTkButton(
    right_inner_frame,
    text="Admin",
    width=200,
    height=60,
    corner_radius=10,
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    fg_color="white",
    text_color="black",
    hover_color="#f0f0f0",
    command=lambda: on_role_selected("Admin")
)
admin_button.grid(row=3, column=0, pady=(15, 15), padx=(0, 0), sticky="n")

employee_button = ctk.CTkButton(
    right_inner_frame,
    text="Employee",
    width=200,
    height=60,
    corner_radius=10,
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    fg_color="white",
    text_color="black",
    hover_color="#f0f0f0",
    command=lambda: on_role_selected("Employee")
)
employee_button.grid(row=4, column=0, pady=(15, 20), padx=(0, 0), sticky="n")

app.mainloop()