import tkinter as tk
from tkinter import scrolledtext
import keyboard
from pynput import mouse

class ClickerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Universal Auto Dropshot")
        self.master.geometry("400x400")

        self.create_widgets()

        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.f3_pressed = False

        # Variable to store the dropshot key
        self.dropshot_key = None
        self.setting_dropshot_key = False
        self.key_hook = None

    def create_widgets(self):
        self.toggle_var = tk.BooleanVar()
        self.toggle_var.set(False)

        self.toggle_label = tk.Label(self.master, text="Status:")
        self.toggle_label.grid(row=0, column=0, pady=10)

        self.status_label = tk.Label(self.master, text="Disabled", fg="red")
        self.status_label.grid(row=0, column=1, pady=10)

        self.toggle_button = tk.Checkbutton(self.master, variable=self.toggle_var, command=self.toggle_clicker)
        self.toggle_button.grid(row=0, column=2, pady=10)

        self.dropshot_label = tk.Label(self.master, text="Dropshot key:")
        self.dropshot_label.grid(row=1, column=0, pady=10)

        self.dropshot_entry = tk.Entry(self.master, state='readonly')
        self.dropshot_entry.grid(row=1, column=1, pady=10)

        self.set_dropshot_keybind_button = tk.Button(self.master, text="Set Dropshot Keybind", command=self.set_dropshot_keybind)
        self.set_dropshot_keybind_button.grid(row=1, column=2, pady=10)

        self.console_label = tk.Label(self.master, text="Console Output:")
        self.console_label.grid(row=2, column=0, pady=10)

        self.console_output = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=40, height=10)
        self.console_output.grid(row=3, column=0, columnspan=3, pady=10)
        self.console_output.configure(state='disabled')  # Disable text widget initially

        self.note_label = tk.Label(self.master, text="Note: Press F3 to toggle Status")
        self.note_label.grid(row=4, column=0, columnspan=3, pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_app)
        self.quit_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Bind F3 key to toggle clicker status
        keyboard.on_press_key('f3', self.toggle_f3)

    def toggle_f3(self, event):
        self.f3_pressed = not self.f3_pressed
        if self.f3_pressed:
            self.toggle_var.set(True)
            self.toggle_clicker()
            self.insert_console_text("F3 pressed: Status Enabled\n")
        else:
            self.toggle_var.set(False)
            self.toggle_clicker()
            self.insert_console_text("F3 pressed: Status Disabled\n")

    def toggle_clicker(self):
        if self.toggle_var.get():
            self.status_label.config(text="Enabled", fg="green")
        else:
            self.status_label.config(text="Disabled", fg="red")

    def set_dropshot_keybind(self):
        self.dropshot_entry.config(state='normal')  # Allow the entry to be modified
        self.dropshot_entry.delete(0, tk.END)
        self.dropshot_entry.insert(0, "Press key...")
        self.dropshot_entry.config(state='readonly')  # Disable the entry

        self.setting_dropshot_key = True
        self.insert_console_text("Press a key to set as dropshot key...\n")

        # Use a separate thread to check for key press while keeping the main loop running
        self.master.after(100, self.check_key_press)

    def check_key_press(self):
        if self.setting_dropshot_key:
            print("Press a key to set as dropshot key...")

            def on_key_event(event):
                if event.event_type == keyboard.KEY_DOWN:
                    self.dropshot_key = event.name
                    self.dropshot_entry.config(state='normal')  # Allow the entry to be modified
                    self.dropshot_entry.delete(0, tk.END)
                    self.dropshot_entry.insert(0, self.dropshot_key)
                    self.dropshot_entry.config(state='readonly')  # Disable the entry

                    self.insert_console_text(f"Dropshot key set to {self.dropshot_key}\n")
                    self.setting_dropshot_key = False

                    # Unhook the event listener after capturing the first key press
                    keyboard.unhook(on_key_event)

            # Hook the event listener for key press
            keyboard.hook(on_key_event)

        # Check again after 100 milliseconds
        self.master.after(100, self.check_key_press)

    def on_mouse_click(self, x, y, button, pressed):
        if self.toggle_var.get() and pressed and button == mouse.Button.left:
            if self.dropshot_key:
                # Simulate keypress of the dropshot key
                keyboard.press(self.dropshot_key)
                keyboard.release(self.dropshot_key)
                self.insert_console_text(f"Key {self.dropshot_key} simulated on left click\n")

    def quit_app(self):
        self.mouse_listener.stop()
        self.master.destroy()

    def insert_console_text(self, text):
        self.console_output.configure(state='normal')  # Allow text widget to be modified
        self.console_output.insert(tk.END, text)
        self.console_output.configure(state='disabled')  # Disable the text widget

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerApp(root)
    app.mouse_listener.start()
    root.mainloop()
