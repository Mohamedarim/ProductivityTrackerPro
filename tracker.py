import win32gui
import time
import threading
from pynput import mouse, keyboard
import json
import os
from datetime import datetime

app_times = {}
_total_active_seconds = 0
running = True
paused = False
idle_time = 0

IDLE_THRESHOLD = 180  # 3 دقائق
SAVE_FILE = 'tracking_data.json'
USERS_DATA_FILE = 'users_data.json'

current_date = datetime.now().strftime("%Y-%m-%d")
current_user_name = ""

def get_active_window():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def track_idle():
    global idle_time
    last_activity = time.time()

    def on_activity(x=None, y=None):
        nonlocal last_activity
        last_activity = time.time()

    mouse_listener = mouse.Listener(on_move=on_activity, on_click=on_activity)
    keyboard_listener = keyboard.Listener(on_press=on_activity)

    mouse_listener.start()
    keyboard_listener.start()

    while running:
        idle_time = time.time() - last_activity
        time.sleep(1)

def update_users_data():
    global app_times, _total_active_seconds, current_date, current_user_name

    user_record = {
        "date": current_date,
        "app_times": app_times,
        "total_active_seconds": _total_active_seconds
    }

    if os.path.exists(USERS_DATA_FILE):
        with open(USERS_DATA_FILE, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    else:
        users_data = {}

    users_data[current_user_name] = user_record

    with open(USERS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)

def save_data():
    data = {
        "app_times": app_times,
        "total_active_seconds": _total_active_seconds,
        "date": current_date
    }

    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    update_users_data()

def load_data():
    global app_times, _total_active_seconds, current_date
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            saved_date = data.get("date", "")
            
            today = datetime.now().strftime("%Y-%m-%d")
            if saved_date == today:
                app_times.update(data.get("app_times", {}))
                _total_active_seconds = data.get("total_active_seconds", 0)
                current_date = today
            else:
                reset_tracking()
                current_date = today

def start_tracking():
    global running, _total_active_seconds
    running = True

    idle_thread = threading.Thread(target=track_idle)
    idle_thread.daemon = True
    idle_thread.start()

    save_interval = 10
    last_save_time = time.time()

    while running:
        if paused:
            time.sleep(1)
            continue

        current_app = get_active_window()

        if idle_time < IDLE_THRESHOLD:
            if current_app:
                app_times[current_app] = app_times.get(current_app, 0) + 1
                _total_active_seconds += 1

        if time.time() - last_save_time > save_interval:
            save_data()
            last_save_time = time.time()

        time.sleep(1)

def stop_tracking():
    global running
    running = False
    save_data()

def get_total_active_seconds():
    return _total_active_seconds

def toggle_pause():
    global paused
    paused = not paused
    return paused

def reset_tracking():
    global app_times, _total_active_seconds, paused, idle_time
    app_times.clear()
    _total_active_seconds = 0
    paused = False
    idle_time = 0
    save_data()

def set_user_name(name):
    global current_user_name
    current_user_name = name

load_data()
