import customtkinter as ctk
from StartPage import StartPage
from LoginPage import LoginPage
from SignUpPage import SignUpPage
from dashboard import DashboardPage
from database import initialize_database

initialize_database()

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSmart")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.center_window()
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, SignUpPage, LoginPage, DashboardPage):
            page_name = F.__name__
            frame = F(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if page_name == "DashboardPage":
            # Destroy the old dashboard if it exists
            if frame is not None:
                frame.destroy()
            # Recreate with updated user info
            from dashboard import DashboardPage
            frame = DashboardPage(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        if frame is not None:
            frame.tkraise()

    def refresh_all_pages(self):
        dashboard = self.frames.get("DashboardPage")
        if dashboard:
            if hasattr(dashboard, "inventory_page"):
                dashboard.inventory_page.refresh_data()
            if hasattr(dashboard, "items_page"):
                dashboard.items_page.refresh_data()
            if hasattr(dashboard, "history_logs"):
                dashboard.history_logs.refresh_data()

    def center_window(self):
        """Center the application window on the screen"""
        # Update window to ensure we have the correct dimensions
        self.update_idletasks()
        
        # Get window dimensions
        window_width = 1200
        window_height = 800
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()