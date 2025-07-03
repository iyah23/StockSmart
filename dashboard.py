import customtkinter as ctk
from tkinter import PhotoImage
import json
import os
from tkcalendar import Calendar
import threading
import time
from tkinter import filedialog
from PIL import Image, ImageTk
from customtkinter import CTkImage
import shutil
from inventoryy import InventoryPage
from items import ItemsPage
from history_log import HistoryLogsFrame
import sys
import subprocess
from datetime import datetime
from database import get_first_name, get_full_name, count_items, count_good_stock_items, count_out_of_stock_items, count_low_stock_items, get_top_consumed_items, get_user_details, update_user_profile, get_all_items, get_near_expiry_items

# ---------- Global Configuration ---------- #
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Enhanced Fonts with better hierarchy
FONT_H1 = ("Segoe UI", 28, "bold")
FONT_H2 = ("Segoe UI", 20, "bold")
FONT_H3 = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 14)
FONT_SMALL = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 14, "bold")
FONT_CARD_VALUE = ("Segoe UI", 32, "bold")

# Updated Color Scheme - Based on your provided palette
COLOR_GREY_BEIGE = "#f5f5eb"  # Grey Beige - Primary Background
COLOR_ROYAL_BLUE = "#11225b"  # Royal Blue - Primary Actions
COLOR_SAPPHIRE = "#8094c2"    # Sapphire - Secondary Elements

# Enhanced palette built around your main colors
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

# Accent colors that complement your main theme
COLOR_ACCENT_SUCCESS = "#2d5a27"   # Dark green that works with your palette
COLOR_ACCENT_WARNING = "#8b6914"   # Golden brown
COLOR_ACCENT_ERROR = "#7a2e2e"     # Dark red
COLOR_ACCENT_INFO = COLOR_SAPPHIRE

# Neutral colors derived from your palette
COLOR_WHITE = "#ffffff"
COLOR_GRAY_50 = COLOR_GREY_BEIGE
COLOR_GRAY_100 = "#ebebd9"
COLOR_GRAY_200 = "#d6d6c4"
COLOR_GRAY_300 = "#c2c2af"
COLOR_GRAY_600 = "#6b6b5a"
COLOR_GRAY_700 = "#565645"
COLOR_GRAY_800 = "#414130"
COLOR_GRAY_900 = COLOR_ROYAL_BLUE

# Text colors that work well with your palette
COLOR_TEXT_PRIMARY = COLOR_ROYAL_BLUE
COLOR_TEXT_SECONDARY = COLOR_SAPPHIRE
COLOR_TEXT_MUTED = "#7a7a6b"

# Shadow effects (simulated with frames)
SHADOW_COLOR = "#00000010"

# This class defines a button with a hover effect that changes the cursor to a hand.
class AnimatedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.original_color = self._fg_color
        
    def on_enter(self, event):
        self.configure(cursor="hand2")
        # Subtle hover animation
        
    def on_leave(self, event):
        self.configure(cursor="")

# This is a placeholder class for creating frames that simulate shadow effects.
class ShadowFrame(ctk.CTkFrame):
    """Custom frame with shadow effect simulation"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

# This class creates a styled dashboard card that shows stats like "Total Products."
# It includes animation for counting up values and supports showing trends (up/down/stable).
class EnhancedCard(ctk.CTkFrame):
    def __init__(self, parent, bg_color, icon_text, value, label_text):
        super().__init__(parent, corner_radius=16, fg_color=COLOR_CARD_BG, border_width=1, border_color=COLOR_GRAY_200)
        
        # Hover effect
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        # Main container for centered content
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Icon with colored background
        icon_frame = ctk.CTkFrame(main_container, fg_color=bg_color, corner_radius=12, width=60, height=60)
        icon_frame.pack(pady=(0, 15))
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text=icon_text, font=("Segoe UI", 24), text_color=COLOR_WHITE)
        icon_label.pack(expand=True)
        
        # Value with animation placeholder
        self.value_label = ctk.CTkLabel(main_container, text="0", font=FONT_CARD_VALUE, text_color=COLOR_TEXT_PRIMARY)
        self.value_label.pack(pady=(0, 8))
        
        # Label
        label = ctk.CTkLabel(main_container, text=label_text, font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        label.pack()
        
        # Animate the value
        self.animate_value(value)
        
    def animate_value(self, target_value):
        """Animate the counter from 0 to target value"""
        def animate():
            current = 0
            target = int(target_value.replace(',', ''))
            step = max(1, target // 30)  # 30 frames for smooth animation
            
            while current < target:
                current = min(current + step, target)
                formatted_value = f"{current:,}" if current >= 1000 else str(current)
                self.value_label.configure(text=formatted_value)
                time.sleep(0.03)
        
        threading.Thread(target=animate, daemon=True).start()
        
    def on_enter(self, event):
        self.configure(border_width=2, border_color=COLOR_PRIMARY)
        
    def on_leave(self, event):
        self.configure(border_width=1, border_color=COLOR_GRAY_200)

# This pop-up window displays the user's profile information.
# It supports editing profile fields, uploading a profile picture, and saving changes.
class UserProfilePopup(ctk.CTkToplevel):
    def __init__(self, master, user_email=None, **kwargs):
        super().__init__(master, **kwargs)
        self.edit_mode = False
        self.master = master
        self.user_email = user_email
        self.setup_window()
        self.setup_ui()
        
        # Center the popup on the parent window
        self.center_on_parent()
        
        # Make the popup modal
        self.transient(master)
        self.grab_set()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.title("User Profile")
        self.geometry("500x580")  # Start with view mode height
        self.resizable(False, False)
        self.configure(fg_color=COLOR_MAIN_BG)
        
        # Remove window decorations for a more modern look (optional)
        # self.overrideredirect(True)

    def center_on_parent(self):
        """Center the popup window on the parent window"""
        self.update_idletasks()
        
        # Get parent window geometry
        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        
        # Calculate center position based on current window size
        popup_width = 500
        popup_height = 580 if not self.edit_mode else 650
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    
    def adjust_window_size(self):
        """Adjust window size based on edit mode"""
        current_geometry = self.geometry()
        width = 500
        height = 650 if self.edit_mode else 580
        
        # Extract current position
        if current_geometry and 'x' in current_geometry:
            pos_part = current_geometry.split('+')[1:]
            if len(pos_part) >= 2:
                x, y = int(pos_part[0]), int(pos_part[1])
                self.geometry(f"{width}x{height}+{x}+{y}")
            else:
                self.geometry(f"{width}x{height}")
        else:
            self.geometry(f"{width}x{height}")
        
        # Re-center the window
        self.center_on_parent()

    def setup_ui(self):
        # Main container with modern styling
        main_container = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=20, 
                                    border_width=2, border_color=COLOR_GRAY_200)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with close button
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
        header_frame.pack(fill="x", padx=25, pady=(20, 0))
        header_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(header_frame, text="👤 User Profile", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
        title_label.pack(side="left", pady=15)

        # Close button
        close_btn = AnimatedButton(header_frame, text="✕", font=("Segoe UI", 16, "bold"),
                                 fg_color=COLOR_ACCENT_ERROR, hover_color="#5a1e1e",
                                 text_color=COLOR_WHITE, corner_radius=15, width=30, height=30,
                                 command=self.on_close)
        close_btn.pack(side="right", pady=15)

        # Edit button (only show when not in edit mode)
        self.edit_btn = AnimatedButton(header_frame, text="✏ Edit", command=self.toggle_edit,
                                     fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER,
                                     text_color=COLOR_WHITE, corner_radius=8, height=36)
        self.edit_btn.pack(side="right", padx=(0, 10), pady=15)

        # Content area
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)

        # Profile form
        self.entries = {}
        
        # Get user details from database
        if self.user_email:
            user_details = get_user_details(self.user_email)
            if user_details:
                first_name, last_name, email, role = user_details
                self.profile_data = {
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Email": email,
                    "Role": role
                }
            else:
                # Fallback to default data if user not found
                self.profile_data = {
                    "First Name": "User",
                    "Last Name": "Unknown",
                    "Email": self.user_email or "No email",
                    "Role": "Unknown"
                }
        else:
            # Fallback to default data if no email provided
            self.profile_data = {
                "First Name": "User",
                "Last Name": "Unknown",
                "Email": "No email provided",
                "Role": "Unknown"
            }

        # Form fields with enhanced styling
        for i, (label_text, default_value) in enumerate(self.profile_data.items()):
            # Skip Photo Path field in the form
            if label_text == "Photo Path":
                continue
                
            # Field container
            field_frame = ctk.CTkFrame(content_frame, fg_color="transparent", height=80)
            field_frame.pack(fill="x", pady=10)
            field_frame.pack_propagate(False)
            
            # Label
            label = ctk.CTkLabel(field_frame, text=label_text, font=FONT_H3, text_color=COLOR_TEXT_SECONDARY)
            label.pack(anchor="w", pady=(0, 5))
            
            # Entry with modern styling
            entry = ctk.CTkEntry(field_frame, placeholder_text=f"Enter {label_text.lower()}",
                               font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY, height=45,
                               fg_color=COLOR_GRAY_50, border_color=COLOR_GRAY_300,
                               corner_radius=10)
            entry.insert(0, default_value)
            entry.configure(state="readonly")
            entry.pack(fill="x", pady=(0, 5))
            self.entries[label_text] = entry

        # Action buttons
        button_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
        button_frame.pack(fill="x", padx=25, pady=(0, 20))
        button_frame.pack_propagate(False)

        # Save and Cancel buttons (initially hidden)
        self.save_btn = AnimatedButton(button_frame, text="💾 Save Changes", 
                                     fg_color=COLOR_ACCENT_SUCCESS, hover_color="#1f3d1b",
                                     text_color=COLOR_WHITE, corner_radius=10, height=45,
                                     command=self.save_changes)
        
        self.cancel_btn = AnimatedButton(button_frame, text="❌ Cancel", 
                                       fg_color=COLOR_GRAY_600, hover_color=COLOR_GRAY_700,
                                       text_color=COLOR_WHITE, corner_radius=10, height=45,
                                       command=self.cancel_changes)

    def toggle_edit(self):
        self.edit_mode = not self.edit_mode
        new_state = "normal" if self.edit_mode else "readonly"

        for entry in self.entries.values():
            entry.configure(state=new_state)
            if self.edit_mode:
                entry.configure(border_color=COLOR_PRIMARY, border_width=2)
            else:
                entry.configure(border_color=COLOR_GRAY_300, border_width=1)

        # Update UI based on edit mode
        if self.edit_mode:
            self.edit_btn.pack_forget()  # Hide the Edit button
            self.save_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
            self.cancel_btn.pack(side="right", expand=True, fill="x", padx=(10, 0))
        else:
            self.edit_btn.pack(side="right", padx=(0, 10), pady=15)  # Show the Edit button
            self.save_btn.pack_forget()
            self.cancel_btn.pack_forget()
        
        # Adjust window size based on mode
        self.adjust_window_size()

    def save_changes(self):
        """Save the profile changes to database and reopen view popup"""
        updated_data = {label: entry.get() for label, entry in self.entries.items()}
        
        first = updated_data.get("First Name", "")
        last = updated_data.get("Last Name", "")
        role = updated_data.get("Role", "")

        # Update in database
        if self.user_email:
            update_user_profile(self.user_email, first, last, role)

        # Update dashboard label/button if available
        # Navigate to the DashboardPage instance
        app_window = self.master
        while app_window is not None and not hasattr(app_window, 'main_frame'):
            app_window = getattr(app_window, 'master', None)
        if app_window:
            main_frame = getattr(app_window, 'main_frame', None)
            if main_frame:
                for child in main_frame.winfo_children():
                    if hasattr(child, 'welcome_label') and hasattr(child, 'profile_btn'):
                        # Update welcome label
                        greeting = child.get_current_greeting()
                        child.welcome_label.configure(text=f"Good {greeting}, {first}!")
                        child.profile_btn.configure(text=f"{first} {last}")
                        break

        # Close current popup
        self.grab_release()
        self.destroy()
        
        # Reopen View Profile popup with updated info
        popup = UserProfilePopup(self.master, self.user_email)
        popup.center_on_parent()
        popup.grab_set()

    def cancel_changes(self):
        """Cancel changes and reopen view profile popup"""
        # Close current popup
        self.grab_release()
        self.destroy()
        
        # Reopen view profile popup with same user_email
        new_popup = UserProfilePopup(self.master, self.user_email)
        new_popup.center_on_parent()
        new_popup.grab_set()

    def on_close(self):
        """Handle window close event"""
        if self.edit_mode:
            # If in edit mode, ask for confirmation or auto-cancel
            self.cancel_changes()
        
        self.grab_release()
        self.destroy()

# This pop-up window shows recent notifications about the inventory, such as low stock alerts and items nearing expiration.
class NotificationPopup(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_window()
        self.setup_ui()
        
        # Center the popup on the parent window
        self.center_on_parent()
        
        # Make the popup modal
        self.transient(master)
        self.grab_set()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.title("Notifications")
        self.geometry("550x400")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_MAIN_BG)

    def center_on_parent(self):
        """Center the popup window on the parent window"""
        self.update_idletasks()
        
        # Get parent window geometry
        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        
        # Calculate center position
        popup_width = 550
        popup_height = 400
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    def setup_ui(self):
        # Main container
        main_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=20, 
                                    border_width=2, border_color=COLOR_GRAY_200)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with close button
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
        header_frame.pack(fill="x", padx=25, pady=(20, 0))
        header_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(header_frame, text="Notifications", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
        title_label.pack(side="left", pady=15)

        # Close button
        close_btn = AnimatedButton(header_frame, text="✕", font=("Segoe UI", 16, "bold"),
                                 fg_color="transparent", hover_color=COLOR_GRAY_100,
                                 text_color=COLOR_GRAY_600, corner_radius=15, width=30, height=30,
                                 command=self.on_close)
        close_btn.pack(side="right", pady=15)

        # Notifications list
        notifications_frame = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        notifications_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Sample notifications data
        notifications = [
            {
                "type": "error",
                "icon": "⚠️",
                "title": "Ketchup is currently out of stock.",
                "date": "May 23, 2025",
                "bg_color": "#fff5f5",
                "border_color": "#fed7d7"
            },
            {
                "type": "warning", 
                "icon": "⚠️",
                "title": "Soy Sauce is running low on stocks.\nOnly 4 remaining.",
                "date": "May 23, 2025",
                "bg_color": "#fffbeb",
                "border_color": "#fed7aa"
            },
            {
                "type": "warning",
                "icon": "⚠️", 
                "title": "Fish Sauce is running low on stocks.\nOnly 2 remaining.",
                "date": "May 23, 2025",
                "bg_color": "#fffbeb",
                "border_color": "#fed7aa"
            },
            {
                "type": "info",
                "icon": "🕐",
                "title": "Sugar is nearing its expiry date.\nExpiry: May 31, 2025.",
                "date": "May 23, 2025", 
                "bg_color": "#fef2f2",
                "border_color": "#fecaca"
            }
        ]

        for notification in notifications:
            self.create_notification_item(notifications_frame, notification)

    def create_notification_item(self, parent, notification):
        # Notification item container
        item_frame = ctk.CTkFrame(parent, fg_color=notification["bg_color"], 
                                  corner_radius=8, border_width=1, border_color=notification["border_color"])
        item_frame.pack(fill="x", pady=5)

        # Content frame
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)

        # Icon
        icon_label = ctk.CTkLabel(content_frame, text=notification["icon"], font=("Segoe UI", 18))
        icon_label.grid(row=0, column=0, rowspan=2, padx=(0, 12), sticky="n")

        # Main message (row 0)
        title_label = ctk.CTkLabel(content_frame, text=notification["title"], 
                                   font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY, anchor="w", justify="left")
        title_label.grid(row=0, column=1, sticky="w")

        # Date (row 1)
        date_label = ctk.CTkLabel(content_frame, text=notification["date"], 
                                  font=FONT_SMALL, text_color=COLOR_TEXT_MUTED, anchor="w")
        date_label.grid(row=1, column=1, sticky="w")

    def on_close(self):
        """Handle window close event"""
        self.grab_release()
        self.destroy()

# This is the sidebar panel containing the logo, app name, and navigation buttons.
# It dynamically adjusts buttons based on the user's role (e.g., Admin sees History Logs).
class ModernSidebar(ctk.CTkFrame):
    def __init__(self, master, on_nav=None, user_role="Employee", **kwargs):
        super().__init__(master, width=280, fg_color=COLOR_SAPPHIRE, corner_radius=0, **kwargs)
        self.pack_propagate(False)
        self.active_button = None
        self.on_nav = on_nav
        self.nav_buttons = {}  # Store buttons by name
        self.user_role = user_role
        self.setup_ui()
        
    def setup_ui(self):
        # Logo section with better styling
        logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", pady=(30, 40))
        logo_frame.pack_propagate(False)
        logo_frame.grid_columnconfigure(1, weight=1)

        # Load and place logo image
        logo_path = os.path.join(os.path.dirname(__file__), "LOGO2.png")
        logo_image = Image.open(logo_path)
        logo_ctk = CTkImage(light_image=logo_image, size=(60, 60))
        logo_icon = ctk.CTkLabel(logo_frame, image=logo_ctk, text="")
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
            ("Dashboard", "🏠", True),
            ("Inventory", "📦", False),
            ("Items", "🏷️", False)
        ]
        # Only add History Logs for Admin/Owner
        if self.user_role.lower() in ["admin", "owner"]:
            nav_buttons.append(("History Logs", "📋", False))

        for name, icon, is_active in nav_buttons:
            btn = self.create_nav_button(nav_frame, name, icon, is_active)
            btn.pack(fill="x", pady=5)
            self.nav_buttons[name] = btn
            
        # User section at bottom
        user_frame = ctk.CTkFrame(self, fg_color=COLOR_SECONDARY_DARK, corner_radius=12, height=80)
        user_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        user_frame.pack_propagate(False)
        
        # Log Out button
        def logout():
            self.master.destroy()
            subprocess.Popen([sys.executable, "StartPage.py"])
        
        logout_btn = ctk.CTkButton(user_frame, text="Log Out", font=FONT_BUTTON,
                                 text_color=COLOR_WHITE, fg_color="transparent",
                                 hover_color=COLOR_SECONDARY_LIGHT, corner_radius=10, height=50,
                                 command=logout)
        logout_btn.pack(expand=True, padx=15, pady=15)

        print("ModernSidebar user_role:", self.user_role)

    def create_nav_button(self, parent, name, icon, is_active=False):
        fg_color = COLOR_SECONDARY_DARK if is_active else "transparent"
        text_color = COLOR_ROYAL_BLUE if is_active else COLOR_ROYAL_BLUE
        hover_color = COLOR_SECONDARY_LIGHT if not is_active else COLOR_SECONDARY_DARK
        
        btn = ctk.CTkButton(parent, text=f"{icon}  {name}", font=FONT_BUTTON,
                           text_color=text_color, fg_color=fg_color,
                           hover_color=hover_color, corner_radius=10, height=50,
                           anchor="w", command=lambda n=name: self.set_active(n))
        
        if is_active:
            self.active_button = btn
            
        return btn
        
    def set_active(self, name):
        # Update all button colors
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(fg_color=COLOR_SECONDARY_DARK, text_color=COLOR_ROYAL_BLUE, hover_color=COLOR_SECONDARY_DARK)
            else:
                btn.configure(fg_color="transparent", text_color=COLOR_ROYAL_BLUE, hover_color=COLOR_SECONDARY_LIGHT)
        if self.on_nav:
            self.on_nav(name)

class DashboardOverviewFrame(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.configure(fg_color=COLOR_MAIN_BG)
        self.build_top_bar()
        self.build_overview_section()
        self.build_analytics_section()

    def build_top_bar(self):
        user_email = getattr(self.controller, 'user_email', None)
        print("DashboardOverviewFrame user_email:", user_email)
        first_name = get_first_name(user_email) or "User"
        full_name = get_full_name(user_email) or "User"
        greeting = f"Good {self.get_current_greeting()}, {first_name}! 🖐"
        sub_label = "Here's what's happening with your inventory today"

        top_bar = ctk.CTkFrame(self, fg_color=COLOR_MAIN_BG)
        top_bar.pack(fill="x", padx=30, pady=(20, 0))
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)
        left_frame = ctk.CTkFrame(top_bar, fg_color=COLOR_MAIN_BG)
        left_frame.grid(row=0, column=0, sticky="w")
        greeting_label = ctk.CTkLabel(left_frame, text=greeting, font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        greeting_label.pack(anchor="w")
        sub_label_widget = ctk.CTkLabel(left_frame, text=sub_label, font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        sub_label_widget.pack(anchor="w")
        right_frame = ctk.CTkFrame(top_bar, fg_color=COLOR_MAIN_BG)
        right_frame.grid(row=0, column=1, sticky="e", padx=(0, 10))

        notif_btn = ctk.CTkButton(
            right_frame,
            text="🔔",
            width=48,
            height=40,
            font=("Segoe UI", 20),
            fg_color="#f6f7fa",
            text_color="#8094c2",
            hover_color="#e9ecf3",
            corner_radius=12,
            border_width=0,
            command=self.show_notifications
        )
        notif_btn.pack(side="left", padx=(0, 12))

        user_btn = ctk.CTkButton(
            right_frame,
            text=full_name,
            width=160,
            height=40,
            font=("Segoe UI", 16, "bold"),
            fg_color="#f6f7fa",
            text_color="#8094c2",
            hover_color="#e9ecf3",
            corner_radius=12,
            border_width=0,
            command=self.show_user_profile
        )
        user_btn.pack(side="left")
        self.greeting_label = greeting_label
        self.user_btn = user_btn

    def build_overview_section(self):
        overview_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=COLOR_CARD_BG, border_width=1, border_color=COLOR_GRAY_200)
        overview_frame.pack(fill="x", padx=30, pady=20)
        header_frame = ctk.CTkFrame(overview_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(25, 20))
        overview_label = ctk.CTkLabel(header_frame, text="📊 Overview", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
        overview_label.pack(side="left")
        refresh_btn = AnimatedButton(header_frame, text="🔄 Refresh", font=FONT_SMALL, fg_color=COLOR_SIDEBAR_BG, text_color=COLOR_TEXT_SECONDARY, hover_color=COLOR_SIDEBAR_ACTIVE, corner_radius=6, height=32, command=self.refresh_overview_cards)
        refresh_btn.pack(side="right")
        cards_frame = ctk.CTkFrame(overview_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=(0, 25))
        item_count = count_items()
        formatted_count = f"{item_count:,}"
        total_quantity = count_good_stock_items()
        formatted_quantity = f"{total_quantity:,}"
        out_of_stock = count_out_of_stock_items()
        formatted_out = f"{out_of_stock:,}"
        low_stock = count_low_stock_items()
        formatted_low = f"{low_stock:,}"
        cards_data = [
            (COLOR_PRIMARY, "📦", formatted_count, "Total Products"),
            (COLOR_ACCENT_SUCCESS, "✅", formatted_quantity, "Items in Stock"),
            (COLOR_ACCENT_ERROR, "⚠️", formatted_out, "Out of Stock"),
            (COLOR_ACCENT_WARNING, "🔔", formatted_low, "Low Stock Alerts")
        ]
        self.cards = []
        for bg_color, icon, value, label in cards_data:
            card = EnhancedCard(cards_frame, bg_color, icon, value, label)
            card.pack(side="left", expand=True, fill="both", padx=8)
            self.cards.append(card)

    def build_analytics_section(self):
        analytics_frame = ctk.CTkFrame(self, fg_color="transparent")
        analytics_frame.pack(fill="x", padx=30, pady=(0, 30))
        calendar_frame = ctk.CTkFrame(analytics_frame, corner_radius=16, fg_color=COLOR_CARD_BG, border_width=1, border_color=COLOR_GRAY_200)
        calendar_frame.pack(side="left", fill="y", padx=(0, 15))
        cal_header = ctk.CTkLabel(calendar_frame, text="📅 Calendar", font=FONT_H3, text_color=COLOR_TEXT_PRIMARY)
        cal_header.pack(pady=(20, 15))
        today = datetime.now()
        calendar = Calendar(
            calendar_frame,
            selectmode='day',
            year=today.year,
            month=today.month,
            day=today.day,
            background=COLOR_CARD_BG,
            foreground=COLOR_TEXT_SECONDARY,
            headersbackground=COLOR_PRIMARY,
            headersforeground=COLOR_WHITE,
            selectbackground=COLOR_SECONDARY,
            selectforeground=COLOR_WHITE,
            weekendbackground=COLOR_SIDEBAR_BG,
            weekendforeground=COLOR_TEXT_MUTED,
            bordercolor=COLOR_GRAY_200,
            font=FONT_BODY,
            firstweekday='sunday'
        )
        calendar.pack(padx=20, pady=(0, 20))
        chart_frame = ctk.CTkFrame(analytics_frame, corner_radius=16, fg_color=COLOR_CARD_BG, border_width=1, border_color=COLOR_GRAY_200)
        chart_frame.pack(side="right", fill="both", expand=True)
        chart_header = ctk.CTkFrame(chart_frame, fg_color="transparent")
        chart_header.pack(fill="x", padx=25, pady=(20, 15))
        chart_title = ctk.CTkLabel(chart_header, text="📈 Top Consumed Products", font=FONT_H3, text_color=COLOR_TEXT_PRIMARY)
        chart_title.pack(side="left")
        period_label = ctk.CTkLabel(chart_header, text="This Week", font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
        period_label.pack(side="right")
        chart_content = ctk.CTkScrollableFrame(chart_frame, fg_color="transparent")
        chart_content.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        top_items = get_top_consumed_items()
        color_palette = [
            COLOR_PRIMARY,
            COLOR_ACCENT_SUCCESS,
            COLOR_ACCENT_ERROR,
            COLOR_SECONDARY,
            COLOR_ACCENT_WARNING,
            COLOR_SECONDARY_DARK,
            COLOR_GRAY_600,
            COLOR_GRAY_700,
            COLOR_GRAY_800
        ]
        for i, (item_name, percentage) in enumerate(top_items):
            color = color_palette[i % len(color_palette)]
            self.create_consumption_bar(chart_content, item_name, percentage, color, i)

    def create_consumption_bar(self, parent, item, value, color, index):
        bar_container = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        bar_container.pack(fill="x", pady=8)
        bar_container.pack_propagate(False)
        info_frame = ctk.CTkFrame(bar_container, fg_color="transparent")
        info_frame.pack(fill="x")
        item_label = ctk.CTkLabel(info_frame, text=item, font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY)
        item_label.pack(side="left")
        value_label = ctk.CTkLabel(info_frame, text=f"{value}%", font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
        value_label.pack(side="right")
        progress_bg = ctk.CTkFrame(bar_container, fg_color=COLOR_SIDEBAR_BG, height=8, corner_radius=4)
        progress_bg.pack(fill="x", pady=(5, 0))
        progress_bar = ctk.CTkFrame(progress_bg, fg_color=color, height=8, corner_radius=4)
        progress_bar.place(x=0, y=0, relheight=1)
        self.animate_progress_bar(progress_bar, value)

    def animate_progress_bar(self, bar, target_width):
        def animate():
            current_width = 0
            target = target_width / 100
            step = target / 30
            while current_width < target:
                current_width = min(current_width + step, target)
                bar.place(x=0, y=0, relwidth=current_width, relheight=1)
                time.sleep(0.02)
        threading.Thread(target=animate, daemon=True).start()

    def get_current_greeting(self):
        now = datetime.now().time()
        if now >= datetime.strptime("05:00", "%H:%M").time() and now < datetime.strptime("12:00", "%H:%M").time():
            return "Morning"
        elif now >= datetime.strptime("12:00", "%H:%M").time() and now < datetime.strptime("18:00", "%H:%M").time():
            return "Afternoon"
        else:
            return "Evening"

    def refresh_overview_cards(self):
        item_count = count_items()
        formatted_count = f"{item_count:,}"
        total_quantity = count_good_stock_items()
        formatted_quantity = f"{total_quantity:,}"
        out_of_stock = count_out_of_stock_items()
        formatted_out = f"{out_of_stock:,}"
        low_stock = count_low_stock_items()
        formatted_low = f"{low_stock:,}"
        if hasattr(self, 'cards') and len(self.cards) >= 4:
            self.cards[0].animate_value(formatted_count)
            self.cards[1].animate_value(formatted_quantity)
            self.cards[2].animate_value(formatted_out)
            self.cards[3].animate_value(formatted_low)

    def show_notifications(self):
        self.controller.show_notifications()

    def show_user_profile(self):
        self.controller.show_user_profile()

# --- Refactored DashboardPage ---
class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.sidebar = ModernSidebar(self, on_nav=self.on_nav, user_role=getattr(controller, 'user_role', 'Employee'))
        self.sidebar.pack(side="left", fill="y")
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_MAIN_BG, corner_radius=0)
        self.main_frame.pack(side="left", fill="both", expand=True)
        # --- New: content_container for swapping frames ---
        self.content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)
        # --- Instantiate all sub-frames ---
        self.dashboard_overview = DashboardOverviewFrame(self.content_container, self)
        from inventoryy import InventoryPage
        from items import ItemsPage
        from history_log import HistoryLogsFrame
        self.inventory_page = InventoryPage(self.content_container, user_id=getattr(controller, 'user_id', None))
        self.items_page = ItemsPage(self.content_container, user_id=getattr(controller, 'user_id', None))
        self.history_logs = HistoryLogsFrame(self.content_container)
        # Show dashboard overview by default
        self.show_content("Dashboard")

    def show_content(self, name):
        for frame in [self.dashboard_overview, self.inventory_page, self.items_page, self.history_logs]:
            frame.pack_forget()
        if name == "Dashboard":
            self.dashboard_overview.pack(fill="both", expand=True)
        elif name == "Inventory":
            self.inventory_page.pack(fill="both", expand=True)
        elif name == "Items":
            self.items_page.pack(fill="both", expand=True)
        elif name == "History Logs":
            self.history_logs.pack(fill="both", expand=True)

    def on_nav(self, name):
        self.show_content(name)

    def show_notifications(self):
        notifications = []
        today = datetime.now().strftime('%b %d, %Y')
        for item in get_all_items():
            name = item[1]
            qty = item[3]
            exp = item[7] if len(item) > 7 else None
            if qty == 0:
                notifications.append({
                    "type": "error",
                    "icon": "⚠️",
                    "title": f"{name} is currently out of stock.",
                    "date": today,
                    "bg_color": "#fff5f5",
                    "border_color": "#fed7d7"
                })
            elif qty < (item[12] if len(item) > 12 and item[12] is not None else 6):
                notifications.append({
                    "type": "warning",
                    "icon": "⚠️",
                    "title": f"{name} is running low on stocks. Only {qty} remaining.",
                    "date": today,
                    "bg_color": "#fffbeb",
                    "border_color": "#fed7aa"
                })
        for name, exp_date, qty in get_near_expiry_items():
            notifications.append({
                "type": "info",
                "icon": "🕐",
                "title": f"{name} is nearing its expiry date. Expiry: {exp_date}.",
                "date": today,
                "bg_color": "#fef2f2",
                "border_color": "#fecaca"
            })
        class RealNotificationPopup(NotificationPopup):
            def setup_ui(self):
                main_container = ctk.CTkFrame(self, fg_color=COLOR_WHITE, corner_radius=20, border_width=2, border_color=COLOR_GRAY_200)
                main_container.pack(fill="both", expand=True, padx=20, pady=20)
                header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
                header_frame.pack(fill="x", padx=25, pady=(20, 0))
                header_frame.pack_propagate(False)
                title_label = ctk.CTkLabel(header_frame, text="Notifications", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
                title_label.pack(side="left", pady=15)
                close_btn = AnimatedButton(header_frame, text="✕", font=("Segoe UI", 16, "bold"), fg_color="transparent", hover_color=COLOR_GRAY_100, text_color=COLOR_GRAY_600, corner_radius=15, width=30, height=30, command=self.on_close)
                close_btn.pack(side="right", pady=15)
                notifications_frame = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
                notifications_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))
                if notifications:
                    for notification in notifications:
                        self.create_notification_item(notifications_frame, notification)
                else:
                    empty_label = ctk.CTkLabel(notifications_frame, text="No notifications.", font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
                    empty_label.pack(pady=20)
        popup = RealNotificationPopup(self)
        popup.center_on_parent()
        popup.grab_set()

    def show_user_profile(self):
        user_email = getattr(self.controller, 'user_email', None)
        UserProfilePopup(self, user_email)

