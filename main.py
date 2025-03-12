import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Focus Timer")
root.geometry("500x500")

# Creating notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Creating Timer Tab
timerFrame = tk.Frame(notebook)
notebook.add(timerFrame, text="Timer")


timer = tk.Label(timerFrame, text="25:00", font=("Helvetica", 26))
timer.pack(pady=20)

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

# Settings Tab
settingsFrame = tk.Frame(notebook)
notebook.add(settingsFrame, text="Settings")

settingsLabel = tk.Label(settingsFrame, text="Settings", font=("Helvetica",26))
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

# Work and Break in MINUTES
workTime = 25
breakTime = 5

root.mainloop()