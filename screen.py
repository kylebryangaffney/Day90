import tkinter as tk
import time

class DisappearingTextApp:

    def __init__(self):
        self.init_variables()
        self.setup_window()
        self.create_widgets()
        self.display_text(self.instructional_text)  # Display the instructional text

    def init_variables(self):
        self.timer_running = False
        self.start_time = 0
        self.high_score_time = 0
        self.instructional_text = ["This app will keep your text as long as you keep typing.",
                                   "After one second of no activity, the text will be deleted.",
                                   "Start typing in the text box below."]
        self.test_lines = "Good Luck. After one second of inactivity, your work will disappear."
        self.display_lines = self.instructional_text
        self.last_keypress_time = time.time()

    def setup_window(self):
        self.window = tk.Tk()
        self.window.title("Disappearing Text App")
        self.window.minsize(600, 400)
        self.window.config(padx=30, pady=20, bg="#2C3E50")

    def create_widgets(self):
        self.create_instruction_frame()
        self.create_timer_label()
        self.create_button_frame()
        self.create_entry_frame()

    def create_instruction_frame(self):
        self.instruction_frame = tk.Frame(self.window, bg='#2C3E50')
        self.instruction_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.instruction_frame.grid_rowconfigure(0, weight=1)
        self.instruction_frame.grid_columnconfigure(0, weight=1)

        self.text_widget = tk.Text(
            self.instruction_frame, font=('Arial', 14), bg='#34495E', fg='white',
            wrap="word", width=60, height=4, padx=10, pady=10, bd=0
        )
        self.text_widget.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.text_widget.insert("end", "\n".join(self.instructional_text))
        self.text_widget.config(state="disabled")

    def create_timer_label(self):
        self.timer_label = tk.Label(
            self.window, font=('Arial', 24), text="Time: 00:00", bg='#2C3E50', fg='white', pady=10
        )
        self.timer_label.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.high_score_label = tk.Label(
            self.window, font=('Arial', 24), text="High Score: 00:00", bg='#2C3E50', fg='white', pady=10
        )
        self.high_score_label.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def create_button_frame(self):
        button_frame = tk.Frame(self.window, bg='#2C3E50')
        button_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        reset_button = tk.Button(
            button_frame, text="Reset", command=self.reset_timer, bg='#E74C3C', fg='white',
            font=('Arial', 14), padx=10, pady=5, bd=0, relief="raised", overrelief="ridge"
        )
        reset_button.grid(row=0, column=0, padx=10, pady=10)

    def create_entry_frame(self):
        self.entry_frame = tk.Frame(self.window, bg='#2C3E50')
        self.entry_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.entry_frame.grid_rowconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_label = tk.Label(
            self.entry_frame, font=('Arial', 18), text="Please enter text:", bg='#2C3E50', fg='white', pady=10
        )
        self.entry_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.entry_box = tk.Text(
            self.entry_frame, font=('Arial', 14), bg='#34495E', fg='white',
            wrap="word", width=70, height=15, padx=10, pady=10, bd=0
        )
        self.entry_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.entry_box.bind("<KeyRelease>", self.reset_keypress_timer)  # Bind key release event to reset timer

    def reset_timer(self):
        if self.timer_running:
            self.window.after_cancel(self.timer)
            self.timer_running = False
        self.timer_label.config(text="Time: 00:00")
        self.entry_box.delete("1.0", tk.END)
        self.display_text(self.instructional_text)
        self.high_score_time = max(self.high_score_time, int(time.time() - self.start_time))
        self.high_score_label.config(text=f"High Score: {self.format_time(self.high_score_time)}")

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {self.format_time(elapsed_time)}")
            if time.time() - self.last_keypress_time > 1:
                self.clear_text()
            else:
                self.timer = self.window.after(100, self.update_timer)  # Update every 100 ms instead of 1000 ms

    def clear_text(self):
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", self.test_lines)
        self.text_widget.config(state="disabled")
        self.entry_box.delete("1.0", tk.END)
        self.high_score_time = max(self.high_score_time, int(time.time() - self.start_time))
        self.high_score_label.config(text=f"High Score: {self.format_time(self.high_score_time)}")
        self.timer_running = False

    def display_text(self, lines):
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        for line in lines:
            self.text_widget.insert("end", line + "\n")
        self.text_widget.config(state="disabled")

    def reset_keypress_timer(self, event):
        if not self.timer_running:
            self.start_timer()
        self.last_keypress_time = time.time()

    def start_timer(self):
        self.timer_running = True
        self.start_time = time.time()
        self.last_keypress_time = self.start_time
        self.display_test_lines()
        self.update_timer()

    def display_test_lines(self):
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", self.test_lines)
        self.text_widget.config(state="disabled")

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def start_mainloop(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = DisappearingTextApp()
    app.start_mainloop()
