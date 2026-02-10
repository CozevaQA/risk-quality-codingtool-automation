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
    root.geometry("900x725")
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

    def auto_resize_measure_box():
        lines = int(measure_text.index("end-1c").split(".")[0])
        new_height = max(2, min(lines, 6))
        measure_text.configure(height=new_height)

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

        measure_text.config(state="normal")
        measure_text.delete("1.0", tk.END)
        measure_text.insert(tk.END, str(subset.iloc[0]["measure"]))
        measure_text.config(state="disabled")
        auto_resize_measure_box()

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
        lob_canvas.xview_moveto(0)

    def create_lob_customer_row(row_index, lob, valid_subset):

        frame = tk.Frame(lob_container, bg=BG_COLOR)
        frame.grid(row=row_index, column=0, sticky="w", pady=6)

        selected_var = tk.BooleanVar(value=True)

        lob_rows = valid_subset[valid_subset["lob"].astype(str) == lob]

        customer_meta_map = {}
        for _, r in lob_rows.iterrows():
            customer_meta_map.setdefault(str(r["customer"]), {
                "customer_id": str(r["customer id"]),
                "measure": str(r["measure"]),
                "domain": str(r["domain"])
            })

        customers = sorted(customer_meta_map.keys())
        cust_var = tk.StringVar(value=customers[0] if customers else "")

        chk = tk.Checkbutton(
            frame,
            text=lob,
            variable=selected_var,
            bg=BG_COLOR,
            fg="black",
            selectcolor="white",
            activebackground=BG_COLOR,
            font=("Arial", 10, "bold"),
            width=20,
            anchor="w"
        )
        chk.grid(row=0, column=0, padx=(0, 10), sticky="w")

        cust_combo = ttk.Combobox(
            frame,
            textvariable=cust_var,
            state="readonly",
            width=32,
            values=customers
        )
        cust_combo.grid(row=0, column=1, padx=(0, 10))

        measure_label = tk.Label(
            frame,
            text="",
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            anchor="w",
            width=55,
            wraplength=420
        )
        measure_label.grid(row=0, column=2, padx=(0, 10), sticky="w")

        domain_label = tk.Label(
            frame,
            text="",
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            anchor="w",
            width=30
        )
        domain_label.grid(row=0, column=3, sticky="w")

        def update_labels(*args):
            cust = cust_var.get()
            meta = customer_meta_map.get(cust, {})
            measure_label.config(text=f"Measure: {meta.get('measure','')}")
            domain_label.config(text=f"Domain: {meta.get('domain','')}")

        def toggle_row():
            if selected_var.get():
                cust_combo.configure(state="readonly")
                update_labels()
            else:
                cust_combo.configure(state="disabled")
                measure_label.config(text="")
                domain_label.config(text="")

        selected_var.trace_add("write", lambda *a: toggle_row())
        cust_var.trace_add("write", lambda *a: update_labels())

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

        measure_name = measure_text.get("1.0", tk.END).strip()

        lob_results = []
        for row in selected_rows:
            cust = row["customer_var"].get()
            meta = row["customer_meta_map"].get(cust, {})

            lob_results.append({
                "lob": row["lob"],
                "customer": cust,
                "customer_id": meta.get("customer_id"),
                "measure": meta.get("measure"),
                "domain": meta.get("domain")
            })

        result_holder["result"] = {
            "abbrev": abbrev_var.get(),
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

    tk.Label(main_frame, text="Measure Abbreviation",
             bg=BG_COLOR, fg="white", font=("Arial", 11, "bold"))\
        .grid(row=0, column=0, sticky="w", pady=6)

    abbrev_combo = ttk.Combobox(
        main_frame, textvariable=abbrev_var, width=60, values=ALL_ABBREV
    )
    abbrev_combo.grid(row=0, column=1, sticky="w")
    abbrev_combo.bind("<KeyRelease>", filter_abbrev)
    abbrev_combo.bind("<<ComboboxSelected>>", on_abbrev_selected)

    tk.Label(main_frame, text="Measure Name",
             bg=BG_COLOR, fg="white", font=("Arial", 11, "bold"))\
        .grid(row=1, column=0, sticky="nw", pady=6)

    measure_text = tk.Text(
        main_frame,
        height=2,
        width=95,
        wrap="word",
        state="disabled",
        font=("Arial", 10, "bold")
    )
    measure_text.grid(row=1, column=1, sticky="w")

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

    # ─────────────────────────────────────────────
    # SCROLLABLE LOB CONTAINER (VERTICAL + HORIZONTAL)
    # ─────────────────────────────────────────────
    lob_canvas = tk.Canvas(main_frame, bg=BG_COLOR, height=500, highlightthickness=0)
    lob_canvas.grid(row=3, column=0, columnspan=2, sticky="nsew")

    v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=lob_canvas.yview)
    v_scrollbar.grid(row=3, column=2, sticky="ns")

    h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=lob_canvas.xview)
    h_scrollbar.grid(row=4, column=0, columnspan=2, sticky="ew")

    lob_canvas.configure(
        yscrollcommand=v_scrollbar.set,
        xscrollcommand=h_scrollbar.set
    )

    lob_container = tk.Frame(lob_canvas, bg=BG_COLOR)
    lob_window = lob_canvas.create_window((0, 0), window=lob_container, anchor="nw")

    def _on_frame_configure(event):
        lob_canvas.configure(scrollregion=lob_canvas.bbox("all"))

    lob_container.bind("<Configure>", _on_frame_configure)

    lob_canvas.bind_all(
        "<MouseWheel>",
        lambda e: lob_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    )

    def _on_shift_mousewheel(event):
        lob_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    lob_canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

    # Buttons
    btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
    btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

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
