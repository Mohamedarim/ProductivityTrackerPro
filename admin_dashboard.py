import customtkinter as ctk
import json

def open_admin_dashboard():
    app = ctk.CTk()
    app.title("Admin Dashboard")
    app.geometry("500x400")

    users_data_file = "users_data.json"

    def load_users_data():
        with open(users_data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def refresh_data():
        data = load_users_data()
        display_text = ""
        for user, info in data.items():
            display_text += f"User: {user}\nDate: {info['date']}\nTotal Active Seconds: {info['total_active_seconds']}\n\n"
        textbox.delete("1.0", "end")
        textbox.insert("1.0", display_text)

    ctk.CTkButton(app, text="Refresh Reports", command=refresh_data).pack(pady=10)

    textbox = ctk.CTkTextbox(app, width=400, height=300)
    textbox.pack(pady=10)

    app.mainloop()
