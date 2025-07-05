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
from datetime import datetime, timedelta
from database import get_all_history_logs

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

# New embeddable frame for history logs
class HistoryLogsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=COLOR_MAIN_BG)
        self.history_data = self.generate_history_data()
        self.setup_ui()

    def generate_history_data(self):
        logs = get_all_history_logs()
        history_by_date = {}

        now = datetime.now()
        for log in logs:
            log_id, action, timestamp, details, first_name, last_name, item_name = log
            # Parse timestamp
            log_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            # Group by date
            if log_time.date() == now.date():
                date_key = f"Today, {now.strftime('%B %d, %Y')}"
            elif log_time.date() == (now - timedelta(days=1)).date():
                date_key = f"Yesterday, {(now - timedelta(days=1)).strftime('%B %d, %Y')}"
            else:
                date_key = log_time.strftime("%B %d, %Y")
            # Format description
            user = f"{first_name} {last_name}" if first_name and last_name else "Unknown User"
            if details:
                description = f"{details}\nBy: {user}"
            else:
                description = f"{user} performed {action} on {item_name or 'an item'}"
            # Calculate "time ago"
            delta = now - log_time
            if delta.days > 0:
                time_ago = f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
            elif delta.seconds >= 3600:
                time_ago = f"{delta.seconds // 3600} hour{'s' if delta.seconds // 3600 > 1 else ''} ago"
            elif delta.seconds >= 60:
                time_ago = f"{delta.seconds // 60} mins ago"
            else:
                time_ago = "just now"
            # Choose icon/type based on action
            action_lower = (action or "").lower()
            if "add" in action_lower:
                icon, type_ = "➕", "add"
            elif "deduct" in action_lower or "remove" in action_lower:
                icon, type_ = "➖", "deduct"
            elif "update" in action_lower:
                icon, type_ = "✏️", "update"
            else:
                icon, type_ = "ℹ️", "info"
            # Build activity dict
            activity = {
                "action": action,
                "description": description,
                "time": time_ago,
                "type": type_,
                "icon": icon
            }
            history_by_date.setdefault(date_key, []).append(activity)
        return history_by_date

    def setup_ui(self):
        self.build_header()
        self.build_content()

    def build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", expand=True, fill="both")
        title_label = ctk.CTkLabel(title_frame, text="📋 History", font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        title_label.pack(anchor="w", pady=(15, 0))
        subtitle = ctk.CTkLabel(title_frame, text="Track all inventory changes and activities", font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        subtitle.pack(anchor="w")
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Add Refresh button
        refresh_btn = AnimatedButton(
            actions_frame,
            text="🔄 Refresh",
            font=FONT_BUTTON,
            fg_color=COLOR_SECONDARY,
            hover_color=COLOR_SECONDARY_DARK,
            corner_radius=8,
            height=40,
            width=120,
            command=self.refresh_data
        )
        refresh_btn.pack(padx=(0, 0), pady=(15, 0))

    def build_content(self):
        self.content_container = ctk.CTkFrame(self, corner_radius=16, fg_color=COLOR_CARD_BG, border_width=1, border_color=COLOR_GRAY_200)
        self.content_container.pack(fill="both", expand=True, padx=30, pady=20)
        self.build_toolbar(self.content_container)
        self.build_history_feed(self.content_container)

    def build_toolbar(self, parent):
        toolbar_frame = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        toolbar_frame.pack(fill="x", padx=25, pady=(20, 15))
        toolbar_frame.pack_propagate(False)
        search_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        search_frame.pack(side="left", expand=True, fill="both")
        search_label = ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 16), text_color=COLOR_TEXT_MUTED)
        search_label.pack(side="left", padx=(0, 10), pady=15)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search History...", font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY, height=40, fg_color=COLOR_GRAY_50, border_color=COLOR_GRAY_300, corner_radius=8)
        self.search_entry.pack(side="left", expand=True, fill="x", pady=15)
        
        # Add clear search button
        clear_btn = AnimatedButton(
            search_frame,
            text="✕",
            font=("Segoe UI", 12, "bold"),
            fg_color="transparent",
            hover_color=COLOR_GRAY_200,
            text_color=COLOR_TEXT_MUTED,
            corner_radius=6,
            width=30,
            height=30,
            command=self.clear_search
        )
        clear_btn.pack(side="right", padx=(10, 0), pady=15)
        
        # Bind search functionality
        self.search_entry.bind("<KeyRelease>", self.on_search)
        self.search_entry.bind("<Return>", self.on_search)

    def build_history_feed(self, parent, filtered_data=None):
        # If feed_frame doesn't exist, create it
        if not hasattr(self, 'feed_frame') or self.feed_frame is None:
            self.feed_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
            self.feed_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        else:
            # Clear existing content instead of destroying the frame
            for widget in self.feed_frame.winfo_children():
                widget.destroy()
        
        # Use filtered data if provided, otherwise use all history data
        data_to_display = filtered_data if filtered_data is not None else self.history_data
        
        if not data_to_display:
            # Show "No results found" message
            no_results_label = ctk.CTkLabel(
                self.feed_frame,
                text="No matching history found.\nTry adjusting your search terms.",
                font=FONT_BODY,
                text_color=COLOR_TEXT_MUTED,
                justify="center"
            )
            no_results_label.pack(pady=50)
        else:
            for date, activities in data_to_display.items():
                self.create_date_section(self.feed_frame, date, activities)
        
        # Force update after adding content
        self.feed_frame.update_idletasks()

    def create_date_section(self, parent, date, activities):
        date_header = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        date_header.pack(fill="x", pady=(15, 10))
        date_header.pack_propagate(False)
        line_frame = ctk.CTkFrame(date_header, fg_color="transparent")
        line_frame.pack(expand=True, fill="both")
        left_line = ctk.CTkFrame(line_frame, fg_color=COLOR_GRAY_300, height=2)
        left_line.pack(side="left", expand=True, fill="x", pady=24)
        date_label = ctk.CTkLabel(line_frame, text=date, font=FONT_H3, text_color=COLOR_TEXT_PRIMARY)
        date_label.pack(side="left", padx=20)
        right_line = ctk.CTkFrame(line_frame, fg_color=COLOR_GRAY_300, height=2)
        right_line.pack(side="right", expand=True, fill="x", pady=24)
        for activity in activities:
            self.create_activity_item(parent, activity)

    def create_activity_item(self, parent, activity):
        activity_frame = ctk.CTkFrame(parent, fg_color=COLOR_WHITE, corner_radius=10, border_width=1, border_color=COLOR_GRAY_200)
        activity_frame.pack(fill="x", pady=5)
        content_frame = ctk.CTkFrame(activity_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", expand=True, fill="x")
        icon_label = ctk.CTkLabel(left_frame, text=activity["icon"], font=("Segoe UI", 18))
        icon_label.pack(side="left", padx=(0, 15))
        text_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        text_frame.pack(side="left", expand=True, fill="x")
        action_label = ctk.CTkLabel(text_frame, text=activity["action"], font=FONT_H3, text_color=COLOR_ACCENT_SUCCESS if activity["type"]=="add" else COLOR_ACCENT_ERROR if activity["type"]=="deduct" else COLOR_ACCENT_INFO if activity["type"]=="update" else COLOR_ACCENT_WARNING if activity["type"]=="alert" else COLOR_TEXT_PRIMARY, anchor="w")
        action_label.pack(anchor="w")
        desc_label = ctk.CTkLabel(text_frame, text=activity["description"], font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY, anchor="w", wraplength=400)
        desc_label.pack(anchor="w", pady=(2, 0))
        time_label = ctk.CTkLabel(content_frame, text=activity["time"], font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
        time_label.pack(side="right", anchor="ne")

    def refresh_data(self):
        """Refresh history data and maintain current search state"""
        # Store current search term
        current_search = ""
        if hasattr(self, 'search_entry'):
            current_search = self.search_entry.get().strip()
        
        # Regenerate history data
        self.history_data = self.generate_history_data()
        
        # Instead of destroying everything, just refresh the feed content
        if hasattr(self, 'feed_frame') and self.feed_frame is not None:
            # Clear only the feed content
            for widget in self.feed_frame.winfo_children():
                widget.destroy()
            
            # Rebuild the feed with current search state
            if current_search:
                filtered_data = self.filter_history_data(current_search)
                self.build_history_feed(self.content_container, filtered_data)
            else:
                self.build_history_feed(self.content_container)
        else:
            # If feed_frame doesn't exist, rebuild everything
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget != self:
                    widget.destroy()
            
            self.setup_ui()
            
            # Restore search term and apply filter if there was one
            if current_search and hasattr(self, 'search_entry'):
                self.search_entry.insert(0, current_search)
                self.on_search()

    def on_search(self, event=None):
        """Handle search input and filter history data"""
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            # If search is empty, show all data
            self.build_history_feed(self.content_container)
        else:
            # Filter data based on search term
            filtered_data = self.filter_history_data(search_term)
            self.build_history_feed(self.content_container, filtered_data)
    
    def filter_history_data(self, search_term):
        """Filter history data based on search term"""
        filtered_data = {}
        
        for date, activities in self.history_data.items():
            matching_activities = []
            
            for activity in activities:
                # Search in action, description, and other relevant fields
                searchable_text = " ".join([
                    activity.get("action", ""),
                    activity.get("description", ""),
                    activity.get("type", "")
                ]).lower()
                
                if search_term in searchable_text:
                    matching_activities.append(activity)
            
            # Only include dates that have matching activities
            if matching_activities:
                filtered_data[date] = matching_activities
        
        return filtered_data

    def clear_search(self):
        """Clear the search field and show all history data"""
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, 'end')
            self.build_history_feed(self.content_container)

# Keep the window version for standalone use
class HistoryLogsPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSmart - History Logs")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=COLOR_MAIN_BG)
        self.frame = HistoryLogsFrame(self)
        self.frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = HistoryLogsPage()
    app.mainloop()