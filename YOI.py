import time
import json
import os
import pythoncom
import pyWinhook as pyHook
import win32api
import win32con
import tkinter as tk
from tkinter import messagebox


class CustomInputMethod:
    def __init__(self, customs_filepath):
        self.customs = self.load_customs(customs_filepath)
        self.key_press_time = {}
        self.long_press_threshold = 0.2  # Setting the Key Trigger Duration
        self.repeat_threshold = 1.0  # seconds
        self.repeating = False

    def load_customs(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return json.load(file)
        return {}

    def on_key_down(self, event):
        key = event.Key

        # 忽略所有特殊键、组合键和Windows键
        if key in ["Back", "Lcontrol", "Rcontrol", "Lmenu", "Rmenu", "Lshift", "Rshift", "Lwin", "Rwin", "Escape",
                   "Tab", "CapsLock", "Space", "Enter", "Insert", "Delete", "Home", "End", "Prior", "Next", "Up",
                   "Down", "Left", "Right", "Snapshot", "Scroll", "Pause", "NumLock", "Num0", "Num1", "Num2", "Num3",
                   "Num4", "Num5", "Num6", "Num7", "Num8", "Num9", "Multiply", "Add", "Separator", "Subtract",
                   "Decimal", "Divide", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]:
            return True

        if key not in self.key_press_time:
            self.key_press_time[key] = time.time()
        return True

    def on_key_up(self, event):
        key = event.Key

        # 忽略所有特殊键、组合键和Windows键
        if key in ["Back", "Lcontrol", "Rcontrol", "Lmenu", "Rmenu", "Lshift", "Rshift", "Lwin", "Rwin", "Escape",
                   "Tab", "CapsLock", "Space", "Enter", "Insert", "Delete", "Home", "End", "Prior", "Next", "Up",
                   "Down", "Left", "Right", "Snapshot", "Scroll", "Pause", "NumLock", "Num0", "Num1", "Num2", "Num3",
                   "Num4", "Num5", "Num6", "Num7", "Num8", "Num9", "Multiply", "Add", "Separator", "Subtract",
                   "Decimal", "Divide", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]:
            return True

        press_duration = time.time() - self.key_press_time.get(key, 0)

        if not self.repeating:
            if press_duration < self.long_press_threshold:
                pass
            elif press_duration < self.repeat_threshold:
                self.send_input(self.customs.get(key.lower(), key))
            else:
                self.send_input(key * int(press_duration))

        if key in self.key_press_time:
            del self.key_press_time[key]
            self.repeating = False

        return True

    def send_input(self, text):
        for char in text:
            win32api.keybd_event(ord(char.upper()), 0, 0, 0)
            win32api.keybd_event(ord(char.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)

    def run(self):
        hm = pyHook.HookManager()
        hm.KeyDown = self.on_key_down
        hm.KeyUp = self.on_key_up
        hm.HookKeyboard()
        pythoncom.PumpMessages()


class App:
    def __init__(self, root, input_method):
        self.root = root
        self.root.title("Custom Input Method")
        self.input_method = input_method

        self.status_label = tk.Label(root, text="Input method is running...", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.quit_button = tk.Button(root, text="Quit", command=self.quit)
        self.quit_button.pack(pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        # Stop the input method gracefully
        messagebox.showinfo("Info", "Shutting down the input method.")
        self.root.quit()
        os._exit(0)  # Force exit to stop the input method thread


if __name__ == "__main__":
    customs_filepath = "customs.json"
    input_method = CustomInputMethod(customs_filepath)

    # Create a Tkinter window
    root = tk.Tk()
    app = App(root, input_method)

    # Run the input method in a separate thread
    import threading

    input_thread = threading.Thread(target=input_method.run)
    input_thread.daemon = True
    input_thread.start()

    # Start the Tkinter event loop
    root.mainloop()
