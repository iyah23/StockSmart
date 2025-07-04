import customtkinter as ctk
from PIL import Image
import threading
import time
from database import add_user
from dashboard import (
    COLOR_CARD_BG, COLOR_GRAY_200, COLOR_ACCENT_ERROR, COLOR_WHITE, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    FONT_H2, FONT_BODY, AnimatedButton
)

class SignUpPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.controller = controller
        self.is_animating = False
        self.selected_role = getattr(controller, 'selected_role', 'Employee')
        # Load icons (create placeholder images if files don't exist)
        try:
            eye_open_img = ctk.CTkImage(Image.open("eye_open.png"), size=(25, 25))
            eye_closed_img = ctk.CTkImage(Image.open("eye_close.png"), size=(25, 25))
        except Exception:
            from PIL import ImageDraw
            img_open = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img_open)
            draw.ellipse([5, 8, 20, 17], fill='black')
            draw.ellipse([10, 10, 15, 15], fill='white')
            eye_open_img = ctk.CTkImage(img_open, size=(25, 25))
            img_closed = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img_closed)
            draw.line([5, 12, 20, 12], fill='black', width=2)
            eye_closed_img = ctk.CTkImage(img_closed, size=(25, 25))
        self.show_password = False
        self.show_confirm_password = False
        for col in (0, 1):
            self.grid_columnconfigure(col, weight=1, uniform="half")
        self.grid_rowconfigure(0, weight=1)
        left_frame = ctk.CTkFrame(self, fg_color="#8094c2", corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        right_frame = ctk.CTkFrame(self, fg_color="#f9f5eb", corner_radius=0)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        left_inner_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        left_inner_frame.grid(row=0, column=0, padx=25, pady=10, sticky="nsew")
        left_inner_frame.grid_rowconfigure(16, weight=1)
        left_inner_frame.grid_columnconfigure(0, weight=1)
        title = ctk.CTkLabel(
            left_inner_frame,
            text="Hi!",
            font=ctk.CTkFont(family="Instrument Sans", size=60, weight="bold"),
            text_color="#0B1D4B"
        )
        title.grid(row=1, column=0, sticky="w", padx=(40,400),  pady=(30,0))
        subtitle = ctk.CTkLabel(
            left_inner_frame,
            text="Please enter your details",
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
            text_color="white"
        )
        subtitle.grid(row=2, column=0, sticky="w", pady=(0, 10), padx=(40, 10))
        first_name_label = ctk.CTkLabel(
            left_inner_frame,
            text="First Name",
            text_color="white",
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
        )
        first_name_label.grid(row=3, column=0, padx=(40, 10), pady=(0, 4), sticky="w")
        self.first_name_entry = ctk.CTkEntry(
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
        self.first_name_entry.grid(row=4, column=0, sticky="ew", pady=(0, 15), padx=(40,10))
        last_name_label = ctk.CTkLabel(
            left_inner_frame,
            text="Last Name",
            text_color="white",
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
        )
        last_name_label.grid(row=5, column=0, sticky="w", padx=(40, 0))
        self.last_name_entry = ctk.CTkEntry(
            left_inner_frame,
            placeholder_text="     Enter your last name",
            height=50,
            corner_radius=10,
            fg_color="#cbd3ea",
            font=ctk.CTkFont(family="Instrument Sans", size=16),
            border_width=2,
            border_color="#cbd3ea"
        )
        self.last_name_entry.grid(row=6, column=0, sticky="ew", pady=(0, 15), padx=(40,10))
        email_label = ctk.CTkLabel(
            left_inner_frame,
            text="Email",
            text_color="white",
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
        )
        email_label.grid(row=7, column=0, sticky="w", padx=(40, 10))
        self.email_entry = ctk.CTkEntry(
            left_inner_frame,
            placeholder_text="     Enter your email",
            height=50,
            corner_radius=10,
            fg_color="#cbd3ea",
            font=ctk.CTkFont(family="Instrument Sans", size=16),
            border_width=2,
            border_color="#cbd3ea"
        )
        self.email_entry.grid(row=8, column=0, sticky="ew", pady=(0, 15), padx=(40, 10))
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
        self.password_entry = ctk.CTkEntry(
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
        self.password_entry.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        def toggle_password():
            self.show_password = not self.show_password
            self.password_entry.configure(show="" if self.show_password else "*")
            eye_button.configure(image=eye_open_img if self.show_password else eye_closed_img)
        eye_button = ctk.CTkButton(password_frame, text="", image=eye_closed_img, width=30, height=30, fg_color="transparent", command=toggle_password)
        eye_button.grid(row=0, column=1, padx=(5,0))
        confirm_password_label = ctk.CTkLabel(
            left_inner_frame,
            text="Confirm Password",
            text_color="white",
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
        )
        confirm_password_label.grid(row=11, column=0, sticky="w", padx=(40, 10))
        confirm_password_frame = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
        confirm_password_frame.grid(row=12, column=0, sticky="ew", padx=(40, 10), pady=(0, 5))
        confirm_password_frame.grid_columnconfigure(0, weight=1)
        self.confirm_password_entry = ctk.CTkEntry(
            confirm_password_frame,
            placeholder_text="     Confirm your password",
            show="*",
            height=50,
            corner_radius=10,
            fg_color="#cbd3ea",
            font=ctk.CTkFont(family="Instrument Sans", size=15),
            border_width=2,
            border_color="#cbd3ea"
        )
        self.confirm_password_entry.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        def toggle_confirm():
            self.show_confirm_password = not self.show_confirm_password
            self.confirm_password_entry.configure(show="" if self.show_confirm_password else "*")
            confirm_eye_button.configure(image=eye_open_img if self.show_confirm_password else eye_closed_img)
        confirm_eye_button = ctk.CTkButton(confirm_password_frame, text="", image=eye_closed_img, width=30, height=30, fg_color="transparent", command=toggle_confirm)
        confirm_eye_button.grid(row=0, column=1, padx=(5,0))
        self.error_label = None
        signup_button = ctk.CTkButton(
            left_inner_frame,
            text="Sign Up",
            height=50,
            width=280,
            corner_radius=8,
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
            fg_color="#0B1D4B",
            text_color="white",
            command=self.signup_click
        )
        signup_button.grid(row=14, column=0, sticky="ew", pady=(10, 10), padx=(40,10))
        signin_row = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
        signin_row.grid(row=15, column=0, pady=(10, 0), padx=(40,10), sticky="ew")
        signin_label = ctk.CTkLabel(signin_row, text="Already have an account?", font=ctk.CTkFont(size=16))
        signin_label.pack(side="left")
        signin_btn = ctk.CTkLabel(signin_row, text="Sign In", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0B1D4B", cursor="hand2")
        signin_btn.pack(side="left", padx=(5,0))
        signin_btn.bind("<Button-1>", lambda e: controller.show_frame("LoginPage"))

    def signup_click(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        if not (first_name and last_name and email and password and confirm_password):
            self.show_error("All fields are required!")
            return
        if password != confirm_password:
            self.show_error("Passwords do not match!")
            return
        # Add more password validation as needed
        # Add user to database
        role = getattr(self.controller, 'selected_role', 'Employee')
        result = add_user(first_name, last_name, email, password, role)
        if result == "exists":
            self.show_error("User already exists!")
            return
        if result == "error":
            self.show_error("Error creating user!")
            return
        # Set user info on the controller BEFORE navigating
        self.controller.user_email = email
        self.controller.user_role = role
        # If you have a user_id, set it as well
        self.controller.show_frame("DashboardPage")
        
    def show_error(self, msg):
        if self.error_label:
            self.error_label.destroy()
        self.error_label = ctk.CTkLabel(self, text=msg, font=ctk.CTkFont(size=16, weight="bold"), text_color="#cc3300")
        self.error_label.place(relx=0.5, rely=0.9, anchor="center")