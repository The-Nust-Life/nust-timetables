import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule Event Generator")

        self.entries = []

        self.day_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.module_var = tk.StringVar()
        self.staff_var = tk.StringVar()
        self.room_var = tk.StringVar()

        ttk.Label(root, text="Select Day:").grid(row=0, column=0, padx=10, pady=5)
        self.day_dropdown = ttk.Combobox(root, textvariable=self.day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.day_dropdown.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="Time Slot (e.g., 07:30 - 09:30):").grid(row=1, column=0, padx=10, pady=5)
        self.time_entry = ttk.Entry(root, textvariable=self.time_var)
        self.time_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(root, text="Module:").grid(row=2, column=0, padx=10, pady=5)
        self.module_entry = ttk.Entry(root, textvariable=self.module_var)
        self.module_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(root, text="Staff:").grid(row=3, column=0, padx=10, pady=5)
        self.staff_entry = ttk.Entry(root, textvariable=self.staff_var)
        self.staff_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(root, text="Room:").grid(row=4, column=0, padx=10, pady=5)
        self.room_entry = ttk.Entry(root, textvariable=self.room_var)
        self.room_entry.grid(row=4, column=1, padx=10, pady=5)

        self.add_button = ttk.Button(root, text="Add Entry", command=self.add_entry)
        self.add_button.grid(row=5, column=0, padx=10, pady=10)

        self.done_button = ttk.Button(root, text="Generate File", command=self.generate_file)
        self.done_button.grid(row=5, column=1, padx=10, pady=10)

    def add_entry(self):
        day = self.day_var.get()
        time_slot = self.time_var.get()
        module = self.module_var.get()
        staff = self.staff_var.get()
        room = self.room_var.get()

        if not all([day, time_slot, module, staff, room]):
            messagebox.showerror("Input Error", "Please fill in all fields")
            return

        start_time, end_time = time_slot.split('-')
        start_time = start_time.strip()
        end_time = end_time.strip()

        start_datetime = datetime.strptime(start_time, "%H:%M")
        end_datetime = datetime.strptime(end_time, "%H:%M")

        self.entries.append({
            'day': day,
            'start_time': start_datetime,
            'end_time': end_datetime,
            'module': module,
            'staff': staff,
            'room': room
        })

        messagebox.showinfo("Success", "Entry added successfully")
        self.clear_fields()

    def generate_file(self):
        with open("schedule_output.txt", 'w') as file:
            for entry in self.entries:
                start_str = entry['start_time'].strftime("%H%M00")
                end_str = entry['end_time'].strftime("%H%M00")
                file.write(f"BEGIN:VEVENT\n")
                file.write(f"SUMMARY:{entry['module']}\n")
                file.write(f"LOCATION:{entry['room']}\n")
                file.write(f"DESCRIPTION:Staff: {entry['staff']}\n")
                file.write(f"RRULE:FREQ=WEEKLY;UNTIL=20251020T000000Z\n")
                file.write(f"DTSTART:20250106T{start_str}\n")
                file.write(f"DTEND:20250106T{end_str}\n")
                file.write(f"END:VEVENT\n\n")

        messagebox.showinfo("Success", "Schedule saved to schedule_output.txt")

    def clear_fields(self):
        self.day_var.set("")
        self.time_var.set("")
        self.module_var.set("")
        self.staff_var.set("")
        self.room_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()
