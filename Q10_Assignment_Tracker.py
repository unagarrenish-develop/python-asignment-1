"""Q10: Tkinter assignment tracker with JSON persistence and CSV export.
Run: python Q10_Assignment_Tracker.py
"""
import csv
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DATA_FILE = "assignment_data.json"
FIELDS = ["enrollment", "name", "assignment", "status", "marks", "remarks"]

class AssignmentTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment Tracker")
        self.root.geometry("900x560")
        self.records = self.load_records()
        self.vars = {key: tk.StringVar() for key in FIELDS}
        self.vars["status"].set("Pending")
        self.build_ui()
        self.refresh()

    def load_records(self):
        if not os.path.exists(DATA_FILE): return []
        try:
            with open(DATA_FILE, encoding="utf-8") as handle:
                data = json.load(handle)
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            messagebox.showwarning("Data warning", "Could not read saved data; starting empty.")
            return []

    def save_records(self):
        temporary = DATA_FILE + ".tmp"
        with open(temporary, "w", encoding="utf-8") as handle:
            json.dump(self.records, handle, indent=2)
        os.replace(temporary, DATA_FILE)

    def build_ui(self):
        form = ttk.LabelFrame(self.root, text="Submission details", padding=8)
        form.pack(fill="x", padx=10, pady=8)
        labels = [("Enrollment", "enrollment"), ("Student name", "name"),
                  ("Assignment", "assignment"), ("Status", "status"),
                  ("Marks", "marks"), ("Remarks", "remarks")]
        for i, (label, key) in enumerate(labels):
            row, col = divmod(i, 3)
            ttk.Label(form, text=label).grid(row=row*2, column=col, sticky="w", padx=5, pady=2)
            if key == "status":
                widget = ttk.Combobox(form, textvariable=self.vars[key],
                                      values=("Pending", "Completed"), state="readonly", width=22)
            else:
                widget = ttk.Entry(form, textvariable=self.vars[key], width=25)
            widget.grid(row=row*2+1, column=col, sticky="ew", padx=5, pady=2)
        buttons = ttk.Frame(self.root); buttons.pack(fill="x", padx=10)
        ttk.Button(buttons, text="Add Submission", command=self.add_record).pack(side="left", padx=4)
        ttk.Button(buttons, text="Update Marks", command=self.update_marks).pack(side="left", padx=4)
        ttk.Button(buttons, text="Filter: All", command=lambda: self.refresh("All")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Pending", command=lambda: self.refresh("Pending")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Completed", command=lambda: self.refresh("Completed")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Export CSV", command=self.export_csv).pack(side="right", padx=4)
        columns = FIELDS
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=14)
        for column in columns:
            self.tree.heading(column, text=column.title())
            self.tree.column(column, width=130 if column not in ("remarks", "name") else 170)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.select_record)

    def validate(self):
        data = {key: self.vars[key].get().strip() for key in FIELDS}
        if not data["enrollment"] or not data["name"] or not data["assignment"]:
            raise ValueError("Enrollment, name, and assignment are required.")
        if data["status"] not in ("Pending", "Completed"):
            raise ValueError("Choose Pending or Completed status.")
        if data["marks"]:
            try: marks = float(data["marks"])
            except ValueError: raise ValueError("Marks must be numeric.")
            if marks < 0: raise ValueError("Marks cannot be negative.")
        else:
            data["marks"] = ""
        return data

    def add_record(self):
        try:
            record = self.validate()
            self.records.append(record)
            self.save_records(); self.refresh()
            messagebox.showinfo("Saved", "Submission added.")
        except (ValueError, OSError) as exc: messagebox.showerror("Invalid submission", str(exc))

    def update_marks(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select record", "Select a submission first."); return
        try:
            marks = float(self.vars["marks"].get())
            if marks < 0: raise ValueError("Marks cannot be negative.")
            values = self.tree.item(selected[0], "values")
            for record in self.records:
                if tuple(str(record.get(k, "")) for k in FIELDS) == tuple(values):
                    record["marks"] = str(marks); record["status"] = "Completed"
                    break
            self.save_records(); self.refresh()
        except (ValueError, OSError) as exc: messagebox.showerror("Invalid marks", str(exc))

    def select_record(self, _event=None):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            for key, value in zip(FIELDS, values): self.vars[key].set(value)

    def refresh(self, status="All"):
        for item in self.tree.get_children(): self.tree.delete(item)
        for record in self.records:
            if status == "All" or record.get("status") == status:
                self.tree.insert("", "end", values=[record.get(key, "") for key in FIELDS])

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")], initialfile="assignment_report.csv")
        if not path: return
        try:
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader(); writer.writerows(self.records)
            messagebox.showinfo("Exported", f"Report saved to {path}")
        except OSError as exc: messagebox.showerror("Export error", str(exc))

if __name__ == "__main__":
    root = tk.Tk()
    AssignmentTracker(root)
    root.mainloop()
