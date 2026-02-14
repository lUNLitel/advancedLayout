from __future__ import annotations

import shutil
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from .model import Project


class AnimaticApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Animatic Builder V1")
        self.geometry("960x620")

        self.project = Project()
        self.current_project_path: Path | None = None
        self.playing = False
        self.current_time = 0.0

        self._build_ui()

    def _build_ui(self) -> None:
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(container)
        left.pack(side="left", fill="y")

        self.timeline = tk.Listbox(left, width=46, height=28)
        self.timeline.pack(fill="y")
        self.timeline.bind("<<ListboxSelect>>", lambda _: self._load_selection())

        btn_frame = tk.Frame(left)
        btn_frame.pack(fill="x", pady=8)
        tk.Button(btn_frame, text="Add Clip", command=self.add_clip).grid(row=0, column=0, sticky="ew")
        tk.Button(btn_frame, text="Replace", command=self.replace_clip).grid(row=0, column=1, sticky="ew")
        tk.Button(btn_frame, text="Move Up", command=lambda: self.move_selected(-1)).grid(row=1, column=0, sticky="ew")
        tk.Button(btn_frame, text="Move Down", command=lambda: self.move_selected(1)).grid(row=1, column=1, sticky="ew")

        tk.Button(left, text="Save Project", command=self.save_project).pack(fill="x")
        tk.Button(left, text="Open Project", command=self.open_project).pack(fill="x")
        tk.Button(left, text="Export MP4", command=self.export_mp4).pack(fill="x", pady=(4, 0))

        right = tk.Frame(container)
        right.pack(side="left", fill="both", expand=True, padx=(16, 0))

        self.preview = tk.Label(right, text="Preview\nShot: -", bg="#202020", fg="white", width=40, height=10)
        self.preview.pack(fill="x")

        ctrl = tk.Frame(right)
        ctrl.pack(fill="x", pady=8)
        tk.Button(ctrl, text="Play/Pause", command=self.toggle_play).pack(side="left")
        self.scrubber = tk.Scale(ctrl, from_=0, to=100, orient="horizontal", command=self.scrub)
        self.scrubber.pack(side="left", fill="x", expand=True, padx=6)
        self.timecode_var = tk.StringVar(value="00:00:00")
        tk.Label(ctrl, textvariable=self.timecode_var, width=10).pack(side="left")

        meta = tk.LabelFrame(right, text="Shot")
        meta.pack(fill="both", expand=True, pady=(8, 0))

        tk.Label(meta, text="Name").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(meta)
        self.name_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(meta, text="Trim In").grid(row=1, column=0, sticky="w")
        self.trim_in_entry = tk.Entry(meta)
        self.trim_in_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(meta, text="Trim Out").grid(row=2, column=0, sticky="w")
        self.trim_out_entry = tk.Entry(meta)
        self.trim_out_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(meta, text="Comment").grid(row=3, column=0, sticky="nw")
        self.comment_text = tk.Text(meta, height=5)
        self.comment_text.grid(row=3, column=1, sticky="nsew")

        tk.Button(meta, text="Apply Metadata", command=self.apply_metadata).grid(row=4, column=1, sticky="e", pady=8)

        meta.columnconfigure(1, weight=1)
        meta.rowconfigure(3, weight=1)

    def selected_index(self) -> int | None:
        sel = self.timeline.curselection()
        if not sel:
            return None
        return sel[0]

    def add_clip(self) -> None:
        path = filedialog.askopenfilename(title="Select clip")
        if not path:
            return
        self.project.add_shot(path)
        self.refresh_timeline(select_last=True)

    def replace_clip(self) -> None:
        idx = self.selected_index()
        if idx is None:
            return
        path = filedialog.askopenfilename(title="Select replacement clip")
        if not path:
            return
        self.project.replace_media(idx, path)
        self.refresh_timeline(keep_index=idx)

    def move_selected(self, delta: int) -> None:
        idx = self.selected_index()
        if idx is None:
            return
        target = idx + delta
        if target < 0 or target >= len(self.project.shots):
            return
        self.project.move_shot(idx, target)
        self.refresh_timeline(keep_index=target)

    def refresh_timeline(self, select_last: bool = False, keep_index: int | None = None) -> None:
        self.timeline.delete(0, tk.END)
        for shot in self.project.shots:
            label = f"{shot.name} | {Path(shot.file_path).name} | {shot.duration():.2f}s"
            self.timeline.insert(tk.END, label)
        if select_last and self.project.shots:
            keep_index = len(self.project.shots) - 1
        if keep_index is not None and self.project.shots:
            self.timeline.selection_set(keep_index)
            self.timeline.activate(keep_index)
            self._load_selection()

    def _load_selection(self) -> None:
        idx = self.selected_index()
        if idx is None:
            return
        shot = self.project.shots[idx]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, shot.name)
        self.trim_in_entry.delete(0, tk.END)
        self.trim_in_entry.insert(0, str(shot.trim_in))
        self.trim_out_entry.delete(0, tk.END)
        self.trim_out_entry.insert(0, str(shot.trim_out))
        self.comment_text.delete("1.0", tk.END)
        self.comment_text.insert("1.0", shot.comment)
        self.preview.configure(text=f"Preview\nShot: {shot.name}")

    def apply_metadata(self) -> None:
        idx = self.selected_index()
        if idx is None:
            return
        shot = self.project.shots[idx]
        shot.name = self.name_entry.get().strip() or shot.name
        try:
            shot.trim_in = float(self.trim_in_entry.get())
            shot.trim_out = float(self.trim_out_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "Trim values must be numbers")
            return
        shot.comment = self.comment_text.get("1.0", tk.END).strip()
        self.refresh_timeline(keep_index=idx)

    def save_project(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".animatic.json", filetypes=[("Animatic Project", "*.animatic.json")])
        if not path:
            return
        self.project.save(path)
        self.current_project_path = Path(path)
        messagebox.showinfo("Saved", f"Project saved to {path}")

    def open_project(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Animatic Project", "*.animatic.json"), ("JSON", "*.json")])
        if not path:
            return
        self.project = Project.load(path)
        self.current_project_path = Path(path)
        self.refresh_timeline()

    def export_mp4(self) -> None:
        if not self.project.shots:
            messagebox.showwarning("No Shots", "Add shots before exporting")
            return
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            messagebox.showerror("Missing ffmpeg", "Install ffmpeg to export MP4")
            return
        output = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4", "*.mp4")])
        if not output:
            return
        concat_file = Path("timeline_concat.txt")
        concat_file.write_text("\n".join([f"file '{Path(shot.file_path).resolve()}'" for shot in self.project.shots]), encoding="utf-8")
        cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", output]
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Exported", f"Exported {output}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Export failed", "ffmpeg failed. Ensure media codecs are compatible.")

    def scrub(self, value: str) -> None:
        seconds = int(float(value))
        self.current_time = seconds
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.timecode_var.set(f"{h:02d}:{m:02d}:{s:02d}")

    def toggle_play(self) -> None:
        self.playing = not self.playing


def run() -> None:
    AnimaticApp().mainloop()
