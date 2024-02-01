import tkinter as tk
from tkinter import messagebox
import time
from pathlib import Path
import http.client, urllib
# from pushover import init, Client

# Replace these with your Pushover API key and user key
def send_pushover_notification(api_token, user_key, message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": f"{api_token}",
        "user": f"{user_key}",
        "message": f"{message}",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
def read_keys_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        keys = {}
        for line in lines:
            key, value = line.strip().split(':')
            keys[key] = value
        return keys

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")

        self.timers = []

        # Make the "Create Timer" button big with big font
        self.create_timer_button = tk.Button(root, text="Create Timer", command=self.create_timer, font=("Helvetica", 16))
        self.create_timer_button.pack()

    def create_timer(self):
        if len(self.timers) < 5:
            timer_window = tk.Toplevel(self.root)
            timer_window.title(f"Timer {len(self.timers) + 1}")

            # Increase the size of the timer window
            timer_window.geometry("600x300")

            label = tk.Label(timer_window, text="Set Timer (seconds):", font=("Helvetica", 12))
            label.pack()

            entry_time = tk.Entry(timer_window, font=("Helvetica", 32))
            entry_time.pack()

            entry_text = tk.Entry(timer_window, font=("Helvetica", 32))
            entry_text.pack()

            time_label = tk.Label(timer_window, text="", font=("Helvetica", 14, "bold"))
            time_label.pack()

            start_button = tk.Button(timer_window, text="Start Timer", command=lambda: self.start_timer(timer_window, entry_time,entry_text, time_label), font=("Helvetica", 14))
            start_button.pack()

            self.timers.append((timer_window, entry_time,entry_text, start_button, time_label))
        else:
            messagebox.showwarning("Limit Reached", "You can only create up to three timers simultaneously.")

    def start_timer(self, timer_window, entry_time,entry_text, time_label):
        try:
            duration = int(entry_time.get())
            description = entry_text.get()
            # timer_window.withdraw()  # Hide the timer window during the timer
            self.run_timer(timer_window, duration,description, time_label)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for the timer duration.")

    def run_timer(self, timer_window, duration,description, time_label):
        for remaining_time in range(duration, 0, -1):
            # Update the time left label
            time_label.config(text=f"Time Left: {remaining_time} seconds")
            time_label.update()
            time.sleep(1)

        # When the timer completes
        
        keys = read_keys_from_file("../pushover.keys")

        api_token = keys.get("api_token")
        user_key = keys.get("user_key")
        send_pushover_notification(api_token, user_key, description)
        messagebox.showwarning("Timer Complete", f"{description}")
        # Close the timer window after the timer is complete
        timer_window.destroy()
        # self.timers.remove((timer_window, entry, start_button, time_label))


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

    