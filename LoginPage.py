import customtkinter as ctk
import threading
import time
from tkinter import messagebox
from database import validate_user, get_user_role
from forgot_password import EmailPopup

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.controller = controller
        self.is_animating = False
        self.selected_role = getattr(controller, 'selected_role', None) or 'Employee'

        for col in (0, 1):
            self.grid_columnconfigure(col, weight=1, uniform="half")
        self.grid_rowconfigure(0, weight=1)

        # Left Frame
        left_frame = ctk.CTkFrame(self, fg_color="#8094c2", corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # Right Frame
        right_frame = ctk.CTkFrame(self, fg_color="#f9f5eb", corner_radius=0)
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

        # Email Entry
        self.email_entry = ctk.CTkEntry(
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
        self.email_entry.grid(row=3, column=0, sticky="ew", pady=(0, 15), padx=(50,10))

        # Password Label
        password_label = ctk.CTkLabel(
            left_inner_frame,
            text="Password",
            text_color="white",
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
        )
        password_label.grid(row=4, column=0, sticky="w", pady=(0, 4), padx=(50,0))

        # Password Entry
        self.password_entry = ctk.CTkEntry(
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
        self.password_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15), padx=(50,10))

        # Forgot Password
        forgot_password = ctk.CTkLabel(
            left_inner_frame,
            text="Forgot Password?",
            text_color="#2f2f41",
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
            cursor="hand2"
        )
        forgot_password.grid(row=6, column=0, sticky="e", pady=(0, 20), padx=(0,10))
        forgot_password.bind("<Button-1>", lambda e: EmailPopup(self))

        # Sign In Button
        self.signin_button = ctk.CTkButton(
            left_inner_frame,
            text="Sign In",
            height=50,
            width=280,
            corner_radius=8,
            font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
            fg_color="#0B1D4B",
            text_color="white",
            command=self.signin_click
        )
        self.signin_button.grid(row=7, column=0, sticky="ew", pady=(0, 15), padx=(50,10))

        # Sign Up Row
        signup_row = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
        signup_row.grid(row=8, column=0, pady=(10, 0), padx=(50,10), sticky="ew")
        signup_label = ctk.CTkLabel(signup_row, text="Don't have an account?", font=ctk.CTkFont(size=16))
        signup_label.pack(side="left")
        signup_btn = ctk.CTkLabel(signup_row, text="Sign Up", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0B1D4B", cursor="hand2")
        signup_btn.pack(side="left", padx=(5,0))
        signup_btn.bind("<Button-1>", lambda e: controller.show_frame("SignUpPage"))

        self.error_label = None

    def signin_click(self):
        if self.is_animating:
            return
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not (email and password):
            self.show_error("All fields are required!")
            return
        user = validate_user(email, password)
        if not user:
            self.show_error("Invalid email or password!")
            return
        actual_role = get_user_role(email)
        selected_role = getattr(self.controller, 'selected_role', 'Employee')
        if actual_role and actual_role.lower() != selected_role.lower():
            messagebox.showerror("Access Denied", f"This account is registered as {actual_role}. Please go back and select the correct role.")
            return
        role = actual_role if actual_role else "Employee"
        user_id = user[0]  # Assuming id is the first column
        self.is_animating = True
        self.signin_button.configure(text="Signing in...", state="disabled")
        def after_signin():
            time.sleep(1.0)
            def go_dashboard():
                # Set user info on the controller BEFORE navigating
                self.controller.user_email = email
                self.controller.user_role = role
                self.controller.user_id = user_id
                self.controller.show_frame("DashboardPage")
                self.is_animating = False
                self.signin_button.configure(text="Sign In", state="normal")
            self.after(0, go_dashboard)
        threading.Thread(target=after_signin, daemon=True).start()

    def show_error(self, msg):
        if self.error_label:
            self.error_label.destroy()
        self.error_label = ctk.CTkLabel(self, text=msg, font=ctk.CTkFont(size=16, weight="bold"), text_color="#cc3300")
        self.error_label.place(relx=0.5, rely=0.9, anchor="center")