import customtkinter as ctk
from tkinter import messagebox
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import is_email_registered, update_password
import dashboard  # for color/font constants and AnimatedButton

# Use dashboard's color/font constants
COLOR_CARD_BG = dashboard.COLOR_CARD_BG
COLOR_GRAY_200 = dashboard.COLOR_GRAY_200
COLOR_MAIN_BG = dashboard.COLOR_MAIN_BG
COLOR_TEXT_PRIMARY = dashboard.COLOR_TEXT_PRIMARY
COLOR_TEXT_SECONDARY = dashboard.COLOR_TEXT_SECONDARY
COLOR_ACCENT_ERROR = dashboard.COLOR_ACCENT_ERROR
COLOR_ACCENT_SUCCESS = dashboard.COLOR_ACCENT_SUCCESS
COLOR_PRIMARY = dashboard.COLOR_PRIMARY
COLOR_PRIMARY_HOVER = dashboard.COLOR_PRIMARY_HOVER
COLOR_WHITE = dashboard.COLOR_WHITE
FONT_H2 = dashboard.FONT_H2
FONT_BODY = dashboard.FONT_BODY
FONT_SMALL = dashboard.FONT_SMALL
AnimatedButton = dashboard.AnimatedButton

# Email credentials (replace with real ones in production)
# IMPORTANT: Use an App Password, not your regular Gmail password
# Go to Google Account Settings > Security > 2-Step Verification > App passwords
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@gmail.com'  # Replace with your Gmail
SENDER_PASSWORD = 'your_app_password'  # Replace with your 16-character App Password

# Helper: Send OTP email
def send_otp_email(receiver_email, otp):
    sender_email = "aquino.rheanacerise00@gmail.com"
    app_password = "qvqrgjrpnfjczbqt"  

    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return False

# Helper: Password strength check
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

class EmailPopup(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_window()
        self.setup_ui()
        self.center_on_parent()
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.title("Forgot Password - Enter Email")
        self.geometry("400x250")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_MAIN_BG)

    def center_on_parent(self):
        self.update_idletasks()
        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        popup_width = 400
        popup_height = 250
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    def setup_ui(self):
        main_container = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=20, border_width=2, border_color=COLOR_GRAY_200)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        header = ctk.CTkLabel(main_container, text="🔒 Forgot Password", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
        header.pack(pady=(10, 20))
        self.email_entry = ctk.CTkEntry(main_container, placeholder_text="Enter your email", font=FONT_BODY, height=40)
        self.email_entry.pack(fill="x", padx=10, pady=(0, 20))
        self.next_btn = AnimatedButton(main_container, text="Next", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, text_color=COLOR_WHITE, corner_radius=8, height=40, command=self.on_next)
        self.next_btn.pack(pady=(0, 10))
        self.close_btn = AnimatedButton(main_container, text="Cancel", fg_color=COLOR_ACCENT_ERROR, hover_color="#5a1e1e", text_color=COLOR_WHITE, corner_radius=8, height=36, command=self.on_close)
        self.close_btn.pack()

    def on_next(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("Input Required", "Please enter your email.")
            return
        if not is_email_registered(email):
            messagebox.showerror("Not Found", "This email is not registered.")
            return
        otp = f"{random.randint(100000, 999999)}"
        if not send_otp_email(email, otp):
            messagebox.showerror("Email Error", "Failed to send OTP. Please try again later.")
            return
        messagebox.showinfo("OTP Sent", f"An OTP has been sent to {email}.")
        self.grab_release()
        self.destroy()
        OTPPopup(self.master, email=email, otp=otp)

    def on_close(self):
        self.grab_release()
        self.destroy()

class OTPPopup(ctk.CTkToplevel):
    def __init__(self, master, email, otp, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.email = email
        self.otp = otp
        self.setup_window()
        self.setup_ui()
        self.center_on_parent()
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.title("Forgot Password - Enter OTP")
        self.geometry("400x250")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_MAIN_BG)

    def center_on_parent(self):
        self.update_idletasks()
        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        popup_width = 400
        popup_height = 250
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    def setup_ui(self):
        main_container = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=20, border_width=2, border_color=COLOR_GRAY_200)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        header = ctk.CTkLabel(main_container, text="🔑 Enter OTP", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
        header.pack(pady=(10, 20))
        self.otp_entry = ctk.CTkEntry(main_container, placeholder_text="Enter the 6-digit OTP", font=FONT_BODY, height=40)
        self.otp_entry.pack(fill="x", padx=10, pady=(0, 20))
        self.verify_btn = AnimatedButton(main_container, text="Verify", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, text_color=COLOR_WHITE, corner_radius=8, height=40, command=self.on_verify)
        self.verify_btn.pack(pady=(0, 10))
        self.close_btn = AnimatedButton(main_container, text="Cancel", fg_color=COLOR_ACCENT_ERROR, hover_color="#5a1e1e", text_color=COLOR_WHITE, corner_radius=8, height=36, command=self.on_close)
        self.close_btn.pack()

    def on_verify(self):
        entered_otp = self.otp_entry.get().strip()
        if entered_otp == self.otp:
            self.grab_release()
            self.destroy()
            NewPasswordPopup(self.master, email=self.email)
        else:
            messagebox.showerror("Invalid OTP", "The OTP you entered is incorrect.")

    def on_close(self):
        self.grab_release()
        self.destroy()

class NewPasswordPopup(ctk.CTkToplevel):
    def __init__(self, master, email, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.email = email
        self.setup_window()
        self.setup_ui()
        self.center_on_parent()
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.title("Forgot Password - New Password")
        self.geometry("400x320")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_MAIN_BG)

    def center_on_parent(self):
        self.update_idletasks()
        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        popup_width = 400
        popup_height = 320
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    def setup_ui(self):
        main_container = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=20, border_width=2, border_color=COLOR_GRAY_200)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        header = ctk.CTkLabel(main_container, text="🔒 Set New Password", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
        header.pack(pady=(10, 20))
        self.pw_entry = ctk.CTkEntry(main_container, placeholder_text="New password", font=FONT_BODY, height=40, show="*")
        self.pw_entry.pack(fill="x", padx=10, pady=(0, 10))
        self.confirm_entry = ctk.CTkEntry(main_container, placeholder_text="Confirm password", font=FONT_BODY, height=40, show="*")
        self.confirm_entry.pack(fill="x", padx=10, pady=(0, 20))
        self.save_btn = AnimatedButton(main_container, text="Save Password", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, text_color=COLOR_WHITE, corner_radius=8, height=40, command=self.on_save)
        self.save_btn.pack(pady=(0, 10))
        self.close_btn = AnimatedButton(main_container, text="Cancel", fg_color=COLOR_ACCENT_ERROR, hover_color="#5a1e1e", text_color=COLOR_WHITE, corner_radius=8, height=36, command=self.on_close)
        self.close_btn.pack()

    def on_save(self):
        pw = self.pw_entry.get()
        confirm = self.confirm_entry.get()
        if not pw or not confirm:
            messagebox.showwarning("Input Required", "Please fill in both password fields.")
            return
        if pw != confirm:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return
        if not is_strong_password(pw):
            messagebox.showerror("Weak Password", "Password must be 8+ chars, include upper/lowercase, a number, and a special character.")
            return
        if update_password(self.email, pw):
            messagebox.showinfo("Success", "Your password has been updated.")
            self.grab_release()
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to update password. Please try again.")

    def on_close(self):
        self.grab_release()
        self.destroy() 