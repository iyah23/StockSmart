import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import os
from database import update_item, log_history
from datetime import datetime
try:
    from tkcalendar import Calendar
except ImportError:
    Calendar = None

class EditItemWindow(ctk.CTkToplevel):
    def __init__(self, master, item_data, on_save=None, user_id=None):
        super().__init__(master)
        self.title("Edit Item")
        self.geometry("800x600")
        self.resizable(False, False)
        self.configure(fg_color="#F9F5EB")
        self.on_save = on_save
        self.item_data = item_data
        self.item_id = int(item_data.get("item_no", 0))
        self.user_id = user_id
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        # Left frame
        left_frame = ctk.CTkFrame(master=self, fg_color="#F9F5EB")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.grid_columnconfigure(0, weight=1)
        # Right frame
        right_frame = ctk.CTkFrame(master=self, fg_color="#F9F5EB")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, minsize=60)
        # Title
        title = ctk.CTkLabel(
            left_frame,
            text="Edit Item",
            font=ctk.CTkFont(family="Instrument Sans", size=25, weight="bold"),
            text_color="#112250"
        )
        title.grid(row=0, column=0, sticky="w", padx=(10,0), pady=(5,10))
        # Item Name
        item_name_label = ctk.CTkLabel(left_frame, text="Item Name", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        item_name_label.grid(row=1, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.item_name_entry = ctk.CTkEntry(left_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black")
        self.item_name_entry.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.item_name_entry.insert(0, item_data.get("item_name", ""))
        # Type
        type_label = ctk.CTkLabel(left_frame, text="Type", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        type_label.grid(row=3, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.type_dropdown = ctk.CTkComboBox(left_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black", values=["Condiment & Sauces", "Dairy", "Meat", "Vegetables", "Fruits", "Staples", "Spices & Seasonings"])
        self.type_dropdown.grid(row=4, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.type_dropdown.set(item_data.get("type", "Condiment & Sauces"))

        # Minimum Quantity
        min_qty_label = ctk.CTkLabel(left_frame, text="Minimum Quantity", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        min_qty_label.grid(row=5, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.min_quantity_entry = ctk.CTkEntry(left_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black", placeholder_text="Enter minimum quantity")
        self.min_quantity_entry.grid(row=6, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.min_quantity_entry.insert(0, item_data.get("min_quantity", ""))

        # Quantity & Unit
        qty_unit_frame = ctk.CTkFrame(left_frame, fg_color="#F9F5EB")
        qty_unit_frame.grid(row=7, column=0, sticky="ew", padx=(10, 10), pady=(0, 8))
        qty_unit_frame.grid_columnconfigure(0, weight=1)
        qty_unit_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(qty_unit_frame, text="Quantity", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold")).grid(row=0, column=0, padx=(0, 5), pady=(5, 4), sticky="w")
        ctk.CTkLabel(qty_unit_frame, text="Unit", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold")).grid(row=0, column=1, padx=(5, 0), pady=(5, 4), sticky="w")
        self.quantity_entry = ctk.CTkEntry(qty_unit_frame, height=30, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black")
        self.quantity_entry.grid(row=1, column=0, padx=(0, 5), pady=(0, 0), sticky="ew")
        self.quantity_entry.insert(0, item_data.get("quantity", ""))
        self.unit_dropdown = ctk.CTkComboBox(qty_unit_frame, height=30, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black", values=["pack", "piece", "bottle"])
        self.unit_dropdown.grid(row=1, column=1, padx=(5, 0), pady=(0, 0), sticky="ew")
        self.unit_dropdown.set(item_data.get("unit", "pack"))
        # Storage Location
        storage_label = ctk.CTkLabel(left_frame, text="Storage Location", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        storage_label.grid(row=8, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.storage_dropdown = ctk.CTkComboBox(left_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black", values=["Pantry", "Refrigerator", "Freezer"])
        self.storage_dropdown.grid(row=9, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.storage_dropdown.set(item_data.get("storage_location", "Pantry"))
        # Brand
        brand_label = ctk.CTkLabel(left_frame, text="Brand", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        brand_label.grid(row=10, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.brand_entry = ctk.CTkEntry(left_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black")
        self.brand_entry.grid(row=11, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.brand_entry.insert(0, item_data.get("brand", ""))
        # Expiry Date
        expiry_label = ctk.CTkLabel(left_frame, text="Expiry Date", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        expiry_label.grid(row=12, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        expiry_frame = ctk.CTkFrame(left_frame, fg_color="#F9F5EB")
        expiry_frame.grid(row=13, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        expiry_frame.grid_columnconfigure(0, weight=1)
        self.expiry_entry = ctk.CTkEntry(expiry_frame, height=30, width=220, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black")
        self.expiry_entry.grid(row=0, column=0, sticky="ew")
        self.expiry_entry.insert(0, item_data.get("expiry_date", ""))
        calendar_btn = ctk.CTkButton(expiry_frame, text="📅", width=40, height=30, font=ctk.CTkFont(size=16), command=self.open_calendar)
        calendar_btn.grid(row=0, column=1, padx=(5,0))
        # BUTTONS inside left_frame
        button_frame = ctk.CTkFrame(left_frame, fg_color="#F9F5EB")
        button_frame.grid(row=14, column=0, pady=(10, 10))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", text_color="white", height=35, width=150, corner_radius=15, fg_color="#8094C2", hover_color="#6F84B3", font=ctk.CTkFont(family="Lexend", size=20, weight="bold"), command=self.destroy)
        cancel_btn.grid(row=0, column=0, padx=10)
        save_btn = ctk.CTkButton(button_frame, text="Save", text_color="white", height=35, width=150, corner_radius=15, fg_color="#112250", hover_color="#1A2E6B", font=ctk.CTkFont(family="Lexend", size=20, weight="bold"), command=self.save_item)
        save_btn.grid(row=0, column=1, padx=10)
        # Right frame supplier info
        supplier_label = ctk.CTkLabel(right_frame, text="Supplier", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        supplier_label.grid(row=1, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.supplier_entry = ctk.CTkEntry(right_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black")
        self.supplier_entry.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.supplier_entry.insert(0, item_data.get("supplier", ""))
        contact_person_label = ctk.CTkLabel(right_frame, text="Contact Person", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        contact_person_label.grid(row=3, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.contact_person_entry = ctk.CTkEntry(right_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black")
        self.contact_person_entry.grid(row=4, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.contact_person_entry.insert(0, item_data.get("contact_person", ""))
        contact_number_label = ctk.CTkLabel(right_frame, text="Contact Number", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        contact_number_label.grid(row=5, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.contact_number_entry = ctk.CTkEntry(right_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black")
        self.contact_number_entry.grid(row=6, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.contact_number_entry.insert(0, item_data.get("contact_number", ""))
        email_label = ctk.CTkLabel(right_frame, text="Email", text_color="black", font=ctk.CTkFont(family="Lexend", size=16, weight="bold"))
        email_label.grid(row=7, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.email_entry = ctk.CTkEntry(right_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black")
        self.email_entry.grid(row=8, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.email_entry.insert(0, item_data.get("email", ""))
        # Move Save and Cancel buttons to right_frame bottom
        button_frame = ctk.CTkFrame(right_frame, fg_color="#F9F5EB")
        button_frame.grid(row=9, column=0, pady=(30, 10), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        save_btn = ctk.CTkButton(
            button_frame, text="Save", text_color="white", height=40, width=150,
            corner_radius=15, fg_color="#112250", hover_color="#1A2E6B",
            font=ctk.CTkFont(family="Lexend", size=20, weight="bold"),
            command=self.save_item
        )
        save_btn.grid(row=0, column=0, padx=10, sticky="ew")
        cancel_btn = ctk.CTkButton(
            button_frame, text="Cancel", text_color="white", height=40, width=150,
            corner_radius=15, fg_color="#8094C2", hover_color="#6F84B3",
            font=ctk.CTkFont(family="Lexend", size=20, weight="bold"),
            command=self.destroy
        )
        cancel_btn.grid(row=0, column=1, padx=10, sticky="ew")
        self.lift()
        self.focus_force()
        self.transient(master)
        self.grab_set()
        self.attributes('-topmost', True)
        self.after(10, lambda: self.attributes('-topmost', False))

    def save_item(self):
        item_id = self.item_id
        # Old values
        old = self.item_data
        # New values
        new = {
            "item_name": self.item_name_entry.get(),
            "type": self.type_dropdown.get(),
            "min_quantity": self.min_quantity_entry.get(),
            "quantity": self.quantity_entry.get(),
            "unit": self.unit_dropdown.get(),
            "storage_location": self.storage_dropdown.get(),
            "brand": self.brand_entry.get(),
            "expiry_date": self.expiry_entry.get(),
            "supplier": self.supplier_entry.get(),
            "contact_person": self.contact_person_entry.get(),
            "contact_number": self.contact_number_entry.get(),
            "email": self.email_entry.get(),
        }

        # Validate and convert quantities to integers
        try:
            if new["quantity"]:
                new["quantity"] = int(new["quantity"])
            else:
                messagebox.showerror("Validation Error", "Quantity is required!", parent=self)
                return
        except ValueError:
            messagebox.showerror("Validation Error", "Quantity must be a valid whole number!", parent=self)
            return

        try:
            if new["min_quantity"]:
                new["min_quantity"] = int(new["min_quantity"])
            else:
                new["min_quantity"] = None
        except ValueError:
            messagebox.showerror("Validation Error", "Minimum quantity must be a valid whole number!", parent=self)
            return

        # Update in database
        update_item(
            item_id,
            ItemName=new["item_name"],
            Type=new["type"],
            Quantity=new["quantity"],
            Unit=new["unit"],
            StorageLocation=new["storage_location"],
            Brand=new["brand"],
            ExpirationDate=new["expiry_date"],
            LastUpdated=datetime.now().strftime("%Y-%m-%d"),
            MinimumQuantity=new["min_quantity"]
        )

        # Log changes for each field
        for field, new_value in new.items():
            old_value = old.get(field, "")
            if str(new_value) != str(old_value):
                log_history(
                    item_id=item_id,
                    user_id=self.user_id,
                    action=f"Updated {field.replace('_', ' ').title()}",
                    details=f"Changed {field.replace('_', ' ')} from '{old_value}' to '{new_value}'"
                )

        messagebox.showinfo("Success", "Item updated successfully!")
        if self.on_save:
            self.on_save()
        self.destroy()

    def open_calendar(self):
        if Calendar is None:
            messagebox.showerror("Calendar Not Available", "tkcalendar is not installed.")
            return
        top = Toplevel(self)
        top.title("Select Date")
        cal = Calendar(top, selectmode='day', date_pattern='mm/dd/yy')
        cal.pack(padx=10, pady=10)
        def set_date():
            self.expiry_entry.delete(0, 'end')
            self.expiry_entry.insert(0, cal.get_date())
            top.destroy()
        select_btn = ctk.CTkButton(top, text="Select", command=set_date)
        select_btn.pack(pady=(0,10))