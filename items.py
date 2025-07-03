import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from PIL import Image
from customtkinter import CTkImage
from database import get_all_items
import os
from add_item import AddItemWindow

# Colors 
COLOR_GREY_BEIGE = "#f5f5eb"  # Grey Beige - Primary Background
COLOR_ROYAL_BLUE = "#11225b"  # Royal Blue - Primary Actions
COLOR_SAPPHIRE = "#8094c2"    # Sapphire - Secondary Elements

# Main colors
COLOR_PRIMARY = COLOR_ROYAL_BLUE
COLOR_PRIMARY_HOVER = "#0d1a47"  # Darker Royal Blue
COLOR_SECONDARY = COLOR_SAPPHIRE
COLOR_SECONDARY_LIGHT = "#a0b3d9"  # Lighter Sapphire
COLOR_SECONDARY_DARK = "#6b7ba8"   # Darker Sapphire

# Background variations using Grey Beige
COLOR_MAIN_BG = COLOR_GREY_BEIGE
COLOR_SIDEBAR_BG = "#f0f0e6"      # Slightly darker Grey Beige
COLOR_SIDEBAR_ACTIVE = "#ebebd9"   # Active sidebar item
COLOR_CARD_BG = "#fafaff"          # Card backgrounds (very light grey-beige)

# Accent colors 
COLOR_ACCENT_SUCCESS = "#2d5a27"   # Dark green that works with your palette
COLOR_ACCENT_WARNING = "#8b6914"   # Golden brown
COLOR_ACCENT_ERROR = "#7a2e2e"     # Dark red
COLOR_ACCENT_INFO = COLOR_SAPPHIRE

# Neutral colors 
COLOR_WHITE = "#ffffff"
COLOR_GRAY_50 = COLOR_GREY_BEIGE
COLOR_GRAY_100 = "#ebebd9"
COLOR_GRAY_200 = "#d6d6c4"
COLOR_GRAY_300 = "#c2c2af"
COLOR_GRAY_600 = "#6b6b5a"
COLOR_GRAY_700 = "#565645"
COLOR_GRAY_800 = "#414130"
COLOR_GRAY_900 = COLOR_ROYAL_BLUE

# Text colors
COLOR_TEXT_PRIMARY = COLOR_ROYAL_BLUE
COLOR_TEXT_SECONDARY = COLOR_SAPPHIRE
COLOR_TEXT_MUTED = "#7a7a6b"

# Fonts
FONT_H1 = ("Segoe UI", 28, "bold")
FONT_H2 = ("Segoe UI", 20, "bold")
FONT_H3 = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 14)
FONT_SMALL = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 14, "bold")
FONT_CARD_VALUE = ("Segoe UI", 32, "bold")

def get_items_from_database():
    """Fetch items from database and format them for display"""
    try:
        items_data = get_all_items()
        formatted_items = []
        
        for item in items_data:
            # Database columns: ItemID, ItemName, Type, Quantity, Unit, StorageLocation, 
            # Brand, ExpirationDate, DateAdded, PurchasePrice, UpdatedBy, DateUpdated, 
            # SupplierID, SupplierName, ContactPerson, ContactNumber, Email
            
            formatted_item = {
                "item_no": f"{item[0]:04d}",  # ItemID formatted as 4-digit number
                "item_name": item[1] or "N/A",  # ItemName
                "type": item[2] or "N/A",  # Type
                "unit": item[4] or "N/A",  # Unit
                "storage_location": item[5] or "N/A",  # StorageLocation
                "category": item[2] or "N/A",  # Using Type as category
                "supplier": item[12] if item[12] else "N/A",  # SupplierName
                "description": f"Brand: {item[6] or 'N/A'}, Expiry: {item[7] or 'N/A'}" if item[6] or item[7] else "No additional details",
                "quantity": item[3] or 0,  # Quantity
                "brand": item[6],  # Brand
                "expiry_date": item[7],  # ExpirationDate
                "date_added": item[8],  # DateAdded
                "supplier_id": item[12],  # SupplierID
                "contact_person": item[13] if item[13] else "N/A",  # ContactPerson
                "contact_number": item[14] if item[14] else "N/A",  # ContactNumber
                "email": item[15] if item[15] else "N/A"  # Email
            }
            formatted_items.append(formatted_item)
        
        return formatted_items
    except Exception as e:
        print(f"Error fetching items from database: {e}")
        return []

class AnimatedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.original_color = self._fg_color
        
    def on_enter(self, event):
        self.configure(cursor="hand2")
        
    def on_leave(self, event):
        self.configure(cursor="")

class ModernSidebar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=280, fg_color=COLOR_SAPPHIRE, corner_radius=0, **kwargs)
        self.pack_propagate(False)
        self.active_button = None
        self.setup_ui()
        
    def setup_ui(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", pady=(30, 40))
        logo_frame.pack_propagate(False)
        logo_frame.grid_columnconfigure(1, weight=1)

        # Load and place logo image
        try:
            logo_image = Image.open("LOGO2.png")
            logo_ctk = CTkImage(light_image=logo_image, size=(60, 60))
            logo_icon = ctk.CTkLabel(logo_frame, image=logo_ctk, text="")
            logo_icon.grid(row=0, column=0, padx=(20, 0), sticky="w")
        except:
            # Fallback if logo image not found
            logo_icon = ctk.CTkLabel(logo_frame, text="📦", font=("Segoe UI", 40), text_color=COLOR_ROYAL_BLUE)
            logo_icon.grid(row=0, column=0, padx=(20, 0), sticky="w")

        # App name and subtitle next to logo
        text_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        text_frame.grid(row=0, column=1, sticky="w")

        logo_label = ctk.CTkLabel(text_frame, text="StockSmart", font=FONT_H1, text_color=COLOR_ROYAL_BLUE)
        logo_label.pack(anchor="w")

        # Navigation with modern design
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20)

        nav_buttons = [
            ("Dashboard", "🏠", False),
            ("Inventory", "📦", False),
            ("Items", "🏷️", True),  # This is now active
            ("History Logs", "📋", False)
        ]

        for name, icon, is_active in nav_buttons:
            btn = self.create_nav_button(nav_frame, name, icon, is_active)
            btn.pack(fill="x", pady=5)
            
        # User section at bottom
        user_frame = ctk.CTkFrame(self, fg_color=COLOR_SECONDARY_DARK, corner_radius=12, height=80)
        user_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        user_frame.pack_propagate(False)
        
        user_info = ctk.CTkLabel(user_frame, text="👤 Mingyu Kim\nOwner", 
                               font=FONT_SMALL, text_color=COLOR_WHITE, justify="left")
        user_info.pack(expand=True, padx=15)

    def create_nav_button(self, parent, name, icon, is_active=False):
        fg_color = COLOR_SECONDARY_DARK if is_active else "transparent"
        text_color = COLOR_WHITE if is_active else COLOR_ROYAL_BLUE
        hover_color = COLOR_SECONDARY_LIGHT if not is_active else COLOR_SECONDARY_DARK
        
        btn = ctk.CTkButton(parent, text=f"{icon}  {name}", font=FONT_BUTTON,
                           text_color=text_color, fg_color=fg_color,
                           hover_color=hover_color, corner_radius=10, height=50,
                           anchor="w", command=lambda n=name: self.set_active(n))
        
        if is_active:
            self.active_button = btn
            
        return btn
        
    def set_active(self, name):
        print(f"{name} clicked")

class ItemsPage(ctk.CTkFrame):
    def __init__(self, master, user_id=None, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        self.search_var = ctk.StringVar()
        self.filter_var = ctk.StringVar(value="All")
        self.active_category = "All"
        self.category_buttons = {}
        self.refresh_data()
        self.setup_ui()
    
    def refresh_data(self):
        """Refresh data from database"""
        self.filtered_data = get_items_from_database()
        if hasattr(self, 'table_scroll'):
            self.apply_filters()
        
    def setup_ui(self):
        self.configure(fg_color=COLOR_MAIN_BG, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.build_header()
        
        content_container = ctk.CTkFrame(self, corner_radius=16, fg_color=COLOR_CARD_BG,
                                         border_width=1, border_color=COLOR_GRAY_200)
        content_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_rowconfigure(1, weight=1)
        
        header_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(15, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Item Management",
            font=FONT_H2,
            text_color=COLOR_TEXT_PRIMARY
        )
        header_label.grid(row=0, column=0, sticky="w")
        
        today_str = "Today, " + datetime.now().strftime("%B %d, %Y")
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=today_str,
            font=FONT_BODY,
            text_color=COLOR_TEXT_MUTED
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Add Item button
        add_btn = AnimatedButton(
            header_frame,
            text="+ Add Item",
            font=FONT_BUTTON,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=8,
            height=40,
            width=120,
            command=self.add_item
        )
        add_btn.grid(row=0, column=1, rowspan=2, sticky="e", padx=(10, 0))
        
        # Refresh button
        refresh_btn = AnimatedButton(
            header_frame,
            text="🔄 Refresh",
            font=FONT_BUTTON,
            fg_color=COLOR_SECONDARY,
            hover_color=COLOR_SECONDARY_DARK,
            corner_radius=8,
            height=40,
            width=120,
            command=self.refresh_data
        )
        refresh_btn.grid(row=0, column=2, rowspan=2, sticky="e", padx=(10, 0))
        
        # Search and Filter Bar (Updated to match inventory page)
        self.create_search_filter_bar(content_container)
        
        # Category Filter Tabs
        self.create_category_tabs(content_container)
        
        # Items Table
        self.create_items_table(content_container)

    def build_header(self):
        """Build the header section with title"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(0, 0))
        header_frame.pack_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)

        # Title section
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, text="Items", 
                                 font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        title_label.grid(row=0, column=0, sticky="w", pady=(5, 0))
        
        subtitle = ctk.CTkLabel(title_frame, text="Manage your inventory items and categories", 
                              font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        subtitle.grid(row=1, column=0, sticky="w")

    def create_search_filter_bar(self, parent):
        """Create search bar"""
        filter_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filter_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=(20, 10))
        filter_frame.grid_columnconfigure(1, weight=1)
        
        # Search entry
        search_label = ctk.CTkLabel(filter_frame, text="Search:", font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        search_label.grid(row=0, column=2, padx=(0, 10), sticky="w")
        
        search_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.search_var,
            placeholder_text="Search items...",
            font=FONT_BODY,
            corner_radius=8,
            border_width=1,
            border_color=COLOR_GRAY_300,
            width=300
        )
        search_entry.grid(row=0, column=3, padx=(0, 10), sticky="ew")
        search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())
        
        # Search button
        search_btn = AnimatedButton(
            filter_frame,
            text="🔍",
            font=("Segoe UI", 16),
            fg_color=COLOR_SECONDARY,
            hover_color=COLOR_SECONDARY_DARK,
            corner_radius=8,
            width=40,
            height=32,
            command=lambda: self.apply_filters()
        )
        search_btn.grid(row=0, column=4, sticky="w")

    def create_category_tabs(self, parent):
        """Create category filter tabs with horizontal scrolling"""
        # Create a frame with a canvas and horizontal scrollbar
        tabs_outer_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tabs_outer_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=(10, 20))
        tabs_outer_frame.grid_columnconfigure(0, weight=1)

        canvas = ctk.CTkCanvas(tabs_outer_frame, height=50, bg="white", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="ew")
        h_scroll = ctk.CTkScrollbar(tabs_outer_frame, orientation="horizontal", command=canvas.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")
        canvas.configure(xscrollcommand=h_scroll.set)

        tabs_frame = ctk.CTkFrame(canvas, fg_color="transparent")
        canvas.create_window((0, 0), window=tabs_frame, anchor="nw")

        categories = ["All", "Fruits", "Vegetables", "Condiments & Sauces", "Staples", "Spices & Seasonings", "Dairy", "Meat"]
        self.active_category = "All"
        self.category_buttons = {}

        for i, category in enumerate(categories):
            is_active = category == "All"
            btn = AnimatedButton(
                tabs_frame,
                text=category,
                font=FONT_BODY,
                fg_color=COLOR_PRIMARY if is_active else "transparent",
                hover_color=COLOR_PRIMARY_HOVER if is_active else COLOR_SIDEBAR_ACTIVE,
                text_color=COLOR_WHITE if is_active else COLOR_TEXT_SECONDARY,
                corner_radius=8,
                height=35,
                border_width=0 if is_active else 1,
                border_color=COLOR_GRAY_300,
                anchor="center",
                width=150,
                command=lambda c=category: self.set_active_category(c)
            )
            btn.pack(side="left", padx=(0, 10), pady=0, anchor="center")
            self.category_buttons[category] = btn

        # Update scrollregion after adding widgets
        tabs_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def create_items_table(self, parent):
        """Create the items table with scrollable content"""
        # Table container
        table_container = ctk.CTkFrame(parent, fg_color="transparent")
        table_container.grid(row=3, column=0, sticky="nsew", padx=25, pady=(0, 25))
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame for table
        self.table_scroll = ctk.CTkScrollableFrame(table_container, fg_color="transparent", height=400)
        self.table_scroll.grid(row=0, column=0, sticky="nsew")
        self.table_scroll.grid_columnconfigure(0, weight=1)
        
        # Table header
        self.create_table_header()
        
        # Table rows
        self.create_table_rows()

    def create_table_header(self):
        """Create table header with uniform columns"""
        header_frame = ctk.CTkFrame(self.table_scroll, fg_color=COLOR_SECONDARY, corner_radius=8, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header_frame.grid_propagate(False)
        # Set column configurations (removed image column)
        for i in range(5):
            header_frame.grid_columnconfigure(i, weight=[1,2,1,1,2][i], uniform="col", minsize=[80,150,100,80,120][i])
        headers = ["Item No.", "Item Name", "Type", "Unit", "Storage Location"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(weight="bold", size=14),
                text_color=COLOR_WHITE
            )
            header_label.grid(row=0, column=i, padx=8, pady=12, sticky="nsew")

    def create_table_rows(self):
        """Create table rows based on filtered data"""
        # Clear existing rows
        for widget in self.table_scroll.winfo_children()[1:]:  # Skip header
            widget.destroy()
        
        for i, item in enumerate(self.filtered_data):
            self.create_table_row(item, i + 1)

    def create_table_row(self, item, row_index):
        """Create a single table row"""
        row_color = COLOR_WHITE if row_index % 2 == 0 else COLOR_GRAY_50
        row_frame = ctk.CTkFrame(self.table_scroll, fg_color=row_color, corner_radius=8, height=50)
        row_frame.grid(row=row_index, column=0, sticky="ew", pady=2)
        row_frame.grid_propagate(False)
        for i in range(5):
            row_frame.grid_columnconfigure(i, weight=[1,2,1,1,2][i], uniform="col", minsize=[80,150,100,80,120][i])
        data = [
            item["item_no"],
            item["item_name"],
            item["type"],
            item["unit"],
            item["storage_location"]
        ]
        for i, cell_data in enumerate(data):
            cell_label = ctk.CTkLabel(
                row_frame,
                text=cell_data,
                font=ctk.CTkFont(size=14),
                text_color=COLOR_TEXT_PRIMARY,
                anchor="center"
            )
            cell_label.grid(row=0, column=i, padx=8, pady=12, sticky="nsew")

    def set_active_category(self, category):
        """Set active category and update button styles"""
        # Reset all buttons
        for cat, btn in self.category_buttons.items():
            is_active = cat == category
            btn.configure(
                fg_color=COLOR_PRIMARY if is_active else "transparent",
                hover_color=COLOR_PRIMARY_HOVER if is_active else COLOR_SIDEBAR_ACTIVE,
                text_color=COLOR_WHITE if is_active else COLOR_TEXT_SECONDARY,
                border_width=0 if is_active else 1
            )
        
        self.active_category = category
        self.apply_filters()

    def apply_filters(self):
        """Apply search and filter to items data"""
        search_term = self.search_var.get().lower()
        
        self.filtered_data = []
        
        for item in get_items_from_database():
            # Apply category filter from tabs
            if self.active_category != "All":
                item_type = item["type"].lower()
                category = self.active_category.lower()
                
                # Map categories to item types
                if category == "condiments & sauces" and ("condiments" not in item_type and "sauces" not in item_type):
                    continue
                elif category == "fruits" and "fruits" not in item_type:
                    continue
                elif category == "vegetables" and "vegetables" not in item_type:
                    continue
                elif category == "staples" and "staples" not in item_type:
                    continue
                elif category == "spices & seasonings" and ("spices" not in item_type and "seasonings" not in item_type):
                    continue
                elif category == "dairy" and "dairy" not in item_type:
                    continue
                elif category == "meat" and "meat" not in item_type:
                    continue
            
            # Apply search filter
            if search_term and search_term not in item["item_name"].lower():
                continue
            
            self.filtered_data.append(item)
        
        # Recreate table rows
        self.create_table_rows()

    def add_item(self):
        def on_item_added():
            self.refresh_data()
        AddItemWindow(self, on_success=on_item_added, user_id=self.user_id)

class ItemsApp(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.title("StockSmart - Items Management")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=COLOR_MAIN_BG)

        # Main items page
        self.items_page = ItemsPage(self, user_id=self.user_id)
        self.items_page.pack(side="left", fill="both", expand=True)


# Test the items page with sidebar
if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    app = ItemsApp(user_id=1)
    app.mainloop()