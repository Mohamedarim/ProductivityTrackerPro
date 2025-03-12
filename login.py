import customtkinter as ctk
from dashboard import open_dashboard
from admin_dashboard import open_admin_dashboard

users = {
    "admin": "admin123",
    "user1": "userpass"
}

def start_login():
    app = ctk.CTk()
    app.title("Login")
    app.geometry("400x300")

    ctk.CTkLabel(app, text="Username:").pack(pady=10)
    username_entry = ctk.CTkEntry(app)
    username_entry.pack(pady=5)

    ctk.CTkLabel(app, text="Password:").pack(pady=10)
    password_entry = ctk.CTkEntry(app, show="*")
    password_entry.pack(pady=5)

    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        if username in users and users[username] == password:
            app.destroy()
            if username == "admin":
                open_admin_dashboard()
            else:
                open_dashboard(username)
        else:
            ctk.CTkLabel(app, text="Invalid Credentials", text_color="red").pack()

    ctk.CTkButton(app, text="Login", command=verify_login).pack(pady=20)

    app.mainloop()
