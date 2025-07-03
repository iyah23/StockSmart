import customtkinter as ctk

# Import your page/frame classes (to be implemented/refactored as CTkFrame subclasses)
# from StartPage import StartPage
# from SignUpPage import SignUpPage
# from LoginPage import LoginPage
# from dashboard import DashboardPage

# Placeholder frame classes for demonstration
class StartPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        label = ctk.CTkLabel(self, text="Start Page", font=("Arial", 32))
        label.pack(pady=50)
        # Example navigation button
        signup_btn = ctk.CTkButton(self, text="Go to Sign Up", command=lambda: controller.show_frame("SignUpPage"))
        signup_btn.pack(pady=10)
        signin_btn = ctk.CTkButton(self, text="Go to Sign In", command=lambda: controller.show_frame("LoginPage"))
        signin_btn.pack(pady=10)

class SignUpPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        label = ctk.CTkLabel(self, text="Sign Up Page", font=("Arial", 32))
        label.pack(pady=50)
        back_btn = ctk.CTkButton(self, text="Back to Start", command=lambda: controller.show_frame("StartPage"))
        back_btn.pack(pady=10)
        dashboard_btn = ctk.CTkButton(self, text="Go to Dashboard", command=lambda: controller.show_frame("DashboardPage"))
        dashboard_btn.pack(pady=10)

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        label = ctk.CTkLabel(self, text="Login Page", font=("Arial", 32))
        label.pack(pady=50)
        back_btn = ctk.CTkButton(self, text="Back to Start", command=lambda: controller.show_frame("StartPage"))
        back_btn.pack(pady=10)
        dashboard_btn = ctk.CTkButton(self, text="Go to Dashboard", command=lambda: controller.show_frame("DashboardPage"))
        dashboard_btn.pack(pady=10)

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        label = ctk.CTkLabel(self, text="Dashboard Page", font=("Arial", 32))
        label.pack(pady=50)
        back_btn = ctk.CTkButton(self, text="Log Out", command=lambda: controller.show_frame("StartPage"))
        back_btn.pack(pady=10)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSmart")
        self.geometry("1200x800")
        self.resizable(True, True)
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, SignUpPage, LoginPage, DashboardPage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 