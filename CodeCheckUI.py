"""
CodeCheckUI – Measure / LOB / Customer selector for CodeChecker automation.

Returns a dict:
  {
    "abbrev": "<measure abbrev>",
    "lob_customer_mapping": [
      {"lob", "customer", "customer_id", "measure", "domain"}, ...
    ]
  }
or None if the user cancels.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
EXCEL_FILE = r"Measure List CE OFF MY2026.xlsx"
SHEET_NAME = "MY2026"

# Brand / theme (Cozeva green)
BG_COLOR = "#8eab41"
BG_DARK = "#6f8a2e"
BG_PANEL = "#f4f7ec"
FG_LABEL = "#ffffff"
FG_TEXT = "#1a1a1a"
ACCENT = "#2f3d12"

WINDOW_TITLE = "Measure Verification — MY2026"
WINDOW_SIZE = "980x760"


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
    """Open the selector dialog and return the user's selection (or None)."""

    result_holder = {"result": None}

    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)
    root.configure(bg=BG_COLOR)
    root.minsize(900, 650)

    # ttk styling
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("TCombobox", padding=4)
    style.configure(
        "Accent.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(12, 6),
    )
    style.configure("TButton", font=("Segoe UI", 10), padding=(10, 5))

    abbrev_var = tk.StringVar()
    status_var = tk.StringVar(value="Select a measure abbreviation to begin.")
    lob_customer_widgets = []

    # ---------- HELPERS ----------
    def clear_lob_rows():
        for row in lob_customer_widgets:
            row["frame"].destroy()
        lob_customer_widgets.clear()
        _update_status()

    def filter_abbrev(event=None):
        typed = abbrev_var.get().lower()
        abbrev_combo["values"] = (
            [a for a in ALL_ABBREV if typed in a.lower()] if typed else ALL_ABBREV
        )

    def auto_resize_measure_box():
        lines = int(measure_text.index("end-1c").split(".")[0])
        measure_text.configure(height=max(2, min(lines, 6)))

    def _selected_count():
        return sum(1 for r in lob_customer_widgets if r["selected_var"].get())

    def _update_status(*_args):
        total = len(lob_customer_widgets)
        selected = _selected_count()
        if total == 0:
            status_var.set("Select a measure abbreviation to begin.")
        else:
            status_var.set(
                f"{selected} of {total} LOB(s) selected  ·  "
                f"Deselected rows have customer dropdown disabled."
            )

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

        # Show measure name (read-only)
        measure_text.config(state="normal")
        measure_text.delete("1.0", tk.END)
        measure_text.insert(tk.END, str(subset.iloc[0]["measure"]))
        measure_text.config(state="disabled")
        auto_resize_measure_box()

        # Only LOBs with non-zero denominator are runnable
        valid_subset = subset[subset["denominator"] != 0]
        if valid_subset.empty:
            messagebox.showinfo(
                "No Valid LOBs",
                "No LOBs found where Denominator is non-zero for this measure.",
            )
            _update_status()
            return

        lobs = sorted(valid_subset["lob"].dropna().astype(str).unique())
        for idx, lob in enumerate(lobs):
            create_lob_customer_row(idx, lob, valid_subset)

        lob_canvas.yview_moveto(0)
        lob_canvas.xview_moveto(0)
        _update_status()

    def create_lob_customer_row(row_index, lob, valid_subset):
        """One selectable LOB row: checkbox | customer combo | measure | domain."""

        frame = tk.Frame(lob_container, bg=BG_PANEL, padx=8, pady=6)
        frame.grid(row=row_index, column=0, sticky="ew", pady=3, padx=2)
        frame.grid_columnconfigure(2, weight=1)

        selected_var = tk.BooleanVar(value=True)
        lob_rows = valid_subset[valid_subset["lob"].astype(str) == lob]

        # customer → metadata map
        customer_meta_map = {}
        for _, r in lob_rows.iterrows():
            customer_meta_map.setdefault(
                str(r["customer"]),
                {
                    "customer_id": str(r["customer id"]),
                    "measure": str(r["measure"]),
                    "domain": str(r["domain"]),
                },
            )

        customers = sorted(customer_meta_map.keys())
        cust_var = tk.StringVar(value=customers[0] if customers else "")

        chk = tk.Checkbutton(
            frame,
            text=lob,
            variable=selected_var,
            bg=BG_PANEL,
            fg=FG_TEXT,
            selectcolor="white",
            activebackground=BG_PANEL,
            font=("Segoe UI", 10, "bold"),
            width=18,
            anchor="w",
            command=_update_status,
        )
        chk.grid(row=0, column=0, padx=(0, 8), sticky="w")

        cust_combo = ttk.Combobox(
            frame,
            textvariable=cust_var,
            state="readonly",
            width=28,
            values=customers,
        )
        cust_combo.grid(row=0, column=1, padx=(0, 8))

        measure_label = tk.Label(
            frame,
            text="",
            bg="white",
            fg=FG_TEXT,
            font=("Segoe UI", 9),
            anchor="w",
            width=48,
            wraplength=360,
            relief="solid",
            bd=1,
            padx=4,
            pady=2,
        )
        measure_label.grid(row=0, column=2, padx=(0, 8), sticky="ew")

        domain_label = tk.Label(
            frame,
            text="",
            bg="white",
            fg=FG_TEXT,
            font=("Segoe UI", 9),
            anchor="w",
            width=22,
            relief="solid",
            bd=1,
            padx=4,
            pady=2,
        )
        domain_label.grid(row=0, column=3, sticky="w")

        def update_labels(*_args):
            cust = cust_var.get()
            meta = customer_meta_map.get(cust, {})
            measure_label.config(text=meta.get("measure", ""))
            domain_label.config(text=meta.get("domain", ""))

        def toggle_row(*_args):
            """Disable customer dropdown (and mute labels) when LOB is unchecked."""
            if selected_var.get():
                cust_combo.configure(state="readonly")
                measure_label.config(fg=FG_TEXT, bg="white")
                domain_label.config(fg=FG_TEXT, bg="white")
                update_labels()
            else:
                # Non-selected LOBs: dropdown disabled so user cannot pick a customer
                cust_combo.configure(state="disabled")
                measure_label.config(text="—", fg="#888888", bg="#eeeeee")
                domain_label.config(text="—", fg="#888888", bg="#eeeeee")
            _update_status()

        selected_var.trace_add("write", toggle_row)
        cust_var.trace_add("write", update_labels)
        toggle_row()

        lob_customer_widgets.append({
            "lob": lob,
            "selected_var": selected_var,
            "customer_var": cust_var,
            "customer_meta_map": customer_meta_map,
            "cust_combo": cust_combo,
            "frame": frame,
        })

    def select_all_lobs():
        for row in lob_customer_widgets:
            row["selected_var"].set(True)

    def deselect_all_lobs():
        for row in lob_customer_widgets:
            row["selected_var"].set(False)

    def on_submit():
        selected_rows = [r for r in lob_customer_widgets if r["selected_var"].get()]

        if not abbrev_var.get().strip():
            messagebox.showwarning("Missing Data", "Select a Measure Abbreviation.")
            return

        if not selected_rows:
            messagebox.showwarning("Validation Error", "Select at least one LOB.")
            return

        lob_results = []
        for row in selected_rows:
            cust = row["customer_var"].get()
            meta = row["customer_meta_map"].get(cust, {})
            lob_results.append({
                "lob": row["lob"],
                "customer": cust,
                "customer_id": meta.get("customer_id"),
                "measure": meta.get("measure"),
                "domain": meta.get("domain"),
            })

        result_holder["result"] = {
            "abbrev": abbrev_var.get().strip(),
            "lob_customer_mapping": lob_results,
        }
        root.quit()

    def on_cancel():
        result_holder["result"] = None
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_cancel)

    # ─────────────────────────────────────────────
    # UI LAYOUT
    # ─────────────────────────────────────────────
    main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=16)
    main_frame.pack(fill="both", expand=True)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(4, weight=1)

    # Title bar
    title = tk.Label(
        main_frame,
        text="CodeChecker  ·  Measure Selector",
        bg=BG_COLOR,
        fg=FG_LABEL,
        font=("Segoe UI", 16, "bold"),
        anchor="w",
    )
    title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

    # Abbreviation
    tk.Label(
        main_frame,
        text="Measure Abbreviation",
        bg=BG_COLOR,
        fg=FG_LABEL,
        font=("Segoe UI", 11, "bold"),
    ).grid(row=1, column=0, sticky="w", pady=4)

    abbrev_combo = ttk.Combobox(
        main_frame, textvariable=abbrev_var, width=55, values=ALL_ABBREV
    )
    abbrev_combo.grid(row=1, column=1, sticky="w", pady=4)
    abbrev_combo.bind("<KeyRelease>", filter_abbrev)
    abbrev_combo.bind("<<ComboboxSelected>>", on_abbrev_selected)

    # Measure name (read-only)
    tk.Label(
        main_frame,
        text="Measure Name",
        bg=BG_COLOR,
        fg=FG_LABEL,
        font=("Segoe UI", 11, "bold"),
    ).grid(row=2, column=0, sticky="nw", pady=4)

    measure_text = tk.Text(
        main_frame,
        height=2,
        width=90,
        wrap="word",
        state="disabled",
        font=("Segoe UI", 10),
        bg=BG_PANEL,
        relief="solid",
        bd=1,
    )
    measure_text.grid(row=2, column=1, sticky="ew", pady=4)

    # LOB section header + select/deselect
    header_row = tk.Frame(main_frame, bg=BG_COLOR)
    header_row.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(14, 6))
    header_row.grid_columnconfigure(0, weight=1)

    tk.Label(
        header_row,
        text="Select LOBs to Execute  (non-zero denominators only)",
        bg=BG_COLOR,
        fg=FG_LABEL,
        font=("Segoe UI", 12, "bold"),
    ).grid(row=0, column=0, sticky="w")

    action_frame = tk.Frame(header_row, bg=BG_COLOR)
    action_frame.grid(row=0, column=1, sticky="e")
    ttk.Button(action_frame, text="Select All", command=select_all_lobs).pack(
        side="left", padx=4
    )
    ttk.Button(action_frame, text="Deselect All", command=deselect_all_lobs).pack(
        side="left", padx=4
    )

    # ─────────────────────────────────────────────
    # SCROLLABLE LOB LIST
    # ─────────────────────────────────────────────
    list_wrap = tk.Frame(main_frame, bg=BG_DARK, padx=1, pady=1)
    list_wrap.grid(row=4, column=0, columnspan=2, sticky="nsew")
    list_wrap.grid_columnconfigure(0, weight=1)
    list_wrap.grid_rowconfigure(1, weight=1)

    # Column headers (fixed above scroll area)
    col_header = tk.Frame(list_wrap, bg=BG_DARK)
    col_header.grid(row=0, column=0, sticky="ew")
    for col, (text, width) in enumerate([
        ("LOB", 20),
        ("Customer", 30),
        ("Measure", 48),
        ("Domain", 22),
    ]):
        tk.Label(
            col_header,
            text=text,
            bg=BG_DARK,
            fg=FG_LABEL,
            font=("Segoe UI", 9, "bold"),
            width=width,
            anchor="w",
        ).grid(row=0, column=col, padx=6, pady=4, sticky="w")

    lob_canvas = tk.Canvas(
        list_wrap, bg=BG_PANEL, highlightthickness=0, height=420
    )
    lob_canvas.grid(row=1, column=0, sticky="nsew")

    v_scrollbar = ttk.Scrollbar(
        list_wrap, orient="vertical", command=lob_canvas.yview
    )
    v_scrollbar.grid(row=1, column=1, sticky="ns")

    h_scrollbar = ttk.Scrollbar(
        main_frame, orient="horizontal", command=lob_canvas.xview
    )
    h_scrollbar.grid(row=5, column=0, columnspan=2, sticky="ew")

    lob_canvas.configure(
        yscrollcommand=v_scrollbar.set,
        xscrollcommand=h_scrollbar.set,
    )

    lob_container = tk.Frame(lob_canvas, bg=BG_PANEL)
    lob_canvas.create_window((0, 0), window=lob_container, anchor="nw")

    def _on_frame_configure(_event):
        lob_canvas.configure(scrollregion=lob_canvas.bbox("all"))

    lob_container.bind("<Configure>", _on_frame_configure)

    def _on_mousewheel(event):
        lob_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(event):
        lob_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    lob_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    lob_canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

    # Status + buttons
    status_bar = tk.Label(
        main_frame,
        textvariable=status_var,
        bg=BG_COLOR,
        fg=FG_LABEL,
        font=("Segoe UI", 9),
        anchor="w",
    )
    status_bar.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(8, 0))

    btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
    btn_frame.grid(row=7, column=0, columnspan=2, pady=(12, 0), sticky="e")

    ttk.Button(btn_frame, text="Cancel", command=on_cancel).pack(
        side="right", padx=6
    )
    ttk.Button(
        btn_frame, text="Run Validation", style="Accent.TButton", command=on_submit
    ).pack(side="right", padx=6)

    root.mainloop()
    root.destroy()
    return result_holder["result"]


if __name__ == "__main__":
    result = launch_measure_selector()
    print("Returned Result:")
    print(result)
