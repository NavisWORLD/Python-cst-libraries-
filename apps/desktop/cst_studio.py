from __future__ import annotations

import json
import math
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from cstlib import GaussianSynapse, Runtime

APP_NAME = "CST Studio"
APP_VERSION = "0.3.0"
BG = "#071018"
PANEL = "#0d1822"
PANEL_2 = "#122331"
TEXT = "#eaf8f4"
MUTED = "#89aaa2"
ACCENT = "#58f0c7"
ACCENT_2 = "#7ba7ff"


class CSTStudio(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("1080x720")
        self.minsize(900, 620)
        self.configure(bg=BG)
        self.runtime = Runtime.local(Path.home() / ".cst-studio")
        self.history: list[list[float]] = []
        self._style()
        self._build()
        self._refresh_health()

    def _style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Arial", 11))
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Arial", 24, "bold"))
        style.configure("Sub.TLabel", background=BG, foreground=MUTED, font=("Arial", 10))
        style.configure("Card.TLabel", background=PANEL, foreground=TEXT, font=("Arial", 11))
        style.configure("Accent.TButton", font=("Arial", 11, "bold"), padding=10)
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 10), font=("Arial", 10, "bold"))

    def _build(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill="x", padx=28, pady=(22, 12))
        ttk.Label(header, text="CST Studio", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Persistent state • semantic memory • synaptic affinity • CST-L builder tools",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=28, pady=(0, 22))
        self.notebook = ttk.Notebook(body)
        self.notebook.pack(fill="both", expand=True)
        self._state_tab()
        self._memory_tab()
        self._about_tab()

    def _state_tab(self) -> None:
        tab = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(tab, text="State Lab")

        controls = ttk.Frame(tab, style="Panel.TFrame")
        controls.pack(fill="x", padx=20, pady=20)
        self.message = tk.StringVar(value="music follows rhythm")
        entry = tk.Entry(
            controls,
            textvariable=self.message,
            bg=PANEL_2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Arial", 12),
        )
        entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 12))
        ttk.Button(controls, text="Evolve state", command=self._evolve, style="Accent.TButton").pack(side="left")
        ttk.Button(controls, text="Reset", command=self._reset).pack(side="left", padx=(8, 0))

        self.canvas = tk.Canvas(tab, bg=PANEL, highlightthickness=0, height=300)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=(0, 8))
        self.metrics = tk.Text(tab, height=8, bg=PANEL_2, fg=TEXT, relief="flat", font=("Courier", 10))
        self.metrics.pack(fill="x", padx=20, pady=(0, 20))
        self.metrics.configure(state="disabled")
        self._draw_state()

    def _memory_tab(self) -> None:
        tab = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(tab, text="Memory")
        wrap = ttk.Frame(tab, style="Panel.TFrame")
        wrap.pack(fill="both", expand=True, padx=20, pady=20)

        self.memory_input = tk.Text(wrap, height=5, bg=PANEL_2, fg=TEXT, insertbackground=TEXT, relief="flat", font=("Arial", 11))
        self.memory_input.pack(fill="x")
        self.memory_input.insert("1.0", "Store a durable CST memory here.")
        buttons = ttk.Frame(wrap, style="Panel.TFrame")
        buttons.pack(fill="x", pady=10)
        ttk.Button(buttons, text="Store", command=self._store_memory).pack(side="left")
        ttk.Button(buttons, text="Recall similar", command=self._recall_memory).pack(side="left", padx=(8, 0))
        self.memory_results = tk.Text(wrap, bg=BG, fg=TEXT, relief="flat", font=("Courier", 10))
        self.memory_results.pack(fill="both", expand=True)

    def _about_tab(self) -> None:
        tab = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(tab, text="Build / Health")
        box = ttk.Frame(tab, style="Panel.TFrame")
        box.pack(fill="both", expand=True, padx=24, pady=24)
        ttk.Label(box, text="CST Libraries packaged application", style="Card.TLabel", font=("Arial", 18, "bold")).pack(anchor="w")
        ttk.Label(
            box,
            text="This desktop app runs the dependency-free CST Python core locally. No account or cloud service is required.",
            style="Card.TLabel",
            wraplength=760,
        ).pack(anchor="w", pady=(12, 18))
        self.health = tk.Text(box, height=16, bg=BG, fg=TEXT, relief="flat", font=("Courier", 10))
        self.health.pack(fill="both", expand=True)
        ttk.Button(box, text="Refresh health", command=self._refresh_health).pack(anchor="w", pady=(12, 0))

    def _evolve(self) -> None:
        message = self.message.get().strip()
        if not message:
            return
        try:
            response = self.runtime.respond(message)
            self.history.append(self.runtime.state.vector())
            self.history = self.history[-20:]
            self._draw_state()
            metrics = self.runtime.state.metrics()
            extra = {"response": response, "state_metrics": metrics}
            if len(self.history) >= 3:
                diagnostics = GaussianSynapse("median").diagnostics(self.history)
                extra["kernel"] = diagnostics.__dict__
            self._set_text(self.metrics, json.dumps(extra, indent=2, default=str))
            self._refresh_health()
        except Exception as exc:
            messagebox.showerror(APP_NAME, str(exc))

    def _reset(self) -> None:
        self.runtime.state.reset()
        self.history.clear()
        self._draw_state()
        self._set_text(self.metrics, "State reset.")

    def _draw_state(self) -> None:
        self.canvas.delete("all")
        values = self.runtime.state.vector()
        width = max(self.canvas.winfo_width(), 700)
        height = max(self.canvas.winfo_height(), 280)
        pad = 30
        usable = width - 2 * pad
        bar_w = usable / max(1, len(values))
        mid = height / 2
        self.canvas.create_line(pad, mid, width - pad, mid, fill="#29404c")
        for i, value in enumerate(values):
            magnitude = min(1.0, abs(value))
            h = magnitude * (height * 0.36)
            x0 = pad + i * bar_w + 5
            x1 = pad + (i + 1) * bar_w - 5
            y0, y1 = (mid - h, mid) if value >= 0 else (mid, mid + h)
            color = ACCENT if value >= 0 else ACCENT_2
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            self.canvas.create_text((x0 + x1) / 2, height - 18, text=str(i + 1), fill=MUTED, font=("Arial", 8))

    def _store_memory(self) -> None:
        text = self.memory_input.get("1.0", "end").strip()
        if not text:
            return
        try:
            record = self.runtime.memory.store(text, salience=0.8)
            self._set_text(self.memory_results, f"Stored memory {record.id}\n\n{text}")
            self._refresh_health()
        except Exception as exc:
            messagebox.showerror(APP_NAME, str(exc))

    def _recall_memory(self) -> None:
        query = self.memory_input.get("1.0", "end").strip()
        try:
            rows = self.runtime.memory.recall(query, limit=8)
            rendered = "\n\n".join(f"score={score:.4f}\n{record.text}" for record, score in rows) or "No memories yet."
            self._set_text(self.memory_results, rendered)
        except Exception as exc:
            messagebox.showerror(APP_NAME, str(exc))

    def _refresh_health(self) -> None:
        if hasattr(self, "health"):
            payload = {"app": APP_NAME, "version": APP_VERSION, "runtime": self.runtime.health()}
            self._set_text(self.health, json.dumps(payload, indent=2, default=str))

    @staticmethod
    def _set_text(widget: tk.Text, content: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.configure(state="disabled")


if __name__ == "__main__":
    app = CSTStudio()
    app.after(150, app._draw_state)
    app.mainloop()
