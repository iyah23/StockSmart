import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import shutil
import re
from datetime import datetime
from database import add_supplier, get_supplier_by_info, add_item, log_history
from tkcalendar import Calendar
import tkinter as tk


class AddItemWindow(ctk.CTkToplevel):
    def __init__(self, master, on_success=None, user_id=None):
        super().__init__(master)
        self.title("Add Item")
        self.geometry("800x600")
        self.resizable(False, False)
        self.on_success = on_success
        self.user_id = user_id
        # Set background color of the window itself
        self.configure(fg_color="#F9F5EB")
        # Make the window modal and always on top of the parent
        self.transient(master)
        self.grab_set()
        self.focus_force()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.build_form()

    def build_form(self):
        # Left frame
        left_frame = ctk.CTkFrame(master=self, fg_color="#F9F5EB")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        left_frame.grid_columnconfigure(0, weight=1)

        # Right frame
        right_frame = ctk.CTkFrame(master=self, fg_color="#F9F5EB")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 30), pady=0)
        right_frame.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            left_frame,
            text="Add Item",
            font=ctk.CTkFont(family="Instrument Sans", size=25, weight="bold"),
            text_color="#112250"
        ).grid(row=0, column=0, sticky="w", padx=(10,0), pady=(5,10))

        # Item Name
        ctk.CTkLabel(left_frame, text="Item Name", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=1, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.item_name_entry = ctk.CTkEntry(left_frame, height=30, width=280, corner_radius=8,
                                            fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                            border_width=2, border_color="black")
        self.item_name_entry.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=(10,0))

        # Type
        ctk.CTkLabel(left_frame, text="Type", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=3, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.type_dropdown = ctk.CTkComboBox(
            left_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB",
            font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black",
            values=["Condiments & Sauces", "Dairy", "Meat", "Vegetables", "Fruits", "Staples", "Spices & Seasonings"]
        )
        self.type_dropdown.grid(row=4, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.type_dropdown.set("")

        # Minimum Quantity
        ctk.CTkLabel(left_frame, text="Minimum Quantity", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=5, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.min_quantity_entry = ctk.CTkEntry(left_frame, height=30, width=280, corner_radius=8,
                                               fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                               border_width=2, border_color="black")
        self.min_quantity_entry.grid(row=6, column=0, sticky="ew", pady=(0, 8), padx=(10,0))

        # Quantity & Unit
        qty_unit_frame = ctk.CTkFrame(left_frame, fg_color="#F9F5EB")
        qty_unit_frame.grid(row=7, column=0, sticky="ew", padx=(10, 10), pady=(0, 8))
        qty_unit_frame.grid_columnconfigure(0, weight=1)
        qty_unit_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(qty_unit_frame, text="Quantity", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=0, column=0, padx=(0, 5), pady=(5, 4), sticky="w")
        ctk.CTkLabel(qty_unit_frame, text="Unit", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=0, column=1, padx=(5, 0), pady=(5, 4), sticky="w")
        self.quantity_entry = ctk.CTkEntry(qty_unit_frame, height=30, corner_radius=8,
                                           fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                           border_width=2, border_color="black")
        self.quantity_entry.grid(row=1, column=0, padx=(0, 5), pady=(0, 0), sticky="ew")
        self.unit_dropdown = ctk.CTkComboBox(
            qty_unit_frame, height=30, corner_radius=8, fg_color="#F9F5EB",
            font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black",
            values=["pack", "piece", "bottle"]
        )
        self.unit_dropdown.grid(row=1, column=1, padx=(5, 0), pady=(0, 0), sticky="ew")
        self.unit_dropdown.set("")

        # Storage Location
        ctk.CTkLabel(left_frame, text="Storage Location", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=9, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.storage_dropdown = ctk.CTkComboBox(
            left_frame, height=30, width=280, corner_radius=8, fg_color="#F9F5EB",
            font=ctk.CTkFont(family="Lexend", size=16), border_width=2, border_color="black",
            values=["Pantry", "Refrigerator", "Freezer"]
        )
        self.storage_dropdown.grid(row=10, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.storage_dropdown.set("")

        # Brand
        ctk.CTkLabel(left_frame, text="Brand", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=11, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.brand_entry = ctk.CTkEntry(left_frame, height=30, width=280, corner_radius=8,
                                        fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                        border_width=2, border_color="black")
        self.brand_entry.grid(row=12, column=0, sticky="ew", pady=(0, 8), padx=(10,0))

        # Expiry Date
        ctk.CTkLabel(left_frame, text="Expiry Date (MM/DD/YY)", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=13, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.expiry_entry = ctk.CTkEntry(left_frame, height=30, width=280, corner_radius=8,
                                         fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                         border_width=2, border_color="black", placeholder_text="MM/DD/YY")
        self.expiry_entry.grid(row=14, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        self.expiry_entry.insert(0, "")
        calendar_btn = ctk.CTkButton(
            left_frame, text="📅", text_color="white", height=30, width=40, corner_radius=8,
            fg_color="#112250", hover_color="#1A2E6B", font=ctk.CTkFont(family="Lexend", size=14),
            command=self.pick_date
        )
        calendar_btn.grid(row=14, column=1, pady=(0, 8), padx=(5, 10), sticky="w")

        # Right frame: Supplier info
        ctk.CTkLabel(right_frame, text="Supplier", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=0, column=0, padx=(10,0), pady=(60, 4), sticky="w")
        self.supplier_entry = ctk.CTkEntry(right_frame, height=30, width=280, corner_radius=8,
                                           fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                           border_width=2, border_color="black")
        self.supplier_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        ctk.CTkLabel(right_frame, text="Contact Person", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=2, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.contact_person_entry = ctk.CTkEntry(right_frame, height=30, width=280, corner_radius=8,
                                                 fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                                 border_width=2, border_color="black")
        self.contact_person_entry.grid(row=3, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        ctk.CTkLabel(right_frame, text="Contact Number", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=4, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.contact_number_entry = ctk.CTkEntry(right_frame, height=30, width=280, corner_radius=8,
                                                 fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                                 border_width=2, border_color="black",
                                                 placeholder_text="11 digits (e.g., 09123456789)")
        self.contact_number_entry.grid(row=5, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
        ctk.CTkLabel(right_frame, text="Email", text_color="black",
                     font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
        ).grid(row=6, column=0, padx=(10,0), pady=(5, 4), sticky="w")
        self.email_entry = ctk.CTkEntry(right_frame, height=30, width=280, corner_radius=8,
                                        fg_color="#F9F5EB", font=ctk.CTkFont(family="Lexend", size=16),
                                        border_width=2, border_color="black")
        self.email_entry.grid(row=7, column=0, sticky="ew", pady=(0, 8), padx=(10,0))

        # BUTTONS inside right_frame (move to very bottom)
        button_frame = ctk.CTkFrame(right_frame, fg_color="#F9F5EB")
        button_frame.grid(row=16, column=0, pady=(30, 10), sticky="ew")
        save_btn = ctk.CTkButton(
            button_frame, text="Add Item", text_color="white", height=40, width=150,
            corner_radius=15, fg_color="#112250", hover_color="#1A2E6B",
            font=ctk.CTkFont(family="Lexend", size=20, weight="bold"),
            command=self.validate_and_add_item
        )
        save_btn.grid(row=0, column=0, sticky="ew", padx=10)

    def pick_date(self):
        self.grab_release()
        top = tk.Toplevel(self)  
        top.title("Select Expiry Date")
        cal = Calendar(top, selectmode='day', date_pattern='mm/dd/yy', font=("Arial", 16),
                       background='white', foreground='black')
        cal.pack(padx=20, pady=20, ipadx=20, ipady=20, expand=True, fill='both')
        def on_select():
            self.expiry_entry.delete(0, 'end')
            self.expiry_entry.insert(0, cal.get_date())
            top.destroy()
        select_btn = ctk.CTkButton(top, text="Select", command=on_select, height=40, width=120)
        select_btn.pack(pady=(0,20))
        top.geometry("400x400")
        self.wait_window(top)
        self.grab_set()

    def validate_and_add_item(self):
        item_name = self.item_name_entry.get().strip()
        item_type = self.type_dropdown.get()
        min_quantity=self.min_quantity_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        unit = self.unit_dropdown.get()
        storage = self.storage_dropdown.get()
        brand = self.brand_entry.get().strip()
        expiry = self.expiry_entry.get().strip()
        supplier = self.supplier_entry.get().strip()
        contact_person = self.contact_person_entry.get().strip()
        contact_number = self.contact_number_entry.get().strip()
        email = self.email_entry.get().strip()

        # Basic validation
        if not item_name:
            messagebox.showerror("Validation Error", "Item Name is required!", parent=self)
            return
        if not item_type:
            messagebox.showerror("Validation Error", "Type is required!", parent=self)
            return
        if not quantity:
            messagebox.showerror("Validation Error", "Quantity is required!", parent=self)
            return
        try:
            int(quantity)
        except ValueError:
            messagebox.showerror("Validation Error", "Quantity must be a valid whole number!", parent=self)
            return
        if not unit:
            messagebox.showerror("Validation Error", "Unit is required!", parent=self)
            return
        if not storage:
            messagebox.showerror("Validation Error", "Storage Location is required!", parent=self)
            return
        if expiry:
            if not re.match(r'^\d{2}/\d{2}/\d{2}$', expiry):
                messagebox.showerror("Validation Error", "Expiry Date must be in MM/DD/YY format!", parent=self)
                return
            try:
                datetime.strptime(expiry, '%m/%d/%y')
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid expiry date! Please use MM/DD/YY format.", parent=self)
                return
        if contact_number:
            if not re.match(r'^\d{11}$', contact_number):
                messagebox.showerror("Validation Error", "Contact Number must be exactly 11 digits!", parent=self)
                return

        try:
            supplier_id = None
            if supplier or contact_person or contact_number or email:
                supplier_id = get_supplier_by_info(supplier, contact_person, contact_number, email)
                if not supplier_id:
                    supplier_id = add_supplier(supplier, contact_person, contact_number, email)
                    if not supplier_id:
                        messagebox.showerror("Database Error", "Failed to add supplier information!", parent=self)
                        return

            item_id = add_item(
                item_name=item_name,
                item_type=item_type,
                quantity=int(quantity),
                unit=unit,
                storage_location=storage,
                brand=brand if brand else None,
                expiry_date=expiry if expiry else None,
                supplier_id=supplier_id,
                min_quantity=int(min_quantity) if min_quantity else None
            )
            if item_id:
                messagebox.showinfo("Success", f"Item '{item_name}' has been added successfully!", parent=self)
                if self.on_success:
                    self.on_success()
                self.destroy()
                log_history(
                    item_id=item_id,
                    user_id=self.user_id,
                    action="Added Item",
                    details=f"Added {quantity} {unit} of {item_name}"
                )
            else:
                messagebox.showerror("Database Error", "Failed to add item to database!", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self)

if __name__ == "__main__":
    app = ctk.CTk()
    AddItemWindow(app)
    app.mainloop()