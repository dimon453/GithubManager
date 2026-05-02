#!/usr/bin/env python3
"""
GitHub Collaborator Adder — GUI (tkinter)
Цветовая схема: фон #0E0E0B, акцент #AFE607
Языки: RU / EN / RO
"""

import json
import os
import ssl
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
MUTED    = "#555550"
FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
FONT_BIG = ("Segoe UI", 13, "bold")

PERMISSION_CHOICES = ["pull", "push", "maintain", "triage", "admin"]
USERDATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "USERDATA.json")
SSL_CONTEXT   = ssl.create_default_context(cafile=certifi.where())

# ── переводы ──────────────────────────────────────────────────────────────────

STRINGS = {
    "RU": {
        "title":        "GitHub Collaborator Adder",
        "lbl_file":     "Файл с никами",
        "lbl_repo":     "Репозиторий (OWNER/REPO)",
        "lbl_user":     "GitHub Username",
        "lbl_token":    "GitHub Token",
        "lbl_perm":     "Разрешение",
        "btn_browse":   "Обзор",
        "btn_run":      "▶  Добавить collaborators",
        "chk_save":     "Сохранить username и токен в USERDATA.json",
        "saved":        "Сохранено в USERDATA.json",
        "err_nofile":   "Укажи путь к файлу с никами.",
        "err_notfound": "Файл не найден: {}",
        "err_repo":     "Репозиторий должен быть в формате OWNER/REPO.",
        "err_nouser":   "Укажи GitHub username.",
        "err_notoken":  "Укажи GitHub Token.",
        "err_empty":    "Файл пуст или не содержит ников.",
        "log_repo":     "Репозиторий : {}/{}",
        "log_perm":     "Разрешение  : {}",
        "log_total":    "Всего ников : {}",
        "log_invited":  "приглашение отправлено",
        "log_already":  "уже collaborator",
        "log_done":     "Готово: {} успешно, {} ошибок.",
        "footer":       "Proudly made by Popov Dmitrii",
    },
    "EN": {
        "title":        "GitHub Collaborator Adder",
        "lbl_file":     "Usernames file",
        "lbl_repo":     "Repository (OWNER/REPO)",
        "lbl_user":     "GitHub Username",
        "lbl_token":    "GitHub Token",
        "lbl_perm":     "Permission",
        "btn_browse":   "Browse",
        "btn_run":      "▶  Add collaborators",
        "chk_save":     "Save username and token to USERDATA.json",
        "saved":        "Saved to USERDATA.json",
        "err_nofile":   "Please specify a path to the usernames file.",
        "err_notfound": "File not found: {}",
        "err_repo":     "Repository must be in OWNER/REPO format.",
        "err_nouser":   "Please enter your GitHub username.",
        "err_notoken":  "Please enter your GitHub Token.",
        "err_empty":    "File is empty or contains no usernames.",
        "log_repo":     "Repository : {}/{}",
        "log_perm":     "Permission  : {}",
        "log_total":    "Total users : {}",
        "log_invited":  "invitation sent",
        "log_already":  "already a collaborator",
        "log_done":     "Done: {} succeeded, {} failed.",
        "footer":       "Proudly made by Popov Dmitrii",
    },
    "RO": {
        "title":        "GitHub Collaborator Adder",
        "lbl_file":     "Fișier cu utilizatori",
        "lbl_repo":     "Depozit (OWNER/REPO)",
        "lbl_user":     "Nume utilizator GitHub",
        "lbl_token":    "Token GitHub",
        "lbl_perm":     "Permisiune",
        "btn_browse":   "Răsfoire",
        "btn_run":      "▶  Adaugă colaboratori",
        "chk_save":     "Salvează utilizatorul și tokenul în USERDATA.json",
        "saved":        "Salvat în USERDATA.json",
        "err_nofile":   "Specifică calea către fișierul cu utilizatori.",
        "err_notfound": "Fișierul nu a fost găsit: {}",
        "err_repo":     "Depozitul trebuie să fie în formatul OWNER/REPO.",
        "err_nouser":   "Introdu numele de utilizator GitHub.",
        "err_notoken":  "Introdu tokenul GitHub.",
        "err_empty":    "Fișierul este gol sau nu conține utilizatori.",
        "log_repo":     "Depozit    : {}/{}",
        "log_perm":     "Permisiune : {}",
        "log_total":    "Utilizatori: {}",
        "log_invited":  "invitație trimisă",
        "log_already":  "deja colaborator",
        "log_done":     "Gata: {} reușite, {} eșuate.",
        "footer":       "Proudly made by Popov Dmitrii",
    },
}

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
        self.lang = "RU"
        self.resizable(False, False)
        self.configure(bg=BG)
        self.userdata = load_userdata()
        self._build_ui()
        self._load_saved()
        self._apply_lang()

    def t(self, key, *args):
        s = STRINGS[self.lang][key]
        return s.format(*args) if args else s

    # ── стили ─────────────────────────────────────────────────────────────────

    def _entry(self, parent, textvariable):
        return tk.Entry(
            parent, textvariable=textvariable,
            bg=BG3, fg=FG, insertbackground=ACCENT,
            relief="flat", font=FONT,
            highlightthickness=1, highlightcolor=ACCENT,
            highlightbackground="#333330",
        )

    def _label(self, parent, text="", bold=False):
        return tk.Label(parent, text=text, bg=BG,
                        fg=ACCENT if bold else FG,
                        font=FONT_B if bold else FONT)

    def _btn(self, parent, text, cmd, small=False):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=ACCENT, fg=BG, activebackground="#c8f010",
            activeforeground=BG, font=FONT_B if not small else FONT,
            relief="flat", cursor="hand2",
            padx=10 if not small else 6, pady=4,
        )

    # ── построение UI ─────────────────────────────────────────────────────────

    def _build_ui(self):
        pad = {"padx": 20, "pady": 6}

        # — шапка —
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(18, 2))

        self.lbl_title = tk.Label(header, text="", bg=BG, fg=ACCENT, font=FONT_BIG)
        self.lbl_title.pack(side="left")

        # кнопки языков
        lang_frame = tk.Frame(header, bg=BG)
        lang_frame.pack(side="right")
        self.lang_btns = {}
        for lang in ("RU", "EN", "RO"):
            b = tk.Button(
                lang_frame, text=lang, width=3,
                relief="flat", cursor="hand2", font=FONT_B,
                command=lambda l=lang: self._switch_lang(l),
            )
            b.pack(side="left", padx=2)
            self.lang_btns[lang] = b
        self._update_lang_btns()

        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x", padx=20, pady=(4, 10))

        # — форма —
        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", **pad)
        form.columnconfigure(1, weight=1)

        # файл
        self.lbl_file = self._label(form)
        self.lbl_file.grid(row=0, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_file = tk.StringVar()
        file_frame = tk.Frame(form, bg=BG)
        file_frame.grid(row=0, column=1, sticky="ew", pady=5)
        file_frame.columnconfigure(0, weight=1)
        self._entry(file_frame, self.var_file).grid(row=0, column=0, sticky="ew", ipady=4)
        self.btn_browse = self._btn(file_frame, "", self._browse, small=True)
        self.btn_browse.grid(row=0, column=1, padx=(6, 0))

        # репозиторий
        self.lbl_repo = self._label(form)
        self.lbl_repo.grid(row=1, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_repo = tk.StringVar()
        self._entry(form, self.var_repo).grid(row=1, column=1, sticky="ew", ipady=4, pady=5)

        # username
        self.lbl_user = self._label(form)
        self.lbl_user.grid(row=2, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_user = tk.StringVar()
        self._entry(form, self.var_user).grid(row=2, column=1, sticky="ew", ipady=4, pady=5)

        # токен
        self.lbl_token = self._label(form)
        self.lbl_token.grid(row=3, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_token = tk.StringVar()
        self._entry(form, self.var_token).grid(row=3, column=1, sticky="ew", ipady=4, pady=5)

        # permission
        self.lbl_perm = self._label(form)
        self.lbl_perm.grid(row=4, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_perm = tk.StringVar(value="push")
        perm_frame = tk.Frame(form, bg=BG)
        perm_frame.grid(row=4, column=1, sticky="w", pady=5)
        for p in PERMISSION_CHOICES:
            tk.Radiobutton(
                perm_frame, text=p, variable=self.var_perm, value=p,
                bg=BG, fg=FG, selectcolor=BG2,
                activebackground=BG, activeforeground=ACCENT, font=FONT,
            ).pack(side="left", padx=(0, 10))

        # чекбокс сохранить
        self.var_save = tk.BooleanVar(value=True)
        self.chk_save = tk.Checkbutton(
            self, variable=self.var_save,
            bg=BG, fg=FG, selectcolor=BG2,
            activebackground=BG, activeforeground=ACCENT, font=FONT,
        )
        self.chk_save.pack(anchor="w", padx=20, pady=(0, 4))

        # кнопка запуска
        self.btn_run = self._btn(self, "", self._run)
        self.btn_run.pack(fill="x", padx=20, pady=(4, 10), ipady=6)

        # прогресс-бар
        self.progress = ttk.Progressbar(self, mode="determinate", length=400)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TProgressbar",
                        troughcolor=BG3, background=ACCENT,
                        bordercolor=BG, lightcolor=ACCENT, darkcolor=ACCENT)
        self.progress.pack(fill="x", padx=20, pady=(0, 6))

        # лог
        log_frame = tk.Frame(self, bg=BG2,
                             highlightbackground=ACCENT, highlightthickness=1)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.log = tk.Text(
            log_frame, bg=BG2, fg=FG, font=("Consolas", 9),
            relief="flat", state="disabled", wrap="word", height=12,
        )
        sb = tk.Scrollbar(log_frame, command=self.log.yview, bg=BG3,
                          troughcolor=BG3, relief="flat")
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        sb.pack(side="right", fill="y")
        self.log.tag_config("ok",      foreground=ACCENT)
        self.log.tag_config("err",     foreground=RED)
        self.log.tag_config("info",    foreground=FG)
        self.log.tag_config("heading", foreground=ACCENT, font=FONT_B)

        # футер
        self.lbl_footer = tk.Label(self, bg=BG, fg=MUTED, font=("Segoe UI", 8))
        self.lbl_footer.pack(pady=(0, 10))

    # ── язык ──────────────────────────────────────────────────────────────────

    def _switch_lang(self, lang):
        self.lang = lang
        self._update_lang_btns()
        self._apply_lang()

    def _update_lang_btns(self):
        for lang, btn in self.lang_btns.items():
            if lang == self.lang:
                btn.configure(bg=ACCENT, fg=BG)
            else:
                btn.configure(bg=BG3, fg=FG)

    def _apply_lang(self):
        self.title(self.t("title"))
        self.lbl_title.configure(text=self.t("title"))
        self.lbl_file.configure(text=self.t("lbl_file"))
        self.lbl_repo.configure(text=self.t("lbl_repo"))
        self.lbl_user.configure(text=self.t("lbl_user"))
        self.lbl_token.configure(text=self.t("lbl_token"))
        self.lbl_perm.configure(text=self.t("lbl_perm"))
        self.btn_browse.configure(text=self.t("btn_browse"))
        self.btn_run.configure(text=self.t("btn_run"))
        self.chk_save.configure(text=self.t("chk_save"))
        self.lbl_footer.configure(text=self.t("footer"))

    # ── прочее ────────────────────────────────────────────────────────────────

    def _load_saved(self):
        saved_user = self.userdata.get("github_username", "")
        self.var_user.set(saved_user)
        self.var_token.set(self.userdata.get("github_token", ""))
        # подставить username/ в поле репозитория
        if saved_user:
            self.var_repo.set(saved_user + "/")
        # следить за изменением username → обновлять префикс репо
        self.var_user.trace_add("write", self._on_user_change)

    def _on_user_change(self, *_):
        user = self.var_user.get().strip()
        repo = self.var_repo.get()
        # обновляем только часть до первого /
        if "/" in repo:
            after_slash = repo.split("/", 1)[1]
        else:
            after_slash = ""
        self.var_repo.set((user + "/" + after_slash) if user else after_slash)

    def _browse(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            self.var_file.set(path)

    def _log(self, text, tag="info"):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n", tag)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _log_clear(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _run(self):
        file_path = self.var_file.get().strip()
        repo_raw  = self.var_repo.get().strip()
        gh_user   = self.var_user.get().strip()
        token     = self.var_token.get().strip()
        perm      = self.var_perm.get()

        errors = []
        if not file_path:
            errors.append(self.t("err_nofile"))
        elif not os.path.isfile(file_path):
            errors.append(self.t("err_notfound", file_path))
        if not repo_raw or len(repo_raw.split("/")) != 2:
            errors.append(self.t("err_repo"))
        if not gh_user:
            errors.append(self.t("err_nouser"))
        if not token:
            errors.append(self.t("err_notoken"))
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
            self._log("⚠  " + self.t("err_empty"), "err")
            return

        saved_user  = self.userdata.get("github_username", "")
        saved_token = self.userdata.get("github_token", "")
        if self.var_save.get() and (gh_user != saved_user or token != saved_token):
            save_userdata(gh_user, token)
            self.userdata = {"github_username": gh_user, "github_token": token}

        threading.Thread(
            target=self._worker,
            args=(owner, repo, token, perm, usernames),
            daemon=True,
        ).start()

    def _worker(self, owner, repo, token, perm, usernames):
        self._log_clear()
        self._log(self.t("log_repo", owner, repo), "heading")
        self._log(self.t("log_perm", perm),         "heading")
        self._log(self.t("log_total", len(usernames)) + "\n", "heading")

        self.progress["maximum"] = len(usernames)
        self.progress["value"]   = 0

        ok_count = fail_count = 0

        for i, username in enumerate(usernames, 1):
            result = add_collaborator(owner, repo, username, token, perm)
            if result["ok"]:
                tag_text = self.t("log_invited") if result["status"] == 201 \
                           else self.t("log_already")
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

        self._log("\n" + self.t("log_done", ok_count, fail_count), "heading")


if __name__ == "__main__":
    app = App()
    app.mainloop()