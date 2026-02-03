import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
EXCEL_FILE = r"Measure List CE OFF MY2026.xlsx"
SHEET_NAME = "MY2026"
BG_COLOR = "#8eab41"

# ─────────────────────────────────────────────
# LOAD MASTER DATA
# ─────────────────────────────────────────────
try:
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    df.columns = df.columns.str.strip().str.lower()
except Exception as e:
    messagebox.showerror("Error", f"Failed to load Excel file:\n{e}")
    raise SystemExit

df["denominator"] = pd.to_numeric(df["denominator"], errors="coerce").fillna(0)
df["customer id"] = df["customer id"].astype(str)

ALL_ABBREV = sorted(df["abbrev"].dropna().astype(str).unique())


# ─────────────────────────────────────────────
# MAIN LAUNCHER
# ─────────────────────────────────────────────
def launch_measure_selector():

    result_holder = {"result": None}

    root = tk.Tk()
    root.title("Measure Verification MY2026")
    root.geometry("900x750")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    abbrev_var = tk.StringVar()

    lob_customer_widgets = []

    # ---------- HELPERS ----------
    def clear_lob_rows():
        for row in lob_customer_widgets:
            row["frame"].destroy()
        lob_customer_widgets.clear()

    def filter_abbrev(event=None):
        typed = abbrev_var.get().lower()
        abbrev_combo["values"] = [
            a for a in ALL_ABBREV if typed in a.lower()
        ] if typed else ALL_ABBREV

    def on_abbrev_selected(event=None):
        clear_lob_rows()

        abbrev = abbrev_var.get().strip()
        if not abbrev:
            return

        subset = df[df["abbrev"].astype(str) == abbrev]

        if subset.empty:
            measure_text.config(state="normal")
            measure_text.delete("1.0", tk.END)
            measure_text.config(state="disabled")
            return

        # Show measure name at the TOP (single, consistent)
        measure_text.config(state="normal")
        measure_text.delete("1.0", tk.END)
        measure_text.insert(tk.END, str(subset.iloc[0]["measure"]))
        measure_text.config(state="disabled")

        valid_subset = subset[subset["denominator"] != 0]

        if valid_subset.empty:
            messagebox.showinfo(
                "No Valid LOBs",
                "No LOBs found where Denominator is non-zero for this measure."
            )
            return

        lobs = sorted(valid_subset["lob"].dropna().astype(str).unique())

        for idx, lob in enumerate(lobs):
            create_lob_customer_row(idx, lob, valid_subset)

        lob_canvas.yview_moveto(0)

    def create_lob_customer_row(row_index, lob, valid_subset):

        frame = tk.Frame(lob_container, bg=BG_COLOR)
        frame.grid(row=row_index, column=0, sticky="w", pady=6)

        selected_var = tk.BooleanVar(value=True)

        lob_rows = valid_subset[valid_subset["lob"].astype(str) == lob]

        # Build customer → metadata mapping
        customer_meta_map = {}
        for _, r in lob_rows.iterrows():
            customer_meta_map.setdefault(str(r["customer"]), {
                "customer_id": str(r["customer id"]),
                "domain": str(r["domain"])
            })

        customers = sorted(customer_meta_map.keys())
        cust_var = tk.StringVar(value=customers[0] if customers else "")

        # ----- UI WIDGETS PER ROW -----

        chk = tk.Checkbutton(
            frame,
            text=lob,
            variable=selected_var,
            bg=BG_COLOR,
            fg="black",
            selectcolor="white",
            activebackground=BG_COLOR,
            font=("Arial", 10, "bold"),
            width=22,
            anchor="w"
        )
        chk.grid(row=0, column=0, padx=(0, 10), sticky="w")

        cust_combo = ttk.Combobox(
            frame,
            textvariable=cust_var,
            state="readonly",
            width=40,
            values=customers
        )
        cust_combo.grid(row=0, column=1, padx=(0, 10))

        domain_label = tk.Label(
            frame,
            text="",
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            anchor="w",
            width=40
        )
        domain_label.grid(row=0, column=2, sticky="w")

        def update_domain_label(*args):
            cust = cust_var.get()
            meta = customer_meta_map.get(cust, {})
            domain_label.config(text=f"Domain: {meta.get('domain','')}")

        def toggle_row():
            if selected_var.get():
                cust_combo.configure(state="readonly")
                update_domain_label()
            else:
                cust_combo.configure(state="disabled")
                domain_label.config(text="")

        selected_var.trace_add("write", lambda *a: toggle_row())
        cust_var.trace_add("write", lambda *a: update_domain_label())

        toggle_row()

        lob_customer_widgets.append({
            "lob": lob,
            "selected_var": selected_var,
            "customer_var": cust_var,
            "customer_meta_map": customer_meta_map,
            "frame": frame
        })

    def select_all_lobs():
        for row in lob_customer_widgets:
            row["selected_var"].set(True)

    def deselect_all_lobs():
        for row in lob_customer_widgets:
            row["selected_var"].set(False)

    def on_submit():
        selected_rows = [r for r in lob_customer_widgets if r["selected_var"].get()]

        if not abbrev_var.get():
            messagebox.showwarning("Missing Data", "Select a Measure Abbreviation.")
            return

        if not selected_rows:
            messagebox.showwarning("Validation Error", "Select at least one LOB.")
            return

        # Extract single measure name from top text box
        measure_name = measure_text.get("1.0", tk.END).strip()

        lob_results = []
        for row in selected_rows:
            cust = row["customer_var"].get()
            meta = row["customer_meta_map"].get(cust, {})

            lob_results.append({
                "lob": row["lob"],
                "customer": cust,
                "customer_id": meta.get("customer_id"),
                "domain": meta.get("domain")
            })

        result_holder["result"] = {
            "abbrev": abbrev_var.get(),
            "measure": measure_name,          # SINGLE measure throughout
            "lob_customer_mapping": lob_results
        }

        root.quit()

    def on_cancel():
        result_holder["result"] = None
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_cancel)

    # ─────────────────────────────────────────────
    # UI LAYOUT
    # ─────────────────────────────────────────────
    main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    main_frame.grid_columnconfigure(1, weight=1)

    # ----- MEASURE ABBREV -----
    tk.Label(main_frame, text="Measure Abbreviation",
             bg=BG_COLOR, fg="white", font=("Arial", 11, "bold"))\
        .grid(row=0, column=0, sticky="w", pady=6)

    abbrev_combo = ttk.Combobox(
        main_frame, textvariable=abbrev_var, width=55, values=ALL_ABBREV
    )
    abbrev_combo.grid(row=0, column=1, sticky="w")
    abbrev_combo.bind("<KeyRelease>", filter_abbrev)
    abbrev_combo.bind("<<ComboboxSelected>>", on_abbrev_selected)

    # ----- MEASURE NAME AT TOP -----
    tk.Label(main_frame, text="Measure Name",
             bg=BG_COLOR, fg="white", font=("Arial", 11, "bold"))\
        .grid(row=1, column=0, sticky="nw", pady=6)

    measure_text = tk.Text(main_frame, height=2, width=90, wrap="word", state="disabled", font=("Arial",10,"bold"))
    measure_text.grid(row=1, column=1, sticky="w")

    # ----- HEADER + BUTTONS -----
    tk.Label(main_frame,
             text="Select LOBs to Execute (Non-zero Denominators)",
             bg=BG_COLOR, fg="white", font=("Arial", 12, "bold"))\
        .grid(row=2, column=0, sticky="w", pady=(15, 8))

    action_frame = tk.Frame(main_frame, bg=BG_COLOR)
    action_frame.grid(row=2, column=1, sticky="e", pady=(15, 8))

    ttk.Button(action_frame, text="Select All", command=select_all_lobs)\
        .pack(side="left", padx=5)
    ttk.Button(action_frame, text="Deselect All", command=deselect_all_lobs)\
        .pack(side="left")

    # ----- SCROLLABLE LOB LIST -----
    lob_canvas = tk.Canvas(main_frame, bg=BG_COLOR, height=520, highlightthickness=0)
    lob_canvas.grid(row=3, column=0, columnspan=2, sticky="nsew")

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=lob_canvas.yview)
    scrollbar.grid(row=3, column=2, sticky="ns")

    lob_canvas.configure(yscrollcommand=scrollbar.set)

    lob_container = tk.Frame(lob_canvas, bg=BG_COLOR)
    lob_window = lob_canvas.create_window((0, 0), window=lob_container, anchor="nw")

    lob_container.bind(
        "<Configure>",
        lambda e: lob_canvas.configure(scrollregion=lob_canvas.bbox("all"))
    )
    lob_canvas.bind(
        "<Configure>",
        lambda e: lob_canvas.itemconfig(lob_window, width=e.width)
    )

    lob_canvas.bind_all(
        "<MouseWheel>",
        lambda e: lob_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    )

    # ----- BUTTONS -----
    btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

    ttk.Button(btn_frame, text="Cancel", command=on_cancel)\
        .pack(side="right", padx=10)
    ttk.Button(btn_frame, text="Submit", command=on_submit)\
        .pack(side="right")

    root.mainloop()
    root.destroy()
    return result_holder["result"]


if __name__ == "__main__":
    result = launch_measure_selector()
    print("Returned Result:")
    print(result)

