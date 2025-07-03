import customtkinter as ctk
import threading
import time
import sys
import subprocess
from tkinter import messagebox
from app_navigation import show_signup, show_dashboard
from database import validate_user, get_user_role
from forgot_password import EmailPopup

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# App Setup
app = ctk.CTk()
app.geometry("1200x800")
app.resizable(True, True)
app.title("Login Page")

def center_window(window, width=1200, height=800):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

center_window(app, 1200, 800)

# Get selected role from command line arguments
selected_role = sys.argv[1] if len(sys.argv) > 1 else "Employee"

# Animation variables
is_animating = False

# Grid Layout
for col in (0, 1):
    app.grid_columnconfigure(col, weight=1, uniform="half")
app.grid_rowconfigure(0, weight=1)

# Left Frame
left_frame = ctk.CTkFrame(app, fg_color="#8094c2", corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew")
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

# Right Frame
right_frame = ctk.CTkFrame(app, fg_color="#f9f5eb", corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# Inner Content Frame (Left) - Centered vertically
left_inner_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
left_inner_frame.grid(row=0, column=0, padx=25, pady=0, sticky="nsew")
left_inner_frame.grid_columnconfigure(0, weight=1)

# Title
title = ctk.CTkLabel(
    left_inner_frame,
    text="Welcome back!",
    font=ctk.CTkFont(family="Instrument Sans", size=60, weight="bold"),
    text_color="#0B1D4B"
)
title.grid(row=0, column=0, pady=(150, 0), padx=(40,20), sticky="ew")

# Subtitle
subtitle = ctk.CTkLabel(
    left_inner_frame,
    text="Please enter your details",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    text_color="white"
)
subtitle.grid(row=1, column=0, pady=(0, 25), padx=(50,0), sticky="w")

# Email Label
email_label = ctk.CTkLabel(
    left_inner_frame,
    text="Email",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
email_label.grid(row=2, column=0, sticky="w", pady=(0, 4), padx=(50,0))

# Email Entry with animations
email_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="     Enter your email",
    height=50,
    width=280,
    corner_radius=8,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
email_entry.grid(row=3, column=0, sticky="ew", pady=(0, 15), padx=(50,10))

# Password Label
password_label = ctk.CTkLabel(
    left_inner_frame,
    text="Password",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
password_label.grid(row=4, column=0, sticky="w", pady=(0, 4), padx=(50,0))

# Password Entry with animations
password_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="     Enter your password",
    show="*",
    height=50,
    width=280,
    corner_radius=8,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
password_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15), padx=(50,10))

# Forgot Password with hover animation
forgot_password = ctk.CTkLabel(
    left_inner_frame,
    text="Forgot Password?",
    text_color="#2f2f41",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    cursor="hand2"
)
forgot_password.grid(row=6, column=0, sticky="e", pady=(0, 20), padx=(0,10))

def signin_click():
    """Handle sign in button click with animation"""
    global is_animating
    if is_animating:
        return
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    if not (email and password):
        show_error("All fields are required!")
        return
    user = validate_user(email, password)
    if not user:
        show_error("Invalid email or password!")
        return
    
    # Check if user's actual role matches the selected role
    actual_role = get_user_role(email)
    if actual_role and actual_role.lower() != selected_role.lower():
        messagebox.showerror("Access Denied", f"This account is registered as {actual_role}. Please go back and select the correct role.")
        return
    
    role = actual_role if actual_role else "Employee"
    user_id = user[0]  # Assuming id is the first column
    is_animating = True
    signin_button.configure(text="Signing in...", state="disabled")
    def after_signin():
        time.sleep(1.0)
        def go_dashboard_and_close():
            show_dashboard(app, str(role), email, str(user_id))
            app.destroy()
        app.after(0, go_dashboard_and_close)
    threading.Thread(target=after_signin, daemon=True).start()

def forgot_password_click(event):
    """Handle forgot password click"""
    # Open the EmailPopup for forgot password flow
    EmailPopup(app)

def signup_click(event):
    subprocess.Popen([sys.executable, "SignUpPage.py", selected_role])
    app.destroy()

def animate_entrance():
    """Animate the entrance of form elements"""
    def entrance_animation():
        # Start with elements invisible
        elements = [
            title, subtitle, email_label, email_entry,
            password_label, password_entry, forgot_password,
            signin_button, signup_row
        ]
        
        # Initially hide all elements
        for element in elements:
            element.grid_remove()
        
        # Animate elements appearing one by one
        for i, element in enumerate(elements):
            time.sleep(0.15)  # Delay between each element
            app.after(0, lambda el=element: el.grid())
    
    # Run animation in separate thread
    threading.Thread(target=entrance_animation, daemon=True).start()

def show_error(msg):
    error_label = ctk.CTkLabel(left_inner_frame, text=msg, font=ctk.CTkFont(size=16, weight="bold"), text_color="#cc3300")
    error_label.grid(row=9, column=0, pady=(10, 0))
    app.after(2000, error_label.destroy)

# Bind Events
# Email entry focus animations
email_entry.bind("<FocusIn>", lambda e: animate_entry_focus(email_entry, True))
email_entry.bind("<FocusOut>", lambda e: animate_entry_focus(email_entry, False))

# Password entry focus animations
password_entry.bind("<FocusIn>", lambda e: animate_entry_focus(password_entry, True))
password_entry.bind("<FocusOut>", lambda e: animate_entry_focus(password_entry, False))

# Forgot password hover and click
forgot_password.bind("<Enter>", lambda e: animate_hover(forgot_password, True))
forgot_password.bind("<Leave>", lambda e: animate_hover(forgot_password, False))
forgot_password.bind("<Button-1>", forgot_password_click)

# Sign Up Row
signup_row = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
signup_row.grid(row=8, column=0, sticky="", pady=(0, 0))

# Sign Up Label
signup_label = ctk.CTkLabel(
    signup_row,
    text="Don't have an account?",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="normal"),
    text_color="white"
)
signup_label.grid(row=0, column=0, padx=(25,5))

# Sign Up Link with hover animation
signup_link = ctk.CTkLabel(
    signup_row,
    text="Sign Up here",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    text_color="#2f2f41",
    cursor="hand2"
)
signup_link.grid(row=0, column=1, padx=(0, 0))

# Now you can bind events to signup_link
signup_link.bind("<Enter>", lambda e: animate_hover(signup_link, True))
signup_link.bind("<Leave>", lambda e: animate_hover(signup_link, False))
signup_link.bind("<Button-1>", signup_click)

# Now create your widgets
signin_button = ctk.CTkButton(
    left_inner_frame,
    text="Sign In",
    fg_color="#0B1D4B",
    hover_color="#162A5C",
    height=50,
    width=280,
    corner_radius=8,
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    command=signin_click
)
signin_button.grid(row=7, column=0, sticky="ew", pady=(0, 20), padx=(125,100))

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

# Start entrance animation
animate_entrance()

# Start app
app.mainloop()