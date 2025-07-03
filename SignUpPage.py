import customtkinter as ctk
from PIL import Image
import threading
import time
import sys
from app_navigation import show_signin, show_dashboard
from database import add_user
import subprocess
from dashboard import (
    COLOR_CARD_BG, COLOR_GRAY_200, COLOR_ACCENT_ERROR, COLOR_WHITE, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_H2, FONT_BODY, AnimatedButton
)

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# App Setup
role = 'Employee'
if len(sys.argv) > 1:
    role = sys.argv[1]
app = ctk.CTk()
app.geometry("1200x800")
app.resizable(True, True)
app.title("Sign Up")

def center_window(window, width=1200, height=800):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

center_window(app, 1200, 800)

# Animation variables
is_animating = False

# Load icons (create placeholder images if files don't exist)
try:
    eye_open_img = ctk.CTkImage(Image.open("eye_open.png"), size=(25, 25))
    eye_closed_img = ctk.CTkImage(Image.open("eye_close.png"), size=(25, 25))
except FileNotFoundError:
    # Create simple placeholder images if files don't exist
    from PIL import Image, ImageDraw
    
    # Create eye open image
    img_open = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_open)
    draw.ellipse([5, 8, 20, 17], fill='black')
    draw.ellipse([10, 10, 15, 15], fill='white')
    eye_open_img = ctk.CTkImage(img_open, size=(25, 25))
    
    # Create eye closed image
    img_closed = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_closed)
    draw.line([5, 12, 20, 12], fill='black', width=2)
    eye_closed_img = ctk.CTkImage(img_closed, size=(25, 25))

show_password = False
show_confirm_password = False

# Grid config
for col in (0, 1):
    app.grid_columnconfigure(col, weight=1, uniform="half")
app.grid_rowconfigure(0, weight=1)

# Frames
left_frame = ctk.CTkFrame(app, fg_color="#8094c2", corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew")
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

right_frame = ctk.CTkFrame(app, fg_color="#f9f5eb", corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

left_inner_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
left_inner_frame.grid(row=0, column=0, padx=25, pady=10, sticky="nsew")
left_inner_frame.grid_rowconfigure(16, weight=1)  # Changed to 16 to accommodate error label at row 15
left_inner_frame.grid_columnconfigure(0, weight=1)

# Title
title = ctk.CTkLabel(
    left_inner_frame,
    text="Hi!",
    font=ctk.CTkFont(family="Instrument Sans", size=60, weight="bold"),
    text_color="#0B1D4B"
)
title.grid(row=1, column=0, sticky="w", padx=(40,400),  pady=(30,0))

# Subtitle
subtitle = ctk.CTkLabel(
    left_inner_frame,
    text="Please enter your details",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    text_color="white"
)
subtitle.grid(row=2, column=0, sticky="w", pady=(0, 10), padx=(40, 10))

# First Name Label
first_name_label = ctk.CTkLabel(
    left_inner_frame,
    text="First Name",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
first_name_label.grid(row=3, column=0, padx=(40, 10), pady=(0, 4), sticky="w")

# First Name Entry with animations
first_name_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="     Enter your first name",
    height=50,
    width=280,
    corner_radius=8,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
first_name_entry.grid(row=4, column=0, sticky="ew", pady=(0, 15), padx=(40,10))

# Last Name Label
last_name_label = ctk.CTkLabel(
    left_inner_frame,
    text="Last Name",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
last_name_label.grid(row=5, column=0, sticky="w", padx=(40, 0))

# Last Name Entry with animations
last_name_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="     Enter your last name",
    height=50,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
last_name_entry.grid(row=6, column=0, sticky="ew", pady=(0, 15), padx=(40,10))

# Email Label
email_label = ctk.CTkLabel(
    left_inner_frame,
    text="Email",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
email_label.grid(row=7, column=0, sticky="w", padx=(40, 10))

# Email Entry with animations
email_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="     Enter your email",
    height=50,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
email_entry.grid(row=8, column=0, sticky="ew", pady=(0, 15), padx=(40, 10))

# Password Label
password_label = ctk.CTkLabel(
    left_inner_frame,
    text="Password",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
password_label.grid(row=9, column=0, sticky="w", padx=(40, 10))

password_frame = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
password_frame.grid(row=10, column=0, sticky="ew", padx=(40, 10), pady=(0, 5))
password_frame.grid_columnconfigure(0, weight=1)

password_entry = ctk.CTkEntry(
    password_frame,
    placeholder_text="     Enter your password",
    show="*",
    height=50,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=15),
    border_width=2,
    border_color="#cbd3ea"
)
password_entry.grid(row=0, column=0, sticky="ew", pady=(0, 15))

def toggle_password():
    global show_password
    show_password = not show_password
    password_entry.configure(show="" if show_password else "*")
    eye_button.configure(image=eye_open_img if show_password else eye_closed_img)

eye_button = ctk.CTkButton(
    password_frame,
    text="",
    image=eye_closed_img,
    width=40,
    height=50,
    command=toggle_password,
    fg_color="transparent",
    hover_color="#d6d6d6"
)
eye_button.grid(row=0, column=1, padx=(5, 0))

# Confirm Password Label
confirm_password_label = ctk.CTkLabel(
    left_inner_frame,
    text="Confirm Password",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
confirm_password_label.grid(row=11, column=0, sticky="w", padx=(40, 10))

confirm_frame = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
confirm_frame.grid(row=12, column=0, sticky="ew", padx=(40, 10), pady=(0, 5))
confirm_frame.grid_columnconfigure(0, weight=1)

confirm_entry = ctk.CTkEntry(
    confirm_frame,
    placeholder_text="     Confirm your password",
    show="*",
    height=50,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
confirm_entry.grid(row=0, column=0, sticky="ew", padx=(0, 0), pady=(0, 15))

def toggle_confirm():
    global show_confirm_password
    show_confirm_password = not show_confirm_password
    confirm_entry.configure(show="" if show_confirm_password else "*")
    confirm_button.configure(image=eye_open_img if show_confirm_password else eye_closed_img)

confirm_button = ctk.CTkButton(
    confirm_frame,
    text="",
    image=eye_closed_img,
    width=40,
    height=50,
    command=toggle_confirm,
    fg_color="transparent",
    hover_color="#d6d6d6"
)
confirm_button.grid(row=0, column=1, padx=(5, 0))

# Sign Up Button
signup_button = ctk.CTkButton(
    left_inner_frame,
    text="Sign Up",
    fg_color="#0B1D4B",
    height=50,
    corner_radius=6,
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
signup_button.grid(row=16, column=0, sticky="ew", pady=(30, 10), padx=(130, 120))

# Sign In Link
signin_row = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
signin_row.grid(row=17, column=0, sticky="n", pady=(0, 30))

signin_label = ctk.CTkLabel(
    signin_row,
    text="Already have an account?",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="normal"),
    text_color="white"
)
signin_label.grid(row=0, column=0, padx=(10, 0))

signin_link = ctk.CTkLabel(
    signin_row,
    text=" Sign In here",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    text_color="#2f2f41",
    cursor="hand2"
)
signin_link.grid(row=0, column=1)

# Animation Functions
def animate_entry_focus(entry, is_focused):
    """Animate entry field when focused/unfocused"""
    if is_focused:
        entry.configure(border_color="#0B1D4B", border_width=3)
        # Subtle scale effect simulation
        entry.configure(height=52)
    else:
        entry.configure(border_color="#cbd3ea", border_width=2)
        entry.configure(height=50)

def animate_hover(label, is_hovered):
    """Animate label hover effects"""
    if is_hovered:
        # Darken color on hover
        label.configure(text_color="#1a1a2e")
    else:
        # Return to original color
        label.configure(text_color="#2f2f41")

def signup_click():
    print("Clicked")  # Debug print to confirm function is called
    global is_animating
    if is_animating:
        return
    # Validate all fields
    first = first_name_entry.get().strip()
    last = last_name_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    confirm = confirm_entry.get().strip()
    if not (first and last and email and password and confirm):
        show_error("All fields are required!")
        return
    if password != confirm:
        show_error("Passwords do not match!")
        return
    # Validate password strength
    if not is_strong_password(password):
        show_error("Password must be at least 8 characters with uppercase, lowercase, number, and special character!")
        return
    # Add user to database
    success = add_user(first, last, email, password, role)
    if not success:
        show_error("User already exists!")
        return
    is_animating = True
    signup_button.configure(text="Creating account...", state="disabled")
    def after_signup():
        time.sleep(1.0)
        def go_dashboard_and_close():
            show_dashboard(app, role, email)
            app.destroy()
        app.after(0, go_dashboard_and_close)
    threading.Thread(target=after_signup, daemon=True).start()

# Global variable to track current error popup
current_error_popup = None  # Track the current error popup window

def show_error(msg):
    global current_error_popup
    print(f"Showing error: {msg}")  # Debug print

    # Destroy any previous error popup
    if current_error_popup is not None:
        try:
            current_error_popup.destroy()
        except:
            pass
        current_error_popup = None

    # Create the popup window
    popup = ctk.CTkToplevel(app)
    popup.title("Error")
    popup.geometry("420x220")
    popup.resizable(False, False)
    popup.attributes("-topmost", True)
    popup.grab_set()  # Modal-like: block interaction with main window
    popup.configure(fg_color=COLOR_CARD_BG)
    popup.overrideredirect(False)  # Set to True for borderless, False for standard

    # Center the popup on the screen
    def center_popup(window, width=420, height=220):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    center_popup(popup)

    # Main container with rounded corners and border
    main_container = ctk.CTkFrame(
        popup, fg_color=COLOR_CARD_BG, corner_radius=20, border_width=2, border_color=COLOR_GRAY_200
    )
    main_container.pack(fill="both", expand=True, padx=18, pady=18)

    # Header bar with error icon and title
    header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=56)
    header_frame.pack(fill="x", padx=18, pady=(12, 0))
    header_frame.pack_propagate(False)

    icon_label = ctk.CTkLabel(header_frame, text="❌", font=FONT_H2, text_color=COLOR_ACCENT_ERROR)
    icon_label.pack(side="left", pady=10)

    title_label = ctk.CTkLabel(header_frame, text="Error", font=FONT_H2, text_color=COLOR_ACCENT_ERROR)
    title_label.pack(side="left", padx=(8, 0), pady=10)

    # Message container
    message_frame = ctk.CTkFrame(main_container, fg_color=COLOR_WHITE, corner_radius=12)
    message_frame.pack(fill="both", expand=True, padx=18, pady=(16, 10))

    error_label = ctk.CTkLabel(
        message_frame,
        text=msg,
        font=FONT_BODY,
        text_color=COLOR_ACCENT_ERROR,
        wraplength=340,
        justify="center"
    )
    error_label.pack(pady=18, padx=10)

    # Close button styled like profile popup
    def close_popup():
        try:
            popup.destroy()
        except:
            pass
        global current_error_popup
        current_error_popup = None

    close_btn = AnimatedButton(
        main_container,
        text="Close",
        fg_color=COLOR_ACCENT_ERROR,
        hover_color="#5a1e1e",
        text_color=COLOR_WHITE,
        font=FONT_BODY,
        corner_radius=10,
        height=40,
        width=120,
        command=close_popup
    )
    close_btn.pack(pady=(0, 18))

    # Auto-close after 2.5 seconds
    popup.after(2500, close_popup)

    # Track the popup globally
    current_error_popup = popup

def signin_click(event):
    app.destroy()
    subprocess.Popen([sys.executable, "LoginPage.py"])

def animate_entrance():
    """Animate the entrance of form elements"""
    def entrance_animation():
        # Start with elements invisible
        elements = [
            title, subtitle, 
            first_name_label, first_name_entry,
            last_name_label, last_name_entry,
            email_label, email_entry,
            password_label, password_frame,
            confirm_password_label, confirm_frame,
            signup_button, signin_row
        ]
        
        # Initially hide all elements
        for element in elements:
            element.grid_remove()
        
        # Animate elements appearing one by one
        for i, element in enumerate(elements):
            time.sleep(0.12)  # Delay between each element
            app.after(0, lambda el=element: el.grid())
    
    # Run animation in separate thread
    threading.Thread(target=entrance_animation, daemon=True).start()

def validate_passwords():
    """Add real-time password validation feedback"""
    password = password_entry.get()
    confirm = confirm_entry.get()
    
    if len(password) > 0 and len(confirm) > 0:
        if password == confirm:
            confirm_entry.configure(border_color="#2d5016")  # Green for match
        else:
            confirm_entry.configure(border_color="#cc3300")  # Red for mismatch

# Bind Events
# Entry focus animations
first_name_entry.bind("<FocusIn>", lambda e: animate_entry_focus(first_name_entry, True))
first_name_entry.bind("<FocusOut>", lambda e: animate_entry_focus(first_name_entry, False))

last_name_entry.bind("<FocusIn>", lambda e: animate_entry_focus(last_name_entry, True))
last_name_entry.bind("<FocusOut>", lambda e: animate_entry_focus(last_name_entry, False))

email_entry.bind("<FocusIn>", lambda e: animate_entry_focus(email_entry, True))
email_entry.bind("<FocusOut>", lambda e: animate_entry_focus(email_entry, False))

password_entry.bind("<FocusIn>", lambda e: animate_entry_focus(password_entry, True))
password_entry.bind("<FocusOut>", lambda e: animate_entry_focus(password_entry, False))

confirm_entry.bind("<FocusIn>", lambda e: animate_entry_focus(confirm_entry, True))
confirm_entry.bind("<FocusOut>", lambda e: animate_entry_focus(confirm_entry, False))

# Password validation on typing
password_entry.bind("<KeyRelease>", lambda e: validate_passwords())
confirm_entry.bind("<KeyRelease>", lambda e: validate_passwords())

# Sign in link hover and click
signin_link.bind("<Enter>", lambda e: animate_hover(signin_link, True))
signin_link.bind("<Leave>", lambda e: animate_hover(signin_link, False))
signin_link.bind("<Button-1>", signin_click)

# Eye button hover effects
eye_button.bind("<Enter>", lambda e: eye_button.configure(hover_color="#b8b8b8"))
eye_button.bind("<Leave>", lambda e: eye_button.configure(hover_color="#d6d6d6"))

confirm_button.bind("<Enter>", lambda e: confirm_button.configure(hover_color="#b8b8b8"))
confirm_button.bind("<Leave>", lambda e: confirm_button.configure(hover_color="#d6d6d6"))



# Configure button commands after functions are defined
signup_button.configure(command=signup_click)

# Start entrance animation
animate_entrance()

# Helper: Password strength validation
import re
def is_strong_password(pw):
    if len(pw) < 8:
        return False
    if not re.search(r"[A-Z]", pw):
        return False
    if not re.search(r"[a-z]", pw):
        return False
    if not re.search(r"[0-9]", pw):
        return False
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", pw):
        return False
    return True

# Run the app
app.mainloop()