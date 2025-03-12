import customtkinter as ctk
from tracker import start_tracking, stop_tracking, get_total_active_seconds, toggle_pause
from reports import generate_report
from email_sender import send_email
import threading
import time

user_email = "mohamed.amin@med.mnu.edu.eg"

def open_dashboard(username):
    app = ctk.CTk()
    app.title("Dashboard")
    app.geometry("500x400")

    tracking_thread = None
    sending_reports = True

    total_time_label = ctk.CTkLabel(app, text="Total Time: 0 seconds", font=("Arial", 14))
    total_time_label.pack(pady=20)

    def update_total_time():
        while True:
            total_seconds = get_total_active_seconds()
            total_time_label.configure(text=f"Total Time: {total_seconds} seconds")
            time.sleep(1)

    def start_tracking_action():
        nonlocal tracking_thread
        tracking_thread = threading.Thread(target=start_tracking)
        tracking_thread.start()

    def stop_tracking_action():
        stop_tracking()

    def send_report_action():
        report_file = generate_report(username)
        send_email(user_email, report_file)

    def auto_send_reports():
        while sending_reports:
            report_file = generate_report(username)
            send_email(user_email, report_file)
            time.sleep(300)  # كل 5 دقائق

    # Start auto sending reports in background
    threading.Thread(target=auto_send_reports, daemon=True).start()

    # Start updating time display
    threading.Thread(target=update_total_time, daemon=True).start()

    ctk.CTkButton(app, text="Start Tracking", command=start_tracking_action).pack(pady=10)
    ctk.CTkButton(app, text="Stop Tracking", command=stop_tracking_action).pack(pady=10)
    ctk.CTkButton(app, text="Send Report Now", command=send_report_action).pack(pady=10)

    app.mainloop()
