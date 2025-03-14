import tkinter as tk
from tkinter import ttk
from playsound import playsound
import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('sessions.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                        session_name text, 
                        session_time int,
                        session_date date )''')
    conn.commit()
    conn.close()

# Create DB
create_database()

def save_session(session_name, session_time):
    conn = sqlite3.connect("sessions.db")
    cursor = conn.cursor()
    session_date = datetime.now().strftime("%d.%m.%Y %H:%M")
    cursor.execute('''INSERT INTO sessions (session_name, session_time, session_date)
                      VALUES (?, ?, ?)''', (session_name, session_time, session_date))
    conn.commit()
    conn.close()


def get_sessions():
    conn = sqlite3.connect("sessions.db")
    cursor = conn.cursor()
    # DESC
    cursor.execute('''SELECT session_name, session_time, session_date 
                      FROM sessions 
                      ORDER BY session_date DESC''')
    sessions = cursor.fetchall()
    conn.close()
    return sessions



root = tk.Tk()
root.title("Focus Timer")
root.geometry("500x500")

# Creating notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Creating Timer Tab
timerFrame = tk.Frame(notebook)
notebook.add(timerFrame, text="Timer")

text = tk.Label(timerFrame, text="Focus Timer", font=("Helvetica", 26))
text.pack(pady=5)

timerLabel = tk.Label(timerFrame, text="00:00", font=("Helvetica", 26))
timerLabel.pack(pady=20)

# Creating Frame for Buttons
buttonsFrame = tk.Frame(timerFrame)
buttonsFrame.pack()

# Creating Buttons
startButton = tk.Button(buttonsFrame, text="Start", padx=20, pady=5)
pauseButton = tk.Button(buttonsFrame, text="Pause", padx=20, pady=5)
skipButton = tk.Button(buttonsFrame, text="Skip", padx=20, pady=5)

startButton.grid(row=0, column=0, padx=10)
pauseButton.grid(row=0, column=1, padx=10)
skipButton.grid(row=0, column=2, padx=10)

# History Tab
historyFrame = tk.Frame(notebook)
notebook.add(historyFrame, text="History")

historyLabel = tk.Label(historyFrame,
                        text="Sessions History",
                        font=("Helvetica", 26),
                        pady=10)
historyLabel.pack()

# History ListBox
historyListBox = tk.Listbox(historyFrame, font=("Helvetica", 14))
historyListBox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Settings Tab
settingsFrame = tk.Frame(notebook)
notebook.add(settingsFrame, text="Settings")

settingsLabel = tk.Label(settingsFrame, text="Settings", font=("Helvetica", 26))
settingsLabel.pack(pady=10)

# Work time
workTimeLabel = tk.Label(
    settingsFrame,
    text="Work session time (minutes):",
    font=("Helvetica", 12)
)

workTimeLabel.pack(pady=2)

workTimeVar = tk.StringVar(value="25")

workSpinBox = tk.Spinbox(settingsFrame, from_=1, to=9999, textvariable=workTimeVar, font=("Helvetica", 20))
workSpinBox.pack(pady=2, padx=5)

# Break time
breakSessionTime = tk.Label(
    settingsFrame,
    text="Break session time (minutes):",
    font=("Helvetica", 12)
)

breakSessionTime.pack(pady=2)

breakTimeVar = tk.StringVar(value="5")

breakSpinBox = tk.Spinbox(settingsFrame, from_=1, to=9999, textvariable=breakTimeVar, font=("Helvetica", 20))
breakSpinBox.pack(pady=2)


class Timer:
    def __init__(self):
        self.is_running = False
        self.is_work_session = True
        self.minutes = int(workTimeVar.get())
        self.seconds = 0

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.countdown()

    def pause(self):
        self.is_running = False

    def reset(self):
        self.is_running = False
        if self.is_work_session:
            self.minutes = int(workTimeVar.get())
        else:
            self.minutes = int(breakTimeVar.get())
        self.seconds = 0
        timerLabel.config(text=f"{self.minutes:02}:{self.seconds:02}")

    def switch_session(self, play_sound=True):
        if self.is_work_session:
            session_name = "Work"
        else:
            session_name = "Break"

        session_time = self.minutes

        if self.is_work_session:
            self.is_work_session = False
            self.minutes = int(breakTimeVar.get())
        else:
            self.is_work_session = True
            self.minutes = int(workTimeVar.get())

        self.seconds = 0
        timerLabel.config(text=f"{self.minutes:02}:{self.seconds:02}")
        save_session(session_name, session_time)

        update_history_listbox()  # Update History ListBox

        if play_sound:
            playsound("session_end_sound.mp3")

    def countdown(self):
        if self.is_running:
            if self.seconds == 0 and self.minutes > 0:
                self.minutes -= 1
                self.seconds = 59
            elif self.seconds > 0:
                self.seconds -= 1

            timerLabel.config(text=f"{self.minutes:02}:{self.seconds:02}")

            # Next session if time is up
            if self.minutes == 0 and self.seconds == 0:
                self.switch_session()

            # Continue countdown
            if self.minutes > 0 or self.seconds > 0:
                root.after(1000, self.countdown)


# Creating Timer
focus_timer = Timer()


def update_settings():
    focus_timer.reset()


def update_history_listbox():
    historyListBox.delete(0, tk.END)
    sessions = get_sessions()

    for session in sessions:
        historyListBox.insert(tk.END, f"{session[0]} {session[1]} minutes {session[2]}")


update_history_listbox()  # Initial update

startButton.config(command=focus_timer.start)
pauseButton.config(command=focus_timer.pause)
skipButton.config(command=lambda: focus_timer.switch_session(play_sound=False))
saveButton = tk.Button(settingsFrame, text="Save", padx=10, pady=5, command=update_settings)
saveButton.pack(pady=5)

root.mainloop()
