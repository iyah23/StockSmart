import customtkinter as ctk
from PIL import Image
import os

app = ctk.CTk()
app.geometry("800x600")
app.title("View Item")
app.resizable(False, False)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app.configure(fg_color="#F9F5EB")
app.grid_columnconfigure(0, weight=2)
app.grid_columnconfigure(1, weight=3)
app.grid_rowconfigure(0, weight=1)

# Left Frame
left_frame = ctk.CTkFrame(master=app, fg_color="#F9F5EB")
left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
left_frame.grid_columnconfigure(0, weight=1)

# Right Frame
right_frame = ctk.CTkFrame(master=app, fg_color="#F9F5EB")
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(0, minsize=60)  # Adjust minsize as needed for more space

# Title
title_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
title_frame.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(5, 10))
title_frame.grid_columnconfigure(1, weight=1)  # make title expand if needed

# Load the arrow icon
arrow_path = os.path.join(os.path.dirname(__file__), "arrow-circle-left.png")
arrow_icon = ctk.CTkImage(light_image=Image.open(arrow_path), size=(30, 30))

back_btn = ctk.CTkButton(
    title_frame,
    image=arrow_icon,
    text="",
    width=36,
    height=36,
    fg_color="transparent",
    hover_color="#e0e0e0",
    command=app.destroy
)
back_btn.grid(row=0, column=0, padx=(0, 5))

# Title Label
title = ctk.CTkLabel(
    title_frame,
    text="View Item",
    font=ctk.CTkFont("Instrument Sans", 25, weight="bold"),
    text_color="#112250"
)
title.grid(row=0, column=1, sticky="w")


# Function for read-only entries
def create_readonly_entry(master, row, label_text, value):
    label = ctk.CTkLabel(master, text=label_text, text_color="black",
                         font=ctk.CTkFont("Lexend", 16, weight="bold"))
    label.grid(row=row, column=0, padx=(10, 0), pady=(5, 4), sticky="w")

    entry = ctk.CTkEntry(master, height=30, width=280, corner_radius=8,
                         fg_color="#F9F5EB", font=ctk.CTkFont("Lexend", 16),
                         border_width=2, border_color="black")
    entry.grid(row=row + 1, column=0, sticky="ew", pady=(0, 8), padx=(10, 0))
    entry.insert(0, value)
    entry.configure(state="readonly")  
    return entry

# Item Details
create_readonly_entry(left_frame, 1, "Item Name", "Vinegar")

type_label = ctk.CTkLabel(left_frame, text="Type", text_color="black",
                          font=ctk.CTkFont("Lexend", 16, weight="bold"))
type_label.grid(row=3, column=0, padx=(10, 0), pady=(5, 4), sticky="w")
type_entry = ctk.CTkEntry(left_frame, height=30, width=280, corner_radius=8,
                          fg_color="#F9F5EB", font=ctk.CTkFont("Lexend", 16),
                          border_width=2, border_color="black")
type_entry.grid(row=4, column=0, sticky="ew", pady=(0, 8), padx=(10, 0))
type_entry.insert(0, "Condiments")
type_entry.configure(state="readonly")  

# Quantity and Unit
qty_unit_frame = ctk.CTkFrame(left_frame, fg_color="#F9F5EB")
qty_unit_frame.grid(row=5, column=0, sticky="ew", padx=(10, 10), pady=(0, 8))
qty_unit_frame.grid_columnconfigure(0, weight=1)
qty_unit_frame.grid_columnconfigure(1, weight=1)

q_label = ctk.CTkLabel(qty_unit_frame, text="Quantity", text_color="black",
                       font=ctk.CTkFont("Lexend", 16, weight="bold"))
q_label.grid(row=0, column=0, padx=(0, 5), pady=(5, 4), sticky="w")

u_label = ctk.CTkLabel(qty_unit_frame, text="Unit", text_color="black",
                       font=ctk.CTkFont("Lexend", 16, weight="bold"))
u_label.grid(row=0, column=1, padx=(5, 0), pady=(5, 4), sticky="w")

q_entry = ctk.CTkEntry(qty_unit_frame, height=30, corner_radius=8,
                       fg_color="#F9F5EB", font=ctk.CTkFont("Lexend", 16),
                       border_width=2, border_color="black")
q_entry.grid(row=1, column=0, padx=(0, 5), sticky="ew")
q_entry.insert(0, "20")
q_entry.configure(state="readonly")  

u_entry = ctk.CTkEntry(qty_unit_frame, height=30, corner_radius=8,
                       fg_color="#F9F5EB", font=ctk.CTkFont("Lexend", 16),
                       border_width=2, border_color="black")
u_entry.grid(row=1, column=1, padx=(5, 0), sticky="ew")
u_entry.insert(0, "pack")
u_entry.configure(state="readonly")  

create_readonly_entry(left_frame, 7, "Storage Location", "Pantry")
create_readonly_entry(left_frame, 9, "Brand", "Datu Puti")
create_readonly_entry(left_frame, 11, "Expiry Date", "May 25, 2025")

# Right Frame (Supplier Info Only)
create_readonly_entry(right_frame, 1, "Supplier", "NutriAsia")
create_readonly_entry(right_frame, 3, "Contact Person", "Kim Mingyu")
create_readonly_entry(right_frame, 5, "Contact Number", "09230492304")
create_readonly_entry(right_frame, 7, "Email", "kimmingyu@gmail.com")

app.mainloop()
