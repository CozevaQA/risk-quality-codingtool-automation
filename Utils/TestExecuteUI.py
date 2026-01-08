import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sys
import os

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_FILE_DIR)
EXCEL_FILE = os.path.join(PROJECT_ROOT, "Utils", "POC Database.xlsx")
COZEVA_GREEN = "#8eab41"   # background green
FORM_BG = "#8eab41"       # form surface
ICON_PATH = os.path.join(PROJECT_ROOT, "Utils", "icon16.png")
# ─────────────────────────────────────────────
# LOAD EXCEL DATA
# ─────────────────────────────────────────────
try:
    df = pd.read_excel(EXCEL_FILE)
    df.columns = df.columns.str.strip().str.lower()
except Exception as e:
    messagebox.showerror("Error", f"Failed to load Excel file:\n{e}")
    sys.exit(1)

# ─────────────────────────────────────────────
# TKINTER ROOT
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("POC Verification Launcher")
root.geometry("570x350")
root.configure(bg=COZEVA_GREEN)
root.resizable(False, False)

# ─────────────────────────────────────────────
# VARIABLES
# ─────────────────────────────────────────────
verification_var = tk.StringVar(value="")
customer_var = tk.StringVar()
czid_var = tk.StringVar()
test_choice_var = tk.StringVar(value="")

# ─────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────
def update_customers():
    customer_combo["values"] = []
    czid_combo["values"] = []
    customer_var.set("")
    czid_var.set("")
    clear_comments()

    vf = verification_var.get()
    if not vf:
        return

    customers = sorted(
        df[df["verification field"] == vf]["customer name"].unique()
    )
    customer_combo["values"] = customers


def update_cz_ids(event=None):
    czid_combo["values"] = []
    czid_var.set("")
    clear_comments()

    vf = verification_var.get()
    cust = customer_var.get()

    if not vf or not cust:
        return

    cz_ids = (
        df[
            (df["verification field"] == vf) &
            (df["customer name"] == cust)
        ]["cz id"]
        .astype(str)
        .unique()
    )

    czid_combo["values"] = sorted(cz_ids)


def populate_comments(event=None):
    comments_text.config(state="normal", font=("Arial", 9, "bold"))
    comments_text.delete("1.0", tk.END)

    vf = verification_var.get()
    cust = customer_var.get()
    czid = czid_var.get()

    if not (vf and cust and czid):
        comments_text.config(state="disabled")
        return

    row = df[
        (df["verification field"] == vf) &
        (df["customer name"] == cust) &
        (df["cz id"].astype(str) == czid)
    ]

    if not row.empty:
        comment = row.iloc[0].get("comments", "")
        if pd.notna(comment):
            comments_text.insert(tk.END, str(comment))

    comments_text.config(state="disabled")


def clear_comments():
    comments_text.config(state="normal")
    comments_text.delete("1.0", tk.END)
    comments_text.config(state="disabled")


def on_submit():
    if not all([
        verification_var.get(),
        customer_var.get(),
        czid_var.get(),
        test_choice_var.get()
    ]):
        messagebox.showwarning("Missing Data", "Please complete all fields.")
        return

    result = [
        customer_var.get(),
        czid_var.get(),
        test_choice_var.get()
    ]

    print(result)
    root.destroy()


def on_cancel():
    root.destroy()
    sys.exit(0)

# ─────────────────────────────────────────────
# FORM CONTAINER (THIS FIXES THE UI)
# ─────────────────────────────────────────────
form = tk.Frame(root, bg=FORM_BG, padx=20, pady=20)
form.pack(padx=15, pady=15, fill="both", expand=True)

form.grid_columnconfigure(1, weight=1)

# ─────────────────────────────────────────────
# UI LAYOUT
# ─────────────────────────────────────────────

# Verification Field
tk.Label(form, text="Verification Field", bg=FORM_BG, fg="white", font=("Arial", 11, "bold")).grid(
    row=0, column=0, sticky="w", pady=(0, 5)
)

vf_frame = tk.Frame(form, bg=FORM_BG)
vf_frame.grid(row=0, column=1, sticky="w")

for val in ["Risk POC", "Quality POC", "Quality Coding Tool"]:
    tk.Radiobutton(
        vf_frame,
        text=val,
        value=val,
        variable=verification_var,
        command=update_customers,
        bg=COZEVA_GREEN,
        fg="black",
        activebackground=COZEVA_GREEN,
        activeforeground="white",
        selectcolor="white",
        highlightthickness=1,
        borderwidth=1,
        font= ("Arial", 10, "bold")
    ).pack(side="left", padx=5)

# Customer
tk.Label(form, text="Customer", bg=FORM_BG, fg="white", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", pady=10)
customer_combo = ttk.Combobox(form, textvariable=customer_var, state="readonly", width=38)
customer_combo.grid(row=1, column=1, sticky="w")
customer_combo.bind("<<ComboboxSelected>>", update_cz_ids)

# Patient CZ ID
tk.Label(form, text="Patient (CZ ID)", bg=FORM_BG, fg="white", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=10)
czid_combo = ttk.Combobox(form, textvariable=czid_var, state="readonly", width=38)
czid_combo.grid(row=2, column=1, sticky="w")
czid_combo.bind("<<ComboboxSelected>>", populate_comments)

# Comments
tk.Label(form, text="Comments", bg=FORM_BG, fg="white", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="nw", pady=10)
comments_text = tk.Text(
    form,
    height=1,
    width=38,
    wrap="word",
    state="disabled"
)
comments_text.grid(row=3, column=1, sticky="w")

# Test Choice
tk.Label(form, text="Choice of Test", bg=FORM_BG, fg="white", font=("Arial", 11, "bold")).grid(row=4, column=0, sticky="w", pady=10)
test_frame = tk.Frame(form, bg=FORM_BG)
test_frame.grid(row=4, column=1, sticky="w")

for val in ["Smoke", "Regression"]:
    tk.Radiobutton(
        test_frame,
        text=val,
        value=val,
        variable=test_choice_var,
        bg=COZEVA_GREEN,
        fg="black",
        activebackground=COZEVA_GREEN,
        activeforeground="white",
        selectcolor="white",
        highlightthickness=1,
        borderwidth=1,
        font=("Arial", 10, "bold")
    ).pack(side="left", padx=10)

# Buttons
btn_frame = tk.Frame(form, bg=FORM_BG)
btn_frame.grid(row=5, column=0, columnspan=2, sticky="n", pady=(20, 0))

ttk.Button(btn_frame, text="Cancel", command=on_cancel).pack(side="right", padx=5)
ttk.Button(btn_frame, text="Submit", command=on_submit).pack(side="right", padx=5)

# Footer-frame
logo_img = tk.PhotoImage(file=ICON_PATH)
footer_frame = tk.Frame(root, bg=COZEVA_GREEN)
footer_frame.place(
    relx=1.0,
    rely=1.0,
    anchor="se",
    x=-10,
    y=-10
)

logo_label = tk.Label(
    footer_frame,
    image=logo_img,
    bg=COZEVA_GREEN
)
logo_label.pack(side="left", padx=(0, 5))

text_label = tk.Label(
    footer_frame,
    text="© Applied Research Works Cozeva",
    bg=COZEVA_GREEN,
    fg="white",
    font=("Arial", 8, "bold")
)
text_label.pack(side="left")


# ─────────────────────────────────────────────
# START APP
# ─────────────────────────────────────────────
root.mainloop()