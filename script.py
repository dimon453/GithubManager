#!/usr/bin/env python3
"""
GitHub Collaborator Adder — GUI (tkinter, Windows 10)
Цветовая схема: фон #0E0E0B, акцент #AFE607
"""

import json
import os
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
import certifi
import tkinter as tk
from tkinter import filedialog, ttk

# ── константы ─────────────────────────────────────────────────────────────────

BG       = "#0E0E0B"
ACCENT   = "#AFE607"
FG       = "#E8E8E8"
BG2      = "#1A1A16"
BG3      = "#252520"
RED      = "#FF4C4C"
FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
FONT_BIG = ("Segoe UI", 13, "bold")

PERMISSION_CHOICES = ["pull", "push", "maintain", "triage", "admin"]
USERDATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "USERDATA.json")
SSL_CONTEXT   = ssl.create_default_context(cafile=certifi.where())

# ── USERDATA ──────────────────────────────────────────────────────────────────

def load_userdata() -> dict:
    if os.path.isfile(USERDATA_FILE):
        try:
            with open(USERDATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_userdata(username: str, token: str):
    with open(USERDATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"github_username": username, "github_token": token},
                  f, ensure_ascii=False, indent=2)

# ── GitHub API ────────────────────────────────────────────────────────────────

def add_collaborator(owner, repo, username, token, permission) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}/collaborators/{username}"
    payload = json.dumps({"permission": permission}).encode()
    req = urllib.request.Request(
        url, data=payload, method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, context=SSL_CONTEXT) as resp:
            return {"status": resp.status, "ok": True, "body": resp.read().decode()}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "ok": False, "body": e.read().decode()}

# ── GUI ───────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitHub Collaborator Adder")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._set_icon()

        self.userdata = load_userdata()

        self._build_ui()
        self._load_saved()

    # ── иконка ────────────────────────────────────────────────────────────────
    def _set_icon(self):
        try:
            ico = tk.PhotoImage(width=1, height=1)
            self.iconphoto(True, ico)
        except Exception:
            pass

    # ── стили ─────────────────────────────────────────────────────────────────
    def _entry(self, parent, textvariable, show=""):
        e = tk.Entry(
            parent, textvariable=textvariable, show=show,
            bg=BG3, fg=FG, insertbackground=ACCENT,
            relief="flat", font=FONT,
            highlightthickness=1, highlightcolor=ACCENT,
            highlightbackground="#333330",
        )
        return e

    def _label(self, parent, text, bold=False):
        return tk.Label(parent, text=text, bg=BG,
                        fg=ACCENT if bold else FG,
                        font=FONT_B if bold else FONT)

    def _btn(self, parent, text, cmd, small=False):
        b = tk.Button(
            parent, text=text, command=cmd,
            bg=ACCENT, fg=BG, activebackground="#c8f010",
            activeforeground=BG, font=FONT_B if not small else FONT,
            relief="flat", cursor="hand2",
            padx=10 if not small else 6, pady=4,
        )
        return b

    # ── построение UI ─────────────────────────────────────────────────────────
    def _build_ui(self):
        pad = {"padx": 20, "pady": 6}

        # заголовок
        tk.Label(self, text="GitHub Collaborator Adder",
                 bg=BG, fg=ACCENT, font=FONT_BIG).pack(pady=(18, 2))
        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x", padx=20, pady=(0, 10))

        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", **pad)
        form.columnconfigure(1, weight=1)

        def row(r, label):
            self._label(form, label).grid(row=r, column=0, sticky="w",
                                           padx=(0, 12), pady=5)

        # — файл —
        row(0, "Файл с никами")
        self.var_file = tk.StringVar()
        file_frame = tk.Frame(form, bg=BG)
        file_frame.grid(row=0, column=1, sticky="ew", pady=5)
        file_frame.columnconfigure(0, weight=1)
        self._entry(file_frame, self.var_file).grid(row=0, column=0, sticky="ew", ipady=4)
        self._btn(file_frame, "Обзор", self._browse, small=True)\
            .grid(row=0, column=1, padx=(6, 0))

        # — репозиторий —
        row(1, "Репозиторий (OWNER/REPO)")
        self.var_repo = tk.StringVar()
        self._entry(form, self.var_repo).grid(row=1, column=1, sticky="ew",
                                               ipady=4, pady=5)

        # — username —
        row(2, "GitHub Username")
        self.var_user = tk.StringVar()
        self._entry(form, self.var_user).grid(row=2, column=1, sticky="ew",
                                               ipady=4, pady=5)

        # — токен —
        row(3, "GitHub Token")
        self.var_token = tk.StringVar()
        self._entry(form, self.var_token).grid(row=3, column=1, sticky="ew",
                                                ipady=4, pady=5)

        # — permission —
        row(4, "Разрешение")
        self.var_perm = tk.StringVar(value="push")
        perm_frame = tk.Frame(form, bg=BG)
        perm_frame.grid(row=4, column=1, sticky="w", pady=5)
        for p in PERMISSION_CHOICES:
            tk.Radiobutton(
                perm_frame, text=p, variable=self.var_perm, value=p,
                bg=BG, fg=FG, selectcolor=BG2,
                activebackground=BG, activeforeground=ACCENT,
                font=FONT,
            ).pack(side="left", padx=(0, 10))

        # — чекбокс сохранить —
        self.var_save = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self, text="Сохранить username и токен в USERDATA.json",
            variable=self.var_save,
            bg=BG, fg=FG, selectcolor=BG2,
            activebackground=BG, activeforeground=ACCENT,
            font=FONT,
        ).pack(anchor="w", padx=20, pady=(0, 4))

        # — кнопка запуска —
        self._btn(self, "▶  Добавить collaborators", self._run)\
            .pack(fill="x", padx=20, pady=(4, 10), ipady=6)

        # — прогресс-бар —
        self.progress = ttk.Progressbar(self, mode="determinate", length=400)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TProgressbar",
                        troughcolor=BG3, background=ACCENT,
                        bordercolor=BG, lightcolor=ACCENT, darkcolor=ACCENT)
        self.progress.pack(fill="x", padx=20, pady=(0, 6))

        # — лог —
        log_frame = tk.Frame(self, bg=BG2,
                             highlightbackground=ACCENT, highlightthickness=1)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self.log = tk.Text(
            log_frame, bg=BG2, fg=FG, font=("Consolas", 9),
            relief="flat", state="disabled",
            wrap="word", height=12,
        )
        sb = tk.Scrollbar(log_frame, command=self.log.yview, bg=BG3,
                          troughcolor=BG3, relief="flat")
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        sb.pack(side="right", fill="y")

        # — футер —
        tk.Label(self, text="Proudly made by Popov Dmitrii, CR-253",
                 bg=BG, fg="#555550", font=("Segoe UI", 8)).pack(pady=(0, 10))

        # теги цвета в логе
        self.log.tag_config("ok",      foreground=ACCENT)
        self.log.tag_config("err",     foreground=RED)
        self.log.tag_config("info",    foreground=FG)
        self.log.tag_config("heading", foreground=ACCENT, font=FONT_B)

    # ── загрузить сохранённые данные ──────────────────────────────────────────
    def _load_saved(self):
        self.var_user.set(self.userdata.get("github_username", ""))
        self.var_token.set(self.userdata.get("github_token", ""))

    # ── обзор файла ───────────────────────────────────────────────────────────
    def _browse(self):
        path = filedialog.askopenfilename(
            title="Выбери txt-файл с никами",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            self.var_file.set(path)

    # ── лог-хелперы ───────────────────────────────────────────────────────────
    def _log(self, text, tag="info"):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n", tag)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _log_clear(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    # ── запуск ────────────────────────────────────────────────────────────────
    def _run(self):
        file_path = self.var_file.get().strip()
        repo_raw  = self.var_repo.get().strip()
        gh_user   = self.var_user.get().strip()
        token     = self.var_token.get().strip()
        perm      = self.var_perm.get()

        # валидация
        errors = []
        if not file_path:
            errors.append("Укажите путь к файлу с никами.")
        elif not os.path.isfile(file_path):
            errors.append(f"Файл не найден: {file_path}")
        if not repo_raw or len(repo_raw.split("/")) != 2:
            errors.append("Репозиторий должен быть в формате OWNER/REPO.")
        if not gh_user:
            errors.append("Укажите GitHub username.")
        if not token:
            errors.append("Укажите GitHub Token.")
        if errors:
            self._log_clear()
            for e in errors:
                self._log("⚠  " + e, "err")
            return

        owner, repo = repo_raw.split("/")

        with open(file_path, encoding="utf-8") as f:
            usernames = [l.strip() for l in f
                         if l.strip() and not l.strip().startswith("#")]
        if not usernames:
            self._log_clear()
            self._log("⚠  Файл пуст или не содержит ников.", "err")
            return

        # сохранить данные
        saved_user  = self.userdata.get("github_username", "")
        saved_token = self.userdata.get("github_token", "")
        if self.var_save.get() and (gh_user != saved_user or token != saved_token):
            save_userdata(gh_user, token)
            self.userdata = {"github_username": gh_user, "github_token": token}

        # запустить в потоке
        threading.Thread(
            target=self._worker,
            args=(owner, repo, token, perm, usernames),
            daemon=True,
        ).start()

    def _worker(self, owner, repo, token, perm, usernames):
        self._log_clear()
        self._log(f"Репозиторий : {owner}/{repo}", "heading")
        self._log(f"Разрешение  : {perm}", "heading")
        self._log(f"Всего ников : {len(usernames)}\n", "heading")

        self.progress["maximum"] = len(usernames)
        self.progress["value"]   = 0

        ok_count = fail_count = 0

        for i, username in enumerate(usernames, 1):
            result = add_collaborator(owner, repo, username, token, perm)
            if result["ok"]:
                tag_text = "приглашение отправлено" if result["status"] == 201 \
                           else "уже collaborator"
                self._log(f"  ✓  {username:<28}  [{result['status']}] {tag_text}", "ok")
                ok_count += 1
            else:
                try:
                    msg = json.loads(result["body"]).get("message", result["body"])
                except Exception:
                    msg = result["body"]
                self._log(f"  ✗  {username:<28}  [{result['status']}] {msg}", "err")
                fail_count += 1

            self.progress["value"] = i
            time.sleep(0.3)

        self._log(f"\nГотово: {ok_count} успешно, {fail_count} ошибок.", "heading")


# ── точка входа ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()