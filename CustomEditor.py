import tkinter as tk
from tkinter import messagebox
import json
import os

class CustomEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Custom Editor")

        self.key_label = tk.Label(master, text="Key:")
        self.key_label.grid(row=0, column=0, padx=10, pady=10)

        self.key_entry = tk.Entry(master)
        self.key_entry.grid(row=0, column=1, padx=10, pady=10)

        self.custom_label = tk.Label(master, text="Custom Texts:")
        self.custom_label.grid(row=1, column=0, padx=10, pady=10)

        self.custom_entry = tk.Entry(master)
        self.custom_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(master, text="Add Custom Texts", command=self.add_custom)
        self.add_button.grid(row=2, columnspan=2, padx=10, pady=10)

        self.save_button = tk.Button(master, text="Save Custom Texts", command=self.save_customs)
        self.save_button.grid(row=3, columnspan=2, padx=10, pady=10)

        self.customs = self.load_existing_customs()

    def load_existing_customs(self):
        if os.path.exists("customs.json"):
            with open("customs.json", 'r') as file:
                return json.load(file)
        return {}

    def add_custom(self):
        key = self.key_entry.get()
        custom_text = self.custom_entry.get()

        if key and custom_text:
            self.customs[key] = custom_text
            messagebox.showinfo("Success", f"Added custom text: {key} -> {custom_text}")
            # 清除输入框内容
            self.key_entry.delete(0, tk.END)
            self.custom_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Both key and custom text are required.")

    def save_customs(self):
        with open("customs.json", 'w') as file:
            json.dump(self.customs, file)
        messagebox.showinfo("Success", "Custom texts saved successfully.")

    def get_customs(self):
        return self.customs

if __name__ == "__main__":
    root = tk.Tk()
    editor = CustomEditor(root)
    root.mainloop()
